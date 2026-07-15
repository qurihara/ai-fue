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
PORT_R = 3.0           # ポート半径。v3ヘッドの吸込口(外Ø7/内Ø6)の内径Ø6に一致させる
                       # （2026/7/14 Ø4→Ø6。前版はポートと吸込口の径がズレて送気が漏れ鳴らなかった）
SHEET_HOLE_R = 2.5     # 穴あきシートの穴 半径（Ø5）。ポートØ6より小さくして隣列の閉じ代(ランド)を
                       # 稼ぐ（ピッチ8で Ø5なら片側1.5mmランド）。送気はポートØ6が律速なので通気は十分。
SHEET_T = 1.0          # シート厚
SLOT_CL = 0.15         # シート溝クリアランス（片側）。シート1mm(PLA)前提。溝=1.0+2*0.15=1.3mm
                       # （2026/7/14 0.3→0.15。前版は溝1.6mmが緩く送気漏れが大きかった＝実機確認）
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


def _y_slot(cx, cy, slot_len, r=PORT_R, h=None):
    """Y方向に長い角丸スロット(スタジアム形)の切り抜き体。X幅=2r(=ポート径), Y全長=slot_len。
    Y=時間軸なので、スロットのY長さが「その音のおおよその音価(鳴っている時間)」になる。"""
    if h is None:
        h = SHEET_T + 1.0
    slot_len = max(slot_len, 2 * r)
    straight = slot_len - 2 * r                       # 直線部のY長さ（両端は半円キャップ）
    parts = []
    if straight > 1e-6:
        b = trimesh.creation.box(extents=[2 * r, straight, h]); b.apply_translation([cx, cy, h / 2])
        parts.append(b)
    for s in (-1, 1):
        c = trimesh.creation.cylinder(radius=r, height=h, sections=24)
        c.apply_translation([cx, cy + s * (slot_len / 2 - r), h / 2])
        parts.append(c)
    return trimesh.boolean.union(parts, engine="manifold") if len(parts) > 1 else parts[0]


def punched_sheet(score, n=8, pitch=8.0, W=None, lead=8.0, slot_len=6.0, step_y=None):
    """楽譜を穴にした薄い帯。score=各時刻ステップで鳴らすポート番号(0..n-1)の集合のリスト。
    穴は「X幅=ポート径・Y長さ=slot_len」の角丸スロット（正円ではなくY方向に長い）。X幅はポート径の
    ままにして隣の列へ漏らさない。step_y は行間隔(mm, 既定 STEP_Y)。和音は {0,2,4} のように複数。"""
    if step_y is None:
        step_y = STEP_Y
    if W is None:
        # 幅はチャンバーのレール間隔(reader_monolithic と同じ式)から決める＝スリットに収まる。
        x_rail = (n - 1) / 2.0 * pitch + pitch * 0.75    # レール中心
        rail_gap = 2 * x_rail - 2.0                       # レール(幅2mm)内側どうしの間隔
        W = rail_gap - 2.0                                # 片側1mmの横クリアランス（ポート±(n-1)/2*pitch は覆う）
    steps = len(score)
    L = lead * 2 + steps * step_y                # 帯の長さ(Y)
    strip = trimesh.creation.box(extents=[W, L, SHEET_T]); strip.apply_translation([0, 0, SHEET_T / 2])
    xs = [(-(n - 1) / 2 + i) * pitch for i in range(n)]
    holes = []
    for t, notes in enumerate(score):
        y = -L / 2 + lead + (t + 0.5) * step_y
        for i in notes:
            holes.append(_y_slot(xs[i], y, slot_len, r=SHEET_HOLE_R))
    if holes:
        strip = trimesh.boolean.difference([strip, trimesh.boolean.union(holes, engine="manifold")], engine="manifold")
    info = dict(n=n, steps=steps, W=W, L=L, slot_len=slot_len, step_y=step_y, land=step_y - slot_len,
                dims=tuple(np.round(strip.extents, 1)))
    return strip, info


