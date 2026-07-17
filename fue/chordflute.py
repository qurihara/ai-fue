"""コード笛：半割り笛を三度連鎖に並べ、隣り合う3本を同時に吹くと和音が鳴るコーム。

着想（栗原さん）: 笛を上手に並べて「左から3音ずつ取り出すと IV・I・V の和音になる」ようにしたい。
展開形（インバージョン）と、必要なら移調で、いま使えるクリーン域に収められないか。

■ からくり: 三度連鎖
  IV・I・V の3和音を、共有音でつなぐと1本の連鎖になる。C majorなら:
      IV = F A C
      I  =     C E G      （IV と C を共有）
      V  =         G B D  （I  と G を共有）
  重ねると  F A C E G B D  ＝ 7音の連鎖。左から幅3の窓を1音ずつ重ねて滑らせると:
      [F A C] = IV,  [C E G] = I,  [G B D] = V
  つまり7本の笛を並べ、1〜3本目を吹けばIV、3〜5本目でI、5〜7本目でV。
  3本目(C)と5本目(G)は2つの和音で共有される「ピボット笛」。

■ 移調は要らない（展開形だけで収まる）:
  我々のクリーン域は F6→E7。これは半音でちょうど長7度＝F,F#,…,E の12ピッチクラスが1つずつ入る窓。
  だから任意のピッチクラスは、この窓の中でオクターブが一意に決まる。7音の連鎖 F A C E G B D を
  それぞれ窓に落とすと、根音位置では2オクターブ近く跨ぐ和音が、自動的に「展開形」に畳まれて全部収まる:
      F6  A6  C7  E7  G6  B6  D7
  各和音は
      [F6 A6 C7] = F majorの根音位置(IV)
      [C7 E7 G6] = C majorの第2転回(I)   ← G6が最低音
      [G6 B6 D7] = G majorの根音位置(V)
  すべて F6(74.7mm)〜E7(44.7mm) のクリーン域内。C major がちょうど両端に収まる。

  （他のキーでも同様に収まる。C majorは最長がF6・最短がE7で両端いっぱい。安全側に寄せたいなら
   G/D/A/E majorは最長がF#6(71mm)止まりで低音側にわずかに余裕がある。CHORD_KEYS 参照。）
"""
import os
import sys
import numpy as np
import trimesh

sys.path.insert(0, os.path.dirname(__file__))
import halfcut

OUT = os.path.join(os.path.dirname(__file__), os.pardir, "out")
NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']


def _pc(n):
    return NAMES.index(n)


def _place_in_window(pitchclass, lo='F'):
    """ピッチクラスを F6..E7 の窓に一意配置。F..B→oct6 / C..E→oct7。"""
    off = (_pc(pitchclass) - _pc(lo)) % 12          # F からの上向き半音 0..11
    octv = 6 if off <= (_pc('B') - _pc('F')) else 7
    return "%s%d" % (pitchclass, octv)


def _major_scale(root):
    return [NAMES[(_pc(root) + s) % 12] for s in (0, 2, 4, 5, 7, 9, 11)]


def chord_chain_notes(root="C"):
    """IV·I·V を三度連鎖にした7音を、F6..E7 の窓に収めた音名リストを返す。
    度数連鎖 4·6·1·3·5·7·2（ピボット=1度と5度）。"""
    sc = _major_scale(root)
    chain_pc = [sc[d - 1] for d in (4, 6, 1, 3, 5, 7, 2)]
    return [_place_in_window(p) for p in chain_pc]


# 既定＝C major（栗原さんの例と同じ。IV I V = F C G の最も基本的なカデンツ）。
# 並びは 4·6·1·3·5·7·2 連鎖のうち外側ペアを長→短に整えた F6 A6 C7 E7 G6 B6 D7。
CHORD_CMAJOR = ["F6", "A6", "C7", "E7", "G6", "B6", "D7"]
CHORD_KEYS = ["C", "G", "D", "A", "E", "F"]     # どれもクリーン域に収まる

