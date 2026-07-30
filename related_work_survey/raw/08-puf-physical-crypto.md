# 物理複製困難関数と物理的な一方向性関数

（担当した切り口の調査結果である。指示されたファイルパスが `undefined/raw/08-puf-physical-crypto.md` となっていて先頭部分が壊れていたため、他の切り口の出力が置かれている `related_work_survey/raw/` の下に同じファイル名で書き出した。）

## この切り口の要約

物理複製困難関数の研究は、Pappuらが2002年にScienceで発表した「Physical One-Way Functions」を起点として、半導体の製造ばらつきを使うシリコン系、光散乱体を使う光学系、紙や表面の微細構造を使う個体識別系へと広がってきた。日本語圏では同じ概念が「人工物メトリクス」と呼ばれ、松本勉らのナノ人工物メトリクスが代表的である。この分野の中心的な主張は「物理的な乱れは複製できないので、それ自体を鍵や識別子にしてよい」というものであり、CipherFluteが宣言している「物理層に秘匿の力はまったく無い」という立場とは正反対に見える。しかし調べてみると、両者は矛盾していない。物理複製困難関数が使う乱れは、製造者自身にも制御できない微視的な乱れであって、設計図どおりに作られる巨視的な形状ではない。CipherFluteの管長は設計図そのものであり、物理複製困難関数の要件を最初から満たさない。したがってCipherFluteの宣言は学術的に正しく、むしろ物理複製困難関数の定義に忠実である。

複製の容易さについても裏付けが取れた。Laxtonらは写真から物理鍵の刻みを復元して複製できることを示し、Rameshらは鍵を鍵穴に差し込む音だけから刻みを推定できることを示した。Al Faruqueらは3Dプリンタの動作音から印刷中の形状とGコードを復元できることを示し、Songらはスマートフォンの内蔵する音響センサと磁気センサの信号から同じことを示している。CipherFluteの笛は形状を計測されれば無音で読めるという主張は、これらの結果と整合する。さらにMarakisらは光学的物理複製困難関数の複製に成功しており、物理複製困難性そのものが絶対ではないことも分かった。

一方で、能動的な音源も電子部品も持たない3Dプリント共鳴体の共鳴周波数のばらつきを物理複製困難関数として使う研究は、今回の調査では見つからなかった。「音響物理複製困難関数」を名乗る研究は、センサノードを対象とするVaidyaらのものと、2026年に投稿されたWangらの査読前原稿の二つだけである。前者は電源とマイクロホンを持つセンサノードを対象とし、後者は二酸化クロムの微粒子を絹フィブロインに分散させた磁気記録媒体の磁区の乱れを利用して、通常の再生装置で読み出す構成である。いずれも受動的な3Dプリント構造の共鳴を使っていない。CipherFluteを物理複製困難関数の方向へ発展させる道は、学術的には空いている。

## 新規性への脅威が大きい文献

脅威が「高」に相当する文献、すなわちCipherFluteの主要な主張を崩す文献は見つからなかった。以下はすべて「中」であり、必ず引用して差分を述べるべきものである。脅威の大きい順に並べた。

### 1. Sensor Identification via Acoustic Physically Unclonable Function

- 著者は Girish Vaidya, T. V. Prabhakar, Nithish Gnani, Ryan Shah, Shishir Nagaraja である。
- Digital Threats: Research and Practice（ACM）, 第4巻第2号, 論文番号20, pp.1-25, 2023年。
- 確認先は https://doi.org/10.1145/3488306 である（Crossrefの書誌登録で題名・著者・掲載誌・巻号・ページ・抄録を確認した）。
- なお、この論文の年は注意が要る。Crossrefの登録日は2022年3月15日であり、これはオンライン先行公開の日付である。冊子としては第4巻第2号（2023年）に論文番号20として収録されており、DBLPの記録（https://dblp.org/rec/journals/dtrap/Vaidya0GSN23 ）も2023年としている。引用では2023年とするのが安全である。
- 市販部品で組んだセンサノードには、識別用の専用ハードウェアを追加できないという問題がある。著者らはノードが持つ音響部品の製造公差に由来する固有性と、設置場所に由来する音場の応答とを組み合わせ、「音響物理複製困難関数」と名付けた識別子を提案している。固有性の成分は製造公差から導かれるため複製困難であり、位置の成分は音響的なフィンガープリンティングによって得られる。数週間にわたる実運用で、数千台規模を99パーセントの精度で識別しつつ、機器の移動も検知できることを示した。合成音場のなかでの物理的な位置を、識別子としてだけでなく機器の物理的完全性の検証にも使っている。
- CipherFluteとの関係は、「音響」と「物理複製困難関数」を結び付けた先行例として最も近いという点にある。ただし対象は電源とマイクロホンを持つセンサノードであり、読み出しには能動的な音源と信号処理が要る。CipherFluteは電源も電子部品も持たない受動的な笛であり、しかも運ぶのは識別子ではなく利用者が指定した任意のビット列である。さらにCipherFluteは製造ばらつきを情報源ではなく雑音として扱い、基準笛で打ち消している。この「ばらつきを消す設計」と「ばらつきを使う設計」の対比は、論文で明示的に書く価値がある。
- 脅威の度合いは「中」である。用語「acoustic PUF」を先に取られているため、CipherFluteが不用意に音響と物理複製困難性を結び付けて語ると先行研究と衝突する。ただし読み出し機構も目的も異なるので、主張が崩れることはない。

### 2. Reconsidering Physical Key Secrecy: Teleduplication via Optical Decoding

- 著者は Benjamin Laxton, Kai Wang, Stefan Savage である。
- Proceedings of the 15th ACM Conference on Computer and Communications Security（CCS 2008）, pp.469-478。
- 確認先は https://doi.org/10.1145/1455770.1455830 である（Crossrefの書誌登録で著者・会議名・ページを確認し、抄録の全文も確認した）。Crossrefには副題を落とした「Reconsidering physical key secrecy」という短い題名で登録されているが、副題を含む題名が正しい。
- 物理錠の防御は、鍵の情報内容が私的であること、すなわち複製には鍵の所持か切削情報の事前知識が要ることを前提にしている。著者らはこの前提が撮像技術の普及によって崩れることを示した。ありふれた撮影機材と標準的な計算機視覚のアルゴリズムだけで、離れた場所から鍵の刻みコードを完全かつ正確に読み取り、精密な複製を切削できることを実証している。試作システムをSneakeyと名付け、実験室と実環境の両方で、米国で最も普及している住宅用の鍵に対して有効性を評価した。
- CipherFluteとの関係は極めて直接的である。CipherFluteは「形状を計測されれば無音で読める、複製も容易である」と宣言しているが、これはまさに本論文が物理鍵について示した結果を笛に置き換えたものである。CipherFluteの脅威モデルの正当化として、この文献を引くのが最も強い。逆に言えば、CipherFluteが「物理層に秘匿がある」と主張していたら、この文献によって直ちに否定されていた。
- 脅威の度合いは「中」である。CipherFluteの主張を崩すのではなく支えるが、引用しないと脅威モデルの記述が学術的な裏付けを欠く。

### 3. Listen to Your Key: Towards Acoustics-based Physical Key Inference（SpiKey）

