"""クレジットカード大の暗号笛カードを2枚作り、境界にハートを抜く（分散暗号 v3）。

Chordika のカード（harmonica_deck/make_chordika_mini10.py）と同じ作りにする。

  8本の笛を0.3mmずつ重ねて融合すると、幅は 7 + 7×6.7 = 53.9mm になり、クレジットカードの
  短辺 53.98mm にちょうど収まる。笛の窓は上向き、吸込口はカードの短辺にそろう。
  厚み0.5mmの板を融合して総厚4mmにする（板を厚くするとボアを侵すので0.5mmから変えない）。

暗号笛なので、笛は[* 外見統一版]（外形を最長管に揃え、内部の仕切り壁で音を決める）を使う。
12音すべてを使うと外形長は66mmになり、カードの長辺85.6mmに対して足側に19.6mmの余白が残る。

2枚のカードを[* 余白どうしを向かい合わせ]に並べると、境界に39.2mm幅の平らな帯ができる。
そこへハートを抜く。ハートは境界をまたぐので、[* 1枚では半分のハートにしかならず、
2枚をそろえて初めてハートが現れる]。秘密分散の「2つ合わせて初めて開く」を、形が語る。

秘密の分け方は 2-of-2 である。片方に乱数、もう片方に「秘密−乱数」を入れる。

符号化はスプールや本立てと同じ fue/cipher_codec を使う。[* 隣り合う笛が必ず違う音になる]
（no_repeat）ので、無音を置かずに続けて吹いても1本ずつの区切りが分かる。先頭の1本は基準笛で、
温度と息の強さを打ち消す。残り7本のうちパリティに使う数だけ誤り訂正に回る。

  パリティ0 … 記号7個・24.2ビット（0〜19,487,170）。訂正はできない。
  パリティ1 … 記号6個・20.8ビット（0〜1,771,560）。既定。
  パリティ2 … 記号5個・17.3ビット（0〜161,050）。誤り1つを直せる。

使い方:
    python3 fue/cipher_cardpair.py                      # 既定（パリティ1）
    python3 fue/cipher_cardpair.py --parity 2           # 誤り訂正を厚くする
    python3 fue/cipher_cardpair.py --split-out          # 1枚ずつの3mfも書き出す
"""
from __future__ import annotations
import argparse
import math
import os
import sys

import numpy as np
import trimesh
from shapely.geometry import Polygon, MultiPolygon, Point
from shapely.affinity import scale as shp_scale, translate as shp_translate

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.pardir, "harmonica_deck"))
import cipher_codec
import mini10
import namecard as NC
import orient_check

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)
OUT = os.path.join(ROOT, "out")

CX, CY, CZ = 85.6, 53.98, 0.5      # クレジットカードの大きさと、融合する板の厚み
OVER = 0.3                          # 隣り合う笛の重なり（Chordikaと同じ）
CORNER_R = 2.0
N_FLUTES = 8
BAND_GAP = 1.5       # 笛の足から刻印帯までの距離[mm]
BAND_H = 4.0         # 刻印帯の文字高さ[mm]
STRAP_R = 2.5        # ストラップ穴の半径[mm]


def heart_polygon(width=34.0, height=30.0, cx=0.0, cy=0.0, n=240):
    """ハートの多角形。よく使われる媒介変数表示を、指定の大きさへ合わせる。"""
    # 始点と終点を重ねると多角形が退化して、押し出したメッシュが水密にならない
    ts = np.linspace(0, 2 * math.pi, n, endpoint=False)
    xs = 16 * np.sin(ts) ** 3
    ys = (13 * np.cos(ts) - 5 * np.cos(2 * ts)
          - 2 * np.cos(3 * ts) - np.cos(4 * ts))
    poly = Polygon(np.column_stack([xs, ys])).buffer(0)
    poly = shp_scale(poly, xfact=width / (xs.max() - xs.min()),
                     yfact=height / (ys.max() - ys.min()), origin="center")
    c = poly.centroid
    return shp_translate(poly, cx - c.x, cy - c.y)


def cut_plate(mesh, poly):
    """2Dの図形を、板(z=0..CZ)だけ貫通で抜く。上の笛には触れない（Chordikaと同じ）。"""
    geoms = list(poly.geoms) if isinstance(poly, MultiPolygon) else [poly]
    for g in geoms:
        if g.is_empty:
            continue
        pr = trimesh.creation.extrude_polygon(g, height=CZ + 0.4)
        pr.apply_translation([0, 0, -0.2])
        mesh = trimesh.boolean.difference([mesh, pr], engine="manifold")
    return mesh


