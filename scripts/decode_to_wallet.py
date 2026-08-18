#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""実演の録画から秘密を復号し、その秘密で開く口座の残高までを通しで確かめる。

なぜ要るか
----------
笛の現物が手元にないときでも、[* 録画の音から口座が開くこと]を確かめられる。
「笛を吹く → 秘密が戻る → 口座が現れる → 残高が出る」という一連が、実際に
つながっているかを見る道具である。

何をするか
----------
1. `decode_videos.py` と同じ手順で、録画の音から秘密を復号する
2. 復号できた秘密を、そのまま鍵導出へ渡す（合言葉は demo）
3. 出てきた口座の残高を Polygon Amoy から読む

[* 秘密は台帳の値を写さない。] 録画から復号した値だけを使う。写してしまうと、
録画から本当に戻るのかが確かめられなくなる。

鍵導出とアドレスの計算は JavaScript 側（docs/dapp/flute_key.js）に任せる。
ページとまったく同じ関数を通すので、ここで出た口座は画面でも同じになる。

使い方
    python3 scripts/decode_to_wallet.py            全部
    python3 scripts/decode_to_wallet.py --only かるた
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import decode_videos as dv          # noqa: E402  録画から音を拾う処理をそのまま使う
from fue import cipher_codec as cd  # noqa: E402
from fue import threshold as th     # noqa: E402

RPC = "https://polygon-amoy-bor-rpc.publicnode.com"
DAPP = os.path.join(ROOT, "docs", "dapp")


def secret_from_case(case, raw=False):
    """録画から秘密を復号する。返すのは (秘密, 説明) で、失敗したら (None, 理由)。"""
    path = os.path.join(dv.VIDEOS, case["name"] + ".TS.mp4")
    if not os.path.exists(path):
        return None, "録画が無い"
    want = case["per"] * case["parts"]
    if case["kind"] in ("threshold", "sum"):
        _all, segs = dv.segments_of(path, keep_all=raw)
        segs = [x for x in segs if x.get("durationMs", 0) >= dv.MIN_MS]
    else:
        _all, segs = dv.prepare(path, want, keep_all=raw)
    freqs = [s["freq"] for s in segs]
    c, kind = case["cfg"], case["kind"]

    if kind == "symbols":
        r = dv.decode_notes(freqs[:case["per"]], c)
        if r.status.startswith("error"):
            return None, "復号できない（%s）" % r.status
        return list(r.symbols), "記号 %s" % list(r.symbols)

    if kind == "payload":
        r, how = dv.repair_decode(freqs, c, want, lambda x: getattr(x, "payload", None))
        if not getattr(r, "payload", None):
            return None, "復号できない（%s）" % r.status
        return list(bytes(r.payload)), "%r（%s）" % (bytes(r.payload), how)

    if kind == "sum":
        groups = [dv.tightest_run(g, case["per"])
                  for g in dv.split_by_gaps(segs, case["parts"])]
        syms = []
        for g in groups:
            fr = [x["freq"] for x in g]
            need = case["per"] - 1 - c.ecc_parity
            good = (lambda rr: (not rr.status.startswith("error")
                                and len(rr.symbols) == need))
            r, _how = dv.repair_decode(fr, c, case["per"], good)
            if not good(r):
                r2, _h2 = dv.repair_decode(list(reversed(fr)), c, case["per"], good)
                if good(r2):
                    r = r2
            if not good(r):
                return None, "1枚が読めない（%s）" % r.status
            syms.append(list(r.symbols))
        base = cd._wire_params(c)[1]
        width = len(syms[0])
        span = base ** width
        def _val(ds):
            v = 0
            for d in ds:
                v = v * base + d
            return v
        total = sum(_val(s) for s in syms) % span
        # 合成した値を、口座へ渡すのと同じ「記号の配列」に戻す
        digits = []
        v = total
        for _ in range(width):
            digits.append(v % base)
            v //= base
        digits.reverse()
        return digits, "合わせた秘密 %d ／ 記号 %s" % (total, digits)

    if kind == "threshold":
        tiles = [dv.tightest_run(t, case["per"])
                 for t in dv.split_by_gaps(segs, case["parts"])]
        shares = []
        for i, t in enumerate(tiles):
            r = dv.decode_notes([x["freq"] for x in t], c)
            if r.symbols and not r.status.startswith("error"):
                shares.append((i + 1, list(r.symbols)))
        import itertools
        for a, b in itertools.combinations(shares, 2):
            try:
                digits = list(th.combine([a, b]))
            except Exception:
                continue
            value = th.value_of(digits)
            if value == case["expect"]:
                return digits, "タイル%dと%dの組から 秘密 %d ／ 記号 %s" % (a[0], b[0], value, digits)
        return None, "どの2枚の組でも秘密が戻らない"

    return None, "この種類は扱わない（%s）" % kind


