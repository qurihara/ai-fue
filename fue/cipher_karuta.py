#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""絵入りの2-of-2カード。かるたの読み札のように和歌と歌人を刷り、裏に笛を並べる。

なにを作るか
------------
クレジットカード大の板を2枚。**表は百人一首の読み札**（和歌と歌人の絵を2色で刷る）、
**裏は笛8本**である。2枚そろえて吹くと秘密が戻る（2-of-2）。上の句の札と下の句の札に
分かれているので、2枚そろわないと歌も完成しない。**歌の完成と秘密の復元が一致する。**

層の作り（画像タイル fue/image_tiles.py と同じ）

    z = 0    〜 0.4mm   絵柄（濃い色）  … ベッド側。裏向きに刷る
    z = 0.4  〜 0.8mm   素地（白）
    z = 0.8  〜 4.8mm   笛8本（素地と同じ色）

ハート札（fue/cipher_cardpair.py）との違い
------------------------------------------
ハート札は2枚の境界にハートを抜き、形で「2枚そろって初めて開く」を語った。
こちらは**絵と歌で同じことを語る**。したがって

* 板が0.5mmから0.8mmへ厚くなる（絵柄の層が要るため）。総厚は4.8mm。
* ストラップの穴は残す。**★の刻印は要らない**（絵柄があるので向きは自明である）。
* ハートの切り欠きは無い。カードは2枚とも完全な長方形である。

★穴は outline から引いてから組み立てる★
----------------------------------------
plate.image_plate が返す板は押し出しを重ねただけで水密ではないので、あとから
ブーリアンで穴を開けられない。返ってきた `outline` と `ink_poly` から穴を引き、
素地と絵柄を組み直す。extrude_poly は穴が多い形でも通る。

使い方
------
    python3 fue/cipher_karuta.py --upper 上の句.png --lower 下の句.png \\
        --secret 123456 --stem out/karuta_izumi
"""
from __future__ import annotations

import argparse
import json
import os
import sys

import numpy as np
import trimesh
from shapely.geometry import Point

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE_PRINTING = ("/Users/kurihara/Library/CloudStorage/GoogleDrive-qurihara@gmail.com/"
                  "マイドライブ/share/google_desktop_share/3D_Print/image_printing")
sys.path.insert(0, IMAGE_PRINTING)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "harmonica_deck"))
import plate                       # noqa: E402  画像の板（image-card-print）
import img2card as I               # noqa: E402
import image_tiles as IT           # noqa: E402  extrude_poly を借りる
import cipher_codec                # noqa: E402
import mini10                      # noqa: E402

# ★cipher_cardpair は import しない★ あちらは刻印（stencil→matplotlib）を連れてくるが、
# この札には刻印が無く、image-card-print の仮想環境には matplotlib が入っていない。
# 使うのは寸法と秘密の分け方だけなので、下に写して依存を切る。
CX, CY = 85.6, 53.98               # クレジットカード
OVER = 0.3                         # 隣り合う笛の重なり[mm]
N_FLUTES = 8                       # 基準笛を含む本数
INK_T, BASE_T = 0.4, 0.4           # 絵柄と素地の厚み。画像タイルと同じ
CORNER_R = 2.0
STRAP_R = 2.5                      # ストラップ穴の半径[mm]
STRAP_MARGIN = 3.0                 # 穴の縁からカードの縁までの距離[mm]
SINK = 0.05                        # 笛を板へわずかに沈めて重ねる量[mm]


def split_secret(secret, base, n_symbols):
    """2-of-2 の分散。片方に乱数、もう片方に (秘密−乱数) を入れる。

    ★分ける先の空間は「記号の底の n_symbols 乗」に取る★ ここを取り違えると、断片が
    符号化できる範囲をはみ出し、笛の本数が合わなくなる。12スロットなら底は11なので、
    データ記号6個で 11^6 = 1,771,561 通りである。
    """
    span = base ** n_symbols
    rnd = (7 ** n_symbols) % span
    return rnd % span, (secret - rnd) % span


def codec_config(parity):
    """12スロット（G#6〜G7）・隣接同音禁止・基準笛C7。ハート札と同じ符号である。"""
    return cipher_codec.CodecConfig(
        lo_note="G#6", hi_note="G7", reference_note="C7",
        no_repeat=True, use_reference=True, ecc_parity=parity)


def encode_share(value, n_symbols, parity):
    """断片の値を、基準笛を先頭に置いた音名の並びへ符号化する。"""
    cfg = codec_config(parity)
    base = cipher_codec._wire_params(cfg)[1]
    symbols, v = [], value
    for _ in range(n_symbols):
        symbols.append(v % base)
        v //= base
    return list(cipher_codec.encode_symbols(symbols[::-1], cfg).notes)


