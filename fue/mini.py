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
import notes as notemod  # note_to_midi / midi_to_note（音名の移調用）

ROOT = os.path.join(os.path.dirname(__file__), os.pardir)
MINI_STL = os.path.join(ROOT, "mini", "recorder-mini-c-v3.stl")   # v3=v2+底に外7/内6mmの吸込口(z[-4,0])
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
C4 = 343000.0 / 4.0   # c/4 (mm/s /4)  ＝閉管 f=c/4L 用
C2 = 343000.0 / 2.0   # c/2 (mm/s /2)  ＝開管(トーンホール笛) f=c/2L 用
WH_ECO = 6.0          # 開管の実効端補正(mm)。第一近似。実測で更新


def predict_freq(z_top):
    """ボア上端z_topから発音周波数(Hz)を予測（閉管＋端補正）。"""
    return C4 / (z_top - Z_WINDOW + ENDCORR)


def z_top_for_freq(f):
    return Z_WINDOW - ENDCORR + C4 / f


def z_top_for_note(note):
    return z_top_for_freq(fold._note_freq(note))


def _mini_head():
    """実績ヘッド：mini-c-v3 を切り出す（発音部＋底の吸込口Ø6を保持）。
    v3=v2整列版で、窓/ウインドウェイ/ボアは v2 と同じ z、底 z[-4,0] に外7/内6mmの吸込口。
    切り出しは z=-6..CUT_Z+1（吸込口も残す）。音響は v2 と不変（吸込口を足しただけ）。"""
    m = trimesh.load(MINI_STL)
    big = trimesh.creation.box(extents=[FOOT + 4, FOOT + 4, CUT_Z + 7])
    big.apply_translation([CX, CY, (CUT_Z + 7) / 2.0 - 6.0])   # z -6..CUT_Z+1
    head = trimesh.boolean.intersection([m, big], engine="manifold")
    return head


def _bore_extension(z_top, round_bore=False):
    """ヘッド上に生やす閉じボア。外形7×7・内寸BORE、z=CUT_Z-1..z_top（上端閉）。
    round_bore=True で丸ボア（Ø=BORE）。横倒し(flat/spigot-up)印刷で天井が自己ブリッジし、
    ボア内部にサポートが入らない。"""
    z0 = CUT_Z - 1.0
    outer = trimesh.creation.box(extents=[FOOT, FOOT, (z_top + TOP_CAP) - z0])
    outer.apply_translation([CX, CY, (z0 + z_top + TOP_CAP) / 2.0])
    # ボア空洞: z=CUT_Z-2 .. z_top（上端で閉じ、下はヘッドのボアへ連結）
    vh = z_top - (CUT_Z - 2.0)
    if round_bore:
        void = trimesh.creation.cylinder(radius=BORE / 2.0, height=vh, sections=48)
    else:
        void = trimesh.creation.box(extents=[BORE, BORE, vh])
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


