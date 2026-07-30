# モデル共有基盤における3Dプリントの笛と情報を埋め込んだモデル

この文書は、CipherFluteの新規性を検討するために、3Dモデル共有基盤（MakerWorld、Printables、Thingiverse、Cults3D）に実際に公開されているモデルを一件ずつブラウザで開いて調べた結果である。学術論文ではなく実物のページを一次資料として扱い、確認したページのURLと、そのページ上で確認できた数値をそのまま記載した。数値はすべて2026年7月30日に確認したものである。

なお、この調査では検索エンジンの利用枠を使い切ったため、各基盤の内部検索機能とサイトマップを直接叩くという方法をとった。そのぶん基盤内部の網羅性は高いが、基盤の外側（ニュース記事や市場調査レポート）についてはWikipediaなどの二次資料に頼った箇所がある。該当箇所は明示した。

---

## この切り口の要約

3Dプリントできる笛は、モデル共有基盤において巨大かつ成熟したジャンルである。Printablesでは「whistle」の検索で1,150件が該当し、最上位のFlat Pocket Whistleは厚さ3mm、43×22mmで財布に入る平板型の笛で、いいね12,926件、ダウンロード97,000件、実作と書き込みの合計2,965件、リミックス99件に達している。MakerWorldでも同種の平板型笛や超大音量笛が数万ダウンロード級で多数存在する。したがってCipherFluteが前提とする「薄く小さくサポート材なしで平置き印刷でき、確実に鳴るフィップル笛」という工作技術それ自体は、すでにコミュニティの共有財産であって新規ではない。さらにdp makesのWhistle Pan Fluteは「長さの異なる笛を一列につないだ」構成を明言しており、CipherFluteの物理形態（複数の笛を融合した一体物）に最も近い先行実装である。音高の設計についても、ThreeD-Michaelは4.2kHzから23kHzまで周波数を明示した犬笛のシリーズを公開し、スマートフォンのアプリで周波数を検証する手順まで書いている。半音階を扱うモデルも存在し、Chromatic Pan Fluteの作者は「管長を理論値どおりに計算すると高音側が高くなりすぎて下げられないので全管に2cm足して直した」と書いており、CipherFluteが f = A/(L+e) の e で扱う端補正に相当する現象を経験的に把握している。

一方で、笛の音高を符号として情報を運ぶモデルは、4つの基盤のいずれにも1件も見つからなかった。多音笛はすべて「同時に鳴らして大音量や不快な音を作る」ためのものであり、1本ずつ順に吹いて記号列として読む発想は存在しない。他方、暗号資産の復元情報を3Dプリント物に「機械可読な符号として」載せる系譜はすでに確立している。QR SafeShareは秘密をShamirの秘密分散またはXORで分割し、各シェアを3MFとして書き出して3Dプリントする道具であり、脅威モデルの立て方（数学的な安全性は秘密分散だけが担い、物理層は走査コストを上げるだけ）がCipherFluteとほぼ同型である。SeedQRおよびその3Dプリント用テンプレートも同じ位置にある。CipherFluteの新規性は、この既存の系譜のなかで「読み出し経路が光学ではなく音である」ことと「日用品に偽装できる」ことに絞られる。

---

## 基盤の規模（公開されている数字）

第四の設問に対する回答である。各基盤の公式なプレスリリース上の数字は見つけられなかったので、各基盤が自ら公開しているサイトマップと検索画面の表示から数えた。サイトマップは検索エンジン向けに基盤自身が生成している一次データである。

| 基盤 | 公開モデル数の推定 | 数え方 |
|---|---|---|
| MakerWorld | 約2,329,861件 | サイトマップ索引（https://makerworld.com/sitemaps/index.xml ）に models.xml のページが p=0 から p=2329 まで2,330枚あり、1枚に10,000のURLが入るが、同一モデルが10言語分並ぶので1枚あたり1,000モデルである。最終ページ（p=2329）は8,610URL、すなわち861モデルであった。したがって2,329×1,000＋861＝2,329,861件となる。 |
| Thingiverse | 約2,248,046件 | sitemap_thing_1.xml から sitemap_thing_45.xml まで45枚あり、1枚50,000件、最終ページのみ48,046件であった。sitemap_thing_46.xml はHTTP 500を返し、45枚で打ち止めであることも確かめた。 |
| Printables | 約1,383,000件 | sitemap-model.xml が1,383ページあり、1ページ1,000件であった（最終ページ p=1383 も1,000件で満杯であった）。 |
| Cults3D | 3.5M（350万件）と自称 | 検索窓のプレースホルダに "Search 3.5M designs…" と表示される。ただし内訳の定義は示されていない。 |

- MakerWorldの1枚あたり1,000モデルという数え方は、実際に p=0 を取得して確かめた。10,000件のURLに含まれるモデルIDは1,000種であり、言語は en、zh、de、fr、it、es、ja、ko、sv、pt の10種であった。
- MakerWorldのサイトマップの先頭に置かれているモデルは、Bambu Lab自身が2023年4月13日に公開した「Bambu Christmas Cabin」（https://makerworld.com/en/models/12682-bambu-christmas-cabin 、投稿者名はBambu Lab、作成日時は2023-04-13、ダウンロード8,984件）である。サイトマップはモデルIDの昇順に並んでいるので、これが最古のモデルだと考えられる。つまりMakerWorldは公開から3年3か月で約233万件に達し、2008年開設のThingiverse（約225万件）を件数で追い抜き、Printables（約138万件）の1.7倍規模になっている。この成長速度は、CipherFluteが「日用品に埋め込んだモデルを配布する」ことを想定するうえでの流通基盤の実勢を示す数字として使える。
- 検索語「whistle」の該当件数は、Printablesが1,150件、Cults3Dが836件、MakerWorldが2,021件であった（いずれも2026年7月30日の再確認値である。前回の調査時点ではCults3Dが838件、MakerWorldが2,018件であった）。MakerWorldについては、検索画面の表示が「モデル (999+)」で打ち切られるため、件数は基盤自身の内部APIである https://makerworld.com/api/v1/search-service/select/all?keyword=... が返す design.total の値を用いた。ただしこの値はあいまい一致を含む緩い数字であって、厳密な該当件数としては扱えない。同じ方法で「ocarina」は1,180件、「pan flute」は1,069件を返す一方、笛と無関係な「flute cipher」でも1,191件、「shamir secret sharing」でも1,266件、「acoustic barcode」でも1,238件を返すからである。Thingiverseは検索結果が「Showing 10,000 results」で打ち切られるため件数が取れなかった（この打ち切り表示も再確認した）。
- Bambu Lab社の規模については、Wikipedia英語版のBambu Labの項に、年間売上が15億人民元に迫るというEqualOceanの記事が出典として挙げられている（https://en.wikipedia.org/wiki/Bambu_Lab 、出典の題名は "Bambu Lab, Consumer-Grade 3D Printing Manufacturer, Nears CNY 1.5 Billion in Annual Revene"、参照日は2025年2月11日）。この15億人民元という数字は出典の題名に現れるものであって、Wikipediaの本文が「2024年の」年間売上と明記しているわけではない。二次資料であり、EqualOceanの原典まで当たれていない。
- 業界地図として、Thingiverseは2026年2月12日にMyMiniFactoryに買収された。Thingiverse自身のブログ記事「Thingiverse joins the MyMiniFactory family!」（Arun Chapman、2026年2月12日、https://www.thingiverse.com/blog?p=thingiverse-joins-the-myminifactory-family ）で確認した。同記事は「MyMiniFactory has acquired 100% of Thingiverse」と明記している。Printablesを運営するPrusa Research、MakerWorldを運営するBambu Labと合わせ、造形機メーカーが共有基盤を垂直統合する構図になっている。

---

## 新規性への脅威が大きい文献

脅威の大きい順に並べた。ここでいう「文献」は、実際に公開されているモデルのページ、付随するソフトウェア、および仕様文書である。

### 1. QR SafeShare — 秘密をShamirの秘密分散で分割し、各シェアを3Dプリント可能なQRコードとして書き出す道具

