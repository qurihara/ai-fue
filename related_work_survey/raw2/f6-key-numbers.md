# 比較表を数字で書き直すための一次資料確認（容量と読出装置）

本稿は CipherFlute の論文にある先行研究比較表を、粗い区分（「ID級」「数十bit」「約14bit」など）から
数字に置き換えるために、対象13件の容量と読み出し装置を一次資料で確定した記録である。
前段の調査で報告された数値を1件ずつ原典の本文で確かめ、確かめられた箇所は原典の文言を引用し、
確かめられなかったものは「原典では確認できなかった」と明記した。

## 作業の方法

まず、各研究の本文PDFを著者・研究室・出版社・arXiv・機関リポジトリから取得し、
テキストを抽出して該当箇所を直接読んだ。ACM Digital Library は本文の取得を拒んだため
（Seedmarkers の全文HTMLは HTTP 403 を返した）、著者の公開版と arXiv 版で代替した。
表が画像として埋め込まれていて抽出が崩れた Seedmarkers の表3については、
該当ページを画像に変換して目視で数値を読み取った。

取得できた本文PDFは13件すべてである。すなわち対象13件のうち12件は本文で数値を確認でき、
残る1件（SoundOff）も著者本人が公開しているPDFで本文を確認できた。

## 1件ずつの検証記録

### 1. InfraStructs（SIGGRAPH 2013、Willis and Wilson）

- 前段の報告: 一次元タグで8ビット、行列型タグで27ビット、Picometrix T-Ray 4000、100×100画素で約2分、
  リードソロモン符号は将来課題。
- 検証の結果: すべて原典の本文と一致した。
- 容量: 一次元タグは説明用の例として「eight bits of binary information」を符号化すると書いてある。
  実際に造形して読み出したのは行列型タグであり、「Each of the 27 bits were successfully decoded」と
  書いてある。同じ走査で記録した全ビット状態は603個で、正しく読めたのは567個（94パーセント）である。
- 読出装置: Picometrix T-Ray 4000 というテラヘルツ時間領域分光システムを使い、
  すべて反射モードで走査している。走査速度は毎秒約100画素で、100×100画素の走査に約2分かかると
  書いてある。
- 誤り訂正: 実装していない。本文は「More advanced encoding schemes may look to utilize an error
  correction scheme such as Reed-Solomon」と将来の可能性として述べるだけである。
- 脅威モデル: 無い。7.4節の題名は「Safety and Privacy」であるが、内容はテラヘルツ波の人体への安全性と、
  衣服を透過して人体を走査する場合の倫理であって、埋め込んだ情報を狙う攻撃者の議論ではない。
- 確認先: https://www.microsoft.com/en-us/research/wp-content/uploads/2016/10/WillisSiggraph2013.pdf

### 2. AirCode（UIST 2017、Li ら）

- 前段の報告: 2センチメートル角に約106ビット、5センチメートル角に500ビット超、
  リードソロモン符号で40パーセントの冗長度。
- 検証の結果: すべて原典の本文と一致した。ただし「500ビット超」は正確には「約500ビット」である。
- 容量: 「the physical size of an AirCode tag is around 2cm×2cm, allowing the tag to accommodate
  about 106 bits」と書いてある。拡張については「a 5cm×5cm tag stores about 500 bits」と書いてあり、
  図の説明にも「500 bits are encoded in this 5cm by 5cm AirCode tag」と書いてある。
  したがって5センチメートル角は「約500ビット」であって「500ビット超」ではない。
- 誤り訂正: 実際に使っている。「In practice, we also use Reed-Solomon code to add 40% redundancy
  in the encoded bits」と書いてある。
- 読出装置: Mitsubishi PK20 という画素数800×600のデジタル光処理方式プロジェクタで市松模様を投影し、
  Point Grey Grasshopper3 という画素数2048×1536の単色カメラで撮像する。
  プロジェクタとカメラの双方の前に位相をずらした偏光板を置く。低照度で雑音が多いため、
  投影する模様1枚あたり16枚の画像を平均している。撮像には3分から4分かかると書いてある。
- 脅威モデル: 無い。本文には脅威、攻撃者、安全性、プライバシー、暗号のいずれの語も現れなかった。
- 確認先: https://www.cs.columbia.edu/cg/aircode/aircode-uist-2017-li-et-al.pdf

### 3. LayerCode（SIGGRAPH 2019、Maia ら）

- 前段の報告: 24ビット、近赤外では12ビット、誤り訂正の冗長をあえて付けていない。
- 検証の結果: すべて原典の本文と一致した。
- 容量: 「all of our virtual evaluations use a 24 bit-length base-2 encoding, leading to an entropy
  over 16 million」と書いてある。2の24乗は16,777,216であるから、この記述と整合する。
  実物についても「our real world two-color and layer-height examples also use 24 bit-length
  encodings」と書いてある。近赤外については「The near-infrared prints employ 12 bit binary encodings
  due to the printer's smaller build volume and subsequently smaller prints」と書いてある。
