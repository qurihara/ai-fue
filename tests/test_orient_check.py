"""orient_check の判定が、実機で確かめた結果と食い違わないかを確かめる。"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "fue"))
import numpy as np
import orient_check as oc


def roll(deg):
    """横置きのまま、長軸(x)まわりに deg 度回した向きを返す。"""
    t = math.radians(deg)
    R = np.array([[1, 0, 0], [0, math.cos(t), -math.sin(t)], [0, math.sin(t), math.cos(t)]])
    return dict(R=R)


def stand(mouth):
    """縦置き。mouth="up" なら吸込口が上、"down" なら下。"""
    b = math.radians(90.0 if mouth == "up" else -90.0)
    R = np.array([[math.cos(b), 0, math.sin(b)], [0, 1, 0], [-math.sin(b), 0, math.cos(b)]])
    return dict(R=R)


def main():
    fails = []

    def expect(name, kw, verdict, angle=None):
        r = oc.check_orientation(**kw)
        ok = r.verdict == verdict
        if angle is not None and not math.isnan(r.angle_deg):
            ok = ok and abs(((r.angle_deg - angle + 180) % 360) - 180) < 1.0
        print("%-22s → %-7s 角度%7.1f 傾き%5.1f  %s"
              % (name, r.verdict, r.angle_deg, r.tilt_deg, "PASS" if ok else "**FAIL**"))
        if not ok:
            fails.append(name)

    # 実機で鳴った角度は ok になること
    for d in (0, 45, -45, 90, -90, 135, -135):
        expect("横置き %+d度" % d, roll(d), "ok", angle=d)
    # 実機で鳴らなかった角度は ng になること
    for d in (180, -180, 150, -160):
        expect("横置き %+d度" % d, roll(d), "ng")
    # 縦置き
    expect("縦置き 吸込口が下", stand("down"), "caution")
    expect("縦置き 吸込口が上", stand("up"), "ng")
    # 中途半端な傾きは未検証
    t = math.radians(45)
    Ry = np.array([[math.cos(t), 0, math.sin(t)], [0, 1, 0], [-math.sin(t), 0, math.cos(t)]])
    expect("長軸が45度傾く", dict(R=Ry), "unknown")
    # 向きを直接渡す形
    expect("直接指定 窓が+y", dict(window_normal=[0, 1, 0], long_axis=[1, 0, 0]), "ok", angle=-90)
    expect("直接指定 窓が-z", dict(window_normal=[0, 0, -1], long_axis=[1, 0, 0]), "ng")

    # 窓と長軸が直交していない渡し方は弾く
    try:
        oc.check_orientation(window_normal=[1, 0, 0], long_axis=[1, 0, 0])
        print("直交していない入力       → **FAIL**（弾かれなかった）"); fails.append("直交検査")
    except ValueError:
        print("直交していない入力       → PASS（ValueErrorで弾いた）")

    print()
    if fails:
        print("**FAIL** %d件: %s" % (len(fails), fails)); return 1
    print("orient_check: 全件パス")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
