#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""実演の映像に、復号画面の録画を子画面（PinP）として重ねる。

なにをするか
------------
`record_decoder.py` で撮った復号画面を、実演の映像の右下へ小さく置く。
音声は実演のものをそのまま使う（復号画面の録画に音は入っていない）。

★時間の合わせ方★
----------------
復号画面の録画は「開始を押す→0.9秒待つ→音を流す」という段取りなので、
録画の先頭と実演の音の先頭がずれている。record_decoder.py が書き出した
`.marks.json` に、各コマが実演の音の何秒目にあたるかが入っているので、
音が0秒を過ぎた最初のコマを起点にして切り出す。

使い方
    python3 scripts/pinp_compose.py --base <実演.mp4> --pinp out/pinp/demo_2of2.mp4 \\
        --out out/pinp/demo_2of2_composed.mp4
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys


def audio_start_offset(marks_path):
    """復号画面の録画の中で、実演の音が鳴り始めた時刻[秒]を返す。"""
    if not os.path.exists(marks_path):
        return 0.0
    d = json.load(open(marks_path))
    for m in d.get("marks", []):
        if m.get("audio", 0) > 0.05:
            # そのコマの1つ前が「まだ鳴っていない」ので、間を取る
            return max(0.0, m["wall"] - m["audio"])
    return 0.0


def first_note_offset(marks_path):
    """★1本目の音名が出るまでの時間[秒]★ 子画面はここから出す。

    これより前から出すと、まだ何も描かれていない枠が黒い箱として映る
    （v9 で5つの場面がそうなった）。
    """
    if not os.path.exists(marks_path):
        return None
    d = json.load(open(marks_path))
    if d.get("firstNoteWall") is not None:
        return float(d["firstNoteWall"])
    for m in d.get("marks", []):
        if m.get("idle") is False:
            return float(m["wall"])
    return None


def blow_span(path, pad_head=0.6, pad_tail=1.2):
    """笛の音が鳴っている範囲[秒]を返す。子画面を出す区間を決めるために使う。

    ★吹く前後は子画面を出さない★ 出しっぱなしにすると、物音を拾って音名が増えたり、
    まだ何も吹いていないのに枠だけが浮いていたりして、見ている人を惑わせる。
    """
    import wave, tempfile, math
    import numpy as np
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as t:
        wav = t.name
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", path, "-ac", "1",
                    "-ar", "22050", wav], check=True)
    w = wave.open(wav); sr = w.getframerate()
    a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float)
    w.close(); os.unlink(wav)
    win = int(sr * 0.1)
    times = []
    for i in range(0, len(a) - win, win // 2):
        seg = a[i:i + win] * np.hanning(win)
        sp = np.abs(np.fft.rfft(seg)); fr = np.fft.rfftfreq(win, 1 / sr)
        tot = sp.sum() + 1e-9
        band = sp[(fr > 1600) & (fr < 3200)].sum()
        if band / tot > 0.25 and tot > 3e4:
            times.append(i / sr)
    if not times:
        return None
    return max(0.0, times[0] - pad_head), times[-1] + pad_tail


def compose(base, pinp, out, width_ratio, margin, corner, span, delay=0.0):
    marks = os.path.splitext(pinp)[0] + ".marks.json"
    off = audio_start_offset(marks)
    # 子画面の置き場所。右下が既定。実演は人物が中央に写るので隅が邪魔にならない。
    pos = {
        "右下": f"W-w-{margin}:H-h-{margin}",
        "左下": f"{margin}:H-h-{margin}",
        "右上": f"W-w-{margin}:{margin}",
        "左上": f"{margin}:{margin}",
    }[corner]
    # 子画面は角を丸めず、白い細枠を付けて実演と切り分ける。
    enable = ""
    if span:
        enable = f":enable='between(t,{span[0]:.2f},{span[1]:.2f})'"
    # 子画面を親のどの時刻から重ねるか。1本の映像に独立した吹奏が2回あるときは、
    # 見せたい吹奏の頭に合わせる（ハートとかるたを1本にした素材で必要になった）。
    # 子画面の「1本目が出る瞬間」を、実演で最初の音が鳴る瞬間に合わせる
    at = (span[0] - delay) if span else 0.0
    fc = (f"[1:v]trim=start={off:.3f},setpts=PTS-STARTPTS+{at:.3f}/TB,"
          f"scale=iw*{width_ratio}/1:-2,pad=iw+6:ih+6:3:3:white[p];"
          f"[0:v][p]overlay={pos}:shortest=1{enable}[v]")
    cmd = ["ffmpeg", "-v", "error", "-y", "-i", base, "-i", pinp,
           "-filter_complex", fc, "-map", "[v]", "-map", "0:a?",
           "-c:v", "libx264", "-crf", "18", "-preset", "medium",
           "-c:a", "aac", "-b:a", "192k", out]
    subprocess.run(cmd, check=True)
    return off


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True, help="実演の映像")
    ap.add_argument("--pinp", required=True, help="復号画面の録画")
    ap.add_argument("--out", required=True)
    ap.add_argument("--ratio", type=float, default=0.30, help="子画面の幅（親に対する割合）")
    ap.add_argument("--margin", type=int, default=24, help="端からの余白[px]")
    ap.add_argument("--corner", default="右上", choices=["右下", "左下", "右上", "左上"])
    ap.add_argument("--span", default=None,
                    help="子画面を出す区間を手で決める（例 10.2,19.4）。"
                         "1本の映像に独立した吹奏が2回入るときは自動判定に任せない")
    ap.add_argument("--whole", action="store_true",
                    help="吹いている区間だけでなく、最初から最後まで子画面を出す")
    a = ap.parse_args(argv)
    # 子画面の実寸は「親の幅 × ratio」。scale へ渡すため、親の幅を測って係数にする。
    def vwidth(path):
        # ★"634," のように余計な区切りが付いて返ることがある★ 数字だけ取り出す。
        out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                              "-show_entries", "stream=width", "-of", "csv=p=0", path],
                             capture_output=True, text=True).stdout
        return int("".join(ch for ch in out.split("\n")[0] if ch.isdigit()))
    ratio = (vwidth(a.base) * a.ratio) / vwidth(a.pinp)
    if a.span:
        span = tuple(float(x) for x in a.span.split(","))
    else:
        span = None if a.whole else blow_span(a.base)
    # ★子画面が黒く映らないようにする★
    # 録画の中では、音が鳴り始めてから1本目の音名が出るまでに少し間がある（解析の遅れ）。
    # 実演で最初の音が鳴る瞬間に1本目の音名が出るよう、**重ねる位置を前へずらす**。
    # 表示を始める時刻はそのままにする（ここを動かすと子画面が出遅れて短くなる）。
    marks = os.path.splitext(a.pinp)[0] + ".marks.json"
    fn = first_note_offset(marks)
    off0 = audio_start_offset(marks)
    delay = 0.0
    if fn is not None:
        delay = max(0.0, fn - off0)
    off = compose(a.base, a.pinp, a.out, ratio, a.margin, a.corner, span, delay)
    print("重ねた: %s（幅%.0f%%・%s・出す区間 %s・解析の遅れ %.1f秒ぶん前へ）"
          % (a.out, a.ratio * 100, a.corner,
             ("%.1f〜%.1f秒" % span) if span else "全部", delay))
    return 0


if __name__ == "__main__":
    sys.exit(main())
