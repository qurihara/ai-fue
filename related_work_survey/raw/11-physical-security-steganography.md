# 物理的な鍵とトークンの安全性、および物理的な隠蔽

本ファイルは、CipherFlute（WISS 2026投稿予定、栗原一貴）の関連研究調査のうち、「物理的な鍵とトークンの安全性、および物理世界での隠蔽（ステガノグラフィ）」という切り口を担当した結果である。書誌情報はすべて、Crossref（DOI登録機関の一次データ）、CiNii Research、Internet Archive Scholar、arXiv API、著者本人が公開している原稿PDF、Bitcoin改善提案の公式リポジトリのいずれかにWebFetchで直接当たって確認した。確認できなかったものは末尾の「未検証のまま残ったもの」に隔離した。

なお、依頼で指定された書き出し先パスが `undefined/raw/...` となっていたため、既存の同一調査の他の切り口（`01-fab-embed-optical.md` から `05-jp-fabrication-hci.md`）と同じディレクトリである `related_work_survey/raw/` に書き出した。

---

## この切り口の要約

この切り口を洗い直した結果、CipherFluteにとって最も危険なのは「先に同じものを作られていた」という型の先行研究ではなく、「物理層が探索コストを引き上げる」という主張そのものを定量的に切り崩す実証研究の系列であると判明した。中心はロジャー・ジョンストンらの封印（tamper-indicating seal）の脆弱性評価であり、広く使われている120種類の封印すべてが一般人でも入手できる道具で破られ、熟練した1人あたりの平均所要時間は5分未満、攻撃の平均費用は55ドルであったと報告されている。アンドリュー・アペルは同じ論法を投票機の封印に適用し、鍵のピッキングを平均13秒で行い、法廷で全封印を45分以内に痕跡なく外して戻して見せた。つまり物理層の防護は「分」と「数十ドル」の単位で測られる。CipherFluteが物理層に期待できる効果はこの桁を超えないと考えるのが妥当であり、論文はこの数字を引いたうえで自らの主張の大きさを抑えるべきである。

一方で、偽装が探索コストを上げること自体を裏づける実証もある。ウルフらの「まれな標的は見落とされる」という出現率効果は、探す側が「そこに秘密がある」と期待していない状況では検出率が大きく落ちることを示している。シュヴァニンガーらの空港のX線検査の研究群も同じ方向を向く。逆に、クロフォードとイリベリの隠れ場所選択の実験は、隠す側が体系的に予測されうることを示しており、素朴な偽装の限界を示す反証側の証拠になる。

物理的な鍵の複製については、写真から鍵の刻みを復元するSneakey、深層学習で写真から印刷可能な鍵モデルを作るDeepKey、3Dプリンタで規制されたキーウェイを突破するBurgessらの研究、印影から印章を3Dプリンタで偽造する木村らの日本語研究があり、いずれも「形状が観測できれば複製できる」というCipherFluteの脅威モデルの宣言を強く裏づける。物理暗号の側では、視覚暗号、音響暗号、カードベース暗号、3Dプリンタで作る物理暗号装置（伊藤ら）、手計算可能な誤り訂正付き秘密分散であるcodex32が隣接する。他方、「日用品に偽装した容器（隠し金庫）」や「強要下での否認可能な資産保管」に関する学術研究は事実上存在せず、この空白はCipherFluteの新規性の根拠として使える。

---

## 新規性への脅威が大きい文献

### 1. Tamper-Indicating Seals for Nuclear Disarmament and Hazardous Waste Management

- 著者: Roger G. Johnston
- 掲載: Science & Global Security, Vol. 9, pp. 93–112, 2001年
- 確認先: https://doi.org/10.1080/08929880108426490 および全文 https://scienceandglobalsecurity.org/archive/sgs09johnston.pdf （PDF本文を取得して内容を直接確認した）

内容の要約を述べる。この論文は、ロスアラモス国立研究所の脆弱性評価チーム（Vulnerability Assessment Team）が広く使われている120種類の封印を評価した結果を報告している。低技術のものから高技術のもの、受動型と能動型の双方を含む120種類すべてが、一般に入手可能な低技術の道具と手法で破られた。しかもその破壊は、それぞれの封印に対して通常行われる検査手順では検出されなかった。熟練した1人による所要時間は3秒から2時間に分布し、平均は5分をはるかに下回った。核関連用途に現用されているものに限っても平均所要時間は8分未満であった。攻撃1件あたりの平均費用は55ドルであり、限界費用はそれよりはるかに小さかった。著者は、封印の価格は脆弱性の予測因子として役に立たないこと、封印そのものより「封印の運用手順」のほうが効果を決めることを強調している。また、あらゆる封印は原理的に偽造可能であるという議論も展開している。

CipherFluteとの関係を述べる。CipherFluteは「物理層に暗号学的な秘匿の力はまったく無い」と宣言したうえで、物理層の役割を「日用品への偽装による探索コストの引き上げ」に限定している。この論文は、物理層の防護効果が実際にどれくらいの大きさなのかを、専門機関が体系的に測った数少ない一次資料である。5分未満、55ドルという数字は、CipherFluteが物理層に期待してよい上限の目安を与える。

脅威の度合いは「高」である。理由を述べる。CipherFluteが残した唯一の物理層の主張が「探索コストの引き上げ」であるところ、この研究はその種のコストが分単位・数十ドル単位で崩れることを120種類の実測で示しており、主張の大きさを大幅に割り引かせる。さらに、この論文を引かずに「探索コストが上がる」とだけ書くと、物理セキュリティの専門家からは根拠のない楽観と読まれる危険がある。

### 2. Security Seals on Voting Machines: A Case Study

- 著者: Andrew W. Appel
- 掲載: ACM Transactions on Information and System Security (TISSEC), Vol. 14, No. 2, Article 18, 29ページ, 2011年9月
- 確認先: https://doi.org/10.1145/2019599.2019603 および著者公開版 https://www.cs.princeton.edu/~appel/voting/SealsOnVotingMachines.pdf （PDF本文を取得して内容を直接確認した）

