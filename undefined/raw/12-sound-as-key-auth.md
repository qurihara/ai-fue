# 音を鍵とする認証の研究

この文書は、CipherFluteの位置づけを定めるための先行研究調査のうち、「音そのものを認証の要素として使う研究」という切り口を担当した結果である。

書誌情報の確認方法について最初に断っておく。今回の作業環境ではWeb検索の回数上限に達していたため、検索エンジンによる探索は使えなかった。そのかわりに、DOI登録機関であるCrossrefの書誌API（https://api.crossref.org/）、計算機科学の書誌データベースであるDBLP（https://dblp.org/）、日本語文献についてはCiNii Research（https://cir.nii.ac.jp/）、および学会自身の予稿集ページに直接あたって、著者・題名・会議名または雑誌名・巻号ページ・年を一件ずつ照合した。したがって以下に挙げる文献は、いずれも一次的な書誌記録の上で実在を確認したものである。確認できなかったものは末尾の「未検証のまま残ったもの」にまとめた。

## この切り口の要約

音を認証に使う研究は、大きく四つの流れに分かれることが分かった。第一に、旋律やリズムを人間の記憶の助けとして合言葉に使う流れがある。GibsonらのMusipass（NSPW 2009）を中心とする一連の仕事と、WobbrockのTapSongs（UIST 2009）やBeat-PIN（AsiaCCS 2018）のリズム認証がここに属する。第二に、周囲の環境音の一致を近接の証明に使う二要素認証の流れがあり、Sound-Proof（USENIX Security 2015）が代表である。第三に、音響チャネルを機器同士の鍵交換の補助路として使う機器ペアリングの流れがあり、Loud and Clear（ICDCS 2006）、HAPADEP（ISC 2008）、Acoustic Integrity Codes（WiSec 2020）が並ぶ。第四に、打鍵音やプリンタの動作音から秘密を推定する音響サイドチャネル攻撃の流れがある。

この四つの流れを通して見たとき、CipherFluteが取る「音の層に暗号学的な秘匿の力はまったく無いと最初から宣言する」という立場は、既存研究のなかでは珍しい。既存の音響認証は、音が盗聴されうるという事実を弱点として扱い、環境音の共有秘密性に頼るか、時間的な鮮度で盗聴を無効化するかの、どちらかで守ろうとしてきた。HaleviとSaxenaがCCS 2010で音響チャネルの秘匿性は仮定できないと実験的に示し、Acoustic Integrity Codesが音響チャネルを完全性専用の公開路として設計し直した系譜だけが、CipherFluteと同じ方向を向いている。ただしこれらはいずれも電源を持つ機器同士の通信の話であり、電源を持たない受動的な物体が音高の符号として鍵素材そのものを保持するという形は、今回調べた範囲では見つからなかった。したがってCipherFluteの新規性は、この切り口からは崩れない。一方で、3Dプリンタの動作音から造形物の形状が復元できるという一連の研究があるため、秘密を刻んだ笛を印刷している最中に音響サイドチャネルで秘密が漏れるという指摘は、脅威モデルの節に書き足しておかないと査読で突かれる。

## 新規性への脅威が大きい文献

### 1. Musipass: authenticating me softly with "my" song

- 著者: Marcia Gibson, Karen Renaud, Marc Conrad, Carsten Maple
- 発表: Proceedings of the 2009 Workshop on New Security Paradigms（NSPW 2009）, pp. 85-100, 2009年
- 確認先: https://doi.org/10.1145/1719030.1719043 （Crossrefの書誌記録で題名・著者・会議名・ページ・年を確認した）

利用者が自分で選んだ楽曲を認証の秘密として使う方式を提案した論文である。人間は歌の記憶を非常に長く保持し、しかも語句の記憶よりも忘れにくいという心理学の知見を出発点として、ログイン時には複数の候補音から自分の曲を認識させるという再認方式を設計している。文字列のパスワードが覚えられないという問題に対して、音の記憶という別の認知資源を持ち込んだ点が主張の中心である。同じ著者らはこの後、視覚障害や識字障害のある利用者に向けた設計制約の検討（i-Society 2010）と、音楽による認証の到達点をまとめた総説（Play That Funky Password!, 2015年）を書いており、この一群が「音を鍵とする認証」の直系の先行研究になっている。

CipherFluteとの関係を述べる。Musipassは秘密を人間の記憶のなかに置き、音はその記憶を呼び出す手がかりとして使う。CipherFluteは逆に、人間の記憶をまったく当てにせず、秘密を物体の管長として外部化し、音はその物体から符号を取り出すための搬送波として使う。したがって「音を鍵にする」という語彙は共有するが、秘密の置き場所が正反対である。

脅威の度合いは中である。理由は、査読者が「音を認証の鍵にすること自体は2009年に既にやられている」と指摘してくる筋がここにあるためで、引用したうえで、記憶に預けるのか物体に預けるのかという違いを明示的に書かないと新規性の説明が弱くなるからである。

### 2. TapSongs: tapping rhythm-based passwords on a single binary sensor

- 著者: Jacob O. Wobbrock
- 発表: Proceedings of the 22nd Annual ACM Symposium on User Interface Software and Technology（UIST 2009）, pp. 93-96, 2009年
- 確認先: https://doi.org/10.1145/1622176.1622194 （Crossrefの書誌記録で題名・著者・会議名・ページ・年を確認した）