- 著者は Soundarya Ramesh, Harini Ramprasad, Jun Han である。
- Proceedings of the 21st International Workshop on Mobile Computing Systems and Applications（HotMobile 2020）, pp.3-8。
- 確認先は https://doi.org/10.1145/3376897.3377853 である（Crossrefの書誌登録で著者・会議名・ページを確認し、抄録の全文で下記の数値を確認した）。Crossrefには副題を落とした「Listen to Your Key」という題名で登録されている。
- 物理錠は錠前破りに弱いが、専用の道具と訓練が要り、怪しまれやすいので依然として広く使われている。著者らはSpiKeyという攻撃を提案し、攻撃者に必要なものをスマートフォンのマイクロホンだけに引き下げた。被害者が鍵を差し込むときに出る音を録音し、聞こえるクリック音の時間差から鍵の刻みの深さを推定する。実録音に基づくシミュレーションで、33万本以上の鍵の候補集合を、最頻のケースでは3本にまで絞り込めることを示した。
- CipherFluteとの関係は二重である。第一に、音が形状を漏らすという事実そのものがCipherFluteの脅威モデルを裏付ける。第二に、CipherFluteは「吹いた音の高さを符号として読む」設計なので、正規の読み出しと攻撃者の盗聴とが同じ物理量を共有している。すなわち利用者が読み出しのために吹いた音を録音されれば、それだけで秘密が漏れる。この点は論文中の脅威モデルで明記すべきであり、SpiKeyはその最良の引用先である。
- 脅威の度合いは「中」である。CipherFluteの新規性は崩さないが、音響的な盗聴という攻撃面を先に定式化しているので、引用と差分の記述が要る。

### 4. Unclonable security features for additive manufacturing

- 著者は O. Ivanova, A. Elliott, T. A. Campbell, C. B. Williams である。
- Additive Manufacturing, 第1巻から第4巻の合併号, pp.24-31, 2014年10月。
- 確認先は https://doi.org/10.1016/j.addma.2014.07.001 である（Crossrefで書誌を確認し、OpenAIREの記録 https://api.openaire.eu/search/publications?doi=10.1016/j.addma.2014.07.001 で抄録の全文を確認した）。
- 積層造形が複数材料を部品の内部に選択的に配置できることを利用して、造形物そのものに物理的なセキュリティ機能を作り込む方法を提案している。紫外線を吸収して可視光を出す量子ドットを分散させた光硬化樹脂を作り、PolyJet方式（材料噴射方式）の3Dプリンタで物体の内部に埋め込む。巨視的には規則正しく見えても、噴射液滴の単位では微視的に確率的な配置になるため、この乱れが物理複製困難関数の中核要素になると論じている。抄録には量子ドットの添加量が5×10のマイナス3乗重量パーセント、すなわち0.005重量パーセントまで下げても蛍光顕微鏡で内部から検出でき、同じ濃度では肉眼には見えないと書かれており、この数値は原典の抄録で裏が取れた。顕微鏡の倍率を変えることで三次元的な多層のセキュリティ模様が作れるという展望も示している。
- CipherFluteとの関係は、「3Dプリント物に物理複製困難関数を持たせる」という発想の代表的な先行例であるという点である。CipherFluteは同じく3Dプリント物に秘密を持たせるが、乱れではなく設計どおりの管長を使い、読み出しには顕微鏡ではなく人の息を使う。装置が要らないことと、識別ではなく任意のビット列を運ぶことが差分である。
- 脅威の度合いは「中」である。CipherFluteが「3Dプリント物にセキュリティ機能を埋め込む研究」の系譜に自分を置くなら、この文献を落とすことはできない。

### 5. 3D Unclonable Optical Identity for Universal Product Verification

- 著者は Chenxing Wang, Lily Raymond, Yifei Jin, Alireza Tavakkoli, Haoting Shen である。
- IEEE International Symposium on Hardware Oriented Security and Trust（HOST）2021, pp.136-146。
- 確認先は https://doi.org/10.1109/HOST49136.2021.9702273 である（Crossrefで著者・会議名・ページを確認し、OpenAlexの記録 https://api.openalex.org/works/doi:10.1109/HOST49136.2021.9702273 で抄録の全文を確認した。以下の要約は抄録の記述と一致している）。
- 通し番号やバーコードのような従来の識別手段は容易に複製できる。物理複製困難関数やナノ化学材料を使う新しい識別手段は微小な乱れを利用して複製を難しくするが、前者は電子機器にしか使えず、後者は特殊な製造工程か不便な検証手順を要する。著者らはこれらの欠点に対処するため、微細構造がランダムな三次元のタグを提案し、構造の再現が技術的に難しいことによって複製を防ぐ。低コストで作れて、固体表面を持つほとんどの製品に適用でき、携帯電話程度の機材で検証できると主張している。タグの光学画像を撮り、機械学習による物体検出で強化した検証アルゴリズムを開発して、試作タグで検証の信頼性を実証した。
- CipherFluteとの関係は、電子部品を持たない三次元の物体に複製困難な同一性を持たせ、身近な機材で検証するという目標が近い点にある。ただし読み出しは光学であって音響ではなく、運ぶのは同一性であって秘密のビット列ではない。
- 脅威の度合いは「中」である。「電子部品なしの物体に検証可能な同一性を与える」という主張の一部が重なるため、差分を明示する必要がある。

### 6. Acoustic Side-Channel Attacks on Additive Manufacturing Systems

- 著者は Mohammad Abdullah Al Faruque, Sujit Rokka Chhetri, Arquimedes Canedo, Jiang Wan である。
- 2016 ACM/IEEE 7th International Conference on Cyber-Physical Systems（ICCPS 2016）, pp.1-10。
- 確認先は https://doi.org/10.1109/ICCPS.2016.7479068 である（Crossrefで著者・会議名・ページを確認し、OpenAlexの記録 https://api.openalex.org/works/doi:10.1109/ICCPS.2016.7479068 で抄録の全文を確認した）。
- 3Dプリンタなどの積層造形装置は造形中に音を出しており、その音には工程の情報が含まれている。著者らはこの音響的な副次経路から、元の設計データに触れることなく印刷中の物体を間接的に復元できることを示した。抄録では、これを物理領域から情報領域への攻撃と位置づけ、音響信号処理と機械学習と文脈に基づく後処理を並べた処理系を提案している。熱溶解積層方式の装置で試験用の物体とそのGコードを復元し、軸の予測の平均正解率が78.35パーセント、長さの予測の平均誤差が17.82パーセントであったと報告している。知的財産や営業秘密の窃取につながる脆弱性であり、積層造形装置に対してこの種の攻撃を論じたのは自分たちが最初であると述べている。
- CipherFluteとの関係は、笛の形状という秘密が「印刷の瞬間」に漏れうるという点にある。CipherFluteは秘密を含む笛を利用者自身が家庭用プリンタで印刷する運用を想定しているので、印刷現場に録音機があれば秘密が漏れる。脅威モデルに「製造時の副次経路」を書き足す根拠になる。
- 脅威の度合いは「中」である。CipherFluteの主張は崩さないが、脅威モデルの完全性に関わるので引用が要る。

