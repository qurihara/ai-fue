"""笛の印刷向きの安定性を調べる試験片。

いま実績があるのは「横置き・窓がz+方向に開口」だけである（外見統一版のコームや
カード、スプールはすべてこれ）。日用品に埋め込むには他の向きでも鳴る必要があるので、
向きを1つずつ変えて確かめる。この生成器は段階(2)「横置き・窓が水平方向に開口」の
試験片を作る。

作りは、62.07×7×7mm の直方体を長辺が横になるように置き、その側面に外見統一版の
笛を1本、窓が水平方向へ開口するように接する。直方体が土台と支えを兼ねるので、
笛そのものは寝かせたまま、窓の向きだけが90度変わる。
"""
from __future__ import annotations
import argparse, os, sys
import numpy as np
import trimesh
from trimesh import transformations as tf

sys.path.insert(0, os.path.dirname(__file__))
import mini10

BAR = 7.0        # 土台の直方体の断面（7×7mm）
OVER = 0.3       # 笛の床へ食い込ませて確実に一体化させる量


def build(note="C7", notes=None, bar=BAR):
    """段階(2)の試験片を作る。戻り値 (mesh, flute, 情報dict)。"""
    notes = notes or (mini10.CALIB11 + ["G7"])          # 12音 G#6〜G7
    L_max = mini10.uniform_body_length([mini10.length_for_note(n) for n in notes])
    L = mini10.length_for_note(note)
    g = mini10.uniform_flute(L, L_max=L_max)            # native: 窓=+z, 床=z=0, 長さ=+x
    # x軸まわり -90度: 窓(+z)を +y へ、幅(+y)を -z へ。窓が水平方向に開く。
    R = np.eye(4); R[:3, :3] = np.array([[1, 0, 0], [0, 0, 1], [0, -1, 0]], float)
    assert abs(np.linalg.det(R[:3, :3]) - 1) < 1e-9
    g.apply_transform(R)
    b = g.bounds
    g.apply_translation([-b[0][0], -b[0][1], -b[0][2]])  # 原点へ
    gb = g.bounds
    # 土台は笛の床側(y<0)に接する。窓のある +y 側には何も置かない。
    barbox = trimesh.creation.box(extents=[L_max, bar + OVER, bar])
    barbox.apply_translation([L_max / 2, -(bar + OVER) / 2 + OVER, bar / 2])
    mesh = trimesh.boolean.union([barbox, g], engine="manifold")
    info = dict(note=note, L=round(L, 2), L_max=round(L_max, 2),
                extents=tuple(np.round(mesh.extents, 2)))
    return mesh, g, info


def verify(mesh, g):
    """ボアが中空か、窓と吸込口が空気に開いているかを実メッシュで確かめる。"""
    gb = g.bounds
    zc = (gb[0][2] + gb[1][2]) / 2
    L = gb[1][0] - gb[0][0]
    out = {}
    pts = [[gb[0][0] + t * L, gb[0][1] + 1.7, zc] for t in np.linspace(0.25, 0.85, 7)]
    out["ボアが中空"] = bool((~mesh.contains(np.array(pts))).all())
    wp = [[gb[0][0] + d, gb[1][1] + o, zc] for d in (13.0, 16.0, 19.0) for o in (1.0, 3.0, 6.0)]
    out["窓の前が空気"] = bool((~mesh.contains(np.array(wp))).all())
    mp = [[gb[0][0] - 2.0, gb[0][1] + 1.7, zc]]
    out["吸込口の外が空気"] = bool((~mesh.contains(np.array(mp))).all())
    return out


# 土台の3つの面に同じ笛を1本ずつ付ける。native（窓=+z・床=z=0・長さ=+x）から
# 各面へ移すための回転を、面ごとに持つ。底面はベッドに接するので使わない。
FACES = {
    "右側面": dict(
        説明="窓が+y方向（水平）に開口。段階(2)そのもの。",
        R=[[1, 0, 0], [0, 0, 1], [0, -1, 0]],   # 窓(+z) を +y へ
    ),
    "左側面": dict(
        説明="窓が-y方向（水平）に開口。段階(2)を左右反転した向き。",
        R=[[1, 0, 0], [0, 0, -1], [0, 1, 0]],   # 窓(+z) を -y へ
    ),
    "上面": dict(
        説明="窓が+z方向に開口。いま実績のある向きで、比較のための対照。",
        R=[[1, 0, 0], [0, 1, 0], [0, 0, 1]],    # native のまま
    ),
}

WINDOW_X = (12.0, 16.5)   # 上面の窓の開口（実測）