- 題名: QR SafeShare – Split and protect secrets in QR codes / QR SafeShare
- 著者: Jurgen（GitHubのアカウント名は cmd1982）
- 発表: GitHubリポジトリの最初のコミットが2025年9月11日、MakerWorldに2026年1月14日公開、Printablesに公開（2026年7月26日更新）、専用サイトを併設
- 確認先のURL:
  - https://makerworld.com/en/models/2244875-qr-safeshare （投稿者名Jurgen、作成日時2026-01-14、ダウンロード0件、いいね1件、造形プロファイル0件）
  - https://www.printables.com/model/1419250-qr-safeshare-split-and-protect-secrets-in-qr-codes （投稿者名Jurgen、2026年7月26日更新、いいね2件、ダウンロード6件、閲覧159件、ファイル4個）
  - https://qrsafeshare.com/ （道具の本体。「split secrets into offline QR fragments」と掲げる）
  - https://github.com/cmd1982/qr-safeshare （スター3件、ライセンスは "QR SafeShare License (Non-Commercial)"、コミット129件。GitHub APIで確認したところ、リポジトリ作成と最初のコミット "Initial commit" がいずれも2025年9月11日、最後のプッシュが2025年10月5日であった）
- 内容の要約: ブラウザ内で完結する道具であり、パスワードや暗号資産の復元用フレーズを複数のQRコードに分割する。分割方式としてShamirの秘密分散（例として3個作って2個で復元する構成）とXORによる2分の2分割を選べる。各シェアを3MFファイルとして書き出せるので、そのまま3Dプリントして完全にオフラインの耐久バックアップにできる。作者は自ら「CryptoSteelは頑丈だが、泥棒に見つかればフレーズ全体が即座に渡ってしまう」「物理バックアップを2つに割るのも安全ではない、半分ずつが既に部分情報を漏らすからだ」と既存手法の弱点を整理し、そのうえで秘密分散に安全性を負わせている。さらに「QR SafeShare Sleeve」という覆いを併せて印刷することを勧め、その理由を「本気の攻撃者は壊して開けられるが、覆いはその場での素早い、気づかれない走査を防ぎ、不正なアクセスに必要な労力を上げる」と説明している。
- CipherFluteとの関係: CipherFluteの脅威モデルの骨格、すなわち「物理層と符号層には暗号学的な秘匿の力はまったく無い」「秘匿はShamirの秘密分散やSLIP-39だけが担う」「物理層が担うのは探索コストの引き上げと正当な利用者の手軽さだけである」という3点を、この道具はすでにそのまま実装し、文章として明言している。運ぶ情報も同じく暗号資産の復元用フレーズである。異なるのは読み出し経路だけであり、こちらは光学的なQRコード、CipherFluteは吹いた音である。
- 脅威の度合い: 高。CipherFluteの応用上の主張「3Dプリント物を秘密分散のシェアの器にする」と、脅威モデルの主張「安全性は秘密分散に、物理層は探索コストの引き上げに」の両方が、すでに実物として存在してしまっている。CipherFluteはこれを必ず引用し、差分を「読み出しが音であること」「日用品への偽装で符号の存在そのものを隠せること」「電源も撮像装置も不要で人間の口と耳だけで読めること」に明確に絞り込む必要がある。時間的な前後関係については、最初のコミットが2025年9月11日であることを確認したので、WISS 2026に投稿するCipherFluteからみて明確に先行する研究外の実装として扱わなければならない。
- 検証の注記: 上に引用した4つの文言は、いずれもPrintablesのページ本文に原文で存在することを確かめた。原文は "A CryptoSteel is tough, but if a burglar finds it, they instantly have your entire phrase."、"Splitting a physical backup in two isn't secure either, because each half already exposes part of your phrase and you yourself are left knowing only half of it."、"While a determined attacker could force it open, the sleeve prevents quick or unnoticed scans and raises the effort required for unauthorized access."、および "Each QR code on its own is worthless." である。Shamirの秘密分散を3個のうち2個で復元する例、XORによる2分の2分割、3MFでの書き出し、覆い（Sleeve）の推奨も、すべてページ本文に記述がある。

### 2. SeedQRとCompactSeedQR、およびその3Dプリント用テンプレート — 復元用シードを機械可読な符号として物理媒体に載せる確立した規格

- 題名: SeedQR（およびCompactSeedQR）仕様、ならびに「21x21 Modular QR-Code for Seedsigner」「21x21 SeedQR template」
- 著者: SeedSignerプロジェクト（仕様）、happy（アカウント名は happyonion_1659843、Printablesのモデル）、arlm（Cults3Dのフォーク）
- 発表: 仕様はSeedSignerのリポジトリに文書化、Printablesのモデルは2024年3月18日更新、Cults3Dのフォークは2025年3月20日公開
- 確認先のURL:
  - https://github.com/SeedSigner/seedsigner/tree/dev/docs/seed_qr （README.md、img、printable_templates を含む。本文は https://raw.githubusercontent.com/SeedSigner/seedsigner/dev/docs/seed_qr/README.md で確認した）
  - https://www.printables.com/model/786967-21x21-modular-qr-code-for-seedsigner （いいね11件、ダウンロード90件、閲覧952件、ファイル3個）
  - https://cults3d.com/en/3d-model/various/21x21-seedqr-template （投稿者arlm、2025年3月20日、無料。作者自身が「an unchanged fork」すなわち上記Printablesのモデルの無改変のフォークであると書いている）
- 内容の要約: SeedQRは、BIP39の復元用フレーズをQRコードに載せるための最小化された符号化方式である。標準方式は各語をBIP39単語表の索引（0から2047）に直し、4桁のゼロ詰め十進数として連結してQRの数値モードで詰める。CompactSeedQRは索引を11ビット二進数に直してビット列として連結し、末尾のチェックサムに相当するビット（12語で4ビット、24語で8ビット）は数学的に導けるので省く。仕様書の原文は「The checksum is trivially calculated from the prior bits」と述べている。この圧縮により12語のシードは25×25から21×21へ、24語は29×29から25×25へ縮み、金属板に手で打刻する面積が12語で61パーセント、24語で65パーセントに減る、すなわち35から40パーセント減る。以上の数値はすべて仕様書の本文で裏を取った。3Dプリント用テンプレートは70×70×6mmの板である（Printablesのページに "Dimension Plate: 70x70x6mm" と明記されている）。なお題名にある「Modular」が具体的にどういう組み替えを指すのかは、ページの説明文には書かれていない。
- CipherFluteとの関係: 「128ビットの復元用情報を、最小の物理量で、機械可読な符号として物理媒体に固定する」という問題設定が完全に一致している。CipherFluteが13スロットの語彙で1本あたり約3.7ビットを運び、40本から49本で128ビットを運ぶという計算をしているのに対し、CompactSeedQRは11ビット×12語からチェックサムを引いて128ビットにするという同じ最適化を、すでに規格として済ませている。チェックサムを省いて後で導く発想も、CipherFluteの誤り訂正符号の設計と同じ土俵にある。
- 脅威の度合い: 高。CipherFluteの「符号としての情報量の設計」と「復元用シードを物理媒体に載せる」という部分は、この規格の前でほとんど新規性を主張できない。CipherFluteは、SeedQRが撮像装置を必要とし、また模様として見れば符号の存在が明白であることに対して、音による読み出しと日用品への偽装がどう違うのかを述べる必要がある。なおCipherFluteの現在の先行研究一覧にはSLIP-39とSSKRが入っているが、SeedQRは入っていない。この抜けは埋めるべきである。

### 3. Bitcoin binary seed storage（BIP39 12語）とBitCard — クレジットカード大の3Dプリント板に穴でシードを符号化し、偽装で探索コストを上げると明言した実装

- 題名: Bitcoin binary seed storage. BIP39 12 words. / Bitcoin BitCard. Seed storage 1248 card size.
- 著者: ErnestoFer
- 発表: Thingiverse、2024年10月28日
- 確認先のURL:
  - https://www.thingiverse.com/thing:6811428 （題名「Bitcoin binary seed storage. BIP39 12 words.」、公開日2024年10月28日、いいね1件、コメント2件、ファイル1個）
  - https://www.thingiverse.com/thing:6811420 （題名「Bitcoin BitCard. Seed storage 1248 card size.」、公開日2024年10月28日、いいね12件、コメント0件、ファイル1個）
