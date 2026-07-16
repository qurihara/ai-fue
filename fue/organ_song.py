"""オルガンのデモ楽譜シート：和音で完結する短い曲（C major, C6〜C7の8笛）。

organ.punched_sheet を使って印刷可能な穴あきシートSTLと、楽譜図(どのステップでどの音)を出力する。
ポート対応：pipe_bank は notes を逆順に並べる（長管=低音を+xへ）ので、シートのポート番号 i は
rev[i]=notes[7-i] を鳴らす（C6→port7, D6→port6, …, B6→port1, C7→port0）。
実機で「音程が逆／時間が逆」に鳴ったら reverse_ports / reverse_time を True にして作り直せばよい。
"""
import os
import sys
import numpy as np
import trimesh

sys.path.insert(0, os.path.dirname(__file__))
import organ

OUT = os.path.join(os.path.dirname(__file__), os.pardir, "out")
NOTES = ["C6", "D6", "E6", "F6", "G6", "A6", "B6", "C7"]   # オルガンの8笛（低→高）

# 和音で完結する短い曲（C major）：ド-ミ-ソ-ラ-ソ …（上げて）ミ-ファ-ミ-レ（下げて戻り）→ ドミソ → ドミソド'
SONG = [
    {"C6"}, {"E6"}, {"G6"}, {"A6"}, {"G6"}, set(),
    {"E6"}, {"F6"}, {"E6"}, {"D6"}, set(),
    {"C6", "E6", "G6"}, {"C6", "E6", "G6", "C7"},
]


def _note_ports(notes=NOTES):
    rev = list(notes)[::-1]                      # pipe_bank と同じ逆順
    return {n: i for i, n in enumerate(rev)}


def build(song=SONG, reverse_ports=False, reverse_time=False, slot_len=6.0, step_y=None):
    n2p = _note_ports()

    def port(note):
        i = n2p[note]
        return (len(NOTES) - 1 - i) if reverse_ports else i

    score = [set(port(x) for x in step) for step in song]
    if reverse_time:
        score = score[::-1]
    sheet, info = organ.punched_sheet(score, n=len(NOTES), slot_len=slot_len, step_y=step_y)
    return sheet, info, score


def _render_score(song, path):
    """楽譜図：縦=時間(上→下で進行)、横=音名。穴のあるマスに●、和音は色を変える。"""
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(7, 6))
    order = NOTES                                 # 左→右で C6→C7（低→高）
    for t, step in enumerate(song):
        y = len(song) - 1 - t                     # 上を先頭に
        chord = len(step) >= 3
        for note in step:
            x = order.index(note)
            ax.scatter([x], [y], s=260, c=("#d1495b" if chord else "#3a6ea5"),
                       edgecolors="#222", zorder=3)
        if not step:
            ax.text(-0.9, y, "(休)", va="center", ha="right", fontsize=8, color="#888")
    ax.set_xticks(range(len(order))); ax.set_xticklabels(order)
    ax.set_yticks(range(len(song))); ax.set_yticklabels(["t%d" % (len(song) - 1 - i) for i in range(len(song))])
    ax.set_xlim(-1.5, len(order) - 0.5); ax.set_ylim(-0.5, len(song) - 0.5)
    ax.set_xlabel("pitch (low -> high)"); ax.set_title("organ song sheet (red = final chord)")
    ax.grid(True, alpha=0.25); plt.tight_layout(); plt.savefig(path, dpi=100); plt.close()


def main():
    os.makedirs(OUT, exist_ok=True)
    import sys as _s
    rp = "--reverse-ports" in _s.argv
    rt = "--reverse-time" in _s.argv
    sheet, info, score = build(reverse_ports=rp, reverse_time=rt)
    name = os.path.join(OUT, "organ_song_cadence.stl")
    sheet.export(name)
    n2p = _note_ports()
    print("オルガン デモ楽譜シート『和音で完結する短い曲』(C major):")
    print("  曲（上=先頭）:")
    for t, step in enumerate(SONG):
        label = "休符" if not step else " ".join(sorted(step, key=lambda x: NOTES.index(x)))
        ports = "" if not step else "  ports=" + str(sorted(_note_ports()[x] for x in step))
        print("    t%-2d: %-18s%s" % (t, label, ports))
    print("  音→ポート: " + ", ".join("%s=%d" % (n, n2p[n]) for n in NOTES))
    print("  シート外形%s watertight=%s ステップ%d 穴Ø%.0f 溝%.0fmm 送り%.0fmm/step" %
          (info["dims"], sheet.is_watertight, info["steps"], organ.SHEET_HOLE_R * 2, info["slot_len"], info["step_y"]))
    print("  reverse_ports=%s reverse_time=%s -> %s" % (rp, rt, name))
    _render_score(SONG, os.path.join(OUT, "organ_song_cadence_score.png"))
    print("  楽譜図 -> out/organ_song_cadence_score.png")


if __name__ == "__main__":
    main()
