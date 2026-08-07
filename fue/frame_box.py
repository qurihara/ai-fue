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
import math
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

# 分けて刷るときの継ぎ手（当て板）
#
# ★相欠き（舌と座繰り）は試したうえでやめた★
# 底の厚みを半分ずつ食い違わせる継ぎ手は、接着面が板の面になるので確かに強い。
# ところが受ける側が[* 高さ0.85mmから12mm張り出す形]になり、下に何もないので
# サポートなしでは垂れる。斜めにして逃がそうにも、底が1.6mmしかないため
# 傾きが4度ほどにしかならず、水平と変わらない。
#
# そこで継ぎ目は単純な突き合わせにして、[* 箱の内側から当て板で留める]。
# 座繰りは上向きに開くので張り出しが出ず、当て板もただの平板で刷りやすい。
# 当て板はタイルの下に隠れる。
STRAP_T = 0.7     # 当て板の厚さ
STRAP_SEAT = 0.8  # 底の内側に掘る座繰りの深さ。当て板との差 0.10mm が遊びになる
STRAP_GAP = 0.2   # 当て板の外形を、座繰りより各辺これだけ小さくする

# 自立させる脚（透明フォトフレームの作りに倣う）
#
# 板の面から丸棒を垂直に突き出させ、[* 板の下端と棒の先端の2点]で支える。
# 棒が長いほど後ろの支点が遠くなり、倒れにくい。
#
# ★額縁と一体では作れない★
# 棒は背面から出るので、背面を下にして刷ると棒がベッドに刺さる向きになる。
# 表を下にすればポケットが204×194mmの巨大な張り出しになって刷れない。
# そこで[* 脚を別部品にして背面に貼る]。脚は棒を上に立てた向きで平らに刷れる。
# 額縁の底は1.6mmしかないので、棒を挿す穴を掘る手も取れない。
STAND_W = 40.0       # 背面板の幅
STAND_H = 25.0       # 背面板の高さ
STAND_T = 2.5        # 背面板の厚さ
STAND_ROD_D = 5.0    # 棒の直径
STAND_ROD_L = 30.0   # 棒が背面板から出る長さ
STAND_ROD_H = 8.3    # 棒の中心の高さ（背面板の下端から）。傾き12度になる値
STAND_X = 70.0       # 額縁の中心から左右へこの距離に貼る
STAND_MARK = 0.2     # 背面に彫る、貼る位置の印の深さ（1層ぶん）
STAND_MARK_W = 0.8   # 印の線の幅


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
    """箱を作る。内寸は絵の大きさ＋遊び、深さはタイルの厚み＋遊び。

    返り値は (下段の立体, 上段の模様のポリゴン, 上段の底の高さ, 外寸) である。
    [* 上段を立体にせずポリゴンのまま返す]のは、分けて刷るときに切るためである。
    立体にしてしまうと、弧の小片が数百個の別々の立体になり、水密でなくなって
    ブーリアンが通らない。ポリゴンなら平面で切るのも容易い。
    """
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

    top = None
    if frame:
        _, out_part = framed_pair(frame, art_w, art_h, band, WALL)
        out_part = translate(out_part, WALL + PLAY / 2.0, WALL + PLAY / 2.0)
        top = FP.polys_only(outer.difference(inner).difference(out_part))
        if top.is_empty:
            top = None
    return box, top, low_h, (ow, oh, FLOOR + depth)


def stack_top(solid, top, low_h):
    """下段の立体に、上段（模様のある壁の天面）を積む。"""
    if top is None or top.is_empty:
        return solid
    return trimesh.util.concatenate([solid, I.extrude(top, low_h, ENGRAVE)])


def _brick(lo, hi):
    """軸に沿った直方体。領域を切り出す道具として使う。"""
    ext = [hi[k] - lo[k] for k in range(3)]
    m = trimesh.creation.box(extents=ext)
    m.apply_translation([(lo[k] + hi[k]) / 2.0 for k in range(3)])
    return m


def stand_geometry(box_thick):
    """脚を付けたときの傾きと、倒れにくさの余裕を返す。

    机に着くのは[* 額縁の下端]と[* 棒の先端]の2点である。棒の先が床に届く条件から
    傾きが決まり、重心がその2点のあいだに落ちていれば立つ。
    """
    lever = box_thick + STAND_T + STAND_ROD_L      # 下端から棒の先までの、面に垂直な距離
    theta = math.degrees(math.atan(STAND_ROD_H / lever))
    return dict(theta=theta, lever=lever)


