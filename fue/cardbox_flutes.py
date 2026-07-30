"""Chordikaのカードを収める枡箱の床に、笛8本を仕込む（2-of-3の担体のひとつ）。

もとの箱は harmonica_deck/make_box.py で作った、カード12枚＋表紙を平積みで収める枡である。
その床を厚くして、笛を8本埋め込む。

置き方（[* 窓は真上（z+）に開く]）
  * 笛は床の中に寝かせ、[* 窓を箱の内側（上）へ]、[* 吸込口を箱の外側（短辺の外面）へ]向ける。
    壁の縁に垂直に並べる置き方は、実機で造形不良が多く復号できなかった（2026-07-30）。
    窓が真上に開く置き方だけを使う。
  * 吸込口は短辺の外面と面一にする。箱を持って外から吹ける。
  * 窓は箱の内側の底に開く。[* カードを入れたままでは吹けない]。中身をどけて初めて読める、
    という性質が物の形から出てくる（本立てで本をどけるのと同じ）。

床の厚み
  笛は高さ4mmなので、床を FLOOR_THICK（既定5mm）にする。もとの箱は床1.2mmだったので、
  内部の深さはそのぶん浅くなる。箱全体の高さを足して、収まる枚数は変えない。

使い方:
    python3 fue/cardbox_flutes.py --symbols 6,7,1,2,1 --index 1 \\
        --out out/cardbox_v1_share1.3mf
"""
from __future__ import annotations

import argparse
import json
import os
import sys

import numpy as np
import trimesh
from shapely.geometry import Point

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.pardir, "harmonica_deck"))
import cipher_codec as cd
import mini10
import orient_check
import stencil

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)
OUT = os.path.join(ROOT, "out")
CONFIG = os.path.join(ROOT, "docs", "cipher", "cipher_config.json")
SLOT12 = dict(lo_note="G#6", hi_note="G7")

# --- カードと箱（harmonica_deck/make_box.py と同じ寸法体系） ---
CARD_LONG = 85.6
CARD_SHORT = 53.98
CLR = 1.5              # カードと内壁の隙間
INNER_DEPTH = 55.0     # 内部の深さ（カードの実測51mmに余裕）
WALL = 1.2             # 側壁の厚み
SCOOP_R = 16.0         # 指がかりの半円の半径
SCOOP_FROM_TOP = 26.0

# --- 笛を仕込むための床 ---
FLOOR_THICK = 5.0      # 床の厚み（笛の高さ4mm＋下の余裕1mm）
FLOOR_UNDER = 1.0      # 笛の下に残す材料の厚み
OVER = 0.3             # 隣り合う笛の重なり（Chordikaのカードと同じ）
PROUD = 0.3            # 窓を床の面からどれだけ出すか
N_FLUTES = 8
FILL_FRONT = 2.0       # 吸込口の面を、この奥行きぶん埋める（v2）


def _box(w, l, h):
    b = trimesh.creation.box(extents=(w, l, h))
    b.apply_translation((w / 2.0, l / 2.0, h / 2.0))
    return b


def build_comb(notes, l_max):
    """8本の笛を0.3mmずつ重ねて融合した櫛を作る（native姿勢：窓が+z・床がz=0）。"""
    w = trimesh.load(mini10.BASE).extents[1]
    step = w - OVER
    flutes = []
    for i, note in enumerate(notes):
        f = mini10.uniform_flute(mini10.length_for_note(note), L_max=l_max)
        f.apply_translation([0, i * step, 0])
        flutes.append(f)
    comb = trimesh.boolean.union(flutes, engine="manifold")
    comb.merge_vertices()
    return comb, w + step * (len(notes) - 1)


