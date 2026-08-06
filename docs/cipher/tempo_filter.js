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

    // 拍に乗っているかどうかで、[* 扱いを3つに分ける]。
    //
    //   drop（除外）… 拍から外れた短い音。咳や物音であって笛ではないので、
    //                 位置ごと取り除く。本数には数えない。
    //   skip（飛ばし）… 拍には乗っているのに読めない音。[* そこに笛はあったが鳴らなかった]
    //                 ということなので、位置を保ったまま消失として扱い、パリティで訂正させる。
    //   keep（採用）… そのまま使う。
    //
    // この区別は栗原さんの指摘による（2026-08-06）。以前はどちらも「除外」にしていたので、
    // 笛が鳴らなかったときに本数が1つ減り、パリティで直せる誤りを直せなくしていた。
    for (const it of items) {
      it.action = it.keep ? "keep" : "drop";
      if (it.startMs == null) continue;
      const phase = nearestBeatDistance(it.startMs, sure, beatMs);
      const onBeat = phase != null && phase <= beatMs * opt.onBeatTol;
      const short = it.durationMs != null && it.durationMs < beatMs * opt.shortRatio;

      if (it.kind === "reject") {
        if (onBeat && it.freq) {
          it.keep = true; it.action = "keep";
          it.reason = "拍に乗っていたので拾い直した";
        } else if (onBeat) {
          // 拍には来ているのに音程が取れなかった＝笛が鳴らなかった
          it.keep = false; it.action = "skip";
          it.reason = "拍に来たが読めなかった（鳴らない笛として飛ばす）";
        } else {
          it.keep = false; it.action = "drop";
          it.reason = (it.reason || "短すぎた") + "／拍にも乗っていない（雑音）";
        }
      } else if (!onBeat && short) {
        it.keep = false; it.action = "drop";
        it.reason = "拍から外れた短い音（雑音の疑い）";
      }

      if (it.keep && it.durationMs != null && it.durationMs > beatMs * opt.mergedRatio) {
        it.warn = "長い（2本ぶんが繋がった疑い）";
      }
    }

    // [* 拍の位置に音がまったく来なかった]場合も、笛が鳴らなかったということである。
    // 最初の音から最後の音までのあいだで、拍の格子に穴が空いていれば飛ばしを挿す。
    const missing = [];
    const live = items.filter(it => it.action !== "drop" && it.startMs != null);
    if (live.length >= 2) {
      const t0 = live[0].startMs;
      const tEnd = live[live.length - 1].startMs;
      const nBeats = Math.round((tEnd - t0) / beatMs);
      for (let k = 1; k < nBeats; k++) {
        const t = t0 + k * beatMs;
        const near = live.some(it => Math.abs(it.startMs - t) <= beatMs * opt.onBeatTol);
        if (!near) missing.push({beatIndex: k, startMs: t,
                                 reason: "この拍に音が来なかった（鳴らない笛として飛ばす）"});
      }
    }
    return {items, beatMs, missing, note: ""};
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
