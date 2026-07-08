"""全体を直方体にするコンパクト笛ジェネレータ（目標①・箱モジュール、A案）。

これまでの小型笛は「折り曲げによる箱胴＋円筒ヘッド」で、外形が箱と円筒の
混在だった。ここでは3モデル（折りなし／折り1／折り2）とも、外形を1個の
直方体（共通フットプリント 16×16mm、折りは幅だけ伸びる）に統一する。

A案の考え方（音を変えない）:
  実績のあるv6円筒ヘッド（assets/head_v6.stl）と共鳴ボアはそのまま使い、
  外側だけを角shellで包む。窓（歌口）の1面だけ角shellを凹ませて開口を残す。
  ボアの形状・長さは各モデルの実績値そのままなので、既存の較正式が流用できる。

  ・折りなし … compact.py と同じ丸ボアØ9.5（片閉じ管）を16角柱に内包
  ・折り1/2 … fold.py と同じ蛇行ボア(bore=8)を16角柱に内包

作り方は build.py/compact.py の哲学を踏襲する。箱の中空（ボア・ヘッド逃げ・
窓の開口）は watertight 同士の manifold 差で彫り、非watertightな実績ヘッドは
差の後にメッシュとして重ねてスライサに union させる。

実行には trimesh + manifold3d が要る（fold.py / plenum.py と同じ環境）。
"""
import os
import sys
import argparse
import numpy as np
import trimesh

sys.path.insert(0, os.path.dirname(__file__))
import fold

ASSETS = os.path.join(os.path.dirname(__file__), os.pardir, "assets")
OUT = os.path.join(os.path.dirname(__file__), os.pardir, "out")
HEAD = os.path.join(ASSETS, "head_v6.stl")

FOOT = 16.0            # 共通フットプリント（16×16mm、折りは幅Wだけ伸びる）
HEAD_CUT_Z = fold.HEAD_CUT_Z     # 143.0  v6座標の切断面
HEAD_LEN = fold.HEAD_LEN         # 26.48  ヘッド高
HEAD_POCKET_D = 14.6             # ヘッド逃げ穴（Ø14.07 円筒＋クリアランス0.5）
WALL = 2.0                       # 折りボアの壁（fold.py と同じ）
CAP_TH = 2.0                     # 片閉じ管の閉端（compact.py と同じ）
STRAIGHT_BORE_D = 9.5            # 折りなしの丸ボア（compact.py と同じ）


def _len_for_note(note):
    """折りなし用: 音→片閉じ管の管長(mm)。compact.py と同一の較正式。"""
    return fold.CALIB_K / fold._note_freq(note) - fold.CALIB_DELTA

# 窓（歌口）の開口を彫るレシピ。v6ヘッドの窓は切断面直上 z=143..161（＝0..18mm）に
# あり、円筒の1面へ開いている。ヘッドを+90°ヨーして窓を箱の-y面へ向け、その面を凹ませる。
WIN_YAW = np.pi / 2.0            # 窓を -y 面へ向ける
WIN_Z0 = -1.0                    # ボア上端(=切断面)を基準にした窓開口の下端
WIN_Z1 = 18.0                    # 同 上端
WIN_HALF_X = 6.0                 # 窓開口の x 半幅


def _round_bore(bore_d, z0, z1, cx=0.0, cy=0.0):
    """折りなし用の丸ボア中空（片閉じ管）。z0..z1 の円柱。"""
    r = bore_d / 2.0
    c = trimesh.creation.cylinder(radius=r, segment=[[cx, cy, z0], [cx, cy, z1]], sections=64)
    return c


def _head_mesh(head_stl, x_head, y_head, bore_top_z, yaw=WIN_YAW):
    """実績ヘッドを読み込み、x/y中心を原点へ→ヨー→切断面をbore_top_zへ、(x_head,y_head)に置く。"""
    m = trimesh.load(head_stl)
    b = m.bounds
    cx, cy = (b[0][0] + b[1][0]) / 2, (b[0][1] + b[1][1]) / 2
    m.apply_translation([-cx, -cy, 0.0])                       # x/y中心を原点へ
    m.apply_transform(trimesh.transformations.rotation_matrix(yaw, [0, 0, 1]))
    m.apply_translation([x_head, y_head, bore_top_z - HEAD_CUT_Z])
    return m


