# 暗号笛ウォレット（段階0）

笛を吹くと、その場で秘密鍵が組み立てられ、Polygon Amoy 上の口座が現れる。鍵はどこにも保存しない。
契約は使わない（段階0）。設計の検討は [DESIGN.md](DESIGN.md) にある。

## 中身

| ファイル | 役割 |
|---|---|
| `index.html` | 画面。笛を吹く→鍵を作る→アドレスと残高を出す |
| `flute_key.js` | 秘密から口座を作る。PBKDF2（60万回）→ secp256k1 → keccak |
| `flute_key.test.js` | 鍵導出の検査。`node docs/dapp/flute_key.test.js` |
| `vendor/` | 外部ライブラリの実体。CDNから読まず、ここに置いたものだけを使う |

## 鍵の作り方（仕様）

```
salt = "cipherflute/v1" + "|" + ラベル        （例 "cipherflute/v1|amoy"）
seed = PBKDF2-HMAC-SHA256(秘密のバイト列, salt, 600000回, 32バイト)
秘密鍵 = seed（曲線の外に出たら salt に通し番号を足して作り直す）
アドレス = keccak256(公開鍵の非圧縮65バイトの先頭1バイトを除いた部分) の下位20バイト
```

[* この仕様を変えると、既に印刷した笛が別の口座を指す]。版（`cipherflute/v1`）と繰り返し回数は
仕様の一部であり、迂闊に変えてはいけない。検査（`flute_key.test.js`）がその見張りである。

## 手元で動かす

```
python3 -m http.server 8765 --directory docs
```
のあと `http://localhost:8765/dapp/` を開く。ES モジュールを使うので `file://` では動かない。

## いまできること・まだできないこと

* できる … 笛を吹いて口座を開く、アドレスを見る、残高を読む
* まだ … 送金（次の段階で、この画面から署名して送れるようにする）
