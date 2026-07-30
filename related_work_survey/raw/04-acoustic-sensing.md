# 音響センシングと静電容量センシングによる物体・状態の認識

この文書は、CipherFluteの新規性を確かめるために、音響と静電容量を用いて物体そのものや物体の状態・操作を認識する研究を洗い出した結果をまとめたものである。書誌情報は原則としてdblp、CiNii Research、Crossref、DataCite、OpenAlex、Semantic Scholar、出版社のページ、著者本人または所属研究室の業績ページ、学会の予稿集ページ、NSFの公開リポジトリ、arXivのいずれかにあたって確認した。確認できなかったものは「未検証のまま残ったもの」の節に分けて書いた。

なおこの文書は2026年7月30日に、別の担当者による独立した検証を受けている。検証で見つかった誤りはすべて本文に反映し、訂正した箇所にはその旨を書き添えた。検証の内容と結果は末尾の「検証の記録」の節にまとめてある。

各文献については、依頼のとおり次の3点を必ず書いた。第一に、読み出しの対象となる物体そのものが無電源で成立するのか、それとも物体側に電源や電子部品が要るのかである。第二に、その手法が識別できる情報量がどれくらいかである。第三に、CipherFluteのように「物体の形が情報を固定して保持する」という発想があるかどうかである。

## この切り口の要約

この切り口を調べた結論を述べる。まず、音響で物体を認識する研究は大きく3つの系統に分かれていた。第一の系統は、物体側にスピーカとマイクを貼り付けて掃引信号を流し込み、伝達特性の変化から接触や把持や物体を判別するアクティブ音響センシングである。日本ではこの系統が非常に厚く、大野・志築・田中によるTouch & Activateを起点として、大阪大学の伊藤雄一の研究室、立命館大学の村尾和哉の研究室、筑波大学の志築文太郎の研究室が現在まで継続的に発表している。この系統は物体側または近傍に電源が要るという点で、CipherFluteとは前提が異なる。第二の系統は、物体の形そのものが受動的に固有の音を作り出し、それをマイクで読むというものである。Acoustic Barcodes、Lamello、Acoustruments、SqueezaPulse、Let It Rip、そしてBlowholeがこれにあたり、CipherFluteに最も近い。第三の系統は、環境音や操作音を機械学習で分類する系統であり、UbicousticsやSynthetic Sensorsのように物体には何も付けない。

決定的に重要な発見が2件あった。1件目はBlowholeであり、3Dプリント物体の内部にヘルムホルツ共鳴空洞を埋め込み、穴に息を吹き込むと固有の音が鳴って穴を識別できるという研究である。これはCipherFluteの物理的な着想そのものであり、すでに論文で引用されているとおり最大の先行研究である。2件目はSoundOffであり、2025年のIMWUTに出た、電子部品を一切持たない受動超音波タグである。幾何形状が固有振動数を決めるという原理を物理モデルで定式化し、区別しやすい数千の設計を系統的に生成する手法を示している。これはCipherFluteの「形が符号語彙を固定する」という主張に最も近い最新研究であり、現在の論文には入っていないので必ず引用して差分を述べるべきである。

検証の過程で3件目の重要な文献が加わった。Asterisk and Obelisk（UIST 2018）であり、面に印刷された模様を慣性センサ内蔵の指輪をつけた指でなぞって読む受動タグである。1680万通り、すなわち約24ビットの情報容量に対して95パーセントの精度を報告している。音響ではないが、「無電源の受動タグに多ビットの符号を書き込む」という枠組みがすでに20ビット台で達成されていることを示すので、CipherFluteの新規性の言い方に影響する。

一方で、受動的な音響物体に暗号鍵やリカバリーシードのような多ビットの秘密を格納し、誤り訂正符号と基準体による正規化を伴って読み出すという研究は、英語でも日本語でも見つからなかった。既存の受動「音響」タグはいずれも識別子やイベント検出が目的であり、搬送する情報量は数ビットから十数ビットにとどまる。ここがCipherFluteの立つ位置である。ただし音響から離れれば、上のAsterisk and Obeliskのように約24ビットに達する受動タグが存在するので、「受動タグは少数ビットしか運べない」という一般化した書き方は避け、音響に限った主張として書くべきである。

静電容量側では、無電源の3Dプリント物体を静電容量式タッチ画面に載せて導電パターンでIDを読むという系統が確立していた。Itsy-Bits、CAPath、DuoTouchなどがそれにあたり、「形が情報を固定して保持する」という発想は共有されている。ただしIDの規模はやはり小さく、秘密保持の議論は存在しない。

温度変動への対処についても、検証で見方を改めるべき点が出た。川崎ら（情報処理学会論文誌2021）は、問題を指摘しているだけでなく、周波数方向と振幅方向に周波数特性を補正して基準温度における特性に揃えるという解法を提案しており、識別精度を21.5パーセントから75.1パーセントまで引き上げている。したがってCipherFluteの基準笛の新しさは、温度ずれを正規化するという着想そのものではなく、参照を事前の測定ではなく物体の中に同居させて較正を不要にした点にある。

## 新規性への脅威が大きい文献

### 1. Blowhole: Blowing-Activated Tags for Interactive 3D-Printed Models

- 著者: Carlos Tejada, Osamu Fujimoto, Zhiyuan Li, Daniel Ashbrook（dblpとDataCiteのいずれも、この論文の第一著者を中名の頭文字なしの「Carlos Tejada」と記録している。同一人物は後述のEchoTubeやAirTouchでは「Carlos E. Tejada」と表記されており、論文ごとに表記が揺れている。Blowholeを引くときは中名の頭文字を付けないほうが一次情報に沿う）
- 発表: Proceedings of Graphics Interface 2018, pp. 131-137, 2018年（DOI 10.20380/GI2018.18、発行はCanadian Human-Computer Communications Society）
- 確認先: https://api.datacite.org/dois/10.20380/GI2018.18 （DOIの登録元。題名、著者4名、収録先、ページ、年を確認した）、https://api.openalex.org/works/doi:10.20380/GI2018.18 （抄録の全文を確認した）、https://dblp.org/search/publ/api?q=Blowhole+blowing+activated+tags&format=json
- 内容の要約: 3Dプリントした模型の内部に音響的に共鳴する空洞を作り、物体表面に目立たない開口を設ける手法である。開口に軽く息を吹き込むと空洞ごとに固有の音が鳴り、どの穴を吹いたかを計算機が判別して対応する情報を提示できる。抄録には、特別な印刷手法も部品も組み立ても要らず一般消費者向けの3Dプリンタで動くこと、空洞の各パラメタが性能に与える影響を特性づけたこと、既存のモデルに自動で空洞を埋め込む扱いやすいソフトウェアを用意したことが明記されている。
- CipherFluteとの関係: 「3Dプリントした無電源の物体に息を吹き込んで音を出し、その音の違いを符号として読む」という機構がそのまま重なる。ただしBlowholeはヘルムホルツ共鳴の空洞であって管の長さで基本周波数を決めるフィップル笛ではなく、目的も模型のどの部位を吹いたかという位置の識別であって、多ビットの秘密の保持ではない。空洞1個が担う情報は「その穴かどうか」に近い。誤り訂正も、既知の音高を持つ基準体による正規化も、符号語彙の設計も扱っていない。物体の形が情報を固定して保持するという発想は明確に共有されている。無電源で成立し、読み出し側にマイクが要るという構図も同じである。
- 数値についての注記: 「模型あたりの穴の数はせいぜい数個から十数個である」という記述は、抄録には根拠が見当たらなかったため、この調査の推測として扱ってほしい。抄録は穴の個数も1個あたりのビット数も述べていない。
- 脅威の度合い: 高
- 理由: CipherFluteの物理層の着想がすでに2018年に提示されている以上、「吹いて読む3Dプリント無電源タグ」という枠自体は新規ではない。CipherFluteの新規性は、符号語彙の設計、基準笛による正規化、誤り訂正、秘密分散との組合せという情報設計の側にあると明確に述べ直さないと、主張が大きく弱まる。

### 2. SoundOff: Low-cost Passive Ultrasound Tags for Non-invasive and Non-Intrusive Smart Home Sensing

- 著者: Yibo Fu, Vivian Shen, Víctor Riera Naranjo, Bolei Deng, Alex Adams, Josiah Hester（dblpは第5著者を Alexander Travis Adams、第6著者を Josiah D. Hester と記録している）
- 発表: Proceedings of the ACM on Interactive, Mobile, Wearable and Ubiquitous Technologies (IMWUT), Vol. 9, No. 4, 記事番号174, pp. 174:1-174:32, 2025年（DOI 10.1145/3770666）
- 確認先: https://par.nsf.gov/biblio/10670927 （抄録の全文を確認した。なお本文の公開は2026年12月2日まで留保されている）、https://api.crossref.org/works/10.1145/3770666 、https://dblp.org/search/publ/api?q=SoundOff+ultrasound+tags&format=json （記事番号とページを確認した）
- 内容の要約: 電池も回路も持たない受動超音波タグを室内の家具や建具、すなわちドアノブ、便座の蓋、戸棚、蛇口、窓に取り付ける手法である。抄録によれば、これらの家具が動くとタグごとに固有の超音波放射が生じ、人の可聴域を超えているため邪魔にならず、また撮影や録音のような privacy の問題も起こしにくい。物理に基づくモデル化によって、互いに区別しやすい固有の超音波放射を持つ設計を数千通り系統的に生成できることを示し、幾何モデリングの流れと製作の指針、そして書き換えやすい認識系を公開している。読み出しは利用者が身につけた装置で行うと抄録に明記されている。
- CipherFluteとの関係: 「形が周波数を決める」「区別しやすい符号語彙を物理モデルから系統的に設計する」「タグ側は完全に無電源で電子部品を持たない」という3点がCipherFluteと正面から重なる。CipherFluteが管長Lと基本周波数fの関係をf = A/(L+e)で近似して13個のスロットに切り分けたのと同じ設計行為を、SoundOffは幾何形状の振動に対して行っている。ただしSoundOffのタグは1個が1つの識別子を担うだけで、多ビットの情報を並べて秘密を運ぶという発想はない。誤り訂正も基準タグによる正規化もない。用途は生活行動のセンシングであり、秘密の保管や脅威モデルの議論は存在しない。
- 数値と素材についての注記: この調査の初回の記述にあった「硬貨より小さい」という寸法、「ステンレス鋼を特定の形に切り出す」という素材、「タグが弾かれる」という励振の機構、そして「板状金属の曲げ振動」という振動の型は、いずれも抄録には書かれておらず裏が取れなかったので、本文からは削った。本文は2026年12月2日まで公開が留保されているため、素材と寸法を論文で述べる場合は改めて原文にあたってほしい。抄録で確かに裏が取れたのは、電子部品を持たないこと、数千通りの設計を系統的に生成できること、読み出しが利用者の身につけた装置で行われることの3点である。
- 脅威の度合い: 高
- 理由: 「無電源の物体の形状に符号語彙を作り込み、音で読む」という設計方法論がすでに2025年に体系化されている。しかもCipherFluteの投稿先より新しく、査読付きの主要ジャーナルである。現行の論文はこの研究を引用していないため、そのままだと最新の直近先行を見落としているという指摘を受ける危険が大きい。

### 3. FabAuth: Printed Objects Identification Using Resonant Properties of Their Inner Structures

