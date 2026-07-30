# 音でデータを送る通信方式の歴史と現在

調査担当の切り口は「空気中の音や電話回線の音声帯域を使ってデータを送る技術の系譜」である。電話回線のモデム、ファクシミリの手順、押しボタン信号、音響カプラ、カセットテープへの記録、放送による配布、超音波ビーコン、可聴音による端末間通信、音による機器設定、船舶と航空の音響信号までを対象とした。書誌情報はITUの勧告ページ、Crossrefのdoi登録レコード、J-STAGE、CiNii Research、著者本人の業績ページ、学会の予稿集PDF、公的機関の一次文書に当たって確認した。

## この切り口の要約

音でデータを送る技術は1960年前後に電話網のなかで体系化された。Schenkerが1960年に示した二群の音声周波数による押しボタン発信の符号は、可聴域に離散的な周波数の集合を定めて記号を割り当て、受信側は周波数の同定だけで復号する。これがCipherFluteの半音刻みスロットの直接の先祖であり、のちにITU-T勧告Q.23になった。同じ時期に周波数偏移変調のモデムがV.21として、ファクシミリの手順がT.30として整い、音声帯域は汎用の搬送路になった。1970年代には音響カプラが普及し、1975年にはカセットテープに音として計算機のデータを固定するKansas City標準が定まり、1984年にはイギリスの放送局が番組の電波でプログラムを音として配った。音の波形を物理媒体や放送に固定して配る発想はこの時期に出そろっている。

2000年代からは空気中の可聴音そのものを通信路として扱う研究が始まった。LopesとAguiarは空中音響通信を正面から扱い、2002年にはピアノとクラリネットと鐘という音響楽器を送信機に用いている。その後は音響OFDM、チャープ信号、音響電子透かしが加わり、2010年代には超音波ビーコンが商用化された。この系譜のなかでCipherFluteは、送信機が形状として固定され書き換えができず、電源を持たず、人間の息だけで駆動するという極端な特殊例に位置づく。周波数スロットへの記号割り当てと誤り訂正という符号の組み合わせはggwaveなどが既に採っているため、新規性はそこに置かないほうがよい。

## 新規性への脅威が大きい文献

### 1. Aerial communications using piano, clarinet, and bells

- 著者: N. Domingues, J. Lacerda, P. M. Q. Aguiar, C. V. Lopes
- 発表: 2002 IEEE Workshop on Multimedia Signal Processing (MMSP), pp. 460-463, 2002年
- 確認先: https://doi.org/10.1109/MMSP.2002.1203345 （Crossrefのdoi登録レコードで題名、著者、会議名、ページを確認した）
- 著者本人の業績ページでも確認した: https://ics.uci.edu/~lopes/publications.html

内容の要約を述べる。この論文は、LopesとAguiarが2001年から進めていた空中音響通信の研究の一環であり、電子的に合成した搬送波ではなく、ピアノとクラリネットと鐘という音響楽器が出す実際の楽音を伝送の媒体として使うことを扱っている。空中音響通信の研究群のなかでは、通信路の設計を「人が聞いても不自然でない音」に寄せる方向の初期の試みにあたる。同じ著者らはWASPAA 2001で空中音響通信の基本方式を、IEEE Pervasive Computing 2003で音響モデムの全体像を発表しており、この楽器の論文はその中間に位置する。なおIEEE Xploreと出版社系の要旨ページはいずれも取得できず、変調方式の細部や達成ビットレートまでは確認できていない。

CipherFluteとの関係を述べる。CipherFluteは笛という音響楽器が出す楽音の高さを記号として使う。楽音を通信の記号として使うという着想そのものは、この論文がすでに2002年に提示している。したがってCipherFluteが「楽器の音でデータを運ぶ」という水準で新規性を主張すると、この論文と正面から衝突する。逆に言えば、この論文の送信機は演奏者または機構が任意の音列を出す能動的な装置であり、形状が符号を固定してはいない。

脅威の度合いは「高」と判定する。理由を述べる。楽音の高さを符号の語彙に使うという中核の着想が20年以上前に先行しており、CipherFluteの新規性をそこに置くことができなくなるからである。差分は、送信機が受動的な造形物であって符号が形状として不可逆に固定される点、および日用品への偽装と秘密分散という応用の枠組みにあると明示する必要がある。

### 2. ggwave（データ・オーバー・サウンドの実装）

- 著者: Georgi Gerganov（オープンソース実装、継続的に開発）
- 発表: ソフトウェアリポジトリ（学術発表ではない）
- 確認先: https://github.com/ggerganov/ggwave

内容の要約を述べる。ggwaveは音でデータを送るための小さなライブラリであり、多周波の周波数偏移変調を用いる。周波数間隔は46.875ヘルツで、可聴用のプロトコルは1875ヘルツ、超音波用のプロトコルは15000ヘルツを基準周波数とし、4.5キロヘルツの帯域に96個の等間隔の周波数を並べる。データは4ビットずつに分割され、各片が特定の周波数に割り当てられ、6つの音を同時に鳴らして1回あたり3バイトを送る。復調の頑健性を上げるためにReed–Solomon符号を用いる。用途としては機器のペアリング、音のQRコード、連絡先の交換、認可の受け渡しなどが挙げられている。2025年に話題になったGibberLinkという、会話する人工知能どうしが音の通信に切り替える実演も、このライブラリを使っている。

