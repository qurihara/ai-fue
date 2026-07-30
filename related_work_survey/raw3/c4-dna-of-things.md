# 反例の検証（4）DNA-of-things と Hollow Nickel 事件

本稿は、CipherFlute の新規性の主張に対して別の評価者が挙げた二つの反例を、一次資料に当たって検証した記録である。
検証したのは次の二点である。第一に、Nature Biotechnology に載った DNA-of-things の論文が実在し、
評価者が述べた数字と用途の記述が本当に書かれているかどうかである。
第二に、アメリカ連邦捜査局の Hollow Nickel 事件について、評価者が述べた事実関係が公式資料で裏付けられるかどうかである。

検証の結論を先に述べる。**二つの反例はいずれも本物である。**
とくに DNA-of-things は、「100ビットを超える秘密の値を電源なしの物体に埋め、日用品に偽装した先行研究は存在しない」
という書き方をそのまま崩す。この書き方は撤回するほかない。
ただし、崩れるのは「先行例がない」という部分であって、CipherFlute の中身のすべてではない。
何が残るかは末尾の節に書いた。

---

## 1. 対象論文の書誌の確定

評価者が挙げた論文は実在する。書誌は次のとおりに確定した。

- 著者: Julian Koch, Silvan Gantenbein, Kunal Masania, Wendelin J. Stark, Yaniv Erlich, Robert N. Grass（6名）
- 題名: "A DNA-of-things storage architecture to create materials with embedded memory"
- 掲載: Nature Biotechnology, 第38巻, 第1号, 39–43頁
- 年: 印刷版は2020年1月号であり、オンライン先行公開は2019年12月9日である
- 識別子: DOI 10.1038/s41587-019-0356-z、PubMed 識別番号 31819259

確認先は次の三つである。
Crossref の登録書誌 https://api.crossref.org/works/10.1038/s41587-019-0356-z 、
PubMed の書誌と抄録 https://pubmed.ncbi.nlm.nih.gov/31819259/ 、
Europe PMC の書誌と抄録 https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:%2210.1038/s41587-019-0356-z%22&resultType=core&format=json 。
抄録の原文は、アメリカ国立生物工学情報センターの efetch から取得したテキストと Europe PMC の abstractText の両方で同一であることを照合した。

補足として次の点を確認した。
Erlich と Grass の二名が「これらの著者は等しく貢献した」と注記された責任著者である。
所属は、Koch と Stark と Grass がチューリッヒ工科大学の Functional Materials Laboratory、
Gantenbein と Masania が同大学の Complex Materials、Erlich がイスラエルの Erlich Lab LLC である。
Crossref の登録によれば参考文献は25件であり、被引用は181件である（2026年7月28日時点の Crossref の集計）。
Europe PMC は107件、Semantic Scholar は174件を数えており、集計元によって幅がある。
Unpaywall に問い合わせたところ oa_status は closed であり、著者公開版も機関リポジトリ版も存在しない
（確認先 https://api.unpaywall.org/v2/10.1038/s41587-019-0356-z ）。
したがって本文全体を読むことはできず、以下では抄録の原文、出版社ページで公開されている図の見出しと謝辞と参考文献、
およびチューリッヒ工科大学の公式プレスリリースを根拠とする。

---

## 2. 45キロバイトと1.4メガバイトという数字の検証

**両方とも、論文の抄録に原文どおり書かれている。** 該当箇所を引用する。

> First, we applied DoT to three-dimensionally print a Stanford Bunny9 that contained a 45 kB digital DNA blueprint for its synthesis.

> To test the scalability of DoT, we stored a 1.4 MB video in DNA in plexiglass spectacle lenses and retrieved it by excising a tiny piece of the plexiglass and sequencing the embedded DNA.

意味を日本語で述べる。前者は、スタンフォードバニーという3次元形状のベンチマークモデルを3次元印刷し、
その造形物の中に、自分自身を合成するための45キロバイトの設計図をDNAとして持たせたという報告である。
後者は、方式の規模の限界を試すために、1.4メガバイトの動画をDNAに符号化してアクリル樹脂製の眼鏡レンズに収め、
アクリルの小片を切り出して埋め込まれたDNAを配列決定することで取り出したという報告である。

