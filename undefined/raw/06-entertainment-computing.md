# エンタテインメントコンピューティングにおける音・楽器・遊びと認証

この文書は、CipherFluteの先行研究調査のうち「エンタテインメントコンピューティングにおける音・楽器・遊びと認証」という切り口を担当した調査の結果である。国際会議ICEC（International Conference on Entertainment Computing、dblpの系列名はInternational Conference/Workshop on Entertainment Computing）の2003年から2025年までの全巻、ACE（Advances in Computer Entertainment Technology）の2004年から2017年までの全巻、ACM CHI PLAYの2014年から2025年までの全巻（Companionを含む）、TEI（Tangible, Embedded, and Embodied Interaction）の2007年から2026年までの全巻、NIME（New Interfaces for Musical Expression）の全巻について、dblpの巻別目次を機械的に取得したうえで題目を走査した。日本語文献についてはCiNii ResearchのOpenSearch APIおよび検索結果ページを直接取得し、情報処理学会エンタテインメントコンピューティング研究会（EC研究会）の研究報告、エンタテインメントコンピューティングシンポジウム論文集、科学研究費助成事業データベース（KAKEN）を調べた。書誌情報はすべてCrossrefのDOI登録メタデータ、dblpの会議録目次、OpenAlex、CiNii Researchの書誌ページのいずれかで確認した。

## この切り口の要約

エンタテインメントコンピューティングの主要会議を題目レベルで網羅的に走査した結果として、まず言えることは、音や演奏を「鍵」として扱う遊戯的な体験の研究は、この分野にほとんど存在しないということである。ICECの全24巻には音楽・音響を扱う論文が多数あるが、それらはすべて音楽生成、音楽推薦、音響効果、音ゲーム、聴覚障害支援などであり、音を秘密や識別子の担体とする研究は1件も見当たらなかった。ICECで「認証」を題目に持つ論文は掌紋バイオメトリクスの1件だけである。ACE、CHI PLAY、NIMEでも同様であった。

いっぽうTEIには、CipherFluteと発想を共有する研究が集中している。TEI 2018のアート作品「The Bronze Key」は、モーションキャプチャした身体動作から生成した3Dプリント造形物そのものを対称暗号の鍵として提示し、平文をカセットテープ、暗号文を書籍として物質化した。TEI 2017の「Knock Knock to Unlock」はドアを叩くリズムを鍵として扱い、TEI 2024の「Act2Auth」は机上の日用品を動かす日常の所作に認証を埋め込んだ。TEI 2017の「UTAP」は3Dプリントした格子構造の音響伝搬特性の違いを状態の符号として使っている。認証の側からは、UIST 2009の「TapSongs」、NSPW 2009の「Musipass」のように、リズムや旋律を合言葉にする研究が古くからある。日本語圏では、水木敬明らを中心とするカードベース暗号が「身近な道具を用いる電源不要の暗号技術」として大きな系譜を作っており、2026年には情報処理学会誌の特集にまでなっている。

つまり、物理的な物体を鍵として扱う遊戯的研究も、リズムや旋律を合言葉にする認証研究も、電源不要の物理暗号の研究も、それぞれ独立に存在する。しかし、受動的に発音する造形物の音高そのものに多ビットの秘密を格納し、吹いて読み出すという組み合わせは見つからなかった。CipherFluteの位置づけは、これら三つの系譜の交点にある空白を埋めるものだと主張してよい。

## 新規性への脅威が大きい文献

この切り口では、脅威「高」に該当する文献は見つからなかった。CipherFluteの主要な主張（受動的な造形物の音高を語彙とする符号、基準笛によるパイロット補正、誤り訂正と遷移保証、秘密分散に秘匿を負わせる脅威モデル）のいずれかを先取りしている研究は存在しない。以下は脅威「中」に相当し、いずれも引用して差分を述べるべき文献である。

### 1. The Bronze Key: Performing Data Encryption

- 著者は Susan Kozel、Ruth Gibson、Bruno Martelli である。
- 発表は Proceedings of the Twelfth International Conference on Tangible, Embedded, and Embodied Interaction (TEI 2018), pp.549-554 である。
- 確認先は https://doi.org/10.1145/3173225.3173306 および https://api.openalex.org/works/doi:10.1145/3173225.3173306 である。

The Bronze Keyは、身体のデータを再物質化するパフォーマンスから生まれたアートインスタレーションである。身体動作、モーションキャプチャ、バーチャルリアリティを、データの痕跡とデータ保護への批評的な意識とともに統合している。対称暗号系を実演として遂行し、その過程で生じた成果物を物質として残した。TEIのアートトラックに出品された構成要素は三つあり、元の動作系列の生のモーションキャプチャデータを音声合成してカセットテープに録音したものが平文であり、モーションキャプチャされた身振りから作った3Dプリントのブロンズ形状が暗号鍵であり、かき混ぜたモーションキャプチャデータを印刷した書籍が暗号文である。