- 誤り訂正: あえて付けていない。「In our experiments, we choose not to add any error-correction
  redundancy to study the pure performance of our method」と書いてある。
  そのうえでリードソロモン符号を採用できるとも書いてある。
- 読出装置: 「a Canon DSLR camera with 5184×3456px」で撮影しており、
  画素数4032×3024のiPhoneのカメラでも同様の結果が得られたと書いてある。
  近赤外の変種だけは近赤外フィルタを付けやすい Point Grey Grasshopper3（画素数2048×1536）を使っている。
  外部の光源は要らないと書いてある。
- 脅威モデル: 無い。近赤外の変種を「steganography」と呼んではいるが、攻撃者を定義していない。
- 確認先: https://www.cs.columbia.edu/cg/layercode/LayerCode_Maia_et_al_2019_lowRez.pdf

### 4. G-ID（CHI 2020、Dogan ら）

- 前段の報告: カメラのみで204通り、光源併用で17,136通り。
- 検証の結果: 原典の本文と一致した。しかも原典は自分でビット換算を書いている。
- 容量: 「we can achieve a total of 204 instances if we only use the camera, or 17,136 instances
  if we use both the camera and light」と書いてある。続けて
  「these parameter spaces have a larger code capacity than a 1D barcode with 7 or 14 bits,
  respectively」と書いてある。つまり原典自身が7ビットおよび14ビットに相当すると述べている。
  2を底とする対数で計算すると204は7.67ビット、17,136は14.06ビットである。
- 誤り訂正: 符号としての誤り訂正は無い。ただし表1の脚注に「2 angles reserved for error checking」と
  あり、36通りの角度のうち2通りを誤り検査のために予約している。
  したがって誤り検出のための予約はあるが、訂正符号は無い。
- 読出装置: 市販のスマートフォンのカメラだけでよいと書いてある。
  ただし充填の変化（充填角度、充填模様、充填密度）まで読むには小さな光源が要り、
  評価では Nitecore Tini という小型灯を物体の側面に当てている。読み出しは専用の携帯端末用アプリで行う。
- 脅威モデル: 無い。
- 確認先: https://groups.csail.mit.edu/hcie/files/research-projects/G-ID/2020-CHI-GID-paper.pdf

### 5. Acoustic Barcodes（UIST 2012、Harrison ら）

- 前段の報告: 6ビットから24ビット、ガード列、0の連続の禁止、
  BCH符号やリードソロモン符号による誤り訂正の検討。
- 検証の結果: おおむね原典の本文と一致した。ただし誤り訂正の中身はもっと具体的であり、
  「BCH符号やリードソロモン符号」という要約は不正確である。実際に評価したのは
  ハミング符号、短縮BCH符号、拡張ゴレイ符号の三つで、リードソロモン符号は将来の提案として挙げただけである。
- 容量: 利用者実験で使ったのは6ビット、12ビット、24ビットの符号である
  （「The barcodes varied in bit count (6, 12, and 24 bit codes) and unit gap length
  (1.6mm and 3.2mm)」）。
- ガード列: 「Barcodes begin and end with a guard sequence consisting of three grooves separated
  by unit gaps」と書いてある。両端に3本ずつの溝を置く。
- 0の連続の禁止: 固定物理長方式について「we constrain the space of permissible bit sequences to
  exclude sequences with two consecutive 0 bits. This better assures that a "clock signal" can be
  recovered」と書いてある。すなわち隣接する記号への制約が明示的に入っている。
  この点は CipherFlute の隣接同音禁止と発想が同じであり、比較表で正直に書く価値がある。
- 誤り訂正を入れたあとの実効容量: ここが最も重要な数字である。原典は次のように書いている。
  6ビット符号で1ビットの誤りを訂正するには短縮(7,4)ハミング符号を使い、データは3ビットになる。
  12ビット符号で2ビットの誤りを訂正するには短縮(15,7)BCH符号を使い、データ4ビットと検査8ビットになる。
  24ビット符号で3ビットの誤りを訂正するには拡張ゴレイ符号を使い、
  「which yields 12 data bits and 12 check bits, offering 4096 unique acoustic barcodes」と書いてある。
  したがって実証された最大の実効容量は24ビット符号のうちデータ12ビット（4096通り）である。
  さらに将来の提案として、(63,30)BCH符号なら63ビット列でデータ30ビット、約10億通りになると書いてある。
- 精度: 誤りゼロの生の認識率は、携帯電話で87.4パーセント、指の爪で77.9パーセント、
  ホワイトボード用マーカーで66.4パーセントである。誤り訂正を入れると93.1パーセント、
  87.4パーセント、77.3パーセントになる。
- 読出装置: 安価な市販の圧電接触型マイクロホンを机や窓やホワイトボードに貼り付け、
  増幅して一般的なノートパソコンに送る。標本化周波数は96キロヘルツで、4キロヘルツの高域通過フィルタをかける。
  読み出しの動作は、指の爪、マーカー、携帯電話のいずれかで刻み目の列をなぞることである。