CipherFluteとの関係を述べる。CipherFluteの符号層、すなわち周波数のスロットに記号を割り当て、Reed–Solomon符号で訂正するという設計は、ggwaveの設計とほぼ同一である。異なるのは、ggwaveがスピーカーから任意の音列を出すのに対し、CipherFluteは造形された笛の並びが音列を固定している点である。

脅威の度合いは「中」と判定する。理由を述べる。符号の構成そのものに新規性がないことを明確に示す資料であり、論文が符号設計を新規性として書いていると弱くなる。ただしCipherFluteの主張の中心が物理層と運用にある限り、位置づけを整理するための引用で足りる。

### 3. HAPADEP: Human-Assisted Pure Audio Device Pairing

- 著者: Claudio Soriente, Gene Tsudik, Ersin Uzun
- 発表: Information Security (ISC 2008), Lecture Notes in Computer Science, pp. 385-400, 2008年
- 確認先: https://doi.org/10.1007/978-3-540-85886-7_27 （Crossrefのdoi登録レコードで題名、著者、書名、ページを確認した）

内容の要約を述べる。この論文は、共通の鍵も既存の無線路も持たない二台の機器が、音だけを使って鍵素材を交換し、人間が聞いて確認することで中間者攻撃を排除する方式を提案している。鍵の転送そのものを音で行い、その正しさの検証も人間の聴覚に委ねる点が特徴である。前段の研究として同じグループのLoud and Clearがあり、そちらは音声化した検証文を人間に読ませて認証する。

CipherFluteとの関係を述べる。CipherFluteは暗号資産の復元用情報という鍵素材を音で運ぶ。鍵素材を音の通路で運ぶこと自体はこの研究がすでに行っている。ただしHAPADEPは二台の電子機器のあいだの一時的な通路であり、秘密が物体の形として保管されるわけではない。

脅威の度合いは「中」と判定する。理由を述べる。「鍵を音で運ぶ」という応用が先行しているため、CipherFluteはその応用ではなく「鍵を形として保管し、必要なときだけ音として取り出す」という保管の側面に主張を寄せる必要がある。

### 4. On the Privacy and Security of the Ultrasound Ecosystem

- 著者: Vasilios Mavroudis, Shuang Hao, Yanick Fratantonio, Federico Maggi, Christopher Kruegel, Giovanni Vigna
- 発表: Proceedings on Privacy Enhancing Technologies, vol. 2017, no. 2, pp. 95-112, 2017年
- 確認先: https://doi.org/10.1515/popets-2017-0018 （Crossrefのdoi登録レコードで題名、著者、巻号ページ、年を確認した）

内容の要約を述べる。この論文は、超音波を使って端末どうしや広告と端末を結びつける商用の生態系を体系的に調べ、その設計上の弱点を示している。超音波の信号は誰でも受信でき、記録して再生すれば容易に複製できるため、認証や課金の根拠にすると危険であることを実証的に述べている。あわせて、利用者の同意なしに視聴履歴を追跡できてしまう privacy の問題を扱っている。

CipherFluteとの関係を述べる。CipherFluteは「音や物体の層には暗号学的な秘匿の力はまったく無い」と宣言している。その宣言を裏づける先行研究として、この論文は最も的確である。音響の通路には秘匿も認証も期待できないという結論が独立に得られている。

脅威の度合いは「中」と判定する。理由を述べる。脅威モデルの主張が独自のものではなく先行研究に沿ったものであることを示すため、引用しないと「既知の事実を発見として書いている」と見られる危険がある。逆に引用すれば主張の裏づけとして機能する。

### 5. Pushbutton Calling with a Two-Group Voice-Frequency Code

- 著者: L. Schenker
- 発表: Bell System Technical Journal, vol. 39, no. 1, pp. 235-255, 1960年1月
- 確認先: https://archive.org/details/bstj39-1-235 （原誌の走査版で題名、著者、巻号ページ、年を確認した）
- 関連する標準: ITU-T勧告 Q.23 "Technical features of push-button telephone sets"（現行版は1988年11月版）https://www.itu.int/rec/T-REC-Q.23/en

内容の要約を述べる。この論文は、電話機の押しボタンから交換機へ数字を送るために、低群と高群それぞれから1つずつ周波数を選んで同時に鳴らす符号を提案している。可聴域のなかに離散的な周波数の集合を定め、その組み合わせに記号を割り当て、受信側は周波数の同定だけで記号を復元する。音声との誤検出を避けるために周波数の選び方が慎重に設計されている。この方式は後に世界中の電話網に採用され、ITU-T勧告Q.23として標準化された。

CipherFluteとの関係を述べる。CipherFluteは1480ヘルツから2960ヘルツまでを半音刻みで13のスロットに区切り、笛1本に1つの記号を割り当てる。周波数の離散集合を語彙とし、周波数の同定だけで復号するという構成は、この符号と本質的に同じである。相違は、CipherFluteが1回に1つの周波数だけを出す点と、周波数の選び方が音楽の半音階に従っている点である。

