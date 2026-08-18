#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""暗号笛ウォレットの画面を、実演の音に合わせて動画に撮る（紹介動画の子画面用）。

record_demo.py との違い
-----------------------
あちらは復号の画面（音名がそろうと「認証成功」）を撮る。こちらは[* 口座と残高]を撮る。
「笛を吹く → 口座が現れる → 残高が出る」という一連が、子画面だけで伝わる。

撮るのは画面の上端だけである。題名・残高・アドレスが入る高さで切る。

守っていること
--------------
* [* 吹いていないのに音名が出ないこと。] ページ側で区切り器を保つようにしてある
  （demoAdvance）。ここでは各コマの音の位置と本数を控えて、あとから確かめられるようにする。
* [* 口座が出たあとのゆとり。] 音が終わってからも --after 秒だけ撮り続ける。
  残高とアドレスを目で追える時間を作るためである。
* 最初の音が出た時刻を書き出す。合成の側は、そこから子画面を出せばよい。

使い方
    python3 scripts/record_wallet.py --audio karuta.wav \\
        --url "?lo=G%236&hi=G7&norepeat=1&mode=symbols&parity=1&cards=2&expect=8" \\
        --out out/pinp/wallet_karuta.mp4 --after 3

音声は docs/dapp/_demoaudio/ に置く（gitでは追跡しない）。
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
import urllib.parse
import urllib.request

import websocket

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PORT = 9334                       # record_demo.py（9333）と別にして、同時に動かせるようにする
SERVE_PORT = 8793
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))
DOCS = os.path.join(ROOT, "docs")