- 内容の要約: クレジットカードと同じ寸法の3Dプリント板であり、釘などで穴を開けて記録する。前者は最大12語を二進数に直して記録し、後者は最大24語をBIP39の公式単語表（bitcoin/bips のenglish.txt）の索引に直して記録する。作者は用途を3点挙げている。第一に、樹脂製なので金属探知機に反応せず空港を通過できる。第二に、財布に入るので携帯できる。第三に、「これらのカードの目的は暗号の層をもう一枚重ねることであり、12語や24語が何を意味するか完全に分かっている者からビットコイン保有者を守ることである」。原文は "the purpose of these cards is to add an extra layer of encryption, protecting bitcoiners from individuals who fully understand what 12/24 words mean" である。金属板の欠点を論じたポッドキャスト（Renato Amoedo教授の発言）が着想の元だと述べている。なお後者の題名にある「1248」が1・2・4・8の重みを指すことは、題名からの推測であって説明文には明記されていない。
- CipherFluteとの関係: CipherFluteが物理層に負わせている役割、すなわち「日用品への偽装によって探索コストを上げる」という論法が、そのままの言葉で書かれている。また媒体の形状（クレジットカード大の薄板）も、CipherFluteのカード実装と一致している。異なるのは、読み出しが目視と手作業であり、笛のような能動的な発音を伴わない点である。
- 脅威の度合い: 中。CipherFluteの主要な主張である音による読み出しは無傷だが、「カード形状の3Dプリント物にシードを符号として刻み、偽装で探索コストを上げる」という発想の部分は先行している。引用して差分を述べる必要がある。

### 4. Whistle Pan Flute — 長さの異なるフィップル笛を一列に融合した、サポート材なしで印刷できるモデル

- 題名: Whistle Pan flute
- 著者: dp makes
- 発表: Printablesに2023年のPrintables「Musical Instruments」コンテストの応募作として公開（最終更新2024年11月18日、入賞作）、MakerWorldに2023年8月8日公開
- 確認先のURL:
  - https://makerworld.com/en/models/13026-whistle-pan-flute （作成日時2023-08-08、ダウンロード49,149件、いいね12,767件、印刷36,729件、造形プロファイル9種、コメント4,738件、コレクション登録34,557件）
  - https://www.printables.com/model/444168-whistle-pan-flute （いいね10,835件、ダウンロード表示は「48 k」、閲覧135千件、実作と書き込みの合計516件、コレクション登録11,614件、レビュー370件）
- 内容の要約: 作者は説明文で「長さの異なる笛をつないで一列にすることでパンフルートを作るという私の考えは、面白く創造的なものだと思う」「注意深く笛を選んで並べれば、従来のパンフルートより広い音域が得られるかもしれない」と述べている。原文は "I think my idea of creating a \"Whistle Pan flute\" by connecting whistles of different lengths in a line is an interesting and creative one." および "By carefully selecting and aligning the whistles, it may be possible to achieve a greater range of notes than a traditional pan flute." である。印刷設定はサポートなし、層厚0.2mm、インフィル15パーセントである。「このモデルは進行中であり、良いホイッスル・フルートの音が出るモデルになるまで調律を続ける」とも書いている。無断転載を受けたためライセンスを再配布禁止に変更したという注記もある。Printablesのページには「Awarded in the contest Musical Instruments」と表示されており、385件の応募のなかで入賞していることも確認した。
- CipherFluteとの関係: CipherFluteの物理形態、すなわち「複数のフィップル笛を長さを変えて融合し、サポート材なしで平置き印刷する一体物」という構成に最も近い先行実装である。ダウンロード数が両基盤合計で約9万7千件に達しており、無名の実験ではなく広く知られたモデルである。
- 脅威の度合い: 中。CipherFluteが物理形態そのものを新規性として主張するなら、この1件で大きく弱まる。ただしこのモデルは楽器であって、各管を符号のスロットとして読む設計は無く、調律も作者が「継続中」と述べる段階にとどまる。CipherFluteは「複数の笛を融合する」ことではなく「融合した笛の集合を半音刻みのスロット語彙として読み、基準笛で正規化し、誤り訂正を付ける」ことに新規性を置くべきである。

### 5. Flat Pocket Whistle — 厚さ3mmで財布に入る平板型フィップル笛、Printablesの笛カテゴリ最上位

- 題名: Flat Pocket Whistle
- 著者: Jonas Daehnert（Printablesのアカウント名は PhoneDesigner）
- 発表: Printables、2023年6月以降に段階的に更新（最終更新2026年3月28日）
- 確認先のURL: https://www.printables.com/model/495173-flat-pocket-whistle （いいね12,926件、ダウンロード97,000件、実作と書き込みの合計2,965件、閲覧227,000件、リミックス99件、コレクション登録14,231件、レビュー1,154件、評価4.9）。ページ上のタブ表示は「Makes & Comments 2,965」であり、2,965件は実作報告と書き込みを合算した数である。実作報告だけの件数はページ上では分離されていない。
- 内容の要約: 厚さ3mmで財布に入り、平板でありながら非常に大きな音が出ると説明されている。音については「明瞭な二重音である。寸法が小さいため音はかなり高いが、注意を引くには十分である」と述べ、音声サンプルを添付している。原文は "It has a clear double tone. Due to the size, the sound is quite high. But it is enough to get attention. An audio sample is attached." である。寸法は43×22×3mm、43×22×4mm、43×22×5mm、39×11.5×3mmの4種である。印刷はノズル0.4mm、層厚0.2mm以下、外周2本、サポートなしを推奨し、「上下の壁厚が0.6mmしかないので第一層が完璧であることが極めて重要である」と書いている。うまく鳴らない場合の対処として層厚と外周数の調整、上下ソリッド層を各5層以上にすることを挙げている。
- CipherFluteとの関係: CipherFluteの発音体は厚さ4mm、幅7mmであり、この平板型笛と同じ設計空間にある。0.6mmの薄壁が第一層の品質に強く依存するという記述は、CipherFluteのメモにある「0.5mm壁は実機で安定造形できず無音になる」という経験と一致し、薄壁フィップル笛の造形限界がコミュニティで共有された知識であることを示す。
- 脅威の度合い: 中。CipherFluteの「厚さ4mmの平板でサポートなしに鳴る笛を作った」という工作面の主張は、この先行実装の前では新規性を主張しにくい。背景として必ず引用し、CipherFluteの寄与は薄板化ではなく符号化にあると位置づけ直すべきである。

### 6. 周波数を明示した犬笛のシリーズ（4.2kHzから23kHzまで） — 目標周波数を狙って印刷し、スマートフォンで検証する実践

- 題名: Dog Whistle 7 kHz、10 kHz Dog Whistle、Ultrasonic Dog Whistle 21 kHz、Ultrasonic Dog Whistle 23 kHz、Dog Whistle 9 kHz、18 kHz Dog Whistle、Dog Whistle 4.2 kHz、First 3d printable Ultrasonic Whistle ほか
- 著者: ThreeD-Michael（Printablesのアカウント名は ThreeDMichael）
- 発表: Printables（7kHz版、10kHz版、23kHz版はいずれも2024年3月17日更新）およびMakerWorld
- 確認先のURL:
  - https://www.printables.com/model/808031-dog-whistle-7-khz （いいね638件、ダウンロード5,852件、閲覧13,000件、実作と書き込みの合計50件、レビュー35件、評価4.9）
  - https://www.printables.com/model/664240-10-khz-dog-whistle （いいね1,224件、ダウンロード9,376件、閲覧24千件、レビュー69件）
  - https://www.printables.com/model/732469-ultrasonic-dog-whistle-23-khz （いいね1,014件、ダウンロード13.3千件、閲覧26千件、レビュー68件、評価4.3）
  - https://makerworld.com/en/models/151111-ultrasonic-dog-whistle-23-khz （作成日時2024-01-21、ダウンロード18,185件、いいね2,316件、印刷15,438件）
  - https://www.printables.com/@ThreeDMichael/models （公開モデル76件。笛の系列として Dog Whistle 4.2 kHz、Long Range Dog Whistle 5.2 kHz／5.7 kHz／6.2 kHz、Dog Whistle 7 kHz、Dog Whistle 9 kHz、10 kHz から19 kHz までの各1kHz刻み、Ultrasonic Dog Whistle 21 kHz／22 kHz／23 kHz、First 3d printable Ultrasonic Whistle、Ultimate Referee Whistle、Loudest Emergency Whistle、Steam Train Whistle が並んでいることを一覧で確認した。すなわち周波数を明示した笛の下限は4.2kHz、上限は23kHzである）