# 8本版（名刺は8本＝幅53.6mmが収まる）。7本鎖の右端に1本足して和音進行を多彩化する。
# クリーン域(F6-E7=長7度)は7音でちょうど埋まるので、8本目は必ず半音(黒鍵)＝借用/転調の音になる。
# 右端 [B6 D7 X] が綺麗な三和音になるのは X=F#6(→Bm) か G#6(→G#dim) の2つだけ（実測探索）。
#
# ▼本命 CHORD8_TO_G（+F#6）: 深いアルペジオ(4本窓)が Fmaj7·Am7·Cmaj7·Em7·Gmaj7 の全ダイアトニック7th。
#   F#で C major∪G major の全音を保持＝属調Gへ転調できる。IV·I·V(左から3本ずつ)はそのまま残る。
CHORD8_TO_G = CHORD_CMAJOR + ["F#6"]
# ▼陰り CHORD8_TO_AM（+G#6）: 右端3本が G#dim(vii°/vi)→ Am へ解決＝平行短調の翳りを足す。
#   ただし4本窓 G B D G# は濁る（深いアルペジオには不向き。3本で切るなら綺麗）。
CHORD8_TO_AM = CHORD_CMAJOR + ["G#6"]


def windows(notes):
    """幅3・ステップ2の窓＝3和音を返す [(ラベル, [音名×3]) ...]。"""
    labels = ["IV", "I", "V"]
    return [(labels[k], notes[2 * k:2 * k + 3]) for k in range(3)]


def build(notes=None):
    """コード笛コーム（7本を一列に融合）。戻り値 (mesh, infos, notes, lengths)。
    scale_comb は渡した順序をそのまま左→右に並べる（音名リストの並び＝物理配置）。"""
    if notes is None:
        notes = CHORD_CMAJOR
    comb, infos, notes, lengths = halfcut.scale_comb(notes=notes)
    return comb, infos, notes, lengths


def main():
    os.makedirs(OUT, exist_ok=True)
    root = "C"
    if "--to-g" in sys.argv:
        notes, stem, root = CHORD8_TO_G, "chordflute8_toG", "C(+F#→G)"
    elif "--to-am" in sys.argv:
        notes, stem, root = CHORD8_TO_AM, "chordflute8_toAm", "C(+G#→Am)"
    else:
        for a in sys.argv[1:]:
            if a.startswith("--key="):
                root = a[6:]
        notes = CHORD_CMAJOR if root == "C" else chord_chain_notes(root)
        stem = "chordflute_%smajor" % root.replace("#", "s")
    comb, infos, notes, lengths = build(notes=notes)
    name = os.path.join(OUT, stem + ".stl")
    comb.export(name)

    print("コード笛（IV·I·V 三度連鎖・%s major・隣接3本で和音）:" % root)
    for it in infos:
        print("    %-3s L=%4.1fmm  行y=%5.1f  予測 %5.0fHz" % (it["note"], it["L"], it["y"], it["freq"]))
    print("  和音（左から幅3・1音重ねて滑らせる。★=ピボット笛）:")
    for lab, w in windows(notes):
        print("    %-2s = %s" % (lab, " ".join(w)))
    print("    ピボット: 3本目 %s（IV↔I）, 5本目 %s（I↔V）" % (notes[2], notes[4]))
    lo, hi = halfcut.length_for_note("F6"), halfcut.length_for_note("E7")
    inrange = all(hi - 0.6 <= L <= lo + 0.6 for L in lengths)
    print("  クリーン域 F6(%.1f)〜E7(%.1f) 内=%s   外形=%s watertight=%s 体積=%.2fcm3" %
          (lo, hi, inrange, tuple(np.round(comb.extents, 1)), comb.is_watertight, comb.volume / 1000.0))
    print("  -> %s" % name)


if __name__ == "__main__":
    main()
