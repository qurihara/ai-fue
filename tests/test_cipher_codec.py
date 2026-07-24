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

from fue.cipher_codec import (CodecConfig, _from_base, _payload_width,
                              _rs_decode, _rs_encode, _to_base,
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
