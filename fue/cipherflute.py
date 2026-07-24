"""暗号笛（目標③派生）の第1段：本数の限界と引き込みの下限を測る実験用コーム。

正典の設計ドキュメントは cosense「暗号笛＝ハードウェアパスワードウォレット」。方針は、プレナム
（共通の吹き込み室）を使わず、口そのものを共有の吹き込み室にして、複数の吹き込み口をまとめて
くわえて同時に鳴らす構成である。既存のコード笛（半割笛を隣り合わせに並べたコーム）と同じ土台
（halfcut.scale_comb）を使い、目的の違う二種類のコームを作る。

測りたいこと（測定Webアプリ qurihara.github.io/ai-fue の複数ピーク検出で読む）：
  1. 広いコーム（cipher_wide5）：確実に鳴る帯 F6→D7 に音を広く散らした5本。全部を吹いたときに、
     5本の音の山がFFTで分かれて読めるか。分かれなければ4本、3本、2本とくわえる本数を減らし、
     どこまで分離できるかを見る＝同時に読める最大本数と、息が足りなくなる限界を測る。
  2. 詰めたコーム（cipher_close4）：帯の中ほどで隣り合う半音を4本。近い音どうしの山が引き込み
     合って（注入同期で）くっつくか、片方が消えるか＝分離できる最小の音の間隔を測る。

各歌口を一つずつ指で塞いだとき、その音の山だけが消えて他が変わらなければ、「各笛が鳴っているか
どうか」を独立に読めるということで、これが暗号笛の容量の土台になる。
"""
import os
import sys

import numpy as np
import trimesh

sys.path.insert(0, os.path.dirname(__file__))
import halfcut
# make_3mf は numpy-stl に依存し、ジオメトリ生成の trimesh/manifold とは別の環境にあるため、
# ここでは取り込まず、3mf化は下の main 内で環境が揃っているときだけ行う（無ければSTLのみ出す）。

OUT = os.path.join(os.path.dirname(__file__), os.pardir, "out")

# 実機で確実に鳴る帯 F6..D7（下端F6は余裕あり、上端はD7まで。D#7以上は無音と実機で判明）に音を
# 広く散らした5本。本数の限界を測る。互いに離れているのでFFTで分離しやすい最良条件になる。
WIDE5 = ["F6", "G6", "A6", "C7", "D7"]
# 帯の中ほどで隣り合う半音を4本。近い音どうしの引き込み（注入同期）が始まる下限を測る。
CLOSE4 = ["G#6", "A6", "A#6", "B6"]
# 詰めたコーム4本を、隣り合う2本ずつの独立した2ピースに分けたもの。2ピースを背合わせにすると
# 2×2の笛になり、各窓が外側の面に出るので指1本で1本ずつ塞げる（4本を一列に並べると中央の
# 窓が指では塞げないという2026-07-20の実測の問題を解く）。各ピース単独でも半音差の2本を同時に
# 吹く試験になり、2ピースを合わせると中央のA6-A#6の半音差も試せる。
CLOSE_PAIRS = [["G#6", "A6"], ["A#6", "B6"]]

# 内部壁で管長を決める方式の較正確認用。実機のクリーン域 F6..D#7 の半音11音。
UNIFORM_CALIB = ["F6", "F#6", "G6", "G#6", "A6", "A#6", "B6", "C7", "C#7", "D7", "D#7"]

# コーム同士をプレートで並べるときの、行方向(y)の隙間[mm]。
PLATE_GAP_Y = 8.0


def build_comb(notes):
    """音名リストから半割笛コームを作る。各ボアは独立のまま一体化される（実績パンフルートと同じ）。
    戻り値は (mesh, infos, 物理順の音名, 管長)。"""
    return halfcut.scale_comb(notes=notes, gap=0.0, merge=True)


WALL_MARGIN = 3.0   # 最長音にも壁を作るための外形余白[mm]（全笛を壁ありに揃える）


def build_uniform_comb(notes, L_max=None):
    """外形長を L_max に揃え、内部壁で各音の管長を決めたコームを作る。
    戻り値は (mesh, infos, 物理順の音名, 管長)。音の物理順は build_comb と同じ。
    """
    notes = list(reversed(notes))
    lengths = [round(halfcut.length_for_note(n), 1) for n in notes]
    # 一番長い音にも壁を入れて「最長だけ壁なし＝例外」をなくすため、余白を足す。
    # こうすると全笛が壁ありで挙動が揃い、較正のずれが残っても基準笛と同じように出て相殺される。
    body_length = (max(lengths) + WALL_MARGIN) if L_max is None else L_max
    flutes, infos = [], []
    y = 0.0
    overlap = 0.3
    for note, L in zip(notes, lengths):
        flute = halfcut._printpose(halfcut.uniform_body_flute(L, body_length))
        bounds = flute.bounds
        flute.apply_translation([-bounds[0][0], -bounds[0][1] + y, 0])
        placed_bounds = flute.bounds
        width = placed_bounds[1][1] - placed_bounds[0][1]
        infos.append(dict(L=L, y=round(y, 1), freq=halfcut.est_freq(L),
                          x_foot=round(placed_bounds[1][0], 1), note=note))
        y += width - overlap
        flutes.append(flute)
    comb = trimesh.boolean.union(flutes, engine="manifold")
    return comb, infos, notes, lengths


