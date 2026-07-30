# 反例検証 c5: 半音格子を符号語彙とする発想は先行研究に存在しないのか（語ではなく概念で探し直す）

調査日: 2026年7月30日
調査者: 反例検証担当（第三段）
検証対象の批判: 「`semitone` という語が0件だから半音格子を符号語彙とする発想は先行研究に存在しないという結論は、単語の不在と概念の不在を混同している。Whooshは本文で管長を 2^(i/12) によって定めており、`semitone` という語がなくても概念として半音格子を使っている」

---

## 0. 結論

**この批判は正しい。反例は成立する。**

概念で探し直した結果、次の三つが一次資料で確認できた。

第一に、Whoosh の FluteCase は、管長を公比 2^(1/12) の等比数列で定めているだけでなく、そこから生じる8つの離散した共鳴周波数を「どの領域を吹いたかを見分けるため」に使うと本文に明記している。すなわち「等比数列で並べる」ことと「その離散周波数の集合を識別の語彙として使う」ことの両方が、2016年に既に一つの論文の中で揃っている。単語の不在を根拠に概念の不在を言うことはできない。

第二に、公比が半音比かどうかを問わなければ、「受動的な造形物に複数の共鳴体を並べ、その離散周波数の集合を識別や符号化の語彙として使う」研究は複数存在する。CHI 2015 の Lamello は櫛歯の長さを変えて7つの離散周波数を作り、どの歯が叩かれたかを識別し、さらにドブラン列で位置を符号化している。Journal of Applied Physics 2022 の水中音響バーコードは、球の半径を変えて共鳴峰の有無を3ビットの二進符号として読み出している。

第三に、平均律の格子そのものを符号の語彙として使う先行例も存在する。Google の特許「Communicating data with audible harmonies」は、平均律の音名から成る音階を記号写像として指定している。日本語文献では、中沢誠と山崎芳男による「1/12Nオクターブ分析を用いた音の符号化」が、12音平均律に基づく対数等間隔の周波数分割を符号化の格子として使い、分割数 N を設計変数として扱っている。

したがって、SURVEY.md 第180行の「半音刻みの格子を符号の語彙とする発想は、この系譜の後続に一切現れない」という文は、そのままでは維持できない。ただし後述するとおり、CipherFlute に残るものは依然としてある。格子そのものではなく、格子の使い方の側にある。

---

## 1. 観点1: 櫛歯、管、板、共鳴器を等比数列で並べた受動的なデバイス

### 1.1 Whoosh / FluteCase（ISWC 2016）——決定的な反例

| 項目 | 内容 |
|---|---|
| 題名 | Whoosh: Non-Voice Acoustics for Low-Cost, Hands-Free, and Rapid Input on Smartwatches |
| 著者 | Gabriel Reyes, Dingtian Zhang, Sarthak Ghosh, Pratik Shah, Jason Wu, Aman Parnami, Bailey Bercik, Thad Starner, Gregory D. Abowd, W. Keith Edwards |
| 掲載 | Proceedings of the 2016 ACM International Symposium on Wearable Computers, pp. 120-127 |
| DOI | 10.1145/2971763.2971765 |
| 書誌の確認先 | https://api.crossref.org/works/10.1145/2971763.2971765 （題名、著者10名、会議名、120-127ページ、2016年をそのまま返した） |
| 全文の確認先 | https://sites.cc.gatech.edu/fac/keith/pubs/iswc2016-whoosh.pdf （本調査で自分で取得し、pdftotext で本文を抽出して該当箇所を目視した） |

本文6ページの該当箇所を抽出したままの形で示す。

> "The cases have 8 closed pipe tubes of different lengths, each with an open hole. ... The eight tubes are designed to resonate at eight distinct frequencies between 2kHz to 10kHz, allowing blows near particular regions of the watch face to be readily disambiguated."

日本語訳: 「ケースは長さの異なる8本の閉管を持ち、それぞれに開いた穴が一つある。（中略）8本の管は2キロヘルツから10キロヘルツの間の8つの異なる周波数で共鳴するよう設計されており、これにより時計面の特定の領域の近くへの吹奏を容易に見分けられる。」

そして設計式が続く。

> "The length of each tube is defined by:  L = 14.956 ∗ 2^(i/12) [mm] (2)  where L is the length of each tube as a function of i, which denotes the ith tube."

