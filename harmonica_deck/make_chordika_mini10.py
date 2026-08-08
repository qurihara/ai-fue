"""mini10（半割・厚壁1mm・深い窓）パイプで作る新Chordikaカードの生成器。

背景・経緯は cosense「AI笛作り」2026/7/23 08:35 の引き継ぎ参照。
- 旧Chordika（薄壁・旧ジオメトリ）は harmonica_deck/deck.py + fue/namecard.py。本ファイルは
  「厚壁mini10パイプ＋名刺プレート」への置換版で、まず C/Am の確認カードを作った時のコードを保存したもの。
- パイプ = mini10（基STL mini10/recorder-mini-c-v3-half-2-v2.stl、フット可変 THR=17, base=60）。
  安定帯 F#6(1480Hz)〜G#7(3320Hz)=14半音。窓は上面(+z)。管長→周波数の再較正 f=A/(L+e), A=86338, e=-13.06。
  逆算は L = A/f - e（e=-13.06 なので +13.06）。符号ミス注意（一度 L=A/f+e で全部短くなった）。
- 窓の選定: C/Am は低音版 G6〜F#7（low_midi=91）を採用。高音版は A6〜G#7（low_midi=93）。
  C/Am はこの2窓で G音1本だけ違う（G6=68.1mm / G7=40.6mm）。

カードの作り（build_card）:
- 8本のmini10パイプを 0.3mm 重ねて融合（窓は上向き・吸込口x=0そろえ）。
- 名刺プレート(クレカ大 85.6×53.98)を厚み CZ=0.5mm で融合。
  ★重要: mini10のボア床は z≈0.5mm。プレートは CZ=0.5（笛の床厚に一致）にすること。
   これで総厚4mm・ボア無傷（断面のボア穴 9.808 が素の笛と一致）を確認済み。
   CZ=1.0 にすると z=1.0 がボア床に達してボアを侵食する（body断面 7.326 に痩せる）ので不可。
- 角丸R2・主音＊(トニックのパイプの足先)・調性名ステンシル(足側余白帯)・ストラップ穴・触覚の切り欠き(調の半音番号)。
- namecard.py の _corner_prism / _text_line と stencil を流用。

出力(確認済み): out/nc2_CAm_G6Fs7_plate.stl（4mm・切り欠き・ボア無傷）、スライス out/nc2_CAm_G6Fs7_plate_h2d.gcode.3mf（未印刷）。

実行環境: /Users/kurihara/Desktop/claude_work/mesh_venv/bin/python（trimesh/manifold3d/numpy-stl/lxml/matplotlib 導入済）。
"""
import os
import sys
import numpy as np
import trimesh
from shapely.geometry import MultiPolygon, Point, Polygon

HERE = os.path.dirname(__file__)
ROOT = os.path.join(HERE, os.pardir)
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(ROOT, "fue"))
import namecard as NC   # _corner_prism / _text_line を流用
import stencil          # text_holes / asterisk

BASE = os.path.join(ROOT, "mini10/recorder-mini-c-v3-half-2-v2.stl")
THR = 17.0
BASE_LEN = 60.0
A, E = 86338.0, -13.06                 # 再較正 f=A/(L+e)。実測が入ったら calib_from_file() で上書きする

CX, CY, CZ = 85.6, 53.98, 0.5          # 名刺プレート（CZ=0.5＝笛の床厚。総厚4mm・ボア無傷）
OVER = 0.3                             # パイプ融合の重なり

MAJOR = [0, 2, 4, 5, 7, 9, 11]         # 長音階の音程
DEGREES = [2, 4, 6, 1, 3, 5, 7, 2]     # Chordikaの度数連鎖（隣接3本= ii IV vi I iii V）
NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

