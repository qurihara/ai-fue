# 音を鍵とする認証の研究

この文書は、CipherFluteの位置づけを定めるための先行研究調査のうち、「音そのものを認証の要素として使う研究」という切り口を担当した結果である。

書誌情報の確認方法について最初に断っておく。今回の作業環境ではWeb検索の回数上限に達していたため、検索エンジンによる探索は使えなかった。そのかわりに、DOI登録機関であるCrossrefの書誌API（https://api.crossref.org/）、計算機科学の書誌データベースであるDBLP（https://dblp.org/）、日本語文献についてはCiNii Research（https://cir.nii.ac.jp/）、および学会自身の予稿集ページに直接あたって、著者・題名・会議名または雑誌名・巻号ページ・年を一件ずつ照合した。したがって以下に挙げる文献は、いずれも一次的な書誌記録の上で実在を確認したものである。確認できなかったものは末尾の「未検証のまま残ったもの」にまとめた。

この文書は2026年7月30日に、別の担当者が独立に検証を行っている。書誌情報はすべて実在が裏付けられたが、内容の記述には誤りが18件あり、その場で訂正した。訂正の跡は本文中に「2026年7月30日の検証で」という書き出しで残してあり、全体の集計と経緯は末尾の「検証の記録」に書いた。原稿を読むときは、この訂正の跡もあわせて読んでほしい。

## この切り口の要約

音を認証に使う研究は、大きく四つの流れに分かれることが分かった。第一に、旋律やリズムを人間の記憶の助けとして合言葉に使う流れがある。GibsonらのMusipass（NSPW 2009）を中心とする一連の仕事と、WobbrockのTapSongs（UIST 2009）やBeat-PIN（AsiaCCS 2018）のリズム認証がここに属する。第二に、周囲の環境音の一致を近接の証明に使う二要素認証の流れがあり、Sound-Proof（USENIX Security 2015）が代表である。第三に、音響チャネルを機器同士の鍵交換の補助路として使う機器ペアリングの流れがあり、Loud and Clear（ICDCS 2006）、HAPADEP（ISC 2008）、Acoustic Integrity Codes（WiSec 2020）が並ぶ。第四に、打鍵音やプリンタの動作音から秘密を推定する音響サイドチャネル攻撃の流れがある。

この四つの流れを通して見たとき、CipherFluteが取る「音の層に暗号学的な秘匿の力はまったく無いと最初から宣言する」という立場は、既存研究のなかでは珍しい。既存の音響認証は、音が盗聴されうるという事実を弱点として扱い、環境音の共有秘密性に頼るか、時間的な鮮度で盗聴を無効化するかの、どちらかで守ろうとしてきた。HaleviとSaxenaがCCS 2010で音響チャネルの秘匿性は仮定できないと実験的に示し、Acoustic Integrity Codesが音響チャネルを完全性専用の公開路として設計し直した系譜だけが、CipherFluteと同じ方向を向いている。ただしこれらはいずれも電源を持つ機器同士の通信の話であり、電源を持たない受動的な物体が音高の符号として鍵素材そのものを保持するという形は、今回調べた範囲では見つからなかった。したがってCipherFluteの新規性は、この切り口からは崩れない。一方で、3Dプリンタの動作音から造形物の形状が復元できるという一連の研究があるため、秘密を刻んだ笛を印刷している最中に音響サイドチャネルで秘密が漏れるという指摘は、脅威モデルの節に書き足しておかないと査読で突かれる。2026年7月30日の検証でこの懸念はさらに具体的になった。この系譜には実測データの公開まで含まれており、しかも公開されているデータセットの測定機種のひとつが Bambu Lab A1 mini である。CipherFluteの笛を実際に刷っている機種そのものであるから、査読者は追加の実験をせずにこの指摘を書ける状態にある。

## 必ず引用して差分を述べるべき文献（脅威の度合いはいずれも中である）

この節の見出しは当初「新規性への脅威が大きい文献」であったが、収録した十二件はすべて脅威の度合いが中と判定されており、見出しが内容を過大に表していた。そのため2026年7月30日の検証で、内容に合う見出しに改めた。脅威の度合いが高と判定される文献は、この切り口では一件も見つかっていない。

### 1. Musipass: authenticating me softly with "my" song

- 著者: Marcia Gibson, Karen Renaud, Marc Conrad, Carsten Maple
- 発表: Proceedings of the 2009 Workshop on New Security Paradigms（NSPW 2009）, pp. 85-100, 2009年
- 確認先: https://doi.org/10.1145/1719030.1719043 （Crossrefの書誌記録で題名・著者・会議名・ページ・年を確認した。副題を含む完全な題名も同じ記録で確認した）

利用者が自分で選んだ楽曲を認証の秘密として使う方式を提案した論文である。要旨が述べているのは、英数字のかわりに旋律で構成したパスワードを使ってみた経験の報告であり、その動機として、音楽は世界中に共通して存在し、人間は音楽に対して優れた記憶を持つという点が挙げられている。文字列のパスワードが覚えられないという問題に対して、音の記憶という別の認知資源を持ち込んだ点が主張の中心である。同じ著者らはこの後、画像や音を用いるパスワードにおいてアクセシビリティと安全性の目標が衝突する点の検討（i-Society 2010）と、音楽による認証の到達点をまとめた総説（Play That Funky Password!, 2015年）を書いており、この一群が「音を鍵とする認証」の直系の先行研究になっている。

なお、この項目には当初「ログイン時には複数の候補音から自分の曲を認識させるという再認方式を設計している」と書かれていたが、2026年7月30日の検証ではこの機構を原典で裏付けられなかった。ACM Digital Libraryは本文も要旨も機械的な取得を拒み、OpenAlexが保持する要旨には再認か再生かの区別が書かれておらず、University of Bedfordshireのリポジトリにあった全文（ハンドル10547/270603）は現在リンクが切れている。したがって再認方式であるという記述はいったん取り下げた。CipherFluteの論文で機構に踏み込んで対比するのであれば、全文を入手して確かめる必要がある。

CipherFluteとの関係を述べる。Musipassは秘密を人間の記憶のなかに置き、音はその記憶を呼び出す手がかりとして使う。CipherFluteは逆に、人間の記憶をまったく当てにせず、秘密を物体の管長として外部化し、音はその物体から符号を取り出すための搬送波として使う。したがって「音を鍵にする」という語彙は共有するが、秘密の置き場所が正反対である。

脅威の度合いは中である。理由は、査読者が「音を認証の鍵にすること自体は2009年に既にやられている」と指摘してくる筋がここにあるためで、引用したうえで、記憶に預けるのか物体に預けるのかという違いを明示的に書かないと新規性の説明が弱くなるからである。

### 2. TapSongs: tapping rhythm-based passwords on a single binary sensor

- 著者: Jacob O. Wobbrock
- 発表: Proceedings of the 22nd Annual ACM Symposium on User Interface Software and Technology（UIST 2009）, pp. 93-96, 2009年
- 確認先: https://doi.org/10.1145/1622176.1622194 （Crossrefの書誌記録で題名・著者・会議名・ページ・年を確認した）

利用者が知っている歌のリズムを、押しボタン一つの二値センサに叩き込むことで認証する方式である。入力できる情報は押した時刻の列だけであり、鍵の語彙は時間軸上のパターンとして定義される。歌という誰でも持っている記憶資源を、極端に貧しい入力装置の上に写し取った点が寄与である。認証の判定は、押し下げと押し上げの時刻の列を、利用者があらかじめ作った旋律の時間モデルと照合するかたちで行う。要旨によれば照合には絶対的な一致基準を用い、さらに成功したログインから学習して基準を更新する。当初この項目には「統計的な手法」と書かれていたが、原典の要旨が述べているのは絶対的な一致基準と学習であるため、2026年7月30日の検証で書き改めた。

実験の数値も原典の要旨で裏を取れた。被験者10名が12回の例示から自分の旋律モデルを作るのに2分未満しかかからず、その後のログインは83.2パーセント成功した。他人が実験者のログインを耳と目で盗み見た場合、なりすましの成功率は10.7パーセントにとどまり、目標の旋律を合成ピアノで聞かせた場合でも19.4パーセントであった。著者はこの結果を、人の叩き方には微妙だが安定した個人差があるためだと説明している。

CipherFluteとの関係を述べる。両者はどちらも「音楽的な構造を符号の語彙にする」という発想を共有する。ただしTapSongsが使うのは時間軸上のパターンであり、CipherFluteが使うのは周波数軸上の離散値である。CipherFluteの13スロットの半音刻みという設計は、時間ではなく音高を語彙にした点で区別できる。さらに重要な対比がある。TapSongsは人の叩き方の個人差そのものを安全性の土台にしており、旋律を知っただけの他人はなりすませないことを寄与として掲げている。CipherFluteはこれと正反対で、誰が吹いても同じ符号が出ることを要件にしており、個人差は打ち消すべき誤差として扱う。CipherFluteでは揺らぎの原因が気温と息の強さに限られるため、基準笛との比を測ることで打ち消せる。

