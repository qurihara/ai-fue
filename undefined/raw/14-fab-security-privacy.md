# デジタルファブリケーションと安全・プライバシーの交差

## この切り口の要約

この領域には、追加製造（アディティブマニュファクチャリング）を対象とした情報セキュリティ研究が20年近く蓄積されており、ACM CCSには2021年と2022年に専用のワークショップ（AMSec）まで置かれていた。研究は大きく四つの系統に分かれる。第一が造形機の発する音・振動・磁界・消費電力から造形物の形状を復元する側チャネル攻撃であり、第二が造形物を密かに弱くしたり造形機の制御を奪ったりする破壊攻撃であり、第三が造形物や造形機を一意に特定する指紋認識と法科学であり、第四が3次元モデルや造形物への電子透かしと情報ハイディングである。

CipherFluteにとって最も重大なのは第一の系統である。Al Faruqueらは2016年に、家庭用の熱溶解積層方式の造形機が発する音だけから工具経路を復元し、軸の推定精度86パーセント、長さの推定誤差11.11パーセントを達成したと報告した。2024年のJamaraniらは、離れた場所に置いた携帯電話の音響と磁界から軸方向を98.80パーセントで当て、平面的な形状で平均傾向誤差4.47パーセントを得たと報告している。CipherFluteは半音1段ごとに管の実効長を約5パーセント変えるので、この誤差は半音1段の差にほぼ並ぶ水準まで来ている。さらにGatlinらの論文は表題そのものが「暗号化は無意味である」であり、Dolgavinらは暗号化された造形データでも消費電力から設計を復元できることを産業機で示した。したがって「印刷データに秘密がそのまま載るのでネットワークから切り離した環境で印刷する」という論文の記述は、データ経路については正しいが、放射経路については不十分である。実際、Doらは家庭用造形機がネットワーク越しに侵害されて設計データを持ち出せることを2016年に示しており、切り離しの推奨自体には強い裏づけがある。逆にChhetriらの「Tool of Spies」は、スライサ（造形コンパイラ）を書き換えるだけで側チャネルからの復元率が最大39パーセント上がることを示し、切り離しても道具連鎖が汚染されていれば漏れることを示している。

一方で、造形物に秘密を埋め込むという着想自体は既存である。海野浩らの一連の研究は造形物の内部に空洞を作って情報を隠し、サーモグラフィやX線で読む方式を2014年から積み上げている。GuptaらはCADモデル内部にQRコードを隠して計算機トモグラフィで読む方式を示している。しかし読み出しの経路はいずれも光学・熱・X線・磁界であり、「人が吹いて音として読む」ものはこの領域には一つも見つからなかった。また「物理層に秘匿の力は無いと宣言して秘匿を秘密分散に全部負わせる」という設計思想も、この領域には見当たらなかった。

## 新規性への脅威が大きい文献

以下では脅威の種類を二つに分けて書く。一つは「同じ発明が既にある」という新規性そのものへの脅威であり、もう一つは「論文が書いている安全性の主張や運用上の推奨が弱まる」という主張への脅威である。CipherFluteの場合、この切り口で見つかったもののうち脅威が最も大きいのは後者である。

### 1. Confidentiality Breach Through Acoustic Side-Channel in Cyber-Physical Additive Manufacturing Systems

- 著者: Sujit Rokka Chhetri, Arquimedes Canedo, Mohammad Abdullah Al Faruque
- 掲載: ACM Transactions on Cyber-Physical Systems, 第2巻第1号, 論文番号3, 全25ページ, 2018年（学会発表版は Mohammad Abdullah Al Faruque, Sujit Rokka Chhetri, Arquimedes Canedo, Jiang Wan, "Acoustic Side-Channel Attacks on Additive Manufacturing Systems", ACM/IEEE International Conference on Cyber-Physical Systems (ICCPS) 2016, 論文番号19, 全10ページ）
- 確認先: https://doi.org/10.1145/3078622 （Crossrefの登録内容を取得して確認した。学会版は https://doi.org/10.1109/ICCPS.2016.7479068 ）

熱溶解積層方式の造形機が動作中に発する音を1本のマイクロフォンで録り、信号処理と機械学習と文脈に基づく後処理を組み合わせて、造形機に与えられた制御コードと造形物の形状を復元する攻撃を示した論文である。著者らは「平均の軸推定精度86パーセント、平均の長さ推定誤差11.11パーセント」を報告している。攻撃者は造形機に触る必要がなく、同じ部屋に居られればよい。この論文はこの分野の出発点であり、被引用数も181件（Semantic Scholarの集計）と多く、以後の全ての音響側チャネル研究がここから枝分かれしている。

CipherFluteとの関係は極めて直接的である。CipherFluteの秘密は管の長さそのものであり、この攻撃が復元しようとしている量とまったく同じものである。論文が挙げる「ネットワークから切り離した環境で印刷する」という対策は、データが通信路を通ることを止めるだけで、造形機が音を出すことを止めない。したがって切り離しの推奨は必要条件にすぎず、十分条件ではない、と論文中で明言する必要がある。ただし報告された長さ誤差11.11パーセントは、CipherFluteが半音1段に割り当てている実効長の変化（約5パーセント）の2段分に相当するので、2018年時点の技術では個々のスロットまでは読めなかったと言える。この「読める粒度」と「符号の粒度」の比較は、CipherFluteが自分の脅威モデルを定量的に語るための良い材料になる。

脅威の度合いは高である。理由は、新規性を崩すからではなく、論文が書いている運用上の推奨（切り離して印刷せよ）が防げる範囲を明確に狭めるからである。引用せずに済ませることはできない。

### 2. Practitioner Paper: Decoding Intellectual Property: Acoustic and Magnetic Side-channel Attack on a 3D Printer

- 著者: Amirhossein Jamarani, Yazhou Tu, Xiali Hei
- 掲載: 2nd EAI International Conference on Security and Privacy in Cyber-Physical Systems and Smart Vehicles (EAI SmartSP) 2024, 全22ページ（プレプリントは arXiv:2411.10887, 2024年11月16日投稿）
- 確認先: https://arxiv.org/abs/2411.10887 （arXivの論文ページを取得し、表題・著者・掲載先の記載・要旨を確認した）

前項の攻撃を、専用の測定器ではなく市販の携帯電話で、しかも造形機から離れた位置から行った研究である。音響と磁界の両方を使い、勾配ブースティング決定木で軸方向の移動・ステッピングモータの動作・ノズル速度・ロータ速度を推定し、平均約98.80パーセントの精度を報告している。実際の造形物に適用した評価では、平面的な設計に対して平均傾向誤差4.47パーセントを得たとしている。近接も高価な装置も不要であることを強調している点が、先行研究との差である。