# ---------------------------------------------------------------------------
# 印刷可能な分割：チャンバー天井(幅広ブリッジ不可)を避け、
#   base = 上面開放トレー（床＋壁＋吹込口＋合わせリム）
#   lid  = ポート板＋シート溝レール＋リム内に落ちる段（baseに嵌めて接着）
# の2部品にする。両方とも平物で無理なく刷れる。
# ---------------------------------------------------------------------------
def reader_base(n=8, pitch=8.0, chest_h=12.0, depth=22.0, bore_d=6.0, spigot_len=8.0):
    """加圧チャンバー（上面開放トレー）。

    -X 端面に外向きのスピゴット（差込口）を立て、直径 bore_d（既定6mm）の円筒で
    チャンバー内部まで貫通させてくり抜く。ここへゴムチューブを差し込み、息または
    空気ポンプで送気する。スピゴットはチューブを掴む長さ（spigot_len）を稼ぐための
    肉厚 WALL の筒で、外径は bore_d + 2*WALL になる。
    """
    W = n * pitch + 2 * WALL + 8.0
    outer = trimesh.creation.box(extents=[W, depth, chest_h]); outer.apply_translation([0, 0, chest_h / 2])
    # 上面開放の内空洞（上に WALL 分の縁は残さず開ける）
    inner = trimesh.creation.box(extents=[W - 2 * WALL, depth - 2 * WALL, chest_h])
    inner.apply_translation([0, 0, chest_h / 2 + WALL])          # 上へずらして天井を無くす＝開放
    base = trimesh.boolean.difference([outer, inner], engine="manifold")
    # 送気スピゴット（差込口）：外向きの筒を足してチューブ挿入代を確保
    bore_r = bore_d / 2.0
    boss_r = bore_r + WALL                                       # 外径 = bore_d + 2*WALL
    boss_len = spigot_len + WALL                                 # 外側 spigot_len ＋ 壁厚ぶん
    boss = trimesh.creation.cylinder(radius=boss_r, height=boss_len, sections=48)
    boss.apply_transform(trimesh.transformations.rotation_matrix(np.radians(90), [0, 1, 0]))
    boss.apply_translation([-W / 2 - spigot_len + boss_len / 2, 0, chest_h / 2])
    base = trimesh.boolean.union([base, boss], engine="manifold")
    # 直径 bore_d の円筒でくり抜き：スピゴット外端からチャンバー内部まで貫通させる
    bore_len = spigot_len + WALL + 4.0                           # チャンバー内へ 4mm 突き抜けて確実に開通
    bore = trimesh.creation.cylinder(radius=bore_r, height=bore_len, sections=48)
    bore.apply_transform(trimesh.transformations.rotation_matrix(np.radians(90), [0, 1, 0]))
    bore.apply_translation([-W / 2 - spigot_len + bore_len / 2, 0, chest_h / 2])
    base = trimesh.boolean.difference([base, bore], engine="manifold")
    info = dict(W=W, depth=depth, chest_h=chest_h, n=n, pitch=pitch,
                bore_d=bore_d, spigot_len=spigot_len, boss_od=round(2 * boss_r, 1))
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
# 一体版チャンバー（①土台＋②蓋＋シートレールを継ぎ目なしで一体化）。
# ①↔②の合わせ目が無いので、加圧チャンバーの漏れの心配が消える。
# 送気口を +Z に向けて印刷する前提：-X端を45°テントに絞り、その頂点に縦向きの送気口ボスを付ける。
# これで spigot-up 印刷は「内部天井=45°以下・送気口=縦筒・ポート=横穴のブリッジ」となりサポート無し
# で刷れる（実機スライスで押出0を確認）。使用時は送気口を横・ポート面を上にして使う。
# パンフルート(④)はシートを挟んで動かすため一体化できず、別部品で嵌め合い＋押さえにする。
# ---------------------------------------------------------------------------
def _x_cyl(r, x_a, x_b, y, z, sections=48):
    """X軸に沿う円柱（x_a〜x_b, 中心(y,z)）。"""
    c = trimesh.creation.cylinder(radius=r, height=abs(x_b - x_a), sections=sections)
    c.apply_transform(trimesh.transformations.rotation_matrix(np.radians(90), [0, 1, 0]))
    c.apply_translation([(x_a + x_b) / 2.0, y, z])
    return c


