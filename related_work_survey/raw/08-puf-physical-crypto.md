# 物理複製困難関数と物理的な一方向性関数

（担当した切り口の調査結果である。指示されたファイルパスが `undefined/raw/08-puf-physical-crypto.md` となっていて先頭部分が壊れていたため、他の切り口の出力が置かれている `related_work_survey/raw/` の下に同じファイル名で書き出した。）

## この切り口の要約

物理複製困難関数の研究は、Pappuらが2002年にScienceで発表した「Physical One-Way Functions」を起点として、半導体の製造ばらつきを使うシリコン系、光散乱体を使う光学系、紙や表面の微細構造を使う個体識別系へと広がってきた。日本語圏では同じ概念が「人工物メトリクス」と呼ばれ、松本勉らのナノ人工物メトリクスが代表的である。この分野の中心的な主張は「物理的な乱れは複製できないので、それ自体を鍵や識別子にしてよい」というものであり、CipherFluteが宣言している「物理層に秘匿の力はまったく無い」という立場とは正反対に見える。しかし調べてみると、両者は矛盾していない。物理複製困難関数が使う乱れは、製造者自身にも制御できない微視的な乱れであって、設計図どおりに作られる巨視的な形状ではない。CipherFluteの管長は設計図そのものであり、物理複製困難関数の要件を最初から満たさない。したがってCipherFluteの宣言は学術的に正しく、むしろ物理複製困難関数の定義に忠実である。

複製の容易さについても裏付けが取れた。Laxtonらは写真から物理鍵の刻みを復元して複製できることを示し、Rameshらは鍵を鍵穴に差し込む音だけから刻みを推定できることを示した。Al FaruqueらとSongらは3Dプリンタの動作音から印刷中の形状を復元できることを示している。CipherFluteの笛は形状を計測されれば無音で読めるという主張は、これらの結果と整合する。さらにMarakisらは光学的物理複製困難関数の複製に成功しており、物理複製困難性そのものが絶対ではないことも分かった。

一方で、能動的な音源も電子部品も持たない3Dプリント共鳴体の共鳴周波数のばらつきを物理複製困難関数として使う研究は、今回の調査では見つからなかった。「音響物理複製困難関数」を名乗る研究はセンサノードを対象とするVaidyaらのものと2026年の査読前原稿だけであり、いずれも電子部品または能動的な音源を前提としている。CipherFluteを物理複製困難関数の方向へ発展させる道は、学術的には空いている。

## 新規性への脅威が大きい文献

脅威が「高」に相当する文献、すなわちCipherFluteの主要な主張を崩す文献は見つからなかった。以下はすべて「中」であり、必ず引用して差分を述べるべきものである。脅威の大きい順に並べた。

### 1. Sensor Identification via Acoustic Physically Unclonable Function

- 著者は Girish Vaidya, T. V. Prabhakar, Nithish Gnani, Ryan Shah, Shishir Nagaraja である。
- Digital Threats: Research and Practice（ACM）, 2022年, pp.1-25。
- 確認先は https://doi.org/10.1145/3488306 である（Crossrefの書誌登録で題名・著者・掲載誌・ページを確認した）。
- 市販部品で組んだセンサノードには、識別用の専用ハードウェアを追加できないという問題がある。著者らはノードが持つ音響部品の製造公差に由来する固有性と、設置場所に由来する音場の応答とを組み合わせ、「音響物理複製困難関数」と名付けた識別子を提案している。固有性の成分は製造公差から導かれるため複製困難であり、位置の成分は音響的なフィンガープリンティングによって得られる。数週間にわたる実運用で、数千台規模を99パーセントの精度で識別しつつ、機器の移動も検知できることを示した。合成音場のなかでの物理的な位置を、識別子としてだけでなく機器の物理的完全性の検証にも使っている。
- CipherFluteとの関係は、「音響」と「物理複製困難関数」を結び付けた先行例として最も近いという点にある。ただし対象は電源とマイクロホンを持つセンサノードであり、読み出しには能動的な音源と信号処理が要る。CipherFluteは電源も電子部品も持たない受動的な笛であり、しかも運ぶのは識別子ではなく利用者が指定した任意のビット列である。さらにCipherFluteは製造ばらつきを情報源ではなく雑音として扱い、基準笛で打ち消している。この「ばらつきを消す設計」と「ばらつきを使う設計」の対比は、論文で明示的に書く価値がある。
- 脅威の度合いは「中」である。用語「acoustic PUF」を先に取られているため、CipherFluteが不用意に音響と物理複製困難性を結び付けて語ると先行研究と衝突する。ただし読み出し機構も目的も異なるので、主張が崩れることはない。

### 2. Reconsidering Physical Key Secrecy: Teleduplication via Optical Decoding

