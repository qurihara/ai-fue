# 低容量の物理媒体のための符号化と誤り訂正

この文書は、CipherFluteの符号設計（13個または12個のスロットからなる非二進の記号、隣接同音禁止の制約、リード・ソロモン符号による誤り訂正、基準笛による共通ずれの打ち消し）が符号理論と物理媒体符号化の系譜のどこに位置するかを定めるために、一次資料に当たって集めた調査結果である。書誌情報は原則としてCrossrefのDOI登録記録、出版社のページ、特許庁の公開特許、規格団体のページ、著者本人または研究機関の公開している原稿に当たって確認した。確認できなかったものは末尾の「未検証のまま残ったもの」にまとめた。

## この切り口の要約

物理媒体に少量の情報を載せる技術は、記号の作り方（変調と制約）と、壊れた記号を直す仕組み（誤り訂正）という二つの層に、ほぼ例外なく分かれている。この二層構造は磁気記録と光ディスクで確立した考え方であり、記録媒体の側の都合で許される記号列を制限する「制約符号」と、その外側に置く誤り訂正符号を組み合わせる。CipherFluteが採る「隣接同音禁止」は、この制約符号の系譜のうち、同じ記号が続くと読み手が記号の切れ目を見失うという問題に対する古典的な処方であり、ランレングス制限符号（Franaszek 1970、Tang and Bahl 1970、Immink 1990）と8B/10B符号（Widmer and Franaszek 1983）がその代表である。ただし現在この制約に最も近い実例は磁気記録ではなく、DNAへのデータ保存である。Goldmanらは2013年に、三進符号の各桁を「直前に使った塩基とは違う三塩基のいずれか」に写すことで同一塩基の連続を原理的に排除しており、これはCipherFluteの隣接同音禁止と機構としてまったく同じである。さらにGrassらは2015年に、DNAの記号数に合わせて有限体GF(47)上のリード・ソロモン符号を用い、素数個の記号を扱う設計を長期保存の文脈で実行している。二次元コードの側でも、PDF417は0から928までの929個の符号語を扱っており、929が素数であることから素数体上の算術を採っている。郵便のIntelligent Mail Barcodeに至っては、二進ではなく1365進などの混合基数へ変換したうえで、13ビット中の1の個数を5個または2個に固定した定重み符号へ写している。すなわち「記号数が2のべき乗でない物理媒体を、混合基数と素数体で素直に扱う」という設計はすでに実務の標準に存在する。一方で、こうした符号設計を3Dプリント造形物に対して実際に適用した例はきわめて乏しく、最も近いLayerCodeは24ビットしか載せず、しかも論文中で誤り訂正冗長を「あえて付けていない」と明言している。この空白がCipherFluteの符号面の主張の足場になる。

## 新規性への脅威が大きい文献

### 1. Toward practical high-capacity low-maintenance storage of digital information in synthesised DNA

- 著者: Nick Goldman, Paul Bertone, Siyuan Chen, Christophe Dessimoz, Emily M. LeProust, Botond Sipos, Ewan Birney
- 掲載: Nature, 第494巻, 第7435号, 77-80ページ, 2013年
- 確認先: https://pmc.ncbi.nlm.nih.gov/articles/PMC3672958/ （DOIは10.1038/nature11875）

内容の要約を述べる。バイト列をハフマン符号で三進の桁（トリット）へ変換し、その各トリットを「直前に使った塩基とは異なる三種類の塩基」のいずれかへ写すという差分的な写像でDNA配列を作っている。この写像の帰結として、同一塩基が二つ以上連続する状態（ホモポリマー）が構造的に生じない。さらに各配列を重なりを持つ断片へ分割して四重の冗長を与え、断片ごとにファイル識別子と位置の索引、および単純なパリティによる誤り検出を付けている。合計757,051バイトを117塩基の配列153,335本へ格納し、復元に成功している。

CipherFluteとの関係を述べる。「隣り合う記号が同じにならないように、次の記号を直前と異なるものから選ぶ」という制約の課し方が、CipherFluteの隣接同音禁止とまったく同じ機構である。CipherFluteが記号数13から実効12へ落として制約を満たす構成も、Goldmanらが四塩基から三塩基へ落とす構成と数え方まで一致する。断片ごとの索引と単純パリティという層構造も、CipherFluteの基準笛と誤り訂正の配置に対応する。

脅威の度合いは「高」である。理由を述べる。CipherFluteが隣接同音禁止を自分の設計上の工夫として提示すると、低容量の物理媒体において同じ制約が2013年のNature論文で確立していることを見落としたと受け取られる恐れがある。現論文が挙げている8B/10Bよりもこちらのほうが状況が近く、必ず引用して「先行する制約符号の考え方を音高の媒体へ持ち込んだ」と位置づけを明示する必要がある。

### 2. codex32: Checksummed SSSS-aware BIP32 seeds（BIP-93）

- 著者: Leon Olsson Curr, Pearlwort Sneed, Andrew Poelstra
- 掲載: Bitcoin Improvement Proposal 93, 状態はDraft, 2023年2月13日
- 確認先: https://github.com/bitcoin/bips/blob/master/bip-0093.mediawiki

内容の要約を述べる。暗号資産のシード（BIP32のマスターシード）をShamirの秘密分散で分割し、各シェアをbech32と同じ32文字の記号集合で表記したうえで、GF(32)上のBCH符号による検査符号を付ける規格である。標準の検査符号は13文字で最大80文字のデータを守り、長い方は15文字で75文字から103文字を守る。いずれも「最大8文字に影響する誤りは必ず検出する」と規定し、置換誤りなら4文字まで、消失なら8文字まで訂正できるとしている。設計上の中心的な主張は、小さな有限体と線形符号を選んだことにより「すべての計算を単純な参照表で行える」ため、検査符号の計算と検証、秘密の分割と復元のすべてを紙と鉛筆だけで実行できる、という点にある。

CipherFluteとの関係を述べる。目的（暗号資産のシードの物理的な保管）、秘密の守り方（Shamirの秘密分散に安全性を負わせる）、そして誤り訂正符号を物理媒体上の可読性の担保として使う点が、CipherFluteとほぼ完全に重なる。異なるのは媒体だけであり、codex32は紙とペン、CipherFluteは日用品に埋めた笛と音である。

脅威の度合いは「高」である。理由を述べる。「電源も電子部品も要らない物理媒体に、秘密分散のシェアを誤り訂正符号つきで載せる」という枠組み自体はcodex32がすでに完成させており、しかもcodex32は復号にも一切の電子機器を必要としない点でCipherFluteより徹底している。CipherFluteは復号に音の解析（すなわち計算機）を要するため、電源不要性の主張はこの文献との対比で慎重に述べ直す必要がある。CipherFluteの差分は、秘密が「文字列として見えていない」点、つまり日用品への偽装による探索コストの引き上げに絞られる。

