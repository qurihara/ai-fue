"""ジェノバ機構（外ジェノバ）の生成器 — 目標②リボルバー笛の1音ずつ割り出し用。

駆動側（driver）を1回転させると、割り出し盤（driven, Geneva wheel）が 1/N 回転だけ進み、
残りの間はロック板で静止する。これでリボルバー笛の各笛を吹き込み口の真下で止められる。

外ジェノバの基本寸法（スロット数N・中心間距離D）:
  クランクのピン距離   Rc = D·sin(π/N)
  割り出し盤の半径     R2 = D·cos(π/N)   （Rc² + R2² = D²）

まずは機構だけ（driver + driven + 2軸の台）を検証用に作る。噛み合いはトレランス依存なので、
これを1枚刷って「送り／ロック」を確かめてから、笛カルーセルを driven の上に載せる。

2Dプロファイルは shapely、押し出しは trimesh（コントローラ .venv）。
"""
import numpy as np
import trimesh
from shapely.geometry import Point, box
from shapely.affinity import rotate as srotate, translate as stranslate
from shapely.ops import unary_union


def geneva_2d(N, D, pin_r=2.5, clr=0.35, axle_r=2.1):
    Rc = D * np.sin(np.pi / N)          # クランクのピン距離（駆動中心→ピン）
    R2 = D * np.cos(np.pi / N)          # 割り出し盤の半径（スロット入口）
    Rw = R2 + pin_r + 3                 # 盤の外半径（入口の少し外）
    Rin = D - Rc - 1                    # スロット内端（ピンの最接近半径）
    w = 2 * pin_r + 2 * clr             # スロット幅
    Rlock = Rc - pin_r - 1.0            # ロック板の半径

    # --- driven（割り出し盤）: 駆動は +x 方向 (D,0) にあるとする ---
    wheel = Point(0, 0).buffer(Rw, resolution=96)
    for k in range(N):
        ang = 360.0 * k / N
        slot = box(Rin, -w / 2, Rw + 3, w / 2)          # +x向きの半径スロット
        slot = srotate(slot, ang, origin=(0, 0))
        wheel = wheel.difference(slot)
        lock_cut = Point(D, 0).buffer(Rlock + clr, resolution=64)  # ロック用の凹み
        lock_cut = srotate(lock_cut, ang, origin=(0, 0))
        wheel = wheel.difference(lock_cut)
    wheel = wheel.difference(Point(0, 0).buffer(axle_r + clr, resolution=48))

    # --- driver（駆動）: 盤は +x 方向 (D,0) にある。自分の中心を原点に置く ---
    disc = Point(0, 0).buffer(Rlock, resolution=96)      # ロック板
    disc = disc.difference(Point(D, 0).buffer(Rw + clr, resolution=96))  # 盤が回れるよう切り欠く
    pin = Point(Rc, 0).buffer(pin_r, resolution=48)      # スロットに入るピン
    crank = box(-axle_r - 2, -4, Rc + 6, 4)              # クランク腕
    driver = unary_union([disc, pin, crank]).difference(Point(0, 0).buffer(axle_r + clr, resolution=48))

    return wheel, driver, dict(Rc=round(Rc, 1), R2=round(R2, 1), Rw=round(Rw, 1), Rlock=round(Rlock, 1), D=D, N=N)


def build(N=6, D=44.0, th=6.0, base_th=3.0, post_h=None, axle_r=2.1):
    wheel2d, driver2d, g = geneva_2d(N, D, axle_r=axle_r)
    wheel = trimesh.creation.extrude_polygon(wheel2d, height=th)
    driver = trimesh.creation.extrude_polygon(driver2d, height=th)
    # 台と2本の軸（driven=原点, driver=(D,0)）。組み立て用に別STLで返す
    span = g["Rw"] + D + g["Rc"] + 12
    base = trimesh.creation.box(extents=[g["Rw"] + D + g["Rc"] + 20, 2 * g["Rw"] + 12, base_th])
    base.apply_translation([(D) / 2, 0, -base_th / 2])
    ph = post_h or th + 3
    post_a = trimesh.creation.cylinder(radius=axle_r, height=ph, sections=48); post_a.apply_translation([0, 0, ph / 2])
    post_b = trimesh.creation.cylinder(radius=axle_r, height=ph, sections=48); post_b.apply_translation([D, 0, ph / 2])
    stand = trimesh.boolean.union([base, post_a, post_b])
    return wheel, driver, stand, g


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--N", type=int, default=6)
    ap.add_argument("--D", type=float, default=44.0)
    ap.add_argument("--out", default="out/geneva")
    a = ap.parse_args()
    wheel, driver, stand, g = build(a.N, a.D)
    wheel.export(a.out + "_wheel.stl"); driver.export(a.out + "_driver.stl"); stand.export(a.out + "_stand.stl")
    print("ジェノバ機構 N=%d D=%.0f: Rc=%.1f R2=%.1f 盤半径Rw=%.1f ロック半径=%.1f" % (g["N"], g["D"], g["Rc"], g["R2"], g["Rw"], g["Rlock"]))
    for nm, m in [("wheel", wheel), ("driver", driver), ("stand", stand)]:
        print("  %-7s %s mm  watertight=%s" % (nm, np.round(m.extents, 1), m.is_watertight))
    print("  saved", a.out + "_{wheel,driver,stand}.stl")
