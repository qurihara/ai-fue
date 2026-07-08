"""和音ジグソーブロック（アイデア(1)）：機能和声の制約を幾何の嵌合に符号化する。

考え方（Wangタイルの和声版）:
  各ブロック = 1和音。左面=前の和音を受ける穴、右面=次へ渡すペグ。
  機能を「コネクタのy位置キー」で符号化する：
      T→S = キーα(y=+7) / S→D = キーβ(y=0) / D→T = キーγ(y=-7)
  隣り合う面のペグ(凸)と穴(凹)が同じy位置のときだけ嵌まる＝正しい機能遷移だけ連結できる。
  Tブロック: 左穴=γ / 右ペグ=α     （Dを受け、Sへ渡す）
  Sブロック: 左穴=α / 右ペグ=β
  Dブロック: 左穴=β / 右ペグ=γ
  → 連結できる並びは …T S D T S D… ＝機能和声の循環だけ。逆順や飛ばしはペグが壁に当たり嵌まらない。

最小4個 = I–IV–V–I（C F G C ＝ T S D T）。上面の凸ドット数＝度数(I=1,IV=4,V=5)。矢印は連結方向(+x)。

実行: trimesh + manifold3d（fold.py 等と同じ環境）。
"""
import os
import sys
import numpy as np
import trimesh

OUT = os.path.join(os.path.dirname(__file__), os.pardir, "out")

# --- ブロック寸法 ---
BX, BY, BZ = 30.0, 26.0, 9.0     # 本体 x(連結方向)×y(幅)×z(厚)
PEG_R = 3.5                       # ペグ半径
PEG_L = 5.0                       # ペグ突き出し
HOLE_R = 3.75                     # 穴半径（＝ペグ+0.25clearance）
HOLE_D = 6.0                      # 穴深さ
KEY_Y = {"a": 7.0, "b": 0.0, "g": -7.0}   # 機能キーの y位置（α/β/γ）

# 機能→(左穴キー, 右ペグキー)。T→S(α), S→D(β), D→T(γ) の循環。
FUNC = {"T": ("g", "a"), "S": ("a", "b"), "D": ("b", "g")}
# 和音定義：(表示名, 機能, 度数ドット数, 構成音)
CHORDS = {
    "I":  ("I",  "T", 1, ["C6", "E6", "G6"]),
    "IV": ("IV", "S", 4, ["F6", "A6", "C7"]),
    "V":  ("V",  "D", 5, ["G6", "B6", "D7"]),
}


def _cyl_x(r, length, center):
    """x軸に沿う円柱（ペグ/穴用）。center=(x,y,z)は円柱の中心。"""
    c = trimesh.creation.cylinder(radius=r, height=length, sections=48)
    c.apply_transform(trimesh.transformations.rotation_matrix(np.radians(90), [0, 1, 0]))
    c.apply_translation(center)
    return c


def chord_block(chord="I"):
    """1和音のジグソーブロックを生成。"""
    name, func, dots, notes = CHORDS[chord]
    lkey, rkey = FUNC[func]
    ly, ry = KEY_Y[lkey], KEY_Y[rkey]
    body = trimesh.creation.box(extents=[BX, BY, BZ])   # 中心原点

    # 右ペグ（+x面から突き出す）
    peg = _cyl_x(PEG_R, PEG_L + 1.0, center=[BX / 2 + PEG_L / 2 - 0.5, ry, 0])
    solid = trimesh.boolean.union([body, peg], engine="manifold")

    # 左穴（-x面から掘る）
    hole = _cyl_x(HOLE_R, HOLE_D + 1.0, center=[-BX / 2 - 0.5 + (HOLE_D + 1.0) / 2, ly, 0])
    solid = trimesh.boolean.difference([solid, hole], engine="manifold")

    # 上面：度数ドット（数=度数）＋連結方向矢印（+x）
    marks = []
    for i in range(dots):
        d = trimesh.creation.cylinder(radius=1.6, height=1.4, sections=24)
        d.apply_translation([-8 + i * 4.0, 5.0, BZ / 2 + 0.6])
        marks.append(d)
    # 矢印（三角柱）: +x方向を指す
    arr = trimesh.creation.box(extents=[6, 2.0, 1.2]); arr.apply_translation([3, -6, BZ / 2 + 0.5])
    tip = trimesh.creation.cylinder(radius=2.4, height=1.2, sections=3)
    tip.apply_transform(trimesh.transformations.rotation_matrix(np.radians(-90), [0, 0, 1]))
    tip.apply_translation([8, -6, BZ / 2 + 0.5])
    marks += [arr, tip]
    solid = trimesh.boolean.union([solid] + marks, engine="manifold")

    info = dict(chord=name, func=func, dots=dots, notes=notes,
                left_key=lkey, right_key=rkey, left_y=ly, right_y=ry)
    return solid, info


def four_block_plate(seq=("I", "IV", "V", "I"), gap=8.0):
    """最小4個(I-IV-V-I)を印刷用に間隔をあけて1プレートに並べる。"""
    blocks, infos = [], []
    y0 = 0.0
    for i, ch in enumerate(seq):
        b, info = chord_block(ch)
        b.apply_translation([0, y0, BZ / 2])   # z底を0へ
        y0 += BY + gap
        info["slot"] = i + 1
        blocks.append(b); infos.append(info)
    mesh = trimesh.util.concatenate(blocks)
    bb = mesh.bounds
    mesh.apply_translation([-(bb[0][0] + bb[1][0]) / 2, -(bb[0][1] + bb[1][1]) / 2, 0])
    return mesh, infos


