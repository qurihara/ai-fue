#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""実演の録画から音を取り出し、台帳どおりの秘密が戻るかを確かめる。

なにをするか
------------
temp/tools/videos に置いた実演の動画それぞれについて、
音声を解析して笛の並びを取り出し、`cipher_registry.py` に記録した構成で復号する。

★短い音と小さい音は落とす★
--------------------------
解析器（scripts/analyze_recording.py）にはテンポの判定が無いので、吹き終わりの
揺れや物音が余分な音として出る。実際、箱では13音、北斎では103音が拾われた
（設計はそれぞれ8音と81音）。落とす条件は次の2つで、どちらも実測から決めた。

  * 長さが MIN_MS 未満  … 本物の音は250〜700msある。雑音は90〜100msで出た
  * 大きさが最大から DROP_DB 以上小さい … 雑音は本物より20〜40dB低かった

使い方
    python3 scripts/decode_videos.py                 # 全部
    python3 scripts/decode_videos.py --only spool    # 名前で選ぶ
    python3 scripts/decode_videos.py --raw           # 落とす前の音も全部見せる
"""
from __future__ import annotations

import argparse
import itertools
import json
import os
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "fue"))

import cipher_codec as cd   # noqa: E402
import threshold as th      # noqa: E402

VIDEOS = os.path.join(ROOT, "temp", "tools", "videos")
FFMPEG = "/opt/homebrew/bin/ffmpeg"

MIN_MS = 150.0       # これより短い音は雑音とみなす
DROP_DB = 18.0       # いちばん大きい音からこれ以上小さければ雑音とみなす


def cfg(lo, hi, parity, mode="symbols", no_repeat=True):
    return cd.CodecConfig(lo_note=lo, hi_note=hi, reference_note="C7",
                          no_repeat=no_repeat, use_reference=True,
                          ecc_parity=parity, mode=mode)


# 台帳（cosense「暗号笛の実物・秘密・復号URL一覧」）と同じ構成を書く。
CASES = [
    dict(name="card_2026724", label="カード「2026724」",
         cfg=cfg("G#6", "F#7", 0, no_repeat=False), per=8, parts=1,
         kind="symbols", expect=[2, 0, 2, 6, 7, 2, 4]),
    dict(name="card_2of3", label="2-of-3 カード（断片2）",
         cfg=cfg("G#6", "G7", 2), per=8, parts=1,
         kind="symbols", expect=[4, 9, 5, 10, 3]),
    dict(name="box_2of3", label="2-of-3 箱（断片1）",
         cfg=cfg("G#6", "G7", 2), per=8, parts=1,
         kind="symbols", expect=[6, 7, 1, 2, 1]),
    dict(name="bookstand_2of3", label="2-of-3 本立て（断片3）",
         cfg=cfg("G#6", "G7", 2), per=8, parts=1,
         kind="symbols", expect=[2, 0, 9, 7, 5]),
    # ★取り直した版を使う★ 最初の録画は1枚目の4本目（B6）が鳴っておらず、
    # パリティ1では途中の欠落を直せないため復号できなかった。
    dict(name="heart_cards_2of2_take2", label="ハートのカード2枚（2-of-2・取り直し）",
         cfg=cfg("G#6", "G7", 1), per=8, parts=2,
         kind="sum", expect=260729),
    dict(name="karuta_sutokuin_2of2", label="かるた札2枚（2-of-2）",
         cfg=cfg("G#6", "G7", 1), per=8, parts=2,
         kind="sum", expect=260812),
    dict(name="hokusai_2of9", label="北斎の画像タイル9枚（2-of-9）",
         cfg=cfg("G#6", "G7", 2), per=9, parts=9,
         kind="threshold", expect=314159),
    dict(name="spool", label="スプール2枚（128ビット）",
         cfg=cfg("G#6", "G7", 2, mode="sequential"), per=49, parts=1,
         kind="payload", expect=b"CipherFlute-demo"),
    dict(name="scale_12", label="照合笛（12本の音階）",
         cfg=cfg("G#6", "G7", 0), per=12, parts=1,
         kind="scale", expect=None),
]


def segments_of(path, keep_all=False):
    """動画から音を取り出し、雑音を落とした区間の一覧を返す。"""
    with tempfile.TemporaryDirectory() as tmp:
        wav = os.path.join(tmp, "a.wav")
        subprocess.run([FFMPEG, "-v", "error", "-i", path, "-ac", "1",
                        "-ar", "48000", "-y", wav], check=True)
        js = os.path.join(tmp, "a.json")
        subprocess.run([sys.executable,
                        os.path.join(ROOT, "scripts", "analyze_recording.py"),
                        wav, "--json", js],
                       check=True, stdout=subprocess.DEVNULL)
        data = json.load(open(js))
    segs = data["segments"] if isinstance(data, dict) else data
    if keep_all or not segs:
        return segs, segs
    top = max(s.get("db", 0.0) for s in segs)
    kept = [s for s in segs
            if s.get("durationMs", 0) >= MIN_MS and s.get("db", 0.0) >= top - DROP_DB]
    return segs, kept


def prepare(path, want, keep_all=False):
    """雑音を落とし、多すぎるときは本番の並びだけに絞る。"""
    allsegs, kept = segments_of(path, keep_all=keep_all)
    return allsegs, tightest_run(kept, want)


def tightest_run(segs, want):
    """欲しい本数ぶんの、いちばん詰まっている連続した並びを選ぶ。

    ★吹く前の試し吹きや、吹き終わったあとの物音が混ざる★ 実際、箱の録画では
    本番の10音の前に3つ、離れた場所に音が拾われていた。本番は一定の拍で続けて
    吹くので、同じ本数を取るなら時間の幅がいちばん狭い並びが本番である。
    """
    if want <= 0 or len(segs) <= want:
        return segs
    best, span = 0, None
    for i in range(len(segs) - want + 1):
        w = segs[i:i + want]
        d = (w[-1]["startMs"] + w[-1]["durationMs"]) - w[0]["startMs"]
        if span is None or d < span:
            best, span = i, d
    return segs[best:best + want]


def split_by_gaps(segs, parts):
    """吹く物が変わるときの長い間で、録音を parts 個の組に切る。

    ★本数で機械的に割ってはいけない★ 1枚でも余分に拾えば以降が全部ずれる。
    実際、北斎の9枚は本数割りだと3枚しか復号できなかった。持ち替えの間は
    笛と笛の間よりはっきり長いので、そこで切るほうが確実である。
    """
    if parts <= 1 or len(segs) < parts:
        return [segs]
    gaps = []
    for i in range(1, len(segs)):
        prev = segs[i - 1]
        g = segs[i]["startMs"] - (prev["startMs"] + prev["durationMs"])
        gaps.append((g, i))
    cuts = sorted(i for _, i in sorted(gaps, reverse=True)[:parts - 1])
    out, prev = [], 0
    for cidx in cuts + [len(segs)]:
        out.append(segs[prev:cidx])
        prev = cidx
    return out


def repair_decode(freqs, c, want, check):
    """本数が足りないとき、鳴らなかった1本を探して「飛ばし」を入れて復号し直す。

    ★実演では1本が拾えないことがある★ スプールの録画がそうで、4本目が拾えず
    以降が1つずつずれていた（末尾には余分な吹きが1つあった）。どの位置が欠けたかは
    分からないので、順に「飛ばし」を入れて試す。パリティが1本ぶんを直せるので、
    当たりの位置では復号が通る。
    """
    r = decode_notes(freqs[:want], c)
    if check(r):
        return r, "そのまま"
    ph = freqs[0] * (2 ** (3.5 / 12.0))   # どのスロットからも遠い値＝鳴らなかった印
    guard = cd.CodecConfig(**{**c.__dict__, "decision_guard_cents": 25.0})
    for k in range(1, min(len(freqs), want)):
        trial = freqs[:k] + [ph] + freqs[k:want - 1]
        r = decode_notes(trial, guard)
        if check(r):
            return r, "%d本目が鳴らなかったものとして復号" % (k + 1)
    return decode_notes(freqs[:want], c), "直せなかった"


def decode_notes(freqs, c):
    try:
        return cd.decode(freqs, c)
    except Exception as e:                       # 本数が合わない等はここに来る
        return type("R", (), {"status": "error: " + str(e)[:60], "symbols": [],
                              "payload": None})()


def run_case(case, raw=False):
    path = os.path.join(VIDEOS, case["name"] + ".TS.mp4")
    if not os.path.exists(path):
        print("  ★動画が無い★ %s" % path)
        return False
    want = case["per"] * case["parts"]
    if case["kind"] in ("threshold", "sum"):
        allsegs, segs = segments_of(path, keep_all=raw)   # 組ごとに絞るのであとで
        segs = [x for x in segs if x.get("durationMs", 0) >= MIN_MS]
    else:
        allsegs, segs = prepare(path, want, keep_all=raw)
    freqs = [s["freq"] for s in segs]
    print("  拾った音 %d（雑音を落とす前 %d）／設計 %d"
          % (len(segs), len(allsegs), want))
    if len(segs) != want:
        print("  ※本数が合わないので、そのまま復号すると崩れる")

    c, kind = case["cfg"], case["kind"]
    ok = False
    if kind == "scale":
        names = [cd.midi_to_note(round(cd.note_to_midi("C7")
                                       + 12 * __import__("math").log2(f / cd.note_to_freq("C7"))))
                 for f in freqs]
        print("  音名 %s" % " ".join(names))
        ok = True
    elif kind == "payload":
        def good(r):
            return getattr(r, "payload", None) and bytes(r.payload) == case["expect"]
        r, how = repair_decode(freqs, c, want, good)
        got = bytes(r.payload) if getattr(r, "payload", None) else b""
        ok = good(r)
        print("  status=%s payload=%r（%s）→ %s"
              % (r.status, got, how, "一致" if ok else "食い違い"))
    elif kind == "symbols":
        r = decode_notes(freqs[:case["per"]], c)
        ok = (r.status.startswith("ok") or r.status.startswith("corrected")) \
            and list(r.symbols) == case["expect"]
        print("  status=%s 記号 %s  期待 %s → %s"
              % (r.status, list(r.symbols), case["expect"], "一致" if ok else "食い違い"))
    elif kind == "sum":
        groups = [tightest_run(g, case["per"])
                  for g in split_by_gaps(segs, case["parts"])]
        syms = []
        for i, g in enumerate(groups):
            fr = [x["freq"] for x in g]
            # 記号が正しい本数そろうことを手がかりに、鳴らなかった1本を探す
            need = case["per"] - 1 - c.ecc_parity
            good = (lambda rr: (not rr.status.startswith("error")
                                and len(rr.symbols) == need))
            r, how = repair_decode(fr, c, case["per"], good)
            if not good(r):
                # ★2枚組の札は、片方が逆向きに吹かれることがある★
                # 2枚は余白どうしを向かい合わせに並べてあるので、それぞれの
                # ストラップ側から吹くと、板の上では逆の順になる。
                r2, how2 = repair_decode(list(reversed(fr)), c, case["per"], good)
                if good(r2):
                    r, how = r2, "逆向きに吹かれている（" + how2 + "）"
            print("    %d枚目 %d音（%s）" % (i + 1, len(g), how), end=" ")
            print("    %d枚目 status=%s 記号 %s" % (i + 1, r.status, list(r.symbols)))
            syms.append(list(r.symbols))
        if all(syms) and all(len(s) == len(syms[0]) for s in syms):
            # ★断片は整数として足す★ 桁ごとに足して余りを取ると繰り上がりが落ちて
            # 別の値になる。分けるときも (秘密 − 乱数) を整数で計算している。
            base = cd._wire_params(c)[1]
            span = base ** len(syms[0])
            def _val(ds):
                v = 0
                for d in ds:
                    v = v * base + d
                return v
            v = sum(_val(s) for s in syms) % span
            ok = (v == case["expect"])
            print("  合わせた秘密 %d  期待 %d → %s" % (v, case["expect"], "一致" if ok else "食い違い"))
    elif kind == "threshold":
        tiles = [tightest_run(t, case["per"])
                 for t in split_by_gaps(segs, case["parts"])]
        shares = []
        for i, t in enumerate(tiles):
            r = decode_notes([x["freq"] for x in t], c)
            print("    タイル%d %d音 status=%s 記号 %s"
                  % (i + 1, len(t), r.status, list(r.symbols)))
            if r.symbols and not r.status.startswith("error"):
                shares.append((i + 1, list(r.symbols)))
        hits = []
        for a, b in itertools.combinations(shares, 2):
            try:
                if th.value_of(th.combine([a, b])) == case["expect"]:
                    hits.append((a[0], b[0]))
            except Exception:
                pass
        if hits:
            ok = True
            print("  %d通りの組で %d が戻った: %s"
                  % (len(hits), case["expect"],
                     " / ".join("%dと%d" % h for h in hits)))
        if not ok:
            print("  どの2枚の組でも %d は戻らなかった" % case["expect"])
    return ok


def main(argv=None):
    ap = argparse.ArgumentParser(description="実演の録画から復号できるかを確かめる")
    ap.add_argument("--only", default=None, help="この名前を含むものだけ")
    ap.add_argument("--raw", action="store_true", help="雑音を落とさずに全部使う")
    args = ap.parse_args(argv)

    results = []
    for case in CASES:
        if args.only and args.only not in case["name"]:
            continue
        print("───── %s（%s）" % (case["label"], case["name"]))
        results.append((case["label"], run_case(case, raw=args.raw)))
        print()
    print("■ まとめ")
    for label, ok in results:
        print("  %-34s %s" % (label, "復号できた" if ok else "できていない"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