### 3. Robust chemical preservation of digital information on DNA in silica with error-correcting codes

- 著者: Robert N. Grass, Reinhard Heckel, Michela Puddu, Daniela Paunescu, Wendelin J. Stark
- 掲載: Angewandte Chemie International Edition, 第54巻, 第8号, 2552-2555ページ, 2015年
- 確認先: https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=TITLE%3A%22Robust%20chemical%20preservation%20of%20digital%20information%20on%20DNA%20in%20silica%20with%20error-correcting%20codes%22&format=json&resultType=core （DOIは10.1002/anie.201411378、PMIDは25650567）

内容の要約を述べる。83キロバイトのデータを4,991本のDNA断片へ符号化し、シリカで封止して保存する方式を示している。内符号と外符号を重ねた誤り訂正符号を用い、70度で一週間という加速試験に耐えたことから、中央ヨーロッパの気候ではおよそ2,000年に相当する保存が可能だと主張している。要旨には「幅広い条件下で数千年にわたりDNA上に情報を保管できる」と述べられている。

CipherFluteとの関係を述べる。物理媒体に固有の記号数（DNAの場合は三塩基の組み合わせ）へ合わせて有限体の位数を選び、その上でリード・ソロモン符号を組む、という設計の順序がCipherFluteと同じである。CipherFluteが13個または12個のスロットに合わせて有限体を選ぶ判断は、この論文の判断の再現に当たる。長期保存という動機の面でも近い。

脅威の度合いは「中」である。理由を述べる。媒体はまったく異なるが、「符号語の個数を媒体の物理的な記号数に合わせ、二進に切り詰めずに非二進のリード・ソロモン符号を組む」という設計判断の先例として必ず引用すべきである。なお有限体GF(47)を用いたという広く知られた記述は本文ではなく補足資料にあるとみられ、今回は一次資料で確認できなかったため、引用の際は位数の数値を書かずに「三塩基の組み合わせ数に合わせた非二進の有限体」と述べるのが安全である。

### 4. Embracing Errors Is More Efficient Than Avoiding Them Through Constrained Coding for DNA Data Storage

- 著者: Franziska Weindel, Andreas L. Gimpel, Robert N. Grass, Reinhard Heckel
- 掲載: arXiv:2308.05952, 2023年8月11日投稿, 2024年6月26日改訂
- 確認先: https://arxiv.org/abs/2308.05952

内容の要約を述べる。DNAへのデータ保存では、同一塩基の連続を避け、GC含量を釣り合わせる制約符号が広く使われてきたが、制約を課すこと自体が冗長を増やす。この論文は、制約を課さずに配列を乱数化して誤りを受け入れ、その分を誤り訂正の冗長で払うほうが効率的になる誤り率の領域を定量的に決めている。結論として、現行のDNA保存系では置換誤りに対する制約符号は非効率であり、制約符号が有利になるには、ホモポリマー部分やGC含量が偏った配列での誤り率の増加が非常に大きくなければならないと述べている。

CipherFluteとの関係を述べる。CipherFluteは隣接同音禁止という制約と、リード・ソロモン符号という誤り訂正の両方を同時に採用している。この論文は、まさにその二つの手段のどちらにどれだけ資源を割くべきかという問いを正面から扱い、条件によっては制約を課さないほうが良いと結論している。

脅威の度合いは「中」である。理由を述べる。査読者から「なぜ制約と誤り訂正を両方入れるのか、制約をやめて笛の本数を減らしたほうが得ではないのか」と問われたときに、この論文が判断の枠組みを与える。CipherFluteの場合は隣接同音が読み取り時の区切り検出そのものを壊す（無音区切りの自動送りが働かなくなる）ため、置換誤り率の話ではなく同期の話であり、制約が必要だと反論できる。その反論を用意しておかないと符号設計の妥当性が弱く見える。

### 5. Capacity-Approaching Constrained Codes with Error Correction for DNA-Based Data Storage

- 著者: Tuan Thanh Nguyen, Kui Cai, Kees A. Schouhamer Immink, Han Mao Kiah
- 掲載: IEEE Transactions on Information Theory, 第67巻, 第8号, 5602-5613ページ, 2021年（プレプリントはarXiv:2001.02839, 2020年1月9日）
- 確認先: https://arxiv.org/abs/2001.02839 （DOIは10.1109/TIT.2021.3066430）

内容の要約を述べる。同一塩基の連続長を制限する制約と、GC含量を0.5の近傍に保つ制約を同時に満たしながら、一個の編集誤り（挿入、削除、置換のいずれか）を訂正できる符号化と復号を構成している。制約符号と誤り訂正符号を別々に重ねると誤り伝播と冗長の損失が生じるため、両者を一体として設計し、容量に近い符号化率を低い計算量で達成している。著者にランレングス制限符号の理論を築いたImminkが入っている点が、この論文が制約符号の系譜の直系であることを示している。

CipherFluteとの関係を述べる。CipherFluteは「隣接同音禁止という制約」と「リード・ソロモン符号」を単純に重ねている。この論文は、その重ね方が符号化率の面で最適ではないこと、そして一体化した設計が存在することを示している。

脅威の度合いは「中」である。理由を述べる。CipherFluteの符号設計を「制約符号と誤り訂正符号の単純な連接」と正確に述べたうえで、一体設計という改良の余地が既知であることに触れておけば十分である。触れずに済ませると、符号理論の側の査読者から素朴だと見なされる。

### 6. Intelligent Mail Barcode 4-State SPECIFICATION（USPS-B-3200, Rev H）

- 著者: 米国郵政公社（United States Postal Service）、承認者はStephen M. Dearing、責任技術者はJohn E. Werntz
- 掲載: USPS-B-3200 CAGE CODE 27085, Rev H, 2015年4月20日
- 確認先: https://www.legis.iowa.gov/docs/publications/SD/1034080.pdf

内容の要約を述べる。31桁までの郵便物情報を、四つの高さ状態を持つ65本のバーへ符号化する規格である。手順は明快で、まず二進化したデータの右側102ビットに対して生成多項式0xF35を用いて11ビットの巡回冗長検査（Frame Check Sequence）を計算する。次にデータを混合基数へ変換し、右端の符号語は636進、左端の符号語は659通り、中間の8個の符号語は1365進として、合計10個の符号語を得る。そして各符号語を13ビットの文字へ写すが、値が0から1286までは「13ビット中に1が5個」という表（5 of 13 Characters、1287通り）を、1287から1364までは「13ビット中に1が2個」という表（2 of 13 Characters、78通り）を引く。最後に、先に求めた11ビットの検査値の各ビットに応じて対応する文字をビット反転させることで、検査情報を記号列そのものへ埋め込んでいる。

