"""ストリートオルガン式演奏機構（アイデア(2)）。

パンフルートの各笛（吹込口）に、加圧チャンバー(windchest)から空気を配り、
その間に「穴あきシート（楽譜ロール）」を挟んでスクロールさせる。シートの穴が来た
ポートにだけ空気が通り、その笛が鳴る＝紙ロール式自動演奏（ストリートオルガン/自動ピアノ）。

  仕組み（断面, z方向）:
    [チャンバー(加圧)]→(ポート:上面へ貫通)→[シート溝(穴あきシートが Y方向にスクロール)]→[笛の吹込口(上に載る)]
  音軸 = X（Nポートを一列, ピッチ pitch）。時間軸 = Y（シートを +Y へ送る）。
  シートの穴 (x=ポートi, y=時刻t) が読み取り線(y=0)に来た瞬間、その笛が鳴る。

部品:
  reader_block(): チャンバー＋吹込口＋ポート列＋シート溝レール（1体印刷）
  punched_sheet(score): 楽譜（各時刻に鳴らすポート番号）を穴にした薄い帯

実行: trimesh + manifold3d。
"""
import os
import numpy as np
import trimesh

OUT = os.path.join(os.path.dirname(__file__), os.pardir, "out")

WALL = 2.0
PORT_R = 2.0            # ポート/シート穴 半径
SHEET_T = 1.0          # シート厚
SLOT_CL = 0.6          # シート溝クリアランス（片側）
STEP_Y = 8.0           # 楽譜の1時間ステップの送り量(mm)


def reader_block(n=8, pitch=8.0, chest_h=12.0, depth=22.0, blow_r=4.0):
    """加圧チャンバー＋ポート列＋シート溝レール（1体）。上面にポートが開き、笛が載る。"""
    W = n * pitch + 2 * WALL + 8.0          # X（音軸）幅
    D = depth                                # Y（時間軸）奥行き
    H = chest_h                              # チャンバー高さ(z)
    # チャンバー（外箱−内空洞）
    outer = trimesh.creation.box(extents=[W, D, H]); outer.apply_translation([0, 0, H / 2])
    inner = trimesh.creation.box(extents=[W - 2 * WALL, D - 2 * WALL, H - 2 * WALL])
    inner.apply_translation([0, 0, H / 2])
    chest = trimesh.boolean.difference([outer, inner], engine="manifold")
    # 吹込口（-X端面から chamber へ）
    blow = trimesh.creation.cylinder(radius=blow_r, height=WALL + 6, sections=48)
    blow.apply_transform(trimesh.transformations.rotation_matrix(np.radians(90), [0, 1, 0]))
    blow.apply_translation([-W / 2 - 3 + (WALL + 6) / 2, 0, H / 2])
    chest = trimesh.boolean.union([chest, blow], engine="manifold")
    # ポート列（上面 z=H を貫通、読み取り線 y=0）
    ports = []
    xs = [(-(n - 1) / 2 + i) * pitch for i in range(n)]
    for x in xs:
        p = trimesh.creation.cylinder(radius=PORT_R, height=2 * WALL + 2, sections=32)
        p.apply_translation([x, 0, H - WALL / 2])       # 上壁を貫通
        ports.append(p)
    chest = trimesh.boolean.difference([chest, trimesh.boolean.union(ports, engine="manifold")], engine="manifold")
    # シート溝レール：上面の左右(X端)に沿ってY方向のレール＋内側リップでシートを押さえる
    gap = SHEET_T + 2 * SLOT_CL
    rails = []
    rail_h = gap + 1.5
    for sx in (-1, 1):
        x0 = sx * (W / 2 - 1.0)
        base = trimesh.creation.box(extents=[2.0, D + 10, rail_h]); base.apply_translation([x0, 0, H + rail_h / 2])
        lip = trimesh.creation.box(extents=[4.0, D + 10, 1.2]); lip.apply_translation([x0 - sx * 2.0, 0, H + gap + 0.6])
        rails += [base, lip]
    block = trimesh.boolean.union([chest] + rails, engine="manifold")
    info = dict(n=n, pitch=pitch, W=W, D=D, H=H, ports_x=xs, sheet_top_z=H, gap=gap,
                dims=tuple(np.round(block.extents, 1)))
    return block, info