def build_card(notes, l_max, mirror=False, label=None, strap=True):
    """8本の笛を載せたクレジットカード大の板を1枚作る。

    mirror=True なら左右を反転する（吸込口が反対の短辺に来る）。2枚を余白どうし
    向かい合わせに並べるために使う。
    """
    if len(notes) != N_FLUTES:
        raise ValueError("笛は%d本にする" % N_FLUTES)
    w = trimesh.load(mini10.BASE).extents[1]        # 笛の幅 ≈7mm
    step = w - OVER
    flutes, y = [], 0.0
    for note in notes:
        f = mini10.uniform_flute(mini10.length_for_note(note), L_max=l_max)
        f.apply_translation([0, y, 0])
        flutes.append(f)
        y += step
    comb = trimesh.boolean.union(flutes, engine="manifold")
    comb.merge_vertices()
    comb.apply_translation([0, (CY - comb.extents[1]) / 2.0, 0])   # 短辺の中央へ

    plate = trimesh.creation.box(extents=[CX, CY, CZ])
    plate.apply_translation([CX / 2, CY / 2, CZ / 2])
    card = trimesh.boolean.union([plate, comb], engine="manifold")
    keep = NC._corner_prism(CX, CY, CORNER_R, "round", -1.0, comb.bounds[1][2] + 1.0)
    card = trimesh.boolean.intersection([card, keep], engine="manifold")

    # 反転は刻印より先に行う。あとで反転すると文字が鏡文字になって読めなくなる。
    if mirror:
        card.apply_transform(trimesh.transformations.reflection_matrix(
            [CX / 2, 0, 0], [1, 0, 0]))
        card.apply_translation(-card.bounds[0] * np.array([1, 0, 0]))

    # 刻印帯：笛の足とハートのあいだの余白に、文字を板だけ貫通で抜く。
    # 2枚とも同じ文字列を入れる（対であることが物を見て分かるようにする）。
    if label:
        x_band = l_max + BAND_GAP + BAND_H / 2.0
        if mirror:
            x_band = CX - x_band            # 反転後の座標系では帯も反対の端に来る
        pl, _ = NC._text_line(label, x_band, BAND_H, CY, rot180=not mirror)
        if pl is not None and not pl.is_empty:
            card = cut_plate(card, pl)

    # ストラップ穴（板だけでなく全厚を貫通させる。笛には掛からない位置に置く）
    if strap:
        sx = STRAP_R + 3.0 if mirror else CX - (STRAP_R + 3.0)
        c = Point(sx, STRAP_R + 3.0).buffer(STRAP_R, resolution=48)
        pr = trimesh.creation.extrude_polygon(c, height=comb.bounds[1][2] + 2.0)
        pr.apply_translation([0, 0, -1.0])
        card = trimesh.boolean.difference([card, pr], engine="manifold")

    return card


def build_pair(notes_a, notes_b, l_max, heart=(17.0, 15.0), gap=0.0,
               label="CipherFlute 2of2"):
    """2枚を余白どうし向かい合わせに並べ、境界にハートを抜く。

    刻印は2枚とも同じ文字列にする。対の片割れどうしであることが、音を鳴らさなくても
    見ただけで分かるようにするためである。
    """
    a = build_card(notes_a, l_max, mirror=False, label=label)
    b = build_card(notes_b, l_max, mirror=True, label=label)
    b.apply_translation([CX + gap, 0, 0])

    top = max(a.bounds[1][2], b.bounds[1][2])
    hp = heart_polygon(heart[0], heart[1], cx=CX + gap / 2.0, cy=CY / 2.0)
    cutter = trimesh.creation.extrude_polygon(hp, height=top + 2.0)
    cutter.apply_translation([0, 0, -1.0])
    a = trimesh.boolean.difference([a, cutter], engine="manifold")
    b = trimesh.boolean.difference([b, cutter], engine="manifold")
    return a, b, hp


def split_secret(secret, m, n):
    """2-of-2 の分散。片方に乱数、もう片方に (秘密−乱数) を入れる。戻り値は m進 n桁の2つ。"""
    span = m ** n
    rnd = (7 ** n) % span                     # 記録のため決め打ちのデモ値
    a, b = rnd % span, (secret - rnd) % span
    def digits(v):
        out = []
        for _ in range(n):
            out.append(v % m)
            v //= m
        return out[::-1]
    return digits(a), digits(b), a, b


def codec_config(parity):
    """カードの符号化の設定。12スロット（G#6〜G7）・隣接同音禁止・基準笛C7。

    スプールや本立てと同じ fue/cipher_codec を使う。隣り合う笛が必ず違う音になるので、
    無音を置かずに続けて吹いても区切りが分かる。復号ページも同じ設定で読める。
    """
    return cipher_codec.CodecConfig(
        lo_note="G#6", hi_note="G7", reference_note="C7",
        no_repeat=True, use_reference=True, ecc_parity=parity)


def encode_share(value, n_symbols, parity):
    """share の値を、基準笛を先頭に置いた笛の音名の並びへ符号化する。"""
    cfg = codec_config(parity)
    base = cipher_codec._wire_params(cfg)[1]          # 記号の底（12スロットなら11）
    symbols, v = [], value
    for _ in range(n_symbols):
        symbols.append(v % base)
        v //= base
    return cipher_codec.encode_symbols(symbols[::-1], cfg).notes