日本語訳: 「各管の長さは次式で定義される。ここで L は i の関数としての各管の長さであり、i は i 番目の管を表す。」

さらに図5Gの説明文にも次の一文がある。

> "(G) bezel blows (labeled on the figure) starting from the lowest to highest resonant frequency."

日本語訳: 「(G) 最低の共鳴周波数から最高の共鳴周波数へと順に並べたベゼル吹き（図中に名前を付した）。」

この三つを並べると、批判の言うとおりのことが確認できる。第一に、公比は 2^(1/12) であり、これは平均律の半音比そのものである。第二に、その8つの離散周波数は「見分ける（disambiguate）」ために設計されたと明言されている。すなわち離散周波数の集合が識別の語彙として使われている。第三に、著者たちは図の説明で管を共鳴周波数の順に並べており、周波数の並びを構造として意識している。

`semitone` という語が0回であることは事実だが、それは概念の不在を意味しない。前段の推論は誤りである。

なお、前段の報告（raw2/v1-whoosh-flutecase.md）が指摘した差分は今回も変わらず成り立つ。読み取り側はメル周波数ケプストラム係数とサポートベクターマシンによる利用者ごとの学習分類であって、基本周波数の推定と量子化ではない。また管長は論文に公開された固定の定数であり、すべての複製が同一形状になることを意図している。この二点は後述する。

### 1.2 Lamello（CHI 2015）——語彙としての離散周波数は先取りされている。ただし等比ではない

| 項目 | 内容 |
|---|---|
| 題名 | Lamello: Passive Acoustic Sensing for Tangible Input Components |
| 著者 | Valkyrie Savage, Andrew Head, Björn Hartmann, Dan B. Goldman, Gautham Mysore, Wilmot Li |
| 掲載 | Proceedings of the 33rd Annual ACM Conference on Human Factors in Computing Systems, pp. 1277-1280 |
| DOI | 10.1145/2702123.2702207 |
| 書誌の確認先 | https://api.crossref.org/works/10.1145/2702123.2702207 （題名、著者6名、CHI 2015、1277-1280ページ、2015年を返した） |
| 全文の確認先 | https://people.eecs.berkeley.edu/~bjoern/papers/savage-lamello-chi2015.pdf （本調査で自分で取得し、pdftotext で抽出した） |

Lamello は、長さの違う櫛歯（tine）を並べた受動的な3Dプリント部品であり、叩かれた歯の基本周波数から「どの歯が叩かれたか」を判定する。名前は親指ピアノの類（ラメロフォン）に由来すると本文が述べている。

重要なのは、Lamello が離散周波数の集合を明示的に符号の語彙として扱っている点である。

> "Encoding information: We use unique f0s to differentiate buttons and directions on a D-pad. For position sensing, f0 can increase across the range of motion. If more distinctions are needed than can be reliably recognized by varying f0, we create de Bruijn patterns. ... A de Bruijn sequence D(k, n) is one which, given an alphabet size k and a subsequence length n, contains each subsequence exactly once: we can uniquely infer sequence position from n recognitions."

日本語訳: 「情報の符号化: 我々は固有の基本周波数を使って、ボタンと十字キーの方向を区別する。位置検出については、可動域にわたって基本周波数を増加させることができる。基本周波数を変えることで確実に認識できる数より多くの区別が必要なら、ドブラン模様を作る。（中略）ドブラン列 D(k, n) とは、字母の大きさ k と部分列の長さ n が与えられたとき、各部分列をちょうど一度ずつ含む列である。すなわち n 回の認識から列中の位置を一意に推定できる。」

`alphabet size k`（字母の大きさ）という語がそのまま使われている。つまり「離散した基本周波数の集合を字母とし、その列で情報を符号化する」という発想は、2015年に完全に成立している。この点は CipherFlute の新規性ではない。

ただし**格子は等比ではない**。本文は次のように書いている。

> "for dials and sliders that encode position with linearly increasing tine lengths"

日本語訳: 「歯の長さを線形に増加させて位置を符号化するダイヤルとスライダについては」

論文が報告した7本の歯の基本周波数（図6）は、スライダが 924, 1103, 1340, 1662, 2116, 2784, 3824 ヘルツ、ダイヤルが 840, 1003, 1218, 1511, 1923, 2530, 3478 ヘルツである。私がこれらから計算した結果を示す（論文が報告した値ではなく私の計算である）。