CipherFluteとの関係を述べる。二のべき乗ではない記号数（この場合は1365や636や659）を混合基数の変換で素直に扱う実務、13という長さの記号の中で「1の個数を固定する」という定重み制約を課して読み取りの頑健性を得る発想、そして検査情報を別領域に置かずに記号列へ畳み込む工夫が、CipherFluteの13スロットの扱いと直接対応する。偶然ではあるが、記号の長さがどちらも13である点も目を引く。

脅威の度合いは「中」である。理由を述べる。CipherFluteが「13進の記号を扱う」ことや「制約を課す」ことを新規性として述べると、四十年近く運用されている郵便標準がすでに同じことをしていると指摘され得る。逆にこの規格を引用すれば、CipherFluteの記号設計が実務の標準的な作法に沿っていることの裏づけになる。

### 7. LayerCode: Optical Barcodes for 3D Printed Shapes

- 著者: Henrique Teles Maia, Dingzeyu Li, Yuan Yang, Changxi Zheng
- 掲載: ACM Transactions on Graphics, 第38巻, 第4号, 論文番号1, 17ページ, 2019年7月（SIGGRAPH 2019）
- 確認先: https://www.cs.columbia.edu/cg/layercode/LayerCode_Maia_et_al_2019_lowRez.pdf （DOIは10.1145/3306346.3322960）

内容の要約を述べる。3Dプリントの積層そのものにバーコードを埋め込む手法である。符号化は層の絶対的な厚みではなく、隣り合う二層の厚みの比の対数差で行い、比が1（同じ厚み）なら0、比がMまたは1/Mなら1とする。この差分的な表現を採ることで、曲面や撮影距離によって画像上の見かけの厚みが変わっても復号できる。ビット列の始点と終点は、通常より厚い層（実装ではN=4倍）を置くことで示している。実験で埋め込んだのは24ビット（近赤外の例では12ビット）であり、誤り訂正については「我々の符号化方式は任意の誤り訂正符号を載せられるが、本手法そのものの性能を測るために、実験では誤り訂正の冗長をあえて付けないことを選んだ」と明記し、リード・ソロモン符号などを載せられると述べるにとどめている。

CipherFluteとの関係を述べる。二点で近い。第一に、未知の全体的なずれ（LayerCodeでは撮影倍率、CipherFluteでは気温と息の強さ）を打ち消すために、絶対値ではなく比で読むという設計が同じである。CipherFluteは基準笛という一本の基準を混ぜる方式、LayerCodeは隣接層どうしの差分という方式であり、通信でいえば前者がパイロット信号、後者が差分符号化に当たる。第二に、3Dプリント造形物という同じ媒体を扱っている。

脅威の度合いは「中」である。理由を述べる。現論文はすでにLayerCodeを引用しているが、比で読むという設計の一致に触れていないなら、必ず触れて差分を述べるべきである。同時に、LayerCodeが24ビットで誤り訂正を入れていないという事実は、CipherFluteが128ビットのシードを誤り訂正つきで運ぶという主張の相対的な強さを示す最良の材料でもある。

### 8. ggwave（音による小容量データ伝送ライブラリ）

- 著者: Georgi Gerganov
- 掲載: オープンソースソフトウェア（GitHubリポジトリ）
- 確認先: https://github.com/ggerganov/ggwave

内容の要約を述べる。データを4ビットずつに分割し、ある時刻に3バイトを6つの音で送る多周波の周波数偏移変調である。4.5キロヘルツの帯域を96個の等間隔な周波数に分け、周波数の刻みは46.875ヘルツ、非超音波の場合の基準周波数は1875.000ヘルツとしている。転送速度はプロトコルにより毎秒8バイトから16バイトである。誤り訂正にはリード・ソロモン符号を用い、冗長バイト数は元データ長に応じて決めている。

CipherFluteとの関係を述べる。周波数の集合を記号の語彙とし、その上にリード・ソロモン符号を載せるという符号設計が、CipherFluteとほぼ同一である。周波数の刻み方（ggwaveは等間隔の周波数、CipherFluteは等比の半音）と、担い手が能動的な発振器か受動的な笛かという点が異なる。

脅威の度合いは「中」である。理由を述べる。「音の高さを記号にして誤り訂正符号を載せる」こと自体には先例があると示す文献なので、引用せずに新規性を主張すると危うい。CipherFluteの差分は、記号を発する主体が電源も電子部品も持たない造形物であり、記号列が物体の形として恒久的に固定されている点にある。

### 9. Polynomial Codes Over Certain Finite Fields（および二次元コードにおける非二進体の実例）

- 著者: Irving S. Reed, Gustave Solomon
- 掲載: Journal of the Society for Industrial and Applied Mathematics, 第8巻, 第2号, 300-304ページ, 1960年
- 確認先: https://epubs.siam.org/doi/10.1137/0108018 （DOIは10.1137/0108018）

内容の要約を述べる。有限体上の多項式の値を並べることで符号語を作るという構成を示した原論文である。符号語の各記号が有限体の元であるため、記号の個数は有限体の位数と一致する。この構成はSingletonの限界を等号で満たす最大距離分離符号になり、消失（どの位置が壊れたか分かる誤り）に対しては検査記号の個数と同数まで訂正できる。

CipherFluteとの関係を述べる。CipherFluteが13個または12個のスロットを記号として扱う以上、記号数と有限体の位数の関係を正しく述べる必要がある。13は素数であるから素数体GF(13)がそのまま存在し、リード・ソロモン符号を符号長12以下で組める。12は素数のべきではないため、GF(12)は存在せず、12個の記号を扱うには剰余環上の符号（Blake 1972を参照）に頼るか、より大きな体へ埋めるか、記号を組にして基数変換するかのいずれかを選ぶ必要がある。この区別を論文で明示できるかどうかが、符号理論の側の査読者に対する信頼性を左右する。

素数体を実際に採った物理媒体の例として、PDF417が挙げられる。Ynjiun P. Wangの特許（米国特許第5,243,655号、Symbol Technologies、1992年出願、1993年登録、確認先 https://patents.google.com/patent/US5243655A/en ）には「PDF417では929個の符号語の値が定義されている」と明記されており、符号語は0から928の値をとる。929は素数であるから、この符号は素数体上のリード・ソロモン符号である。安全水準は0から8まで選べ、水準6では合計126個の符号語が欠落または破壊されても復号できると述べている。

