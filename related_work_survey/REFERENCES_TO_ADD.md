# 論文に追加すべき参考文献

2026年7月30日作成。すべて一次資料または著者公開版で書誌を確認し、確認先のURLを付けた。ACM Digital LibraryとIEEE Xploreは調査環境から取得を拒まれたため、著者公開版、arXiv版、機関リポジトリ、Crossref、DBLPで代替した確認を行っている。その旨は各項目に記した。

`PAPER_REVISION.md` の文面案で用いた仮の番号（新1から新26）を見出しに残してある。

## 優先度1　これを引かずに投稿してはならない（2件）

### 新1　Whoosh の FluteCase

Reyes, G., Zhang, D., Ghosh, S., Shah, P., Wu, J., Parnami, A., Bercik, B., Starner, T., Abowd, G. D. and Edwards, W. K.: Whoosh: Non-Voice Acoustics for Low-Cost, Hands-Free, and Rapid Input on Smartwatches, Proc. 2016 ACM International Symposium on Wearable Computers (ISWC '16), pp. 120–127 (2016).

- DOI: 10.1145/2971763.2971765
- 確認先: 著者所属機関の公開版 https://sites.cc.gatech.edu/fac/keith/pubs/iswc2016-whoosh.pdf を全文取得して精読した。書誌はCrossref（https://api.crossref.org/works/10.1145/2971763.2971765）とDBLP（https://dblp.org/rec/conf/iswc/ReyesZGSWPBSAE16）で照合した。
- 注意: Semantic Scholarはこの論文の会議名を International Workshop on the Semantic Web という誤った値で持っている。実際の掲載先はウェアラブルコンピューティングの国際シンポジウムである。
- 引用時に使える確定事実: 節見出しは「FLUTECASE: A PASSIVE 3D-PRINTED WATCH CASE」である。管の本数は8本で閉管である。管長の式は L = 14.956 × 2^(i/12) [mm] であり、公比は平均律の半音比である。設計式から出る8本の周波数は約3827 Hzから5733 Hzで、広がりは半音7個分にとどまる（実測周波数は論文に報告がない）。認識はメル周波数ケプストラム係数とサポートベクターマシンによる分類であり、基本周波数の推定を行わない。利用者非依存では79.7パーセントに落ちる。管長は「For replicability」として定数公開されている。

### 新4　Printone

Umetani, N., Panotopoulou, A., Schmidt, R. and Whiting, E.: Printone: Interactive Resonance Simulation for Free-form Print-wind Instrument Design, ACM Trans. Graphics, Vol. 35, No. 6, Article 184, pp. 184:1–184:14 (2016).

- DOI: 10.1145/2980179.2980250
- 確認先: 著者の研究室ページ https://cgenglab.github.io/en/publication/sigga16_printone/ が掲げる公開版（全14ページ）を取得して精読した。ACM Digital LibraryとDartmouth大学の公開版はいずれもHTTP 403であった。書誌はDOIへのコンテンツネゴシエーションで照合した。
- 短縮版: Proc. 2017 International Symposium on Musical Acoustics, pp. 18–21 (2017). https://isma2017.cirmmt.mcgill.ca/proceedings/pdf/ISMA_2017_paper_47.pdf
- 引用時の注意: **「56個の目標周波数のうち53個」という数値は短縮版にしか存在しない。** 本体は「104個の目標周波数のうち、目標を出せなかったのは4例だけであった」と書いている。本体の全14ページに「56」は現れない。論文に書くなら本体の数値を使う。
- 引用時に使える確定事実: 本体と短縮版の両方に cent および cents は0件である。「実測範囲」は吹く速さを徐々に上げながら明瞭に鳴った最低周波数と最高周波数の幅である。「吹く速さの変化は10 Hzの誤差を容易に補償できる」と述べている。空洞を作るため模型を手作業で半分に切り、別々に印刷してサポート材を除去し、接着している。装置はMakerBot Replicator 2でPLAである。指孔5個の作例（DOUGHNUT）は1つの物体から9音を出す。

## 優先度2　物理バックアップの先例と、脅威モデルの穴（7件）

### 新7　codex32

Curr, L. O., Sneed, P. and Poelstra, A.: codex32: Checksummed SSSS-aware BIP32 seeds, Bitcoin Improvement Proposal 93, Informational, Draft (2023).

- 確認先: https://raw.githubusercontent.com/bitcoin/bips/master/bip-0093.mediawiki を全文取得した。回転円板は参照実装 https://github.com/BlockstreamResearch/codex32 と公式サイト https://secretcodex32.com/ で確認した。
- 引用時の注意: 「紙の回転円板」はBIP-93の本文に一度も現れない。BIP-93は手計算の具体的手順を標準の範囲外と明記している。参照実装は「対応する財布が存在しないので本物の金銭に使うな」と警告しており、状態は今もDraftである。
- 確定事実: 有限体はGF(32)で、1の原始三乗根を添加してGF(1024)へ拡大する。13文字の検査符号は8文字以内に影響する任意の誤りを必ず検出し、置換4文字まで、消失8文字まで、連続消失13文字までを訂正する。閾値は2から9、断片は最大31枚。128ビットの主種子は48文字に収まる。hide、hidden、conceal、disguise、steganography、plausible、deniable はすべて0件である。

### 新8　SeedQR と CompactSeedQR

SeedSigner Project: SeedQR and CompactSeedQR Specification (2022年1月22日初出、継続更新).

- 確認先: https://raw.githubusercontent.com/SeedSigner/seedsigner/dev/docs/seed_qr/README.md を全文取得した。3Dプリント実装はPrintablesの識別番号786967（21×21、2024年3月18日初公開）、782441（25×25）、1165469で確認した。金属板の商品は https://www.gobrrr.me/product/steelqr-c12/ で確認した。
- 確定事実: 標準形式はBIP-39索引を4桁零詰めで連結し、12語は48桁で25×25になる。CompactSeedQRは索引を11ビットで連結して検査ビットを落とし、12語は128ビット・16バイト・21×21になる。誤り訂正水準はLである。金属板に手で穴を開ける場合、CompactSeedQRなら作業量が35から40パーセント減ると書いている。
- 引用時の注意: 仕様書自身はReed–Solomonという語を一度も使っていない。誤り訂正を自前で設計せず二次元コード規格の機能に依存している。秘密分散は持たない（Shamir、split、share が全文で0件）。

### 新9　QR SafeShare

Jurgen (GitHubのアカウント名は cmd1982): QR SafeShare – Split and protect secrets in QR codes (2025).

- 確認先: https://github.com/cmd1982/qr-safeshare （最初のコミットは2025年9月11日14時25分18秒・協定世界時、全129コミット、最終の押し上げは2025年10月5日）、https://makerworld.com/en/models/2244875-qr-safeshare （作成は2026年1月14日）、Printables投稿1419250（初公開は2025年9月19日）、qrsafeshare.com。GitHub API（https://api.github.com/repos/cmd1982/qr-safeshare）で日付を確認した。
- 確定事実: 説明文のExtra protectionの節に「決意した攻撃者ならこじ開けられるが、この覆いは素早い走査や気づかれない走査を防ぎ、許可の無い読み出しに必要な労力を上げる」という一文がある。安全性はすべて秘密分散（排他的論理和方式とShamir方式）に負わせている。各断片を3MFで書き出し、スライサで高さ2ミリメートルのすぐ上に色替えを入れる指示がある。錠つき覆いの立体データも同梱されている。
- 引用時の注意: 日用品への偽装は謳っていない。MakerWorld、Printables、GitHubのREADME、help.html、disclaimer.html、index.html、split.htmlの全文を確認したが、偽装や迷彩や目立たない物に仕込むという記述はどこにもない。攻撃者の能力を列挙して守らない範囲を宣言する学術的な節も存在しない。普及はごく小さく、MakerWorldはいいね1件でダウンロード0件である。

### 新3　SoundOff

Fu, Y., Shen, V., Riera-Naranjo, V., Deng, B., Adams, A. and Hester, J.: SoundOff: Low-cost Passive Ultrasound Tags for Non-invasive and Non-Intrusive Smart Home Sensing, Proc. ACM on Interactive, Mobile, Wearable and Ubiquitous Technologies, Vol. 9, No. 4, Article 174, pp. 1–32 (2025).

- DOI: 10.1145/3770666
- 確認先: 著者公開版 https://drive.google.com/file/d/1StyNwdbcGeV810e1TdhXK2Wv9YkMV2a8/view を取得して本文を読んだ。書誌はDBLPで照合した。
- 引用時の注意: 抄録の「数千通りの設計」に対応する具体的な数は本文に無い。実装で生成した候補は1277通りであり、そこから対の間のハミング距離で選んだ15個を造形して0.5メートルで93.75パーセントを得ている。**1277通りを10.3ビットと換算するのは誤りである。** 区別できた集合は15個であり、3.907ビット相当である。

### 新18　造形機の音響側チャネル（起点）

Chhetri, S. R., Canedo, A. and Al Faruque, M. A.: Confidentiality Breach Through Acoustic Side-Channel in Cyber-Physical Additive Manufacturing Systems, ACM Trans. Cyber-Physical Systems, Vol. 2, No. 1, Article 3, pp. 1–25 (2018).

- DOI: 10.1145/3078622
- 会議版: Acoustic Side-Channel Attacks on Additive Manufacturing Systems, Proc. ACM/IEEE ICCPS 2016, pp. 1–10. DOI 10.1109/ICCPS.2016.7479068
- 確定事実: 造形機の音だけから工具経路と形状を復元し、平均の軸推定精度86パーセント、平均の長さ推定誤差11.11パーセントを報告している。被引用181件。

### 新19　造形機の音響と磁界の側チャネル（最新の到達点）

Jamarani, A., Tu, Y. and Hei, X.: Practitioner Paper: Decoding Intellectual Property: Acoustic and Magnetic Side-channel Attack on a 3D Printer, EAI SmartSP 2024.

- 確認先: プレプリント https://arxiv.org/abs/2411.10887 （2024年11月16日投稿）
- 確定事実: 離れた場所の市販の携帯電話の音響と磁界から、軸方向の平均精度98.80パーセント、平面的な設計で平均傾向誤差4.47パーセントを報告している。

### 新20　使用機材そのものを対象とした評価

Yocam, E., Vaidyan, V., Flack, M., Comert, G. and Mwakalonge, J. L.: Side-Channel Attacks Bypass Protection in 3D Printers, arXiv:2606.13952 (2026年6月11日投稿).

- 確認先: https://arxiv.org/abs/2606.13952
- 査読の有無は未確認である。査読前原稿として引くか、投稿前に掲載先を確認する。
- 確定事実: **CipherFluteが実際に使っているBambu Lab社の造形機2台を対象としている。** 能動的なモータ騒音打ち消しにより音響チャネルは無作為の基準値8.33パーセントと区別が付かない水準まで潰れる一方、振動は残り、時系列モデルで約61パーセントの分類精度が出る。振動、磁界、電力は開いたままだと結論している。

### 新21　スライサの汚染

Chhetri, S. R., Barua, A., Faezi, S., Regazzoni, F., Canedo, A. and Al Faruque, M. A.: Tool of Spies: Leaking your IP by Altering the 3D Printer Compiler, IEEE Trans. Dependable and Secure Computing, Vol. 18, pp. 667–678 (2021).

- DOI: 10.1109/TDSC.2019.2923215
- 確定事実: スライサを密かに書き換えるだけで、音・電力・振動・電磁波の4つの側チャネルからの制御コード復元成功率が最大39パーセント上がる。

## 優先度3　国内の近接研究（6件）

### 新10　FabAuth と WISS 2019版

久保勇貴, 江口佳那, 青木良輔, 近藤重邦, 東正造, 犬童拓也: 内部構造パターンの差異を利用した3Dプリントオブジェクト識別手法, WISS 2019（第27回インタラクティブシステムとソフトウェアに関するワークショップ）.

- 確認先: https://www.wiss.org/WISS2019Proceedings/oral/8.pdf
- 英語版: Kubo, Y., Eguchi, K., Aoki, R., Kondo, S., Azuma, S. and Indo, T.: FabAuth: Printed Objects Identification Using Resonant Properties of Their Inner Structures, Extended Abstracts of ACM CHI 2019. DOI 10.1145/3290607.3313005
- 続報: 3D-Printed Object Identification Method using Inner Structure Patterns Configured by Slicer Software, Extended Abstracts of ACM CHI 2020, pp. 1–7. DOI 10.1145/3334480.3382847
- 確定事実: 充填率と充填パターンの違いで固有の音響周波数応答を割り当て、圧電素子による20キロヘルツから40キロヘルツの掃引信号と機械学習で8個を平均99.3パーセントで識別する。引用している先行研究の集合（Acoustic Barcodes、Acoustic Voxels、AirCode、InfraStructs）がCipherFluteと重なる。2019年と2020年の3件で完結しており、符号量を伸ばす続編は存在しない。

### 新11　スタイラスの把持状態識別

髙倉礼, 鈴木健介, 國分晴利, 志築文太郎: 能動的音響計測に基づくスタイラスの把持状態識別手法の検討, WISS 2021.

- 確認先: https://www.wiss.org/WISS2021Proceedings/data/20.pdf
- 確定事実: 3Dプリント時の充填率を変えてスタイラスの内部構造を変え、能動的音響計測で音響信号の伝わり方の違いを機械学習で読む。充填率25、50、75パーセントで6つの把持状態を95パーセント程度、充填率100パーセントで89.8パーセントで識別した。

### 新12　造形物内部への情報埋め込み（神奈川工科大学の系譜の代表）

Suzuki, M., Dechrueng, P., Techavichian, S., Silapasuphakornwong, P., Torii, H. and Uehira, K.: Embedding Information into Objects Fabricated With 3-D Printers by Forming Fine Cavities inside Them, IS&T International Symposium on Electronic Imaging (Media Watermarking, Security, and Forensics), Vol. 29, pp. 6–9 (2017).

- 確認先: https://library.imaging.org/ei/articles/29/7/art00002
- 国内の関連発表は電子情報通信学会技術研究報告に8件（116(34)、116(132)、116(176)、116(501)、117(113)、117(282)、117(476)など）と画像電子学会研究会講演予稿16.03がある。科学研究費助成事業の課題番号は19H04141である。
- 確定事実: 造形中に物体内部へ微小空洞、高反射突起、近赤外蛍光染料、強磁性セルを作り込み、X線、サーモグラフィ、近赤外線、磁力計で非破壊に読み出す。数センチメートルの造形物に数百ビットを埋め込めると明記している。動機は著作権保護である。

### 新13　カードベース暗号

den Boer, B.: More Efficient Match-Making and Satisfiability: The Five Card Trick, Advances in Cryptology — EUROCRYPT '89, Lecture Notes in Computer Science (1990). DOI 10.1007/3-540-46885-4_23

- 国内の特集: 情報処理, 2026年5月号および6月号「カードベース暗号とその展開」（副題は「情報セキュリティ教育にも応用可能な身近な道具を利用した暗号技術」、駒野雄一さん、水木敬明さん、真鍋義文さん、縫田光司さんら）
- 日用品への拡張: Murata, S., Miyahara, D., Mizuki, T. and Sone, H.: Public-PEZ Cryptography, Information Security (ISC 2020) (2020). DOI 10.1007/978-3-030-62974-8_4。ほかにダイヤル錠（TAMC 2007）、15パズル（COCOA 2007）、硬貨（TPNC 2018）、ボールと袋（DICOMO 2019）がある。
- 確定事実: CiNii Researchで「カードベース暗号」は95件が該当する。いずれも複数人の秘密計算プロトコルであり、物体に秘密を保管して後から読み出す用途のものはない。

### 新14　3Dプリンタで作るカードベース暗号の実行装置

伊藤優樹, 四方隼人, 水木敬明, 菅沼拓夫: 3Dプリンタによるオープン装置や特殊カードケースの作成と対称関数の秘密計算への適用, コンピュータセキュリティシンポジウム2023論文集, pp. 192–199 (2023).

- 確認先: https://cir.nii.ac.jp/crid/1050579444484578048
- 家庭用3Dプリンタで作った受動的な物体が暗号的役割を担う点で、国内で最も近い研究である。

### 新22　X線CTによる笛の内径の復元

中尾美月, 須藤壮一朗, 水野明哲, 高橋義典: 尺八のCT画像の輝度値に基づく3Dモデルの内径補正と付加製造による復元評価, 情報処理学会研究報告 音声言語情報処理, 2026-SLP-159, No. 24, pp. 1–6 (2026年2月24日).

- 確認先: https://ipsj.ixsq.nii.ac.jp/records/2007593
- 脅威モデルにおける「CTスキャンによる無音の読み出し」の根拠として使える。ただし内径の復元になお差が残り、倍音構造の再現は手法によって順位が逆転すると報告しているため、半音1段（管長でおよそ2ミリメートル台）を確実に分離できるとまでは書けない。

## 優先度4　符号設計と物理暗号の先例（5件）

### 新17　隣接同記号禁止の最も近い先例

Goldman, N., Bertone, P., Chen, S., Dessimoz, C., LeProust, E. M., Sipos, B. and Birney, E.: Towards practical, high-capacity, low-maintenance information storage in synthesized DNA, Nature, Vol. 494, No. 7435, pp. 77–80 (2013).

- DOI: 10.1038/nature11875
- 確認先: https://pmc.ncbi.nlm.nih.gov/articles/PMC3672958/
- 書誌の注意: 確定版の題名は上記である。PubMed Centralの著者原稿の題名は「Toward practical high-capacity low-maintenance storage of digital information in synthesised DNA」であり、こちらを引くと誤りになる。
- 確定事実: バイト列をハフマン符号で三進の桁へ変換し、各桁を「直前に使った塩基とは異なる三塩基のいずれか」へ写している。原文は "by replacement of each trit with one of the three nucleotides different from the previous one used, ensuring no homopolymers were generated" である。

### 隣接同記号禁止の容量の理論（3件、まとめて1つの根拠として引く）

- Shannon, C. E.: A Mathematical Theory of Communication, Bell System Technical Journal, Vol. 27, pp. 379–423 (1948). 第1節の定理1（容量は行列式方程式の最大の実根の対数である）
- Marcus, B. H., Roth, R. M. and Siegel, P. H.: An Introduction to Coding for Constrained Systems, 第5版（著者公開の教科書草稿）. 第3章の定理3.4
- Immink, K. A. S. and Cai, K.: Design of Capacity-Approaching Constrained Codes for DNA-Based Storage Systems, IEEE Access, Vol. 8, pp. 49523–49531 (2020). 特性方程式 x^(m+1) − q x^m + q − 1 = 0 の最大の実根の対数であり、m = 1 で q − 1 になる。表1のm=1の欄が log2 3 = 1.5850 である。
  - 確認先: 著者公開の査読前版 arXiv:1812.06798。確定版のPDFはHTTP 502で取得できなかったため、数式番号や表番号を書かず内容だけで引くのが安全である。書誌はCrossrefで確認した。
- **これらから言える結論**: 記号の種類がq個で隣り合う記号が同じにならない制約のもとでの1記号あたりの容量は log2(q−1) ビットである。CipherFluteの差分の写像は有限の長さでもこれをちょうど達成しており、余分な冗長は一切ない。隣接同音を禁じたq種類は制約のないq−1種類とまったく同じ量を運ぶ。

### 新24　視覚暗号

Naor, M. and Shamir, A.: Visual Cryptography, Advances in Cryptology — EUROCRYPT '94, Lecture Notes in Computer Science, Vol. 950, pp. 1–12 (1995).

- DOI: 10.1007/BFb0053419
- 確認先: 著者公開の全文 https://www.wisdom.weizmann.ac.il/~naor/PAPERS/vis.pdf
- 叢書の巻番号は第950巻である（出版社の章のページと、大川さんと栃窪さんの論文の参考文献欄で一致を確認した）。
- 確定事実: 抄録が "which can decode concealed images without any cryptographic computations"、本文が "can be decoded directly by the human visual system"、"each one of them is indistinguishable from random noise"、"The original encryption problem can be considered as a 2 out of 2 secret sharing problem" と述べている。

### 新25　音響暗号と光学暗号

Desmedt, Y., Hou, S. and Quisquater, J.-J.: Audio and Optical Cryptography, Advances in Cryptology — ASIACRYPT '98, Lecture Notes in Computer Science, Vol. 1514, pp. 392–404 (1998).

- DOI: 10.1007/3-540-49649-1_31
- 続報: Desmedt, Y., Le, T. V. and Quisquater, J.-J.: Nonbinary Audio Cryptography, Information Hiding 2000, Lecture Notes in Computer Science, Vol. 1768, pp. 478–489 (2000).
- 引用時の注意: **「計算機なしに人間の感覚器だけで復号できる」と書くのは言いすぎである。** 音響の側は抄録が "To decrypt the message, one just plays two shares on a stereo system" であり再生装置を要する。光学の側は "The Mach-Zehnder interferometer is used as the decryption machine" であり干渉計を要する。装置も計算も不要という主張は視覚暗号の側に限られる。
- 引用価値: 抄録に "Also the shares are random and therefore suspect to a censor" および "shares are music or images and are not suspect to a human censor" とあり、**シェアを検閲者に怪しまれない見た目や音にすることを設計目標として明示している。偽装の動機の先例である。**
- 本文は出版社が有料であり取得できなかった。判定は抄録の記述に基づく。

### 新26　視覚復号型秘密分散法によるパスワードの分散管理

大川直也, 栃窪孝也: 視覚復号型秘密分散法を用いたパスワードの分散管理の提案, 情報処理学会論文誌デジタルプラクティス, Vol. 7, No. 2, pp. 35–50 (2026年4月15日発行、受付2025年6月22日、採録2026年1月13日).

- 確認先: https://ipsj.ixsq.nii.ac.jp/record/2009100/files/IPSJ-TDP0702007.pdf
- **用途がCipherFluteのハートのカードとほぼ同じで、日本語の査読誌であり、発行が2026年4月である。引用しないという選択は取れない。**
- 確定事実: パスワードを2-of-2の視覚復号型秘密分散法で分散し、シェア画像の1枚を紙に印刷し、もう一方をOHPシートやスマートフォンで保管して重ねて復元する。復号に計算装置を一切要さない点でCipherFluteより徹底している。

### 参考　国内の音響秘密分散

徳重佑樹, 三澤裕人, 吉田文晶, 上床昌也, 岩本貢, 太田和夫: 物理的復元が容易な音響秘密分散法, 電子情報通信学会技術研究報告, Vol. 115, No. 38, IT2015-14 / EMM2015-14, pp. 75–80 (2015年5月14日発行、講演は5月22日).

- 確認先: https://ken.ieice.org/ken/paper/20150522IbAn/
- **書誌の訂正が2件ある。** 著者は6名であり、全員が電気通信大学である。CiNii Researchの書誌が3名しか登録していないため、そちらを写すと岩本貢さんと太田和夫さんが落ちる。
- **内容の訂正がある。** 提案手法は復号に波の干渉を用いない。著者抄録は「これは，復号に音の干渉を用いたためであり」（既存研究の問題点）と「復号に波の干渉を用いない，新しい音響秘密分散法を提案する」と述べている。英語抄録も "which does not use wave interference but is based on frequency dividing" である。
- 完全秘匿を意図的に捨てている。「我々は完全秘匿を達成することを目的とせず，復号者の聴覚能力で秘密音源の情報が理解できないことを規準とした新たな安全性を定義し」と述べているため、視覚暗号と同列の情報理論的に安全な方式として扱うと誤りになる。
- 対比として使える。徳重らは音響秘密分散を実空間で本当に復元できるようにするために情報理論的な安全性を捨てたのに対し、CipherFluteは情報理論的な安全性を保ったまま読み出しに計算装置を要求するという、ちょうど逆の取引をしている。

## 優先度5　余裕があれば入れる（10件）

### 新2　Blowholeの著者による位置づけ直し

Tejada, C. E.: Print-and-Play: 3D-printed Interactive Objects Without Assembly or Calibration, Extended Abstracts of ACM CHI 2020, pp. 1–6 (2020). DOI 10.1145/3334480.3375025

### 新5　管楽器の形状最適化と逆問題（openwind）

Ernoult, A., Vergez, C., Missoum, S., Guillemain, P. and Jousserand, M.: Woodwind instrument design optimization based on impedance characteristics with geometric constraints, J. Acoustical Society of America, Vol. 148, No. 5, pp. 2864–2877 (2020). DOI 10.1121/10.0002449

- 関連: Ernoult, A., Chabassier, J., Rodriguez, S. and Humeau, A.: Full waveform inversion for bore reconstruction of woodwind-like instruments, Acta Acustica, Vol. 5, Article 47 (2021). DOI 10.1051/aacus/2021038
- 道具そのものを主題とするもの: Forum Acusticum 2023, pp. 4873–4876. DOI 10.61782/fa.2023.0233
- なお demakein（Paul Francis Harrison、http://www.logarithmic.net/pfh/design ）は査読論文の裏づけをまったく持たない。学術的先行性の主張には使えないが、デジタルファブリケーションの査読者には広く知られている。

### 新6　印刷した笛の音高精度

Dabin, M., Narushima, T., Beirne, S., Ritz, C. and Grady, K.: 3D Modelling and Printing of Microtonal Flutes, Proc. NIME 2016, pp. 286–290 (2016).

- 確認先: https://nime.org/proc/nime2016_dabin/
- 確定事実（原典の表1と本文で確認済み）: リコーダー1が+6から+34セント（内訳は+34, +23, +24, +14, +16, +6）、リコーダー2が−40から+1セント、指孔2個をやすりで手修正した版が−13から+14セントである。将来目標は "no more than a five cent error so that manual adjustments are not needed" である。
- 関連: Ritzらは既存の数理モデルによる指孔位置の解が通常30セント程度の精度であると述べている（SPIE Newsroom 2015）。100セント刻みという粗い量子化を必然として説明する材料になる。

### 新15　音でデータを送る実装

Gerganov, G.: ggwave（オープンソースソフトウェア）. https://github.com/ggerganov/ggwave

- 4.5キロヘルツの帯域に96個の等間隔の周波数を並べる多周波の周波数偏移変調に、Reed–Solomon符号による訂正を組み合わせている。

### 新16　AnisoTag

Ma, Z., Zhou, H. and Zhang, W.: AnisoTag: 3D Printed Tag on 2D Surface via Reflection Anisotropy, Proc. ACM CHI 2023.

- 確認先: arXiv版 https://arxiv.org/pdf/2301.10599
- **引用の要点**: 本文が「同寸のタグでAnisoTagは51ビット、LayerCodeは25ビット、acoustic barcodeは40ビットを符号化する」と三者を比較している。寸法は53.98×85.6ミリメートル（クレジットカードと同寸）である。

### 新23　鍵の音から刻みを推定する攻撃

Ramesh, S., Xiao, R., Maiti, A., Lee, J. T., Ramprasad, H., Kumar, A., Jadliwala, M. and Han, J.: Acoustics to the Rescue: Physical Key Inference Attack Revisited, Proc. 30th USENIX Security Symposium (2021).

- 確認先: https://www.usenix.org/conference/usenixsecurity21/presentation/ramesh
- 先行: Ramesh, S., Ramprasad, H. and Han, J.: Listen to Your Key: Towards Acoustics-based Physical Key Inference, Proc. HotMobile 2020, pp. 3–8. DOI 10.1145/3376897.3377853
- 確定事実: 75本の鍵について音響だけで候補を平均約75パーセント削減し、映像と併用すると75本のうち6本で候補を10本未満に絞れた。

### 造形物への情報埋め込みで秘密分散に言及した唯一の例

Jiang, W., Yu, D., Wang, C., Sarsenbayeva, Z., van Berkel, N., Goncalves, J. and Kostakos, V.: Near-infrared Imaging for Information Embedding and Extraction with Layered Structures, ACM Trans. Graphics, Vol. 42, No. 1, pp. 1–26 (2022). DOI 10.1145/3533426

- 確認先: 全文 https://nielsvanberkel.com/files/publications/tog2023a.pdf
- 要旨の末尾で応用として「チップを使わない情報の埋め込み、物理的な秘密分散、3Dプリントの評価、ステガノグラフィ」を明示的に挙げている。**「造形物への情報埋め込みの分野で秘密分散への言及が皆無である」と書くと誤りになる。**

### 造形物への情報埋め込みで脅威モデルを持つ唯一の例

Wang, C., Wang, J., Zhou, M., Pham, V., Hao, S., Zhou, C., Zhang, N. and Raviv, N.: Secure Information Embedding in Forensic 3D Fingerprinting, arXiv:2403.04918 (2024年、2025年2月改訂).

- 確認先: https://arxiv.org/abs/2403.04918
- 符号理論的な土台: Wang, C., Sima, J. and Raviv, N.: Break-Resilient Codes, IEEE Trans. Information Theory (2026年早期公開). DOI 10.1109/tit.2026.3708787、プレプリントは arXiv:2310.03897
- **「この分野で脅威モデルを明示したのは我々が初めてである」という書き方は成立しない。** 目的が正反対（追跡不能な偽造品の製造を防ぐ）なので主張自体は衝突しない。

### 管の音響が安全性の系を欺く例

Ahmed, S., Wani, Y., Shamsabadi, A. S., Yaghini, M., Shumailov, I., Papernot, N. and Fawaz, K.: Tubes Among Us: Analog Attack on Automatic Speaker Identification, Proc. 32nd USENIX Security Symposium (2023).

- 確認先: https://www.usenix.org/conference/usenixsecurity23/presentation/ahmed 、プレプリントは arXiv:2202.02751
- Printoneを引用している。人が管を通して話すだけで話者識別の機械学習模型に対して他人になりすませる。

### 幾何が共鳴位置を決めて二進符号になる例

Zhou, Y., Fan, J., Huang, J. and Wang, B.: Passive underwater acoustic barcodes using Rayleigh wave resonance, J. Applied Physics, Vol. 131, No. 12 (2022年3月22日). DOI 10.1063/5.0086290

- 確認先: プレプリント https://arxiv.org/pdf/2107.13860
- 同趣旨の中国特許3件がある（CN113009408B、CN113359137B、CN113359138B、上海交通大学）。請求項の中国語原文は未確認である。

### 偽装の効果に関する外部証拠（賛否の両方を引く）

- Johnston, R. G.: Tamper-Indicating Seals for Nuclear Disarmament and Hazardous Waste Management, Science & Global Security, Vol. 9, pp. 93–112 (2001). DOI 10.1080/08929880108426490　封印120種類すべてが熟練者1人あたり平均5分未満、平均55ドルで破られた。
- Appel, A. W.: Security Seals on Voting Machines: A Case Study, ACM Trans. Information and System Security, Vol. 14, No. 2, Article 18 (2011). DOI 10.1145/2019599.2019603　ピッキング未経験から40ドル未満の工具と数時間の練習で錠を平均13秒で開け、法廷で全封印の脱着を45分未満で実演した。
- Wolfe, J. M., Horowitz, T. S. and Kenner, N. M.: Rare items often missed in visual searches, Nature, Vol. 435, pp. 439–440 (2005). DOI 10.1038/435439a　標的の出現率が低いほど見落としが劇的に増える。偽装を支える側の証拠である。
- Crawford, V. P. and Iriberri, N.: Fatal Attraction: Salience, Naivete, and Sophistication in Experimental "Hide-and-Seek" Games, American Economic Review, Vol. 97, No. 5 (2007). DOI 10.1257/aer.97.5.1731　隠す側の選択が体系的に予測されうる。反証側の証拠である。

### 音響チャネルに秘匿を求めない立場の先行

- Halevi, T. and Saxena, N.: On pairing constrained wireless devices based on secrecy of auxiliary channels: the case of acoustic eavesdropping, Proc. ACM CCS 2010, pp. 97–108. DOI 10.1145/1866307.1866319
- Putz, F., Álvarez, F. and Classen, J.: Acoustic integrity codes: secure device pairing using short-range acoustic communication, Proc. ACM WiSec 2020, pp. 31–41. DOI 10.1145/3395351.3399420

### 無電源物体に符号を固定して市販端末で読む国内の研究

- Yamanaka, S., Ta, T. D., Tsubouchi, K., Okuya, F., Tsushio, K., Kato, K. and Kawahara, Y.: SheetKey: Generating Touch Events by a Pattern Printed with Conductive Ink for User Authentication, Proc. Graphics Interface 2020 (2020). DOI 10.20380/GI2020.45
- 池松香, 加藤邦拓: DuoTouch: Passive Two-Footprint Attachments Using Binary Sequences to Extend Touch Interaction, Proc. ACM CHI 2026 (2026). DOI 10.1145/3772318.3790411　前身は UIST Adjunct 2025（DOI 10.1145/3746058.3758444）
- Sugiyama, H., Lee, H., Fujino, H., Kuwana, M., Dogan, M. D., He, L. and Narumi, K.: Weaving and Disguising Infrared Markers toward Invisible Textile Interaction, Extended Abstracts of ACM CHI 2026 (2026). DOI 10.1145/3772363.3799013　偽装を独立した設計課題として分解し、不可視性と可読性を評価している。

### 端補正の国内の一次文献

吉川茂: 正倉院尺八吹奏時の歌口端補正長さの推定, 情報処理学会研究報告 音楽情報科学, 2011-MUS-89, No. 1, pp. 1–5 (2011年2月4日). https://ipsj.ixsq.nii.ac.jp/records/72682

- f = A/(L+e) の e が音響学の確立した概念であり、国内の情報処理学会研究報告に一次文献があることを示せる。

### 暗号資産の鍵管理の物理的隔離（国内の直近の共通語彙）

須賀祐治: Virtual Vaults: A Key Management Model for Both Physical and Virtual Isolation in Cryptoasset Backup Operations, 情報処理学会研究報告 コンピュータセキュリティ, 2026-CSEC-113, No. 16, pp. 1–7 (2026年5月21日). https://ipsj.ixsq.nii.ac.jp/records/2009634

### 人工物メトリクス（日本語圏の語彙での位置づけ説明の相手）

藤川真樹, 實川康輝, 渕真悟: マルチモーダル人工物メトリクスの研究（合成樹脂製品への適用）, 産業応用工学会論文誌, Vol. 5, No. 2, p. 52 (2017). https://www.jstage.jst.go.jp/article/jjiiae/5/2/5_52/_article/-char/ja/

- 会議版はコンピュータセキュリティシンポジウム2016論文集, 第2分冊, pp. 343–348 (2016).
- 合成樹脂製品を対象とし、カード形という形状までCipherFluteのカード実装と一致する。松本勉さんらのナノ人工物メトリクス（Scientific Reports 2014、DOI 10.1038/srep06142）より具体的で近い。

### モデル共有基盤の先行実装（工作面の新規性を主張しないために引く）

- Daehnert, J. (PhoneDesigner): Flat Pocket Whistle, Printables model 495173 (2023年公開、最終更新2026年3月28日). https://www.printables.com/model/495173-flat-pocket-whistle　厚さ3ミリメートル、43×22ミリメートル、いいね12,926件、ダウンロード97,000件、実作報告2,965件。上下の壁厚が0.6ミリメートルしかないので第一層の品質が決定的だと記述している。
- dp makes: Whistle Pan flute, MakerWorld model 13026 (2023年8月8日公開). https://makerworld.com/en/models/13026-whistle-pan-flute　長さの異なるフィップル笛を一列に融合し、サポート材なしで平置き印刷する。両基盤合計で約10万ダウンロードである。

### 特許（本文で触れるかどうかは判断による）

- US4821670A: Whistle（発明者 Ronald L. Foxcroft、出願人 Fortron Inc.、出願1987年8月7日、登録1989年4月18日）https://www.freepatentsonline.com/4821670.html　請求項1が「単一のホイッスル本体の中に少なくとも3個のフィップル型ホイッスル要素を持ち、少なくとも2つの気柱の長さが異なり、3要素に共通の吹き口を持つ」。従属請求項9は最長室と最短室の差を最短室長の約5から10パーセントとする。
- US5113784: Multi-tone whistle（発明者・出願人 Randall A. Forselius、登録1992年5月19日）https://www.freepatentsonline.com/5113784.html　融合した複数の共鳴室から、指で孔を塞いだ室だけを選択的に鳴らす。
- US10147410B2: Toot suite whistle pack（出願人 Thoroughbred Kids LLC、登録2018年12月4日）https://www.freepatentsonline.com/10147410.html　請求項2が「その信号特性が受信され、吹かれたホイッスルを識別するために用いられる」、請求項7が「音の特性は音高、音質、音量、持続時間のうち1つ以上を含む」。
- US11151848B2: Determining opening of portals through acoustic emissions（出願人 Kali Care, Inc.、登録2021年10月19日）https://www.freepatentsonline.com/11151848.html　元データを符号化して閉鎖材の降伏強度の逐次的な不均一さとして表し、破断音がそれを担う。
- US9912477B2: Using everyday objects as cryptographic keys（発明者 Jeffrey Robert Hoy、出願人 International Business Machines Corporation、登録2018年3月6日）https://www.freepatentsonline.com/9912477.html　機構は正反対（物体が偶然もつ個性から鍵を生成する）。明細書にsound、audio、acoustic、whistle、blow、pitch、frequencyはいずれも現れない。**「日用品を暗号鍵にする」という言い回しを論文で使うとこの特許が想起されるため、区別を明示する必要がある。**
### 日本国特許2件　請求項の原文を確認した（2026年7月30日追記）

**JP6537049B2「３次元造形物に所望の情報を付加するための方法及びプログラム」**

出願人は**学校法人幾徳学園**（神奈川工科大学を設置する法人、識別番号391022614）、発明者は上平員丈さんと鈴木雅洋さんである。出願は2014年1月6日、**優先権の基礎は特願2013-188426（2013年9月11日出願）であり、実際の優先日は2013年9月11日である。** 登録は2019年7月3日、公開番号はJP2015077775A、国際特許分類はB29C 67/00である。**権利は現在も有効である**（2026年7月30日に特許情報プラットフォームで確認）。

書誌は特許情報プラットフォームの特許願で確認した。**Google Patentsの日本語ページは出願人を「学校法人育徳学園」と表示するが、これは誤りである。正しくは「学校法人幾徳学園」である。** 請求項の原文は https://patents.google.com/patent/JP6537049B2/ja で確認した。

なお審査の経緯として、2017年11月21日に第29条第1項等（新規性の欠如）を理由とする拒絶理由通知を受け、補正と意見書を経ても2017年12月26日に拒絶査定となり、査定不服審判（2018-003866）を請求して、前置審査でも拒絶が維持されたのち、審判を経て2019年4月2日に特許査定となっている。**下に引く請求項1の細かい限定は、この審査の過程で追い込まれて入ったものと考えられる。** 狭い請求項でようやく成立した特許である。

請求項1は次のとおりである。「３次元造形装置で造形される３次元造形物に所望の情報を付加するための方法であって、所望の３次元造形物を造形するための３次元形状データを取得するステップと、所望の情報を表すための形状が前記３次元造形物に付加されるように前記３次元形状データを加工するステップとを含み、前記３次元形状データを加工するステップは、**前記所望の情報を表すための形状を複数の要素に分割するステップと、前記複数の要素を前記形状を含む平面の法線方向に分散配置して３次元パターンを生成するステップと**、前記３次元パターンが、３次元造形物の内部に、その物性が３次元パターンが形成されない場所における３次元造形物の内部の物性と異なる領域として形成されるように前記３次元形状データを加工するステップとを含む、方法。」

請求項6が「前記３次元造形物の内部と物性が異なる前記領域は、中空領域として形成される」であり、請求項1の従属項である。課題は3次元形状データの違法な複製に対する著作権侵害の立証であり、請求項7が著作権情報を明示している。

**評価。** 請求項1は「情報を表す形状を複数の要素に分割し、その形状を含む平面の法線方向に分散配置する」ことを構成要件としている。CipherFluteは管の長さで音の高さを決めるのであって、この分割と法線方向への分散配置を行わない。したがって請求項1の構成要件を満たさないと考えられる。中空領域を扱う請求項6も請求項1の従属項なので同じである。ただし最終的な判断は弁理士による。

**注意。** 出願人の表記について、Google Patentsの日本語の頁は「学校法人育徳学園」と表示するが、神奈川工科大学を設置する法人は「学校法人幾徳学園」である。英語表記はいずれも IKUTOKU GAKUEN である。**論文に書くなら特許情報プラットフォームで正式な表記を確認するのが安全である。**

**JP5620594B1「３Ｄプリンタで作製された三次元造形物、三次元造形物を用いた情報伝達システム」**
出願人と発明者はいずれも丸井智敬さん、出願は2014年1月31日、登録は2014年11月5日である。確認先は https://patents.google.com/patent/JP5620594B1/ja である（末尾はB2ではなくB1であり、B2は存在しない）。**権利は消滅している**（2026年7月30日に特許情報プラットフォームで確認）。ただし先行技術としての価値は権利の存否と無関係である。

請求項1は次のとおりである。「３Ｄプリンタで作製された三次元造形物であって、該三次元造形物は**３Ｄプリンタで作製された他の物体と結合する結合部**を具備し、**該結合部に暗号またはコードが積層造形によって配設**されていて、かつ、前記の暗号またはコードが、**結合された状態で解読できるよう前記結合部で分離され再結合される**積層造形で配設された暗号またはコードである、三次元造形物。」

**評価。** 請求項1は「結合部を具備し、その結合部に積層造形で暗号またはコードが配設されている」ことを構成要件とする。CipherFluteの2枚そろって初めてハートが現れるカードは、余白どうしを向かい合わせに並べるだけで結合部を持たず、符号は音であって結合部に配設された暗号やコードではない。したがって構成要件を満たさないと考えられる。ただし「2つそろって初めて解読できる造形物」という発想の重なりは実在するので、関連研究として一文触れる価値はある。

**両方に共通する留保。** 研究発表そのものは特許権の効力の外にある（日本の特許法69条1項が試験または研究のための実施を定めている）。ここでの評価は権利侵害の判断ではなく、学術的な先行技術としての距離を測るためのものである。

## 自己引用の候補

栗原一貴, 板谷あかり, 植村あい子, 北原鉄朗: Picognizer: 電子音の検出および認識のためのJavaScriptライブラリ, WISS 2017. https://www.wiss.org/WISS2017Proceedings/oral/17.pdf

- 再生ごとの音響的変動が小さい電子音を、動的時間伸縮法などのテンプレートに基づくパターンマッチングで検出し認識するJavaScriptライブラリである。CipherFluteの復号ページがWebブラウザで音の高さを読む設計はこの延長線上にあるため、自己引用として明示するとよい。

## 現行の参考文献のうち訂正が必要なもの

| 現行の記述 | 訂正 |
| --- | --- |
| Blowholeのページ範囲を pp. 131–137 としている | 予稿集のファイル名は `gi2018-18.pdf` である。ページ範囲は資料によって131–137と122–128の両方が流通しているため、DOI 10.20380/GI2018.18 を併記するのが安全である。なお `gi2018-16.pdf` はFittsの法則に関する無関係な論文であり、番号を誤ると存在しない引用になる |
| AirCodeの容量を本文で「500ビット超」と書いている | 原典は「a 5cm×5cm tag stores about 500 bits」であり、**約500ビット**である |
| Acoustic Barcodesの容量を「数十bit」としている | 誤り訂正後の実効データは24ビット符号で12ビット（4096通り）である。誤り訂正の符号は拡張ゴレイ符号、短縮(15,7)BCH符号、短縮(7,4)ハミング符号である（Reed–Solomon符号は将来の提案として言及されているだけである） |
| ITU-T勧告の発行年（V.21とQ.23が1988年、T.30が2005年） | メインプロジェクトのcosenseの2026年7月29日の記録が指摘しているとおり、投稿前に一次資料で確認するのが安全である。なお周波数スロット符号の技術的出典まで遡るなら Schenker, L.: Pushbutton Calling with a Two-Group Voice-Frequency Code, Bell System Technical Journal, Vol. 39, No. 1, pp. 235–255 (1960) がある（https://archive.org/details/bstj39-1-235 で確認済み） |
