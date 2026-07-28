"""カップル用キーホルダー（Portachiavi）の片割れ2つに、笛を2本ずつ埋め込む。

ホストは temp/tools/Portachiavi.3mf。厚さ5mmの板が2枚で、合わせると1枚になる。
上にキーリングの穴、下にハート形の抜きがあり、この2つが笛の通り道をふさぐ。

置き方の考え方。

  [* 笛は板の中に寝かせて、長さの方向（板の長手）に通す]。板を平らに置いて刷るので、
  笛の長軸は水平・窓は真上（0度）になり、実機で確かめた向きのいちばん良いところに入る。

  [* 窓は板の表の面へ開く]。板の厚みは5mm×拡大率で、笛の厚み4mmを引いた残りが裏に残る。

  [* 吸込口は板の外形より少し前へ出す]。板の上下は丸まっているので、笛の端をちょうど
  縁に合わせることができない。1mm出しておけば、丸みのどこであっても必ず空気に開く。

  [* キーリングの穴とハートの抜きを避ける]。幅7mmの帯が材料の中をまっすぐ通せる場所を
  実測で探し、重ならない2本を選ぶ。

音は高い側だけを使う。管が短くなるので板を大きくしすぎずに済む。既定は D7〜G7 の6音で、
笛の外形長は50.5mmになる（12音すべてを使うと66mmになり、板を2.2倍にしないと入らない）。

基準笛は置かない。2本しかないので、1本を基準に使うと運べる情報が半分になるためである。
そのぶん、読むときは温度と息の強さの影響を受ける。

笛2本ずつを、左右に1.2mmの肉厚を残して入れるのに要る拡大率は次のとおりである。
    4音(E7〜G7)  笛50.5mm→46.4mm  1.9倍  片割れ 34×89×10 と 23×89×9 mm  秘密は0〜15
    6音(D7〜G7)  笛50.5mm         2.1倍  片割れ 38×99×11 と 25×99×10 mm 秘密は0〜35
    12音(G#6〜G7) 笛66.0mm        2.4倍  片割れ 44×113×12 と 29×113×12 mm 秘密は0〜143

使い方:
    python3 fue/keychain_flutes.py                          # 既定（2.1倍・6音・各2本）
    python3 fue/keychain_flutes.py --scale 1.9 --notes 4    # 小さめの版
    python3 fue/keychain_flutes.py --scale 2.4 --notes 12   # 情報を増やした版
"""
from __future__ import annotations
import argparse
import os
import sys

import numpy as np
import trimesh
from trimesh import transformations as tf

sys.path.insert(0, os.path.dirname(__file__))
import mini10
import orient_check

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)
OUT = os.path.join(ROOT, "out")
HOST = os.path.join(ROOT, "temp", "tools", "Portachiavi.3mf")

# 高い側の6音。管が短いので小さな板に収まる。見た目は互いに同じ（外見統一）。
NOTES6 = ["D7", "D#7", "E7", "F7", "F#7", "G7"]

FLUTE_W = 7.0        # 笛の幅[mm]
MOUTH_OUT = 1.0      # 吸込口を板の外形より前へ出す量[mm]
BACK_WALL = 1.0      # 笛の裏に残す板の厚み[mm]
GAP = 1.0            # 笛どうしの隙間[mm]
SIDE_WALL = 1.2      # 笛の左右に残す板の肉厚[mm]


def halves(scale):
    """2つの片割れを、指定の倍率で拡大して返す。"""
    sc = trimesh.load(HOST)
    out = []
    for key in ("1", "3"):
        m = sc.geometry[key].copy()
        m.apply_scale(scale)
        m.apply_translation(-m.bounds[0])
        out.append((key, m))
    return out


def find_bands(plate, body, width=FLUTE_W + 2 * SIDE_WALL, step_x=0.25, step_y=0.4):
    """幅 width の帯が材料の中をまっすぐ（板の長手＝y方向に）通せる場所を実測で探す。

    帯は笛の幅に左右の肉厚を足した幅で探し、笛はその中央に置く。縁ぎりぎりに寄せると
    板が薄い殻になってしまうためである。戻り値は (長さ, 帯の左端x, 材料が始まるy,
    材料が終わるy) の一覧を長い順に並べたもの。キーリングの穴やハートの抜きは材料では
    ないので、自動的に避けられる。
    """
    b = plate.bounds
    zc = (b[0][2] + b[1][2]) / 2.0
    xs = np.arange(0.0, b[1][0] - width, step_x)
    ys = np.arange(0.0, b[1][1], step_y)
    X, Y = np.meshgrid(np.arange(0.0, b[1][0], step_x), ys, indexing="ij")
    ins = plate.contains(np.column_stack(
        [X.ravel(), Y.ravel(), np.full(X.size, zc)])).reshape(X.shape)
    nw = int(round(width / step_x))
    found = []
    for i in range(len(xs)):
        band = ins[i:i + nw].all(axis=0)
        run_s = run_len = best = best_s = 0
        for j, v in enumerate(band):
            if v:
                if run_len == 0:
                    run_s = j
                run_len += 1
                if run_len > best:
                    best, best_s = run_len, run_s
            else:
                run_len = 0
        if best * step_y >= body:
            found.append((best * step_y, xs[i], ys[best_s], ys[best_s + best - 1]))
    found.sort(reverse=True)
    return found


def pick_two(found, width=FLUTE_W + 2 * SIDE_WALL, gap=GAP):
    """重ならない帯を2本選ぶ。長いものから、間隔が空くように取る。"""
    picked = []
    for L, x0, y0, y1 in found:
        if all(abs(x0 - p[1]) >= width + gap for p in picked):
            picked.append((L, x0, y0, y1))
        if len(picked) == 2:
            break
    return picked


