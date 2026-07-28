"""較正コーム36本の集計が、既知の答えを持つ合成データで正しい値を出すかを確かめる。"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "fue"))
import calib_comb as cc


def test_layout_has_no_adjacent_duplicates():
    """隣り合う位置が同じ音になっていないこと（音の変わり目で区切れる前提）。"""
    assert len(cc.LAYOUT) == 36
    for a, b in zip(cc.LAYOUT, cc.LAYOUT[1:]):
        assert a != b
    for note in cc.NOTES12:
        assert cc.LAYOUT.count(note) == 3


def test_parse_blocks_and_missing():
    text = """
# 1回目
1661 1760 1865 1976 2093 2217 2349 2489 2637 2794 2960 3136
1661 1760 1865 1976 2093 2217 2349 2489 2637 2794 2960 3136
1661 1760 1865 1976 2093 2217 2349 2489 2637 2794 2960 3136

# 2回目（1本鳴らず）
- 1760 1865 1976 2093 2217 2349 2489 2637 2794 2960 3136
1661 1760 1865 1976 2093 2217 2349 2489 2637 2794 2960 3136
1661 1760 1865 1976 2093 2217 2349 2489 2637 2794 2960 3136
"""
    passes = cc.parse_measurements(text)
    assert len(passes) == 2
    assert passes[1][0] is None
    assert passes[0][0] == 1661.0


def test_parse_rejects_wrong_count():
    try:
        cc.parse_measurements("1000 1100 1200")
    except ValueError:
        return
    raise AssertionError("36個でない入力は例外にならなければならない")


def _synth(offset_cents, forming_sd, blow_sd, n_passes=3, seed=1):
    """狙いの周波数に、共通のずれ・造形のばらつき・吹き方のばらつきを載せた合成データを作る。"""
    rng = random.Random(seed)
    form = [rng.gauss(0.0, forming_sd) for _ in cc.LAYOUT]  # 1本ごとに固定のずれ
    passes = []
    for _ in range(n_passes):
        row = []
        for i, note in enumerate(cc.LAYOUT):
            c = offset_cents + form[i] + rng.gauss(0.0, blow_sd)
            row.append(cc.note_to_freq(note) * 2 ** (c / 1200.0))
        passes.append(row)
    return passes


def test_common_offset_is_recovered():
    """全音一律のずれを入れたら、共通分としてほぼそのまま出て、音依存分は小さいこと。"""
    res = cc.analyze(_synth(offset_cents=80.0, forming_sd=0.0, blow_sd=0.0))
    assert abs(res["common_offset_cents"] - 80.0) < 0.5
    assert res["note_dependent_rms"] < 0.5


def test_blow_and_forming_are_separated():
    """吹き方のばらつきと造形のばらつきを別々に入れたら、別々に取り出せること。"""
    res = cc.analyze(_synth(offset_cents=0.0, forming_sd=12.0, blow_sd=8.0,
                            n_passes=6, seed=7))
    assert 4.0 < res["blow_sd_cents"] < 13.0
    assert 6.0 < res["forming_sd_corrected"] < 20.0
    # 補正値は、そのままの値より小さいか同じであること（吹き方のぶんを引くので）。
    assert res["forming_sd_corrected"] <= res["forming_sd_cents"] + 1e-9


def test_forming_correction_handles_uneven_pass_counts():
    """本によって吹鳴の回数が違っても、造形のばらつきの補正が壊れないこと。

    以前は「いちばん少ない回数」で補正していたため、1回しか吹いていない本が
    1つでもあると差し引きが過大になり、造形のばらつきが0と出てしまった。
    """
    passes = _synth(offset_cents=0.0, forming_sd=14.0, blow_sd=6.0, n_passes=3, seed=11)
    for row in passes[1:]:                       # 一部の本は1回しか吹いていない
        for i in range(0, 36, 3):
            row[i] = None
    res = cc.analyze(passes)
    assert res["forming_sd_corrected"] > 5.0, res["forming_sd_corrected"]
    assert res["forming_sd_corrected"] <= res["forming_sd_cents"]


def test_fit_can_use_measured_lengths():
    """実測した管長を渡すと、そちらで当てはめること。

    外見統一のコームでは、いちばん低い音の空洞が外形の長さに頭打ちされて設計より
    短くなる。実測値で当てはめれば、その本だけ高く鳴るのは造形の問題だと分かり、
    較正の式そのものを疑わずに済む。
    """
    short = 1.6                                   # G#6 だけ管長が足りない
    lengths = {n: cc.length_for_note(n) for n in cc.NOTES12}
    lengths["G#6"] -= short
    passes = [[cc.CALIB_A / (lengths[n] + cc.CALIB_E) for n in cc.LAYOUT]]
    naive = cc.analyze(passes)["fit"]
    aware = cc.analyze(passes, lengths=lengths)["fit"]
    assert aware["rms_cents"] < 0.5               # 実測値なら現行の定数がそのまま出る
    assert abs(aware["A"] - cc.CALIB_A) / cc.CALIB_A < 1e-3
    assert naive["rms_cents"] > aware["rms_cents"] * 5


def test_g7_judgement():
    """G7が3本とも狙いに近ければ合格、1本でも欠ければ不合格になること。"""
    ok = cc.analyze(_synth(offset_cents=0.0, forming_sd=5.0, blow_sd=3.0))
    assert ok["g7"]["ok"]

    passes = _synth(offset_cents=0.0, forming_sd=5.0, blow_sd=3.0)
    g7_pos = cc.LAYOUT.index("G7")
    for row in passes:
        row[g7_pos] = None
    ng = cc.analyze(passes)
    assert not ng["g7"]["ok"]
    assert ng["g7"]["sounded"] == 2


def test_fit_recovers_known_constants():
    """既知の A,e から作った周波数を与えたら、その A,e を当て直せること。"""
    a_true, e_true = 92000.0, -6.0
    pairs = [(cc.length_for_note(n), a_true / (cc.length_for_note(n) + e_true))
             for n in cc.NOTES12]
    a, e, rms = cc.fit_calibration(pairs)
    assert abs(a - a_true) / a_true < 1e-3
    assert abs(e - e_true) < 0.05
    assert rms < 0.1


def test_fit_on_uniform_offset_matches_scaled_A():
    """全音が一律に +100 セントずれた実測なら、e は変わらず A だけが 2^(1/12) 倍になること。"""
    passes = _synth(offset_cents=100.0, forming_sd=0.0, blow_sd=0.0, n_passes=1)
    res = cc.analyze(passes)
    f = res["fit"]
    assert abs(f["e"] - cc.CALIB_E) < 0.2
    assert abs(f["A"] / cc.CALIB_A - 2 ** (1 / 12.0)) < 1e-3


def test_range_fills_dead_ends():
    """両端が造形不良のとき、生きている範囲だけを書いて --range で位置を合わせられること。"""
    body = " ".join("2000" for _ in range(30))
    passes = cc.parse_measurements(body, first=4, last=33)
    assert len(passes[0]) == 36
    assert passes[0][:3] == [None, None, None]
    assert passes[0][33:] == [None, None, None]
    assert passes[0][3] == 2000.0


def test_range_rejects_wrong_count():
    try:
        cc.parse_measurements(" ".join("2000" for _ in range(29)), first=4, last=33)
    except ValueError as e:
        assert "4番から33番" in str(e)
        return
    raise AssertionError("個数が合わない入力は例外にならなければならない")


def test_dead_ends_still_leave_two_copies_per_note():
    """両端4本ずつが死んでも、どの音も2本以上残ること（σを出せる条件）。"""
    for k in (3, 4):
        sub = cc.LAYOUT[k:36 - k]
        for note in cc.NOTES12:
            assert sub.count(note) >= 2, (k, note)
        for a, b in zip(sub, sub[1:]):
            assert a != b  # 音の変わり目で区切れること


def test_dead_positions_are_reported():
    """一度も鳴らなかった位置が造形不良として数え上げられること。"""
    passes = _synth(offset_cents=0.0, forming_sd=5.0, blow_sd=3.0)
    for row in passes:
        for i in list(range(3)) + list(range(33, 36)):
            row[i] = None
    res = cc.analyze(passes)
    assert len(res["dead"]) == 6
    assert res["dead"][0][0] == 1 and res["dead"][-1][0] == 36
    assert res["forming_sd_corrected"] is not None  # 残り2本でも推定は出る
    assert "鳴らなかった位置" in cc.format_report(res)


def test_parses_the_decoder_console_output():
    """復号ページが「終了し復号」で書き出す形を、そのまま読めること。

    形は docs/cipher/index.html の logMeasurements が決めており、そちらは
    docs/cipher/measure_log.test.js で固定してある。ここでは実際に書き出される
    見た目（見出しのコメント行、1行12個、鳴らない笛は -）を写して受け取れるか
    を確かめる。両端が造形不良で4番から33番だけを吹いた場合を想定している。
    """
    text = """
