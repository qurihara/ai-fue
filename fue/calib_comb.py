"""較正コーム36本（12音 G#6〜G7 を各3本）の実測周波数を集計する。

コームの並びは、12音を3周し、各周の開始音を4半音ずらしたものである。隣り合う位置が同じ音に
なることは1箇所もないので、音の変わり目で区切る読み方（復号ページの pitchsplit）で36本を
続けて吹いて一気に測れる。同じ音の3本は左・中・右の区画に1本ずつ入る。

このモジュールが出す指標は次の4つである。

  吹き方のばらつき
      同じ笛を複数回吹いた値の標準偏差をすべての位置でまとめたもの。

  造形のばらつき σ
      同じ音の3本それぞれの平均が散らばる度合い。吹き方のばらつきが混ざるぶんを差し引いた
      値も出す。10セント前後であれば50セント刻みが成立し、笛1本あたりの情報量が26%増える。

  系統的なずれ
      狙いの周波数からのずれ。復号器は基準笛との比で読むので、全音に共通するずれは自動的に
      消える。実害があるのは音によって違う成分（共通分を引いた残り）だけである。

  較正定数の再推定
      f = A/(L+e) を実測へ最小二乗で当てはめ直して、新しい A と e を出す。e を1次元で走査し、
      各 e について A を対数軸上の平均から閉じた形で決める（セント単位の残差を最小にする）。

使い方:
    python fue/calib_comb.py 測定値.txt
    python fue/calib_comb.py 測定値.txt --range=4-33   # 4番から33番までを吹いた場合

測定値ファイルは、1回ぶんの吹鳴（36個の数値）を1つのまとまりとして、空行かコメント行で
区切って並べる。鳴らなかった笛は - か x と書けば欠測として扱う。両端の笛がめくれなどの
造形不良で鳴らず、生きている範囲だけを吹いた場合は --range=最初-最後 を渡せば、その範囲の
個数だけを書けばよい。範囲の外は欠測として集計する。
"""
import math
import os
import re
import sys

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, "out")
NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']


def load_calibration():
    """較正定数 A,e を読む。mini10 と同じファイル（同じ優先順位）を見る。

    集計だけのためにメッシュ処理の重い依存を持ち込みたくないので、mini10 を読み込まずに
    同じファイルを直接読む。参照先が同じなので値が食い違うことはない。
    """
    A, E = 86338.0, -13.06
    for name in ("cipher_mini10_calib.txt", "mini10_calib_v11.txt"):
        p = os.path.join(OUT, name)
        if os.path.exists(p):
            for line in open(p, encoding="utf-8"):
                line = line.strip()
                if line.startswith("A="):
                    A = float(line.split("=")[1].split()[0])
                elif line.lower().startswith("e="):
                    E = float(line.split("=")[1].split()[0])
            break
    return A, E


CALIB_A, CALIB_E = load_calibration()


def note_to_midi(note):
    name, octv = note[:-1], int(note[-1])
    return 12 * (octv + 1) + NAMES.index(name)


def note_to_freq(note):
    return 440.0 * 2 ** ((note_to_midi(note) - 69) / 12.0)


def length_for_note(note):
    """狙いの音を出すために設計した管長[mm]（現行の較正定数による）。"""
    return CALIB_A / note_to_freq(note) - CALIB_E


# 12スロット体系の音（G#6〜G7）。
NOTES12 = ["G#6", "A6", "A#6", "B6", "C7", "C#7", "D7", "D#7", "E7", "F7", "F#7", "G7"]

# 36本の並び。12音を3周し、各周の開始音を4半音（インデックス4つ）ずらしてある。
LAYOUT = [NOTES12[(i + 4 * r) % 12] for r in range(3) for i in range(12)]


def cents(f, f_ref):
    """f が f_ref より何セント高いか。"""
    return 1200.0 * math.log2(f / f_ref)


