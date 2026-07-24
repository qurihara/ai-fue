"""rect（直方体フィッポル笛）の「1回折り曲げ」版を生成する。

背景・経緯は cosense「AI笛作り」2026/7/23 08:35 の引き継ぎ参照。
- 基STL: mini-rect/recorder-mini-c-half-rect-1-v1.stl（直管・窓は+y面・native姿勢[60,4,7]でz7が縦=窓横向き=サポート無し印刷可）。
  x=管軸(0..60 正規化後), y=幅4, z=高7。窓は頭部x≈14付近・+y面。直管フットは x>=THR。フット平行移動で長さ可変。
- 折りの狙い: 物理長を短く・外形を長方形にしつつ、窓を露出させる。
  (1)折る向きは窓と反対の -y 側（窓+yを覆わない）。
  (2)返し脚を全長にして閉端を吸込口x=0にそろえる → 窓を無視すると外形が長方形。
     ※これによりボア量は折り前後で頭部ぶん非対称になる（承知の上）。

★重要（バグと修正）:
  fold2()＝旧版はU字溝を「キャップだけ」から差し引いてから頭部(笛)と合体していたため、
  合体時に笛のフット蓋(中実)がU字溝を埋め戻し、bore1がU字から分断される疑いが濃厚だった
  （実機・断面図で確認）。
  fold3()＝修正版は、溝(bore2, Ubore)を「頭部＋脚outer＋capouter を合体した“全体”から」差し引く。
  これでU字溝が笛のフット蓋も貫き、bore1がU字へ開いて一続きになる（はず）。
  → 次セッションで conn_check() の内部エア連結（bore1→bore2 が x>18 限定＝頭部経由せずU経由で到達）を必ず確認し、
    通れば fold3 を採用、3候補(Lp=30/40/50)を build_plate() でA1mini用に並べて印刷（swaps=1推奨）。

実行環境: /Users/kurihara/Desktop/claude_work/mesh_venv/bin/python（trimesh/manifold3d/numpy-stl/lxml 導入済）。
"""
import os
from collections import deque
import numpy as np
import trimesh

HERE = os.path.dirname(__file__)
ROOT = os.path.join(HERE, os.pardir)
OUT = os.path.join(ROOT, "out")
RB = os.path.join(HERE, "recorder-mini-c-half-rect-1-v1.stl")
THR = -16.0      # 直管フットの開始x（この基STLの生座標）
BASE_LEN = 60.0  # 基STLの物理長

# ボア/脚の寸法（基STLの正規化後の実測に基づく）。bore断面≈ y方向2.5 × z方向5、床/壁≈0.5〜1mm。
WALL = 1.2       # U字/返し脚の壁厚
CAPL = 4.0       # U字キャップの張り出し長


def flute(L):
    """物理長 L[mm] の直管rect笛。フット(x>=THR)を平行移動して長さを変える。
    返り値は x0/y0/z0 に正規化（吸込口x=0, y=0, z=0）。"""
    m = trimesh.load(RB).copy()
    v = m.vertices.copy()
    v[v[:, 0] >= THR, 0] += (L - BASE_LEN)
    m.vertices = v
    m.merge_vertices()
    b = m.bounds
    m.apply_translation([-b[0][0], -b[0][1], -b[0][2]])
    return m


