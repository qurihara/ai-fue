#!/usr/bin/env python3
"""Python正解実装からブラウザ復号器の共有テストベクタを生成する。

各ベクタはper-vector設定(parity, mode)を持ち、生成時にPython側で
復号往復を検証してから書き出す。
"""
from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fue.cipher_codec import (CodecConfig, decode, encode,  # noqa: E402
                              encode_symbols, simulate)

# 既定は cipher_config.json（12スロット G#6..G7・隣接同音の禁止あり）。論文と作例が
# この体系で、隣り合う値が11通り＝素数になるのでGF(11)がそのまま使え、本数の代償がゼロになる。
#
# ★どのベクタも、音域を config に明示する。★ 既定を変えたときにベクタの意味が
# 黙って変わらないようにするためである。テストはパリティ・方式・隣接同音の禁止を
# ベクタから読むが、音域だけは既定から読むので、ここを空にすると既定に引きずられる。
SLOT11 = {"hi_note": "F#7"}   # 旧体系。印刷済みのカードとスプールがこれで作ってある
SLOT12 = {"hi_note": "G7"}    # 現行

CASES = [
    dict(parity=2, mode="sequential", payload_hex="a5", config=SLOT11),
    dict(parity=2, mode="sequential", payload_hex="00112233", config=SLOT11),
    dict(parity=2, mode="sequential", payload_hex=bytes(range(16)).hex(), config=SLOT11),
    dict(parity=2, mode="sequential", payload_hex="0000a5", config=SLOT11),
    dict(parity=0, mode="sequential", payload_hex="00112233", config=SLOT11),
    dict(parity=0, mode="symbols", symbols=[3, 1, 4, 1, 5, 9], config=SLOT11),
    # 隣接同音を禁じる符号化。12スロットと組み合わせるのが本来の使い方である。
    dict(parity=2, mode="sequential", payload_hex="a5", no_repeat=True,
         config=SLOT12),
    dict(parity=2, mode="sequential", payload_hex=bytes(range(8)).hex(),
         no_repeat=True, config=SLOT12),
    dict(parity=2, mode="sequential", payload_hex=bytes(range(16)).hex(),
         no_repeat=True, config=SLOT12),
    dict(parity=0, mode="symbols", symbols=[3, 1, 4, 1, 5, 6], no_repeat=True,
         config=SLOT12),
    # 実際に印刷した物に対応するケース。カード「2026724」とスプール「pass_#26」。
    # どちらも旧体系で、差分の写像を通していない。
    dict(parity=0, mode="symbols", symbols=[2, 0, 2, 6, 7, 2, 4], config=SLOT11),
    dict(parity=2, mode="sequential", payload_hex=b"pass_#26".hex(), config=SLOT11),
]


def main() -> int:
    config_path = ROOT / "docs" / "cipher" / "cipher_config.json"
    with config_path.open(encoding="utf-8") as src:
        base = json.load(src)
    vectors = []
    for index, case in enumerate(CASES):
        no_repeat = case.get("no_repeat", False)
        overrides = case.get("config", {})
        cfg = CodecConfig(**{**base, **overrides, "ecc_parity": case["parity"],
                             "mode": case["mode"], "no_repeat": no_repeat})
        if case["mode"] == "symbols":
            encoded = encode_symbols(case["symbols"], cfg)
        else:
            encoded = encode(bytes.fromhex(case["payload_hex"]), cfg)
        measured = simulate(encoded.notes, cfg, common_mode_pct=3,
                            per_flute_sigma_cents=10, seed=20260723 + index)
        vector = {"parity": case["parity"], "mode": case["mode"]}
        if no_repeat:
            vector["no_repeat"] = True
        if overrides:
            vector["config"] = dict(overrides)
        vector["measured_freqs"] = measured
        result = decode(measured, cfg)
        if result.status.startswith("error:"):
            raise SystemExit(f"vector {index}: {result.status}")
        if case["mode"] == "symbols":
            if result.symbols != case["symbols"]:
                raise SystemExit(f"vector {index}: symbols roundtrip failed")
            vector["symbols"] = case["symbols"]
            vector["expected_symbols"] = case["symbols"]
        else:
            if result.payload.hex() != case["payload_hex"]:
                raise SystemExit(f"vector {index}: payload roundtrip failed")
            vector["payload_hex"] = case["payload_hex"]
            vector["expected_payload_hex"] = case["payload_hex"]
        vectors.append(vector)
    output = {"config": "cipher_config.json", "vectors": vectors}
    with (ROOT / "docs" / "cipher" / "cipher_test_vectors.json").open("w", encoding="utf-8") as dst:
        json.dump(output, dst, ensure_ascii=False, indent=2)
        dst.write("\n")
    print(f"generated {len(vectors)} vectors")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
