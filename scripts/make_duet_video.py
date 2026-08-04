"""別々に撮ったChordikaとRecorikaの演奏を、拍を合わせて1本の動画に並べる。

2本の録画には同じ100bpmのメトロノームが入っている。これを手がかりに、和音側を何秒
遅らせれば拍が揃うかを求め、上下または左右に並べて書き出す。

ずれの求め方は2段階である。まず冒頭のメトロノームのクリックから拍の位相を実測し、
遅らせる量を「位相差 + 0.6秒 × 整数」に絞り込む。位相だけでは何拍ぶんずれているかが
決まらないので、次に音楽そのもので拍を決める。旋律は弱起で駆け上がってから最初の音を
長く伸ばし、和音側も最初の和音を長く鳴らす。この2つが同じ小節頭なので、その差を取って
先の格子に丸めればよい。

包絡の相互相関でも同じ値になるが、メトロノームが周期的なためピークが0.6秒おきに並び、
単独では決め手にならなかった。「長く伸ばした最初の音どうしを合わせる」ほうが確実である。

  python3 scripts/make_duet_video.py --dir temp/chordika_recorika
  python3 scripts/make_duet_video.py --dir temp/chordika_recorika --delay 1.755

--delay を渡すと自動推定を使わずその値で合成する。1拍(0.6秒)ずれていたら
ここを 0.6 増減させて刷り直すのが早い。
"""
import argparse
import os
import subprocess
import sys

import numpy as np

SR = 22050
NFFT = 1024
HOP = 64
FPS = SR / HOP
BEAT = 0.6008          # 100bpm。実測したクリック間隔
FUE_BAND = (1400, 3600)  # 笛の音がいる帯域。メトロノームや息の音と分けるため


def decode(path, out):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", path,
                    "-ac", "1", "-ar", str(SR), "-f", "f32le", out], check=True)
    return np.fromfile(out, dtype=np.float32)


def band_env(x, lo, hi):
    n = (len(x) - NFFT) // HOP
    w = np.hanning(NFFT)
    S = np.abs(np.fft.rfft(np.stack([x[i * HOP:i * HOP + NFFT] * w for i in range(n)]), axis=1))
    f = np.fft.rfftfreq(NFFT, 1 / SR)
    return S[:, (f >= lo) & (f < hi)].mean(1)


def click_phase(x, guesses):
    """メトロノームのクリック時刻を精密化し、拍の位相を返す。"""
    times = []
    for t in guesses:
        i = int(t * SR)
        a, b = max(0, i - int(0.035 * SR)), i + int(0.035 * SR)
        times.append((a + int(np.argmax(np.abs(x[a:b])))) / SR)
    return times[0] % BEAT, times


