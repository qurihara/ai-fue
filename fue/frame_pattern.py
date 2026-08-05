"""絵の外周に置く枠模様と、それに合う額縁の箱。

なぜ枠模様が要るか
------------------
画像をタイルに割ると、絵の薄い場所に当たったタイルが真っ白になり、[* どのタイルか
区別が付かなくなる]。北斎「神奈川沖浪裏」を3列3行に割ると、右上の1枚がほぼ真っ白に
なる。外周に模様の帯を置けば、少なくとも「上辺の1枚」「左上の角の1枚」という位置の
手がかりが必ず乗る。

塗り潰した黒帯ではなく[* 模様]にするのは、絵として見たときに額縁らしく見せるためと、
模様の切れ方そのものが位置の手がかりになるためである。

つなぎ目が合う仕組み
--------------------
模様は[* 絵全体の座標で一度に作り]、それをタイルに割る。タイルごとに作らないので、
隣どうしのつなぎ目は必ず合う。額縁の箱も同じ座標系で作るので、箱の縁からタイルの縁へ
模様が途切れずに続く。

模様は3種類から選べる。
  seigaiha … 青海波。重なる半円の連なり。波の絵と呼応する
  ichimatsu … 市松。正方形の互い違い。位置がいちばん読み取りやすい
  sayagata … 紗綾形。卍を崩した連続文様。密度が高く、細部が出るかは要確認
"""
from __future__ import annotations

import math

import numpy as np
from shapely.geometry import Point, Polygon, box as sbox
from shapely.ops import unary_union


def polys_only(g):
    """面だけを残す。

    交差の結果には線や点が混じることがあり、そのまま押し出すと
    「立体ではない」と拒まれる（2026-07-31に箱で踏んだ）。
    """
    from shapely.geometry import MultiPolygon, Polygon
    if isinstance(g, Polygon):
        return g if not g.is_empty else Polygon()
    parts = [x for x in getattr(g, "geoms", []) if isinstance(x, Polygon) and not x.is_empty]
    return MultiPolygon(parts) if parts else Polygon()


def _band(w, h, t):
    """外周の帯（幅 t）を返す。"""
    return sbox(0, 0, w, h).difference(sbox(t, t, w - t, h - t))


def seigaiha(w, h, t=6.0, r=3.0, lw=0.8, rings=2):
    """青海波。[* 上半分の弧]だけを鱗のように重ねて並べる。

    同心円をまるごと重ねると線が密集して塗り潰しに近くなる（2026-07-31に一度そうなった）。
    本来の青海波は半円の弧の連なりなので、下半分を落とす。
    r は弧の半径、lw は線の太さで、押出線（0.42mm）より確実に太くする。
    """
    shapes = []
    dx, dy = r * 2.0, r * 0.7
    for j in range(-2, int(h / dy) + 3):
        for i in range(-2, int(w / dx) + 3):
            cx = i * dx + (r if j % 2 else 0.0)
            cy = j * dy
            for k in range(1, rings + 1):
                rr = r * k / rings
                ring = Point(cx, cy).buffer(rr, resolution=48).exterior.buffer(lw / 2.0)
                upper = ring.intersection(sbox(cx - rr - lw, cy, cx + rr + lw, cy + rr + lw))
                if not upper.is_empty:
                    shapes.append(upper)
    return unary_union(shapes).intersection(_band(w, h, t))


def ichimatsu(w, h, t=6.0, cell=6.0):
    """市松。正方形を互い違いに置く。"""
    shapes = []
    for j in range(int(h / cell) + 2):
        for i in range(int(w / cell) + 2):
            if (i + j) % 2:
                continue
            shapes.append(sbox(i * cell, j * cell, (i + 1) * cell, (j + 1) * cell))
    return unary_union(shapes).intersection(_band(w, h, t))