def assembled(seq=("I", "IV", "V", "I")):
    """正しい並びを連結した状態（確認・レンダー用）。ペグを穴へ差し込んで一列に。"""
    blocks, infos = [], []
    xoff = 0.0
    for ch in seq:
        b, info = chord_block(ch)
        b.apply_translation([xoff, 0, BZ / 2])
        xoff += BX   # 本体幅ぶん進む（ペグが次の穴に入る）
        blocks.append(b); infos.append(info)
    return trimesh.util.concatenate(blocks), infos


# ---------------------------------------------------------------------------
# 笛化：各ブロックを「その和音の3音を鳴らす笛」にする。
# 3音を z方向にスタックした mini.pan_flute を核にする（吹込口=−x側面, 窓=−y側面）。
# ジグソー連結は上下(±z)面に置き、機能キーは x位置で符号化（α=+10/β=0/γ=−10）。
# → 和音ブロックを縦に積んで進行を作る（各ブロックの上ペグが次ブロックの下穴に嵌合）。
#   吹き方：各段の−x吹込口を（3口まとめて）吹くとその和音が鳴る。
# ---------------------------------------------------------------------------
KEY_X = {"a": 10.0, "b": 0.0, "g": -10.0}   # 機能キーの x位置（±z面の連結ペグ/穴）


def _cyl_z(r, length, center):
    c = trimesh.creation.cylinder(radius=r, height=length, sections=48)
    c.apply_translation(center)
    return c


def chord_whistle_block(chord="I"):
    """その和音の3音を鳴らす笛ブロック（pan_flute核＋±z面ジグソー連結）。"""
    sys.path.insert(0, os.path.dirname(__file__))
    import mini
    name, func, dots, notes = CHORDS[chord]
    lkey, rkey = FUNC[func]                     # 左(=下穴)/右(=上ペグ) の機能キー
    core, _ = mini.pan_flute(notes=notes)       # 3音 z-stack（centered x/y, z=0..H）
    b0, b1 = core.bounds
    H = b1[2]
    lx, rx = KEY_X[lkey], KEY_X[rkey]
    # 上面(+z)ペグ・下面(-z)穴
    peg = _cyl_z(PEG_R, PEG_L + 1.0, center=[rx, 0, H + PEG_L / 2 - 0.5])
    solid = trimesh.boolean.union([core, peg], engine="manifold")
    hole = _cyl_z(HOLE_R, HOLE_D + 1.0, center=[lx, 0, -0.5 + (HOLE_D + 1.0) / 2])
    solid = trimesh.boolean.difference([solid, hole], engine="manifold")
    info = dict(chord=name, func=func, notes=notes, dots=dots,
                left_key=lkey, right_key=rkey, left_x=lx, right_x=rx,
                dims=tuple(np.round(solid.extents, 1)))
    return solid, info


def chord_whistle_set(seq=("I", "IV", "V", "I"), gap=8.0):
    """和音笛ブロックを印刷用に間隔をあけて1プレートに並べる。"""
    blocks, infos = [], []
    xoff = 0.0
    for i, ch in enumerate(seq):
        b, info = chord_whistle_block(ch)
        w = b.extents[0]
        b.apply_translation([xoff + w / 2 - (b.bounds[0][0] + b.bounds[1][0]) / 2, 0, -b.bounds[0][2]])
        xoff += w + gap
        info["slot"] = i + 1
        blocks.append(b); infos.append(info)
    mesh = trimesh.util.concatenate(blocks)
    bb = mesh.bounds
    mesh.apply_translation([-(bb[0][0] + bb[1][0]) / 2, -(bb[0][1] + bb[1][1]) / 2, 0])
    return mesh, infos


def main():
    os.makedirs(OUT, exist_ok=True)
    if "--whistle" in sys.argv:
        mesh, infos = chord_whistle_set()
        mesh.export(os.path.join(OUT, "chordwhistle_IVVI.stl"))
        print("和音笛ブロック 最小4個 I-IV-V-I（3音pan_flute核＋±zジグソー）:")
        for i in infos:
            print("  slot%d %-3s func%s 音%s 外形%s 下穴%s(x=%+.0f) 上ペグ%s(x=%+.0f)"
                  % (i["slot"], i["chord"], i["func"], "/".join(i["notes"]), i["dims"],
                     i["left_key"], i["left_x"], i["right_key"], i["right_x"]))
        print("外形", np.round(mesh.extents, 1), "watertight", mesh.is_watertight,
              "-> out/chordwhistle_IVVI.stl")
        return
    mesh, infos = four_block_plate()
    mesh.export(os.path.join(OUT, "chordblocks_IVVI.stl"))
    print("和音ジグソーブロック 最小4個 I-IV-V-I:")
    for i in infos:
        print("  slot%d %-3s func%s dots%d 左穴%s(y=%+.0f) 右ペグ%s(y=%+.0f) 音%s"
              % (i["slot"], i["chord"], i["func"], i["dots"], i["left_key"], i["left_y"],
                 i["right_key"], i["right_y"], "/".join(i["notes"])))
    print("外形", np.round(mesh.extents, 1), "watertight", mesh.is_watertight,
          "-> out/chordblocks_IVVI.stl")


if __name__ == "__main__":
    main()