CipherFluteとの関係は、脅威の現実味を一段上げる点にある。平均傾向誤差4.47パーセントは、CipherFluteが半音1段に割り当てる実効長の変化（周波数比2の12乗根から計算すると約5.95パーセント、外形の管長では約5パーセント）とほぼ同じ大きさである。つまり、造形中に近所で携帯電話を置かれた場合、隣接スロットの区別が付く水準に技術が到達しつつある。CipherFluteが誤り訂正符号を持っていることは、この文脈では攻撃者の側を助ける方向にも働く。攻撃者が復元した音列に誤りが残っても、同じReed-Solomon符号で訂正できてしまうからである。この指摘は論文の脅威モデル節に必ず書くべきである。

脅威の度合いは高である。この論文が示す精度は、CipherFluteの符号設計の粒度と正面から衝突しており、「造形の瞬間だけは秘密が守られている」という暗黙の前提を崩す。

### 3. Encryption is Futile: Reconstructing 3D-Printed Models Using the Power Side-Channel

- 著者: Jacob Gatlin, Sofia Belikovetsky, Yuval Elovici, Anthony Skjellum, Joshua Lubell, Paul Witherell, Mark Yampolskiy
- 掲載: 24th International Symposium on Research in Attacks, Intrusions and Defenses (RAID) 2021, 135-147ページ, ACM
- 確認先: https://doi.org/10.1145/3471621.3471850 （Crossrefの登録内容を取得して、表題・著者7名・予稿集名・ページを確認した。ACM Digital Libraryの本文ページは自動取得が拒否された）

造形機の消費電力の波形から造形物の形状を復元する攻撃である。表題が示すとおり、設計ファイルを暗号化しても、造形機が動く時点で電力波形として同じ情報が外に出てしまうので暗号化は無意味だ、という主張を掲げている。

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
- 掲載: arXiv:2606.13952, 2026年6月11日投稿（査読の有無は確認できていない）
- 確認先: https://arxiv.org/abs/2606.13952 （arXivの論文ページを取得し、表題・著者・投稿日・要旨を確認した）

市販の造形機に搭載されている能動的なモータ騒音打ち消し機構を、知的財産保護の観点から評価した研究である。Bambu Lab社の造形機2台のデータを使い、12種類の造形物の分類問題を立てた。要旨によれば、この機構は音響チャネルを完全に無力化し、分類精度は無作為の基準値8.33パーセントと区別が付かない水準まで落ちる。しかし振動は残り、要約統計量で約31パーセント、造形順序の時系列モデルで約61パーセントの精度が得られたとしている。また識別器は造形機ごとに固有で、別の機体には転移しないと述べている。結論として、音響は防げても振動・磁界・電力の側チャネルは開いたままだとしている。

CipherFluteとの関係は、使用している造形機が実際にBambu Lab社の機体（A1 miniとH2D）である点で、他人事ではない。良い知らせは、当該機体の騒音打ち消し機構が音響チャネルをほぼ潰すことである。悪い知らせは、振動・磁界・電力が開いていることである。CipherFluteの脅威モデル節は、この2点をそのまま書けば非常に具体的で説得力のある議論になる。

脅威の度合いは高である。使用機材そのものを扱った最新の評価であり、脅威モデルの記述の精度を大きく変える。ただしプレプリントなので、断定を避けて「プレプリントの段階での報告によれば」と書く配慮が必要である。

### 8. My Smartphone Knows What You Print: Exploring Smartphone-based Side-channel Attacks Against 3D Printers

- 著者: Chen Song, Feng Lin, Zhongjie Ba, Kui Ren, Chi Zhou, Wenyao Xu（いずれもニューヨーク州立大学バッファロー校）
- 掲載: Proceedings of the 2016 ACM SIGSAC Conference on Computer and Communications Security (CCS 2016), 895-907ページ
- 確認先: https://doi.org/10.1145/2976749.2978300 （Crossrefの登録内容を取得して、表題・著者6名と所属・予稿集名・ページ・公開日を確認した。要旨は出版社が公開していないため取得できていない）

造形機のそばに市販の携帯電話を置くだけで、その内蔵センサから造形物を推定する攻撃である。攻撃に特別な機材が要らないという点を前面に出しており、Al Faruqueらの研究と並んで、この脅威が現実的であることを広く知らせた論文である。

CipherFluteとの関係は第2項と同じ系統だが、こちらは査読を通ったトップ会議の論文であり、引用の重みが違う。「工房や研究室で造形している最中に、机に置かれた誰かの携帯電話が秘密を録っている」という具体的な絵を描くのに適している。

脅威の度合いは中である。運用上の推奨に効くが、より新しく精度の高い第2項があるので、こちらは系統の起点として引くのがよい。

### 9. 造形物の内部に情報を隠す一連の研究（海野浩・鈴木雅洋・ピヤラット シラパスパコォンウォン・鳥井秀幸・高嶋洋一ら）

主な文献を確認できた順に挙げる。

- Masahiro Suzuki, Piyarat Silapasuphakornwong, Kazutake Uehira, Hiroshi Unno, Youichi Takashima, "Copyright Protection for 3D Printing by Embedding Information Inside Real Fabricated Objects", 10th International Conference on Computer Vision Theory and Applications (VISAPP) 2015, 180-185ページ, 確認先 https://doi.org/10.5220/0005342401800185
- Kazutake Uehira, Satoru Baba, Masahiro Suzuki, Piyarat Silapasuphakornwong, Hideyuki Torii, Youichi Takashima, "Hiding Information in 3D Printed Objects by Forming Fine Cavities inside Objects", 2nd World Congress on Electrical Engineering and Computer Systems and Science 2016, 確認先 https://doi.org/10.11159/mhci16.102
- Kazutake Uehira, Masahiro Suzuki, Piyarat Silapasuphakornwong, Hideyuki Torii, Youichi Takashima, "Copyright Protection for 3D Printing by Embedding Information Inside 3D-Printed Objects", Digital Forensics and Watermarking (IWDW), Lecture Notes in Computer Science, 370-378ページ, 2017年, 確認先 https://doi.org/10.1007/978-3-319-53465-7_27
- Masahiro Suzuki, Piyarat Silapasuphakornwong, Youichi Takashima, Hideyuki Torii, Kazutake Uehira, "Number of Detectable Gradations in X-Ray Photographs of Cavities Inside 3-D Printed Objects", IEICE Transactions on Information and Systems, 第E100.D巻, 1364-1367ページ, 2017年, 確認先 https://doi.org/10.1587/transinf.2016edl8213
- Piyarat Silapasuphakornwong, Masahiro Suzuki, Youichi Takashima, Hideyuki Torii, Kazutake Uehira, "New Technique of Embedding Information Inside 3-D Printed Objects", Journal of Imaging Science and Technology, 第63巻, 010501-1から010501-8ページ, 2019年, 確認先 https://doi.org/10.2352/j.imagingsci.technol.2019.63.1.010501
- Masahiro Suzuki, Hideyuki Torii, Kazutake Uehira, "GAN technique for reading QR code embedded in 3D printed object", 2023 5th International Conference on Image, Video and Signal Processing, 157-163ページ, 2023年, 確認先 https://doi.org/10.1145/3591156.3591179
- 日本語版として、ピヤラット シラパスパコォンウォン, 鈴木雅洋, 海野浩「3Dプリント用デジタルデータの著作権保護のための情報ハイディング技術」電子情報通信学会技術研究報告, 第114巻第117号, 265-270ページ, 2014年7月, 確認先 https://cir.nii.ac.jp/crid/1520009408040188672 、および同題で 情報処理学会研究報告CSEC, 2014年第40号, 1-6ページ, 2014年6月26日, 確認先 https://cir.nii.ac.jp/crid/1573105977687785088

