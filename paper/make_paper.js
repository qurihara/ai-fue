/* 暗号笛 論文ドラフト（情報処理学会論文誌 体裁の近似）を生成する。
 * 実験データはすべて仮想値（理想的結果のシミュレーション）であり、本文にその旨を明記する。
 * 使い方: node make_paper.js  →  cipherflute_ipsj_draft.docx
 */
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
  Table, TableRow, TableCell, WidthType, BorderStyle, ShadingType,
} = require("docx");

const MINCHO = { ascii: "Times New Roman", hAnsi: "Times New Roman", eastAsia: "ＭＳ 明朝" };
const GOTHIC = { ascii: "Arial", hAnsi: "Arial", eastAsia: "ＭＳ ゴシック" };

// ---- 段落ヘルパ ----
function body(text, opts = {}) {
  return new Paragraph({
    alignment: AlignmentType.JUSTIFIED,
    indent: { firstLine: opts.noindent ? 0 : 180 },
    spacing: { after: 0, line: 260, lineRule: "auto" },
    children: [new TextRun({ text, font: MINCHO, size: 18, ...opts.run })],
  });
}
function h1(num, text) {
  return new Paragraph({
    spacing: { before: 200, after: 80 },
    children: [new TextRun({ text: `${num}. ${text}`, font: GOTHIC, size: 21, bold: true })],
  });
}
function h2(num, text) {
  return new Paragraph({
    spacing: { before: 140, after: 60 },
    children: [new TextRun({ text: `${num} ${text}`, font: GOTHIC, size: 19, bold: true })],
  });
}
function caption(text) {
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 80, after: 60 },
    children: [new TextRun({ text, font: GOTHIC, size: 16, bold: true })],
  });
}
function figbox(label) {
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 120, after: 20 },
    border: { top: { style: BorderStyle.SINGLE, size: 4 }, bottom: { style: BorderStyle.SINGLE, size: 4 },
              left: { style: BorderStyle.SINGLE, size: 4 }, right: { style: BorderStyle.SINGLE, size: 4 } },
    children: [new TextRun({ text: `${label}（写真・図版挿入予定）`, font: MINCHO, size: 16, color: "888888" })],
  });
}

// ---- 表ヘルパ（列幅DXA配列＋2次元文字列。1行目はヘッダ） ----
function tbl(widths, rows) {
  const total = widths.reduce((a, b) => a + b, 0);
  return new Table({
    width: { size: total, type: WidthType.DXA },
    columnWidths: widths,
    rows: rows.map((cells, ri) => new TableRow({
      children: cells.map((c, ci) => new TableCell({
        width: { size: widths[ci], type: WidthType.DXA },
        shading: ri === 0 ? { type: ShadingType.CLEAR, fill: "EEEEEE" } : undefined,
        margins: { top: 40, bottom: 40, left: 60, right: 60 },
        children: [new Paragraph({
          children: [new TextRun({ text: c, font: ri === 0 ? GOTHIC : MINCHO, size: 15, bold: ri === 0 })],
        })],
      })),
    })),
  });
}

