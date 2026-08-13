#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""刷った暗号笛の「実物・秘密・笛の並び・復号URL」を1つの表にまとめる。

なぜ要るか
----------
秘密は生成器の既定値、cosenseの記述、out/ の数点のテキストへ散らばっていて、
**どこにもまとまっていない**。実物が手元にあっても、何が入っていてどのURLで読めるのかを
毎回たどり直すことになる。かるた札のように、秘密も笛の並びもファイルに残っていない
ものもある。

★生成器を再実行しても、刷った物と同じにならないことがある★
--------------------------------------------------------
2-of-3 の分け方は `threshold.py` の乱数の使い方が変わったため、同じ種を渡しても
**当時と違う断片が出る**（実際に確かめた）。したがって刷った物の断片は、生成器では
なくこの表が正本である。2-of-2 の分け方は決め打ち（7のn乗）なので再現できる。

検証のしかた
------------
`--verify` を付けると、印刷ファイルそのものから笛の並びを読み直して表と突き合わせる。
やり方は物によって2つある。

* 3mfにオブジェクト名が残っているもの（スプールなど）… 名前から音名を読む。
* 名前が残っていないもの（かるた札など）… **STLを水平に切って空洞の長さを測り**、
  管長から音名を逆算する。切る高さは z=2.4mm、頭部のぶん12.00mmを足すと設計値に一致する。
  メッシュの体積は使えない（水密でないので、別の秘密でも同じ値が出る）。

使い方
    python3 scripts/cipher_registry.py             # 表を出す（Markdown）
    python3 scripts/cipher_registry.py --scrapbox  # cosense記法で出す
    python3 scripts/cipher_registry.py --verify    # 印刷ファイルと突き合わせる
"""
from __future__ import annotations

import argparse
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "fue"))

import cipher_codec as cd  # noqa: E402

BASE = "https://qurihara.github.io/ai-fue/cipher/"

# 音域は3世代ある。★隣接同音禁止（no_repeat）は途中から入れたので、
# 古い物は禁止していない★。ここを取り違えると復号器が「ブロック構成が不正」で止まる。
SLOT12 = dict(lo_note="G#6", hi_note="G7")     # 現行。隣接同音禁止あり
SLOT11 = dict(lo_note="G#6", hi_note="F#7")    # 初期のスプールと本立て。禁止なし
SLOT13 = dict(lo_note="F#6", hi_note="F#7")    # 最初の往復デモ。禁止なし


def cfg(slots, parity, mode="symbols", no_repeat=True):
    return cd.CodecConfig(reference_note="C7", no_repeat=no_repeat, use_reference=True,
                          ecc_parity=parity, mode=mode, **slots)


def url_of(c):
    """復号ページのURL。設定はフラグメント（#以降）に置くのでサーバへ送られない。"""
    p = ["lo=" + c.lo_note, "hi=" + c.hi_note]
    if c.no_repeat:
        p.append("norepeat=1")
    p += ["mode=" + c.mode, "parity=%d" % c.ecc_parity, "pitchsplit=1", "splitcents=80"]
    return BASE + "#" + "&".join(p)


def base_of(c):
    return cd._wire_params(c)[1]


def enc_symbols(symbols, c):
    return list(cd.encode_symbols(symbols, c).notes)


def enc_payload(payload: bytes, c):
    return list(cd.encode(payload, c).notes)


def split2(secret, base, n):
    """2-of-2。片方に決め打ちの値（7のn乗）、もう片方に（秘密−その値）を入れる。

    ★決め打ちなので、記号数が同じ物どうしは1枚目がまったく同じ並びになる★
    ハート札とかるた札は、どちらも6記号なので1枚目が同一である。取り違えると
    別の秘密が出てしまうので、実物には歌や絵で区別が付くようにしてある。
    """
    span = base ** n
    rnd = (7 ** n) % span
    return rnd % span, (secret - rnd) % span


def digits(v, base, n):
    out = []
    for _ in range(n):
        out.append(v % base)
        v //= base
    return out[::-1]