def _box(W, D, H, cx=0.0, cy=0.0):
    b = trimesh.creation.box(extents=[W, D, H])
    b.apply_translation([cx, cy, H / 2.0])
    return b


def _frustum(r0, r1, z0, z1, cx=0.0, cy=0.0, sections=64):
    """円錐台（下端半径r0・上端半径r1）のwatertightメッシュ。ポケット床の45°漏斗に使う。"""
    ang = np.linspace(0, 2 * np.pi, sections, endpoint=False)
    b = np.column_stack([cx + r0 * np.cos(ang), cy + r0 * np.sin(ang), np.full(sections, z0)])
    t = np.column_stack([cx + r1 * np.cos(ang), cy + r1 * np.sin(ang), np.full(sections, z1)])
    cb = [cx, cy, z0]; ct = [cx, cy, z1]
    V = np.vstack([b, t, cb, ct])
    ib, it = 2 * sections, 2 * sections + 1
    F = []
    for i in range(sections):
        j = (i + 1) % sections
        F.append([i, j, sections + j]); F.append([i, sections + j, sections + i])   # 側面
        F.append([ib, j, i])                                                         # 下キャップ
        F.append([it, sections + i, sections + j])                                   # 上キャップ
    m = trimesh.Trimesh(vertices=V, faces=np.array(F), process=True)
    m.fix_normals()
    return m


def _head_pocket(x_head, bore_r, bore_top, total_H):
    """ヘッド逃げ穴。床は45°漏斗（ボア径→Ø14.6）にして、ヘッド底の円環が無垢の上に着地するようにする
    （平床だとヘッド底リングの真下が空洞になり空中印刷になるため）。"""
    r_pk = HEAD_POCKET_D / 2.0
    cone_h = r_pk - bore_r                    # 45°（半径差ぶん立ち上げ）
    funnel = _frustum(bore_r, r_pk, bore_top - 0.2, bore_top - 0.2 + cone_h, cx=x_head)
    tube = trimesh.creation.cylinder(
        radius=r_pk, segment=[[x_head, 0, bore_top - 0.2 + cone_h], [x_head, 0, total_H + 1.0]],
        sections=64)
    return trimesh.util.concatenate([funnel, tube])


def _extrude_yz(poly, x0, x1):
    """y-z平面の凸多角形poly（+x方向から見てCCW）をx方向[x0,x1]へ押し出したwatertightメッシュ。"""
    n = len(poly)
    V = [[x0, y, z] for (y, z) in poly] + [[x1, y, z] for (y, z) in poly]
    F = []
    for i in range(1, n - 1):                       # 前キャップ(-x外向き)
        F.append([0, i + 1, i])
    for i in range(1, n - 1):                       # 後キャップ(+x外向き)
        F.append([n, n + i, n + i + 1])
    for i in range(n):                              # 側面
        j = (i + 1) % n
        F.append([i, j, n + j])
        F.append([i, n + j, n + i])
    m = trimesh.Trimesh(vertices=np.array(V, float), faces=np.array(F), process=True)
    m.fix_normals()
    return m


def _window_void(x_head, y_face, y_inner, z0, z1, half_x):
    """窓の前を開ける凹み。天井を45°ひさしにしてサポート無しで自立させる（プレナムと同じ原理）。
    内側(y_inner)で天井z1、外側(y_face)へz1+Δと45°で上がる（Δ=y_inner-y_face）。
    下向きの水平天井を作らないので、縦置き印刷で支え無しに架かる。"""
    d = y_inner - y_face                            # >0
    # y-z断面: 外下→内下→内上(z1)→外上(z1+d) の台形（45°の天井）
    poly = [(y_face, z0), (y_inner, z0), (y_inner, z1), (y_face, z1 + d)]
    return _extrude_yz(poly, x_head - half_x, x_head + half_x)


