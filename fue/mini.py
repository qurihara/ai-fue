"""mini-c-v2 ベースの極小笛ジェネレータ（音域探索・モジュール化・折り）。

mini/recorder-mini-c-v2.stl は 7×7×40mm の極小閉管リコーダー（Tinkercad製、印刷&
発音実績あり）。下16mmが発音部（ウインドウェイ＋窓＋ラビウム、下から吹く）、上が
共鳴ボア（内寸6.06角、上端閉）。音程を決めるのは共鳴ボア長だけなので、実績ヘッドを
そのまま残し、上に「任意長の閉じ角ボア」を生やして音程を振る。

  ・直管スイープ … ボア上端 z_top を変えて音程スイープ（音域の地図づくり）
  ・折り        … 低い音でボアが長くなるぶんを蛇行で畳んで寸法を保つ

較正（実測1点＋閉管理論）:
  f ≈ c/(4·Leff),  Leff = (z_top − Z_WINDOW) + ENDCORR
  原型 z_top=39.5 → 約F7(2750Hz) にフィットするよう ENDCORR≈4.5mm。
  実測が増えたら ENDCORR / Z_WINDOW を更新する。

実行には trimesh + manifold3d（fold.py / box.py と同じ環境）。
"""
import os
import sys
import argparse
import numpy as np
import trimesh

sys.path.insert(0, os.path.dirname(__file__))
import fold  # _note_freq, centerline, bore_solid

ROOT = os.path.join(os.path.dirname(__file__), os.pardir)
MINI_STL = os.path.join(ROOT, "mini", "recorder-mini-c-v2.stl")
OUT = os.path.join(ROOT, "out")

# --- mini-c-v2 の実測ジオメトリ ---
FOOT = 7.0            # 外形 7×7mm
BORE = 6.06           # ボア内寸（角）
CX, CY = 1.5, -16.0   # x/y中心
CUT_Z = 18.0          # ヘッド切断面（窓の少し上、ボアが素直な所）
Z_WINDOW = 13.0       # 窓（音響的な開口端）のz
TOP_CAP = 2.0         # 生やすボアの上端キャップ厚
ENDCORR = 1.9         # 端補正(mm)。2026/7/7 C6直管(N1)実測で 4.5→1.9 に更新（直管が+55c上ずり）
FLAT_FOLD_CORR = 3.5  # flat折り補正(mm/折)。折り1回ごとに実効長が縮み音程が上がる。
                      # 2026/7/7 C6でN=1/2/3実測（1081/1134/1184Hz）→約3.4-3.7mm/折。旧compact.py 3.3と一致
C4 = 343000.0 / 4.0   # c/4 (mm/s /4)


def predict_freq(z_top):
    """ボア上端z_topから発音周波数(Hz)を予測（閉管＋端補正）。"""
    return C4 / (z_top - Z_WINDOW + ENDCORR)


def z_top_for_freq(f):
    return Z_WINDOW - ENDCORR + C4 / f


def z_top_for_note(note):
    return z_top_for_freq(fold._note_freq(note))


def _mini_head():
    """実績ヘッド：mini-c-v2 を z≤CUT_Z で切り出す（発音部を保持）。"""
    m = trimesh.load(MINI_STL)
    big = trimesh.creation.box(extents=[FOOT + 4, FOOT + 4, CUT_Z + 2])
    big.apply_translation([CX, CY, (CUT_Z + 2) / 2.0 - 1.0])   # z -1..CUT_Z
    head = trimesh.boolean.intersection([m, big], engine="manifold")
    return head


def _bore_extension(z_top):
    """ヘッド上に生やす閉じ角ボア。外形7×7・内寸BORE、z=CUT_Z-1..z_top（上端閉）。"""
    z0 = CUT_Z - 1.0
    outer = trimesh.creation.box(extents=[FOOT, FOOT, (z_top + TOP_CAP) - z0])
    outer.apply_translation([CX, CY, (z0 + z_top + TOP_CAP) / 2.0])
    # ボア空洞: z=CUT_Z-2 .. z_top（上端で閉じ、下はヘッドのボアへ連結）
    void = trimesh.creation.box(extents=[BORE, BORE, z_top - (CUT_Z - 2.0)])
    void.apply_translation([CX, CY, ((CUT_Z - 2.0) + z_top) / 2.0])
    return trimesh.boolean.difference([outer, void], engine="manifold")


