"""Chordika の12枚＋表紙(実測厚み約51mm)を収める枡箱と、かぶせる枡状の蓋を生成する。

クレジットカード大(85.6×53.98mm)のカードを立てずに平積みで収納する。内部深さは51mmに
余裕を見て55mm。本体は上が開いた枡、蓋は本体外側にかぶせるスリップ嵌合の枡。長辺に指がかりの
半円スカラップを設けてカードを取り出しやすくする。すべてサポート不要で印刷できる形状。
"""
import os
import sys
import numpy as np
import trimesh
from shapely.affinity import translate as _translate2d
from shapely.affinity import rotate as _rotate2d_shapely

sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.pardir, "fue"))
import stencil  # 表紙と同じ Black Ops One ステンシル

OUT = os.path.join(os.path.dirname(__file__), os.pardir, "out")

# --- カードと収納 ---
CARD_LONG = 85.6      # クレジットカードの長辺
CARD_SHORT = 53.98    # 短辺
CLR = 1.5             # カードと内壁の隙間(各辺)
INNER_DEPTH = 55.0    # 内部の深さ(実測51mmに余裕)

# --- 本体(枡) ---
WALL = 1.2            # 側壁の厚み(0.4ノズル3周ぶん・印刷可能な範囲で薄く)
FLOOR = 1.2           # 床の厚み

# --- 蓋(かぶせる枡) ---
LID_GAP = 0.3         # 蓋内側と本体外側の隙間(各辺、スリップ嵌合)
LID_WALL = 1.2        # 蓋の側壁の厚み
LID_TOP = 1.2         # 蓋の天面の厚み
LID_OVERLAP = 40.0    # 蓋が本体にかぶさる深さ(本体上部から)

# --- 蓋のステンシル(表紙と同じ Chordika) ---
LID_TITLE = "Chordika"
LID_TITLE_MARGIN = 10.0   # 天面端からの余白(長辺方向)

# --- 指がかり ---
SCOOP_R = 16.0        # 半円スカラップの半径
SCOOP_DEPTH_FROM_TOP = 26.0  # 上縁からの深さ


def _rounded_box(w, l, h):
    """原点中心・底面z=0の直方体。"""
    b = trimesh.creation.box(extents=(w, l, h))
    b.apply_translation((0, 0, h / 2.0))
    return b


def build_base():
    inner_w = CARD_LONG + 2 * CLR      # 88.6
    inner_l = CARD_SHORT + 2 * CLR     # 56.98
    outer_w = inner_w + 2 * WALL       # 92.6
    outer_l = inner_l + 2 * WALL       # 60.98
    height = INNER_DEPTH + FLOOR       # 56.5

    outer = _rounded_box(outer_w, outer_l, height)
    # 内側の空洞: 床の上から上端まで、上は開放
    cavity = _rounded_box(inner_w, inner_l, INNER_DEPTH + 1.0)
    cavity.apply_translation((0, 0, FLOOR))  # 床の上に載せ、+1で上を突き抜けて開放
    box = trimesh.boolean.difference([outer, cavity])

    # 指がかり: 長辺(y=+側)の壁を半円柱でえぐる。上縁から SCOOP_DEPTH_FROM_TOP だけ。
    cyl = trimesh.creation.cylinder(radius=SCOOP_R, height=WALL * 4)
    # x軸まわりに寝かせて水平の半円にする(円柱軸をy方向へ)
    cyl.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, (1, 0, 0)))
    cyl.apply_translation((0, outer_l / 2.0, height))  # 円の中心を上縁の高さ・外壁上に
    box = trimesh.boolean.difference([box, cyl])

    box.merge_vertices()
    return box, (outer_w, outer_l, height)


def build_lid(base_outer_w, base_outer_l):
    inner_w = base_outer_w + 2 * LID_GAP   # 本体外側+隙間
    inner_l = base_outer_l + 2 * LID_GAP
    outer_w = inner_w + 2 * LID_WALL
    outer_l = inner_l + 2 * LID_WALL
    height = LID_OVERLAP + LID_TOP         # かぶさる深さ+天面

    outer = _rounded_box(outer_w, outer_l, height)
    cavity = _rounded_box(inner_w, inner_l, LID_OVERLAP + 1.0)
    # 下から開放にするため、床(z=0)を突き抜けさせて上は天面を残す
    cavity.apply_translation((0, 0, -1.0))
    lid = trimesh.boolean.difference([outer, cavity])

    # 天面に表紙と同じ Chordika ステンシルを貫通で入れる。時計回り90°回転で短辺(y)方向に読ませ、
    # 短辺に収まるよう自動縮小（width_max を短辺長にする）。
    poly, (tw, th) = stencil.text_holes(LID_TITLE, height=30.0,
                                        width_max=outer_l - 2 * LID_TITLE_MARGIN, bridge_w=1.4)
    poly = _rotate2d_shapely(poly, -90.0, origin=(0, 0))   # 時計回り90°
    minx, miny, maxx, maxy = poly.bounds
    poly = _translate2d(poly, xoff=-(minx + maxx) / 2.0, yoff=-(miny + maxy) / 2.0)  # 原点中心へ
    geoms = list(poly.geoms) if poly.geom_type == "MultiPolygon" else [poly]
    for g in geoms:  # 文字ごとに押し出して天面板を貫通で差し引く
        cut = trimesh.creation.extrude_polygon(g, height=LID_TOP + 2.0)
        cut.apply_translation((0, 0, height - LID_TOP - 1.0))
        lid = trimesh.boolean.difference([lid, cut])

    lid.merge_vertices()
    return lid, (outer_w, outer_l, height), (round(tw, 1), round(th, 1))


def main():
    base, bdim = build_base()
    base_path = os.path.join(OUT, "chordika_box_base.stl")
    base.export(base_path)
    print("base:", base_path, "外形 %.1f x %.1f x %.1f mm  watertight=%s" %
          (bdim[0], bdim[1], bdim[2], base.is_watertight))

    lid, ldim, tdim = build_lid(bdim[0], bdim[1])
    lid_path = os.path.join(OUT, "chordika_box_lid.stl")
    lid.export(lid_path)
    print("lid :", lid_path, "外形 %.1f x %.1f x %.1f mm  watertight=%s" %
          (ldim[0], ldim[1], ldim[2], lid.is_watertight))
    print("     ステンシル '%s' 幅 %.1f x 高さ %.1f mm（天面を貫通、板厚 %.1fmm）" %
          (LID_TITLE, tdim[0], tdim[1], LID_TOP))

    closed_h = bdim[2] + (ldim[2] - LID_OVERLAP)  # 本体高さ + 蓋のはみ出し(天面ぶん)
    print("収納カード面: %.1f x %.1f mm / 内部深さ %.1f mm" %
          (CARD_LONG + 2 * CLR, CARD_SHORT + 2 * CLR, INNER_DEPTH))
    print("蓋をかぶせた見かけ高さ 約 %.1f mm、本体の露出(つかむ縁) 約 %.1f mm" %
          (bdim[2] + LID_TOP, bdim[2] - LID_OVERLAP))


if __name__ == "__main__":
    main()