// ============================== タイトルブロック（1段組） ==============================
const front = [
  new Paragraph({
    alignment: AlignmentType.CENTER, spacing: { before: 200, after: 60 },
    children: [new TextRun({ text: "【執筆計画検証用ドラフト】本稿の5章の実験データはすべて仮想値（期待される理想的結果のシミュレーション）である。実測が完了するまで本稿は投稿・配布しないこと。", font: GOTHIC, size: 16, color: "CC0000", bold: true })],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER, spacing: { before: 160, after: 80 },
    children: [new TextRun({ text: "暗号笛：日用品に偽装可能な無電源音響読み出しによる", font: GOTHIC, size: 32, bold: true })],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER, spacing: { after: 120 },
    children: [new TextRun({ text: "秘密分散シェアの物理的担体", font: GOTHIC, size: 32, bold: true })],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER, spacing: { after: 160 },
    children: [new TextRun({ text: "CipherFlute: A Powerless, Acoustically Readable Physical Carrier of Secret-Sharing Shares Disguisable as Everyday Objects", font: MINCHO, size: 20, italics: true })],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER, spacing: { after: 40 },
    children: [new TextRun({ text: "栗原 一貴†", font: MINCHO, size: 22 })],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER, spacing: { after: 160 },
    children: [new TextRun({ text: "†津田塾大学　Tsuda University", font: MINCHO, size: 18 })],
  }),
  new Paragraph({
    alignment: AlignmentType.JUSTIFIED, indent: { left: 720, right: 720 }, spacing: { after: 80 },
    children: [
      new TextRun({ text: "概要：", font: GOTHIC, size: 18, bold: true }),
      new TextRun({ text: "暗号資産の復元シードに代表される少量高価値の秘密情報を，電源も電子部品も持たない3Dプリント物体に埋め込み，吹いて読み出す物理的バックアップ担体「暗号笛」を提案する．笛列の各管長を較正式にもとづき半音間隔の周波数スロットへ割り当てることで，1本あたり約3.6ビット，17本コーム1個あたり実効46.6ビットを符号化し，複数個体でShamir秘密分散のシェアを運ぶ．秘匿は音響層に一切負わせず（音響層の秘匿寄与は0ビット），閾値未満のシェア集合が情報理論的に無価値であることのみに依拠する．提案担体の特長は，(1)名刺や置物など日用品への機能的偽装により所在の探索コストを引き上げられること，(2)正当な利用者はスマートフォンと息だけで復元でき，読み出しに複雑な機器を要しないことである．基準笛との相対音程で復号する自己校正符号により温度変動を相殺し，仮想データによる評価計画では，未訓練被験者による128ビットシードの復元成功と，同時発音時の分離限界にもとづく符号設計則の確立を見込む．", font: MINCHO, size: 18 }),
    ],
  }),
  new Paragraph({
    alignment: AlignmentType.JUSTIFIED, indent: { left: 720, right: 720 }, spacing: { after: 200 },
    children: [
      new TextRun({ text: "キーワード：", font: GOTHIC, size: 18, bold: true }),
      new TextRun({ text: "デジタルファブリケーション，音響タグ，秘密分散，鍵管理，ステガノグラフィ，楽器", font: MINCHO, size: 18 }),
    ],
  }),
];

// ============================== 本文（2段組） ==============================
const main = [];

// ---- 1. はじめに ----
main.push(h1(1, "はじめに"));
main.push(body("暗号資産のウォレットや電子署名基盤の普及に伴い，すべての認証手段を失った際の最後の砦となる復元用秘密（リカバリーシード）を，どのような物理形態で保管するかという問題が現実の課題となっている．実務では復元シードを金属板に刻印する製品群が定着しており，耐火性・耐水性において優れた解である[15]．しかしこれらの担体には共通の弱点がある．それ自体が「秘密の保管物」であることが一目で分かるため，攻撃者に発見された場合に窃取の標的となることを避けられない点である．"));
main.push(body("本研究では，3Dプリントした笛の列（コーム）に秘密分散のシェアを符号化し，吹いて生じる音をスマートフォンのマイクで解析して読み出す物理的担体「暗号笛」を提案する．暗号笛は電源も電子部品も持たず，家庭用の熱溶解積層方式（FDM）プリンタで利用者自身が製造できる．そして笛列は名刺や置物といった日用品の形状へ機能ごと融合できるため，保管物の存在そのものを日常の風景に紛れさせることができる．"));
main.push(body("重要なのは，本研究が音響層に暗号学的な秘匿を一切負わせない点である．物体の所在を特定した攻撃者は，幾何計測や透過撮影により無音で内容を読み取れるし，物体を複製することもできる．本研究はこれを設計上の前提として甘受し，秘密の保護はShamirの秘密分散[18]の閾値性（閾値未満のシェア集合は情報理論的に秘密について何も漏らさない）のみに依拠する．暗号笛が提供する価値は秘匿の強度ではなく，(1)日用品への偽装による所在の探索コストの引き上げと，(2)正当な利用者が複雑な機器なしに，体一つとスマートフォンだけで復元を実行できる読み出し障壁の低さである．"));
main.push(body("本研究の貢献は次の4点である．第一に，従来は識別ID（数ビット級）の担体であった無電源音響タグを，鍵素材シェア（100ビット超級）を運ぶデータ担体へ再定義し，そのための容量工学（較正式にもとづくピッチスロット符号，誤り訂正，容量会計）を確立する．第二に，基準笛との相対音程で復号する自己校正符号により，温度・吹圧の系統変動を相殺する設計を示す．第三に，秘匿を負う層と運搬する層を明確に分離した誠実な脅威モデルを提示し，音響層の秘匿寄与が0ビットであることを会計として明記する．第四に，実128ビットのテストシードを分散・印刷・復元する端到端の評価計画を示す．"));