def parse_measurements(text, first=1, last=None):
    """測定値のテキストを、吹鳴1回ぶん36個の並びの一覧へ変換する。

    空行かコメント行（# で始まる行）でまとまりを区切る。各まとまりから数値を順に拾い、
    - か x か欠測を表す語は None にする。

    first と last は、実際に吹いた位置の範囲（1始まり、両端を含む）である。両端の笛が
    めくれなどの造形不良で鳴らず、生きている範囲だけを吹いた場合に使う。範囲の外は
    欠測として埋める。既定では36個ちょうどを求める。
    """
    blocks, cur = [], []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            if cur:
                blocks.append(cur)
                cur = []
            continue
        cur.append(stripped)
    if cur:
        blocks.append(cur)

    n_all = len(LAYOUT)
    last = n_all if last is None else last
    if not (1 <= first <= last <= n_all):
        raise ValueError("範囲の指定が正しくない: %d〜%d（1〜%dの中で指定する）"
                         % (first, last, n_all))
    n_want = last - first + 1

    token = re.compile(r"[-+]?\d*\.?\d+|[-xX×]|欠|なし")
    passes = []
    for block in blocks:
        vals = []
        for tok in token.findall(" ".join(block)):
            if tok in ("-", "x", "X", "×", "欠", "なし"):
                vals.append(None)
            else:
                vals.append(float(tok))
        if len(vals) != n_want:
            raise ValueError(
                "1回ぶんの測定値が%d個ある。%d番から%d番までの%d個でなければならない。"
                "両端が造形不良で鳴らないなら、その位置に - と書くか、範囲を指定する: %s"
                % (len(vals), first, last, n_want, vals)
            )
        passes.append([None] * (first - 1) + vals + [None] * (n_all - last))
    if not passes:
        raise ValueError("測定値が1回ぶんも読み取れなかった。")
    return passes


def align_measurements(meas, notes, center=70.0, sigma=45.0, miss=6.0, split=3.0):
    """測定値の並びを、期待する音の並びへ対応づける（動的計画法）。

    実物を続けて吹くと、鳴らない笛が飛ばされたり、1本の吹鳴が途中の音の揺れで2つに
    分かれたりして、測定値の個数が笛の本数と合わなくなる。そこで、音1つに対して
    測定値0個（鳴らず）・1個・2個（区切りの誤分割。2つは幾何平均でまとめる）を許し、
    狙いからのずれが共通の値 center の近くに揃う対応を選ぶ。

    meas は測定値の並び（欠測を除いたもの）、notes は吹いた順の音名の並びである。
    戻り値は (合計費用, 対応の並び)。対応は (音の位置, 種別, 使った測定値) の組で、
    種別は "one"（1対1）、"split"（2つに分かれた）、"miss"（鳴らなかった）である。
    費用は小さいほど良く、吹いた向きの判定にも使える（正順と逆順で比べる）。
    """
    m, n = len(meas), len(notes)
    inf = float("inf")
    D = [[inf] * (n + 1) for _ in range(m + 1)]
    B = [[None] * (n + 1) for _ in range(m + 1)]
    D[0][0] = 0.0

    def w(f, note):
        return ((cents(f, note_to_freq(note)) - center) / sigma) ** 2

    for i in range(m + 1):
        for j in range(n + 1):
            if D[i][j] == inf or j >= n:
                continue
            c = D[i][j] + miss                      # この音は鳴らなかった
            if c < D[i][j + 1]:
                D[i][j + 1] = c
                B[i][j + 1] = (i, j, "miss", [])
            if i < m:                               # 1対1で対応する
                c = D[i][j] + w(meas[i], notes[j])
                if c < D[i + 1][j + 1]:
                    D[i + 1][j + 1] = c
                    B[i + 1][j + 1] = (i, j, "one", [meas[i]])
            if i + 1 < m and abs(cents(meas[i], meas[i + 1])) < 100:
                avg = math.sqrt(meas[i] * meas[i + 1])   # 1本が2つに分かれた
                c = D[i][j] + w(avg, notes[j]) + split
                if c < D[i + 2][j + 1]:
                    D[i + 2][j + 1] = c
                    B[i + 2][j + 1] = (i, j, "split", [meas[i], meas[i + 1]])

    if D[m][n] == inf:
        raise ValueError("測定値を音の並びへ対応づけられなかった。")
    path, i, j = [], m, n
    while B[i][j]:
        pi, pj, kind, vals = B[i][j]
        path.append((pj, kind, vals))
        i, j = pi, pj
    path.reverse()
    return D[m][n], path


def blow_direction(meas, layout=None, **kw):
    """吹いた向きを、対応づけの費用が小さい方から判定する。

    戻り値は ("forward" か "reverse", 正順の費用, 逆順の費用)。並びの端から端まで
    吹くとき、どちらの端から始めたかを取り違えると較正を丸ごと誤るので、
    測定値そのものから決める。
    """
    layout = layout or LAYOUT
    fwd, _ = align_measurements(meas, layout, **kw)
    rev, _ = align_measurements(meas, layout[::-1], **kw)
    return ("forward" if fwd <= rev else "reverse"), fwd, rev