利用者が知っている歌のリズムを、押しボタン一つの二値センサに叩き込むことで認証する方式である。入力できる情報は押した時刻の列だけであり、鍵の語彙は時間軸上のパターンとして定義される。歌という誰でも持っている記憶資源を、極端に貧しい入力装置の上に写し取った点が寄与である。認証の判定には、叩打の間隔と押下時間を基準の列と照合する統計的な手法を用いている。

CipherFluteとの関係を述べる。両者はどちらも「音楽的な構造を符号の語彙にする」という発想を共有する。ただしTapSongsが使うのは時間軸上のパターンであり、CipherFluteが使うのは周波数軸上の離散値である。CipherFluteの13スロットの半音刻みという設計は、時間ではなく音高を語彙にした点で区別できる。また、TapSongsは人間が叩くため入力の揺らぎが本質的な難しさになるのに対し、CipherFluteは物体が音高を決めるので揺らぎの原因は気温と息の強さに限られ、基準笛による比の測定で打ち消せる。

脅威の度合いは中である。理由は、UISTという同種の会場で「音楽を鍵にする」という発想が既に示されているため、必ず引用して差分を述べる必要があるからである。ただし符号の軸が時間か周波数かという違いは明確なので、主要な主張が崩れることはない。

### 3. Beat-PIN: A User Authentication Mechanism for Wearable Devices Through Secret Beats

- 著者: Ben Hutchins, Anudeep Reddy, Wenqiang Jin, Michael Zhou, Ming Li, Lei Yang
- 発表: Proceedings of the 2018 on Asia Conference on Computer and Communications Security（AsiaCCS 2018）, pp. 101-115, 2018年
- 確認先: https://doi.org/10.1145/3196494.3196543 （Crossrefの書誌記録で題名・著者・会議名・ページ・年を確認した）

画面が小さく文字入力が難しいウェアラブル機器のために、暗証番号のかわりに秘密の拍のパターンを叩いて認証する方式である。叩打の時系列から特徴量を取り出し、正規の利用者かどうかを判定する。TapSongsの発想を、装着型機器という現実の必要と、攻撃者を想定した安全性評価の枠組みへ持ち込んだ位置づけになる。鍵空間の大きさと、他人が肩越しに見て真似できるかという観察耐性の議論を含む。

CipherFluteとの関係を述べる。Beat-PINは、拍のパターンという音楽的な語彙を、暗証番号の代替として位置づけている。CipherFluteが音高を暗号資産の復元用情報の符号にするのと、目的が異なる。Beat-PINの秘密は人間が覚えて再現するものであり、CipherFluteの秘密は物体が保持して誰が吹いても同じ音が出るものである。CipherFluteは「誰が吹いても同じ」であることを利点として設計しているのに対し、Beat-PINは「本人しか再現できない」ことを安全性の根拠にしている点が対照的である。

脅威の度合いは中である。理由は、音楽的なパターンを鍵の語彙にするという発想が主要なセキュリティ会議で既に確立していることを示す文献であり、隣接研究として引用が必要だからである。

### 4. On pairing constrained wireless devices based on secrecy of auxiliary channels: the case of acoustic eavesdropping

- 著者: Tzipora Halevi, Nitesh Saxena
- 発表: Proceedings of the 17th ACM Conference on Computer and Communications Security（CCS 2010）, pp. 97-108, 2010年
- 確認先: https://doi.org/10.1145/1866307.1866319 （Crossrefの書誌記録で題名・著者・会議名・ページ・年を確認した）

入出力の乏しい機器同士を安全につなぐ手法のなかには、音や振動といった補助チャネルが秘密を運べると暗黙に仮定するものがある。この論文は、その仮定が成り立たないことを実験で示した。離れた場所に置いた盗聴用のマイクロホンで、音響チャネルを流れる秘密の情報が復元できることを実証し、補助チャネルの秘匿性に依存した設計を批判している。著者らはこの結果を発展させ、IEEE Transactions on Information Forensics and Security誌の論文（2013年）としてまとめ直している。

CipherFluteとの関係を述べる。CipherFluteは「音の層には暗号学的な秘匿の力はまったく無い」と宣言しているが、この宣言はこの論文が2010年に確立した知見と完全に一致する。つまりCipherFluteの脅威モデルの前半部分は、新しい洞察ではなく既知の結論の再確認である。逆に言えば、この論文を引くことでCipherFluteの立場に確かな根拠を与えられる。

脅威の度合いは中である。理由は、CipherFluteが脅威モデルの独自性として「音に秘匿を求めない」ことを掲げるなら、その論点は既に決着済みであると指摘されうるためで、引用したうえで、CipherFluteの寄与は秘匿の放棄そのものではなく、放棄したうえで秘密分散に全責任を移す設計にあると書き分ける必要があるからである。

### 5. Acoustic integrity codes: secure device pairing using short-range acoustic communication

- 著者: Florentin Putz, Flor Álvarez, Jiska Classen
- 発表: Proceedings of the 13th ACM Conference on Security and Privacy in Wireless and Mobile Networks（WiSec 2020）, pp. 31-41, 2020年
- 確認先: https://doi.org/10.1145/3395351.3399420 （Crossrefの書誌記録で題名・著者・会議名・ページ・年を確認した）

短距離の音響通信を使って機器を安全に対応づける方式を提案した論文である。設計の核心は、音響チャネルに秘匿性をいっさい期待せず、かわりに完全性だけを保証する符号を載せる点にある。攻撃者が音を聞くことは前提として許し、そのうえで攻撃者が符号を書き換えたり打ち消したりできないような符号化を与えることで、盗聴されても安全な鍵確立を実現している。

