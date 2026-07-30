# 造形物への情報埋め込み（光学読み取り）

本稿は CipherFlute の関連研究調査のうち、「デジタルファブリケーションで作った物体の内部や表面に情報を埋め込み、撮像装置で読み出す」という切り口を担当したものである。読み出しの原理は光学に限定せず、赤外線、蛍光、熱、テラヘルツ、X線、電波、磁気、生体分子まで含めて洗い出した。書誌情報は原則としてdblp、Crossref、OpenAlex、arXiv、出版社ページ、著者・研究室の公式ページ、J-STAGE、CiNii Research、Europe PMC、PubMed、WISS予稿集ページのいずれかを直接取得して確認し、確認先のURLを各項目に記した。2026年7月30日に別の担当者が全項目を独立に再検証しており、その経緯は末尾の「検証の記録」に書いた。

## この切り口の要約

この分野は2013年の InfraStructs 以降、十年以上にわたって連続的に積み上げられており、CipherFlute が「日用品に符号を埋め込む」と主張する部分については、光学系の先行研究が圧倒的に厚い。到達点を数字で押さえると次のようになる。AirCode は2センチメートル角の埋め込みタグに約106ビット、5センチメートル角に約500ビットを収め、しかもリードソロモン符号で40パーセントの冗長度を与えている。InfraredTags は赤外線を透過するフィラメントと内部空隙で21×21のQRコードを物体内部に丸ごと隠し、外見はまったく変わらない。AnisoTag はクレジットカードと同じ寸法の面に51ビット、RGBカメラと画像処理を併用する構成なら160ビットを刻み、読み取り装置は10ドル程度で作れる。上平員丈らの一連の研究は、数センチメートルの造形物の内部に空洞や近赤外蛍光染料や強磁性セルを作り込み、X線、サーモグラフィ、近赤外線で数百ビットを非破壊で読み出す方法を2015年から継続的に発表している。したがって「消費者向けFDMプリンタで日用品に情報を仕込み、電子部品も電源も使わずに読み出す」という枠組み自体は、まったく新しくない。

一方で、この分野の全論文に共通する空白がはっきり見えた。第一に、脅威モデルを明示した研究がほぼ皆無である。AirCode、InfraredTags、LayerCode、G-ID、AnisoTag のいずれも、攻撃者が誰で、何を守り、何を守らないのかを書いていない。唯一の例外は2024年の Secure Information Embedding in Forensic 3D Fingerprinting で、これは破断と隠匿を行う敵を明示して符号理論で対処している。第二に、読み出しに所有者の身体的な行為を要する設計が存在しない。光学系はすべて、物体を撮像装置の前に置きさえすれば所有者の関与なく読める。第三に、秘密分散や暗号資産のリカバリーシードの保管を目的として設計された造形タグは見つからなかった。第四に、基準素子を同一物体に混ぜて環境変動を正規化する設計も、隣接シンボルの同値禁止のような遷移保証も、造形タグの文脈では見当たらなかった。CipherFlute の新規性は、埋め込みという行為そのものではなく、この四点に置くのが正確である。

## 新規性への脅威が大きい文献

### 1. InfraredTags: Embedding Invisible AR Markers and Barcodes Using Low-Cost, Infrared-Based 3D Printing and Imaging Tools

- 著者: Mustafa Doga Dogan, Ahmad Taka, Michael Lu, Yunyi Zhu, Akshat Kumar, Aakar Gupta, Stefanie Mueller
- 発表: CHI 2022, pages 269:1-269:12, DOI 10.1145/3491102.3501951
- 確認先: https://dblp.org/search/publ/api?q=InfraredTags&format=json （書誌）、https://ar5iv.labs.arxiv.org/html/2202.06165 （本文）

赤外線を透過する市販フィラメントで物体本体を印刷し、内部に空隙を作ることでタグのビットを表現する。可視光では完全に不透明な普通の物体に見えるが、近赤外線カメラで撮ると内部の空隙が輝度差として現れ、QRコードやArUcoマーカーが読める。本文で用いているのは21×21のQRコード（数字なら25文字まで）と4×4のArUcoマーカーである。読み取り装置は Raspberry Pi NoIR カメラ、940ナノメートルの赤外線LEDを2個、可視光カットフィルタ、Raspberry Pi Zero を組み合わせた132グラムのモジュールで、TPUのケースでスマートフォンに取り付ける（ケースは柔らかいTPUで刷り、撮像モジュール本体は硬いPLAで刷って差し込む）。照明については、多材料で印刷した符号なら0.2ルクス、単一材料で印刷した符号なら1.1ルクスの微弱な赤外照明で検出でき、250センチメートル離れても読める。

CipherFlute との関係は正面衝突である。消費者向けFDMプリンタで、追加の電子部品も電源も使わず、日用品の外見をまったく損なわずに機械可読な情報を埋め込むという枠組みが完全に一致する。しかも情報量は笛40本から49本ぶんの128ビットを大きく上回り、体積あたりの密度も比較にならない。差分として主張できるのは、赤外線を透過する特殊なフィラメントを必要としない点、追加の撮像モジュールを必要としない点、読み出しが所有者の身体的な行為（吹くこと）と結びついている点の三つに限られる。

脅威の度合いは高である。「日用品に隠して埋め込み、消費者向け機材で読む」という主張のうち、隠蔽性と容量の両面で CipherFlute より優れた手段がすでに存在するため、論文はこの研究との差分を数字で書かないと立たない。

### 2. 上平員丈・鈴木雅洋らによる造形物内部への情報埋め込みの一連の研究

代表的な文献を五つ挙げる。いずれも書誌情報を一次資料で確認した。

- Masahiro Suzuki, Pailin Dechrueng, Soravit Techavichian, Piyarat Silapasuphakornwong, Hideyuki Torii, Kazutake Uehira, "Embedding Information into Objects Fabricated With 3-D Printers by Forming Fine Cavities inside Them", IS&T International Symposium on Electronic Imaging: Media Watermarking, Security, and Forensics, vol. 29, no. 7, pp. 6-9, 2017, DOI 10.2352/ISSN.2470-1173.2017.7.MWSF-317
  確認先: https://library.imaging.org/ei/articles/29/7/art00002 （出版社の論文ページで題名・著者6名・巻号・頁・抄録を確認した）
- Kazutake Uehira, Masahiro Suzuki, Piyarat Silapasuphakornwong, Hideyuki Torii, Youichi Takashima, "Copyright Protection for 3D Printing by Embedding Information Inside 3D-Printed Objects", International Workshop on Digital Watermarking (IWDW) 2016, Lecture Notes in Computer Science, vol. 10082, pp. 370-378, Springer, 2017, DOI 10.1007/978-3-319-53465-7_27
  確認先: https://link.springer.com/chapter/10.1007/978-3-319-53465-7_27 （出版社ページでLNCSの巻号10082と頁370-378を確認した）
- Hideo Kasuga, Piyarat Silapasuphakornwong, Hideyuki Torii, Masahiro Suzuki, Kazutake Uehira, "Technique to Embed Information in 3D Printed Objects Using Near Infrared Fluorescent Dye", IIEEJ Transactions on Image Electronics and Visual Computing, vol. 8, no. 1, pp. 2-9, 2020, DOI 10.11371/tievciieej.8.1_2
  確認先: https://www.jstage.jst.go.jp/article/tievciieej/8/1/8_2/_article （J-STAGEで題名・著者5名・巻号・頁・抄録を確認した）
