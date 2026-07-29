"""オクターブカード＝どれみふぁそらしどの8本を1枚のカードに載せた笛。

Chordikaが和音のカードなのに対し、これは[* 音階のカード]である。左端が最低音、右端が最高音で、
順に吹くと長音階が1オクターブ鳴る。カードの外形・厚み・作りはChordikaと共通なので、同じケースに
収まり、同じ持ち方で吹ける。

[音の選定]
 1オクターブは根音から数えて13半音ぶんの幅を要る（根音と、その1オクターブ上の音を両端に含むため）。
 mini10パイプの実績帯は F#6(1480Hz)〜G#7(3320Hz) の14半音なので、根音として置けるのは F#6・G6・G#6 の3つ。
 このうち [* 根音 G#6（＝A♭6）の A♭メジャー] を採る。理由は次の2つ。
  ・最長管が64.2mmで、Chordikaの最長管と同じ寸法になる。67mmのG6は実機で鳴らない個体が出たので避ける。
  ・8本のうち7本（64.2/58.5/53.5/51.2/47.0/43.2/39.9mm）が[* Chordikaで実績のある管長そのまま]。
    新規に確かめる必要があるのは最高音のG#7＝38.4mmだけで、危険が1点に絞られる。
 ドをCにした C7〜C8 は最高音が4186Hzで帯を大きく外れる。この音域では移調が避けられない。

[名前] Recoca（recorder＋card）。和音のChordikaに対して、音階のRecoca という対にする。

[作り]
 ・8本のmini10パイプを0.3mm重ねて融合し、名刺プレート(85.6×53.98)と厚み CZ=0.5mm で一体化する。
   ★CZ=0.5 は笛の床厚と一致させること。1.0にするとボアを侵食して鳴らなくなる。
 ・[* 左端が最低音]。y の大きい側に低音を置く（yの昇順では高音から低音へ並ぶ）。
 ・刻印は足側の余白帯にy方向読みで2行。外側にブランド名 Recoca を大きく、その内側に調名を小さく。
 ・管ごとの番号と触覚の切り欠きは設けない（Chordikaと違い、音階カードは1種類しかないため）。

実行: /Users/kurihara/Desktop/claude_work/mesh_venv/bin/python harmonica_deck/make_octave_card.py
"""
import os
import sys

import numpy as np
import trimesh
from shapely.geometry import MultiPolygon, Point, Polygon

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, os.pardir)
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "fue"))
import make_chordika_mini10 as CK
import namecard as NC
import stencil

CX, CY, CZ = CK.CX, CK.CY, CK.CZ
OVER = CK.OVER
MAJOR_SCALE = [0, 2, 4, 5, 7, 9, 11, 12]   # ど れ み ふぁ そ ら し ど
ROOT_MIDI = 92                              # G#6＝A♭6。上の docstring の理由で選定
BRAND = "Recoca"                            # recorder＋card。この音階カードの名前
KEY_LABEL = "Ab major"                      # 調名。G#ではなくA♭が正式な綴り（G#majorは重嬰記号を要する）


def _cut_plate(mesh, poly):
    """2Dポリゴンをプレート(z=0..CZ)だけ貫通で差し引く。上のパイプは触らない。"""
    geoms = list(poly.geoms) if isinstance(poly, MultiPolygon) else [poly]
    for g in geoms:
        pr = trimesh.creation.extrude_polygon(g, height=CZ + 0.4)
        pr.apply_translation([0, 0, -0.2])
        mesh = trimesh.boolean.difference([mesh, pr], engine="manifold")
    return mesh


def scale_midis(root_midi=ROOT_MIDI):
    return [root_midi + i for i in MAJOR_SCALE]