CipherFluteとの関係を述べる。「音は公開チャネルであって秘匿はしない」というCipherFluteの立場と、設計思想がもっとも近い先行研究である。ただし守ろうとしているものが違う。Acoustic Integrity Codesが守るのは通信の完全性であり、能動的な攻撃者が符号を改変できないことを目標にしている。CipherFluteが音の層に求めているのは完全性ですらなく、誤り訂正符号による読み取りの頑健性だけであり、安全性はすべて秘密分散に委ねている。したがって「音響チャネルに何を期待し何を期待しないか」という設計の分節において、両者は近い場所にありながら違う点に立っている。

脅威の度合いは中である。理由は、音響チャネルを公開路として扱う立場そのものは既に確立していることを示す文献であり、これを引かないと「音に秘匿を求めない」という宣言が唐突に見えるからである。

### 6. Sound-Proof: Usable Two-Factor Authentication Based on Ambient Sound

- 著者: Nikolaos Karapanos, Claudio Marforio, Claudio Soriente, Srdjan Capkun
- 発表: 24th USENIX Security Symposium（USENIX Security 2015）, pp. 483-498, 2015年
- 確認先: https://www.usenix.org/conference/usenixsecurity15/technical-sessions/presentation/karapanos （DBLPの書誌記録および学会の予稿集ページで題名・著者・会議名・ページ・年を確認した）

パソコンと携帯電話が同じ場所にあることを、両者のマイクロホンが拾った周囲の音の一致によって確かめ、利用者に何も操作させずに二要素認証を成立させる方式である。利用者は携帯電話を取り出す必要すらない。音の一致度を相互相関で測り、閾値で判定する。この方式については後に、共在する攻撃者や音を予測できる攻撃者に対して脆弱であることが示され、同じ問題意識からListening Watch（WiSec 2018）と、その発展であるSound-based Two-factor Authentication: Vulnerabilities and Redesign（ACM Transactions on Privacy and Security誌, 2024年, https://doi.org/10.1145/3632175 ）が提案されている。後者は、受動的に環境音を聞くのではなく、ブラウザが能動的に乱数から生成した音声を鳴らすことで鮮度を確保する設計に変えている。

CipherFluteとの関係を述べる。Sound-Proofは音を「共有された秘密に近いもの」として扱う。同じ場所にいる者だけが同じ音を聞ける、という前提に安全性を置いているため、盗聴とリプレイが本質的な脅威になる。CipherFluteは音の共有秘密性をいっさい前提にしないため、リプレイ攻撃も盗聴も脅威として定義されない。この対比は、CipherFluteの位置づけを説明する材料としてそのまま使える。

脅威の度合いは中である。理由は、音を認証要素として使う研究の代表例であり、CipherFluteが「音は公開チャネルである」と述べるとき、その主張が既存の音響認証のどこに位置するかを説明するために必ず引用が要るからである。

### 7. My Smartphone Knows What You Print: Exploring Smartphone-based Side-channel Attacks Against 3D Printers

- 著者: Chen Song, Feng Lin, Zhongjie Ba, Kui Ren, Chi Zhou, Wenyao Xu
- 発表: Proceedings of the 2016 ACM SIGSAC Conference on Computer and Communications Security（CCS 2016）, pp. 895-907, 2016年
- 確認先: https://doi.org/10.1145/2976749.2978300 （Crossrefの書誌記録で題名・著者・会議名・ページ・年を確認した）

3Dプリンタのそばに置いた携帯電話のマイクロホンと加速度センサだけで、印刷中の造形物の形状を復元できることを示した論文である。ノズルの移動音と振動からノズルの軌跡を推定し、造形物の輪郭を再構成する。同じ問題を扱った独立の研究として、Al Faruqueらの Acoustic Side-Channel Attacks on Additive Manufacturing Systems（ICCPS 2016, https://doi.org/10.1109/iccps.2016.7479068 ）と、その拡張であるACM Transactions on Cyber-Physical Systems誌の論文（2017年, https://doi.org/10.1145/3078622 ）があり、対策側としてQuietPrint（ACM Cyber-Physical System Security Workshop, 2026年, https://doi.org/10.1145/3775042.3807880 ）が提案されている。

CipherFluteとの関係を述べる。CipherFluteの秘密は管長という形状そのものであるから、形状が復元されれば秘密が復元される。この一連の研究は、印刷という製造工程の最中に、音だけで形状が漏れうることを示している。CipherFluteの脅威モデルは「形状を計測されれば無音で読める」ことを既に認めているが、その計測が完成後の物体に対してではなく、製造中に離れた場所から可能であるという点までは書かれていない。ここは加筆が必要である。

脅威の度合いは中である。理由は、CipherFluteの新規性そのものを崩す研究ではないが、脅威モデルの記述に明らかな穴を作る研究であり、引用したうえで「印刷環境も秘密の一部として扱う必要がある」と書かなければ、査読で弱点を突かれるからである。

### 8. Listen to Your Key: Towards Acoustics-based Physical Key Inference

- 著者: Soundarya Ramesh, Harini Ramprasad, Jun Han
- 発表: Proceedings of the 21st International Workshop on Mobile Computing Systems and Applications（HotMobile 2020）, pp. 3-8, 2020年
- 確認先: https://doi.org/10.1145/3376897.3377853 （DBLPの書誌記録で題名・著者・会議名・ページ・年を確認した）

