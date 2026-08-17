/* デモ映像で使う笛の口座へ、Polygon Amoy のテスト用トークンをまとめて送る。
 *
 * ★秘密鍵はこのファイルにも、このリポジトリのどこにも書かない。★
 * 次の場所に置いたテキストファイルから読む。
 *
 *   ~/.config/cipherflute/amoy_key.txt
 *
 * [* この置き場所はGoogle Driveの外である。] このリポジトリはDriveの中にあるので、
 * リポジトリに置くと鍵がクラウドへ同期されてしまう。ファイルは本人だけが読める
 * 権限（600）にしてある。# で始まる行と空の行は読み飛ばすので、覚え書きを書いてよい。
 *
 *   node scripts/fund_demo_wallets.mjs            送る内容を見せるだけ
 *   node scripts/fund_demo_wallets.mjs --yes      実際に送る
 *
 * 環境変数 AMOY_KEY があれば、そちらが優先される（ファイルを使わない運用もできる）。
 * --key-file <パス> で別のファイルを指せる。
 *
 * 主な指定
 *   --amount 1        1口座あたりの金額[POL]。既定 1
 *                     テストネットのトークンに価値はないので、少なく刻む意味はない。
 *                     1にすると残高が「1.000000 POL」と出て、紹介動画の子画面でも読みやすい。
 *                     手数料の上限は1回あたり0.0006 POL程度なので、1あれば1500回以上送れる。
 *   --only かるた,箱   名前の一部で絞る（読点か空白で区切る）
 *   --rpc <URL>       接続先。既定は publicnode
 *   --list            宛先の一覧だけ出して終わる（鍵は要らない）
 *
 * 何をするか
 *   1. 笛の秘密から口座のアドレスを導く（合言葉は demo）
 *   2. いまの残高を読み、[* すでに入っている口座は飛ばす]
 *   3. 送り主の残高で足りるかを確かめる
 *   4. 1件ずつ署名して送り、台帳に載るのを待つ
 *
 * 送金の部品は docs/dapp/tx.js をそのまま使う。ページと同じ道を通るので、
 * ここで通れば画面でも通る。
 */
import { webcrypto } from "node:crypto";
import https from "node:https";
import path from "node:path";
import fs from "node:fs";
import os from "node:os";
import { fileURLToPath } from "node:url";

if (!globalThis.crypto?.subtle) globalThis.crypto = webcrypto;

const HERE = path.dirname(fileURLToPath(import.meta.url));
const DAPP = path.join(HERE, "..", "docs", "dapp");
const { deriveAccount } = await import(path.join(DAPP, "flute_key.js"));
const tx = await import(path.join(DAPP, "tx.js"));

/* ---------------------------------------------------------------- 宛先 */

// デモ映像に出てくる笛と、口座を開くための秘密。合言葉は demo。
// 北斎のタイルは、実演の録画から読めた7枚ぶんである（1と5は当時読めていない）。
const WALLETS = [
  ["かるた札2枚（崇徳院）",     [1, 6, 8, 10, 5, 2]],
  ["2-of-3の箱（断片1）",       [6, 7, 1, 2, 1]],
  ["2-of-3のカード（断片2）",   [4, 9, 5, 10, 3]],
  ["2-of-3の本立て（断片3）",   [2, 0, 9, 7, 5]],
  ["スプール2枚（128ビット）",  new TextEncoder().encode("CipherFlute-demo")],
  ["電子錠のカード（2026724）", [2, 0, 2, 6, 7, 2, 4]],
  ["北斎タイル2", [10, 0, 8, 2, 6, 6]],
  ["北斎タイル3", [9, 6, 4, 3, 2, 4]],
  ["北斎タイル4", [8, 1, 0, 4, 9, 2]],
  ["北斎タイル6", [5, 3, 3, 10, 1, 9]],
  ["北斎タイル7", [4, 9, 10, 0, 8, 7]],
  ["北斎タイル8", [3, 4, 6, 1, 4, 5]],
  ["北斎タイル9", [3, 9, 2, 9, 0, 3]],
];

