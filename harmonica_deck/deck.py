"""ハーモニカライク・カード笛デッキ生成器。

コンセプト:
  ダイアトニック・ハーモニカは調ごとに1本あり、Cのハーモニカは C major と（同じ白鍵で）その平行調
  A minor を担当する。これをコード笛カードで再現する。1枚のコード笛カード＝1つのハーモニカ（1調）。

からくり（既存コード笛の拡張）:
  クリーン域 F6→E7 は半音でちょうど長7度＝12ピッチクラスが1つずつ入る「窓」。だから任意調の
  ダイアトニック7音を、オクターブ一意でこの窓に必ず落とせる。7音を三度連鎖に並べると、隣り合う3本が
  その調のダイアトニック三和音になる。

各カードの並び（8本・度数連鎖 2·4·6·1·3·5·7·2）:
  この8本窓は、隣接3本ステップ1で 6 つの主要三和音を与える:
      (2,4,6)=ii   (4,6,1)=IV  (6,1,3)=vi  (1,3,5)=I  (3,5,7)=iii  (5,7,2)=V
  ＝ Cなら Dm F Am C Em G。これは C major の I·IV·V·ii·iii·vi と、平行 A minor(自然的短音階) の
  i(Am)·iv(Dm)·v(Em)·III(C)·VI(F)·VII(G) を同時に含む。つまり1枚でメジャーと平行ナチュラルマイナーの
  常用和音を全部カバーする（唯一欠けるのは誰も使わない vii°=Bdim と、和声的短調の V=E major＝
  導音G#を要するので白鍵ハーモニカでは出せない＝実機ハーモニカと同じ制約）。

  度数2が両端に重複する＝同じ長さの笛が2本、左右端に来る（幾何的に無問題）。8本で幅約53.9mmは
  クレジットカード短辺53.98mmにちょうど収まる。
"""
import os
import sys

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, os.pardir, "fue"))
import chordflute
import halfcut
import namecard

CARDS = os.path.join(HERE, "cards")
CARDS_BOSS = os.path.join(HERE, "cards_boss")     # ストラップ穴に補強ボスを付けた別バージョン
NAMES = chordflute.NAMES

# ダイアトニック・ハーモニカの調は12種（クロマチックの各キー）。実機ハーモニカの慣用表記に合わせ、
# Db/Eb/Ab/Bb はフラット、F# はシャープで表示する。計算用の根音はシャープ名(NAMES準拠)で持つ。
# (計算用root, 表示ラベル=メジャー/平行短調)
KEYS = [
    ("C",  "C / Am"),
    ("G",  "G / Em"),
    ("D",  "D / Bm"),
    ("A",  "A / F#m"),
    ("E",  "E / C#m"),
    ("B",  "B / G#m"),
    ("F#", "F# / D#m"),
    ("C#", "Db / Bbm"),
    ("G#", "Ab / Fm"),
    ("D#", "Eb / Cm"),
    ("A#", "Bb / Gm"),
    ("F",  "F / Dm"),
]

# 度数連鎖 2·4·6·1·3·5·7·2（8本）。隣接3本で ii·IV·vi·I·iii·V の6三和音。
DECK_DEGREES = [2, 4, 6, 1, 3, 5, 7, 2]


def deck_chain(root):
    """調 root の8本カードの音名リスト（F6..E7 窓に配置済み）。"""
    sc = chordflute._major_scale(root)                      # 長音階7音（ピッチクラス名）
    return [chordflute._place_in_window(sc[d - 1]) for d in DECK_DEGREES]


# 全カードで刻印帯の開始xを揃える固定値＝全キーの連鎖に現れる最長管（=最低音F6, 約74.7mm）の先端＋1.5mm。
# どのカードもこの位置なら最長管を侵さず、かつカード端からの刻印座標が全カードで同一になる。
FIXED_BAND_X0 = max(halfcut.length_for_note(n) for root, _ in KEYS for n in deck_chain(root)) + 1.5


def tonic_note(root):
    """調 root の「ド」（主音・度数1）を F6..E7 窓に配置した音名。＊の目印を打つ笛。"""
    return chordflute._place_in_window(chordflute._major_scale(root)[0])


def _quality(pcs):
    """3ピッチクラス集合の三和音の種類を判定（root基準の音程で major/minor/dim/?）。"""
    for r in pcs:
        ivs = sorted(((NAMES.index(p) - NAMES.index(r)) % 12) for p in pcs)
        if ivs == [0, 4, 7]:
            return r, "major"
        if ivs == [0, 3, 7]:
            return r, "minor"
        if ivs == [0, 3, 6]:
            return r, "dim"
    return pcs[0], "?"


def triads_of(chain):
    """カードの隣接3本（ステップ1）が作る三和音の一覧 [(3本の音名, 'C major'等) ...]。"""
    out = []
    for i in range(len(chain) - 2):
        w = chain[i:i + 3]
        pcs = [n[:-1] for n in w]                           # 音名（オクターブ除去）
        root, qual = _quality(pcs)
        out.append((w, "%s %s" % (root, qual)))
    return out


def build_card(root, label, credit=True, boss=False):
    """1調のコード笛カードを生成。boss=True でストラップ穴まわりに4mm厚の補強ボスを足す別版。"""
    chain = deck_chain(root)
    cx, cy = (namecard.CREDIT_X, namecard.CREDIT_Y) if credit else (namecard.CARD_X, namecard.CARD_Y)
    r = namecard.CREDIT_CORNER_R if credit else namecard.CORNER_R
    m, info = namecard.build(notes=chain, card=(cx, cy, namecard.CARD_Z),
                             corner_r=r, corner_style="round", label=label,
                             band_x0=FIXED_BAND_X0, star_note=tonic_note(root),
                             strap=True, strap_d=6.0, strap_boss=boss, boss_d=9.0)
    return m, info, chain, triads_of(chain)


def main():
    analyze = "--analyze" in sys.argv or "--dry" in sys.argv   # 生成せず解析だけ
    boss = "--boss" in sys.argv                                # ストラップ穴に補強ボスを付けた別版
    outdir = CARDS_BOSS if boss else CARDS
    if not analyze:
        os.makedirs(outdir, exist_ok=True)
    ver = "補強ボス付き(別版)" if boss else "素の穴"
    print("=== ハーモニカライク・カード笛デッキ（%d調・ストラップ穴%s）===" % (len(KEYS), ver))
    print("各カード=8本(度数 2·4·6·1·3·5·7·2)・クレジットカード85.6×53.98×4.0mm・刻印=調性\n")
    for root, label in KEYS:
        chain = deck_chain(root)
        tris = triads_of(chain)
        print("[%s]  並び(F6..E7): %s" % (label, " ".join(chain)))
        print("     隣接3本の和音: %s" % "  ".join("%s=%s" % ("".join(w), c) for w, c in tris))
        if not analyze:
            safe = label.replace(" ", "").replace("/", "_").replace("#", "s")
            m, info, _, _ = build_card(root, label, boss=boss)
            fn = os.path.join(outdir, "card_%s.stl" % safe)
            m.export(fn)
            print("     -> %s  外形%s watertight=%s" %
                  (os.path.relpath(fn, HERE), info["extents"], info["watertight"]))
        print()


if __name__ == "__main__":
    main()