45キロバイトは約36万ビットであり、1.4メガバイトは約1120万ビットである。
いずれも「100ビットを超える」という水準を4桁から5桁上回る。

数字について一点だけ食い違いを記録しておく。
チューリッヒ工科大学の公式プレスリリースは、うさぎに入っているデータ量を
"contains the instructions (about 100 kilobytes' worth of data) for printing the object" と書いており、約100キロバイトとしている
（確認先 https://ethz.ch/en/news-and-events/eth-news/news/2019/12/dna-of-things-storing-data-in-everyday-objects.html ）。
論文の抄録は45キロバイトである。両者が食い違う理由は、圧縮の前後を指しているのか、
それとも設計図ファイルの形式が異なるのかのいずれかだと推測されるが、
本文を読めないので断定はできない。引用するときは論文本体の45キロバイトを採るべきである。

なお、うさぎのほうは装飾品であって日用品とは言いにくいが、眼鏡のほうは疑いなく日用品である。
出版社ページで公開されている図3の見出しは "A video is concealed in reading glasses."（動画は老眼鏡に隠されている）であり、
論文自身が「隠す」という語を使っている。

---

## 3. 読み出しに何が必要か

**読み出しは破壊的である。** 抄録の原文が
"retrieved it by excising a tiny piece of the plexiglass and sequencing the embedded DNA" と述べているとおり、
眼鏡レンズのアクリルから小片を切り出す操作が要る。プレスリリースも、うさぎについて
"retrieving the printing instructions from a small part of the rabbit"（うさぎの小さな一部分から印刷指示を取り出す）と書いている。
物体そのものを削らずに読むことはできない。

**専門の設備が要る。** 出版社ページの謝辞に
"The authors thank the Christen group at ETH for giving access to the iSeq 100 sequencing device."
（iSeq 100 という配列決定装置を使わせてくれた同大学の Christen グループに謝意を表する）とあり、
イルミナ社の次世代シーケンサ iSeq 100 を用いたことが確認できる。
また、供給情報の図の見出しに定量ポリメラーゼ連鎖反応の閾値サイクルに関する図があること、
参考文献に Luby の LT 符号、PEAR というイルミナ用のペアエンド読み結合ツール、MUSCLE という多重配列整列ツールが挙がっていることから、
読み出しは、シリカ粒子からのDNAの回収、増幅、配列決定、計算機上での復号という一連の分子生物学の工程で成り立っている。
誤り訂正には Erlich らの DNA Fountain が使われており、実装が
https://github.com/TeamErlich/dna-fountain で公開されている。
配列決定の生データは欧州ヌクレオチドアーカイブに登録番号 PRJEB35217 で登録されている。

**時間については原典で確認できなかった。** 読み出しに何時間あるいは何日かかったかを述べた記述は、
抄録にも、出版社ページで公開されている範囲にも、プレスリリースにも見つからなかった。
本文と供給情報を読めないため、ここは「確認できなかった」と書くほかない。

**費用については書き込み側の数字だけが分かった。** プレスリリースに
"Translating a 3D-printing file like the one stored in the plastic rabbit's DNA costs around 2,000 Swiss francs"
（うさぎに入っているような3次元印刷ファイルをDNAに翻訳するには約2000スイスフランかかる）とあり、
その大部分がDNA分子の合成に充てられると述べている。これは書き込みの費用であって、読み出しの費用ではない。

---

## 4. 著者自身が日用品へのステガノグラフィを用途に挙げているか

**挙げている。** 抄録の最後から二番目の文が該当する。原文を引用する。

> DoT could be applied to store electronic health records in medical implants, to hide data in everyday objects (steganography) and to manufacture objects containing their own blueprint.

日本語で述べると、この方式は、医療用の埋め込み機器に電子診療記録を収めること、
日用品にデータを隠すこと（すなわちステガノグラフィ）、
自身の設計図を含む物体を製造することに応用しうる、という文である。
括弧の中の steganography は著者自身が置いた語であり、評価者の解釈ではない。

論文がステガノグラフィの文脈を意識していることは、参考文献からも裏付けられる。
出版社ページの参考文献一覧には、Clelland, Risca, Bancroft の
"Hiding messages in DNA microdots", Nature 第399巻 533–534頁 1999年（DOI 10.1038/21092、Crossref で照合した）と、
Schmeh, K. の "Versteckte Botschaften: Die faszinierende Geschichte der Steganografie"（Heise Verlag, 2017年）という
ステガノグラフィの歴史を扱った書籍が入っている。

