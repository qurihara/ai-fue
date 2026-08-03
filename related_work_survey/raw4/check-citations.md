# 草稿の引用の検証と、完全な参考文献リスト

検証対象は `/Users/kurihara/.../ai-fue/paper/cipherflute_wiss2026_v2_draft.md`（2026年7月30日版、426行）である。
検証日は2026年7月30日である。

突き合わせに使った記録は次のとおりである。

- `related_work_survey/REFERENCES_TO_ADD.md`
- `related_work_survey/raw2/`（f2、f5、f6、v1、v3、v4）
- `related_work_survey/raw3/`（c1からc6）
- `related_work_survey/raw/02-passive-acoustic-tags.md`、`raw/11-physical-security-steganography.md`
- `related_work_survey/PAPER_REVISION.md`、`REVIEW_AND_REPOSITIONING.md`、`SURVEY.md`、`00-digest.md`
- 旧稿の生成器 `paper/make_paper_wiss_v12.py` の732行から756行（旧版の参考文献リスト[1]から[23]）

記録に無い引用、および記録と食い違う引用については、以下の一次情報にこの検証のなかで実際に当たった。

- Blowholeの予稿集の本文（http://graphicsinterface.org/wp-content/uploads/gi2018-18.pdf を取得し、pdftotextで全文を抽出した）
- Crossrefの書誌レコード（Smith and Senturia、Levine and Schwinger、Widmer and Franaszek、Crawford and Iriberri、Wolfe ら、Putz ら、Tejada、Miyatake ら、Immink and Cai）
- 情報処理学会電子図書館の吉川茂さんの書誌（https://ipsj.ixsq.nii.ac.jp/records/72682）
- BIP-93の本文（https://raw.githubusercontent.com/bitcoin/bips/master/bip-0093.mediawiki）
- 国際電気通信連合の勧告ページ（Q.23、V.21、T.30）
- Semantic Scholarの書誌と抄録（Tejadaさんの Print-and-Play）

---

## 0. 全体の判定

**書誌が実在しないもの、すなわち捏造された引用は1件も見つからなかった。** 草稿が挙げる文献はすべて実在する。

一方で、投稿前に必ず直さなければならない問題が7件ある。最も重いのは次の3つである。

1. 参考文献リストが未完成である。本文が59個の番号を引くのに対し、リストには23件しか実体が無い。36個の番号が空である。
2. 本文の番号と旧版の番号が混在しており、[17][18][23]が欠番になっている。
3. 原典の内容と食い違う記述が3か所ある（Desmedtらの復号装置、SeedQRの規模、codex32の回転円板）。

以下に、確認した内容を順に書く。

---

## 1. 本文の番号と参考文献リストの対応

### 1.1 本文が引く番号

草稿の本文（表を含む）が引く番号を機械的に数えた。出現する番号は次の59個である。

1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 19, 20, 21, 22, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62

**欠番は[17]、[18]、[23]の3つである。** この3つは旧稿の生成器 `paper/make_paper_wiss_v12.py` の749行、750行、755行に実体があり、それぞれ次のものである。

- [17] Eskandari, S. ほか: A First Look at the Usability of Bitcoin Key Management, USEC 2015
- [18] Shamir, A.: How to Share a Secret, Communications of the ACM, 1979
- [23] Madhavapeddy, A. ほか: Audio Networking: The Forgotten Wireless Technology, IEEE Pervasive Computing, 2005

すなわち、v2の草稿は番号をv1.2から引き継いだまま本文を書き直したため、v1.2で引いていた3件が本文から落ちて欠番になっている。**重複した番号は無い。**

### 1.2 参考文献リストにある番号

草稿の参考文献リスト（399行から426行）に実体があるのは次の23件だけである。

1, 2, 3, 4, 5, 6, 7, 8, 24, 25, 26, 28, 30, 31, 32, 34, 39, 41, 42, 44, 48, 51, 60

**したがって、本文が引きながらリストに実体が無い番号が36個ある。**

9, 10, 11, 12, 13, 14, 15, 16, 19, 20, 21, 22, 27, 29, 33, 35, 36, 37, 38, 40, 43, 45, 46, 47, 49, 50, 52, 53, 54, 55, 56, 57, 58, 59, 61, 62

このうち[9]から[16]、[19]から[22]は旧稿の生成器に実体があるので、単に転記すれば埋まる。ただし[16]については後述する内容の食い違いがある。残りは本稿の第4章に補った。

---

## 2. 投稿前に必ず直すべきもの

### 2.1 Desmedtらの方式を「復号に計算装置をまったく要さない」と書いている（草稿125行）

草稿125行は次のように書いている。

> 計算機を使わずに人間の感覚だけで復号する系譜としては、視覚暗号 [42] が1994年に……Desmedtら [43] は音響版と光学版を示し……国内では大川と栃窪 [44] が……**これらは復号に計算装置をまったく要さない点で本研究より徹底しており**、一方で符号が見えていることは避けられない。

「これら」に[43]が含まれるので、Desmedtらの方式も装置を要しないことになる。これは原典と食い違う。

根拠は `related_work_survey/REFERENCES_TO_ADD.md` の174行である。

> **「計算機なしに人間の感覚器だけで復号できる」と書くのは言いすぎである。** 音響の側は抄録が "To decrypt the message, one just plays two shares on a stereo system" であり再生装置を要する。光学の側は "The Mach-Zehnder interferometer is used as the decryption machine" であり干渉計を要する。装置も計算も不要という主張は視覚暗号の側に限られる。

**直し方。** 「これらは」を「視覚暗号と大川さんと栃窪さんの方式は」に限定し、Desmedtらについては別に一文を立てて、音響版はステレオ再生装置を、光学版はマッハ・ツェンダー干渉計を復号装置として要すると書く。査読者がASIACRYPT'98の抄録を見れば一目で分かる箇所なので、放置すると論文全体の正確性が疑われる。

### 2.2 SeedQRの規模の記述が標準形式と圧縮形式を取り違えている（草稿120行）

草稿120行は次のように書いている。

> SeedQR [40] はBIP-39の語を索引番号に写して二次元コードに収め、**128ビットを21×21の格子に載せて**金属板に打刻する仕様である。

128ビットが21×21に収まるのは、標準のSeedQRではなくCompactSeedQRである。根拠は `related_work_survey/raw2/v3-codex32-seedqr.md` の94行と96行である。

> 標準のSeedQRは、BIP-39の英語語彙2048語における各語の位置……を4桁の十進数に零詰めし……12語では48桁になり、誤り訂正水準Lの21×21には……入らず**25×25に収まる**。
> CompactSeedQRは、各語の索引を11ビットの二進で表して連結し、末尾のBIP-39検査ビット……を落として……**12語では128ビットすなわち16バイトになり21×21に収まる**。

`REFERENCES_TO_ADD.md` の43行も同じ内容を確定事実として書いている。

**直し方。** 「SeedQRは……128ビットを21×21に載せる」を「SeedQRの圧縮形式であるCompactSeedQRは、索引を11ビットで連結して検査ビットを落とし、128ビットを21×21の格子に収める。標準のSeedQRは索引を4桁の十進数で連結するので12語では25×25になる」と書き分ける。

なお草稿351行の「128ビットの秘密は、二次元コードを使う仕様なら70ミリメートル角の板1枚に収まり」も同じ数字を指しているので、ここにも同じ文献番号を付ける必要がある。現在この文には出典が付いていない。根拠は `raw2/v3-codex32-seedqr.md` の218行の表（「21×21の枡（70ミリメートル角の板1枚）」）である。

### 2.3 codex32の「回転円板」をBIP-93に帰している（草稿119行、203行、347行）

草稿119行は次のように書いている。

> codex32 [39] はシードを32文字のアルファベットで符号化し、有限体GF(32)上のBCH符号による検査符号を付けて、Shamirの秘密分散の分割と復元を**紙と鉛筆と回転円板だけで人手で実行する**。

