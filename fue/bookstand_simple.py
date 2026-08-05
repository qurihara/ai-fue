"""直方体3枚だけで作る本立て（v5）に、笛を水平に埋め込む。

なぜ作り直したか（2026-07-31、栗原さんの実機観察による）
--------------------------------------------------------
v4（tinker.obj をホストにした版）をA1 mini・PLAで刷ったところ、3つの問題が出た。

  1. [* 端がめくれ上がった]。ブリムが5mmでは足りない。
  2. [* 笛の造形が雑になった]。gcodeを調べると、笛のある高さで
     「すかすかの充填（sparse infill）」が13,707本、「宙に浮いた垂直な殻
     （floating vertical shell）」が6,105本あった。同じ0.08mmで刷ったカードは
     それぞれ0本と163本である。厚い底板の中に笛が埋まると、笛の周りと下が
     すかすかになり、ボアの下面や窓の天井が支えを失う。
     → [* 対策はスライス側]。笛のある高さ範囲の充填を100パーセントにする。
  3. [* 壁が立ち上がる角のアールが中空に張り出し、糸が垂れた]。
     → [* 対策はこの設計]。角の丸みをやめ、面はすべて垂直か水平にする。

新しい形（栗原さんの指示）
--------------------------
[* 床の板1枚と、それに直交する壁2枚を、単純な直方体で作る]。外形は前の本立ての凸包と
同じ（105 × 70 × 163.5mm）である。壁は床の上に乗せるのではなく[* 床と同じ高さ0から
立ち上げる]ので、壁の底面はすべてベッドに接地する。張り出しも丸みも無い。

笛の置き方は v4 から変えない。[* 床板だけに8本]、[* 窓は真上（+z）]、吸込口は手前の
端面（y=0）にそろえる。壁の縁に立てる置き方は造形不良が多いと分かっているので使わない。

使い方:
    python3 fue/bookstand_simple.py --symbols 2,0,9,7,5 --out out/bookstand_v5_share3.3mf
"""
from __future__ import annotations

import argparse
import json
import os
import sys

import numpy as np
import trimesh

sys.path.insert(0, os.path.dirname(__file__))
import bookstand_flutes as B
import cipher_codec as cd
import mini10
import orient_check

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)
OUT = os.path.join(ROOT, "out")
CONFIG = os.path.join(ROOT, "docs", "cipher", "cipher_config.json")

# 外形は v4（tinker.obj を奥行き0.7倍したもの）の凸包に合わせる。
WIDTH = 105.0       # 幅（笛が並ぶ方向）
DEPTH = 70.0        # 奥行き（笛の長軸の方向）
HEIGHT = 163.5      # 高さ（壁）
FLOOR = 4.9         # 床板の厚さ。笛は z1.2〜5.2 に入り、窓が上面より0.3mm出る
WALL = 5.0          # 壁の厚さ


def wall_mesh(round_top):
    """壁1枚を作る。round_top なら上端を半円にする（v4の見た目に合わせる）。

    v4（tinker.obj）の壁は[* z=124mmから上が丸く]、丸みの高さは39.5mm、奥行きは70mmで
    あった。ほぼ半径35mm（奥行きの半分）の半円である。ここでもその形を使う。
    断面は y-z 平面で作り、厚み方向（x）へ押し出す。
    """
    from shapely.geometry import Point, box as sbox
    from shapely.ops import unary_union

    r = DEPTH / 2.0
    if round_top:
        prof = unary_union([sbox(0, 0, DEPTH, HEIGHT - r),
                            Point(r, HEIGHT - r).buffer(r, resolution=96)])
        prof = prof.intersection(sbox(0, 0, DEPTH, HEIGHT))
    else:
        prof = sbox(0, 0, DEPTH, HEIGHT)
    m = trimesh.creation.extrude_polygon(prof, height=WALL)   # 押し出しは +z
    M = np.eye(4)
    M[:3, :3] = np.array([[0.0, 0.0, 1.0],     # 断面の x（＝奥行き y）→ 世界の y
                          [1.0, 0.0, 0.0],     # 断面の y（＝高さ z）→ 世界の z
                          [0.0, 1.0, 0.0]])    # 押し出し方向 → 世界の x（壁の厚み）
    m.apply_transform(M)
    m.apply_translation(-m.bounds[0])
    return m


def build_host(round_top=True):
    """床板1枚と壁2枚を作り、和を取る。

    壁は床の上に乗せず[* z=0から立ち上げる]ので、壁の底面はすべてベッドに接地する。
    v4では壁が立ち上がる角にアールがあり、それが中空に張り出して糸が垂れた。
    """
    floor = trimesh.creation.box(extents=[WIDTH, DEPTH, FLOOR])
    floor.apply_translation([WIDTH / 2, DEPTH / 2, FLOOR / 2])
    left = wall_mesh(round_top)
    right = wall_mesh(round_top)
    right.apply_translation([WIDTH - WALL, 0, 0])
    host = trimesh.boolean.union([floor, left, right], engine="manifold")
    host.merge_vertices()
    return host


