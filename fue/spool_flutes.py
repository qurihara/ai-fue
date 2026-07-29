"""スプール（フィラメントリール）の円周をN分割し、指定した音の笛を放射状に埋め込む。

- 笛の個数と種類（音名リスト）を渡すと、N=len(notes)本を 360/N 度ずつ均等配置する。
- 各笛は「窓を内側(-x)へ・吸込口をリム(r=100)＝円周に接する・平床を外面と面一」に置く
  （外面のHex notchハニカムを避け、窓は内側の開いた空間へ開口する）。
- carve=True なら、笛の外形（凸包）でスプールにポケットをboolean彫り抜きしてから笛を戻す。
  これでボア（笛内部の空洞）はスプール材料で埋まらない。carve=False は重ね置き（高速・確認用）。

使い方:
  python3 fue/spool_flutes.py --notes C7,G#6,F#6,G#6,C7 --out out/spool.3mf
  python3 fue/spool_flutes.py --notes F#6,A6,C7,E7,F#7,C7,G6,B6 --out out/spool8.3mf --no-carve
"""
from __future__ import annotations
import argparse, os, sys
import numpy as np
import trimesh
from trimesh import transformations as tf

sys.path.insert(0, os.path.dirname(__file__))
import mini10

SPOOL = os.path.join(os.path.dirname(__file__), os.pardir,
                     "temp", "tools", "Spool_V3_Hex_notch_(sticker).3mf")
# 元の3mfは半体を2つ含み、円盤(フランジ)の向きが互いに逆である。
#   geom "3" = プレート2 "My spool V3 Hex notch updated"（厚さ40.7mm・外面は最大x）
#   geom "1" = プレート1 "My spool V3 hex (sticker)" （厚さ34.1mm・外面は最小x）
# どちらでも「床を外面に面一・窓を内側へ・吸込口をリムへ」を保つよう、外面の側を自動判定して
# 配置行列を選ぶ。どちらも det=+1 の回転で、鏡像にはしない（笛は真正なコピーのまま）。
#
# 外面が最大x側のとき: 窓 local z -> -X(内側), 長さ local x -> -Y(半径), 幅 local y -> +Z
M_INNER = np.eye(4)
M_INNER[:3, :3] = np.array([[0, 0, -1], [-1, 0, 0], [0, 1, 0]], float)
# 外面が最小x側のとき: 窓 local z -> +X(内側), 長さ local x -> -Y(半径), 幅 local y -> -Z
M_INNER_MINX = np.eye(4)
M_INNER_MINX[:3, :3] = np.array([[0, 0, 1], [-1, 0, 0], [0, -1, 0]], float)


def _spool_body(path=SPOOL, geom_key="3"):
    s = trimesh.load(path)
    g = s.geometry[geom_key].copy()
    g.apply_translation(-g.bounds[0])
    return g


def _outer_face(body, rrim=100.0, probe_r=95.0):
    """円盤(フランジ)がどちらのx面にあるかを実測して返す。
    戻り値 (xface, sign)。sign=+1 は外面が最大x側、-1 は最小x側。"""
    X = body.bounds[1][0]
    yc, zc = 100.0, 100.0
    xs_lo = np.arange(0.3, min(6.0, X), 0.5)              # 最小x側の数mm
    xs_hi = np.arange(X - 0.3, max(X - 6.0, 0.0), -0.5)   # 最大x側の数mm
    def hits(xs):
        pts = np.column_stack([xs, np.full_like(xs, yc + probe_r), np.full_like(xs, zc)])
        return int(body.contains(pts).sum())
    n_lo, n_hi = hits(xs_lo), hits(xs_hi)
    if n_hi >= n_lo:
        return float(X), +1
    return 0.0, -1


def _orient_and_place(g, xface, sign, yc, zc, rrim, width=None):
    """1本の笛を、外面の側に応じて向けて置く（床を外面に面一・窓を内側・吸込口をリムへ）。

    width を渡すと、その幅で中心を合わせる。基準笛の印（タブや矢印）を付けた笛は幅が
    広くなるので、印まで含めた幅で中心を取ると[* 本体そのものが横へずれて隣の笛と当たる]。
    印の無い笛の幅を渡して、本体の位置が印の有無で動かないようにする。
    """
    g.apply_transform(M_INNER if sign > 0 else M_INNER_MINX)
    wz = width if width is not None else (g.bounds[1][2] - g.bounds[0][2])
    dz = (zc - wz / 2) if sign > 0 else (zc + wz / 2)
    g.apply_transform(tf.translation_matrix([xface, yc + rrim, dz]))
    return g


