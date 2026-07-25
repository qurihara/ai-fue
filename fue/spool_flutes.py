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


def _orient_and_place(g, xface, sign, yc, zc, rrim):
    """1本の笛を、外面の側に応じて向けて置く（床を外面に面一・窓を内側・吸込口をリムへ）。"""
    g.apply_transform(M_INNER if sign > 0 else M_INNER_MINX)
    wz = g.bounds[1][2] - g.bounds[0][2]
    dz = (zc - wz / 2) if sign > 0 else (zc + wz / 2)
    g.apply_transform(tf.translation_matrix([xface, yc + rrim, dz]))
    return g


def place_flutes(notes, carve=True, spool_path=SPOOL, start_deg=90.0, rrim=100.0,
                 geom_key="3"):
    """音名リストを 360/N 度ずつ放射状に配置。戻り値 (result_mesh, infos)。"""
    spool = _spool_body(spool_path, geom_key)
    xface, sign = _outer_face(spool, rrim)      # 円盤(外面)がどちら側かを実測
    yc, zc = 100.0, 100.0
    L_max = max(mini10.length_for_note(nt) for nt in notes)   # 外見統一の外形長
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


def place_flutes_multiobj(notes, carve=True, spool_path=SPOOL, start_deg=90.0, rrim=100.0,
                          geom_key="3"):
    """スプール本体と各笛を別オブジェクトにした Scene を返す（GUIでオブジェクトごとの設定用）。
    彫り抜き(carve)はスプール本体だけに適用し、笛は別オブジェクトのまま残す。戻り値 (scene, infos)。"""
    spool = _spool_body(spool_path, geom_key)
    xface, sign = _outer_face(spool, rrim)
    yc, zc = 100.0, 100.0
    L_max = max(mini10.length_for_note(nt) for nt in notes)
    n = len(notes)
    placed, infos = [], []
    for i, note in enumerate(notes):
        L = mini10.length_for_note(note)
        g = mini10.uniform_flute(L, L_max=L_max)
        if i == 0:
            g = mini10.reference_tab(g)
        g = _orient_and_place(g, xface, sign, yc, zc, rrim)
        theta = np.deg2rad(start_deg + i * (360.0 / n))
        g.apply_transform(tf.rotation_matrix(theta, [1, 0, 0], [0, yc, zc]))
        placed.append(g)
        infos.append(dict(note=note, L=round(L, 1), angle=round((start_deg + i * 360.0 / n) % 360, 1)))
    body = spool
    if carve:
        for g in placed:
            body = body.difference(g.convex_hull, engine="manifold")
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
