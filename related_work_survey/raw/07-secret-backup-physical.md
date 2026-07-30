# 秘密分散と秘密情報の物理的バックアップの実務と標準

調査担当の切り口は、暗号資産のリカバリーシードや暗号鍵を物理的に保管するための方式・製品・標準である。既知として与えられたSLIP-39、SSKR、Casascius物理ビットコイン、金属製シード保管製品、Shamirの秘密分散の外側を重点的に洗った。調査は2026年7月30日に実施した。Web検索APIの予算が枯渇していたため、検索はDuckDuckGoのHTML版・Bing・OpenAlex・Crossref・dblp・CiNii Research・J-STAGE・情報処理学会電子図書館の各エンドポイントをWebFetchで直接叩く方法で行い、書誌はできる限り一次資料（規格本文、提案本文、RFC本文、著者の業績ページ、出版社のメタデータ、学会リポジトリ）に当たって確認した。取得したPDFはローカルでテキスト抽出して本文を読んだものがある。

## この切り口の要約

この分野の実務は、大きく三つの層に分かれていることが分かった。第一に、秘密を人間可読な語や文字へ写す符号化の標準がある。BIP-39の2048語リスト、SLIP-39の1024語リスト、Blockchain CommonsのBytewordsの256語リスト、そして暗号資産以前からあるRFC 1751とRFC 2289の英単語符号化がここに属する。第二に、その符号化された秘密を複数の担体へ割る方式がある。SLIP-39とSSKRに加えて、BIP-93として提案されたcodex32、CoinkiteのSeed XOR、Armoryの断片バックアップ、Cypherock X1、Ledger Recover、HashiCorp Vaultの封印鍵、決済業界のPCI PIN要件、ICANNのルート鍵署名鍵の儀式などが実在する。第三に、割った断片を物理的にどう保管し運ぶかの指針がある。ここでは金属板への打刻、封緘袋、貸金庫、複数の宅配経路の分離といった、いずれも「明らかに秘密の保管物に見える」担体が標準になっている。

最も注意すべき発見はcodex32（BIP-93）である。これは紙の円板（ヴォルヴェル）と対照表だけでShamirの秘密分散の分割と復元、およびBCH誤り訂正符号による検査を人手で行う方式であり、電源も計算機も使わない物理バックアップに誤り訂正符号を載せるという発想がすでに標準提案として存在する。CipherFluteが主張しうる「誤り訂正付きの電源不要な物理的秘密保管」という一般論は、この一点で新規性を失う。ただしcodex32の担体は印刷された文字列であり、日用品への偽装も、音による読み出しも扱っていない。

偽装や隠蔽の扱いについては、明確な断層があった。データ層の偽装（合言葉による囮ウォレット、各断片自体が正当なシードに見えるSeed XOR、強要時の囮PIN）は複数の製品が正面から実装している。しかし担体そのものを日用品に偽装するという設計は、学術文献にも標準にも製品にも見つからなかった。実務の指針はむしろ逆で、封緘袋の連番照合や改ざん痕の点検といった「見えること・検査できること」を要件にしている。ここがCipherFluteの立ち位置を最も明瞭にする差分である。

## 新規性への脅威が大きい文献

### 1. codex32: Checksummed SSSS-aware BIP32 seeds（BIP-93）

- 題名: codex32: Checksummed SSSS-aware BIP32 seeds（Bitcoin Improvement Proposal 93）
- 著者: Leon Olsson Curr、Pearlwort Sneed（いずれも仮名）、Andrew Poelstra
- 発表: Bitcoin Improvement Proposals、Informational、Draft、2023年2月13日作成
- 確認先URL: https://github.com/bitcoin/bips/blob/master/bip-0093.mediawiki 、 https://bips.dev/93/ 、 https://secretcodex32.com/ 、 https://github.com/BlockstreamResearch/codex32 、 https://blog.blockstream.com/codex32-a-shamir-secret-sharing-scheme/ 、数学的補遺は https://secretcodex32.com/docs/2023-08-23--math.pdf

内容の要約を述べる。codex32は、BIP-32のマスターシードをbech32のアルファベットで符号化し、そこにBCH誤り訂正符号による検査符号を付けた形式である。仕様本文は、すべての計算が単純な対照表だけで行えるので、検査符号の計算と検証、シードの分割と復元を紙と鉛筆だけで完結できると明言している。公式サイトは印刷用の小冊子を配布しており、厚紙に印刷して組み立てる回転円板（ヴォルヴェル）が5ページ、検査符号の計算用紙と断片の変換用紙が付属する。数学的補遺（著者はPearlwort Snead、2023年8月23日版）は、加算ホイール、融合変換ホイール、復元用計算尺、BCH符号とcodex32検査符号、そして秘密分散の各章から成る。Blockstreamのブログ記事（Andrew Poelstra、2023年9月7日）は、電子計算機は速すぎて人間が動作を確かめられないという動機を述べ、手計算での検証に30分から60分かかり、最初は二度行うべきだと書いている。仕様は、長期に眠らせる鍵については、検査符号を人手で確かめられること自体に価値があり、秘密情報を新しい機材に晒さずに毎年の健全性確認ができると述べている。

CipherFluteとの関係を述べる。CipherFluteは、電源も電子部品も持たない物理的な担体に秘密を載せ、Reed–Solomon符号で誤り訂正を掛けるという構成を取る。codex32は同じ「電源不要の物理担体」「誤り訂正符号」「Shamirの秘密分散」という三点を、紙という担体で先に実現している。読み出しに関しても、codex32は人間の目と手だけで完結し、CipherFluteは吹く動作と音高計測を要する点で、むしろcodex32のほうが機材依存が少ない。

