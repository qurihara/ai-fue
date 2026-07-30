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

内容の要約を述べる。codex32は、BIP-32のマスターシードをbech32のアルファベットで符号化し、そこにBCH誤り訂正符号による検査符号を付けた形式である。仕様本文は、小さな体と線形の誤り訂正符号を使っているので、検査符号の計算と検証、シードの分割と復元を紙と鉛筆だけで完結できると明言している（原文は「It is therefore possible to compute and verify checksums, and to split and recover seeds, entirely using pen and paper.」である）。公式サイトは印刷用の小冊子を配布しており、厚紙に印刷して組み立てる回転円板（ヴォルヴェル）が5ページ、残りは普通紙でよいと書かれている。付属する用紙は乱数文字用紙、変換用紙、検査符号用紙、復元ホイールである。数学的補遺は表題が「The codex32 Mathematical Companion」、著者名の表記は「Pearlwort Snead」であり、2023年8月23日版のPDFを取得して目次を確認した。章立ては数学の準備、ヴォルヴェルと対照表（bech32のアルファベット、加算ホイール、融合変換ホイール、復元用計算尺）、BCH符号（codex32検査符号、検査符号用紙）、秘密分散、簡易検査、誤り訂正、結語である。なお、BIPの著者欄の綴りは「Pearlwort Sneed」であり、数学的補遺の綴りは「Pearlwort Snead」である。両者は実際に食い違っており、これは書き写しの誤りではないことを確認した。Blockstreamのブログ記事（Andrew Poelstra、2023年9月7日）は、電子計算機は速すぎて人間が動作を確かめられないという動機を述べている。手計算の所要時間については、検査符号を作る作業に30分から60分かかり、最初の作業での誤りを捕らえるために二度行う必要があると書かれている。検証は同じだけの時間を要するが一度で足りるとされている。仕様は、長期に眠らせる鍵については、検査符号を人手で確かめられること自体に価値があり、秘密情報を新しい機材に晒さずに毎年の健全性確認ができると述べている（該当箇所を原文で確認した）。

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

- 題名: SeedQR Format Specification（標準のSeedQRとCompactSeedQRの両方を1つの文書で定めている。当初の記載「SeedQR Documentation および CompactSeedQR Specification」は文書の実際の表題と一致しなかったので訂正した）
- 著者: SeedSignerプロジェクト（開発者コミュニティ）
- 発表: SeedSignerリポジトリ内の仕様文書（継続更新、devブランチ）
- 確認先URL: https://github.com/SeedSigner/seedsigner/blob/dev/docs/seed_qr/README.md 、原文は https://raw.githubusercontent.com/SeedSigner/seedsigner/dev/docs/seed_qr/README.md で取得した

内容の要約を述べる。SeedQRは、BIP-39の各語を語彙表の索引番号（0から2047）へ写し、4桁ゼロ詰めで連結した数字列を数字モードの二次元コードに収める形式である。12語なら48桁となり25×25のコードに収まる。24語なら96桁となり29×29になる。CompactSeedQRは索引を11ビットの生の二進で詰める形式で、12語の場合は11ビット掛ける12語で132ビットとなり、そこから検査ビット4ビットを差し引いた128ビットを収めるので、21×21まで縮む。仕様は、コードが十分小さいので手で書き写せることを設計目標に掲げており、手描きした二次元コードの写真を載せている。金属板に穴を打って転写する運用にも触れ、CompactSeedQRにすると手打ちの作業量が35パーセントから40パーセントほど減ると述べている（原文は「that's cutting out about 35-40% of the work!」である）。標準のSeedQRは数字列がそのまま読めるので、専用の道具がなくても語彙表を引けば人手で復号できる。

CipherFluteとの関係を述べる。二次元コードで鍵を運ぶ方式の代表例であり、しかも二次元コードは規格上Reed–Solomon符号を内蔵している。したがって「Reed–Solomon符号で守られた物理的なシードのバックアップを、電源なしの担体に打刻する」という実務は、金属板に打ったCompactSeedQRとしてすでに存在する。CipherFluteの符号設計（スロット化した音高の系列にReed–Solomonを掛ける）は、二次元コードの符号設計と役割が重なる。

脅威の度合いは中である。理由は、誤り訂正符号を物理担体に載せる実務が既にあることを示すからである。一方で、二次元コードは明らかに機械可読な模様であって日用品には見えず、読み出しにカメラが要る点は差分として残る。

### 4. Of Secrets and Seedphrases: Conceptual Misunderstandings and Security Challenges for Seed Phrase Management among Cryptocurrency Users

- 題名: Of Secrets and Seedphrases: Conceptual Misunderstandings and Security Challenges for Seed Phrase Management among Cryptocurrency Users
- 著者: Farida Eleshin、Qi Sun、Mengzhe Ye、Sauvik Das、Jason I. Hong（カーネギーメロン大学）
- 発表: CHI Conference on Human Factors in Computing Systems（CHI '25）、2025年4月26日から5月1日、横浜、pp. 1–19（全19ページ）、ACM ISBN 979-8-4007-1394-1/25/04
- 確認先URL: https://doi.org/10.1145/3706598.3713209 （ACM Digital Libraryの当該ページはHTTP 403で開けなかったため、書誌はCrossrefのAPI https://api.crossref.org/works/10.1145/3706598.3713209 で照合し、本文PDFは https://sauvik.me/papers/63/serve から取得してローカルでテキスト抽出して読んだ）

内容の要約を述べる。20名への半構造化面接と643名への調査を組み合わせた混合手法の研究である。回答者の43パーセントしかリカバリーフレーズの画像を正しく見分けられず、多くがフレーズを再発行できると誤解していた。バックアップ方法としては紙が最多で39パーセントであり、紙は最も安全（167件）とも最も便利（161件）とも評価されていた。31パーセントはクラウドに保存していた。面接では、複数箇所へ分割して保管していたのは20名中1名（P8）だけであった。相続や死亡時の備えをしている者は少数にとどまった。以上の数値はすべて本文で裏を取った。本文には隠蔽やステガノグラフィに関する記述はない。抽出した全文に対してsteganography、conceal、hidden、disguise、decoyの各語を検索したところ、いずれも0件であった。参加者の工夫は「個人的な日記に書く」「暗号化する」といった水準にとどまっていた。

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
- 発表: 第8版、2025年4月14日発効（儀式の記録は第1回が2010年6月16日、最新の掲載は第63回の2026年11月12日で、合計63回が公開されている）
- 確認先URL: https://www.iana.org/dnssec/procedures 、 https://www.iana.org/dnssec/procedures/ksk-operator/ksk-dps-20250414.html 、 https://www.iana.org/dnssec/ceremonies