def launch(profile_dir, width, height):
    # 前回の Chrome を必ず片づける。残っているとポートを奪い合って静かに落ちる。
    subprocess.run(["pkill", "-f", f"remote-debugging-port={PORT}"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.0)
    shutil.rmtree(profile_dir, ignore_errors=True)
    args = [CHROME, "--headless=new", f"--remote-debugging-port={PORT}",
            f"--user-data-dir={profile_dir}", "--no-first-run", "--disable-gpu",
            # ★これらが無いと、前面でないタブとして描画も時計も止められる★
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
    raise SystemExit("Chrome を起動できなかった")


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
        r = self.send("Runtime.evaluate", expression=expr, returnByValue=True,
                      awaitPromise=True)
        return r.get("result", {}).get("value")


def serve():
    """docs/ を配る。ページは同じ場所の音声とスクリプトを読むので、file:// では動かない。"""
    p = subprocess.Popen([sys.executable, "-m", "http.server", str(SERVE_PORT),
                          "--directory", DOCS],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(40):
        try:
            with urllib.request.urlopen(f"http://localhost:{SERVE_PORT}/dapp/", timeout=1):
                return p
        except Exception:
            time.sleep(0.2)
    p.terminate()
    raise SystemExit("配信を始められなかった")


def record(audio, query, out_path, after, width, height, tmp):
    frames = os.path.join(tmp, "frames")
    shutil.rmtree(frames, ignore_errors=True)
    os.makedirs(frames, exist_ok=True)

    srv = serve()
    proc = launch(os.path.join(tmp, "prof-%d" % os.getpid()), width, height)
    first_note_t = None
    try:
        tabs = json.load(urllib.request.urlopen(f"http://localhost:{PORT}/json"))
        tab = Tab([t for t in tabs if t["type"] == "page"][0]["webSocketDebuggerUrl"])
        tab.send("Page.enable")
        tab.send("Runtime.enable")
        q = query.lstrip("?&")
        url = (f"http://localhost:{SERVE_PORT}/dapp/?{q}"
               f"&demoaudio=_demoaudio/{urllib.parse.quote(audio)}")
        tab.send("Page.navigate", url=url)
        time.sleep(2.5)

        dur = tab.evaluate("""(async () => {
          const a = new Audio('_demoaudio/%s');
          await new Promise(r => { a.onloadedmetadata = r; a.onerror = r; });
          return a.duration || 0;
        })()""" % audio)
        if not dur:
            raise SystemExit("音声を読めなかった（docs/dapp/_demoaudio/%s を確かめること）" % audio)
        seconds = dur + after
        print("  音 %.1f秒 ＋ 後ろのゆとり %.1f秒 ＝ %.1f秒を撮る" % (dur, after, seconds))

        # ★切り取る高さは最初に決めて固定する★ コマごとに変えると、動画にしたとき
        # ffmpeg が最初のコマの大きさへ合わせて縦に潰す。
        fixed_h = int(tab.evaluate("""(() => {
          const c = document.getElementById('acctCard');
          return Math.ceil(c.getBoundingClientRect().bottom) + 12;
        })()""") or 260)
        print("  切り取る高さ %d px（題名と口座が入る。最後まで変えない）" % fixed_h)

        started = tab.evaluate("window.__startDemo().then(r => JSON.stringify(r))")
        if not started:
            raise SystemExit("音を流し始められなかった（demoaudio= が効いているか確かめること）")

        n, marks = 0, []
        t0 = time.time()
        interval = 1.0 / 10
        while time.time() - t0 < seconds:
            tick = time.time()
            st = tab.evaluate("""(() => {
              const card = document.getElementById('acctCard');
              return JSON.stringify({
                n: document.querySelectorAll('#seq .chip').length,
                open: card.classList.contains('open'),
                bal: document.getElementById('bal').textContent,
                addr: document.getElementById('addr').textContent.slice(0, 12),
                at: window.__demoAudio ? window.__demoAudio.currentTime : -1});
            })()""")
            s = json.loads(st) if st else {}
            r = tab.send("Page.captureScreenshot", format="jpeg", quality=88,
                         clip={"x": 0, "y": 0, "width": width, "height": fixed_h, "scale": 1},
                         captureBeyondViewport=True)
            n += 1
            with open(os.path.join(frames, "f%05d.jpg" % n), "wb") as f:
                f.write(base64.b64decode(r["data"]))
            marks.append({"frame": n, "wall": round(tick - t0, 3),
                          "audio": round(s.get("at", 0) or 0, 3),
                          "n": s.get("n", 0), "open": bool(s.get("open")),
                          "bal": s.get("bal", "")})
            if first_note_t is None and s.get("n"):
                first_note_t = tick - t0
            rest = interval - (time.time() - tick)
            if rest > 0:
                time.sleep(rest)

        fin = json.loads(tab.evaluate("""JSON.stringify({
          bal: document.getElementById('bal').textContent,
          addr: document.getElementById('addr').textContent,
          open: document.getElementById('acctCard').classList.contains('open')})"""))
        print("  口座 %s ／ 残高 %s POL ／ %s"
              % (fin["addr"][:14] + "…", fin["bal"], "開いた" if fin["open"] else "★開いていない★"))
        # 残高が見えていた時間を数える。ゆとりが足りているかの目安になる。
        shown = sum(1 for m in marks if m["bal"] not in ("–", ""))
        print("  残高が映っていたのは %.1f秒" % (shown * interval))
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except Exception:
            proc.kill()
        srv.terminate()

    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    fps = max(1.0, n / seconds)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", "%.3f" % fps,
                    "-i", os.path.join(frames, "f%05d.jpg"),
                    "-vf", "fps=30,scale=trunc(iw/2)*2:trunc(ih/2)*2,format=yuv420p",
                    "-c:v", "libx264", "-crf", "20", out_path], check=True)
    meta = os.path.splitext(out_path)[0] + ".marks.json"
    with open(meta, "w", encoding="utf-8") as f:
        json.dump({"firstNoteWall": first_note_t, "marks": marks}, f, ensure_ascii=False)
    print("  書き出した %s（最初の音名まで %.2f秒）"
          % (out_path, first_note_t if first_note_t is not None else -1))
    return first_note_t


def main(argv=None):
    ap = argparse.ArgumentParser(description="ウォレットの画面を録画する（紹介動画の子画面用）")
    ap.add_argument("--audio", required=True, help="docs/dapp/_demoaudio/ に置いた音声の名前")
    ap.add_argument("--url", required=True, help="読む笛の設定（?lo=…&cards=… の部分）")
    ap.add_argument("--out", required=True)
    ap.add_argument("--after", type=float, default=3.0,
                    help="音が終わってから撮り続ける秒数。残高を目で追う時間になる")
    ap.add_argument("--width", type=int, default=680)
    ap.add_argument("--height", type=int, default=900)
    ap.add_argument("--tmp", default="/tmp/record_wallet")
    args = ap.parse_args(argv)

    os.makedirs(args.tmp, exist_ok=True)
    record(args.audio, args.url, args.out, args.after, args.width, args.height, args.tmp)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