- 脅威モデル: 無い。
- 確認先: https://www.chrisharrison.net/projects/acousticbarcodes/AcousticBarcodes.pdf

### 6. Lamello（CHI 2015、Savage ら）

- 前段の報告: 基本周波数924ヘルツから3824ヘルツ、de Bruijn 系列による符号設計、
  2キロヘルツ以上で識別率が下がる。
- 検証の結果: すべて原典の本文と一致した。ただし「924ヘルツから3824ヘルツ」は
  評価に使った7枚の櫛歯の予測周波数の範囲であり、設計として作れる範囲は400ヘルツから4000ヘルツである
  （「fabricated tines with f0 between 400Hz (4mm × 50mm × 6mm) and 4000Hz
  (7.25mm × 6.0mm × 1.2mm)」）。
- 周波数: スライダの7枚の櫛歯の予測周波数は924、1103、1340、1662、2116、2784、3824ヘルツである。
  ダイヤルの7枚は840、1003、1218、1511、1923、2530、3478ヘルツである。
- 2キロヘルツ以上の劣化: 「precision and recall rates are much lower on a set of 7 tines with
  frequencies above 2kHz: the recognizer fails to classify higher f0, which have lower energies and
  shorter decays」と書いてある。表1の数値では、4枚のスライダで適合率93パーセント・再現率90パーセント、
  7枚のスライダで適合率49パーセント・再現率56パーセントである。ダイヤルは7枚で適合率63パーセント、
  手で弾いたDelrin製は7枚で適合率72パーセントである。
  考察でも「classification accuracy still needs improvement, and may require a new approach for
  f0 > 2kHz」と書いてある。
- de Bruijn 系列: 「by varying f0, we create de Bruijn patterns」と書いてあり、
  図3の説明に「de Bruijn sequences allow classification of fewer tine lengths, but require more
  consecutive tine recognitions to determine position and direction」と書いてある。
- 容量: 原典はビット数をまったく書いていない。この研究の目的はスライダやダイヤルの位置と方向の入力検出であり、
  データを蓄えることではない。信頼して区別できたのは4枚の櫛歯であるから、
  1回の打撃あたり2.0ビット相当と換算できる。この換算は本稿による計算であって原典の記述ではない。
- 読出装置: 接触型マイクロホンを標本化周波数16000ヘルツで使い、Python で書いた高速フーリエ変換の
  処理系で分類する。読み出しの動作は、スライダやダイヤルを動かして撥が櫛歯を弾くことである。
- 誤り訂正: 無い。
- 脅威モデル: 無い。
- 確認先: https://people.eecs.berkeley.edu/~bjoern/papers/savage-lamello-chi2015.pdf

### 7. Acoustic Voxels（SIGGRAPH 2016、Li ら）

- 前段の報告: 透過損失曲線を使った4ビット。
- 検証の結果: 原典の本文で確認できた。前段の調査では
  「抄録にはビット数が書かれていないので本文で確認するまで使わないほうがよい」と保留されていたが、
  本文には明確に書いてある。この保留は解除してよい。
- 容量: 「To encode N bits of information, we evenly sample 2N frequency values and group the
  samples pairwise」という符号化方式を述べたうえで、
  「We fabricated three objects with an identical, octopus-like surface shape, and use them to
  encode different 4-bit strings, including "0000", "1001", and "0111"」と書いてある。
  つまり実証されたのは1個あたり4ビットである。
  これとは別に、音響タグとしては3個の同形の豚の置物をインピーダンス曲線の峰の位置で区別している。
  3通りの識別は1.585ビット相当である。
- 読出装置: iPhone のアプリである。透過損失で4ビットを読むときは、iPhone のスピーカから白色雑音を鳴らし、
  同時にマイクロホンで録音して、物体の入口と出口の二つの穴にスピーカとマイクロホンを合わせる。
  インピーダンスで豚を識別するときは、手のひらで鼻を叩いた音を録って共鳴周波数を検出する。
- 誤り訂正: 無い。
- 脅威モデル: 無い。
- 確認先: https://www.cs.columbia.edu/cg/lego/acoustic-voxels-siggraph-2016-li-et-al.pdf

### 8. Blowhole（Graphics Interface 2018、Tejada ら）

- 前段の報告: 管長2.5ミリメートルで球径8から28ミリメートルの6種類なら利用者非依存で98パーセント、
  最大9個のタグ。
- 検証の結果: すべて原典の本文と一致した。
  なお論文番号に注意が必要である。この論文は Graphics Interface 2018 の18番であり、
  16番は Fitts の法則に関する別の論文である。誤って16番を引かないようにしたい。