# 板を平らに置いたときの笛の向き。長軸を +y、窓を +z（表の面）へ。
R_FLAT = tf.rotation_matrix(np.radians(90), [0, 0, 1])


def place(note, plate, band, l_max):
    """1本を帯へ置く。吸込口は材料が始まる少し手前（空気の側）に出す。"""
    _, x0, y0, _ = band
    fl = mini10.uniform_flute(mini10.length_for_note(note), L_max=l_max)
    fl.apply_transform(R_FLAT)
    b = plate.bounds
    top = b[1][2]
    d = np.array([(x0 + SIDE_WALL) - fl.bounds[0][0],
                  (y0 - MOUTH_OUT) - fl.bounds[0][1],
                  (top - (fl.bounds[1][2] - fl.bounds[0][2])) - fl.bounds[0][2]])
    fl.apply_translation(d)
    return fl


def carve_tool(fl, ahead=0.8, out=0.4):
    """彫り抜きの道具。吸込口の向きと窓の向きへ少し広げ、面の重なりを避ける。"""
    v = fl.vertices
    pts = np.vstack([v, v - np.array([0, ahead, 0]), v + np.array([0, 0, out])])
    return trimesh.Trimesh(vertices=pts).convex_hull


def build(notes_per_half, scale=1.8, note_set=None, carve=True, engine="manifold"):
    """片割れ2つに笛を埋め込み、横に並べた Scene を返す。"""
    note_set = note_set or NOTES6
    l_max = mini10.uniform_body_length(
        [mini10.length_for_note(n) for n in note_set])
    sc = trimesh.Scene()
    infos = []
    xcursor = 0.0
    for (key, plate), notes in zip(halves(scale), notes_per_half):
        found = find_bands(plate, l_max)
        bands = pick_two(found)
        if len(bands) < len(notes):
            raise ValueError("片割れ '%s' に幅%.1fmm・長さ%.1fmmの帯が%d本しか取れない"
                             % (key, FLUTE_W + 2 * SIDE_WALL, l_max, len(bands)))
        bands.sort(key=lambda b: b[1])          # 左から右の順に吹く
        placed = []
        for note, band in zip(notes, bands):
            fl = place(note, plate, band, l_max)
            res = orient_check.check_orientation(R=R_FLAT)
            if res.verdict != "ok":
                raise ValueError("向きが %s: %s" % (res.verdict, res.message))
            placed.append(fl)
            infos.append(dict(half=key, note=note, x=round(band[1], 1),
                              window_deg=round(res.angle_deg, 1),
                              tilt_deg=round(res.tilt_deg, 1)))
        body = plate
        if carve:
            for fl in placed:
                body = body.difference(carve_tool(fl), engine=engine)
        shift = tf.translation_matrix([xcursor - body.bounds[0][0], 0, 0])
        body.apply_transform(shift)
        sc.add_geometry(body, geom_name="keychain_%s_0.20mm" % key)
        merged = trimesh.util.concatenate(placed)
        merged.apply_transform(shift)
        sc.add_geometry(merged, geom_name="flutes_%s_0.08careful" % key)
        xcursor = body.bounds[1][0] + 8.0
    return sc, infos


def main(argv=None):
    ap = argparse.ArgumentParser(description="キーホルダーの片割れ2つに笛を2本ずつ埋め込む")
    ap.add_argument("--scale", type=float, default=2.1, help="板の拡大率（6音なら2.1倍で2本ずつ入る）")
    ap.add_argument("--notes", default="6", help="使う音の数（6=D7〜G7 / 12=G#6〜G7）")
    ap.add_argument("--secret", type=int, default=19, help="デモの秘密（0〜35の整数）")
    ap.add_argument("--no-carve", action="store_true")
    ap.add_argument("--out", default=os.path.join(OUT, "keychain_pair.3mf"))
    args = ap.parse_args(argv)

    note_set = {"4": ["E7", "F7", "F#7", "G7"], "6": NOTES6}.get(args.notes, mini10.CALIB12)
    m = len(note_set)
    if not 0 <= args.secret < m * m:
        raise SystemExit("秘密は0から%dまでで指定する" % (m * m - 1))

    # 2-of-2 の秘密分散。片割れだけでは何も分からず、2つ合わせて初めて秘密が出る。
    # 片割れAに乱数 r、片割れBに (秘密 - r) mod m^2 を、それぞれ2桁の m 進数で入れる。
    rnd = {4: 5, 6: 7}.get(m, 41)                # 記録のため決め打ちのデモ値
    share_a, share_b = rnd % (m * m), (args.secret - rnd) % (m * m)
    to_notes = lambda v: [note_set[v // m], note_set[v % m]]
    notes_per_half = [to_notes(share_a), to_notes(share_b)]

    print("デモの秘密 %d（0〜%d）を2つに分けた" % (args.secret, m * m - 1))
    print("  片割れ1 の笛: %s（値 %d）" % (" ".join(notes_per_half[0]), share_a))
    print("  片割れ3 の笛: %s（値 %d）" % (" ".join(notes_per_half[1]), share_b))
    print("  片方だけでは秘密は分からない（もう片方が乱数の役をする）")

    sc, infos = build(notes_per_half, scale=args.scale, note_set=note_set,
                      carve=not args.no_carve)
    os.makedirs(OUT, exist_ok=True)
    sc.export(args.out)
    for it in infos:
        print("  片割れ%s %-4s 帯の左端 x=%.1f  窓%+.0f度・傾き%.0f度"
              % (it["half"], it["note"], it["x"], it["window_deg"], it["tilt_deg"]))
    print("外形 %s mm -> %s" % (np.round(sc.bounds[1] - sc.bounds[0], 1),
                               os.path.relpath(args.out, ROOT)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