脅威の度合いは中である。理由は、UISTという同種の会場で「音楽を鍵にする」という発想が既に示されているため、必ず引用して差分を述べる必要があるからである。ただし符号の軸が時間か周波数かという違いは明確なので、主要な主張が崩れることはない。

### 3. Beat-PIN: A User Authentication Mechanism for Wearable Devices Through Secret Beats

- 著者: Ben Hutchins, Anudeep Reddy, Wenqiang Jin, Michael Zhou, Ming Li, Lei Yang
- 発表: Proceedings of the 2018 on Asia Conference on Computer and Communications Security（AsiaCCS 2018）, pp. 101-115, 2018年
- 確認先: https://doi.org/10.1145/3196494.3196543 （Crossrefの書誌記録で題名・著者・会議名・ページ・年を確認した。なおCrossrefが記録する第四著者はMichael Zhouであり、Semantic Scholarは同じ人物をMi Zhouと記録している。出版者であるACMが登録した綴りに従ってMichael Zhouと書いた）

画面が小さく文字入力が難しいウェアラブル機器のために、暗証番号のかわりに秘密の拍のパターンを叩いて認証する方式である。触覚センサを備えた装着型機器の上で、利用者が機器を叩いたときの拍の集まりをパスワードとし、その拍の時刻の並びで表す。訓練の手間を小さくしたまま精度を上げるために独自の分類手法を提案しており、124名の被験者による評価で、訓練の見本を7個与えるだけで平均等誤り率7.2パーセントを達成し、ログインにかかる時間は1.7秒まで短くなったと報告している。TapSongsの発想を、装着型機器という現実の必要と、攻撃者を想定した安全性評価の枠組みへ持ち込んだ位置づけになる。

当初この項目には「鍵空間の大きさと、他人が肩越しに見て真似できるかという観察耐性の議論を含む」と書かれていた。2026年7月30日の検証では、鍵空間についての理論的な解析があること、すなわち拍による暗証番号の素の鍵空間が数字の暗証番号や従来のパスワードよりはるかに大きいと示していることは要旨で裏付けられた。しかし肩越しの覗き見に対する耐性の議論は要旨に見あたらなかったため、その部分は取り下げた。

CipherFluteとの関係を述べる。Beat-PINは、拍のパターンという音楽的な語彙を、暗証番号の代替として位置づけている。CipherFluteが音高を暗号資産の復元用情報の符号にするのと、目的が異なる。Beat-PINの秘密は人間が覚えて再現するものであり、CipherFluteの秘密は物体が保持して誰が吹いても同じ音が出るものである。CipherFluteは「誰が吹いても同じ」であることを利点として設計しているのに対し、Beat-PINは「本人しか再現できない」ことを安全性の根拠にしている点が対照的である。

脅威の度合いは中である。理由は、音楽的なパターンを鍵の語彙にするという発想が主要なセキュリティ会議で既に確立していることを示す文献であり、隣接研究として引用が必要だからである。

### 4. On pairing constrained wireless devices based on secrecy of auxiliary channels: the case of acoustic eavesdropping

- 著者: Tzipora Halevi, Nitesh Saxena
- 発表: Proceedings of the 17th ACM Conference on Computer and Communications Security（CCS 2010）, pp. 97-108, 2010年
- 確認先: https://doi.org/10.1145/1866307.1866319 （Crossrefの書誌記録で題名・著者・会議名・ページ・年を確認した）

入出力の乏しい機器同士を安全につなぐ手法のなかには、音や振動といった補助チャネルが秘密を運べると暗黙に仮定するものがある。この論文は、その仮定が成り立たないことを実験で示した。攻撃の的にしたのは、認証済みかつ秘密であることを仮定する補助チャネル（著者らの言う AS-OOB チャネル）に依拠した三つの既存方式である。すなわち、低い周波数の音響チャネルで体内植込み機器と外部の読み取り機を対応づける IMD Pairing、振動を自動で使って携帯電話と個人用のRFIDタグを対応づける PIN-Vibra、そして片方の機器の振動または点滅に合わせて人間がボタンを押す BEDA である。著者らはこれら三方式に伴って生じる音響的な放射を盗聴できることを実証し、当初想定されていたよりも安全性の水準が低いと結論した。ここで重要なのは、三方式のうち二つは音そのものではなく振動を使う方式であり、盗聴されたのはその振動が空気中に漏らす音であるという点である。著者らはこの結果を発展させ、IEEE Transactions on Information Forensics and Security誌の論文（2013年）としてまとめ直している。

当初この項目には「離れた場所に置いた盗聴用のマイクロホンで」と書かれていたが、盗聴に用いた距離を原典の要旨で裏付けられなかったため、2026年7月30日の検証で距離への言及を削った。

CipherFluteとの関係を述べる。CipherFluteは「音の層には暗号学的な秘匿の力はまったく無い」と宣言しているが、この宣言はこの論文が2010年に確立した知見と完全に一致する。つまりCipherFluteの脅威モデルの前半部分は、新しい洞察ではなく既知の結論の再確認である。逆に言えば、この論文を引くことでCipherFluteの立場に確かな根拠を与えられる。

脅威の度合いは中である。理由は、CipherFluteが脅威モデルの独自性として「音に秘匿を求めない」ことを掲げるなら、その論点は既に決着済みであると指摘されうるためで、引用したうえで、CipherFluteの寄与は秘匿の放棄そのものではなく、放棄したうえで秘密分散に全責任を移す設計にあると書き分ける必要があるからである。

### 5. Acoustic integrity codes: secure device pairing using short-range acoustic communication

- 著者: Florentin Putz, Flor Álvarez, Jiska Classen
- 発表: Proceedings of the 13th ACM Conference on Security and Privacy in Wireless and Mobile Networks（WiSec 2020）, pp. 31-41, 2020年
- 確認先: https://doi.org/10.1145/3395351.3399420 （Crossrefの書誌記録で題名・著者・会議名・ページ・年を確認した）

短距離の音響通信を使って機器を安全に対応づける方式を提案した論文である。設計の核心は、音響チャネルに秘匿性をいっさい期待せず、かわりに完全性だけを保証する符号を載せる点にある。攻撃者が音を聞くことは前提として許し、そのうえで攻撃者が符号を書き換えたり打ち消したりできないような符号化を与えることで、盗聴されても安全な鍵確立を実現している。要旨で裏を取れた具体策は次のとおりである。信号を打ち消す攻撃に対しては自己相関の低い信号を設計することで防ぎ、上から覆い被せる攻撃に対しては閾値を持つ三値の判定関数で検知する。評価では、信号対雑音比が14デシベルの条件で実効100ビット毎秒を出しながらビット誤り率を0.1パーセント未満に抑えた。実装はAndroid端末上の公開された概念実証であり、機種の異なる端末同士の対応づけを示している。既存の機器に共通の専用ハードウェアを要求せず、音響ハードウェアが広く備わっていることを利点として挙げている点も、この論文の動機として明記されている。

CipherFluteとの関係を述べる。「音は公開チャネルであって秘匿はしない」というCipherFluteの立場と、設計思想がもっとも近い先行研究である。ただし守ろうとしているものが違う。Acoustic Integrity Codesが守るのは通信の完全性であり、能動的な攻撃者が符号を改変できないことを目標にしている。CipherFluteが音の層に求めているのは完全性ですらなく、誤り訂正符号による読み取りの頑健性だけであり、安全性はすべて秘密分散に委ねている。したがって「音響チャネルに何を期待し何を期待しないか」という設計の分節において、両者は近い場所にありながら違う点に立っている。

脅威の度合いは中である。理由は、音響チャネルを公開路として扱う立場そのものは既に確立していることを示す文献であり、これを引かないと「音に秘匿を求めない」という宣言が唐突に見えるからである。

### 6. Sound-Proof: Usable Two-Factor Authentication Based on Ambient Sound

- 著者: Nikolaos Karapanos, Claudio Marforio, Claudio Soriente, Srdjan Capkun
- 発表: 24th USENIX Security Symposium（USENIX Security 2015）, pp. 483-498, 2015年
- 確認先: https://www.usenix.org/conference/usenixsecurity15/technical-sessions/presentation/karapanos （学会の予稿集ページに掲載されたBibTeX記録で題名・著者・会議名・ページ・年・国際標準図書番号を確認した。全文の書誌情報はhttps://www.usenix.org/system/files/conference/usenixsecurity15/sec15-paper-karapanos.pdf でも確認した）