- 著者は Benjamin Laxton, Kai Wang, Stefan Savage である。
- ACM Conference on Computer and Communications Security（CCS）2008, pp.469-478。
- 確認先は https://doi.org/10.1145/1455770.1455830 である。
- 物理錠の防御は、鍵の情報内容が私的であること、すなわち複製には鍵の所持か切削情報の事前知識が要ることを前提にしている。著者らはこの前提が撮像技術の普及によって崩れることを示した。ありふれた撮影機材と標準的な計算機視覚のアルゴリズムだけで、離れた場所から鍵の刻みコードを完全かつ正確に読み取り、精密な複製を切削できることを実証している。試作システムをSneakeyと名付け、実験室と実環境の両方で、米国で最も普及している住宅用の鍵に対して有効性を評価した。
- CipherFluteとの関係は極めて直接的である。CipherFluteは「形状を計測されれば無音で読める、複製も容易である」と宣言しているが、これはまさに本論文が物理鍵について示した結果を笛に置き換えたものである。CipherFluteの脅威モデルの正当化として、この文献を引くのが最も強い。逆に言えば、CipherFluteが「物理層に秘匿がある」と主張していたら、この文献によって直ちに否定されていた。
- 脅威の度合いは「中」である。CipherFluteの主張を崩すのではなく支えるが、引用しないと脅威モデルの記述が学術的な裏付けを欠く。

### 3. Listen to Your Key: Towards Acoustics-based Physical Key Inference（SpiKey）

- 著者は Soundarya Ramesh, Harini Ramprasad, Jun Han である。
- ACM International Workshop on Mobile Computing Systems and Applications（HotMobile）2020, pp.3-8。
- 確認先は https://doi.org/10.1145/3376897.3377853 である。
- 物理錠は錠前破りに弱いが、専用の道具と訓練が要り、怪しまれやすいので依然として広く使われている。著者らはSpiKeyという攻撃を提案し、攻撃者に必要なものをスマートフォンのマイクロホンだけに引き下げた。被害者が鍵を差し込むときに出る音を録音し、聞こえるクリック音の時間差から鍵の刻みの深さを推定する。実録音に基づくシミュレーションで、33万本以上の鍵の候補集合を、最頻のケースでは3本にまで絞り込めることを示した。
- CipherFluteとの関係は二重である。第一に、音が形状を漏らすという事実そのものがCipherFluteの脅威モデルを裏付ける。第二に、CipherFluteは「吹いた音の高さを符号として読む」設計なので、正規の読み出しと攻撃者の盗聴とが同じ物理量を共有している。すなわち利用者が読み出しのために吹いた音を録音されれば、それだけで秘密が漏れる。この点は論文中の脅威モデルで明記すべきであり、SpiKeyはその最良の引用先である。
- 脅威の度合いは「中」である。CipherFluteの新規性は崩さないが、音響的な盗聴という攻撃面を先に定式化しているので、引用と差分の記述が要る。

### 4. Unclonable security features for additive manufacturing

- 著者は O. Ivanova, A. Elliott, T. A. Campbell, C. B. Williams である。
- Additive Manufacturing, 2014年, pp.24-31。
- 確認先は https://doi.org/10.1016/j.addma.2014.07.001 である（Crossrefで書誌を確認し、OpenAIREの抄録記録で内容を確認した）。
- 積層造形が複数材料を部品の内部に選択的に配置できることを利用して、造形物そのものに物理的なセキュリティ機能を作り込む方法を提案している。紫外線を吸収して可視光を出す量子ドットを分散させた光硬化樹脂を作り、材料噴射方式の3Dプリンタで物体の内部に埋め込む。巨視的には規則正しく見えても、噴射液滴の単位では微視的に確率的な配置になるため、この乱れが物理複製困難関数の中核要素になると論じている。量子ドットの添加量が0.005重量パーセント程度でも蛍光顕微鏡で内部から検出でき、同じ濃度では肉眼には見えないことを示した。顕微鏡の倍率を変えることで三次元的な多層のセキュリティ模様が作れるという展望も示している。
- CipherFluteとの関係は、「3Dプリント物に物理複製困難関数を持たせる」という発想の代表的な先行例であるという点である。CipherFluteは同じく3Dプリント物に秘密を持たせるが、乱れではなく設計どおりの管長を使い、読み出しには顕微鏡ではなく人の息を使う。装置が要らないことと、識別ではなく任意のビット列を運ぶことが差分である。
- 脅威の度合いは「中」である。CipherFluteが「3Dプリント物にセキュリティ機能を埋め込む研究」の系譜に自分を置くなら、この文献を落とすことはできない。

### 5. 3D Unclonable Optical Identity for Universal Product Verification