脅威の度合いは「中」と判定する。理由を述べる。周波数スロットによる符号化の原型として必ず引用すべき文献であり、これを引かずに「周波数を語彙にする」ことを新しく述べると、電話技術の常識を知らないと受け取られる。現在の論文はQ.23を挙げているが、その技術的な出典であるこの論文まで遡ると位置づけが明確になる。

### 6. 空中音波通信技術とその応用（解説）

- 著者: 西村明（東京情報大学）
- 発表: 日本音響学会誌, 第77巻, 第6号, pp. 390-395, 2021年
- 確認先: https://www.jstage.jst.go.jp/article/jasj/77/6/77_390/_article/-char/ja （J-STAGEの記事ページで題名、著者、巻号ページ、発行年、doiを確認した）

内容の要約を述べる。この解説は、空気中を伝わる音でデータを送る技術を、音響電子透かしの系統と音響モデムの系統に分けて整理している。振幅偏移変調、周波数偏移変調、位相偏移変調、直交振幅変調、直交周波数分割多重、スペクトル拡散といった変調方式の使い分けを述べ、到達距離、伝送速度、雑音耐性、聴感上の目立たなさのあいだの折り合いを論じている。応用としては、放送や館内放送への情報重畳、多言語字幕、災害情報の伝達、来店の検知などを挙げる。参考文献の一覧が空中音響通信の主要文献をよく網羅しており、この分野の入口として使える。

CipherFluteとの関係を述べる。CipherFluteは空中を伝わる音でデータを読む方式であるから、この分野の全体像を示す解説として引用する価値が高い。特に、既存の方式がすべて能動的なスピーカーを前提にしていることを、この解説を根拠に述べられる。

脅威の度合いは「中」と判定する。理由を述べる。日本語で書かれた数少ない体系的な解説であり、これを引かずに空中音響通信を語ると調査不足に見える。内容そのものはCipherFluteの主張を脅かさない。

### 7. Aerial Acoustic Communication（書籍の章）

- 著者: Rong Zheng, Chao Cai
- 発表: Acoustic Sensing on Commodity Devices and its Applications, Wireless Networks シリーズ, Springer Nature Switzerland, pp. 63-76, 2025年
- 確認先: https://doi.org/10.1007/978-3-031-96875-4_4 （Crossrefのdoi登録レコードで章題、著者、書名、シリーズ、出版社、ページ、年を確認した）

内容の要約を述べる。市販の機器に載っているマイクとスピーカーを使った音響センシングと音響通信をまとめた書籍の一章であり、空中音響通信を扱っている。同じ著者らはチャープ信号を用いた空中音響通信の一連の論文をIEEE Transactions on Mobile ComputingやIEEE Transactions on Vehicular Technologyに発表しており、その知見を整理した位置づけと考えられる。なお出版社のページは認証の壁で取得できず、章の要旨の本文までは確認できていない。

CipherFluteとの関係を述べる。空中音響通信の最新の総説にあたるため、この分野の現在地を示すために引用できる。

脅威の度合いは「中」と判定する。理由を述べる。分野の総説を引かないままでは位置づけの議論が弱くなるためである。内容がCipherFluteの主張を直接脅かすわけではない。

### 8. Encoding Data by Frequency Modulation of a High-Low Siren Emitted by an Emergency Vehicle

- 著者: Akira Nishimura
- 発表: 2014 Tenth International Conference on Intelligent Information Hiding and Multimedia Signal Processing (IIH-MSP), pp. 255-259, 2014年8月
- 確認先: https://doi.org/10.1109/IIH-MSP.2014.70 （Crossrefのdoi登録レコードで題名、著者、会議名、ページ、年を確認した）

内容の要約を述べる。この論文は、緊急車両が鳴らす高低二音のサイレンという既存の発音に、周波数変調でデータを重ねる方式を提案している。もともと社会的な意味を持って鳴っている音を、そのまま符号の担体として使うところに特徴がある。聞き手には従来どおりのサイレンに聞こえながら、受信機は付加情報を取り出せる。

CipherFluteとの関係を述べる。CipherFluteも「笛の音」という、それ自体が用途を持つ音を符号の担体にしている。既存の発音体の音高を操作して情報を載せるという発想の先例として近い。ただしサイレンは電気的に駆動される能動的な発音装置である。

脅威の度合いは「中」と判定する。理由を述べる。「既存の音を符号にする」という着想の先例であり、引用して差分を述べるべきである。CipherFluteの受動性と形状固定という核心には触れない。

### 9. Kansas City標準（カセットテープへのデータ記録方式）

- 制定: BYTE誌が招集した規格検討会（1975年11月7日から8日、アメリカ合衆国ミズーリ州カンザスシティ）、結果は同誌1976年2月号に掲載
- 確認先: https://www.swtpc.com/mholley/AC30/KansasCityStandard.html （原文書を再録した頁で、招集の経緯、周波数、ビットレート、フレーム構成を確認した）