def pair_notes(secret, parity, n_flutes, slots=SLOT12):
    c = cfg(slots, parity)
    b = base_of(c)
    n = n_flutes - 1 - parity
    a, bb = split2(secret, b, n)
    return c, [enc_symbols(digits(a, b, n), c), enc_symbols(digits(bb, b, n), c)]


def build_rows():
    rows = []

    # ── A群 実機で吹いて復号まで通ったもの ────────────────────────
    c = cfg(SLOT13, 0, no_repeat=False)
    rows.append(dict(
        group="A", name="往復デモコーム（笛5本）",
        secret="2026", detail="記号列そのもの・パリティなし・13スロット（初代）",
        pieces=[("1枚", enc_symbols([2, 0, 2, 6], c))],
        url=url_of(c) + "&sha256=a9415803d7307e2b936e24cdf169cfa7691d7b4ac6e549c64f1d8becaef4df66",
        files="out/cipher_roundtrip_demo.stl",
        photo="—",
        checked="2026-07-23 実機で復号成功（照合子 a9415803… と一致）"))

    c, ns = pair_notes(260729, 1, 8)
    rows.append(dict(
        group="A", name="ハートのカード2枚",
        secret="260729", detail="2-of-2・11進6桁・笛8本ずつ",
        pieces=[("1枚目", ns[0]), ("2枚目", ns[1])],
        url=url_of(c),
        files="out/cipher_cardpair_v3.3mf",
        photo="ph_paircards.jpg",
        checked="2026-07-29 実機で2枚を吹いて復元成功"))

    c = cfg(SLOT12, 2)
    rows.append(dict(
        group="A", name="2-of-3 の三点（箱・カード・本立て）",
        secret="124816", detail="2-of-3・11進5桁・笛8本ずつ",
        pieces=[("断片1 箱", enc_symbols([6, 7, 1, 2, 1], c)),
                ("断片2 カード", enc_symbols([4, 9, 5, 10, 3], c)),
                ("断片3 本立て", enc_symbols([2, 0, 9, 7, 5], c))],
        url=url_of(c),
        files="out/cardbox_v1_share1.3mf ／ out/cipher_card_v4_share2.3mf ／ out/bookstand_v4_share3.3mf",
        photo="ph_2of3card.jpg ph_box_pens.jpg ph_bookstand.jpg",
        checked="2026-08-02 箱とカードの2つで復号成功"))

    c = cfg(SLOT12, 2, mode="sequential")
    rows.append(dict(
        group="A", name="スプール2枚（128ビット）",
        secret='"CipherFlute-demo"', detail="16バイト・笛49本（25本＋24本）",
        pieces=[("2枚を続けて", enc_payload(b"CipherFlute-demo", c))],
        url=url_of(c),
        files="out/spool128_plate1.3mf ／ out/spool128_plate2.3mf",
        photo="ph_spool.jpg",
        checked="2026-08-06 録音から復元成功（5通りすべて）"))

    c = cfg(SLOT12, 2)
    rows.append(dict(
        group="A", name="画像タイル9枚（北斎「神奈川沖浪裏」）",
        secret="314159", detail="2-of-9・11進6桁・1枚9本／計81本",
        pieces=[],
        url=url_of(c),
        files="fue/image_tiles.py --secret 314159（9枚ぶんを書き出す）",
        photo="ph_tiles_framed.jpg ph_tiles_back.jpg",
        checked="2026-08-06 2枚を吹いて復元成功"))

    # ── B群 秘密は入っているが、実機の復号は未確認 ────────────────
    c, ns = pair_notes(260812, 1, 8)
    rows.append(dict(
        group="A", name="かるた札2枚（崇徳院）",
        secret="260812", detail="2-of-2・11進6桁・笛8本ずつ",
        pieces=[("上の句の札", ns[0]), ("下の句の札", ns[1])],
        url=url_of(c),
        files="out/karuta/sutoku_both_h2d.gcode.3mf",
        photo="ph_karuta.jpg",
        checked="2026-08-13 実機で2枚を吹いて復元成功（印刷ファイルの空洞長とも一致）"))

    # 旧11スロットの物は隣接同音を禁じていない。禁止して読もうとすると復号器が止まる。
    c = cfg(SLOT11, 2, mode="sequential", no_repeat=False)
    rows.append(dict(
        group="B", name="スプール「pass_#26」",
        secret='"pass_#26"', detail="8バイト・笛26本・旧11スロット・隣接同音の禁止なし",
        pieces=[("1枚", enc_payload(b"pass_#26", c))],
        url=url_of(c),
        files="out/spool_pass26_petg_h2d.3mf",
        photo="—",
        checked="未確認（実物は手元にある）"))

    rows.append(dict(
        group="B", name="標準スプール26本",
        secret='"STANDARD"', detail="8バイト・笛26本・旧11スロット・隣接同音の禁止なし",
        pieces=[("1枚", enc_payload(b"STANDARD", c))],
        url=url_of(c),
        files="out/spool_standard_64bit_multiobj.3mf",
        photo="—",
        checked="印刷ファイルの笛の名前と一致（実機で吹く確認は未）"))

    rows.append(dict(
        group="B", name="本立て（pass_#26 版）",
        secret='"pass_#26"', detail="8バイト・旧11スロット・隣接同音の禁止なし",
        pieces=[("1台", enc_payload(b"pass_#26", c))],
        url=url_of(c),
        files="out/bookstand_pass26_v2.3mf",
        photo="ph_bookstand.jpg",
        checked="未確認（3mfに笛の名前が残っていない）"))

    rows.append(dict(
        group="B", name="カード「2026724」",
        secret="2026724", detail="初期のカード。符号の体系は特定できていない",
        pieces=[],
        url=url_of(c) + "　（素のURLでも読めたと記録にある）",
        files="（初期の版。3mfを特定できていない）",
        photo="—",
        checked="未確認（実物は手元にある）"))

    rows.append(dict(
        group="B", name="HeartBeads 2個",
        secret="3記号（約1バイト）", detail="2-of-2・GF(7)・1個あたり笛4本",
        pieces=[],
        url=BASE + "#lo=C7&hi=F#7&mode=symbols&parity=0&pitchsplit=1&splitcents=80",
        files="out/heartbeads_secret_share.3mf",
        photo="—",
        checked="未確認（かたわれ3本版のみ手元にある。休止中。秘密の値も残っていない）"))

    return rows


