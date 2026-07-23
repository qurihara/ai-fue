"""CipherFlute用 mini10 ヘッド生成（厚壁1mm・床0.5mm・深窓）。

旧 halfcut（薄壁 mini v2）を置き換える本命ヘッド。安定帯は F#6(1480Hz)〜G#7(3320Hz)＝14〜15半音と
広く、0.5mm壁の無発音・印刷不良を解消する。基STL mini10/recorder-mini-c-v3-half-2-v2.stl の
フット(x>=THR=17)を平行移動して管長を変える（Chordika の make_chordika_mini10.py と同じ機構）。

較正 f=A/(L+e) は out/mini10_calib_v11.txt（1行目 A= / 2行目 e=）を読む。Chordika と共有。
現況 A=85695.9, e=-12.57（C/Am カード全域8長さの再フィット・RMS 17.8セント）。CipherFlute の
コームでも当たるかは、可視長の較正コームを刷って実測で確認する（この段の目的）。

姿勢: 基STL は窓が上面(+z)・床が下面(z=0, 0.5mm)。寝かせ印刷そのままでサポートフリー。
"""
import os
import numpy as np
import trimesh

ROOT = os.path.join(os.path.dirname(__file__), os.pardir)
BASE = os.path.join(ROOT, "mini10", "recorder-mini-c-v3-half-2-v2.stl")
OUT = os.path.join(ROOT, "out")

THR = 17.0          # このx以上（フット）を平行移動して管長を変える
BASE_LEN = 60.0     # 基STLの管長

NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']


def _load_calib():
    """A,e を読む。CipherFlute専用 out/cipher_mini10_calib.txt があればそれを優先し、
    無ければ Chordika 共有の out/mini10_calib_v11.txt、いずれも無ければ暫定値。
    CipherFlute のコームは Chordika のカードと形が違うので較正を分離する（2026-07-23 確定）。"""
    A, E = 86338.0, -13.06
    for name in ("cipher_mini10_calib.txt", "mini10_calib_v11.txt"):
        p = os.path.join(OUT, name)
        if os.path.exists(p):
            for line in open(p):
                line = line.strip()
                if line.startswith("A="):
                    A = float(line.split("=")[1].split()[0])
                elif line.lower().startswith("e="):
                    E = float(line.split("=")[1].split()[0])
            break
    return A, E


A, E = _load_calib()


def note_to_midi(note):
    name, octv = note[:-1], int(note[-1])
    return 12 * (octv + 1) + NAMES.index(name)


def note_to_freq(note):
    return 440.0 * 2 ** ((note_to_midi(note) - 69) / 12.0)


def est_freq(L):
    """管長L[mm]→基本周波数[Hz]（mini10 較正）。"""
    return A / (L + E)


def length_for_note(note):
    """音名→その音を出す管長[mm]。L = A/f - e（e<0 なので実質 +）。"""
    return A / note_to_freq(note) - E


def flute(L, base=None):
    """管長 L[mm] の mini10 半割笛メッシュ（native向き: 窓が+z・床がz=0）。"""
    m = (base if base is not None else trimesh.load(BASE)).copy()
    v = m.vertices.copy()
    v[v[:, 0] >= THR, 0] += (L - BASE_LEN)     # フットを平行移動して総管長を L に
    m.vertices = v
    m.merge_vertices()
    b = m.bounds
    m.apply_translation([-b[0][0], -b[0][1], -b[0][2]])   # 最小角を原点へ
    return m


def build_calib_comb(notes, gap=0.0, merge=True, overlap=0.3):
    """音名リストの可視長コーム（各笛の実管長がそのまま外形＝長さで見分けられる）。
    全笛の吸込口(x=0)を揃え、フットが長いほど+xへ伸びる。幅方向(y)に並べる。
    戻り値 (mesh, infos)。infos は note/L/freq/y。"""
    base = trimesh.load(BASE)
    flutes, infos = [], []
    y = 0.0
    for n in notes:
        L = length_for_note(n)
        f = flute(L, base=base)
        b = f.bounds
        f.apply_translation([-b[0][0], -b[0][1] + y, 0])
        fb = f.bounds
        w = fb[1][1] - fb[0][1]
        infos.append(dict(note=n, L=round(L, 1), freq=est_freq(L), y=round(y, 1)))
        step = w + gap
        if merge and gap == 0.0:
            step -= overlap
        y += step
        flutes.append(f)
    if merge:
        comb = trimesh.boolean.union(flutes, engine="manifold")
    else:
        comb = trimesh.util.concatenate(flutes)
    return comb, infos


