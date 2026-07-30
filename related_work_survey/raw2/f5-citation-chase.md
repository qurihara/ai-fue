# f5 被引用追跡（前段でAPIの回数制限のため埋められなかった穴を埋める作業）

作業日は2026年7月30日である。対象はCipherFlute（WISS 2026投稿予定、栗原一貴、津田塾大学）であり、依頼された8件の文献を引用している後続研究を洗い出し、CipherFluteに関わるものを拾った。

--------------------------------------------------------------------------------

## 0. 走査の方法と数量

### 使った経路と、使えなかった経路

まずOpenAlexを試したが、この環境からの問い合わせは全件が応答コード429（Rate limit exceeded）を返した。応答本文には「Insufficient budget. This request costs $0.0001 but you only have $0 remaining. Resets at midnight UTC」と書かれており、前段の担当者たちが同じ日のうちに一日ぶんの利用枠を使い切っていた。待つのではなく経路を切り替えるという指示に従い、OpenAlexは以降まったく使わなかった。

主経路にはSemantic Scholarの被引用API（`https://api.semanticscholar.org/graph/v1/paper/DOI:...../citations`）を使った。100件ずつのページ送りと、応答コード429に当たったときの指数的な待ち直し（5秒から始めて最大80秒まで倍にする）を組み込んだ取得スクリプトを書き、8件すべての被引用一覧を一度の実行で取り切った。書誌の照合にはCrossrefの単一DOI取得（`https://api.crossref.org/works/DOI`）、arXivのAPI（`https://export.arxiv.org/api/query`）、そしてUSENIXの発表ページを使った。DBLPは応答が40秒で時間切れになり使えなかった。

### 引用元8件の同定

8件のうち7件は想定した学術資源識別子でそのまま引けたが、Whooshだけは想定した値が別の論文を指していた。当初 `10.1145/2971763.2971773` で引いたところ「A comparison of order picking methods augmented with weight checking error detection」という無関係な論文が返ったため、Crossrefの書誌検索で正しい値が `10.1145/2971763.2971765` であることを確かめ直し、被引用を取り直した。前段の調査でWhooshの被引用がまったく取れていなかった原因の一つはこれだと思われる。

| 引用元 | 掲載と年 | 学術資源識別子 | 得た被引用の件数 |
|---|---|---|---|
| Blowhole（Tejadaら） | Graphics Interface 2018 | 10.20380/GI2018.18 | 17件 |
| Whoosh（Reyesら） | ISWC 2016 | 10.1145/2971763.2971765 | 44件 |
| Acoustic Barcodes（Harrisonら） | UIST 2012 | 10.1145/2380116.2380187 | 99件 |
| Lamello（Savageら） | CHI 2015 | 10.1145/2702123.2702207 | 78件 |
| Acoustic Voxels（Liら） | SIGGRAPH 2016 | 10.1145/2897824.2925960 | 50件 |
| Printone（梅谷信行さんら） | SIGGRAPH Asia 2016 | 10.1145/2980179.2980250 | 42件 |
| AirCode（Liら） | UIST 2017 | 10.1145/3126594.3126635 | 63件 |
| InfraredTags（Doganら） | CHI 2022 | 10.1145/3491102.3501951 | 67件 |

### 数字による報告

被引用の一覧として得た記録は合計460件である。同一の論文が複数の引用元を引いている重複を取り除くと、異なる論文は351件である。この351件すべてについて、題名、著者、掲載、年、学術資源識別子を一件ずつ画面に出して目で確認した。そのうち48件は要旨まで個別に読んだ。さらにそのうち26件は、Semantic Scholar以外の一次情報で書誌を照合した。照合先の内訳はCrossrefの書誌が20件、arXivの原文が7件、USENIXの発表ページが1件であり、CrossrefとarXivの両方で照合したものが2件あるため、異なる論文の数は26件である。

また351件の全体に対して、題名と要旨を横断する語句照合を四種類かけた。笛と音高に関わる語（flute、whistle、fipple、recorder、pitch、semitone、wind instrument、Helmholtz）、秘密分散と鍵保管に関わる語（secret sharing、Shamir、mnemonic、seed phrase、private key、key backup）、誤り訂正に関わる語（Reed-Solomon、error correction、BCH、Hamming code、parity、redundancy）、吹奏と呼気に関わる語（blow、breath、exhale、puff）である。この結果は下の第9節にまとめた。

--------------------------------------------------------------------------------

## 1. Blowhole（Graphics Interface 2018、Tejadaら）を引用する後続研究

**得た被引用は17件、そのうち17件すべてを個別に確認した。**

17件の内訳がこの節で最も重要な発見である。17件のうち9件が著者本人（Carlos E. TejadaとDaniel Ashbrookの研究室）の自己引用系列であり、残る8件のうち情報の符号化に関わるものは1件（レビュー論文）しかない。つまりBlowholeを情報符号化の方向へ発展させた第三者の研究は、Semantic Scholarに登録されている限りでは存在しない。

### 1-1. Print-and-Play: 3D-printed Interactive Objects Without Assembly or Calibration

- 著者は Carlos E. Tejada である。
- 掲載は Extended Abstracts of the 2020 CHI Conference on Human Factors in Computing Systems, pp.1-6, 2020年（博士課程学生コンソーシアム発表）である。
- URLは https://doi.org/10.1145/3334480.3375025 である。書誌はCrossrefで照合した。
- 要約すると、Blowholeの著者本人が自分の博士研究全体を「組み立ても較正も要らない3Dプリント対話物体」という一語で位置づけ直したものである。要旨には、よく研究された物理現象（音響共鳴と流体力学が例として挙げられている）に利用者の行為がどう作用するかを外部から測るという方針を掲げ、その方針から生まれた二つの技法としてBlowhole（音響共鳴を使う吹奏による対話技法）とAirTouch（空気圧センシングと流体力学による触覚感応物体の製作技法）を挙げている。
- CipherFluteとの関係を述べると、CipherFluteが立てる「電源も電子部品も持たない造形物を、人が息を吹くという行為で読む」という枠組みが、2020年にすでに一人の研究者の博士研究の主題として明文化されていたことになる。CipherFluteが差分を主張できるのは、この枠組みの中で運ぶ情報を状態や識別子ではなく任意のビット列に変えた点、そして情報の秘匿という応用文脈を持ち込んだ点に限られる。
- 脅威の度合いは**高**である。Blowhole単体への差分説明だけでは足りず、Blowholeを含む研究系列全体が「吹いて読む造形物」という枠を確立していることを認めた上で差分を書く必要がある。

### 1-2. AirLogic: Embedding Pneumatic Computation and I/O in 3D Models to Fabricate Electronics-Free Interactive Objects

- 著者は Valkyrie Savage, Carlos E. Tejada, Daniel Ashbrook である。
- 掲載は Proceedings of the 35th Annual ACM Symposium on User Interface Software and Technology (UIST 2022) である。
- URLは https://doi.org/10.1145/3526113.3545642 であり、公開版の全文が https://dl.acm.org/doi/pdf/10.1145/3526113.3545642 にある。
- 要約すると、空気圧による入力、論理処理、出力の部品を3Dプリント可能なモデルに埋め込み、電子回路も物理的な組み立ても使い直しのための復帰操作も要らない対話物体を作る技法である。13個の見本部品を用意し、部品ごとの空気漏れ、印刷の向きによる漏れ、物体内部の形状による漏れを定量している。
- CipherFluteとの関係を述べると、LamelloとBlowholeの双方を引く位置にあり、電子部品を使わない造形物に計算と入出力を持たせるという路線の到達点を示す。CipherFluteが「電源も電子部品も要らない」ことを価値として掲げるとき、その価値だけでは新規性にならないことをこの論文が示している。
- 脅威の度合いは**中**である。前段の調査（raw/02とraw/04）で既に把握されているが、Blowholeの直系の後続として位置づけ直す価値がある。

### 1-3. Ubiquitous BlowClick: Non-verbal Vocal Input for Confirmation with Hand-held Mobile Devices in the Field

- 著者は Daniel Zielasko, Javier Alejandro Jaquez Lora である。
- 掲載は Proceedings of the ACM Symposium on Spatial User Interaction (SUI 2024), pp.1-8, 2024年10月7日である。
- URLは https://doi.org/10.1145/3677386.3682101 であり、公開版の全文が https://dl.acm.org/doi/pdf/10.1145/3677386.3682101 にある。書誌はCrossrefで照合した。
- 要約すると、吹く音のような非言語の発声を機械学習で分類し、携帯端末の確定操作（タップの代替）として実地で評価したものである。Android上で動く軽量な分類の仕組みを作り、反応時間課題とISO 9241:411のFitts則選択課題で従来のタップと比べている。BlowholeとWhooshの両方を引いている。
- CipherFluteとの関係を述べると、「吹く」という行為が対話の入力として実用水準で評価された最新の例であり、CipherFluteが吹奏を読み出しの手続きに選んだことの妥当性を外部から支える。物体側に何も持たせない純粋な入力手法なので、符号化の主張とは衝突しない。
- 脅威の度合いは**中**である。主要な主張を崩さないが、吹奏を入力に使う研究の現況として引いておくと、読み出し手続きの選択に根拠が付く。