内容の要約を述べる。ルート鍵署名鍵の運用は、最低4階層の物理的な区画を設け、下位の階層を通らないと上位へ入れない構造にしている。すべての入退室は記録され、録画される。ハードウェアセキュリティモジュールは改ざん検知袋、施錠された金庫や保管庫で守られる。暗号担当者はそれぞれ個別の貸金庫を持ち、そこに個別の識別番号を付けた改ざん検知袋で認証情報を保管する。鍵の起動には7名の暗号担当者のうち3名の資格情報が必要である。災害復旧のために鍵の暗号化複製を可搬媒体に取って施設間で運ぶが、その暗号化鍵は7名の復旧鍵保持者のうち5名が必要な閾値方式で守られ、保持者は地理的に分散し、それぞれ改ざん検知包装で保管する。

CipherFluteとの関係を述べる。世界で最も監査された「秘密を物理的に分割して複数の人と場所へ預ける」運用の実例である。CipherFluteが想定する家庭内の秘密分散運用（複数の日用品に断片を仕込む）の、対極にある重量級の運用として引用できる。ここでも担体はスマートカードと封緘袋であり、偽装の発想はまったく現れない。

脅威の度合いは中である。理由は、閾値方式による物理的な鍵バックアップが現実に稼働していることを示す最良の事例であり、背景として引くだけでなく、CipherFluteの脅威モデル（秘匿は秘密分散に負わせる）の妥当性を支える論拠にもなるからである。

### 7. Visual Cryptography（Naor and Shamir）と視覚復号型秘密分散のパスワード応用（大川・栃窪）

- 題名1: Visual Cryptography
- 著者1: Moni Naor、Adi Shamir
- 発表1: Advances in Cryptology — EUROCRYPT '94、Lecture Notes in Computer Science、pp. 1–12、DOIは10.1007/BFb0053419。年については注意が要る。dblpは会議年に合わせて1994年としているが、Springerが登録したCrossrefのメタデータでは刊行年が1995年である。会議は1994年、Springerの予稿集刊行は1995年と書き分けるのが安全である。LNCSの巻番号はCrossrefのメタデータに含まれておらず、本検証では確定できなかった
- 確認先URL1: https://dblp.org/rec/conf/eurocrypt/NaorS94.html 、書誌の照合には https://api.crossref.org/works/10.1007/BFb0053419 も用いた
- 題名2: 視覚復号型秘密分散法を用いたパスワードの分散管理の提案（英題 Visual Secret Sharing Schemes for Passwords）
- 著者2: 大川直也、栃窪孝也
- 発表2: 情報処理学会論文誌デジタルプラクティス（TDP）、第7巻第2号、pp. 35–50、2026年4月15日、DOIは10.20729/0002009100、ISSN 2435-6484
- 確認先URL2: https://ipsj.ixsq.nii.ac.jp/records/2009100

内容の要約を述べる。Naor と Shamir の視覚復号型秘密分散は、秘密の画像を複数の透明シートに分け、シートを重ね合わせるだけで人間の視覚が復号を行う方式である。計算機も計算も要らず、閾値未満のシートからは情報が漏れない。大川と栃窪の論文は、生体認証が使えない場面でのパスワード保護を課題とし、視覚復号型秘密分散を画像に適用してパスワードを分散管理する方式を提案し、オーバーヘッドプロジェクタ用シートとスマートフォンを用いて実用性を評価している。復号が画像の重ね合わせだけで済み、複雑な計算を要さないことを利点として挙げている。この抄録の内容は情報処理学会電子図書館の当該レコードで確認した。大川は同じ主題で日本大学から博士（工学）を授与されている。学位論文の表題は「視覚復号型秘密分散法を用いた秘密情報の分散管理に関する研究」（英題 Study on Visual Secret Sharing Schemes for Secret Information）で、授与日は2026年3月25日である（https://nihon-u.repo.nii.ac.jp/records/2004470 ）。

CipherFluteとの関係を述べる。CipherFluteの実装のひとつに「2枚そろって初めてハートが現れるカード」がある。これは事実上、2-of-2の視覚的な秘密分散の演出であり、視覚復号型秘密分散の系譜に直接つながる。また「電源も計算機もなしに人間の感覚だけで秘密を復号する」という点で、音を使うCipherFluteの最も近い先行概念である。感覚のモダリティが視覚か聴覚かという違いが差分になる。

脅威の度合いは中である。理由は、CipherFluteのカード実装と「感覚だけで復号する物理媒体」という枠組みが、視覚の側では30年以上前に確立していることを示すからである。日本語の近接研究として大川・栃窪も併せて引くべきである。

### 8. Cypherock X1（秘密分散を担体そのものに組み込んだ製品）

- 題名: Cypherock X1（X1 Vault と 4枚の X1 Card）
- 著者: Cypherock社
- 発表: 市販製品（技術文書は docs.cypherock.com、WalletScrutinyによる検証とKeylabsによる監査を掲載）
- 確認先URL: https://www.cypherock.com/ 、 https://docs.cypherock.com

内容の要約を述べる。Cypherock X1は、秘密鍵をShamirの秘密分散で5つに分割し、1台のヴォルトと4枚の近距離無線通信カードに分けて保持する製品である（原文は「Your Crypto private key is cryptographically split into 5 parts using Shamir's Secret Sharing.」である）。リカバリーフレーズの書き写しを不要にすることを売りにし、カードを別々の場所へ分散させることで単一障害点をなくすと述べている。取引に署名するときは4枚のうち任意の1枚をヴォルトにかざす。カードは共通基準EAL6以上の安全素子を持ち、銀行のクレジットカードと同じ安全ハードウェアだと謳っている。

CipherFluteとの関係を述べる。「秘密分散の断片を複数の物理的な担体に載せ、利用者が分散配置する」という運用を製品として完成させた例である。ただし断片は電子的な安全素子の中にあり、読み出しには専用のヴォルトが要る。CipherFluteは電子部品を一切持たず、読み出しは吹くことと音高計測で済む点が対照的である。

脅威の度合いは中である。理由は、CipherFluteが訴える「複数の物体に分けて持ち歩く」という利用像がすでに商用化されていることを示すためである。電源不要という点と日用品への偽装という点で差分は明確に残る。

## 背景として押さえるべき文献

以下は脅威の度合いを低と判断したものである。いずれも一次資料で実在を確認した。

**人間可読な符号化の標準**

