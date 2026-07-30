# 深掘り調査 F4 CipherFluteに近接する日本の研究者の業績の系統的洗い出し

調査日は2026年7月30日である。調査対象はCipherFlute（栗原一貴、津田塾大学、WISS 2026投稿予定）である。

## この調査で使った情報源と走査の方法

各研究者について、次の一次情報を実際に開いて業績の全体像を取った。

1. DBLPの著者ページの機械可読版（`https://dblp.org/pid/《著者識別子》.xml`）を取得し、全レコードを題名・著者・掲載・年・識別子つきで書き出した。取得できた著者識別子は次のとおりである。高橋治輝は188/0408、松村耕平は05/11081、加藤邦拓は161/3323、鳴海紘也は161/3873、久保勇貴は29/5947、上平員丈は85/2972、鳥井秀幸は15/4341、渡邊恵太は65/415、片倉翔平は218/0155、伊藤雄一はi/YuichiItoh、水木敬明は95/402である。合計622レコードを機械的に列挙した。
2. CiNii Researchのオープンサーチ（`https://cir.nii.ac.jp/opensearch/all?creator=《氏名》&format=json&count=100`）で著者名による検索を行い、和文の学会誌・研究会報告・シンポジウム論文を拾った。合計1123レコードを列挙した。ただしCiNiiの著者名検索は同姓同名を区別しないため、後述のとおり別人のレコードが多量に混入している。
3. researchmapの公開論文欄、および研究室の業績ページを開いた。開いたのは高橋治輝のresearchmap（20件）、立命館大学Playful Laboratory（松村耕平と高橋治輝の研究室、2014年から2025年までの約190件）、加藤邦拓のresearchmap（2ページ分で33件）、渡邊恵太のresearchmap（47件）、伊藤雄一の研究室χLab.の業績ページである。
4. WISS 2025の予稿集索引（`https://www.wiss.org/WISS2025Proceedings/`）の全文を取得し、登壇24件・国際会議招待10件・デモ約174件・WISS Challenge 4件の全題名と著者を対象に、笛・オカリナ・管楽器・音響・共鳴・3Dプリント・暗号・秘密・認証・振動という語で機械的に走査した。
5. 個別の書誌はCrossref（`https://api.crossref.org/works/《識別子》`）とSemantic Scholar（`https://api.semanticscholar.org/graph/v1/paper/DOI:《識別子》`）で照合し、抄録が取れるものは抄録も取った。
6. 科研費の課題はCiNii Research経由のKAKENレコードで確認した。

うまくいかなかったこともあるので正直に書く。Google Patentsの検索応答（`https://patents.google.com/xhr/query?...`）は応答が解析できず、特許は一件も確認できていない。上平員丈らの一連の研究には特許が存在する可能性が高いが、この調査では確認していない。Springer LinkのQuality and User Experience誌は認証画面に転送されて本文を取れず、Crossrefの書誌と検索結果に現れた抄録の記述で代替した。WISS 2025のデモ予稿のPDFは埋め込みフォントに文字対応表がなく本文のテキストを抽出できなかったので、題名・著者・所属・掲載までを予稿集索引で確認し、内容の記述は題名が述べている範囲にとどめた。ACM Digital LibraryとIEEE Xploreは直接開かず、DBLP・Crossref・Semantic Scholarの書誌で代替した。

## 依頼時の所属についての訂正

依頼文の所属と、確認できた最新の所属が食い違うものが二つある。

- 鳴海紘也さんは依頼文では東京大学とあるが、DBLPの著者注記とresearchmapのいずれも慶應義塾大学理工学部情報工学科（Programmable Products Lab）を示している。日本バーチャルリアリティ学会誌2025年3月号に「慶應義塾大学 理工学部情報工学科 Programmable Products Lab」という研究室紹介記事を自ら書いている（<https://cir.nii.ac.jp/crid/1520305101993931520>）。東京大学の川原圭博研究室は博士課程および助教時代の所属である。
- 片倉翔平さんは依頼文では明治大学とあるが、2021年以降の業績はすべてドイツのハッソ・プラットナー研究所（ポツダム大学、Patrick Baudisch研究室）の共著である。明治大学の渡邊恵太研究室は学生時代の所属である。

CipherFluteの謝辞や関連研究の記述で所属に触れる場合は、この二点に注意が必要である。

---

## 1 高橋治輝さん（立命館大学情報理工学部）

### 確認した業績の件数

DBLPで22件、researchmapの公開論文欄で20件、CiNiiの著者名検索で20件、Playful Laboratoryの業績ページとWISS 2025索引で7件を確認した。CiNiiの20件のうち6件は同姓同名の別人である（土木学会論文集の地域公共交通、日本デザイン学会と設計工学・システム部門講演会の感性設計、水晶振動子マイクロバランス法による界面スリップ計測）。重複と別人を除いた実質の業績は45件前後である。CipherFluteに関わるものは5件である。

### 拾った仕事

**Programmable Filament: Printed Filaments for Multi-material 3D Printing**
著者は高橋治輝、Parinya Punpongsanon、Jeeeun Kim。掲載はProceedings of the 33rd Annual ACM Symposium on User Interface Software and Technology（UIST 2020）である。年は2020年である。確認先は<https://doi.org/10.1145/3379337.3415863>である。
内容は、複数の色や材質のフィラメントをあらかじめ所定の長さで継ぎ合わせて一本のフィラメントを作り、単一のノズルを持つ家庭用の熱溶解積層方式プリンタで多材料の造形を実現する手法である。
CipherFluteとの関係は、造形物ではなくフィラメントという材料の側に情報（材質の並び）を書き込み、それを造形過程が読み出すという構図が、CipherFluteの「印刷データに秘密がそのまま載る」という性質と裏表の関係にある点である。CipherFluteが「印刷は自分の環境で行え」と述べる根拠を技術的に補強する材料になる。
新規性への脅威の度合いは低である。情報の担い手は材料の並びであり、読み出しは造形機であって人の吹く行為ではなく、秘密の保管という文脈も持たない。

**3D Printed Fabric: Techniques for Design and 3D Weaving Programmable Textiles**
著者は高橋治輝、Jeeeun Kim。掲載はProceedings of the 32nd Annual ACM Symposium on User Interface Software and Technology（UIST 2019）である。年は2019年である。確認先は<https://doi.org/10.1145/3332165.3347896>である。
内容は、熱溶解積層方式プリンタの吐出挙動そのものを制御して布状の構造を織り上げる造形手法である。
CipherFluteとの関係は、造形挙動の制御によってしか作れない微細構造を積極的に設計変数として使うという方法論が共通する点である。CipherFluteの半割り笛が「サポート材なしで平置き印刷できる」という主張は、この系統の造形挙動の理解の上に立っている。
新規性への脅威の度合いは低である。情報を持たせることも音を出すことも扱っていない。

**Conductive, Ferromagnetic and Bendable 3D Printed Hair for Designing Interactive Objects**（および和文の「導電性・強磁性・および土台の可撓性を持つ毛構造の造形手法と評価」）
著者は鎌田航誠、高橋治輝、塚田浩二。掲載は英語版がAdjunct Proceedings of the 36th Annual ACM Symposium on User Interface Software and Technology（UIST Adjunct 2023）、和文版が情報処理学会論文誌（2025年2月）である。確認先は<https://doi.org/10.1145/3586182.3615823>と<https://cir.nii.ac.jp/crid/1390021758113218048>である。
内容は、造形物の表面から生える毛構造に導電性や強磁性を与え、それをそのままセンサや入力機構として使う手法である。
CipherFluteとの関係は、造形物そのものが電子部品を持たずに機能を担うという発想を共有する点である。
新規性への脅威の度合いは低である。導電性フィラメントを必要とし、読み出しには電子回路が必要であり、情報の符号化を目的としていない。

**リズムゲームへの入力を3Dプリンタ制御に活用する手法の検討**
著者は高橋治輝、松村耕平。掲載は第33回インタラクティブシステムとソフトウェアに関するワークショップ（WISS 2025）のデモ発表3-B06である。年は2025年である。確認先は<https://www.wiss.org/WISS2025Proceedings/data/demo/3-B06.pdf>である。予稿集索引で題名・著者・所属を確認した。埋め込みフォントの制約でPDFの本文テキストを抽出できなかったため、内容は題名が述べる範囲にとどめる。
CipherFluteとの関係は、CipherFluteが投稿を狙うWISSにおいて、同一の研究室が3Dプリンタを扱うデモを継続的に出しているという場の状況である。
新規性への脅威の度合いは低である。

**音響マクロ: マウス操作の音響記録・再生・配信と編集**
著者は太田佳敬、高橋治輝、中橋雅弘、宮下芳明。掲載は情報処理学会研究報告の音声言語情報処理研究会報告およびヒューマンコンピュータインタラクション研究会報告である。年は2013年である。確認先は<https://cir.nii.ac.jp/crid/1572261552735953408>である。
内容は、マウス操作を音響信号として記録し再生・配信・編集する手法である。
CipherFluteとの関係は、高橋治輝さんの業績のなかで唯一「音を情報の担体にする」ものだという点にとどまる。対象は画面上の操作であって造形物ではない。
新規性への脅威の度合いは低である。

### この研究者について言えること

高橋治輝さんの業績は、熱溶解積層方式プリンタの吐出挙動を制御して新しい形と質感と機能を得る系統に一貫して集中している。造形物に情報を埋め込む仕事、造形物の音を読む仕事、笛や楽器を作る仕事、認証や秘密を扱う仕事は一件も見つからなかった。CipherFluteが引くべきは「サポート材なしで印刷できる微細構造の設計」という文脈においてであり、競合ではない。

---

## 2 松村耕平さん（立命館大学情報理工学部）

### 確認した業績の件数

DBLPで58件、Playful Laboratoryの業績ページで2014年から2025年までの約190件、CiNiiの著者名検索で86件を確認した。CiNiiの86件には同姓同名の別人（遺伝的プログラミングの交叉法など）が数件混じる。重複を除いた実質の業績は200件を超える。CipherFluteに関わるものは6件である。

### 拾った仕事

**Acoustic Probing for Estimating the Storage Time and Firmness of Tomatoes and Mandarin Oranges**
著者はHidetomo Kataoka、Takashi Ijiri、松村耕平、Jeremy White、Akira Hirabayashi。掲載はarXivのプレプリント（arXiv:1809.10581）である。年は2018年である。確認先は<http://arxiv.org/abs/1809.10581>である。
内容は、果実に音響信号を与えて応答を測り、内部の状態（貯蔵時間と硬さ）を推定する手法である。
CipherFluteとの関係は、物体の内部の状態が音響応答に現れるという物理を利用する点で共通する。CipherFluteは管長という設計された内部構造が基本周波数を決めるという同じ物理の上に立っている。
新規性への脅威の度合いは中である。物体側に設計された符号を持たせるわけではなく、能動的な加振と計測を要し、秘密の保管という文脈を持たない。ただし国内で「物体の内部を音で読む」研究として引用の候補になる。