- 内容の要約: 作者は「安定した周波数」を特徴として掲げ、犬ごとに反応する周波数が違うので音高の異なる一連の笛を用意したと説明している。印刷条件として線幅0.4mm、層厚0.2mm、上下6層を指定し、さらに「Zシームが笛の内部の狭い空気通路に来てはいけない」としてシーム位置を画像で指定し、Cura、PrusaSlicer、Bambu Studioでのシーム制御の設定名まで書いている。仕上げの鋭いエッジを得るために低速で印刷せよとも書く。周波数を確認したい人にはAndroidの測定アプリを案内している。23kHzのモデルでは「波長が短いため笛の内部の微細構造が0.4mmノズルの限界に達しており、すべてのプリンタでは動作しない」「22kHzでは多くのスマートフォンが録音できない」と限界を明示している。
- CipherFluteとの関係: 「目標周波数を決めて笛を設計し、印刷し、スマートフォンで実測して確認する」という作業ループが、すでにコミュニティの標準的な実践として成立していることを示す。CipherFluteが13スロットの半音刻みを設計するときの前提技術は、この水準の知識のうえに乗っている。またZシームの位置が空気通路を塞ぐという指摘は、CipherFluteが実機で遭遇する造形不良（固まった不良に対するインターリーブの必要性など）と同じ問題である。
- 脅威の度合い: 中。CipherFluteが「印刷した笛の周波数を設計で狙える」ことを寄与として挙げるなら、この一連のモデルが先行する。ただし単一周波数の設計であり、スロット語彙、基準笛による正規化、誤り訂正は無い。差分を述べるために引用すべきである。

### 7. TeleTunes Octo Tune Major Flute / Whistle (F#) と3Dprintableflutes.comのカタログ — 平置きサポートなしで音階が出る笛の商業的な系列