脅威の度合いは「中」である。理由を述べる。原論文そのものは背景であるが、「物理媒体の記号数に合わせて素数体を選ぶ」という実務がPDF417として三十年以上前から標準化されている事実は、CipherFluteの符号選択が新規ではなく妥当であることを示すために引用が要る。逆に引用しないまま「素数個の記号を扱った」ことを新規性として述べると、事実誤認を指摘される。

### 10. A fuzzy commitment scheme / Fuzzy Extractors: How to Generate Strong Keys from Biometrics and Other Noisy Data

- 著者: Ari Juels, Martin Wattenberg（前者）／Yevgeniy Dodis, Leonid Reyzin, Adam Smith（後者）
- 掲載: Proceedings of the 6th ACM Conference on Computer and Communications Security, 28-36ページ, 1999年／Advances in Cryptology - EUROCRYPT 2004, Lecture Notes in Computer Science, 523-540ページ, 2004年
- 確認先: https://api.crossref.org/works/10.1145/319709.319714 および https://api.crossref.org/works/10.1007/978-3-540-24676-3_31 （DOIは10.1145/319709.319714 と 10.1007/978-3-540-24676-3_31）

内容の要約を述べる。生体情報のように毎回わずかに異なる値が得られる「雑音のある物理的な測定値」から、安定した鍵を取り出すために誤り訂正符号を使う枠組みである。前者は符号語と測定値の差分だけを公開して秘密を隠すファジーコミットメントを与え、後者はそれを一般化して、秘密の推測しにくさをどれだけ失うかを定量化したファジー抽出器と安全スケッチを定式化した。

CipherFluteとの関係を述べる。CipherFluteは物理的な測定値（吹いた音の高さ）から秘密を復元するのだから、構造としてはこの枠組みそのものである。ただしCipherFluteは測定値の量子化後の記号列を秘密そのものとして扱い、公開情報として何も置かない設計であるため、ファジー抽出器の安全性解析（公開する補助情報が秘密をどれだけ漏らすか）は直接には適用されない。逆に言えば、この枠組みを引用しつつ「補助情報を公開しないため漏洩の解析が不要である」と述べると、脅威モデルの記述が締まる。

脅威の度合いは「中」である。理由を述べる。暗号の側の査読者は、雑音のある物理測定から鍵を作る話を見ればまずこの枠組みを想起する。引用がないと、関連分野の把握が不十分だと見なされる恐れがある。

### 11. QRコードの誤り訂正能力について（限界距離以上の誤り訂正、および消失同時誤り訂正によるデータ復元について）

- 著者: 齋藤圭輔, 遠藤祐介, 森井昌克
- 掲載: 電子情報通信学会技術研究報告, 第110巻, 第375号, 45-50ページ, 2011年1月
- 確認先: https://cir.nii.ac.jp/crid/1520009407096898048

内容の要約を述べる。QRコードのリード・ソロモン符号について、限界距離復号を超えた訂正、および誤りと消失を同時に扱う復号によって、規格が保証する能力を上回るデータ復元が可能であることを論じている。汚損や破損の位置が分かっている場合には消失として扱えるため、同じ検査記号の数でより多くの記号を回復できるという性質を使っている。

CipherFluteとの関係を述べる。CipherFluteでは、造形不良で詰まった笛や鳴らない笛は「読めなかった位置が分かっている」誤り、すなわち消失である。消失として扱えば訂正能力は倍になるため、この扱いを論文で明示するかどうかで必要な笛の本数が変わる。日本語で書かれた、物理媒体の二次元コードに対する消失訂正の議論として直接に参照できる。

脅威の度合いは「中」である。理由を述べる。新規性を脅かすというより、CipherFluteの誤り訂正の設計が消失を活かしていないなら弱点になるという意味で重要である。国内の査読者に対しても、日本語の先行研究を押さえている証拠になる。

### 12. Shamir's Secret-Sharing for Mnemonic Codes（SLIP-0039）の検査符号

- 著者: Pavol Rusnak, Andrew Kozlik, Ondrej Vejpustek, Tomas Susanka, Marek Palatinus, Jochen Hoenicke
- 掲載: SatoshiLabs Improvement Proposal 0039, 状態はFinal, 2017年12月18日作成
- 確認先: https://github.com/satoshilabs/slips/blob/master/slip-0039.md

内容の要約を述べる。1024語の単語表を用い、10ビットずつを一語へ写す方式である。各シェアの末尾3語（30ビット）に、GF(1024)上のリード・ソロモン符号による検査符号（RS1024）を置く。この検査符号は、最大3語に影響する誤りを必ず検出し、それを超える誤りを見逃す確率は十億分の一未満であると規定している。128ビットの秘密なら20語、256ビットなら33語となる。

CipherFluteとの関係を述べる。現論文はSLIP-39を秘密分散の規格として引用しているが、SLIP-39自体が「人間が扱う物理的な記録（紙に書いた単語列）の転記誤りに備えて、記号数に合わせた非二進のリード・ソロモン符号を置く」という設計になっている点は、CipherFluteの符号設計と同じ問題意識である。

脅威の度合いは「中」である。理由を述べる。CipherFluteがSLIP-39のシェアを笛に載せる場合、SLIP-39の検査符号とCipherFluteのリード・ソロモン符号が二重になる。この重複を整理して述べないと、冗長の見積もり（40本から49本という本数）に疑義が生じる。

### 13. Decoding the Cauzin Softstrip: a case study in extracting information from old media

- 著者: Marc Reimsbach, John Aycock
- 掲載: Archival Science, 第21巻, 第3号, 281-294ページ, 2021年
- 確認先: https://pmc.ncbi.nlm.nih.gov/articles/PMC8591774/ （DOIは10.1007/s10502-021-09358-z）

内容の要約を述べる。1980年代に雑誌の誌面へ印刷されてソフトウェアを配布した光学式データ帯「Cauzin Softstrip」の形式を解析し、復号器を実装した論文である。1ビットを白黒二個の正方形の順序（ダイビット）で表すため、記号列に直流成分が生じず、同じ色が長く続くことがない。同期のための市松模様の列があり、行ごとに奇数番目と偶数番目それぞれのパリティを持ち、加えてファイルヘッダにストリップ全体の検査和を持つ。最大容量は5500バイトであり、製造元は未検出のビット誤り率が100億分の1未満だと主張していたと引用されている。誤り訂正符号は用いておらず、検出のみである。

CipherFluteとの関係を述べる。低容量の印刷媒体において、同期のための構造、直流成分を持たない記号設計、パリティと検査和という層構造が、CipherFluteの基準笛と隣接同音禁止と誤り訂正という層構造に一対一で対応する。訂正まで行かず検出で止まっている点が、CipherFluteとの差分になる。