内容の要約を述べる。著者はニュージャージー州の投票機に使われた封印の運用を、訴訟の専門家証人として調査した。投票機のキャビネットの錠はウェハータンブラー錠であり、著者はピッキングの経験がまったくない状態から、40ドル未満の工具と1、2時間の練習で開けられるようになり、練習後は平均13秒（2台の投票機で10回試行）で開錠できた。粘着テープ型の封印はヒートガンを80秒当てて40秒かけて剥がすだけで「VOID」の文字を出さずに外せた。ケーブル錠型の封印は初回の実機試行で50秒で外れた。州が次々に導入した3世代の封印体制すべてについて、著者は素人でも破れることを示し、法廷では全封印の取り外しと再取り付けを45分未満（そのうち7分は封印が無くても必要なねじとROMの着脱の時間）で実演した。結論として、封印は運用手順がなければ「粘着テープの偽薬」にすぎないと述べている。

CipherFluteとの関係を述べる。CipherFluteが「日用品に偽装すれば探索と読み出しの手間が増える」と述べるとき、その手間はまさにこの論文が測っている種類の量である。また、この論文は「物理的な防護は、それが遅延を生むか、事後に検出されるか、のどちらかを満たさなければ価値がない」という判定基準を明示しており、CipherFluteの物理層の価値もこの基準で自己評価すべきである。

脅威の度合いは「高」である。理由を述べる。物理層による保護が、素人が数十分で無効化できる程度のものであることを、査読付きの主要ジャーナルで具体的な秒数とともに示した研究であり、CipherFluteの「探索コストの引き上げ」という定性的な主張をそのまま書くことを許さない。逆に言えば、この論文を引いて「我々の物理層もこの桁の防護しか与えない」と明記すれば、主張は堅くなる。

### 3. Fatal Attraction: Salience, Naïveté, and Sophistication in Experimental "Hide-and-Seek" Games

- 著者: Vincent P. Crawford, Nagore Iriberri
- 掲載: American Economic Review, Vol. 97, No. 5, 2007年
- 確認先: https://doi.org/10.1257/aer.97.5.1731

内容の要約を述べる。この論文は、隠す側と探す側が対戦する実験ゲームの結果を、レベルk思考のモデルで説明したものである。理論的には隠す側は一様ランダムに隠すべきであるにもかかわらず、実験の参加者は目立つ（顕著性の高い）選択肢に体系的に引き寄せられ、あるいは逆にそれを避け、その傾向が探す側に予測されて利用される。結果として、隠す側の成功率は理論的な均衡値から系統的にずれる。著者らはこの現象を「致命的な魅力」と呼び、素朴な隠し手と洗練された探し手の間に生じる非対称を定量化している。

CipherFluteとの関係を述べる。CipherFluteの利用者は、どの日用品に笛を仕込むかを自分で選ぶ。この論文は、人間が隠し場所を選ぶときに体系的な偏りを持ち、その偏りが敵に読まれることを実験で示している。したがって「日用品に偽装すれば探索コストが上がる」という主張は、隠し場所の選び方が敵に予測されない限りにおいてのみ成り立つ。

脅威の度合いは「中」である。理由を述べる。CipherFluteの主張を直接否定するわけではないが、その主張の成立条件（隠し場所の選択の予測不能性）を明示的に突きつける実証研究であり、引用して差分と限界を述べる必要がある。とくにCipherFluteが「探索コストの引き上げ」を売りにする以上、隠す側の偏りに触れないのは片手落ちである。

### 4. Rare items often missed in visual searches ／ Low target prevalence is a stubborn source of errors in visual search tasks

- 著者: Jeremy M. Wolfe, Todd S. Horowitz, Naomi M. Kenner（2005年）／ Jeremy M. Wolfe, Todd S. Horowitz, Michael J. Van Wert, Naomi M. Kenner, Skyler S. Place, Nour Kibbi（2007年）
- 掲載: Nature, Vol. 435, 2005年 ／ Journal of Experimental Psychology: General, Vol. 136, No. 4, 2007年
- 確認先: https://doi.org/10.1038/435439a および https://doi.org/10.1037/0096-3445.136.4.623

内容の要約を述べる。2005年のNature論文は、探索課題で標的の出現率が低いほど見落としが劇的に増えることを示した。出現率が50パーセントのときの見落としが7パーセント程度であるのに対し、1パーセントのときは30パーセント程度まで跳ね上がる。2007年の論文はこの効果が訓練やフィードバックでは容易に消えない頑健なものであることを、複数の実験で確かめている。空港の手荷物X線検査のように、探すべきものがめったに存在しない現場でこの効果が問題になることが繰り返し指摘されている。

CipherFluteとの関係を述べる。CipherFluteの「日用品に偽装する」という戦略が効く理由の最も科学的な裏づけがこれである。敵が「この本立てには秘密が入っているかもしれない」と考えていない限り、目の前にあっても見落とされる確率が高い。逆に、敵が特定の対象を疑って集中的に調べる状況では出現率効果は働かず、偽装の効果は急速に失われる。

脅威の度合いは「中」である。理由を述べる。新規性を脅かすというより、CipherFluteの主張を支える最良の外部証拠であり、引用しないと「探索コストが上がる」という主張が単なる直感に見えてしまう。同時に、出現率効果が成り立つ条件（敵が疑っていないこと）を明示することで、脅威モデルの記述が精密になる。

### 5. Replication Prohibited: Attacking Restricted Keyways with 3D-Printing

- 著者: Ben Burgess, Eric Wustrow, J. Alex Halderman
- 掲載: USENIX Workshop on Offensive Technologies (WOOT), 2015年
- 確認先: https://scholar.archive.org/work/fe05aa46-5454-46d5-a0c1-0334d8133ca6 （Internet Archive Scholarの書誌レコードと、そこから辿れる保存済み全文PDF https://www.usenix.org/system/files/conference/woot15/woot15-paper-burgess.pdf ）

内容の要約を述べる。この研究は、「複製禁止（Do Not Duplicate）」や特許で守られた制限付きキーウェイの錠前が、消費者向けの3Dプリンタによって実質的に無力化されることを示した。著者らは制限付きキーウェイの鍵をモデル化して出力し、実際の錠を開けることに成功している。物理的な鍵の安全性が「鍵素材（キーブランク）の入手困難性」という供給側の制約に依存していたところ、その制約が積層造形によって消えたことを示す点に主眼がある。

CipherFluteとの関係を述べる。CipherFluteは3Dプリントされた形状そのものが秘密の担体であり、論文は「形状を計測されれば無音で読める、複製も容易」と宣言している。この研究は、その宣言が抽象的な可能性ではなく、CipherFluteとまったく同じ技術（家庭用3Dプリンタ）で既に実証された事実であることを裏づける。同時に、物理鍵の分野で「複製困難性に頼る設計」が崩れた歴史をそのまま引用できる。