内容の要約を述べる。この標準は、家庭用のカセットレコーダを計算機のデータ記録に使うための音の書式を定めている。論理の1は2400ヘルツを8周期、論理の0は1200ヘルツを4周期で表し、最大300ボーで送る。1文字はスタートビットとしての0、8ビットのデータ、2ビット以上のストップビットからなり、データブロックの前に5秒以上のマークを置く。テープの速度がふらついてもビットの時計が波形から取り出せるように、周波数が常にビットレートの整数倍になるよう設計されている。

CipherFluteとの関係を述べる。CipherFluteは物理的な物体に音の符号を固定して保存する。音の波形を物理媒体に固定して保管し、再生して読み出すという枠組みは、この標準がすでに大量に実用化している。CipherFluteとの相違は、媒体が磁性体ではなく造形物であり、書き換えができず、再生に機械も電源も要らないところにある。

脅威の度合いは「中」と判定する。理由を述べる。「音の符号を物に固定して保存する」という枠組みの先行例として最も重要であり、これを踏まえずに保管媒体としての新規性を述べると弱い。ただし読み出しに機械を必要とする点で決定的に異なる。

### 10. Dhwani: secure peer-to-peer acoustic NFC

- 著者: Rajalakshmi Nandakumar, Krishna Kant Chintalapudi, Venkat Padmanabhan, Ramarathnam Venkatesan
- 発表: Proceedings of the ACM SIGCOMM 2013 conference, pp. 63-74, 2013年8月
- 確認先: https://doi.org/10.1145/2486001.2486037 （Crossrefのdoi登録レコードで題名、著者、会議名、ページ、年を確認した）

内容の要約を述べる。この論文は、スマートフォンの標準的なスピーカーとマイクだけで近距離無線通信に相当する機能を実現する方式を示している。音響の到達範囲が短いことを利用し、さらに受信側が意図的に雑音を出して盗聴者だけを妨害する仕組みを組み込み、機密性を物理層で確保しようとする。数キロビット毎秒の伝送を達成している。

CipherFluteとの関係を述べる。音による近接通信の代表的な研究であり、CipherFluteが「音で秘密を渡す」という文脈で必ず参照される位置にある。とりわけDhwaniが物理層で機密性を作ろうとしたのに対し、CipherFluteは物理層に機密性を一切期待しないと宣言している点が対照的である。

脅威の度合いは「中」と判定する。理由を述べる。音響を安全な通路にしようとする代表的な試みであり、CipherFluteの脅威モデルの位置づけを説明するために引用が要る。ただし送信機が電子機器である点で系統が異なる。

### 11. Acoustic modems for ubiquitous computing / Audio Networking: The Forgotten Wireless Technology

- 著者と発表: C. V. Lopes, P. M. Q. Aguiar, IEEE Pervasive Computing, vol. 2, no. 3, pp. 62-71, 2003年7月。ならびに A. Madhavapeddy, D. Scott, A. Tse, R. Sharp, IEEE Pervasive Computing, vol. 4, no. 3, pp. 55-60, 2005年7月
- 確認先: https://doi.org/10.1109/MPRV.2003.1228528 および https://doi.org/10.1109/MPRV.2005.50 （いずれもCrossrefのdoi登録レコードで題名、著者、巻号ページ、年を確認した）

内容の要約を述べる。前者は空中音響通信を汎用の通信路として設計する立場から、変調方式、通信路の性質、到達距離、実装の要点を整理している。後者は、音による通信が無線技術の系譜のなかで忘れられてきたことを指摘し、機器の位置づけ、部屋の境界を越えないという性質、既存のスピーカーとマイクをそのまま使える利点を論じ、いくつかの応用を示す。CipherFluteの現行の参考文献では後者の著者が3名で書かれているが、正しくは Madhavapeddy, Scott, Tse, Sharp の4名であり、掲載は第4巻第3号の55ページから60ページである。

CipherFluteとの関係を述べる。音を通信路として使う理由づけ、すなわち壁を越えない、ペアリングが要らない、既存の機器で読めるという議論は、この2本がすでに整理している。CipherFluteが音を選ぶ理由もここに含まれる。

脅威の度合いは「中」と判定する。理由を述べる。音を選ぶ動機づけが先行研究にあるため、動機の新規性は主張できない。あわせて現行の書誌情報の誤りを直す必要がある。

### 12. Hermes: data transmission over unknown voice channels

- 著者: Aditya Dhananjay, Ashlesh Sharma, Michael Paik, Jay Chen, Trishank Karthik Kuppusamy, Jinyang Li, Lakshminarayanan Subramanian
- 発表: Proceedings of the 16th Annual International Conference on Mobile Computing and Networking (MobiCom 2010), pp. 113-124, 2010年9月
- 確認先: https://doi.org/10.1145/1859995.1860010 （Crossrefのdoi登録レコードで題名、著者、会議名、ページ、年を確認した）

内容の要約を述べる。この論文は、音声符号化器が入った携帯電話網の音声通話路という、波形が保存されない厳しい経路の上でデータを通す方式を示している。通話路が何をするか事前に分からないという前提のもとで、通話路に耐える記号の設計と適応を行う。開発途上地域でデータ通信の代わりに音声通話を使うという動機がある。

