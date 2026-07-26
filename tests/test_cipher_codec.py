"""暗号笛コーデックの単体テスト。

pytestがあればpytestで、無ければ内蔵シムで
`python3 tests/test_cipher_codec.py` により全テストが走る。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np

try:
    import pytest
    _HAVE_PYTEST = True
except ImportError:  # pytest互換の最小シムを内部定義する。
    _HAVE_PYTEST = False

    class _Raises:
        def __init__(self, exc):
            self.exc = exc

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            if exc_type is None:
                raise AssertionError("%r が送出されなかった" % self.exc)
            return issubclass(exc_type, self.exc)

    class _Mark:
        @staticmethod
        def parametrize(argnames, argvalues):
            def deco(fn):
                fn._parametrize = (argnames, list(argvalues))
                return fn
            return deco

    class pytest:  # noqa: N801 - pytest互換名
        raises = _Raises
        mark = _Mark

from fue import cipher_codec
from fue.cipher_codec import (CodecConfig, _from_base, _payload_width,
                              _rs_decode, _rs_encode, _to_base, _wire_params,
                              _width_to_bytes, decode, encode, encode_symbols,
                              ref_slot_index, simulate, slots)


def test_slots_and_reference_validation():
    assert len(slots(CodecConfig())) == 13            # F#6..F#7 半音13
    assert len(slots(CodecConfig(step_cents=50))) == 25
    CodecConfig(reference_note="E6")                                            # 音域外の基準も許可(データ域外だが格子上ならOK)
    with pytest.raises(ValueError): CodecConfig(step_cents=250)                 # 1200cが250で割り切れない
    with pytest.raises(ValueError): CodecConfig(step_cents=200, reference_note="A6")  # A6が200c格子外


@pytest.mark.parametrize("payload", [b"", b"\0", b"\1", b"\0\xff", b"abc"])
def test_noiseless_roundtrip(payload):
    cfg = CodecConfig(); enc = encode(payload, cfg)
    assert decode(simulate(enc.notes, cfg), cfg).payload == payload


@pytest.mark.parametrize("payload", [b"", b"\0", b"\1", b"\0\xff", b"abc"])
def test_noiseless_roundtrip_parity0(payload):
    cfg = CodecConfig(ecc_parity=0); enc = encode(payload, cfg)
    result = decode(simulate(enc.notes, cfg), cfg)
    assert result.status == "ok" and result.payload == payload


def test_common_mode_relative_only():
    cfg = CodecConfig(); enc = encode(b"\xa5", cfg)
    measured = simulate(enc.notes, cfg, common_mode_pct=3)
    assert decode(measured, cfg).payload == b"\xa5"
    table = slots(cfg)
    absolute = [min(range(len(table)), key=lambda i: abs(f - table[i].freq_hz)) for f in measured[1:]]
    assert absolute != enc.symbols


def test_rs_errors_and_erasures():
    original = _rs_encode([1, 2, 3, 4, 5], 4, 13)
    bad = original.copy(); bad[1] = (bad[1] + 3) % 13; bad[6] = (bad[6] + 4) % 13
    assert _rs_decode(bad, 4, 13)[0] == original
    bad = original.copy()
    for i in (0, 2, 5, 8): bad[i] = (bad[i] + i + 1) % 13
    assert _rs_decode(bad, 4, 13, {0, 2, 5, 8})[0] == original


def test_fixed_width_leading_zeroes():
    for value in (0, 1, 10, 11, 120, 12345): assert _from_base(_to_base(value, 11), 11) == value
    cfg = CodecConfig()
    for payload in (b"\0", b"\0\0", b"\0\1", b"\0\0\xa5", b"\0\0\xff"):
        enc = encode(payload, cfg)
        assert decode(simulate(enc.notes, cfg), cfg).payload == payload


def test_width_maps_bytes_one_to_one():
    widths = [_payload_width(b, 11) for b in range(64)]
    assert widths[:5] == [0, 3, 5, 7, 10]
    assert sorted(set(widths)) == widths  # 狭義単調増加=一対一
    for b, d in enumerate(widths):
        assert _width_to_bytes(d, 11) == b


def test_invalid_symbol_count_raises():
    for bad_width in (1, 2, 4, 6):
        with pytest.raises(ValueError): _width_to_bytes(bad_width, 13)
    # RS的には正しいがデータ記号数d=1が不正な笛列はerror状態になる。
    cfg = CodecConfig(ecc_parity=2)
    wire = _rs_encode([5], 2, 13)
    result = decode(simulate([ref_slot_index(cfg)] + wire, cfg), cfg)
    assert result.status.startswith("error:") and "データ記号数が不正" in result.status


@pytest.mark.parametrize("parity", [0, 2])
def test_symbols_mode_roundtrip(parity):
    secret = [3, 1, 4, 1, 5, 9]
    cfg = CodecConfig(mode="symbols", ecc_parity=parity)
    enc = encode_symbols(secret, cfg)
    assert len(enc.symbols) == len(secret) + parity
    result = decode(simulate(enc.notes, cfg), cfg)
    assert result.status == "ok"
    assert result.symbols == secret and result.payload == b""
    with pytest.raises(ValueError): encode_symbols([13], cfg)
    with pytest.raises(ValueError): encode_symbols([-1], cfg)


def test_symbols_mode_corrects_one_error():
    secret = [3, 1, 4, 1]
    cfg = CodecConfig(mode="symbols", ecc_parity=2)
    enc = encode_symbols(secret, cfg)
    damaged = enc.symbols.copy()
    damaged[2] = (damaged[2] + 5) % enc.m
    result = decode(simulate([ref_slot_index(cfg)] + damaged, cfg), cfg)
    assert result.status == "corrected" and result.symbols == secret


@pytest.mark.parametrize("size", [4, 8, 16, 32, 64])
def test_interleaved_blocks_roundtrip(size):
    cfg = CodecConfig()
    patterns = [bytes((i * 37 + 11) % 256 for i in range(size)),
                np.random.default_rng(20260721 + size).bytes(size)]
    for payload in patterns:
        enc = encode(payload, cfg)
        assert decode(simulate(enc.notes, cfg), cfg).payload == payload


def test_interleaved_blocks_common_mode_relative_only():
    cfg = CodecConfig()
    payload = bytes(range(16))
    enc = encode(payload, cfg)
    assert decode(simulate(enc.notes, cfg, common_mode_pct=3), cfg).payload == payload


def test_one_error_in_each_rs_block():
    cfg = CodecConfig(ecc_parity=2)
    payload = bytes(range(32))
    enc = encode(payload, cfg)
    damaged = enc.codeword.copy()
    for start in range(0, len(damaged), enc.p - 1):
        damaged[start] = (damaged[start] + 1) % enc.p
    wire = [d for value in damaged
            for d in _to_base(value, enc.m, enc.field_width)]
    frequencies = [simulate([cfg.reference_note], cfg)[0]] + simulate(wire, cfg)
    assert decode(frequencies, cfg).payload == payload


def _no_repeat_cfg(**kw):
    """隣り合う笛が同じ音にならない設定。"""
    return CodecConfig(no_repeat=True, **kw)


def _damaged_freqs(enc, cfg, index, step=1):
    """データ笛1本だけを隣のスロットへ読み違えた周波数列を作る。"""
    damaged = list(enc.symbols)
    damaged[index] = (damaged[index] + step) % enc.m
    return simulate([cfg.reference_note], cfg) + simulate(damaged, cfg)


@pytest.mark.parametrize("payload", [b"", b"\1", b"\0\xff", bytes(range(8)), bytes(range(16))])
def test_no_repeat_roundtrip(payload):
    cfg = _no_repeat_cfg()
    enc = encode(payload, cfg)
    result = decode(simulate(enc.notes, cfg), cfg)
    assert not result.status.startswith("error:") and result.payload == payload


def test_no_repeat_symbols_mode_roundtrip():
    cfg = _no_repeat_cfg(mode="symbols")
    mb = _wire_params(cfg)[1]                       # 記号の上限(m=13ならp=11)
    secret = [3, 1, 4, 1, 5, 9, 2, 6]
    enc = encode_symbols(secret, cfg)
    result = decode(simulate(enc.notes, cfg), cfg)
    assert result.status == "ok" and result.symbols == secret
    with pytest.raises(ValueError): encode_symbols([mb], cfg)     # 差分値の上限を超える記号
    with pytest.raises(ValueError): encode_symbols([-1], cfg)


def test_no_repeat_never_repeats_a_note():
    """基準笛と1本目の間も含め、隣り合う笛が同じ音にならない。"""
    cfg, rng = _no_repeat_cfg(), np.random.default_rng(20260726)
    m = len(slots(cfg))
    for _ in range(100):
        payload = rng.bytes(int(rng.integers(1, 17)))
        enc = encode(payload, cfg)
        assert enc.notes[0] == cfg.reference_note
        slot_seq = [ref_slot_index(cfg) % m] + enc.symbols
        assert all(a != b for a, b in zip(slot_seq, slot_seq[1:]))
        assert all(a != b for a, b in zip(enc.notes, enc.notes[1:]))
        assert decode(simulate(enc.notes, cfg), cfg).payload == payload


def test_no_repeat_corrects_any_single_misread():
    cfg, payload = _no_repeat_cfg(), bytes(range(1, 9))
    enc = encode(payload, cfg)
    for index in range(len(enc.symbols)):
        result = decode(_damaged_freqs(enc, cfg, index), cfg)
        assert result.payload == payload, "笛%dの読み違いを訂正できない" % index


def test_no_repeat_interleave_is_required():
    """インターリーブを外すと、1本の読み違いが同一ブロックの2記号を壊し訂正できない。"""
    cfg, payload = _no_repeat_cfg(), bytes(range(1, 9))
    enc = encode(payload, cfg)
    original = cipher_codec._interleave_order
    try:  # 送出順を混ぜない版に差し替えて符号化・復号する。
        cipher_codec._interleave_order = lambda sizes: list(range(sum(sizes)))
        plain = encode(payload, cfg)
        failures = [i for i in range(len(plain.symbols))
                    if decode(_damaged_freqs(plain, cfg, i), cfg).payload != payload]
    finally:
        cipher_codec._interleave_order = original
    assert failures, "インターリーブ無しでも全て訂正できてしまう"
    assert all(decode(_damaged_freqs(enc, cfg, i), cfg).payload == payload
               for i in failures)


def test_no_repeat_needs_reference():
    with pytest.raises(ValueError): CodecConfig(no_repeat=True, use_reference=False)


# --- 12スロット体系 G#6..G7（復号ページの既定・no_repeatの本命） ---

def _deck12(**kw):
    """12スロット体系(G#6..G7)の設定。差分値がm-1=11通りでGF(11)がそのまま使える。"""
    return CodecConfig(lo_note="G#6", hi_note="G7", reference_note="C7",
                       no_repeat=True, **kw)


def _deck11(**kw):
    """従来の11スロット体系(G#6..F#7)。印刷済みのカード・スプールが使う。"""
    return CodecConfig(lo_note="G#6", hi_note="F#7", reference_note="C7", **kw)


def test_deck12_uses_gf11_at_full_rate():
    """12スロットのno_repeatはGF(11)・笛1本=記号1個・log2(11)bitになる。"""
    cfg = _deck12()
    assert [s.nearest_note for s in slots(cfg)][-1] == "G7"
    m, mb, wb, p, w = _wire_params(cfg)
    assert (m, mb, wb, p, w) == (12, 11, 11, 11, 1)
    assert abs(cipher_codec.symbol_bits(cfg) - np.log2(11)) < 1e-12
    # ブロック長(p-1)とパリティ効率が、制約なしの11スロット体系と完全に同じであること。
    assert p - 1 == _wire_params(_deck11())[3] - 1 == 10


@pytest.mark.parametrize("payload", [b"", b"\1", b"\0\xff", b"abc", bytes(range(8)),
                                     bytes(range(16))])
def test_deck12_no_repeat_roundtrip(payload):
    cfg = _deck12()
    enc = encode(payload, cfg)
    result = decode(simulate(enc.notes, cfg), cfg)
    assert not result.status.startswith("error:") and result.payload == payload


def test_deck12_no_repeat_symbols_roundtrip():
    cfg = _deck12(mode="symbols")
    secret = [3, 1, 4, 1, 5, 9, 2, 6, 10, 0]
    enc = encode_symbols(secret, cfg)
    result = decode(simulate(enc.notes, cfg), cfg)
    assert result.status == "ok" and result.symbols == secret
    with pytest.raises(ValueError): encode_symbols([11], cfg)   # 記号はGF(11)の0..10


@pytest.mark.parametrize("bits_and_flutes", [(24, 10), (64, 26), (128, 49)])
def test_deck12_flute_counts_match_unconstrained_11(bits_and_flutes):
    """本数(基準笛込み)が、制約なしの11スロット体系と同じであること。"""
    bits, expected = bits_and_flutes
    payload = bytes(range(bits // 8))
    assert len(encode(payload, _deck12()).notes) == expected
    assert len(encode(payload, _deck11()).notes) == expected


def test_deck12_no_repeat_never_repeats_a_note():
    """基準笛と1本目の間も含め、隣り合う笛が同じ音にならない(ランダム100通り)。"""
    cfg, rng = _deck12(), np.random.default_rng(20260726)
    m = len(slots(cfg))
    for _ in range(100):
        payload = rng.bytes(int(rng.integers(1, 17)))
        enc = encode(payload, cfg)
        assert enc.notes[0] == cfg.reference_note
        slot_seq = [ref_slot_index(cfg) % m] + enc.symbols
        assert all(a != b for a, b in zip(slot_seq, slot_seq[1:]))
        assert all(a != b for a, b in zip(enc.notes, enc.notes[1:]))
        assert decode(simulate(enc.notes, cfg), cfg).payload == payload


def test_deck12_no_repeat_corrects_any_single_misread():
    cfg, payload = _deck12(), bytes(range(1, 9))
    enc = encode(payload, cfg)
    for index in range(len(enc.symbols)):
        result = decode(_damaged_freqs(enc, cfg, index), cfg)
        assert result.payload == payload, "笛%dの読み違いを訂正できない" % index


def test_deck12_interleave_is_required():
    """インターリーブを外すと、1本の読み違いが同一ブロックの2記号を壊し訂正できない。"""
    cfg, payload = _deck12(), bytes(range(1, 9))
    enc = encode(payload, cfg)
    original = cipher_codec._interleave_order
    try:
        cipher_codec._interleave_order = lambda sizes: list(range(sum(sizes)))
        plain = encode(payload, cfg)
        failures = [i for i in range(len(plain.symbols))
                    if decode(_damaged_freqs(plain, cfg, i), cfg).payload != payload]
    finally:
        cipher_codec._interleave_order = original
    assert failures, "インターリーブ無しでも全て訂正できてしまう"
    assert all(decode(_damaged_freqs(enc, cfg, i), cfg).payload == payload
               for i in failures)


def test_legacy_11_slot_printed_items_still_decode():
    """印刷済みの11スロット体系(?hi=F#7)がそのまま読めること。"""
    card = _deck11(mode="symbols", ecc_parity=0)
    enc = encode_symbols([2, 0, 2, 6, 7, 2, 4], card)
    assert decode(simulate(enc.notes, card), card).symbols == [2, 0, 2, 6, 7, 2, 4]
    spool = _deck11(ecc_parity=2)
    enc = encode(b"pass_#26", spool)
    assert len(enc.notes) == 26
    assert decode(simulate(enc.notes, spool), spool).payload == b"pass_#26"


def _run_all():
    """シム実行用の最小ランナー。parametrizeを展開して全テストを回す。"""
    failures, count = [], 0
    for name in sorted(k for k in globals() if k.startswith("test_")):
        fn = globals()[name]
        params = getattr(fn, "_parametrize", None)
        calls = ([(repr(v), {params[0]: v}) for v in params[1]]
                 if params else [("", {})])
        for label, kwargs in calls:
            count += 1
            try:
                fn(**kwargs)
                print("PASS %s%s" % (name, "[%s]" % label if label else ""))
            except Exception as exc:  # noqa: BLE001 - 失敗を集計する
                failures.append((name, label, exc))
                print("FAIL %s%s: %r" % (name, "[%s]" % label if label else "", exc))
    print("%d passed, %d failed" % (count - len(failures), len(failures)))
    return 1 if failures else 0


if __name__ == "__main__":
    if _HAVE_PYTEST:
        sys.exit(pytest.main([__file__, "-v"]))
    sys.exit(_run_all())