プレスリリースはさらに直截である。原文を二つ引用する。

> A further application of the technology would be to conceal information in everyday objects, a technique experts refer to as steganography.

> It would be no problem to take a pair of glasses like this through airport security and thus transport information from one place to another undetected.

後者は Erlich の発言として引かれており、こうした眼鏡なら空港の保安検査を問題なく通り抜けられ、
気づかれずに情報をある場所から別の場所へ運べる、という趣旨である。
偽装した日用品で秘密を運ぶという用途を、著者本人が名指しで述べている。
デモンストレーションの題材として、ワルシャワ・ゲットーの秘密文書がミルク缶に隠されて残された史実
（現在は国際連合教育科学文化機関の世界の記憶に登録されている）を選び、
その記録映画を眼鏡レンズに収めたことも述べられている。

---

## 5. この論文を引用している後続研究のうち、日用品への秘密の埋め込みに関わるもの

Semantic Scholar の被引用一覧（174件）を機械的に絞り込み、Crossref と Europe PMC で書誌を照合した。
関係が深いものを挙げる。

- Fahim Farzadfard, "DNA storage in everyday objects", Nature Biotechnology, 第38巻, 第1号, 31–32頁, 2019年12月18日公開, DOI 10.1038/s41587-019-0376-8。
  確認先 https://api.crossref.org/works/10.1038/s41587-019-0376-8 。同じ号に載った解説記事であり、
  題名そのものが「日用品のなかのDNA記憶」である。この分野が当該論文を「日用品への埋め込み」として受け取ったことの証拠になる。
  抄録は登録されていない。

- Cecilia Wetzl, Diana Soukarie, Jokin Yeregui Elosua, Ibon Santiago, "Integrating DNA-Based Memory in Water-Resistant Electrospun Polymer Fibers for Nondestructive Data Retrieval", ACS Applied Materials & Interfaces, 第17巻, 第32号, 46089–46098頁, 2025年, DOI 10.1021/acsami.5c06554。
  確認先 https://api.crossref.org/works/10.1021/acsami.5c06554 および Europe PMC の抄録。
  DNA-of-things の弱点である破壊的読み出しを正面から扱った後続である。抄録に
  "DNA/cellulose acetate fiber composites are true nondestructive readout memory: repeated access to messages stored in fibers is afforded without damaging the integrity of fibers or DNA."
  とあり、酢酸セルロース繊維の複合材では、繊維もDNAも損なわずに繰り返し読めると主張している。
  ただし読み出しに配列決定が要る点は変わらない。

- Diana Soukarie, Lluis Nocete, Alexander M. Bittner, Ibon Santiago, "DNA data storage in electrospun and melt-electrowritten composite nucleic acid-polymer fibers", Materials Today Bio, 第24巻, 論文番号 100900, 2024年2月, DOI 10.1016/j.mtbio.2023.100900。
  確認先 https://api.crossref.org/works/10.1016/j.mtbio.2023.100900 。上の論文の前段にあたる同じ研究室の仕事である。

- Hanna Matusik, Mina Konakovic Lukovic, "ObjGen: Constructing Objects with Digital Genetic Information", CHI Conference on Human Factors in Computing Systems Extended Abstracts 2023, 論文番号219, 全8頁, DOI 10.1145/3544549.3585781。
  確認先 https://api.crossref.org/works/10.1145/3544549.3585781 および dblp https://dblp.org/rec/conf/chi/MatusikK23 。
  ヒューマンコンピュータインタラクションの会議の予稿であり、物体が自身の生成情報を持つという発想を扱っている。
  本文を取得できなかったため、日用品への秘密の埋め込みをどこまで扱っているかは確認できなかった。

- Anne M. Luescher, Andreas L. Gimpel, Wendelin J. Stark, Reinhard Heckel, Robert N. Grass, "Chemical unclonable functions based on operable random DNA pools", Nature Communications, 第15巻, 2024年4月5日, DOI 10.1038/s41467-024-47187-7。
  確認先 https://api.crossref.org/works/10.1038/s41467-024-47187-7 。
  同じ Grass のグループによる後続で、物体に結びついた暗号（抄録の語では object-bound cryptography）を扱っている。
  複製困難関数を DNA プールで実現する試みであり、CipherFlute の複製容易性についての宣言と対比できる。