この検証でBIP-93の本文（https://raw.githubusercontent.com/bitcoin/bips/master/bip-0093.mediawiki）を取得して確かめたところ、"wheel"、"volvelle"、"rotating disc" のいずれの語も本文に出現しない。`REFERENCES_TO_ADD.md` の35行も同じことを書いている。

> 「紙の回転円板」はBIP-93の本文に一度も現れない。BIP-93は手計算の具体的手順を標準の範囲外と明記している。参照実装は「対応する財布が存在しないので本物の金銭に使うな」と警告しており、状態は今もDraftである。

同じ問題が草稿347行にもある。「作者自身が本物の金銭に使わないよう警告している」という記述の出所も、BIP-93ではなく参照実装のリポジトリと公式サイトである。

**直し方。** [39]をBIP-93への引用とし、回転円板と実用への警告については参照実装（https://github.com/BlockstreamResearch/codex32）と公式サイト（https://secretcodex32.com/）を別の番号で引く。本稿の第4章の[36]がそれにあたる。

なお、BIP-93の本文から確認できた検査符号の性能は「detection of any error affecting at most 8 characters」であり、置換4文字まで、消失8文字まで、連続消失13文字までの訂正である。草稿の記述はこの範囲で正確である。

### 2.4 [16]の実体が旧稿のままだと本文の数字を支えない

草稿241行は次のように書いている。

> 広く使われる封印120種類が熟練者1人あたり平均5分未満、平均55ドルで破られたという報告 [16]

旧稿の[16]は `paper/make_paper_wiss_v12.py` の748行にある次の文献である。

> [16] Johnston, R. G.: Tamper-Indicating Seals: Practices, Problems, and Standards, Los Alamos National Laboratory Report (2003).

しかし、120種類・5分未満・55ドルという数字を報告しているのは2001年の別の論文である。根拠は `REFERENCES_TO_ADD.md` の270行と `raw/11-physical-security-steganography.md` の29行である。

> Johnston, R. G.: Tamper-Indicating Seals for Nuclear Disarmament and Hazardous Waste Management, Science & Global Security, Vol. 9, pp. 93–112 (2001). DOI 10.1080/08929880108426490　封印120種類すべてが熟練者1人あたり平均5分未満、平均55ドルで破られた。

**直し方。** [16]を2001年のScience & Global Securityの論文に差し替える。

さらに `raw/11-physical-security-steganography.md` の31行が次の留保を付けているので、そのまま書くかどうかは判断が要る。

> 120種類という数字とそれに伴う所要時間や費用の数値は、この2001年の論文が自ら測ったものとして報告しているが、その出所として同論文の注11が Johnston と Garcia の1997年の脆弱性評価論文を挙げている。

本稿は2001年の論文を引く案を採る。数値をそのまま引用しても不正確ではないが、原出典が1997年の論文であることは記録に残っている。

### 2.5 記録側の[50]の書誌に題名の誤りがある

草稿185行は隣接同記号禁止の容量の上限を[50]で引いている。この[50]の中身として `REFERENCES_TO_ADD.md` の155行が挙げているのは次の文献である。

> Immink, K. A. S. and Cai, K.: **Design of Capacity-Approaching Constrained Codes for DNA-Based Storage Systems**, IEEE Access, Vol. 8, pp. 49523–49531 (2020).
> 確認先: 著者公開の査読前版 arXiv:1812.06798。

**この書誌は題名と掲載が食い違っている。** この検証で一次情報に当たって確かめた。

- arXiv:1812.06798（https://arxiv.org/abs/1812.06798）の題名は "Properties and constructions of constrained codes for DNA-based data storage" である。
- Crossrefによれば、"Properties and Constructions of Constrained Codes for DNA-Based Data Storage" は IEEE Access, Vol. 8, pp. 49523–49531 (2020)、DOI 10.1109/ACCESS.2020.2980036 である。
- 一方、"Design of Capacity-Approaching Constrained Codes for DNA-Based Storage Systems" は別の論文であり、Crossrefによれば IEEE Communications Letters, Vol. 22, pp. 224–227 (2018)、DOI 10.1109/LCOMM.2017.2775608 である。

すなわち記録は、2018年の論文の題名に2020年の論文の掲載とページを貼り合わせている。**このまま論文に写すと、存在しない書誌を印刷することになる。** 本稿の第4章では2020年のIEEE Accessの論文として正しく書いた。

なお、この差し替えによって主張が変わるかどうかは確かめていない。記録は「表1のm=1の欄が log2 3 = 1.5850 である」と書いているが、その表がどちらの論文の表かをこの検証では確認できていない。**投稿前に、採用する側の論文の本文で特性方程式と表を確認することを勧める。** 確認できない場合は、Shannon（1948）とMarcus、Roth、Siegelの教科書だけで論を立てても十分に成り立つ。

### 2.6 [47]の実体が無く、端の補正の一次文献が決まっていない

草稿161行は次のように書いている。

> この形の関係と端の補正は管楽器の音響学で確立した知識であり [47]、本研究の寄与ではない。

参考文献リストに[47]の実体は無い。依頼にあった吉川茂さんの論文が適切かどうかを判断した。

**書誌はこの検証で情報処理学会電子図書館（https://ipsj.ixsq.nii.ac.jp/records/72682）に当たって確定した。**

> 吉川茂: 正倉院尺八吹奏時の歌口端補正長さの推定（英語題名は Estimation of the embouchure-hole length correction when playing a shousouin shakuhachi）, 情報処理学会研究報告 音楽情報科学, 2011-MUS-89, No. 1, pp. 1–5 (2011年2月4日). 著者所属は九州大学大学院芸術工学研究院である。

**判定。この論文は「端の補正が音響学の確立した概念である」ことの傍証にはなるが、草稿161行の主張の一次文献としては不十分である。** 理由は2つある。第一に、この論文が扱うのは正倉院に伝わる特定の尺八の歌口端と指孔開孔端の補正長さの推定であって、管の長さと基本周波数の一般的な関係式を確立した文献ではない。第二に、この論文はむしろ「端の補正が既に確立した概念であること」を前提として使う側の研究である。

**より適切な一次文献として、次を推す。** この検証でCrossref（https://api.crossref.org/works/10.1103/PhysRev.73.383）に当たって書誌を確定した。

> Levine, H. and Schwinger, J.: On the Radiation of Sound from an Unflanged Circular Pipe, Physical Review, Vol. 73, No. 4, pp. 383–406 (1948).

これは開いた管の端から放射される音を解析的に解き、開口端の補正長さを管の半径の0.6133倍として導いた論文であり、管楽器の音響学において端の補正の出発点として引かれる文献である。草稿の「この形の関係と端の補正は管楽器の音響学で確立した知識であり」という文には、この文献が直接に対応する。

そのうえで、**吉川さんの論文は落とさずに併記することを勧める。** 実際の笛について端の補正を推定する営みが国内の情報処理学会研究報告に存在することを示せるので、投稿先の読者に対する目配りとして働く。本稿の第4章では[44]と[45]の2件として並べた。

### 2.7 出典の無い数値と規範がある

次の4か所は、数値や規範を述べながら文献番号を持たない。査読で必ず問われる。

| 草稿の行 | 出典の無い記述 | 付けるべき文献 |
| --- | --- | --- |
| 35行 | 「覆いを外さなければ読めないことを認めていたり、仕様書が『自分の二次元コードを絶対に撮影するな』と警告していたり」 | QR SafeShareとSeedQRの2件。根拠は `raw2/v3-codex32-seedqr.md` の133行と238行にある |
| 107行 | 「10万回規模でダウンロードされている」 | Flat Pocket Whistle（`REFERENCES_TO_ADD.md` 305行、ダウンロード97,000件）と Whistle Pan flute（同306行） |
| 245行 | 「112ビット以上の秘密に限って成り立つ」 | NIST SP 800-131A Rev. 2。根拠は `raw3/c6-security-soundness.md` の83行にある |
| 351行 | 「二次元コードを使う仕様なら70ミリメートル角の板1枚に収まり」 | CompactSeedQR。根拠は `raw2/v3-codex32-seedqr.md` の218行にある |