CipherFluteとの関係は強い。3Dプリントした造形物そのものを「暗号鍵」と呼び、それをエンタテインメント寄りの会場（TEIアートトラック）で提示した点が共通する。また、平文を音声メディアに載せている点も、音を情報の担体とする発想を先取りしている。ただし、この鍵は形状として提示されるだけで、読み出しの手順も、ビット数も、誤り訂正も、脅威モデルも定義されていない。CipherFluteが工学的な符号設計として提示するものを、Bronze Keyは芸術的な比喩として提示している。

脅威の度合いは「中」である。「3Dプリント造形物を暗号鍵とする」という一文だけを取り出せばCipherFluteの新規性と衝突して見えるため、必ず引用して、読み出し可能な符号としての設計の有無という差分を明示する必要がある。

### 2. カードベース暗号の系譜（den Boer 1990、Mizuki and Sone 2009、情報処理学会誌2026年特集）

- 著者は Bert den Boer、水木敬明、曽根秀昭、および情報処理学会誌特集の執筆陣（駒野雄一、水木敬明、真鍋義文、縫田光司ほか）である。
- 発表は Advances in Cryptology, EUROCRYPT '89, Lecture Notes in Computer Science (1990)、Frontiers in Algorithmics, Lecture Notes in Computer Science (2009)、情報処理 2026年5月号および6月号の特集「カードベース暗号とその展開〜情報セキュリティ教育にも応用可能な身近な道具を利用した暗号技術〜」である。
- 確認先は https://doi.org/10.1007/3-540-46885-4_23 、https://doi.org/10.1007/978-3-642-02270-8_36 、https://cir.nii.ac.jp/crid/1390026890675052288 である。

カードベース暗号は、トランプのような身近な物理的道具だけを使って秘密計算や秘密情報のやり取りを実現する研究分野である。den Boerの「五枚カードの技法」が出発点であり、水木と曽根の六枚カードによる論理積と四枚カードによる排他的論理和が効率化の基礎を作った。日本ではこの分野が継続的に発展しており、CiNii Researchで「カードベース暗号」を検索すると95件が該当する。2026年には情報処理学会誌が前編と後編の二回にわたって特集を組み、副題に「情報セキュリティ教育にも応用可能な身近な道具を利用した暗号技術」と掲げている。歴史と概要、算術計算とアンケートやレクリエーションへの応用、計算モデル、数学的解析といった章立てである。

CipherFluteとの関係は、「電源も電子部品も持たない物理的な物体で暗号的な営みを行う」という枠組みの共有である。しかもレクリエーションへの応用や教育への応用が明示的に語られており、遊戯性という点でも重なる。ただし、カードベース暗号が扱うのは複数人の間での秘密計算プロトコルであり、物体に秘密を「保管」して後から読み出すという用途ではない。またCipherFluteは物理層に暗号学的な秘匿力が無いと宣言しているのに対し、カードベース暗号は物理的操作そのものが情報理論的な安全性を担う。

脅威の度合いは「中」である。WISSの読者層は日本の情報処理学会の関係者であり、「身近な道具を使った電源不要の暗号技術」といえばカードベース暗号を連想する。引用せずに新規性を主張すると、位置づけが甘いと見なされる危険が高い。

### 3. TapSongs: Tapping Rhythm-Based Passwords on a Single Binary Sensor

- 著者は Jacob O. Wobbrock である。
- 発表は UIST 2009 (Proceedings of the 22nd Annual ACM Symposium on User Interface Software and Technology), pp.93-96 である。
- 確認先は https://doi.org/10.1145/1622176.1622194 および https://dblp.org/db/conf/uist/uist2009.html である。

TapSongsは、ボタンのような二値のセンサ一つだけで利用者を認証する手法である。利用者が自分で作った「ジングル」の押下と解放のタイミングモデルに、入力されたリズムを照合する。タイミングモデルは各事象の平均時刻と標準偏差を持ち、候補系列の各事象がモデル平均のプラスマイナス三標準偏差以内に収まるかどうかで判定する。10名の被験者が12回の例示から自分のモデルを2分未満で作成した後、ログイン試行の83.2パーセントが成功した。

CipherFluteとの関係は、「音楽の断片を秘密として使う」という発想の共有である。CipherFluteが音高の系列を語彙とするのに対し、TapSongsは時間間隔の系列を語彙とする。また、後続のBeat-PIN（AsiaCCS 2018）やSmartEar（IEEE Internet of Things Journal 2022）に至るまで、この系譜は継続している。

脅威の度合いは「中」である。「音楽を鍵にする」という着想の先行例として必ず引用すべきであるが、TapSongsは電子センサと計算機による照合を前提としており、電源も電子部品も持たない物体が音高で情報を保持するCipherFluteとは、担い手が根本的に異なる。この差分を明示すれば新規性は損なわれない。

### 4. Knock Knock to Unlock: A Human-centered Novel Authentication Method for Secure System Fluidity

- 著者は Marisa Lu、Gautam Bose、Austin S. Lee、Peter Scupelli である。
- 発表は TEI 2017 (Proceedings of the Eleventh International Conference on Tangible, Embedded, and Embodied Interaction), pp.729-732 である。
- 確認先は https://doi.org/10.1145/3024969.3035530 および https://api.openalex.org/works/doi:10.1145/3024969.3035530 である。