パソコンと携帯電話が同じ場所にあることを、両者のマイクロホンが拾った周囲の音の一致によって確かめ、利用者に何も操作させずに二要素認証を成立させる方式である。利用者は携帯電話を取り出す必要すらなく、携帯電話がポケットや鞄の中にあっても、また屋内でも屋外でも働く。一致度の測り方は全文で確かめた。可聴域を3分の1オクターブの帯域に分けて帯域通過フィルタをかけ、帯域ごとに相互相関を取ってその平均を類似度とし、閾値を超え、かつ試料の平均パワーが別の閾値（実験では40デシベル）を超えたときに正当なログインと判定する。判定はサーバではなく携帯電話の側で行い、パソコンの録音は携帯電話の公開鍵で暗号化して渡すため、平文の音声はサーバに上がらない。

この方式の弱点については、当初「後に、共在する攻撃者や音を予測できる攻撃者に対して脆弱であることが示され」と書かれていた。2026年7月30日の検証で、この記述を二つに分けて正確にした。共在する攻撃者に弱いことは後から指摘されたのではなく、原論文自身が脅威モデルの節で対象外だと明記している。原論文は、利用者と同じ場所にいて認証情報も持っている標的型の攻撃を守る設計ではないと述べ、安全性より使いやすさと展開しやすさを優先した設計上の割り切りだと認めている。後から示されたのは、環境音を推測する受動的な遠隔攻撃者と、環境音を操作する能動的な遠隔攻撃者に対する脆弱性である。これを示し、あわせて設計をやり直したのが、Prakash Shrestha, Ahmed Tanvir Mahdad, Nitesh Saxena による Sound-based Two-factor Authentication: Vulnerabilities and Redesign（ACM Transactions on Privacy and Security誌, 第27巻 第1号, pp. 1-27, 2024年, https://doi.org/10.1145/3632175 ）であり、同じ著者らのListening Watch（WiSec 2018）を発展させたListening-Watchという方式を提案している。この方式は、受動的に環境音を聞くのではなく、ブラウザが乱数から短い符号を作って音声として鳴らし、腕時計側の録音にその符号が含まれることを音声認識で確かめることで鮮度を確保する設計に変えている。

CipherFluteとの関係を述べる。Sound-Proofは音を「共有された秘密に近いもの」として扱う。同じ場所にいる者だけが同じ音を聞ける、という前提に安全性を置いているため、盗聴とリプレイが本質的な脅威になる。CipherFluteは音の共有秘密性をいっさい前提にしないため、リプレイ攻撃も盗聴も脅威として定義されない。この対比は、CipherFluteの位置づけを説明する材料としてそのまま使える。

脅威の度合いは中である。理由は、音を認証要素として使う研究の代表例であり、CipherFluteが「音は公開チャネルである」と述べるとき、その主張が既存の音響認証のどこに位置するかを説明するために必ず引用が要るからである。

### 7. My Smartphone Knows What You Print: Exploring Smartphone-based Side-channel Attacks Against 3D Printers

- 著者: Chen Song, Feng Lin, Zhongjie Ba, Kui Ren, Chi Zhou, Wenyao Xu
- 発表: Proceedings of the 2016 ACM SIGSAC Conference on Computer and Communications Security（CCS 2016）, pp. 895-907, 2016年
- 確認先: https://doi.org/10.1145/2976749.2978300 （Crossrefの書誌記録で題名・著者・会議名・ページ・年を確認した）

3Dプリンタのそばに置いた携帯電話の内蔵センサだけで、印刷中の造形物の形状を復元できることを示した論文である。ここに当初「マイクロホンと加速度センサ」と書かれていたのは誤りであった。2026年7月30日の検証で原典の要旨に当たったところ、この攻撃が使うのは音響と磁気の二つのサイドチャネルであり、加速度センサではなく磁気センサ（磁力計）が使われている。しかも著者らは、磁気の情報で補強したモデルによってノズルの向きを伴う動作を正確に推定している。復元の対象は造形物の輪郭にとどまらず、造形物そのものとそれを作るG-codeまで再構成しており、平均傾向誤差は通常の設計で5.87パーセント、複雑な設計で9.67パーセントであったと報告している。研究の動機として掲げられているのは、知的財産としての設計情報の保護である。

同じ問題を扱った独立の研究として、Mohammad Abdullah Al Faruque, Sujit Rokka Chhetri, Arquimedes Canedo, Jiang Wan による Acoustic Side-Channel Attacks on Additive Manufacturing Systems（ICCPS 2016, pp. 1-10, https://doi.org/10.1109/iccps.2016.7479068 ）と、その拡張であるACM Transactions on Cyber-Physical Systems誌の論文（第2巻 第1号, pp. 1-25, 2017年, https://doi.org/10.1145/3078622 ）がある。対策側としては QuietPrint（第12回ACM Cyber-Physical System Security Workshop, pp. 25-34, 2026年, https://doi.org/10.1145/3775042.3807880 ）が提案されており、大型のスピーカーや雑音打ち消し装置といった追加のハードウェアを要さず、G-codeへの最小限の改変だけで造形物を守る点を利点として掲げている。

CipherFluteにとって見過ごせないのは、この系譜に実測データの公開まで含まれていることである。Christos Madamopoulos と Nektarios Georgios Tsoutsos が公開したデータセット（Data in Brief誌, 第57巻, 論文番号111002, 2024年, https://doi.org/10.1016/j.dib.2024.111002 ）は、熱溶解積層方式の3Dプリンタの音と振動を収めたものであり、その測定に使われた機種が Bambu Lab P1P と A1 mini である。A1 miniはCipherFluteの笛を実際に印刷している機種そのものであるから、「この機種の印刷音から形状が復元できるか」を問うための材料が、すでに誰でも入手できる形で公開されていることになる。脅威モデルの節でこの事実に触れないのは危うい。

CipherFluteとの関係を述べる。CipherFluteの秘密は管長という形状そのものであるから、形状が復元されれば秘密が復元される。この一連の研究は、印刷という製造工程の最中に、音だけで形状が漏れうることを示している。CipherFluteの脅威モデルは「形状を計測されれば無音で読める」ことを既に認めているが、その計測が完成後の物体に対してではなく、製造中に離れた場所から可能であるという点までは書かれていない。ここは加筆が必要である。

脅威の度合いは中である。理由は、CipherFluteの新規性そのものを崩す研究ではないが、脅威モデルの記述に明らかな穴を作る研究であり、引用したうえで「印刷環境も秘密の一部として扱う必要がある」と書かなければ、査読で弱点を突かれるからである。

### 8. Listen to Your Key: Towards Acoustics-based Physical Key Inference

- 著者: Soundarya Ramesh, Harini Ramprasad, Jun Han
- 発表: Proceedings of the 21st International Workshop on Mobile Computing Systems and Applications（HotMobile 2020）, pp. 3-8, 2020年
- 確認先: https://doi.org/10.1145/3376897.3377853 （Crossrefの書誌記録で題名・著者・会議名・ページ・年を確認し、Semantic Scholarが保持する要旨で内容とシステム名を確認した）

物理的な鍵を錠に差し込むときに出る、山と谷が錠のピンに当たる小さな音を録音し、そこから鍵の刻みの深さを推定する攻撃を示した論文である。システムの名前がSpiKeyであることは要旨で確認できた。要旨によれば、推定の手がかりは聞き取れるクリック音の時間差であり、そこから鍵の秘密にあたる刻みの深さを導く。鍵という物理的な秘密が、その物体を使うときに出る音によって漏れることを示した点が寄与である。

当初この項目には「合鍵を作る攻撃」と書かれていたが、2026年7月30日の検証で言い過ぎであると判断して書き改めた。原典が示しているのは実際の合鍵の製作ではなく、現実の録音に基づく模擬実験としての概念実証であり、成果は探索空間の削減である。もっとも頻度の高い場合について、33万本を超える候補の集まりから3本の候補まで絞り込めたと報告している。この違いは、CipherFluteが「形状を計測されれば読める」と認めるときの論の運び方に関わるので、正確に引くべきである。

CipherFluteとの関係を述べる。CipherFluteは「音を鳴らして秘密を読み出す」ことを正規の利用者の手続きとして設計しているが、この論文は「物理的な秘密が音で漏れる」ことを攻撃として示している。同じ物理現象を、一方は機能として、他方は脆弱性として扱っている点で、対比の材料としてきわめて有用である。CipherFluteが物理層に秘匿を求めないという立場を取ることの正しさを、外側から補強する文献でもある。

脅威の度合いは中である。理由は、物体が発する音がその物体の秘密を明かすという構図が既に確立していることを示すため、CipherFluteの脅威モデルの記述で必ず参照すべきだからである。ただし目的も対象も異なるので、新規性そのものは脅かさない。

### 9. HAPADEP: Human-Assisted Pure Audio Device Pairing

- 著者: Claudio Soriente, Gene Tsudik, Ersin Uzun
- 発表: Information Security Conference（ISC 2008）, Lecture Notes in Computer Science 第5222巻, pp. 385-400, 2008年
- 確認先: https://doi.org/10.1007/978-3-540-85886-7_27 （Crossrefの書誌記録で題名・著者・会議名・ページを確認し、出版者であるSpringerの当該章のページで要旨・叢書の巻番号・会議名・年を確認した）

