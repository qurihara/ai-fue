"""折り曲げ（蛇行）ボアのコンパクト笛ジェネレータ（目標①のさらなる小型化）。

角柱ブロックの中に、上下に往復する蛇行ボアを彫る。実効的な気柱長（中心線の路長）は
そのままに、背の高さを折り回数でほぼ 1/N に縮められる。上には実績のあるv6ヘッドを載せる。

印刷: ヘッドを上にして縦置きする。往復する縦管の壁は完全に垂直なので張り出しゼロ。
折り返しの水平部だけが天井を持つが、ボアを細くすればブリッジ span が数mmと短く、
FDMが架けられる。うまく垂れる場合は断面を涙滴/菱形にする（別途）。

ブロックからボアを引くブール演算は trimesh + manifold3d を使う（コントローラの .venv）。
ヘッドは非watertightなので結合せず、別メッシュとして重ねてスライサに union させる。
"""
import sys
import numpy as np
import trimesh

HEAD_STL = None  # 実行時に指定
HEAD_CUT_Z = 143.0
HEAD_TOP_Z = 169.48
HEAD_LEN = HEAD_TOP_Z - HEAD_CUT_Z

# 較正（コンパクト笛と共通）と、折り補正。
#   直管: f = CALIB_K/(Leff+CALIB_DELTA)
#   折り補正: 180°折り返し1回につき実効長が約3.3mm短くなる（2026/7/1 折りパネル実測）。
#   よって狙いの実効長Leffに対し、必要な中心線路長 = Leff + 3.3*(折り返し回数)。
CALIB_K = 91891.5
CALIB_DELTA = 14.227
FOLD_CORR_PER_TURN = 3.3


def _note_freq(note):
    names = {"C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4, "F": 5,
             "F#": 6, "G": 7, "G#": 8, "A": 9, "A#": 10, "B": 11}
    import re
    m = re.match(r"([A-G]#?)(-?\d)", note)
    midi = names[m.group(1)] + 12 * (int(m.group(2)) + 1)
    return 440.0 * 2 ** ((midi - 69) / 12)


def geom_len_for_note(note, N):
    """狙いの音と折り本数Nから、彫るべき中心線路長(mm)を折り補正込みで返す。"""
    Leff = CALIB_K / _note_freq(note) - CALIB_DELTA
    return Leff + FOLD_CORR_PER_TURN * (N - 1)


def centerline(L, N, bore_d, wall, top_wall):
    """N本の縦パスからなる蛇行の中心線。返り値は点列と、ブロック寸法。"""
    s = bore_d + wall                     # パス間隔
    xs = [(i - (N - 1) / 2.0) * s for i in range(N)]
    c = bore_d / 2.0 + top_wall           # パス0が上面まで余分に伸びるぶん
    p = (L - (N - 1) * s - c) / N         # 1パスの縦長さ（ターンと上面余白を差し引く）
    if p <= 5:
        raise ValueError("Lに対して折り回数Nが多すぎる（p=%.1f）" % p)
    zb = wall + bore_d / 2.0
    zt = zb + p
    H = zt + bore_d / 2.0 + top_wall
    W = (N - 1) * s + bore_d + 2 * wall
    Dep = bore_d + 2 * wall
    # 点列: パス0を上面(H)から下(zb)へ、以降ターンして往復
    pts = [(xs[0], H + 0.5), (xs[0], zb)]
    z_cur = zb
    for i in range(1, N):
        pts.append((xs[i], z_cur))                      # 水平ターン
        z_other = zt if z_cur == zb else zb
        pts.append((xs[i], z_other))                    # 縦パス
        z_cur = z_other
    # 路長（上面 z=H から閉端まで＝音響的な長さ）
    path = [(xs[0], H)] + pts[1:]
    length = sum(np.hypot(path[k + 1][0] - path[k][0], path[k + 1][1] - path[k][1])
                 for k in range(len(path) - 1))
    return pts, (W, Dep, H), (xs[0], length)


def bore_solid(pts, bore_d):
    r = bore_d / 2.0
    parts = []
    for k in range(len(pts) - 1):
        a = np.array([pts[k][0], 0.0, pts[k][1]])
        b = np.array([pts[k + 1][0], 0.0, pts[k + 1][1]])
        parts.append(trimesh.creation.cylinder(radius=r, segment=[a, b], sections=48))
    for (x, z) in pts[1:-1]:                              # 角に球を置いて滑らかに繋ぐ
        sph = trimesh.creation.icosphere(subdivisions=2, radius=r)
        sph.apply_translation([x, 0.0, z])
        parts.append(sph)
    return trimesh.boolean.union(parts)


