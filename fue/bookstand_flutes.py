"""シンプルな本立て（底板＋立った壁2枚）に、笛を水平に埋め込む。

ホストは temp/tools/book_stand/tinker.obj（栗原さんの新しいデザイン）。底板が厚さ約5mm、
その両端に厚さ約5mmの壁が2枚立っている、素直なコの字である。前の本立て（櫛状の仕切りが
並ぶ複雑な形）と違い、笛を置ける平らな板が3枚あるだけなので、レイアウトが単純になる。

置き方の考え方は次のとおりである。

  [* 笛はすべて水平]（長軸を奥行き方向 y に沿わせる）。実機で確かめた「横置きで窓が
  真上から±135度以内なら鳴る」範囲のうち、壁では±90度、底板では0度になる。前の本立ては
  笛を縦に立てていて、これは鳴らないと分かった向きであった。

  [* 窓は本立ての内側（本が入る側）へ向ける]。壁の笛は内面へ、底板の笛は上面へ開く。
  内側は空気なので、窓の正面に障害物が無い。

  [* 吸込口は手前の端面（y=0）にそろえる]。前から見ると、左の壁・底板・右の壁の縁に
  吸込口が並ぶので、コの字を一筆でなぞるように順に吹ける。

  [* 窓は面より0.3mmだけ出す]。面ちょうどに合わせると、彫り抜き（笛の凸包ぶん）の外側に
  薄い材料が残って窓が密閉されることがある（HeartBeadsで踏んだ失敗）。

使い方:
    python3 fue/bookstand_flutes.py                      # 既定の秘密 pass_#26 を埋める
    python3 fue/bookstand_flutes.py --payload 'text'
    python3 fue/bookstand_flutes.py --no-carve           # 彫り抜きなし（形の確認用・速い）
"""
from __future__ import annotations
import argparse
import json
import os
import sys

import numpy as np
import trimesh
from trimesh import transformations as tf

sys.path.insert(0, os.path.dirname(__file__))
import cipher_codec as cd
import mini10
import orient_check

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)
OUT = os.path.join(ROOT, "out")
HOST = os.path.join(ROOT, "temp", "tools", "book_stand", "tinker.obj")
CONFIG = os.path.join(ROOT, "docs", "cipher", "cipher_config.json")

DEMO_PAYLOAD = b"pass_#26"      # 64bit。以前のスプールから引き継いだデモの秘密
SLOT12 = dict(lo_note="G#6", hi_note="G7")

PROUD = 0.3        # 窓を面からどれだけ出すか[mm]
MARGIN_Z = 12.0    # 壁の笛を置き始める高さ[mm]（底板との取り合いを避ける）
MARGIN_TOP = 1.5   # 壁が丸くなり始める高さから、さらに下へ取る余白[mm]
MARGIN_X = 6.0     # 底板の笛を壁から離す距離[mm]
MOUTH_Y = 0.4      # 吸込口を置く手前の端面[mm]


def measure_host(host):
    """底板の上面、壁の内面と外面を実測する。"""
    b = host.bounds
    zs = np.arange(0.1, 20, 0.1)
    ins = host.contains(np.column_stack([np.full_like(zs, (b[0][0] + b[1][0]) / 2),
                                         np.full_like(zs, (b[0][1] + b[1][1]) / 2), zs]))
    base_top = float(zs[ins][-1])
    zc = base_top + 60.0
    xs = np.arange(b[0][0] - 0.1, b[0][0] + 12, 0.1)
    i = host.contains(np.column_stack([xs, np.full_like(xs, 50.0), np.full_like(xs, zc)]))
    left = (float(xs[i][0]), float(xs[i][-1]))
    xs = np.arange(b[1][0] - 12, b[1][0] + 0.1, 0.1)
    i = host.contains(np.column_stack([xs, np.full_like(xs, 50.0), np.full_like(xs, zc)]))
    right = (float(xs[i][0]), float(xs[i][-1]))
    # 壁の上端は円形に絞られている。笛は吸込口を手前の端面にそろえ、奥へ66mm伸びるので、
    # [* 前縁と、笛の足の位置の両方が、まだ full の奥行きで残っている高さ]までしか置けない。
    # その境目を実測する（設計を変えても自動で追従するように、値を決め打ちしない）。
    zs = np.arange(float(b[1][2]) - 0.5, base_top, -0.5)
    xc = (left[0] + left[1]) / 2.0
    front = host.contains(np.column_stack([np.full_like(zs, xc),
                                           np.full_like(zs, MOUTH_Y + 0.4), zs]))
    back = host.contains(np.column_stack([np.full_like(zs, xc),
                                          np.full_like(zs, MOUTH_Y + 66.0), zs]))
    ok = np.where(front & back)[0]
    wall_top = float(zs[ok[0]]) if len(ok) else base_top + 20.0
    return dict(base_top=base_top, left=left, right=right,
                top=float(b[1][2]), wall_top=wall_top, depth=float(b[1][1]))


