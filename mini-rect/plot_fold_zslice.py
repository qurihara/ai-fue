"""fold2(旧・分断) と fold3(修正) のボア中心 z=3.5 水平断面を上下に並べて比較する図を作る。
黒=材料(壁)、白=ボア空洞/外側。conn_check の判定も各図タイトルに併記する。
出力: out/fold3_vs_fold2_zslice.png
実行: /Users/kurihara/Desktop/claude_work/mesh_venv/bin/python mini-rect/plot_fold_zslice.py
"""
import os
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(__file__)
sys.path.insert(0, HERE)
import make_fold_rect as M

Lp, pitch, z = 40, 0.1, 3.5


def occ_slice(fd):
    vg = fd.voxelized(pitch=pitch)
    occ = vg.matrix
    org = vg.transform[:3, 3]
    k = max(0, min(occ.shape[2] - 1, int(round((z - org[2]) / pitch))))
    ext = [org[0], org[0] + occ.shape[0] * pitch, org[1], org[1] + occ.shape[1] * pitch]
    return occ[:, :, k].T, ext


def main():
    fig, axes = plt.subplots(2, 1, figsize=(11, 6))
    for ax, fn, name in [(axes[0], M.fold2, "fold2 (OLD, severed)"),
                         (axes[1], M.fold3, "fold3 (FIXED)")]:
        fd = fn(Lp)
        conn = M.conn_check(fd)
        sl, ext = occ_slice(fd)
        ax.imshow(sl, origin="lower", extent=ext, cmap="gray_r", aspect="equal",
                  interpolation="nearest")
        ax.set_title("%s   Lp%d z=%.1f   conn=%s" % (name, Lp, z, conn))
        ax.set_xlabel("x (mm)")
        ax.set_ylabel("y (mm)")
        ax.grid(True, color="c", lw=0.3, alpha=0.5)
    plt.tight_layout()
    out = os.path.join(HERE, os.pardir, "out", "fold3_vs_fold2_zslice.png")
    plt.savefig(out, dpi=110)
    print("wrote", os.path.normpath(out))


if __name__ == "__main__":
    main()
