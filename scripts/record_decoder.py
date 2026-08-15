#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""実演の録画を復号ページに流し込み、その画面を動画に撮る（紹介動画のPinP用）。

なにをするか
------------
画面を持たない Chrome で復号ページを開き、`demoaudio=` で実演の音声を流す。
1本ずつ音名が現れていく様子を CDP の Page.startScreencast で受け取り、
連番の画像として貯めてから ffmpeg で動画にする。

★画面を持たない Chrome を使う理由★
--------------------------------
手元の画面を録るやり方だと、画面がスリープしていると真っ黒になるし、その間
利用者の画面を占有する。ヘッドレスなら状態に左右されない。

★踏んだ罠★
-----------
* **タブが前面にないと requestAnimationFrame が止まる。** 音だけが進んで解析が
  一度も回らない。復号ページ側は demoaudio のとき setTimeout で回すようにしたが、
  Chrome にも --disable-background-timer-throttling などを渡しておく。
* **音声の自動再生**は利用者の操作を求められる。--autoplay-policy=no-user-gesture-required
  を渡して外す。
* **AudioContext は止まった状態で始まる**ので、ページ側で resume している。

使い方
    python3 scripts/record_decoder.py --audio demo_2of2.wav --out out/pinp/demo_2of2.mp4 \\
        --seconds 22
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import shutil
import signal
import subprocess
import sys
import time
import urllib.request

import websocket                      # pip install websocket-client

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PORT = 9333
BASE = "http://localhost:8790/cipher/"
# 復号の設定は崇徳院・あらざらむと同じ（12スロット・隣接同音の禁止・パリティ1）
# ★雑音を2つの物差しで落とす★
# minnote=200 … 短い物音（実測93〜197ms）を落とす。本物は227〜630msある。
# onmargin=26 … ★これが要る★ 長さ534msの物音があり、短さだけでは落ちなかった
#   （つないだ映像の境目で出る）。大きさで見れば、雑音0.1〜4.6dBに対して本物は
#   20〜38dBとはっきり分かれる。32dBまで上げると本物の弱い音まで落ちたので26にした。
PARAMS = ("lo=G%236&hi=G7&norepeat=1&mode=symbols&parity=1&pitchsplit=1"
          "&splitcents=80&minnote=200&onmargin=26")


