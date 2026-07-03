"""目標②リボルバー笛（参考ジェノバ機構を再利用する版）。

構成（下→上）:
- ロータ = 参考の歯車(assets/geneva_ref/ref_wheel.stl)の上に、同一外形・同一歌口高さの
  コンパクト笛を6本、環状に立てたもの。歯車ごとジェノバで割り出し回転する。
- 固定中心軸 + ステータ = 歯車のハブ穴(Φ15)を通って歌口の上まで延びる固定軸の上端に、
  ポート穴が1つだけ開いた固定フタと吹き込み筒を付けたもの。ロータはこの軸の周りを回る。
  ポート直下に来た1本だけに送風され、順に吹くとメロディになる（ガトリング砲式）。

ステータは「軸＋フタ＋ポート＋吹き込み筒」を1部品にする。フタは全歌口を薄い隙間で覆うが、
息が入る口はポート1つだけなので、原則その1本だけが鳴る（v1のface seal、多少の漏れは許容）。
ポートの縁には短い襟(collar)を垂らして直下の歌口へ息を集める。

trimesh+manifold3d（コントローラ .venv）。ヘッドは非watertightなので結合せず重ねる。
"""
import os
import numpy as np
import trimesh

OUTER_D = 14.07
BORE_D = 9.5
HEAD_CUT_Z = 143.0
HEAD_TOP_Z = 169.48
HEAD_LEN = HEAD_TOP_Z - HEAD_CUT_Z   # 26.48
CALIB_K = 91891.5
CALIB_DELTA = 14.227

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF_WHEEL = os.path.join(HERE, "assets", "geneva_ref", "ref_wheel.stl")
HEAD_STL = os.path.join(HERE, "assets", "head_v6.stl")

NOTE_NAMES = {"C":0,"C#":1,"D":2,"D#":3,"E":4,"F":5,"F#":6,"G":7,"G#":8,"A":9,"A#":10,"B":11}


def note_freq(note):
    import re
    m = re.match(r"([A-G]#?)(-?\d)", note)
    midi = NOTE_NAMES[m.group(1)] + 12 * (int(m.group(2)) + 1)
    return 440.0 * 2 ** ((midi - 69) / 12)


def air_for_note(note):
    return CALIB_K / note_freq(note) - CALIB_DELTA


def _load_ref_wheel():
    """参考歯車を読み、ハブ中心を原点・底面をz=0へ。"""
    W = trimesh.load(REF_WHEEL)
    b = W.bounds
    W.apply_translation([-(b[0][0] + b[1][0]) / 2, -(b[0][1] + b[1][1]) / 2, -b[0][2]])
    return W


def _pipe(cx, cy, T, air):
    outer = trimesh.creation.cylinder(radius=OUTER_D / 2, height=T, sections=64)
    outer.apply_translation([cx, cy, T / 2])
    bore = trimesh.creation.cylinder(radius=BORE_D / 2, height=air + 1, sections=48)
    bore.apply_translation([cx, cy, T - air / 2 + 0.5])
    return trimesh.boolean.difference([outer, bore])


def _place_head(cx, cy, z_bottom, yaw=0.0):
    m = trimesh.load(HEAD_STL)
    if yaw:
        m.apply_transform(trimesh.transformations.rotation_matrix(yaw, [0, 0, 1]))
    b = m.bounds
    m.apply_translation([cx - (b[0][0] + b[1][0]) / 2, cy - (b[0][1] + b[1][1]) / 2, z_bottom - b[0][2]])
    return m


def build_rotor(notes, gap=4.0, T=None):
    """参考歌車 + 6笛のロータ。戻り値: (mesh, info)。全笛は同一外形・同一歌口高さ。"""
    airs = [air_for_note(n) for n in notes]
    if T is None:
        T = max(airs) + 4.0
    N = len(notes)
    W = _load_ref_wheel()
    wtop = W.bounds[1][2]                       # 歯車上面 z
    R = max((OUTER_D + gap) * N / (2 * np.pi), OUTER_D)   # 笛が重ならない環半径
    mouth_z = wtop + T + HEAD_LEN               # 歌口(ヘッド上端)の高さ
    bodies, heads = [], []
    for i, air in enumerate(airs):
        a = 2 * np.pi * i / N
        cx, cy = R * np.cos(a), R * np.sin(a)
        bodies.append(_pipe(cx, cy, wtop + T, air))     # 胴はz=0..wtop+T（歯車に食い込ませて結合）
        # ヘッドは半径方向に向きを揃える（各笛を同じ相対姿勢にしてポートが同一に被さるように）
        heads.append(_place_head(cx, cy, wtop + T, yaw=a))
    rotor = trimesh.util.concatenate([W] + bodies + heads)
    info = dict(N=N, R=round(R, 2), T=round(T, 2), wtop=round(wtop, 2),
                mouth_z=round(mouth_z, 2), notes=list(notes),
                airs=[round(x, 1) for x in airs], freqs=[round(note_freq(n)) for n in notes])
    return rotor, info


