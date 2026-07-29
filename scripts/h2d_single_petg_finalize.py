"""H2Dで単色PETGを右ノズル（AMS側＝ノズル群2）から刷るための、スライス後の仕上げ。

なぜ要るか
----------
H2Dは2ノズル機で、この機体では左ノズルが外部スプール（導電性の黒PLAで固定）、
右ノズルがAMS供給である。プロセスプロファイルは3本のフィラメントを持ったまま
スライスするので、出来上がった3mfは「使わない2本」を抱えている。そのまま
print_3mf へ送ると、AMSの割り当てが [2, -1, -1] のように欠けて、受理直後に
FAILED になる。

そこで、gcodeには一切触れずに metadata だけを次のように整える。

  * project_settings … フィラメント関係の配列を実際に使う1本へ切り詰め、
    filament_map を群2にし、printer_model_id を O1D にする。
  * model_settings  … filament_map_mode を Manual にし、filament_maps を群2にする。
  * slice_info      … filament_maps を群2、ノズルを id=1・extruder_id=2、
    printer_model_id を O1D にする。

再スライスはしない。スライスし直すと、笛のボアのような内向きの殻が
「空洞ではなく中実」と解釈されて、材料が倍近くに膨らむことがある
（2026-07-29、スプールの1枚目で実際に 101g が 195.7g になった）。

使い方:
    python3 scripts/h2d_single_petg_finalize.py \
        --in temp/xxx_sliced.3mf --out out/xxx_petg_h2d.gcode.3mf
"""
from __future__ import annotations

import argparse
import json
import os
import re
import zipfile

NOZZLE_GROUP = "2"          # AMSが繋がるノズル群（右ノズル）
PRINTER_MODEL_ID = "O1D"    # H2D


def trim_filament_arrays(ps: dict, keep: int = 1) -> dict:
    """フィラメント N 本ぶんの配列を、実際に使う keep 本へ切り詰める。

    H2Dは2ノズル機なので、フラッシュ量は 2×N（ベクトル）や 2×N×N（マトリクス）と、
    ノズル2つぶんが連結された形で入っている。長さで見分けて、それぞれ先頭を取る。
    """
    n = len(ps["filament_type"])
    if keep >= n:
        return ps

    def sub(block):
        return [block[i * n + j] for i in range(keep) for j in range(keep)]

    for key, v in list(ps.items()):
        if not isinstance(v, list):
            continue
        length = len(v)
        if length == 2 * n * n:
            ps[key] = sub(v[:n * n]) + sub(v[n * n:])
        elif length == n * n:
            ps[key] = sub(v)
        elif length == 2 * n:
            ps[key] = v[:keep] + v[n:n + keep]
        elif length == n:
            ps[key] = v[:keep]
    return ps


def finalize(src: str, dst: str, group: str = NOZZLE_GROUP,
             model_id: str = PRINTER_MODEL_ID) -> dict:
    zin = zipfile.ZipFile(src)
    items = zin.infolist()
    data = {i.filename: zin.read(i.filename) for i in items}

    ps = json.loads(data["Metadata/project_settings.config"])
    n_before = len(ps["filament_type"])
    ps = trim_filament_arrays(ps, 1)
    ps["filament_map"] = [group]
    ps["printer_model_id"] = model_id
    data["Metadata/project_settings.config"] = json.dumps(ps, ensure_ascii=False).encode()

    ms = data["Metadata/model_settings.config"].decode()
    ms = re.sub(r'key="filament_map_mode" value="[^"]*"',
                'key="filament_map_mode" value="Manual"', ms)
    maps = " ".join([group] * n_before)
    if 'key="filament_maps"' in ms:
        ms = re.sub(r'key="filament_maps" value="[^"]*"',
                    'key="filament_maps" value="%s"' % maps, ms)
    else:
        ms = ms.replace('key="filament_map_mode" value="Manual"/>',
                        'key="filament_map_mode" value="Manual"/>\n'
                        '    <metadata key="filament_maps" value="%s"/>' % maps, 1)
    data["Metadata/model_settings.config"] = ms.encode()

    si = data["Metadata/slice_info.config"].decode()
    si = si.replace('printer_model_id" value=""', 'printer_model_id" value="%s"' % model_id)
    si = re.sub(r'key="filament_maps" value="[^"]*"',
                'key="filament_maps" value="%s"' % maps, si)
    si = re.sub(r'key="limit_filament_maps" value="[^"]*"',
                'key="limit_filament_maps" value="0"', si)
    si = re.sub(r'<nozzle id="\d+" extruder_id="\d+"',
                '<nozzle id="1" extruder_id="%s"' % group, si)
    data["Metadata/slice_info.config"] = si.encode()

    os.makedirs(os.path.dirname(os.path.abspath(dst)), exist_ok=True)
    if os.path.exists(dst):
        os.remove(dst)
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zo:
        for i in items:
            zi = zipfile.ZipInfo(i.filename, date_time=i.date_time)
            zi.compress_type = i.compress_type
            zi.external_attr = i.external_attr
            zo.writestr(zi, data[i.filename])

    gcode = data["Metadata/plate_1.gcode"].decode("latin1")
    def grab(pat, default="?"):
        m = re.search(pat, gcode)
        return m.group(1) if m else default
    return {
        "解凍MB": round(len(data["Metadata/plate_1.gcode"]) / 1e6, 2),
        "層厚": grab(r"; layer_height = (\S+)"),
        "層数": grab(r"total layer number: (\d+)"),
        "重さg": grab(r"total filament weight \[g\] : ([\d.]+)"),
        "時間": grab(r"model printing time: ([^;]+)"),
        "フィラメント本数": "%d -> 1" % n_before,
        "ノズル群": group,
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description="H2D単色PETG（右ノズル）用の仕上げ")
    ap.add_argument("--in", dest="src", required=True, help="スライス済み3mf")
    ap.add_argument("--out", dest="dst", required=True, help="出力する gcode.3mf")
    ap.add_argument("--group", default=NOZZLE_GROUP, help='AMS側のノズル群（既定 "2"）')
    args = ap.parse_args(argv)
    info = finalize(args.src, args.dst, args.group)
    print("書き出し %s" % args.dst)
    for k, v in info.items():
        print("  %s: %s" % (k, v))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