- BIP-39 Mnemonic code for generating deterministic keys（Marek Palatinus、Pavol Rusnak、Aaron Voisine、Sean Bowe、Type: Specification、Status: Deployed、2013年9月10日作成）。2048語、11ビットずつの索引、SHA-256による検査ビット、PBKDF2によるシード導出を定める。仕様本文が「The sentence could be written on paper or spoken over the telephone.」と述べている点はCipherFluteの前提として引ける。https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki
- SLIP-0039 Shamir's Secret-Sharing for Mnemonic Codes（Pavol Rusnak、Andrew Kozlik、Ondrej Vejpustek、Tomas Susanka、Marek Palatinus、Jochen Hoenicke、2017年12月18日作成、Final）。1024語、20語（128ビット安全性）または33語（256ビット安全性）の断片、RS1024検査符号。ここで重要なのは、RS1024がGF(1024)上のReed–Solomon符号だと仕様本文に明記されていることである。CipherFluteが使うReed–Solomon符号は、暗号資産のニーモニック符号の世界ではすでに標準の一部になっている。語彙表の設計基準は4文字以上8文字以下で先頭4文字が一意、任意の2語のDamerau–Levenshtein距離が2以上と定めており、手書きや刻印での誤りを想定した設計である。合言葉を変えることで囮のウォレットへ入れる「もっともらしい否認」に言及しており、原文は「the owner can use one passphrase to access their real wallet and another passphrase to access a decoy wallet」である。https://github.com/satoshilabs/slips/blob/master/slip-0039.md
- Bytewords: Encoding binary data as English words（BCR-2020-012、Wolf McNally、Christopher Allen、2020年6月20日、2020年10月4日改訂）。256語すべて4文字の語彙表で、各語は先頭1文字と末尾1文字の計2文字だけで一意に決まる（当初の記載「先頭と末尾の2文字」は計4文字と読めてしまうので訂正した）。文字数を減らすことで打刻した金属など恒久媒体への転写を容易にするという設計意図を明記しており、原文は「minimizing the number of letters for each word simplifies transfer to permanent media such as stamped metal」である。https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2020-012-bytewords.md
- RFC 1751 A Convention for Human-Readable 128-bit Keys（D. McDonald、NRL、1994年12月、Category: Informational）。128ビット鍵を2048語の辞書から12語へ写す。暗号資産以前の単語列符号化の原型である。https://datatracker.ietf.org/doc/html/rfc1751
- RFC 2289 A One-Time Password System（N. Haller、C. Metz、P. Nesser、M. Straw、1998年2月）。RFC本文の見出しは Category: Standards Track であるが、IETFのデータトラッカー上の現在の状態は Internet Standard であり STD 61 に指定されている。64ビットを2048語辞書の6語へ写し、余る2ビットに検査を入れる。付録Dに標準辞書がある。いずれも本文で確認した。https://datatracker.ietf.org/doc/html/rfc2289 、状態は https://datatracker.ietf.org/doc/rfc2289/ で確認した

**秘密分散と閾値署名の理論と標準**

- Adi Shamir, How to Share a Secret, Communications of the ACM, Vol. 22, No. 11, pp. 612–613, 1979年11月、DOI 10.1145/359168.359176。書誌はCrossrefのAPI（https://api.crossref.org/works/10.1145/359168.359176 ）とdblpの検索APIの両方で照合した。https://dblp.org/rec/journals/cacm/Shamir79.html
- SSKR、正式な表題は UR Type Definition for Sharded Secret Key Reconstruction (SSKR)（BCR-2020-011、Wolf McNally、Christopher Allen、2020年6月19日、2021年3月6日改訂）。SLIP-39とは互換でないことを明記し、BIP-39と同じマスターシードを往復できる点を利点として挙げる。断片はBytewordsまたは二次元コード向けのUniform Resources（ur:sskr）で符号化する。物理的な保管や隠蔽への言及はない。https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2020-011-sskr.md
- RFC 9591 The Flexible Round-Optimized Schnorr Threshold (FROST) Protocol for Two-Round Schnorr Signatures（D. Connolly（Zcash Foundation）、C. Komlo（University of Waterloo, Zcash Foundation）、I. Goldberg（University of Waterloo）、C. A. Wood（Cloudflare）、2024年6月、Category: Informational、IRTFストリーム）。t-of-nの閾値署名を定める。鍵を1か所に復元せずに署名できるため、シードを物理的に分散する動機そのものを減らす方向の技術である。https://datatracker.ietf.org/doc/rfc9591/
- NIST IR 8214 Threshold Schemes for Cryptographic Primitives: Challenges and Opportunities in Standardization and Validation of Threshold Cryptography（Luís T. A. N. Brandão、Nicky Mouha、Apostol Vassilev、2019年3月、DOI 10.6028/NIST.IR.8214）。当初は副題を省いていたので正式な表題に直した。閾値方式の標準化と検証の課題を整理している。https://csrc.nist.gov/pubs/ir/8214/final

**鍵管理の実務指針（NISTを含む）**

- NIST SP 800-57 Part 1 Revision 5 Recommendation for Key Management: Part 1 – General（Elaine Barker、2020年5月、DOI 10.6028/NIST.SP.800-57pt1r5）。PDFを取得して該当箇所を本文で確かめた。鍵情報を紙の形で金庫に置く運用を明示的に想定しており、原文は第6.2.2節の「in hard copy form and placed in a safe; this would be typical for backup or archive storage」である。複製を物理的に離れた場所に置き、完全性を定期的に確認することを勧める記述も第6.2.2節にあり、原文は「one or more copies of the key information should be maintained in physically separate locations (i.e., in backup or archive storage; see Sections 8.2.2.1 and 8.3.1). The integrity of each copy should be periodically checked.」である。当初は根拠箇所を「第8.2節から第8.3節」と書いていたが、正しくは第6.2.2節が中心で、バックアップの機能は第8.2.2.1節、保存書庫と復元の機能は第8.3.1節にあるので訂正した。表については表7が鍵のバックアップ、表8が関連情報のバックアップ、表9が鍵の保存書庫、表10が関連情報の保存書庫であり、表7から表10という記載は正しい。保護手段としてFIPS 140による物理保護と、金庫や管理区域による物理保護を並べている。用語集に「split knowledge（知識の分割）」を含む。https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-57pt1r5.pdf
- NIST SP 800-152 A Profile for U.S. Federal Cryptographic Key Management Systems (CKMS)（Elaine Barker（NIST）、Dennis Branstad（NIST）、Miles Smid（Orion Security Solutions）、2015年10月28日確定、DOI 10.6028/NIST.SP.800-152）。SP 800-130の枠組みを連邦政府向けに具体化した要件集である。https://csrc.nist.gov/pubs/sp/800/152/final

**分散保管を実装した製品と運用**

