#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""公開用リポジトリ cipherflute を、この開発用リポジトリから書き出す。

なぜ要るか
----------
開発用の ai-fue は出力物を含めて841MBあり、そのままでは配布に向かない。かといって
手作業で選んで複製すると、更新のたびに何を写したか分からなくなる。

そこで[* 書き出しをスクリプトにする]。何を入れ、何を入れないかがコードに残り、
更新のたびに同じ手順で作り直せる。公開用リポジトリは、いつでも捨てて作り直してよい。

使い方:
    python3 scripts/export_public.py                    既定の場所へ書き出す
    python3 scripts/export_public.py --out <パス>       場所を指定する
    python3 scripts/export_public.py --dry-run          何をするかだけ出す
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))
SKILLS = os.path.expanduser("~/.claude/skills")
DEFAULT_OUT = os.path.abspath(os.path.join(ROOT, os.pardir, "cipherflute"))

sys.path.insert(0, os.path.join(ROOT, "fue"))


def log(msg):
    print("  " + msg)


def copy(src, dst, dry=False):
    """1つ写す。src が無ければ知らせて飛ばす（止めない）。"""
    if not os.path.exists(src):
        log("★見つからない★ %s" % src)
        return False
    if dry:
        log("写す予定 %s" % os.path.relpath(dst, DEFAULT_OUT))
        return True
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(src, dst)
    log("写した %s" % os.path.relpath(dst, os.path.dirname(os.path.dirname(dst))))
    return True


# ---------------------------------------------------------------- 笛の素材

def export_flutes(out, dry=False):
    """統一管長の笛を12音ぶん書き出し、較正データを添える。

    外形はすべて同じで、中の空洞の長さだけが違う。これが「見た目から音が読めない」
    という設計の要である。
    """
    import mini10
    d = os.path.join(out, "flutes")
    os.makedirs(os.path.join(d, "uniform"), exist_ok=True)

    notes = mini10.CALIB12
    Ls = [mini10.length_for_note(n) for n in notes]
    l_max = mini10.uniform_body_length(Ls)

    rows = []
    for note, L in zip(notes, Ls):
        f = mini10.note_to_freq(note)
        name = "flute_%s.stl" % note.replace("#", "s")
        rows.append(dict(note=note, freq_hz=round(f, 2), bore_mm=round(L, 3), file=name))
        if dry:
            continue
        m = mini10.uniform_flute(L, l_max)
        m.export(os.path.join(d, "uniform", name))
    log("笛 %d本（統一外形長 %.2fmm）" % (len(rows), l_max))

    calib = dict(
        note_range=[notes[0], notes[-1]],
        reference_note="C7",
        step_cents=100,
        body_length_mm=round(l_max, 3),
        formula="freq_hz = A / (bore_mm - e)",
        A=mini10.A, e=mini10.E,
        note="この係数は実測から当てはめたものである。当てはめには設計値ではなく、"
             "造形データから実測した空洞の長さを用いた。プリンタや材料が違えば"
             "ずれるので、手元で較正コームを刷って測り直すこと。",
        mesh_note="12本のうち数本は、内部の仕切り壁が外壁に接する箇所で辺が4つの面に"
                  "共有される（穴は開いていない）。スライサは問題なく扱え、実機で刷って"
                  "鳴ることを確かめてあるが、厳密な水密性を求める道具では警告が出る。"
                  "自動修復をかけると形が変わって音がずれるので、直していない。",
        notes=rows,
    )
    if not dry:
        with open(os.path.join(d, "calibration.json"), "w", encoding="utf-8") as fp:
            json.dump(calib, fp, ensure_ascii=False, indent=2)
    log("較正データ（A=%.1f, e=%.3f）" % (mini10.A, mini10.E))
    return calib


# ---------------------------------------------------------------- 符号

