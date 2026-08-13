#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""かるた札の3色版（黒い字・白い地・緑のふち）をH2Dの左右2ノズル用にスライスする。

なぜ専用の包みが要るか
----------------------
image_printing/dual_slice.py は「フィラメント1を右ノズル、2を左ノズル、残りは全部左」に
割り当てる（maps = "2 1 1 …"）。2色ならこれでよいが、3色目の緑は白と同じ右ノズルの
AMSから出したいので、そのままだと緑まで左ノズル（外部スプールの黒）へ行ってしまう。

ここでは maps を "2 1 2" にする。
    フィラメント1 = 白い地  → 右ノズル（AMS スロット0）
    フィラメント2 = 黒い字  → 左ノズル（外部スプール）
    フィラメント3 = 緑のふち → 右ノズル（AMS スロット3）

使い方
    TMPDIR=<作業用> .venv/bin/python karuta3_slice.py --source <3mf> --out <gcode.3mf>
"""
import os
import re
import sys

IMG = ("/Users/kurihara/Library/CloudStorage/GoogleDrive-qurihara@gmail.com/"
       "マイドライブ/share/google_desktop_share/3D_Print/image_printing")
RECIPE = ("/Users/kurihara/Library/CloudStorage/GoogleDrive-qurihara@gmail.com/"
          "マイドライブ/share/google_desktop_share/3D_Print/swap/h2d-slice-recipe")
sys.path.insert(0, IMG)
sys.path.insert(0, RECIPE)

import h2d_dual_slice as D                                        # noqa: E402

# カードで効かせたい設定を元のプロジェクトから引き継ぐ（dual_slice.py と同じ）
D.CARRY_FROM_SOURCE = list(D.CARRY_FROM_SOURCE) + [
    "brim_type", "brim_width", "brim_object_gap",
    "detect_thin_wall", "wall_loops",
]


def _maps_3color(model_path, n_filaments: int):
    """1→右、2→左、3以降→右。★3色目を右ノズルへ送るのがこの関数の要点である★"""
    maps = " ".join(["2", "1"] + ["2"] * max(0, n_filaments - 2))
    s = model_path.read_text()
    s = re.sub(r'key="filament_map_mode" value="[^"]*"',
               'key="filament_map_mode" value="Manual"', s)
    if "filament_maps" in s:
        s = re.sub(r'key="filament_maps" value="[^"]*"',
                   f'key="filament_maps" value="{maps}"', s)
    else:
        s = s.replace('key="filament_map_mode" value="Manual"/>',
                      f'key="filament_map_mode" value="Manual"/>\n'
                      f'    <metadata key="filament_maps" value="{maps}"/>')
    model_path.write_text(s)
    return maps


D.set_model_filament_maps = _maps_3color

_orig_build = D.build_project_settings


def _build_3color(seed_ps, source_ps, keep_quality):
    """★3本目のフィラメントも元のプロジェクトから引き継ぐ★

    元の関数は per-filament の配列について v[0] と v[1] しか写さない。したがって
    3本目は種(seed)の値のまま残り、種は PETG（GFG01・半透明グレー）なので、
    緑のPLAを入れたつもりが PETG の設定で刷られてしまう（実際にそうなった）。
    ノズル温度もベッド温度も違うので、気づかずに刷ると失敗する。
    """
    d = _orig_build(seed_ps, source_ps, keep_quality)
    n_seed = len(d["filament_type"])
    n_src = len(source_ps["filament_type"])
    for k, v in list(d.items()):
        if (isinstance(v, list) and len(v) == n_seed
                and k in source_ps and isinstance(source_ps[k], list)
                and len(source_ps[k]) == n_src):
            for i in range(2, min(n_seed, n_src)):
                v[i] = source_ps[k][i]
    return d


D.build_project_settings = _build_3color

if __name__ == "__main__":
    argv = sys.argv[1:]
    if "--seed" not in argv:
        argv += ["--seed", os.path.join(RECIPE, "nozzle_seed_rnz.3mf")]
    if "--keep-quality" not in argv:
        argv += ["--keep-quality"]
    sys.exit(D.main(argv))