// ---- 2. 関連研究 ----
main.push(h1(2, "関連研究"));
main.push(h2("2.1", "ファブリケーション物への情報埋め込み"));
main.push(body("物体の内部や造形の副産物に情報を埋め込む研究は多数ある．InfraStructs[4]は内部の空隙パターンをテラヘルツ撮像で読み，AirCode[3]は表面直下の空気ポケットを計算撮像で読む．LayerCode[5]は積層をバーコードとして通常カメラで読み，G-ID[6]はスライサ設定の副産物模様で個体を識別する（約14ビット相当）．StructCode[11]はレーザーカットの継ぎ目寸法の変調に，Seedmarkers[10]は輪郭に溶け込む視覚マーカーに情報を載せる．これらはいずれも読み出しが光学的・受動的であり（撮影や走査で所有者の関与なく読める），搬送量は識別子級で，秘密情報を守る脅威モデルを持たない．"));
main.push(h2("2.2", "音響・共鳴による無電源読み出し"));
main.push(body("音響で物体を読む系譜では，Acoustic Barcodes[7]が表面のノッチ列をこすった音からIDを復号し，Lamello[8]はくし歯の長さと固有振動数の対応で入力位置を検出した．Acoustruments[9]はスマートフォンの超音波を3Dプリント管で変調して操作を認識する．Acoustic Voxels[2]は空洞群の音響応答を計算設計し，置物に音響署名を埋め込む音響タグまで実証した．そして機構の面で本研究に最も近いBlowhole[1]は，3Dプリント物の内部空洞に吹き込んで生じる共鳴音でタグを識別する．ただしBlowholeは1タグ1トリガの識別が目的であり，多ビットのペイロード符号化，較正式による音高の狙い撃ち調律，秘密分散との統合のいずれも扱っていない．本研究はこれらの機構的蓄積の上に，応用の再定義と容量工学を積む（表1）．"));
main.push(caption("表1　先行研究との比較"));
main.push(tbl([1250, 950, 800, 700, 900], [
  ["研究", "読出装置", "励振", "容量級", "脅威モデル"],
  ["InfraStructs[4]", "THz撮像", "（受動）", "ID級", "なし"],
  ["AirCode[3]", "投影+カメラ", "（受動）", "ID級", "なし"],
  ["LayerCode[5]", "カメラ", "（受動）", "数十bit", "なし"],
  ["G-ID[6]", "スマホカメラ", "（受動）", "約14bit", "なし"],
  ["Acoustic Barcodes[7]", "接触マイク", "スワイプ", "数十bit", "なし"],
  ["Lamello[8]", "接触マイク", "打撃", "入力検出", "なし"],
  ["Acoustic Voxels[2]", "マイク", "外部音源", "ID級", "なし"],
  ["Blowhole[1]", "マイク", "呼気", "ID級", "なし"],
  ["本研究", "スマホマイク", "呼気", "46.6bit/個", "あり"],
]));
main.push(h2("2.3", "鍵バックアップの実務と研究"));
main.push(body("金属シードプレート製品群[15]は耐災害性に全振りした担体であり，偽装性と機械可読性を持たない．Casascius物理ビットコイン[14]は鍵の封入とホログラム破壊による読み出しの一回性を製品化したが，製造者が鍵を知り得る構造だった．SLIP-39[12]とSSKR[13]はShamirシェアの符号化と運用の業界標準であり，本研究はこれらの「シェアの新しい物理担体」として自然に接続する．物理封印の脆弱性を体系評価したJohnstonの研究[16]は，物理層に秘匿を負わせないという本研究の撤退線を裏付ける．鍵管理のユーザビリティを定式化したEskandariらの枠組み[17]に対して，本研究は「自己製造可能・無電源機械可読・偽装可能」という未充足の組み合わせを埋める位置にある．"));