# 穴を左に置くとき、笛を右へどれだけ逃がすか[mm]
# ★左上に穴を開けるなら、笛をずらさないと風道を壊す★ 笛の頭部（風道と窓）は
# 吸込口から約13mmある。板の左端に穴を開けると、いちばん端の笛のその部分に
# ちょうど当たり、息の通り道が抜けて鳴らなくなる。
STRAP_SHIFT = 8.0


def card_size(portrait):
    """札の外形。縦長なら長辺を高さに取る。"""
    return (CY, CX) if portrait else (CX, CY)


def strap_hole(where, size):
    """ストラップ穴の平面図形。★位置は「見たときの向き」で指定する★

    絵柄は face_down で刷るので、plate.image_plate が版下の左右を返してから板にする
    （裏返して見たときに元の絵のとおりに見せるため）。**穴だけ返さずに置くと、
    見たときの左上に開けたつもりが、絵柄と同じ側に来て文字と重なる。**
    2026-08-12、崇徳院札の「せ」が穴と一体化して発覚した。ここで同じ反転をかける。
    """
    r, m = STRAP_R, STRAP_MARGIN
    w, h = size
    pos = {"右下": (w - r - m, r + m), "右上": (w - r - m, h - r - m),
           "左下": (r + m, r + m), "左上": (r + m, h - r - m)}[where]
    x, y = pos
    return Point(w - x, y).buffer(r, resolution=48)      # 刷る向きへ返す


def flute_offset(where):
    """横長のとき、穴の位置に応じて笛の帯を右へ逃がす量[mm]。

    穴は刷る向きへ返されるので、「見たときの左」は板の上では右に来る。
    笛の吸込口は板の左端（x=0）にあるため、逃がすのは「見たときの右」のときである。
    """
    return STRAP_SHIFT if where.startswith("右") else 1.0


def flute_offset_portrait(where):
    """縦長のとき、笛を下からどれだけ上げるか[mm]。

    吸込口は下辺に置く。下側に穴があると風道に当たるので、そのときだけ逃がす。
    """
    return STRAP_SHIFT if where.endswith("下") else 1.0


def edge_ring(outline, width, hole):
    """外周から内へ width[mm] の帯（ふち取り）を作る。穴の分は抜く。

    ★ふちは絵柄の面にしか意味が無い★ 板の上（笛の側）は全部おなじ色で刷るので、
    ふちが色として見えるのは、白地と隣り合う絵柄の面だけである。
    """
    inner = outline.buffer(-width, join_style=2)
    return outline.difference(inner).difference(hole), inner


def image_plate_3color(image_path, hole, size, edge_w, face_t, **kw):
    """絵柄の面を3色（黒い字・白い地・緑のふち）にした板を作る。

    層の作り（z は絵柄の面を0とする。裏返して刷るので、この面がベッドに接する）

        z = 0      〜 face_t   黒い字 ／ 白い地 ／ 緑のふち   ← ここだけ3色
        z = face_t 〜 0.8mm    緑（板の残り）
        z = 0.8mm  〜          緑（笛8本）

    ★白い地の厚みが face_t である★ この上はすべて緑なので、薄いと緑が透ける。
    0.2mm（1層）だと緑がかって見え、0.4mm（2層）ならほぼ隠れる。フィラメントの
    交換の回数と引き換えになるので、呼ぶ側で決める。
    """
    p = plate.image_plate(image_path, size, corner_r=CORNER_R,
                          corner_style="round", fit="cover", face_down=True,
                          trim=False, ink_t=INK_T, base_t=BASE_T,
                          mode="threshold", threshold=kw.pop("threshold", 220), **kw)
    outline = p["outline"].difference(hole)
    ring, inner = edge_ring(p["outline"], edge_w, hole)

    # 字がふちに食い込んでいないかを見る。食い込むと、その字だけ緑で刷られる。
    ink_poly = p["ink_poly"].difference(hole)
    eaten = ink_poly.intersection(ring).area
    ink_poly = ink_poly.intersection(inner)
    white_poly = inner.difference(hole).difference(ink_poly)

    total = INK_T + BASE_T
    ink = IT.extrude_poly(ink_poly, 0.0, face_t)
    white = IT.extrude_poly(white_poly, 0.0, face_t)
    green = trimesh.util.concatenate([
        IT.extrude_poly(ring, 0.0, face_t),          # ふち（絵柄の面）
        IT.extrude_poly(outline, face_t, total - face_t),   # その上の板は全部これ
    ])
    for m in (ink, white, green):
        m.merge_vertices()
    q = dict(p)
    q.update(base=white, ink=ink, edge=green, outline=outline,
             ink_poly=ink_poly, white_poly=white_poly, ring=ring,
             top_z=total, edge_eaten_mm2=round(eaten, 2))
    q["info"] = {**p["info"], "edge_w": edge_w, "face_t": face_t,
                 "edge_eaten_mm2": round(eaten, 2),
                 "white_area_mm2": round(white_poly.area, 1),
                 "edge_area_mm2": round(ring.area, 1)}
    return q