無線の共通路をいっさい使わず、音だけで機器同士に鍵素材を渡し、人間の関与によってその真正性を担保する方式である。要旨で明確に裏を取れたのは次の点である。従来の対応づけ手法はいずれも、赤外線や802.11やBluetoothといった人間に知覚できないデジタルな共通媒体の上に、安全でない通信路が既に確立していることを前提にしていた。HAPADEPはその前提を外し、データと検証情報の両方を音響チャネルだけでやりとりする。音を、秘密の通り道ではなく、人間が監査できる公開の通り道として使っている点が特徴である。

当初この項目には「まず機器が鍵素材を音として送り、続いて短い確認用の旋律を鳴らして、人間が二つの機器から同じ旋律が聞こえることを確かめる」と書かれていた。二段階の構成そのものは要旨の「データと検証情報の両方を音響チャネルでやりとりする」という記述と整合するが、検証の段が旋律であること、および二つの機器が同じ旋律を鳴らして人間が聞き比べることは、要旨からは裏付けられなかった。全文はSpringerが購読者向けに限っており、International Association for Cryptologic Researchの電子公開資料（2007年093番）も機械的な取得を拒んだため確かめられなかった。したがって旋律という記述は取り下げ、確かめられた範囲に書き直した。

CipherFluteとの関係を述べる。音を鍵素材の搬送路として使い、しかもその音が公開であることを前提にする点で、CipherFluteと発想が近い。違いは、HAPADEPが電源を持つ機器の間の通信であり、鍵素材はその場で生成される一時的なものであるのに対し、CipherFluteでは物体そのものが恒久的に鍵素材を保持し、送信側に電源がまったく要らない点である。

脅威の度合いは中である。理由は、「音で鍵素材を運ぶ」という行為の先行例として、査読者が真っ先に思い浮かべる種類の研究であり、引用して差分を述べておく必要があるからである。

### 10. Talking to Strangers: Authentication in Ad-Hoc Wireless Networks / Loud and Clear: Human-Verifiable Authentication Based on Audio

- Talking to Strangers の著者: Dirk Balfanz, D. K. Smetters, Paul Stewart, H. Chi Wong
- 発表: Network and Distributed System Security Symposium（NDSS 2002）, 2002年
- 確認先: https://www.ndss-symposium.org/ndss2002/talking-strangers-authentication-ad-hoc-wireless-networks/ （学会の予稿集ページで題名・著者・会議名・年を確認した。ページは生きており、全文の電子ファイルも掲げられている）
- Loud and Clear の著者: Michael T. Goodrich, Michael Sirivianos, John Solis, Gene Tsudik, Ersin Uzun
- 発表: 26th IEEE International Conference on Distributed Computing Systems（ICDCS 2006）, 2006年（IEEEの版では論文番号が10であり、通しのページ番号は付されていない）
- 確認先: https://doi.org/10.1109/icdcs.2006.52 （Crossrefの書誌記録で題名・著者・会議名を確認し、OpenAlexが保持する要旨で内容と年を確認した）

Talking to Strangersは、赤外線や音のように届く範囲が物理的に限られたチャネルを「場所限定チャネル」と呼び、そこには秘匿性は無いが、誰と話しているかを人間が確認できるという真正性がある、という枠組みを提示した。ただし「場所限定チャネル」という用語そのものは、学会の予稿集ページに要旨が載っていないため確認できていない。この点は末尾の「未検証のまま残ったもの」にも記した。

Loud and Clearについては、当初「公開鍵の指紋を英語の文や旋律に変換して読み上げ、人間が二つの機器から同じものが聞こえることを確認する方式」と書かれていたが、2026年7月30日の検証で二か所を訂正した。第一に、要旨が述べる機構は、機器の公開鍵のハッシュから導いた、頑健に聞こえる英語らしい構文の文を音声合成の機構で読み上げるものであり、旋律への変換は要旨に現れない。第二に、確認の作法は「二つの機器から同じものが聞こえる」ことではない。片方の機器が読み上げるのと同時に、もう一方の機器が同じ情報を画面に表示し、人間はその二つを突き合わせる。したがって耳と目を組み合わせる方式であって、耳だけを二度使う方式ではない。どちらの論文も、音を秘密の通り道ではなく人間が監査できる公開の通り道として位置づけている点は変わらない。関連する理論的背景として、Vaudenayの短い認証済み文字列に基づく安全通信の枠組み（CRYPTO 2005, Lecture Notes in Computer Science, pp. 309-326, https://doi.org/10.1007/11535218_19 ）がある。

CipherFluteとの関係を述べる。CipherFluteが音に対して求めているものは、この系譜が音に求めてきたもの、すなわち「秘匿ではない何か」と同じ方向にある。ただしCipherFluteが求めるのは真正性でもなく、単に読み取りの正確さである。この差は、CipherFluteの脅威モデルの説明において、既存の枠組みのどれとも一致しない位置を占めることを示す材料になる。

脅威の度合いは中である。理由は、音響チャネルの性質を論じる際の古典であり、これを引かずに「音は公開チャネルである」と書くと、既存の議論の蓄積を知らないと見なされるおそれがあるからである。

### 11. RhythmLink: securely pairing I/O-constrained devices by tapping

- 著者: Felix Xiaozhu Lin, Daniel Ashbrook, Sean White
- 発表: Proceedings of the 24th Annual ACM Symposium on User Interface Software and Technology（UIST 2011）, pp. 263-272, 2011年
- 確認先: https://doi.org/10.1145/2047196.2047231 （Crossrefの書誌記録で題名・著者・会議名・ページ・年を確認した）

画面もボタンも乏しい機器同士を、利用者が知っているリズムをそれぞれの機器に叩き込むことによって安全に対応づける方式である。叩打の時系列を両方の機器が観測し、それが一致することを対応づけの根拠にする。要旨で裏を取れた技術的な核心は、不正確に入力された叩打の列同士を、その列の秘密を保ったまま比較できる算法である。また、対応づけの最中に母艦側の機器を操作する必要がなく、周辺機器の側には二値の入力しか求めないため、物理的な操作手段の乏しい小型機器に向くとされている。人間の身体動作が生む共通の時間パターンを、秘密の共有と機器選択の両方に使っている。

CipherFluteとの関係を述べる。リズムという音楽的な語彙を機器の対応づけに使う点で、TapSongsやBeat-PINと同じ系列に属する。CipherFluteとの違いは、やはり時間軸か周波数軸かという符号の軸の違いと、秘密が人間の動作に由来するか物体の寸法に由来するかという違いである。

脅威の度合いは中である。理由は、UISTという同種の会場に「音楽的な構造で鍵を作る」という系譜が複数あることを示す文献であり、まとめて引用しておくと差分の説明が明快になるからである。

### 12. 携帯電話の着信メロディによる認証システムに関する検討

- 著者: 太田正哉, 山下勝己
- 発表: 電子情報通信学会技術研究報告（信学技報）, 第103巻 第376号, pp. 19-22, 2003年10月22日
- 確認先: https://cir.nii.ac.jp/crid/1520853833500569088 （CiNii Researchの書誌記録で題名・著者名・誌名・巻号・ページ・発行日を確認した。国立国会図書館の書誌記録 http://id.ndl.go.jp/bib/6766908 にも同じ記述がある）

携帯電話の着信メロディ、すなわち電話機が鳴らす旋律を認証に使う仕組みを検討した日本語の技術報告である。旋律を認証の要素として扱う日本語の文献としては早い時期のものであり、音を鍵にするという発想が日本でも2003年の時点で検討されていたことを示す。

内容についての注意を書いておく。当初この項目には「音の生成は電子機器が行っており、旋律は電話機の識別に使われている」と書かれていたが、2026年7月30日の検証ではこれを裏付けられなかった。CiNii Researchおよび国立国会図書館の記録にはいずれも要旨が収められておらず、付与されている主題語が authentication system と mobile-phone と ringing Melody の三語だけである。信学技報の2003年の号は電子的に開かれていないため、本文にあたれなかった。したがって、旋律が何を識別するために使われているのか、認証されるのは電話機なのか利用者なのかは未確認である。この点は末尾の「未検証のまま残ったもの」にも記した。CipherFluteの論文で日本語圏の先行例として引くのであれば、電子情報通信学会の会員向け電子図書館などで本文を確かめる必要がある。

CipherFluteとの関係を述べる。旋律を認証の要素にするという着想の先行例であることは題名から言える。ただし音の生成は電源を持つ電話機が行っているのであって、CipherFluteのように電源を持たない受動的な物体が音高で秘密を保持するものではない。

