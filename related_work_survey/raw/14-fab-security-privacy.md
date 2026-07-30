# デジタルファブリケーションと安全・プライバシーの交差

## この切り口の要約

この領域には、追加製造（アディティブマニュファクチャリング）を対象とした情報セキュリティ研究が20年近く蓄積されており、ACM CCSには2021年と2022年に専用のワークショップ（AMSec）まで置かれていた。研究は大きく四つの系統に分かれる。第一が造形機の発する音・振動・磁界・消費電力から造形物の形状を復元する側チャネル攻撃であり、第二が造形物を密かに弱くしたり造形機の制御を奪ったりする破壊攻撃であり、第三が造形物や造形機を一意に特定する指紋認識と法科学であり、第四が3次元モデルや造形物への電子透かしと情報ハイディングである。

CipherFluteにとって最も重大なのは第一の系統である。Al Faruqueらは2016年に、家庭用の熱溶解積層方式の造形機が発する音だけから工具経路を復元し、軸の推定精度86パーセント、長さの推定誤差11.11パーセントを達成したと報告した。同じ2016年にSongらは、市販の携帯電話の内蔵センサだけで、通常の設計に対して平均傾向誤差5.87パーセント、複雑な設計に対して9.67パーセントで造形物と制御コードを復元したと報告している。2024年のJamaraniらは、離れた場所に置いた携帯電話の音響と磁界から、軸方向の移動・ステッピングモータの動作・ノズル速度・ロータ速度の推定について平均98.80パーセントの精度を得て、単純な（原文の言葉ではplainな）設計に対して平均傾向誤差4.47パーセントを得たと報告している。CipherFluteは半音1段ごとに管の実効長を5パーセントから6パーセント変えるので、この誤差は半音1段の差にほぼ並ぶ水準まで来ている。さらにGatlinらの論文は表題そのものが「暗号化は無意味である」であり、Dolgavinらは暗号化された造形データでも消費電力から設計を復元できることを産業機で示した。したがって「印刷データに秘密がそのまま載るのでネットワークから切り離した環境で印刷する」という論文の記述は、データ経路については正しいが、放射経路については不十分である。実際、Doらは家庭用造形機がネットワーク越しに侵害されて設計データを持ち出せることを2016年に示しており、切り離しの推奨自体には強い裏づけがある。逆にChhetriらの「Tool of Spies」は、スライサ（造形コンパイラ）を書き換えるだけで側チャネルからの復元率が最大39パーセント上がることを示し、切り離しても道具連鎖が汚染されていれば漏れることを示している。

一方で、造形物に秘密を埋め込むという着想自体は既存である。上平員丈らの一連の研究は造形物の内部に空洞を作って情報を隠し、サーモグラフィやX線で読む方式を2014年から積み上げている。GuptaらはCADモデル内部にQRコードを隠して微小焦点の計算機トモグラフィまたはX線透過写真で読む方式を示している。しかし読み出しの経路はいずれも光学・熱・X線・磁界であり、「人が吹いて音として読む」ものはこの領域には一つも見つからなかった。また「物理層に秘匿の力は無いと宣言して秘匿を秘密分散に全部負わせる」という設計思想も、この領域には見当たらなかった。

## 新規性への脅威が大きい文献

以下では脅威の種類を二つに分けて書く。一つは「同じ発明が既にある」という新規性そのものへの脅威であり、もう一つは「論文が書いている安全性の主張や運用上の推奨が弱まる」という主張への脅威である。CipherFluteの場合、この切り口で見つかったもののうち脅威が最も大きいのは後者である。

### 1. Confidentiality Breach Through Acoustic Side-Channel in Cyber-Physical Additive Manufacturing Systems

- 著者: Sujit Rokka Chhetri, Arquimedes Canedo, Mohammad Abdullah Al Faruque
- 掲載: ACM Transactions on Cyber-Physical Systems, 第2巻第1号, 論文番号3, 全25ページ, 2018年1月号（電子版の公開は2017年12月14日である）。学会発表版は Mohammad Abdullah Al Faruque, Sujit Rokka Chhetri, Arquimedes Canedo, Jiang Wan, "Acoustic Side-Channel Attacks on Additive Manufacturing Systems", 2016 ACM/IEEE 7th International Conference on Cyber-Physical Systems (ICCPS), 論文番号19, 全10ページ, 2016年である。
- 確認先: https://doi.org/10.1145/3078622 （Crossrefの登録内容で著者3名・巻号・全25ページ・要旨を確認し、論文番号3と全25ページは dblp の https://dblp.org/search/publ/api の書誌「3:1-3:25」で確認した。学会版は https://doi.org/10.1109/ICCPS.2016.7479068 で、論文番号19と全10ページは同じくdblpの「19:1-19:10」で確認した）

熱溶解積層方式の造形機が動作中に発する音を1本のマイクロフォンで録り、信号処理と機械学習と文脈に基づく後処理を組み合わせて、造形機に与えられた制御コードと造形物の形状を復元する攻撃を示した論文である。著者らは要旨において「平均の軸推定精度86パーセント、平均の長さ推定誤差11.11パーセント」を報告している（この2つの数値はCrossrefに登録された雑誌版の要旨の本文で確認した）。攻撃者は造形機に触る必要がなく、同じ部屋に居られればよい。この論文はこの分野の出発点であり、以後の全ての音響側チャネル研究がここから枝分かれしている。被引用数は、2026年7月時点のSemantic Scholarの集計で会議発表版（ICCPS 2016）が181件、雑誌版（ACM Transactions on Cyber-Physical Systems）が38件である。この分野で数えられているのは主に会議発表版のほうである。

CipherFluteとの関係は極めて直接的である。CipherFluteの秘密は管の長さそのものであり、この攻撃が復元しようとしている量とまったく同じものである。論文が挙げる「ネットワークから切り離した環境で印刷する」という対策は、データが通信路を通ることを止めるだけで、造形機が音を出すことを止めない。したがって切り離しの推奨は必要条件にすぎず、十分条件ではない、と論文中で明言する必要がある。ただし報告された長さ誤差11.11パーセントは、CipherFluteが半音1段に割り当てている実効長の変化（約5パーセント）の2段分に相当するので、2018年時点の技術では個々のスロットまでは読めなかったと言える。この「読める粒度」と「符号の粒度」の比較は、CipherFluteが自分の脅威モデルを定量的に語るための良い材料になる。

脅威の度合いは高である。理由は、新規性を崩すからではなく、論文が書いている運用上の推奨（切り離して印刷せよ）が防げる範囲を明確に狭めるからである。引用せずに済ませることはできない。

### 2. Practitioner Paper: Decoding Intellectual Property: Acoustic and Magnetic Side-channel Attack on a 3D Printer

- 著者: Amirhossein Jamarani, Yazhou Tu, Xiali Hei
- 掲載: 2nd EAI International Conference on Security and Privacy in Cyber-Physical Systems and Smart Vehicles (EAI SmartSP) 2024, 全22ページ（プレプリントは arXiv:2411.10887, 2024年11月16日投稿）
- 確認先: https://arxiv.org/abs/2411.10887 （arXivの論文ページを取得し、表題・著者・掲載先の記載・要旨を確認した）

前項の攻撃を、専用の測定器ではなく市販の携帯電話で、しかも造形機から離れた位置から行った研究である。音響と磁界の両方を使い、勾配ブースティング決定木で軸方向の移動・ステッピングモータの動作・ノズル速度・ロータ速度を推定し、平均約98.80パーセントの精度を報告している。実際の造形物に適用した評価では、単純な設計（要旨の言葉は "a plain G-code design" である）に対して平均傾向誤差4.47パーセントを得たとしている。要旨は、先行研究が高性能な録音機器を造形機のすぐ近くに置くことを前提にしていたのに対し、自分たちはより遠い距離から携帯電話だけで成功させたと述べている。ただし「携帯電話を使う」こと自体は後述の第8項のSongらが2016年に既に行っているので、この論文の差分は装置の安さではなく距離のほうにあると読むのが正確である。

CipherFluteとの関係は、脅威の現実味を一段上げる点にある。平均傾向誤差4.47パーセントは、CipherFluteが半音1段に割り当てる実効長の変化とほぼ同じ大きさである。ここで実効長の変化の大きさを確認しておく。半音1段の周波数比は2の12乗根で約1.0595であり、f = A/(L+e) の関係から実効長 L+e はその逆数倍になるので、半音上げると実効長は約5.6パーセント縮み、半音下げると約5.9パーセント伸びる。つまり半音1段は実効長で5パーセント台から6パーセント台の差である。つまり、造形中に近所で携帯電話を置かれた場合、隣接スロットの区別が付く水準に技術が到達しつつある。CipherFluteが誤り訂正符号を持っていることは、この文脈では攻撃者の側を助ける方向にも働く。攻撃者が復元した音列に誤りが残っても、同じReed-Solomon符号で訂正できてしまうからである。この指摘は論文の脅威モデル節に必ず書くべきである。

脅威の度合いは高である。この論文が示す精度は、CipherFluteの符号設計の粒度と正面から衝突しており、「造形の瞬間だけは秘密が守られている」という暗黙の前提を崩す。

### 3. Encryption is Futile: Reconstructing 3D-Printed Models Using the Power Side-Channel

- 著者: Jacob Gatlin, Sofia Belikovetsky, Yuval Elovici, Anthony Skjellum, Joshua Lubell, Paul Witherell, Mark Yampolskiy
- 掲載: 24th International Symposium on Research in Attacks, Intrusions and Defenses (RAID) 2021, 135-147ページ, ACM
- 確認先: https://doi.org/10.1145/3471621.3471850 （Crossrefの登録内容を取得して、表題・著者7名・予稿集名・ページを確認した。要旨は Semantic Scholar の登録内容で確認した。ACM Digital Libraryの本文ページは自動取得が拒否された）

造形機の消費電力の波形から造形物の形状を復元する攻撃である。表題が示すとおり、設計ファイルを暗号化しても、造形機が動く時点で電力波形として同じ情報が外に出てしまうので暗号化は無意味だ、という主張を掲げている。要旨は、外部委託の造形において設計者と造形機の間を端から端まで暗号化しても側チャネルで迂回できると述べ、熱溶解積層方式の造形機での評価で復元精度99パーセントを達成したとしている。事前知識をまったく持たずに復元できると明記している点も重要である。

CipherFluteとの関係は、論文の運用上の推奨に対する直接の反論として働く点である。CipherFluteは「印刷データに秘密がそのまま載る」ことを問題視して切り離しを勧めているが、この論文は「データを守っても物理量が漏れる」と述べている。CipherFluteの側で誠実に書くなら、切り離しはデータ経路の対策であって放射経路の対策ではない、と分けて書くべきである。

脅威の度合いは高である。新規性ではなく安全性の主張に効くが、表題が強烈なので査読者が必ず思い出す種類の論文であり、言及がないと不備と見られる。

### 4. Turning Hearsay into Discovery: Industrial 3D Printer Side Channel Information Translated to Stealing the Object Design

- 著者: Aleksandr Dolgavin, Jacob Gatlin, Moti Yung, Mark Yampolskiy
- 掲載: arXiv:2509.18366, 2025年9月22日投稿（査読の有無は確認できていない）
- 確認先: https://arxiv.org/abs/2509.18366 （arXivの論文ページを取得し、表題・著者・投稿日・要旨を確認した）