---

## 3. 直したほうがよいが致命的でないもの

### 3.1 [51]の題名が途中で切れている

草稿424行は次のようになっている。

> [51] 中尾美月ほか：尺八のCT画像の輝度値に基づく3Dモデルの内径補正, 情報処理学会研究報告SLP (2026).

正しい題名は「尺八のCT画像の輝度値に基づく3Dモデルの内径補正**と付加製造による復元評価**」である。根拠は `raw2/f2-ipsj-nenji.md` の58行から63行である。著者は中尾美月さん、須藤壮一朗さん、水野明哲さん、高橋義典さんの4名、所属は工学院大学、掲載は2026-SLP-159, No. 24, pp. 1–6（2026年2月24日）である。

### 3.2 [60]に題名が無い

草稿425行は「Chhetri, S. R., Canedo, A. and Al Faruque, M. A.: ACM Trans. Cyber-Physical Systems, Vol. 2, No. 1 (2018).」となっており、題名が抜けている。正しくは "Confidentiality Breach Through Acoustic Side-Channel in Cyber-Physical Additive Manufacturing Systems" である（`REFERENCES_TO_ADD.md` 64行）。

あわせて、草稿255行は「造形機の動作音から工具経路と形状を復元する攻撃は**2016年に**軸の推定精度86パーセントで示され [60]」と書いているが、[60]は2018年の論文誌版である。86パーセントという数字を報告しているのは論文誌版であり、2016年はICCPSの会議版の年である（`REFERENCES_TO_ADD.md` 67行）。会議版を併記するか、「2016年に」を落とすかのどちらかにする必要がある。

### 3.3 [1]のページ範囲と予稿集のファイル名

**依頼にあった注記は正しい。** この検証で予稿集の本文（http://graphicsinterface.org/wp-content/uploads/gi2018-18.pdf）を取得し、pdftotextで全文を抽出して確かめた。

- 1ページ目の柱は "Graphics Interface Conference 2018, 8-11 May, Toronto, Ontario, Canada" である。
- 題名は "Blowhole: Blowing-Activated Tags for Interactive 3D-Printed Models"、著者は Carlos Tejada、Osamu Fujimoto、Zhiyuan Li、Daniel Ashbrook で、所属は Rochester Institute of Technology である。
- 最終ページの下端の頁番号は128である。したがって通し頁は122から128である。

つまり「予稿集のファイル名は gi2018-18.pdf である」という草稿403行の注記は正しい。ただし、注記の書き方としては読者の役に立ちにくい。**予稿集のファイル名を本文に書くよりも、DOI 10.20380/GI2018.18 とページ範囲 pp. 122–128 を書き、ACM Digital Libraryが131–137を掲げていることを注記するほうが実用的である。** 根拠は `raw/02-passive-acoustic-tags.md` の54行と55行、および `REFERENCES_TO_ADD.md` の352行である。

なお、同じ抽出のなかで次の2点も原典で直接に確かめた。草稿95行の記述はいずれも正確である。

> "with up to six cavities, the system achieves a high user-independent performance of 98%"
> "Our system enables high performance for up to nine different blowholes"

### 3.4 Print-and-Playを「博士研究全体」と書いている（草稿95行）

草稿95行は「著者自身が後に、自らの博士研究全体を『組み立ても較正も要らない3Dプリント対話物体』という枠組みで位置づけ直している [33]」と書いている。

この検証でCrossref（https://api.crossref.org/works/10.1145/3334480.3375025）とSemantic Scholarに当たったところ、単著の Extended Abstracts of the 2020 CHI Conference, pp. 1–6 であることは確定したが、**博士課程のための投稿区分であることを示す記載は見つからなかった。** 抄録は2つの技術をまとめた研究の見取り図として書かれている。

「博士研究全体」と断定できる根拠を持たないのであれば、「自らの一連の研究を……という枠組みでまとめ直している」と書くほうが安全である。

### 3.5 視覚暗号の年

草稿421行は「[42] Naor, M. and Shamir, A.: Visual Cryptography, EUROCRYPT '94, LNCS Vol. 950.」と書き、年を落としている。`REFERENCES_TO_ADD.md` の161行は「Advances in Cryptology — EUROCRYPT '94, Lecture Notes in Computer Science, Vol. 950, pp. 1–12 (1995)」としている。会議は1994年、講義ノートの巻の刊行は1995年である。草稿125行が「1994年に」と書いていることと、参考文献に(1995)と書くことは両立するが、読者が混乱しないように「EUROCRYPT '94（1995年刊）」のように示すのがよい。

### 3.6 Dabinらの数値の言い方

草稿103行は「印刷したリコーダーの初版が目標に対して+6から+34セント、やすりで手修正した版が−13から+14セント」と書いている。`REFERENCES_TO_ADD.md` の215行は次のように書いている。

> リコーダー1が+6から+34セント（内訳は+34, +23, +24, +14, +16, +6）、リコーダー2が−40から+1セント、指孔2個をやすりで手修正した版が−13から+14セントである。

草稿は「リコーダー1」を「初版」と言い換え、リコーダー2の値を落としている。誤りではないが、原典の3つの版のうち2つだけを取り出していることが分かる書き方にしたほうがよい。

### 3.7 記録が「投稿前に一次資料で確認せよ」としていた国際電気通信連合の勧告の年を確認した

`REFERENCES_TO_ADD.md` の355行が積み残しにしていた項目である。この検証で勧告のページに当たって確かめた。

- Q.23「Technical features of push-button telephone sets」は1988年11月版が現行である（https://www.itu.int/rec/T-REC-Q.23/en）。
- V.21「300 bits per second duplex modem standardized for use in the general switched telephone network」は1988年11月版が現行である（https://www.itu.int/rec/T-REC-V.21/en）。
- T.30「Procedures for document facsimile transmission in the general switched telephone network」は2005年9月版が現行であり、2007年1月の追補が現行である（https://www.itu.int/rec/T-REC-T.30/en）。

**旧稿の生成器が書いていた1988年、2005年という年は正しい。** そのまま使ってよい。

### 3.8 引くべきなのに引いていない文献

`PAPER_REVISION.md` の110行が明示していた注記が、草稿63行の貢献の第四点に入っていない。

> 4. **どの層が秘密を守り、どの層は守らないのかを明示した脅威モデル。** 造形タグ13件のいずれも脅威モデルを持たない。**ただしQR SafeShareが同じ立場を実物として先に公開しており、Secure Information Embedding in Forensic 3D Fingerprinting が明示的な攻撃者モデルを置いていることは注記する。**

草稿63行は「攻撃者の能力を列挙して守れない範囲を宣言した研究は数少ない」と書いており、断定は避けているが、Wang らの2024年の論文を挙げていない。**「数少ない」と書くなら、その少数が誰かを示すのが誠実である。** 本稿の第4章の[67]に書誌を用意した。

同じく、秘密分散を3.7節と4章で扱いながら、Shamirの1979年の原典を引いていない。旧稿では[18]として持っていたものである。本稿の第4章の[66]に置いた。

また、`REFERENCES_TO_ADD.md` の344行が自己引用の候補として挙げているPicognizer（栗原一貴さんら、WISS 2017）は、草稿の経路1の実装が依って立つ系譜であるから、5.3節あるいは3.5節で引く価値がある。本稿の第4章の[68]に置いた。

---

## 4. 完全な参考文献リスト

番号を1から振り直した。**順序は本文で最初に引かれる順である。** 各項目に、本文のどこで引かれるべきかを付けた。

書誌の確度を3段階で示す。

- 「原典確認」は、この検証または記録において原典または著者公開版の本文に当たったものである。
- 「書誌確認」は、Crossref、DBLP、学会の予稿集ページ、標準化機関のページなど、書誌そのものを提供する一次的な経路で確かめたものである。
- 「要確認」は、投稿前に著者が確かめるべきものである。