CipherFluteとの関係を述べる。CipherFluteは空気と部屋の残響と息の強さという未知の伝達特性の上で音高を読む。未知の非線形な通路の上で符号を成立させるという問題設定が共通する。CipherFluteの基準笛による正規化は、この系統の問題への素朴な対処にあたる。

脅威の度合いは「中」と判定する。理由を述べる。未知の通路に対する適応という論点の先行研究であり、基準笛の位置づけを説明するために引用すると議論が締まる。

### 13. ITU-T勧告 V.21 と T.30（電話網における音でのデータ搬送の標準）

- 標準: ITU-T Recommendation V.21 "300 bits per second duplex modem standardized for use in the general switched telephone network"（現行版は1988年11月版）
- 標準: ITU-T Recommendation T.30 "Procedures for document facsimile transmission in the general switched telephone network"（現行版は2005年9月版、初版は1988年11月版、2007年1月の追補1がある）
- 標準: ITU-T Recommendation V.23 "600/1200-baud modem standardized for use in the general switched telephone network"（現行版は1988年11月版）
- 標準: ITU-T Recommendation V.34 "A modem operating at data signalling rates of up to 33 600 bit/s for use on the general switched telephone network and on leased point-to-point 2-wire telephone-type circuits"（現行版は1998年2月版）
- 確認先: https://www.itu.int/rec/T-REC-V.21/en 、 https://www.itu.int/rec/T-REC-T.30/en 、 https://www.itu.int/rec/T-REC-V.23/en 、 https://www.itu.int/rec/T-REC-V.34/en

内容の要約を述べる。V.21は音声帯域の2つの周波数対によって毎秒300ビットの全二重通信を行う周波数偏移変調のモデムを定める。V.23は600ボーと1200ボーの非対称なモデムを定め、映像文字多重などに使われた。T.30はファクシミリの呼の確立から能力交換、訓練、画像伝送、終了までの手順を音声帯域の信号で定める。V.34は毎秒33600ビットまでの高速モデムを定め、通信路の測定と訓練の手順を含む。CipherFluteが現行の論文で挙げているV.21とT.30については、正式な題名と現行版の日付が上のとおりであることを確認した。

CipherFluteとの関係を述べる。音声帯域を汎用のデータ搬送路として標準化した系譜であり、CipherFluteが引く背景として妥当である。特にT.30の訓練手順は、通信路の状態を既知の信号で測ってから本文を送るという点で、基準笛の考え方に近い。

脅威の度合いは「低」と判定する。理由を述べる。いずれも背景として引くべき標準であって、CipherFluteの主張と競合しない。ただし勧告番号と正式題名と版の日付を正確に書く必要がある。

### 14. SilverPushの音響ビーコンに対するアメリカ連邦取引委員会の警告書

- 発行: United States Federal Trade Commission, Bureau of Consumer Protection、2016年3月17日付の見本文書
- 確認先: https://www.ftc.gov/system/files/attachments/press-releases/ftc-issues-warning-letters-app-developers-using-silverpush-code/160317samplesilverpushltr.pdf

内容の要約を述べる。この文書は、Silverpushという企業が提供する「固有の音響ビーコン」の開発キットを組み込んだアプリケーションの開発者に宛てた警告書である。この技術は、テレビの音声に埋め込まれた固有の符号を携帯端末のマイクが常時聞き取り、近くのテレビでどの番組や広告が流れているかを判定する。利用者に開示のないまま背景で動作し、視聴履歴の詳細な記録を作れることを問題としている。

CipherFluteとの関係を述べる。音響ビーコンによる符号の配布が実社会で稼働し、規制当局の関心を集めるところまで来ていたことを示す一次資料である。音の符号が誰にでも読まれてしまうという性質を、規制の観点から裏づける。

脅威の度合いは「低」と判定する。理由を述べる。CipherFluteの主張とは競合せず、音響層に秘匿がないという前提を社会的な文脈で補強する背景資料にとどまる。

## 背景として押さえるべき文献

以下は脅威の度合いを「低」と判定したものである。いずれも一次資料またはdoi登録レコードで書誌情報を確認した。