造形物の内部に微小な空洞を作る、金属を混ぜたフィラメントで内部に層を作る、近赤外の蛍光染料を二重に置く、内部に強磁性のセルを印刷するなど、さまざまな方式で造形物の中に情報を隠し、サーモグラフィ・X線写真・近赤外撮影・磁気センサで読み出す。目的は主に著作権保護であり、読み出した情報は権利者の識別子である。10年以上にわたって同じ着想を材料と読み出し手段を変えながら深めており、この分野の日本国内の中心的な系統である。

CipherFluteとの関係は、「日用品に見える3次元造形物の内部に、外から見えない情報を隠す」という枠組みがすでに確立していることを示す点にある。CipherFluteの差分は三つある。第一に、読み出しがサーモグラフィやX線ではなく人間の息と汎用のマイクロフォンだけで済むことである。第二に、埋め込む中身が権利者の識別子ではなく暗号資産の復元情報という高価値の秘密であり、そのため脅威モデルを明示していることである。第三に、秘匿の力を物理層に求めず秘密分散に負わせている点である。この三つを明確に書けば差分は立つ。

脅威の度合いは中である。着想の骨格が近いので必ず引用して差分を述べる必要があるが、読み出し手段と目的が異なるので新規性が崩れるとは考えにくい。

### 10. CADモデルの内部に認証符号を隠す一連の研究（Fei Chen, Nikhil Gupta ら）

- Fei Chen, Gary Mac, Nikhil Gupta, "Security features embedded in computer aided design (CAD) solid models for additive manufacturing", Materials & Design, 第128巻, 182-194ページ, 2017年, 確認先 https://doi.org/10.1016/j.matdes.2017.04.078
- Fei Chen, Yuxi Luo, Nektarios Georgios Tsoutsos, Michail Maniatakos, Khaled Shahin, Nikhil Gupta, "Embedding Tracking Codes in Additive Manufactured Parts for Product Authentication", Advanced Engineering Materials, 第21巻, 2018年, 確認先 https://doi.org/10.1002/adem.201800495
- Fei Chen, Jian H. Yu, Nikhil Gupta, "Obfuscation of Embedded Codes in Additive Manufactured Components for Product Authentication", Advanced Engineering Materials, 第21巻, 2019年, 確認先 https://doi.org/10.1002/adem.201900146
- Fei Chen, Jaime Zabalza, Paul Murray, Stephen Marshall, Jian Yu, Nikhil Gupta, "Embedded product authentication codes in additive manufactured parts: Imaging and image processing for improved scan ability", Additive Manufacturing, 第35巻, 101319, 2020年, 確認先 https://doi.org/10.1016/j.addma.2020.101319
- Nikhil Gupta, Fei Chen, Nektarios Georgios Tsoutsos, Michail Maniatakos, "ObfusCADe: Obfuscating Additive Manufacturing CAD Models Against Counterfeiting", Design Automation Conference (DAC) 2017, 論文番号82, 全6ページ, 確認先 https://doi.org/10.1145/3061639.3079847

部品の内部に二次元コードを分割して埋め込み、計算機トモグラフィで撮影して復元する。ただ埋めるだけでは第三者にも読まれてしまうので、符号を意図的に散らして難読化し、正しい復元手順を知る者だけが読めるようにする方向へ発展している。ObfusCADeは、CADモデルの側に偽の特徴を混ぜて模造を妨げる考え方である。

CipherFluteとの関係は、「造形物の内部に秘密の符号を隠し、専用の読み出し手順を要する」という構図が既にあることを示す点である。ただし読み出しに産業用の計算機トモグラフィが必要であり、正当な利用者にとっても手軽ではない。CipherFluteの「正当な利用者は吹くだけで読める」という利点は、この系列との対比で最も鮮明になる。逆に、この系列はCipherFluteに対する攻撃手段も示している。産業用の計算機トモグラフィを持つ攻撃者は、笛を吹かずに、外形からでは分からない内部の管長を読み取れるはずである。論文の脅威モデルには「計算機トモグラフィによる無音の読み出し」も明記したほうが誠実である。

脅威の度合いは中である。着想が近く、かつCipherFluteの脅威モデルの穴を一つ埋めてくれる。

### 11. Information Embedding in Additive Manufacturing through Printing Speed Control / Information Embedding for Secure Manufacturing

- 著者: Karim A. ElSayed, Adam Dachowicz, Jitesh H. Panchal（後者は Karim A. ElSayed, Adam Dachowicz, Mikhail J. Atallah, Jitesh H. Panchal）
- 掲載: Proceedings of the 2021 Workshop on Additive Manufacturing (3D Printing) Security (AMSec@CCS 2021), 31-37ページ / Journal of Computing and Information Science in Engineering, 第23巻, 2023年
- 確認先: https://doi.org/10.1145/3462223.3485623 および https://doi.org/10.1115/1.4062600 （前者は dblp の AMSec 2021 予稿集目次 https://dblp.org/db/conf/ccs/amsec2021.html とCrossrefの双方で、後者はCrossrefで確認した）

造形の速度という工程パラメータを変調して、造形物そのものに情報を埋め込む方式である。2023年の論文は、製造の安全確保のために情報を埋め込むという課題全体を整理した展望論文になっている。

CipherFluteとの関係は、「造形の物理的な自由度を情報の担体として使う」という発想が追加製造の安全研究の中に既にあることを示す点にある。CipherFluteは形状（管長）を担体にしており、こちらは速度を担体にしている。読み出しも異なるが、上位の枠組みとしては同じ棚に並ぶ。展望論文のほうは、CipherFluteが自分をこの分野の地図上のどこに置くかを述べるのに便利である。

脅威の度合いは中である。引用して枠組みの位置関係を述べるべきである。

### 12. 造形機と造形物の指紋認識（PrinTracker / ThermoTag / SI3DP）