/* ---------------------------------------------------------------- 引数 */

const argv = process.argv.slice(2);
const flag = (name) => argv.includes(name);
const opt = (name, def) => {
  const i = argv.indexOf(name);
  return i >= 0 && argv[i + 1] ? argv[i + 1] : def;
};
const RPC_URL = opt("--rpc", "https://polygon-amoy-bor-rpc.publicnode.com");
const AMOUNT = opt("--amount", "1");
const ONLY = opt("--only", "").split(/[,、\s]+/).filter(Boolean);
const CHAIN_ID = 80002n;

/* ---------------------------------------------------------------- RPC */

function rpc(method, params) {
  return new Promise((res, rej) => {
    const body = JSON.stringify({jsonrpc: "2.0", id: 1, method, params});
    const r = https.request(RPC_URL, {
      method: "POST",
      headers: {"content-type": "application/json", "content-length": Buffer.byteLength(body)},
    }, (s) => {
      let d = "";
      s.on("data", (c) => d += c);
      s.on("end", () => {
        try {
          const j = JSON.parse(d);
          j.error ? rej(new Error(j.error.message)) : res(j.result);
        } catch (e) { rej(new Error("応答を読めない: " + d.slice(0, 120))); }
      });
    });
    r.on("error", rej);
    r.write(body);
    r.end();
  });
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

/** 取引が台帳に載るのを待つ。載らなければ null を返す。 */
async function waitReceipt(hash, tries = 40) {
  for (let i = 0; i < tries; i++) {
    const r = await rpc("eth_getTransactionReceipt", [hash]).catch(() => null);
    if (r) return r;
    await sleep(3000);
  }
  return null;
}

/* ---------------------------------------------------------------- 本体 */

const targets = [];
for (const [name, secret] of WALLETS) {
  if (ONLY.length && !ONLY.some((w) => name.includes(w))) continue;
  const a = await deriveAccount(secret, {label: "amoy", passphrase: "demo"});
  targets.push({name, address: a.address});
}
if (!targets.length) { console.error("宛先が1つも選ばれていない（--only の指定を見直すこと）"); process.exit(1); }

if (flag("--list")) {
  console.log("デモ映像で使う笛の口座（合言葉 demo）\n");
  for (const t of targets) console.log("  " + t.name.padEnd(26) + t.address);
  process.exit(0);
}

/** 秘密鍵を読む。環境変数が先、無ければファイル。★中身は決して表示しない。★ */
function readKey() {
  if (process.env.AMOY_KEY) return process.env.AMOY_KEY.trim();
  const file = opt("--key-file", path.join(os.homedir(), ".config", "cipherflute", "amoy_key.txt"));
  if (!fs.existsSync(file)) {
    console.error("秘密鍵のファイルが無い: " + file);
    console.error("次の行で作って、MetaMask から取り出した鍵を貼ること。");
    console.error("  code " + file);
    process.exit(1);
  }
  const st = fs.statSync(file);
  if (st.mode & 0o077) {
    console.error("★このファイルは他の人からも読める★ " + file);
    console.error("次の行で直すこと。  chmod 600 " + file);
    process.exit(1);
  }
  // # で始まる行と空の行は覚え書きとみなして読み飛ばす
  const line = fs.readFileSync(file, "utf8").split("\n")
    .map((l) => l.trim()).filter((l) => l && !l.startsWith("#"))[0];
  if (!line) {
    console.error("秘密鍵がまだ書かれていない: " + file);
    console.error("  code " + file);
    process.exit(1);
  }
  return line;
}

// MetaMask は 0x を付けずに書き出す。どちらで貼られても受けるよう、ここで揃える。
const RAW_KEY = readKey().replace(/^0x/i, "");
if (!/^[0-9a-fA-F]{64}$/.test(RAW_KEY)) {
  console.error("秘密鍵の形が違う。16進64桁を1行で書くこと（0x は付けても付けなくてよい）。");
  console.error("いま読めたのは " + RAW_KEY.length + "文字。MetaMaskの「アカウントの詳細」→「秘密鍵」で"
                + "「長押しして秘密鍵を表示」を押し続けると出る値である。");
  process.exit(1);
}
const KEY = "0x" + RAW_KEY;
const priv = tx.hexToBytes(KEY);
const from = tx.addressOf(priv);
const valueWei = tx.parseEther(AMOUNT);

console.log("接続先 " + RPC_URL);
const chainId = BigInt(await rpc("eth_chainId", []));
if (chainId !== CHAIN_ID) {
  console.error(`つないだ先が Amoy ではない（chainId ${chainId}）。--rpc を見直すこと。`);
  process.exit(1);
}
console.log("送り主 " + from);
const fromBal = BigInt(await rpc("eth_getBalance", [from, "latest"]));
console.log("残高   " + tx.formatEther(fromBal) + " POL\n");

// すでに入っている口座は飛ばす。何度実行しても二重に送らないためである。
console.log("宛先といまの残高");
const todo = [];
for (const t of targets) {
  const bal = BigInt(await rpc("eth_getBalance", [t.address, "latest"]));
  const skip = bal >= valueWei;
  console.log(`  ${skip ? "済" : "→"} ${t.name.padEnd(26)} ${t.address}  ${tx.formatEther(bal)} POL`);
  if (!skip) todo.push(t);
}
if (!todo.length) { console.log("\nすべての口座に入っている。送るものはない。"); process.exit(0); }

// 手数料の見積もり。1件あたりの上限を出し、件数ぶん足して足りるかを見る。
const probe = await tx.buildTransfer(rpc, {from, to: todo[0].address, valueWei, chainId: CHAIN_ID});
const feePer = tx.maxFeeWei(probe);
const need = (valueWei + feePer) * BigInt(todo.length);
console.log(`\n送る先 ${todo.length}件 × ${AMOUNT} POL`);
console.log(`手数料の上限 1件あたり ${tx.formatEther(feePer)} POL`);
console.log(`合わせて要る額 ${tx.formatEther(need)} POL ／ 残高 ${tx.formatEther(fromBal)} POL`);
if (fromBal < need) {
  console.error("\n★残高が足りない★ 蛇口から足すか、--amount を下げること。");
  process.exit(1);
}

if (!flag("--yes")) {
  console.log("\n（ここまでは下見である。実際に送るには --yes を付ける）");
  process.exit(0);
}

console.log("\n送る");
let nonce = BigInt(await rpc("eth_getTransactionCount", [from, "pending"]));
for (const t of todo) {
  const built = await tx.buildTransfer(rpc, {from, to: t.address, valueWei, chainId: CHAIN_ID});
  built.nonce = nonce++;          // 続けて送るので通し番号は自分で進める
  const {raw, hash} = await tx.signTransaction(built, priv);
  process.stdout.write(`  ${t.name.padEnd(26)} `);
  try {
    const sent = await tx.sendRaw(rpc, raw);
    process.stdout.write(sent.slice(0, 18) + "… ");
    const rec = await waitReceipt(sent);
    console.log(rec ? (BigInt(rec.status) === 1n ? "成功" : "★失敗（台帳に載ったが status=0）★")
                    : "★台帳に載ったか確認できない★ " + sent);
  } catch (e) {
    console.log("★送れない★ " + e.message);
  }
}

console.log("\n仕上がりの残高");
for (const t of targets) {
  const bal = BigInt(await rpc("eth_getBalance", [t.address, "latest"]));
  console.log(`  ${t.name.padEnd(26)} ${tx.formatEther(bal)} POL`);
}