def uniform_calib_comb():
    """内部壁式の較正確認用半音11音コームをSTLに書き出す。"""
    os.makedirs(OUT, exist_ok=True)
    comb, infos, notes, lengths = build_uniform_comb(UNIFORM_CALIB)
    path = os.path.join(OUT, "cipher_uniform_calib.stl")
    comb.export(path)
    return comb, infos, notes, lengths


def _pairwise_min_ratio(freqs):
    """隣り合う音の周波数比のうち最小のもの（1に近いほど近接＝分離が難しい）。"""
    fs = sorted(freqs)
    return min(fs[i + 1] / fs[i] for i in range(len(fs) - 1))


def _report(title, notes, infos):
    fs = [it["freq"] for it in infos]
    r = _pairwise_min_ratio(fs)
    cents = 1200.0 * np.log2(r)
    print("  %s" % title)
    for it in infos:
        print("    %-4s L=%5.1fmm  予測 %5.0fHz  行y=%5.1f" %
              (it["note"], it["L"], it["freq"], it["y"]))
    print("    隣接音の最小間隔 = %.0fセント（比 %.3f）。1オクターブ内なので基音は互いの倍音に当たらない。"
          % (cents, r))


def _lay_on_plate(combs):
    """複数コームを行方向(y)に隙間を空けて並べ、一体のプレート用メッシュに連結する。
    各コームは水密のまま別々の物体として残る（スライサが個別に造形する）。"""
    placed = []
    y_cursor = 0.0
    for comb in combs:
        c = comb.copy()
        b = c.bounds
        c.apply_translation([-b[0][0], -b[0][1] + y_cursor, -b[0][2]])  # x下端0・y下端をy_cursorへ・z=0
        placed.append(c)
        y_cursor += (b[1][1] - b[0][1]) + PLATE_GAP_Y
    return trimesh.util.concatenate(placed)


def build_close_pairs():
    """詰めたコーム(CLOSE4)を隣り合う2本ずつの2ピースに分けて作り、1枚のプレートに並べる。
    各ピースは半割笛2本を密着一体化したもの。印刷姿勢では窓が下面・丸い背が上面なので、
    刷り上がった2ピースを背合わせ（丸い背どうしを合わせる）にすると、4つの窓が外側の2面に
    分かれて出て、指1本でどれでも塞げるようになる。戻り値はプレートのSTLパス。"""
    os.makedirs(OUT, exist_ok=True)
    pieces = []
    print("暗号笛 詰めコーム分割ピース（2本×2・背合わせで2×2・窓を1本ずつ塞ぐ用）:")
    for i, pair in enumerate(CLOSE_PAIRS):
        comb, infos, notes2, lengths = build_comb(pair)
        tag = chr(ord("A") + i)
        stem = "cipher_close_pair%s" % tag
        path = os.path.join(OUT, stem + ".stl")
        comb.export(path)
        _report("ピース%s（%s）" % (tag, "＋".join(notes2)), notes2, infos)
        print("    外形=%s watertight=%s -> out/%s.stl" %
              (tuple(np.round(comb.extents, 1)), comb.is_watertight, stem))
        pieces.append(comb)
    plate = _lay_on_plate(pieces)
    plate_stl = os.path.join(OUT, "cipher_close_pairs_plate.stl")
    plate.export(plate_stl)
    print("  2ピースのプレート 外形=%s -> out/cipher_close_pairs_plate.stl" %
          (tuple(np.round(plate.extents, 1)),))
    try:
        import make_3mf
        tmf = make_3mf.stl_to_3mf(plate_stl, "a1mini")
        print("  A1 mini 3mf -> %s (%.0f KB)" % (tmf, os.path.getsize(tmf) / 1024))
    except ImportError:
        print("  3mf化は別環境で: (numpy-stlのある python) fue/make_3mf.py out/cipher_close_pairs_plate.stl --printer a1mini")
    return plate_stl


