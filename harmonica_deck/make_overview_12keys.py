"""12調のカードを一覧にした overview_12keys.png を作る。

向きは chord_map・早見表とそろえてある。カードを窓が上(z+)・吹き込み口が手前になるよう
置いて上から見た姿で、左から順に位置1〜8になる。

以前の版は同じ図を90度倒して描いていた。鏡像ではないので誤りではないが、他の図と向きが
違うと読み手が突き合わせられない。図どうしで向きが食い違っていたことが、そもそも左右の
取り違えを生んだ原因だったので、すべて同じ向きに統一する。

  python3 harmonica_deck/make_overview_12keys.py
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import make_chordika_mini10 as CK

JP_FONT = "/System/Library/Fonts/Hiragino Sans GB.ttc"
CARD_FACE = "#f2f3f5"
CARD_EDGE = "#9aa3ad"
PIPE_FACE = "#cfe0f2"
PIPE_EDGE = "#4a79b8"
TONIC = "#c0392b"


def card_axes(ax, root_pc, label, fp, fpb):
    chain = CK.chain_pitchclasses(root_pc)
    midis = [CK.LOW_MIDI + ((pc - CK.LOW_MIDI) % 12) for pc in chain]
    lens = [CK._len_of(m) for m in midis]
    tonic = CK.DEGREES.index(1)

    import trimesh
    W = 7.0                      # パイプ幅（BASE の実測に合わせた固定値）
    step = W - CK.OVER
    yshift = (CK.CY - (step * 7 + W)) / 2.0
    cen = [i * step + yshift + W / 2.0 for i in range(8)]

    # 画面 = 実物を上から見た姿。sx(y)=CY-y で y小が右へ、sy(x)=x で吹き込み口が下。
    def sx(y):
        return CK.CY - y

    ax.add_patch(FancyBboxPatch((0.0, 0.0), CK.CY, CK.CX,
                                boxstyle="round,pad=0,rounding_size=2.0",
                                facecolor=CARD_FACE, edgecolor=CARD_EDGE, linewidth=1.1))
    for i, L in enumerate(lens):
        x = sx(cen[i]) - W / 2.0
        ax.add_patch(Rectangle((x, 0.0), W, L, facecolor=PIPE_FACE,
                               edgecolor=PIPE_EDGE, linewidth=0.8))
        if i == tonic:
            # ＊は棒の中に置く。棒の上に出すと、長い管の調で調名の帯とぶつかる。
            ax.text(sx(cen[i]), L - 5.0, "＊", ha="center", va="top",
                    fontsize=12, color=TONIC, fontproperties=fpb)
    ax.add_patch(Circle((sx(CK.CY - 6.0), CK.CX - 6.0), 3.0,
                        facecolor="white", edgecolor=TONIC, linewidth=1.0))
    ax.text(CK.CY / 2.0 + 4, CK.CX - 7.0, label, ha="center", va="center",
            fontsize=11, color="#333", fontproperties=fpb)
    ax.set_xlim(-1, CK.CY + 1)
    ax.set_ylim(-2, CK.CX + 2)
    ax.set_aspect("equal")
    ax.axis("off")


def main():
    CK.calib_from_file()
    fp = fm.FontProperties(fname=JP_FONT)
    fpb = fm.FontProperties(fname=JP_FONT, weight="bold")
    fig, axes = plt.subplots(2, 6, figsize=(15.0, 7.2), dpi=110)
    for ax, (root_pc, label) in zip(axes.ravel(), CK.KEYS):
        card_axes(ax, root_pc, label, fp, fpb)
    fig.suptitle("Chordika 12調。カードを持ち替えるだけで、同じ手の動きがそのまま移調になる"
                 "（窓を上・吹き込み口を手前にして見た姿／＊＝主音）",
                 fontsize=14, y=0.975, fontproperties=fpb)
    fig.tight_layout(rect=[0, 0, 1, 0.945])
    out = os.path.join(HERE, "overview_12keys.png")
    fig.savefig(out, dpi=110)
    plt.close(fig)
    print("wrote %s" % out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