**Universal earphones: earphones with automatic side and shared use detection**
著者は松村耕平、Daisuke Sakamoto、Masahiko Inami、Takeo Igarashi。掲載はProceedings of the 2012 ACM International Conference on Intelligent User Interfaces（IUI 2012）である。年は2012年である。確認先は<https://doi.org/10.1145/2166966.2167025>である。
内容は、イヤホンが左右どちらの耳に入っているかや共有されているかを自動判別する手法である。
CipherFluteとの関係は、日用品の側に判別のための仕掛けを持たせるという構図である。
新規性への脅威の度合いは低である。

**Guitar Clicker: A Gamified Approach to Motivating Guitar Practice for Beginners**
著者はItsuki Okamo、松村耕平、高橋治輝。掲載はEntertainment Computing – ICEC 2025, 24th IFIP TC 14 International Conferenceである。年は2025年である。確認先は<https://doi.org/10.1007/978-3-032-02555-5_56>である。
内容は、初心者のギター練習の動機づけをゲーム化する系である。
CipherFluteとの関係は「楽器を扱う仕事」という括りにおいてのみである。楽器を作るわけではない。
新規性への脅威の度合いは低である。

**Press the Button to 3D Print: Lowering Barriers to 3D Printing with a Single-Button Interface**（および和文の「ボタンひとつで3Dプリントが体験できるシステムの提案と運用」WISS 2024、「Purikura-Fab: 3Dプリンタ未経験者の造形プロセス理解と利用意欲を促進する体験型システムの開発」WISS 2025）
著者は高橋治輝、松村耕平（Purikura-Fabは臼井義人、高橋治輝、松村耕平）。掲載はProceedings of the 10th ACM Symposium on Computational Fabrication（SCF 2025）およびWISS 2024・WISS 2025である。確認先は<https://doi.org/10.1145/3745778.3766657>と<https://www.wiss.org/WISS2025Proceedings/data/paper/11.pdf>である。
内容は、3Dプリンタの利用の敷居を下げる体験型のシステムである。
CipherFluteとの関係は、家庭用3Dプリンタの普及という前提を共有する点である。
新規性への脅威の度合いは低である。

**Lightweight Authentication and Dynamic Key Generation for IMU-Based Canine Motion Recognition IoT Systems**
著者はGuanyu Chen、Hiroki Watanabe、松村耕平、Yoshinari Takegawa。掲載はFuture Internet 18巻2号である。年は2026年である。確認先は<https://doi.org/10.3390/fi18020111>である。
内容は、慣性センサを用いる犬の動作認識の系に軽量な認証と動的な鍵生成を組み込む方式である。
CipherFluteとの関係は「認証や鍵を扱う仕事」という括りにおいてのみである。
新規性への脅威の度合いは低である。物理的な担体を持たない通信路の認証である。

**ペングリップ型デバイスを用いた個人認証の提案**
著者は岡田一志、大井翔、松村耕平、野間春生。掲載は情報処理学会インタラクション2019論文集である。年は2019年である。確認先はPlayful Laboratoryの業績ページ<https://www.playful.re/papers>である。予稿集そのものの所在は確認できなかった。
内容は、ペンの握り方から個人を認証する手法である。
CipherFluteとの関係は「認証を扱う仕事」という括りにおいてのみである。
新規性への脅威の度合いは低である。

### この研究者について言えること

松村耕平さんの業績はエンタテインメントコンピューティング、社会ロボット、車内体験、医療訓練シミュレータに広く分布し、造形物に情報を埋め込む仕事は一件もない。音を扱う仕事は果実の音響探査と歩行時の音響操作にとどまる。CipherFluteの競合ではない。

---

## 3 加藤邦拓さん（東京工科大学メディア学部）

### 確認した業績の件数

DBLPで43件、researchmapの公開論文欄で2ページ分の33件、CiNiiの著者名検索で30件、WISS 2025索引で2件を確認した。重複を除いた実質の業績は60件前後である。CipherFluteに関わるものは15件である。この研究者は今回の対象のなかで、CipherFluteの発想と最も広い面で接している。

### 拾った仕事

**SheetKey: Generating Touch Events by a Pattern Printed with Conductive Ink for User Authentication**
著者はShota Yamanaka、Tung D. Ta、Kota Tsubouchi、Fuminori Okuya、Kenji Tsushio、加藤邦拓、Yoshihiro Kawahara。掲載はProceedings of Graphics Interface 2020である。年は2020年である。確認先は<https://doi.org/10.20380/GI2020.45>である。書誌はSemantic Scholarで題名・著者・掲載・年を照合した（<https://api.semanticscholar.org/graph/v1/paper/DOI:10.20380/GI2020.45>）。抄録は取得できなかったため、内容の記述は題名と副題が述べる範囲にとどめる。
内容は、導電性インクで印刷したパターンをタッチスクリーンに当てるとタッチイベントの列が生成され、それを利用者の認証に使う手法である。
CipherFluteとの関係は決定的に近い。電源も電子部品も持たない印刷物そのものが鍵になり、市販の端末がそれを読むという構図は、CipherFluteが笛と携帯端末のマイクで実現しようとしていることと同型である。異なるのは物理層が静電容量であるか音響であるか、そして所有者の身体的な行為（吹く）を要するか要さないかである。
新規性への脅威の度合いは高である。「無電源の印刷物を認証の鍵にする」という枠組みそのものが日本の研究者の手で2020年に確立されている。CipherFluteは、符号量（SheetKeyの符号量は不明だがタッチ点の配置に律速される）、誤り訂正の有無、基準素子による正規化、脅威モデルの明示、秘密分散との組み合わせという点で差分を述べる必要がある。引用しないままWISSに出すのは危険である。

**DuoTouch: Passive Two-Footprint Attachments Using Binary Sequences to Extend Touch Interaction**
著者は池松香、加藤邦拓。掲載はProceedings of the 2026 CHI Conference on Human Factors in Computing Systemsである。年は2026年である。確認先は<https://doi.org/10.1145/3772318.3790411>とプレプリント<https://doi.org/10.48550/arXiv.2602.17961>である。
内容は、静電容量式タッチパネル用の受動的なアタッチメントであり、二つの接触足跡と二本の導線を使って動きを二進符号列として符号化し、改変していない端末の標準のタッチ応答インタフェースで復号する。固定長の符号を離散的な命令に対応づける構成と、位相をずらして相対的な時刻差から方向と距離を推定する構成の二つを提示し、動作速度・導線幅・端末のタッチ標本化率と復号精度の関係を標本化限界の式として導いている。ハンドストラップ、スマートフォンのリングホルダー、タッチパッド用の付属品に機構を埋め込んだ実装を示している。
CipherFluteとの関係はきわめて近い。無電源の受動物体に二進符号を固定し、市販の端末で復号し、復号精度を物理パラメータの関係式で議論し、しかも日用品の形（ストラップ、リングホルダー）に埋め込むという四点がCipherFluteの構成とそのまま重なる。
新規性への脅威の度合いは高である。とくに「符号の復号可能性を物理パラメータの上限式で議論する」という論述の型がCipherFluteの管長とスロット幅の議論と同じ性格を持つ。差分として述べられるのは、符号量（DuoTouchは動作あたり短い固定長）、秘密の保管という応用文脈、誤り訂正符号の導入、基準素子による環境補正、脅威モデルの明示である。

**Passive Attachments for Back-of-Device Interaction via Binary Touch Sequences**
著者は池松香、加藤邦拓。掲載はAdjunct Proceedings of the 38th Annual ACM Symposium on User Interface Software and Technology（UIST Adjunct 2025）である。年は2025年である。確認先は<https://doi.org/10.1145/3746058.3758444>である。
内容はDuoTouchの前身である。指で動かす導体を介して、アタッチメント上の導電部と非導電部の並びに応じた二進符号列を生成し、外部電源も基本ソフトウェアの改変もなしに表現力のある入力を実現する。
CipherFluteとの関係と脅威の度合いはDuoTouchと同じである。度合いは中である（DuoTouchが本体であるため）。

**ExtensionSticker: A Proposal for a Striped Pattern Sticker to Extend Touch Interfaces and its Assessment**（および前身のUIST Adjunct 2014版と和文のヒューマンインタフェース学会論文誌18巻1号版）
著者は加藤邦拓、宮下芳明。掲載はProceedings of the 33rd Annual ACM Conference on Human Factors in Computing Systems（CHI 2015）である。年は2015年である。確認先は<https://doi.org/10.1145/2702123.2702500>と<https://cir.nii.ac.jp/crid/1390282763127758720>である。
内容は、縞模様の導電パターンを印刷したシールを貼ることでタッチ入力を離れた場所へ転送する手法である。
CipherFluteとの関係は、印刷された幾何パターンそのものが情報の通り道になるという構図である。
新規性への脅威の度合いは中である。SheetKeyとDuoTouchの系譜の出発点として引用する価値がある。

**紙窓: カード内領域を独立したタッチパネルディスプレイのように扱うインタフェース**
著者は加藤邦拓、宮下芳明。掲載はヒューマンインタフェース学会論文誌17巻3号である。年は2015年である。確認先は<https://cir.nii.ac.jp/crid/1390845713079678080>である。WISS 2013版とWISS 2014版も存在する。
内容は、カードに印刷した領域を独立したタッチ操作面のように扱う手法である。
CipherFluteとの関係は、カードという日用品の形に機能を溶け込ませるという構図である。CipherFluteのカード実装と形が同じである。
新規性への脅威の度合いは中である。

**3D Printed Physical Interfaces that can Extend Touch Devices**、**A Tangible Interface to Realize Touch Operations on the Face of a Physical Object**、**CAPath: 3D-Printed Interfaces with Conductive Points in Grid Layout to Extend Capacitive Touch Inputs**
著者はそれぞれ加藤邦拓と宮下芳明、上野新葉と加藤邦拓と宮下芳明、加藤邦拓と池松香と川原圭博である。掲載はUIST Adjunct 2016（前二者）、Proceedings of the ACM on Human-Computer Interaction 4巻ISS号（CAPath）である。年は2016年と2020年である。確認先は<https://doi.org/10.1145/2984751.2985700>、<https://doi.org/10.1145/2984751.2985711>、<https://doi.org/10.1145/3427321>である。
内容は、3Dプリントした立体物に導電経路を仕込み、タッチ端末の入力を拡張する系である。
CipherFluteとの関係は、3Dプリントした立体物が電源を持たずに機能を担うという構図である。
新規性への脅威の度合いは中である。

