"""サブプロジェクト③「日常品に笛を仕込む」：スマホケース一体の非常警報ホイッスル（PoC）。

パラメトリックな簡易ケース殻（背板＋側壁のトレー型）の周辺部に、実績の7mm flat笛を
一体化する。まずは「雑でよい」概念実証。TPU印刷前提（壁厚め）。機種寸法は phone_w/h/t
を変えて合わせる。窓（発音口）はケース外側に向け、吹込口を角に出して吹けるようにする。
"""
import os
import sys
import numpy as np
import trimesh

sys.path.insert(0, os.path.dirname(__file__))
import mini

OUT = os.path.join(os.path.dirname(__file__), os.pardir, "out")
# 薄型の本命＝v2円筒を半割りした極薄笛(40×4×7mm・厚み4mm・弱い力で安定発音・0.08mm積層で良好)
HALF40 = os.path.join(os.path.dirname(__file__), os.pardir, "mini", "recorder-mini-c-v3-half-v2-40.stl")
HALF60 = os.path.join(os.path.dirname(__file__), os.pardir, "mini", "recorder-mini-c-v3-half-v2-60.stl")


def phone_case(phone_w=72.0, phone_h=150.0, phone_t=8.0, wall=2.0, back=2.0, lip=2.5):
    """簡易スマホケース殻（背板＋側壁、前面開放トレー）。TPU前提で壁2mm。
    lip=前面へ回り込む縁（機種を保持）。ラフPoCなので角丸・カメラ穴は省略。"""
    cw, ch = phone_w + 2 * wall, phone_h + 2 * wall
    cd = back + phone_t                              # 背板＋機種厚（前面開放）
    outer = trimesh.creation.box(extents=[cw, ch, cd]); outer.apply_translation([0, 0, cd / 2.0])
    # 機種ポケット（前面+zへ開放）
    cav = trimesh.creation.box(extents=[phone_w, phone_h, phone_t + 2.0])
    cav.apply_translation([0, 0, back + (phone_t + 2.0) / 2.0])
    case = trimesh.boolean.difference([outer, cav], engine="manifold")
    info = dict(case_w=cw, case_h=ch, case_d=cd, wall=wall)
    return case, info


def case_with_whistle(corner="br", overlap=1.5, margin=2.0, flute_stl=HALF40, **kw):
    """ケース殻の『短辺(下端)の角』に 半割り極薄笛(40×4×7mm・厚み4mm) を一体化。
    管軸(40mm)を短辺(x)方向、幅(7mm)を短辺の奥行き(y)、厚み(4mm)をケース背面外へ薄く突出。
    corner: 'br'=右下 / 'bl'=左下。flute_stl=HALF40(短・約3.5kHz) or HALF60(長・約1.8kHz)。"""
    case, ci = phone_case(**kw)
    cw, ch, cd = ci["case_w"], ci["case_h"], ci["case_d"]
    m = trimesh.load(flute_stl)                                # 40(x,管軸)×4(y,厚み)×7(z,幅)
    b0 = m.bounds
    m.apply_translation([-(b0[0][0] + b0[1][0]) / 2.0, -(b0[0][1] + b0[1][1]) / 2.0,
                         -(b0[0][2] + b0[1][2]) / 2.0])         # 中心を原点へ
    # y(厚み4)→ケースz(背面外へ薄く), z(幅7)→ケースy(短辺の奥行き)。x軸まわり-90°: (x,y,z)->(x,z,-y)
    m.apply_transform(trimesh.transformations.rotation_matrix(-np.pi / 2.0, [1, 0, 0]))
    b = m.bounds                                              # x=40(管軸), y=7(幅), z=4(厚み)
    flen = b[1][0] - b[0][0]
    sx = 1.0 if corner == "br" else -1.0
    if sx > 0:
        tx = (cw / 2.0 - margin) - b[1][0]                     # 右端を右壁内側へ
    else:
        tx = (-cw / 2.0 + margin) - b[0][0]                    # 左端を左壁内側へ
    ty = (-ch / 2.0 + overlap + (b[1][1] - b[0][1]) / 2.0) - (b[0][1] + b[1][1]) / 2.0  # 下端沿い
    tz = -b[1][2] - 0.01 + 1.0                                 # 背面(z=0)外へ厚み分突出＋1mm食い込み
    m.apply_translation([tx, ty, tz])
    combo = trimesh.boolean.union([case, m], engine="manifold")
    info = dict(case=ci, flute=os.path.basename(flute_stl), flute_len=round(flen, 1), corner=corner,
                dims=tuple(np.round(combo.extents, 1)), watertight=bool(combo.is_watertight))
    return combo, info


def main():
    os.makedirs(OUT, exist_ok=True)
    # Pixel 7: 155.6 × 73.2 × 8.7mm
    combo, info = case_with_whistle(corner="br", phone_w=73.2, phone_h=155.6, phone_t=8.7)
    name = os.path.join(OUT, "phonecase_pixel7_whistle.stl")
    combo.export(name)
    print("Pixel7 ケース＋mini_v2 リコーダー（短辺の角に一体）:")
    print("  ケース %.1fx%.1fx%.1f  笛=%s(管長%.0fmm) 角=%s" %
          (info["case"]["case_w"], info["case"]["case_h"], info["case"]["case_d"],
           info["flute"], info["flute_len"], info["corner"]))
    print("  外形%s watertight=%s -> %s" % (info["dims"], info["watertight"], name))


if __name__ == "__main__":
    main()