- 容量: 「The best performance/versatility tradeoff occurs at Lt of 2.5 mm and six spheres from
  8-28 mm, which yields an overall 98% accuracy. Adding a 32 mm sphere decreases accuracy to 90%」と
  書いてある。考察では「with up to six cavities, the system achieves a high user-independent
  performance of 98%」と書いてある。結論では「enables high performance for up to nine different
  blowholes」と書いてあり、序論では「Blowhole achieves high accuracy with up to nine tags per
  object」と書いてある。
  したがって、利用者非依存で98パーセントとなる区別できる穴の数は6個で、これは2.585ビット相当である。
  上限として述べている9個は3.170ビット相当である。このビット換算は本稿による計算である。
- 周波数の範囲: 「a frequency space ranging from 500 Hz to 5900 Hz」と書いてある。
- 読出装置: ノートパソコンの内蔵マイクロホンを標本化周波数44,100ヘルツで使い、
  Welch の方法で基本周波数を求める。分類は Python の scikit-learn で行う。
  LG-R という Android の腕時計でも試したと書いてある。
  読み出しの動作は、穴に軽く息を吹き込むことである。
- 誤り訂正: 無い。
- 脅威モデル: 無い。
- 確認先: http://graphicsinterface.org/wp-content/uploads/gi2018-18.pdf

### 9. InfraredTags（CHI 2022、Dogan ら）

- 前段の報告: 21×21のQRコードで数字25文字。
- 検証の結果: 原典の本文と一致した。
- 容量: 「21x21 QR codes (can store up to 25 numeric characters)」と書いてある。
  10進数25桁を情報量に換算すると83.05ビットである。この換算は本稿による計算である。
  併せて4×4の ArUco マーカーも埋め込んでいる。
- 読み出しの速さ: 「it takes 6ms to decode a 4x4 ArUco marker and 14ms to decode a 21x21 QR code
  from a single original frame」と書いてある。
- 読出装置: 近赤外カメラである。安価な選択肢として Raspberry Pi NoIR カメラモジュール（20ドル）を挙げ、
  これと Raspberry Pi Zero と電池を、柔軟フィラメントで造形した携帯電話用ケースに収めた
  自作の撮像モジュールを作っている。このモジュールの重さは132グラムである。
  必要な近赤外の照度は、二材料印刷で0.2ルクス、単材料印刷で1.1ルクスであり、
  最大250センチメートルまで検出できると抄録に書いてある。
- 誤り訂正: QRコードそのものが持つ誤り訂正に依拠しており、独自の追加は無い。
- 脅威モデル: 無い。
- 確認先: https://arxiv.org/pdf/2202.06165

### 10. AnisoTag（CHI 2023、Ma ら）

- 前段の報告: クレジットカードと同寸の面に51ビット、画像処理併用で160ビット。
- 検証の結果: すべて原典の本文と一致した。
- 容量: 「an easily accessible size setting: 53.98 × 85.6, the same as a credit card」の面に
  「we divide 17 encoding regions along the horizontal axis」「could encode 3 bits」とし、
  「using the AnisoTag G-code tool with a bitstream of 17 × 3 = 51 bits」と書いてある。
  表1の説明には「its capacity can be extended to 160 bits if it is extracted by an RGB camera and
  image processing operations」と書いてある。
  なお領域の数を16から21まで変えた評価では48ビットから63ビットの範囲になると書いてある。
- 同寸比較: 原典は同じ大きさのタグで比べて
  「AnisoTag encodes 51 bits, LayerCode encodes 25 bits, and acoustic barcode encodes 40 bits」と
  書いている。この一文は CipherFlute のカード実装を比較するときにそのまま引ける。
- 読出装置: 自作の検出装置である。Class IIIA の市販レーザーポインタ（3ドル）を光源とし、
  背面板に16個の光導電素子（フォトレジスタ）を半径1.5の円周上に並べ、
  マイクロコントローラ STM32F103（7ドル）で読む。三脚でレーザー光源を固定し、入射角は70度である。
  読み出しの動作は、レーザーの照射域をタグが横切るように滑らせることである。
- 誤り訂正: 記述が無い。
- 脅威モデル: 無い。
- 確認先: https://arxiv.org/pdf/2301.10599

### 11. SoundOff（IMWUT 2025、Fu ら）

- 前段の報告: 区別しやすい設計を数千通り生成できる。1個あたり何ビットかを確定したい。
- 検証の結果: 「数千通り」は抄録の表現であって、実装で生成した数は1277通りである。
  1個あたりのビット数は原典にまったく書かれていない。以下が確定できた数字である。
- 設計候補の数: 「1277 in total for 1, 2, 3, 4, and 6 sectors」と図5に書いてある。
  本文でも「we first filtered the 1277 generated geometries down to those exhibiting at least six
  eigenfrequencies within the ultrasonic range」「15 of the most distinct tags selected from the
  1277 candidates」と書いてある。
  抄録の「systematically generate thousands of designs」という表現に対応する具体的な数は
  本文には現れず、1277通りが実装で生成した数である。
  なお展望の節に「generate and evaluate thousands of shapes」という将来の設計ツールの話がある。
