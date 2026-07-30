# モデル共有基盤における3Dプリントの笛と情報を埋め込んだモデル

この文書は、CipherFluteの新規性を検討するために、3Dモデル共有基盤（MakerWorld、Printables、Thingiverse、Cults3D）に実際に公開されているモデルを一件ずつブラウザで開いて調べた結果である。学術論文ではなく実物のページを一次資料として扱い、確認したページのURLと、そのページ上で確認できた数値をそのまま記載した。数値はすべて2026年7月30日に確認したものである。

なお、この調査では検索エンジンの利用枠を使い切ったため、各基盤の内部検索機能とサイトマップを直接叩くという方法をとった。そのぶん基盤内部の網羅性は高いが、基盤の外側（ニュース記事や市場調査レポート）についてはWikipediaなどの二次資料に頼った箇所がある。該当箇所は明示した。

---

## この切り口の要約

3Dプリントできる笛は、モデル共有基盤において巨大かつ成熟したジャンルである。Printablesでは「whistle」の検索で1,150件が該当し、最上位のFlat Pocket Whistleは厚さ3mm、43×22mmで財布に入る平板型の笛で、いいね12,926件、ダウンロード97,000件、実作報告2,965件、リミックス99件に達している。MakerWorldでも同種の平板型笛や超大音量笛が数万ダウンロード級で多数存在する。したがってCipherFluteが前提とする「薄く小さくサポート材なしで平置き印刷でき、確実に鳴るフィップル笛」という工作技術それ自体は、すでにコミュニティの共有財産であって新規ではない。さらにdp makesのWhistle Pan Fluteは「長さの異なる笛を一列につないだ」構成を明言しており、CipherFluteの物理形態（複数の笛を融合した一体物）に最も近い先行実装である。音高の設計についても、ThreeD-Michaelは4.2kHzから23kHzまで周波数を明示した犬笛のシリーズを公開し、スマートフォンのアプリで周波数を検証する手順まで書いている。半音階を扱うモデルも存在し、Chromatic Pan Fluteの作者は「管長を理論値どおりに計算すると高音側が高くなりすぎて下げられないので全管に2cm足して直した」と書いており、CipherFluteが f = A/(L+e) の e で扱う端補正に相当する現象を経験的に把握している。

一方で、笛の音高を符号として情報を運ぶモデルは、4つの基盤のいずれにも1件も見つからなかった。多音笛はすべて「同時に鳴らして大音量や不快な音を作る」ためのものであり、1本ずつ順に吹いて記号列として読む発想は存在しない。他方、暗号資産の復元情報を3Dプリント物に「機械可読な符号として」載せる系譜はすでに確立している。QR SafeShareは秘密をShamirの秘密分散またはXORで分割し、各シェアを3MFとして書き出して3Dプリントする道具であり、脅威モデルの立て方（数学的な安全性は秘密分散だけが担い、物理層は走査コストを上げるだけ）がCipherFluteとほぼ同型である。SeedQRおよびその3Dプリント用テンプレートも同じ位置にある。CipherFluteの新規性は、この既存の系譜のなかで「読み出し経路が光学ではなく音である」ことと「日用品に偽装できる」ことに絞られる。

---

## 基盤の規模（公開されている数字）

第四の設問に対する回答である。各基盤の公式なプレスリリース上の数字は見つけられなかったので、各基盤が自ら公開しているサイトマップと検索画面の表示から数えた。サイトマップは検索エンジン向けに基盤自身が生成している一次データである。

| 基盤 | 公開モデル数の推定 | 数え方 |
|---|---|---|
| MakerWorld | 約2,329,861件 | サイトマップ索引に models.xml のページが2,330枚あり、1枚に10,000のURLが入るが、同一モデルが10言語分並ぶので1枚あたり1,000モデルである。最終ページ（p=2329）は8,610URL、すなわち861モデルであった。 |
| Thingiverse | 約2,248,046件 | sitemap_thing_1.xml から sitemap_thing_45.xml まで45枚あり、1枚50,000件、最終ページのみ48,046件であった。 |
| Printables | 約1,383,000件 | sitemap-model.xml が1,383ページあり、1ページ1,000件であった（最終ページも1,000件で満杯であった）。 |
| Cults3D | 3.5M（350万件）と自称 | 検索窓のプレースホルダに "Search 3.5M designs…" と表示される。ただし内訳の定義は示されていない。 |

- MakerWorldのサイトマップに載る最古のモデルは、Bambu Lab自身が2023年4月13日に公開した「Bambu Christmas Cabin」（https://makerworld.com/en/models/12682-bambu-christmas-cabin ）である。つまりMakerWorldは公開から3年3か月で約233万件に達し、2008年開設のThingiverse（約225万件）を件数で追い抜き、Printables（約138万件）の1.7倍規模になっている。この成長速度は、CipherFluteが「日用品に埋め込んだモデルを配布する」ことを想定するうえでの流通基盤の実勢を示す数字として使える。
- 検索語「whistle」の該当件数は、Printablesが1,150件、Cults3Dが838件、MakerWorldが2,018件であった。ただしMakerWorldの件数はあいまい一致を含む緩い数字であり（「ocarina」で1,179件、「pan flute」で1,069件と、無関係な語でも同程度の値が返る）、厳密な該当件数としては扱えない。Thingiverseは検索結果が「Showing 10,000 results」で打ち切られるため件数が取れなかった。
- Bambu Lab社の規模については、Wikipedia英語版が2024年の年間売上を約15億人民元と記述している（https://en.wikipedia.org/wiki/Bambu_Lab ）。これは二次資料であり、原典まで当たれていない。
- 業界地図として、Thingiverseは2026年2月12日にMyMiniFactoryに買収された。Thingiverse自身のブログ記事「Thingiverse joins the MyMiniFactory family!」（https://www.thingiverse.com/blog?p=thingiverse-joins-the-myminifactory-family ）で確認した。Printablesを運営するPrusa Research、MakerWorldを運営するBambu Labと合わせ、造形機メーカーが共有基盤を垂直統合する構図になっている。