人がドアの前に立って中に入りたいときに何をするかといえば、ノックをする。このシステムでは、利用者に固有のノックの型が本人性を認証し、ドアを開ける。人の直感的な行為と反応が、新しいかたちで周囲の世界に働きかけられるようにすることをねらいとしている。IoTとフィジカルコンピューティングを活用して、技術の存在をより感じさせないようにしている。ノックによる入室という仕組みは、共有空間における社会的相互作用にアフォーダンスを生み、所有の流動性やアクセス可能性と安全性との釣り合いを取ろうとしている。

CipherFluteとの関係は、日常の物理的な行為（叩く、吹く）をそのまま鍵の入力とする点にある。さらに「日用品や建具に認証を溶け込ませる」という設計思想も重なる。ただしノックの型は利用者の身体が生成するものであり、物体側に情報が刻まれているわけではない。

脅威の度合いは「中」である。TEIという、CipherFluteが投稿しても不思議のない場で「物理的な行為を鍵にする」提案が出ている以上、引用して、鍵が人にあるのか物にあるのかという差分を述べる必要がある。

### 5. Act2Auth: A Novel Authentication Concept based on Embedded Tangible Interaction at Desks

- 著者は Sarah Delgado Rodriguez、Sarah Prange、Lukas Mecke、Florian Alt である。
- 発表は TEI 2024 (Proceedings of the Eighteenth International Conference on Tangible, Embedded, and Embodied Interaction), 論文番号12, pp.1-15 である。
- 確認先は https://doi.org/10.1145/3623509.3633360 および https://api.openalex.org/works/doi:10.1145/3623509.3633360 である。

Act2Authは、机の上での実体的な操作を検知することで、認証を利用者の既存の生活習慣に埋め込む概念である。利用者はカップを机に置く、キーボードを置き直す、マウスに触れるといった（秘密の）一連の所作を行うことで認証できる。この概念は、Redditから集めた107枚の机の写真の物体分析、65名を対象に触覚ベースの認証の秘密をどう作るかを調べたオンライン調査、机における静電容量式タッチ検知の技術的検討という三つの調査に基づいている。試作を実装し、文章によるパスワードと比較して使いやすさと記憶しやすさを8名で評価した。

CipherFluteとの関係は、「日用品に認証を偽装して埋め込み、日常の所作のまま読み出す」という設計目標の一致である。CipherFluteが日用品への偽装による探索コストの引き上げを物理層の役割としているのと、発想が近い。ただしAct2Authは静電容量センサと計算機を前提とし、秘密は所作の順序にあって物体にはない。

脅威の度合いは「中」である。「日用品に埋め込む認証」という主張の先行例であり、引用して、電源の有無と秘密の所在という差分を述べるべきである。

### 6. UTAP: Unique Topographies for Acoustic Propagation

- 著者は Jan Rod、David Collins、Daniel Wessolek、Thavishi Ilandara、Ye Ai、Hyowon Lee、Suranga Nanayakkara である。
- 発表は TEI 2017 (Proceedings of the Eleventh International Conference on Tangible, Embedded, and Embodied Interaction), pp.141-152 である。
- 確認先は https://doi.org/10.1145/3024969.3024987 および https://api.openalex.org/works/doi:10.1145/3024969.3024987 である。

UTAPは、可鍛性のある実体的インタフェースをアルゴリズム的に設計する手法である。核心は、アルゴリズムで生成したトポロジー的に相異なる格子を圧電トランスデューサに取り付け、変形にともなう変調音響信号の変化を検知して相互作用の状態に分類することである。レーザ切断と3Dプリントで作った格子をシリコーン成形と組み合わせた複数のインタフェースで手法を実証した。四つの異なるインタフェース設計について、一点や複数点の押下、力の強さの違い、曲げやねじりといった動作の検知と位置同定の性能を技術評価した。

CipherFluteとの関係は、「3Dプリントした受動的な構造の音響特性の違いを、区別可能な符号として使う」という点にある。既に論文が引用しているAcoustic Voxels（SIGGRAPH 2016）と同じ発想の系譜であり、TEIというエンタテインメント寄りの場での実例にあたる。ただしUTAPは能動的な音源（圧電素子）を必要とし、目的は変形の検知であって情報の格納ではない。

脅威の度合いは「中」である。3Dプリント構造の音響的個体差を符号に使う先行例として、Acoustic Voxelsと並べて引用しておくのが安全である。

### 7. Musipass: Authenticating Me Softly with "My" Song

- 著者は Marcia Gibson、Karen Renaud、Marc Conrad、Carsten Maple である。
- 発表は NSPW 2009 (Proceedings of the 2009 Workshop on New Security Paradigms Workshop) である。
- 確認先は https://doi.org/10.1145/1719030.1719043 および https://www.nspw.org/papers/2009/nspw2009-gibson.pdf である。