- 実証された区別可能な数: 15個である。1277通りから対の間のハミング距離を計算して貪欲法で選んだ15個を
  造形し、0.5メートルの固定条件で分類精度93.75パーセントを得ている。
  実環境では11個を6か所（事務室、居間、運動室、実験室、浴室、寝室）に設置し、
  精度は約87パーセントから98パーセント、平均92.1パーセントである。
  複数の利用者では平均86.2パーセントである。マイクロホンがタグから1メートル以内なら98パーセントを超える。
  「For this study, we limited the number of selected tags to 15 for practical reasons, but the
  number could be readily increased if needed」と書いてある。
- 1個あたりのビット数: 原典は書いていない。識別子として使うと考えれば、
  実証された15個は3.907ビット相当である。この換算は本稿による計算である。
  1277通りを10.319ビットと換算するのは誤りである。1277通りは互いに区別できる集合ではなく、
  そこから区別しやすいものを選び出した元の候補集合だからである。
- 読出装置: Ultramic384K BLE という超音波マイクロホン（16ビット、標本化周波数384キロヘルツ、
  内部は Knowles FG23629）を手首に巻き、Raspberry Pi Zero で処理する。
  読み出しの動作は、扉、便座、引き出し、蛇口、窓などを普通に動かすことであり、
  そのときタグが受動的に超音波を発する。
- 誤り訂正: 無い。機械学習を使わず、周波数の照合による規則で分類している。
  「If at least 40% of the labeled frequencies are matched & the penalty score is less than 0.2,
  the signal is classified as that tag」という規則である。
- 脅威モデル: 無い。プライバシーは8か所で言及されるが、
  それはカメラや可聴音の録音を使わないという設計目標としてのプライバシーであり、
  埋め込んだ情報を狙う攻撃者の議論ではない。
- 確認先: 著者 Vivian Shen の公開頁からたどれる本文PDF
  https://drive.google.com/file/d/1StyNwdbcGeV810e1TdhXK2Wv9YkMV2a8/view （本文全体を読んだ）。
  抄録は https://par.nsf.gov/biblio/10670927-soundoff-low-cost-passive-ultrasound-tags-non-invasive-non-intrusive-smart-home-sensing
  にある（このページには本文が2026年12月2日に公開予定と書いてある）。
  書誌は https://dblp.org/search/publ/api?q=SoundOff+passive+ultrasound+tags&format=json で確認し、
  Proc. ACM Interact. Mob. Wearable Ubiquitous Technol. 第9巻第4号 論文番号174、
  全32ページ、DOI は 10.1145/3770666 である。

### 12. StructCode（SCF 2023、Dogan ら）

- 前段の報告: 指型継手で12文字、リビングヒンジで21文字。
- 検証の結果: 原典の本文と一致した。
- 符号化の単位: 3進の符号を使い、「Four elements, i.e., four bits, represent one character.
  The different combinations of element widths that make up the four bits can generate up to 81
  different variations, which allows to embed 81 different character types, including 62
  alphanumeric characters and 18 special characters」と書いてある。
  1文字あたり81通りであるから6.34ビットである。
- 容量: 指型継手については、Instructables の作例で四辺すべてに継手を持つ板は平均50.3個の指と隙間を
  持つことを調べ、「this allows us to embed 7 characters with a base 2 scheme, or 12 characters with
  a base 3 scheme」と書いてある。
  リビングヒンジについては平均85.7本の切れ目から
  「This allows for a data capacity of 21 characters using our base 3 scheme」と書いてある。
  検出の評価では、15×10センチメートルの板（26個の指）で14文字、
  20×20センチメートルの板（60個の指）で31文字、
  5×3.7センチメートルのヒンジ（72本の切れ目）で9文字、
  10×7.4センチメートルのヒンジ（193本の切れ目）で36文字と書いてある。
- ビット換算: 12文字は76.08ビット、21文字は133.14ビット、36文字は228.23ビットである。
  この換算は本稿による計算であり、原典はビット数を書いていない。
  なお原典が「bits」と呼ぶのは3進の1桁であって2進の1桁ではないことに注意したい。
  原典自身が脚注で「we use the term bits in the paper although it is normally used for the binary
  system」と断っている。
- 読出装置: 一般的なカラーカメラだけでよい。評価では Pixel 2 の1220万画素のカメラで撮影し、
  画素数2048×1536に縮小して処理している。3枚の板が画面に入るように45センチメートル離して構えている。
  読み出しの動作は、継手やヒンジが写るように携帯電話で写真を撮ることである。
- 誤り訂正: 実装していない。「Error correction codes such as Reed-Solomon or Hamming code could be
  added to StructCodes to further increase detection robustness」と将来の可能性として述べている。
- 脅威モデル: 無い。ただし「For the most sensitive tags, the mapping of code to label can be
  encrypted and available to that user only」という一文があり、
  符号から意味への対応表を暗号化するという発想には触れている。
  これは CipherFlute の goto_enc に近い発想であるから、比較表の脅威モデル欄では
  「無し（ただし対応表の暗号化に一言だけ言及）」と正確に書くのがよい。
