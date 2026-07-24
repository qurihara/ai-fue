"""厚壁・深窓mini10 の較正式 f = A/(L+e) を実測データから再フィットする。

背景: 現行は較正コーム5点フィットで A=86338, e=-13.06（RMS 35.2 cent・やや低めに出る＝要精緻化）。
このセッションでは手元のC/Amカード2枚（実カード＝実際に鳴らして使うジオメトリ）の実測Hzで
フィットし直し、基準窓 G6〜F#7 の管長を確定する。

モデル: f = A/(L+e)。変形すると A − e·f = f·L となり (A, e) について線形。
        よって最小二乗 [1, −f_i]·[A, e]ᵀ = f_i·L_i を解く。

使い方:
  DATA に (管長mm, 実測Hz) を入れて実行。設計管長→目標Hzの対応は card_CAm_measure_sheet.txt 参照。
  8本の異なる管長: G7=40.6, F7=44.0, E7=45.8, D7=49.8, C7=54.3, B6=56.8, A6=62.1, G6=68.1

実行: /Users/kurihara/Desktop/claude_work/mesh_venv/bin/python mini10/refit_calib.py
"""
import os
import numpy as np

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, os.pardir, "out")

# (管長mm, 実測Hz)。栗原さんが手元カードを吹いて測った値をここに入れる。
# ↓ 実測が入るまでは現行フィットの根拠＝較正コーム5点（比較用）。
DATA = [
    # (40.6, ____),  # G7 目標3136
    # (44.0, ____),  # F7 目標2794
    # (45.8, ____),  # E7 目標2637
    # (49.8, ____),  # D7 目標2349
    # (54.3, ____),  # C7 目標2093 ＊主音
    # (56.8, ____),  # B6 目標1976
    # (62.1, ____),  # A6 目標1760
    # (68.1, ____),  # G6 目標1568
]

# 参考: 較正コーム5点（旧フィットの根拠。実測が無いとき比較に使う）
COMB5 = [(72, 1480), (64, 1689), (56, 1987), (48, 2413), (40, 3320)]


def fit(data):
    L = np.array([d[0] for d in data], float)
    f = np.array([d[1] for d in data], float)
    # [1, -f]·[A,e] = f*L
    M = np.column_stack([np.ones_like(f), -f])
    rhs = f * L
    (A, e), *_ = np.linalg.lstsq(M, rhs, rcond=None)
    pred = A / (L + e)
    cents = 1200.0 * np.log2(pred / f)
    rms = float(np.sqrt(np.mean(cents ** 2)))
    return A, e, rms, list(zip(L.tolist(), f.tolist(), np.round(pred, 1).tolist(), np.round(cents, 1).tolist()))


def length_for(freq, A, e):
    return A / freq - e


if __name__ == "__main__":
    data = [d for d in DATA if len(d) == 2 and isinstance(d[1], (int, float))]
    if not data:
        print("※ DATA が空です。card_CAm_measure_sheet.txt の実測Hzを DATA に入れて再実行してください。")
        print("  比較用に較正コーム5点でフィットした現行値を表示します:")
        data = COMB5
        tag = "較正コーム5点(現行)"
    else:
        tag = "手元C/Amカード実測(%d点)" % len(data)
    A, e, rms, rows = fit(data)
    print("=== %s フィット: f = A/(L+e) ===" % tag)
    print("  A = %.1f   e = %.3f   RMS = %.1f cent" % (A, e, rms))
    print("  管長 | 実測Hz | 予測Hz | 誤差cent")
    for L, f, p, c in rows:
        print("  %5.1f | %6.0f | %6.1f | %+5.1f" % (L, f, p, c))
    # 基準窓 G6〜F#7 の12ピッチクラス管長（平均律）
    A4 = 440.0
    names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    # G6..F#7 の窓: G,G#,A,A#,B→oct6, C,C#,D,D#,E,F,F#→oct7
    print("\n=== 基準窓 G6〜F#7 の管長（A=%.0f, e=%.2f）===" % (A, e))
    for nm in ['G', 'G#', 'A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#']:
        octv = 6 if names.index(nm) >= names.index('G') else 7
        midi = 12 * (octv + 1) + names.index(nm)
        freq = A4 * 2 ** ((midi - 69) / 12.0)
        print("  %-3s%d  %6.1fHz  L=%.1fmm" % (nm, octv, freq, length_for(freq, A, e)))
