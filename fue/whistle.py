"""薄い平型ホイッスル（緊急警報用ネイティブ フィッポル）。

サブプロジェクト③「日常品に笛を仕込む」＝TPUスマホケース一体の非常警報笛に向けた、
実績ミニヘッドを潰すのではなく最初から薄く設計するフィッポル。緊急ホイッスルと同じく
幅広×薄で、薄い噴流を最初から作る（潰さない）。

座標: x=幅（広・ケース面内）, y=厚み（薄T・ケース垂直）, z=長さ（=共鳴, 上端=吹込）。
印刷は立てて(z上): 縦ボア・縦windwayが自己ブリッジ、窓は45°ひさし(box._window_void)で自立。
使用時は寝かせ（y=厚みTがケースからの出っ張り）。

薄型化の要点: ボアを「平たいスロット（幅bore_x × 薄bore_y）」にして、-y側に外部windwayを
置く隙間を確保する（丸Ø9.5だと厚み13mm超が要り薄くできない）。TPU前提で壁は厚め(1.2mm)。

未検証の新設計＝実機ボイシング（鳴る flue/cutup/offset の組合せ探し）が要る。
"""
import os
import sys
import numpy as np
import trimesh

sys.path.insert(0, os.path.dirname(__file__))
import box  # _window_void（45°ひさし窓）, _extrude_yz

OUT = os.path.join(os.path.dirname(__file__), os.pardir, "out")
C4 = 343000.0 / 4.0     # 閉管 c/4（mm/s /4）


def flat_whistle(L=26.0, W=20.0, T=8.0, wall=1.2, bore_y=2.5,
                 flue=0.8, wall_wf=1.0, cutup=4.0, winway=9.0,
                 win_inset=1.2, cap=1.5, win_frac=0.85, T_body=None):
    """薄い平型ホイッスル1本。
      L        閉ボア長（閉端→窓下端, z）。音程を決める（閉管 f≈C4/(L+端補正)）。
      W,T      外形の幅(x)・厚み(y)。Tはケースからのはみだしなのでできるだけ小さく。
      wall     外壁厚（TPU前提で1.2mm）。
      bore_y   ボア（平スロット）の厚み(y)。薄いほど外部windwayの隙間ができる。
      flue     windway（噴流の通路）の厚み(y)＝ジェット厚。
      wall_wf  ボア-y壁とwindwayの間の壁厚＝flue–labiumオフセットを決める。
      cutup    窓のz長（噴流が窓を渡る距離）。
      winway   windwayのz長（吹込口までの高さ）。
      win_inset窓が-y面からボア内へ入り込む深さ。
      win_frac 窓・windwayのx幅 = bore_x*win_frac（端に壁を残す）。
    """
    bore_x = W - 2 * wall
    ry = bore_y / 2.0                       # ボア-y壁 = -ry
    H = cap + L + cutup + winway
    half_x = bore_x * win_frac / 2.0
    if T_body is None:
        T_body = T                          # None=一様厚
    zc = cap + L                            # 胴↔頭の境界（窓の下端）

    # 外形＝段付き厚み：頭部(z>=zc, 厚T・windwayが要る) ＋ 胴体(z<zc, 薄T_body・ボア+壁のみ)。
    # 段差は45°チャンファ(高さchf=(T-T_body)/2)でテーパさせ、立て置き印刷で自己支持させる。
    chf = max((T - T_body) / 2.0, 0.0)
    head = trimesh.creation.box(extents=[W, T, H - zc]); head.apply_translation([0, 0, (zc + H) / 2.0])
    body = trimesh.creation.box(extents=[W, T_body, zc - chf]); body.apply_translation([0, 0, (zc - chf) / 2.0])
    parts = [head, body]
    if chf > 1e-6:
        lo = [[sx * W / 2.0, sy * T_body / 2.0, zc - chf] for sx in (-1, 1) for sy in (-1, 1)]
        hi = [[sx * W / 2.0, sy * T / 2.0, zc] for sx in (-1, 1) for sy in (-1, 1)]
        parts.append(trimesh.PointCloud(np.array(lo + hi, float)).convex_hull)
    col = trimesh.boolean.union(parts, engine="manifold")
    # ボア（閉スロット）: z=cap .. cap+L+cutup、閉端はcap厚で塞ぐ
    bz0, bz1 = cap, cap + L + cutup
    bore = trimesh.creation.box(extents=[bore_x, bore_y, bz1 - bz0])
    bore.apply_translation([0, 0, (bz0 + bz1) / 2.0])
    # 窓（-y面→ボア内, z=[cap+L, cap+L+cutup], 45°ひさしで自立）
    wz0, wz1 = cap + L, cap + L + cutup
    win = box._window_void(0.0, y_face=-T / 2.0 - 0.1, y_inner=-ry + win_inset,
                           z0=wz0, z1=wz1, half_x=half_x)
    # windway（-y側, ボア壁の外にwall_wf残し、flue厚の縦チャンネルを天面まで）
    ywi = -ry - wall_wf
    ywo = ywi - flue
    ww = trimesh.creation.box(extents=[2 * half_x, flue, winway + 0.1])
    ww.apply_translation([0, (ywi + ywo) / 2.0, H - winway / 2.0 + 0.05])
    voids = trimesh.util.concatenate([bore, win, ww])
    whistle = trimesh.boolean.difference([col, voids], engine="manifold")

    # windwayが外壁を突き破っていないか（ywo > -T/2 が必須）
    ok_flue = ywo > (-T / 2.0 + 0.1)
    offset = wall_wf + flue / 2.0
    info = dict(W=W, T=T, T_body=T_body, L=L, bore=(round(bore_x, 1), round(bore_y, 1)), cutup=cutup,
                flue=flue, offset=round(offset, 2), H=round(H, 1),
                flue_wall_ok=bool(ok_flue), back_wall=round(-T / 2.0 - ywo, 2),
                freq=C4 / (L + 8.0), watertight=bool(whistle.is_watertight),
                dims=tuple(np.round(whistle.extents, 1)))
    return whistle, info