脅威の度合いは高である。理由は、CipherFluteが「電源不要の物理媒体に誤り訂正付きで秘密を格納すること」を新規性として掲げる場合、その一般的主張はcodex32によって先取りされているからである。査読者がこの提案を知っていれば、差分は音響チャネルと日用品への偽装だけに絞られるため、論文の主張の言い方を先に修正しておく必要がある。

### 2. Seed XOR（Coinkite / COLDCARD）

- 題名: Seed XOR
- 著者: Coinkite社（COLDCARDハードウェアウォレットの開発元）
- 発表: 製品機能および仕様解説（年次は仕様ページに明記されていないが、COLDCARDファームウェアに実装済み）
- 確認先URL: https://seedxor.com/ 、 https://coldcard.com/docs/ 、 https://coldcard.com/docs/seedxor/

内容の要約を述べる。Seed XORは、1つの12語または24語のBIP-39シードを、排他的論理和によって2つ以上の部分に分ける方式である。分けた各部分は、それ自体が正当なBIP-39シード語列になっている。閾値方式ではなくN個すべてが必要な方式であり、1つでも欠ければ復元できない。仕様ページは、各部分が元の秘密と見た目も振る舞いも同じであり、見つかった語列のどの組み合わせも完全に機能するウォレットになるので、強要への備えとして優れていると述べている。つまり各断片に囮の資金を置いておけば、断片を奪った者はそれを本物の財布だと信じることができる。

CipherFluteとの関係を述べる。CipherFluteは「担体が明らかに秘密の保管物に見えてしまう」問題を、日用品への物理的な偽装で解こうとしている。Seed XORは同じ問題を、データ層の偽装で解いている。すなわち断片を隠すのではなく、断片が別の無害な秘密に見えるようにする。両者は解の層が違うだけで、動機はまったく同じである。

脅威の度合いは中である。理由は、偽装によって探索コストを上げるという発想がすでに実務に存在することを示すため、CipherFluteが「偽装という着眼自体が新しい」とは書けなくなるからである。担体そのものを日用品に変える点は依然として差分として残るので、主要な主張は崩れない。

### 3. SeedQR および CompactSeedQR（SeedSigner）

- 題名: SeedQR Documentation および CompactSeedQR Specification
- 著者: SeedSignerプロジェクト（開発者コミュニティ）
- 発表: SeedSignerリポジトリ内の仕様文書（継続更新）
- 確認先URL: https://github.com/SeedSigner/seedsigner/blob/dev/docs/seed_qr/README.md

内容の要約を述べる。SeedQRは、BIP-39の各語を語彙表の索引番号（0から2047）へ写し、4桁ゼロ詰めで連結した数字列を数字モードの二次元コードに収める形式である。12語なら48桁となり25×25のコードに収まる。CompactSeedQRは索引を11ビットの生の二進で詰め、検査ビット分を省くことで12語を21×21まで縮める。仕様は、コードが十分小さいので手で書き写せることを設計目標に掲げ、金属板に穴を打って二次元コードを転写した実例の写真を載せている。CompactSeedQRにすると手打ちの作業量が35パーセントから40パーセントほど減るとも述べている。標準のSeedQRは数字列がそのまま読めるので、専用の道具がなくても語彙表を引けば人手で復号できる。

CipherFluteとの関係を述べる。二次元コードで鍵を運ぶ方式の代表例であり、しかも二次元コードは規格上Reed–Solomon符号を内蔵している。したがって「Reed–Solomon符号で守られた物理的なシードのバックアップを、電源なしの担体に打刻する」という実務は、金属板に打ったCompactSeedQRとしてすでに存在する。CipherFluteの符号設計（スロット化した音高の系列にReed–Solomonを掛ける）は、二次元コードの符号設計と役割が重なる。

脅威の度合いは中である。理由は、誤り訂正符号を物理担体に載せる実務が既にあることを示すからである。一方で、二次元コードは明らかに機械可読な模様であって日用品には見えず、読み出しにカメラが要る点は差分として残る。

### 4. Of Secrets and Seedphrases: Conceptual Misunderstandings and Security Challenges for Seed Phrase Management among Cryptocurrency Users

- 題名: Of Secrets and Seedphrases: Conceptual Misunderstandings and Security Challenges for Seed Phrase Management among Cryptocurrency Users
- 著者: Farida Eleshin、Qi Sun、Mengzhe Ye、Sauvik Das、Jason I. Hong（カーネギーメロン大学）
- 発表: CHI Conference on Human Factors in Computing Systems（CHI '25）、2025年、横浜、全19ページ
- 確認先URL: https://doi.org/10.1145/3706598.3713209 （本文PDFは https://sauvik.me/papers/63/serve から取得して読んだ）

内容の要約を述べる。20名への半構造化面接と643名への調査を組み合わせた混合手法の研究である。回答者の43パーセントしかリカバリーフレーズの画像を正しく見分けられず、多くがフレーズを再発行できると誤解していた。バックアップ方法としては紙が最多で39パーセントであり、紙は最も安全とも最も便利とも評価されていた。31パーセントはクラウドに保存していた。面接では、複数箇所へ分割して保管していたのは20名中1名（P8）だけであった。相続や死亡時の備えをしている者は少数にとどまった。本文には隠蔽やステガノグラフィに関する記述はなく、参加者の工夫は「個人的な日記に書く」「暗号化する」といった水準にとどまっていた。