- 著者は Chenxing Wang, Lily Raymond, Yifei Jin, Alireza Tavakkoli, Haoting Shen である。
- IEEE International Symposium on Hardware Oriented Security and Trust（HOST）2021, pp.136-146。
- 確認先は https://doi.org/10.1109/HOST49136.2021.9702273 である。
- 通し番号やバーコードのような従来の識別手段は容易に複製できる。物理複製困難関数やナノ化学材料を使う新しい識別手段は微小な乱れを利用して複製を難しくするが、前者は電子機器にしか使えず、後者は特殊な製造工程か不便な検証手順を要する。著者らはこれらの欠点に対処するため、微細構造がランダムな三次元のタグを提案し、構造の再現が技術的に難しいことによって複製を防ぐ。低コストで作れて、固体表面を持つほとんどの製品に適用でき、携帯電話程度の機材で検証できると主張している。タグの光学画像を撮り、機械学習による物体検出で強化した検証アルゴリズムを開発して、試作タグで検証の信頼性を実証した。
- CipherFluteとの関係は、電子部品を持たない三次元の物体に複製困難な同一性を持たせ、身近な機材で検証するという目標が近い点にある。ただし読み出しは光学であって音響ではなく、運ぶのは同一性であって秘密のビット列ではない。
- 脅威の度合いは「中」である。「電子部品なしの物体に検証可能な同一性を与える」という主張の一部が重なるため、差分を明示する必要がある。

### 6. Acoustic Side-Channel Attacks on Additive Manufacturing Systems

- 著者は Mohammad Abdullah Al Faruque, Sujit Rokka Chhetri, Arquimedes Canedo, Jiang Wan である。
- ACM/IEEE International Conference on Cyber-Physical Systems（ICCPS）2016, pp.1-10。
- 確認先は https://doi.org/10.1109/ICCPS.2016.7479068 である。
- 3Dプリンタが動作するときに出す音には、ステッピングモータの動きに由来する情報が含まれている。著者らはこの音響的な副次経路から、印刷中の物体の形状を復元できることを示した。設計データに直接触れなくても、印刷現場で音を録るだけで知的財産が漏れるという主張である。（抄録の全文は一次資料から取得できなかったため、内容の記述は題名と会議名、および広く引用されている主旨の範囲にとどめた。）
- CipherFluteとの関係は、笛の形状という秘密が「印刷の瞬間」に漏れうるという点にある。CipherFluteは秘密を含む笛を利用者自身が家庭用プリンタで印刷する運用を想定しているので、印刷現場に録音機があれば秘密が漏れる。脅威モデルに「製造時の副次経路」を書き足す根拠になる。
- 脅威の度合いは「中」である。CipherFluteの主張は崩さないが、脅威モデルの完全性に関わるので引用が要る。

### 7. My Smartphone Knows What You Print: Exploring Smartphone-based Side-channel Attacks against 3D Printers

- 著者は Chen Song, Feng Lin, Zhongjie Ba, Kui Ren, Chi Zhou, Wenyao Xu である。
- ACM Conference on Computer and Communications Security（CCS）2016, pp.895-907。
- 確認先は https://doi.org/10.1145/2976749.2978300 である。
- 3Dプリンタのそばに置いたスマートフォンの内蔵センサだけを使い、印刷されている物体の形状を推定する攻撃を示した研究である。音響センサと磁気センサの信号からノズルの動きを再構成する。専用の計測器を持たない攻撃者でも実行できることが要点である。（抄録の全文は一次資料から取得できなかったため、記述は題名と会議名、および主旨の範囲にとどめた。）
- CipherFluteとの関係は前項と同じで、製造時の副次経路による漏洩である。攻撃の敷居が「スマートフォンだけ」というところまで下がっている点で、家庭での印刷を前提とするCipherFluteにはより現実的な脅威である。
- 脅威の度合いは「中」である。

### 8. Physical One-Way Functions

- 著者は Ravikanth Pappu, Ben Recht, Jason Taylor, Neil Gershenfeld である。
- Science, 2002年, pp.2026-2030。
- 確認先は https://doi.org/10.1126/science.1074376 である。
- 近代の暗号技術は一方向性関数の上に成り立っているが、著者らはその類似物を物理的な系で構成した。透明な樹脂のなかに微小球をランダムに分散させた三次元の散乱体にレーザ光を当て、生じるスペックル模様を応答とする。入射角などの問い掛けに対して応答が定まり、応答から構造を逆算することも同じ構造を作り直すこともできない。この構成を「物理的一方向性関数」と呼び、鍵の生成や認証に使えることを示した。この論文が物理複製困難関数という分野の出発点になっている。
- CipherFluteとの関係は、CipherFluteが「そうではないもの」を定義する基準点になるという点である。CipherFluteの笛は設計図どおりの管長を持ち、形状から応答が完全に予測でき、同じ設計ファイルから何本でも同じ笛が作れる。つまり物理的一方向性関数の要件を意図的に満たしていない。この対比を明示すれば、CipherFluteの脅威モデルの宣言は「弱さの告白」ではなく「定義上の位置づけ」として読める。
- 脅威の度合いは「中」である。主張は崩さないが、この文献との対比を書かないと査読者から「なぜ物理複製困難関数にしないのか」と必ず問われる。

