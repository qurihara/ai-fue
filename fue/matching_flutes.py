"""照合笛：12個のスロットに対応する笛を1枚の板へ並べた、読み出し専用の物差し。

なぜ要るか
----------
較正コーム（12音を各3本、計36本）は**制作の側の道具**である。プリンタごとに管の長さと
音の高さを結ぶ係数を測るためのもので、同じ音を3本ずつ持つのは統計を取るためであった。
読み出しの側でこれを流用すると、目的の違う道具を再利用している形になる。

読み出しに要るのは別の物である。**12個のスロットに1本ずつ、どの笛がどのスロットかが
板の面を見れば分かること。** データの笛を吹き、この板の笛を順に吹いて、同じ高さになる
ものを探す。うなりが消えたところの番号がそのスロットである。電子機器はどこにも要らない。

設計
----
* 笛は**外形統一**（すべて同じ長さ）にする。長さで音を当てられないので、読み手は必ず
  刻んだ番号を見る。データ笛と同じ作りなので、造形の条件もそろう。
* 番号は各笛の足の先、板だけを貫通する抜き文字として刻む。笛のボア・窓・吸込口には
  掛からない位置に置く（掛かると鳴らなくなる）。
* 吹く側（吸込口）には何も置かない。口が触れる場所だからである。

使い方
    python3 fue/matching_flutes.py --out out/matching_flutes_v1.3mf
"""
from __future__ import annotations

import argparse
import os
import sys

import numpy as np
import trimesh
from shapely.geometry import MultiPolygon

sys.path.insert(0, os.path.dirname(__file__))
import mini10
import namecard as NC
import stencil

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)
OUT = os.path.join(ROOT, "out")

OVER = 0.3          # 隣り合う笛の重なり[mm]。カード実装と同じ
PLATE_Z = 0.5       # 板の厚み[mm]。笛の床と融合する
MARGIN = 1.0        # 笛の列の両脇に残す余白[mm]。板の縁を笛のすぐ際まで寄せる
BAND_GAP = 2.0      # 笛の足から番号までの距離[mm]
NUM_H = 4.5         # 番号の文字高さ[mm]
NUM_W = 7.0         # 番号に充てる帯の幅[mm]。2桁（10・11）が収まる分を取る
TAIL = 1.5          # 番号の先に残す余白[mm]
HEAD = 1.0          # 吸込口の側に残す余白[mm]
# 角丸の半径は余白と同じにする。こうすると角を丸める円弧の中心が笛の角と一致するので、
# **丸めても笛は1ミリも削られない**。半径を余白より大きくすると、両端の笛の吸込口や足が
# 欠ける。吸込口が欠けると鳴らないので、ここは値を変えるときに必ず確かめること。
CORNER_R = min(MARGIN, HEAD)


def _digits_poly(text, x_left, y_center):
    """番号を1つ、板の座標へ置いたポリゴンにする。x_leftは数字の左端、y_centerは笛の中心。

    ★字送りは笛の長軸(x)方向に取る★ 笛の並び(y)方向に字送りすると、2桁の「10」「11」の
    幅が約6mmになり、笛のピッチ6.7mmに対して隣の数字と接する。長軸方向なら帯の幅を
    好きに取れるので干渉しない。
    """
    poly, (w, th) = stencil.text_holes(text, height=NUM_H, bridge_w=1.0)
    return NC._translate2d(poly, xoff=x_left, yoff=y_center - th / 2.0)


