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
python3 fue/make_3mf.py out/flute_ring_5558564F.stl                 # A1 mini（既定）
python3 fue/make_3mf.py out/compact_calibration_comb.stl --printer h2d   # H2D
```

### 3mf の作り方（導電性ゲームコントローラの方式を踏襲）

Bambu Studio が実際に生成した動作実績のある3mfを骨組みとして持ち、形状とモデル設定だけを差し替える。

- **A1 mini**: 骨組みはコントローラ用3mf。印刷設定（`templates/a1mini_project_settings.config`）は
  単一フィラメント版に固定してあり、「mixed filament is not supported」で弾かれないようにしている。
  ベッド180×180の中央へ自動配置。BambuStudioのCLIでスライスが通り（return code 0）、G-codeまで生成できることを確認済み。
- **H2D**: 骨組みは栗原さんの印刷実績のあるH2D 3mf（`templates/h2d_skeleton.3mf`）。ベッド350×320の中央へ配置。
  H2Dはデュアル押出機のため、フィラメントの最終割り当ては Bambu Studio 側で調整する前提
  （MCP/CLIでのH2D自動スライスは現状通らないため、3mfの整形性のみ検証）。

### 音程測定・較正Webアプリ

`docs/index.html`（GitHub Pagesで公開）。印刷した笛を吹くと周波数と音名を測る。較正コームの各音を測って、
結果をコピーしてClaudeへ貼り付けると、管長と音程の対応表を作れる。音程検出は pitchy を使用（ToneDecoderと同系統）。

## 状態 / TODO

- [x] 音階↔MIDI↔hex マッピング（ToneDecoder互換・自己検証済み）
- [x] チューニング表復元
- [x] straight-bore 笛生成 + row/ring レイアウト + 台座（numpy-stl, water-tight検証）
- [x] 実機の笛本体 v6 を組み込み（本体＋内挿する棒＝length_inside）
- [x] A1 mini 印刷用 3mf の自動生成（CLIスライス通過を確認）
- [ ] 実機チューニング再検証（v6は再設計版のため旧F#表の再測定が必要）
- [x] **コンパクト化（目標①）**: 実績ヘッド＋必要長の閉管。棒も死んだ材料も無し。全長=26.5mm＋管長。管長60mmで全長86.5mm（従来169mmの約半分）
- [x] **管長↔音程の実測較正**（H2Dで4本測定、`f = 91891.5/(L+14.23)`、RMS 0.28mm。片閉じ管の1/4波長則）
- [x] **音階列→音程の合ったコンパクト笛**（`fue/compact.py --notes` / `--pass-hex`）
- [x] **ボア折返しで背を縮小**（`fue/fold.py`、trimesh+manifold3d）。C6は直管112mm→3折り54mm。サポート無しで印刷（要実機確認）
- [ ] 折り補正・細ボア・小ヘッドの実測較正（テストパネル `panel_fold_c6` / `panel_high_octave`）
- [x] **全体を直方体に統一（箱モジュール・A案）**（`fue/box.py`）。3モデル（折りなし/折り1/折り2）とも共通16mmフットプリントの直方体に。実績の円筒ヘッドを角shellで内包し窓面だけ開口＝音は不変で既存較正を流用
- [ ] **角ネイティブ フィッポルヘッド（B案）の実機ボイシング**（`fue/box.py --fipple-comb`）。円筒ヘッド不使用の完全一体押し出し。要 較正やり直し
- [ ] 断面の涙滴/菱形化
- [ ] ② リボルバー/ジェノバ回転機構、③ 3Dモデルへの秘密音階埋め込み

### コンパクト笛（目標①）

```bash
# 較正コーム（管長を変えた笛を一列に。1回印刷して各笛の音程を測り、管長↔音程の表を作る）
python3 fue/compact.py                      # 既定 管長 40,70,100,130mm の4本
python3 fue/compact.py --comb 40,80,120     # 本数を減らして時短

# 単一のコンパクト笛（管長を直接指定）
python3 fue/compact.py --single 60          # 全長 86.5mm