- 確認先: http://groups.csail.mit.edu/hcie/files/research-projects/structcode/2023-SCF-StructCode-paper.pdf
  （書誌は https://dblp.org/search/publ/api?q=StructCode+laser-cut&format=json で確認し、
  SCF 2023、DOI 10.1145/3623263.3623353 である）

### 13. Seedmarkers（TEI 2021、Getschmann and Echtler）

- 前段の報告: 重み付きボロノイ図による位相的な最適化（容量は未確認だった）。
- 検証の結果: 容量を表3で確定できた。ACM Digital Library の全文HTMLは HTTP 403 を返したため、
  著者 Florian Echtler の公開版PDFを取得し、表が画像で埋め込まれていたのでページを画像に変換して
  目視で読み取った。
- 容量: 表3「Number of unique topological trees (left-heavy-depth-sequences) by maximum width and
  depth」の値は次のとおりである。
  深さ2で幅2が3通り、深さ2で幅3が4通り、深さ2で幅4が5通り、
  深さ3で幅2が10通り、深さ3で幅3が35通り、深さ3で幅4が126通り、
  深さ4で幅2が66通り、深さ4で幅3が8436通り、深さ4で幅4が11,358,880通りである。
  最後の場合だけ6自由度の姿勢推定に使える部分集合の数が書かれており、58,905通りである。
  本文にも「given trees with a maximum depth of 4 and a width of up to 4 children per node,
  the resulting 58905 distinct markers with the ability to estimate 6-DoF pose should be sufficient
  for many applications」と書いてある。
  ビットに換算すると、11,358,880通りは23.437ビット、58,905通りは15.846ビットである。
  この換算は本稿による計算である。
- 誤り訂正: 明確に無い。著者自身が欠点として
  「One is the lack of error correction, thus Seedmarkers can not deal with occlusion and are less
  robust than other marker designs」と書いている。
- 誤検出: 41,602枚の画像で試して8.36パーセントの画像に少なくとも1件の誤検出があり、
  深さ3以上の葉を1つ以上含む図を使えば1枚あたり0.5パーセントまで下げられると書いてある。
- 読出装置: 一般的なカメラである。ReacTIVision と互換であり、専用のプロジェクタや特殊なカメラは
  要らないと書いてある。読み出しの動作は、標識が写るように撮像することである。
- 脅威モデル: 無い。
- 確認先: https://floe.butterbrot.org/matrix/publications/getschmann2021seedmarkers.pdf

## 確定できた数値の一覧表

ビット数のうち、原典に書かれている数字はそのまま示し、
原典が個数だけを書いていて本稿で2を底とする対数によって換算したものには「換算」と付した。

