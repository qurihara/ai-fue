# -*- coding: utf-8 -*-
"""論文v1.1用の図5枚を paper/figs/ に生成する。
実行: mesh_venv の python で（trimesh + matplotlib が必要）。
"""
import os
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["font.family"] = "Hiragino Sans"
matplotlib.rcParams["axes.unicode_minus"] = False
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import trimesh

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "paper", "figs")
os.makedirs(OUT, exist_ok=True)


def render_mesh(ax, mesh, elev, azim, face="#9db8dc", edge="#3a4a63"):
    ax.add_collection3d(Poly3DCollection(
        mesh.triangles, alpha=0.9, facecolor=face, edgecolor=edge, linewidths=0.15))
    b = mesh.bounds
    c = (b[0] + b[1]) / 2
    r = (b[1] - b[0]).max() / 2 * 1.05
    ax.set_xlim(c[0]-r, c[0]+r); ax.set_ylim(c[1]-r, c[1]+r); ax.set_zlim(c[2]-r, c[2]+r)
    ax.set_box_aspect((1, 1, 1))
    ax.view_init(elev=elev, azim=azim)
    ax.set_axis_off()


# ---------- 図1 全体の流れ ----------
def fig1():
    fig, ax = plt.subplots(figsize=(6.4, 2.1))
    ax.set_xlim(0, 100); ax.set_ylim(0, 26); ax.axis("off")
    boxes = [
        (1,  "日用品に見える\n笛入りの物体", "#e8f0fe"),
        (21, "息で吹く\n（電源不要）", "#e8f0fe"),
        (41, "スマートフォンで\n録音・周波数分析", "#fef7e0"),
        (61, "音の高さの列を\n数字列に戻す", "#fef7e0"),
        (81, "断片を集めて\n秘密を復元", "#e6f4ea"),
    ]
    for x, t, c in boxes:
        ax.add_patch(plt.Rectangle((x, 6), 17, 14, fc=c, ec="#555", lw=1))
        ax.text(x+8.5, 13, t, ha="center", va="center", fontsize=8.5)
    for x in (18.3, 38.3, 58.3, 78.3):
        ax.annotate("", xy=(x+2.6, 13), xytext=(x, 13),
                    arrowprops=dict(arrowstyle="-|>", color="#555", lw=1.4))
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig1_overview.png"), dpi=220)
    plt.close(fig)


# ---------- 図2 実験に使った笛の板（STL） ----------
def fig2():
    m = trimesh.load(os.path.join(ROOT, "out", "cipher_test_plate.stl"))
    fig = plt.figure(figsize=(6.4, 2.9))
    ax1 = fig.add_subplot(121, projection="3d")
    render_mesh(ax1, m, elev=28, azim=-62)
    ax1.set_title("斜めから見た様子", fontsize=9, pad=0)
    ax2 = fig.add_subplot(122, projection="3d")
    render_mesh(ax2, m, elev=88, azim=-90)
    ax2.set_title("真上から見た様子（吹き込み口は左）", fontsize=9, pad=0)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig2_plate.png"), dpi=220)
    plt.close(fig)


# ---------- 図3 音の高さの刻みと基準笛 ----------
def fig3():
    notes = ["F6", "F#6", "G6", "G#6", "A6", "A#6", "B6", "C7", "C#7", "D7", "D#7"]
    freqs = [1396.9, 1480.0, 1568.0, 1661.2, 1760.0, 1864.7, 1975.5, 2093.0, 2217.5, 2349.3, 2489.0]
    fig, ax = plt.subplots(figsize=(6.4, 2.6))
    ax.set_xscale("log")
    for i, (n, f) in enumerate(zip(notes, freqs)):
        col = "#d93025" if n == "A6" else "#3a6bc9"
        ax.axvline(f, ymin=0.55, ymax=0.95, color=col, lw=2.4 if n == "A6" else 1.4)
        ax.text(f, 1.02, n, ha="center", va="bottom", fontsize=7.5,
                color=col, transform=ax.get_xaxis_transform())
    shift = 1.03  # 全体が+3%ずれた場合
    for f in freqs:
        ax.axvline(f*shift, ymin=0.08, ymax=0.48, color="#999", lw=1.2)
    ax.text(1385, 0.80, "設計どおりの音の高さ（11の置き場）", fontsize=8,
            transform=ax.get_xaxis_transform(), ha="left")
    ax.text(1385, 0.33, "気温などで全体が同じ割合でずれた場合（+3%の例）", fontsize=8,
            color="#666", transform=ax.get_xaxis_transform(), ha="left")
    ax.annotate("赤=基準笛(A6)。各笛の値は基準笛との比で読むため、\n全体が同じ割合でずれても読み取り結果は変わらない",
                xy=(1810, 0.55), xytext=(1980, 0.16), fontsize=8,
                xycoords=ax.get_xaxis_transform(), textcoords=ax.get_xaxis_transform(),
                arrowprops=dict(arrowstyle="->", color="#d93025"))
    ax.set_xlim(1330, 2760)
    ax.set_xticks([1400, 1600, 1800, 2000, 2200, 2400, 2600])
    ax.set_xticklabels(["1400", "1600", "1800", "2000", "2200", "2400", "2600"], fontsize=8)
    ax.set_yticks([])
    ax.set_xlabel("周波数 [Hz]（対数目盛）", fontsize=9)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig3_slots.png"), dpi=220)
    plt.close(fig)