### 4.1 リスト

**[1]** Willis, K. D. D. and Wilson, A. D.: InfraStructs: Fabricating Information Inside Physical Objects for Imaging in the Terahertz Region, ACM Trans. Graphics, Vol. 32, No. 4, Article 138 (2013). DOI 10.1145/2461912.2461936
引く場所は2.1節と表1である。書誌確認である。

**[2]** Li, D., Nair, A. S., Nayar, S. K. and Zheng, C.: AirCode: Unobtrusive Physical Tags for Digital Fabrication, Proc. ACM UIST 2017, pp. 449–460 (2017). DOI 10.1145/3126594.3126635
引く場所は2.1節、貢献の第二点、表1である。原典確認である（`raw3/c1-optical-hidden.md` が著者公開版の本文を精読している）。

**[3]** Maia, H. T., Li, D., Yang, Y. and Zheng, C.: LayerCode: Optical Barcodes for 3D Printed Shapes, ACM Trans. Graphics, Vol. 38, No. 4, Article 112 (2019). DOI 10.1145/3306346.3322960
引く場所は2.1節、2.6節、表1、6.3節である。書誌確認である。

**[4]** Dogan, M. D., Faruqi, F., Churchill, A. D., Friedman, K., Cheng, L., Subramanian, S. and Mueller, S.: G-ID: Identifying 3D Prints Using Slicing Parameters, Proc. ACM CHI 2020 (2020). DOI 10.1145/3313831.3376202
引く場所は2.1節である。書誌確認である。

**[5]** Dogan, M. D., Chan, V., Qi, R., Tang, G., Roumen, T. and Mueller, S.: StructCode: Leveraging Fabrication Artifacts to Store Data in Laser-Cut Objects, Proc. ACM SCF 2023 (2023).
引く場所は2.1節と表1である。書誌確認である。

**[6]** Getschmann, C. and Echtler, F.: Seedmarkers: Embeddable Markers for Physical Objects, Proc. ACM TEI 2021 (2021). DOI 10.1145/3430524.3440645
引く場所は2.1節である。書誌確認である。

**[7]** Ma, Z., Zhou, H. and Zhang, W.: AnisoTag: 3D Printed Tag on 2D Surface via Reflection Anisotropy, Proc. ACM CHI 2023 (2023). arXiv:2301.10599
引く場所は2.1節、2.6節、6.3節である。原典確認である（`REFERENCES_TO_ADD.md` 226行から229行）。

**[8]** Dogan, M. D., Taka, A., Lu, M., Zhu, Y., Kumar, A., Gupta, A. and Mueller, S.: InfraredTags: Embedding Invisible AR Markers and Barcodes Using Low-Cost, Infrared-Based 3D Printing and Imaging Tools, Proc. ACM CHI 2022, Article 269 (2022). DOI 10.1145/3491102.3501951
引く場所は2.1節、貢献の第二点、表1である。原典確認である（`raw3/c1-optical-hidden.md` が著者公開版の本文を精読している）。

**[9]** Jiang, W., Wang, C., Wei, J., Sarsenbayeva, Z., Irlitti, A., Knibbe, J., Dingler, T., Goncalves, J. and Kostakos, V.: InfoPrint: Embedding Interactive Information in 3D Prints Using Low-Cost Readily-Available Printers and Materials, Proc. ACM Interact. Mob. Wearable Ubiquitous Technol., Vol. 7, No. 3, pp. 1–29 (2023). DOI 10.1145/3610933
引く場所は2.1節である。原典確認である（`raw3/c2-thermal-and-viewangle.md` が査読前版の本文を読んでいる）。**要確認は著者の並びである。** 記録は「出版版は著者に Jing Wei が加わって9名になっている」と書いているが、並び順までは確定していない。

**[10]** Suzuki, M., Dechrueng, P., Techavichian, S., Silapasuphakornwong, P., Torii, H. and Uehira, K.: Embedding Information into Objects Fabricated With 3-D Printers by Forming Fine Cavities inside Them, IS&T International Symposium on Electronic Imaging (Media Watermarking, Security, and Forensics), Vol. 29, pp. 6–9 (2017).
引く場所は2.1節である。書誌確認である（`REFERENCES_TO_ADD.md` 112行から116行）。

**[11]** 久保勇貴, 江口佳那, 青木良輔, 近藤重邦, 東正造, 犬童拓也: 内部構造パターンの差異を利用した3Dプリントオブジェクト識別手法, WISS 2019（第27回インタラクティブシステムとソフトウェアに関するワークショップ）(2019). https://www.wiss.org/WISS2019Proceedings/oral/8.pdf
引く場所は2.1節である。原典確認である。英語版として Kubo, Y. ほか: FabAuth, Extended Abstracts of ACM CHI 2019, DOI 10.1145/3290607.3313005 を併記してもよい。

**[12]** Miyatake, Y., Punpongsanon, P., Iwai, D. and Sato, K.: interiqr: Unobtrusive Edible Tags using Food 3D Printing, Proc. ACM UIST 2022, pp. 1–11 (2022). DOI 10.1145/3526113.3545669
引く場所は2.1節である。書誌確認である（この検証でCrossrefに当たった）。草稿は国内の全国大会発表を指していたが、査読を経た国際会議の論文があるので、そちらを引くほうが強い。

**[13]** Koch, J., Gantenbein, S., Masania, K., Stark, W. J., Erlich, Y. and Grass, R. N.: A DNA-of-things storage architecture to create materials with embedded memory, Nature Biotechnology, Vol. 38, No. 1, pp. 39–43 (2020). DOI 10.1038/s41587-019-0356-z
引く場所は2.1節と2.6節の本文である。書誌確認である（`raw3/c4-dna-of-things.md`。本文は有料のため抄録と図の見出しと謝辞で確認している）。

**[14]** Harrison, C., Xiao, R. and Hudson, S. E.: Acoustic Barcodes: Passive, Durable and Inexpensive Notched Identification Tags, Proc. ACM UIST 2012, pp. 563–568 (2012). DOI 10.1145/2380116.2380187
引く場所は2.2節、表1、3.4節である。原典確認である（`raw2/f6-key-numbers.md` の105行が "we constrain the space of permissible bit sequences to exclude sequences with two consecutive 0 bits" を原文で引いている）。

**[15]** Savage, V., Head, A., Hartmann, B., Goldman, D. B., Mysore, G. and Li, W.: Lamello: Passive Acoustic Sensing for Tangible Input Components, Proc. ACM CHI 2015, pp. 1277–1280 (2015). DOI 10.1145/2702123.2702207
引く場所は2.2節と表1である。原典確認である。

**[16]** Laput, G., Brockmeyer, E., Hudson, S. E. and Harrison, C.: Acoustruments: Passive, Acoustically-Driven, Interactive Controls for Handheld Devices, Proc. ACM CHI 2015, pp. 2161–2170 (2015).
引く場所は2.2節である。書誌確認である（Blowholeの参考文献[10]でページを照合した）。

**[17]** Li, D., Levin, D. I. W., Matusik, W. and Zheng, C.: Acoustic Voxels: Computational Optimization of Modular Acoustic Filters, ACM Trans. Graphics, Vol. 35, No. 4, Article 88 (2016). DOI 10.1145/2897824.2925960
引く場所は2.2節と表1である。原典確認である。

**[18]** Fu, Y., Shen, V., Riera-Naranjo, V., Deng, B., Adams, A. and Hester, J.: SoundOff: Low-cost Passive Ultrasound Tags for Non-invasive and Non-Intrusive Smart Home Sensing, Proc. ACM Interact. Mob. Wearable Ubiquitous Technol., Vol. 9, No. 4, Article 174, pp. 1–32 (2025). DOI 10.1145/3770666
引く場所は2.2節と表1である。原典確認である。