- 題名: TeleTunes Octo Tune Major Flute / Whistle (F#)（MakerWorld上の正式な題名にハイフンは無い。前回の記載「Octo-Tune」は誤りである）
- 著者: Tele Tunes（アカウント名は TeleTunes）
- 発表: MakerWorld、2024年5月22日
- 確認先のURL:
  - https://makerworld.com/en/models/471686-teletunes-octo-tune-major-flute-whistle-f （作成日時2024-05-22、ダウンロード31,371件、いいね5,314件、印刷27,313件、造形プロファイル8種、コメント2,777件）
  - https://www.3dprintableflutes.com/ （販売サイト。トップページで確認できたのは Best Sellers、Latest Flutes、Maker's Picks の各4件という抜粋の掲示だけであり、掲載総数は表示されていない）
- 内容の要約: 捻れた管を持つ縦笛であり、F#メジャーの音階が出る。作者は「指穴を造形板側にして平らに印刷し、サポートは一切要らない」と明記している。演奏はネイティブアメリカンフルートやペニーホイッスルに近く、端から順に穴を開けて音階を上げるが、管が捻れているため上3つの穴だけ順序が反転する。印刷上の注意として「管楽器の3Dプリントは難しく結果はばらつく。小さな不完全さや寸法誤差が最終結果に大きく影響する。同じ機械、同じ設定、同じフィラメントでも複数回の印刷で異なる結果になりうる」と率直に書いている。風道を研磨すると音が明瞭になりオーバーブローも容易になるが調律に影響するとも述べている。説明文の末尾で自身のサイトに「70本以上の印刷可能な笛のカタログ」があると案内している。
- CipherFluteとの関係: 「平置き、サポートなし、指穴を下向き」という印刷方針はCipherFluteと同じである。さらに「同一条件でも印刷ごとに結果がばらつく」という記述は、CipherFluteが基準笛による比読みを導入する動機（気温や息の強さだけでなく造形のばらつきも吸収する必要がある）を外部から裏づける。F#メジャーという調の選択が、CipherFluteのクリーン域F#6からF#7と偶然一致しているのも興味深い。
- 脅威の度合い: 中。音階が出る印刷笛の設計と、その調律の難しさに関する実務知識が先行しているため、CipherFluteは「音高を設計できる」ことではなく「音高のばらつきを基準笛と誤り訂正で工学的に押さえ込んだ」ことを寄与として立てる必要がある。

### 8. 多音笛の系列（12音、6音、4音、3音、8音） — 複数のフィップルを一体化して同時に鳴らすモデル群

- 題名と著者、確認先のURL:
  - Infinity Whistle!  12 Tone.  Extremely Loud Benchy（bloodVixen、2024年7月29日、ダウンロード13,985件、いいね3,589件、印刷10,128件）https://makerworld.com/en/models/562104-infinity-whistle-12-tone-extremely-loud-benchy
  - Super Loud 6 Tone Whistle - Thunderstorm V4（Chox、2026年7月1日、ダウンロード17,697件、いいね4,772件、印刷17,118件。公開から1か月足らずの新作であり、数字は日ごとに増えている）https://makerworld.com/en/models/2999228-super-loud-6-tone-whistle-thunderstorm-v4
  - Echo | 3 tone whistle（LetsMakeThings、2015年12月12日、いいね24,731件、実作134件、リミックス7件、書き込み169件）https://www.thingiverse.com/thing:1192426
  - Micro fischietto bitonale（ACstudio、2025年3月6日、ダウンロード20,483件、いいね3,927件、印刷15,475件）https://makerworld.com/en/models/1181642-small-two-tone-whistle 。MakerWorldに登録されている題名はイタリア語の「Micro fischietto bitonale」であり、英語圏の表示や短縮URLに現れる「Small Two Tone Whistle」は自動翻訳と短縮URLの側の表記である。
  - Eight whistles ( 8 grams of consumables required)（淘淘和小年糕、2025年5月12日、ダウンロード80件、いいね24件、印刷56件）https://makerworld.com/en/models/1408568-eight-whistles-8-grams-of-consumables-required
- 内容の要約: いずれも複数の共鳴室を一体に持ち、一度に吹いてすべてを同時に鳴らす設計である。12音のInfinity Whistleは「息子と一緒に、これまでで最も強烈なものを作った。12の別々の音、耳を貫くほど大きい」「サポートは不要である」と述べ、後継版では「壁を厚くし、3つのサイズを用意し、ポートを調律した（tuned ports）」と書いている。Echoは「3Dプリンタで最も大きな笛を作るという着想から始まった」もので、印刷は横倒しが最も大きく鳴るとし、サポートは不要である。8音のモデルも「サポート不要の超大音量」であり、超薄型笛の設計を発展させて8グラムで印刷できるとする。
- CipherFluteとの関係: 「複数のフィップルを一体化する」構造はすでに一般的である。ただし目的が音量と不快さの最大化であり、各音を個別に、順番に、独立した記号として鳴らす発想はどのモデルにも無い。CipherFluteの符号化はここを分岐点にしている。
- 脅威の度合い: 中。物理構造の新規性を弱める一方で、符号化の新規性を際立たせる。引用して「先行は同時発音による音量最大化であり、本研究は逐次発音による記号列である」と書き分けるべきである。

### 9. 半音階パンフルートと端補正の経験知 — 管長の理論値を実測で補正した記録

- 題名: Chromatic pan flute 7 Octave Customisable、Chromatic Pan Flute 4 octave Tunable、Chromatic DOUBLE BASS pan flute 4 octave Tunable、およびその原典 Chromatic Tenor Panflute
- 著者: AskMe（アカウント名は AskMe_221856、リミックス）、Caran（原典）
- 発表: Printables（7オクターブ版は2023年4月7日更新、4オクターブ版は2023年4月6日更新、いずれもPrintablesの「Musical Instruments」コンテストへの応募作）、Thingiverse（Caran版は2015年11月14日）
- 確認先のURL:
  - https://www.printables.com/model/442532-chromatic-pan-flute-7-octave-customisable （いいね54件、ダウンロード203件、閲覧1,565件、ファイル61個。更新日はページ上では April 7, 2023 と表示される。前回の記載「2023年4月8日更新」は1日ずれていた）
  - https://www.printables.com/model/139274-chromatic-pan-flute-4-octave-tunable （いいね26件、ダウンロード169件、閲覧1,297件、ファイル16個、更新日 April 6, 2023）
  - https://www.thingiverse.com/thing:1129462 （題名は「Chromatic Tenor Panflute」、著者Caran、2015年11月14日、いいね85件、書き込み4件、実作1件。説明文に "A chromatic panflute from C3 to C6" および "Prints without supports" とあることを確認した）
- 内容の要約: C2からC9までの半音階のパンフルートである。AskMeは原典の問題点を次のように記録している。「元のモデルには大きな問題があった。管は正確にその音になるように計算されていたが、高い音では高すぎて、下げる方向に調律できなかった。そこで全部の管に2cm足して直した」。原文は "The original had a major issue. The tubes where calculates to be exactly on the right note. But for the high ones they were too high and one cannot tune it down. So I have corrected the model by adding it 2 cm on all the tubes." である。調律は蜜蝋で行うと指示し（"You'll must tune it with bee wax!"）、音域ごとに必要なノズル径（C8からC9は0.4mm以下、C2からC3は1mm以上）を細かく書き分けている。原典のCaranのモデルはサポートなしで印刷でき、大きなプリンタが無ければ管を個別に印刷してエポキシで接着するという分割方法を示している。
- CipherFluteとの関係: 「管長から周波数を計算すると高音側で系統的にずれ、一律の補正が必要である」という現象を、コミュニティが実測で把握して対処している記録である。CipherFluteが f = A/(L+e) の e として定式化した端補正に対応する。またPrintablesの「Musical Instruments」コンテスト（2023年4月1日から5月31日23時59分まで、応募385件、1人あたり5件まで、https://www.printables.com/contest/368-musical-instruments ）は、印刷可能な楽器の設計が組織的に大量生産された場であり、印刷笛の技術水準を示す指標として使える。前回の記載では終了日を6月1日としていたが、コンテストのページは "April 1, 2023 – May 31, 2023 at 11:59 PM" と表示している。運営側は「すべての有効な応募作は演奏でき音が出なければならない。楽器に見えるだけで鳴らない玩具は求めない」と条件を明記している。
- 脅威の度合い: 中。CipherFluteの f = A/(L+e) は、この経験知を素直に定式化しただけと見なされる余地がある。CipherFluteは、単に補正するのではなく較正定数を実測で求め、13スロットを100セント刻みで安全に分離できることを検証した点に寄与を置くべきである。

---

## 背景として押さえるべき文献

脅威の度合いは低いが、CipherFluteの位置づけを説明するために有用な実物である。

- Loud Whistle（Federico、MakerWorld、作成日時2024-01-02、ダウンロード90,546件、いいね12,817件、印刷78,447件、https://makerworld.com/en/models/119995-loud-whistle ）は、120dBを謳う笛である。説明文には設計者の氏名としてFederico Franceschelliが記されている。今回確認したMakerWorldの笛のなかで最多のダウンロード数であるが、MakerWorldの検索はダウンロード数での並べ替えが効かず全件を通した順位が取れないため、「MakerWorldで最も普及した笛」と断定はできない。前回の記載はこの点で言い過ぎであった。いずれにせよ印刷笛が一般家庭で日常的に量産されている現実を示す。
- Mini Flat Whistle - Flat Design, Full Power（ACstudio、MakerWorld、作成日時2025-12-10、ダウンロード13,608件、いいね3,097件、https://makerworld.com/en/models/2099305-mini-flat-whistle-flat-design-full-power ）は、「財布に入れて邪魔にならないように、より平たく、より小さく」と明言する平板型笛であり、CipherFluteのカード実装と同じ携帯形態を狙っている。説明文はイタリア語であり、原文は "più piatto, più piccolo e con la stessa potenza! Pensato per poter essere inserito comodamente in un portafogli senza dare il minimo fastidio" である。作者は笛だけを集めたコレクション（https://makerworld.com/it/collections/5266584-whistles ）を運営している。
- Whistle Magic - create your own whistle - Your Whistle your Music（nischi、Thingiverse、2013年2月4日、いいね1.3千件、リミックス1,800件、実作26件、書き込み35件、https://www.thingiverse.com/thing:46825 ）は、OpenSCADによる媒介変数化された笛の生成器である。高さ、半径、内部の穴、内球を変えて「たくさんの違う音」を作れると書くが、音名や周波数との対応は与えていない。媒介変数化の系譜として引ける。前回は題名を「Whistle Magic - create your own whistle」と短く記していたが、正式な題名は上記のとおり後半まで続く。
- Recorder / Flute Musical Instrument（HumbleBee、MakerWorld、作成日時2025-02-25、ダウンロード9,328件、いいね2,529件、https://makerworld.com/en/models/1149042-recorder-flute-musical-instrument ）は、C管のバロック式ソプラノリコーダー（説明文ではPeripole Baroque Soprano recorder PB6000を範としたと述べている）を模したモデルであり、「作ったとおりでよく鳴り、すべての音が正しい音高で出る」と主張する。原文は "The 3D model as built plays great and all the notes come out at the right pitch and sound." である。印刷楽器が実用的な調律に達しうるという主張の例である。
- Native American Drone Flute（F#、A=432hz）（MakerWorldの投稿者はblackpixel、作成日時2025-06-04、ダウンロード4,205件、いいね1,154件、https://makerworld.com/en/models/1485827-native-american-drone-flute-f-a-432hz ）は、基準ピッチをA=432Hzと明記し、設計の主要な参考文献としてflutopedia.comを挙げている。「造形板から出た状態で調律されているはずだが、材料設定や穴径をいじる必要があるかもしれない」とも書かれている。ただし説明文は "From the original author:" と前置きして引用されており、blackpixelは再投稿者であって原設計者ではない。引用するときは原設計者が別人であることに注意が必要である。
- PANPIPES - PAN FLUTE（Savy_Maker、MakerWorld、作成日時2025-02-25、ダウンロード11,696件、いいね2,893件、https://makerworld.com/en/models/1148458-panpipes-pan-flute ）は、一体で全音が出ると謳い、サポート不要で速く印刷できるとする。原文は "With this little pan flute you can play all the notes. 1 PIECE NO SUPPORTS EASY AND FAST PRINT" である。
- Stimmbare Panflöte in C-Dur (2 Oktaven) C´-C´´´（g3d-Solutions、MakerWorld、作成日時2025-02-27、ダウンロード600件、いいね205件、https://makerworld.com/en/models/1157247-tunable-pan-flute-in-c-major-2-octaves-c-c ）は、ねじ込み栓と8×2の密封リングで各管の長さを最大5mm変えて精密に調律する仕組みを持つ。栓は6mmの六角レンチで回す。管は15本、音域はC´からC´´´である。物理的な後調律の実装例である。なおMakerWorldに登録されている題名はドイツ語であり、「Tunable pan flute in C major 2 octaves」は短縮URLと自動翻訳の側の表記である。
- 32-note pipe organ（Chrysibulum、MakerWorld、作成日時2025-12-23、ダウンロード609件、いいね414件、印刷103件、https://makerworld.com/en/models/2151850-32-note-pipe-organ ）は、G3からD6までの32鍵の本格的なパイプオルガンである。歴史的ピッチ（A415、A392、A466）に対応し、風圧の測定値（65mm、すなわち2 5/8インチ水柱で発音調整した）と単管の音圧（80から85dBA、和音では90dBAを超える）まで記録している。印刷部品数について説明文は「鍵盤に204点、ストップト・フルート管に158点、ストリング・プリンシパル管に139点」と別々に書いており、合計501点は当方が足した数である。印刷した気柱楽器の到達点として引ける。
- 音量のための多音笛はきわめて多い。実在を確かめた例として、Ultimative Trillerpfeife mit 3 Tönen（Scheggy、ダウンロード1,352件、https://makerworld.com/en/models/1066613 ）、超大声哨子、口哨、125 db三频、户外求生、带孔可挂绳（22min）（3D Miker、ダウンロード17,908件、https://makerworld.com/en/models/1617101 ）、双响口哨 超过130dB（Hung3d、ダウンロード791件、https://makerworld.com/en/models/2821933 ）、Low Pitch Dual-Frequency Whistle | 125dB+ | 1.7g（Radu | Design & 3D、https://makerworld.com/en/models/3007466 ）がある。いずれも音量のための多音であり、音高を情報として使わない。前回はこれらを「Ultimate Triller Whistle with 3 tones」「Super Loud Whistle 125 dB Triple Tone」「Dual Tone Whistle over 130dB」「Low pitch dual frequency whistle 125dB 1.7g」という英語の題名で挙げていたが、実際に登録されている題名はドイツ語や中国語であり、英語表記は自動翻訳を写したものであった。多音笛の題名を引用するときは、必ずモデルIDとともに原語の題名を書くべきである。
- 1880 "Secret" Whistle. Really Loud! Easy print :)（bloodVixen、MakerWorld、作成日時2026-05-18、ダウンロード14件、いいね10件、https://makerworld.com/en/models/2819109-1880-secret-whistle-really-loud-easy-print ）は、Popular Science Monthly第33巻（1888年6月）の記事「Whistles Ancient and Modern」に載った設計の再現である。「secret」の意味は「指で環を閉じないと可聴音が出ない」ことであり、情報の秘匿とは無関係である。原文は "The \"secret\" was that it produces no audible sound without the fingers closing the ring" である。題名は1880年としているが説明文の出典は1888年であり、作者自身の記述のなかで年が食い違っている。「秘密の笛」という語がすでに別の意味で使われていることを注意点として押さえておく価値がある。
- Pocket Whistle with secret compartment（H2Jack Concepts、MakerWorld、作成日時2026-02-04、ダウンロード457件、いいね345件、https://makerworld.com/en/models/2348284-pocket-whistle-with-secret-compartment ）は、笛と収納室を組み合わせた唯一の例だが、収納するのは薬（鎮痛剤、抗生物質、ビタミン、乳糖分解酵素の錠剤などを例示している）であり、情報を音高で運ぶ発想は無い。二重音で約118dBを謳う。
- QR Code Generator（SnaKKo、MakerWorld、作成日時2024-05-27、ダウンロード32,384件、いいね12,390件、https://makerworld.com/en/models/476280-qr-code-generator-qrcode-for-mail-wifi-ect ）は、OpenSCADでQRコードを立体化する媒介変数モデルであり、テキスト、Wi-Fi、電話、vCardの4種を扱える。印刷物に光学符号を載せる系譜の代表であり、ダウンロード数の大きさから「符号を印刷する」需要の規模が読める。
- Secure Snap Card - Bitcoin Seed/Passphrase Backup（BlackHawk、MakerWorld、作成日時2025-06-01、ダウンロード40件、いいね18件、https://makerworld.com/en/models/1475714-secure-snap-card-bitcoin-seed-passphrase-backup ）は、8.5cm×5.5cmのカードを封入し、開けるには物理的に壊すしかないという容器である。作者は「不透明な紙を挟むか黒フィラメントで印刷して透過を防げ」と助言する。改竄の痕跡が残ることを安全性の根拠にしている。原文は "Once sealed, the only way to open it is by physically breaking the case, providing clear evidence if it's ever been tampered with." である。
- Secret text / Password vault for one-time opening（JesseZhang、MakerWorld、作成日時2025-10-29、ダウンロード86件、いいね57件、https://makerworld.com/en/models/1936443-secret-text-password-vault-for-one-time-opening ）は、印刷を一時停止して付箋を挿入し、そのまま封止するカードである。核のコードを収めた「The Biscuit」に着想したと述べる。内部の収納空間は45mm×80mm×1.2mmで、付箋を3枚から4枚重ねられるとする。印刷過程そのものを封止手段に使う例である。
- Seed Phrase Keeper - Bitcoin Recovery Codebook（SRRN、MakerWorld、作成日時2025-01-24、ダウンロード121件、いいね61件、https://makerworld.com/en/models/1031732-seed-phrase-keeper-bitcoin-recovery-codebook ）は、シードを一度も計算機に入力せずに記録するための文字タイルの集合であり、Scrabbleの文字出現頻度に合わせてタイル枚数を割り振っている。作者自ら「火災で樹脂が溶ける」という弱点を挙げ、2部作って別の場所に保管せよと勧めている。文字は24行の溝にあり継ぎで差し込み、最後に外側のあり継ぎで閉じて改竄が分かる封をするとしている。
- Cults3Dの「seed phrase」検索で得られた15件（https://cults3d.com/en/search?q=seed+phrase ）は、打刻用の治具、Trezor用の容器、封止式の金庫が中心であり、符号として情報を刻むものはSeedQRのテンプレート2件、すなわち「21x21 SeedQR template」と「25x25 SeedQR template」だけであった。いずれも無料である。
- Thingiverseの秘密関連モデル群として、Corrugated Secret Sign（mathgrrl、thing:548191）、SimpleCrypt: Pocket Tube Cipher（enrohtkcalb、thing:2728148）、Caesar Cipher Decoder Ring Rounded（cymon、thing:14891）、Caesar Cipher Decoder Ring Flat（cymon、thing:18315）、Morse code keychain - FDM remix（MegaSaturnv、thing:3641800）などがある。いずれも人間が手で解く暗号の道具であり、機械可読な符号ではない。前回はシーザー暗号の輪とモールス符号のキーホルダーの題名を短く記していたが、正式な題名は上記のとおりである。
- Wallet Card Morse Code（danyelol、MakerWorld、作成日時2024-02-14、ダウンロード8,454件、いいね4,524件、https://makerworld.com/en/models/186023-wallet-card-morse-code ）は、モールス符号の一覧を刻んだ財布サイズのカードである。符号表を印刷物に載せる例だが、情報そのものは載っていない。
- Cryptocurrency-seed break card vault（Heigre、Thingiverse、2018年1月15日、いいね140件、書き込み5件、https://www.thingiverse.com/thing:2757112 ）は、暗号資産の12語または24語のシードを収めるための「割って開ける」カード容器である。作者は核ミサイルの発射認証カードを模したと述べ、Ledger Nano Sに同梱される空欄のカードが収まる寸法にしている。中身をアルミ箔で包めば透過光や放射線による読み取りを防げるとし、印刷を封止の数層前で一時停止してカードを差し込み、そのまま閉じるという手順を示す。「カード自体の盗難は防げないが、誰にも見られていないことを保証し、見られた場合は改竄の痕跡で分かる」と、安全性の根拠を改竄検知に置いている。CipherFluteの脅威モデルと同じく物理層に暗号学的な力を求めていない好例である。
- Thingiverseの古い多音笛として、Multi-tone Whistle（conanh、2012年1月21日、いいね583件、https://www.thingiverse.com/thing:16286 ）、Duo Tone Whistle（jipvanleeuwenstein、2014年10月12日、いいね4.8千件、https://www.thingiverse.com/thing:497948 ）、Whistle（Zaggo、2009年9月23日、いいね2.7千件、https://www.thingiverse.com/thing:1046 ）がある。説明文を読んだところ、調律に関する記述はどれにも無かった。conanhのものはFox 40という審判用の笛を印刷できる形に作り直したもので、目的は「二重音で内玉が無い」ことの再現であり、8回の試作を要したと述べている。Zaggoのものは内玉を笛の中に一緒に印刷して後で折り取る設計であり、2009年という最初期の印刷笛である。いずれも音高を情報として使わない。
- Bitcoin seed coin（PeteLaric、Thingiverse、2019年3月10日、いいね18件、https://www.thingiverse.com/thing:3481293 ）は、シードを刻んだ硬貨状の板である。ABSで印刷すれば数千年もつとし、失われた鋳型法で金属に鋳造する手順も案内する。「樹脂製なので地面に埋めても金属探知機に反応しない」と述べる点はErnestoFerのカードと同じ論法である。JustinSDKのモデルの改変であるとも書いている。媒介変数化されてはいるが、符号化するのは人間が読む文字であって幾何形状ではない。