def _window_for_head(x_head, D, bore_top_z, half_x=WIN_HALF_X):
    """A案（実績ヘッド内包）用の浅い窓凹み。ヘッド前面(y≈-7)手前の薄い箱壁だけを削り、
    45°ひさしを付ける。深掘りしない（深掘りは大きな水平天井を作るため不可）。"""
    y_face = -(D / 2.0) - 1.0        # 外面より少し外（きれいに削る）
    y_inner = -(FOOT / 2.0) + 2.0    # ヘッド前面(≈-7)を1mm越える浅さ（16なら y=-6）
    return _window_void(x_head, y_face, y_inner,
                        bore_top_z + WIN_Z0, bore_top_z + WIN_Z1, half_x)


def boxed_flute(note=None, N=1, L=None, bore_d=None, head_stl=HEAD):
    """1本の箱笛。N=1は丸ボアの折りなし、N>=2は蛇行ボアの折り笛。
    返り値 (mesh, info)。外形は W×16×(H_body+26.5) の直方体。"""
    if N <= 1:
        # 折りなし: compact.py と同じ丸ボアØ9.5
        bd = bore_d if bore_d else STRAIGHT_BORE_D
        bore_len = L if L is not None else _len_for_note(note)
        W = D = FOOT
        x_head = 0.0
        H_body = bore_len
        total_H = H_body + HEAD_LEN
        box = _box(W, D, total_H)
        bore = _round_bore(bd, CAP_TH, H_body + 0.5)           # 閉端CAP_TH残し、上端はヘッドへ連結
        pocket = _head_pocket(x_head, bd / 2.0, H_body, total_H)
        slot = _window_for_head(x_head, D, H_body)
        voids = trimesh.util.concatenate([bore, pocket, slot])
        path_len = bore_len
    else:
        # 折り: fold.py と同じ蛇行ボア(bore=8)
        bd = bore_d if bore_d else 8.0
        Lgeo = L if L is not None else fold.geom_len_for_note(note, N)
        pts, (W, _Dep, H), (x0, path_len) = fold.centerline(Lgeo, N, bd, WALL, WALL)
        D = FOOT
        x_head = x0
        H_body = H
        total_H = H_body + HEAD_LEN
        box = _box(W, D, total_H)
        bore = fold.bore_solid(pts, bd)
        pocket = _head_pocket(x_head, bd / 2.0, H_body, total_H)
        slot = _window_for_head(x_head, D, H_body)
        voids = trimesh.util.concatenate([bore, pocket, slot])

    hollow = trimesh.boolean.difference([box, voids], engine="manifold")
    head = _head_mesh(head_stl, x_head, 0.0, H_body)
    flute = trimesh.util.concatenate([hollow, head])
    info = dict(W=W, D=D, H_body=H_body, total_H=total_H, path_len=path_len,
                N=N, bore=bd, x_head=x_head)
    return flute, info


def three_model_panel(note="C6", gap=6.0, head_stl=HEAD):
    """折りなし／折り1／折り2 の3モデルを、同じ音で横一列に並べたパネル。"""
    specs = [("折りなし", 1), ("折り1", 2), ("折り2", 3)]
    flutes, infos = [], []
    xoff = 0.0
    prev_half = 0.0
    for label, N in specs:
        f, info = boxed_flute(note=note, N=N, head_stl=head_stl)
        w = info["W"]
        # 各笛はx中心が0なので、パネル上ではxoffへ平行移動
        if flutes:
            xoff += prev_half + gap + w / 2.0
        f.apply_translation([xoff, 0, 0])
        prev_half = w / 2.0
        info["label"] = label
        info["x"] = xoff
        flutes.append(f)
        infos.append(info)
    panel = trimesh.util.concatenate(flutes)
    return panel, infos


# ---------------------------------------------------------------------------
# B案: 角ネイティブのフィッポルヘッド（実験的・要 実機ボイシング）。
# 実績ヘッドの構造（上吹き込み → 縦windway → 側面窓 → labium）を角断面へ移す。
# 完全な一体押し出し（円筒ヘッド不使用）。音は変わるので較正はやり直し。
# ---------------------------------------------------------------------------
SQ_BORE = 9.5          # 共鳴ボア（実績と同径の丸ボア）
SQ_CUTUP = 4.5         # 窓のz長（cutup）
SQ_WINW = 9.0          # 窓のx幅
SQ_WINLEN = 12.0       # windwayのz長（吹込口までの高さ）
SQ_FLUE_GAP = 1.0      # flue（windway）の厚み
SQ_WCH = 8.0           # windwayのx幅
SQ_WALL_WF = 1.0       # windwayとボア窓面の間の壁厚（flue–labiumオフセットを決める）