// ---- 3. 設計 ----
main.push(h1(3, "暗号笛の設計"));
main.push(h2("3.1", "半割笛と較正式"));
main.push(body("発音体には，円筒リコーダーを管軸方向に半割りしたD字断面の小型笛（厚さ4 mm，幅7 mm級）を用いる．FDMでサポート材なしに平置き印刷でき，複数本を密着させて一体の板（コーム）に融合できる．管長L [mm]と基本周波数f [Hz]の関係は閉管モデルにもとづく較正式 f = A/(L+e) で表され，実測フィットによりA = 89086，e = −10.9，残差はRMS 16セントであった．安定して発音するクリーン音域はF6（約1397 Hz，L = 74.7 mm）からE7（約2637 Hz，L = 44.7 mm）までの約1オクターブである．"));
main.push(figbox("図1　暗号笛の概要（コーム・読み出しの流れ）"));
main.push(caption("図1　暗号笛の構成と読み出しの流れ"));
main.push(h2("3.2", "ピッチスロット符号"));
main.push(body("クリーン音域を半音間隔の12スロットに分割すると，1本の笛は12値シンボル（log2 12 ≈ 3.58ビット）を運ぶ．較正式の残差（16セント）はスロット幅（100セント）に対して十分小さい．笛を1本ずつ順に吹く逐次読みが基本であり，複数本を同時に吹く同時読みは容量を増やさないが読み出し時間を短縮する（5.1節）．名刺型（91×55 mm）には8本，置物型のコームには17本を搭載できる．"));
main.push(h2("3.3", "基準笛による相対復号（自己校正）"));
main.push(body("管楽器の音高は音速に比例するため，気温が10 ℃変わると全笛の周波数が約1.7%（約29セント）同じ向きにずれる．絶対周波数で復号するとこの系統シフトが誤読を生む．そこで各コームに音高既知の基準笛を1本含め，データ笛の値を基準笛との周波数比で復号する．温度・平均吹圧の変動は全笛に等比で乗るため，比を取ることで相殺される．これは通信におけるパイロット信号と同じ原理であり，コーム自体が温度計を内蔵した自己校正符号となる．"));
main.push(h2("3.4", "誤り訂正と容量会計"));
main.push(body("スロット誤読は隣接スロットへの1段ずれが支配的であり（5.3節），無発音は消失として扱える．17本コームでは基準笛1本を除く16シンボルに対しReed–Solomon符号で3シンボルの冗長を与え，データ13シンボル＝実効46.6ビット/個とする．128ビットのシェア本体に識別子とチェックサムを加えた約148ビットは，コーム4個で1シェアを構成して運ぶ（表2）．"));
main.push(caption("表2　容量会計（17本コーム，仮設計）"));
main.push(tbl([2600, 2000], [
  ["項目", "値"],
  ["スロット数（クリーン域F6–E7）", "12（半音間隔）"],
  ["1本あたり生容量", "3.58 bit"],
  ["コーム構成", "基準笛1本＋データ16本"],
  ["誤り訂正", "RS符号 冗長3シンボル"],
  ["実効容量", "46.6 bit/コーム"],
  ["1シェア（148 bit）", "コーム4個"],
  ["2-of-3分散の総物量", "コーム12個"],
]));
main.push(h2("3.5", "秘密分散との統合と自己検証"));
main.push(body("秘密（128ビットのシード）はSLIP-39[12]に準じた2-of-3のShamir分散でシェア化し，各シェアをコーム群に符号化する．秘匿はこの分散の閾値性のみが担う．復元の正しさは，秘密に対応する公開鍵をあらかじめ利用者が保持（紙への併記，物体への刻印，または公開台帳への固定）しておき，復元値との照合で自己検証する．読み出しアプリはマイク入力のFFTと複数ピーク検出からなるWebアプリであり，オフラインで動作する．仕様・テストベクタ・検証鍵を公開台帳に固定する実装選択肢はあるが，これは本研究の貢献には数えない．"));
main.push(h2("3.6", "造形と偽装"));
main.push(body("素材は不透明PETGを標準とする（透明材は内部検査には便利だが，ボアが透けて見えるため偽装の観点では不利である）．笛列は名刺の板（総厚4 mm）や置物の台座に融合し，吹き込み口と歌口の開口は縁の意匠として処理する．印刷は家庭用FDM機（本研究ではBambu Lab A1 miniおよびH2D）で完結し，発音の安定には外壁線幅0.5 mmと低速印刷が有効であることを実装知見として得ている．製造チェーンに秘密が乗るため，スライスと印刷はオフラインの自己環境で行うことを推奨する．"));
main.push(figbox("図2　名刺型試作（不透明PETG・8本）"));
main.push(caption("図2　名刺型の試作（不透明PETG，笛8本を融合）"));