### 1-4. Embedding Information into or onto Additively Manufactured Parts: A Review of QR Codes, Steganography and Watermarking Methods

- 著者は Muhammad Usama, Ulas Yaman である。
- 掲載は Materials, 第15巻第7号, 論文番号2596, 2022年である。
- URLは https://doi.org/10.3390/ma15072596 である。
- 要約すると、付加製造された部品への情報の埋め込みを、QRコード、ステガノグラフィ、電子透かしという三つの枠で総覧したレビューである。BlowholeとAirCodeの両方を引いている。
- CipherFluteとの関係を述べると、造形物への情報埋め込みという分野が2022年時点でレビュー可能な厚みに達していたことを示す資料であり、CipherFluteの背景節で分野の成熟を一言で示すのに使える。
- 脅威の度合いは**中**である。個別の技術としては脅かさないが、レビューが存在するという事実そのものが「埋め込み自体は新しくない」という前段の判断を裏づける。

### 1-5. Blowholeの被引用のうち、拾わなかったものと、その理由

Tejada自身の系列である AirTouch（CHI 2020、空気圧で触覚感応にする3Dプリント物体、https://doi.org/10.1145/3313831.3376136 ）、EchoTube（UIST 2019、柔軟な管を導波路に使う超音波の押圧検出、https://doi.org/10.1145/3343055.3359712 ）、ClipWidgets（TEI 2022、円錐鏡でスマートフォンの背面カメラの視野を周辺に振り向けて受動的な3Dプリント部品の操作を読む、https://doi.org/10.1145/3490149.3501314 ）は、いずれも管や空洞を使うが情報の符号化をしないため脅威の度合いを**低**と判断した。ただしEchoTubeとClipWidgetsは「電源なしの造形部品を外部の機器で読む」という構図がCipherFluteと同型なので、必要なら一行で並べる価値がある。

LayerCode（SIGGRAPH 2019）、G-ID（CHI 2020）、Designing Physical Interactions with Triboelectric Material Sensing（CHI 2025）、BioTube（CHI 2025、生分解性の中空管状デバイス、https://doi.org/10.1145/3706598.3714165 ）、TouchPilot（ASSETS 2023）、Enhancing Tactile Learning（CHI 2025）、Tribo Tribe（CHI EA 2022）は、Blowholeを背景として一言引くだけで内容が離れており、脅威の度合いは**低**である。

--------------------------------------------------------------------------------

## 2. Whoosh（ISWC 2016、Reyesら）を引用する後続研究

**得た被引用は44件、そのうち44件すべてを個別に確認した。**

前段の調査では取得できていなかった一覧である。そして、この節の内容は新規性の主張にとってきわめて有利な否定的発見に尽きる。

44件のうち、Whooshの受動的な3Dプリント多管笛（FluteCase）の部分を引き継いだ研究は**1件も存在しない**。44件の内訳は、スマートウォッチの入力手法が約20件、呼気や呼吸を入力に使う研究が5件、腕時計以外の身体入力が約10件、レビューと学位論文が6件、そして音響センシング一般が3件である。FluteCaseに触れる形で引いているのはBlowhole自身（Whooshを引く44件のうちの1件として現れる）だけであり、Blowhole以降にFluteCaseの多管構造を発展させた研究は見つからなかった。

この事実は二つの意味を持つ。第一に、CipherFluteがWhooshを引用していないという前段が指摘した穴は依然として塞ぐ必要があるが、Whooshの笛の部分が学術的にほとんど継承されていないため、CipherFluteが「Whooshが素描だけで終えた受動多管笛を、符号語彙として設計し直した最初の研究である」という位置づけを取ることが可能である。第二に、WhooshとBlowholeを結ぶ線は文献上に実在する（BlowholeがWhooshを引いている）ので、CipherFluteがBlowholeを引きながらWhooshを引かないという現状は、系譜の一段を飛ばしている状態に見える。

拾うに値するものは次の4件である。

### 2-1. A Survey on Acoustic Sensing in the Metasurface Era: Challenges, Advances, and Applications

- 著者は Liheng Jiang, Yongzhao Zhang, Ting Chen, Yi-Chao Chen, Dian Ding, Yijie Li, Fenghua Xu, Liwei Guo, Jingwei Li, Xiong Li, Jiguo Yu, Xiaosong Zhang である。
- 掲載は Fundamental Research, 2025年（オンライン先行公開）である。
- URLは https://doi.org/10.1016/j.fmre.2025.07.015 である。要旨はSemantic Scholarにも本文提供元にも登録されておらず、内容は題名と掲載誌の書誌情報までしか確認できなかった。
- 要約すると、音響センシングを音響メタサーフェス（音波を形状で操る人工構造）の時代という視点から総覧した2025年の総説である。Whooshを引いている。
- CipherFluteとの関係を述べると、「形状そのものが音を規定する」という物理をセンシングの主流に位置づける最新の総説であり、CipherFluteの物理層をこの文脈に接続できる。
- 脅威の度合いは**中**である。個別の技術で脅かすものではないが、2025年の総説を引かないと分野の現況を押さえていないと見られうる。要旨を確認できていないので、引用する前に本文の確認が必要である。

### 2-2. BreathPrint: Breathing Acoustics-based User Authentication

- 著者は Jagmohan Chauhan, Yining Hu, Suranga Seneviratne, Archan Misra, Aruna Seneviratne である。
- 掲載は Proceedings of the 15th Annual International Conference on Mobile Systems, Applications, and Services (MobiSys 2017) である。
- URLは https://doi.org/10.1145/3081333.3081355 である。
- 要約すると、呼吸（鼻からの呼気、通常の呼吸、深い呼吸）の音響的な特徴を使って利用者を認証する手法である。
- CipherFluteとの関係を述べると、「息の音」を安全性の文脈で使った先行例である。ただし認証するのは人の身体的な特徴であって物体に格納された秘密ではなく、CipherFluteとは秘密の所在が正反対である。
- 脅威の度合いは**中**である。息と安全性を結ぶ先行研究として一言で位置づけ、CipherFluteが読むのは人ではなく物体であることを明示するのに使える。

### 2-3. The Design Space of 3D Printable Interactivity

- 著者は Rafael Ballagas, Sarthak Ghosh, James Landay である。
- 掲載は Proceedings of the ACM on Interactive, Mobile, Wearable and Ubiquitous Technologies, 2018年である。
- URLは https://doi.org/10.1145/3214264 である。
- 要約すると、3Dプリントで完全に機能するセンサとアクチュエータを作る研究を機構、意図された手がかり、対話の原素、出力の様式という四つの軸で分類し、Zwickyの箱という多次元の表にまとめた総覧である。既存研究の穴も指摘している。Whoosh、Lamello、Acoustic Voxels、AirCodeの四つすべてを引いている。
- CipherFluteとの関係を述べると、CipherFluteが立つ設計空間を外部の枠組みで位置づけられる。CipherFluteの位置は、機構が空気の共鳴、手がかりが吹き口、対話の原素が吹奏、出力の様式が可聴音という組み合わせになる。
- 脅威の度合いは**中**である。技術としては脅かさないが、設計空間の整理として引いておくと貢献の位置が明確になる。

### 2-4. Knock knock, what's there: converting passive objects into customizable smart controllers

- 著者は Lei Shi, Maryam Ashoori, Yunfeng Zhang, Shiri Azenkot である。
- 掲載は Proceedings of the 20th International Conference on Human-Computer Interaction with Mobile Devices and Services (MobileHCI 2018) である。
- URLは https://doi.org/10.1145/3229434.3229453 である。
- 要約すると、受動的な日用品を叩く音で識別して操作器に転用する手法である。
- CipherFluteとの関係を述べると、受動的な日用品を音で読むという枠組みが共通する。ただし格納する情報は少数のクラスにとどまる。
- 脅威の度合いは**低**である。前段の調査（raw/06と raw2/v1）で既に把握されている。

--------------------------------------------------------------------------------

## 3. Acoustic Barcodes（UIST 2012、Harrisonら）を引用する後続研究

**得た被引用は99件、そのうち題名と書誌を99件すべて確認し、要旨まで読んだものは19件である。**

