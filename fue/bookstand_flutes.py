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
import stencil

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)
OUT = os.path.join(ROOT, "out")
HOST = os.path.join(ROOT, "temp", "tools", "book_stand", "tinker.obj")
CONFIG = os.path.join(ROOT, "docs", "cipher", "cipher_config.json")

DEMO_PAYLOAD = b"pass_#26"      # 64bit。以前のスプールから引き継いだデモの秘密
SLOT12 = dict(lo_note="G#6", hi_note="G7")

# 吸込口は[* 面一（0.0）でよい]。本体の前面にそのまま穴として開く（実測で被り0.00mm）。
# 面より引っ込めると被って塞がるので、そこだけ気をつければよい（底板の笛を前面より
# 0.4mm奥に置いて0.35mm塞いだことがある）。
# 窓は面一だと[* 0.08mmの薄皮が残った]（凸包の面と本体の面がぴったり重なるため）。
# 押し出し線1本(0.42mm)より薄いので刷られない公算が高いが、0.3mm出しておけば確実に消える。
PROUD = 0.3        # 窓を面からどれだけ出すか[mm]
MOUTH_PROUD = 0.0  # 吸込口を本体の前面からどれだけ前へ出すか[mm]
MARGIN_Z = 12.0    # 壁の笛を置き始める高さ[mm]（底板との取り合いを避ける）
MARGIN_TOP = 1.5   # 壁が丸くなり始める高さから、さらに下へ取る余白[mm]
MARGIN_X = 6.0     # 底板の笛を壁から離す距離[mm]
MOUTH_Y = -MOUTH_PROUD   # 吸込口のy座標。本体の前面(y=0)より前へ出す


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
    # 探る点は本体の中に取る（吸込口は本体より前へ出しているので、MOUTH_Yを基準にしない）
    front = host.contains(np.column_stack([np.full_like(zs, xc),
                                           np.full_like(zs, 0.6), zs]))
    back = host.contains(np.column_stack([np.full_like(zs, xc),
                                          np.full_like(zs, MOUTH_Y + 66.5), zs]))
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


def engrave_star(host, fl, R, r=None, depth=0.8, gap=None, margin=0.5):
    """1本目（基準笛）の[* 足のすぐ先]に、＊を浅く彫り込む。

    Chordika のトニック笛と同じ目印である。突起や隆起した帯は目立ちすぎるので、
    本の側（本立ての内側）を向く面へ、少しだけ彫る。笛の足より先の材料に彫るので、
    ボアにも窓にも吸込口にも触れない。
    """
    axis = R[:3, :3] @ np.array([1.0, 0.0, 0.0])       # 吸込口→足
    win = R[:3, :3] @ np.array([0.0, 0.0, 1.0])        # 窓の向き＝内側
    for v in (axis, win):
        v /= np.linalg.norm(v)
    v = fl.vertices
    foot = float(v.dot(axis).max())
    # ＊は笛の足の先の帯に彫る。帯の幅は本立ての奥行きで決まるので、そこから大きさを決める。
    # 奥行きを縮めた版（v2）では帯が4mmほどしかないので、＊も小さくする。
    strip = float(host.vertices.dot(axis).max()) - foot
    if r is None:
        r = min(2.4, (strip - 2 * margin) / 2.0)
    if gap is None:
        # 帯が広いときは足のすぐ先（3.5mm）に置き、狭いときは帯の中央に寄せる
        gap = max(margin, min(3.5, (strip - 2 * r) / 2.0))
    if r < 1.0:
        raise ValueError("笛の足の先に残る帯が %.1fmm しかなく、＊を彫れない" % strip)
    center_u = np.array([0.0, 0.0, 0.0])
    width = R[:3, :3] @ np.array([0.0, 1.0, 0.0])
    width = width / np.linalg.norm(width)
    cw = (float(v.dot(width).min()) + float(v.dot(width).max())) / 2.0
    # 彫る面は「その笛が埋まっている板の、内側を向く面」である。ホスト全体の最外面を
    # 取ると、反対側の壁の外面に彫ってしまう（一度それで外れた）。笛は窓を面より
    # PROUD だけ出して置いてあるので、笛自身から面の位置を逆算する。
    surf = float(v.dot(win).max()) - PROUD
    pos = axis * (foot + gap + r) + width * cw + win * surf

    poly = stencil.asterisk(0.0, 0.0, r)
    tool = trimesh.creation.extrude_polygon(poly, height=depth + 0.5)
    M = np.eye(4)
    M[:3, 0] = axis
    M[:3, 1] = width
    M[:3, 2] = -win                                    # 内側の面から材料の中へ掘る
    M[:3, 3] = pos + win * 0.5                          # 面から少し外に出してから掘る
    tool.apply_transform(M)
    return trimesh.boolean.difference([host, tool], engine="manifold")


