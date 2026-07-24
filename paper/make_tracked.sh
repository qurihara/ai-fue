#!/bin/sh
# ---------------------------------------------------------------------------
# CipherFlute 論文の「変更前 -> 変更後」編集履歴(tracked changes)付き docx と，
# 編集履歴なしのクリーンな PDF を作る。
#
# 前提: make_paper_wiss_v12.py は再生成の前に既存 docx を
#       paper/prev/cipherflute_wiss2026_v1.2_prev.docx へ退避している。
#
# 手順:
#   1) make_paper_wiss_v12.py で最新 docx を生成（同時に prev/ へ旧版を退避）。
#   2) make_tracked.py で prev(変更前) と最新(変更後) を比較し，w:ins/w:del の
#      編集履歴を書き込んだ  *_tracked.docx を出力。
#   3) LibreOffice で最新 docx から編集履歴なしのクリーン PDF を出力。
#
# soffice が PATH になければ LibreOffice.app 同梱のものを使う。
# ---------------------------------------------------------------------------
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE"

SOFFICE="$(command -v soffice || true)"
if [ -z "$SOFFICE" ]; then
  SOFFICE="/Applications/LibreOffice.app/Contents/MacOS/soffice"
fi

echo "[1/3] regenerate docx (+ backup previous to prev/)"
python3 make_paper_wiss_v12.py

echo "[2/3] build tracked-changes docx (prev -> current)"
python3 make_tracked.py

echo "[3/3] export clean PDF (no tracked changes)"
"$SOFFICE" --headless --convert-to pdf --outdir "$HERE" cipherflute_wiss2026_v1.2.docx

echo "done:"
echo "  clean docx   : cipherflute_wiss2026_v1.2.docx"
echo "  clean pdf    : cipherflute_wiss2026_v1.2.pdf"
echo "  tracked docx : cipherflute_wiss2026_v1.2_tracked.docx"