Musipassは、英数字の代わりに旋律で構成されるパスワードの方式である。ウェブ上での認証という課題に向けて、利用者を念頭に置いて設計されている。音楽は世界中で普遍的であり、人間は音楽に対して優れた記憶を持つという前提に立っている。試作システムの評価では、記憶しやすさと利用者の受容の両面で優れた結果が示されたと報告されている。同じ著者らはその後、音楽による認証の進展をまとめた書籍章も執筆している。

CipherFluteとの関係は、「旋律そのものを秘密として扱う」という一点で直接に重なる。CipherFluteの符号は音高の系列であり、聞けば旋律として知覚される。この意味で、Musipassは「音楽を鍵にする」という発想の代表的な先行研究である。ただしMusipassは画面上で楽曲を選択・再生する電子的な仕組みであり、物体は関与しない。

脅威の度合いは「中」である。音楽を鍵にする発想は既にあると指摘されうるため、必ず引用したうえで、CipherFluteの新規性が「旋律を鍵にすること」ではなく「電源を持たない造形物が旋律を保持し、吹くことで読み出せること」にあると明確に言い直す必要がある。

### 8. Puzzles Unpuzzled: Towards a Unified Taxonomy for Analog and Digital Escape Room Games

- 著者は Andrey Krekhov、Katharina Emmerich、Ronja Rotthaler、Jens Krueger である。
- 発表は Proceedings of the ACM on Human-Computer Interaction, Vol.5, No.CHI PLAY (2021), pp.1-24 である。
- 確認先は https://doi.org/10.1145/3474696 である。

脱出ゲームは実在の施設、ボードゲーム、デジタル実装など様々な形態で存在し、いずれも部屋から脱出するために多様なパズルを解くという同じ発想に立っている。この10年で人気が急速に高まり、関連する研究も増えたが、学術的な状況は断片化しており、多様性に耐える共通のモデルと語彙が欠けている。本論文は脱出ゲームの分析と構築の基盤を確立することを目指し、先行文献から高水準の設計枠組みを導いたうえで、アナログとデジタルの隔たりを埋める原子的なパズル分類学を主要な貢献として提示している。分類学は39のアナログおよびデジタルの脱出ゲーム（近年のバーチャルリアリティ作品を含む）の分析によって精緻化され、精神的、身体的、感情的な挑戦から構成される。

CipherFluteとの関係は、CipherFluteの遊戯的な応用（宝探し的に日用品の中の笛を見つけて吹く、2枚そろって初めてハートが現れるカード）を、脱出ゲーム研究の語彙で位置づけられる点にある。とくに「物理的な挑戦」の分類は、吹くという行為をパズルの要素として記述する道具になる。

脅威の度合いは「中」である。CipherFluteの主張を直接に脅かすものではないが、遊戯性を論じるならこの分類学を無視した記述は弱い。引用して、CipherFluteが提供するのは新しいパズル素材（音高で読める物理的な符号）であると述べるのが有効である。

### 9. 情報タイムカプセルにおける地図情報を用いた認証システムの実装

- 著者は北山海、西岡大、村山優子（いずれも岩手県立大学）である。
- 発表は情報処理学会研究報告 EC（エンタテインメントコンピューティング）2014巻62号, pp.1-6, 2014年3月6日である。GN研究会およびHCI研究会との共同開催であり、同一の報告が3研究会の研究報告として登録されている。
- 確認先は https://cir.nii.ac.jp/crid/1573950402603038976 である。

本研究は、災害時の世代間の情報伝達の不足という問題を解決するために、記憶情報を未来に伝える情報タイムカプセルを提案している。ネットワーク上で情報タイムカプセルを実現するには記憶情報を識別子とパスワードで管理する必要があるが、それらは十数年たつと忘れてしまうという問題が生じる。そこで記憶に残りやすい地図情報を用いた認証方法を提案し、十数年後でも記憶情報にアクセスできる情報タイムカプセルを実装したと報告している。

CipherFluteとの関係は、「長期にわたって秘密を保管し、後から本人が読み出す」という時間軸の問題設定の共有である。CipherFluteが暗号資産のリカバリーシードという長期保管の用途を掲げていることと重なる。EC研究会という、CipherFluteの投稿先の隣接コミュニティで発表されている点も重要である。ただし手法はネットワーク上のパスワード代替であり、物体も音も関与しない。

脅威の度合いは「中」である。日本のエンタテインメントコンピューティング分野で「秘密の長期保管と認証」を扱った数少ない先行例であり、引用して、記憶に頼るのか物体に頼るのかという差分を述べるとよい。

### 10. Bit:chat: A Tangible Approach to Teach Children about Everyday Secure Communication and Cryptography

- 著者は Mille Skovhus Lunding、Maja Dybboe、Karl-Emil Kjær Bilstrup、Ane Vielandt Jensen、Line Have Musaeus、Ole Sejer Iversen、Marianne Graves Petersen である。
- 発表は IDC 2026 (Proceedings of the 25th Annual ACM Interaction Design and Children Conference) である。
- 確認先は https://doi.org/10.1145/3773077.3806132 および https://api.openalex.org/works/doi:10.1145/3773077.3806132 である。