粉末床溶融結合方式の産業用造形機を対象に、駆動部の消費電力を測って造形物の設計を復元した研究である。差分電力解析の考え方を持ち込み、複数回の測定波形を重ねることで精度を上げている。二つの複雑さの異なるモデルで、真陽性率が最大90.29パーセント、偽陽性率7.02パーセント、偽陰性率9.71パーセントに達したとしている。要旨は、設計の知的財産を守るにはファイルを守るだけでは足りず、製造現場の電力波形や音響放射といった環境要因まで守らなければならないと結論している。

CipherFluteとの関係は、前項と同じ論点をより新しく、より高い精度で述べている点にある。元のファイルが暗号化されていても復元できたと明言しているので、CipherFluteの「切り離して印刷せよ」という一文をそのまま残すと、この分野の常識に対して素朴に見えてしまう。

脅威の度合いは高である。ただしプレプリントであり査読状況が確認できていないので、引用する際は先行の査読論文（第1項と第3項）を主として、これを補強として添えるのがよい。

### 5. Tool of Spies: Leaking your IP by Altering the 3D Printer Compiler

- 著者: Sujit Rokka Chhetri, Anomadarshi Barua, Sina Faezi, Francesco Regazzoni, Arquimedes Canedo, Mohammad Abdullah Al Faruque
- 掲載: IEEE Transactions on Dependable and Secure Computing, 第18巻, 667-678ページ, 2021年
- 確認先: https://doi.org/10.1109/TDSC.2019.2923215 （Semantic Scholarの書誌と要旨を取得して確認した）

造形物のスライス処理を行うソフトウェア（造形コンパイラ）を密かに書き換え、造形機が出す音・電力・振動・電磁波の4つの側チャネルからの制御コード復元成功率を、既存手法に対して最大39パーセント引き上げる攻撃である。攻撃者は造形データを直接盗む必要がなく、道具連鎖のどこかに手を入れておけばよい。

CipherFluteとの関係は、切り離しという対策の抜け道を示す点にある。CipherFluteの現在の実装はBambu Studio系のスライサとPythonの自作スクリプトを通しているので、その部分が汚染されていれば、造形機をネットワークから切り離しても秘密が外へ漏れる。論文が推奨すべき対策は「切り離す」だけではなく「スライサとファームウェアの真正性を確かめる」「造形後に一時ファイルと造形機内の残留データを消す」まで含むべきである。

脅威の度合いは高である。運用上の推奨の書き換えを要求する種類の指摘である。

### 6. A Data Exfiltration and Remote Exploitation Attack on Consumer 3D Printers

- 著者: Quang Do, Ben Martini, Kim-Kwang Raymond Choo
- 掲載: IEEE Transactions on Information Forensics and Security, 第11巻第10号, 2174-2186ページ, 2016年
- 確認先: https://doi.org/10.1109/TIFS.2016.2578285 （Crossrefの登録内容を取得して、表題・著者・巻号ページを確認した。IEEE Xploreの本文ページは自動取得できず、要旨は取得できていない）

家庭用の3次元造形機を対象に、ネットワーク越しに造形機を遠隔から悪用し、造形に使われた設計データを外に持ち出す攻撃を示した論文である。家庭用機の通信プロトコルが認証をほとんど持たないことに着目している。

CipherFluteとの関係は、「切り離して印刷せよ」という推奨に対する最も直接的な裏づけである。CipherFluteの査読者に対して、この推奨が思いつきではなく既知の脅威に基づくものだと示すために、まずこの論文を引くのがよい。あわせてMillerらの残留データの論文（後述）を引けば、造形前・造形中・造形後の三つの局面を押さえられる。

脅威の度合いは中である。新規性を脅かさず、むしろ論文の主張を支える方向に働くが、この記述の根拠として必ず引く必要がある。

### 7. Side-Channel Attacks Bypass Protection in 3D Printers

- 著者: Eric Yocam, Varghese Vaidyan, Micah Flack, Gurcan Comert, Judith L. Mwakalonge
- 掲載: arXiv:2606.13952, 2026年6月11日投稿, 全11ページ（査読の有無は確認できていない）
- 確認先: https://arxiv.org/abs/2606.13952 （arXivのAPIで表題・著者5名・投稿日・注記・要旨の全文を確認した）

市販の熱溶解積層方式の造形機に搭載されている能動的なモータ騒音打ち消し機構（原文の言葉ではActive Motor Noise Cancellation、略してAMNC）を、知的財産保護の観点から評価した研究である。同期して収録された音響と振動の公開データセットを使い、Bambu Lab社の騒音打ち消し機構付きの造形機2台、12種類の造形物の分類問題を立てた。要旨によれば、この機構は音響チャネルを完全に無力化し、分類精度は無作為の基準値8.33パーセントと区別が付かない水準まで落ちる。しかし機構が対象にしていない振動は残り、要約統計量では約31パーセント（機体ごとに36パーセントから47パーセント）、造形順序をそのまま入れる時系列モデルでは約61パーセントの精度が得られたとしている。順序を混ぜる対照実験では約33パーセントに落ちるので、精度のかなりの部分は造形の進行順序に由来するとしている。また識別器は造形機ごとに固有で、別の機体には転移しないと述べている。

ここは正確に書き写す必要がある。要旨の結論は「音響は防げても振動・磁界・電力は開いたまま」で終わっているのではない。要旨は、振動チャネルは部分的で形状と相関するにとどまり、このデータセットでは完全な幾何形状の復元を支えるところまでは行かない、と明言している。復元に足る水準の攻撃をするなら、騒音打ち消し機構が手を付けていない磁界か電力のチャネルが必要になる、という言い方である。

CipherFluteとの関係は、使用している造形機が実際にBambu Lab社の機体（A1 miniとH2D）である点で、他人事ではない。良い知らせは2つある。当該機体の騒音打ち消し機構が音響チャネルをほぼ潰すこと、そしてこのデータセットでは振動だけでは形状の完全復元に届いていないことである。悪い知らせは、磁界と電力が手つかずで残っていることである。CipherFluteの脅威モデル節は、この3点をそのまま書けば非常に具体的で説得力のある議論になる。振動が形状復元に届いていないという部分を落として「振動でも読める」と書くと、原典より強い主張になってしまうので注意が必要である。

脅威の度合いは高である。使用機材そのものを扱った最新の評価であり、脅威モデルの記述の精度を大きく変える。ただしプレプリントなので、断定を避けて「プレプリントの段階での報告によれば」と書く配慮が必要である。

### 8. My Smartphone Knows What You Print: Exploring Smartphone-based Side-channel Attacks Against 3D Printers

- 著者: Chen Song, Feng Lin, Zhongjie Ba, Kui Ren, Chi Zhou, Wenyao Xu（いずれもニューヨーク州立大学バッファロー校）
- 掲載: Proceedings of the 2016 ACM SIGSAC Conference on Computer and Communications Security (CCS 2016), 895-907ページ
- 確認先: https://doi.org/10.1145/2976749.2978300 （Crossrefの登録内容を取得して、表題・著者6名と所属・予稿集名・ページ・公開日を確認した。要旨はACM Digital Libraryが自動取得を拒否するため、OpenAlex に登録された要旨の全文で確認した。確認先は https://api.openalex.org/works/doi:10.1145/2976749.2978300 である）

造形機のそばに市販の携帯電話を置くだけで、その内蔵センサから造形物を推定する攻撃である。要旨によれば、音響と磁界の側チャネルを携帯電話の内蔵センサで捉え、さらに磁界で補強した攻撃モデルで造形機の重要な方向動作を推定する。結果として、通常の設計に対して平均傾向誤差5.87パーセント、複雑な設計に対して9.67パーセントで、造形物とその制御コードを復元したとしている。攻撃に特別な機材が要らないという点を前面に出しており、Al Faruqueらの研究と並んで、この脅威が現実的であることを広く知らせた論文である。

CipherFluteとの関係は第2項と同じ系統だが、こちらは査読を通ったトップ会議の論文であり、引用の重みが違う。「工房や研究室で造形している最中に、机に置かれた誰かの携帯電話が秘密を録っている」という具体的な絵を描くのに適している。加えて、この論文と第2項は平均傾向誤差という同じ指標を使っているので、直接比べられる。2016年の5.87パーセントから2024年の4.47パーセントへの改善であり、8年でこの程度しか動いていない。CipherFluteの側で脅威を論じるときは、「携帯電話による復元の粒度は、10年ほど前から半音1段（実効長で5パーセント台から6パーセント台）とほぼ同じところに張り付いている」と書くのが最も正確である。過度に「近年急速に精度が上がった」と書くと原典と食い違う。

脅威の度合いは中である。運用上の推奨に効くが、より新しい第2項があるので、こちらは系統の起点として引くのがよい。

### 9. 造形物の内部に情報を隠す一連の研究（上平員丈・鈴木雅洋・ピヤラット シラパスパコォンウォン・鳥井秀幸・高嶋洋一ら）

この系統の中心人物の名前について、前の調査者が書いていた記述には誤りがあったので、まず正しておく。英語論文で Kazutake Uehira と表記される人物の日本語表記は「上平員丈」であり、神奈川工科大学の研究者である。「海野浩」は Hiroshi Unno という別人であり、初期の論文の共著者の一人にすぎない。CiNii Researchの同一著者情報で、2014年の情報処理学会研究報告の記事に「海野 浩（Hiroshi Unno）」と「上平 員丈（Kazutake Uehira）」が別々の著者として並んで載っていることを確認した（確認先 https://cir.nii.ac.jp/crid/1573105977687785088 ）。よってこの系統は「上平員丈らの研究」と呼ぶのが正しい。以下、本文中の呼び方もすべて改めた。なお「鳥井秀幸」が Hideyuki Torii の日本語表記であることは、同じ著者の別分野の論文（符号系列の研究）の日本語書誌で確認した。

主な文献を確認できた順に挙げる。

