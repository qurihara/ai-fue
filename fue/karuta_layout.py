#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""百人一首の読み札のような版下を組む。歌人の絵と、縦書きの和歌を1枚に収める。

なぜ版下を先に作るか
--------------------
カードは2色で刷るので、**最後は白と黒の2値になる**。階調は残らない。だから
「刷ってみたら文字が潰れた」を避けるには、版下の段階で2値にしたときの見え方を
決めておく必要がある。ここでは白地に黒で組み、絵はしきい値で2値化する。

★文字の大きさは画素の粗さで決まる★
------------------------------------
板は `pixel` mm 刻みの格子に量子化される（既定0.4mm）。カードの高さ54mmを縦書き3行に
割ると1文字あたり9mm弱、0.4mm刻みでは22画素ほどになる。ひらがなは読めるが、
画数の多い漢字はこのあたりが限界である。**行を増やして字を小さくしてはいけない。**

構成
----
**絵は札の全面に敷き、その上へ和歌を重ねる。** 実際の百人一首の読み札がそうなっている。
絵の側は人物を左へ寄せて右半分を余白にしてあるので、そこへ縦書きの歌が乗る。

    全面        歌人の絵
    右側        和歌を縦書き。いちばん右の細い列に歌人の名前

★絵と歌を左右に分割してはいけない★ 分割すると絵が細くなり、札というより名刺に見える。
札に見えるかどうかは、絵が紙面いっぱいに広がっているかで決まる。

使い方
------
    python3 fue/karuta_layout.py --illust out/karuta/izumi_a.png \\
        --text "あらざらむこの世のほかの思ひ出に" --poet 和泉式部 \\
        -o out/karuta/fuda_upper.png