脅威の度合いは「中」である。理由を述べる。CipherFluteの主張を崩すのではなく、その脅威モデルの正しさを外部から支持する。ただし、CipherFluteが物理層の複製困難性に少しでも寄りかかった書き方をしている箇所があれば、この研究の存在によってその記述は成立しなくなるため、必ず引用して線を引く必要がある。

### 6. 3Dプリンタによる印影からの印章の偽造

- 著者: 木村悠生, 山元陽佑雅, 榎竜盛, 上原哲太郎
- 掲載: マルチメディア，分散，協調とモバイル（DICOMO）シンポジウム2023論文集, pp. 1269–1276, 2023年
- 確認先: https://cir.nii.ac.jp/crid/1050860532220398464

内容の要約を述べる。この研究は、押された印影の画像から、消費者が入手できる安価な3Dプリンタを用いて印章（はんこ）を偽造できることを示した。偽造した印章で照合実験を行い、姓の種類や文字数といった要因が判別精度にどう影響するかを評価している。さらに、偽造の容易さと、偽造を困難にしうる要素の双方を検討している。

CipherFluteとの関係を述べる。日本社会で長く物理的な認証トークンとして機能してきた印章が、その出力（印影）を観測するだけで3Dプリンタで再現されるという構図は、CipherFluteの笛が「音を聞かれれば、あるいは形を測られれば再現される」という構図と同型である。日本語圏の読者に脅威モデルを説明するうえで、これ以上に通りのよい先行事例はない。

脅威の度合いは「中」である。理由を述べる。CipherFluteの新規性を直接脅かしはしないが、「観測可能な物理トークンは3Dプリンタで複製される」という論点の国内の一次事例であり、脅威モデルの節で引用すべきである。引用しないと、日本の査読者から「印章偽造の議論を知らないのか」と問われる可能性がある。

### 7. Audio and Optical Cryptography ／ Nonbinary Audio Cryptography ／ 物理的復元が容易な音響秘密分散法

- 著者: Yvo Desmedt, Shuang Hou, Jean-Jacques Quisquater（1998年）／ Yvo Desmedt, Tri V. Le, Jean-Jacques Quisquater（2000年）／ 徳重佑樹, 三澤裕人, 吉田文晶（2015年）
- 掲載: ASIACRYPT'98（LNCS）, 1998年 ／ Information Hiding 2000（LNCS）, 2000年 ／ 電子情報通信学会技術研究報告, Vol. 115, No. 38, pp. 75–80, 2015年5月
- 確認先: https://doi.org/10.1007/3-540-49649-1_31 、 https://doi.org/10.1007/10719724_33 、 https://cir.nii.ac.jp/crid/1520572358843442048

内容の要約を述べる。Desmedtらの音響暗号は、視覚暗号（透明シートを重ねると秘密の像が現れる方式）の音響版であり、複数の音響シェアを同時に再生すると、人間の聴覚が干渉によって秘密を復元するという仕組みである。計算機なしに人間の感覚器だけで復号できる点が要点である。2000年の論文は二値に限らない拡張を扱う。徳重らの日本語の報告は、波の干渉と周波数分割を用いて「物理的な復元が容易な」音響秘密分散法を提案しており、キーワードとして音響秘密分散、秘密分散、波の干渉、周波数分割が挙げられている。

CipherFluteとの関係を述べる。CipherFluteは音の高さを符号の語彙にし、秘密分散に秘匿を負わせ、「2枚そろって初めてハートが現れるカード」という実装を持つ。音響領域での秘密分散と、物理的に重ねると秘密が現れるという発想は、この系列が1998年から扱ってきたものである。CipherFluteの新規性は、音を秘密分散の復元手段に使うことではなく、電源も電子部品も持たない造形物が音の高さで少量の情報を運ぶことにあると、明確に切り分ける必要がある。

脅威の度合いは「中」である。理由を述べる。CipherFluteが「音で秘密を運ぶ」あるいは「2つそろって初めて意味を持つ物理媒体」という点に新規性を置くと、この系列と正面から衝突する。逆に、符号化された情報を受動的な造形物が発音するという点に限定すれば衝突しない。したがって必ず引用して差分を述べる必要がある。

### 8. Visual Cryptography

- 著者: Moni Naor, Adi Shamir
- 掲載: Advances in Cryptology — EUROCRYPT'94（LNCS）, 1995年
- 確認先: https://doi.org/10.1007/bfb0053419

内容の要約を述べる。秘密の画像を複数枚の透明シートに分割し、規定枚数を重ね合わせたときにだけ人間の目に像が現れる方式である。計算機を使わずに人間の視覚系が復号を行い、規定枚数未満のシートからは情報理論的にまったく情報が漏れない。以後の「物理的な暗号プリミティブ」研究の出発点となった。

CipherFluteとの関係を述べる。CipherFluteの実装のひとつである「2枚そろって初めてハートが現れるカード」は、視覚暗号の閾値2の構成そのものの見た目を持つ。CipherFluteのカードが実際に行っているのはShamirの秘密分散の物理的な担体であって視覚暗号ではないが、読者が混同する可能性が高い。

脅威の度合いは「中」である。理由を述べる。デモの見た目が視覚暗号と重なるため、引用して「見た目は似ているが、秘匿は視覚的な重ね合わせではなく秘密分散に負わせている」と明示しないと、既知手法の焼き直しと誤読される危険がある。

### 9. 3Dプリンタによるオープン装置や特殊カードケースの作成と対称関数の秘密計算への適用

- 著者: 伊藤優樹, 四方隼人, 水木敬明, 菅沼拓夫
- 掲載: コンピュータセキュリティシンポジウム（CSS）2023論文集, pp. 192–199, 2023年10月
- 確認先: https://cir.nii.ac.jp/crid/1050579444484578048

内容の要約を述べる。この研究は、カードベース暗号プロトコルを実行するための物理装置を3Dプリンタで作製したものである。複数のカードを同時に操作する「カードオープン装置」と特殊なカードケースを設計し、効率的なコミットメントの加算を可能にして、対称関数の秘密計算に有用であることを示している。カードベース暗号の物理実装という日本発の系列に、積層造形を持ち込んだ位置づけになる。

CipherFluteとの関係を述べる。「家庭用3Dプリンタで作った受動的な物体が暗号的な役割を担う」という一点で、CipherFluteと最も近い日本語圏の研究である。ただし、この研究の物体は秘密を保持する媒体ではなく、プロトコルを人が実行するための治具である。