def fmt_notes(notes, limit=12):
    if not notes:
        return "—"
    if len(notes) <= limit:
        return " ".join(notes)
    return " ".join(notes[:limit]) + " …（全%d本）" % len(notes)


# ── 印刷ファイルとの突き合わせ ───────────────────────────────
def notes_from_3mf(path):
    """3mfのオブジェクト名から吹く順の音名を読む。名前が残っていなければ空を返す。"""
    import re
    import warnings
    warnings.filterwarnings("ignore")
    import trimesh
    scene = trimesh.load(path)
    found = {}
    for key in getattr(scene, "geometry", {}):
        m = re.match(r"flute(\d+)_([A-G]#?\d)", key)
        if m:
            found[int(m.group(1))] = m.group(2)
    return [found[i] for i in sorted(found)]


def notes_from_stl(path, z=2.4, head=12.00):
    """STLを水平に切って空洞の長さを測り、管長から音名を逆算する。

    ★体積は使えない★ 笛の空洞は開いていてメッシュが水密でないため、
    trimeshの体積は別の秘密でも同じ値を返す（実際に確かめた）。
    """
    import warnings
    warnings.filterwarnings("ignore")
    import trimesh
    import mini10
    names = ["G#6", "A6", "A#6", "B6", "C7", "C#7", "D7", "D#7", "E7", "F7", "F#7", "G7"]
    table = {n: mini10.length_for_note(n) for n in names}
    mesh = trimesh.load(path)
    section, _ = mesh.section(plane_origin=[0, 0, z], plane_normal=[0, 0, 1]).to_planar()
    lanes = {}
    for poly in section.polygons_full:
        xc = round((poly.bounds[0] + poly.bounds[2]) / 2)
        for hole in poly.interiors:
            ys = [c[1] for c in hole.coords]
            lanes[xc] = max(lanes.get(xc, 0), max(ys) - min(ys))
    out = []
    for xc in sorted(lanes):
        length = lanes[xc] + head
        out.append(min(names, key=lambda n: abs(table[n] - length)))
    return out