SEPARATE_WIDE5 = ["F6", "G6", "A6", "C7", "D7"]   # 温度・吹圧の再実験用（基準A6を含み広く散る）


def build_separate_flutes(notes=None, gap=14.0, stem="cipher_separate_wide5"):
    """実験用に「1本ずつ独立した笛」を、連結せず間隔を空けて1枚のプレートに並べる。

    従来の可視長デザイン（halfcut.half_flute）＝長さで音を見分けられる（長い＝低い）。
    各笛は密着させず gap[mm] だけ離すので、刷り上がりは別々の物体になり、1本を手に取って
    その笛だけを吹ける（隣の窓に息が回り込む問題を根絶）。印刷時はブリムを付けてベッド定着を確保する
    （STLにブリムは含まれない＝スライサ設定。以前ブリムなしで定着に失敗した反省）。"""
    os.makedirs(OUT, exist_ok=True)
    notes = notes or SEPARATE_WIDE5
    base = trimesh.load(halfcut.BASE_STL)
    placed, infos = [], []
    y = 0.0
    print("暗号笛 実験用 1本ずつ独立した笛（連結なし・可視長で見分け可・要ブリム）:")
    for note in notes:
        L = halfcut.length_for_note(note)
        f = halfcut._printpose(halfcut.half_flute(L, base=base))
        b = f.bounds
        f.apply_translation([-b[0][0], -b[0][1] + y, 0])           # 吸込口 x=0・幅方向に y
        fb = f.bounds
        w = fb[1][1] - fb[0][1]
        infos.append(dict(note=note, L=round(L, 1), freq=halfcut.est_freq(L), y=round(y, 1)))
        print("    %-4s L=%5.1fmm  予測 %5.0fHz  行y=%5.1f  長さで見分け（長い＝低い）"
              % (note, L, halfcut.est_freq(L), y))
        placed.append(f)
        y += w + gap                                                # gap だけ離す＝連結しない
    plate = trimesh.util.concatenate(placed)                        # union しない＝別オブジェクトのまま
    path = os.path.join(OUT, stem + ".stl")
    plate.export(path)
    print("  %d本を別オブジェクトで配置 外形=%s watertight=%s -> out/%s.stl"
          % (len(notes), tuple(np.round(plate.extents, 1)), plate.is_watertight, stem))
    print("  ※印刷時はブリムを付けること（careful プロファイルは no_brim なので brim 版で刷る）。")
    return path


def main():
    if "--separate" in sys.argv:
        build_separate_flutes()
        return
    if "--uniform-calib" in sys.argv:
        comb, infos, notes, lengths = uniform_calib_comb()
        print("暗号笛 内部壁式較正確認コーム（F6-D#7 半音11音）:")
        _report("全笛同一外形長", notes, infos)
        print("    外形=%s watertight=%s -> out/cipher_uniform_calib.stl" %
              (tuple(np.round(comb.extents, 1)), comb.is_watertight))
        return
    if "--close-pairs" in sys.argv:
        build_close_pairs()
        return
    os.makedirs(OUT, exist_ok=True)
    specs = [
        ("cipher_wide5", WIDE5, "広いコーム（F6→D7に5本・本数の限界を測る）"),
        ("cipher_close4", CLOSE4, "詰めたコーム（隣接半音4本・引き込みの下限を測る）"),
    ]
    combs = []
    print("暗号笛 第1段 実験用コーム（プレナムなし・口でまとめて吹く前提）:")
    for stem, notes, label in specs:
        comb, infos, notes2, lengths = build_comb(notes)
        path = os.path.join(OUT, stem + ".stl")
        comb.export(path)
        _report(label, notes2, infos)
        print("    外形=%s watertight=%s -> out/%s.stl" %
              (tuple(np.round(comb.extents, 1)), comb.is_watertight, stem))
        combs.append(comb)

    # 2つを1枚のプレートにまとめる。A1 mini 用3mfは、環境が揃っていればここで作る。
    plate = _lay_on_plate(combs)
    plate_stl = os.path.join(OUT, "cipher_test_plate.stl")
    plate.export(plate_stl)
    print("  プレート（2コーム）外形=%s -> out/cipher_test_plate.stl" %
          (tuple(np.round(plate.extents, 1)),))
    try:
        import make_3mf
        tmf = make_3mf.stl_to_3mf(plate_stl, "a1mini")
        print("  A1 mini 3mf -> %s (%.0f KB)" % (tmf, os.path.getsize(tmf) / 1024))
    except ImportError:
        print("  3mf化は別環境で: (numpy-stlのある python) fue/make_3mf.py out/cipher_test_plate.stl --printer a1mini")


if __name__ == "__main__":
    main()