### 7. My Smartphone Knows What You Print: Exploring Smartphone-based Side-channel Attacks against 3D Printers

- 著者は Chen Song, Feng Lin, Zhongjie Ba, Kui Ren, Chi Zhou, Wenyao Xu である。
- Proceedings of the 2016 ACM SIGSAC Conference on Computer and Communications Security（CCS 2016）, pp.895-907。
- 確認先は https://doi.org/10.1145/2976749.2978300 である（Crossrefで著者・会議名・ページを確認し、OpenAlexの記録 https://api.openalex.org/works/doi:10.1145/2976749.2978300 で抄録の全文を確認した）。
- 3Dプリンタのそばに置いたスマートフォンの内蔵センサだけを使い、印刷されている物体を推定する攻撃を端から端まで検討した研究である。抄録によれば、音響の副次経路と磁気の副次経路の両方をスマートフォンの内蔵センサで調べ、さらに磁気で補強した攻撃モデルによってノズルの向きの動作を精度よく推定している。物体とそのGコードを復元し、平均傾向誤差が通常の設計で5.87パーセント、複雑な設計で9.67パーセントであったと報告している。専用の計測器を持たない攻撃者でも実行できることが要点である。
- CipherFluteとの関係は前項と同じで、製造時の副次経路による漏洩である。攻撃の敷居が「スマートフォンだけ」というところまで下がっている点で、家庭での印刷を前提とするCipherFluteにはより現実的な脅威である。
- 脅威の度合いは「中」である。

### 8. Physical One-Way Functions

- 著者は Ravikanth Pappu, Ben Recht, Jason Taylor, Neil Gershenfeld である。
- Science, 第297巻第5589号, pp.2026-2030, 2002年9月20日。
- 確認先は https://doi.org/10.1126/science.1074376 である（Crossrefの書誌登録で著者・掲載誌・巻号・ページ・日付を確認し、抄録の全文も確認した）。
- 近代の暗号技術は一方向性関数の上に成り立っているが、常用される一方向性関数は未証明の予想に依拠するか既知の弱点を持つ、と著者らは述べる。そこで数論に頼るのをやめ、無秩序な媒質のなかを光がコヒーレントに伝わるという中間尺度の物理を使い、媒質の微細構造を固定長のビット列へ物理的に還元して、一意な識別子の割り当てと認証を行う。抄録によれば、この物理的一方向性関数は安価に作れ、複製が著しく困難で、簡潔な数学的表現を持たず、本質的に改変耐性を備えている。膨大な番地空間を利用した認証の手順も示している。この論文が物理複製困難関数という分野の出発点になっている。（レーザ光を当てて得るスペックル模様を応答とするという読み出しの具体は本文にあり、抄録では「無秩序な媒質中のコヒーレント輸送」と記されている。散乱体の材質の細部までは本文を読んで確認していない。）
- CipherFluteとの関係は、CipherFluteが「そうではないもの」を定義する基準点になるという点である。CipherFluteの笛は設計図どおりの管長を持ち、形状から応答が完全に予測でき、同じ設計ファイルから何本でも同じ笛が作れる。つまり物理的一方向性関数の要件を意図的に満たしていない。この対比を明示すれば、CipherFluteの脅威モデルの宣言は「弱さの告白」ではなく「定義上の位置づけ」として読める。
- 脅威の度合いは「中」である。主張は崩さないが、この文献との対比を書かないと査読者から「なぜ物理複製困難関数にしないのか」と必ず問われる。

### 9. PrinTracker: Fingerprinting 3D Printers using Commodity Scanners

- 著者は Zhengxiong Li, Aditya Singh Rathore, Chen Song, Sheng Wei, Yanzhi Wang, Wenyao Xu である。
- Proceedings of the 2018 ACM SIGSAC Conference on Computer and Communications Security（CCS 2018）, pp.1306-1323。
- 確認先は https://doi.org/10.1145/3243734.3243735 である（Crossrefで著者・会議名・ページを確認し、OpenAlexの記録 https://api.openalex.org/works/doi:10.1145/3243734.3243735 で抄録の全文を確認した。台数14台と92パーセントという数値は抄録の記述と一致している）。
- 3Dプリンタが違法な道具の製造に使われる懸念に対して、印刷物からその出所のプリンタを特定する手法を提案している。情報埋め込みや電子透かしは製造工程を管理できる場合にしか使えないので、犯罪捜査には向かないというのが出発点である。著者らは、プリンタの機械的な不完全性が造形線の形成にばらつきを生み、それが繰り返し現れて固有の質感になると論じ、これを指紋として使う。14台のプリンタで高い精度を得て、試料の面積や位置や工程が制約された不利な条件でも92パーセントの精度を保った。
- CipherFluteとの関係は二つある。第一に、CipherFluteの笛には印刷したプリンタの指紋が残るので、日用品への偽装が「誰が作ったか」の匿名性までは保証しないという注意になる。第二に、笛の造形ばらつきを積極的に使えば物理複製困難関数の方向へ発展させられるという可能性を示す先行例でもある。
- 脅威の度合いは「中」である。CipherFluteが偽装による探索コストの引き上げを主張するとき、出所の追跡可能性という残余リスクを述べる根拠になる。

### 10. Nano-artifact metrics based on random collapse of resist（およびナノ人工物メトリクスの一連の研究）

- 著者は Tsutomu Matsumoto, Morihisa Hoga, Yasuyuki Ohyagi, Mikio Ishikawa, Makoto Naruse, Kenta Hanaki, Ryosuke Suzuki, Daiki Sekiguchi, Naoya Tate, Motoichi Ohtsu の10名である。
- Scientific Reports, 第4巻, 論文番号6142, 2014年8月21日。確認先は https://doi.org/10.1038/srep06142 である（Crossrefの書誌登録で著者全員・掲載誌・巻・論文番号・日付を確認し、抄録の全文も確認した）。
- 関連する続報として Tsutomu Matsumoto, Naoki Yoshida, Shumpei Nishio, Morihisa Hoga, Yasuyuki Ohyagi, Naoya Tate, Makoto Naruse: Optical nano artifact metrics using silicon random nanostructures（Scientific Reports, 第6巻, 論文番号32438, 2016年8月31日, https://doi.org/10.1038/srep32438 ）がある。こちらもCrossrefで著者・巻・論文番号を確認した。
- 日本語の最新の成果として、宮本岩麒, 岩橋虎, 吉田直樹, 吉岡克成, 松本勉「ナノ人工物メトリクスの耐クローン性：シンプルな白色干渉計の有効性」情報処理学会論文誌, 第66巻第3号, pp.545-554, 2025年3月15日がある。英語題名は Clone Resistance of Nano-artifact Metrics: Effectiveness of a Simple White-light Interferometer である。確認先は https://cir.nii.ac.jp/crid/1390022067669403520 および情報処理学会電子図書館の本文記録 https://ipsj.ixsq.nii.ac.jp/records/2001672 である。この論文にはDOI 10.20729/0002001672 が付いている。
- 人工物メトリクスは、物体が本来持つ特性を認証と耐クローン性に使う情報セキュリティ技術である、と2014年の論文の抄録で定義されている。著者らは電子線描画に曝したレジストの柱の配列をランダムに倒壊させ、現在の描画装置の解像度より細かい、最小寸法が10ナノメートルを下回る形態を作り出した。抄録では他人受入率、本人拒否率、耐クローン率を評価して、高い水準のセキュリティ用途の要件を満たすと述べている。2025年の論文は、高価な計測器でなく簡素な白色干渉計でも、高級機を使う系と同等の照合精度と耐クローン性が得られることを示した。この記述は情報処理学会電子図書館の抄録で裏を取った。
- CipherFluteとの関係は、日本語圏における「物理複製困難関数」の呼称と評価尺度の標準がここにあるという点である。CipherFluteは日本語の学会に投稿するので、「人工物メトリクスではない」ことを人工物メトリクスの語彙で言う必要がある。具体的には、CipherFluteの笛には他人受入率も耐クローン率も定義できず、そもそも同一設計から同一の応答を出すことが目的である、と書けばよい。
- 脅威の度合いは「中」である。日本語圏の読者に対して位置づけを説明する義務が生じる。