脅威の度合いは中である。理由は、日本語圏の関連研究として、投稿先がWISSであることを考えると触れておくのが穏当だからである。内容の新規性を脅かすものではない。

## 背景として押さえるべき文献

以下はいずれも一次的な書誌記録で実在を確認した。CipherFluteの背景として引用する程度でよいものである。

### 音を鍵とする認証と機器ペアリングの周辺

- Dominik Schürmann, Stephan Sigg, "Secure Communication Based on Ambient Audio", IEEE Transactions on Mobile Computing, 第12巻 第2号, pp. 358-370, 2013年。 https://doi.org/10.1109/tmc.2011.271 。周囲の音から同じ場所にいる機器同士が共通の鍵を導出する方式である。音を共有秘密の源とする立場であり、CipherFluteの立場と対照的である。
- Rajalakshmi Nandakumar, Krishna Kant Chintalapudi, Venkat Padmanabhan, Ramarathnam Venkatesan, "Dhwani: secure peer-to-peer acoustic NFC", ACM SIGCOMM 2013, pp. 63-74。 https://doi.org/10.1145/2486001.2486037 。音を使った近距離通信を、既存の携帯電話のスピーカーとマイクロホンだけで実現する方式である。盗聴への対策はJamSecureと名づけられた仕組みで、受信側が自ら雑音を出しつつその自己干渉を除去することで、情報理論的に安全な通信路を作る。速度は2.4キロビット毎秒までであり、当時の近距離通信の用途には足りると述べている。
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
- Ravikanth Pappu, Ben Recht, Jason Taylor, Neil Gershenfeld, "Physical One-Way Functions", Science, 第297巻 第5589号, pp. 2026-2030, 2002年。 https://doi.org/10.1126/science.1074376 。物理的複製困難関数の原典である。CipherFluteが複製困難性をあえて主張しないことの対比として引ける。
- Yu Wang, Ying-Hao Fu, Zi-Ting Wang, Xin-Yu Cheng, Tao Wang, Yanqing Lu, "Listening to disorder: acoustic physical unclonable functions for audio-enabled secure authentication", Research Square掲載の投稿前原稿, 2026年5月14日。 https://doi.org/10.21203/rs.3.rs-9353152/v1 。当初は末尾の「未検証のまま残ったもの」に置かれていたが、2026年7月30日の検証でCrossrefが保持する要旨の全文を取得できたため、内容の評価がついたものとしてこの節へ移した。内容は材料科学の研究である。二酸化クロムの微粒子をシルクフィブロインの母材に埋め込んだ複合磁性媒体を作り、そこに音を予測不能な励起として与えると、微視的な磁区の無秩序と音響のゆらぎが相互作用して、本質的に複製も再現もできない応答が生じる。これを音響の物理的複製困難関数と呼び、偽造防止と情報保護の技術として位置づけている。機械学習による攻撃への耐性と再構成可能性を主張し、周波数領域の符号化による多重の偽造防止や、音響と光学を組み合わせた複合ラベルも示している。脅威の度合いは低である。理由は、題名だけを見ると「物体が出す音で認証する」という点でCipherFluteに近く見えるが、実際には目的が正反対だからである。この研究は複製できないことを価値としており、秘密は物体の無秩序に宿ってあらかじめ選べない。CipherFluteは選んだ秘密を管長として意図的に書き込み、複製が容易であることを最初から認めて、秘匿の責任を秘密分散に移している。査読を経ていない投稿前原稿である点にも注意が要る。

### 音を出す身体と生体的な要素

- Jagmohan Chauhan, Yining Hu, Suranga Seneviratne, Archan Misra, Aruna Seneviratne, Youngki Lee, "BreathPrint: Breathing Acoustics-based User Authentication", MobiSys 2017, pp. 278-291。 https://doi.org/10.1145/3081333.3081355 。息を吹く音を生体的な特徴として認証に使う研究である。CipherFluteが「誰が吹いても同じ音が出る」ことを利点にしているのと正反対の設計である。
- M. L. Shuwandy, B. B. Zaidan, A. A. Zaidan, "Novel authentication of blowing voiceless password for android smartphones using a microphone sensor", Multimedia Tools and Applications, pp. 44207-44243, 2022年。 https://doi.org/10.1007/s11042-022-13264-6 。携帯電話のマイクロホンに息を吹きかけるパターンを合言葉にする方式である。同誌に訂正記事（ https://doi.org/10.1007/s11042-022-13386-x ）が出ている点に注意が要る。
- Tomi Kinnunen, Md Sahidullah, Héctor Delgado, Massimiliano Todisco, Nicholas Evans, Junichi Yamagishi, Kong Aik Lee, "The ASVspoof 2017 Challenge: Assessing the Limits of Replay Spoofing Attack Detection", Interspeech 2017, pp. 2-6。 https://doi.org/10.21437/interspeech.2017-1111 。話者照合における録音再生攻撃の検出を競う共通課題である。音を秘密として使う方式がリプレイに悩まされることを端的に示す。

### 音響サイドチャネル攻撃

- Dmitri Asonov, Rakesh Agrawal, "Keyboard acoustic emanations", IEEE Symposium on Security and Privacy 2004, pp. 3-11。 https://doi.org/10.1109/secpri.2004.1301311
- Li Zhuang, Feng Zhou, J. D. Tygar, "Keyboard acoustic emanations revisited", CCS 2005, pp. 373-382。 https://doi.org/10.1145/1102120.1102169 。雑誌版は同じ著者・同じ題名で、ACM Transactions on Information and System Security, 第13巻 第1号, pp. 1-26, 2009年, https://doi.org/10.1145/1609956.1609959 である。
- Yigael Berger, Avishai Wool, Arie Yeredor, "Dictionary attacks using keyboard acoustic emanations", CCS 2006, pp. 245-254。 https://doi.org/10.1145/1180405.1180436
- Tong Zhu, Qiang Ma, Shanfeng Zhang, Yunhao Liu, "Context-free Attacks Using Keyboard Acoustic Emanations", CCS 2014, pp. 453-464。 https://doi.org/10.1145/2660267.2660296
- Michael Backes, Markus Dürmuth, Sebastian Gerling, Manfred Pinkal, Caroline Sporleder, "Acoustic Side-Channel Attacks on Printers", USENIX Security Symposium 2010, pp. 307-322。 https://dblp.org/rec/conf/uss/BackesDGPS10.html （DBLPの当該書誌記録で題名・著者・会議名・ページ・年を確認した）。学会の予稿集ページ https://www.usenix.org/legacy/events/sec10/tech/ にも同じ題名と著者が掲載されている。当初の確認先はDBLPの検索用の応用プログラム接続口を指す綴りであって特定の文献を指していなかったため、2026年7月30日の検証で書誌記録そのものの位置に差し替えた。
- Daniel Genkin, Adi Shamir, Eran Tromer, "RSA Key Extraction via Low-Bandwidth Acoustic Cryptanalysis", CRYPTO 2014, Lecture Notes in Computer Science, pp. 444-461。 https://doi.org/10.1007/978-3-662-44371-2_25 。計算機が発する高周波の音から秘密鍵を抽出した研究である。
- Alberto Compagno, Mauro Conti, Daniele Lain, Gene Tsudik, "Don't Skype & Type! Acoustic Eavesdropping in Voice-Over-IP", AsiaCCS 2017, pp. 703-715。 https://doi.org/10.1145/3052973.3053005 。これを発展させた雑誌論文が、Stefano Cecconello, Alberto Compagno, Mauro Conti, Daniele Lain, Gene Tsudik, "Skype & Type: Keyboard Eavesdropping in Voice-over-IP", ACM Transactions on Privacy and Security, 第22巻 第4号, pp. 1-34, 2019年, https://doi.org/10.1145/3365366 である。当初この行には「雑誌版は」とだけ書かれ、題名も著者も示されていなかったが、2026年7月30日の検証で、雑誌論文は題名が異なり（感嘆符が無く、副題が Keyboard Eavesdropping in Voice-over-IP に変わっている）、筆頭にStefano Cecconelloが加わって著者が五名になっていることを確認したため、書誌情報を明記した。単なる再録ではないので、引くときは別の文献として扱うのが正確である。
- Joshua Harrison, Ehsan Toreini, Maryam Mehrnezhad, "A Practical Deep Learning-Based Acoustic Side Channel Attack on Keyboards", IEEE European Symposium on Security and Privacy Workshops 2023, pp. 270-280。 https://doi.org/10.1109/eurospw59978.2023.00034
- Daniel Arp, Erwin Quiring, Christian Wressnegger, Konrad Rieck, "Privacy Threats through Ultrasonic Side Channels on Mobile Devices", IEEE European Symposium on Security and Privacy 2017, pp. 35-47。 https://doi.org/10.1109/eurosp.2017.33 。当初この行には「人間に聞こえない音を機器の対応づけに使う商用技術の危険性を示した研究である」と書かれていたが、2026年7月30日の検証で要旨に当たったところ、主題は機器の対応づけではなく利用者の追跡であった。音声や店舗の中に超音波のビーコンを埋め込み、携帯電話のマイクロホンでそれを拾うことで、利用者の現在位置を突き止め、テレビの視聴傾向を覗き、同じ人物の複数の端末を紐づけるという商用の追跡技術が対象である。著者らは三つの商用の実装を調べ、欧州の二都市の35店舗のうち4店舗で位置追跡に使われる信号を検出し、超音波のビーコンを利用者に知られないまま常時聞き続けているAndroidのアプリを234件見つけた。テレビ放送については七か国の配信を調べたが検出されなかった。
- Benjamin Quattrone, Youakim Badr, "A Survey on Acoustic Side-Channel Attacks: An Artificial Intelligence Perspective", Journal of Cybersecurity and Privacy, 第6巻 第1号, 論文番号6, 2025年12月29日。 https://doi.org/10.3390/jcp6010006 。音響サイドチャネル攻撃の全体像を一件で引くための総説である。2020年1月から2025年2月までの研究を体系的に見渡し、文字列の復元をどこまで細かく行うかによって三つの水準に分けている。巻号が第6巻でありながら発行日が2025年末である点は、CrossrefとOpenAlexの双方で確認した。
- Sujit Rokka Chhetri, Arquimedes Canedo, Mohammad Abdullah Al Faruque, "Confidentiality Breach Through Acoustic Side-Channel in Cyber-Physical Additive Manufacturing Systems", ACM Transactions on Cyber-Physical Systems, 第2巻 第1号, pp. 1-25, 2017年。 https://doi.org/10.1145/3078622
- Seyed Ali Ghazi Asgar, Narasimha Reddy, "QuietPrint: Protecting 3D Printers Against Acoustic Side-Channel Attacks", 第12回ACM Cyber-Physical System Security Workshop, pp. 25-34, 2026年。 https://doi.org/10.1145/3775042.3807880 。3Dプリンタの音響漏洩に対する対策側の研究である。大型のスピーカーや雑音打ち消し装置を足すのではなく、G-codeに最小限の改変を加えるだけで造形物を守る点を利点として掲げている。
- Christos Madamopoulos, Nektarios Georgios Tsoutsos, "3D printer audio and vibration side channel dataset for vulnerability research in additive manufacturing security", Data in Brief, 第57巻, 論文番号111002, 2024年12月。 https://doi.org/10.1016/j.dib.2024.111002 。当初この行の題名は "3D printer audio and vibration side channel dataset" までで切れていたため、2026年7月30日の検証で完全な題名と巻号に直した。内容も確認した。熱溶解積層方式のプリンタ2機種、すなわち Bambu Lab P1P と A1 mini について、iPhoneのアプリとTeensy 4.0のセンサ装置という二通りの方法で、印刷中の音と三軸の加速度を収録し、12種類の造形物ぶんを公開している。設計ファイルとG-codeと3mfファイルも付いている。CipherFluteはA1 miniで笛を刷っているため、この一件はCipherFluteの脅威モデルに直接効く。
- Sina Faezi, Sujit Rokka Chhetri, Arnav Vaibhav Malawade, John Charles Chaput, William Grover, Philip Brisk, Mohammad Abdullah Al Faruque, "Acoustic Side Channel Attack Against DNA Synthesis Machines: Poster Abstract", ICCPS 2020, pp. 186-187。 https://doi.org/10.1109/iccps48487.2020.00026 。当初は「Sina Faezi ほか」と略していたが、2026年7月30日の検証でCrossrefの記録から全員の綴りを確認したので補った。

