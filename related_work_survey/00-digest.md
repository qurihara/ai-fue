# 切り口別の調査結果ダイジェスト（2026年7月30日、14の切り口の探索と検証の結果を機械的に集約したもの）

各切り口の生の調査記録は raw/ にある。この文書は各担当が返した要約・脅威の大きい文献・調べ残した穴を並べたものである。

==========================================================================================
## [01-fab-embed-optical] 造形物への情報埋め込み（光学読み取り）  (確認42 / 未検証5 / 訂正38 / 削除0)

### 要約
この切り口は2013年のInfraStructs以降十年以上積み上がっており、「消費者向けFDMプリンタで日用品に情報を仕込み、電子部品も電源も使わずに読み出す」という枠組み自体はまったく新しくない。到達点を数字で示すと、AirCodeは2センチメートル角に約106ビット、5センチメートル角に500ビット超を収め、しかもリードソロモン符号で40パーセントの冗長度を与えている。InfraredTagsは赤外線透過フィラメントと内部空隙で21×21のQRコードを物体内部に隠す。AnisoTagはクレジットカードと同寸の面に51ビットから160ビットを刻み、読み取り装置は10ドル程度で作れる。上平員丈らは2015年から、造形物内部の空洞や近赤外蛍光染料や強磁性セルに数百ビットを入れ、X線・サーモグラフィ・近赤外線で非破壊に読む研究を続けている。Iyerらは2017年に鉄粉入りフィラメントの磁界にデータを埋め、市販スマートフォンの磁力計で復号している。一方で全論文に共通する空白がはっきり見えた。第一に脅威モデルを明示した研究がほぼ皆無で、例外は2024年のSecure Information Embedding in Forensic 3D Fingerprintingだけである。第二に読み出しに所有者の身体的な行為を要する設計が存在せず、光学系はすべて撮像だけで受動的に読める。第三に秘密分散や暗号鍵の保管を目的に設計された造形タグは見つからなかった。第四に基準素子による正規化も隣接同値禁止も前例がない。CipherFluteの新規性は埋め込みそのものではなくこの四点に置くのが正確である。なおリードソロモン符号の採用はAirCodeに前例があるため新規性として主張できない。

### 脅威の大きい文献
- 【高】InfraredTags: Embedding Invisible AR Markers and Barcodes Using Low-Cost, Infrared-Based 3D Printing and Imaging Tools
  著者: Mustafa Doga Dogan, Ahmad Taka, Michael Lu, Yunyi Zhu, Akshat Kumar, Aakar Gupta, Stefanie Mueller
  掲載: ACM CHI 2022, pages 269:1-269:12
  URL: https://dblp.org/search/publ/api?q=InfraredTags&format=json
  関係: 赤外線を透過するフィラメントと内部空隙で、日用品の外見をまったく変えずに21×21のQRコード（数字25文字）を物体内部へ埋め込み、近赤外カメラモジュールを付けたスマートフォンで読み出す。消費者向けFDMプリンタで電子部品も電源も使わず日用品に機械可読情報を仕込むという枠組みがCipherFluteと完全に一致する。容量も笛40本から49本ぶんの128ビットを大きく上回る。
  脅威理由: 隠蔽性と情報量の両面でCipherFluteより優れた手段が同じ枠組みですでに存在するため、日用品への偽装という価値提案が大幅に弱まる。差分は特殊フィラメント不要、追加撮像装置不要、読み出しが所有者の行為と結びつく点に限られる。
- 【高】Embedding Information into Objects Fabricated With 3-D Printers by Forming Fine Cavities inside Them（上平員丈・鈴木雅洋らの一連の研究の代表）
  著者: Masahiro Suzuki, Pailin Dechrueng, Soravit Techavichian, Piyarat Silapasuphakornwong, Hideyuki Torii, Kazutake Uehira
  掲載: IS&T International Symposium on Electronic Imaging (Media Watermarking, Security, and Forensics), vol.29, pp.6-9, 2017
  URL: https://library.imaging.org/ei/articles/29/7/art00002
  関係: 造形中に物体内部へ微小空洞・高反射突起・近赤外蛍光染料・強磁性セルを作り込み、X線・サーモグラフィ・近赤外線・磁力計で非破壊に読み出す。数センチメートルの造形物に数百ビットを埋め込めると明記している。CipherFluteが管の長さという内部空洞で符号を表すのは、この枠組みの音響版と読める。
  脅威理由: 内部空洞に数百ビットを入れて非破壊で読むという主張が2015年から確立しており、著作権保護という安全性寄りの動機まで持つ。CipherFluteは読み出しが撮像でなく息と音である意味を独立に説明しなければならない。
- 【中】AnisoTag: 3D Printed Tag on 2D Surface via Reflection Anisotropy
  著者: Zehua Ma, Hang Zhou, Weiming Zhang
  掲載: ACM CHI 2023
  URL: https://ar5iv.labs.arxiv.org/html/2301.10599
  関係: 3Dプリント表面の異方性反射を使い、クレジットカードと同一寸法（53.98×85.6ミリメートル）の面に51ビット、画像処理併用で160ビットを刻む。読み取り装置は3ドルのレーザーポインタと16個のフォトレジスタと7ドルのマイクロコントローラで作れる。
  脅威理由: CipherFluteのカード型実装と形状も面積も一致し、同じ面積により多くのビットをより目立たない形で刻めるため、カード1枚あたりの容量が直接比較される。ただし専用治具が要る点は差分になる。
- 【中】BrightMarker: 3D Printed Fluorescent Markers for Object Tracking
  著者: Mustafa Doga Dogan, Raul Garcia-Martin, Patrick William Haertel, Jamison John O'Keefe, Ahmad Taka, Akarsh Aurora, Raul Sanchez-Reillo, Stefanie Mueller
  掲載: ACM UIST 2023
  URL: https://api.semanticscholar.org/graph/v1/paper/DOI:10.1145/3586183.3606758
  関係: 赤外蛍光フィラメントで入射光の波長をずらし、物体表面の色によらず高コントラストでマーカーを検出する。1インチ角でも2メートル以上離れて追跡でき、既存の不可視マーキングを検出率で上回ると主張している。日用品に見えない印を埋める路線の最新到達点にあたる。
  脅威理由: 主眼が追跡であり少量の秘密情報の保管とは目的が異なるが、不可視埋め込みの性能水準を示す基準となるため、隠蔽性を論じる際に必ず引用して差分を述べる必要がある。
- 【中】3D printing wireless connected objects
  著者: Vikram Iyer, Justin Chan, Shyamnath Gollakota
  掲載: ACM Transactions on Graphics, vol.36, 2017（SIGGRAPH Asia 2017）
  URL: https://api.semanticscholar.org/graph/v1/paper/DOI:10.1145/3130800.3130822
  関係: 電池も電子部品も使わず市販プリンタと市販フィラメントだけで無線通信する物体を作る研究であり、鉄粉入りフィラメントで磁界の形にデータを埋め込み、市販スマートフォンの磁力計で復号する仕組みを含む。眼鏡フレームや腕輪に磁気データを埋めた例がある。
  脅威理由: 電源不要・電子部品不要・市販端末で読めるというCipherFluteの主張を2017年にすでに達成している。差分は特殊な鉄粉入りフィラメントが不要である点と、笛が意匠に溶け込む点に絞られる。
- 【中】InfoPrint: Embedding Interactive Information in 3D Prints Using Low-Cost Readily-Available Printers and Materials
  著者: Weiwei Jiang, Chaofan Wang, Zhanna Sarsenbayeva, Andrew Irlitti, Jing Wei, Jarrod Knibbe, Tilman Dingler, Jorge Goncalves, Vassilis Kostakos
  掲載: Proceedings of the ACM on Interactive, Mobile, Wearable and Ubiquitous Technologies (IMWUT), vol.7, no.3, 2023
  URL: https://api.semanticscholar.org/graph/v1/paper/DOI:10.1145/3610933
  関係: 安価な市販デュアルエクストルーダFDMプリンタと一般的なPLAだけで、材料の熱特性の差により情報を埋め込む。人が物体に触れて温度を移したあと、サーマルカメラ付きスマートフォンで撮ると情報が現れる。人間の行為が読み出しの引き金になる点がCipherFluteの「吹く」に最も近い。
  脅威理由: 特殊材料を使わず一般材料だけで日用品に情報を隠す点と、人間の行為を読み出しに組み込む点の二つで先行しているため、CipherFluteの同種の論点は差分を丁寧に書く必要がある。
- 【中】内部構造パターンの差異を利用した3Dプリントオブジェクト識別手法
  著者: 久保勇貴、江口佳那、青木良輔、近藤重邦、東正造、犬童拓也（日本電信電話株式会社）
  掲載: WISS 2019（第27回インタラクティブシステムとソフトウェアに関するワークショップ）
  URL: https://www.wiss.org/WISS2019Proceedings/
  関係: スライサの内部充填パターン設定を変えて外見が同一の造形物に識別情報を持たせ、加振したときの振動特性の違いで識別する。8種類の識別で99.3パーセントの精度を報告している。読み出しにはピエゾ素子を用いる。
  脅威理由: 投稿先であるWISSに「造形物の内部構造に情報を持たせ、力学的・音響的な現象で読み出す」論文が既に存在し、同じ日本のコミュニティで査読者が想起しやすい。ただし少数クラスの識別でありビット列の格納ではない点は差分になる。
- 【中】Secure Information Embedding in Forensic 3D Fingerprinting
  著者: Canran Wang, Jinwen Wang, Mi Zhou, Vinh Pham, Senyue Hao, Chao Zhou, Ning Zhang, Netanel Raviv
  掲載: arXiv preprint arXiv:2403.04918, 2024年（2025年2月改訂）
  URL: https://arxiv.org/abs/2403.04918
  関係: 3Dプリント造形物への情報埋め込みに、破断と断片の隠匿を行う敵という明示的な脅威モデルを置き、欠損に耐える符号理論的な設計とTrusted Execution Environmentによる保護を与えている。目的は追跡不能な偽造品の製造を防ぐことである。
  脅威理由: 造形物への情報埋め込みに明示的な攻撃者モデルと符号理論を持ち込んだ数少ない例であり、「この分野で脅威モデルを明示したのは我々が初めてである」という書き方は成立しなくなる。目的が正反対なので主張自体は衝突しない。

### 調べ残した穴
Web検索の呼び出し予算をセッション途中で使い切ったため、後半は既知URLへのWebFetchのみで進めた。その結果、2024年から2026年のSCF、UIST、TEI、Graphics Interfaceの予稿集を一件ずつ走査する作業が残っている。日本語文献も網羅が不十分で、電子情報通信学会と画像電子学会の技術研究報告は題名までしか確認できておらず、画像電子学会誌2023年の第52巻第1号（デジタルファブリケーション特集）の目次はファイルが大きすぎて取得に失敗した。WISSは2019年の一件しか確認できておらず、2020年から2025年の予稿集とインタラクションのプログラムを年ごとに開く必要がある。Semantic ScholarのAPIで呼び出し回数制限に繰り返し当たり、AirCode・InfraredTags・LayerCodeの被引用一覧をたどる作業に到達できなかったため、API鍵を用意して後続研究を機械的に列挙し直すべきである。材料科学側の偽造防止タグ（アップコンバージョン蛍光体、量子ドット、プラズモニック粒子による物理的複製困難関数）は家庭用プリンタで作れないと判断して深追いしなかった。特許も未調査で、検索の過程で「Using everyday objects as cryptographic keys」など着想の近い米国特許が繰り返し現れたため、必要なら別途調べるべきである。

==========================================================================================
## [02-passive-acoustic-tags] 受動的な音響タグと音で読む物体  (確認37 / 未検証7 / 訂正20 / 削除0)

### 要約
受動的な音響タグの研究は動作の種類でこする系、はじく系、叩く系、吹く系、剥がす系、機械的に弾いて超音波を出す系に分かれ、別系統として表面弾性波タグ、水中受動音響識別タグ、音響メタマテリアル識別タグがある。CipherFluteにとって最も危険なのは三件である。Whoosh（ISWC 2016）のFluteCaseは、長さの異なる8本の閉管を並べた受動的な3Dプリント構造を吹いて8つの音高で識別し、管長を半音比の等比数列で決め、しかも認証への応用まで述べている。にもかかわらず現在の論文はこれを引用していない。Acoustic Barcodes（UIST 2012）は受動音響タグに6ビットから24ビットの符号を載せ、ガード列、0の連続を禁じる遷移保証、BCH符号やReed-Solomon符号による誤り訂正を具体的に論じており、CipherFluteの符号層の要素がほぼ出そろっている。Blowhole（GI 2018）は3Dプリント物の空洞を吹いて最大9個のタグを98パーセントで識別する。一方、100ビットを超える秘密の値を電源なしの可聴音タグで運んだ例、半音格子を符号語彙とした例、基準音で環境変動を比で打ち消す設計、誤り訂正を実装した動作系、暗号学的脅威モデルを明示して秘匿性を秘密分散に委ねる議論は、いずれも見つからなかった。

