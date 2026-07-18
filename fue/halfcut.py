"""半割り極薄笛（v2円筒を管軸方向に半割りしたD字断面）の較正コーム。

実績: mini/recorder-mini-c-v3-half-v2-40.stl (管長40mm)=約3.5kHz(≈A7)、-60.stl(60mm)=約1.83kHz(≈A6)。
＝長さ40→60mm でほぼ1オクターブ。長さは「頭部・窓(x<=14 固定)＋フット(x>=20)を平行移動」で
完全にパラメトリック化できる（-60 は -40 のフットを +20mm した実体と体積差1.1%で一致を確認）。

この較正コームで「管長→音程」を実測し、ダイアトニック(オクターブ)の各長さを確定する。
角柱では作らず、必ず元と同じ半割り(D字/半円状ボア)のまま長さだけ変える。
"""
import os
import sys
import numpy as np
import trimesh

sys.path.insert(0, os.path.dirname(__file__))

OUT = os.path.join(os.path.dirname(__file__), os.pardir, "out")
BASE_STL = os.path.join(os.path.dirname(__file__), os.pardir, "mini", "recorder-mini-c-v3-half-v2-40.stl")

# 半割り笛の x 構造（-40 実測）: 吸込口 x=-4 / 窓・ラビウム x=8〜14 / 直管フット x=14〜35 / 端面 x=36。
# 窓より先(x>=FOOT_THR)だけを平行移動すればフット長=総管長が変わる（頭部・窓は不変）。
FOOT_THR = 20.0
BASE_LEN = 40.0

# 実測較正（2026/7/17, 較正コーム8本の clean run＝高→低で単音抽出）: 管長L[mm]→基本周波数f[Hz]。
# 音域は G#6(64mm,1682Hz)〜A7(36mm,3615Hz) の約1.1オクターブ。全長よく鳴った。
CALIB = [(36, 3615), (40, 3041), (44, 2689), (48, 2361), (52, 2168), (56, 1980), (60, 1816), (64, 1682)]
# 物理閉管モデル f = A/(L+e) が最良（RMS≈16cent・最大33cent。log線形はRMS57centで不可）。
# 1/f = (1/A)L + e/A の線形回帰で係数を得る。
_CL = np.array([p[0] for p in CALIB], float)
_CF = np.array([p[1] for p in CALIB], float)
_invA, _eoverA = np.polyfit(_CL, 1.0 / _CF, 1)
_A = 1.0 / _invA
_E = _eoverA * _A                                  # ≈ A=89086, e=-10.9


def est_freq(L):
    """実測較正 f=A/(L+e) による周波数[Hz]。"""
    return _A / (L + _E)


def length_for_freq(f):
    """目標周波数 f[Hz] を出す管長[mm]（est_freq の逆）。"""
    return _A / f - _E


