"""Chordika デッキ同梱用のチートシート（コード進行早見表）を日本語版・英語版で生成する。

全カード共通の並び（足側から ii IV vi I iii V ＝ 3度連鎖の窓）を1枚に図示し、
主要三和音と平行短調の隣接、定番のコード進行、12調で運指共通であることを伝える。
C/Am を具体例に使う（他調は動きが同一で鳴る音だけ移調）。
"""
import os
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import FancyBboxPatch, Rectangle

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import make_chordika_mini10 as CK   # 音域と管長は生成器から取り、カードと必ず一致させる


def window_text(lang):
    """カードの音域（窓）と管長域の一文。生成器の LOW_MIDI・較正から作る。"""
    CK.calib_from_file()
    lo, hi = CK.LOW_MIDI, CK.LOW_MIDI + 11
    name = lambda m: "%s%d" % (CK.NAMES[m % 12], m // 12 - 1)
    # 波ダッシュ（〜）は Hiragino Sans GB に無いので en dash を使う
    if lang == "ja":
        return "音域 %s–%s（管長は約%.0fmmから%.0fmm）。全12枚が同じ音域に収まる。" % (
            name(lo), name(hi), CK._len_of(hi), CK._len_of(lo))
    return "Range %s–%s (pipe length approx. %.0f–%.0f mm). All 12 cards share this range." % (
        name(lo), name(hi), CK._len_of(hi), CK._len_of(lo))

# 日本語対応フォント（macOS）。英語版でも同じで問題なく出る。
JP_FONT = "/System/Library/Fonts/Hiragino Sans GB.ttc"
EN_FONT = "/Library/Fonts/Arial Unicode.ttf"

# 実物を見たままの左→右に並べる。カードを窓が上・吹き込み口が手前に置くと、この順に鳴る。
# 色は chord_map と同じで、和音の機能ごとに固定してある（並べ替えても色は付いて回る）。
COLORS = ["#f5c518", "#9ec54a", "#d982c0", "#7b8fc4", "#f2864b", "#63c2a6"]
DEGREES = ["V", "iii", "I", "vi", "IV", "ii"]
CAM = ["G", "Em", "C", "Am", "F", "Dm"]   # C/Am での実際の和音
POS = [1, 2, 3, 4, 5, 6]                  # その和音が始まる位置（左から数える）

# 定番進行： (名前, 度数リスト)  位置番号は DEGREES.index+1、C/Am和音は CAM で引く
PROG = [
    ("royal",   ["I", "IV", "V"]),
    ("pop",     ["I", "V", "vi", "IV"]),
    ("fifties", ["I", "vi", "IV", "V"]),
    ("circle",  ["I", "vi", "ii", "V"]),
    ("jazz",    ["ii", "V", "I"]),
    ("sixfour", ["vi", "IV", "I", "V"]),
]

TXT = {
    "ja": {
        "title": "Chordika ― コード進行 早見表",
        "sub": "どのカードも並びは同じ。C / Am を例にすると：",
        "layout_h": "隣り合う3本ずつを吹くと、左から順にこの6和音（＊＝主音トニック I）",
        "adj_h": "主要三和音と平行短調が隣どうし（スライド1つで行き来）",
        "adj": ["C(I) ↔ Am(vi)", "F(IV) ↔ Dm(ii)", "G(V) ↔ Em(iii)"],
        "prog_h": "定番のコード進行（位置番号と C/Am の和音）",
        "prog_names": {
            "royal": "王道進行 I–IV–V",
            "pop": "ポップ進行 I–V–vi–IV",
            "fifties": "50年代進行 I–vi–IV–V",
            "circle": "循環進行 I–vi–ii–V",
            "jazz": "ジャズ終止 ii–V–I",
            "sixfour": "vi–IV–I–V",
        },
        "foot_h": "12枚で全調",
        "foot": "位置と機能は全カード共通。カードを持ち替えるだけで、同じ手の動きのまま12調どれでも弾ける。",
        "lim_h": "できないこと",
        "lim": "vii°(減三和音)は無し。平行短調は自然的短音階の範囲(i・iv・v)。ii–V は位置1と6で最も離れる。",
        "poslabel": "位置",
    },
    "en": {
        "title": "Chordika — Chord Progression Cheat Sheet",
        "sub": "Every card has the same layout. Example in C / Am:",
        "layout_h": "Blow any 3 adjacent pipes — left to right, these 6 chords (＊ = tonic I)",
        "adj_h": "Each primary triad sits next to its relative minor (one slide apart)",
        "adj": ["C(I) ↔ Am(vi)", "F(IV) ↔ Dm(ii)", "G(V) ↔ Em(iii)"],
        "prog_h": "Common progressions (position numbers and C/Am chords)",
        "prog_names": {
            "royal": "I–IV–V",
            "pop": "Pop  I–V–vi–IV",
            "fifties": "50s  I–vi–IV–V",
            "circle": "Circle  I–vi–ii–V",
            "jazz": "Jazz cadence  ii–V–I",
            "sixfour": "vi–IV–I–V",
        },
        "foot_h": "All 12 keys",
        "foot": "Position and function are identical on every card. Swap the card and the same hand motion plays any of the 12 keys.",
        "lim_h": "Limits",
        "lim": "No vii° (diminished). Parallel minor stays natural-minor (i, iv, v). ii–V is the widest reach (pos 1 to 6).",
        "poslabel": "pos",
    },
}


def deg_to_pos(d):
    return DEGREES.index(d) + 1


def deg_to_cam(d):
    return CAM[DEGREES.index(d)]


def render(lang, out_path):
    t = TXT[lang]
    fp = fm.FontProperties(fname=(JP_FONT if lang == "ja" else EN_FONT))
    fp_bold = fm.FontProperties(fname=JP_FONT, weight="bold") if lang == "ja" \
        else fm.FontProperties(fname=EN_FONT, weight="bold")

    fig = plt.figure(figsize=(8.27, 11.69), dpi=200)  # A4 縦
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 100); ax.set_ylim(0, 140)
    ax.axis("off")

    def text(x, y, s, size, bold=False, ha="left", va="baseline", color="#222"):
        ax.text(x, y, s, fontsize=size, ha=ha, va=va, color=color,
                fontproperties=(fp_bold if bold else fp))

    # タイトル
    text(50, 134, t["title"], 20, bold=True, ha="center")
    text(50, 130.4, t["sub"], 12, ha="center", color="#555")
    text(50, 127.4, window_text(lang), 10.5, ha="center", color="#777")

    # --- 6和音の並び（横帯） ---
    y0 = 116; bw = 13.5; gap = 1.4; x_start = 8.5
    text(8.5, 124, t["layout_h"], 12.5, bold=True)
    for i in range(6):
        x = x_start + i * (bw + gap)
        is_tonic = DEGREES[i] == "I"
        ax.add_patch(FancyBboxPatch((x, y0), bw, 6.4,
                     boxstyle="round,pad=0.15,rounding_size=0.8",
                     linewidth=(2.2 if is_tonic else 0.8),
                     edgecolor=("#c0392b" if is_tonic else "#888"),
                     facecolor=COLORS[i]))
        deg = DEGREES[i] + ("  ＊" if is_tonic else "")
        text(x + bw / 2, y0 + 3.9, deg, 15, bold=True, ha="center", va="center", color="#1a1a1a")
        text(x + bw / 2, y0 + 1.4, CAM[i], 12.5, ha="center", va="center", color="#1a1a1a")
        text(x + bw / 2, y0 - 1.6, "%s %d" % (t["poslabel"], POS[i]), 9.5, ha="center", color="#666")
    # --- 平行短調の隣接 ---
    ya = 102
    text(8.5, ya, t["adj_h"], 12.5, bold=True)
    fp_latin = fm.FontProperties(fname=EN_FONT)  # ↔ を含む記号はラテン用フォントで確実に出す
    for i, s in enumerate(t["adj"]):
        ax.text(12 + i * 30, ya - 4.5, s, fontsize=12.5, ha="left", va="baseline",
                color="#222", fontproperties=fp_latin)

    # --- 定番進行 ---
    yp = 90
    text(8.5, yp, t["prog_h"], 12.5, bold=True)
    row_h = 8.6
    for r, (key, degs) in enumerate(PROG):
        yr = yp - 4.5 - r * row_h
        # 帯
        ax.add_patch(Rectangle((8, yr - 5.0), 84, row_h - 0.8,
                     facecolor=("#f4f4f4" if r % 2 else "#eceff3"), edgecolor="none"))
        text(10, yr - 1.2, t["prog_names"][key], 12.5, bold=True)
        # チップ列（位置番号＋和音）
        cx = 10; cy = yr - 4.2
        for j, d in enumerate(degs):
            col = COLORS[DEGREES.index(d)]
            chip_w = 11.5
            ax.add_patch(FancyBboxPatch((cx, cy - 1.6), chip_w, 3.4,
                         boxstyle="round,pad=0.1,rounding_size=0.5",
                         linewidth=0.6, edgecolor="#999", facecolor=col))
            text(cx + chip_w / 2, cy + 0.1, "%s  %d" % (deg_to_cam(d), deg_to_pos(d)),
                 10.5, ha="center", va="center", color="#1a1a1a")
            cx += chip_w + 1.2
            if j < len(degs) - 1:
                text(cx - 0.4, cy + 0.1, "→", 11, ha="center", va="center", color="#444")
                cx += 3.2

    # --- 12調共通 ---
    import textwrap
    yf = 31
    foot_lines = textwrap.fill(t["foot"], width=(42 if lang == "ja" else 74)).split("\n")
    box_h = 6.5 + 3.6 * len(foot_lines)
    ax.add_patch(FancyBboxPatch((8, yf + 1.5 - box_h), 84, box_h,
                 boxstyle="round,pad=0.2,rounding_size=1.0",
                 linewidth=1.0, edgecolor="#5a7", facecolor="#eaf6ef"))
    text(11, yf - 1.6, t["foot_h"], 12.5, bold=True, color="#2c6")
    for k, line in enumerate(foot_lines):
        text(11, yf - 5.6 - k * 3.6, line, 11, color="#234")

    # --- 限界 ---
    yl = 13.5
    text(8.5, yl, t["lim_h"], 11.5, bold=True, color="#a33")
    # 折り返し
    import textwrap
    wrapped = textwrap.fill(t["lim"], width=(46 if lang == "ja" else 78))
    for k, line in enumerate(wrapped.split("\n")):
        text(8.5, yl - 4 - k * 3.6, line, 10.5, color="#555")

    fig.savefig(out_path, dpi=200)
    plt.close(fig)
    print("wrote", out_path)


if __name__ == "__main__":
    render("ja", os.path.join(HERE, "cheatsheet_ja.png"))
    render("en", os.path.join(HERE, "cheatsheet_en.png"))