### 11. Clones of the Unclonable: Nanoduplicating Optical PUFs and Applications

- 著者は E. Marakis, U. Rührmair, M. Lachner, R. Uppu, B. Škorić, P. W. H. Pinkse である。
- arXiv:2212.12495, 2022年12月23日投稿。
- 確認先は https://arxiv.org/abs/2212.12495 である（arXivの論文ページで題名・著者・抄録・投稿日を確認した。arXivが付与するDOIは 10.48550/arXiv.2212.12495 である。査読誌への掲載は、Crossrefの題名検索でも該当が出ず、確認できていない）。
- 物理複製困難関数の分野が置いてきた基礎的な仮定、すなわち「正規の製造者も外部の攻撃者も等しく複製できない」という仮定が常に成り立つわけではないことを実証した研究である。著者らは最新の微細加工技術を使い、自明でない光散乱構造の複製を63個作り、本質的に同じ散乱挙動を示すことを確かめた。残る差は雑音の水準に近いか、それを下回るという。これは物理複製困難関数を使う一部の方式の安全性を損なう一方で、新しい応用も開く。抄録には、価値ある品物のための偽造不能なラベル、デジタル網の上での鍵を使わない集団認証、秘密鍵を内部に持たない暗号化復号装置が挙げられている。以上はすべてarXivの抄録の記述で裏が取れた。
- CipherFluteとの関係は、「物理層に秘匿を期待しない」というCipherFluteの設計判断が保守的で正しいことを示す根拠になる点である。物理複製困難性は絶対ではなく、専用の設備があれば破られうる。CipherFluteが秘匿を秘密分散だけに負わせているのは、この意味で堅実である。
- 脅威の度合いは「中」である。CipherFluteの主張を支える側だが、査読者から「物理複製困難関数にすればよいのでは」と言われたときの反論材料として引用価値が高い。

### 12. 包絡線情報の相関による楽器の個体差識別

- 著者は小幡健作, 山崎芳男である。
- 日本音響学会研究発表会講演論文集, 第2003巻第1号, pp.659-660, 2003年3月18日（春季研究発表会である）。
- 確認先は https://cir.nii.ac.jp/crid/1570572700389150080 である（CiNii Researchの書誌記録で題名・著者・掲載・巻号・ページ・日付を確認した。抄録は記録されていないため、内容は題名から読み取れる範囲にとどめる）。
- 同じ種類の楽器であっても個体ごとに音が違うという事実に着目し、音の包絡線情報の相関から個体を識別する試みを報告した2ページの発表である。
- CipherFluteとの関係は、「楽器の音から個体を見分ける」という、音響的な人工物メトリクスに最も近い日本語の先行例である点にある。CipherFluteは逆に、個体差を基準笛で打ち消して同じ設計の笛が同じ符号を返すようにしている。つまり同じ物理現象を、片方は識別の情報源として使い、もう片方は消すべき雑音として扱っている。この対比は日本語の論文で書くと分かりやすい。
- 脅威の度合いは「中」である。ただし2ページの発表であり、認証や鍵生成を目的としていないので、脅威というより位置づけの整理に使う文献である。

### 13. Listening to disorder: acoustic physical unclonable functions for audio-enabled secure authentication

- 著者は Yu Wang, Ying-Hao Fu, Zi-Ting Wang, Xin-Yu Cheng, Tao Wang, Yanqing Lu である。
- Research Squareの査読前原稿, 2026年5月14日公開。
- 確認先は https://doi.org/10.21203/rs.3.rs-9353152/v1 である（Crossrefの登録記録で題名・著者・種別・日付を確認した。Research Squareの本文ページはアクセスが拒否されたが、Europe PMCが査読前原稿として収録しており、その記録 https://europepmc.org/article/PPR/PPR1207897 で抄録の全文を確認できた）。
- 抄録によれば、音響信号は安全な情報符号化、偽造防止、認証のための豊かな物理媒体でありながらほとんど活用されていない、という問題意識から出発する。著者らは、ありふれた音を予測不能な励起として使い、高いエントロピーの物理的署名を生む「音響物理複製困難関数」を提案している。素子の実体は、二酸化クロムの微粒子を絹フィブロインの基質に分散させた磁気複合媒体である。確率的な音響の揺らぎが微視的な磁区の乱れと相互作用して、本質的に複製も再現もできない応答が生じる、と述べている。人が聞き取れる音声出力とハードウェアに基づく安全性を統合し、再構成可能性と機械学習攻撃への耐性を持ち、標準的な再生装置とそのまま両立するという。周波数領域の符号化による多重の偽造防止と、音響と光学を組み合わせた複合ラベルによる多次元の安全性も示している。
- CipherFluteとの関係は、「音響」と「物理複製困難関数」と「音で読む認証」という三つの要素が同時にそろっている点で、用語の上では最も近い。しかし内容を確認した結果、素子は磁気記録媒体であって受動的な3Dプリント構造ではなく、読み出しには標準的な再生装置が要り、運ぶのは複製困難な署名であって利用者が指定したビット列ではない。人の息で吹いて読むという構成とはまったく異なる。
- 脅威の度合いは「中」である。抄録を確認した結果、受動的な3Dプリント構造の共鳴を使っていないことがはっきりしたので、当初懸念した「高」への引き上げは不要になった。ただし「音響物理複製困難関数」という名称が2026年にも使われている事実は、CipherFluteが音響と物理複製困難性を安易に結び付けないための材料として引くべきである。

## 背景として押さえるべき文献

以下はすべて脅威が「低」であり、背景として引用する程度でよい。書誌はすべてCrossrefの登録記録またはCiNii Researchの書誌記録で、著者名の綴り、題名、掲載誌または会議名、年、巻号ページまで確認した。2026年7月30日の検証では、下に挙げた30件すべてについてDOIが解決し、登録された書誌が本文の記述と一致することを確かめた。