def export_codec(out, dry=False):
    """符号の参照実装（Python）と、言語をまたいで正しさを確かめる試験ベクタ。"""
    d = os.path.join(out, "codec")
    copy(os.path.join(ROOT, "fue/cipher_codec.py"), os.path.join(d, "cipher_codec.py"), dry)
    # cipher_codec.py が音名と周波数の対応をここから読む。無いと import そのものが通らない。
    copy(os.path.join(ROOT, "fue/notes.py"), os.path.join(d, "notes.py"), dry)
    copy(os.path.join(ROOT, "fue/threshold.py"), os.path.join(d, "threshold.py"), dry)
    copy(os.path.join(ROOT, "docs/cipher/cipher_test_vectors.json"),
         os.path.join(d, "test_vectors.json"), dry)
    # 紙の上で誤り訂正まで行うための早見表と、その検証
    copy(os.path.join(ROOT, "docs/cipher/manual_decode_card.md"),
         os.path.join(d, "manual_decode_card.md"), dry)
    copy(os.path.join(ROOT, "scripts/verify_manual_decode.py"),
         os.path.join(d, "verify_manual_decode.py"), dry)
    copy(os.path.join(ROOT, "docs/cipher/cipher_config.json"),
         os.path.join(d, "default_config.json"), dry)
    if dry:
        return
    # 開発用では cipher_codec.py が fue パッケージの中にあるが、公開用では隣に置く。
    # 読み込み方を直さないと、そのままでは動かない。
    p = os.path.join(d, "verify_manual_decode.py")
    s = open(p, encoding="utf-8").read()
    s = s.replace(
        'sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))\n'
        'from fue import cipher_codec as cc  # noqa: E402',
        '# 公開版では、このファイルと同じ場所に cipher_codec.py を置いてある\n'
        'sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))\n'
        'import cipher_codec as cc  # noqa: E402')
    open(p, "w", encoding="utf-8").write(s)
    log("verify_manual_decode.py の読み込み方を公開版に合わせた")


# ---------------------------------------------------------------- 復号器

def export_decoder(out, dry=False):
    """ブラウザだけで動く復号器。検査も一緒に入れる（正しさの根拠になる）。"""
    d = os.path.join(out, "decoder")
    src = os.path.join(ROOT, "docs/cipher")
    for f in ("index.html", "cipher_codec.js", "fft_peak.js", "silence_segmenter.js",
              "tempo_filter.js", "cipher_config.json", "cipher_test_vectors.json",
              "fft_peak.test.js", "silence_segmenter.test.js", "tempo_filter.test.js",
              "cipher_codec.test.js"):
        copy(os.path.join(src, f), os.path.join(d, f), dry)


# ---------------------------------------------------------------- 埋め込み

def export_embed(out, dry=False):
    """日用品へ笛を埋め込む道具と、2つの検査。"""
    d = os.path.join(out, "embed")
    copy(os.path.join(SKILLS, "flute-embed/scripts/embed_flutes.py"),
         os.path.join(d, "embed_flutes.py"), dry)
    # 判断を伴う部分は手順書（スキル）の側にある。プログラムだけでは埋め込みは再現できない。
    # 手元のスキル（~/.claude/skills）は個人の環境と非公開の記録に依存しているので、
    # そのままでは配れない。公開用に書き直したものを docs/skills に置いてあり、そちらを写す。
    copy(os.path.join(ROOT, "docs/skills/flute-embed.md"),
         os.path.join(d, "flute-embed.md"), dry)
    copy(os.path.join(ROOT, "fue/orient_check.py"), os.path.join(d, "orient_check.py"), dry)
    copy(os.path.join(ROOT, "scripts/check_flute_cavity.py"),
         os.path.join(d, "check_cavity.py"), dry)
    # check_cavity.py が gcode から押し出し線を読むのに使う。無いと動かない。
    copy(os.path.join(ROOT, "fue/check_cavity.py"),
         os.path.join(d, "gcode_segments.py"), dry)
    copy(os.path.join(ROOT, "fue/mini10.py"), os.path.join(d, "mini10.py"), dry)
    # 笛の素の形（発音部を持つ半割りリコーダー）。mini10.py がこれを読んで
    # ボアを伸ばし縮みさせるので、これが無いと笛を作れない。栗原さんがTinkercadで
    # 作ったもので、印刷と発音の実績がある
    copy(os.path.join(ROOT, "mini10/recorder-mini-c-v3-half-2-v2.stl"),
         os.path.join(d, "mini10", "recorder-mini-c-v3-half-2-v2.stl"), dry)
    if dry:
        return
    # 開発用では mini10.py の1つ上に mini10/ と out/ があるが、公開用では平らに置く。
    # 探し先を自分と同じ場所へ直し、較正も同梱の calibration.json から読ませる。
    p = os.path.join(d, "mini10.py")
    s = open(p, encoding="utf-8").read()
    s = s.replace('ROOT = os.path.join(os.path.dirname(__file__), os.pardir)',
                  '# 公開版では、このファイルと同じ場所に mini10/ を置いてある\n'
                  'ROOT = os.path.dirname(os.path.abspath(__file__))')
    s = s.replace('OUT = os.path.join(ROOT, "out")',
                  'OUT = os.path.join(ROOT, os.pardir, "flutes")   # 較正は flutes/ にある')
    s = s.replace('for name in ("cipher_mini10_calib.txt", "mini10_calib_v11.txt"):',
                  'for name in ("calibration.json",):')
    # 較正の読み方も JSON へ合わせる
    s = s.replace('''            for line in open(p):
                line = line.strip()
                if line.startswith("A="):
                    A = float(line.split("=")[1].split()[0])
                elif line.lower().startswith("e="):
                    E = float(line.split("=")[1].split()[0])
            break''',
                  '''            import json as _json
            _c = _json.load(open(p, encoding="utf-8"))
            A, E = float(_c["A"]), float(_c["e"])
            break''')
    open(p, "w", encoding="utf-8").write(s)
    log("mini10.py のパスと較正の読み方を公開版に合わせた")

    # check_cavity.py も、開発用では fue パッケージ越しに読んでいる。公開版では隣に置く。
    p = os.path.join(d, "check_cavity.py")
    s = open(p, encoding="utf-8").read()
    s = s.replace('from fue.check_cavity import load_segments  # noqa: E402',
                  'from gcode_segments import load_segments  # noqa: E402')
    open(p, "w", encoding="utf-8").write(s)
    log("check_cavity.py の読み込み方を公開版に合わせた")


