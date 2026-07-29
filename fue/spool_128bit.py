"""128bitの秘密を、スプール2枚（2つの半体）へ分けて埋め込む。

1つの符号語を2枚に割るので、[* 両方そろわないと復元できない]。片方だけでは、
足りない記号が消失として大量に残り、誤り訂正の能力を大きく超える。金庫の鍵を
2箇所に置くのと同じ意味を、物のかたちで持たせられる。

符号化は12スロット（G#6〜G7）・隣接同音禁止・ブロック長10のRS符号である。
128bit（16バイト）は37記号になり、パリティ2記号／ブロック×5ブロックで48記号、
基準笛を含めて笛49本になる。1枚あたり25本と24本で、スプールに安全に入る本数（26本）の
内側に収まる。

基準笛は1枚目の先頭に1本だけ置く（吸込口の脇のタブで見分けられる）。復号器は
先頭の1本を基準として周波数比を取るので、[* 1枚目から順に、続けて2枚目を吹く]。

使い方:
    python3 fue/spool_128bit.py                      # 既定のデモ秘密で2枚を書き出す
    python3 fue/spool_128bit.py --payload 'text'     # 秘密を指定する（16バイト）
    python3 fue/spool_128bit.py --no-carve           # 彫り抜きなし（形の確認用・速い）
"""
from __future__ import annotations
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import cipher_codec as cd
import mini10
import orient_check
import spool_flutes

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)
OUT = os.path.join(ROOT, "out")
CONFIG = os.path.join(ROOT, "docs", "cipher", "cipher_config.json")

# デモと分かる固定の秘密。ちょうど16バイト＝128bitである。リポジトリは公開なので、
# 本番の秘密をここに書かないこと。
DEMO_PAYLOAD = b"CipherFlute-demo"

# 12スロット体系（G#6〜G7）。隣接同音禁止と組み合わせるのが本来の使い方。
SLOT12 = dict(lo_note="G#6", hi_note="G7")

# 1枚に安全に置ける本数。26本で隣どうしの隙間が1.25mm、27本で0.95mm、28本で0.66mm、
# 30本で接触する（笛の外形 65.97×7.00mm・リム半径100mmでの計算）。
MAX_PER_PLATE = 26

PLATES = [
    dict(key="3", name="プレート2（notch updated・厚さ40.7mm）"),
    dict(key="1", name="プレート1（sticker・厚さ34.1mm）"),
]


def build_config(parity=2):
    with open(CONFIG, encoding="utf-8") as fp:
        base = json.load(fp)
    return cd.CodecConfig(**{**base, **SLOT12, "ecc_parity": parity,
                            "mode": "sequential", "no_repeat": True})


def split_notes(notes, n_plates=2):
    """笛の並びを、枚数ぶんへ順に割る。前の枚が多くなるように分ける。"""
    per = -(-len(notes) // n_plates)
    return [notes[i:i + per] for i in range(0, len(notes), per)]


def main(argv=None):
    ap = argparse.ArgumentParser(description="128bitの秘密をスプール2枚へ分けて埋め込む")
    ap.add_argument("--payload", default=None, help="秘密（16バイトの文字列）。既定はデモ用の固定値")
    ap.add_argument("--parity", type=int, default=2, help="RSブロックあたりのパリティ記号数")
    ap.add_argument("--no-carve", action="store_true", help="彫り抜きなし（形の確認用）")
    ap.add_argument("--prefix", default="spool128", help="出力ファイル名の頭")
    ap.add_argument("--version", default=None,
                    help="版の名前（例 v4）。付けると out/spool128_v4_plate1.3mf のように書き出す。"
                         "試行錯誤の途中で前の版を上書きしないための決まりである")
    args = ap.parse_args(argv)

    payload = args.payload.encode() if args.payload else DEMO_PAYLOAD
    if len(payload) != 16:
        raise SystemExit("秘密は16バイト（128bit）でなければならない。いまは%dバイト。" % len(payload))

    cfg = build_config(args.parity)
    enc = cd.encode(payload, cfg)
    notes = list(enc.notes)      # 符号化器の戻り値は先頭が基準笛になっている
    plates = split_notes(notes, len(PLATES))
    print("秘密 %r（%dbit）" % (payload, len(payload) * 8))
    print("符号化: 12スロット・隣接同音禁止・パリティ%d記号/ブロック" % args.parity)
    print("笛は全部で%d本（基準笛1本＋データとパリティ%d本）" % (len(notes), len(notes) - 1))
    for i in range(len(notes) - 1):
        assert notes[i] != notes[i + 1], "隣り合う笛が同じ音になっている: %d本目" % (i + 1)
    for p, ns in zip(PLATES, plates):
        print("  %s … %d本" % (p["name"], len(ns)))
        if len(ns) > MAX_PER_PLATE:
            raise SystemExit("1枚あたり%d本は多すぎる（安全な上限は%d本）。" % (len(ns), MAX_PER_PLATE))

    # 外形長は全プレートで共通にする（外見から音が読めないようにするため）。
    l_max = mini10.uniform_body_length(
        [mini10.length_for_note(n) for n in mini10.CALIB12])
    print("笛の外形長 %.2fmm（12スロット全体の最長管＋余白）" % l_max)

    os.makedirs(OUT, exist_ok=True)
    for idx, (p, ns) in enumerate(zip(PLATES, plates)):
        sc, infos = spool_flutes.place_flutes_multiobj(
            ns, carve=not args.no_carve, geom_key=p["key"],
            ref_tab=(idx == 0), l_max=l_max)
        stem = args.prefix if not args.version else "%s_%s" % (args.prefix, args.version)
        path = os.path.join(OUT, "%s_plate%d.3mf" % (stem, idx + 1))
        if os.path.exists(path) and args.version:
            raise SystemExit("すでにある版を上書きしようとしている: %s（--version を新しくする）" % path)
        sc.export(path)
        print()
        print("%s -> %s" % (p["name"], os.path.relpath(path, ROOT)))
        print("  笛 %d本: %s" % (len(ns), " ".join(ns)))
        # 向きの検査。スプールは円盤の外面を下にして刷る前提で、笛は寝たまま円周に並ぶ。
        # 検証済みの範囲（横置き・窓が-135度から+135度）に入っているかを1本ずつ確かめる。
        results = [orient_check.check_orientation(R=it["R"]) for it in infos]
        bad = [(it["note"], r) for it, r in zip(infos, results) if r.verdict != "ok"]
        print("  向きの検査: %d本中%d本が ok（窓の角度 %.1f度・長軸の傾き %.1f度）"
              % (len(results), len(results) - len(bad),
                 results[0].angle_deg, results[0].tilt_deg))
        if bad:
            raise SystemExit("向きの検査に通らない笛がある: %s"
                             % ", ".join("%s(%s)" % (n, r.verdict) for n, r in bad[:5]))

    print()
    print("吹く順番: プレート2（基準笛のタブがある方）を1本目から順に、続けてプレート1。")
    print("片方だけでは復元できない（消失が多すぎて訂正能力を超えるため）。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