| 研究の名前 | 発表年 | 読み出しに要する装置 | 鳴らし方または読み出しの動作 | 実証された容量（ビット） | 誤り訂正の有無と種類 | 脅威モデルの有無 | 確認先のURL |
| --- | --- | --- | --- | --- | --- | --- | --- |
| InfraStructs | 2013 | テラヘルツ時間領域分光システム Picometrix T-Ray 4000（100×100画素で約2分） | 物体を走査台に置いて反射モードで走査する | 27ビット（行列型タグ、全27ビットの復号に成功）。一次元タグは説明用の例として8ビット | 無し。リードソロモン符号は将来課題として言及のみ | 無し（7.4節はテラヘルツ波の人体安全性と身体走査の倫理） | https://www.microsoft.com/en-us/research/wp-content/uploads/2016/10/WillisSiggraph2013.pdf |
| AirCode | 2017 | デジタル光処理方式プロジェクタ Mitsubishi PK20 と単色カメラ Point Grey Grasshopper3、交差偏光板（撮像3分から4分） | 物体をプロジェクタとカメラの前に置き、市松模様を掃引して16枚平均する | 約106ビット（2センチメートル角）、約500ビット（5センチメートル角） | 有り。リードソロモン符号で冗長度40パーセント | 無し | https://www.cs.columbia.edu/cg/aircode/aircode-uist-2017-li-et-al.pdf |
| Acoustic Voxels | 2016 | iPhone 1台（スピーカとマイクロホン） | 透過損失を読む場合はスピーカから白色雑音を鳴らし入口と出口に当てる。識別だけなら手のひらで叩く | 4ビット（透過損失曲線、3個の造形物で実証）。叩いて識別する用途では3通り＝1.585ビット（換算） | 無し | 無し | https://www.cs.columbia.edu/cg/lego/acoustic-voxels-siggraph-2016-li-et-al.pdf |
| LayerCode | 2019 | 一般的なカメラ（Canon の一眼レフ 5184×3456画素、iPhone 4032×3024画素でも同等）。近赤外の変種のみ近赤外フィルタ付きカメラ | 物体を撮影する。追加の光源は不要 | 24ビット（二色印刷と層厚変調）、12ビット（近赤外の変種） | 無し。あえて付けないと明記。リードソロモン符号を採用可能とも記述 | 無し | https://www.cs.columbia.edu/cg/layercode/LayerCode_Maia_et_al_2019_lowRez.pdf |
| G-ID | 2020 | 市販スマートフォンのカメラと専用アプリ。充填まで読むには小型光源 Nitecore Tini を併用 | 物体の底面を輪郭に合わせて撮影する。充填を読むときは側面から光を当てる | 204通り＝7.672ビット（カメラのみ）、17,136通り＝14.065ビット（カメラと光源）。原典自身が「7ビットまたは14ビットの一次元バーコードより大きい」と記述 | 訂正符号は無し。36通りの角度のうち2通りを誤り検査に予約 | 無し | https://groups.csail.mit.edu/hcie/files/research-projects/G-ID/2020-CHI-GID-paper.pdf |
| Acoustic Barcodes | 2012 | 圧電接触型マイクロホンを面に貼り、増幅してノートパソコンへ（標本化96キロヘルツ、4キロヘルツ高域通過） | 指の爪、マーカー、携帯電話のいずれかで刻み目の列をなぞる | 生の符号長は6ビット、12ビット、24ビット。誤り訂正後の実効データは24ビット符号で12ビット（4096通り）、12ビット符号で4ビット、6ビット符号で3ビット | 有り。24ビットに拡張ゴレイ符号、12ビットに短縮(15,7)BCH符号、6ビットに短縮(7,4)ハミング符号。(63,30)BCH符号とリードソロモン符号は将来の提案 | 無し | https://www.chrisharrison.net/projects/acousticbarcodes/AcousticBarcodes.pdf |
| Lamello | 2015 | 接触型マイクロホン（標本化16000ヘルツ）とPython の高速フーリエ変換処理系 | スライダやダイヤルを動かして撥が櫛歯を弾く | 原典はビット数を書いていない。信頼できたのは4枚の櫛歯（924から1662ヘルツ）で適合率93パーセント、すなわち2.0ビット相当（換算）。7枚では適合率49パーセントまで落ちる | 無し。de Bruijn 系列は位置と方向の決定のための符号設計であって誤り訂正ではない | 無し | https://people.eecs.berkeley.edu/~bjoern/papers/savage-lamello-chi2015.pdf |
| Blowhole | 2018 | ノートパソコンの内蔵マイクロホン（標本化44,100ヘルツ）、Welch の方法、scikit-learn による分類。Android 腕時計でも可 | 穴に軽く息を吹き込む | 6個の穴を利用者非依存98パーセントで区別＝2.585ビット（換算）。上限として9個＝3.170ビット（換算） | 無し | 無し | http://graphicsinterface.org/wp-content/uploads/gi2018-18.pdf |
| Seedmarkers | 2021 | 一般的なカメラ（ReacTIVision と互換） | 標識が写るように撮像する | 11,358,880通り＝23.437ビット（深さ4・幅4）。6自由度の姿勢推定を伴う部分集合は58,905通り＝15.846ビット（いずれも換算） | 無し。著者自身が誤り訂正の欠如を欠点として明記 | 無し | https://floe.butterbrot.org/matrix/publications/getschmann2021seedmarkers.pdf |
| InfraredTags | 2022 | 自作の近赤外撮像モジュール（Raspberry Pi NoIR カメラ20ドル、Raspberry Pi Zero、電池、重さ132グラム）を携帯電話ケースに装着 | 物体に近赤外カメラを向ける（必要な近赤外照度は0.2ルクスから1.1ルクス、距離は最大250センチメートル） | 21×21のQRコードで数字25文字＝83.05ビット（換算）。4×4の ArUco マーカーも埋め込み | QRコード自身の誤り訂正に依拠。独自の追加は無し | 無し | https://arxiv.org/pdf/2202.06165 |
| AnisoTag | 2023 | 自作の検出装置（Class IIIA レーザーポインタ3ドル、光導電素子16個、マイクロコントローラ STM32F103 が7ドル、三脚で固定） | タグをレーザーの照射域を横切るように滑らせる | 51ビット（53.98×85.6ミリメートル、クレジットカードと同寸、17領域×3ビット）。カラーカメラと画像処理併用への拡張で160ビット | 記述無し | 無し | https://arxiv.org/pdf/2301.10599 |
| StructCode | 2023 | 一般的なカラーカメラ（Pixel 2 の1220万画素、45センチメートル離して撮影） | 継手やヒンジが写るように携帯電話で撮影する | 指型継手で12文字＝76.08ビット、リビングヒンジで21文字＝133.14ビット、大きなヒンジ（193本の切れ目）で36文字＝228.23ビット（いずれも1文字81通りからの換算） | 無し。リードソロモン符号とハミング符号は将来の可能性として言及 | 無し。ただし対応表の暗号化に一言だけ言及 | http://groups.csail.mit.edu/hcie/files/research-projects/structcode/2023-SCF-StructCode-paper.pdf |
| SoundOff | 2025 | 超音波マイクロホン Ultramic384K BLE（16ビット、標本化384キロヘルツ）を手首に巻き、Raspberry Pi Zero で処理 | 扉、便座、引き出し、蛇口、窓などを普通に動かすと、タグが受動的に超音波を発する | 原典はビット数を書いていない。区別できた設計は15個＝3.907ビット（換算、0.5メートルで93.75パーセント）。設計候補は1277通りだが互いに区別できる集合ではない。抄録の「数千通り」に対応する具体的な数は本文に無い | 無し。周波数照合の規則による分類 | 無し（プライバシーは「カメラも可聴音録音も使わない」という設計目標としての言及） | https://drive.google.com/file/d/1StyNwdbcGeV810e1TdhXK2Wv9YkMV2a8/view |

