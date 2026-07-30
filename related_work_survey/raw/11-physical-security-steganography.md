# 物理的な鍵とトークンの安全性、および物理的な隠蔽

本ファイルは、CipherFlute（WISS 2026投稿予定、栗原一貴）の関連研究調査のうち、「物理的な鍵とトークンの安全性、および物理世界での隠蔽（ステガノグラフィ）」という切り口を担当した結果である。書誌情報は、Crossref（DOI登録機関の一次データ）、CiNii Research、Internet Archive Scholar、arXiv API、著者本人が公開している原稿PDF、Bitcoin改善提案の公式リポジトリのいずれかにWebFetchで直接当たって確認した。確認できなかったものは末尾の「未検証のまま残ったもの」に隔離した。

2026年7月30日に、別の担当者が全67件を独立に再検証した。その結果、巻号やページの欠落を補い、内容の要約の誤りを8か所訂正した。あわせて、初版の時点では5件の確認先が検索結果一覧のURLになっていて当該の書誌そのものを指していなかったので、それぞれのDOIを特定して差し替えた。したがって初版の「書誌情報はすべて一次資料で確認した」という書き方は、正確にはこの再検証を経てはじめて成り立つ。訂正の一覧と、何が確認できなかったかは、末尾の「検証の記録」に書いた。

なお、依頼で指定された書き出し先パスが `undefined/raw/...` となっていたため、既存の同一調査の他の切り口（`01-fab-embed-optical.md` から `05-jp-fabrication-hci.md`）と同じディレクトリである `related_work_survey/raw/` に書き出した。

---

## この切り口の要約

この切り口を洗い直した結果、CipherFluteにとって最も危険なのは「先に同じものを作られていた」という型の先行研究ではなく、「物理層が探索コストを引き上げる」という主張そのものを定量的に切り崩す実証研究の系列であると判明した。中心はロジャー・ジョンストンらの封印（tamper-indicating seal）の脆弱性評価であり、広く使われている120種類の封印すべてが一般人でも入手できる道具で破られ、熟練した1人あたりの平均所要時間は5分未満、攻撃の平均費用は55ドルであったと報告されている。アンドリュー・アペルは同じ論法を投票機の封印に適用し、鍵のピッキングを平均13秒で行い、法廷で全封印を45分以内に痕跡なく外して戻して見せた。つまり物理層の防護は「分」と「数十ドル」の単位で測られる。CipherFluteが物理層に期待できる効果はこの桁を超えないと考えるのが妥当であり、論文はこの数字を引いたうえで自らの主張の大きさを抑えるべきである。以上の数字は、いずれも原典のPDF本文に当たって一字一句の水準で裏を取った。

一方で、偽装が探索コストを上げること自体を裏づける実証もある。ウルフらの「まれな標的は見落とされる」という出現率効果は、探す側が「そこに秘密がある」と期待していない状況では検出率が大きく落ちることを示している。シュヴァニンガーらの空港のX線検査の研究群も同じ方向を向く。逆に、クロフォードとイリベリの隠れ場所選択のゲームの再分析は、隠す側が体系的に予測されうることを示しており、素朴な偽装の限界を示す反証側の証拠になる。さらに強い反証は、ニーとミーナハンが実際の侵入窃盗の受刑者50人に面接し、そのうち45人が予測可能な探索の型を持っていたと報告したことである。隠す側の工夫は、熟練した探す側の定型的な探索の前ではあらかじめ織り込まれている可能性がある。

物理的な鍵の複製については、写真から鍵の刻みを復元するSneakey、深層学習で写真から印刷可能な鍵モデルを作るDeepKey、3Dプリンタで規制されたキーウェイを突破するBurgessらの研究、印影から印章を3Dプリンタで偽造する木村らの日本語研究があり、いずれも「形状が観測できれば複製できる」というCipherFluteの脅威モデルの宣言を強く裏づける。物理暗号の側では、視覚暗号、音響暗号、カードベース暗号、3Dプリンタで作る物理暗号装置（伊藤ら）、手計算可能な誤り訂正付き秘密分散であるcodex32が隣接する。他方、「日用品に偽装した容器（隠し金庫）」や「強要下での否認可能な資産保管」に関する学術研究は事実上存在せず、この空白はCipherFluteの新規性の根拠として使える。

---

## 新規性への脅威が大きい文献

### 1. Tamper-Indicating Seals for Nuclear Disarmament and Hazardous Waste Management

- 著者: Roger G. Johnston
- 掲載: Science & Global Security, Vol. 9, pp. 93–112, 2001年（原稿受理は1999年10月10日）
- 確認先: https://doi.org/10.1080/08929880108426490 （Crossrefの登録書誌）および全文 https://scienceandglobalsecurity.org/archive/sgs09johnston.pdf （PDF本文を取得し、下に挙げる数値をすべて本文の該当箇所で照合した）

内容の要約を述べる。この論文は、ロスアラモス国立研究所の脆弱性評価チーム（Vulnerability Assessment Team）が広く使われている120種類の封印を評価した結果を報告している。低技術のものから高技術のもの、受動型と能動型の双方を含む120種類すべてが、一般に入手可能な低技術の道具と手法で破られた。しかもその破壊は、それぞれの封印に対して通常行われる検査手順では検出されなかった。熟練した1人による所要時間は3秒から2時間に分布し、平均は5分をはるかに下回った。核関連用途に現用されているものに限っても平均所要時間は8分未満であった。攻撃1件あたりの平均費用は55ドルであり、限界費用はそれよりはるかに小さかった。高技術の封印のほうが低技術の封印より簡単に破れる場合もあった。著者は、封印の価格は脆弱性の予測因子として役に立たないこと、封印そのものより「封印の運用手順」のほうが効果を決めることを強調している。また、あらゆる封印は原理的に偽造可能であるという議論も展開している。

一次資料に当たって分かった注意点を書き添える。120種類という数字とそれに伴う所要時間や費用の数値は、この2001年の論文が自ら測ったものとして報告しているが、その出所として同論文の注11が Johnston と Garcia の1997年の脆弱性評価論文を挙げている。したがって数値の一次の出所はその1997年論文であり、2001年論文はそれを要約して再掲した文献である。引用の際にどちらを引くかは、この関係を踏まえて決めるとよい（注11の書誌については末尾の「未検証のまま残ったもの」を参照）。

CipherFluteとの関係を述べる。CipherFluteは「物理層に暗号学的な秘匿の力はまったく無い」と宣言したうえで、物理層の役割を「日用品への偽装による探索コストの引き上げ」に限定している。この論文は、物理層の防護効果が実際にどれくらいの大きさなのかを、専門機関が体系的に測った数少ない一次資料である。5分未満、55ドルという数字は、CipherFluteが物理層に期待してよい上限の目安を与える。

脅威の度合いは「高」である。理由を述べる。CipherFluteが残した唯一の物理層の主張が「探索コストの引き上げ」であるところ、この研究はその種のコストが分単位・数十ドル単位で崩れることを120種類の実測で示しており、主張の大きさを大幅に割り引かせる。さらに、この論文を引かずに「探索コストが上がる」とだけ書くと、物理セキュリティの専門家からは根拠のない楽観と読まれる危険がある。

### 2. Security Seals on Voting Machines: A Case Study

- 著者: Andrew W. Appel
- 掲載: ACM Transactions on Information and System Security (TISSEC), Vol. 14, No. 2, Article 18, 全29ページ, 2011年9月（2010年12月受理、2011年3月改訂、2011年3月採録）
- 確認先: https://doi.org/10.1145/2019599.2019603 （Crossrefの登録書誌）および著者公開版 https://www.cs.princeton.edu/~appel/voting/SealsOnVotingMachines.pdf （PDF本文を取得し、下に挙げる数値をすべて本文の該当箇所で照合した）

内容の要約を述べる。著者はニュージャージー州の投票機に使われた封印の運用を、訴訟の専門家証人として調査した。投票機のキャビネットの錠は安価なウェハータンブラー錠であり、著者はピッキングの経験がまったくない状態から、40ドル未満の工具と1、2時間の練習で開けられるようになり、練習後は平均13秒（2台の投票機で10回試行）で開錠できた。粘着テープ型の封印はヒートガンを80秒当てて軟化させ、40秒かけて剥がすだけで「VOID」や「OPEN」の文字を出さずに外せた（取り外しに合計2分、貼り直しは約2秒）。ケーブル錠型の封印は初回の実機試行で50秒で外れた。州が次々に導入した4世代の封印体制（1990年から2008年までの第1体制、第2体制、2008年12月の第3体制、2009年3月の第4体制）すべてについて、著者は素人でも破れることを示し、法廷では全封印の取り外しと再取り付けを45分未満（そのうち7分は封印が無くても必要なねじとROMの着脱の時間）で実演した。結論として、封印は運用手順がなければ「粘着テープの偽薬」にすぎないと述べている。

CipherFluteとの関係を述べる。CipherFluteが「日用品に偽装すれば探索と読み出しの手間が増える」と述べるとき、その手間はまさにこの論文が測っている種類の量である。また、この論文は封印の運用手順が満たすべき条件を8項目の一覧として明示している。すなわち、（1）攻撃者が容器に近づける時間帯に封印が実際に付いていること、（2）攻撃者が封印を迂回できないこと、（3）同じ封印を痕跡なく外して戻すことが難しいこと、（4）別の封印に取り替えることが難しいこと（通し番号の一意性と、番号の書き換えが痕跡を残す設計によって達成される）、（5）どの番号の封印がどの番号の容器に付いたかの記録を運用し、その記録自体が改ざんから守られていること、（6）定期的に検査して記録と番号を照合すること、（7）検査員を訓練すること、（8）異常が報告されたときに適切な対処が取られること、である。著者はこのうち1つでも欠ければ封印は無断の開封を検出する役に立たないと述べている。CipherFluteの物理層の価値も、この種の運用条件の一覧に落として自己評価すべきである。

