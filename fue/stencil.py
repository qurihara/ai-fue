"""ステンシル文字を「板を貫く穴」として彫るためのユーティリティ。

狙い: 笛つきカードの余白帯に「C major」のような文字を、板(0.5mm)を貫通する穴として刻む。
穴＝インク(文字の塗り)そのものを型抜きするので、O/A/D/B/8 等の閉じた"カウンター"(字の中の島)が
周囲の板から切り離されて脱落する。これを避けるのが本来ステンシルフォントの役目。

既定フォント＝Black Ops One（fue/fonts/ に同梱・SIL Open Font License）。設計段階で橋(ブリッジ)が入った
本物のステンシル書体なので、閉じたカウンターが生じず（島=0）、美しく確実に型抜きできる。全12調ラベル
＋"C major"/"F major" で島0・全グリフ有りを検証済み（'#' '/' 小文字 b も可）。

保険として、非ステンシルのフォントを渡された場合に備え、**カウンター(interior ring)が残ったら橋を自動で
架ける**フォールバックも残す（本物ステンシルでは interior ring が生じないので no-op）。

方式:
  1. matplotlib.textpath.TextPath でテキストのアウトライン輪郭を得る。
  2. even-odd規則（輪郭のXOR＝symmetric_difference）で「塗り」ポリゴン（穴になる領域）を作る。
  3. もしカウンター（interior ring）が残っていれば、その代表点から字の上端の外まで伸びる細い縦長方形
     （ブリッジ）を塗りから差し引いて島を地続きにする（ステンシルフォント使用時は該当なし）。
  4. 仕上げた2Dポリゴンを返す（呼び出し側で任意の姿勢に配置し、押し出して板から差し引く）。
"""
import os
import numpy as np
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties
from shapely.geometry import Polygon, MultiPolygon, box as sbox
from shapely.ops import unary_union
from shapely.affinity import scale as _scale, translate as _translate, rotate as _rotate

# 既定＝同梱の Black Ops One（本物のステンシル書体・OFL）。無ければ太字サンセリフに退避（橋を自動生成）。
_FONT_PATH = os.path.join(os.path.dirname(__file__), "fonts", "BlackOpsOne-Regular.ttf")
if os.path.exists(_FONT_PATH):
    _FP = FontProperties(fname=_FONT_PATH)
else:
    _FP = FontProperties(family="sans-serif", weight="bold")


def _fill_polygon(text, fp=None):
    """テキストのアウトラインを even-odd(XOR) で塗りつぶした shapely 図形にする。
    size=100 の局所座標（ベースラインが y=0）で返す。カウンターは interior ring として残る。"""
    fp = fp or _FP
    tp = TextPath((0, 0), text, size=100, prop=fp)
    rings = [np.asarray(p) for p in tp.to_polygons() if len(p) >= 3]
    polys = []
    for r in rings:
        p = Polygon(r)
        if not p.is_valid:
            p = p.buffer(0)                    # 自己接触などを修復
        if not p.is_empty:
            polys.append(p)
    if not polys:
        return None
    fill = polys[0]
    for p in polys[1:]:
        fill = fill.symmetric_difference(p)    # even-odd 塗り＝XOR
    return fill


def _stencilize(fill, bridge_w, top_y):
    """各カウンター(interior ring)に縦ブリッジを架けてステンシル化。
    fill から、カウンター重心xを中心に幅 bridge_w・上端が top_y を超える縦長方形を差し引く。"""
    geoms = list(fill.geoms) if isinstance(fill, MultiPolygon) else [fill]
    bridges = []
    for g in geoms:
        for ring in g.interiors:
            c = Polygon(ring).representative_point()   # カウンター内部の1点（重心が字画に載る字でも安全）
            bx0, bx1 = c.x - bridge_w / 2.0, c.x + bridge_w / 2.0
            by0 = c.y                                   # カウンター内部から
            by1 = top_y + 5.0                           # 字の上端の外へ抜ける
            bridges.append(sbox(bx0, by0, bx1, by1))
    if not bridges:
        return fill
    return fill.difference(unary_union(bridges))


def text_holes(text, height, width_max=None, bridge_w=1.0, fp=None):
    """刻印する穴のポリゴン（ステンシル化済み）を返す。局所座標: x=右へ字が進む, y=上, 左下寄せ。
      height    … 文字帯の高さ[mm]（テキスト全体の縦の外形をこれに合わせる）
      width_max … 与えると、この幅[mm]を超える場合に等方縮小して収める
      bridge_w  … ブリッジ（島を保持する橋）の幅[mm]。細すぎると印刷で切れ、太いと字が割れる。0.8〜1.4推奨。
    戻り値: (poly, (w, h))  poly=shapely図形（穴）, (w,h)=配置後の外形[mm]。
    """
    fill = _fill_polygon(text, fp=fp)
    if fill is None or fill.is_empty:
        raise ValueError("空のテキスト、またはグリフ生成に失敗: %r" % text)
    minx, miny, maxx, maxy = fill.bounds
    s = height / (maxy - miny)                          # 縦をheightに合わせる
    if width_max is not None and (maxx - minx) * s > width_max:
        s = width_max / (maxx - minx)                   # 幅超過なら幅で律速
    fill = _scale(fill, xfact=s, yfact=s, origin=(0, 0))
    minx, miny, maxx, maxy = fill.bounds
    fill = _translate(fill, xoff=-minx, yoff=-miny)     # 左下を原点へ
    _, _, w, h = fill.bounds
    poly = _stencilize(fill, bridge_w=bridge_w, top_y=h)
    return poly, (w, h)


def asterisk(cx, cy, r, bar_w=None, arms=3):
    """＊（アスタリスク）ポリゴンを返す。arms本のバーを中心で放射状に交差＝2*arms本の腕。
    穴として彫るのに使う（連結した1図形なので島は生じない）。既定 arms=3 → 6本腕の＊。"""
    bar_w = bar_w if bar_w is not None else r * 0.5
    bars = []
    for k in range(arms):
        b = sbox(-r, -bar_w / 2.0, r, bar_w / 2.0)
        bars.append(_rotate(b, 180.0 * k / arms, origin=(0, 0)))
    a = unary_union(bars)
    return _translate(a, cx, cy)


def place_along_y(poly, size, x0, y_center, mirror=False):
    """局所(x=字送り, y=字高) を カードの (card_x=帯の奥行き, card_y=字送り) へ写す。
    カードを縦(短辺=横)に持ったとき文字が正立して読める向き。
      x0        … 帯の下端 card_x（ここから字高ぶん +x へ立ち上がる）
      y_center  … 文字列を card_y 方向にセンタリングする中心
    局所x→card_y, 局所y→card_x（転置）になるので鏡像を避けるため既定で y を反転して写す。
    戻り値: カード座標に配置した shapely図形。
    """
    w, h = size
    # 局所(x,y)->(card_x,card_y): card_x = x0 + y,  card_y = (w - x) + (y_center - w/2)  ← 鏡像回避
    p = _rotate(poly, 90, origin=(0, 0))          # (x,y)->(-y,x)
    # rotate90: 点(x,y)->(-y,x). これで new_x=-y, new_y=x。new_xを+へ、原点補正。
    p = _translate(p, xoff=h, yoff=0)             # new_x を 0..h に戻す（-h..0 -> 0..h）
    if mirror:
        p = _scale(p, xfact=1, yfact=-1, origin=(0, 0))
        p = _translate(p, xoff=0, yoff=w)
    # ここで p は x:0..h（字高）, y:0..w（字送り）
    p = _translate(p, xoff=x0, yoff=y_center - w / 2.0)
    return p