def flat_flute(note=None, Lg=None, N=3, z_low=4.0, r=3.0, end_wall=1.2, pitch=7.0, head=None, flatten=True, owall=0.0):
    """flat印刷用：実績ヘッド＋丸ボアの面内蛇行。出力STLは既にflat向き（窓横向き）。
    flatten=False で寝かせず立てたまま返す（オルガンの縦笛用）：ヘッドボア(CX,CY)を原点xyへ、
    ヘッド下端(吹込口)を z=0 へ置く。折れは +y 方向にN-1本ぶん深くなる（窓=-y面）。
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
    # owall: 胴を左右(x=管の並び方向)へ広げてボア側壁を厚くする。オルガンのように笛間に
    # 隙間があると 0.5mm 壁ではボア片面が密閉されず無発音になる(実機で確認)。owall>0 で
    # 側壁を owall 分厚くし、さらに並べたとき隣と重なって一体化(=実績パンフルート状態)させる。
    solid = trimesh.creation.box(extents=[FOOT + 2 * owall, y1 - y0, H])
    solid.apply_translation([CX, (y0 + y1) / 2.0, H / 2.0])
    slot = trimesh.creation.box(extents=[FOOT + 0.02, FOOT + 0.02, CUT_Z + 0.5])
    slot.apply_translation([CX, CY, (CUT_Z + 0.5) / 2.0 - 0.25])
    solid = trimesh.boolean.difference([solid, slot], engine="manifold")
    hollow = trimesh.boolean.difference([solid, void], engine="manifold")
    flute = trimesh.util.concatenate([hollow, h])
    if flatten:
        # flat向きにベイク（y軸まわり90°→管軸を水平・窓を横向き）、ベッドに落とし中心化
        flute.apply_transform(trimesh.transformations.rotation_matrix(np.radians(90), [0, 1, 0]))
        flute.apply_translation([0, 0, -flute.bounds[0][2]])
        bb = flute.bounds
        flute.apply_translation([-(bb[0][0] + bb[1][0]) / 2.0, -(bb[0][1] + bb[1][1]) / 2.0, 0])
    else:
        # 立てたまま：ボア(CX,CY)を原点xyへ、ヘッド下端(吹込口)を z=0 へ
        flute.apply_translation([-CX, -CY, -flute.bounds[0][2]])
    # 実際に鳴る音＝幾何路長から折り縮みを差し引いた実効長で予測（Lgは折り補正込みなので相殺）
    freq = C4 / (Lg + ENDCORR - FLAT_FOLD_CORR * (N - 1))
    info = dict(N=N, z_high=z_high, freq=freq, r=r, kind="flat%d" % N, flatten=flatten,
                dims=tuple(np.round(flute.extents, 1)))
    return flute, info


# --- 大ヘッド(mini を2倍にスケール)の flat 笛：低音1オクターブ(C5〜B5)用 ---
# mini ヘッド単体は約1オクターブ(C6〜C7)しか綺麗に鳴らない。低い1オクターブは
# ヘッドを2倍にした大ヘッドが安定して鳴る(2026/7/10 実機で確認。1.5/1.75倍は不安定で不採用)。
# 較正は 2倍笛の実測(C5=522/F5=686/A5=848, さらにE5/B5で検証, C5〜B5を±16c)から:
#   f = BIGHEAD_A / (2*Lg + BIGHEAD_B)   （Lg=スケール前のmini路長, 物理ボア=2*Lg）
BIGHEAD_SCALE = 2.0
BIGHEAD_A = 90165.0
BIGHEAD_B = 5.60


def bighead_flat_flute(note, N=2, head=None):
    """大ヘッド(2倍)の flat 笛。低音(C5〜B5)を較正どおりの音程で生成する。"""
    f = fold._note_freq(note)
    Lg = (BIGHEAD_A / f - BIGHEAD_B) / 2.0
    flute, info = flat_flute(Lg=Lg, N=N, head=head)
    flute.apply_scale(BIGHEAD_SCALE)
    info.update(note=note, bighead=True, scale=BIGHEAD_SCALE,
                freq=BIGHEAD_A / (2 * Lg + BIGHEAD_B),
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


def thin_comb(note="C6", N=1, thicks=(7.0, 5.0, 4.0, 3.0, 2.0), gap=4.0, axis="z"):
    """薄さ（厚み）を振った測定コーム。TPUスマホケース付随の極薄緊急ホイッスル向けに、
    音・路長を固定して「どの方向にどこまで薄くできるか」を測る。proven flat_flute を
    指定軸だけ非一様スケールして厚みTにする。
      axis="z"（既定）：高さ方向を圧縮。丸ボアØ6→横長楕円6×(6T/7)。窓(x-z)がz方向に潰れ、
                        寝かせ印刷ではボア天井が幅広で自己ブリッジしにくい。
      axis="y"：幅方向を圧縮。丸ボア→縦長楕円(6T/7)×6。窓は-y面にあるので窓の形(x-z)は不変で、
               寝かせ印刷ではボア天井が細くなり自己ブリッジしやすい（栗原さんの予想）。
    どちらも壁は同率で薄くなる（壁=T/14）ため印刷下限は同程度だが、窓形状と印刷性は異なる。"""
    ax = 2 if axis == "z" else 1
    head = _mini_head()
    base, binfo = flat_flute(note=note, N=N, head=head)
    t0 = float(base.extents[ax])                     # 元の厚み（z:7 / y:7〜）
    flutes, infos = [], []
    off = 0.0
    for T in thicks:
        f = base.copy()
        s = [1.0, 1.0, 1.0, 1.0]; s[ax] = T / t0
        f.apply_transform(np.diag(s))                # 指定軸→厚みT
        # y方向に並べる（コーム）。各笛を床(z=0)へ、y方向にoffで分離
        f.apply_translation([0.0, off - f.bounds[0][1], -f.bounds[0][2]])
        infos.append(dict(note=note, N=N, thick=round(T, 2), axis=axis, freq=binfo["freq"],
                          label="%s %s t%.1f" % (note, axis, T), off=off,
                          dims=tuple(np.round(f.extents, 1)), watertight=bool(f.is_watertight)))
        off += f.extents[1] + gap
        flutes.append(f)
    mesh = trimesh.util.concatenate(flutes)
    bb = mesh.bounds
    mesh.apply_translation([-(bb[0][0] + bb[1][0]) / 2, -(bb[0][1] + bb[1][1]) / 2, 0])
    return mesh, infos


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
def pan_flute(notes=None, N=2, gap=0.0, axis="z", mirror_y=None, bighead=False):
    if notes is None:
        notes = ["C6", "D6", "E6", "F6", "G6", "A6", "B6", "C7"]   # Cメジャー1オクターブ
    if mirror_y is None:
        mirror_y = [False] * len(notes)
    head = _mini_head()
    flutes, infos = [], []
    off = 0.0
    for i, note in enumerate(notes):
        if bighead:
            f, info = bighead_flat_flute(note, N=N, head=head)
        else:
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


# ---------------------------------------------------------------------------
# クロマチック2オクターブ（C5〜C7）一式とペンタトニック・ペンダント。
# 低音1オクターブ(C5〜B5)は大ヘッド(2倍)、高音(C6〜C7)は mini ヘッド。
# v3ヘッドなので各笛の吹込端に外Ø7/内Ø6(大ヘッドは14/12)の吸込口が4mm(大8mm)突き出す。
# ---------------------------------------------------------------------------
CHROM_LOW = ["C5", "C#5", "D5", "D#5", "E5", "F5", "F#5", "G5", "G#5", "A5", "A#5", "B5"]
CHROM_HIGH = ["C6", "C#6", "D6", "D#6", "E6", "F6", "F#6", "G6", "G#6", "A6", "A#6", "B6", "C7"]


def flat_row(row_notes, N=1, gap=3.0, bighead=False):
    """flat笛を独立のまま横一列（+y方向・gapで分離）。吹込端(-x)を x=0 に揃える。
    連結しない＝1本ずつ切り離して測定できる較正/検証プレート向き。"""
    head = _mini_head()
    flutes, infos = [], []
    yoff = 0.0
    for note in row_notes:
        if bighead:
            f, info = bighead_flat_flute(note, N=N, head=head)
        else:
            f, info = flat_flute(note=note, N=N, head=head)
        f.apply_translation([-f.bounds[0][0], yoff - f.bounds[0][1], -f.bounds[0][2]])
        info["label"] = note
        info["y"] = yoff
        yoff += f.extents[1] + gap
        flutes.append(f)
        infos.append(info)
    return trimesh.util.concatenate(flutes), infos


def penta_notes(root="C6"):
    """root から始まるメジャーペンタトニック5音（ドレミソラ＝+0,2,4,7,9半音）。"""
    m = notemod.note_to_midi(root)
    return [notemod.midi_to_note(m + s) for s in (0, 2, 4, 7, 9)]


def strap_lug(mesh, hole_d=5.0, wall=3.0, depth=FOOT / 3.0, cx=None):
    """タワー上面にストラップ用の耳（縦タブ＋横穴）を載せて返す。
    穴の軸は y（水平）＝寝かせ丸ボアと同じ自己ブリッジで印刷できる。
    タブ厚 depth はスラブ厚の1/3(約2.3mm)＝ストラップ紐には十分で嵩張らない。
    タブの足元が最上段スラブの実体に乗るよう、上面直下の断面から x 位置をクランプする。"""
    b = mesh.bounds
    T = b[1][2]
    R = hole_d / 2.0 + wall
    # 最上段スラブの x 範囲（上面の1mm下の断面）にタブを収める
    sec = mesh.section(plane_origin=[0, 0, T - 1.0], plane_normal=[0, 0, 1])
    xa, xb = sec.bounds[0][0], sec.bounds[1][0]
    if cx is None:
        cx = 0.0
    cx = min(max(cx, xa + R + 1.0), xb - R - 1.0)
    rot_y = trimesh.transformations.rotation_matrix(np.radians(90), [1, 0, 0])
    box = trimesh.creation.box(extents=[2 * R, depth, 6.0])
    box.apply_translation([cx, 0, T + 3.0])
    cap = trimesh.creation.cylinder(radius=R, height=depth, sections=64)
    cap.apply_transform(rot_y)
    cap.apply_translation([cx, 0, T + 6.0])
    hole = trimesh.creation.cylinder(radius=hole_d / 2.0, height=depth + 2.0, sections=48)
    hole.apply_transform(rot_y)
    hole.apply_translation([cx, 0, T + 6.0])
    lug = trimesh.boolean.union([box, cap], engine="manifold")
    lug = trimesh.boolean.difference([lug, hole], engine="manifold")
    return trimesh.util.concatenate([mesh, lug]), dict(cx=cx, hole_z=T + 6.0, top=T + 6.0 + R)


def pentatonic_pendant(root="C6", N=2, ring=True):
    """ペンタトニック5音（ドレミソラ）だけを z 積層でつないだ携帯用パンフルート。
    ring=True で最上段の上面にストラップ耳を付ける（穴Ø5・横穴＝自己ブリッジ）。"""
    nts = penta_notes(root)
    mesh, infos = pan_flute(notes=nts, N=N)
    lug_info = None
    if ring:
        mesh, lug_info = strap_lug(mesh)
    return mesh, infos, lug_info


# ---------------------------------------------------------------------------
# トーンホール笛（開管・直管）＝ミニ・ティンホイッスル。
# 実績ヘッド＋直管ボアを OPEN foot（上端開口）にし、側面にトーンホールを開ける。
# 指で穴を塞ぐと音程が変わる（リコーダー/ティンホイッスル式）。開管 f=c/2L。
# 穴位置は第一近似 z=Z_WINDOW + C2/f − WH_ECO。実測で WH_ECO と穴径を較正する。
# 印刷：寝かせ（rotate_y=90）で穴が上面に来る／ボア横向きでブリッジ、実質サポート小。
# ---------------------------------------------------------------------------
def _open_z_for_note(note):
    return Z_WINDOW + C2 / fold._note_freq(note) - WH_ECO


def whistle(base="C6", scale=None, bore_r=3.0, hole_r=1.5, foot_wall=1.0, head=None):
    """開管トーンホール笛。base=全閉(最低音)、scale=各穴を開けたときの音（低い順）。
    既定は7穴で基音C6〜C7の全音階1オクターブ（全閉=C6, 全開=C7）。過吹きで2オクターブ目。
    穴は窓と同じ面(−y)に開ける。片面のみ（貫通させない）ので指で塞げる。"""
    if scale is None:
        scale = ["D6", "E6", "F6", "G6", "A6", "B6", "C7"]   # C6基音の全音階7穴＝1オクターブ
    FW = 2 * bore_r + 2 * foot_wall                     # 外形角（壁 foot_wall）
    z_foot = _open_z_for_note(base)                     # 全閉=最低音の実効フット
    z0 = CUT_Z - 1.0
    H = z_foot                                          # 上端で開口（キャップ無し）
    # 外形角柱（ヘッド上に body）: z0..H
    outer = trimesh.creation.box(extents=[FW, FW, H - z0])
    outer.apply_translation([CX, CY, (z0 + H) / 2.0])
    # ボア（丸・上端まで貫通＝OPEN）: z=CUT_Z-2 .. H+1
    bore = trimesh.creation.cylinder(radius=bore_r, height=(H + 1) - (CUT_Z - 2), sections=48)
    bore.apply_translation([CX, CY, ((CUT_Z - 2) + (H + 1)) / 2.0])
    solid = trimesh.boolean.difference([outer, bore], engine="manifold")
    # トーンホール（窓と同じ面=-y から半径方向にボアへ）。片面のみ（貫通させない）。
    holes = []
    zpos = []
    Lh = FW / 2 + 1.0                                   # -y面外→ボア中心を少し越える
    for note in scale:
        z = _open_z_for_note(note)
        zpos.append((note, z))
        c = trimesh.creation.cylinder(radius=hole_r, height=Lh, sections=32)
        c.apply_transform(trimesh.transformations.rotation_matrix(np.radians(90), [1, 0, 0]))  # 軸→y
        c.apply_translation([CX, CY - FW / 2 - 0.5 + Lh / 2, z])   # -y面から内側へ、ボアで止める
        holes.append(c)
    void = trimesh.boolean.union(holes, engine="manifold")
    solid = trimesh.boolean.difference([solid, void], engine="manifold")
    # 吹込口クリアランス：ヘッド(-y面)のフリュー/窓/ウインドウェイ前を確実に開ける（トーンホールより低いz）
    mouth = trimesh.creation.box(extents=[FW + 4, 7.0, Z_WINDOW + 3.0])
    mouth.apply_translation([CX, CY - 6.5, (Z_WINDOW + 3.0) / 2.0 - 2.0])
    solid = trimesh.boolean.difference([solid, mouth], engine="manifold")
    h = head if head is not None else _mini_head()
    flute = trimesh.util.concatenate([solid, h])
    # flat向き：rotate_y 90 → 管軸を水平・穴を上面へ。ベッドに落とし中心化
    flute.apply_transform(trimesh.transformations.rotation_matrix(np.radians(90), [0, 1, 0]))
    flute.apply_translation([0, 0, -flute.bounds[0][2]])
    bb = flute.bounds
    flute.apply_translation([-(bb[0][0] + bb[1][0]) / 2.0, -(bb[0][1] + bb[1][1]) / 2.0, 0])
    info = dict(base=base, scale=scale, z_foot=z_foot, holes=zpos, bore_r=bore_r,
                hole_r=hole_r, FW=FW, dims=tuple(np.round(flute.extents, 1)))
    return flute, info


def whistle_fold(base="C6", scale=None, bore_r=3.0, hole_r=1.5, foot_wall=1.0, pitch=8.0, mouth_len=8.0, head=None):
    """開管トーンホール笛の1回折り版。ボアをU字に1回折り返して全長を約半分に。
    脚1(窓側)は穴なしの戻り管、脚2(フット側)に全トーンホール＋開口フット。穴は脚2の外面。
    音響路長=脚1+折返し+脚2 で開管 f=c/2L。第一近似、実測で WH_ECO/穴径/折り補正を較正。"""
    if scale is None:
        scale = ["D6", "E6", "F6", "G6", "A6", "B6", "C7"]
    FW = 2 * bore_r + 2 * foot_wall
    Ltot = C2 / fold._note_freq(base) - WH_ECO          # 窓→開口フットの実効路長
    Lfold = np.pi * (pitch / 2.0)                        # 折返し半周(近似)
    z0 = 16.0                                            # 脚1の下端(ヘッドボアへ連結)
    # 脚1(穴なし戻り管)は、最も窓寄りの穴(最高音)より手前で折り返す＝全穴を脚2に乗せる
    d_top = C2 / fold._note_freq(scale[-1]) - WH_ECO
    Lg1 = max(20.0, d_top - Lfold - 4.0)
    Lg2 = Ltot - Lfold - Lg1
    z_fold = z0 + Lg1                                    # 折返しの高さ
    y2 = CY + pitch                                      # 脚2のy
    z_foot = z_fold - Lg2                                # 脚2フット高さ(ここで開口)

    def path_point(d):                                   # 窓(=z0基準)から路長dの点
        if d <= Lg1:
            return np.array([CX, CY, z0 + d])
        d2 = d - Lg1
        if d2 <= Lfold:
            th = np.pi * (d2 / Lfold); cy = (CY + y2) / 2.0; r = pitch / 2.0
            return np.array([CX, cy - r * np.cos(th), z_fold + r * np.sin(th)])
        return np.array([CX, y2, z_fold - (d2 - Lfold)])

    # ボアU字の void（脚1→折返し→脚2、フットは少し延ばして開口）
    pts = [np.array([CX, CY, z0 - 2.0])]
    pts += [path_point(d) for d in np.linspace(0.5, Ltot, 40)]
    pts.append(np.array([CX, y2, z_foot - 2.0]))         # 開口フット(下へ突き出す)
    void = _round_serpentine_void(pts, bore_r)

    # 外形（両脚を囲む角柱）。フットは z_foot で開口させるため下端=z_foot。
    y_lo, y_hi = CY - FW / 2, y2 + FW / 2
    z_hi = z_fold + pitch / 2.0 + bore_r + foot_wall     # 折返し半径(pitch/2)ぶん延長し、折返しボア上端(apex+bore_r)を foot_wall で覆う
    solid = trimesh.creation.box(extents=[FW, y_hi - y_lo, z_hi - z_foot])
    solid.apply_translation([CX, (y_lo + y_hi) / 2.0, (z_foot + z_hi) / 2.0])
    # ヘッド差し込みスロット
    slot = trimesh.creation.box(extents=[FW + 0.02, FW + 0.02, CUT_Z + 0.5])
    slot.apply_translation([CX, CY, (CUT_Z + 0.5) / 2.0 - 0.25])
    solid = trimesh.boolean.difference([solid, slot], engine="manifold")
    solid = trimesh.boolean.difference([solid, void], engine="manifold")

    # トーンホール（脚2の外面=+y からボアへ、片面のみ）
    holes, zpos = [], []
    Lh = FW / 2 + 1.0
    for note in scale:
        d = C2 / fold._note_freq(note) - WH_ECO
        p = path_point(d)                                 # 脚2上の点(はず)
        c = trimesh.creation.cylinder(radius=hole_r, height=Lh, sections=32)
        c.apply_transform(trimesh.transformations.rotation_matrix(np.radians(90), [1, 0, 0]))  # 軸y
        c.apply_translation([CX, y2 + FW / 2 + 0.5 - Lh / 2, p[2]])   # +y面から内側へ
        holes.append(c); zpos.append((note, float(p[2])))
    solid = trimesh.boolean.difference([solid, trimesh.boolean.union(holes, engine="manifold")], engine="manifold")
    # 吹込口/窓クリアランス（リークを出さない2切り欠き）:
    #  ① 吹込口＝ヘッド下(z<Z_WINDOW-1 ＝ボア/空洞より下)を全周開放。
    #  ② 窓＝-y側だけ z=Z_WINDOW-1〜CUT_Z。leg1ボア(CY)や+yには触れない＝リーク無し。
    zc = Z_WINDOW - 1.0
    inlet_cut = trimesh.creation.box(extents=[FW + 6, 9.0, zc - (z_foot - 1.0)])
    inlet_cut.apply_translation([CX, CY - 0.5, ((z_foot - 1.0) + zc) / 2.0])
    win_cut = trimesh.creation.box(extents=[FW + 6, 5.0, CUT_Z - zc])
    win_cut.apply_translation([CX, CY - 5.5, (zc + CUT_Z) / 2.0])
    solid = trimesh.boolean.difference([solid, inlet_cut, win_cut], engine="manifold")

    # 吹込口マウスピース：この笛は下からでなく左(=最終-x)から吹く。左から筒を差して吹けるよう、
    # 開口端(leg2 foot)より mouth_len だけ左へ突出させ、右端はヘッド左端(=底 z=0)まで伸ばして接続する。
    # inlet_cut の後に union するので削られない。内孔はヘッド底ボア(z=0 で開口)へ貫通させ送気路をつなぐ。
    mp_ro, mp_ri = 3.75, 2.6                              # 外Ø7.5(筒を差す)/内Ø5.2(送気路)
    mp_zbot = z_foot - mouth_len                          # 突出先端(設計z＝最終-x側の最左点)
    mp_ztop = 1.0                                         # ヘッド底(z=0)へ1mm食い込ませて接続
    mp_out = trimesh.creation.cylinder(radius=mp_ro, height=mp_ztop - mp_zbot, sections=48)
    mp_out.apply_translation([CX, CY, (mp_zbot + mp_ztop) / 2.0])
    solid = trimesh.boolean.union([solid, mp_out], engine="manifold")
    mp_bore = trimesh.creation.cylinder(radius=mp_ri, height=2.0 - (mp_zbot - 1.0), sections=48)
    mp_bore.apply_translation([CX, CY, ((mp_zbot - 1.0) + 2.0) / 2.0])
    solid = trimesh.boolean.difference([solid, mp_bore], engine="manifold")

    h = head if head is not None else _mini_head()
    flute = trimesh.util.concatenate([solid, h])
    flute.apply_transform(trimesh.transformations.rotation_matrix(np.radians(90), [0, 1, 0]))
    flute.apply_translation([0, 0, -flute.bounds[0][2]])
    bb = flute.bounds
    flute.apply_translation([-(bb[0][0] + bb[1][0]) / 2.0, -(bb[0][1] + bb[1][1]) / 2.0, 0])
    info = dict(base=base, scale=scale, Ltot=Ltot, Lg1=Lg1, Lg2=Lg2, z_fold=z_fold,
                pitch=pitch, holes=zpos, bore_r=bore_r, hole_r=hole_r, FW=FW, mouth_len=mouth_len,
                dims=tuple(np.round(flute.extents, 1)))
    return flute, info


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
    ap.add_argument("--whistle", help="開管トーンホール笛(直管)。値=基音(全閉の最低音, 例C6)")
    ap.add_argument("--whistle-fold", help="開管トーンホール笛(1回折り・短い)。値=基音(例C6)")
    ap.add_argument("--pan-flute", action="store_true", help="1オクターブのパンフルート型一体楽器")
    ap.add_argument("--pan-notes", help="パンフルートの音名リスト（既定 Cメジャー C6..C7）")
    ap.add_argument("--pan-N", type=int, default=2, help="パンフルート各管の折りパス数N（既定2=1折り）")
    ap.add_argument("--chrom-low", action="store_true", help="低音クロマチックC5〜B5（大ヘッド12本）をZ積層タワーに")
    ap.add_argument("--chrom-high", action="store_true", help="高音クロマチックC6〜C7（mini13本・N=1直管）を独立横並びプレートに")
    ap.add_argument("--chrom-groups", action="store_true", help="低音を4本ずつA/B/Cの独立横並びプレート3枚に（大ヘッド・N=2）")
    ap.add_argument("--pentatonic", help="ペンタトニック・ペンダント。値=ルート音（例 C6）。ドレミソラ5音＋ストラップ耳")
    ap.add_argument("--no-ring", action="store_true", help="--pentatonic のストラップ耳を省く")
    ap.add_argument("--thin-comb", help="薄さ(厚み)スイープの測定コーム。値=音名(例C6)。極薄ホイッスル探索用")
    ap.add_argument("--thicks", default="7,5,4,3,2", help="thin-combの厚みリスト(mm, 既定 7,5,4,3,2)")
    ap.add_argument("--thin-N", type=int, default=1, help="thin-combの折りパス数N（既定1=直管）")
    ap.add_argument("--thin-axis", default="z", choices=["z", "y"], help="thin-combの圧縮軸（z=高さ/y=幅, 既定z）")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    if a.thin_comb:
        thicks = tuple(float(x) for x in a.thicks.replace(",", " ").split())
        mesh, infos = thin_comb(note=a.thin_comb, N=a.thin_N, thicks=thicks, axis=a.thin_axis)
        name = a.out or os.path.join(OUT, "mini_thin_comb_%s_%s.stl" % (a.thin_comb, a.thin_axis))
        mesh.export(name)
        print("薄さ(厚み)スイープ・コーム（音・路長固定, 厚みだけ変化, N=%d）:" % a.thin_N)
        for i in infos:
            print("  %-7s 厚み%.1fmm 外形%s wt=%s 予測%6.0fHz" %
                  (i["label"], i["thick"], i["dims"], i["watertight"], i["freq"]))
        print("外形", np.round(mesh.extents, 1), "->", name)
        return

    if a.chrom_low:
        mesh, infos = pan_flute(notes=CHROM_LOW, N=2, bighead=True)
        mesh.apply_translation([-mesh.bounds[0][0], 0, 0])   # 吹込端を x=0 へ（旧版と同じ框）
        name = a.out or os.path.join(OUT, "chrom_low_zstack.stl")
        mesh.export(name)
        print("低音クロマチックタワー（大ヘッド・v3吸込口付き・N=2・Z積層12段）:")
        for i in infos:
            print("  %-4s %s 予測%6.0fHz" % (i["label"], i["dims"], i["freq"]))
        print("外形", np.round(mesh.extents, 1), "->", name)
    elif a.chrom_high:
        mesh, infos = flat_row(CHROM_HIGH, N=1, gap=3.0, bighead=False)
        name = a.out or os.path.join(OUT, "chrom2oct_D_C6-C7_mini.stl")
        mesh.export(name)
        print("高音クロマチックプレート（mini・v3吸込口付き・N=1直管・独立13本）:")
        for i in infos:
            print("  %-4s %s 予測%6.0fHz" % (i["label"], i["dims"], i["freq"]))
        print("外形", np.round(mesh.extents, 1), "->", name)
    elif a.chrom_groups:
        groups = [("A", CHROM_LOW[0:4]), ("B", CHROM_LOW[4:8]), ("C", CHROM_LOW[8:12])]
        for tag, nts in groups:
            mesh, infos = flat_row(nts, N=2, gap=5.0, bighead=True)
            label = "%s_%s-%s" % (tag, nts[0].replace("#", "s"), nts[-1].replace("#", "s"))
            name = os.path.join(OUT, "chrom2oct_%s.stl" % label)
            mesh.export(name)
            print("低音グループ%s（大ヘッド・v3吸込口付き・N=2・独立%d本）: 外形%s -> %s"
                  % (tag, len(nts), np.round(mesh.extents, 1), name))
            for i in infos:
                print("  %-4s %s 予測%6.0fHz" % (i["label"], i["dims"], i["freq"]))
    elif a.pentatonic:
        mesh, infos, lug = pentatonic_pendant(root=a.pentatonic, N=a.pan_N, ring=not a.no_ring)
        name = a.out or os.path.join(OUT, "penta_pendant_%s.stl" % a.pentatonic)
        mesh.export(name)
        print("ペンタトニック・ペンダント（ドレミソラ5音・Z積層・N=%d）:" % a.pan_N)
        for i in infos:
            print("  %-4s %s 予測%6.0fHz" % (i["label"], i["dims"], i["freq"]))
        if lug:
            print("  ストラップ耳: 穴Ø5 中心 x=%.1f z=%.1f 頂部z=%.1f" % (lug["cx"], lug["hole_z"], lug["top"]))
        print("外形", np.round(mesh.extents, 1), "->", name)
    elif a.whistle_fold:
        flute, info = whistle_fold(base=a.whistle_fold)
        name = a.out or os.path.join(OUT, "mini_whistlefold_%s.stl" % a.whistle_fold)
        flute.export(name)
        print("開管トーンホール笛(1回折り) base=%s: 外形%s watertight=%s 路長%.0f(脚%.0f+折+脚%.0f)"
              % (a.whistle_fold, info["dims"], flute.is_watertight, info["Ltot"], info["Lg1"], info["Lg2"]))
        for note, z in info["holes"]:
            print("    穴 %-3s z=%.1f" % (note, z))
        print("  -> %s" % name)
    elif a.whistle:
        flute, info = whistle(base=a.whistle)
        name = a.out or os.path.join(OUT, "mini_whistle_%s.stl" % a.whistle)
        flute.export(name)
        print("開管トーンホール笛 base=%s（全閉=%s、穴を低い順に開けて音階、C↑は過吹き）:" % (a.whistle, a.whistle))
        print("  外形%s watertight=%s ボアØ%.0f 穴Ø%.0f 外形角%.0f" %
              (info["dims"], flute.is_watertight, 2 * info["bore_r"], 2 * info["hole_r"], info["FW"]))
        print("  トーンホール位置(窓からの実効長方向 z, mm):")
        prev = None
        for note, z in info["holes"]:
            gap = "" if prev is None else " (間隔%.1f)" % (z - prev)
            print("    %-3s z=%5.1f%s" % (note, z, gap)); prev = z
        print("  -> %s" % name)
    elif a.pan_flute:
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