**LightTouch Gadgets: Extending Interactions on Capacitive Touchscreens by Converting Light Emission to Touch Inputs**、**ShiftTouch: Extending Touchscreens with Passive Interfaces using Small Occluded Area for Discrete Touch Input**
著者は池松香、加藤邦拓、川原圭博（LightTouch）および池松香と加藤邦拓（ShiftTouch）である。掲載はProceedings of the 2021 CHI ConferenceおよびProceedings of the Seventeenth International Conference on Tangible, Embedded, and Embodied Interaction（TEI 2023）である。確認先は<https://doi.org/10.1145/3411764.3445581>と<https://doi.org/10.1145/3569009.3572742>である。
内容は、電源を持たない受動的なガジェットが画面の発光や小さな遮蔽を介してタッチ入力を生み出す系である。
CipherFluteとの関係は、無電源の物体が市販端末を介して離散的な情報を渡すという構図である。
新規性への脅威の度合いは中である。

**Acoustic+Pose: Adding Input Modality to Smartphones with Near-Surface Hand-Pose Recognition using Acoustic Surface**、**Detecting Thumb-Posture for One-handed Interactions with Smartphone using Acoustic Sensing**、**Leveraging Screen-integrated Speakers for Hand-pose Recognition in Mobile Interfaces**
著者は加藤邦拓、池松香である。掲載はProceedings of the 2023 ACM International Symposium on Wearable Computers（ISWC 2023）2件と、International Journal of Human-Computer Interaction（2025年12月）である。確認先は<https://doi.org/10.1145/3594738.3611362>、<https://doi.org/10.1145/3594738.3611378>、researchmapの公開論文欄<https://researchmap.jp/kkunihir/published_papers>である。
内容は、スマートフォンの画面一体型スピーカを音源として使い、近接した手の姿勢を音響で認識する系である。
CipherFluteとの関係は、市販端末のスピーカとマイクだけで音響センシングを成立させるという実装上の前提を共有する点である。CipherFluteは吹く音をマイクで拾うだけなので、こちらのほうが装置の条件は緩い。
新規性への脅威の度合いは低である。

**金彩回路を用いたオカリナ演奏支援システム**
著者は郭安邦、太田高志、加藤邦拓（いずれも東京工科大学）。掲載は第33回インタラクティブシステムとソフトウェアに関するワークショップ（WISS 2025）のデモ発表2-C23である。年は2025年である。確認先は<https://www.wiss.org/WISS2025Proceedings/data/demo/2-C23.pdf>である。予稿集索引で題名・著者・所属を確認した。PDFの本文テキストは埋め込みフォントの制約で抽出できなかったので、内容の記述は題名が述べる範囲にとどめる。加藤邦拓さんが可食金箔による回路（FoodSkin、<https://doi.org/10.1145/3613904.3642372>）と伝統工芸技法を用いた日用品への回路組み込み（科研費課題、<https://cir.nii.ac.jp/crid/1040589375703469568>）を継続的に扱っていることから、金属箔の回路をオカリナに施して運指などを検出し演奏を支援する系だと推測されるが、これは推測であって確認した事実ではない。
CipherFluteとの関係は、CipherFluteが投稿を狙うWISSの直近の回において、笛（オカリナ）を題材にした発表が同じ日本のコミュニティから出ているという場の状況である。査読者や聴衆が「WISSで笛といえばこれ」と想起する可能性がある。
新規性への脅威の度合いは中である。主要な主張は崩さない。オカリナは既製の楽器であって符号の担体ではなく、回路という電気的な仕掛けを必要とし、秘密や情報の埋め込みを扱っていない。しかし引用して「笛を電子的に拡張するのではなく、笛そのものの音高を符号にする」という差分を明示するのが誠実である。

**子どもの積み木造形における反復的創造プロセスを支援する音風景フィードバックシステム**
著者は中野仁美、加藤邦拓、太田高志。掲載は情報処理学会全国大会に相当するフォーラムの予稿である（researchmapの表示は2026年3月）。確認先は<https://researchmap.jp/kkunihir/published_papers>である。掲載誌の正式名称はresearchmapの表示からは確定できなかった。
内容は、積み木の造形に音の風景で反応を返す系である。
CipherFluteとの関係は、造形と音を結びつけるという括りにおいてのみである。
新規性への脅威の度合いは低である。

**FoodSkin: Fabricating Edible Gold Leaf Circuits on Food Surfaces**、**CircWood: Laser Printed Circuit Boards and Sensors for Affordable DIY Woodworking**、**Paper-Woven Circuits: Fabrication Approach for Papercraft-based Electronic Devices**
著者はそれぞれ加藤邦拓ら、石井綾郁ら、加藤邦拓らである。掲載はProceedings of the 2024 CHI Conference、TEI 2022の2件である。確認先は<https://doi.org/10.1145/3613904.3642372>、<https://doi.org/10.1145/3490149.3501317>、<https://doi.org/10.1145/3490149.3502253>である。
内容は、食品、木材、紙という日用の素材の上に回路を作る手法である。
CipherFluteとの関係は、日用品に機能を溶け込ませるという括りである。
新規性への脅威の度合いは低である。電気的な機能の付与であり、情報の符号化ではない。

### この研究者について言えること

加藤邦拓さんと共同研究者の池松香さんの系譜は、CipherFluteの新規性の主張にとって最も注意深い扱いを要する。「電源も電子部品も持たない受動的な物体が、市販の端末を介して離散的な符号を渡す」という枠組みは、2014年のExtensionStickerから2026年のDuoTouchまで一貫して日本で追求されており、SheetKeyでは明示的に認証の鍵として使われている。CipherFluteが物理層に新規性を置くことはできない。CipherFluteが置ける新規性は、音高という語彙を選んだこと、誤り訂正符号と隣接同値禁止を符号設計として持ち込んだこと、基準笛による環境正規化を構造で解いたこと、脅威モデルを明示して秘匿の力を秘密分散に負わせたこと、そして符号量が128ビット級に達することである。

---

## 4 鳴海紘也さん（慶應義塾大学理工学部、旧所属は東京大学）

### 確認した業績の件数

DBLPで45件、CiNiiの著者名検索で27件を確認した。重複を除いた実質の業績は65件前後である。CipherFluteに関わるものは9件である。

### 拾った仕事

**低出力ミリ波レーダで広範囲から読み取り可能なコーナーリフレクタ型チップレスRFID**
著者は飯塚達哉、笹谷拓也、小阪尚子、久田正樹、鳴海紘也、川原圭博。掲載はマルチメディア、分散、協調とモバイルシンポジウム2022論文集の1085ページから1091ページである。年は2022年（2022年7月6日）である。確認先は<https://cir.nii.ac.jp/crid/1050293246444164352>である。
内容は、コーナーリフレクタという幾何構造だけでできた電子部品も電源も持たない札に情報を刻み、低出力のミリ波レーダで読み出す手法である。屋外の見通しの悪い条件で、14メートル離れたドローンから8ビットの札を読み出す実地実験を行っている。
CipherFluteとの関係はきわめて近い。「電源も電子部品も持たない造形物の幾何そのものに数ビットを刻み、離れたところから市販に近い装置で読む」という構図が同型である。符号量が8ビットであることも、CipherFluteの笛1本あたり約3.7ビットと比較可能な数字である。
新規性への脅威の度合いは中である。読み出しの物理が電波であって音ではなく、読み手にミリ波レーダを要し、秘密の保管という応用文脈も脅威モデルもない。しかし国内で「無電源の幾何構造にビットを刻んで遠隔から読む」研究として引用しないと調査不足に見える。

**Weaving and Disguising Infrared Markers toward Invisible Textile Interaction**
著者はHal Sugiyama、Hsuanling Lee、Hanako Fujino、Mayuka Kuwana、Mustafa Doga Dogan、Liang He、鳴海紘也。掲載はExtended Abstracts of the 2026 CHI Conference on Human Factors in Computing Systemsである。年は2026年である。確認先は<https://doi.org/10.1145/3772363.3799013>である。
内容は、近赤外線を吸収する糸を織り込んで、可視光の下では通常の繊維と見分けがつかず近赤外線の撮像では高い明暗差を持つマーカを作る手法である。不可視性をさらに高めるために、糸の撚り合わせ、模様による囮、インクジェットの重ね刷り、後染めという四つの偽装手法を検討し、織り込んだ二次元コードを持つTシャツの試作を示している。
CipherFluteとの関係はきわめて近い。「日用品（衣服）に情報を埋め込み、意図的に偽装して見つけにくくし、専用の装置で読む」という三点がCipherFluteの主張とそのまま重なる。とくに「偽装（disguising）」を独立した設計課題として四手法に分解し、不可視性と可読性の両方を評価しているところは、CipherFluteが「探索コストの引き上げ」を物理層の役割だと述べる部分に正面から対応する。
新規性への脅威の度合いは中から高である。読み出しの物理が近赤外線であって音ではなく、符号は既存の二次元コードであり、誤り訂正の設計も基準素子による正規化も脅威モデルもない。しかしCipherFluteが「偽装による探索コストの引き上げ」を主張するなら、この論文の偽装手法の分類と評価に触れないわけにはいかない。

**GadJets: Air-Jet-Actuated Passive Materials and Mechanisms for Actuated and Shape-Changing Interfaces**
著者はSora Oka、Willa Yunqi Yang、Yifan Zou、Miyu Fukuoka、鳴海紘也、Yasuaki Kakehi、Ken Nakagaki。掲載はProceedings of the Twentieth International Conference on Tangible, Embedded, and Embodied Interaction（TEI 2026）である。年は2026年である。確認先は<https://doi.org/10.1145/3731459.3773313>である。
内容は、空気の噴流によって受動的な材料や機構を遠隔から動かす手法である。一つの駆動源で複数の受動モジュールを選択的に動かせることを設計空間として整理している。
CipherFluteとの関係は、空気の流れという駆動源だけで、電源を持たない造形物に機能を発現させるという構図が共通する点である。CipherFluteは人の息という空気の流れで受動物体に音を出させる。
新規性への脅威の度合いは低である。目的は形状変化するインタフェースであって情報の読み出しではなく、空気の供給に電動の装置を要する。

**TactPrint: 3D Printing Lattice-based Tactile Displays with Optimized and Local Vibration**
著者はRyota Sakuma、鳴海紘也、Yoshihiro Kawahara、Takefumi Hiraki。掲載はExtended Abstracts of the 2024 CHI Conferenceである。年は2024年である。確認先は<https://doi.org/10.1145/3613905.3648665>である。
内容は、3Dプリントした格子構造の振動特性を設計して局所的な触覚提示を行う手法である。
CipherFluteとの関係は、造形した格子構造の振動特性を設計変数として最適化するという点である。CipherFluteの管長設計と同じ性格の設計問題を扱っている。
新規性への脅威の度合いは低である。振動は触覚提示のためであり、情報の符号ではない。

