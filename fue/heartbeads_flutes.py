"""HeartBeads（ハート型ビーズのかたわれ2つ）に、暗号笛を埋め込む。

- 元モデル temp/tools/HeartBeads.3mf は geom '1'(右半分)・'3'(左半分)。組むとハート。各かたわれは
  厚さ約7mmの板状で、中央に縦(z方向)の円筒穴(径約5mm)がある。
- 笛(mini10)はそのままでは入らないので、かたわれを scale 倍に拡大して使う。
- 各かたわれに最大2本の笛を、中央の円筒穴を挟んで対向させて立てる:
    ・1本目は穴の -y 壁に沿わせ、窓を穴の内側(+y)へ開口。
    ・2本目は穴の +y 壁に沿わせ、z軸まわり180度回して、窓を穴の内側(-y)へ開口。
  どちらも吹き込み口をハート上端(z+端)に揃え、笛本体はハート内に収める。穴に息を吹き込むと鳴る。
- carve=True なら笛の凸包でビーズにポケットを彫ってから笛を戻す(ボアが中空。スキル flute-embed)。
- geom '3' は非watertightなので open3d の fill_holes ＋ trimesh の向き修正で、元メッシュの滑らかさを
  保ったまま水密化する。
- 2つのかたわれを1つの3mfにまとめて出力する（横に並べる。本体と各笛は別オブジェクト）。
"""
from __future__ import annotations
import argparse, os, sys
import numpy as np
import trimesh

sys.path.insert(0, os.path.dirname(__file__))
import mini10
import orient_check

HEART = os.path.join(os.path.dirname(__file__), os.pardir, "temp", "tools", "HeartBeads.3mf")

# native(窓+z,床z=0,吸込口x=0,長さ+x,幅+y) を立てる基本回転
_R = np.eye(4); _R[:3, :3] = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], float)
_RZ = np.eye(4); _RZ[:3, :3] = np.array([[-1, 0, 0], [0, -1, 0], [0, 0, 1]], float)  # z軸180
_RX = np.eye(4); _RX[:3, :3] = np.array([[1, 0, 0], [0, -1, 0], [0, 0, -1]], float)  # x軸180
R3 = _RX @ _RZ @ _R    # 1本目: 窓→+y(穴の内側), 吸込口→z上, 長さ→+z
R4 = _RZ @ R3          # 2本目: R3をz軸180 → 窓→-y(穴の内側・対向), 吸込口→z上


def _rz(deg):
    th = np.radians(deg); c, s = np.cos(th), np.sin(th)
    M = np.eye(4); M[:3, :3] = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]], float)
    return M


# 円筒穴の壁への割り当て: (回転, 寄せる軸, 符号)。最大4本を ±y, ±x の十字に配置する。
WALLS = [(R3, 'y', -1), (R4, 'y', +1), (_rz(-90) @ R3, 'x', -1), (_rz(90) @ R3, 'x', +1)]


def load_halves(path=HEART):
    s = trimesh.load(path)
    return s.geometry['1'].copy(), s.geometry['3'].copy()


def repair_watertight(mesh):
    """非watertightなメッシュを、元の三角形を保ったまま水密化する（滑らかさ維持）。"""
    if mesh.is_watertight:
        return mesh
    import open3d as o3d
    m = o3d.geometry.TriangleMesh(o3d.utility.Vector3dVector(mesh.vertices),
                                  o3d.utility.Vector3iVector(mesh.faces))
    m.remove_duplicated_vertices(); m.remove_duplicated_triangles()
    m.remove_degenerate_triangles(); m.remove_non_manifold_edges()
    filled = o3d.t.geometry.TriangleMesh.from_legacy(m).fill_holes().to_legacy()
    g = trimesh.Trimesh(np.asarray(filled.vertices), np.asarray(filled.triangles), process=True)
    for fn in ("fix_winding", "fix_inversion", "fix_normals"):
        getattr(trimesh.repair, fn)(g)
    g.merge_vertices(); g.remove_unreferenced_vertices()
    return g