CipherFluteとの関係を述べる。CipherFluteの動機づけ（物理バックアップは紙が主流で、分散保管はほとんど実践されていない）を実データで裏づける論文である。同時に、実利用者が偽装や隠蔽をほぼ行っていないことの証拠にもなるため、CipherFluteの狙いが実務の空白を突いていることを示せる。

脅威の度合いは中である。理由は、新規性を脅かすというより、引用しないと動機づけの根拠が弱くなる位置にあるからである。CHI 2025という近接分野の最新の実証研究であり、査読者が知っている可能性が高い。

### 5. PCI PIN Security Requirements（決済業界における鍵成分の物理配送の要件）

- 題名: Payment Card Industry (PCI) PIN Security Requirements, Version 2.0
- 著者: PCI Security Standards Council
- 発表: 2014年12月（初版は2011年10月）
- 確認先URL: https://listings.pcisecuritystandards.org/documents/PCI_PIN_Security_Requirements_v2.pdf （PDFを取得して本文を読んだ）

内容の要約を述べる。この要件は、平文の鍵成分を人間が物理的に運ぶ場合の作法を細かく規定している。要件6-3は、印刷した鍵成分は目隠し封筒の中で印刷するか印刷直後に封をし、担当者が自分の成分だけを見られること、改ざんが目視で検出できることを求めている。要件6-6は、鍵成分を口頭で伝えること、留守番電話に残すこと、ファクスや電子メールで送ること、改ざん検知可能な包装なしで運ぶこと、手順書に書き込むこと、機器に貼り付けることを明示的に禁じている。要件8-1と8-2は、成分を2つ以上に分けて別々の伝送経路（別々の宅配業者など）で送ること、Shamirのような公認の秘密分散方式を使うm-of-n方式では1人が閾値未満の断片しか触れないようにすることを求めている。要件9-1から9-5は、連番の付いた改ざん検知可能な封緘袋を使い、受領時に連番を別経路で照合し、開封前に改ざん痕を点検することを求めている。参照規格としてANSI X9.24パート1・パート2、ISO 11568、ISO 13491、NIST SP 800-57が挙げられている。

CipherFluteとの関係を述べる。「秘密を複数の物体に分けて別々に保管・輸送する」という運用の、最も成熟した産業標準である。注目すべきは設計思想が正反対である点で、この標準は担体を隠すのではなく、連番と改ざん痕によって「見えること・検査できること」を要件にしている。CipherFluteが偽装を選ぶ理由（強要や捜索に対する探索コストの引き上げ）と、この標準が可視性を選ぶ理由（内部不正の抑止と監査可能性）を対比させると、脅威モデルの差が鮮明になる。

脅威の度合いは中である。理由は、分散保管の実務指針としてこれを外すと「実務の指針を調べた」と言えなくなるからである。担体の偽装には触れていないので、CipherFluteの主張を直接崩すものではない。

### 6. DNSSECルート鍵署名鍵の運用実務（ICANN / IANA）

- 題名: DNSSEC Practice Statement for the Root Zone KSK Operator（第8版）および関連する鍵儀式手順書
- 著者: Root Zone KSK Operator（ICANN / Public Technical Identifiers）
- 発表: 2025年4月14日発効（儀式は2010年から2026年まで63回の記録が公開されている）
- 確認先URL: https://www.iana.org/dnssec/procedures 、 https://www.iana.org/dnssec/procedures/ksk-operator/ksk-dps-20250414.html 、 https://www.iana.org/dnssec/ceremonies

内容の要約を述べる。ルート鍵署名鍵の運用は、最低4階層の物理的な区画を設け、下位の階層を通らないと上位へ入れない構造にしている。すべての入退室は記録され、録画される。ハードウェアセキュリティモジュールは改ざん検知袋、施錠された金庫や保管庫で守られる。暗号担当者はそれぞれ個別の貸金庫を持ち、そこに個別の識別番号を付けた改ざん検知袋で認証情報を保管する。鍵の起動には7名の暗号担当者のうち3名の資格情報が必要である。災害復旧のために鍵の暗号化複製を可搬媒体に取って施設間で運ぶが、その暗号化鍵は7名の復旧鍵保持者のうち5名が必要な閾値方式で守られ、保持者は地理的に分散し、それぞれ改ざん検知包装で保管する。

CipherFluteとの関係を述べる。世界で最も監査された「秘密を物理的に分割して複数の人と場所へ預ける」運用の実例である。CipherFluteが想定する家庭内の秘密分散運用（複数の日用品に断片を仕込む）の、対極にある重量級の運用として引用できる。ここでも担体はスマートカードと封緘袋であり、偽装の発想はまったく現れない。

脅威の度合いは中である。理由は、閾値方式による物理的な鍵バックアップが現実に稼働していることを示す最良の事例であり、背景として引くだけでなく、CipherFluteの脅威モデル（秘匿は秘密分散に負わせる）の妥当性を支える論拠にもなるからである。

### 7. Visual Cryptography（Naor and Shamir）と視覚復号型秘密分散のパスワード応用（大川・栃窪）

- 題名1: Visual Cryptography
- 著者1: Moni Naor、Adi Shamir
- 発表1: Advances in Cryptology — EUROCRYPT '94、Lecture Notes in Computer Science、pp. 1–12、1994年（Springer）
- 確認先URL1: https://dblp.org/rec/conf/eurocrypt/NaorS94.html （DOIは10.1007/BFb0053419）
- 題名2: 視覚復号型秘密分散法を用いたパスワードの分散管理の提案（英題 Visual Secret Sharing Schemes for Passwords）
- 著者2: 大川直也、栃窪孝也
- 発表2: 情報処理学会論文誌デジタルプラクティス、第7巻第2号、pp. 35–50、2026年
- 確認先URL2: https://ipsj.ixsq.nii.ac.jp/records/2009100