def front_filler(comb, depth=FILL_FRONT):
    """吸込口の面の「吹き込み口以外の隙間」を埋める板を作る（v2）。

    笛は7mm幅の半割で、隣どうしは0.3mmしか重ねていないので、[* 笛と笛のあいだに谷が残る]。
    彫り抜きは笛の凸包で行うため、その谷はそのまま箱の前面に開口として現れる。実物では
    「吹き込み口が8つ」ではなく「大きな溝の中に8つの穴がある」ように見えてしまう。

    そこで、笛の口元の断面から[* ボア（吹き込み口）の穴だけを抜き出し]、それ以外を板で埋める。
    窓は吸込口から11.5mm奥から開くので、前面2mmを埋めても窓には触らない。
    """
    # 板は笛の外形より少し大きく取る。上側は彫り抜きの逃げ（窓の向きへ0.5mm広げた分）まで
    # 覆わないと、笛の上に 0.3mm の細い隙間が1本残る（実際に残った）。
    b = comb.bounds
    y0, y1 = b[0][1] - 0.2, b[1][1] + 0.2
    z0, z1 = b[0][2] - 0.2, b[1][2] + 0.7
    slab = trimesh.creation.box(extents=[depth + 0.2, y1 - y0, z1 - z0])
    slab.apply_translation([(depth + 0.2) / 2.0 - 0.1,
                            (y0 + y1) / 2.0, (z0 + z1) / 2.0])

    # 口元の断面を取り、内側の輪（＝ボア）の位置と大きさを読む
    sec = comb.section(plane_origin=[min(depth / 2.0, 1.0), 0, 0], plane_normal=[1, 0, 0])
    if sec is None:
        raise ValueError("笛の口元で断面が取れない")
    p2d, to3d = sec.to_planar()
    to3d = np.asarray(to3d)
    bores = []
    for poly in p2d.polygons_full:
        for ring in poly.interiors:
            uv = np.array(ring.coords)
            pts = np.column_stack([uv, np.zeros(len(uv)), np.ones(len(uv))]) @ to3d.T
            y0, y1 = pts[:, 1].min(), pts[:, 1].max()
            z0, z1 = pts[:, 2].min(), pts[:, 2].max()
            hole = trimesh.creation.box(extents=[depth + 1.0, y1 - y0, z1 - z0])
            hole.apply_translation([(depth + 1.0) / 2.0 - 0.5,
                                    (y0 + y1) / 2.0, (z0 + z1) / 2.0])
            bores.append(hole)
    if len(bores) != N_FLUTES:
        raise ValueError("吹き込み口が%d個しか見つからない（%d個のはず）" % (len(bores), N_FLUTES))
    for hole in bores:
        slab = trimesh.boolean.difference([slab, hole], engine="manifold")
    return slab, len(bores)


def build(notes, index=None, carve=True, fill_front=True):
    """笛を床に仕込んだ枡箱の本体を作る。戻り値 (scene, info)。"""
    l_max = mini10.uniform_body_length(
        [mini10.length_for_note(n) for n in mini10.CALIB12])
    comb, comb_w = build_comb(notes, l_max)

    inner_w = CARD_LONG + 2 * CLR                 # 88.6（笛の長さ方向）
    inner_l = max(CARD_SHORT + 2 * CLR, comb_w + 2.0)   # 56.98（笛の並ぶ方向）
    outer_w = inner_w + 2 * WALL
    outer_l = inner_l + 2 * WALL
    height = INNER_DEPTH + FLOOR_THICK
    if comb_w > inner_l:
        raise ValueError("笛%d本（幅%.1fmm）は内寸%.1fmmに並ばない"
                         % (len(notes), comb_w, inner_l))

    outer = _box(outer_w, outer_l, height)
    cavity = _box(inner_w, inner_l, INNER_DEPTH + 1.0)
    cavity.apply_translation((WALL, WALL, FLOOR_THICK))
    box = trimesh.boolean.difference([outer, cavity], engine="manifold")

    # 指がかり（長辺の外壁を半円柱でえぐる）
    cyl = trimesh.creation.cylinder(radius=SCOOP_R, height=WALL * 6)
    cyl.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, (1, 0, 0)))
    cyl.apply_translation((outer_w / 2.0, outer_l, height))
    box = trimesh.boolean.difference([box, cyl], engine="manifold")

    # 笛を床へ。吸込口(x=0)を短辺の外面(x=0)に合わせ、窓(+z)は箱の内側へ向く。
    # 床の上面は z=FLOOR_THICK。窓を PROUD だけ内側へ出す。
    comb.apply_translation([0.0,
                            (outer_l - comb_w) / 2.0,
                            FLOOR_THICK + PROUD - comb.extents[2]])
    placed = comb

    if carve:
        # 笛の外形（凸包）でポケットを彫ってから笛を戻す。彫る道具は、外へ抜ける2方向
        # （吸込口の向きと窓の向き）へ少し伸ばして、面が重なって彫り残るのを防ぐ。
        v = placed.vertices
        pts = np.vstack([v,
                         v - np.array([0.6, 0.0, 0.0]),      # 吸込口の側へ
                         v + np.array([0.0, 0.0, 0.5])])     # 窓の側へ
        tool = trimesh.Trimesh(vertices=pts).convex_hull
        box = trimesh.boolean.difference([box, tool], engine="manifold")

    n_bores = 0
    if fill_front:
        # 吸込口以外を埋める板を足す（v2）。笛の材料と重なるが、和なので問題ない。
        filler, n_bores = front_filler(placed)
        box = trimesh.boolean.union([box, filler], engine="manifold")

    if index:
        box = engrave_index(box, index, outer_w, outer_l, height)

    sc = trimesh.Scene()
    sc.add_geometry(box, geom_name="cardbox_0.28fast")
    sc.add_geometry(placed, geom_name="flutes_0.08careful")
    info = dict(outer=(outer_w, outer_l, height), inner_depth=height - FLOOR_THICK,
                comb_w=comb_w, notes=list(notes), n_bores=n_bores)
    return sc, info