- L. Schenkerの押しボタン符号を国際標準化した ITU-T Recommendation Q.23 "Technical features of push-button telephone sets"（1988年11月版）。https://www.itu.int/rec/T-REC-Q.23/en
- C. V. Lopes, P. M. Q. Aguiar, "Aerial acoustic communications", IEEE Workshop on Applications of Signal Processing to Audio and Acoustics (WASPAA 2001), pp. 219-222。https://doi.org/10.1109/ASPAA.2001.969582
- H. Matsuoka, Y. Nakashima, T. Yoshimura, "Acoustic OFDM System and Performance Analysis", IEICE Transactions on Fundamentals, vol. E91-A, no. 7, pp. 1652-1658, 2008年。音声に並行して直交周波数分割多重の搬送波を高域に重ね、毎秒数百ビットを約3メートル届ける。https://www.jstage.jst.go.jp/article/transfun/E91.A/7/E91.A_7_1652/_article/-char/en
- H. Lee, T. H. Kim, J. W. Choi, S. Choi, "Chirp signal-based aerial acoustic communication for smart devices", IEEE INFOCOM 2015, pp. 2407-2415。https://doi.org/10.1109/INFOCOM.2015.7218629
- K. Cho, J. Choi, N. S. Kim, "An acoustic data transmission system based on audio data hiding: method and performance evaluation", EURASIP Journal on Audio, Speech, and Music Processing, 2015年。https://doi.org/10.1186/s13636-015-0053-x
- M. T. Goodrich, M. Sirivianos, J. Solis, G. Tsudik, E. Uzun, "Loud and Clear: Human-Verifiable Authentication Based on Audio", ICDCS 2006。https://doi.org/10.1109/ICDCS.2006.52
- B. Zhang, Q. Zhan, S. Chen, M. Li, K. Ren, C. Wang, D. Ma, "PriWhisper: Enabling Keyless Secure Acoustic Communication for Smartphones", IEEE Internet of Things Journal, vol. 1, no. 1, pp. 33-45, 2014年。https://doi.org/10.1109/JIOT.2014.2297998
- M. Hanspach, M. Goetz, "On Covert Acoustical Mesh Networks in Air", Journal of Communications, vol. 8, no. 11, pp. 758-767, 2013年。空気を伝わる超音波で隔離された計算機のあいだに秘密の網を作る。https://doi.org/10.12720/jcm.8.11.758-767
- M. Guri, Y. Solewicz, Y. Elovici, "MOSQUITO: Covert Ultrasonic Transmissions Between Two Air-Gapped Computers Using Speaker-to-Speaker Communication", IEEE Conference on Dependable and Secure Computing 2018, pp. 1-8。https://doi.org/10.1109/DESEC.2018.8625124
- N. Roy, H. Hassanieh, R. Roy Choudhury, "BackDoor", MobiSys 2017, pp. 2-14。可聴域外の音を通常のマイクに聞かせる非線形性の利用。https://doi.org/10.1145/3081333.3081366
- C. Cilleruelo, J. Junquera-Sanchez, L. de-Marcos, N. Logghe, J.-J. Martinez-Herraiz, "Security and privacy issues of data-over-sound technologies used in IoT healthcare devices", IEEE Globecom Workshops 2021。https://doi.org/10.1109/GCWkshps52748.2021.9682007
- H. Gupta, B. Nayak, A. Ashok, R. Pratap, "Data-Over-Sound With PMUTs", IEEE Open Journal of Ultrasonics, Ferroelectrics, and Frequency Control, vol. 2, pp. 152-161, 2022年。https://doi.org/10.1109/OJUFFC.2022.3197126
- S. Kim, H. Mun, Y. Lee, "A Data-Over-Sound Application: Attendance Book", APNOMS 2019, pp. 1-4。https://doi.org/10.23919/APNOMS.2019.8892996
- M. Stojanovic, "Recent advances in high-speed underwater acoustic communications", IEEE Journal of Oceanic Engineering, vol. 21, no. 2, pp. 125-136, 1996年。https://doi.org/10.1109/48.486787
- I. F. Akyildiz, D. Pompili, T. Melodia, "Underwater acoustic sensor networks: research challenges", Ad Hoc Networks, vol. 3, no. 3, pp. 257-279, 2005年。https://doi.org/10.1016/j.adhoc.2005.01.004
- A. X. Widmer, P. A. Franaszek, "A DC-Balanced, Partitioned-Block, 8B/10B Transmission Code", IBM Journal of Research and Development, vol. 27, no. 5, pp. 440-451, 1983年。隣り合う記号に制約を課して遷移を保証する符号の原典であり、現行の論文がすでに挙げている。https://doi.org/10.1147/rd.275.0440
- 国際海上衝突予防規則（1972年の海上における衝突の予防のための国際規則）の第34条と第35条。短音1回で右転、2回で左転、3回で後進、5回以上で疑問の表明を示し、視界制限状態では2分を超えない間隔で長音の組み合わせを鳴らす。合図の意味は規約表で決まり、送信側は固定の音を鳴らすだけである。https://www.navcen.uscg.gov/navigation-rules-amalgamated
- アメリカ連邦航空局の Aeronautical Information Manual における航法援助施設の識別。超短波全方向式無線標識や計器着陸装置の位置指示装置は、国際モールス符号による3文字の識別符号を音として送出し続ける。送信内容が固定されており、受信側は表と照合して局を同定する。https://www.faa.gov/air_traffic/publications/atpubs/aim_html/chap1_section_1.html
- The Chip Shop（イギリス放送協会のRadio 4、1984年）。番組の枠で計算機のプログラムを音として放送し、聴取者が録音して計算機に読み込ませる方式であり、オランダのBasicodeの書式が使われた。https://www.computinghistory.org.uk/det/21276/The%20Chip%20Shop%20Basicode%202/
- 日本語の音響カプラ関係の文献。岩原廉「音響カプラ」エレクトロニクス, 1973年5月（https://cir.nii.ac.jp/crid/1521699230884271488 ）、金沢真「高性能音響カプラ」National Technical Report, 1975年12月（https://cir.nii.ac.jp/crid/1520573330594441344 ）、荒木庸夫「音響カプラによるCAI遠隔端末」医学教育, 1977年（https://cir.nii.ac.jp/crid/1390282679076662528 ）。
- 日本語の可聴音データ伝送の初期文献。「可聴音を用いた4値FSKデータ伝送方式における送波システムの回路構成について」信州短期大学研究紀要, 1992年12月（https://cir.nii.ac.jp/crid/1571135651784290560 ）ならびに受波側を扱った続報, 1993年7月（https://cir.nii.ac.jp/crid/1572824501630771200 ）。可聴音で4値の周波数偏移変調を行う点でCipherFluteのスロット符号に近い発想である。
- 宮下慶多, 中原崇文, 串山久美子「物理的な発音媒体を用いた情報の可聴化システム」インタラクション2018論文集, 3A13, p. 909, 2018年。計算機の合成音ではなく物理的な発音体の振動で情報を可聴化する試みであり、造形物が音を出すことの意味を論じている。https://www.interaction-ipsj.org/proceedings/2018/data/pdf/3A13.pdf
- ヤマハの音波によるデータ伝送技術INFOSOUNDの発表（2012年6月13日）。直接スペクトル拡散により、ほとんど聞こえない形で音響の識別子をスピーカーから送り、携帯端末のマイクで受けてURLに変換する。https://archive.yamaha.com/ja/news_release/2012/12061302.html
- Googleの実験的な拡張機能Tone（2015年5月19日、Alex KauffmannとBoris Smus）。超音波の方式と押しボタン信号に基づく可聴の方式を併用して、現在のタブのURLを聞こえる範囲の計算機に配る。壁を越えず、ペアリングも宛先指定も要らないという性質を人の声にたとえて説明している。https://research.google/blog/tone-an-experimental-chrome-extension-for-instant-sharing-over-audio/
- Chirp（2011年にユニヴァーシティ・カレッジ・ロンドンの計算機科学科から独立、2020年2月にSonosが買収）。機器の初期設定、近接の検知、音響による近距離通信、電波が使えない環境での遠隔測定を用途としていた。https://audioxpress.com/news/data-over-sound-pioneer-chirp-acquired-by-sonos
- LISNR。超音波によるデータ・オーバー・サウンドを、非接触の認証と決済に使う商用サービスを提供している。https://lisnr.com/
- エヴィクサー株式会社。音響電子透かしと音響フィンガープリントを用いて、放送や館内放送から携帯端末へ情報を渡す事業を日本で行っている。劇場の多言語字幕、球団アプリ、防災放送などの導入事例がある。https://www.evixar.com/applications/
- PhonoPaper（Alexander Zolotov作）。音を画像として紙に印刷し、携帯端末のカメラで走査して音に戻す。符号が連続量であるため画像の劣化に強い。読み取りが光学である点で音響通信ではないが、「音を物の模様として固定する」系譜に属する。http://warmplace.ru/soft/phonopaper/

