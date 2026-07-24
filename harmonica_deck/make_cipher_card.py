"""CipherFluteの暗号カード（クレジットカードサイズ）を作る。

Chordika（make_chordika_mini10.build_card）のカード物理設計を流用しつつ、和音の度数連鎖ではなく
cipher_codec が生成する「基準笛1本＋データ笛」の音列をそのまま8本並べる。
既定は11音体系（G#6..F#7・GF(11)）で、数字列（例 今日の日付 2026724）を各データ笛に割り当てる。

- カード寸法・厚み・角丸・ボア無傷の条件は Chordika と同じ（CX,CY,CZ=85.6,53.98,0.5、総厚4mm）。
- 音名→管長は cipher 用較正を読む mini10.length_for_note（f=A/(L+e), A=88811.7, e=-8.612）。
- 先頭（index 0）が基準笛。その足先に ＊ を刻み、基準笛だと分かるようにする。
- 復号はスマホの復号ページ（11音デフォルト・symbols・基準あり）で、吹くと数字列がそのまま出る。

使い方:
  python3 harmonica_deck/make_cipher_card.py --digits 2026724 --out out/cipher_card_2026724.stl
"""
import argparse
import os
import sys
import numpy as np
import trimesh
from shapely.geometry import Point, Polygon

HERE = os.path.dirname(__file__)
ROOT = os.path.join(HERE, os.pardir)
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(ROOT, "fue"))
sys.path.insert(0, HERE)
import mini10                       # cipher 較正を読む length_for_note
import cipher_codec as cc
import make_chordika_mini10 as CH   # _flute / _cut_plate / CX,CY,CZ,OVER を流用
import namecard as NC
import stencil


def build_cipher_card(notes, label=None, mark_index=0, asterisk_r=2.6, reverse=True):
    """基準笛先頭の音名列 notes（8本想定）をクレカ大カードに融合して返す。
    全笛を外見統一版(uniform_flute)にし、外形を最長管に揃えて長さから音が読めないようにする。
    mark_index の笛（既定=基準笛）の足先に ＊ を刻む（半径 asterisk_r）。
    reverse=True なら並びを反転（カードを左から右へ吹くと基準→データの順になる）。
    label があれば足側にステンシル。"""
    L_max = max(mini10.length_for_note(n) for n in notes)   # 外形＝最長管に統一
    W = mini10.uniform_flute(L_max, L_max=L_max).extents[1]  # パイプ幅 ≈7
    step = W - CH.OVER
    order = list(range(len(notes)))
    if reverse:
        order = order[::-1]
    ms, y, feet = [], 0.0, [None] * len(notes)
    for oi in order:
        L = mini10.length_for_note(notes[oi])   # 内部壁でボア長=音を決める（外形はL_max一定）
        f = mini10.uniform_flute(L, L_max=L_max)
        f.apply_translation([0, y, 0])
        ms.append(f)
        feet[oi] = (y, L_max)                    # 足先は全笛 L_max（外見統一）
        y += step
    comb = trimesh.boolean.union(ms, engine="manifold")
    comb.merge_vertices()
    cw = comb.extents[1]
    yshift = (CH.CY - cw) / 2.0
    comb.apply_translation([0, yshift, 0])      # 積まない(z=0..4)＝プレート融合で総厚4mm

    plate = trimesh.creation.box(extents=[CH.CX, CH.CY, CH.CZ])
    plate.apply_translation([CH.CX / 2, CH.CY / 2, CH.CZ / 2])
    card = trimesh.boolean.union([plate, comb], engine="manifold")
    keep = NC._corner_prism(CH.CX, CH.CY, 2.0, "round", -1.0, comb.bounds[1][2] + 1.0)
    card = trimesh.boolean.intersection([card, keep], engine="manifold")

    # 基準笛（mark_index）の足先に ＊（はっきり見えるよう大きめ）
    yr, Lc = feet[mark_index]
    scx = Lc + 2.0 + asterisk_r
    scy = yr + yshift + W / 2.0
    card = CH._cut_plate(card, stencil.asterisk(scx, scy, asterisk_r))

    # 任意ラベル（足側の余白帯にy方向読み）。データを露出したくないときは None。
    if label:
        fx = max(f[1] for f in feet)
        bx0, bx1 = fx + 2.0, CH.CX - 3.0
        h = min(5.0, bx1 - bx0 - 1.0)
        xc = (bx0 + bx1) / 2
        pl, _ = NC._text_line(label, xc, h, CH.CY)
        if pl is not None and not pl.is_empty:
            card = CH._cut_plate(card, pl)

    # ストラップ穴（貫通）
    sr = 3.0
    circ = Point(CH.CX - (sr + 3.0), CH.CY - (sr + 3.0)).buffer(sr, resolution=48)
    pr = trimesh.creation.extrude_polygon(circ, height=comb.bounds[1][2] + 2.0)
    pr.apply_translation([0, 0, -1.0])
    card = trimesh.boolean.difference([card, pr], engine="manifold")

    card.apply_translation([0, 0, -card.bounds[0][2]])
    # ボア無傷チェック（x=30断面のボア穴面積が素の笛=9.808と一致するか）
    s = card.section(plane_origin=[30, 0, 0], plane_normal=[1, 0, 0])
    pl2, _ = s.to_planar()
    areas = set(round(abs(Polygon(r).area), 3) for p in pl2.polygons_full for r in p.interiors)
    return card, areas


def main(argv=None):
    ap = argparse.ArgumentParser(description="CipherFlute暗号カード（クレカ大・基準1＋データN）")
    ap.add_argument("--digits", default="2026724", help="各データ笛に割り当てる数字列（0..10、既定=今日の日付）")
    ap.add_argument("--lo", default="G#6", help="音域下端（11音体系はG#6）")
    ap.add_argument("--hi", default="F#7")
    ap.add_argument("--ref", default="C7", help="基準笛の音")
    ap.add_argument("--parity", type=int, default=0, help="RSパリティ本数（カジュアルは0）")
    ap.add_argument("--label", default=None, help="足側に刻むラベル（省略時は刻まない＝データ非露出）")
    ap.add_argument("--out", default=os.path.join(OUT, "cipher_card.stl"))
    args = ap.parse_args(argv)

    digits = [int(c) for c in args.digits]
    cfg = cc.CodecConfig(lo_note=args.lo, hi_note=args.hi, reference_note=args.ref,
                         ecc_parity=args.parity, mode="symbols")
    m = len(cc.slots(cfg))
    if any(not 0 <= d < m for d in digits):
        raise SystemExit("数字が体系の範囲外（0..%d）" % (m - 1))
    enc = cc.encode_symbols(digits, cfg)
    card, areas = build_cipher_card(enc.notes, label=args.label, mark_index=0)

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    card.export(args.out)
    # 往復確認
    freqs = [mini10.est_freq(mini10.length_for_note(n)) for n in enc.notes]
    dec = cc.decode(freqs, cfg)
    print("数字列 %s（%d桁）＝基準笛1＋データ%d＝%d本" % (args.digits, len(digits), len(digits), len(enc.notes)))
    print("音列(先頭=基準):", ",".join(enc.notes))
    print("管長mm:", ",".join("%.1f" % mini10.length_for_note(n) for n in enc.notes))
    print("カード ext=%s watertight=%s ボア穴=%s(素9.808)" %
          (np.round(card.extents, 1).tolist(), card.is_watertight, areas))
    print("往復復号 status=%s symbols=%s" % (dec.status, dec.symbols))
    print("-> %s" % os.path.relpath(args.out, ROOT))


if __name__ == "__main__":
    main()
