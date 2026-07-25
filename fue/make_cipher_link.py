"""復号ページのデモ用リンクを1本にまとめて作る。

秘匿の考え方は2つある。

第一に、設定を [* URLのフラグメント(#以降)] に置く。フラグメントはサーバへ送られない
ので、GitHub Pages のアクセスログにも、遷移先へ渡る参照元情報にも残らない。ブラウザの
中だけで完結する。

第二に、遷移先URLや成功時の言葉といった中身を、[* 笛の秘密そのものを鍵にして暗号化]し、
c= という一つの値へ畳む。AES-GCM は改ざんも検出するので、取り出せたこと自体が「正しい
秘密を吹いた」証拠になる。照合用のハッシュを別に載せる必要がなく、URLからは何も読めない。

ただし音域や記号の体系（lo, hi, ref, mode, parity）は、復号そのものに要るので暗号化
できない。これらは秘密の値も長さも明かさないが、フラグメントに置くことでサーバには
渡らないようにする。

WebCrypto と互換:
  鍵    = SHA-256(canonical)                 canonical = 記号列のバイト列 か payload のバイト列
  暗号  = AES-GCM 256bit, IV 12バイト
  出力  = base64url( IV(12) + 暗号文+タグ )   ← これを c= に載せる

使い方:
  python3 fue/make_cipher_link.py --symbols 2,0,2,6,7,2,4 --goto https://example.com/secret
  python3 fue/make_cipher_link.py --payload-hex 70617373 --msg "ようこそ" --parity 2 --mode sequential
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
from urllib.parse import quote

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

BASE = "https://qurihara.github.io/ai-fue/cipher/"


def make_pack(canonical: bytes, payload: dict) -> str:
    """設定一式(dict)を笛の秘密で暗号化し、c= に載せる文字列を返す。"""
    key = hashlib.sha256(canonical).digest()
    iv = os.urandom(12)
    raw = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    ct = AESGCM(key).encrypt(iv, raw, None)
    return base64.urlsafe_b64encode(iv + ct).decode("ascii").rstrip("=")


def build_link(canonical: bytes, payload: dict, config: dict, base: str = BASE) -> str:
    """フラグメントに体系と暗号文を載せた、デモ用のURLを組み立てる。"""
    parts = ["%s=%s" % (k, quote(str(v), safe="")) for k, v in config.items()]
    parts.append("c=" + make_pack(canonical, payload))
    return base + "#" + "&".join(parts)


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="笛の秘密で設定を包み、フラグメントに載せたデモ用リンクを作る")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--symbols", help="記号列（symbolsモード）例 2,0,2,6,7,2,4")
    g.add_argument("--payload-hex", help="payload hex（sequentialモード）")
    ap.add_argument("--goto", help="認証成功で開く遷移先URL（省略可）")
    ap.add_argument("--msg", help="認証成功で見せる言葉（省略可）")
    ap.add_argument("--lo", default="G#6", help="音域の下端（既定 G#6）")
    ap.add_argument("--hi", default="F#7", help="音域の上端（既定 F#7）")
    ap.add_argument("--ref", default="C7", help="基準笛（既定 C7）")
    ap.add_argument("--mode", default="symbols", choices=("symbols", "sequential"))
    ap.add_argument("--parity", type=int, default=0, help="検査用の笛の本数（既定 0）")
    ap.add_argument("--base", default=BASE, help="復号ページのURL")
    a = ap.parse_args(argv)

    if a.symbols is not None:
        canonical = bytes(int(x) for x in a.symbols.split(",") if x.strip() != "")
    else:
        canonical = bytes.fromhex(a.payload_hex)

    payload = {}
    if a.goto:
        payload["goto"] = a.goto
    if a.msg:
        payload["msg"] = a.msg
    if not payload:
        raise SystemExit("--goto か --msg のどちらかは指定してください")

    config = {"lo": a.lo, "hi": a.hi, "ref": a.ref, "mode": a.mode, "parity": a.parity}
    link = build_link(canonical, payload, config, a.base)
    print("包んだ中身:", json.dumps(payload, ensure_ascii=False))
    print("URL:")
    print(link)
    print()
    print("このURLはフラグメントに設定を置いているので、サーバには何も送られません。")
    print("中身は笛の秘密でしか開けないため、URLを見ても遷移先や言葉は分かりません。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
