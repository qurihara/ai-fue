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