- Masahiro Suzuki, Piyarat Silapasuphakornwong, Kazutake Uehira, Hiroshi Unno, Youichi Takashima, "Copyright Protection for 3D Printing by Embedding Information Inside Real Fabricated Objects", 10th International Conference on Computer Vision Theory and Applications (VISAPP) 2015, 180-185ページ, 確認先 https://doi.org/10.5220/0005342401800185
- Kazutake Uehira, Satoru Baba, Masahiro Suzuki, Piyarat Silapasuphakornwong, Hideyuki Torii, Youichi Takashima, "Hiding Information in 3D Printed Objects by Forming Fine Cavities inside Objects", 2nd World Congress on Electrical Engineering and Computer Systems and Science 2016, 確認先 https://doi.org/10.11159/mhci16.102
- Kazutake Uehira, Masahiro Suzuki, Piyarat Silapasuphakornwong, Hideyuki Torii, Youichi Takashima, "Copyright Protection for 3D Printing by Embedding Information Inside 3D-Printed Objects", Digital Forensics and Watermarking (IWDW), Lecture Notes in Computer Science, 370-378ページ, 2017年, 確認先 https://doi.org/10.1007/978-3-319-53465-7_27
- Masahiro Suzuki, Piyarat Silapasuphakornwong, Youichi Takashima, Hideyuki Torii, Kazutake Uehira, "Number of Detectable Gradations in X-Ray Photographs of Cavities Inside 3-D Printed Objects", IEICE Transactions on Information and Systems, 第E100.D巻, 1364-1367ページ, 2017年, 確認先 https://doi.org/10.1587/transinf.2016edl8213
- Piyarat Silapasuphakornwong, Masahiro Suzuki, Youichi Takashima, Hideyuki Torii, Kazutake Uehira, "New Technique of Embedding Information Inside 3-D Printed Objects", Journal of Imaging Science and Technology, 第63巻第1号, 010501-1から010501-8ページ, 2019年, 確認先 https://doi.org/10.2352/j.imagingsci.technol.2019.63.1.010501 。要旨を取得して内容も確認した。造形物の内部に微小な空洞を作り、空洞の熱伝導率が本体より低いことを使って表面温度から空洞の配置を読む方式である。熱溶解積層方式の造形機とサーモグラフィで実験し、表面が曲面であっても2ミリメートル×2ミリメートルという小さな空洞まで検出できたとしている。
- Masahiro Suzuki, Hideyuki Torii, Kazutake Uehira, "GAN technique for reading QR code embedded in 3D printed object", 2023 5th International Conference on Image, Video and Signal Processing, 157-163ページ, 2023年, 確認先 https://doi.org/10.1145/3591156.3591179
- 日本語版として、ピヤラット シラパスパコォンウォン, 鈴木雅洋, 海野浩「3Dプリント用デジタルデータの著作権保護のための情報ハイディング技術」電子情報通信学会技術研究報告, 第114巻第117号, 265-270ページ, 2014年7月, 確認先 https://cir.nii.ac.jp/crid/1520009408040188672 （この書誌のCiNii登録は著者3名である）、および同題で ピヤラット シラパスパコォンウォン, 鈴木雅洋, 海野浩, 上平員丈, 高嶋洋一「3Dプリント用デジタルデータの著作権保護のための情報ハイディング技術」情報処理学会研究報告CSEC, 2014年第40号, 1-6ページ, 2014年6月26日, 確認先 https://cir.nii.ac.jp/crid/1573105977687785088 （こちらは著者5名である。前の調査者は両方を著者3名と書いていたので改めた）

以下の3件は、前の調査者が本文で「金属を混ぜたフィラメント」「近赤外の蛍光染料」「強磁性のセル」と述べていた方式の典拠である。前の記述には典拠が付いていなかったので、Crossrefの書誌検索で当該論文を突き止めて補った。

- Piyarat Silapasuphakornwong, Chaiwuth Sithiwichankit, Kazutake Uehira, "Information Embedding in 3D Printed Objects Using Metal-Infused PLA and Reading with Thermography", NIP & Digital Fabrication Conference, 第34巻, 202-207ページ, 2018年, 確認先 https://doi.org/10.2352/issn.2169-4451.2018.34.202
- Piyarat Silapasuphakornwong, Hideyuki Torii, Kazutake Uehira, Apisara Funsian, Kewalee Asawapithulsert, Tattawat Sermpong, "Embedding Information in 3D Printed Objects Using Double Layered near Infrared Fluorescent Dye", International Journal of Materials, Mechanics and Manufacturing, 第7巻第6号, 230-234ページ, 2019年, 確認先 https://doi.org/10.18178/ijmmm.2019.7.6.465
- Piyarat Silapasuphakornwong, Hideyuki Torii, Masahiro Suzuki, Kazutake Uehira, "Effects of Embedded Depth of Internal Printed Ferromagnetic Cell on Data Clarity of Rewritable 3D Objects", NIP & Digital Fabrication Conference, 第37巻, 28-31ページ, 2021年, 確認先 https://doi.org/10.2352/issn.2169-4451.2021.37.28

造形物の内部に微小な空洞を作る、金属を混ぜたフィラメント（金属を含ませたPLA）で内部に領域を作る、近赤外の蛍光染料を二層に置く、内部に強磁性のセルを印刷するなど、さまざまな方式で造形物の中に情報を隠し、サーモグラフィ・X線写真・近赤外撮影・磁気センサで読み出す。ただし表題まで確かめると、金属を混ぜたフィラメントの場合の読み出しもサーモグラフィである。目的は主に著作権保護であり、読み出した情報は権利者の識別子である。10年以上にわたって同じ着想を材料と読み出し手段を変えながら深めており、この分野の日本国内の中心的な系統である。

CipherFluteとの関係は、「日用品に見える3次元造形物の内部に、外から見えない情報を隠す」という枠組みがすでに確立していることを示す点にある。CipherFluteの差分は三つある。第一に、読み出しがサーモグラフィやX線ではなく人間の息と汎用のマイクロフォンだけで済むことである。第二に、埋め込む中身が権利者の識別子ではなく暗号資産の復元情報という高価値の秘密であり、そのため脅威モデルを明示していることである。第三に、秘匿の力を物理層に求めず秘密分散に負わせている点である。この三つを明確に書けば差分は立つ。

脅威の度合いは中である。着想の骨格が近いので必ず引用して差分を述べる必要があるが、読み出し手段と目的が異なるので新規性が崩れるとは考えにくい。

### 10. CADモデルの内部に認証符号を隠す一連の研究（Fei Chen, Nikhil Gupta ら）

- Fei Chen, Gary Mac, Nikhil Gupta, "Security features embedded in computer aided design (CAD) solid models for additive manufacturing", Materials & Design, 第128巻, 182-194ページ, 2017年, 確認先 https://doi.org/10.1016/j.matdes.2017.04.078
- Fei Chen, Yuxi Luo, Nektarios Georgios Tsoutsos, Michail Maniatakos, Khaled Shahin, Nikhil Gupta, "Embedding Tracking Codes in Additive Manufactured Parts for Product Authentication", Advanced Engineering Materials, 第21巻, 2018年, 確認先 https://doi.org/10.1002/adem.201800495
- Fei Chen, Jian H. Yu, Nikhil Gupta, "Obfuscation of Embedded Codes in Additive Manufactured Components for Product Authentication", Advanced Engineering Materials, 第21巻, 2019年, 確認先 https://doi.org/10.1002/adem.201900146
- Fei Chen, Jaime Zabalza, Paul Murray, Stephen Marshall, Jian Yu, Nikhil Gupta, "Embedded product authentication codes in additive manufactured parts: Imaging and image processing for improved scan ability", Additive Manufacturing, 第35巻, 101319, 2020年, 確認先 https://doi.org/10.1016/j.addma.2020.101319
- Nikhil Gupta, Fei Chen, Nektarios Georgios Tsoutsos, Michail Maniatakos, "ObfusCADe: Obfuscating Additive Manufacturing CAD Models Against Counterfeiting", Design Automation Conference (DAC) 2017, 論文番号82, 全6ページ, 確認先 https://doi.org/10.1145/3061639.3079847 （dblpの書誌では表題の末尾に "Invited" と付いており、招待論文である）

部品の内部に二次元コードを分割して埋め込み、微小焦点の計算機トモグラフィまたはX線透過写真で撮影して復元する。ただ埋めるだけでは第三者にも読まれてしまうので、符号を意図的に散らして難読化し、正しい復元手順を知る者だけが読めるようにする方向へ発展している。2019年の論文では、特定の方向から見たときだけ正しく像が結ぶように分片を配る難読化や、複数の識別符号を互いに入り込ませて埋める難読化が示されている。ObfusCADeは、CADモデルの側に設計の完全性に干渉する特殊な特徴を仕込み、正しい加工条件でしか良品ができないようにすることで模造を妨げる考え方である。前の調査者は「偽の特徴を混ぜて模造を妨げる」と書いていたが、要旨の言い方はこれと少し違い、他の条件で刷ると品質が落ちたり早期に壊れたり動作不良を起こす、という機構である。

読み出し手段については裏が取れた。2020年のAdditive Manufacturing誌の論文は公開されており、埋め込んだ符号は「微小焦点の計算機トモグラフィ（micro-CT）の走査装置またはX線透過写真」で読むと明記している。実験ではBruker社のSkyScan 1172という装置を使い、チタン合金の試料での走査分解能は1画素あたり10.08マイクロメートルであった。この論文の目的は、走査で得た像の質を上げて、市販の携帯電話のアプリでそのまま読める状態にすることである。確認先は公開版の本文 https://pmc.ncbi.nlm.nih.gov/articles/PMC8017490/ である。

CipherFluteとの関係は、「造形物の内部に秘密の符号を隠し、専用の読み出し手順を要する」という構図が既にあることを示す点である。ただし読み出しに産業用の計算機トモグラフィが必要であり、正当な利用者にとっても手軽ではない。CipherFluteの「正当な利用者は吹くだけで読める」という利点は、この系列との対比で最も鮮明になる。逆に、この系列はCipherFluteに対する攻撃手段も示している。上に挙げた1画素あたり10.08マイクロメートルという分解能は、CipherFluteが半音1段に割り当てる管長の差（おおよそ2ミリメートル台）より2桁以上細かいので、計算機トモグラフィを持つ攻撃者が笛を吹かずに内部の管長を読み取れることは、もはや予想ではなく文献で裏づけられた事実である。論文の脅威モデルには「計算機トモグラフィによる無音の読み出し」を明記したほうが誠実であり、その根拠としてこの2020年の論文を引くのがよい。

脅威の度合いは中である。着想が近く、かつCipherFluteの脅威モデルの穴を一つ埋めてくれる。

### 11. Information Embedding in Additive Manufacturing through Printing Speed Control / Information Embedding for Secure Manufacturing

- 著者: Karim A. ElSayed, Adam Dachowicz, Jitesh H. Panchal（後者は Karim A. ElSayed, Adam Dachowicz, Mikhail J. Atallah, Jitesh H. Panchal）
- 掲載: Proceedings of the 2021 Workshop on Additive Manufacturing (3D Printing) Security (AMSec@CCS 2021), 31-37ページ / 2023年の論文の正式な表題は "Information Embedding for Secure Manufacturing: Challenges and Research Opportunities" であり、Journal of Computing and Information Science in Engineering, 第23巻第6号, 論文番号060813, 2023年である
- 確認先: https://doi.org/10.1145/3462223.3485623 および https://doi.org/10.1115/1.4062600 （前者は dblp の AMSec 2021 予稿集目次 https://dblp.org/db/conf/ccs/amsec2021.html とCrossrefの双方で確認し、要旨は Semantic Scholar の登録内容で確認した。後者はCrossrefで表題・巻号・論文番号を確認した）

造形の速度という工程パラメータを変調して、造形物そのものに情報を埋め込む方式である。要旨によれば、造形速度を変えると部品の表面に微妙な局所的な高さの差が生じるので、それを符号として使う。読み出しには光学式の表面形状測定器（プロファイロメータ）を用い、造形後に取得した表面形状のデータから各領域のビットを推定する。符号化するビットの間で造形速度に毎秒53ミリメートルの差を付けた場合に、正解率80パーセントを達成したとしている。2023年の論文は、製造の安全確保のために情報を埋め込むという課題全体を整理した展望論文になっている。

CipherFluteとの関係は、「造形の物理的な自由度を情報の担体として使う」という発想が追加製造の安全研究の中に既にあることを示す点にある。CipherFluteは形状（管長）を担体にしており、こちらは速度を担体にしている。読み出しも異なり、こちらは光学式の表面形状測定器という実験室の装置を要する。正解率80パーセントという数字も、誤り訂正なしではそのまま秘密を運べる水準ではない。CipherFluteの「汎用のマイクロフォンと息だけで読める」「Reed-Solomon符号で誤りを訂正する」という2点は、この論文との対比で位置づけを述べやすい。展望論文のほうは、CipherFluteが自分をこの分野の地図上のどこに置くかを述べるのに便利である。