def build(notes=None, label="CipherFlute"):
    """照合笛の板を作る。戻り値は (メッシュ, 情報の一覧)。

    ★音階の並べ方はこのプロジェクトの標準に従う★
    窓が+zに開き、吹き込み口を下へ揃えて水平に並べたとき、**右へ行くほど音が高い**。
    世の中の楽器（鍵盤・パンフルート・木琴）がそうなっているからで、読む人が並びを
    教わらなくても分かる。

    この板は、笛の長軸をxに寝かせ、笛をy方向に積む形で作る（数字の字送りを長軸方向に
    取れるので、2桁の番号が隣と干渉しない）。**吸込口のある左辺を下へ倒すように
    反時計回りへ90度回すと、上の標準の向きになる。** そのため板の上では
    y=上が最低音（スロット0）、y=下が最高音（スロット11）と、上下を裏返した順に積む。
    番号が上から0,1,…,11と並ぶので、回したときに左から0,1,…,11になる。
    """
    notes = list(notes or mini10.CALIB12)
    lengths = [mini10.length_for_note(n) for n in notes]
    l_max = mini10.uniform_body_length(lengths)

    width = trimesh.load(mini10.BASE).extents[1]        # 笛1本の幅 ≈ 7mm
    step = width - OVER
    n = len(notes)

    flutes, infos = [], []
    for i, (note, L) in enumerate(zip(notes, lengths)):
        y = MARGIN + (n - 1 - i) * step          # スロット0を上端に置く（反転して積む）
        f = mini10.uniform_flute(L, L_max=l_max)
        f.apply_translation([HEAD, y, 0])
        flutes.append(f)
        infos.append(dict(slot=i, note=note, L=round(L, 2),
                          freq=round(mini10.est_freq(L), 1),
                          y_center=round(y + width / 2.0, 2)))
    comb = trimesh.boolean.union(flutes, engine="manifold")
    comb.merge_vertices()

    cx = HEAD + l_max + BAND_GAP + NUM_W + TAIL
    cy = MARGIN * 2 + width + (n - 1) * step
    plate = trimesh.creation.box(extents=[cx, cy, PLATE_Z])
    plate.apply_translation([cx / 2, cy / 2, PLATE_Z / 2])
    board = trimesh.boolean.union([plate, comb], engine="manifold")

    keep = NC._corner_prism(cx, cy, CORNER_R, "round", -1.0, board.bounds[1][2] + 1.0)
    board = trimesh.boolean.intersection([board, keep], engine="manifold")

    # 番号。各笛の足の先に、その笛と同じ高さで置く。上から0,1,…,11と並ぶ。
    # ★笛の真下には何も抜かないこと★ 板は笛の床であり、抜けばボアに穴が開いて鳴らない。
    # 置いてよいのは笛の足より先（x > HEAD + l_max）と、笛の列の外の余白だけである。
    # 向きを示す印は要らない。番号そのものが順序と向きを示すからである。
    x_left = HEAD + l_max + BAND_GAP
    parts = []
    for info in infos:
        p = _digits_poly(str(info["slot"]), x_left, info["y_center"])
        if p is not None and not p.is_empty:
            parts.append(p)
    if parts:
        board = NC._apply_2d(board, MultiPolygon(
            [g for p in parts for g in (p.geoms if isinstance(p, MultiPolygon) else [p])]),
            PLATE_Z)
    return board, infos


def main(argv=None):
    ap = argparse.ArgumentParser(description="照合笛（読み出し用の物差し）を作る")
    ap.add_argument("--out", required=True, help="出力する3mfまたはstl（版を含む名前にする）")
    ap.add_argument("--label", default="CipherFlute", help="板に入れる表題")
    args = ap.parse_args(argv)

    if os.path.exists(args.out):
        raise SystemExit("すでにある版を上書きしようとしている: %s" % args.out)

    board, infos = build(label=args.label)
    os.makedirs(OUT, exist_ok=True)
    if args.out.endswith(".3mf"):
        trimesh.Scene({"matching_flutes_0.08careful": board}).export(args.out)
    else:
        board.export(args.out)

    print("照合笛 %.1f×%.1f×%.1fmm（笛%d本）-> %s"
          % (*np.round(board.extents, 1), len(infos), os.path.relpath(args.out, ROOT)))
    for info in infos:
        print("  スロット%2d  %-4s  管長%6.2fmm  %6.1fHz  板の上でのy中心%6.2fmm"
              % (info["slot"], info["note"], info["L"], info["freq"], info["y_center"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
