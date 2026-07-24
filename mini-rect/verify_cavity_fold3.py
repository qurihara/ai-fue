"""fold3_rect_3cand の スライス済み3mf で、折り笛のボア空洞(U字含む)が無充填かを実gcodeで確認する。

方針:
  1) 元STL(out/fold3_rect_3cand_a1m.stl)を z=Zcut で水平断面にする。断面の充填領域(polygons_full)が材料。
     各笛の断面には bore が「穴(hole)」として現れる。穴の内部＝ボア空洞。
  2) 断面のバウンディング内に格子点を撒き、材料多角形の外(=穴 or 外側)を拾い、
     さらに各笛の外形の中に入っている点だけ(=内部の穴=ボア)に絞る。
  3) その点を 3mf の build item transform でベッド座標へ写し、gcode の当該層の押出線分との最短距離を測る。
     距離が線幅の半分(≈0.25mm)より大きければ「その点に材料は通っていない=無充填」。
     ボア点のどれかが押出線に乗っていれば「充填=NG」。
実行: /Users/kurihara/Desktop/claude_work/mesh_venv/bin/python mini-rect/verify_cavity_fold3.py
"""
import os
import sys
import zipfile
import numpy as np
import trimesh
from shapely.geometry import Point

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, os.pardir, "fue"))
import check_cavity as CC

ROOT = os.path.join(HERE, os.pardir)
# 既定は fold3。引数で STL と スライス済み3mf を差し替え可能（fold4検証用）。
STL = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "out", "fold3_rect_3cand_a1m.stl")
MF = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "temp", "fold3_rect_3cand_a1m_sliced.3mf")
OUTPNG = sys.argv[3] if len(sys.argv) > 3 else os.path.join(ROOT, "out", "fold3_cavity_check.png")
ZCUT = 3.5           # ボア中心高さ
GRID = 0.5           # 格子間隔[mm]
FILL_THR = 0.30      # ベッド上でこの距離[mm]以内に押出線があれば「材料が通っている=充填」


def section_polys(mesh, z):
    sec = mesh.section(plane_origin=[0, 0, z], plane_normal=[0, 0, 1])
    if sec is None:
        return None
    p2d, _ = sec.to_planar()
    return p2d


