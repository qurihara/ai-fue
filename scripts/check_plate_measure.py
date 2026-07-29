"""スプール1枚だけの実測周波数を集計して、造形と較正の出来を見る。

基準笛が別のプレートにある場合でも、[* 1本目を仮の基準にすれば相対の並びは検証できる]。
復号器がやっているのと同じ「基準との比を半音刻みへ丸める」計算を、仮の基準で行う。
全体に共通するずれ（温度・息の強さ・材料）は比を取る時点で消えるので、残るのは笛ごとの
ばらつきだけであり、それが50セントの判定境界にどれだけ余裕を持っているかが分かる。

出すもの:
  * 鳴らなかった笛の位置（測定値に - か x と書いた箇所）
  * 笛ごとのずれ（セント）と、その中央値を引いた残差
  * 仮の基準に対する相対スロットの判定が、設計どおりかどうか
  * 判定境界（±50セント）までの最小の余裕

使い方:
    python3 scripts/check_plate_measure.py out/spool128_plate2.3mf 測定値.txt

測定値ファイルは、1回ぶんの吹鳴を1つのまとまりとして空行で区切って並べる。
鳴らなかった笛は - か x と書く。# で始まる行は注釈として読み飛ばす。
"""
from __future__ import annotations

import os
import re
import sys
import warnings

warnings.filterwarnings("ignore")
import numpy as np
import trimesh

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, "fue"))
from notes import note_to_freq


def notes_from_3mf(path):
    """3mfのオブジェクト名から、吹く順番どおりの音名を取り出す。"""
    scene = trimesh.load(path)
    found = {}
    for key in scene.geometry:
        m = re.match(r"flute(\d+)_([A-G]#?\d)_", key)
        if m:
            found[int(m.group(1))] = m.group(2)
    if not found:
        raise SystemExit("笛のオブジェクト名が見つからない: %s" % path)
    return [found[i] for i in sorted(found)]


def read_measured(path, n):
    """測定値ファイルを読む。1回ぶん n 個の並びのリストを返す。鳴らない笛は None。"""
    runs, cur = [], []
    for line in open(path, encoding="utf-8"):
        line = line.split("#")[0].strip()
        if not line:
            if cur:
                runs.append(cur)
                cur = []
            continue
        for tok in line.split():
            cur.append(None if tok in ("-", "x", "X") else float(tok))
    if cur:
        runs.append(cur)
    for i, r in enumerate(runs):
        if len(r) != n:
            raise SystemExit("%d回目の測定が%d個ある（笛は%d本）" % (i + 1, len(r), n))
    return runs


def cents(a, b):
    return 1200.0 * np.log2(a / b)


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if len(argv) < 2:
        raise SystemExit(__doc__)
    three_mf, measured = argv[0], argv[1]

    notes = notes_from_3mf(three_mf)
    ideal = np.array([note_to_freq(n) for n in notes])
    print("%s … 笛%d本" % (os.path.basename(three_mf), len(notes)))
    print("意図した並び: %s" % " ".join(notes))

    runs = read_measured(measured, len(notes))
    print("測定は%d回ぶん" % len(runs))

    arr = np.array([[np.nan if v is None else v for v in r] for r in runs], dtype=float)
    dead = [i + 1 for i in range(len(notes)) if np.all(np.isnan(arr[:, i]))]
    print("鳴らなかった笛: %s" % ("なし" if not dead else " ".join("%d本目(%s)" % (i, notes[i - 1]) for i in dead)))

    mean = np.nanmean(arr, axis=0)
    with np.errstate(invalid="ignore"):
        dev = cents(mean, ideal)
    common = np.nanmedian(dev)
    resid = dev - common
    print("全体に共通するずれ: %+.1f セント（比で読むので復号には効かない）" % common)
    print("共通分を引いた残差: 標準偏差 %.1f セント・最大 %.1f セント"
          % (np.nanstd(resid), np.nanmax(np.abs(resid))))

    # 仮の基準（最初に鳴った笛）に対する相対スロットの判定
    base = next((i for i in range(len(notes)) if not np.isnan(mean[i])), None)
    if base is None:
        raise SystemExit("どの笛も鳴っていない")
    print("仮の基準は%d本目(%s)" % (base + 1, notes[base]))
    ng, margins = [], []
    print()
    print(" 番号 音名   実測Hz   狙いHz   ずれ  残差  相対半音(実測/設計) 判定")
    for i, note in enumerate(notes):
        if np.isnan(mean[i]):
            print(" %3d  %-4s      --                                        鳴らない" % (i + 1, note))
            continue
        rel = cents(mean[i], mean[base]) / 100.0
        want = round(cents(ideal[i], ideal[base]) / 100.0)
        got = int(round(rel))
        margin = 50.0 - abs(rel - got) * 100.0
        margins.append(margin)
        ok = (got == want)
        if not ok:
            ng.append(i + 1)
        print(" %3d  %-4s %8.1f %8.1f %+6.0f %+5.0f   %+4d / %+4d       %s"
              % (i + 1, note, mean[i], ideal[i], dev[i], resid[i], got, want,
                 "ok" if ok else "★ずれ"))
    print()
    print("相対スロットを誤った笛: %s" % ("なし" if not ng else " ".join(map(str, ng))))
    if margins:
        k = int(np.argmin(margins))
        print("判定境界（±50セント）までの最小の余裕: %.0f セント" % min(margins))
    if len(runs) > 1:
        spread = np.nanstd(arr, axis=0)
        print("同じ笛を吹き直したときのばらつき: 平均 %.1f Hz（%.1f セント相当）"
              % (np.nanmean(spread), np.nanmean(1200 * spread / (mean * np.log(2)))))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