前段の調査（raw/02）では99件の一覧は得たものの個別確認をしていないと報告されていた。個別に見た結果、前段が明示的に「調べ残した穴」として挙げていた2件が両方ともこの一覧の中にあり、どちらも確認できた。

### 3-1. Acoustics to the Rescue: Physical Key Inference Attack Revisited（Keynergy）

- 著者は Soundarya Ramesh, Rui Xiao（シンガポール国立大学）, Anindya Maiti（オクラホマ大学）, Jong Taek Lee, Harini Ramprasad, Ananda Kumar（シンガポール国立大学）, Murtuza Jadliwala（テキサス大学サンアントニオ校）, Jun Han（シンガポール国立大学）である。
- 掲載は 30th USENIX Security Symposium (USENIX Security 2021) である。
- URLは https://www.usenix.org/conference/usenixsecurity21/presentation/ramesh である。要旨と著者所属はこのUSENIXの発表ページ本文で直接確認した。Semantic Scholarには学術資源識別子も要旨も登録されていないため、この一次ページが唯一の確認先である。
- 要約すると、ピンタンブラー錠の鍵を挿入するときに必然的に生じる可聴の「かちり」という音と、被害者が鍵を持っている様子の映像を組み合わせ、鍵の刻み（論文はこれを秘密と呼んでいる）を離れた場所から推定する攻撃である。75本の鍵に対する実験で、音響だけを使う手法で候補を平均して約75パーセント削減し、音響と映像を組み合わせると75本のうち6本（8パーセント）について候補を10本未満まで絞り込めたと報告している。
- CipherFluteとの関係を述べると、物理的な鍵の形状という秘密が、その鍵が発する音から推定できることを実証した研究である。CipherFluteの脅威モデルは「音や物体の層には暗号学的な秘匿の力はまったく無い」と宣言しているが、この論文はその宣言が誇張ではなく、むしろ音響からの秘密推定が現実の攻撃として成立することを示す具体的な証拠になる。CipherFluteの場合、笛が鳴った音そのものが符号なので、聞かれれば秘密が漏れるという性質は設計上明らかであり、この論文はその性質を「既知の攻撃類型」として位置づける根拠になる。
- 脅威の度合いは**高**である。新規性を脅かす向きではなく、脅威モデルの記述を強化する向きの高さである。前段の調査（raw/02）が「優先して埋めるべき穴」として名指ししていた文献であり、これを引かないまま「物理層に秘匿の力は無い」と宣言すると、安全性分野の査読者に根拠の欠落と見られる。

### 3-2. Break-Resilient Codes

- 著者は Canran Wang, Jin Sima, Netanel Raviv である。
- 掲載は IEEE Transactions on Information Theory, 2026年（早期公開、掲載ページは1-1と表示される）である。プレプリントは arXiv:2310.03897 として2023年10月5日に公開され、2025年9月21日に第3版へ改訂されている。
- URLは https://doi.org/10.1109/tit.2026.3708787 および https://arxiv.org/abs/2310.03897 である。書誌はCrossrefで、要旨はarXivの原文で照合した。
- 要約すると、長さnの符号語が敵によって最大t箇所の任意の位置で断ち切られても元のデータを復元できる符号（論文はこれを break-resilient code と呼ぶ）の冗長度の下限を示し、その下限を漸近的に無視できる項まで達成する構成を与えたものである。DNAデータ保存の文脈で研究されている torn paper channel と類似の問題であると位置づけている。Acoustic Barcodesを引いている。
- CipherFluteとの関係を述べると、この論文は前段の調査で「高」と判定された Secure Information Embedding in Forensic 3D Fingerprinting（SIDE、USENIX Security 2024）の符号理論的な土台である。SIDEの要旨は、敵が造形物を破断して断片の一部を隠しても指紋を復元できるという性質を break-resilient かつ loss-tolerant と呼んでおり、その break-resilient の定義と構成がこの論文にある。つまり造形物へ埋め込む情報のための符号設計は、応用側（SIDE）だけでなく符号理論側（この論文）でも独立に整備が進んでいる。
- 脅威の度合いは**高**である。CipherFluteがReed-Solomon符号を採用した理由を「造形物という媒体に固有の欠損に合わせた」と書くならば、造形物固有の欠損モデル（破断と断片の隠匿）に対する符号がすでに理論的に構成されていることを認めなければならない。逆に言えば、CipherFluteの符号層の貢献は理論ではなく「11個から13個のスロットという語彙の上で実装した」という工学の側にあると明示すべきである。

### 3-3. Passive underwater acoustic barcodes using Rayleigh wave resonance

- 著者は Yanling Zhou, Jun Fan, Jinfeng Huang, Bin Wang である。
- 掲載は Journal of Applied Physics, 第131巻第12号, 2022年3月22日である。プレプリントは arXiv:2107.13860 である。
- URLは https://doi.org/10.1063/5.0086290 であり、公開版の全文が https://arxiv.org/pdf/2107.13860 にある。書誌はCrossrefで照合した。
- 要約すると、アクリルの球を組み合わせた受動的な水中音響標識を作り、球が広帯域のパルスで励振されたときに現れる亜音速のRayleigh波共鳴による強い後方散乱の峰を符号として使う手法である。共鳴周波数がRayleigh波の速度と球の半径で決まるため、半径を変えるか異なる半径の球を組み合わせることで後方散乱応答を調節でき、選んだ周波数帯において各標識が固有の音響的な署名を持つと述べている。能動的な音響標識に比べて広い帯域で働き、寿命が長く、費用が低いと主張している。
- CipherFluteとの関係を述べると、「寸法が共鳴周波数を決めるという物理を使い、寸法の異なる素子を組み合わせて符号を作る」という設計がCipherFluteの管長設計と正面から同型である。組み合わせによって語彙を作るという発想まで一致する。異なるのは、読み出しに広帯域のパルスを送る送受信機が必要であること、媒質が水であること、格納するのが製造時に決まる識別子であって利用者の秘密ではないことである。
- 脅威の度合いは**中**である。前段の調査（raw/02とraw/04）で「書誌が確定できないまま残った」と報告されていた文献であり、この作業で書誌を確定できた。物理の同型性が明白なので、引用して媒質と読み出し装置の違いを述べるべきである。

### 3-4. Acoustic barcode based on the acoustic scattering characteristics of underwater targets

- 著者は Fan Zhou, Jun Fan, Bin Wang, Yanling Zhou, Jinfeng Huang である。
- 掲載は Applied Acoustics, 第181巻, 論文番号108607, 2022年である。
- URLは https://doi.org/10.1016/j.apacoust.2021.108607 である。要旨はSemantic Scholarにも登録されておらず、内容は題名と掲載誌の書誌情報までしか確認できなかった。
- 要約すると、水中目標の音響散乱特性に基づく音響バーコードを扱う研究であり、3-3と同じ研究グループによる姉妹論文である。
- CipherFluteとの関係を述べると、3-3と同じ枠組みの拡張であり、受動音響符号という枠が水中音響の分野で独立に確立していることを示す。
- 脅威の度合いは**中**である。3-3と合わせて一つの系列として引くのが自然である。要旨を確認できていないので、引用する前に本文の確認が必要である。

### 3-5. Low-cost and Non-visual Labels Using Magnetic Printing（MagCode）

- 著者は Guanhua Zhao, Yueli Yan, Zhice Yang である。
- 掲載は Proceedings of the ACM on Human-Computer Interaction, 第7巻 EICS号, pp.1-18, 2023年6月14日である。
- URLは https://doi.org/10.1145/3593232 であり、公開版の全文が https://dl.acm.org/doi/pdf/10.1145/3593232 にある。書誌はCrossrefで照合した。
- 要約すると、磁性インクを普通のプリンタで印刷して磁界の形でデータを格納するラベルであり、磁力計をなでることでデータを取り出す。視覚の経路に頼らないため、通常の視覚的な符号を読むことが望まれない場合や不可能な場合の対話の機会を開くと述べている。さらに、模様を視覚的に復号できないように設計でき、磁気信号への接近にはきわめて近い距離が必要であるという評価結果を示し、この性質によって「ゲームのイースターエッグや日常の支払い資格情報といった、隠された、そして機微な情報」を運べると主張している。
- CipherFluteとの関係を述べると、隠された機微な情報を日用品に載せるという応用文脈を明示的に掲げた数少ない例である。しかも支払い資格情報という、暗号資産の復元用情報と近い応用を名指ししている。近接を要することを秘匿の根拠にしている点は、CipherFluteが「物理層が担うのは探索コストの引き上げだけである」と宣言した立場と対照的であり、この対照はCipherFluteの脅威モデルの記述の価値を高める。
- 脅威の度合いは**中**である。読み出しの物理が磁気であって音響ではなく、誤り訂正も基準体による正規化も秘密分散もないため主要な主張は崩れない。ただし「日用品に機微な情報を隠す」という応用文脈の先行例として引用が必要である。