**Micro-Gesture Recognition of Tongue via Bone Conduction Sound**
著者はShogo Tomaru、Ken Takaki、Hiroaki Murakami、Damyon Kim、鳴海紘也、Mitsuhiro Kamezaki、Yoshihiro Kawahara。掲載はAdjunct Proceedings of the 37th Annual ACM Symposium on User Interface Software and Technology（UIST Adjunct 2024）である。年は2024年である。確認先は<https://doi.org/10.1145/3672539.3686336>である。
内容は、骨伝導の音から舌の微細な動きを認識する手法である。
CipherFluteとの関係は、口腔の動きを音で読むという点にとどまる。
新規性への脅威の度合いは低である。

**Inkjet 4D Print: Self-folding Tessellated Origami Objects by Inkjet UV Printing**、**Pop-up Print: Rapidly 3D Printing Mechanically Reversible Objects in the Folded State**、**Blow-up Print: Rapidly 3D Printing Inflatable Objects in the Compressed State**、**Zip-up Print: Rapid and Assemblable 3D printing Using 2D Flattened Zipper-like Structures**
著者は鳴海紘也らである。掲載はACM Transactions on Graphics 42巻4号、UIST 2020、SIGGRAPH 2022 Posters、CHI 2026である。確認先は<https://doi.org/10.1145/3592409>、<https://doi.org/10.1145/3379337.3415853>、<https://doi.org/10.1145/3532719.3543230>、<https://doi.org/10.1145/3772318.3790538>である。
内容は、平たく畳んだ状態で高速に印刷して後から立体に展開する一連の造形手法である。
CipherFluteとの関係は、印刷の向きと畳み方を設計して造形時間と支持材を削るという方法論を共有する点である。CipherFluteの半割り笛が平置きでサポート材なしに印刷できるという主張は、この系統と同じ発想である。
新規性への脅威の度合いは低である。

**Yarnkey: 導電糸による2次元パターンのタッチセンシングを利用した太股上ウェアラブル入力デバイス**
著者は柴田謙、鳴海紘也。掲載はマルチメディア、分散、協調とモバイルシンポジウム2022論文集である。年は2022年である。確認先は<https://cir.nii.ac.jp/crid/1050011771467462528>である。
内容は、導電糸で織った二次元のパターンを使って衣服の上でタッチ入力を取る手法である。
CipherFluteとの関係は、日用品（衣服）に印刷や織りで幾何パターンを仕込むという構図である。
新規性への脅威の度合いは低である。

### この研究者について言えること

鳴海紘也さんの業績のうち、チップレスRFIDと近赤外マーカの偽装の二件はCipherFluteの主張に直接触れる。前者は「無電源の幾何構造にビットを刻む」枠組み、後者は「日用品に埋めた情報を意図的に偽装する」枠組みをそれぞれ独立に確立している。CipherFluteはこの二つを引いて、音という物理層と、誤り訂正・基準素子・脅威モデルという符号設計上の三点で差分を述べるのが正確である。

---

## 5 久保勇貴さん（日本電信電話株式会社）

### 確認した業績の件数

DBLPの著者識別子29/5947には54レコードが集まっているが、これは同姓同名が混在したまとまりである。音源分離と多チャネル音声強調（猿渡洋研究室系）、宇宙機の姿勢制御、DARPA地下探査のロボティクス、人工上腕頭のモデリング、無線センサネットワーク、対話ロボット競技会という互いに無関係な系統が同一の識別子に入っている。このうちヒューマンコンピュータインタラクションの系統（筑波大学の志築文太郎研究室出身で日本電信電話株式会社に在籍する久保勇貴さん）は18件である。CiNiiの著者名検索は55件を返したが、確認したところ本人のものはなく、宇宙機や太陽電池パドルを扱う別の久保勇貴さんのものであった。CipherFluteに関わるものは6件である。

### 拾った仕事

**FabAuth: Printed Objects Identification Using Resonant Properties of Their Inner Structures**（および続編の3D-Printed Object Identification Method using Inner Structure Patterns Configured by Slicer Software、および和文の「内部構造パターンの差異を利用した3Dプリントオブジェクト識別手法」）
著者は久保勇貴、江口佳那、青木良輔、近藤重邦、東正造、犬童拓也。掲載はExtended Abstracts of the 2019 CHI Conference（FabAuth）、Extended Abstracts of the 2020 CHI Conference（続編、著者は久保勇貴、江口佳那、青木良輔の3名）、第27回インタラクティブシステムとソフトウェアに関するワークショップ（WISS 2019）である。確認先は<https://doi.org/10.1145/3290607.3313005>、<https://doi.org/10.1145/3334480.3382847>、<https://www.wiss.org/WISS2019Proceedings/oral/8.pdf>である。
内容は、スライサで設定する充填率と充填パターンの違いによって外観の同じ造形物に固有の音響周波数応答を割り当て、圧電素子による掃引信号と機械学習で識別する手法である。
CipherFluteとの関係は前段の調査（<https://.../00-digest.md>）で既に整理されているとおりである。今回の深掘りで新たに分かったのは、この三件が久保勇貴さんの造形物関連の業績の全部であり、続編もそれ以降の展開もないということである。CiNiiの全文検索で「内部構造パターン」「3Dプリントオブジェクト 識別」を引いても該当がゼロだった（`https://cir.nii.ac.jp/opensearch/all?q=...`）。
新規性への脅威の度合いは高である（前段の判定を維持する）。ただし2020年で系列が止まっており、CipherFluteが到達する128ビット級の符号量へ向かう続編は存在しない。

**AudioTouch: Minimally Invasive Sensing of Micro-Gestures via Active Bio-Acoustic Sensing**
著者は久保勇貴、Yuto Koguchi、志築文太郎、高橋伸、Otmar Hilliges。掲載はProceedings of the 21st International Conference on Human-Computer Interaction with Mobile Devices and Services（MobileHCI 2019）である。年は2019年である。確認先は<https://doi.org/10.1145/3338286.3340147>である。
内容は、手の甲に貼った振動子とマイクで手の内部を能動的に音響センシングし、微細なジェスチャを認識する手法である。
CipherFluteとの関係は、能動音響センシングという方法の系譜に久保勇貴さん自身が広く関わっていることを示す点である。
新規性への脅威の度合いは低である。

**CanalSense: Face-Related Movement Recognition System based on Sensing Air Pressure in Ear Canals**（および続編のCanalSense+）
著者はToshiyuki Ando、久保勇貴、志築文太郎、高橋伸。掲載はProceedings of the 30th Annual ACM Symposium on User Interface Software and Technology（UIST 2017）およびExtended Abstracts of the 2018 CHI Conferenceである。確認先は<https://doi.org/10.1145/3126594.3126649>と<https://doi.org/10.1145/3170427.3186600>である。
内容は、外耳道内の気圧の変化を測って顔の動きを認識する手法である。
CipherFluteとの関係は、空気の圧力という媒体を情報の担体にする点にとどまる。
新規性への脅威の度合いは低である。

**Assisting with Fingertip Force Control by Active Bio-Acoustic Sensing and Electrical Muscle Stimulation**（および前身のUIST Adjunct 2021版）
著者はArinobu Niijima、久保勇貴。掲載はProceedings of the 2023 CHI ConferenceおよびUIST Adjunct 2021である。確認先は<https://doi.org/10.1145/3544548.3581192>と<https://doi.org/10.1145/3474349.3480214>である。
内容は、能動的な生体音響センシングと電気刺激を組み合わせて指先の力の制御を助ける手法である。
CipherFluteとの関係は能動音響センシングの系譜という点にとどまる。
新規性への脅威の度合いは低である。

### この研究者について言えること

久保勇貴さんの造形物識別の系列は2019年と2020年で完結しており、CipherFluteが最も注意深く差分を述べる必要のある相手であることは前段の判定どおりである。同時に、この系列が8クラスの識別（3ビット相当）で止まったまま続編がないという事実は、CipherFluteの符号量（笛40本から49本で128ビット）を新規性として述べる根拠になる。

---

## 6 上平員丈さん・鳥井秀幸さん（神奈川工科大学）

この二人の業績は不可分なので一つの節にまとめる。ただし件数は別に数える。

### 確認した業績の件数

上平員丈さんはDBLPで47件、CiNiiの著者名検索で197件を確認した。鳥井秀幸さんはDBLPで34件、CiNiiの著者名検索で74件を確認した。researchmapは`https://researchmap.jp/torii`が同姓の別人（鳥居寛之さん、ミュオンの超微細構造の分光）だったため使えなかった。二人の重複を除いた実質の業績は230件前後である。CipherFluteに関わるものは、3Dプリンタ造形物への情報埋め込みの系列が英語8件と和文22件の計30件、実物体への光学的な情報重畳（光透かし）の系列が約15件である。

### 拾った仕事（3Dプリンタ造形物への情報埋め込みの系列、英語）

いずれも著者は鈴木雅洋、ピヤラット シラパスパコォンウォン、鳥井秀幸、上平員丈、高嶋洋一、海野浩らの組み合わせである。

1. **Nondestructive Readout of Copyright Information Embedded in Objects Fabricated with 3-D Printers**、International Workshop on Digital Watermarking 2015、<https://doi.org/10.1007/978-3-319-31960-5_19>
2. **Copyright Protection for 3D Printing by Embedding Information Inside Real Fabricated Objects**、VISAPP 2015、<https://doi.org/10.5220/0005342401800185>
3. **Copyright Protection for 3D Printing by Embedding Information Inside 3D-Printed Objects**、International Workshop on Digital Watermarking 2016、<https://doi.org/10.1007/978-3-319-53465-7_27>
4. **Embedding Information into Objects Fabricated With 3-D Printers by Forming Fine Cavities inside Them**、Media Watermarking, Security, and Forensics 2017、<https://doi.org/10.2352/ISSN.2470-1173.2017.7.MWSF-317>
5. **Number of Detectable Gradations in X-Ray Photographs of Cavities Inside 3-D Printed Objects**、IEICE Transactions on Information and Systems 2017、<https://doi.org/10.1587/transinf.2016EDL8213>
6. **Information Hiding Inside 3-D Printed Objects by Forming High Reflectance Projections**、International Conference on Video and Image Processing 2017、<https://doi.org/10.1145/3177404.3177455>
7. **A Mobile Scanner Application for Embedding Data inside 3D Fabricated Objects**、IEEE International Conference on Life Sciences and Technologies 2022、<https://doi.org/10.1109/LifeTech53646.2022.9754740>
8. **GAN technique for reading QR code embedded in 3D printed object**、International Conference on Image, Video and Signal Processing 2023、<https://doi.org/10.1145/3591156.3591179>

### 拾った仕事（同系列、和文）

電子情報通信学会技術研究報告、映像情報メディア学会技術報告、画像電子学会研究会講演予稿、情報科学技術フォーラム講演論文集に22件が分布している。代表的なものを挙げる。