## 未検証のまま残ったもの

以下は存在の見当はついたものの、一次資料に到達できず書誌情報を確定できなかった。本文で引用する場合は改めて確認が必要である。

- Amazon Dash Buttonの初期設定における音による無線設定情報の受け渡し。携帯端末のスピーカーから可聴域上端の音でネットワークの認証情報を流し込んだという記述を複数の場所で見た記憶があるが、Amazonの公式文書にも技術解析記事にも到達できなかった。検索エンジンからの応答が得られない状態が続いたため断念した。
- Chromecastのゲストモードにおける超音波によるペアリング。Googleのサポート文書のうち該当すると思われる記事を取得したが、超音波の記述は含まれていなかった。別の記事番号があると考えられるが特定できていない。
- インドのGoogle Pay（旧Tez）のCash Modeにおける音響による近接決済。Googleの公式ブログの想定していたURLが404を返した。存在は強く疑われるが確認できていない。
- ToneTag（インドの音波決済事業者）、株式会社スマート・ソリューション・テクノロジーのTrustSound、Cotofure株式会社の非可聴音ソリューション。検索結果に企業サイトが現れたところまでで、各社の技術説明ページの本文を取得していない。
- 日本のマイコン雑誌の付録ソノシートによるプログラム配布。『PiO』1986年9月号の付録として「パソコンDJソノシート」が存在したという中古販売の記録は見たが、雑誌そのものや国立国会図書館の書誌に当たっていない。音をレコード盤の溝という形状として固定して配布した例であり、CipherFluteの位置づけに効くので確認する価値が高い。
- Cap'n Crunchの景品の笛が2600ヘルツを出し、電話網の制御に使われたという逸話。Ron Rosenbaumの記事（Esquire誌1971年10月号）とPhil Lapsleyの著書が一次資料にあたるが、いずれも本文に到達できなかった。物理的な笛が固定の音を出して機械を動かした唯一に近い実例であり、確認できればCipherFluteの導入として非常に強い。
- 潜水信号会社（Submarine Signal Company）による水中の鐘を使った船舶の信号（20世紀初頭）。存在は広く知られているが一次資料に当たっていない。
- 日本のポケットベルにおける押しボタン信号による文字入力。CiNii Researchで「ポケットベル 文字入力」を検索したが該当がなく、別の語での再検索が必要である。
- Bell 103型データセット（1962年）の一次仕様。ITU-T V.21に相当するアメリカの方式であるが、Bell Systemの技術参考資料に到達できていない。
- Basicodeの規格そのものの一次資料。The Chip Shopについては博物館の記録で確認できたが、オランダの放送局が定めた書式の原文は確認していない。
- 京急のKQスタンプラリーにおける音波の利用。西村の解説が参考文献として挙げているURLを開いたが403が返り、内容を確認できなかった。
- Aerial communications using piano, clarinet, and bells の要旨と技術的な細部。書誌情報はCrossrefで確定したが、変調方式、記号の設計、達成した伝送速度は確認できていない。最重要の文献であるから、図書館経由での本文入手を強く勧める。

