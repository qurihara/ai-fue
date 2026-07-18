#!/bin/bash
# H2Dヘッドレス・スライス（複数STLを1プレートに自動配置・左右ノズル対応）
# Usage: h2d_slice_multi.sh <output_sliced.3mf> [left|right] <seed.3mf> <stl1> <stl2> ...
#   seed は線幅0.5/0.08mm/ブリムなし等を焼き込んだ右ノズルGUIスライス3mf（rnz_careful.3mf）。
#   project_settings は seed のものを丸ごと採用する（層高・線幅・ブリム・温度はseed依存）。
set -e
OUT="$1"; NOZ="${2:-right}"; SEED="$3"; shift 3
STLS=("$@")
BS="/Applications/BambuStudio.app/Contents/MacOS/BambuStudio"
PROFD="/Applications/BambuStudio.app/Contents/Resources/profiles/BBL"
MACH="$PROFD/machine/Bambu Lab H2D 0.4 nozzle.json"
PROC="$PROFD/process/0.20mm Standard @BBL H2D.json"
FIL="$PROFD/filament/Bambu PLA Basic @BBL H2D.json"
[ "$NOZ" = "right" ] && FIDX=2 || FIDX=1
TMP=$(mktemp -d)
echo "配置するSTL: ${#STLS[@]}個  ノズル=$NOZ  seed=$(basename "$SEED")"
# 1) 12個を新規H2Dプロジェクトに読み込んで自動配置
"$BS" --arrange 1 --outputdir "$TMP" --export-3mf p.3mf \
  --load-settings "$MACH;$PROC" --allow-newer-file --ensure-on-bed \
  --load-filaments "$FIL" --load-defaultfila "${STLS[@]}" 2>&1 | tail -3
# 2) seed の project_settings を採用＋各オブジェクトの filament index / plate の filament_maps を設定
mkdir -p "$TMP/e"; unzip -o -q "$TMP/p.3mf" -d "$TMP/e"
mkdir -p "$TMP/s"; unzip -o -q "$SEED" -d "$TMP/s"
cp "$TMP/s/Metadata/project_settings.config" "$TMP/e/Metadata/project_settings.config"
FMAPS=$(grep -oE 'key="filament_maps" value="[^"]*"' "$TMP/s/Metadata/model_settings.config" | head -1 | sed -E 's/.*value="([^"]*)".*/\1/')
[ -z "$FMAPS" ] && FMAPS="1 2 1"
python3 - "$TMP/e/Metadata/model_settings.config" "$FIDX" "$FMAPS" << 'PY'
import sys,re
p,fidx,fmaps=sys.argv[1],sys.argv[2],sys.argv[3]; s=open(p).read()
# 全オブジェクトの extruder を右ノズル(fidx)へ
s=re.sub(r'(<metadata key="extruder" value=")\d+("/>)', rf'\g<1>{fidx}\g<2>', s)
if 'filament_map_mode' not in s:
    s=s.replace('</plate>','    <metadata key="filament_map_mode" value="Auto For Flush"/>\n</plate>',1)
if 'filament_maps' in s:
    s=re.sub(r'key="filament_maps" value="[^"]*"', f'key="filament_maps" value="{fmaps}"', s)
else:
    s=s.replace('key="filament_map_mode" value="Auto For Flush"/>',
                f'key="filament_map_mode" value="Auto For Flush"/>\n    <metadata key="filament_maps" value="{fmaps}"/>')
open(p,'w').write(s)
PY
( cd "$TMP/e" && zip -q -X -r "$TMP/seeded.3mf" "[Content_Types].xml" _rels 3D Metadata )
# 3) スライス
"$BS" --slice 0 --outputdir "$(dirname "$OUT")" --export-3mf "$(basename "$OUT")" \
  --allow-newer-file "$TMP/seeded.3mf" 2>&1 | tail -3
# 4) printer_model_id=O1D にパッチ（print_3mf 受理のため）
mkdir -p "$TMP/o"; unzip -o -q "$OUT" -d "$TMP/o"
if [ -f "$TMP/o/Metadata/project_settings.config" ]; then
  python3 - "$TMP/o/Metadata/project_settings.config" << 'PY'
import sys,re
p=sys.argv[1]; s=open(p).read()
s=re.sub(r'("printer_model_id"\s*:\s*)"[^"]*"', r'\1"O1D"', s)
open(p,'w').write(s)
PY
  ( cd "$TMP/o" && zip -q -X -r "$TMP/patched.3mf" "[Content_Types].xml" _rels 3D Metadata ) && cp "$TMP/patched.3mf" "$OUT"
fi
# 5) 時間・グラム抽出
GC=$(unzip -p "$OUT" Metadata/plate_1.gcode 2>/dev/null)
echo "===== 結果 ====="
echo "$GC" | grep -m1 -iE "model printing time|total estimated time" || true
echo "$GC" | grep -m1 -iE "total filament used \[g\]|filament used \[g\]|filament used \[mm\]|filament used \[cm3\]" || true
echo "$GC" | grep -iE "^; filament used" | head -5 || true
unzip -p "$OUT" Metadata/slice_info.config 2>/dev/null | grep -oE 'used_(g|m)="[0-9.]*"' | head -6 || true
echo "gcode展開サイズ:"; unzip -l "$OUT" 2>/dev/null | grep plate_1.gcode
echo "OUT=$OUT"
rm -rf "$TMP"
