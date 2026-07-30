"""スライス済み3mfに「高さ範囲ごとの層厚」を入れて刷り直し、印刷時間を縮める。

なぜ要るか
----------
笛は 0.08mm で刷らないと窓の天井が垂れて鳴らない。しかし笛が入っているのは物のごく一部
（本立てv3なら底板の 0〜5mm）だけである。そこから上を 0.08mm で刷るのは無駄が大きい。
[* 笛のある高さだけ 0.08mm、それより上は粗く]すれば、造形の質を落とさずに時間が縮む。

仕組み
------
BambuStudio は 3mf の `Metadata/layer_config_ranges.xml` を読む（PrusaSlicer と同じ書式）。

    <objects><object id="1">
      <range min_z="0" max_z="5"><option opt_key="layer_height">0.08</option></range>
      <range min_z="5" max_z="200"><option opt_key="layer_height">0.24</option></range>
    </object></objects>

[* object の id は 1 から始まる通し番号]である（3mf の中の object id ではない）。ここを
間違えると黙って無視される（2026-07-30、実験で確かめた）。

なお `Metadata/layer_heights_profile.txt`（可変層厚のプロファイル）は[* CLIでは効かない]。
同じ実験で層数が変わらないことを確認した。

使い方:
    python3 scripts/set_layer_ranges.py --in temp/x_sliced.3mf --out out/x.gcode.3mf \\
        --fine-until 5 --fine 0.08 --coarse 0.24
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import tempfile
import zipfile

BS = "/Applications/BambuStudio.app/Contents/MacOS/BambuStudio"


def ranges_xml(fine_until, fine, coarse, top, object_id=1, coarse_infill=None, coarse_walls=None):
    """粗い側には層厚のほかに、インフィル密度と壁の数も指定できる。

    速度（outer_wall_speed など）は範囲では効かないことを実験で確かめた（2026-07-30）。
    速さを変えたいときは、笛と本体を別パーツにしてパーツごとの設定で行う。
    """
    extra = ""
    if coarse_infill:
        extra += '   <option opt_key="sparse_infill_density">%s</option>\n' % coarse_infill
    if coarse_walls:
        extra += '   <option opt_key="wall_loops">%d</option>\n' % coarse_walls
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n<objects>\n <object id="%d">\n'
        '  <range min_z="0" max_z="%.4f">\n'
        '   <option opt_key="layer_height">%.3f</option>\n  </range>\n'
        '  <range min_z="%.4f" max_z="%.4f">\n'
        '   <option opt_key="layer_height">%.3f</option>\n%s  </range>\n'
        ' </object>\n</objects>\n'
        % (object_id, fine_until, fine, fine_until, top, coarse, extra))


def gcode_info(path):
    with zipfile.ZipFile(path) as z:
        g = z.read("Metadata/plate_1.gcode").decode("latin1")
    def grab(pat, default="?"):
        m = re.search(pat, g)
        return m.group(1) if m else default
    return dict(layers=grab(r"total layer number: (\d+)"),
                time=grab(r"model printing time: ([^;]+)"),
                grams=grab(r"total filament weight \[g\] : ([\d.]+)"))


def main(argv=None):
    ap = argparse.ArgumentParser(description="高さ範囲ごとの層厚を入れて刷り直す")
    ap.add_argument("--in", dest="src", required=True, help="スライス済み3mf")
    ap.add_argument("--out", dest="dst", required=True, help="出力する3mf")
    ap.add_argument("--fine-until", type=float, required=True, help="この高さまで細かく刷る[mm]")
    ap.add_argument("--fine", type=float, default=0.08, help="細かい側の層厚[mm]")
    ap.add_argument("--coarse", type=float, default=0.24, help="粗い側の層厚[mm]")
    ap.add_argument("--top", type=float, default=400.0, help="範囲の上端[mm]")
    ap.add_argument("--coarse-infill", default=None, help='粗い側のインフィル密度（例 8%%）')
    ap.add_argument("--coarse-walls", type=int, default=None, help="粗い側の壁の数（既定はそのまま）")
    ap.add_argument("--object-id", type=int, default=1, help="通し番号（既定1）")
    ap.add_argument("--bambu-studio", default=os.environ.get("BAMBU_STUDIO", BS))
    args = ap.parse_args(argv)

    before = gcode_info(args.src)
    tmp = tempfile.mkdtemp()
    try:
        staged = os.path.join(tmp, "with_ranges.3mf")
        shutil.copy(args.src, staged)
        with zipfile.ZipFile(staged, "a", zipfile.ZIP_DEFLATED) as z:
            z.writestr("Metadata/layer_config_ranges.xml",
                       ranges_xml(args.fine_until, args.fine, args.coarse, args.top,
                                  args.object_id, args.coarse_infill, args.coarse_walls))
        outdir = os.path.dirname(os.path.abspath(args.dst)) or "."
        os.makedirs(outdir, exist_ok=True)
        r = subprocess.run([args.bambu_studio, "--slice", "0", "--outputdir", outdir,
                            "--export-3mf", os.path.basename(args.dst),
                            "--allow-newer-file", staged],
                           capture_output=True, text=True)
        if not os.path.exists(args.dst):
            bad = [l for l in (r.stdout + r.stderr).splitlines()
                   if "error" in l.lower() and "Invalid T command" not in l]
            print("\n".join(bad[-8:]) or (r.stdout + r.stderr)[-600:])
            raise SystemExit("スライスに失敗した")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    after = gcode_info(args.dst)
    print("書き出し %s" % args.dst)
    print("  前: %s層 / %s / %s g" % (before["layers"], before["time"], before["grams"]))
    print("  後: %s層 / %s / %s g （0〜%.1fmm は %.2fmm、その上は %.2fmm）"
          % (after["layers"], after["time"], after["grams"],
             args.fine_until, args.fine, args.coarse))
    if after["layers"] == before["layers"]:
        print("  ★層数が変わっていない。範囲指定が無視された可能性がある（--object-id を確かめる）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
