"""STL を Bambu A1 mini で直接印刷できる 3mf へ変換する。

導電性ゲームコントローラの make_3mf.py と同じ考え方を使う。すなわち、Bambu Studio
で保存した動作実績のある A1 mini 設定一式を骨組み（templates/a1mini_skeleton.3mf）
として持ち、その中の形状とモデル設定だけを差し替える。印刷設定（project_settings）は
骨組みのものをそのまま使うので、標準プリセットへ勝手に戻る問題を避けられる。

笛は単一素材なので、コントローラの2部品（土台と配線）構成を単一オブジェクトへ簡略化した。
ベッド180×180の中央（90, 90）へ、x/yの中心を原点へ寄せた状態で配置する。
"""
from __future__ import annotations
import argparse
import os
import shutil
import tempfile
import zipfile

import numpy as np
from stl import mesh as npmesh

HERE = os.path.dirname(__file__)
TEMPLATES = os.path.join(HERE, os.pardir, "templates")

# プリンタごとの定義。skeleton は実績のある3mf（プラミング一式と印刷設定の出所）。
#   - a1mini: 骨組みはコントローラ用3mf（AMS複数フィラメント）なので、project で単一フィラメント設定へ差し替える。
#   - h2d: 骨組みは栗原さんの印刷実績のあるH2D 3mf。実績設定をそのまま使うので project の差し替えはしない
#          （フィラメントの最終割り当ては Bambu Studio 側で調整する前提）。
PRINTERS = {
    "a1mini": {"bed": (180.0, 180.0), "skeleton": "a1mini_skeleton.3mf",
               "project": "a1mini_project_settings.config", "suffix": "_a1mini"},
    "h2d": {"bed": (350.0, 320.0), "skeleton": "h2d_skeleton.3mf",
            "project": None, "suffix": "_h2d"},
}


def _dedupe(tris: np.ndarray):
    """(N,3,3) の三角形群を (頂点配列, 面インデックス) へ。位置で重複頂点をまとめる。"""
    flat = tris.reshape(-1, 3)
    key = np.round(flat * 1000).astype(np.int64)  # 1um で量子化して同一視
    _, first_idx, inv = np.unique(key, axis=0, return_index=True, return_inverse=True)
    verts = flat[first_idx]
    faces = inv.reshape(-1, 3)
    return verts, faces


def _object_model(verts, faces) -> str:
    vs = "".join('     <vertex x="%g" y="%g" z="%g"/>\n' % (v[0], v[1], v[2]) for v in verts)
    ts = "".join('     <triangle v1="%d" v2="%d" v3="%d"/>\n' % (f[0], f[1], f[2]) for f in faces)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<model unit="millimeter" xml:lang="en-US" '
            'xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02" '
            'xmlns:BambuStudio="http://schemas.bambulab.com/package/2021" '
            'xmlns:p="http://schemas.microsoft.com/3dmanufacturing/production/2015/06" requiredextensions="p">\n'
            ' <metadata name="BambuStudio:3mfVersion">1</metadata>\n <resources>\n'
            '  <object id="1" p:UUID="00010000-81cb-4c03-9d28-80fed5dfa1dc" type="model">\n'
            '   <mesh>\n    <vertices>\n%s    </vertices>\n    <triangles>\n%s    </triangles>\n   </mesh>\n'
            '  </object>\n </resources>\n</model>\n' % (vs, ts))