内容の要約を述べる。Naor と Shamir の視覚復号型秘密分散は、秘密の画像を複数の透明シートに分け、シートを重ね合わせるだけで人間の視覚が復号を行う方式である。計算機も計算も要らず、閾値未満のシートからは情報が漏れない。大川と栃窪の論文は、生体認証が使えない場面でのパスワード保護を課題とし、視覚復号型秘密分散を画像に適用してパスワードを分散管理する方式を提案し、オーバーヘッドプロジェクタ用シートとスマートフォンを用いて実用性を評価している。復号が画像の重ね合わせだけで済み、複雑な計算を要さないことを利点として挙げている。大川は同じ主題で日本大学に博士論文を提出している（https://nihon-u.repo.nii.ac.jp/records/2004470 ）。

CipherFluteとの関係を述べる。CipherFluteの実装のひとつに「2枚そろって初めてハートが現れるカード」がある。これは事実上、2-of-2の視覚的な秘密分散の演出であり、視覚復号型秘密分散の系譜に直接つながる。また「電源も計算機もなしに人間の感覚だけで秘密を復号する」という点で、音を使うCipherFluteの最も近い先行概念である。感覚のモダリティが視覚か聴覚かという違いが差分になる。

脅威の度合いは中である。理由は、CipherFluteのカード実装と「感覚だけで復号する物理媒体」という枠組みが、視覚の側では30年以上前に確立していることを示すからである。日本語の近接研究として大川・栃窪も併せて引くべきである。

### 8. Cypherock X1（秘密分散を担体そのものに組み込んだ製品）

- 題名: Cypherock X1（X1 Vault と 4枚の X1 Card）
- 著者: Cypherock社
- 発表: 市販製品（技術文書は docs.cypherock.com、WalletScrutinyによる検証とKeylabsによる監査を掲載）
- 確認先URL: https://www.cypherock.com/ 、 https://docs.cypherock.com

内容の要約を述べる。Cypherock X1は、秘密鍵をShamirの秘密分散で分割し、1台のヴォルトと4枚の近距離無線通信カードに分けて保持する製品である。リカバリーフレーズの書き写しを不要にすることを売りにし、カードを別々の場所へ分散させることで単一障害点をなくすと述べている。取引に署名するときは4枚のうち任意の1枚をヴォルトにかざす。カードは共通基準EAL6以上の安全素子を持つ。

CipherFluteとの関係を述べる。「秘密分散の断片を複数の物理的な担体に載せ、利用者が分散配置する」という運用を製品として完成させた例である。ただし断片は電子的な安全素子の中にあり、読み出しには専用のヴォルトが要る。CipherFluteは電子部品を一切持たず、読み出しは吹くことと音高計測で済む点が対照的である。

脅威の度合いは中である。理由は、CipherFluteが訴える「複数の物体に分けて持ち歩く」という利用像がすでに商用化されていることを示すためである。電源不要という点と日用品への偽装という点で差分は明確に残る。

## 背景として押さえるべき文献

以下は脅威の度合いを低と判断したものである。いずれも一次資料で実在を確認した。

**人間可読な符号化の標準**

- BIP-39 Mnemonic code for generating deterministic keys（Marek Palatinus、Pavol Rusnak、Aaron Voisine、Sean Bowe、2013年提案、Deployed）。2048語、11ビットずつの索引、SHA-256による検査ビット、PBKDF2によるシード導出を定める。仕様本文が「紙に書き留めたり電話で口伝したりできる」と述べている点はCipherFluteの前提として引ける。https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki
- SLIP-0039 Shamir's Secret-Sharing for Mnemonic Codes（Pavol Rusnak、Andrew Kozlik、Ondrej Vejpustek、Tomas Susanka、Marek Palatinus、Jochen Hoenicke、2017年12月18日作成、Final）。1024語、20語または33語の断片、RS1024検査符号。語彙表の設計基準は4文字以上8文字以下で先頭4文字が一意、任意の2語のDamerau–Levenshtein距離が2以上と定めており、手書きや刻印での誤りを想定した設計である。合言葉を変えることで囮のウォレットへ入れる「もっともらしい否認」に言及している。https://github.com/satoshilabs/slips/blob/master/slip-0039.md
- Bytewords（BCR-2020-012、Wolf McNally、Christopher Allen、2020年6月20日、2020年10月4日改訂）。256語すべて4文字の語彙表で、各語の先頭と末尾の2文字だけで一意に決まる。文字数を減らすことで打刻した金属など恒久媒体への転写を容易にするという設計意図を明記している。https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2020-012-bytewords.md
- RFC 1751 A Convention for Human-Readable 128-bit Keys（D. McDonald、1994年12月、Informational）。128ビット鍵を2048語の辞書から12語へ写す。暗号資産以前の単語列符号化の原型である。https://datatracker.ietf.org/doc/html/rfc1751
- RFC 2289 A One-Time Password System（N. Haller、C. Metz、P. Nesser、M. Straw、1998年2月、Internet Standard）。64ビットを2048語辞書の6語へ写し、2ビットの検査を付ける。付録Dに標準辞書がある。https://datatracker.ietf.org/doc/html/rfc2289

**秘密分散と閾値署名の理論と標準**