デジタルなやり取りが子どもの社会的相互作用に不可欠になった以上、子どもは自分のプライバシーがいつどのように守られるのかを理解する必要がある。この論文はBit:chatという実体的な教材の設計と評価を報告している。ネットワーク接続したmicro:bitとウェブインタフェースと紙のテンプレートを組み合わせ、安全な通信と暗号を手を動かす協働を通じて子どもに導入する。構成主義と協調学習に立脚し、クライアントとサーバの通信や暗号処理を、子どもが探索し操作できる物理的な人工物と行為として外在化している。K-9の教室で探索的な研究として評価し、質的結果は実体的な設計が関与、仲間との協働、探索的な学習を支えたことを示し、量的結果は中核概念の理解の向上を示した。

CipherFluteとの関係は、「暗号を物理的な人工物として体験させる」という体験型セキュリティ教育の設計目標にある。CipherFluteの秘密分散のデモ（2枚そろって初めてハートが現れるカード）は、まさにこの種の教材として機能しうる。

脅威の度合いは「中」である。CipherFluteの教育的応用を主張する場合には、この論文が直近の比較対象になる。ただしBit:chatはマイクロコントローラを使うため電源を必要とし、秘密を物体に格納するわけでもない。

### 11. Learning from Escape Rooms? A Study Design Concept Measuring the Effect of a Cryptography Educational Escape Room

- 著者は Stefan Seebauer、Sabrina Jahn、Jürgen Mottok である。
- 発表は EDUCON 2020 (IEEE Global Engineering Education Conference) である。
- 確認先は https://doi.org/10.1109/EDUCON45650.2020.9125333 および https://api.openalex.org/works/doi:10.1109/EDUCON45650.2020.9125333 である。

情報セキュリティの専門家が今後さらに必要になると予測される一方で、工学系の高等教育ではこの主題がほとんど扱われていないという問題意識から出発している。ゲームに基づく学習の道具として教育的脱出ゲームを選び、工学系の高等教育で情報セキュリティを教えることを目指した。この脱出ゲームでは、学生が暗号を重点として、学んだ知識でパズルや謎を解く。課題はAES、RSA、SHA3といった異なる暗号方式とハッシュアルゴリズムを扱う。レーゲンスブルク応用科学大学の電気工学・情報技術の学士課程の学生を5名から8名ずつの3グループに分けて実施し、事前説明、実施、事後説明、試験形式の評価票という流れで測定した。

CipherFluteとの関係は、暗号の概念を物理的な謎解きの体験に落とし込むという応用の方向性である。関連して、日本では和泉諭（仙台高等専門学校）が科研費挑戦的研究（萌芽）JP22K18607「体験型謎解きゲームの要素を導入した実践的情報セキュリティ人材育成のための教材開発」（2022年6月30日から2025年3月31日、配分額6,110,000円）を実施しており、キーワードは情報セキュリティ、セキュリティ教育、謎解き、PBL演習である。確認先は https://cir.nii.ac.jp/crid/1040292706176377088 および https://kaken.nii.ac.jp/grant/KAKENHI-PROJECT-22K18607/ である。

脅威の度合いは「中」である。CipherFluteを体験型セキュリティ教育の教材として位置づけるなら、これらは直接の比較対象になる。ただしどちらも既存の暗号知識を問うパズルであり、新しい物理的な符号の担体を作る研究ではない。

## 背景として押さえるべき文献

以下は脅威「低」であり、背景として引用する価値がある文献である。すべて一次資料で書誌を確認した。