| 隣接する2本の間隔（セント） | スライダ | ダイヤル |
|---|---|---|
| 1本目と2本目 | 306.6 | 307.0 |
| 2本目と3本目 | 337.0 | 336.2 |
| 3本目と4本目 | 372.8 | 373.2 |
| 4本目と5本目 | 418.1 | 417.4 |
| 5本目と6本目 | 475.0 | 474.9 |
| 6本目と7本目 | 549.5 | 550.9 |

対数軸上の間隔は307セントから550セントへ単調に広がっており、等間隔からはほど遠い。片持ち梁の基本周波数は長さの2乗に反比例するので、1/√f が長さに比例するはずである。実際に 1/√f の隣接差を計算すると、スライダで 278.7, 279.2, 278.9, 279.0, 278.7, 278.1（いずれも10のマイナス5乗単位）となり、0.4パーセント以内で一定である。すなわち歯の長さは厳密に等差数列であり、周波数は等比数列ではない。

さらに Lamello 自身が、周波数の配り方をまだ決めていないと述べている。

> "Future work can also probe optimal frequency distributions to avoid overlap between tine harmonics."

日本語訳: 「今後の課題として、歯の倍音どうしの重なりを避けるための最適な周波数分布を調べることもできる。」

したがって「対数軸上で等間隔に切る」という選択は Lamello にはない。Lamello が達成できなかったのは2キロヘルツを超える帯域の分類であり（7本のときの再現率はスライダで56パーセント、ダイヤルで54パーセントまで落ちる）、その原因を高い周波数のエネルギーの低さと減衰の速さに帰している。

### 1.3 水中音響バーコード（Journal of Applied Physics 2022）——符号語彙だが等分割は線形

| 項目 | 内容 |
|---|---|
| 題名 | Passive underwater acoustic barcodes using Rayleigh wave resonance |
| 著者 | Yanling Zhou, Jun Fan, Jinfeng Huang, Bin Wang |
| 掲載 | Journal of Applied Physics, 131巻12号, 論文番号124901, 2022年 |
| DOI | 10.1063/5.0086290 |
| 書誌の確認先 | https://api.crossref.org/works?query.title=Passive+underwater+acoustic+barcodes+using+Rayleigh+wave+resonance |
| 全文の確認先 | https://arxiv.org/pdf/2107.13860 （本調査で自分で取得し、pdftotext で抽出した。出版社のページ https://pubs.aip.org/aip/jap/article-abstract/131/12/124901/2836637/ は403を返して読めなかった） |

アクリル球のレイリー波共鳴を使い、球の半径を変えて後方散乱の共鳴峰の位置を制御し、周波数領域に白黒のバーコードを作る研究である。抽出した本文から関係する記述を示す。

> "The frequency spectrum of the broadband signal over the range 6-10.5 kHz is divided into three uniform subbands, and each subband width is Δf = 1.5 kHz."

日本語訳: 「6キロヘルツから10.5キロヘルツの範囲の広帯域信号の周波数スペクトルは、三つの一様な副帯域に分割され、各副帯域の幅は1.5キロヘルツである。」

> "spheres with radii of a1 = 0.045 m, a2 = 0.05 m, a3 = 0.06 m, and a4 = 0.065 m are separately selected."

日本語訳: 「半径 0.045メートル、0.05メートル、0.06メートル、0.065メートルの球がそれぞれ選ばれた。」

そして「Binary codes 001 010 100 101 110 011 111」という表があり、7通りの組み合わせが3ビットの二進符号に対応する。

すなわち「受動的な物体の共鳴周波数の集合を符号語彙として読み出す」という枠組みは成立しているが、帯域の分割は一様（線形）であり、半径も等比数列ではない（比は 1.111, 1.200, 1.083 とばらばらである）。したがって対数格子の反例にはならない。ただし「物体の形状が符号を担い、読み取り側は事前にその値を知らない」という向きは、Whoosh よりも CipherFlute に近い。この点は素直に認めるべきである。