def straight_flute(z_top=None, note=None, head=None):
    """直管の極小笛。head(切り出し済)を渡すと再利用（コーム生成で高速化）。"""
    if z_top is None:
        z_top = z_top_for_note(note)
    h = head if head is not None else _mini_head()
    ext = _bore_extension(z_top)
    flute = trimesh.util.concatenate([h, ext])
    flute.apply_translation([-CX, -CY, 0])          # x/y中心を原点へ
    info = dict(z_top=z_top, total_H=z_top + TOP_CAP, freq=predict_freq(z_top), kind="straight")
    return flute, info


def straight_comb(z_tops, gap=4.0):
    """直管スイープを横一列に並べた測定用コーム。"""
    head = _mini_head()
    flutes, infos = [], []
    xoff = 0.0
    pitch = FOOT + gap
    for i, zt in enumerate(z_tops):
        f, info = straight_flute(z_top=zt, head=head)
        f.apply_translation([xoff, 0, 0])
        info["x"] = xoff
        xoff += pitch
        flutes.append(f)
        infos.append(info)
    return trimesh.util.concatenate(flutes), infos


# ---------------------------------------------------------------------------
# 折り版：低い音でボアが長くなるぶんを蛇行で畳む（fold.py と同趣旨、square bore）。
# 発音ヘッド(7×7)は残し、その上に N本の縦パスの蛇行ボアを +x 方向に並べる。
# 幾何路長（窓→閉端）が直管と同じになるよう z_high を解く。折り補正は実測で更新。
# ---------------------------------------------------------------------------
def _zbox(x, z0, z1, b):
    box = trimesh.creation.box(extents=[b, b, z1 - z0])
    box.apply_translation([x, 0, (z0 + z1) / 2.0])
    return box


def _turn(x, z, pitch, b, top):
    box = trimesh.creation.box(extents=[pitch + b, b, b])
    box.apply_translation([x, 0, z - b / 2.0 if top else z + b / 2.0])
    return box


def folded_flute(note=None, Lg=None, N=2, z_low=4.0, head=None):
    """折り版の極小笛。N=縦パス本数。幾何路長を直管と揃え、背を~1/N に畳む。"""
    b, pitch, cap = BORE, FOOT, TOP_CAP
    if Lg is None:
        Lg = z_top_for_note(note) - Z_WINDOW          # 窓から上の幾何ボア長
    z_high = (Lg + Z_WINDOW - (N - 1) * pitch + (N - 1) * z_low) / N
    H = z_high + cap
    h = (head if head is not None else _mini_head()).copy()
    h.apply_translation([-CX, -CY, 0])                # ボアを原点へ
    x0, x1 = -FOOT / 2, (N - 1) * pitch + FOOT / 2
    solid = trimesh.creation.box(extents=[x1 - x0, FOOT, H])
    solid.apply_translation([(x0 + x1) / 2.0, 0, H / 2.0])
    slot = trimesh.creation.box(extents=[FOOT + 0.02, FOOT + 0.02, CUT_Z + 0.5])
    slot.apply_translation([0, 0, (CUT_Z + 0.5) / 2.0 - 0.25])
    solid = trimesh.boolean.difference([solid, slot], engine="manifold")   # ヘッド用スロット
    voids = [_zbox(0, 16.0, z_high, b)]               # pass0（ヘッドボアへ連結）
    for i in range(1, N):
        voids.append(_zbox(i * pitch, z_low, z_high, b))
    for i in range(N - 1):                            # 折り返し（上下交互）
        voids.append(_turn((i + 0.5) * pitch, z_high if i % 2 == 0 else z_low, pitch, b, top=(i % 2 == 0)))
    void = trimesh.boolean.union(voids, engine="manifold")
    hollow = trimesh.boolean.difference([solid, void], engine="manifold")
    flute = trimesh.util.concatenate([hollow, h])
    bb = flute.bounds
    flute.apply_translation([-(bb[0][0] + bb[1][0]) / 2.0, -(bb[0][1] + bb[1][1]) / 2.0, 0])
    info = dict(N=N, z_high=z_high, total_H=H, W=x1 - x0, freq=C4 / (Lg + ENDCORR), kind="fold%d" % N)
    return flute, info