**[19]** Reyes, G., Zhang, D., Ghosh, S., Shah, P., Wu, J., Parnami, A., Bercik, B., Starner, T., Abowd, G. D. and Edwards, W. K.: Whoosh: Non-Voice Acoustics for Low-Cost, Hands-Free, and Rapid Input on Smartwatches, Proc. ACM ISWC 2016, pp. 120–127 (2016). DOI 10.1145/2971763.2971765
引く場所は2.2節と表1である。原典確認である。**草稿の[32]は著者を「Reyes, G. et al.」と略しているが、10名の共著なので、投稿規定が許す範囲で全員を書くか、規定に従って略すかを決める必要がある。**

**[20]** Tejada, C., Fujimoto, O., Li, Z. and Ashbrook, D.: Blowhole: Blowing-Activated Tags for Interactive 3D-Printed Models, Proc. Graphics Interface 2018, pp. 122–128 (2018). DOI 10.20380/GI2018.18
引く場所は2.2節と表1である。原典確認である（この検証で予稿集の本文を取得して確かめた）。ページ範囲は予稿集の版面に印刷された122から128を採る。ACM Digital Libraryは131から137を掲げているので、注記するか、DOIだけを頼りにする。

**[21]** Tejada, C. E.: Print-and-Play: 3D-printed Interactive Objects Without Assembly or Calibration, Extended Abstracts of ACM CHI 2020, pp. 1–6 (2020). DOI 10.1145/3334480.3375025
引く場所は2.2節である。書誌確認である（この検証でCrossrefとSemantic Scholarに当たった）。

**[22]** Umetani, N., Panotopoulou, A., Schmidt, R. and Whiting, E.: Printone: Interactive Resonance Simulation for Free-form Print-wind Instrument Design, ACM Trans. Graphics, Vol. 35, No. 6, Article 184, pp. 184:1–184:14 (2016). DOI 10.1145/2980179.2980250
引く場所は2.3節である。原典確認である。**104個の目標周波数のうち4例だけが出せなかったという数値は本体のものであり、短縮版の「56個中53個」を混ぜないこと。**

**[23]** Ernoult, A., Vergez, C., Missoum, S., Guillemain, P. and Jousserand, M.: Woodwind instrument design optimization based on impedance characteristics with geometric constraints, J. Acoustical Society of America, Vol. 148, No. 5, pp. 2864–2877 (2020). DOI 10.1121/10.0002449
引く場所は2.3節である。書誌確認である。逆問題については Ernoult, A., Chabassier, J., Rodriguez, S. and Humeau, A.: Full waveform inversion for bore reconstruction of woodwind-like instruments, Acta Acustica, Vol. 5, Article 47 (2021), DOI 10.1051/aacus/2021038 を併記できる。**demakein については査読論文が存在しないので、脚注で http://www.logarithmic.net/pfh/design を示すにとどめること。**

**[24]** Dabin, M., Narushima, T., Beirne, S., Ritz, C. and Grady, K.: 3D Modelling and Printing of Microtonal Flutes, Proc. NIME 2016, pp. 286–290 (2016). https://nime.org/proc/nime2016_dabin/
引く場所は2.3節である。原典確認である。

**[25]** Schenker, L.: Pushbutton Calling with a Two-Group Voice-Frequency Code, Bell System Technical Journal, Vol. 39, No. 1, pp. 235–255 (1960). https://archive.org/details/bstj39-1-235
引く場所は2.4節である。原典確認である。

**[26]** ITU-T: Recommendation Q.23, Technical features of push-button telephone sets (1988年11月).
引く場所は2.4節である。書誌確認である（この検証で https://www.itu.int/rec/T-REC-Q.23/en に当たった）。

**[27]** ITU-T: Recommendation V.21, 300 bits per second duplex modem standardized for use in the general switched telephone network (1988年11月).
引く場所は2.4節である。書誌確認である（https://www.itu.int/rec/T-REC-V.21/en）。

**[28]** ITU-T: Recommendation T.30, Procedures for document facsimile transmission in the general switched telephone network (2005年9月).
引く場所は2.4節である。書誌確認である（https://www.itu.int/rec/T-REC-T.30/en）。

**[29]** Widmer, A. X. and Franaszek, P. A.: A DC-Balanced, Partitioned-Block, 8B/10B Transmission Code, IBM Journal of Research and Development, Vol. 27, No. 5, pp. 440–451 (1983). DOI 10.1147/rd.275.0440
引く場所は2.4節である。書誌確認である（この検証でCrossrefに当たった）。

**[30]** Gerganov, G.: ggwave（オープンソースソフトウェア）. https://github.com/ggerganov/ggwave
引く場所は2.4節である。原典確認である（`REFERENCES_TO_ADD.md` 220行から222行）。

**[31]** Lopp, J.: Metal Bitcoin Seed Storage Reviews. https://jlopp.github.io/metal-bitcoin-storage-reviews/
引く場所は2.5節である。**要確認である。** 閲覧日を添える必要がある。

**[32]** Bitcoin Wiki: Casascius physical bitcoins. https://en.bitcoin.it/wiki/Casascius_physical_bitcoins
引く場所は2.5節と4.4節である。**要確認である。** 閲覧日を添える必要がある。

**[33]** SatoshiLabs: SLIP-0039, Shamir's Secret-Sharing for Mnemonic Codes. https://github.com/satoshilabs/slips/blob/master/slip-0039.md
引く場所は2.5節、3.7節、4.2節である。原典確認である（`raw3/c6-security-soundness.md` が全文を読んでいる）。

**[34]** Blockchain Commons: BCR-2020-011, Sharded Secret Key Reconstruction (SSKR). https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2020-011-sskr.md
引く場所は2.5節である。原典確認である。

**[35]** Curr, L. O., Sneed, P. and Poelstra, A.: codex32: Checksummed SSSS-aware BIP32 seeds, Bitcoin Improvement Proposal 93, Applications layer, Informational, Draft, 作成2023年2月13日. https://github.com/bitcoin/bips/blob/master/bip-0093.mediawiki
引く場所は2.5節、3.5節、表1、6.2節である。原典確認である（この検証で本文を取得して見出しと検査符号の性能を確かめた）。

**[36]** Blockstream Research: codex32 参照実装および公式サイト. https://github.com/BlockstreamResearch/codex32 、https://secretcodex32.com/
引く場所は2.5節（回転円板による手計算と、実用への警告）、3.5節、6.2節である。原典確認である。**[35]と分けることが要点である。** 回転円板も実用への警告もBIP-93の本文には無い。

**[37]** SeedSigner Project: SeedQR and CompactSeedQR Specification (2022年1月22日初出、継続更新). https://github.com/SeedSigner/seedsigner/blob/dev/docs/seed_qr/README.md
引く場所は1.1節、2.5節、6.3節である。原典確認である。

**[38]** Jurgen（GitHubのアカウント名は cmd1982）: QR SafeShare – Split and protect secrets in QR codes (2025). https://github.com/cmd1982/qr-safeshare 、https://qrsafeshare.com
引く場所は1.1節、2.5節、貢献の第四点である。原典確認である。

**[39]** Naor, M. and Shamir, A.: Visual Cryptography, Advances in Cryptology — EUROCRYPT '94, Lecture Notes in Computer Science, Vol. 950, pp. 1–12 (1995). DOI 10.1007/BFb0053419
引く場所は2.5節と5.6節である。原典確認である（著者公開の全文 https://www.wisdom.weizmann.ac.il/~naor/PAPERS/vis.pdf）。

**[40]** Desmedt, Y., Hou, S. and Quisquater, J.-J.: Audio and Optical Cryptography, Advances in Cryptology — ASIACRYPT '98, Lecture Notes in Computer Science, Vol. 1514, pp. 392–404 (1998). DOI 10.1007/3-540-49649-1_31
引く場所は2.5節と5.6節である。抄録は確認済みであり、本文は有料のため未確認である。**復号には音響版がステレオ再生装置を、光学版がマッハ・ツェンダー干渉計を要するので、装置が要らない側に数えないこと。**