なお、この論文は参考文献として Harrison らの Acoustic Barcodes（UIST 2012, DOI 10.1145/2380116.2380187, 563-568ページ, https://api.crossref.org/works/10.1145/2380116.2380187 で確認）を引いている。Acoustic Barcodes は刻みの間隔から時間領域で二進の識別子を作るものであり、周波数の格子は使っていない。

### 1.4 反例にならなかったもの

- **FabAuth（CHI Extended Abstracts 2019）**。題名は Printed Objects Identification Using Resonant Properties of Their Inner Structures、著者は Yuki Kubo, Kana Eguchi, Ryosuke Aoki, Shigekuni Kondo, Shozo Azuma, Takuya Indo、1-6ページ、DOI 10.1145/3290607.3313005（https://api.crossref.org/works/10.1145/3290607.3313005 で確認）。3Dプリント物体の内部構造の違いから生じる共鳴特性の差で個体を識別する。ただし共鳴周波数は設計された格子上に置かれるのではなく、任意の内部構造から創発するものを照合するだけである。本文は dl.acm.org が403を返して読めず、内容は検索結果の要約に留まる。
- **SoundOff（IMWUT 2025）**。題名は SoundOff: Low-cost Passive Ultrasound Tags for Non-invasive and Non-Intrusive Smart Home Sensing、著者は Yibo Fu, Vivian Shen, Víctor Riera Naranjo, Bolei Deng, Alex Adams, Josiah Hester、9巻4号、DOI 10.1145/3770666（https://api.crossref.org/works/10.1145/3770666 で確認）。電子部品を持たない受動的な超音波発生タグを幾何形状の違いで数千通り作り分けるという、CipherFlute に近い枠組みである。ただし本文が読めず（ACM は403、NSF の公開版は2026年12月2日まで公開猶予）、周波数を対数格子上に置いているかどうかは**確認できなかった**。今後の追跡対象として最優先で挙げておく。

---

## 2. 観点2: 周波数の集合を対数軸上で等間隔に配置して識別に使う研究（音響以外を含む）

### 2.1 人工基底膜と蝸牛模倣の共振子アレイ

長さの異なる片持ち梁を並べて、蝸牛の場所ごとの周波数対応を機械的に再現する研究群がある。一次資料として次を確認した。

| 項目 | 内容 |
|---|---|
| 題名 | Mechanical frequency selectivity of an artificial basilar membrane using a beam array with narrow supports |
| 著者 | Sangwon Kim, Won Joon Song, Jongmoon Jang, Jeong Hun Jang, Hongsoo Choi |
| 掲載 | Journal of Micromechanics and Microengineering, 23巻9号, 論文番号095018, 2013年 |
| DOI | 10.1088/0960-1317/23/9/095018 |
| 確認先 | https://iopscience.iop.org/article/10.1088/0960-1317/23/9/095018 （要旨全文を取得した） |

要旨には「Each ABM contained 16 beams with various lengths in a one-dimensional array」（各人工基底膜は一次元配列に長さの異なる16本の梁を含む）とあり、周波数選択性の範囲は2キロヘルツから20キロヘルツと書かれている。ただし**長さの与え方が等比なのか等差なのかは要旨に書かれていない**。

もう一つ、Scientific Reports の Jang らの論文（A microelectromechanical system artificial basilar membrane based on a piezoelectric cantilever array and its characterization using an animal model, Scientific Reports 5巻 論文番号12447, 2015年, DOI 10.1038/srep12447, https://pmc.ncbi.nlm.nih.gov/articles/PMC4521187/ で確認）も見たが、「片持ち梁の幅は300マイクロメートル、長さは600から1350マイクロメートルまで変化させた」とあるだけで、分布則の記述は見つからなかった。

検索結果の要約には「resonance frequency of the beam changes exponentially along the array」（梁の共鳴周波数は配列に沿って指数関数的に変化する）という文が Electronic Materials Letters の別論文（DOI 10.1007/s13391-014-4053-2）について現れたが、出版社のページが認証を要求して開けず、**一次資料では確認できなかった**。

いずれにせよ、この系譜は「音を分析するための共振子の並び」であって、「情報を符号化するための語彙」ではない。CipherFlute の新規性への脅威としては弱い。ただし「対数的に周波数を並べた受動的な共振子アレイ」という物理の作り方それ自体が既知であることは、控えめに認めておくべきである。

### 2.2 チップレスRFIDのスペクトル署名

