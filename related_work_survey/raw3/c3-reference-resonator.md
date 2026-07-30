# C3　反例検証：基準共鳴器を同居させて比で読み共通モードを除く設計

対象とする主張は、CipherFluteの新規性主張のうち「既知の値を持つ基準素子を同じ物体に同居させ、比で読んで環境変動を打ち消すという構造的な自己補正は、造形物への情報埋め込みの文脈で前例がない」という部分である。評価者はこれに対して、Smith と Senturia が1995年に同じ構成を「conventional sensing setup」と呼んでいること、および2014年に表面弾性波共鳴器の一方を基準に使う無線受動センサが実装されていることを反例として挙げた。

調査日は2026年7月30日である。

## 0. 結論

反例は正しい。評価者が挙げた2件はどちらも実在し、内容も評価者の説明どおりである。とくにSmithとSenturiaの論文は、基準共鳴器と検出共鳴器の二つを置いて比を取る構成を、自分たちの新規性としてではなく前提となる「従来の構成」として明示的に記述している。したがって「基準素子を同居させ比で読んで共通モードを打ち消す」という着想そのものをCipherFluteの新規性として主張することは成立しない。ただし後述するとおり、主張を「共鳴管を3Dプリントで一体成形した情報担体における実装と、そのもとでの読み取り誤り率の測定」に限定して書き換えれば、誇張のない形で残せる。

## 1. 反例1：Smith と Senturia（1995年）

### 1.1 書誌の確定

- 著者は James H. Smith（Sandia National Laboratories）と Stephen D. Senturia（Massachusetts Institute of Technology）である。
- 題名は "Self-Consistent Temperature Compensation for Resonant Sensors with Application to Quartz Bulk Acoustic Wave Chemical Sensors" である。
- 掲載は Proceedings of the International Solid-State Sensors and Actuators Conference（TRANSDUCERS '95）、開催地はスウェーデンのストックホルム、掲載ページは724ページから727ページ、発行者は IEEE、発行年は1995年である。
- デジタルオブジェクト識別子は 10.1109/SENSOR.1995.721934 である。

確認先は次の2つである。

- 著者所属機関が公開している原稿本文（Sandia National Laboratories）: https://www.sandia.gov/app/uploads/sites/145/2021/11/5_7SelfConsistent.pdf
- Crossref の書誌レコード: https://api.crossref.org/works/10.1109/sensor.1995.721934

Sandiaが公開している原稿の1ページ目の版面上部には "Transducers, June 1995." と刷られており、Crossrefの登録内容と一致する。本文はこのPDFから `pdftotext -layout` で抽出して読んだ。

### 1.2 原文の記述

温度補償の節の冒頭に次の一文がある。

> "The temperature compensation scheme uses the conventional sensing setup of two resonators, a sense resonator (with frequency f1) and a reference resonator (with frequency f2)."

評価者が指摘した "conventional sensing setup" という語は、この文のとおり原文に存在する。著者自身が、検出共鳴器と基準共鳴器を二つ置く構成を「従来からある構成」と位置づけたうえで、その上に自分たちの回路上の工夫を載せている。

比を取ることについては、次の記述がある。

> "Thus the result of the counting operation (N) can be represented by the divider (D) and the ratio of f1 to f2."

そして共通モードの除去については、式 `N = D f1/f2 = D f01 T(t) X(x) / (f02 T(t) X(0)) = D f01 X(x) / f02` を導いたうえで、次のように述べている。

> "Thus the first-order effects of temperature and other common mode interferents can be eliminated from the final signal."

温度依存項 `T(t)` が分子と分母で同じであるために比を取ると消える、という論法であり、CipherFluteの基準笛の説明とまったく同じ構造である。

さらに、著者たちは1995年の時点ですでにこの種の手法に先行研究があることを明示している。

> "A number of methods for temperature compensation utilizing two resonators have been described in the literature [1, 2]."

> "A method similar to the compensation scheme used here has been previously described for use with external frequency counters, although no temperature-stability data was reported [4]."

参照されている文献は、[1] が Slobodnik, Colvin, Roberts, Silva, "A Digitally Compensated SAW Oscillator", Proc. 1981 Ultrasonics Symposium, pp. 135–138、[2] が Alder, Fox, Przybylko, Rezgui, Snook, Analyst, 114(9), p. 1163, 1989、[4] が Joshi, "A Temperature Compensated High Voltage Probe Using Surface Acoustic Waves", Proc. 1982 Ultrasonics Symposium, pp. 317–320 である。つまり二共鳴器による温度補償という考え方は、1995年よりさらに10年以上さかのぼる。

なお、この論文自身の新規性は「比を取ること」ではなく「基準共鳴器の周波数を分周して周波数カウンタの時間基準そのものに使い、比の計算を外部の演算ではなくカウント動作の中で行い、それを共鳴器駆動用の集積回路に載せたこと」である。結論部でも、比較対象は二つの外部カウンタの読みを引き算する従来手法である。

> "This circuit has shown approximately an order of magnitude improvement in compensation over the conventional frequency-subtraction temperature compensation method using external frequency counters."