# native座標での検査点。ボアの中、窓の外、吸込口の外。面ごとの回転をかけて使う。
def _check_points_native(L_out, width=7.0, height=4.0, L_bore=None):
    """検査点は native 座標で置く。

    ボアの点は「外形の長さ」ではなく[* 音を決めるボアの実長 L_bore]の割合で置く。
    外形長で置くと、音によっては点が内部の仕切り壁（ボアの終端）に落ちて、
    中空なのにNGと出てしまう（D7で実際に起きた）。
    """
    yc = width / 2
    Lb = L_bore if L_bore is not None else L_out
    # ボアは窓より先(x≈16.5mm)から仕切り壁(x=Lb)までにある。頭部と壁を避けて採る。
    x0, x1 = WINDOW_X[1] + 2.0, Lb - 2.0
    bore = [[x0 + t * (x1 - x0), yc, 1.7] for t in np.linspace(0.0, 1.0, 7)]
    window = [[d, yc, height + o] for d in (13.0, 16.0, 19.0) for o in (1.0, 3.0, 6.0)]
    mouth = [[-2.0, yc, 1.7]]
    return dict(ボアが中空=bore, 窓の前が空気=window, 吸込口の外が空気=mouth)


def build_multi(note="C7", notes=None, bar=BAR):
    """土台の3面（右側面・左側面・上面）に同じ笛を1本ずつ付けた試験片。

    1回の印刷で、窓が水平に開く向きを左右2本、実績のある窓が上を向く向きを1本、
    まったく同じ条件で刷れる。上面の1本が対照になるので、もし全部鳴らなければ
    向きではなくプリンタや材料の側に原因があると切り分けられる。
    戻り値は (mesh, 面ごとの検査点dict, 情報dict)。
    """
    notes = notes or (mini10.CALIB11 + ["G7"])          # 12音 G#6〜G7
    L_max = mini10.uniform_body_length([mini10.length_for_note(n) for n in notes])
    L = mini10.length_for_note(note)

    barbox = trimesh.creation.box(extents=[L_max, bar, bar])
    barbox.apply_translation([L_max / 2, 0, bar / 2])   # x:0..L_max, y:±bar/2, z:0..bar
    parts = [barbox]
    points = {}

    for face, spec in FACES.items():
        g = mini10.uniform_flute(L, L_max=L_max)
        T = np.eye(4); T[:3, :3] = np.array(spec["R"], float)
        assert abs(np.linalg.det(T[:3, :3]) - 1) < 1e-9
        g.apply_transform(T)
        b = g.bounds
        if face == "右側面":       # 床(=y最小の面)を土台の+y面へ押し当てる
            shift = [-b[0][0], bar / 2 - OVER - b[0][1], -b[0][2]]
        elif face == "左側面":     # 床(=y最大の面)を土台の-y面へ押し当てる
            shift = [-b[0][0], -(bar / 2 - OVER) - b[1][1], -b[0][2]]
        else:                      # 上面。床(=z最小の面)を土台の上面へ押し当てる
            shift = [-b[0][0], -(b[0][1] + b[1][1]) / 2, bar - OVER - b[0][2]]
        g.apply_translation(shift)
        parts.append(g)
        M = np.eye(4); M[:3, :3] = T[:3, :3]; M[:3, 3] = shift
        points[face] = {k: (M[:3, :3] @ np.array(v).T).T + M[:3, 3]
                        for k, v in _check_points_native(L_max, L_bore=L).items()}

    mesh = trimesh.boolean.union(parts, engine="manifold")
    info = dict(note=note, L=round(L, 2), L_max=round(L_max, 2),
                extents=tuple(np.round(mesh.extents, 2)), faces=list(FACES))
    return mesh, points, info


def verify_multi(mesh, points):
    """面ごとに、ボアが中空か、窓と吸込口が空気に開いているかを確かめる。"""
    return {face: {k: bool((~mesh.contains(np.asarray(pts))).all())
                   for k, pts in d.items()}
            for face, d in points.items()}


# ---- 角度掃引版 ----------------------------------------------------------
# 窓がz+を向く向きを0度とし、長軸(x)まわりに回した角度で並べる。0度と±90度は
# 2026-07-27に実機で鳴ることを確認済みで、残りの角度を同じ条件で確かめる。
CUT_MARGIN = 2.5          # 窓の前を空けるためにバットレスを切り欠く余裕
CLEARANCE = 6.0           # 笛の最下点を床から浮かせる高さ（窓が下を向いても空気が回る）
BUT_TOP = 8.0             # バットレスの上端の幅。笛の幅7.0より広くし、どの角度でも笛の
                          # 下面を端まで受ける。宙づりになるのは窓の帯だけになり条件が揃う