脅威の度合いは「中」である。理由を述べる。査読を経た考古情報学の論文として、低容量物理媒体の符号設計を具体的に記述した数少ない一次資料であり、CipherFluteの位置づけを歴史的に述べるうえで引用価値が高い。新規性そのものを崩す性質のものではない。

## 背景として押さえるべき文献

以下は脅威の度合いが「低」であり、背景や系譜として引用すれば足りるものである。すべて一次資料で書誌を確認した。

### 誤り訂正符号の原典

- Irving S. Reed, Gustave Solomon, "Polynomial Codes Over Certain Finite Fields", Journal of the Society for Industrial and Applied Mathematics, 第8巻, 第2号, 300-304ページ, 1960年。確認先は https://epubs.siam.org/doi/10.1137/0108018 である。
- R. C. Bose, D. K. Ray-Chaudhuri, "On a class of error correcting binary group codes", Information and Control, 第3巻, 第1号, 68-79ページ, 1960年。確認先は https://api.crossref.org/works/10.1016/S0019-9958(60)90287-4 である。BCH符号の原典の一方であり、bech32やcodex32が用いる符号族の出発点である。
- R. Singleton, "Maximum distance q-nary codes", IEEE Transactions on Information Theory, 第10巻, 第2号, 116-118ページ, 1964年。確認先は https://api.crossref.org/works/10.1109/TIT.1964.1053661 である。記号数がqの符号における最小距離の上界を与え、リード・ソロモン符号がこれを等号で満たすことの根拠になる。
- J. Massey, "Shift-register synthesis and BCH decoding", IEEE Transactions on Information Theory, 第15巻, 第1号, 122-127ページ, 1969年。確認先は https://api.crossref.org/works/10.1109/TIT.1969.1054260 である。実装上の復号法の原典である。
- C. E. Shannon, "A Mathematical Theory of Communication", Bell System Technical Journal, 第27巻, 第3号, 379-423ページ, 1948年。確認先は https://api.crossref.org/works/10.1002/j.1538-7305.1948.tb01338.x である。制約のある記号列の容量という概念の出発点であり、「隣り合う記号が同じであってはならない」という制約の容量が記号数から1を引いた値の対数になることも、ここでの状態遷移図による容量計算から導かれる。

### 有限体と非二進の記号の扱い

- F. J. MacWilliams, N. J. A. Sloane, "The Theory of Error-Correcting Codes", North-Holland, 1977年（ISBNは0444850090ほか）。確認先は https://openlibrary.org/search.json?q=theory+of+error-correcting+codes である。非二進符号とリード・ソロモン符号の教科書的原典である。
- Rudolf Lidl, Harald Niederreiter, "Introduction to Finite Fields and Their Applications", Cambridge University Press, 1986年（ISBNは0521307066ほか）。確認先は https://openlibrary.org/search.json?q=Introduction+to+Finite+Fields+and+Their+Applications+Lidl+Niederreiter である。位数が素数のべきに限られること、すなわちGF(12)が存在せずGF(13)が存在することの根拠を与える。
- Ian F. Blake, "Codes over certain rings", Information and Control, 第20巻, 第4号, 396-404ページ, 1972年。確認先は https://api.crossref.org/works/10.1016/S0019-9958(72)90223-9 である。記号数が素数のべきでない場合に剰余環上で符号を組む道筋を与える。CipherFluteが12個の記号を扱う設計を選ぶ場合の根拠になる。

### 制約符号（同じ記号を続けない符号、直流成分を抑える符号）

- P. A. Franaszek, "Sequence-state Methods for Run-length-limited Coding", IBM Journal of Research and Development, 第14巻, 第4号, 376-383ページ, 1970年。確認先は https://api.crossref.org/works/10.1147/rd.144.0376 である。
- D. T. Tang, L. R. Bahl, "Block codes for a class of constrained noiseless channels", Information and Control, 第17巻, 第5号, 436-461ページ, 1970年。確認先は https://api.crossref.org/works/10.1016/S0019-9958(70)90369-4 である。
- A. X. Widmer, P. A. Franaszek, "A DC-Balanced, Partitioned-Block, 8B/10B Transmission Code", IBM Journal of Research and Development, 第27巻, 第5号, 440-451ページ, 1983年。確認先は https://api.crossref.org/works/10.1147/rd.275.0440 である。現論文がすでに挙げている8B/10Bの原典であり、書誌はこの記録で確定できる。
- R. Adler, D. Coppersmith, M. Hassner, "Algorithms for sliding block codes - An application of symbolic dynamics to information theory", IEEE Transactions on Information Theory, 第29巻, 第1号, 5-22ページ, 1983年。確認先は https://api.crossref.org/works/10.1109/TIT.1983.1056597 である。制約を満たす符号器を機械的に構成する一般手法を与えた論文である。
- K. A. S. Immink, "Runlength-limited sequences", Proceedings of the IEEE, 第78巻, 第11号, 1745-1759ページ, 1990年。確認先は https://api.crossref.org/works?query.bibliographic=Runlength-limited+sequences+Immink+Proceedings+of+the+IEEE+1990 である（DOIは10.1109/5.63306）。
- Kees A. Schouhamer Immink, "Codes for Mass Data Storage Systems", Shannon Foundation Publishers, 2004年（ISBNは9789074249270）。確認先は https://openlibrary.org/search.json?q=Codes+for+Mass+Data+Storage+Systems+Immink である。記録媒体のための制約符号を体系的に扱った書籍である。
- Brian H. Marcus, Ron M. Roth, Paul H. Siegel, "An Introduction to Coding for Constrained Systems", 2001年10月版の草稿。確認先は https://cmrr-star.ucsd.edu/psiegel/book_draft/ である。制約系の容量の定義と符号器の構成を扱った標準的な講義資料である。
- "Constrained Coding and Error-Control Coding", Coding and Signal Processing for Magnetic Recording Systems 所収, 383-392ページ, CRC Press, 2004年。確認先は https://api.crossref.org/works/10.1201/9780203490310-24 である。制約符号と誤り訂正符号をどう組み合わせるかという論点そのものを扱った章である。
- J. L. Fan, A. R. Calderbank, "A modified concatenated coding scheme, with applications to magnetic data storage", IEEE Transactions on Information Theory, 第44巻, 第4号, 1565-1574ページ, 1998年。確認先は https://api.crossref.org/works?query.bibliographic=Fan+Calderbank+modified+concatenated+coding+scheme+magnetic+data+storage+IEEE+Transactions+Information+Theory である（DOIは10.1109/18.681333）。制約符号を内側に置くと誤りが伝播するという問題への対処（逆連接）を扱っている。
- Ohad Elishco, Ryan Gabrys, Eitan Yaakobi, Muriel Médard, "Repeat-Free Codes", arXiv:1909.05694, 2019年9月12日。確認先は https://arxiv.org/abs/1909.05694 である。「ある長さの部分列が二度現れない」という制約の容量と符号化を扱っており、繰り返しを禁じる制約符号の現代的な研究の例である。