def stand_stability(oh, box_thick, cg_depth=4.0):
    """立てたときの重心と後ろの支点の位置（水平方向）を返す。差が余裕である。"""
    g = stand_geometry(box_thick)
    s = math.sin(math.radians(g["theta"]))
    c = math.cos(math.radians(g["theta"]))
    cg = (oh / 2.0) * s + cg_depth * c             # 重心。タイルを入れると少し表寄りになる
    pivot = STAND_ROD_H * s + g["lever"] * c       # 棒の先端
    return dict(theta=g["theta"], cg=cg, pivot=pivot, margin=pivot - cg)


def make_stand(n=2, pitch=10.0):
    """自立させる脚。背面板に丸棒が垂直に立つ。

    刷るときは[* 背面板を下にして棒を立てる]。棒はφ5×30mmの柱なので、そのまま載る。
    使うときは背面板を額縁の背面に貼り、棒が後ろへ突き出るようにする。
    """
    parts = []
    for i in range(n):
        plate = I.extrude(I.card_polygon(STAND_W, STAND_H, 2.0, "round"), 0.0, STAND_T)
        rod = trimesh.creation.cylinder(radius=STAND_ROD_D / 2.0,
                                        height=STAND_T + STAND_ROD_L, sections=48)
        # 板に食い込ませてから足す（面で接するだけだと立体にならない）
        rod.apply_translation([STAND_W / 2.0, STAND_ROD_H, (STAND_T + STAND_ROD_L) / 2.0])
        one = trimesh.boolean.union([plate, rod], engine="manifold")
        one.apply_translation([i * (STAND_W + pitch), 0.0, 0.0])
        parts.append(one)
    return trimesh.util.concatenate(parts)


def mark_stand(box, ow):
    """脚を貼る位置を、背面に細い枠として彫る。

    深さは1層ぶんにとどめる。背面はベッドに接する面なので、深く彫ると
    その上に張り出しができてしまう。1層なら、1層目に線が入るだけで済む。
    """
    cuts = []
    for sx in (-STAND_X, STAND_X):
        x0 = ow / 2.0 + sx - STAND_W / 2.0
        outer = sbox(x0, 0.0, x0 + STAND_W, STAND_H)
        inner = sbox(x0 + STAND_MARK_W, STAND_MARK_W,
                     x0 + STAND_W - STAND_MARK_W, STAND_H - STAND_MARK_W)
        ring = outer.difference(inner)
        cuts.append(I.extrude(FP.polys_only(ring), -0.1, STAND_MARK + 0.1))
    return trimesh.boolean.difference([box] + cuts, engine="manifold")


def strap_rects(ow, oh):
    """継ぎ目をまたぐ当て板の位置（箱の座標系での矩形）。

    中心の1枚が4つすべてを結び、残りの4枚が継ぎ目の外寄りを押さえる。
    継ぎ目は2本（縦と横）で中心が交わるので、この置き方で全部の継ぎ目に
    少なくとも2枚がかかる。
    """
    cx, cy = ow / 2.0, oh / 2.0
    return [
        (cx - 30, cy - 30, cx + 30, cy + 30),                 # 中心。4つを一度に結ぶ
        (cx - 12, cy + oh / 4 - 20, cx + 12, cy + oh / 4 + 20),   # 縦の継ぎ目・奥
        (cx - 12, cy - oh / 4 - 20, cx + 12, cy - oh / 4 + 20),   # 縦の継ぎ目・手前
        (cx + ow / 4 - 20, cy - 12, cx + ow / 4 + 20, cy + 12),   # 横の継ぎ目・右
        (cx - ow / 4 - 20, cy - 12, cx - ow / 4 + 20, cy + 12),   # 横の継ぎ目・左
    ]


def carve_straps(box, rects):
    """箱の底の内側に、当て板を落とす座繰りを掘る。"""
    cutters = [_brick((x0, y0, FLOOR - STRAP_SEAT), (x1, y1, FLOOR + 1.0))
               for (x0, y0, x1, y1) in rects]
    return trimesh.boolean.difference([box] + cutters, engine="manifold")


def make_straps(rects, bed=180.0, pitch=5.0):
    """当て板そのもの。刷りやすいように、原点のそばへ折り返しながら並べ直す。"""
    plates = []
    x = y = row = 0.0
    for (x0, y0, x1, y1) in rects:
        w = (x1 - x0) - 2 * STRAP_GAP
        d = (y1 - y0) - 2 * STRAP_GAP
        if x > 0 and x + w > bed:           # 一列に収まらなくなったら次の段へ
            x, y, row = 0.0, y + row + pitch, 0.0
        plates.append(_brick((x, y, 0.0), (x + w, y + d, STRAP_T)))
        x += w + pitch
        row = max(row, d)
    return trimesh.util.concatenate(plates)


