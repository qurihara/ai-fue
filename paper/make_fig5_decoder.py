# -*- coding: utf-8 -*-
"""図5：復号ソフト（スマホWebアプリ）の画面。実際の復号結果を反映したダークUI風の図。
カード「2026724」の理想周波数を CipherFlute の復号ロジックにかけた結果（記号列 2,0,2,6,7,2,4）を示す。
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

for f in ["Hiragino Sans GB", "Hiragino Sans", "Arial Unicode MS", "IPAexGothic"]:
    try:
        plt.rcParams["font.family"] = f
        break
    except Exception:
        pass
plt.rcParams["axes.unicode_minus"] = False

BG = "#0f1523"; PANEL = "#1b2233"; ACC = "#6c7bff"; TX = "#e8ecf4"; SUB = "#9aa4bd"; OK = "#37d67a"

notes = ['C7', 'A#6', 'G#6', 'A#6', 'D7', 'D#7', 'A#6', 'C7']
def n2f(n):
    NAMES = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
    nm, oc = n[:-1], int(n[-1]); midi = 12*(oc+1)+NAMES.index(nm)
    return 440.0*2**((midi-69)/12.0)
freqs = [n2f(n) for n in notes]

fig = plt.figure(figsize=(6.2, 8.0), dpi=150)
fig.patch.set_facecolor(BG)
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 100); ax.set_ylim(0, 130); ax.axis("off")

def panel(x, y, w, h, color=PANEL):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.6,rounding_size=1.6",
                                fc=color, ec="#2a3350", lw=1))

# ヘッダ
ax.text(6, 124, "CipherFlute 復号", color=TX, fontsize=20, fontweight="bold")
ax.text(6, 119.5, "3Dプリントした笛の並びを先頭の基準笛から順に吹くと、音から秘密を復号します。マイクだけで動きます。",
        color=SUB, fontsize=8)

# マイク／スペクトル パネル
panel(6, 92, 88, 22)
ax.add_patch(FancyBboxPatch((10, 104), 16, 6, boxstyle="round,pad=0.3,rounding_size=1.0", fc=ACC, ec="none"))
ax.text(18, 107, "マイク開始", color="white", fontsize=9, ha="center", va="center", fontweight="bold")
ax.text(30, 107, "検出中… 8本すべて安定して検出できました。", color=OK, fontsize=8.5, va="center")
# スペクトル風バー（検出周波数を高さに）
fx = np.linspace(12, 90, 8)
fmin, fmax = min(freqs), max(freqs)
for x, fr, nn, i in zip(fx, freqs, notes, range(8)):
    hh = 3 + 9*(fr-fmin)/(fmax-fmin+1e-9)
    ax.add_patch(plt.Rectangle((x-3.6, 94), 7.2, hh, fc=ACC if i else OK, ec="none", alpha=0.9))
    ax.text(x, 94-1.4, nn, color=SUB, fontsize=6.5, ha="center", va="top")

# 検出した並び
ax.text(6, 88, "1. 順番に吹いて測る（押しながら吹く）", color=ACC, fontsize=11, fontweight="bold")
panel(6, 60, 88, 25)
ax.text(10, 81, "検出した並び（先頭＝基準笛）：", color=SUB, fontsize=8.5)
for i, (nn, fr) in enumerate(zip(notes, freqs)):
    col = i % 4; row = i // 4
    xx = 10 + col*21; yy = 75.5 - row*7
    tag = "★基準 " if i == 0 else "%d: " % i
    ax.add_patch(FancyBboxPatch((xx, yy-3.2), 19, 5.6, boxstyle="round,pad=0.2,rounding_size=0.8",
                                fc="#232c44", ec="none"))
    ax.text(xx+1.4, yy-0.4, "%s%s" % (tag, nn), color=(OK if i == 0 else TX), fontsize=8, va="center", fontweight="bold")
    ax.text(xx+1.4, yy-2.6, "%d Hz" % round(fr), color=SUB, fontsize=6.2, va="center")

# 復号して照合
ax.text(6, 55.5, "2. 復号して照合", color=ACC, fontsize=11, fontweight="bold")
panel(6, 24, 88, 28)
ax.add_patch(FancyBboxPatch((10, 45), 26, 5.5, boxstyle="round,pad=0.3,rounding_size=1.0", fc=ACC, ec="none"))
ax.text(23, 47.7, "この並びで復号", color="white", fontsize=9, ha="center", va="center", fontweight="bold")
ax.text(10, 40.5, "復号に成功しました。", color=OK, fontsize=9)
ax.text(10, 35.5, "復元した記号列：", color=SUB, fontsize=8.5)
ax.text(10, 31.5, "2, 0, 2, 6, 7, 2, 4", color=TX, fontsize=15, fontweight="bold", family="monospace")
ax.text(58, 31.5, "→  2026724", color=OK, fontsize=14, fontweight="bold", va="center")
ax.add_patch(FancyBboxPatch((10, 26), 84, 3.4, boxstyle="round,pad=0.2,rounding_size=0.8", fc="#173a26", ec=OK, lw=1))
ax.text(12, 27.7, "照合：SHA-256 が一致 — 認証成功", color=OK, fontsize=9, va="center", fontweight="bold")

# フッタ
ax.text(6, 20, "復号ロジックは Python版 fue/cipher_codec.py と一致。ネットワーク接続は不要（端末内で完結）。",
        color=SUB, fontsize=7.5)
ax.text(6, 16.5, "先頭の基準笛との比で全体のずれ（温度・息の強さ）を打ち消し、正しく読み取る。",
        color=SUB, fontsize=7.5)

os.makedirs("figs", exist_ok=True)
out = "figs/fig5_decoder.png"
fig.savefig(out, facecolor=BG, bbox_inches="tight", pad_inches=0.15)
print("wrote", out)