def geom_of():
    """bookstand_flutes.layout が求める寸法の辞書を、設計値から直に作る。

    measure_host は複雑な形を実測するためのものだが、こちらは形が決まっているので
    測る必要がない。壁の上端が丸くならないので wall_top は天井そのものである。
    """
    return dict(base_top=FLOOR, left=(0.0, WALL), right=(WIDTH - WALL, WIDTH),
                top=HEIGHT, wall_top=HEIGHT, depth=DEPTH)


def build(notes, carve=True, engine="manifold", round_top=True):
    host = build_host(round_top)
    geom = geom_of()
    placed, infos = B.layout(notes, host, geom, base_only=True)

    for it, fl in zip(infos, placed):
        res = orient_check.check_orientation(R=it["R"])
        it["window_deg"] = round(res.angle_deg, 1)
        it["tilt_deg"] = round(res.tilt_deg, 1)
        if res.verdict != "ok":
            raise ValueError("%s（%s）の向きが %s: %s"
                             % (it["note"], it["where"], res.verdict, res.message))

    body = B.engrave_star(host, placed[0], infos[0]["R"])
    if carve:
        for fl, it in zip(placed, infos):
            body = body.difference(B.carve_tool(fl, it["R"]), engine=engine)

    sc = trimesh.Scene()
    sc.add_geometry(body, geom_name="bookstand_0.28fast")
    sc.add_geometry(trimesh.util.concatenate(placed), geom_name="flutes_0.08careful")
    return sc, infos, geom


def main(argv=None):
    ap = argparse.ArgumentParser(description="直方体3枚の本立てに笛を埋め込む（v5）")
    ap.add_argument("--symbols", default=None,
                    help="記号列を直接載せる（例 2,0,9,7,5）。秘密分散の断片を入れるときに使う")
    ap.add_argument("--payload", default=None, help="秘密（既定は pass_#26）")
    ap.add_argument("--parity", type=int, default=2, help="RSブロックあたりのパリティ記号数")
    ap.add_argument("--no-carve", action="store_true")
    ap.add_argument("--square-top", action="store_true",
                    help="壁の上端を丸めずに角のままにする（既定は半円）")
    ap.add_argument("--out", required=True, help="出力する3mf（版を含む名前にする）")
    args = ap.parse_args(argv)

    if os.path.exists(args.out):
        raise SystemExit("すでにある版を上書きしようとしている: %s（--out を新しくする）" % args.out)

    with open(CONFIG, encoding="utf-8") as fp:
        base = json.load(fp)
    if args.symbols:
        cfg = cd.CodecConfig(**{**base, **B.SLOT12, "ecc_parity": args.parity,
                                "mode": "symbols", "no_repeat": True})
        syms = [int(x) for x in args.symbols.replace(",", " ").split()]
        notes = list(cd.encode_symbols(syms, cfg).notes)
        print("記号列 %s（%d個）を載せる" % (",".join(map(str, syms)), len(syms)))
    else:
        payload = args.payload.encode() if args.payload else B.DEMO_PAYLOAD
        cfg = cd.CodecConfig(**{**base, **B.SLOT12, "ecc_parity": args.parity,
                                "mode": "sequential", "no_repeat": True})
        notes = list(cd.encode(payload, cfg).notes)
        print("秘密 %r（%dbit）" % (payload, len(payload) * 8))
    for i in range(len(notes) - 1):
        assert notes[i] != notes[i + 1], "隣り合う笛が同じ音になっている"
    print("符号化: 12スロット・隣接同音禁止・パリティ%d記号/ブロック → 笛%d本"
          % (args.parity, len(notes)))

    sc, infos, geom = build(notes, carve=not args.no_carve,
                            round_top=not args.square_top)
    os.makedirs(OUT, exist_ok=True)
    sc.export(args.out)
    print("笛 %d本（左から右へこの順に吹く）: %s"
          % (len(infos), " ".join(i["note"] for i in infos)))
    print("向きの検査: %d本すべて ok（窓%+.0f度＝真上、傾きは全部0度）"
          % (len(infos), infos[0]["window_deg"]))
    print("外形 %s mm（床板 %.1fmm・壁 %.1fmm・壁の上端は%s）-> %s"
          % (np.round(sc.bounds[1] - sc.bounds[0], 1), FLOOR, WALL,
             "角のまま" if args.square_top else "半円（半径%.1fmm）" % (DEPTH / 2),
             os.path.relpath(args.out, ROOT)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