- Blaise Gassend, Dwaine Clarke, Marten van Dijk, Srinivas Devadas: Silicon Physical Random Functions. ACM CCS 2002, pp.148-160. https://doi.org/10.1145/586110.586132 。半導体の遅延ばらつきを使う最初期の構成である。
- G. Edward Suh, Srinivas Devadas: Physical Unclonable Functions for Device Authentication and Secret Key Generation. ACM/IEEE DAC 2007, pp.9-14. https://doi.org/10.1145/1278480.1278484 。機器認証と鍵生成という応用の定番である。配線とトランジスタの遅延特性のばらつきを使う構成であることを抄録で確認した。なお、ページはCrossrefのACM登録では開始ページの9だけが登録されているが、DAC 2007の予稿集では9ページから14ページまでの6ページである。
- Charles Herder, Meng-Day Yu, Farinaz Koushanfar, Srinivas Devadas: Physical Unclonable Functions and Applications: A Tutorial. Proceedings of the IEEE, 2014年, pp.1126-1141. https://doi.org/10.1109/JPROC.2014.2320516 。分野の教科書的な解説である。
- Ulrich Rührmair, Srinivas Devadas, Farinaz Koushanfar: Security Based on Physical Unclonability and Disorder. Introduction to Hardware Security and Trust（Springer）, 2011年, pp.65-102. https://doi.org/10.1007/978-1-4419-8080-9_4 。「乱れに基づく安全性」という枠組みの整理である。
- Ulrich Ruhrmair, Daniel E. Holcomb: PUFs at a Glance. DATE 2014, pp.1-6. https://doi.org/10.7873/DATE.2014.360 。短い総覧である。
- Ulrich Rührmair, Frank Sehnke, Jan Sölter, Gideon Dror, Srinivas Devadas, Jürgen Schmidhuber: Modeling Attacks on Physical Unclonable Functions. ACM CCS 2010, pp.237-249. https://doi.org/10.1145/1866307.1866335 。機械学習で応答を予測する攻撃であり、物理複製困難性の限界を示す。
- Clemens Helfmeier, Christian Boit, Dmitry Nedospasov, Jean-Pierre Seifert: Cloning Physically Unclonable Functions. IEEE HOST 2013, pp.1-6. https://doi.org/10.1109/HST.2013.6581556 。半導体の物理複製困難関数を実際に複製した報告である。
- Pim Tuyls, Geert-Jan Schrijen, Boris Škorić, Jan van Geloven, Nynke Verhaegh, Rob Wolters: Read-Proof Hardware from Protective Coatings. CHES 2006, pp.369-383. https://doi.org/10.1007/11894063_29 。被覆材の乱れから鍵を導く構成である。
- Boris Škorić: Quantum Readout of Physical Unclonable Functions. International Journal of Quantum Information, 第10巻第1号, 論文番号1250001, 2012年2月. https://doi.org/10.1142/S0219749912500013 。読み出し側の信頼を不要にする発展である。抄録に「情報量がきわめて大きいわけではない物理複製困難関数については、既知の認証方式と偽造防止方式はいずれも現場に信頼できる読み出し装置を要する」と明記されており、量子状態を問い掛けに使うことでこの前提を外す提案である。CipherFluteの読み出しは人の耳とマイクロホンであって信頼できる装置を前提にしないので、この論点は脅威モデルの議論で対比に使える。
- Ravikanth Pappu: Physical Unclonable Functions: The First Fifty Years. ACM Workshop on Attacks and Solutions in Hardware Security（ASHES）2023, p.3. https://doi.org/10.1145/3605769.3623997 。分野の創始者による回顧である。
- James D. R. Buchanan ほか: 'Fingerprinting' documents and packaging. Nature, 2005年, p.475. https://doi.org/10.1038/436475a 。紙や包装の表面のレーザ反射で個体を識別する。
- William Clarkson, Tim Weyrich, Adam Finkelstein, Nadia Heninger, J. Alex Halderman, Edward W. Felten: Fingerprinting Blank Paper Using Commodity Scanners. IEEE Symposium on Security and Privacy 2009, pp.301-314. https://doi.org/10.1109/SP.2009.7 。市販のスキャナだけで白紙の繊維構造から個体識別する。
- Ashlesh Sharma, Lakshminarayanan Subramanian, Eric A. Brewer: PaperSpeckle: Microscopic Fingerprinting of Paper. ACM CCS 2011, pp.99-110. https://doi.org/10.1145/2046707.2046721 。紙の微視的なスペックルを指紋にする。
- Ehsan Toreini, Siamak F. Shahandashti, Feng Hao: Texture to the Rescue: Practical Paper Fingerprinting Based on Texture Patterns. ACM Transactions on Privacy and Security, 2017年, pp.1-29. https://doi.org/10.1145/3092816 。実用的な紙指紋である。
- Riikka Arppe, Thomas Just Sørensen: Physical unclonable functions generated through chemical methods for anti-counterfeiting. Nature Reviews Chemistry, 2017年. https://doi.org/10.1038/s41570-017-0031 。化学的に作る物理複製困難関数の総説である。
- Fei Chen, Gary Mac, Nikhil Gupta: Security features embedded in computer aided design (CAD) solid models for additive manufacturing. Materials & Design, 第128巻, pp.182-194, 2017年8月. https://doi.org/10.1016/j.matdes.2017.04.078 。設計データが盗まれても、印刷条件の組み合わせが合わないと良品にならないような設計上の仕掛けを提案している。抄録で裏を取ったところ、STLファイルの分解能、スライスの条件、造形台の上での姿勢、装置の運転条件という一意の組み合わせのもとでしか高品質な部品が得られず、それ以外では欠陥品や劣った品になると述べている。CipherFluteの「設計ファイルの秘匿だけでは守れない」という論点に近い。
- Chao Wei, Zhe Sun, Yihe Huang, Lin Li: Embedding anti-counterfeiting features in metallic components via multiple material additive manufacturing. Additive Manufacturing, 第24巻, pp.1-12, 2018年12月. https://doi.org/10.1016/j.addma.2018.09.003 。金属部品の内部に別材料で二次元コードを埋め込み、X線で読む。抄録を確認したところ、粉末を混ぜて供給するレーザ粉末床溶融結合の手法でCu10Snという銅合金のQRコードを316Lステンレス鋼の部品の内部に埋め込み、深さ15ミリメートルまでX線撮像で識別できたと報告している。内部に情報を隠す点でAirCodeやInfraStructsと同系統である。
- Bertrand Cambou ほか: Securing Additive Manufacturing with Blockchains and Distributed Physically Unclonable Functions. Cryptography, 2020年, 17. https://doi.org/10.3390/cryptography4020017 。積層造形の工程をブロックチェーンと物理複製困難関数で守る枠組みである。
- Aaron Pendino ほか: Additively Manufactured RF Electronics With Structurally Integrated Physically Unclonable Functions for Wireless System Security. IEEE Access, 2025年, pp.145042-145059. https://doi.org/10.1109/ACCESS.2025.3600010 。積層造形した高周波回路の構造そのものに物理複製困難関数を組み込む。
- Kaushik Yanamandra, Guan Lin Chen, Xianbo Xu, Gary Mac, Nikhil Gupta: Reverse engineering of additive manufactured composite part by toolpath reconstruction using imaging and machine learning. Composites Science and Technology, 第198巻, 論文番号108318, 2020年9月. https://doi.org/10.1016/j.compscitech.2020.108318 。印刷物の画像から工具経路を復元する。抄録によれば、形状だけでなく微細構造の機械学習によって3Dプリントの工具経路まで再構成し、寸法の差が0.33パーセントの逆解析模型を得ている。造形物からの逆解析が現実的であることを示す。
- Zhen Wang, Hao Zhou, Chao Ye, Changjiang Song, Taiqi Zang: Study on traces left on a mechanical lock picked by a 3D printed key in toolmarks examination. Forensic Science International, 第317巻, 論文番号110514, 2020年12月. https://doi.org/10.1016/j.forsciint.2020.110514 。抄録で数値を確認した。白色樹脂、白色ナイロン粉末、黒色ABSの3種類の高分子材料で40本の鍵を印刷し、そのうち38本で錠が開いて開錠率は95パーセントであったと報告している。論文の主題は開錠そのものよりも、開錠のあとに錠のピンや鍵溝に残る痕跡を鑑識の観点から調べることである。物理鍵が3Dプリントで実用に足る精度で複製できるという事実の一次資料になる。
- Anupam Das, Nikita Borisov, Matthew Caesar: Do You Hear What I Hear? Fingerprinting Smart Devices Through Embedded Acoustic Components. ACM CCS 2014, pp.441-452. https://doi.org/10.1145/2660267.2660325 。スピーカとマイクロホンの製造ばらつきから機器を識別する。
- Adriana Berdich ほか: Fingerprinting Smartphones Based on Microphone Characteristics From Environment Affected Recordings. IEEE Access, 2022年, pp.122399-122413. https://doi.org/10.1109/ACCESS.2022.3223375 。実環境の録音からマイクロホン個体を識別する。
- Oliver Willers, Christopher Huth, Jorge Guajardo, Helmut Seidel: MEMS Gyroscopes as Physical Unclonable Functions. ACM CCS 2016, pp.591-602. https://doi.org/10.1145/2976749.2978295 。機械式センサの製造ばらつきを物理複製困難関数にした例である。
- Monica Arenas, Huseyin Demirci, Gabriele Lenzini: Cholesteric Spherical Reflectors as Physical Unclonable Identifiers in Anti-counterfeiting. ARES 2021, pp.1-11. https://doi.org/10.1145/3465481.3465766 。物体に貼る複製困難な識別子である。
- Vincent Immler, Karthik Uppund: New Insights to Key Derivation for Tamper-Evident Physical Unclonable Functions. IACR Transactions on Cryptographic Hardware and Embedded Systems, 2019年第3号, pp.30-65. https://doi.org/10.46586/tches.v2019.i3.30-65 。開封検知と鍵導出を兼ねる構成であり、CipherFluteが引いているJohnstonの封印評価と接続する。抄録を読むと、この文献はCipherFluteにとって背景以上の価値がある。応答を等間隔に量子化して多値の記号を得る「高次アルファベットの物理複製困難関数」を扱い、記号間の距離を表すのに適したLee距離に基づく誤り訂正符号を提案しているからである。CipherFluteも半音刻みの13スロットという多値アルファベットを量子化で読み、その上にReed-Solomon符号を載せている。符号の選び方の議論をするときは、この文献が最も近い理論的な足場になる。
- Mark Kac: Can One Hear the Shape of a Drum? The American Mathematical Monthly, 第73巻第4号第2部, pp.1-23, 1966年4月. https://doi.org/10.1080/00029890.1966.11970915 。
- Carolyn Gordon, David L. Webb, Scott Wolpert: One cannot hear the shape of a drum. Bulletin of the American Mathematical Society, 第27巻第1号, pp.134-138, 1992年. https://doi.org/10.1090/S0273-0979-1992-00289-6 。この二つは、スペクトルから形状が一意に定まらない場合があるという古典的な結果である。CipherFluteは形状から音を決める向きにしか依存しないので影響はないが、「音から形状を復元して複製する」攻撃を論じるときに、原理的な限界と実際上の容易さを区別する材料になる。
- F. A. P. Petitcolas, R. J. Anderson, M. G. Kuhn: Information Hiding: A Survey. Proceedings of the IEEE, 1999年, pp.1062-1078. https://doi.org/10.1109/5.771065 。CipherFluteの物理層が提供しているものは秘匿ではなく情報隠蔽であるという整理を、この総説の語彙で書ける。
- 古原和邦, 時田俊雄, 松本勉: 「人工物メトリクスを用いた個体管理技術ガイダンス」の紹介：サプライチェーン・バリューチェーンの強化および効率化を目指して. 自動認識, 第35巻第7号, pp.43-49, 2022年6月. https://cir.nii.ac.jp/crid/1520010853668296960 。日本語圏で人工物メトリクスを実務に適用するための指針を紹介した記事である。CiNii Researchの記録で副題まで確認した。

