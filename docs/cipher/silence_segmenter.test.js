"use strict";
/* 無音区切りの状態機械のテスト。合成したレベル列を流し込んで、狙いどおりに
 * 本数と周波数が取れるかを確かめる。実マイクは使わない。 */

const assert = require("assert");
const seg = require("./silence_segmenter.js");

const FRAME_MS = 16;   // 60フレーム毎秒を想定

/* 台本から毎フレームの (level, freq) を作る。
 * 台本は [{ms, db, hz}, ...] の並びで、各区間をその値で埋める。 */
function render(script) {
  const frames = [];
  let t = 0;
  script.forEach(part => {
    const n = Math.round(part.ms / FRAME_MS);
    for (let i = 0; i < n; i++) {
      frames.push({t: t, level: part.db, freq: part.hz || 0});
      t += FRAME_MS;
    }
  });
  return frames;
}

function run(script, options) {
  const s = seg.create(options);
  const notes = [];
  let ended = false;
  render(script).forEach(f => {
    const ev = s.feed(f.t, f.level, f.freq);
    if (ev.type === "note") notes.push(ev);
    if (ev.type === "end") ended = true;
  });
  return {notes: notes, ended: ended, thresholds: s.thresholds()};
}

const QUIET = {ms: 600, db: -95};          // 暗騒音（測定用に十分な長さ）
const note = (hz, ms) => ({ms: ms || 400, db: -45, hz: hz});
const gap = (ms) => ({ms: ms || 300, db: -95});

// 1) 基本：5本を無音で区切って吹く
{
  const r = run([QUIET, note(1046), gap(), note(1318), gap(), note(1567), gap(),
                 note(1975), gap(), note(2093), gap(2000)]);
  assert.strictEqual(r.notes.length, 5, "5本に切り分かれる");
  const hz = r.notes.map(n => Math.round(n.freq));
  assert.deepStrictEqual(hz, [1046, 1318, 1567, 1975, 2093], "各本の周波数が取れる");
  assert.ok(r.ended, "最後の長い無音で終わりを検出する");
  console.log("  1) 基本 5本:", hz.join(","), " しきい値", JSON.stringify(r.thresholds));
}

// 2) 速い演奏：音200ms・無音200msでも切り分かれる
{
  const r = run([QUIET, note(1046, 200), gap(200), note(1318, 200), gap(200),
                 note(1567, 200), gap(2000)]);
  assert.strictEqual(r.notes.length, 3, "短い音でも3本に切り分かれる");
  console.log("  2) 速い演奏(音200ms/無音200ms):", r.notes.map(n => Math.round(n.freq)).join(","));
}

// 3) 短すぎる雑音は捨てる（60msのパチッという音）
{
  const r = run([QUIET, {ms: 60, db: -45, hz: 1500}, gap(),
                 note(1046), gap(2000)]);
  assert.strictEqual(r.notes.length, 1, "雑音を除いて1本だけ");
  assert.strictEqual(Math.round(r.notes[0].freq), 1046);
  console.log("  3) 短い雑音を捨てる: 本数", r.notes.length);
}

// 4) 音の中の一瞬のふらつき（100ms）では切れない
{
  const r = run([QUIET, note(1046, 300), {ms: 100, db: -95}, note(1046, 300), gap(2000)]);
  assert.strictEqual(r.notes.length, 1, "gapMs未満のふらつきでは切れない");
  console.log("  4) 一瞬のふらつき(100ms)で切れない: 本数", r.notes.length);
}

// 5) うるさい部屋：暗騒音が高くても相対しきい値で動く
{
  const loudRoom = {ms: 600, db: -70};
  const r = run([loudRoom, {ms: 400, db: -40, hz: 1046}, {ms: 300, db: -70},
                 {ms: 400, db: -40, hz: 1318}, {ms: 2000, db: -70}]);
  assert.strictEqual(r.notes.length, 2, "暗騒音が高くても2本に切り分かれる");
  console.log("  5) うるさい部屋(暗騒音-70dB): 本数", r.notes.length,
              " しきい値", JSON.stringify(r.thresholds));
}

// 6) 立ち上がりの音程の揺れは測定から外れる（最初の50msだけ外れた値）
{
  const r = run([QUIET, {ms: 48, db: -45, hz: 800}, {ms: 400, db: -45, hz: 1046}, gap(2000)]);
  assert.strictEqual(r.notes.length, 1);
  assert.strictEqual(Math.round(r.notes[0].freq), 1046, "立ち上がりの揺れに引きずられない");
  console.log("  6) 立ち上がりの揺れを除く:", Math.round(r.notes[0].freq), "Hz");
}

// 7) 26本（スプール pass_#26 相当）を通しで切り分ける
{
  const script = [QUIET];
  const want = [];
  for (let i = 0; i < 26; i++) {
    const hz = 1400 + i * 40;
    want.push(hz);
    script.push(note(hz, 250));
    script.push(gap(250));
  }
  script.push(gap(2000));
  const r = run(script);
  assert.strictEqual(r.notes.length, 26, "26本すべて切り分かれる");
  assert.deepStrictEqual(r.notes.map(n => Math.round(n.freq)), want);
  const totalSec = (26 * 0.25 + 27 * 0.25 + 0.6).toFixed(1);
  console.log("  7) 26本の通し: 本数", r.notes.length, " 所要", totalSec, "秒");
}

// 8) 無音のまま何も吹かなければ、何も確定しない
{
  const r = run([QUIET, gap(3000)]);
  assert.strictEqual(r.notes.length, 0);
  assert.strictEqual(r.ended, false, "1本も無いなら終わり判定も出ない");
  console.log("  8) 無音のみ: 本数", r.notes.length, " 終了検出", r.ended);
}

console.log("silence_segmenter: 全8件パス");