def uniform_flute(L, L_max=None, wall_thickness=1.3, correction_mm=0.0):
    """外見統一版：外形を最長管 L_max に揃え、内部の仕切り壁でボア長(=音長)を L にする。
    壁より末端側のボアは埋めず密閉空洞のまま残す(重さをほぼ一定に保つ)。基礎実験では
    correction_mm=0（壁を音長Lちょうどに置く）で刷り、下がり量を実測してから補償を決める。
    向きは flute と同じ native（窓=+z, 床=z=0, 最小角=原点）。L>=L_max では壁なし。"""
    if L_max is None or L >= L_max:
        return flute(L)
    shell = flute(L_max)
    b = shell.bounds
    wall_x0 = L - correction_mm            # 壁の頭側の面（ここでボアを閉じる＝ボア長L）
    extents = [wall_thickness,
               b[1][1] - b[0][1] + 1.0,
               b[1][2] - b[0][2] + 1.0]
    center = [wall_x0 + wall_thickness / 2.0,
              (b[0][1] + b[1][1]) / 2.0,
              (b[0][2] + b[1][2]) / 2.0]
    wall_box = trimesh.creation.box(
        extents=extents,
        transform=trimesh.transformations.translation_matrix(center))
    # ボアを含む外形断面だけを壁にする（直方体の外側は外形に出さない）
    wall = trimesh.boolean.intersection([wall_box, shell.convex_hull], engine="manifold")
    out = trimesh.boolean.union([shell, wall], engine="manifold")
    out.apply_translation(-out.bounds[0])
    return out


def build_uniform_calib_comb(notes, correction_mm=0.0, gap=0.0, merge=True, overlap=0.3):
    """外見統一版の較正コーム：全笛の外形長を最長音(=最低音)に揃える。戻り値 (mesh, infos)。
    見た目では音（長さ）が分からないので、研究では順番で識別する（低い順に並べる）。"""
    base = trimesh.load(BASE)
    Ls = [length_for_note(n) for n in notes]
    L_max = max(Ls)
    flutes, infos, y = [], [], 0.0
    for n, L in zip(notes, Ls):
        f = uniform_flute(L, L_max=L_max, correction_mm=correction_mm)
        b = f.bounds
        f.apply_translation([-b[0][0], -b[0][1] + y, 0])
        fb = f.bounds
        w = fb[1][1] - fb[0][1]
        infos.append(dict(note=n, L=round(L, 1), freq=est_freq(L), y=round(y, 1)))
        step = w + gap - (overlap if (merge and gap == 0.0) else 0.0)
        y += step
        flutes.append(f)
    comb = trimesh.boolean.union(flutes, engine="manifold") if merge else trimesh.util.concatenate(flutes)
    return comb, infos


# 素数13スロットの較正コーム: F#6..F#7（安定帯 F#6〜G#7 の下側13音・GF(13)で1記号=1本）。
CALIB13 = ["F#6", "G6", "G#6", "A6", "A#6", "B6", "C7", "C#7", "D7", "D#7", "E7", "F7", "F#7"]


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    print("mini10 較正定数: A=%.1f e=%.3f" % (A, E))
    comb, infos = build_calib_comb(CALIB13)
    print("CipherFlute mini10 可視長 較正コーム（F#6〜F#7・13音・厚壁1mm）:")
    for it in infos:
        print("  %-4s L=%5.1fmm  予測 %5.0fHz  行y=%5.1f" %
              (it["note"], it["L"], it["freq"], it["y"]))
    path = os.path.join(OUT, "cipher_mini10_calib13.stl")
    comb.export(path)
    print("  外形=%s mm watertight=%s -> out/cipher_mini10_calib13.stl" %
          (tuple(np.round(comb.extents, 1)), comb.is_watertight))