**[41]** 大川直也, 栃窪孝也: 視覚復号型秘密分散法を用いたパスワードの分散管理の提案, 情報処理学会論文誌デジタルプラクティス, Vol. 7, No. 2, pp. 35–50 (2026). https://ipsj.ixsq.nii.ac.jp/record/2009100/files/IPSJ-TDP0702007.pdf
引く場所は2.5節である。原典確認である。

**[42]** den Boer, B.: More Efficient Match-Making and Satisfiability: The Five Card Trick, Advances in Cryptology — EUROCRYPT '89, Lecture Notes in Computer Science, Vol. 434, pp. 208–217 (1990). DOI 10.1007/3-540-46885-4_23
引く場所は2.5節である。書誌確認である。国内の展開として、情報処理, 2026年5月号および6月号の特集「カードベース暗号とその展開」を併記できる。

**[43]** 伊藤優樹, 四方隼人, 水木敬明, 菅沼拓夫: 3Dプリンタによるオープン装置や特殊カードケースの作成と対称関数の秘密計算への適用, コンピュータセキュリティシンポジウム2023論文集, pp. 192–199 (2023). https://cir.nii.ac.jp/crid/1050579444484578048
引く場所は2.5節である。書誌確認である。

**[44]** Levine, H. and Schwinger, J.: On the Radiation of Sound from an Unflanged Circular Pipe, Physical Review, Vol. 73, No. 4, pp. 383–406 (1948). DOI 10.1103/PhysRev.73.383
引く場所は3.1節である。書誌確認である（この検証でCrossrefに当たった）。**端の補正の一次文献として、これを主に置くことを勧める。**

**[45]** 吉川茂: 正倉院尺八吹奏時の歌口端補正長さの推定, 情報処理学会研究報告 音楽情報科学, 2011-MUS-89, No. 1, pp. 1–5 (2011). https://ipsj.ixsq.nii.ac.jp/records/72682
引く場所は3.1節である。書誌確認である（この検証で情報処理学会電子図書館に当たった）。**[44]に添えて国内の一次文献として引く。**

