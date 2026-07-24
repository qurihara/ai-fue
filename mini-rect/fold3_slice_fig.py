"""fold3 の内部エア連結を目視確認するための断面図。
管中心 z=3.5 の水平断面（xy平面）を格子状にサンプリングし、材料=黒/空洞=白で描く。
bore1（窓側+y=上）と bore2（返し脚-y=下）が U字（右端フット）で一続きになっているかを確認する。"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from make_fold_rect import fold3

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, os.pardir, "out")

fig, axes = plt.subplots(3, 1, figsize=(9, 8))
for ax, Lp in zip(axes, (30, 40, 50)):
    fd = fold3(Lp)
    b = fd.bounds
    xs = np.arange(b[0][0] + 0.1, b[1][0], 0.25)
    ys = np.arange(b[0][1] + 0.1, b[1][1], 0.25)
    z = 3.5
    pts = np.array([[x, y, z] for y in ys for x in xs])
    inside = fd.contains(pts).reshape(len(ys), len(xs))
    ax.imshow(inside, origin="lower", cmap="gray_r",
              extent=[xs[0], xs[-1], ys[0], ys[-1]], aspect="equal", interpolation="nearest")
    ax.set_title("fold3 Lp=%d  z=3.5 断面（黒=材料 / 白=空洞）" % Lp, fontsize=10)
    ax.axvline(18, color="red", lw=0.8, ls="--")  # 頭部/フットの境界 x=18
    ax.set_xlabel("x (管軸)")
    ax.set_ylabel("y (幅: 上=窓側bore1 / 下=返しbore2)")

fig.suptitle("fold3 断面: bore1(上) → U字(右端) → bore2(下) が一続きか", fontsize=12)
fig.tight_layout()
p = os.path.join(OUT, "fold3_bore_zslice.png")
fig.savefig(p, dpi=110)
print("wrote", p)