---

## 未検証のまま残ったもの

2026年7月30日の検証で確認が済んだものは、この節から本文の各節へ移した。以下は現在も裏が取れていないものである。

- Cults3Dの「Recovery Phrase Sealed Vault」（Bitcoin edition と no markings edition を含む3件、いずれもJP¥235）、「Hashpack cold seed」（無料）、「Cold-Storage Display Altar - Coin & Backup Plate Stand」（JP¥817）は、検索結果の一覧に題名と価格が載っていることまでは確認した（https://cults3d.com/en/search?q=seed+phrase ）。個別ページの説明文は読んでいないため、内部の符号化方式や脅威モデルの記述は不明である。有料モデルであり、説明文の全文が公開されていない可能性もある。
- 3dprintableflutes.com が「70本以上の印刷可能な笛のカタログ」を持つという記述は、MakerWorld上のTeleTunesの説明文に "my 70+ printable flute cataloque at www.3Dprintableflutes.com" とあることまでは確認した。しかしサイト側のトップページには Best Sellers、Latest Flutes、Maker's Picks の各4件という抜粋しか出ておらず、掲載総数の表示は無い。70本という数はサイト側では裏が取れていない。
- Bambu Lab社の年間売上が15億人民元に迫るという数値は、Wikipedia英語版のBambu Labの項が出典として挙げるEqualOceanの記事の題名に現れるものである。Wikipediaの本文がこれを2024年の売上と明記しているわけではなく、EqualOceanの原典にも当たっていない。造形機の出荷台数や市場占有率については、公開されている一次資料を見つけられなかった。
- Cults3Dが自称する「3.5M designs」は検索窓のプレースホルダ表示で確認したが、この数がCults3D自身に投稿されたモデルのみを指すのか、他基盤の索引を含むのかは判別できていない。
- MakerWorldの登録利用者数、累計ダウンロード数、累計印刷数といった全体統計は取得できなかった。https://makerworld.com/about と https://makerworld.com/en/about はいずれもHTTP 404を返す（前回の記載はHTTP 403としていたが、再確認では404であった）。Bambu Labのブログにも該当記事が見つからなかった。
- MakerWorldの検索が返す design.total の値は、あいまい一致を含む緩い数字である。厳密な該当件数として引用してはならない。今回の再確認で、笛と何の関係も無い「flute cipher」で1,191件、「shamir secret sharing」で1,266件が返ることを実際に確かめた。この値は「該当件数」ではなく「関連度で並べたときの候補集合の大きさ」に近いものだと考えるべきである。
- Printablesのモデル総数約138万件は、サイトマップの最終ページ（p=1383）がちょうど1,000件で満杯だったため、実際にはもう少し多い可能性がある。
- 前回「Super Loud Whistle 125 dB Triple Tone」として挙げた多音笛については、3D Miker の「超大声哨子、口哨、125 db三频、户外求生、带孔可挂绳（22min）」（https://makerworld.com/en/models/1617101 ）が最も近い候補だと判断したが、自動翻訳を経た英語表記との対応が一対一に決まらないため、同一のモデルであると断定できていない。