脅威の度合いは「高」である。理由を述べる。物理層による保護が、素人が数十分で無効化できる程度のものであることを、査読付きの主要ジャーナルで具体的な秒数とともに示した研究であり、CipherFluteの「探索コストの引き上げ」という定性的な主張をそのまま書くことを許さない。逆に言えば、この論文を引いて「我々の物理層もこの桁の防護しか与えない」と明記すれば、主張は堅くなる。

### 3. Fatal Attraction: Salience, Naïveté, and Sophistication in Experimental "Hide-and-Seek" Games

- 著者: Vincent P. Crawford, Nagore Iriberri
- 掲載: American Economic Review, Vol. 97, No. 5, pp. 1731–1750, 2007年
- 確認先: https://doi.org/10.1257/aer.97.5.1731 （Crossrefの登録書誌）および出版社の論文ページ https://www.aeaweb.org/articles?id=10.1257/aer.97.5.1731 （抄録と公式の引用形式を取得して確認した）

内容の要約を述べる。この論文が扱うのは、一方が相手の選択を当てれば勝ち、他方が外させれば勝つというゼロ和2人ゲーム（隠す側と探す側の対戦）である。ここで重要な訂正を書く。この論文は著者ら自身が新しい実験を行ったものではなく、ルビンシュタインやトヴェルスキーらが行った既存の実験の結果を、非中立な「風景」の上で改めて再分析したものである。理論上の均衡はそうした風景の効果を無視するにもかかわらず、被験者は風景に応じて均衡から体系的にずれる。著者らは、複数の説明を理論的かつ計量的に比べたうえで、そのずれがレベルk思考にもとづく非均衡モデルでよく説明できると結論している。目立つ（顕著性の高い）選択肢が引き起こす体系的なずれを、著者らは「致命的な魅力」と呼んでいる。

CipherFluteとの関係を述べる。CipherFluteの利用者は、どの日用品に笛を仕込むかを自分で選ぶ。この論文は、人間が隠し場所を選ぶときに体系的な偏りを持ち、その偏りが敵に読まれることを実験で示している。したがって「日用品に偽装すれば探索コストが上がる」という主張は、隠し場所の選び方が敵に予測されない限りにおいてのみ成り立つ。

脅威の度合いは「中」である。理由を述べる。CipherFluteの主張を直接否定するわけではないが、その主張の成立条件（隠し場所の選択の予測不能性）を明示的に突きつける研究であり、引用して差分と限界を述べる必要がある。とくにCipherFluteが「探索コストの引き上げ」を売りにする以上、隠す側の偏りに触れないのは片手落ちである。ただし引用時には、これが既存実験の再分析であって新規の隠し場所実験ではないことを取り違えないよう注意が必要である。

### 4. Rare items often missed in visual searches ／ Low target prevalence is a stubborn source of errors in visual search tasks

- 著者: Jeremy M. Wolfe, Todd S. Horowitz, Naomi M. Kenner（2005年）／ Jeremy M. Wolfe, Todd S. Horowitz, Michael J. Van Wert, Naomi M. Kenner, Skyler S. Place, Nour Kibbi（2007年）
- 掲載: Nature, Vol. 435, No. 7041, pp. 439–440, 2005年5月 ／ Journal of Experimental Psychology: General, Vol. 136, No. 4, pp. 623–638, 2007年
- 確認先: https://doi.org/10.1038/435439a および https://doi.org/10.1037/0096-3445.136.4.623 （いずれもCrossrefの登録書誌）。2005年論文の本文は著者最終稿 https://pmc.ncbi.nlm.nih.gov/articles/PMC4224304/ を取得して数値を照合し、2007年論文の抄録はPubMed（PMID 17999575）で確認した。なおPubMedの書誌では2005年論文の題名に「Cognitive psychology:」という節名の接頭辞が付いており、引用形式によって題名の見え方が異なる点に注意が必要である。

内容の要約を述べる。2005年のNature論文は、探索課題で標的の出現率が低いほど見落としが劇的に増えることを示した。本文の数値は、出現率50パーセントで見落とし7パーセント、10パーセントで16パーセント、1パーセントで30パーセントである。誤警報（標的が無いのに「ある」と答えること）は0.03パーセントときわめてまれであり、出現率を変えるだけで誤り率が4倍になった。2007年の論文はこの効果が信号検出理論でいう判断基準の移動として説明でき、観察者によい基準を採らせようとする複数の試みが失敗する頑健なものであることを確かめている。ただし同論文は、高い出現率と完全なフィードバックによる短い再訓練期間をはさむやり方であれば、フィードバックのない低出現率の期間でもよい基準を保てることを見いだしており、「どんな介入も効かない」わけではない。空港の手荷物X線検査のように、探すべきものがめったに存在しない現場でこの効果が問題になることが繰り返し指摘されている。

CipherFluteとの関係を述べる。CipherFluteの「日用品に偽装する」という戦略が効く理由の最も科学的な裏づけがこれである。敵が「この本立てには秘密が入っているかもしれない」と考えていない限り、目の前にあっても見落とされる確率が高い。逆に、敵が特定の対象を疑って集中的に調べる状況では出現率効果は働かず、偽装の効果は急速に失われる。

脅威の度合いは「中」である。理由を述べる。新規性を脅かすというより、CipherFluteの主張を支える最良の外部証拠であり、引用しないと「探索コストが上がる」という主張が単なる直感に見えてしまう。同時に、出現率効果が成り立つ条件（敵が疑っていないこと）を明示することで、脅威モデルの記述が精密になる。

### 5. Replication Prohibited: Attacking Restricted Keyways with 3D-Printing