# ---------------------------------------------------------------------------
# flat版：笛を寝かせて印刷（窓は横向き）。延長ボアは丸断面で同一平面(z-y)を蛇行。
# 横向き丸ボアはブリッジで架かる＝延長部はサポート不要。背が低い平物で安定。
# ---------------------------------------------------------------------------
def _round_serpentine_void(pts, r):
    parts = []
    for k in range(len(pts) - 1):
        parts.append(trimesh.creation.cylinder(radius=r, segment=[pts[k], pts[k + 1]], sections=32))
    for p in pts[1:-1]:
        s = trimesh.creation.icosphere(subdivisions=2, radius=r)
        s.apply_translation(p)
        parts.append(s)
    return trimesh.boolean.union(parts, engine="manifold")


def flat_flute(note=None, Lg=None, N=3, z_low=4.0, r=3.0, end_wall=1.2, pitch=7.0, head=None):
    """flat印刷用：実績ヘッド＋丸ボアの面内蛇行。出力STLは既にflat向き（窓横向き）。
    end_wall: +x端（折り返しがある端）の外側に残す壁厚(mm)。折り返しは半径 r の丸みで
    z_high+r まで張り出すため、端の壁は最低でも r 分を見込む必要がある。旧版は端壁が
    TOP_CAP=2mm しか無く r=3mm の折り返しが端面を突き抜けて穴が開いていた（実機で確認）。"""
    if Lg is None:
        # 折り補正：折り1回ごとに実効長が縮む(音程が上がる)ので、その分だけ幾何路長を伸ばす
        Lg = (z_top_for_note(note) - Z_WINDOW) + FLAT_FOLD_CORR * (N - 1)
    z_high = (Lg + Z_WINDOW - (N - 1) * pitch + (N - 1) * z_low) / N
    H = z_high + r + end_wall          # 折り返し(半径r)を end_wall で確実に包む
    h = head if head is not None else _mini_head()
    pts = [[CX, CY, 16.0], [CX, CY, z_high]]          # pass0（ヘッドボアへ連結）
    cur = z_high
    for i in range(1, N):
        yi = CY + i * pitch
        pts.append([CX, yi, cur])                     # 面内ターン(y方向)
        nz = z_low if cur == z_high else z_high
        pts.append([CX, yi, nz]); cur = nz            # 縦パス
    void = _round_serpentine_void([np.array(p, float) for p in pts], r)
    y0, y1 = CY - FOOT / 2, CY + (N - 1) * pitch + FOOT / 2
    solid = trimesh.creation.box(extents=[FOOT, y1 - y0, H])
    solid.apply_translation([CX, (y0 + y1) / 2.0, H / 2.0])
    slot = trimesh.creation.box(extents=[FOOT + 0.02, FOOT + 0.02, CUT_Z + 0.5])
    slot.apply_translation([CX, CY, (CUT_Z + 0.5) / 2.0 - 0.25])
    solid = trimesh.boolean.difference([solid, slot], engine="manifold")
    hollow = trimesh.boolean.difference([solid, void], engine="manifold")
    flute = trimesh.util.concatenate([hollow, h])
    # flat向きにベイク（y軸まわり90°→管軸を水平・窓を横向き）、ベッドに落とし中心化
    flute.apply_transform(trimesh.transformations.rotation_matrix(np.radians(90), [0, 1, 0]))
    flute.apply_translation([0, 0, -flute.bounds[0][2]])
    bb = flute.bounds
    flute.apply_translation([-(bb[0][0] + bb[1][0]) / 2.0, -(bb[0][1] + bb[1][1]) / 2.0, 0])
    # 実際に鳴る音＝幾何路長から折り縮みを差し引いた実効長で予測（Lgは折り補正込みなので相殺）
    freq = C4 / (Lg + ENDCORR - FLAT_FOLD_CORR * (N - 1))
    info = dict(N=N, z_high=z_high, freq=freq, r=r, kind="flat%d" % N,
                dims=tuple(np.round(flute.extents, 1)))
    return flute, info