def punched_sheet(score, n=8, pitch=8.0, W=None, lead=8.0):
    """楽譜を穴にした薄い帯。score=各時刻ステップで鳴らすポート番号(0..n-1)の集合のリスト。
    例 [ {0},{1},{2},{3} ] は ポート0→1→2→3 を順に鳴らす。和音は {0,2,4} のように複数。"""
    if W is None:
        W = n * pitch + 2 * WALL + 8.0 - 3.0     # レール内に収まる幅
    steps = len(score)
    L = lead * 2 + steps * STEP_Y                # 帯の長さ(Y)
    strip = trimesh.creation.box(extents=[W, L, SHEET_T]); strip.apply_translation([0, 0, SHEET_T / 2])
    xs = [(-(n - 1) / 2 + i) * pitch for i in range(n)]
    holes = []
    for t, notes in enumerate(score):
        y = -L / 2 + lead + (t + 0.5) * STEP_Y
        for i in notes:
            h = trimesh.creation.cylinder(radius=PORT_R, height=SHEET_T + 1, sections=24)
            h.apply_translation([xs[i], y, SHEET_T / 2])
            holes.append(h)
    if holes:
        strip = trimesh.boolean.difference([strip, trimesh.boolean.union(holes, engine="manifold")], engine="manifold")
    info = dict(n=n, steps=steps, W=W, L=L, dims=tuple(np.round(strip.extents, 1)))
    return strip, info


# ---------------------------------------------------------------------------
# 印刷可能な分割：チャンバー天井(幅広ブリッジ不可)を避け、
#   base = 上面開放トレー（床＋壁＋吹込口＋合わせリム）
#   lid  = ポート板＋シート溝レール＋リム内に落ちる段（baseに嵌めて接着）
# の2部品にする。両方とも平物で無理なく刷れる。
# ---------------------------------------------------------------------------
def reader_base(n=8, pitch=8.0, chest_h=12.0, depth=22.0, blow_r=4.0):
    W = n * pitch + 2 * WALL + 8.0
    outer = trimesh.creation.box(extents=[W, depth, chest_h]); outer.apply_translation([0, 0, chest_h / 2])
    # 上面開放の内空洞（上に WALL 分の縁は残さず開ける）
    inner = trimesh.creation.box(extents=[W - 2 * WALL, depth - 2 * WALL, chest_h])
    inner.apply_translation([0, 0, chest_h / 2 + WALL])          # 上へずらして天井を無くす＝開放
    base = trimesh.boolean.difference([outer, inner], engine="manifold")
    blow = trimesh.creation.cylinder(radius=blow_r, height=WALL + 6, sections=48)
    blow.apply_transform(trimesh.transformations.rotation_matrix(np.radians(90), [0, 1, 0]))
    blow.apply_translation([-W / 2 - 3 + (WALL + 6) / 2, 0, chest_h / 2])
    base = trimesh.boolean.union([base, blow], engine="manifold")
    info = dict(W=W, depth=depth, chest_h=chest_h, n=n, pitch=pitch)
    return base, info


def reader_lid(n=8, pitch=8.0, depth=22.0, chest_h=12.0, plate_t=2.0):
    W = n * pitch + 2 * WALL + 8.0
    plate = trimesh.creation.box(extents=[W, depth, plate_t]); plate.apply_translation([0, 0, plate_t / 2])
    # baseリム内に落ちる段（内寸 W-2WALL × depth-2WALL, 高さ2mm）で位置決め
    step = trimesh.creation.box(extents=[W - 2 * WALL - 0.4, depth - 2 * WALL - 0.4, 2.0])
    step.apply_translation([0, 0, -1.0])
    lid = trimesh.boolean.union([plate, step], engine="manifold")
    # ポート列（貫通）
    xs = [(-(n - 1) / 2 + i) * pitch for i in range(n)]
    ports = []
    for x in xs:
        p = trimesh.creation.cylinder(radius=PORT_R, height=plate_t + 4, sections=32)
        p.apply_translation([x, 0, 0]); ports.append(p)
    lid = trimesh.boolean.difference([lid, trimesh.boolean.union(ports, engine="manifold")], engine="manifold")
    # シート溝レール（上面）
    gap = SHEET_T + 2 * SLOT_CL; rail_h = gap + 1.5
    rails = []
    for sx in (-1, 1):
        x0 = sx * (W / 2 - 1.0)
        b = trimesh.creation.box(extents=[2.0, depth + 10, rail_h]); b.apply_translation([x0, 0, plate_t + rail_h / 2])
        lip = trimesh.creation.box(extents=[4.0, depth + 10, 1.2]); lip.apply_translation([x0 - sx * 2.0, 0, plate_t + gap + 0.6])
        rails += [b, lip]
    lid = trimesh.boolean.union([lid] + rails, engine="manifold")
    info = dict(W=W, ports_x=xs, plate_t=plate_t, gap=gap)
    return lid, info