複数の共振器をそれぞれ別の周波数に同調させ、共鳴峰の有無で1ビットずつ符号化するという方式は確立している。すなわち「離散周波数の集合を符号語彙にする」という発想は電波の領域では標準的である。ただし今回調べた範囲では、周波数の割り当てを対数軸上の等間隔にすると明記した一次資料は見つからなかった。見つかったものはいずれも帯域を一様に割る方式か、共振器の形状から決まる位置をそのまま使う方式であった。したがって**観点2に対する反例としては、対数格子の部分は確認できなかった**。

---

## 3. 観点3: 楽器の音階を情報の符号語彙として使った研究

### 3.1 Communicating data with audible harmonies（Google の特許）

| 項目 | 内容 |
|---|---|
| 題名 | Communicating data with audible harmonies |
| 発明者 | Boris Smus, Pascal Tom Getreuer |
| 権利者 | Google LLC |
| 特許番号と日付 | US 9,755,764 B2（出願優先日2015年6月24日、登録2017年9月5日）、および継続出願の US 9,882,658 B2（登録2018年1月30日） |
| 確認先 | https://patents.google.com/patent/US9755764B2/en および https://patents.google.com/patent/US9882658B2/en |

記号写像（symbol map）が特定の調の特定の音階を指定し、その音階の音と和音から記号を作ると書かれている。取得した本文には次の記述がある。

> "the symbol map may specify that the C pentatonic major scale is to be used, meaning that symbols will be formed by selecting notes and chords from the notes of that scale (e.g., [C, D, E, G, A])."

日本語訳: 「記号写像はハ長調のペンタトニック音階を使うと指定することができ、これは記号がその音階の音（たとえばド、レ、ミ、ソ、ラ）から音と和音を選ぶことで作られることを意味する。」

周波数は平均律の値（たとえば C4 は 261.6 ヘルツ、D5 は 587.3 ヘルツ）で与えられている。すなわち「平均律の格子上の離散音高を記号の字母とする」という発想は、2015年の優先日を持つ特許として既に存在する。ただし、これは能動的なスピーカから音を出す音響通信であり、物理的な共鳴体を持つ物体ではない。

なお、検索結果の要約には「半音の間隔をビット0に、全音の間隔をビット1に対応させる」という趣旨の文が現れたが、私が二つの特許本文に当たった限りではその記述を見つけられなかった。**この点は確認できなかった**ものとして扱う。

### 3.2 音楽性信号への符号化による携帯端末用音響通信（三重大学 修士論文, 2014年）

| 項目 | 内容 |
|---|---|
| 題名 | 音楽性信号への符号化による携帯端末用音響通信 |
| 著者 | 大石 智久 |
| 種別 | 三重大学大学院工学研究科情報工学専攻 修士論文（2014年） |
| 確認先 | https://cir.nii.ac.jp/crid/2120307889675241344 および機関リポジトリ https://mie-u.repo.nii.ac.jp/records/9533 |

12音階から協和する音を選んで和音を組み、データのビット値（1と0）を音の有無に一対一で対応させ、音楽理論に従って和音を切り替えながら送信する方式である。CM7、DM7、G7、CM7 という進行を4拍ごとに循環させる実装が書かれている。すなわち「音階を符号の語彙にする」という発想は日本語の学位論文としても存在する。

---

## 4. 観点4: 対数的な周波数の刻みを設計変数として決めた研究

### 4.1 1/12Nオクターブ分析を用いた音の符号化（中沢誠, 山崎芳男, 2003年）

| 項目 | 内容 |
|---|---|
| 題名 | 1/12Nオクターブ分析を用いた音の符号化 |
| 著者 | 中沢 誠, 山崎 芳男（早稲田大学国際情報通信研究科） |
| 掲載 | GITS/GITI research bulletin, 2002巻, 81-85ページ, 2003年, 早稲田大学 |
| 確認先 | https://cir.nii.ac.jp/crid/1572261551695122304 |

これが観点4に最も近い。人間の聴覚が音高に対して比で一定の感度を持つことと、楽譜が12音平均律に基づくことを根拠に、1オクターブを12N分割した対数等間隔の格子を分析と符号化の格子として採用している。分割数 N と分析の基準周波数を自由に選べることを設計の自由度として扱い、聴覚特性を考慮したうえで 705.6 キロビット毎秒の信号をおよそ80.0キロビット毎秒から130.0キロビット毎秒まで落とせたと報告している。