### 欠落と挿入への備え

- N. J. A. Sloane, "On Single-Deletion-Correcting Codes", arXiv:math/0207197, 2002年7月22日（Codes and Designs, Ray-Chaudhuri Festschrift, Walter de Gruyter, 273-291ページ, 2002年に所収）。確認先は https://arxiv.org/abs/math/0207197 である。Varshamov・Tenengolts符号が単一の欠落を訂正することを解説した総説である。笛を一本読み飛ばした場合の備えを議論する際の入口になる。

### 検査数字の設計（記号数が10の場合）

- J. Verhoeff, "Error detecting decimal codes", MC Tracts, Centrum voor Wiskunde en Informatica, 1969年（ISBNは978-90-6196-042-3）。確認先は https://ir.cwi.nl/pub/13045 である。十進のように記号数が素数のべきでない場合に、二面体群を用いて隣接する二桁の入れ替わりまで検出する検査数字を構成した原典である。
- H. Michael Damm, "Totally anti-symmetric quasigroups for all orders n ≠ 2, 6", Discrete Mathematics, 第307巻, 第6号, 715-729ページ, 2007年。確認先は https://api.crossref.org/works/10.1016/j.disc.2006.05.033 である。任意の記号数（2と6を除く）で同様の検査数字が作れることを示している。CipherFluteが12個や13個の記号に対して簡便な検査数字を付ける場合の理論的根拠になる。

### 一次元および二次元のコードと媒体

- Norman J. Woodland, Bernard Silver, "Classifying apparatus and method", 米国特許第2,612,994号, 1949年出願, 1952年登録。確認先は https://patents.google.com/patent/US2612994A/en である。線の有無を0と1に対応させるという、光学的に読む符号の出発点である。
- Herman Hollerith, "Art of compiling statistics", 米国特許第395,782号, 1884年出願, 1889年登録。確認先は https://patents.google.com/patent/US395782A/en である。穴の有無を情報とするパンチカードの原典である。
- ECMA-10, "Data interchange on punched tape", 第2版, 1970年7月。確認先は https://ecma-international.org/publications-and-standards/standards/ecma-10/ である。紙テープの規格として書誌は確認できたが、公開されている版が画像のみの走査であるため、パリティトラックの規定そのものは本文から確認できなかった。
- Dennis G. Priddy, Robert S. Cymbalski, "Dynamically variable machine readable binary code and method for reading and producing thereof", 米国特許第4,939,354号, 1988年出願, 1990年登録。確認先は https://patents.google.com/patent/US4939354A/en である。Data Matrixの原型に当たる特許であり、この時点では代数的な誤り訂正符号ではなく、文字間に3ビット以上の差を確保することと、冗長率を0パーセントから400パーセントまで可変にすることで破損に耐える設計であった。後のECC 200でリード・ソロモン符号が導入された経緯を述べる際の対比材料になる。
- Andrew Longacre, Jr., Rob Hussey, "Two dimensional data encoding structure and symbology for use with optical readers", 米国特許第5,591,956号, 1995年出願, 1997年登録。確認先は https://patents.google.com/patent/US5591956A/en である。同一のシンボルの中で、記述子にはGF(16)（原始多項式はx^4+x+1）、メッセージ本体にはGF(1024)（原始多項式はx^10+x^3+1）と、用途ごとに異なる有限体のリード・ソロモン符号を使い分けている点が参考になる。
- ISO/IEC 18004:2015, "Information technology - Automatic identification and data capture techniques - QR Code bar code symbology specification", 第3版, 2015年2月16日発行, 117ページ。確認先は https://webstore.iec.ch/en/publication/21861 である。規格の適用範囲に「誤り訂正の規則」が含まれることを確認した。
- デンソーウェーブによるQRコードの解説ページ。確認先は https://www.qrcode.com/en/about/error_correction.html である。誤り訂正にリード・ソロモン符号を用いること、水準Mが15パーセント、水準Qが25パーセントであることを本文から確認した。水準Lと水準Hの数値は表が画像であるため確認できなかった。
- 末武陽一, 「バーコードよりも大容量, 高密度で誤り訂正機能を持つ 二次元コード「QRコード」の概要」, インターフェース, 第30巻, 第12号, 138-145ページ, 2004年12月。確認先は https://cir.nii.ac.jp/crid/1521980705549941376 である。日本語でQRコードの誤り訂正を解説した資料である。

### 紙にデータを印刷して読み戻す方式

- Twibright Optar（著者はKarel Kulhavý、1998年から2016年）。確認先は http://ronja.twibright.com/optar/ である。A4用紙一枚に200キロバイトを収める。誤り訂正にはGolay符号を用い、24ビットの符号語のうち12ビットが情報で、3ビットまでの誤りを訂正する。さらに「塵が隣接する4画素を覆うと訂正不能になる」ため、画像を24本の帯に分けて各帯に符号語の特定のビット位置だけを載せるというインターリーブを行っている。物理的にまとまった欠損に対してインターリーブで備えるという発想は、CipherFluteが造形不良の塊に備える設計と同じである。
- PaperBack（著者はOleh Yuschuk、版は1.10、2007年）。確認先は https://www.ollydbg.de/Paperbak/ である。600dpiのA4用紙一枚に最大500,000バイトを収め、誤り訂正にリード・ソロモン符号を用いる。加えて「冗長1対5」のように、連続する5個のデータブロックのうち1個が完全に読めなくても復元できる冗長度を設定できる。
- D. L. Hecht, "Printed embedded data graphical user interfaces", Computer, 第34巻, 第3号, 47-55ページ, 2001年。確認先は https://api.crossref.org/works/10.1109/2.910893 である。Xerox社のDataGlyphsに関する解説であり、印刷面に人間には模様に見える形でデータを埋め込む手法を扱っている。

### 超長期保存を狙った媒体