def place_flutes(notes, carve=True, spool_path=SPOOL, start_deg=90.0, rrim=100.0,
                 geom_key="3"):
    """音名リストを 360/N 度ずつ放射状に配置。戻り値 (result_mesh, infos)。"""
    spool = _spool_body(spool_path, geom_key)
    xface, sign = _outer_face(spool, rrim)      # 円盤(外面)がどちら側かを実測
    yc, zc = 100.0, 100.0
    L_max = mini10.uniform_body_length([mini10.length_for_note(nt) for nt in notes])
    n = len(notes)
    placed, infos = [], []
    for i, note in enumerate(notes):
        L = mini10.length_for_note(note)
        g = mini10.uniform_flute(L, L_max=L_max)   # 外見統一版（長さから音が読めない）
        if i == 0:
            g = mini10.reference_tab(g)             # 基準笛の印（吸込口脇のタブ）
        # 床を外面へ面一に→窓は内側。吸込口(y=0)をリムへ。幅をzc中心へ。
        g = _orient_and_place(g, xface, sign, yc, zc, rrim)
        theta = np.deg2rad(start_deg + i * (360.0 / n))
        g.apply_transform(tf.rotation_matrix(theta, [1, 0, 0], [0, yc, zc]))
        placed.append(g)
        infos.append(dict(note=note, L=round(L, 1), angle=round((start_deg + i * 360.0 / n) % 360, 1)))
    if carve:
        carved = spool
        for g in placed:
            carved = carved.difference(g.convex_hull, engine="manifold")
        result = trimesh.util.concatenate([carved] + placed)
    else:
        result = trimesh.util.concatenate([spool] + placed)
    return result, infos


def rim_wedge(center, r_rim, z0, z1, a_start, a_end, h_start=3.5, h_end=0.0, steps=48):
    """円盤の外周に、始まりの笛から次の笛の側へ細くなっていく出っぱりを作る。

    笛は円盤の厚み(4mm)いっぱいに埋まっていて、床は外面と面一である。そのため笛に付けた
    印は外面から出っぱらず、[* 触っても見ても分からない]（2026-07-29、栗原さんの指摘）。
    出っぱらせられるのは外周のふちだけなので、そこへ印を置く。

    始まりの笛のところが3.5mmで、進む向きへ13度ほどかけて0へ細くなる。指を這わせると、
    片側からは崖に当たり、反対側からはなだらかに乗り上がるので、[* 触っただけで向きが分かる]。
    """
    cx, cy = center
    ang = np.linspace(a_start, a_end, steps)
    t = np.linspace(0.0, 1.0, steps)
    h = h_start + (h_end - h_start) * t
    inner = np.column_stack([cx + (r_rim - 0.6) * np.cos(ang), cy + (r_rim - 0.6) * np.sin(ang)])
    outer = np.column_stack([cx + (r_rim + h) * np.cos(ang), cy + (r_rim + h) * np.sin(ang)])
    poly = np.vstack([inner, outer[::-1]])
    from shapely.geometry import Polygon as _Poly
    wedge = trimesh.creation.extrude_polygon(_Poly(poly).buffer(0), height=z1 - z0)
    wedge.apply_translation([0, 0, z0])
    return wedge


