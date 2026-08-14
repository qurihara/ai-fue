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


def compose(base, pinp, out, width_ratio, margin, corner):
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
    fc = (f"[1:v]trim=start={off:.3f},setpts=PTS-STARTPTS,"
          f"scale=iw*{width_ratio}/1:-2,pad=iw+6:ih+6:3:3:white[p];"
          f"[0:v][p]overlay={pos}:shortest=1[v]")
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
    ap.add_argument("--corner", default="右下", choices=["右下", "左下", "右上", "左上"])
    a = ap.parse_args(argv)
    # 子画面の実寸は「親の幅 × ratio」。scale へ渡すため、親の幅を測って係数にする。
    def vwidth(path):
        # ★"634," のように余計な区切りが付いて返ることがある★ 数字だけ取り出す。
        out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                              "-show_entries", "stream=width", "-of", "csv=p=0", path],
                             capture_output=True, text=True).stdout
        return int("".join(ch for ch in out.split("\n")[0] if ch.isdigit()))
    ratio = (vwidth(a.base) * a.ratio) / vwidth(a.pinp)
    off = compose(a.base, a.pinp, a.out, ratio, a.margin, a.corner)
    print("重ねた: %s（子画面は親の幅の%.0f%%・%s・音の頭出し %.2f秒）"
          % (a.out, a.ratio * 100, a.corner, off))
    return 0


if __name__ == "__main__":
    sys.exit(main())