---

## この切り口で見つからなかったこと

ここに書くことは、CipherFluteの新規性の主張の根拠になる。いずれも、4つの基盤の内部検索を英語の複数の語彙で繰り返し、該当が無いことを確認した結果である。

1. **笛の音高を符号として情報を運ぶモデルは1件も存在しない。** MakerWorldで「acoustic code」「sound password」「whistle password」「whistle secret」「binary whistle」「whistle bit」「encode sound」「acoustic barcode」「flute cipher」「audio data」の10通りの検索を行ったが、返ってきたのはすべて大音量の笛、QRコード、吸音パネル、暗号解読の玩具であった。この10語について今回あらためて件数を取り直したところ、いずれも1,191件から1,808件という値を返した。前述のとおりこれはあいまい一致による候補集合の大きさであって、語の意味に対応する該当件数ではない。したがってこの否定的な結論は件数ではなく、返ってきたモデルを目で見て確かめたことに依拠している。Printablesでも「whistle」1,150件の上位36件を個別に確認したが、情報を運ぶ設計は無かった。Thingiverseの「secret message」検索でも、出てきたのは箱、シーザー暗号の輪、モールス符号のキーホルダーであった。すなわち「吹いた音の高さを読んで少量の秘密情報を復元する」という提案は、モデル共有基盤上に前例が無い。

2. **多音笛はすべて同時発音であり、1本ずつ順に吹いて記号列として読むものは無い。** 12音、8音、6音、4音、3音、2音の笛をすべて確認したが、どれも一度に吹いて全部を鳴らす設計であり、目的は音量、不快さ、警報である。「音の並びで情報を表す」という語彙は、どの説明文にも現れなかった。

3. **音高が既知の基準笛を混ぜて他の笛を比で読むという発想は、どのモデルにも無い。** 調律のばらつきに対する対処として基盤上に存在するのは、蜜蝋を詰める、ねじ栓で管長を変える、風道を研磨する、全管に一律の補正長を足すといった物理的な後調律だけである。測定時の正規化という考え方は見当たらない。

4. **誤り訂正符号を印刷物の符号に適用したモデルは無い。** 印刷される符号としてはQRコードが圧倒的に多く、そのReed–Solomon符号はQRコードの規格に内蔵されているので作者は意識しない。符号の設計者自身が誤り訂正を選んで付けた例は見つからなかった。SeedQRのCompactSeedQRがチェックサムのビットを省くという判断をしているのが、最も近い設計上の言及である。

5. **秘密分散を3Dプリント物に適用した例は、QR SafeShareのただ1件である。** MakerWorldで「shamir secret sharing」を検索しても、隠し引き出しや秘密の本型金庫といった無関係な物理的隠匿しか返らない。Printablesで「shamir」を検索した結果は2件で、どちらも人名や作品名の偶然の一致であった。この2件は2026年7月30日に再確認しており、内訳は shamir waldmann という利用者名の投稿した「Cup coaster Amsterdam logo」と、Samir という語を含む「Samir Duel Em Stars Tower of Fantasy Cosplay Prop」である。すなわち「秘密分散のシェアを3Dプリント物として配る」という設計は、基盤上でまだ1件しか実装されていない、きわめて薄い領域である。CipherFluteはこの薄い領域の2件目に当たる。

6. **日用品に偽装した情報保管モデルは、隠し収納の系譜しかない。** 「secret compartment」「hidden message」の検索で出てくるのは、本型の金庫、隠し引き出し、パズルボックス、日本の秘密箱である。いずれも中に物を入れる空洞であり、物体そのものの形状や音に情報を符号化して偽装するものではない。物体の形状に情報を持たせつつ日用品として通用させるという設計は見つからなかった。

7. **笛を日用品に埋め込んで、笛であること自体を隠したモデルは無い。** 「hidden whistle」「whistle disguised」「whistle in object」「whistle business card」「whistle spool」「whistle bookmark」で検索したが、笛は常に笛の形をしていた。ジッパー引き手、指輪、キーホルダーに付ける例はあるが、いずれも笛だと分かる外観である。唯一の例外である「secret compartment付きのポケット笛」も、笛の姿をしたまま薬を入れる容器である。

8. **和音を出す笛を情報表現に使った例は無い。** MakerWorldの「chord whistle」検索で返るのは3音や2音の大音量笛であり、和音という語で意図されているのは音の厚みである。楽理的な和音を情報の単位として扱う設計は見当たらない。

---

## 調べ残した穴

- MakerWorldのコメント欄と「実作報告（Makes）」を読んでいない。作者の説明文には書かれない実測周波数や、鳴らなかった条件の報告がコメント欄に蓄積している可能性が高い。特にFlat Pocket Whistleは実作と書き込みを合わせて2,965件あり、薄壁の造形限界に関する集合知が眠っているはずである。MakerWorld側でも、Whistle Pan fluteに4,738件、TeleTunes Octo Tuneに2,777件のコメントが付いていることを確認した。CipherFluteが「実機で鳴る条件」を論じるときの外部証拠として価値がある。
- Printablesの「remix」の系統樹をたどっていない。Flat Pocket Whistleには99件、Whistle Magicには1,800件のリミックスがあり、そのなかに音高を制御する派生や符号化に近い派生が混ざっている可能性を排除できていない。
- MakerWorldの「Maker Lab」および媒介変数化モデル（Customizer）の一覧を調べていない。利用者が寸法を指定して生成する仕組みのなかに、音名を選べる笛の生成器があるかもしれない。
- 中国語での検索を行っていない。MakerWorldは中国語圏の投稿が多く（八音笛の作者も中国語で書いている）、「口哨」「哨子」「暗号」「助记词」などの語で検索すれば、英語では引っかからないモデルが出る可能性がある。日本語での検索も、MakerWorldの表示が自動翻訳であるため原文の語彙とずれており、十分に試せていない。
- MyMiniFactory自体を調べていない。担当範囲の4基盤に入っていなかったが、Thingiverseを買収した基盤であり、有料モデルの比率が高いため、暗号資産の保管に関する商業モデルが集まっている可能性がある。
- Bambu LabとMakerWorldの規模を示す公式な数字を取れていない。MakerWorldのabout ページはHTTP 404であり、認証を通したブラウザで開いても存在しない。造形機の出荷台数や市場占有率については、CONTEXTなどの市場調査会社の公表値を報じた記事に当たる必要がある。
- Printablesの「Musical Instruments」コンテスト（2023年4月1日から5月31日、応募385件）の応募作を全件見ていない。2か月間に集中的に投稿された印刷楽器の集合であり、音高設計に関する記述の宝庫である可能性が高い。入賞作の一覧では、Hex ukulele（Tomek）、Steel String Mandolin（LoboCNC）、Electric Hurdy-gurdy（demagnetized）が上位3件であり、笛の系統ではPortable Air Horn（Wim V）、HEXADIDG（L3V3C）、Dragon Recorder（P1lotz）、Whistle Pan flute（dp makes）が入賞していることまでを確認した。
- MakerWorldの検索結果はサーバ側で描画されるため、URLを取得するだけでは結果一覧が読めない。今回はブラウザで実際に描画させてからモデルIDを拾い、IDごとに design API を叩いて原語の題名を取るという手順をとった。この手順を使えば網羅性を上げられるが、全件の走査は行っていない。

