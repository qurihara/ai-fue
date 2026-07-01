# ai-fue — AI笛作り (compact scale-flute generator)

3Dプリント可能な「音階笛」をプログラムで生成するツールキット。
[/kuri-lab/AI笛作り] の再始動プロジェクト。母体研究:
[2024夏→秋→2025夏、栗原の楽器作り研究] / https://protopedia.net/prototype/6821

## しくみ

1本の笛 = **発音ヘッド**（`recorderhead.stl`、経験的にF#チューニング済み）
＋ **ボア円柱**（高さ = チューニング表の `length_inside`）。
両者を z=0 に立て x/y 中央寄せし、メッシュを**そのまま結合**する。

> boolean union は使わない。BambuStudio 等のスライサがスライス時に重なりを
> union するため堅牢（2025年に FreeCAD の boolean が繰り返し壊れた反省）。
> 各プリミティブは個別に water-tight。

`recorderhead.stl` が `assets/` に無い間は、パイプライン検証用の
**プレースホルダヘッド**（音響的に無効・要差し替え）で動く。

## チューニング表 `data/tuning_fsharp.csv`

F#5..F#6 の13半音。列: `note, length_outside, length_inside, filename, note_in_c`。
合計100mm（`length_outside + length_inside = 100`）。`length_inside` が印刷する円柱高。

## ToneDecoder 互換

`fue/notes.py` が音階↔MIDI↔hex を一元管理（auth.html とバイト互換）。
「パスワード」= MIDIノート列のhex表記。例 `5558564F` = MIDI 85,88,86,79 = C#6 E6 D6 G5。
https://github.com/qurihara/ToneDecoder

## 使い方

```bash
# パスワード(hex)から笛を生成（リボルバー配置）
python3 fue/build.py --pass-hex 5558564F --style ring

# 音階列から（1UPキノコ）
python3 fue/build.py --notes "C6 G#5 A#5 C6 A#5 C6" --style ring

# パンフルート列
python3 fue/build.py --notes "F#5 G5 A5 B5" --style row

# 別の本体STLを使う（既定は assets/body_v6.stl）
python3 fue/build.py --pass-hex 5558564F --body assets/body_v6.stl
```

出力は `out/` に STL。`--style ring` は回して吹く用の円環、`--style row` はパンフルート列。
F#5..F#6 の外の音は自動で演奏可能オクターブに折り返す。

STLを保存すると同時に、A1 miniでそのまま印刷できる 3mf（`out/<名前>_a1mini.3mf`）も自動で書き出す（`--no-3mf` で抑止）。
既存のSTLから単体で作るときは次のようにする。

```bash
python3 fue/make_3mf.py out/flute_ring_5558564F.stl
```

### 3mf の作り方（導電性ゲームコントローラの方式を踏襲）

Bambu Studio が実際に生成したA1miniの動作実績設定を骨組みとして持ち、形状とモデル設定だけを
差し替える。印刷設定（`templates/a1mini_project_settings.config`）は単一フィラメント版に固定してあり、
「mixed filament is not supported」で弾かれないようにしている。ベッド180×180の中央へ自動配置する。
BambuStudioのCLIでスライスが通り（return code 0）、G-codeまで生成できることを確認済み。

## 状態 / TODO

- [x] 音階↔MIDI↔hex マッピング（ToneDecoder互換・自己検証済み）
- [x] チューニング表復元
- [x] straight-bore 笛生成 + row/ring レイアウト + 台座（numpy-stl, water-tight検証）
- [x] 実機の笛本体 v6 を組み込み（本体＋内挿する棒＝length_inside）
- [x] A1 mini 印刷用 3mf の自動生成（CLIスライス通過を確認）
- [ ] 実機チューニング再検証（v6は再設計版のため旧F#表の再測定が必要）
- [ ] コンパクト化: ボア折返し（U字/蛇行）で全長短縮 ← 次の主眼
- [ ] ② リボルバー/ジェノバ回転機構、③ 3Dモデルへの秘密音階埋め込み
