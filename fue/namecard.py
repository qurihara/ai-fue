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
from shapely.geometry import box as sbox, MultiPolygon, Point as _Point
from shapely.affinity import rotate as _rotate2d, translate as _translate2d

sys.path.insert(0, os.path.dirname(__file__))
import halfcut
import chordflute
import stencil

OUT = os.path.join(os.path.dirname(__file__), os.pardir, "out")

CARD_X = 91.0        # 日本の一般的な名刺（横）
CARD_Y = 55.0
CARD_Z = 0.5         # = 半割り笛のボア床の厚さ(実測0.495mm)。板の上面がボアの床と一致し積み増しゼロになる
CORNER_R = 2.0       # 四隅の角取り量[mm]。E6/E7 の風道側壁を破らない安全上限が約2.0（上の説明参照）

# クレジットカードサイズ(ISO/IEC 7810 ID-1: 85.60×53.98mm)。笛(78.5×53.9)がほぼぴったり収まる:
# 幅方向は 53.9 vs 53.98 で片側わずか0.04mm、長手は 85.6-78.5=7.1mm の帯が余白＝ここに刻印する。
# 幅の余裕がほぼ無いので四隅の角取りは名刺より小さめ(既定1.2mm)にして両端E6/E7の口元を守る。
CREDIT_X = 85.60
CREDIT_Y = 53.98
CREDIT_CORNER_R = 1.2


def _corner_prism(cx, cy, r, style, z0, z1):
    """四隅を落とした板外形の角柱（全高を貫く切り抜き用）。style='round'=R面 / 'chamfer'=C面(45°)。"""
    join = 1 if style == "round" else 3          # shapely: 1=round, 3=bevel(=45°面取り)
    poly = sbox(r, r, cx - r, cy - r).buffer(r, join_style=join, resolution=32)
    prism = trimesh.creation.extrude_polygon(poly, height=z1 - z0)
    prism.apply_translation([0, 0, z0])
    return prism


def _label_poly(text, band_x0, band_x1, cy, cz, text_h=5.0,
                left_margin=3.5, bridge_w=1.1, rot180=True):
    """余白帯(band_x0..band_x1)に刻む刻印文字の 2D 配置ポリゴンと情報を返す（貫通/エンボスは呼び出し側）。
    文字はカード幅(y)方向に読む縦配置。帯の奥行き(band_x1-band_x0)に text_h が収まるよう自動縮小。
    rot180=True（既定）: 文字列を z軸180°回転。左寄せ: 文字ブロックの一端を y=left_margin に揃える（全カード統一）。"""
    band_depth = band_x1 - band_x0
    h = min(text_h, band_depth - 1.6)                           # 帯の前後に0.8mmずつ余白
    poly, (w, th) = stencil.text_holes(text, height=h,
                                       width_max=cy - 2 * left_margin, bridge_w=bridge_w)
    x0 = band_x0 + (band_depth - th) / 2.0                      # 帯の奥行き中央へ
    placed = stencil.place_along_y(poly, (w, th), x0=x0, y_center=cy / 2.0)
    if rot180:                                                  # 帯の中心を軸に180°回す（面内で反転）
        cxb = (band_x0 + band_x1) / 2.0
        placed = _rotate2d(placed, 180, origin=(cxb, cy / 2.0))
    dy = left_margin - placed.bounds[1]                        # 端(min y)を left_margin に揃える＝左寄せ
    placed = _translate2d(placed, yoff=dy)
    info = dict(text=text, text_h=round(h, 2), text_w=round(w, 1),
                band=(round(band_x0, 1), round(band_x1, 1)))
    return placed, info


def _text_line(text, x_center, text_h, cy, left_margin=3.5, bridge_w=1.1, rot180=True):
    """1行のテキストを、帯の奥行き方向で x_center に高さ text_h で置いた 2D ポリゴンを返す。
    幅(y)方向は左寄せ（y=left_margin から）。刻印帯に複数行（調性名＋ブランド）を積むのに使う。"""
    poly, (w, th) = stencil.text_holes(text, height=text_h, width_max=cy - 2 * left_margin, bridge_w=bridge_w)
    x0 = x_center - th / 2.0
    placed = stencil.place_along_y(poly, (w, th), x0=x0, y_center=cy / 2.0)
    if rot180:
        placed = _rotate2d(placed, 180, origin=(x_center, cy / 2.0))
    dy = left_margin - placed.bounds[1]
    placed = _translate2d(placed, yoff=dy)
    return placed, (w, th)