def square_fipple(L, cutup=SQ_CUTUP, wall_wf=SQ_WALL_WF, flue_gap=SQ_FLUE_GAP,
                  bore_d=SQ_BORE):
    """角ネイティブのフィッポル笛（B案）。closedボア長L(閉端→窓下端)。
    flue–labiumオフセット = bore_r + wall_wf + flue_gap/2 - bore_r = wall_wf + flue_gap/2。"""
    r = bore_d / 2.0
    top = L + cutup + SQ_WINLEN
    col = trimesh.creation.box(extents=[FOOT, FOOT, top])
    col.apply_translation([0, 0, top / 2.0])
    bore = trimesh.creation.cylinder(radius=r, segment=[[0, 0, CAP_TH], [0, 0, L + cutup]], sections=64)
    # 窓（-y面から x±SQ_WINW/2、ボア内(y=-r+1.75)まで開口）。天井は45°ひさしで自立。
    win = _window_void(0.0, y_face=-FOOT / 2 - 0.1, y_inner=-r + 1.75,
                       z0=L, z1=L + cutup, half_x=SQ_WINW / 2.0)
    # windway（ボア-y壁の外側に壁wall_wfを残し、flue_gap厚の縦チャンネルを天面まで）
    ywi = -r - wall_wf
    ywo = ywi - flue_gap
    ww = trimesh.creation.box(extents=[SQ_WCH, flue_gap, SQ_WINLEN + 0.1])
    ww.apply_translation([0, (ywi + ywo) / 2.0, top - SQ_WINLEN / 2.0 + 0.05])
    voids = trimesh.util.concatenate([bore, win, ww])
    flute = trimesh.boolean.difference([col, voids], engine="manifold")
    offset = wall_wf + flue_gap / 2.0
    info = dict(W=FOOT, D=FOOT, total_H=top, L=L, cutup=cutup, offset=offset, N="sqfipple")
    return flute, info


def fipple_voicing_comb(L=45.0, gap=6.0):
    """まず『鳴るか』を見る変奏コーム。固定管長Lで、flue–labiumオフセット(壁厚)と
    cutupを振った数本を横一列に。1回刷って鳴る組合せを選び、その後に管長較正へ進む。"""
    variants = [
        ("o0.6c4", dict(wall_wf=0.6, cutup=4.0)),
        ("o1.0c4.5", dict(wall_wf=1.0, cutup=4.5)),
        ("o1.0c6", dict(wall_wf=1.0, cutup=6.0)),
        ("o1.5c5", dict(wall_wf=1.5, cutup=5.0)),
    ]
    flutes, infos = [], []
    xoff = 0.0
    for label, kw in variants:
        f, info = square_fipple(L, **kw)
        if flutes:
            xoff += FOOT / 2.0 + gap + FOOT / 2.0
        f.apply_translation([xoff, 0, 0])
        info["label"] = label
        info["x"] = xoff
        flutes.append(f)
        infos.append(info)
    return trimesh.util.concatenate(flutes), infos


def _row_bar(x0, x1, y_center, depth, z0=-2.0, th=2.0):
    """列の底を繋ぐ薄いバー（印刷安定のため。fold.py の連結バーと同趣旨）。"""
    bar = trimesh.creation.box(extents=[x1 - x0, depth, th])
    bar.apply_translation([(x0 + x1) / 2.0, y_center, z0 + th / 2.0])
    return bar


