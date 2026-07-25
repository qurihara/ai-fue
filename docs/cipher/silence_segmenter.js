/* 無音区切りで笛を1本ずつに切り分ける状態機械。
 *
 * 音を続けて吹き、笛と笛の間に短い無音を置くだけで次の桁へ進む方式のために使う。
 * 判定に使うのは「笛の音域(loFloorHz以上)だけの帯域レベル[dB]」である。低い周波数を
 * 見ないので、話し声や空調の唸りには反応しにくい。
 *
 * 使い方は、毎フレーム feed(t, level, freq) を呼ぶだけである。t は経過時間[ms]、
 * level は帯域レベル[dB]、freq は今の推定周波数[Hz]（無ければ0）。
 * 戻り値は起きた出来事で、"note" なら1本ぶんが確定したことを表す。
 *
 * しきい値は環境ごとに違うので、開始直後の一定時間を暗騒音の測定にあて、そこから
 * 相対的に決める。鳴り始めと鳴り終わりで別のしきい値を使い（ヒステリシス）、境目で
 * ばたつかないようにしている。
 */
(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  if (root) root.SilenceSegmenter = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";

  const DEFAULTS = {
    calibMs: 400,      // 開始直後、暗騒音を測る時間
    onMarginDb: 15,    // 暗騒音からこれだけ上なら「鳴っている」
    offMarginDb: 8,    // 暗騒音からこれだけ下回ったら「切れた」(ヒステリシス)
    absOnDb: -70,      // 暗騒音が静かすぎるときの下限
    onMs: 60,          // この時間続けて大きければ、鳴り始めと認める
    gapMs: 180,        // この時間続けて小さければ、1本の終わりと認める
    minNoteMs: 120,    // これより短い音は雑音として捨てる
    attackSkipMs: 50,  // 鳴り始めは音程が揺れるので、この時間ぶん測定しない
    endMs: 1500        // 1本以上入ったあと、この時間無音なら入力の終わりとみなす
  };

  function median(values) {
    if (!values.length) return null;
    const sorted = values.slice().sort((a, b) => a - b);
    return sorted[Math.floor(sorted.length / 2)];
  }

  function create(options) {
    const opt = Object.assign({}, DEFAULTS, options || {});
    const state = {};

    function reset() {
      state.phase = "calib";   // calib(暗騒音の測定) -> idle(待機) -> note(鳴っている)
      state.t0 = null;
      state.noise = [];
      state.noiseDb = null;
      state.onDb = null;
      state.offDb = null;
      state.onSince = null;    // 大きい状態が続き始めた時刻
      state.offSince = null;   // 小さい状態が続き始めた時刻
      state.noteStart = null;
      state.freqs = [];
      state.count = 0;         // 確定した本数
      state.lastCommit = null; // 直近に確定した時刻
    }
    reset();

    /* 1フレーム進める。戻り値は
     *   {type:"calibrating"} 暗騒音を測っている
     *   {type:"idle"}        待機している
     *   {type:"onset"}       鳴り始めを検出した
     *   {type:"sounding"}    鳴っている最中
     *   {type:"note", freq}  1本ぶんが確定した
     *   {type:"reject"}      短すぎたので捨てた
     *   {type:"end"}         入力の終わり(長い無音)を検出した
     */
    function feed(t, level, freq) {
      if (state.t0 === null) state.t0 = t;
      const loud = state.onDb !== null && level >= state.onDb;
      const quiet = state.offDb !== null && level < state.offDb;

      if (state.phase === "calib") {
        state.noise.push(level);
        if (t - state.t0 < opt.calibMs) return {type: "calibrating"};
        // 暗騒音は中央値で代表する。突発的な物音に引きずられないため。
        state.noiseDb = median(state.noise);
        state.onDb = Math.max(state.noiseDb + opt.onMarginDb, opt.absOnDb);
        state.offDb = Math.max(state.noiseDb + opt.offMarginDb, opt.absOnDb - opt.onMarginDb + opt.offMarginDb);
        state.phase = "idle";
        return {type: "idle"};
      }

      if (state.phase === "idle") {
        if (loud) {
          if (state.onSince === null) state.onSince = t;
          if (t - state.onSince >= opt.onMs) {
            state.phase = "note";
            state.noteStart = state.onSince;   // 立ち上がりの時刻を始点にする
            state.freqs = [];
            state.onSince = null;
            state.offSince = null;
            return {type: "onset"};
          }
        } else {
          state.onSince = null;
        }
        // 1本以上入ったあとの長い無音は、入力の終わりとみなす
        if (state.count > 0 && state.lastCommit !== null &&
            t - state.lastCommit >= opt.endMs && state.onSince === null) {
          return {type: "end"};
        }
        return {type: "idle"};
      }

      // state.phase === "note"
      if (!quiet) {
        state.offSince = null;
        if (t - state.noteStart >= opt.attackSkipMs && freq) state.freqs.push(freq);
        return {type: "sounding"};
      }
      if (state.offSince === null) state.offSince = t;
      if (t - state.offSince < opt.gapMs) return {type: "sounding"};

      // 無音が続いたので1本ぶんを閉じる
      const duration = state.offSince - state.noteStart;
      const f = median(state.freqs);
      state.phase = "idle";
      state.onSince = null;
      state.offSince = null;
      if (duration < opt.minNoteMs || !f) {
        state.freqs = [];
        return {type: "reject"};
      }
      state.freqs = [];
      state.count += 1;
      state.lastCommit = t;
      return {type: "note", freq: f, durationMs: duration};
    }

    return {
      feed: feed,
      reset: reset,
      options: opt,
      thresholds: () => ({noiseDb: state.noiseDb, onDb: state.onDb, offDb: state.offDb}),
      phase: () => state.phase,
      count: () => state.count
    };
  }

  return {create: create, DEFAULTS: DEFAULTS};
});