- 3Dプリンター造形物内部に埋め込んだ情報のサーモグラフィによる非破壊読出し（2014年9月、<https://cir.nii.ac.jp/crid/1520009409288208640>）
- 3Dプリント用デジタルデータの著作権保護のための情報ハイディング技術（情報処理学会コンピュータセキュリティ研究会、2014年6月、<https://cir.nii.ac.jp/crid/1573105977687785088>）
- 石膏材による3Dプリンター造形物への情報埋め込みと読み出し技術（2016年5月、<https://cir.nii.ac.jp/crid/1520572358479877760>）
- 内壁の構造化による3Dプリンター造形物への情報埋め込み技術（2016年7月、<https://cir.nii.ac.jp/crid/1520009407351160576>）
- 3Dプリンター造形物への情報埋め込みと近赤外線透視像による読み出し技術（2016年8月、<https://cir.nii.ac.jp/crid/1520009407437022848>）
- 3Dプリンター造形物への高反射率材料による情報埋め込みと近赤外線撮像による情報読み出し（2017年6月、<https://cir.nii.ac.jp/crid/1520290883087412352>）
- 近赤外蛍光樹脂による3Dプリンター造形物内への情報埋め込み（2017年11月、<https://cir.nii.ac.jp/crid/1520290882466514048>）
- 2色造形を用いた内部構造化による3Dプリンター造形物への情報埋め込み技術（2017年、<https://cir.nii.ac.jp/crid/1390848250115089792>）
- メタルライク樹脂による3Dプリンター造形物内への情報埋め込み（2018年3月、<https://cir.nii.ac.jp/crid/1520290883470341888>）

この系列を支えた科研費の課題を確認した。課題名は「3Dプリンタ造形物への情報埋め込み技術の研究」、研究代表者は鳥井秀幸さん（神奈川工科大学）、研究分担者は上平員丈さんと鈴木雅洋さん、種目は基盤研究(B)、課題番号は19H04141、研究期間は2019年4月1日から2023年3月31日まで、総額は1482万円である（<https://cir.nii.ac.jp/crid/1040282256991712384>）。それ以前に神奈川工科大学工学教育研究推進機構の「デジタルファブリケーションにおける違法造形防止技術に関する研究」が2015年から2017年まで続いている（<https://cir.nii.ac.jp/crid/1520572358914610688>など）。

内容は総じて、造形物の内部に空洞、石膏、高反射率材料、近赤外蛍光樹脂、メタルライク樹脂、2色造形による構造を作りこみ、外観を損なわずに、サーモグラフィ、X線、近赤外線の透視像あるいは反射像で非破壊に読み出す手法である。応用の文脈は一貫して3Dプリント用デジタルデータの著作権保護と違法造形の防止である。

CipherFluteとの関係は、「造形物の内部に情報を埋め込み、外観を損なわずに読み出す」という問題設定がまったく同じであることである。国内における造形物への情報埋め込みの最も体系的で最も長い系譜である。

新規性への脅威の度合いは中である。読み出しの物理が一貫して光学と熱であって音響ではなく、読み手にサーモグラフィ・X線装置・近赤外線カメラという専用の装置を要し、所有者の身体的な行為を要さず、脅威モデルの明示も秘密分散との組み合わせもない。CipherFluteの主要な主張を崩さないが、引用漏れは「国内先行を調べていない」という指摘を確実に招く。前段の調査の判定を維持する。

### 拾った仕事（実物体への光学的な情報重畳、光透かしの系列）

上平員丈さんは2008年から2021年にかけて、輝度を変調した照明を実物体に当てて情報を重ね書きし、撮像で読み出す一連の研究を行っている。代表的なものを挙げる。

- **Digital watermarking technique using brightness-modulated light**、IEEE International Conference on Multimedia and Expo 2008、<https://doi.org/10.1109/ICME.2008.4607420>
- **Optical watermarking technology for protecting portrait rights of three-dimensional shaped real objects using one-dimensional high-frequency patterns**、Journal of Electronic Imaging 22巻3号、2013年、<https://doi.org/10.1117/1.JEI.22.3.033004>
- 光透かしを用いた符号情報埋め込み技術、画像電子学会誌、2011年、<https://cir.nii.ac.jp/crid/1390001204610560512>

CipherFluteとの関係は、実物体の側を改変せずに情報を重ねるという意味では逆方向であるが、「実物体を情報の担体として扱う」という発想の連続性を示す点である。
新規性への脅威の度合いは低である。

### 補足（鳥井秀幸さんのもう一つの顔）

鳥井秀幸さんの業績の大半（DBLPの34件のうち25件）は、実は3Dプリントではなく相関ゼロ域を持つ拡散符号系列（zero-correlation zone sequence）の設計理論である。代表例は**A new class of zero-correlation zone sequences**（IEEE Transactions on Information Theory 50巻3号、2004年、<https://doi.org/10.1109/TIT.2004.825399>）である。
CipherFluteとの関係は、CipherFluteが「隣り合う笛が同じ音にならない制約を課す」と述べる部分、すなわち符号語の集合に構造的な制約を入れて識別性を高めるという議論が、この分野の言葉では相関特性の設計に対応するという点である。直接の先行研究ではない。
新規性への脅威の度合いは低である。ただし、もしCipherFluteの符号設計を理論的に深めるなら、この分野の日本の第一人者が造形物への情報埋め込みも手がけているという事実は、査読の場で議論の質を上げる材料になる。

---

## 7 渡邊恵太さん（明治大学）

### 確認した業績の件数

DBLPの著者識別子65/415には58レコードが集まっているが、神経科学（細胞集成体の系列検出）、信号処理（動き推定のデータパス）、医工学（無線給電の神経刺激装置）、可視化（並行座標プロット）といった別人のレコードが混入している。ヒューマンコンピュータインタラクションの系統は35件前後である。researchmapの公開論文欄で47件、CiNiiの著者名検索で126件（同姓同名の混入あり）を確認した。重複と別人を除いた実質の業績は90件前後である。CipherFluteに関わるものは9件である。

### 拾った仕事

**ProtoHole: Prototyping Interactive 3D Printed Objects Using Holes and Acoustic Sensing**
著者は片倉翔平、渡邊恵太。掲載はExtended Abstracts of the 2018 CHI Conferenceである。年は2018年である。和文版は第25回インタラクティブシステムとソフトウェアに関するワークショップ（WISS 2017）である。確認先は<https://doi.org/10.1145/3170427.3188471>である。
前段の調査で既に整理されている。判定は中を維持する。

**PrintMotion: Actuating Printed Objects Using Actuators Equipped in a 3D Printer**
著者は片倉翔平、渡邊恵太。掲載はAdjunct Proceedings of the 31st Annual ACM Symposium on User Interface Software and Technology（UIST Adjunct 2018）である。年は2018年である。確認先は<https://doi.org/10.1145/3266037.3271627>である。
内容は、3Dプリンタが備える駆動機構をそのまま使って造形物を動かす手法である。
CipherFluteとの関係は、造形物に外部の装置を足さずに機能を発現させるという構図である。
新規性への脅威の度合いは低である。

**A 3D Printer Head as a Robotic Manipulator**
著者は片倉翔平、Yuto Kuroki、渡邊恵太。掲載はProceedings of the 32nd Annual ACM Symposium on User Interface Software and Technology（UIST 2019）である。年は2019年である。確認先は<https://doi.org/10.1145/3332165.3347885>である。
内容は、3Dプリンタのヘッドをロボットアームとして使い、造形と操作を同じ機械で行う手法である。
CipherFluteとの関係は、家庭用3Dプリンタの能力の拡張という文脈である。
新規性への脅威の度合いは低である。

**CursorCamouflage: multiple dummy cursors as a defense against shoulder surfing**
著者は渡邊恵太、Fumito Higuchi、Masahiko Inami、Takeo Igarashi。掲載はSIGGRAPH Asia 2012 Emerging Technologiesである。年は2012年である。確認先は<https://doi.org/10.1145/2407707.2407713>である。
内容は、複数の偽のカーソルを同時に表示して、肩越しの覗き見から入力を守る手法である。
CipherFluteとの関係は、秘密の入力を物理的な観察から守るという問題設定である。CipherFluteは逆に「音は誰にでも聞こえる」と認めて秘匿の力を秘密分散に負わせているので、対照として引く価値がある。
新規性への脅威の度合いは低である。画面上の入力の話であり、造形物も音も扱わない。

**Exploring the Mechanism of Self-Attribution Occurrence using Multiple Dummy Cursors**
著者はKazuma Takada、渡邊恵太。年は2022年である。確認先はresearchmapの公開論文欄<https://researchmap.jp/keitawatanabe/published_papers>である。掲載誌はresearchmapの表示からは確定できなかったので、書誌を引く場合は要確認である。
内容はCursorCamouflageの延長で、偽のカーソル群のなかで自分のカーソルを自分のものだと感じる機構の解明である。関連する科研費課題「インタラクションにおける自己帰属プロセスの解明」も存在する（<https://cir.nii.ac.jp/crid/1040000781927535104>）。
新規性への脅威の度合いは低である。

**CastOven: a microwave oven with just-in-time video clips**
著者は渡邊恵太、Shota Matsuda、Michiaki Yasumura、Masahiko Inami、Takeo Igarashi。掲載はUbiComp 2010 Adjunct Papersである。年は2010年である。確認先は<https://doi.org/10.1145/1864431.1864448>である。
内容は、電子レンジという日用品に映像の機能を溶け込ませる系である。
CipherFluteとの関係は、日用品に機能を溶け込ませるという括りである。
新規性への脅威の度合いは低である。

**WireMolding: 3D Modeling Approach Involving Molding with Wire**、**Filum: A Sewing Technique to Alter Textile Shapes**
著者はKazumi Yoshimuraと渡邊恵太、Tomomi Konoと渡邊恵太である。掲載はTEI 2017およびUIST Adjunct 2017である。確認先は<https://doi.org/10.1145/3024969.3025059>と<https://doi.org/10.1145/3131785.3131797>である。
内容は、針金や糸という日用の素材で形と機能を作る手法である。
新規性への脅威の度合いは低である。

**あアラウド法（Ah-Aloud）の一連の研究**
著者は川島拓也、渡邊恵太ほかである。掲載はCHIuXiD 2022、Proceedings of the ACM on Human-Computer Interaction 8巻CHI PLAY号（2024年）などである。確認先は<https://doi.org/10.1109/CHIuXiD57244.2022.10009797>と<https://doi.org/10.1145/3677056>である。
内容は、「あ」という発声の音響的な特徴から体験中の認知過程や感情を読む手法である。
CipherFluteとの関係は、人が口から出す音を情報源として使う点にとどまる。
新規性への脅威の度合いは低である。

### この研究者について言えること

渡邊恵太さんの研究室は、片倉翔平さんが在籍した2017年から2019年にかけて3Dプリンタと音響に集中的に取り組み、その後は仮想現実、疑似触覚、脳計算機インタフェースへ軸を移している。造形物に情報を埋め込む仕事も、無電源の物体で符号を運ぶ仕事も見つからなかった。CipherFluteが引くべきはProtoHoleの一件に集約され、それは前段の調査で既に押さえられている。

