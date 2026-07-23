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
# 窓 local z -> -X(内側), 長さ local x -> -Y(半径), 幅 local y -> +Z, det=+1
M_INNER = np.eye(4)
M_INNER[:3, :3] = np.array([[0, 0, -1], [-1, 0, 0], [0, 1, 0]], float)


def _spool_body(path=SPOOL):
    s = trimesh.load(path)
    g = s.geometry["3"].copy()          # 40.7mm厚の半体（外面フランジ＝最大x）
    g.apply_translation(-g.bounds[0])
    return g


def place_flutes(notes, carve=True, spool_path=SPOOL, start_deg=90.0, rrim=100.0):
    """音名リストを 360/N 度ずつ放射状に配置。戻り値 (result_mesh, infos)。"""
    spool = _spool_body(spool_path)
    xface = spool.bounds[1][0]          # 外面
    yc, zc = 100.0, 100.0
    base = trimesh.load(mini10.BASE)
    n = len(notes)
    placed, infos = [], []
    for i, note in enumerate(notes):
        L = mini10.length_for_note(note)
        g = mini10.flute(L, base=base)
        g.apply_transform(M_INNER)
        wz = g.bounds[1][2] - g.bounds[0][2]
        # 床を外面へ→窓は内側(xface-4)。吸込口(y=0)をリムへ。幅をzc中心へ。
        g.apply_transform(tf.translation_matrix([xface, yc + rrim, zc - wz / 2]))
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


def place_flutes_multiobj(notes, carve=True, spool_path=SPOOL, start_deg=90.0, rrim=100.0):
    """スプール本体と各笛を別オブジェクトにした Scene を返す（GUIでオブジェクトごとの設定用）。
    彫り抜き(carve)はスプール本体だけに適用し、笛は別オブジェクトのまま残す。戻り値 (scene, infos)。"""
    spool = _spool_body(spool_path)
    xface = spool.bounds[1][0]
    yc, zc = 100.0, 100.0
    base = trimesh.load(mini10.BASE)
    n = len(notes)
    placed, infos = [], []
    for i, note in enumerate(notes):
        L = mini10.length_for_note(note)
        g = mini10.flute(L, base=base)
        g.apply_transform(M_INNER)
        wz = g.bounds[1][2] - g.bounds[0][2]
        g.apply_transform(tf.translation_matrix([xface, yc + rrim, zc - wz / 2]))
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
    args = ap.parse_args(argv)
    notes = [s.strip() for s in args.notes.split(",") if s.strip()]
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    if args.multiobj:
        sc, infos = place_flutes_multiobj(notes, carve=not args.no_carve, start_deg=args.start_deg)
        sc.export(args.out)
        print("wrote %s （マルチオブジェクト・%d本＋スプール・%.1f度間隔・carve=%s）"
              % (args.out, len(notes), 360.0 / len(notes), not args.no_carve))
    else:
        result, infos = place_flutes(notes, carve=not args.no_carve, start_deg=args.start_deg)
        result.export(args.out)
        print("wrote %s （%d本・%.1f度間隔・faces=%d・carve=%s）"
              % (args.out, len(notes), 360.0 / len(notes), len(result.faces), not args.no_carve))
    for it in infos:
        print("  %-4s L=%5.1fmm  角度=%5.1f度" % (it["note"], it["L"], it["angle"]))


if __name__ == "__main__":
    main()