### 音楽を鍵とする認証の日本語文献および周辺

- 古賀千裕, 佐藤敬, 「混合された環境音の聞き取りに基づく認証方式」, コンピュータセキュリティシンポジウム2017論文集, 第2017巻 第2号, 情報処理学会, 2017年10月16日。 https://cir.nii.ac.jp/crid/1050292572146803072 および https://ipsj.ixsq.nii.ac.jp/records/187312 （書誌記録と要旨を確認した）。当初この行には「複数の環境音を混ぜて聞かせ、その聞き分けを認証に使う方式である」と書かれていたが、2026年7月30日の検証で情報処理学会電子図書館の要旨に当たったところ、内容の説明が誤っていた。この論文が提案しているのは人間と自動化された処理を見分けるCAPTCHAであって、秘密の音を鍵にする利用者認証ではない。動機は、視覚障がいのある人でも使える音声型のCAPTCHAにおいて、既存の英数字識別型では音声の聞き取りが難しく解答に時間がかかるという二つの問題を解くことである。そこで、雑音の加わった音声を聞き分けるかわりに、混合された環境音を聞き分けさせる。環境音の識別は人間には易しく自動化された処理には難しいと期待できるという着想である。評価は人間による解答容易性と解答時間について行われている。題名に「認証方式」とあるために取り違えやすいので、引く際には注意が要る。
- 堀孝浩, 喜多義弘, 豊田健太郎, 朴美娘, 岡崎直宣, 「「テンポ感」を特徴量としたリズム認証の認証精度に関する考察」, コンピュータセキュリティシンポジウム2015論文集, 第2015巻 第3号, pp. 779-786, 情報処理学会, 2015年10月14日。 https://cir.nii.ac.jp/crid/1050855522069274880 および https://ipsj.ixsq.nii.ac.jp/records/146895 。要旨によれば、覗き見攻撃への対策として曲に合わせて画面を叩くリズム認証を提案してきたが精度が足りず、同じ曲でも利用者ごとに1音ごとの間隔に癖があると考えてこれを「テンポ感」と定義し、特徴量に加えたときの精度への影響を論じている。ここでも個人差が安全性の土台になっており、CipherFluteとは向きが逆である。
- 野口敦弘, 納富一宏, 斎藤恵一, 「自己組織化マップを用いたタッチスクリーンによるリズム認証手法」, バイオメディカル・ファジィ・システム学会誌, 第15巻 第1号, pp. 31-39, 2013年。 https://doi.org/10.24466/jbfsa.15.1_31 および https://cir.nii.ac.jp/crid/1390282679457668096 。要旨によれば、ピアノ経験が10年を超える者を含む三種類の被験者群で、叩くリズムの個人差を自己組織化マップで解析している。
- 大内結雲, 野崎真之介, 佐々木葵, 奥村紗名, 吉平瑞穂, 芹澤歩弥, 大木哲史, 西垣正勝, 「スマートフォンのタップ音からの入力内容推測可能性に関する研究」, 電子情報通信学会論文誌A（基礎・境界）, 第J105-A巻 第12号, pp. 156-167, 2022年12月。 https://doi.org/10.14923/transfunj.2022bap0004 および https://cir.nii.ac.jp/crid/1390857158422008704 。日本語圏における音響サイドチャネルの研究である。要旨によれば、正規の利用者がスマートフォンに文字を打つときのタップ音を攻撃者が外部のマイクロホンで盗聴するという想定のもとで、最も良い場合に29.4パーセントの識別率を得た。さらに、キーとタップ音の対応が入れ替わるように配置を変えたときの精度も評価している。
- Marcia Gibson, Marc Conrad, Carsten Maple, Karen Renaud, "Accessible and secure? Design constraints on image and sound based passwords", 2010 International Conference on Information Society, pp. 423-428。 https://doi.org/10.1109/i-society16502.2010.6018741 。要旨の主題はデジタル排除である。認証の仕組みが排除に加担している面を論じ、使いやすさと安全性の間に知られた緊張があることを踏まえて、画像や音を用いる方式においてアクセシビリティの目標と安全性の目標が衝突する箇所をいくつも指摘している。本文の主節で当初「視覚障害や識字障害のある利用者に向けた設計制約の検討」と述べていた点は、要旨がそこまで特定していないため、2026年7月30日の検証でより忠実な表現に改めた。
- Marcia Gibson, Karen Renaud, Marc Conrad, Carsten Maple, "Play That Funky Password! Recent Advances in Authentication with Music", Handbook of Research on Emerging Developments in Data Privacy, pp. 101-132, 2015年。 https://doi.org/10.4018/978-1-4666-7381-6.ch006 。音楽による認証の総説であり、この切り口を一件でまとめて引くのに適している。
- Marcia Gibson, Karen Renaud, Marc Conrad, Carsten Maple, "Music is the Key: Using our Enduring Memory for Songs to Help Users Log On", Strategic and Practical Approaches for Information Security Governance, pp. 137-157, 2012年。 https://doi.org/10.4018/978-1-4666-0197-0.ch008 。同内容がIT Policy and Ethics（2013年, https://doi.org/10.4018/978-1-4666-2919-6.ch046 ）にも収録されている。

## 検証で書誌情報を新たに補えたもの

2026年7月30日の検証で、当初「一次資料にあたれなかった」とされていた項目のうち一件について、一次的な書誌記録を見つけることができた。

