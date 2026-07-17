"""笛つき名刺：日本の一般的な名刺(91×55mm・横)の板と、半割り笛の音階コームを融合した一体物。

着想: E major コーム(E6→E7の8本)の幅が 53.9mm で、名刺の短辺 55mm とほぼ同じ。
笛はいまの向き(丸背=上・平坦面=下、管軸=x)のまま、板と**同じ z=0 に置いて融合**する。

板は笛の床そのもの（積み増さない）:
  半割り笛のボア床は実測 z=0〜0.495mm（側壁0.52・丸背の天井0.48。ほぼ全部0.5mm前後）。
  そこで板厚も 0.5mm にして両方 z=0 に置くと、板の上面がちょうどボアの床と一致し、板は
  「笛の床を名刺サイズまで外へ広げた1枚のシート」になる。総厚は笛そのままの 4.0mm。
  （板を笛の下に貼る旧案は 0.8mm 積み増して 4.7mm になっていた。ボアには当たらないが厚い。）

底面側に板を足しても鳴る理由（実形状を断面で確認済み・2026/7/17）:
  - 窓/ラビウムは x≈11.5〜15.5 で**上面(丸背側)**が切り欠かれた開口。底ではない。
  - 吹き込み口は x=0 の**端面**（風道は上半分 z≈2.1〜3.3 を通る）。底ではない。
  - 底面(z=0)は全長にわたり実体の床。板はその床と同じ層に融合するだけ。
つまり板は発音経路をどこも塞がない。

レイアウト: 吹き込み口(x=0)を板の短辺に端揃え。笛の列(53.9mm)は板の55mmに対して幅方向センタリング。
最長のE6が78.5mmなので板の反対端に 91-78.5=12.5mm の余白が残る＝ここが名前を書ける帯になる。

四隅の角取り(CORNER_R): 角は板だけでなく笛ごと垂直に落とす（板だけ落とすと両端の笛 E6/E7 が
角より外へ飛び出して尖りが残り、しかも板の無い所で宙に浮く）。ただし E6/E7 は板端 y=0.55mm まで
来ていて、その内側 y≈0.96〜1.52mm が風道の側壁(厚0.56mm)。R を大きくすると口元でこの壁を破って
息が漏れる。実測(x=0.3, z=2.8 で風道内面 y=1.52)から R=2.0 が安全上限に近い:
  R=2 → 壁を削るのは x<0.29 のみ・風道に届くのは x<0.06（実質無害）
  R=3 → x<0.39 で風道の側壁を貫通＝口元に切り欠きができる
"""
import os
import sys
import numpy as np
import trimesh
from shapely.geometry import box as sbox

sys.path.insert(0, os.path.dirname(__file__))
import halfcut

OUT = os.path.join(os.path.dirname(__file__), os.pardir, "out")

CARD_X = 91.0        # 日本の一般的な名刺（横）
CARD_Y = 55.0
CARD_Z = 0.5         # = 半割り笛のボア床の厚さ(実測0.495mm)。板の上面がボアの床と一致し積み増しゼロになる
CORNER_R = 2.0       # 四隅の角取り量[mm]。E6/E7 の風道側壁を破らない安全上限が約2.0（上の説明参照）


def _corner_prism(cx, cy, r, style, z0, z1):
    """四隅を落とした板外形の角柱（全高を貫く切り抜き用）。style='round'=R面 / 'chamfer'=C面(45°)。"""
    join = 1 if style == "round" else 3          # shapely: 1=round, 3=bevel(=45°面取り)
    poly = sbox(r, r, cx - r, cy - r).buffer(r, join_style=join, resolution=32)
    prism = trimesh.creation.extrude_polygon(poly, height=z1 - z0)
    prism.apply_translation([0, 0, z0])
    return prism