化学センサとしての使い方についても、被覆した検出用共鳴器と無被覆の基準用共鳴器を並べる図が示されている（図4の説明文）。

> "Use of a poly-(isobutylene)-coated sense resonator and an uncoated reference resonator to sense three different concentrations of trichloroethylene (4.4%, 0.9%, and 0.2%)."

## 2. 反例2：Wang ら（2014年）

### 2.1 書誌の確定

- 著者は Wen Wang、Xufeng Xue、Yangqing Huang、Xinlu Liu である。
- 題名は "A Novel Wireless and Temperature-Compensated SAW Vibration Sensor" である。
- 掲載は Sensors 誌の第14巻第11号、20702ページから20712ページ、発行年は2014年である。
- デジタルオブジェクト識別子は 10.3390/s141120702 であり、PubMed識別子は25372617、PubMed Central識別子は PMC4279507 である。
- 受理と公開の日付は、受領が2014年9月23日、採録が2014年10月27日、公開が2014年11月3日である。

確認先は次の2つである。

- Crossref の書誌レコード: https://api.crossref.org/works/10.3390/s141120702
- PubMed Central の全文: https://pmc.ncbi.nlm.nih.gov/articles/PMC4279507/

出版社であるMDPIのページ（https://www.mdpi.com/1424-8220/14/11/20702）は自動取得が拒否されたため、CrossrefとPubMed Centralで確定させた。評価者が示したデジタルオブジェクト識別子のリンクは、実際にこのMDPIのページへ転送される。

### 2.2 原文の記述

同一の水晶片持ち梁の上に一端子型の表面弾性波共鳴器を二つ作り込み、一方を検出用、他方を基準用としている。

> "One resonator acts as the sensing device adjacent to the clamped end for maximum strain sensitivity, and the other one is used as the reference located on clamped end for temperature compensation for vibration sensor through the differential approach."

効果についても数値が示されている。

> "the difference frequency-dependence is only 18.6 Hz/°C in testing temperature range of 20∼120, far less than the cross-temperature sensitivity of the single sensing resonator (8.6 kHz/°C)"

ここで注意すべき差異が一つある。この論文が取っているのは周波数の比ではなく差である。共通モードを打ち消すという目的と、基準素子を同じ物体に同居させるという構造は同じであるが、演算は差分である。比を取る形での記述はSmithとSenturiaの側にある。

この論文において著者たちが自分の新規性としているのは、無線受動の振動センサとして片持ち梁の寸法と表面弾性波素子の設計を最適化して高い感度を得たことであり、差動構成そのものは達成手段として位置づけられている。

> "This sensor presents many advantages over other currently available vibration sensors: (1) it provides high sensitivity through optimal design by using the established theory model on response mechanism; (2) the temperature dependence is compensated effectively by using the differential structure..."

## 3. 分野における確立度

「基準素子を同居させて共通モードを除く」という設計が、微小電気機械システム、水晶振動子、表面弾性波デバイスの各分野でどの程度定着しているかを、総説と査読論文の一次資料で確認した。

### 3.1 微小電気機械システムの総説

- 著者は Yusi Zhu、Zhan Zhao、Zhen Fang、Lidong Du である。
- 題名は "Dual-Resonator-Based (DRB) and Multiple-Resonator-Based (MRB) MEMS Sensors: A Review" である。
- 掲載は Micromachines 誌の第12巻第11号、論文番号1361、発行年は2021年である。
- デジタルオブジェクト識別子は 10.3390/mi12111361 である。
- 確認先は https://api.crossref.org/works/10.3390/mi12111361 と https://pmc.ncbi.nlm.nih.gov/articles/PMC8621490/ である。

この総説には次の一文がある。

> "Therefore, environmental effect is cancelled to the first order with the ratio-based output."

「比による出力では環境の影響が一次の範囲で打ち消される」という言明が、2021年の総説において当然の前提として書かれている。総説という形式で「複数共鳴器を使う微小電気機械システムのセンサ」がひとまとまりの研究領域として整理されている事実そのものが、この設計が確立していることの証拠である。ただしこの総説の本文に "reference resonator" という語そのものは出現せず、差動構成やモード局在型の語彙で書かれている点は正確に述べておく。

### 3.2 水晶振動子の分野

- 著者は Marianna Magni、Diego Scaccabarozzi、Bortolino Saggin である。
- 題名は "Compensation of Thermal Gradients Effects on a Quartz Crystal Microbalance" である。
- 掲載は Sensors 誌の第23巻第1号、論文番号24であり、電子公開は2022年12月20日である。
- デジタルオブジェクト識別子は 10.3390/s23010024 である。
- 確認先は https://api.crossref.org/works/10.3390/s23010024 と https://pmc.ncbi.nlm.nih.gov/articles/PMC9824633/ である。

序論に次の記述がある。

> "Compensation of temperature effects based on the dual crystal configuration exploits the beating frequency of a reference crystal and the active one. The system is conceived to remove the effect of the average crystal temperature, assuming that both crystals have the same temperature, but the effect of temperature gradients is neglected."