BUT_BOTTOM = 14.0         # バットレスの下端（床に着く）の幅
BUT_BITE = 2.0            # 笛の外形へ食い込ませる高さ。控え壁は笛の外周に沿って
                          # 削られる（下の _carve を参照）ので、深く食い込ませるほど
                          # 接する面が広くなり，ボアには一切入らない


def _buttress(y_low, x_ranges, top_z):
    """下へ広がる台形断面の控え壁。上へ行くほど細いのでオーバーハングが出ない。"""
    from shapely.geometry import Polygon
    poly = Polygon([(-BUT_BOTTOM / 2, 0.0), (BUT_BOTTOM / 2, 0.0),
                    (BUT_TOP / 2, top_z), (-BUT_TOP / 2, top_z)])
    parts = []
    for x0, x1 in x_ranges:
        p = trimesh.creation.extrude_polygon(poly, height=x1 - x0)
        # 押し出した局所座標 (u,v,w) を世界の (y,z,x) へ移す
        M = np.eye(4); M[:3, :3] = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], float)
        assert abs(np.linalg.det(M[:3, :3]) - 1) < 1e-9
        p.apply_transform(M)
        p.apply_translation([x0, y_low, 0.0])
        parts.append(p)
    return parts


def _carve(parts, flute):
    """控え壁から「笛の内部の空洞」を彫り抜く。

    控え壁を笛へ深く食い込ませると，そのままでは笛の床を突き抜けてボアを埋めてしまう
    （実際に食い込み0.8mmで0度のボア断面が9%減った）。そこで笛の凸包から笛の実体を
    引いた形＝ボア・風道・窓・末端の死んだ空洞をまとめて求め，それを控え壁から引く。
    こうすると控え壁は笛の外周に沿って削られ，空洞には一切入らないまま接する面だけが
    広くなる。スキル flute-embed でホストに笛を埋めるときと同じ考え方である。
    """
    void = trimesh.boolean.difference([flute.convex_hull, flute], engine="manifold")
    return [trimesh.boolean.difference([p, void], engine="manifold") for p in parts]


def build_angle(theta_deg, note="C7", notes=None):
    """1つの角度ぶんの試験片。戻り値 (mesh, 検査点dict, 情報dict)。"""
    notes = notes or (mini10.CALIB11 + ["G7"])
    L_max = mini10.uniform_body_length([mini10.length_for_note(n) for n in notes])
    L = mini10.length_for_note(note)
    g = mini10.uniform_flute(L, L_max=L_max)

    t = np.radians(theta_deg)
    R = np.array([[1, 0, 0], [0, np.cos(t), -np.sin(t)], [0, np.sin(t), np.cos(t)]])
    T = np.eye(4); T[:3, :3] = R
    g.apply_transform(T)
    b = g.bounds
    shift = np.array([-b[0][0], 0.0, CLEARANCE - b[0][2]])
    g.apply_translation(shift)

    # 最下点のy（そこへ控え壁の頭を当てる）
    v = g.vertices
    low = v[v[:, 2] <= v[:, 2].min() + 0.2]
    y_low = float(low[:, 1].mean())

    x0, x1 = WINDOW_X
    ranges = [(0.0, x0 - CUT_MARGIN), (x1 + CUT_MARGIN, L_max)]
    parts = _carve(_buttress(y_low, ranges, CLEARANCE + BUT_BITE), g)
    mesh = trimesh.boolean.union([g] + parts, engine="manifold")

    M = np.eye(4); M[:3, :3] = R; M[:3, 3] = shift
    points = {k: (R @ np.array(val).T).T + shift
              for k, val in _check_points_native(L_max, L_bore=L).items()}
    info = dict(theta=theta_deg, note=note, L=round(L, 2),
                extents=tuple(np.round(mesh.extents, 2)))
    return mesh, points, info


# ---- 縦置き版（段階(5)〜(7)） --------------------------------------------
# 長軸を立てて刷る。窓がz+を向く向きの笛を y軸まわりに±90度回すと、吹き込み口が
# 上を向く置き方と下を向く置き方になる。窓はどちらも水平（±x）を向く。
# 62mmの塔が7×4mmの断面で立つので、下へ広がる裾で土台を作って倒れないようにする。
SKIRT_H = 10.0            # 裾の高さ。窓は吹き込み口から12mmなので、下向きでも窓に掛からない
SKIRT_BASE = (20.0, 23.0) # 裾の底の大きさ（x, y）
SKIRT_BITE = 0.4          # 裾の頭を笛の断面より少し大きくして確実に一体化させる