脅威の度合いは「中」である。理由を述べる。国内の査読者が真っ先に思い浮かべる隣接研究であり、引用して「向こうは物理暗号プロトコルの実行装置、こちらは秘密を運ぶ受動的な記憶媒体」と差分を述べる必要がある。

### 10. BIP-93 codex32: Checksummed SSSS-aware BIP32 seeds

- 著者: Leon Olsson Curr, Pearlwort Sneed, Andrew Poelstra
- 掲載: Bitcoin Improvement Proposal 93（公式リポジトリで公開）
- 確認先: https://github.com/bitcoin/bips/blob/master/bip-0093.mediawiki

内容の要約を述べる。codex32は、BIP-32のマスターシードを、誤り訂正符号付きのbase32文字列として保管するための規格である。BCH符号により、8文字までの誤りを検出し、4文字までの置換誤りを訂正できる。Shamirの秘密分散に対応し、最大31個のシェアに分割して2個から9個の閾値で復元できる。最大の特徴は、すべての計算が参照表だけで実行できるように設計されていることであり、規格自体が「チェックサムの計算と検証、シードの分割と復元を、紙と鉛筆だけで完全に行える」と述べている。

CipherFluteとの関係を述べる。CipherFluteは、リカバリーシードを対象に、Reed–Solomon符号による誤り訂正と秘密分散を組み合わせている。codex32は同じ目的（種の物理バックアップ）に対して、誤り訂正符号と秘密分散を組み合わせ、しかも電子機器を使わない手計算での復元まで担保している。現在の論文はSLIP-39とSSKRを引いているが、codex32を引いていない。

脅威の度合いは「中」である。理由を述べる。CipherFluteの符号設計（誤り訂正付きの、人が扱える種の保管形式）と目的が完全に重なるため、引用しないのは調査不足に見える。差分は明確であり、codex32は文字列という「読めば分かる」担体を使うのに対し、CipherFluteは日用品に溶け込む物理形状を担体にする。この対比はむしろCipherFluteの位置づけを鮮明にする。

### 11. Chameleon Devices（カメレオン・デバイス）

- 著者: Jennifer Pearson, Simon Robinson, Matt Jones, Anirudha Joshi, Shashank Ahire, Deepak Sahoo, Sriram Subramanian
- 掲載: Proceedings of the 2017 CHI Conference on Human Factors in Computing Systems, 2017年
- 確認先: https://doi.org/10.1145/3025453.3025482 および https://scholar.archive.org/work/2319f254-ce88-4c19-85e6-91a31b2c118c

内容の要約を述べる。この研究は、モバイル機器が周囲の日用品に見えるように外見を変える「カメレオン・デバイス」の概念を提案し、盗難や不要な注目を避けながら目立たずに操作するという用途を検討した。ケープタウン、バンガロール、ムンバイ、ナイロビでの調査に基づいており、機器を魅力的な標的に見せない偽装が、利用者の安全と安心にどう寄与するかを扱っている。

CipherFluteとの関係を述べる。「価値のある物を日用品に偽装することで、敵の注意と探索の対象から外す」という発想を、ヒューマンコンピュータインタラクションの主要会議で扱った数少ない研究である。CipherFluteの偽装戦略の直系の先行研究として位置づけられる。

脅威の度合いは「中」である。理由を述べる。CipherFluteの「日用品への偽装」という主張が、HCI分野で既に提案され現地調査まで行われていることを示す。ただし対象は電源を持つ携帯機器であり、秘密情報の担体としての符号設計は扱っていないため、差分は明確に述べられる。

### 12. Safecracking for the computer scientist

- 著者: Matt Blaze
- 掲載: ペンシルベニア大学 計算機情報科学科 技術報告, 2004年12月7日草稿（同年12月21日改訂）
- 確認先: https://www.mattblaze.org/papers/safelocks.pdf （PDF本文を取得して内容を直接確認した）

内容の要約を述べる。金庫と金庫錠の安全性を計算機科学の視点から概観した文献である。物理セキュリティの世界では、安全性が「破るのにどれだけ時間がかかるか、どんな道具が必要か、どんな痕跡が残るか」という多次元の量として定義されており、Underwriters Laboratoriesの最上位の格付けでさえ15分、30分、60分という時間で表されることを指摘している。攻撃は、痕跡をまったく残さない「surreptitious」、通常の使用では気づかれない痕跡を残す「covert」、明白な痕跡を残す「forced」に分類される。また、金庫業界では「security-by-obscurity」が依然として中心的な信条であり続けていることを、情報セキュリティの立場から批判的に検討している。

CipherFluteとの関係を述べる。CipherFluteが「探索コストの引き上げ」を主張するなら、その主張は本来この語彙（所要時間、必要な道具、残る痕跡の3軸）で書かれるべきである。また「security-by-obscurity」を物理世界がどう扱ってきたかという議論の枠組みを、そのまま借りられる。

脅威の度合いは「中」である。理由を述べる。新規性を脅かすものではないが、CipherFluteの脅威モデルの節を専門的な水準に引き上げるために引用が必要であり、これを欠くと物理セキュリティの語彙を知らずに議論していると見なされる。

### 13. Obfuscation: A User's Guide for Privacy and Protest

- 著者: Finn Brunton, Helen Nissenbaum
- 掲載: MIT Press, 2015年
- 確認先: https://doi.org/10.7551/mitpress/9780262029735.001.0001 （章ごとのDOIも確認した。例として「Will Obfuscation Work?」が https://doi.org/10.7551/mitpress/9780262029735.003.0006 ）

内容の要約を述べる。この書籍は、強い敵に対して秘匿を達成できないとき、ノイズや偽装によって敵のコストを引き上げるという「難読化（obfuscation）」の戦略を体系化したものである。「難読化はうまくいくのか」「難読化は正当化されるのか」という章を設け、弱者が非対称な力関係のもとで取りうる手段としての難読化を、倫理と有効性の両面から検討している。

CipherFluteとの関係を述べる。CipherFluteの物理層の位置づけ、すなわち「秘匿はできないが探索コストを上げる」という主張は、まさに難読化の枠組みそのものである。理論的な後ろ盾としてこの書籍を引くことで、主張の位置づけが明確になる。