すなわち「対数軸上で半音（またはその N 分の1）刻みに周波数を切り、その格子を符号化に使い、刻みの細かさを設計変数として品質と量の兼ね合いで決める」という発想は、2003年の日本語文献に存在する。これは CipherFlute の「等間隔のセントで切って復号の判定を確実にする」という考え方と、目的こそ違うが構造は同じである。

### 4.2 定Q変換（Brown, 1991年）

| 項目 | 内容 |
|---|---|
| 題名 | Calculation of a constant Q spectral transform |
| 著者 | Judith C. Brown |
| 掲載 | The Journal of the Acoustical Society of America, 89巻1号, 425-434ページ, 1991年 |
| DOI | 10.1121/1.400476 |
| 書誌の確認先 | https://api.crossref.org/works?query.title=Calculation+of+a+constant+Q+spectral+transform&query.author=Brown |

周波数の分点を等比数列に置き、1オクターブあたりの分点数を平均律の半音（あるいは四分音）に合わせることで、音楽の音高の識別に適した分析を行う手法である。書誌は Crossref で確認したが、入手できた全文の写し（https://www.ee.columbia.edu/~dpwe/papers/Brown91-cqt.pdf）は画像として取り込まれた走査版であり、文字が抽出できなかったため、**分点の式そのものを一次資料の文言として引用することはできなかった**。したがってここでは「対数等間隔の周波数格子を音高識別の語彙として使う手法が1991年から標準的に存在する」という一般的な事実を、書誌の確認までに留めて記す。

---

## 5. どこまで探して、何が見つからなかったか

### 5.1 実際にかけた検索

英語の検索語として次を試した。geometric progression resonator array logarithmically spaced resonant frequencies identification tag、Lamello passive acoustic sensing 3D printed tine comb frequency、Acoustic Voxels 3D printed acoustic filters tagging、artificial basilar membrane cantilever beam array exponentially varying length、chipless RFID logarithmically spaced resonant frequencies bit encoding、frequency spacing chipless RFID tag design tradeoff detection error constant fractional bandwidth、musical scale notes as data encoding vocabulary acoustic communication、data over sound semitone spacing frequency shift keying、graded metamaterial resonator array geometric progression rainbow trapping、passive resonator tag logarithmic geometric frequency spacing barcode identification、acoustic barcodes Harrison Xiao Hudson UIST 2012、Rayleigh wave resonance underwater acoustic barcode、3D printed passive object encoded identifier tuned resonant pitches musical scale、SoundOff passive ultrasound tags。

Crossref の書誌検索の機能（query.bibliographic）に対して、logarithmically spaced resonant frequencies identification tag と geometric progression resonator array encoding と artificial basilar membrane beam array exponentially varying resonance frequency の三つをかけた。いずれも語句の一致に引きずられた雑多な結果を返し、当たりは Broadband Transducer Composed of Three Elements with Proportionately Spaced Resonant Frequencies（JASA 1960）くらいであった。これは広帯域変換器の設計であって符号化ではない。

日本語では CiNii Research の検索に対して、「共鳴 等比 周波数 符号化」（0件）、「共鳴器アレイ 周波数 識別」（0件）、「音階 符号化 音響 情報埋め込み」（0件）、「共鳴管 識別」（0件）、「音階 符号化」（6件）、「1/12Nオクターブ分析」（1件）、「音楽性信号への符号化による携帯端末用音響通信」（1件）をかけた。当たりは第4節と第3節に挙げた2件である。

### 5.2 見つからなかったもの

次のものは、探した範囲では見つからなかった。

- **公比 2^(1/12) の等比数列で共鳴体を並べ、その音高を絶対値として推定して量子化し、多ビットのデータとして読み出す造形物**。Whoosh は等比で並べるが読み方が学習分類であり、Lamello は読み方が周波数照合だが並べ方が等差である。両方を兼ねた先行例は見つからなかった。
- **チップレスRFIDで周波数の割り当てを対数等間隔にすると明記した一次資料**。
- **人工基底膜の梁の長さを等比数列で与えると明記した一次資料**（二次的な要約にはその記述があったが、一次資料には到達できなかった）。
- **半音の間隔と全音の間隔をビット0とビット1に対応させるという記述**（検索結果の要約には現れたが、二つの特許の本文には見つけられなかった）。

