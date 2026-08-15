#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""デモ専用の復号画面（docs/cipher/demo.html）を、実演の音に合わせて動画に撮る。

record_decoder.py との違い
--------------------------
あちらは本編の復号ページを撮るので、設定のつまみや注意書きを隠す細工が要り、
2枚組では必ず復号に失敗した。こちらは子画面のために作った画面を撮るだけである。

* **指定の本数がそろった瞬間に「認証成功」が出る**（復号の成否は見ない）
* **音が1本も来ていないうちは何も描かない**。まだ何も出ていない黒い枠が
  映像に残るのを防ぐ（v9 で5つの場面がそうなった）
* 最初の音が出た時刻を書き出すので、合成の側はそこから子画面を出せる

使い方
    python3 scripts/record_demo.py --audio demo_box.wav --need 8 \\
        --out out/pinp/demo_box.mp4 --seconds 16
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import shutil
import subprocess
import sys
import time
import urllib.request

import websocket

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PORT = 9333
BASE = "http://localhost:8790/cipher/demo.html"


def launch(profile_dir, width, height):
    # 前回の Chrome を必ず片づける。残っているとポートを奪い合って静かに落ちる。
    subprocess.run(["pkill", "-f", f"remote-debugging-port={PORT}"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.0)
    shutil.rmtree(profile_dir, ignore_errors=True)
    args = [CHROME, "--headless=new", f"--remote-debugging-port={PORT}",
            f"--user-data-dir={profile_dir}", "--no-first-run", "--disable-gpu",
            "--disable-background-timer-throttling",
            "--disable-backgrounding-occluded-windows",
            "--disable-renderer-backgrounding",
            "--autoplay-policy=no-user-gesture-required",
            "--remote-allow-origins=*",        # 無いと CDP の WebSocket が403で弾かれる
            "--mute-audio", f"--window-size={width},{height}", "about:blank"]
    p = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(50):
        try:
            with urllib.request.urlopen(f"http://localhost:{PORT}/json/version", timeout=1):
                return p
        except Exception:
            time.sleep(0.2)
    raise RuntimeError("Chrome が立ち上がらない")


class Tab:
    def __init__(self, ws_url):
        self.ws = websocket.create_connection(ws_url, timeout=30)
        self.id = 0

    def send(self, method, **params):
        self.id += 1
        self.ws.send(json.dumps({"id": self.id, "method": method, "params": params}))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get("id") == self.id:
                return msg.get("result", {})

    def evaluate(self, expr):
        r = self.send("Runtime.evaluate", expression=expr, returnByValue=True)
        return r.get("result", {}).get("value")


def record(audio, need, out_path, seconds, width, height, tmp, extra):
    frames = os.path.join(tmp, "frames")
    shutil.rmtree(frames, ignore_errors=True)
    os.makedirs(frames, exist_ok=True)
    proc = launch(os.path.join(tmp, "prof-%d" % os.getpid()), width, height)
    first_audio_t = None
    try:
        tabs = json.load(urllib.request.urlopen(f"http://localhost:{PORT}/json"))
        tab = Tab([t for t in tabs if t["type"] == "page"][0]["webSocketDebuggerUrl"])
        tab.send("Page.enable"); tab.send("Runtime.enable")
        url = f"{BASE}#demoaudio=_demoaudio/{audio}&need={need}" + (("&" + extra) if extra else "")
        tab.send("Page.navigate", url=url)
        time.sleep(2.0)

        n, marks = 0, []
        t0 = time.time()
        interval = 1.0 / 10
        while time.time() - t0 < seconds:
            tick = time.time()
            st = tab.evaluate("""(() => {
              const w = document.getElementById('wrap');
              const r = w.getBoundingClientRect();
              return JSON.stringify({idle: document.body.classList.contains('idle'),
                                     done: document.body.classList.contains('done'),
                                     n: document.querySelectorAll('#seq .chip').length,
                                     h: Math.ceil(r.height),
                                     at: window.__demoAudio ? window.__demoAudio.currentTime : -1});
            })()""")
            s = json.loads(st) if st else {}
            r = tab.send("Page.captureScreenshot", format="jpeg", quality=85,
                         clip={"x": 0, "y": 0, "width": width,
                               "height": max(120, min(int(s.get("h", 200)) + 8, height)),
                               "scale": 1},
                         captureBeyondViewport=True)
            n += 1
            with open(os.path.join(frames, "f%05d.jpg" % n), "wb") as f:
                f.write(base64.b64decode(r["data"]))
            marks.append({"frame": n, "wall": round(tick - t0, 3),
                          "audio": round(s.get("at", 0) or 0, 3),
                          "idle": bool(s.get("idle")), "n": s.get("n", 0)})
            if first_audio_t is None and not s.get("idle"):
                first_audio_t = tick - t0
            rest = interval - (time.time() - tick)
            if rest > 0:
                time.sleep(rest)
        got = tab.evaluate("document.querySelectorAll('#seq .chip').length")
        done = tab.evaluate("document.body.classList.contains('done')")
        hh = tab.evaluate("Math.ceil(document.getElementById('wrap').getBoundingClientRect().height)")
        print("  %d本を検出（要 %d本）／認証成功 %s／高さ %s px"
              % (got or 0, need, "出た" if done else "出ていない", hh))
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except Exception:
            proc.kill()

    # ★コマの大きさが途中で変わる★ 音が増えると枠が下へ伸びるので、いちばん大きい
    # コマに合わせて下を余白で埋めてから動画にする。揃えないと ffmpeg が受け付けない。
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    fps = max(1.0, n / seconds)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", "%.3f" % fps,
                    "-i", os.path.join(frames, "f%05d.jpg"),
                    "-vf", ("fps=30,pad=ceil(iw/2)*2:ceil(ih/2)*2:0:0:0x0f1420,"
                            "format=yuv420p"),
                    "-c:v", "libx264", "-crf", "20", out_path], check=True)
    meta = os.path.splitext(out_path)[0] + ".marks.json"
    with open(meta, "w") as f:
        json.dump({"firstNoteWall": first_audio_t, "marks": marks}, f, ensure_ascii=False)
    return first_audio_t


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--audio", required=True)
    ap.add_argument("--need", type=int, required=True, help="この本数で認証成功を出す")
    ap.add_argument("--out", required=True)
    ap.add_argument("--seconds", type=float, required=True)
    ap.add_argument("--width", type=int, default=760)
    ap.add_argument("--height", type=int, default=1400)
    ap.add_argument("--extra", default=None, help="画面へ渡す追加のパラメータ（&で連結）")
    ap.add_argument("--tmp", default=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                  os.pardir, "temp", "pinp"))
    a = ap.parse_args(argv)
    os.makedirs(a.tmp, exist_ok=True)
    print("● %s（%d本で成功）を %.0f秒" % (a.audio, a.need, a.seconds))
    t = record(a.audio, a.need, a.out, a.seconds, a.width, a.height, a.tmp, a.extra)
    print("  最初の音まで %.1f秒 → 子画面はここから出す" % (t if t is not None else -1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