## この切り口で見つからなかったこと

丁寧に述べる。以下はCipherFluteの新規性の主張の根拠になる。

第一に、送信機が電源も可動部も持たない受動的な造形物であり、なおかつ複数の記号からなる意味のある長さの荷を運ぶ、という音響通信の方式は見つからなかった。空中音響通信の文献はLopesとAguiarの2001年の論文から2025年のZhengとCaiの総説に至るまで、例外なくスピーカーを送信機として前提している。楽器を使うDominguesらの2002年の論文でさえ、楽器は任意の音列を出せる能動的な送信機として扱われている。受動的な造形物が音を出す研究は、HCIの分野でAcoustic BarcodesやLamelloやBlowholeとして存在するが、それらは物体の同一性を示す短い識別子を扱うものであって、通信路符号を伴う多記号の荷を運ぶ設計ではない。この二つの系譜のあいだが空いている。

第二に、通信の分野で標準的な道具立て、すなわち既知の信号による通信路の正規化、誤り訂正符号、隣接記号への制約を、受動的な造形物の側に持ち込んだ例は見つからなかった。パイロット信号に相当する基準音を同じ物体のなかに造形として同居させ、温度と息の強さによる全体のずれをその比で打ち消すという設計は、既存のどの文献にも見当たらなかった。音響タグの研究では、環境の変動に対しては機械学習による分類か、事前の較正で対処しており、物体の内部に基準を埋め込むという発想は確認できなかった。

第三に、暗号資産の復元用情報のような、失えば取り返しのつかない秘密を、音として読み出す物理媒体に保管するという提案は見つからなかった。音で鍵素材を運ぶ研究はHAPADEPをはじめとして存在するが、それらはいずれも機器のあいだの一時的な通路であって、保管の媒体ではない。保管の側では金属板への刻印などが実用されているが、読み出しは目視であって音ではない。

第四に、日本語の文献においても、可聴音によるデータ伝送は1990年代初頭の信州短期大学の研究から2021年の西村の解説まで一貫して電気的な送受信装置を前提にしており、受動的な発音体を送信機に据えた例は確認できなかった。

第五に、「データ・オーバー・サウンド」を正面から扱った英語の体系的なサーベイ論文は、複数の検索経路を使っても見つからなかった。最も近いのは西村による2021年の日本語の解説、ZhengとCaiによる2025年の書籍の一章、そしてLopesとAguiarおよびMadhavapeddyらによる2000年代の概説記事である。したがって論文でサーベイを引く場合は、この4点を組み合わせて示すのが誠実である。

## 調べ残した穴

- IEEE XploreとACM Digital Libraryが自動取得を拒むため、要旨の本文まで読めた文献が限られた。特にDominguesらの2002年の論文は、CipherFluteにとって最大の脅威候補でありながら題名と書誌情報しか確認できていない。図書館経由で本文を入手し、記号の設計と伝送速度を確かめることを強く勧める。
- 特許の調査をまったく行えなかった。受動的な発音体で符号を出す装置、たとえば音で開く錠や音響式の鍵の特許が存在する可能性がある。Google PatentsやJ-PlatPatでの検索が残っている。
- 音による機器設定という分野を十分に掘れなかった。Amazon Dash Button、Chromecastのゲストモード、補聴器や計測器の設定転送など、実在が疑われる事例に一次資料で到達できていない。
- 船舶と航空の音響信号については、海上衝突予防規則と航法援助施設のモールス識別までは確認したが、潜水艦の水中電話や水中鐘の歴史、霧鐘や霧笛の符号体系の歴史に踏み込めなかった。
- アマチュア無線の音声帯域データ通信、たとえば低速度走査テレビジョン、RTTY、PSK31、および気象図の無線ファクシミリは、音声帯域を記号の語彙として使う長い実践の系譜であるが、時間の都合で標準文書に当たれなかった。
- 蓄音機のレコード、オルゴールの櫛と円筒、自動ピアノのロール、映画フィルムの光学サウンドトラックといった、形状が波形を固定する古典的な媒体を体系的に押さえられなかった。CipherFluteを「形が信号を保持する媒体」の系譜に置く議論には、これらの一次資料があると強くなる。
- Chirpが公開していた技術文書、およびLISNRの技術白書の本文を取得していない。商用の方式が可聴音と超音波のどちらをどう使い分け、どの程度の情報量を運ぶのかという数字を、CipherFluteの1本あたり約3.7ビットと並べて示せると比較が具体的になる。