---

## 新規性への脅威が大きい文献

脅威の大きい順に並べた。ここでいう「文献」は、実際に公開されているモデルのページ、付随するソフトウェア、および仕様文書である。

### 1. QR SafeShare — 秘密をShamirの秘密分散で分割し、各シェアを3Dプリント可能なQRコードとして書き出す道具

- 題名: QR SafeShare – Split and protect secrets in QR codes / QR SafeShare
- 著者: Jurgen（GitHubのアカウント名は cmd1982）
- 発表: MakerWorldに2026年1月14日公開、Printablesに公開（2026年7月26日更新）、専用サイトとGitHubリポジトリを併設
- 確認先のURL:
  - https://makerworld.com/en/models/2244875-qr-safeshare （作成日2026-01-14、ダウンロード0件、いいね1件）
  - https://www.printables.com/model/1419250-qr-safeshare-split-and-protect-secrets-in-qr-codes （2026年7月26日更新、いいね2件、ダウンロード6件、閲覧158件）
  - https://qrsafeshare.com/
  - https://github.com/cmd1982/qr-safeshare （スター3件、非商用ライセンス）
- 内容の要約: ブラウザ内で完結する道具であり、パスワードや暗号資産の復元用フレーズを複数のQRコードに分割する。分割方式としてShamirの秘密分散（例として3個作って2個で復元する構成）とXORによる2分の2分割を選べる。各シェアを3MFファイルとして書き出せるので、そのまま3Dプリントして完全にオフラインの耐久バックアップにできる。作者は自ら「CryptoSteelは頑丈だが、泥棒に見つかればフレーズ全体が即座に渡ってしまう」「物理バックアップを2つに割るのも安全ではない、半分ずつが既に部分情報を漏らすからだ」と既存手法の弱点を整理し、そのうえで秘密分散に安全性を負わせている。さらに「QR SafeShare Sleeve」という覆いを併せて印刷することを勧め、その理由を「本気の攻撃者は壊して開けられるが、覆いはその場での素早い、気づかれない走査を防ぎ、不正なアクセスに必要な労力を上げる」と説明している。
- CipherFluteとの関係: CipherFluteの脅威モデルの骨格、すなわち「物理層と符号層には暗号学的な秘匿の力はまったく無い」「秘匿はShamirの秘密分散やSLIP-39だけが担う」「物理層が担うのは探索コストの引き上げと正当な利用者の手軽さだけである」という3点を、この道具はすでにそのまま実装し、文章として明言している。運ぶ情報も同じく暗号資産の復元用フレーズである。異なるのは読み出し経路だけであり、こちらは光学的なQRコード、CipherFluteは吹いた音である。
- 脅威の度合い: 高。CipherFluteの応用上の主張「3Dプリント物を秘密分散のシェアの器にする」と、脅威モデルの主張「安全性は秘密分散に、物理層は探索コストの引き上げに」の両方が、すでに実物として存在してしまっている。CipherFluteはこれを必ず引用し、差分を「読み出しが音であること」「日用品への偽装で符号の存在そのものを隠せること」「電源も撮像装置も不要で人間の口と耳だけで読めること」に明確に絞り込む必要がある。

### 2. SeedQRとCompactSeedQR、およびその3Dプリント用テンプレート — 復元用シードを機械可読な符号として物理媒体に載せる確立した規格

- 題名: SeedQR（およびCompactSeedQR）仕様、ならびに「21x21 Modular QR-Code for Seedsigner」「21x21 SeedQR template」
- 著者: SeedSignerプロジェクト（仕様）、happy（Printablesのモデル）、Cults3Dの投稿者（フォーク）
- 発表: 仕様はSeedSignerのリポジトリに文書化、Printablesのモデルは2024年3月18日更新
- 確認先のURL:
  - https://github.com/SeedSigner/seedsigner/tree/dev/docs/seed_qr
  - https://www.printables.com/model/786967-21x21-modular-qr-code-for-seedsigner （いいね11件、ダウンロード90件、閲覧951件）
  - https://cults3d.com/en/3d-model/various/21x21-seedqr-template