- Piyarat Silapasuphakornwong, Hideyuki Torii, Kazutake Uehira, Apisara Funsian, Kewalee Asawapithulsert, Tattawat Sermpong, "Embedding Information in 3D Printed Objects Using Double Layered near Infrared Fluorescent Dye", International Journal of Materials, Mechanics and Manufacturing, vol. 7, no. 6, pp. 230-234, 2019, DOI 10.18178/ijmmm.2019.7.6.465
  確認先: https://api.crossref.org/works/10.18178/ijmmm.2019.7.6.465 （Crossrefに出版社が登録した書誌で著者6名・巻号・頁・年を確認した。上のIIEEJ論文と同じ二層構成の手法を扱っている）
- Masahiro Suzuki, Piyarat Silapasuphakornwong, Youichi Takashima, Hideyuki Torii, Kazutake Uehira, "Number of Detectable Gradations in X-Ray Photographs of Cavities Inside 3-D Printed Objects", IEICE Transactions on Information and Systems, vol. E100.D, no. 6, pp. 1364-1367, 2017, DOI 10.1587/transinf.2016EDL8213
  確認先: https://api.crossref.org/works/10.1587/transinf.2016EDL8213 （Crossrefで題名・著者5名・巻号・頁を確認した。内部空洞をX線で読むときに識別できる階調数を扱った短報である）

この研究群は、造形中に物体内部へ微小な空洞、高反射率の突起、近赤外蛍光染料の層、金属混入樹脂、強磁性フィラメントのセルなどを作り込み、X線撮影、サーモグラフィ、近赤外線の透過像や反射像、磁力計で非破壊に読み出す。Electronic Imaging 2017の論文は抄録で、数センチメートルの大きさの造形物であれば著作権情報として十分な量、すなわち数百ビットを埋め込めると明記している。IIEEJ論文では蛍光染料の層を二つの深さに作り分けて4状態を作り、深層学習で判別することで情報量を倍にしている。2021年の IS&T Printing for Fabrication（NIP37）では強磁性セルを再着磁して書き換え可能にした（Piyarat Silapasuphakornwong, Hideyuki Torii, Masahiro Suzuki, Kazutake Uehira, "Effects of Embedded Depth of Internal Printed Ferromagnetic Cell on Data Clarity of Rewritable 3D Objects", NIP & Digital Fabrication Conference, vol. 37, pp. 28-31, 2021, DOI 10.2352/ISSN.2169-4451.2021.37.28、確認先 https://library.imaging.org/admin/apis/public/api/ist/website/downloadArticle/print4fab/37/1/art00004_1 で本文PDFの取得を確認し、巻号と頁は https://api.crossref.org/works/10.2352/ISSN.2169-4451.2021.37.28 で確認した）。金属混入樹脂とサーモグラフィの組み合わせは Piyarat Silapasuphakornwong, Chaiwuth Sithiwichankit, Kazutake Uehira, "Information Embedding in 3D Printed Objects Using Metal-Infused PLA and Reading with Thermography", NIP & Digital Fabrication Conference, vol. 34, pp. 202-207, 2018, DOI 10.2352/issn.2169-4451.2018.34.202 にある（確認先 https://api.crossref.org/works/10.2352/issn.2169-4451.2018.34.202 ）。この系列の起点が2015年であることは Masahiro Suzuki, Piyarat Silapasuphakornwong, Kazutake Uehira, Hiroshi Unno, Youichi Takashima, "Copyright Protection for 3D Printing by Embedding Information Inside Real Fabricated Objects", VISAPP 2015, pp. 180-185, DOI 10.5220/0005342401800185 で確認した（確認先 https://dblp.org/rec/conf/visapp/SuzukiSUUT15 ）。日本語の技術報告も多数あり、中村耕介・鈴木雅洋・高嶋洋一・鳥井秀幸・上平員丈「内壁の構造化による3Dプリンター造形物への情報埋め込み技術」電子情報通信学会技術研究報告、第116巻第132号、19頁、2016年7月が確認できる（確認先 https://cir.nii.ac.jp/crid/1520009407351160576 で著者5名・誌名・巻号・頁・年月を確認した）。

CipherFlute との関係は、内部構造で情報を担わせるという発想の直接の先行研究にあたる。CipherFlute の笛は内部の空洞（管）の長さで符号を表すが、これは「内部に空洞を作って情報を表す」という上平らの枠組みの一変種と読める。読み出しの物理が撮像ではなく共鳴音である点だけが異なる。

脅威の度合いは高である。造形物内部の空洞に数百ビットを入れて非破壊で読むという主張が2015年からすでに確立しており、しかも著作権保護という安全性寄りの動機まで持っている。CipherFlute はこの研究群を引用したうえで、「読み出しに専用撮像装置ではなく人間の息とマイクを使う」ことがなぜ意味を持つのかを説明しなければならない。

### 3. AnisoTag: 3D Printed Tag on 2D Surface via Reflection Anisotropy

- 著者: Zehua Ma, Hang Zhou, Weiming Zhang
- 発表: CHI 2023, pages 420:1-420:15, DOI 10.1145/3544548.3581024
- 確認先: https://api.crossref.org/works/10.1145/3544548.3581024 （出版社が登録した書誌）、https://dblp.org/search/publ/api?q=AnisoTag&format=json （論文番号420。dblpの検索APIは混雑時にHTTP 500を返すことがある）、https://ar5iv.labs.arxiv.org/html/2301.10599 （本文の数値）

3Dプリンタが作る表面微細構造の異方性反射を使い、平滑な円筒状の微細くぼみの角度で情報を符号化する。コリメートしたレーザーを当てると、くぼみの角度に応じて異なる照明パターンが反射する。既定の構成では53.98ミリメートル×85.6ミリメートル、つまりクレジットカードと同じ面に水平方向17区画×3ビットで51ビットを収める。RGBカメラと画像処理を併用する構成では160ビットまで伸びる（本文6.2節）。読み取り装置は3ドルのクラスIIIAレーザーポインタ、半径1.5センチメートルの円周上に並べた16個のフォトレジスタ、7ドルのSTM32F103マイクロコントローラで構成され、カメラを必要としない。

CipherFlute との関係は、カード型実装との形状の一致が痛い。CipherFlute はクレジットカード大のカードに笛を並べる実装を持つが、同じ面積に AnisoTag は51ビットから160ビットを、外見をほとんど変えずに、10ドル程度の装置で読める形で刻む。CipherFlute のカード1枚あたりのビット数と直接比較される。

脅威の度合いは中である。CipherFlute の主要な主張を壊しはしないが、カード型の実装を「情報を運ぶ媒体」として提示するときには必ず比較対象になる。差分は、AnisoTag が専用の読み取り治具を要するのに対し CipherFlute は口とマイクだけで済む点、および AnisoTag が表面のみで内部を使わない点である。

### 4. BrightMarker: 3D Printed Fluorescent Markers for Object Tracking