### 9. PrinTracker: Fingerprinting 3D Printers using Commodity Scanners

- 著者は Zhengxiong Li, Aditya Singh Rathore, Chen Song, Sheng Wei, Yanzhi Wang, Wenyao Xu である。
- ACM Conference on Computer and Communications Security（CCS）2018, pp.1306-1323。
- 確認先は https://doi.org/10.1145/3243734.3243735 である。
- 3Dプリンタが違法な道具の製造に使われる懸念に対して、印刷物からその出所のプリンタを特定する手法を提案している。情報埋め込みや電子透かしは製造工程を管理できる場合にしか使えないので、犯罪捜査には向かないというのが出発点である。著者らは、プリンタの機械的な不完全性が造形線の形成にばらつきを生み、それが繰り返し現れて固有の質感になると論じ、これを指紋として使う。14台のプリンタで高い精度を得て、試料の面積や位置や工程が制約された不利な条件でも92パーセントの精度を保った。
- CipherFluteとの関係は二つある。第一に、CipherFluteの笛には印刷したプリンタの指紋が残るので、日用品への偽装が「誰が作ったか」の匿名性までは保証しないという注意になる。第二に、笛の造形ばらつきを積極的に使えば物理複製困難関数の方向へ発展させられるという可能性を示す先行例でもある。
- 脅威の度合いは「中」である。CipherFluteが偽装による探索コストの引き上げを主張するとき、出所の追跡可能性という残余リスクを述べる根拠になる。

### 10. Nano-artifact metrics based on random collapse of resist（およびナノ人工物メトリクスの一連の研究）

- 著者は Tsutomu Matsumoto, Morihisa Hoga, Yasuyuki Ohyagi, Mikio Ishikawa, Makoto Naruse, Kenta Hanaki, Ryosuke Suzuki, Daiki Sekiguchi ほかである。
- Scientific Reports, 2014年。確認先は https://doi.org/10.1038/srep06142 である。
- 関連する続報として Optical nano artifact metrics using silicon random nanostructures（Scientific Reports, 2016年, https://doi.org/10.1038/srep32438 ）がある。
- 日本語の最新の成果として、宮本岩麒, 岩橋虎, 吉田直樹, 吉岡克成, 松本勉「ナノ人工物メトリクスの耐クローン性：シンプルな白色干渉計の有効性」情報処理学会論文誌, 第66巻第3号, pp.545-554, 2025年がある。確認先は https://cir.nii.ac.jp/crid/1390022067669403520 である。
- 人工物メトリクスは、物体が本来持つ特性を認証と耐クローン性に使う情報セキュリティ技術である、と定義されている。著者らは電子線描画でレジストの柱を意図的にランダムに倒壊させ、10ナノメートル未満という描画装置の解像度より細かい形態を作り出した。他人受入率、本人拒否率、耐クローン率を評価して、高い水準のセキュリティ用途の要件を満たすことを示している。2025年の論文は、高価な計測器でなく簡素な白色干渉計でも同等の照合精度と耐クローン性が得られることを示した。
- CipherFluteとの関係は、日本語圏における「物理複製困難関数」の呼称と評価尺度の標準がここにあるという点である。CipherFluteは日本語の学会に投稿するので、「人工物メトリクスではない」ことを人工物メトリクスの語彙で言う必要がある。具体的には、CipherFluteの笛には他人受入率も耐クローン率も定義できず、そもそも同一設計から同一の応答を出すことが目的である、と書けばよい。
- 脅威の度合いは「中」である。日本語圏の読者に対して位置づけを説明する義務が生じる。

### 11. Clones of the Unclonable: Nanoduplicating Optical PUFs and Applications

- 著者は E. Marakis, U. Rührmair, M. Lachner, R. Uppu, B. Škorić, P. W. H. Pinkse である。
- arXiv:2212.12495, 2022年12月23日投稿。
- 確認先は https://arxiv.org/abs/2212.12495 である（arXivの論文ページで題名・著者・抄録・投稿日を確認した。査読誌への掲載は確認できていない）。
- 物理複製困難関数の分野が置いてきた基礎的な仮定、すなわち「散乱構造は複製できない」という仮定が破れることを実証した研究である。著者らは自明でない光散乱構造の複製を63個作り、本質的に同じ散乱挙動を示すことを確かめた。これは物理複製困難関数を使う一部の方式の安全性を損なう一方で、新しい応用も開く。具体的には、価値ある品物のための偽造不能なラベルや、秘密鍵を内部に持たない暗号化復号装置が挙げられている。
- CipherFluteとの関係は、「物理層に秘匿を期待しない」というCipherFluteの設計判断が保守的で正しいことを示す根拠になる点である。物理複製困難性は絶対ではなく、専用の設備があれば破られうる。CipherFluteが秘匿を秘密分散だけに負わせているのは、この意味で堅実である。
- 脅威の度合いは「中」である。CipherFluteの主張を支える側だが、査読者から「物理複製困難関数にすればよいのでは」と言われたときの反論材料として引用価値が高い。