def measure_hole(bead):
    """拡大済みビーズ中央の縦穴(円筒)の world 中心(cx,cy)と半径 r を実測する。"""
    b = bead.bounds
    zc = (b[0][2] + b[1][2]) / 2
    xs = np.arange(b[0][0] + 0.5, b[1][0], 0.5)
    ys = np.arange(b[0][1] + 0.25, b[1][1], 0.5)
    X, Y = np.meshgrid(xs, ys)
    ins = bead.contains(np.column_stack([X.ravel(), Y.ravel(), np.full(X.size, zc)])).reshape(X.shape)
    hx, hy = [], []
    for i in range(len(ys)):
        for j in range(len(xs)):
            if (not ins[i, j] and ins[i, :j].any() and ins[i, j + 1:].any()
                    and ins[:i, j].any() and ins[i + 1:, j].any()):
                hx.append(xs[j]); hy.append(ys[i])
    hx, hy = np.array(hx), np.array(hy)
    return hx.mean(), hy.mean(), ((hx.max() - hx.min()) + (hy.max() - hy.min())) / 4.0


def _place_flute(note, cx, cy, r, btop, R, axis, sign, fuse):
    """1本の笛を穴の壁へ寄せて配置する。axis='y'/'x'、sign=-1/+1 で 4方向を指定。"""
    fl = mini10.flute(mini10.length_for_note(note))
    fl.apply_transform(R)
    fb = fl.bounds
    dz = btop - fb[1][2]                # 吸込口(z最大)をビーズ上端へ
    if axis == 'y':
        dx = cx - (fb[0][0] + fb[1][0]) / 2.0
        dy = (cy + sign * (r + fuse)) - (fb[0][1] if sign < 0 else fb[1][1])
    else:
        dy = cy - (fb[0][1] + fb[1][1]) / 2.0
        dx = (cx + sign * (r + fuse)) - (fb[0][0] if sign < 0 else fb[1][0])
    fl.apply_translation([dx, dy, dz])
    return fl


def build_half(bead, notes, scale=2.2, carve=True, engine="manifold", fuse=0.5):
    """1つのかたわれに笛(最大4本・十字)を埋め込む。戻り値 (carved_bead, [(flute,note),...], interfere)。
    interfere は干渉した笛ペアと重なり体積のリスト（空なら干渉なし）。"""
    bead = bead.copy()
    bead.apply_scale(scale)
    bead = repair_watertight(bead)
    b = bead.bounds
    cx, cy, r = measure_hole(bead)
    placed = []
    for note, (R, axis, sign) in zip(notes, WALLS):
        placed.append((_place_flute(note, cx, cy, r, b[1][2], R, axis, sign, fuse), note))
    # 笛どうしの干渉(実メッシュの重なり体積)を調べる
    interfere = []
    for i in range(len(placed)):
        for j in range(i + 1, len(placed)):
            try:
                inter = placed[i][0].intersection(placed[j][0], engine=engine)
                v = float(inter.volume) if inter is not None else 0.0
            except Exception:
                v = 0.0
            if v > 0.3:
                interfere.append((placed[i][1], placed[j][1], round(v, 1)))
    carved = bead
    if carve:
        for fl, _ in placed:
            carved = carved.difference(fl.convex_hull, engine=engine)
    return carved, placed, interfere


def build_pair(notes1, notes3, scale=2.2, carve=True, gap=8.0):
    """2つのかたわれを1つの Scene にまとめる（横に並べる）。戻り値 (scene, infos)。"""
    g1, g3 = load_halves()
    sc = trimesh.Scene()
    infos = []
    xcursor = 0.0
    for tag, bead, notes in [("R", g1, notes1), ("L", g3, notes3)]:
        carved, placed, interfere = build_half(bead, notes, scale=scale, carve=carve)
        if interfere:
            print("  [%s 干渉あり] %s" % (tag, interfere))
        else:
            print("  [%s 干渉なし] %d本" % (tag, len(placed)))
        # 横に並べる: このかたわれの左端を xcursor に合わせる
        shift = xcursor - carved.bounds[0][0]
        T = trimesh.transformations.translation_matrix([shift, 0, 0])
        carved.apply_transform(T)
        sc.add_geometry(carved, geom_name="bead_%s_0.20mm" % tag)
        for i, (fl, note) in enumerate(placed):
            fl.apply_transform(T)
            sc.add_geometry(fl, geom_name="flute_%s%d_%s_0.08careful" % (tag, i + 1, note.replace("#", "s")))
            infos.append((tag, note))
        xcursor = carved.bounds[1][0] + gap
    # A1miniベッド中心(128,128)・接地(z=0)へ寄せる（arrange=falseでもスライスできるように）
    ab = sc.bounds
    sc.apply_transform(trimesh.transformations.translation_matrix(
        [128.0 - (ab[0][0] + ab[1][0]) / 2.0, 128.0 - (ab[0][1] + ab[1][1]) / 2.0, -ab[0][2]]))
    return sc, infos


