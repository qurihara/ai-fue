#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""単位体積あたりの情報量が最大になる音域の幅を求める。

なぜ要るか
----------
スロット数を12（実効の記号数11・位数11の有限体）にとった理由は、これまで2つであった。
隣り合う笛が同じ音にならない制約のもとで代償がゼロになることと、11が素数なので
リードソロモン符号をそのまま組めることである。**単位体積あたりの容量という観点は
確かめていなかった。** 論文（cipherflute-wiss2026）の3.3節「符号」に書いた数値は
このスクリプトが出す。

考え方
------
笛の外形は最長管に揃えるので、**いちばん低い音を決めると全部の笛の体積が決まる。**
音域を半音1つ広げると1本あたりの容量は log2(q-1) の分だけ増えるが、最低音の管が
2^(1/12)=5.9パーセント長くなり、体積はそろって増える。容量は対数でしか増えないので、
どこかに頂点がある。

前提の数はすべて実測または実際の較正値である。
  断面 7x4mm       … mini10/recorder-mini-c-v3-half-2-v2.stl の外形を実測
  外形長           … 最長管 + 余白3mm（fue/mini10.py の BODY_MARGIN）
  管長 L = A/f - e … A=87985.1, e=-10.010（out/cipher_mini10_calib.txt、コーム36本の実測）
  材料体積         … L=60mm で 852.8mm3、L=62.97mm で 891.1mm3 の実測2点から直線で当てはめ

結論（上端をG7に保ち、下端を動かした場合）
------------------------------------------
  頂点は10半音（11スロット）の 1.883 bit/cm3 にある。
  本実装の11半音（12スロット）は 1.873 bit/cm3 で、頂点の 0.55 パーセント下にとどまる。
  **実効の記号数が素数になる幅は7・11・13半音の3つしかなく、この中では11半音が最良である。**
  頂点にあたる10半音は実効の記号数が10で、素数でないため符号を組めない。
  密度に効くのは幅よりも音域の位置で、幅を保ったまま上端を1半音上げると約5パーセント増える。

ここで出す値は**笛1本が運ぶ生の情報量**であり、基準笛とパリティ笛の分は引いていない。
カード実装（8本・20.8bit）の実効は 1.41 bit/cm3、板ごと数えれば 1.13 bit/cm3 になる。
論文の表1は面積あたりで比べているので、この値をそのまま持ち込んではいけない。

使い方
    python3 scripts/info_density.py