def ab_plate(note="C6", gap=8.0, row_gap=20.0, head_stl=HEAD):
    """A案(3モデル) と B案(フィッポル変奏4本) を1プレートに載せる。
    Row A(y+)=箱笛3モデル、Row B(y-)=角フィッポル4変奏。各列は底で連結バー留め。"""
    parts, infos = [], []

    # Row A: A案 3モデル
    a_specs = [("折りなし", 1), ("折り1", 2), ("折り2", 3)]
    a_flutes = [(lb, boxed_flute(note=note, N=N, head_stl=head_stl)) for lb, N in a_specs]
    xoff = 0.0
    prev_half = 0.0
    yA = (16.0 + row_gap) / 2.0
    xs_a = []
    for lb, (f, info) in a_flutes:
        w = info["W"]
        if xs_a:
            xoff += prev_half + gap + w / 2.0
        xs_a.append((xoff, w))
        prev_half = w / 2.0
        info["label"] = lb
        info["x"] = xoff
        f.apply_translation([xoff, yA, 0])
        parts.append(f)
        infos.append(info)
    ax0 = xs_a[0][0] - xs_a[0][1] / 2 - 2
    ax1 = xs_a[-1][0] + xs_a[-1][1] / 2 + 2

    # Row B: B案 フィッポル 4変奏
    b_variants = [("o0.6c4", dict(wall_wf=0.6, cutup=4.0)),
                  ("o1.0c4.5", dict(wall_wf=1.0, cutup=4.5)),
                  ("o1.0c6", dict(wall_wf=1.0, cutup=6.0)),
                  ("o1.5c5", dict(wall_wf=1.5, cutup=5.0))]
    yB = -(16.0 + row_gap) / 2.0
    xoff = 0.0
    xs_b = []
    for i, (lb, kw) in enumerate(b_variants):
        f, info = square_fipple(45.0, **kw)
        if i:
            xoff += FOOT / 2.0 + gap + FOOT / 2.0
        xs_b.append(xoff)
        info["label"] = lb
        info["x"] = xoff
        f.apply_translation([xoff, yB, 0])
        parts.append(f)
        infos.append(info)
    bx0 = xs_b[0] - FOOT / 2 - 2
    bx1 = xs_b[-1] + FOOT / 2 + 2

    parts.append(_row_bar(ax0, ax1, yA, 16.0))
    parts.append(_row_bar(bx0, bx1, yB, 16.0))
    plate = trimesh.util.concatenate(parts)
    return plate, infos


def validation_plate(note="C6", gap=8.0, head_stl=HEAD, base_th=2.0, margin=3.0,
                     brim_h=0.0, brim_margin=6.0):
    """検証セット: A案 折りなし(N1)＋折り2(N3)＋B案1変奏 を一列に並べる。
    base_th>0 なら共通ベース板の上に載せる（ラフト兼ブリム）。
    base_th<=0 ならベース無し＝各笛が自分の平底で直接ベッドに立つ。
    brim_h>0 なら各笛の底に薄いフランジ（実体ブリム）を付ける＝スライサ非依存で定着面を確保。"""
    f1, i1 = boxed_flute(note=note, N=1, head_stl=head_stl); i1["label"] = "A:折りなし"
    f3, i3 = boxed_flute(note=note, N=3, head_stl=head_stl); i3["label"] = "A:折り2"
    fb, ib = square_fipple(45.0, wall_wf=0.6, cutup=4.0);     ib["label"] = "B:o0.6c4"
    seq = [(f1, i1), (f3, i3), (fb, ib)]
    parts, infos = [], []
    xoff = 0.0
    prev_half = 0.0
    xs = []
    for f, info in seq:
        w = info["W"]
        if parts:
            xoff += prev_half + gap + w / 2.0
        prev_half = w / 2.0
        info["x"] = xoff
        xs.append((xoff, w))
        f.apply_translation([xoff, 0, 0])
        parts.append(f)
        if brim_h > 0:                       # 各笛の底に実体ブリム（フランジ）を融合
            bw = w + 2 * brim_margin
            bd = FOOT + 2 * brim_margin
            fl = trimesh.creation.box(extents=[bw, bd, brim_h])
            fl.apply_translation([xoff, 0, brim_h / 2.0])
            parts.append(fl)
        infos.append(info)
    x0 = xs[0][0] - xs[0][1] / 2 - margin
    x1 = xs[-1][0] + xs[-1][1] / 2 + margin
    if base_th > 0:
        base = trimesh.creation.box(extents=[x1 - x0, FOOT + 2 * margin, base_th])
        base.apply_translation([(x0 + x1) / 2.0, 0, -base_th / 2.0])
        parts = parts + [base]
    plate = trimesh.util.concatenate(parts)
    plate.apply_translation([-(x0 + x1) / 2.0, 0, 0])   # x中心を原点へ
    return plate, infos