- The Rosetta Disk（Long Now Foundation）。確認先は https://rosettaproject.org/disk/concept/ である。直径3インチのディスクに1,500以上の言語について13,000ページ以上を微細に彫り込んでいる。各ページは「デジタルではなく物理的な像」であるため、形式や機器への依存がなく、光学的な拡大だけで読める。誤り訂正符号は一切使っていない。CipherFluteが「デジタルの符号を物理に載せる」立場であるのに対し、こちらは「符号化そのものを避ける」立場であり、対比として有効である。
- Memory of Mankind（オーストリア、ハルシュタットの岩塩坑）。確認先は https://www.memory-of-mankind.com/ である。セラミックのタブレットに人間が直接読める形で情報を焼き付け、100万年の保存を目標としている。こちらも誤り訂正符号を使わない立場である。
- GitHub Arctic Code Vault。確認先は https://archiveprogram.github.com/arctic-vault/ である。2020年2月2日時点の公開リポジトリ21テラバイトを186巻のフィルムに収めており、データは「QRとして符号化され、圧縮されて」いる。各巻に人間が読める索引と復元手順の手引きを添えている。誤り訂正の具体的な方式はこのページからは確認できなかった。
- Jingyu Zhang, Mindaugas Gecevičius, Martynas Beresna, Peter G. Kazansky, "Seemingly Unlimited Lifetime Data Storage in Nanostructured Glass", Physical Review Letters, 第112巻, 第3号, 論文番号033901, 2014年。確認先は https://api.crossref.org/works/10.1103/PhysRevLett.112.033901 である。ガラス内部の微細構造に情報を書く方式であり、超長期保存の物理媒体として引用される。

### DNAへのデータ保存（本文で扱わなかったもの）

- George M. Church, Yuan Gao, Sriram Kosuri, "Next-Generation Digital Information Storage in DNA", Science, 第337巻, 第6102号, 1628ページ, 2012年。確認先は https://api.crossref.org/works/10.1126/science.1226355 である。
- Yaniv Erlich, Dina Zielinski, "DNA Fountain enables a robust and efficient storage architecture", Science, 第355巻, 第6328号, 950-954ページ, 2017年。確認先は https://api.crossref.org/works/10.1126/science.aaj2038 である。噴水符号を用い、生成した配列のうち制約を満たすものだけを選別する方式である。
- Meinolf Blawat, Klaus Gaedke, Ingo Hütter, Xiao-Ming Chen, Brian Turczyk, Samuel Inverso, Benjamin W. Pruitt, George M. Church, "Forward Error Correction for DNA Data Storage", Procedia Computer Science, 第80巻, 1011-1022ページ, 2016年。確認先は https://api.crossref.org/works/10.1016/j.procs.2016.05.398 である。
- Reinhard Heckel, Gediminas Mikutis, Robert N. Grass, "A Characterization of the DNA Data Storage Channel", arXiv:1803.03322, 2018年3月8日。確認先は https://arxiv.org/abs/1803.03322 である。物理媒体の誤りの性質を測って符号設計に反映するという方法論の例である。

### 暗号資産のシードに関する符号（本文で扱わなかったもの）

- BIP-39, "Mnemonic code for generating deterministic keys"（Marek Palatinus, Pavol Rusnak, Aaron Voisine, Sean Bowe, 2013年9月10日）。確認先は https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki である。2048語の単語表を用い、エントロピー32ビットにつき1ビットの検査符号をSHA-256の先頭ビットから作る。規格自身が「検査符号は短く、無作為な誤りを捕まえる確率は控えめである（256回に1回は見逃す）」と欠点を認めている。CipherFluteが誤り訂正を自前で持つ理由づけになる。
- BIP-173, "Base32 address format for native v0-16 witness outputs"（Pieter Wuille, Greg Maxwell, 2017年3月20日）。確認先は https://github.com/bitcoin/bips/blob/master/bip-0173.mediawiki である。GF(32)上のBCH符号を6文字（30ビット）用い、最大4文字に影響する誤りを必ず検出する。記号集合は視覚的に紛らわしい文字（1、i、o、b）を除いて選んでいる。人間が転記する物理媒体のための符号設計の好例である。

### 造形物への情報埋め込み（符号の観点から）

- Canran Wang, Jinwen Wang, Mi Zhou, Vinh Pham, Senyue Hao, Chao Zhou, Ning Zhang, Netanel Raviv, "Secure Information Embedding in Forensic 3D Fingerprinting", arXiv:2403.04918, 2024年3月7日投稿, 2025年2月3日改訂。確認先は https://arxiv.org/abs/2403.04918 である。3Dプリント物へ法科学的な識別情報を埋め込む枠組みであり、物体を割られて一部を隠されても復元できる「破断耐性」と「欠損耐性」を符号理論的な構成で与えると述べている。物理的な分割に対する耐性を符号で担保するという問題設定がCipherFluteのカードの分割と近い。

## 未検証のまま残ったもの

以下は実在や書誌情報を確認しきれなかったものである。論文に書く場合は、確認するまで数値や書誌を書かないほうがよい。

- ISO/IEC 16022（Data Matrix）の正式な題名、版、および「ECC 200では記号の30パーセントの破損まで復元できる」という一般に流布している数値。ISOのページとANSIのページはいずれもアクセスが拒否され（HTTP 403）、確認できなかった。原型の特許（米国特許第4,939,354号）は確認できたが、そこにはリード・ソロモン符号の記述がない。
- ISO/IEC 15438（PDF417）およびISO/IEC 24778（Aztec Code）の正式な題名と版。規格そのものには到達できなかった。PDF417が929個の符号語を持つことは特許から確認できたが、規格の条文からは確認していない。Aztec Codeの既定の誤り訂正率が23パーセントであるという記述も確認できなかった。
- 米国特許第5,591,956号がAztec Codeそのものの特許であるという対応関係。特許本文には「Aztec」という語が現れないため、名称の対応は確認できていない。有限体の使い分け（GF(16)とGF(1024)）は本文で確認した。
- QRコードの誤り訂正水準Lが約7パーセント、水準Hが約30パーセントであるという数値。デンソーウェーブの解説ページでは該当箇所が画像の表になっており、本文からは水準Mの15パーセントと水準Qの25パーセントしか確認できなかった。
- Grassらの2015年の論文が有限体GF(47)上のリード・ソロモン符号を用いているという広く引用される記述。出版社のページは有料（HTTP 402）で本文に到達できず、Europe PMCの記録からは要旨のみを確認した。当該の記述は補足資料にあるとみられる。
- ECMA-10が定める紙テープのパリティトラックの具体的な規定。公開されている第2版のPDFが走査画像のみで、文字として抽出できなかった。
- A. Hocquenghem, "Codes correcteurs d'erreurs", Chiffres, 1959年。BCH符号のもう一方の原典であるが、Crossrefにも出版社のページにも到達できなかった。
- R. R. Varshamov, G. M. Tenengolts の1965年の原論文、および V. I. Levenshtein の欠落訂正符号に関する1965年から1966年の原論文。いずれもロシア語の一次資料に到達できず、Sloaneの2002年の総説を通じてのみ確認した。
- Brian H. Marcus, Ron M. Roth, Paul H. Siegel による Handbook of Coding Theory（Elsevier, 1998年）所収の章「Constrained Systems and Coding for Recording Channels」。2001年版の講義用草稿は確認できたが、書籍所収版の巻号とページは確認できなかった。
- W. G. Bliss による逆連接（reverse concatenation）の原典とされる IBM Technical Disclosure Bulletin の記事（1981年）。到達できなかった。代わりに Fan と Calderbank の1998年の論文を確認した。
- Stephen B. Wicker, Vijay K. Bhargava 編 "Reed-Solomon Codes and Their Applications"（IEEE Press, 1994年）。Open Libraryでは見つからなかった。
- Piql社のpiqlFilmが用いる符号化方式と誤り訂正の具体。GitHub Arctic Code Vaultのページからは「QRとして符号化され圧縮されている」ことしか確認できなかった。
- Cauzin Softstripの製造元による原規格文書および関連特許の番号。査読論文（Reimsbach and Aycock 2021）を通じてのみ形式を確認した。