// ---- 4. 脅威モデル ----
main.push(h1(4, "脅威モデル"));
main.push(body("前提として，方式は公開であり（Kerckhoffsの原則），秘密はシェアの値のみである．本章ではまず，本研究が主張しないことを明示する．第一に，「吹かなければ読めない」とは主張しない．管長は静的な幾何量であり，所在を特定した攻撃者は開口部の計測，透過撮影，CT等により無音かつ受動的に内容を読み取れる．所在特定後のこの脆弱性は設計として甘受し，防御はShamirの閾値性と地理的分散にのみ委ねる．第二に，読み出しの物理的な一回性や改ざん検知は主張しない．笛は無傷のまま何度でも読め，複製も可能であり，痕跡は残らない．一回性は「復元を実行したら全シェアを廃棄し鍵を更新する」という運用規範として定義する．第三に，音響層・物理層による暗号学的秘匿は一切主張しない（表4）．"));
main.push(body("そのうえで主張する性質は次の4点である．(1)存在の秘匿：方式を知らない非標的型の攻撃者に対し，日用品への機能的偽装は探索コストを引き上げる（5.5節で検出実験により定量化する）．方式を知る標的型の探索者には限定的である．(2)所持要素：物体側に電子部品がなく，ネットワーク・ファームウェア等の遠隔攻撃面が存在しない．また自己製造できるため，製造者が秘密を知る問題[14]を構造的に回避する．(3)正規読み出しの顕在性：正当な復元手続きは本質的に可聴であり，立会人のもとで儀式として実行できる．これは受動走査で無音読み出しされる光学タグ群[3][4]との質的な対比であり，秘匿の機構ではなく手続きの特性である．(4)読み出し障壁の低さ：正当な利用者は複雑な機器を必要とせず，体一つとスマートフォンで復元できる．"));
main.push(caption("表3　脅威モデル（攻撃者類型と防御の所在）"));
main.push(tbl([1400, 1900, 1300], [
  ["攻撃者", "可能な攻撃", "守る層"],
  ["非標的型の侵入者（方式非既知）", "目視探索", "偽装層（探索コスト増）"],
  ["標的型の探索者（方式既知）", "幾何計測・CT・透過撮影で無音読取，物体の複製", "Shamir閾値＋分散配置のみ"],
  ["復元儀式の盗聴者", "録音1回でシェア複製", "運用層（管理環境での復元＋即時鍵更新）"],
  ["遠隔攻撃者", "（物体側に攻撃面なし）", "―（本方式の最強セル）"],
  ["読出端末・アプリへの攻撃者", "復元値の窃取・改竄", "TCBとして別途保護（オフライン動作・検証可能ビルド）"],
  ["製造チェーン", "スライス時にシェア平文を取得", "オフライン自己製造"],
  ["強制（コアーション）", "所有者への強要", "守れない（明示）"],
]));
main.push(caption("表4　エントロピー会計"));
main.push(tbl([1800, 1100, 1700], [
  ["層", "量", "秘匿への寄与"],
  ["秘密本体（CSPRNG）", "128 bit", "―（保護対象）"],
  ["Shamir分散（2-of-3）", "シェア各148 bit", "128 bit（閾値未満で条件付きエントロピー128 bitを維持）"],
  ["物理担体（音響符号）", "46.6 bit/コーム", "0 bit（明示的にゼロ）"],
  ["偽装（存在秘匿）", "―", "0 bit（探索コスト増のみ・条件付き）"],
]));

