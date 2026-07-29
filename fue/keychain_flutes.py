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
SINK = 0.3           # 笛を板の上面へどれだけ沈めるか[mm]（融合させるため）


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


def fill_heart(plate, frac=0.5):
    """ハートの抜きを、板の[* 上半分だけ]埋める。

    笛を下の縁にそろえて並べるとハートの抜きを横切るので、そのままでは笛の下に材料が
    無くなる。上半分（笛が入る側）を埋め、下半分は残す。表からは平らになり、裏からは
    深さ半分のくぼみ＝彫刻として見える。キーリングの穴は埋めない（紐を通すため）。

    輪郭は断面から取るが、to_planar が返す2D座標はワールドとずれるので、必ず一緒に
    返る変換行列で3Dへ戻す（スキルの注意どおり）。
    """
    from shapely.geometry import Polygon
    b = plate.bounds
    zc = (b[0][2] + b[1][2]) / 2.0
    sec = plate.section(plane_origin=[0, 0, zc], plane_normal=[0, 0, 1])
    planar, to_3D = sec.to_planar()
    rings = [r for poly in planar.polygons_full for r in poly.interiors]
    if not rings:
        return plate
    # ワールドでのyが低い方＝ハート（高い方はキーリングの穴）
    def world_y(ring):
        pts = np.array([[p[0], p[1], 0.0, 1.0] for p in ring.coords])
        return float((pts @ to_3D.T)[:, 1].mean())
    heart = min(rings, key=world_y)
    thick = b[1][2] - b[0][2]
    tool = trimesh.creation.extrude_polygon(Polygon(heart), height=thick * frac)
    tool.apply_transform(to_3D)
    # 上面をぴったり合わせて上半分に置く（外形を変えないため）
    tool.apply_translation([0, 0, b[1][2] - tool.bounds[1][2]])
    return trimesh.boolean.union([plate, tool], engine="manifold")


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


def support_map(plate, l_max, width=FLUTE_W, step_x=0.5, step_y=0.5):
    """帯の左端xごとに、笛を[* 上面に乗せられる]いちばん低い開始yを返す。

    上に乗せるので、笛の真下に材料が笛の長さぶん続いていなければならない。
    ハートの抜きは fill_heart で上半分を埋めてあるので、そこも乗せられる。
    """
    b = plate.bounds
    ztop = b[1][2] - 0.5
    xs = np.arange(0.0, b[1][0], step_x)
    ys = np.arange(0.0, b[1][1], step_y)
    X, Y = np.meshgrid(xs, ys, indexing="ij")
    ins = plate.contains(np.column_stack(
        [X.ravel(), Y.ravel(), np.full(X.size, ztop)])).reshape(X.shape)
    nw = int(round(width / step_x))
    out = {}
    for i in range(len(xs) - nw):
        band = ins[i:i + nw].all(axis=0)
        cur = 0
        start = None
        found = None
        for j, v in enumerate(band):
            if v:
                if cur == 0:
                    start = ys[j]
                cur += 1
                if cur * step_y >= l_max and found is None:
                    found = start
            else:
                cur = 0
        out[round(xs[i], 2)] = found
    return out