def reader_monolithic(n=8, pitch=8.0, depth=24.0, H=16.0, bore_d=6.0, spigot_len=8.0, taper=11.0):
    """一体版チャンバー（使用姿勢＝ポート面が+Z・送気口が-X）。印刷は spigot-up 姿勢で。"""
    W = n * pitch + 2 * WALL + 8.0
    x0 = -W / 2.0; cav_x0 = x0 + WALL; xr = W / 2.0
    boss_r = bore_d / 2.0 + WALL
    hull = lambda pts: trimesh.PointCloud(np.array(pts)).convex_hull
    # 外形：本体箱 ＋ -Xテント(frustum) ＋ 送気口ボス
    body = trimesh.creation.box(extents=[W, depth, H]); body.apply_translation([0, 0, H / 2])
    rectO = [[x0, sy * depth / 2, H / 2 + sz * H / 2] for sy in (-1, 1) for sz in (-1, 1)]
    tipO = [[x0 - taper, sy * boss_r, H / 2 + sz * boss_r] for sy in (-1, 1) for sz in (-1, 1)]
    body = trimesh.boolean.union([body, hull(rectO + tipO)], engine="manifold")
    body = trimesh.boolean.union([body, _x_cyl(boss_r, x0 - taper - spigot_len, x0 - taper + 1, 0, H / 2)], engine="manifold")
    # 空洞：本体空洞箱 ＋ -X空洞frustum（ボア径へ絞る＝spigot-upの天井が45°以下）
    cav_main = trimesh.creation.box(extents=[(xr - WALL) - (cav_x0 + taper), depth - 2 * WALL, H - 2 * WALL])
    cav_main.apply_translation([((cav_x0 + taper) + (xr - WALL)) / 2.0, 0, H / 2])
    rectC = [[cav_x0 + taper, sy * (depth / 2 - WALL), H / 2 + sz * (H / 2 - WALL)] for sy in (-1, 1) for sz in (-1, 1)]
    tipC = [[cav_x0, sy * bore_d / 2, H / 2 + sz * bore_d / 2] for sy in (-1, 1) for sz in (-1, 1)]
    cav = trimesh.boolean.union([cav_main, hull(rectC + tipC)], engine="manifold")
    body = trimesh.boolean.difference([body, cav], engine="manifold")
    # 送気口ボア（-X貫通で空洞へ）
    body = trimesh.boolean.difference([body, _x_cyl(bore_d / 2.0, x0 - taper - spigot_len - 1, cav_x0 + 2, 0, H / 2)], engine="manifold")
    # ポート列（上面 z=H を貫通、y=0 読み取り線）
    xs = [(-(n - 1) / 2 + i) * pitch for i in range(n)]
    ports = [trimesh.creation.cylinder(radius=PORT_R, height=2 * WALL + 2, sections=32) for _ in xs]
    for p, x in zip(ports, xs):
        p.apply_translation([x, 0, H - WALL / 2])
    body = trimesh.boolean.difference([body, trimesh.boolean.union(ports, engine="manifold")], engine="manifold")
    # シート溝レール（上面, ポートの外側 x=±x_rail に沿ってY方向の壁）。
    # 高さ＝シート溝の高さ。この上面に笛バンクの穴あき板を接着すると、シート厚ぶんの
    # スリットだけが残る。spigot-up 印刷でサポートが付かないよう内向きリップは付けない。
    rail_h = SHEET_T + 2 * SLOT_CL
    x_rail = (n - 1) / 2.0 * pitch + pitch * 0.75
    rails = []
    for sx in (-1, 1):
        b = trimesh.creation.box(extents=[2.0, depth, rail_h]); b.apply_translation([sx * x_rail, 0, H + rail_h / 2])
        rails.append(b)
    body = trimesh.boolean.union([body] + rails, engine="manifold")
    info = dict(W=W, depth=depth, H=H, ports_x=xs, bore_d=bore_d, x_rail=x_rail,
                dims=tuple(np.round(body.extents, 1)))
    return body, info