脅威の度合いは「中」である。理由を述べる。CipherFluteの中核的な言い分に既存の理論的枠組みが存在することを示すため、引用して自らの位置づけを述べる必要がある。引用しないと「探索コストの引き上げ」という概念を独自に発明したかのように読まれる。

### 14. Expert Decision Making in Burglars ／ Learning on the job

- 著者: Claire Nee, Amy Meenaghan（2006年）／ Claire Nee, Jean-Louis van Gelder, Marco Otte, Zarah Vernham, Amy Meenaghan（2019年）
- 掲載: The British Journal of Criminology, Vol. 46, No. 5, 2006年 ／ Criminology, Vol. 57, 2019年
- 確認先: https://doi.org/10.1093/bjc/azl013 および https://doi.org/10.1111/1745-9125.12210

内容の要約を述べる。2006年の研究は、実際に住居侵入窃盗を行った受刑者への面接に基づいて、彼らの探索が自動化された熟練の判断に支えられていることを示した。2019年の研究は、仮想環境の中で実際の侵入窃盗犯に「仮想の犯行」を行わせ、その探索経路と対象選択を非侵入者と比較して、熟練者の探索が体系的で効率的であることを実験的に示した。いずれも、探す側が何を手がかりにどこを見るかを実証的に扱っている。

CipherFluteとの関係を述べる。CipherFluteの「日用品に偽装すれば探索コストが上がる」という主張の相手方は、多くの場合この種の熟練した探索者である。熟練者の探索が高度に自動化され効率的であるという知見は、素朴な偽装の効果を割り引く方向に働く。

脅威の度合いは「中」である。理由を述べる。CipherFluteの主張を直接否定するわけではないが、探索側の能力を実証的に測った数少ない研究であり、「敵は素人ではない」という前提を論文に持ち込むために引用が必要である。

### 15. Physical One-Way Functions

- 著者: Ravikanth Pappu, Ben Recht, Jason Taylor, Neil Gershenfeld
- 掲載: Science, Vol. 297, 2002年
- 確認先: https://doi.org/10.1126/science.1074376

内容の要約を述べる。微細な構造の乱雑さに由来する、製造者ですら再現できない物理的な一方向性関数（後に物理的複製不能関数、PUFと呼ばれる）を提案した論文である。透明媒体に散乱体をランダムに封じ込め、レーザー照射に対する散乱パターンを応答として使う。物理的な複製が困難であることを安全性の根拠にする設計の出発点である。

CipherFluteとの関係を述べる。CipherFluteはこの設計思想の正反対の位置にある。CipherFluteの笛は決定論的に設計され、形状が分かれば誰でも同じものを刷れる。この対比を明示すると、CipherFluteが何に依拠し何に依拠していないかがはっきりする。

脅威の度合いは「中」である。理由を述べる。「物理的な物体に秘密を持たせる」研究として最も有名な系列であり、引用せずに議論すると、査読者から「なぜ複製不能性を狙わないのか」と当然に問われる。引用して「複製不能性は狙わず、秘匿は秘密分散に負わせる」と明言することで、その問いを先回りできる。

---

## 背景として押さえるべき文献

以下は脅威の度合いが「低」であり、背景として引用する程度でよいものである。すべて一次資料で実在を確認した。

### 物理鍵と錠前の複製

- Benjamin Laxton, Kai Wang, Stefan Savage, "Reconsidering physical key secrecy: teleduplication via optical decoding", ACM CCS 2008. https://doi.org/10.1145/1455770.1455830 。写真から鍵の刻みを復元して複製する攻撃（通称Sneakey）である。CipherFluteの「観測されれば複製される」という宣言の古典的な出発点にあたる。
- Rory Smith, Tilo Burghardt, "DeepKey: Towards End-to-End Physical Key Replication From a Single Photograph", arXiv:1811.01405, 2018年11月4日. https://arxiv.org/abs/1811.01405 。1枚の写真から深層学習で3Dプリント可能な鍵モデルを自動生成し、実際の錠を開けている。
- Soundarya Ramesh, Harini Ramprasad, Jun Han, "Listen to Your Key: Towards Acoustics-based Physical Key Inference", ACM HotMobile 2020. https://doi.org/10.1145/3376897.3377853 。鍵を挿入するときの音から刻みを推定する攻撃である。
- Soundarya Ramesh ほか, "Acoustics to the Rescue: Physical Key Inference Attack Revisited", USENIX Security Symposium 2021. https://scholar.archive.org/work/8e583365-a488-4b3a-904b-d84744fab8fd 。上記の実用性を高めたKeynergyという手法である。音を情報の担体として扱う点でCipherFluteと表裏の関係にある。
- Soundarya Ramesh ほか, "Listen to your key: Towards acoustics-based physical key inference", The Journal of the Acoustical Society of America, 2024年. https://doi.org/10.1121/10.0026832 。上記系列のジャーナル版である。
- Matt Blaze, "Rights amplification in master-keyed mechanical locks", IEEE Security & Privacy, 2003年. https://doi.org/10.1109/msecp.2003.1193208 。1本の子鍵からマスターキーを合成できることを示した研究であり、物理鍵の安全性を計算機科学の語彙で論じた初期の代表例である。
- Deviant Ollam, "Master-Keyed Systems", Keys to the Kingdom（書籍の章）, 2012年. https://doi.org/10.1016/b978-1-59749-983-5.00003-8 。実務側からの解説である。

### 封印と改ざん検知

- Roger G. Johnston, "Effective Vulnerability Assessment of Tamper-Indicating Seals", Journal of Testing and Evaluation, 1997年. https://doi.org/10.1520/jte11883j 。封印の脆弱性評価の方法論である。
- Roger Johnston, "Tamper-Indicating Seals", American Scientist, 2006年. https://doi.org/10.1511/2006.62.515 。一般向けの総説である。
- Roger G. Johnston, Michael J. Timmons, Jon S. Warner, "Protecting Nuclear Safeguards Monitoring Data from Tampering", Science & Global Security, 2007年. https://scholar.archive.org/search?q=%22tamper-indicating+seals%22+defeat で書誌を確認した。

### 物体の同定と偽造対策

