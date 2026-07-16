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


def case_with_whistle(corner="br", margin=0.0, embed=1.0, flute_stl=HALF40, **kw):
    """半割り極薄笛(40×4×7mm)を『ケースの短辺(下端)の縁に沿わせて』一体化する。
    管軸(x)=短辺方向、吹込口(ヘッド側=STL local x-min)を頂点(角)へ端揃えし頂点方向へ向ける。
    窓(平坦カット面=local y-min)は短辺の外(-y)へ向けて露出。厚み4mmが短辺縁から外へ薄く出る。
    corner: 'br'=右下(吹込口が右角) / 'bl'=左下(左角)。embed=縁への食い込み(mm)。
    flute_stl=HALF40(短・約3.5kHz) or HALF60(長・約1.8kHz)。"""
    case, ci = phone_case(**kw)
    cw, ch, cd = ci["case_w"], ci["case_h"], ci["case_d"]
    m = trimesh.load(flute_stl)                                # x=管軸(吹込口=x-min), y=厚み4(窓=y-min), z=幅7
    b0 = m.bounds
    m.apply_translation([-(b0[0][0] + b0[1][0]) / 2.0, -(b0[0][1] + b0[1][1]) / 2.0,
                         -(b0[0][2] + b0[1][2]) / 2.0])         # 中心を原点へ
    right = corner in ("br", "tr")
    if right:
        # y軸まわり180°: 吹込口(x-min)を+x端へ回す。窓(y-min)は-y面のまま維持
        m.apply_transform(trimesh.transformations.rotation_matrix(np.pi, [0, 1, 0]))
    b = m.bounds                                              # x=管軸(40), y=厚み(4), z=幅(7)
    flen = b[1][0] - b[0][0]
    # x: 吹込口端を頂点(左右壁の外面 ±cw/2)へ端揃え
    if right:
        tx = (cw / 2.0 - margin) - b[1][0]                     # 吹込口(+x端)→右角
    else:
        tx = (-cw / 2.0 + margin) - b[0][0]                    # 吹込口(-x端)→左角
    # y: 下短辺の縁(y=-ch/2)に載せ、厚み分を外(-y)へ突出。embed 分だけ縁へ食い込ませ接合
    ty = (-ch / 2.0 + embed) - b[1][1]                         # 笛の上端(y-max)を縁より embed 内側へ
    # z: 背面(z=0)側に寄せて配置（幅7mmが背面から立ち上がる）
    tz = -b[0][2]
    m.apply_translation([tx, ty, tz])
    combo = trimesh.boolean.union([case, m], engine="manifold")
    fb = m.bounds
    info = dict(case=ci, flute=os.path.basename(flute_stl), flute_len=round(flen, 1), corner=corner,
                flute_x=(round(fb[0][0], 1), round(fb[1][0], 1)), flute_y=(round(fb[0][1], 1), round(fb[1][1], 1)),
                dims=tuple(np.round(combo.extents, 1)), watertight=bool(combo.is_watertight))
    return combo, info


def _render(combo, path):
    """全体は笛が小さすぎて見えないため、下短辺の角(笛周辺)を拡大した3面を描く。"""
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    b = combo.bounds
    ylo = b[0][1]                                   # 下端(笛が突出する側)
    fig = plt.figure(figsize=(15, 5))
    for i, (t, (el, az)) in enumerate([("corner iso", (20, -70)), ("bottom (from -y)", (2, -90)), ("under (from below)", (80, -90))]):
        ax = fig.add_subplot(1, 3, i + 1, projection="3d")
        ax.add_collection3d(Poly3DCollection(combo.triangles, alpha=0.5, facecolor="#8899cc", edgecolor="#556"))
        ax.set_xlim(-45, 45); ax.set_ylim(ylo - 4, ylo + 36); ax.set_zlim(-16, 18)
        ax.view_init(elev=el, azim=az); ax.set_title(t, fontsize=9)
        ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
    plt.tight_layout(); plt.savefig(path, dpi=90); plt.close()


def main():
    os.makedirs(OUT, exist_ok=True)
    # Pixel 7: 155.6 × 73.2 × 8.7mm
    combo, info = case_with_whistle(corner="br", phone_w=73.2, phone_h=155.6, phone_t=8.7)
    name = os.path.join(OUT, "phonecase_pixel7_whistle.stl")
    combo.export(name)
    print("Pixel7 ケース＋半割り極薄笛（短辺の縁に沿わせ・吹込口を右角に端揃え）:")
    print("  ケース %.1fx%.1fx%.1f  笛=%s(管長%.0fmm) 角=%s" %
          (info["case"]["case_w"], info["case"]["case_h"], info["case"]["case_d"],
           info["flute"], info["flute_len"], info["corner"]))
    print("  笛x範囲%s y範囲%s（吹込口=x右端が頂点, 窓=-y外向き）" % (info["flute_x"], info["flute_y"]))
    print("  外形%s watertight=%s -> %s" % (info["dims"], info["watertight"], name))
    _render(combo, os.path.join(OUT, "phonecase_pixel7_half_views.png"))
    print("  render -> out/phonecase_pixel7_half_views.png")


if __name__ == "__main__":
    main()