### 3-6. PoBiTag: Toward Unobtrusive and Customizable Tag-Based Interaction With Optical Polarization and Birefringence

- 著者は Seohyeon Park, Seunghun Chae, Jaemin Choi, Hyosu Kim である。
- 掲載は IEEE Access, 第13巻, pp.157730-157741, 2025年である。
- URLは https://doi.org/10.1109/access.2025.3606941 である。書誌はCrossrefで照合した。
- 要約すると、透明で複屈折を持つ日用の材料（PET製シールやセロハンテープが例として挙げられている）をタグとして使い、携帯端末のカメラと照明に偏光フィルムを貼るだけで複屈折の領域を見分けられるようにする、視覚的に目立たないタグの仕組みである。Acoustic BarcodesとAirCodeの両方を引いている。
- CipherFluteとの関係を述べると、日用品の外見を損なわずにタグを載せるという課題設定が共通し、読み取り装置を市販端末に安価な付属品を足すだけで作るという方針も共通する。
- 脅威の度合いは**中**である。読み出しが光学であり秘密の保管も扱わないが、2025年の「目立たないタグ」の到達点として引く価値がある。

### 3-7. Ultralow Power Wireless Ultrasonic Sensor Tag With ID

- 著者は Ethan Kepros, Premjeet Chahal である。
- 掲載は IEEE Sensors Journal, 2025年である。
- URLは https://doi.org/10.1109/JSEN.2025.3529891 である。
- 要約すると、圧電式微細加工超音波振動子を使って識別子とセンサのデータを送る仕組みであり、著者らはこれを programmable acoustic identification と呼び、既存の音響識別が水中で働くのに対して空気中で働き、識別子を動的に書き換えられ、消費電力が低いことを差分として挙げている。電源には二酸化マンガンリチウム一次電池（CR2032）を使う。
- CipherFluteとの関係を述べると、音響で識別子を運ぶという枠組みは共通するが、電池と微細加工振動子と微小制御器を必要とするため、電源も電子部品も持たないというCipherFluteの前提とは正反対である。
- 脅威の度合いは**低**である。前段の調査（raw/02とraw/04）で既に把握されている。

### 3-8. DynaTags: Low-Cost Fiducial Marker Mechanisms

- 著者は Cassandra Scheirer, Chris Harrison である。
- 掲載は Proceedings of the 2022 International Conference on Multimodal Interaction (ICMI 2022), pp.432-443, 2022年11月7日である。
- URLは https://doi.org/10.1145/3536221.3556591 であり、公開版の全文が https://dl.acm.org/doi/pdf/10.1145/3536221.3556591 にある。書誌はCrossrefで照合した。
- 要約すると、Acoustic Barcodesの著者本人（Chris Harrison）が、印刷された基準マーカーの搭載する情報が静的であるという限界を、紙で作った単純な機構によって複数の搭載情報を表せるようにして越えたものである。23個の機構の一覧を示し、標準のスマートフォンの読み取りアプリで読めるとしている。
- CipherFluteとの関係を述べると、受動的な物体に載せた符号の情報量と可変性を上げる方向の後続であり、CipherFluteが13個のスロットという語彙で情報量を上げた方向と対比できる。
- 脅威の度合いは**低**である。読み出しが光学であり、動く機構を要する。

### 3-9. Acoustic Barcodesの被引用のうち、既に前段で押さえられているもの

SoundOff（IMWUT 2025）、Splitcode（2022年、機械の座標誤差分布をVoronoi分割で誇張して部品の真正性を確かめる手法、https://doi.org/10.2139/ssrn.3993045 ）、Secure Information Embedding in Forensic 3D Fingerprinting（USENIX Security 2024）、All-in-one encoder/decoder approach for non-destructive identification of 3D-printed objects（MBE 2022、STLファイルの底面の空き領域に三次元のバーコードを差し込んでテラヘルツ波で読む手法、https://doi.org/10.3934/mbe.2022657 ）、Information Embedding in Additive Manufacturing through Printing Speed Control（AMSec@CCS 2021、印刷速度の差で表面に微小な高低差を作り光学的表面形状測定器で読む手法、53ミリメートル毎秒の速度差で正解率80パーセント、https://doi.org/10.1145/3462223.3485623 ）、Asterisk and Obelisk（UIST 2018）、EarCase（2023）、Owlet（MobiSys 2021、3Dプリントのメタマテリアル構造をマイクに被せて方向固有の署名を音に埋める手法、参照用の第二のマイクで環境変動を打ち消す、https://doi.org/10.1145/3458864.3467880 ）、SAWSense（CHI 2023）、DuoTouch（CHI 2026）は、前段の調査で既に扱われているか、あるいは内容が離れている。

このうちOwletについては一点だけ補足する価値がある。Owletは「参照用の追加マイクを基準チャネルとして使い、環境の変動を打ち消して任意の場所でも頑健に働くようにする」という手法を採っており、CipherFluteが基準笛を混ぜて比で読む設計と発想が同型である。基準となる既知の素子を系に同居させて環境変動を打ち消すという考え方は、音響センシングの分野に前例があると認めるべきである。

--------------------------------------------------------------------------------

## 4. Lamello（CHI 2015、Savageら）を引用する後続研究

**得た被引用は78件、そのうち題名と書誌を78件すべて確認し、要旨まで読んだものは11件である。**

Lamelloの後続78件を通して見た結果、櫛歯の長さで音高を作り分けるという物理を引き継いだ研究はごく少なく、多数がLamelloを「受動的な触知入力部品」の一例として一言引くだけであった。Lamelloのde Bruijn系列による符号設計を多ビットの情報搬送へ延ばした後続は**1件も存在しない**。これはCipherFluteの符号語彙設計にとって有利な否定的発見である。

### 4-1. MoiréTag: A Low-Cost Tag for High-Precision Tangible Interactions without Active Components

- 著者は Peiyu Zhang, Wen Ying, Sara L. Riggs, Seongkook Heo である。
- 掲載は Proceedings of the ACM on Human-Computer Interaction, 第8巻 ISS号, pp.1-19, 2024年10月24日である。
- URLは https://doi.org/10.1145/3698113 であり、公開版の全文が https://dl.acm.org/doi/pdf/10.1145/3698113 にある。書誌はCrossrefで照合した。
- 要約すると、周期の異なる二層の縞模様を重ねてモアレ縞を作り、実際の動きより速く動く縞を使って微小な変位を能動部品なしで拡大して読むタグである。ミリメートル未満の動きを平均誤差0.043ミリメートルで実時間検出できると報告している。
- CipherFluteとの関係を述べると、能動部品を持たないタグで高い分解能を得るという方向の到達点であり、CipherFluteが100セント刻みという粗い分解能を選んだ判断と対比できる。
- 脅威の度合いは**中**である。読み出しが光学であり搬送するのが変位であって符号ではないため主要な主張は崩れないが、受動タグの分解能の水準を示す参照点になる。

### 4-2. Estimation of fused-filament-fabrication structural vibro-acoustic performance by modal impact sound

- 著者は Sixian Zhong, Parinya Punpongsanon, Daisuke Iwai, Kosuke Sato である。
- 掲載は Computers and Graphics, 2023年である。
- URLは https://doi.org/10.1016/j.cag.2023.07.010 である。要旨はSemantic Scholarにも登録されておらず、内容は題名と掲載誌の書誌情報までしか確認できなかった。
- 要約すると、熱溶解積層方式で造形した構造の振動音響的な性能を、叩いたときのモーダルな打撃音から推定する研究である。LamelloとPrintoneの両方を引いている。大阪大学のグループによる日本の研究である。
- CipherFluteとの関係を述べると、熱溶解積層方式で造形した物体の音響応答を予測する研究であり、CipherFluteが管長と基本周波数の関係を実測で較正した工程に対応する。
- 脅威の度合いは**中**である。前段の調査（raw/03とraw/04）で既に触れられている。日本のグループの研究であり投稿先の読者に近い。

### 4-3. ClickSense: A Low-Cost Tangible Active User Input Method Using Passive Acoustic Sensing for Mobile Virtual Reality

- 著者は Kristen Grinyer, Robert J. Teather である。
- 掲載は Extended Abstracts of the 2025 CHI Conference on Human Factors in Computing Systems である。
- URLは https://doi.org/10.1145/3706599.3720000 である。
- 要約すると、受動音響センシングによる低費用の触知入力手法を移動型仮想現実向けに作ったものである。
- CipherFluteとの関係を述べると、受動音響で入力を読むという枠組みが共通する。搬送するのは操作の事象であって情報ではない。
- 脅威の度合いは**低**である。