def build(notes=None, card=(CARD_X, CARD_Y, CARD_Z),
          corner_r=CORNER_R, corner_style="round"):
    """笛つき名刺メッシュを作る。戻り値 (mesh, info)。"""
    if notes is None:
        notes = halfcut.E_MAJOR
    cx, cy, cz = card
    comb, infos, notes, lengths = halfcut.scale_comb(notes=notes)
    b = comb.bounds
    comb.apply_translation([-b[0][0], -b[0][1], -b[0][2]])     # 吸込口 x=0 / 列 y=0 / 底 z=0 へ
    cw = comb.extents[1]                                        # 列の幅（=53.9）
    comb.apply_translation([0.0, (cy - cw) / 2.0, 0.0])         # 吸込口は x=0 のまま=板の端に端揃え

    # 板も笛も z=0 に置く。板厚=笛の床厚なので、笛の足元で厚く重なる＝union は安定（微小接触にならない）。
    plate = trimesh.creation.box(extents=[cx, cy, cz])
    plate.apply_translation([cx / 2.0, cy / 2.0, cz / 2.0])     # x:0..cx / y:0..cy / z:0..cz

    card_mesh = trimesh.boolean.union([plate, comb], engine="manifold")
    if corner_r and corner_r > 0:                               # 四隅を全高で落とす
        keep = _corner_prism(cx, cy, corner_r, corner_style, -1.0, comb.bounds[1][2] + 1.0)
        card_mesh = trimesh.boolean.intersection([card_mesh, keep], engine="manifold")
    card_mesh.apply_translation([0, 0, -card_mesh.bounds[0][2]])   # ベッド(z=0)へ

    info = dict(notes=notes, lengths=lengths, rows=infos,
                margin_x=round(cx - comb.extents[0], 1),
                margin_y=round((cy - cw) / 2.0, 2),
                card_z=cz, corner_r=corner_r, corner_style=corner_style,
                extents=tuple(np.round(card_mesh.extents, 2)),
                watertight=card_mesh.is_watertight)
    return card_mesh, info


# 名刺にできる音階。最長管が91mmに収まることが条件（余白＝91-最長管が名前を書ける帯になる）。
SCALES = {
    "--e":  (halfcut.E_MAJOR, "namecard_Emajor", "E major(E6→E7)"),
    "--a":  (halfcut.A_MAJOR, "namecard_Amajor", "A major(A6→A7)"),
    "--eb": (halfcut.EB_MAJOR, "namecard_Ebmajor", "Eb major(D#6→D#7)"),
    "--f":  (halfcut.F_MAJOR7, "namecard_Fmajor7", "F major 7音(F6→E7)"),
}


def main():
    os.makedirs(OUT, exist_ok=True)
    style = "chamfer" if "--chamfer" in sys.argv else "round"
    r = CORNER_R
    for a in sys.argv[1:]:
        if a.startswith("--r="):
            r = float(a[4:])
    notes, stem, label = SCALES["--e"]                       # 既定は E major
    for flag, v in SCALES.items():
        if flag in sys.argv:
            notes, stem, label = v
            break

    m, info = build(notes=notes, corner_r=r, corner_style=style)
    name = os.path.join(OUT, stem + ".stl")
    m.export(name)
    print("笛つき名刺（%s %d音・名刺 %gx%gx%gmm 板・笛と同じ z=0 に融合）:"
          % (label, len(notes), CARD_X, CARD_Y, info["card_z"]))
    for it in info["rows"]:
        print("    %-4s L=%4.1fmm  行y=%5.1f  予測 %5.0fHz" % (it["note"], it["L"], it["y"], it["freq"]))
    print("  余白: 管先端側 x=%.1fmm（名前を書ける帯）/ 幅方向 各 %.2fmm" % (info["margin_x"], info["margin_y"]))
    print("  四隅: %s %.1fmm（板ごと笛も全高で落とす）" % (info["corner_style"], info["corner_r"]))
    print("  外形=%s watertight=%s 体積=%.2fcm3 -> %s" %
          (info["extents"], info["watertight"], m.volume / 1000.0, name))


if __name__ == "__main__":
    main()