### 12. 包絡線情報の相関による楽器の個体差識別

- 著者は小幡健作, 山崎芳男である。
- 日本音響学会研究発表会講演論文集, 2003年春季, 第2003巻第1号, pp.659-660。
- 確認先は https://cir.nii.ac.jp/crid/1570572700389150080 である（CiNii Researchの書誌記録で題名・著者・掲載・ページ・日付を確認した。抄録は記録されていない）。
- 同じ種類の楽器であっても個体ごとに音が違うという事実に着目し、音の包絡線情報の相関から個体を識別する試みを報告した2ページの発表である。
- CipherFluteとの関係は、「楽器の音から個体を見分ける」という、音響的な人工物メトリクスに最も近い日本語の先行例である点にある。CipherFluteは逆に、個体差を基準笛で打ち消して同じ設計の笛が同じ符号を返すようにしている。つまり同じ物理現象を、片方は識別の情報源として使い、もう片方は消すべき雑音として扱っている。この対比は日本語の論文で書くと分かりやすい。
- 脅威の度合いは「中」である。ただし2ページの発表であり、認証や鍵生成を目的としていないので、脅威というより位置づけの整理に使う文献である。

### 13. Listening to disorder: acoustic physical unclonable functions for audio-enabled secure authentication

- 著者は Yu Wang, Ying-Hao Fu, Zi-Ting Wang, Xin-Yu Cheng, Tao Wang, Yanqing Lu である。
- Research Squareの査読前原稿, 2026年。
- 確認先は https://doi.org/10.21203/rs.3.rs-9353152/v1 である（Crossrefの登録記録で題名・著者・種別・年を確認した。本文ページはアクセスが拒否され、抄録を読めなかった）。
- 題名から、音響的な乱れを利用した物理複製困難関数を、音声で読み出せる認証に使う提案だと読める。内容の詳細は確認できていないため、要約は書かない。
- CipherFluteとの関係は、「音響」と「物理複製困難関数」と「音で読む認証」という三つの要素が同時にそろっている点で最も近い可能性がある。ただし査読前であり、対象が散乱体か電子機器かも確認できていない。
- 脅威の度合いは「中」である。投稿までに本文を入手して確認することを強く勧める。もし受動的な3Dプリント構造の共鳴を使っていた場合には、脅威が「高」に上がる可能性がある。

## 背景として押さえるべき文献

以下はすべて脅威が「低」であり、背景として引用する程度でよい。書誌はすべてCrossrefまたはCiNii Researchで確認した。