def layout_on_top(plate, notes, l_max, gap=GAP):
    """笛を板の上面に乗せて横に並べる。彫り抜かないので、ボアが埋まる心配が無い。

    x は、2本とも真下に材料がある帯の組み合わせから選ぶ（同じなら左へ寄せる。板の
    基幹部に載せるため）。y は[* 板の下の縁にそろえる]。板の下側が継ぎ手の曲線で
    削れている片割れでは、笛の一部がハートの抜きや板の外へ張り出すことになるが、
    上に乗せる形なので発音そのものには影響しない（張り出した部分は宙に浮く）。
    """
    sm = support_map(plate, l_max)
    xs = sorted(sm)
    n = len(notes)
    best = None
    for x0 in xs:
        cand = [round(x0 + k * (FLUTE_W + gap), 2) for k in range(n)]
        vals = [sm.get(min(sm, key=lambda t: abs(t - c))) for c in cand]
        if any(v is None for v in vals):
            continue
        if cand[-1] + FLUTE_W > plate.bounds[1][0]:
            continue
        score = (max(vals), x0)
        if best is None or score < best[0]:
            best = (score, cand, max(vals))
    if best is None:
        raise ValueError("笛%d本を乗せられる場所が無い" % n)
    _, cand, _ = best
    # y は下の縁にそろえる。帯ごとに材料が始まる高さが違うので、早い方に合わせる。
    ys = np.arange(0.0, plate.bounds[1][1], 0.2)
    zc = (plate.bounds[0][2] + plate.bounds[1][2]) / 2.0
    starts = []
    for x0 in cand:
        xs2 = np.linspace(x0 + 0.4, x0 + FLUTE_W - 0.4, 5)
        first = 0.0
        for y in ys:
            pts = np.column_stack([xs2, np.full_like(xs2, y), np.full_like(xs2, zc)])
            if plate.contains(pts).all():
                first = y
                break
        starts.append(first)
    y0 = min(starts) - MOUTH_OUT
    ztop = plate.bounds[1][2]
    placed = []
    for note, x0 in zip(notes, cand):
        fl = mini10.uniform_flute(mini10.length_for_note(note), L_max=l_max)
        fl.apply_transform(R_FLAT)
        # 面がぴったり接するだけだと融合が心もとないので、少しだけ沈める。
        # 笛の床は0.5mm厚なので、0.3mm沈めてもボアには届かない。
        fl.apply_translation([x0 - fl.bounds[0][0], y0 - fl.bounds[0][1],
                              (ztop - SINK) - fl.bounds[0][2]])
        placed.append(fl)
    return placed, y0


def layout_bottom(plate, notes, l_max, gap=GAP):
    """笛を板の下の縁にそろえて横に並べる。

    ハートの抜きは fill_heart で上半分を埋めてあるので、そこを横切ってよい。
    2本の吸込口は[* 同じ高さにそろえる]。板の下端は丸いので、材料が始まる高さは帯ごとに
    違う。早い方に合わせる（遅い方に合わせると、早い方の吸込口が材料に埋まる）。
    """
    b = plate.bounds
    zc = (b[0][2] + b[1][2]) / 2.0
    xc = (b[0][0] + b[1][0]) / 2.0
    n = len(notes)
    span = n * FLUTE_W + (n - 1) * gap
    x_left = xc - span / 2.0
    ys = np.arange(0.0, b[1][1], 0.2)
    starts = []
    for k in range(n):
        x0 = x_left + k * (FLUTE_W + gap)
        xs = np.linspace(x0 + 0.4, x0 + FLUTE_W - 0.4, 5)
        first = 0.0
        for y in ys:
            pts = np.column_stack([xs, np.full_like(xs, y), np.full_like(xs, zc)])
            if plate.contains(pts).all():
                first = y
                break
        starts.append(first)
    # 2本の吸込口をそろえる。材料が始まるのが[* 早い方]に合わせる。遅い方に合わせると、
    # 早い方の吸込口が材料の中に埋まって塞がる（実際にそれで4mm被った）。
    y_mouth = min(starts) - MOUTH_OUT
    placed = []
    for k, note in enumerate(notes):
        x0 = x_left + k * (FLUTE_W + gap)
        fl = mini10.uniform_flute(mini10.length_for_note(note), L_max=l_max)
        fl.apply_transform(R_FLAT)
        d = np.array([x0 - fl.bounds[0][0],
                      y_mouth - fl.bounds[0][1],
                      (b[1][2] - (fl.bounds[1][2] - fl.bounds[0][2])) - fl.bounds[0][2]])
        fl.apply_translation(d)
        placed.append(fl)
    return placed, y_mouth


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
        plate = fill_heart(plate)               # ハートの上半分を埋めてから乗せる
        placed, y_mouth = layout_on_top(plate, notes, l_max)
        for note, fl in zip(notes, placed):
            res = orient_check.check_orientation(R=R_FLAT)
            if res.verdict != "ok":
                raise ValueError("向きが %s: %s" % (res.verdict, res.message))
            infos.append(dict(half=key, note=note, x=round(fl.bounds[0][0], 1),
                              y_mouth=round(y_mouth, 1),
                              window_deg=round(res.angle_deg, 1),
                              tilt_deg=round(res.tilt_deg, 1)))
        # 上に乗せるので彫り抜かない。笛の床がそのまま板の上面に接する。
        body = plate
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