- 著者: Mustafa Doga Dogan, Raul Garcia-Martin, Patrick William Haertel, Jamison John O'Keefe, Ahmad Taka, Akarsh Aurora, Raul Sanchez-Reillo, Stefanie Mueller
- 発表: UIST 2023, pages 55:1-55:13, DOI 10.1145/3586183.3606758
- 確認先: https://api.crossref.org/works/10.1145/3586183.3606758 （出版社が登録した書誌）、https://dblp.org/search/publ/api?q=BrightMarker&format=json （論文番号55。dblpの検索APIは混雑時にHTTP 500を返すことがある）、https://hcie.csail.mit.edu/research/brightmarker/brightmarker.html （著者順と本文の数値）

赤外蛍光フィラメントを使い、入射光の波長をずらして返す性質でマーカーを物体内部に埋め込む。赤外カメラ側で長波長透過フィルタによりマーカー以外の要素を落とすため、物体表面の色にかかわらず高いコントラストで追跡できる。1インチ角の小さなマーカーでも2メートル以上離れて追跡でき、既存の不可視マーキング手法を検出率で上回ると主張している（プロジェクトページ本文に「even small markers (1"x1") can be tracked at distances exceeding 2m」とある。速度実験では InfraredTags の平均検出率60.73パーセントに対して BrightMarker が上回ったと報告している）。既存の携帯端末やAR・VRヘッドセットに取り付けるハードウェアモジュールを作っている。

CipherFlute との関係は、InfraredTags の後継として「日用品に見えない印を埋める」路線の最新到達点にあたる。CipherFlute が「見えない情報を日用品に入れる」ことの価値を論じるとき、この系列の到達点を無視できない。

脅威の度合いは中である。主眼が追跡であって少量の秘密情報の保管ではないため主張は直接ぶつからないが、隠蔽性の水準を示す基準として必ず引用して差分を述べる必要がある。

### 5. 3D printing wireless connected objects

- 著者: Vikram Iyer, Justin Chan, Shyamnath Gollakota
- 発表: ACM Transactions on Graphics, vol. 36, no. 6, pages 242:1-242:13, 2017（SIGGRAPH Asia 2017）, DOI 10.1145/3130800.3130822
- 確認先: https://api.crossref.org/works/10.1145/3130800.3130822 （出版社が登録した書誌。第36巻第6号）、https://dblp.org/search/publ/api?q=wireless+connected+objects+Gollakota&format=json （論文番号242。dblpの検索APIは混雑時にHTTP 503を返すことがある）、https://printedwifi.cs.washington.edu/ （手法の記述。プロジェクトページは第三著者を Shyam Gollakota と略記しているが、出版社の書誌は Shyamnath Gollakota である）

電池も電子部品も使わず、市販の3Dプリンタと市販のフィラメントだけで無線通信するオブジェクトを作る研究である。バックスキャッタでWi-Fi受信機に直接データを送る機構に加えて、鉄粉入りフィラメントを使って磁界の形で物体内部にデータを埋め込み、市販スマートフォンの磁力計で復号する仕組みを含んでいる。眼鏡フレームや腕輪に磁気データを埋めた例が示されている。後続の Wireless Analytics for 3D Printed Objects（Vikram Iyer, Justin Chan, Ian Culhane, Jennifer Mankoff, Shyam Gollakota, UIST 2018、確認先 https://printedanalytics.cs.washington.edu/ ）では、ラチェットと歯車で通信圏外の事象を記録して後から読み出す機構まで作っている。

CipherFlute との関係は、「電子部品も電源も持たない印刷物体に情報を仕込み、追加装置なしの市販スマートフォンで読み出す」という主張が完全に一致する点にある。CipherFlute はマイクを使い、この研究は磁力計を使うという違いしかない。しかも磁気の読み出しは所有者の身体的な行為を必要としない。

脅威の度合いは中である。CipherFlute の「電源不要・電子部品不要・市販端末で読める」という主張は、この研究が2017年にすでに達成している。差分として言えるのは、特殊な鉄粉入りフィラメントを必要としない点と、埋め込んだ笛が物体の意匠に溶け込む点である。

### 6. InfoPrint: Embedding Interactive Information in 3D Prints Using Low-Cost Readily-Available Printers and Materials

- 著者: Weiwei Jiang, Chaofan Wang, Zhanna Sarsenbayeva, Andrew Irlitti, Jing Wei, Jarrod Knibbe, Tilman Dingler, Jorge Goncalves, Vassilis Kostakos
- 発表: Proceedings of the ACM on Interactive, Mobile, Wearable and Ubiquitous Technologies (IMWUT), vol. 7, no. 3, pages 102:1-102:29, 2023, DOI 10.1145/3610933
- 確認先: https://dblp.org/search/publ/api?q=InfoPrint+Embedding+Interactive+Information&format=json （書誌と論文番号102）、抄録は https://api.openalex.org/works/doi:10.1145/3610933 で確認した

安価な市販のデュアルエクストルーダFDMプリンタと一般的なPLAだけを使い、材料の熱特性の違いで情報を物体内部に埋め込む。物体に触れて温度を移したあと、サーマルカメラ付きスマートフォンで撮ると隠された情報が現れる。近赤外撮像への一般化も示している。物体に触るという人間の行為が読み出しの引き金になる点が特徴である。

CipherFlute との関係は、「人間の行為（触る）を経て初めて情報が現れる」という設計思想が、CipherFlute の「吹く」に最も近い先行例である点にある。ただし触れるだけで読めるので、所有者でなくても読める。

脅威の度合いは中である。特殊材料を使わず市販の一般材料だけで日用品に情報を隠す点、および人間の行為を読み出しに組み込む点の二つで先行しているため、CipherFlute の「材料を選ばない」「行為が読み出しの一部」という論点は差分を丁寧に書く必要がある。

### 7. 内部構造パターンの差異を利用した3Dプリントオブジェクト識別手法

- 著者: 久保勇貴、江口佳那、青木良輔、近藤重邦、東正造、犬童拓也（日本電信電話株式会社）
- 発表: WISS 2019（インタラクティブシステムとソフトウェアに関するワークショップ）、口頭発表8
- 確認先: https://www.wiss.org/WISS2019Proceedings/ （題名と著者6名、所属がNTTであること）、本文PDF https://www.wiss.org/WISS2019Proceedings/oral/8.pdf 、査読コメント https://www.wiss.org/WISS2019Proceedings/oral/8.html

提案手法には FabAuth という名前が付いている。スライサの標準機能である内部充填パターンの設定を変えることで、外見が同一の3Dプリント造形物に固有の振動特性を割り当て、その違いから識別する。読み出しはアクティブ音響センシングによる音響周波数応答の解析であり、加振と受振にピエゾ素子を使い、機械学習で判別する。予稿の概要は「平均識別精度99.3%にて8つのオブジェクトを識別できることを確認した」と述べている。査読コメントでは、実用的な用途が不明である点、ピエゾ素子の設置位置の許容範囲が狭い点、識別できる個体数の増加に対する拡張性が不明である点が指摘されている。さらに、権利保護のためにタグを付けたいという動機と、誰でも同じ設定で複製できる充填パターンをタグに使うことのあいだに矛盾があるのではないかという指摘もある。