def main(argv=None):
    ap = argparse.ArgumentParser(description="HeartBeadsのかたわれ2つに笛を埋め込み1つの3mfにまとめる")
    ap.add_argument("--scale", type=float, default=2.2)
    ap.add_argument("--notes1", default="D7,F#7", help="かたわれ1(右)の笛の音（1〜2音・カンマ区切り）")
    ap.add_argument("--notes3", default="D7,F#7", help="かたわれ3(左)の笛の音（1〜2音・カンマ区切り）")
    ap.add_argument("--no-carve", action="store_true")
    ap.add_argument("--merged", action="store_true",
                    help="全オブジェクトを1メッシュに結合して出力(印刷でarrange配置崩れを回避)")
    ap.add_argument("--out", default="out/heartbeads_pair.3mf")
    args = ap.parse_args(argv)
    n1 = [s.strip() for s in args.notes1.split(",") if s.strip()]
    n3 = [s.strip() for s in args.notes3.split(",") if s.strip()]
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    sc, infos = build_pair(n1, n3, scale=args.scale, carve=not args.no_carve)
    if args.merged:
        sc.dump(concatenate=True).export(args.out)
    else:
        sc.export(args.out)
    print("2つのかたわれを1つの3mfにまとめた -> %s" % args.out)
    print("  オブジェクト: %s" % ", ".join(sc.geometry.keys()))
    print("  笛: %s" % ", ".join("%s:%s" % (t, n) for t, n in infos))


if __name__ == "__main__":
    main()


# ---- かたわれ1つ・笛3本・寝かせ印刷（2026-07-28 追加） ------------------------
#
# 笛の長軸を寝かせて刷ると、窓の向きは検証済みの範囲（-135度から+135度）に入って
# いなければならない。穴のまわりに十字（0・90・180・270度）で置くと、寝かせたとき
# 1本だけが「窓が真下」（180度）になり、これが唯一鳴らない向きである。ハートの平らな面を
# ベッドに付ける姿勢（x軸まわり+90度）では、真下になるのは180度の1本なので、
# 0・90・270度 の3本を使う。4本にしたければ45度回して±45度と±135度に
# するしかないが、そうすると4本とも薄い方向へ寄ってハートの側面からはみ出す。
#
# 置き方は「穴の壁に寄せる」を基本とし、それだと笛の背中がハートの表面から出てしまう
# 薄い方向だけは、背中が表面より WALL_IN だけ内側に来るまで穴の側へ押し込む。窓は
# 穴の内側へ少し食い込むが、窓が開くのは空気側なので発音には有利である。
FLAT_ANGLES = (0.0, 90.0, 270.0)      # 穴のまわりの配置角。寝かせると窓は 0/-90/+90 度
WALL_IN = 1.2                          # 笛の背中をハート表面からこれだけ内側に置く[mm]


def _rz4(deg):
    return _rz(deg)