# ---------------------------------------------------------------- 作例

# 第三者が権利を持つモデルを土台にした作例は、写真も造形データも入れない。
# 出所だけを NOTICE.md に記す。
GALLERY_PHOTOS = [
    ("out/hokusai_tiles_photo_framed.jpg", "tiles_framed.jpg",
     "画像タイル9枚を額縁に収めたところ"),
    ("out/hokusai_tiles_photo_flutes.jpg", "tiles_back.jpg",
     "1枚を裏返したところ。笛9本が並ぶ"),
    ("out/hokusai_tiles_photo_standing.jpg", "tiles_standing.jpg",
     "脚を付けて自立させたところ"),
    ("out/karuta_photo_front.jpg", "karuta_front.jpg",
     "かるたの読み札2枚。右が上の句、左が下の句で、そろって歌が完成する"),
    ("out/karuta_photo_back.jpg", "karuta_back.jpg",
     "上の句の札を裏返したところ。笛8本が並ぶ"),
    ("out/paircards_photo.jpg", "paircards.jpg",
     "2枚そろって初めてハートが現れるカード"),
    ("out/card_photo.jpg", "card.jpg",
     "カード1枚。笛8本で20.8bitを記録する"),
    ("out/card_2of3_photo.jpg", "card_2of3.jpg",
     "2-of-3の断片を担うカード"),
    ("out/box_inside_photo.jpg", "box_inside.jpg",
     "箱の内部。床に笛を仕込み、窓は内側へ開く"),
    ("out/box_pens_photo.jpg", "box_pens.jpg",
     "ペンを立てたところ。机の上では文房具にしか見えない"),
]
GALLERY_MODELS = [
    ("out/hokusai_frame_box_plain.stl", "frame_box.stl", "額縁（模様なし）"),
    ("out/hokusai_frame_box_plain_stand.stl", "frame_stand.stl", "自立させる脚2本"),
    ("out/karuta/sutoku_edge_h2d.3mf", "karuta_2of2.3mf",
     "かるたの読み札2枚（3色刷り。白い地・黒い字・緑のふち）"),
    ("out/cipher_cardpair_v3.3mf", "paircards_2of2.3mf",
     "ハートを抜いた2枚組のカード"),
    ("out/cipher_card_v4_share2.3mf", "card.3mf", "カード1枚"),
    ("out/cardbox_v1_share1.3mf", "box.3mf", "笛を床に仕込んだ枡箱"),
]


def export_gallery(out, dry=False):
    d = os.path.join(out, "gallery")
    for src, dst, _ in GALLERY_PHOTOS:
        copy(os.path.join(ROOT, src), os.path.join(d, "photos", dst), dry)
    for src, dst, _ in GALLERY_MODELS:
        copy(os.path.join(ROOT, src), os.path.join(d, "models", dst), dry)


def main(argv=None):
    ap = argparse.ArgumentParser(description="公開用リポジトリを書き出す")
    ap.add_argument("--out", default=DEFAULT_OUT, help="書き出し先")
    ap.add_argument("--dry-run", action="store_true", help="何をするかだけ出す")
    args = ap.parse_args(argv)
    out = os.path.abspath(args.out)

    print("公開用リポジトリを書き出す -> %s" % out)
    print()
    print("笛の素材")
    export_flutes(out, args.dry_run)
    print("符号")
    export_codec(out, args.dry_run)
    print("復号器")
    export_decoder(out, args.dry_run)
    print("埋め込み")
    export_embed(out, args.dry_run)
    print("作例")
    export_gallery(out, args.dry_run)
    print()
    print("※ README・LICENSE・NOTICE・SPEC・HOWTO は書き下ろしなので、この書き出しでは触らない。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
