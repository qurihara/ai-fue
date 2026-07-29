"""v3カード2枚の復号結果（記号の列）を合わせて、元の秘密を出す。

カードは2-of-2の分散である。カードAには乱数、カードBには「秘密−乱数」が入っていて、
[* 2枚の値を足して 11^記号数 で割った余り]が秘密になる。片方だけでは何も分からない。

各カードは独立した符号語で、先頭に自分の基準笛C7を持つ。したがって[* 1枚ずつ別々に測り、
別々に復号する]。8本を続けて吹き、復号ページ（mode=symbols・parity=1）で出た記号の列を
そのまま渡せばよい。

使い方:
    python3 scripts/combine_card_shares.py "0,8,0,4,3,4" "0,9,8,5,5,3"
    python3 scripts/combine_card_shares.py --base 11 A の記号 B の記号
"""
from __future__ import annotations

import argparse
import sys


def to_value(symbols, base):
    v = 0
    for s in symbols:
        v = v * base + s
    return v


def parse(text):
    toks = [t for t in text.replace(",", " ").split() if t]
    try:
        return [int(t) for t in toks]
    except ValueError:
        raise SystemExit("記号は整数で渡す: %r" % text)


def main(argv=None):
    ap = argparse.ArgumentParser(description="v3カード2枚の記号列から秘密を復元する")
    ap.add_argument("card_a", help='カードAの記号列（例 "0,8,0,4,3,4"）')
    ap.add_argument("card_b", help='カードBの記号列')
    ap.add_argument("--base", type=int, default=11,
                    help="記号の底（12スロット・隣接同音禁止なら11。既定）")
    args = ap.parse_args(argv)

    a, b = parse(args.card_a), parse(args.card_b)
    if len(a) != len(b):
        raise SystemExit("記号の数が違う（A=%d個、B=%d個）。どちらかの読みが欠けている" % (len(a), len(b)))
    if any(not 0 <= s < args.base for s in a + b):
        raise SystemExit("記号が0から%dの範囲に無い。底が違うか、読み違えている" % (args.base - 1))

    n = len(a)
    span = args.base ** n
    va, vb = to_value(a, args.base), to_value(b, args.base)
    secret = (va + vb) % span

    print("記号は%d個ずつ、底は%d（表せるのは 0 から %d まで）" % (n, args.base, span - 1))
    print("  カードA の値: %d" % va)
    print("  カードB の値: %d" % vb)
    print("  合わせた秘密: %d" % secret)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