- 著者: Yuki Kubo, Kana Eguchi, Ryosuke Aoki, Shigekuni Kondo, Shozo Azuma, Takuya Indo（日本電信電話株式会社）
- 発表: Extended Abstracts of the 2019 CHI Conference on Human Factors in Computing Systems (CHI EA 2019), Paper No. LBW2215, 2019年5月（DOI 10.1145/3290607.3313005）
- 確認先: https://www.yukikubo.net/index-e.html （著者本人の業績ページ。著者6名、題名、収録先、論文番号、年を確認した）、https://api.semanticscholar.org/graph/v1/paper/DOI:10.1145/3290607.3313005 （抄録で「平均92.2パーセント」を確認した）、https://dblp.org/search/publ/api?q=FabAuth+printed+objects+identification+resonant&format=json
- 内容の要約: 3Dプリントした物体の内部構造を変えることで、外観が同じ物体どうしにも異なる共鳴特性を与え、その差で個体を識別する手法である。物体を通り抜ける振動を利用して共鳴特性の差を読み取る。充填率の低い3Dプリント物体にも、センサ間を音波が伝われば適用できるとしている。抄録には平均92.2パーセントの分類精度が得られたと明記されている。
- CipherFluteとの関係: 「外から見えない内部構造に情報を固定し、音響的な共鳴の違いとして読み出す」という発想がCipherFluteと重なる。日用品への偽装という着想の土台にもなる。ただし読み出しには物体を加振する装置と受振側の装置が要り、物体そのものは受動でも系全体としては電源が必要である。識別できるのは学習済みの数個から十数個のクラスであって、任意のビット列を格納する符号ではない。基準体による正規化も誤り訂正も扱っていない。
- 脅威の度合い: 中
- 理由: 「同じ外観の物体の内部形状に情報を隠し、共鳴で読む」という中核の着想がCipherFluteと共有されているため、引用して差分を述べる必要が高い。ただし情報量が識別クラス数にとどまり、無電源の吹鳴による読み出しでもないため、主要な主張が崩れるところまでは行かない。

### 3の続き. 3D-Printed Object Identification Method using Inner Structure Patterns Configured by Slicer Software（FabAuthの後続研究、検証の過程で新たに見つけたもの）

- 著者: Yuki Kubo, Kana Eguchi, Ryosuke Aoki
- 発表: Extended Abstracts of the 2020 CHI Conference on Human Factors in Computing Systems (CHI EA 2020), pp. 1-7, 2020年4月（DOI 10.1145/3334480.3382847）
- 確認先: https://www.yukikubo.net/index-e.html （著者本人の業績ページ）、https://api.openalex.org/works/doi:10.1145/3334480.3382847 （抄録を復元して数値を確認した）
- 内容の要約: FabAuthと同じ研究陣による続きの仕事である。スライサソフトウェアの設定で決まる内部構造の違いが共鳴特性を変えることを利用して、3Dプリント物体を識別する。物体の形状、材料、構造の境界に応じて共鳴特性がずれることを利用し、音響センシングと機械学習で周波数応答から個体を当てる。2回の実験で8個の物体を99.3パーセントの分類精度で区別できたと報告している。
- CipherFluteとの関係: 「内部構造という外から見えない形に情報を固定し、共鳴で読む」というFabAuthの着想を、スライサの設定という作りやすい変数に落とし込んでいる。識別できるクラス数が8個と明示されている点は、CipherFluteが1本あたり約3.7ビットを13スロットで運ぶという主張と直接比較できるので有用である。8クラスは3ビットに相当し、CipherFluteの1本分とほぼ同じ規模にとどまる。
- 脅威の度合い: 中
- 理由: FabAuthと同じ枠組みの発展であり、CipherFluteの1本あたりの情報量と正面から比較できる数値を持っている。引用して、CipherFluteが符号語を連ねて128ビットに届かせるという設計を差分として述べるべきである。

### 4. Acoustic Voxels: Computational Optimization of Modular Acoustic Filters

- 著者: Dingzeyu Li, David I. W. Levin, Wojciech Matusik, Changxi Zheng
- 発表: ACM Transactions on Graphics (SIGGRAPH 2016), Vol. 35, No. 4, 記事番号88, pp. 88:1-88:12, 2016年（DOI 10.1145/2897824.2925960）
- 確認先: https://api.openalex.org/works/doi:10.1145/2897824.2925960 （抄録を復元して確認した）、https://dblp.org/search/publ/api?q=Acoustic+Voxels+computational+optimization+modular+acoustic+filters&format=json （記事番号とページを確認した）、https://cdfg.mit.edu/publications/acoustic-voxels-computational-optimization-modular-acoustic-filters
- 内容の要約: 中空の立方体状の小室を積み木のように組み合わせて音響フィルタを作り、目標とする音響特性を満たすように配置とパラメタを最適化する計算手法である。各小室の伝達行列をあらかじめ計算しておき、組み合わせ全体の伝達行列を効率よく求めることで対話的な最適化を可能にしている。抄録は応用として消音器の設計、管楽器の試作、そして日用品に知覚されない音響情報を埋め込むことを挙げている。
- CipherFluteとの関係: 「3Dプリント物体の内部形状に情報を埋め込み、音として読み出す」という着想を最初に明示した研究のひとつであり、CipherFluteの論文でもすでに引用されている。物体は無電源で、形が情報を固定して保持するという発想も共有している。ただし読み出しには外部からの加振や送気が必要で、埋め込める情報量については報道記事に4ビット程度という記述があるものの、抄録にはビット数の記述がなく裏が取れていない。符号語彙の設計、誤り訂正、基準体による正規化は扱っていない。なお「外観が同一でも内部の小室の並びが違えば固有の音が出るため音響的なタグとして働く」という説明は抄録の「知覚されない音響情報を埋め込む」という記述からの解釈であり、原文の言い回しそのままではない。
- 脅威の度合い: 中
- 理由: 音響による物体への情報埋め込みという枠組みの先駆であるため必ず引用して差分を述べる必要がある。ただし秘密の保管という目的も、多ビットの符号設計も持っていない。

### 5. Acoustic Barcodes: Passive, Durable and Inexpensive Notched Identification Tags

- 著者: Chris Harrison, Robert Xiao, Scott E. Hudson
- 発表: Proceedings of the 25th Annual ACM Symposium on User Interface Software and Technology (UIST 2012), pp. 563-568, 2012年（DOI 10.1145/2380116.2380187）
- 確認先: https://www.chrisharrison.net/index.php/Research/AcousticBarcodes （著者本人のプロジェクトページ。著者3名、題名、収録先、ページ、年を確認した）、https://dblp.org/search/publ/api?q=Acoustic+Barcodes+passive+durable+inexpensive+notched&format=json 。加えて、インタラクション2018の岩瀬らの論文の参考文献[7]に同じ書誌が載っていることを http://www.interaction-ipsj.org/proceedings/2018/data/pdf/INT18008.pdf の本文から確認した。
- 内容の要約: 物体の表面に切り欠きの並びを刻み、爪などでこすると切り欠きの間隔に応じた複雑な音が鳴り、その波形を二進の識別子に復号する手法である。プロジェクトページには、読み取りに接触マイクを使うこと、こする速度などのばらつきを扱う復号手法を作ったことが書かれている。
- CipherFluteとの関係: 無電源の物体の形状そのものに二進の識別子を固定して保持し、音として読み出すという点で、CipherFluteの直接の祖先にあたる。すでに論文で引用されている。違いは、こする動作による過渡音の時間間隔で符号化する点と、CipherFluteが定常的な発音の音高で符号化する点である。
- 数値についての注記: 1個のバーコードが運ぶビット数は、著者本人のプロジェクトページにも明示されていない。「実用上は十数ビット規模」という見積りはこの調査の推測であって、原典の記述ではない。論文で数値に言及する場合はACM Digital Libraryの本文で確認してほしい。
- 脅威の度合い: 中
- 理由: 「形に二進符号を固定し音で読む受動タグ」という概念そのものはここで確立している。CipherFluteは音高を語彙とすること、基準体で正規化すること、誤り訂正を伴うことで差分を述べる必要がある。

### 6. Lamello: Passive Acoustic Sensing for Tangible Input Components

- 著者: Valkyrie Savage, Andrew Head, Björn Hartmann, Dan B. Goldman, Gautham Mysore, Wilmot Li
- 発表: Proceedings of the 33rd Annual ACM Conference on Human Factors in Computing Systems (CHI 2015), pp. 1277-1280, 2015年（DOI 10.1145/2702123.2702207）
- 確認先: https://api.openalex.org/works/doi:10.1145/2702123.2702207 （抄録を復元し、著者6名とページを確認した）、https://api.semanticscholar.org/graph/v1/paper/DOI:10.1145/2702123.2702207 、https://valkyriesavage.com/lamello.html
- 内容の要約: 親指ピアノのような、長さの異なる櫛歯を並べた構造を入力部品に組み込む手法である。滑り子や回転子が動くと歯が弾かれ、歯ごとに異なる高さの音が鳴る。実時間の音声処理でこれを解析し、高水準の操作イベントを出力する。抄録は貢献として、櫛歯の構造の設計、情報の符号化方式、そして音声解析の流れを一体で作ったことを挙げており、3Dプリントしたボタン、スライダ、ダイヤルで実証している。
- CipherFluteとの関係: 「櫛歯の長さが音高を決める」という設計はCipherFluteの「管の長さが音高を決める」と数理的にほぼ同型であり、長さを離散化して語彙を作るという発想も共通する。しかも抄録が「情報の符号化方式」の設計を明示的に貢献として挙げているので、符号設計という行為そのものはLamelloで先行している。部品は無電源で、形が音高を固定して保持している。ただし目的は操作イベントの検出であって情報の保管ではなく、誤り訂正も既知の音高を持つ基準体による正規化も扱っていない。
- 脅威の度合い: 中
- 理由: 「長さで音高を作り分けて離散的な符号にする」という核心の物理設計に加えて、符号化方式の設計という行為までがLamelloで先行している。すでに論文で引用されているが、CipherFluteの差分は符号語を連ねて128ビットに届かせること、誤り訂正を伴うこと、基準体で正規化することにあると明確に書き分ける必要がある。
- 数値についての注記: 「同時に区別する歯の数は数個から十数個にとどまる」という記述は抄録では確認できなかったため、この調査の推測として扱ってほしい。

### 7. Acoustruments: Passive, Acoustically-Driven, Interactive Controls for Handheld Devices

- 著者: Gierad Laput, Eric Brockmeyer, Scott E. Hudson, Chris Harrison（この調査の初回の記述にあった Mary Mahler は、CHI 2015論文の著者ではない。訂正した経緯は下の注記に書いた）
- 発表: Proceedings of the 33rd Annual ACM Conference on Human Factors in Computing Systems (CHI 2015), pp. 2161-2170, 2015年（DOI 10.1145/2702123.2702414）
- 確認先: https://la.disneyresearch.com/publication/acoustruments/ （出版元に近い研究所のページ。著者4名を確認した。Mary Mahler は載っていない）、https://api.semanticscholar.org/graph/v1/paper/DOI:10.1145/2702123.2702414 （著者4名を確認した）、インタラクション2018論文集の岩瀬らの論文の参考文献[2] http://www.interaction-ipsj.org/proceedings/2018/data/pdf/INT18008.pdf
- 著者名の訂正についての注記: Mary Mahler が著者に入るのは、同じ研究陣がSIGGRAPH 2015のEmerging Technologiesで出した実演発表の版である。すなわち Gierad Laput, Eric Brockmeyer, Mary Mahler, Scott E. Hudson, Chris Harrison「Acoustruments: Passive, Acoustically-driven, Interactive Controls for Handheld Devices」ACM SIGGRAPH 2015 Emerging Technologies, pp. 3:1-3:1, 2015年（DOI 10.1145/2782782.2792490）である。この書誌は岩瀬らの論文の参考文献[18]に載っており、同じ本文から確認した。査読付き論文としてCHI 2015の版を引くなら著者は4名であり、実演発表の版を引くなら5名である。両者を取り違えないでほしい。
- 内容の要約: 携帯端末のスピーカから出た音を、プラスチックで作った受動的な管や弁の構造に通し、マイクに戻ってくる音の変化から操作を検出する手法である。電源も電子部品も要らない一連の設計要素を体系的に洗い出し、それらを組み合わせることでボタン、滑り子、回転子といった馴染みのある機構を受動素材だけで構成できることを示している。
- CipherFluteとの関係: 受動の管構造で音を作り分けるという点が共通する。ただし音源は端末のスピーカであり、人が吹くのではない。また端末側には電源が要る。情報量は操作の種類の判別にとどまる。形が音響特性を固定して保持するという発想は共有している。すでに論文で引用されている。
- 脅威の度合い: 中
- 理由: 「受動の管の形で音を作り分ける」という設計の先例として必ず引用すべきである。ただし目的も読み出し方法も異なるため主張は崩れない。