# 音階列から、音程の合ったコンパクト笛を生成（較正済み）
python3 fue/compact.py --notes "C6 D6 E6 F6 G6 A6 B6 C7" --style row   # ドレミの音階笛
python3 fue/compact.py --pass-hex 5558564F --style ring                # パスワードから
python3 fue/compact.py --notes "C6 D6 E6" --printer h2d                # H2D用3mf
```

較正式は `f = 91891.5 / (L + 14.23)`（L=管長mm, f=周波数Hz）。2026/7/1にH2Dで管長40/70/100/130mmの
4本を印刷し実測してフィットした（RMS 0.28mm）。片閉じ管の1/4波長則そのもので、端補正は約14mm。
`fue/compact.py` の `CALIB_K` / `CALIB_DELTA` に格納。再測定で更新できる。

`assets/head_v6.stl` は v6本体の上端26.5mm（吹き口＋ウインドウェイ＋フィッポル窓）を切り出した実績ヘッド。
その下へ必要な長さの中空管と閉端キャップを足す。管長と音程の対応は端補正等で物理式では正確に出ないため、
較正コームを印刷して実測で対応表を作る想定。音程が確定すれば、音階列から直接コンパクト笛の並びを生成できる。

### 箱モジュール（目標①・全体を直方体に）`fue/box.py`

小型笛の外形を1個の直方体に統一してモジュール性を上げる（スタック／タイル／目標③の3Dモデル埋め込みに直結）。
3モデル（折りなし／折り1／折り2）とも**共通フットプリント奥行き16mm**の直方体にする。折るほど背は低く・幅が広い。
実行には `fold.py` / `plenum.py` と同じ trimesh + manifold3d が要る。

```bash
# A案（推奨）: 実績の円筒ヘッドを角shellで内包し、窓面だけ凹ませて開口＝音は不変（既存較正を流用）
python3 fue/box.py --note C6 --N 1     # 折りなし   16×16×100mm
python3 fue/box.py --note C6 --N 2     # 折り1     22×16×69mm
python3 fue/box.py --note C6 --N 3     # 折り2     32×16×57mm
python3 fue/box.py --note C6 --panel   # 3モデルを同じ音で横一列（out/box_panel_C6.stl + a1mini.3mf）

# B案（実験的）: 角ネイティブのフィッポルヘッド（円筒ヘッド不使用の完全一体押し出し）。音は変わるので要 実機ボイシング
python3 fue/box.py --fipple-comb       # flue-labiumオフセットとcutupを振ったボイシング変奏コーム
```

A案は**円筒ヘッドとボアをそのまま内包**するので音響は不変。外側16角柱の四隅は詰め物になるが少量で、
窓（歌口）の1面だけ角shellを凹ませて噴流の前を開けてある（塞ぐと鳴らない）。まずA案で確実に一体化し、
B案は「鳴るボイシング」を変奏コームで見つけてから管長較正に進む2段構え。

### 極小笛 mini-c-v2 と パンフルート（目標①・最小化の本命）`fue/mini.py`

`mini/recorder-mini-c-v2.stl`（7×7×40mmの極小閉管リコーダー・印刷&発音実績）の発音ヘッドを
z=18で切り出し、上に任意長の閉じボアを生やして音程を振る。**flat（寝かせ印刷・窓横向き・丸ボアの
面内蛇行）** が本命で、横向き丸ボアがブリッジで架かるため実質サポートフリー・背が低く安定。

**実機較正（閉端・A1 mini）:** `ENDCORR=1.9`（端補正）＋ `FLAT_FOLD_CORR=3.5mm/折`（折り補正。折り1回
ごとに実効長が縮み音程が上がる。旧compact.pyの3.3mmと一致）。C6/E6は狙い±25c以内でドンピシャ。
発音性のスイートスポットは **N=2（1折り）**。高音(G6〜C7)はヘッド固有コア(≈F7)に近づくと不安定
＝1ヘッドの綺麗な帯域は約1オクターブ。2オクターブにはヘッドのサイズ違い（ファミリー化）が要る。

**端穴の教訓:** 蛇行の折り返し(半径r=3)が端キャップ(旧2mm)を突き抜けて+x端に穴が開いた
→ `H=z_high+r+end_wall(1.2)` で解決（flat_fluteは閉端）。

```bash
python3 fue/mini.py --flat --note C6 --flat 2      # 単一flat笛（面内蛇行N本）
python3 fue/mini.py --flat-comb                    # flat測定コーム(C7/A6/F6/C6)
python3 fue/mini.py --fold-sweep C6 --Ns 1,2,3     # 音固定・折り数スイープ（折り補正/発音性の計測）
python3 fue/mini.py --pan-flute                    # 1オクターブ パンフルート（z方向スタック・一体）
```

**パンフルート `pan_flute`:** 1オクターブ(C6..C7)の管を z方向に積んだ一体ブロック（土台なし・
51×14×56mm）。`mirror_y`（段ごとにy鏡像＝窓を+y/-yへ）でハーモニカ的な配置に、`notes` の並べ替えで
カリンバ配列などに。段間が近い(1mm壁)と音響結合してフラット化・偶数倍音が出るのが課題（互い違い等で回避を検討中）。

**A1 mini 印刷（MCP）:** 定着に必須の設定（ベッド65℃ Textured PEI＋ブリム＋support critical_regions_only）
を持つ `temp/box_brim_profile.json` に、開始gcode(M620 AMSロード＋G29)を移植した `temp/box_brim_ams_profile.json`
でスライス → `bambu-swaplist-batch` skillの `make_swap.py` でswap化 → `print_3mf(ams_slots=[0])`。
反復印刷はflow/振動キャリブOFF・レベリングON（同一フィラメントで流量キャリブ毎回は無駄）。