def reader_monolithic_printpose(**kw):
    """spigot-up（送気口を+Zに向けた）印刷姿勢のメッシュを返す。"""
    body, info = reader_monolithic(**kw)
    body = body.copy()
    body.apply_transform(trimesh.transformations.rotation_matrix(np.radians(90), [0, 1, 0]))
    body.apply_translation([0, 0, -body.bounds[0][2]])
    info = dict(info); info["print_dims"] = tuple(np.round(body.extents, 1))
    return body, info


# ---------------------------------------------------------------------------
# オルガン用パンフルート（吹込口一列版）：縦の閉管mini笛をポートピッチで一列に。
# 各笛はヘッド(下から吹く)を下端にし、吹込口(底 z=0)をポート位置に一致させて載せる。
# 音は共鳴管長で決める（閉管 予測式を流用）。上部の連結板で一体化（底=吹込口は開放）。
# ---------------------------------------------------------------------------
def organ_panflute(notes=None, pitch=8.0, round_bore=False, web=True, fold=2):
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
        if fold and fold >= 2:
            # 実績の1回折れ（flat_flute N=fold・丸ボア面内蛇行）を『立てたまま』縦笛に。
            # 直管はこのオクターブで安定発音しない（実機確認）ため折れ版を採用。
            pipe, pinfo = mini.flat_flute(note=note, N=fold, head=head.copy(), flatten=False)
            pipe.apply_translation([x, 0, 0])          # ボア(=原点)→ポート位置x
            freq = pinfo["freq"]; zt = None
        else:
            zt = mini.z_top_for_note(note)             # 直管（旧）
            ext = mini._bore_extension(zt, round_bore=round_bore)
            pipe = trimesh.util.concatenate([head.copy(), ext])
            pipe.apply_translation([-mini.CX + x, -mini.CY, 0])
            freq = mini.predict_freq(zt)
        pipes.append(pipe)
        infos.append(dict(note=note, x=x, z_top=zt, freq=freq))
    body = trimesh.util.concatenate(pipes)
    if web:
        # 連結板（z=20〜24）。ボア中心(x_i,0)を通るので、そのままだと各笛のボアを塞ぐ
        # （2026/7/14 発覚：気柱が分断され鳴らなかった真因）。ボア逃げ穴を開けて桁だけ残す。
        b0, b1 = body.bounds
        webbox = trimesh.creation.box(extents=[b1[0] - b0[0] + 2, 8.0, 4.0])
        webbox.apply_translation([(b0[0] + b1[0]) / 2, 0, 22.0])
        clr = mini.BORE / 2.0 + 0.4                    # ボア半径+0.4mmの逃げ
        holes = [trimesh.creation.cylinder(radius=clr, height=4 + 2, sections=40) for _ in xs]
        for hh, x in zip(holes, xs):
            hh.apply_translation([x, 0, 22.0])
        webbox = trimesh.boolean.difference([webbox, trimesh.boolean.union(holes, engine="manifold")], engine="manifold")
        body = trimesh.boolean.union([body, webbox], engine="manifold")
    mesh = body
    info = dict(notes=notes, xs=xs, pitch=pitch, pipes=infos, web=web, dims=tuple(np.round(mesh.extents, 1)))
    return mesh, info