- Zhengxiong Li, Aditya Singh Rathore, Chen Song, Sheng Wei, Yanzhi Wang, Wenyao Xu, "PrinTracker: Fingerprinting 3D Printers using Commodity Scanners", ACM CCS 2018, 確認先 https://doi.org/10.1145/3243734.3243735 （Semantic Scholarで要旨も確認した。14台の造形機で、条件が厳しい場合でも約92パーセントの精度を報告している）
- Yang Gao, Wei Wang, Yincheng Jin, Chi Zhou, Wenyao Xu, Zhanpeng Jin, "ThermoTag: A Hidden ID of 3D Printers for Fingerprinting and Watermarking", IEEE Transactions on Information Forensics and Security, 第16巻, 2805-2820ページ, 2021年, 確認先 https://doi.org/10.1109/TIFS.2021.3065225
- Bo Seok Shim, Yoo Seung Shin, Seong-Wook Park, Jong-Uk Hou, "SI3DP: Source Identification Challenges and Benchmark for Consumer-Level 3D Printer Forensics", ACM Multimedia 2021, 1721-1729ページ, 確認先 https://doi.org/10.1145/3474085.3475316 （Semantic Scholarで要旨も確認した。18種類の造形設定で252個の造形物を撮影したデータセットを公開し、機体レベルの識別や再走査と再印刷の検出という5つの課題を提案している）

造形物の表面に残る微細な痕跡から、どの造形機で作られたかを特定する研究群である。PrinTrackerは市販のスキャナで読める線形成の癖を使い、ThermoTagは押出機の熱的な癖を使い、SI3DPはこの問題を法科学のベンチマークとして定式化している。CipherFluteが既に引用しているG-ID（CHI 2020）は同じ棚の隣にある。

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
- 確認先: https://doi.org/10.1145/3462223.3485618 （dblp の AMSec 2021 予稿集目次 https://dblp.org/db/conf/ccs/amsec2021.html で表題・著者・ページ・DOIを確認した）

追加製造の安全を機密性・完全性・可用性の三つ組で語ることの不十分さを論じた立場表明の論文である。物理的な製造では、この三つ組では捉えられない脅威（造形物の品質の密かな劣化など）が主役になると述べている。

CipherFluteとの関係は、脅威モデルの記述の作法に直結する。CipherFluteは「音や物体の層には暗号学的な秘匿の力はまったく無い」と宣言して機密性を放棄し、秘匿を秘密分散に委ねている。これは三つ組の素朴な適用を避ける態度であり、この論文を引いて自分の立場を位置づけると、脅威モデルの節が理論的な支えを得る。

脅威の度合いは中である。この分野の脅威モデル論の代表的な文献であり、引用しないと脅威モデルの節が孤立して見える。

### 15. 造形データの改竄による破壊攻撃（dr0wned / Sturm らの .STL 攻撃）

- Sofia Belikovetsky, Mark Yampolskiy, Jinghui Toh, Jacob Gatlin, Yuval Elovici, "dr0wned - Cyber-Physical Attack with Additive Manufacturing", 11th USENIX Workshop on Offensive Technologies (WOOT) 2017, 確認先 https://www.usenix.org/conference/woot17/workshop-program/presentation/belikovetsky （プレプリントは http://arxiv.org/abs/1609.00133 ）
- Logan D. Sturm, Christopher B. Williams, Jamie A. Camelio, Jules White, Robert Parker, "Cyber-physical vulnerabilities in additive manufacturing systems: A case study attack on the .STL file with human subjects", Journal of Manufacturing Systems, 第44巻, 154-164ページ, 2017年, 確認先 https://doi.org/10.1016/j.jmsy.2017.05.007

前者は、造形データを密かに書き換えて無人航空機のプロペラを弱くし、飛行中に破壊するまでを通しで実演した研究である。後者は、STLファイルに空洞を挿入して部品の強度を落とす攻撃を、人間の被験者が見つけられるかどうかまで含めて評価した研究である。いずれも「造形データに手を入れられると、外見では分からない欠陥を仕込める」ことを示している。

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

- Benjamin Laxton, Kai Wang, Stefan Savage, "Reconsidering physical key secrecy: teleduplication via optical decoding", ACM CCS 2008, 確認先 https://doi.org/10.1145/1455770.1455830
- Soundarya Ramesh, Harini Ramprasad, Jun Han, "Listen to Your Key: Towards Acoustics-based Physical Key Inference", ACM HotMobile 2020, 確認先 https://doi.org/10.1145/3376897.3377853
- 木村悠生, 山元陽佑雅, 榎竜盛, 上原哲太郎「3Dプリンタによる印影からの印章の偽造」マルチメディア，分散，協調とモバイルシンポジウム2023論文集, 1269-1276ページ, 情報処理学会, 2023年6月28日, 確認先 https://cir.nii.ac.jp/crid/1050860532220398464

一つ目は、離れた場所から撮った写真だけで鍵の刻みを読み取り、複製できることを示した論文である。二つ目は、鍵を鍵穴に差し込むときの音から鍵の形状を推定する研究である。三つ目は、押された印影から3次元造形機で印章を偽造し、真贋の判定実験まで行った日本語の研究である。安価な造形機の普及によって印章の偽造が容易になったことを問題として立てている。

CipherFluteとの関係は、「形状が秘密である物体は、形状を観測されれば秘密を失う」という原理を、この分野の外の文献で裏づける点にある。CipherFluteは「形状を計測されれば無音で読める、複製も容易」と自ら宣言しているので、その宣言の学術的な根拠としてLaxtonらを引くのが最も適切である。Rameshらは「音から形状を推定する」という点で、CipherFluteの読み出し方式の裏返しになっており、対比として面白い。木村らは、日本語の読者に対して3次元造形機による複製の容易さを示す身近な例になる。

脅威の度合いは中である。CipherFluteの脅威モデルの記述が既知の原理に沿っていることを示すために引用すべきである。

### 18. Secure 3D Printing: Reconstructing and Validating Solid Geometries using Toolpath Reverse Engineering

- 著者: Nektarios Georgios Tsoutsos, Homer Gamil, Michail Maniatakos
- 掲載: 3rd ACM Workshop on Cyber-Physical System Security (CPSS@AsiaCCS) 2017
- 確認先: https://doi.org/10.1145/3055186.3055198 （dblpの書誌で表題・著者・掲載先・DOIを確認した）

造形機に与えられる工具経路から立体形状を逆に組み立て、意図した形状と一致するかを検証する研究である。防御側の道具として提案されているが、同じ技術は工具経路を手に入れた攻撃者の道具にもなる。

CipherFluteとの関係は、工具経路が形状と等価な情報であることを明示する点にある。「印刷データに秘密がそのまま載る」という論文の記述の技術的な内実を、この論文で裏づけられる。

脅威の度合いは中である。

### 19. See No Evil, Hear No Evil, Feel No Evil, Print No Evil? Malicious Fill Patterns Detection in Additive Manufacturing

- 著者: Christian Bayens, Tuan Le, Luis Garcia, Raheem Beyah, Mehdi Javanmard, Saman Zonouz
- 掲載: 26th USENIX Security Symposium 2017
- 確認先: https://www.usenix.org/conference/usenixsecurity17/technical-sessions/presentation/bayens （dblpの書誌とSemantic Scholarの書誌で表題・著者・掲載先・年を確認した。USENIXのページは自動取得が拒否されたため要旨は取得できていない）

造形中の音響と空間的な計測、および造形後の材料分析を組み合わせて、造形データに仕込まれた悪意ある充填パターンを検出する防御側の研究である。