### 8. Printone: Interactive Resonance Simulation for Free-form Print-wind Instrument Design

- 著者: Nobuyuki Umetani, Athina Panotopoulou, Ryan Schmidt, Emily Whiting（dblpは第3著者を Ryan M. Schmidt と記録している）
- 発表: ACM Transactions on Graphics (SIGGRAPH Asia 2016), Vol. 35, No. 6, 記事番号184, pp. 184:1-184:14, 2016年（DOI 10.1145/2980179.2980250）
- 確認先: https://api.openalex.org/works/doi:10.1145/2980179.2980250 （抄録を復元し、固有値問題と境界要素法と3Dプリントによる演奏可能な楽器の記述をいずれも確認した）、https://dblp.org/search/publ/api?q=Printone+interactive+resonance+simulation+wind+instrument&format=json （記事番号とページを確認した）
- 内容の要約: 自由形状の管楽器を対話的に設計するための計算手法である。抄録によれば、楽器を受動的な共鳴体としてモデル化して吹き口の励振と切り離し、境界要素法に基づく定式化のうえで固有値に基づく効率のよい方法で共鳴周波数を推定する。利用者が形を編集するそばから鳴る音を予測して提示する。設計結果は3Dプリンタで実際に造形でき、通常でない形の管楽器が演奏できることを示している。なお「意図した曲を演奏できる」という記述は抄録の「演奏可能な管楽器を作れる」という記述より踏み込んでいるので、曲の演奏まで主張する場合は本文で確認してほしい。
- CipherFluteとの関係: 「3Dプリントした管楽器の形と鳴る音高の関係を計算で押さえる」という点でCipherFluteの較正の考え方と正面から関係する。CipherFluteはf = A/(L+e)という単純な回帰でこれを済ませているので、Printoneのような数値解法との位置づけの違いを述べておかないと、なぜ簡易式で足りるのかという問いに答えられない。物体は無電源で、形が音高を固定して保持するという発想も共有している。ただし情報の符号化という発想は一切ない。
- 脅威の度合い: 中
- 理由: 「3Dプリント笛の形と音高の設計」という技術的な土台を先行して確立している。CipherFluteの較正手法の位置づけを述べるうえで引用が要る。ただし情報を運ぶという発想がないため主張は崩れない。

### 9. ProtoHole: Prototyping Interactive 3D Printed Objects Using Holes and Acoustic Sensing

- 著者: Shohei Katakura, Keita Watanabe（明治大学）
- 発表: Extended Abstracts of the 2018 CHI Conference on Human Factors in Computing Systems (CHI EA 2018), pp. 1-6, 2018年（DOI 10.1145/3170427.3188471）
- 確認先: https://api.openalex.org/works/doi:10.1145/3170427.3188471 （抄録を復元し、掃引音響センシングと機械学習による分類、そしてページを確認した）、https://dblp.org/search/publ/api?q=ProtoHole+prototyping+interactive+3D+printed&format=json
- 内容の要約: 3Dプリントした筐体に穴を開けることで対話的な物体を試作する手法である。抄録によれば、掃引音響センシングを用いて、穴が開いているか塞がれているかで生じる共鳴の変化を検出し、機械学習で分類する。内部の配線の取り回しを事前に考え込まなくても対話的な試作ができるので、モデリングに慣れていない人でも扱えるとしている。
- CipherFluteとの関係: 「3Dプリント物体の内部空洞と表面の穴の組合せで音響的な状態を作る」という構成がCipherFluteと重なる。日本の研究であり、Blowholeとほぼ同時期に穴と空洞に着目している点で重要である。掃引信号を流し込む方式なので送信側と受信側の装置が要り、CipherFluteのように人の息だけで鳴るわけではない。情報量は穴の個数分の状態にとどまる。形が音響特性を固定して保持するという発想は部分的に共有している。
- 未確認の記述: この調査の初回の記述にあった「物体の内部にスピーカとマイクを入れる」という構成、および「操縦桿、照明の操作器、玩具の犬を例として実装している」という応用例は、抄録には書かれておらず裏が取れなかったので削った。掃引音響センシングを使う以上、送信側と受信側の変換器が必要であることは原理から言えるが、それらが物体の内部にあるのか外にあるのかは本文で確認してほしい。
- 脅威の度合い: 中
- 理由: 「穴と共鳴空洞で3Dプリント物体を対話的にする」という近接した着想であり、しかも日本のHCI分野の研究であるため、投稿先の読者から必ず指摘される。引用して、無電源であることと吹鳴で読むことの違いを述べる必要がある。

### 10. アクティブ音響センシングにおける環境温度変化にロバストな物体情報識別手法の検討

- 著者: 川崎祐太, 伊藤雄一, 藤田和之, 尾上孝雄
- 発表: 情報処理学会論文誌, 第62巻, 第10号, pp. 1658-1668, 2021年10月15日（DOI 10.20729/00213193）
- 確認先: https://cir.nii.ac.jp/crid/1390290701132201344 （CiNii Research。著者4名、題名、巻号、ページ、発行日、DOIを確認したうえで、抄録の全文を読んで内容を照合した）
- 内容の要約: 面に置かれた物体を音響で認識するSenseSurfaceという系を対象に、環境の温度が変わると面の音響周波数特性が変化して物体識別率が落ちるという問題を扱った研究である。抄録によれば、時間とともに周波数が変わるスイープ信号を面に印加して周波数特性を解析するという基本構成のうえで、環境温度がスイープ信号の周波数特性に与える影響を調査し、その知見に基づいて影響の補正を試みている。具体的には、ある温度T1度における周波数特性を、基準となるT0度における周波数特性に対して、周波数方向と振幅方向の両方で補正する。摂氏22.7度から30.5度までの17パターンで評価し、補正前の21.5パーセントから補正後の75.1パーセントまで識別精度が向上したと報告している。
- CipherFluteとの関係: CipherFluteが「気温や息の強さによる全体のずれを打ち消すために、音高が既知の基準笛を1本混ぜて比で読む」と述べている部分に、この研究が正面から対応する。温度変動への対処という問題設定に加えて、「周波数軸方向に特性をずらして基準の温度における特性に揃える」という正規化の考え方までが、日本の先行研究で明示的に扱われている。ただし正規化の参照の取り方が異なり、川崎らは事前に測っておいた基準温度T0における周波数特性を参照するのに対し、CipherFluteは同じ物体の中に既知の音高を持つ基準体を同居させて、読み出しのその場で相対値を取る。すなわち参照が事前の測定にあるか、物体そのものに作り込まれているかが分かれ目である。物体側の電源については、この系はスピーカとマイクを面に取り付けるため電源が要る。
- 脅威の度合い: 中
- 理由: 「温度変化で音響の読みがずれる」という問題だけでなく、「周波数方向の補正で揃える」という解法の型までがすでに提示されている。したがってCipherFluteの基準笛の新規性は、問題の発見でも周波数方向の正規化という着想でもなく、参照を物体の中に同居させて事前較正を不要にした点に絞って述べる必要がある。日本語の論文誌に載っており、投稿先の読者が知っている可能性が高い。
- 訂正の経緯: この調査の初回の記述は「川崎らは特徴量と学習の側で頑健性を得ようとしている」としていたが、抄録は明確に補正の手法を提案しており、誤りであった。訂正の根拠は上記CiNii Researchの抄録である。

### 11. アクティブ音響センシングによる日常物体識別と位置推定

- 著者: 岩瀬大輝, 伊藤雄一, 秦秀彦, 山下真由, 尾上孝雄（大阪大学大学院情報科学研究科）
- 発表: インタラクション2018論文集（情報処理学会シンポジウムシリーズ）, INT18008, pp. 62-71, 2018年
- 確認先: http://www.interaction-ipsj.org/proceedings/2018/data/pdf/INT18008.pdf （予稿集のPDFを取得し、発表番号、開始ページ62、終了ページ71、要旨に記された98.2パーセント、85.5パーセント、93.8パーセントの3つの数値、および参考文献20件の全体を本文から直接確認した）
- 関連する先行版: 岩瀬大輝, 伊藤雄一, 秦秀彦, 山下真由, 尾上孝雄「アクティブ音響センシングを用いた物体識別と位置推定」電子情報通信学会技術研究報告, 第117巻, 第73号 (MVE2017-1〜13), pp. 135-140, 2017年5月（確認先 https://jglobal.jst.go.jp/detail?JGLOBAL_ID=201702215779835646 。この1件だけはJ-GLOBALの記録によっており、信学技報そのものの目次では確認していない）
- 内容の要約: 面に取り付けたスピーカとマイクの対で掃引信号を流し、面に置かれた日常物体の種類と位置を同時に推定する手法である。りんご、たまねぎ、みかんといった物体を対象に、種類の識別で98.2パーセント、位置の推定で85.5パーセント、両方を合わせた条件で93.8パーセントという結果を報告している。参考文献にRadarCat、Acoustruments、Lumino、Acoustic Barcodes、Touch & Activate、Scratch Input、Stane、SoundWave、Paradisoらの打音追跡などが並んでおり、この分野の日本語での見取り図として有用である。この参考文献一覧は本文を取得して1件ずつ照合したので、後述の背景の節でも確認先として使っている。
- CipherFluteとの関係: 音響で物体そのものを識別するという目的が共通する。ただし物体側は何も加工せず、面の側の電源付き装置がすべてを担うため、CipherFluteとは前提が正反対である。形が情報を固定して保持するという発想はなく、識別できるのは学習済みの数種類である。
- 脅威の度合い: 中
- 理由: 日本のHCI分野におけるこの領域の代表的な仕事であり、投稿先の読者が真っ先に想起する。無電源であることと形に情報を書き込むことの違いを明示して引用すべきである。

### 12. Touch & Activate: Adding Interactivity to Existing Objects Using Active Acoustic Sensing

- 著者: Makoto Ono, Buntarou Shizuki, Jiro Tanaka（筑波大学）
- 発表: Proceedings of the 26th Annual ACM Symposium on User Interface Software and Technology (UIST 2013), pp. 31-40, 2013年（DOI 10.1145/2501988.2501989）
- 確認先: https://api.openalex.org/works/doi:10.1145/2501988.2501989 （抄録を復元し、99.6パーセントと86.3パーセントの2つの数値を確認した）、https://api.crossref.org/works/10.1145/2501988.2501989 （著者3名、収録先、ページ31から40、年を確認した）
- 関連する日本語版: 大野誠, 志築文太郎, 田中二郎「アクティブ音響センシングを用いた把持状態認識」インタラクション2013論文集, 13INT008, pp. 56-63, 2013年（確認先 http://www.interaction-ipsj.org/archives/paper2013/data/Interaction2013/oral/data/pdf/13INT008.pdf 。PDFを取得して英文要旨の数値を直接読んだ）
- 内容の要約: 振動スピーカと圧電マイクを1対だけ既存の物体に貼り付け、物体を伝わる音の変化から触り方や握り方を認識する手法である。抄録には、5種類の触り方で99.6パーセント、6種類の手の姿勢で86.3パーセントという認識精度に加えて、実際の応用の場面では前者が97.8パーセント、後者が71.2パーセントに下がるという数値も記されている。日本語版では、7種類の把持姿勢について個人内で90から99パーセント、利用者をまたぐと66パーセント、3段階の握力について個人内で95から100パーセント、利用者をまたぐと81パーセントという数値を示している。個人内と利用者をまたぐ場合の差が大きい点は、CipherFluteが吹き方の個人差をどう扱うかを論じるうえで参考になる。
- CipherFluteとの関係: 日本におけるアクティブ音響センシングの起点であり、この切り口を語るうえで欠かせない。ただし物体側にスピーカとマイクを貼るため無電源では成立せず、情報量は数種類の状態の判別にとどまる。形が情報を固定して保持するという発想はない。
- 脅威の度合い: 中
- 理由: 分野の起点として引用が必須である。CipherFluteが「物体側に何も貼らず、人の息だけを励振源とする」点を対比の軸として述べる必要がある。