### 4-4. MechSense: A Design and Fabrication Pipeline for Integrating Rotary Encoders into 3D Printed Mechanisms

- 著者は Marwa Alalawi, Noah Pacik-Nelson, Junyi Zhu, Benjamin Greenspan, Andrew Doan, Brandon Wong ほかである。
- 掲載は Proceedings of the 2023 CHI Conference on Human Factors in Computing Systems である。
- URLは https://doi.org/10.1145/3544548.3581361 である。
- 要約すると、回転式の符号器を3Dプリント機構に組み込む設計と製造の一連の流れを示したものである。
- CipherFluteとの関係を述べると、造形物に符号器を組み込むという語の重なりはあるが、電子部品を必要とするため前提が異なる。
- 脅威の度合いは**低**である。

--------------------------------------------------------------------------------

## 5. Acoustic Voxels（SIGGRAPH 2016、Liら）を引用する後続研究

**得た被引用は50件、そのうち題名と書誌を50件すべて確認し、要旨まで読んだものは9件である。**

50件を通して見た結果、Acoustic Voxelsが実証した4ビットという音響埋め込み容量を超える数字を報告した後続は**1件も存在しない**。50件のうち音響を主題とするものは約12件で、残りは計算による製造設計の総覧や幾何処理の論文がAcoustic Voxelsを一例として引くだけである。これはCipherFluteが「音響で運ぶ情報量を桁で引き上げた」と主張する余地を裏づける有利な否定的発見である。

### 5-1. SonicSieve: Bringing Directional Speech Extraction to Smartphones Using Acoustic Microstructures

- 著者は Kuang Yuan, Yifeng Wang, Xiyuxing Zhang, Chengyi Shen, Swarun Kumar, Justin Chan である。
- 掲載は Proceedings of the 2026 CHI Conference on Human Factors in Computing Systems である。プレプリントは arXiv:2504.10793 として2025年4月15日に公開され、2026年2月11日に第3版へ改訂されている。
- URLは https://doi.org/10.1145/3772318.3790376 および https://arxiv.org/abs/2504.10793 である。要旨はarXivの原文で照合した。
- 要約すると、生物に着想を得た音響微細構造をスマートフォンに付ける受動的な設計により、追加の電子部品をまったく使わずに入ってくる音声へ方向の手がかりを埋め込み、端末上の神経網で実時間に方向別の音声を取り出す仕組みである。30度の角度領域に絞ったとき信号品質が5.0デシベル改善し、マイク2個の系が従来のマイク5個の配列を上回ると報告している。
- CipherFluteとの関係を述べると、「受動的な造形構造が音に情報（この場合は方向の手がかり）を書き込み、電子部品を追加せずに読む」という枠組みがCipherFluteと同型である。しかも2026年のCHIに載る最新研究である。
- 脅威の度合いは**中**である。書き込む情報が方向の手がかりであって利用者の秘密ではなく、構造は音を作るのではなく通り過ぎる音を変えるだけなので主要な主張は崩れない。ただし「受動的な造形構造が音に情報を載せる」という言い方をするなら引用が必要である。

### 5-2. LumosX: 3D Printed Anisotropic Light-Transfer

- 著者は Qian Lu, Xiaoying Yang, Xue Wang, Jacob Sayono, Yang Zhang, Jeeeun Kim である。
- 掲載は Proceedings of the 2025 CHI Conference on Human Factors in Computing Systems, pp.1-21, 2025年4月25日である。
- URLは https://doi.org/10.1145/3706598.3714124 である。書誌はCrossrefで照合した。
- 要約すると、3Dプリントで作る光学的な異方性（見る角度によって反射光が変わる性質）を使って光の強度の変化に情報を符号化し復号する一組の技法である。市販の材料と、押出量、走査角、層高、ノズル位置といった処理条件の精密な制御によって方向別の反射と明暗の対比を最適化する。Acoustic Barcodes、Acoustic Voxels、AirCode、InfraredTagsの四つすべてを引いている。
- CipherFluteとの関係を述べると、CipherFluteが引用する（あるいは引用すべき）四つの先行研究をすべて引く位置にあり、CipherFluteと同じ系譜の直近の交差点である。しかも家庭用の押出方式プリンタの処理条件を設計変数に使う点までCipherFluteと重なる。
- 脅威の度合いは**中**である。読み出しが光学であり、格納するのが環境センシング用の情報であって秘密ではないため主要な主張は崩れないが、引用一覧の重なりが大きいため引かないと目立つ。

### 5-3. EchoSnap and PlayableAle: Exploring Audible Resonant Interaction

- 著者は Peter D. Bennett, Christopher Haworth, Gascia Ouzounian, James Wheale である。
- 掲載は Proceedings of the Eleventh International Conference on Tangible, Embedded, and Embodied Interaction (TEI 2017), pp.543-549, 2017年3月20日である。
- URLは https://doi.org/10.1145/3024969.3025091 である。書誌はCrossrefで照合した。要旨はSemantic Scholarにも登録されておらず、内容は題名と書誌までしか確認できなかった。
- 要約すると、題名が示すとおり「可聴の共鳴による対話」を二つの作品を通して探る研究である。
- CipherFluteとの関係を述べると、可聴域の共鳴を対話の媒体として正面から扱った早い例であり、CipherFluteが可聴音を選んだことを位置づけられる。
- 脅威の度合いは**低**である。要旨を確認できていないので、引用する前に本文の確認が必要である。

### 5-4. Acoustic Voxelsの被引用のうち、音響を主題とする残りのもの

SoundBender（UIST 2018、位相配列振動子と音響メタマテリアルを組み合わせて障害物の背後の音場を動的に制御する、https://doi.org/10.1145/3242587.3242590 ）、VARI-SOUND（CHI 2019、音のための可変焦点レンズ）、Assessment on the use of additive manufacturing technologies for acoustic applications（International Journal of Advanced Manufacturing Technology 2020、https://doi.org/10.1007/s00170-020-05853-2 ）、A review on additive manufacturing of wave controlling metamaterial（同誌 2022、https://doi.org/10.1007/s00170-022-10486-8 ）、Acoustic notch filter based on self-collimation sonic crystals（Applied Physics Express 2024）は、いずれも音を形状で操る側の研究であり、情報の符号化を扱わないため脅威の度合いを**低**と判断した。後者二件は要旨が確認できなかった。

--------------------------------------------------------------------------------

## 6. Printone（SIGGRAPH Asia 2016、梅谷信行さんら）を引用する後続研究

**得た被引用は42件、そのうち題名と書誌を42件すべて確認し、要旨まで読んだものは8件である。**

42件を通して見た結果、Printoneの後続で「狙った音高の並びを符号として読む」ものは**1件も存在しない**。42件の内訳は、計算による製造設計の理論と道具が約20件、楽器の音響と製作が7件、造形物の識別が4件、その他が約11件である。フィップル笛を扱う後続はFlueBricks（CHI 2026）が唯一であり、この論文は符号化をまったく扱わない。これはCipherFluteの中核の主張にとってきわめて有利な否定的発見である。

### 6-1. Tubes Among Us: Analog Attack on Automatic Speaker Identification

- 著者は Shimaa Ahmed, Yash Wani, Ali Shahin Shamsabadi, Mohammad Yaghini, Ilia Shumailov, Nicolas Papernot, Kassem Fawaz である。
- 掲載は 32nd USENIX Security Symposium (USENIX Security 2023) である。プレプリントは arXiv:2202.02751 として2022年2月6日に公開されている。学会発表の要旨として The Journal of the Acoustical Society of America 第155巻 3_Supplement号 A68ページ（2024年3月）にも短縮版がある。
- URLは https://www.usenix.org/conference/usenixsecurity23/presentation/ahmed および https://arxiv.org/abs/2202.02751 である。著者、掲載、要旨はarXivの原文で照合し、学会発表要旨の書誌はCrossrefで照合した。
- 要約すると、話者識別のような課題において、人が単に管を通して話すだけで、機械学習の模型に対して他人になりすます「アナログな敵対的事例」を、ほとんど費用も監督もなしに作れることを示した研究である。多くの防御が「人は意味のある狙いを定めた敵対的事例を作れない」という仮定に立っていることを指摘し、その仮定が誤りであると実証している。
- CipherFluteとの関係を述べると、Printoneを引く形で「3Dプリントの管の共鳴が音を系統的に変える」という物理を安全性の攻撃側に使った研究である。CipherFluteの脅威モデルは「物理層に暗号学的な秘匿の力はまったく無い」と宣言するが、この論文は逆向きに「造形した管の音響特性は安全性の系を欺くほど制御可能である」と示している。したがってCipherFluteは、管の音響が制御可能であること自体は攻撃にも使える力であると認めた上で、自分の設計ではその力を秘匿には使わないと述べる形が最も正確になる。
- 脅威の度合いは**高**である。新規性を直接脅かすものではないが、「3Dプリントの管の音響」と「安全性」を結んだ研究がUSENIX Securityという安全性の最上位会議に既に存在するという事実は、CipherFluteが安全性の文脈で語るときに必ず踏まえるべき前提である。前段の14の切り口すべてでこの文献に到達できておらず、この作業で初めて見つかった。