CipherFluteとの関係は、音響を防御側の道具として使える可能性を示す点にある。CipherFluteの利用者は、笛が意図した設計どおりに造形されたかを、造形中の音から検証できるかもしれない。前項の完全性への脅威に対する現実的な対策の芽である。

脅威の度合いは中である。対策の議論を書くなら引用すべきである。

### 20. Security Implications of Malicious G-Codes in 3D Printing

- 著者: Jost Rossel, Vladislav Mladenov, Nico Wördenweber, Juraj Somorovsky
- 掲載: 34th USENIX Security Symposium 2025, 1867-1885ページ
- 確認先: https://www.usenix.org/conference/usenixsecurity25/presentation/rossel （dblpの書誌とSemantic Scholarの書誌の双方で表題・著者4名・掲載先・年・ページを確認した。USENIXの本文ページとオープンアクセス版PDFはいずれも自動取得が拒否されたため、内容は表題からしか判断していない。後述の未検証の節にも記載する）

造形機に与える制御コードが持つ攻撃面を体系的に扱った、この主題では最も新しいトップ会議の論文である。

CipherFluteとの関係は、造形の入力データを信頼できない経路で受け取ることの危険を、最新の査読論文で裏づける点にある。CipherFluteは自分でデータを生成するので直接の被害者にはなりにくいが、「造形の道具連鎖全体を信頼境界の内側に置く」という主張の根拠になる。

脅威の度合いは中である。内容の詳細を確認できていないので、引用する際は表題の範囲を超えた記述をしないほうがよい。

### 21. 側チャネルからの漏洩を設計側で減らす防御の系統

- Sujit Rokka Chhetri, Sina Faezi, Mohammad Abdullah Al Faruque, "Fix the Leak! An Information Leakage Aware Secured Cyber-Physical Manufacturing System", Design, Automation and Test in Europe (DATE) 2017, 1408-1413ページ, 確認先 https://doi.org/10.23919/DATE.2017.7927213
- Sujit Rokka Chhetri, Sina Faezi, Mohammad Abdullah Al Faruque, "Information Leakage-Aware Computer-Aided Cyber-Physical Manufacturing", IEEE Transactions on Information Forensics and Security, 第13巻, 2333-2344ページ, 2018年, 確認先 https://doi.org/10.1109/TIFS.2018.2818659
- Seyed Ali Ghazi Asgar, A. L. Narasimha Reddy, "QuietPrint: Protecting 3D Printers Against Acoustic Side-Channel Attacks", Workshop on Cyber-Physical System Security (CPSS@AsiaCCS) 2026, 確認先 https://doi.org/10.1145/3775042.3807880 （プレプリントは https://arxiv.org/abs/2602.02198 で表題・著者・DOIの記載を確認した。要旨によれば専用の装置を必要とせず、制御コードに最小限の変更を加えることで防御する）

工具経路や工程の設計を変えることで、側チャネルから漏れる情報量を減らす防御の系統である。QuietPrintは制御コードだけをいじって音響側チャネルを防ぐと述べている。

CipherFluteとの関係は、対策として実際に採れる手段を提供する点にある。CipherFluteは笛を複数本まとめて造形するので、造形の順序を無作為化する、無駄な移動を混ぜる、複数の笛の造形を交互に進めるといった対策を制御コードの生成側で実装できる。実装はすでに交互配置（インターリーブ）を持っているので、それを安全上の対策としても位置づけ直せる。

脅威の度合いは中である。対策の節を書くなら引用が必要である。

## 背景として押さえるべき文献

以下はいずれも書誌情報を一次資料または権威ある登録機関で確認したものであり、背景として引く程度の位置づけである。