### 13. Itsy-Bits: Fabrication and Recognition of 3D-Printed Tangibles with Small Footprints on Capacitive Touchscreens

- 著者: Martin Schmitz, Florian Müller, Max Mühlhäuser, Jan Riemann, Huy Viet Le
- 発表: Proceedings of the 2021 CHI Conference on Human Factors in Computing Systems (CHI 2021), 記事番号419, pp. 419:1-419:12, 2021年（DOI 10.1145/3411764.3445502）
- 確認先: https://dblp.org/rec/conf/chi/Schmitz0MRL21.html （著者5名、題名、記事番号、ページ、DOIを確認した）、https://api.openalex.org/works/doi:10.1145/3411764.3445502 （抄録を復元して内容を照合した）
- 内容の要約: 静電容量式タッチ画面の上に置くだけで識別できる3Dプリント有体物を、指先ほどの小さな接地面積で実現する製作の流れである。物体の底面に固有の導電性の二次元形状を持たせ、画面が拾う接触点の空間配置からその形状を同定し、種類と位置と向きを推定する。従来手法が高価な部品を要するか、あるいは接地面積が大きくて画面を隠してしまうという問題に対処している。
- CipherFluteとの関係: 「無電源の3Dプリント物体の形そのものがIDを保持し、汎用の読み取り機で読む」という構図がCipherFluteと同型である。音ではなく静電容量を使うという点だけが異なる。物体は完全に無電源である。識別できるのは学習・登録された形状の集合であり、実質的な情報量は数ビットから十数ビットにとどまる。
- 脅威の度合い: 中
- 理由: 「形が情報を固定して保持する無電源タグ」という枠組みが静電容量側でも確立していることを示す。CipherFluteが音を選ぶ理由（読み取り機がマイクだけでよいこと、日用品の内部に隠せること）を明示的に述べる必要がある。

### 14. DuoTouch: Passive Two-Footprint Attachments Using Binary Sequences to Extend Touch Interaction

- 著者: Kaori Ikematsu, Kunihiro Kato
- 発表: Proceedings of the 2026 CHI Conference on Human Factors in Computing Systems (CHI 2026), 記事番号1118, pp. 1118:1-1118:16, 2026年（DOI 10.1145/3772318.3790411）。査読前の版は arXiv:2602.17961 として2026年2月20日に公開されている（DOI 10.48550/arXiv.2602.17961）。
- 確認先: https://dblp.org/search/publ/api?q=DuoTouch+passive+two-footprint&format=json （会議版と査読前の版の2件が登録されていること、記事番号とページ、双方のDOIを確認した）、https://arxiv.org/abs/2602.17961 （題名、著者2名、投稿日、抄録を確認した）
- 内容の要約: 静電容量式タッチパネルに貼る受動の付属物であり、2つの接触点と導電トレースによって動きを二進の系列として符号化する。改造していない機器の標準的なタッチのAPIの上で動作し、固定長の符号を離散的な命令に対応づける配置と、時間差から方向と距離を推定する配置の2通りを用意している。動かす速さ、トレースの幅、標本化の周期が復号の精度にどう効くかを測り、ハンドストラップやスマートフォンのリングホルダといった形への組み込みを示している。
- CipherFluteとの関係: 「受動の付属物の形状に二進系列を書き込み、汎用の読み取り面で読む」という設計がCipherFluteの符号化と同型である。無電源で成立する。情報量は数ビット規模である。両著者はこの方向を継続的に発展させており、池松香はOhmic-Touch（CHI 2018, DOI 10.1145/3173574.3174095、椎尾一郎との共著）とOhmic-Sticker（UIST 2019）を、加藤邦拓は池松香と川原圭博とともにCAPath（Proceedings of the ACM on Human-Computer Interaction, ISS, 2020）を出している。すなわち「同じ著者ら」というより、隣接する2人の研究者がそれぞれの系列を持ち寄って合流した仕事である。
- 脅威の度合い: 中
- 理由: 二進系列を受動物体の形に固定するという発想の直近の到達点であり、日本のヒューマンコンピュータインタラクション分野で継続的に発表している研究者による仕事なので投稿先の読者に近い。引用して、CipherFluteの符号語彙が二値ではなく13値であること、多数の符号語を連ねて128ビットを運ぶ設計であることを差分として述べるべきである。

### 15. Let It Rip! Using Velcro for Acoustic Labeling

- 著者: Tzu-Sheng Kuo, Eric Rawn
- 発表: Adjunct Publication of the 33rd Annual ACM Symposium on User Interface Software and Technology (UIST 2020 Adjunct), pp. 28-30, 2020年（DOI 10.1145/3379350.3416175）
- 確認先: https://api.crossref.org/works/10.1145/3379350.3416175 （収録先の正式名称が Adjunct Publication であること、著者2名、ページ、年を確認した）、https://api.semanticscholar.org/graph/v1/paper/DOI:10.1145/3379350.3416175 （抄録を確認した）
- 内容の要約: 面ファスナーの形を変えることで、剥がしたときに出る音を作り分け、それを標識として使うという初期段階の試作である。二片を引き剥がす動作が励振になり、形の違いが音の違いになる。抄録によれば、音を自動で分類する処理の流れを作り、3種類の基本的な標識からなる組を4組用意して分類器を評価している。すなわち規模は1組あたり3種類であって、扱っている符号の語彙は極めて小さい。
- CipherFluteとの関係: 「無電源の日用素材の形に標識を書き込み、日常動作で鳴らして読む」という発想がCipherFluteと重なる。形が情報を固定して保持するという発想も共有する。ただし初期試作であって情報量の定量的な議論がなく、符号設計も誤り訂正もない。
- 脅威の度合い: 中
- 理由: 概念としては近いが、規模も完成度も小さいため、背景として短く引用すれば足りる。ただし「日常素材で受動音響標識を作る」という発想の存在を示すため、見落とすと弱点になる。

### 16. UTAP: Unique Topographies for Acoustic Propagation: Designing Algorithmic Waveguides for Sensing in Interactive Malleable Interfaces

- 著者: Jan Rod, David Collins, Daniel Wessolek, Thavishi Ilandara, Ye Ai, Hyowon Lee, Suranga Nanayakkara（第4著者の姓は Ilandara であって Illandara ではない。なおTEI 2017のプログラムページは第3著者と第4著者の順序を入れ替えて載せているが、Crossrefに登録された正式な著者順は上のとおりである）
- 発表: Proceedings of the Eleventh International Conference on Tangible, Embedded, and Embodied Interaction (TEI 2017), pp. 141-152, 2017年（DOI 10.1145/3024969.3024987）
- 確認先: https://api.crossref.org/works/10.1145/3024969.3024987 （著者7名の綴りと順序、収録先の正式名称、ページ、年、DOIを確認した）、https://dblp.org/rec/conf/tei/RodCWIALN17.html 、https://tei.acm.org/2017/cp-papers.php （学会のプログラムページで登壇発表と実演発表の両方に載っていることを確認した）
- 内容の要約: 位相の異なる格子状の導波構造をアルゴリズムで生成し、圧電素子と組み合わせることで、柔らかい有体インタフェースの変形を音響信号の変調として検出する手法である。送信側と受信側の導波要素の間の波長を空間的に変えることで、空間領域の擾乱を周波数領域に写像し、利用者が変形させた位置を特定できるようにしている。
- CipherFluteとの関係: 「形状のトポロジを設計して周波数領域に情報を写像する」という設計思想がCipherFluteの語彙設計と重なる。ただし圧電素子で能動的に信号を送るため電源が要り、目的は変形の検出であって情報の保管ではない。
- 脅威の度合い: 中
- 理由: 「形の設計で周波数上の識別可能性を作り込む」という方法論の先例であり、引用して差分を述べるのが望ましい。

### 17. SqueezaPulse: Adding Interactive Input to Fabricated Objects Using Corrugated Tubes and Air Pulses

- 著者: Liang He, Gierad Laput, Eric Brockmeyer, Jon E. Froehlich
- 発表: Proceedings of the Eleventh International Conference on Tangible, Embedded, and Embodied Interaction (TEI 2017), pp. 341-350, 2017年（DOI 10.1145/3024969.3024976）。この調査の初回の記述は「Tenth」としていたが、TEI 2017の収録先の正式名称は「Eleventh」である。
- 確認先: https://api.crossref.org/works/10.1145/3024969.3024976 （収録先の正式名称、著者4名、ページ、年、DOIを確認した）、https://tei.acm.org/2017/cp-papers.php （学会のプログラムページでポスター発表の枠に載っていることを確認した）
- 内容の要約: 柔らかく受動的で安価な蛇腹状の構造を造形物に埋め込み、空洞を握ると空気の脈が柔軟な管を伝わって、固有の形をした波状の管に入り、そこで予測可能な音の特徴に変換される手法である。マイクがこの空気の脈を捉えて識別することで対話性を実現する。
- CipherFluteとの関係: 「空気の流れを受動の形状に通して固有の音を作り、マイクで読む」という機構がCipherFluteの吹鳴と同型である。物体側は完全に無電源である。ただし識別できるのはどの蛇腹が押されたかという数個の状態であり、形が情報を固定して保持するという発想は部分的である。
- 脅威の度合い: 中
- 理由: 「空気で受動構造を鳴らして読む」という機構の先例として引用が要る。ただし情報量が小さく、目的も異なる。

### 18. AirLogic: Embedding Pneumatic Computation and I/O in 3D Models to Fabricate Electronics-Free Interactive Objects

- 著者: Valkyrie Savage, Carlos Tejada, Mengyu Zhong, Raf Ramakers, Daniel Ashbrook, Hyunyoung Kim（第3著者は Mengyu Zhong である。この調査の初回の記述にあった「Menlin Zhong」は誤りであった）
- 発表: Proceedings of the 35th Annual ACM Symposium on User Interface Software and Technology (UIST 2022), 記事番号9, pp. 9:1-9:12, 2022年（DOI 10.1145/3526113.3545642）
- 確認先: https://dblp.org/search/publ/api?q=AirLogic+pneumatic+computation&format=json （著者6名の綴り、記事番号、ページ、DOIを確認した）、https://api.openalex.org/works/doi:10.1145/3526113.3545642 （抄録を復元し、13種類の見本と印刷方向による空気の損失の測定を確認した）
- 内容の要約: 空気による入力、論理演算、出力の部品を3Dプリント可能なモデルに埋め込み、電子回路を一切使わずに対話的な物体を作る手法である。利用者の入力に対して基本的な演算を行い、目に見える、あるいは音として聞こえる、あるいは触って分かる反応を返す。抄録によれば、電子回路も組み立ても要らず、13種類の部品の見本を用意し、印刷方向と内部形状によって空気がどれだけ失われるかを測定し、5つの応用例を示している。
- CipherFluteとの関係: 「電子部品を一切使わない対話的な3Dプリント物体」という価値観がCipherFluteの目指すところと完全に一致する。しかも一部の出力は音である。情報の保管という目的はないが、無電源で成立するという主張の先例として重要である。形が機能を固定して保持するという発想も共有する。
- 脅威の度合い: 中
- 理由: 「無電源の3Dプリント物体で情報処理まで行う」という主張がすでに存在するため、CipherFluteの「電源も電子部品も持たない」という売り文句だけでは差別化にならない。引用して、CipherFluteの独自性が情報の保管と符号設計にあることを明示すべきである。

### 19. Asterisk and Obelisk: Motion Codes for Passive Tagging（検証の過程で「未検証」から昇格させたもの）