def place_flutes_multiobj(notes, carve=True, spool_path=SPOOL, start_deg=90.0, rrim=100.0,
                          geom_key="3", ref_tab=True, l_max=None, print_pose=True,
                          rim_mark=True):
    """スプール本体と各笛を別オブジェクトにした Scene を返す（GUIでオブジェクトごとの設定用）。
    彫り抜き(carve)はスプール本体だけに適用し、笛は別オブジェクトのまま残す。戻り値 (scene, infos)。

    l_max を渡すと外形長をその値に固定する。1つの秘密を複数のスプールへ分けて埋めるときは、
    プレートごとに音の顔ぶれが違っても外形は同じでなければならない（外見から音が読めては
    ならないため）。ref_tab=False なら基準笛の印(タブ)を付けない（基準笛が別のプレートに
    ある場合）。"""
    spool = _spool_body(spool_path, geom_key)
    xface, sign = _outer_face(spool, rrim)
    yc, zc = 100.0, 100.0
    L_max = l_max or mini10.uniform_body_length([mini10.length_for_note(nt) for nt in notes])
    n = len(notes)

    plain = mini10.uniform_flute(mini10.length_for_note(notes[0]), L_max=L_max)
    plain_w = float(np.abs(
        (M_INNER if sign > 0 else M_INNER_MINX)[:3, :3] @ (plain.bounds[1] - plain.bounds[0]))[2])

    def place(mesh, i):
        mesh = _orient_and_place(mesh, xface, sign, yc, zc, rrim, width=plain_w)
        theta = np.deg2rad(start_deg + i * (360.0 / n))
        rot = tf.rotation_matrix(theta, [1, 0, 0], [0, yc, zc])
        mesh.apply_transform(rot)
        return mesh, rot

    # 印の矢印を、次に吹く笛の側へ向ける。native の +y と -y のどちらが 2本目の方向かは
    # 置き方（外面がどちら側か・回す向き）で決まるので、実際に2本置いて確かめる。
    probe_L = mini10.length_for_note(notes[0])
    p0, rot0 = place(mini10.uniform_flute(probe_L, L_max=L_max), 0)
    p1, _ = place(mini10.uniform_flute(probe_L, L_max=L_max), 1)
    R0 = rot0[:3, :3] @ (M_INNER if sign > 0 else M_INNER_MINX)[:3, :3]
    to_next = p1.bounds.mean(axis=0) - p0.bounds.mean(axis=0)
    tab_plus_y = bool(np.dot(R0 @ np.array([0.0, 1.0, 0.0]), to_next) > 0)

    placed, infos = [], []
    for i, note in enumerate(notes):
        L = mini10.length_for_note(note)
        g = mini10.uniform_flute(L, L_max=L_max)
        if i == 0 and ref_tab:
            # 三角形の印にして、始まりの笛と進む向きの両方を形で示す。
            g = mini10.direction_tab(g, plus_y=tab_plus_y)
        g = _orient_and_place(g, xface, sign, yc, zc, rrim, width=plain_w)
        theta = np.deg2rad(start_deg + i * (360.0 / n))
        rot = tf.rotation_matrix(theta, [1, 0, 0], [0, yc, zc])
        g.apply_transform(rot)
        placed.append(g)
        # 向きの検査(orient_check)に渡せるよう、native姿勢からの回転を記録しておく。
        R = rot[:3, :3] @ (M_INNER if sign > 0 else M_INNER_MINX)[:3, :3]
        infos.append(dict(note=note, L=round(L, 1),
                          angle=round((start_deg + i * 360.0 / n) % 360, 1), R=R))
    body = spool
    if carve:
        for g in placed:
            body = body.difference(g.convex_hull, engine="manifold")
    if print_pose:
        # 元の3mfは円盤が立った姿勢（スプールの軸がx）である。印刷は円盤を寝かせて
        # 外面をベッドに付ける。こうすると笛の長軸が水平になり、窓は真上を向く。
        # 検証済みの向き（横置き・窓が-135度から+135度）のちょうど真ん中である。
        P = tf.rotation_matrix(np.pi / 2 if sign > 0 else -np.pi / 2, [0, 1, 0])
        body.apply_transform(P)
        for g in placed:
            g.apply_transform(P)
        zmin = min([body.bounds[0][2]] + [g.bounds[0][2] for g in placed])
        T = tf.translation_matrix([0, 0, -zmin])
        body.apply_transform(T)
        for g in placed:
            g.apply_transform(T)
        for it in infos:
            it["R"] = P[:3, :3] @ it["R"]

        # 外周のふちに、始まりの笛と進む向きを示す出っぱりを足す（印刷姿勢で作る）。
        if rim_mark and ref_tab and len(placed) >= 2:
            c = np.array([100.0, 100.0])
            def angle_of(mesh):
                v = mesh.bounds.mean(axis=0)[:2] - c
                return float(np.arctan2(v[1], v[0]))
            a0, a1 = angle_of(placed[0]), angle_of(placed[1])
            step = (a1 - a0 + np.pi) % (2 * np.pi) - np.pi      # 進む向き（符号つき）
            span = np.sign(step) * np.deg2rad(13.0)
            zt = max(g.bounds[1][2] for g in placed)            # 笛＝円盤の厚み
            wedge = rim_wedge(c, 100.0, 0.0, zt, a0, a0 + span)
            body = trimesh.boolean.union([body, wedge], engine="manifold")

    sc = trimesh.Scene()
    sc.add_geometry(body, geom_name="spool_0.20mm")
    for i, (note, g) in enumerate(zip(notes, placed)):
        sc.add_geometry(g, geom_name="flute%d_%s_0.08careful" % (i + 1, note))
    return sc, infos


def main(argv=None):
    ap = argparse.ArgumentParser(description="スプール円周N分割・放射状の笛埋め込み")
    ap.add_argument("--notes", required=True, help="音名をカンマ区切り（例 C7,G#6,F#6,G#6,C7）")
    ap.add_argument("--out", required=True, help="出力3mf")
    ap.add_argument("--no-carve", action="store_true", help="彫り抜きせず重ね置き（高速・確認用）")
    ap.add_argument("--multiobj", action="store_true", help="スプールと笛を別オブジェクトで書き出す（GUIでオブジェクトごとの設定用）")
    ap.add_argument("--start-deg", type=float, default=90.0, help="1本目の角度（度）")
    ap.add_argument("--geom", default="3",
                    help="どちらの半体か（'3'=プレート2 notch updated 40.7mm厚, "
                         "'1'=プレート1 sticker 34.1mm厚）。外面の向きは自動判定する")
    args = ap.parse_args(argv)
    notes = [s.strip() for s in args.notes.split(",") if s.strip()]
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    if args.multiobj:
        sc, infos = place_flutes_multiobj(notes, carve=not args.no_carve, start_deg=args.start_deg, geom_key=args.geom)
        sc.export(args.out)
        print("wrote %s （マルチオブジェクト・%d本＋スプール・%.1f度間隔・carve=%s）"
              % (args.out, len(notes), 360.0 / len(notes), not args.no_carve))
    else:
        result, infos = place_flutes(notes, carve=not args.no_carve, start_deg=args.start_deg, geom_key=args.geom)
        result.export(args.out)
        print("wrote %s （%d本・%.1f度間隔・faces=%d・carve=%s）"
              % (args.out, len(notes), 360.0 / len(notes), len(result.faces), not args.no_carve))
    for it in infos:
        print("  %-4s L=%5.1fmm  角度=%5.1f度" % (it["note"], it["L"], it["angle"]))


if __name__ == "__main__":
    main()