- Trezor Shamir Backup（SatoshiLabs）。SLIP-39の実装であり、Model Tが世界初の完全実装であったこと（原文は「The Trezor Model T was the first hardware wallet in the world to implement the fully functional SLIP39 security standard.」）、2024年6月以降Safeファミリーの既定のバックアップ形式になったこと、断片は1から最大16まで作れることを述べている。断片を信頼できる相手や場所へ分散することを勧める一方、電子的な複製を禁じている（原文は「Never make digital copies of your recovery seed or recovery shares.」）。当初は「信頼できる友人」と書いていたが、当該ページの表現は「trusted parties or locations」であって友人に限定していないので改めた。https://trezor.io/learn/a/what-is-shamir-backup
- Armory の断片バックアップ。0.88（2013年4月18日）から0.96.2までShamirの秘密分散によるm-of-nの紙断片バックアップを提供していたが、係数を乱数ではなく秘密のハッシュからの決定的な連鎖で作っていたため安全性が落ちていたことが判明し、0.96.3（2017年9月21日）で修正された。開発者は断片バックアップを持つ財布は危険とみなして資金を移すよう促している。紙に印刷した秘密分散の実装が現実に誤ったという歴史的教訓として引ける。https://btcarmory.com/fragmented-backup-vuln/
- HashiCorp Vault の Shamir 封印。文書の記述を正確に写すと、Shamirの秘密分散で分けられるのは解封鍵（unseal key）であり、運用者が閾値個の断片を順に投入して解封鍵を再構成し、それによってルート鍵を復号する。当初は「ルート鍵をShamirの秘密分散で複数の解封鍵に分け」と書いていたが、分割される対象が違うので訂正した。断片をPGP公開鍵で暗号化して配ることもできる。企業の運用で秘密分散が日常的に使われている例である。https://developer.hashicorp.com/vault/docs/concepts/seal
- Ledger Recover（Ledger）。安全素子の中でシードのエントロピーを暗号化し3つの断片に分け、Coincover、Ledger、EscrowTechの3社に預ける。復元には3つのうち2つが要り、政府発行の身分証明書による本人確認を伴う。以上は当該ページで確認した。ただし「2023年5月発表」という時期は当該ページに書かれておらず、本検証では一次情報で裏を取れなかったので記述から外した。時期を論文に書く場合は改めてLedgerの発表文で確認する必要がある。物理媒体を使わない分散バックアップの代表例であり、自己保管の思想との衝突が議論を呼んだ。https://shop.ledger.com/pages/ledger-recover
- Vault12 Guard（Vault12社、2015年設立）。信頼する人や端末を「守護者」として指名し、暗号化した資産を分散保管する。守護者は何を守っているかも他の守護者が誰かも知らない（原文は「Guardians need not know what they are guarding」である）。相続のための連絡先指定機能を持つ。https://vault12.com/blog/vitalik-buterin-social-recovery/
- Vitalik Buterin, Why we need wide adoption of social recovery wallets, 2021年1月11日。守護者による鍵の差し替えを提案し、シード語列を分割する方式については、128ビットのシードを分割すると1つを盗んだ者が残りの2の64乗通りを総当たりできる恐れがあると指摘している。原文は「if the phrase is short (128 bits) then a sophisticated and motivated attacker who steals one piece may be able to brute-force through all 2^64 possible combinations to find the other」である。素朴な分割の危険性を論じた一次資料として引ける。https://vitalik.eth.limo/general/2021/01/11/recovery.html
- Glacier Protocol。10万ドル以上の長期保管を想定した手順書であり（原文は「Large amounts of money ($100,000+)」）、多重署名を採り、ハードウェアウォレットを使わず、鍵情報を紙へ書き写して保管する工程（Transfer cold storage data to paper）を持つ。隠蔽や偽装への言及はない。https://glacierprotocol.org/ 、 http://glacierprotocol.org/docs/overview/ （旧URL https://glacierprotocol.github.io/docs/overview/ はここへ301で転送される）
- SmartCustody（Christopher Allen、Shannon Appelcline、Blockchain Commons、186ページ、ライセンスはBSD-2-Clause Plus Patent）。年については訂正が要る。リポジトリの記述では第1.01版の公開は2019年7月であり、当初書いていた2020年ではない。第1版の章立てはリスクモデリング、単独での冷蔵保管の想定場面、敵対者、電子的な管理責任、Frank Family Fundの例の5部である。多重署名、SSKRの断片、時間錠による復旧は、書籍本体ではなくリポジトリに併載された記事群が扱っており、多重署名の想定場面は準備中の第2版で大幅に拡張されると書かれている。https://www.smartcustody.com/ 、 https://github.com/BlockchainCommons/SmartCustody

**物理的な担体そのものの製品**

- Casascius 物理ビットコイン（Mike Caldwell）。秘密鍵をカードに印刷してコイン内部に封入し、改ざん検知ホログラムで覆う。ホログラムを剥がすと蜂の巣模様が残る（原文は「The hologram leaves behind a honeycomb pattern if it is peeled.」）。外側に見える8文字は、そのコインに割り当てられたビットコインアドレスの先頭8文字である。年については訂正が要る。本人のサイトで確認できるのは「2013年11月27日に、電子的なビットコインを含む商品の販売を停止した」という記述だけであり、開始年の2011年は当該ページでは裏が取れなかった。https://www.casascius.com/
- Opendime（Coinkite）。秘密鍵を装置内部で生成して人間に一切見せず（原文は「The private key is generated inside the device, and is never known to any human, not even you!」）、封を物理的にピンで破ることで初めて秘密鍵が現れる使い捨てのハードウェアウォレットである。この操作は不可逆だと明記されている。手渡しでオンチェーン取引なしに価値を移せる持参人証券として売られている。https://opendime.com/
- SATSCARD と TAPSIGNER（Coinkite Inc.）。決済カードの形をした近距離無線通信の鍵担体である。SATSCARDは独立した10個のスロットを持ち、封をしたスロットに資金を入れたままカードごと手渡すことで、オンチェーン取引なしに所有権が移る。TAPSIGNERは1つのBIP-32マスター鍵を持ち、持ち主が使い続ける署名用の鍵として設計されている。https://satscard.com/ 、 https://tapsigner.com/
- Jameson Lopp による金属製シード保管製品の耐久試験。サイト本文は「after testing 75 devices」と書いており、75機種を試験したと読める（当初の「75機種以上」は原文より強い言い方だったので直した）。加熱、腐食、圧壊の試験を行い、Blockplate、Cryptosteel Capsule、Hodlinox、NGRAVE GRAPHENE、CryptoTag Thor などを比較している。部品が多いほど故障点が増えるので単板の格子型がよいと結論している。金属担体が「明らかに秘密の保管物」であることを前提にした市場の姿がよく分かる。https://jlopp.github.io/metal-bitcoin-storage-reviews/

**偽装・否認・強要への対処**