def find_clicks(x, upto):
    """冒頭の静かな区間から、0.6秒間隔で並ぶ小さな立ち上がりを拾う。"""
    W = int(0.01 * SR)
    seg = x[:int(upto * SR)]
    e = np.sqrt((seg[:len(seg) // W * W].reshape(-1, W) ** 2).mean(1))
    thr = np.percentile(e, 97)
    cand = [i * 0.01 for i in range(len(e)) if e[i] > thr and (i == 0 or e[i - 1] <= thr)]
    # 0.6秒間隔で2つ以上つながるものだけを残す
    keep = [t for t in cand if any(abs((u - t) - BEAT) < 0.05 for u in cand)]
    return keep[:4] if keep else cand[:2]


def first_long_note(x, minlen=0.35):
    """最初に minlen 秒以上のばされた音の始まりを返す（＝最初の小節頭）。

    しきい値は最大値ではなく上位分位で決める。録画によっては終盤だけが極端に大きく、
    最大値を基準にすると冒頭の音が丸ごと沈黙とみなされてしまう（実際にそうなった）。
    """
    e = band_env(x, *FUE_BAND)
    on = e > np.percentile(e, 90) * 0.25
    need = int(minlen * FPS)
    run = 0
    for i, v in enumerate(on):
        if v:
            run += 1
            if run >= need:
                return (i - run + 1) / FPS
        else:
            run = 0
    raise SystemExit("のばした音を見つけられなかった。--delay で直接指定する。")


def estimate_delay(xa, xb):
    """xa(和音)を何秒遅らせれば xb(旋律)と拍が合うかを推定する。"""
    ca = find_clicks(xa, 1.4)
    cb = find_clicks(xb, 2.3)
    if not ca or not cb:
        raise SystemExit("メトロノームのクリックを見つけられなかった。--delay で直接指定する。")
    pa, ta = click_phase(xa, ca)
    pb, tb = click_phase(xb, cb)
    base = (pb - pa) % BEAT
    la = first_long_note(xa)
    lb = first_long_note(xb)
    raw = lb - la
    k = round((raw - base) / BEAT)
    d = base + BEAT * max(0, k)
    print("  クリック実測  和音 %s / 旋律 %s" % (np.round(ta, 4), np.round(tb, 4)))
    print("  拍の位相      和音 %.4f 秒 / 旋律 %.4f 秒" % (pa, pb))
    print("  候補は %.4f + 0.6008k 秒 に限られる" % base)
    print("  最初にのばした音  和音 %.3f 秒 / 旋律 %.3f 秒  → 差 %.3f 秒" % (la, lb, raw))
    print("  格子に丸めて %.3f 秒（%d拍）" % (d, round(d / BEAT)))
    return d


def build(a, b, delay, out, layout):
    """拍を合わせて a(和音)と b(旋律)を並べる。文字は入れない。

    和音側を黒で待たせるのではなく、旋律側の頭を delay 秒だけ切り落とす。こうすれば
    1フレーム目から両方に映像が出る。終わりは短いほうに合わせて切る。
    """
    W, H = 960, 540
    stack = "vstack" if layout == "vertical" else "hstack"
    fc = (
        "[0:v]scale={W}:{H},setpts=PTS-STARTPTS[a];"
        "[1:v]trim=start={d:.4f},setpts=PTS-STARTPTS,scale={W}:{H}[b];"
        "[a][b]{stack}=shortest=1[v];"
        "[0:a]volume=1.0,asetpts=PTS-STARTPTS[aa];"
        "[1:a]atrim=start={d:.4f},asetpts=PTS-STARTPTS,volume=1.6[bb];"
        "[aa][bb]amix=inputs=2:duration=shortest:normalize=0,alimiter=limit=0.95[aout]"
    ).format(W=W, H=H, d=delay, stack=stack)
    cmd = ["ffmpeg", "-v", "error", "-y", "-i", a, "-i", b,
           "-filter_complex", fc, "-map", "[v]", "-map", "[aout]",
           "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--chord", default="march_chord.TS.mp4")
    ap.add_argument("--melody", default="march_melody.TS.mp4")
    ap.add_argument("--delay", type=float, default=None, help="和音側を遅らせる秒数。省略すると自動推定")

    args = ap.parse_args()

    a = os.path.join(args.dir, args.chord)
    b = os.path.join(args.dir, args.melody)
    for p in (a, b):
        if not os.path.exists(p):
            raise SystemExit("見つからない: %s" % p)

    if args.delay is None:
        print("ずれを推定する")
        xa = decode(a, "/tmp/_duet_a.raw")
        xb = decode(b, "/tmp/_duet_b.raw")
        delay = estimate_delay(xa, xb)
    else:
        delay = args.delay
    print("\n和音側を %.3f 秒 遅らせて合成する（%.2f 拍ぶん）" % (delay, delay / BEAT))

    outs = []
    for layout, name in (("vertical", "march_duet_updown.mp4"), ("horizontal", "march_duet_leftright.mp4")):
        o = os.path.join(args.dir, name)
        build(a, b, delay, o, layout)
        size = os.path.getsize(o) / 1e6
        print("  書き出し %s (%.1f MB)" % (name, size))
        outs.append(o)
    return 0


if __name__ == "__main__":
    sys.exit(main())