def _rot(axis, deg):
    return tf.rotation_matrix(np.radians(deg), axis)


# 3つの置き場。R は native（窓+z・床z=0・吸込口x=0・長さ+x）に掛ける回転。
#   長軸はどれも +y（奥行き方向）にそろえる。
R_BASE = _rot([0, 0, 1], 90)                      # 窓は +z（上面＝内側）
R_LEFT = _rot([0, 1, 0], 90) @ R_BASE             # 窓は +x（左の壁の内面）
R_RIGHT = _rot([0, 1, 0], -90) @ R_BASE           # 窓は -x（右の壁の内面）


def place(note, R, window_plane, l_max, mouth_y=MOUTH_Y, ref_tab=False):
    """1本を置く。window_plane は窓を合わせる面の上の1点（世界座標）。

    面の位置は必ず点で渡し、窓の向き w への投影として使う。座標の値をそのまま渡すと、
    w が -x のような向きのときに符号が反転して笛が反対側へ飛ぶ。
    """
    fl = mini10.uniform_flute(mini10.length_for_note(note), L_max=l_max)
    fl.apply_transform(R)
    w = R[:3, :3] @ np.array([0.0, 0.0, 1.0])      # 窓の向き
    w = w / np.linalg.norm(w)
    v = fl.vertices
    target = float(np.dot(np.asarray(window_plane, dtype=float), w))
    d = (target - float(v.dot(w).max())) * w
    d[1] = mouth_y - fl.bounds[0][1]               # 吸込口を手前の端面へ
    fl.apply_translation(d)
    return fl, w


def add_front_tab(fl, R, host_center=None, out=2.5, size=(2.5, 1.6)):
    """基準笛の印を、吸込口のある端面から手前へ出る小さな突起として付ける。

    突起は[* 笛自身の断面の中に収める]。隣の笛との隙間へ横に出すと、隙間が2mmを切る
    詰め方では隣に当たる。前方（吸込口の側）だけへ出せば、隣にも板の縁にも触れない。
    位置は断面の窓寄りに取る。吸込口の風道は床の側にあるので、そこは塞がない。

    mini10.reference_tab は native 姿勢を前提に箱を置くので、笛を回してから呼ぶと
    まったく違う場所に生えてしまう。ここでは配置に使った回転行列から軸を作る。
    """
    axis = R[:3, :3] @ np.array([1.0, 0.0, 0.0])       # 長軸（吸込口→足）
    width = R[:3, :3] @ np.array([0.0, 1.0, 0.0])      # 幅
    win = R[:3, :3] @ np.array([0.0, 0.0, 1.0])        # 窓の向き
    for v in (axis, width, win):
        v /= np.linalg.norm(v)
    v = fl.vertices
    mouth = float(v.dot(axis).min())
    center_w = (float(v.dot(width).min()) + float(v.dot(width).max())) / 2.0
    top_v = float(v.dot(win).max())
    pos = (axis * (mouth - out / 2.0 + 0.2)
           + width * center_w
           + win * (top_v - size[1] / 2.0 - 0.6))
    tab = trimesh.creation.box(extents=[size[0], out, size[1]])
    M = np.eye(4)
    M[:3, 0] = width
    M[:3, 1] = axis
    M[:3, 2] = win
    M[:3, 3] = pos
    tab.apply_transform(M)
    return trimesh.boolean.union([fl, tab], engine="manifold")


