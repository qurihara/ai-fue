#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""笛を吹くと電子錠が開く。マイクを聞き続け、正しい音の列が来たらその場で解錠する。

なにをするか
------------
マイクを常時開いたまま、直近の数秒を繰り返し復号する。**ボタンを押す操作はどこにもない。**
カード（笛8本＝基準笛1本＋データ7本、パリティなし）を吹き終えると、無音が来た時点で
復号し、あらかじめ登録した秘密と一致すれば錠へコマンドを送る。

なぜこの作りか
--------------
* [* 錠との接続は開いたまま保つ]。毎回つなぎ直すと、接続2秒・ログイン2秒・応答待ち2秒で
  6秒かかる。吹いてから6秒待つ体験は成立しない。ログイン済みの Session を持ち回れば
  送信だけになり、1秒を切る。切られたら黙って繋ぎ直す。
* [* 吹き終わりを無音で判定する]。窓をずらしながら常に復号を試すと、途中まで吹いた列が
  たまたま通ってしまう。最後の音から一定の無音が続いたときだけ判定する。
* 解析は録音解析（scripts/analyze_recording.py）と同じ関数を使う。復号ページと山の追い方・
  暗騒音の決め方が揃っているので、ページで読める音はここでも読める。

使い方
------
先に人の手で中継サーバを起動しておく（macOSがBluetoothの用途説明を求めるため、
ここから起動すると強制終了される）。

    cd .../sesami-api/sesame-ctrl
    bash run_ble_server.sh        # このウィンドウは開いたままにする

そのうえで、

    python3 demo/whistle_unlock.py --device bot2 --secret 4,9,5,10,3,7,2
    python3 demo/whistle_unlock.py --device bot2 --card out/cipher_card_v4_share2.3mf