- 内容の要約: SeedQRは、BIP39の復元用フレーズをQRコードに載せるための最小化された符号化方式である。標準方式は各語をBIP39単語表の索引（0から2047）に直し、4桁のゼロ詰め十進数として連結してQRの数値モードで詰める。CompactSeedQRは索引を11ビット二進数に直してビット列として連結し、末尾のチェックサムに相当するビット（12語で4ビット、24語で8ビット）は数学的に導けるので省く。この圧縮により12語のシードは25×25から21×21へ、24語は29×29から25×25へ縮み、金属板に手で打刻する面積が35から40パーセント減る。3Dプリント用テンプレートは70×70×6mmの板であり、モジュールを組み替えて自分のSeedQRの模様を作る。
- CipherFluteとの関係: 「128ビットの復元用情報を、最小の物理量で、機械可読な符号として物理媒体に固定する」という問題設定が完全に一致している。CipherFluteが13スロットの語彙で1本あたり約3.7ビットを運び、40本から49本で128ビットを運ぶという計算をしているのに対し、CompactSeedQRは11ビット×12語からチェックサムを引いて128ビットにするという同じ最適化を、すでに規格として済ませている。チェックサムを省いて後で導く発想も、CipherFluteの誤り訂正符号の設計と同じ土俵にある。
- 脅威の度合い: 高。CipherFluteの「符号としての情報量の設計」と「復元用シードを物理媒体に載せる」という部分は、この規格の前でほとんど新規性を主張できない。CipherFluteは、SeedQRが撮像装置を必要とし、また模様として見れば符号の存在が明白であることに対して、音による読み出しと日用品への偽装がどう違うのかを述べる必要がある。なおCipherFluteの現在の先行研究一覧にはSLIP-39とSSKRが入っているが、SeedQRは入っていない。この抜けは埋めるべきである。

### 3. Bitcoin binary seed storage（BIP39 12語）とBitCard — クレジットカード大の3Dプリント板に穴でシードを符号化し、偽装で探索コストを上げると明言した実装

- 題名: Bitcoin binary seed storage. BIP39 12 words. / Bitcoin BitCard. Seed storage 1248 card size.
- 著者: ErnestoFer
- 発表: Thingiverse、2024年10月28日
- 確認先のURL:
  - https://www.thingiverse.com/thing:6811428 （いいね1件、コメント2件）
  - https://www.thingiverse.com/thing:6811420 （ダウンロード12件相当の表示、コメント0件）
- 内容の要約: クレジットカードと同じ寸法の3Dプリント板であり、BIP39の各語を二進数（前者）または1・2・4・8の重みの索引（後者）に直し、釘などで穴を開けて記録する。作者は用途を3点挙げている。第一に、樹脂製なので金属探知機に反応せず空港を通過できる。第二に、財布に入るので携帯できる。第三に、「これらのカードの目的は暗号の層をもう一枚重ねることであり、12語や24語が何を意味するか完全に分かっている者からビットコイン保有者を守ることである」。金属板の欠点を論じたポッドキャストが着想の元だと述べている。
- CipherFluteとの関係: CipherFluteが物理層に負わせている役割、すなわち「日用品への偽装によって探索コストを上げる」という論法が、そのままの言葉で書かれている。また媒体の形状（クレジットカード大の薄板）も、CipherFluteのカード実装と一致している。異なるのは、読み出しが目視と手作業であり、笛のような能動的な発音を伴わない点である。
- 脅威の度合い: 中。CipherFluteの主要な主張である音による読み出しは無傷だが、「カード形状の3Dプリント物にシードを符号として刻み、偽装で探索コストを上げる」という発想の部分は先行している。引用して差分を述べる必要がある。

### 4. Whistle Pan Flute — 長さの異なるフィップル笛を一列に融合した、サポート材なしで印刷できるモデル

- 題名: Whistle Pan flute
- 著者: dp makes
- 発表: MakerWorldに2023年8月8日公開、Printablesにも公開
- 確認先のURL:
  - https://makerworld.com/en/models/13026-whistle-pan-flute （ダウンロード49,148件、いいね12,766件、印刷36,729件、プロファイル9種）
  - https://www.printables.com/model/444168-whistle-pan-flute （いいね10.8千件、ダウンロード48.8千件）
- 内容の要約: 作者は説明文で「長さの異なる笛をつないで一列にすることでパンフルートを作るという私の考えは、面白く創造的なものだと思う」「注意深く笛を選んで並べれば、従来のパンフルートより広い音域が得られるかもしれない」と述べている。印刷設定はサポートなし、層厚0.2mm、インフィル15パーセントである。「このモデルは進行中であり、良いホイッスル・フルートの音が出るモデルになるまで調律を続ける」とも書いている。無断転載を受けたためライセンスを再配布禁止に変更したという注記もある。
- CipherFluteとの関係: CipherFluteの物理形態、すなわち「複数のフィップル笛を長さを変えて融合し、サポート材なしで平置き印刷する一体物」という構成に最も近い先行実装である。ダウンロード数が両基盤合計で約10万件に達しており、無名の実験ではなく広く知られたモデルである。
- 脅威の度合い: 中。CipherFluteが物理形態そのものを新規性として主張するなら、この1件で大きく弱まる。ただしこのモデルは楽器であって、各管を符号のスロットとして読む設計は無く、調律も作者が「継続中」と述べる段階にとどまる。CipherFluteは「複数の笛を融合する」ことではなく「融合した笛の集合を半音刻みのスロット語彙として読み、基準笛で正規化し、誤り訂正を付ける」ことに新規性を置くべきである。

### 5. Flat Pocket Whistle — 厚さ3mmで財布に入る平板型フィップル笛、Printablesの笛カテゴリ最上位