- Hang Zhou, Weiming Zhang, Kejiang Chen, Weixiang Li, Nenghai Yu, "Three-Dimensional Mesh Steganography and Steganalysis: A Review", IEEE Transactions on Visualization and Computer Graphics, 第28巻, 第12号, 5006–5025頁, 2022年, DOI 10.1109/TVCG.2021.3075136。
  確認先 https://api.crossref.org/works/10.1109/tvcg.2021.3075136 。
  こちらは3次元メッシュという電子データのなかに情報を隠す話であって、物理的な造形物への埋め込みではない。
  区別して扱う必要がある。

---

## 6. Hollow Nickel 事件の一次資料の検証

### 6.1 確定した事実関係

アメリカ連邦捜査局の公式ページ「Hollow Nickel/Rudolf Abel」を取得した。
本体の www.fbi.gov は自動取得を拒むため、インターネットアーカイブに保存された同一ページ
（2024年1月11日採取、https://web.archive.org/web/20240111043945/https://www.fbi.gov/history/famous-cases/hollow-nickel-rudolph-abel 、
原本は https://www.fbi.gov/history/famous-cases/hollow-nickel-rudolph-abel ）から全文を読んだ。
確認できた事実を時系列で述べる。

- 1953年6月22日（月）の夕方、ブルックリンの Foster Avenue 3403番地の集合住宅で、
  「Brooklyn Eagle」紙の配達少年が集金した硬貨のうち5セント硬貨を落としたところ、硬貨が二つに割れた。
  中には数字の並びを写したとみられる微小な写真が入っていた。
- 1953年6月24日、ニューヨーク市警の刑事が別件の打ち合わせの席で連邦捜査局の捜査官にこの話をし、
  少年から硬貨と写真を受け取って連邦捜査局に引き渡した。
- 硬貨の中身について、公式ページは
  "the microphotograph appeared to portray nothing more then ten columns of typewritten numbers. There was five digits in each number and 21 numbers in most columns."
  と書いている。すなわちタイプ打ちの数字が10列あり、1個の数は5桁で、多くの列に21個の数が並んでいた。
  単純に掛けると1050桁になる。10進の1桁は約3.32ビットに相当するので、情報量はおよそ3500ビットである
  （この換算は本稿の筆者が行ったものであって、連邦捜査局が述べた数字ではない）。
- 1953年6月26日、ワシントンの連邦捜査局研究所が硬貨を受領した。
  表面は1948年のジェファーソン5セント硬貨であり、"TRUST" の文字の "R" に微小な穴が開けられていて、
  細い針などを差し込めば開けられるようになっていた。裏面は1942年から1945年のあいだに鋳造された別の硬貨から作られており、
  第二次世界大戦中のニッケル不足のため銅と銀の合金であった。
- 1953年から1957年まで、暗号は解けなかった。使われたタイプライターも特定できず、外国製と推定された。
- 1957年5月、ソビエト国家保安委員会の中佐 Reino Hayhanen がパリのアメリカ大使館に亡命を申し出た。
  5月10日にニューヨークへ戻り、連邦捜査局の聴取を受けた。
- 1957年5月15日、プロスペクト公園のコンクリート階段の穴から、長さ約2インチ、直径約4分の1インチの中空のボルトが見つかり、
  タイプ打ちの伝言が入っていた。
- 1957年5月17日、ピークスキルの Hayhanen 宅から中空のフィンランド50マルッカ硬貨が見つかった。
  こちらも "Tasavalta" の最初の "a" に小さな穴が開けられており、ジェファーソン5セント硬貨と作りがよく似ていた。
- Hayhanen が提供した暗号の知識を研究所が微小写真に適用し、1957年6月3日までに全文が判明した。
  内容は、無事の到着を祝い、偽装のための資金3000（現地通貨）を送ること、
  自分自身の情報を1通の暗号文にまとめて送らないことなどを指示する、番号付きの5項目の通信文であった。