脅威の度合いは中である。引用して枠組みの位置関係を述べるべきである。

### 12. 造形機と造形物の指紋認識（PrinTracker / ThermoTag / SI3DP）

- Zhengxiong Li, Aditya Singh Rathore, Chen Song, Sheng Wei, Yanzhi Wang, Wenyao Xu, "PrinTracker: Fingerprinting 3D Printers using Commodity Scanners", ACM CCS 2018, 1306-1323ページ, 確認先 https://doi.org/10.1145/3243734.3243735 （Crossrefでページを確認し、Semantic Scholarで要旨も確認した。14台の造形機を使い、試料の面積・位置・工程が制限された不利な条件でも92パーセントの精度を報告している）
- Yang Gao, Wei Wang, Yincheng Jin, Chi Zhou, Wenyao Xu, Zhanpeng Jin, "ThermoTag: A Hidden ID of 3D Printers for Fingerprinting and Watermarking", IEEE Transactions on Information Forensics and Security, 第16巻, 2805-2820ページ, 2021年, 確認先 https://doi.org/10.1109/TIFS.2021.3065225 （CrossrefとOpenAlexの双方で著者6名を確認した。要旨によれば、同じ機種の押出機の先端部分だけを取り換えた45個の先端の間で約92パーセントの識別精度を達成している）
- Bo Seok Shim, Yoo Seung Shin, Seong-Wook Park, Jong-Uk Hou, "SI3DP: Source Identification Challenges and Benchmark for Consumer-Level 3D Printer Forensics", ACM Multimedia 2021, 1721-1729ページ, 確認先 https://doi.org/10.1145/3474085.3475316 （Semantic Scholarで要旨も確認した。18種類の造形設定で252個の造形物を撮影したデータセットを公開し、機体レベルの識別や再走査と再印刷の検出という5つの課題を提案している）

造形物の表面に残る微細な痕跡から、どの造形機で作られたかを特定する研究群である。PrinTrackerは市販のスキャナで読める線形成の癖を使い、ThermoTagは押出機の熱的な癖（予熱時の温度の上がり方）を使い、SI3DPはこの問題を法科学のベンチマークとして定式化している。CipherFluteが既に引用しているG-ID（CHI 2020）は同じ棚の隣にある。

CipherFluteとの関係は二つある。第一に、CipherFluteは「複製も容易」と述べて物理層の秘匿を放棄しているが、この研究群は「複製はできても、どの機体で作られたかは残る」と述べている。攻撃者が笛を複製した場合、複製物が攻撃者の造形機に紐づく痕跡を残す可能性がある。これは論文にとって有利な材料であり、脅威モデルの記述に厚みを与える。第二に、逆向きに、正当な利用者が作った笛も出所を特定されるので、匿名性は無いと書くべきである。

脅威の度合いは中である。新規性は脅かさないが、脅威モデルの記述を精密にするために引用が必要である。

### 13. Never Trust the Manufacturer, Never Trust the Client: A Novel Method for Streaming STL Files for Secure Additive Manufacturing

- 著者: Seyed Ali Ghazi Asgar, Narasimha Reddy, Satish T. S. Bukkapatnam
- 掲載: arXiv:2507.06421, 2025年7月8日投稿, 同年7月11日改訂（査読の有無は確認できていない）
- 確認先: https://arxiv.org/abs/2507.06421 （arXivの論文ページを取得し、表題・著者・投稿日・分野・要旨を確認した）

製造受託の場面で、設計者は設計データを渡すと知的財産を盗まれ、受託側は渡された制御コードを実行すると自分の機械を壊されるという、双方向の不信の問題を扱っている。解決として、設計ファイルを分割して逐次的に送り、受託側では実時間でSTLから制御コードへ変換する仕組みを置く。これによって設計側の知的財産と受託側の工程の知的財産の双方を守るとしている。

CipherFluteとの関係は、「家庭で作れるので製造者を信頼しなくてよい」という利点の主張に対する、最も近い先行研究である。この論文は外部の製造者が必ず居る前提で問題を解いているので、CipherFluteの「自分で刷るのでその問題自体が消える」という主張は、この論文の存在によってむしろ意味を持つ。引用して「受託製造では複雑な仕組みが必要になる問題を、家庭で刷ることで回避している」と述べれば、家庭製造の利点を先行研究に基づいて論じられる。

脅威の度合いは中である。新規性は脅かさず、むしろ論拠として使えるが、主張を裏づけるためには引用が必要である。なお表題の「製造者を信頼するな」という言い回しは、CipherFluteの主張と正面から響き合う。

### 14. Myths and Misconceptions in Additive Manufacturing Security: Deficiencies of the CIA Triad

- 著者: Mark Yampolskiy, Jacob Gatlin, Moti Yung
- 掲載: Proceedings of the 2021 Workshop on Additive Manufacturing (3D Printing) Security (AMSec@CCS 2021), 3-9ページ
- 確認先: https://doi.org/10.1145/3462223.3485618 （dblp の AMSec 2021 予稿集目次 https://dblp.org/db/conf/ccs/amsec2021.html で副題まで含む表題・著者・ページ・DOIを確認し、要旨は OpenAlex の登録内容で確認した。なおCrossrefの登録では副題が落ちて主題だけになっている）

追加製造の安全を機密性・完全性・可用性の三つ組で語ることの不十分さを論じた立場表明の論文である。要旨の論旨はこうである。追加製造は「純粋なデータ」の領域ではなく、ソフトウェア・データファイル・そしてデータを物理的な人工物に変換する工程を含む領域である。したがって、他分野で確立した機密性・完全性・可用性の三つ組をそのまま持ち込むと、誤った方向へ導き、ときには逆効果になる。この分野で既に確立している具体的な脅威の分類、すなわち技術データの窃取、破壊行為（サボタージュ）、違法な部品製造の3つを、三つ組で置き換えることはできない、と述べている。

CipherFluteとの関係は、脅威モデルの記述の作法に直結する。CipherFluteは「音や物体の層には暗号学的な秘匿の力はまったく無い」と宣言して機密性を放棄し、秘匿を秘密分散に委ねている。これは三つ組の素朴な適用を避ける態度であり、この論文を引いて自分の立場を位置づけると、脅威モデルの節が理論的な支えを得る。

脅威の度合いは中である。この分野の脅威モデル論の代表的な文献であり、引用しないと脅威モデルの節が孤立して見える。

### 15. 造形データの改竄による破壊攻撃（dr0wned / Sturm らの .STL 攻撃）

- Sofia Belikovetsky, Mark Yampolskiy, Jinghui Toh, Jacob Gatlin, Yuval Elovici, "dr0wned - Cyber-Physical Attack with Additive Manufacturing", 11th USENIX Workshop on Offensive Technologies (WOOT) 2017, 確認先 https://www.usenix.org/conference/woot17/workshop-program/presentation/belikovetsky （USENIXの発表ページで著者5名と所属、要旨を確認した。プレプリントは http://arxiv.org/abs/1609.00133 であるが、こちらは著者4名でJacob Gatlinを含まないので、引用するときは会議版の著者を使うべきである）
- Logan D. Sturm, Christopher B. Williams, Jamie A. Camelio, Jules White, Robert Parker, "Cyber-physical vulnerabilities in additive manufacturing systems: A case study attack on the .STL file with human subjects", Journal of Manufacturing Systems, 第44巻, 154-164ページ, 2017年, 確認先 https://doi.org/10.1016/j.jmsy.2017.05.007 （Crossrefで表題・著者5名・巻ページを確認した。要旨は取得できていない）

前者は、造形データを密かに書き換えて無人航空機のプロペラの疲労寿命を縮め、飛行中に破壊するまでを通しで実演した研究である。要旨は「疲労の加速」を新しい種類の破壊攻撃として位置づけている。後者は、STLファイルに空洞を挿入して部品の強度を落とす攻撃を、人間の被験者が見つけられるかどうかまで含めて評価した研究である。いずれも「造形データに手を入れられると、外見では分からない欠陥を仕込める」ことを示している。

CipherFluteとの関係は、完全性への脅威として直接効く。攻撃者が造形データに手を入れられるなら、笛の管長をわずかに変えて秘密の一部を書き換えられる。しかも外見はほとんど変わらないので、利用者は気付かない。CipherFluteがReed-Solomon符号を持っていることは検出には役立つが、攻撃者が符号ごと整合的に書き換えれば通ってしまう。論文の脅威モデルに「造形データの完全性が破られた場合、秘密は静かに破壊されうる」と一行入れるべきであり、その根拠としてこの二つを引くのがよい。

脅威の度合いは中である。新規性ではなく脅威モデルの網羅性に効く。

### 16. Identifying 3D printer residual data via open-source documentation

- 著者: Daniel Bradford Miller, William Bradley Glisson, Mark Yampolskiy, Kim-Kwang Raymond Choo
- 掲載: Computers & Security, 第75巻, 10-23ページ, 2018年
- 確認先: https://doi.org/10.1016/j.cose.2018.01.011 （Crossrefの登録内容を取得して、表題・著者・巻号ページ・出版社を確認した。要旨は取得できていない）

造形機の内部に造形後も残るデータを、公開文書を手がかりに法科学的に特定する研究である。参考文献84件を持つ、この主題の基礎的な調査でもある。

CipherFluteとの関係は、運用上の推奨の抜けを埋める点にある。切り離した環境で刷っても、造形機のストレージや記録媒体に造形データが残るので、その機体を他人に渡したり修理に出したりすれば秘密が漏れる。CipherFluteは「印刷後に造形データと造形機内の残留データを消去する」ことまで推奨に含めるべきであり、その根拠としてこの論文が使える。

脅威の度合いは中である。運用上の推奨の記述を具体化するために必要である。

### 17. 物理的な鍵や印章の複製という系統

- Benjamin Laxton, Kai Wang, Stefan Savage, "Reconsidering physical key secrecy: teleduplication via optical decoding", ACM CCS 2008, 469-478ページ, 確認先 https://doi.org/10.1145/1455770.1455830 （Crossrefでページを確認した。Crossrefの登録では表題が副題を落として "Reconsidering physical key secrecy" だけになっている）
- Soundarya Ramesh, Harini Ramprasad, Jun Han, "Listen to Your Key: Towards Acoustics-based Physical Key Inference", ACM HotMobile 2020（正式な予稿集名は Proceedings of the 21st International Workshop on Mobile Computing Systems and Applications である）, 3-8ページ, 確認先 https://doi.org/10.1145/3376897.3377853 （Crossrefでページを確認し、要旨は Semantic Scholar の登録内容で確認した）
- 木村悠生, 山元陽佑雅, 榎竜盛, 上原哲太郎「3Dプリンタによる印影からの印章の偽造」マルチメディア，分散，協調とモバイルシンポジウム2023論文集, 1269-1276ページ, 情報処理学会, 2023年6月28日, 確認先 https://cir.nii.ac.jp/crid/1050860532220398464 （CiNii Researchの書誌で著者4名・予稿集名・ページ・発行日を確認した。本文は https://ipsj.ixsq.nii.ac.jp/records/228209 にある）

