"""H2DのCLIスライス出力を、BambuStudioとファームが読める形に直す。

CLIが書く model_settings.config には、XMLとして壊れた属性が2種類ある。
  (1) 生のgcodeを抱えた属性（machine_start_gcode・change_filament_gcode など）。
      中に " や < がそのまま入る。正本は project_settings.config にあり、
      gcode 本体は plate_1.gcode に展開済みなので、[* 行ごと落としてよい]。
  (2) 入れ子の引用符（H2Dの extruder_variant_list は "A";"B" のように2組以上ある）。
      値を正しく逃がして書き直す。
あわせて slice_info.config の printer_model_id を O1D に補填する（空だとファームが照合できない）。
"""
import sys, zipfile, re
src, dst = sys.argv[1], sys.argv[2]
zin = zipfile.ZipFile(src); items = zin.infolist()
data = {i.filename: zin.read(i.filename) for i in items}

si = data['Metadata/slice_info.config'].decode('utf-8')
si2 = si.replace('printer_model_id" value=""', 'printer_model_id" value="O1D"')
print("printer_model_id を O1D に補填" if si2 != si else "printer_model_id は既に入っている")
data['Metadata/slice_info.config'] = si2.encode('utf-8')

mkey = 'Metadata/model_settings.config'
ms = data[mkey].decode('utf-8')
ms, n_drop = re.subn(r'[ \t]*<metadata key="[^"]*gcode"[^\n]*\n?', '', ms)
print("生gcodeを抱えた属性を %d 行落とした" % n_drop)

def esc(v):
    v = re.sub(r'&(?!(amp|lt|gt|quot|apos);)', '&amp;', v)
    return v.replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
ms, n_esc = re.subn(r'<metadata key="([^"]+)" value="(.*)"\s*/>',
                    lambda m: '<metadata key="%s" value="%s"/>' % (m.group(1), esc(m.group(2))), ms)
print("metadata %d 行の値を逃がした" % n_esc)
data[mkey] = ms.encode('utf-8')

with zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED) as zo:
    for i in items:
        zi = zipfile.ZipInfo(i.filename, date_time=i.date_time)
        zi.compress_type = i.compress_type; zi.external_attr = i.external_attr
        zo.writestr(zi, data[i.filename])
print("wrote", dst)