物理的な鍵を錠に差し込むときに出る、山と谷が錠のピンに当たる小さな音を録音し、そこから鍵の刻みの深さを推定して合鍵を作る攻撃を示した論文である。システムの名前はSpiKeyである。鍵という物理的な秘密が、その物体を使うときに出る音によって漏れることを示した点が寄与である。

CipherFluteとの関係を述べる。CipherFluteは「音を鳴らして秘密を読み出す」ことを正規の利用者の手続きとして設計しているが、この論文は「物理的な秘密が音で漏れる」ことを攻撃として示している。同じ物理現象を、一方は機能として、他方は脆弱性として扱っている点で、対比の材料としてきわめて有用である。CipherFluteが物理層に秘匿を求めないという立場を取ることの正しさを、外側から補強する文献でもある。

脅威の度合いは中である。理由は、物体が発する音がその物体の秘密を明かすという構図が既に確立していることを示すため、CipherFluteの脅威モデルの記述で必ず参照すべきだからである。ただし目的も対象も異なるので、新規性そのものは脅かさない。

### 9. HAPADEP: Human-Assisted Pure Audio Device Pairing

- 著者: Claudio Soriente, Gene Tsudik, Ersin Uzun
- 発表: Information Security Conference（ISC 2008）, Lecture Notes in Computer Science, pp. 385-400, 2008年
- 確認先: https://doi.org/10.1007/978-3-540-85886-7_27 （DBLPの書誌記録で題名・著者・会議名・ページ・年を確認した）

無線の共通路をいっさい使わず、音だけで機器同士に鍵素材を渡し、人間が耳で確認することでその真正性を担保する方式である。まず機器が鍵素材を音として送り、続いて短い確認用の旋律を鳴らして、人間が二つの機器から同じ旋律が聞こえることを確かめる。音を、秘密の通り道ではなく、人間が監査できる公開の通り道として使っている点が特徴である。

CipherFluteとの関係を述べる。音を鍵素材の搬送路として使い、しかもその音が公開であることを前提にする点で、CipherFluteと発想が近い。違いは、HAPADEPが電源を持つ機器の間の通信であり、鍵素材はその場で生成される一時的なものであるのに対し、CipherFluteでは物体そのものが恒久的に鍵素材を保持し、送信側に電源がまったく要らない点である。

脅威の度合いは中である。理由は、「音で鍵素材を運ぶ」という行為の先行例として、査読者が真っ先に思い浮かべる種類の研究であり、引用して差分を述べておく必要があるからである。

### 10. Talking to Strangers: Authentication in Ad-Hoc Wireless Networks / Loud and Clear: Human-Verifiable Authentication Based on Audio

- Talking to Strangers の著者: Dirk Balfanz, D. K. Smetters, Paul Stewart, H. Chi Wong
- 発表: Network and Distributed System Security Symposium（NDSS 2002）, 2002年
- 確認先: https://www.ndss-symposium.org/ndss2002/talking-strangers-authentication-ad-hoc-wireless-networks/ （学会の予稿集ページで題名・著者・会議名・年を確認した）
- Loud and Clear の著者: Michael T. Goodrich, Michael Sirivianos, John Solis, Gene Tsudik, Ersin Uzun
- 発表: 26th IEEE International Conference on Distributed Computing Systems（ICDCS 2006）, 2006年
- 確認先: https://doi.org/10.1109/icdcs.2006.52 （Crossrefの書誌記録で題名・著者・会議名・年を確認した）

Talking to Strangersは、赤外線や音のように届く範囲が物理的に限られたチャネルを「場所限定チャネル」と呼び、そこには秘匿性は無いが、誰と話しているかを人間が目と耳で確認できるという真正性がある、という枠組みを提示した。Loud and Clearは、この考え方を音に特化させ、公開鍵の指紋を英語の文や旋律に変換して読み上げ、人間が二つの機器から同じものが聞こえることを確認する方式を作った。どちらも、音を秘密の通り道ではなく人間が監査できる公開の通り道として位置づけている。関連する理論的背景として、Vaudenayの短い認証済み文字列に基づく安全通信の枠組み（CRYPTO 2005, https://doi.org/10.1007/11535218_19 ）がある。

CipherFluteとの関係を述べる。CipherFluteが音に対して求めているものは、この系譜が音に求めてきたもの、すなわち「秘匿ではない何か」と同じ方向にある。ただしCipherFluteが求めるのは真正性でもなく、単に読み取りの正確さである。この差は、CipherFluteの脅威モデルの説明において、既存の枠組みのどれとも一致しない位置を占めることを示す材料になる。

脅威の度合いは中である。理由は、音響チャネルの性質を論じる際の古典であり、これを引かずに「音は公開チャネルである」と書くと、既存の議論の蓄積を知らないと見なされるおそれがあるからである。

### 11. RhythmLink: securely pairing I/O-constrained devices by tapping

- 著者: Felix Xiaozhu Lin, Daniel Ashbrook, Sean White
- 発表: Proceedings of the 24th Annual ACM Symposium on User Interface Software and Technology（UIST 2011）, pp. 263-272, 2011年
- 確認先: https://doi.org/10.1145/2047196.2047231 （Crossrefの書誌記録で題名・著者・会議名・ページ・年を確認した）

画面もボタンも乏しい機器同士を、利用者が同じリズムで叩くことによって安全に対応づける方式である。叩打の時系列を両方の機器が観測し、それが一致することを対応づけの根拠にする。人間の身体動作が生む共通の時間パターンを、秘密の共有と機器選択の両方に使っている。