一つ目は、離れた場所から撮った写真だけで鍵の刻みを読み取り、複製できることを示した論文である。二つ目は、鍵を鍵穴に差し込むときの音から鍵の形状を推定する研究であり、著者らはこの攻撃をSpiKeyと呼んでいる。ここは数値まで確かめておく。要旨によれば、鍵が鍵穴に入るときに聞こえる「かちり」という音の時間差から刻みの深さを推定し、33万本を超える鍵の候補集合を、最も多い場合について3本まで絞り込めるとしている。ただし要旨は、これが実際の録音に基づく計算機上の模擬実験（概念実証）であると明記しているので、実機で鍵を作るところまで通した研究として引くと言い過ぎになる。三つ目は、押された印影から3次元造形機で印章を偽造し、真贋の判定実験まで行った日本語の研究である。安価な造形機の普及によって印章の偽造が容易になったことを問題として立てている。

CipherFluteとの関係は、「形状が秘密である物体は、形状を観測されれば秘密を失う」という原理を、この分野の外の文献で裏づける点にある。CipherFluteは「形状を計測されれば無音で読める、複製も容易」と自ら宣言しているので、その宣言の学術的な根拠としてLaxtonらを引くのが最も適切である。Rameshらは「音から形状を推定する」という点で、CipherFluteの読み出し方式の裏返しになっており、対比として面白い。木村らは、日本語の読者に対して3次元造形機による複製の容易さを示す身近な例になる。

脅威の度合いは中である。CipherFluteの脅威モデルの記述が既知の原理に沿っていることを示すために引用すべきである。

### 18. Secure 3D Printing: Reconstructing and Validating Solid Geometries using Toolpath Reverse Engineering

- 著者: Nektarios Georgios Tsoutsos, Homer Gamil, Michail Maniatakos
- 掲載: 3rd ACM Workshop on Cyber-Physical System Security (CPSS@AsiaCCS) 2017, 15-20ページ
- 確認先: https://doi.org/10.1145/3055186.3055198 （Crossrefの登録内容で表題・著者3名・予稿集名・ページを確認した。要旨は取得できていない）

造形機に与えられる工具経路から立体形状を逆に組み立て、意図した形状と一致するかを検証する研究である。防御側の道具として提案されているが、同じ技術は工具経路を手に入れた攻撃者の道具にもなる。

CipherFluteとの関係は、工具経路が形状と等価な情報であることを明示する点にある。「印刷データに秘密がそのまま載る」という論文の記述の技術的な内実を、この論文で裏づけられる。

脅威の度合いは中である。

### 19. See No Evil, Hear No Evil, Feel No Evil, Print No Evil? Malicious Fill Patterns Detection in Additive Manufacturing

- 著者: Christian Bayens, Tuan Le, Luis Garcia, Raheem Beyah, Mehdi Javanmard, Saman Zonouz
- 掲載: 26th USENIX Security Symposium 2017, 1181-1198ページ
- 確認先: https://www.usenix.org/conference/usenixsecurity17/technical-sessions/presentation/bayens （USENIXの発表ページの本文を取得して、表題・著者6名と所属・要旨を確認した。ページはdblpの書誌で確認した。前の調査者はこのページの自動取得が拒否されたと書いていたが、利用者エージェントを通常の閲覧器のものにすれば取得できる）

造形中の音響と空間的な計測、および造形後の材料分析を組み合わせて、造形データに仕込まれた悪意ある充填パターンを検出する防御側の研究である。要旨によれば、検証と侵入検知の仕組みを造形機のファームウェアと制御用の計算機から独立させた点が特徴であり、製造工程の音響的な特徴の解析、機械の各部の実時間追跡、造形後の材料分析の3つを組み合わせている。3種類の造形機と1台の数値制御工作機械で評価し、誤った造形物の実時間検出において100パーセントの正解率を得たとしている。人工膝関節の脛骨側の部品が誤って造形された事例を検出する応用例も示している。

CipherFluteとの関係は、音響を防御側の道具として使える可能性を示す点にある。CipherFluteの利用者は、笛が意図した設計どおりに造形されたかを、造形中の音から検証できるかもしれない。前項の完全性への脅威に対する現実的な対策の芽である。ただしこの論文が検出しているのは充填パターンの改変という比較的粗い欠陥であり、半音1段に相当する管長のわずかな差を検出できるかどうかは、この論文からは言えない。

脅威の度合いは中である。対策の議論を書くなら引用すべきである。

### 20. Security Implications of Malicious G-Codes in 3D Printing

- 著者: Jost Rossel, Vladislav Mladenov, Nico Wördenweber, Juraj Somorovsky
- 掲載: 34th USENIX Security Symposium 2025, 1867-1885ページ
- 確認先: https://www.usenix.org/conference/usenixsecurity25/presentation/rossel （USENIXの発表ページの本文を取得して、表題・著者4名と所属・要旨・書誌情報の記載を確認した。ページはdblpの書誌で確認した。前の調査者はこのページが取得できず内容を表題からしか判断していないと書いていたが、利用者エージェントを通常の閲覧器のものにすれば取得できたので、以下の記述は要旨に基づいて書き直した。なお発表の区分は短時間発表である）

造形機に与える制御コードが持つ攻撃面を体系的に扱った、この主題では最も新しいトップ会議の論文である。要旨によれば、先行研究が強力な攻撃者を前提として造形物そのものの改変に注目していたのに対し、この論文はより弱い攻撃者を想定した攻撃と攻撃者モデルを導入している。結論として、造形機へのごくわずかな接触権限しかない攻撃者でも、その後に投入される造形ジョブへの不正な読み取りや、造形機の設定を永続的に狂わせることといった重大な侵害を起こせるとしている。情報漏洩、サービス妨害、モデル改変という3つの分類にわたって、悪用しうる制御コードを278件特定している。

CipherFluteとの関係は2つある。第一に、造形の入力データを信頼できない経路で受け取ることの危険を、最新の査読論文で裏づける点である。第二に、こちらのほうが重要である。要旨が明言している「その後に投入される造形ジョブへの不正な読み取り」は、CipherFluteの秘密に直接効く。攻撃者が笛を刷る前に一度だけ造形機に触れれば、後から刷られる笛の設計を読み出せることになる。造形機を他人と共用している場合、あるいは造形機を中古で入手した場合に、この経路が開く。CipherFluteの運用上の推奨は「切り離す」だけでは足りず、「造形機の設定とファームウェアが汚染されていないことを確かめる」「他人と共用している造形機で秘密を刷らない」まで含めるべきであり、その根拠としてこの論文を引くのが最も強い。

脅威の度合いは中である。新規性は脅かさないが、運用上の推奨の記述を具体的に書き換えることを要求する。

### 21. 側チャネルからの漏洩を設計側で減らす防御の系統

- Sujit Rokka Chhetri, Sina Faezi, Mohammad Abdullah Al Faruque, "Fix the Leak! An Information Leakage Aware Secured Cyber-Physical Manufacturing System", Design, Automation and Test in Europe (DATE) 2017, 1408-1413ページ, 確認先 https://doi.org/10.23919/DATE.2017.7927213
- Sujit Rokka Chhetri, Sina Faezi, Mohammad Abdullah Al Faruque, "Information Leakage-Aware Computer-Aided Cyber-Physical Manufacturing", IEEE Transactions on Information Forensics and Security, 第13巻, 2333-2344ページ, 2018年, 確認先 https://doi.org/10.1109/TIFS.2018.2818659
- Seyed Ali Ghazi Asgar, Narasimha Reddy, "QuietPrint: Protecting 3D Printers Against Acoustic Side-Channel Attacks", Proceedings of the 12th ACM Cyber-Physical System Security Workshop (CPSS@AsiaCCS) 2026, 25-34ページ, 確認先 https://doi.org/10.1145/3775042.3807880 （Crossrefの登録内容で表題・著者2名・予稿集名・ページ・年を確認した。プレプリントは https://arxiv.org/abs/2602.02198 であり、arXivのAPIで同じDOIが登録されていることと要旨を確認した。要旨によれば大型のスピーカや騒音打ち消し装置といった追加の機材を必要とせず、制御コードに最小限の変更を加えることで防御する）

工具経路や工程の設計を変えることで、側チャネルから漏れる情報量を減らす防御の系統である。QuietPrintは制御コードだけをいじって音響側チャネルを防ぐと述べている。

CipherFluteとの関係は、対策として実際に採れる手段を提供する点にある。CipherFluteは笛を複数本まとめて造形するので、造形の順序を無作為化する、無駄な移動を混ぜる、複数の笛の造形を交互に進めるといった対策を制御コードの生成側で実装できる。実装はすでに交互配置（インターリーブ）を持っているので、それを安全上の対策としても位置づけ直せる。

脅威の度合いは中である。対策の節を書くなら引用が必要である。

## 背景として押さえるべき文献

以下はいずれも書誌情報を一次資料または権威ある登録機関で確認したものであり、背景として引く程度の位置づけである。