- COLDCARD の Trick PIN。囮の暗証番号で別のウォレットを開く「Duress Wallet」、装置を恒久的に使用不能にする「Brick Self」、初期化済みに見せかけて実際には種を消さない「Look Blank」といった動作を割り当てられる。囮ウォレットの導出はBIP-85を用い、24語の種の場合は導出経路の索引が1001、1002、1003になると書かれている。強要下でのもっともらしい否認を正面から扱っている。https://coldcard.com/docs/pins/
- Trezor の合言葉と隠しウォレット。合言葉ごとに別のウォレットが生成される（原文は「Every passphrase you enter creates a different wallet, even if it's a typo or mistake.」）。当該ページを本文で確認したところ、もっともらしい否認や囮ウォレットという用途への言及はまったくなく、技術的な仕組みと注意喚起に終始している。この点は当初の記述どおりであった。https://trezor.io/learn/a/passphrases-and-hidden-wallets
- Border Wallets。2048語の全語を並べた乱順の格子を作り、自分だけが知る図形や座標の並びで語を拾うことで、書き留めずに記憶で復元できるようにする。絵の優位性効果を根拠に挙げている。国境を越えて資産を安全に持ち運ぶ場面を想定用途として明記しており、担体を持たないことによる隠蔽の一形態である。https://www.borderwallets.com/
- seed_encode（CypherToad）。BIP-39の2048語を、動物や絵文字やゲーム機のボタン記号など任意の記号集合へ写し、シードを一見それと分からない形で紙に記録できるようにする実験的な道具である。README自身が「移植性も安全性も検証しておらず、思考実験の共有にすぎない」と述べている。学術的な裏づけはないが、担体の見た目を変える発想が趣味の水準では存在することを示す。https://github.com/CypherToad/seed_encode
- Chen Chen, Xiao Liang, Bogdan Carbunar, Radu Sion, SoK: Plausibly Deniable Storage, Proceedings on Privacy Enhancing Technologies, Vol. 2022, No. 2, pp. 132–151, 2022年3月3日、DOI 10.2478/popets-2022-0039。書誌はCrossrefで照合した。もっともらしい否認が可能な保存の体系化である。対象は電子的な記憶装置であり、物理的な担体は扱っていない。https://petsymposium.org/popets/2022/popets-2022-0039.php
- Solfa Cipher（https://solfa-co.de/ 。著作権表示は2013年、改訂は2024年）。当初は「未検証のまま残ったもの」に置いていたが、今回サイト本文を取得して内容を確認できたのでここへ移した。各文字を音階の階名（Do、Re、Mi など）と音長（4分、8分、16分、全音符に対応する1から4）の組へ写し、文章を旋律として符号化する音楽的な暗号である。鍵（Solfa Key）を変えると旋律の音が変わるので、音符だけを渡された者は鍵を知らないと復号できないと述べている。音を符号の担体にする趣味水準の先行例として押さえておく価値があるが、物理的な発音体を作るわけではなく、誤り訂正も秘密分散もなく、暗号資産のバックアップを想定してもいない。脅威の度合いは低である。音そのものを符号化する系譜としては、切り口「音でデータを送る」の担当者の一覧と突き合わせるとよい。

**時間錠と相続**

- Ronald L. Rivest, Adi Shamir, David A. Wagner, Time-lock puzzles and timed-release Crypto, MIT Laboratory for Computer Science, 1996年3月10日改訂。情報を未来へ送るという課題に対し、本質的に逐次的な計算による時間錠と、信頼できる代理人（秘密分散で信頼を分散する）という二つの道筋を示している。著者本人の業績ページからPDFを取得し、表題、著者3名、所属（MIT、ワイツマン科学研究所、カリフォルニア大学バークレー校）、改訂日、そして二つの道筋を本文で確認した。ただし報告番号 MIT/LCS/TR-684 はPDF本文のどこにも現れない。この番号は外部の目録で流通しているものであり、引用に用いる場合は別途確認するのが安全である。https://people.csail.mit.edu/rivest/pubs/RSW96.pdf
- BIP-85 Deterministic Entropy From BIP32 Keychains（Ethan Kosakovsky、Aneesh Karve、Type: Informational、Status: Deployed、2020年3月20日作成）。1つのマスター鍵から任意個の子シードやパスワードを決定的に導出する。COLDCARDの囮ウォレットの実装基盤にもなっている。https://github.com/bitcoin/bips/blob/master/bip-0085.mediawiki
- BIP-38 Passphrase-protected private key（Mike Caldwell、Aaron Voisine、Type: Specification、Status: Deployed、2012年11月20日作成）。合言葉で保護した秘密鍵を58文字のBase58Check文字列にする。物理ビットコインや紙ウォレットのために設計され、製造者（仕様中の呼称は printer）が利用者の合言葉を知らずに鍵を作れる楕円曲線の乗算による2要素方式を含む。https://github.com/bitcoin/bips/blob/master/bip-0038.mediawiki

**利用実態と体系化の論文**

- Shayan Eskandari, Jeremy Clark, David Barrera, Elizabeth Stobert, A First Look at the Usability of Bitcoin Key Management, USEC 2015（NDSS Workshop on Usable Security、2015年2月8日、サンディエゴ）。6つのビットコインクライアントを評価している。arXivの登録情報で表題、著者4名、会議名、開催日を確認した。https://arxiv.org/abs/1802.04351
- Katharina Krombholz, Aljosha Judmayer, Matthias Gusenbauer, Edgar Weippl, The Other Side of the Coin: User Experiences with Bitcoin Security and Privacy, Financial Cryptography and Data Security 2016（会議は2016年2月、バルバドス）, Springer, Lecture Notes in Computer Science, pp. 555–580。Springerの予稿集（Revised Selected Papers）の刊行年はCrossrefでは2017年である。990名の調査と10名の面接を行った。https://link.springer.com/chapter/10.1007/978-3-662-54970-4_33 、事前刷は https://fc16.ifca.ai/preproceedings/33_Krombholz.pdf
- Gunnar Lindqvist, Joakim Kävrestad, Dennis Modig, Ali Padyab（いずれもスウェーデンのシェブデ大学）, How do Bitcoin Users Manage Their Private Keys?, 7th International Workshop on Socio-Technical Perspective in IS Development (STPIS 2021), CEUR-WS Vol. 3016, pp. 11–21, 2021年（予稿集の公開は2021年11月21日）。339名の調査で、利用者は多重署名よりも手軽さから暗号化を選ぶ傾向があり、ハードウェアウォレットが最も使われていると報告している。多重署名の利用は34.5パーセントである。PDFをローカルでテキスト抽出して本文の数値を確認した。https://ceur-ws.org/Vol-3016/paper2.pdf 、会議名と巻とページは https://ceur-ws.org/Vol-3016/ で確認した
- Yaman Yu, Tanusree Sharma, Sauvik Das, Yang Wang, "Don't put all your eggs in one basket": How Cryptocurrency Users Choose and Secure Their Wallets, CHI 2024, pp. 1–17, DOI 10.1145/3613904.3642534。書誌はCrossrefで照合した。
- Artemij Voskobojnikov, Oliver Wiese, Masoud Mehrabi Koushki, Volker Roth, Konstantin Beznosov, The U in Crypto Stands for Usable: An Empirical Study of User Experience with Mobile Cryptocurrency Wallets, CHI 2021, pp. 1–14, DOI 10.1145/3411764.3445407。当初は3人目までを挙げて「ほか」としていたので、Crossrefで確認した全5名に直した。
- Sabine Houy, Philipp Schmid, Alexandre Bartel, Security Aspects of Cryptocurrency Wallets—A Systematic Literature Review, ACM Computing Surveys, Vol. 56, No. 1, pp. 1–31, DOI 10.1145/3596906。年については、Crossrefの登録日が2023年8月28日で、掲載号は第56巻第1号（2024年1月号）である。オンライン公開が2023年、誌面が2024年と書き分けるのが正確である。
- Thierry Sans, Ziming Liu, Kevin Oh, A Decentralized Mnemonic Backup System for Non-custodial Cryptocurrency Wallets, Lecture Notes in Computer Science, pp. 355–370, 2023年、DOI 10.1007/978-3-031-30122-3_22。書誌はCrossrefで照合した。
- Syeda Tayyaba Bukhari, Muhammad Umar Janjua, Junaid Qadir, Secure Storage of Crypto Wallet Seed Phrase Using ECC and Splitting Technique, IEEE Open Journal of the Computer Society, Vol. 5, pp. 278–289, 2024年、DOI 10.1109/ojcs.2024.3398794。書誌はCrossrefで照合した。