- A. Weaver, N. A. Newell, "In-Band Single-Frequency Signaling", Bell System Technical Journal, 第33巻 第6号, pp. 1309-1330, 1954年11月。 https://doi.org/10.1002/j.1538-7305.1954.tb03755.x 。Crossrefの書誌記録で題名・著者・誌名・巻号・ページ・年を確認し、この識別子がIEEE Xploreの当該文献（文献番号6769690）へ解決することも確認した。これが、電話網の帯域内単一周波数信号方式を記述したベル研究所側の一次文献である。いわゆる2600ヘルツの笛による不正接続（ブルーボックス）の背景として引くのに適する。ただし注意が要る。論文の本文および要旨をIEEE Xploreから取得できなかったため、「2600ヘルツ」という具体的な周波数がこの論文に書かれていることは確認できていない。周波数の数値まで論文で裏を取るなら、本文の入手が必要である。この論文が本研究の枠組みによく合う理由は、物体（笛）が出す音がそのまま網の制御鍵として働いた歴史的事例であり、CipherFluteが「音を鍵にする」ことの最古の大衆的な実例だからである。脅威の度合いは低である。学術的な新規性を争う相手ではなく、導入で位置づけを語るための歴史的な背景である。

## 未検証のまま残ったもの

- 近距離の可聴域外の音を第二要素に使う商用技術として、2014年にGoogleが買収したSlickLoginという事例が知られているが、学術的な一次資料を確認できなかったため、実在と技術内容の両方を未確認のまま残す。2026年7月30日の検証でも状況は変わらなかった。企業の事例であるため一次資料は当事者自身の公表物になるが、その所在を確かめられていない。
- 「Musical password based biometric authentication」（Ravi Prakash, Suresh Kumar, Chandan Kumar, K. K. Mishra, 2016 International Conference on Computing, Communication and Automation, pp. 1016-1019, 2016年, https://doi.org/10.1109/ccaa.2016.7813865 ）と「User Authentication using Musical Password」（Naveen Kumar, International Journal of Computer Applications, 第59巻 第9号, pp. 1-4, 2012年, https://doi.org/10.5120/9573-4048 ）と「Graphical Password based Authentication System with Sound Sequence」（Shabina Sayed, Aman Mohid, Manish Pal, Murtaza Haji, International Journal of Computer Applications, 第138巻 第12号, pp. 38-43, 2016年, https://doi.org/10.5120/ijca2016909072 ）は、書誌情報の上では実在を確認した。2026年7月30日の検証で、当初は書かれていなかった著者名と巻号ページをCrossrefの記録から補った。ただし本文を読んでいないため、内容と質の評価はできていない。査読の質が高くない媒体であるため、引用するかどうかは慎重に判断すべきである。
- Musipass（NSPW 2009）の認証機構が再認方式であるかどうかは未確認である。ACM Digital Libraryが機械的な取得を拒み、University of Bedfordshireのリポジトリにあった全文（ハンドル10547/270603）はリンクが切れているため、要旨より詳しい情報を得られなかった。
- HAPADEP（ISC 2008）の検証段の詳しい作法は未確認である。データと検証情報の両方を音響チャネルでやりとりすることは要旨で確認できたが、検証の段で何を鳴らし、人間が何と何を聞き比べるのかは確認できていない。全文がSpringerの購読者向けに限られ、International Association for Cryptologic Researchの電子公開資料も取得できなかった。
- Talking to Strangers（NDSS 2002）が「場所限定チャネル」という用語を導入したという記述は未確認である。学会の予稿集ページには題名と著者と年しか掲載されておらず、要旨が無いため用語の有無を確かめられなかった。全文の電子ファイルは同ページに掲げられているので、これを読めば確認できる見込みが高い。
- 太田正哉・山下勝己の信学技報（2003年）の内容は未確認である。CiNii Researchと国立国会図書館の記録には要旨が無く、付与された主題語三語しか手がかりが無い。認証される対象が電話機なのか利用者なのかも分かっていない。

## この切り口で見つからなかったこと

以下は、探したうえで見つからなかったことである。CipherFluteの新規性の主張の根拠になるので、丁寧に書いておく。

第一に、電源も電子部品も持たない受動的な物体が、それ自身の共鳴周波数の列として暗号鍵や復元用情報を保持し、それを吹くことで読み出すという方式は見つからなかった。音を鍵にする研究はすべて、音の発生源が人間（歌う、叩く、吹く、話す）か、電源を持つ機器（スピーカー、プリンタ、計算機）のいずれかであった。物体そのものが音高の符号として鍵素材を持ち、吹く人が誰であっても同じ符号が出るという形は、CrossrefとDBLPとCiNiiのいずれの検索でも該当が出なかった。

第二に、音響チャネルに秘匿性をまったく期待しないと明示的に宣言したうえで、安全性の責任をすべて秘密分散に移すという設計は見つからなかった。もっとも近いのはAcoustic Integrity Codes（WiSec 2020）だが、これは音響チャネルに完全性を期待する設計であり、秘密分散とは組み合わせていない。HaleviとSaxenaのCCS 2010は音響チャネルの秘匿性が成り立たないことを示したが、それを前提とした肯定的な設計は与えていない。

第三に、音高を離散的なスロットに量子化し、既知の音高を持つ基準音を混ぜて全体のずれを打ち消し、そのうえで誤り訂正符号と隣接同一値の禁止を課す、という符号設計を認証や鍵運搬に適用した研究は見つからなかった。この組み合わせは通信工学では標準的だが、認証の文脈で音に適用した例は見当たらない。

第四に、口笛や笛といった気鳴楽器を認証や鍵の運搬に使った研究は、日本語文献では皆無であった。CiNii Researchで「口笛 認証」「笛 認証 鍵」「音響 トークン 認証 音波」のいずれで検索しても、論文・書籍・博士論文・研究データのすべてで結果が零件であった。この零件という結果は、2026年7月30日の検証で独立に追試した。CiNii ResearchのOpenSearch接続口に同じ三つの問い合わせを投げ、いずれも該当件数が0であることを確かめた。さらに「笛 秘密鍵」「音高 符号化 秘密」「3Dプリント 音 認証」の三つを足して調べたが、これらも0件であった。「リコーダー 認証」は1件、「共鳴周波数 情報 埋め込み」は3件返ったが、内容はそれぞれ大学の環境管理、医用画像や核物理、野生の猿の個体識別であり、いずれも本研究とは無関係であった。したがって当初の主張はそのまま成り立つ。

第五に、旋律や音を暗証番号の代わりに使う研究のうち、覚えやすさと安全性の兼ね合いを大規模に測ったものは、Gibsonらの一連の仕事以外にはほとんど見当たらなかった。音を鍵にする認証は、この十数年で「人間の記憶に預ける」方向から「機器が観測する環境音に預ける」方向へ移っており、記憶容易性の研究としては細い流れのまま止まっている。CipherFluteが「人間の記憶をまったく使わない」立場を取ることは、この流れの外側に位置する。

第六に、3Dプリンタの音響サイドチャネルに関する研究群は、いずれも「造形物の形状という知的財産を守る」ことを目的としており、「造形物の形状が暗号鍵そのものである」場合を扱ったものは見つからなかった。この点は2026年7月30日の検証でも変わらなかった。Song らのCCS 2016、Al Faruque らのICCPS 2016、Chhetri らのACM Transactions on Cyber-Physical Systems誌の論文、QuietPrint、Madamopoulos と Tsoutsos のデータセットの五件すべてについて要旨を読み直したが、守るべきものとして挙げられているのは一貫して知的財産としての設計情報であった。CipherFluteは形状そのものが鍵であるという場合に該当するため、既存の攻撃研究の帰結を新しい文脈に持ち込む立場になる。ただしこれは新規性の主張というより、脅威モデルの負債である。形状が知的財産であるだけなら復元の誤差が5.87パーセントあっても被害は限定的だが、形状が鍵であれば1本の笛の音高スロットを1個読み違えるだけで鍵は復元できない代わりに、逆に十分な精度が出れば鍵がそのまま漏れる。誤差と被害の関係が既存研究とは違う形になるので、この違いは自分の言葉で書いておくべきである。

## 調べ残した穴

