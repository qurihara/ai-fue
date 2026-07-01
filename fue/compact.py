"""コンパクト音階笛ジェネレータ（目標①）。

v6の解析で分かった構造を使う。v6は「上端の吹き口ブロック＋ウインドウェイ、その少し下の
フィッポル窓、下へ伸びる直管ボア、下端の閉端」からなる縦笛である。直管ボアは音程を決める
ためだけの共鳴管であり、ヘッド（窓と吹き口）は固定の実績部品である。

そこで1本の笛を次のように組み立てる。実績のあるヘッド（assets/head_v6.stl、v6の上端26.5mm
を切り出したもの）を上に置き、その下へ「必要な長さぶんだけの中空管」と「閉端キャップ」を足す。
棒も死んだ材料も使わないので、高い音ほど短い笛になる。全長は 26.5mm＋管長 になる。

管長と音程の対応は、端補正やフィッポルの実効長のため物理式では正確に出ない。実測で較正する
必要があるので、まず管長を段階的に変えた較正用コームを出力し、1回の印刷で対応表を作る。

ボア（中空）は差し引き（boolean）で作れないので、中空の管壁（annulus）として最初から作る。
結合はメッシュを重ねてスライサに任せる方針（build.py と同じ）。
"""
from __future__ import annotations
import argparse
import os

import numpy as np
from stl import mesh as npmesh

from build import cylinder, annulus, translate, bbox, save, check_watertight, OUT, ASSETS

HEAD = os.path.join(ASSETS, "head_v6.stl")
HEAD_CUT_Z = 143.0      # v6座標での切断面（この面が管の上端に接する）
HEAD_TOP_Z = 169.48     # v6座標でのヘッド上端
HEAD_LEN = HEAD_TOP_Z - HEAD_CUT_Z   # 約26.5mm
OUTER_D = 14.07         # v6本体の外径に合わせる
BORE_D = 9.5            # 共鳴管の内径（v6ボア約10mmに合わせる）
CAP_TH = 2.0            # 閉端キャップの厚み


def _head_tris(head_path: str, bore_top_z: float) -> np.ndarray:
    """ヘッドを読み込み、x/yの中心を原点へ、切断面を z=bore_top_z へ合わせる。"""
    m = npmesh.Mesh.from_file(head_path)
    tris = m.vectors.astype(np.float64)
    pts = tris.reshape(-1, 3)
    mn, mx = pts.min(0), pts.max(0)
    cx, cy = (mn[0] + mx[0]) / 2, (mn[1] + mx[1]) / 2
    dz = bore_top_z - HEAD_CUT_Z
    return translate(tris, dx=-cx, dy=-cy, dz=dz)


def compact_flute(bore_len: float, head_path: str = HEAD,
                  outer_d: float = OUTER_D, bore_d: float = BORE_D) -> np.ndarray:
    """1本のコンパクト笛。閉端キャップ＋中空管＋ヘッド。z=0の閉端に立つ。"""
    cap = cylinder(outer_d, CAP_TH, z0=0.0)                      # 閉端（下）
    tube = annulus(outer_d / 2, bore_d / 2, bore_len - CAP_TH, z0=CAP_TH)  # 中空管
    head = _head_tris(head_path, bore_top_z=bore_len)            # ヘッド（上）
    # 管の上端とヘッドの底を少し重ねて確実に結合させる
    return np.concatenate([cap, tube, head])


def layout_row(flutes, pitch: float):
    out = []
    n = len(flutes)
    y0 = -(n - 1) * pitch / 2
    for i, f in enumerate(flutes):
        out.append(translate(f, dy=y0 + i * pitch))
    return np.concatenate(out)


def base_bar(n: int, pitch: float, width: float, thick: float = 3.0) -> np.ndarray:
    """笛列の下に敷く連結バー（印刷の安定と取り回しのため）。"""
    length = (n - 1) * pitch + width
    # z=-thick..0 の直方体を三角形で
    hx, hy = width / 2, length / 2
    x0, x1, y0, y1, z0, z1 = -hx, hx, -hy, hy, -thick, 0.0
    v = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
         (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
    q = [(0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]
    tris = []
    for a, b, c, d in q:
        tris.append([v[a], v[b], v[c]])
        tris.append([v[a], v[c], v[d]])
    return np.array(tris)


def calibration_comb(lengths, head_path: str = HEAD, outer_d: float = OUTER_D,
                     bore_d: float = BORE_D, gap: float = 3.0):
    """管長を段階的に変えた笛を一列に並べた較正用コーム。"""
    flutes = [compact_flute(L, head_path, outer_d, bore_d) for L in lengths]
    pitch = outer_d + gap
    row = layout_row(flutes, pitch)
    bar = base_bar(len(lengths), pitch, outer_d + 2.0)
    return np.concatenate([row, bar])


def main():
    ap = argparse.ArgumentParser(description="コンパクト音階笛ジェネレータと較正コーム")
    ap.add_argument("--comb", default="40,70,100,130",
                    help="較正コームの管長リスト(mm)。既定は4本（印刷時間短縮のため）。"
                         "3〜4本あれば管長と周波数の関係を直線近似できる")
    ap.add_argument("--single", type=float, default=None, help="単一笛の管長(mm)")
    ap.add_argument("--bore", type=float, default=BORE_D)
    ap.add_argument("--out", default=None)
    ap.add_argument("--no-3mf", action="store_true")
    args = ap.parse_args()

    if args.single is not None:
        asm = compact_flute(args.single, bore_d=args.bore)
        name = args.out or os.path.join(OUT, f"compact_L{args.single:.0f}.stl")
        label = f"単一笛 管長{args.single:.0f}mm（全長 {args.single+HEAD_LEN:.0f}mm）"
    else:
        lengths = [float(x) for x in args.comb.split(",")]
        asm = calibration_comb(lengths, bore_d=args.bore)
        name = args.out or os.path.join(OUT, "compact_calibration_comb.stl")
        label = f"較正コーム 管長={lengths}mm（{len(lengths)}本）"

    save(asm, name)
    mn, mx = bbox(asm)
    ok, oe = check_watertight(asm)
    print(label)
    print(f"外形寸法     : {np.round(mx-mn,1)} mm   三角形数={len(asm)}")
    print(f"保存先       : {name}")
    if not args.no_3mf:
        from make_3mf import stl_to_a1mini_3mf
        three = stl_to_a1mini_3mf(name)
        print(f"印刷用3mf    : {three}")


if __name__ == "__main__":
    main()