- Ge Wang, "Ocarina: Designing the iPhone's Magic Flute", Computer Music Journal, 2014（初出はNIME 2009の "Designing Smule's Ocarina: The iPhone's Magic Flute", pp.303-307）。確認先は https://doi.org/10.1162/COMJ_a_00236 と https://doi.org/10.5281/zenodo.1177697 である。息を吹き込む笛型の相互作用を大衆的な娯楽として成立させた代表例であり、「吹く」という行為の親しみやすさの根拠として引用できる。
- Nobuyuki Umetani, Athina Panotopoulou, Ryan Schmidt, Emily Whiting, "Printone: Interactive Resonance Simulation for Free-form Print-wind Instrument Design", ACM Transactions on Graphics (SIGGRAPH Asia 2016)。確認先は https://doi.org/10.1145/2980179.2980250 である。自由形状の3Dプリント管楽器を共鳴シミュレーションで対話的に設計する研究であり、CipherFluteの管長と基本周波数の関係式による設計と対比できる。
- Young-Mi Kim, Jong-Soo Choi, "Bamboo flute", ACE 2009, p.448。確認先は https://doi.org/10.1145/1690388.1690496 である。韓国の伝統楽器テグムと竹の絵画を主題としたインタラクティブなアート作品であり、笛がエンタテインメントコンピューティングの場に現れた数少ない例である。
- Tiago Martins, Christa Sommerer, Laurent Mignonneau, Nuno Correia, "Noon: A Secret Told by Objects", ACE 2009, p.446。確認先は https://doi.org/10.1145/1690388.1690494 である。火災から回収されたとされる実物体に触れて操作することで物語が展開する対話的な物語装置であり、「物が秘密を語る」という体験設計の先行例である。
- Laddy P. Cadavid, "Knotting the memory//Encoding the Khipu_: Reuse of an ancient Andean device as a NIME", NIME 2020, pp.495-498。確認先は https://doi.org/10.5281/zenodo.4813495 である。アンデスの結縄キープを電子楽器として再生した作品であり、情報を符号化する物理的装置と楽器が同一の物であるという構図がCipherFluteと重なる。
- Jun Munemori, Shunsuke Miyai, Junko Itou, "Electronic Treasure Hunt: Real-Time Cooperation Type Game That Uses Location Information", ICEC 2006, pp.336-339。確認先は https://doi.org/10.1007/11872320_45 である。ICECにおける宝探しゲームの代表例である。
- Michel Simatic ほか, "\"Plug: Secrets of the Museum\": A Pervasive Game Taking Place in a Museum", ICEC 2009, pp.302-303。確認先は https://doi.org/10.1007/978-3-642-04052-8_44 である。博物館という日常空間に秘密を仕込む遍在ゲームである。
- Jaime Carvalho, Luís Duarte, Luís Carriço, "An Analysis of Player Strategies and Performance in Audio Puzzles", ICEC 2012, pp.349-362。確認先は https://doi.org/10.1007/978-3-642-33542-6_31 である。音そのものをパズルの素材とする数少ないICEC論文である。
- Hanieh Shakeri, Samarth Singhal, Rui Pan, Carman Neustaedter, Anthony Tang, "Escaping Together: The Design and Evaluation of a Distributed Real-Life Escape Room", CHI PLAY 2017, pp.115-128。確認先は https://doi.org/10.1145/3116595.3116601 である。離れた二つの部屋を音声と映像でつなぎ、共有された人工物を通じて協力する脱出ゲームであり、「複数人がそろって初めて成立する体験」の設計知見が得られる。
- Joseph Tu, Ekaterina Durmanova, "Curioscape: A Curiosity-driven Escape Room Board Game", CHI PLAY 2020 Companion, pp.94-97。確認先は https://doi.org/10.1145/3383668.3419925 である。
- Chunhan Chen, Yihan Tang, Tianyi Xie, Stefania Druga, "The Humming Box: AI-powered Tangible Music Toy for Children", CHI PLAY 2019 Companion, pp.87-95。確認先は https://doi.org/10.1145/3341215.3356990 である。手回しオルゴールと計算機音楽を融合した子ども向け玩具である。
- Linas K. Gabrielaitis, Oguz 'Oz' Buruk, "Playing Esker Formations: Additive Games with a 3D Printer", CHI PLAY 2024, pp.365-371。確認先は https://doi.org/10.1145/3665463.3678828 である。3Dプリンタ自体を遊びの装置として扱う研究である。
- Tamara Denning, Adam Lerner, Adam Shostack, Tadayoshi Kohno, "Control-Alt-Hack: The Design and Evaluation of a Card Game for Computer Security Awareness and Education", CCS 2013。確認先は https://doi.org/10.1145/2508859.2516753 である。体験型のセキュリティ教育の古典であり、約800部を150名の教育者に配布して評価した。
- Daria Tsoupikova, Rong Zeng, Vera Pless, Janet Beissinger, "Cryptography and mathematics: educational game \"Treasure Hunt\"", ACM SIGGRAPH 2006 Research Posters, p.40。確認先は https://doi.org/10.1145/1179622.1179668 である。暗号と数学の教育を宝探しゲームとして構成した例である。
- B. Hutchins, A. Reddy, Wenqiang Jin, Mi Zhou, Ming Li, "Beat-PIN: A User Authentication Mechanism for Wearable Devices Through Secret Beats", AsiaCCS 2018。確認先は https://doi.org/10.1145/3196494.3196543 である。TapSongsの系譜に連なるリズム認証である。
- S. Abhishek Anand, Prakash Shrestha, Nitesh Saxena, "Bad Sounds Good Sounds: Attacking and Defending Tap-Based Rhythmic Passwords Using Acoustic Signals", CANS 2015。確認先は https://doi.org/10.1007/978-3-319-26823-1_7 である。リズム認証が音響的な盗聴に弱いことを示しており、CipherFluteが「音の層に秘匿力は無い」と宣言していることの裏付けとして使える。
- Mirko Fetter, Christoph Beckmann, Tom Gross, "MagnetiCode: Physical Mobile Interaction through Time-encoded Magnetic Identification Tags", TEI 2014, pp.205-212。確認先は https://doi.org/10.1145/2540930.2540963 である。物体に時間符号で識別子を埋め込む発想の隣接例である。
- Mitsuru Minakuchi, Satoshi Nakamura, "Collaborative ambient systems by blow displays", TEI 2007, pp.105-108。確認先は https://doi.org/10.1145/1226969.1226992 である。息を吹きかける行為を入力とする実体的インタフェースである。
- Stefanie Mueller ほか, "Scotty: Relocating Physical Objects Across Distances Using Destructive Scanning, Encryption, and 3D Printing", TEI 2015, pp.233-240。確認先は https://doi.org/10.1145/2677199.2680547 である。3Dプリントと暗号を組み合わせた数少ないTEI論文である。
- 沖真帆, 塚田浩二, 栗原一貴, 椎尾一郎「イルゴール：家庭の生活状況を奏でるオルゴール型インタフェースの研究」情報処理学会論文誌 2011年（初出はインタラクション2010）。確認先は https://cir.nii.ac.jp/all?q=%E3%82%AA%E3%83%AB%E3%82%B4%E3%83%BC%E3%83%AB%20%E3%82%A4%E3%83%B3%E3%82%BF%E3%83%A9%E3%82%AF%E3%82%B7%E3%83%A7%E3%83%B3 である。オルゴールという受動的な発音機構を情報提示に使う日本の先行例であり、著者自身の系譜としても言及できる。
- 菊地勇斗, 塚田浩二「3Dプリンタを用いた封蝋表現手法の研究」エンタテインメントコンピューティングシンポジウム2023論文集。確認先は https://cir.nii.ac.jp/crid/1050860222033198208 である。3Dプリンタで「封をする」表現を作る研究であり、秘密を物体に閉じ込める遊戯性という点で近い。
- 太田正哉, 山下勝己「携帯電話の着信メロディによる認証システムに関する検討」電子情報通信学会技術研究報告 103巻376号, pp.19-22, 2003年。確認先は https://cir.nii.ac.jp/all?q=%E3%83%A1%E3%83%AD%E3%83%87%E3%82%A3%20%E8%AA%8D%E8%A8%BC である。日本語圏で旋律を認証に使った初期の検討である。
- Kevin Valencia-Aragón ほか, "Learning Through Play: Implementing an Educational Escape Room for Teaching Traditions and Culture", ICEC 2025, pp.349-359。確認先は https://doi.org/10.1007/978-3-032-02555-5_25 である。
- Pablo Gutiérrez-Sánchez ほか, "Initializing Interactive Treasure Hunts in Cultural Heritage Sites: An LLM-Based Approach", ICEC 2025, pp.151-165。確認先は https://doi.org/10.1007/978-3-032-02555-5_11 である。
- Irina Paraschivoiu, Josef Buchner, Robert Praxmarer, Thomas Layer-Wagner, "Escape the Fake: Development and Evaluation of an Augmented Reality Escape Room Game for Fighting Fake News", CHI PLAY 2021 Extended Abstracts, pp.320-325。確認先は https://doi.org/10.1145/3450337.3483454 である。