def launch(profile_dir, width, height):
    # ★前回の Chrome を必ず片づける★ 続けて何本も撮ると、終わりきる前に次が起動して
    # ポートを奪い合い、2本目以降が静かに落ちる（6本まとめて撮って1本しか残らなかった）。
    subprocess.run(["pkill", "-f", f"remote-debugging-port={PORT}"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.0)
    args = [CHROME, "--headless=new", f"--remote-debugging-port={PORT}",
            f"--user-data-dir={profile_dir}", "--no-first-run", "--disable-gpu",
            "--disable-background-timer-throttling",
            "--disable-backgrounding-occluded-windows",
            "--disable-renderer-backgrounding",
            "--autoplay-policy=no-user-gesture-required",
            # これが無いと CDP の WebSocket が 403 で弾かれる（Chrome 111以降）
            "--remote-allow-origins=*",
            "--mute-audio",                    # 解析はWeb Audio内で行う。外へ出す音は要らない
            f"--window-size={width},{height}",
            "about:blank"]
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


def record(audio_name, out_path, seconds, width, height, tmp, clip_h):
    crop_h = None
    frames_dir = os.path.join(tmp, "frames")
    shutil.rmtree(frames_dir, ignore_errors=True)
    os.makedirs(frames_dir, exist_ok=True)
    # ★プロファイルは毎回作り直す★ 前のインスタンスを pkill で落とすとロックが
    # 残り、次の起動が静かに失敗する。続けて何本も撮るときにこれで落ちた。
    profile = os.path.join(tmp, "chrome-profile-%d" % os.getpid())
    shutil.rmtree(profile, ignore_errors=True)
    proc = launch(profile, width, height)
    try:
        tabs = json.load(urllib.request.urlopen(f"http://localhost:{PORT}/json"))
        page = [t for t in tabs if t["type"] == "page"][0]
        tab = Tab(page["webSocketDebuggerUrl"])
        tab.send("Page.enable")
        tab.send("Runtime.enable")
        url = f"{BASE}#{PARAMS}&demoaudio=_demoaudio/{audio_name}"
        tab.send("Page.navigate", url=url)
        time.sleep(2.5)
        tab.evaluate("document.getElementById('autoStartBtn').click(); 1")

        # ★Page.startScreencast はヘッドレスではフレームを1枚も返さなかった★
        # （--headless=new + --disable-gpu の組み合わせ。30秒待っても無音のまま）。
        # 一定の間合いで captureScreenshot を撮るほうが確実である。PinPは小さく
        # 出すので、10コマ毎秒あれば音名が増える瞬間は十分に拾える。
        # ★撮るのはページ全体ではない★ そのまま撮ると版の履歴と注意書きばかりが写る。
        # 音名が増えていく列（autoSeq）と、拍のドット・状態表示を含む帯だけを切り取る。
        # ★高さは固定で取る★ autoSeq は音が増えるにつれて下へ伸びるので、撮り始めの
        # 高さで切ると、増えた行がはみ出して肝心のところが写らない（1度これで撮り直した）。
        # ★音名の列より下は隠す★ 隠さないと「録音ファイルから読む」の説明が子画面に
        # 入り込み、何を見せたいのか分からない絵になる。高さを固定で撮る以上、
        # 余った所は背景色で埋まってくれたほうがよい。
        # ★子画面では音名だけを大きく見せる★ 親の幅の3割に縮めて置くので、周波数や
        # 長さの小さい字は読めない。読めないものを載せても画が濁るだけなので落とす。
        tab.evaluate("""(() => {
          const st = document.createElement('style');
          st.textContent = '#autoSeq .fz{display:none}'
            + '#autoSeq .why{display:none}'
            + '#autoSeq .cents{display:none}'
            + '#autoSeq .nm{font-size:40px;line-height:1.15;margin:2px 0}'
            + '#autoSeq .idx{font-size:13px;opacity:.75}'
            + '#autoSeq .chip{padding:8px 14px}';
          document.head.appendChild(st);
          return 1;
        })()""")
        tab.evaluate("""(() => {
          const seq = document.getElementById('autoSeq');
          // ★同じ親の中だけでは足りない★ 次の節（2''の説明）は別のまとまりに入って
          // いるので、seq を含むまとまりごと後ろを隠さないと子画面に写り込む。
          let n = seq.nextElementSibling;
          while(n){ n.style.display = 'none'; n = n.nextElementSibling; }
          let box = seq.parentElement;
          while(box && box !== document.body){
            let m = box.nextElementSibling;
            while(m){ m.style.display = 'none'; m = m.nextElementSibling; }
            box = box.parentElement;
          }
          return 1;
        })()""")
        clip = json.loads(tab.evaluate(("""(() => {
          const seq = document.getElementById('autoSeq');
          const r = seq.getBoundingClientRect();
          return JSON.stringify({x: Math.round(r.left + scrollX - 10),
                                 y: Math.round(r.top + scrollY - 10),
                                 width: Math.round(r.width + 20),
                                 height: CLIP_H, scale: 1});
        })()""").replace("CLIP_H", str(clip_h))))
        print("  切り取る範囲 %(width)dx%(height)d（左上 %(x)d,%(y)d）" % clip)

        t0 = time.time()
        n = 0
        interval = 1.0 / 10
        ended = False
        marks = []          # 各コマが実演の音の何秒目にあたるか。あとで映像と合わせる
        while time.time() - t0 < seconds:
            tick = time.time()
            r = tab.send("Page.captureScreenshot", format="jpeg", quality=85,
                         clip=clip, captureBeyondViewport=True)
            n += 1
            with open(os.path.join(frames_dir, "f%05d.jpg" % n), "wb") as f:
                f.write(base64.b64decode(r["data"]))
            at = tab.evaluate("window.__demoAudio ? window.__demoAudio.currentTime : -1")
            marks.append({"frame": n, "wall": round(tick - t0, 3), "audio": round(at or 0, 3)})
            # 音が終わったら「終了し復号」を押す。復号までを1本の映像に収めるため。
            if not ended and tab.evaluate("window.__demoAudio && window.__demoAudio.ended ? 1 : 0"):
                tab.evaluate("document.getElementById('autoStartBtn').click(); 1")
                ended = True
                time.sleep(0.4)          # 復号の結果が画面に出るのを待つ
                # ★想定の本数がそろって復号できたときだけ「認証成功」を出す★
                # ★判定は「復号できました」の文言で行う★ decodedPayload の中身だけを
                # 見ると、失敗しているのに成功と出してしまう（一度そうなった）。
                tab.evaluate("""(() => {
                  const box = document.getElementById('autoDecoded');
                  const t = box ? (box.textContent || '') : '';
                  if(t.indexOf('\u5fa9\u53f7\u3067\u304d\u307e\u3057\u305f') < 0) return 0;
                  if(t.indexOf('\u3067\u304d\u307e\u305b\u3093') >= 0) return 0;
                  const b = document.createElement('div');
                  b.textContent = '\u8a8d\u8a3c\u6210\u529f';
                  b.style.cssText = 'flex-basis:100%;text-align:center;font-size:46px;'
                    + 'font-weight:700;color:#3ddc84;letter-spacing:.12em;padding:10px 0 2px';
                  document.getElementById('autoSeq').appendChild(b);
                  return 1;
                })()""")
            rest = interval - (time.time() - tick)
            if rest > 0:
                time.sleep(rest)
        # ★最後に実際の高さを測る★ 音が何本になるかは撮ってみないと分からないので、
        # 撮影は大きめの枠で行い、終わってから使われた高さぶんに切り詰める。
        # そうしないと8本の素材で下半分が空白のまま残る。
        used_h = tab.evaluate("""(() => {
          const r = document.getElementById('autoSeq').getBoundingClientRect();
          return Math.ceil(r.height) + 20;
        })()""") or clip["height"]
        crop_h = max(120, min(int(used_h), clip["height"]))
        with open(os.path.splitext(out_path)[0] + ".marks.json", "w") as f:
            json.dump({"clip": clip, "cropHeight": crop_h, "marks": marks}, f, ensure_ascii=False)
        print("  使った高さ %d px（撮った枠は %d px）" % (crop_h, clip["height"]))
        seq = tab.evaluate("document.getElementById('autoSeq').textContent.replace(/\\s+/g,' ')")
        print("  取れた枚数 %d（%.1f秒・平均%.1f fps）" % (n, seconds, n / max(seconds, 1e-9)))
        print("  読み取り: %s" % (seq or "")[:200])
    finally:
        proc.send_signal(signal.SIGTERM)
        try:
            proc.wait(timeout=10)
        except Exception:
            proc.kill()

    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    fps = max(1.0, n / seconds)
    # ★幅と高さは偶数にする★ 奇数のままだと libx264 が yuv420p を組めず
    # 「Could not open encoder before EOF」で落ちる（高さ1113で踏んだ）。
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", "%.3f" % fps,
                    "-i", os.path.join(frames_dir, "f%05d.jpg"),
                    "-vf", f"crop=iw:{crop_h}:0:0,fps=30,"
                           "scale=trunc(iw/2)*2:trunc(ih/2)*2,format=yuv420p",
                    "-c:v", "libx264", "-crf", "20", out_path], check=True)
    return out_path


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--audio", required=True, help="docs/cipher/_demoaudio/ の中の音声ファイル名")
    ap.add_argument("--out", required=True, help="書き出す動画")
    ap.add_argument("--seconds", type=float, required=True, help="撮る長さ[秒]")
    ap.add_argument("--clip-height", type=int, default=360,
                    help="切り取る高さ[px]。音が多いほど列が下へ伸びる。8本なら360、24本なら480")
    ap.add_argument("--width", type=int, default=900)
    ap.add_argument("--height", type=int, default=1200)
    ap.add_argument("--tmp", default=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                  os.pardir, "temp", "pinp"))
    a = ap.parse_args(argv)
    os.makedirs(a.tmp, exist_ok=True)
    print("● %s を %.1f 秒ぶん撮る" % (a.audio, a.seconds))
    out = record(a.audio, a.out, a.seconds, a.width, a.height, a.tmp, a.clip_height)
    print("  書き出した: %s" % out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