def layout(notes, host, geom, base_only=False):
    """左の壁（上から下）→底板（左から右）→右の壁（下から上）の順に置く。

    コの字を一筆でなぞる順になるので、吹く順番が物の形から分かる。

    base_only=True なら[* 底板だけに置き、壁の縁には置かない]（v3）。壁の縁に垂直に並べた
    笛は、実機で造形不良が多く復号できなかった（2026-07-30、栗原さんの判断）。窓が真上に
    開く底板の笛だけを使い、足りないビット数は本立てを複数刷って足す。
    """
    l_max = mini10.uniform_body_length(
        [mini10.length_for_note(n) for n in mini10.CALIB12])
    if base_only:
        span_base = (geom["right"][0] - MARGIN_X) - (geom["left"][1] + MARGIN_X)
        n_base = len(notes)
        gap_b = (span_base - 7.0 * n_base) / max(1, n_base - 1)
        if gap_b < 0.8:
            raise ValueError("笛%d本は底板（幅%.1fmm）に入らない。隙間が%.2fmmになる"
                             % (n_base, span_base, gap_b))
        xs = np.linspace(geom["left"][1] + MARGIN_X,
                         geom["right"][0] - MARGIN_X - 7.0, n_base) + 3.5
        print("  底板だけに%d本。隣どうしの隙間 %.2fmm（幅 %.1fmm）" % (n_base, gap_b, span_base))
        placed, infos = [], []
        for note, x in zip(notes, xs):
            R, win = R_BASE, [0.0, 0.0, geom["base_top"] + PROUD]
            fl, w = place(note, R, win, l_max)
            fl.apply_translation([x - (fl.bounds[0][0] + fl.bounds[1][0]) / 2, 0, 0])
            placed.append(fl)
            infos.append(dict(note=note, where="base", R=R))
        return placed, infos
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
        raise ValueError("笛%d本は、この本立てには詰め込めない（壁%.0fmm・底板%.0fmm）"
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
        placed.append(fl)
        infos.append(dict(note=note, where=where, R=R))
    return placed, infos


def carve_tool(fl, R, ahead=0.6, out=0.4):
    """彫り抜きに使う道具（笛の凸包を、吸込口の側と窓の側へ少しだけ広げたもの）。

    笛をちょうど面一に置くと、凸包の面と本体の面が同一平面になり、boolean が
    不安定になって彫り残しが出る（実際に36本中23本のボアに材料が残った）。
    道具を吸込口の向きと窓の向きへ少し伸ばして、面がぴったり重ならないようにする。
    伸ばすのは外へ抜ける2方向だけなので、余分に彫れるのは表面のごく薄い層である。
    """
    axis = R[:3, :3] @ np.array([1.0, 0.0, 0.0])
    win = R[:3, :3] @ np.array([0.0, 0.0, 1.0])
    axis = axis / np.linalg.norm(axis)
    win = win / np.linalg.norm(win)
    v = fl.vertices
    pts = np.vstack([v, v - axis * ahead, v + win * out])
    return trimesh.Trimesh(vertices=pts).convex_hull


def engrave_index(host, geom, index, height=3.0, depth=0.8):
    """断片の番号（1〜3）を、正面（吸込口が並ぶ面）の底板の端に彫る。

    2-of-3 のような分け方では「これが何番の断片か」が分からないと復元できない。開始笛の＊は
    「どこから吹くか」を示すためのもので、番号はそれとは別に、正面から読める位置へ数字で入れる。
    底板の前面（厚さ約5mm・幅105mm）は本にも笛にも隠れないので、ここが読みやすい。
    """
    if not index:
        return host
    poly, (w, th) = stencil.text_holes(str(index), height=height, bridge_w=0.9)
    # 文字は複数の島に分かれることがある（MultiPolygon）ので、島ごとに押し出して束ねる
    from shapely.geometry import MultiPolygon
    geoms = list(poly.geoms) if isinstance(poly, MultiPolygon) else [poly]
    parts = [trimesh.creation.extrude_polygon(g, height=depth + 0.5)
             for g in geoms if not g.is_empty and g.area > 0]
    if not parts:
        return host
    tool = trimesh.util.concatenate(parts)
    # 押し出しは +z 方向なので、前面（-y を向く面）へ向けて倒す
    M = _rot([1.0, 0.0, 0.0], -90.0)
    tool.apply_transform(M)
    b = tool.bounds
    # 正面の左端から6mm、底板の厚みの中央へ置く
    shift = np.array([6.0 - b[0][0],
                      depth - b[1][1],
                      (geom["base_top"] - (b[1][2] - b[0][2])) / 2.0 - b[0][2]])
    for part in parts:
        part.apply_transform(M)
        part.apply_translation(shift)
        host = host.difference(part, engine="manifold")
    return host


def build(notes, carve=True, engine="manifold", scale_y=1.0, base_only=False, index=None):
    host = trimesh.load(HOST, force="mesh")
    if scale_y != 1.0:
        host.apply_scale([1.0, scale_y, 1.0])     # 奥行きだけを縮める
    host.apply_translation(-host.bounds[0])
    geom = measure_host(host)
    placed, infos = layout(notes, host, geom, base_only=base_only)

    # 向きの検査（必須）。本立ては使う向き（壁が立った姿勢）のまま刷る。
    for it, fl in zip(infos, placed):
        res = orient_check.check_orientation(R=it["R"])
        it["window_deg"] = round(res.angle_deg, 1)
        it["tilt_deg"] = round(res.tilt_deg, 1)
        if res.verdict != "ok":
            raise ValueError("%s（%s）の向きが %s: %s"
                             % (it["note"], it["where"], res.verdict, res.message))

    body = engrave_star(host, placed[0], infos[0]["R"])
    body = engrave_index(body, geom, index)
    if carve:
        for fl, it in zip(placed, infos):
            body = body.difference(carve_tool(fl, it["R"]), engine=engine)

    sc = trimesh.Scene()
    sc.add_geometry(body, geom_name="bookstand_0.20mm")
    sc.add_geometry(trimesh.util.concatenate(placed), geom_name="flutes_0.08careful")
    return sc, infos, geom


def main(argv=None):
    ap = argparse.ArgumentParser(description="本立てに笛を水平に埋め込む")
    ap.add_argument("--payload", default=None, help="秘密（既定は pass_#26）")
    ap.add_argument("--parity", type=int, default=4, help="RSブロックあたりのパリティ記号数")
    ap.add_argument("--no-carve", action="store_true")
    ap.add_argument("--scale-y", type=float, default=1.0,
                    help="本立ての奥行きの倍率（v2は0.7＝30%%縮小）")
    ap.add_argument("--out", default=os.path.join(OUT, "bookstand_pass26.3mf"))
    ap.add_argument("--base-only", action="store_true",
                    help="底板だけに笛を置く（v3）。壁の縁は造形が不安定なので使わない")
    ap.add_argument("--symbols", default=None,
                    help="記号列を直接載せる（例 0,7,8,2,0,10）。秘密分散の断片を入れるときに使う")
    ap.add_argument("--index", type=int, default=None,
                    help="断片の番号（1〜3）。正面の底板に数字を彫る")
    args = ap.parse_args(argv)

    payload = args.payload.encode() if args.payload else DEMO_PAYLOAD
    with open(CONFIG, encoding="utf-8") as fp:
        base = json.load(fp)
    if args.symbols:
        cfg = cd.CodecConfig(**{**base, **SLOT12, "ecc_parity": args.parity,
                                "mode": "symbols", "no_repeat": True})
        syms = [int(x) for x in args.symbols.replace(",", " ").split()]
        notes = list(cd.encode_symbols(syms, cfg).notes)
        print("記号列 %s（%d個）を載せる" % (",".join(map(str, syms)), len(syms)))
    else:
        cfg = cd.CodecConfig(**{**base, **SLOT12, "ecc_parity": args.parity,
                                "mode": "sequential", "no_repeat": True})
        notes = list(cd.encode(payload, cfg).notes)
        print("秘密 %r（%dbit）" % (payload, len(payload) * 8))
    for i in range(len(notes) - 1):
        assert notes[i] != notes[i + 1], "隣り合う笛が同じ音になっている"
    print("符号化: 12スロット・隣接同音禁止・パリティ%d記号/ブロック → 笛%d本"
          % (args.parity, len(notes)))
    if args.index:
        print("断片の番号 %d を正面の底板に彫る" % args.index)

    if os.path.exists(args.out):
        raise SystemExit("すでにある版を上書きしようとしている: %s（--out を新しくする）" % args.out)
    sc, infos, geom = build(notes, carve=not args.no_carve, scale_y=args.scale_y,
                            base_only=args.base_only, index=args.index)
    os.makedirs(OUT, exist_ok=True)
    sc.export(args.out)
    n = {}
    for it in infos:
        n[it["where"]] = n.get(it["where"], 0) + 1
    if args.base_only:
        print("配置: 底板だけに%d本（左から右へこの順に吹く）" % n.get("base", 0))
        print("向きの検査: %d本すべて ok（窓は%+.0f度＝真上、傾きは全部0度）"
              % (len(infos), infos[0]["window_deg"]))
    else:
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