# ---------------------------------------------------------------------------
# オルガン用パンフルート（吹込口一列版）：縦の閉管mini笛をポートピッチで一列に。
# 各笛はヘッド(下から吹く)を下端にし、吹込口(底 z=0)をポート位置に一致させて載せる。
# 音は共鳴管長で決める（閉管 予測式を流用）。上部の連結板で一体化（底=吹込口は開放）。
# ---------------------------------------------------------------------------
def organ_panflute(notes=None, pitch=8.0):
    import sys as _s
    _s.path.insert(0, os.path.dirname(__file__))
    import mini
    if notes is None:
        notes = ["C6", "D6", "E6", "F6", "G6", "A6", "B6", "C7"]
    n = len(notes)
    xs = [(-(n - 1) / 2 + i) * pitch for i in range(n)]
    head = mini._mini_head()
    pipes, infos = [], []
    for x, note in zip(xs, notes):
        zt = mini.z_top_for_note(note)                 # 閉管：上端z
        ext = mini._bore_extension(zt)                  # ヘッド上の閉じボア
        h = head.copy()
        pipe = trimesh.util.concatenate([h, ext])
        # ヘッドのxy中心(CX,CY)を原点化→ポート位置xへ（y=0中心）
        pipe.apply_translation([-mini.CX + x, -mini.CY, 0])
        pipes.append(pipe)
        infos.append(dict(note=note, x=x, z_top=zt, freq=mini.predict_freq(zt)))
    body = trimesh.util.concatenate(pipes)
    # 上部連結板（各ヘッド上・z=20〜24, 底の吹込口は開放）でrigid一体化
    b0, b1 = body.bounds
    web = trimesh.creation.box(extents=[b1[0] - b0[0] + 2, 8.0, 4.0])
    web.apply_translation([(b0[0] + b1[0]) / 2, 0, 22.0])
    mesh = trimesh.util.concatenate([body, web])
    info = dict(notes=notes, xs=xs, pitch=pitch, pipes=infos, dims=tuple(np.round(mesh.extents, 1)))
    return mesh, info


def main():
    import sys
    os.makedirs(OUT, exist_ok=True)
    if "--split" in sys.argv:
        base, _ = reader_base(); base.export(os.path.join(OUT, "organ_reader_base.stl"))
        lid, li = reader_lid(); lid.export(os.path.join(OUT, "organ_reader_lid.stl"))
        print("分割リーダー：base(上面開放トレー)＋lid(ポート板＋レール)")
        print("  base -> out/organ_reader_base.stl 外形%s watertight=%s" % (tuple(np.round(base.extents, 1)), base.is_watertight))
        print("  lid  -> out/organ_reader_lid.stl  外形%s watertight=%s ポートx=%s" %
              (tuple(np.round(lid.extents, 1)), lid.is_watertight, [round(x, 1) for x in li["ports_x"]]))
        return
    if "--panflute" in sys.argv:
        mesh, info = organ_panflute()
        mesh.export(os.path.join(OUT, "organ_panflute_row.stl"))
        print("オルガン用パンフルート(吹込口一列・縦8本):")
        for p in info["pipes"]:
            print("  %-3s x=%+5.1f z_top=%.1f 予測%.0fHz" % (p["note"], p["x"], p["z_top"], p["freq"]))
        print("  外形%s watertight=%s -> out/organ_panflute_row.stl" % (info["dims"], mesh.is_watertight))
        return
    n = 8
    block, bi = reader_block(n=n)
    block.export(os.path.join(OUT, "organ_reader.stl"))
    print("オルガン reader（チャンバー＋%dポート＋シート溝）: 外形%s watertight=%s 吹込口=-X端" %
          (n, bi["dims"], block.is_watertight))
    print("  ポートx:", [round(x, 1) for x in bi["ports_x"]], " シート上面z=%.1f 溝gap=%.1f" % (bi["sheet_top_z"], bi["gap"]))
    # サンプル楽譜：ドレミファソラシド（ポート0..7を順に）＋最後に和音(0,2,4)
    score = [{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, set(), {0, 2, 4}]
    sheet, si = punched_sheet(score, n=n)
    sheet.export(os.path.join(OUT, "organ_sheet_scale.stl"))
    print("サンプル穴あきシート（ドレミ…＋和音）: 外形%s watertight=%s ステップ%d" %
          (si["dims"], sheet.is_watertight, si["steps"]))
    print("  -> out/organ_reader.stl / out/organ_sheet_scale.stl")


if __name__ == "__main__":
    main()