- Blaise Gassend, Dwaine Clarke, Marten van Dijk, Srinivas Devadas: Silicon Physical Random Functions. ACM CCS 2002, pp.148-160. https://doi.org/10.1145/586110.586132 。半導体の遅延ばらつきを使う最初期の構成である。
- G. Edward Suh, Srinivas Devadas: Physical Unclonable Functions for Device Authentication and Secret Key Generation. ACM/IEEE DAC 2007, p.9. https://doi.org/10.1145/1278480.1278484 。機器認証と鍵生成という応用の定番である。
- Charles Herder, Meng-Day Yu, Farinaz Koushanfar, Srinivas Devadas: Physical Unclonable Functions and Applications: A Tutorial. Proceedings of the IEEE, 2014年, pp.1126-1141. https://doi.org/10.1109/JPROC.2014.2320516 。分野の教科書的な解説である。
- Ulrich Rührmair, Srinivas Devadas, Farinaz Koushanfar: Security Based on Physical Unclonability and Disorder. Introduction to Hardware Security and Trust（Springer）, 2011年, pp.65-102. https://doi.org/10.1007/978-1-4419-8080-9_4 。「乱れに基づく安全性」という枠組みの整理である。
- Ulrich Ruhrmair, Daniel E. Holcomb: PUFs at a Glance. DATE 2014, pp.1-6. https://doi.org/10.7873/DATE.2014.360 。短い総覧である。
- Ulrich Rührmair, Frank Sehnke, Jan Sölter, Gideon Dror, Srinivas Devadas, Jürgen Schmidhuber: Modeling Attacks on Physical Unclonable Functions. ACM CCS 2010, pp.237-249. https://doi.org/10.1145/1866307.1866335 。機械学習で応答を予測する攻撃であり、物理複製困難性の限界を示す。
- Clemens Helfmeier, Christian Boit, Dmitry Nedospasov, Jean-Pierre Seifert: Cloning Physically Unclonable Functions. IEEE HOST 2013, pp.1-6. https://doi.org/10.1109/HST.2013.6581556 。半導体の物理複製困難関数を実際に複製した報告である。
- Pim Tuyls, Geert-Jan Schrijen, Boris Škorić, Jan van Geloven, Nynke Verhaegh, Rob Wolters: Read-Proof Hardware from Protective Coatings. CHES 2006, pp.369-383. https://doi.org/10.1007/11894063_29 。被覆材の乱れから鍵を導く構成である。
- Boris Škorić: Quantum Readout of Physical Unclonable Functions. International Journal of Quantum Information, 2012年, 1250001. https://doi.org/10.1142/S0219749912500013 。読み出し側の信頼を不要にする発展である。
- Ravikanth Pappu: Physical Unclonable Functions: The First Fifty Years. ACM Workshop on Attacks and Solutions in Hardware Security（ASHES）2023, p.3. https://doi.org/10.1145/3605769.3623997 。分野の創始者による回顧である。
- James D. R. Buchanan ほか: 'Fingerprinting' documents and packaging. Nature, 2005年, p.475. https://doi.org/10.1038/436475a 。紙や包装の表面のレーザ反射で個体を識別する。
- William Clarkson, Tim Weyrich, Adam Finkelstein, Nadia Heninger, J. Alex Halderman, Edward W. Felten: Fingerprinting Blank Paper Using Commodity Scanners. IEEE Symposium on Security and Privacy 2009, pp.301-314. https://doi.org/10.1109/SP.2009.7 。市販のスキャナだけで白紙の繊維構造から個体識別する。
- Ashlesh Sharma, Lakshminarayanan Subramanian, Eric A. Brewer: PaperSpeckle: Microscopic Fingerprinting of Paper. ACM CCS 2011, pp.99-110. https://doi.org/10.1145/2046707.2046721 。紙の微視的なスペックルを指紋にする。
- Ehsan Toreini, Siamak F. Shahandashti, Feng Hao: Texture to the Rescue: Practical Paper Fingerprinting Based on Texture Patterns. ACM Transactions on Privacy and Security, 2017年, pp.1-29. https://doi.org/10.1145/3092816 。実用的な紙指紋である。
- Riikka Arppe, Thomas Just Sørensen: Physical unclonable functions generated through chemical methods for anti-counterfeiting. Nature Reviews Chemistry, 2017年. https://doi.org/10.1038/s41570-017-0031 。化学的に作る物理複製困難関数の総説である。
- Fei Chen, Gary Mac, Nikhil Gupta: Security features embedded in computer aided design (CAD) solid models for additive manufacturing. Materials & Design, 2017年, pp.182-194. https://doi.org/10.1016/j.matdes.2017.04.078 。設計データが盗まれても、印刷条件の組み合わせが合わないと良品にならないような設計上の仕掛けを提案している。CipherFluteの「設計ファイルの秘匿だけでは守れない」という論点に近い。
- Chao Wei, Zhe Sun, Yihe Huang, Lin Li: Embedding anti-counterfeiting features in metallic components via multiple material additive manufacturing. Additive Manufacturing, 2018年, pp.1-12. https://doi.org/10.1016/j.addma.2018.09.003 。金属部品の内部に別材料で二次元コードを埋め込み、X線で読む。内部に情報を隠す点でAirCodeやInfraStructsと同系統である。
- Bertrand Cambou ほか: Securing Additive Manufacturing with Blockchains and Distributed Physically Unclonable Functions. Cryptography, 2020年, 17. https://doi.org/10.3390/cryptography4020017 。積層造形の工程をブロックチェーンと物理複製困難関数で守る枠組みである。
- Aaron Pendino ほか: Additively Manufactured RF Electronics With Structurally Integrated Physically Unclonable Functions for Wireless System Security. IEEE Access, 2025年, pp.145042-145059. https://doi.org/10.1109/ACCESS.2025.3600010 。積層造形した高周波回路の構造そのものに物理複製困難関数を組み込む。
- Kaushik Yanamandra, Guan Lin Chen, Xianbo Xu, Gary Mac, Nikhil Gupta: Reverse engineering of additive manufactured composite part by toolpath reconstruction using imaging and machine learning. Composites Science and Technology, 2020年, 108318. https://doi.org/10.1016/j.compscitech.2020.108318 。印刷物の画像から工具経路を復元する。造形物からの逆解析が現実的であることを示す。
- Zhen Wang, Hao Zhou, Chao Ye, Changjiang Song, Taiqi Zang: Study on traces left on a mechanical lock picked by a 3D printed key in toolmarks examination. Forensic Science International, 2020年, 110514. https://doi.org/10.1016/j.forsciint.2020.110514 。3Dプリントした鍵で錠が実際に開くことを40本の試作で確かめ、95パーセントが開錠に成功したと報告している。物理鍵が3Dプリントで複製できるという事実の一次資料である。
- Anupam Das, Nikita Borisov, Matthew Caesar: Do You Hear What I Hear? Fingerprinting Smart Devices Through Embedded Acoustic Components. ACM CCS 2014, pp.441-452. https://doi.org/10.1145/2660267.2660325 。スピーカとマイクロホンの製造ばらつきから機器を識別する。
- Adriana Berdich ほか: Fingerprinting Smartphones Based on Microphone Characteristics From Environment Affected Recordings. IEEE Access, 2022年, pp.122399-122413. https://doi.org/10.1109/ACCESS.2022.3223375 。実環境の録音からマイクロホン個体を識別する。
- Oliver Willers, Christopher Huth, Jorge Guajardo, Helmut Seidel: MEMS Gyroscopes as Physical Unclonable Functions. ACM CCS 2016, pp.591-602. https://doi.org/10.1145/2976749.2978295 。機械式センサの製造ばらつきを物理複製困難関数にした例である。
- Monica Arenas, Huseyin Demirci, Gabriele Lenzini: Cholesteric Spherical Reflectors as Physical Unclonable Identifiers in Anti-counterfeiting. ARES 2021, pp.1-11. https://doi.org/10.1145/3465481.3465766 。物体に貼る複製困難な識別子である。
- Vincent Immler, Karthik Uppund: New Insights to Key Derivation for Tamper-Evident Physical Unclonable Functions. IACR Transactions on Cryptographic Hardware and Embedded Systems, 2019年, pp.30-65. https://doi.org/10.46586/tches.v2019.i3.30-65 。開封検知と鍵導出を兼ねる構成であり、CipherFluteが引いているJohnstonの封印評価と接続する。
- Mark Kac: Can One Hear the Shape of a Drum? The American Mathematical Monthly, 1966年, pp.1-23. https://doi.org/10.1080/00029890.1966.11970915 。
- Carolyn Gordon, David L. Webb, Scott Wolpert: One cannot hear the shape of a drum. Bulletin of the American Mathematical Society, 1992年, pp.134-138. https://doi.org/10.1090/S0273-0979-1992-00289-6 。この二つは、スペクトルから形状が一意に定まらない場合があるという古典的な結果である。CipherFluteは形状から音を決める向きにしか依存しないので影響はないが、「音から形状を復元して複製する」攻撃を論じるときに、原理的な限界と実際上の容易さを区別する材料になる。
- F. A. P. Petitcolas, R. J. Anderson, M. G. Kuhn: Information Hiding: A Survey. Proceedings of the IEEE, 1999年, pp.1062-1078. https://doi.org/10.1109/5.771065 。CipherFluteの物理層が提供しているものは秘匿ではなく情報隠蔽であるという整理を、この総説の語彙で書ける。
- 古原和邦, 時田俊雄, 松本勉: 「人工物メトリクスを用いた個体管理技術ガイダンス」の紹介. 自動認識, 第35巻第7号, pp.43-49, 2022年. https://cir.nii.ac.jp/crid/1520010853668296960 。日本語圏で人工物メトリクスを実務に適用するための指針を紹介した記事である。