---

## 8 片倉翔平さん（ハッソ・プラットナー研究所／ポツダム大学、旧所属は明治大学）

### 確認した業績の件数

DBLPで14件、CiNiiの著者名検索で2件（いずれも国際会議の参加報告）を確認した。重複を除いた実質の業績は15件である。CipherFluteに関わるものは6件である。この研究者は業績数が少ないので、全件を実際に見て分類できた。

### 拾った仕事

**ProtoHole**（渡邊恵太さんの節に記載、判定は中）、**PrintMotion**（同、低）、**A 3D Printer Head as a Robotic Manipulator**（同、低）。

**Trusscillator: a System for Fabricating Human-Scale Human-Powered Oscillating Devices**
著者はRobert Kovacs、Lukas Rambold、Lukas Fritzsche、Dominik Meier、Jotaro Shigeyama、片倉翔平、Ran Zhang、Patrick Baudisch。掲載はProceedings of the 34th Annual ACM Symposium on User Interface Software and Technology（UIST 2021）である。年は2021年である。確認先は<https://doi.org/10.1145/3472749.3474807>である。
内容は、人の力だけで振動する等身大の装置（ブランコやシーソーの類）を、共振周波数を設計しながら作るためのシステムである。
CipherFluteとの関係は、電源を持たない造形物の共振周波数を設計変数として計算し、それを狙って作るという設計行為が同型である点である。CipherFluteが管長Lと基本周波数fの関係を f = A/(L+e) で近似して設計するのと、Trusscillatorが人力の振動体の共振周波数を設計するのは、規模が違うだけで同じ設計問題である。
新規性への脅威の度合いは低である。共振周波数を符号として使う発想はなく、情報も秘密も扱わない。ただし「無電源の造形物の共振を設計する」系譜として引用の候補になる。

**Kerfmeter: Automatic Kerf Calibration for Laser Cutting**
著者は片倉翔平、Martin Taraz、Muhammad Abdullah、Paul Methfessel、Lukas Rambold、Robert Kovacs、Patrick Baudisch。掲載はProceedings of the 2023 CHI Conferenceである。年は2023年である。確認先は<https://doi.org/10.1145/3544548.3580914>である。
内容は、レーザ加工機の切り幅（カーフ）を自動で較正する手法である。個々の機械と材料の差を実測して補正するという構図である。
CipherFluteとの関係は、製造機と材料の個体差を較正で吸収するという方法論を共有する点である。CipherFluteが係数Aとeを較正で決め、さらに基準笛で環境のずれを吸収するのと同じ性格の問題である。
新規性への脅威の度合いは低である。

**AirForce: Personal Fabrication of Large-Scale, Load-Bearing Animatronics Structures from a Single Tube**
著者はLukas Rambold、Robert Kovacs、Min Deng、Antonius Naumann、Konrad Gerlach、Horatio Hamkins、Helena Lendowski、Chiao Fang、片倉翔平、Conrad Lempert、Muhammad Abdullah、Patrick Baudisch。掲載はProceedings of the 2026 CHI Conferenceである。年は2026年である。確認先は<https://doi.org/10.1145/3772318.3791706>である。
内容は、一本の管から大型で荷重を支えるアニマトロニクス構造を作る手法である。空気を使って駆動する。
CipherFluteとの関係は、管という単純な構造と空気の流れで機能を出すという括りにとどまる。
新規性への脅威の度合いは低である。

### この研究者について言えること

片倉翔平さんの業績は明治大学時代の3Dプリンタと音響から、ハッソ・プラットナー研究所でのレーザ加工と大型構造の製造へ移っている。CipherFluteが引くべきはProtoHoleであり、加えてTrusscillatorとKerfmeterを「無電源の造形物の共振を設計する」「製造の個体差を較正で吸収する」という二つの方法論の先例として引く選択肢がある。

---

## 9 伊藤雄一さん（青山学院大学理工学部、旧所属は大阪大学）

### 確認した業績の件数

DBLPで104件、CiNiiの著者名検索で300件（同姓同名の物理学者などの混入あり）、研究室χLab.の業績ページ（<https://x-lab.team/publications/>）を確認した。重複と別人を除いた実質の業績は250件を超える。CipherFluteに関わるものは18件である。

### 拾った仕事（アクティブ音響センシングによる物体識別の系列）

この系列は、CiNiiの全文検索で「アクティブ音響センシング」を引いた結果（該当34件）から系統的に取り出した。伊藤雄一さんのものは7件である。

**アクティブ音響センシングを用いた物体識別と位置推定**
著者は岩瀬大輝、伊藤雄一、秦秀彦、山下真由、尾上孝雄。掲載は電子情報通信学会技術研究報告、映像情報メディア学会技術報告、ヒューマンインタフェース学会研究報告集の三誌である。年は2017年6月である。確認先は<https://cir.nii.ac.jp/crid/1520572358619297024>である。
これが系列の最初である。

**アクティブ音響センシングによる日常物体識別と位置推定**
著者は岩瀬大輝、伊藤雄一、秦秀彦、山下真由、尾上孝雄。掲載は情報処理学会インタラクション2018論文集の62ページから71ページである。年は2018年である。確認先は<http://www.interaction-ipsj.org/proceedings/2018/data/pdf/INT18008.pdf>である。
前段の調査で既に押さえられている。判定は中を維持する。

**SenseSurface: Using Active Acoustic Sensing to Detect What is Where**（和文題名は「SenseSurface: アクティブ音響センシングによる物体識別と位置推定」）
著者は岩瀬大輝、伊藤雄一、秦秀彦、尾上孝雄。掲載は情報処理学会論文誌60巻10号の1869ページから1880ページである。年は2019年10月である。確認先は<https://cir.nii.ac.jp/crid/1050282813791887744>である。
内容は、平板の上に置かれた物体の種類と位置を、板を伝わる音響信号の周波数応答の違いから識別する手法である。物体の種類の識別で98.9パーセント、単一物体の位置の識別で89.2パーセント、複数物体を同時に置いた場合で最大98.3パーセントの精度である。
CipherFluteとの関係は、日用の物体を音響で識別するという構図である。前段の調査ではインタラクション2018版だけが拾われていたが、これはその論文誌版であり、より詳しい数字と評価を含む。CipherFluteが「音響で物体を読む国内研究」を引くなら、査読つきの論文誌版であるこちらを引くべきである。
新規性への脅威の度合いは中である。物体側に符号を設計して埋め込むわけではなく、能動的な加振と機械学習を要する。

**アクティブ音響センシングを用いた物体情報識別における環境温度変化に関する一検討**
著者は川崎祐太、伊藤雄一、藤田和之、尾上孝雄。掲載はヒューマンインタフェース学会研究会研究報告集22巻の55ページから60ページである。年は2020年である。確認先は<https://cir.nii.ac.jp/crid/1520009409573385216>である。
内容は、音響で物体を識別する系において環境温度の変化が識別精度を落とすという問題を扱った検討である。
CipherFluteとの関係は、前段の調査で拾われた情報処理学会論文誌62巻10号（2021年10月、<https://cir.nii.ac.jp/crid/1390290701132201344>）の前身であり、この問題が2020年の研究会の段階から日本語で明示的に議論されていたことを示す点である。CipherFluteの基準笛による正規化は、問題の発見としてはこちらが先である。
新規性への脅威の度合いは中である。CipherFluteは「温度で音がずれるという問題は既知であり、我々の貢献は既知音高の基準体を同じ造形物に同居させて比で読むという構造的な解法である」と述べるのが正確である。

この系列を支えた科研費の課題を確認した。課題名は「アクティブ音響センシングによる表面センサ化技術の確立とその応用」、研究代表者は伊藤雄一さん（青山学院大学）、研究分担者は杉浦裕太さん（慶應義塾大学）と高嶋和毅さん（東北大学）、種目は基盤研究(B)、課題番号は20H04228、研究期間は2020年4月1日から2023年3月31日までである（<https://cir.nii.ac.jp/crid/1040566775673251200>）。

**Recognizing object localization using acoustic markers with active acoustic sensing**
著者はFuma Kishi（岸楓馬）、Kodai Ito（伊藤弘大）、Kazuyuki Fujita（藤田和之）、伊藤雄一。掲載はQuality and User Experience 9巻1号である。年は2024年（2024年3月11日）である。確認先は<https://doi.org/10.1007/s41233-024-00066-x>である。書誌はCrossrefで確認した（<https://api.crossref.org/works/10.1007/s41233-024-00066-x>）。Springer Linkの本文は認証画面に転送されて取得できなかったため、内容は検索結果に現れた記述に基づく。
内容は、物体に貼った薄型スピーカを「音響マーカ」として使い、音源からの距離に応じて高い周波数成分が低い周波数成分より強く減衰するという性質を利用して、ランダムフォレストで面上の位置を推定する手法である。木製の板の20センチメートル四方の領域で、単一物体の位置を平均絶対誤差0.41センチメートルで、4物体の配置を1.83センチメートルの精度で推定する。
CipherFluteとの関係は、題名の「音響マーカ」という語がCipherFluteの笛と重なって見える点である。しかし実体は薄型スピーカという電源を要する能動素子であり、CipherFluteの無電源の笛とは性質が異なる。
新規性への脅威の度合いは低である。むしろ「音響マーカという語が既に別の意味（能動スピーカ）で使われている」という語の衝突に注意すべきである。CipherFluteでこの語を使うなら定義を明示するのが安全である。

**棒の引っかきによる音波を用いたインタラクション取得手法の検討**
著者は林吉経、尾崎亮太、上堀まい、岩本涼、菊地萌花、石黒成紀、伊藤雄一。掲載は第33回インタラクティブシステムとソフトウェアに関するワークショップ（WISS 2025）のデモ発表1-C30である。年は2025年である。確認先は<https://www.wiss.org/WISS2025Proceedings/data/demo/1-C30.pdf>である。
前段の調査で既に押さえられている。判定は中を維持する。なお前段の調査では所属を「DAIKEN株式会社」と記していたが、予稿集索引では岩本涼さん、菊地萌花さん、石黒成紀さんの3名がDAIKEN株式会社、林吉経さんと尾崎亮太さんと伊藤雄一さんが青山学院大学、上堀まいさんが青山学院大学および日本学術振興会である。前段の記述にあった「岩本諒」は「岩本涼」が正しい。

**PUNIcon: ゲルを用いた柔らかい物体の物体識別およびインタラクションの取得**
著者は伊藤雄一ほか。掲載は情報処理学会インタラクション2025予稿集である。年は2025年である。確認先は<https://cir.nii.ac.jp/crid/1010025255246587393>である。CiNiiの表示では共著者が省略されており、完全な著者一覧は確認できなかった。
内容は、ゲルを使った柔らかい物体の識別とインタラクションの取得である。
CipherFluteとの関係は、物体の材質と形が識別の手がかりになるという構図である。
新規性への脅威の度合いは低である。