# ---------------------------------------------------------------------------
# 完全一体オルガン：チャンバー＋ポート＋シート溝＋丸ボアの笛バンクを一体化（可動はシートだけ）。
# spigot-up で印刷すると、丸ボアが横倒しで自己ブリッジしてボア内部にはサポートが入らない
# （実測で半径2.5mm以内のサポート0）。笛どうしの間の外部サポートは外から切除できる。
# 送気口⊥笛の二律背反は、笛を丸ボア化して spigot-up でブリッジさせることで解いている。
# ---------------------------------------------------------------------------
def pipe_bank(notes=None, pitch=8.0, plate_t=2.0):
    """笛バンク＝穴あき接合板＋丸ボア笛。逆順（長管=低音を+x側へ）で spigot-up の
    print-z 低側に長い管が来てサポートが減る。板の穴は各ポート位置(x_i,0)。
    板の下面（z=-plate_t）をチャンバーのレール上面に接着すると、シート厚スリットが残る。"""
    if notes is None:
        notes = ["C6", "D6", "E6", "F6", "G6", "A6", "B6", "C7"]
    rev = list(notes)[::-1]                               # 逆順：長管を+xへ
    # web=False：オルガンでは下の穴あき板＋チャンバーで一体化されるので連結板は不要
    # （連結板はボアを塞ぐため使わない。2026/7/14修正）
    pan, pi = organ_panflute(notes=rev, pitch=pitch, round_bore=True, web=False)
    # v3吸込口の底(z=-4)が板の上面(z=0)にちょうど載るよう持ち上げる。こうしないと
    # 外Ø7スピゴットが板を突き抜けてシート溝に突き出し、シートのスクロールを妨げる。
    pan.apply_translation([0, 0, -pan.bounds[0][2]])       # 吸込口の底 → z=0（板上面に着座）
    xs = pi["xs"]; b0, b1 = pan.bounds
    plate = trimesh.creation.box(extents=[(b1[0] - b0[0]) + 4.0, b1[1] - b0[1] + 4.0, plate_t])
    plate.apply_translation([(b0[0] + b1[0]) / 2.0, (b0[1] + b1[1]) / 2.0, -plate_t / 2.0])
    # 板の穴＝Ø6（PORT_R）で各吸込口ボア(x_i,0)と同軸に貫通
    holes = [trimesh.creation.cylinder(radius=PORT_R, height=plate_t + 2, sections=32) for _ in xs]
    for hh, x in zip(holes, xs):
        hh.apply_translation([x, 0, -plate_t / 2.0])
    plate = trimesh.boolean.difference([plate, trimesh.boolean.union(holes, engine="manifold")], engine="manifold")
    bank = trimesh.boolean.union([pan, plate], engine="manifold")
    info = dict(notes=rev, ports_x=xs, plate_t=plate_t, dims=tuple(np.round(bank.extents, 1)))
    return bank, info


def organ_monolithic(notes=None, pitch=8.0, slot=None, plate_t=2.0):
    """完全オルガンを「2部品＋接着」で構成して返す（part A, part B, 組立情報）。
      A = チャンバー＋ポート＋シート溝レール（reader_monolithic, spigot-up印刷）
      B = 笛バンク（pipe_bank：穴あき板＋丸ボア笛, spigot-up印刷）
    B の板下面を A のレール上面(z=H+slot)に接着すると、z=H..H+slot のシート厚スリットが残り、
    そこをシートがスクロールする。"""
    if notes is None:
        notes = ["C6", "D6", "E6", "F6", "G6", "A6", "B6", "C7"]
    if slot is None:
        slot = SHEET_T + 2 * SLOT_CL
    chamber, ci = reader_monolithic(n=len(notes), pitch=pitch)
    bank, bi = pipe_bank(notes=notes, pitch=pitch, plate_t=plate_t)
    info = dict(notes=notes, ports_x=ci["ports_x"], H=ci["H"], slot=slot, plate_t=plate_t,
                chamber_dims=tuple(np.round(chamber.extents, 1)), bank_dims=bi["dims"],
                bank_notes=bi["notes"])
    return chamber, bank, info


def organ_onepiece(notes=None, pitch=8.0, slot=None, plate_t=2.0):
    """完全一体オルガン（1部品・接着不要）：チャンバー＋ポート＋シート溝＋穴あき板＋丸ボア笛。
    笛バンクの穴あき板をチャンバーのレール上面に載せて一体化。可動はシートだけ。
    逆順（長管を print-z 低側へ）＋丸ボアなので、spigot-up 印刷はサポートが最下部(z<約7mm)の
    ブリム際だけで、スリット・ボア・笛はすべて空いたまま刷れる（実機スライスで確認）。"""
    if notes is None:
        notes = ["C6", "D6", "E6", "F6", "G6", "A6", "B6", "C7"]
    if slot is None:
        slot = SHEET_T + 2 * SLOT_CL
    chamber, ci = reader_monolithic(n=len(notes), pitch=pitch)
    bank, bi = pipe_bank(notes=notes, pitch=pitch, plate_t=plate_t)
    bank = bank.copy(); bank.apply_translation([0, 0, ci["H"] + slot + plate_t])  # 板下面→レール上面(z=H+slot)
    mesh = trimesh.util.concatenate([chamber, bank])
    info = dict(notes=notes, bank_notes=bi["notes"], H=ci["H"], slot=slot, plate_t=plate_t,
                dims=tuple(np.round(mesh.extents, 1)))
    return mesh, info


