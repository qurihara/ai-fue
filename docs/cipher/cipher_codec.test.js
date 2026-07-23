"use strict";

const assert = require("assert");
const fs = require("fs");
const path = require("path");
const codec = require("./cipher_codec.js");

const config = JSON.parse(fs.readFileSync(path.join(__dirname, "cipher_config.json"), "utf8"));
const fixture = JSON.parse(fs.readFileSync(path.join(__dirname, "cipher_test_vectors.json"), "utf8"));

fixture.vectors.forEach((vector, index) => {
  const cfg = Object.assign({}, config, {ecc_parity: vector.parity, mode: vector.mode});
  const result = codec.decode(vector.measured_freqs, cfg);
  assert(!result.status.startsWith("error:"), `vector ${index}: ${result.status}`);
  let label;
  if (vector.mode === "symbols") {
    assert.deepStrictEqual(result.symbols, vector.expected_symbols, `vector ${index}`);
    label = "symbols [" + vector.symbols.join(",") + "]";
  } else {
    assert.strictEqual(codec.bytesToHex(result.payload), vector.expected_payload_hex, `vector ${index}`);
    label = vector.payload_hex;
  }
  console.log(`PASS ${index + 1}/${fixture.vectors.length}: ${label} parity=${vector.parity} (${result.status})`);
});

// データ記号数が不正な笛列(RS的には無矛盾のd=1)はエラーになることを確認する。
{
  const cfg = Object.assign({}, config, {ecc_parity: 2, mode: "sequential"});
  const table = codec.slots(cfg);
  const wire = codec._rsEncode([5], 2, codec._prime(table.length));
  const freqs = [table[table.reference_index].freq_hz].concat(wire.map(s => table[s].freq_hz));
  const result = codec.decode(freqs, cfg);
  assert(result.status.includes("データ記号数が不正"), `bad-width: ${result.status}`);
  console.log("PASS bad-width rejection (" + result.status + ")");
}

console.log(`ALL PASS (${fixture.vectors.length} vectors)`);
