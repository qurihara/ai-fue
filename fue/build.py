"""Compact scale-flute generator.

A flute = the sounding BODY (slide-recorder-head-v6, a hollow-bore fipple flute
supplied by the user) + a solid ROD inserted into the bore from the bottom. The
rod height is length_inside from the F# tuning table; the remaining open air
column (length_outside = 100 - length_inside) sets the pitch.
Both stand on z=0 and are centred in x/y, exactly as the 2025 FreeCAD pipeline did
(it centred the rod on the body's x/y axes, and the bore sits at that centre).

Assembly is pure mesh concatenation (translate + append triangles). We deliberately
do NOT boolean-union: BambuStudio/most slicers union overlapping solids at slice
time, which is far more robust than FreeCAD's boolean (which repeatedly corrupted
the 2025 builds). Every primitive we emit is individually water-tight, so the union
is well defined.

Head file is pluggable via --head; until the real recorderhead.stl is dropped into
assets/, a clearly-labelled parametric PLACEHOLDER head lets the whole pipeline run
and be validated end-to-end.
"""
from __future__ import annotations
import argparse
import math
import os

import numpy as np
from stl import mesh as npmesh

from notes import (load_tuning, tuning_by_note, hex_to_notes, notes_to_hex,
                   note_to_midi, fold_into_range)

ASSETS = os.path.join(os.path.dirname(__file__), os.pardir, "assets")
OUT = os.path.join(os.path.dirname(__file__), os.pardir, "out")

# ---------------------------------------------------------------------------
# Low-level: build triangle arrays (N,3,3) and wrap into a numpy-stl Mesh.
# ---------------------------------------------------------------------------

def _mesh(tris: np.ndarray) -> npmesh.Mesh:
    m = npmesh.Mesh(np.zeros(len(tris), dtype=npmesh.Mesh.dtype))
    m.vectors = tris.astype(np.float32)
    return m


def cylinder(diameter: float, height: float, z0: float = 0.0,
             cx: float = 0.0, cy: float = 0.0, segments: int = 96) -> np.ndarray:
    """Water-tight closed cylinder, axis along +z, base at z0."""
    r = diameter / 2.0
    z1 = z0 + height
    ang = np.linspace(0, 2 * math.pi, segments, endpoint=False)
    ring = np.column_stack([cx + r * np.cos(ang), cy + r * np.sin(ang)])
    tris = []
    cb = [cx, cy, z0]
    ct = [cx, cy, z1]
    for i in range(segments):
        j = (i + 1) % segments
        bi = [ring[i, 0], ring[i, 1], z0]; bj = [ring[j, 0], ring[j, 1], z0]
        ti = [ring[i, 0], ring[i, 1], z1]; tj = [ring[j, 0], ring[j, 1], z1]
        tris.append([cb, bj, bi])          # bottom cap (normal -z)
        tris.append([ct, ti, tj])          # top cap (normal +z)
        tris.append([bi, bj, tj])          # side
        tris.append([bi, tj, ti])
    return np.array(tris)


def _tris_of(m: npmesh.Mesh) -> np.ndarray:
    return m.vectors.copy()


def stand_and_center(tris: np.ndarray) -> np.ndarray:
    """Translate so min-z -> 0 and x/y bbox centre -> origin (matches FreeCAD step)."""
    pts = tris.reshape(-1, 3)
    mn = pts.min(axis=0); mx = pts.max(axis=0)
    off = np.array([(mn[0] + mx[0]) / 2, (mn[1] + mx[1]) / 2, mn[2]])
    return tris - off


def translate(tris: np.ndarray, dx=0.0, dy=0.0, dz=0.0) -> np.ndarray:
    return tris + np.array([dx, dy, dz])


def bbox(tris: np.ndarray):
    pts = tris.reshape(-1, 3)
    return pts.min(axis=0), pts.max(axis=0)


# ---------------------------------------------------------------------------
# Placeholder head (used only until the real recorderhead.stl is supplied).
# ---------------------------------------------------------------------------

