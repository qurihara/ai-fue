"""?goto_enc の生成: 笛の秘密（symbols か payload）から鍵を作り、遷移先URLを AES-GCM で暗号化する。

復号ページ(docs/cipher/index.html)は、笛を吹いて秘密を正しく復元できたときだけ、この暗号文を
復号して遷移先URLを開ける。秘密を知らない者はURLを復号できないので、?goto_enc がURLに載っていても
どこへ飛ぶか分からない（対称暗号：鍵＝笛の秘密。公開鍵は不要）。

WebCrypto と互換:
  鍵    = SHA-256(canonical)                 canonical = symbolsのバイト列 or payloadのバイト列
  暗号  = AES-GCM 256bit, IV 12バイト
  出力  = base64url( IV(12) + 暗号文+タグ )   ← これを ?goto_enc= に載せる
"""
import argparse
import base64
import hashlib
import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def make_goto_enc(canonical: bytes, url: str) -> str:
    key = hashlib.sha256(canonical).digest()
    iv = os.urandom(12)
    ct = AESGCM(key).encrypt(iv, url.encode("utf-8"), None)
    return base64.urlsafe_b64encode(iv + ct).decode("ascii").rstrip("=")


def main(argv=None):
    ap = argparse.ArgumentParser(description="笛の秘密でURLを暗号化して ?goto_enc を作る")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--symbols", help="記号列（symbolsモード）例 2,0,2,6,7,2,4")
    g.add_argument("--payload-hex", help="payload hex（sequentialモード）")
    ap.add_argument("--url", required=True, help="認証成功で開く遷移先URL")
    ap.add_argument("--base", default="https://qurihara.github.io/ai-fue/cipher/index.html",
                    help="復号ページのベースURL")
    ap.add_argument("--params", default="lo=G%236&hi=F%237&mode=symbols&parity=0",
                    help="体系を指定するGETパラメータ（既定は11音・記号列・パリティ0）")
    a = ap.parse_args(argv)
    if a.symbols is not None:
        canonical = bytes(int(x) for x in a.symbols.split(",") if x.strip() != "")
    else:
        canonical = bytes.fromhex(a.payload_hex)
    enc = make_goto_enc(canonical, a.url)
    print("goto_enc =", enc)
    print("URL:")
    print("%s?%s&goto_enc=%s" % (a.base, a.params, enc))


if __name__ == "__main__":
    main()