def image_plate_with_hole(image_path, hole, size, **kw):
    """絵柄つきの板を作り、穴を開ける。

    ★plate.image_plate の返り値をそのまま彫ることはできない★
    押し出しを重ねただけのメッシュなので水密ではなく、manifold のブーリアンが
    「立体ではない」と拒む。平面図形の段階で穴を引き、そこから押し出し直す。
    """
    p = plate.image_plate(image_path, size, corner_r=CORNER_R,
                          corner_style="round", fit="cover", face_down=True,
                          trim=False, ink_t=INK_T, base_t=BASE_T,
                          mode="threshold", threshold=kw.pop("threshold", 220), **kw)
    outline = p["outline"].difference(hole)
    ink_poly = p["ink_poly"].difference(hole)
    rest = outline.difference(ink_poly)
    ink = IT.extrude_poly(ink_poly, 0.0, INK_T)
    base = trimesh.util.concatenate([
        IT.extrude_poly(rest, 0.0, INK_T),
        IT.extrude_poly(outline, INK_T, BASE_T),
    ])
    base.merge_vertices()
    q = dict(p)
    q.update(base=base, ink=ink, outline=outline, ink_poly=ink_poly,
             top_z=INK_T + BASE_T)
    return q


def export_3color(q, stem):
    """黒い字・白い地・緑のふちを別々のSTLで書き出し、3色のプレビューを描く。"""
    from PIL import Image, ImageDraw
    from shapely.geometry import MultiPolygon, Polygon

    paths = {"ink": stem + "_ink.stl", "base": stem + "_base.stl",
             "edge": stem + "_edge.stl"}
    q["ink"].export(paths["ink"])
    q["base"].export(paths["base"])
    q["edge"].export(paths["edge"])

    sx, sy = q["info"]["size"]
    scale = 8
    img = Image.new("RGB", (int(sx * scale), int(sy * scale)), (235, 235, 235))
    d = ImageDraw.Draw(img)

    def draw(poly, fill):
        geoms = poly.geoms if isinstance(poly, MultiPolygon) else [poly]
        for g in geoms:
            if not isinstance(g, Polygon):
                continue
            d.polygon([(x * scale, (sy - y) * scale) for x, y in g.exterior.coords], fill=fill)
            for ring in g.interiors:
                d.polygon([(x * scale, (sy - y) * scale) for x, y in ring.coords],
                          fill=(235, 235, 235))

    # ★描く順を間違えると白地が消える★ ふちは「外形から内側を引いた」形なので、
    # 内側が穴として入っている。穴は背景色で塗り戻すので、白地より後に描くと
    # 白地をまるごと塗りつぶしてしまう。ふちを先に描く。
    draw(q["ring"], (34, 139, 60))
    draw(q["white_poly"], (255, 255, 255))
    draw(q["ink_poly"], (25, 25, 25))
    paths["preview"] = stem + "_preview.png"
    img.save(paths["preview"])

    with open(stem + "_info.json", "w") as f:
        json.dump({**q["info"], "top_z": q["top_z"], "outputs": paths},
                  f, ensure_ascii=False, indent=2)
    return paths


def build_card(image_path, notes, l_max, stem, strap="右下", threshold=220,
               portrait=False, edge_w=0.0, face_t=INK_T):
    """絵入りカード1枚を作る。板を作り、その上面へ笛の帯を載せる。

    ★縦長では笛を90度回す★ 笛の長軸はいつも札の長辺に沿わせる（65.97mmは短辺53.98に
    収まらない）。縦長では吸込口を下辺（y=0）に置くので、笛の頭部（風道）は下に来る。
    したがって★上側に穴を開けるなら笛を逃がす必要がない★（足の先に当たるため）。
    """
    size = card_size(portrait)
    w, h = size
    hole = strap_hole(strap, size)
    if edge_w > 0:
        p = image_plate_3color(image_path, hole, size, edge_w, face_t, threshold=threshold)
    else:
        p = image_plate_with_hole(image_path, hole, size, threshold=threshold)
    comb = _comb(notes, l_max)
    if portrait:
        comb.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [0, 0, 1]))
        b = comb.bounds
        comb.apply_translation([-b[0][0] + (w - comb.extents[0]) / 2.0,
                                -b[0][1] + flute_offset_portrait(strap),
                                p["top_z"] - SINK - b[0][2]])
    else:
        comb.apply_translation([-comb.bounds[0][0] + flute_offset(strap),
                                (h - comb.extents[1]) / 2.0 - comb.bounds[0][1],
                                p["top_z"] - SINK - comb.bounds[0][2]])
    q = dict(p)
    q["flutes"] = comb
    if edge_w > 0:
        # ★笛は緑に足す★ 白い地は絵柄の面の1層ぶんだけで、その上は全部緑である。
        q["edge"] = trimesh.util.concatenate([p["edge"], comb])
        q["top_z"] = float(comb.bounds[1][2])
        export_3color(q, stem)
    else:
        q["base"] = trimesh.util.concatenate([p["base"], comb])
        q["top_z"] = float(comb.bounds[1][2])
        plate.export(q, stem)
    return q