def sayagata(w, h, t=6.0, cell=8.0, lw=1.0):
    """紗綾形に近い連続文様。卍崩しを、折れ線の帯で近似する。"""
    segs = []
    for j in range(-1, int(h / cell) + 2):
        for i in range(-1, int(w / cell) + 2):
            x, y = i * cell, j * cell
            c = cell
            pts = [(x, y + c * 0.5), (x + c * 0.5, y + c * 0.5), (x + c * 0.5, y),
                   (x + c, y), (x + c, y + c * 0.5), (x + c * 0.5, y + c * 0.5),
                   (x + c * 0.5, y + c), (x, y + c)]
            for a, b in zip(pts, pts[1:]):
                segs.append(Polygon([a, b, b, a]).buffer(lw / 2.0, cap_style=2)
                            if a != b else Point(a).buffer(lw / 2.0))
    from shapely.geometry import LineString
    segs = []
    for j in range(-1, int(h / cell) + 2):
        for i in range(-1, int(w / cell) + 2):
            x, y = i * cell, j * cell
            c = cell
            pts = [(x, y + c * 0.5), (x + c * 0.5, y + c * 0.5), (x + c * 0.5, y),
                   (x + c, y), (x + c, y + c * 0.5), (x + c * 0.5, y + c * 0.5),
                   (x + c * 0.5, y + c), (x, y + c)]
            segs.append(LineString(pts).buffer(lw / 2.0, cap_style=2, join_style=2))
    return unary_union(segs).intersection(_band(w, h, t))


PATTERNS = dict(seigaiha=seigaiha, ichimatsu=ichimatsu, sayagata=sayagata)


def frame_polygon(name, w, h, t=6.0, **kw):
    """名前で模様を作る。返り値は絵全体の座標に置かれた平面図形。"""
    if name not in PATTERNS:
        raise ValueError("知らない模様: %s（%s から選ぶ）" % (name, "・".join(PATTERNS)))
    return polys_only(PATTERNS[name](w, h, t=t, **kw))


def preview(poly, w, h, path, scale=4, extra=None, grid=None):
    """模様を絵にして確かめる。grid=(列, 行) を渡すとタイルの境目も描く。"""
    from PIL import Image, ImageDraw
    from shapely.geometry import MultiPolygon
    img = Image.new("L", (int(w * scale), int(h * scale)), 255)
    d = ImageDraw.Draw(img)

    def draw(p, fill):
        geoms = list(p.geoms) if hasattr(p, "geoms") else [p]
        for g in geoms:
            # 交差の結果には線や点が混じることがあるので、面だけを描く
            if g.is_empty or not hasattr(g, "exterior"):
                continue
            d.polygon([(x * scale, (h - y) * scale) for x, y in g.exterior.coords], fill=fill)
            for r in g.interiors:
                d.polygon([(x * scale, (h - y) * scale) for x, y in r.coords], fill=255)

    if extra is not None:
        draw(extra, 160)
    draw(poly, 0)
    if grid:
        gx, gy = grid
        for i in range(1, gx):
            d.line([(w * i / gx * scale, 0), (w * i / gx * scale, h * scale)], fill=128, width=2)
        for j in range(1, gy):
            d.line([(0, h * j / gy * scale), (w * scale, h * j / gy * scale)], fill=128, width=2)
    img.save(path)
    return path


if __name__ == "__main__":
    import argparse
    import os
    ap = argparse.ArgumentParser(description="枠模様を作って絵にする")
    ap.add_argument("--size", default="204x194", help="絵の大きさ（mm）")
    ap.add_argument("--band", type=float, default=6.0, help="枠の帯の幅[mm]")
    ap.add_argument("--grid", default="3x3", help="タイルの格子")
    ap.add_argument("--out-dir", default="out", help="出力先")
    a = ap.parse_args()
    w, h = (float(v) for v in a.size.lower().split("x"))
    gx, gy = (int(v) for v in a.grid.lower().split("x"))
    os.makedirs(a.out_dir, exist_ok=True)
    for name in PATTERNS:
        p = frame_polygon(name, w, h, t=a.band)
        path = os.path.join(a.out_dir, "frame_%s.png" % name)
        preview(p, w, h, path, grid=(gx, gy))
        print("%-10s 面積 %.0f mm2 -> %s" % (name, p.area, path))