def wallets(items):
    """秘密の一覧を JavaScript 側へ渡し、口座と残高を受け取る。"""
    js = r"""
import { webcrypto } from "node:crypto";
import https from "node:https";
import fs from "node:fs";
if (!globalThis.crypto?.subtle) globalThis.crypto = webcrypto;
const { deriveAccount } = await import(process.argv[2] + "/flute_key.js");
const items = JSON.parse(fs.readFileSync(process.argv[3], "utf8"));
const rpc = (method, params) => new Promise((res, rej) => {
  const body = JSON.stringify({jsonrpc:"2.0", id:1, method, params});
  const r = https.request(process.argv[4], {method:"POST",
    headers:{"content-type":"application/json","content-length":Buffer.byteLength(body)}}, (s) => {
    let d = ""; s.on("data", c => d += c);
    s.on("end", () => { try { const j = JSON.parse(d); j.error ? rej(new Error(j.error.message)) : res(j.result); }
                        catch(e){ rej(e); } });
  });
  r.on("error", rej); r.write(body); r.end();
});
const out = [];
for (const it of items) {
  const a = await deriveAccount(Uint8Array.from(it.secret), {label:"amoy", passphrase:"demo"});
  const wei = BigInt(await rpc("eth_getBalance", [a.address, "latest"]));
  const whole = wei / 10n**18n, frac = (wei % 10n**18n).toString().padStart(18,"0").slice(0,6);
  out.push({label: it.label, address: a.address, balance: `${whole}.${frac}`});
}
console.log(JSON.stringify(out));
"""
    with tempfile.TemporaryDirectory() as d:
        js_path = os.path.join(d, "w.mjs")
        json_path = os.path.join(d, "items.json")
        open(js_path, "w", encoding="utf-8").write(js)
        json.dump(items, open(json_path, "w", encoding="utf-8"))
        out = subprocess.run(["node", js_path, DAPP, json_path, RPC],
                             capture_output=True, text=True)
        if out.returncode != 0:
            raise SystemExit("口座を作れなかった:\n" + out.stderr[-800:])
        return json.loads(out.stdout)


def main(argv=None):
    ap = argparse.ArgumentParser(description="録画から復号し、その秘密で開く口座の残高まで確かめる")
    ap.add_argument("--only", default=None, help="この名前を含むものだけ")
    ap.add_argument("--raw", action="store_true", help="雑音を落とさずに全部使う")
    args = ap.parse_args(argv)

    items, failed = [], []
    for case in dv.CASES:
        if case["kind"] == "scale":
            continue                      # 照合笛は秘密を持たない
        if args.only and args.only not in case["name"] and args.only not in case["label"]:
            continue
        print("───── %s" % case["label"])
        secret, how = secret_from_case(case, raw=args.raw)
        if secret is None:
            print("  ★%s★" % how)
            failed.append(case["label"])
            continue
        print("  %s" % how)
        items.append({"label": case["label"], "secret": secret})

    if not items:
        print("\n復号できたものが無い。")
        return 1

    print("\n口座と残高（合言葉 demo）")
    for w in wallets(items):
        mark = "○" if w["balance"] != "0.000000" else "★残高なし★"
        print("  %-34s %s  %s POL  %s" % (w["label"], w["address"], w["balance"], mark))
    if failed:
        print("\n復号できなかったもの: " + " / ".join(failed))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