- Avesta Hojjati ほか8名, "Leave Your Phone at the Door: Side Channels that Reveal Factory Floor Secrets", ACM CCS 2016, 883-894ページ, 確認先 https://doi.org/10.1145/2976749.2978323 （Crossrefで著者9名とページを確認した）。工場の床で携帯電話のセンサから製造の秘密が漏れることを示した論文であり、造形機に限らない一般化として引ける。
- Michael Backes, Markus Dürmuth, Sebastian Gerling, Manfred Pinkal, Caroline Sporleder, "Acoustic Side-Channel Attacks on Printers", USENIX Security Symposium 2010, 307-322ページ, 確認先 http://www.usenix.org/events/sec10/tech/full_papers/Backes.pdf （PDFが実際に取得できることを確認し、ページはdblpの書誌で確認した）。紙の印刷機の音から印字内容を復元した古典であり、音響側チャネルの系譜の起点として引ける。
- Sujit Rokka Chhetri, Arquimedes Canedo, Mohammad Abdullah Al Faruque, "KCAD: Kinetic Cyber-Attack Detection Method for Cyber-Physical Additive Manufacturing Systems", ICCAD 2016, 全8ページ, 確認先 https://doi.org/10.1145/2966986.2967050 （Crossrefの登録では表題が副題を落として "KCAD" だけになっている）。
- Sujit Rokka Chhetri, Sina Faezi, Arquimedes Canedo, Mohammad Abdullah Al Faruque, "Poster Abstract: Thermal Side-Channel Forensics in Additive Manufacturing Systems", ICCPS 2016, 全1ページ, 確認先 https://doi.org/10.1109/ICCPS.2016.7479115 。Crossrefの登録内容を確認したところ、これは表題の頭に "Poster Abstract" が付く1ページのポスター概要であった。前の調査者は通常の論文のように書いていたので改めた。1ページの概要なので、これを本格的な研究として引くのは避けたほうがよい。
- Sujit Rokka Chhetri, Mohammad Abdullah Al Faruque, "Side Channels of Cyber-Physical Systems: Case Study in Additive Manufacturing", IEEE Design & Test, 第34巻第4号, 18-25ページ, 2017年, 確認先 https://doi.org/10.1109/MDAT.2017.2682225 。
- Shih-Yuan Yu, Arnav Vaibhav Malawade, Sujit Rokka Chhetri, Mohammad Abdullah Al Faruque, "Sabotage Attack Detection for Additive Manufacturing Systems", IEEE Access, 第8巻, 27218-27231ページ, 2020年, 確認先 https://doi.org/10.1109/ACCESS.2020.2971947 。
- Nathan Costa, Shih-Yuan Yu, Arnav Malawade, Sujit Chhetri, Mohammad Al Faruque, "SideChannel-3D: Acoustic, Vibration, Magnetic, and Power Side-Channel 3D Printer Dataset", IEEE DataPort, 2021年, 確認先 https://doi.org/10.21227/j6cw-y314 、および掲載ページ https://ieee-dataport.org/documents/sidechannel-3d-acoustic-vibration-magnetic-and-power-side-channel-3d-printer-dataset 。公開データセットであり、CipherFluteの笛が読み取られるかを自分で検証したい場合の出発点になる。なおこのDOIはCrossrefではなくDataCiteに登録されているので、Crossrefで問い合わせると見つからない。DataCiteの登録内容と掲載ページの双方で表題・作成者5名・年を確認した。前の調査者が書いていた「Nathan D. Costa」という中黒付きの表記は一次資料では確認できなかったので、掲載ページの表記に合わせた。
- Sina Faezi ほか6名, "Oligo-Snoop: A Non-Invasive Side Channel Attack Against DNA Synthesis Machines", NDSS 2019, 確認先 https://www.ndss-symposium.org/ndss-paper/oligo-snoop-a-non-invasive-side-channel-attack-against-dna-synthesis-machines/ （発表ページの本文を取得して、著者7名と所属を確認した。共著者は Sujit Rokka Chhetri, Arnav Vaibhav Malawade, John Charles Chaput, William Grover, Philip Brisk, Mohammad Abdullah Al Faruque である）。音響側チャネルが造形機に限らない一般的な脅威であることを示す例である。
- Mark Yampolskiy, Wayne E. King, Jacob Gatlin, Sofia Belikovetsky, Adam Brown, Anthony Skjellum, Yuval Elovici, "Security of additive manufacturing: Attack taxonomy and survey", Additive Manufacturing, 第21巻, 431-457ページ, 2018年, 確認先 https://doi.org/10.1016/j.addma.2018.03.015 。この分野の標準的な調査論文である。
- Priyanka Mahesh ほか7名, "A Survey of Cybersecurity of Digital Manufacturing", Proceedings of the IEEE, 第109巻, 495-516ページ, 2021年, 確認先 https://doi.org/10.1109/JPROC.2020.3032074 。
- Steven Eric Zeltmann, Nikhil Gupta, Nektarios Georgios Tsoutsos, Michail Maniatakos, Jeyavijayan Rajendran, Ramesh Karri, "Manufacturing and Security Challenges in 3D Printing", JOM, 第68巻第7号, 1872-1881ページ, 2016年, 確認先 https://doi.org/10.1007/s11837-016-1937-7 。
- Samuel Bennett Moore, William Bradley Glisson, Mark Yampolskiy, "Implications of Malicious 3D Printer Firmware", Hawaii International Conference on System Sciences (HICSS) 2017, 確認先 https://hdl.handle.net/10125/41899 （ハワイ大学の機関リポジトリの本文ページを取得して、表題・著者3名・2017年1月4日という日付・要旨を確認した。Printrbot社が公開しているMarlinファームウェアの分岐に悪意ある処理を実装した研究である）。
- Mark Yampolskiy, Anthony Skjellum, Michael Kretzschmar, Ruel A. Overfelt, Kenneth R. Sloan, Alec Yasinsac, "Using 3D printers as weapons", International Journal of Critical Infrastructure Protection, 第14巻, 58-71ページ, 2016年, 確認先 https://doi.org/10.1016/j.ijcip.2015.12.004 。造形機そのものを凶器として使う脅威を扱う。
- Gerald Walther, "Printing Insecurity? The Security Implications of 3D-Printing of Weapons", Science and Engineering Ethics, 第21巻第6号, 1435-1445ページ, 2015年（オンライン公開は2014年）, 確認先 https://doi.org/10.1007/s11948-014-9617-x 。3次元造形による武器製造の安全上の含意を倫理の観点から論じる。
- 茂出木敏雄「違法造形物の3Dプリンタによる製造を規制するための3Dデータ照合技術に関する研究」尚美学園大学芸術情報研究, 第25巻, 101-120ページ, 2016年3月31日, 確認先 https://cir.nii.ac.jp/crid/1050282677910856960 （本文は https://shobi-u.repo.nii.ac.jp/records/464 ）、および同「違法造形物の3Dプリンタによる製造を規制するための3Dデータ照合技術の高精度化」同誌 第28巻, 1-19ページ, 2018年3月31日, 確認先 https://cir.nii.ac.jp/crid/1050282677911423360 （本文は https://shobi-u.repo.nii.ac.jp/records/622 ）。いずれもCiNii Researchの書誌で著者・誌名・巻・ページ・発行日を確認した。ポリゴンデータを特徴ベクトルに変換して禁止一覧と照合し、危険物や違法物の造形を止める方式である。造形の入口で内容を検査するという発想は、CipherFluteのように意味のある情報を形状に載せる手法にとって将来の障害になりうる。
- 伊藤優樹, 四方隼人, 水木敬明, 菅沼拓夫「3Dプリンタによるオープン装置や特殊カードケースの作成と対称関数の秘密計算への適用」コンピュータセキュリティシンポジウム2023論文集, 192-199ページ, 情報処理学会, 2023年10月23日, 確認先 https://cir.nii.ac.jp/crid/1050579444484578048 （本文は https://ipsj.ixsq.nii.ac.jp/records/228640 にある。CiNii Researchの書誌で著者4名・予稿集名・ページ・発行日を確認した）。カードベース暗号の物理的な道具を3次元造形機で作る研究であり、「造形物を暗号のための物理装置として使う」日本国内の別の系統である。
- 加藤大弥, 林達也, 砂原秀樹「サイバーフィジカル時代の物理媒体による認証・識別に関する考察」コンピュータセキュリティシンポジウム2017論文集, 2017年第2号, 2017年10月16日, 確認先 https://cir.nii.ac.jp/crid/1050011097170108928 （本文は https://ipsj.ixsq.nii.ac.jp/records/187256 にある）。CiNii Researchの書誌では巻が2017、号が2であり、前の調査者が書いていた「第2巻第2号」は誤りなので改めた。ページ番号はCiNiiに登録されていない。
- Ryutarou Ohbuchi, Hiroshi Masuda, Masaki Aono, "Watermarking three-dimensional polygonal models", 5th ACM International Conference on Multimedia 1997, 261-272ページ, 確認先 https://doi.org/10.1145/266180.266377 （Crossrefの登録では表題の一部が "Watermaking" と誤記されていることを、こちらでも取得して確かめた）、および同著者による "Watermarking three-dimensional polygonal models through geometric and topological modifications", IEEE Journal on Selected Areas in Communications, 第16巻, 551-560ページ, 1998年, 確認先 https://doi.org/10.1109/49.668977 。3次元モデルへの電子透かしの古典である。
- Jong-Uk Hou, Do-Gon Kim, Heung-Kyu Lee, "Blind 3D Mesh Watermarking for 3D Printed Model by Analyzing Layering Artifact", IEEE Transactions on Information Forensics and Security, 第12巻第11号, 2712-2725ページ, 2017年, 確認先 https://doi.org/10.1109/TIFS.2017.2718482 。造形時の積層痕を解析して、造形後の物体から透かしを読む。
- Arnaud Delmotte, Kenichiro Tanaka, Hiroyuki Kubo, Takuya Funatomi, Yasuhiro Mukaigawa, "Blind 3D-Printing Watermarking Using Moment Alignment and Surface Norm Distribution", IEEE Transactions on Multimedia, 第23巻, 3467-3482ページ, 2021年, 確認先 https://doi.org/10.1109/TMM.2020.3025660 。あわせて Arnaud Delmotte, "Blind watermarking for 3D printed objects by applying small geometric modification on the surface", 奈良先端科学技術大学院大学 博士論文 甲第1675号, 2020年3月31日, 確認先 https://cir.nii.ac.jp/crid/1910583860655800832 （本文は https://naist.repo.nii.ac.jp/records/10918 ）。日本国内の造形物向け透かしの学位論文である。
- Benoît Macq, Patrice Rondao-Alface, Mireia Montañola Sales, "Applicability of watermarking for intellectual property rights protection in a 3D printing scenario", 20th International Conference on 3D Web Technology (Web3D) 2015, 89-95ページ, 確認先 https://doi.org/10.1145/2775292.2775313 （Crossrefの登録は第3著者を "Mireia Montanola" と短く書いているが、dblpの書誌では "Mireia Montañola Sales" なので、前の調査者の表記のままで正しい）。
- Zhenyu Li, Daofu Gong, Lei Tan, Xiangyang Luo, Fenlin Liu, Adrian G. Bors, "Self-embedding watermarking method for G-code used in 3D printing", IEEE International Workshop on Information Forensics and Security (WIFS) 2021, 確認先 https://doi.org/10.1109/WIFS53200.2021.9648386 。造形の制御コードそのものに透かしを埋める。
- Giao N. Pham, Suk-Hwan Lee, Oh-Heum Kwon, Ki-Ryong Kwon, "A Watermarking Method for 3D Printing Based on Menger Curvature and K-Mean Clustering", Symmetry, 第10巻第4号, 97, 2018年, 確認先 https://doi.org/10.3390/sym10040097 。第一著者の表記について、前の調査者は「Pham Ngoc Giao」と書いていたが、Crossrefの登録は "Giao N. Pham" なので出版社の表記に合わせた。
- James Griffin ほか5名, "Artificial Intelligence and Digital Watermarking will Transform Copyright Arbitration and Dispute Resolution for 3D Printing: An Empirical Analysis", European Journal of Law and Technology, 第14巻第2号, 2023年, 確認先 https://ejlt.org/index.php/ejlt/article/view/970 （雑誌の論文ページを取得して、表題・著者6名・巻号・査読区分を確認した。共著者は Kyriaki Noussia, Stanislava Nedeva, Stavros Zervoudakis, Jonathan Lux, John McNamara である）。法律の側から3次元造形と透かしを論じる。第一著者の表記について、前の調査者は「James G. H. Griffin」と書いていたが、雑誌のページの表記は「James Griffin」なのでそちらに合わせた。
- Ahmet Turan Erozan, Michael Hefenbrock, Dennis R. E. Gnad, Michael Beigl, Jasmin Aghassi-Hagmann, Mehdi B. Tahoori, "Counterfeit Detection and Prevention in Additive Manufacturing Based on Unique Identification of Optical Fingerprints of Printed Structures", IEEE Access, 第10巻, 105910-105919ページ, 2022年, 確認先 https://doi.org/10.1109/ACCESS.2022.3209241 。
- Akash Tiwari, Eduardo Jose Villasenor, Nikhil Gupta, A. L. Narasimha Reddy, Ramesh Karri, Satish T. S. Bukkapatnam, "Protection against Counterfeiting Attacks in 3D Printing by Streaming Signature-embedded Manufacturing Process Instructions", AMSec@CCS 2021, 11-21ページ, 確認先 https://doi.org/10.1145/3462223.3485620 。
- Felix Engelmann, Jan Philip Speichert, Ralf God, Frank Kargl, Christoph Bösch, "Confidential Token-Based License Management", AMSec@CCS 2021, 39-48ページ, 確認先 https://doi.org/10.1145/3462223.3485619 。
- Theo Zinner, Grant Parker, Nima Shamsaei, Wayne E. King, Mark Yampolskiy, "Spooky Manufacturing: Probabilistic Sabotage Attack in Metal AM using Shielding Gas Flow Control", AMSec@CCS 2022, 15-24ページ, 確認先 https://doi.org/10.1145/3560833.3563565 。
- Adam Dachowicz, Siva Chaitanya Chaduvula, Mikhail Atallah, Jitesh H. Panchal, "Microstructure-Based Counterfeit Detection in Metal Part Manufacturing", JOM, 第69巻, 2390-2396ページ, 2017年, 確認先 https://doi.org/10.1007/s11837-017-2502-8 。
- Siva Chaitanya Chaduvula, Adam Dachowicz, Mikhail J. Atallah, Jitesh H. Panchal, "Security in Cyber-Enabled Design and Manufacturing: A Survey", Journal of Computing and Information Science in Engineering, 第18巻第4号, 論文番号040802, 2018年, 確認先 https://doi.org/10.1115/1.4040341 。
- Mordechai Guri らによる空隙越え covert channel の一連の研究。代表として Mordechai Guri, Yosef A. Solewicz, Yuval Elovici, "Fansmitter: Acoustic data exfiltration from air-Gapped computers via fans noise", Computers & Security, 第91巻, 101721, 2020年, 確認先 https://doi.org/10.1016/j.cose.2020.101721 、Mordechai Guri, Boris Zadov, Dima Bykhovsky, Yuval Elovici, "PowerHammer: Exfiltrating Data From Air-Gapped Computers Through Power Lines", IEEE Transactions on Information Forensics and Security, 第15巻, 1879-1890ページ, 2020年, 確認先 https://doi.org/10.1109/TIFS.2019.2952257 、Mordechai Guri ほか5名, "GSMem: Data Exfiltration from Air-Gapped Computers over GSM Frequencies", USENIX Security Symposium 2015, 849-864ページ, 確認先 https://www.usenix.org/conference/usenixsecurity15/technical-sessions/presentation/guri 。ネットワークから切り離すことが万能ではないという一般命題の裏づけとして引ける。
- Lin Zhang, Longfei Zhou, Luo Xiao, "Security and Privacy in Cloud 3D Printing", Customized Production Through 3D Printing in Cloud Manufacturing, 157-179ページ, 2023年, 確認先 https://doi.org/10.1016/B978-0-12-823501-0.00013-4 。クラウド経由の造形における安全とプライバシーを整理した章であり、クラウドスライサを避けるという推奨の根拠になる。
- Milan Šorf, Petr Švenda, Łukasz Chmielewski, "Large-Scale Security Analysis of Hardware Wallets", International Conference on Availability, Reliability and Security (ARES) 2025, Lecture Notes in Computer Science 第15995巻, 360-377ページ, 確認先 https://doi.org/10.1007/978-3-032-00633-2_21 （出版社の論文ページを取得して、ARES 2025の会議論文であること、叢書の巻、ページ、電子版の公開日である2025年8月9日を確認した）。電子的なハードウェアウォレットの安全性評価であり、CipherFluteが「電源も電子部品も持たない」ことの利点を語る際の対比になる。著者名の綴りについて、前の調査者は発音符号を落として書いていたので、出版社の表記に合わせて補った。
- Tyler Cultice, Joseph Clark, Wu Yang, Himanshu Thapliyal, "A Novel Hierarchical Security Solution for Controller-Area-Network-Based 3D Printing in a Post-Quantum World", Sensors, 第23巻第24号, 9886, 2023年, 確認先 https://doi.org/10.3390/s23249886 。
- Nawfal F. Fadhel, Richard M. Crowder, Fatimah Y. Akeel, Gary B. Wills, "Component for 3D Printing Provenance Framework: Security Properties Components for Provenance Framework", WorldCIS 2014, 91-96ページ, 確認先 https://doi.org/10.1109/WorldCIS.2014.7028174 。
- Mahender Kumar, Gregory Epiphaniou, Carsten Maple, "Security of cyber-physical Additive Manufacturing supply chain: Survey, attack taxonomy and solutions", Computers & Security, 第157巻, 104557, 2025年, 確認先 https://doi.org/10.1016/j.cose.2025.104557 。最新の調査論文である。
- Michael R. Durling ほか7名, "Model-Based Security Analysis in Additive Manufacturing Systems", AMSec@CCS 2022, 3-13ページ, 確認先 https://doi.org/10.1145/3560833.3563566 、および Nils Ole Tippenhauer, "Déjà Vu? Challenges and Opportunities for AM Security from an ICS perspective", AMSec@CCS 2022, 1ページ, 確認先 https://doi.org/10.1145/3560833.3563556 。いずれもAMSec 2022の予稿集目次 https://dblp.org/db/conf/ccs/amsec2022.html で確認した。