CipherFlute との関係は二重に危険である。第一に、投稿先である WISS に「3Dプリント造形物の内部構造に情報を持たせ、振動という力学的・音響的な現象で読み出す」という論文がすでに存在する。第二に、著者らが日本の同一コミュニティに属するため、査読者が想起する可能性が高い。ただし識別できるのは少数のクラスであって、ビット列の格納ではない。

脅威の度合いは中である。CipherFlute のビット容量と誤り訂正、日用品への偽装という論点は残るが、「内部構造に情報を持たせて非光学的に読む」という着想の先行例として必ず引用し、識別と情報格納の違いを明確に述べる必要がある。

### 8. Secure Information Embedding in Forensic 3D Fingerprinting

- 著者: Canran Wang, Jinwen Wang, Mi Zhou, Vinh Pham, Senyue Hao, Chao Zhou, Ning Zhang, Netanel Raviv
- 発表: arXiv preprint arXiv:2403.04918, 2024年3月7日投稿（第5版が2025年2月3日）
- 確認先: https://arxiv.org/abs/2403.04918 （題名・著者8名・投稿日と改訂日・抄録を確認した。査読付き会議や雑誌に採録された記録は見つからず、現時点ではプレプリントである）

提案手法には SIDE（Secure Information Embedding and Extraction）という名前が付いている。3Dプリント造形物に法科学的な指紋情報を埋め込む枠組みで、敵が造形物を破断して一部の断片を隠すという明示的な脅威モデルを置き、断片化と欠損に耐える符号理論的な埋め込みを設計している。さらに埋め込み処理そのものを Trusted Execution Environment で保護する。動機は、消費者向け3Dプリンタによる追跡不能な偽造品や銃器の製造を防ぐことにある。

CipherFlute との関係は、造形物への情報埋め込みに明示的な攻撃者モデルと符号理論を持ち込んだ数少ない例である点にある。CipherFlute が「この分野で脅威モデルを明示したのは我々が初めてである」と書くと、この研究に反証される。

脅威の度合いは中である。目的が正反対（こちらは所有者に無断で追跡するための埋め込み、CipherFlute は所有者のための秘密保管）なので主張は衝突しないが、「脅威モデルの明示」という新規性の言い方は必ず調整が必要である。

### 9. すでに把握している六件についての追加の数値

論文が既に挙げている六件についても、差分を数字で書くために必要な情報を一次資料から取り直した。

- InfraStructs（Karl D. D. Willis, Andrew D. Wilson, ACM Transactions on Graphics, vol. 32, no. 4, pp. 138:1-138:10, 2013, DOI 10.1145/2461912.2461936、確認先 https://www.microsoft.com/en-us/research/publication/infrastructs-fabricating-information-inside-physical-objects-imaging-terahertz-region/ および本文PDF https://www.microsoft.com/en-us/research/wp-content/uploads/2016/10/WillisSiggraph2013.pdf ）。単純な一次元タグで8ビット、行列型タグで27ビットを実証している。行列型タグは3×3×3の立体格子であり、レーザーカットしたポリスチレンの層を3Dプリントしたケースに収めて作っている。読み出しには Picometrix T-Ray 4000 というテラヘルツ時間領域分光装置が要り、走査速度が毎秒約100画素なので100×100画素の走査に約2分かかる。リードソロモン符号は将来課題として言及されるにとどまる。認証や偽造防止に触れるが、攻撃者モデルは書いていない。
- AirCode（Dingzeyu Li, Avinash S. Nair, Shree K. Nayar, Changxi Zheng, UIST 2017, pp. 449-460, DOI 10.1145/3126594.3126635、確認先 https://arxiv.org/abs/1707.05754 および本文PDF https://www.cs.columbia.edu/cg/aircode/aircode-uist-2017-li-et-al.pdf ）。2センチメートル角で約106ビット、5センチメートル角で500ビット超。読み出しにはプロジェクタとカメラ、偏光板を使った直接成分と大域成分の分離が必要で、撮像に3分から4分かかる。重要なのは、リードソロモン符号で40パーセントの冗長度を与えている点である。つまり「造形タグにリードソロモン符号を使う」こと自体はすでに先行例がある。安全性や攻撃者の議論はない。
- LayerCode（Henrique Teles Maia, Dingzeyu Li, Yuan Yang, Changxi Zheng, ACM Transactions on Graphics, vol. 38, no. 4, pp. 112:1-112:14, 2019, DOI 10.1145/3306346.3322960、確認先 https://dblp.org/search/publ/api?q=LayerCode&format=json および本文PDF https://www.cs.columbia.edu/cg/layercode/LayerCode_Maia_et_al_2019_lowRez.pdf ）。24ビットの符号を用い、近赤外の変種では12ビットである。読み出しは普通のカメラで、近赤外の変種でも近赤外フィルタと光源（テレビのリモコンで足りる）を足すだけでよい。二つの連続する層の厚さの比で1を表し、比が1のときに0を表すという設計で、印刷方向や曲率に対して不変になっている。誤り訂正は「任意の符号を載せられるが本実験では純粋な性能を見るためあえて付けない」と明記している。
- G-ID（Mustafa Doga Dogan, Faraz Faruqi, Andrew Day Churchill, Kenneth Friedman, Leon Cheng, Sriram Subramanian, Stefanie Mueller, CHI 2020, pp. 1-13, DOI 10.1145/3313831.3376202、確認先 https://dblp.org/search/publ/api?q=G-ID+Identifying+3D+Prints&format=json および本文PDF https://groups.csail.mit.edu/hcie/files/research-projects/G-ID/2020-CHI-GID-paper.pdf ）。カメラのみで204通り、光源を併用して17,136通り、すなわち約7.7ビットから約14ビットに相当する。読み取りは市販スマートフォンのカメラだけで足り、内部の充填を見る場合にのみ小型懐中電灯（Nitecore Tini）を造形物の側面に当てる。偽造対策の応用例には触れるが、攻撃者モデルはない。
- StructCode（Mustafa Doga Dogan, Vivian Hsinyueh Chan, Richard Qi, Grace Tang, Thijs Roumen, Stefanie Mueller, SCF 2023, pp. 6:1-6:13, DOI 10.1145/3623263.3623353、確認先 https://api.crossref.org/works/10.1145/3623263.3623353 およびプロジェクトページ https://hcie.csail.mit.edu/research/structcode/structcode.html ）。レーザーカットの指型継手で3値符号により約12文字、リビングヒンジで最大21文字を格納する。読み出しは携帯端末やヘッドセットのRGBカメラで足りる（この点は同じ著者の博士論文 arXiv:2407.11748 に「StructCode only requires a conventional RGB camera for detection, and thus can be used on off-the-shelf mobile devices and headsets」とある）。プロジェクトページには「最も機微なタグでは符号とラベルの対応を暗号化してその利用者だけが持てばよい」という一文があり、秘匿を暗号に負わせる発想が既に述べられている点は注意を要する。
- Seedmarkers（Christopher Getschmann, Florian Echtler, TEI 2021, pp. 26:1-26:11, DOI 10.1145/3430524.3440645、確認先 https://dblp.org/search/publ/api?q=Seedmarkers&format=json ）。重み付きボロノイ図で位相的な最適化を行い、任意形状の面に埋め込める形状非依存の位相マーカーを生成する。読み出しは普通のカメラで、3自由度または6自由度の追跡に対応する。