- Adi Shamir, How to Share a Secret, Communications of the ACM, Vol. 22, No. 11, pp. 612–613, 1979年、DOI 10.1145/359168.359176。https://dblp.org/rec/journals/cacm/Shamir79.html
- SSKR（BCR-2020-011、Wolf McNally、Christopher Allen、2020年6月、2021年3月改訂）。SLIP-39とは互換でないことを明記し、BIP-39と同じマスターシードを往復できる点を利点として挙げる。断片はBytewordsまたは二次元コード向けのUniform Resourcesで符号化する。物理的な保管や隠蔽への言及はない。https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2020-011-sskr.md
- RFC 9591 The Flexible Round-Optimized Schnorr Threshold (FROST) Protocol for Two-Round Schnorr Signatures（D. Connolly、C. Komlo、I. Goldberg、C. A. Wood、2024年6月、Informational、IRTFストリーム）。t-of-nの閾値署名を定める。鍵を1か所に復元せずに署名できるため、シードを物理的に分散する動機そのものを減らす方向の技術である。https://datatracker.ietf.org/doc/rfc9591/
- NISTIR 8214 Threshold Schemes for Cryptographic Primitives（Luís T. A. N. Brandão、Nicky Mouha、Apostol Vassilev、2019年3月、DOI 10.6028/NIST.IR.8214）。閾値方式の標準化と検証の課題を整理している。https://csrc.nist.gov/pubs/ir/8214/final

**鍵管理の実務指針（NISTを含む）**

- NIST SP 800-57 Part 1 Revision 5 Recommendation for Key Management: Part 1 – General（Elaine Barker、2020年5月、DOI 10.6028/NIST.SP.800-57pt1r5）。鍵のバックアップと保存書庫を独立の機能として扱い、鍵情報を紙の形で金庫に置く運用を明示的に想定している（第8.2節から第8.3節、表7から表10）。複製を物理的に離れた場所に置き、完全性を定期的に確認することを勧めている。保護手段としてFIPS 140検証済み暗号モジュールによる物理保護と、金庫や管理区域による物理保護を並べている。用語集に「split knowledge（知識の分割）」を含む。https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-57pt1r5.pdf
- NIST SP 800-152 A Profile for U.S. Federal Cryptographic Key Management Systems（Elaine Barker、Dennis Branstad、Miles Smid、2015年10月、DOI 10.6028/NIST.SP.800-152）。SP 800-130の枠組みを連邦政府向けに具体化した要件集である。https://csrc.nist.gov/pubs/sp/800/152/final

**分散保管を実装した製品と運用**

- Trezor Shamir Backup（SatoshiLabs）。SLIP-39の実装であり、Model Tが世界初の完全実装であったこと、2024年6月以降Safeファミリーの既定のバックアップ形式になったこと、最大16の断片を作れることを述べている。断片を信頼できる友人や安全な場所へ分散することを勧める一方、電子的な複製を禁じている。https://trezor.io/learn/a/what-is-shamir-backup
- Armory の断片バックアップ。0.88（2013年4月）から0.96.2までShamirの秘密分散によるm-of-nの紙断片バックアップを提供していたが、係数を乱数ではなく秘密からの決定的な連鎖で作っていたため安全性が落ちていたことが判明し、0.96.3（2017年9月21日）で修正された。紙に印刷した秘密分散の実装が現実に誤ったという歴史的教訓として引ける。https://btcarmory.com/fragmented-backup-vuln/
- HashiCorp Vault の Shamir 封印。ルート鍵をShamirの秘密分散で複数の解封鍵に分け、運用者が順に投入して復元する。断片をPGP公開鍵で暗号化して配ることもできる。企業の運用で秘密分散が日常的に使われている例である。https://developer.hashicorp.com/vault/docs/concepts/seal
- Ledger Recover（Ledger、2023年5月発表）。安全素子の中でシードのエントロピーを暗号化し3つの断片に分け、Coincover、Ledger、EscrowTechの3社に預ける。復元には3つのうち2つが要り、政府発行の身分証明書による本人確認を伴う。物理媒体を使わない分散バックアップの代表例であり、自己保管の思想との衝突が議論を呼んだ。https://shop.ledger.com/pages/ledger-recover
- Vault12 Guard（Vault12社、2015年設立）。信頼する人や端末を「守護者」として指名し、暗号化した資産を分散保管する。守護者は何を守っているかも他の守護者が誰かも知らない。相続のための連絡先指定機能を持つ。https://vault12.com/blog/vitalik-buterin-social-recovery/
- Vitalik Buterin, Why we need wide adoption of social recovery wallets, 2021年1月11日。守護者による鍵の差し替えを提案し、シード語列を分割する方式については、128ビットのシードを分割すると1つを盗んだ者が残りを総当たりできる恐れがあると指摘している。素朴な分割の危険性を論じた一次資料として引ける。https://vitalik.eth.limo/general/2021/01/11/recovery.html
- Glacier Protocol。10万ドル以上の長期保管を想定した手順書であり、多重署名を採り、ハードウェアウォレットを使わず、鍵情報を紙へ書き写して保管する工程を持つ。隠蔽や偽装への言及はない。https://glacierprotocol.org/ 、 https://glacierprotocol.github.io/docs/overview/
- SmartCustody（Christopher Allen、Shannon Appelcline、Blockchain Commons、2020年、186ページ、BSD-2-Clause Plus Patent）。リスクモデリングと敵対者分析を軸に、多重署名、SSKRの断片、時間錠による復旧を組み合わせる指針を示す。https://www.smartcustody.com/ 、 https://github.com/BlockchainCommons/SmartCustody

**物理的な担体そのものの製品**