def _mean(xs):
    return sum(xs) / len(xs)


def _sd(xs, ddof=1):
    """標本標準偏差。データが足りなければ None を返す。"""
    if len(xs) - ddof <= 0:
        return None
    m = _mean(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - ddof))


def fit_calibration(pairs):
    """(管長L, 実測周波数f) の組から f = A/(L+e) を最小二乗で当てはめる。

    セント単位（対数軸）の残差を最小にする。e を粗い走査から段階的に細かくして決め、
    各 e に対する A は log A = mean(log f + log(L+e)) で閉じた形に決まる。
    戻り値は (A, e, RMSセント)。
    """
    def solve_for(e):
        logs = [math.log(f) + math.log(L + e) for L, f in pairs]
        log_a = _mean(logs)
        resid = [(la - log_a) * 1200.0 / math.log(2) for la in logs]
        rms = math.sqrt(_mean([r * r for r in resid]))
        return math.exp(log_a), rms

    lo, hi = -30.0, 15.0
    best = None
    for _ in range(60):
        step = (hi - lo) / 200.0
        cands = []
        e = lo
        while e <= hi + 1e-12:
            if min(L + e for L, _ in pairs) > 1.0:
                a, rms = solve_for(e)
                cands.append((rms, e, a))
            e += step
        if not cands:
            raise ValueError("当てはめ可能な e の範囲が無い。")
        best = min(cands)
        lo, hi = best[1] - step, best[1] + step
        if hi - lo < 1e-6:
            break
    rms, e, a = best
    return a, e, rms