- 著者: Aakar Gupta, Jiushan Yang, Ravin Balakrishnan
- 発表: Proceedings of the 31st Annual ACM Symposium on User Interface Software and Technology (UIST 2018), pp. 725-736, 2018年（DOI 10.1145/3242587.3242637）
- 確認先: https://dblp.org/search/publ/api?q=Asterisk+Obelisk+motion+codes+passive+tagging&format=json （著者3名、題名、収録先、ページ、DOIを確認した）、https://api.semanticscholar.org/graph/v1/paper/DOI:10.1145/3242587.3242637 （抄録を確認し、情報量と精度の数値を読んだ）
- 内容の要約: 面に印刷された模様の上を、慣性センサを内蔵した指輪をつけた指でなぞることで、模様に書き込まれた符号を読み出す手法である。指輪が捉えた手の動きの向きの列から符号を復号する。AsteriskとObeliskという2つの符号化方式を作り、模様の向き、大きさ、データの密度が性能にどう効くかを評価している。抄録には、Asteriskが1680万通りの系列という情報容量に対して95パーセントの精度を達成したと明記されている。
- CipherFluteとの関係: タグの側は印刷された模様だけであって完全に無電源であり、「形が符号を固定して保持する」という発想を共有している。重要なのは情報量であって、1680万通りは約24ビットに相当する。すなわち受動タグの系譜のなかで、数ビットから十数ビットという水準を超えて20ビット台に達した例が2018年に存在する。CipherFluteが128ビットを運ぶという主張は依然としてこれを上回るが、「受動タグは少数ビットしか運べない」という単純な対比は成り立たない。ただしAsterisk and Obeliskは音響を使わず、読み出しには慣性センサを内蔵した指輪という専用の装着物が要り、秘密の保管や誤り訂正、基準体による正規化は扱っていない。
- 脅威の度合い: 中
- 理由: 「無電源の受動タグに多ビットの符号を書き込み、日常的な動作で読み出す」という枠組みが、音響ではない経路ですでに24ビット規模で実現されている。CipherFluteの新規性を「受動タグで多ビットを運んだこと」に置くと弱くなるため、音響で運ぶこと、汎用のマイクだけで読めること、秘密分散と組み合わせたことに絞る必要がある。

## 背景として押さえるべき文献

以下は、この切り口の地図を描くうえで背景として引用する価値があるが、CipherFluteの新規性を直接には脅かさないものである。

### 音響で状態や操作を読むもの（物体側に電源が要る、または物体に情報を書き込まない）

- Chris Harrison, Scott E. Hudson「Scratch Input: Creating Large, Inexpensive, Unpowered and Mobile Finger Input Surfaces」UIST 2008, pp. 205-208, DOI 10.1145/1449715.1449747。確認先はインタラクション2018の岩瀬らの論文の参考文献 http://www.interaction-ipsj.org/proceedings/2018/data/pdf/INT18008.pdf である。面をこする音で入力を取る。面は無加工で、情報量は数種類のジェスチャである。
- Roderick Murray-Smith, John Williamson, Stephen Hughes, Torben Quaade「Stane: Synthesized Surfaces for Tactile Input」CHI 2008, pp. 1299-1302, DOI 10.1145/1357054.1357257。同上の参考文献で確認した。表面のテクスチャを設計して、こすったときの音でジェスチャを分ける。形が音を決めるという点でCipherFluteに近いが、情報量は数種類である。
- Sidhant Gupta, Dan Morris, Shwetak Patel, Desney Tan「SoundWave: Using the Doppler Effect to Sense Gestures」CHI 2012, pp. 1911-1914, DOI 10.1145/2207676.2208331。同上の参考文献で確認した。端末のスピーカとマイクだけでジェスチャを取る。物体には何も付けない。
- Joseph A. Paradiso, Che King Leo, Nisha Checka, Kaijen Hsiao「Passive Acoustic Knock Tracking for Interactive Windows」CHI EA 2002, pp. 732-733, DOI 10.1145/506443.506570。同上の参考文献で確認した。叩いた位置を受動的に音で求める。
- Yasha Iravantchi, Yi Zhao, Kenrick Kin, Alanson P. Sample「SAWSense: Using Surface Acoustic Waves for Surface-bound Event Recognition」CHI 2023, 記事番号422, pp. 422:1-422:18, DOI 10.1145/3544548.3580991。確認先は https://dblp.org/search/publ/api?q=SAWSense+surface+acoustic+waves+surface-bound&format=json である。この調査の初回の記述はDOIをAcoustic Barcodesのものと取り違え、確認先として被引用一覧の問い合わせURLを挙げていたので、いずれも訂正した。表面波で面上の事象を分類する。センサ側に電源が要る。
- Carlos E. Tejada, Jess McIntosh, Klaes Alexander Bergen, Sebastian Boring, Daniel Ashbrook, Asier Marzo「EchoTube: Robust Touch Sensing along Flexible Tubes using Waveguided Ultrasound」ACM ISS 2019, DOI 10.1145/3343055.3359712。確認先は https://api.semanticscholar.org/graph/v1/paper/DOI:10.1145/3343055.3359712 であり、抄録で内容を照合した。柔らかい管を導波路として超音波の反射から変形の位置を測る。電子部品を管の片端に集めるという設計であり、装置側に電源が要る。
- Carlos E. Tejada, Raf Ramakers, Sebastian Boring, Daniel Ashbrook「AirTouch: 3D-printed Touch-Sensitive Objects Using Pneumatic Sensing」CHI 2020, DOI 10.1145/3313831.3376136。確認先は https://api.semanticscholar.org/graph/v1/paper/DOI:10.1145/3313831.3376136 である。抄録によれば、最大12箇所の接触点を持つ多様な形状で90パーセント以上の精度を得ており、印刷後の調整を要しない事前学習済みの分類器を使う。3Dプリント物体の空気圧で接触を検出するので物体は無電源だが、圧力センサ側に電源が要る。
- Kristen Grinyer, Robert J. Teather「ClickSense: A Low-Cost Tangible Active User Input Method Using Passive Acoustic Sensing for Mobile Virtual Reality」CHI EA 2025, DOI 10.1145/3706599.3720000。確認先は https://api.semanticscholar.org/graph/v1/paper/DOI:10.1145/3706599.3720000 である。抄録によれば、家庭にある材料で作った手持ちの器具のクリック音を端末のマイクで識別し、単独で使うと97.33パーセント、通常の選択操作のなかでは95.05パーセントの認識率を得ている。受動音響で仮想現実の選択操作を取る。
- Gierad Laput, Karan Ahuja, Mayank Goel, Chris Harrison「Ubicoustics: Plug-and-Play Acoustic Activity Recognition」UIST 2018, DOI 10.1145/3242587.3242609。確認先は https://www.figlab.com/research/2018/ubicoustics である。環境音を分類する。物体には何も付けない。
- Gierad Laput, Yang Zhang, Chris Harrison「Synthetic Sensors: Towards General-Purpose Sensing」CHI 2017, pp. 3986-3999, DOI 10.1145/3025453.3025773。確認先は https://dblp.org/rec/conf/chi/LaputZH17.html である。部屋に1個の多機能センサを置いて周囲の文脈を推定する。
- Yang Zhang, Gierad Laput, Chris Harrison「Vibrosight: Long-Range Vibrometry for Smart Environment Sensing」UIST 2018, DOI 10.1145/3242587.3242608。確認先は https://www.figlab.com/research/2018/vibrosight である。受動の反射シールを物体に貼り、レーザ振動計で遠くから振動を読む。シール自体は無電源だが、情報量は活動の分類である。
- Jason Wu, Chris Harrison, Jeffrey P. Bigham, Gierad Laput「Automated Class Discovery and One-Shot Interactions for Acoustic Activity Recognition」CHI 2020, DOI 10.1145/3313831.3376875。確認先は https://api.semanticscholar.org/graph/v1/paper/DOI:10.1145/3313831.3376875 である。題名の先頭の語は Automated であって Automatic ではない。この調査の初回の記述は Automatic としていたので訂正した。系の名称はListen Learnerである。
- Dhruv Jain, Hung Ngo, Pratyush Patel, Steven Goodman, Leah Findlater, Jon Froehlich「SoundWatch: Exploring Smartwatch-based Deep Learning Approaches to Support Sound Awareness for Deaf and Hard of Hearing Users」ASSETS 2020, DOI 10.1145/3373625.3416991。確認先は https://api.semanticscholar.org/graph/v1/paper/DOI:10.1145/3373625.3416991 である。抄録によれば、20種類の音を平均81.2パーセント、優先度の高い3種類を97.6パーセントで分類する。
- Gierad Laput, Xiang 'Anthony' Chen, Chris Harrison「SweepSense: Ad Hoc Configuration Sensing Using Reflected Swept-Frequency Ultrasonics」IUI 2016, pp. 332-335, DOI 10.1145/2856767.2856812。確認先は https://dblp.org/search/publ/api?q=SweepSense+configuration+sensing+swept+frequency+ultrasonics&format=json である。この調査の初回の記述が挙げていた著者本人のPDFのURLは現在404を返すので、確認先を差し替えたうえでページとDOIを補った。
- Yasha Iravantchi, Karan Ahuja, Mayank Goel, Chris Harrison, Alanson Sample「PrivacyMic: Utilizing Inaudible Frequencies for Privacy Preserving Daily Activity Recognition」CHI 2021, DOI 10.1145/3411764.3445169。確認先は https://api.semanticscholar.org/graph/v1/paper/DOI:10.1145/3411764.3445169 である。抄録によれば、家庭と職場の127個の物体から出る音を調べ、可聴域と音声の帯域を落とした録音でも95パーセントを超える分類精度を得ている。
- Shengze Zhong, Parinya Punpongsanon, Daisuke Iwai, Kosuke Sato「Estimation of fused-filament-fabrication structural vibro-acoustic performance by modal impact sound」Computers & Graphics, Vol. 115, pp. 137-147, 2023年7月（DOI 10.1016/j.cag.2023.07.010）。確認先は https://researchmap.jp/daisukeiwai/published_papers/42866887 であり、著者4名の順序、巻、ページ、年、DOIを確認した。3Dプリント構造の振動音響特性をマイク1本の打音から推定する。CipherFluteの較正の方法論と関係する。
- 渡邉拓貴「モバイル/ウェアラブルデバイスにおけるアクティブ音響センシングの最前線」日本音響学会誌, 第80巻, 第9号, pp. 523-527, 2024年9月1日（DOI 10.20697/jasj.80.9_523）。確認先は https://cir.nii.ac.jp/crid/1390020209538449920 である。日本語の総説であり、この分野の見取り図として引用できる。
- 小西智樹, 崔明根, 雨坂宇宙, 志築文太郎「ドアノブの握り方に基づくアクティブ音響センシングを用いた個人認証システムの検討」情報処理学会研究報告 2024-HCI-209, 2024年。確認先は https://cir.nii.ac.jp/crid/1010025255259071745 である。この調査の初回の記述は著者を「雨坂宇宙, 志築文太郎」の2名としていたが、実際には4名の共著であり雨坂宇宙は第3著者であった。訂正した。
- 雨坂宇宙, 志築文太郎「アクティブ音響センシングを用いたズボンのポケットに対するジェスチャ認識」情報処理学会研究報告 2025-HCI-212, 2025年。確認先は https://cir.nii.ac.jp/all?q=%E9%9B%A8%E5%9D%82%E5%AE%87%E5%AE%99%20%E5%BF%97%E7%AD%91%E6%96%87%E5%A4%AA%E9%83%8E である。著者2名を確認した。いずれも情報処理学会ヒューマンコンピュータインタラクション研究会での継続的な発表である。なお両件ともページ番号はCiNii Researchの記録に載っていないため補えていない。
- 立花巧樹, 松田裕貴, 磯部海斗, 真弓大輝, 諏訪博彦, 安本慶一, 村尾和哉「アクティブ音響センシングによるポイ捨てごみの種別認識手法の提案」マルチメディア，分散，協調とモバイル（DICOMO2022）シンポジウム論文集, pp. 258-264, 2022年7月6日。確認先は https://cir.nii.ac.jp/crid/1050011771467529088 である。
- 高橋大輝, 村尾和哉「アクティブ音響センシングを用いた卵と肉の加熱状況識別手法」DICOMO2023シンポジウム論文集, pp. 758-767, 2023年6月28日。確認先はCiNii Researchで題名を検索した結果であり、著者2名、ページ、年を確認した。
- 佐々木啓人, 渡邉拓貴, 寺田努, 塚本昌彦「板状ゲルへのアクティブ音響センシングによる押下位置・圧力・せん断力同時認識手法の提案」DICOMO2022シンポジウム論文集, pp. 247-257, 2022年7月6日。確認先は https://cir.nii.ac.jp/crid/1050011771467304704 である。この3件はいずれも著者名をCiNii Researchで1件ずつ確認して補った。立花らの仕事は奈良先端科学技術大学院大学と村尾和哉の系列の共同であり、佐々木らの仕事は神戸大学の寺田努と塚本昌彦の系列であって、村尾和哉の研究室とは別である。日本におけるこの系統の広がりを示す。