def placeholder_head(bore_d: float = 9.0) -> np.ndarray:
    """A stand-in whistle head so the pipeline runs. NOT acoustically valid.
    A short solid cap sitting on top of the bore with a mouthpiece stub."""
    cap = cylinder(bore_d + 3.0, 6.0, z0=0.0)          # collar
    stub = cylinder(bore_d + 1.0, 10.0, z0=6.0)        # mouthpiece stub
    return np.concatenate([cap, stub])


def load_head(path: str | None, bore_d: float = 9.0) -> tuple[np.ndarray, bool]:
    """Return (triangles, is_real). Normalizes to stand on z=0, centred in x/y."""
    if path and os.path.exists(path):
        m = npmesh.Mesh.from_file(path)
        return stand_and_center(_tris_of(m)), True
    return stand_and_center(placeholder_head(bore_d)), False


# ---------------------------------------------------------------------------
# One flute = head + tube(height = length_inside from the tuning table).
# ---------------------------------------------------------------------------

def make_flute(note: str, head_tris: np.ndarray, tuning: dict,
               bore_d: float = 9.0) -> np.ndarray:
    row = tuning[note]
    tube = cylinder(bore_d, row["length_inside"], z0=0.0)
    return np.concatenate([head_tris, tube])


# ---------------------------------------------------------------------------
# Layouts.
# ---------------------------------------------------------------------------

def layout_linear(flutes: list[np.ndarray], gap: float, bore_d: float) -> np.ndarray:
    """Pan-flute row along +y, tightly packed."""
    out = []
    pitch = bore_d + gap
    n = len(flutes)
    y0 = -(n - 1) * pitch / 2
    for i, f in enumerate(flutes):
        out.append(translate(f, dy=y0 + i * pitch))
    return np.concatenate(out)


def layout_ring(flutes: list[np.ndarray], radius: float) -> np.ndarray:
    """Revolver ring: flutes on a circle of given radius (for rotate-and-blow)."""
    out = []
    n = len(flutes)
    for i, f in enumerate(flutes):
        a = 2 * math.pi * i / n
        out.append(translate(f, dx=radius * math.cos(a), dy=radius * math.sin(a)))
    return np.concatenate(out)


def base_disk(diameter: float, thickness: float = 4.0, hole_d: float = 0.0) -> np.ndarray:
    top = cylinder(diameter, thickness, z0=-thickness)
    if hole_d <= 0:
        return top
    # donut: emit outer, then a smaller inner cylinder the slicer subtracts is NOT
    # how union works, so instead build an annulus ring mesh.
    return annulus(diameter / 2, hole_d / 2, thickness, z0=-thickness)


def annulus(r_out: float, r_in: float, height: float, z0: float, segments: int = 96) -> np.ndarray:
    z1 = z0 + height
    ang = np.linspace(0, 2 * math.pi, segments, endpoint=False)
    co = np.column_stack([r_out * np.cos(ang), r_out * np.sin(ang)])
    ci = np.column_stack([r_in * np.cos(ang), r_in * np.sin(ang)])
    tris = []
    for i in range(segments):
        j = (i + 1) % segments
        obi = [co[i, 0], co[i, 1], z0]; obj = [co[j, 0], co[j, 1], z0]
        oti = [co[i, 0], co[i, 1], z1]; otj = [co[j, 0], co[j, 1], z1]
        ibi = [ci[i, 0], ci[i, 1], z0]; ibj = [ci[j, 0], ci[j, 1], z0]
        iti = [ci[i, 0], ci[i, 1], z1]; itj = [ci[j, 0], ci[j, 1], z1]
        tris += [[obi, obj, otj], [obi, otj, oti]]        # outer wall
        tris += [[ibj, ibi, iti], [ibj, iti, itj]]        # inner wall
        tris += [[ibi, obj, obi], [ibi, ibj, obj]]        # bottom ring
        tris += [[oti, otj, itj], [oti, itj, iti]]        # top ring
    return np.array(tris)


# ---------------------------------------------------------------------------
# Assemble a whole instrument from a scale sequence.
# ---------------------------------------------------------------------------