def flat_measure_comb(specs=None, gap=5.0):
    """flat版の測定コーム：面内蛇行の丸ボア笛を数本、横一列に（実質サポートフリー）。"""
    if specs is None:
        specs = [("C7", 2), ("A6", 2), ("F6", 3), ("C6", 3)]
    head = _mini_head()
    flutes, infos = [], []
    cursor = 0.0
    for note, N in specs:
        f, info = flat_flute(note=note, N=N, head=head)
        w = f.extents[0]
        f.apply_translation([cursor + w / 2.0, 0, 0])
        info["label"] = "%s(f%d)" % (note, N)
        info["x"] = cursor
        cursor += w + gap
        flutes.append(f)
        infos.append(info)
    return trimesh.util.concatenate(flutes), infos


def fold_sweep_comb(note="C6", Ns=(1, 2, 3), gap=6.0):
    """音（＝路長）を固定し折り数 N だけ振るコーム。各笛を y方向に段積み（長さが大きく
    違うため）。同一路長でNを変える→音程差＝折り補正、鳴りやすさ差＝発音性 vs 折り。
    N=1は直管（折り0）、N=2は1折り、N=3は2折り…（折り回数 = N−1）。"""
    head = _mini_head()
    flutes, infos = [], []
    yoff = 0.0
    for N in Ns:
        f, info = flat_flute(note=note, N=N, head=head)
        hy = f.extents[1]
        f.apply_translation([0.0, yoff + hy / 2.0, 0.0])   # x中心、y段積み
        info["label"] = "%s N%d(%df)" % (note, N, N - 1)
        info["y"] = yoff
        yoff += hy + gap
        flutes.append(f)
        infos.append(info)
    mesh = trimesh.util.concatenate(flutes)
    bb = mesh.bounds
    mesh.apply_translation([-(bb[0][0] + bb[1][0]) / 2.0, -(bb[0][1] + bb[1][1]) / 2.0, 0])
    return mesh, infos


# ---------------------------------------------------------------------------
# パンフルート：1オクターブの管を一体化した楽器。
# 各管は実績の flat_flute（既定N=2=1折り、低音のスイートスポット）。ヘッド(吹込端=-x)を
# x=0 に揃える。積み方向 axis="z" で C6 を最下段に D6→…→C7 と z方向に積む（フットプリント
# 最小のブロック＝モジュール化向き）。axis="y" なら横並び。gap=0 で段が密着し一体化する。
# 窓は側面(±y)、吹込口は前面(x=0)で、各段は別zに来るので塞がない。土台(プレート)は付けない。
# ---------------------------------------------------------------------------
def pan_flute(notes=None, N=2, gap=0.0, axis="z", mirror_y=None):
    if notes is None:
        notes = ["C6", "D6", "E6", "F6", "G6", "A6", "B6", "C7"]   # Cメジャー1オクターブ
    if mirror_y is None:
        mirror_y = [False] * len(notes)
    head = _mini_head()
    flutes, infos = [], []
    off = 0.0
    for i, note in enumerate(notes):
        f, info = flat_flute(note=note, N=N, head=head)
        if mirror_y[i]:
            f.apply_transform(np.diag([1.0, -1.0, 1.0, 1.0]))     # y方向に鏡像（窓が −y→+y へ）
            f.fix_normals()
        f.apply_translation([-f.bounds[0][0], 0.0, 0.0])          # ヘッド端を x=0 に揃える
        cy = (f.bounds[0][1] + f.bounds[1][1]) / 2.0
        if axis == "z":
            f.apply_translation([0.0, -cy, off - f.bounds[0][2]])  # y中心、z方向に積む(min_z=off)
            off += f.extents[2] + gap
        else:
            f.apply_translation([0.0, off - f.bounds[0][1], 0.0])  # +y に段積み
            off += f.extents[1] + gap
        info["label"] = note
        info["mirror_y"] = mirror_y[i]
        info["off"] = off
        flutes.append(f)
        infos.append(info)
    mesh = trimesh.util.concatenate(flutes)
    bb = mesh.bounds
    mesh.apply_translation([-(bb[0][0] + bb[1][0]) / 2.0, -(bb[0][1] + bb[1][1]) / 2.0, -bb[0][2]])
    return mesh, infos