// ---- 5. 実験 ----
main.push(h1(5, "実験（仮想データによる評価計画）"));
main.push(body("本章の数値はすべて仮想値であり，期待される理想的結果を示す評価計画である（実測完了後に全面差し替える）．実験は，物理層の限界確定（5.1〜5.2），符号設計の確定（5.3），システム全体の成立（5.4），セキュリティ主張の定量化（5.5〜5.6），耐久の初期評価（5.7）の順に構成する．", { noindent: false }));
main.push(h2("5.1", "同時発音の分離限界と封止整合（仮想）"));
main.push(body("音を広く散らした5本コーム（最小間隔200セント）と，半音間隔の4本コーム（99セント）を用い，複数本の吹き込み口を口にまとめてくわえて同時に発音させた．全ピークの分離維持は，間隔200セント以上では5本まで成功した（音圧の安定は3本まで）．半音間隔では2本同時の59%の試行でピークが融合（引き込み）し，分離に失敗した．したがって同時読みの最小スロット間隔は200セント，逐次読みは100セントとする設計則を得た．また各歌口を1つずつ指で塞ぐ封止整合試験では，45試行すべてで該当ピークのみが消失し，他のピークは不変であった．弱→強の吹圧ランプでは全ピークが同方向に+18±6セント移動し（共通モード），笛間の差動成分はσ = 7セントに留まった．"));
main.push(caption("表5　同時発音の分離限界（仮想データ）"));
main.push(tbl([1800, 1400, 1400], [
  ["条件", "分離成功率", "備考"],
  ["間隔200セント・5本同時", "100%（40/40）", "音圧安定は3本まで"],
  ["間隔100セント・2本同時", "41%（33/80）", "59%で引き込み融合"],
  ["逐次読み（1本ずつ）", "100%", "間隔100セントで問題なし"],
]));
main.push(h2("5.2", "温度頑健性と相対復号（仮想）"));
main.push(body("5〜35 ℃の環境で読み出しを行った．絶対周波数による復号では，10 ℃あたり約29セントの系統シフトにより35 ℃条件でスロット誤り率が12%まで悪化した．基準笛との相対復号では，全温度条件を通してスロット誤りは600スロット中0件であり，自己校正の有効性が確認された．"));
main.push(h2("5.3", "スロット誤り特性と実効容量（仮想）"));
main.push(body("被験者3名がスマートフォン3機種で各笛20回の逐次読みを行い，混同行列を取得した．スロット誤り率は0.5%（誤りはすべて隣接スロットへの1段ずれ），無発音（消失）は1.2%であった．この誤り分布に対しRS符号の冗長3シンボルで十分であり，17本コームの実効容量46.6ビット，フレーム成功率99.2%を得た．"));
main.push(h2("5.4", "端到端の復元スタディ（仮想）"));
main.push(body("実資産と無関係な128ビットのテストシードを2-of-3で分散し，1シェア分のコーム4個を未訓練の被験者12名が読み出した．初回成功は10名（83%），読み直しを含めると12名全員が復元に成功し，平均所要時間は9.6分（SD 3.1）であった．全員が公開鍵との照合により復元の正誤を自己判定できた．"));
main.push(h2("5.5", "存在秘匿の検出実験（仮想）"));
main.push(body("日用品30点（うち暗号笛入り6点，不透明PETG）を用意し，方式を知らされていない探索者20名と，方式を説明された探索者20名に，秘密の保管物を選ばせた．前者の検出性能はほぼ偶然水準（AUC 0.54）であり，後者はAUC 0.83，1点あたり平均4.2分の検査を要した．存在の秘匿は非標的型に有効であり，標的型には限定的であるという4章の主張と整合する．"));
main.push(h2("5.6", "幾何読み取りによる自己攻撃実験（仮想）"));
main.push(body("提案の誠実性の検証として，著者自身が攻撃者の立場で，不透明PETGの名刺型に対し開口部からのデプスゲージ計測と歯科用X線撮影を行い，全スロット値の無音復元に成功した．所在が特定された物体は読まれるという4章の前提の実証であり，防御がShamir閾値のみであることを確認した．"));
main.push(h2("5.7", "経年・使用劣化の初期データ（仮想）"));
main.push(body("3か月間の常温保管，200回の吹奏，および加速条件（40 ℃・湿度90%・30日）の後，ピッチドリフトは最大−11セントであり，スロット幅100セントに対して十分な余裕を保った．相対復号では誤りは生じなかった．10年スケールの耐久は本データの外挿にもとづく設計目標であり，検証値ではない．"));