CipherFluteとの関係を述べる。リズムという音楽的な語彙を機器の対応づけに使う点で、TapSongsやBeat-PINと同じ系列に属する。CipherFluteとの違いは、やはり時間軸か周波数軸かという符号の軸の違いと、秘密が人間の動作に由来するか物体の寸法に由来するかという違いである。

脅威の度合いは中である。理由は、UISTという同種の会場に「音楽的な構造で鍵を作る」という系譜が複数あることを示す文献であり、まとめて引用しておくと差分の説明が明快になるからである。

### 12. 携帯電話の着信メロディによる認証システムに関する検討

- 著者: 太田正哉, 山下勝己
- 発表: 電子情報通信学会技術研究報告, 第103巻 第376号, pp. 19-22, 2003年
- 確認先: https://cir.nii.ac.jp/crid/1520853833500569088 （CiNii Researchの書誌記録で題名・著者・誌名・巻号・ページ・年を確認した）

携帯電話の着信メロディ、すなわち電話機が鳴らす旋律を認証に使う仕組みを検討した日本語の技術報告である。旋律を認証の要素として扱う日本語の文献としては早い時期のものであり、音を鍵にするという発想が日本でも2003年の時点で検討されていたことを示す。

CipherFluteとの関係を述べる。旋律を認証の要素にするという着想の先行例であるが、音の生成は電子機器が行っており、旋律は電話機の識別に使われている。CipherFluteのように受動的な物体が音高で秘密を保持するものではない。

脅威の度合いは中である。理由は、日本語圏の関連研究として、投稿先がWISSであることを考えると触れておくのが穏当だからである。内容の新規性を脅かすものではない。

## 背景として押さえるべき文献

以下はいずれも一次的な書誌記録で実在を確認した。CipherFluteの背景として引用する程度でよいものである。

### 音を鍵とする認証と機器ペアリングの周辺

- Dominik Schürmann, Stephan Sigg, "Secure Communication Based on Ambient Audio", IEEE Transactions on Mobile Computing, 第12巻 第2号, pp. 358-370, 2013年。 https://doi.org/10.1109/tmc.2011.271 。周囲の音から同じ場所にいる機器同士が共通の鍵を導出する方式である。音を共有秘密の源とする立場であり、CipherFluteの立場と対照的である。
- Rajalakshmi Nandakumar, Krishna Kant Chintalapudi, Venkat Padmanabhan, Ramarathnam Venkatesan, "Dhwani: secure peer-to-peer acoustic NFC", ACM SIGCOMM 2013, pp. 63-74。 https://doi.org/10.1145/2486001.2486037 。音を使った近距離通信を、既存の携帯電話のスピーカーとマイクロホンだけで実現し、意図的な雑音の重畳によって盗聴を防ぐ方式である。
- Tzipora Halevi, Di Ma, Nitesh Saxena, Tuo Xiang, "Secure Proximity Detection for NFC Devices Based on Ambient Sensor Data", ESORICS 2012, Lecture Notes in Computer Science, pp. 379-396。 https://doi.org/10.1007/978-3-642-33167-1_22 。周囲の音を含む環境センサの情報で近接を確かめ、中継攻撃を防ぐ方式である。
- Hien Thi Thu Truong, Xiang Gao, Babins Shrestha, Nitesh Saxena, N. Asokan, Petteri Nurmi, "Comparing and fusing different sensor modalities for relay attack resistance in Zero-Interaction Authentication", PerCom 2014, pp. 163-171。 https://doi.org/10.1109/PerCom.2014.6813957 。周囲の音を含む複数のセンサ情報を組み合わせて中継攻撃への耐性を比較した研究である。
- Babins Shrestha, Nitesh Saxena, Hien Thi Thu Truong, N. Asokan, "Sensor-Based Proximity Detection in the Face of Active Adversaries", IEEE Transactions on Mobile Computing, 第18巻 第2号, pp. 444-457, 2019年。 https://doi.org/10.1109/TMC.2018.2839604 。能動的な攻撃者を想定したときに、音を含むセンサによる近接判定がどこまで持ちこたえるかを論じている。
- Prakash Shrestha, Nitesh Saxena, "Listening Watch: Wearable Two-Factor Authentication using Speech Signals Resilient to Near-Far Attacks", WiSec 2018, pp. 99-110。 https://doi.org/10.1145/3212480.3212501 。腕時計型端末と、ブラウザが能動的に鳴らす音声を使って、Sound-Proofの弱点を補う方式である。
- Jun Han, Albert Jin Chung, Manal Kumar Sinha, Madhumitha Harishankar, Shijia Pan, Hae Young Noh, Pei Zhang, Patrick Tague, "Do You Feel What I Hear? Enabling Autonomous IoT Device Pairing Using Different Sensor Types", IEEE Symposium on Security and Privacy 2018, pp. 836-852。 https://doi.org/10.1109/sp.2018.00041 。異なる種類のセンサが同じ物理事象を観測することを対応づけの根拠にする方式である。
- Xiaoyan Zhu, Suiyu Yu, Qingqi Pei, "QuickAuth: Two-Factor Quick Authentication Based on Ambient Sound", IEEE GLOBECOM 2016, pp. 1-6。 https://doi.org/10.1109/glocom.2016.7842192 。環境音による二要素認証の別実装である。
- S. Abhishek Anand, Nitesh Saxena, "Vibreaker: Securing Vibrational Pairing with Deliberate Acoustic Noise", WiSec 2016, pp. 103-108。 https://doi.org/10.1145/2939918.2939934 。意図的に雑音を出すことで音響盗聴を防ぐという、対策側の設計である。
- S. Abhishek Anand, Nitesh Saxena, "Coresident evil: noisy vibrational pairing in the face of co-located acoustic eavesdropping", WiSec 2017, pp. 173-183。 https://doi.org/10.1145/3098243.3098256 。同じ場所にいる攻撃者に対して、その雑音対策がどこまで有効かを検証している。
- Tzipora Halevi, Nitesh Saxena, "Acoustic Eavesdropping Attacks on Constrained Wireless Device Pairing", IEEE Transactions on Information Forensics and Security, 第8巻 第3号, pp. 563-577, 2013年。 https://doi.org/10.1109/tifs.2013.2247758 。CCS 2010の結果を発展させた雑誌版である。
- Serge Vaudenay, "Secure Communications over Insecure Channels Based on Short Authenticated Strings", CRYPTO 2005, Lecture Notes in Computer Science, pp. 309-326。 https://doi.org/10.1007/11535218_19 。公開だが改変されない短い文字列という抽象化を与えた理論的基礎である。
- Ravikanth Pappu, Ben Recht, Jason Taylor, Neil Gershenfeld, "Physical One-Way Functions", Science, 第297巻, pp. 2026-2030, 2002年。 https://doi.org/10.1126/science.1074376 。物理的複製困難関数の原典である。CipherFluteが複製困難性をあえて主張しないことの対比として引ける。