def main(argv=None):
    ap = argparse.ArgumentParser(description="暗号笛カード2枚＋境界のハート（分散暗号v3）")
    ap.add_argument("--secret", type=int, default=260729,
                    help="デモの秘密（整数）。既定は今日の日付の下6桁")
    ap.add_argument("--parity", type=int, default=1,
                    help="誤り訂正のパリティ記号の数。0なら7記号(24.2bit)、1なら6記号(20.8bit)、"
                         "2なら5記号(17.3bit)まで運べる")
    ap.add_argument("--heart", type=float, nargs=2, default=(17.0, 15.0), help="ハートの幅と高さ")
    ap.add_argument("--label", default="CipherFlute 2of2",
                    help="刻印の文字列（2枚とも同じものを入れる）")
    ap.add_argument("--split-out", action="store_true",
                    help="2枚を別々の3mfにも書き出す（1枚ずつ印刷するため）")
    ap.add_argument("--out", default=os.path.join(OUT, "cipher_cardpair_v3.3mf"))
    args = ap.parse_args(argv)

    slots = mini10.CALIB12
    l_max = mini10.uniform_body_length([mini10.length_for_note(x) for x in slots])

    # 笛8本のうち1本は基準笛なので、データに使えるのは7本。そのうちパリティのぶんを
    # 引いた残りが、秘密そのものを運ぶ記号の数になる。
    cfg = codec_config(args.parity)
    base = cipher_codec._wire_params(cfg)[1]          # 12スロットなら記号の底は11
    n_sym = N_FLUTES - 1 - args.parity
    if n_sym < 1:
        raise SystemExit("パリティが多すぎる（笛は%d本しかない）" % N_FLUTES)
    span = base ** n_sym
    if not 0 <= args.secret < span:
        raise SystemExit(
            "秘密は 0 から %d までにする（記号%d個・底%d。パリティを減らせば広がる）"
            % (span - 1, n_sym, base))

    va, vb = split_secret(args.secret, base, n_sym)[2:]
    notes_a = encode_share(va, n_sym, args.parity)
    notes_b = encode_share(vb, n_sym, args.parity)
    for tag, ns in (("A", notes_a), ("B", notes_b)):
        if len(ns) != N_FLUTES:
            raise SystemExit("カード%sの笛が%d本になった（%d本にしたい）" % (tag, len(ns), N_FLUTES))
        if any(x == y for x, y in zip(ns, ns[1:])):
            raise SystemExit("カード%sに隣り合う同じ音がある" % tag)

    print("秘密 %d（0〜%d、記号%d個×底%d＝%.1f bit）" % (
        args.secret, span - 1, n_sym, base, n_sym * math.log2(base)))
    print("  カードA の笛: %s（値 %d）" % (" ".join(notes_a), va))
    print("  カードB の笛: %s（値 %d）" % (" ".join(notes_b), vb))
    print("  片方だけでは秘密は分からない（もう片方が乱数の役をする）")
    print("  先頭のC7は基準笛。温度と息の強さを打ち消す")
    print("  隣り合う笛は必ず違う音（no_repeat）。パリティ%d個ぶんの誤り訂正が付く" % args.parity)

    a, b, hp = build_pair(notes_a, notes_b, l_max, heart=tuple(args.heart),
                          label=args.label)
    res = orient_check.check_orientation(R=np.eye(3))
    print("向きの検査: 窓%+.0f度・長軸の傾き%.0f度 → %s（笛はnative姿勢のまま寝ている）"
          % (res.angle_deg, res.tilt_deg, res.verdict))

    sc = trimesh.Scene()
    sc.add_geometry(a, geom_name="cardA_0.08careful")
    sc.add_geometry(b, geom_name="cardB_0.08careful")
    os.makedirs(OUT, exist_ok=True)
    sc.export(args.out)
    print("カード1枚 %.1f×%.1f×%.1fmm、2枚並べて %s mm -> %s"
          % (*np.round(a.extents, 1), np.round(sc.bounds[1] - sc.bounds[0], 1),
             os.path.relpath(args.out, ROOT)))
    print("刻印は2枚とも「%s」（対であることが見て分かる）" % args.label)

    # 1枚ずつ印刷するために、別々の3mfにも書き出す。A1 miniは解凍後gcodeが4MB前後で
    # 頭打ちになるので、2枚を1つのプレートに載せると上限を超える。
    if args.split_out:
        base = os.path.splitext(args.out)[0]
        for tag, mesh in (("A", a), ("B", b)):
            one = mesh.copy()
            one.apply_translation(-one.bounds[0])
            p = "%s_%s.3mf" % (base, tag)
            trimesh.Scene({"card%s_0.08careful" % tag: one}).export(p)
            print("  1枚だけ書き出し -> %s" % os.path.relpath(p, ROOT))
    print("ハート %.0f×%.0fmm を境界にまたがせて抜いた（1枚では半分にしかならない）"
          % tuple(args.heart))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