## 背景として押さえるべき文献

以下は脅威の度合いが低く、背景として引用すれば足りるものである。

- Muhammad Usama, Ulas Yaman, "Embedding Information into or onto Additively Manufactured Parts: A Review of QR Codes, Steganography and Watermarking Methods", Materials, vol. 15, no. 7, article 2596, 2022, DOI 10.3390/ma15072596。確認先 https://pmc.ncbi.nlm.nih.gov/articles/PMC9000573/ 。この分野をQRコード、電子透かしと著作権保護、ステガノグラフィ、その他の手法の四つに分類した総説であり（本文の節見出しで確認した）、読み出しにカメラ、赤外サーモグラフィ、X線撮影、X線蛍光、マイクロCTが使われることを整理している。表には情報密度の欄があり、上平グループの Suzuki らが2017年に示した高反射率の投影を埋め込む手法について1平方センチメートルあたり6.25ビットという数字を挙げている。この6.25ビットは分野全体の代表値ではなく特定手法の実測値であるから、引用するときは手法名を添える必要がある。関連研究節の見取り図として引用する価値が高い。なお本文に「超音波」による読み出しの記述は見当たらず、テラヘルツは InfraStructs を引用する形でしか現れないため、当初の記述からこの二つを外した。
- Karl Willis, Eric Brockmeyer, Scott Hudson, Ivan Poupyrev, "Printed Optics: 3D Printing of Embedded Optical Elements for Interactive Devices", UIST 2012, DOI 10.1145/2380116.2380190。確認先 https://api.crossref.org/works/10.1145/2380116.2380190 。造形物の中に導光路や光学素子を作り込む研究で、内部構造に機能を持たせる系譜の起点にあたる。
- Jiani Zeng, Honghao Deng, Yunyi Zhu, Michael Wessely, Axel Kilian, Stefanie Mueller, "Lenticular Objects: 3D Printed Objects with Lenticular Lens Surfaces That Can Change their Appearance Depending on the Viewpoint", UIST 2021, DOI 10.1145/3472749.3474815。確認先 https://api.crossref.org/works/10.1145/3472749.3474815 。視点によって見え方が変わる造形物であり、特定の条件でのみ情報が現れるという意味で隠蔽性の議論に使える。
- Omid Ettehadi, Fraser Anderson, Adam R. Tindale, Sowmya Somanath, "Documented: Embedding Information onto and Retrieving Information from 3D Printed Objects", CHI 2021, pages 424:1-424:11, DOI 10.1145/3411764.3445551。確認先 https://api.crossref.org/works/10.1145/3411764.3445551 （出版社が登録した書誌）および https://dblp.org/search/publ/api?q=Documented+Embedding+Information+onto+Retrieving+3D+Printed&format=json （論文番号424。dblpの検索APIは混雑時にHTTP 500を返すことがある）。3Dプリント造形物に制作の記録を紐づけ、モバイル拡張現実で取り出す研究である。
- Martin Feick, Xuxin Tang, Raul Garcia-Martin, Alexandru Luchianov, Roderick Wei Xiao Huang, Chang Xiao, Alexa Siu, Mustafa Doga Dogan, "Imprinto: Enhancing Infrared Inkjet Watermarking for Human and Machine Perception", CHI 2025, pages 447:1-447:18, DOI 10.1145/3706598.3713286。確認先 https://arxiv.org/abs/2502.17089 および https://dblp.org/search/publ/api?q=Imprinto+Infrared+Inkjet+Watermarking&format=json 。赤外線吸収インクで紙や物体に不可視の情報を刷り込み、赤外センサを備えた携帯端末で読む。ただし読み取りには近赤外センサと850ナノメートルのLEDを載せた自作モジュールをUSB-Cで端末に接続する必要があり、素のスマートフォンだけでは読めない。造形物ではないが、日用品に不可視の情報を載せる路線の最新例である。
- Arnaud Delmotte, Kenichiro Tanaka, Hiroyuki Kubo, Takuya Funatomi, Yasuhiro Mukaigawa, "Blind Watermarking for 3-D Printed Objects by Locally Modifying Layer Thickness", IEEE Transactions on Multimedia, vol. 22, no. 11, pp. 2780-2791, 2020, DOI 10.1109/TMM.2019.2962306。確認先 https://api.crossref.org/works/10.1109/TMM.2019.2962306 および奈良先端科学技術大学院大学のプレスリリース https://www.naist.jp/pressrelease/2020/01/006624.html 。隣接する二層の厚みのバランスで二進情報を表し、市販のドキュメントスキャナで読み出す。日本の研究であり、光学読み取りの造形透かしとして重要である。
- Jong-Uk Hou, Do-Gon Kim, Heung-Kyu Lee, "Blind 3D Mesh Watermarking for 3D Printed Model by Analyzing Layering Artifact", IEEE Transactions on Information Forensics and Security, vol. 12, no. 11, pp. 2712-2725, 2017, DOI 10.1109/TIFS.2017.2718482。確認先 https://api.crossref.org/works/10.1109/TIFS.2017.2718482 。積層痕を歪みではなく方向推定のテンプレートとして使う発想が面白い。同じ著者らの Jong-Uk Hou, Do-Gon Kim, Sunghee Choi, Heung-Kyu Lee, "3D Print-Scan Resilient Watermarking Using a Histogram-Based Circular Shift Coding Structure", IH&MMSec 2015, DOI 10.1145/2756601.2756607 も併せて押さえるとよい。
- Zhengxiong Li, Aditya Singh Rathore, Chen Song, Sheng Wei, Yanzhi Wang, Wenyao Xu, "PrinTracker: Fingerprinting 3D Printers using Commodity Scanners", ACM CCS 2018, pp. 1306-1323, DOI 10.1145/3243734.3243735。確認先 https://api.crossref.org/works/10.1145/3243734.3243735 。造形物の充填の微細な癖から製造したプリンタを99.8パーセントの精度で特定する。CipherFlute の脅威モデルにおいて「物理層は情報を漏らす」という主張の裏づけとして使える。
- Chen Song, Zhengxiong Li, Wenyao Xu, Chi Zhou, Zhanpeng Jin, Kui Ren, "My Smartphone Recognizes Genuine QR Codes!: Practical Unclonable QR Code via 3D Printing", IMWUT, vol. 2, no. 2, 2018, DOI 10.1145/3214286。確認先 https://api.crossref.org/works/10.1145/3214286 。3Dプリントの物理的な個体差を複製困難な指紋として使い、市販スマートフォンで真贋を判定する。複製容易性についての CipherFlute の宣言と対比できる。
- Hao Peng, Lin Lu, Lin Liu, Andrei Sharf, Baoquan Chen, "Fabricating QR codes on 3D objects using self-shadows", Computer-Aided Design, vol. 114, pp. 91-100, 2019, DOI 10.1016/j.cad.2019.05.029。確認先 本文PDF https://cfcs.pku.edu.cn/baoquan/docs/2019-06/20190610093546503775.pdf 。単一材料で彫り込んだ幾何が落とす自己影で白黒パターンを作り、標準のQRリーダーで読ませる。
- Jingru Yang, Hao Peng, Lin Liu, Lin Lu, "3D printed perforated QR codes", Computers & Graphics, vol. 81, pp. 117-124, 2019, DOI 10.1016/j.cag.2019.04.005。確認先 https://api.crossref.org/works/10.1016/j.cag.2019.04.005 。
- Hao Peng, Peiqing Liu, Lin Lu, Andrei Sharf, Lin Liu, Dani Lischinski, Baoquan Chen, "Fabricable Unobtrusive 3D-QR-Codes with Directional Light", Computer Graphics Forum, vol. 39, no. 5, pp. 15-27, 2020, DOI 10.1111/cgf.14065。確認先 https://cris.huji.ac.il/en/publications/fabricable-unobtrusive-3d-qr-codes-with-directional-light/ およびプロジェクトページ http://irc.cs.sdu.edu.cn/DirectQR/index.html 。形状の改変を最小にしてQRコードを埋める三部作である。
- Fei Chen, Jaime Zabalza, Paul Murray, Stephen Marshall, Jian Yu, Nikhil Gupta, "Embedded product authentication codes in additive manufactured parts: Imaging and image processing for improved scan ability", Additive Manufacturing, vol. 35, article 101319, 2020, DOI 10.1016/j.addma.2020.101319。確認先 https://strathprints.strath.ac.uk/72334/ 。金属造形物の内部にQRコードを埋め、マイクロCTやラジオグラフィで撮って画像処理を施し、最終的に市販のスマートフォンアプリで読める画像まで復元する。
- Julian Koch, Silvan Gantenbein, Kunal Masania, Wendelin J. Stark, Yaniv Erlich, Robert N. Grass, "A DNA-of-things storage architecture to create materials with embedded memory", Nature Biotechnology, vol. 38, no. 1, pp. 39-43, 2020（オンライン公開は2019年12月9日）, DOI 10.1038/s41587-019-0356-z。確認先 https://pubmed.ncbi.nlm.nih.gov/31819259/ （題名・著者6名・巻号・頁・抄録）および https://api.crossref.org/works/10.1038/s41587-019-0356-z 。DNAをシリカ粒子に封じてフィラメントに練り込み、3Dプリントしたスタンフォードバニーに45キロバイトの自身の設計図を保持させた。抄録は前世代の記憶だけから5世代の複製を作ったこと、および眼鏡レンズのアクリルに1.4メガバイトの動画を収めたことも述べている。日用品に情報を隠すステガノグラフィとしての用途を論文自身が挙げている。読み出しにはDNAシーケンサが要るため実用の敷居は高いが、「日用品が自身の情報を持つ」という主張の極北として引用価値がある。
- Rong-Hao Liang, Hannah van Iterson, Holly Krueger, Marina Toeters, Loe Feijs, "Chic-Marker: Fashionably Fusing Fiducial Markers into Apparel and Accessories", SCF 2024, pp. 1-15, DOI 10.1145/3639473.3665790。確認先 https://api.crossref.org/works/10.1145/3639473.3665790 および著者所属機関の公開記録 https://research.tue.nl/en/publications/de9bca47-1187-47b4-9152-1a5c4cc2f3cf 。千鳥格子（Pied-de-poule）の模様に四角形の基準マーカーを溶け込ませ、衣類や小物としての見た目を保ったまま機械可読にする。日用品への偽装という論点の直接の先行例である。マーカーの具体的な方式が AprilTag なのか ArUco なのかは、抄録では「square fiducial markers」までしか確認できなかった。
- Hal Sugiyama, Hsuanling Lee, Hanako Fujino, Mayuka Kuwana, Mustafa Doga Dogan, Liang He, Koya Narumi, "Weaving and Disguising Infrared Markers toward Invisible Textile Interaction", CHI Extended Abstracts 2026, pp. 1-5, DOI 10.1145/3772363.3799013。確認先 https://api.crossref.org/works/10.1145/3772363.3799013 （題名・著者7名・会議名・年を確認した。5頁の Extended Abstracts であり本会議論文ではない）。近赤外を吸収する糸で織物にマーカーを織り込み、意匠を損なわずに読ませる。日本の研究者が関わる最新の「偽装」研究である。
- Marco Maida, Alberto Crescini, Marco Perronet, Elena Camuffo, "Claycode: Stylable and Deformable 2D Scannable Codes", ACM Transactions on Graphics, vol. 44, no. 4, pp. 1-14, 2025, DOI 10.1145/3730853。確認先 https://api.crossref.org/works/10.1145/3730853 および抄録 https://api.openalex.org/works/doi:10.1145/3730853 。ビット列を位相の木に写してから対象の輪郭のなかに入れ子の色領域として描く二次元コードで、任意形状に溶け込ませられる。位相でビットを表すという点で Seedmarkers と同じ系譜にあたる。
- Zhonghua Ma, Yanfeng Jiang, "High-Density 3D Printable Chipless RFID Tag with Structure of Passive Slot Rings", Sensors, vol. 19, no. 11, article 2535, 2019, DOI 10.3390/s19112535。確認先 https://api.crossref.org/works/10.3390/s19112535 、https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:%2210.3390/s19112535%22&resultType=core&format=json 、および本文 https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6603627/fullTextXML 。電子部品を持たない印刷可能なタグで、同心の矩形スロットリングの共振周波数の違いをビットに割り当てる。実装したのは35ミリメートル角の12ビットのタグであり、2ギガヘルツから9ギガヘルツの帯域を使い、読み取り器との距離50センチメートルで正しく読めたと報告している。読み出しには広帯域の電波送受信装置が要る。第一著者名について、当初この項目は AnisoTag の著者 Zehua Ma と同一人物であるかのように「Zehua Ma」と書いていたが、出版社が登録した書誌とEurope PMCの著者情報はいずれも別人の Zhonghua Ma であったため訂正した。また「拡張版で22ビット」という記述は本文全体を検索しても根拠が見つからなかったため削除した。本文に現れるビット数は12ビットだけである。
- Mustafa Doga Dogan, "Ubiquitous Metadata: Design and Fabrication of Embedded Markers for Real-World Object Identification and Interaction", arXiv:2407.11748, 2024（MIT博士論文）。確認先 https://arxiv.org/abs/2407.11748 および https://dblp.org/search/publ/api?q=Ubiquitous+Metadata+Dogan&format=json 。本文に「We categorize the proposed tagging approaches into three distinct categories: natural markers, structural markers, and internal markers」とあり、埋め込みマーカーを自然マーカー、構造マーカー、内部マーカーの三つに分類する枠組みを与えている。CipherFlute の位置づけを図示するときに使える。
- Sinan Gültekin, Ahmet Ural, Ulas Yaman, "Embedding QR Codes on the Interior Surfaces of FFF Fabricated Parts", Procedia Manufacturing, vol. 39, pp. 519-525, 2019, DOI 10.1016/j.promfg.2020.01.411。確認先 https://api.crossref.org/works/10.1016/j.promfg.2020.01.411 。溶融樹脂積層（FFF）方式の造形物の内部の面にQRコードを作り込む研究である。上の総説の著者 Ulas Yaman の研究室の成果であり、当初この項目は著者も掲載誌も不明として未検証に置いていたが、Crossrefで書誌を特定できた。
- Ankit Mohan, Grace Woo, Shinsaku Hiura, Quinn Smithwick, Ramesh Raskar, "Bokode: imperceptible visual tags for camera based interaction from a distance", ACM Transactions on Graphics, vol. 28, no. 3, article 98, 2009, DOI 10.1145/1531326.1531404。確認先 https://api.crossref.org/works/10.1145/1531326.1531404 および https://dblp.org/search/publ/api?q=Bokode+imperceptible+visual+tags&format=json 。カメラのボケを積極的に使って微小な光学タグを遠くから読ませる研究である。造形物への埋め込みではないので背景にとどまるが、「小さくて目立たない光学タグ」の古典として押さえておく価値がある。