def _apply_2d(mesh, poly, cz, emboss=False, emboss_h=0.6):
    """2Dポリゴン poly を、emboss=False なら板を貫通する穴として差し引き、True なら板上面(z=cz)から
    emboss_h だけ盛り上げた浮き彫り(凸)として和算する。触知性のためのエンボスに使う。"""
    geoms = poly.geoms if isinstance(poly, MultiPolygon) else [poly]
    parts = []
    for g in geoms:
        if g.area <= 0:
            continue
        if emboss:
            pr = trimesh.creation.extrude_polygon(g, height=emboss_h)
            pr.apply_translation([0, 0, cz])                    # z: cz..cz+emboss_h（板上面に凸）
        else:
            pr = trimesh.creation.extrude_polygon(g, height=cz + 2.0)
            pr.apply_translation([0, 0, -1.0])                  # 板を確実に貫く
        parts.append(pr)
    if not parts:
        return mesh
    tool = trimesh.util.concatenate(parts)
    if emboss:
        return trimesh.boolean.union([mesh, tool], engine="manifold")
    return trimesh.boolean.difference([mesh, tool], engine="manifold")


def _star_cutter(cx0, cy0, r, cz):
    """(cx0,cy0) を中心にした ＊ の貫通穴メッシュ。板(z=0..cz)を確実に貫く。"""
    poly = stencil.asterisk(cx0, cy0, r)
    pr = trimesh.creation.extrude_polygon(poly, height=cz + 2.0)
    pr.apply_translation([0, 0, -1.0])
    return pr


def _strap_cutter(cx0, cy0, r, cz):
    """(cx0,cy0) を中心にした Ø2r のストラップ穴（円）の貫通穴メッシュ。板(z=0..cz)を貫く。"""
    circ = _Point(cx0, cy0).buffer(r, resolution=48)
    pr = trimesh.creation.extrude_polygon(circ, height=cz + 2.0)
    pr.apply_translation([0, 0, -1.0])
    return pr