### 6-2. An overview of additive manufacturing technologies for musical wind instruments

- 著者は Ajith Damodaran, M. Sugavaneswaran, Larry Lessard である。
- 掲載は SN Applied Sciences, 第3巻第2号, 2021年1月20日である。
- URLは https://doi.org/10.1007/s42452-021-04170-x である。書誌はCrossrefで照合した。
- 要約すると、管楽器に対する付加製造技術の応用を体系的に総覧したものである。各方式、使う材料、技術的な特徴、管楽器に固有の処理条件を論じ、既存の管楽器の革新と外観の改善、古代の音楽の理解、専門の演奏家のための個別化という応用を示している。「楽器の設計条件を狙って調律できる能力」を付加製造の利点として明記している。
- CipherFluteとの関係を述べると、3Dプリントで管楽器を作り狙った音高に合わせる工程が2021年時点で総説の対象になるほど確立していたことを示す資料である。
- 脅威の度合いは**中**である。前段の調査（raw/03）で既に把握されている。CipherFluteの計算設計を新規性に掲げると即座に反証されることを補強する。

### 6-3. Printoneの被引用のうち、楽器と音響に関わる残りのもの

FlueBricks（CHI 2026、前段の調査で把握済み）、Estimation of fused-filament-fabrication structural vibro-acoustic performance by modal impact sound（第4節の4-2に記載）、3D Virtual Reconstruction and Sound Simulation of an Ancient Roman Brass Musical Instrument（2020年、https://doi.org/10.1007/978-3-030-50267-6_21 ）、Individual Fabrication of Cymbals using Incremental Robotic Sheet Forming（NIME 2018、https://doi.org/10.5281/zenodo.1302585 ）、Sound Synthesis, Propagation, and Rendering（総説、2022年）、ThermalRouter（UIST 2023）は、いずれも情報の符号化を扱わないため脅威の度合いを**低**と判断した。

なおPrintoneの被引用にはFabAuth（CHI EA 2019）とProtoHole（CHI EA 2018）の両方が含まれている。この二件は前段の調査で「高」および「中」と判定された日本の研究であり、両方がPrintoneを引いているという事実は、日本のHCI分野の造形音響研究がPrintoneを共通の背景としていることを示す。CipherFluteがPrintoneを引かないままFabAuthやProtoHoleと差分を述べると、共通の背景を欠いた比較になる。

--------------------------------------------------------------------------------

## 7. AirCode（UIST 2017、Liら）を引用する後続研究

**得た被引用は63件、そのうち題名と書誌を63件すべて確認し、要旨まで読んだものは16件である。**

### 7-1. Near-infrared Imaging for Information Embedding and Extraction with Layered Structures

- 著者は Weiwei Jiang, Difeng Yu, Chaofan Wang, Zhanna Sarsenbayeva, Niels van Berkel, Jorge Goncalves, Vassilis Kostakos である。
- 掲載は ACM Transactions on Graphics, 第42巻第1号, pp.1-26, 2022年8月12日である。
- URLは https://doi.org/10.1145/3533426 であり、著者の一人が公開している全文が https://nielsvanberkel.com/files/publications/tog2023a.pdf にある。書誌はCrossrefで照合した。
- 要約すると、小型化した近赤外分光の走査器を計算機制御の平面描画機で動かし、日常の環境で使える低費用の非破壊検査を実現したものである。埋め込む内容を最適化する手法と、人の監督なしに内容を取り出すための波長選択の算法を示し、16枚重ねた紙の束を透して隠された文字を取り出せると報告している。そして要旨の末尾で、この手法が開く応用として「チップを使わない情報の埋め込み、**物理的な秘密分散**、3Dプリントの評価、そしてステガノグラフィ」を明示的に挙げている。
- CipherFluteとの関係を述べると、これが今回の作業で見つかった最も重要な文献である。前段の調査は14の切り口すべてを通じて「秘密分散を目的に設計された造形タグは見つからなかった」と報告していたが、この論文は物理的な秘密分散を応用として明記している。したがって「物理媒体への情報埋め込みと秘密分散を結びつけたのは我々が初めてである」という書き方は成立しない。ただし決定的な差分が二つある。第一に、この論文は物理的な秘密分散を要旨の応用の一覧に一語として挙げるだけであり、分散の閾値の設計や復元の手続きや脅威モデルには踏み込んでいない。第二に、読み出しには近赤外分光の走査器と計算機制御の平面描画機が必要であり、正当な利用者が手軽に読むという要件を満たさない。CipherFluteの新規性は「秘密分散との組み合わせを初めて考えた」ことではなく、「秘密分散を秘匿の唯一の担い手として明示的に据え、物理層の役割を探索コストの引き上げと読み出しの手軽さに限定した脅威モデルを書いた」ことに置き直すのが正確である。
- 脅威の度合いは**高**である。前段の全14切り口が見落としていた重大な先行例であり、新規性の主張の書き方を変える必要がある。

### 7-2. Source Identification of 3D Printer Based on Layered Texture Encoders

- 著者は Bo Seok Shim, Jae Hong Choe, Jong-Uk Hou である。
- 掲載は IEEE Transactions on Multimedia, 第25巻, pp.8240-8252, 2023年である。
- URLは https://doi.org/10.1109/TMM.2022.3233764 である。書誌はCrossrefで照合した。
- 要約すると、3Dプリント製品の出所を表面の検査による特徴だけから特定する法科学的な技法である。付加製造の過程で必然的に生じる極細の周期的な特徴を、高速フーリエ変換と変換器型符号器の位置符号化を組み合わせた二流の質感符号器（著者らはCFTNetと呼ぶ）で捉える。六つの出所特定の課題を定義し、SI3DP++という大規模な基準データ集合を示している。
- CipherFluteとの関係を述べると、CipherFluteは「印刷データに秘密がそのまま載るため、スライスと印刷はネットワークから切り離した自分の環境で行うことを推奨する」と述べている。この論文は、造形物の表面からどの機械で刷ったかを特定できることを示しており、印刷を自分の環境で行っても造形物自体から製造環境の情報が漏れうるという追加の脅威を意味する。脅威モデルの記述に反映する価値がある。
- 脅威の度合いは**中**である。新規性は脅かさないが、脅威モデルの完全性に関わる。

### 7-3. interiqr: Unobtrusive Edible Tags using Food 3D Printing、および EateryTag: investigating unobtrusive edible tags using digital food fabrication

- 著者は interiqr が Yamato Miyatake, Parinya Punpongsanon, Daisuke Iwai, Kosuke Sato であり、EateryTag が Yamato Miyatake, Parinya Punpongsanon である。
- 掲載は interiqr が Proceedings of the 35th Annual ACM Symposium on User Interface Software and Technology (UIST 2022), pp.1-11, 2022年10月28日であり、EateryTag が Frontiers in Nutrition, 第12巻, 2025年10月15日である。
- URLは https://doi.org/10.1145/3526113.3545669 および https://doi.org/10.3389/fnut.2025.1641849 である。書誌は両方Crossrefで照合した。
- 要約すると、interiqr は食品用3Dプリンタの充填条件を使い、モデルの形状を変えずに食品の内部に空気層や第二の材料で特定の模様を作り、人の目には見えにくい「食べられるタグ」として情報を格納する手法である。背面からの照明と単純な画像処理で復号する。EateryTag はその発展で、3Dプリンタによる方法に加えて型取りと押印による方法を作り、家庭の料理人3名との作業会で受け入れられやすさを確かめている。
- CipherFluteとの関係を述べると、日用品（この場合は食品）の外見と機能を損なわずに内部にタグを埋め込むという課題設定が完全に一致し、しかも「充填条件を使う」という手段までCipherFluteのスライサ設定の扱いと近い。日本のグループ（大阪大学）の研究である。
- 脅威の度合いは**中**である。読み出しが光学であり秘密の保管も誤り訂正も扱わないが、「日用品への偽装」という価値提案の先行例として、しかも国内の研究として引用が必要である。

### 7-4. Ninja Codes: Neurally Generated Fiducial Markers for Stealthy 6-DoF Tracking

