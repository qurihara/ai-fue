"""CipherFlute 往復デモ：小さな秘密を符号化→（印刷用STL生成）→復号→ハッシュ照合。

既定のテスト秘密は記号列モードの [2,0,2,6]（今年の西暦「2026」・パリティ0）。
mini10ヘッド・13スロット（F#6〜F#7・基準C7）・CipherFlute専用較正（out/cipher_mini10_calib.txt）で作る。

  python3 fue/roundtrip_demo.py                 # 既定=2026・記号列・パリティ0
  python3 fue/roundtrip_demo.py --symbols 7,0,10,2
  python3 fue/roundtrip_demo.py --payload-hex a5 --parity 2
  python3 fue/roundtrip_demo.py --no-stl        # STL生成を省く（trimesh不要）

照合はハッシュ自己検証：秘密の正準バイト列（記号列は bytes(symbols)、バイト列はそのまま）の
SHA-256 を照合子とし、復号した秘密のSHA-256と一致すれば成功。基準笛は先頭なので
positions_known=True で復号する。印刷後はこのSTLを吹いて測定Webアプリで復号・照合する。
"""
from __future__ import annotations
import argparse
import hashlib
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from cipher_codec import (CodecConfig, encode, encode_symbols, decode, simulate,
                          slots, note_to_freq)

OUT = os.path.join(os.path.dirname(__file__), os.pardir, "out")


def _canonical_bytes(mode, symbols, payload):
    """秘密の正準バイト列（ハッシュ対象）。記号列は各記号1バイト、バイト列はそのまま。"""
    return bytes(symbols) if mode == "symbols" else payload


def run(symbols=None, payload=None, parity=0, make_stl=True,
        stem="cipher_roundtrip_demo", seed=2026):
    mode = "symbols" if symbols is not None else "sequential"
    cfg = CodecConfig(mode=mode, ecc_parity=parity)
    if mode == "symbols":
        enc = encode_symbols(symbols, cfg)
        secret_repr = ",".join(map(str, symbols))
    else:
        enc = encode(payload, cfg)
        secret_repr = payload.hex()
    verifier = hashlib.sha256(_canonical_bytes(mode, symbols, payload)).hexdigest()

    # 往復検証（シミュレーション・印刷なしで通す）：共通モード+3%・差動σ10。
    measured = simulate(enc.notes, cfg, common_mode_pct=3, per_flute_sigma_cents=10, seed=seed)
    dec = decode(measured, cfg, positions_known=True)
    got_bytes = _canonical_bytes(mode, dec.symbols, dec.payload)
    ok = (dec.status in ("ok", "corrected")
          and hashlib.sha256(got_bytes).hexdigest() == verifier)

    table = slots(cfg)
    lines = ["CipherFlute 往復デモ", "秘密(%s): %s" % (mode, secret_repr),
             "SHA-256 照合子: %s" % verifier,
             "笛 %d本（基準笛C7が先頭）: %s" % (len(enc.notes), " ".join(enc.notes)),
             "", "位置  音    目標周波数[Hz]  役割"]
    for i, n in enumerate(enc.notes):
        role = "基準笛" if i == 0 else "データ"
        lines.append("%2d   %-4s %8.0f       %s" % (i + 1, n, note_to_freq(n), role))
    lines.append("")
    lines.append("往復検証(シミュレーション): %s" % ("成功（ハッシュ一致）" if ok else "失敗"))

    if make_stl:
        try:
            import mini10
            comb, infos = mini10.build_calib_comb(list(enc.notes))
            os.makedirs(OUT, exist_ok=True)
            path = os.path.join(OUT, stem + ".stl")
            comb.export(path)
            lines.append("印刷用STL: out/%s.stl 外形=%s watertight=%s"
                         % (stem, tuple(round(x, 1) for x in comb.extents), comb.is_watertight))
        except Exception as exc:  # trimesh 不在など
            lines.append("STL生成は省略（%s）。--no-stl か trimeshのある環境で。" % exc)

    info = "\n".join(lines)
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, stem + "_info.txt"), "w") as f:
        f.write(info + "\n")
    print(info)
    return ok


def main(argv=None):
    ap = argparse.ArgumentParser(description="CipherFlute 往復デモ")
    ap.add_argument("--symbols", default="2,0,2,6",
                    help="記号列モードの秘密（0..12をカンマ区切り。既定=2,0,2,6＝2026）")
    ap.add_argument("--payload-hex", default=None, help="バイト列モードの秘密（hex）。指定すると記号列より優先")
    ap.add_argument("--parity", type=int, default=0, help="誤り訂正のパリティ本数（既定0＝なし）")
    ap.add_argument("--no-stl", action="store_true", help="STL生成を省く")
    args = ap.parse_args(argv)
    if args.payload_hex is not None:
        ok = run(payload=bytes.fromhex(args.payload_hex), parity=args.parity,
                 make_stl=not args.no_stl)
    else:
        symbols = [int(x) for x in args.symbols.split(",") if x.strip() != ""]
        ok = run(symbols=symbols, parity=args.parity, make_stl=not args.no_stl)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
