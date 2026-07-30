# CipherFluteの符号設計と2枚1組の物理媒体についての原典確認（v4）

作成日は2026年7月30日である。担当は前段の網羅探索とは別の検証者である。対象は次の2点に絞ってある。第一は「隣り合う笛が同じ音にならない制約」の先例であり、Nick Goldmanらの2013年のNature論文と、記号の連続を禁じる制約符号の理論的な容量の上限である。第二は「2枚そろって初めて意味を持つ物理媒体」の先例であり、Moni NaorとAdi Shamirの視覚暗号、Yvo Desmedtらの音響暗号と光学暗号、大川直也と栃窪孝也の日本語論文、徳重佑樹らの日本語の研究会報告である。

作業の方法を先に述べる。前段の集約（`related_work_survey/00-digest.md`）と切り口ごとの生の記録（`related_work_survey/raw/10-codes-for-physical-media.md`、`raw/11-physical-security-steganography.md`、`raw/07-secret-backup-physical.md`）を読み、そこに書かれた主張を原典に当たって確かめた。取得はすべてコマンド行からの直接取得で行い、取得できた本文と抄録の該当箇所を逐語で引いてある。取得できなかったものは末尾の「確認できなかったこと」にまとめてある。

---

## 第1部　隣接同音禁止の先例

### 1.1 Goldmanらの2013年のNature論文の書誌

- 題名は Towards practical, high-capacity, low-maintenance information storage in synthesized DNA である。
- 著者は Nick Goldman, Paul Bertone, Siyuan Chen, Christophe Dessimoz, Emily M. LeProust, Botond Sipos, Ewan Birney である。
- 掲載は Nature 第494巻 第7435号 77ページから80ページ、2013年である。DOIは 10.1038/nature11875 である。
- 確認先は https://pmc.ncbi.nlm.nih.gov/articles/PMC3672958/ （PubMed Centralに置かれた著者原稿の全文）である。

書誌についてひとつ注意を書く。依頼文が挙げていた題名「Toward practical high-capacity low-maintenance storage of digital information in synthesised DNA」は、PubMed Centralに置かれた著者原稿の題名である。同じページが「Nature. Author manuscript」と明記し、あわせて「Published in final edited form as: Nature. 2013 Jan 23;494(7435):77-80」と併記している。Nature誌に載った確定版の題名は上に記したほうである。前段の記録（`raw/10-codes-for-physical-media.md`）はこの点をすでに訂正済みであり、その訂正は正しい。論文で引くときは確定版の題名を使うのが安全である。

### 1.2 前段の報告の主張は原典で裏が取れた

前段の担当者は「バイト列を三進の桁へ変換し、各桁を直前に使った塩基とは異なる三塩基のいずれかへ写すことで同一記号の連続を構造的に排除している。記号数を4から実効3へ落とす数え方まで一致する」と報告した。この報告は原典の本文で裏が取れた。以下に根拠を逐語で引く。

図1の説明文が符号化の全体を述べている。原文は次のとおりである。

> Digital information (a, in blue), here binary digits holding the ASCII codes for part of Shakespeare's sonnet 18, was converted to base-3 (b, red) using a Huffman code that replaces each byte with five or six base-3 digits (trits). This in turn was converted in silico to our DNA code (c, green) by replacement of each trit with one of the three nucleotides different from the previous one used, ensuring no homopolymers were generated. This formed the basis for a large number of overlapping segments of length 100 bases with overlap of 75 bases, creating fourfold redundancy

本文はホモポリマーの定義とそれを避ける理由を次のように書いている。