def main():
    ap = argparse.ArgumentParser(description="全体直方体のコンパクト笛（A案）")
    ap.add_argument("--note", default="C6", help="狙いの音（例 C6）")
    ap.add_argument("--N", type=int, default=None, help="折り本数。1=折りなし,2=折り1,3=折り2")
    ap.add_argument("--panel", action="store_true", help="3モデルを同じ音で横一列に")
    ap.add_argument("--fipple-comb", action="store_true",
                    help="B案: 角ネイティブ フィッポルのボイシング変奏コーム（実験的）")
    ap.add_argument("--ab-plate", action="store_true",
                    help="A案3モデル＋B案4変奏を1プレートに（A1 mini投入用）")
    ap.add_argument("--valid-plate", action="store_true",
                    help="検証セット(A案N1+N3+B案1変奏)を共通ベース板に載せて（先行印刷用）")
    ap.add_argument("--no-base", action="store_true",
                    help="--valid-plate でベース板を付けず、3本を並べただけにする（手動GUI印刷用）")
    ap.add_argument("--head", default=HEAD)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    if a.valid_plate:
        base_th = 0.0 if a.no_base else 2.0
        mesh, infos = validation_plate(a.note, head_stl=a.head, base_th=base_th)
        suffix = "_nobase" if a.no_base else ""
        name = a.out or os.path.join(OUT, f"box_valid_plate_{a.note.replace('#','s')}{suffix}.stl")
        mesh.export(name)
        print(f"検証セット（{a.note}, {'ベース無し・3本並べただけ' if a.no_base else '共通ベース板2mm'}）:")
        for i in infos:
            print("  %-10s 外形%.0f×%.0f×%.0f" % (i["label"], i["W"], i["D"], i["total_H"]))
        print("プレート外形", np.round(mesh.extents, 1), "->", name)
    elif a.ab_plate:
        mesh, infos = ab_plate(a.note, head_stl=a.head)
        name = a.out or os.path.join(OUT, f"box_ab_plate_{a.note.replace('#','s')}.stl")
        mesh.export(name)
        print(f"AB結合プレート（A案3モデル＋B案4変奏, {a.note}）:")
        for i in infos:
            tag = "A案" if i["N"] != "sqfipple" else "B案"
            print("  %-4s %-9s 外形%.0f×%.0f×%.0f  x=%.0f"
                  % (tag, i["label"], i["W"], i["D"], i["total_H"], i["x"]))
        print("プレート外形", np.round(mesh.extents, 1), "（A1 mini 180×180 に収まるか要確認）->", name)
    elif a.fipple_comb:
        mesh, infos = fipple_voicing_comb()
        name = a.out or os.path.join(OUT, "box_fipple_voicing_comb.stl")
        mesh.export(name)
        print("B案 角フィッポル ボイシング変奏コーム（固定管長・実験的）:")
        for i in infos:
            print("  %-9s 外形%.0f×%.0f×%.0f  cutup%.1f flue-labiumオフセット%.2fmm"
                  % (i["label"], i["W"], i["D"], i["total_H"], i["cutup"], i["offset"]))
        print("コーム外形", np.round(mesh.extents, 1), "->", name)
    elif a.panel:
        mesh, infos = three_model_panel(a.note, head_stl=a.head)
        name = a.out or os.path.join(OUT, f"box_panel_{a.note.replace('#','s')}.stl")
        mesh.export(name)
        print(f"3モデル箱笛パネル（{a.note}）:")
        for i in infos:
            print("  %-6s 外形 %.0f×%.0f×%.0f mm  路長%.1f  縦パス%d(折り%d)"
                  % (i["label"], i["W"], i["D"], i["total_H"], i["path_len"], i["N"], i["N"] - 1))
        print("パネル外形", np.round(mesh.extents, 1), "->", name)
    else:
        N = a.N if a.N is not None else 1
        mesh, info = boxed_flute(note=a.note, N=N, head_stl=a.head)
        name = a.out or os.path.join(OUT, f"box_{a.note.replace('#','s')}_N{N}.stl")
        mesh.export(name)
        print("%s N=%d -> 外形 %.0f×%.0f×%.0f mm  路長%.1f"
              % (a.note, N, info["W"], info["D"], info["total_H"], info["path_len"]))
        print("  saved", name)


if __name__ == "__main__":
    main()