def _spigotup(mesh):
    m = mesh.copy()
    m.apply_transform(trimesh.transformations.rotation_matrix(np.radians(90), [0, 1, 0]))
    m.apply_translation([0, 0, -m.bounds[0][2]])
    return m


def main():
    import sys
    os.makedirs(OUT, exist_ok=True)
    if "--split" in sys.argv:
        base, bi = reader_base(); base.export(os.path.join(OUT, "organ_reader_base.stl"))
        lid, li = reader_lid(); lid.export(os.path.join(OUT, "organ_reader_lid.stl"))
        print("分割リーダー：base(上面開放トレー)＋lid(ポート板＋レール)")
        print("  base -> out/organ_reader_base.stl 外形%s watertight=%s" % (tuple(np.round(base.extents, 1)), base.is_watertight))
        print("       吸気口=-X端スピゴット 穴Ø%.1fmm(貫通)/外径Ø%.1fmm/差込長%.1fmm ← ゴムチューブを差して送気" %
              (bi["bore_d"], bi["boss_od"], bi["spigot_len"]))
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
    if "--mono" in sys.argv:
        body, bi = reader_monolithic()
        body.export(os.path.join(OUT, "organ_reader_monolithic.stl"))
        pbody, pi = reader_monolithic_printpose()
        pbody.export(os.path.join(OUT, "organ_reader_monolithic_spigotup.stl"))
        print("一体版チャンバー（①土台＋②ポート＋シートレール・継ぎ目なし）:")
        print("  使用姿勢 外形%s watertight=%s 送気口Ø%.1f ポートx=%s" %
              (bi["dims"], body.is_watertight, bi["bore_d"], [round(x, 1) for x in bi["ports_x"]]))
        print("  印刷姿勢(spigot-up) 外形%s -> out/organ_reader_monolithic_spigotup.stl（送気口が+Z）" % (pi["print_dims"],))
        print("  -> out/organ_reader_monolithic.stl / out/organ_reader_monolithic_spigotup.stl")
        return
    if "--mono-organ" in sys.argv:
        one, oi = organ_onepiece()
        oa = _spigotup(one); oa.export(os.path.join(OUT, "organ_onepiece_spigotup.stl"))
        print("完全一体オルガン（1部品・接着不要・可動はシートだけ）:")
        print("  spigot-up 外形%s watertight=%s 音(print-z 下→上)=%s" %
              (tuple(np.round(oa.extents, 1)), one.is_watertight, oi["bank_notes"]))
        print("  ※逆順(長管を下層)＋丸ボア＝サポートは最下部(z<約7mm)のブリム際だけ。スリット/ボア/笛は空き。")
        print("  -> out/organ_onepiece_spigotup.stl")
        if "--split" in sys.argv:
            chamber, bank, mi = organ_monolithic()
            _spigotup(chamber).export(os.path.join(OUT, "organ_chamber_spigotup.stl"))
            _spigotup(bank).export(os.path.join(OUT, "organ_pipebank_spigotup.stl"))
            print("  （--split 併用：2部品版も出力 -> organ_chamber_spigotup.stl / organ_pipebank_spigotup.stl）")
        return
    if "--pressure-test" in sys.argv:
        score = [set(range(k + 1)) for k in range(8)]     # 1本→8本を1行ずつ増やす
        sheet, si = punched_sheet(score, n=8, slot_len=6.0, step_y=12.0)
        sheet.export(os.path.join(OUT, "organ_sheet_pressure_test.stl"))
        print("同時発音テストシート（1→8本を1行ずつ・Y方向スロット）:")
        print("  行数%d 各行の同時本数=%s" % (si["steps"], [len(s) for s in score]))
        print("  スロット長%.1fmm・行間隔%.1fmm・ランド(閉じ)%.1fmm 外形%s watertight=%s" %
              (si["slot_len"], si["step_y"], si["land"], si["dims"], sheet.is_watertight))
        print("  -> out/organ_sheet_pressure_test.stl")
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
