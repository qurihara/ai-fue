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


def case_with_whistle(note="C6", N=1, **kw):
    """ケース殻の +x 側面の周辺部に 7mm flat笛を一体化。笛の長手をケース高さ(y)に沿わせ、
    窓(-y面)を +x 外側に向け、吹込口(-x端)をケース下端の角に出す（吹ける位置）。"""
    case, ci = phone_case(**kw)
    cw, ch, cd = ci["case_w"], ci["case_h"], ci["case_d"]
    f, fi = mini.flat_flute(note=note, N=N)          # 長手x, 窓-y, 厚みz（7mm）
    # z軸+90°回転: (x,y)->(-y,x)。長手x→+y、窓-y面の法線(0,-1)->(+1,0)=+x（外向き）。
    f.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2.0, [0, 0, 1]))
    fb = f.bounds
    fl_len = fb[1][1] - fb[0][1]      # 笛の長さ(いまy方向)
    fl_th = fb[1][0] - fb[0][0]       # 笛の厚み(いまx方向, 7mm)
    fl_h = fb[1][2] - fb[0][2]        # 笛の高さ(z, 7mm)
    # 配置：+x側壁の外面に貼る（少し食い込ませて一体化）。y中央、背面側(z=0..)に載せる。
    x_place = cw / 2.0 - 1.0          # 側壁外面に1mm食い込み
    f.apply_translation([x_place - fb[0][0], -(fb[0][1] + fb[1][1]) / 2.0, -fb[0][2] + 0.5])
    combo = trimesh.boolean.union([case, f], engine="manifold")
    info = dict(case=ci, flute=dict(note=note, N=N, len=round(fl_len, 1), th=round(fl_th, 1)),
                dims=tuple(np.round(combo.extents, 1)), watertight=bool(combo.is_watertight))
    return combo, info


def main():
    os.makedirs(OUT, exist_ok=True)
    combo, info = case_with_whistle()
    name = os.path.join(OUT, "phonecase_whistle_demo.stl")
    combo.export(name)
    print("スマホケース＋7mm警報笛 PoC:")
    print("  ケース %.0fx%.0fx%.0f  笛 %s(N=%d) 長さ%.0fmm" %
          (info["case"]["case_w"], info["case"]["case_h"], info["case"]["case_d"],
           info["flute"]["note"], info["flute"]["N"], info["flute"]["len"]))
    print("  外形%s watertight=%s -> %s" % (info["dims"], info["watertight"], name))


if __name__ == "__main__":
    main()
