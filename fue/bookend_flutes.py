"""本立て（Bent Bookend Organizer）の最上面＝薄板の上端リッジに、暗号笛を鉛直に立てて並べる。

配置（栗原さんの指定・2026-07-24）:
- 笛を鉛直に立てる。管長方向を z 軸に沿わせ、吹き込み口（吸込口・native x=0端）を上（z+）にする。
- 吹き込み口を薄板の上端 z=zmax に面一で揃える。笛は板の面に沿って下（z<zmax）へ伸びる。
- 窓は板に埋まらず外部へ開口するよう回転で向きを調整する。板厚(約2mm)に窓側の一部を埋め、
  窓の開口はモデル中心と反対の外側（cx>=0なら+x、cx<0なら-x）へ露出させる。
- 笛の幅を板の走向（y方向）に沿わせ、上端リッジに沿って等間隔にずらりと並べる。
- carve=True なら笛の凸包で板をポケット状に彫り抜いてから笛を戻し、ボアを中空のまま保つ（スキル flute-embed）。

笛は外見統一版（mini10.uniform_flute）。外形を最長管に揃え、内部の仕切り壁でボア長=音を決めるので、
見た目では音（データ）が分からない。correction_mm は内部壁の音下がり補償で、印刷中の較正コームの
実測が出たら渡す（既定 0）。

128bit を GF(13) で表すには 13^35 >= 2^128 より 35本のデータ笛が要る。基準笛を先頭に1本足すと相対読み。
"""
from __future__ import annotations
import argparse, os, sys
import numpy as np
import trimesh
from trimesh import transformations as tf

sys.path.insert(0, os.path.dirname(__file__))
import mini10

HOST = os.path.join(os.path.dirname(__file__), os.pardir,
                    "temp", "tools", "Bent_Bookend_Organizer.3mf")

# native(窓+z,床z=0,吸込口x=0,長さ+x,幅+y) を立てる回転。
#   窓+x版: native x->world -z(吸込口が上), native y->+y, native z(窓)->+x
R_WIN_PLUS = np.array([[0, 0, 1], [0, 1, 0], [-1, 0, 0]], float)
#   窓-x版: 上を Rz180 したもの（吸込口は上のまま・窓が -x）
R_WIN_MINUS = np.array([[0, 0, -1], [0, -1, 0], [-1, 0, 0]], float)


def load_host(path=HOST, geom_key="3"):
    """元3mfは2プレートに2つの本立てを含む。geom '3'=small_bookshelf=プレート1（1つ目）、
    geom '1'=Large_bookshelf=プレート2。既定はプレート1の本立てだけを使う（融合させない）。
    geom_key=None なら全geometryを結合（非推奨・2つの本立てが融合する）。"""
    s = trimesh.load(path)
    if isinstance(s, trimesh.Scene):
        if geom_key is not None and geom_key in s.geometry:
            g = s.geometry[geom_key].copy()
            g.apply_translation(-g.bounds[0] * [1, 1, 0])   # xyだけ原点寄せ・zは保持
            return g
        return trimesh.util.concatenate([g for g in s.geometry.values()])
    return s


def detect_ridges(host, x_tol=3.0, min_yspan=10.0):
    """z=zmax の上向き上端面を x でクラスタリングし、板の上端リッジ列を返す。
    各リッジは (x中心, その上端に現れる y の昇順配列)。y方向に長い薄板の上辺を1本とみなす。"""
    zmax = host.bounds[1][2]
    tn = host.face_normals
    fc = host.triangles_center
    mask = (tn[:, 2] > 0.99) & (fc[:, 2] >= zmax - 0.5)
    c = fc[mask]
    order = np.argsort(c[:, 0])
    xs = c[order, 0]
    ridges = []
    cur = [order[0]]
    for k in range(1, len(order)):
        if xs[k] - xs[k - 1] <= x_tol:
            cur.append(order[k])
        else:
            ridges.append(cur)
            cur = [order[k]]
    ridges.append(cur)
    out = []
    for cl in ridges:
        cx = float(c[cl, 0].mean())
        ys = np.sort(c[cl, 1])
        if ys[-1] - ys[0] >= min_yspan:
            out.append((cx, ys))
    out.sort(key=lambda r: r[0])   # x昇順（読み順の基準）
    return out, zmax