- William Clarkson, Tim Weyrich, Adam Finkelstein, Nadia Heninger, J. Alex Halderman, Edward W. Felten, "Fingerprinting Blank Paper Using Commodity Scanners", IEEE Symposium on Security and Privacy 2009. https://doi.org/10.1109/sp.2009.7 。白紙の繊維の乱雑さを市販スキャナで指紋化する研究である。
- Zhengxiong Li ほか, "PrinTracker", ACM CCS 2018. https://doi.org/10.1145/3243734.3243735 。3Dプリント物からプリンタ個体を同定する研究である。
- Antonella Sola ほか, "How Can We Provide Additively Manufactured Parts with a Fingerprint? A Review of Tagging Strategies in Additive Manufacturing", Materials, 2021年. https://scholar.archive.org/search?q=physical+unclonable+function+3D+printed+object+anti-counterfeiting で書誌を確認した。積層造形物への標識付けの総説である。
- Muhammad Usama, Ulas Yaman, "Embedding Information into or onto Additively Manufactured Parts: A Review of QR Codes, Steganography and Watermarking Methods", Materials, Vol. 15, 2596, 2022年. https://doi.org/10.3390/ma15072596 。積層造形物への情報埋め込みの総説であり、光学コード、ステガノグラフィ、透かしを整理している。音響による読み出しは扱われていない。
- Timo Richter, Stephan Escher, Dagmar Schönfeld, Thorsten Strufe, "Forensic Analysis and Anonymisation of Printed Documents", ACM IH&MMSec 2018. https://doi.org/10.1145/3206004.3206019 。カラープリンタが印刷物に埋め込む追跡ドットの解析と除去である。実社会に大規模展開された物理的ステガノグラフィの数少ない例である。

### 存在を隠す技術（ステガノグラフィと否認可能性）

- Ross Anderson, Roger Needham, Adi Shamir, "The Steganographic File System", Information Hiding 1998（LNCS）. https://doi.org/10.1007/3-540-49380-8_6 。
- Christian Cachin, "An Information-Theoretic Model for Steganography", Information Hiding 1998（LNCS）. https://doi.org/10.1007/3-540-49380-8_21 、およびジャーナル版 Information and Computation, 2004年. https://doi.org/10.1016/j.ic.2004.02.003 。「存在を隠す」ことの安全性を情報理論的に定義した基礎文献である。CipherFluteが「物理層に暗号学的な秘匿の力は無い」と述べるとき、その「秘匿」の定義としてこれを引ける。
- Ran Canetti, Cynthia Dwork, Moni Naor, Rafail Ostrovsky, "Deniable Encryption", CRYPTO'97（LNCS）. https://doi.org/10.1007/bfb0052229 。
- Adam Skillen, Mohammad Mannan, "Mobiflage: Deniable Storage Encryption for Mobile Devices", IEEE Transactions on Dependable and Secure Computing, 2014年. https://doi.org/10.1109/tdsc.2013.56 。
- Timothy M. Peters, Mark A. Gondree, Zachary N. J. Peterson, "DEFY: A Deniable, Encrypted File System for Log-Structured Storage", NDSS 2015. https://doi.org/10.14722/ndss.2015.23078 。
- Michal Kedziora, Yang-Wai Chow, Willy Susilo, "Improved Threat Models for the Security of Encrypted and Deniable File Systems", 2017年. https://doi.org/10.1007/978-981-10-5281-1_24 。否認可能ストレージが周辺の痕跡から暴かれるという議論である。物理世界でも「秘密がある痕跡」が別経路から漏れる点で示唆的である。
- Catherine Taylor Clelland, Viviana Risca, Carter Bancroft, "Hiding messages in DNA microdots", Nature, Vol. 399, 1999年. https://doi.org/10.1038/21092 。物理的ステガノグラフィの古典であり、微小点という日常的な記号に秘密を隠す。
- Yinglei Wang, Wing-kei Yu, Sarah Q. Xu, Edwin Kan, G. Edward Suh, "Hiding Information in Flash Memory", IEEE Symposium on Security and Privacy 2013. https://scholar.archive.org/search?q=%22physical+steganography%22 の結果一覧で書誌を確認した。デバイスの物理的な特性そのものに情報を隠す例である。
- Ching-Chun Chang, Yijie Lin, Isao Echizen, "Cyber-Physical Steganography in Robotic Motion Control", arXiv:2501.04541, 2025年1月8日. https://arxiv.org/abs/2501.04541 。「物理的ステガノグラフィ」という語をタイトル級で使う数少ない近年の研究であり、ロボットの動きに秘密を埋め込む。CipherFluteの「物理現象そのものを担体にする」という発想の同時代的な隣接例である。
- Katarzyna Koptyra, Marek R. Ogiela, "Subliminal Channels in Visual Cryptography", Cryptography, 2022年. https://scholar.archive.org/search?q=Koptyra+Ogiela+steganography+physical+objects+information+hiding で書誌を確認した。

### 物理的な暗号プリミティブ

- Takaaki Mizuki, Michihito Kumamoto, Hideaki Sone, "The Five-Card Trick Can Be Done with Four Cards", ASIACRYPT 2012（LNCS）. https://doi.org/10.1007/978-3-642-34961-4_36 。カードベース暗号の代表例である。
- Ronen Gradwohl, Moni Naor, Benny Pinkas, Guy N. Rothblum, "Cryptographic and Physical Zero-Knowledge Proof Systems for Solutions of Sudoku Puzzles", FUN 2007（LNCS）https://doi.org/10.1007/978-3-540-72914-3_16 、ジャーナル版 Theory of Computing Systems, 2008年 https://doi.org/10.1007/s00224-008-9119-9 。日用品（カードや封筒）で暗号プロトコルを実行する研究である。

### 探索と隠蔽の実証