- Hayhanen 宅の中空の鋼片からは1インチ角に満たないマイクロフィルムが見つかり、
  暗号名 "Quebec" が陸軍軍曹 Roy Rhodes であることが判明した。Rhodes は軍法会議で重労働5年を科された。
- 1957年6月21日、"Mark" と呼ばれていた人物が逮捕された。本人は Rudolf Ivanovich Abel と名乗った。
  写真スタジオとホテルの部屋には
  "shortwave radios, cipher pads, cameras and film for producing microdots, a hollow shaving brush, cuff links, and numerous other 'trick' containers"
  すなわち短波無線機、暗号表、マイクロドット作成用のカメラとフィルム、中空のひげそり用ブラシ、カフスボタン、
  その他多数の「仕掛け」容器があった。
- 1957年10月25日に有罪の評決が出て、11月15日に Mortimer W. Byers 判事が3件の訴因に対して
  30年、10年と2000ドル、5年と1000ドルを言い渡した。3件は同時に執行される。
- 1960年3月28日、連邦最高裁が5対4で有罪を支持した。
- 1962年2月10日、Abel はソビエト連邦に捕らえられていた U-2 偵察機の操縦士 Francis Gary Powers と交換された。

### 6.2 評価者の記述との照合

評価者は「硬貨、鉛筆、電池、ねじなどに暗号文やマイクロフィルムを隠した実例がある」と述べた。
**この記述は連邦捜査局の公式ページで裏付けられる。** 該当箇所を引用する。

> Among the items he had been supplied by the Soviets were hollow pens, pencils, screws, batteries, and coins—in some instances magnetized so they would adhere to metal objects.

すなわち、Hayhanen がソビエト側から支給された物品には、中空のペン、鉛筆、ねじ、電池、硬貨があり、
なかには金属物に貼り付くよう磁化されたものもあった、と Hayhanen 自身が供述している。
評価者が挙げた4種類のうち3種類（硬貨、鉛筆、電池、ねじのうち鉛筆・電池・ねじ）はこの一文にそのまま現れ、硬貨は事件の中心そのものである。

電池については、連邦捜査局の別の公式ページに実物の説明がある。
「Rudolf Abel and the Hollow Nickel Case」
（原本 https://www.fbi.gov/history/artifacts/rudolph-abel-hollow-nickel-case 、
保存版 https://web.archive.org/web/2024/https://www.fbi.gov/history/artifacts/rudolph-abel-hollow-nickel-case ）は、
展示品について
"This piece of espionage equipment is a flashlight battery hollowed out to create a container for the concealment of larger objects like a roll of film."
と書いている。懐中電灯用の電池をくり抜いて、フィルムのロールのような大きめの物を隠す容器にしたものである。

### 6.3 訂正すべき細部が二つある

第一に、Hollow Nickel の中身は**マイクロフィルムではなく微小写真である**。
公式ページは一貫して microphotograph という語を使っており、数字の列を写した紙焼きに近いものを指す。
マイクロフィルムが登場するのは別の物件であり、Hayhanen 宅の中空の鋼片から出た1インチ角未満のもの、
および上に引いた中空の懐中電灯用電池の想定用途である。
「硬貨にマイクロフィルムを隠した」と書くと不正確になる。

第二に、刑期について連邦捜査局の二つのページが食い違う。
「Famous Cases」のページは30年・10年・5年の3件を同時執行と明記し、罰金を合計3000ドルとしている。
一方「Artifacts」のページは "sentenced to 45 years of imprisonment and a $3,000 fine" と書いており、
3件を単純に足した45年としている。同時執行であれば実際に服する上限は30年である。
引用するなら、内訳を明記している「Famous Cases」のページを採るべきである。

### 6.4 学術論文の関連研究で引用できるか

引用できる。ただし二段構えにするのがよい。

事実関係の典拠としては、アメリカ連邦捜査局の公式ページを、政府機関のウェブ資源として閲覧日付を添えて引用すればよい。
アメリカ司法省の公式サイトであり、一次資料として扱って差し支えない。
本稿の検証ではインターネットアーカイブの保存版を用いたので、参考文献には原本と保存版の両方を書くのが誠実である。

査読を経た文献を並べたい場合は、この事件で使われた暗号を扱った次の論文がある。