- Casascius 物理ビットコイン（Mike Caldwell、2011年から2013年）。秘密鍵をカードに印刷してコイン内部に封入し、改ざん検知ホログラムで覆う。ホログラムを剥がすと蜂の巣模様が残る。外側には残高照会用の8文字が見える。https://www.casascius.com/
- Opendime（Coinkite）。秘密鍵を装置内部で生成して人間に一切見せず、封を物理的にピンで破ることで初めて秘密鍵が現れる使い捨てのハードウェアウォレットである。手渡しでオンチェーン取引なしに価値を移せる持参人証券として売られている。https://opendime.com/
- SATSCARD と TAPSIGNER（Coinkite）。決済カードの形をした近距離無線通信の鍵担体である。SATSCARDはカードごと手渡すことで所有権が移り、TAPSIGNERは持ち主が使い続ける署名用の鍵を持つ。https://satscard.com/ 、 https://tapsigner.com/
- Jameson Lopp による金属製シード保管製品の耐久試験（75機種以上）。加熱、腐食、圧壊などの試験を行い、Blockplate、Cryptosteel Capsule、Hodlinox、NGRAVE GRAPHENE、CryptoTag Thor などを比較している。金属担体が「明らかに秘密の保管物」であることを前提にした市場の姿がよく分かる。https://jlopp.github.io/metal-bitcoin-storage-reviews/

**偽装・否認・強要への対処**

- COLDCARD の Trick PIN。囮の暗証番号で別のウォレット（BIP-85由来）を開く、装置を恒久的に使用不能にする、初期化済みに見せかけて実際には種を消さない、といった動作を割り当てられる。強要下でのもっともらしい否認を正面から扱っている。https://coldcard.com/docs/pins/
- Trezor の合言葉と隠しウォレット。合言葉ごとに別のウォレットが生成される。ただし公式の解説はもっともらしい否認や囮ウォレットという用途を積極的には謳っていない。https://trezor.io/learn/a/passphrases-and-hidden-wallets
- Border Wallets。2048語の全語を並べた格子を作り、自分だけが知る図形や座標の並びで語を拾うことで、書き留めずに記憶で復元できるようにする。国境を越えて資産を持ち運ぶ場面を想定用途として挙げている点で、担体を持たないことによる隠蔽の一形態である。https://www.borderwallets.com/
- seed_encode（CypherToad）。BIP-39の2048語を、動物や絵文字やゲーム機のボタン記号など任意の記号集合へ写し、シードを一見それと分からない形で紙に記録できるようにする実験的な道具である。学術的な裏づけはないが、担体の見た目を変える発想が趣味の水準では存在することを示す。https://github.com/CypherToad/seed_encode
- Chen Chen, Xiao Liang, Bogdan Carbunar, Radu Sion, SoK: Plausibly Deniable Storage, Proceedings on Privacy Enhancing Technologies, Vol. 2022, No. 2, pp. 132–151, 2022年、DOI 10.2478/popets-2022-0039。もっともらしい否認が可能な保存の体系化である。対象は電子的な記憶装置であり、物理的な担体は扱っていない。https://petsymposium.org/popets/2022/popets-2022-0039.php

**時間錠と相続**

- Ronald L. Rivest, Adi Shamir, David A. Wagner, Time-lock puzzles and timed-release Crypto, MIT Laboratory for Computer Science, 1996年3月10日改訂（報告番号 MIT/LCS/TR-684 として流通している）。情報を未来へ送るという課題に対し、本質的に逐次的な計算による時間錠と、信頼できる代理人（秘密分散で信頼を分散する）という二つの道筋を示している。著者本人の業績ページからPDFを取得し、表題と著者と日付を本文で確認した。https://people.csail.mit.edu/rivest/pubs/RSW96.pdf
- BIP-85 Deterministic Entropy From BIP32 Keychains（Ethan Kosakovsky、Aneesh Karve、2020年3月20日、Deployed）。1つのマスター鍵から任意個の子シードやパスワードを決定的に導出する。COLDCARDの囮ウォレットの実装基盤にもなっている。https://github.com/bitcoin/bips/blob/master/bip-0085.mediawiki
- BIP-38 Passphrase-protected private key（Mike Caldwell、Aaron Voisine、2012年11月20日、Deployed）。合言葉で保護した秘密鍵を58文字のBase58Check文字列にする。物理ビットコインや紙ウォレットのために設計され、製造者が利用者の合言葉を知らずに鍵を作れる2要素方式を含む。https://github.com/bitcoin/bips/blob/master/bip-0038.mediawiki

**利用実態と体系化の論文**