def build_card(root_midi=ROOT_MIDI, label=KEY_LABEL, brand=BRAND):
    """低音から高音へ並べた8本のオクターブカードを返す。"""
    CK.calib_from_file()
    midis = scale_midis(root_midi)

    W = trimesh.load(CK.BASE).extents[1]        # パイプ幅 ≈7
    step = W - OVER

    # ★並び: 左端が最低音になるよう、y の大きい側から低音を置く（yの昇順では高音→低音）
    ms, y, feet = [], 0.0, []
    for m in reversed(midis):
        L = CK._len_of(m)
        f = CK._flute(L)
        f.apply_translation([0, y, 0])
        ms.append(f)
        feet.append((y, L, m))
        y += step
    comb = trimesh.boolean.union(ms, engine="manifold")
    comb.merge_vertices()
    yshift = (CY - comb.extents[1]) / 2.0
    comb.apply_translation([0, yshift, 0])

    plate = trimesh.creation.box(extents=[CX, CY, CZ])
    plate.apply_translation([CX / 2, CY / 2, CZ / 2])
    card = trimesh.boolean.union([plate, comb], engine="manifold")
    keep = NC._corner_prism(CX, CY, 2.0, "round", -1.0, comb.bounds[1][2] + 1.0)
    card = trimesh.boolean.intersection([card, keep], engine="manifold")

    # 刻印（足側の余白帯にy方向読み・2行）。ブランド名を大きく、調名をその下に小さく。
    fx = max(f[1] for f in feet)
    bx0, bx1 = fx + 2.0, CX - 3.0
    depth = bx1 - bx0
    # ★読む向き: 文字はy方向に流れるので、カードを反時計回りに90度回すと読める。このとき +x が上になる。
    #   したがって[* 高x側が読み手から見て上]。ブランド名を高x（上）、調名を低x（下）に置く。
    bh, kh, gap = 5.5, 3.5, 1.2                  # ブランド高さ・調名高さ・行間
    mgn = (depth - bh - kh - gap) / 2.0
    lines = [(label, bx0 + mgn + kh / 2.0, kh),                    # 内側(低x)＝下＝調名
             (brand, bx0 + mgn + kh + gap + bh / 2.0, bh)]         # 外側(高x)＝上＝ブランド名
    for txt, xc, h in lines:
        pl, _ = NC._text_line(txt, xc, h, CY)
        if pl is not None and not pl.is_empty:
            card = _cut_plate(card, pl)

    # ストラップ穴（貫通）
    sr = 3.0
    circ = Point(CX - (sr + 3.0), CY - (sr + 3.0)).buffer(sr, resolution=48)
    pr = trimesh.creation.extrude_polygon(circ, height=comb.bounds[1][2] + 2.0)
    pr.apply_translation([0, 0, -1.0])
    card = trimesh.boolean.difference([card, pr], engine="manifold")

    card.apply_translation([0, 0, -card.bounds[0][2]])
    return card, feet, yshift


def report(midis):
    nm = lambda m: "%s%d" % (CK.NAMES[m % 12], m // 12 - 1)
    sol = ["ど", "れ", "み", "ふぁ", "そ", "ら", "し", "ど"]
    print("=== オクターブカード（%s メジャー・左が最低音）===" % CK.NAMES[ROOT_MIDI % 12])
    print("較正 A=%.1f e=%.4f" % (CK.A, CK.E))
    print(" 位置 階名   音     周波数Hz  管長mm")
    for i, m in enumerate(midis):
        print("  %d   %-4s  %-5s %8.1f  %6.1f" % (i + 1, sol[i], nm(m), CK._hz(m), CK._len_of(m)))


if __name__ == "__main__":
    CK.calib_from_file()
    midis = scale_midis()
    report(midis)
    card, feet, yshift = build_card()
    fn = os.path.join(OUT, "recoca_Ab_Gs6_Gs7.stl")
    card.export(fn)

    # 検証: 総厚・水密・ボア無傷（x=30断面のボア穴面積が素の笛=9.808と一致するか）
    s = card.section(plane_origin=[30, 0, 0], plane_normal=[1, 0, 0])
    p2, _ = s.to_planar()
    areas = sorted(set(round(abs(Polygon(r).area), 3) for p in p2.polygons_full for r in p.interiors))
    print("\n外形 %.1f×%.1f×%.1f mm  水密=%s" % (*card.extents, card.is_watertight))
    print("x=30断面のボア穴面積 %s （素の笛=9.808）" % areas)
    print("-> %s" % os.path.relpath(fn, ROOT))