## 未検証のまま残ったもの

以下は、実在と書誌情報は確認できたが内容（要旨や本文）を一次資料から読めなかったもの、あるいは実在自体を確認しきれなかったものである。2026年7月30日の検証で解消したものは、この節から本文へ移した。何が解消したかは末尾の「検証の記録」に書いた。

1. Sujit Rokka Chhetri ほか2名の学会発表版、すなわち Mohammad Abdullah Al Faruque, Sujit Rokka Chhetri, Arquimedes Canedo, Jiang Wan, "Acoustic Side-Channel Attacks on Additive Manufacturing Systems", ICCPS 2016 について、IEEE Xploreの本文ページから要旨を取得できていない。本文の第1項で挙げた86パーセントと11.11パーセントという数値は、Crossrefに登録された雑誌版（ACM Transactions on Cyber-Physical Systems 2018年）の要旨の本文で確かに確認できたので、雑誌版の数値としては裏が取れている。しかし2016年の会議版が同じ数値を報告しているかどうかは確認できていない。引用の際は雑誌版を主に引くのが安全である。
2. Fei Chen, Gary Mac, Nikhil Gupta, "Security features embedded in computer aided design (CAD) solid models for additive manufacturing", Materials & Design 2017年について、要旨を一次資料から読めていない。ScienceDirectの本文ページは自動取得を拒否し、CrossrefとOpenAlexのいずれにも要旨が登録されていない。ただし同じ研究群の2018年・2019年・2020年の論文の要旨は取得できており、そのうち2020年の論文が読み出し手段を微小焦点の計算機トモグラフィまたはX線透過写真と明記しているので、系統全体の読み出し手段については裏が取れている。
3. Logan D. Sturm ほか4名の Journal of Manufacturing Systems 2017年の論文について、書誌情報はCrossrefで確認したが、要旨を取得できていない。「STLファイルに空洞を挿入して部品の強度を落とす攻撃を人間の被験者が見つけられるかを評価した」という記述は表題（副題に "A case study attack on the .STL file with human subjects" と書かれている）から述べたものであり、実験の具体的な結果は確認していない。
4. Nektarios Georgios Tsoutsos ほか2名の CPSS@AsiaCCS 2017 の論文について、書誌情報はCrossrefで確認したが、要旨を取得できていない。本文の第18項の内容は表題から述べた範囲にとどまる。
5. 3次元造形機で作った「バンプキー」を使った錠の解錠に関する発表が、DEF CONやBlack Hatといった実務者向けの会議で行われたという記憶があるが、一次資料を見つけられなかったため書誌情報を書いていない。物理的な鍵の複製という論点はLaxtonらとRameshらと木村らで十分に押さえられるので、この穴は大きくないと考える。
6. 背景として挙げた文献のうち、書誌情報はCrossrefまたはDataCiteで確認したが要旨を読んでいないものがある。具体的には、KCAD（ICCAD 2016）、Chhetriらの IEEE Design & Test 2017、Yuらの IEEE Access 2020、Yampolskiyらの Additive Manufacturing 2018の調査論文、Maheshらの Proceedings of the IEEE 2021、Zeltmannらの JOM 2016、Yampolskiyらの武器に関する2016年の論文、Waltherの2015年の論文、透かしの各論文、Guriらの空隙越えの各論文、Zhangらの2023年の章、Culticeらの2023年の論文、Fadhelらの2014年の論文、Kumarらの2025年の調査論文、Durlingらと Tippenhauer の AMSec 2022 の各論文である。これらは背景として引く位置づけなので、書誌情報の正しさが確認できていれば当面は足りると判断した。ただし本文でこれらの内容に踏み込んだ主張をする場合は、要旨を人が読み直す必要がある。

## この切り口で見つからなかったこと

ここに書くことは、CipherFluteの新規性の主張の根拠として使える。いずれも「探したが見つからなかった」ことであり、「存在しない」ことの証明ではないが、この切り口で通常たどり着く範囲は網羅したと考えている。

第一に、デジタルファブリケーションの安全研究の中に、造形物に埋め込んだ情報を「人が吹いて出る音の高さ」として読み出す手法は一つも見つからなかった。この分野で使われている読み出しの経路は、可視光による撮影、サーモグラフィによる熱の観測、X線写真、計算機トモグラフィ、近赤外の蛍光、磁気センサ、光学式の表面形状測定、電波の反射に限られていた。上平員丈らの系統もGuptaらの系統もElSayedらの系統も、読み出しには何らかの計測装置を必要とする。汎用のマイクロフォンと人間の息だけで読めるものは無かった。

第二に、「物理層には暗号学的な秘匿の力がまったく無いと宣言し、秘匿の責任を秘密分散に全部移す」という設計思想を明示的に取った研究は見つからなかった。追加製造の安全研究では、機密性を守ろうとする研究（暗号化、難読化、免許管理）と、機密性の枠組み自体を批判する研究（Yampolskiyらの「Myths and Misconceptions」）の両方があるが、後者は批判にとどまり、機密性を意図的に放棄した設計を提示してはいない。CipherFluteの脅威モデルの立て方は、この分野の中では新しい。

第三に、誤り訂正符号を物理的な造形物に載せて秘密の分片を運ぶという組み合わせは、この切り口では見つからなかった。造形物に符号を載せる研究（LayerCodeやSeedmarkersなど、他の切り口で扱われるもの）はあり、誤り訂正を含むものもあるが、運ぶ中身は識別子であって秘密ではなかった。追加製造の安全研究の側では、造形物に情報を埋め込む研究（ElSayedら、Chenら）はあるが、運ぶ中身は認証符号や権利者の識別子であり、秘密分散の分片ではなかった。

第四に、「家庭で作るので製造者を信頼しなくてよい」という利点を、造形物を秘密の担体として使う文脈で正面から論じた研究は見つからなかった。最も近いAsgarらの2025年のプレプリントは、外部の製造者が必ず居る前提で相互不信の問題を解いており、家庭製造によってその問題が消えるという議論はしていない。したがってCipherFluteはこの論点を自分の言葉で述べる余地があるが、逆に言えば、その主張を支える先行研究が薄いので、Asgarらを引いて「受託製造では複雑な仕組みを要する問題を、自家製造で回避している」という形に組み直すのが説得力を持つ。