- 著者は Yuichiro Takeuchi, Yusuke Imoto, Shunya Kato である。
- 掲載は arXiv:2510.18976 として2025年10月21日に公開され、2026年に第2版へ改訂されている。原文の注記に「CVPR 2026 Findings」と書かれているため、Computer Vision and Pattern Recognition 2026のFindings枠に採録されたものである。会議の予稿集としての書誌はまだ確認できなかった。
- URLは https://arxiv.org/abs/2510.18976 であり、著者が公開している紹介ページが https://sento.net/research/ninjacodes にある。著者、日付、採録先の注記はarXivの原文で照合した。
- 要約すると、任意の画像を視覚的に控えめな改変によって基準マーカーに変換する符号器の神経網を作り、印刷して面に貼ると現実の環境の質感に自然に紛れる基準マーカーになるという手法である。普通の色プリンタと普通の印刷用紙で作れ、現代的なRGBカメラを備えて推論を実行できる装置で検出できる。
- CipherFluteとの関係を述べると、「環境に紛れて目立たない符号」という価値提案が共通し、その最新の到達点を示す。日本人研究者による研究である。
- 脅威の度合いは**中**である。読み出しが光学であり、秘密の保管も情報量の議論もない。査読前のプレプリントなので、引用する場合はその旨を明記すべきである。

### 7-5. A Preliminary Study for Identification of Additive Manufactured Objects with Transmitted Images

- 著者は Kenta Yamamoto, Ryota Kawamura, Kazuki Takazawa, Hiroyuki Osone, Yoichi Ochiai である。
- 掲載は 2020年である。プレプリントは arXiv:2005.12027 として2020年5月25日に公開されており、Springerの論文集としての識別子は 10.1007/978-3-030-77772-2_29 である。
- URLは https://arxiv.org/abs/2005.12027 である。著者と公開日はarXivの原文で照合した。
- 要約すると、造形物の内部にバーコードを埋め込むのではなく、内部の支持構造の違いと製造誤差を含む透過像そのものを使って製品を識別する手法である。透過像のデータ集合が用意できれば90パーセントを超える正解率で識別できると報告している。
- CipherFluteとの関係を述べると、造形物の内部構造を情報の担体として扱う日本の研究であり、埋め込みを事前に計画しなくても個体を識別できるという逆向きの発想を示す。
- 脅威の度合いは**低**である。識別できるのは登録済みの個体であって任意のビット列ではない。

### 7-6. Artificial Markers: A Comprehensive Systematic Review and Design Framework

- 著者は Benedito Ribeiro Neto, Bianchi Meiguins, Tiago Araújo, Carlos dos Santos である。
- 掲載は ACM Computing Surveys, 第58巻第9号, pp.1-35, 2026年2月25日である。
- URLは https://doi.org/10.1145/3793661 である。書誌はCrossrefで照合した。
- 要約すると、雪だるま式の手法で選んだ88本の論文を体系的に調べ、基準マーカーの形式的な定義、内在的および外在的な性質、形態と算法の両面を覆う分類体系を作った総説である。AirCodeとInfraredTagsの両方を引いている。
- CipherFluteとの関係を述べると、造形物に載せる符号の分野を2026年に整理した最新の総説であり、CipherFluteが自分の位置を外部の分類体系で示すのに使える。ただし対象は視覚的な基準マーカーであり、音響は扱わない。
- 脅威の度合いは**低**である。

### 7-7. AirCodeの被引用のうち、既に前段で押さえられているもの

Secure Information Embedding in Forensic 3D Fingerprinting（USENIX Security 2024）、AnisoTag（CHI 2023）、StructCode（SCF 2023）、Claycode（ACM Transactions on Graphics 2025）、Seedmarkers（TEI 2021）、G-ID（CHI 2020）、LayerCode（SIGGRAPH 2019）、FabAuth（CHI EA 2019）、3D-Printed Object Identification Method using Inner Structure Patterns Configured by Slicer Software（CHI EA 2020）、How Can We Provide Additively Manufactured Parts with a Fingerprint?（Materials 2021）、Blind Watermarking for 3-D Printed Objects by Locally Modifying Layer Thickness（IEEE Transactions on Multimedia 2020）、Blind 3D-Printing Watermarking Using Moment Alignment and Surface Norm Distribution（同誌 2020）、QRコードを3D造形物へ埋め込む一連の研究（自己影を使うもの、穴を開けるもの、B-スプライン面に載せるもの、方向性のある光を使うもの、水平線に基づく環境遮蔽を使うもの）、Wireless Analytics for 3D Printed Objects（UIST 2018）、FibAR（IEEE Transactions on Visualization and Computer Graphics 2020）は、前段の調査（raw/01、raw/10、raw/11、raw/14）で既に扱われている。

--------------------------------------------------------------------------------

## 8. InfraredTags（CHI 2022、Doganら）を引用する後続研究

**得た被引用は67件、そのうち題名と書誌を67件すべて確認し、要旨まで読んだものは13件である。**

67件を通して見た結果、InfraredTagsの後続は**全件が光学の系統である**。赤外線マーカー、蛍光マーカー、偏光タグ、モアレタグ、赤外線インクの透かし、拡張現実の基準マーカー、視線計測というように、読み出しの物理はすべて光である。InfraredTagsの発想を音響へ渡した後続は1件も存在しない。CipherFluteの主張の一つである「読み出しが撮像でなく息と音である」という差分は、この否定的発見によって支えられる。

### 8-1. Weaving and Disguising Infrared Markers toward Invisible Textile Interaction

- 著者は Hal Sugiyama, Hsuanling Lee, Hanako Fujino, Mayuka Kuwana, Mustafa Doga Dogan, Liang He, Koya Narumi である。
- 掲載は Extended Abstracts of the 2026 CHI Conference on Human Factors in Computing Systems, pp.1-5, 2026年4月13日である。
- URLは https://doi.org/10.1145/3772363.3799013 である。書誌はCrossrefで照合した。
- 要約すると、赤外線マーカーを織物に織り込んで隠し、見えない織物の対話を実現する試みである。InfraredTagsの著者（Mustafa Doga Dogan）と日本の研究者（鳴海紘也さんら）の共同研究である。
- CipherFluteとの関係を述べると、造形物ではなく織物という別の日用品の類へ不可視の符号を移す最新の展開であり、CipherFluteのカードや本立てへの埋め込みと同じ「日用品への偽装」の系譜にある。日本のHCI分野の研究者が関わっているため投稿先の読者に近い。
- 脅威の度合いは**中**である。読み出しが光学であり情報量も秘密の議論もないが、2026年の最新の展開として引く価値がある。

### 8-2. GlintMarkers: Spatial Perception on XR Eyewear using Corneal Reflections

- 著者は Seungjoo Lee, Vimal Mollyn, Chris Harrison, Justin Chan, Mayank Goel である。
- 掲載は arXiv:2604.12949 として2026年4月14日に公開されたプレプリントである。査読を経た掲載は確認できなかった。
- URLは https://arxiv.org/abs/2604.12949 である。著者と公開日はarXivの原文で照合した。
- 要約すると、拡張現実の眼鏡に付いた内向きのカメラで角膜の反射を捉え、受動的な再帰反射マーカーが近赤外の光を角膜へ集めて作る輝点の模様から、タグを付けた物体の向きと距離の推定および固有の物体の識別を行う仕組みである。
- CipherFluteとの関係を述べると、受動的なマーカーを日常の物体に付ける路線の最新の一つである。
- 脅威の度合いは**低**である。査読前のプレプリントであり、情報量も秘密の議論もない。

### 8-3. InfraredTagsの被引用のうち、既に前段で押さえられているもの

BrightMarker（UIST 2023）とその実演版、AnisoTag（CHI 2023）、StructCode（SCF 2023）、Imprinto（CHI 2025）、Claycode（ACM Transactions on Graphics 2025）、interiqr（UIST 2022）、MoiréWidgets（CHI 2024）、3D Printed Pyrography（Additive Manufacturing 2024）、XR-Objects（UIST 2024）、It's Not the Shape, It's the Settings（CHI 2025）は、前段の調査で既に扱われているか、あるいは内容が離れている。

--------------------------------------------------------------------------------

## 9. 351件を横断した語句照合の結果（新規性の主張の根拠になる否定的発見）

8件の引用元を引く異なる論文351件すべての題名と要旨を対象に、四種類の語句照合をかけた。結果は次のとおりである。

**秘密分散と鍵保管に関わる語（secret sharing、Shamir、mnemonic、seed phrase、private key、key backup、BIP39）を含む論文は、351件中わずか1件である。** その1件が第7節の7-1に挙げた Near-infrared Imaging for Information Embedding and Extraction with Layered Structures（ACM Transactions on Graphics 2022）であり、要旨の応用の一覧に「physical secret sharing」を一語として挙げるだけである。したがって「造形物への情報埋め込みの分野で、秘密分散を秘匿の唯一の担い手として据えた設計は存在しない」と述べることは、この351件の範囲では正確である。ただし「秘密分散を応用として言及した例が皆無である」と述べるのは誤りになる。