## 未検証のまま残ったもの

以下は実在または書誌情報を確認しきれなかったものであり、論文に書く場合は追加の確認が必要である。

- Mark Gondree, Zachary N. J. Peterson による "[d0x3d!]: A Board Game for Network Security Education" は、USENIX 3GSE 2013（Summit on Gaming, Games and Gamification in Security Education）で発表されたとされる。DOIが付与されておらず、USENIXのサイト上で該当ページを取得できなかった。存在自体は他の文献から強く示唆されるが、一次資料に到達していないため未検証である。
- キャプテン・クランチのシリアル箱に入っていた笛が2600ヘルツの純音を出し、それが長距離電話網の制御信号として機能したという事例は、CipherFluteにとって「受動的な笛が鍵として働いた」最古の実例にあたる。Ron Rosenbaum "Secrets of the Little Blue Box", Esquire, 1971年10月号が一次資料であるが、今回はこの雑誌記事そのものを取得できず、電話博物館やAtlas Obscuraなどの二次資料までしか確認できなかった。
- Y. Takase ほかによる "Poster: Rhythm Tap: Inclusive Personal Authentication Method Based on Rhythmic Variation" は、Semantic Scholarに登録されているが会議名と年が空欄であり、発表媒体を特定できなかった。
- 増山一光「発達段階に応じた主体的な情報セキュリティへの学びを促すカードゲーム教材の開発」は、CiNii Researchの科研費データとして題名と代表者を確認したが、課題番号や研究期間などの詳細は取得していない。
- 金丸紫乃「体験型謎解きゲームへの遠隔地からの参加を支援するARシステムの提案」は、CiNii Researchに登録があることを確認したが、掲載媒体と年が空欄であり、学位論文か大会発表かを特定できなかった。

## この切り口で見つからなかったこと

以下は、実際に走査したうえで「存在しなかった」と言える事柄である。CipherFluteの新規性の主張の根拠として使える。

第一に、ICECの2003年から2025年までの全巻（dblpの系列 conf/iwec に収録された24冊）の題目を機械的に走査した結果、音や笛や楽器を「鍵」「秘密」「符号」の担体とする論文は1件も存在しなかった。ICECに現れる音楽・音響関連の論文は、音楽生成、音楽推薦、音響効果の設計、音ゲーム、音のみのゲーム、音楽療法、視覚障害者支援などに限られる。ICECで「認証」を扱ったのは2007年の掌紋バイオメトリクス1件のみであり、遊びと認証を結びつけた論文は無かった。

