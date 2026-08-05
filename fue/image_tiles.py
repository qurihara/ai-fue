"""暗号笛内蔵画像タイル。1枚の画像をタイルに割り、その裏に笛を仕込む。

考え方
------
画像を2色の薄い板として刷り、それを格子に割って[* タイル]にする。タイルの上面（絵柄の
裏側）に統一管長笛を並べる。並べ直すと絵が戻り、裏返して吹くと秘密が戻る。

  z = 0    〜 0.4mm   絵柄（濃い色）  … ベッド側。裏向きに刷る
  z = 0.4  〜 0.8mm   素地（白）
  z = 0.8  〜 4.8mm   笛 y 本（素地と同じ色）

この作りには利点が3つある。

  1. [* 絵を飾るときは笛が下、笛を吹くときは絵が下]になる。見た目と機能が排他なので、
     絵として置いてあるかぎり秘密は目に触れない。
  2. [* カードと同じ造形条件]になる。薄い板（0.8mm）の上に笛が露出するので、本立てで
     問題になった「厚い板の中に笛が埋まり、周りがすかすかになる」状態が起きない。
  3. [* タイルを全部そろえないと絵が完成しない]。物としての「そろえる意味」と、秘密分散の
     「そろえる意味」が一致する。

寸法は笛が決める
----------------
統一管長笛は 65.97 × 7 × 4mm で、隣どうしは0.3mm重ねて並べる。したがって

  笛8本 … 帯 53.9mm → タイル 68.0 × 57.9mm
  笛9本 … 帯 60.6mm → タイル 68.0 × 64.6mm（ほぼ正方形）

長辺68mmは笛の長さで決まる（吸込口をタイルの縁と面一にし、足側に2mmの余白を取る）。

秘密の載せ方は2通り
-------------------
  --mode single … 全タイルの笛を通しで1つの符号語にする。3列3行・笛9本なら81本で、
                  基準笛を除く80本に約277ビット。1枚でも欠けると復元できない。
  --mode shares … タイルごとに独立した断片を持たせ、k-of-n のしきい値秘密分散を重ねる。
                  1枚あたり基準笛1本＋データで、パリティ2なら記号6個（11進6桁）。
                  1枚失っても開き、k-1枚まで盗まれても漏れない。

使い方:
    python3 fue/image_tiles.py 絵.png --out-dir out/tiles_demo
    python3 fue/image_tiles.py 絵.png --grid 3x4 --flutes 9 --mode shares -k 4
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
import tempfile

import numpy as np
import trimesh

IMAGE_PRINTING = ("/Users/kurihara/Library/CloudStorage/GoogleDrive-qurihara@gmail.com/"
                  "マイドライブ/share/google_desktop_share/3D_Print/image_printing")
sys.path.insert(0, IMAGE_PRINTING)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import plate                      # noqa: E402  画像の板を作る部品（image-card-print）
import img2card as I               # noqa: E402  plate.py が内部で使う押し出しの道具
import frame_pattern as FP         # noqa: E402
import cipher_codec as cd         # noqa: E402
import mini10                     # noqa: E402
import orient_check               # noqa: E402
import threshold as th            # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)
CONFIG = os.path.join(ROOT, "docs", "cipher", "cipher_config.json")
SLOT12 = dict(lo_note="G#6", hi_note="G7")

FLUTE_W = 7.0        # 笛の幅
OVER = 0.3           # 隣どうしの重なり
MARGIN_LONG = 2.0    # 笛の足の先に残す余白（長辺）
MARGIN_SIDE = 2.0    # 笛の帯の両側に残す余白（短辺）
CORNER_R = 0.5       # タイルの角を落とす量


def tile_size(n_flutes, l_max):
    """笛の本数からタイルの寸法（幅＝笛の長さ方向、高さ＝笛が並ぶ方向）を決める。"""
    comb = FLUTE_W + (FLUTE_W - OVER) * (n_flutes - 1)
    return (l_max + MARGIN_LONG, comb + 2 * MARGIN_SIDE), comb


def choose_grid(image_path, n_flutes, l_max, want=None):
    """グリッドを決める。--grid を指定すればそれ、無ければ画像の縦横比に一番近いものを選ぶ。"""
    (tw, th), _ = tile_size(n_flutes, l_max)
    if want:
        gx, gy = (int(v) for v in want.lower().split("x"))
        return gx, gy
    from PIL import Image
    with Image.open(image_path) as im:
        r = im.width / im.height
    best = None
    for gx in range(2, 6):
        for gy in range(2, 6):
            ratio = (tw * gx) / (th * gy)
            d = abs(math.log(ratio / r))
            if best is None or d < best[0]:
                best = (d, gx, gy)
    return best[1], best[2]


def split_image(image_path, gx, gy, out_dir, tile=None):
    """画像を gx × gy に割り、タイルごとのPNGを書き出す。左上から右へ、行を下へ進む。

    [* 先に絵全体を切り出してから割る]。順序を逆にして、割ってからタイルごとに
    切り出すと、タイルごとに独立して左右（または上下）が落ちるので、
    並べても絵がつながらない（2026-07-31に気づいた）。
    """
    from PIL import Image
    paths = []
    with Image.open(image_path) as im:
        im = im.convert("RGB")
        if tile is not None:
            target = (tile[0] * gx) / (tile[1] * gy)
            r = im.width / im.height
            if r > target:                       # 横長すぎるので左右を落とす
                w2 = int(round(im.height * target))
                x0 = (im.width - w2) // 2
                im = im.crop((x0, 0, x0 + w2, im.height))
            elif r < target:                     # 縦長すぎるので上下を落とす
                h2 = int(round(im.width / target))
                y0 = (im.height - h2) // 2
                im = im.crop((0, y0, im.width, y0 + h2))
            print("絵全体を先に切り出した（%.3f → %.3f）。割ってから切ると絵がつながらない"
                  % (r, target))
        w, h = im.size
        for row in range(gy):
            for col in range(gx):
                box = (round(w * col / gx), round(h * row / gy),
                       round(w * (col + 1) / gx), round(h * (row + 1) / gy))
                p = os.path.join(out_dir, "part_r%dc%d.png" % (row, col))
                im.crop(box).save(p)
                paths.append((row, col, p))
    return paths


def comb_of(notes, l_max):
    """笛を1本ずつ作って帯にする。吸込口は x=0、窓は +z を向く。"""
    step = FLUTE_W - OVER
    flutes, y = [], 0.0
    for note in notes:
        f = mini10.uniform_flute(mini10.length_for_note(note), L_max=l_max)
        f.apply_translation([0.0, y, 0.0])
        flutes.append(f)
        y += step
    comb = trimesh.boolean.union(flutes, engine="manifold")
    comb.merge_vertices()
    return comb


SINK = 0.02          # 笛を板へどれだけ沈めるか[mm]


def extrude_poly(poly, z0, h):
    """平面図形を押し出す。穴が多くても通る。

    img2card.extrude は穴をブーリアンで開けるので、枠模様を足したあとの素地のように
    [* 穴が数百個ある形]では「立体ではない」と拒まれる。trimesh の押し出しは
    三角形分割で穴を扱うので、この形でも通る（2026-07-31に差し替えた）。
    """
    geoms = list(poly.geoms) if hasattr(poly, "geoms") else [poly]
    parts = []
    for g in geoms:
        if g.is_empty or not hasattr(g, "exterior"):
            continue
        m = trimesh.creation.extrude_polygon(g, height=h)
        m.apply_translation([0.0, 0.0, z0])
        parts.append(m)
    if not parts:
        return trimesh.Trimesh()
    out = trimesh.util.concatenate(parts)
    out.merge_vertices()
    return out


def blank_plate(size, ink_t=0.4, base_t=0.4):
    """絵柄がひとつも無い板。真っ白なタイルのために用意する。"""
    from shapely.geometry import Polygon
    outline = I.card_polygon(size[0], size[1], CORNER_R, "chamfer")
    base = trimesh.util.concatenate([
        extrude_poly(outline, 0.0, ink_t),
        extrude_poly(outline, ink_t, base_t),
    ])
    return dict(base=base, ink=trimesh.Trimesh(), outline=outline,
                ink_poly=Polygon(), top_z=ink_t + base_t,
                info=dict(size=size, ink_t=ink_t, base_t=base_t, blank=True))


def global_threshold(image_path):
    """画像[* 全体]で大津の方法のしきい値を決める。

    タイルごとに決めてはいけない。タイルごとに明るさの分布が違うので、切る位置が
    ばらばらになり、[* 並べたときに絵がつながらない]（2026-07-31に実際にそうなった）。
    """
    from PIL import Image
    import numpy as _np
    with Image.open(image_path) as im:
        a = _np.asarray(im.convert("L"), dtype=_np.uint8)
    hist = _np.bincount(a.ravel(), minlength=256).astype(float)
    total = hist.sum()
    w0 = _np.cumsum(hist)
    w1 = total - w0
    mean = _np.cumsum(hist * _np.arange(256))
    m0 = _np.divide(mean, w0, out=_np.zeros(256), where=w0 > 0)
    m1 = _np.divide(mean[-1] - mean, w1, out=_np.zeros(256), where=w1 > 0)
    var = w0 * w1 * (m0 - m1) ** 2
    return int(_np.argmax(var))


def frame_for_tile(frame_poly, row, col, gx, gy, tw, th):
    """絵全体の座標で作った枠模様から、このタイルの持ち分を切り出す。

    [* 画像の行は上から数え、板の座標は下から数える]ので、y をひっくり返して対応させる。
    模様は絵全体で一度に作ってあるから、切り出すだけで隣どうしのつなぎ目が合う。
    """
    from shapely.affinity import translate
    from shapely.geometry import box as sbox
    x0 = col * tw
    y0 = (gy - 1 - row) * th
    part = frame_poly.intersection(sbox(x0, y0, x0 + tw, y0 + th))
    return translate(part, -x0, -y0)


def add_frame(p, frame_part):
    """板の絵柄へ枠模様を足し、素地を作り直す（face_down の並びに合わせる）。"""
    if frame_part is None or frame_part.is_empty:
        return p
    ink_poly = p["ink_poly"].union(frame_part).intersection(p["outline"])
    rest = p["outline"].difference(ink_poly)
    ink_t, base_t = p["info"]["ink_t"], p["info"]["base_t"]
    q = dict(p)
    q["ink_poly"] = ink_poly
    q["ink"] = extrude_poly(ink_poly, 0.0, ink_t)
    q["base"] = trimesh.util.concatenate([
        extrude_poly(rest, 0.0, ink_t),
        extrude_poly(p["outline"], ink_t, base_t),
    ])
    return q


def build_tile(image_path, notes, size, l_max, stem, binarize="threshold", threshold=None,
               frame_part=None):
    """タイル1枚を作る。板を作り、その上面へ笛の帯を載せる。

    [* ブーリアンで融合しない]。plate.image_plate が返す素地は押し出しを重ねただけの
    メッシュで水密ではないため、manifold のブーリアンが「立体ではない」と拒む。
    笛は板の上に載るだけなので、[* わずかに沈めて重ねれば十分]である。重なった閉じた
    立体は、スライサが和として正しく解釈する（2026-07-31にここで詰まった）。
    """
    try:
        p = plate.image_plate(image_path, size, corner_r=CORNER_R, corner_style="chamfer",
                              fit="cover", face_down=True, trim=False,
                              mode=binarize, threshold=threshold)
    except SystemExit:
        # 絵柄がひとつも無いタイル（絵の真っ白な場所に当たった）。
        # image_plate は「黒い画素がひとつもない」と止まるが、[* 枠模様だけのタイルは
        # 作れなければ困る]ので、絵柄が空の板を自分で組み立てる。
        p = blank_plate(size)
    p = add_frame(p, frame_part)
    comb = comb_of(notes, l_max)
    # 吸込口（x=0）をタイルの縁と面一にし、帯を短辺の中央へ寄せ、上面へ載せる。
    comb.apply_translation([-comb.bounds[0][0],
                            (size[1] - comb.extents[1]) / 2.0 - comb.bounds[0][1],
                            p["top_z"] - SINK - comb.bounds[0][2]])
    q = dict(p)
    q["base"] = trimesh.util.concatenate([p["base"], comb])
    q["top_z"] = float(comb.bounds[1][2])
    q["flutes"] = comb
    plate.export(q, stem)
    return q


def notes_for_single(payload, parity, total_flutes):
    """全タイルの笛を通しで1つの符号語にする。"""
    with open(CONFIG, encoding="utf-8") as fp:
        base = json.load(fp)
    cfg = cd.CodecConfig(**{**base, **SLOT12, "ecc_parity": parity,
                            "mode": "sequential", "no_repeat": True})
    notes = list(cd.encode(payload, cfg).notes)
    if len(notes) > total_flutes:
        raise SystemExit("秘密が大きすぎる。笛が%d本要るが、タイル全体で%d本しかない"
                         % (len(notes), total_flutes))
    return notes, cfg


def notes_for_shares(secret, parity, n_tiles, k, per_tile, seed):
    """タイルごとに独立した断片を作り、k-of-n のしきい値秘密分散を重ねる。"""
    import random
    with open(CONFIG, encoding="utf-8") as fp:
        base = json.load(fp)
    cfg = cd.CodecConfig(**{**base, **SLOT12, "ecc_parity": parity,
                            "mode": "symbols", "no_repeat": True})
    # 1枚に入る記号の数を、実際に符号化して確かめる（基準笛とパリティを含めて per_tile 本）
    width = 1
    while True:
        probe = [0] * (width + 1)
        if len(cd.encode_symbols(probe, cfg).notes) > per_tile:
            break
        width += 1
    if width < 1:
        raise SystemExit("タイル1枚に記号が1つも入らない")
    top = 11 ** width
    if secret >= top:
        raise SystemExit("秘密 %d は大きすぎる。この構成の上限は %d である" % (secret, top - 1))
    syms = th.symbols_of(secret, width)
    shares = th.split(syms, k, n_tiles, rng=random.Random(seed))
    out = []
    for idx, sh in shares:
        notes = list(cd.encode_symbols(list(sh), cfg).notes)
        if len(notes) != per_tile:
            raise SystemExit("断片%dの笛が%d本になった（%d本にそろえたい）"
                             % (idx, len(notes), per_tile))
        out.append((idx, list(sh), notes))
    return out, cfg, width


def main(argv=None):
    ap = argparse.ArgumentParser(description="画像をタイルに割り、その裏に笛を仕込む")
    ap.add_argument("image", help="入力画像")
    ap.add_argument("--out-dir", required=True, help="出力先のフォルダ")
    ap.add_argument("--grid", default=None,
                    help="格子の列数x行数（例 3x3）。省くと画像の縦横比から選ぶ。既定は3x3")
    ap.add_argument("--auto-grid", action="store_true",
                    help="画像の縦横比に一番近い格子を選ぶ")
    ap.add_argument("--flutes", type=int, default=9, help="タイル1枚あたりの笛の本数")
    ap.add_argument("--mode", choices=["single", "shares"], default="shares",
                    help="single＝全部を1つの符号語、shares＝タイルごとの秘密分散")
    ap.add_argument("--parity", type=int, default=2, help="RSブロックあたりのパリティ記号数")
    ap.add_argument("--payload", default="CipherFlute-tiles", help="single のときの秘密")
    ap.add_argument("--secret", type=int, default=124816, help="shares のときの秘密（整数）")
    ap.add_argument("-k", type=int, default=None, help="shares のとき、何枚そろえば開くか")
    ap.add_argument("--seed", type=int, default=20260731, help="分散の乱数の種")
    ap.add_argument("--no-build", action="store_true", help="寸法と符号の計画だけを出す")
    ap.add_argument("--frame", default=None,
                    help="外周に置く枠模様（seigaiha・ichimatsu・sayagata）。"
                         "タイルが真っ白になっても位置が分かるようにする")
    ap.add_argument("--frame-band", type=float, default=8.0, help="枠の帯の幅[mm]")
    ap.add_argument("--binarize", choices=["threshold", "white"], default="threshold",
                    help="2値化の方法。写真や線画は threshold、カラーの版下は white")
    ap.add_argument("--threshold", type=int, default=None,
                    help="明るさのしきい値。省くと画像全体から大津の方法で決める")
    ap.add_argument("--only", type=int, default=None,
                    help="最初のN枚だけ作る（形を確かめるとき用）")
    args = ap.parse_args(argv)

    l_max = mini10.uniform_body_length(
        [mini10.length_for_note(n) for n in mini10.CALIB12])
    size, comb_w = tile_size(args.flutes, l_max)
    if args.auto_grid:
        gx, gy = choose_grid(args.image, args.flutes, l_max)
    else:
        gx, gy = choose_grid(args.image, args.flutes, l_max, args.grid or "3x3")
    n_tiles = gx * gy
    total = n_tiles * args.flutes

    print("タイル %.1f × %.1f mm（笛%d本・帯%.1fmm）" % (size[0], size[1], args.flutes, comb_w))
    print("格子 %d列 × %d行 = %d枚 → 絵の大きさ %.0f × %.0f mm"
          % (gx, gy, n_tiles, size[0] * gx, size[1] * gy))
    print("笛は合計 %d本" % total)

    if args.mode == "single":
        notes, cfg = notes_for_single(args.payload.encode(), args.parity, total)
        print("符号化: 通しで1つの符号語。秘密 %r（%dbit）→ 笛%d本"
              % (args.payload, len(args.payload) * 8, len(notes)))
        per = -(-len(notes) // n_tiles)
        plan = [(i + 1, None, notes[i * per:(i + 1) * per]) for i in range(n_tiles)]
        plan = [(i, s, ns) for i, s, ns in plan if ns]
    else:
        k = args.k or max(2, n_tiles // 2)
        plan, cfg, width = notes_for_shares(args.secret, args.parity, n_tiles, k,
                                            args.flutes, args.seed)
        print("符号化: タイルごとの断片。%d枚のうち[* %d枚]そろえば開く。"
              "秘密 %d（11進%d桁・上限%d）" % (n_tiles, k, args.secret, width, 11 ** width - 1))

    for idx, syms, ns in plan:
        for i in range(len(ns) - 1):
            assert ns[i] != ns[i + 1], "隣り合う笛が同じ音になっている（タイル%d）" % idx
        res = orient_check.check_orientation(R=np.eye(3))
        if res.verdict != "ok":
            raise SystemExit("向きの検査に通らない: %s" % res.message)
        print("  タイル%2d … 笛%d本 %s%s"
              % (idx, len(ns), " ".join(ns),
                 ("  記号 " + ",".join(map(str, syms))) if syms else ""))

    if args.no_build:
        return 0

    os.makedirs(args.out_dir, exist_ok=True)
    thr = args.threshold
    if args.binarize == "threshold" and thr is None:
        thr = global_threshold(args.image)
        print("2値化: 画像全体の大津の方法で しきい値 %d（全タイル共通）" % thr)
    elif args.binarize == "threshold":
        print("2値化: しきい値 %d（手で指定・全タイル共通）" % thr)
    else:
        print("2値化: 白かそれ以外かで分ける")
    frame_poly = None
    if args.frame:
        frame_poly = FP.frame_polygon(args.frame, size[0] * gx, size[1] * gy,
                                      t=args.frame_band)
        print("枠模様: %s（帯 %.1fmm・面積 %.0f mm2）。絵全体の座標で作ってから割るので、"
              "タイルのつなぎ目で必ずつながる" % (args.frame, args.frame_band, frame_poly.area))
    parts = split_image(args.image, gx, gy, args.out_dir, tile=size)
    pairs = list(zip(parts, plan))
    if args.only:
        pairs = pairs[:args.only]
        print("（形を確かめるため、最初の%d枚だけ作る）" % args.only)
    for (row, col, img), (idx, syms, ns) in pairs:
        stem = os.path.join(args.out_dir, "tile_%02d_r%dc%d" % (idx, row, col))
        fp = (frame_for_tile(frame_poly, row, col, gx, gy, size[0], size[1])
              if frame_poly is not None else None)
        build_tile(img, ns, size, l_max, stem, binarize=args.binarize, threshold=thr,
                   frame_part=fp)
        print("  書き出した %s（笛%d本）" % (os.path.relpath(stem, ROOT), len(ns)))
    print("2色の3mfに組み立てるには image-card-print の make_card_3mf.py を使う")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