def _3dmodel(name, bx, by) -> str:
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<model unit="millimeter" xml:lang="en-US" '
            'xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02" '
            'xmlns:BambuStudio="http://schemas.bambulab.com/package/2021" '
            'xmlns:p="http://schemas.microsoft.com/3dmanufacturing/production/2015/06" requiredextensions="p">\n'
            ' <metadata name="Application">BambuStudio-02.07.01.57</metadata>\n'
            ' <metadata name="BambuStudio:3mfVersion">1</metadata>\n'
            ' <metadata name="Title">%s</metadata>\n'
            ' <resources>\n'
            '  <object id="5" p:UUID="00000001-61cb-4c03-9d28-80fed5dfa1dc" type="model">\n'
            '   <components>\n'
            '    <component p:path="/3D/Objects/object_1.model" objectid="1" '
            'p:UUID="00010000-b206-40ff-9872-83e8017abed1" transform="1 0 0 0 1 0 0 0 1 0 0 0"/>\n'
            '   </components>\n'
            '  </object>\n'
            ' </resources>\n'
            ' <build p:UUID="2c7c17d8-22b5-4d84-8835-1976022ea369">\n'
            '  <item objectid="5" p:UUID="00000005-b1ec-4553-aec9-835e5b724bb4" '
            'transform="1 0 0 0 1 0 0 0 1 %g %g 0" printable="1"/>\n'
            ' </build>\n</model>\n' % (name, bx, by))


def _model_settings(name, nfaces, cx, cy) -> str:
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<config>\n'
            '  <object id="5">\n'
            '    <metadata key="name" value="%s"/>\n'
            '    <metadata key="extruder" value="1"/>\n'
            '    <metadata face_count="%d"/>\n'
            '    <part id="1" subtype="normal_part">\n'
            '      <metadata key="name" value="%s"/>\n'
            '      <metadata key="matrix" value="1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1"/>\n'
            '      <metadata key="source_file" value="%s.stl"/>\n'
            '      <metadata key="source_offset_x" value="%g"/>'
            '<metadata key="source_offset_y" value="%g"/><metadata key="source_offset_z" value="0"/>\n'
            '      <metadata key="extruder" value="1"/>\n'
            '      <mesh_stat face_count="%d" edges_fixed="0" degenerate_facets="0" '
            'facets_removed="0" facets_reversed="0" backwards_edges="0"/>\n'
            '    </part>\n'
            '  </object>\n'
            '  <plate>\n'
            '    <metadata key="plater_id" value="1"/>\n'
            '    <metadata key="filament_map_mode" value="Auto"/>\n'
            '    <metadata key="thumbnail_file" value="Metadata/plate_1.png"/>\n'
            '    <metadata key="thumbnail_no_light_file" value="Metadata/plate_no_light_1.png"/>\n'
            '    <metadata key="top_file" value="Metadata/top_1.png"/>\n'
            '    <metadata key="pick_file" value="Metadata/pick_1.png"/>\n'
            '    <model_instance><metadata key="object_id" value="5"/>'
            '<metadata key="instance_id" value="0"/><metadata key="identify_id" value="2592"/></model_instance>\n'
            '  </plate>\n'
            '  <assemble><assemble_item object_id="5" instance_id="0" '
            'transform="1 0 0 0 1 0 0 0 1 %g %g 0" offset="0 0 0" /></assemble>\n'
            '</config>\n' % (name, nfaces, name, name, cx, cy, nfaces, cx, cy))