# ---------- 図4 予備測定（実測） ----------
def fig4():
    # 実験プレート（2026-07-19 手順1・9本）
    plate = [("F6", 5), ("G6", 2), ("A6", 4), ("C7", 1), ("D7", -4),
             ("G#6", 2), ("A6 ", -2), ("A#6", 0), ("B6", 4)]
    # D6-F#7の17本笛（2026-07-21・きれいに読めた11本）
    comb = [("G#6", 9), ("A6", 10), ("A#6", 10), ("B6", -22), ("C7", -6),
            ("C#7", 3), ("D7", -8), ("D#7", -11), ("E7", 144), ("F7", 140), ("F#7", 138)]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.6, 2.6),
                                   gridspec_kw={"width_ratios": [9, 11]})
    for ax, data, title in ((ax1, plate, "笛の板（9本・7月19日）"),
                            (ax2, comb, "17本の笛の列（7月21日）")):
        xs = np.arange(len(data))
        vals = [v for _, v in data]
        cols = ["#3a6bc9" if abs(v) <= 50 else "#d93025" for v in vals]
        ax.bar(xs, vals, color=cols, width=0.62)
        ax.axhspan(-50, 50, color="#3a6bc9", alpha=0.08)
        ax.axhline(0, color="#888", lw=0.8)
        ax.set_xticks(xs)
        ax.set_xticklabels([n for n, _ in data], fontsize=7, rotation=45)
        ax.set_title(title, fontsize=9)
        ax.tick_params(axis="y", labelsize=8)
    ax1.set_ylabel("目標からのずれ [セント]", fontsize=9)
    ax1.set_ylim(-60, 60)
    ax2.set_ylim(-60, 170)
    ax2.text(7.55, 118, "上限の外（強く高い方へ\n引っ張られ不安定）→", fontsize=7.5,
             color="#d93025", ha="right")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig4_prelim.png"), dpi=220)
    plt.close(fig)


# ---------- 図5 窓を1本ずつ塞ぐための2ピース（STL） ----------
def fig5():
    a = trimesh.load(os.path.join(ROOT, "out", "cipher_close_pairA.stl"))
    b = trimesh.load(os.path.join(ROOT, "out", "cipher_close_pairB.stl"))
    plate = trimesh.load(os.path.join(ROOT, "out", "cipher_close_pairs_plate.stl"))
    # 組み立てイメージ: bは印刷姿勢のまま(丸い背が上)。aを上下反転して(丸い背が下)
    # bの真上に重ねる=丸い背どうしが接し、窓が上面と下面の外側に出る。
    b2 = b.copy()
    b2.apply_translation(-b2.bounds[0])                     # 最小角を原点へ
    a2 = a.copy()
    a2.apply_transform(trimesh.transformations.rotation_matrix(np.pi, [1, 0, 0]))
    a2.apply_translation(-a2.bounds[0])                     # 反転後、最小角を原点へ
    a2.apply_translation([0, 0, b2.bounds[1][2]])           # bの真上へ積む
    asm = trimesh.util.concatenate([a2, b2])
    fig = plt.figure(figsize=(6.4, 2.7))
    ax1 = fig.add_subplot(121, projection="3d")
    render_mesh(ax1, plate, elev=30, azim=-60)
    ax1.set_title("印刷時（2ピースを並べて印刷）", fontsize=9, pad=0)
    ax2 = fig.add_subplot(122, projection="3d")
    render_mesh(ax2, asm, elev=20, azim=-58, face="#a9cba5", edge="#3f5c3c")
    ax2.set_title("使用時（丸い背どうしを合わせて2×2に）", fontsize=9, pad=0)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig5_pairs.png"), dpi=220)
    plt.close(fig)


if __name__ == "__main__":
    fig1(); fig2(); fig3(); fig4(); fig5()
    for f in sorted(os.listdir(OUT)):
        print(f, os.path.getsize(os.path.join(OUT, f)), "bytes")