- 題名: Flat Pocket Whistle
- 著者: Jonas Daehnert（Printablesのアカウント名は PhoneDesigner）
- 発表: Printables、2023年6月以降に段階的に更新（最終更新2026年3月28日）
- 確認先のURL: https://www.printables.com/model/495173-flat-pocket-whistle （いいね12,926件、ダウンロード97,000件、実作報告2,965件、閲覧227,000件、リミックス99件、コレクション登録14,231件、評価4.90／1,154件）
- 内容の要約: 厚さ3mmで財布に入り、平板でありながら非常に大きな音が出ると説明されている。音については「明瞭な二重音である。寸法が小さいため音はかなり高いが、注意を引くには十分である」と述べ、音声サンプルを添付している。寸法は43×22×3mm、43×22×4mm、43×22×5mm、39×11.5×3mmの4種である。印刷はノズル0.4mm、層厚0.2mm以下、外周2本、サポートなしを推奨し、「上下の壁厚が0.6mmしかないので第一層が完璧であることが極めて重要である」と書いている。うまく鳴らない場合の対処として層厚と外周数の調整、上下ソリッド層を各5層以上にすることを挙げている。
- CipherFluteとの関係: CipherFluteの発音体は厚さ4mm、幅7mmであり、この平板型笛と同じ設計空間にある。0.6mmの薄壁が第一層の品質に強く依存するという記述は、CipherFluteのメモにある「0.5mm壁は実機で安定造形できず無音になる」という経験と一致し、薄壁フィップル笛の造形限界がコミュニティで共有された知識であることを示す。
- 脅威の度合い: 中。CipherFluteの「厚さ4mmの平板でサポートなしに鳴る笛を作った」という工作面の主張は、この先行実装の前では新規性を主張しにくい。背景として必ず引用し、CipherFluteの寄与は薄板化ではなく符号化にあると位置づけ直すべきである。

### 6. 周波数を明示した犬笛のシリーズ（4.2kHzから23kHzまで） — 目標周波数を狙って印刷し、スマートフォンで検証する実践

- 題名: Dog Whistle 7 kHz、10 kHz Dog Whistle、Ultrasonic Dog Whistle 21 kHz、Ultrasonic Dog Whistle 23 kHz、Dog Whistle 9 kHz、18 kHz Dog Whistle、Dog Whistle 4.2 kHz、First 3d printable Ultrasonic Whistle ほか
- 著者: ThreeD-Michael
- 発表: Printables（7kHz版は2024年3月17日更新）およびMakerWorld
- 確認先のURL:
  - https://www.printables.com/model/808031-dog-whistle-7-khz （いいね638件、ダウンロード5,852件、閲覧13,000件、コメント50件、評価4.9／35件）
  - https://www.printables.com/model/664240-10-khz-dog-whistle （いいね1.2千件、ダウンロード9.4千件）
  - https://www.printables.com/model/732469-ultrasonic-dog-whistle-23-khz （いいね1千件、ダウンロード13.3千件）
  - https://makerworld.com/en/models/151111-ultrasonic-dog-whistle-23-khz （ダウンロード18,182件、いいね2,316件）
- 内容の要約: 作者は「安定した周波数」を特徴として掲げ、犬ごとに反応する周波数が違うので音高の異なる一連の笛を用意したと説明している。印刷条件として線幅0.4mm、層厚0.2mm、上下6層を指定し、さらに「Zシームが笛の内部の狭い空気通路に来てはいけない」としてシーム位置を画像で指定し、Cura、PrusaSlicer、Bambu Studioでのシーム制御の設定名まで書いている。仕上げの鋭いエッジを得るために低速で印刷せよとも書く。周波数を確認したい人にはAndroidの測定アプリを案内している。23kHzのモデルでは「波長が短いため笛の内部の微細構造が0.4mmノズルの限界に達しており、すべてのプリンタでは動作しない」「22kHzでは多くのスマートフォンが録音できない」と限界を明示している。
- CipherFluteとの関係: 「目標周波数を決めて笛を設計し、印刷し、スマートフォンで実測して確認する」という作業ループが、すでにコミュニティの標準的な実践として成立していることを示す。CipherFluteが13スロットの半音刻みを設計するときの前提技術は、この水準の知識のうえに乗っている。またZシームの位置が空気通路を塞ぐという指摘は、CipherFluteが実機で遭遇する造形不良（固まった不良に対するインターリーブの必要性など）と同じ問題である。
- 脅威の度合い: 中。CipherFluteが「印刷した笛の周波数を設計で狙える」ことを寄与として挙げるなら、この一連のモデルが先行する。ただし単一周波数の設計であり、スロット語彙、基準笛による正規化、誤り訂正は無い。差分を述べるために引用すべきである。

### 7. TeleTunes Octo-Tune Major Flute/Whistle（F#）と3Dprintableflutes.comのカタログ — 平置きサポートなしで音階が出る笛の商業的な系列