def _upright(base_flute, cx, y0, zmax, winside, embed_mm=2.0):
    """1本を立てて配置する変換済みメッシュを返す。
    winside=+1: 窓を+xへ露出（板の-x面側に埋込）。winside=-1: 窓を-xへ露出。
    吸込口(上端)を zmax に面一。埋込量 embed_mm 分だけ板に食い込ませる。"""
    g = base_flute.copy()
    g.apply_transform(_mat(R_WIN_PLUS if winside > 0 else R_WIN_MINUS))
    b = g.bounds
    # z: 吸込口(上端)を zmax に
    dz = zmax - b[1][2]
    # y: 幅の手前端を y0 に
    dy = y0 - b[0][1]
    # x: 板厚(約2mm)に embed_mm 埋める。窓露出側と反対の面を板中心 cx から埋込量ぶん内側へ。
    if winside > 0:      # 床(-x側)を板に埋める。床面 xmin を (cx - embed_mm) に
        dx = (cx - embed_mm) - b[0][0]
    else:                # 床(+x側)を板に埋める。床面 xmax を (cx + embed_mm) に
        dx = (cx + embed_mm) - b[1][0]
    g.apply_transform(tf.translation_matrix([dx, dy, dz]))
    return g


def _mat(R3):
    M = np.eye(4)
    M[:3, :3] = R3
    return M


def detect_walls(host, sample_ys=(20, 30, 40, 50, 60), step=0.5):
    """垂直な板の壁を断面 contains で個別に検出する。壁は垂直なので x 位置は z に依らず一定。
    複数の y 断面で材料区間の中心を集め、近い中心をまとめて壁 x 中心のリストを返す。"""
    zmax = host.bounds[1][2]
    x0, x1 = host.bounds[0][0], host.bounds[1][0]
    xs = np.arange(x0, x1 + step, step)
    z = zmax - 1.0
    centers = []
    for sy in sample_ys:
        pts = np.column_stack([xs, np.full_like(xs, sy), np.full_like(xs, z)])
        ins = host.contains(pts)
        a = None
        for i, b in enumerate(ins):
            if b and a is None:
                a = xs[i]
            if (not b) and a is not None:
                centers.append((a + xs[i - 1]) / 2.0)
                a = None
        if a is not None:
            centers.append((a + xs[-1]) / 2.0)
    # 近い中心(±1.5mm)をまとめる
    centers.sort()
    walls = []
    cur = [centers[0]]
    for c in centers[1:]:
        if c - cur[-1] <= 1.5:
            cur.append(c)
        else:
            walls.append(float(np.mean(cur)))
            cur = [c]
    walls.append(float(np.mean(cur)))
    return walls, zmax


def wall_yspan(host, xc, zmax, step=1.0):
    """壁 x=xc に沿って材料のある y 範囲（連続最長区間）を返す。切り欠き・穴は最長区間で代表。"""
    y0, y1 = host.bounds[0][1], host.bounds[1][1]
    ys = np.arange(y0, y1 + step, step)
    z = zmax - 1.0
    pts = np.column_stack([np.full_like(ys, xc), ys, np.full_like(ys, z)])
    ins = host.contains(pts)
    best = (0.0, 0.0, 0.0)
    a = None
    for i, b in enumerate(ins):
        if b and a is None:
            a = ys[i]
        if (not b) and a is not None:
            if ys[i - 1] - a > best[2]:
                best = (a, ys[i - 1], ys[i - 1] - a)
            a = None
    if a is not None and ys[-1] - a > best[2]:
        best = (a, ys[-1], ys[-1] - a)
    return best[0], best[1]