### 5.3 読めなかった資料

- https://pubs.aip.org/... （AIP、403を返した。arXiv 版で代替した）
- https://dl.acm.org/... （ACM、403を返した。Crossref と著者公開版で代替した。FabAuth と SoundOff の本文は代替できなかった）
- https://link.springer.com/article/10.1007/s13391-014-4053-2 （認証画面に転送された）
- https://www.mdpi.com/1424-8220/15/8/18851 （403を返した）
- https://www.researchgate.net/... （403を返した）
- https://www.cs.columbia.edu/cg/lego/acoustic-voxels-siggraph-2016-slides-li-et-al.pdf （10メガバイトの上限を超えて取得できず、Acoustic Voxels の音響タグの周波数の置き方は確認できなかった）
- https://www.ee.columbia.edu/~dpwe/papers/Brown91-cqt.pdf （走査画像で文字が抽出できなかった）

---

## 6. この反例のもとで CipherFlute に残るもの

誇張も過小評価もせずに書く。

**放棄すべき主張**。「半音格子を符号の語彙とする発想は先行研究に存在しない」とは書けない。等比数列で共鳴管を並べること（Whoosh）、離散周波数の集合を字母として列で符号化すること（Lamello）、平均律の音階を記号の字母にすること（Google の特許、大石の修士論文）、対数等間隔の格子の細かさを設計変数にすること（中沢と山崎）は、いずれも先行例がある。また「semitone という語が0件だった」という語句照合の結果を新規性の根拠に使うことは、今後やめるべきである。語の不在は概念の不在ではない。

**それでも残る主張**。残るのは格子そのものではなく、格子の使い方の側にある。具体的には次の四つである。

第一に、**情報の向きである**。Whoosh の管長は論文に公開された定数であり、すべての複製が同一形状になることを意図している。情報は形状ではなく利用者の選択に載る。Lamello も同じで、歯の長さは部品の設計に固定されており、情報は利用者の操作に載る。CipherFlute はこれと逆で、格子上のどの位置に管を置くかが個体ごとに違い、その違いこそが運ぶべき値である。読み取り側は事前にその値を知らない。水中音響バーコードだけはこの向きが同じだが、そちらは対数格子を使っていない。

第二に、**読み方である**。Whoosh はメル周波数ケプストラム係数とサポートベクターマシンによる利用者ごとの学習分類であり、基本周波数を推定しない。したがって未知の管長を読むことができない。Lamello は基本周波数を照合するが、照合先は部品ごとに与えられる既知の周波数表であって、格子ではない。CipherFlute は絶対的な音高を推定して格子上に量子化するので、事前に知らない値を読める。

第三に、**格子の刻みを何から決めたかである**。Lamello は最適な周波数分布を今後の課題として明示的に残している。中沢と山崎は聴覚特性と符号量から刻みを決めており、造形の誤差や吹奏の揺らぎからではない。CipherFlute が刻みを実測の造形誤差と吹奏誤差から決めているのなら、その決め方は先行例と違う。ただしこれは「対数格子を設計変数にする」という発想そのものの新規性ではなく、「何を根拠に決めたか」の新規性であるから、論文では慎重に、決め方の具体を数字で示す形で書くべきである。

第四に、**符号列としての扱いである**。Lamello はドブラン列を使って字母数を減らしているが、誤り訂正は行っていない。多ビットの容量、符号語への連結、誤り訂正の付与という組み立ては、今回見た先行例のいずれにもない。

まとめると、CipherFlute が主張できるのは「半音格子を使うこと」ではなく、「半音格子を、未知の値を運ぶ担体の形状として使い、絶対音高の推定と量子化で読み、造形と吹奏の実測誤差から刻みを決め、誤り訂正を載せて多ビットの秘密として運ぶこと」の組み合わせである。個々の部品はいずれも先行例があるので、論文では組み合わせであることを明示し、部品ごとの先行例を正しく引くのがよい。とくに Whoosh は「半音比の等比数列で受動的な多管構造を作った先行例」として、Lamello は「離散周波数の集合を字母として列で符号化した先行例」として、明示的に引くべきである。