### 静電容量、電磁、レーダで物体や触り方を読むもの

- Munehiko Sato, Ivan Poupyrev, Chris Harrison「Touché: Enhancing Touch Interaction on Humans, Screens, Liquids, and Everyday Objects」CHI 2012, pp. 483-492。確認先は https://la.disneyresearch.com/publication/touche-enhancing-touch-interaction-on-humans-screens-liquids-and-everyday-objects/ であり、ページ番号はインタラクション2013の大野らの論文の参考文献[13] http://www.interaction-ipsj.org/archives/paper2013/data/Interaction2013/oral/data/pdf/13INT008.pdf の本文から確認して補った。掃引周波数静電容量センシングにより、触り方の複雑な構成を判別する。対象側に電極を付ける必要がある。
- Chris Harrison, Munehiko Sato, Ivan Poupyrev「Capacitive Fingerprinting: Exploring User Differentiation by Sensing Electrical Properties of the Human Body」UIST 2012, pp. 537-544, DOI 10.1145/2380116.2380183。確認先は https://api.semanticscholar.org/graph/v1/paper/DOI:10.1145/2380116.2380183 であり、著者3名と順序を確認した。人の電気的性質で利用者を区別する。
- Hui-Shyong Yeo, Gergely Flamich, Patrick Schrempf, David Harris-Birtill, Aaron Quigley「RadarCat: Radar Categorization for Input and Interaction」UIST 2016, pp. 833-841, DOI 10.1145/2984511.2984515。確認先は https://api.openalex.org/works/doi:10.1145/2984511.2984515 であり、抄録を復元して確認した。抄録は3つの実験を述べており、複合物体を含む26種類の材質、厚みと染料が異なる16種類の透明素材、6名の10箇所の身体部位を分類している。物体は無加工かつ無電源だが、読み取り側にレーダが要る。形が情報を保持するという発想はない。加えて、この書誌はインタラクション2018の岩瀬らの論文の参考文献[1]にも載っている。
- Jun Gong, Yu Wu, Lei Yan, Teddy Seyed, Xing-Dong Yang「Tessutivo: Contextual Interactions on Interactive Fabrics with Inductive Sensing」UIST 2019, DOI 10.1145/3332165.3347897。確認先は https://api.semanticscholar.org/graph/v1/paper/DOI:10.1145/3332165.3347897 である。抄録によれば、導電性の糸で作った6行6列の渦巻き状のコイルを多層の布地に仕込み、鍵や硬貨や電子機器といった身のまわりの導電性の物体27種類を10名の参加者による実験で識別し、実時間で93.9パーセントの精度を得ている。ここは訂正が要る点であって、識別の対象は設計されたタグではなく、もともと家庭や職場にある普通の導電性の物体である。したがって「標識は無電源で形が情報を保持する」という初回の記述は誤りであり、削った。CipherFluteのように情報を書き込んだタグを読む研究ではなく、既存の物体を材質と形から当てる研究である。
- Martin Schmitz, Mohammadreza Khalilbeigi, Matthias Balwierz, Roman Lissermann, Max Mühlhäuser, Jürgen Steimle「Capricate: A Fabrication Pipeline to Design and 3D Print Capacitive Touch Sensors for Interactive Objects」UIST 2015, pp. 253-258, DOI 10.1145/2807442.2807503。確認先は https://api.semanticscholar.org/graph/v1/paper/DOI:10.1145/2807442.2807503 であり、著者6名を確認した。導電フィラメントで静電容量センサを3Dプリントに埋め込む。読み出しには電子回路が要る。
- Martin Schmitz, Martin Stitz, Florian Müller, Markus Funk, Max Mühlhäuser「./trilaterate: A Fabrication Pipeline to Design and 3D Print Hover-, Touch-, and Force-Sensitive Objects」CHI 2019, DOI 10.1145/3290605.3300684。確認先は https://api.semanticscholar.org/graph/v1/paper/DOI:10.1145/3290605.3300684 であり、著者5名を確認して初回の「Martin Schmitzほか」を埋めた。題名の先頭に「./」が付くのが正式な表記である。三点測量の考え方で静電容量から指の3次元位置を推定する。
- Kunihiro Kato, Kaori Ikematsu, Yoshihiro Kawahara「CAPath: 3D-Printed Interfaces with Conductive Points in Grid Layout to Extend Capacitive Touch Inputs」Proceedings of the ACM on Human-Computer Interaction, Vol. 4, ISS, pp. 1-17, 2020年, DOI 10.1145/3427321。確認先は https://api.semanticscholar.org/graph/v1/paper/DOI:10.1145/3427321 であり、著者3名と巻とページを確認して初回の「Kunihiro Katoほか」を埋めた。無電源の3Dプリント物体を静電容量画面で読む。
- Kaori Ikematsu, Masaaki Fukumoto, Itiro Siio「Ohmic-Sticker: Force-to-Motion Type Input Device that Extends Capacitive Touch Surface」UIST 2019, DOI 10.1145/3332165.3347903。確認先は https://api.semanticscholar.org/graph/v1/paper/DOI:10.1145/3332165.3347903 であり、著者3名と抄録を確認した。抄録は電池を要しないことを述べているが、「厚み2ミリメートル未満」という数値は抄録では確認できなかったので、この寸法を論文で引く場合は原文にあたってほしい。関連して同じ第一著者のOhmic-Touchは Kaori Ikematsu, Itiro Siio によるCHI 2018の論文（pp. 1-8, DOI 10.1145/3173574.3174095）であり、確認先は https://api.crossref.org/works?query.bibliographic=Ohmic-Touch+Extending+Touch+Interaction+Indirect+Touch+Resistive+Objects+Ikematsu である。
- Simon Voelker, Kosuke Nakajima, Christian Thoresen, Yuichi Itoh, Kjell Ivar Øvergård, Jan Borchers「PUCs: Detecting Transparent, Passive Untouched Capacitive Widgets on Unmodified Multi-touch Displays」ITS 2013, pp. 101-104, DOI 10.1145/2512349.2512791。同じ著者らによる実演発表がITS 2013の予稿集追補（pp. 325-328, DOI 10.1145/2512349.2514595）とUIST 2013の予稿集追補（pp. 1-2, DOI 10.1145/2508468.2514926）にそれぞれある。確認先は https://hci.rwth-aachen.de/pucs （研究室のページで3件の書誌を確認した）および https://dblp.org/search/publ/api?q=PUCs+detecting+transparent+passive+untouched+capacitive+widgets&format=json である。電源不要、透明、非接触でも検出できる受動の有体物である。
- Rafael Morales González, Caroline Appert, Gilles Bailly, Emmanuel Pietriga「TouchTokens: Guiding Touch Patterns with Passive Tokens」CHI 2016, pp. 4189-4202, DOI 10.1145/2858036.2858041。確認先は https://api.openalex.org/works/doi:10.1145/2858036.2858041 であり、抄録を復元して「95パーセントを超える精度」という記述とページを確認した。初回の記述が挙げていたHALのURLは現在アクセス制御で内容が取れないため、確認先を差し替えた。受動の駒の形が指の配置を拘束し、その接触模様から駒を識別する。形が情報を保持するという発想を共有する。
- Minto Funakoshi, Shun Fujita, Kaori Minawa, Buntarou Shizuki「SilverCodes: Thin, Flexible, and Single-Line Connected Identifiers Inputted by Swiping with a Finger」HCI International 2020, LNCS 12182, pp. 350-362, Springer, DOI 10.1007/978-3-030-49062-1_24。確認先は https://www.iplab.cs.tsukuba.ac.jp/~funakoshi/ （著者本人の業績ページ。著者4名の綴り、巻、ページを確認した）である。導電インクで印刷した識別子を指でなぞって読む。なお「平均95.3パーセントの認識精度」という数値は、著者本人の業績ページにも、Semantic ScholarとOpenAlexの記録にも見当たらず裏が取れなかった。論文で引く場合は原文で確認してほしい。
- Valkyrie Savage, Colin Chang, Björn Hartmann「Sauron: Embedded Single-Camera Sensing of Printed Physical User Interfaces」UIST 2013, DOI 10.1145/2501988.2501992。確認先は https://api.semanticscholar.org/graph/v1/paper/DOI:10.1145/2501988.2501992 であり、著者3名と抄録を確認した。3Dプリント物体の内部を、環状の照明を組み込んだカメラ1台で観測する。鏡の配置と内部形状を計算して、操作部品がカメラに見えるようにしている。物体側に電源が要る。
- 瀬崎夕陽, 関口祐豊, 中村聡史（明治大学）「溝間隔の違いによる筆圧変化を活用したシート埋め込み型ID認識手法」WISS 2025（登壇発表の発表番号23。実演発表としても発表番号3-A07で載っている）。確認先は https://www.wiss.org/WISS2025Proceedings/ であり、著者3名と発表番号を予稿集の目次で確認して初回の「瀬崎夕陽ほか」を埋めた。溝の間隔という形状にIDを固定するという点でAcoustic Barcodesと同型の発想を、日本のインタラクション分野で最近扱っている。
- 林吉経, 尾崎亮太, 上堀まい（青山学院大学および日本学術振興会）, 岩本涼, 菊地萌花, 石黒成紀（大建工業株式会社）, 伊藤雄一（青山学院大学）「棒の引っかきによる音波を用いたインタラクション取得手法の検討」WISS 2025（実演発表の発表番号1-C30）。確認先は同上であり、著者7名を予稿集の目次で確認して初回の「林吉経ほか」を埋めた。棒を引っかいたときの音波でインタラクションを取るという着想はAcoustic Barcodesの系譜に連なり、しかも伊藤雄一の研究室の仕事であるから、CipherFluteの投稿先の読者と近い位置にある。

## 検証で書誌が確定したもの（初回は「未検証」に置かれていた文献）

2026年7月30日の検証で、初回に未検証として保留されていた文献の書誌をCrossref、DataCite、OpenAlex、dblpの各機械可読な問い合わせ先で確定させた。以下はその結果である。