def split_quarters(box, size):
    """箱を十字に4分割する。継ぎ目は単純な突き合わせで、当て板が留める。

    なぜ分けるか
    ------------
    箱は外寸 214.5 × 204.4mm あり、A1 mini のベッド（180 × 180mm）に入らない。
    斜めに置いても2分割では収まらない（214.5 × 102.2 を回しても最小の外接が
    214.5mm にしかならない）。4つに分ければ1個が 107.2 × 102.2mm になり、
    余裕をもって載る。
    """
    ow, oh, hz = size
    cx, cy = ow / 2.0, oh / 2.0
    BIG = 1e3
    parts = {}
    for i in (0, 1):
        for j in (0, 1):
            x0, x1 = (-BIG, cx) if i == 0 else (cx, BIG)
            y0, y1 = (-BIG, cy) if j == 0 else (cy, BIG)
            region = _brick((x0, y0, -BIG), (x1, y1, BIG))
            parts[(i, j)] = trimesh.boolean.intersection([box, region], engine="manifold")
    return parts


def main(argv=None):
    ap = argparse.ArgumentParser(description="画像タイルを収める額縁の箱を作る")
    ap.add_argument("--tiles", default="3x3", help="タイルの格子（例 3x3）")
    ap.add_argument("--flutes", type=int, default=9, help="タイル1枚あたりの笛の本数")
    ap.add_argument("--frame", default="seigaiha", help="壁の上面に彫る模様。none で彫らない")
    ap.add_argument("--band", type=float, default=8.0, help="タイル側の帯の幅[mm]")
    ap.add_argument("--tile-thick", type=float, default=4.78,
                    help="タイルの厚み[mm]（板0.8＋笛4）")
    ap.add_argument("-o", "--out", required=True, help="出力するSTL")
    ap.add_argument("--split", default="none",
                    help="分けて刷る（2x2）。A1 mini はベッドが180×180mmなので、"
                         "一体では入らない。継ぎ目は相欠きにする")
    ap.add_argument("--bed", type=float, default=180.0,
                    help="載せるベッドの一辺[mm]。分けたあとの寸法を検査する")
    ap.add_argument("--stand", action="store_true",
                    help="自立させる脚（丸棒2本）も作り、背面に貼る位置の印を彫る")
    args = ap.parse_args(argv)

    gx, gy = (int(v) for v in args.tiles.lower().split("x"))
    tw, th = tile_extent(args.flutes)
    art_w, art_h = tw * gx, th * gy
    depth = args.tile_thick + 0.3

    frame = None if args.frame in (None, "none", "") else args.frame
    box, top, low_h, (ow, oh, hz) = build_box(art_w, art_h, depth, frame=frame, band=args.band)
    if args.stand:
        box = mark_stand(box, ow)
    whole = stack_top(box, top, low_h)

    os.makedirs(os.path.dirname(os.path.abspath(args.out)) or ".", exist_ok=True)
    print("タイル %.1f × %.1f mm × %d枚 → 絵 %.1f × %.1f mm" % (tw, th, gx * gy, art_w, art_h))
    print("箱: 外寸 %.1f × %.1f × %.1f mm（壁 %.1fmm・底 %.1fmm・内側の深さ %.1fmm）"
          % (ow, oh, hz, WALL, FLOOR, depth))
    print("    体積 %.1f cm3（材料の目安 %.0f g）" % (whole.volume / 1000, whole.volume / 1000 * 1.27))
    if frame:
        print("    壁の上面に %s を %.1fmm 彫った（タイル側の模様と同じ座標系）" % (frame, ENGRAVE))

    if args.stand:
        stem, ext = os.path.splitext(args.out)
        stand = make_stand()
        spath = "%s_stand%s" % (stem, ext)
        stand.export(spath)
        st = stand_stability(oh, hz)
        lo, hi = stand.bounds
        print()
        print("自立させる脚を2本作った（背面板 %.0f×%.0f×%.1fmm ＋ 丸棒 φ%.0f×%.0fmm）"
              % (STAND_W, STAND_H, STAND_T, STAND_ROD_D, STAND_ROD_L))
        print("  傾き %.1f度（棒の中心を背面板の下端から %.1fmm に置いた結果）"
              % (st["theta"], STAND_ROD_H))
        print("  倒れにくさ … 重心 %.1fmm ／ 後ろの支点 %.1fmm ／ 余裕 %.1fmm"
              % (st["cg"], st["pivot"], st["margin"]))
        print("  貼る位置 … 額縁の背面、下端に揃えて中心から左右 ±%.0fmm（印を %.1fmm 彫ってある）"
              % (STAND_X, STAND_MARK))
        print("  刷る向き … 背面板を下にして棒を立てる。並べて %.0f×%.0f×%.1fmm"
              % (hi[0] - lo[0], hi[1] - lo[1], hi[2] - lo[2]))
        print("      -> %s" % os.path.relpath(spath, ROOT))
        if st["margin"] < 8.0:
            raise SystemExit("脚の余裕が乏しい（%.1fmm）。棒を長くするか、位置を下げること。"
                             % st["margin"])
        print()

    if args.split in (None, "none", ""):
        whole.export(args.out)
        if max(ow, oh) > args.bed:
            print("    ※ベッド %.0fmm には入らない。--split 2x2 で分けて刷れる" % args.bed)
        print("-> %s" % os.path.relpath(args.out, ROOT))
        return 0

    if args.split != "2x2":
        raise SystemExit("いまのところ分けられるのは 2x2 だけである（指定は %s）。" % args.split)

    rects = strap_rects(ow, oh)
    box = carve_straps(box, rects)          # 先に当て板の座繰りを掘ってから分ける
    parts = split_quarters(box, (ow, oh, hz))
    stem, ext = os.path.splitext(args.out)
    names = {(0, 0): "左手前", (1, 0): "右手前", (0, 1): "左奥", (1, 1): "右奥"}
    print()
    print("十字に4分割した（継ぎ目は突き合わせ。箱の内側から当て板%d枚で留める）" % len(rects))
    cx, cy, BIG = ow / 2.0, oh / 2.0, 1e3
    total = 0.0
    bad = []
    for (i, j), solid in sorted(parts.items()):
        total += solid.volume            # 検査は下段どうしで突き合わせる
        # 模様のある天面は、舌に関わらない高さにあるので単純に十字で切る。
        # 同じ座標系から切り出すので、組んだときに模様はぴったり続く。
        sub = None
        if top is not None:
            q = sbox(-BIG if i == 0 else cx, -BIG if j == 0 else cy,
                     cx if i == 0 else BIG, cy if j == 0 else BIG)
            sub = FP.polys_only(top.intersection(q))
        part = stack_top(solid, sub, low_h)
        lo, hi = part.bounds
        w, d, h = hi - lo
        path = "%s_%d%d%s" % (stem, i + 1, j + 1, ext)
        part.export(path)
        ng = []
        # 水密かどうかは[* 下段で見る]。模様を積んだあとは、弧の小片が別々の立体に
        # なるので水密にならない（一体で出しているときと同じで、スライサは通る）。
        if not solid.is_watertight:
            ng.append("水密でない")
        if max(w, d) > args.bed:
            ng.append("ベッドに入らない")
        bad += [(path, s) for s in ng]
        print("  %s … %.1f × %.1f × %.1f mm・%.1f cm3（%.0f g）  %s"
              % (names[(i, j)], w, d, h, part.volume / 1000, part.volume / 1000 * 1.27,
                 "／".join(ng) if ng else "ok"))
        print("      -> %s" % os.path.relpath(path, ROOT))
    # 分けたあとの体積の和は、元とぴったり合うはずである（突き合わせなので遊びがない）。
    # 合わなければ領域の作り方が間違っている（重なりか抜けがある）。
    ratio = total / box.volume
    print("  体積の和は元の %.3f%%" % (ratio * 100))
    if not 0.999 < ratio < 1.001:
        bad.append(("全体", "体積が合わない（%.3f%%）" % (ratio * 100)))

    straps = make_straps(rects, bed=args.bed)
    spath = "%s_straps%s" % (stem, ext)
    straps.export(spath)
    lo, hi = straps.bounds
    print("  当て板 %d枚 … 並べて %.1f × %.1f mm・厚さ %.1fmm・%.1f cm3（%.0f g）"
          % (len(rects), hi[0] - lo[0], hi[1] - lo[1], STRAP_T,
             straps.volume / 1000, straps.volume / 1000 * 1.27))
    print("      -> %s" % os.path.relpath(spath, ROOT))
    if max(hi[0] - lo[0], hi[1] - lo[1]) > args.bed:
        bad.append((spath, "ベッドに入らない"))

    if bad:
        raise SystemExit("分割の検査に通らない: "
                         + "／".join("%s: %s" % (os.path.basename(p), s) for p, s in bad))

    # 2個を並べて刷れるかどうか。並べられれば印刷の回数が減る
    ws = sorted(max(p.bounds[1][:2] - p.bounds[0][:2]) for p in parts.values())
    if ws[0] + ws[1] <= args.bed:
        print("  小さい2個は並べて刷れる（%.1f + %.1f = %.1fmm）。"
              % (ws[0], ws[1], ws[0] + ws[1]))
    else:
        print("  4個は1枚ずつ刷る（小さい2個を並べても %.1fmm でベッド %.0fmm に入らない）。"
              % (ws[0] + ws[1], args.bed))
    print("  組み立て … 継ぎ目を突き合わせて接着し、箱の内側の座繰りに当て板を落として接着する。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