def voicing_comb(L=26.0, T=8.0, T_body=5.0, gap=6.0, variants=None):
    """『鳴るか』を見るボイシング変奏コーム。管長L・頭厚T・胴厚T_body固定で、flue–labium
    オフセット(wall_wf) と cutup を振った数本を横一列に。1回刷って鳴る組合せを選ぶ。"""
    if variants is None:
        variants = [
            ("o0.6c3.5", dict(wall_wf=0.6, cutup=3.5)),
            ("o1.0c4",   dict(wall_wf=1.0, cutup=4.0)),
            ("o1.0c5",   dict(wall_wf=1.0, cutup=5.0)),
            ("o1.5c4.5", dict(wall_wf=1.5, cutup=4.5)),
        ]
    flutes, infos = [], []
    xoff = 0.0
    for label, kw in variants:
        f, info = flat_whistle(L=L, T=T, T_body=T_body, **kw)
        w = f.extents[0]
        f.apply_translation([xoff + w / 2.0, 0, 0])
        info["label"] = label; info["x"] = xoff
        xoff += w + gap
        flutes.append(f); infos.append(info)
    mesh = trimesh.util.concatenate(flutes)
    bb = mesh.bounds
    mesh.apply_translation([-(bb[0][0] + bb[1][0]) / 2.0, -(bb[0][1] + bb[1][1]) / 2.0, 0])
    return mesh, infos


def main():
    import argparse
    ap = argparse.ArgumentParser(description="薄い平型ホイッスル（緊急警報用フィッポル）")
    ap.add_argument("--voicing", action="store_true", help="ボイシング変奏コーム（鳴る組合せ探し）")
    ap.add_argument("--single", action="store_true", help="単体1本")
    ap.add_argument("--L", type=float, default=26.0)
    ap.add_argument("--T", type=float, default=8.0, help="頭部(フィッポル)の厚み")
    ap.add_argument("--T-body", type=float, default=5.0, dest="T_body", help="胴体(共鳴)の厚み＝実効的な薄さ")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    if a.voicing:
        mesh, infos = voicing_comb(L=a.L, T=a.T, T_body=a.T_body)
        name = a.out or os.path.join(OUT, "whistle_voicing_L%.0f_T%.0f_b%.0f.stl" % (a.L, a.T, a.T_body))
        mesh.export(name)
        print("平型ホイッスル ボイシングコーム（L=%.0f・厚みT=%.0f・立て置き印刷）:" % (a.L, a.T))
        for i in infos:
            print("  %-9s 外形%s ボア%s flue壁OK=%s 背壁%.2f wt=%s 予測%.0fHz"
                  % (i["label"], i["dims"], i["bore"], i["flue_wall_ok"], i["back_wall"],
                     i["watertight"], i["freq"]))
        print("外形", np.round(mesh.extents, 1), "->", name)
    else:
        f, info = flat_whistle(L=a.L, T=a.T, T_body=a.T_body)
        name = a.out or os.path.join(OUT, "whistle_L%.0f_T%.0f_b%.0f.stl" % (a.L, a.T, a.T_body))
        f.export(name)
        print("平型ホイッスル L=%.0f T=%.0f: 外形%s ボア%s flue壁OK=%s watertight=%s 予測%.0fHz -> %s"
              % (a.L, a.T, info["dims"], info["bore"], info["flue_wall_ok"], info["watertight"],
                 info["freq"], name))


if __name__ == "__main__":
    main()