### 拾った仕事（無電源の受動物体を市販装置で識別する系列）

**PUCs: detecting transparent, passive untouched capacitive widgets on unmodified multi-touch displays**
著者はSimon Voelker、Kosuke Nakajima、Christian Thoresen、伊藤雄一、Kjell Ivar Øvergård、Jan O. Borchers。掲載はProceedings of the 2013 ACM International Conference on Interactive Tabletops and Surfaces（ITS 2013）である。年は2013年である。確認先は<https://doi.org/10.1145/2512349.2512791>である。
内容は、透明で受動的な（電源を持たない）部品を、改変していない市販のマルチタッチディスプレイの上で識別する手法である。
CipherFluteとの関係は、「無電源の受動物体を、改変していない市販の装置で識別する」という枠組みが同型である点である。加藤邦拓さんと池松香さんの系譜（LightTouch、ShiftTouch、DuoTouch）の国際的な先行研究でもある。
新規性への脅威の度合いは中である。読み出しが静電容量であり、符号の語彙も誤り訂正もない。

### 拾った仕事（日用品に振動と音で情報を持たせる系列）

**Funbrella: recording and replaying vibrations through an umbrella axis**（および和文の「アソブレラ: 振動を記録・再生可能な傘型アンビエントインタフェース」日本バーチャルリアリティ学会論文誌2010年）
著者はKazuyuki Fujita、伊藤雄一、Ai Yoshida、Maya Ozaki、Tetsuya Kikukawa、Ryo Fukazawa、Kazuki Takashima、Yoshifumi Kitamura、Fumio Kishino。掲載はProceedings of the International Conference on Advances in Computer Entertainment Technology 2009である。確認先は<https://doi.org/10.1145/1690388.1690400>と<https://cir.nii.ac.jp/crid/1010282257108122496>である。
**U-brella: A portable umbrella-shaped device for vibrationizing information**
著者はYuichi Fujii、Fumio Kishino、Kazuyuki Fujita、伊藤雄一。掲載はIEEE Virtual Reality 2013である。確認先は<https://doi.org/10.1109/VR.2013.6549432>である。
内容は、傘という日用品の軸に伝わる振動を記録・再生し、あるいは情報を振動に変換して伝える系である。
CipherFluteとの関係は、日用品の振動を情報の担体にするという構図である。
新規性への脅威の度合いは低である。電源と電子部品を要する。

**Emoballoon: A balloon-shaped interface recognizing social touch interactions**
著者はKosuke Nakajima、伊藤雄一、Yusuke Hayashi、Kazuaki Ikeda、Kazuyuki Fujita、Takao Onoye。掲載はAdvances in Computer Entertainment 2013およびIEEE Virtual Reality 2013である。確認先は<https://doi.org/10.1007/978-3-319-03161-3_13>である。
内容は、風船の内部の気圧の変化から触り方を認識する系である。
CipherFluteとの関係は、空気の圧力を情報の担体にするという点にとどまる。
新規性への脅威の度合いは低である。

**DAWBalloon: An Intuitive Musical Interface Using Floating Balloons**
著者はMai Kamihori、Ayumu Ogura、Kodai Ito、伊藤雄一。掲載はUIST Adjunct 2022である。確認先は<https://doi.org/10.1145/3526114.3561354>である。
内容は、浮かぶ風船を使った音楽のインタフェースである。
CipherFluteとの関係は「楽器を作る仕事」という括りにおいてのみである。
新規性への脅威の度合いは低である。

**音で何が置かれているかを知る: 盤上物体識別装置**
著者は伊藤雄一。掲載は化学工業2021年3月号である。確認先は<https://cir.nii.ac.jp/crid/1521699230974962304>である。
内容はSenseSurfaceの一般向け解説である。
CipherFluteとの関係は、この系列が学術外の媒体にも紹介されており、日本の読者に知られている可能性が高いことを示す点である。
新規性への脅威の度合いは低である。

### この研究者について言えること

伊藤雄一さんの業績のうち、アクティブ音響センシングによる物体識別の系列（2017年から2025年まで7件、科研費基盤研究(B)一件）は、CipherFluteが位置づけを説明するうえで欠かせない国内の背景である。とくに環境温度の影響を扱った2020年の研究会報告と2021年の論文誌論文は、CipherFluteの基準笛の新規性を「問題の発見」ではなく「解法の構造」に置き直す必要があることを示している。一方で、この系列はすべて能動的な加振と機械学習を必要とし、物体の側に符号を設計して埋め込む発想はまったくない。

---

## 10 水木敬明さん（東北大学）

### 確認した業績の件数

DBLPで142件、CiNiiの著者名検索で206件を確認した。重複を除いた実質の業績は250件を超える。CipherFluteに関わるものは、日用品を電源不要の暗号装置にする系列が12件、カードの配布による鍵共有の系列が15件前後である。

### 拾った仕事（日用品を電源不要の暗号装置にする系列）

**Practical Card-Based Cryptography**
著者は水木敬明、静谷啓樹。掲載はProceedings of the 7th International Conference on Fun with Algorithms（FUN 2014）である。年は2014年である。確認先は<https://doi.org/10.1007/978-3-319-07890-8_27>である。
内容は、市販のトランプで安全な計算を実行する実用的なプロトコルである。
CipherFluteとの関係は、「電源も電子部品も持たない身近な道具だけで暗号的な機能を実現する」という枠組みそのものである。CipherFluteが物理層に暗号学的な力はないと宣言して秘匿を秘密分散に委ねるのに対し、カードベース暗号は物理操作そのものに情報理論的な安全性を持たせる。対照が鮮やかである。
新規性への脅威の度合いは中である。CipherFluteの主要な主張は崩さないが、「電源不要の物理暗号」という日本の大きな系譜を引かないと、投稿先（WISS）の読者に対して位置づけを説明できない。

**Secure Multiparty Computations Using a Dial Lock**
著者は水木敬明、Yoshinori Kugimoto、曽根秀昭。掲載はTheory and Applications of Models of Computation 2007（TAMC 2007）である。年は2007年である。確認先は<https://doi.org/10.1007/978-3-540-72504-6_45>である。
内容は、ダイヤル錠という日用品を使って安全な多者計算を行う手法である。
CipherFluteとの関係は、日用品そのものを暗号の道具に転用するという発想である。
新規性への脅威の度合いは中である。

**Secure Multiparty Computations Using the 15 Puzzle**
著者は水木敬明、Yoshinori Kugimoto、曽根秀昭。掲載はCombinatorial Optimization and Applications 2007（COCOA 2007）である。年は2007年である。確認先は<https://doi.org/10.1007/978-3-540-73556-4_28>である。
内容は、15パズルという玩具を使って安全な多者計算を行う手法である。
新規性への脅威の度合いは中である。

**Public-PEZ Cryptography**
著者はSoma Murata、宮原大輝、水木敬明、曽根秀昭。掲載はInformation Security 2020（ISC 2020）である。年は2020年である。確認先は<https://doi.org/10.1007/978-3-030-62974-8_4>である。
内容は、菓子のディスペンサ（PEZ）を暗号の装置として使う手法である。
CipherFluteとの関係は、まったく日用の物体を暗号の装置に変えるという点で、CipherFluteが日用品に笛を埋め込むのと発想の型が同じである。
新規性への脅威の度合いは中である。

**Multi-party Computation Based on Physical Coins**（および発展版のCoin-based Secure Computations、および和文の「コインを用いる新たなマルチパーティ計算」）
著者は駒野雄一、水木敬明。掲載はTheory and Practice of Natural Computing 2018（TPNC 2018）、International Journal of Information Security 21巻（2022年）、マルチメディア、分散協調とモバイルシンポジウム2018論文集である。確認先は<https://doi.org/10.1007/978-3-030-04070-3_7>、<https://doi.org/10.1007/s10207-022-00585-8>、<https://cir.nii.ac.jp/crid/1050292572112365568>である。
内容は、物理的な硬貨を使って安全な計算を行う手法である。
新規性への脅威の度合いは中である。

**ボールと袋を用いた秘密計算**
著者は宮原大輝、駒野雄一、水木敬明、曽根秀昭。掲載はマルチメディア、分散協調とモバイルシンポジウム2019論文集である。年は2019年である。確認先は<https://cir.nii.ac.jp/crid/1050855522099574656>である。
内容は、ボールと袋という日用品で秘密計算を行う手法である。
新規性への脅威の度合いは中である。

**Card-Based Protocols Using Regular Polygon Cards**、**Card-based Protocols Using Triangle Cards**
著者はKazumasa Shinagawa、水木敬明ほか。掲載はIEICE Transactions on Fundamentals 100巻9号（2017年）およびFUN 2018である。確認先は<https://doi.org/10.1587/transfun.E100.A.1900>と<https://doi.org/10.4230/LIPIcs.FUN.2018.31>である。
内容は、正多角形や三角形という「形」そのものが情報を担うカードを使うプロトコルである。
CipherFluteとの関係は、物体の幾何形状が符号を担うという発想である。CipherFluteが管長という一次元の量を符号にするのと、正多角形の回転角を符号にするのは同じ性格の設計である。
新規性への脅威の度合いは中である。

**Two UNO Decks Efficiently Perform Zero-Knowledge Proof for Sudoku**
著者はKodai Tanaka、水木敬明。掲載はFundamentals of Computation Theory 2023（FCT 2023）である。年は2023年である。確認先は<https://doi.org/10.1007/978-3-031-43587-4_29>である。
内容は、市販のカードゲームUNOの札二組で数独のゼロ知識証明を実行する手法である。
CipherFluteとの関係は、既製の日用品をそのまま暗号の道具として流用するという点である。
新規性への脅威の度合いは低である。

**Light Cryptography**
著者はPascal Lafourcade、水木敬明、Atsuki Nagao、Kazumasa Shinagawa。掲載はInformation Security Education 2019である。年は2019年である。確認先は<https://doi.org/10.1007/978-3-030-23451-5_7>である。
内容は、身近な道具を使う軽量な暗号を情報セキュリティ教育に用いる提案である。
新規性への脅威の度合いは低である。

**カードベース暗号とその展開（前編）情報セキュリティ教育にも応用可能な身近な道具を利用した暗号技術 1. カードベース暗号の歴史と概要**
著者は水木敬明。掲載は情報処理（情報処理学会誌）である。年は2026年5月である。確認先は<https://cir.nii.ac.jp/crid/1390026890675052288>である。
前段の調査で既に押さえられている。CipherFluteの投稿と同じ2026年に情報処理学会誌の特集になっているという事実は、WISSの読者がこの系譜を今まさに読んでいる可能性を示す。
新規性への脅威の度合いは中である。

### 拾った仕事（カードの配布による鍵共有の系列）