def place_flute_around_hole(note, bead, angle_deg, l_max, fuse=0.5, wall_in=WALL_IN):
    """穴のまわり angle_deg の位置に、窓を穴へ向けて笛を1本置く。戻り値 (mesh, R)。"""
    cx, cy, r = measure_hole(bead)
    ztop = bead.bounds[1][2]
    fl = mini10.uniform_flute(mini10.length_for_note(note), L_max=l_max)
    R = _rz(angle_deg) @ R3
    fl.apply_transform(R)
    w = R[:3, :3] @ np.array([0.0, 0.0, 1.0])      # 窓の向き
    w = w / np.linalg.norm(w)
    u = np.cross([0.0, 0.0, 1.0], w)
    v = fl.vertices
    hole_w = float(np.dot([cx, cy, 0.0], w))
    shift_hug = (hole_w - (r + fuse)) - v.dot(w).max()          # 窓の面を穴の壁へ
    surf = float((bead.vertices.dot(-w)).max())
    shift_wall = -(surf - wall_in) - v.dot(w).min()             # 背中を表面の内側へ
    shift_w = max(shift_hug, shift_wall)                        # 穴に近い方を採る
    shift_u = float(np.dot([cx, cy, 0.0], u)) - (v.dot(u).min() + v.dot(u).max()) / 2.0
    d = shift_w * w + shift_u * u
    d[2] = ztop - fl.bounds[1][2]                               # 吸込口をハート上端へ
    fl.apply_translation(d)
    return fl, R


def build_flat_half(notes, scale=2.4, carve=True, engine="manifold", which="1"):
    """かたわれ1つに笛を置き、寝かせた印刷姿勢の Scene を返す。戻り値 (scene, infos)。

    印刷姿勢は、笛の長軸(モデルのz)が水平になるようy軸まわりに-90度回したもの。
    窓の向きは1本ずつ orient_check で確かめ、検証済みの範囲を外れたら例外にする。
    """
    if len(notes) > len(FLAT_ANGLES):
        raise ValueError("寝かせ印刷で置けるのは%d本まで（4本目は窓が真下になる）"
                         % len(FLAT_ANGLES))
    g1, g3 = load_halves()
    bead = (g1 if which == "1" else g3).copy()
    bead.apply_scale(scale)
    bead = repair_watertight(bead)
    l_max = mini10.uniform_body_length(
        [mini10.length_for_note(n) for n in mini10.CALIB12])
    if bead.extents[2] < l_max:
        raise ValueError("ハートの高さ %.1fmm が笛の外形長 %.1fmm より短い。scaleを上げること"
                         % (bead.extents[2], l_max))

    # 平らな面をベッドに付ける姿勢。x軸まわり+90度で、モデルのy(厚み)が上下、
    # z(笛の長軸)が水平になる。縁で立たせるより footprint が安定する。
    lay = trimesh.transformations.rotation_matrix(np.pi / 2, [1, 0, 0])
    placed, infos = [], []
    for note, ang in zip(notes, FLAT_ANGLES):
        fl, R = place_flute_around_hole(note, bead, ang, l_max)
        res = orient_check.check_orientation(R=lay[:3, :3] @ R[:3, :3])
        if res.verdict != "ok":
            raise ValueError("%s（穴まわり%.0f度）の向きが %s: %s"
                             % (note, ang, res.verdict, res.message))
        placed.append(fl)
        infos.append(dict(note=note, angle=ang, window_deg=round(res.angle_deg, 1),
                          tilt_deg=round(res.tilt_deg, 1)))

    body = bead
    if carve:
        for fl in placed:
            body = body.difference(fl.convex_hull, engine=engine)

    sc = trimesh.Scene()
    for m in [body] + placed:
        m.apply_transform(lay)
    zmin = min([body.bounds[0][2]] + [m.bounds[0][2] for m in placed])
    T = trimesh.transformations.translation_matrix([0, 0, -zmin])
    for m in [body] + placed:
        m.apply_transform(T)
    sc.add_geometry(body, geom_name="heart_0.20mm")
    for i, (fl, it) in enumerate(zip(placed, infos)):
        sc.add_geometry(fl, geom_name="flute%d_%s_0.08careful"
                        % (i + 1, it["note"].replace("#", "s")))
    # A1 miniのベッド中心へ寄せる
    ab = sc.bounds
    sc.apply_transform(trimesh.transformations.translation_matrix(
        [128.0 - (ab[0][0] + ab[1][0]) / 2.0, 128.0 - (ab[0][1] + ab[1][1]) / 2.0, 0.0]))
    return sc, infos