def verify():
    ok = True
    print("■ 印刷ファイルと突き合わせる")

    print("\n スプール2枚（128ビット）… 3mfのオブジェクト名から読む")
    notes = notes_from_3mf(os.path.join(ROOT, "out", "spool128_plate1.3mf")) + \
        notes_from_3mf(os.path.join(ROOT, "out", "spool128_plate2.3mf"))
    c = cfg(SLOT12, 2, mode="sequential")
    result = cd.decode([cd.note_to_freq(n) for n in notes], c)
    text = bytes(result.payload).decode("ascii", errors="replace")
    print("   笛%d本 → status=%s payload=%r" % (len(notes), result.status, text))
    ok &= (result.status == "ok" and text == "CipherFlute-demo")

    print("\n かるた札2枚… STLを切って空洞の長さから読む")
    _, expect = pair_notes(260812, 1, 8)
    for tag, want in (("upper", expect[0]), ("lower", expect[1])):
        path = os.path.join(ROOT, "out", "karuta", "sutoku_%s_base.stl" % tag)
        got = notes_from_stl(path)[::-1]      # 板は裏返して刷るので右から読む
        same = got == want
        ok &= same
        print("   %-6s %s  %s" % (tag, " ".join(got), "一致" if same else "食い違い"))

    print("\n 標準スプール26本… 3mfのオブジェクト名から読む")
    got = notes_from_3mf(os.path.join(ROOT, "out", "spool_standard_64bit_multiobj.3mf"))
    c = cfg(SLOT11, 2, mode="sequential", no_repeat=False)
    want = enc_payload(b"STANDARD", c)
    print("   %s" % ("一致" if got == want else "食い違い: %s" % " ".join(got)))
    ok &= (got == want)

    print("\n 往復デモコーム… 記録した音名と突き合わせる")
    c = cfg(SLOT13, 0, no_repeat=False)
    got = enc_symbols([2, 0, 2, 6], c)
    want = "C7 G#6 F#6 G#6 C7".split()          # out/cipher_roundtrip_demo_info.txt
    print("   %s → %s" % (" ".join(got), "一致" if got == want else "食い違い"))
    ok &= (got == want)

    print("\n" + ("すべて一致した" if ok else "★食い違いがある★"))
    return 0 if ok else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description="刷った暗号笛の実物・秘密・復号URLの一覧")
    ap.add_argument("--scrapbox", action="store_true", help="cosense記法で出す")
    ap.add_argument("--verify", action="store_true", help="印刷ファイルと突き合わせる")
    args = ap.parse_args(argv)

    if args.verify:
        return verify()

    for r in build_rows():
        if args.scrapbox:
            print(" [* %s]（%s群）" % (r["name"], r["group"]))
            print("  秘密 %s ／ %s" % (r["secret"], r["detail"]))
            for label, notes in r["pieces"]:
                print("  %s … %s" % (label, fmt_notes(notes)))
            # ★URLは素で書く★ バッククォートで囲むとcosenseがコードとして扱い、
            # 押せるリンクにならない。押せないと台帳として使えない。
            print("  %s" % r["url"])
            print("  ファイル %s" % r["files"])
            print("  確認 %s" % r["checked"])
        else:
            print("## %s（%s群）" % (r["name"], r["group"]))
            print("- 秘密: %s（%s）" % (r["secret"], r["detail"]))
            for label, notes in r["pieces"]:
                print("- %s: %s" % (label, fmt_notes(notes)))
            print("- URL: %s" % r["url"])
            print("- ファイル: %s" % r["files"])
            print("- 写真: %s" % r["photo"])
            print("- 確認: %s\n" % r["checked"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
