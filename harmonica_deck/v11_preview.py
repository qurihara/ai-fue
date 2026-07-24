"""Chordika v1.1 全12調のプレート層(z=0.3)をグリッド判定で一覧描画して目視QAする。
黒=材料 / 白=穴。外形・角丸R2・ストラップ穴・主音＊・調性ステンシル・触覚切り欠きの位置を確認。
切り欠きは調の半音番号(C=0..B=11)で y位置が上がっていくので、12枚並べると段々ずれるのが正しい。"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import trimesh

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, os.pardir, "out")

ORDER = ["C_Am", "G_Em", "D_Bm", "A_Fsm", "E_Csm", "B_Gsm",
         "Fs_Dsm", "Db_Bbm", "Ab_Fm", "Eb_Cm", "Bb_Gm", "F_Dm"]

fig, axes = plt.subplots(12, 1, figsize=(11, 16))
z = 0.3
xs = np.arange(0.3, 85.6, 0.4)
ys = np.arange(0.3, 53.98, 0.4)
gx, gy = np.meshgrid(xs, ys)
pts = np.column_stack([gx.ravel(), gy.ravel(), np.full(gx.size, z)])
for ax, key in zip(axes, ORDER):
    f = os.path.join(OUT, "chordika_v11_%s.stl" % key)
    m = trimesh.load(f)
    inside = m.contains(pts).reshape(gy.shape)
    ax.imshow(inside, origin="lower", cmap="gray_r",
              extent=[xs[0], xs[-1], ys[0], ys[-1]], aspect="equal", interpolation="nearest")
    ax.set_ylabel(key.replace("_", "/"), fontsize=8, rotation=0, ha="right", va="center")
    ax.set_xticks([]); ax.set_yticks([])
fig.suptitle("Chordika v1.1  plate layer (z=0.3)  black=material white=hole\n"
             "left edge x=0=吸込口 / right band=key stencil + tonic * / top-right=strap hole / bottom edge notch marches with key",
             fontsize=11)
fig.tight_layout()
p = os.path.join(OUT, "chordika_v11_qa.png")
fig.savefig(p, dpi=100)
print("wrote", p)