def build(notes=None, card=(CARD_X, CARD_Y, CARD_Z),
          corner_r=CORNER_R, corner_style="round", label=None, band_x0=None,
          star_note=None, star_r=1.5, star_gap=2.0,
          strap=False, strap_d=6.0, strap_edge=3.0,
          strap_boss=False, boss_d=9.0,
          brim=False, brim_width=4.0, brim_height=0.25,
          emboss=False, emboss_h=0.6,
          brand=None, brand_h=2.2):
    """笛つき名刺/カードメッシュを作る。label を与えると余白帯にステンシル文字を貫通穴で刻む。
    band_x0 を与えると刻印帯の開始xを固定する（複数カードで刻印位置をカード端から揃えたいとき。
    None なら従来どおり「そのカードの最長管の先端＋1.5mm」＝カードごとに位置が動く）。
    star_note を与えると、その音の笛の先端(足)のすぐ先に ＊ を貫通穴で彫る（＝トーン/主音の目印）。
    ＊が刻印帯に食い込む場合は帯の開始を後退させる。戻り値 (mesh, info)。"""
    if notes is None:
        notes = halfcut.E_MAJOR
    cx, cy, cz = card
    comb, infos, notes, lengths = halfcut.scale_comb(notes=notes)
    b = comb.bounds
    comb.apply_translation([-b[0][0], -b[0][1], -b[0][2]])     # 吸込口 x=0 / 列 y=0 / 底 z=0 へ
    cw = comb.extents[1]                                        # 列の幅（=53.9）
    yshift = (cy - cw) / 2.0
    comb.apply_translation([0.0, yshift, 0.0])                  # 吸込口は x=0 のまま=板の端に端揃え
    flute_x_max = comb.bounds[1][0]                            # 最長管の先端x（この先が刻印できる余白帯）
    pitch = (infos[1]["y"] - infos[0]["y"]) if len(infos) > 1 else cw

    # 板も笛も z=0 に置く。板厚=笛の床厚なので、笛の足元で厚く重なる＝union は安定（微小接触にならない）。
    plate = trimesh.creation.box(extents=[cx, cy, cz])
    plate.apply_translation([cx / 2.0, cy / 2.0, cz / 2.0])     # x:0..cx / y:0..cy / z:0..cz

    card_mesh = trimesh.boolean.union([plate, comb], engine="manifold")
    if corner_r and corner_r > 0:                               # 四隅を全高で落とす
        keep = _corner_prism(cx, cy, corner_r, corner_style, -1.0, comb.bounds[1][2] + 1.0)
        card_mesh = trimesh.boolean.intersection([card_mesh, keep], engine="manifold")

    # ＊（主音の目印）を先に決める＝刻印帯が食い込まれないよう帯開始を後退させるため。
    star_info = None
    if star_note:
        row = next((it for it in infos if it["note"] == star_note), None)
        if row is not None:
            star_cx = row["x_foot"] + star_gap + star_r        # 足の先から star_gap だけ離す
            star_cy = row["y"] + yshift + pitch / 2.0          # その笛の列の中心y
            star_poly = stencil.asterisk(star_cx, star_cy, star_r)
            card_mesh = _apply_2d(card_mesh, star_poly, cz, emboss=emboss, emboss_h=emboss_h)
            star_info = dict(note=star_note, x=round(star_cx, 1), y=round(star_cy, 1), r=star_r)

    label_info = None
    if label:
        # 刻印帯は固定（band_x0）。左寄せラベルは幅方向の端から書き始めるので、中央にある ＊（主音の行）
        # とは干渉しない（短いラベルはその行まで届かない）。ゆえに帯を後退させる必要がない＝全カード統一。
        bx0 = flute_x_max + 1.5 if band_x0 is None else max(band_x0, flute_x_max + 1.0)
        band_x1 = cx - max(corner_r, 1.5) - 1.0               # 反対端の角取り/縁を避ける
        depth = band_x1 - bx0
        lines = []                                            # (text, x_center, height)
        if brand:
            # 帯の奥行きを2行に分ける：ブランド(小)を内側(低x)、調性名(大)を外側(高x)。両方印刷可サイズ。
            gap = 0.5
            kh = min(3.8, depth - brand_h - gap - 0.4)
            m = (depth - kh - brand_h - gap) / 2.0
            brand_c = bx0 + m + brand_h / 2.0
            key_c = bx0 + m + brand_h + gap + kh / 2.0
            lines = [(brand, brand_c, brand_h), (label, key_c, kh)]
            label_info = dict(text=label, brand=brand, key_h=round(kh, 1), brand_h=brand_h,
                              band=(round(bx0, 1), round(band_x1, 1)))
        else:
            h = min(5.0, depth - 1.6)
            lines = [(label, bx0 + depth / 2.0, h)]
            label_info = dict(text=label, text_h=round(h, 1), band=(round(bx0, 1), round(band_x1, 1)))
        for txt, xc, th_ in lines:
            pl, _ = _text_line(txt, xc, th_, cy)
            if pl is not None and not pl.is_empty:
                card_mesh = _apply_2d(card_mesh, pl, cz, emboss=emboss, emboss_h=emboss_h)

    # ストラップ穴：文字を寄せていない側の角（+x/+y 側＝far-x・high-y）に固定位置で開ける。
    # 端から strap_edge だけ内側（=穴の縁が端から strap_edge mm 入る）。全カード同じ座標。
    strap_info = None
    if strap:
        sr = strap_d / 2.0
        scx = cx - (sr + strap_edge)
        scy = cy - (sr + strap_edge)
        hole_h = cz                                    # 素の穴は板厚(0.5)を貫くだけ
        if strap_boss:                                 # 穴まわりを 4mm 厚(＝笛の高さ)に盛る補強ボス
            boss_top = float(comb.bounds[1][2])        # 笛の頂部z（≈4mm）
            boss = trimesh.creation.cylinder(radius=boss_d / 2.0, height=boss_top, sections=64)
            boss.apply_translation([scx, scy, boss_top / 2.0])   # z:0..boss_top
            card_mesh = trimesh.boolean.union([card_mesh, boss], engine="manifold")
            hole_h = boss_top                          # 穴はボスを丸ごと貫く
        # 穴（円）を hole_h + 余白 で確実に貫通
        circ = _Point(scx, scy).buffer(sr, resolution=48)
        pr = trimesh.creation.extrude_polygon(circ, height=hole_h + 2.0)
        pr.apply_translation([0, 0, -1.0])
        card_mesh = trimesh.boolean.difference([card_mesh, pr], engine="manifold")
        strap_info = dict(d=strap_d, x=round(scx, 1), y=round(scy, 1), edge=strap_edge,
                          boss=(boss_d if strap_boss else None))

    # 造形ブリム：カード周囲に brim_height(=0.25<カード0.5) の薄いフランジを造形。
    # カード床(0.5mm)より低いので接合部に段差ができ、そこを切って剥がしやすい（後で切り離しやすい）。
    # スライサのブリムは第1層だけで高さ制御できないため、幾何で作って高さを差別化する。
    brim_info = None
    if brim:
        r = corner_r if (corner_r and corner_r > 0) else 0.0
        outline = (sbox(r, r, cx - r, cy - r).buffer(r, join_style=1, resolution=32)
                   if r > 0 else sbox(0, 0, cx, cy))
        flange = outline.buffer(brim_width, join_style=1, resolution=32)   # 外周へ brim_width 張り出す
        fl = trimesh.creation.extrude_polygon(flange, height=brim_height)  # z:0..brim_height
        card_mesh = trimesh.boolean.union([card_mesh, fl], engine="manifold")
        brim_info = dict(width=brim_width, height=brim_height)

    card_mesh.apply_translation([0, 0, -card_mesh.bounds[0][2]])   # ベッド(z=0)へ

    info = dict(notes=notes, lengths=lengths, rows=infos,
                margin_x=round(cx - comb.extents[0], 1),
                margin_y=round((cy - cw) / 2.0, 2),
                card_z=cz, corner_r=corner_r, corner_style=corner_style,
                card_size=(cx, cy), label=label_info, star=star_info, strap=strap_info,
                brim=brim_info, emboss=(emboss_h if emboss else None),
                extents=tuple(np.round(card_mesh.extents, 2)),
                watertight=card_mesh.is_watertight)
    return card_mesh, info