def analyze(passes, notes=None, lengths=None):
    """吹鳴ごとの36個の測定値から、各指標を計算する。

    lengths に {音名: 実際の管長[mm]} を渡すと、較正定数の当てはめにその値を使う。
    渡さなければ設計上の管長を使う。実物が設計どおりに刷れているとは限らず、たとえば
    外見統一のコームでは、いちばん低い音の空洞が外形の長さに頭打ちされて設計より
    短くなる。そのときは実測した管長で当てはめないと、造形の問題を較正の問題と
    取り違えてしまう。
    """
    notes = notes or LAYOUT
    n_pos = len(notes)
    result = {"n_passes": len(passes), "positions": [], "notes": {}}

    # 位置ごとの集計。
    for i in range(n_pos):
        vals = [p[i] for p in passes if p[i] is not None]
        note = notes[i]
        target = note_to_freq(note)
        entry = {
            "index": i + 1,
            "note": note,
            "values": vals,
            "n_missing": len(passes) - len(vals),
            "mean": _mean(vals) if vals else None,
            "sd_cents": None,
            "dev_cents": None,
        }
        if vals:
            cs = [cents(v, target) for v in vals]
            entry["dev_cents"] = _mean(cs)
            entry["sd_cents"] = _sd(cs)
        result["positions"].append(entry)

    # 一度も鳴らなかった位置（造形不良）。本数そのものが測定値なので記録する。
    result["dead"] = [(e["index"], e["note"]) for e in result["positions"] if not e["values"]]

    # 吹き方のばらつき（位置内のばらつきをまとめたもの）。
    ss, dof = 0.0, 0
    for e in result["positions"]:
        if e["sd_cents"] is not None:
            k = len(e["values"])
            ss += e["sd_cents"] ** 2 * (k - 1)
            dof += k - 1
    result["blow_sd_cents"] = math.sqrt(ss / dof) if dof else None
    result["blow_dof"] = dof

    # 音ごとの集計（同じ音の3本）。
    # あわせて、1本の平均が吹鳴 n 回の平均であることによる水増し分 σ_吹き方^2/n を、
    # 本ごとの回数に合わせて足し込んでおく（回数が本によって違うことがあるため）。
    ss_f, dof_f, inflate, n_inf = 0.0, 0, 0.0, 0
    for note in NOTES12:
        idxs = [i for i, nm in enumerate(notes) if nm == note]
        means = [result["positions"][i]["dev_cents"] for i in idxs]
        counts = [len(result["positions"][i]["values"]) for i in idxs
                  if result["positions"][i]["dev_cents"] is not None]
        means = [m for m in means if m is not None]
        if len(means) >= 2:
            inflate += sum(1.0 / c for c in counts) / len(counts)
            n_inf += 1
        info = {
            "copies": len(idxs),
            "measured": len(means),
            "dev_cents": _mean(means) if means else None,
            "spread_cents": _sd(means),
        }
        result["notes"][note] = info
        if info["spread_cents"] is not None:
            ss_f += info["spread_cents"] ** 2 * (len(means) - 1)
            dof_f += len(means) - 1
    result["forming_sd_cents"] = math.sqrt(ss_f / dof_f) if dof_f else None
    result["forming_dof"] = dof_f

    # 造形のばらつきから、吹き方のばらつきが混ざるぶんを差し引く。
    # 本ごとに吹鳴の回数が違うので、1/n の平均を使って水増し分を見積もる。
    corrected = None
    if result["forming_sd_cents"] is not None and result["blow_sd_cents"] is not None:
        share = inflate / n_inf if n_inf else 1.0
        var = result["forming_sd_cents"] ** 2 - result["blow_sd_cents"] ** 2 * share
        corrected = math.sqrt(var) if var > 0 else 0.0
    result["forming_sd_corrected"] = corrected

    # 系統的なずれ。全音に共通する分（復号では基準笛との比で自動的に消える）と、
    # 音によって違う分（実害があるのはこちら）に分ける。
    devs = [i["dev_cents"] for i in result["notes"].values() if i["dev_cents"] is not None]
    result["common_offset_cents"] = _mean(devs) if devs else None
    if devs:
        off = result["common_offset_cents"]
        residual = {
            nm: i["dev_cents"] - off
            for nm, i in result["notes"].items()
            if i["dev_cents"] is not None
        }
        result["note_dependent"] = residual
        result["note_dependent_rms"] = math.sqrt(_mean([v * v for v in residual.values()]))
        result["note_dependent_max"] = max(residual.items(), key=lambda kv: abs(kv[1]))
    else:
        result["note_dependent"] = {}
        result["note_dependent_rms"] = None
        result["note_dependent_max"] = None

    # G7 が使えるか。3本とも鳴り、かつ狙いから±50セント以内であることを条件にする。
    # ただし全音に共通するずれは基準笛との比で消えるので、共通分を引いた残りで判定する
    # （較正がずれているだけの状態を、G7 が使えないと誤って判定しないため）。
    off = result["common_offset_cents"] or 0.0
    g7_idx = [i for i, nm in enumerate(notes) if nm == "G7"]
    sounded = [result["positions"][i] for i in g7_idx if result["positions"][i]["values"]]
    result["g7"] = {
        "copies": len(g7_idx),
        "sounded": len(sounded),
        "dev_cents": [e["dev_cents"] for e in sounded],
        "resid_cents": [e["dev_cents"] - off for e in sounded],
        "ok": len(sounded) == len(g7_idx)
        and all(abs(e["dev_cents"] - off) <= 50.0 for e in sounded),
    }

    # 較正定数の再推定。設計時の管長は現行の A,e から決まっているので、それを説明変数にする。
    pairs = []
    for i, e in enumerate(result["positions"]):
        if e["mean"] is None:
            continue
        note = notes[i]
        L = (lengths or {}).get(note, length_for_note(note))
        pairs.append((L, e["mean"]))
    result["fit_used_measured_lengths"] = bool(lengths)
    if len(pairs) >= 3:
        a_new, e_new, rms = fit_calibration(pairs)
        result["fit"] = {"A": a_new, "e": e_new, "rms_cents": rms, "n": len(pairs)}
    else:
        result["fit"] = None
    return result