// ---- 6. 議論と限界 ----
main.push(h1(6, "議論と限界"));
main.push(body("なぜ音か．第一に，読み出し装置（マイク）が全スマートフォンに普及しており，正当な利用者の読み出し障壁が事実上ゼロである．第二に，励振源が呼気であり電源を要しない．第三に，符号が周波数という速度不変量に載るため，こすり速度に依存する時間軸符号[7]より人間の操作ばらつきに頑健である．"));
main.push(body("本方式の限界は明確である．第一に，かさばる．128ビットの秘密を2-of-3で守るにはコーム12個を要し，金属プレート1枚や紙片に対して物量で劣る．本方式は容量あたりの効率ではなく，偽装性と読み出し障壁の低さを買うための担体であり，性質の異なる冗長バックアップの一つとして併用することを推奨する．第二に，複製が容易で読み取りの痕跡が残らないため，所有者は漏洩に気づけない．第三に，論文として方式を公開する以上，標的型の攻撃者に対する存在秘匿は限定的である（5.5節）．第四に，読み出しアプリと端末は信頼の起点（TCB）であり，物体側の攻撃面ゼロという性質はソフトウェア側には及ばない．第五に，樹脂の経年（特に歌口の鋭縁の劣化）は長期の未解決課題であり，長寿命が必要な場合は金属積層造形への移行が候補となる．"));
main.push(body("応用として，復元の儀式性（可聴・立会い可能）を積極的に使う複数人の鍵セレモニー，遺言・デジタル遺産の引き継ぎ，および楽器としての演奏性を伴う体験的なセキュリティ教育が考えられる．利用にあたっては，本方式を唯一のバックアップとしないことを強く注意喚起する．"));

// ---- 7. おわりに ----
main.push(h1(7, "おわりに"));
main.push(body("秘密分散シェアの無電源物理担体として，日用品に偽装可能で，スマートフォンと息だけで読み出せる3Dプリント笛列「暗号笛」を提案した．音響層の秘匿寄与を明示的に0ビットと会計し，秘密の保護をShamirの閾値性に一元化する誠実な脅威モデルのもとで，較正式にもとづくピッチスロット符号，基準笛による自己校正，誤り訂正を含む容量工学を設計した．仮想データによる評価計画では，同時発音の分離限界にもとづく符号設計則と，未訓練者による128ビットシードの端到端復元の成立を見込む．今後は本計画に沿って実測を完遂し，素材と耐久の確定（金属積層造形版を含む）へ進む．"));