def build_cover(title="Chordika", card=(CREDIT_X, CREDIT_Y, CARD_Z),
                corner_r=CREDIT_CORNER_R, corner_style="round",
                emboss=False, emboss_h=0.6, title_margin=4.0,
                strap=True, strap_d=6.0, strap_edge=3.0):
    """デッキの表紙カード：笛は無く、大きな title を中央に刻む＋ストラップ穴（デッキと同座標）。
    既定 emboss=False＝ステンシル（貫通穴）で、板厚は他のカードと同じ card[2]=CARD_Z(0.5mm)。
    emboss=True にすると凸（総厚 card[2]+emboss_h）。タイトルの向きは調性名と同じ（y方向読み・z軸180°）で中央配置。"""
    cx, cy, pz = card
    plate = trimesh.creation.box(extents=[cx, cy, pz])
    plate.apply_translation([cx / 2.0, cy / 2.0, pz / 2.0])
    mesh = plate
    if corner_r and corner_r > 0:
        keep = _corner_prism(cx, cy, corner_r, corner_style, -1.0, pz + (emboss_h if emboss else 0.0) + 1.0)
        mesh = trimesh.boolean.intersection([mesh, keep], engine="manifold")
    # タイトルを中央に（幅方向いっぱいまで自動縮小）・調性名と同じ向きで刻む（貫通 or 凸）
    poly, (w, th) = stencil.text_holes(title, height=40.0, width_max=cy - 2 * title_margin, bridge_w=1.4)
    placed = stencil.place_along_y(poly, (w, th), x0=cx / 2.0 - th / 2.0, y_center=cy / 2.0)
    placed = _rotate2d(placed, 180, origin=(cx / 2.0, cy / 2.0))
    mesh = _apply_2d(mesh, placed, pz, emboss=emboss, emboss_h=emboss_h)
    strap_info = None
    if strap:
        sr = strap_d / 2.0
        scx = cx - (sr + strap_edge)
        scy = cy - (sr + strap_edge)
        circ = _Point(scx, scy).buffer(sr, resolution=48)
        pr = trimesh.creation.extrude_polygon(circ, height=pz + 2.0)
        pr.apply_translation([0, 0, -1.0])
        mesh = trimesh.boolean.difference([mesh, pr], engine="manifold")
        strap_info = dict(d=strap_d, x=round(scx, 1), y=round(scy, 1))
    mesh.apply_translation([0, 0, -mesh.bounds[0][2]])
    info = dict(title=title, title_h=round(th, 1), title_w=round(w, 1), plate_z=pz,
                emboss=(emboss_h if emboss else None), strap=strap_info, card_size=(cx, cy),
                extents=tuple(np.round(mesh.extents, 2)), watertight=mesh.is_watertight)
    return mesh, info