**[46]** Smith, J. H. and Senturia, S. D.: Self-Consistent Temperature Compensation for Resonant Sensors with Application to Quartz Bulk Acoustic Wave Chemical Sensors, Proc. International Solid-State Sensors and Actuators Conference (TRANSDUCERS '95), Stockholm, Sweden, pp. 724–727, IEEE (1995). DOI 10.1109/SENSOR.1995.721934
引く場所は貢献の第三点と3.3節である。原典確認である（`raw3/c3-reference-resonator.md` が著者所属機関の公開原稿 https://www.sandia.gov/app/uploads/sites/145/2021/11/5_7SelfConsistent.pdf を精読し、この検証でCrossrefの書誌を照合した）。**"conventional sensing setup" という語が原文にあることが草稿175行の根拠である。**

**[47]** Goldman, N., Bertone, P., Chen, S., Dessimoz, C., LeProust, E. M., Sipos, B. and Birney, E.: Towards practical, high-capacity, low-maintenance information storage in synthesized DNA, Nature, Vol. 494, No. 7435, pp. 77–80 (2013). DOI 10.1038/nature11875
引く場所は3.4節である。原典確認である。**PubMed Centralの著者原稿にある別題名を引かないこと。**

**[48]** Shannon, C. E.: A Mathematical Theory of Communication, Bell System Technical Journal, Vol. 27, pp. 379–423 (1948).
引く場所は3.4節である。書誌確認である。制約付き系列の容量が行列式方程式の最大の実根の対数であることの出発点である。

**[49]** Marcus, B. H., Roth, R. M. and Siegel, P. H.: An Introduction to Coding for Constrained Systems（著者公開の教科書草稿、第5版）.
引く場所は3.4節である。**要確認である。** 教科書の草稿であるため、査読誌に載った形を引きたい場合は、同じ著者らによる Handbook of Coding Theory（1998年）の該当章に差し替える必要がある。版と入手先を投稿前に確定すること。

**[50]** Immink, K. A. S. and Cai, K.: Properties and Constructions of Constrained Codes for DNA-Based Data Storage, IEEE Access, Vol. 8, pp. 49523–49531 (2020). DOI 10.1109/ACCESS.2020.2980036（査読前版は arXiv:1812.06798）
引く場所は3.4節である。書誌確認である（この検証でarXivとCrossrefの両方に当たった）。**`REFERENCES_TO_ADD.md` の155行が書いている題名は誤りであり、そのまま写してはならない。** 第2章の2.5節に詳しく書いた。

**[51]** 中尾美月, 須藤壮一朗, 水野明哲, 高橋義典: 尺八のCT画像の輝度値に基づく3Dモデルの内径補正と付加製造による復元評価, 情報処理学会研究報告 音声言語情報処理, 2026-SLP-159, No. 24, pp. 1–6 (2026). https://ipsj.ixsq.nii.ac.jp/records/2007593
引く場所は4.1節である。書誌確認である。**内径の復元になお差が残るという原典の限界を併記すること。**

**[52]** Laxton, B., Wang, K. and Savage, S.: Reconsidering Physical Key Secrecy: Teleduplication via Optical Decoding, Proc. ACM CCS 2008, pp. 469–478 (2008). DOI 10.1145/1455770.1455830
引く場所は4.1節である。原典確認である（`raw/11-physical-security-steganography.md` の221行が本文で試作系の名前がSneakeyであることを確認している）。

**[53]** Burgess, B., Wustrow, E. and Halderman, J. A.: Replication Prohibited: Attacking Restricted Keyways with 3D-Printing, Proc. 9th USENIX Workshop on Offensive Technologies (WOOT '15) (2015). https://www.usenix.org/conference/woot15/workshop-program/presentation/burgess
引く場所は4.1節である。原典確認である。

**[54]** Halevi, T. and Saxena, N.: On pairing constrained wireless devices based on secrecy of auxiliary channels: the case of acoustic eavesdropping, Proc. ACM CCS 2010, pp. 97–108 (2010). DOI 10.1145/1866307.1866319
引く場所は4.1節である。書誌確認である。

**[55]** Putz, F., Álvarez, F. and Classen, J.: Acoustic integrity codes: secure device pairing using short-range acoustic communication, Proc. ACM WiSec 2020, pp. 31–41 (2020). DOI 10.1145/3395351.3399420
引く場所は4.1節である。書誌確認である（この検証でCrossrefに当たった）。

**[56]** Johnston, R. G.: Tamper-Indicating Seals for Nuclear Disarmament and Hazardous Waste Management, Science & Global Security, Vol. 9, pp. 93–112 (2001). DOI 10.1080/08929880108426490
引く場所は4.1節である。原典確認である。**旧稿の[16]（2003年のロスアラモス国立研究所の報告）から差し替えること。**

**[57]** Appel, A. W.: Security Seals on Voting Machines: A Case Study, ACM Trans. Information and System Security, Vol. 14, No. 2, Article 18 (2011). DOI 10.1145/2019599.2019603
引く場所は4.1節である。原典確認である。

**[58]** Wolfe, J. M., Horowitz, T. S. and Kenner, N. M.: Rare items often missed in visual searches, Nature, Vol. 435, pp. 439–440 (2005). DOI 10.1038/435439a
引く場所は4.1節である。書誌確認である（この検証でCrossrefに当たった）。

**[59]** Crawford, V. P. and Iriberri, N.: Fatal Attraction: Salience, Naiveté, and Sophistication in Experimental "Hide-and-Seek" Games, American Economic Review, Vol. 97, No. 5, pp. 1731–1750 (2007). DOI 10.1257/aer.97.5.1731
引く場所は4.1節である。書誌確認である（この検証でCrossrefに当たった）。

**[60]** National Institute of Standards and Technology: Recommendation for Password-Based Key Derivation, Part 1: Storage Applications, NIST Special Publication 800-132 (2010). DOI 10.6028/NIST.SP.800-132
引く場所は4.2節（鍵導出関数を強くしても費用が定数倍になるだけであること）である。原典確認である（`raw3/c6-security-soundness.md` の109行が Appendix A.2.2 の原文を引いている）。

**[61]** National Institute of Standards and Technology: Transitioning the Use of Cryptographic Algorithms and Key Lengths, NIST Special Publication 800-131A Revision 2 (2019).
引く場所は4.2節（112ビットという下限）である。原典確認である（`raw3/c6-security-soundness.md` の83行）。**現在この数値には出典が付いていないので、必ず足すこと。**

**[62]** Chhetri, S. R., Canedo, A. and Al Faruque, M. A.: Confidentiality Breach Through Acoustic Side-Channel in Cyber-Physical Additive Manufacturing Systems, ACM Trans. Cyber-Physical Systems, Vol. 2, No. 1, Article 3, pp. 1–25 (2018). DOI 10.1145/3078622（会議版は Acoustic Side-Channel Attacks on Additive Manufacturing Systems, Proc. ACM/IEEE ICCPS 2016, pp. 1–10, DOI 10.1109/ICCPS.2016.7479068）
引く場所は4.3節である。書誌確認である。**草稿255行が「2016年に」と書いているので、会議版を併記するか、年の記述を論文誌版に合わせること。**

**[63]** Jamarani, A., Tu, Y. and Hei, X.: Practitioner Paper: Decoding Intellectual Property: Acoustic and Magnetic Side-channel Attack on a 3D Printer, EAI SmartSP 2024. arXiv:2411.10887
引く場所は4.3節である。書誌確認である。

**[64]** Chhetri, S. R., Barua, A., Faezi, S., Regazzoni, F., Canedo, A. and Al Faruque, M. A.: Tool of Spies: Leaking your IP by Altering the 3D Printer Compiler, IEEE Trans. Dependable and Secure Computing, Vol. 18, pp. 667–678 (2021). DOI 10.1109/TDSC.2019.2923215
引く場所は4.3節である。書誌確認である。

### 4.2 追加を勧めるもの

以下は現在の草稿には番号が無いが、記録が「引くべきである」と述べているか、出典の無い記述を支えるために必要なものである。

**[65]** Daehnert, J. (PhoneDesigner): Flat Pocket Whistle, Printables model 495173 (2023). https://www.printables.com/model/495173-flat-pocket-whistle
ならびに dp makes: Whistle Pan flute, MakerWorld model 13026 (2023). https://makerworld.com/en/models/13026-whistle-pan-flute
引く場所は2.3節の末尾である。「10万回規模でダウンロードされている」という数値の出所になる。原典確認である（`REFERENCES_TO_ADD.md` 305行と306行。ダウンロードは97,000件と記録されている）。閲覧日を添えること。

**[66]** Shamir, A.: How to Share a Secret, Communications of the ACM, Vol. 22, No. 11, pp. 612–613 (1979). DOI 10.1145/359168.359176
引く場所は3.7節である。秘密分散を論の中心に据えながら原典を引かないのは不自然である。旧稿では[18]として持っていた。

**[67]** Wang, C., Wang, J., Zhou, M., Pham, V., Hao, S., Zhou, C., Zhang, N. and Raviv, N.: Secure Information Embedding in Forensic 3D Fingerprinting, arXiv:2403.04918 (2024年、2025年2月改訂). https://arxiv.org/abs/2403.04918
引く場所は貢献の第四点（1.3節）と4章の冒頭である。`PAPER_REVISION.md` の110行と129行が、この文献の存在を注記せよと明示している。**「この分野で脅威モデルを持つのは初めてである」と書けない根拠でもある。**

**[68]** 栗原一貴, 板谷あかり, 植村あい子, 北原鉄朗: Picognizer: 電子音の検出および認識のためのJavaScriptライブラリ, WISS 2017 (2017). https://www.wiss.org/WISS2017Proceedings/oral/17.pdf
引く場所は3.5節の経路1、あるいは5.3節である。`REFERENCES_TO_ADD.md` の344行が自己引用の候補として挙げている。

**[69]** Jiang, W., Yu, D., Wang, C., Sarsenbayeva, Z., van Berkel, N., Goncalves, J. and Kostakos, V.: Near-infrared Imaging for Information Embedding and Extraction with Layered Structures, ACM Trans. Graphics, Vol. 42, No. 1, pp. 1–26 (2022). DOI 10.1145/3533426
引く場所は2.1節、あるいは3.7節である。`REFERENCES_TO_ADD.md` の244行が「造形物への情報埋め込みの分野で秘密分散への言及が皆無であると書くと誤りになる」と警告している。現在の草稿はその誤りを犯していないので必須ではないが、3.7節で秘密分散との組み合わせを論じるときに引いておくと守りが固くなる。

### 4.3 旧番号と新番号の対応

| 草稿の番号 | 新しい番号 | 文献 |
| --- | --- | --- |
| 1 | 20 | Blowhole |
| 2 | 17 | Acoustic Voxels |
| 3 | 2 | AirCode |
| 4 | 1 | InfraStructs |
| 5 | 3 | LayerCode |
| 6 | 4 | G-ID |
| 7 | 14 | Acoustic Barcodes |
| 8 | 15 | Lamello |
| 9 | 16 | Acoustruments |
| 10 | 6 | Seedmarkers |
| 11 | 5 | StructCode |
| 12 | 33 | SLIP-0039 |
| 13 | 34 | SSKR |
| 14 | 32 | Casascius |
| 15 | 31 | 金属板の比較ページ |
| 16 | 56 | Johnston（2001年版に差し替え） |
| 17 | 削除 | Eskandari ら（本文から落ちた） |
| 18 | 66 | Shamir（3.7節で引き直す） |
| 19 | 27 | ITU-T V.21 |
| 20 | 28 | ITU-T T.30 |
| 21 | 26 | ITU-T Q.23 |
| 22 | 29 | 8B/10B |
| 23 | 削除 | Audio Networking（本文から落ちた） |
| 24 | 7 | AnisoTag |
| 25 | 8 | InfraredTags |
| 26 | 9 | InfoPrint |
| 27 | 10 | 上平さんらの系譜 |
| 28 | 11 | 久保さんら |
| 29 | 12 | 宮武さんら（interiqrに差し替え） |
| 30 | 13 | DNA-of-things |
| 31 | 18 | SoundOff |
| 32 | 19 | Whoosh |
| 33 | 21 | Print-and-Play |
| 34 | 22 | Printone |
| 35 | 23 | openwind（demakeinは脚注へ） |
| 36 | 24 | Dabin ら |
| 37 | 25 | Schenker |
| 38 | 30 | ggwave |
| 39 | 35 と 36 | codex32（標準文書と参照実装に分割） |
| 40 | 37 | SeedQRとCompactSeedQR |
| 41 | 38 | QR SafeShare |
| 42 | 39 | 視覚暗号 |
| 43 | 40 | 音響暗号と光学暗号 |
| 44 | 41 | 大川さんと栃窪さん |
| 45 | 42 | カードベース暗号 |
| 46 | 43 | 伊藤さんら |
| 47 | 44 と 45 | 端の補正（新設） |
| 48 | 46 | Smith と Senturia |
| 49 | 47 | Goldman ら |
| 50 | 48、49、50 | 制約符号の容量（3件に分割） |
| 51 | 51 | 中尾さんら |
| 52 | 52 | Sneakey |
| 53 | 53 | Burgess ら |
| 54 | 54 | Halevi と Saxena |
| 55 | 55 | Putz ら |
| 56 | 57 | Appel |
| 57 | 58 | Wolfe ら |
| 58 | 59 | Crawford と Iriberri |
| 59 | 60 | NIST SP 800-132 |
| 60 | 62 | Chhetri ら（2018年） |
| 61 | 63 | Jamarani ら |
| 62 | 64 | Tool of Spies |
| （新設） | 61 | NIST SP 800-131A Rev. 2 |
| （新設） | 65 | モデル共有基盤の先行実装 |
| （新設） | 67 | Wang ら（脅威モデルの先例） |
| （新設） | 68 | Picognizer（自己引用） |
| （新設） | 69 | Jiang ら（層構造と近赤外） |

---

## 5. 確かめて問題が無かったこと

以下は、どう確かめたかとあわせて記す。

**Blowholeの数値。** 草稿95行の「6種類なら利用者非依存で98パーセント、上限は1つの物体あたり9個」は、予稿集の本文を直接に取得して確かめた。原文は "with up to six cavities, the system achieves a high user-independent performance of 98%" と "Our system enables high performance for up to nine different blowholes" である。ヘルムホルツ共鳴を使うという記述も本文にある。表1の「約2.6 bit相当」は6個を2の対数で数えた2.585と整合する。

**Whooshに関する記述。** 草稿89行から93行の管長の式 L = 14.956 × 2^(i/12)、8本の閉管、利用者非依存で79.7パーセント、再現性のために管長を定数として公開していることは、`REFERENCES_TO_ADD.md` の16行と `raw3/c5-semitone-concept.md` の38行から56行が原典から引いた原文と一致する。ページ範囲120から127は、この検証でBlowholeの参考文献[16]からも照合できた。

**AirCodeとInfraredTagsに関する記述。** 草稿73行から75行の「外部に開口をいっさい持たない」「撮像に3分から4分」「プロジェクタと産業用の単色カメラと交差偏光板」「均質で半透明な材料」「重さ132グラムの近赤外撮像モジュール」「サーバ側で画像処理」「最大250センチメートル」「4×4のマーカーで平均6ミリ秒、二次元コードで平均14ミリ秒」「スプールごとの再較正」は、いずれも `raw3/c1-optical-hidden.md` が著者公開版の本文から引いた原文と一致する。

**Acoustic Barcodesに関する記述。** 草稿87行の「誤り訂正後の実効データ量として12ビット（4096通り）」と、183行の「0の連続を禁じて区切りの信号を復元できるようにしており」は、`raw2/f6-key-numbers.md` の105行が引く原文 "we constrain the space of permissible bit sequences to exclude sequences with two consecutive 0 bits. This better assures that a 'clock signal' can be ..." と一致する。

**InfoPrintに関する記述。** 草稿77行の「安価な市販のプリンタと一般的なフィラメント」「人が手で触れて温めたあとにサーマルカメラで読む」は、`raw3/c2-thermal-and-viewangle.md` の40行が確認した hand-warming の記述と一致する。

**DNA-of-thingsに関する記述。** 草稿81行の「老眼鏡のレンズに1.4メガバイト」「著者自身が用途としてステガノグラフィを挙げている」「読み出しは破壊的で次世代シーケンサを要する」は、`raw3/c4-dna-of-things.md` の47行から51行、107行から114行、77行から92行が抄録の原文で確認したとおりである。

**SoundOffに関する記述。** 草稿87行の「1277通りの候補から選んだ15個を区別している」は、`REFERENCES_TO_ADD.md` の60行と一致する。**「1277通りを10.3ビットと換算するのは誤りである」という記録の警告に、草稿は従っている。**

**Printoneに関する記述。** 草稿101行の「104個の目標周波数のうち、出せなかったのは4例だけ」「指孔5個の作例は1つの物体から9音を出す」、105行の「吹く速さの変化は10ヘルツの誤差を容易に補償できる」は、`REFERENCES_TO_ADD.md` の25行と26行の確定事実と一致する。**短縮版にしかない「56個中53個」を使っていない点も正しい。**

**AnisoTagの三者比較。** 草稿151行と351行の「AnisoTagは51ビット、LayerCodeは25ビット、acoustic barcodeは40ビット」「寸法はクレジットカードと同一」は、`REFERENCES_TO_ADD.md` の229行と一致する。

**Smith と Senturia。** 依頼にあった[48]の書誌は、`raw3/c3-reference-resonator.md` の15行から18行にあり、この検証でCrossref（https://api.crossref.org/works/10.1109/sensor.1995.721934）でも照合した。題名、著者、TRANSDUCERS '95、724から727ページ、IEEE、1995年がすべて一致する。草稿175行の「1995年の文献 [48] は既にこれを『従来の構成』と呼んでいる」も、原文 "The temperature compensation scheme uses the conventional sensing setup of two resonators" と一致する。

**QR SafeShareの引用。** 草稿121行の「素早い走査や気づかれない走査を防ぎ、許可の無い読み出しに必要な労力を上げる」という趣旨は、`REFERENCES_TO_ADD.md` の51行が説明文から確認した一文と一致する。「日用品への偽装は謳っておらず」という草稿の記述も、記録の52行と一致する。

**SLIP-39の否認可能性。** 草稿249行の「パスフレーズが正しいかを検証する方法を意図的に持たない」は、`REVIEW_AND_REPOSITIONING.md` の193行および `PAPER_REVISION.md` の191行と一致する。

**造形機の側チャネルの数値。** 草稿255行の86パーセント、98.80パーセント、39パーセントは、`REFERENCES_TO_ADD.md` の68行、75行、90行と一致する。

**封印と探索の数値。** 草稿241行の「投票機の錠が平均13秒」「標的の出現率が低いほど見落としが増える」「隠す側の選択が体系的に予測されうる」は、`REFERENCES_TO_ADD.md` の271行から273行と一致する。Wolfe らの書誌とCrawford と Iriberri の書誌は、この検証でCrossrefでも照合した。

**鍵の複製の2件。** 草稿237行の「写真から物理鍵の刻みを復元する研究」「3Dプリンタで制限付きの鍵を複製する研究」は、それぞれ Laxton ら（CCS 2008、Sneakey）と Burgess ら（WOOT '15）に対応し、`raw/11-physical-security-steganography.md` の221行と79行の記述と一致する。

**音響チャネルの秘匿の2件。** 草稿239行は、Halevi と Saxena（CCS 2010）および Putz ら（WiSec 2020）に対応する。`SURVEY.md` の237行と `00-digest.md` の658行が同じ位置づけを与えている。

**隣接同記号禁止の先例。** 草稿183行の「各桁を直前に使った塩基とは異なる3塩基のいずれかへ写している」は、`REFERENCES_TO_ADD.md` の149行が引く原文 "by replacement of each trit with one of the three nucleotides different from the previous one used, ensuring no homopolymers were generated" と一致する。

**国際電気通信連合の勧告の年。** 記録が積み残していた確認を済ませた。第3章の3.7節に書いたとおり、旧稿の年はすべて正しい。

---

## 6. 確認できなかったこと

正直に記す。

- Immink と Cai の論文の本文を読んでいない。書誌は arXiv と Crossref で確定したが、特性方程式と表1の内容は確かめていない。`REFERENCES_TO_ADD.md` が書いている「表1のm=1の欄が log2 3 = 1.5850 である」がどちらの論文の表かは未確定である。
- Marcus、Roth、Siegel の教科書草稿の版と入手先を確認していない。定理3.4の番号が第5版のものかどうかも確かめていない。
- Desmedt らの1998年の論文の本文を読んでいない。判定は抄録の記述にもとづく。ただし抄録の "one just plays two shares on a stereo system" と "The Mach-Zehnder interferometer is used as the decryption machine" だけで、第2章の2.1節の指摘は成り立つ。
- InfoPrint の出版版の著者の並び順を確認していない。査読前版の8名に Jing Wei が加わって9名になったことまでが記録にある。
- Print-and-Play が博士課程のための投稿区分であるかどうかを確認できなかった。Crossref にも Semantic Scholar にもその記載が無い。
- 上平さんら、Casascius、金属板の比較ページ、SoundOff の出版版など、ACM Digital Library と IEEE Xplore に本体がある文献の版面そのものは見ていない。記録も同じ制約のもとで著者公開版や Crossref を用いている。
- Blowhole のページ範囲について、ACM Digital Library が131から137を掲げる理由を確認していない。予稿集の版面の数字が122から128であることは、この検証で直接に確かめた。