- Shayan Eskandari, Jeremy Clark, David Barrera, Elizabeth Stobert, A First Look at the Usability of Bitcoin Key Management, USEC 2015（NDSS Workshop on Usable Security）。https://arxiv.org/abs/1802.04351
- Katharina Krombholz, Aljosha Judmayer, Matthias Gusenbauer, Edgar Weippl, The Other Side of the Coin: User Experiences with Bitcoin Security and Privacy, Financial Cryptography and Data Security 2016, Springer, pp. 555–580。990名の調査と10名の面接を行った。https://link.springer.com/chapter/10.1007/978-3-662-54970-4_33 、事前刷は https://fc16.ifca.ai/preproceedings/33_Krombholz.pdf
- Gunnar Lindqvist, Joakim Kävrestad, Dennis Modig, Ali Padyab, How do Bitcoin Users Manage Their Private Keys?, 7th International Workshop on Socio-Technical Perspective in IS development (STPIS'21), CEUR-WS Vol. 3016, 2021年。339名の調査で、暗号化と多重署名の利用状況、ハードウェアウォレットの普及を報告している。https://ceur-ws.org/Vol-3016/paper2.pdf
- Yaman Yu, Tanusree Sharma, Sauvik Das, Yang Wang, "Don't put all your eggs in one basket": How Cryptocurrency Users Choose and Secure Their Wallets, CHI 2024, pp. 1–17, DOI 10.1145/3613904.3642534。
- Artemij Voskobojnikov, Oliver Wiese, Masoud Mehrabi Koushki ほか, The U in Crypto Stands for Usable: An Empirical Study of User Experience with Mobile Cryptocurrency Wallets, CHI 2021, DOI 10.1145/3411764.3445407。
- Sabine Houy, Philipp Schmid, Alexandre Bartel, Security Aspects of Cryptocurrency Wallets—A Systematic Literature Review, ACM Computing Surveys, Vol. 56, No. 1, pp. 1–31, 2024年、DOI 10.1145/3596906。
- Thierry Sans, Ziming Liu, Kevin Oh, A Decentralized Mnemonic Backup System for Non-custodial Cryptocurrency Wallets, Lecture Notes in Computer Science, pp. 355–370, 2023年、DOI 10.1007/978-3-031-30122-3_22。
- Syeda Tayyaba Bukhari, Muhammad Umar Janjua, Junaid Qadir, Secure Storage of Crypto Wallet Seed Phrase Using ECC and Splitting Technique, IEEE Open Journal of the Computer Society, Vol. 5, pp. 278–289, 2024年、DOI 10.1109/ojcs.2024.3398794。

**計算機を使わない暗号の系譜（日本の研究を含む）**

- カード組を使う暗号プロトコルの研究群。東北大学の水木敬明と曽根秀昭を中心に、物理的なカードだけで秘密計算やゼロ知識証明を実現する体系が築かれている。例として Julia Kastner ほか, The Minimum Number of Cards in Practical Card-Based Protocols, ASIACRYPT 2017, DOI 10.1007/978-3-319-70700-6_5、Daiki Miyahara ほか, Practical card-based implementations of Yao's millionaire protocol, Theoretical Computer Science, 2020年, DOI 10.1016/j.tcs.2019.11.005 がある。dblpの検索結果で書誌を確認した（https://dblp.org/search/publ/api?q=card-based%20Mizuki%20Sone&format=json ）。電源も計算機も使わずに暗号的な処理を行うという思想の、日本発の主要な系譜である。
- 日本語文献の状況として、CiNii Researchで「暗号資産 秘密鍵 管理」「ビットコイン 秘密鍵 管理」を検索したところ、岩下直行「暗号資産への脅威と対策」（デジタルプラクティス、第10巻第3号、pp. 441–456、2019年、https://cir.nii.ac.jp/crid/1050282813364719744 ）、山澤昌夫ほか「暗号資産（ビットコイン）・ブロックチェーンの高信頼化へ向けてのMELT-UP活動」（マルチメディア，分散協調とモバイルシンポジウム2019、https://cir.nii.ac.jp/crid/1050011097135362816 ）、森安翔太・森山雅光「暗号通貨ウォレットの秘密鍵管理手法の提案と評価」（経営情報学会全国研究発表大会要旨集、2017年、https://cir.nii.ac.jp/crid/1390001205709384960 ）などが見つかったが、いずれも物理的な担体の設計を扱っていない。

## 未検証のまま残ったもの

以下は実在や書誌情報を確認しきれなかったものである。憶測で書かず、どこまで確認できたかを記す。

- ISO/IEC 19592-1:2016 Information technology — Security techniques — Secret sharing — Part 1: General および ISO/IEC 19592-2:2017（Part 2: Fundamental mechanisms）。秘密分散そのものの国際規格である。ISOのカタログ（https://www.iso.org/standard/65422.html ）はHTTP 403で本文を取得できず、ANSIのウェブストアとiTeh Standardsも取得できなかった。検索結果の表題表示から番号と表題と年を推定できたにとどまるため、引用する場合は改めて規格書誌を確認する必要がある。
- ANSI X9.24 Part 1 / Part 2（小売金融サービスの対称鍵管理）および ISO 11568（銀行業務の鍵管理）、ISO 13491（安全な暗号装置）。いずれもPCI PIN Security Requirements v2.0の参照規格一覧と本文中の参照として実在を確認したが、規格本文そのものは有償のため取得できていない。CipherFluteの論文で引く場合は、PCI経由の間接引用にとどめるか、規格書誌を別途確認するのが安全である。
- PCI PIN Security Requirements の最新版。本調査で取得できたのはVersion 2.0（2014年12月）である。より新しい版（v3系）が存在する可能性が高いが、配布ページの構造上、最新版のPDFに直接到達できなかった。
- Blakley の秘密分散（1979年、AFIPS National Computer Conference）。Shamirと同年の独立提案として広く知られているが、本調査では一次資料に当たっていない。
- Diceware、PGP word list（Zimmermann と Juola）。人手による乱数生成と語による鍵の読み上げの標準的手法として言及したいが、一次資料の確認をしていない。
- Solfa Cipher（https://solfa-co.de/ ）。文字を音階の階名と音長へ写す音楽的な暗号である。検索結果の説明文でのみ内容を把握しており、サイト本文を取得していない。音を担体にする先行例として、他の切り口の担当者と突き合わせる価値がある。
- 相続や時間錠を扱う商用サービス（Casa、Liana、Unchained、SafeHaven の Inheriti など）。検索結果では複数確認できたが、各社の一次情報を取得していない。ビットコインのCHECKLOCKTIMEVERIFY（BIP-65）とCHECKSEQUENCEVERIFY（BIP-112）についても、提案本文を取得していない。
- 割符（わりふ）や英国のタリースティックなど、物体を二つに割って照合する歴史的な仕組み。CipherFluteの「2枚そろって初めてハートが現れるカード」の文化的先例として有用だが、学術的な一次資料に当たっていない。

## この切り口で見つからなかったこと

丁寧に書く。以下はCipherFluteの新規性の主張の根拠になる。

第一に、秘密情報の物理的バックアップの担体を、日用品として自然に振る舞う物体に偽装する方式は、標準にも、番号付き提案にも、学術論文にも、実在の製品にも見つからなかった。市販製品の担体はいずれも「秘密を保管するための専用品」として設計されており、金属板、カプセル、ホログラム封緘のコイン、決済カード型の鍵装置、封緘袋のいずれかである。Jameson Lopp の75機種以上の比較を見ても、外見を日用品に寄せた製品は一つもない。偽装に近い記述として見つかったのは「刻印した金属は目立たないので運用上の秘匿に役立ちうる」という程度の言及にとどまる。

第二に、決済業界と根鍵運用の実務指針は、担体を隠さないことを積極的に要件化していた。PCI PIN Security Requirements は連番付きの改ざん検知封筒の使用と、開封前の連番照合と改ざん痕点検を求めている。ICANNのルート鍵の運用も改ざん検知袋と貸金庫と録画を前提にしている。つまり、この分野の確立した実務は「見えて、検査できて、監査に残る」ことを価値としており、CipherFluteが選んだ「見えないこと」は、実務の主流とは反対方向の設計判断である。この対比は論文で明示的に述べる価値がある。

第三に、秘密分散の断片や暗号資産のリカバリーシードを音として符号化し、物理的な発音体から読み出す方式は、標準にも製品にも学術文献にも見つからなかった。音を使う秘密の符号化としては、趣味の水準でSolfa Cipherや文字を旋律へ写す実験的な道具があるだけで、リカバリーシードの物理バックアップとして設計されたものは確認できなかった。CipherFluteの音響チャネルという中核は、この切り口からは無傷である。

第四に、電源を持たない物理担体に誤り訂正符号を載せて秘密を保管するという発想は、既に二つの形で存在する。すなわち、codex32のBCH符号と、二次元コードに内在するReed–Solomon符号を金属板に打刻するCompactSeedQRである。したがってCipherFluteは「誤り訂正符号を物理バックアップに載せたこと」自体を新規性として主張してはならない。新規性は、音高というアナログ量を離散スロットへ量子化する際の誤りモデル、温度と息の強さによる全体のずれを基準笛で打ち消す設計、隣接同音の禁止といった、音響チャネル固有の符号設計に置くべきである。

第五に、日本語の学術文献の側では、秘密分散の物理的な担体設計を扱った研究がほとんど存在しない。CiNii ResearchとJ-STAGEと情報処理学会電子図書館を横断して調べた限り、日本の秘密分散研究は分散ストレージ、秘密計算、医療情報の分散管理、通信路への応用に集中しており、物理的な保管媒体そのものを設計した研究は視覚復号型秘密分散の応用（大川・栃窪）を除いて見当たらなかった。WISS 2025の予稿集にも暗号・鍵管理・秘密分散を扱った発表はなかった。日本の対話型システム分野において、この主題はほぼ未開拓である。

第六に、紙と鉛筆だけで秘密分散の復元計算ができる方式は、codex32という単一の系譜しか見つからなかった。視覚復号型秘密分散は計算を要さない点で近いが、これは分散した画像を重ねる方式であって、算術による復元ではない。つまり「人手で復元計算ができる秘密分散」の先行例は極めて少なく、CipherFluteが自らをどちらの系譜に置くかを明示すれば、位置づけは明瞭になる。

## 調べ残した穴

第一に、有償の国際規格の本文を読めていない。ISO/IEC 19592の秘密分散規格、ISO 11568の銀行鍵管理、ANSI X9.24の対称鍵管理は、いずれも「鍵成分を物理的に分けて運ぶ」実務の源流であり、本文に担体の要件がどこまで書かれているかを確認できていない。大学図書館の規格閲覧サービスを使えば確認できるはずである。

第二に、特許を調べていない。物理的なシード保管の分野は製品が先行しており、意匠や特許に「日用品への偽装」を謳ったものが存在する可能性がある。Google PatentsやJ-PlatPatを「seed phrase storage」「秘密鍵 保管 物品」などで探す作業が残っている。

第三に、相続と時間錠の系統を追い切れていない。BIP-65とBIP-112の提案本文、Miniscriptに基づく相続用ウォレット（Lianaなど）、および暗号資産の相続を扱う法学寄りの文献を確認していない。CipherFluteが「相続のために日用品に秘密を仕込む」という用途を主張する場合、ここは必ず補う必要がある。

第四に、被引用の追跡が十分ではない。OpenAlexが調査の途中でレート制限に掛かり、Semantic Scholarも429を返したため、codex32や視覚復号型秘密分散を引用している新しい論文を芋づる式に辿る作業が途中で止まっている。特にcodex32を引用した学術論文があるかどうかは、CipherFluteの位置づけを決めるうえで重要である。

第五に、実務家コミュニティの一次資料を網羅していない。bitcoin-devメーリングリストにおけるcodex32やSeed XORの議論、Blockchain Commonsの設計文書群、Bitcoin Optechのニュースレターなどには、担体の物理性についてより踏み込んだ議論がある可能性が高い。

第六に、日本語圏の実務側（取引所の鍵管理の開示文書、金融庁や日本暗号資産取引業協会の指針）を確認していない。国内の規制文書に「秘密鍵の物理的分散保管」に関する記述があれば、日本の学会で発表する論文としては引く価値がある。