- Chang Xiao, Karl Bayer, Changxi Zheng, Shree K. Nayar「Vidgets: Modular Mechanical Widgets for Mobile Devices」ACM Transactions on Graphics, Vol. 38, No. 4, 記事番号101, pp. 1-12, 2019年（SIGGRAPH 2019, DOI 10.1145/3306346.3322943）。確認先は https://api.crossref.org/works/10.1145/3306346.3322943 および https://www.cs.columbia.edu/cg/vidgets/ である。押しボタンと回転つまみという受動の機械部品を携帯端末に取り付け、操作したときに生じる加速度の変化を端末の加速度計で読み取る手法である。力の掛かり方の設計に物理モデルを用い、実時間の信号処理で識別する。CipherFluteとの関係では、無電源の受動部品の形が読み取れる信号を決めるという点が共通するが、読み取るのは慣性センサであってマイクではなく、情報量は部品の種類の判別にとどまる。脅威の度合いは低である。理由は、音響ではないこと、情報の保管という目的を持たないことである。
- Peiyu Zhang, Wen Ying, Sara L. Riggs, Seongkook Heo「MoiréTag: A Low-Cost Tag for High-Precision Tangible Interactions without Active Components」Proceedings of the ACM on Human-Computer Interaction, Vol. 8, ISS, pp. 1-19, 2024年（DOI 10.1145/3698113）。確認先は https://api.crossref.org/works?query.bibliographic=MoireTag+low-cost+tag+high-precision+tangible+interactions+without+active+components である。初回の記述は第3著者を「Sarah Riggs」としていたが、正しくは「Sara L. Riggs」である。訂正した。能動部品を一切持たない受動タグという点でCipherFluteと発想を共有する。脅威の度合いは低である。理由は、モアレという光学の効果を使うため読み取りに撮像が要り、目的が高精度の位置検出であって情報の保管ではないことである。
- Daniel Campos Zamora, Mustafa Doga Dogan, Alexa F. Siu, Eunyee Koh, Chang Xiao「MoiréWidgets: High-Precision, Passive Tangible Interfaces via Moiré Effect」CHI 2024（DOI 10.1145/3613904.3642734）。確認先は https://api.semanticscholar.org/graph/v1/paper/DOI:10.1145/3613904.3642734 であり、著者5名と抄録を確認した。初回の記述の著者名と題名はいずれも正しかった。3Dプリントした2層の模様のずれで、ボタンや滑り子や回転子の操作を距離100センチメートルでも1ミリメートル未満の精度で検出する。電子部品を持たない。脅威の度合いは低である。理由はMoiréTagと同じである。
- Ethan Kepros, Premjeet Chahal「Ultralow Power Wireless Ultrasonic Sensor Tag With ID」IEEE Sensors Journal, Vol. 25, No. 5, pp. 8823-8827, 2025年（DOI 10.1109/JSEN.2025.3529891）。確認先は https://api.crossref.org/works?query.bibliographic=Ultralow+Power+Wireless+Ultrasonic+Sensor+Tag+With+ID+Kepros+Chahal である。識別子を持つ超音波センサタグという点でSoundOffの周辺にあたる。脅威の度合いは低である。理由は、極低電力とはいえ電源を要する能動タグであり、CipherFluteの無電源という前提とは異なることである。
- Yanling Zhou, Jun Fan, Jinfeng Huang, Bin Wang「Passive Underwater Acoustic Barcodes Using Rayleigh Wave Resonance」Journal of Applied Physics, Vol. 131, No. 12, 記事番号124901, 2022年（DOI 10.1063/5.0086290）。確認先は https://api.crossref.org/works?query.bibliographic=Passive+underwater+acoustic+barcodes+using+Rayleigh+wave+resonance である。初回は2021年とする記述と2022年とする記述が混在していたが、Crossrefの記録では2022年で確定した。水中で受動の音響バーコードを読むという内容であり、幾何形状が共鳴周波数を決めるという物理原理はCipherFluteと同じ系統である。脅威の度合いは低である。理由は、応用が水中音響であってヒューマンコンピュータインタラクションの文脈を持たず、情報の保管や秘密分散との組合せを扱っていないことである。ただし物理原理が近いので、CipherFluteの原理の一般性を示す傍証として引用する値打ちはある。
- Aakar Gupta, Jiushan Yang, Ravin Balakrishnan「Asterisk and Obelisk: Motion Codes for Passive Tagging」UIST 2018については、書誌に加えて情報量の数値まで確定できたので、上の「新規性への脅威が大きい文献」の第19項に移した。

## 未検証のまま残ったもの

以下は、書誌そのものは確定したが、内容についての個別の主張の裏が取れなかったものである。本文で数値や事実に言及する場合は改めて原文にあたる必要がある。

- Acoustic Voxelsが「4ビットの二進データを検出できる」という記述は、報道記事（https://phys.org/news/2016-07-acoustic-voxels-embed.html など）に由来する。OpenAlexで抄録を復元して確かめたところ、抄録には「知覚されない音響情報を日用品に埋め込む」という応用の記述はあるが、ビット数はまったく書かれていなかった。同じ研究室のAirCodeの記述と混同している可能性があるため、論文本文で確認するまでこの数値は使わないほうがよい。
- SoundOffのタグの素材（ステンレス鋼かどうか）と寸法（硬貨より小さいかどうか）、および励振の機構（タグが弾かれるのかどうか）は、抄録には書かれていなかった。NSFの公開リポジトリは本文の公開を2026年12月2日まで留保しているため、原文で確認できていない。
- SilverCodesの「平均95.3パーセントの認識精度」という数値は、著者本人の業績ページ、Semantic Scholar、OpenAlexのいずれにも見当たらなかった。
- Ohmic-Stickerの「厚み2ミリメートル未満」という寸法は、抄録では確認できなかった。
- ProtoHoleについて、スピーカとマイクを物体の内部に入れるのかどうか、および応用例として操縦桿や照明の操作器や玩具の犬を実装したのかどうかは、抄録では確認できなかった。
- Acoustic Barcodesが1個のバーコードで運ぶビット数は、著者本人のプロジェクトページにも抄録にも明示されていない。
- Blowholeについて、1つの模型に埋め込める空洞の個数、および空洞1個あたりの実効的なビット数は、抄録には書かれていない。
- 岩瀬らの信学技報の先行版（第117巻第73号, pp. 135-140, 2017年5月）は、J-GLOBALの記録によってのみ確認しており、電子情報通信学会の技術研究報告そのものの目次では照合していない。
- 雨坂宇宙らの情報処理学会研究報告2件（2024-HCI-209および2025-HCI-212）のページ番号は、CiNii Researchの記録に載っていないため補えていない。
- ACM Digital Libraryの本文ページはこの調査環境からは403で取得できなかった。ただしCrossref、OpenAlex、Semantic Scholarの各問い合わせ先から抄録を取得できたため、初回に「原文で確認できていない」とされていた数値のうち、FabAuthの92.2パーセント、Touch & Activateの99.6パーセントと86.3パーセント、SoundWatchの81.2パーセント、Tessutivoの93.9パーセント、TouchTokensの95パーセント超、SoundOffの「数千通りの設計」については抄録で裏が取れた。取れなかったものは上に列挙したとおりである。

## この切り口で見つからなかったこと

以下は、丁寧に探したうえで「存在しない、あるいは少なくとも主要な会議・雑誌には見当たらない」と言えることである。CipherFluteの新規性の主張の根拠になる。

第一に、無電源で受動的な音響物体に、暗号鍵やリカバリーシードのような多ビットの秘密を格納し、それを吹鳴などの日常動作で読み出すという研究は見つからなかった。受動音響タグの系譜（Acoustic Barcodes、Lamello、Acoustruments、SqueezaPulse、Let It Rip、Blowhole、SoundOff）はいずれも識別子の付与かイベントの検出が目的である。128ビット級の情報を運ぶために符号語を連ねるという設計は、この系譜には存在しない。ただし搬送する情報量については書き方に注意が要る。「数ビットから十数ビットにとどまる」という言明は、Acoustic Barcodes、Blowhole、Lamelloのいずれについても原典に明示のビット数がなく、この調査の推測にすぎない。またAsterisk and Obelisk（UIST 2018）は音響ではないものの受動タグで約24ビットを達成しているので、受動タグ一般に対する情報量の上限のような主張はできない。原典に数値がないことを踏まえ、「既存の受動音響タグは1個あたり数ビット相当の識別子を担う設計にとどまり、符号語を連ねて128ビットに届かせる設計は見当たらない」という言い方が安全である。

第二に、受動音響タグに誤り訂正符号を組み合わせた研究は見つからなかった。Reed-Solomon符号どころか、単純なパリティや繰り返し符号を音響タグに導入した例も見当たらなかった。既存研究は分類器の精度を上げることで信頼性を確保しており、符号理論の道具を持ち込んでいない。ただし「符号化方式を設計する」という行為そのものはLamelloの抄録が貢献として明示しているので、符号設計が前例のない行為であるとは書かないほうがよい。差分は誤り訂正の導入にある。

第三に、隣り合う符号が同じ値にならないという遷移保証の制約（8B/10B符号と同じ狙い）を、物理的な受動タグの設計に課した研究は見つからなかった。

第四に、音高が既知の「基準体」を同じ物体の中に同居させ、他の符号をその比で読むというパイロット信号型の正規化は、受動音響タグの文献には見つからなかった。ただしここは検証で記述を改めた箇所である。川崎ら（情報処理学会論文誌2021）は温度変動への対処という問題を扱っているだけでなく、周波数方向と振幅方向に周波数特性を補正して基準温度における特性に揃えるという解法を提案している。すなわち「周波数軸を正規化してずれを打ち消す」という着想はすでに存在する。CipherFluteの差分は、参照を事前の温度別の測定に置くのではなく、既知の音高を持つ基準体を同じ物体の中に作り込み、読み出しのその場で相対値を取ることによって事前較正を不要にした点にある。この点に絞って書くべきである。

第五に、音響を用いたPhysical Unclonable Functionは見つからなかった。光学、電気、化学を用いたPUFは多数存在するが、音響のものは検索の範囲では確認できなかった。裏返せば、CipherFluteが「音や物体の層には暗号学的な秘匿の力はまったく無い」と宣言していることは、既存研究の実態とも整合する。

第六に、3Dプリントしたフィップル笛（歌口とラビウムを持つ、リコーダー型の発音体）を情報記録の媒体として使う研究は見つからなかった。Printoneは自由形状の管楽器の設計手法であって情報を運ばない。Blowholeはヘルムホルツ共鳴の空洞であって管長で音高を決める笛ではない。円筒を軸方向に半分に割った断面の小型フィップル笛を複数本融合し、それぞれの管長を符号のスロットに割り当てるという設計は、この切り口では前例が見当たらなかった。

第七に、静電容量の側にも、無電源のタグが多ビットの秘密を保持する研究は見つからなかった。Itsy-Bits、CAPath、DuoTouch、TouchTokens、PUCsはいずれも識別子の規模が小さく、秘密保持や脅威モデルの議論を持たない。ただし秘密保持を目的としないタグの情報容量に限れば、Asterisk and Obeliskが約24ビットに達しているので、「無電源タグの情報量はどれも小さい」という書き方は避けるべきである。正確には、無電源タグに多ビットの情報を載せる技術は存在するが、それを秘密の保管という目的に向け、秘密分散と脅威モデルの議論を伴わせた研究が見当たらないということである。

第八に、日本国内の情報処理学会ヒューマンコンピュータインタラクション研究会、ユビキタスコンピューティングシステム研究会、インタラクション、WISSのいずれにも、3Dプリントの笛と暗号鍵の保管を結びつけた研究は見当たらなかった。CiNii Researchで「3Dプリンタ 笛 音響」「音響タグ 物体識別」「音響 パッシブタグ 識別 インタラクション」を検索したところ、いずれも0件であった。ただしWISS 2025には、溝の間隔という形状にIDを固定する瀬崎らの発表と、棒の引っかき音を使う林らの発表があり、いずれも形と音を情報に結びつける発想を扱っている。CipherFluteとの距離は近いので、投稿先の読者が想起する可能性を踏まえて言及しておくのが安全である。

## 調べ残した穴

以下は時間の都合で追い切れなかった方向である。

第一に、ACM Digital Libraryの本文ページがこの環境から403で取得できなかったため、Blowhole、SoundOff、FabAuth、Acoustic Barcodesの各論文の「実効的なビット数」「区別できるスロット数」「読み取りの誤り率」といった、CipherFluteと直接比較したい数値を原文で確認できていない。ただし2026年7月30日の検証で、Crossref、OpenAlex、Semantic Scholarの機械可読な問い合わせ先から抄録を取得できることが分かり、FabAuthの92.2パーセントをはじめ多くの数値の裏が取れた。それでも1個のタグや1個の空洞あたりのビット数は、どの抄録にも書かれていない。特にSoundOffが述べる「数千通りの設計」が1個のタグあたり何ビットに相当するのかは、差分を述べるうえで重要なので本文で確認すべきである。SoundOffの本文はNSFの公開リポジトリでは2026年12月2日まで公開が留保されているので、それまではACM Digital Libraryの購読経由で見るしかない。