## 未検証のまま残ったもの

2026年7月30日の検証で、この節にあった項目のうち、内容が確認できていなかった文献3件（項目としては2項目）が解消した。解消の経過も含めて現状を書く。かわりに、誌面で確かめきれなかった細部を新たに3項目書き加えた。

- 【解消】Yu Wangらの「Listening to disorder: acoustic physical unclonable functions for audio-enabled secure authentication」（Research Square, 2026年）は、Research Squareの本文ページが依然としてアクセス拒否であるが、Europe PMCが査読前原稿として収録しており（ https://europepmc.org/article/PPR/PPR1207897 ）、そこで抄録の全文を読めた。素子は二酸化クロムの微粒子を絹フィブロインに分散させた磁気複合媒体であって、受動的な3Dプリント構造ではないことが判明した。上の第13項を書き直してある。
- 【解消】Al Faruqueらの「Acoustic Side-Channel Attacks on Additive Manufacturing Systems」（ICCPS 2016）とSongらの「My Smartphone Knows What You Print」（CCS 2016）は、いずれもOpenAlexの記録に抄録の全文が収録されており、そこから内容と数値を確認できた。上の第6項と第7項を書き直し、抄録に書かれている数値を補ってある。
- 物理複製困難関数の総説類で「音響物理複製困難関数」の初期の例として修士論文が挙げられることがあると記憶しているが、今回の検索（OpenAlexの題名検索、arXivの全文検索、Crossrefの題名検索）では一次資料に到達できなかった。2026年7月30日の再検証でも、Crossrefの題名検索で「unclonable」と音響系の語を同時に含む題名を洗い出したところ、Vaidyaらの論文とWangらの査読前原稿の二つしか出てこなかった。実在も書誌情報も確認できていないので、名前や年を書くことは避ける。もし引用したい場合は、Eindhoven工科大学あるいはPhilipsの技術報告の所蔵を直接確認する必要がある。
- 「人工物メトリクスを用いた個体管理技術ガイダンス」そのもの（紹介記事ではなく本体の文書）には到達できていない。発行元と正式名称を確認する必要がある。紹介記事の側は副題まで含めてCiNii Researchで確認済みである。
- 暗号と情報セキュリティシンポジウム（SCIS）の予稿は電子的に公開されていないものが多く、人工物メトリクスの音響応用がSCISで発表されていないかどうかを確認できなかった。
- Ivanovaらの論文（Additive Manufacturing, 2014年）の第3著者の表記は、CrossrefとOpenAIREでは「T. Campbell」であり、中間名の頭文字を含む「T. A. Campbell」という形は誌面で確かめられていない。ScienceDirectの本文ページはアクセス拒否であった。引用時にどちらの表記を使うかは、誌面を見て決めるのが安全である。
- Suh と Devadas のDAC 2007論文のページ範囲は、CrossrefのACM登録には開始ページの9しか入っていない。9ページから14ページまでという範囲は、IEEE由来の書誌を収録するSemantic Scholarの記録で確認したものであり、予稿集の誌面そのものでは確かめていない。
- ACM Digital Library、IEEE Xplore、ScienceDirect、Research Squareの各本文ページは、いずれもこの環境からのアクセスが拒否された（HTTP 403）。そのため書誌の確認はCrossrefの登録記録を主とし、抄録の確認はOpenAlex、OpenAIRE、Europe PMC、arXiv、情報処理学会電子図書館、CiNii Researchを用いた。いずれも出版社が登録した書誌または出版社由来の抄録を配信する経路であるが、誌面そのものを見ていない点は書き留めておく。