"""
from __future__ import annotations

import argparse
import os

from PIL import Image, ImageDraw, ImageFont

# ★毛筆の書体を使う★ このMacの標準には明朝と角ゴシックしか無く、和歌には硬い。
# Yuji Syuku（尹朱肅）は SIL Open Font License の毛筆書体で、わずかに崩した線が
# 百人一首に合う。assets/fonts/ に本体とライセンスを収めてある。
_HERE = os.path.dirname(os.path.abspath(__file__))
BRUSH = os.path.join(_HERE, os.pardir, "assets", "fonts", "YujiSyuku-Regular.ttf")
MINCHO = BRUSH if os.path.exists(BRUSH) else "/System/Library/Fonts/ヒラギノ明朝 ProN.ttc"
CX_MM, CY_MM = 85.6, 53.98
DPMM = 12                      # 版下の細かさ[画素/mm]。板の量子化(0.4mm)より十分細かく取る
W, H = int(CX_MM * DPMM), int(CY_MM * DPMM)

POEM_W_MM = 30.0               # 和歌を重ねる帯の幅[mm]。絵の右半分に乗る
POET_COL_MM = 9.0              # 歌人の名前の列
PAD_MM = 2.5
FRAME_PAD_MM = 3.4             # 外枠を描くとき、文字を内側へ寄せる量[mm]
ILLUST_BAND_MM = 52.0          # 縦長の札で絵に充てる高さ[mm]。残りが歌の場所になる


def _mm(v):
    return int(round(v * DPMM))


def vertical_text(draw, text, cx, top, size, fill=0, leading=1.06):
    """1文字ずつ縦に置く。縦書き用の字形は使わず、素直に積む。"""
    font = ImageFont.truetype(MINCHO, size)
    y = top
    for ch in text:
        b = draw.textbbox((0, 0), ch, font=font)
        w = b[2] - b[0]
        draw.text((cx - w / 2 - b[0], y - b[1]), ch, font=font, fill=fill)
        y += int(size * leading)
    return y


def _lines_of(text):
    """句の区切り（/）で分けて行にする。★1行＝1句が原則★

    和歌は五七五七七の切れ目で読む。字数をそろえて機械的に折ると、句の途中で行が
    変わって歌に見えなくなる。呼ぶ側が「あらざらむ/このよのほかの/おもひでに」の
    ように句で渡す。区切りが無ければ、そのまま1行として扱う。
    """
    return [t for t in text.split("/") if t]


def _flow(text, n_lines):
    """字数をそろえて n 行に流し込む。★句の区切りを無視して詰める版★

    五七五七七で折ると行の長さがばらつき、字を大きく取れない。札いっぱいに
    大きな字で組みたいときは、こちらで均等に割る。
    """
    text = text.replace("/", "")
    per = -(-len(text) // n_lines)
    return [text[i * per:(i + 1) * per] for i in range(n_lines) if text[i * per:(i + 1) * per]]


def _best_flow(text, w_mm, h_mm, pad_mm, leading=1.06, line_gap=1.18):
    """札に収まる中で、いちばん字を大きくできる行数と大きさを探す。"""
    best = None
    plain = text.replace("/", "")
    for n in range(2, 9):
        lines = _flow(plain, n)
        longest = max(len(t) for t in lines)
        by_h = (h_mm - pad_mm * 2) / (longest * leading)      # 縦に収まるか
        by_w = (w_mm - pad_mm * 2) / (len(lines) * line_gap)  # 横に並ぶか
        size = min(by_h, by_w)
        if best is None or size > best[0]:
            best = (size, n, lines)
    return best


def _fit_font_mm(lines, avail_mm, leading=1.06, cap=None):
    """いちばん長い句が縦に収まる文字の大きさを求める。"""
    longest = max(len(t) for t in lines)
    v = avail_mm / (longest * leading)
    return min(v, cap) if cap else v


def draw_frame(d, w, h, inset_mm=2.2, width_mm=1.1, gap_mm=0.9, double=True):
    """かるた札の外枠。細い二重罫にすると札らしくなる。"""
    def rect(inset, width):
        a, b = _mm(inset), _mm(width)
        d.rectangle([a, a, w - 1 - a, h - 1 - a], outline=0, width=b)
    rect(inset_mm, width_mm)
    if double:
        rect(inset_mm + width_mm + gap_mm, max(0.4, width_mm * 0.45))


def build(illust_path, text, poet, out_path, cols=3, font_mm=None, portrait=False,
          right_pad_mm=None, frame=False, flow=False, valign="top",
          hcenter=False, top_reserve_mm=0.0):
    """札を1枚組む。★絵は全面に敷き、その上へ歌を重ねる（縦長でも同じ）★

    絵と歌が重なるのは百人一首の読み札のふるまいであり、避けるべきものではない。
    重ねる前提にすると文字を大きく取れるので、2色に落としたときも読める。
    """
    w, h = (H, W) if portrait else (W, H)
    card = Image.new("L", (w, h), 255)
    lines = _lines_of(text)
    auto_size = None
    if flow:
        auto_size, _, lines = _best_flow(text, w / DPMM, h / DPMM,
                                         PAD_MM + (FRAME_PAD_MM if frame else 0.0))

    if False:
        # --- 縦長の札。★人物を下半分へ置き、上に歌の場所を空ける★ ---
        # 実物の百人一首の読み札がこの割りである。絵を全面に伸ばすと歌が絵の上に
        # 乗って読みにくくなるので、縦長では上下に分ける。
        band = _mm(ILLUST_BAND_MM)
        if illust_path and os.path.exists(illust_path):
            im = Image.open(illust_path).convert("L")
            scale = max(w / im.width, band / im.height)
            im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))),
                           Image.LANCZOS)
            left = (im.width - w) // 2
            top = im.height - band          # 下端を合わせて切る（人物の足元を残す）
            card.paste(im.crop((left, top, left + w, top + band)), (0, h - band))

        d = ImageDraw.Draw(card)
        size = _mm(font_mm)
        x_right = w - _mm(PAD_MM)
        span = w - _mm(PAD_MM * 2)
        # ★行数は字数から決める★ 4行に決め打ちすると、13文字の下の句で最終行が
        # 「な」1文字だけになり間が抜ける。**最終行が2文字を切るなら行数を1つ減らす。**
        n = cols
        while n > 1 and len(text) - ((len(text) + n - 1) // n) * (n - 1) < 2:
            n -= 1
        per = (len(text) + n - 1) // n
        for i in range(n):
            chunk = text[i * per:(i + 1) * per]
            if not chunk:
                continue
            cx = x_right - span * (i + 0.5) / n
            vertical_text(d, chunk, cx, _mm(PAD_MM), size)
        card.save(out_path)
        return out_path

    # --- 絵を札の全面に敷く（縦長でも横長でも同じ） ---
    if illust_path and os.path.exists(illust_path):
        im = Image.open(illust_path).convert("L")
        scale = max(w / im.width, h / im.height)
        im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))),
                       Image.LANCZOS)
        left = (im.width - w) // 2
        top = (im.height - h) // 2
        card.paste(im.crop((left, top, left + w, top + h)), (0, 0))

    d = ImageDraw.Draw(card)
    if frame:
        draw_frame(d, w, h)
    avail = h / DPMM - (PAD_MM + (FRAME_PAD_MM if frame else 0.0)) * 2
    fmm = font_mm or auto_size or _fit_font_mm(lines, avail, cap=11.0)
    size = _mm(fmm)

    # 右から左へ、1行ずつ置く
    block_w = len(lines) * size * 1.18
    if hcenter:
        # ★文字の塊を札の左右中央に置く★ 右端からの一定の余白ではなく、
        # 塊の幅から左右の余白を等しく取る。行数が変わっても重心が動かない。
        x_right = int(w - (w - block_w) / 2)
    else:
        right_pad = right_pad_mm if right_pad_mm is not None else PAD_MM
        right_pad += (FRAME_PAD_MM if frame else 0.0) + (POET_COL_MM if poet else 0.0)
        x_right = w - _mm(right_pad)
    step = size * 1.18
    pad = _mm(PAD_MM + (FRAME_PAD_MM if frame else 0.0))
    for i, line in enumerate(lines):
        cx = x_right - step * (i + 0.5)
        # ★上下の寄せ★ 3通りある。
        #   top    … 全行を上端から。字数の違う行は下が空く
        #   center … 行ごとに中央へ。行の頭がそろわず、和歌には向かない
        #   block  … ★全行の頭をそろえ、文字の塊ごと札の中央へ置く★
        #             行の字数が違っても頭が一直線に並び、かつ重心が中ほどに来る
        if valign == "center":
            used = len(line) * size * 1.06
            top = int((h - used) / 2)
        elif valign == "block":
            # ★上に確保した帯（ストラップ穴の場所）を除いた範囲の中央へ置く★
            longest = max(len(t) for t in lines)
            used = longest * size * 1.06
            reserve = _mm(top_reserve_mm)
            top = reserve + int((h - reserve - used) / 2)
        else:
            # ★上端そろえ★ 2枚組では、行数や字数が違っても上端を同じにしたい。
            # block（塊ごと中央）は最長行の長さで位置が動くので、対の札では頭がずれる。
            top = pad + _mm(top_reserve_mm)
        vertical_text(d, line, cx, top, size)

    if poet:
        vertical_text(d, poet, w - _mm(PAD_MM + POET_COL_MM / 2), _mm(PAD_MM),
                      int(size * 0.62))

    card.save(out_path)
    return out_path


def main(argv=None):
    ap = argparse.ArgumentParser(description="かるたの読み札の版下を組む")
    ap.add_argument("--illust", default=None, help="歌人の絵")
    ap.add_argument("--text", required=True, help="刷る和歌（上の句か下の句）")
    ap.add_argument("--poet", default="", help="歌人の名前")
    ap.add_argument("--cols", type=int, default=3, help="（使わない。句の数で行が決まる）")
    ap.add_argument("--font-mm", type=float, default=None,
                    help="文字の大きさ[mm]。省くといちばん長い句が収まる大きさを自動で決める")
    ap.add_argument("--portrait", action="store_true", help="縦長の札にする")
    ap.add_argument("--frame", action="store_true", help="かるた札のように外枠を縁取る")
    ap.add_argument("--hcenter", action="store_true", help="文字の塊を左右中央に置く")
    ap.add_argument("--top-reserve", type=float, default=0.0,
                    help="上に空けておく帯の高さ[mm]。ストラップ穴の場所にする")
    ap.add_argument("--valign", default="top", choices=["top", "center", "block"],
                    help="上下の寄せ。block は行の頭をそろえたまま塊ごと中央へ置く")
    ap.add_argument("--flow", action="store_true",
                    help="句の区切りを無視し、札いっぱいに大きな字で均等に流し込む")
    ap.add_argument("--right-pad", type=float, default=None,
                    help="歌の右端の余白[mm]。大きくすると歌が左へ寄る")
    ap.add_argument("-o", "--out", required=True)
    args = ap.parse_args(argv)
    p = build(args.illust, args.text, args.poet, args.out, args.cols, args.font_mm,
              portrait=args.portrait, right_pad_mm=args.right_pad,
              frame=args.frame, flow=args.flow, valign=args.valign,
              hcenter=args.hcenter, top_reserve_mm=args.top_reserve)
    im = Image.open(p)
    print("版下 %s（%d×%d 画素 = %.1f×%.1fmm）" % (p, im.width, im.height, CX_MM, CY_MM))
    if args.flow:
        w = CY_MM if args.portrait else CX_MM
        h = CX_MM if args.portrait else CY_MM
        fmm, _, lines = _best_flow(args.text, w, h,
                                   PAD_MM + (FRAME_PAD_MM if args.frame else 0.0))
        fmm = args.font_mm or fmm
    else:
        lines = _lines_of(args.text)
        avail = (CX_MM if args.portrait else CY_MM) - PAD_MM * 2
        fmm = args.font_mm or _fit_font_mm(lines, avail, cap=11.0)
    print("%d行（%s）／1文字 %.1fmm＝板の量子化0.4mmで約%d画素"
          % (len(lines), "・".join(str(len(t)) for t in lines), fmm, fmm / 0.4))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