def _comb(notes, l_max):
    """笛8本を0.3mm重ねて並べた帯。"""
    w = trimesh.load(mini10.BASE).extents[1]
    step = w - OVER
    parts = []
    for i, n in enumerate(notes):
        f = mini10.uniform_flute(mini10.length_for_note(n), L_max=l_max)
        f.apply_translation([0, i * step, 0])
        parts.append(f)
    comb = trimesh.boolean.union(parts, engine="manifold")
    comb.merge_vertices()
    return comb


def main(argv=None):
    ap = argparse.ArgumentParser(description="絵入りの2-of-2カード（かるたの読み札）")
    ap.add_argument("--upper", required=True, help="上の句の札に刷る画像")
    ap.add_argument("--lower", required=True, help="下の句の札に刷る画像")
    ap.add_argument("--secret", required=True, help="分ける秘密（整数）")
    ap.add_argument("--parity", type=int, default=1, help="パリティ記号の数")
    ap.add_argument("--stem", required=True, help="出力の名前の幹")
    ap.add_argument("--strap", default="左上", choices=["右下", "右上", "左下", "左上"],
                    help="ストラップ穴の位置。笛の頭部に当たる側なら自動で逃がす")
    ap.add_argument("--portrait", action="store_true", help="縦長の札にする")
    ap.add_argument("--threshold", type=int, default=220,
                    help="2値化のしきい値。これより暗い画素が絵柄になる")
    ap.add_argument("--edge", type=float, default=0.0,
                    help="ふち取りの幅[mm]。0なら付けない（2色のまま）")
    ap.add_argument("--face-t", type=float, default=INK_T,
                    help="絵柄の面の厚み[mm]。白い地の厚みでもある。"
                         "0.2なら層1つで交換1回、0.4なら層2つで交換3回")
    args = ap.parse_args(argv)

    secret = int(args.secret)
    # ★笛の本数の内訳★ 基準笛1 ＋ データ記号 ＋ パリティ記号 = N_FLUTES
    n_data = N_FLUTES - 1 - args.parity
    base = cipher_codec._wire_params(codec_config(args.parity))[1]
    share_a, share_b = split_secret(secret, base, n_data)
    l_max = mini10.uniform_body_length(
        [mini10.length_for_note(x) for x in mini10.CALIB12])

    print("笛%d本 = 基準1 + データ%d + パリティ%d。記号の底は%d（1枚あたり %d 通り）"
          % (N_FLUTES, n_data, args.parity, base, base ** n_data))
    print("秘密 %d を2つに分けた: %d と %d（足すと戻る）" % (secret, share_a, share_b))
    outs = []
    for share, image, tag in ((share_a, args.upper, "upper"),
                              (share_b, args.lower, "lower")):
        notes = encode_share(share, n_data, args.parity)
        stem = "%s_%s" % (args.stem, tag)
        q = build_card(image, notes, l_max, stem, strap=args.strap,
                       threshold=args.threshold, portrait=args.portrait,
                       edge_w=args.edge, face_t=args.face_t)
        print("  %-6s 断片 %-12d 笛 %s" % (tag, share, " ".join(notes)))
        if args.edge > 0:
            info = q["info"]
            print("         黒 %s_ink.stl ／ 白 %s_base.stl ／ 緑 %s_edge.stl"
                  % (stem, stem, stem))
            print("         ふち幅 %.1fmm・絵柄の面の厚み %.2fmm"
                  % (info["edge_w"], info["face_t"]))
            print("         面積 白 %.1f / 緑 %.1f / 黒 %.1f mm2"
                  % (info["white_area_mm2"], info["edge_area_mm2"], info["ink_area_mm2"]))
            if info["edge_eaten_mm2"] > 0.01:
                print("         ★字がふちに %.2f mm2 食い込んだので、その分は緑になる★"
                      % info["edge_eaten_mm2"])
        else:
            print("         %s_base.stl / %s_ink.stl（%.1f×%.1f×%.1fmm）"
                  % (stem, stem, *np.round(q["base"].extents, 1)))
        outs.append(q)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