## 表を書き直すときに気をつけたい点

第一に、容量の性質が二つに分かれる。データを運ぶことを目的として設計した研究（InfraStructs の行列型タグ、
AirCode、LayerCode、Acoustic Barcodes、InfraredTags、AnisoTag、StructCode、Acoustic Voxels の符号化）と、
個体を識別することを目的として設計した研究（G-ID、Seedmarkers、Blowhole、Lamello、SoundOff、
Acoustic Voxels の音響タグ）である。後者のビット数はすべて本稿が個数から換算したものであり、
原典はビット数を書いていない。表では換算であることを注記するのが誠実である。

第二に、同じ面積での比較が可能である。AnisoTag が自分の論文で
「同じ大きさのタグで AnisoTag は51ビット、LayerCode は25ビット、Acoustic Barcodes は40ビット」と
書いている。CipherFlute のカード実装のビット数はこの三つの数字と直接並べられる。

第三に、リードソロモン符号を実際に使っているのは AirCode だけである。
LayerCode、InfraStructs、StructCode は「採用できる」または「将来課題」と書くにとどまり、
Acoustic Barcodes は拡張ゴレイ符号と短縮BCH符号と短縮ハミング符号を実際に評価している。
したがって「造形タグに誤り訂正符号を入れた」ことは新規性にならないが、
「リードソロモン符号を実際に組み込んだ造形タグ」はAirCodeに次ぐ2例目という位置づけになる。

第四に、隣接する記号への制約は Acoustic Barcodes に前例がある。
固定物理長方式で「0が2つ続く列を禁止する」制約を入れており、
その理由も「クロック信号を復元できるようにするため」と CipherFlute と同じ動機である。
CipherFlute の隣接同音禁止を新規性として書くのは危うく、
「音高スロットという離散化に対して同じ発想を適用した」と書くのが正確である。

第五に、脅威モデルを持つ研究は13件のうち1件も無い。
InfraStructs の「Safety and Privacy」節はテラヘルツ波の安全性、
SoundOff の「privacy」はカメラや可聴音を使わない設計目標、
StructCode の暗号化は一文だけの言及であり、いずれも攻撃者を定義した脅威モデルではない。
この空白は前段の調査の結論と一致し、一次資料でも裏付けられた。

第六に、読み出しに要する装置の水準が三段階に分かれる。
研究室級の装置（InfraStructs のテラヘルツ分光、AirCode のプロジェクタとカメラの組）、
10ドルから20ドルの自作装置（AnisoTag のレーザーとフォトレジスタ、InfraredTags の近赤外モジュール、
SoundOff の超音波マイクロホン）、
市販の端末そのまま（LayerCode、G-ID、StructCode、Seedmarkers はカメラのみ、
Acoustic Voxels は iPhone のみ、Blowhole はノートパソコンの内蔵マイクロホンのみ、
Acoustic Barcodes と Lamello は接触型マイクロホンを面に貼る）である。
CipherFlute の「口とマイクだけ」は三段目に属し、この段には既に6件がいる。
差分は装置の安さではなく、読み出しに所有者の身体的な行為（吹く）を要することである。

## 残っている不足

第一に、SoundOff の1個あたりのビット数は原典に書かれていないため、
15個という実証値からの換算で書くしかない。本文が2026年12月2日に自由に公開される予定なので、
それ以降に改訂版が出ていないかを確かめたほうがよい。

第二に、Lamello の容量は原典が意図していない換算であるため、比較表に載せるべきかどうかは判断が必要である。
入力部品の位置検出という目的が CipherFlute と異なるので、
容量の欄を「該当せず」とし、注で4枚2ビット相当と書く選び方もありうる。

第三に、InfraredTags の「数字25文字」がQRコードの規格上のどの誤り訂正水準に対応するのかは
原典に書かれていない。21×21はQRコードの型番1であり、規格上の数字容量は誤り訂正水準が低いほうから
41文字、34文字、27文字、17文字である。25文字はこのどれとも一致しないので、
原典の数字をそのまま引くのが安全であり、規格から逆算した水準を書くべきではない。

第四に、ACM Digital Library の本文には一件も到達できなかった。
すべて著者の公開版、arXiv版、機関の公開ファイル、著者本人が公開した保存領域で代替した。
出版社版と著者版で数値が食い違う可能性は残るが、
今回引用したものはいずれも著者自身が公開した版であり、査読後の版と考えられる。