**誤り訂正に関わる語（Reed-Solomon、error correction、BCH、Hamming code、parity、redundancy）を含む論文は351件中3件である。** Break-Resilient Codes（第3節の3-2）、Blind Watermarking for 3-D Printed Objects by Locally Modifying Layer Thickness、Fabricable Unobtrusive 3D-QR-Codes with Directional Light である。前者は符号理論の論文であり、後の二件はパリティを一言使うだけである。誤り訂正を正面から設計した後続は事実上Break-Resilient Codes系列だけであり、そのすべてが破断と欠損という光学および力学の欠損モデルに向いており、音高の読み違いという欠損モデルに向いたものは存在しない。

**笛と音高に関わる語（flute、whistle、fipple、recorder、pitch、semitone、wind instrument、Helmholtz）を含む論文は351件中4件である。** 語句照合では26件が引っかかったが、そのうち22件は「percent」や「center」の一部として「cent」が誤って一致したものであった。実質的に該当するのは FlueBricks（CHI 2026、flute と pitch）、An overview of additive manufacturing technologies for musical wind instruments（SN Applied Sciences 2021）、3D Virtual Reconstruction and Sound Simulation of an Ancient Roman Brass Musical Instrument（2020）、Printone の別版（ISMA 2017短縮版）の4件である。**「whistle」を含む論文は351件中0件であり、「fipple」を含む論文も0件であり、「semitone」を含む論文も0件である。** 半音刻みの格子を符号語彙とするという発想は、この8件の引用元の後続の系譜に一切現れない。

**吹奏と呼気に関わる語（blow、breath、exhale、puff）を含む論文は351件中9件である。** そのうち3Dプリントされた受動的な共鳴体を吹くものは、Blowhole自身、その著者の自己総括である Print-and-Play、そして FlueBricks の3件だけである。残る6件（Ubiquitous BlowClick、BREATHTURES、AirRes Mask、Breathin、BreathPrint、VibroAware）は人の呼気そのものを測る研究であり、物体側に符号を持たせない。

--------------------------------------------------------------------------------

## 10. 探したが存在しなかったこと

第9節の語句照合の結果に加えて、351件を目で確認する過程で次のことを確かめた。

第一に、電源も電子部品も持たない造形物の音を読んで、100ビットを超える利用者の秘密を運んだ後続研究は1件も存在しない。音響で情報を運ぶ後続のうち容量を数字で報告しているものは、Acoustic Voxels 自身の4ビットが最大である。

第二に、既知の音高を持つ基準となる素子を同じ物体に同居させ、他の素子をその比で読むという較正の構造を、造形物への情報埋め込みの文脈で採った後続研究は1件も存在しない。近いものは Owlet（MobiSys 2021）の参照用マイクによる環境変動の打ち消しだが、これは基準を物体側ではなく読み取り装置側に置く設計である。

第三に、隣り合う素子が同じ値を取ることを禁じる制約を、造形物への情報埋め込みの文脈で採った後続研究は1件も存在しない。Acoustic Barcodes 自身が0の連続を禁じる遷移保証を持っているが、その考え方を後続が引き継いだ例は見つからなかった。

第四に、Whooshの受動的な3Dプリント多管笛（FluteCase）を発展させた研究は、Whooshを引く44件のうち1件も存在しない。Blowholeが唯一の関連する後続であり、Blowholeは管ではなく球状のヘルムホルツ共鳴空洞を使う。

第五に、InfraredTagsを引く67件はすべて光学の系統であり、音響へ渡した後続は存在しない。

第六に、Printoneを引く42件のうち、狙った音高の並びを符号として読むものは存在しない。フィップル笛を扱う唯一の後続である FlueBricks は符号化を扱わない。

第七に、Lamelloのde Bruijn系列による符号設計を多ビットの情報搬送へ延ばした後続は、Lamelloを引く78件のうち1件も存在しない。

第八に、暗号資産の復元用情報（回復用の語句列や秘密鍵）を造形物へ保管することを扱った後続研究は、351件のうち1件も存在しない。MagCode（PACM HCI 2023）が「日常の支払い資格情報」を応用として挙げるのが最も近いが、これは磁気印刷であり造形物ではない。

--------------------------------------------------------------------------------

## 11. 残る穴

第一に、OpenAlexの利用枠が今日ぶん使い切られていたため、Semantic Scholarに登録されていない被引用を取りこぼしている可能性がある。とくにBlowholeの被引用17件とWhooshの被引用44件は、Semantic Scholarの登録件数がGoogle Scholarの表示件数より少ないことが知られている。OpenAlexの利用枠が回復する翌日以降に、8件それぞれの `cites:` 検索を実行して差分を取るべきである。Blowholeについては https://api.openalex.org/works?filter=doi:10.20380/GI2018.18 でWの番号を得たうえで `filter=cites:W番号` を引く手順になる。

第二に、Google Scholarの被引用一覧をこの環境から取得できず、被引用の網羅性を第三の情報源で確かめられなかった。

第三に、要旨を確認できなかった文献が5件残った。A Survey on Acoustic Sensing in the Metasurface Era（Fundamental Research 2025）、Acoustic barcode based on the acoustic scattering characteristics of underwater targets（Applied Acoustics 2022）、Estimation of fused-filament-fabrication structural vibro-acoustic performance by modal impact sound（Computers and Graphics 2023）、EchoSnap and PlayableAle（TEI 2017）、Assessment on the use of additive manufacturing technologies for acoustic applications（2020）である。いずれも題名と掲載誌の書誌までは一次情報で確認したが、内容の要約は書誌情報の範囲を超えていない。引用する前に本文を取得すべきである。

第四に、二次の被引用（今回見つけた後続研究を引く、さらにその後続）をまったくたどっていない。とくに第7節の7-1（Near-infrared Imaging、物理的な秘密分散に言及）と第6節の6-1（Tubes Among Us）と第3節の3-1（Keynergy）と3-2（Break-Resilient Codes）の4件は、CipherFluteの新規性の核心に触れるため、この4件の被引用をたどる価値が高い。

第五に、Semantic Scholarに学術資源識別子が登録されていない記録が351件のうち十数件あり（学位論文や技術報告と思われる）、これらの書誌を確定できていない。

第六に、日本語の後続研究をこの経路では拾えない。Semantic ScholarもCrossrefも、WISSやインタラクションや情報処理学会研究報告の発表を被引用として登録していない。前段の調査（raw/05）が指摘した国内の予稿集を年ごとにめくる作業は、この作業では代替できていない。

第七に、特許の被引用（前方引用）をまったく調べていない。Google Patentsの個別特許ページには引用している後続特許の一覧があるので、Acoustic BarcodesやAirCodeに対応する特許があればそこから追える可能性がある。

--------------------------------------------------------------------------------

## 12. 執筆への提言（要点だけ）

この作業の結果を論文に反映するとき、優先度の高い変更は次の4点である。

第一に、Near-infrared Imaging for Information Embedding and Extraction with Layered Structures（ACM Transactions on Graphics 2022）を引用し、「物理的な秘密分散」という応用が2022年に言及されていることを認めたうえで、CipherFluteの差分を「秘密分散を秘匿の唯一の担い手として据え、物理層の役割を探索コストの引き上げと読み出しの手軽さに限定した脅威モデルを明示的に書いた点」に置き直す。

第二に、Tubes Among Us（USENIX Security 2023）とKeynergy（USENIX Security 2021）を脅威モデルの節で引用する。前者は3Dプリントの管の音響が安全性の系を欺くほど制御可能であることを示し、後者は物理鍵の秘密が音から推定できることを示す。この二件を引くことで「音や物体の層には暗号学的な秘匿の力はまったく無い」という宣言に実証的な裏づけが付く。

第三に、Break-Resilient Codes（IEEE Transactions on Information Theory）とSecure Information Embedding in Forensic 3D Fingerprinting（USENIX Security 2024）を並べて引用し、造形物という媒体に固有の欠損に対する符号設計が理論の側でも整備されていることを認めたうえで、CipherFluteの符号層の貢献を「音高の読み違いという欠損モデルに向けてReed-Solomon符号を実装した工学の側」に限定して述べる。

第四に、Whooshを引用する。第2節で示したとおり、WhooshのFluteCaseを継承した研究は44件の後続のうち1件も存在せず、BlowholeがWhooshを引いているという系譜が文献上に実在する。CipherFluteがBlowholeを引きながらWhooshを引かない現状は系譜の一段を飛ばしているように見えるが、逆にWhooshを引いたうえで「Whooshが素描に留めた受動多管笛を、符号語彙として設計し直した最初の研究である」と書けば、脅威が新規性の根拠に転じる。