第五に、笛のような共鳴管を持つ造形物の形状が、造形機の放射（音・振動・電力・磁界）からどの精度で復元できるかを測った研究は見つからなかった。既存の側チャネル研究の評価対象は、直線と円弧からなる一般的な部品であり、「半音1段に相当する数パーセントの管長差を区別できるか」という問いは立てられていない。これはCipherFluteが将来の課題として名指しできる、明確に空いている評価である。

第六に、3次元造形物を暗号資産の鍵や復元情報の保管媒体として扱った学術研究は、この切り口では見つからなかった。金属製のシード保管製品やCasascius物理ビットコインは製品であり、ハードウェアウォレットの安全性評価（Sorfら）は電子機器を対象にしている。

第七に、日本語の文献に、3次元造形と秘密分散と音響読み出しを組み合わせたものは見つからなかった。日本国内で近いのは、上平員丈らの造形物内部への情報ハイディング、Delmotteの造形物向け透かし、伊藤優樹らのカードベース暗号のための造形装置、木村悠生らの印章偽造、茂出木敏雄の違法造形物の照合であり、いずれもCipherFluteとは目的か読み出し手段が異なる。

## 調べ残した穴

第一に、計算機トモグラフィやX線による無音の読み出しについて、前の調査者は「産業用の計算機トモグラフィの空間分解能が半音1段の管長差（おおよそ2ミリメートル台）を分離できるのはほぼ確実だと予想されるが、文献で裏づけていない」と書いていた。2026年7月30日の検証でこの穴は埋まった。Chenらの2020年のAdditive Manufacturing誌の論文（公開版の本文 https://pmc.ncbi.nlm.nih.gov/articles/PMC8017490/ ）が、Bruker社のSkyScan 1172という装置で1画素あたり10.08マイクロメートルの走査分解能を得たと明記している。2ミリメートル台の管長差より2桁以上細かいので、計算機トモグラフィを持つ攻撃者が無音で笛の管長を読めることは文献で裏づけられた。残っている課題は、その攻撃者が実際に何秒でどれだけの本数を読めるかという実務的な見積もりであり、これは論文の主張には必須ではない。

第二に、電磁波側チャネルによる造形物の復元について、単独の論文を確認していない。Chhetriらの「Tool of Spies」が4つの側チャネルの一つとして電磁波を挙げていることは確認したが、電磁波だけを扱った研究の書誌を押さえていない。

第三に、標準や指針の類（米国国立標準技術研究所の報告書、ASTM F42委員会やISO/ASTM 52920系の規格）を調べていない。「切り離した環境で印刷する」という推奨が、業界の指針の中でどう書かれているかを確認できれば、論文の記述に権威づけができる。なおGatlinらのRAID 2021の共著者にはJoshua LubellとPaul Witherellという米国国立標準技術研究所の研究者が入っているので、そこから辿るのが早い。

第四に、CHI・UIST・Symposium on Computational Fabrication・TEIといったヒューマンコンピュータインタラクションの会議を、安全とプライバシーの観点で系統的に走査していない。G-IDやStructCodeは既に論文が引用しているが、たとえば「ファブリケーションの安全に対する利用者の理解」を扱う質的研究が存在する可能性があり、CipherFluteの利用者像の議論に効くかもしれない。

第五に、Bambu Lab社の造形機のクラウド機構が造形データをどう扱うかについて、学術的な分析を一つも見つけていない。Yocamらのプレプリントが同社の機体を対象にしているが、扱っているのは騒音打ち消し機構であってクラウドではない。CipherFluteが実際に使っている機体の通信経路の話なので、査読者から問われる可能性がある論点である。

第六に、日本の法制度（銃砲刀剣類所持等取締法や印章に関する実務）の側から、3次元造形による複製をどう扱っているかを調べていない。CipherFluteの用途は武器や印章ではないので直接の関係は薄いが、「造形の入口で内容を検査する」という茂出木敏雄の系統が制度化された場合、形状に意味を載せる手法一般に影響しうる。

第七に、特許文献を一切調べていない。造形物に情報を埋め込む技術は、上平員丈らの系統をはじめとして出願がある可能性が高い。学会論文としての新規性とは別の話であるが、実用化を考えるなら確認が必要である。

## 検証の記録

2026年7月30日に、書誌情報の検証を担当する別の調査者が、このファイルに書かれた文献をすべて独立に洗い直した。前の調査者の記述を信じずに、一次情報または権威ある登録機関に当たり直す方針で作業した。

確認した件数は次のとおりである。検証前のファイルに現れるDOIは64件あり、そのすべてをCrossrefの登録内容に問い合わせて、著者名・表題・掲載誌または予稿集名・巻号・ページ・年を1件ずつ突き合わせた。63件はCrossrefに登録されており、内容も一致した。残る1件はIEEE DataPortのデータセットのDOIであり、これはCrossrefではなくDataCiteに登録されていたので、DataCiteの登録内容と掲載ページの双方で確認した。この検証で新たに補った3件のDOI（上平員丈らの金属を含ませたPLA・近赤外の蛍光染料・強磁性のセルの各論文）についても、同じくCrossrefの登録内容で書誌を確認し、さらにDOIが実際に出版社の掲載ページへ解決することを確認した。したがって現在このファイルに載っているDOIは67件であり、そのすべてが検証済みである。arXivのプレプリントは6件あり、いずれもarXivの応用プログラム接続口に問い合わせて、表題・著者・投稿日・改訂日・注記・要旨の全文を取得して確認した。2026年に投稿された2件（Yocamらの側チャネル評価と、QuietPrintの元となるプレプリント）も含めて、6件すべてが実在した。CiNii Researchの記録は8件あり、すべて機械可読な形で取得して、著者名・誌名または予稿集名・巻号・ページ・発行日を確認した。このほか、USENIXの発表ページ3件、NDSSの発表ページ1件、ハワイ大学の機関リポジトリ1件、出版社の論文ページ2件、雑誌の論文ページ1件、IEEE DataPortの掲載ページ1件、公開された本文1件を取得して内容を確認した。dblpの書誌は論文番号とページ番号の裏取りに使った。文中に現れるDOI以外のURLは27件あり、すべてに要求を出して、27件すべてが応答することを確認した。存在しない文献は1件も見つからなかった。

訂正または補足を加えた箇所は、ファイル全体で37箇所である。そのうち、前の調査者の記述が事実として誤っていたものは12件であり、残りは書誌情報の欠けを補ったものと、要旨を読んだうえで内容の記述をより正確にしたものである。事実として誤っていた12件のうち、特に重いものを5つ挙げる。第一に、造形物の内部に情報を隠す日本国内の系統について、前の調査者は中心人物を「海野浩」と書いていたが、これは誤りである。英語論文で Kazutake Uehira と表記される中心人物の日本語表記は「上平員丈」であり、「海野浩」は Hiroshi Unno という別人の共著者である。CiNii Researchの著者情報で両者が別々の著者として同じ論文に並んでいることを確認したうえで、ファイル本文の5箇所を「上平員丈」に改めた。第二に、Chhetriらの音響側チャネルの論文について、前の調査者は被引用数181件を雑誌版のものとして書いていたが、Semantic Scholarの2026年7月時点の集計では雑誌版は38件であり、181件は会議発表版のほうの数である。第三に、Jamaraniらの論文の要旨にある "a plain G-code design" を、前の調査者は「平面的な設計」と訳していたが、これは「単純な設計」の意味であり、平面という意味ではない。CipherFluteの符号の粒度と比べる議論の土台になる箇所なので訳を改めた。第四に、Yocamらのプレプリントの結論について、前の調査者は「音響は防げても振動・磁界・電力は開いたまま」と要約していたが、要旨は「振動は部分的にとどまり、このデータセットでは完全な幾何形状の復元は支えない」と明言している。この限定を落とすと原典より強い主張になるので補った。第五に、加藤大弥らのコンピュータセキュリティシンポジウム2017の論文の巻号を「第2巻第2号」と書いていたが、正しくは2017年第2号である。残る7件は、情報処理学会研究報告CSECの2014年の記事の著者数を3名としていた（正しくは5名である）こと、Chhetriらの熱側チャネルの文献を通常の論文として扱っていた（正しくは全1ページのポスター概要である）こと、Pham Ngoc GiaoとJames G. H. GriffinとNathan D. Costaという3件の著者名の表記が一次資料と合っていなかったこと、ObfusCADeの機構の説明が要旨と食い違っていたこと、そして半音1段に対応する実効長の変化を周波数比の値そのままで「約5.95パーセント」と書いていた計算の混同である。

このほかの訂正は、ページ番号や論文番号の補い（Chhetriらの雑誌版が論文番号3で全25ページ、その会議版が論文番号19で全10ページ、ObfusCADeが論文番号82で全6ページ、Bayensらが1181から1198ページ、Laxtonらが469から478ページ、Hojjatiらが883から894ページ、Backesらが307から322ページ、QuietPrintが25から34ページ、PrinTrackerが1306から1323ページ、Tsoutsosらが15から20ページ）、著者名の表記の直し（Šorf・Švenda・Chmielewskiの発音符号を補い、Pham Ngoc Giaoを出版社表記のGiao N. Phamに、James G. H. GriffinをJames Griffinに、Nathan D. CostaをNathan Costaに改めた）、文献の種別の訂正（Chhetriらの熱側チャネルのICCPS 2016の文献は通常の論文ではなく全1ページのポスター概要であり、ObfusCADeは招待論文である）、そしてdr0wnedのarXiv版が会議版と著者数が違う（arXiv版はJacob Gatlinを含まない4名である）ことの注記である。

内容の裏取りによって記述を強められた箇所も5つある。第一に、前の調査者が「未検証」に置いていたRossel らのUSENIX Security 2025の要旨を取得できた。要旨は、造形機へのわずかな接触権限しかない攻撃者でも「その後に投入される造形ジョブへの不正な読み取り」ができると明言しており、これはCipherFluteの秘密に直接効く脅威なので、本文に反映した。第二に、同じく「未検証」だったBayensらのUSENIX Security 2017の要旨も取得でき、音響・実時間の部品追跡・造形後の材料分析の3つを組み合わせて誤った造形物を100パーセントの正解率で検出したという内容を確認した。第三に、同じく「未検証」だったSongらのACM CCS 2016の要旨をOpenAlexから取得でき、平均傾向誤差5.87パーセントおよび9.67パーセントという数値を確認した。これによって、Jamaraniらの4.47パーセントとの8年間の比較ができるようになった。第四に、前の調査者が典拠を付けずに書いていた上平員丈らの「金属を混ぜたフィラメント」「近赤外の蛍光染料」「強磁性のセル」という3つの方式について、Crossrefの書誌検索で該当する3件の論文を突き止め、DOIを補って裏づけた。第五に、「調べ残した穴」の第一項に挙げられていた計算機トモグラフィの分解能の問題が解決した。Chenらの2020年の論文の公開本文に、Bruker社のSkyScan 1172で1画素あたり10.08マイクロメートルという記述があり、半音1段の管長差（2ミリメートル台）より2桁以上細かいことが文献で裏づけられた。

実在が確認できず削除した文献は1件もない。「未検証のまま残ったもの」の節には6件を残したが、その内訳は、要旨を読めていないだけで書誌情報は確認済みのものが5件と、実務者向け会議の発表という記憶があるだけで一次資料が見つからないものが1件である。書誌情報の正しさが確認できていない文献は、このファイルには1件も残っていない。