def measure_comb(gap=4.0):
    """較正用の少数スイープ：直管2本(F7,C7)＋折り1本(C6, N=3)。
    直管2点で ENDCORR を較正し、折りC6で折り補正と低音側を確認。"""
    head = _mini_head()
    specs = []
    f, i = straight_flute(note="F7", head=head); i["label"] = "F7直"; specs.append((f, i))
    f, i = straight_flute(note="C7", head=head); i["label"] = "C7直"; specs.append((f, i))
    f, i = folded_flute(note="C6", N=3, head=head); i["label"] = "C6折3"; specs.append((f, i))
    flutes, infos = [], []
    xoff = 0.0
    for f, info in specs:
        w = f.extents[0]
        f.apply_translation([xoff + w / 2.0, 0, 0])
        info["x"] = xoff
        xoff += w + gap
        flutes.append(f)
        infos.append(info)
    return trimesh.util.concatenate(flutes), infos


def main():
    ap = argparse.ArgumentParser(description="mini-c-v2ベースの極小笛（音域スイープ）")
    ap.add_argument("--note", help="単一笛：狙いの音（例 C6）")
    ap.add_argument("--ztop", type=float, help="単一笛：ボア上端z(mm)を直接指定")
    ap.add_argument("--sweep", help="スイープ：z_topのリスト（例 39.5,50,60,70）")
    ap.add_argument("--notes", help="スイープ：音名リスト（例 'F7 C7 G6 F6'）")
    ap.add_argument("--fold", type=int, default=0, help="単一笛を折り版で（縦パス本数N、例 3）")
    ap.add_argument("--measure-comb", action="store_true", help="較正用の少数スイープ(F7直/C7直/C6折3)")
    ap.add_argument("--flat", type=int, default=0, help="単一flat笛（面内蛇行N本、例3）。--note併用")
    ap.add_argument("--flat-comb", action="store_true", help="flat測定コーム(C7/A6/F6/C6, 面内蛇行)")
    ap.add_argument("--fold-sweep", help="音固定・折り数スイープ。値=音名(例C6)。--Ns併用可")
    ap.add_argument("--Ns", default="1,2,3", help="fold-sweepの折り数リスト（既定 1,2,3）")
    ap.add_argument("--pan-flute", action="store_true", help="1オクターブのパンフルート型一体楽器")
    ap.add_argument("--pan-notes", help="パンフルートの音名リスト（既定 Cメジャー C6..C7）")
    ap.add_argument("--pan-N", type=int, default=2, help="パンフルート各管の折りパス数N（既定2=1折り）")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    if a.pan_flute:
        notes = a.pan_notes.replace(",", " ").split() if a.pan_notes else None
        mesh, infos = pan_flute(notes=notes, N=a.pan_N)
        name = a.out or os.path.join(OUT, "mini_panflute.stl")
        mesh.export(name)
        print("パンフルート（1オクターブ・一体・N=%d）:" % a.pan_N)
        for i in infos:
            print("  %-4s %s 予測%6.0fHz" % (i["label"], i["dims"], i["freq"]))
        print("外形", np.round(mesh.extents, 1), "watertight", mesh.is_watertight, "->", name)
    elif a.fold_sweep:
        Ns = tuple(int(x) for x in a.Ns.replace(",", " ").split())
        mesh, infos = fold_sweep_comb(note=a.fold_sweep, Ns=Ns)
        name = a.out or os.path.join(OUT, "mini_foldsweep_%s.stl" % a.fold_sweep)
        mesh.export(name)
        print("折り数スイープ（音固定=%s, 閉端）:" % a.fold_sweep)
        for i in infos:
            print("  %-10s %s 予測%6.0fHz" % (i["label"], i["dims"], i["freq"]))
        print("外形", np.round(mesh.extents, 1), "->", name)
    elif a.flat_comb:
        mesh, infos = flat_measure_comb()
        name = a.out or os.path.join(OUT, "mini_flat_comb.stl")
        mesh.export(name)
        print("flat測定コーム（面内蛇行・丸ボア, 既にflat向き）:")
        for i in infos:
            print("  %-8s %s 予測%6.0fHz" % (i["label"], i["dims"], i["freq"]))
        print("外形", np.round(mesh.extents, 1), "->", name)
    elif a.flat and (a.note or a.ztop):
        Lg = (a.ztop - Z_WINDOW) if a.ztop else None
        flute, info = flat_flute(note=a.note, Lg=Lg, N=a.flat)
        name = a.out or os.path.join(OUT, "mini_%s_flat%d.stl" % (a.note or "z", a.flat))
        flute.export(name)
        print("flat%d %s 外形%s 予測%.0fHz -> %s" % (a.flat, a.note or "", info["dims"], info["freq"], name))
    elif a.measure_comb:
        mesh, infos = measure_comb()
        name = a.out or os.path.join(OUT, "mini_measure_comb.stl")
        mesh.export(name)
        print("較正用スイープ（少数）:")
        for i in infos:
            print("  %-6s %-7s 全長%5.1f 幅%4.1f 予測%6.0fHz" % (i["label"], i["kind"], i["total_H"], i.get("W", FOOT), i["freq"]))
        print("外形", np.round(mesh.extents, 1), "->", name)
    elif a.fold and (a.note or a.ztop):
        note = a.note
        Lg = (a.ztop - Z_WINDOW) if a.ztop else None
        flute, info = folded_flute(note=note, Lg=Lg, N=a.fold)
        name = a.out or os.path.join(OUT, "mini_%s_fold%d.stl" % (a.note or "z", a.fold))
        flute.export(name)
        print("折り%d %s 全長%.1f 幅%.1f 予測%.0fHz -> %s" % (a.fold, a.note or "", info["total_H"], info["W"], info["freq"], name))
    elif a.sweep or a.notes:
        if a.notes:
            notes = a.notes.replace(",", " ").split()
            zts = [z_top_for_note(n) for n in notes]
            labels = notes
        else:
            zts = [float(x) for x in a.sweep.split(",")]
            labels = ["z%.0f" % z for z in zts]
        mesh, infos = straight_comb(zts)
        name = a.out or os.path.join(OUT, "mini_sweep.stl")
        mesh.export(name)
        print("極小笛スイープ（直管, 7×7角）:")
        for lab, i in zip(labels, infos):
            print("  %-6s z_top=%5.1f 全長%5.1fmm 予測%6.0fHz" % (lab, i["z_top"], i["total_H"], i["freq"]))
        print("外形", np.round(mesh.extents, 1), "->", name)
    else:
        if a.ztop:
            zt = a.ztop
        elif a.note:
            zt = z_top_for_note(a.note)
        else:
            zt = 39.5   # 原型相当
        flute, info = straight_flute(z_top=zt)
        name = a.out or os.path.join(OUT, "mini_%s.stl" % (a.note or ("z%.0f" % zt)))
        flute.export(name)
        print("z_top=%.1f 全長%.1fmm 予測%.0fHz -> %s" % (info["z_top"], info["total_H"], info["freq"], name))


if __name__ == "__main__":
    main()