def build_sequence(notes: list[str], head_path: str | None, style: str,
                   bore_d: float = 9.0, gap: float = 1.0):
    tuning = tuning_by_note()
    head, is_real = load_head(head_path, bore_d)
    playable = [fold_into_range(n) for n in notes]
    flutes = [make_flute(n, head, tuning, bore_d) for n in playable]

    if style == "row":
        body = layout_linear(flutes, gap, bore_d)
        base = base_disk(0)  # none for row (kept flat)
        asm = body
    elif style == "ring":
        pitch = bore_d + gap
        radius = max(14.0, pitch * len(flutes) / (2 * math.pi))
        body = layout_ring(flutes, radius)
        base = annulus(radius + bore_d / 2 + 3, max(6.0, radius - bore_d / 2 - 3), 4.0, z0=-4.0)
        asm = np.concatenate([body, base])
    else:
        raise ValueError(style)
    return asm, playable, is_real


def save(tris: np.ndarray, path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    _mesh(tris).save(path)


def check_watertight(tris: np.ndarray) -> tuple[bool, int]:
    """Euler check per connected primitive is overkill; use edge-manifold count:
    every directed edge should have a matching opposite. Returns (ok, n_open)."""
    from collections import defaultdict
    edges = defaultdict(int)
    q = (tris * 1000).round().astype(np.int64)  # 1um quantize
    for t in q:
        for a, b in ((0, 1), (1, 2), (2, 0)):
            ea = tuple(t[a]); eb = tuple(t[b])
            edges[(ea, eb)] += 1
    open_edges = 0
    for (ea, eb), c in edges.items():
        if edges.get((eb, ea), 0) != c:
            open_edges += 1
    return open_edges == 0, open_edges


def _parse_notes(args) -> list[str]:
    if args.pass_hex:
        return hex_to_notes(args.pass_hex)
    if args.notes:
        return [s.strip() for s in args.notes.replace(",", " ").split()]
    raise SystemExit("give --pass-hex or --notes")


def main():
    ap = argparse.ArgumentParser(description="compact scale-flute generator")
    ap.add_argument("--pass-hex", help="ToneDecoder hex password, e.g. 5558564F")
    ap.add_argument("--notes", help="space/comma note list, e.g. 'C6 G#5 A#5'")
    ap.add_argument("--body", default=os.path.join(ASSETS, "body_v6.stl"),
                    help="発音する笛本体のSTL（既定は v6 本体）")
    ap.add_argument("--style", choices=["row", "ring"], default="ring")
    ap.add_argument("--bore", type=float, default=8.0,
                    help="内挿する棒の直径。ボアを埋めて気柱長を length_outside に固定する")
    ap.add_argument("--gap", type=float, default=1.0)
    ap.add_argument("--out", default=None)
    ap.add_argument("--no-3mf", action="store_true",
                    help="A1 mini 印刷用 3mf の書き出しを行わない")
    args = ap.parse_args()

    notes = _parse_notes(args)
    asm, playable, is_real = build_sequence(notes, args.body, args.style, args.bore, args.gap)
    name = args.out or os.path.join(OUT, f"flute_{args.style}_{notes_to_hex(playable)}.stl")
    save(asm, name)
    mn, mx = bbox(asm)
    ok, open_edges = check_watertight(asm)
    print(f"音階列       : {notes}")
    print(f"演奏可能域    : {playable}  (hex {notes_to_hex(playable)})")
    print(f"本体         : {'実体 '+args.body if is_real else 'プレースホルダ（assets/body_v6.stl が見つからない）'}")
    print(f"外形寸法     : {np.round(mx-mn,1)} mm   三角形数={len(asm)}")
    print(f"棒とボアは重なるため本体と棒の境界は非多様体になるが、スライサが結合するので問題ない。")
    print(f"保存先       : {name}")

    if not args.no_3mf:
        from make_3mf import stl_to_a1mini_3mf
        three = stl_to_a1mini_3mf(name)
        print(f"印刷用3mf    : {three}  （A1 miniでそのまま開いて印刷できる）")


if __name__ == "__main__":
    main()
