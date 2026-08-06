"""録音した笛の音から、音の並びを取り出す。

なぜ要るか
----------
復号ページはその場のマイクで読むが、うまくいかないときに何が起きていたのかを
あとから調べられない。録音があれば、区切り方やしきい値を変えて何度でも試せる。
ページと同じ考え方（帯域レベルで区切り、区間ごとに周波数の中央値を取る）で実装し、
結果をページの照合器へそのまま渡せる形で出す。

使い方:
    python3 scripts/analyze_recording.py temp/spool128/spool1_1.m4a
    python3 scripts/analyze_recording.py 録音.m4a --expect "C7 C#7 A6 ..." --ref C7
"""
from __future__ import annotations

import argparse
import json
import math
import os
import subprocess
import sys
import tempfile
import wave

import numpy as np

FFMPEG = "/opt/homebrew/bin/ffmpeg"


def to_wav(path, sr=44100):
    """ffmpeg で単声のwavに直す。"""
    out = os.path.join(tempfile.mkdtemp(), "a.wav")
    subprocess.run([FFMPEG, "-v", "error", "-y", "-i", path,
                    "-ac", "1", "-ar", str(sr), out], check=True)
    return out


def read_wav(path):
    with wave.open(path, "rb") as w:
        sr = w.getframerate()
        n = w.getnframes()
        raw = w.readframes(n)
    x = np.frombuffer(raw, dtype=np.int16).astype(np.float64) / 32768.0
    return x, sr


def spectrum_track(x, sr, lo_hz, hi_hz, win=4096, hop=512):
    """窓ごとに、笛の音域の中でいちばん強い山とその強さを返す。

    [* 音域の外は見ない]。話し声や空調は低い方に、擦れる音は高い方に出るので、
    見る範囲を絞るだけで雑音がかなり落ちる。
    """
    w = np.hanning(win)
    freqs = np.fft.rfftfreq(win, 1.0 / sr)
    band = (freqs >= lo_hz) & (freqs <= hi_hz)
    fb = freqs[band]
    times, peaks, levels = [], [], []
    for i in range(0, len(x) - win, hop):
        seg = x[i:i + win] * w
        sp = np.abs(np.fft.rfft(seg))[band]
        k = int(np.argmax(sp))
        # 山の頂点を、両隣を使った放物線で補間する（分解能より細かく読む）
        if 0 < k < len(sp) - 1 and sp[k] > 0:
            a, b, c = sp[k - 1], sp[k], sp[k + 1]
            d = (a - c) / (2 * (a - 2 * b + c)) if (a - 2 * b + c) != 0 else 0.0
            f = fb[k] + d * (fb[1] - fb[0])
        else:
            f = fb[k]
        times.append(i / sr * 1000.0)
        peaks.append(f)
        levels.append(20 * math.log10(sp[k] + 1e-12))
    return np.array(times), np.array(peaks), np.array(levels)


def segment(times, peaks, levels, on_db, gap_ms=120, min_ms=90, attack_ms=40,
            split_cents=80.0, stable_ms=70.0):
    """音を切り分ける。無音だけでなく[* 音程が変わったところでも切る]。

    息を切らずに続けて吹くと、音は途切れないまま高さだけが変わる。レベルだけを見ていると
    そこが1つの長い音になってしまう（実際に12秒の音が1つ、という読み方になった）。
    隣り合う笛は必ず違う音になる符号（隣接同音禁止）なので、音程の変わり目は
    そのまま笛の変わり目である。
    """
    on = levels >= on_db
    notes = []
    i, n = 0, len(on)

    def commit(a, b):
        """[a,b] の区間を1本として確定する。"""
        t0, t1 = times[a], times[b]
        if t1 - t0 < min_ms:
            return
        sel = np.zeros(n, dtype=bool)
        sel[a:b + 1] = True
        sel &= on & (times >= t0 + min(attack_ms, (t1 - t0) * 0.3))
        if sel.sum() < 2:
            return
        notes.append(dict(startMs=float(t0), durationMs=float(t1 - t0),
                          freq=float(np.median(peaks[sel])),
                          level=float(np.median(levels[sel]))))

    while i < n:
        if not on[i]:
            i += 1
            continue
        start = i
        last = i
        ref = None           # いまの音の高さ（安定してから決める）
        drift_from = None    # 離れ始めた位置
        j = i
        while j < n:
            if on[j]:
                last = j
                if times[j] - times[start] >= attack_ms:
                    if ref is None:
                        ref = peaks[j]
                    else:
                        cents = 1200 * math.log2(peaks[j] / ref) if peaks[j] > 0 else 0.0
                        if abs(cents) > split_cents:
                            if drift_from is None:
                                drift_from = j
                            elif times[j] - times[drift_from] >= stable_ms:
                                # 新しい高さが続いた。ここで切って、次の音を始める
                                commit(start, drift_from - 1)
                                start = drift_from
                                ref = peaks[j]
                                drift_from = None
                        else:
                            drift_from = None
            elif times[j] - times[last] > gap_ms:
                break
            j += 1
        commit(start, last)
        i = last + 1
    return notes


def main(argv=None):
    ap = argparse.ArgumentParser(description="録音から笛の音の並びを取り出す")
    ap.add_argument("audio")
    ap.add_argument("--lo", type=float, default=1500.0, help="見る音域の下[Hz]")
    ap.add_argument("--hi", type=float, default=3400.0, help="見る音域の上[Hz]")
    ap.add_argument("--on-margin", type=float, default=18.0,
                    help="暗騒音からこれだけ上なら鳴っているとみなす[dB]")
    ap.add_argument("--gap", type=float, default=120.0, help="この無音で区切る[ms]")
    ap.add_argument("--min", type=float, default=90.0, help="これより短い音は捨てる[ms]")
    ap.add_argument("--split-cents", type=float, default=80.0,
                    help="この幅より音程が動いたら別の笛とみなす[セント]")
    ap.add_argument("--json", default=None, help="結果をJSONで書き出す")
    args = ap.parse_args(argv)

    x, sr = read_wav(to_wav(args.audio))
    t, p, l = spectrum_track(x, sr, args.lo, args.hi)
    noise = float(np.percentile(l, 20))          # 静かな側の2割を暗騒音とみなす
    on_db = noise + args.on_margin
    notes = segment(t, p, l, on_db, args.gap, args.min, split_cents=args.split_cents)

    print("%s … %.1f秒、暗騒音 %.1fdB、しきい値 %.1fdB"
          % (os.path.basename(args.audio), len(x) / sr, noise, on_db))
    print("音の数 %d" % len(notes))
    gaps = [notes[i + 1]["startMs"] - notes[i]["startMs"] for i in range(len(notes) - 1)]
    if gaps:
        print("間隔の中央値 %.0fms（最小 %.0f・最大 %.0f）"
              % (float(np.median(gaps)), min(gaps), max(gaps)))
    for i, nt in enumerate(notes):
        print("  %2d  %7.1fHz  %5.0fms  開始%7.0fms  %.1fdB"
              % (i + 1, nt["freq"], nt["durationMs"], nt["startMs"], nt["level"]))
    if args.json:
        with open(args.json, "w", encoding="utf-8") as fp:
            json.dump(notes, fp, ensure_ascii=False, indent=1)
        print("-> %s" % args.json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