**計算機を使わない暗号の系譜（日本の研究を含む）**

- カード組を使う暗号プロトコルの研究群。東北大学の水木敬明と曽根秀昭を中心に、物理的なカードだけで秘密計算やゼロ知識証明を実現する体系が築かれている。書誌はCrossrefで照合し、次のとおりであった。Julia Kastner, Alexander Koch, Stefan Walzer, Daiki Miyahara, Yu-ichi Hayashi, Takaaki Mizuki, Hideaki Sone, The Minimum Number of Cards in Practical Card-Based Protocols, ASIACRYPT 2017, Lecture Notes in Computer Science, pp. 126–155, 2017年, DOI 10.1007/978-3-319-70700-6_5。Daiki Miyahara, Yu-ichi Hayashi, Takaaki Mizuki, Hideaki Sone, Practical card-based implementations of Yao's millionaire protocol, Theoretical Computer Science, Vol. 803, pp. 207–221, 2020年1月, DOI 10.1016/j.tcs.2019.11.005。電源も計算機も使わずに暗号的な処理を行うという思想の、日本発の主要な系譜である。
- 日本語文献の状況として、CiNii Researchで「暗号資産 秘密鍵 管理」「ビットコイン 秘密鍵 管理」を検索したところ、次の3件などが見つかった。いずれもCiNiiまたはJ-STAGEのレコードで書誌を確認したが、物理的な担体の設計を扱ったものはなかった。第一に、岩下直行「暗号資産への脅威と対策 --ビットコインの社会への展開による変質--」（デジタルプラクティス、第10巻第3号、pp. 441–456、2019年7月15日、情報処理学会、https://cir.nii.ac.jp/crid/1050282813364719744 ）である。当初は副題を落としていたので補った。第二に、山澤昌夫、角田篤泰、藤田亮、近藤健、才所敏明、五太子政史、佐藤直、山本博資、辻井重男、野田啓一「暗号資産（ビットコイン）・ブロックチェーンの高信頼化へ向けてのMELT-UP活動」（マルチメディア，分散協調とモバイルシンポジウム2019論文集、pp. 192–195、2019年6月26日、情報処理学会、https://cir.nii.ac.jp/crid/1050011097135362816 ）である。第三に、森安昭太、森山真光「暗号通貨ウォレットの秘密鍵管理手法の提案と評価」（経営情報学会全国研究発表大会要旨集、pp. 55–58、2017年、いずれも近畿大学、DOI 10.11497/jasmin.2017f.0_55、https://cir.nii.ac.jp/crid/1390001205709384960 ）である。この第三の文献は著者名に誤りがあったので訂正した。当初は「森安翔太・森山雅光」と書いていたが、J-STAGEの当該ページのメタデータ（citation_author）は「森安 昭太」「森山 真光」であり、名の字が二人とも違っていた。内容は、ハードウェアウォレットが不正に操作される危険に対し、ホストとの間でインターネット非接続を確認してから利用を許すプロトコルを提案するものである。

## 未検証のまま残ったもの

以下は実在や書誌情報を確認しきれなかったものである。憶測で書かず、どこまで確認できたかを記す。

- ISO/IEC 19592-1:2016 Information technology — Security techniques — Secret sharing — Part 1: General および ISO/IEC 19592-2:2017（Part 2: Fundamental mechanisms）。秘密分散そのものの国際規格である。2026年7月30日の検証でもISOのカタログ（https://www.iso.org/standard/65422.html および https://www.iso.org/standard/65425.html ）はCloudflareの認証画面でHTTP 403となり、本文にも書誌表示にも到達できなかった。ANSIのウェブストアとiTeh Standardsも取得できていない。番号と表題と年はいずれも一次情報で裏が取れていないので、引用する場合は改めて規格書誌を確認する必要がある。
- ANSI X9.24 Part 1 / Part 2（小売金融サービスの対称鍵管理）および ISO 11568（銀行業務の鍵管理）、ISO 13491（安全な暗号装置）。今回、PCI PIN Security Requirements v2.0のPDFを取得して参照規格の表を本文で確認した。表には「ANSI X9.24 (Part 1): Retail Financial Services Symmetric Key Management Part 1: Using Symmetric Techniques」「ANSI X9.24 (Part 2): ... Using Asymmetric Techniques for the Distribution of Symmetric Keys」「ISO 11568: Banking - Key Management (Retail)」「ISO 13491: Banking - Secure Cryptographic Devices (Retail)」「NIST Special Publication 800-57: Recommendation for Key Management」が確かに載っていた。ただし各規格の本文そのものは有償のため取得できていない。CipherFluteの論文で引く場合は、PCI経由の間接引用にとどめるか、規格書誌を別途確認するのが安全である。
- PCI PIN Security Requirements の最新版。本調査で取得して本文まで読めたのはVersion 2.0（2014年12月。文書冒頭の改版履歴に「October 2011 1.0 Initial release」「December 2014 2.0 Initial release of requirements with test procedures」と記載されている）である。より新しい版が存在する可能性は高いが、今回の検証時点でWeb検索の実行回数が上限に達しており、最新版の所在を探せなかった。版番号を論文に書く場合は、PCI Security Standards Councilの文書ライブラリで最新版を確認する必要がある。
- Blakley の秘密分散（1979年、AFIPS National Computer Conference）。Shamirと同年の独立提案として広く知られているが、本調査では一次資料に当たっていない。
- Diceware、PGP word list（Zimmermann と Juola）。人手による乱数生成と語による鍵の読み上げの標準的手法として言及したいが、一次資料の確認をしていない。
- 相続や時間錠を扱う商用サービス（Casa、Liana、Unchained、SafeHaven の Inheriti など）。検索結果では複数確認できたが、各社の一次情報を取得していない。ビットコインのCHECKLOCKTIMEVERIFY（BIP-65）とCHECKSEQUENCEVERIFY（BIP-112）についても、提案本文を取得していない。
- 割符（わりふ）や英国のタリースティックなど、物体を二つに割って照合する歴史的な仕組み。CipherFluteの「2枚そろって初めてハートが現れるカード」の文化的先例として有用だが、学術的な一次資料に当たっていない。
- EUROCRYPT '94の予稿集のLecture Notes in Computer Scienceの巻番号。Naor と Shamir の視覚復号型秘密分散を引くにあたって巻番号を添えたいが、Crossrefのメタデータには巻番号が入っておらず、Springerの章ページは認証画面へ転送されて開けなかったので確定できていない。