基準用の水晶と実働の水晶を組み合わせる構成が、既知の標準的手法として紹介されており、この論文の新規性はその手法が温度勾配を無視している点を改良することにある。つまり2022年の時点では、基準素子との組み合わせ自体はすでに批判的検討の対象になる程度に古い。

### 3.3 表面弾性波デバイスの分野

第2節で確認した Wang ら（2014年）が、この分野における実装例そのものである。加えて、SmithとSenturiaが1995年に引用した Slobodnik ら（1981年）と Joshi（1982年）は、いずれも Ultrasonics Symposium における表面弾性波デバイスの温度補償の論文である。

なお、表面弾性波センサの総説として Mandal と Banerjee の "Surface Acoustic Wave (SAW) Sensors: Physics, Materials, and Applications"（Sensors, 22巻, 論文番号820, 2022年, デジタルオブジェクト識別子 10.3390/s22030820, 確認先 https://pmc.ncbi.nlm.nih.gov/articles/PMC8839725/ ）を当たったが、基準素子や二重遅延線による共通モード補償に触れた記述は見つからなかった。表面弾性波の分野で総説レベルの明示的な記述を押さえることは、今回の調査ではできなかった。

## 4. 判定

反例は正しい。

「既知の値を持つ基準素子を同じ物体に同居させ、比を取って共通モードの環境変動を一次の範囲で打ち消す」という設計は、遅くとも1981年から1995年の間に共鳴型センサの分野で標準的な構成として確立しており、1995年の時点で当事者自身が "conventional sensing setup" と書いている。2014年には表面弾性波共鳴器での実装例があり、2021年と2022年の総説および査読論文でも既知の手法として扱われている。したがって、この着想を一般的な形で「前例がない」と述べることはできない。

一方で、次の3点は反例によって否定されていない。

第一に、CipherFluteの基準素子は電子回路も電源も持たない受動的な共鳴管であり、読み取りは人間の呼気と携帯電話の内蔵マイクだけで行われる。挙げられた反例はいずれも発振回路と周波数カウンタを前提とする。

第二に、CipherFluteの基準素子は「センサの環境補償」ではなく「離散符号の復号における基準」として働く。打ち消す対象は温度だけでなく吹奏者の息の強さや個体差であり、出力は連続量の測定値ではなく離散スロットの番号である。この用途の違いは、評価指標が測定確度ではなく記号誤り率になる点に現れる。

第三に、造形物への情報埋め込みという文脈における前例の有無は、今回の調査では確定していない。参考として、受動音響で情報を担う3Dプリント造形物の代表例である Lamello（Savage、Head、Hartmann、Goldman、Mysore、Li、Proceedings of CHI 2015、著者公開版 https://people.eecs.berkeley.edu/~bjoern/papers/savage-lamello-chi2015.pdf ）の本文を全文抽出して調べたところ、"reference"、"calibration"、"temperature" のいずれの語も本文中に出現せず、既知周波数の基準要素を同時造形する設計は取られていなかった。ただしこれは1件の確認にすぎず、この文脈での網羅的な調査には至っていない。

## 5. 書き換え案

現在の論文本文（`paper/v11_text_dump.txt` の第163行から第167行、および貢献を列挙した第29行）では、基準笛について「通信で使われるパイロット信号と同じ発想であり」と既存概念への言及がすでに入っている。ここをさらに正確にするには、次の2点を直すとよい。

第一に、貢献の記述から「新しい」という含意を外し、既知の原理の移植であることを明示する。たとえば次のように書き換える。

> 第二に、共鳴型センサで確立している基準素子との比による共通モード補償の考え方を、電源も回路も持たない受動的な共鳴管の離散符号復号へ移し、温度と吹奏条件の変動下での記号誤り率を実測して有効性を示す。

第二に、3.3節の説明にひとこと出典を添える。たとえば次のように書く。

> この考え方自体は新しいものではなく、検出用の共鳴器と基準用の共鳴器を並べて比あるいは差で読むことで温度などの共通変動を打ち消す構成は、共鳴型センサの分野で古くから用いられてきた［Smith and Senturia 1995］。本研究の位置づけは、この原理を電子回路も電源も持たない受動的な共鳴管に移し、連続量の測定ではなく離散スロットの復号に用いた点にある。

このように書けば、査読者が反例を出したときに崩れる部分がなくなる。逆に「前例がない」と書き続けた場合、この分野を知る査読者からは高い確度で指摘を受ける。

## 6. 確認できなかったこと

- 出版社であるMDPIの論文ページ（https://www.mdpi.com/1424-8220/14/11/20702 ）は HTTP 403 で取得できなかったため、Crossref と PubMed Central を一次確認先として用いた。
- IEEE Xplore における Smith と Senturia の論文ページ本体は取得していない。書誌は Crossref の登録内容と、著者所属機関が公開している原稿本文で確定させた。
- 表面弾性波デバイスの分野について、基準素子との差または比による共通モード補償を「標準的手法」と明記した総説レベルの一次資料を見つけることはできなかった。個別論文と1981年および1982年の会議録の引用にとどまる。
- 造形物への情報埋め込みという文脈における基準素子の同時造形の前例について、網羅的な調査は行っていない。Lamello 1件を確認したのみである。