## 未検証のまま残ったもの

以下は実在または書誌情報を一次資料で確認しきれなかった。本文に書く場合は改めて確認が必要である。2026年7月30日の検証で、以前ここにあった4件のうち Bokode、IEICEのX線階調の短報、FFF内部面のQRコード、二層の近赤外蛍光染料の4件はすべて書誌を特定できたため、それぞれ該当する節へ移した。残ったのは次の2件である。

1. ローレンス・リバモア国立研究所によるテラヘルツ帯の「キラルQRコード」（左巻きと右巻きの螺旋を画素として円偏光の違いで二つの符号を読み分けるもの）。報道記事でしか確認できておらず、論文の書誌情報を特定できていない。2026年7月30日の検証では、Crossrefの書誌検索（query.bibliographic に chiral, terahertz, QR code, circular polarization, additive manufacturing を与えたもの）でも該当する論文が出てこなかった。Web検索の予算を使い切っていたため、報道記事からの追跡ができていない。偏光を使う情報埋め込みの例として面白いので、必要なら追加調査を勧める。
2. Chic-Marker が使っている四角形の基準マーカーが AprilTag なのか ArUco なのか。抄録と所属機関の公開記録には「square fiducial markers」とだけあり、本文PDFは著者所属機関のリポジトリでも取得できなかった（HTTPは200を返すが本文ではなくエラーページが返る）。本文で AprilTag と断定して書くことはできない。