- Jozef Kollár, "Soviet VIC Cipher: No Respector of Kerckoff's Principles", Cryptologia, 第40巻, 第1号, 33–48頁, 2016年（オンライン先行公開は2015年7月16日）, DOI 10.1080/01611194.2015.1028679。
  確認先 https://api.crossref.org/works/10.1080/01611194.2015.1028679 。
  出版社サイトが取得を拒んだため抄録の原文は確認できなかったが、
  出版社である Taylor & Francis の報道発表を伝える複数の記事が、この論文が扱う鍵に Hayhanen の個人情報が含まれることを述べている。
  なお題名の "Respector" と "Kerckoff" は Crossref に登録されたとおりの綴りであり、本稿では原綴りのままとした。

---

## 7. 判定

### 7.1 DNA-of-things についての判定

**反例は正しい。** 論文は実在し、著者・題名・掲載誌・巻号・頁・年はすべて確定した。
45キロバイトと1.4メガバイトという数字は抄録に原文どおり書かれている。
日用品へのステガノグラフィという用途は、抄録の本文と図3の見出しとプレスリリースの三箇所で、著者自身の言葉として確認できた。

したがって「100ビットを超える秘密の値を電源なしの物体に埋め、日用品に偽装した先行研究は存在しない」という主張は、**成り立たない。**
老眼鏡という日用品に、電源も電子部品も持たない形で約1120万ビットが埋められており、
著者はそれを空港の保安検査を通り抜けさせられると明言している。
この一文をこのまま論文に書けば、査読者に一撃で崩される。

「符号を担体の外観にまったく現さずに機械可読に保てる」という主張についても、
DNA-of-things はまさにそれを達成している。外観にはなにも現れず、材料の中に情報が溶けている。
「この隠蔽と可読性の両立は光学符号には原理的に得られない構造的な差である」という文は、
比較対象を光学符号に限れば技術的には正しいままだが、
「隠蔽と可読性の両立自体が新しい」という読まれ方をすると誤りになる。
比較の相手を光学符号だけに絞った議論は、分子的な埋め込みという第三の系統を無視しているように見える。

### 7.2 Hollow Nickel 事件についての判定

**評価者の指摘は、細部の訂正を除いて正しい。** 事件の事実関係は連邦捜査局の公式ページで確認できた。
硬貨、鉛筆、電池、ねじといった日用品に秘密を隠す実務は、1950年代に確かに存在した。

ただし、この事件は「研究」ではない。したがって「先行研究は存在しない」という文への直接の反例にはならない。
反例になるのは「日用品に偽装した秘密容器という発想が新しい」という含意のほうである。
その含意は捨てるべきである。発想そのものは新しくない。

また、Hollow Nickel は構造としては CipherFlute とかなり違う。
硬貨は容器であって、符号が素材そのものに組み込まれているわけではない。
読むには針で硬貨をこじ開ける必要があり、開けなければ中身に到達できない。
中身は微小写真であって、当時の意味で機械可読ではなく、
実際に読めるようになるまでに1953年から1957年までの4年と、亡命者の供述が要った。
「開けずに、機械で読む」という点は Hollow Nickel には無い。

### 7.3 二つ目の主張（基準素子による自己補正）について

DNA-of-things はこの主張の反例にならない。
既知の値を持つ基準素子を同じ物体に同居させ、比で読んで環境変動を打ち消すという構造は、
確認できた範囲（抄録、図の見出し、謝辞、参考文献、プレスリリース）には現れない。
DNA-of-things の頑健性は、DNA Fountain という符号の側の冗長性とシリカ封止による化学的安定性で担保されており、
測定量の環境依存を基準素子との比で消すという発想ではない。
ただし本文と供給情報を読めていないので、「反例が無いことを確かめた」とまでは言えず、
「入手できた範囲には見当たらなかった」というのが正確な言い方である。

---

## 8. この反例のもとで CipherFlute に残る主張

削るべきものと残るものを分けて書く。

**削るべきもの。**
「100ビットを超える秘密の値を電源なしの物体に埋め、日用品に偽装した先行研究は存在しない」という書き方は削る。
「隠蔽と可読性の両立は前例がない」という書き方も削る。
比較の相手を光学符号だけに絞る書き方も、分子的な埋め込みを無視していると読まれるので改める。