## この切り口で見つからなかったこと

新規性の主張の根拠になるため、探して存在しなかったと言えることを丁寧に書く。

第一に、音の高さ（共鳴周波数）を記号の語彙とし、その記号列に誤り訂正符号を載せ、しかもその記号列が電源を持たない受動的な造形物の形状として固定されている、という組み合わせの先行研究は見つからなかった。Crossrefに対して3Dプリント、音響タグ、共鳴周波数、誤り訂正符号を組み合わせた検索を行ったが、関連する文献は返らなかった（確認先は https://api.crossref.org/works?query.bibliographic=3D+printed+acoustic+tag+resonant+frequency+encode+data+error+correcting+code である）。音の高さを記号にして誤り訂正符号を載せる例（ggwave）は存在するが、それは能動的な発振器による実時間の伝送であり、物体に固定された記録ではない。逆に、3Dプリント物に符号を埋め込む例（LayerCodeなど）は存在するが、そちらは光学的に読むものであり、しかも誤り訂正符号を実際には適用していない。

第二に、3Dプリントで造形した物体に、実用的な鍵長（128ビット以上）の秘密を誤り訂正符号つきで格納した実装例は見つからなかった。LayerCodeが埋め込んだのは24ビット（近赤外の実装では12ビット）であり、論文中で誤り訂正の冗長を意図的に付けていないと明言している。すなわち「造形物に載せる情報量」と「誤り訂正の実装」の両方を同時に満たした先行例は、調べた範囲では存在しない。

第三に、記号数が13または12という、二のべき乗でも典型的な有限体の位数でもない語彙に対して、隣接同音禁止の制約とリード・ソロモン符号を同時に適用した設計を、物理媒体の文脈で明示的に述べた文献は見つからなかった。個々の要素はすべて先例がある。混合基数と定重み制約はIntelligent Mail Barcodeにあり、素数体上のリード・ソロモン符号はPDF417にあり、隣接記号を必ず変える制約はGoldmanらのDNA符号にあり、制約符号と誤り訂正符号の一体設計はNguyenらの論文にある。しかしこれらを一つの物理媒体の上でまとめた記述は見当たらなかった。したがってCipherFluteの符号設計は、要素技術としては既知の部品の組み合わせであると正直に述べたうえで、その組み合わせが音響的な受動媒体という新しい文脈で初めて実装された点に主張を置くのが妥当である。

第四に、日本語文献については、二次元コードの誤り訂正に関する研究（齋藤らの消失訂正、末武の解説など）は存在するが、物理造形物の音響的な符号化と誤り訂正を扱ったものはCiNii Researchの検索では見つからなかった。なお「ランレングス制限符号」という語ではCiNii Researchで0件であり、日本語では「変調符号」「記録符号」という語で光ディスクや磁気記録の文脈に現れることを確認した。

第五に、基準となる記号を一つ混ぜて全体のずれを打ち消すという手法（CipherFluteの基準笛）について、物理媒体の符号化の文脈で明示的に「パイロット記号」と呼んで扱った先行研究は見つからなかった。近い設計としてLayerCodeの隣接層の比による差分符号化があるが、これは一つの基準を混ぜる方式ではなく、隣接する記号どうしの差をとる方式である。両者は雑音への強さと符号化率の面で性質が異なるため、CipherFluteが差分符号化ではなく基準笛を選んだ理由を述べると差分が明確になる。

## 調べ残した穴

時間の都合で追い切れなかった方向を挙げる。

第一に、ISO/IEC 16022、ISO/IEC 15438、ISO/IEC 24778の各規格の条文そのものに到達できなかった。二次元コードの誤り訂正能力を数値で述べたい場合は、図書館などを通じて規格本体を確認する必要がある。特にData MatrixのECC 200が規定する訂正能力は、CipherFluteの冗長率を比較するうえで有用な数値になるはずである。

第二に、Grassらの2015年の論文の補足資料を確認できなかったため、DNA保存で用いられた有限体の位数と内符号・外符号の構成を一次資料で押さえられなかった。CipherFluteが「素数体上のリード・ソロモン符号を物理媒体で使った先例」として引用するなら、この確認は必須である。

第三に、CD-ROMやDVDが用いるCross-Interleaved Reed-Solomon Codeについて、Imminkによる一次資料に到達できなかった。制約符号（EFM）と誤り訂正符号（リード・ソロモン符号）とインターリーブを三層に重ねる設計は、CipherFluteの層構造の最も整った先例であり、押さえておく価値が高い。IEEE Transactions on Consumer ElectronicsのEFMに関する論文（DOIは10.1109/30.628663）は書誌のみ確認したが、本文は読んでいない。

第四に、マイクロフィルムや石版の規格（ISO 18901など）と、Piql社のフィルムの符号化方式について、技術的な一次資料に到達できなかった。超長期保存の媒体が誤り訂正をどう扱っているか（あるいは扱わずに人間可読性に賭けているか）を体系的に述べるには、この方向の追加調査が要る。

第五に、被引用をたどる作業を十分に行えなかった。特にGoldmanらの2013年の論文と、Elishcoらの繰り返し禁止符号の被引用一覧をたどれば、「隣接記号を必ず変える」という制約に関する最新の理論的成果（達成可能な符号化率の上限など）が得られるはずである。CipherFluteが記号数13から実効12へ落とすことによる損失（1本あたり約0.115ビット）が理論的に最適かどうかを述べたいなら、この方向が必要である。

第六に、日本語文献の探索が二次元コードに偏った。情報処理学会電子図書館とJ-STAGEを直接検索していないため、記録媒体の変調符号や、物体への情報埋め込みに関する国内の解説記事を取りこぼしている可能性がある。
