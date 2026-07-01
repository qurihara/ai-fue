"""STL を Bambu A1 mini で直接印刷できる 3mf へ変換する。

導電性ゲームコントローラの make_3mf.py と同じ考え方を使う。すなわち、Bambu Studio
で保存した動作実績のある A1 mini 設定一式を骨組み（templates/a1mini_skeleton.3mf）
として持ち、その中の形状とモデル設定だけを差し替える。印刷設定（project_settings）は
骨組みのものをそのまま使うので、標準プリセットへ勝手に戻る問題を避けられる。

笛は単一素材なので、コントローラの2部品（土台と配線）構成を単一オブジェクトへ簡略化した。
ベッド180×180の中央（90, 90）へ、x/yの中心を原点へ寄せた状態で配置する。
"""
from __future__ import annotations
import os
import shutil
import tempfile
import zipfile

import numpy as np
from stl import mesh as npmesh

HERE = os.path.dirname(__file__)
TEMPLATES = os.path.join(HERE, os.pardir, "templates")
SKELETON = os.path.join(TEMPLATES, "a1mini_skeleton.3mf")
# 単一フィラメントの A1 mini 印刷設定（BambuStudio がSTLをスライスしたものから収穫した実績版）。
# 骨組みのコントローラ用3mfはAMSに6本のフィラメントを定義しており、単一素材の笛では
# 「mixed filament is not supported」で弾かれるため、この単一設定で必ず上書きする。
PROJECT_SETTINGS = os.path.join(TEMPLATES, "a1mini_project_settings.config")
BED = (180.0, 180.0)  # A1 mini


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


def stl_to_a1mini_3mf(stl_path: str, out_3mf: str | None = None,
                      model_name: str | None = None) -> str:
    """STL を A1 mini 印刷用 3mf へ変換して保存し、そのパスを返す。"""
    if not os.path.exists(SKELETON):
        raise FileNotFoundError("骨組み %s が無い" % SKELETON)
    name = model_name or os.path.splitext(os.path.basename(stl_path))[0]
    out_3mf = out_3mf or os.path.splitext(stl_path)[0] + "_a1mini.3mf"

    m = npmesh.Mesh.from_file(stl_path)
    tris = m.vectors.astype(np.float64)
    # x/y の中心を原点へ寄せる（配置は build 側の transform でベッド中央へ運ぶ）
    pts = tris.reshape(-1, 3)
    mn, mx = pts.min(0), pts.max(0)
    cx, cy = (mn[0] + mx[0]) / 2, (mn[1] + mx[1]) / 2
    tris[:, :, 0] -= cx
    tris[:, :, 1] -= cy
    dim = mx - mn
    if dim[0] > BED[0] or dim[1] > BED[1]:
        raise ValueError("ベッド %gx%g に収まらない（外形 %.1fx%.1f）" % (BED[0], BED[1], dim[0], dim[1]))

    verts, faces = _dedupe(tris)

    work = tempfile.mkdtemp()
    ref = os.path.join(work, "ref")
    try:
        with zipfile.ZipFile(SKELETON) as z:
            z.extractall(ref)
        with open(os.path.join(ref, "3D/Objects/object_1.model"), "w") as f:
            f.write(_object_model(verts, faces))
        with open(os.path.join(ref, "3D/3dmodel.model"), "w") as f:
            f.write(_3dmodel(name, BED[0] / 2, BED[1] / 2))
        with open(os.path.join(ref, "Metadata/model_settings.config"), "w") as f:
            f.write(_model_settings(name, len(faces), cx, cy))
        # 印刷設定を単一フィラメント版へ差し替える（骨組みの6フィラメント定義を捨てる）。
        shutil.copyfile(PROJECT_SETTINGS, os.path.join(ref, "Metadata/project_settings.config"))
        # フィラメント列を単一に整える。
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


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        raise SystemExit("使い方: python make_3mf.py <stlのパス> [出力3mfのパス]")
    out = stl_to_a1mini_3mf(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
    kb = os.path.getsize(out) / 1024
    print("書き出した 3mf: %s (%.0f KB)" % (out, kb))