- Avesta Hojjati ほか8名, "Leave Your Phone at the Door: Side Channels that Reveal Factory Floor Secrets", ACM CCS 2016, 確認先 https://doi.org/10.1145/2976749.2978323 。工場の床で携帯電話のセンサから製造の秘密が漏れることを示した論文であり、造形機に限らない一般化として引ける。
- Michael Backes, Markus Dürmuth, Sebastian Gerling, Manfred Pinkal, Caroline Sporleder, "Acoustic Side-Channel Attacks on Printers", USENIX Security Symposium 2010, 確認先 http://www.usenix.org/events/sec10/tech/full_papers/Backes.pdf 。紙の印刷機の音から印字内容を復元した古典であり、音響側チャネルの系譜の起点として引ける。
- Sujit Rokka Chhetri, Arquimedes Canedo, Mohammad Abdullah Al Faruque, "KCAD: Kinetic Cyber-Attack Detection Method for Cyber-Physical Additive Manufacturing Systems", ICCAD 2016, 確認先 https://doi.org/10.1145/2966986.2967050 。
- Sujit Rokka Chhetri, Sina Faezi, Arquimedes Canedo, Mohammad Abdullah Al Faruque, "Thermal Side-Channel Forensics in Additive Manufacturing Systems", ICCPS 2016, 確認先 https://doi.org/10.1109/ICCPS.2016.7479115 。
- Sujit Rokka Chhetri, Mohammad Abdullah Al Faruque, "Side Channels of Cyber-Physical Systems: Case Study in Additive Manufacturing", IEEE Design & Test, 第34巻第4号, 18-25ページ, 2017年, 確認先 https://doi.org/10.1109/MDAT.2017.2682225 。
- Shih-Yuan Yu, Arnav Vaibhav Malawade, Sujit Rokka Chhetri, Mohammad Abdullah Al Faruque, "Sabotage Attack Detection for Additive Manufacturing Systems", IEEE Access, 第8巻, 27218-27231ページ, 2020年, 確認先 https://doi.org/10.1109/ACCESS.2020.2971947 。
- Nathan D. Costa, Shih-Yuan Yu, Arnav Vaibhav Malawade, Sujit Rokka Chhetri, Mohammad Abdullah Al Faruque, "SideChannel-3D: Acoustic, Vibration, Magnetic, and Power Side-Channel 3D Printer Dataset", IEEE DataPort, 2021年, 確認先 https://doi.org/10.21227/j6cw-y314 。公開データセットであり、CipherFluteの笛が読み取られるかを自分で検証したい場合の出発点になる。
- Sina Faezi ほか6名, "Oligo-Snoop: A Non-Invasive Side Channel Attack Against DNA Synthesis Machines", NDSS 2019, 確認先 https://www.ndss-symposium.org/ndss-paper/oligo-snoop-a-non-invasive-side-channel-attack-against-dna-synthesis-machines/ 。音響側チャネルが造形機に限らない一般的な脅威であることを示す例である。
- Mark Yampolskiy, Wayne E. King, Jacob Gatlin, Sofia Belikovetsky, Adam Brown, Anthony Skjellum, Yuval Elovici, "Security of additive manufacturing: Attack taxonomy and survey", Additive Manufacturing, 第21巻, 431-457ページ, 2018年, 確認先 https://doi.org/10.1016/j.addma.2018.03.015 。この分野の標準的な調査論文である。
- Priyanka Mahesh ほか7名, "A Survey of Cybersecurity of Digital Manufacturing", Proceedings of the IEEE, 第109巻, 495-516ページ, 2021年, 確認先 https://doi.org/10.1109/JPROC.2020.3032074 。
- Steven Eric Zeltmann, Nikhil Gupta, Nektarios Georgios Tsoutsos, Michail Maniatakos, Jeyavijayan Rajendran, Ramesh Karri, "Manufacturing and Security Challenges in 3D Printing", JOM, 第68巻, 1872-1881ページ, 2016年, 確認先 https://doi.org/10.1007/s11837-016-1937-7 。
- Samuel Bennett Moore, William Bradley Glisson, Mark Yampolskiy, "Implications of Malicious 3D Printer Firmware", Hawaii International Conference on System Sciences (HICSS) 2017, 確認先 https://hdl.handle.net/10125/41899 。
- Mark Yampolskiy, Anthony Skjellum, Michael Kretzschmar, Ruel A. Overfelt, Kenneth R. Sloan, Alec Yasinsac, "Using 3D printers as weapons", International Journal of Critical Infrastructure Protection, 第14巻, 58-71ページ, 2016年, 確認先 https://doi.org/10.1016/j.ijcip.2015.12.004 。造形機そのものを凶器として使う脅威を扱う。
- Gerald Walther, "Printing Insecurity? The Security Implications of 3D-Printing of Weapons", Science and Engineering Ethics, 第21巻第6号, 1435-1445ページ, 2015年（オンライン公開は2014年）, 確認先 https://doi.org/10.1007/s11948-014-9617-x 。3次元造形による武器製造の安全上の含意を倫理の観点から論じる。
- 茂出木敏雄「違法造形物の3Dプリンタによる製造を規制するための3Dデータ照合技術に関する研究」尚美学園大学芸術情報研究, 第25巻, 101-120ページ, 2016年, 確認先 https://cir.nii.ac.jp/crid/1050282677910856960 、および同「違法造形物の3Dプリンタによる製造を規制するための3Dデータ照合技術の高精度化」同誌 第28巻, 1-19ページ, 2018年, 確認先 https://cir.nii.ac.jp/crid/1050282677911423360 （本文は https://shobi-u.repo.nii.ac.jp/records/622 ）。ポリゴンデータを特徴ベクトルに変換して禁止一覧と照合し、危険物や違法物の造形を止める方式である。造形の入口で内容を検査するという発想は、CipherFluteのように意味のある情報を形状に載せる手法にとって将来の障害になりうる。
- 伊藤優樹, 四方隼人, 水木敬明, 菅沼拓夫「3Dプリンタによるオープン装置や特殊カードケースの作成と対称関数の秘密計算への適用」コンピュータセキュリティシンポジウム2023論文集, 192-199ページ, 情報処理学会, 2023年, 確認先 https://cir.nii.ac.jp/crid/1050579444484578048 。カードベース暗号の物理的な道具を3次元造形機で作る研究であり、「造形物を暗号のための物理装置として使う」日本国内の別の系統である。
- 加藤大弥, 林達也, 砂原秀樹「サイバーフィジカル時代の物理媒体による認証・識別に関する考察」コンピュータセキュリティシンポジウム2017論文集, 第2巻第2号, 2017年, 確認先 https://cir.nii.ac.jp/crid/1050011097170108928 。
- Ryutarou Ohbuchi, Hiroshi Masuda, Masaki Aono, "Watermarking three-dimensional polygonal models", 5th ACM International Conference on Multimedia 1997, 261-272ページ, 確認先 https://doi.org/10.1145/266180.266377 （Crossrefの登録では表題の一部が "Watermaking" と誤記されている）、および同著者による "Watermarking three-dimensional polygonal models through geometric and topological modifications", IEEE Journal on Selected Areas in Communications, 第16巻, 551-560ページ, 1998年, 確認先 https://doi.org/10.1109/49.668977 。3次元モデルへの電子透かしの古典である。
- Jong-Uk Hou, Do-Gon Kim, Heung-Kyu Lee, "Blind 3D Mesh Watermarking for 3D Printed Model by Analyzing Layering Artifact", IEEE Transactions on Information Forensics and Security, 第12巻第11号, 2712-2725ページ, 2017年, 確認先 https://doi.org/10.1109/TIFS.2017.2718482 。造形時の積層痕を解析して、造形後の物体から透かしを読む。
- Arnaud Delmotte, Kenichiro Tanaka, Hiroyuki Kubo, Takuya Funatomi, Yasuhiro Mukaigawa, "Blind 3D-Printing Watermarking Using Moment Alignment and Surface Norm Distribution", IEEE Transactions on Multimedia, 第23巻, 3467-3482ページ, 2021年, 確認先 https://doi.org/10.1109/TMM.2020.3025660 。あわせて Arnaud Delmotte, "Blind watermarking for 3D printed objects by applying small geometric modification on the surface", 奈良先端科学技術大学院大学 博士論文 甲第1675号, 2020年3月31日, 確認先 https://cir.nii.ac.jp/crid/1910583860655800832 （本文は https://naist.repo.nii.ac.jp/records/10918 ）。日本国内の造形物向け透かしの学位論文である。
- Benoît Macq, Patrice Rondao-Alface, Mireia Montañola Sales, "Applicability of watermarking for intellectual property rights protection in a 3D printing scenario", 20th International Conference on 3D Web Technology (Web3D) 2015, 89-95ページ, 確認先 https://doi.org/10.1145/2775292.2775313 。
- Zhenyu Li, Daofu Gong, Lei Tan, Xiangyang Luo, Fenlin Liu, Adrian G. Bors, "Self-embedding watermarking method for G-code used in 3D printing", IEEE International Workshop on Information Forensics and Security (WIFS) 2021, 確認先 https://doi.org/10.1109/WIFS53200.2021.9648386 。造形の制御コードそのものに透かしを埋める。
- Pham Ngoc Giao, Suk-Hwan Lee, Oh-Heum Kwon, Ki-Ryong Kwon, "A Watermarking Method for 3D Printing Based on Menger Curvature and K-Mean Clustering", Symmetry, 第10巻第4号, 97, 2018年, 確認先 https://doi.org/10.3390/sym10040097 。
- James G. H. Griffin ほか5名, "Artificial Intelligence and Digital Watermarking will Transform Copyright Arbitration and Dispute Resolution for 3D Printing: An Empirical Analysis", European Journal of Law and Technology, 第14巻第2号, 2023年, 確認先 https://ejlt.org/index.php/ejlt/article/view/970 。法律の側から3次元造形と透かしを論じる。
- Ahmet Turan Erozan, Michael Hefenbrock, Dennis R. E. Gnad, Michael Beigl, Jasmin Aghassi-Hagmann, Mehdi B. Tahoori, "Counterfeit Detection and Prevention in Additive Manufacturing Based on Unique Identification of Optical Fingerprints of Printed Structures", IEEE Access, 第10巻, 105910-105919ページ, 2022年, 確認先 https://doi.org/10.1109/ACCESS.2022.3209241 。
- Akash Tiwari, Eduardo Jose Villasenor, Nikhil Gupta, A. L. Narasimha Reddy, Ramesh Karri, Satish T. S. Bukkapatnam, "Protection against Counterfeiting Attacks in 3D Printing by Streaming Signature-embedded Manufacturing Process Instructions", AMSec@CCS 2021, 11-21ページ, 確認先 https://doi.org/10.1145/3462223.3485620 。
- Felix Engelmann, Jan Philip Speichert, Ralf God, Frank Kargl, Christoph Bösch, "Confidential Token-Based License Management", AMSec@CCS 2021, 39-48ページ, 確認先 https://doi.org/10.1145/3462223.3485619 。
- Theo Zinner, Grant Parker, Nima Shamsaei, Wayne E. King, Mark Yampolskiy, "Spooky Manufacturing: Probabilistic Sabotage Attack in Metal AM using Shielding Gas Flow Control", AMSec@CCS 2022, 15-24ページ, 確認先 https://doi.org/10.1145/3560833.3563565 。
- Adam Dachowicz, Siva Chaitanya Chaduvula, Mikhail Atallah, Jitesh H. Panchal, "Microstructure-Based Counterfeit Detection in Metal Part Manufacturing", JOM, 第69巻, 2390-2396ページ, 2017年, 確認先 https://doi.org/10.1007/s11837-017-2502-8 。
- Siva Chaitanya Chaduvula, Adam Dachowicz, Mikhail J. Atallah, Jitesh H. Panchal, "Security in Cyber-Enabled Design and Manufacturing: A Survey", Journal of Computing and Information Science in Engineering, 第18巻, 2018年, 確認先 https://doi.org/10.1115/1.4040341 。
- Mordechai Guri らによる空隙越え covert channel の一連の研究。代表として Mordechai Guri, Yosef A. Solewicz, Yuval Elovici, "Fansmitter: Acoustic data exfiltration from air-Gapped computers via fans noise", Computers & Security, 第91巻, 101721, 2020年, 確認先 https://doi.org/10.1016/j.cose.2020.101721 、Mordechai Guri, Boris Zadov, Dima Bykhovsky, Yuval Elovici, "PowerHammer: Exfiltrating Data From Air-Gapped Computers Through Power Lines", IEEE Transactions on Information Forensics and Security, 第15巻, 1879-1890ページ, 2020年, 確認先 https://doi.org/10.1109/TIFS.2019.2952257 、Mordechai Guri ほか5名, "GSMem: Data Exfiltration from Air-Gapped Computers over GSM Frequencies", USENIX Security Symposium 2015, 849-864ページ, 確認先 https://www.usenix.org/conference/usenixsecurity15/technical-sessions/presentation/guri 。ネットワークから切り離すことが万能ではないという一般命題の裏づけとして引ける。
- Lin Zhang, Longfei Zhou, Luo Xiao, "Security and Privacy in Cloud 3D Printing", Customized Production Through 3D Printing in Cloud Manufacturing, 157-179ページ, 2023年, 確認先 https://doi.org/10.1016/B978-0-12-823501-0.00013-4 。クラウド経由の造形における安全とプライバシーを整理した章であり、クラウドスライサを避けるという推奨の根拠になる。
- Milan Sorf, Petr Svenda, Lukasz Chmielewski, "Large-Scale Security Analysis of Hardware Wallets", ARES 2025, 360-377ページ, 確認先 https://doi.org/10.1007/978-3-032-00633-2_21 。電子的なハードウェアウォレットの安全性評価であり、CipherFluteが「電源も電子部品も持たない」ことの利点を語る際の対比になる。
- Tyler Cultice, Joseph Clark, Wu Yang, Himanshu Thapliyal, "A Novel Hierarchical Security Solution for Controller-Area-Network-Based 3D Printing in a Post-Quantum World", Sensors, 第23巻第24号, 9886, 2023年, 確認先 https://doi.org/10.3390/s23249886 。
- Nawfal F. Fadhel, Richard M. Crowder, Fatimah Y. Akeel, Gary B. Wills, "Component for 3D Printing Provenance Framework: Security Properties Components for Provenance Framework", WorldCIS 2014, 91-96ページ, 確認先 https://doi.org/10.1109/WorldCIS.2014.7028174 。
- Mahender Kumar, Gregory Epiphaniou, Carsten Maple, "Security of cyber-physical Additive Manufacturing supply chain: Survey, attack taxonomy and solutions", Computers & Security, 第157巻, 104557, 2025年, 確認先 https://doi.org/10.1016/j.cose.2025.104557 。最新の調査論文である。
- Michael R. Durling ほか7名, "Model-Based Security Analysis in Additive Manufacturing Systems", AMSec@CCS 2022, 3-13ページ, 確認先 https://doi.org/10.1145/3560833.3563566 、および Nils Ole Tippenhauer, "Déjà Vu? Challenges and Opportunities for AM Security from an ICS perspective", AMSec@CCS 2022, 1ページ, 確認先 https://doi.org/10.1145/3560833.3563556 。いずれもAMSec 2022の予稿集目次 https://dblp.org/db/conf/ccs/amsec2022.html で確認した。