# 基準窓＝G#6〜G7 に全調統一。窓下端 G#6 の MIDI=92（2026/7/23 実機検証で+1半音へ変更）。
# 旧・低音版 G6〜F#7(low_midi=91)は最長G6=67mmで、実機で最長管が鳴らない個体差が出た。窓を1半音上げると
# 最長管が約64mmに縮み低音側のマージンが増える。全12ピッチクラスの管長は約38〜64mmで、較正範囲(40〜72mm)の
# 上半分＝短めに寄る（高音側の最短G7=38mmは帯の上端に近い）。位置→和音機能は全カード不変・移調運指共通。
LOW_MIDI = 92

# 12調（クロマチックの各キー）。(主音の半音番号 root_pc, 表示ラベル=メジャー/平行短調)。
# 表記は実機ハーモニカ慣用に合わせ Db/Eb/Ab/Bb はフラット、F# はシャープ。切り欠き位置=root_pc。
KEYS = [
    (0,  "C / Am"),
    (7,  "G / Em"),
    (2,  "D / Bm"),
    (9,  "A / F#m"),
    (4,  "E / C#m"),
    (11, "B / G#m"),
    (6,  "F# / D#m"),
    (1,  "Db / Bbm"),
    (8,  "Ab / Fm"),
    (3,  "Eb / Cm"),
    (10, "Bb / Gm"),
    (5,  "F / Dm"),
]


def _hz(m):
    return 440.0 * 2 ** ((m - 69) / 12.0)


def _len_of(m):
    return A / _hz(m) - E               # ★ L = A/f - e（e=-13.06 → +13.06）。符号注意


def _flute(L):
    m = trimesh.load(BASE).copy()
    v = m.vertices.copy()
    v[v[:, 0] >= THR, 0] += (L - BASE_LEN)
    m.vertices = v
    m.merge_vertices()
    b = m.bounds
    m.apply_translation([-b[0][0], -b[0][1], -b[0][2]])
    return m


def _cut_plate(mesh, poly):
    """2Dポリゴンをプレート(z=0..CZ)だけ貫通で差し引く（上のパイプは触らない）。"""
    geoms = list(poly.geoms) if isinstance(poly, MultiPolygon) else [poly]
    for g in geoms:
        pr = trimesh.creation.extrude_polygon(g, height=CZ + 0.4)
        pr.apply_translation([0, 0, -0.2])
        mesh = trimesh.boolean.difference([mesh, pr], engine="manifold")
    return mesh


def chain_pitchclasses(root_pc):
    """度数連鎖のピッチクラス列（8本、末尾は先頭と同じ）。"""
    return [(root_pc + MAJOR[d - 1]) % 12 for d in DEGREES]


def _triad_quality(pcs):
    """3ピッチクラス集合の三和音の種類（root基準の音程で major/minor/dim/?）。"""
    for r in pcs:
        ivs = sorted((p - r) % 12 for p in pcs)
        if ivs == [0, 4, 7]:
            return "%s major" % NAMES[r]
        if ivs == [0, 3, 7]:
            return "%s minor" % NAMES[r]
        if ivs == [0, 3, 6]:
            return "%s dim" % NAMES[r]
    return "%s ?" % NAMES[pcs[0]]


def triads_of(chain):
    """カードの隣接3本（ステップ1）が作る三和音の一覧 [(3本のpc, 'C major'等) ...]。"""
    return [(chain[i:i + 3], _triad_quality(chain[i:i + 3])) for i in range(len(chain) - 2)]


def calib_from_file(path=None):
    """実測の再フィット結果を A,E に反映する。mini10/refit_calib.py が書き出す
    out/mini10_calib_v11.txt（1行目 'A=..' 2行目 'e=..'）があれば読む。無ければ現行値のまま。"""
    global A, E
    p = path or os.path.join(OUT, "mini10_calib_v11.txt")
    if not os.path.exists(p):
        return A, E, False
    d = {}
    for line in open(p):
        line = line.strip()
        if line.startswith("A="):
            d["A"] = float(line[2:])
        elif line.lower().startswith("e="):
            d["E"] = float(line[2:])
    if "A" in d and "E" in d:
        A, E = d["A"], d["E"]
        return A, E, True
    return A, E, False