## この切り口で見つからなかったこと

丁寧に書く。以下はCipherFluteの新規性の主張の根拠になる。

第一に、秘密情報の物理的バックアップの担体を、日用品として自然に振る舞う物体に偽装する方式は、標準にも、番号付き提案にも、学術論文にも、実在の製品にも見つからなかった。市販製品の担体はいずれも「秘密を保管するための専用品」として設計されており、金属板、カプセル、ホログラム封緘のコイン、決済カード型の鍵装置、封緘袋のいずれかである。Jameson Lopp の75機種の比較を見ても、外見を日用品に寄せた製品は一つもない。偽装に近い記述として見つかったのは「刻印した金属は目立たないので運用上の秘匿に役立ちうる」という程度の言及にとどまる。

第二に、決済業界と根鍵運用の実務指針は、担体を隠さないことを積極的に要件化していた。PCI PIN Security Requirements は連番付きの改ざん検知封筒の使用と、開封前の連番照合と改ざん痕点検を求めている。ICANNのルート鍵の運用も改ざん検知袋と貸金庫と録画を前提にしている。つまり、この分野の確立した実務は「見えて、検査できて、監査に残る」ことを価値としており、CipherFluteが選んだ「見えないこと」は、実務の主流とは反対方向の設計判断である。この対比は論文で明示的に述べる価値がある。

第三に、秘密分散の断片や暗号資産のリカバリーシードを音として符号化し、物理的な発音体から読み出す方式は、標準にも製品にも学術文献にも見つからなかった。音を使う秘密の符号化としては、趣味の水準でSolfa Cipher（今回の検証でサイト本文を確認した）のように文字を階名と音長へ写す実験的な道具があるだけで、リカバリーシードの物理バックアップとして設計されたものは確認できなかった。CipherFluteの音響チャネルという中核は、この切り口からは無傷である。

第四に、電源を持たない物理担体に誤り訂正符号や検査符号を載せて秘密を保管するという発想は、既に三つの形で存在する。第一はcodex32のBCH符号である。第二は、二次元コードに内在するReed–Solomon符号を金属板に打刻するCompactSeedQRである。第三は、検証の途中で気づいた点であるが、SLIP-39の検査符号RS1024そのものが、仕様本文にGF(1024)上のReed–Solomon符号だと明記されていることである。つまりCipherFluteが選んだReed–Solomon符号という道具は、暗号資産のニーモニック符号の標準の内側にすでに置かれている。したがってCipherFluteは「誤り訂正符号を物理バックアップに載せたこと」自体を新規性として主張してはならない。新規性は、音高というアナログ量を離散スロットへ量子化する際の誤りモデル、温度と息の強さによる全体のずれを基準笛で打ち消す設計、隣接同音の禁止といった、音響チャネル固有の符号設計に置くべきである。

第五に、日本語の学術文献の側では、秘密分散の物理的な担体設計を扱った研究がほとんど存在しない。CiNii ResearchとJ-STAGEと情報処理学会電子図書館を横断して調べた限り、日本の秘密分散研究は分散ストレージ、秘密計算、医療情報の分散管理、通信路への応用に集中しており、物理的な保管媒体そのものを設計した研究は視覚復号型秘密分散の応用（大川・栃窪）を除いて見当たらなかった。WISS 2025の予稿集についても、今回の検証で発表一覧のページ（https://www.wiss.org/WISS2025/program.html ）を取得し、本文全体に対して「暗号」「鍵」「秘密」「セキュリ」「認証」「分散」「パスワード」の各語を検索したところ、いずれも0件であった。この否定的な主張は裏が取れた。なお「音」は7件あったが、いずれも楽曲推薦、管楽器のロングトーン練習支援、視覚障害者向けの音声案内といった主題であり、鍵管理とは関係がなかった。日本の対話型システム分野において、この主題はほぼ未開拓である。

第六に、紙と鉛筆だけで秘密分散の復元計算ができる方式は、codex32という単一の系譜しか見つからなかった。視覚復号型秘密分散は計算を要さない点で近いが、これは分散した画像を重ねる方式であって、算術による復元ではない。つまり「人手で復元計算ができる秘密分散」の先行例は極めて少なく、CipherFluteが自らをどちらの系譜に置くかを明示すれば、位置づけは明瞭になる。

## 調べ残した穴

第一に、有償の国際規格の本文を読めていない。ISO/IEC 19592の秘密分散規格、ISO 11568の銀行鍵管理、ANSI X9.24の対称鍵管理は、いずれも「鍵成分を物理的に分けて運ぶ」実務の源流であり、本文に担体の要件がどこまで書かれているかを確認できていない。大学図書館の規格閲覧サービスを使えば確認できるはずである。

第二に、特許を調べていない。物理的なシード保管の分野は製品が先行しており、意匠や特許に「日用品への偽装」を謳ったものが存在する可能性がある。Google PatentsやJ-PlatPatを「seed phrase storage」「秘密鍵 保管 物品」などで探す作業が残っている。

第三に、相続と時間錠の系統を追い切れていない。BIP-65とBIP-112の提案本文、Miniscriptに基づく相続用ウォレット（Lianaなど）、および暗号資産の相続を扱う法学寄りの文献を確認していない。CipherFluteが「相続のために日用品に秘密を仕込む」という用途を主張する場合、ここは必ず補う必要がある。

第四に、被引用の追跡が十分ではない。OpenAlexが調査の途中でレート制限に掛かり、Semantic Scholarも429を返したため、codex32や視覚復号型秘密分散を引用している新しい論文を芋づる式に辿る作業が途中で止まっている。特にcodex32を引用した学術論文があるかどうかは、CipherFluteの位置づけを決めるうえで重要である。

第五に、実務家コミュニティの一次資料を網羅していない。bitcoin-devメーリングリストにおけるcodex32やSeed XORの議論、Blockchain Commonsの設計文書群、Bitcoin Optechのニュースレターなどには、担体の物理性についてより踏み込んだ議論がある可能性が高い。

第六に、日本語圏の実務側（取引所の鍵管理の開示文書、金融庁や日本暗号資産取引業協会の指針）を確認していない。国内の規制文書に「秘密鍵の物理的分散保管」に関する記述があれば、日本の学会で発表する論文としては引く価値がある。

## 検証で削除したもの

該当なしである。2026年7月30日の検証では、明らかに存在しない文献であると判断できたものは1件もなかったので、削除は行っていない。書誌の一部を裏づけられなかった3件（Ledger Recoverの発表時期、Casasciusの販売開始年、Rivest・Shamir・Wagnerの報告番号）については、文献そのものは実在するため削除せず、それぞれの箇所に確認できなかった内容を書き添えるかたちで残した。