第二に、Semantic Scholarの応答制限により、Acoustic VoxelsとPrintoneとSoundOffの被引用をたどり切れていない。とりわけSoundOffは2025年末の出版なので、その後続を確認できていない。

第三に、電子情報通信学会の技術研究報告については、J-GLOBAL経由で岩瀬らの1件しか押さえられていない。信学技報のマルチメディア・仮想環境基礎研究会、ヒューマンコミュニケーション基礎研究会、応用音響研究会、およびヒューマンコミュニケーショングループのシンポジウムを横断的に見ていない。

第四に、情報処理学会電子図書館（情報学広場）はWebFetchで検索結果の本体が取得できず、ヒューマンコンピュータインタラクション研究会とユビキタスコンピューティングシステム研究会の個別の発表を網羅できていない。CiNii Researchで拾える範囲にとどまっている。

第五に、受動の超音波タグや表面弾性波タグについて、計測工学やセンサ工学の分野（IEEE Sensors Journal、Sensors誌など）の文献をほとんど見ていない。SoundOffの周辺にこの系譜が厚く存在する可能性が高い。

第六に、楽器音響学の一次文献を押さえていない。CipherFluteが用いるf = A/(L+e)という近似は開管の端部補正の標準的な扱いであり、フィップル笛の管長と基音の関係については音響学側に長い先行がある。新規性の主張には直接影響しないが、較正手法の位置づけを述べるうえで確認しておくべきである。

第七に、水中音響やソナーの分野における受動音響バーコードの系譜については、2026年7月30日の検証でZhouらの書誌（Journal of Applied Physics, Vol. 131, No. 12, 記事番号124901, 2022年, DOI 10.1063/5.0086290）が確定した。ただしこの1件の周辺、すなわちRayleigh波共鳴を用いた受動タグの系譜そのものは追えていない。物理原理はCipherFluteと近いので、確認する価値がある。

## 検証で削除したもの

明らかに存在しない文献として削除したものは1件もない。この文書に挙げられていた文献は、書誌のうえではすべて実在が確認できた。削除したのは文献そのものではなく、文献の内容についての誤った記述と、その論文の著者ではない人物の氏名1件である。具体的には次のとおりである。なお、綴りだけを直した著者名の訂正6件は、削除ではなく訂正として上の各項目に書き込んであり、この節には挙げていない。

- Acoustrumentsの著者一覧から Mary Mahler を削除した。Mary Mahler は実在の研究者であり、同じ研究陣がSIGGRAPH 2015のEmerging Technologiesで出した実演発表の版の著者である。しかしCHI 2015の論文の著者ではないので、CHI 2015の書誌としては誤りであった。削除の根拠は、Disney Researchのページに載っている著者一覧とSemantic Scholarの記録である。実演発表の版の書誌は、取り違えを避けるために当該項目の注記として残した。
- SoundOffの内容の要約から、「硬貨より小さい」という寸法、「ステンレス鋼を特定の形に切り出す」という素材、「タグが弾かれる」という励振の機構、「板状金属の曲げ振動」という振動の型の4点を削除した。いずれも抄録に根拠が見当たらず、裏が取れなかった。
- ProtoHoleの内容の要約から、「物体の内部にスピーカとマイクを入れる」という構成と、「操縦桿、照明の操作器、玩具の犬を例として実装している」という応用例を削除した。いずれも抄録に根拠が見当たらなかった。
- Tessutivoの説明から、「導電性の標識」を識別するという記述と「標識は無電源で形が情報を保持する」という評価を削除した。抄録が述べているのは、鍵や硬貨や電子機器といった身のまわりの普通の導電性の物体27種類を識別することであって、設計されたタグを読むことではない。CipherFluteとの関係の評価が根本的に変わる誤りであった。

## 検証の記録

2026年7月30日に、この文書の書誌情報と内容の記述について、執筆者とは別の担当者が独立に検証を行った。

検証した文献は合わせて62件である。内訳は、「新規性への脅威が大きい文献」の節にあった18件、その節に関連版として併記されていた2件（岩瀬らの信学技報版と大野らのインタラクション2013版）、「背景として押さえるべき文献」の節にあった36件、「未検証のまま残ったもの」の節にあった6件である。このうち、著者名、題名、発表した会議名または雑誌名、年、巻号やページ、DOIのいずれかについて一次情報にあたって照合できたものが62件すべてであり、実在が確認できなかった文献は1件もなかった。照合には、dblpの publ API、Crossref の works API、DataCite の DOI API、OpenAlex の works API、Semantic Scholar の graph API、CiNii Research、著者本人または所属研究室の業績ページ、学会の予稿集のPDF、NSFの公開リポジトリ、arXivを用いた。日本語の文献については、CiNii Researchで題名を検索したうえで各文献の記録を個別に開いて確認し、インタラクション2013とインタラクション2018の予稿集についてはPDFそのものを取得して本文と参考文献一覧を読んだ。WISS 2025については学会の予稿集の目次を開いて著者名と発表番号を確認した。内容の記述については、可能なかぎりOpenAlexで抄録を復元するか、Semantic ScholarとCrossrefの抄録を取得して照合した。

訂正した箇所は、性質ごとに数えると次のようになる。合計で60箇所を超える。

第一に、明らかな誤りの訂正が16件である。うち著者名の誤りが7件であって、Acoustrumentsの著者一覧に Mary Mahler が入っていたもの、AirLogicの第3著者を「Menlin Zhong」としていたもの（正しくは Mengyu Zhong である）、UTAPの第4著者を「Thavishi Illandara」としていたもの（正しくは Thavishi Ilandara である）、MoiréTagの第3著者を「Sarah Riggs」としていたもの（正しくは Sara L. Riggs である）、Blowholeの第一著者を「Carlos E. Tejada」としていたもの（dblpとDataCiteのいずれも「Carlos Tejada」である）、SoundOffの第3著者を「Víctor Riera-Naranjo」としていたもの（一次情報の表記は「Víctor Riera Naranjo」である）、そしてドアノブの握り方による個人認証の研究の著者を「雨坂宇宙, 志築文太郎」の2名としていたもの（実際には小西智樹、崔明根、雨坂宇宙、志築文太郎の4名の共著であり、雨坂宇宙は第3著者である）である。題名の誤りが2件であって、「Automatic Class Discovery」を正しい「Automated Class Discovery」に直し、Trilaterateの正式な題名が「./trilaterate」で始まることを補った。収録先の名称の誤りが2件であって、SqueezaPulseの収録先を「Tenth International Conference on TEI」から正しい「Eleventh」に直し、Let It Ripの収録先を「Adjunct Proceedings」から正しい「Adjunct Publication」に直した。DOIの誤りが1件であって、SAWSenseのDOIがAcoustic Barcodesのものと取り違えられていたので直した。内容の記述の誤りが4件であって、川崎らの研究、Tessutivo、SoundOff、ProtoHoleについて、抄録の記述と食い違う説明を書き換えた。

第二に、著者名が「ほか」で省略されていた箇所を埋めたものが6件である。Trilaterate、CAPath、立花らのDICOMO2022論文、佐々木らのDICOMO2022論文、瀬崎らのWISS 2025発表、林らのWISS 2025発表について、それぞれ全員の氏名を一次情報で確認して書き入れた。

第三に、原典に根拠が見当たらない数値や記述を、削るか推測であると明示したものが7件である。Acoustic Voxelsのタグとしての働きの説明、Acoustic Barcodesの1個あたりのビット数、Blowholeの模型あたりの穴の個数、Lamelloの区別する歯の数、Printoneの「意図した曲を演奏できる」という記述、SilverCodesの95.3パーセントという精度、Ohmic-Stickerの厚み2ミリメートル未満という寸法である。

第四に、確認先のURLの差し替えが3件である。リンク切れになっていたSweepSenseの著者本人のPDF、アクセス制御で内容が取れないTouchTokensのHALのページ、そして文献を指していないSAWSenseの被引用一覧の問い合わせURLを、実際に内容を確認できた問い合わせ先に置き換えた。加えて、初回に「dblp.org/search?q=」という人間向けの検索ページを確認先としていた箇所は、機械可読な publ API の問い合わせURLに書き換えて、何をどこで確認したのかがたどれるようにした。

第五に、記事番号、ページ、DOI、発行日といった書誌の補完が34件である。とくに記事番号を持つACMの論文については、SoundOff、Acoustic Voxels、Printone、Itsy-Bits、AirLogic、DuoTouch、SAWSenseのそれぞれに記事番号を補った。

とくに重い訂正が2件あった。1件目は川崎らの研究についてである。初回の記述は「川崎らは特徴量と学習の側で頑健性を得ようとしている」としていたが、抄録は明確に、ある温度における周波数特性を基準温度における特性に対して周波数方向と振幅方向に補正するという手法を提案しており、識別精度を21.5パーセントから75.1パーセントへ引き上げたと述べていた。すなわち「周波数軸の正規化で温度ずれを打ち消す」という着想自体が日本の先行研究にすでにある。この訂正によって、CipherFluteの基準笛の新規性を主張できる範囲が狭まり、「参照を物体の中に同居させて事前較正を不要にした点」に絞る必要が生じた。2件目はTessutivoについてである。初回の記述は「導電性の標識の誘導的な足跡から物体を識別し、標識は無電源で形が情報を保持する」としていたが、抄録が述べているのは鍵や硬貨や電子機器といった普通の導電性の物体27種類を識別することであって、設計されたタグを読む研究ではなかった。CipherFluteとの関係の評価が根本から変わるので書き換えた。

実在が確認できず削除または未検証へ移した文献は0件である。逆に、「未検証のまま残ったもの」の節にあった6件の文献のうち5件（Vidgets、MoiréTag、MoiréWidgets、Kepros と Chahal、Zhou ら）は書誌を確定させて「検証で書誌が確定したもの」の節へ移し、残る1件（Asterisk and Obelisk）は情報量の数値まで確定したうえで、CipherFluteの新規性の言い方に影響する重要な文献として「新規性への脅威が大きい文献」の節の第19項へ昇格させた。

また検証の途中で、次の5件の文献を新たに見つけて追加した。第一に、FabAuthの後続研究にあたる Yuki Kubo, Kana Eguchi, Ryosuke Aoki のCHI EA 2020論文「3D-Printed Object Identification Method using Inner Structure Patterns Configured by Slicer Software」（pp. 1-7, DOI 10.1145/3334480.3382847、8個の物体を99.3パーセントで識別）である。第二に、Kaori Ikematsu と Itiro Siio のOhmic-Touch（CHI 2018, pp. 1-8, DOI 10.1145/3173574.3174095）であり、DuoTouchの位置づけを述べるうえで書誌を確定させた。第三に、Acoustrumentsの実演発表の版（ACM SIGGRAPH 2015 Emerging Technologies, pp. 3:1-3:1, DOI 10.1145/2782782.2792490）であり、Mary Mahler が著者に入るのはこの版であることを明示するために書誌を残した。第四と第五に、PUCsの実演発表の2つの版（ITS 2013の予稿集追補 pp. 325-328, DOI 10.1145/2512349.2514595、およびUIST 2013の予稿集追補 pp. 1-2, DOI 10.1145/2508468.2514926）であり、どの版を引いているのかがあいまいだった記述を整理した。

そのため、この文書が扱う文献の総数は、検証を経て67件になった。

書誌は確定したものの内容についての個別の主張の裏が取れなかった項目は9件あり、「未検証のまま残ったもの」の節に列挙した。主なものは、Acoustic Voxelsの4ビットという数値、SoundOffのタグの素材と寸法、SilverCodesの95.3パーセントという精度、Acoustic BarcodesとBlowholeの1個あたりのビット数である。これらはいずれも、CipherFluteとの情報量の比較に直接効く数値であるから、論文で言及する前にACM Digital Libraryなどの本文で確認してほしい。
