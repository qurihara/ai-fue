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

CASES = [
    dict(parity=2, mode="sequential", payload_hex="a5"),
    dict(parity=2, mode="sequential", payload_hex="00112233"),
    dict(parity=2, mode="sequential", payload_hex=bytes(range(16)).hex()),
    dict(parity=2, mode="sequential", payload_hex="0000a5"),
    dict(parity=0, mode="sequential", payload_hex="00112233"),
    dict(parity=0, mode="symbols", symbols=[3, 1, 4, 1, 5, 9]),
]


def main() -> int:
    config_path = ROOT / "docs" / "cipher_config.json"
    with config_path.open(encoding="utf-8") as src:
        base = json.load(src)
    vectors = []
    for index, case in enumerate(CASES):
        cfg = CodecConfig(**{**base, "ecc_parity": case["parity"],
                             "mode": case["mode"]})
        if case["mode"] == "symbols":
            encoded = encode_symbols(case["symbols"], cfg)
        else:
            encoded = encode(bytes.fromhex(case["payload_hex"]), cfg)
        measured = simulate(encoded.notes, cfg, common_mode_pct=3,
                            per_flute_sigma_cents=10, seed=20260723 + index)
        vector = {"parity": case["parity"], "mode": case["mode"],
                  "measured_freqs": measured}
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
    with (ROOT / "docs" / "cipher_test_vectors.json").open("w", encoding="utf-8") as dst:
        json.dump(output, dst, ensure_ascii=False, indent=2)
        dst.write("\n")
    print(f"generated {len(vectors)} vectors")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
