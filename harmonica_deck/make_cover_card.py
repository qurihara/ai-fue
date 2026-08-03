"""Chordika デッキの表紙カードを生成する。

笛は入っておらず、Chordika の文字をステンシル（貫通穴）で刻んだだけの薄い板である。
板厚はデッキの各カードの床と同じ 0.5mm で、ストラップ穴の位置も各カードと揃えてある。
12枚のカードと重ねて箱に収め、いちばん上に置く一枚として使う。

生成の実体は fue/namecard.py の build_cover にある。この場所に置いてあるのは、
表紙を作り直したくなったときに同じものが確実に出てくるようにするためである。

  python3 harmonica_deck/make_cover_card.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.pardir, "fue"))
import namecard

OUT = os.path.join(os.path.dirname(__file__), os.pardir, "out")

TITLE = "Chordika"


def main():
    mesh, info = namecard.build_cover(title=TITLE)
    path = os.path.join(OUT, "chordika_cover.stl")
    mesh.export(path)
    print("書き出し %s" % os.path.relpath(path))
    print("  外形: %.2f x %.2f x %.2f mm" % info["extents"])
    print("  文字: %s（高さ %.1fmm・幅 %.1fmm）" % (info["title"], info["title_h"], info["title_w"]))
    print("  ストラップ穴: 直径%.1fmm  中心(%.1f, %.1f)" % (
        info["strap"]["d"], info["strap"]["x"], info["strap"]["y"]))
    print("  水密: %s" % info["watertight"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