def build_vertical(mouth="up", note="C7", notes=None):
    """縦置きの試験片。mouth="up" なら吹き込み口が上、"down" なら下を向く。"""
    notes = notes or (mini10.CALIB11 + ["G7"])
    L_max = mini10.uniform_body_length([mini10.length_for_note(n) for n in notes])
    L = mini10.length_for_note(note)
    g = mini10.uniform_flute(L, L_max=L_max)

    beta = np.radians(90.0 if mouth == "up" else -90.0)
    R = np.array([[np.cos(beta), 0, np.sin(beta)],
                  [0, 1, 0],
                  [-np.sin(beta), 0, np.cos(beta)]])
    T = np.eye(4); T[:3, :3] = R
    assert abs(np.linalg.det(R) - 1) < 1e-9
    g.apply_transform(T)
    b = g.bounds
    shift = np.array([-(b[0][0] + b[1][0]) / 2, -(b[0][1] + b[1][1]) / 2, -b[0][2]])
    g.apply_translation(shift)

    gb = g.bounds
    top = [(gb[0][0] - SKIRT_BITE, gb[0][1] - SKIRT_BITE),
           (gb[1][0] + SKIRT_BITE, gb[1][1] + SKIRT_BITE)]
    bw, bd = SKIRT_BASE
    pts = [[x, y, 0.0] for x in (-bw / 2, bw / 2) for y in (-bd / 2, bd / 2)]
    pts += [[x, y, SKIRT_H] for x in (top[0][0], top[1][0]) for y in (top[0][1], top[1][1])]
    skirt = trimesh.PointCloud(np.array(pts)).convex_hull   # 下へ広がる四角錐台
    mesh = trimesh.boolean.union([g] + _carve([skirt], g), engine="manifold")

    M = np.eye(4); M[:3, :3] = R; M[:3, 3] = shift
    points = {k: (R @ np.array(v).T).T + shift
              for k, v in _check_points_native(L_max, L_bore=L).items()}
    info = dict(mouth=mouth, note=note, L=round(L, 2),
                extents=tuple(np.round(mesh.extents, 2)))
    return mesh, points, info


def build_vertical_plate(note="C7", gap=14.0, mouths=("up", "down"), notes=None):
    """縦置きの試験片を並べた1枚の板。

    mouths で吹き込み口の向き、notes で音を指定する。両方を指定すると、その全部の
    組み合わせを作る。音を変えると管の長さ（内部の仕切り壁の位置）だけが変わり、
    外形・風道・窓は同じなので、音による鳴りやすさの違いだけを比べられる。
    """
    labels = {"up": "吸込口が上", "down": "吸込口が下"}
    notes = notes or [note]
    pieces, points, infos, x = [], {}, [], 0.0
    for mo in mouths:
      for nt in notes:
        label = "%s %s" % (labels[mo], nt)
        m, pts, info = build_vertical(mo, nt)
        b = m.bounds
        d = np.array([x - b[0][0], -b[0][1], 0.0])
        m.apply_translation(d)
        pieces.append(m)
        points[label] = {k: np.asarray(v) + d for k, v in pts.items()}
        info["label"] = label
        info["x"] = round(x, 1)
        infos.append(info)
        x += (b[1][0] - b[0][0]) + gap
    return trimesh.util.concatenate(pieces), points, infos


def build_angle_plate(angles, note="C7", gap=10.0, per_row=4, row_gap=10.0):
    """角度ぶんの試験片を格子に並べた1枚の板。戻り値 (mesh, 検査点dict, 情報list)。

    1列に並べると幅が出すぎてブリムどうしが繋がるので、per_row本ずつ折り返す。
    列(x方向)が手前から奥へ、各列の中は左から右へ角度の順に並ぶ。
    """
    pieces, points, infos = [], {}, []
    y = 0.0
    for i, a in enumerate(angles):
        row, col = divmod(i, per_row)
        if col == 0:
            y = 0.0
        m, pts, info = build_angle(a, note)
        b = m.bounds
        d = np.array([row * (b[1][0] - b[0][0] + row_gap) - b[0][0], y - b[0][1], 0.0])
        m.apply_translation(d)
        pieces.append(m)
        key = "%+d度" % a
        points[key] = {k: np.asarray(val) + d for k, val in pts.items()}
        info.update(列=row + 1, x=round(d[0], 1), y=round(y, 1),
                    幅=round(b[1][1] - b[0][1], 2))
        infos.append(info)
        y += (b[1][1] - b[0][1]) + gap
    return trimesh.util.concatenate(pieces), points, infos