def stl_to_3mf(stl_path: str, printer: str = "a1mini", out_3mf: str | None = None,
               model_name: str | None = None) -> str:
    """STL を指定プリンタ（a1mini / h2d）の印刷用 3mf へ変換して保存し、そのパスを返す。"""
    if printer not in PRINTERS:
        raise ValueError("未知のプリンタ: %s（%s のいずれか）" % (printer, ", ".join(PRINTERS)))
    prof = PRINTERS[printer]
    bed = prof["bed"]
    skeleton = os.path.join(TEMPLATES, prof["skeleton"])
    project = os.path.join(TEMPLATES, prof["project"]) if prof["project"] else None
    if not os.path.exists(skeleton):
        raise FileNotFoundError("骨組み %s が無い" % skeleton)
    if project and not os.path.exists(project):
        raise FileNotFoundError("印刷設定 %s が無い" % project)
    name = model_name or os.path.splitext(os.path.basename(stl_path))[0]
    out_3mf = out_3mf or os.path.splitext(stl_path)[0] + prof["suffix"] + ".3mf"

    m = npmesh.Mesh.from_file(stl_path)
    tris = m.vectors.astype(np.float64)
    # x/y の中心を原点へ寄せる（配置は build 側の transform でベッド中央へ運ぶ）
    pts = tris.reshape(-1, 3)
    mn, mx = pts.min(0), pts.max(0)
    cx, cy = (mn[0] + mx[0]) / 2, (mn[1] + mx[1]) / 2
    tris[:, :, 0] -= cx
    tris[:, :, 1] -= cy
    dim = mx - mn
    if dim[0] > bed[0] or dim[1] > bed[1]:
        raise ValueError("ベッド %gx%g に収まらない（外形 %.1fx%.1f）" % (bed[0], bed[1], dim[0], dim[1]))

    verts, faces = _dedupe(tris)

    work = tempfile.mkdtemp()
    ref = os.path.join(work, "ref")
    try:
        with zipfile.ZipFile(skeleton) as z:
            z.extractall(ref)
        # 骨組みに残る既存のオブジェクトモデル（object_2.model 等）を消してから自分のを書く。
        objdir = os.path.join(ref, "3D/Objects")
        if os.path.isdir(objdir):
            for fn in os.listdir(objdir):
                if fn.endswith(".model"):
                    os.remove(os.path.join(objdir, fn))
        os.makedirs(objdir, exist_ok=True)
        with open(os.path.join(objdir, "object_1.model"), "w") as f:
            f.write(_object_model(verts, faces))
        # 3dmodel.model.rels を object_1.model へ向け直す（骨組みが object_2 等を指す場合の対策）。
        rels = os.path.join(ref, "3D/_rels/3dmodel.model.rels")
        os.makedirs(os.path.dirname(rels), exist_ok=True)
        with open(rels, "w") as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">\n'
                    ' <Relationship Target="/3D/Objects/object_1.model" Id="rel-1" '
                    'Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>\n'
                    '</Relationships>\n')
        with open(os.path.join(ref, "3D/3dmodel.model"), "w") as f:
            f.write(_3dmodel(name, bed[0] / 2, bed[1] / 2))
        with open(os.path.join(ref, "Metadata/model_settings.config"), "w") as f:
            f.write(_model_settings(name, len(faces), cx, cy))
        # a1mini は骨組みの複数フィラメント設定を単一フィラメント版へ差し替える。
        # h2d は骨組み（実績3mf）の設定をそのまま使う（project=None）。
        if project:
            shutil.copyfile(project, os.path.join(ref, "Metadata/project_settings.config"))
        with open(os.path.join(ref, "Metadata/filament_sequence.json"), "w") as f:
            f.write('{"plate_1":{"nozzle_sequence":[],"optimal_assignment":[],"sequence":[]}}')
        if os.path.exists(out_3mf):
            os.remove(out_3mf)
        with zipfile.ZipFile(out_3mf, "w", zipfile.ZIP_DEFLATED) as z:
            for r, _, fs in os.walk(ref):
                for fn in fs:
                    full = os.path.join(r, fn)
                    z.write(full, os.path.relpath(full, ref))
    finally:
        shutil.rmtree(work)
    return out_3mf


def stl_to_a1mini_3mf(stl_path: str, out_3mf: str | None = None,
                      model_name: str | None = None) -> str:
    """後方互換の別名。A1 mini 用 3mf を作る。"""
    return stl_to_3mf(stl_path, "a1mini", out_3mf, model_name)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="STL を A1 mini / H2D 印刷用 3mf へ変換")
    ap.add_argument("stl", help="入力STLのパス")
    ap.add_argument("--printer", choices=list(PRINTERS), default="a1mini")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    out = stl_to_3mf(a.stl, a.printer, a.out)
    print("書き出した 3mf（%s）: %s (%.0f KB)" % (a.printer, out, os.path.getsize(out) / 1024))