## この切り口で見つからなかったこと

以下は、探したうえで「見つからなかった」と言えることである。CipherFluteの新規性の主張の根拠になるので、探索の範囲も併せて書く。

- 電源も電子部品も持たない受動的な3Dプリント共鳴体（笛、管、共鳴箱など）の共鳴周波数の製造ばらつきを、物理複製困難関数あるいは人工物メトリクスとして使う研究は見つからなかった。探索の範囲は、OpenAlexの題名検索と題名抄録検索（「acoustic PUF」「acoustic unclonable」「unclonable 3D printed」「unclonable additive manufacturing」など）、Crossrefの題名検索によるACM刊行物の横断（「unclonable」「physically unclonable」「physical unclonable」を題名に含む会議論文をすべて列挙して目視で確認）、arXivの全文検索である。
- 「acoustic PUF」または「acoustic physically unclonable function」を名乗る研究は、Vaidyaらのセンサノード識別と、2026年のResearch Squareの査読前原稿の二つしか見つからなかった。前者は電源とマイクロホンを持つセンサノードを対象とし、後者は磁気複合媒体を標準的な再生装置で読む構成であって、いずれも人が息を吹き込んで読む構成ではない。2026年7月30日の検証では、Crossrefの題名検索で「unclonable」と「acoustic」「sound」「resonance」「audio」「whistle」「vibration」などを組み合わせて探し直したが、題名の水準ではこの二つ以外に該当がなかった。
- CHI、UIST、TEI、SIGGRAPH、SCFといったヒューマンコンピュータインタラクションおよびデジタルファブリケーションの会議で、題名に「unclonable」を含む論文は、Crossrefで確認できたACM刊行物のなかに1件も存在しなかった。2026年7月30日の検証でも同じ探索をやり直した。CrossrefでACMのDOI接頭辞10.1145に限り、種別を会議論文に絞って題名に「unclonable」を含むものを列挙し、掲載会議名を目視で確認した。出てきたのはDesign Automation Conference、Great Lakes Symposium on VLSI、CCS、FPGA、International Conference on Computer-Aided Designといった設計自動化と安全性の会議ばかりで、ヒューマンコンピュータインタラクション寄りの会議は一つも含まれていなかった。唯一それらしく見えたのは、無線と移動体の安全性の会議であるWiSec 2022に出たMAG-PUFという磁気の物理複製困難関数の論文（ https://doi.org/10.1145/3507657.3529656 ）だけであり、これも対象は電子機器である。すなわち、日用品を作る研究の系譜と物理複製困難関数の系譜は、まだほとんど接続されていない。CipherFluteはこの二つの領域のあいだに立つ位置にある。
- 物理複製困難関数を用いて秘密分散の持ち分（シェア）を保護する3Dプリント物、という組み合わせは見つからなかった。Cambouらが積層造形の工程管理に分散的な物理複製困難関数を使っているが、これは工程の真正性のためであって、利用者の秘密の保管ではない。
- 息を吹き込んで読み出す物理的な鍵、あるいは笛の音高を符号として鍵素材にする研究は、物理複製困難関数の文脈では見つからなかった。音を出す受動的な物体を扱う先行研究（BlowholeやAcoustic Barcodes）は識別子やタグの読み出しが目的であり、暗号鍵やリカバリーシードのような秘密の運搬を目的としていない。
- 日本語圏の人工物メトリクスの研究は、レジスト倒壊によるナノ構造、レーザスペックル、パール顔料や白色顔料といった光学的な手段が中心であり、音響を使う人工物メトリクスは見つからなかった。CiNii Researchで「音響 PUF」「複製困難 物体 認証」を検索しても該当が0件であった。楽器の個体差識別（小幡・山崎, 2003年）は音響を使うが、認証や耐クローン性を目的としていない。
- 「物理層に秘匿の力はまったく無い」と明示的に宣言したうえで、秘匿をすべて秘密分散に負わせる、という設計方針を採る物理的な秘密保管の研究は、この切り口の範囲では見つからなかった。多くの研究はむしろ物理層に何らかの安全性を期待している。CipherFluteの宣言は、この分野の常識からするとかなり珍しい立場であり、そこを明示的に書けば独自性として読める。

## 調べ残した穴

- 調査の途中でOpenAlexの応答が制限（HTTP 429、再試行まで約24時間）になり、被引用のたどり直しを最後までできなかった。特に、Pappu 2002の被引用のうちデジタルファブリケーション寄りの枝と、Vaidyaの音響物理複製困難関数の被引用は追い切れていない。時間をおいて再度たどる価値がある。
- ACM Digital LibraryとIEEE Xploreの全文検索を直接使えなかった（いずれもアクセス拒否である）。ACMについてはCrossrefの題名検索で代替したが、題名に「unclonable」を含まず抄録や本文にだけ含むヒューマンコンピュータインタラクション系の論文は取りこぼしている可能性がある。
- Semantic ScholarとGoogle Scholarの被引用一覧を使えなかった（前者は応答制限、後者は自動アクセスの遮断）。芋づる式の探索が想定より浅い。2026年7月30日の検証でも、OpenAlexとSemantic ScholarとDBLPはいずれも短時間で応答制限（HTTP 429または503）に落ちたため、被引用のたどり直しは今回もできていない。書誌の照合はCrossrefの登録記録が中心である。
- 特許文献をまったく調べていない。3Dプリント物の音響的な認証や、笛を使った識別については特許が出ている可能性がある。査読論文よりも特許が先行しているという事態は、この種の応用寄りの技術ではしばしば起きる。
- カードを使う物理暗号（card-based cryptography）の系譜、すなわち電子計算機を使わずに秘密計算やゼロ知識証明を行う研究は、今回の切り口から外して調べていない。「電源を使わない暗号」という括りでCipherFluteを語るなら、この系譜との関係を別途整理する必要がある。
- 物理複製困難関数の応答から鍵を安定に取り出すための誤り訂正（fuzzy extractor、secure sketch）の理論は、名前を確認しただけで一次資料に当たっていない。CipherFluteがReed-Solomon符号を使う設計と、この理論的な枠組みとの関係は整理し切れていない。ただし2026年7月30日の検証で、ImmlerとUppundのTCHES 2019論文が、等間隔の量子化で得た多値記号の物理複製困難関数に対してLee距離に基づく誤り訂正符号を提案していることが分かった。CipherFluteの13スロットという多値アルファベットに最も近い足場はここなので、まずこの論文の本文から入るのがよい。
- 材料や環境の変化による経年での応答のずれ（エイジング）に関する物理複製困難関数の研究は列挙しただけで内容を読んでいない。CipherFluteの笛が温度や湿度、樹脂の経年でどれだけ音高が動くかという議論に、この分野の評価尺度が使える可能性がある。