def main(argv=None):
    ap = argparse.ArgumentParser(description="印刷向きの試験片")
    ap.add_argument("--note", default="C7", help="使う音（既定 C7）")
    ap.add_argument("--faces", action="store_true",
                    help="土台の3面（右側面・左側面・上面）に1本ずつ付けた版を作る")
    ap.add_argument("--angles", default=None,
                    help="長軸まわりの回転角をカンマ区切りで指定した掃引版を作る（例 -135,-90,-45,0,45,90,135,180）")
    ap.add_argument("--vertical", action="store_true",
                    help="長軸を立てた縦置き版（吸込口が上と下の2本）を作る")
    ap.add_argument("--mouth", default="up,down",
                    help="縦置き版でどちらを作るか（up / down / up,down）")
    ap.add_argument("--out", default=None)
    a = ap.parse_args(argv)

    if a.vertical:
        out = a.out or "out/orient_vertical.stl"
        mouths = tuple(m.strip() for m in a.mouth.split(",") if m.strip())
        notes = [n.strip() for n in a.note.split(",") if n.strip()]
        mesh, points, infos = build_vertical_plate(mouths=mouths, notes=notes)
        res = verify_multi(mesh, points)
        os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
        mesh.export(out)
        print("縦置き版 長軸を立てて刷る（窓はどちらも水平を向く）")
        print("  音 %s  外形 %s mm  watertight=%s"
              % (a.note, tuple(np.round(mesh.extents, 2)), mesh.is_watertight))
        ok = True
        for info in infos:
            d = res[info["label"]]
            ok = ok and all(d.values())
            print("  [%-14s] x=%5.1f 管長%5.2fmm  %s" % (
                info["label"], info["x"], info["L"],
                "  ".join("%s:%s" % (k, "OK" if v else "**NG**") for k, v in d.items())))
        print("  ->", out, "（全項目OK）" if ok else "（**NGあり**）")
        return 0 if ok else 1

    if a.angles:
        angles = [float(s) for s in a.angles.split(",")]
        angles = [int(v) if float(v).is_integer() else v for v in angles]
        out = a.out or "out/orient_angles.stl"
        mesh, points, infos = build_angle_plate(angles, a.note)
        res = verify_multi(mesh, points)
        os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
        mesh.export(out)
        print("角度掃引版 窓がz+を向く向きを0度とし、長軸まわりに回した角度で並べる")
        print("  音 %s  外形 %s mm  本数 %d" %
              (a.note, tuple(np.round(mesh.extents, 2)), len(angles)))
        ok = True
        for info in infos:
            key = "%+d度" % info["theta"]
            d = res[key]
            ok = ok and all(d.values())
            print("  [%6s] %d列目 x=%5.1f y=%5.1f  %s" % (
                key, info["列"], info["x"], info["y"],
                "  ".join("%s:%s" % (k, "OK" if v else "**NG**") for k, v in d.items())))
        print("  ->", out, "（全項目OK）" if ok else "（**NGあり**）")
        return 0 if ok else 1

    if a.faces:
        out = a.out or "out/orient_3faces.stl"
        mesh, points, info = build_multi(a.note)
        res = verify_multi(mesh, points)
        os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
        mesh.export(out)
        print("3面版 土台の右側面・左側面・上面に同じ笛を1本ずつ")
        print("  音 %s（管長 %.2fmm・外形は12音のL_max %.2fmm に統一）" % (info["note"], info["L"], info["L_max"]))
        print("  外形 %s mm  watertight=%s" % (info["extents"], mesh.is_watertight))
        for face, d in res.items():
            print("  [%s] %s" % (face, FACES[face]["説明"]))
            for k, v in d.items():
                print("     %-16s %s" % (k, "OK" if v else "**NG**"))
        print("  ->", out)
        return 0

    out = a.out or "out/orient2_window_horizontal.stl"
    mesh, g, info = build(a.note)
    res = verify(mesh, g)
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    mesh.export(out)
    print("段階(2) 横置き・窓が水平方向に開口")
    print("  音 %s（管長 %.2fmm・外形は12音のL_max %.2fmm に統一）" % (info["note"], info["L"], info["L_max"]))
    print("  外形 %s mm  watertight=%s" % (info["extents"], mesh.is_watertight))
    for k, v in res.items():
        print("   %-16s %s" % (k, "OK" if v else "**NG**"))
    print("  ->", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