---

## 検証の記録

2026年7月30日に、この文書の書誌情報を独立に検証した。検証は原著者とは別の担当者が、この文書に書かれた記述を一度も前提とせず、すべて一次資料に当たり直すという方針で行った。

検証の方法は次のとおりである。MakerWorldとPrintablesは通常のHTTP取得に対してHTTP 403を返すため、実際のブラウザでページを開いて描画結果を読むという手順をとった。Thingiverseは取得自体はできるが、いいね数や公開日を含む本体が後から描画される仕組みなので、これもブラウザで開いた。MakerWorldについては各モデルの一次データである https://makerworld.com/api/v1/design-service/design/{ID} を直接取得し、題名、投稿者名、作成日時、ダウンロード数、いいね数、印刷数、造形プロファイル数、説明文の原文を得た。Printablesについては各モデルのページの描画結果から同じ項目を得た。Thingiverseについては各thingのページを描画し、いいね数はボタンのtitle属性に入っている正確な整数を読んだ。基盤の規模はサイトマップを実際に取得して数え、GitHubはWeb画面とGitHubのAPIの両方を用いた。Cults3D、Wikipedia、qrsafeshare.com、3dprintableflutes.com は通常のHTTP取得で読めた。

確認した対象は72件である。内訳はPrintablesが14件（モデル9件、コンテストのページ1件、検索2件、サイトマップ1件、投稿者の一覧1件）、Thingiverseが18件（thing 15件、サイトマップ1件、ブログ記事1件、検索1件）、MakerWorldが31件（モデル28件、サイトマップ1件、検索の件数取得1件、aboutページ1件）、Cults3Dが4件、GitHubが2件、その他のサイトが3件である。

訂正は40か所に加えた。内訳は、事実の誤りが1件、題名の誤りが9件、日付の誤りが2件、数の読み方の誤解が2件、断定が強すぎる記述の緩和が5件、時間の経過で動いた数値の更新が19件、未検証の節への移動が2件である。主なものを挙げる。

第一に、明確な事実の誤りが1件あった。Thingiverseの thing:6811420 について「ダウンロード12件相当の表示」と書かれていたが、この12はいいね数である。Thingiverseはthingのページにダウンロード数を表示していない。ダウンロード数を根拠にした記述は成り立たないので、いいね12件、書き込み0件と直した。

第二に、題名の誤りを9件直した。MakerWorldの471686は「TeleTunes Octo-Tune Major Flute/Whistle (F#)」ではなく「TeleTunes Octo Tune Major Flute / Whistle (F#)」である。MakerWorldの1181642に登録されている題名はイタリア語の「Micro fischietto bitonale」であり、1157247はドイツ語の「Stimmbare Panflöte in C-Dur (2 Oktaven) C´-C´´´」であり、1148458は「PANPIPES - PAN FLUTE」である。英語の題名は自動翻訳と短縮URLの側の表記であった。Thingiverseの thing:46825、thing:14891、thing:18315、thing:3641800 についても、正式な題名がもっと長いことを確かめて直した。MakerWorldの2819109も、正式には「1880 "Secret" Whistle. Really Loud! Easy print :)」である。この種の誤りは、自動翻訳された画面を見て英語に訳し戻したときに生じたものだと考えられる。MakerWorldのモデルを引用するときは、必ずモデルIDを併記し、design APIが返す原語の題名を使うべきである。

第三に、日付の誤りを2件直した。Printablesの442532の更新日は2023年4月8日ではなく4月7日である。Printablesの「Musical Instruments」コンテストの終了日は2023年6月1日ではなく5月31日である。

第四に、数の読み方に関する誤解を2か所直した。Printablesのモデルのページに出る「Makes & Comments」の数は実作報告と書き込みの合計であり、実作報告だけの件数ではない。Flat Pocket Whistleの2,965件と Dog Whistle 7 kHz の50件がこれに当たる。

第五に、時間の経過で動いた数値を19か所更新した。いいね数、ダウンロード数、印刷数、閲覧数は日ごとに増えるので、前回の値と数件から数十件のずれがあった。たとえばEcho | 3 tone whistleのいいね数は「24,700件」と丸めて書かれていたが、実際の値は24,731件である。公開から1か月足らずのSuper Loud 6 Tone Whistle - Thunderstorm V4はダウンロード数が17,681件から17,697件へ、いいね数が4,767件から4,772件へ動いていた。この種のずれは誤りではないが、論文で数字を引くときは確認した日付を必ず添えるべきである。

第六に、断定が強すぎる記述を3か所ゆるめた。MakerWorldのLoud Whistleを「最も普及した笛」と断定していたが、MakerWorldの検索はダウンロード数での並べ替えが効かず全件の順位が取れないため、「確認した範囲で最多」という言い方に直した。MakerWorldの多音笛4件の英語の題名は自動翻訳を写したものであったため、原語の題名とモデルIDに置き換えた。Wikipedia英語版がBambu Labの2024年の年間売上を約15億人民元と「記述している」という書き方も、実際には出典として挙がっているEqualOceanの記事の題名に現れる数字であって本文の記述ではないため、正確な言い方に直した。

第七に、確認が済んで未検証の節から本文へ移したものが5件ある。Thingiverseの thing:2757112、thing:3481293、thing:16286、thing:497948、thing:1046 である。とくに thing:3481293 については「シードを幾何形状に符号化している可能性」が疑問として残されていたが、説明文を読んだ結果、符号化するのは人間が読む文字であって幾何形状ではないことが分かった。またQR SafeShareのGitHubリポジトリの最初のコミットが2025年9月11日であることが分かったので、時間的な前後関係の疑問も解消した。

第八に、逆に未検証の節へ移した記述が1件ある。前回「Super Loud Whistle 125 dB Triple Tone」として挙げた多音笛は、自動翻訳を経た英語表記との対応が一対一に決まらず、どのモデルを指すのか断定できなかった。またMakerWorldのaboutページの応答はHTTP 403ではなくHTTP 404であった。

実在が確認できず削除した文献は無い。この文書に挙げられた文献と事例は、モデルの題名や数値の細部に上記の誤りがあったものの、すべて実在することを確認できた。

検証で裏が取れた重要な数値は次のとおりである。SeedQR仕様の符号長（標準方式が12語で25×25、24語で29×29、CompactSeedQRが12語で21×21、24語で25×25、打刻面積が12語で61パーセント、24語で65パーセントに減る）は、SeedSignerのリポジトリのREADME.mdの本文と完全に一致した。基盤の規模（MakerWorld約233万件、Thingiverse約225万件、Printables約138万件）は、サイトマップを実際に数えて再現できた。Thingiverseが2026年2月12日にMyMiniFactoryに買収されたという記述は、Thingiverseのブログ記事の本文に "MyMiniFactory has acquired 100% of Thingiverse" とあることで裏が取れた。QR SafeShareの脅威モデルに関する4つの引用も、Printablesのページの原文と一致した。

残る不確かさとして最も大きいのは、MakerWorldの検索が返す件数の意味である。今回、笛と何の関係も無い語でも1,000件から2,000件が返ることを実測で確かめた。この文書の否定的な結論、すなわち「笛の音高を符号として情報を運ぶモデルは1件も無い」という主張は、件数ではなく実際に返ってきたモデルを目で確かめたことに依拠している。したがってこの主張の強さは、走査したモデルの件数がどれだけあったかに依存する。CipherFluteの論文でこの否定的な結論に触れるなら、「網羅的に検索したが無かった」ではなく「上位N件を目視で確かめたが無かった」という形で、確かめた範囲を明示して書くのが誠実である。