## 検証の記録

2026年7月30日に、この切り口の文献一覧を書いた担当者とは別の担当者が、書誌情報の実在を独立に検証した。検証したのは本文に挙がっている文献45件のすべてである。内訳は、脅威が「中」の節に並ぶ13項目に含まれる15件（第10項がScientific Reportsの2本と情報処理学会論文誌の1本を含むため、項目数より件数が多い）と、背景の節に並ぶ30件である。

検証の手順は次のとおりである。まず本文からDOIを41件、それ以外のURLを4件（arXivが1件、CiNii Researchが3件）機械的に抜き出した。次にDOIの41件についてCrossrefの登録記録を一件ずつ取得し、著者名の綴り、題名、掲載誌または会議名、発行年、巻号、ページ、資料種別を本文の記述と突き合わせた。41件すべてがCrossrefで解決し、存在しない文献は1件もなかった。arXivの1件は論文ページを直接開いて題名、著者、投稿日、抄録を確認した。CiNii Researchの3件はそれぞれの記録を開いて題名、著者、掲載、巻号、ページ、日付を確認し、情報処理学会論文誌の1件については情報処理学会電子図書館の記録も併せて開いた。

数値や事実の主張については、原典の抄録で裏を取ることを原則とした。ACM Digital Library、IEEE Xplore、ScienceDirect、Research Squareの各本文ページはこの環境からのアクセスが拒否されたため、抄録はOpenAlex、OpenAIRE、Europe PMC、arXiv、情報処理学会電子図書館、CiNii Researchの各記録から取得した。この方法で、SpiKeyの「33万本以上から3本へ」、Ivanovaらの「0.005重量パーセント」、PrinTrackerの「14台」と「92パーセント」、Vaidyaらの「数千台を99パーセント」、Marakisらの「63個の複製」、Wangらの「40本のうち38本、95パーセント」、Weiらの「深さ15ミリメートルまでX線で読める」といった数値の主張が、いずれも原典の抄録の記述と一致することを確認した。

本文への手入れは31か所に及ぶ。そのうち、はっきりした誤りを直したものが4件、内容の記述を原典の抄録に合わせて書き直したものが3件、書誌の欠けを補ったものと確認先を明記したものが残りである。内訳を順に書く。第一に、Vaidyaらの論文の年を2022年から2023年に直した。Crossrefの登録日である2022年3月15日はオンライン先行公開の日付であり、冊子としてはDigital Threats: Research and Practiceの第4巻第2号に論文番号20として収録されているためである。巻号と論文番号も補った。第二に、SuhとDevadasのDAC 2007論文のページを「p.9」から「pp.9-14」に直した。第三に、Al Faruqueらの論文とSongらの論文について、抄録が取得できなかったという注記を外し、抄録に書かれている内容と数値（軸の予測の平均正解率78.35パーセントと長さの予測の平均誤差17.82パーセント、平均傾向誤差5.87パーセントと9.67パーセント）を本文に補った。第四に、Wangらの2026年の査読前原稿について、抄録をEurope PMCで入手できたので、内容が不明であるという記述を実際の内容の記述に置き換えた。素子は二酸化クロムの微粒子を絹フィブロインに分散させた磁気複合媒体であり、受動的な3Dプリント構造の共鳴ではないことが判明したので、脅威が「高」に上がりうるという留保も外した。第五に、LaxtonらとRameshらの論文について、Crossrefでは副題が落ちた形で登録されている旨を注記し、会議名を予稿集の正式な名称に直した。第六に、Pappuらの1966年ではなく2002年の論文の記述を、抄録で確かめられる範囲と本文にしか書かれていない範囲とに切り分けた。第七に、ScientificReportsの2本、Science、Kac、Gordonら、Ivanovaら、Weiら、Yanamandraら、Wangら（法科学）、Chenら、Škorić、Immlerらの各項目に、抜けていた巻号または論文番号を補った。第八に、古原らの記事に副題を補った。第九に、ImmlerとUppundの項目に、この論文が多値アルファベットの物理複製困難関数に対してLee距離に基づく誤り訂正符号を提案しているという、CipherFluteの符号設計に直接関わる事実を書き加えた。第十に、冒頭の要約でSongらの攻撃を「動作音から」と書いていたのを、音響と磁気の両方のセンサを使うという原典どおりの記述に直した。第十一に、冒頭の要約で音響物理複製困難関数を名乗る二つの研究を「いずれも電子部品または能動的な音源を前提としている」と書いていたのを、Wangらの構成が磁気複合媒体を標準的な再生装置で読むものであるという事実に基づく記述に直した。前の書き方は原典を読まない推測であった。第十二に、松本らの2025年の論文にDOI（10.20729/0002001672）と情報処理学会電子図書館の記録の場所、および英語題名を補った。

はっきりした誤りとして直したのは、Vaidyaらの年、SuhとDevadasのページ範囲、要約におけるSongらの攻撃の記述、要約における音響物理複製困難関数の二例の性質の記述の4件である。存在しない文献の捏造は1件も見つからなかった。

実在が確認できずに削除した文献は1件もない。「未検証のまま残ったもの」の節へ新たに移した文献も1件もない。その節には、書誌そのものは確認できたが誌面で確かめきれていない細部（Ivanovaらの第3著者の中間名の頭文字、SuhとDevadasのページ範囲）と、もともと到達できていない項目を整理して残した。したがって「検証で削除したもの」の節は設けていない。

「見つからなかったこと」の節にある主張のうち、新規性の判断に直接効く二つを独立に再検証した。ひとつは、音響と物理複製困難関数を結び付けた研究が二つしかないという主張である。Crossrefの題名検索で「unclonable」と音響系の語を組み合わせて探し直し、題名の水準では確かにVaidyaらとWangらの二つしかないことを確かめた。もうひとつは、ヒューマンコンピュータインタラクションとデジタルファブリケーションの会議に「unclonable」を題名に含む論文が無いという主張である。CrossrefでACMのDOI接頭辞に限って会議論文を洗い出し、掲載会議が設計自動化と安全性の会議に限られることを確かめた。どちらの主張も裏付けられたので、CipherFluteの新規性に対する「高」の脅威は、この切り口では引き続き見つかっていないと結論する。

なお、この再検証では検索エンジンによる自由検索が使えず（この作業環境の検索回数の上限に達していた）、OpenAlexとSemantic ScholarとDBLPも短時間で応答制限に落ちた。したがって被引用をたどる芋づる式の探索は今回も深められていない。書誌の実在という点では45件すべてに裏が取れたが、まだ知られていない先行研究を掘り出す作業は残っている。