# 2026-07-28 17:20  続けて吹く  30本  うち鳴らず1本  区切り 40セント/220ms
2088.0 2211.0 2343.0 2482.0 2630.0 2786.0 2952.0 - 3313.0 1748.0 1852.0 1962.0
2079.0 2203.0 2334.0 2473.0 2620.0 2776.0 2941.0 3116.0 3302.0 1742.0 1846.0 1956.0
2073.0 2197.0 2327.0 2466.0 2613.0 2768.0

# 2026-07-28 17:23  続けて吹く  30本  区切り 40セント/220ms
2090.0 2213.0 2345.0 2484.0 2632.0 2788.0 2954.0 3130.0 3315.0 1750.0 1854.0 1964.0
2081.0 2205.0 2336.0 2475.0 2622.0 2778.0 2943.0 3118.0 3304.0 1744.0 1848.0 1958.0
2075.0 2199.0 2329.0 2468.0 2615.0 2770.0
"""
    passes = cc.parse_measurements(text, first=4, last=33)
    assert len(passes) == 2
    assert all(len(p) == 36 for p in passes)
    assert passes[0][:3] == [None, None, None] and passes[0][33:] == [None, None, None]
    assert passes[0][3] == 2088.0
    assert passes[0][10] is None      # 11番目の位置が「鳴らず」
    res = cc.analyze(passes)
    assert len(res["dead"]) == 6      # 吹かなかった両端3本ずつ
    assert res["positions"][10]["n_missing"] == 1
    assert cc.format_report(res)


def _blow(notes, offset=65.0):
    return [cc.note_to_freq(n) * 2 ** (offset / 1200.0) for n in notes]


def test_alignment_maps_one_to_one():
    """欠けも分かれもなければ、素直に1対1で対応すること。"""
    meas = _blow(cc.LAYOUT)
    cost, path = cc.align_measurements(meas, cc.LAYOUT)
    assert [k for _, k, _ in path] == ["one"] * 36
    assert cost < 36 * 0.05


def test_alignment_finds_a_silent_flute():
    """鳴らなかった1本を、位置をずらさずに「鳴らず」として拾えること。"""
    meas = _blow(cc.LAYOUT)
    del meas[17]                       # 18番目が鳴らなかった
    cost, path = cc.align_measurements(meas, cc.LAYOUT)
    kinds = [k for _, k, _ in path]
    assert kinds.count("miss") == 1
    assert kinds.index("miss") == 17


def test_alignment_merges_a_split_blow():
    """1本の吹鳴が2つに分かれたとき、まとめて1本として扱えること。"""
    meas = _blow(cc.LAYOUT)
    f = meas[5]
    meas[5:6] = [f * 2 ** (-0.02), f * 2 ** (0.02)]   # 約48セント離れた2つに分かれた
    cost, path = cc.align_measurements(meas, cc.LAYOUT)
    kinds = [k for _, k, _ in path]
    assert kinds.count("split") == 1
    assert kinds.index("split") == 5
    assert len([p for p in path if p[1] != "miss"]) == 36


def test_blow_direction_is_detected():
    """端から端まで吹いたとき、どちらの端から始めたかを測定値から決められること。"""
    d, fwd, rev = cc.blow_direction(_blow(cc.LAYOUT))
    assert d == "forward" and fwd < rev
    d, fwd, rev = cc.blow_direction(_blow(cc.LAYOUT[::-1]))
    assert d == "reverse" and rev < fwd


def test_report_runs():
    res = cc.analyze(_synth(offset_cents=70.0, forming_sd=10.0, blow_sd=8.0))
    text = cc.format_report(res)
    assert "較正コーム36本の集計" in text
    assert "造形のばらつき" in text


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print("ok", fn.__name__)
    print("全%d件が通った" % len(fns))