## この切り口で見つからなかったこと

CipherFlute の新規性の主張を支える材料として、次のことは「探したが見つからなかった」と言える。いずれも今回の調査で、UIST、CHI、SIGGRAPH、SCF、TEI、UbiComp（IMWUT）、Graphics Interface、および画像・情報ハイディング系の主要誌を横断して確認した範囲での結論である。

第一に、造形物への情報埋め込みで、明示的な脅威モデルを立て、しかも「物理層には暗号学的な秘匿の力がまったく無い」と宣言した研究は見つからなかった。AirCode、InfraredTags、BrightMarker、LayerCode、G-ID、AnisoTag、StructCode、Seedmarkers、InfoPrint、Documented のいずれも、安全性、プライバシー、攻撃者についての節を持たない。偽造防止や著作権保護を動機として挙げる研究（InfraStructs、上平グループ、PrinTracker、unclonable QR、Chen らの認証コード）はあるが、そこでの敵は「偽物を作る者」であって「秘密を読み出す者」ではない。所有者の秘密を守るために埋め込むという構図で、守る力の所在を秘密分散に明け渡した設計は、この分野に前例がない。唯一近いのは Secure Information Embedding in Forensic 3D Fingerprinting であるが、こちらは所有者に無断で追跡するための埋め込みであり、立場が逆である。

第二に、暗号資産のリカバリーシードや暗号鍵の保管を目的として、造形物に光学的に読める符号を埋め込む研究は見つからなかった。金属製のシード保管製品のような工業製品はあるが、これらは平文の刻印であって符号化も誤り訂正も日用品への偽装も行っていない。学術文献としては、3Dモデルに対する秘密分散（Shamir の方式を3Dオブジェクトのジオメトリに適用するもの）が計算機科学の側にあるだけで、印刷された物理物体を分散の担い手にした研究は見当たらなかった。

第三に、読み出しに所有者の身体的な行為を必要とする光学タグは見つからなかった。光学系はすべて、物体を撮像装置の前に置きさえすれば所有者の関与なく読める。InfoPrint だけが「触って温度を移す」という行為を要求するが、これは誰が触ってもよいので所有者に限定されない。逆に言えば、「吹く」という行為が読み出しの必須手順になる CipherFlute は、この点で光学系のどれとも異なる。ただしこの差は秘匿性を生まないことに注意が必要である。形状を計測すれば無音で読めるという CipherFlute 自身の宣言と整合させて書く必要がある。

第四に、既知の音高を持つ基準素子を同一物体に混ぜて全体のずれを打ち消すという設計（通信のパイロット信号にあたるもの）は、光学系の造形タグには見当たらなかった。LayerCode は隣接する二層の厚みの比を使うことで自己正規化を実現しているが、これは基準素子を別に置く発想ではない。AirCode は既知ビットを散らして分類器をその場で学習させており、これが最も近いが、目的は環境変動の正規化ではなく画素分類である。

第五に、隣接するシンボルが同じ値にならないという制約（8B/10B のような遷移保証）を課した造形タグは見つからなかった。光学系では隣接セルの同値は問題にならないため、この制約自体が音響固有の設計である。

第六に、40個から50個の独立した符号素子を一つの日用品の各所に分散配置して128ビットを運ぶ、という空間構成の光学的な先行例は見つからなかった。光学タグはいずれも情報を一つの面や一つの層列に集約する。分散配置は、破損耐性の観点では LayerCode（物体全体に符号が行き渡るので破片からも読める）や Delmotte の局所パッチ方式が近いが、これらは同じ符号の反復であって、素子ごとに異なるシンボルを担わせる構成ではない。

第七に、リードソロモン符号については前例がある点を明記しておく。AirCode は40パーセントの冗長度でリードソロモン符号を実際に使っており、InfraStructs と LayerCode は採用可能であることを明記している。したがって「造形タグに誤り訂正符号を入れたこと」は新規性として主張できない。主張できるのは、音高スロットという離散化の粒度と、基準笛による正規化と、隣接同値禁止の三つを組み合わせた符号設計の全体である。

## 調べ残した穴

第一に、Web検索の呼び出し予算をセッション途中で使い切ったため、後半は既知のURLに対するWebFetchだけで進めた。その結果、2024年から2026年にかけての最新の SCF、UIST、TEI、Graphics Interface の予稿集を網羅的には見ていない。特に SCF 2024、SCF 2025、SCF 2026 と UIST 2025、CHI 2026 の本会議論文に、造形タグの新作がある可能性が残る。各会議の予稿集ページを一件ずつ開いて題名を走査する作業が残っている。

第二に、日本語文献の網羅が不十分である。CiNii Research の全文検索で上平グループの技術報告は多数拾えたが、電子情報通信学会や画像電子学会の技術研究報告は題名までしか確認できていない。また、画像電子学会誌の2023年のデジタルファブリケーション特集（第52巻第1号）の目次を取得しようとしたがファイルが大きすぎて失敗した。この特集には日本語の関連研究が含まれる可能性が高い。WISS についても2019年の一件しか確認できておらず、2020年から2025年の予稿集を年ごとに開いて確認する作業が残っている。インタラクションの予稿集も同様である。