- 著者: Ben Burgess, Eric Wustrow, J. Alex Halderman（3名ともミシガン大学）
- 掲載: 9th USENIX Workshop on Offensive Technologies (WOOT '15), ワシントンD.C., 2015年
- 確認先: https://www.usenix.org/conference/woot15/workshop-program/presentation/burgess （USENIXの予稿集ページ。題名、著者、所属、抄録、公式のBibTeX項目を取得して確認した）。全文PDFは https://www.usenix.org/system/files/conference/woot15/woot15-paper-burgess.pdf にある。

内容の要約を述べる。この研究は、「複製禁止（Do Not Duplicate）」や特許で守られた制限付きキーウェイの錠前が、消費者向けの3Dプリンタによって実質的に無力化されることを示した。ここで原典の記述に沿って正確に書き直す。著者らが示したのは、市販の3Dプリンタで鍵素材（キーブランク）や切削済みの鍵を、よく使われるいくつかのピンタンブラー錠で機能するだけの解像度で出力できること、そしてその材料がバンピング、型どり、権限増幅、遠隔複製といった攻撃の負荷に耐える強度を持つことである。さらに著者らは、錠のキーウェイを写した1枚の写真だけから3Dプリント可能なキーブランクのCADモデルを自動生成する道具を作り、攻撃に必要な技能の低さを実証した。物理的な鍵の安全性が「鍵素材の入手困難性」という供給側の制約に依存していたところ、その制約が積層造形によって消えたことを示す点に主眼がある。

CipherFluteとの関係を述べる。CipherFluteは3Dプリントされた形状そのものが秘密の担体であり、論文は「形状を計測されれば無音で読める、複製も容易」と宣言している。この研究は、その宣言が抽象的な可能性ではなく、CipherFluteとまったく同じ技術（家庭用3Dプリンタ）で既に実証された事実であることを裏づける。同時に、物理鍵の分野で「複製困難性に頼る設計」が崩れた歴史をそのまま引用できる。

脅威の度合いは「中」である。理由を述べる。CipherFluteの主張を崩すのではなく、その脅威モデルの正しさを外部から支持する。ただし、CipherFluteが物理層の複製困難性に少しでも寄りかかった書き方をしている箇所があれば、この研究の存在によってその記述は成立しなくなるため、必ず引用して線を引く必要がある。

### 6. 3Dプリンタによる印影からの印章の偽造

- 著者: 木村悠生, 山元陽佑雅, 榎竜盛, 上原哲太郎
- 掲載: マルチメディア，分散，協調とモバイルシンポジウム2023論文集（DICOMO2023）, Vol. 2023, pp. 1269–1276, 2023年6月28日, 情報処理学会
- 確認先: https://cir.nii.ac.jp/crid/1050860532220398464 （CiNii Researchの書誌。著者4名、題名、掲載誌名、巻、ページ、発行日、抄録を照合した）および情報処理学会電子図書館 https://ipsj.ixsq.nii.ac.jp/records/228209

内容の要約を述べる。この研究は、押された印影の画像から、消費者が入手できる安価な3Dプリンタを用いて印章（はんこ）を偽造できることを示した。偽造した印章で照合実験を行い、姓の種類や文字数といった要因が判別精度にどう影響するかを評価している。さらに、偽造の容易さと、偽造を困難にしうる要素の双方を検討している。

CipherFluteとの関係を述べる。日本社会で長く物理的な認証トークンとして機能してきた印章が、その出力（印影）を観測するだけで3Dプリンタで再現されるという構図は、CipherFluteの笛が「音を聞かれれば、あるいは形を測られれば再現される」という構図と同型である。日本語圏の読者に脅威モデルを説明するうえで、これ以上に通りのよい先行事例はない。

脅威の度合いは「中」である。理由を述べる。CipherFluteの新規性を直接脅かしはしないが、「観測可能な物理トークンは3Dプリンタで複製される」という論点の国内の一次事例であり、脅威モデルの節で引用すべきである。引用しないと、日本の査読者から「印章偽造の議論を知らないのか」と問われる可能性がある。

### 7. Audio and Optical Cryptography ／ Nonbinary Audio Cryptography ／ 物理的復元が容易な音響秘密分散法

- 著者: Yvo Desmedt, Shuang Hou, Jean-Jacques Quisquater（1998年）／ Yvo Desmedt, Tri V. Le, Jean-Jacques Quisquater（2000年）／ 徳重佑樹, 三澤裕人, 吉田文晶（2015年）
- 掲載: Advances in Cryptology — ASIACRYPT'98（LNCS）, pp. 392–404, 1998年 ／ Information Hiding: Third International Workshop, IH'99, ドイツ・ドレスデン, 1999年9月29日から10月1日（LNCS 1768）, pp. 478–489, 2000年刊 ／ 電子情報通信学会技術研究報告, Vol. 115, No. 38, pp. 75–80, 2015年5月（英語題名は An Audio Secret Sharing Scheme Easy to Reproduce Secret Physically）
- 確認先: https://doi.org/10.1007/3-540-49649-1_31 、 https://doi.org/10.1007/10719724_33 （いずれもCrossrefの登録書誌）、抄録は出版社ページ https://link.springer.com/chapter/10.1007/3-540-49649-1_31 、収録書の正式名称は https://link.springer.com/book/10.1007/10719724 で確認した。日本語の報告は https://cir.nii.ac.jp/crid/1520572358843442048 （CiNii Researchの書誌。著者3名、題名、巻号、ページ、発行年月、キーワードを照合した）

ここで会議名の訂正を書く。2000年の論文が載ったのは「Information Hiding 2000」という会議ではなく、1999年9月29日から10月1日にドレスデンで開かれた第3回Information Hidingワークショップ（IH'99）であり、その予稿集がLNCS第1768巻として2000年に刊行された。会議年と刊行年が1年ずれるため、引用の際は取り違えないほうがよい。

内容の要約を述べる。Desmedtらの音響暗号は、視覚暗号（透明シートを重ねると秘密の像が現れる方式）の音響版であり、2つの音響シェアをステレオ装置で同時に再生すると、音の干渉、あるいは人間の聴覚の左右の知覚によって秘密が復元されるという仕組みである。計算機なしに人間の感覚器だけで復号できる点が要点である。同じ論文は光を使う方式も扱い、そちらの復号装置にはマッハ・ツェンダー干渉計を使う。2000年の論文は二値に限らない拡張を扱う。徳重らの日本語の報告は、波の干渉と周波数分割を用いて「物理的な復元が容易な」音響秘密分散法を提案しており、キーワードとして音響秘密分散法、秘密分散法、波の干渉、周波数分割が挙げられている。

抄録に当たって分かった重要な点を書き添える。Desmedtらは、視覚暗号ではシェアがランダムな模様になるため検閲者に怪しまれるという弱点を明示し、自分たちの方式ではシェアが音楽や画像であって「人間の検閲者に怪しまれない」ことを利点として挙げている。つまり秘密分散と「怪しまれない偽装」の組み合わせは、この1998年の論文がすでに設計目標として掲げていた。

CipherFluteとの関係を述べる。CipherFluteは音の高さを符号の語彙にし、秘密分散に秘匿を負わせ、「2枚そろって初めてハートが現れるカード」という実装を持つ。音響領域での秘密分散と、物理的に重ねると秘密が現れるという発想は、この系列が1998年から扱ってきたものである。しかも上に書いたとおり、「シェアを怪しまれない見た目や音にする」という偽装の動機まで共有している。CipherFluteの新規性は、音を秘密分散の復元手段に使うことでも、シェアを怪しまれない形にすることでもなく、電源も電子部品も持たない造形物が、吹かれたときの音の高さで少量の情報を運ぶことにあると、明確に切り分ける必要がある。

脅威の度合いは「中」である。理由を述べる。CipherFluteが「音で秘密を運ぶ」あるいは「2つそろって初めて意味を持つ物理媒体」あるいは「怪しまれない担体に秘密を載せる」という点に新規性を置くと、この系列と正面から衝突する。逆に、符号化された情報を受動的な造形物が発音するという点に限定すれば衝突しない。したがって必ず引用して差分を述べる必要がある。

### 8. Visual Cryptography

- 著者: Moni Naor, Adi Shamir
- 掲載: Advances in Cryptology — EUROCRYPT'94（LNCS）, pp. 1–12, 1995年
- 確認先: https://doi.org/10.1007/bfb0053419 （Crossrefの登録書誌。収録書名が Advances in Cryptology — EUROCRYPT'94 であること、ページが1から12であることを確認した。なお登録上の題名は小文字で Visual cryptography と記録されている）

内容の要約を述べる。秘密の画像を複数枚の透明シートに分割し、規定枚数を重ね合わせたときにだけ人間の目に像が現れる方式である。計算機を使わずに人間の視覚系が復号を行い、規定枚数未満のシートからは情報理論的にまったく情報が漏れない。以後の「物理的な暗号プリミティブ」研究の出発点となった。

CipherFluteとの関係を述べる。CipherFluteの実装のひとつである「2枚そろって初めてハートが現れるカード」は、視覚暗号の閾値2の構成そのものの見た目を持つ。CipherFluteのカードが実際に行っているのはShamirの秘密分散の物理的な担体であって視覚暗号ではないが、読者が混同する可能性が高い。

脅威の度合いは「中」である。理由を述べる。デモの見た目が視覚暗号と重なるため、引用して「見た目は似ているが、秘匿は視覚的な重ね合わせではなく秘密分散に負わせている」と明示しないと、既知手法の焼き直しと誤読される危険がある。

### 9. 3Dプリンタによるオープン装置や特殊カードケースの作成と対称関数の秘密計算への適用

- 著者: 伊藤優樹, 四方隼人, 水木敬明, 菅沼拓夫
- 掲載: コンピュータセキュリティシンポジウム2023論文集, pp. 192–199, 2023年10月23日（英語題名は Creation of Card-Open Device and Special Card Cases Using 3D Printer and an Application to Secure Computations of Symmetric Functions）
- 確認先: https://cir.nii.ac.jp/crid/1050579444484578048 （CiNii Researchの書誌。著者4名、和文と英文の題名、掲載誌名、ページ、発行日、日英の抄録を照合した）および情報処理学会電子図書館 https://ipsj.ixsq.nii.ac.jp/records/228640

内容の要約を述べる。この研究は、カードベース暗号プロトコルを実行するための物理装置を3Dプリンタで作製したものである。抄録によれば、著者らは2023年7月の情報処理学会コンピュータセキュリティ研究会で先に装置とカードケースの作製を報告しており、本稿はその続報である。具体的には、通常の2色カードで動くFive-card Trickの最終段で5枚のカードを同時にめくれる「オープン装置」を作ったことを報告し、あわせて先の報告で紙面の都合により省いたカードケースの機能を説明して、そのカードケースによってコミットメントの加算が効率よく実現でき、対称関数の秘密計算に有用であることを示している。カードベース暗号の物理実装という日本発の系列に、積層造形を持ち込んだ位置づけになる。

CipherFluteとの関係を述べる。「家庭用3Dプリンタで作った受動的な物体が暗号的な役割を担う」という一点で、CipherFluteと最も近い日本語圏の研究である。ただし、この研究の物体は秘密を保持する媒体ではなく、プロトコルを人が実行するための治具である。

脅威の度合いは「中」である。理由を述べる。国内の査読者が真っ先に思い浮かべる隣接研究であり、引用して「向こうは物理暗号プロトコルの実行装置、こちらは秘密を運ぶ受動的な記憶媒体」と差分を述べる必要がある。

### 10. BIP-93 codex32: Checksummed SSSS-aware BIP32 seeds

- 著者: Leon Olsson Curr, Pearlwort Sneed, Andrew Poelstra
- 掲載: Bitcoin Improvement Proposal 93（公式リポジトリで公開）。文書中の欄では、種別は Informational、状態は Draft、作成日は2023年2月13日と記載されている。
- 確認先: https://github.com/bitcoin/bips/blob/master/bip-0093.mediawiki （公式リポジトリの本文。番号、題名、著者欄、種別と状態と作成日、下に挙げる符号の性能と手計算に関する記述を照合した）

内容の要約を述べる。codex32は、BIP-32のマスターシードを、誤り訂正符号付きのbase32文字列として保管するための規格である。標準のチェックサムは、8文字までに影響する誤りをどのようなものであれ必ず検出することを保証し、4文字までの置換誤り、または8文字までの消失（位置の分かっている欠落）を訂正できる。長い文字列に対しては、同じ検出能力のもとで15文字までの連続した消失を訂正できる。Shamirの秘密分散に対応し、最大31個のシェアに分割できて、閾値は1桁の数字で2から9までを取る。最大の特徴は、すべての計算が参照表だけで実行できるように設計されていることであり、規格自体が「チェックサムの計算と検証、シードの分割と復元を、ペンと紙だけで完全に行える」と述べている。この性質は、小さな体を選んだことと線形の誤り訂正符号を使ったことから来ると規格は説明している。

CipherFluteとの関係を述べる。CipherFluteは、リカバリーシードを対象に、Reed–Solomon符号による誤り訂正と秘密分散を組み合わせている。codex32は同じ目的（種の物理バックアップ）に対して、誤り訂正符号と秘密分散を組み合わせ、しかも電子機器を使わない手計算での復元まで担保している。現在の論文はSLIP-39とSSKRを引いているが、codex32を引いていない。

脅威の度合いは「中」である。理由を述べる。CipherFluteの符号設計（誤り訂正付きの、人が扱える種の保管形式）と目的が完全に重なるため、引用しないのは調査不足に見える。差分は明確であり、codex32は文字列という「読めば分かる」担体を使うのに対し、CipherFluteは日用品に溶け込む物理形状を担体にする。この対比はむしろCipherFluteの位置づけを鮮明にする。

### 11. Chameleon Devices: Investigating More Secure and Discreet Mobile Interactions via Active Camouflaging

- 著者: Jennifer Pearson, Simon Robinson, Matt Jones, Anirudha Joshi, Shashank Ahire, Deepak Sahoo, Sriram Subramanian
- 掲載: Proceedings of the 2017 CHI Conference on Human Factors in Computing Systems, pp. 5184–5196, 2017年
- 確認先: https://doi.org/10.1145/3025453.3025482 （Crossrefの登録書誌。著者7名とページを確認した）。副題を含む完全な題名はSemantic Scholarの書誌 https://api.semanticscholar.org/graph/v1/paper/DOI:10.1145/3025453.3025482 で確認した。本文PDFは著者所属機関の公開版 https://hdl.handle.net/10779/uos.23443868.v1 （figshare上のサセックス大学の登録。書誌はfigshare API、本文はPDFを取得して直接読んだ）

ここで題名の補足を述べる。Crossrefの登録は副題が落ちて「Chameleon Devices」だけになっているが、本文PDFの正式な題名は「Chameleon Devices: Investigating More Secure and Discreet Mobile Interactions via Active Camouflaging」である。

内容の要約を述べる。この研究は、モバイル機器が周囲に溶け込むように外見を変える「カメレオン・デバイス」の概念を提案し、強盗の標的になることや、周囲に対して無礼あるいは不注意と見られることを避けながら、目立たずに操作するという用途を検討した。ここで調査地の訂正を書く。本文によれば、ワークショップに招いたのはバンガロール（インド）の新興利用者54名、ケープタウン（南アフリカ）のランガという地区の8名、ナイロビ（ケニア）周辺の9名である。ムンバイは調査地ではなく、共著者2名の所属であるインド工科大学ボンベイ校の所在地である。参加者は将来の機器やサービスの案をスケッチなどで作る課題に取り組み、たとえばある女性はヘアブラシに携帯電話を隠す案を出して、髪をとかしながら夫の通話を聞き、ブラシに向かって話せると説明したという。

CipherFluteとの関係を述べる。「価値のある物を日用品に偽装することで、敵の注意と探索の対象から外す」という発想を、ヒューマンコンピュータインタラクションの主要会議で扱った数少ない研究である。とくに上に挙げたヘアブラシの案は、CipherFluteが日用品に笛を仕込むという発想とほとんど同じ形をしている。CipherFluteの偽装戦略の直系の先行研究として位置づけられる。

脅威の度合いは「中」である。理由を述べる。CipherFluteの「日用品への偽装」という主張が、HCI分野で既に提案され現地調査まで行われていることを示す。ただし対象は電源を持つ携帯機器であり、秘密情報の担体としての符号設計は扱っていないため、差分は明確に述べられる。

### 12. Safecracking for the computer scientist

- 著者: Matt Blaze（ペンシルベニア大学 計算機情報科学科）
- 掲載: 査読誌や会議の予稿集ではなく、著者が自ら公開している草稿である。表紙に「DRAFT - 7 December 2004 (Revised 21 December 2004) - DRAFT」と印字されている。
- 確認先: https://www.mattblaze.org/papers/safelocks.pdf （PDF本文を取得し、題名、著者、所属、草稿と改訂の日付、下に挙げる内容をすべて本文で照合した）。本文には正典の場所として http://www.crypto.com/papers/safelocks.pdf が記されている。

ここで掲載形態の訂正を書く。この文献をペンシルベニア大学の技術報告として扱うことはできない。表紙には技術報告番号や叢書名が一切なく、あるのは著者名、所属、草稿の日付と改訂日だけである。引用する場合は、査読を経ていない著者公開の草稿として扱うのが正確である。

内容の要約を述べる。金庫と金庫錠の安全性を計算機科学の視点から概観した文献である。物理セキュリティの世界では、安全性が「破るのにどれだけ時間がかかるか、どんな道具が必要か、どんな痕跡が残るか」という多次元の量として定義されており、Underwriters Laboratoriesの最上位の格付け区分でさえ15分、30分、60分という時間しかなく、アメリカ連邦政府調達庁の力ずくの攻撃に対する格付けは0分または10分であることを指摘している。攻撃は、痕跡をまったく残さない「surreptitious」、通常の使用では気づかれない（専門家の検査でなら気づかれうる）痕跡を残す「covert」、痕跡が明白な「forced」に分類される。また、金庫業界では「security-by-obscurity」が依然として中心的な信条であり続けていることを、情報セキュリティの立場から批判的に検討している。あわせて、情報システムの側にはこれに相当する時間で測る安全性の尺度が一般には存在しないことを指摘している。

CipherFluteとの関係を述べる。CipherFluteが「探索コストの引き上げ」を主張するなら、その主張は本来この語彙（所要時間、必要な道具、残る痕跡の3軸）で書かれるべきである。また「security-by-obscurity」を物理世界がどう扱ってきたかという議論の枠組みを、そのまま借りられる。

脅威の度合いは「中」である。理由を述べる。新規性を脅かすものではないが、CipherFluteの脅威モデルの節を専門的な水準に引き上げるために引用が必要であり、これを欠くと物理セキュリティの語彙を知らずに議論していると見なされる。

### 13. Obfuscation: A User's Guide for Privacy and Protest

- 著者: Finn Brunton, Helen Nissenbaum
- 掲載: The MIT Press, 2015年9月
- 確認先: https://doi.org/10.7551/mitpress/9780262029735.001.0001 （Crossrefの登録書誌。書籍として登録されており著者2名を確認した）。章ごとのDOIも確認した。例として「Will Obfuscation Work?」は https://doi.org/10.7551/mitpress/9780262029735.003.0006 で、同書の84ページから96ページに当たる。

内容の要約を述べる。この書籍は、強い敵に対して秘匿を達成できないとき、ノイズや偽装によって敵のコストを引き上げるという「難読化（obfuscation）」の戦略を体系化したものである。「難読化はうまくいくのか」「難読化は正当化されるのか」という章を設け、弱者が非対称な力関係のもとで取りうる手段としての難読化を、倫理と有効性の両面から検討している。

CipherFluteとの関係を述べる。CipherFluteの物理層の位置づけ、すなわち「秘匿はできないが探索コストを上げる」という主張は、まさに難読化の枠組みそのものである。理論的な後ろ盾としてこの書籍を引くことで、主張の位置づけが明確になる。

脅威の度合いは「中」である。理由を述べる。CipherFluteの中核的な言い分に既存の理論的枠組みが存在することを示すため、引用して自らの位置づけを述べる必要がある。引用しないと「探索コストの引き上げ」という概念を独自に発明したかのように読まれる。

### 14. Expert Decision Making in Burglars ／ Learning on the job: Studying expertise in residential burglars using virtual environments

- 著者: Claire Nee, Amy Meenaghan（2006年）／ Claire Nee, Jean-Louis van Gelder, Marco Otte, Zarah Vernham, Amy Meenaghan（2019年）。2019年論文の完全な題名は「Learning on the job: Studying expertise in residential burglars using virtual environments」であり、短く「Learning on the job」とだけ書くと副題が落ちる。
- 掲載: The British Journal of Criminology, Vol. 46, No. 5, pp. 935–949, 2006年9月1日 ／ Criminology, Vol. 57, No. 3, pp. 481–511, 2019年8月
- 確認先: https://doi.org/10.1093/bjc/azl013 および https://doi.org/10.1111/1745-9125.12210 （いずれもCrossrefの登録書誌）。2006年論文の抄録はCrossrefに登録がないため、ポーツマス大学の研究業績データベース https://researchportal.port.ac.uk/en/publications/expert-decision-making-in-burglars で抄録と巻号ページを取得して確認した。2019年論文の抄録はCrossrefに登録された抄録で確認した。

内容の要約を述べる。2006年の研究は、まず住居侵入窃盗犯が標的を選ぶときの認知処理に関する既存研究を整理し、それを認知科学一般の「熟練」の概念と結びつけている。すなわち初心者と比べて、処理が明示的な熟慮から離れ、作業が速く手順どおりに進み、手がかりの認識がきわめて速く、ほとんど瞬間的であるという性質である。そのうえで、経験を積んだ窃盗犯50名への面接から得た新しいデータを提示し、家に侵入してからの探索の進め方を英国で初めて詳しく論じた。50名のうち45名が予測可能な探索の型を持っており、37名は自分の探索を自動性を示す言葉で自発的に説明したという。2019年の研究は、収監中の経験を積んだ窃盗犯56名、他の罪種の受刑者50名、非犯罪者55名に、仮想の住宅地の中で模擬的な侵入窃盗を行わせた準実験である。窃盗犯は他の集団より住宅地を入念に下見し、犯行現場の価値の高い区域により長くとどまりながらそこでの移動距離は短く、狙う物品も異なっていた。いずれも、探す側が何を手がかりにどこを見るかを実証的に扱っている。

CipherFluteとの関係を述べる。CipherFluteの「日用品に偽装すれば探索コストが上がる」という主張の相手方は、多くの場合この種の熟練した探索者である。熟練者の探索が高度に自動化され効率的であるという知見は、素朴な偽装の効果を割り引く方向に働く。とくに「50名中45名が予測可能な探索の型を持つ」という数字は、偽装の効き方が探す側の定型的な手順との関係で決まることを示しており、CipherFluteが「どこに隠すか」を利用者任せにする設計の弱点をそのまま突く。

脅威の度合いは「中」である。理由を述べる。CipherFluteの主張を直接否定するわけではないが、探索側の能力を実証的に測った数少ない研究であり、「敵は素人ではない」という前提を論文に持ち込むために引用が必要である。

### 15. Physical One-Way Functions

- 著者: Ravikanth Pappu, Ben Recht, Jason Taylor, Neil Gershenfeld
- 掲載: Science, Vol. 297, No. 5589, pp. 2026–2030, 2002年9月20日
- 確認先: https://doi.org/10.1126/science.1074376 （Crossrefの登録書誌。著者4名、巻号、ページ、発行日を確認した）

内容の要約を述べる。微細な構造の乱雑さに由来する、製造者ですら再現できない物理的な一方向性関数（後に物理的複製不能関数、PUFと呼ばれる）を提案した論文である。透明媒体に散乱体をランダムに封じ込め、レーザー照射に対する散乱パターンを応答として使う。物理的な複製が困難であることを安全性の根拠にする設計の出発点である。

CipherFluteとの関係を述べる。CipherFluteはこの設計思想の正反対の位置にある。CipherFluteの笛は決定論的に設計され、形状が分かれば誰でも同じものを刷れる。この対比を明示すると、CipherFluteが何に依拠し何に依拠していないかがはっきりする。

脅威の度合いは「中」である。理由を述べる。「物理的な物体に秘密を持たせる」研究として最も有名な系列であり、引用せずに議論すると、査読者から「なぜ複製不能性を狙わないのか」と当然に問われる。引用して「複製不能性は狙わず、秘匿は秘密分散に負わせる」と明言することで、その問いを先回りできる。

---

## 背景として押さえるべき文献

以下は脅威の度合いが「低」であり、背景として引用する程度でよいものである。すべて一次資料で実在を確認した。2026年7月30日の再検証で、巻号とページを補い、検索結果一覧のURLで代用していた確認先を書誌そのものを指すDOIに差し替えた。

### 物理鍵と錠前の複製

- Benjamin Laxton, Kai Wang, Stefan Savage, "Reconsidering Physical Key Secrecy: Teleduplication via Optical Decoding", ACM CCS 2008, pp. 469–478. https://doi.org/10.1145/1455770.1455830 。写真から鍵の刻み（bitting code）を遠隔で復元して精密な複製を作る攻撃であり、著者らの試作系の名前がSneakeyである。原稿PDF（https://cseweb.ucsd.edu/~savage/papers/CCS08OptDecode.pdf ）を取得して本文を確認したところ、システム名がSneakeyであること、そして復元した刻みから作った複製鍵で対応する錠を実際に開けたことが本文に書かれていた。CipherFluteの「観測されれば複製される」という宣言の古典的な出発点にあたる。
- Rory Smith, Tilo Burghardt, "DeepKey: Towards End-to-End Physical Key Replication From a Single Photograph", arXiv:1811.01405, 2018年11月4日. https://arxiv.org/abs/1811.01405 （arXiv APIで題名、著者2名、投稿日、抄録を確認した）。1枚の写真から深層学習で3Dプリント可能な鍵モデルを自動生成する。抄録には実在の錠を開けた例を示すと書かれている。
- Soundarya Ramesh, Harini Ramprasad, Jun Han, "Listen to Your Key: Towards Acoustics-based Physical Key Inference", 第21回 ACM International Workshop on Mobile Computing Systems and Applications（HotMobile 2020）, pp. 3–8. https://doi.org/10.1145/3376897.3377853 。鍵を挿入するときの音から刻みを推定する攻撃である。
- Soundarya Ramesh, Rui Xiao, Anindya Maiti, Jong Taek Lee, Harini Ramprasad, Ananda Kumar, Murtuza Jadliwala, Jun Han, "Acoustics to the Rescue: Physical Key Inference Attack Revisited", USENIX Security Symposium 2021. https://www.usenix.org/conference/usenixsecurity21/presentation/ramesh （USENIXの予稿集ページで題名、著者8名と所属、抄録を確認した）。上記の実用性を高めたKeynergyという手法であり、鍵の挿入時の可聴のカチッという音と、鍵を持つ被害者を写した映像を組み合わせて刻みを推定する。音を情報の担体として扱う点でCipherFluteと表裏の関係にある。
- Soundarya Ramesh ほか, "Listen to your key: Towards acoustics-based physical key inference", The Journal of the Acoustical Society of America, Vol. 155, No. 3_Supplement, p. A69, 2024年3月1日. https://doi.org/10.1121/10.0026832 。ここで訂正を書く。これは論文誌の本論文（ジャーナル版）ではなく、米国音響学会の大会の講演要旨であり、補遺号に載った1ページの抄録である。上記の系列を論文誌に投稿し直したものとして引用してはならない。
- Matt Blaze, "Rights amplification in master-keyed mechanical locks", IEEE Security & Privacy, Vol. 1, No. 2, pp. 24–32, 2003年. https://doi.org/10.1109/msecp.2003.1193208 。1本の子鍵からマスターキーを合成できることを示した研究であり、物理鍵の安全性を計算機科学の語彙で論じた初期の代表例である。
- Deviant Ollam, "Master-Keyed Systems", Keys to the Kingdom（書籍の章）, pp. 121–152, 2012年, Elsevier. https://doi.org/10.1016/b978-1-59749-983-5.00003-8 。実務側からの解説である。

### 封印と改ざん検知

- Roger G. Johnston, "Effective Vulnerability Assessment of Tamper-Indicating Seals", Journal of Testing and Evaluation, Vol. 25, No. 4, pp. 451–455, 1997年7月1日, ASTM International. https://doi.org/10.1520/jte11883j 。封印の脆弱性評価の方法論である。
- Roger Johnston, "Tamper-Indicating Seals", American Scientist, Vol. 94, No. 6, p. 515, 2006年, Sigma Xi. https://doi.org/10.1511/2006.62.515 。一般向けの総説である。
- Roger G. Johnston, Michael J. Timmons, Jon S. Warner, "Protecting Nuclear Safeguards Monitoring Data from Tampering", Science & Global Security, Vol. 15, No. 3, pp. 185–209, 2007年. https://doi.org/10.1080/08929880701715076 （再検証でDOIを特定し、著者3名、巻号、ページを確認した。以前はCrossrefやInternet Archive Scholarの検索結果一覧のURLで代用していた）。

### 物体の同定と偽造対策

- William Clarkson, Tim Weyrich, Adam Finkelstein, Nadia Heninger, J. Alex Halderman, Edward W. Felten, "Fingerprinting Blank Paper Using Commodity Scanners", IEEE Symposium on Security and Privacy 2009, pp. 301–314. https://doi.org/10.1109/sp.2009.7 。白紙の繊維の乱雑さを市販スキャナで指紋化する研究である。
- Zhengxiong Li, Aditya Singh Rathore, Chen Song, Sheng Wei, Yanzhi Wang, Wenyao Xu, "PrinTracker", ACM CCS 2018, pp. 1306–1323. https://doi.org/10.1145/3243734.3243735 。3Dプリント物からプリンタ個体を同定する研究である。Crossrefの登録では題名が「PrinTracker」だけになっており副題が落ちているため、副題まで書く場合は出版社ページで確かめる必要がある。
- Antonella Sola, Yilin Sai, Adrian Trinchi, Clement Chu, Shirley Shen, Shiping Chen, "How Can We Provide Additively Manufactured Parts with a Fingerprint? A Review of Tagging Strategies in Additive Manufacturing", Materials, Vol. 15, No. 1, 記事番号85, 公開日2021年12月23日. https://doi.org/10.3390/ma15010085 （再検証でDOIを特定し、Crossref、EuropePMC、OpenAlexの3つで著者6名、巻号、記事番号、公開日が一致することを確認した。以前は検索結果一覧のURLで代用していた）。積層造形物への標識付けの総説である。なお発行元のページに到達できなかったため、発行元の慣習にしたがう巻年の表記が2022年になる可能性がある。投稿時には出版社ページで年の表記を確かめたほうがよい。
- Muhammad Usama, Ulas Yaman, "Embedding Information into or onto Additively Manufactured Parts: A Review of QR Codes, Steganography and Watermarking Methods", Materials, Vol. 15, No. 7, 記事番号2596, 2022年4月1日. https://doi.org/10.3390/ma15072596 。積層造形物への情報埋め込みの総説であり、光学コード、ステガノグラフィ、透かしを整理している。音響による読み出しは扱われていない。
- Timo Richter, Stephan Escher, Dagmar Schönfeld, Thorsten Strufe, "Forensic Analysis and Anonymisation of Printed Documents", 第6回 ACM Workshop on Information Hiding and Multimedia Security 2018, pp. 127–138. https://doi.org/10.1145/3206004.3206019 。カラープリンタが印刷物に埋め込む追跡ドットの解析と除去である。実社会に大規模展開された物理的ステガノグラフィの数少ない例である。

### 存在を隠す技術（ステガノグラフィと否認可能性）

- Ross Anderson, Roger Needham, Adi Shamir, "The Steganographic File System", Information Hiding 1998（LNCS）, pp. 73–82. https://doi.org/10.1007/3-540-49380-8_6 。
- Christian Cachin, "An Information-Theoretic Model for Steganography", Information Hiding 1998（LNCS）, pp. 306–318. https://doi.org/10.1007/3-540-49380-8_21 、および論文誌版 Information and Computation, Vol. 192, No. 1, pp. 41–56, 2004年7月. https://doi.org/10.1016/j.ic.2004.02.003 。「存在を隠す」ことの安全性を情報理論的に定義した基礎文献である。CipherFluteが「物理層に暗号学的な秘匿の力は無い」と述べるとき、その「秘匿」の定義としてこれを引ける。
- Ran Canetti, Cynthia Dwork, Moni Naor, Rafail Ostrovsky, "Deniable Encryption", CRYPTO'97（LNCS）, pp. 90–104. https://doi.org/10.1007/bfb0052229 。なおCrossrefの登録では第1著者の名が「Rein Canetti」と誤記されている。正しくはRan Canettiであり、登録の誤記に引きずられないよう注意が必要である。
- Adam Skillen, Mohammad Mannan, "Mobiflage: Deniable Storage Encryption for Mobile Devices", IEEE Transactions on Dependable and Secure Computing, Vol. 11, No. 3, pp. 224–237, 2014年5月. https://doi.org/10.1109/tdsc.2013.56 。Crossrefの登録には著者名が入っていないため、著者はコンコルディア大学の機関リポジトリで確認した。同リポジトリには同じ2名による会議版 "On Implementing Deniable Storage Encryption for Mobile Devices"（20th Annual Network & Distributed System Security Symposium, 2013年2月）が登録されている（https://spectrum.library.concordia.ca/ でMobiflageを検索して書誌を取得した）。
- Timothy M. Peters, Mark A. Gondree, Zachary N. J. Peterson, "DEFY: A Deniable, Encrypted File System for Log-Structured Storage", NDSS 2015. https://doi.org/10.14722/ndss.2015.23078 。
- Michal Kedziora, Yang-Wai Chow, Willy Susilo, "Improved Threat Models for the Security of Encrypted and Deniable File Systems", Mobile and Wireless Technologies 2017（Lecture Notes in Electrical Engineering）, pp. 223–230, 2017年. https://doi.org/10.1007/978-981-10-5281-1_24 。抄録に当たって内容を確かめた。主眼は、携帯機器とクラウドの普及によって従来の脅威モデルが陳腐化したと論じ、一回限りのアクセス、複数回のアクセス、稼働中の機器への対応という3つの脅威モデルを新たに立てることである。あわせて既知の攻撃経路を整理し、従来の脅威モデルが見落としていた経路を追加している。否認可能ストレージが周辺の痕跡から暴かれるという論点は、この整理の一部として扱われている。物理世界でも「秘密がある痕跡」が別経路から漏れる点で示唆的である。
- Catherine Taylor Clelland, Viviana Risca, Carter Bancroft, "Hiding messages in DNA microdots", Nature, Vol. 399, No. 6736, pp. 533–534, 1999年6月10日. https://doi.org/10.1038/21092 。物理的ステガノグラフィの古典であり、微小点という日常的な記号に秘密を隠す。
- Yinglei Wang, Wing-kei Yu, Sarah Q. Xu, Edwin Kan, G. Edward Suh, "Hiding Information in Flash Memory", IEEE Symposium on Security and Privacy 2013. https://doi.org/10.1109/sp.2013.26 （再検証でDOIを特定し、著者5名と会議名を確認した。以前は検索結果一覧のURLで代用していた）。デバイスの物理的な特性そのものに情報を隠す例である。
- Ching-Chun Chang, Yijie Lin, Isao Echizen, "Cyber-Physical Steganography in Robotic Motion Control", arXiv:2501.04541, 2025年1月8日. https://arxiv.org/abs/2501.04541 （arXiv APIで題名、著者3名、投稿日、抄録を確認した）。「物理的ステガノグラフィ」という語をタイトル級で使う数少ない近年の研究であり、ロボットの動きに秘密を埋め込む。CipherFluteの「物理現象そのものを担体にする」という発想の同時代的な隣接例である。
- Katarzyna Koptyra, Marek R. Ogiela, "Subliminal Channels in Visual Cryptography", Cryptography, Vol. 6, No. 3, 記事番号46, 2022年9月16日. https://doi.org/10.3390/cryptography6030046 （再検証でDOIを特定し、著者2名、巻号、記事番号、公開日を確認した。以前は検索結果一覧のURLで代用していた）。

### 物理的な暗号プリミティブ

- Takaaki Mizuki, Michihito Kumamoto, Hideaki Sone, "The Five-Card Trick Can Be Done with Four Cards", ASIACRYPT 2012（LNCS）, pp. 598–606. https://doi.org/10.1007/978-3-642-34961-4_36 。カードベース暗号の代表例である。
- Ronen Gradwohl, Moni Naor, Benny Pinkas, Guy N. Rothblum, "Cryptographic and Physical Zero-Knowledge Proof Systems for Solutions of Sudoku Puzzles", FUN 2007（LNCS）, pp. 166–182. https://doi.org/10.1007/978-3-540-72914-3_16 、および論文誌版 Theory of Computing Systems, Vol. 44, No. 2, pp. 245–268. https://doi.org/10.1007/s00224-008-9119-9 。日用品（カードや封筒）で暗号プロトコルを実行する研究である。論文誌版の年について訂正を書く。Crossrefの印刷版の発行日は2009年2月であり、2008年と書くのは正確ではない。オンライン先行公開が2008年であったために2008年と表記されることがあるため、引用形式を決めるときに確かめたほうがよい。

### 探索と隠蔽の実証

- Anton Bolfing, Tobias Halbherr, Adrian Schwaninger, "How Image Based Factors and Human Factors Contribute to Threat Detection Performance in X-Ray Aviation Security Screening", USAB 2008（LNCS）, pp. 419–438. https://doi.org/10.1007/978-3-540-89350-9_30 。X線検査における検出性能の規定要因を扱う。
- D. Hardmeier, F. Hofer, A. Schwaninger, "The X-ray object recognition test (X-ray ORT) - a reliable and valid instrument for measuring visual abilities needed in X-ray screening", 第39回 International Carnahan Conference on Security Technology 2005, pp. 189–192. https://doi.org/10.1109/ccst.2005.1594876 。重なりや向きによって物体が見つけにくくなることを測る標準テストである。
- Eugene Winograd, Robert M. Soloway, "On forgetting the locations of things stored in special places", Journal of Experimental Psychology: General, Vol. 115, No. 4, pp. 366–372, 1986年12月. https://doi.org/10.1037/0096-3445.115.4.366 。「特別な場所に隠すほど思い出せなくなる」という古典的知見である。CipherFluteの利用者自身が隠し場所を忘れる危険を論じるときに使える。
- Alan S. Brown, Tamara A. Rahhal, "Hiding valuables: A questionnaire study of mnemonically risky behavior", Applied Cognitive Psychology, Vol. 8, No. 2, pp. 141–154, 1994年4月. https://doi.org/10.1002/acp.2350080205 。貴重品を隠す行動とその記憶上の危険性の質問紙調査である。
- John Knowles, Nicola Persico, Petra Todd, "Racial Bias in Motor Vehicle Searches: Theory and Evidence", Journal of Political Economy, Vol. 109, No. 1, pp. 203–229, 2001年2月. https://doi.org/10.1086/318603 （再検証でDOIを特定し、著者3名、巻号、ページを確認した。以前は検索結果一覧のURLで代用していた。なお同題の全米経済研究所の作業論文が1999年12月に出ており、そのDOIは10.3386/w7449 である）。捜索が実際に禁制品を発見する確率を扱う経済学の代表的研究である。
- Steve Alpern, Shmuel Gal, The Theory of Search Games and Rendezvous, Springer, 2003年（International Series in Operations Research & Management Science）. https://doi.org/10.1007/b100809 。書籍そのもののDOIで、著者2名（ロンドン・スクール・オブ・エコノミクスのSteve Alpernとハイファ大学のShmuel Gal）と2003年という刊行年を出版社ページで確認した。以前この項目は章のDOI（https://doi.org/10.1007/0-306-48212-6_5 、第5章 "Miscellaneous Search Games", pp. 79–97, Kluwer Academic Publishers, ISBN 0792374681）で代用しており、その章のDOIには著者名も刊行年も登録されていない。隠す側と探す側の最適戦略を扱う数理的枠組みである。

### 難読化と不透明性の理論

- Woodrow Hartzog, Frederic D. Stutzman, "The Case for Online Obscurity", 2010年（SSRN Electronic Journal）. https://doi.org/10.2139/ssrn.1597745 。「秘匿ではない不透明性」に法的な保護価値を認める議論であり、CipherFluteの物理層の位置づけと平行する。なおこの論考は後に法律雑誌に掲載されたと考えられるが、その掲載版の書誌はCrossrefに登録が見当たらず、法律雑誌の当該ページにも到達できなかったため確認できていない。引用は上のSSRN版で行うのが確実である。
- Ari Juels, Ronald L. Rivest, "Honeywords: making password-cracking detectable", ACM CCS 2013, pp. 145–160. https://doi.org/10.1145/2508859.2516671 。Crossrefの登録は題名が「Honeywords」だけになっているため、副題はSemantic Scholarの書誌で確認した。偽の候補を混ぜて攻撃者のコストを上げ、かつ攻撃を検出可能にする設計である。CipherFluteが将来おとりの笛を混ぜる拡張を考えるなら直接の参考になる。

### 暗号資産の鍵管理

- Myrto Arapinis, Andriana Gkaniatsou, Dimitris Karakostas, Aggelos Kiayias, "A Formal Treatment of Hardware Wallets", Financial Cryptography and Data Security 2019（LNCS）, pp. 426–445. https://doi.org/10.1007/978-3-030-32101-7_26 。
- Katharina Krombholz, Aljosha Judmayer, Matthias Gusenbauer, Edgar Weippl, "The Other Side of the Coin: User Experiences with Bitcoin Security and Privacy", Financial Cryptography and Data Security: 20th International Conference, FC 2016（バルバドス・クライストチャーチ, 2016年2月22日から26日）の改訂選抜論文集（LNCS, 2017年刊）, pp. 555–580. https://doi.org/10.1007/978-3-662-54970-4_33 。会議は2016年で、予稿集の刊行が2017年である。この関係は出版社の書籍ページ https://link.springer.com/book/10.1007/978-3-662-54970-4 で確認した。
- Artemij Voskobojnikov, Oliver Wiese, Masoud Mehrabi Koushki, Volker Roth, Konstantin Beznosov, "The U in Crypto Stands for Usable: An Empirical Study of User Experience with Mobile Cryptocurrency Wallets", ACM CHI 2021, pp. 1–14. https://doi.org/10.1145/3411764.3445407 。
- Hristo Bojinov, Daniel Sanchez, Paul Reber, Dan Boneh, Patrick Lincoln, "Neuroscience meets cryptography: crypto primitives secure against rubber hose attacks", Communications of the ACM, Vol. 57, No. 5, pp. 110–118, 2014年5月. https://doi.org/10.1145/2594445 。副題と抄録をCrossrefで確認した。強要（いわゆるゴムホース攻撃）に対して、認知心理学の暗黙学習の考えを使い、本人が鍵を明かせないようにする設計である。CipherFluteの強要下の脅威を論じる際の対極の設計として引ける。
- Alexei Czeskis, David J. St. Hilaire, Karl Koscher, Steven D. Gribble, Tadayoshi Kohno, Bruce Schneier, "Defeating Encrypted and Deniable File Systems: TrueCrypt v5.1a and the Case of the Tattling OS and Applications", USENIX HotSec 2008. https://www.usenix.org/legacy/events/hotsec08/tech/full_papers/czeskis/czeskis_html/ 。再検証でUSENIXの旧予稿集ページに到達し、題名、著者6名、抄録を確認できたため、この項目を「未検証のまま残ったもの」から移した。抄録によれば、Windows Vista本体、Microsoft Word、Google Desktopのいずれもが、TrueCryptの否認可能ファイルシステムの否認可能性を損なうことを見いだしている。ファイルシステム自体が数学的な意味で否認可能であっても、その周囲の環境が否認可能性を崩すという論点であり、物理世界の隠蔽にもそのまま当てはまる。

### 日本語圏のその他の関連

- 加藤大弥, 林達也, 砂原秀樹, 「サイバーフィジカル時代の物理媒体による認証・識別に関する考察」, コンピュータセキュリティシンポジウム2017論文集, Vol. 2017, No. 2, 2017年10月16日. https://cir.nii.ac.jp/crid/1050011097170108928 および情報処理学会電子図書館 https://ipsj.ixsq.nii.ac.jp/records/187256 。抄録には、指紋認証に対するいわゆる「グミ指」の攻撃と並んで、3Dプリンタによる「判子の危殆化」が喫緊の課題として挙げられている。ページ番号はCiNii Researchの書誌に記録がない。
- 吉田妃菜, 松崎なつめ, 「紙を用いた立体QRコードの基礎検討」, コンピュータセキュリティシンポジウム2021論文集, pp. 530–534, 2021年10月19日. https://cir.nii.ac.jp/crid/1050855522064066816 および情報処理学会電子図書館 https://ipsj.ixsq.nii.ac.jp/records/214472 。
- ピヤラット シラパスパコォンウォン, 鈴木雅洋, 海野浩, 「3Dプリント用デジタルデータの著作権保護のための情報ハイディング技術」, 電子情報通信学会技術研究報告, Vol. 114, No. 117, pp. 265–270, 2014年7月. https://cir.nii.ac.jp/crid/1520009408040188672 。
- 茂出木敏雄, 「違法造形物の3Dプリンタによる製造を規制するための3Dデータ照合技術に関する研究」, 尚美学園大学芸術情報研究, Vol. 25, pp. 101–120, 2016年3月31日. https://cir.nii.ac.jp/crid/1050282677910856960 、および高精度化の続報「違法造形物の3Dプリンタによる製造を規制するための3Dデータ照合技術の高精度化」, 同誌 Vol. 28, pp. 1–19, 2018年3月31日. https://cir.nii.ac.jp/crid/1050282677911423360 。

---

## 未検証のまま残ったもの

以下は、存在の可能性が高いと考えられるものの、この調査の範囲では一次資料に到達できなかったため、論文に書く場合は改めて確認が必要である。2026年7月30日の再検証で、このうち2件（もとの2番と3番）は確認が取れたか、あるいは記述を差し替えられる状態になった。

1. Roger G. Johnston, Anthony R. E. Garcia, "Vulnerability Assessment of Security Seals", Journal of Security Administration, Vol. 20, 1997年。実在はほぼ確実であるが、Crossrefにこの書誌の登録がなく、当該誌のページにも到達できなかったため、依然として一次資料での確認ができていない。ただし再検証で、2つの査読文献の参考文献一覧に載った書誌を取得できた。すなわちジョンストン自身の2001年のScience & Global Security論文の注11は「Journal of Security Administration 20 (1997): 15-23」と書き、アペルの2011年のTISSEC論文の参考文献一覧は「J. Sec. Admin. 20, 15-27」と書いている。巻は20で一致するが、終わりのページが23と27で食い違う。したがって巻号ページを断定して書くことはできない。この食い違いを解消できないうちは、この文献を引くのは避け、Crossrefで確認できた Johnston, "Effective Vulnerability Assessment of Tamper-Indicating Seals", Journal of Testing and Evaluation, Vol. 25, No. 4, pp. 451–455, 1997年（https://doi.org/10.1520/jte11883j ）を代わりに引くのが安全である。なお両論文はロスアラモス国立研究所の公開版の場所（http://lib-www.lanl.gov/la-pubs/00418796.pdf ）を挙げているが、このURLは現在は別の場所へ転送され、当該PDFには到達できなかった。
2. アメリカ国土安全保障省監察官室による空港保安検査の覆面テストの失敗率（95パーセントという数字が広く報じられている）。政府の一次報告書に到達できなかった。出現率効果の実務的な裏づけとして魅力的だが、確認できるまで論文には書かないほうがよい。
3. Bruce Schneier, Beyond Fear（2003年）における「セキュリティ劇場（security theater）」の議論。再検証で書籍そのものは著者本人の公開ページ https://www.schneier.com/books/beyond-fear/ で確認できた。すなわち Bruce Schneier, Beyond Fear: Thinking Sensibly about Security in an Uncertain World, Copernicus Books, 2003年9月, 296ページ, ハードカバーのISBNは0-387-02620-7である。しかし同ページの本文には「security theater」という語が現れず、その語がこの書籍の中で使われているかどうかは確認できていない。この語の定義を引きたい場合は、著者本人のサイトで全文を確認できる Bruce Schneier, "Beyond Security Theater", New Internationalist, No. 427, 2009年11月, pp. 10–13（https://www.schneier.com/blog/archives/2009/11/beyond_security.html ）を引くのが確実である。この記事には、セキュリティ劇場とは実際の安全性を少しも高めずに人々を安心させるだけの対策を指す、という定義が書かれている。
4. 「隠し金庫（diversion safe）」「日用品に偽装した容器」を扱う学術文献。Internet Archive Scholarで検索した結果、1950年代の歯科医師会誌の広告や1881年の雑誌記事など、学術研究ではないものしか出てこなかった。存在しないという判断に傾いているが、犯罪学や税関の実務文献まで当たり切れていない。
5. Sneakeyのプロジェクトページ。カリフォルニア大学サンディエゴ校の公開ページには依然として到達できない。ただし再検証で論文本体のPDF（https://cseweb.ucsd.edu/~savage/papers/CCS08OptDecode.pdf ）を取得でき、そこで「Sneakey」が試作系の名前であることと、複製鍵で実際に錠を開けたことを本文で確認できた。したがってプロジェクトページを引く必要はない。

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

2. OpenAlexとSemantic Scholarが繰り返しHTTP 429を返し（OpenAlexは再試行まで約24時間と応答した）、被引用関係をたどる芋づる式の探索がほとんどできなかった。Johnstonの封印研究、Appelの投票機研究、Burgessらの3Dプリント鍵複製の被引用一覧をたどれば、さらに近い研究が出てくる可能性がある。2026年7月30日の再検証では、OpenAlexとSemantic Scholarのいずれも書誌の個別照会には応答したため、被引用をたどる芋づる式の探索は改めて試す価値がある。ただし再検証は書誌の確認に絞って行ったので、被引用の探索そのものは今回も行っていない。

3. ACM Digital Library、IEEE Xplore、MDPIの各サイトがいずれも403を返したため、抄録の確認をCrossrefと著者公開版に頼った。ただし再検証では、USENIXのサイトはブラウザと同じUser-Agentを付けたHTTP要求であれば200を返し、WOOT '15とUSENIX Security 2021とHotSec 2008の予稿集ページを取得できた。Chameleon Devices（CHI 2017）についても、著者所属機関がfigshare上に公開している本文PDFを取得して抄録と本文の記述を直接確認できたので、この穴は埋まった。

4. 税関、警察、刑務所における隠匿物の捜索の成功率を扱う実証研究を、犯罪学と法執行の専門誌まで掘り下げられなかった。Knowles らの経済学的研究には到達したが、これは差別の検証が主眼であり、隠匿の巧拙と発見率の関係を扱っていない。麻薬探知犬の性能評価（Porritt らの研究など）にも当たっていない。

5. 日本語文献について、CiNii Researchの全文検索は語をすべて含む条件で動くため、語の選び方に結果が強く依存した。情報処理学会電子図書館、WISSの各年の予稿集ページ、インタラクションのプログラムページには直接当たれていない。とくにWISSで「隠す」「秘密」を扱ったインタフェース研究がある可能性は残っている。

6. 特許文献をまったく調べていない。日用品に情報を埋め込む、あるいは音で情報を読み出す機構は、学術論文より特許に先に現れている可能性がある。

7. 「security by obscurity」の是非を扱う理論的な文献（Ross Andersonのオープン系と閉鎖系の比較など）を確認できなかった。Crossrefの検索では該当が出ず、原典のURLに到達していない。CipherFluteが物理層の役割を主張する際の理論的な文脈として、追って確認する価値がある。

---

## 検証の記録

2026年7月30日、この文献一覧を作成した担当者とは別の担当者が、書誌情報の実在を独立に検証した。検証したのは、この一覧に書誌情報として現れる文献のすべてで、合計67件である。内訳は次のとおりである。「新規性への脅威が大きい文献」の節に19件（項目番号は15までだが、番号4と7と14がそれぞれ複数の文献をまとめているため件数は増える）、「背景として押さえるべき文献」の節に46件（Cachinの会議版と論文誌版、Gradwohlらの会議版と論文誌版、茂出木の2本をそれぞれ別に数えた）、「未検証のまま残ったもの」の節に文献の形をしているものが2件である。このうち65件については実在を一次資料で確認でき、確認できなかったのは1件（Johnston と Garcia の1997年論文）と、書籍自体は確認できたが引用しようとしている記述の所在が確認できなかった1件（Schneierの Beyond Fear）である。

検証の方法を述べる。DOIを持つ51件は、DOI登録機関であるCrossrefの登録データ（api.crossref.org）に1件ずつ直接照会し、題名、著者名の綴りと人数、掲載誌名または予稿集名、巻、号、ページ、発行年月を照合した。日本語の8件は、CiNii Researchの各書誌をJSON形式で取得し、題名、著者名、掲載誌名、巻、号、ページ、発行日、抄録を照合し、あわせて情報処理学会電子図書館の該当レコードの所在も確かめた。DOIを持たない残りについては、USENIXの3件（Burgessら、Ramesh らのKeynergy、Czeskisら）はUSENIXの予稿集ページを、arXivの2件（DeepKey、Chang らの論文）はarXivのAPIを、codex32はBitcoin改善提案の公式リポジトリの本文を、Blazeの金庫の草稿は著者本人が公開しているPDFを、それぞれ直接取得して確認した。会議名と刊行年の関係が疑わしい3件（Desmedtらの2000年の論文、Krombholzらの論文、Alpern と Gal の書籍）は、出版社の書籍ページまで遡って収録書の正式名称と刊行年を確かめた。抄録がCrossrefに登録されていないものは、著者所属機関の業績データベースや機関リポジトリ（ポーツマス大学、コンコルディア大学、サセックス大学）、PubMed、EuropePMCまで当たった。

数値や事実の主張については、原典の本文まで当たって裏を取った。Johnstonの2001年論文はPDF全文を取得し、120種類の封印、所要時間が3秒から2時間で平均が5分をはるかに下回ること、核関連用途に限れば平均8分未満であること、攻撃1件あたりの平均費用55ドル、という4つの数値すべてが本文の同一段落に書かれていることを確かめた。アペルの2011年論文もPDF全文を取得し、40ドル未満の工具、1、2時間の練習、平均13秒（2台の投票機で10回試行）、ヒートガン80秒と剥離40秒、ケーブル錠50秒、法廷での45分未満とそのうちの7分、という数値すべてを本文で確かめた。ウルフらの2005年論文は著者最終稿の全文を取得し、出現率50パーセントで見落とし7パーセント、10パーセントで16パーセント、1パーセントで30パーセント、という数値を本文で確かめた。codex32は規格本文で、8文字までの誤りの検出、4文字までの置換誤りまたは8文字までの消失の訂正、最大31シェア、閾値2から9、ペンと紙だけでの計算、をすべて確かめた。Blazeの草稿はPDF全文を取得し、Underwriters Laboratoriesの最上位区分が15分、30分、60分であること、攻撃の3分類の定義、金庫業界におけるsecurity-by-obscurityの位置づけを確かめた。Chameleon Devicesは著者所属機関が公開する本文PDFを取得し、調査地と参加者数を確かめた。

訂正は8か所に加えた。第1に、アペルの論文について、州が導入した封印体制は3世代ではなく4世代である。第2に、同じ論文が示している判定基準は「遅延を生むか事後に検出されるか」という2択ではなく、封印の運用手順が満たすべき8項目の条件の一覧であり、原典には「遅延」に当たる語が一度も現れない。この2点を本文に沿って書き直した。第3に、Desmedtらの2000年の論文が載ったのは「Information Hiding 2000」という会議ではなく、1999年にドレスデンで開かれた第3回Information Hidingワークショップであり、その予稿集がLNCS第1768巻として2000年に刊行されたものである。第4に、米国音響学会誌に2024年に載ったRamesh らの記事は、鍵の音響推定の系列の論文誌版ではなく、大会の講演要旨として補遺号に載った1ページの抄録である。第5に、Chameleon Devicesの調査地からムンバイを削った。ムンバイは共著者2名の所属であるインド工科大学ボンベイ校の所在地であって調査地ではなく、実際の調査地はバンガロールとケープタウンのランガ地区とナイロビ周辺である。第6に、Blazeの金庫の文献をペンシルベニア大学の技術報告と書いていたのを、査読を経ていない著者公開の草稿に直した。表紙に技術報告番号も叢書名もないことを確認した。第7に、Burgessらの研究の要約を、原典の抄録の記述に合わせて書き直した。抄録が述べているのは、出力した鍵素材と切削済みの鍵がいくつかの一般的なピンタンブラー錠で機能する解像度を持ち、材料が攻撃に耐える強度を持つこと、および写真1枚からキーブランクのCADモデルを生成する道具を作ったことである。第8に、クロフォードとイリベリの論文が著者ら自身の新しい実験ではなく、ルビンシュタインやトヴェルスキーらの既存の実験の再分析であることを明記した。

以上の8か所が内容そのものの誤りである。これに加えて、書誌の細部についても次の訂正を入れた。Gradwohlらの論文誌版は2008年ではなく、Crossrefの印刷版の発行日が2009年2月である。Kedzioraらの論文の収録書名は Mobile and Wireless Technologies 2017（Lecture Notes in Electrical Engineering）である。Solaらの総説の巻号は第15巻第1号の記事番号85で、公開日は2021年12月23日である。Krombholzらの論文が載ったのは2016年のFinancial Cryptography and Data Securityの改訂選抜論文集で、刊行が2017年である。Canettiらの論文はCrossrefの登録で第1著者名が「Rein Canetti」と誤記されている。Laxton らの論文、PrinTracker、Honeywords、Chameleon Devicesの4件は、Crossrefの登録で副題が落ちているため、副題を含む完全な題名を別の一次資料で特定して書き添えた。全67件について、巻、号、ページ、発行年月のうち欠けていたものはすべて補った。

このほか、訂正には数えないが記述を強めた箇所がある。ウルフらの2007年論文について、複数の介入が失敗する一方で、高い出現率と完全なフィードバックによる短い再訓練をはさむやり方は成功したという原典の記述を補った。Desmedtらの1998年の論文について、シェアが音楽であって「人間の検閲者に怪しまれない」ことを利点として掲げているという抄録の記述を補い、CipherFluteとの重なりが当初の記述より大きいことを明示した。ニーとミーナハンの2006年論文について、面接した窃盗犯50名のうち45名が予測可能な探索の型を持っていたという数値をポーツマス大学の業績データベースから補った。ジョンストンの2001年論文について、120種類という数値の一次の出所が同論文の注11に挙がるJohnston と Garcia の1997年論文であることを補った。

確認先のURLも6か所差し替えた。もとの一覧では、Johnston と Timmons と Warner の2007年論文、Sola らの総説、Wang らのフラッシュメモリの論文、Koptyra と Ogiela の論文、Knowles らの論文の5件について、確認先として検索結果一覧のURLが書かれていた。検索結果一覧は当該の書誌そのものを指すものではないので、それぞれの書誌を指すDOIを特定して差し替えた。Alpern と Gal の書籍については、著者名も刊行年も登録されていない章のDOIから、著者2名と2003年という刊行年が確認できる書籍そのもののDOIに差し替えた。

実在が確認できなかったために削除した文献は1件もない。したがって「検証で削除したもの」の節は設けていない。

「未検証のまま残ったもの」の節については2件を移動と昇格の形で処理した。Czeskisらの2008年のHotSec論文は、USENIXの旧予稿集ページに到達できたため、題名と著者6名と抄録を確認して「背景として押さえるべき文献」の節に移した。Sneakeyのプロジェクトページは、そもそも引く必要がないことが分かったため、論文本体のPDFで「Sneakey」が試作系の名前であることを確認した旨に書き換えた。逆に、Johnston と Garcia の1997年論文は、依然として一次資料に到達できないうえ、2つの査読文献の参考文献一覧の間で終わりのページが23と27で食い違うことが判明したため、その食い違いを明記したまま未検証に留めた。Schneierの Beyond Fear は、書籍そのものは著者本人のページで確認できたが、「security theater」という語がその書籍の中で使われているかどうかは確認できなかったため、書誌を補いつつ未検証に留めた。

URLの生存についても正直に書いておく。DOIはいずれもCrossrefに登録されていることを確認済みであり、その意味で「生きている」。ただしDOIを解決した先の出版社のページは、機械的な要求に対してHTTP 403を返すものがある。今回の確認では、MDPI、シカゴ大学出版局、Taylor & Francisの各ページがそうであった。したがってこれらの書誌の裏づけは、出版社のページを開けたことではなく、DOI登録機関の登録データに当たれたことに依っている。人間がブラウザで開けば表示されるはずだが、投稿前に手で確かめておくとよい。なおUSENIXの全文PDF、情報処理学会電子図書館のレコード、Springerの書籍ページ、figshare上の本文は、いずれも取得に成功した。

最後に、検証の範囲について正直に書いておく。今回の検証は、書かれている書誌情報が実在するかと、内容の要約が原典と食い違わないかに絞って行った。「この切り口で見つからなかったこと」の節に書かれた否定的な主張（たとえば、日用品に偽装した担体に鍵を保管しその効果を実験で定量化した研究は見つからなかった、という主張）は、探索そのものを再実行していないため検証していない。それらは元の担当者の探索結果として読む必要がある。