- Anton Bolfing, Tobias Halbherr, Adrian Schwaninger, "How Image Based Factors and Human Factors Contribute to Threat Detection Performance in X-Ray Aviation Security Screening", USAB 2008（LNCS）. https://doi.org/10.1007/978-3-540-89350-9_30 。X線検査における検出性能の規定要因を扱う。
- D. Hardmeier, F. Hofer, A. Schwaninger, "The X-ray object recognition test (X-ray ORT)", International Carnahan Conference on Security Technology 2005. https://doi.org/10.1109/ccst.2005.1594876 。重なりや向きによって物体が見つけにくくなることを測る標準テストである。
- Eugene Winograd, Robert M. Soloway, "On forgetting the locations of things stored in special places", Journal of Experimental Psychology: General, Vol. 115, No. 4, 1986年. https://doi.org/10.1037/0096-3445.115.4.366 。「特別な場所に隠すほど思い出せなくなる」という古典的知見である。CipherFluteの利用者自身が隠し場所を忘れる危険を論じるときに使える。
- Alan S. Brown, Tamara A. Rahhal, "Hiding valuables: A questionnaire study of mnemonically risky behavior", Applied Cognitive Psychology, Vol. 8, No. 2, 1994年. https://doi.org/10.1002/acp.2350080205 。貴重品を隠す行動とその記憶上の危険性の質問紙調査である。
- John Knowles, Nicola Persico, Petra Todd, "Racial Bias in Motor Vehicle Searches: Theory and Evidence", Journal of Political Economy, 2001年. https://scholar.archive.org/search?q=concealment+contraband+search+detection+probability+police+experiment で書誌を確認した。捜索が実際に禁制品を発見する確率を扱う経済学の代表的研究である。
- Steve Alpern, Shmuel Gal, The Theory of Search Games and Rendezvous, Springer（International Series in Operations Research & Management Science）. 章のDOIとして https://doi.org/10.1007/0-306-48212-6_5 などを確認した。隠す側と探す側の最適戦略を扱う数理的枠組みである。

### 難読化と不透明性の理論

- Woodrow Hartzog, Frederic D. Stutzman, "The Case for Online Obscurity", 2010年（SSRN）. https://doi.org/10.2139/ssrn.1597745 。「秘匿ではない不透明性」に法的な保護価値を認める議論であり、CipherFluteの物理層の位置づけと平行する。
- Ari Juels, Ronald L. Rivest, "Honeywords", ACM CCS 2013. https://doi.org/10.1145/2508859.2516671 。偽の候補を混ぜて攻撃者のコストを上げ、かつ攻撃を検出可能にする設計である。CipherFluteが将来おとりの笛を混ぜる拡張を考えるなら直接の参考になる。

### 暗号資産の鍵管理

- Myrto Arapinis, Andriana Gkaniatsou, Dimitris Karakostas, Aggelos Kiayias, "A Formal Treatment of Hardware Wallets", Financial Cryptography and Data Security 2019（LNCS）. https://doi.org/10.1007/978-3-030-32101-7_26 。
- Katharina Krombholz, Aljosha Judmayer, Matthias Gusenbauer, Edgar Weippl, "The Other Side of the Coin: User Experiences with Bitcoin Security and Privacy", Financial Cryptography and Data Security（LNCS, 2017年刊）. https://doi.org/10.1007/978-3-662-54970-4_33 。
- Artemij Voskobojnikov, Oliver Wiese, Masoud Mehrabi Koushki, Volker Roth, Konstantin Beznosov, "The U in Crypto Stands for Usable: An Empirical Study of User Experience with Mobile Cryptocurrency Wallets", ACM CHI 2021. https://doi.org/10.1145/3411764.3445407 。
- Hristo Bojinov, Daniel Sanchez, Paul Reber, Dan Boneh, Patrick Lincoln, "Neuroscience meets cryptography", Communications of the ACM, 2014年. https://doi.org/10.1145/2594445 。強要（いわゆるゴムホース攻撃）に対して、本人が鍵を明かせないようにする設計である。CipherFluteの強要下の脅威を論じる際の対極の設計として引ける。

### 日本語圏のその他の関連

- 加藤大弥, 林達也, 砂原秀樹, 「サイバーフィジカル時代の物理媒体による認証・識別に関する考察」, コンピュータセキュリティシンポジウム2017論文集. https://cir.nii.ac.jp/crid/1050011097170108928 。
- 吉田妃菜, 松崎なつめ, 「紙を用いた立体QRコードの基礎検討」, コンピュータセキュリティシンポジウム2021論文集. https://cir.nii.ac.jp/crid/1050855522064066816 。
- ピヤラット シラパスパコォンウォン, 鈴木雅洋, 海野浩, 「3Dプリント用デジタルデータの著作権保護のための情報ハイディング技術」, 電子情報通信学会技術研究報告, 2014年. https://cir.nii.ac.jp/crid/1520009408040188672 。
- 茂出木敏雄, 「違法造形物の3Dプリンタによる製造を規制するための3Dデータ照合技術に関する研究」, 尚美学園大学芸術情報研究, 2016年. https://cir.nii.ac.jp/crid/1050282677910856960 、および高精度化の続報（2018年）https://cir.nii.ac.jp/crid/1050282677911423360 。

---

## 未検証のまま残ったもの

以下は、存在の可能性が高いと考えられるものの、この調査の範囲では一次資料に到達できなかったため、論文に書く場合は改めて確認が必要である。

1. Roger G. Johnston, Anthony R. E. Garcia, "Vulnerability assessment of security seals", Journal of Security Administration, 1997年。アペルのTISSEC論文が [Johnston and Garcia 1997] として繰り返し引用しており、実在はほぼ確実である。ただしCrossrefにはこの書誌が登録されておらず、当該誌のページにも到達できなかった。巻号ページを確認できていない。同じ内容に近いものとして、Crossrefで確認できた Johnston, "Effective Vulnerability Assessment of Tamper-Indicating Seals", Journal of Testing and Evaluation, 1997年（https://doi.org/10.1520/jte11883j ）を代わりに引くことができる。
2. Alexei Czeskis, David J. St. Hilaire, Karl Koscher, Steven D. Gribble, Tadayoshi Kohno, Bruce Schneier, "Defeating Encrypted and Deniable File Systems: TrueCrypt v5.1a and the Case of the Tattling OS and Applications", USENIX HotSec 2008。否認可能ストレージが周辺の痕跡から暴かれることを示した有名な論文である。USENIXのサイトがHTTP 403を返し、Internet ArchiveのWayback Machineにも到達できなかったため、書誌を一次資料で確認できていない。同趣旨の内容は、確認済みの Kedziora ら（2017年）で代替できる。
3. Sneakeyのプロジェクトページ。カリフォルニア大学サンディエゴ校の公開ページを複数のURLで試したがすべて404であった。論文本体（CCS 2008）はCrossrefで確認済みであるため、引用には支障がない。
4. アメリカ国土安全保障省監察官室による空港保安検査の覆面テストの失敗率（95パーセントという数字が広く報じられている）。政府の一次報告書に到達できなかった。出現率効果の実務的な裏づけとして魅力的だが、確認できるまで論文には書かないほうがよい。
5. Bruce Schneier, Beyond Fear（2003年）における「セキュリティ劇場（security theater）」の議論。書籍の存在は広く知られているが、出版社ページに当たっていない。
6. 「隠し金庫（diversion safe）」「日用品に偽装した容器」を扱う学術文献。Internet Archive Scholarで検索した結果、1950年代の歯科医師会誌の広告や1881年の雑誌記事など、学術研究ではないものしか出てこなかった。存在しないという判断に傾いているが、犯罪学や税関の実務文献まで当たり切れていない。