**Dealing Necessary and Sufficient Numbers of Cards for Sharing a One-Bit Secret Key**
著者は水木敬明、静谷啓樹、西関隆夫。掲載はAdvances in Cryptology – EUROCRYPT 1999である。年は1999年である。確認先は<https://doi.org/10.1007/3-540-48910-X_27>である。
和文の対応するものとして「1ビットの鍵共有に必要十分なカード配布枚数について」（情報処理学会アルゴリズム研究会報告、1998年、<https://cir.nii.ac.jp/crid/1571698602117026176>）、「秘密鍵共有に必要なカードの配布枚数に関する必要十分条件」（電子情報通信学会論文誌A、1999年1月、<https://cir.nii.ac.jp/crid/1520290885262496640>）などがある。この系列は1996年から2012年まで15件前後続いている。
内容は、カードをランダムに配ることで情報理論的に安全な鍵を共有する手法である。何枚のカードが必要十分かを厳密に決めている。
CipherFluteとの関係は、物理的な媒体（カード）の配布によって鍵を共有するという構図である。CipherFluteが2枚そろって初めてハートが現れるカードに秘密を分けて埋め込むという実装は、見た目が似ている。
新規性への脅威の度合いは低である。この系列は鍵の共有（key agreement）であって閾値秘密分散ではなく、物理媒体は情報の保管ではなく乱数の配布に使われている。CipherFluteが使う秘密分散とは数学的に別のものである。

### この研究者について言えること

水木敬明さんの業績を142件のDBLPレコードと206件のCiNiiレコードにわたって走査した結果、次の二つが確認できた。第一に、「電源も電子部品も持たない身近な道具で暗号的な機能を実現する」という系譜は日本において水木敬明さんを中心に30年にわたって築かれており、道具はトランプ、ダイヤル錠、15パズル、菓子のディスペンサ、硬貨、ボールと袋、UNOの札、正多角形のカードへと広がっている。CipherFluteはこの系譜の隣に立つものとして位置づけを述べるのが正確である。第二に、この系譜には3Dプリンタで作った造形物を扱ったものが一件もなく、音を扱ったものも一件もなく、閾値秘密分散を物理媒体に保管することを扱ったものも一件もない。

---

## 11 調査の途中で浮かんだ、対象外だが近接する研究者

依頼の対象ではないが、CiNiiの「アクティブ音響センシング」の全文検索（該当34件）で目立ったので記録しておく。

- 雨坂宇宙さんと志築文太郎さん（筑波大学）「ドアノブの握り方に基づくアクティブ音響センシングを用いた個人認証システムの検討」情報処理学会研究報告、2024年、<https://cir.nii.ac.jp/crid/1010025255259071745>。日用品（ドアノブ）を音響で読んで認証するという構図がCipherFluteと近い。
- 村尾和哉さん（立命館大学）の研究室は、アクティブ音響センシングを個人認証（指輪型デバイス、身体部位ごと、指紋の偽装検出）に応用する論文をDICOMOに継続して出している。<https://cir.nii.ac.jp/crid/1050297582267009536>、<https://cir.nii.ac.jp/crid/1050306031277949568>、<https://cir.nii.ac.jp/crid/1050306031277948800>。
- 渡邉拓貴さん（北海道大学）「モバイル/ウェアラブルデバイスにおけるアクティブ音響センシングの最前線」日本音響学会誌、2024年9月、<https://cir.nii.ac.jp/crid/1390020209538449920>。この分野の日本語の総説であり、CipherFluteが「音響センシング」の系譜に触れるなら引く価値がある。巻号とページは今回確認していない。

この三者はいずれも「音響で認証する」側であり、CipherFluteの「無電源の造形物に符号を刻む」側とは反対の立場にある。深掘りの対象を広げるなら次はここである。

---

## 12 今回の深掘りで新たに分かったことのまとめ

### 前段の調査に無かった重要な発見

1. 加藤邦拓さんと池松香さんの系譜が、CipherFluteの物理層の枠組みと最も広く重なる。SheetKey（2020年、印刷パターンを認証の鍵にする）とDuoTouch（2026年、無電源アタッチメントが二進符号列を生成し標準の応答インタフェースで復号され、しかも復号可能性を物理パラメータの上限式で論じ、日用品の形に埋め込む）の二件は、CipherFluteが「無電源の物体に符号を刻み市販端末で読む」という枠組みに新規性を置けないことを決定づける。
2. 鳴海紘也さんの共著に、無電源の幾何構造（コーナーリフレクタ）に8ビットを刻んでミリ波レーダで14メートル先から読む研究（2022年）と、衣服に情報を織り込んで四つの手法で偽装する研究（2026年）がある。後者は「偽装」を独立した設計課題として分解し評価しており、CipherFluteの「探索コストの引き上げ」の議論に正面から対応する。
3. 伊藤雄一さんの音響物体識別の系列は、前段の調査が拾ったインタラクション2018版と情報処理学会論文誌2021版のあいだに、査読つき論文誌版のSenseSurface（情報処理学会論文誌60巻10号、2019年）と、温度問題の初報（ヒューマンインタフェース学会研究会報告22巻、2020年）が挟まっている。系列全体は7件で、科研費基盤研究(B)（課題番号20H04228）に支えられている。
4. 加藤邦拓さんの研究室がWISS 2025で「金彩回路を用いたオカリナ演奏支援システム」というデモを出している。CipherFluteが投稿を狙う場で、笛を題材にした発表が同じコミュニティから出ている。
5. 水木敬明さんの「日用品を電源不要の暗号装置にする」系譜は、トランプ以外にダイヤル錠、15パズル、菓子のディスペンサ、硬貨、ボールと袋、UNOの札、正多角形のカードまで広がっている。前段の調査はカードベース暗号としてまとめていたが、日用品への拡張という側面はCipherFluteの「日用品への偽装」と直接に対応する。
6. 上平員丈さんと鳥井秀幸さんの系列を支えた科研費が課題番号19H04141の基盤研究(B)（2019年から2023年、総額1482万円、研究代表者は鳥井秀幸さん）であることを確認した。系列は英語8件と和文22件の計30件であり、国内で最も体系的である。
7. 久保勇貴さんの造形物識別は2019年と2020年の三件で完結し、続編がない。CiNiiの全文検索でも和文の続報はゼロである。
8. 片倉翔平さんは2021年以降ハッソ・プラットナー研究所に所属し、Trusscillator（無電源の造形物の共振周波数を設計する）とKerfmeter（製造の個体差を較正で吸収する）という、CipherFluteの設計方法論に対応する仕事を持つ。
9. 鳴海紘也さんの現所属は慶應義塾大学であり、片倉翔平さんの現所属はハッソ・プラットナー研究所である。

### 探したが存在しなかったこと

CipherFluteの新規性の主張の根拠になるので、丁寧に書く。

第一に、今回の11名について、DBLPの622レコード、CiNiiの1123レコード、researchmapと研究室業績ページの290件、WISS 2025の索引全体を走査したが、3Dプリンタで笛や管楽器そのものを造形した研究は一件もなかった。CiNiiの全文検索で「3Dプリンタ 笛」「3Dプリント 楽器 造形」「オカリナ 3Dプリンタ」を引いた結果はいずれも該当ゼロであった。加藤邦拓さんの研究室のオカリナは既製の楽器に回路を足すものである。

第二に、管長と基本周波数の関係を設計変数として離散化し、電源も計測器も機械学習も用いず、人が吹くだけで多数ビットの符号を読み出す研究は一件もなかった。伊藤雄一さんと久保勇貴さんの音響系はすべて能動的な加振（圧電素子やスピーカ）と機械学習を必要とする。片倉翔平さんと渡邊恵太さんのProtoHoleも物体の内部にスピーカとマイクを入れる。

第三に、誤り訂正符号を物理造形の符号設計に持ち込んだ研究は一件もなかった。上平員丈さんらの系列は誤り訂正を論じておらず、鳴海紘也さんのチップレスRFIDも8ビットの生の符号である。加藤邦拓さんと池松香さんのDuoTouchは復号精度を標本化限界の式で論じるが、誤り訂正符号は導入していない。

第四に、既知の値を持つ基準素子を同じ造形物に同居させて比で読むことによって環境変動を打ち消す構造的な解法は一件もなかった。伊藤雄一さんらは同じ問題（環境温度による音響特性のずれ）を2020年と2021年に扱っているが、解法は特徴量と学習の側にある。

第五に、暗号資産の復元用情報や閾値秘密分散の分け前を物理媒体に保管することを目的とした研究は一件もなかった。水木敬明さんの142件のDBLPレコードを検索したが、secret sharingという語を含むものは一件もなく（該当0件）、鍵共有はすべてカード配布による鍵合意であって閾値秘密分散ではない。

第六に、脅威モデルを明示した造形物の情報埋め込み研究は一件もなかった。上平員丈さんと鳥井秀幸さんの系列は著作権保護と違法造形防止を目的に掲げるが、攻撃者の能力と守れる範囲を定式化していない。久保勇貴さんのFabAuthは認証を名に冠しながら脅威モデルを述べていない。

第七に、水木敬明さんの物理暗号の系譜には3Dプリンタで造形した物体を扱ったものが一件もなく、音を扱ったものも一件もなかった。物理暗号の側とデジタルファブリケーションの側は、日本において接触していない。CipherFluteはこの二つの系譜の交点に立つと述べてよい。

### 残った課題

1. Google Patentsの検索応答が取得できなかったため、上平員丈さんと鳥井秀幸さんの3Dプリンタ情報埋め込みに関する特許、および日本電信電話株式会社の久保勇貴さんの造形物識別に関する特許を一件も確認していない。科研費の課題が基盤研究(B)まで進んでいることから特許が存在する可能性は高く、別途の確認が望ましい。
2. WISS 2025のデモ予稿（金彩回路のオカリナ、リズムゲームによる3Dプリンタ制御）の本文テキストを抽出できなかった。内容の記述は題名の範囲にとどまっている。実物のPDFを人が読んで内容を確定させる必要がある。
3. Quality and User Experience誌の「Recognizing object localization using acoustic markers」の本文を取得できていない。抄録の記述は検索結果に依拠している。
4. 渡邊恵太さんの「Exploring the Mechanism of Self-Attribution Occurrence using Multiple Dummy Cursors」（2022年）の掲載誌が確定していない。
5. WISS 2024およびそれ以前の回について、予稿集索引の全文走査を行っていない。WISS 2025のみ全文で走査した。CipherFluteがWISSに出すのであれば、少なくとも直近5回分の全題名を同じ手順で走査するのが望ましい。
6. 対象外だが近接する研究者として、雨坂宇宙さん・志築文太郎さん（筑波大学）、村尾和哉さん（立命館大学）、渡邉拓貴さん（北海道大学）の「音響で認証する」系譜が浮かんだ。次の深掘りの対象として推奨する。