// ---- 参考文献（番号なし見出し） ----
main.push(new Paragraph({
  spacing: { before: 200, after: 80 },
  children: [new TextRun({ text: "参考文献", font: GOTHIC, size: 21, bold: true })],
}));
const refs = [
  "[1] Tejada, C., Fujimoto, O., Li, Z. and Ashbrook, D.: Blowhole: Blowing-Activated Tags for Interactive 3D-Printed Models, Proc. Graphics Interface 2018, pp. 131–137 (2018).",
  "[2] Li, D., Levin, D. I. W., Matusik, W. and Zheng, C.: Acoustic Voxels: Computational Optimization of Modular Acoustic Filters, ACM Trans. Graphics, Vol. 35, No. 4, Article 88 (2016).",
  "[3] Li, D., Nair, A. S., Nayar, S. K. and Zheng, C.: AirCode: Unobtrusive Physical Tags for Digital Fabrication, Proc. ACM UIST 2017, pp. 449–460 (2017).",
  "[4] Willis, K. D. D. and Wilson, A. D.: InfraStructs: Fabricating Information Inside Physical Objects for Imaging in the Terahertz Region, ACM Trans. Graphics, Vol. 32, No. 4, Article 138 (2013).",
  "[5] Maia, H. T., Li, D., Yang, Y. and Zheng, C.: LayerCode: Optical Barcodes for 3D Printed Shapes, ACM Trans. Graphics, Vol. 38, No. 4, Article 112 (2019).",
  "[6] Dogan, M. D., Faruqi, F., Churchill, A. D., Friedman, K., Cheng, L., Subramanian, S. and Mueller, S.: G-ID: Identifying 3D Prints Using Slicing Parameters, Proc. ACM CHI 2020 (2020).",
  "[7] Harrison, C., Xiao, R. and Hudson, S. E.: Acoustic Barcodes: Passive, Durable and Inexpensive Notched Identification Tags, Proc. ACM UIST 2012, pp. 563–568 (2012).",
  "[8] Savage, V., Head, A., Hartmann, B., Goldman, D. B., Mysore, G. and Li, W.: Lamello: Passive Acoustic Sensing for Tangible Input Components, Proc. ACM CHI 2015, pp. 1277–1280 (2015).",
  "[9] Laput, G., Brockmeyer, E., Hudson, S. E. and Harrison, C.: Acoustruments: Passive, Acoustically-Driven, Interactive Controls for Handheld Devices, Proc. ACM CHI 2015, pp. 2161–2170 (2015).",
  "[10] Getschmann, C. and Echtler, F.: Seedmarkers: Embeddable Markers for Physical Objects, Proc. ACM TEI 2021 (2021).",
  "[11] Dogan, M. D., Chan, V., Qi, R., Tang, G., Roumen, T. and Mueller, S.: StructCode: Leveraging Fabrication Artifacts to Store Data in Laser-Cut Objects, Proc. ACM SCF 2023 (2023).",
  "[12] SatoshiLabs: SLIP-0039: Shamir's Secret-Sharing for Mnemonic Codes (2017). https://github.com/satoshilabs/slips/blob/master/slip-0039.md",
  "[13] Blockchain Commons: SSKR: Sharded Secret Key Reconstruction. https://developer.blockchaincommons.com/sskr/",
  "[14] Bitcoin Wiki: Casascius physical bitcoins. https://en.bitcoin.it/wiki/Casascius_physical_bitcoins",
  "[15] Lopp, J.: Metal Bitcoin Seed Storage Reviews. https://jlopp.github.io/metal-bitcoin-storage-reviews/",
  "[16] Johnston, R. G.: Tamper-Indicating Seals: Practices, Problems, and Standards, Los Alamos National Laboratory Report (2003).",
  "[17] Eskandari, S., Barrera, D., Stobert, E. and Clark, J.: A First Look at the Usability of Bitcoin Key Management, Proc. NDSS Workshop on Usable Security (USEC 2015) (2015).",
  "[18] Shamir, A.: How to Share a Secret, Communications of the ACM, Vol. 22, No. 11, pp. 612–613 (1979).",
];
for (const r of refs) {
  main.push(new Paragraph({
    alignment: AlignmentType.JUSTIFIED,
    indent: { left: 240, hanging: 240 },
    spacing: { after: 20 },
    children: [new TextRun({ text: r, font: MINCHO, size: 16 })],
  }));
}

// ============================== 文書 ==============================
const MARGIN = { top: 1418, bottom: 1418, left: 1134, right: 1134 };
const doc = new Document({
  styles: { default: { document: { run: { font: MINCHO, size: 18 } } } },
  sections: [
    { properties: { page: { margin: MARGIN } }, children: front },
    { properties: { page: { margin: MARGIN }, column: { count: 2, space: 425 } }, children: main },
  ],
});

Packer.toBuffer(doc).then((buf) => {
  const out = path.join(__dirname, "cipherflute_ipsj_draft.docx");
  fs.writeFileSync(out, buf);
  console.log("saved:", out, buf.length, "bytes");
});
