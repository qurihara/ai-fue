"""暗号笛内蔵画像タイルを収める額縁の箱。

置き方
------
タイルは[* 笛を下に向けて伏せる]。箱に入れた状態では絵が上を向き、笛は見えない。
取り出して裏返すと笛が現れる。見た目と機能が排他になるという、タイルそのものの
性質を、箱がそのまま受け継ぐ。

枠線を合わせる仕組み
--------------------
模様は[* 箱の座標系で一度に作り]、内側（タイルの持ち分）と外側（箱の壁の上面）へ
切り分ける。同じ座標系から切り出すので、タイルを箱へ入れると模様が途切れずに続く。
箱は1色なので、壁の模様は彫り込みで表す。

使い方:
    python3 fue/frame_box.py --tiles 3x3 --frame seigaiha -o out/hokusai_box.stl
"""
from __future__ import annotations

import argparse
import os
import sys

import numpy as np
import trimesh
from shapely.affinity import translate
from shapely.geometry import box as sbox

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
IMAGE_PRINTING = ("/Users/kurihara/Library/CloudStorage/GoogleDrive-qurihara@gmail.com/"
                  "マイドライブ/share/google_desktop_share/3D_Print/image_printing")
sys.path.insert(0, IMAGE_PRINTING)

import frame_pattern as FP        # noqa: E402
import img2card as I              # noqa: E402
import mini10                     # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)

WALL = 5.0        # 壁の厚さ
FLOOR = 1.6       # 底の厚さ
PLAY = 0.6        # タイルと内側のあいだの遊び（全体で）
ENGRAVE = 0.6     # 壁の上面に模様を彫る深さ
CORNER = 2.0      # 箱の外側の角を丸める量


def tile_extent(n_flutes):
    """タイル1枚の寸法（fue/image_tiles.py と同じ決め方）。"""
    l_max = mini10.uniform_body_length(
        [mini10.length_for_note(n) for n in mini10.CALIB12])
    comb = 7.0 + 6.7 * (n_flutes - 1)
    return (l_max + 2.0, comb + 4.0)


def framed_pair(name, art_w, art_h, band, wall):
    """模様を箱の座標系で一度に作り、(タイルの持ち分, 箱の壁の持ち分) に切り分ける。

    返り値の座標系は[* 絵の左下が原点]である。箱の壁は負の側（−wall）まで伸びる。
    """
    big = FP.frame_polygon(name, art_w + 2 * wall, art_h + 2 * wall, t=wall + band)
    big = translate(big, -wall, -wall)
    art = sbox(0, 0, art_w, art_h)
    return FP.polys_only(big.intersection(art)), FP.polys_only(big.difference(art))


def build_box(art_w, art_h, depth, frame=None, band=8.0):
    """箱を作る。内寸は絵の大きさ＋遊び、深さはタイルの厚み＋遊び。"""
    iw, ih = art_w + PLAY, art_h + PLAY
    ow, oh = iw + 2 * WALL, ih + 2 * WALL
    outer = I.card_polygon(ow, oh, CORNER, "round")
    inner = sbox(WALL, WALL, WALL + iw, WALL + ih)

    # 壁を2段に分ける。下段までをブーリアンで作り、模様は[* ポリゴンの段階で引いてから]
    # 上段として積む。模様を立体にしてから彫ろうとすると、弧の小片が数百個の別々の
    # 立体になり、manifold が「立体ではない」と拒む（2026-07-31に踏んだ）。
    low_h = FLOOR + depth - (ENGRAVE if frame else 0.0)
    body = I.extrude(outer, 0.0, low_h)
    pocket = I.extrude(inner, FLOOR, low_h + 1.0)
    box = trimesh.boolean.difference([body, pocket], engine="manifold")

    if frame:
        _, out_part = framed_pair(frame, art_w, art_h, band, WALL)
        out_part = translate(out_part, WALL + PLAY / 2.0, WALL + PLAY / 2.0)
        top = FP.polys_only(outer.difference(inner).difference(out_part))
        if not top.is_empty:
            box = trimesh.util.concatenate([box, I.extrude(top, low_h, ENGRAVE)])
    return box, (ow, oh, FLOOR + depth)


def main(argv=None):
    ap = argparse.ArgumentParser(description="画像タイルを収める額縁の箱を作る")
    ap.add_argument("--tiles", default="3x3", help="タイルの格子（例 3x3）")
    ap.add_argument("--flutes", type=int, default=9, help="タイル1枚あたりの笛の本数")
    ap.add_argument("--frame", default="seigaiha", help="壁の上面に彫る模様。none で彫らない")
    ap.add_argument("--band", type=float, default=8.0, help="タイル側の帯の幅[mm]")
    ap.add_argument("--tile-thick", type=float, default=4.78,
                    help="タイルの厚み[mm]（板0.8＋笛4）")
    ap.add_argument("-o", "--out", required=True, help="出力するSTL")
    args = ap.parse_args(argv)

    gx, gy = (int(v) for v in args.tiles.lower().split("x"))
    tw, th = tile_extent(args.flutes)
    art_w, art_h = tw * gx, th * gy
    depth = args.tile_thick + 0.3

    frame = None if args.frame in (None, "none", "") else args.frame
    box, (ow, oh, hz) = build_box(art_w, art_h, depth, frame=frame, band=args.band)

    os.makedirs(os.path.dirname(os.path.abspath(args.out)) or ".", exist_ok=True)
    box.export(args.out)
    print("タイル %.1f × %.1f mm × %d枚 → 絵 %.1f × %.1f mm" % (tw, th, gx * gy, art_w, art_h))
    print("箱: 外寸 %.1f × %.1f × %.1f mm（壁 %.1fmm・底 %.1fmm・内側の深さ %.1fmm）"
          % (ow, oh, hz, WALL, FLOOR, depth))
    print("    体積 %.1f cm3（材料の目安 %.0f g）" % (box.volume / 1000, box.volume / 1000 * 1.27))
    if frame:
        print("    壁の上面に %s を %.1fmm 彫った（タイル側の模様と同じ座標系）" % (frame, ENGRAVE))
    print("-> %s" % os.path.relpath(args.out, ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
