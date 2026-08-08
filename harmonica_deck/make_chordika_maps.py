"""Chordika v1.1（mini10厚壁パイプ・窓 G#6〜G7）の全12調 対応表 PNG を生成する。

旧 make_chord_maps.py は薄壁の旧ジオメトリ（deck.py + halfcut.py）を参照していたため、
音名も管長も現行のカードと合わなくなった。本ファイルはカードの生成器そのもの
（make_chordika_mini10）から並び・音名・管長を取るので、STLと必ず一致する。

図の構成は旧版を踏襲する。
  上段: 8本のパイプを棒で表す（棒の高さ＝管長＝音高、下に音名と位置番号）。
  下段: 隣り合う3本を吹くとどの和音になるかを6行で色分けする（左の組から順に上の行へ）。

並びは実物を見たままにしてある。カードを窓が上・吹き込み口が手前に置いたとき、モデルの
y が小さい側が右に来るため、生成器の索引順にそのまま描くと左右が逆の図になる。
出力は harmonica_deck/chord_map_<調>.png。
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import Rectangle

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import make_chordika_mini10 as CK

JP_FONT = "/System/Library/Fonts/Hiragino Sans GB.ttc"

# 6行の色（上から ii IV vi I iii V）。旧 chord_map の配色を引き継ぐ。
ROW_COLORS = ["#63c2a6", "#f2864b", "#7b8fc4", "#d982c0", "#9ec54a", "#f5c518"]
ROW_LABELS = ["ii", "IV", "vi", "I", "iii", "V"]
BAR_FACE = "#cfe0f2"
BAR_EDGE = "#3a3a3a"
TONIC_FACE = "#f7dede"
TONIC_EDGE = "#c0392b"


def _note_name(midi):
    return "%s%d" % (CK.NAMES[midi % 12], midi // 12 - 1)


def card_data(root_pc):
    """カード1枚ぶんの (音名リスト, 管長リスト, MIDIリスト, 隣接3本の和音リスト)。"""
    chain = CK.chain_pitchclasses(root_pc)
    midis = [CK.LOW_MIDI + ((pc - CK.LOW_MIDI) % 12) for pc in chain]
    lens = [CK._len_of(m) for m in midis]
    notes = [_note_name(m) for m in midis]
    triads = [(i, notes[i:i + 3], q) for i, (_w, q) in enumerate(CK.triads_of(chain))]
    return notes, lens, midis, triads


def to_display(notes, lens, triads, n):
    """モデルの並びを、実物を見たときの左→右に直す。

    カードを窓が上(z+)・吹き込み口が手前になるように置くと、モデルの y が小さい側が
    右に来る。生成器の索引0から順に左へ描くと、実物と左右が逆の図になる（2026-08-04に
    実機と照合して判明）。図は見たままの左→右で並べ、位置番号もその順に振る。
    """
    d_notes = notes[::-1]
    d_lens = lens[::-1]
    rows = []
    for start, w, q in triads:                 # start はモデル索引
        rows.append((n - 3 - start, w[::-1], q, ROW_LABELS[start], ROW_COLORS[start]))
    rows.sort(key=lambda r: r[0])              # 左の組から順に上の行へ
    return d_notes, d_lens, rows


def make_map(root_pc, label, outdir=HERE):
    CK.calib_from_file()
    notes, lens, midis, triads = card_data(root_pc)
    n = len(notes)
    notes, lens, rows = to_display(notes, lens, triads, n)
    tonic_idx = n - 1 - CK.DEGREES.index(1)
    # 波ダッシュ（〜）は Hiragino Sans GB に無いので、図中では en dash を使う
    win = "%s–%s" % (_note_name(CK.LOW_MIDI), _note_name(CK.LOW_MIDI + 11))
    fp = fm.FontProperties(fname=JP_FONT)
    fpb = fm.FontProperties(fname=JP_FONT, weight="bold")

    fig = plt.figure(figsize=(13.5, 12.0))
    gs = fig.add_gridspec(2, 1, height_ratios=[1.05, 1.55], hspace=0.16,
                          left=0.06, right=0.97, top=0.89, bottom=0.04)

    # ---- 上段: パイプの棒 ----
    ax = fig.add_subplot(gs[0])
    for x, (note, L) in enumerate(zip(notes, lens)):
        is_tonic = (x == tonic_idx)
        ax.add_patch(Rectangle((x - 0.4, 0), 0.8, L,
                               facecolor=(TONIC_FACE if is_tonic else BAR_FACE),
                               edgecolor=(TONIC_EDGE if is_tonic else BAR_EDGE),
                               linewidth=(2.4 if is_tonic else 1.4)))
        ax.text(x, L + 2.0, "%.1f" % L, ha="center", va="bottom",
                fontsize=11, color="#555", fontproperties=fp)
        ax.text(x, -6.0, note + ("  ＊" if is_tonic else ""), ha="center", va="top",
                fontsize=15, fontproperties=fpb)
        ax.text(x, -13.5, "位置 %d" % (x + 1), ha="center", va="top",
                fontsize=10, color="#777", fontproperties=fp)
    ax.set_xlim(-0.9, n - 0.2)
    ax.set_ylim(-20, max(lens) * 1.16)
    ax.axis("off")
    ax.set_title("%s のカード ― 8本の半割パイプ（棒の高さ＝管長mm＝音高／＊＝主音）" % label,
                 fontsize=16, pad=20, fontproperties=fp)
    fig.suptitle("Chordika %s ― 隣り合う3本を吹くと何の和音になるか（6和音 I IV V ii iii vi）／音域 %s"
                 % (label, win), fontsize=18, y=0.955, fontproperties=fpb)

    # ---- 下段: 隣接3本→和音 ----
    ax2 = fig.add_subplot(gs[1])
    ax2.text(-0.02, 6.55, "隣り合う3本を同時に吹くと、その和音が鳴る（位置番号は上の図と同じ）",
             fontsize=15, ha="left", va="bottom", fontproperties=fpb,
             transform=ax2.get_yaxis_transform())
    cell, gap, x0 = 1.0, 0.12, 1.2
    for row, (start, w, chord, deg, color) in enumerate(rows):
        y = len(rows) - 1 - row
        ax2.text(0.55, y + cell / 2, deg, ha="center", va="center",
                 fontsize=17, fontproperties=fpb)
        for c in range(n):
            cx = x0 + c * (cell + gap)
            on = start <= c <= start + 2
            ax2.add_patch(Rectangle((cx, y), cell, cell,
                                    facecolor=(color if on else "#eee"),
                                    edgecolor=(color if on else "#ddd"),
                                    linewidth=(2.0 if on else 1.0)))
            if on:
                ax2.text(cx + cell / 2, y + cell / 2, notes[c], ha="center",
                         va="center", fontsize=12, color="#222", fontproperties=fpb)
        tx = x0 + n * (cell + gap) + 0.5
        ax2.text(tx, y + cell / 2,
                 "位置 %d-%d-%d を吹く ： %s ＝ %s" %
                 (start + 1, start + 2, start + 3, " ".join(w), chord),
                 ha="left", va="center", fontsize=14, fontproperties=fp)
    ax2.set_xlim(0, x0 + n * (cell + gap) + 8.0)
    ax2.set_ylim(-0.4, len(rows) + 0.4)
    ax2.axis("off")

    out = os.path.join(outdir, "chord_map_%s.png" % CK._safe(label))
    fig.savefig(out, dpi=110)
    plt.close(fig)
    return out, notes, [round(L, 1) for L in lens], [r[2] for r in rows]


def main():
    CK.calib_from_file()
    print("Chordika v1.1 対応表（窓 %s〜%s / 較正 A=%.1f e=%.3f）" % (
        _note_name(CK.LOW_MIDI), _note_name(CK.LOW_MIDI + 11), CK.A, CK.E))
    for root_pc, label in CK.KEYS:
        out, notes, lens, chords = make_map(root_pc, label)
        print("[%-9s] %s" % (label, os.path.relpath(out, HERE)))
        print("    音名: %s" % " ".join(notes))
        print("    管長: %s" % " ".join("%.1f" % L for L in lens))
        print("    和音(左の組から順に): %s" % "  ".join(chords))


if __name__ == "__main__":
    main()
