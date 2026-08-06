/* 吹いたテンポを手がかりに、雑音まじりの音の列を整える。
 *
 * なぜ要るか
 * ----------
 * 不調な笛が混じると、無音区切りの自動送りが崩れる。音がうまく鳴らずに短い雑音が
 * 入ったり、まったく違う高さに聞こえたりするためである。しきい値（これより短ければ
 * 無視）だけでは、短いが本物の音と、長めの雑音を見分けられない。
 *
 * 手がかりになるのが[* テンポ]である。うまく吹けているとき、笛は almost 一定の間隔で
 * 入ってくる。そこで、確かな音どうしの間隔から拍を測り、その拍に乗らない短い音を
 * 雑音とみなす。人が「調子よく吹けているときのリズム」で判断しているのと同じことを、
 * 機械にさせる。
 *
 * 判断はすべて[* 提案]であって、決定ではない。返り値には理由を添えるので、画面で
 * 人が見て、必要なら手で有効・無効を切り替えられるようにする。
 *
 * 使い方:
 *   const out = TempoFilter.analyze(events, {});
 *   out.items      各音の判定（keep / drop と理由）
 *   out.beatMs     測ったテンポ（拍の間隔[ms]）。測れなければ null
 */
(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  if (root) root.TempoFilter = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";

  const DEFAULTS = {
    // 拍から見て、この割合より内側なら「拍に乗っている」とみなす。
    // 0.5 は隣の拍とのちょうど中間なので、そこに近い値にすると何でも
    // 「乗っている」ことになってしまう（0.45 で実際に誤判定した）。
    // 人が吹くときのばらつきを考えて ±30% に取る。
    onBeatTol: 0.30,
    // 拍のこの割合より短い音は、拍に乗っていなければ雑音とみなす
    shortRatio: 0.5,
    // 長さが拍のこの倍を超えたら「2本ぶんが繋がった疑い」を立てる
    mergedRatio: 1.7,
    // テンポを測るのに最低これだけの音が要る
    minForTempo: 3
  };

  function median(xs) {
    if (!xs.length) return null;
    const a = xs.slice().sort((x, y) => x - y);
    const m = a.length >> 1;
    return a.length % 2 ? a[m] : (a[m - 1] + a[m]) / 2;
  }

  /* 音の列を調べ、1つずつに判定を付ける。
   *
   * events は {kind:"note"|"reject", freq, durationMs, startMs} の配列である。
   * kind が "note" のものは、セグメンタが確かだと判断した音である。 */
  function analyze(events, options) {
    const opt = Object.assign({}, DEFAULTS, options || {});
    const items = events.map((e, i) => ({
      index: i,
      kind: e.kind,
      freq: e.freq == null ? null : e.freq,
      durationMs: e.durationMs == null ? null : e.durationMs,
      startMs: e.startMs == null ? null : e.startMs,
      keep: e.kind === "note",
      reason: e.kind === "note" ? "" : (e.reason || "短すぎた")
    }));

    // テンポは「確かな音」どうしの間隔から測る。雑音を混ぜると拍が狂う。
    const sure = items.filter(it => it.kind === "note" && it.startMs != null);
    let beatMs = null;
    if (sure.length >= opt.minForTempo) {
      const gaps = [];
      for (let i = 1; i < sure.length; i++) gaps.push(sure[i].startMs - sure[i - 1].startMs);
      beatMs = median(gaps);
    }
    if (!beatMs || beatMs <= 0) {
      return {items, beatMs: null, note: "テンポを測るには音が足りない（判定は変えていない）"};
    }

    // 捨てられた音のうち、拍に乗っているものは拾い直す。
    // 逆に、確かだとされた音でも、拍から大きく外れた短い音は雑音とみなす。
    for (const it of items) {
      if (it.startMs == null) continue;
      const phase = nearestBeatDistance(it.startMs, sure, beatMs);
      const onBeat = phase != null && phase <= beatMs * opt.onBeatTol;
      const short = it.durationMs != null && it.durationMs < beatMs * opt.shortRatio;

      if (it.kind === "reject") {
        if (onBeat && it.freq) {
          it.keep = true;
          it.reason = "拍に乗っていたので拾い直した";
        } else {
          it.keep = false;
          it.reason = (it.reason || "短すぎた") + "／拍にも乗っていない";
        }
      } else if (!onBeat && short) {
        it.keep = false;
        it.reason = "拍から外れた短い音（雑音の疑い）";
      }

      if (it.keep && it.durationMs != null && it.durationMs > beatMs * opt.mergedRatio) {
        it.warn = "長い（2本ぶんが繋がった疑い）";
      }
    }
    return {items, beatMs, note: ""};
  }

  /* いちばん近い拍からの隔たり[ms]。拍の格子は、確かな音の並びから作る。 */
  function nearestBeatDistance(t, sure, beatMs) {
    if (!sure.length) return null;
    const t0 = sure[0].startMs;
    const k = Math.round((t - t0) / beatMs);
    return Math.abs(t - (t0 + k * beatMs));
  }

  return {analyze, DEFAULTS, _median: median};
});