def build_card(root_pc, low_midi, label, notch_index, invert=False):
    """1調ぶんの8本カード（名刺プレート付き）。
    root_pc: 主音の半音番号(C=0)。low_midi: 窓の下端音のMIDI(G6=91, A6=93)。
    label: 刻印文字（例 'C / Am'）。notch_index: 切り欠き位置(調の半音番号 C=0)。
    invert: 笛の並びだけを逆順にした「逆並び版」を作る。刻印・ストラップ穴・切り欠きは
    通常版と同じ位置のままなので、外形と手触りは変わらず、鳴る和音の左右だけが入れ替わる。"""
    W = trimesh.load(BASE).extents[1]              # パイプ幅 ≈7
    step = W - OVER
    chain = chain_pitchclasses(root_pc)
    tonic_idx = DEGREES.index(1)                    # 主音(度数1)の連鎖内位置＝3（＊を置く笛）
    if invert:
        chain = chain[::-1]
        tonic_idx = len(chain) - 1 - tonic_idx

    ms, y, feet = [], 0.0, []
    for pc in chain:
        midi = low_midi + ((pc - low_midi) % 12)   # 窓[low..low+11]内へ折り込む
        L = _len_of(midi)
        f = _flute(L)
        f.apply_translation([0, y, 0])
        ms.append(f)
        feet.append((y, L, midi))
        y += step
    comb = trimesh.boolean.union(ms, engine="manifold")
    comb.merge_vertices()
    cw = comb.extents[1]
    yshift = (CY - cw) / 2.0
    comb.apply_translation([0, yshift, 0])          # ★積まない(z=0..4)＝プレート融合で総厚4mm

    plate = trimesh.creation.box(extents=[CX, CY, CZ])
    plate.apply_translation([CX / 2, CY / 2, CZ / 2])
    card = trimesh.boolean.union([plate, comb], engine="manifold")
    keep = NC._corner_prism(CX, CY, 2.0, "round", -1.0, comb.bounds[1][2] + 1.0)
    card = trimesh.boolean.intersection([card, keep], engine="manifold")

    # 主音＊（トニックのパイプの足先）
    yr, Lc, _mc = feet[tonic_idx]
    scx = Lc + 2.0 + 1.6
    scy = yr + yshift + W / 2.0
    card = _cut_plate(card, stencil.asterisk(scx, scy, 1.6))

    # 調性名ステンシル（足側の余白帯にy方向読み）
    fx = max(f[1] for f in feet)
    bx0 = fx + 2.0
    bx1 = CX - 3.0
    h = min(5.0, bx1 - bx0 - 1.0)
    xc = (bx0 + bx1) / 2
    pl, _ = NC._text_line(label, xc, h, CY)
    if pl is not None and not pl.is_empty:
        card = _cut_plate(card, pl)

    # ストラップ穴（貫通）
    sr = 3.0
    circ = Point(CX - (sr + 3.0), CY - (sr + 3.0)).buffer(sr, resolution=48)
    pr = trimesh.creation.extrude_polygon(circ, height=comb.bounds[1][2] + 2.0)
    pr.apply_translation([0, 0, -1.0])
    card = trimesh.boolean.difference([card, pr], engine="manifold")

    # 触覚の切り欠き（調の半音番号でy位置。足側の辺x=CXに半円凹み。y_lo3..y_hi43で12分割）
    y_lo, y_hi, n, nr = 3.0, 43.0, 12, 1.6
    ny = y_lo + (y_hi - y_lo) * (notch_index / (n - 1))
    cutter = trimesh.creation.cylinder(radius=nr, height=comb.bounds[1][2] + 6.0, sections=48)
    cutter.apply_translation([CX, ny, (comb.bounds[1][2] + 6.0) / 2.0 - 1.0])
    card = trimesh.boolean.difference([card, cutter], engine="manifold")

    card.apply_translation([0, 0, -card.bounds[0][2]])
    # ボア無傷チェック（x=30断面のボア穴面積が素の笛=9.808と一致するか）
    s = card.section(plane_origin=[30, 0, 0], plane_normal=[1, 0, 0])
    pl2, _ = s.to_planar()
    areas = set(round(abs(Polygon(r).area), 3) for p in pl2.polygons_full for r in p.interiors)
    print("[%s low=%d] ext=%s wt=%s ボア穴=%s(素9.808)" % (
        label, low_midi, np.round(card.extents, 1).tolist(), card.is_watertight, areas))
    return card