"""
import math

# --- 前提の数 ---------------------------------------------------------------
A, E = 87985.1, -10.010          # 較正 f = A/(L+e)。out/cipher_mini10_calib.txt
SECTION = 7.0 * 4.0              # 断面[mm2]
MARGIN = 3.0                     # 外形長に持たせる余白[mm]。fue/mini10.BODY_MARGIN
MAT_SLOPE, MAT_INTERCEPT = 12.90, 79.1   # 材料体積[mm3] = 傾き*外形長 + 切片
TOP_MIDI = 103                   # 上端 G7。安定帯の上端は G#7(104)

NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
PRIMES = (7, 11, 13)             # 実効の記号数が素数になる幅（実用の範囲で）


def note_name(midi):
    return "%s%d" % (NAMES[midi % 12], midi // 12 - 1)


def freq(midi):
    return 440.0 * 2 ** ((midi - 69) / 12.0)


def pipe_length(midi):
    """その音を出す管の長さ[mm]。"""
    return A / freq(midi) - E


def body_length(k, top=TOP_MIDI):
    """幅k半音のときの外形長[mm]。最低音の管に余白を足したもの。"""
    return pipe_length(top - k) + MARGIN


def occupied_volume(k, top=TOP_MIDI):
    """笛1本が占める直方体の体積[mm3]。"""
    return SECTION * body_length(k, top)


def material_volume(k, top=TOP_MIDI):
    """笛1本の材料の体積[mm3]。半割で中空なので占有体積のおよそ半分になる。"""
    return MAT_SLOPE * body_length(k, top) + MAT_INTERCEPT


def bits_per_flute(k):
    """隣り合う笛が同じ音にならない制約のもとで、笛1本が運ぶ量[bit]。"""
    return math.log2(k)


def density(k, top=TOP_MIDI, volume=occupied_volume):
    """単位体積あたりの容量[bit/cm3]。"""
    return bits_per_flute(k) / volume(k, top) * 1000.0


def main():
    print("=== 幅ごとの密度（上端 G7 に固定し、下端を動かす）===")
    print("%4s %6s %10s %9s %10s %8s %10s" % (
        "半音", "スロット", "音域", "外形長", "占有体積", "bit/本", "bit/cm3"))
    rows = {}
    for k in range(2, 19):
        d = density(k)
        rows[k] = d
        print("%4d %6d %10s %9.2f %10.1f %8.3f %10.4f" % (
            k, k + 1, "%s-G7" % note_name(TOP_MIDI - k), body_length(k),
            occupied_volume(k), bits_per_flute(k), d))
    peak = max(rows, key=lambda k: rows[k])
    print("頂点は %d半音（%dスロット）の %.4f bit/cm3" % (peak, peak + 1, rows[peak]))
    print("本実装の11半音（12スロット）は %.4f bit/cm3 で、頂点の %.2f パーセント下\n"
          % (rows[11], (1 - rows[11] / rows[peak]) * 100))

    print("=== 符号を組める幅だけに絞る（実効の記号数が素数）===")
    for k in PRIMES:
        print("  %2d半音（位数%2d）… %.4f bit/cm3　頂点比 %+.2f パーセント"
              % (k, k, rows[k], (rows[k] / rows[peak] - 1) * 100))
    best_prime = max(PRIMES, key=lambda k: rows[k])
    print("  → この中では %d半音（%dスロット）が最良であり、本実装がこれにあたる\n"
          % (best_prime, best_prime + 1))

    print("=== 頂点の平らさ ===")
    for k in range(8, 14):
        print("  %2d半音 %.4f bit/cm3 （頂点比 %+.2f パーセント）"
              % (k, rows[k], (rows[k] / rows[peak] - 1) * 100))
    print()

    print("=== 材料の体積で測り直した場合 ===")
    mat = {k: density(k, volume=material_volume) for k in range(2, 19)}
    mpeak = max(mat, key=lambda k: mat[k])
    print("  頂点は %d半音の %.4f bit/cm3、本実装の11半音は %.4f で %.2f パーセント下\n"
          % (mpeak, mat[mpeak], mat[11], (1 - mat[11] / mat[mpeak]) * 100))

    print("=== 音域の位置を変えた場合（幅は11半音のまま）===")
    base = density(11, top=TOP_MIDI)
    for top in range(TOP_MIDI, TOP_MIDI + 5):
        d = density(11, top=top)
        print("  上端 %-4s … %.4f bit/cm3 （G7比 %+.1f パーセント）"
              % (note_name(top), d, (d / base - 1) * 100))
    print("  安定帯の上端は G#7 なので、1半音ぶんの余地が設計上ある（要実測）\n")

    print("=== 頂点が10付近になる理由 ===")
    print("  最適条件は 1/(k ln k) = (ln2/12) * (長さの可変分 / 外形長) である。")
    print("  可変分の割合が1なら k ln k = 12/ln2 = %.2f となり、k は 8.2 付近になる。"
          % (12 / math.log(2)))
    fixed = -E + MARGIN
    print("  実際には端補正 %.3fmm と余白 %.1fmm を合わせた %.2fmm が、"
          % (-E, MARGIN, fixed))
    print("  音の高さによらない固定分として乗るので、頂点が10付近まで押し上げられる。")
    var = A / freq(TOP_MIDI - 11)
    print("  本実装（11半音）では可変分 %.2fmm・固定分 %.2fmm で、可変の割合は %.3f である。"
          % (var, fixed, var / (var + fixed)))


if __name__ == "__main__":
    main()
