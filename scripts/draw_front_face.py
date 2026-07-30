"""箱を「外から」吸込口の側に立って見た顔を描き、吹く順番を番号で示す。

視線は +x 方向（箱の外から中へ）、上は +z である。このとき右手は -y になるので、
図の横軸は y を[* 反転]して描く。こうすると図がそのまま実物を正面から見た絵になる。
"""
import sys
import numpy as np
import trimesh
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

src, out = sys.argv[1], sys.argv[2]
notes = sys.argv[3].split(",") if len(sys.argv) > 3 else []
JP = "Hiragino Sans"

mesh = trimesh.util.concatenate(list(trimesh.load(src).geometry.values()))
x0 = mesh.bounds[0][0]
v = mesh.vertices
sel = v[(v[:, 0] > x0 + 0.02) & (v[:, 0] < x0 + 1.2)]

# 吸込口（z が笛の高さにある点）を y でまとめて、8つの群に分ける
bore = sel[(sel[:, 2] > 0.5) & (sel[:, 2] < 7.0)]
# 笛どうしは0.3mmだけ重なるので、山と山のあいだに隙間が無い。
# 帯の端から端までを本数で等分して、それぞれの中心を出す。
y_lo, y_hi = float(bore[:, 1].min()), float(bore[:, 1].max())
n = len(notes) if notes else 8
centers = [y_lo + (i + 0.5) * (y_hi - y_lo) / n for i in range(n)]
print("笛の帯 y %.1f〜%.1f を %d 等分。中心 %s"
      % (y_lo, y_hi, n, np.round(centers, 1)))

fig, ax = plt.subplots(figsize=(11, 6))
ax.scatter(sel[:, 1], sel[:, 2], s=4, c="#c33")
for i, yc in enumerate(centers):
    ax.annotate("%d\n%s" % (i + 1, notes[i] if i < len(notes) else ""),
                (yc, 7.5), ha="center", va="bottom", fontsize=11,
                color="#06c", fontname=JP)
if centers:
    ax.annotate("", xy=(centers[-1], 14.0), xytext=(centers[0], 14.0),
                arrowprops=dict(arrowstyle="->", color="#06c", lw=2))
    ax.text((centers[0] + centers[-1]) / 2, 14.8, "この向きに吹く",
            ha="center", color="#06c", fontsize=12, fontname=JP)

ax.set_xlim(sel[:, 1].max() + 3, sel[:, 1].min() - 3)      # ← 左右を反転して外から見た絵にする
ax.set_ylim(-3, mesh.bounds[1][2] + 3)
ax.set_aspect("equal")
ax.set_xlabel("実物を正面から見た左右", fontname=JP)
ax.set_ylabel("高さ [mm]", fontname=JP)
ax.set_title("箱（2-of-3の断片1）を吸込口の側から見た顔と、吹く順番", fontname=JP)
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(out, dpi=130)
print("書き出した", out)