## 未検証のまま残ったもの

- Yu Wangらの「Listening to disorder: acoustic physical unclonable functions for audio-enabled secure authentication」（Research Square, 2026年）は、Crossrefの登録記録で題名、著者、種別、公開年までは確認できたが、本文ページがアクセス拒否となり抄録を読めなかった。内容が確認できていないので、上の記述は題名から読み取れる範囲にとどめてある。
- Al Faruqueらの「Acoustic Side-Channel Attacks on Additive Manufacturing Systems」（ICCPS 2016）とSongらの「My Smartphone Knows What You Print」（CCS 2016）は、Crossrefで書誌を確認できたが、抄録の全文は一次資料から取得できなかった。内容の記述を題名と会議名から読み取れる範囲にとどめた。投稿前に本文を確認してほしい。
- 物理複製困難関数の総説類で「音響物理複製困難関数」の初期の例として修士論文が挙げられることがあると記憶しているが、今回の検索（OpenAlexの題名検索、arXivの全文検索、Crossrefの題名検索）では一次資料に到達できなかった。実在も書誌情報も確認できていないので、名前や年を書くことは避ける。もし引用したい場合は、Eindhoven工科大学あるいはPhilipsの技術報告の所蔵を直接確認する必要がある。
- 「人工物メトリクスを用いた個体管理技術ガイダンス」そのもの（紹介記事ではなく本体の文書）には到達できていない。発行元と正式名称を確認する必要がある。
- 暗号と情報セキュリティシンポジウム（SCIS）の予稿は電子的に公開されていないものが多く、人工物メトリクスの音響応用がSCISで発表されていないかどうかを確認できなかった。

## この切り口で見つからなかったこと

以下は、探したうえで「見つからなかった」と言えることである。CipherFluteの新規性の主張の根拠になるので、探索の範囲も併せて書く。

