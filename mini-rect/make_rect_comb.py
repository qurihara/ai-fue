"""直管rect（直方体・深窓・壁1mm・床0.5mm）の較正／限界コームを生成する。

背景は cosense「AI笛作り」2026/7/23 の引き継ぎ参照。印刷済みの
out/comb_rect_calib5_zstack_base.stl（5本z積み＋底ベース）を作った生成器は
セッション消滅で残っていなかったため、再現可能な形でここに整備する。

方式（H2Dで定着FAILEDを避けるための実績パターン）:
  - 各管は make_fold_rect.flute(L) の直管rect（窓+y面・native姿勢[L,4,7]）。
  - z方向に OVERLAP だけ重ねて積み、boolean union で一体化（連続接地）。
    窓は各管の+y側面（中ほどのz）にあり、重なりは上下端だけなので塞がらない。
  - 足元に底ベース（薄い床スラブ）を付けてベッド接地面積を広げる（塔が細く倒れる/剥離するのを防ぐ）。
    ベースは窓と反対の -y 側へ張り出させ、窓の前を塞がない。
  - 吸込口(x=0)をそろえ、短い管を下・長い管を上に積む。

実行環境: /Users/kurihara/Desktop/claude_work/mesh_venv/bin/python
"""
import os
import numpy as np
import trimesh
from make_fold_rect import flute, _box  # flute(L): 直管rect（x0/y0/z0正規化）

HERE = os.path.dirname(__file__)
ROOT = os.path.join(HERE, os.pardir)
OUT = os.path.join(ROOT, "out")

A, E = 84910.0, -11.24         # rect直管 較正フィット(2026/7/23実測4本, RMS25.6cent)。out/rect_calib_fit.txt
def predf(L): return A / (L + E)

TUBE_H = 7.0                    # 管の高さ（z）
OVERLAP = 0.3                   # z積みの重なり（融合のため）
BASE_H = 0.8                    # 底ベースの厚み（z）。平置き横並びは低く安定なので薄く（定着用の最小限）。
                                # 窓クリアランスは管をベース厚ぶん持ち上げる設計のため、ベース厚に依らず
                                # 0.5-OVERLAP=0.2mm で一定（限界コームで0.2mmでも低音が良く鳴った実績）。
BASE_W = 24.0                   # 底ベースのy方向の全幅（笛を中央に立てて左右対称に張り出す）
TUBE_W = 4.0                    # 管のy方向の幅


def build_zstack(lengths, base=True, xmargin=4.0):
    """lengths を長い順に下から z 積みし一体化。base=True で底ベースを付ける。
    返り値: (mesh, infos)。窓は+y面、吸込口x=0そろえ。
    長い管を最下段に置くことで、各上段（短い管）が必ず下段の長い管の上に載り、
    x方向にはみ出す張り出し（オーバーハング）が生じない＝サポート無しで印刷できる。
    さらに、管を底ベースの厚みぶん持ち上げてベースの『上』に立て、ベースを管のy中心
    まわりに左右対称（BASE_W幅）へ広げる。窓はz=0.5以上に開くが、管をベース厚(2mm)だけ
    持ち上げるので全ての窓がベース上面より高くなり、ベースを窓側(+y)へ広げても塞がない。"""
    lengths = sorted(lengths, reverse=True)   # 長い管を下に（自己支持のため）
    tubes = []
    z0 = BASE_H - OVERLAP if base else 0.0    # 管をベースの上に乗せる（0.3だけ食い込ませ融合）
    infos = []
    for L in lengths:
        t = flute(L)               # x0/y0/z0 正規化（吸込口x=0, y=0, z=0）
        t.apply_translation([0, 0, z0])
        tubes.append(t)
        infos.append(dict(L=L, z0=round(z0, 2), predHz=round(predf(L))))
        z0 += TUBE_H - OVERLAP
    parts = list(tubes)
    if base:
        maxL = max(lengths)
        yc = TUBE_W / 2.0          # 管のy中心
        # 床スラブ: x=0..maxL+margin, y=管中心まわりに±BASE_W/2（左右対称）, z=0..BASE_H
        parts.append(_box(0.0, maxL + xmargin, yc - BASE_W / 2.0, yc + BASE_W / 2.0, 0.0, BASE_H))
    comb = trimesh.boolean.union(parts, engine="manifold")
    comb.merge_vertices()
    b = comb.bounds
    comb.apply_translation([-b[0][0], -b[0][1], -b[0][2]])
    return comb, infos


ROW_GAP = 6.0                  # 横並びの管どうしのy隙間（窓が呼吸できるだけ空ける）


def build_row(lengths, base=True, gap=ROW_GAP, xmargin=4.0):
    """全管を『立てたまま(z=7・窓+y横向き)』y方向へ横並びにし、底ベースの上に乗せて一体化する。
    z積みと違い全管が同じ低い高さ(約9mm)なので造形品質が均一で、短い高音管も塔頂部の
    乱れを受けない。窓横向きは自己ブリッジでサポート不要。底ベースで定着（過去に横並び独立
    版がH2Dで剥離した弱点を、底ベース＋一体化で解消）。管はベース厚ぶん持ち上げて窓を塞がない。
    返り値: (mesh, infos)。lengths の順に -y から +y へ並べ、吸込口x=0そろえ。"""
    lengths = list(lengths)
    tubes = []
    infos = []
    z0 = BASE_H - OVERLAP if base else 0.0    # 管をベースの上に乗せる
    y = 0.0
    for L in lengths:
        t = flute(L)
        t.apply_translation([0, y, z0])
        tubes.append(t)
        infos.append(dict(L=L, y=round(y, 1), predHz=round(predf(L))))
        y += TUBE_W + gap
    parts = list(tubes)
    if base:
        maxL = max(lengths)
        y_hi = (len(lengths) - 1) * (TUBE_W + gap) + TUBE_W
        parts.append(_box(0.0, maxL + xmargin, -gap / 2.0, y_hi + gap / 2.0, 0.0, BASE_H))
    comb = trimesh.boolean.union(parts, engine="manifold")
    comb.merge_vertices()
    b = comb.bounds
    comb.apply_translation([-b[0][0], -b[0][1], -b[0][2]])
    return comb, infos


def place_on_bed(mesh, bed=(350.0, 160.0)):
    c = (mesh.bounds[0] + mesh.bounds[1]) / 2
    mesh.apply_translation([bed[0] / 2 - c[0], bed[1] / 2 - c[1], 0])
    return mesh


def emit(name, lengths, base=True):
    comb, infos = build_zstack(lengths, base=base)
    place_on_bed(comb)
    path = os.path.join(OUT, name)
    comb.export(path)
    print("%s  ext=%s wt=%s 本数=%d" % (
        os.path.basename(path), np.round(comb.extents, 1).tolist(),
        comb.is_watertight, len(lengths)))
    for i in infos:
        print("   L=%3dmm z0=%5.1f 予測%5dHz" % (i["L"], i["z0"], i["predHz"]))
    return path, infos


if __name__ == "__main__":
    # 較正コーム（印刷済みと同じ 40/48/56/64/72 を再現）
    emit("comb_rect_calib5_zstack_base_rebuilt.stl", [40, 48, 56, 64, 72], base=True)
    # 限界コーム（高音側28/32/36で上限、低音側60/68で死の境界=64△/72×の間を挟む）
    emit("comb_rect_limit5_zstack_base.stl", [28, 32, 36, 60, 68], base=True)