第三に、被引用のたどりが浅い。AirCode、InfraredTags、LayerCode の被引用一覧を Semantic Scholar でたどれば、まだ拾えていない後続研究が出てくるはずである。今回は Semantic Scholar の呼び出し回数制限（HTTP 429）に何度も当たり、被引用の網羅までは到達できなかった。API鍵を用意して被引用を機械的に列挙し直すべきである。

第四に、材料科学側の偽造防止タグ（アップコンバージョン蛍光体、量子ドット、ランタノイド、プラズモニック粒子による物理的複製困難関数）を表面的にしか見ていない。これらは光学読み取りで数百ビット以上を扱う例があり、CipherFlute の容量の議論に影響する可能性がある。ただし家庭用のFDMプリンタでは作れないため、脅威としては低いと判断して深追いしなかった。

第五に、特許を調べていない。検索の過程で「Using everyday objects as cryptographic keys」「Retrieving data embedded into the surface of a 3D printed object」「Method and apparatus for storing and retrieving data embedded into the surface of a 3D printed object」といった米国特許が繰り返し現れた。学術文献ではないが、CipherFlute の着想に近いものが特許として存在する可能性があり、必要なら別途調べるべきである。

## 検証で削除したもの

2026年7月30日の検証で、実在しない文献であると判断して削除した項目は一件もない。この文書に挙がっていた文献はすべて、出版社が登録した書誌または学会の公式な予稿集ページで実在を確認できた。削除したのは文献ではなく、次の一つの事実主張である。

1. Zhonghua Ma と Yanfeng Jiang による Sensors 誌のチップレスRFIDタグの項目にあった「拡張版で22ビットを扱う」という記述を削除した。Europe PMC から取得した本文全文を機械的に走査し、「N ビット」の形で現れる数を数えたところ、この論文が自身の実装として述べているのは12ビットだけであり、22という数はどこにも現れなかった。参考文献に挙がっている他者の研究には35ビットのものがあるので、そこと混同した可能性がある。

## 検証の記録

2026年7月30日、この文書の書誌情報を、当初の調査担当者とは別の担当者が独立に検証した。手順は、まず文書に挙がっている文献と事例をすべて列挙し、次に各項目のDOIを Crossref に問い合わせて出版社が登録した題名・著者・掲載誌・巻号・頁・年を取り出し、論文番号については dblp に問い合わせ、内容の主張については本文PDFまたは著者の公式プロジェクトページを取得して該当箇所を原文で確かめる、というものである。日本語文献は CiNii Research と J-STAGE、WISS の予稿集ページを直接取得した。生物医学系の一件は PubMed と Europe PMC を使った。

検証した文献と事例は、この文書に挙がっていた44件である。このうち43件について実在と書誌情報の両方を確認できた。確認できなかったのは「ローレンス・リバモア国立研究所のキラルQRコード」の1件だけであり、これは「未検証のまま残ったもの」の節に残した。あわせて、Chic-Marker が使う基準マーカーの具体的な方式という細部も裏が取れなかったので、同じ節に書き足した。実在しないと判断して削除した文献は一件もない。また検証の過程で、上平グループの系列が2015年に始まることを示す VISAPP 2015 の論文と、金属混入樹脂とサーモグラフィを組み合わせた2018年の論文の2件を新たに確認して追加したため、文書に載っている文献は46件になった。

訂正は38箇所である。内訳は次のとおりである。第一に、明白な誤りが2件あった。Sensors 誌のチップレスRFIDタグの第一著者を「Zehua Ma」と書いていたのは誤りで、正しくは別人の「Zhonghua Ma」である。当初の記述は AnisoTag の第一著者 Zehua Ma と混同したものと見られる。もう一つは、同じ項目の「拡張版で22ビット」という記述に根拠がなかったことである。第二に、G-ID の識別数204通りを「約7.4ビット」と換算していたのを「約7.7ビット」に直した。第三に、WISS 2019 の論文について、査読コメントの要点を原文に合わせて直した。当初は「著者らの過去の電子透かし研究との整合性が問われた」と書いていたが、実際に指摘されているのは、権利保護という動機と誰でも複製できる充填パターンをタグに使うことのあいだの矛盾、および識別できる個体数の拡張性である。あわせて、この論文の提案手法に FabAuth という名前が付いていること、読み出しがアクティブ音響センシングによる音響周波数応答の解析であることを補った。第四に、Usama と Yaman の総説について、読み出し方式の一覧から「超音波」を外し、「テラヘルツ」も InfraStructs を引用する文脈でしか現れないため外した。また1平方センチメートルあたり6.25ビットという数字が分野の代表値ではなく上平グループの特定手法の実測値であることを明記した。第五に、Sugiyama らの CHI Extended Abstracts 2026 の共著者「M. Kuwana」をフルネームの「Mayuka Kuwana」に直した。第六に、書誌情報の欠けを埋めた。InfraredTags 以外の11件について論文番号や頁、巻号を補い、DNA-of-things の年を2019年から2020年（巻38、第1号、39-43頁、オンライン公開は2019年12月9日）に直し、IWDW 2016 の論文に LNCS 第10082巻と370-378頁を補い、Iyer らの ACM Transactions on Graphics 論文に第6号と242:1-242:13頁を補った。第七に、確認先のURLを、実際にこの検証で取得したもの（Crossref、dblp、OpenAlex、Europe PMC、PubMed、出版社ページ、公式プロジェクトページ）に置き換えた。当初は7件が Semantic Scholar API を確認先としていたが、この検証では使っていないため書き換えた。第八に、誤字「ノズイズ」を「ノイズ」相当の記述に直した。

数値の主張については、次のものを原典の本文で裏を取った。AirCode の「2センチメートル角で約106ビット、5センチメートル角で約500ビット、リードソロモン符号で40パーセントの冗長度、撮像に3分から4分」はすべて本文PDFの記述と一致した。InfraStructs の「一次元タグで8ビット、行列型タグで27ビット、Picometrix T-Ray 4000、100×100画素で約2分、リードソロモン符号は将来課題」はすべて一致した。LayerCode の「24ビット、近赤外の変種で12ビット、誤り訂正はあえて付けない」も一致した。G-ID の「カメラのみで204通り、光源併用で17,136通り」も一致した。InfraredTags の「21×21のQRコードで数字25文字、4×4のArUcoマーカー、132グラムのモジュール、250センチメートル」も一致した。AnisoTag の「53.98×85.6ミリメートルで51ビット、160ビットへの拡張、3ドルのレーザーポインタと7ドルのマイクロコントローラ」も一致した。StructCode の「指型継手で12文字、リビングヒンジで21文字」および暗号化に関する一文も一致した。Seedmarkers の「重み付きボロノイ図による位相的な最適化」も抄録と一致した。BrightMarker の「1インチ角で2メートル以上」も一致した。WISS 2019 の「99.3パーセントで8個」も予稿の概要と一致した。DNA-of-things の「45キロバイト」も一致した。Delmotte らの「隣接する二層の厚みのバランス」と「市販のドキュメントスキャナ」も奈良先端科学技術大学院大学のプレスリリースの記述と一致した。Chen らの「市販のスマートフォンアプリで読める画像まで復元する」も本文の記述と一致した。