### 音を出す身体と生体的な要素

- Jagmohan Chauhan, Yining Hu, Suranga Seneviratne, Archan Misra, Aruna Seneviratne, Youngki Lee, "BreathPrint: Breathing Acoustics-based User Authentication", MobiSys 2017, pp. 278-291。 https://doi.org/10.1145/3081333.3081355 。息を吹く音を生体的な特徴として認証に使う研究である。CipherFluteが「誰が吹いても同じ音が出る」ことを利点にしているのと正反対の設計である。
- M. L. Shuwandy, B. B. Zaidan, A. A. Zaidan, "Novel authentication of blowing voiceless password for android smartphones using a microphone sensor", Multimedia Tools and Applications, pp. 44207-44243, 2022年。 https://doi.org/10.1007/s11042-022-13264-6 。携帯電話のマイクロホンに息を吹きかけるパターンを合言葉にする方式である。同誌に訂正記事（ https://doi.org/10.1007/s11042-022-13386-x ）が出ている点に注意が要る。
- Tomi Kinnunen, Md Sahidullah, Héctor Delgado, Massimiliano Todisco, Nicholas Evans, Junichi Yamagishi, Kong Aik Lee, "The ASVspoof 2017 Challenge: Assessing the Limits of Replay Spoofing Attack Detection", Interspeech 2017, pp. 2-6。 https://doi.org/10.21437/interspeech.2017-1111 。話者照合における録音再生攻撃の検出を競う共通課題である。音を秘密として使う方式がリプレイに悩まされることを端的に示す。

### 音響サイドチャネル攻撃

- Dmitri Asonov, Rakesh Agrawal, "Keyboard acoustic emanations", IEEE Symposium on Security and Privacy 2004, pp. 3-11。 https://doi.org/10.1109/secpri.2004.1301311
- Li Zhuang, Feng Zhou, J. D. Tygar, "Keyboard acoustic emanations revisited", CCS 2005, pp. 373-382。 https://doi.org/10.1145/1102120.1102169 。雑誌版はACM Transactions on Information and System Security, 2009年, https://doi.org/10.1145/1609956.1609959 である。
- Yigael Berger, Avishai Wool, Arie Yeredor, "Dictionary attacks using keyboard acoustic emanations", CCS 2006, pp. 245-254。 https://doi.org/10.1145/1180405.1180436
- Tong Zhu, Qiang Ma, Shanfeng Zhang, Yunhao Liu, "Context-free Attacks Using Keyboard Acoustic Emanations", CCS 2014, pp. 453-464。 https://doi.org/10.1145/2660267.2660296
- Michael Backes, Markus Dürmuth, Sebastian Gerling, Manfred Pinkal, Caroline Sporleder, "Acoustic Side-Channel Attacks on Printers", USENIX Security Symposium 2010, pp. 307-322。 DBLPの書誌記録で確認した（ https://dblp.org/search/publ/api?q=Backes+printers+acoustic ）。
- Daniel Genkin, Adi Shamir, Eran Tromer, "RSA Key Extraction via Low-Bandwidth Acoustic Cryptanalysis", CRYPTO 2014, Lecture Notes in Computer Science, pp. 444-461。 https://doi.org/10.1007/978-3-662-44371-2_25 。計算機が発する高周波の音から秘密鍵を抽出した研究である。
- Alberto Compagno, Mauro Conti, Daniele Lain, Gene Tsudik, "Don't Skype & Type! Acoustic Eavesdropping in Voice-Over-IP", AsiaCCS 2017, pp. 703-715。 https://doi.org/10.1145/3052973.3053005 。雑誌版はACM Transactions on Privacy and Security, 2019年, https://doi.org/10.1145/3365366 である。
- Joshua Harrison, Ehsan Toreini, Maryam Mehrnezhad, "A Practical Deep Learning-Based Acoustic Side Channel Attack on Keyboards", IEEE European Symposium on Security and Privacy Workshops 2023, pp. 270-280。 https://doi.org/10.1109/eurospw59978.2023.00034
- Daniel Arp, Erwin Quiring, Christian Wressnegger, Konrad Rieck, "Privacy Threats through Ultrasonic Side Channels on Mobile Devices", IEEE European Symposium on Security and Privacy 2017, pp. 35-47。 https://doi.org/10.1109/eurosp.2017.33 。人間に聞こえない音を機器の対応づけに使う商用技術の危険性を示した研究である。
- Benjamin Quattrone, Youakim Badr, "A Survey on Acoustic Side-Channel Attacks: An Artificial Intelligence Perspective", Journal of Cybersecurity and Privacy, 第6巻 第1号, 論文番号6, 2025年。 https://doi.org/10.3390/jcp6010006 。音響サイドチャネル攻撃の全体像を一件で引くための総説である。
- Sujit Rokka Chhetri, Arquimedes Canedo, Mohammad Abdullah Al Faruque, "Confidentiality Breach Through Acoustic Side-Channel in Cyber-Physical Additive Manufacturing Systems", ACM Transactions on Cyber-Physical Systems, 2017年。 https://doi.org/10.1145/3078622
- Seyed Ali Ghazi Asgar, Narasimha Reddy, "QuietPrint: Protecting 3D Printers Against Acoustic Side-Channel Attacks", ACM Cyber-Physical System Security Workshop 2026, pp. 25-34。 https://doi.org/10.1145/3775042.3807880 。3Dプリンタの音響漏洩に対する対策側の研究である。
- Christos Madamopoulos, Nektarios Georgios Tsoutsos, "3D printer audio and vibration side channel dataset", Data in Brief, 2024年, 論文番号111002。 https://doi.org/10.1016/j.dib.2024.111002
- Sina Faezi ほか, "Acoustic Side Channel Attack Against DNA Synthesis Machines: Poster Abstract", ICCPS 2020, pp. 186-187。 https://doi.org/10.1109/iccps48487.2020.00026