def outer_walls(walls, x_mid, pair_gap=15.0):
    """壁を近接ペア(U溝の2枚)にまとめ、各ペアの外側(モデル中心から遠い方)＝外壁を選ぶ。
    ペアを組めない単独壁はそれ自体を外壁とする。戻り値は外壁 x 中心の昇順リスト。"""
    ws = sorted(walls)
    outers, i = [], 0
    while i < len(ws):
        if i + 1 < len(ws) and ws[i + 1] - ws[i] <= pair_gap:
            a, b = ws[i], ws[i + 1]
            outers.append(a if abs(a - x_mid) >= abs(b - x_mid) else b)
            i += 2
        else:
            outers.append(ws[i])
            i += 1
    return sorted(outers)


def _even_positions(ymin, ymax, k, width, margin):
    """[ymin,ymax] の内側に k 本の笛(幅width)を等間隔で置くときの、各笛の手前端 y を返す。"""
    lo, hi = ymin + margin, ymax - margin
    if k <= 0:
        return []
    if k == 1:
        return [(lo + hi - width) / 2.0]
    step = ((hi - lo) - width) / (k - 1)
    return [lo + j * step for j in range(k)]


def layout(count, reference=True, correction_mm=0.0, host_path=HOST, uniform_window=True,
           gap_mm=3.0, margin_mm=6.0, embed_mm=2.0, notes=None, geom_key="3", slots=13):
    """必要本数を上端リッジに沿って配置。戻り値 (host, placed[list mesh], infos[list dict])。
    notes 未指定なら音セット(slots=13→CALIB13 / 11→CALIB11)を巡回した見本音列（外見統一なので
    配置プレビュー用）。geom_key 既定 '3'＝プレート1の small_bookshelf のみ使う。"""
    host = load_host(host_path, geom_key=geom_key)
    x_mid = (host.bounds[0][0] + host.bounds[1][0]) / 2.0   # 窓を外向きにする基準
    walls, zmax = detect_walls(host)
    walls = sorted(walls)                  # 内壁・外壁すべて使う（x昇順＝読み順）
    n_total = count + (1 if reference else 0)
    calib = mini10.CALIB11 if slots == 11 else mini10.CALIB13
    if notes is None:
        data_notes = [calib[i % len(calib)] for i in range(count)]
    else:
        data_notes = list(notes)
    seq = (["C7"] if reference else []) + data_notes    # 先頭=基準笛
    seq = seq[:n_total]

    # 外形は使う音のうち最長管(=最低音)に統一
    Ls = [mini10.length_for_note(n) for n in seq]
    L_max = mini10.uniform_body_length(Ls)
    sample = mini10.uniform_flute(max(Ls), L_max=L_max, correction_mm=correction_mm)
    width = sample.bounds[1][1] - sample.bounds[0][1]

    # 各壁の使える y 範囲（両端 margin を除く）。全壁で共通の一定ピッチ p を、
    # 全 n_total 本が全壁に行き渡るように二分探索で決める（p を大きくすると総数が減る）。
    spans = [wall_yspan(host, cx, zmax) for cx in walls]
    usable = [max(0.0, (y1 - margin_mm) - (y0 + margin_mm)) for (y0, y1) in spans]

    def k_of(u, p):
        return 0 if u < width else int((u - width) / p + 1e-9) + 1

    lo, hi = width + gap_mm, max(usable) + 1.0    # 下限=最小ピッチ, 上限=1壁1本
    for _ in range(60):
        mid = (lo + hi) / 2.0
        if sum(k_of(u, mid) for u in usable) >= len(seq):
            lo = mid
        else:
            hi = mid
    pitch = lo
    ks = [k_of(u, pitch) for u in usable]
    # 超過分は本数の多い壁の末尾から1本ずつ間引く（各壁は端からpitch詰めなので間隔は不変）
    over = sum(ks) - len(seq)
    order = sorted(range(len(ks)), key=lambda i: -ks[i])
    j = 0
    while over > 0:
        i = order[j % len(order)]
        if ks[i] > 0:
            ks[i] -= 1
            over -= 1
        j += 1

    placed, infos = [], []
    si = 0
    for wi, cx in enumerate(walls):
        if si >= len(seq):
            break
        y0, y1 = spans[wi]
        # 窓の向きは全本そろえる（2026-07-28）。以前はモデル中心より外側へ向けていたが、
        # 向きが2種類できて印刷向きの検査が煩雑になるうえ、揃える利点のほうが大きい。
        # 板の厚みは約2mmで隣の板とは10mm以上あくので、どちら側を向いても窓の前は空気である。
        winside = +1 if uniform_window else (+1 if cx >= x_mid else -1)
        y = y0 + margin_mm
        for _ in range(ks[wi]):
            if si >= len(seq):
                break
            note = seq[si]
            L = mini10.length_for_note(note)
            fl = mini10.uniform_flute(L, L_max=L_max, correction_mm=correction_mm)
            if reference and si == 0:
                fl = mini10.reference_tab(fl)   # 基準笛の印（吸込口脇のタブ）
            g = _upright(fl, cx, y, zmax, winside, embed_mm=embed_mm)
            placed.append(g)
            infos.append(dict(idx=si,
                              role=("基準" if (reference and si == 0) else "データ"),
                              note=note, L=round(L, 1), wall=wi,
                              x=round(cx, 1), y=round(y, 1),
                              win=("+x" if winside > 0 else "-x")))
            si += 1
            y += pitch
    return host, placed, infos, (si, len(seq))