--secret はカードに載せた記号列である。--dry-run を付けると錠へ送らずに判定だけ出す
（音の調整に使う）。--list-audio でマイクの一覧が出る。
"""
from __future__ import annotations

import argparse
import json
import math
import os
import subprocess
import sys
import threading
import time
from collections import deque

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "fue"))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import cipher_codec as cc                     # noqa: E402
import analyze_recording as ar                # noqa: E402

# 錠の側。別リポジトリにあるので明示的に足す（鍵はあちら側の devices.json にある）
SESAME_DIR = os.path.join(ROOT, os.pardir, "sesami-api", "sesame-ctrl")

SR = 44100
WINDOW_SEC = 9.0        # 解析にかける窓。カード8本は4〜5秒で吹き終わる
TAIL_SILENCE = 0.45     # 最後の音からこれだけ無音が続いたら「吹き終わり」とみなす[秒]
POLL_SEC = 0.20         # 窓を見直す間隔
COOLDOWN_SEC = 6.0      # 一度開けたら、これだけは次を受け付けない
N_FLUTES = 8            # カードの笛の本数（基準笛を含む）
SLOT12 = dict(lo_note="G#6", hi_note="G7")

# 錠のコマンド。Bot 2 は押すだけ、他は解錠。
DEFAULT_COMMAND = {"bot2": "click", "bike": "unlock", "m315": "unlock"}


# ---------------------------------------------------------------- 音を聞く
class Ear:
    """ffmpeg にマイクを開かせ、生の波形を輪の緩衝へ流し込む。"""

    def __init__(self, device="0", seconds=WINDOW_SEC + 3.0, ffmpeg="ffmpeg"):
        self.n = int(SR * seconds)
        self.buf = np.zeros(self.n, dtype=np.float32)
        self.filled = 0
        self.pos = 0
        self.lock = threading.Lock()
        self.proc = subprocess.Popen(
            [ffmpeg, "-hide_banner", "-loglevel", "error",
             "-f", "avfoundation", "-i", ":%s" % device,
             "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.alive = True
        threading.Thread(target=self._pump, daemon=True).start()

    def _pump(self):
        chunk = 4096 * 4
        while self.alive:
            raw = self.proc.stdout.read(chunk)
            if not raw:
                break
            x = np.frombuffer(raw, dtype=np.float32)
            with self.lock:
                for part in (x,):
                    k = len(part)
                    if k >= self.n:
                        self.buf[:] = part[-self.n:]
                        self.pos = 0
                    else:
                        end = self.pos + k
                        if end <= self.n:
                            self.buf[self.pos:end] = part
                        else:
                            first = self.n - self.pos
                            self.buf[self.pos:] = part[:first]
                            self.buf[:k - first] = part[first:]
                        self.pos = end % self.n
                    self.filled = min(self.n, self.filled + k)

    def snapshot(self):
        """いま持っている波形を、古い順に並べ直して返す。"""
        with self.lock:
            if self.filled < self.n:
                return self.buf[:self.pos].copy()
            return np.concatenate([self.buf[self.pos:], self.buf[:self.pos]])

    def close(self):
        self.alive = False
        try:
            self.proc.terminate()
        except Exception:
            pass


# ---------------------------------------------------------------- 錠を開ける
class Lock:
    """ログイン済みの接続を持ち回る。切られたら黙って繋ぎ直す。"""

    def __init__(self, name, command=None, dry_run=False):
        self.name = name
        self.command = command or DEFAULT_COMMAND.get(name, "unlock")
        self.dry_run = dry_run
        self.session = None
        self.sb = None
        if dry_run:
            return
        sys.path.insert(0, os.path.abspath(SESAME_DIR))
        import sesame_ble  # noqa: E402
        self.sb = sesame_ble

    def ensure(self):
        """接続が無ければ張る。張れたら True。"""
        if self.dry_run or self.session is not None:
            return True
        try:
            address, device = self.sb.find_address(self.name)
            self.session = self.sb.connect_and_login(address, device["secret"])
            print("[錠] %s に接続してログインした。あとは送るだけで動く。" % device["label"])
            return True
        except Exception as e:
            print("[錠] 接続できない（%s: %s）。あとでやり直す。" % (type(e).__name__, e))
            self.session = None
            return False

    def fire(self):
        """コマンドを送る。1回だけ繋ぎ直して再試行する。"""
        if self.dry_run:
            print("[錠] （--dry-run のため送らない）%s に %s" % (self.name, self.command))
            return True
        for attempt in (1, 2):
            if not self.ensure():
                time.sleep(1.0)
                continue
            try:
                t0 = time.time()
                self.session.send(self.sb.COMMANDS[self.command])
                print("[錠] %s を送った（%.2f秒）" % (self.command, time.time() - t0))
                return True
            except Exception as e:
                print("[錠] 送信に失敗（%s）。繋ぎ直す。" % type(e).__name__)
                self.session = None
        return False


# ---------------------------------------------------------------- 音を読む
def listen_once(x, cfg, on_db_margin=12.0):
    """波形から音の並びを取り出す。戻り値は (周波数の列, 各音の終わり時刻)。"""
    lo = cc.note_to_freq(cfg.lo_note) * 0.94
    hi = cc.note_to_freq(cfg.hi_note) * 1.06
    times, peaks, levels = ar.spectrum_track(x, SR, lo, hi)
    if len(levels) == 0:
        return [], []
    quiet = np.sort(levels)[: max(1, len(levels) // 10)]
    on_db = float(np.median(quiet)) + on_db_margin
    segs = ar.segment(times, peaks, levels, on_db)
    freqs = [s["freq"] for s in segs]
    # segment はミリ秒で startMs / durationMs を返す。終わりの時刻を秒で作る。
    ends = [(s["startMs"] + s["durationMs"]) / 1000.0 for s in segs]
    return freqs, ends


def matches(got, want, tolerance=1):
    """読めた記号列が、登録した列と一致するとみなせるか。

    ★差分符号なので、1本の音の読み違いは必ず隣り合う2つの記号へ波及する★
    記号は「今回のスロット − 前回のスロット − 1」なので、ある笛が1スロット低く
    読まれると、その笛の記号が−1、次の笛の記号が+1になる（10,0 が 9,1 になる）。
    そこで「食い違いが隣り合う2箇所で、片方が+d、もう片方が−d」という形なら、
    音1本のずれとみなして通す。tolerance はそのずれの大きさの上限[スロット]である。

    デモのための緩和であって、秘密の保管には使わない。パリティを付けた用途では
    誤り訂正が同じ仕事をきちんと行う。
    """
    if len(got) != len(want):
        return False, "本数が違う"
    diff = [(i, g - w) for i, (g, w) in enumerate(zip(got, want)) if g != w]
    if not diff:
        return True, "完全に一致"
    if len(diff) == 2:
        (i, d1), (j, d2) = diff
        if j == i + 1 and d1 == -d2 and abs(d1) <= tolerance:
            return True, "%d本目が%dスロットずれただけ" % (i + 1, -d1)
    return False, "%d箇所が違う" % len(diff)


def main(argv=None):
    # 端末へ流しながら見るので、行ごとに吐き出す。パイプ越しだと既定では溜まって
    # しまい、吹いている最中に何本拾えているかが見えない。
    try:
        sys.stdout.reconfigure(line_buffering=True)
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="笛を吹くと電子錠が開く")
    ap.add_argument("--device", default="bot2", help="錠の名前（bot2 / bike / m315）")
    ap.add_argument("--command", default=None, help="送るコマンド。既定は機器ごとに決まる")
    ap.add_argument("--secret", default=None, help="カードに載せた記号列（例 4,9,5,10,3,7,2）")
    ap.add_argument("--audio", default="0", help="マイクの番号。--list-audio で調べる")
    ap.add_argument("--list-audio", action="store_true", help="音の入力装置を並べて終わる")
    ap.add_argument("--dry-run", action="store_true", help="錠へ送らず、判定だけ出す")
    ap.add_argument("--margin", type=float, default=12.0, help="暗騒音からのしきい値[dB]")
    ap.add_argument("--tolerance", type=int, default=1,
                    help="音1本ぶんのずれを何スロットまで許すか。0で厳密に一致を求める")
    args = ap.parse_args(argv)

    if args.list_audio:
        subprocess.run(["ffmpeg", "-hide_banner", "-f", "avfoundation",
                        "-list_devices", "true", "-i", ""])
        return 0

    with open(os.path.join(ROOT, "docs", "cipher", "cipher_config.json"), encoding="utf-8") as fp:
        base = json.load(fp)
    cfg = cc.CodecConfig(**{**base, **SLOT12, "ecc_parity": 0,
                            "mode": "symbols", "no_repeat": True})

    want = None
    if args.secret:
        want = [int(v) for v in args.secret.replace(",", " ").split()]
        print("[設定] 待ち受ける記号列: %s（笛%d本）" % (want, N_FLUTES))
    else:
        print("[設定] 記号列を指定していないので、8本そろって復号できたら開ける")

    lock = Lock(args.device, args.command, args.dry_run)
    lock.ensure()

    ear = Ear(args.audio)
    print("[耳] マイク %s を開いた。吹いてください。（Ctrl-C で終わり）" % args.audio)

    last_fire = 0.0
    last_report = 0.0
    try:
        while True:
            time.sleep(POLL_SEC)
            x = ear.snapshot()
            if len(x) < SR * 2:
                continue
            x = x[-int(SR * WINDOW_SEC):]
            freqs, ends = listen_once(x, cfg, args.margin)
            now = time.time()

            # 何本聞こえているかを、変化したときだけ出す（撮影中の目安になる）
            if freqs and now - last_report > 0.5:
                last_report = now
                print("  …%d本 %s" % (len(freqs), " ".join("%.0f" % f for f in freqs[-8:])))

            if len(freqs) != N_FLUTES:
                continue
            # 吹き終わりを待つ。最後の音の後に無音が続いていること。
            tail = (len(x) / SR) - ends[-1]
            if tail < TAIL_SILENCE:
                continue
            if now - last_fire < COOLDOWN_SEC:
                continue

            res = cc.decode(freqs, cfg)
            got = list(res.symbols) if hasattr(res, "symbols") else []
            if want is None:
                ok, why = res.status.startswith("ok"), res.status
            else:
                ok, why = matches(got, want, args.tolerance)
            print("[判定] %s → %s（%s）" % (got or res.status, "一致" if ok else "違う", why))
            if ok:
                last_fire = now
                lock.fire()
    except KeyboardInterrupt:
        print("\n終わります。")
    finally:
        ear.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
