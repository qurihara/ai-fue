"""プレナム（共通吹き込み室）＋複数笛の同時発音テスト（目標③の要）。

一息で複数の笛を同時に鳴らし、FFTで各ピークに切り分けられるかを確かめる最小プロトタイプ。
オルガンのウインドチェスト（風箱）と同じ原理で、箱に吹き込むと各笛の歌口が一斉に駆動される。

設計:
- 各笛は「外形・全長を同一」にし、内部の閉端の高さ（充填量）だけ変えて別々の音にする。
  こうすると全ての歌口を同じ高さに揃えられる。閉管なので実証済み（プローブでC6〜C8が鳴った）。
- 上に切妻（ゲーブル）屋根のプレナムを載せる。屋根は45°以下にしてサポート無しで自立させる。
  片側の妻面に吹き込み口の筒を付ける。

発音ヘッドは非watertightなので結合(boolean)せず、他の部品に重ねてスライサに union させる。
プレナムと笛胴は watertight なので trimesh+manifold3d の boolean で作る。
"""
import sys
import numpy as np
import trimesh

OUTER_D = 14.07
BORE_D = 9.5
HEAD_CUT_Z = 143.0
HEAD_TOP_Z = 169.48
HEAD_LEN = HEAD_TOP_Z - HEAD_CUT_Z   # 26.48


def pipe_body(x0, T, air_len, r_o=OUTER_D/2, r_b=BORE_D/2):
    """外径一定の胴。上から air_len ぶんが中空（気柱）、その下は中実（閉端）。z=0..T。"""
    outer = trimesh.creation.cylinder(radius=r_o, height=T, sections=64)
    outer.apply_translation([x0, 0, T/2])
    bore = trimesh.creation.cylinder(radius=r_b, height=air_len+1, sections=48)
    bore.apply_translation([x0, 0, T - air_len/2 + 0.5])   # 上端から air_len ぶんをくり抜く
    return trimesh.boolean.difference([outer, bore])


def place_head(head_stl, x0, z_bottom):
    m = trimesh.load(head_stl)
    b = m.bounds
    cx, cy = (b[0][0]+b[1][0])/2, (b[0][1]+b[1][1])/2
    m.apply_translation([x0 - cx, -cy, z_bottom - b[0][2]])   # 切断面(min z)を z_bottom へ
    return m


def _prism_x(x0, x1, yz):
    """(y,z)の凸多角形断面を x0..x1 で押し出した三角柱を頂点から直接作る。"""
    n = len(yz)
    V = [[x0, y, z] for (y, z) in yz] + [[x1, y, z] for (y, z) in yz]
    F = []
    for i in range(n):                       # 側面
        j = (i + 1) % n
        F += [[i, j, n + j], [i, n + j, n + i]]
    for i in range(1, n - 1):                # 妻面（凸なので扇状）
        F.append([0, i + 1, i])
        F.append([n, n + i, n + i + 1])
    m = trimesh.Trimesh(vertices=np.array(V, float), faces=np.array(F), process=True)
    m.fix_normals()
    return m


def gable_prism(x0w, x1w, y_half, z_base, z_wall, z_peak):
    """x方向に伸びる切妻（家型の五角形断面）。壁z_base..z_wall + 屋根z_wall..z_peak。"""
    yz = [(-y_half, z_base), (y_half, z_base), (y_half, z_wall), (0.0, z_peak), (-y_half, z_wall)]
    return _prism_x(x0w, x1w, yz)


def build(head_stl, airs, gap_x=18.0, T=None):
    """airs=[気柱長,...] のN本。外形・全長は共通（T+HEAD_LEN）。Tは省略時 max(airs)+4。"""
    N = len(airs)
    if T is None:
        T = max(airs) + 4.0
    xs = [(i - (N - 1) / 2.0) * gap_x for i in range(N)]
    bodies = []
    heads = []
    mouth_z = T + HEAD_LEN
    for x0, air in zip(xs, airs):
        bodies.append(pipe_body(x0, T, air))
        heads.append(place_head(head_stl, x0, T))
    body_union = trimesh.boolean.union(bodies)

    # プレナム（切妻）: 歌口(z=mouth_z)の上に載せる
    zb = mouth_z
    z_wall = zb + 5.0
    z_peak = zb + 15.0
    xw0, xw1 = xs[0] - 11, xs[-1] + 11
    yh = 9.0
    outer = gable_prism(xw0, xw1, yh, zb, z_wall, z_peak)
    inner = gable_prism(xw0+2, xw1-2, yh-2, zb+2, z_wall, z_peak-3)
    chamber = trimesh.boolean.difference([outer, inner])
    # 歌口へ通す穴（径11mm）を室の底(2mm)に開ける
    holes = []
    for x0 in xs:
        h = trimesh.creation.cylinder(radius=5.5, height=6, sections=48)
        h.apply_translation([x0, 0, zb])
        holes.append(h)
    # 吹き込み口の筒（+X妻面から）
    inlet = trimesh.creation.cylinder(radius=4.0, height=16, sections=48)
    inlet.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [0, 1, 0]))
    inlet.apply_translation([xw1 - 2, 0, z_wall + 1.0])
    chamber = trimesh.boolean.difference([chamber] + holes + [inlet])
    # 吹き込み筒の外側（中空）を足す
    inlet_out = trimesh.creation.cylinder(radius=5.5, height=10, sections=48)
    inlet_out.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [0, 1, 0]))
    inlet_out.apply_translation([xw1 + 3, 0, z_wall + 1.0])
    inlet_bore = trimesh.creation.cylinder(radius=4.0, height=12, sections=48)
    inlet_bore.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [0, 1, 0]))
    inlet_bore.apply_translation([xw1 + 3, 0, z_wall + 1.0])
    inlet_tube = trimesh.boolean.difference([inlet_out, inlet_bore])

    solids = trimesh.boolean.union([body_union, chamber, inlet_tube])
    return trimesh.util.concatenate([solids] + heads)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--head", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--air", default="54,27", help="2本の気柱長(mm)")
    a = ap.parse_args()
    airs = [float(x) for x in a.air.split(",")]
    mesh = build(a.head, airs)
    mesh.export(a.out)
    K, D = 91891.5, 14.227
    print("プレナム＋%d本: 外形%s mm" % (len(airs), np.round(mesh.extents, 1)))
    for air in airs:
        print("  気柱%.0fmm → 狙い %.0f Hz" % (air, K/(air+D)))
    print("  saved", a.out)
