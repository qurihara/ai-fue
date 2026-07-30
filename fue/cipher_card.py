"""記号列を1枚のカードに載せる（しきい値秘密分散の断片を、カード1枚で持つため）。

cipher_cardpair.py は2-of-2の2枚組を作る専用だったが、2-of-3のように担体を混ぜる
（カード・箱・本立て）場合は、[* カード1枚に任意の記号列を載せる]口が必要になる。
形はcipher_cardpairのカードと同じで、笛8本・クレジットカード大・総厚4mmである。

使い方:
    python3 fue/cipher_card.py --symbols 4,9,5,10,3 --label "2 of 3" --index 2 \\
        --out out/cipher_card_v4_share2.3mf
"""
from __future__ import annotations

import argparse
import json
import os
import sys

import numpy as np
import trimesh

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.pardir, "harmonica_deck"))
import cipher_cardpair as CP
import cipher_codec as cd
import mini10
import orient_check

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)
OUT = os.path.join(ROOT, "out")
CONFIG = os.path.join(ROOT, "docs", "cipher", "cipher_config.json")
SLOT12 = dict(lo_note="G#6", hi_note="G7")


def main(argv=None):
    ap = argparse.ArgumentParser(description="記号列を1枚のカードに載せる")
    ap.add_argument("--symbols", required=True, help="載せる記号列（例 4,9,5,10,3）")
    ap.add_argument("--parity", type=int, default=2, help="RSブロックあたりのパリティ記号数")
    ap.add_argument("--label", default="CipherFlute", help="刻印の文字列")
    ap.add_argument("--index", type=int, default=None,
                    help="断片の番号。刻印の末尾に「#n」として足す")
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
    if len(notes) != CP.N_FLUTES:
        raise SystemExit("笛が%d本になった（カードは%d本）。記号数かパリティを見直す"
                         % (len(notes), CP.N_FLUTES))
    for i in range(len(notes) - 1):
        if notes[i] == notes[i + 1]:
            raise SystemExit("隣り合う笛が同じ音になっている")

    label = args.label if not args.index else "%s #%d" % (args.label, args.index)
    l_max = mini10.uniform_body_length(
        [mini10.length_for_note(x) for x in mini10.CALIB12])
    card = CP.build_card(notes, l_max, mirror=False, label=label)

    res = orient_check.check_orientation(R=np.eye(3))
    print("記号列 %s（%d個）→ 笛%d本: %s"
          % (",".join(map(str, syms)), len(syms), len(notes), " ".join(notes)))
    print("向きの検査: 窓%+.0f度（真上）・長軸の傾き%.0f度 → %s"
          % (res.angle_deg, res.tilt_deg, res.verdict))
    if res.verdict != "ok":
        raise SystemExit("向きの検査に通らない")

    os.makedirs(OUT, exist_ok=True)
    trimesh.Scene({"card_0.08careful": card}).export(args.out)
    print("カード %.1f×%.1f×%.1fmm、刻印「%s」-> %s"
          % (*np.round(card.extents, 1), label, os.path.relpath(args.out, ROOT)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