def format_report(res):
    """集計結果を日本語の報告文にする。"""
    out = []
    w = out.append
    w("較正コーム36本の集計（吹鳴%d回ぶん）" % res["n_passes"])
    w("")
    w("[位置ごとの測定値]")
    w("  番号 音名   測定値                     狙いからのずれ  吹鳴ばらつき")
    for e in res["positions"]:
        vals = " ".join("%6.1f" % v for v in e["values"]) or "（鳴らず）"
        dev = "%+7.1f" % e["dev_cents"] if e["dev_cents"] is not None else "      -"
        sd = "%6.1f" % e["sd_cents"] if e["sd_cents"] is not None else "     -"
        w("  %3d  %-4s %-26s %s cent  %s cent" % (e["index"], e["note"], vals, dev, sd))
    w("")
    w("[音ごとの集計（同じ音の3本）]")
    w("  音名   本数 鳴った  平均のずれ   3本の散らばり")
    for note in NOTES12:
        i = res["notes"][note]
        dev = "%+7.1f" % i["dev_cents"] if i["dev_cents"] is not None else "      -"
        sp = "%6.1f" % i["spread_cents"] if i["spread_cents"] is not None else "     -"
        w("  %-4s   %2d   %2d    %s cent  %s cent" % (note, i["copies"], i["measured"], dev, sp))
    w("")
    if res["dead"]:
        w("[鳴らなかった位置（造形不良）]")
        w("  %d本／36本。%s" %
          (len(res["dead"]), "、".join("%d番(%s)" % d for d in res["dead"])))
        thin = [n for n in NOTES12 if res["notes"][n]["measured"] < 2]
        if thin:
            w("  残りが1本以下で3本の散らばりを出せない音: %s" % "、".join(thin))
        w("")
    w("[指標]")
    if res["blow_sd_cents"] is not None:
        w("  吹き方のばらつき: %.1f セント（自由度%d）" % (res["blow_sd_cents"], res["blow_dof"]))
    if res["forming_sd_cents"] is not None:
        w("  造形のばらつき  : %.1f セント（自由度%d、そのまま）" %
          (res["forming_sd_cents"], res["forming_dof"]))
    if res["forming_sd_corrected"] is not None:
        if res["forming_sd_corrected"] <= 0.0:
            w("  造形のばらつき  : 吹き方のばらつきに埋もれて検出できない")
            w("      → 本どうしの散らばりは、吹き方のばらつきだけで説明がつく大きさである。")
            w("      → 造形のばらつきは多くとも %.1f セント程度と言える（それ以上の主張はできない）。"
              % res["forming_sd_cents"])
            w("      → 50セント刻みには有利な結果だが、確かめるには吹き方のばらつきを"
              "小さくした測り直しが要る。")
        else:
            w("  造形のばらつき  : %.1f セント（吹き方のばらつきを差し引いた値）" %
              res["forming_sd_corrected"])
            if res["forming_sd_corrected"] <= 12.0:
                w("      → 10セント前後なので、50セント刻みが成立する見込みである。")
            else:
                w("      → 10セント前後より大きいので、50セント刻みは危うい。")
    if res["common_offset_cents"] is not None:
        w("  全音に共通するずれ: %+.1f セント（基準笛との比で読むので復号では消える）" %
          res["common_offset_cents"])
        w("  音によって違うずれ: %.1f セント（実効値）、最大は %s の %+.1f セント" %
          (res["note_dependent_rms"], res["note_dependent_max"][0], res["note_dependent_max"][1]))
        if res["note_dependent_rms"] <= 15.0:
            w("      → ずれはほぼ全音一律なので、較正定数を直すだけで済む。")
        else:
            w("      → 音によってずれ方が違うので、f=A/(L+e) の式そのものを見直す必要がある。")
    g7 = res["g7"]
    detail = "、".join("%+.1f" % c for c in g7["resid_cents"]) or "なし"
    w("  G7: %d本中%d本が鳴った。共通のずれを引いた残りは %s セントである。" %
      (g7["copies"], g7["sounded"], detail))
    w("      → %s" %
      ("3本とも±50セント以内なので、12スロット体系を既定へ昇格できる。"
       if g7["ok"] else "条件を満たさないので、11スロット体系に留めるのが安全である。"))
    if res["fit"]:
        f = res["fit"]
        w("")
        w("[較正定数の再推定]")
        w("  現行 A=%.1f e=%.3f" % (CALIB_A, CALIB_E))
        w("  再推定 A=%.1f e=%.3f（%d本で当てはめ、残差の実効値 %.1f セント、管長は%s）" %
          (f["A"], f["e"], f["n"], f["rms_cents"],
           "実測値" if res.get("fit_used_measured_lengths") else "設計値"))
        w("  out/cipher_mini10_calib.txt をこの値へ書き換えると、以後の笛がこの較正で刷られる。")
    return "\n".join(out)


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    opts = [a for a in argv[1:] if a.startswith("--")]
    if not args:
        print(__doc__)
        return 1
    first, last = 1, len(LAYOUT)
    for o in opts:
        if o.startswith("--range="):
            lo, _, hi = o.split("=", 1)[1].partition("-")
            first, last = int(lo), int(hi)
        else:
            print("知らないオプション: %s" % o)
            return 1
    with open(args[0], encoding="utf-8") as fp:
        text = fp.read()
    res = analyze(parse_measurements(text, first=first, last=last))
    print(format_report(res))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