## 未検証のまま残ったもの

以下は、実在と書誌情報は確認できたが内容（要旨や本文）を一次資料から読めなかったもの、あるいは実在自体を確認しきれなかったものである。

1. Jost Rossel, Vladislav Mladenov, Nico Wördenweber, Juraj Somorovsky, "Security Implications of Malicious G-Codes in 3D Printing", USENIX Security Symposium 2025, 1867-1885ページ。書誌情報はdblpとSemantic Scholarの双方で一致を確認したが、USENIXの発表ページ（https://www.usenix.org/conference/usenixsecurity25/presentation/rossel ）とオープンアクセス版PDF（https://www.usenix.org/system/files/conference/usenixsecurity25/sec25cycle1-prepub-195-rossel.pdf ）はいずれもHTTP 403で自動取得が拒否され、要旨を読めていない。したがって内容は表題から推測した範囲でしか書いておらず、引用の際には本文を人が確認する必要がある。
2. Christian Bayens ほか5名, "See No Evil, Hear No Evil, Feel No Evil, Print No Evil?", USENIX Security 2017。同じ理由で要旨を読めていない。防御に音響を使うという記述は、この論文が音響を含む複数のセンサで検証することを表題と既知の紹介から述べたものであり、具体的な精度は確認していない。
3. Chen Song ほか5名, "My Smartphone Knows What You Print", ACM CCS 2016。ACM Digital Libraryの本文ページはHTTP 403で取得できず、Crossrefにも要旨が登録されていないため、報告されている精度の数値を確認できていない。本文で数値に触れていないのはこの理由である。
4. Mohammad Abdullah Al Faruque ほか3名, "Acoustic Side-Channel Attacks on Additive Manufacturing Systems", ICCPS 2016。IEEE Xploreの本文ページから内容を取得できなかった。本文で挙げた86パーセントと11.11パーセントという数値は、同じ著者らによる拡張版であるACM Transactions on Cyber-Physical Systems 2018年の論文の要旨（Crossrefに登録されている）から取ったものであり、2016年の会議版の数値ではない可能性がある。引用の際は拡張版を主に引くのが安全である。
5. 3次元造形機で作った「バンプキー」を使った錠の解錠に関する発表が、DEF CONやBlack Hatといった実務者向けの会議で行われたという記憶があるが、一次資料を見つけられなかったため書誌情報を書いていない。物理的な鍵の複製という論点はLaxtonらとRameshらと木村らで十分に押さえられるので、この穴は大きくないと考える。