## 検証の記録

2026年7月30日に、検証担当者（この節を書いた者。調査担当者とは別の担当である）が、このファイルに書かれた文献と事例のすべてを独立に洗い直した。作業の方針は、調査担当者の記述をいっさい前提とせず、一件ずつ一次情報に当たって書誌と内容の主張を確かめることであった。

対象とした件数は、文献と事例を数えて54件である。内訳は次のとおりである。「新規性への脅威が大きい文献」の節に挙げられた8つの項目、文献の数では9件（codex32、Seed XOR、SeedQRとCompactSeedQR、CHI 2025のOf Secrets and Seedphrases、PCI PIN Security Requirements、DNSSECルート鍵署名鍵の運用実務、Naor と Shamir の視覚復号型秘密分散、大川と栃窪の論文、Cypherock X1）である。「背景として押さえるべき文献」の節に挙げられた42の項目、文献と事例の数では45件である。これに加えて、「未検証のまま残ったもの」に置かれていた8件についても、確認できるようになっていないかを再点検した。

確認の方法は次のとおりである。番号付き提案と規格と技術文書については、BIPとSLIPのリポジトリの原文、Blockchain Commonsのリポジトリの原文、RFC Editorの本文、NISTのCSRCの刊行物ページ、PCI Security Standards Councilが配布するPDF、IANAのDNSSEC手順書のページに直接当たった。PDFはローカルでテキストに変換し、本文を検索して該当箇所を読んだ。学術論文については、CrossrefのAPIで書誌を照合し、DOIが実際に当該の著者と表題と巻号ページを指していることを1件ずつ確かめた。ACM Digital LibraryはHTTP 403で開けなかったため、CHI 2025の論文は著者の業績ページから本文PDFを取得して数値の裏を取った。日本語文献については、情報処理学会電子図書館、CiNii Research、J-STAGE、日本大学の学術リポジトリの各レコードを直接開いた。製品と実務の事例については、各社の一次ページの本文を取得した。また生きているかどうかを確かめるために、ファイルに書かれたURLを54本まとめてHTTPで叩き、応答符号を確認した。GitHubの一部URLが一時的にHTTP 429を返したため、それらはraw.githubusercontent.comの原文で代替して確認した。dblpも一時的にHTTP 503を返したので、Crossrefと検索APIで補った。

訂正した件数は21件である。加えて1件を未検証から確認済みへ移した。主な訂正は次のとおりである。第一に、日本語文献の著者名の誤りを1件直した。「森安翔太・森山雅光」は、J-STAGEのメタデータでは「森安 昭太」「森山 真光」であり、二人とも名の字が違っていた。第二に、SmartCustodyの年を2020年から2019年（第1.01版）へ直し、書籍本体の章立てと、多重署名やSSKRや時間錠を扱うのが併載記事群であることを書き分けた。第三に、NIST SP 800-57 Part 1 Revision 5について、紙で金庫に置く運用と離れた場所への複製の根拠箇所を「第8.2節から第8.3節」から第6.2.2節（および第8.2.2.1節と第8.3.1節への参照）へ直した。第四に、HashiCorp VaultのShamir封印について、分割される対象がルート鍵ではなく解封鍵であることを直した。第五に、Blockstreamのブログ記事の記述について、30分から60分かかって二度行う必要があるのは検査符号の「作成」であり、検証は同じ時間で一度でよいという書き分けに直した。第六に、SeedSignerの文書の表題を「SeedQR Documentation および CompactSeedQR Specification」から実際の表題である「SeedQR Format Specification」へ直し、CompactSeedQRのビット数の説明を132ビットから検査ビット4ビットを引いた128ビットという正確な言い方に直した。第七に、Bytewordsの「先頭と末尾の2文字」という書き方が計4文字と読めてしまうので、「先頭1文字と末尾1文字の計2文字」に直した。第八に、Jameson Loppの試験機種数を「75機種以上」から原文どおりの「75機種」に直した。そのほか、NIST IR 8214の副題、NIST SP 800-152の表題の(CKMS)、岩下直行の論文の副題、Voskobojnikovらの共著者5名の全員、Krombholzらの予稿集刊行年、HouyらのCSUR掲載号の年、Kastnerらのページ範囲、Miyaharaらの巻とページ、Lindqvistらのページ範囲、SSKRの正式表題と正確な日付、RFC 2289の状態（本文の見出しはStandards Trackだが現在の状態はInternet StandardでSTD 61）、SATSCARDの10スロット構成、Cypherock X1の5分割、Trezorの断片配布先の表現、Armoryの版の日付、IANAの鍵儀式の第1回と最新回の日付、大川の学位論文の正式表題と授与日を補った。

実在が確認できず削除または未検証へ移した件数は0件である。すなわち、このファイルに書かれていた文献と事例は、削除に値するもの、つまり明らかに存在しないと判断できるものは1件もなかった。一方で、書誌の一部を一次情報で裏づけられなかったものが3件あり、それぞれ本文にその旨を書き添えた。Ledger Recoverの「2023年5月発表」という時期は当該ページに記載がなかったので記述から外した。Casasciusの「2011年から」という開始年は本人のサイトでは確認できず、確認できたのは2013年11月27日の販売停止だけであった。Rivest・Shamir・Wagnerの時間錠の報告番号 MIT/LCS/TR-684 はPDF本文のどこにも現れなかった。

逆に、未検証だったものを1件、確認済みへ移した。Solfa Cipherである。サイト本文を取得して、各文字を音階の階名と音長の組へ写す音楽的な暗号であること、鍵を変えると旋律の音が変わることを確認したので、「背景として押さえるべき文献」の節へ移し、脅威の度合いを低と判定した。

否定的な主張についても、可能な範囲で裏を取った。CHI 2025の論文の本文には隠蔽やステガノグラフィに関する記述がないという主張は、抽出した全文に対する語の検索で0件を確認した。WISS 2025の予稿集に暗号や鍵管理や秘密分散の発表がないという主張は、発表一覧のページを取得して語の検索で0件を確認した。Trezorの合言葉の解説ページがもっともらしい否認を謳っていないという主張も、当該ページの本文で確認した。

残る不確かさは3点である。第一に、有償の国際規格（ISO/IEC 19592、ISO 11568、ISO 13491、ANSI X9.24）の本文に到達できていない。ISOのカタログは今回もCloudflareの認証画面でHTTP 403となった。第二に、PCI PIN Security Requirementsの最新版を特定できていない。今回の検証時点でWeb検索の実行回数が上限に達しており、文書ライブラリを辿れなかった。第三に、EUROCRYPT '94の予稿集のLNCS巻番号を確定できていない。またNaor と Shamir の視覚復号型秘密分散については、dblpが会議年に合わせて1994年とする一方、SpringerがCrossrefへ登録した刊行年は1995年であるため、論文で引くときは会議年と刊行年を書き分けるのが安全である。