def _box(x0, x1, y0, y1, z0, z1):
    b = trimesh.creation.box(extents=[x1 - x0, y1 - y0, z1 - z0])
    b.apply_translation([(x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2])
    return b


def fold2(Lp, capL=CAPL, wall=WALL):
    """【旧版・分断バグの疑い。参考用に残す】U字溝をキャップだけから差引→頭部と合体。"""
    head = flute(Lp)                                            # 脚1: y0..4, 窓+y, bore1, 吸込口x0, フットx=Lp（蓋あり）
    rleg = trimesh.boolean.difference(                          # 脚2: -y側 全長 返しbore2, 吸込口側x0は閉
        [_box(0, Lp, -4, 1.2, 0, 7), _box(wall, Lp + 1, -3.25, -0.75, 1.0, 6.0)], engine="manifold")
    cap = trimesh.boolean.difference(                          # U字キャップ（★ここだけ溝を掘る＝合体で埋め戻る）
        [_box(Lp - 1.5, Lp + capL, -4, 4, 0, 7), _box(Lp - 2.5, Lp + capL - wall, -3.25, 3.25, 1.0, 6.0)],
        engine="manifold")
    fd = trimesh.boolean.union([head, rleg, cap], engine="manifold")
    fd.merge_vertices()
    b = fd.bounds
    fd.apply_translation([-b[0][0], -b[0][1], -b[0][2]])
    return fd


def fold3(Lp, capL=CAPL, wall=WALL):
    """【修正版】溝(bore2, Ubore)を『頭部＋脚outer＋capouter を合体した全体』から差し引く。
    U字溝が笛のフット蓋も貫き、bore1がU字へ開いて一続きになる。"""
    head = flute(Lp)                                           # 頭部（窓・ウインドウェイ・bore1 は生かす）
    outer = trimesh.boolean.union(
        [head, _box(0, Lp, -4, 1.2, 0, 7), _box(Lp - 1.5, Lp + capL, -4, 4, 0, 7)], engine="manifold")
    fd = trimesh.boolean.difference(
        [outer,
         _box(wall, Lp + 1, -3.25, -0.75, 1.0, 6.0),           # bore2（返し脚）
         _box(Lp - 2.5, Lp + capL - wall, -3.25, 3.25, 1.0, 6.0)],  # Ubore（U字。フット蓋も貫く）
        engine="manifold")
    fd.merge_vertices()
    b = fd.bounds
    fd.apply_translation([-b[0][0], -b[0][1], -b[0][2]])
    return fd


def fold4(Lp, capL=CAPL, wall=WALL):
    """【開放端版】fold3 の返し脚 bore2 を頭側(x=0面)まで貫通させ、大気への開放端を作る。
    これで音響経路が『窓→bore1→U→bore2→開放端』の開管になる（fold3は閉端で高風圧・低音不発だった）。
    bore2 の切削開始xを wall(=1.2) から -1.0 に伸ばし、x=0 の端面に開口を抜く。他は fold3 と同じ。"""
    head = flute(Lp)
    outer = trimesh.boolean.union(
        [head, _box(0, Lp, -4, 1.2, 0, 7), _box(Lp - 1.5, Lp + capL, -4, 4, 0, 7)], engine="manifold")
    fd = trimesh.boolean.difference(
        [outer,
         _box(-1.0, Lp + 1, -3.25, -0.75, 1.0, 6.0),           # bore2（返し脚・頭側x=0面まで貫通＝開放端）
         _box(Lp - 2.5, Lp + capL - wall, -3.25, 3.25, 1.0, 6.0)],  # Ubore（U字）
        engine="manifold")
    fd.merge_vertices()
    b = fd.bounds
    fd.apply_translation([-b[0][0], -b[0][1], -b[0][2]])
    return fd


def open_end_check(fd, pitch=0.15):
    """返し脚bore2の頭側端が大気に開いているかを確認する。
    x=0 端面のすぐ内側(bore2位置)が空洞で、かつその外側(x<0側)が部品外＝開放、を確かめる。"""
    vg = fd.voxelized(pitch=pitch)
    occ = vg.matrix
    org = vg.transform[:3, 3]
    sh = occ.shape

    def c(p):
        return tuple(np.round((np.array(p) - org) / pitch).astype(int))

    def air(i, j, k):
        return 0 <= i < sh[0] and 0 <= j < sh[1] and 0 <= k < sh[2] and not occ[i, j, k]

    b = fd.bounds
    ybore2 = b[0][1] + 1.5     # 返し脚(-y側)の代表y
    inside = c([0.6, ybore2, 3.5])    # 端面のすぐ内側
    if not air(*inside):
        return "★端面内側が中実＝開放端が抜けていない"
    # 端面から -x 方向へ辿り、部品の外(=xが小さく材料が無い領域)へ抜けられるか
    i0, j0, k0 = inside
    for i in range(i0, -1, -1):
        if occ[i, j0, k0]:
            return "★-x方向に材料があり閉じている"
    return "開放端OK(頭側x=0面が大気に開いている)"


def conn_check(fd, pitch=0.15):
    """内部エア連結の検証。bore1(窓側+y=上) → bore2(-y=下) が、頭部(x<=18)を経由せず
    U字(フット)経由で到達するかをvoxel BFSで確認する。'連結OK(U経由)' なら折りが成立。"""
    vg = fd.voxelized(pitch=pitch)
    occ = vg.matrix
    org = vg.transform[:3, 3]
    sh = occ.shape

    def c(p):
        return tuple(np.round((np.array(p) - org) / pitch).astype(int))

    def air(i, j, k):
        return 0 <= i < sh[0] and 0 <= j < sh[1] and 0 <= k < sh[2] and not occ[i, j, k]

    b = fd.bounds
    s1 = c([25, b[1][1] - 1.5, 3.5])   # bore1（上・窓側）
    s2 = c([25, b[0][1] + 1.5, 3.5])   # bore2（下・返し）
    xl = int((18 - org[0]) / pitch)    # x>18 に限定（頭部の窓/口を除外）
    if not air(*s1) or not air(*s2):
        return "seed不良（座標がずれている。y位置を調整して再確認）"
    seen = {s1}
    dq = deque([s1])
    while dq:
        cur = dq.popleft()
        if cur == s2:
            return "連結OK(U経由)"
        i, j, k = cur
        for d in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]:
            n = (i + d[0], j + d[1], k + d[2])
            if n in seen or not air(*n) or n[0] < xl:
                continue
            seen.add(n)
            dq.append(n)
    return "★未到達=分断（fold3の溝寸法・重なりを調整）"


def build_plate(lengths=(30, 40, 50), gap=12.0, use_fold=fold3, bed=(180.0, 180.0)):
    """折り候補を y方向に並べたA1mini用プレートSTLを作る。窓+yが露出するよう間隔を空ける。"""
    placed = []
    y = 0.0
    for Lp in lengths:
        fd = use_fold(Lp)
        b = fd.bounds
        fd.apply_translation([-b[0][0], -b[0][1] + y, -b[0][2]])
        placed.append(fd)
        y += fd.extents[1] + gap
    plate = trimesh.util.concatenate(placed)
    ctr = (plate.bounds[0] + plate.bounds[1]) / 2
    plate.apply_translation([bed[0] / 2 - ctr[0], bed[1] / 2 - ctr[1], 0])
    return plate


if __name__ == "__main__":
    # 開放端版fold4の検証＋プレート出力
    for Lp in (30, 40, 50):
        fd = fold4(Lp)
        print("fold4 Lp%d ext=%s wt=%s 連結=%s 開放端=%s" % (
            Lp, np.round(fd.extents, 1).tolist(), fd.is_watertight,
            conn_check(fd), open_end_check(fd)))
    plate = build_plate((30, 40, 50), use_fold=fold4)
    out = os.path.join(OUT, "fold4_rect_3cand_a1m.stl")
    plate.export(out)
    print("wrote", out, np.round(plate.extents, 1).tolist(), "watertight=", plate.is_watertight)
