/* CipherFlute復号器。fue/cipher_codec.pyと同じ計算を依存なしで行う。 */
(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  if (root) root.CipherCodec = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";

  const NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];

  function noteToMidi(note) {
    const match = /^([A-Ga-g])([#b]?)(-?\d+)$/.exec(String(note).trim());
    if (!match) throw new Error("bad note: " + JSON.stringify(note));
    const base = {C: 0, D: 2, E: 4, F: 5, G: 7, A: 9, B: 11}[match[1].toUpperCase()];
    const accidental = {"": 0, "#": 1, b: -1}[match[2]];
    return base + accidental + 12 * (Number(match[3]) + 1);
  }

  function midiToNote(midi) {
    return NOTE_NAMES[((midi % 12) + 12) % 12] + (Math.floor(midi / 12) - 1);
  }

  function noteToFreq(note) {
    return 440 * Math.pow(2, (noteToMidi(note) - 69) / 12);
  }

  function validateConfig(cfg) {
    if (!(cfg.step_cents > 0) || cfg.ecc_parity < 0) throw new Error("ステップは正、パリティは0以上が必要");
    const lo = noteToMidi(cfg.lo_note) * 100;
    const hi = noteToMidi(cfg.hi_note) * 100;
    const ref = noteToMidi(cfg.reference_note) * 100;
    const span = (hi - lo) / cfg.step_cents;
    const q = (ref - lo) / cfg.step_cents;
    if (hi < lo || Math.abs(span - Math.round(span)) > 1e-9) throw new Error("音域がスロット間隔で割り切れない");
    if (ref < lo || ref > hi || Math.abs(q - Math.round(q)) > 1e-9) throw new Error("reference_noteがスロット格子上かつ音域内ではない");
    if (cfg.mode !== "sequential" && cfg.mode !== "symbols") throw new Error("未対応のmode");
  }

  function slots(cfg) {
    validateConfig(cfg);
    const lo = noteToMidi(cfg.lo_note);
    const count = Math.round((noteToMidi(cfg.hi_note) - lo) * 100 / cfg.step_cents);
    const f0 = noteToFreq(cfg.lo_note);
    const table = [];
    for (let i = 0; i <= count; i++) {
      table.push({
        index: i,
        cents_from_lo: i * cfg.step_cents,
        freq_hz: f0 * Math.pow(2, i * cfg.step_cents / 1200),
        nearest_note: midiToNote(Math.round(lo + i * cfg.step_cents / 100))
      });
    }
    table.m = table.length;
    table.reference_index = refSlotIndex(cfg);
    return table;
  }

  function refSlotIndex(cfg) {
    return Math.round((noteToMidi(cfg.reference_note) - noteToMidi(cfg.lo_note)) * 100 / cfg.step_cents);
  }

  function _prime(n) {
    while (n < 2 || Array.from({length: Math.max(0, Math.floor(Math.sqrt(n)) - 1)}, (_, i) => i + 2).some(d => n % d === 0)) n++;
    return n;
  }

  function _toBase(value, base, width) {
    value = typeof value === "bigint" ? value : BigInt(value);
    const b = BigInt(base);
    if (value < 0n || base < 2) throw new Error("不正な値または底");
    const out = value === 0n ? [0] : [];
    while (value) {
      out.push(Number(value % b));
      value /= b;
    }
    out.reverse();
    if (width !== undefined) {
      if (out.length > width) throw new Error("指定幅に収まらない");
      while (out.length < width) out.unshift(0);
    }
    return out;
  }

  function _fromBase(digits, base) {
    let value = 0n;
    for (const d of digits) {
      if (!(0 <= d && d < base)) throw new Error("数字が範囲外");
      value = value * BigInt(base) + BigInt(d);
    }
    return value;
  }

  function mod(x, p) { return ((x % p) + p) % p; }
  function modPow(base, exponent, p) {
    let out = 1;
    base = mod(base, p);
    while (exponent > 0) {
      if (exponent % 2) out = mod(out * base, p);
      base = mod(base * base, p);
      exponent = Math.floor(exponent / 2);
    }
    return out;
  }

  function _generator(nsym, p) {
    let g = [1];
    for (let r = 1; r <= nsym; r++) {
      const a = modPow(2, r, p), next = Array(g.length + 1).fill(0);
      g.forEach((c, i) => {
        next[i] = mod(next[i] + c, p);
        next[i + 1] = mod(next[i + 1] - c * a, p);
      });
      g = next;
    }
    return g;
  }

  function _rsEncode(message, nsym, p) {
    if (!nsym) return message.slice();
    if (message.length + nsym > p - 1) throw new Error("RS符号長がp-1を超える");
    const g = _generator(nsym, p), work = message.concat(Array(nsym).fill(0));
    for (let i = 0; i < message.length; i++) {
      const c = work[i];
      g.forEach((x, j) => { work[i + j] = mod(work[i + j] - c * x, p); });
    }
    return message.concat(work.slice(-nsym).map(x => mod(-x, p)));
  }

  function _syndromes(word, nsym, p) {
    return Array.from({length: nsym}, (_, k) => {
      const r = k + 1, a = modPow(2, r, p), n = word.length;
      return mod(word.reduce((sum, v, i) => sum + v * modPow(a, n - 1 - i, p), 0), p);
    });
  }

  function _solve(a, b, p) {
    const n = b.length;
    const z = a.map((row, i) => row.map(x => mod(x, p)).concat(mod(b[i], p)));
    for (let c = 0; c < n; c++) {
      const pivot = z.findIndex((row, r) => r >= c && row[c] !== 0);
      if (pivot < 0) return null;
      [z[c], z[pivot]] = [z[pivot], z[c]];
      const inv = modPow(z[c][c], p - 2, p);
      z[c] = z[c].map(x => mod(x * inv, p));
      for (let r = 0; r < n; r++) {
        if (r === c) continue;
        const q = z[r][c];
        z[r] = z[r].map((x, i) => mod(x - q * z[c][i], p));
      }
    }
    return z.map((row, i) => row[n]);
  }

  function combinations(values, count) {
    if (count === 0) return [[]];
    const out = [];
    function visit(start, chosen) {
      if (chosen.length === count) { out.push(chosen.slice()); return; }
      for (let i = start; i <= values.length - (count - chosen.length); i++) {
        chosen.push(values[i]); visit(i + 1, chosen); chosen.pop();
      }
    }
    visit(0, []);
    return out;
  }

  function _rsDecode(received, nsym, p, erasures) {
    const erased = new Set(erasures || []), syn = _syndromes(received, nsym, p);
    if (!syn.some(Boolean) && !erased.size) return [received.slice(), new Set()];
    const candidates = received.map((_, i) => i).filter(i => !erased.has(i));
    const maxExtra = Math.floor((nsym - erased.size) / 2);
    for (let count = 0; count <= maxExtra; count++) {
      for (const extra of combinations(candidates, count)) {
        const pos = Array.from(new Set([...erased, ...extra])).sort((a, b) => a - b);
        if (!pos.length) continue;
        const a = pos.map((_, row) => {
          const r = row + 1, alpha = modPow(2, r, p);
          return pos.map(i => modPow(alpha, received.length - 1 - i, p));
        });
        const mag = _solve(a, syn.slice(0, pos.length).map(x => mod(-x, p)), p);
        if (!mag) continue;
        const trial = received.slice();
        pos.forEach((at, i) => { trial[at] = mod(trial[at] + mag[i], p); });
        if (!_syndromes(trial, nsym, p).some(Boolean)) return [trial, new Set(pos)];
      }
    }
    throw new Error("RSで訂正できない");
  }

  function _width(m, p) {
    let w = 1, cap = m;
    while (cap < p) { w++; cap *= m; }
    return w;
  }

  function _payloadWidth(nbytes, m) {
    /* Bバイトを表すのに必要な最小のbase-m固定幅d (m**d >= 256**B)。 */
    if (nbytes < 0) throw new Error("バイト数が負");
    let width = 0, cap = 1n;
    const target = 256n ** BigInt(nbytes), base = BigInt(m);
    while (cap < target) { width++; cap *= base; }
    return width;
  }

  function _widthToBytes(width, m) {
    /* データ記号数dから唯一のバイト数Bを逆算する(d→Bは一対一)。 */
    let nbytes = 0;
    while (_payloadWidth(nbytes, m) < width) nbytes++;
    if (_payloadWidth(nbytes, m) !== width) throw new Error("データ記号数が不正");
    return nbytes;
  }

  function bigintToBytes(value, size) {
    if (value < 0n) throw new Error("整数が負");
    const out = new Uint8Array(size);
    for (let i = size - 1; i >= 0; i--) { out[i] = Number(value & 255n); value >>= 8n; }
    if (value) throw new Error("int too big to convert");
    return out;
  }

  function bytesToHex(bytes) {
    return Array.from(bytes, x => x.toString(16).padStart(2, "0")).join("");
  }

  function decode(measuredFreqs, cfg, positionsKnown) {
    positionsKnown = positionsKnown === undefined ? true : positionsKnown;
    if (!Array.isArray(measuredFreqs) || !measuredFreqs.length || measuredFreqs.some(f => !(f > 0))) {
      return {payload: new Uint8Array(), payloadHex: "", decisions: [], status: "error: 正の周波数が必要", symbols: [], correctedCount: 0, erasureCount: 0};
    }
    let table;
    try { table = slots(cfg); } catch (e) {
      return {payload: new Uint8Array(), payloadHex: "", decisions: [], status: "error: " + e.message, symbols: [], correctedCount: 0, erasureCount: 0};
    }
    const ri = refSlotIndex(cfg);
    let rp = 0;
    if (!positionsKnown) {
      rp = measuredFreqs.reduce((best, f, i) =>
        Math.abs(1200 * Math.log2(f / table[ri].freq_hz)) < Math.abs(1200 * Math.log2(measuredFreqs[best] / table[ri].freq_hz)) ? i : best, 0);
    }
    const ref = measuredFreqs[rp];
    const data = measuredFreqs.slice(0, rp).concat(measuredFreqs.slice(rp + 1));
    const ratios = table.map(s => s.freq_hz / table[ri].freq_hz);
    const guard = cfg.decision_guard_cents == null ? cfg.step_cents / 2 : cfg.decision_guard_cents;
    const decisions = [], wire = [], erased = new Set();
    data.forEach((f, j) => {
      const residuals = ratios.map(x => 1200 * Math.log2((f / ref) / x));
      let index = 0;
      for (let i = 1; i < residuals.length; i++) if (Math.abs(residuals[i]) < Math.abs(residuals[index])) index = i;
      const bad = Math.abs(residuals[index]) > guard;
      decisions.push({slotIndex: index, slot_index: index, residualCents: residuals[index], residual_cents: residuals[index], isErasure: bad, is_erasure: bad, corrected: false});
      wire.push(index);
      if (bad) erased.add(j);
    });
    const m = table.length, p = _prime(m), w = _width(m, p);
    try {
      if (wire.length % w) throw new Error("記号数が不正");
      const received = [], erasures = new Set();
      for (let start = 0; start < wire.length; start += w) {
        let value = Number(_fromBase(wire.slice(start, start + w), m));
        const pos = start / w;
        if (value >= p || Array.from({length: w}, (_, i) => start + i).some(i => erased.has(i))) {
          erasures.add(pos); value %= p;
        }
        received.push(value);
      }
      const blockSize = p - 1, changed = new Set(), msg = [];
      for (let start = 0; start < received.length; start += blockSize) {
        const block = received.slice(start, start + blockSize);
        if (block.length < cfg.ecc_parity + 1) throw new Error("RSブロック長が不正");
        const blockErasures = new Set(Array.from(erasures).filter(pos => start <= pos && pos < start + block.length).map(pos => pos - start));
        const [decoded, blockChanged] = _rsDecode(block, cfg.ecc_parity, p, blockErasures);
        blockChanged.forEach(pos => changed.add(start + pos));
        msg.push(...decoded.slice(0, block.length - cfg.ecc_parity));
      }
      let payload, outSymbols;
      if (cfg.mode === "symbols") {
        payload = new Uint8Array(); outSymbols = msg;
      } else {
        const size = _widthToBytes(msg.length, m);
        payload = bigintToBytes(_fromBase(msg, m), size);
        outSymbols = wire;
      }
      changed.forEach(pos => {
        for (let j = pos * w; j < Math.min((pos + 1) * w, decisions.length); j++) decisions[j].corrected = true;
      });
      return {payload, payloadHex: bytesToHex(payload), decisions, status: changed.size ? "corrected" : "ok", symbols: outSymbols, correctedCount: changed.size, erasureCount: erasures.size};
    } catch (e) {
      return {payload: new Uint8Array(), payloadHex: "", decisions, status: "error: " + e.message, symbols: wire, correctedCount: 0, erasureCount: erased.size};
    }
  }

  return {noteToMidi, midiToNote, noteToFreq, slots, decode, bytesToHex,
    _generator, _rsEncode, _rsDecode, _syndromes, _solve, _toBase, _fromBase,
    _prime, _width, _payloadWidth, _widthToBytes};
});