def main():
    mesh = trimesh.load(STL)
    print("STL bounds:", np.round(mesh.bounds, 2).tolist())
    p2d = section_polys(mesh, ZCUT)
    filled = p2d.polygons_full          # 材料(穴を除いた充填領域)
    # to_planar は原点を移動しうるので、STL座標へ戻す変換を取得
    T = p2d.metadata.get("to_3D")
    # to_3D: 3x? -> use it to map 2D pt to 3D. We only need x,y in STL frame.
    # trimesh returns to_3D as 4x4. 2D (u,v)->3D.
    to3d = np.asarray(T)

    from shapely.ops import unary_union
    material = unary_union(list(filled))       # 実際の材料(断面の充填領域)
    bb = np.asarray(p2d.bounds).reshape(-1)
    minx, miny, maxx, maxy = bb[0], bb[1], bb[2], bb[3]

    # ボア(内部チャンネル)判定:
    #   このボアは窓開口で外気とつながるため断面では「島状の穴」にならない。
    #   代わりに「材料でない点で、y方向の両側が近く(<=YENC mm)で材料に挟まれている点」を
    #   内部チャンネル(=bore1/bore2 は x に走り y で挟まれる)として拾う。
    YENC = 2.5   # 両側材料までこの距離以内なら内部チャンネルとみなす
    def solid(u, v):
        return material.contains(Point(u, v))
    def enclosed_y(u, v):
        up = any(solid(u, v + d) for d in np.arange(0.2, YENC + 0.01, 0.2))
        dn = any(solid(u, v - d) for d in np.arange(0.2, YENC + 0.01, 0.2))
        return up and dn
    bore_uv = []
    xs = np.arange(minx, maxx, GRID)
    ys = np.arange(miny, maxy, GRID)
    for u in xs:
        for v in ys:
            if not solid(u, v) and enclosed_y(u, v):
                bore_uv.append((u, v))
    bore_uv = np.array(bore_uv)
    print("ボア(内部チャンネル)サンプル点数:", len(bore_uv))
    if len(bore_uv) == 0:
        print("★ボア点が拾えなかった。YENC/断面高さを調整して再確認。")
        return

    # 2D(u,v) -> STL(x,y)
    def uv_to_xy(u, v):
        p = to3d @ np.array([u, v, 0.0, 1.0])
        return p[0], p[1]
    bore_xy = np.array([uv_to_xy(u, v) for u, v in bore_uv])

    # STL(x,y) -> ベッド(x,y)
    f, m = CC.bed_transform(MF)
    bore_bed = np.array([f(x, y, ZCUT) for x, y in bore_xy])

    # gcode を取り出して当該層の線分を得る
    with zipfile.ZipFile(MF) as z:
        g = z.read("Metadata/plate_1.gcode")
    gpath = os.path.join(HERE, os.pardir, "temp", "_plate_1.gcode")
    open(gpath, "wb").write(g)
    segs = CC.load_segments(gpath)
    zk = min(segs.keys(), key=lambda k: abs(k - ZCUT))
    S = np.array(segs[zk])
    print("使用gcode層 z=%.2f (目標%.1f) 線分数=%d" % (zk, ZCUT, len(S)))

    # 各ボア点の最短距離
    dmin = np.array([CC.dist_to_segments(px, py, S) for px, py in bore_bed])
    # 壁際の境界点(内壁ペリメータのすぐ内側)は当然ペリメータ線に近い。
    # 充填の有無は「壁から十分離れた深部ボア点」で判定する。
    from shapely.ops import unary_union as _uu  # material は uv 座標系。深さは uv で測る
    wall_dist = np.array([material.distance(Point(u, v)) for u, v in bore_uv])  # 材料(壁)までの距離[mm]
    DEEP = 0.55   # 壁からこの距離より内側=深部(ペリメータの影響を受けない)
    deep = wall_dist >= DEEP
    print("深部ボア点(壁から>=%.2fmm): %d / %d" % (DEEP, int(deep.sum()), len(dmin)))
    print("全ボア点の 材料までの最短距離 min/median/max = %.2f / %.2f / %.2f mm" % (
        dmin.min(), np.median(dmin), dmin.max()))
    if deep.any():
        dd = dmin[deep]
        deep_filled = int((dd < FILL_THR).sum())
        print("深部ボア点の 押出線までの距離 min/median/max = %.2f / %.2f / %.2f mm" % (
            dd.min(), np.median(dd), dd.max()))
        print("深部ボア点で押出線が横切る(<%.2fmm)点数: %d / %d" % (FILL_THR, deep_filled, len(dd)))
        if deep_filled == 0:
            print("★判定: ボア空洞(深部)は無充填 = OK。赤点は壁際ペリメータ隣接のみ。")
        else:
            print("★判定: 深部で %d 点が充填の疑い = 要確認" % deep_filled)
    else:
        print("★判定: 深部点が無い。DEEPを下げて再確認。")

    # 可視化(ベッド座標): 押出線分と ボア点
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(10, 6))
        for (x0, y0, x1, y1) in S:
            ax.plot([x0, x1], [y0, y1], color="0.5", lw=0.3)
        good = dmin >= FILL_THR
        ax.scatter(bore_bed[good, 0], bore_bed[good, 1], s=4, c="lime", label="bore void (unfilled OK)")
        if (~good).any():
            ax.scatter(bore_bed[~good, 0], bore_bed[~good, 1], s=8, c="red", label="filled?!")
        ax.set_aspect("equal")
        ax.set_title("rect fold  layer z=%.2f  extrusion(gray) vs bore-void(green)" % zk)
        ax.legend(loc="upper right")
        plt.savefig(OUTPNG, dpi=110, bbox_inches="tight")
        print("wrote", OUTPNG)
    except Exception as e:
        print("plot skipped:", e)


if __name__ == "__main__":
    main()