### 音楽を鍵とする認証の日本語文献および周辺

- 古賀千裕, 佐藤敬, 「混合された環境音の聞き取りに基づく認証方式」, コンピュータセキュリティシンポジウム2017論文集。 https://cir.nii.ac.jp/crid/1050292572146803072 。複数の環境音を混ぜて聞かせ、その聞き分けを認証に使う方式である。
- 堀孝浩, 喜多義弘, 豊田健太郎, 朴美娘, 岡崎直宣, 「「テンポ感」を特徴量としたリズム認証の認証精度に関する考察」, コンピュータセキュリティシンポジウム2015論文集, pp. 779-786。 https://cir.nii.ac.jp/crid/1050855522069274880
- 野口敦弘, 納富一宏, 斎藤恵一, 「自己組織化マップを用いたタッチスクリーンによるリズム認証手法」, バイオメディカル・ファジィ・システム学会誌, 第15巻 第1号, pp. 31-39, 2013年。 https://cir.nii.ac.jp/crid/1390282679457668096
- 大内結雲, 野崎真之介, 佐々木葵, 奥村紗名, 吉平瑞穂, 芹澤歩弥, 大木哲史, 西垣正勝, 「スマートフォンのタップ音からの入力内容推測可能性に関する研究」, 電子情報通信学会論文誌A, 第J105-A巻 第12号, pp. 156-167, 2022年。 https://cir.nii.ac.jp/crid/1390857158422008704 。日本語圏における音響サイドチャネルの研究である。
- Marcia Gibson, Marc Conrad, Carsten Maple, Karen Renaud, "Accessible and secure? Design constraints on image and sound based passwords", 2010 International Conference on Information Society, pp. 423-428。 https://doi.org/10.1109/i-society16502.2010.6018741
- Marcia Gibson, Karen Renaud, Marc Conrad, Carsten Maple, "Play That Funky Password! Recent Advances in Authentication with Music", Handbook of Research on Emerging Developments in Data Privacy, pp. 101-132, 2015年。 https://doi.org/10.4018/978-1-4666-7381-6.ch006 。音楽による認証の総説であり、この切り口を一件でまとめて引くのに適している。
- Marcia Gibson, Karen Renaud, Marc Conrad, Carsten Maple, "Music is the Key: Using our Enduring Memory for Songs to Help Users Log On", Strategic and Practical Approaches for Information Security Governance, pp. 137-157, 2012年。 https://doi.org/10.4018/978-1-4666-0197-0.ch008 。同内容がIT Policy and Ethics（2013年, https://doi.org/10.4018/978-1-4666-2919-6.ch046 ）にも収録されている。

## 未検証のまま残ったもの

- 「Listening to disorder: acoustic physical unclonable functions for audio-enabled secure authentication」, Yu Wang, Ying-Hao Fu, Zi-Ting Wang, Xin-Yu Cheng, Tao Wang, Yanqing Lu。Crossrefの書誌記録の上で、2026年のResearch Square掲載の投稿前原稿（ https://doi.org/10.21203/rs.3.rs-9353152/v1 ）として存在することまでは確認した。査読を経た論文ではなく、本文の内容は確認できていない。題名から判断すると、物体の音響応答を物理的複製困難関数として認証に使う研究であり、もし内容が想像どおりであれば「物体が出す音で認証する」という点でCipherFluteに近い位置に来る。ただし複製困難性を主張する方向であるため、複製容易性を前提とするCipherFluteとは目的が逆になる可能性が高い。本文を入手して確認する必要がある。
- 近距離の可聴域外の音を第二要素に使う商用技術として、2014年にGoogleが買収したSlickLoginという事例が知られているが、学術的な一次資料を確認できなかったため、実在と技術内容の両方を未確認のまま残す。
- 電話網の単一周波数信号方式、いわゆる2600ヘルツの笛による不正接続（ブルーボックス）は、「物体が出す音が網の制御鍵として働いた」歴史的事例として本研究の枠組みにきわめてよく合う。しかし今回、電話網の信号方式を記述した一次資料（ベル研究所の技術誌など）にあたることができなかったため、未検証とする。CipherFluteの導入で歴史的な例として触れるなら、一次資料の確認が必要である。
- 「Musical password based biometric authentication」（2016 International Conference on Computing, Communication and Automation, https://doi.org/10.1109/ccaa.2016.7813865 ）と「User Authentication using Musical Password」（International Journal of Computer Applications, 2012年, https://doi.org/10.5120/9573-4048 ）と「Graphical Password based Authentication System with Sound Sequence」（International Journal of Computer Applications, 2016年, https://doi.org/10.5120/ijca2016909072 ）は、書誌情報の上では実在を確認した。ただし本文を読んでいないため、内容と質の評価はできていない。査読の質が高くない媒体であるため、引用するかどうかは慎重に判断すべきである。