---

## この切り口で見つからなかったこと

以下は、相当量の検索を行った結果として「見つからなかった」と述べられるものであり、CipherFluteの新規性の主張の根拠に使える。ただし、Web検索の予算が尽きたためCrossref、Internet Archive Scholar、arXiv、CiNii Research、DOI解決先の直接取得に依拠した点は割り引いて読む必要がある。

1. 日用品に偽装した物理的な担体に暗号鍵やリカバリーシードを保管し、その偽装の効果を実験で定量化した研究は見つからなかった。偽装の効果を測った研究は、視覚探索の出現率効果（ウルフら）、X線検査（シュヴァニンガーら）、隠れ場所選択のゲーム実験（クロフォードとイリベリ）、住居侵入窃盗犯の探索行動（ニーら）といった別分野に散在しており、いずれも「秘密の担体を日用品に偽装する」という設定では行われていない。CipherFluteが仮に小規模でも探索実験を行えば、それ自体が新規の貢献になる。

2. 「物理的ステガノグラフィ（physical steganography）」という語を、物理的な人工物に秘密の存在を隠す技術として体系的に扱った研究分野は確立していない。この語で検索して出てくるのは、ほぼすべて画像や3Dメッシュのデジタルステガノグラフィである。例外は Chang らのロボット動作へのステガノグラフィ（arXiv 2025年）程度であり、造形物を担体とする体系的な議論は見当たらなかった。積層造形への情報埋め込みの総説（Usama と Yaman, 2022年）も、光学コード、電子透かし、内部構造への埋め込みを扱うのみで、「秘密が存在すること自体を隠す」という安全性の目標を立てていない。

3. 隠し金庫や偽装容器の有効性を測った学術研究は見つからなかった。この領域は商業製品と実務知に閉じており、査読を経た評価が存在しない。CipherFluteが「日用品への偽装」を主張する際、比較すべき先行の定量結果が存在しないこと自体を述べられる。

4. 強要下（いわゆる5ドルのレンチ攻撃）における暗号資産の物理バックアップの否認可能性を、体系的に扱った研究は見つからなかった。否認可能性の研究はファイルシステムと暗号方式に集中しており、物理的な担体に対する否認可能性は空白である。BIP-39のパスフレーズによる「隠しウォレット」は実務では知られているが、学術的な評価は見当たらない。

5. 音の高さを符号の語彙とし、基準となる音を混ぜて環境変動を打ち消し、誤り訂正符号を載せる、という構成を持つ物理的な記憶媒体は、この切り口の範囲では見つからなかった。音響領域の秘密分散（Desmedt ら、徳重ら）は存在するが、それらは複数のシェアを同時に鳴らして人間の聴覚が復元するという別の枠組みである。

6. 3Dプリントされた受動的な物体に、誤り訂正符号付きで暗号鍵を保管する研究は見つからなかった。arXivで「3D printed」「private key」「storage」を掛け合わせた検索の結果は0件であった。3Dプリンタと暗号の交差点にある研究は、伊藤らのカードベース暗号用の物理装置、および3Dプリント物の同定と偽造対策（PrinTracker、積層造形の標識付け総説）に限られる。

7. 封印や隠蔽の分野で、「物理層は秘匿を担わず、秘匿は秘密分散にのみ負わせる」という役割分担を明示的に宣言した設計は見つからなかった。物理セキュリティの文献（ジョンストン、ブレイズ）は物理層の限界を厳しく指摘するが、その限界を認めたうえで暗号的な秘匿を別レイヤに追い出す設計を提案してはいない。CipherFluteの脅威モデルの立て方は、この意味で新しい。

---

## 調べ残した穴

1. Web検索の予算がこのセッションの開始時点で既に上限に達していたため、一般のWeb検索を1回も使えなかった。DuckDuckGo、Bing、Mojeek、Marginaliaを直接取得する迂回も試みたが、CAPTCHAや403で実用にならなかった。したがって、学術データベースに載らない技術報告、DEF CONやBlack Hatの講演、特許、実務文献は、ほとんど拾えていない。とくに鍵の型どり（impressioning）、隠し金庫の実態、税関の摘発事例はこの層に集中していると思われる。

2. OpenAlexとSemantic Scholarが繰り返しHTTP 429を返し（OpenAlexは再試行まで約24時間と応答した）、被引用関係をたどる芋づる式の探索がほとんどできなかった。Johnstonの封印研究、Appelの投票機研究、Burgessらの3Dプリント鍵複製の被引用一覧をたどれば、さらに近い研究が出てくる可能性がある。

3. ACM Digital Library、IEEE Xplore、USENIXの各サイトがいずれも403を返したため、抄録の確認をCrossrefと著者公開版に頼った。Chameleon Devices（CHI 2017）については抄録の全文を確認できておらず、内容の記述はInternet Archive Scholarに残る本文断片と検索結果の要約に基づく。論文に引用する前に抄録を確認したほうがよい。

4. 税関、警察、刑務所における隠匿物の捜索の成功率を扱う実証研究を、犯罪学と法執行の専門誌まで掘り下げられなかった。Knowles らの経済学的研究には到達したが、これは差別の検証が主眼であり、隠匿の巧拙と発見率の関係を扱っていない。麻薬探知犬の性能評価（Porritt らの研究など）にも当たっていない。

5. 日本語文献について、CiNii Researchの全文検索は語をすべて含む条件で動くため、語の選び方に結果が強く依存した。情報処理学会電子図書館、WISSの各年の予稿集ページ、インタラクションのプログラムページには直接当たれていない。とくにWISSで「隠す」「秘密」を扱ったインタフェース研究がある可能性は残っている。

6. 特許文献をまったく調べていない。日用品に情報を埋め込む、あるいは音で情報を読み出す機構は、学術論文より特許に先に現れている可能性がある。

7. 「security by obscurity」の是非を扱う理論的な文献（Ross Andersonのオープン系と閉鎖系の比較など）を確認できなかった。Crossrefの検索では該当が出ず、原典のURLに到達していない。CipherFluteが物理層の役割を主張する際の理論的な文脈として、追って確認する価値がある。