def engrave_index(box, index, outer_w, outer_l, height, size=4.0, depth=0.8):
    """断片の番号を、吸込口が並ぶ短辺の外面に彫る（吹く側から見える位置）。"""
    poly, (w, th) = stencil.text_holes(str(index), height=size, bridge_w=0.9)
    from shapely.geometry import MultiPolygon
    geoms = list(poly.geoms) if isinstance(poly, MultiPolygon) else [poly]
    M = trimesh.transformations.rotation_matrix(np.pi / 2, (0, 1, 0))
    for g in geoms:
        if g.is_empty or g.area <= 0:
            continue
        t = trimesh.creation.extrude_polygon(g, height=depth + 0.5)
        t.apply_transform(M)
        b = t.bounds
        # 短辺の外面（x=0）に、上寄りの高さで置く
        t.apply_translation([depth - b[1][0],
                             (outer_l - (b[1][1] - b[0][1])) / 2.0 - b[0][1],
                             height - 8.0 - b[0][2]])
        box = trimesh.boolean.difference([box, t], engine="manifold")
    return box


def main(argv=None):
    ap = argparse.ArgumentParser(description="Chordikaの箱の床に笛を仕込む")
    ap.add_argument("--symbols", required=True, help="載せる記号列（例 6,7,1,2,1）")
    ap.add_argument("--parity", type=int, default=2, help="RSブロックあたりのパリティ記号数")
    ap.add_argument("--index", type=int, default=None, help="断片の番号（短辺の外面に彫る）")
    ap.add_argument("--no-carve", action="store_true")
    ap.add_argument("--no-fill-front", action="store_true",
                    help="吸込口の面を埋めない（v1の挙動）")
    ap.add_argument("--out", required=True, help="出力する3mf（版を含む名前にする）")
    args = ap.parse_args(argv)

    if os.path.exists(args.out):
        raise SystemExit("すでにある版を上書きしようとしている: %s" % args.out)

    with open(CONFIG, encoding="utf-8") as fp:
        base = json.load(fp)
    cfg = cd.CodecConfig(**{**base, **SLOT12, "ecc_parity": args.parity,
                            "mode": "symbols", "no_repeat": True})
    syms = [int(x) for x in args.symbols.replace(",", " ").split()]
    notes = list(cd.encode_symbols(syms, cfg).notes)
    if len(notes) != N_FLUTES:
        raise SystemExit("笛が%d本になった（%d本にしたい）。記号数かパリティを見直す"
                         % (len(notes), N_FLUTES))
    for i in range(len(notes) - 1):
        if notes[i] == notes[i + 1]:
            raise SystemExit("隣り合う笛が同じ音になっている")
    print("記号列 %s（%d個）→ 笛%d本: %s"
          % (",".join(map(str, syms)), len(syms), len(notes), " ".join(notes)))

    sc, info = build(notes, index=args.index, carve=not args.no_carve,
                     fill_front=not args.no_fill_front)

    res = orient_check.check_orientation(R=np.eye(3))
    print("向きの検査: 窓%+.0f度（真上）・長軸の傾き%.0f度 → %s"
          % (res.angle_deg, res.tilt_deg, res.verdict))
    if res.verdict != "ok":
        raise SystemExit("向きの検査に通らない")

    os.makedirs(OUT, exist_ok=True)
    sc.export(args.out)
    print("箱の外形 %.1f×%.1f×%.1fmm（内部の深さ %.1fmm・床 %.1fmm）"
          % (*info["outer"], info["inner_depth"], FLOOR_THICK))
    print("笛8本の幅 %.1fmm（内寸 %.1fmm に収まる）" % (info["comb_w"], info["outer"][1] - 2 * WALL))
    if info["n_bores"]:
        print("吸込口の面を前から%.1fmm埋め、吹き込み口%d個だけを残した" % (FILL_FRONT, info["n_bores"]))
    print("-> %s" % os.path.relpath(args.out, ROOT))
    if args.index:
        print("断片の番号 %d を、吸込口が並ぶ短辺の外面に彫った" % args.index)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