### 脅威の大きい文献
- 【高】Whoosh: non-voice acoustics for low-cost, hands-free, and rapid input on smartwatches（受動3Dプリント時計ケース FluteCase を含む）
  著者: Gabriel Reyes, Dingtian Zhang, Sarthak Ghosh, Pratik Shah, Jason Wu, Aman Parnami, Bailey Bercik, Thad Starner, Gregory D. Abowd, W. Keith Edwards
  掲載: Proceedings of the 2016 ACM International Symposium on Wearable Computers (ISWC '16), pp. 120-127, 2016年
  URL: https://sites.cc.gatech.edu/fac/keith/pubs/iswc2016-whoosh.pdf
  関係: 長さの異なる8本の閉管を並べた受動的な3Dプリント構造（FluteCase）を吹き、2キロヘルツから10キロヘルツの8つの音高で位置を識別する。管長は半音比の等比数列で決められており、CipherFluteの物理機構および音高設計とほぼ一致する。さらに一連の吹奏イベント列を端末のロック解除や購入承認の物理的チャレンジに使う認証構想まで論文中で述べている。
  脅威理由: 受動的な3Dプリント多管笛を吹いて音高で識別するというCipherFluteの物理機構の新規性がほぼ消える。しかも認証という安全性の文脈にまで踏み込んでいるうえ、現在の論文はこの文献を一切引用していないため、査読で指摘された場合の打撃が大きい。
- 【高】Acoustic Barcodes: Passive, Durable and Inexpensive Notched Identification Tags
  著者: Chris Harrison, Robert Xiao, Scott E. Hudson
  掲載: Proceedings of the 25th Annual ACM Symposium on User Interface Software and Technology (UIST '12), pp. 563-568, 2012年
  URL: https://www.chrisharrison.net/projects/acousticbarcodes/AcousticBarcodes.pdf
  関係: 受動音響タグに6ビットから24ビットの二進符号を載せ、前後にガード列を置き、固定物理長方式では0の連続を禁じて必ず遷移が起きるようにしている。さらにBCH符号やReed-Solomon符号やHamming符号による誤り訂正を具体的に計算しており、CipherFluteが符号層で主張しうる三要素（基準、遷移保証、誤り訂正）がすべて先取りされている。
  脅威理由: 受動音響タグに符号設計と誤り訂正を持ち込んだという水準の主張が成立しなくなる。現在の論文は引用しているが、遷移保証と誤り訂正の設計論がすでに詳細に論じられていることを踏まえた差分の書き方をしないと符号層の貢献が否定されかねない。
- 【高】Blowhole: Blowing-Activated Tags for Interactive 3D-Printed Models
  著者: Carlos Tejada, Osamu Fujimoto, Zhiyuan Li, Daniel Ashbrook
  掲載: Proceedings of the 44th Graphics Interface Conference (GI 2018), pp. 122-128, 2018年
  URL: http://graphicsinterface.org/wp-content/uploads/gi2018-18.pdf
  関係: 3Dプリント物の内部に球状の空洞と直管を彫り、軽く吹いて生じるヘルムホルツ共鳴の音高で最大9個のタグを識別する。管長2.5ミリメートルで球径8から28ミリメートルの6種類なら利用者非依存で98パーセントの精度が出る。サポート材なしで印刷でき後加工も組み立ても不要という点までCipherFluteと重なる。
  脅威理由: 電源なしの3Dプリント物を吹いて音高で符号を読むという着想の直接の先行研究である。各穴が独立した識別子であり符号語を成さないこと、誤り訂正も基準音も秘密情報の議論もないことを数字で示さないと、増分的な改良と見なされる危険が高い。
- 【中】Lamello: Passive Acoustic Sensing for Tangible Input Components
  著者: Valkyrie Savage, Andrew Head, Björn Hartmann, Dan B. Goldman, Gautham Mysore, Wilmot Li
  掲載: Proceedings of the 33rd Annual ACM Conference on Human Factors in Computing Systems (CHI '15), pp. 1277-1280, 2015年
  URL: https://people.eecs.berkeley.edu/~bjoern/papers/savage-lamello-chi2015.pdf
  関係: 長さの異なる櫛歯をはじいて生じる基本周波数（924から3824ヘルツ）を記号として使い、de Bruijn系列で符号語を設計している。音高を符号記号とし符号設計まで踏み込んだ受動音響部品の先行例であり、周波数域もCipherFluteと大きく重なる。2キロヘルツ以上で識別率が下がるという報告も含む。
  脅威理由: 音高を記号とする受動音響符号という枠組みが先行しているため必ず引用して差分を述べる必要がある。ただし運ぶ情報はスライダ位置などの状態であって任意のビット列ではなく、誤り訂正も秘密情報の視点もない。
- 【中】Acoustic Voxels: Computational Optimization of Modular Acoustic Filters
  著者: Dingzeyu Li, David I. W. Levin, Wojciech Matusik, Changxi Zheng
  掲載: ACM Transactions on Graphics, 第35巻第4号, pp. 1-12, 2016年（SIGGRAPH 2016）
  URL: https://www.cs.columbia.edu/cg/lego/acoustic-voxels-siggraph-2016-li-et-al.pdf
  関係: 3Dプリント物の音響応答にビット列を埋め込み、スマートフォンで叩いた音から復号するという骨格がCipherFluteと一致する。ただし実証された容量は透過損失曲線を使った4ビットにとどまり、音響タグの例も外見の同じ豚の置物3体の識別である。誤り訂正も基準による正規化も秘密情報の視点もない。
  脅威理由: 着想としては最も近い部類だが実証容量が4ビットと桁違いに小さく、128ビットの秘密を運ぶという主張は直接には脅かされない。既に引用済みなので4ビットという数字を明示して規模の差を書くべきである。
- 【中】SoundOff: Low-cost Passive Ultrasound Tags for Non-invasive and Non-Intrusive Smart Home Sensing
  著者: Yibo Fu, Vivian Shen, Víctor Riera Naranjo, Bolei Deng, Alex Adams, Josiah Hester
  掲載: Proceedings of the ACM on Interactive, Mobile, Wearable and Ubiquitous Technologies, 第9巻第4号, 論文番号174, pp. 1-32, 2025年
  URL: https://par.nsf.gov/biblio/10670927-soundoff-low-cost-passive-ultrasound-tags-non-invasive-non-intrusive-smart-home-sensing
  関係: 電池も電子部品も持たない3Dプリント製タグの片持ち梁が金属円板を弾き、形状に固有の超音波を出す。幾何設計を系統的に変えることで識別容易な設計を数千通り生成できると主張しており、CipherFluteの13スロットという語彙より桁違いに大きい。
  脅威理由: 2025年の最新研究として審査員が想起しやすく、識別可能な設計数の大きさでCipherFluteの語彙設計が見劣りしうる。ただしタグ1個が1識別子であり符号語も誤り訂正も秘密情報の視点もない。
- 【中】Artificial Intelligence in Metamaterial Informatics for Sonic Frequency Mechanical Identification Tags
  著者: Daniel Saatchi, Myung‐Joon Lee, Tushar Prashant Pandit, Manmatha Mahato, Il‐Kwon Oh
  掲載: Advanced Functional Materials, 第35巻, 2025年（オンライン公開は2024年）
  URL: https://doi.org/10.1002/adfm.202414670
  関係: 三重周期極小曲面をもとにした3Dプリントのフォノニック構造で「符号化された機械式識別タグ」を作り、深層学習の音響分類器で楽器の所有者を識別する。著者らはこれを第一世代の受動的ソニック周波数識別トランスポンダタグと位置づけている。
  脅威理由: 材料科学側から受動ソニック識別タグという枠を正面から立てた最新の研究であり、引用しないと分野横断の目配りを欠くと見なされる。ただしビット数や誤り訂正の有無は要旨からは読み取れず、秘密情報の視点も見当たらない。
- 【中】Surface Acoustic Wave RFID Tags（章）ならびに Review on SAW RFID tags（総説）
  著者: Sanna Härmä, Victor P. Plessky（章）／ Victor P. Plessky, Leonhard M. Reindl（総説）
  掲載: 章は書籍 Development and Implementation of RFID Technology（InTech, 2009年）第8章。総説は IEEE Transactions on Ultrasonics, Ferroelectrics, and Frequency Control, 第57巻, pp. 654-668, 2010年
  URL: https://cdn.intechopen.com/pdfs/6032/InTech-Surface_acoustic_wave_rfid_tags.pdf
  関係: 完全に受動的な音響素子に多ビット符号を載せる確立した技術である。10個の反射器のうち最初と最後を基準とチェックサムに充て、時間位置符号化で4のn乗通り、位相符号化を加えると40ビット相当まで到達する。実用容量は32ビットから128ビットである。CipherFluteの基準笛と誤り訂正に相当する設計が既に存在する。
  脅威理由: 受動音響タグの多ビット符号化という一般論は工学分野に確立した先行例があるため、符号設計そのものを新規と主張できない。ただし読み出しに無線送受信機が要り可聴音でもなく、格納するのは工場で決まる識別子であって利用者の秘密ではない。

### 調べ残した穴
検索の予算を使い切ったため、最後に予定していた二件の確認ができなかった。一つは物理鍵の音響推定攻撃のUSENIX Security 2021版であり、もう一つは「音で読める秘密の物理バックアップ」という直球の検索である。後者は新規性の中心に関わるため優先して埋めるべき穴である。またBlowholeの被引用はSemantic Scholar上で17件しか登録されておらず、Google Scholarの被引用一覧を参照できなかったため2023年以降の造形分野の新しい引用を取りこぼしている可能性がある。Acoustic Barcodesの被引用99件は一覧を取得したものの個別確認はしておらず、とくにSplitcode（2022年）、Secure Information Embedding in Forensic 3D Fingerprinting（USENIX Security 2024）、All-in-one encoder/decoder approach for non-destructive identification of 3D-printed objects（2022年）は造形物への情報埋め込みと安全性を扱っており追跡の価値がある。特許を体系的に検索しておらず、玩具や包装の分野に「吹くと音が出る識別子」の先行技術がある可能性が残る。中国語と韓国語の文献、および医療用インプラントの超音波受動識別子も未探索である。日本語文献はCiNii Researchを三語で引いたのみで、情報処理学会電子図書館、電子情報通信学会技術研究報告、WISSとインタラクションの各年の予稿集を直接めくる作業を行えていない。犬笛や汽笛など実用品としての多音高吹奏具の先行技術も調べていない。

==========================================================================================
## [03-printed-wind-instruments] 3Dプリントされた笛と気鳴楽器の計算設計  (確認35 / 未検証7 / 訂正21 / 削除0)

### 要約
この切り口で最も危険な先行研究はSIGGRAPH Asia 2016のPrintoneである。任意の自由形状を中空化し、境界要素法で共鳴周波数を予測しながらフィップル吹き口と指孔を配置して家庭用FDM機で印刷し、16本の楽器で56個の目標周波数のうち53個が実測範囲に入ったと報告している。つまり印刷できる笛の形を計算して狙った音高に合わせ実機で検証する工程は既に達成済みであり、しかも現行のCipherFluteはこれを引用していない。これがこの調査で見つかった最大の穴である。音高精度をセント単位で報告した査読文献はNIME 2016のDabinらがほぼ唯一で、印刷したリコーダーで初版が+6から+34セント、手修正版が-13から+14セント、目標として5セント以内を掲げている。この数値はCipherFluteが100セント刻みのスロットと基準笛較正を選んだ判断を外部から裏づける。設計道具としてはdemakeinとopenwindが存在し、管形状の最適化も音から形状を復元する逆問題も確立している。一方で、印刷した笛の音高を符号として読み、複数本の並びで情報を運ぶ研究、基準笛を同居させて比で読む較正、遷移保証や誤り訂正を形状設計に持ち込む発想は、いずれも見つからなかった。日本語圏には該当研究が存在しない。

### 脅威の大きい文献
- 【高】Printone: Interactive Resonance Simulation for Free-form Print-wind Instrument Design
  著者: Nobuyuki Umetani, Athina Panotopoulou, Ryan Schmidt, Emily Whiting
  掲載: ACM Transactions on Graphics 35(6), pp.1-14, 2016 (SIGGRAPH Asia 2016)。短縮版は International Symposium on Musical Acoustics 2017, pp.18-21
  URL: https://doi.org/10.1145/2980179.2980250
  関係: 任意形状を中空化し、境界要素法で共鳴周波数を予測しながらフィップル吹き口と指孔を配置し、家庭用FDM機で印刷して旋律を演奏させている。16本を製作し、56個の目標周波数のうち53個が実測範囲に入ったと報告している。CipherFluteが行う「印刷できる笛の形を計算して狙った音高に合わせ、実機で検証する」工程を10年前に達成している。
  脅威理由: CipherFluteの計算設計という技術的貢献をほぼ完全に先取りしており、しかも現行論文の引用一覧に入っていない。査読者に最も基本的な先行研究の見落としと受け取られる危険が最大である。
- 【高】Blowhole: Blowing-Activated Tags for Interactive 3D-Printed Models
  著者: Carlos Tejada, Osamu Fujimoto, Zhiyuan Li, Daniel Ashbrook
  掲載: Proceedings of Graphics Interface 2018, pp.131-137, 2018
  URL: https://doi.org/10.20380/GI2018.18
  関係: 印刷物内部のヘルムホルツ共鳴空洞に息を吹き込み、鳴った音の高さから計算機がどの穴かを同定する。識別できるクラス数は9個程度で、正解率は約98パーセントから90パーセントに低下する。読み出しの一次的な仕組みがCipherFluteと共通するが、系列符号化・誤り訂正・基準音較正・秘密保管の発想はない。
  脅威理由: 「印刷物に吹いて音高から情報を読む」という中核の仕組みが最も近い。既に引用されているが、ヘルムホルツ共鳴と開管共鳴の違い、識別クラス数と系列長、較正と誤り訂正の有無を数値で書き分けないと差分が説明できない。
- 【中】Demakein: design and make instruments
  著者: Paul Francis Harrison
  掲載: オープンソースソフトウェア、2014年公開、バージョン1.1を2025年7月公開(査読論文ではない)
  URL: http://www.logarithmic.net/pfh/design
  関係: 与えた運指と音階に対して管の断面形状と指孔の位置・径・深さを数値最適化し、3DプリンタやCNCで作れる形に変換する。フルート、ホイッスル(フィップル笛)、ショームが組み込みで用意されている。CipherFluteの管長と周波数の対応づけは、この道具が扱う設計問題の最も単純な部分集合にあたる。
  脅威理由: 査読論文ではないため学術的先行性の主張は弱いが、デジタルファブリケーションの査読者には広く知られており、計算による笛の設計を新規性に掲げると即座に反証される。
- 【中】3D Modelling and Printing of Microtonal Flutes
  著者: Matthew Dabin, Terumi Narushima, Stephen Beirne, Christian Ritz, Kraig Grady
  掲載: Proceedings of NIME 2016, pp.286-290, 2016
  URL: https://nime.org/proc/nime2016_dabin/
  関係: Benade由来の簡略音響モデルで管端補正を積み上げて指孔位置と径を決め、PolyJet方式でリコーダーを印刷している。目標との差をセントで報告しており、初版が+6から+34セント、次版が-40から+1セント、やすりで手修正した版が-13から+14セント、目標として5セント以内を掲げている。CipherFluteが100セント刻みのスロットと基準笛較正を選んだ根拠を外部数値で裏づける。
  脅威理由: 主要な主張は崩れないが、印刷した笛の音高精度をセント単位で評価する方法自体は新しくないため、必ず引用して自分の実測値と並べて示す必要がある。
- 【中】FlueBricks: A Construction Kit of Flute-like Instruments for Acoustic Reasoning
  著者: Bo-Yu Chen, Chiao-Wei Huang, Lung-Pan Cheng
  掲載: Proceedings of the 2026 CHI Conference on Human Factors in Computing Systems, 18 pages, 2026
  URL: https://doi.org/10.1145/3772318.3790595
  関係: フィップル笛を生成部・共鳴部・連結部に分解し、FFF方式(PLAとTPU)で印刷したモジュールを組み替えて音響的な理解を促す構築キットである。目標周波数の計算も情報符号化も扱わない。本文中でPrintoneとAcoustic Voxelsを計算設計研究として明示的に位置づけている。
  脅威理由: 同年のCHIで同じ3Dプリントのフィップル笛を扱う最新研究であり、引用しないと調査不足に見える。この論文が引く計算設計研究とCipherFluteの引用一覧の食い違いも目立つ。
- 【中】Woodwind instrument design optimization based on impedance characteristics with geometric constraints / Full waveform inversion for bore reconstruction of woodwind-like instruments
  著者: Augustin Ernoult, Christophe Vergez, Samy Missoum, Philippe Guillemain, Michael Jousserand / Augustin Ernoult, Juliette Chabassier, Samuel Rodriguez, Augustin Humeau
  掲載: The Journal of the Acoustical Society of America 148(5), pp.2864-2877, 2020 / Acta Acustica 5, article 47, 2021
  URL: https://doi.org/10.1121/10.0002449
  関係: 管形状と側孔位置を目標の共鳴特性に合わせて最適化する順問題と、測定した音響応答から管の内径分布を復元する逆問題の両方が確立している。実装はInriaのopenwindとして公開されている。CipherFluteの脅威モデル(形状を計測されれば無音で読める)を裏づけると同時に、音の測定だけでも形状推定が可能でありうることを示唆する。
  脅威理由: 符号化の主張は崩れないが、管長から周波数を求める計算が既存技術であることを明確にし、物理層に秘匿性がないという宣言を補強するために引用が必要である。
- 【中】Aerophones in Flatland: Interactive Wave Simulation of Wind Instruments
  著者: Andrew Allen, Nikunj Raghuvanshi
  掲載: ACM Transactions on Graphics 34(4), pp.1-11, 2015 (SIGGRAPH 2015)
  URL: https://doi.org/10.1145/2767001
  関係: 二次元に落とした管楽器の波動方程式を直接解き、毎秒128000サンプルで全帯域の音を実時間合成する。リードや唇の非線形励振を結合でき、指孔の開閉や吹く圧力を制御できる。物理製作ではなく音響合成が目的である。
  脅威理由: 情報符号化とは無関係だが、気鳴楽器を計算機で扱う代表的研究であり、Printoneと並べて背景に置かないと網羅性を欠く。
- 【中】ProtoHole: Prototyping Interactive 3D Printed Objects Using Holes and Acoustic Sensing / FabAuth: Printed Objects Identification Using Resonant Properties of Their Inner Structures
  著者: Shohei Katakura, Keita Watanabe / Yuki Kubo, Kana Eguchi, Ryosuke Aoki, Shigekuni Kondo, Shozo Azuma, Takuya Indo
  掲載: Extended Abstracts of CHI 2018, pp.1-6, 2018 / Extended Abstracts of CHI 2019, pp.1-6, 2019
  URL: https://doi.org/10.1145/3290607.3313005
  関係: いずれも3Dプリント物体の内部空洞や内部構造の共鳴を音で読む研究である。ProtoHoleは穴と音響センシングによる対話のプロトタイピング、FabAuthは内部構造の共鳴特性による個体同定を扱う。笛としての発音(エッジトーン)は使わず、情報量は個体同定にとどまる。
  脅威理由: 印刷物の内部形状に情報を持たせて音で読むという枠組みが共通し、国内外の査読者が指摘しうる近接研究である。少なくともFabAuthは引用しておくべきである。

### 調べ残した穴
Printone本体のACM Transactions on Graphics版のPDFに到達できず、シミュレーション誤差の定量値をセント換算で取れていない。確認できたのはISMA 2017短縮版の「56個中53個が実測範囲に入った」という記述までである。ACM Symposium on Computational Fabricationの全年次の目次、ISMA、Forum Acusticum、Stockholm Musical Acoustics Conference、日本音響学会音楽音響研究会の各年次プログラムを個別に当たり切れていない。特許を全く調べておらず、検索結果には米国特許のMultiple tone whistleやFipple flutes having improved airwaysが現れているため、複数音の笛や音で情報を読む玩具の特許にCipherFluteに近い構成が存在する可能性が残る。中国語圏と韓国語圏の文献、およびThingiverseやPrintablesなど非査読の設計物も網羅していない。Jazz Research Journalの「Walrus Pipes and Waving Panpipes」は掲載誌が有料の壁を返して書誌を確定できず、複数の共鳴管を1つの物体にまとめる先行例として重要になりうるため追加調査を勧める。Yuan LanのUBC博士論文(尺八型縦笛の伝達行列法設計)とISMA 2019のオカリナ数値解析も原典に到達できていない。

==========================================================================================
## [04-acoustic-sensing] 音響センシングと静電容量センシングによる物体・状態の認識  (確認44 / 未検証8 / 訂正66 / 削除0)

### 要約
この切り口では、音響で物体を認識する研究が3つの系統に分かれることが分かった。第一に物体側にスピーカとマイクを貼って伝達特性の変化を読むアクティブ音響センシング、第二に物体の形そのものが受動的に固有の音を作る受動音響タグ、第三に環境音を機械学習で分類する系統である。CipherFluteに直接関わるのは第二の系統である。決定的な発見は2件あった。1件目はすでに引用済みのBlowholeで、3Dプリント物体の共鳴空洞に息を吹き込んで穴を識別する研究であり、CipherFluteの物理的着想そのものである。2件目はSoundOff（IMWUT 2025）で、電子部品を持たない受動超音波タグの幾何形状から固有振動数を物理モデルで設計し、区別しやすい数千の設計を系統的に生成している。これは「形が符号語彙を固定する」というCipherFluteの主張に最も近く、未引用なので必ず追加すべきである。ほかにFabAuth、Acoustic Voxels、Acoustic Barcodes、Lamello、Printone、ProtoHole、UTAP、SqueezaPulse、AirLogicが中程度の脅威として挙がった。日本国内ではTouch & Activateを起点に大阪大学、立命館大学、筑波大学が厚い蓄積を持ち、特に川崎らの温度ロバスト性の研究が基準笛の位置づけに直結する。静電容量側ではItsy-BitsやDuoTouchが無電源の形状によるID保持を確立している。一方で、受動音響物体に多ビットの秘密を格納し、誤り訂正と基準体による正規化を伴って読み出す研究は英語でも日本語でも見つからなかった。

### 脅威の大きい文献
- 【高】SoundOff: Low-cost Passive Ultrasound Tags for Non-invasive and Non-Intrusive Smart Home Sensing
  著者: Yibo Fu, Vivian Shen, Víctor Riera-Naranjo, Bolei Deng, Alex Adams, Josiah Hester
  掲載: Proceedings of the ACM on Interactive, Mobile, Wearable and Ubiquitous Technologies (IMWUT), 第9巻第4号, pp.1-32, 2025年（DOI 10.1145/3770666）
  URL: https://par.nsf.gov/biblio/10670927-soundoff-low-cost-passive-ultrasound-tags-non-invasive-non-intrusive-smart-home-sensing
  関係: 電池も回路も持たない受動超音波タグであり、幾何形状と材料だけで固有振動数が決まるという原理を物理モデルで定式化している。区別しやすい固有の超音波放射を持つ設計を数千通り系統的に生成する手法を示しており、CipherFluteが管長と基本周波数の関係から13個のスロットを切り出した設計行為と正面から重なる。ただしタグ1個は1つの識別子を担うだけで、多ビットの秘密を運ぶ発想も誤り訂正も基準体による正規化も存在しない。
  脅威理由: 「無電源の物体の形状に符号語彙を作り込み、音で読む」という設計方法論がすでに体系化されており、しかも現行の論文が引用していない直近の主要ジャーナル論文である。見落とすと最新の先行を押さえていないという致命的な指摘を受ける。
- 【高】Blowhole: Blowing-Activated Tags for Interactive 3D-Printed Models
  著者: Carlos E. Tejada, Osamu Fujimoto, Zhiyuan Li, Daniel Ashbrook
  掲載: Proceedings of Graphics Interface 2018, pp.131-137, 2018年（DOI 10.20380/GI2018.18）
  URL: https://dblp.org/search?q=Blowhole+blowing-activated+tags
  関係: 3Dプリント物体の内部に共鳴空洞を作り、表面の目立たない開口に息を吹き込むと固有の音が鳴って穴を識別できる手法である。CipherFluteの物理的な着想そのものであり、無電源であることも、マイクで読むことも一致する。異なるのはヘルムホルツ共鳴の空洞であって管長で音高を決めるフィップル笛ではない点と、目的が位置の識別であって多ビットの秘密の保持ではない点である。
  脅威理由: 「吹いて読む3Dプリント無電源タグ」という枠自体がすでに2018年に提示されているため、物理層の新規性は主張できない。新規性を符号語彙の設計、基準笛による正規化、誤り訂正、秘密分散との組合せという情報設計の側に明確に置き直す必要がある。
- 【中】FabAuth: Printed Objects Identification Using Resonant Properties of Their Inner Structures
  著者: Yuki Kubo, Kana Eguchi, Ryosuke Aoki, Shigekuni Kondo, Shozo Azuma, Takuya Indo
  掲載: Extended Abstracts of the 2019 CHI Conference on Human Factors in Computing Systems (CHI EA 2019), 2019年（DOI 10.1145/3290607.3313005）
  URL: https://dblp.org/search?q=FabAuth
  関係: 3Dプリント物体の内部構造を変えることで、外観が同じ物体どうしに異なる共鳴特性を与えて個体を識別する手法である。外から見えない内部形状に情報を固定し、音響的な共鳴として読み出すという着想がCipherFluteの日用品への偽装と重なる。ただし加振装置が必要で系全体としては電源が要り、識別できるのは学習済みの少数のクラスにとどまる。
  脅威理由: 「同じ外観の物体の内部形状に情報を隠し共鳴で読む」という中核の着想が共有されているため、引用して差分を述べる必要が高い。情報量が識別クラス数にとどまり無電源の吹鳴でもないため、主要な主張が崩れるところまでは行かない。
- 【中】Acoustic Voxels: Computational Optimization of Modular Acoustic Filters
  著者: Dingzeyu Li, David I. W. Levin, Wojciech Matusik, Changxi Zheng
  掲載: ACM Transactions on Graphics (SIGGRAPH 2016), 第35巻第4号, 2016年（DOI 10.1145/2897824.2925960）
  URL: https://cdfg.mit.edu/publications/acoustic-voxels-computational-optimization-modular-acoustic-filters
  関係: 中空の小室を組み合わせて音響特性を最適化し、応用のひとつとして日用品に知覚されない音響情報を埋め込むことを挙げている。外観が同一でも内部の小室の並びが違えば固有の音が出るという点で、形が情報を固定して保持するという発想を共有する。すでに論文で引用済みであるが、埋め込める情報量は小さく符号設計や誤り訂正の議論はない。
  脅威理由: 音響による物体への情報埋め込みという枠組みの先駆であり必ず引用して差分を述べる必要がある。ただし秘密の保管という目的も多ビットの符号設計も持っていない。
- 【中】Acoustic Barcodes: Passive, Durable and Inexpensive Notched Identification Tags
  著者: Chris Harrison, Robert Xiao, Scott E. Hudson
  掲載: Proceedings of the 25th Annual ACM Symposium on User Interface Software and Technology (UIST 2012), pp.563-568, 2012年（DOI 10.1145/2380116.2380187）
  URL: https://dblp.org/search?q=Acoustic+Barcodes+notched+identification
  関係: 表面の切り欠きの並びをこすって鳴る音を二進の識別子に復号する受動タグであり、無電源の物体の形に符号を固定して音で読むというCipherFluteの直接の祖先にあたる。すでに引用済みである。CipherFluteとの違いは、こする動作の過渡音の時間間隔で符号化する点と、CipherFluteが定常的な発音の音高で符号化する点にある。
  脅威理由: 「形に二進符号を固定し音で読む受動タグ」という概念そのものはここで確立している。音高を語彙とすること、基準体で正規化すること、誤り訂正を伴うことを差分として述べる必要がある。
- 【中】Lamello: Passive Acoustic Sensing for Tangible Input Components
  著者: Valkyrie Savage, Andrew Head, Björn Hartmann, Dan B. Goldman, Gautham Mysore, Wilmot Li
  掲載: Proceedings of the 33rd Annual ACM Conference on Human Factors in Computing Systems (CHI 2015), 2015年（DOI 10.1145/2702123.2702207）
  URL: https://escholarship.org/uc/item/79j098j8
  関係: 長さの異なる櫛歯を弾いて音高の違いで操作を判別する受動部品である。櫛歯の長さが音高を決めるという設計はCipherFluteの管長が音高を決める設計とほぼ同型であり、長さを離散化して語彙を作るという発想も共通する。部品は無電源だが、目的は操作イベントの検出であって情報の保管ではなく、同時に区別する歯の数は数個から十数個にとどまる。
  脅威理由: 「長さで音高を作り分けて離散的な符号にする」という核心の物理設計が共有されているため必ず引用して差分を述べる必要がある。すでに論文で引用済みである。
- 【中】アクティブ音響センシングにおける環境温度変化にロバストな物体情報識別手法の検討
  著者: 川崎祐太, 伊藤雄一, 藤田和之, 尾上孝雄
  掲載: 情報処理学会論文誌, 第62巻第10号, pp.1658-1668, 2021年10月
  URL: https://cir.nii.ac.jp/crid/1390290701132201344
  関係: 面に置かれた物体を音響で認識する系において、環境温度の変化が音響特性を変えて認識精度を落とすという問題を正面から扱っている。CipherFluteが基準笛を混ぜて比で読むと述べている部分に対応する問題設定が、日本語の論文誌ですでに明示的に扱われていることを示す。ただし解法は特徴量と学習の側にあり、既知音高の基準体を同じ物体に同居させる構造的な解ではない。
  脅威理由: 温度変動で音響の読みがずれるという問題自体は既知であると示されるため、基準笛の新規性を問題の発見ではなく解法の構造に置き直す必要がある。日本語の論文誌に載っており投稿先の読者が知っている可能性が高い。
- 【中】ProtoHole: Prototyping Interactive 3D Printed Objects Using Holes and Acoustic Sensing
  著者: Shohei Katakura, Keita Watanabe
  掲載: Extended Abstracts of the 2018 CHI Conference on Human Factors in Computing Systems (CHI EA 2018), 2018年（DOI 10.1145/3170427.3188471）
  URL: https://dblp.org/search?q=ProtoHole
  関係: 3Dプリント物体の内部空洞と表面の複数の穴を組み合わせ、掃引信号を流して穴を塞いだときの共鳴変化を分類する手法である。穴と空洞という構成がCipherFluteと重なり、しかもBlowholeとほぼ同時期の日本の研究である。ただし物体内部にスピーカとマイクを入れる必要があり無電源では成立せず、情報量は穴の個数分の状態にとどまる。
  脅威理由: 穴と共鳴空洞で3Dプリント物体を対話的にするという近接した着想であり、日本のHCI分野の研究であるため投稿先の読者から必ず指摘される。無電源であることと吹鳴で読むことの違いを述べて引用すべきである。

### 調べ残した穴
最大の穴は、ACM Digital Libraryの本文ページがこの環境から403で取得できず、Blowhole、SoundOff、FabAuth、Acoustic Barcodesの実効ビット数やスロット数や誤り率といった、CipherFluteと直接比較したい数値を原文で確認できていない点である。特にSoundOffの「数千の設計」が1個のタグあたり何ビットに相当するのかは差分を述べるうえで重要である。次に、Semantic Scholarの応答制限によりAcoustic Voxels、Printone、SoundOffの被引用をたどり切れておらず、とりわけ2025年末出版のSoundOffの後続を確認できていない。電子情報通信学会の技術研究報告はJ-GLOBAL経由で1件しか押さえられておらず、応用音響研究会やヒューマンコミュニケーション基礎研究会を横断していない。情報処理学会電子図書館はWebFetchで検索結果の本体が取れず、HCI研究会とUBI研究会の個別発表を網羅できていない。受動超音波タグや表面弾性波タグについてIEEE Sensors JournalやSensors誌などセンサ工学分野の文献をほとんど見ていない。楽器音響学におけるフィップル笛の管長と基音の関係、端部補正の一次文献も押さえていない。水中音響の受動音響バーコード（Rayleigh波共鳴）は書誌が確定できないまま残った。

==========================================================================================
## [05-jp-fabrication-hci] 日本のHCI分野におけるデジタルファブリケーション研究  (確認46 / 未検証6 / 訂正12 / 削除1)

### 要約
日本のHCI分野のデジタルファブリケーション研究は三つの系統に分かれる。第一は熱溶解積層方式3Dプリンタの造形挙動そのものを制御して新しい表現や機能を得る系統で、高橋治輝（立命館大学）を中心に毛構造、布状構造、ブリッジ造形、複数材料フィラメントの成果が積み上がっている。第二は印刷物や日用品に電気的な機能を付与する系統で、加藤邦拓、川原圭博、鳴海紘也、池松香、石井綾郁らが導電インク、食用金箔、レーザ炭化による木製回路、自己折り紙を扱っている。第三が造形物そのものを情報の担体として使う系統であり、CipherFluteにとって決定的に重要である。国内にはNTTの久保勇貴らによるFabAuthの一連の研究（内部充填パターンを能動音響センシングと機械学習で識別）と、神奈川工科大学の鳥井秀幸と上平員丈らによる一連の研究（造形物内部に情報を埋め込み近赤外線で読み出す）という二つの独立した研究群が存在する。前者は「造形物に情報を埋め込み音で読む」という一文でCipherFluteと重なり、引用集合まで重なるため最も注意深く差分を述べる必要がある。一方で、管長と基本周波数の関係を設計変数として扱い、人が吹くだけで電源も計測器も機械学習も用いずに多数ビットの符号を読み出す研究は国内に存在しなかった。誤り訂正符号や基準笛による正規化を物理造形の符号設計へ持ち込んだ国内先行研究、および暗号資産のリカバリーシードを物理媒体へ保管することを扱った国内HCI研究も見つからなかった。

### 脅威の大きい文献
- 【高】内部構造パターンの差異を利用した3Dプリントオブジェクト識別手法（およびFabAuth: Printed Objects Identification Using Resonant Properties of Their Inner Structures、3D-Printed Object Identification Method using Inner Structure Patterns Configured by Slicer Software）
  著者: 久保勇貴、江口佳那、青木良輔、近藤重邦、東正造、犬童拓也（日本電信電話株式会社）
  掲載: WISS 2019 登壇発表。英語版はExtended Abstracts of CHI 2019（DOI: 10.1145/3290607.3313005）およびExtended Abstracts of CHI 2020, pp.1-7（DOI: 10.1145/3334480.3382847）
  URL: https://www.wiss.org/WISS2019Proceedings/oral/8.pdf
  関係: スライサで設定する充填率と充填パターンの違いによって、外観が同一の3Dプリント造形物に固有の音響周波数応答を割り当て、圧電素子による20キロヘルツから40キロヘルツの掃引信号と機械学習で8個の物体を平均99.3パーセントの精度で識別する。CipherFluteと「家庭用3Dプリンタで造形した物体に情報を仕込み、音響を通じて読み出す」という一文が重なり、引用しているAcoustic Barcodes、Acoustic Voxels、AirCode、InfraStructsという先行研究の集合まで重なっている。
  脅威理由: 一文要約と引用集合の両方が重なるため、引用しないと国内査読で「既に日本でやられている」と判断される危険が大きい。ただし得られるのは8クラス（3ビット相当）の識別であってデータ搬送ではなく、圧電素子と事前学習を必須とし、秘密の保管という応用文脈を持たない点が決定的な差分である。
- 【中】ProtoHole: 穴と音響センシングを用いたインタラクティブな3Dプリントオブジェクトの提案（ProtoHole: Prototyping Interactive 3D Printed Objects Using Holes and Acoustic Sensing）
  著者: 片倉翔平、渡邊恵太（明治大学）
  掲載: WISS 2017。英語版はExtended Abstracts of the 2018 CHI Conference on Human Factors in Computing Systems（DOI: 10.1145/3170427.3188471）
  URL: https://api.semanticscholar.org/graph/v1/paper/DOI:10.1145/3170427.3188471
  関係: 3Dプリント物体の内部に空洞を設け表面に穴を開け、高周波の掃引信号を放射して穴の開閉による共鳴特性の変化を機械学習で分類する。空洞と穴という幾何が音を規定する物理は、CipherFluteの管長と窓の関係とよく似ている。ただし目的は動的な入力の検出であり、静的なデータの符号化ではない。
  脅威理由: 主要な主張を直接崩すものではないが、「3Dプリント造形物の空洞の音響を利用する」という点で明確に隣接し、同じ日本のコミュニティ（WISSと明治大学）の成果であるため、引用して差分を述べないと不誠実に見える。
- 【中】3Dプリンター造形物への情報埋め込み技術の一連の研究（石膏材、内壁の構造化、近赤外線透視像、近赤外線反射像、2色造形、高反射率材料、近赤外蛍光樹脂、メタルライク樹脂）
  著者: 中村耕介、鈴木雅洋、松本知久、髙沢渓吾、高嶋洋一、鳥井秀幸、上平員丈（神奈川工科大学ほか）
  掲載: 電子情報通信学会技術研究報告 116(34) pp.93-97 (2016)、116(132) pp.19-22 (2016)、116(176) pp.57-61 (2016)、116(501) pp.13-17 (2017)、117(113) pp.29-33 (2017)、117(282) pp.13-16 (2017)、117(476) pp.41-44 (2018)、および画像電子学会研究会講演予稿 16.03 pp.141-145 (2017)。関連する科学研究費助成事業の課題は「3Dプリンタ造形物への情報埋め込み技術の研究」2019年4月から2023年3月まで
  URL: https://cir.nii.ac.jp/all?q=3D%E3%83%97%E3%83%AA%E3%83%B3%E3%82%BF%E9%80%A0%E5%BD%A2%E7%89%A9%20%E6%83%85%E5%A0%B1%E5%9F%8B%E3%82%81%E8%BE%BC%E3%81%BF
  関係: 造形物の内部に材料の光学的性質の違いや内壁の構造化によって情報を埋め込み、近赤外線の撮像や透視で外観を損なわずに読み出す。「造形物の内部に情報を埋め込み、外観を損なわずに読み出す」という問題設定はCipherFluteとまったく同じであり、AirCodeやInfraStructsに相当する国内の系譜を成している。
  脅威理由: 読み出しの物理が光学であって音響ではないため主要な主張は崩さないが、国内における造形物への情報埋め込みの最も体系的な先行研究群であり、引用漏れは「国内先行を調べていない」という指摘を招く。
- 【中】溝間隔の違いによる筆圧変化を活用したシート埋め込み型ID認識手法
  著者: 瀬崎夕陽、関口祐豊、中村聡史（明治大学）
  掲載: WISS 2025 登壇発表
  URL: https://www.wiss.org/WISS2025Proceedings/data/paper/23.pdf
  関係: 一定間隔で溝を設けた透明なシートをディスプレイ上に置き、デジタルペンの筆圧のピークから溝間隔を推定してシートを識別する。物体側に電子部品を一切持たせず物理的な幾何そのものが識別子を符号化するという構図がCipherFluteと同型で、Acoustic Barcodesを明示的に参照している。符号の語彙は4種類、識別精度は0.78にとどまる。
  脅威理由: 直近のWISSで「電子部品なしの物理構造でIDを符号化する」という同じ発想が発表されているため査読者が想起しやすく、符号量と読み出し手段の違いを述べる必要がある。ただし読み手がデジタルペンとディスプレイという電子機器であり、誤り訂正の設計もない。
- 【中】棒の引っかきによる音波を用いたインタラクション取得手法の検討
  著者: 林吉経、尾崎亮太、上堀まい、岩本諒、菊地萌花、石黒成紀、伊藤雄一（青山学院大学、日本学術振興会特別研究員、DAIKEN株式会社）
  掲載: WISS 2025 デモ発表 1-C30
  URL: https://www.wiss.org/WISS2025Proceedings/data/demo/1-C30.pdf
  関係: 3Dプリンタで作成した突起列を、オルゴールの櫛歯を加工した長さの異なる2本の爪が引っかくことで異なる周波数の音波を発生させ、その発生順番から移動方向を、回数から移動量を推定する。物理構造の寸法を音の周波数に写像するという中核の物理がCipherFluteと共通する。
  脅威理由: Lamelloの日本における延長として同じ物理を使っており直近のWISS発表であるため引用が望ましいが、目的が運動計測であってデータ搬送の符号語彙を設計しているわけではないため主要な主張は崩さない。
- 【中】アクティブ音響センシングによる日常物体識別と位置推定
  著者: 岩瀬大輝、伊藤雄一、秦秀彦、山下真由、尾上孝雄（大阪大学大学院情報科学研究科）
  掲載: 情報処理学会 インタラクション2018 論文集, pp.62-71, 2018年
  URL: http://www.interaction-ipsj.org/proceedings/2018/data/pdf/INT18008.pdf
  関係: アクリル平板にマイクとスピーカを配して音響信号を伝搬させ、板上に置かれた物体の種類を98.2パーセント、位置を85.5パーセントの精度で推定する。日常空間の物体を音響で識別するという構図が、CipherFluteの「日用品に偽装した物体を音で読む」という枠組みと隣接する。
  脅威理由: 日本のHCI分野における音響センシングによる物体識別の代表例でありCipherFluteの位置づけの説明に必要だが、物体側に情報を埋め込む設計を持たず、能動計測と機械学習を必要とするため主張を直接には脅かさない。
- 【中】Touch & Activate: Adding Interactivity to Existing Objects using Active Acoustic Sensing
  著者: Makoto Ono（大野誠）, Buntarou Shizuki（志築文太郎）, Jiro Tanaka（田中二郎）（筑波大学）
  掲載: Proceedings of the 26th Annual ACM Symposium on User Interface Software and Technology (UIST 2013), pp.31-40, DOI: 10.1145/2501988.2501989
  URL: https://www.iplab.cs.tsukuba.ac.jp/en/paper/6151b7ff551fd46e82abdb1b/
  関係: 振動スピーカと圧電マイクを一組だけ既存の物体に貼り付け、掃引信号を注入して周波数応答の変化を学習することで触り方や握り方を認識する。久保らの研究、片倉らの研究、岩瀬らの研究、林らの研究がいずれも引用している日本発の能動音響センシングの原典であり、CipherFluteの系譜上の基準点になる。
  脅威理由: 直接の競合ではないが、国内の音響センシング研究すべての基点であり、これを引かないと「音響で物体の内部状態を読む」系譜のなかでCipherFluteがどこに立つのかを日本の読者へ説明できない。
- 【中】木、紙、金属、磁器 – 予め吹き込まれた音響のないレコード
  著者: 城一裕（九州大学大学院芸術工学研究院 准教授）
  掲載: 展覧会、2023年2月、福岡市のギャラリーEUREKA。2021年に文化庁メディア芸術祭エンターテインメント部門推薦作品
  URL: https://www.design.kyushu-u.ac.jp/topics/16705/
  関係: バウハウスのモホイ＝ナジの構想を現代のパーソナルファブリケーションで実現する試みで、楽譜から周波数を計算し対応する波形を木、紙、金属、磁器の表面に音溝として直接刻む。録音を経ずに計算した数値を造形の幾何へ彫り込み、そこから音として読み出すという構図がCipherFluteと概念的に近い。
  脅威理由: 査読付き論文としての先行研究ではないため主要な主張は崩さないが、「物理造形に音を刻む」という発想の国内における最も近い実践であり、知らずに提案すると発想の独自性を過大に主張しているように見える恐れがある。

### 調べ残した穴
情報処理学会のインタラクションシンポジウムは2018年、2024年、2025年しか通せておらず、2014年から2023年までのデモ発表とインタラクティブ発表にファブリケーションと音響の関連発表が埋もれている可能性が残る。情報処理学会ヒューマンコンピュータインタラクション研究会の研究報告にはまったく手をつけられなかった。情報処理学会電子図書館の検索インタフェースがJavaScriptで動作しWebFetchから直接検索できなかったため、CiNii Researchを経由した代替検索にとどまり、研究報告レベルの初期段階の研究を網羅できていない。エンタテインメントコンピューティングシンポジウムと日本バーチャルリアリティ学会論文誌（塚田浩二がゲストエディタを務めた「デジタルファブリケーションとVR」特集号を含む）の目次も確認できていない。日本画像学会の4D and Functional Fabrication研究会の電子論文誌J4DFFは第1号から第4号の存在を確認しただけで各号の目次を取得できず、画像工学と材料工学の側からの先行研究を見落としている可能性がある。有力文献の被引用の追跡も部分的で、Semantic Scholarの検索APIが断続的に応答しなかったため、FabAuthやAcoustic BarcodesやLamelloを引用する国内後続研究の網羅ができていない。加えて、城一裕や松浦知也を中心とするメディアアートとサウンドアートの領域は査読付き論文の形をとらない実践が多く、学術データベースからは見つけにくいため、展覧会カタログや作家のウェブサイトを直接当たる作業が残っている。WISS 2014のCapacitiveMarkerとWISS 2017のM系列円筒バーコードは、物理的な符号設計という観点でCipherFluteに近い可能性があるが本文を読めていない。

==========================================================================================
## [06-entertainment-computing] エンタテインメントコンピューティングにおける音・楽器・遊びと認証  (確認37 / 未検証5 / 訂正30 / 削除0)

### 要約
エンタテインメントコンピューティングの主要会議を題目レベルで網羅走査した結果、音や演奏を「鍵」として扱う遊戯的体験の研究はこの分野にほとんど存在しないことが分かった。ICECの2003年から2025年までの全24巻には音楽・音響論文が多数あるが、音を秘密や識別子の担体とするものは皆無で、認証を扱ったのは掌紋バイオメトリクス1件だけである。ACE（2004年から2017年）、CHI PLAY（2014年から2025年、Companionを含む）、NIMEの全巻でも同様であった。いっぽうTEIには発想を共有する研究が集中しており、3Dプリント造形物を対称暗号の鍵として物質化したThe Bronze Key（2018年）、ノックのリズムを鍵とするKnock Knock to Unlock（2017年）、日用品を動かす所作に認証を埋め込むAct2Auth（2024年）、3Dプリント格子の音響伝搬特性を状態符号に使うUTAP（2017年）が見つかった。認証の側ではTapSongs（UIST 2009）とMusipass（NSPW 2009）がリズムや旋律を合言葉にしている。日本語圏では水木敬明らのカードベース暗号が「身近な道具を用いる電源不要の暗号技術」として大きな系譜を作り、2026年に情報処理学会誌の特集にまでなっている。物体を鍵とする遊戯研究、旋律を合言葉にする認証研究、電源不要の物理暗号の三つの系譜はそれぞれ独立に存在するが、受動的に発音する造形物の音高に多ビットの秘密を格納し吹いて読み出す構成は見つからなかった。CipherFluteはこれら三系譜の交点にある空白を埋めるものだと主張してよい。

### 脅威の大きい文献
- 【中】The Bronze Key: Performing Data Encryption
  著者: Susan Kozel, Ruth Gibson, Bruno Martelli
  掲載: TEI 2018 (Proceedings of the Twelfth International Conference on Tangible, Embedded, and Embodied Interaction), pp.549-554
  URL: https://doi.org/10.1145/3173225.3173306
  関係: モーションキャプチャした身振りから作った3Dプリント造形物そのものを対称暗号の「鍵」として提示し、平文をカセットテープの音声、暗号文を書籍として物質化したアート作品である。3Dプリント物体を暗号鍵と呼ぶ点と、平文を音のメディアに載せる点がCipherFluteと直接に重なる。ただし読み出し手順もビット数も誤り訂正も脅威モデルも定義されておらず、工学的な符号設計ではなく芸術的な比喩にとどまる。
  脅威理由: 「3Dプリント造形物を暗号鍵とする」という一文だけを取り出すとCipherFluteの新規性と衝突して見えるため、必ず引用して、読み出し可能な符号としての設計の有無という差分を明示する必要がある。
- 【中】カードベース暗号の系譜（More Efficient Match-Making and Satisfiability: The Five Card Trick / Six-Card Secure AND and Four-Card Secure XOR / 情報処理学会誌2026年特集「カードベース暗号とその展開」）
  著者: Bert den Boer / 水木敬明, 曽根秀昭 / 駒野雄一, 水木敬明, 真鍋義文, 縫田光司ほか
  掲載: EUROCRYPT '89 (LNCS, 1990) / Frontiers in Algorithmics (LNCS, 2009) / 情報処理 2026年5月号・6月号
  URL: https://doi.org/10.1007/3-540-46885-4_23
  関係: トランプのような身近な道具だけで秘密計算を行う分野であり、日本で継続的に発展してCiNiiに95件が該当し、2026年には情報処理学会誌が「情報セキュリティ教育にも応用可能な身近な道具を利用した暗号技術」という副題で前後編の特集を組んでいる。電源も電子部品も持たない物理的な暗号という枠組みと、レクリエーションや教育への応用という遊戯性の両方でCipherFluteと重なる。ただし扱うのは複数人の秘密計算プロトコルであり、物体に秘密を保管して後から読み出す用途ではない。
  脅威理由: WISSの読者層は日本の情報処理学会関係者であり、「身近な道具を使った電源不要の暗号技術」といえばカードベース暗号を連想するため、引用せずに新規性を主張すると位置づけが甘いと見なされる危険が高い。
- 【中】TapSongs: Tapping Rhythm-Based Passwords on a Single Binary Sensor
  著者: Jacob O. Wobbrock
  掲載: UIST 2009 (Proceedings of the 22nd Annual ACM Symposium on User Interface Software and Technology), pp.93-96
  URL: https://doi.org/10.1145/1622176.1622194
  関係: ボタンのような二値センサ一つで、自作のジングルのタイミングモデルに照合して本人を認証する手法である。音楽の断片を秘密として使うという発想がCipherFluteと共通し、Beat-PINやSmartEarへ続く系譜の起点になっている。CipherFluteが音高の系列を語彙とするのに対し、TapSongsは時間間隔の系列を語彙とする。
  脅威理由: 「音楽を鍵にする」という着想の代表的先行例であり必ず引用すべきだが、電子センサと計算機による照合を前提としており、電源を持たない物体が音高で情報を保持するCipherFluteとは担い手が根本的に異なる。
- 【中】Knock Knock to Unlock: A Human-centered Novel Authentication Method for Secure System Fluidity
  著者: Marisa Lu, Gautam Bose, Austin S. Lee, Peter Scupelli
  掲載: TEI 2017 (Proceedings of the Eleventh International Conference on Tangible, Embedded, and Embodied Interaction), pp.729-732
  URL: https://doi.org/10.1145/3024969.3035530
  関係: ドアを叩くリズムの型を本人性の鍵として扱い、IoTとフィジカルコンピューティングで技術の存在を感じさせないようにした提案である。日常の物理的行為（叩く、吹く）をそのまま鍵の入力にする点と、建具や日用品に認証を溶け込ませる設計思想がCipherFluteと重なる。ただし鍵は利用者の身体が生成するもので、物体側には情報が刻まれていない。
  脅威理由: CipherFluteが投稿しても不思議のないTEIという場で「物理的な行為を鍵にする」提案が出ている以上、引用して、鍵が人にあるのか物にあるのかという差分を述べる必要がある。
- 【中】Act2Auth: A Novel Authentication Concept based on Embedded Tangible Interaction at Desks
  著者: Sarah Delgado Rodriguez, Sarah Prange, Lukas Mecke, Florian Alt
  掲載: TEI 2024 (Proceedings of the Eighteenth International Conference on Tangible, Embedded, and Embodied Interaction), 論文番号12, pp.1-15
  URL: https://doi.org/10.1145/3623509.3633360
  関係: 机の上でカップを置く、キーボードを置き直すといった日常の所作の秘密の系列で認証する概念であり、107枚の机の写真の物体分析、65名の調査、静電容量式検知の技術検討、8名での評価から構成される。日用品に認証を偽装して埋め込み、日常の所作のまま読み出すという設計目標がCipherFluteの物理層の役割と近い。ただし秘密は所作の順序にあり、物体そのものには格納されない。
  脅威理由: 「日用品に埋め込む認証」という主張の直接の先行例であり、引用して、電源の有無と秘密の所在という差分を述べないと新規性の輪郭がぼやける。
- 【中】UTAP: Unique Topographies for Acoustic Propagation - Designing Algorithmic Waveguides for Sensing in Interactive Malleable Interfaces
  著者: Jan Rod, David Collins, Daniel Wessolek, Thavishi Ilandara, Ye Ai, Hyowon Lee, Suranga Nanayakkara
  掲載: TEI 2017 (Proceedings of the Eleventh International Conference on Tangible, Embedded, and Embodied Interaction), pp.141-152
  URL: https://doi.org/10.1145/3024969.3024987
  関係: アルゴリズムで生成したトポロジー的に相異なる3Dプリント格子を圧電素子に取り付け、変調音響信号の変化から変形状態を分類する手法である。3Dプリントした受動構造の音響特性の違いを区別可能な符号として使う点で、既に論文が引用しているAcoustic Voxelsと同じ系譜にあり、その実例がTEIにも存在することを示す。ただし能動的な音源を必要とし、目的は変形検知であって情報の格納ではない。
  脅威理由: 3Dプリント構造の音響的個体差を符号に使う先行例であり、Acoustic Voxelsと並べて引用しておかないと「造形の音響特性で情報を区別する」着想の既出性を見落としたと見なされうる。
- 【中】Musipass: Authenticating Me Softly with "My" Song
  著者: Marcia Gibson, Karen Renaud, Marc Conrad, Carsten Maple
  掲載: NSPW 2009 (Proceedings of the 2009 Workshop on New Security Paradigms Workshop)
  URL: https://doi.org/10.1145/1719030.1719043
  関係: 英数字の代わりに旋律で構成されるパスワード方式であり、人間が音楽に対して優れた記憶を持つことを前提に、記憶しやすさと受容の面で良好な評価を報告している。旋律そのものを秘密として扱う点でCipherFluteの符号（聞けば旋律として知覚される音高系列）と直接に重なる。ただし画面上で楽曲を選択・再生する電子的な仕組みであり、物体は関与しない。
  脅威理由: 音楽を鍵にする発想は既にあると指摘されうるため、引用したうえで、新規性が「旋律を鍵にすること」ではなく「電源を持たない造形物が旋律を保持し吹くことで読み出せること」にあると言い直す必要がある。
- 【中】情報タイムカプセルにおける地図情報を用いた認証システムの実装
  著者: 北山海, 西岡大, 村山優子（岩手県立大学）
  掲載: 情報処理学会研究報告 EC（エンタテインメントコンピューティング）2014巻62号, pp.1-6, 2014年3月6日（GN研究会・HCI研究会と共同開催）
  URL: https://cir.nii.ac.jp/crid/1573950402603038976
  関係: 災害時の世代間の情報伝達を補うために記憶情報を未来へ伝える情報タイムカプセルを提案し、十数年後には識別子とパスワードを忘れるという問題に対して記憶に残りやすい地図情報による認証を実装した報告である。秘密を長期に保管して後から本人が読み出すという時間軸の問題設定が、CipherFluteのリカバリーシード長期保管の用途と重なる。EC研究会というCipherFluteの隣接コミュニティでの発表である点も重要である。
  脅威理由: 日本のエンタテインメントコンピューティング分野で「秘密の長期保管と認証」を扱った数少ない先行例であり、引用して、記憶に頼るのか物体に頼るのかという差分を述べないと国内先行研究の見落としと見なされうる。

### 調べ残した穴
情報処理学会電子図書館はJavaScript依存で機械的な全題目走査ができず、OAI-PMHも集合が1万件以上あってEC研究会の集合を特定できなかったため、EC研究会の研究報告とエンタテインメントコンピューティングシンポジウム論文集はCiNii Researchのキーワード検索に頼っており全数走査をしていない。dblpのACE系列は2017年までしか収録がなく2018年以降のACEを見ていない。ICEC 2002（IWEC）の巻とICEC 2025本体の一部も取得できていない。WISS各年の予稿集、日本デジタルゲーム学会年次大会、日本バーチャルリアリティ学会大会、インタラクションの全題目走査も未実施である。Ars ElectronicaやSIGGRAPH Art Galleryなど芸術系の文脈に音を鍵とする作品がある可能性を追い切れていない。キャプテン・クランチの笛（2600ヘルツ）については、Esquire誌1971年10月号のRon Rosenbaumの記事本体に到達できず二次資料までしか確認していない。d0x3d!（USENIX 3GSE 2013）もUSENIXサイト上で該当ページを取得できず未検証である。有力文献の被引用をたどる作業も不十分で、とくにTapSongsとControl-Alt-Hackは被引用が多く、そこから遊戯性と認証を結ぶ研究が新たに出る可能性が残っている。なお成果物は指示されたパスの「undefined」が変数展開の失敗と判断したため、実際に用意されていたrelated_work_survey/raw/06-entertainment-computing.mdに書き、念のため同内容をundefined/raw/06-entertainment-computing.mdにも複製した。

==========================================================================================
## [07-secret-backup-physical] 秘密分散と秘密情報の物理的バックアップの実務と標準  (確認52 / 未検証9 / 訂正21 / 削除0)

### 要約
この分野は三層に分かれている。第一に秘密を人間可読な語へ写す符号化の標準があり、BIP-39、SLIP-39、Bytewords、RFC 1751、RFC 2289が属する。第二に断片へ割る方式があり、codex32、Seed XOR、Armoryの断片バックアップ、Cypherock X1、Ledger Recover、HashiCorp Vault、PCI PIN要件、ICANNの鍵儀式が実在する。第三に断片の物理的保管の指針があり、金属打刻、封緘袋、貸金庫、宅配経路の分離が標準になっている。最も危険な発見はcodex32（BIP-93）で、紙の回転円板と対照表だけでShamirの分割と復元とBCH誤り訂正を人手で行う。電源不要の物理担体に誤り訂正符号を載せる発想は既に標準提案として存在し、CipherFluteはこれを一般的新規性として主張できない。一方、担体そのものを日用品に偽装する設計は、標準にも論文にも製品にも見つからなかった。偽装はデータ層（囮ウォレット、Seed XOR、囮PIN）でのみ実装されており、物理層の実務指針はむしろ連番照合と改ざん痕点検という可視性を要件にしている。音で秘密を読み出す物理バックアップも皆無であった。

### 脅威の大きい文献
- 【高】codex32: Checksummed SSSS-aware BIP32 seeds（BIP-93）と付属の紙の計算器（ヴォルヴェル）
  著者: Leon Olsson Curr、Pearlwort Sneed（いずれも仮名）、Andrew Poelstra
  掲載: Bitcoin Improvement Proposal 93、Informational、Draft、2023年2月13日作成。数学的補遺は2023年8月23日版、解説記事はBlockstream Research、2023年9月7日
  URL: https://github.com/bitcoin/bips/blob/master/bip-0093.mediawiki
  関係: シードをbech32アルファベットで符号化しBCH誤り訂正符号を付け、Shamirの秘密分散の分割と復元を紙の回転円板と対照表だけで人手で行う方式である。電源も計算機も使わない物理担体に誤り訂正符号を載せるという構成がCipherFluteと完全に重なる。担体が印刷文字列である点と、日用品への偽装や音響読み出しがない点だけが差分である。
  脅威理由: 「電源不要の物理媒体に誤り訂正符号付きで秘密を格納する」という一般的な新規性主張は本提案に先取りされており、そのまま書くと大幅に弱まる。既知のビットコイン標準提案でもあり、査読者に指摘される可能性が高い。
- 【中】Seed XOR（各断片がそれ自体正当なBIP-39シードに見えるN-of-N分割）
  著者: Coinkite社（COLDCARDの開発元）
  掲載: 製品仕様および解説サイト（COLDCARDファームウェアに実装済み）
  URL: https://seedxor.com/
  関係: 1つのシードを排他的論理和で分け、各断片自体を正当なBIP-39シードにする。各断片に囮の資金を置けるため、断片を奪った者はそれを本物の財布だと信じる。CipherFluteが物体の層でやろうとしている偽装を、データの層で先に実現している。
  脅威理由: 「担体が明らかに秘密の保管物に見える」問題への対処が既に実務にあることを示すため、偽装という着眼自体を新規性として書けなくなる。ただし担体を日用品に変える点は差分として残る。
- 【中】SeedQR および CompactSeedQR（二次元コード化したシードの金属板への打刻）
  著者: SeedSignerプロジェクト
  掲載: SeedSignerリポジトリ内の仕様文書、継続更新
  URL: https://github.com/SeedSigner/seedsigner/blob/dev/docs/seed_qr/README.md
  関係: BIP-39の語を索引番号へ写して二次元コードに収め、手で書き写せる大きさに縮める仕様である。金属板に穴を打って転写した実例を載せている。二次元コードは規格上Reed–Solomon符号を内蔵するため、Reed–Solomonで守られた物理的シードバックアップが既に実在する。
  脅威理由: CipherFluteのReed–Solomon採用が物理バックアップとして新規ではないことを示す。ただし機械可読の模様であって日用品には見えず、読み出しにカメラが要る点は差分になる。
- 【中】Of Secrets and Seedphrases: Conceptual Misunderstandings and Security Challenges for Seed Phrase Management among Cryptocurrency Users
  著者: Farida Eleshin、Qi Sun、Mengzhe Ye、Sauvik Das、Jason I. Hong
  掲載: CHI Conference on Human Factors in Computing Systems（CHI '25）、2025年、横浜、19ページ
  URL: https://doi.org/10.1145/3706598.3713209
  関係: 20名の面接と643名の調査により、紙のバックアップが39パーセントで最多、分割保管の実践は面接20名中1名だけ、相続の備えは少数と報告している。本文に隠蔽やステガノグラフィの記述はない。CipherFluteの動機づけを実データで裏づけ、同時に偽装が実践されていない空白を示す。
  脅威理由: 新規性を直接脅かすものではないが、近接分野の最新の実証研究であり、引用しないと動機づけの根拠が弱く見える。査読者が知っている可能性が高い。
- 【中】Payment Card Industry (PCI) PIN Security Requirements, Version 2.0（鍵成分の物理配送の要件）
  著者: PCI Security Standards Council
  掲載: 2014年12月（初版2011年10月）
  URL: https://listings.pcisecuritystandards.org/documents/PCI_PIN_Security_Requirements_v2.pdf
  関係: 印刷した鍵成分を目隠し封筒に封入すること、Shamirのようなm-of-n方式で1人が閾値未満しか触れないこと、断片を別々の宅配経路で送ること、連番付きの改ざん検知封緘袋を使い受領時に別経路で連番を照合することを要求している。秘密を複数の物体に分けて保管・輸送する実務の最も成熟した標準である。
  脅威理由: 分散保管の実務指針としてこれを外すと調査の網羅性を欠く。設計思想が「隠す」ではなく「見えて検査できる」である点でCipherFluteと正反対であり、脅威モデルの対比材料として必須である。
- 【中】DNSSECルート鍵署名鍵の運用実務（DNSSEC Practice Statement for the Root Zone KSK Operator 第8版）
  著者: Root Zone KSK Operator（ICANN / Public Technical Identifiers）
  掲載: 2025年4月14日発効。鍵の儀式は2010年から2026年まで63回の記録が公開されている
  URL: https://www.iana.org/dnssec/procedures/ksk-operator/ksk-dps-20250414.html
  関係: 7名の暗号担当者のうち3名で鍵を起動し、災害復旧用の鍵は7名の復旧鍵保持者のうち5名を要する閾値方式で守る。改ざん検知袋、貸金庫、四層の物理区画、録画を用いる。秘密を物理的に分割して複数の人と場所に預ける運用の、世界で最も監査された実例である。
  脅威理由: 閾値方式による物理的鍵バックアップが現実に稼働していることを示す最良の事例であり、CipherFluteの脅威モデルの妥当性を支えると同時に、偽装という選択が実務の主流でないことを裏づける。
- 【中】Visual Cryptography（重ね合わせるだけで人間の視覚が復号する秘密分散）および視覚復号型秘密分散法を用いたパスワードの分散管理の提案
  著者: Moni Naor、Adi Shamir／大川直也、栃窪孝也
  掲載: Advances in Cryptology — EUROCRYPT '94、Lecture Notes in Computer Science、pp. 1–12、1994年／情報処理学会論文誌デジタルプラクティス、第7巻第2号、pp. 35–50、2026年
  URL: https://dblp.org/rec/conf/eurocrypt/NaorS94.html
  関係: 透明シートを重ねるだけで計算なしに秘密が現れる物理的な秘密分散である。大川と栃窪はこれをパスワードの分散管理に応用し、オーバーヘッドプロジェクタ用シートとスマートフォンで実用性を評価している。CipherFluteの「2枚そろって初めてハートが現れるカード」は事実上この系譜に属する。
  脅威理由: 「電源も計算機もなしに人間の感覚だけで秘密を復号する物理媒体」という枠組みが視覚の側で30年以上前に確立している。CipherFluteのカード実装はほぼ同じ発想であり、モダリティの違い以外の差分を明示する必要がある。
- 【中】Cypherock X1（Shamirの秘密分散を4枚のカードと本体に組み込んだ製品）
  著者: Cypherock社
  掲載: 市販製品。技術文書はdocs.cypherock.comで公開
  URL: https://www.cypherock.com/
  関係: 秘密鍵をShamirの秘密分散で分け、1台の本体と4枚の近距離無線通信カードに保持する。リカバリーフレーズの書き写しを不要にし、カードを別々の場所へ分散することを推奨する。CipherFluteが訴える「複数の物体に分けて持つ」という利用像を商用化している。
  脅威理由: 分散した物理担体で秘密を持つという利用像が既に製品として存在することを示す。ただし断片は電子的な安全素子内にあり専用機器が要るので、電源不要と日用品偽装という差分は明確に残る。

### 調べ残した穴
有償の国際規格の本文を読めていない。ISO/IEC 19592の秘密分散規格、ISO 11568の銀行鍵管理、ANSI X9.24の対称鍵管理は鍵成分を物理的に分けて運ぶ実務の源流であり、担体の要件がどこまで書かれているか未確認である。特許も調べていない。物理的なシード保管は製品が先行しており、意匠や特許に日用品への偽装を謳ったものがある可能性があるので、Google PatentsとJ-PlatPatの調査が残っている。相続と時間錠の系統も追い切れておらず、BIP-65とBIP-112の提案本文、Miniscriptに基づく相続用ウォレット、暗号資産相続の法学寄り文献を確認していない。被引用の追跡も不十分で、OpenAlexとSemantic Scholarが調査途中でレート制限に掛かったため、codex32や視覚復号型秘密分散を引用する新しい論文を芋づる式に辿る作業が止まっている。bitcoin-devメーリングリストの議論やBlockchain Commonsの設計文書群といった実務家コミュニティの一次資料、および国内の取引所の鍵管理開示文書や金融庁の指針も未確認である。

==========================================================================================
## [08-puf-physical-crypto] 物理複製困難関数と物理的な一方向性関数  (確認45 / 未検証5 / 訂正31 / 削除0)

### 要約
物理複製困難関数の研究は、Pappuらが2002年にScienceで示した物理的一方向性関数を起点に、シリコン系、光散乱系、紙や表面の微細構造による個体識別へと広がった。日本語圏では同じ概念が人工物メトリクスと呼ばれ、松本勉らのナノ人工物メトリクスが代表的である。この分野は「物理的な乱れは複製できないので鍵にしてよい」と主張しており、CipherFluteの「物理層に秘匿の力はない」という宣言と正反対に見えるが、実際には矛盾しない。物理複製困難関数が使う乱れは製造者にも制御できない微視的な乱れであり、設計図どおりに作られる巨視的な形状ではない。CipherFluteの管長は設計図そのものなので、定義上そもそも物理複製困難関数ではない。この整理により、CipherFluteの宣言は学術的に正しいと言える。複製の容易さも裏付けが取れた。Laxtonらは写真から物理鍵の刻みを復元し、Rameshらは差し込み音だけから刻みを推定し、Al FaruqueらとSongらは3Dプリンタの動作音から印刷中の形状を復元している。さらにMarakisらは光学的物理複製困難関数の複製に成功しており、物理複製困難性そのものが絶対でないことも分かった。一方で、電源も電子部品も持たない受動的な3Dプリント共鳴体の共鳴周波数のばらつきを物理複製困難関数として使う研究は見つからなかった。音響物理複製困難関数を名乗る研究はセンサノードを対象とするものと査読前原稿だけである。CipherFluteを物理複製困難関数の方向へ発展させる道は学術的に空いている。

### 脅威の大きい文献
- 【中】Sensor Identification via Acoustic Physically Unclonable Function
  著者: Girish Vaidya, T. V. Prabhakar, Nithish Gnani, Ryan Shah, Shishir Nagaraja
  掲載: Digital Threats: Research and Practice（ACM）, 2022年, pp.1-25
  URL: https://doi.org/10.1145/3488306
  関係: 「音響」と「物理複製困難関数」を結び付けた最も近い先行例である。ただし対象は電源とマイクロホンを持つセンサノードで、製造公差を識別の情報源として使う。CipherFluteは電源も電子部品も持たず、逆に製造ばらつきを基準笛で打ち消し、識別子ではなく任意のビット列を運ぶ。
  脅威理由: 用語「acoustic PUF」を先に取られているため、CipherFluteが音響と物理複製困難性を不用意に結び付けて語ると衝突する。ただし読み出し機構も目的も異なるので主張は崩れない。
- 【中】Reconsidering Physical Key Secrecy: Teleduplication via Optical Decoding
  著者: Benjamin Laxton, Kai Wang, Stefan Savage
  掲載: ACM CCS 2008, pp.469-478
  URL: https://doi.org/10.1145/1455770.1455830
  関係: 写真から物理鍵の刻みを完全に復元して複製できることを示した研究である。CipherFluteの「形状を計測されれば無音で読める、複製も容易である」という宣言を、物理鍵について先に実証したものにあたる。
  脅威理由: CipherFluteの脅威モデルを支える側だが、引用しないと「物理層に秘匿がない」という宣言が学術的裏付けを欠く。
- 【中】Listen to Your Key: Towards Acoustics-based Physical Key Inference（SpiKey）
  著者: Soundarya Ramesh, Harini Ramprasad, Jun Han
  掲載: ACM HotMobile 2020, pp.3-8
  URL: https://doi.org/10.1145/3376897.3377853
  関係: 鍵を差し込む音のクリック間隔だけから刻みを推定し、33万本の候補を3本まで絞った。CipherFluteは正規の読み出しと盗聴が同じ物理量（音）を共有するため、利用者が吹いた音を録音されれば秘密が漏れるという攻撃面をこの文献が先に定式化している。
  脅威理由: 新規性は崩さないが、音響的な盗聴という攻撃面の先行定式化なので引用と差分の記述が必須である。
- 【中】Unclonable security features for additive manufacturing
  著者: O. Ivanova, A. Elliott, T. A. Campbell, C. B. Williams
  掲載: Additive Manufacturing, 2014年, pp.24-31
  URL: https://doi.org/10.1016/j.addma.2014.07.001
  関係: 量子ドットを分散させた樹脂を材料噴射方式で造形物内部に埋め込み、液滴単位の確率的配置を物理複製困難関数の中核にする提案である。CipherFluteも3Dプリント物に秘密を持たせるが、乱れではなく設計どおりの管長を使い、顕微鏡ではなく人の息で読む。
  脅威理由: 「3Dプリント物にセキュリティ機能を埋め込む」系譜の代表的先行例であり、この系譜に自分を置くなら落とせない。
- 【中】3D Unclonable Optical Identity for Universal Product Verification
  著者: Chenxing Wang, Lily Raymond, Yifei Jin, Alireza Tavakkoli, Haoting Shen
  掲載: IEEE HOST 2021, pp.136-146
  URL: https://doi.org/10.1109/HOST49136.2021.9702273
  関係: 電子部品を持たない三次元タグにランダム微細構造で複製困難な同一性を与え、携帯電話程度の機材で検証する。CipherFluteと目標が近いが、読み出しは光学であり、運ぶのは同一性であって秘密のビット列ではない。
  脅威理由: 「電子部品なしの物体に検証可能な同一性を与える」という主張の一部が重なるため、差分の明示が要る。
- 【中】Acoustic Side-Channel Attacks on Additive Manufacturing Systems / My Smartphone Knows What You Print
  著者: Mohammad Abdullah Al Faruque, Sujit Rokka Chhetri, Arquimedes Canedo, Jiang Wan ／ Chen Song, Feng Lin, Zhongjie Ba, Kui Ren, Chi Zhou, Wenyao Xu
  掲載: ACM/IEEE ICCPS 2016, pp.1-10 ／ ACM CCS 2016, pp.895-907
  URL: https://doi.org/10.1109/ICCPS.2016.7479068
  関係: 3Dプリンタの動作音（およびスマートフォン内蔵センサ）から印刷中の形状を復元できることを示した二件である。CipherFluteは秘密を含む笛を利用者が家庭で印刷する運用なので、印刷現場に録音機があれば製造時に秘密が漏れる。
  脅威理由: 主張は崩さないが、脅威モデルに「製造時の副次経路」を書き足す根拠であり、完全性のために引用が要る。
- 【中】Physical One-Way Functions
  著者: Ravikanth Pappu, Ben Recht, Jason Taylor, Neil Gershenfeld
  掲載: Science, 2002年, pp.2026-2030
  URL: https://doi.org/10.1126/science.1074376
  関係: 物理複製困難関数という分野の出発点である。CipherFluteの笛は設計図どおりの管長を持ち、応答が完全に予測でき同じ設計から何本でも作れるので、この定義を意図的に満たさない。対比によってCipherFluteの宣言が「弱さの告白」ではなく「定義上の位置づけ」だと示せる。
  脅威理由: 主張は崩さないが、この対比を書かないと査読者から「なぜ物理複製困難関数にしないのか」と必ず問われる。
- 【中】Nano-artifact metrics based on random collapse of resist（人工物メトリクスの系譜）
  著者: Tsutomu Matsumoto, Morihisa Hoga, Yasuyuki Ohyagi, Mikio Ishikawa, Makoto Naruse ほか
  掲載: Scientific Reports, 2014年（続報は Scientific Reports 2016年、情報処理学会論文誌 66(3), 2025年）
  URL: https://doi.org/10.1038/srep06142
  関係: 日本語圏で物理複製困難関数に相当する概念は「人工物メトリクス」と呼ばれ、他人受入率・本人拒否率・耐クローン率という評価尺度が定着している。CipherFluteは日本語の学会に投稿するので、この語彙で「人工物メトリクスではない」ことを説明する義務がある。
  脅威理由: 日本語圏の読者に対する位置づけ説明が必要になる。CipherFluteの笛には耐クローン率が定義できず、むしろ同一設計が同一応答を返すことが目的だと明記すればよい。

### 調べ残した穴
調査の途中でOpenAlexが応答制限（再試行まで約24時間）となり、被引用のたどり直しを最後まで実行できなかった。特にPappu 2002の被引用のうちデジタルファブリケーション寄りの枝と、Vaidyaの音響物理複製困難関数の被引用を追い切れていない。ACM Digital LibraryとIEEE Xploreの全文検索、Semantic ScholarとGoogle Scholarの被引用一覧も使えず、芋づる式の探索が想定より浅い。ACMについてはCrossrefの題名検索で代替したが、題名に「unclonable」を含まず抄録や本文にだけ含むヒューマンコンピュータインタラクション系の論文は取りこぼしている可能性がある。特許文献はまったく調べていないため、3Dプリント物の音響的な認証や笛を使った識別について特許が先行している可能性が残る。カードを使う物理暗号（card-based cryptography）の系譜は今回の切り口から外して未調査であり、「電源を使わない暗号」という括りで語るなら別途整理が要る。物理複製困難関数の応答から鍵を安定に取り出す誤り訂正の理論（fuzzy extractor、secure sketch）は名前を確認しただけで一次資料に当たっておらず、CipherFluteのReed-Solomon符号の設計との関係を整理し切れていない。経年による応答のずれに関する研究も列挙しただけで内容を読んでいない。また、Research Squareの査読前原稿「Listening to disorder」は本文にアクセスできず、もし受動的な3Dプリント構造の共鳴を扱っていた場合には脅威が「高」に上がる可能性があるため、投稿前に本文の入手を強く勧める。

==========================================================================================
## [09-data-over-sound] 音でデータを送る通信方式の歴史と現在  (確認49 / 未検証14 / 訂正9 / 削除0)

### 要約
音でデータを送る技術は1960年前後に電話網で体系化された。Schenkerの二群音声周波数符号（1960年、のちのITU-T勧告Q.23）が周波数スロット符号の原型であり、V.21のモデムとT.30のファクシミリ手順が音声帯域を汎用の搬送路にした。1970年代の音響カプラ、1975年のKansas City標準によるカセットテープへの音の固定、1984年のイギリスの放送によるプログラム配布と、音の波形を物理媒体や放送に固定して配る発想はこの時期に出そろっている。2000年代からはLopesとAguiarを起点に空中音響通信の研究が始まり、2002年には音響楽器のピアノとクラリネットと鐘を送信機に使う論文まで出ている。以後は音響OFDM、チャープ信号、音響電子透かしが加わり、2010年代には超音波ビーコンが商用化され、規制当局の関心も集めた。この系譜のなかでCipherFluteは、送信機が形状として固定されて書き換えができず、電源を持たず、人の息だけで駆動するという極端な特殊例に位置づく。符号の組み合わせ自体はggwaveなどが既に採っているため、新規性は符号層ではなく受動的な造形物という送信機の側と、日用品への偽装および秘密分散という運用の側に置くべきである。

### 脅威の大きい文献
- 【高】Aerial communications using piano, clarinet, and bells
  著者: N. Domingues, J. Lacerda, P. M. Q. Aguiar, C. V. Lopes
  掲載: 2002 IEEE Workshop on Multimedia Signal Processing (MMSP), pp. 460-463, 2002年
  URL: https://doi.org/10.1109/MMSP.2002.1203345
  関係: ピアノ、クラリネット、鐘という音響楽器が出す楽音そのものを送信機として空中でデータを送る研究である。CipherFluteが笛の楽音の高さを記号として使うのと、着想の中核が重なる。ただし送信機は任意の音列を出せる能動的な装置であり、形状が符号を固定してはいない。
  脅威理由: 楽音を通信の記号語彙に使うという中核の着想が2002年に先行しているため、CipherFluteが「楽器の音でデータを運ぶ」水準で新規性を主張すると崩れる。差分は受動的な造形物で符号が形状として不可逆に固定される点に絞る必要がある。
- 【中】ggwave（データ・オーバー・サウンドの実装ライブラリ）
  著者: Georgi Gerganov
  掲載: オープンソースソフトウェア（学術発表ではない）
  URL: https://github.com/ggerganov/ggwave
  関係: 4.5キロヘルツの帯域に96個の等間隔の周波数を並べる多周波の周波数偏移変調に、Reed–Solomon符号による訂正を組み合わせている。CipherFluteの符号層とほぼ同一の構成である。異なるのは送信がスピーカーであるか造形物であるかだけである。
  脅威理由: 周波数スロットへの記号割り当てと誤り訂正という符号設計に新規性がないことを明確に示す資料であるため、論文が符号層を新規性として書いていると弱くなる。物理層と運用に主張を寄せる限りは引用で足りる。
- 【中】Pushbutton Calling with a Two-Group Voice-Frequency Code
  著者: L. Schenker
  掲載: Bell System Technical Journal, vol. 39, no. 1, pp. 235-255, 1960年1月
  URL: https://archive.org/details/bstj39-1-235
  関係: 可聴域に離散的な周波数の集合を定め、その組み合わせに記号を割り当て、受信側は周波数の同定だけで復号する。CipherFluteが半音刻みの13スロットに記号を割り当てる考え方の直接の原型である。のちにITU-T勧告Q.23として標準化された。
  脅威理由: 周波数スロットによる符号化の原型であり、これを引かずに周波数を語彙にすることを新しく述べると電話技術の常識を知らないと見られる。現行論文はQ.23を挙げているが技術的出典まで遡ると位置づけが明確になる。
- 【中】Kansas City標準（家庭用カセットテープへのデータ記録方式）
  著者: BYTE誌が招集した規格検討会（1975年11月7日から8日、ミズーリ州カンザスシティ）、1976年2月号掲載
  掲載: BYTE Magazine, 1976年2月号
  URL: https://www.swtpc.com/mholley/AC30/KansasCityStandard.html
  関係: 論理の1を2400ヘルツ8周期、論理の0を1200ヘルツ4周期で表し、最大300ボーで送る。音の符号を物理媒体に固定して保管し、再生して読み出すという枠組みをCipherFluteより半世紀前に大量実用化している。
  脅威理由: 「音の符号を物に固定して保存する」枠組みの最も重要な先行例であり、これを踏まえずに保管媒体としての新規性を述べると弱い。ただし読み出しに機械と電源を要する点で決定的に異なる。
- 【中】HAPADEP: Human-Assisted Pure Audio Device Pairing
  著者: Claudio Soriente, Gene Tsudik, Ersin Uzun
  掲載: Information Security (ISC 2008), Lecture Notes in Computer Science, pp. 385-400, 2008年
  URL: https://doi.org/10.1007/978-3-540-85886-7_27
  関係: 共通鍵も既存の無線路も持たない二台の機器が、音だけで鍵素材を交換し、人間が聞いて確認することで中間者攻撃を排除する。CipherFluteが暗号資産の復元用情報という鍵素材を音で運ぶことと重なる。
  脅威理由: 鍵素材を音の通路で運ぶ応用が先行しているため、CipherFluteはその応用ではなく「鍵を形として保管し必要なときだけ音として取り出す」という保管の側面に主張を寄せる必要がある。
- 【中】On the Privacy and Security of the Ultrasound Ecosystem
  著者: Vasilios Mavroudis, Shuang Hao, Yanick Fratantonio, Federico Maggi, Christopher Kruegel, Giovanni Vigna
  掲載: Proceedings on Privacy Enhancing Technologies, vol. 2017, no. 2, pp. 95-112, 2017年
  URL: https://doi.org/10.1515/popets-2017-0018
  関係: 商用の超音波ビーコン生態系を体系的に調べ、信号が誰にでも受信でき記録と再生で複製できるため認証や課金の根拠にできないことを実証している。CipherFluteの「音響層に秘匿の力は無い」という宣言を裏づける。
  脅威理由: 脅威モデルの主張が独自ではなく先行研究に沿ったものであることを示すため、引用しないと既知の事実を発見として書いていると見られる危険がある。引用すれば逆に主張の裏づけになる。
- 【中】空中音波通信技術とその応用（解説）
  著者: 西村明（東京情報大学）
  掲載: 日本音響学会誌, 第77巻, 第6号, pp. 390-395, 2021年
  URL: https://www.jstage.jst.go.jp/article/jasj/77/6/77_390/_article/-char/ja
  関係: 空気中を伝わる音でデータを送る技術を音響電子透かしと音響モデムの二系統に分けて整理した日本語の解説である。既存の方式がすべて能動的なスピーカーを前提にしていることを、この解説を根拠に述べられる。
  脅威理由: 日本語で書かれた数少ない体系的な解説であり、引かずに空中音響通信を語ると調査不足に見える。内容自体はCipherFluteの主張を脅かさない。
- 【中】Dhwani: secure peer-to-peer acoustic NFC
  著者: Rajalakshmi Nandakumar, Krishna Kant Chintalapudi, Venkat Padmanabhan, Ramarathnam Venkatesan
  掲載: ACM SIGCOMM 2013, pp. 63-74, 2013年
  URL: https://doi.org/10.1145/2486001.2486037
  関係: スマートフォンのスピーカーとマイクだけで近距離無線通信に相当する機能を実現し、受信側が意図的に雑音を出して盗聴を妨害することで物理層に機密性を作ろうとする。物理層に機密性を一切期待しないCipherFluteと対照的である。
  脅威理由: 音による近接通信の代表的研究であり、音で秘密を渡す文脈で必ず参照される位置にある。ただし送信機が電子機器である点で系統が異なるため、脅威は差分の明示で解消できる。

### 調べ残した穴
IEEE XploreとACM Digital Libraryが自動取得を拒むため、最大の脅威候補であるDominguesらの2002年の論文について書誌情報しか確認できず、記号の設計と伝送速度が未確認のまま残った。図書館経由での本文入手を強く勧める。特許の調査をまったく行えておらず、音で開く錠や受動的な発音体で符号を出す装置の特許が存在する可能性がある。音による機器設定については、Amazon Dash Buttonの音による無線設定、Chromecastのゲストモードの超音波ペアリング、インドのGoogle Payの音響決済のいずれも一次資料に到達できなかった。船舶と航空については海上衝突予防規則と航法援助施設のモールス識別まで確認したが、水中電話や水中鐘、霧笛の符号体系の歴史に踏み込めなかった。アマチュア無線の低速度走査テレビジョンやPSK31、無線ファクシミリという音声帯域データ通信の長い実践も追えていない。さらに、蓄音機のレコード、オルゴールの円筒、自動ピアノのロール、映画フィルムの光学サウンドトラックという「形状が波形を固定する」古典的媒体を体系的に押さえられておらず、CipherFluteをその系譜に置く議論の材料が不足している。Chirpの技術文書とLISNRの白書も未取得で、商用方式の情報量とCipherFluteの1本あたり約3.7ビットを並べた比較ができていない。

==========================================================================================
## [10-codes-for-physical-media] 低容量の物理媒体のための符号化と誤り訂正  (確認57 / 未検証14 / 訂正16 / 削除0)

### 要約
情報を物理媒体に載せる技術は、記号の作り方を制限する制約符号と、壊れた記号を直す誤り訂正符号という二層構造をほぼ例外なく採っている。CipherFluteの隣接同音禁止は、この制約符号の系譜のうち同じ記号が続くと切れ目を見失うという問題への古典的な処方であり、ランレングス制限符号（Franaszek 1970、Tang and Bahl 1970、Immink 1990）と8B/10B符号（Widmer and Franaszek 1983）がその原典である。ただし機構として最も近い実例は磁気記録ではなくDNA保存であり、Goldmanらは2013年に「次の塩基は直前と必ず異なるものから選ぶ」という写像で同一記号の連続を構造的に排除している。素数個の記号を扱う設計にも先例があり、PDF417は0から928までの929個の符号語（929は素数）を扱い、Grassらは媒体の記号数に合わせた非二進の有限体上でリード・ソロモン符号を組んでいる。二のべき乗でない記号数の扱いは郵便のIntelligent Mail Barcodeがさらに徹底しており、1365進などの混合基数へ変換したうえで13ビット中の1の個数を5個または2個に固定した定重み符号へ写している。応用面ではcodex32（BIP-93）が、紙と鉛筆だけで計算できるGF(32)上のBCH符号つきの秘密分散として、CipherFluteと同じ目的をすでに達成している。一方で、こうした符号設計を3Dプリント造形物へ実際に適用した例は乏しく、最も近いLayerCodeは24ビットしか載せず、誤り訂正の冗長を意図的に付けていないと明記している。この空白がCipherFluteの符号面の足場になる。

### 脅威の大きい文献
- 【高】Toward practical high-capacity low-maintenance storage of digital information in synthesised DNA
  著者: Nick Goldman, Paul Bertone, Siyuan Chen, Christophe Dessimoz, Emily M. LeProust, Botond Sipos, Ewan Birney
  掲載: Nature, 第494巻, 第7435号, 77-80ページ, 2013年
  URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC3672958/
  関係: バイト列を三進の桁へ変換し、各桁を「直前に使った塩基とは異なる三塩基のいずれか」へ写すことで、同一記号の連続を構造的に排除している。これはCipherFluteの隣接同音禁止とまったく同じ機構であり、記号数を4から実効3へ落とす数え方まで一致する。断片の重なりによる冗長、索引、単純パリティという層構造も対応する。
  脅威理由: 隣接記号を必ず変えるという制約を、低容量の物理媒体で確立した有名な先行研究である。CipherFluteがこの制約を自身の工夫として述べると主張が崩れるため、8B/10Bよりも近い先例として必ず引用し差分を述べる必要がある。
- 【高】codex32: Checksummed SSSS-aware BIP32 seeds (BIP-93)
  著者: Leon Olsson Curr, Pearlwort Sneed, Andrew Poelstra
  掲載: Bitcoin Improvement Proposal 93, Draft, 2023年2月13日
  URL: https://github.com/bitcoin/bips/blob/master/bip-0093.mediawiki
  関係: 暗号資産のシードをShamirの秘密分散で分割し、GF(32)上のBCH符号による検査符号（13文字または15文字）を付ける規格である。最大8文字の誤り検出、4文字の置換訂正、8文字の消失訂正を保証する。小さな有限体と線形符号を選んだことで、分割も復元も検査も紙と鉛筆だけで実行できると明言している。
  脅威理由: 目的（シードの物理保管）、安全性の負わせ方（秘密分散）、誤り訂正符号の役割がCipherFluteとほぼ完全に重なる。しかも復号に電子機器を一切要しない点でCipherFluteより徹底しており、電源不要性の主張を対比のうえで述べ直す必要がある。
- 【中】Robust chemical preservation of digital information on DNA in silica with error-correcting codes
  著者: Robert N. Grass, Reinhard Heckel, Michela Puddu, Daniela Paunescu, Wendelin J. Stark
  掲載: Angewandte Chemie International Edition, 第54巻, 第8号, 2552-2555ページ, 2015年
  URL: https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=TITLE%3A%22Robust%20chemical%20preservation%20of%20digital%20information%20on%20DNA%20in%20silica%20with%20error-correcting%20codes%22&format=json&resultType=core
  関係: 媒体固有の記号数に合わせて非二進の有限体を選び、その上に内符号と外符号を重ねたリード・ソロモン符号を組む、という設計の順序がCipherFluteと同じである。83キロバイトを4,991本の断片へ載せ、シリカ封止で数千年の保存を主張している。長期保存という動機の面でも近い。
  脅威理由: 媒体は異なるが「符号語の個数を物理記号数に合わせて非二進のリード・ソロモン符号を組む」判断の先例であり、CipherFluteの13進の扱いの新規性を弱める。引用して設計判断の系譜を示す必要がある。
- 【中】Intelligent Mail Barcode 4-State SPECIFICATION (USPS-B-3200, Rev H)
  著者: 米国郵政公社（承認者 Stephen M. Dearing、責任技術者 John E. Werntz）
  掲載: USPS-B-3200 CAGE CODE 27085, Rev H, 2015年4月20日
  URL: https://www.legis.iowa.gov/docs/publications/SD/1034080.pdf
  関係: 11ビットの巡回冗長検査を計算したうえで、データを1365進や636進や659通りという混合基数へ変換し、各符号語を「13ビット中に1が5個」または「13ビット中に1が2個」という定重み符号へ写している。検査ビットは対応する文字のビット反転として記号列に畳み込む。二のべき乗でない記号数の扱いと定重み制約の課し方がCipherFluteの13スロットと直接対応する。
  脅威理由: 13進の記号を扱うことや制約を課すこと自体は、四十年近く運用されている郵便標準がすでに実行している。新規性としてこれを述べると指摘されるが、引用すれば設計が実務の作法に沿う裏づけにもなる。
- 【中】LayerCode: Optical Barcodes for 3D Printed Shapes
  著者: Henrique Teles Maia, Dingzeyu Li, Yuan Yang, Changxi Zheng
  掲載: ACM Transactions on Graphics, 第38巻, 第4号, 論文番号1, 2019年（SIGGRAPH 2019）
  URL: https://www.cs.columbia.edu/cg/layercode/LayerCode_Maia_et_al_2019_lowRez.pdf
  関係: 層の絶対厚みではなく隣接二層の厚み比の対数差で符号化し、撮影倍率という未知の全体的なずれを打ち消している。これはCipherFluteの基準笛と同じ狙いを差分符号化で果たす設計である。一方で埋め込んだのは24ビット（近赤外では12ビット）にとどまり、誤り訂正の冗長を「あえて付けていない」と本文で明記している。
  脅威理由: すでに引用済みだが、比で読むという設計の一致に触れずに済ませると差分が曖昧になる。同時に、誤り訂正なし24ビットという事実はCipherFluteの128ビット誤り訂正つきという主張の強さを示す最良の対比材料である。
- 【中】Embracing Errors Is More Efficient Than Avoiding Them Through Constrained Coding for DNA Data Storage
  著者: Franziska Weindel, Andreas L. Gimpel, Robert N. Grass, Reinhard Heckel
  掲載: arXiv:2308.05952, 2023年8月11日投稿・2024年6月26日改訂
  URL: https://arxiv.org/abs/2308.05952
  関係: 同一記号の連続を避ける制約符号と、制約を課さずに誤りを受け入れて誤り訂正の冗長で払う方式とを定量的に比較し、現行のDNA保存系では制約符号が非効率だと結論している。CipherFluteは制約と誤り訂正の両方を採用しているため、その配分の妥当性を問う枠組みを与える。
  脅威理由: 「なぜ制約と誤り訂正を両方入れるのか」という査読者の問いに直結する。CipherFluteの隣接同音禁止は置換誤り率ではなく無音区切りの同期のために必要だと反論を用意しておかないと、符号設計の根拠が弱く見える。
- 【中】Capacity-Approaching Constrained Codes with Error Correction for DNA-Based Data Storage
  著者: Tuan Thanh Nguyen, Kui Cai, Kees A. Schouhamer Immink, Han Mao Kiah
  掲載: IEEE Transactions on Information Theory, 第67巻, 第8号, 5602-5613ページ, 2021年（プレプリント arXiv:2001.02839）
  URL: https://arxiv.org/abs/2001.02839
  関係: 同一記号の連続長の制限と含量の釣り合いという制約を満たしつつ、一個の編集誤りを訂正できる符号を、制約符号と誤り訂正符号を一体として設計している。CipherFluteが両者を単純に重ねているのに対し、一体設計のほうが符号化率で優ることを示している。
  脅威理由: CipherFluteの符号を「制約符号と誤り訂正符号の単純な連接」と正確に述べたうえで一体設計という改良余地に触れないと、符号理論側の査読者から素朴だと見なされる。
- 【中】ggwave（音による小容量データ伝送ライブラリ）
  著者: Georgi Gerganov
  掲載: オープンソースソフトウェア（GitHubリポジトリ）
  URL: https://github.com/ggerganov/ggwave
  関係: 4.5キロヘルツ帯を96個の等間隔な周波数に分け、4ビットずつを音へ写して6音同時に送る多周波の周波数偏移変調である。誤り訂正にリード・ソロモン符号を用い、冗長バイト数をデータ長に応じて決める。周波数の集合を記号の語彙としてリード・ソロモン符号を載せるという構成がCipherFluteとほぼ同一である。
  脅威理由: 「音の高さを記号にして誤り訂正符号を載せる」こと自体に先例があると示す文献であり、引用せずに新規性を主張すると危うい。差分は記号を発するのが電源を持たない受動的な造形物である点に絞られる。

### 調べ残した穴
第一に、ISO/IEC 16022（Data Matrix）、ISO/IEC 15438（PDF417）、ISO/IEC 24778（Aztec Code）の規格本体に到達できず、ECC 200の訂正能力の数値やQRコードの水準Lと水準Hの割合を一次資料で確認できなかった。第二に、Grassらの2015年の論文が有限体GF(47)を用いたという広く引用される記述は、出版社のページが有料で本文に到達できず未確認のまま残った。第三に、コンパクトディスクのCross-Interleaved Reed-Solomon Codeと、EFMという制約符号とインターリーブを三層に重ねる設計について、Imminkによる一次資料を読めていない。CipherFluteの層構造の最も整った先例であるため、ここは追加調査の価値が高い。第四に、被引用をたどる作業が不十分であり、特にGoldmanらの2013年の論文と繰り返し禁止符号（Elishcoら）の被引用一覧をたどれば、隣接記号を必ず変える制約で達成可能な符号化率の理論的上界が得られるはずである。CipherFluteが13から実効12へ落とす損失が最適かどうかを述べたいなら必要である。第五に、日本語文献の探索が二次元コードに偏り、情報処理学会電子図書館とJ-STAGEを直接検索していないため、記録媒体の変調符号や物体への情報埋め込みに関する国内の解説を取りこぼしている可能性がある。加えて、この会話ではWeb検索の回数上限に達したため、以降はDuckDuckGoの簡易ページ、Crossref、arXiv、Europe PMC、CiNiiの各APIと出版社ページの直接取得のみで調査した。

==========================================================================================
## [11-physical-security-steganography] 物理的な鍵とトークンの安全性、および物理的な隠蔽  (確認63 / 未検証6 / 訂正25 / 削除0)

### 要約
この切り口で最も危険なのは「先に同じものを作られていた」型ではなく、「物理層が探索コストを引き上げる」という主張自体を定量的に切り崩す実証の系列であった。ジョンストンは広く使われる封印120種類すべてが平均5分未満、平均55ドルで破られたと報告し、アペルは投票機の錠を平均13秒で開け、法廷で全封印を45分未満で痕跡なく脱着した。物理層の防護は分と数十ドルの単位で測られるため、CipherFluteはこの数字を引いて主張の大きさを抑えるべきである。他方、偽装の効果を支える証拠もあり、ウルフらの出現率効果は、敵が疑っていなければ目の前の物でも見落とされることを示す。逆にクロフォードとイリベリの隠れ場所実験は、隠す側の選択が体系的に予測されうることを示す反証側の証拠である。物理鍵の複製では、写真から鍵を復元するSneakeyとDeepKey、3Dプリンタで制限キーウェイを破るBurgessら、印影から印章を偽造する木村らが、CipherFluteの脅威モデルの宣言を強く裏づける。物理暗号の側では視覚暗号、音響暗号、カードベース暗号、3Dプリンタ製の物理暗号装置、手計算可能な誤り訂正付き秘密分散codex32が隣接する。一方で、隠し金庫の有効性、強要下の否認可能な物理保管、偽装効果の定量化はいずれも学術的な空白であった。

### 脅威の大きい文献
- 【高】Tamper-Indicating Seals for Nuclear Disarmament and Hazardous Waste Management
  著者: Roger G. Johnston
  掲載: Science & Global Security, Vol.9, pp.93-112, 2001年
  URL: https://doi.org/10.1080/08929880108426490
  関係: ロスアラモス国立研究所の脆弱性評価チームが、広く使われている120種類の封印すべてを一般入手可能な低技術の道具で破ったと報告している。熟練者1人あたりの平均所要時間は5分未満、攻撃の平均費用は55ドルであった。CipherFluteが物理層に期待できる防護の大きさの上限を、実測値として示す一次資料である。
  脅威理由: CipherFluteに残る唯一の物理層の主張が「探索コストの引き上げ」であるところ、この研究は同種の物理的防護が分単位・数十ドル単位で崩れることを120種類の実測で示しており、主張を大幅に割り引かせる。引かずに書けば根拠のない楽観と読まれる。
- 【高】Security Seals on Voting Machines: A Case Study
  著者: Andrew W. Appel
  掲載: ACM Transactions on Information and System Security, Vol.14, No.2, Article 18, 2011年
  URL: https://doi.org/10.1145/2019599.2019603
  関係: 著者はピッキング未経験から40ドル未満の工具と数時間の練習で錠を平均13秒で開け、テープ封印はヒートガン80秒で痕跡なく剥がし、法廷で全封印の脱着を45分未満で実演した。物理的防護は「遅延を生むか事後に検出されるか」を満たさなければ価値がないという判定基準も示している。
  脅威理由: 物理層の保護が素人でも数十分で無効化されることを、具体的な秒数とともに査読付き主要誌で示している。CipherFluteの「探索コストの引き上げ」を定性的に書くことを許さず、同じ判定基準による自己評価を要求する。
- 【中】Fatal Attraction: Salience, Naivete, and Sophistication in Experimental "Hide-and-Seek" Games
  著者: Vincent P. Crawford, Nagore Iriberri
  掲載: American Economic Review, Vol.97, No.5, 2007年
  URL: https://doi.org/10.1257/aer.97.5.1731
  関係: 隠す側と探す側の対戦実験で、隠す側が顕著性の高い選択肢に体系的に引き寄せられ、あるいは避け、その偏りが探す側に読まれて利用されることを定量化した。理論上は一様ランダムに隠すべきなのに、人間はそうできない。
  脅威理由: CipherFluteの主張の成立条件（利用者が選ぶ隠し場所が敵に予測されないこと）を実験で突きつける。主張を直接否定はしないが、限界を述べずに引用しないのは片手落ちである。
- 【中】Rare items often missed in visual searches（および Low target prevalence is a stubborn source of errors in visual search tasks）
  著者: Jeremy M. Wolfe, Todd S. Horowitz, Naomi M. Kenner（2005年）／ Wolfe, Horowitz, Van Wert, Kenner, Place, Kibbi（2007年）
  掲載: Nature, Vol.435, 2005年 ／ Journal of Experimental Psychology: General, Vol.136, No.4, 2007年
  URL: https://doi.org/10.1038/435439a
  関係: 標的の出現率が低いほど見落としが劇的に増える出現率効果を示し、その効果が訓練でも容易に消えない頑健なものであることを確かめた。敵が「そこに秘密がある」と期待していない限り、目の前にあっても見落とされる。
  脅威理由: 「日用品への偽装が探索コストを上げる」という主張を裏づける最良の外部証拠であり、引用しないと主張が直感の表明に見える。同時に、敵が疑っている状況では効果が消えるという条件を明示させる。
- 【中】Replication Prohibited: Attacking Restricted Keyways with 3D-Printing
  著者: Ben Burgess, Eric Wustrow, J. Alex Halderman
  掲載: USENIX Workshop on Offensive Technologies (WOOT), 2015年
  URL: https://scholar.archive.org/work/fe05aa46-5454-46d5-a0c1-0334d8133ca6
  関係: 複製禁止や特許で守られた制限付きキーウェイの鍵を消費者向け3Dプリンタで出力し、実際の錠を開けた。物理鍵の安全性がキーブランクの入手困難性に依存していたところ、その制約が積層造形で消えたことを示す。
  脅威理由: CipherFluteの「形状を計測されれば複製できる」という宣言が、まったく同じ技術で既に実証済みの事実であることを裏づける。物理層の複製困難性に少しでも寄りかかった記述があれば、この研究の存在で成立しなくなる。
- 【中】Audio and Optical Cryptography（および Nonbinary Audio Cryptography、物理的復元が容易な音響秘密分散法）
  著者: Yvo Desmedt, Shuang Hou, Jean-Jacques Quisquater（1998年）／ Desmedt, Le, Quisquater（2000年）／ 徳重佑樹, 三澤裕人, 吉田文晶（2015年）
  掲載: ASIACRYPT'98, 1998年 ／ Information Hiding 2000 ／ 電子情報通信学会技術研究報告 Vol.115 No.38 pp.75-80, 2015年
  URL: https://doi.org/10.1007/3-540-49649-1_31
  関係: 視覚暗号の音響版であり、複数の音響シェアを同時に再生すると人間の聴覚が干渉によって秘密を復元する。計算機なしに感覚器だけで復号できる点が要点である。徳重らは波の干渉と周波数分割で物理的復元が容易な音響秘密分散を提案している。
  脅威理由: CipherFluteが「音で秘密を運ぶ」あるいは「2つそろって初めて意味を持つ物理媒体」に新規性を置くと正面衝突する。受動的な造形物が音高で符号を運ぶ点に限定すれば衝突しないため、差分の明示が必須である。
- 【中】3Dプリンタによる印影からの印章の偽造
  著者: 木村悠生, 山元陽佑雅, 榎竜盛, 上原哲太郎
  掲載: マルチメディア，分散，協調とモバイルシンポジウム2023論文集, pp.1269-1276, 2023年
  URL: https://cir.nii.ac.jp/crid/1050860532220398464
  関係: 押された印影の画像から安価な3Dプリンタで印章を偽造し、照合実験で姓の種類や文字数が判別精度に与える影響を評価している。日本で長く物理的な認証トークンだった印章が、その出力を観測するだけで再現される構図を示した。
  脅威理由: CipherFluteの脅威モデル（観測可能な物理トークンは3Dプリンタで複製される）の国内における一次事例であり、日本語圏の査読者が最初に想起する。引用を欠くと調査不足と受け取られる。
- 【中】3Dプリンタによるオープン装置や特殊カードケースの作成と対称関数の秘密計算への適用
  著者: 伊藤優樹, 四方隼人, 水木敬明, 菅沼拓夫
  掲載: コンピュータセキュリティシンポジウム2023論文集, pp.192-199, 2023年
  URL: https://cir.nii.ac.jp/crid/1050579444484578048
  関係: カードベース暗号プロトコルを実行するための物理装置を3Dプリンタで作製し、効率的なコミットメント加算と対称関数の秘密計算への有用性を示した。家庭用3Dプリンタで作った受動的な物体が暗号的役割を担う点でCipherFluteに最も近い日本語圏の研究である。
  脅威理由: 国内の査読者が真っ先に思い浮かべる隣接研究であり、引用して「向こうは物理暗号プロトコルの実行治具、こちらは秘密を運ぶ受動的な記憶媒体」という差分を述べる必要がある。

### 調べ残した穴
このセッションは開始時点でWeb検索の予算を使い切っていたため、一般のWeb検索を1回も使えず、Crossref、Internet Archive Scholar、arXiv、CiNii Research、著者公開PDFの直接取得だけで調べた。したがって学会の技術報告、DEF ConやBlack Hatの講演、特許、税関や警察の実務文献は拾えていない。とくに鍵の型どりと隠し金庫の実態はこの層に集中していると思われる。OpenAlexとSemantic Scholarが繰り返しHTTP 429を返したため、被引用関係をたどる芋づる式の探索がほとんどできず、ジョンストン、アペル、Burgessらの被引用一覧を追えていない。ACM Digital Library、IEEE Xplore、USENIXはいずれも403を返したため抄録の確認をCrossrefと著者公開版に頼り、Chameleon Devices（CHI 2017）は抄録全文を確認できていない。日本語文献については、情報処理学会電子図書館、WISS各年の予稿集ページ、インタラクションのプログラムページに直接当たれておらず、WISSで「隠す」「秘密」を扱ったインタフェース研究が残っている可能性がある。また税関や刑務所での隠匿物捜索の発見率、麻薬探知犬の性能評価、Ross Andersonのオープン系と閉鎖系の比較といった理論文献も未到達である。

==========================================================================================
## [12-sound-as-key-auth] 音を鍵とする認証の研究  (確認54 / 未検証6 / 訂正18 / 削除0)

### 要約
音を認証に使う研究は四つの流れに分かれる。第一に旋律やリズムを人間の記憶の助けとして合言葉に使う流れがあり、GibsonらのMusipass(NSPW 2009)を中心とする一連の仕事と、TapSongs(UIST 2009)、RhythmLink(UIST 2011)、Beat-PIN(AsiaCCS 2018)が属する。第二に環境音の一致を近接の証明に使う二要素認証の流れがあり、Sound-Proof(USENIX Security 2015)が代表で、その脆弱性と再設計がACM TOPS 2024にまとめられている。第三に音響チャネルを鍵交換の補助路に使う機器ペアリングの流れがあり、Talking to Strangers(NDSS 2002)、Loud and Clear(ICDCS 2006)、HAPADEP(ISC 2008)、Acoustic Integrity Codes(WiSec 2020)が並ぶ。第四に打鍵音やプリンタ音から秘密を推定する音響サイドチャネル攻撃の流れがある。この全体を通して見ると、CipherFluteの「音の層に秘匿の力はまったく無い」という立場は珍しい。HaleviとSaxenaがCCS 2010で音響チャネルの秘匿性は仮定できないと実験的に示し、Acoustic Integrity Codesが音響チャネルを完全性専用の公開路として設計し直した系譜だけが同じ方向を向いている。ただしこれらは電源を持つ機器同士の通信であり、電源を持たない受動的な物体が音高の符号として鍵素材そのものを保持する形は見つからなかった。したがってこの切り口からCipherFluteの新規性は崩れない。一方で3Dプリンタの音から形状が復元できる研究群があるため、印刷中に秘密が漏れるという指摘は脅威モデルに書き足す必要がある。

### 脅威の大きい文献
- 【中】Musipass: authenticating me softly with "my" song
  著者: Marcia Gibson, Karen Renaud, Marc Conrad, Carsten Maple
  掲載: Proceedings of the 2009 Workshop on New Security Paradigms (NSPW 2009), pp. 85-100, 2009年
  URL: https://doi.org/10.1145/1719030.1719043
  関係: 利用者が自分で選んだ楽曲を認証の秘密として使う方式であり、「音を鍵にする認証」の直系の先行研究である。ただし秘密は人間の記憶のなかにあり、音はその記憶を呼び出す手がかりにすぎない。CipherFluteは人間の記憶を当てにせず秘密を物体の管長として外部化するので、秘密の置き場所が正反対である。
  脅威理由: 音を認証の鍵にすること自体が2009年に既にやられていると指摘されうる筋がここにあるためである。同じ著者らの総説「Play That Funky Password!」(2015)も含めて引用し、記憶に預けるのか物体に預けるのかという違いを明示しないと新規性の説明が弱くなる。
- 【中】TapSongs: tapping rhythm-based passwords on a single binary sensor
  著者: Jacob O. Wobbrock
  掲載: Proceedings of the 22nd Annual ACM Symposium on User Interface Software and Technology (UIST 2009), pp. 93-96, 2009年
  URL: https://doi.org/10.1145/1622176.1622194
  関係: 知っている歌のリズムを押しボタン一つに叩き込んで認証する方式である。音楽的な構造を符号の語彙にするという発想をCipherFluteと共有するが、使う軸が時間軸である点が異なる。CipherFluteは周波数軸上の13スロットを語彙にしており、揺らぎの原因も人間の運動ではなく気温と息の強さに限られる。
  脅威理由: UISTという同種の会場で「音楽を鍵にする」発想が既に示されているため、必ず引用して符号の軸の違いを述べる必要がある。ただし時間軸と周波数軸の違いは明確なので主要な主張は崩れない。
- 【中】Beat-PIN: A User Authentication Mechanism for Wearable Devices Through Secret Beats
  著者: Ben Hutchins, Anudeep Reddy, Wenqiang Jin, Michael Zhou, Ming Li, Lei Yang
  掲載: Proceedings of the 2018 on Asia Conference on Computer and Communications Security (AsiaCCS 2018), pp. 101-115, 2018年
  URL: https://doi.org/10.1145/3196494.3196543
  関係: 秘密の拍のパターンを叩いて暗証番号を代替する方式であり、鍵空間と観察耐性の評価を含む。Beat-PINは「本人しか再現できない」ことを安全性の根拠にするのに対し、CipherFluteは「誰が吹いても同じ音が出る」ことを利点として設計しており、狙いが正反対である。
  脅威理由: 音楽的なパターンを鍵の語彙にする発想が主要なセキュリティ会議で確立していることを示す文献であり、隣接研究として引用が必要である。
- 【中】On pairing constrained wireless devices based on secrecy of auxiliary channels: the case of acoustic eavesdropping
  著者: Tzipora Halevi, Nitesh Saxena
  掲載: Proceedings of the 17th ACM Conference on Computer and Communications Security (CCS 2010), pp. 97-108, 2010年
  URL: https://doi.org/10.1145/1866307.1866319
  関係: 音響チャネルが秘密を運べるという仮定が成り立たないことを、離れた場所のマイクロホンによる盗聴実験で示した論文である。CipherFluteの「音の層に暗号学的な秘匿の力はまったく無い」という宣言は、この2010年の知見と完全に一致する。
  脅威理由: CipherFluteが脅威モデルの独自性として「音に秘匿を求めない」ことを掲げるなら、その論点は既に決着済みだと指摘されうるためである。引用して、寄与は秘匿の放棄そのものではなく秘密分散に全責任を移す設計にあると書き分ける必要がある。
- 【中】Acoustic integrity codes: secure device pairing using short-range acoustic communication
  著者: Florentin Putz, Flor Álvarez, Jiska Classen
  掲載: Proceedings of the 13th ACM Conference on Security and Privacy in Wireless and Mobile Networks (WiSec 2020), pp. 31-41, 2020年
  URL: https://doi.org/10.1145/3395351.3399420
  関係: 音響チャネルに秘匿性をいっさい期待せず、完全性だけを保証する符号を載せる設計であり、CipherFluteの立場ともっとも近い先行研究である。ただしCipherFluteが音の層に求めるのは完全性ですらなく誤り訂正による読み取りの頑健性だけであり、安全性はすべて秘密分散に委ねている。
  脅威理由: 音響チャネルを公開路として扱う立場そのものが既に確立していることを示す文献であり、これを引かないと「音に秘匿を求めない」という宣言が唐突に見える。
- 【中】Sound-Proof: Usable Two-Factor Authentication Based on Ambient Sound
  著者: Nikolaos Karapanos, Claudio Marforio, Claudio Soriente, Srdjan Capkun
  掲載: 24th USENIX Security Symposium (USENIX Security 2015), pp. 483-498, 2015年
  URL: https://www.usenix.org/conference/usenixsecurity15/technical-sessions/presentation/karapanos
  関係: 周囲の音の一致で近接を確かめる二要素認証の代表例である。音を共有された秘密に近いものとして扱うため、盗聴とリプレイが本質的な脅威になる。CipherFluteは音の共有秘密性を前提にしないので、リプレイも盗聴も脅威として定義されない。後続のListening Watch(WiSec 2018)とSound-based Two-factor Authentication: Vulnerabilities and Redesign(ACM TOPS 2024)がこの弱点を補っている。
  脅威理由: 音を認証要素として使う研究の代表例であり、CipherFluteの「音は公開チャネルである」という主張が既存の音響認証のどこに位置するかを説明するために引用が必須である。
- 【中】My Smartphone Knows What You Print: Exploring Smartphone-based Side-channel Attacks Against 3D Printers
  著者: Chen Song, Feng Lin, Zhongjie Ba, Kui Ren, Chi Zhou, Wenyao Xu
  掲載: Proceedings of the 2016 ACM SIGSAC Conference on Computer and Communications Security (CCS 2016), pp. 895-907, 2016年
  URL: https://doi.org/10.1145/2976749.2978300
  関係: 3Dプリンタのそばの携帯電話のマイクロホンと加速度センサだけで造形物の形状を復元できることを示した。CipherFluteの秘密は管長という形状そのものなので、印刷中に音響サイドチャネルで秘密が漏れる。独立研究としてAl Faruqueら(ICCPS 2016)、対策としてQuietPrint(CPSS 2026)がある。
  脅威理由: 新規性そのものを崩す研究ではないが、脅威モデルの記述に明らかな穴を作る。引用して「印刷環境も秘密の一部として扱う必要がある」と書かなければ査読で弱点を突かれる。
- 【中】Listen to Your Key: Towards Acoustics-based Physical Key Inference
  著者: Soundarya Ramesh, Harini Ramprasad, Jun Han
  掲載: Proceedings of the 21st International Workshop on Mobile Computing Systems and Applications (HotMobile 2020), pp. 3-8, 2020年
  URL: https://doi.org/10.1145/3376897.3377853
  関係: 物理鍵を錠に差し込む音から刻みの深さを推定して合鍵を作る攻撃(SpiKey)である。CipherFluteは「物体が音で秘密を明かす」ことを正規の手続きとして設計し、この論文は同じ現象を攻撃として示している。CipherFluteが物理層に秘匿を求めない立場の正しさを外側から補強する。
  脅威理由: 物体が発する音がその物体の秘密を明かすという構図が既に確立していることを示すため、脅威モデルの記述で必ず参照すべきである。目的も対象も異なるので新規性そのものは脅かさない。

### 調べ残した穴
今回はWeb検索の回数上限に達していたため、検索エンジンによる探索が使えず、CrossrefのAPI、DBLP、CiNii Research、学会の予稿集ページへの直接のアクセスだけで調べた。この制約から次の穴が残った。第一に、Semantic ScholarとOpenAlexが要求回数の制限で応答しなかったため、有力文献の被引用一覧をたどる芋づる式の探索がほとんどできなかった。特にMusipassとSound-Proofの被引用一覧は網羅性を上げるうえで見る価値が高い。第二に、SOUPSの予稿集を年ごとに直接あたれなかった。SOUPSは2015年から2018年まではUSENIX、2019年以降はACMが刊行しており刊行元をまたぐため一括の検索がしにくく、音を使う認証の使い勝手を測った研究がある可能性が残る。第三に、WISSとインタラクションの各年のプログラムページを直接あたれなかった。CiNiiはこの二つの会議を十分に索引していないため、会議のウェブサイトを年ごとに開く作業が要る。第四に、話者照合における「秘匿できない生体情報をどう鍵として扱うか」という膨大な議論を、ASVspoof 2017の共通課題論文一件を代表として押さえるにとどめた。第五に、音響サイドチャネルに対する規格上の対策について、TEMPEST関連の規格やISO/IEC 19790やFIPS 140-3が音響漏洩をどこまで扱っているかを確認できていない。第六に、特許文献をまったく見ていない。音を鍵にする認証は商用化の動機が強く、論文になっていない実装が特許として存在する可能性が高い。

==========================================================================================
## [13-makerworld-printable-whistles] モデル共有基盤における3Dプリントの笛と情報を埋め込んだモデル  (確認46 / 未検証12 / 訂正40 / 削除0)

### 要約
3Dプリントできる笛はモデル共有基盤において巨大かつ成熟したジャンルである。Printablesの「whistle」検索は1,150件が該当し、最上位のFlat Pocket Whistleは厚さ3mm、43×22mmで財布に入る平板型の笛でいいね12,926件、ダウンロード97,000件、実作報告2,965件に達する。したがって薄く小さくサポート材なしで平置き印刷でき確実に鳴るフィップル笛という工作技術それ自体は新規ではない。dp makesのWhistle Pan Fluteは長さの異なる笛を一列につないだ構成を明言しており、CipherFluteの物理形態に最も近い先行実装である。音高の設計についてもThreeD-Michaelが4.2kHzから23kHzまで周波数を明示した犬笛のシリーズを公開し、スマートフォンでの検証手順まで書いている。半音階パンフルートの作者は理論値どおりの管長では高音側が高すぎたので全管に2cm足したと記録しており、端補正を経験的に把握している。一方で笛の音高を符号として情報を運ぶモデルは4基盤に1件も無く、多音笛はすべて同時発音による音量最大化である。他方、暗号資産の復元情報を3Dプリント物に機械可読な符号として載せる系譜はすでに確立しており、QR SafeShareは秘密分散で分割したシェアを3MFとして印刷する道具であって脅威モデルの立て方がCipherFluteとほぼ同型である。SeedQRとその3Dプリント用テンプレートも同じ位置にある。CipherFluteの新規性は、読み出し経路が光学ではなく音であることと、日用品に偽装できることに絞られる。規模については、サイトマップから数えてMakerWorldが約233万件、Thingiverseが約225万件、Printablesが約138万件であり、2023年4月開設のMakerWorldが件数で首位に立っている。

### 脅威の大きい文献
- 【高】QR SafeShare – Split and protect secrets in QR codes（秘密をShamirの秘密分散で分割し各シェアを3Dプリント可能なQRコードとして書き出す道具）
  著者: Jurgen（GitHubのアカウント名は cmd1982）
  掲載: MakerWorld（2026年1月14日公開）、Printables（2026年7月26日更新）、qrsafeshare.com、GitHub
  URL: https://makerworld.com/en/models/2244875-qr-safeshare
  関係: CipherFluteの脅威モデルの骨格、すなわち安全性は秘密分散だけが担い物理層は走査コストを上げるだけという立て方を、この道具はすでに実装し文章でも明言している。運ぶ情報も同じ暗号資産の復元用フレーズである。異なるのは読み出し経路が光学的なQRコードである点だけである。
  脅威理由: CipherFluteの応用上の主張と脅威モデルの主張の両方が実物として先行している。作者自身が併設の覆いについて「素早い気づかれない走査を防ぎ不正アクセスに必要な労力を上げる」と書いており、探索コスト引き上げという論法まで一致する。
- 【高】SeedQRおよびCompactSeedQR仕様と、その3Dプリント用テンプレート（21x21 Modular QR-Code for Seedsigner）
  著者: SeedSignerプロジェクト（仕様）、happy（Printablesのモデル）
  掲載: SeedSignerリポジトリの仕様文書、Printablesのモデルは2024年3月18日更新
  URL: https://github.com/SeedSigner/seedsigner/tree/dev/docs/seed_qr
  関係: BIP39の復元用フレーズを最小の物理量で機械可読な符号として物理媒体に固定するという問題設定がCipherFluteと完全に一致する。索引を11ビットに直し末尾のチェックサムビットは導けるので省くという最適化も、CipherFluteの情報量設計と誤り訂正の設計と同じ土俵にある。
  脅威理由: CipherFluteの符号としての情報量設計と、復元用シードを物理媒体に載せる部分は、この確立した規格の前で新規性を主張しにくい。しかもCipherFluteの現在の先行研究一覧にSLIP-39とSSKRはあるがSeedQRが無く、明白な抜けになっている。
- 【中】Bitcoin binary seed storage. BIP39 12 words. / Bitcoin BitCard. Seed storage 1248 card size.
  著者: ErnestoFer
  掲載: Thingiverse、2024年10月28日
  URL: https://www.thingiverse.com/thing:6811428
  関係: クレジットカード大の3Dプリント板にBIP39の語を二進数や重み付き索引として穴で刻む。作者は目的を「暗号の層をもう一枚重ね、12語や24語が何を意味するか完全に分かっている者から保有者を守る」ことだと書き、樹脂なので金属探知機に反応しない点も挙げている。
  脅威理由: CipherFluteが物理層に負わせる「偽装によって探索コストを上げる」という論法と、カード形状の媒体という点が先行している。ただし読み出しは目視と手作業であり、音による能動的な読み出しは無い。
- 【中】Whistle Pan flute（長さの異なるフィップル笛を一列に融合したサポート材なしのモデル）
  著者: dp makes
  掲載: MakerWorld（2023年8月8日公開）、Printablesにも掲載
  URL: https://makerworld.com/en/models/13026-whistle-pan-flute
  関係: CipherFluteの物理形態、すなわち複数のフィップル笛を長さを変えて融合しサポート材なしで平置き印刷する一体物に最も近い先行実装である。作者自身が「長さの異なる笛をつないで一列にする」と明言している。両基盤合計で約10万ダウンロードに達する。
  脅威理由: CipherFluteが物理形態そのものを新規性として主張するならこの1件で大きく弱まる。ただし楽器であって符号のスロットとして読む設計は無く、作者も調律は継続中だと述べている。
- 【中】Flat Pocket Whistle（厚さ3mmで財布に入る平板型フィップル笛）
  著者: Jonas Daehnert（アカウント名 PhoneDesigner）
  掲載: Printables、2023年公開で最終更新2026年3月28日
  URL: https://www.printables.com/model/495173-flat-pocket-whistle
  関係: CipherFluteの発音体は厚さ4mm幅7mmであり、この平板型笛と同じ設計空間にある。上下の壁厚が0.6mmしかないので第一層の品質が決定的だという記述は、CipherFluteが実機で得た薄壁の造形限界の知見と一致する。
  脅威理由: いいね12,926件、ダウンロード97,000件、実作報告2,965件という規模で普及しているため、厚さ4mmの平板でサポートなしに鳴る笛を作ったという工作面の主張はほぼ新規性を主張できない。寄与を符号化側に置き直す必要がある。
- 【中】周波数を明示した犬笛のシリーズ（4.2kHzから23kHzまで）
  著者: ThreeD-Michael
  掲載: Printables（7kHz版は2024年3月17日更新）およびMakerWorld
  URL: https://www.printables.com/model/808031-dog-whistle-7-khz
  関係: 目標周波数を決めて笛を設計し印刷しスマートフォンのアプリで実測して確認するという作業ループが、すでにコミュニティの標準実践として成立していることを示す。Zシームが内部の狭い空気通路を塞ぐという指摘は、CipherFluteが遭遇する造形不良と同じ問題である。
  脅威理由: 印刷した笛の周波数を設計で狙えること自体は先行しているため、CipherFluteはスロット語彙、基準笛による正規化、誤り訂正という上位の設計に寄与を置く必要がある。
- 【中】TeleTunes Octo-Tune Major Flute/Whistle (F#)と3Dprintableflutes.comのカタログ
  著者: Tele Tunes
  掲載: MakerWorld、2024年5月22日
  URL: https://makerworld.com/en/models/471686-teletunes-octo-tune-major-flute-whistle-f
  関係: 指穴を造形板側にして平置きしサポートを一切使わないという印刷方針がCipherFluteと同じである。作者が「同じ機械、同じ設定、同じフィラメントでも複数回の印刷で異なる結果になりうる」と書いている点は、CipherFluteが基準笛による比読みを導入する動機を外部から裏づける。
  脅威理由: 音階が出る印刷笛の設計と、その調律の難しさに関する実務知識が先行している。CipherFluteは音高を設計できること自体ではなく、ばらつきを基準笛と誤り訂正で押さえ込んだことを寄与として立てる必要がある。
- 【中】半音階パンフルート群（Chromatic pan flute 7 Octave Customisableとその原典 Chromatic Tenor Panflute）
  著者: AskMe（リミックス）、Caran（原典）
  掲載: Printables 2023年4月8日更新（Musical Instrumentsコンテスト応募作）、Thingiverse原典は2015年11月14日
  URL: https://www.printables.com/model/442532-chromatic-pan-flute-7-octave-customisable
  関係: 作者が「管は正確にその音になるよう計算されていたが高い音では高すぎて下げられなかったので全部の管に2cm足して直した」と記録している。これはCipherFluteが f = A/(L+e) の e として定式化した端補正に対応する現象を、コミュニティが実測で把握した記録である。
  脅威理由: CipherFluteの f = A/(L+e) はこの経験知を素直に定式化しただけと見なされる余地がある。較正定数を実測で求め13スロットを100セント刻みで安全に分離できることを検証した点に寄与を絞るべきである。

### 調べ残した穴
MakerWorldとPrintablesのコメント欄および実作報告を読んでいないため、作者の説明文に現れない実測周波数や失敗条件の集合知を拾えていない。Flat Pocket Whistleの2,965件の実作報告とWhistle Magicの1,800件のリミックス、Flat Pocket Whistleの99件のリミックスのなかに音高制御や符号化に近い派生が混ざっている可能性を排除できていない。中国語での検索を行っておらず、MakerWorldは中国語圏の投稿が多いため「口哨」「哨子」「助记词」といった語では英語で引っかからないモデルが出る恐れがある。MakerWorldの媒介変数化モデル（Maker Lab／Customizer）の一覧を調べていないので、音名を選べる笛の生成器の有無が未確認である。Thingiverseの thing:2757112（Cryptocurrency-seed break card vault）と thing:3481293（Bitcoin seed coin、媒介変数化）は一覧でしか見ておらず、後者はシードを幾何形状に符号化している可能性があるため優先して確認すべきである。担当外だったMyMiniFactoryは、Thingiverseを買収した基盤であり有料モデルが多いため暗号資産保管の商業モデルが集まっている可能性がある。MakerWorldのabout ページがHTTP 403を返したため登録利用者数や累計ダウンロード数の公式値を取れておらず、Bambu Labの出荷台数や市場占有率も一次資料に当たれていない。QR SafeShareのGitHubの最初のコミット日が分かればCipherFluteとの時間的前後関係を正確に述べられるが、履歴を読んでいない。Printablesの「Musical Instruments」コンテストの応募385件を全件見ていないのも穴である。

==========================================================================================
## [14-fab-security-privacy] デジタルファブリケーションと安全・プライバシーの交差  (確認61 / 未検証5 / 訂正37 / 削除0)

### 要約
この領域には追加製造を対象とした情報セキュリティ研究が20年近く蓄積されており、ACM CCSには2021年と2022年に専用ワークショップ（AMSec）が置かれていた。研究は側チャネルによる形状復元、造形物の破壊攻撃、造形機と造形物の指紋認識、3次元モデルへの透かしと情報ハイディングの四系統に分かれる。CipherFluteに最も重大なのは第一系統である。Al Faruqueらは音だけから軸86パーセント・長さ誤差11.11パーセントで形状を復元し、2024年のJamaraniらは離れた携帯電話で軸98.80パーセント・平均傾向誤差4.47パーセントに到達した。CipherFluteは半音1段で実効長を約5パーセント変えるので、この誤差はスロットの粒度に並びつつある。Gatlinらの論文は表題が「暗号化は無意味である」であり、Dolgavinらは暗号化ファイルでも電力から設計を復元した。したがって「切り離して印刷する」という記述はデータ経路には正しいが放射経路には無効である。切り離し自体はDoらの遠隔搾取攻撃とMillerらの残留データ研究で強く裏づけられる。一方Chhetriらの「Tool of Spies」はスライサ汚染で漏洩率が最大39パーセント上がると示し、切り離しても道具連鎖が汚れていれば漏れると述べている。造形物に情報を隠す着想自体は海野浩らとGuptaらの系統で確立しているが、読み出し経路は光学・熱・X線・磁界に限られ、人が吹いて音で読むものは一つも見つからなかった。物理層の秘匿を意図的に放棄して秘密分散に委ねる設計も見当たらなかった。

### 脅威の大きい文献
- 【高】Practitioner Paper: Decoding Intellectual Property: Acoustic and Magnetic Side-channel Attack on a 3D Printer
  著者: Amirhossein Jamarani, Yazhou Tu, Xiali Hei
  掲載: EAI SmartSP 2024（プレプリントは arXiv:2411.10887, 2024年11月16日投稿）
  URL: https://arxiv.org/abs/2411.10887
  関係: 離れた場所に置いた市販の携帯電話の音響と磁界から造形機の動作を推定し、軸方向の平均精度98.80パーセント、平面的な設計で平均傾向誤差4.47パーセントを報告している。CipherFluteが半音1段に割り当てる実効長の変化は約5パーセントなので、隣接スロットの区別が付く水準に迫っている。攻撃者が復元した音列の誤りを、CipherFlute自身のReed-Solomon符号で訂正できてしまう危険もある。
  脅威理由: 新規性ではなく安全性の主張に効く。造形の瞬間だけは秘密が守られているという暗黙の前提を崩し、「切り離して印刷する」という推奨が放射経路を防げないことを数値で示してしまう。
- 【高】Side-Channel Attacks Bypass Protection in 3D Printers
  著者: Eric Yocam, Varghese Vaidyan, Micah Flack, Gurcan Comert, Judith L. Mwakalonge
  掲載: arXiv:2606.13952, 2026年6月11日投稿（査読の有無は未確認）
  URL: https://arxiv.org/abs/2606.13952
  関係: CipherFluteが実際に使っているBambu Lab社の造形機2台を対象に、能動的なモータ騒音打ち消し機構を評価した。音響チャネルは無作為の基準値8.33パーセントと区別が付かない水準まで潰れる一方、振動は残り、時系列モデルで約61パーセントの分類精度が出る。振動・磁界・電力は開いたままだと結論している。
  脅威理由: 使用機材そのものを扱った最新の評価であり、脅威モデルの記述の精度を大きく変える。音響は防げるが振動は防げないという具体的な結論が、論文の推奨文をそのまま書き換えることを要求する。
- 【高】Confidentiality Breach Through Acoustic Side-Channel in Cyber-Physical Additive Manufacturing Systems（会議版は Acoustic Side-Channel Attacks on Additive Manufacturing Systems, ICCPS 2016）
  著者: Sujit Rokka Chhetri, Arquimedes Canedo, Mohammad Abdullah Al Faruque
  掲載: ACM Transactions on Cyber-Physical Systems, 第2巻第1号, 論文番号3, 全25ページ, 2018年
  URL: https://doi.org/10.1145/3078622
  関係: 造形機の音だけから工具経路と形状を復元し、平均の軸推定精度86パーセント、平均の長さ推定誤差11.11パーセントを報告している。CipherFluteの秘密は管の長さそのものであり、この攻撃が復元しようとしている量と完全に一致する。ただし11.11パーセントは半音2段分に相当するので、2018年時点では個々のスロットまでは読めなかったと言える。
  脅威理由: この系統の起点であり被引用181件。ネットワークから切り離しても造形機は音を出し続けるので、論文の運用上の推奨が防げる範囲を明確に狭める。言及がないと不備と見られる。
- 【高】Tool of Spies: Leaking your IP by Altering the 3D Printer Compiler
  著者: Sujit Rokka Chhetri, Anomadarshi Barua, Sina Faezi, Francesco Regazzoni, Arquimedes Canedo, Mohammad Abdullah Al Faruque
  掲載: IEEE Transactions on Dependable and Secure Computing, 第18巻, 667-678ページ, 2021年
  URL: https://doi.org/10.1109/TDSC.2019.2923215
  関係: スライサ（造形コンパイラ）を密かに書き換えるだけで、音・電力・振動・電磁波の4つの側チャネルからの制御コード復元成功率が最大39パーセント上がる。CipherFluteはBambu Studio系のスライサと自作スクリプトを通しているので、そこが汚染されていれば切り離しても漏れる。
  脅威理由: 「切り離す」だけでは足りず「スライサとファームウェアの真正性を確かめる」まで推奨に含めることを要求する。運用上の推奨の書き換えを直接迫る指摘である。
- 【高】Encryption is Futile: Reconstructing 3D-Printed Models Using the Power Side-Channel
  著者: Jacob Gatlin, Sofia Belikovetsky, Yuval Elovici, Anthony Skjellum, Joshua Lubell, Paul Witherell, Mark Yampolskiy
  掲載: 24th International Symposium on Research in Attacks, Intrusions and Defenses (RAID) 2021, 135-147ページ
  URL: https://doi.org/10.1145/3471621.3471850
  関係: 消費電力の波形から造形物の形状を復元する攻撃であり、表題そのものが「暗号化は無意味である」と述べている。あわせて Dolgavin, Gatlin, Yung, Yampolskiy の arXiv:2509.18366（2025年）は産業機で真陽性率90.29パーセントを報告し、ファイルを暗号化しても復元できたと明言している。
  脅威理由: データ経路を守っても物理量が漏れると述べており、CipherFluteの推奨文と正面から衝突する。表題が強烈なので査読者が必ず思い出す種類の論文である。
- 【中】造形物の内部に情報を隠す一連の研究（内部空洞・金属混入・近赤外蛍光・強磁性セルとサーモグラフィやX線による読み出し）
  著者: 海野浩, 鈴木雅洋, ピヤラット シラパスパコォンウォン, 鳥井秀幸, 高嶋洋一 ほか
  掲載: VISAPP 2015, IWDW 2016, IEICE Transactions on Information and Systems 2017, Journal of Imaging Science and Technology 2019, IVSP 2023 など。日本語版は電子情報通信学会技術研究報告 114(117) 265-270 (2014) と情報処理学会研究報告CSEC 2014(40) 1-6
  URL: https://doi.org/10.1007/978-3-319-53465-7_27
  関係: 日用品に見える造形物の内部に外から見えない情報を隠し、専用の計測装置で読み出す枠組みを10年以上かけて確立している。CipherFluteの差分は、読み出しが人間の息と汎用マイクロフォンだけで済むこと、中身が権利者識別子ではなく高価値の秘密であること、秘匿を物理層に求めず秘密分散に負わせることの三点である。
  脅威理由: 着想の骨格が近く、日本国内の中心的な先行系統なので必ず引用して差分を述べる必要がある。ただし読み出し手段と目的が異なるので新規性が崩れるとは考えにくい。
- 【中】A Data Exfiltration and Remote Exploitation Attack on Consumer 3D Printers
  著者: Quang Do, Ben Martini, Kim-Kwang Raymond Choo
  掲載: IEEE Transactions on Information Forensics and Security, 第11巻第10号, 2174-2186ページ, 2016年
  URL: https://doi.org/10.1109/TIFS.2016.2578285
  関係: 家庭用造形機をネットワーク越しに遠隔から悪用し、造形に使われた設計データを外に持ち出す攻撃を示した。CipherFluteの「ネットワークから切り離した環境で印刷する」という推奨に対する最も直接的な裏づけであり、あわせてMillerらの残留データ論文（Computers & Security 75巻10-23ページ, 2018年）を引けば造形前・造形中・造形後の三局面を押さえられる。
  脅威理由: 新規性を脅かさず論文の主張を支える方向に働くが、切り離しの推奨が思いつきでなく既知の脅威に基づくことを示すために必ず引く必要がある。
- 【中】Never Trust the Manufacturer, Never Trust the Client: A Novel Method for Streaming STL Files for Secure Additive Manufacturing
  著者: Seyed Ali Ghazi Asgar, Narasimha Reddy, Satish T. S. Bukkapatnam
  掲載: arXiv:2507.06421, 2025年7月8日投稿, 同年7月11日改訂（査読の有無は未確認）
  URL: https://arxiv.org/abs/2507.06421
  関係: 設計者と受託製造者の双方が互いを信頼できない問題を、設計ファイルの分割逐次送信と受託側での実時間変換で解いている。CipherFluteの「家庭で作れるので製造者を信頼しなくてよい」という利点の主張に最も近い先行研究であり、受託製造では複雑な仕組みを要する問題を自家製造で回避しているという形で引き直せる。
  脅威理由: 新規性は脅かさず論拠として使えるが、家庭製造の利点を先行研究に基づいて論じるためには引用が必要である。表題の言い回しが論文の主張と正面から響き合う。

### 調べ残した穴
第一に、計算機トモグラフィやX線による無音の読み出しが半音1段の管長差（およそ2ミリメートル台）を分離できるかを文献で裏づけていない。Chenらの系統は計算機トモグラフィを正当な読み出し手段として使っているので、CipherFluteに対しては攻撃手段になるはずであり、脅威モデルに関わる重要な穴である。第二に、電磁波側チャネル単独の研究の書誌を押さえていない。第三に、米国国立標準技術研究所の報告書やASTM F42・ISO/ASTM 52920系の規格といった指針類を調べていないので、「切り離して印刷する」という推奨が業界の指針にどう書かれているかを確認できていない。GatlinらのRAID論文の共著者に同研究所の研究者が入っているので、そこから辿るのが早い。第四に、CHI・UIST・Symposium on Computational Fabrication・TEIを安全とプライバシーの観点で系統的に走査していないため、利用者の理解を扱う質的研究を取りこぼしている可能性がある。第五に、Bambu Lab社のクラウド機構が造形データをどう扱うかについての学術的分析を一つも見つけていない。実際に使っている機体の通信経路の話なので査読で問われうる。第六に、日本の法制度の側から3次元造形による複製をどう扱うかを調べていない。茂出木敏雄の「造形の入口で内容を照合する」系統が制度化された場合、形状に意味を載せる手法一般に影響しうる。第七に、特許文献を一切調べていない。造形物への情報埋め込みは海野浩らの系統を含めて出願がある可能性が高い。なお指定された出力パスに文字列 undefined がディレクトリ名として入っていたため、指定どおりの場所に書いたうえで、他の切り口のファイルが並ぶ related_work_survey/raw/14-fab-security-privacy.md にも同じ内容を複製した。