def _safe(label):
    return label.replace(" ", "").replace("/", "_").replace("#", "s")


def build_deck(outdir=OUT, prefix="chordika_v11", analyze=False, invert=False):
    """全12調のカードを基準窓 G6〜F#7 で生成。analyze=True なら和音・管長の解析のみ（STL出力なし）。"""
    A4used, Eused, loaded = calib_from_file()
    win = "%s%d〜%s%d" % (NAMES[LOW_MIDI % 12], LOW_MIDI // 12 - 1,
                          NAMES[(LOW_MIDI + 11) % 12], (LOW_MIDI + 11) // 12 - 1)
    allmid = [LOW_MIDI + ((pc - LOW_MIDI) % 12) for r, _ in KEYS for pc in chain_pitchclasses(r)]
    lo_mm, hi_mm = _len_of(max(allmid)), _len_of(min(allmid))
    print("=== Chordika v1.1（mini10 厚壁・深窓 / 窓 %s / 全12調）===" % win)
    print("較正 f=A/(L+e): A=%.1f e=%.3f %s" % (A, E, "（実測再フィット反映）" if loaded else "（現行値＝実測待ち）"))
    print("各カード8本・度数連鎖 2·4·6·1·3·5·7·2・隣接3本= ii IV vi I iii V の6三和音")
    print("管長域 約%.0f〜%.0fmm\n" % (lo_mm, hi_mm))
    for root_pc, label in KEYS:
        chain = chain_pitchclasses(root_pc)
        midis = [LOW_MIDI + ((pc - LOW_MIDI) % 12) for pc in chain]
        lens = [round(_len_of(m), 1) for m in midis]
        notes = ["%s%d" % (NAMES[m % 12], m // 12 - 1) for m in midis]
        tris = triads_of(chain)
        print("[%s]  並び(%s): %s" % (label, win, " ".join(notes)))
        print("     管長mm: %s" % " ".join("%.1f" % L for L in lens))
        print("     隣接3本の和音: %s" % "  ".join("%s%s%s=%s" % (
            NAMES[w[0]], NAMES[w[1]], NAMES[w[2]], q) for w, q in tris))
        if not analyze:
            card = build_card(root_pc=root_pc, low_midi=LOW_MIDI, label=label,
                              notch_index=root_pc, invert=invert)
            fn = os.path.join(outdir, "%s_%s.stl" % (prefix, _safe(label)))
            card.export(fn)
            print("     -> %s" % os.path.relpath(fn, ROOT))
        print()


if __name__ == "__main__":
    if "--one" in sys.argv:
        # C/Am 低音版（G6〜F#7, low_midi=91, 主音C=root_pc0, 切り欠きC=0）の確認カードだけ
        card = build_card(root_pc=0, low_midi=91, label="C / Am", notch_index=0)
        out = os.path.join(OUT, "nc2_CAm_G6Fs7_plate.stl")
        card.export(out)
        print("wrote", out)
    elif "--inverted" in sys.argv:
        # 逆並び版。図に合わせて左から位置1になる並び。おまけ扱いで、専用の図は作らない。
        build_deck(outdir=os.path.join(OUT, "inverted"), prefix="chordika_inv", invert=True)
    else:
        build_deck(analyze=("--analyze" in sys.argv or "--dry" in sys.argv))