def carve(host, placed, engine="manifold"):
    body = host
    for g in placed:
        body = body.difference(g.convex_hull, engine=engine)
    return body


# 通常の本立として使う向きへ全体を起こす回転。x軸まわりに+90度で
#   もとのy（仕切りの背丈）→ +z（高さ）、もとのz（押し出し120mm）→ -y（奥行き）。
# これで仕切りの上端が真上を向き、[* 笛の長軸が水平になる]（もとのzに沿っていたため）。
# 窓はもとの±xのまま水平を向くので、印刷向きは±90度＝2026-07-27に実機で確かめた範囲に入る。
R_UPRIGHT = np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]], float)


def to_upright(meshes):
    """本立てと笛をまとめて、通常の使用向きへ起こす。ベッド(z=0)へ落とす。"""
    M = _mat(R_UPRIGHT)
    for m in meshes:
        m.apply_transform(M)
    zmin = min(m.bounds[0][2] for m in meshes)
    ymin = min(m.bounds[0][1] for m in meshes)
    xmin = min(m.bounds[0][0] for m in meshes)
    for m in meshes:
        m.apply_transform(tf.translation_matrix([-xmin, -ymin, -zmin]))
    return meshes


def flute_orientation(winside, upright):
    """配置した笛の回転行列を返す。印刷向きの検査 orient_check へ渡すためのもの。"""
    R = R_WIN_PLUS if winside > 0 else R_WIN_MINUS
    return (R_UPRIGHT @ R) if upright else R


def build_scene(host, placed, infos, carve_body=True):
    body = carve(host, placed) if carve_body else host
    sc = trimesh.Scene()
    sc.add_geometry(body, geom_name="bookend_0.20mm")
    for g, it in zip(placed, infos):
        sc.add_geometry(g, geom_name="f%02d_%s_%s_0.08careful" %
                        (it["idx"], it["role"], it["note"].replace("#", "s")))
    return sc, body


def verify_cavity(placed, combined, correction_mm=0.0):
    """各笛のボア中心が combined の外（中空）かを確認。全 True なら埋まっていない。"""
    ok = []
    for g in placed:
        # nativeボア中心 (L/2, W/2, 中庸高さ) を、この笛の実変換で世界座標へ
        b0 = g.bounds
        p = g.centroid.copy()          # 立てた笛の重心≒ボア近傍（殻の中心）
        inside = combined.contains([p])[0]
        ok.append(not bool(inside))
    return ok