- 音声そのものを合言葉にする話者照合の研究は、量が膨大であるため、ASVspoof 2017の共通課題論文一件を代表として押さえるにとどめた。話者照合における「秘匿できない生体情報をどう鍵として扱うか」という議論には、CipherFluteの立場と響き合う蓄積がある可能性が高く、追い切れていない。
- SOUPSの予稿集を年ごとに直接あたることができなかった。SOUPSは2015年から2018年まではUSENIXが、2019年以降はACMが刊行しており、刊行元をまたぐため一括の検索がしにくい。音を使う認証の使い勝手を測った研究がSOUPSにある可能性は残る。
- WISSとインタラクションの各年のプログラムページを直接あたることができなかった。日本語圏のヒューマンコンピュータインタラクション分野に、音を鍵にする発表がある可能性は残る。CiNiiはこの二つの会議を十分に索引していないため、会議のウェブサイトを年ごとに開いて確認する作業が要る。
- 音響サイドチャネルに対する「規格上の対策」については、TEMPEST関連の規格や暗号モジュールの物理セキュリティ要件（ISO/IEC 19790やFIPS 140-3）が音響漏洩をどこまで扱っているかを確認できなかった。触れるのであれば規格本文を確認する必要がある。
- 有力文献の被引用一覧をたどる芋づる式の探索が、Semantic ScholarとOpenAlexの両方が要求回数の制限で応答しなかったため、ほとんどできなかった。特にMusipassとSound-Proofの被引用一覧は、この切り口の網羅性を上げるうえで見ておく価値が高い。
- 特許文献をまったく見ていない。音を鍵にする認証は商用化の動機が強い領域であり、論文になっていない実装が特許として存在する可能性が高い。
- 2026年7月30日の検証でも、Semantic ScholarとOpenAlexの被引用一覧をたどる芋づる式の探索はできていない。今回の作業時間はすべて既存の記載の照合に充てた。したがって網羅性の穴は当初のまま残っている。

## 検証で削除したもの

該当なしである。2026年7月30日の検証では、一件も削除しなかった。ファイルに挙げられていた文献はすべて、Crossref、DBLP、CiNii Research、情報処理学会電子図書館、出版社のページ、学会の予稿集ページのいずれかで実在を確認できた。存在しない文献をつかまされた形跡はなかった。誤りはいずれも、実在する文献についての書誌情報の不足か、内容の記述の食い違いであった。

## 検証の記録

2026年7月30日、この文書の書誌情報と内容の記述を、原稿を書いた調査担当者とは別の担当者が独立に検証した。検証には、CrossrefのDOI書誌応用プログラム接続口、DBLPの書誌記録、OpenAlexとSemantic Scholarが保持する要旨、CiNii Researchの書誌記録と情報処理学会電子図書館、Springerの当該章のページ、USENIXの予稿集ページ、NDSS Symposiumの予稿集ページを用いた。なおWeb検索の回数上限は、原稿を書いた時点と同じくこの検証時点でも尽きていたため、検索エンジンは使えなかった。原稿の冒頭でその旨が断られていたことは事実であると確認できた。

確認した書誌記録は延べ60件、重複を除いて57件である。内訳は、DOIを持つ文献51件（延べ数。重複3件を除くと48件）、CiNii Researchの識別子で示された日本語文献5件、DOIを持たない文献としてSound-Proof（USENIXの予稿集ページとBibTeX記録）、Backesらのプリンタの論文（DBLPの書誌記録とUSENIXの予稿集ページ）、Talking to Strangers（NDSS Symposiumの予稿集ページ）の3件、および検証の過程で新たに突き止めたベル研究所の技術誌の論文1件である。この57件はすべて実在した。著者名の綴り、題名、会議名または雑誌名、年、巻号ページのいずれかに疑いが残ったものは一件も無い。

ファイルへの書き込みは、性質の異なる三種類に分けられる。第一に、原典と食い違っていた明確な誤りの訂正が18件である。第二に、巻号やページや論文番号や著者の全員の綴りなど、書誌情報の欠落を埋めた補足が22か所である。第三に、原典の要旨または全文で裏を取った数値や機構の説明の追加が17か所である。以下では第一の18件を、重いものから順に述べる。

最も重い誤りは3件である。第一に、Song らのCCS 2016の論文について、攻撃が使うセンサを「マイクロホンと加速度センサ」と書いていたのを「音響と磁気の二つのサイドチャネル、すなわちマイクロホンと磁気センサ」に直した。原典は磁気の情報でノズルの向きを伴う動作を補強して推定しており、加速度センサは使っていない。第二に、古賀千裕と佐藤敬のコンピュータセキュリティシンポジウム2017の論文について、「環境音の聞き分けを認証に使う方式」と書いていたのを、人間と自動化された処理を見分けるCAPTCHAであると直した。題名に「認証方式」とあるため取り違えやすいが、要旨は視覚障がいのある人でも使える音声型のCAPTCHAの改良であると明言している。第三に、Loud and Clearの機構について、「公開鍵の指紋を英語の文や旋律に変換して読み上げ、人間が二つの機器から同じものが聞こえることを確認する」と書いていたのを、公開鍵のハッシュから導いた英語らしい構文の文を片方の機器が音声合成で読み上げ、もう一方の機器が同じ情報を画面に表示し、人間が耳と目で突き合わせる方式であると直した。旋律への変換は原典の要旨に現れず、確認は耳を二度使うのではなく耳と目を組み合わせる。

残る15件の誤りを挙げる。TapSongsの照合手法を「統計的な手法」から「絶対的な一致基準と、成功したログインからの学習」に直した。Beat-PINについて、要旨で裏の取れない覗き見耐性の議論への言及を削り、鍵空間の理論的解析という裏の取れた部分だけを残した。HaleviとSaxenaのCCS 2010について、裏の取れない「離れた場所」という距離への言及を削った。Sound-Proofについて、共在する攻撃者への弱さは後から指摘されたのではなく原論文自身が対象外だと明記していることに直し、後から示されたのは環境音を推測または操作する遠隔攻撃者への脆弱性であると書き分けた。SpiKeyについて、「合鍵を作る攻撃」を「33万本超の候補を3本まで絞り込む模擬実験としての概念実証」に直した。HAPADEPについて、裏の取れない「短い確認用の旋律を二つの機器から鳴らして人間が聞き比べる」という記述を削った。Musipassの認証機構が再認方式であるという裏の取れない記述を削った。Musipassの項で同じ著者らのi-Society 2010の論文を「視覚障害や識字障害のある利用者に向けた設計制約の検討」と説明していたのを、要旨に忠実な「画像や音を用いるパスワードにおいてアクセシビリティと安全性の目標が衝突する点の検討」に直した。太田正哉と山下勝己の信学技報について、「旋律は電話機の識別に使われている」という裏の取れない記述を削り、未確認である旨を明記した。Skype & Typeの雑誌論文について、単なる再録であるかのように書かれていたのを、題名が異なり著者が五名に増えた別の文献であると直した。Backesらの論文の確認先が、特定の文献を指さないDBLPの検索用接続口の綴りであったため、書誌記録そのものの位置に差し替えた。Madamopoulos と Tsoutsos のデータセットについて、途中で切れていた題名を完全な題名に直した。Arp らの超音波の論文について、主題が機器の対応づけではなく利用者の追跡であると直した。Talking to Strangersについて、「場所限定チャネル」という用語の導入が予稿集ページからは確認できない旨を明記した。そして節の見出しが内容を過大に表していた点を直した。

文献の置き場所も一件変えた。「未検証のまま残ったもの」に置かれていた音響の物理的複製困難関数の投稿前原稿について、Crossrefから要旨の全文を取得できたので、内容の評価をつけて背景の節へ移した。内容は二酸化クロムの微粒子とシルクフィブロインの複合材による偽造防止の材料研究であり、複製できないことを価値とする点でCipherFluteとは目的が正反対であるため、脅威の度合いは低と判定した。

新たに一次資料を突き止めたものが一件ある。電話網の帯域内単一周波数信号方式については、当初「一次資料にあたることができなかった」とされていたが、Weaver と Newell によるBell System Technical Journal誌の1954年の論文を見つけ、書誌情報を確認した。ただし2600ヘルツという具体的な周波数がこの論文に書かれていることは、本文を取得できなかったため未確認である。

未検証のまま残ったものは6件に整理した。内訳は、商用技術SlickLoginの一次資料、査読の質が高くない媒体に載った音楽パスワードの3件の内容、Musipassの認証機構が再認方式であるかどうか、HAPADEPの検証段の詳しい作法、Talking to Strangersにおける「場所限定チャネル」という用語の有無、そして太田正哉と山下勝己の信学技報の内容である。いずれも、書誌情報そのものは確認できているが、本文または要旨を取得できなかったために内容を裏付けられなかったものである。

最後に、この検証で最も強調したい点を書いておく。この切り口には、CipherFluteの新規性を崩す文献は無かった。誤りの訂正は18件出たが、そのすべてが実在する文献についての記述の精度の問題であり、位置づけの結論を覆すものではない。一方で、脅威モデルには実際に穴があることが検証によってはっきりした。3Dプリンタの印刷音から形状を復元する攻撃は、公開されたデータセットの測定機種にCipherFluteが使っている Bambu Lab A1 mini が含まれるところまで来ている。「形状を計測されれば読める」と認めるだけでは足りず、「印刷している最中に、離れた場所から音だけで読まれうる」ところまで書かないと、査読でここを突かれる。
