"""勝ちパターン(壁1mm・深い窓)の較正コームと音階限界コームを生成する。

対象:
  mini10 = 半割(D字)・深い窓  … mini10/recorder-mini-c-v3-half-2-v2.stl
  rect   = 直方体・深い窓      … mini-rect/recorder-mini-c-half-rect-1-v1.stl

いずれも「頭部・窓・壁」を固定し、フット(x>=thr)を平行移動して総管長 L を変える(halfcutと同じ)。
較正用の目安 f=A/(L+e)（旧半割の実測フィット・A=89086, e=-10.9）で予測周波数を併記する。
各笛は独立オブジェクトとして幅方向に並べ、吸込口(x最小)をそろえてベッドに平置きで出力する。
"""
import os
import numpy as np
import trimesh

HERE = os.path.dirname(__file__)
ROOT = os.path.join(HERE, os.pardir)
OUT = os.path.join(ROOT, "out")

A, E = 89086.0, -10.9
def predf(L): return A / (L + E)

GEOM = {
    "mini10": dict(stl=os.path.join(ROOT, "mini10/recorder-mini-c-v3-half-2-v2.stl"),
                   thr=17.0, base=60.0, step=11.0),   # 幅y=7 → 11間隔
    "rect":   dict(stl=os.path.join(ROOT, "mini-rect/recorder-mini-c-half-rect-1-v1.stl"),
                   thr=-16.0, base=60.0, step=12.0),  # 幅y=4・窓横向き → 12間隔
}

CALIB = [40, 46, 52, 58, 64, 70]
LIMIT = [28, 32, 36, 76, 84, 92]


def make_flute(g, L):
    m = trimesh.load(g["stl"]).copy()
    v = m.vertices.copy()
    v[v[:, 0] >= g["thr"], 0] += (L - g["base"])
    m.vertices = v
    m.merge_vertices()
    # 吸込口(x最小)を0へ、ベッド(z最小)を0へ
    b = m.bounds
    m.apply_translation([-b[0][0], 0, -b[0][2]])
    return m


def build_comb(gname, lengths, tag):
    g = GEOM[gname]
    parts = []
    y = 0.0
    infos = []
    for L in lengths:
        f = make_flute(g, L)
        b = f.bounds
        f.apply_translation([0, -b[0][1] + y, 0])   # 幅方向に y だけずらす
        parts.append(f)
        infos.append((L, round(predf(L))))
        y += g["step"]
    comb = trimesh.util.concatenate(parts)
    # ベッド中央(H2D 350x160)へ
    c = (comb.bounds[0] + comb.bounds[1]) / 2
    comb.apply_translation([175 - c[0], 160 - c[1], 0])
    path = os.path.join(OUT, "comb_%s_%s.stl" % (gname, tag))
    comb.export(path)
    print("%s: %s  笛%d本 ext=%s wt=%s" % (
        os.path.basename(path), [i[0] for i in infos], len(lengths),
        np.round(comb.extents, 1).tolist(), comb.is_watertight))
    print("   L→予測Hz:", ", ".join("%d→%d" % (L, f) for L, f in infos))
    return path


if __name__ == "__main__":
    for gname in ["mini10", "rect"]:
        build_comb(gname, CALIB, "calib")
        build_comb(gname, LIMIT, "limit")
