"""笛の印刷向きの安定性を調べる試験片。

いま実績があるのは「横置き・窓がz+方向に開口」だけである（外見統一版のコームや
カード、スプールはすべてこれ）。日用品に埋め込むには他の向きでも鳴る必要があるので、
向きを1つずつ変えて確かめる。この生成器は段階(2)「横置き・窓が水平方向に開口」の
試験片を作る。

作りは、62.07×7×7mm の直方体を長辺が横になるように置き、その側面に外見統一版の
笛を1本、窓が水平方向へ開口するように接する。直方体が土台と支えを兼ねるので、
笛そのものは寝かせたまま、窓の向きだけが90度変わる。
"""
from __future__ import annotations
import argparse, os, sys
import numpy as np
import trimesh
from trimesh import transformations as tf

sys.path.insert(0, os.path.dirname(__file__))
import mini10

BAR = 7.0        # 土台の直方体の断面（7×7mm）
OVER = 0.3       # 笛の床へ食い込ませて確実に一体化させる量


def build(note="C7", notes=None, bar=BAR):
    """段階(2)の試験片を作る。戻り値 (mesh, flute, 情報dict)。"""
    notes = notes or (mini10.CALIB11 + ["G7"])          # 12音 G#6〜G7
    L_max = max(mini10.length_for_note(n) for n in notes)
    L = mini10.length_for_note(note)
    g = mini10.uniform_flute(L, L_max=L_max)            # native: 窓=+z, 床=z=0, 長さ=+x
    # x軸まわり -90度: 窓(+z)を +y へ、幅(+y)を -z へ。窓が水平方向に開く。
    R = np.eye(4); R[:3, :3] = np.array([[1, 0, 0], [0, 0, 1], [0, -1, 0]], float)
    assert abs(np.linalg.det(R[:3, :3]) - 1) < 1e-9
    g.apply_transform(R)
    b = g.bounds
    g.apply_translation([-b[0][0], -b[0][1], -b[0][2]])  # 原点へ
    gb = g.bounds
    # 土台は笛の床側(y<0)に接する。窓のある +y 側には何も置かない。
    barbox = trimesh.creation.box(extents=[L_max, bar + OVER, bar])
    barbox.apply_translation([L_max / 2, -(bar + OVER) / 2 + OVER, bar / 2])
    mesh = trimesh.boolean.union([barbox, g], engine="manifold")
    info = dict(note=note, L=round(L, 2), L_max=round(L_max, 2),
                extents=tuple(np.round(mesh.extents, 2)))
    return mesh, g, info


def verify(mesh, g):
    """ボアが中空か、窓と吸込口が空気に開いているかを実メッシュで確かめる。"""
    gb = g.bounds
    zc = (gb[0][2] + gb[1][2]) / 2
    L = gb[1][0] - gb[0][0]
    out = {}
    pts = [[gb[0][0] + t * L, gb[0][1] + 1.7, zc] for t in np.linspace(0.25, 0.85, 7)]
    out["ボアが中空"] = bool((~mesh.contains(np.array(pts))).all())
    wp = [[gb[0][0] + d, gb[1][1] + o, zc] for d in (13.0, 16.0, 19.0) for o in (1.0, 3.0, 6.0)]
    out["窓の前が空気"] = bool((~mesh.contains(np.array(wp))).all())
    mp = [[gb[0][0] - 2.0, gb[0][1] + 1.7, zc]]
    out["吸込口の外が空気"] = bool((~mesh.contains(np.array(mp))).all())
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description="印刷向きの試験片(段階2: 窓が水平方向)")
    ap.add_argument("--note", default="C7", help="使う音（既定 C7）")
    ap.add_argument("--out", default="out/orient2_window_horizontal.stl")
    a = ap.parse_args(argv)
    mesh, g, info = build(a.note)
    res = verify(mesh, g)
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    mesh.export(a.out)
    print("段階(2) 横置き・窓が水平方向に開口")
    print("  音 %s（管長 %.2fmm・外形は12音のL_max %.2fmm に統一）" % (info["note"], info["L"], info["L_max"]))
    print("  外形 %s mm  watertight=%s" % (info["extents"], mesh.is_watertight))
    for k, v in res.items():
        print("   %-16s %s" % (k, "OK" if v else "**NG**"))
    print("  ->", a.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
