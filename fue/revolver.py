"""リボルバー笛（目標②）: 回して吹くとメロディになるガトリング砲式の笛。

考え方（オルガンの風箱＋回転セレクタ）:
- ロータ（回転盤）: コンパクト笛を円環に並べる。全笛は外形・全長を共通にして、
  歌口(mouth)を同じ高さに揃える。内部の閉端位置だけ音ごとに変える。中央に回転軸の柱。
- ステータ（固定フタ）: 歌口の環の上に被せる円盤。吹き込み口(port)が1つだけ開いていて、
  そこへ息を吹き込む筒が付く。中央はロータの柱に嵌まって同心を保つ。
- 使い方: フタに息を入れつつロータを回すと、portの真下に来た笛だけに送風されて鳴る。
  回すたびに次の音へ。円環の並び順がそのままメロディの順になる。

2部品（rotor / stator）を別々に印刷して、中央軸で組む。face seal は多少漏れても、
port直下の笛が最も送風されるので鳴る（v1）。段階割り出し(ジェノバ/デテント)は後日。

trimesh+manifold3d（コントローラ .venv）で作る。ヘッドは非watertightなので結合せず重ねる。
"""
import numpy as np
import trimesh

OUTER_D = 14.07
BORE_D = 9.5
HEAD_CUT_Z = 143.0
HEAD_TOP_Z = 169.48
HEAD_LEN = HEAD_TOP_Z - HEAD_CUT_Z   # 26.48
CALIB_K = 91891.5
CALIB_DELTA = 14.227


def note_freq(note):
    names = {"C":0,"C#":1,"D":2,"D#":3,"E":4,"F":5,"F#":6,"G":7,"G#":8,"A":9,"A#":10,"B":11}
    import re
    m = re.match(r"([A-G]#?)(-?\d)", note)
    midi = names[m.group(1)] + 12*(int(m.group(2))+1)
    return 440.0*2**((midi-69)/12)


def air_for_note(note):
    return CALIB_K/note_freq(note) - CALIB_DELTA


def pipe_at(cx, cy, T, air, r_o=OUTER_D/2, r_b=BORE_D/2):
    outer = trimesh.creation.cylinder(radius=r_o, height=T, sections=64); outer.apply_translation([cx, cy, T/2])
    bore = trimesh.creation.cylinder(radius=r_b, height=air+1, sections=48); bore.apply_translation([cx, cy, T-air/2+0.5])
    return trimesh.boolean.difference([outer, bore])


def place_head(head_stl, cx, cy, z_bottom):
    m = trimesh.load(head_stl); b = m.bounds
    hx, hy = (b[0][0]+b[1][0])/2, (b[0][1]+b[1][1])/2
    m.apply_translation([cx-hx, cy-hy, z_bottom-b[0][2]])
    return m


def build(head_stl, notes, gap=4.0, T=None, base_th=3.0, lid_th=3.0, clr=0.4, axle_d=8.0):
    N = len(notes)
    airs = [air_for_note(n) for n in notes]
    if T is None:
        T = max(airs) + 4.0
    outer = OUTER_D
    R = max((outer+gap)*N/(2*np.pi), outer+axle_d)     # 笛が重ならない半径
    Zm = T + HEAD_LEN                                   # 歌口の高さ
    Do = 2*R + outer + 6                                # 盤の直径

    # ---- ロータ ----
    bodies, heads = [], []
    ang = []
    for i, (note, air) in enumerate(zip(notes, airs)):
        a = 2*np.pi*i/N
        ang.append(a)
        cx, cy = R*np.cos(a), R*np.sin(a)
        bodies.append(pipe_at(cx, cy, T, air))
        heads.append(place_head(head_stl, cx, cy, 0.0))
    base = trimesh.creation.cylinder(radius=Do/2, height=base_th, sections=96); base.apply_translation([0,0,-base_th/2])
    post = trimesh.creation.cylinder(radius=axle_d/2-0.1, height=Zm+10, sections=48); post.apply_translation([0,0,(Zm+10)/2-base_th])
    grip = trimesh.creation.cylinder(radius=Do/2, height=base_th, sections=96); grip.apply_translation([0,0,-base_th*1.5])  # 掴み用の下鍔
    rotor = trimesh.boolean.union(bodies + [base, post])
    rotor = trimesh.util.concatenate([rotor] + heads)

    # ---- ステータ（固定フタ） ----
    lid = trimesh.creation.cylinder(radius=Do/2, height=lid_th, sections=96); lid.apply_translation([0,0,Zm+clr+lid_th/2])
    axle_hole = trimesh.creation.cylinder(radius=axle_d/2+0.3, height=lid_th+20, sections=48); axle_hole.apply_translation([0,0,Zm+clr+lid_th/2+5])
    port = trimesh.creation.cylinder(radius=BORE_D/2, height=lid_th+4, sections=48); port.apply_translation([R,0,Zm+clr+lid_th/2])
    lid = trimesh.boolean.difference([lid, axle_hole, port])
    # 吹き込み筒（portの上に立てる。斜めでなく上向きで簡潔に）
    inlet_o = trimesh.creation.cylinder(radius=BORE_D/2+2, height=16, sections=48); inlet_o.apply_translation([R,0,Zm+clr+lid_th+8])
    inlet_b = trimesh.creation.cylinder(radius=BORE_D/2, height=20, sections=48); inlet_b.apply_translation([R,0,Zm+clr+lid_th+8])
    inlet = trimesh.boolean.difference([inlet_o, inlet_b])
    stator = trimesh.boolean.union([lid, inlet])

    info = dict(N=N, R=round(R,1), Do=round(Do,1), Zm=round(Zm,1), T=round(T,1),
                notes=notes, airs=[round(a,1) for a in airs], freqs=[round(note_freq(n)) for n in notes])
    return rotor, stator, info


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--head", required=True)
    ap.add_argument("--notes", default="G6 A6 B6 C7 D7 E7")
    ap.add_argument("--rotor", required=True)
    ap.add_argument("--stator", required=True)
    a = ap.parse_args()
    notes = a.notes.split()
    rotor, stator, info = build(a.head, notes)
    rotor.export(a.rotor); stator.export(a.stator)
    print("リボルバー笛: %d音 %s" % (info["N"], " ".join(notes)))
    print("  ロータ外径Ø%.0f 歌口高さ%.0f 半径R%.0f" % (info["Do"], info["Zm"], info["R"]))
    print("  狙い周波数:", info["freqs"], "Hz")
    print("  rotor:", np.round(rotor.extents,1), " stator:", np.round(stator.extents,1))
    print("  saved", a.rotor, a.stator)