> The bytes comprising each file were represented as single DNA sequences with no homopolymers (runs of ≥ 2 identical bases, which are associated with higher error rates in existing high-throughput sequencing technologies and led to errors in Church et al.'s experiment)

規模と復元の成否については次のとおりである。

> giving a total of 757,051 bytes (Shannon information 5.2 × 10^6 bits)

> the five files were represented by a total of 153,335 strings of DNA, each comprising 117 nt

> reconstructed the original files with 100% accuracy

断片ごとの層構造についても記述がある。

> Each segment was then augmented with indexing information that permitted determination of the file from which it originated and its location within that file, and simple parity-check error-detection

したがって前段の3つの主張はいずれも成り立つ。第一に、バイト列を三進の桁へ変換している（ハフマン符号を用い、1バイトを5桁または6桁の三進の桁に置き換えている）。第二に、各桁を「直前に使った塩基とは異なる三種類の塩基」のいずれかへ写している。第三に、その帰結として「2個以上の同一塩基の連続」が構造的に生じない。そして四塩基のうち直前の1個を除いた三塩基から選ぶという数え方は、CipherFluteが13スロットから直前の1個を除いた12通りから選ぶという数え方とまったく同じである。「記号数を4から実効3へ落とす数え方まで一致する」という前段の判定は正しい。

### 1.3 ただし制約を課す動機はGoldmanらとCipherFluteで違う

原典を読んで分かった重要な点を書き添える。Goldmanらが同一塩基の連続を避ける理由は、上に引いたとおり「既存の高速並列読み取り技術では誤り率が高くなる」ためである。すなわち動機は誤り率の低減である。いっぽうCipherFluteが隣接同音を禁じる理由は、息を切らずに続けて吹いたときに音の変化そのものを記号の切れ目として使うためであり、動機は同期（区切りの検出）である。

この違いは論文の書き方に影響する。同期を目的として記号の並びを制限するという考え方は、磁気記録と光記録のランレングス制限符号、および8B/10B符号の側の伝統である。機構としてはGoldmanらのほうが近く、動機としては8B/10B符号とランレングス制限符号のほうが近い。前段の記録は「機構として最も近い実例は磁気記録ではなくDNA保存である」と書いており、機構に限れば正しい。ただし「8B/10Bよりも近い先例」と一言で片づけると動機の違いを落とすことになるので、論文では両方を引いて「機構はDNA保存の側、目的は自己同期の側」と書き分けるのが正確である。

なお8B/10B符号は隣接する同一記号を禁じていない。二進の記号列に対して連の長さの上限とおおよその直流成分の釣り合いを課す符号である。二進では「隣接する記号を必ず変える」という制約を課すと記号列が交互に並ぶだけになり、運べる情報が0になる（次節の式で言えば底2の対数の1が0である）。この制約が実用になるのは記号の種類が3以上のときだけであり、CipherFluteが音高を語彙にして13種類まで広げているからこそ支払える制約である。この点は論文で述べる価値がある。

---

## 第2部　同じ記号を続けない制約のもとでの容量の上限

依頼にあった「同じ記号を続けない制約のもとで1記号あたり何ビット運べるか」について、一次資料を4件押さえた。結論を先に書く。**記号の種類がq個あり、隣り合う記号が同じにならないという制約だけを課したとき、1記号あたり運べる情報の上限は底2の対数の (q − 1) ビットである。** さらに、CipherFluteが採っている差分の写像（直前の記号を除いた q − 1 通りから選ぶ）は、この上限をちょうど達成しており、符号としての無駄が一切ない。以下に根拠を示す。

### 2.1 Shannonの1948年の論文（容量の定義と一般公式）

- 題名は A Mathematical Theory of Communication である。著者は C. E. Shannon である。
- 掲載は The Bell System Technical Journal 第27巻 379ページから423ページおよび623ページから656ページ、1948年7月および10月である。
- 確認先は https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf である。この版は冒頭に「Reprinted with corrections from The Bell System Technical Journal, Vol. 27, pp. 379-423, 623-656, July, October, 1948.」と記した完全な再録である。

第1節「The Discrete Noiseless Channel」に、記号の並びに制限がある場合の容量の定義と一般公式がある。定義は次のとおりである。

> Definition: The capacity C of a discrete channel is given by C = lim_{T tends to infinity} log N_T / T where N_T is the number of allowed signals of duration T.

一般公式は同節の定理1である。原文は次のとおりである。

> Theorem 1: Let b_ij^(s) be the duration of the sth symbol which is allowable in state i and leads to state j. Then the channel capacity C is equal to log W where W is the largest real root of the determinant equation: |Σ_s W^(−b_ij^(s)) − δ_ij| = 0

同節はこの枠組みが状態遷移で書ける制限に一般に使えることを明言している。原文は「A very general type of restriction which may be placed on allowed sequences is the following: We imagine a number of possible states a_1, a_2, …, a_m. For each state only certain symbols from the set S_1, …, S_n can be transmitted (different subsets for the different states).」である。CipherFluteの隣接同音禁止はまさにこの形の制限であり、状態は「直前に鳴らした音」で、各状態から出られる記号は「その音以外の q − 1 個」である。すべての記号の長さを1とおくと定理1の行列式は W = q − 1 を最大の実根に持ち、容量は底2の対数の (q − 1) になる。

### 2.2 Marcus、Roth、Siegelの教科書（代数的な特徴づけ）

- 題名は An Introduction to Coding for Constrained Systems である。
- 著者は Brian H. Marcus（IBM Research Division, Almaden Research Center）、Ron M. Roth（Technion）、Paul H. Siegel（University of California at San Diego）である。
- 版は Fifth Edition (October 2001) である。
- 確認先は https://personal.math.ubc.ca/~marcus/Handbook/ である（表紙、目次、第3章の各PDFを直接取得して読んだ）。表紙の記載を画像から読み取って題名、著者、版、日付を確定した。

第3章の題名は Capacity である。3.1節「Combinatorial characterization of capacity」の定義は次のとおりである。

> Let S be a constrained system over an alphabet Σ and denote by N(ℓ; S) the number of words of length ℓ in S. The base-2 Shannon capacity, or simply capacity of S, is defined by cap(S) = limsup_{ell tends to infinity} (1/ℓ) log N(ℓ; S).

3.2節「Algebraic characterization of capacity」の定理3.4が計算法を与える。原文は次のとおりである（72ページ）。

> Theorem 3.4 Let S be an irreducible constrained system and let G be an irreducible lossless (in particular, deterministic) presentation of S. Then, cap(S) = log λ(A_G).

ここで λ(A_G) は隣接行列のスペクトル半径である。CipherFluteの制約を表す図はq個の状態を持ち、状態iから状態j（jはiと異なる）へ記号jのラベルの辺が1本ずつ出る。この図は既約かつ決定的であり、隣接行列は全成分1の行列から単位行列を引いたものである。その最大固有値は q − 1 であるから、容量は底2の対数の (q − 1) である。私の計算でもq = 4、11、12、13について最大固有値が3、10、11、12になることを数値で確かめた。

同じ第3章の冒頭が、容量が符号化率の上限であることを明言している。原文は次のとおりである。

> In the context of coding, the significance of capacity will be made apparent in Chapter 4, where we show that it sets an (attainable) upper bound on the rate of any finite-state encoder for a given constrained system.

これが「これより上はない」という根拠になる。

### 2.3 ImminkとCaiの論文（q個の記号について明示の数式と数値）

- 題名は Properties and Constructions of Constrained Codes for DNA-Based Data Storage である。
- 著者は Kees A. Schouhamer Immink（Turing Machines Inc, Rotterdam）と Kui Cai（Singapore University of Technology and Design）である。
- 掲載は IEEE Access 第8巻 49523ページから49531ページ、2020年である。DOIは 10.1109/ACCESS.2020.2980036 であり、Crossrefの登録でCreative Commons Attribution 4.0の利用許諾が付いていることを確認した。
- 私が読んだのは著者が公開している査読前の版である。arXiv:1812.06798v1、2018年12月14日、題名は Properties and constructions of constrained codes for DNA-based data storage、確認先は https://arxiv.org/pdf/1812.06798 である。IEEE Xploreの確定版のPDFは取得に失敗した（HTTP 502）。書誌はCrossrefとDBLPで照合した（https://api.crossref.org/works/10.1109/ACCESS.2020.2980036 、https://dblp.org/search/publ/api?q=constrained+codes+DNA+Immink&format=json ）。

この論文の第4節が、まさに必要な数式を与えている。連の長さの上限をm、記号の種類をqとおくと、定理2が長さnの許される語の個数 N_q(m, n) を母関数で与え、式(19)と式(20)が容量を与える。原文は次のとおりである。

> For asymptotically large codeword length n, the maximum number of (binary) user bits that can be stored per q-ary symbol, called (information) capacity, denoted by C_q(m), is given by C_q(m) = lim_{n tends to infinity} (1/n) log_2 N_q(m, n) = log_2 λ_q(m), where λ_q(m), is the largest real root of the characteristic equation x^(m+1) − q x^m + q − 1 = 0.

隣接する同一記号を禁じる制約は m = 1 の場合である。このとき特性方程式は x^2 − q x + q − 1 = 0 となり、因数分解すると (x − 1)(x − (q − 1)) = 0 であるから最大の実根は q − 1 である。したがって容量は底2の対数の (q − 1) である。

同論文の表1（TABLE I）はq = 4の場合の数値を載せており、m = 1 の欄に「1.5850(= log2 3)」と明記してある。さらに本文は有限の長さについての厳密な個数も書いている。原文は次のとおりである。

> For m = 1, we simply find N4(1, n) = 4·3^(n−1).

一般のqに書き直すと N_q(1, n) = q (q − 1)^(n−1) である。これは初等的な数え上げ（1番目の記号がq通り、2番目以降がそれぞれ q − 1 通り）と一致する。

### 2.4 McLaughlin、Luo、Xieの論文（q個の記号のランレングス制限符号の容量）

- 題名は On the capacity of M-ary runlength-limited codes である。
- 著者は Steven W. McLaughlin, Jian Luo, Qun Xie である。
- 掲載は IEEE Transactions on Information Theory 第41巻 第5号 1508ページから1511ページ、1995年9月である。DOIは 10.1109/18.412712 である。
- 確認先は https://dblp.org/search/publ/api?q=Capacity+of+M-ary+Runlength-Limited+Codes&format=json および https://api.semanticscholar.org/graph/v1/paper/DOI:10.1109/18.412712 である。書誌は両方で一致した。本文と抄録は出版社が閉じており取得できなかった（Semantic Scholarの応答が「the following paper fields have been elided by the publisher: {'abstract'}」と明記している）。

ImminkとCaiは上記の特性方程式の出所としてShannonの1948年の論文とこの論文の2件を挙げている。ひとつ注意を書くと、ImminkとCaiの参考文献欄は第1著者の姓を「MacLauhlin」と誤記している。正しくは McLaughlin である。DBLPとSemantic Scholarの双方で確かめた。

### 2.5 CipherFluteへの当てはめ

以上を合わせると、CipherFluteの13スロットのうち隣接同音を禁じて実効12通りに落とす扱いについて、次のことが言える。

第一に、**1本あたり運べる量は底2の対数の12、すなわち約3.585ビットが上限であり、これより上はない。** CipherFluteが用いている差分の写像（直前の音に1を足したうえでデータの桁を足し、記号の個数で割った余りを取る形）は、この上限をちょうど達成する。理由を述べる。長さnの許される音列の総数は厳密に 13 × 12^(n−1) であり、差分の写像は「1番目の音が13通り、2番目以降がそれぞれ12通り」という選び方と1対1に対応するので、余分な冗長が一切ない。すなわち有限の長さでも最適である。前段の記録が「13から実効12へ落とすことによる損失（1本あたり約0.115ビット）が理論的に最適かどうか」を未解決の課題として挙げていたが、答えは「最適である」であり、しかも損失は符号化の下手さによるものではなく制約そのものの値段である。

第二に、その値段は次のとおりである。数値は私が計算したものであり、上に挙げた式から直接出る。

| 記号の種類 | 制約なしの1本あたり（ビット） | 隣接同音禁止のもとでの1本あたり（ビット） | 差（ビット） | 率の損失 |
|---|---|---|---|---|
| 2 | 1.0000 | 0.0000 | 1.0000 | 100.00パーセント |
| 4（DNAの場合） | 2.0000 | 1.5850 | 0.4150 | 20.75パーセント |
| 11 | 3.4594 | 3.3219 | 0.1375 | 3.97パーセント |
| 12 | 3.5850 | 3.4594 | 0.1255 | 3.50パーセント |
| 13 | 3.7004 | 3.5850 | 0.1155 | 3.12パーセント |

第三に、この表から出るいちばん使える言い方を書く。**隣接同音を禁じたq種類の記号は、制約のない q − 1 種類の記号とちょうど同じ量を運ぶ。** したがって「音域を半音1つ広げれば、隣接同音禁止は容量の代償なしに手に入る」という設計判断は、思いつきではなく情報理論の等式である。既存のメモ（`ai-fue-norepeat-12slot`）が12スロットにすると11がちょうど素数になってリード・ソロモン符号の体がそのまま使えるので「代償は容量ではなく音域を半音1つ広げることだけである」と書いているのは、この等式に完全に一致する。論文でこの点を上の一次資料つきで書けば、符号設計の節はかなり強くなる。

第四に、上限を超える方法はひとつしかない。それは「記号の切れ目を音の変化以外の手がかりで見つける」ことである。無音を置いて区切る方式（既存のメモ `ai-fue-silence-segmentation` にある無音区切りの自動送り）を採れば制約は不要になり、1本あたり底2の対数の13、すなわち約3.700ビットまで使える。すなわち隣接同音禁止は「約3.1パーセントの容量を払って、無音を置く時間と無音検出の信頼性を買う」取引である。この取引の是非は容量の理論では決まらず、読み出しの実際で決まる。

### 2.6 制約そのものを課すべきかを問う反対材料

制約と誤り訂正のどちらに資源を割くべきかを正面から扱った論文がある。前段の記録が挙げていたもので、私も抄録を原典で確認した。

- 題名は Embracing Errors Is More Efficient Than Avoiding Them Through Constrained Coding for DNA Data Storage である。
- 著者は Franziska Weindel, Andreas L. Gimpel, Robert N. Grass, Reinhard Heckel である。
- arXiv:2308.05952、2023年8月11日投稿、2024年6月26日改訂である。確認先は https://export.arxiv.org/api/query?id_list=2308.05952 である。学術誌への掲載情報はarXivの登録に入っていない。

抄録の要点を逐語で引く。

> However, constrained coding comes at the cost of an increase in redundancy. An alternative is to control errors by randomizing the sequences, embracing errors, and paying for them with additional coding redundancy. In this paper, we determine the error regimes in which embracing substitutions is more efficient than constrained coding for DNA data storage. Our results suggest that constrained coding for substitution errors is inefficient for existing DNA data storage systems.

この論文の結論はCipherFluteにそのまま当てはまらない。理由は、この論文が扱っているのは「制約を破ると置換誤りが増える」という誤り率の問題であって、CipherFluteの隣接同音禁止が解いているのは「制約を破ると記号の切れ目が見えなくなる」という同期の問題だからである。同期が壊れると記号の個数そのものが変わるので、誤り訂正符号の冗長では原理的に払えない。査読者から「制約と誤り訂正を両方入れるのは無駄ではないか」と問われたときは、この区別（誤り率の話ではなく同期の話である）で答えるのが筋である。

---

## 第3部　2枚そろって初めて意味を持つ物理媒体の先例

### 3.1 NaorとShamirの視覚暗号

- 題名は Visual Cryptography である。著者は Moni Naor と Adi Shamir である。
- 掲載は Advances in Cryptology — EUROCRYPT '94、Lecture Notes in Computer Science 第950巻、1ページから12ページ、1995年である。DOIは 10.1007/BFb0053419 である。会議は1994年、Springerによる予稿集の刊行は1995年であるから、引くときは書き分けるのが安全である。
- 確認先は次の3つである。第一に著者本人が公開している全文（https://www.wisdom.weizmann.ac.il/~naor/PAPERS/vis.pdf 、著者の業績一覧 https://www.wisdom.weizmann.ac.il/~naor/onpub.html から辿った）。第二に出版社の章のページ（https://link.springer.com/chapter/10.1007/BFb0053419 、ここで叢書名がLecture Notes in Computer Scienceの第950巻であることを確認した）。第三に大川と栃窪の論文の参考文献欄（後述、そこでも「Lecture Notes in Computer Science, Vol.950, pp.1-12 (1995)」と書かれている）。

前段の記録は「EUROCRYPT '94の予稿集のLecture Notes in Computer Scienceの巻番号を確定できなかった」と書いていた。**第950巻である。**出版社の章のページの記載「Part of the book series: Lecture Notes in Computer Science ((LNCS, volume 950))」と、大川と栃窪の論文の参考文献[2]の記載が一致した。この未確認事項は解消できた。

「計算機を使わずに人間の感覚器だけで復号する」という性質について、この論文がどこまで主張しているかを逐語で確定する。抄録は次のとおりである。

> In this paper we consider a new type of cryptographic scheme, which can decode concealed images without any cryptographic computations. The scheme is perfectly secure and very easy to implement. We extend it into a visual variant of the k out of n secret sharing problem, in which a dealer provides a transparency to each one of the n users; any k of them can see the image by stacking their transparencies, but any k−1 of them gain no information about it.

本文の導入はさらに強く述べている。

> In this paper we consider the problem of encrypting written material (printed text, handwritten notes, pictures, etc.) in a perfectly secure way which can be decoded directly by the human visual system.

> The original cleartext is revealed by placing the transparency with the key over the page with the ciphertext, even though each one of them is indistinguishable from random noise.

> Due to its simplicity, the system can be used by anyone without any knowledge of cryptography and without performing any cryptographic computations.

閾値2の場合が原型であることも明記してある。

> The original encryption problem can be considered as a 2 out of 2 secret sharing problem.

つまりこの論文は、（1）計算をまったく行わずに復号できること、（2）復号を行うのは人間の視覚系そのものであること、（3）情報理論的に完全に安全であること、（4）1枚だけを見ても乱雑な模様と区別がつかないこと、（5）閾値2の場合が原型であること、をすべて明示して主張している。CipherFluteの「2枚そろって初めてハートが現れるカード」が主張しようとしている性質のうち、（3）（4）（5）はここで完全に先取りされている。

なお復号の演算については差がある。透明シートを重ねる操作は黒画素の論理和であり、この論文の模型もそう定義している（原文は「we see a combined share whose black subpixels are represented by the Boolean "or" of rows i_1, i_2, …, i_r in S」である）。論理和であるため元の白黒の対比は必ず落ちる。CipherFluteのカードは記号の加減算による一度限りの鍵の方式であって、対比の劣化はない。ただしこれは実装の質の差であって、枠組みの新しさではない。

### 3.2 Desmedt、Hou、Quisquaterの音響暗号と光学暗号

- 題名は Audio and Optical Cryptography である。著者は Yvo Desmedt, Shuang Hou, Jean-Jacques Quisquater である。
- 掲載は Advances in Cryptology — ASIACRYPT'98、Lecture Notes in Computer Science 第1514巻、392ページから404ページ、1998年である。DOIは 10.1007/3-540-49649-1_31 である。
- 確認先は https://link.springer.com/chapter/10.1007/3-540-49649-1_31 である。題名、著者3名、収録書名、ページ、刊行年、叢書の巻番号（第1514巻）、および抄録の全文をここで確認した。本文は有料であり取得できなかった。

抄録の全文を引く。

> In visual cryptography the additive property of light is used. Also the shares are random and therefore suspect to a censor. In this paper we present two new cryptographic schemes which use music and the wave properties of light. Both schemes are also secret sharing schemes in which shares are music or images and are not suspect to a human censor. Our scheme guarantees perfect privacy as well as high quality. To decrypt the message, one just plays two shares on a stereo system. There are two decryption methods which are either based on the interference property of sound or based on the stereo perception of the human hearing system. In optical cryptography, we use pictures as covers and the wave interference property of light. The privacy is perfect and the modified images are non-suspicious. The Mach-Zehnder interferometer is used as the decryption machine.

ここから「計算機を使わず人間の感覚器だけで復号する」という性質の主張の範囲を確定する。音響の側について、この論文は「2つのシェアをステレオ装置で再生するだけである」と述べており、復号の仕組みは音の干渉、あるいは人間の聴覚の左右の知覚のどちらかである。したがって暗号学的な計算は不要であるが、再生装置は必要である。光の側については「マッハ・ツェンダー干渉計を復号の装置として用いる」と明記しており、これは装置である。すなわちこの論文は「計算機なしに復号できる」とは主張しているが、「装置なしに人間の感覚器だけで復号できる」とは主張していない。前段の記録の「計算機なしに人間の感覚器だけで復号できる点が要点である」という書き方は、視覚暗号については正しく、この音響暗号と光学暗号については言いすぎである。

もうひとつ重要な点を書く。この論文は偽装を設計目標として明示している。抄録の「Also the shares are random and therefore suspect to a censor」および「shares are music or images and are not suspect to a human censor」が根拠である。すなわち「秘密分散のシェアを、検閲者に怪しまれない見た目や音にする」という発想は1998年の時点で設計目標として掲げられていた。CipherFluteが「日用品への偽装による探索コストの引き上げ」を新規性の柱に置くなら、この論文が先例であることを認めた上で差分を述べる必要がある。

### 3.3 Desmedt、Le、Quisquaterの非二値の音響暗号

- 題名は Nonbinary Audio Cryptography である。著者は Yvo Desmedt, Tri V. Le, Jean-Jacques Quisquater である。
- 掲載は Information Hiding（第3回Information Hidingワークショップの予稿集）、Lecture Notes in Computer Science 第1768巻、478ページから489ページ、2000年刊である。DOIは 10.1007/10719724_33 である。
- 確認先は https://link.springer.com/chapter/10.1007/10719724_33 である。題名、著者3名、収録書名、ページ、刊行年（2000年）、叢書の巻番号（第1768巻）、および抄録の全文をここで確認した。

会議名について注意を書く。依頼文は「Information Hiding 2000」と書いていたが、この会議は1999年9月29日から10月1日にドイツのドレスデンで開かれた第3回Information Hidingワークショップであり、その予稿集がLecture Notes in Computer Science 第1768巻として2000年に刊行されたものである。出版社の章のページの会議名は「International Workshop on Information Hiding」であり、刊行年は2000年である。会議年と刊行年が1年ずれるので、引くときは取り違えないほうがよい。前段の記録はこの点をすでに訂正済みであり、その訂正は正しい。

抄録の全文を引く。

> Visual cryptography, introduced by Naor-Shamir at Eurocrypt '94, only requires primitive technology to decrypt the ciphertext. However, a disadvantage of it is that the "ciphertext", as a random looking transparency, is suspicious to a censor. The solutions recently proposed by Desmedt-Hou-Quisquater to avoid these problems are neither user friendly, having a low bandwidth, nor are tested. In this paper we present three schemes that overcome these problems. As in one of the Desmedt-Hou-Quisquater's schemes, a share (or a ciphertext) corresponds to an audio signal, such as music. While in the Desmedt-Hou-Quisquater scheme the plaintext was binary, in our schemes the plaintext can also be speech, or any other audio signal. By introducing variations of the one-time pad we guarantee perfect secrecy. The ciphertext is non-suspicious, when tested with human ears, is indistinguishable from normal music.

この抄録から2つのことが分かる。第一に、視覚暗号の復号について「only requires primitive technology」という言い方をしており、これも「装置がまったく不要」とは言っていない。第二に、1998年のDesmedtらの方式を自分たちが「使いやすくなく、帯域が低く、しかも試験されていない」と評している。すなわち音響暗号の系譜は1998年の時点では実機での検証を伴っていなかった。CipherFluteが実機で通したことを主張するときに使える対比である。

### 3.4 大川直也と栃窪孝也の視覚復号型秘密分散によるパスワードの分散管理

- 題名は「視覚復号型秘密分散法を用いたパスワードの分散管理の提案」である。英語題名は Visual Secret Sharing Schemes for Passwords である。
- 著者は大川直也（日本大学大学院生産工学研究科数理情報工学専攻）と栃窪孝也（日本大学生産工学部数理情報工学科）である。
- 掲載は情報処理学会論文誌デジタルプラクティス 第7巻 第2号 35ページから50ページ、2026年4月15日発行である。ISSNは 2435-6484 である。受付日は2025年6月22日、採録日は2026年1月13日である。
- 確認先は情報処理学会電子図書館の当該レコード（https://ipsj.ixsq.nii.ac.jp/records/2009100 ）と、そこから取得した本文のPDF（https://ipsj.ixsq.nii.ac.jp/record/2009100/files/IPSJ-TDP0702007.pdf 、全16ページ）である。本文は誌面の画像として読んだ。

日本語の概要は次のとおりである（1ページから引く）。

> 現在の認証システムではパスワードが広く使われている．一方，指紋などのバイオメトリクスを使用するシステムも幅広く利用されているが，バイオメトリクスが使用できない場合はパスワードを使用するものが多くパスワードの管理は非常に重要な問題となっている．また，複数のパスワードを管理するパスワード管理ツールが広く普及しているが，これらのツールにおいても「マスターパスワード」と呼ばれるパスワードの管理が必要となる．一般に，秘密情報の分散管理には秘密分散法が非常に有効であり，秘密分散法を画像に応用した視覚復号型秘密分散法では秘密情報の復元時に複雑な計算なしに画像を重ね合わせることのみで秘密情報を復元できるという特徴がある．本研究では，OHPシートやスマートフォンを利用した視覚復号型秘密分散法によるパスワードの分散管理手法を提案し，その実現可能性を評価する．

提案手法の中身は3.1節にある。逐語で引く。

> 提案手法では，パスワードを（2, 2）しきい値視覚復号型秘密分散法で分散し，シェア画像の1枚は紙に印刷して職場や家に保管し，もう一方のシェア画像はOHPシートやスマートフォンなどで保管して分散管理する．そして，紙に印刷しているシェア画像とOHPシートやスマートフォンなどで保管しているシェア画像を重ねて復元したパスワードを利用することでパスワードを安全に管理することができる．

> 従来手法では，パスワードの復元が文字単位で行われるのに対し，提案手法では，パスワード全体を1度に復元できる点が特徴である．

評価と今後の課題は6節（49ページ）にある。5節で30代から50代の社会人と大学生を対象とした簡易的な評価を行っていることと、「複数の場所でパスワードを復元して利用することが想定されるため、家と会社の両方でシェア画像を保管することができるように現状の（2, 2）しきい値視覚復号型秘密分散法から発展させ、（2, 3）しきい値視覚復号型秘密分散法を実装することもまた今後の課題である」と述べていることを確認した。

「計算機を使わず人間の感覚器だけで復号する」という性質の主張の範囲を確定する。この論文が主張しているのは「複雑な計算なしに画像を重ね合わせることのみで」復元できることである（英語の抄録は「by simply superimposing images without complicated calculations」である）。「計算機なしに」とは書いていないが、実際の手順は紙に印刷したシェアとOHPシートを重ねて人が読むだけであり、装置も計算もいらない。スマートフォンは「シェア画像を保管する」および表示する媒体として使われるだけであって、復元の計算には関わらない。したがって**復号に一切の計算装置を要さないという点で、この論文はCipherFluteより徹底している。**

これは前段の記録が「脅威の度合いは中」としていたが、私の判断ではもう少し重い。2026年4月に日本語の査読誌に載った、しかも「物理的な2枚1組でパスワードを守る」というCipherFluteのカード実装と用途がほとんど同じ論文であり、WISS 2026の日本の査読者が知っている可能性が高い。引用しないという選択は取れない。

### 3.5 徳重らの音響秘密分散は前段の報告が2か所で間違っていた

- 題名は「物理的復元が容易な音響秘密分散法」である。英語題名は An Audio Secret Sharing Scheme Easy to Reproduce Secret Physically である。
- **著者は6名である。**徳重佑樹、三澤裕人、吉田文晶、上床昌也、岩本貢、太田和夫であり、全員が電気通信大学（大学院情報理工学研究科）である。発表者は吉田文晶である。
- 掲載は電子情報通信学会技術研究報告（信学技報）第115巻 第38号、資料番号は IT2015-14 および EMM2015-14、75ページから80ページ、発行日は2015年5月14日である。ISSNは印刷版が 0913-5685、オンライン版が 2432-6380 である。
- 研究会はマルチメディア情報ハイディング・エンリッチメント研究会と情報理論研究会の共催であり、開催期間は2015年5月21日から22日、開催地は京都市国際交流会館、講演は2015年5月22日13時40分である。
- 確認先は電子情報通信学会の講演論文の公式ページ（https://ken.ieice.org/ken/paper/20150522IbAn/ ）である。ここで題名、著者6名、所属、資料番号、巻号、ページ、発行日、研究会、開催地、日本語と英語の抄録の全文を確認した。書誌はCiNii Research（https://cir.nii.ac.jp/crid/1520572358843442048 ）、国立国会図書館サーチ（https://ndlsearch.ndl.go.jp/api/opensearch?any=物理的復元が容易な音響秘密分散法 ）、J-GLOBAL（https://jglobal.jst.go.jp/detail?JGLOBAL_ID=201502205393039990 ）でも照合した。

前段の報告に対して2つの訂正を書く。

**訂正1。著者は3名ではなく6名である。**前段の記録（`raw/11-physical-security-steganography.md` および `00-digest.md`）は「徳重佑樹, 三澤裕人, 吉田文晶」の3名と書いている。これはCiNii Researchの書誌が3名しか登録していないためである。電子情報通信学会の公式ページとJ-GLOBALはいずれも6名を挙げており、うしろの3名（上床昌也、岩本貢、太田和夫）が落ちている。岩本貢と太田和夫は電気通信大学の暗号研究の主要な研究者であり、この2名を落として引用すると日本の査読者には不自然に見える。必ず6名で引くべきである。

**訂正2。この論文は復号に波の干渉を用いない。**前段の記録は「徳重らは波の干渉と周波数分割を用いて『物理的な復元が容易な』音響秘密分散を提案している」と書いている。これは逆である。日本語の著者抄録を逐語で引く。

> 音響特性を利用した秘密分散法である，音響秘密分散法の既存研究の多くは，完全秘匿を達成する一方で，実際の空間上での物理的な復元が困難であるという問題がある．これは，復号に音の干渉を用いたためであり，これによってシェア音声の時間的・空間的なずれが殆ど許容できないことに起因する．我々は完全秘匿を達成することを目的とせず，復号者の聴覚能力で秘密音源の情報が理解できないことを規準とした新たな安全性を定義し，そのもとで，復号に波の干渉を用いない，新しい音響秘密分散法を提案する．提案手法は，音声データを一定の周波数帯で分割し，一定時間ごとにシェアに含まれる周波数をランダムに変化させ，各シェアに含まれる情報量を平均化することにより実現される．実験により，我々の提案する安全性を満たし，物理的な復元が容易な音響秘密分散法が実際に実現可能であることを示す．

英語の抄録も同じことを述べている。

> In previous work on audio secret sharing schemes, it is hard to reproduce the secret in physical space whereas they can achieve perfect secrecy. This drawback is due to the requirement that sound wave interference is necessary to be realized with high accuracy. In this paper, we introduce a new security criteria such that it is considered to be secure if secret information cannot be recognized by human acoustic sense. Under our new security criteria, we propose a new method of audio secret sharing schemes which does not use wave interference but is based on frequency dividing.

前段の誤りの原因は、CiNii Researchのキーワード欄に「波の干渉」が挙がっていることである。この語は既存研究の問題点として本文に出てくるものであって、提案手法が用いる仕組みではない。なお電子情報通信学会の公式ページのキーワード欄も第4項を「周波数分割 / wave interference」と対訳を誤っている。学会側の登録の誤りであり、これに引きずられないほうがよい。

内容の要点を3つ書く。第一に、Desmedtらの系譜が達成していた完全秘匿を、この論文は意図的に捨てている。安全性の基準を「復号者の聴覚能力で秘密音源の情報が理解できないこと」に置き換えている。第二に、復号に波の干渉を使わず、音声を周波数帯に分けて一定時間ごとにシェアに含まれる周波数を乱数で入れ替える方式を採っている。第三に、実験で物理空間での復元の容易さを示している。

CipherFluteとの関係で言うと、この論文は音響秘密分散を「実空間で本当に復元できるようにする」ために情報理論的な安全性を捨てた研究である。CipherFluteはちょうど逆の取引をしている。すなわち、2枚1組のカードでは情報理論的な安全性（片方だけでは一様な乱数にしか見えない）を保ったまま、復号にスマートフォンという計算装置を要求している。この対比は論文の関連研究の節で書く価値がある。

### 3.6 「計算機を使わず人間の感覚器だけで復号する」という性質の主張の範囲

依頼のうち、この性質がどこまで主張されているかについての答えをまとめる。数値と引用はすべて前の各節に示した原典の記述に基づく。

| 文献 | 復号を行うもの | 必要な装置 | 安全性の主張 | 実機での検証 |
|---|---|---|---|---|
| NaorとShamir 1994年 | 人間の視覚系 | 不要（透明シートを重ねるだけである） | 完全に安全である | 論文末に実物の点模様を添付している |
| Desmedt、Hou、Quisquater 1998年（音響） | 音の干渉、または人間の聴覚の左右の知覚 | ステレオの再生装置が必要である | 完全な秘匿を保証すると述べている | 1999年の続報が「試験されていない」と述べている |
| Desmedt、Hou、Quisquater 1998年（光学） | 光の波の干渉 | マッハ・ツェンダー干渉計が必要である | 完全であると述べている | 同上 |
| Desmedt、Le、Quisquater 2000年 | 人間の聴覚 | 再生装置が必要である | 一度限りの鍵の変形で完全秘匿を保証すると述べている | 人間の耳で試験したと述べている |
| 大川と栃窪 2026年 | 人間の視覚系 | 不要（紙とOHPシートを重ねるだけである） | 視覚復号型秘密分散法に負わせている | 社会人と大学生を対象とした評価を行っている |
| 徳重ら 2015年 | 人間の聴覚 | 再生装置が必要である | 完全秘匿を捨て、聴覚で理解できないことを基準に置き換えている | 実験を行っている |
| CipherFluteのカード | スマートフォンの読み出しアプリ | マイクと計算装置が必要である | 2-of-2の秘密分散に負わせている | 2026年7月に実機で確認している |

この表からはっきり言えることは、**「計算機を使わずに人間の感覚器だけで復号する」という性質を最も強く主張しているのは視覚の側（NaorとShamir、および大川と栃窪）であり、CipherFluteはこの軸では最も弱い**ということである。CipherFluteは復号に必ずスマートフォンと専用のアプリを要する。論文で「電源不要」を売り込むときは、電源が不要なのは記憶媒体の側だけであり、読み出しの側は装置に依存すると明記しなければならない。前段の記録がcodex32との対比で同じ指摘をしていたが、視覚暗号の系譜に対しても同じ指摘が当てはまる。

### 3.7 派生して見つかった国内の関連研究

調査の途中で、国内に音響秘密分散の系譜がもう少し広く存在することが分かった。書誌はCiNii Researchの検索応答（https://cir.nii.ac.jp/opensearch/all?q=音響秘密分散&format=json&count=50 、総件数6件）で確認した。抄録と本文には当たっていないので、内容は題名から読めるところまでしか書かない。

- 藤田倫弘「1ビットオーディオを対象とした音響秘密分散法の提案」日本音響学会講演論文集 2004年、578ページ。
- 藤田倫弘、西村竜一、鈴木陽一「1ビットオーディオ音響秘密分散法における分散情報の有意味音化」電子情報通信学会技術研究報告 第104巻 第246号 13ページ、2004年8月19日。同じ題名で聴覚研究会資料 第34巻 第6号 409ページ（2004年8月）にも登録がある。
- 野口洲、薗田光太郎、喜安千弥「ポスター講演 ステガノグラフィック音響秘密分散法」電子情報通信学会技術研究報告 第118巻 第495号 55ページから60ページ、2019年3月。CiNii Researchのキーワードは秘密分散法、ステガノグラフィ、エコー拡散法である。

このうち3件目は「音響の秘密分散にステガノグラフィを組み合わせる」という主題であり、CipherFluteの「偽装した担体に秘密を載せる」という主張と重なる可能性がある。国内の先例として一度は当たっておくべきものである。

あわせて、大川と栃窪の論文の参考文献欄（49ページ）で、国内の視覚復号型秘密分散の応用研究がいくつか挙がっていることを確認した。私は各原典に当たっていないので、大川と栃窪の記載をそのまま写す。

- 須賀雄治、岩村惠市、櫻井幸一、今井秀樹「複数の機密画像を埋め込み可能なグラフタイプ視覚復号型秘密分散方式のお拡張」情報処理学会論文誌 第42巻 第8号 2106ページから2113ページ、2001年。
- 高澤匠、鈴木一弘、高田直樹「ホログラフィと視覚復号型秘密分散法を利用した三次元画像暗号化の検討」CSEC 第86巻 第28号 1ページから6ページ、2019年。
- 大岡悠加、稲葉宏幸「覗き見を考慮した視覚復号型秘密分散法による個人認証方式の提案」コンピュータセキュリティシンポジウム 1043ページから1049ページ、2015年。
- 水野涼、稲葉宏幸「スマートフォンを用いた視覚復号型秘密分散法による個人認証方式の提案」ISEC2017-35、第117巻 第125号 259ページから266ページ、2017年。

---

## 第4部　CipherFluteのハートのカードに残る差分についての厳しい判断

判断の材料として、CipherFluteの当該実装の内容を論文の原稿（`paper/` の第12版のテキスト、6.3節相当）から確認した。要点は次のとおりである。同じ作りのカードを2枚、余白どうしを向かい合わせに並べ、その境界にハートを抜いてある。1枚では半分のハートにしかならない。秘密は2-of-2で分け、片方に乱数を、もう片方に秘密から乱数を引いた値を入れる。片方だけでは一様な乱数にしか見えない。2枚で20.8ビットを運ぶ。読み出しアプリで1枚目を確定してから2枚目を吹くと合成して認証まで進む。合成した秘密を鍵として遷移先URLをAES-GCMで暗号化しておくと、2枚がそろったときにだけそのページが開く。

これを上に確定した文献群と突き合わせると、次のようになる。

### 4.1 新規性として主張できないもの（4件）

第一に、「2枚そろって初めて意味を持つ物理媒体」という枠組みは新しくない。NaorとShamirが1994年に「The original encryption problem can be considered as a 2 out of 2 secret sharing problem」と明言している。

第二に、「片方だけでは一様な乱数にしか見えない」という性質も新しくない。NaorとShamirが「each one of them is indistinguishable from random noise」と書き、閾値未満のシェアから情報理論的に何も漏れないことを主張している。

第三に、「秘密分散のシェアを、怪しまれない見た目や音にする」という偽装の動機も新しくない。Desmedt、Hou、Quisquaterが1998年に、視覚暗号のシェアが乱雑な模様であることを弱点として明示し、自分たちのシェアが音楽や画像であって人間の検閲者に怪しまれないことを利点として掲げている。

第四に、「物理的な2枚1組でパスワードを守る」という応用も新しくない。大川と栃窪が2026年4月に、紙のシェアとOHPシートまたはスマートフォンのシェアを重ねてパスワードを復元する方式を提案し、社会人と大学生を対象に評価している。用途はCipherFluteのカード実装とほぼ同じである。

### 4.2 差分として残るもの（3件、いずれも軽い）

第一に、**復号の計算の所在が逆である。**視覚暗号と大川・栃窪の方式では、復号は人間の感覚器が行い、装置も計算もいらない。CipherFluteのカードでは、復号は記号の加減算であり、読み出しはスマートフォンのマイクとアプリが行う。これは差分ではあるが、**CipherFluteの側が劣っている方向の差分である。**新規性の主張にはならない。論文では「電源不要」の主張の範囲を記憶媒体の側に限定して書き、読み出し側の装置依存を認めるべきである。

第二に、**媒体の形が閾値そのものを述べている。**半分のハートという外形が「2枚そろえる必要がある」ことを、覚え書きを添えずに物の形だけで告げている。視覚暗号のシェアは乱雑な模様であるから、それを見ても必要な枚数は分からない。大川・栃窪の方式も、シェア画像を見て枚数は分からない。この「外形が接続構造を宣言する」という性質は、私が調べた範囲では先例を見つけられなかった。ただし、これは暗号としての貢献ではなく、対話型システムの設計としての貢献である。WISSの査読の枠組みではそれで十分に通る種類の主張であるが、「新しい暗号プリミティブ」として書くと確実に落とされる。

第三に、**秘密の正体が違う。**視覚暗号の秘密は画像であり、音響秘密分散の秘密は音である（徳重らの英語の抄録が「a secret and shares are acoustic information」と明記している）。すなわち従来の系譜では、感覚に訴える内容そのものが秘密であった。CipherFluteの秘密はビット列（暗号資産の復元用情報など）であり、音は運搬の経路にすぎない。この違いは実は大きい。感覚に訴える内容を秘密にする方式は、対比の劣化や聴覚の解像度に律速されるので運べる量が本質的に曖昧である。ビット列を運ぶ方式は誤り訂正符号を載せられ、運べる量を数字で言える。CipherFluteが2枚で20.8ビットと言えるのはこの違いによる。ただしこれは「秘密分散を物理媒体に載せる」というcodex32やSLIP-0039と同じ土俵の話であり、視覚暗号や音響暗号との差分としては言えるが、それらに対する優位を主張するには相手を取り違えていることになる。

### 4.3 厳しい結論

ハートのカードは、**視覚暗号と音響暗号の系譜に対して、暗号としての新規性をまったく持たない。**枠組み（2-of-2）、安全性の性質（片方だけでは一様な乱数に見える）、偽装の動機（怪しまれない担体）、応用（パスワードの物理的な分散保管）のすべてに先例がある。しかも復号に計算装置を要する点で、視覚暗号と大川・栃窪の方式より徹底していない。

残るのは、（1）外形が閾値を宣言するという物の作りの工夫と、（2）秘密がビット列であることによって運べる量を数字で言えることである。前者は本質的に演出であり、後者は視覚暗号との差分ではなくcodex32との共通点である。

したがって論文での書き方として次を推奨する。ハートのカードを「新しい秘密分散の方式」として書くのはやめ、**「符号化された笛という媒体が2-of-2の秘密分散のシェアを担えることを示す実装例」**として位置づけ、視覚暗号（NaorとShamir）、音響暗号（Desmedtら）、大川と栃窪の3件を引いたうえで「秘匿の力は秘密分散にのみ負わせており、感覚器による重ね合わせを復号手段として主張するものではない」と明記する。この一文があるかないかで、査読者が「既知手法の焼き直し」と読むか「実装例」と読むかが分かれる。前段の記録も同じ趣旨の助言をしていたが、私が原典を読んだ結果、その助言の必要性は前段の判定（脅威の度合いは中）よりも強い。

なお、CipherFluteの新規性の主張は、この2枚1組の実装ではなく次の点に置くしかない。電源も電子部品も持たない造形物が、吹かれたときの音の高さで、誤り訂正符号つきの少量の情報を運び、それを日用品に埋め込んだまま鳴らせるという点である。これはこの文献群のどれもやっていない。第2部で確定した符号設計の最適性（隣接同音禁止のもとでの上限をちょうど達成していること）も、その主張を支える材料になる。

---

## 第5部　前段の報告に対する判定

- 第一の論点について、前段の報告は**おおむね正しい。**Goldmanらの3つの主張はすべて原典で裏が取れた。訂正すべき点はなく、補うべき点が1つある（制約を課す動機がGoldmanらは誤り率、CipherFluteは同期であるという違いである）。あわせて、前段が未解決として残した「13から実効12へ落とす損失が最適かどうか」に答えを出した。最適である。
- 第二の論点について、前段の報告は**一部誤りである。**Desmedtらの論文の内容と書誌はおおむね正しかったが、「計算機なしに人間の感覚器だけで復号できる」という性質の帰属が音響暗号と光学暗号については言いすぎであった。そして徳重らについて2か所の誤りがあった。著者が3名ではなく6名であり、提案手法は波の干渉を用いるのではなく用いない方式である。
- あわせて、前段が未確認としていたEUROCRYPT '94の予稿集のLecture Notes in Computer Scienceの巻番号を第950巻と確定した。

---

## 第6部　確認できなかったこと

1. McLaughlin、Luo、Xieの1995年の論文の本文と抄録に到達できなかった。出版社が閉じており、Semantic Scholarの応答も抄録が削除されていることを明記している。この論文は書誌のみを確認した。q個の記号のランレングス制限符号の容量を扱っていることは、ImminkとCaiがこの論文を特性方程式の出所として挙げていることから分かるが、その中身を私自身で読んで確かめてはいない。したがって論文で引くなら、Shannonの1948年の論文とMarcus・Roth・Siegelの教科書とImmink・Caiの論文の3件で足り、McLaughlinらは「同じ結果をq個の記号について扱った論文がある」という位置づけで添えるのが安全である。
2. ImminkとCaiの論文について、IEEE Accessの確定版のPDFを取得できなかった（HTTP 502）。私が読んだのは著者が公開している査読前の版（arXiv:1812.06798v1、2018年12月14日）である。表1の数値と式(19)(20)がこの版に載っていることは確認したが、確定版で数式番号や表番号が変わっている可能性がある。論文で引くときは、数式番号や表番号を書かず、内容だけで引くのが安全である。
3. Marcus、Roth、Siegelの文書は著者が公開している教科書の草稿であり、査読を経た刊行物ではない。同じ3名による Constrained Systems and Coding for Recording Channels というHandbook of Coding Theoryの章が存在するとされているが、その書誌を私は確認していない。教科書として引くなら Immink, Codes for Mass Data Storage Systems, Second Edition, Shannon Foundation Publishers, 2004（ImminkとCaiの参考文献[10]として確認した）のほうが刊行物としては正式であるが、こちらの本文には到達していない。
4. Desmedt、Hou、Quisquaterの1998年の論文と、Desmedt、Le、Quisquaterの2000年の論文について、本文に到達できなかった。出版社が有料である。書誌（題名、著者、収録書名、叢書の巻番号、ページ、刊行年）と抄録の全文は出版社の章のページで確認した。したがって「復号にどの程度の装置が必要か」についての私の判定は抄録の記述に基づくものであり、本文にさらに詳しい条件が書かれている可能性がある。
5. 徳重らの論文の本文に到達できなかった。電子情報通信学会の技報閲覧サービスは会員向けである。著者抄録の全文（日本語と英語）は学会の公式ページで確認したので、方式の骨格と安全性の基準は原典の記述で言える。ただし実験の条件や、シェアを何枚に分けたかといった細部は確認できていない。
6. 「媒体の外形が秘密分散の閾値を宣言する」という設計に先例があるかどうかを、確定できなかった。英語のWeb検索と、CiNii Researchの日本語検索を行ったが、該当する研究や特許を見つけられなかった。見つからなかったことは「存在しない」ことの証明ではない。とくにジグソーパズル状の形をした鍵の分割については、意匠や玩具の特許に埋もれている可能性がある。Google PatentsとJ-PlatPatを外形の観点で調べる作業が残っている。
7. 大川直也の学位論文について、前段の記録は日本大学から2026年3月25日に授与されたと書いている。いっぽう2026年4月15日発行の本論文の著者紹介欄は「2024 日本大学大学院・生産工学研究科・数理情報工学専攻博士後期課程在学中」と書いている。採録日が2026年1月13日であるから紹介文が学位授与前に書かれたと考えれば矛盾しないが、私はこの点を学位記録に当たって確かめていない。

---

## 第7部　この文書で確定した書誌の一覧

第1部と第2部（符号設計）

1. Nick Goldman, Paul Bertone, Siyuan Chen, Christophe Dessimoz, Emily M. LeProust, Botond Sipos, Ewan Birney, "Towards practical, high-capacity, low-maintenance information storage in synthesized DNA", Nature, Vol. 494, No. 7435, pp. 77-80, 2013. DOIは 10.1038/nature11875 である。確認先は https://pmc.ncbi.nlm.nih.gov/articles/PMC3672958/ である。
2. C. E. Shannon, "A Mathematical Theory of Communication", The Bell System Technical Journal, Vol. 27, pp. 379-423 and pp. 623-656, July and October 1948. 第1節と定理1が該当箇所である。確認先は https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf である。
3. Brian H. Marcus, Ron M. Roth, Paul H. Siegel, "An Introduction to Coding for Constrained Systems", Fifth Edition, October 2001. 第3章、3.1節の定義および72ページの定理3.4が該当箇所である。確認先は https://personal.math.ubc.ca/~marcus/Handbook/ である。
4. Kees A. Schouhamer Immink, Kui Cai, "Properties and Constructions of Constrained Codes for DNA-Based Data Storage", IEEE Access, Vol. 8, pp. 49523-49531, 2020. DOIは 10.1109/ACCESS.2020.2980036 である。私が読んだのは arXiv:1812.06798v1（2018年12月14日、https://arxiv.org/pdf/1812.06798 ）である。第4節の式(19)(20)と表1が該当箇所である。
5. Steven W. McLaughlin, Jian Luo, Qun Xie, "On the capacity of M-ary runlength-limited codes", IEEE Transactions on Information Theory, Vol. 41, No. 5, pp. 1508-1511, September 1995. DOIは 10.1109/18.412712 である。書誌のみ確認した。確認先は https://dblp.org/search/publ/api?q=Capacity+of+M-ary+Runlength-Limited+Codes&format=json である。
6. Franziska Weindel, Andreas L. Gimpel, Robert N. Grass, Reinhard Heckel, "Embracing Errors Is More Efficient Than Avoiding Them Through Constrained Coding for DNA Data Storage", arXiv:2308.05952, 2023年8月11日投稿、2024年6月26日改訂である。確認先は https://arxiv.org/abs/2308.05952 である。

第3部（2枚1組の物理媒体）

7. Moni Naor, Adi Shamir, "Visual Cryptography", Advances in Cryptology — EUROCRYPT '94, Lecture Notes in Computer Science, Vol. 950, pp. 1-12, Springer, 1995（会議は1994年である）。DOIは 10.1007/BFb0053419 である。確認先は著者公開の全文 https://www.wisdom.weizmann.ac.il/~naor/PAPERS/vis.pdf と出版社のページ https://link.springer.com/chapter/10.1007/BFb0053419 である。
8. Yvo Desmedt, Shuang Hou, Jean-Jacques Quisquater, "Audio and Optical Cryptography", Advances in Cryptology — ASIACRYPT'98, Lecture Notes in Computer Science, Vol. 1514, pp. 392-404, Springer, 1998. DOIは 10.1007/3-540-49649-1_31 である。確認先は https://link.springer.com/chapter/10.1007/3-540-49649-1_31 である。
9. Yvo Desmedt, Tri V. Le, Jean-Jacques Quisquater, "Nonbinary Audio Cryptography", Information Hiding（第3回Information Hidingワークショップ、1999年9月29日から10月1日、ドイツ・ドレスデン）, Lecture Notes in Computer Science, Vol. 1768, pp. 478-489, Springer, 2000. DOIは 10.1007/10719724_33 である。確認先は https://link.springer.com/chapter/10.1007/10719724_33 である。
10. 大川直也、栃窪孝也「視覚復号型秘密分散法を用いたパスワードの分散管理の提案」情報処理学会論文誌デジタルプラクティス、第7巻、第2号、35ページから50ページ、2026年4月15日。ISSNは 2435-6484 である。確認先は https://ipsj.ixsq.nii.ac.jp/records/2009100 と本文のPDF https://ipsj.ixsq.nii.ac.jp/record/2009100/files/IPSJ-TDP0702007.pdf である。
11. 徳重佑樹、三澤裕人、吉田文晶、上床昌也、岩本貢、太田和夫（電気通信大学）「物理的復元が容易な音響秘密分散法」電子情報通信学会技術研究報告（信学技報）、第115巻、第38号、IT2015-14 および EMM2015-14、75ページから80ページ、2015年5月14日発行（講演は2015年5月22日、マルチメディア情報ハイディング・エンリッチメント研究会と情報理論研究会の共催、京都市国際交流会館）。確認先は https://ken.ieice.org/ken/paper/20150522IbAn/ である。
12. 野口洲、薗田光太郎、喜安千弥「ポスター講演 ステガノグラフィック音響秘密分散法」電子情報通信学会技術研究報告（信学技報）、第118巻、第495号、55ページから60ページ、2019年3月。確認先は https://cir.nii.ac.jp/crid/1520290883418767872 である。書誌のみ確認した。
13. 藤田倫弘、西村竜一、鈴木陽一「1ビットオーディオ音響秘密分散法における分散情報の有意味音化」電子情報通信学会技術研究報告（信学技報）、第104巻、第246号、13ページ、2004年8月19日。確認先は https://cir.nii.ac.jp/crid/1520853832636632832 である。書誌のみ確認した。
14. 藤田倫弘「1ビットオーディオを対象とした音響秘密分散法の提案」日本音響学会講演論文集、2004年、578ページ。確認先は https://cir.nii.ac.jp/crid/1571698600027500160 である。書誌のみ確認した。