- 電源も電子部品も持たない受動的な3Dプリント共鳴体（笛、管、共鳴箱など）の共鳴周波数の製造ばらつきを、物理複製困難関数あるいは人工物メトリクスとして使う研究は見つからなかった。探索の範囲は、OpenAlexの題名検索と題名抄録検索（「acoustic PUF」「acoustic unclonable」「unclonable 3D printed」「unclonable additive manufacturing」など）、Crossrefの題名検索によるACM刊行物の横断（「unclonable」「physically unclonable」「physical unclonable」を題名に含む会議論文をすべて列挙して目視で確認）、arXivの全文検索である。
- 「acoustic PUF」または「acoustic physically unclonable function」を名乗る研究は、Vaidyaらのセンサノード識別と、2026年のResearch Squareの査読前原稿の二つしか見つからなかった。いずれも能動的な音源または電子部品を前提としており、人が息を吹き込んで読む構成ではない。
- CHI、UIST、TEI、SIGGRAPH、SCFといったヒューマンコンピュータインタラクションおよびデジタルファブリケーションの会議で、題名に「unclonable」を含む論文は、Crossrefで確認できたACM刊行物のなかに1件も存在しなかった。すなわち、日用品を作る研究の系譜と物理複製困難関数の系譜は、まだほとんど接続されていない。CipherFluteはこの二つの領域のあいだに立つ位置にある。
- 物理複製困難関数を用いて秘密分散の持ち分（シェア）を保護する3Dプリント物、という組み合わせは見つからなかった。Cambouらが積層造形の工程管理に分散的な物理複製困難関数を使っているが、これは工程の真正性のためであって、利用者の秘密の保管ではない。
- 息を吹き込んで読み出す物理的な鍵、あるいは笛の音高を符号として鍵素材にする研究は、物理複製困難関数の文脈では見つからなかった。音を出す受動的な物体を扱う先行研究（BlowholeやAcoustic Barcodes）は識別子やタグの読み出しが目的であり、暗号鍵やリカバリーシードのような秘密の運搬を目的としていない。
- 日本語圏の人工物メトリクスの研究は、レジスト倒壊によるナノ構造、レーザスペックル、パール顔料や白色顔料といった光学的な手段が中心であり、音響を使う人工物メトリクスは見つからなかった。CiNii Researchで「音響 PUF」「複製困難 物体 認証」を検索しても該当が0件であった。楽器の個体差識別（小幡・山崎, 2003年）は音響を使うが、認証や耐クローン性を目的としていない。
- 「物理層に秘匿の力はまったく無い」と明示的に宣言したうえで、秘匿をすべて秘密分散に負わせる、という設計方針を採る物理的な秘密保管の研究は、この切り口の範囲では見つからなかった。多くの研究はむしろ物理層に何らかの安全性を期待している。CipherFluteの宣言は、この分野の常識からするとかなり珍しい立場であり、そこを明示的に書けば独自性として読める。

## 調べ残した穴

- 調査の途中でOpenAlexの応答が制限（HTTP 429、再試行まで約24時間）になり、被引用のたどり直しを最後までできなかった。特に、Pappu 2002の被引用のうちデジタルファブリケーション寄りの枝と、Vaidyaの音響物理複製困難関数の被引用は追い切れていない。時間をおいて再度たどる価値がある。
- ACM Digital LibraryとIEEE Xploreの全文検索を直接使えなかった（いずれもアクセス拒否である）。ACMについてはCrossrefの題名検索で代替したが、題名に「unclonable」を含まず抄録や本文にだけ含むヒューマンコンピュータインタラクション系の論文は取りこぼしている可能性がある。
- Semantic ScholarとGoogle Scholarの被引用一覧を使えなかった（前者は応答制限、後者は自動アクセスの遮断）。芋づる式の探索が想定より浅い。
- 特許文献をまったく調べていない。3Dプリント物の音響的な認証や、笛を使った識別については特許が出ている可能性がある。査読論文よりも特許が先行しているという事態は、この種の応用寄りの技術ではしばしば起きる。
- カードを使う物理暗号（card-based cryptography）の系譜、すなわち電子計算機を使わずに秘密計算やゼロ知識証明を行う研究は、今回の切り口から外して調べていない。「電源を使わない暗号」という括りでCipherFluteを語るなら、この系譜との関係を別途整理する必要がある。
- 物理複製困難関数の応答から鍵を安定に取り出すための誤り訂正（fuzzy extractor、secure sketch）の理論は、名前を確認しただけで一次資料に当たっていない。CipherFluteがReed-Solomon符号を使う設計と、この理論的な枠組みとの関係は整理し切れていない。
- 材料や環境の変化による経年での応答のずれ（エイジング）に関する物理複製困難関数の研究は列挙しただけで内容を読んでいない。CipherFluteの笛が温度や湿度、樹脂の経年でどれだけ音高が動くかという議論に、この分野の評価尺度が使える可能性がある。