def head_mesh(head_stl, x0, block_H):
    m = trimesh.load(head_stl)
    b = m.bounds
    cx, cy = (b[0][0] + b[1][0]) / 2, (b[0][1] + b[1][1]) / 2
    # x/y中心を(x0,0)へ、切断面(min z=143)をブロック上面Hへ
    m.apply_translation([x0 - cx, -cy, block_H - b[0][2]])
    return m


def folded_flute(L, N, head_stl, bore_d=8.0, wall=2.0, top_wall=2.0):
    pts, (W, Dep, H), (x0, length) = centerline(L, N, bore_d, wall, top_wall)
    block = trimesh.creation.box(extents=[W, Dep, H])
    block.apply_translation([0, 0, H / 2.0])             # z 0..H
    bore = bore_solid(pts, bore_d)
    hollow = trimesh.boolean.difference([block, bore])
    head = head_mesh(head_stl, x0, H)
    flute = trimesh.util.concatenate([hollow, head])
    return flute, dict(W=W, D=Dep, H=H, total_H=H + HEAD_LEN, path_len=length, passes=N)


def panel(specs, head_stl, bore_d=8.0, gap=4.0):
    """specs=[(label,L,N),...] を横一列に並べ、下に連結バーを付けたテストパネル。"""
    flutes = []
    infos = []
    xoff = 0.0
    prev_half = 0.0
    for (label, L, N) in specs:
        f, info = folded_flute(L, N, head_stl, bore_d)
        w = info["W"]
        if flutes:
            xoff += prev_half + gap + w / 2.0
        f.apply_translation([xoff, 0, 0])
        prev_half = w / 2.0
        flutes.append(f)
        info["label"] = label
        info["x"] = xoff
        infos.append(info)
    # 連結バー
    x0 = infos[0]["x"] - infos[0]["W"] / 2 - 2
    x1 = infos[-1]["x"] + infos[-1]["W"] / 2 + 2
    bar = trimesh.creation.box(extents=[x1 - x0, bore_d + 6, 3])
    bar.apply_translation([(x0 + x1) / 2, 0, -1.5])
    return trimesh.util.concatenate(flutes + [bar]), infos


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="折り曲げボアのコンパクト笛")
    ap.add_argument("--L", type=float, help="ボアの中心線長さ(mm)")
    ap.add_argument("--note", help="狙いの音（折り補正込みでLを自動計算）、例 C6")
    ap.add_argument("--N", type=int, default=2, help="折り（縦パス）本数")
    ap.add_argument("--panel", help="テストパネル指定 'label:L:N,...'（例 C6n1:73.6:1,C6n2:73.6:2）")
    ap.add_argument("--bore", type=float, default=8.0)
    ap.add_argument("--head", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    if a.panel:
        specs = []
        for tok in a.panel.split(","):
            lab, L, N = tok.split(":")
            specs.append((lab, float(L), int(N)))
        mesh, infos = panel(specs, a.head, a.bore)
        mesh.export(a.out)
        for info in infos:
            print("  %-8s L狙い ブロック%.0fx%.0fx%.0f 全長%.0fmm 実路長%.1fmm 折り%d"
                  % (info["label"], info["W"], info["D"], info["H"], info["total_H"],
                     info["path_len"], info["passes"]))
        print("外形", np.round(mesh.extents, 1), "saved", a.out)
    else:
        L = a.L if a.L is not None else geom_len_for_note(a.note, a.N)
        if a.note:
            print("狙い %s → 折り補正込み中心線路長 %.1fmm（折り%d）" % (a.note, L, a.N))
        flute, info = folded_flute(L, a.N, a.head, a.bore)
        flute.export(a.out)
        print("L=%.1f N=%d bore=%.1f -> ブロック %.0fx%.0fx%.0f 全長%.0fmm 実路長%.1fmm"
              % (a.L, a.N, a.bore, info['W'], info['D'], info['H'], info['total_H'], info['path_len']))
        print("  saved", a.out)