# 名刺/カードにできる音階。(音名リスト, ファイル名幹, 説明, 調性ラベル)。
# 調性ラベルは刻印の既定文字＝そのカードの調性を表す（--label で上書き可）。
SCALES = {
    "--e":  (halfcut.E_MAJOR,  "namecard_Emajor",  "E major(E6→E7)",     "E major"),
    "--a":  (halfcut.A_MAJOR,  "namecard_Amajor",  "A major(A6→A7)",     "A major"),
    "--eb": (halfcut.EB_MAJOR, "namecard_Ebmajor", "Eb major(D#6→D#7)",  "Eb major"),
    "--f":  (halfcut.F_MAJOR7, "namecard_Fmajor7", "F major 7音(F6→E7)", "F major"),
}

# コード笛カード。(音名リスト, ファイル名幹, 説明, 調性ラベル)。調性ラベル＝主調（IV·I·V の I の調）。
CHORDS = {
    "--chord":      (chordflute.CHORD_CMAJOR, "card_chord7",     "コード笛 C major 7本(IV·I·V=F·C·G)",       "C major"),
    "--chord-to-g": (chordflute.CHORD8_TO_G,  "card_chord8_toG", "コード笛 C major 8本(+F#6→属調G・本命)",   "C major"),
    "--chord-to-am":(chordflute.CHORD8_TO_AM, "card_chord8_toAm","コード笛 C major 8本(+G#6→平行短調Am)",   "C major"),
}


def main():
    os.makedirs(OUT, exist_ok=True)
    style = "chamfer" if "--chamfer" in sys.argv else "round"
    credit = "--credit" in sys.argv                          # クレジットカードサイズ(85.6×53.98)
    label = None
    label_given = False
    for a in sys.argv[1:]:
        if a.startswith("--label="):
            label = a[len("--label="):]                      # 空文字なら刻印なし
            label_given = True
    notes, stem, desc, keylabel = SCALES["--e"]              # 既定は E major
    for flag, v in CHORDS.items():                           # コード笛カードを優先判定
        if flag in sys.argv:
            notes, stem, desc, keylabel = v
            break
    else:
        for flag, v in SCALES.items():
            if flag in sys.argv:
                notes, stem, desc, keylabel = v
                break
    if not label_given:
        label = keylabel                                     # 既定＝そのカードの調性ラベル

    if credit:
        cx, cy = CREDIT_X, CREDIT_Y
        r = CREDIT_CORNER_R
        stem = stem.replace("namecard_", "card_")
    else:
        cx, cy = CARD_X, CARD_Y
        r = CORNER_R
    for a in sys.argv[1:]:                                    # --r= で上書き可
        if a.startswith("--r="):
            r = float(a[4:])
    if label:
        safe = "".join(c if c.isalnum() else "_" for c in label).strip("_")
        stem += "_" + safe

    m, info = build(notes=notes, card=(cx, cy, CARD_Z), corner_r=r,
                    corner_style=style, label=label)
    name = os.path.join(OUT, stem + ".stl")
    m.export(name)
    kind = "クレジットカード" if credit else "名刺"
    print("笛つき%s（%s %d音・%gx%gx%gmm 板・笛と同じ z=0 に融合）:"
          % (kind, desc, len(notes), cx, cy, info["card_z"]))
    for it in info["rows"]:
        print("    %-4s L=%4.1fmm  行y=%5.1f  予測 %5.0fHz" % (it["note"], it["L"], it["y"], it["freq"]))
    print("  余白: 管先端側 x=%.1fmm / 幅方向 各 %.2fmm" % (info["margin_x"], info["margin_y"]))
    print("  四隅: %s %.1fmm（板ごと笛も全高で落とす）" % (info["corner_style"], info["corner_r"]))
    if info["label"]:
        li = info["label"]
        print("  刻印: '%s' 帯x=%s 文字高=%.1fmm 幅=%.1fmm（ステンシル穴・貫通）"
              % (li["text"], li["band"], li["text_h"], li["text_w"]))
    print("  外形=%s watertight=%s 体積=%.2fcm3 -> %s" %
          (info["extents"], info["watertight"], m.volume / 1000.0, name))


if __name__ == "__main__":
    main()
