"""全12調のコード笛カード対応表(chord_map_*.png)を生成する。

既存の chord_map_C_Am.png と同じ体裁で、上段=8本の笛(棒の高さ=笛長=音高、ラベル=音名)、
下段=隣接3本を吹くとどの和音になるか(6行: V iii I vi IV ii)を色分けで示す。

並び順は deck.deck_chain(root) の逆順で描く(=物理カードと同じ左右の並び。C/Amなら D B G E C A F D)。
隣接3本の和音は描画順(逆順)の連続3セルで、行ラベルは全調共通で V iii I vi IV ii。
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrow

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, os.pardir, "fue"))
sys.path.insert(0, HERE)
import halfcut
import deck

# 6行の色(上から V iii I vi IV ii)。既存C/Am図の配色に寄せた。
ROW_COLORS = ["#63c2a6", "#f2864b", "#7b8fc4", "#d982c0", "#9ec54a", "#f5c518"]
# 全調共通(度数連鎖が固定)。物理カードの並び=deck_chain順のとき、隣接3本(pos1-2-3から)は上から ii IV vi I iii V。
ROW_LABELS = ["ii", "IV", "vi", "I", "iii", "V"]
BAR_FACE = "#cfe0f2"
BAR_EDGE = "#3a3a3a"


def make_map(root, label):
    chain = deck.deck_chain(root)
    draw = list(chain)                              # 物理カードと同じ左右の並び(deck_chain順)
    lens = [halfcut.length_for_note(n) for n in draw]
    # 隣接3本(描画順の連続3セル)の和音
    triads = []
    for i in range(len(draw) - 2):
        w = draw[i:i + 3]
        pcs = [n[:-1] for n in w]
        r, qual = deck._quality(pcs)
        triads.append((i, w, "%s %s" % (r, qual)))

    fig = plt.figure(figsize=(13.5, 12.0))
    gs = fig.add_gridspec(2, 1, height_ratios=[1.05, 1.55], hspace=0.16,
                          left=0.06, right=0.97, top=0.90, bottom=0.04)

    # ---- 上段: 笛の棒グラフ ----
    ax = fig.add_subplot(gs[0])
    n = len(draw)
    xs = range(n)
    for x, (note, L) in enumerate(zip(draw, lens)):
        ax.add_patch(Rectangle((x - 0.4, 0), 0.8, L, facecolor=BAR_FACE,
                               edgecolor=BAR_EDGE, linewidth=1.4))
        ax.text(x, L + 2.0, "%d" % round(L), ha="center", va="bottom",
                fontsize=11, color="#555")
        ax.text(x, -6.0, note, ha="center", va="top", fontsize=15, fontweight="bold")
        ax.text(x, -13.5, "pos %d" % (x + 1), ha="center", va="top",
                fontsize=10, color="#777")
    ax.annotate("mouthpieces all aligned here (x=0)\nyou blow this edge",
                xy=(-0.35, 3.0), xytext=(0.6, max(lens) * 0.36),
                fontsize=11, color="#555", ha="left", va="center",
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#ccc", alpha=0.85),
                arrowprops=dict(arrowstyle="->", color="#999", lw=1.4))
    ax.set_xlim(-0.9, n - 0.2)
    ax.set_ylim(-20, max(lens) * 1.16)
    ax.axis("off")
    ax.set_title("%s card — 8 half-cut pipes (bar height = length = pitch)"
                 % label, fontsize=16, pad=20)
    fig.suptitle("%s chord flute: which 3 pipes -> which chord (6 chords: I IV V ii iii vi)"
                 % label, fontsize=19, y=0.965)

    # ---- 下段: 隣接3本->和音 ----
    ax2 = fig.add_subplot(gs[1])
    ax2.text(-0.02, 6.55, "blow 3 ADJACENT pipes -> that chord  (positions match the card above)",
             fontsize=15, fontweight="bold", ha="left", va="bottom",
             transform=ax2.get_yaxis_transform())
    cell = 1.0
    gap = 0.12
    x0 = 1.2
    for row, (start, w, chord) in enumerate(triads):
        y = (len(triads) - 1 - row)              # 上が最初のトリオ
        color = ROW_COLORS[row]
        ax2.text(0.55, y + cell / 2, ROW_LABELS[row], ha="center", va="center",
                 fontsize=17, fontweight="bold")
        for c in range(n):
            cx = x0 + c * (cell + gap)
            on = start <= c <= start + 2
            ax2.add_patch(Rectangle((cx, y), cell, cell,
                                    facecolor=color if on else "#eee",
                                    edgecolor=(color if on else "#ddd"),
                                    linewidth=2.0 if on else 1.0))
            if on:
                ax2.text(cx + cell / 2, y + cell / 2, draw[c], ha="center",
                         va="center", fontsize=12, fontweight="bold", color="#222")
        tx = x0 + n * (cell + gap) + 0.5
        notes = " ".join(w)
        ax2.text(tx, y + cell / 2,
                 "blow pos %d-%d-%d :  %s  =  %s" %
                 (start + 1, start + 2, start + 3, notes, chord),
                 ha="left", va="center", fontsize=14)
    ax2.set_xlim(0, x0 + n * (cell + gap) + 7.5)
    ax2.set_ylim(-0.4, len(triads) + 0.4)
    ax2.axis("off")

    safe = label.replace(" ", "").replace("/", "_").replace("#", "s")
    out = os.path.join(HERE, "chord_map_%s.png" % safe)
    fig.savefig(out, dpi=110)
    plt.close(fig)
    return out, draw, [round(L) for L in lens], [(t[2]) for t in triads]


def main():
    for root, label in deck.KEYS:
        out, draw, lens, chords = make_map(root, label)
        print("[%s] -> %s" % (label, os.path.relpath(out, HERE)))
        print("    draw:", draw, "lens:", lens)
        print("    chords(V iii I vi IV ii):", chords)


if __name__ == "__main__":
    main()