- 題名: TeleTunes Octo-Tune Major Flute/Whistle (F#)
- 著者: Tele Tunes
- 発表: MakerWorld、2024年5月22日
- 確認先のURL:
  - https://makerworld.com/en/models/471686-teletunes-octo-tune-major-flute-whistle-f （ダウンロード31,370件、いいね5,314件、印刷27,312件、プロファイル8種）
  - https://www.3dprintableflutes.com/ （販売サイト。掲載モデルは十数種を確認した）
- 内容の要約: 捻れた管を持つ縦笛であり、F#メジャーの音階が出る。作者は「指穴を造形板側にして平らに印刷し、サポートは一切要らない」と明記している。演奏はネイティブアメリカンフルートやペニーホイッスルに近く、端から順に穴を開けて音階を上げるが、管が捻れているため上3つの穴だけ順序が反転する。印刷上の注意として「管楽器の3Dプリントは難しく結果はばらつく。小さな不完全さや寸法誤差が最終結果に大きく影響する。同じ機械、同じ設定、同じフィラメントでも複数回の印刷で異なる結果になりうる」と率直に書いている。風道を研磨すると音が明瞭になりオーバーブローも容易になるが調律に影響するとも述べている。説明文の末尾で自身のサイトに「70本以上の印刷可能な笛のカタログ」があると案内している。
- CipherFluteとの関係: 「平置き、サポートなし、指穴を下向き」という印刷方針はCipherFluteと同じである。さらに「同一条件でも印刷ごとに結果がばらつく」という記述は、CipherFluteが基準笛による比読みを導入する動機（気温や息の強さだけでなく造形のばらつきも吸収する必要がある）を外部から裏づける。F#メジャーという調の選択が、CipherFluteのクリーン域F#6からF#7と偶然一致しているのも興味深い。
- 脅威の度合い: 中。音階が出る印刷笛の設計と、その調律の難しさに関する実務知識が先行しているため、CipherFluteは「音高を設計できる」ことではなく「音高のばらつきを基準笛と誤り訂正で工学的に押さえ込んだ」ことを寄与として立てる必要がある。

### 8. 多音笛の系列（12音、6音、4音、3音、8音） — 複数のフィップルを一体化して同時に鳴らすモデル群

- 題名と著者、確認先のURL:
  - Infinity Whistle! 12 Tone Extremely Loud Benchy（bloodVixen、2024年7月29日、ダウンロード13,985件、いいね3,588件）https://makerworld.com/en/models/562104-infinity-whistle-12-tone-extremely-loud-benchy
  - Super Loud 6-Tone Whistle - Thunderstorm V4（Chox、2026年7月1日、ダウンロード17,681件、いいね4,767件、印刷17,099件）https://makerworld.com/en/models/2999228-super-loud-6-tone-whistle-thunderstorm-v4
  - Echo | 3 tone whistle（LetsMakeThings、2015年12月12日、いいね24,700件、実作134件、リミックス7件）https://www.thingiverse.com/thing:1192426
  - Small Two Tone Whistle（ACstudio、2025年3月6日、ダウンロード20,483件、いいね3,927件）https://makerworld.com/en/models/1181642-small-two-tone-whistle
  - Eight whistles, 8 grams of consumables required（淘淘和小年糕、2025年5月12日、ダウンロード80件、いいね24件）https://makerworld.com/en/models/1408568-eight-whistles-8-grams-of-consumables-required
- 内容の要約: いずれも複数の共鳴室を一体に持ち、一度に吹いてすべてを同時に鳴らす設計である。12音のInfinity Whistleは「息子と一緒に、これまでで最も強烈なものを作った。12の別々の音、耳を貫くほど大きい」「サポートは不要である」と述べ、後継版では「壁を厚くし、3つのサイズを用意し、ポートを調律した（tuned ports）」と書いている。Echoは「3Dプリンタで最も大きな笛を作るという着想から始まった」もので、印刷は横倒しが最も大きく鳴るとし、サポートは不要である。8音のモデルも「サポート不要の超大音量」であり、超薄型笛の設計を発展させて8グラムで印刷できるとする。
- CipherFluteとの関係: 「複数のフィップルを一体化する」構造はすでに一般的である。ただし目的が音量と不快さの最大化であり、各音を個別に、順番に、独立した記号として鳴らす発想はどのモデルにも無い。CipherFluteの符号化はここを分岐点にしている。
- 脅威の度合い: 中。物理構造の新規性を弱める一方で、符号化の新規性を際立たせる。引用して「先行は同時発音による音量最大化であり、本研究は逐次発音による記号列である」と書き分けるべきである。

### 9. 半音階パンフルートと端補正の経験知 — 管長の理論値を実測で補正した記録

- 題名: Chromatic pan flute 7 Octave Customisable、Chromatic Pan Flute 4 octave Tunable、Chromatic DOUBLE BASS pan flute 4 octave Tunable、およびその原典 Chromatic Tenor Panflute
- 著者: AskMe（リミックス）、Caran（原典）
- 発表: Printables（AskMe版は2023年4月8日更新、Printablesの「Musical Instruments」コンテストへの応募作）、Thingiverse（Caran版は2015年11月14日）
- 確認先のURL:
  - https://www.printables.com/model/442532-chromatic-pan-flute-7-octave-customisable （いいね54件、ダウンロード203件、閲覧1,564件、ファイル61個）
  - https://www.printables.com/model/139274-chromatic-pan-flute-4-octave-tunable
  - https://www.thingiverse.com/thing:1129462 （いいね85件、C3からC6の半音階、サポートなしで印刷可）
- 内容の要約: C2からC9までの半音階のパンフルートである。AskMeは原典の問題点を次のように記録している。「元のモデルには大きな問題があった。管は正確にその音になるように計算されていたが、高い音では高すぎて、下げる方向に調律できなかった。そこで全部の管に2cm足して直した」。調律は蜜蝋で行うと指示し、音域ごとに必要なノズル径（C8からC9は0.4mm以下、C2からC3は1mm以上）を細かく書き分けている。原典のCaranのモデルはサポートなしで印刷でき、大きなプリンタが無ければ管を個別に印刷してエポキシで接着するという分割方法を示している。
- CipherFluteとの関係: 「管長から周波数を計算すると高音側で系統的にずれ、一律の補正が必要である」という現象を、コミュニティが実測で把握して対処している記録である。CipherFluteが f = A/(L+e) の e として定式化した端補正に対応する。またPrintablesの「Musical Instruments」コンテスト（2023年4月1日から6月1日、応募385件、https://www.printables.com/contest/368-musical-instruments ）は、印刷可能な楽器の設計が組織的に大量生産された場であり、印刷笛の技術水準を示す指標として使える。
- 脅威の度合い: 中。CipherFluteの f = A/(L+e) は、この経験知を素直に定式化しただけと見なされる余地がある。CipherFluteは、単に補正するのではなく較正定数を実測で求め、13スロットを100セント刻みで安全に分離できることを検証した点に寄与を置くべきである。

---

## 背景として押さえるべき文献

脅威の度合いは低いが、CipherFluteの位置づけを説明するために有用な実物である。

- Loud Whistle（Federico、MakerWorld、ダウンロード90,546件、いいね12,817件、印刷78,443件、https://makerworld.com/en/models/119995-loud-whistle ）は、MakerWorldで最も普及した笛であり、120dBを謳う。印刷笛が一般家庭で日常的に量産されている現実を示す。
- Mini Flat Whistle - Flat Design, Full Power（ACstudio、MakerWorld、ダウンロード13,608件、いいね3,097件、https://makerworld.com/en/models/2099305-mini-flat-whistle-flat-design-full-power ）は、「財布に入れて邪魔にならないように、より平たく、より小さく」と明言する平板型笛であり、CipherFluteのカード実装と同じ携帯形態を狙っている。作者は笛だけを集めたコレクションを運営している。
- Whistle Magic - create your own whistle（nischi、Thingiverse、2013年2月4日、リミックス1,800件、実作26件、https://www.thingiverse.com/thing:46825 ）は、OpenSCADによる媒介変数化された笛の生成器である。高さ、半径、内部の穴、内球を変えて「たくさんの違う音」を作れると書くが、音名や周波数との対応は与えていない。媒介変数化の系譜として引ける。
- Recorder / Flute Musical Instrument（HumbleBee、MakerWorld、ダウンロード9,328件、いいね2,529件、https://makerworld.com/en/models/1149042-recorder-flute-musical-instrument ）は、C管のバロック式ソプラノリコーダーを模したモデルであり、「作ったとおりでよく鳴り、すべての音が正しい音高で出る」と主張する。印刷楽器が実用的な調律に達しうるという主張の例である。
- Native American Drone Flute（F#、A=432hz）（blackpixel、MakerWorld、ダウンロード4,205件、いいね1,154件、https://makerworld.com/en/models/1485827-native-american-drone-flute-f-a-432hz ）は、基準ピッチをA=432Hzと明記し、設計の主要な参考文献としてflutopedia.comを挙げている。作者は「造形板から出た状態で調律されているはずだが、材料設定や穴径をいじる必要があるかもしれない」と書く。
- Panpipes / Pan flute（Savy_Maker、MakerWorld、ダウンロード11,695件、いいね2,892件、https://makerworld.com/en/models/1148458-panpipes-pan-flute ）は、一体で全音が出ると謳い、サポート不要で速く印刷できるとする。
- Tunable pan flute in C major 2 octaves（g3d-Solutions、MakerWorld、https://makerworld.com/en/models/1157247-tunable-pan-flute-in-c-major-2-octaves-c-c ）は、ねじ込み栓とOリングで各管の長さを最大5mm変えて精密に調律する仕組みを持つ。物理的な後調律の実装例である。
- 32-note pipe organ（Chrysibulum、MakerWorld、ダウンロード609件、いいね414件、https://makerworld.com/en/models/2151850-32-note-pipe-organ ）は、G3からD6までの32鍵、印刷部品501点の本格的なパイプオルガンである。歴史的ピッチ（A415、A392、A466）に対応し、風圧の測定値と単管の音圧（80から85dBA）まで記録している。印刷した気柱楽器の到達点として引ける。
- Ultimate Triller Whistle with 3 tones、Super Loud Whistle 125 dB Triple Tone、Dual Tone Whistle over 130dB、Low pitch dual frequency whistle 125dB 1.7g などの一群は、いずれも音量のための多音であり、音高を情報として使わない。
- 1880 "secret" whistle（bloodVixen、MakerWorld、https://makerworld.com/en/models/2819109-1880-secret-whistle-really-loud-easy-print ）は、Popular Science Monthly第33巻（1888年6月）の記事「Whistles Ancient and Modern」に載った設計の再現である。「secret」の意味は「指で環を閉じないと可聴音が出ない」ことであり、情報の秘匿とは無関係である。「秘密の笛」という語がすでに別の意味で使われていることを注意点として押さえておく価値がある。
- Pocket Whistle with secret compartment（H2Jack Concepts、MakerWorld、ダウンロード457件、いいね345件、https://makerworld.com/en/models/2348284-pocket-whistle-with-secret-compartment ）は、笛と収納室を組み合わせた唯一の例だが、収納するのは薬であり、情報を音高で運ぶ発想は無い。
- QR Code Generator（SnaKKo、MakerWorld、ダウンロード32,379件、いいね12,389件、https://makerworld.com/en/models/476280-qr-code-generator-qrcode-for-mail-wifi-ect ）は、OpenSCADでQRコードを立体化する媒介変数モデルであり、テキスト、Wi-Fi、電話、vCardの4種を扱える。印刷物に光学符号を載せる系譜の代表であり、ダウンロード数の大きさから「符号を印刷する」需要の規模が読める。
- Secure Snap Card - Bitcoin Seed/Passphrase Backup（BlackHawk、MakerWorld、https://makerworld.com/en/models/1475714-secure-snap-card-bitcoin-seed-passphrase-backup ）は、8.5×5.5cmのカードを封入し、開けるには物理的に壊すしかないという容器である。作者は「不透明な紙を挟むか黒フィラメントで印刷して透過を防げ」と助言する。改竄の痕跡が残ることを安全性の根拠にしている。
- Secret text/password vault for one-time opening（JesseZhang、MakerWorld、ダウンロード86件、https://makerworld.com/en/models/1936443-secret-text-password-vault-for-one-time-opening ）は、印刷を一時停止して付箋を挿入し、そのまま封止するカードである。核のコードを収めた「The Biscuit」に着想したと述べる。印刷過程そのものを封止手段に使う例である。
- Seed Phrase Keeper - Bitcoin recovery codebook（SRRN、MakerWorld、https://makerworld.com/en/models/1031732-seed-phrase-keeper-bitcoin-recovery-codebook ）は、シードを一度も計算機に入力せずに記録するための文字タイルの集合であり、Scrabbleの文字出現頻度に合わせてタイル枚数を割り振っている。作者自ら「火災で樹脂が溶ける」という弱点を挙げ、2部作って別の場所に保管せよと勧めている。
- Cults3Dの「seed phrase」検索で得られた15件（https://cults3d.com/en/search?q=seed+phrase ）は、打刻用の治具、Trezor用の容器、封止式の金庫が中心であり、符号として情報を刻むものは前述のSeedQRテンプレート2件だけであった。
- Thingiverseの秘密関連モデル群として、Corrugated Secret Sign（mathgrrl、thing:548191）、SimpleCrypt: Pocket Tube Cipher（thing:2728148）、Caesar Cipher Decoder Ring（thing:14891、thing:18315）、Morse code keychain（thing:3641800）などがある。いずれも人間が手で解く暗号の道具であり、機械可読な符号ではない。
- Wallet Card Morse Code（danyelol、MakerWorld、ダウンロード8,454件、いいね4,524件、https://makerworld.com/en/models/186023-wallet-card-morse-code ）は、モールス符号の一覧を刻んだ財布サイズのカードである。符号表を印刷物に載せる例だが、情報そのものは載っていない。

---

## 未検証のまま残ったもの

- Thingiverseの thing:2757112「Cryptocurrency-seed break card vault」（Heigre、いいね140件）と thing:3481293「Bitcoin seed coin」（PeteLaric、Customizable、いいね18件）は、検索結果の一覧でのみ確認した。前者は「break card」という名称から封止式の容器と推測されるが、説明文を読んでいない。後者は媒介変数化されているため、シードを幾何形状に符号化している可能性があるが未確認である。この2件は追加で確認する価値が高い。
- Thingiverseの thing:16286「Multi-tone Whistle」（conanh、Featured、いいね583件）、thing:497948「Duo Tone Whistle」（jipvanleeuwenstein、Featured、いいね4,800件）、thing:1046「Whistle」（Zaggo、いいね2,700件）は、一覧でいいね数まで確認したが、説明文の調律に関する記述を読んでいない。
- Cults3Dの「RECOVERY PHRASE SEALED VAULT」「HASHPACK COLD SEED」「COLD-STORAGE DISPLAY ALTAR」は、検索結果の一覧と価格表示のみ確認した。個別ページの説明文は読んでいない。
- 3dprintableflutes.com が「70本以上の印刷可能な笛のカタログ」を持つという記述は、MakerWorld上のTeleTunesの説明文にある主張である。実際にサイトを開いたところ確認できたのは十数種の掲載であり、70本という数は検証できていない。
- Bambu Lab社の2024年の年間売上約15億人民元という数値は、Wikipedia英語版の記述であって原典に当たっていない。造形機の出荷台数や市場占有率については、公開されている一次資料を見つけられなかった。
- Cults3Dが自称する「3.5M designs」は検索窓の表示で確認したが、この数がCults3D自身に投稿されたモデルのみを指すのか、他基盤の索引を含むのかは判別できていない。
- MakerWorldの登録利用者数、累計ダウンロード数、累計印刷数といった全体統計は、MakerWorldのabout ページがHTTP 403を返し、Bambu Labのブログにも該当記事が見つからなかったため取得できなかった。
- MakerWorldの検索が返す「total」の値（whistle で2,018など）は、あいまい一致を含む緩い数字である。厳密な該当件数として引用してはならない。
- Printablesのモデル総数約138万件は、サイトマップの最終ページがちょうど1,000件で満杯だったため、実際にはもう少し多い可能性がある。

---

## この切り口で見つからなかったこと

ここに書くことは、CipherFluteの新規性の主張の根拠になる。いずれも、4つの基盤の内部検索を英語の複数の語彙で繰り返し、該当が無いことを確認した結果である。

1. **笛の音高を符号として情報を運ぶモデルは1件も存在しない。** MakerWorldで「acoustic code」「sound password」「whistle password」「whistle secret」「binary whistle」「whistle bit」「encode sound」「acoustic barcode」「flute cipher」「audio data」の10通りの検索を行ったが、返ってきたのはすべて大音量の笛、QRコード、吸音パネル、暗号解読の玩具であった。Printablesでも「whistle」1,150件の上位36件を個別に確認したが、情報を運ぶ設計は無かった。Thingiverseの「secret message」検索でも、出てきたのは箱、シーザー暗号の輪、モールス符号のキーホルダーであった。すなわち「吹いた音の高さを読んで少量の秘密情報を復元する」という提案は、モデル共有基盤上に前例が無い。

2. **多音笛はすべて同時発音であり、1本ずつ順に吹いて記号列として読むものは無い。** 12音、8音、6音、4音、3音、2音の笛をすべて確認したが、どれも一度に吹いて全部を鳴らす設計であり、目的は音量、不快さ、警報である。「音の並びで情報を表す」という語彙は、どの説明文にも現れなかった。

3. **音高が既知の基準笛を混ぜて他の笛を比で読むという発想は、どのモデルにも無い。** 調律のばらつきに対する対処として基盤上に存在するのは、蜜蝋を詰める、ねじ栓で管長を変える、風道を研磨する、全管に一律の補正長を足すといった物理的な後調律だけである。測定時の正規化という考え方は見当たらない。

4. **誤り訂正符号を印刷物の符号に適用したモデルは無い。** 印刷される符号としてはQRコードが圧倒的に多く、そのReed–Solomon符号はQRコードの規格に内蔵されているので作者は意識しない。符号の設計者自身が誤り訂正を選んで付けた例は見つからなかった。SeedQRのCompactSeedQRがチェックサムのビットを省くという判断をしているのが、最も近い設計上の言及である。

5. **秘密分散を3Dプリント物に適用した例は、QR SafeShareのただ1件である。** MakerWorldで「shamir secret sharing」を検索しても、隠し引き出しや秘密の本型金庫といった無関係な物理的隠匿しか返らない。Printablesで「shamir」を検索した結果は2件で、どちらも人名や作品名の偶然の一致であった。すなわち「秘密分散のシェアを3Dプリント物として配る」という設計は、基盤上でまだ1件しか実装されていない、きわめて薄い領域である。CipherFluteはこの薄い領域の2件目に当たる。

6. **日用品に偽装した情報保管モデルは、隠し収納の系譜しかない。** 「secret compartment」「hidden message」の検索で出てくるのは、本型の金庫、隠し引き出し、パズルボックス、日本の秘密箱である。いずれも中に物を入れる空洞であり、物体そのものの形状や音に情報を符号化して偽装するものではない。物体の形状に情報を持たせつつ日用品として通用させるという設計は見つからなかった。

7. **笛を日用品に埋め込んで、笛であること自体を隠したモデルは無い。** 「hidden whistle」「whistle disguised」「whistle in object」「whistle business card」「whistle spool」「whistle bookmark」で検索したが、笛は常に笛の形をしていた。ジッパー引き手、指輪、キーホルダーに付ける例はあるが、いずれも笛だと分かる外観である。唯一の例外である「secret compartment付きのポケット笛」も、笛の姿をしたまま薬を入れる容器である。

8. **和音を出す笛を情報表現に使った例は無い。** MakerWorldの「chord whistle」検索で返るのは3音や2音の大音量笛であり、和音という語で意図されているのは音の厚みである。楽理的な和音を情報の単位として扱う設計は見当たらない。

---

## 調べ残した穴

- MakerWorldのコメント欄と「実作報告（Makes）」を読んでいない。作者の説明文には書かれない実測周波数や、鳴らなかった条件の報告がコメント欄に蓄積している可能性が高い。特にFlat Pocket Whistleは2,965件の実作報告があり、薄壁の造形限界に関する集合知が眠っているはずである。CipherFluteが「実機で鳴る条件」を論じるときの外部証拠として価値がある。
- Printablesの「remix」の系統樹をたどっていない。Flat Pocket Whistleには99件、Whistle Magicには1,800件のリミックスがあり、そのなかに音高を制御する派生や符号化に近い派生が混ざっている可能性を排除できていない。
- MakerWorldの「Maker Lab」および媒介変数化モデル（Customizer）の一覧を調べていない。利用者が寸法を指定して生成する仕組みのなかに、音名を選べる笛の生成器があるかもしれない。
- 中国語での検索を行っていない。MakerWorldは中国語圏の投稿が多く（八音笛の作者も中国語で書いている）、「口哨」「哨子」「暗号」「助记词」などの語で検索すれば、英語では引っかからないモデルが出る可能性がある。日本語での検索も、MakerWorldの表示が自動翻訳であるため原文の語彙とずれており、十分に試せていない。
- MyMiniFactory自体を調べていない。担当範囲の4基盤に入っていなかったが、Thingiverseを買収した基盤であり、有料モデルの比率が高いため、暗号資産の保管に関する商業モデルが集まっている可能性がある。
- Bambu LabとMakerWorldの規模を示す公式な数字を取れていない。MakerWorldのabout ページがHTTP 403を返したため、認証を通したブラウザで開けば取得できる可能性がある。造形機の出荷台数や市場占有率については、CONTEXTなどの市場調査会社の公表値を報じた記事に当たる必要がある。
- Printablesの「Musical Instruments」コンテスト（応募385件）の応募作を全件見ていない。2か月間に集中的に投稿された印刷楽器の集合であり、音高設計に関する記述の宝庫である可能性が高い。
- QR SafeShareのGitHubリポジトリの履歴（コミット129件）を読んでいない。最初のコミット日が分かれば、CipherFluteとの時間的な前後関係を正確に述べられる。