def layout(notes, host, geom):
    """左の壁（上から下）→底板（左から右）→右の壁（下から上）の順に置く。

    コの字を一筆でなぞる順になるので、吹く順番が物の形から分かる。
    """
    l_max = mini10.uniform_body_length(
        [mini10.length_for_note(n) for n in mini10.CALIB12])
    # 壁と底板に何本ずつ置くかは、隣どうしの隙間ができるだけ均等になるように決める。
    span_wall = (geom["wall_top"] - MARGIN_TOP) - MARGIN_Z
    span_base = (geom["right"][0] - MARGIN_X) - (geom["left"][1] + MARGIN_X)
    best = None
    for n_base in range(2, len(notes) - 3):
        n_wall, rem = divmod(len(notes) - n_base, 2)
        if rem or n_wall < 1:
            continue
        gw = (span_wall - 7.0 * n_wall) / max(1, n_wall - 1)
        gb = (span_base - 7.0 * n_base) / max(1, n_base - 1)
        if min(gw, gb) < 1.0:            # 隙間1mmを下回る詰め方はしない
            continue
        score = -min(gw, gb)             # いちばん狭い隙間ができるだけ広くなる分け方
        if best is None or score < best[0]:
            best = (score, n_wall, n_base, gw, gb)
    if best is None:
        raise ValueError("笛%d本は、この本立てには詰め込めない（壁%.0fmm・底板%.0mm）"
                         % (len(notes), span_wall, span_base))
    _, n_wall, n_base, gap_w, gap_b = best
    zs = np.linspace(MARGIN_Z, geom["wall_top"] - MARGIN_TOP - 7.0, n_wall) + 3.5
    xs = np.linspace(geom["left"][1] + MARGIN_X,
                     geom["right"][0] - MARGIN_X - 7.0, n_base) + 3.5
    print("  壁は z=%.1f まで（そこから上は円形に絞られる）。隣どうしの隙間は壁%.1fmm・底板%.1fmm"
          % (geom["wall_top"], gap_w, gap_b))

    placed, infos = [], []
    order = ([("left", z) for z in zs[::-1]]
             + [("base", x) for x in xs]
             + [("right", z) for z in zs])
    for i, (note, (where, pos)) in enumerate(zip(notes, order)):
        if where == "left":
            R, win = R_LEFT, [geom["left"][1] + PROUD, 0.0, 0.0]
        elif where == "right":
            R, win = R_RIGHT, [geom["right"][0] - PROUD, 0.0, 0.0]
        else:
            R, win = R_BASE, [0.0, 0.0, geom["base_top"] + PROUD]
        fl, w = place(note, R, win, l_max)
        # 板に沿う方向へずらす（壁は高さ、底板は左右）
        if where == "base":
            fl.apply_translation([pos - (fl.bounds[0][0] + fl.bounds[1][0]) / 2, 0, 0])
        else:
            fl.apply_translation([0, 0, pos - (fl.bounds[0][2] + fl.bounds[1][2]) / 2])
        if i == 0:
            fl = add_front_tab(fl, R)
        placed.append(fl)
        infos.append(dict(note=note, where=where, R=R))
    return placed, infos


def build(notes, carve=True, engine="manifold"):
    host = trimesh.load(HOST, force="mesh")
    host.apply_translation(-host.bounds[0])
    geom = measure_host(host)
    placed, infos = layout(notes, host, geom)

    # 向きの検査（必須）。本立ては使う向き（壁が立った姿勢）のまま刷る。
    for it, fl in zip(infos, placed):
        res = orient_check.check_orientation(R=it["R"])
        it["window_deg"] = round(res.angle_deg, 1)
        it["tilt_deg"] = round(res.tilt_deg, 1)
        if res.verdict != "ok":
            raise ValueError("%s（%s）の向きが %s: %s"
                             % (it["note"], it["where"], res.verdict, res.message))

    body = host
    if carve:
        for fl in placed:
            body = body.difference(fl.convex_hull, engine=engine)

    sc = trimesh.Scene()
    sc.add_geometry(body, geom_name="bookstand_0.20mm")
    sc.add_geometry(trimesh.util.concatenate(placed), geom_name="flutes_0.08careful")
    return sc, infos, geom


def main(argv=None):
    ap = argparse.ArgumentParser(description="本立てに笛を水平に埋め込む")
    ap.add_argument("--payload", default=None, help="秘密（既定は pass_#26）")
    ap.add_argument("--parity", type=int, default=4, help="RSブロックあたりのパリティ記号数")
    ap.add_argument("--no-carve", action="store_true")
    ap.add_argument("--out", default=os.path.join(OUT, "bookstand_pass26.3mf"))
    args = ap.parse_args(argv)

    payload = args.payload.encode() if args.payload else DEMO_PAYLOAD
    with open(CONFIG, encoding="utf-8") as fp:
        base = json.load(fp)
    cfg = cd.CodecConfig(**{**base, **SLOT12, "ecc_parity": args.parity,
                            "mode": "sequential", "no_repeat": True})
    notes = list(cd.encode(payload, cfg).notes)
    for i in range(len(notes) - 1):
        assert notes[i] != notes[i + 1], "隣り合う笛が同じ音になっている"
    print("秘密 %r（%dbit）" % (payload, len(payload) * 8))
    print("符号化: 12スロット・隣接同音禁止・パリティ%d記号/ブロック → 笛%d本"
          % (args.parity, len(notes)))

    sc, infos, geom = build(notes, carve=not args.no_carve)
    os.makedirs(OUT, exist_ok=True)
    sc.export(args.out)
    n = {}
    for it in infos:
        n[it["where"]] = n.get(it["where"], 0) + 1
    print("配置: 左の壁%d本・底板%d本・右の壁%d本（この順に吹く）"
          % (n.get("left", 0), n.get("base", 0), n.get("right", 0)))
    print("向きの検査: %d本すべて ok（壁は窓%+.0f度／%+.0f度、底板は窓%+.0f度、傾きは全部0度）"
          % (len(infos),
             [i["window_deg"] for i in infos if i["where"] == "left"][0],
             [i["window_deg"] for i in infos if i["where"] == "right"][0],
             [i["window_deg"] for i in infos if i["where"] == "base"][0]))
    print("外形 %s mm -> %s" % (np.round(sc.bounds[1] - sc.bounds[0], 1),
                               os.path.relpath(args.out, ROOT)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