**残るもの。** 残るのは容量の記録ではなく、**読み出しの経済である。**
DNA-of-things の読み出しは、物体から小片を切り出す破壊的な操作を要し、
次世代シーケンサという専門の装置と分子生物学の工程を要し、
書き込みだけで1件あたり約2000スイスフランかかる。
一度読めば、その部分は失われる。持ち主が自分の秘密を日常的に取り出す用途には向かない。
CipherFlute の読み出しは、息と、手元のマイクロホンと、その場で走る復号処理だけで済み、
物体を削らず、何度でも繰り返せる。
この差は「どちらが優れているか」ではなく「どの用途に使えるか」を分ける差であり、
そこにこそ主張の重心を移すべきである。

したがって主張の書き換えの方向は次のようになる。
物体に大量の秘密を埋めること自体は DNA-of-things がすでに達成しており、その事実は認める。
その先で残っている問題は、**専門の設備も破壊も伴わずに、持ち主自身が現場で読み出せるかどうか**である。
CipherFlute はそこを、共鳴管という機構と、可聴音という媒体と、
同居させた基準素子による自己補正で埋めている。
既存研究の空白は「容量」ではなく「読み出しの敷居」の側にあり、
その空白は既存の受動音響タグの系譜（本調査の他のファイルで確認した容量の上限は誤り訂正後で12ビットである）と、
DNA-of-things の系譜（容量は桁違いだが読み出しの敷居が高い）のあいだにある。
CipherFlute はその中間の位置を占めており、その位置づけであれば、
本稿で確認した二つの反例のいずれとも矛盾しない。

第二の主張（基準素子を同居させて比で読む自己補正）は、本稿の検証の範囲では反証されなかった。
ただし「造形物への情報埋め込みの文脈で前例がない」という強い言い方は、
本稿が DNA-of-things の本文を読めていない以上、この検証だけでは支えきれない。

---

## 9. 確認できなかったこと

- DNA-of-things の本文と供給情報の全体を読めなかった。Unpaywall によれば公開版が存在せず、出版社ページは抄録までしか出さない。
  以下は原典で確認できなかった。
  読み出しに要した時間、読み出し1回あたりの費用、
  眼鏡レンズから切り出した小片の質量や寸法、うさぎから採った試料の質量、
  DNAをシリカ粒子から回収する具体的な工程（フッ化物系の溶解を用いたかどうか）、
  ポリメラーゼ連鎖反応のサイクル数、配列決定の読み取り本数。
- うさぎのデータ量が論文では45キロバイト、プレスリリースでは約100キロバイトと食い違う理由を確認できなかった。
- ObjGen（CHI Extended Abstracts 2023）の本文を取得できなかったため、
  日用品への秘密の埋め込みをどこまで扱っているかを確認できなかった。書誌のみ確定している。
- Cryptologia の Kollár 論文の抄録の原文を確認できなかった。書誌のみ Crossref で確定している。
- Nature Biotechnology の解説記事（Farzadfard, 2019年）の本文を取得できなかった。書誌のみ確定している。
- 連邦捜査局の公式ページは本体サイトが自動取得を拒むため、インターネットアーカイブの保存版で読んだ。
  保存版の採取日は2024年1月11日である。2026年7月時点の原本の文面が同一であることは確認していない。

---

## 10. 検証の方法

書誌は Crossref、PubMed、Europe PMC、Unpaywall、dblp、Semantic Scholar のいずれかに直接問い合わせて確定した。
抄録の原文は、アメリカ国立生物工学情報センターの efetch が返すテキストと Europe PMC の abstractText を突き合わせて同一であることを確かめた。
出版社ページは、通常の取得が認証へ転送されるため、利用者エージェントを指定した直接取得で本文の一部（図の見出し、謝辞、参考文献、データ公開先）を得た。
チューリッヒ工科大学のプレスリリースは全文を取得して該当箇所を原文で照合した。
アメリカ連邦捜査局のページはインターネットアーカイブの保存版から全文を取得した。
被引用の絞り込みは Semantic Scholar の被引用一覧174件を機械的に検索し、
該当したものを Crossref と Europe PMC で1件ずつ照合した。
検証を行ったのは2026年7月30日である。
