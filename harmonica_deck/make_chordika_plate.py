"""Chordikaのカードを2枚ずつ並べた印刷プレートSTLを作る。

A1 mini で刷るとき、1プレートに2枚を並べる。結合した大きなswapファイルは展開に失敗して
直前のファイルを再生してしまうため（2026/7/25の事故）、[* プレートは必ず1ファイルずつ]にする。
このスクリプトは「2枚を並べた1プレートぶんのSTL」までを作り、スライスとswap生成は別で行う。

配置は既存の plate1・plate2 に合わせた。カード外形は 85.6×54.0×4.0（クレジットカード大・総厚4mm）で、
Y方向に 6.0mm の隙間を空けて2枚を積む。したがってプレート外形は 85.6×114.0×4.0 になる。
X方向には並べない。カードの長辺（笛の管の向き）を揃えておくと、ブリムの取り回しと剥がしが楽になる。

入力は out/chordika_v11_<調>.stl（make_chordika_mini10.py が出力したもの）。
調のラベルは make_chordika_mini10.KEYS の表記に従う（例 "C / Am"、"Db / Bbm"）。

使い方:
  python harmonica_deck/make_chordika_plate.py "B / G#m" "F# / D#m"
  python harmonica_deck/make_chordika_plate.py --rest        # C/Am と既存プレート以外を順に2枚ずつ
"""
import os
import sys

import trimesh

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, os.pardir)
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, HERE)
import make_chordika_mini10 as CK

GAP_Y = 6.0          # カード間の隙間。ブリム幅5mmが互いに干渉しない最小限
PREFIX = "chordika_v11"


def _safe(label):
    return CK._safe(label)


def card_path(label):
    return os.path.join(OUT, "%s_%s.stl" % (PREFIX, _safe(label)))


def build_plate(labels, outpath=None):
    """調のラベル2つ（またはそれ以上）を受け取り、Y方向に並べた1プレートぶんのSTLを書き出す。"""
    parts = []
    y = 0.0
    for label in labels:
        p = card_path(label)
        if not os.path.exists(p):
            raise SystemExit("カードのSTLが無い: %s（先に make_chordika_mini10.py を実行する）" % p)
        m = trimesh.load(p)
        b = m.bounds
        m.apply_translation([-b[0][0], -b[0][1] + y, -b[0][2]])   # 原点そろえ＋Y方向へ送る
        parts.append(m)
        y += (b[1][1] - b[0][1]) + GAP_Y
    plate = trimesh.util.concatenate(parts)
    if outpath is None:
        outpath = os.path.join(OUT, "%s_plate_%s.stl" % (PREFIX, "_".join(_safe(l) for l in labels)))
    plate.export(outpath)
    e = plate.extents
    print("  %s" % os.path.relpath(outpath, ROOT))
    print("     %s  外形 %.1f×%.1f×%.1f mm  カード%d枚（隙間%.1fmm）"
          % (" ＋ ".join(labels), e[0], e[1], e[2], len(labels), GAP_Y))
    return outpath


def remaining_keys(done):
    """まだプレートに載せていない調を、KEYSの順（五度圏）で返す。"""
    return [label for _pc, label in CK.KEYS if label not in done]


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--rest" in sys.argv:
        done = ["C / Am", "G / Em", "D / Bm", "A / F#m", "E / C#m", "B / G#m", "F# / D#m"]
        rest = remaining_keys(done)
        print("残りの調: %s" % " / ".join(rest))
        for i in range(0, len(rest), 2):
            build_plate(rest[i:i + 2])
    elif args:
        build_plate(args)
    else:
        raise SystemExit(__doc__)