## この切り口で見つからなかったこと

ここに書くことは、CipherFluteの新規性の主張の根拠として使える。いずれも「探したが見つからなかった」ことであり、「存在しない」ことの証明ではないが、この切り口で通常たどり着く範囲は網羅したと考えている。

第一に、デジタルファブリケーションの安全研究の中に、造形物に埋め込んだ情報を「人が吹いて出る音の高さ」として読み出す手法は一つも見つからなかった。この分野で使われている読み出しの経路は、可視光による撮影、サーモグラフィによる熱の観測、X線写真、計算機トモグラフィ、近赤外の蛍光、磁気センサ、電波の反射に限られていた。海野浩らの系統もGuptaらの系統も、読み出しには何らかの計測装置を必要とする。汎用のマイクロフォンと人間の息だけで読めるものは無かった。

第二に、「物理層には暗号学的な秘匿の力がまったく無いと宣言し、秘匿の責任を秘密分散に全部移す」という設計思想を明示的に取った研究は見つからなかった。追加製造の安全研究では、機密性を守ろうとする研究（暗号化、難読化、免許管理）と、機密性の枠組み自体を批判する研究（Yampolskiyらの「Myths and Misconceptions」）の両方があるが、後者は批判にとどまり、機密性を意図的に放棄した設計を提示してはいない。CipherFluteの脅威モデルの立て方は、この分野の中では新しい。

第三に、誤り訂正符号を物理的な造形物に載せて秘密の分片を運ぶという組み合わせは、この切り口では見つからなかった。造形物に符号を載せる研究（LayerCodeやSeedmarkersなど、他の切り口で扱われるもの）はあり、誤り訂正を含むものもあるが、運ぶ中身は識別子であって秘密ではなかった。追加製造の安全研究の側では、造形物に情報を埋め込む研究（ElSayedら、Chenら）はあるが、運ぶ中身は認証符号や権利者の識別子であり、秘密分散の分片ではなかった。

第四に、「家庭で作るので製造者を信頼しなくてよい」という利点を、造形物を秘密の担体として使う文脈で正面から論じた研究は見つからなかった。最も近いAsgarらの2025年のプレプリントは、外部の製造者が必ず居る前提で相互不信の問題を解いており、家庭製造によってその問題が消えるという議論はしていない。したがってCipherFluteはこの論点を自分の言葉で述べる余地があるが、逆に言えば、その主張を支える先行研究が薄いので、Asgarらを引いて「受託製造では複雑な仕組みを要する問題を、自家製造で回避している」という形に組み直すのが説得力を持つ。

第五に、笛のような共鳴管を持つ造形物の形状が、造形機の放射（音・振動・電力・磁界）からどの精度で復元できるかを測った研究は見つからなかった。既存の側チャネル研究の評価対象は、直線と円弧からなる一般的な部品であり、「半音1段に相当する数パーセントの管長差を区別できるか」という問いは立てられていない。これはCipherFluteが将来の課題として名指しできる、明確に空いている評価である。

第六に、3次元造形物を暗号資産の鍵や復元情報の保管媒体として扱った学術研究は、この切り口では見つからなかった。金属製のシード保管製品やCasascius物理ビットコインは製品であり、ハードウェアウォレットの安全性評価（Sorfら）は電子機器を対象にしている。

第七に、日本語の文献に、3次元造形と秘密分散と音響読み出しを組み合わせたものは見つからなかった。日本国内で近いのは、海野浩らの造形物内部への情報ハイディング、Delmotteの造形物向け透かし、伊藤優樹らのカードベース暗号のための造形装置、木村悠生らの印章偽造、茂出木敏雄の違法造形物の照合であり、いずれもCipherFluteとは目的か読み出し手段が異なる。

## 調べ残した穴

第一に、計算機トモグラフィやX線による無音の読み出しが、CipherFluteの管長をどの精度で読めるかを調べ切れていない。Chenらの系統は計算機トモグラフィを正当な読み出し手段として使っているので、CipherFluteに対しては攻撃手段になる。産業用の計算機トモグラフィの空間分解能が、半音1段の管長差（おおよそ2ミリメートル台）を分離できるのはほぼ確実だと予想されるが、文献で裏づけていない。ここは論文の脅威モデルに関わるので、追って埋めるべきである。

第二に、電磁波側チャネルによる造形物の復元について、単独の論文を確認していない。Chhetriらの「Tool of Spies」が4つの側チャネルの一つとして電磁波を挙げていることは確認したが、電磁波だけを扱った研究の書誌を押さえていない。

第三に、標準や指針の類（米国国立標準技術研究所の報告書、ASTM F42委員会やISO/ASTM 52920系の規格）を調べていない。「切り離した環境で印刷する」という推奨が、業界の指針の中でどう書かれているかを確認できれば、論文の記述に権威づけができる。なおGatlinらのRAID 2021の共著者にはJoshua LubellとPaul Witherellという米国国立標準技術研究所の研究者が入っているので、そこから辿るのが早い。

第四に、CHI・UIST・Symposium on Computational Fabrication・TEIといったヒューマンコンピュータインタラクションの会議を、安全とプライバシーの観点で系統的に走査していない。G-IDやStructCodeは既に論文が引用しているが、たとえば「ファブリケーションの安全に対する利用者の理解」を扱う質的研究が存在する可能性があり、CipherFluteの利用者像の議論に効くかもしれない。

第五に、Bambu Lab社の造形機のクラウド機構が造形データをどう扱うかについて、学術的な分析を一つも見つけていない。Yocamらのプレプリントが同社の機体を対象にしているが、扱っているのは騒音打ち消し機構であってクラウドではない。CipherFluteが実際に使っている機体の通信経路の話なので、査読者から問われる可能性がある論点である。

第六に、日本の法制度（銃砲刀剣類所持等取締法や印章に関する実務）の側から、3次元造形による複製をどう扱っているかを調べていない。CipherFluteの用途は武器や印章ではないので直接の関係は薄いが、「造形の入口で内容を検査する」という茂出木敏雄の系統が制度化された場合、形状に意味を載せる手法一般に影響しうる。

第七に、特許文献を一切調べていない。造形物に情報を埋め込む技術は、海野浩らの系統をはじめとして出願がある可能性が高い。学会論文としての新規性とは別の話であるが、実用化を考えるなら確認が必要である。
