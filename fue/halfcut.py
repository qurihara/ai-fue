"""半割り極薄笛（v2円筒を管軸方向に半割りしたD字断面）の較正コーム。

実績: mini/recorder-mini-c-v3-half-v2-40.stl (管長40mm)=約3.5kHz(≈A7)、-60.stl(60mm)=約1.83kHz(≈A6)。
＝長さ40→60mm でほぼ1オクターブ。長さは「頭部・窓(x<=14 固定)＋フット(x>=20)を平行移動」で
完全にパラメトリック化できる（-60 は -40 のフットを +20mm した実体と体積差1.1%で一致を確認）。

この較正コームで「管長→音程」を実測し、ダイアトニック(オクターブ)の各長さを確定する。
角柱では作らず、必ず元と同じ半割り(D字/半円状ボア)のまま長さだけ変える。
"""
import os
import sys
import numpy as np
import trimesh

sys.path.insert(0, os.path.dirname(__file__))

OUT = os.path.join(os.path.dirname(__file__), os.pardir, "out")
BASE_STL = os.path.join(os.path.dirname(__file__), os.pardir, "mini", "recorder-mini-c-v3-half-v2-40.stl")

# 半割り笛の x 構造（-40 実測）: 吸込口 x=-4 / 窓・ラビウム x=8〜14 / 直管フット x=14〜35 / 端面 x=36。
# 窓より先(x>=FOOT_THR)だけを平行移動すればフット長=総管長が変わる（頭部・窓は不変）。
FOOT_THR = 20.0
BASE_LEN = 40.0

# 実測アンカー2点からの log 線形補間（f = f40 * exp(k*(L-40))）。あくまで概算＝要実測。
_F40, _F60 = 3500.0, 1830.0
_K = np.log(_F60 / _F40) / (60.0 - 40.0)          # ≈ -0.0325 /mm （1オクターブ≈21.3mm）


def est_freq(L):
    """2アンカーの log 線形補間による概算周波数[Hz]（要実測で較正）。"""
    return _F40 * np.exp(_K * (L - BASE_LEN))


def half_flute(L, base=None):
    """管長 L[mm] の半割り笛メッシュ（元STL native向き: x=管軸, y=厚み4, z=幅7, 窓=y最小面）。
    頭部・窓は不変のまま、フット(x>=FOOT_THR)を平行移動して総管長を L にする。"""
    m = (base if base is not None else trimesh.load(BASE_STL)).copy()
    v = m.vertices.copy()
    v[v[:, 0] >= FOOT_THR, 0] += (L - BASE_LEN)
    m.vertices = v
    return m


def _printpose(m):
    """印刷姿勢: 平坦面(窓, y最小)を下・丸い背(y最大)を上にした平置き＝サポートフリー。
    実績単体印刷と同じく厚み4mmを垂直(z)にする。x軸まわり+90°で y→z。"""
    m = m.copy()
    m.apply_transform(trimesh.transformations.rotation_matrix(np.radians(90), [1, 0, 0]))
    m.apply_translation([0, 0, -m.bounds[0][2]])          # ベッド(z=0)へ落とす
    return m


def half_calib_comb(lengths=None, gap=0.0, merge=True, overlap=0.3):
    """長さ違いの半割り笛を一列に並べた較正コーム。全笛の吸込口(x=0)を揃え、フットが長いほど
    +x へ伸びる。幅方向(y)に gap を空けて並べる（gap=0 で隙間なく密着）。
    merge=True: 密着した笛を boolean union で一体のwatertight連結コームにする（各ボアは独立のまま
    残る＝実績パンフルートと同じ密閉。union を確実にするため密着時は overlap だけ食い込ませる）。"""
    if lengths is None:
        lengths = [36, 40, 44, 48, 52, 56, 60, 64]        # 4mm刻み・アンカー40/60含む・約1.3oct
    base = trimesh.load(BASE_STL)
    flutes, infos = [], []
    y = 0.0
    for L in lengths:
        f = _printpose(half_flute(L, base=base))
        b = f.bounds
        f.apply_translation([-b[0][0], -b[0][1] + y, 0])  # 吸込口を x=0、幅方向に y だけずらす
        fb = f.bounds
        w = fb[1][1] - fb[0][1]
        infos.append(dict(L=L, y=round(y, 1), freq=est_freq(L), x_foot=round(fb[1][0], 1)))
        step = w + gap
        if merge and gap == 0.0:
            step -= overlap                               # 密着時は微小に重ねて union を確実化
        y += step
        flutes.append(f)
    if merge:
        comb = trimesh.boolean.union(flutes, engine="manifold")
    else:
        comb = trimesh.util.concatenate(flutes)
    return comb, infos


def _render(comb, infos, path):
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    b = comb.bounds
    fig = plt.figure(figsize=(14, 6))
    for i, (t, (el, az)) in enumerate([("iso", (28, -60)), ("top (windows down)", (88, -90))]):
        ax = fig.add_subplot(1, 2, i + 1, projection="3d")
        ax.add_collection3d(Poly3DCollection(comb.triangles, alpha=0.55, facecolor="#8fb0e0", edgecolor="#456"))
        ax.set_xlim(b[0][0], b[1][0]); ax.set_ylim(b[0][1], b[1][1]); ax.set_zlim(b[0][2] - 1, b[0][2] + (b[1][1] - b[0][1]))
        ax.view_init(elev=el, azim=az); ax.set_title(t, fontsize=9)
        ax.set_xlabel("x(bore)"); ax.set_ylabel("y(row)"); ax.set_zlabel("z")
    plt.tight_layout(); plt.savefig(path, dpi=95); plt.close()


def main():
    os.makedirs(OUT, exist_ok=True)
    comb, infos = half_calib_comb()
    name = os.path.join(OUT, "halfcut_calib_comb.stl")
    comb.export(name)
    print("半割り笛 較正コーム（D字断面のまま長さのみ可変・平置きサポートフリー）:")
    print("  管長→概算音程（要実測。log補間 f=%.0f*exp(%.4f*(L-40)); 1oct≈%.1fmm）" % (_F40, _K, np.log(2) / -_K))
    for it in infos:
        print("    L=%2dmm  行y=%5.1f  概算 %5.0fHz  フット先 x=%.1f" % (it["L"], it["y"], it["freq"], it["x_foot"]))
    print("  笛数=%d 外形=%s watertight=%s -> %s" %
          (len(infos), tuple(np.round(comb.extents, 1)), comb.is_watertight, name))
    _render(comb, infos, os.path.join(OUT, "halfcut_calib_comb_views.png"))
    print("  render -> out/halfcut_calib_comb_views.png")


if __name__ == "__main__":
    main()