## この切り口で見つからなかったこと

以下は、探したうえで見つからなかったことである。CipherFluteの新規性の主張の根拠になるので、丁寧に書いておく。

第一に、電源も電子部品も持たない受動的な物体が、それ自身の共鳴周波数の列として暗号鍵や復元用情報を保持し、それを吹くことで読み出すという方式は見つからなかった。音を鍵にする研究はすべて、音の発生源が人間（歌う、叩く、吹く、話す）か、電源を持つ機器（スピーカー、プリンタ、計算機）のいずれかであった。物体そのものが音高の符号として鍵素材を持ち、吹く人が誰であっても同じ符号が出るという形は、CrossrefとDBLPとCiNiiのいずれの検索でも該当が出なかった。

第二に、音響チャネルに秘匿性をまったく期待しないと明示的に宣言したうえで、安全性の責任をすべて秘密分散に移すという設計は見つからなかった。もっとも近いのはAcoustic Integrity Codes（WiSec 2020）だが、これは音響チャネルに完全性を期待する設計であり、秘密分散とは組み合わせていない。HaleviとSaxenaのCCS 2010は音響チャネルの秘匿性が成り立たないことを示したが、それを前提とした肯定的な設計は与えていない。

第三に、音高を離散的なスロットに量子化し、既知の音高を持つ基準音を混ぜて全体のずれを打ち消し、そのうえで誤り訂正符号と隣接同一値の禁止を課す、という符号設計を認証や鍵運搬に適用した研究は見つからなかった。この組み合わせは通信工学では標準的だが、認証の文脈で音に適用した例は見当たらない。

第四に、口笛や笛といった気鳴楽器を認証や鍵の運搬に使った研究は、日本語文献では皆無であった。CiNii Researchで「口笛 認証」「笛 認証 鍵」「音響 トークン 認証 音波」のいずれで検索しても、論文・書籍・博士論文・研究データのすべてで結果が零件であった。

第五に、旋律や音を暗証番号の代わりに使う研究のうち、覚えやすさと安全性の兼ね合いを大規模に測ったものは、Gibsonらの一連の仕事以外にはほとんど見当たらなかった。音を鍵にする認証は、この十数年で「人間の記憶に預ける」方向から「機器が観測する環境音に預ける」方向へ移っており、記憶容易性の研究としては細い流れのまま止まっている。CipherFluteが「人間の記憶をまったく使わない」立場を取ることは、この流れの外側に位置する。

第六に、3Dプリンタの音響サイドチャネルに関する研究群は、いずれも「造形物の形状という知的財産を守る」ことを目的としており、「造形物の形状が暗号鍵そのものである」場合を扱ったものは見つからなかった。CipherFluteはこの場合に該当するため、既存の攻撃研究の帰結を新しい文脈に持ち込む立場になる。

## 調べ残した穴

- 音声そのものを合言葉にする話者照合の研究は、量が膨大であるため、ASVspoof 2017の共通課題論文一件を代表として押さえるにとどめた。話者照合における「秘匿できない生体情報をどう鍵として扱うか」という議論には、CipherFluteの立場と響き合う蓄積がある可能性が高く、追い切れていない。
- SOUPSの予稿集を年ごとに直接あたることができなかった。SOUPSは2015年から2018年まではUSENIXが、2019年以降はACMが刊行しており、刊行元をまたぐため一括の検索がしにくい。音を使う認証の使い勝手を測った研究がSOUPSにある可能性は残る。
- WISSとインタラクションの各年のプログラムページを直接あたることができなかった。日本語圏のヒューマンコンピュータインタラクション分野に、音を鍵にする発表がある可能性は残る。CiNiiはこの二つの会議を十分に索引していないため、会議のウェブサイトを年ごとに開いて確認する作業が要る。
- 音響サイドチャネルに対する「規格上の対策」については、TEMPEST関連の規格や暗号モジュールの物理セキュリティ要件（ISO/IEC 19790やFIPS 140-3）が音響漏洩をどこまで扱っているかを確認できなかった。触れるのであれば規格本文を確認する必要がある。
- 有力文献の被引用一覧をたどる芋づる式の探索が、Semantic ScholarとOpenAlexの両方が要求回数の制限で応答しなかったため、ほとんどできなかった。特にMusipassとSound-Proofの被引用一覧は、この切り口の網羅性を上げるうえで見ておく価値が高い。
- 特許文献をまったく見ていない。音を鍵にする認証は商用化の動機が強い領域であり、論文になっていない実装が特許として存在する可能性が高い。