第二に、ACEの2004年から2017年までの全巻を走査したところ、暗号に触れる論文は2005年の暗号化ストリーミング配信1件のみであり、秘密を物体に格納する研究は無かった。笛が現れるのは2009年の「Bamboo flute」というアート作品1件だけで、これは情報の担体ではない。

第三に、CHI PLAYの2014年から2025年までの全巻（Companionを含む19冊）を走査したところ、脱出ゲームや宝探しの研究は多数あるが、音を鍵とする遊びも、物体に秘密を格納する遊びも無かった。「Ethereum Crypto-Games」「Tokenfication」のように暗号資産を扱う論文はあるが、いずれもゲーム経済の議論であり、鍵の保管の問題は扱っていない。

第四に、TEIの2007年から2026年までの全巻を走査したところ、認証を扱う論文は「Knock Knock to Unlock」「Act2Auth」「Authentication on public terminals with private devices」の3件、暗号を扱う論文は「The Bronze Key」「Scotty」の2件であった。これらのいずれも、音高を語彙とする符号を物体に刻む発想は持っていない。

第五に、NIMEの全巻を走査したところ、3Dプリントで楽器を作る研究や、キープのように情報を符号化する装置を楽器に転用する研究はあるが、楽器に秘密を格納して読み出す研究は無かった。

第六に、日本語文献では、CiNii Researchで「エンタテインメントコンピューティングシンポジウム 暗号」「同 秘密」「同 謎解き」がいずれも0件であった。「同 笛」は自転車の警笛音に関する1件のみである。「エンタテインメントコンピューティング 暗号」も0件、「3Dプリント 音響 情報 埋め込み」も0件、「笛 3Dプリンタ」も0件、「秘密分散 体験」も0件であった。日本のエンタテインメントコンピューティング分野に、音を鍵にする研究も、造形物に秘密を格納する研究も存在しないと言ってよい。

第七に、音楽やリズムを鍵にする認証研究（Musipass、TapSongs、Beat-PIN、SmartEar、着信メロディ認証など）はすべて、電子センサと計算機による照合を前提としている。受動的な物体そのものが音高によって多ビットの情報を保持し、人が吹くだけで読み出せるという構成は、この系譜のどこにも無かった。

第八に、贈り物や記念品に秘密を込める研究は、TEI 2010の「Slow computing gifts」やTEI 2012の「Giffi: a gift for future inventors」のように贈与の設計として存在するが、暗号学的な秘密を込めるものではなかった。「複数人がそろって初めて成立する体験」も、分散型脱出ゲームや協調ゲームとしては存在するが、秘密分散の閾値構造を物体に実装した遊戯研究は見つからなかった。

第九に、暗号資産のリカバリーシードを遊戯的な物体に埋め込む研究は、エンタテインメント系のどの会議にも見つからなかった。

## 調べ残した穴

情報処理学会電子図書館（https://ipsj.ixsq.nii.ac.jp/）の検索インタフェースはJavaScriptに依存しており、機械的な全題目走査ができなかった。OAI-PMHの応答は得られたものの、集合が刊行物の巻号単位で1万件以上あり、EC研究会の集合を特定するところまで到達できなかった。そのためEC研究会の研究報告とエンタテインメントコンピューティングシンポジウム論文集については、CiNii Researchのキーワード検索に頼っており、題目の全数走査はしていない。ここは追加調査の価値がある。

dblpのACE系列（conf/ACMace）は2017年までしか収録されておらず、2018年以降のACEを走査していない。ICEC 2002（IWEC）の巻と、ICEC 2025本体の一部も取得できていない。CHI PLAYのCompanionは2016年より前の年度が存在しないため問題ないが、2016年と2017年のCompanionの一部しか見ていない可能性がある。

WISSの各年の予稿集の全題目走査も行っていない。CiNiiのキーワード検索では音や鍵に関する該当が出なかったが、WISSは予稿集がウェブ上に独立して置かれているため、直接の走査が望ましい。

日本デジタルゲーム学会（DiGRA JAPAN）年次大会、日本バーチャルリアリティ学会大会、インタラクションのプログラムについても、キーワード検索の範囲にとどまっており、全数走査はしていない。

芸術系の文脈（Ars Electronica、SIGGRAPH Art Gallery、文化庁メディア芸術祭）で、音を鍵とする作品が存在する可能性を追い切れていない。The Bronze Keyのような作品は学術会議のアートトラックに現れるとは限らないため、この方向は残った穴である。

キャプテン・クランチの笛のように、玩具や景品として配られた受動的な発音体が実際の認証を破った事例は、技術史・ハッカー文化史の側に一次資料がある。Esquire誌1971年10月号の記事本体、および電話網の信号方式の当時の技術文書に当たれば、CipherFluteの位置づけをより強く語れるはずである。

最後に、有力文献の被引用関係をたどる作業を十分に行えていない。The Bronze Key、Knock Knock to Unlock、UTAPはいずれも被引用数が一桁であり、被引用をたどっても広がりは小さいと見込まれるが、TapSongsとControl-Alt-Hackは被引用が多く、そこから遊戯性と認証を結ぶ研究が見つかる可能性が残っている。