def note_freq(note):
    """音名(例 'A6','C#7')→周波数[Hz]（A4=440・平均律）。"""
    idx = {'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5,
           'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11}
    name, octv = note[:-1], int(note[-1])
    midi = 12 * (octv + 1) + idx[name]
    return 440.0 * 2 ** ((midi - 69) / 12.0)


def length_for_note(note):
    """音名→その音を出す管長[mm]（較正範囲 36〜64mm 内が実用。範囲外は外挿=要確認）。"""
    return length_for_freq(note_freq(note))


def half_flute(L, base=None):
    """管長 L[mm] の半割り笛メッシュ（元STL native向き: x=管軸, y=厚み4, z=幅7, 窓=y最小面）。
    頭部・窓は不変のまま、フット(x>=FOOT_THR)を平行移動して総管長を L にする。"""
    m = (base if base is not None else trimesh.load(BASE_STL)).copy()
    v = m.vertices.copy()
    v[v[:, 0] >= FOOT_THR, 0] += (L - BASE_LEN)
    m.vertices = v
    return m


def _printpose(m):
    """印刷姿勢: 平坦面(窓, y最小)を下・丸い背(y最大)を上にした平置き＝サポートフリー。
    実績単体印刷と同じく厚み4mmを垂直(z)にする。x軸まわり+90°で y→z。"""
    m = m.copy()
    m.apply_transform(trimesh.transformations.rotation_matrix(np.radians(90), [1, 0, 0]))
    m.apply_translation([0, 0, -m.bounds[0][2]])          # ベッド(z=0)へ落とす
    return m


def half_calib_comb(lengths=None, gap=0.0, merge=True, overlap=0.3):
    """長さ違いの半割り笛を一列に並べた較正コーム。全笛の吸込口(x=0)を揃え、フットが長いほど
    +x へ伸びる。幅方向(y)に gap を空けて並べる（gap=0 で隙間なく密着）。
    merge=True: 密着した笛を boolean union で一体のwatertight連結コームにする（各ボアは独立のまま
    残る＝実績パンフルートと同じ密閉。union を確実にするため密着時は overlap だけ食い込ませる）。"""
    if lengths is None:
        lengths = [36, 40, 44, 48, 52, 56, 60, 64]        # 4mm刻み・アンカー40/60含む・約1.3oct
    base = trimesh.load(BASE_STL)
    flutes, infos = [], []
    y = 0.0
    for L in lengths:
        f = _printpose(half_flute(L, base=base))
        b = f.bounds
        f.apply_translation([-b[0][0], -b[0][1] + y, 0])  # 吸込口を x=0、幅方向に y だけずらす
        fb = f.bounds
        w = fb[1][1] - fb[0][1]
        infos.append(dict(L=L, y=round(y, 1), freq=est_freq(L), x_foot=round(fb[1][0], 1)))
        step = w + gap
        if merge and gap == 0.0:
            step -= overlap                               # 密着時は微小に重ねて union を確実化
        y += step
        flutes.append(f)
    if merge:
        comb = trimesh.boolean.union(flutes, engine="manifold")
    else:
        comb = trimesh.util.concatenate(flutes)
    return comb, infos


# --- 実測較正から作るダイアトニック音階コーム＆限界探索コーム ---
A_MAJOR = ["A6", "B6", "C#7", "D7", "E7", "F#7", "G#7", "A7"]   # 較正範囲(G#6〜A7)に収まる1オクターブ
# E major(E6→E7): クリーン域(F6〜E7)の上端E7にぴったり収まるフルオクターブ。7音は実測クリーン確定、
# 最低音E6(78.5mm)だけが F6(76mm,明瞭)と D6(84mm,辛うじて)の間＝やや弱い見込み。幅53.9mmが名刺の短辺55mmと一致。
E_MAJOR = ["E6", "F#6", "G#6", "A6", "B6", "C#7", "D#7", "E7"]
# Eb major(D#6→D#7): クリーン域に最も収まるフルオクターブ。8音中7音が明瞭、最低音D#6(82.5mm)だけ弱い。
# 上端D#7(46.7mm)はオーバーブロー域から離れて安全＝E6-E7より良い置き所（実測音域 F6〜E7 より, 2026/7/17）。
EB_MAJOR = ["D#6", "F6", "G6", "G#6", "A#6", "C7", "D7", "D#7"]
# F major 7音(F6→E7): octaveの高いドを捨てた7音。クリーン域 F6〜E7 に丸ごと収まり全音鳴る
# （幅=長7度=窓とほぼ同じなので両端F6/E7はクリーン域の縁。中5音は余裕。G majorに上げると最高音F#7が✗）。
F_MAJOR7 = ["F6", "G6", "A6", "A#6", "C7", "D7", "E7"]
# クロマチック(半音12音): オクターブに拘らず、クリーンに鳴る下限F6〜上限E7の半音を全部集めた全パレット。
# 任意の調・半音進行の旋律がこの音域で吹ける。管長は74.7→44.7mmの滑らかな階段。
CHROMATIC = ["F6", "F#6", "G6", "G#6", "A6", "A#6", "B6", "C7", "C#7", "D7", "D#7", "E7"]
# 全域探索(F6→A7 半音17): クリーン下限F6から、上端の不安定ゾーン(F#7〜A7=較正では鳴った/音階では
# オーバーブロー)まで欲張って全部並べる。実機で吹けば本当のクリーン上限が一発で確定する。
FULLRANGE = ["F6", "F#6", "G6", "G#6", "A6", "A#6", "B6", "C7", "C#7", "D7", "D#7", "E7",
             "F7", "F#7", "G7", "G#7", "A7"]
# 低音シフト版(2026/7/18): 実機で FULLRANGE は下端F6余裕あり・鳴るのは〜D7(11本目以降=D#7↑は無音)と判明。
# 全体を3半音下げ、下端をD6まで伸ばして低音側の限界を探る＋鳴る本数を増やす。17本 D6→F#7。
LOWSHIFT3 = ["D6", "D#6", "E6", "F6", "F#6", "G6", "G#6", "A6", "A#6", "B6", "C7", "C#7", "D7",
             "D#7", "E7", "F7", "F#7"]
# 既知の良音域 A6〜A7(≈36〜62mm)は鳴ると確定済みなので省き、両端に集中して限界を探る。
# 高音側(短): 22〜34mm=A7より上(B7〜C8域, オーバーブロー限界)。低音側(長): 68〜100mm=G#6より下(E6域へ, 駆動限界)。
LIMIT_LENGTHS = [22, 26, 30, 34, 68, 76, 84, 92, 100]


def scale_comb(notes=None, gap=0.0, merge=True):
    """実測較正 length_for_note で各音の管長を求めたダイアトニック音階コーム。既定=A majorオクターブ。"""
    if notes is None:
        notes = A_MAJOR
    lengths = [round(length_for_note(n), 1) for n in notes]
    comb, infos = half_calib_comb(lengths=lengths, gap=gap, merge=merge)
    for info, n, L in zip(infos, notes, lengths):
        info["note"] = n
    return comb, infos, notes, lengths


def limit_comb(lengths=None, gap=0.0, merge=True):
    """音域の限界探索コーム：既知の良音域(36〜64mm)を超えて短側(高音・オーバーブロー限界)と
    長側(低音・駆動限界)へ延ばす。どこまで綺麗に鳴るかを実測して可能音域の上限下限を確定する。"""
    if lengths is None:
        lengths = LIMIT_LENGTHS
    comb, infos = half_calib_comb(lengths=lengths, gap=gap, merge=merge)
    return comb, infos, lengths


def _render(comb, infos, path):
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    b = comb.bounds
    fig = plt.figure(figsize=(14, 6))
    for i, (t, (el, az)) in enumerate([("iso", (28, -60)), ("top (windows down)", (88, -90))]):
        ax = fig.add_subplot(1, 2, i + 1, projection="3d")
        ax.add_collection3d(Poly3DCollection(comb.triangles, alpha=0.55, facecolor="#8fb0e0", edgecolor="#456"))
        ax.set_xlim(b[0][0], b[1][0]); ax.set_ylim(b[0][1], b[1][1]); ax.set_zlim(b[0][2] - 1, b[0][2] + (b[1][1] - b[0][1]))
        ax.view_init(elev=el, azim=az); ax.set_title(t, fontsize=9)
        ax.set_xlabel("x(bore)"); ax.set_ylabel("y(row)"); ax.set_zlabel("z")
    plt.tight_layout(); plt.savefig(path, dpi=95); plt.close()


def main():
    os.makedirs(OUT, exist_ok=True)
    _scales = {"--scale-e": ("scale-e", E_MAJOR, "halfcut_scale_Emajor", "E major(E6-E7)"),
               "--scale-eb": ("scale-eb", EB_MAJOR, "halfcut_scale_Ebmajor", "Eb major(D#6-D#7)"),
               "--scale-f": ("scale-f", F_MAJOR7, "halfcut_scale_Fmajor7", "F major 7音(F6-E7)"),
               "--scale-chrom": ("scale-chrom", CHROMATIC, "halfcut_scale_chromatic", "クロマチック(F6-E7 半音12)"),
               "--scale-full": ("scale-full", FULLRANGE, "halfcut_scale_fullrange", "全域探索(F6-A7 半音17)"),
               "--scale-low3": ("scale-low3", LOWSHIFT3, "halfcut_comb17_low3", "低音シフト(D6-F#7 半音17・3半音下げ)"),
               "--scale": ("scale", A_MAJOR, "halfcut_scale_Amajor", "A major(A6-A7)")}
    mode = "limit" if "--limit" in sys.argv else "calib"
    for flag, (mname, notes_sel, stem_, label) in _scales.items():
        if flag in sys.argv:
            mode = mname; break
    if mode.startswith("scale"):
        comb, infos, notes, lengths = scale_comb(notes=notes_sel)
        stem = stem_
        print("半割り笛 音階コーム（%s・実測較正で管長決定・D字/平置き）:" % label)
        for it in infos:
            print("    %-4s L=%4.1fmm  行y=%5.1f  予測 %5.0fHz" % (it["note"], it["L"], it["y"], it["freq"]))
    elif mode == "limit":
        comb, infos, lengths = limit_comb()
        stem = "halfcut_limit_comb"
        print("半割り笛 限界探索コーム（既知36-64mmを超えて両端へ。予測は外挿=要実測）:")
        for it in infos:
            print("    L=%2dmm  行y=%5.1f  予測 %5.0fHz  フット先 x=%.1f" % (it["L"], it["y"], it["freq"], it["x_foot"]))
    else:
        comb, infos = half_calib_comb()
        stem = "halfcut_calib_comb"
        print("半割り笛 較正コーム（D字断面のまま長さのみ可変・平置きサポートフリー）:")
        print("  管長→音程（実測較正 f=%.0f/(L%+.1f)。範囲 G#6〜A7 の約1.1oct）" % (_A, _E))
        for it in infos:
            print("    L=%2dmm  行y=%5.1f  概算 %5.0fHz  フット先 x=%.1f" % (it["L"], it["y"], it["freq"], it["x_foot"]))
    name = os.path.join(OUT, stem + ".stl")
    comb.export(name)
    print("  笛数=%d 外形=%s watertight=%s -> %s" %
          (len(infos), tuple(np.round(comb.extents, 1)), comb.is_watertight, name))
    _render(comb, infos, os.path.join(OUT, stem + "_views.png"))
    print("  render -> out/%s_views.png" % stem)


if __name__ == "__main__":
    main()