def main(argv=None):
    ap = argparse.ArgumentParser(description="本立て上端リッジへ暗号笛を鉛直配置")
    ap.add_argument("--count", type=int, default=0, help="データ笛の本数（0=体系ごとの128bit本数。13音は35, 11音は38）")
    ap.add_argument("--flat", action="store_true",
                    help="通常の使用向きへ起こさず、もとの寝かせた向きのまま出す（笛が縦置きになるので非推奨）")
    ap.add_argument("--slots", type=int, default=13, choices=(11, 13),
                    help="スロット体系（13=F#6..F#7/GF13, 11=G#6..F#7/GF11・低音2音除く安定版）")
    ap.add_argument("--no-reference", action="store_true", help="先頭の基準笛を付けない（絶対音程）")
    ap.add_argument("--correction", type=float, default=0.0, help="内部壁の音下がり補償[mm]（実測後に指定）")
    ap.add_argument("--gap", type=float, default=3.0, help="笛どうしの隙間[mm]")
    ap.add_argument("--embed", type=float, default=2.0, help="板への埋込量[mm]")
    ap.add_argument("--no-carve", action="store_true", help="彫り抜かず重ね置き（高速・確認用）")
    ap.add_argument("--multiobj", action="store_true", help="本体と笛を別オブジェクトで出力")
    ap.add_argument("--verify", action="store_true", help="ボア中空を確認")
    ap.add_argument("--geom", default="3", help="使う本立て geometry ('3'=プレート1 small, '1'=プレート2 large)")
    ap.add_argument("--out", required=True, help="出力3mf")
    args = ap.parse_args(argv)

    count = args.count if args.count > 0 else (38 if args.slots == 11 else 35)
    host, placed, infos, (placed_n, need_n) = layout(
        count, reference=not args.no_reference,
        correction_mm=args.correction, gap_mm=args.gap, embed_mm=args.embed,
        geom_key=args.geom, slots=args.slots)

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)

    # 通常の本立として使う向きへ起こす（既定）。これで笛の長軸が水平になる。
    upright = not args.flat
    if upright:
        to_upright([host] + placed)

    # 印刷向きの検査（2026-07-28に実機で確定した範囲に入っているか）
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import orient_check as oc
    checks = [("f%02d %s" % (it["idx"], it["note"]),
               dict(R=flute_orientation(+1 if it["win"] == "+x" else -1, upright)))
              for it in infos]
    results = oc.check_many(checks)
    bad = [(n, r) for n, r in results if r.verdict != "ok"]
    kinds = sorted({(r.verdict, round(r.angle_deg), round(r.tilt_deg)) for _, r in results})
    print("印刷向きの検査: %d本中 ok %d本" % (len(results), len(results) - len(bad)))
    for vd, ang, tl in kinds:
        n = sum(1 for _, r in results
                if (r.verdict, round(r.angle_deg), round(r.tilt_deg)) == (vd, ang, tl))
        print("   %-8s 窓の角度 %+4d度 / 長軸の傾き %2d度 … %d本" % (vd, ang, tl, n))
    if bad:
        print("   [注意] 検証していない向きの笛がある。1本目: %s" % bad[0][1].message)

    if args.multiobj:
        sc, body = build_scene(host, placed, infos, carve_body=not args.no_carve)
        sc.export(args.out)
        combined = trimesh.util.concatenate([body] + placed)
    else:
        body = carve(host, placed) if not args.no_carve else host
        combined = trimesh.util.concatenate([body] + placed)
        combined.export(args.out)

    print("配置: %d/%d 本（%d音体系・データ%d＋基準%d）を上端リッジに立てた。carve=%s"
          % (placed_n, need_n, args.slots, count, 0 if args.no_reference else 1, not args.no_carve))
    if placed_n < need_n:
        print("  [注意] 上端リッジに収まったのは %d 本。残り %d 本は場所が足りない。"
              % (placed_n, need_n - placed_n))
    for it in infos[:6] + ([{"idx": "…"}] if len(infos) > 8 else []) + infos[-2:]:
        if it.get("idx") == "…":
            print("   …")
        else:
            print("  f%02d %-4s %-4s L=%5.1f  x=%6.1f y=%6.1f 窓%s"
                  % (it["idx"], it["role"], it["note"], it["L"], it["x"], it["y"], it["win"]))
    print("  出力 -> %s  （本体 z=%.0f 面一, watertight(body)=%s）"
          % (args.out, host.bounds[1][2], body.is_watertight))
    if args.verify:
        ok = verify_cavity(placed, combined, correction_mm=args.correction)
        print("  ボア中空(重心が中空): %d/%d 本 True" % (sum(ok), len(ok)))


if __name__ == "__main__":
    main()