def build_stator(info, hub_d=15.0, axle_clr=0.35, gap=0.5,
                 inlet_h=16.0, base_seat=2.0, arm_w=12.0, arm_th=3.0):
    """固定中心軸 + 「1本だけを覆うカップ」+ 吹き込み筒（1部品）。

    全面フタにすると薄い隙間でプレナム化して全笛が鳴るため、フタは張らず、中心軸から
    半径方向の腕(arm)を1本だけ伸ばし、その先に1本の歌口を覆うカップを付ける。ポート直下に
    来た笛だけに息が入り、他の5本は上が開いていて送風されない。回すと順に鳴る（ガトリング式）。

    軸は歯車ハブ穴(Φhub_d)より細く（回転隙間axle_clr）、ロータはこの固定軸の周りを回る。
    """
    R = info["R"]
    mouth_z = info["mouth_z"]
    axle_r = hub_d / 2 - axle_clr
    cup_z0 = mouth_z + gap                 # カップ下端（歌口の少し上、ここを歌口が回って通る）
    cup_z1 = cup_z0 + 3.0                  # カップ天井
    arm_z1 = cup_z1
    arm_z0 = cup_z1 - arm_th
    cup_ro = OUTER_D / 2 + 2.0             # カップ外半径
    cup_ri = OUTER_D / 2 + 0.5             # カップ内半径（歌口Φ14.07+隙間）

    parts = []
    # 中心固定軸
    axle = trimesh.creation.cylinder(radius=axle_r, height=arm_z1 + base_seat, sections=64)
    axle.apply_translation([0, 0, (arm_z1 + base_seat) / 2 - base_seat])
    parts.append(axle)
    # 腕（中心→カップ）: 薄い平板。他の歌口は覆わない（半径方向のみ）
    arm = trimesh.creation.box(extents=[R + cup_ro, arm_w, arm_th])
    arm.apply_translation([(R + cup_ro) / 2 - 1, 0, (arm_z0 + arm_z1) / 2])
    parts.append(arm)
    # カップ（1本の歌口を覆う筒。天井は閉、下は開）
    cup = trimesh.creation.cylinder(radius=cup_ro, height=cup_z1 - cup_z0, sections=48)
    cup.apply_translation([R, 0, (cup_z0 + cup_z1) / 2])
    parts.append(cup)
    # 吹き込み筒（カップ天井の上）
    inlet_o = trimesh.creation.cylinder(radius=BORE_D / 2 + 2.0, height=inlet_h, sections=48)
    inlet_o.apply_translation([R, 0, arm_z1 + inlet_h / 2])
    parts.append(inlet_o)
    stator = trimesh.boolean.union(parts)

    # くり抜き: カップ内腔（下開き）＋ 吹き込み筒の内腔をつなぐ
    cuts = []
    cavity = trimesh.creation.cylinder(radius=cup_ri, height=(cup_z1 - cup_z0) + 0.2, sections=48)
    cavity.apply_translation([R, 0, cup_z0 + ((cup_z1 - cup_z0) + 0.2) / 2 - 0.1])  # 下端は開口
    cuts.append(cavity)
    bore = trimesh.creation.cylinder(radius=BORE_D / 2, height=inlet_h + arm_th + 2, sections=48)
    bore.apply_translation([R, 0, arm_z0 + (inlet_h + arm_th + 2) / 2 - 0.5])
    cuts.append(bore)
    stator = trimesh.boolean.difference([stator] + cuts)
    sinfo = dict(axle_r=round(axle_r, 2), cup_at=(round(R, 2), 0.0),
                 cup_z0=round(cup_z0, 2), top_z=round(arm_z1 + inlet_h, 2))
    return stator, sinfo


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--notes", default="E6 B6 G#6 E7 F#7 B7", help="6音（1UP=長三度上げ既定）")
    ap.add_argument("--rotor", default="out/revolver_geneva_rotor.stl")
    ap.add_argument("--stator", default="out/revolver_geneva_stator.stl")
    a = ap.parse_args()
    notes = a.notes.split()
    rotor, info = build_rotor(notes)
    stator, sinfo = build_stator(info)
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    rotor.export(os.path.join(HERE, a.rotor))
    stator.export(os.path.join(HERE, a.stator))
    print("リボルバー笛（ジェノバ版）: %d音 %s" % (info["N"], " ".join(notes)))
    print("  狙い周波数:", info["freqs"], "Hz")
    print("  気柱長:", info["airs"], "mm  外形共通T=%.1f" % info["T"])
    print("  環半径R=%.1f 歌口高さ=%.1f 歯車上面=%.1f" % (info["R"], info["mouth_z"], info["wtop"]))
    print("  ロータ外形:", np.round(rotor.extents, 1), " watertight(胴):n/a(ヘッド重ね)")
    print("  ステータ:", np.round(stator.extents, 1), " watertight=", stator.is_watertight, sinfo)
    print("  saved", a.rotor, a.stator)
