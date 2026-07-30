# 3Dプリントされた笛と気鳴楽器の計算設計

調査担当の切り口は、3Dプリントやデジタルファブリケーションで笛やオカリナなどの気鳴楽器を設計・製造する研究である。狙った音の高さに合わせ込む計算設計、共鳴のシミュレーション、自由な形の物体を楽器にする研究、複数の音を出す構造の設計、印刷後の調律を重点的に洗い出した。書誌情報はすべてCrossrefのDOI解決結果、DataCite、DBLP、Semantic Scholar、学会の予稿集ページ、著者や研究所の公式ページ、CiNii Researchのいずれかで確認した。確認先のURLを各項目に付けた。

このファイルは2026年7月30日に別の担当者が独立に検証し直した。訂正した箇所には、何をどう直したかを本文中に明記した。検証の全体像は末尾の「検証の記録」にまとめてある。

出力ファイルの指定パスに `undefined` という未展開の変数が含まれていたため、既存の `related_work_survey/raw/` ディレクトリに書き出した。

## この切り口の要約

この分野で最も危険な先行研究は、SIGGRAPH Asia 2016のPrintoneである。任意の自由形状の内部を中空化し、境界要素法で共鳴周波数を予測しながらフィップル(リコーダーやオカリナと同じ吹き口)と指孔を配置し、家庭用のFDM方式3Dプリンタで印刷して実際に旋律を演奏させている。16本の楽器を作り、56個の目標周波数のうち53個が実測範囲に入ったと報告している。つまり「印刷できる笛の形を計算して狙った音高に合わせ、実機で検証する」という部分は10年前にすでに達成されている。現在のCipherFluteの引用一覧にPrintoneが入っていないことは、この切り口で見つかった最大の穴である。

音高精度をセント単位で報告した査読文献はきわめて少なく、NIME 2016のDabinらの微分音リコーダーがほぼ唯一である。彼らはPolyJet方式で印刷したリコーダーで、初版が目標に対して+6から+34セント、次版が−40から+1セント、指孔をやすりで手修正した版が−13から+14セントという結果を出し、目標として「5セント以内」を掲げている。これはCipherFluteが半音(100セント)刻みのスロットを選び、基準笛による較正を必要とした判断の妥当性を、外部の数値で裏づける材料になる。

計算設計の道具としては、Paul Harrisonのオープンソースソフトウェアdemakeinが2012年から公開されており、管の断面形状と指孔の位置・径・深さを数値最適化して狙った運指と音階を実現し、3DプリンタやCNCで作れる形に変換する。フランスのInriaのopenwindは、インピーダンスの計算と管形状の最適化に加えて、測定したインピーダンスから管形状を復元する逆問題まで扱う。したがって「管の長さと周波数の対応を計算して形を決める」ことも「音から形を推定する」ことも既存技術である。加えて、今回の検証で新たに見つかったLanとWalthamのActa Acustica united with Acustica論文(2016年)とLanの博士論文(2015年)は、伝達行列法で中国の縦笛「簫」を設計するものであり、CipherFluteの一次元の経験式 f = A/(L+e) に最も近い位置にある。境界要素法のPrintoneより、こちらのほうがモデルの性質としては近い。

複数の共鳴管を1つの3Dプリント物体にまとめること自体にも査読つきの先行例がある。Szabóの3Dプリントのパンフルート合奏体(Jazz Research Journal, 2024年)である。したがって「多数の笛を1つの物体に融合した前例がない」という言い方は避けたほうがよい。差分は融合そのものではなく、音高の並びを符号語として読む点にある。

一方で、印刷した笛の音高を符号として読み、複数本の音高の並びで情報を運ぶという発想は、この切り口の文献にはまったく見つからなかった。最も近いのはGraphics Interface 2018のBlowholeであるが、これは開管の共鳴ではなくヘルムホルツ共鳴を使う。ただしBlowholeの識別クラス数や正解率といった数値は、今回の検証では本文に到達できず裏を取れなかった。系列符号化も誤り訂正も基準音による較正も持たないという点は、公開されている題名と概要の水準では確かめられる。

## 新規性への脅威が大きい文献

### 1. Printone: Interactive Resonance Simulation for Free-form Print-wind Instrument Design

- 著者: Nobuyuki Umetani, Athina Panotopoulou, Ryan Schmidt, Emily Whiting
- 発表: ACM Transactions on Graphics, Vol. 35, No. 6, 論文番号184, pp. 184:1-184:14, 2016年11月(SIGGRAPH Asia 2016)
- 確認先: https://doi.org/10.1145/2980179.2980250 (Crossrefで著者・巻号・ページ・年を確認), https://www.research.autodesk.com/publications/printone-interactive-resonance-simulation-for-free-form-print-wind-instrument-design/ (著者4名と掲載誌を確認)
- 論文番号184の確認先: 下記ISMA 2017版の参考文献[1]に「ACM Trans. Graph., vol. 35, no. 6, pp. 184:1-184:14, Nov. 2016」と自己引用されている
- 短縮版の確認先: Nobuyuki Umetani, Athina Panotopoulou, Ryan Schmidt, Emily Whiting, "Printone: Interactive Resonance Simulation for Print-wind Instrument Design", Proceedings of the 2017 International Symposium on Musical Acoustics, 6月18日から22日, モントリオール, pp. 18-21, 2017年, https://isma2017.cirmmt.mcgill.ca/proceedings/pdf/ISMA_2017_paper_47.pdf (本文を取得し、以下の数値をすべて原文で確認した)

内容の要約は次のとおりである。任意の三次元メッシュを取り込み、自動で中空化したうえで、フィップル型の吹き口と指孔をユーザーが対話的に配置していく。共鳴周波数の予測は境界要素法にもとづき、共鳴を非線形行列の最小固有値問題として定式化し、波数について一次のテイラー展開を行って一般化固有値問題に帰着させることで高速化している。指孔の径を連続的に変えるあいだは感度解析による粗い一次近似で毎秒30フレーム以上の応答を保ち、待機中により正確な計算を数秒で回す。なおISMA 2017版は、道具全体の平均動作速度を毎秒5フレームと報告している。目標周波数を複数の運指について指定すると、指孔の径を自動最適化する「AutoTune」機能がある。吹き口はFDM方式で作りやすいという理由でフィップルを選んでおり、CipherFluteと同じ発音機構である。ISMA 2017版は「16本のうち5本を図に示す」と述べており、設計・印刷した楽器は16本である。検証では、吹く速さを徐々に上げながら明瞭に鳴る最低周波数と最高周波数を記録し、「56個の目標周波数のうち53個が実測範囲に入った(53 out of 56 target frequencies)」と報告している。音色は扱わず基本周波数だけを対象にしていることを明記している。

CipherFluteとの関係を述べる。CipherFluteが行っている「フィップル笛の形状を計算で決め、家庭用FDM機で印刷し、狙った音高が出ることを実機で確かめる」という工程は、Printoneがより一般的な形状に対してすでに達成している。CipherFluteの近似式 f = A/(L+e) は、Printoneの境界要素法と比べれば著しく単純な一次元モデルであり、精度で勝る主張はできない。逆にCipherFluteの独自性は、単一の楽器で旋律を演奏することではなく、多数の単音笛を1つの日用品に融合して音高の並びに情報を載せる点にある。

脅威の度合いは「高」である。理由は三つある。第一に、印刷された笛の計算設計という技術的貢献をほぼ完全に先取りしている。第二に、現在の論文がこの研究を引用していないため、査読者に「最も基本的な先行研究を知らない」と受け取られる危険がきわめて大きい。第三に、Printoneが目標周波数への合わせ込みを実機で検証しているため、CipherFluteの実測評価も同じ土俵で比較されることになる。必ず引用し、「旋律を奏でる1本の楽器」対「情報を運ぶ多数の単音笛」という違いと、対話的な自由形状設計を必要としない理由を明示すべきである。

### 2. Blowhole: Blowing-Activated Tags for Interactive 3D-Printed Models

- 著者: Carlos Tejada, Osamu Fujimoto, Zhiyuan Li, Daniel Ashbrook
- 発表: Proceedings of the 44th Graphics Interface Conference, トロント, 5月8日から11日, pp. 131-137, 2018年
- 確認先: https://doi.org/10.20380/GI2018.18 (DOIのコンテンツネゴシエーションで著者・題名・ページ・年・出版者を確認), https://dblp.org/rec/conf/graphicsinterface/TejadaF0A18.bib (会議の正式名称・開催地・会期・編者・出版者ACMを確認), https://api.semanticscholar.org/graph/v1/paper/DOI:10.20380/GI2018.18 (著者4名と年を確認)
- 注意: 予稿集ページ http://graphicsinterface.org/proceedings/gi2018/gi2018-18/ は2026年7月30日時点でCloudflareのボット判定によりHTTP 403を返し、本文にも概要にも到達できなかった。ACM Digital Libraryの当該ページも403であった。出版者の表記はDOI登録情報ではCanadian Human-Computer Communications Society、DBLPではACMとなっており、両方が流通している。

内容の要約は次のとおりである。3Dモデルの内部に共鳴空洞を埋め込み、表面の目立たない開口から軽く息を吹き込むと固有の音が鳴り、計算機がその音でどの穴かを同定する。ここまでは題名と、CipherFluteが現に引用している内容と一致する。

以下の数値は、前任の調査担当者が書いたものであるが、今回の検証では本文に到達できなかったため裏が取れていない。引用するなら本文を入手して確かめ直す必要がある。すなわち、空洞が球形で細い管で表面につながりヘルムホルツ共鳴の式で共鳴周波数を見積もること、管の長さ・管の径・球の径で周波数を作り分けること、FDM機3種とSLA機で試作しSLA印刷のほうが予測値に平均で約100ヘルツ近いこと、1000ヘルツ未満は雑音が多いこと、管が長いほど雑音が増えること、ある空洞集合で全体98パーセントの正解率を得たが32ミリメートルの球を加えると90パーセントに下がること、同時に扱える穴が最大9個程度であること、既存モデルへ自動で穴を埋め込むソフトウェアを提供していることである。

CipherFluteとの関係を述べる。「印刷物に吹き込んで、鳴った音の高さから計算機が意味を読み取る」という一次的な仕組みが共通する。ただし発音機構がヘルムホルツ共鳴であって管の共鳴ではなく、1個の穴が1個の識別子を表すだけで、複数の音の並びを符号語として扱う設計、誤り訂正、基準音による較正、秘密の保管という発想はいずれもない。容量の比較については、Blowholeの識別クラス数が9個であるという前提が未検証であるため、「9クラスで約3.2ビット」という対比はそのままでは書けない。CipherFlute側の13スロットで約3.7ビットという数値は自分の設計であるから確かである。差は本数を並べて系列にする点と、環境変動を打ち消す基準笛を混ぜる点にある。

脅威の度合いは「高」である。現行論文がすでに引用してはいるが、読み出しの一次的な仕組みが最も近いため、査読者は真っ先にこの研究との差分を問う。ヘルムホルツ共鳴と開管共鳴の違い、識別クラス数と系列長、較正の有無、誤り訂正の有無を書き分ける必要がある。そのためには本文の入手が前提になるので、大学図書館経由などで確実に手に入れてから数値を書くべきである。

### 3. Demakein: design and make instruments

- 著者: Paul Francis Harrison
- 発表: ソフトウェア(査読論文ではない)。最初の版0.1をPyPIに2012年9月28日公開、GitHubのリポジトリは2013年5月31日作成、バージョン1.1を2025年7月26日公開
- 確認先: http://www.logarithmic.net/pfh/design (作者・機能・組み込み楽器・バージョン1.1が2025年7月であることを確認), https://github.com/pfh/demakein , https://pypi.org/pypi/demakein/json (全リリースの公開日時を確認), https://api.github.com/repos/pfh/demakein (リポジトリ作成日を確認)
- 前任の記述にあった「2014年公開」は誤りである。2014年という数字は、Dabinら(NIME 2016)の参考文献[10]が本ソフトウェアを「2014」と付記して引用していることに由来すると推測される。それは参照した年であって公開年ではない。

内容の要約は次のとおりである。Pythonで書かれた木管楽器の設計・製造ツールである。公式ページは「Demakein is software to design and make woodwind instruments using a 3D printer or CNC mill.」と自ら説明している。「design」段階では、与えた運指と音階に対して正しい音が出るように、管の断面形状と指孔の位置・径・深さを数値最適化する。「make」段階では、設計を三次元形状に変換し、3DプリンタやCNCで作れる部品に分割する。フルート、ホイッスル(フィップル笛)、ショームが組み込みで用意され、Pythonスクリプトを書けば任意の音階や運指の楽器を設計できる。作者は2025年時点でBambu Lab P1SによるPLA印刷を試していると記し、壁のループ数を非常に多くすれば中実に近い楽器が得られると述べている。なお「音響モデルは管が枝分かれした木構造の共鳴周波数を求める形で組まれている」という前任の記述は、公式ページとGitHubのREADMEには対応する明示的な記載がなく、今回の検証では裏が取れなかった。

CipherFluteとの関係を述べる。「狙った音階になるように笛の寸法を計算し、3Dプリンタで作る」というワークフローそのものが、査読論文の外で10年以上前から公開・実用されている。CipherFluteが提示する管長と周波数の対応づけは、この道具が扱う設計問題の最も単純な部分集合にあたる。

脅威の度合いは「中」である。査読論文ではないため学術的な先行性の主張は弱いが、デジタルファブリケーションの査読者はこの道具を知っている可能性が高く、「計算で笛を設計する」ことを新規性として掲げると即座に反証される。背景として引用し、CipherFluteの貢献が設計計算ではなく符号化にあることを述べるのが安全である。

### 4. 3D Modelling and Printing of Microtonal Flutes

- 著者: Matthew Dabin, Terumi Narushima, Stephen Beirne, Christian Ritz, Kraig Grady
- 発表: Proceedings of the 16th International Conference on New Interfaces for Musical Expression (NIME 2016), pp. 286-290, 2016年7月11日から15日, グリフィス大学, ブリスベン
- 確認先: https://nime.org/proc/nime2016_dabin/ (著者5名・題名・年・開催地・ページを確認), https://www.nime.org/proceedings/2016/nime2016_paper0056.pdf (本文を取得し、以下のセント値と設計手法をすべて原文の表1と本文で確認した)

内容の要約は次のとおりである。微分音音階を演奏するためのリコーダーと横笛を3Dプリントで作る研究である。設計にはBenadeの理論をHoekjeがまとめた簡略モデルをMATLABに書き直したものを使い、指孔を1つ開けたときの実効管長と管端補正を求め、開いた孔と閉じた孔の補正を順に積み上げて、目標周波数を出す孔の位置と径を決める。モデルの出典は本文中で二つに分かれており、全体のモデルはHoekjeの音楽音響のウェブ教材(参考文献[12])、リコーダー1の吹き口の管端補正はHoekjeがCatgut Acoustical Society Journalにまとめた要約(参考文献[11])に拠っている。吹き口はまずFDM機(Dimension uPrintPlus、ABS、層厚0.254ミリメートル)で作ったが、ラビウム(エッジ)の望む鋭さが出ず、ボア内壁の粗さのために奏者はより高い吹圧を出さねばならず、安定した音を立ち上げるまでに市販のフルートより長い時間がかかった。そこでPolyJet方式(Objet Connex 350、材料Objet MED610、層厚0.016ミリメートル)に切り替え、市販のアルトリコーダーの吹き口と比べて音高も必要な吹圧もほとんど区別がつかない品質を得ている。評価では無響環境でBehringer ECM8000により録音し、Melodyneで音高を求め、第7から第12の下方倍音にあたる音階について目標周波数との差をセントで報告している。初版のリコーダー1は+6から+34セント、リコーダー2は−40から+1セント、指孔2つをやすりで削って手修正したリコーダー2改は−13から+14セントであった。将来目標として「手作業の修正が不要になるよう、誤差を5セント以内に抑える」ことを掲げている。同一設計を複数本印刷すると音高がそろうことも、下方倍音リコーダーを同一設計で対にして印刷することで確認している。

CipherFluteとの関係を述べる。CipherFluteが半音(100セント)刻みのスロットを採用し、基準笛で全体のずれを打ち消す設計を選んだ根拠として、この論文の数値はきわめて有用である。数十セント規模の誤差が印刷楽器では普通に生じるという外部の実測があるため、100セント刻みという粗い量子化とパイロット較正の必要性を正当化できる。逆に、「印刷した笛の音高をセント単位で評価する」という評価方法自体は新しくない。

脅威の度合いは「中」である。CipherFluteの主要な主張は崩れないが、この論文の存在を無視して「印刷した笛の音高精度を測った」ことを新規性に数えると弱くなる。必ず引用し、報告されたセント値と自分の実測値を並べて示すべきである。

### 5. FlueBricks: A Construction Kit of Flute-like Instruments for Acoustic Reasoning

- 著者: Bo-Yu Chen(国立台湾大学), Chiao-Wei Huang(独立研究者), Lung-Pan Cheng(国立台湾大学)
- 発表: Proceedings of the 2026 CHI Conference on Human Factors in Computing Systems (CHI '26), 4月13日から17日, バルセロナ, 全18ページ, 2026年
- 確認先: https://doi.org/10.1145/3772318.3790595 (Crossrefで著者・会議名・年・ページを確認), https://arxiv.org/abs/2604.03636 (2026年4月4日投稿、CHI 2026採録と明記), https://arxiv.org/pdf/2604.03636 (本文全18ページを取得し、以下の記述をすべて原文で確認した)

内容の要約は次のとおりである。フィップル笛を「生成部(generator)」「共鳴部(resonator)」「連結部(connector)」の3種のモジュール族に分解し、組み替えながら吹いて音を確かめることで、吹き込み穴の形、管長、指孔の位置が立ち上がり・音高・音色をどう変えるかを体得させる構築キットである。LeMoの分類を引き継ぎつつ、笛は胴と孔から放射するという理由で「放射部」を省き、代わりに連結部を加えている。全モジュールをFFF方式またはFDM方式(Ultimaker S3およびS5)で作り、剛体部分をPLA、可撓部分(窓の調整具や締めリング)をTPUで印刷し、基準の設定は層厚0.1ミリメートル、充填率20パーセントである。生成部は8種の下位モジュール(Air intake, Air duct support, Air deflector, Air facade, Window regulator, Splitting edge, Labium support, Labium base)に分解されており、これらはオルガンのフルー管とフルートの音響研究から抽出した6つの内部形状、すなわちフルー管路(flue tunnel)、空気室(air chamber)、風道(windway)、窓(window)、分割エッジ(splitting edge)、発音室(sound chamber)に対応づけられている。前任の記述はここに「調律スロット」を含めていたが、これは誤りである。調律スロット(tuning node)は共鳴部の側の別モジュールであり、オルガンのフルー管の調律スロットに着想を得て、円形の指孔を縦長のスロットに置き換えるものである。連結部には、1つの息を複数の出口へ分配する「Air distribution hub」があり、二重音や持続低音のような多声構成を作れる。12名の参加者による探索的な利用調査を行い、楽器の足場づくり(instrument scaffolding)、規則の形成(rule formation)、再解釈(reinterpretation)、演奏的行為(performative acts)という4つの振る舞いを報告している。目標周波数を計算して寸法を決める機能は持たず、情報を載せる発想も現れない。本文全体を検索したが、符号化・情報・秘密・識別子にあたる語はいずれも出てこなかった。

CipherFluteとの関係を述べる。同じ年に同じ「3Dプリントしたフィップル笛」を扱う最新のCHI論文であり、査読者が知っている可能性が高い。しかも本文中で「Printone [53] provides sophisticated resonance modeling, and Acoustic Voxels [29] optimizes resonator geometry via simulation」と、この分野の計算設計研究を明示的に位置づけている。CipherFluteは同じ土俵の上で、教育でも演奏でもなく情報保存を狙う点で区別できる。なお1つの息を複数の管へ分配する連結部が存在することは押さえておくべきである。CipherFluteは笛を1本ずつ順に吹いて読むので構成は異なるが、「1つの物体に複数の発音体を同居させる」という点だけは重なる。

脅威の度合いは「中」である。技術的な主張は重ならないが、直近の関連研究として引用しないと調査不足に見える。特に、この論文が引く計算設計研究(PrintoneとAcoustic Voxels)がCipherFluteの引用一覧と食い違っている点は目立つ。

### 6. Woodwind instrument design optimization based on impedance characteristics with geometric constraints / Full waveform inversion for bore reconstruction of woodwind-like instruments

- 著者: Augustin Ernoult, Christophe Vergez, Samy Missoum, Philippe Guillemain, Michael Jousserand(前者) / Augustin Ernoult, Juliette Chabassier, Samuel Rodriguez, Augustin Humeau(後者)
- 発表: The Journal of the Acoustical Society of America, Vol. 148, No. 5, pp. 2864-2877, 2020年 / Acta Acustica, Vol. 5, 論文番号47, 2021年
- 確認先: https://doi.org/10.1121/10.0002449 (Crossrefで著者5名・巻号・ページ・年を確認), https://doi.org/10.1051/aacus/2021038 (Crossrefで著者4名・巻・論文番号47・年を確認), 実装は https://openwind.inria.fr/ (InriaのMakutuチームによる開発であること、および1次元スペクトル有限要素法または伝達行列法によるインピーダンス計算、時間領域の音の合成、形状最適化、測定インピーダンスからの管形状復元を備えることを公式ページで確認)

内容の要約は次のとおりである。前者は、入力インピーダンスの共鳴周波数と振幅を目的関数に取り、円錐でない管形状や半径と煙突高さの異なる複数の側孔といった幾何的制約のもとで、木管楽器の形状を勾配法で最適化する枠組みを示している。小さな幾何変化でインピーダンスの特徴が大きく変わって勾配法が破綻する問題に対し、共鳴周波数と振幅の新しい定式化を導入している。後者は、測定した音響応答から管の内径分布を復元する完全波形逆解析を提示しており、音の測定から形状を推定する逆問題を扱う。両者の実装はInriaのopenwindとして公開され、インピーダンス計算、時間領域シミュレーション、管形状と側孔位置の最適化、測定インピーダンスからの管形状復元を備える。

CipherFluteとの関係を述べる。順問題(形状から音高)も逆問題(音から形状)も、木管楽器の分野では確立した計算技術である。とくに逆問題の存在は、CipherFluteが脅威モデルで宣言している「形状を計測されれば無音で読める」という主張を裏づけると同時に、「音を録るだけでも形状が推定できる」というより強い攻撃が理論上可能であることを示唆する。

脅威の度合いは「中」である。CipherFluteの符号化の主張は崩れないが、物理層に秘匿性がないという宣言を補強する根拠として引用する価値が高い。また「管長から周波数を求める計算は既存技術である」という位置づけを明確にできる。

### 7. Aerophones in Flatland: Interactive Wave Simulation of Wind Instruments

- 著者: Andrew Allen, Nikunj Raghuvanshi
- 発表: ACM Transactions on Graphics, Vol. 34, No. 4, pp. 1-11, 2015年7月27日(SIGGRAPH 2015)
- 確認先: https://doi.org/10.1145/2767001 (Crossrefで著者2名・巻号・ページ・年・所属Microsoft Researchを確認), https://www.microsoft.com/en-us/research/publication/aerophones-flatland-interactive-wave-simulation-wind-instruments/
- 注意: Crossrefに登録された題名は「Aerophones in flatland」であり、副題は登録されていない。副題を含む完全な題名は上記Microsoft Researchのページで確認した。

内容の要約は次のとおりである。二次元に落とした仮想の管楽器に対して、波動方程式を直接解くことで全帯域の音を実時間合成する手法である。市販のグラフィックスカード上で毎秒128000サンプルの音を合成し、リードや唇のような非線形の励振機構を二次元の波動場に結合できる。指孔の開閉や吹く圧力を利用者の入力で制御し、仮想演奏を実現している。物理製作ではなく音響合成が目的であり、印刷は扱わない。

CipherFluteとの関係を述べる。「管楽器の共鳴を計算機で解く」系譜の代表的な研究であり、Printoneと並べて計算音響の背景として引用できる。CipherFluteが波動シミュレーションを行わず経験式で済ませている選択の位置づけを説明するのに使える。

脅威の度合いは「中」である。情報符号化とは無関係だが、気鳴楽器の計算的取り扱いの代表例として引用しないと網羅性を欠く。

### 8. ProtoHole: Prototyping Interactive 3D Printed Objects Using Holes and Acoustic Sensing / FabAuth: Printed Objects Identification Using Resonant Properties of Their Inner Structures

- 著者: Shohei Katakura, Keita Watanabe(前者) / Yuki Kubo, Kana Eguchi, Ryosuke Aoki, Shigekuni Kondo, Shozo Azuma, Takuya Indo(後者)
- 発表: Extended Abstracts of the 2018 CHI Conference on Human Factors in Computing Systems, pp. 1-6, 2018年 / Extended Abstracts of the 2019 CHI Conference on Human Factors in Computing Systems, pp. 1-6, 2019年
- 確認先: https://doi.org/10.1145/3170427.3188471 (Crossrefで著者2名・掲載巻・ページ・年を確認。Crossrefの題名登録は「ProtoHole」のみで副題を含まない), https://doi.org/10.1145/3290607.3313005 (Crossrefで著者6名・掲載巻・ページ・年を確認。同様に題名登録は「FabAuth」のみ), https://api.semanticscholar.org/graph/v1/paper/DOI:10.1145/3290607.3313005 (FabAuthの副題を含む完全な題名と概要を確認)

内容の要約は次のとおりである。ProtoHoleは3Dプリント物体に穴を設け、音響センシングによって対話を実現するプロトタイピング手法である。ただしProtoHoleの概要はACM Digital LibraryもSemantic Scholarも取得できず、この一文は副題からの読み取りにとどまる。FabAuthについては概要を確認できた。同じ外観の物体でも内部構造を変えることで個体ごとに固有の共鳴特性を与え、物体を透過する振動を用いて、一方のセンサから他方のセンサへ伝わる音波の違いから個体を同定する。予備実験で低充填率の印刷物にも適用でき、平均識別精度は92.2パーセントであったと報告している。いずれも国内の研究者による短報であり、印刷物の内部空洞と音を結びつける点でBlowholeと同じ系譜に属する。

CipherFluteとの関係を述べる。印刷物の内部形状を音で読むという枠組みが共通する。ただしFabAuthは笛としての発音(エッジトーン)を使わず、加振器とセンサを物体に当てて透過振動を測る能動的な方式であり、人が息を吹くだけでは読めない。得られる情報量も個体同定にとどまる。

脅威の度合いは「中」である。国内会議・国際会議のいずれでも査読者が指摘しうる近接研究であり、少なくともFabAuthは「印刷物の内部構造に情報を持たせる」文脈で引用しておくべきである。

### 9. The titanium 3D-printed flute: New prospects of additive manufacturing for musical wind instruments design

- 著者: Anastasia Kolomiets, Yasha J. Grobman, Vladimir V. Popov, Evgeny Strokin, G. Senchikhin, Ezri Tarazi
- 発表: Journal of New Music Research, Vol. 50, No. 1, pp. 1-17, 2020年オンライン公開(2021年の巻号に収載)
- 確認先: https://doi.org/10.1080/09298215.2020.1824240 (Crossrefで著者6名・題名・巻号・ページ・年を確認), https://api.semanticscholar.org/graph/v1/paper/DOI:10.1080/09298215.2020.1824240 (概要の冒頭を確認), https://doi.org/10.1007/s42452-021-04170-x (Damodaranらの総説が参考文献[26]としてこの論文を引用し、造形方式と特徴を要約している)

内容の要約は次のとおりである。概要は「チタン合金の積層造形は医療・航空・宇宙の特注部品に用いられているが、管楽器の分野では試みがなかった。本事例研究はチタン製フルートの設計と3Dプリントに焦点を当てる」と述べている。造形方式は電子ビーム溶融(EBM)である。ここまでは確認できた。

前任の記述には二つの誤りがあったので訂正する。第一に、対象楽器は「リコーダー型の笛」ではなくフルートである。概要と総説の記述はいずれも flute としており、フィップル笛であるとは書かれていない。第二に、「得られた笛の音響的な振る舞いが従来の金属製フルートに近いと報告している」という要約は裏が取れなかった。Taylor & Francisの本文ページは2026年7月30日時点でHTTP 403を返し、本文に到達できていない。総説が要約している範囲では、この研究の特徴として革新的な設計、生体適合性の高さ、著しく豊かな楽音、長い寿命、硬さ、設計変更の容易さ、シロアリに食われないことが挙げられ、さらに外気温や湿度の変化によって音質が影響を受けないと述べられている。「従来の金属製フルートに近い」ではなく「著しく豊かな音」とされている点は、要約の向きが逆である。また「印刷後の後処理や壁の気密性の課題を扱い」という記述も本文未確認である。

CipherFluteとの関係を述べる。CipherFluteは長期保管の観点から樹脂から金属への展開を将来課題に挙げているため、金属積層造形で笛が実際に鳴ることを示したこの研究は、その将来展望の根拠になる。加えて、総説が伝える「外気温や湿度で音質が変わらない」という主張は、CipherFluteが基準笛による較正を導入した理由と正面から関わるので、本文を入手して真意を確かめる価値が高い。

脅威の度合いは「中」である。符号化とは無関係だが、金属化の実現可能性を語るときに引用が必要になる。

### 10. 3D printing of police whistles for STEM education

- 著者: Masato Makino, Kodai Suzuki, Kyuichiro Takamatsu, Atsuki Shiratori, Azusa Saito, Kazuyuki Sakai, Hidemitsu Furukawa
- 発表: Microsystem Technologies, Vol. 24, No. 1, pp. 745-748, 2017年オンライン公開(2018年の巻号に収載)
- 確認先: https://doi.org/10.1007/s00542-017-3393-x (Crossrefで著者7名・題名・巻号・ページ・年を確認), https://doi.org/10.1007/s42452-021-04170-x (Damodaranらの総説の参考文献[21]としてこの論文が引用され、内容が要約されている。以下の要約はその総説の本文で裏を取った)
- 注意: Springerの本文ページはリダイレクト先の認証画面に飛ぶため、本文そのものには到達できていない。以下の内容はDamodaranらの総説による要約に依拠する。

内容の要約は次のとおりである。山形大学のグループが高校生を対象に、3D CADで警笛(いわゆるホイッスル)を設計し、FDM方式で印刷して機能を検証する教育実践を報告している。総説は「さまざまな設計パラメータのうち、笛の半径が周波数に有意に影響した」と述べ、さらに「高校生が笛の中の空気の循環量が周波数にどう効くかを予測できたことは興味深い」と続けている。前任の記述はこの2点をほぼ正確に写しており、訂正の必要はなかった。

CipherFluteとの関係を述べる。3Dプリントした笛の寸法と周波数の関係を扱った、査読つきの数少ない例である。ただし目標周波数への合わせ込みや情報の符号化はなく、教育実践の報告にとどまる。

脅威の度合いは「中」である。CipherFluteの主張を脅かさないが、「印刷した笛の寸法と音高の関係」という最も基本的な部分の先行例として押さえておく必要がある。

### 11. Acoustic Modeling and Optimization of the Xiao / Acoustics of the xiao: a case study of modern methods for the design of woodwind instruments

- 著者: Y. Lan, C. E. Waltham(前者。Crossrefの登録がイニシャル表記であるため、名を勝手に展開せずそのまま記す) / Yang Lan(後者。DataCiteに「Lan, Yang」と登録されている)
- 発表: Acta Acustica united with Acustica, Vol. 102, No. 6, pp. 1128-1137, 2016年 / ブリティッシュコロンビア大学 博士論文, 2015年
- 確認先: https://doi.org/10.3813/aaa.919024 (Crossrefで著者2名・題名・巻号・ページ・年を確認), https://doi.org/10.14288/1.0167080 (DataCiteで著者名Lan, Yang・題名・大学名・年・概要を確認。ハンドルは 2429/51768)
- この2件は、前任の調査では「未検証のまま残ったもの」に置かれていた。今回の検証で両方とも実在を確認し、あわせて査読誌の論文の存在も新たに見つけたので、この節に移した。前任の記述にあった著者名「Yuan Lan」は誤りである。正しくは Yang Lan である。Dabinらの参考文献[13]が「Y. Lan」と略記していたため、名を取り違えたものと推測される。

内容の要約は次のとおりである。博士論文の概要は次のように述べる。尺八の近縁にあたる中国の縦笛「簫」は千年を超える歴史を持ちながら、竹の形状が一定しないために標準化や現代的な要求への適応が進んでおらず、調律、音域、音の安定性、高音の演奏性に不備がある。音響学の立場ではこれらの不備はすべて音響インピーダンスによって特徴づけられる。設計手法については、Dabinらが本文中で「伝達行列法は中国の簫(笛)の特性のモデル化にも使われている」と述べて参考文献[13]、すなわちこの博士論文を引用しており、伝達行列法にもとづく設計であることは外部の記述で裏が取れる。査読誌版は題名のとおり簫のインピーダンスのモデル化と最適化を扱うが、概要が公開されていないため中身は未確認である。

CipherFluteとの関係を述べる。CipherFluteの近似式 f = A/(L+e) は一次元の経験モデルであり、簫の研究が用いる伝達行列法は同じ一次元の枠組みのなかで管の断面変化と側孔を厳密に扱うものである。すなわちCipherFluteの管長と周波数の対応づけは、この系譜の最も単純な特別な場合にあたる。しかも簫は縦笛であってCipherFluteに形が近い。

脅威の度合いは「中」である。CipherFluteの符号化の主張は崩れないが、「管長から周波数を予測する一次元モデル」の先行研究として、Printoneの境界要素法よりむしろ近い位置にある。設計計算の新規性を主張しないことを明示する材料として引用するのが安全である。

### 12. Walrus Pipes and Waving Panpipes: 3D printed instrument designs for speculative community music

- 著者: Bálint Szabó
- 発表: Jazz Research Journal, Vol. 17, No. 1-2, pp. 193-222, 2024年11月28日
- 確認先: https://doi.org/10.1558/jazz.28243 (Crossrefで著者・題名・副題・掲載誌・巻号・ページ・年・概要を確認)
- この文献は、前任の調査では掲載誌のページがHTTP 402を返したため「未検証のまま残ったもの」に置かれていた。今回、CrossrefのAPIで書誌情報と概要を完全に取得できたので、この節に移した。なお掲載誌の記事ページ https://journal.equinoxpub.com/JAZZ/article/view/28243 は2026年7月30日時点でHTTP 403を返す。

内容の要約は次のとおりである。概要は、大量生産された西洋の楽器が名人の技巧に奉仕し単一の標準的な調律しか鳴らさないのに対し、この3Dプリント管楽器の企画はその対位法をなすと述べる。作られる楽器は単純で特注であり、合奏として共同で吹くことに奉仕する。論文は企画で開発された2つの3Dプリント管楽器の合奏体、すなわち Walrus Pipes と Waving Panpipes の設計過程の全体を明かす。パンフルートは複数の管を1つの物体に並べた楽器である。

CipherFluteとの関係を述べる。「複数の共鳴管を1つの3Dプリント物体にまとめる」という構成の、査読つきの先行例である。ただし目的は共同での音楽演奏であり、音高の並びを符号語として読む発想はない。CipherFluteが「多数の単音笛を融合する」構成そのものは前例がないと主張するなら、パンフルート型の印刷楽器がすでに査読文献にあることを認めた上で、符号として読む点に絞って差分を述べる必要がある。

脅威の度合いは「中」である。技術的な主張は重ならないが、「複数の共鳴管を1つの印刷物にまとめた前例はない」と書いてしまうと即座に反証されるため、引用して差分を述べる必要がある。なお概要までは確認したが本文は未読であり、管の数や調律の決め方は確かめていない。

## 背景として押さえるべき文献

以下は脅威の度合いが「低」であり、背景として引用する程度でよいものである。

- Amit Zoran, "The 3D Printed Flute: Digital Fabrication and Design of Musical Instruments", Journal of New Music Research, Vol. 40, No. 4, pp. 379-387, 2011年。https://doi.org/10.1080/09298215.2011.621541 (Crossrefで著者・題名・巻号・ページ・年を確認)。FDM方式(ABS)とPolyJet方式でコンサートフルートの複製を作った先駆的な事例である。前任の記述は「本文を通読した」としていたが、今回の検証ではTaylor & Francisの本文ページがHTTP 403を返し、Crossrefにも概要が登録されておらず、本文には到達できなかった。したがって「計算による音響設計は行っておらず、セント単位の音高精度の測定も報告していない」という主張は本文で裏を取れていない。ただしDabinら(NIME 2016)がこの論文を引用して「Zoranは3Dプリントでコンサートフルートの複製を作れることを示したが、壁の水密性と材料の劣化に問題があり、楽器として使えるものにはならなかった」と述べており、造形の限界に関する部分は外部の記述で裏が取れる。この点はCipherFluteが薄壁で苦労した経験と対応する。
- Nicholas J. Bailey, Théo Cremel, Alexander South, "Using Acoustic Modelling to Design and Print a Microtonal Clarinet", Proceedings of the 9th International Conference on Interdisciplinary Musicology (CIM14), ベルリン, 2014年12月4日から6日。https://eprints.gla.ac.uk/124083/ (グラスゴー大学の機関リポジトリで著者3名・題名・会議名・開催地・会期を確認)。前任の記述は会議名を「9th Conference on Interdisciplinary Musicology」としていたが、正式には「9th International Conference on Interdisciplinary Musicology」であり、International が抜けていたので補った。C++でオブジェクト指向の音響モデルを作り、OpenSCADで楽器形状を記述して19平均律のクラリネットを印刷し、プロ奏者が評価しているという内容の要約は、本文未取得のため裏が取れていない。
- Christian Ritz, Matthew Dabin, Terumi Narushima, Kraig Grady, Stephen Beirne, "3D printing for custom design and manufacture of microtonal flutes", SPIE Newsroom, 2015年。https://doi.org/10.1117/2.1201508.006082 (Crossrefで著者5名・題名・掲載媒体・年を確認。巻号とページは登録されていない)。上記NIME 2016論文の一般向け短報である。
- Openwind(Inria Makutuチーム)。https://openwind.inria.fr/ (公式ページでチーム名と機能一覧を確認)。管楽器のインピーダンス計算(1次元スペクトル有限要素法または伝達行列法)、リードや唇を管口に結合した時間領域の音の合成、管形状と側孔位置の最適化、測定インピーダンスからの管形状復元をまとめたPythonライブラリである。
- Dingzeyu Li, David I. W. Levin, Wojciech Matusik, Changxi Zheng, "Acoustic Voxels: Computational Optimization of Modular Acoustic Filters", ACM Transactions on Graphics, Vol. 35, No. 4, pp. 1-12, 2016年。https://doi.org/10.1145/2897824.2925960 。すでに現行論文が引用している。共鳴体を組み合わせて伝達関数を設計する研究であり、気鳴楽器の計算設計の隣接領域として位置づけられる。
- Gaurav Bharaj, David I. W. Levin, James Tompkin, Yun Fei, Hanspeter Pfister, Wojciech Matusik, Changxi Zheng, "Computational Design of Metallophone Contact Sounds", ACM Transactions on Graphics, Vol. 34, No. 6, pp. 1-13, 2015年。https://doi.org/10.1145/2816795.2818108 。打楽器(体鳴楽器)の形状を目標周波数と振幅に合わせて最適化する研究である。気鳴ではないが「目標音高に合わせる形状最適化」の代表例である。
- Soizic Terrien, Christophe Vergez, Benoît Fabre, "Flute-like musical instruments: A toy model investigated through numerical continuation", Journal of Sound and Vibration, Vol. 332, No. 15, pp. 3833-3848, 2013年。https://doi.org/10.1016/j.jsv.2013.01.041 。フルート型楽器の発振を数値接続法で解析する物理モデル研究である。
- Péter Rucz, Fülöp Augusztinovicz, Judit Angster, Tim Preukschat, András Miklós, "Acoustic behavior of tuning slots of labial organ pipes", The Journal of the Acoustical Society of America, Vol. 135, No. 5, pp. 3056-3065, 2014年。https://doi.org/10.1121/1.4869679 。同じ著者らによる有限要素モデルの続報が The Journal of the Acoustical Society of America, Vol. 137, No. 3, pp. 1226-1237, 2015年(https://doi.org/10.1121/1.4913460)にある。製造後の調律を目的とした調律スロットの音響を扱っており、印刷後の調律を論じるときの理論的背景になる。
- Taizo Kobayashi, Toshiya Takami, Masataka Miyamoto, Kin'ya Takahashi, Akira Nishida, Mutsumi Aoyagi, "3D Calculation with Compressible LES for Sound Vibration of Ocarina", arXiv:0911.3567, 2009年11月18日投稿。https://arxiv.org/abs/0911.3567 (arXivで著者6名・題名・投稿日・概要を確認)。オカリナをエッジトーンとヘルムホルツ共鳴器の結合系とみなし、圧縮性大渦解法で二次元および三次元の数値解析を行っている。arXivの注記によれば全8ページで、Open Source CFD International Conference 2009 で発表されたものである。
- Sho Iwagami, Ryoya Tabata, Taizo Kobayashi, Yuji Hattori, Kin'ya Takahashi, "Numerical study on edge tone with compressible direct numerical simulation: Sound intensity and jet motion", International Journal of Aeroacoustics, Vol. 20, No. 3-4, pp. 283-316, 2021年。https://doi.org/10.1177/1475472X211003296 (Crossrefで著者5名・題名・巻号・ページ・年を確認)。フィップル笛の発音の中核であるエッジトーンの直接数値計算である。
- Shengze Zhong, Parinya Punpongsanon, Daisuke Iwai, Kosuke Sato, "Estimation of fused-filament-fabrication structural vibro-acoustic performance by modal impact sound", Computers & Graphics, Vol. 115, pp. 137-147, 2023年。https://doi.org/10.1016/j.cag.2023.07.010 (Crossrefで著者4名・題名・巻・ページ・年を確認。前任の記述に欠けていた第115巻を補った)。FDM印刷物の振動音響特性を打音から推定する研究であり、印刷物と音の関係を扱う近年の例である。
- Ajith Damodaran, M. Sugavaneswaran, Larry Lessard, "An overview of additive manufacturing technologies for musical wind instruments", SN Applied Sciences, Vol. 3, No. 2, 論文番号162, 2021年1月20日。https://doi.org/10.1007/s42452-021-04170-x (Crossrefで著者3名・題名・巻号・論文番号・年を確認。オープンアクセスの本文PDFを取得して全文を検索した)。管楽器の積層造形に関する体系的総説である。全文検索により、音高精度をセント単位で示した記述はないこと、Printone(参考文献[35])、Dabinら(同[36])、Ritzら(同[37])、Makinoらの警笛(同[21])、Zoran(同[20])、Avanziniら(同[38])、Kolomietsらのチタン製フルート(同[26])をいずれも紹介していることを確認した。前任の要約は正確であった。
- Antreas Kantaros, Olaf Diegel, "3D printing technology in musical instrument research: reviewing the potential", Rapid Prototyping Journal, Vol. 24, No. 9, pp. 1511-1523, 2018年。https://doi.org/10.1108/RPJ-05-2017-0095 (Crossrefで著者2名・題名・巻号・ページ・年・概要を確認)。概要によれば、楽器への積層造形の応用史を文献調査でたどり、従来の製法では作れない全く新しい管楽器を作れるかを問うものである。既存楽器の意匠を独自にする用途では広く使われているが、まったく新しい音を作る本来の潜在力はほとんど未開拓であると結論している。
- Robert Howe, Sina Shahbazmohamadi, Richard Bass, Prabhjot Singh, "Digital evaluation and replication of period wind instruments: the role of micro-computed tomography and additive manufacturing", Early Music, Vol. 42, No. 4, pp. 529-536, 2014年。https://doi.org/10.1093/em/cau091 (Crossrefで著者4名・題名・巻・号・ページ・年を確認。前任の記述に欠けていた第4号を補った)。歴史的管楽器をマイクロX線CTで計測して積層造形で複製する研究である。CipherFluteの脅威モデル(形状の計測による無音の読み出し)に対して、CTで内部形状を取れることを示す実例として引用できる。
- Javier Esclapés, Almudena Gómez, Ana Ibañez, "Flow. A Socially Responsible 3D Printed One-Handed Recorder", International Journal of Environmental Research and Public Health, Vol. 18, No. 22, 12200, 2021年。https://doi.org/10.3390/ijerph182212200 (Crossrefで著者3名・題名・巻号・論文番号・年・概要を確認)。片手だけが使える児童のために安価な片手用リコーダーを作る設計事例である。造形方式は光造形(ステレオリソグラフィ)であり、20名の小学生に対して補助機器の心理社会的影響尺度(PIADS)による評価を行っている。
- Lior Arbel, François Gautier, "LeMo: an assembly kit for musical acoustics education", Journal of New Music Research, Vol. 51, No. 2-3, pp. 106-120, 2022年。https://doi.org/10.1080/09298215.2022.2150651 (Crossrefで著者2名・題名・巻号・ページ・年を確認。概要はSemantic Scholarで確認)。概要は楽器を振動の生成・共鳴・放射という基本的な音響的性質で分類し、共鳴部と放射部の独立したモジュールから成る組み立てキットを述べるとしている。前任の「励振部・共鳴部・放射部に分解する」という要約は正確である。FlueBricksが「LeMoの概念を拡張する」と明記しているので、直接の下敷きであることも確認できた。
- Federico Avanzini, Adriano Baratè, Luca A. Ludovico, "3D printing in preschool music education: Opportunities and challenges", Qwerty - Open and Interdisciplinary Journal of Technology, Culture and Education, Vol. 14, No. 1, pp. 71-92, 2019年。https://doi.org/10.30557/qw000012 (Crossrefで著者3名・題名・掲載誌・巻号・年を確認。ページ範囲はDamodaranらの総説の参考文献[38]の記載で補った)。
- Francesco Di Maggio, Catharina Maria van Riet, Sergio Picella, Berry Eggen, Bart Hengeveld, "The Aerophone Kit: A Toolkit for Pneumatic Musical Instrument Design", Proceedings of the International Conference on New Interfaces for Musical Expression (NIME '26), 6月24日から27日, ロンドン, 2026年。https://nime.org/proceedings/2026/nime2026_80.pdf (本文PDFを取得し、著者5名の氏名と所属アイントホーフェン工科大学、会議名、会期、開催地、概要を確認)。空気圧回路と流体論理だけで動き、電子部品もデジタル部品も使わない楽器の設計キットである。発音はチューブ形状と弁の特性で調律される笛モジュールが担い、2オクターブすなわち24半音にわたる。前任の記述にあった「電源を使わない点で発想は近い」は不正確なので訂正する。電子的・デジタル的な制御を使わないのであって、正圧を供給するポンプは用いており、電源が不要な機構ではない。音高の計算設計も情報符号化も扱わないという点は本文検索で確認した。
- 有元慶太, 「エアリード楽器のフルー形状と発音特性に関する実験的考察」, 音楽音響研究会資料, 第44巻第8号, pp. 59-61, 2026年2月15日。https://cir.nii.ac.jp/crid/1520026358358670592 (CiNii Researchの機械可読レコードで著者名・題名・掲載誌名・巻・号・ページ・発行日を確認)。フルー(風道)の形状と発音特性の関係を実験的に調べており、CipherFluteの吹き口設計の背景として日本語圏で最も近い最新の研究である。
- 小島正典, 「リコーダーの右手運指を持つケーナの構造と音程」, 音楽音響研究会資料, 第41巻第3号, pp. 1-4, 2022年6月18日。https://cir.nii.ac.jp/crid/1520294740085074432 (CiNii Researchの機械可読レコードで著者名・題名・巻・号・ページ・発行日を確認。前任の記述に欠けていた巻号とページを補った)。管の構造と音程の関係を扱う国内研究である。
- 山田真司, 「オカリナ音に含まれる周波数 振幅ゆらぎとオカリナ音らしさとの関係」, 音楽音響研究会資料, pp. 21-26, 1993年。https://cir.nii.ac.jp/crid/1573668924031425920 (CiNii Researchの機械可読レコードで著者名・題名・掲載誌名・ページ・年を確認。巻号はレコードに登録がない)。国内のオカリナ音響研究として存在を確認した。
- Hiroaki Okada, Sho Iwagami, Taizo Kobayashi, Kinya Takahashi, "Numerical Simulation of Aerodynamics Sound in an Ocarina Model", Proceedings of the International Symposium on Music Acoustics (ISMA 2019), 9月13日から17日, デトモルト, pp. 263-268, 2019年, ISBN 978-3-939296-16-4。http://pub.dega-akustik.de/ISMA2019/data/articles/000010.pdf (予稿集の著者索引で著者4名と題名を確認し、本文PDFを取得して各ページ下部の頁番号263から268を確認)。前任の調査では予稿集ページに到達できず未検証とされていたが、今回ISMA 2019の公式サイトが案内する予稿集の所在(http://pub.dega-akustik.de/ISMA2019)から到達できた。オカリナの胴をヘルムホルツ共鳴器とみなし、圧縮性大渦解法で1億5千万格子を超える三次元モデルを解いている。
- Michael Prairie, "Understanding the Acoustics of the Native American-Style Flute", 2006年10月4日, 全62ページ, 自主公開の文書。http://www.flutopedia.com/refs/Prairie_2006_UnderstandingAcousticsOfTheNAF.pdf (Flutopediaの参考文献一覧 http://www.flutopedia.com/references_p.htm で題名・著者・日付・分量を確認し、PDFの存在も確認した)。前任の調査では査読の有無を含めて確認できないとされていたが、Flutopediaの記載と文書自身の序文により、査読誌の論文ではなく著者が随時更新する自主公開の文書であることが判明した。学術的な先行性の主張には使えない。
- Voichita Bucur, "Digital Fabrication of Some Wind Instruments", Handbook of Materials for Wind Musical Instruments 所収, Springer, 第16章, pp. 593-613, 2019年。https://doi.org/10.1007/978-3-030-19175-7_16 (Crossrefで著者・章題・書名・章番号・ページ・年を確認)。前任の調査ではページを593-612としていたが、正しくは593-613である。章の本文は未読である。
- Paul Hoekje, "A brief summary of A. H. Benade's wind instrument adjustment principles", Catgut Acoustical Society Journal (CASJ), Vol. 2, No. 7, pp. 16-24, 1995年5月。https://purl.stanford.edu/zk714gv4615 (スタンフォード大学デジタルリポジトリで当該号「CAS journal. Volume 2, number 7, 1995-05」の実在、出版者Catgut Acoustical Society、ISSN 1053-7694を確認)。Dabinらが吹き口の管端補正の出典として挙げている。前任の記述は誌名を「Journal of the Catgut Acoustical Society」としていたが、正式には「Catgut Acoustical Society Journal」である。掲載号の実在は確認したが、記事本体は走査画像の閲覧器の中にあり読めていないため、題名とページはDabinらの参考文献[11]の記載に依拠する。

## 未検証のまま残ったもの

前任の調査が挙げていた7件のうち6件は、今回の検証で書誌情報を確定できたので、それぞれ本文の該当する節に移した。移した先は次のとおりである。Walrus PipesとWaving Panpipesは「新規性への脅威が大きい文献」の12番、Lanの博士論文は同11番、Okadaらのオカリナ論文とHoekjeの要約とPrairieの文書とBucurの章は「背景として押さえるべき文献」の末尾である。以下に残るのは、書誌情報は確定したが本文または一部の主張に到達できなかったものである。いずれも「書誌情報は引用してよいが、内容の要約を書くには本文の入手が必要」という状態にある。

1. Blowhole(Tejadaら, Graphics Interface 2018)の本文。予稿集ページはCloudflareのボット判定で、ACM Digital Libraryのページも権限不足で、いずれもHTTP 403を返した。識別クラス数が9個であること、正解率が98パーセントから90パーセントへ落ちること、SLA印刷のほうがヘルムホルツ式の予測に近いことなど、前任が書いた数値はすべて未検証である。CipherFluteの最重要の比較対象であるから、大学図書館経由などで本文を確実に入手すべきである。
2. ProtoHole(Katakura, Watanabe, CHI EA 2018)の概要。ACM Digital LibraryもSemantic Scholarも概要を出さなかった。書誌情報は確定したが、内容の要約は副題からの読み取りにとどまる。
3. Zoran(2011年)の本文。Taylor & FrancisがHTTP 403を返し、Crossrefにも概要の登録がない。「計算による音響設計を行っていない」「セント単位の音高精度を報告していない」という前任の主張は本文で裏が取れていない。
4. Kolomietsら(2020年)のチタン製フルートの本文。同じくTaylor & FrancisがHTTP 403を返した。造形方式がEBMであることと概要の冒頭までは確認したが、後処理や気密性の議論、および音響的な振る舞いの評価は未確認である。
5. Makinoら(2017年)の警笛の本文。Springerが認証画面に飛ばすため到達できていない。内容の要約はDamodaranらの総説による二次的な記述に依拠している。
6. PrintoneのACM Transactions on Graphics版の本文。シミュレーション誤差の定量値(セント換算やパーセント表記)を取れていない。ISMA 2017の短縮版で確認できた「56個の目標周波数のうち53個が実測範囲に入った」という記述までにとどまる。
7. Hoekjeの要約記事(1995年)の本文。掲載号がスタンフォード大学デジタルリポジトリに存在することは確認したが、記事本体は走査画像の閲覧器の中にあり読めていない。題名とページはDabinらの参考文献の記載に依拠する。
8. Bucurの章(2019年)の本文。書誌情報はCrossrefで確定したが、章の中身は未読である。
9. Demakeinの音響モデルの詳細。公式ページとGitHubのREADMEはいずれも設計計算の中身を明示せず、実装コードまで読み込めていない。前任が書いた「枝分かれした管の共鳴周波数を求める」という記述も、公式の文書には対応する記載が見つからなかった。CipherFluteの f = A/(L+e) との関係を厳密に述べるには追加調査が必要である。
10. Bailey, Cremel, South(CIM14)の本文。機関リポジトリの書誌記録は確認したが、本文PDFの内容は確認していない。C++の音響モデルとOpenSCADによる19平均律クラリネットという要約は未検証である。
11. Szabó(2024年)のWalrus PipesとWaving Panpipesの本文。概要までは取得したが、管の本数や調律の決め方は確認していない。

## 検証で削除したもの

削除した文献は1件もない。前任の調査が挙げた文献と事例は、書誌情報の水準ではすべて実在を確認できた。存在しないものを捏造した箇所は見つからなかった。訂正はいずれも、著者名の綴り、会議名の正式表記、公開年、巻号やページの欠落や誤り、内容の要約の行き過ぎ、という種類のものである。

## この切り口で見つからなかったこと

以下は、検索と文献追跡を尽くしたうえで「見つからなかった」と言えることであり、CipherFluteの新規性の主張の根拠になる。

1. 印刷した笛の音高を離散的な符号(スロット)として読み、複数本の音高の並びで数十ビットから百数十ビットの情報を運ぶ研究は見つからなかった。Blowholeは1つの空洞が1つの識別子を表すだけである(ただし識別クラス数の具体的な値は本文未取得のため確認できていない)。パンフルート状に複数の管を並べる工作物は多数あり、査読文献としてもSzabó(2024年)の3Dプリントのパンフルート合奏体が実在するが、それらは音楽を奏でるためのものであって、音高の系列を符号語として扱う設計は査読文献にも非査読の設計物にも見当たらなかった。

2. 基準となる音高が既知の笛を同じ物体に同居させ、他の笛を基準笛との比で読むことで気温や息の強さによる全体のずれを打ち消すという設計は、印刷楽器の文献に見つからなかった。楽器音響には基準ピッチや調律スロットの議論があり、Dabinらは吹く息による音高変動を「奏者の影響」として受け入れ、Printoneは吹く速さによる周波数の幅を実測範囲として示すにとどまる。物体の中に較正用の音源を混ぜて相対量で読むという発想は、通信のパイロット信号からの転用としてCipherFlute固有と言える。

3. 隣り合う笛が同じ音にならない制約(遷移保証)や、Reed-Solomon符号のような誤り訂正を、印刷楽器の形状設計に持ち込んだ例は見つからなかった。印刷楽器の文献における誤差対策は、より精細な造形方式への変更、やすりによる手修正、奏法による補正のいずれかであり、符号レベルの対策は現れない。

4. 円筒を軸方向に半分に割った断面(厚さ4ミリメートル、幅7ミリメートル)の小型フィップル笛を、サポート材なしで平置き印刷し、多数本を融合して1つの日用品に埋め込むという構成は、査読文献に見つからなかった。Printoneは1つの物体を1つの楽器にし、FlueBricksはモジュールを組み替え、Dabinらは管を1本ずつ作る。ただし「多数の管を1つの印刷物にまとめる」ことそのものには前例があるので、ここは注意して書く必要がある。Szabó(2024年)は3Dプリントのパンフルート合奏体を査読誌で報告しており、FlueBricksは1つの息を複数の管へ分配する連結部を備えている。CipherFlute固有と言えるのは、融合そのものではなく、単音笛を情報担体として日用品に偽装して埋め込む点である。

5. 3Dプリントした笛の音高精度をセント単位で系統的に報告した査読文献は、Dabinら(2016年)がほぼ唯一である。しかもそれはPolyJet方式という高精細な装置での結果であり、家庭用のFDM方式で多数本の笛の音高分布を測った報告は見つからなかった。CipherFluteが家庭用FDM機で実測する評価は、この意味で空白を埋める。

6. 日本語圏では、3Dプリント笛の計算設計を扱う研究が見つからなかった。この主張は今回あらためてCiNii ResearchのOpenSearch APIで検証した。2026年7月30日時点で「3Dプリンタ 笛」は0件、「3Dプリント 笛」は0件、「3Dプリンタ オカリナ」は0件、「3Dプリント リコーダー」は0件である。「3Dプリンタ 楽器」は10件出るが、上位はデジタル技術による木管楽器奏者の口腔問題対策、樹脂3Dプリンタ製の双腕協働ロボットによる音符型電子楽器の演奏、産業用ヒューマノイドロボットによる同様の操り動作など、ロボット演奏と口腔装置の研究であり、前任の記述どおりであった。「オカリナ」「気鳴楽器」「エアリード楽器」「リコーダー 音響」ではエアリード楽器の物理と数値流体力学の研究群(安藤由典、吉川茂、足立整治、高橋公也らの系譜)が並ぶが、いずれも印刷や情報符号化とは結びついていない。情報処理学会の音楽情報科学研究会およびWISSの予稿集にも該当する研究は見当たらなかった。

7. 印刷後に音高を測って符号を確定する、あるいは印刷誤差を測定して設計にフィードバックする「印刷後調律」の計算的枠組みは、笛については見つからなかった。オルガンのフルー管の調律スロットに関する音響研究(Ruczら)は存在するが、印刷とは結びついていない。

## 調べ残した穴

1. Printoneの本体であるACM Transactions on Graphics版のPDFに到達できず、シミュレーション誤差の定量値(セント換算やパーセント表記)を取れていない。ISMA 2017の短縮版で確認できた「56個の目標周波数のうち53個が実測範囲に入った」という記述までにとどまる。大学図書館経由などで本文を入手し、精度の表を確認すべきである。

2. ACM Symposium on Computational Fabrication(SCF)の全年次のプログラムを網羅的には見ていない。音響を扱うSCF論文が他にないかを、2017年から2026年までの目次で確認する価値がある。

3. 音響系の会議(ISMA、Forum Acusticum、Stockholm Musical Acoustics Conference、日本音響学会の音楽音響研究会)の各年次プログラムを個別に当たり切れていない。ISMA 2019については今回、公式サイト(http://www.isma2019.de/)から予稿集(http://pub.dega-akustik.de/ISMA2019)に到達し、著者索引を通してオカリナと管楽器の数値解析の論文群があることを確認した。ISMA 2023以降は依然として未確認である。

4. 特許を体系的には調べていない。ただし前任が「検索結果に現れる」とだけ書いていた特許について、今回は実在と識別番号を確認した。米国特許 US 6,348,647 B1 「Fipple flutes having improved airways」は発明者Karl P. Ahrens、優先日2000年3月31日、公告日2002年2月19日である。日本の公開特許公報 特開平7-64562 「Multiple-tone whistle(多音笛)」は出願人Seron Manufacturing Co.、優先日1993年8月12日、公開日1995年3月10日である。いずれもGoogle Patents(https://patents.google.com/patent/US6348647B1/en , https://patents.google.com/patent/JPH0764562A/en)で確認した。すなわち複数の音を出す笛は少なくとも1993年から特許として存在する。音で情報を読み取る玩具の特許は未調査である。

5. 中国語圏および韓国語圏の文献を調べていない。オカリナや尺八型縦笛の設計研究がある可能性がある。

6. ThingiverseやPrintables、MakerWorldなどに投稿された非査読の設計物を網羅していない。「Whistle Pan flute」のように複数の笛を並べた作品が実在するため、先行「作品」としての言及が必要になる場合は、代表例を選んで出典を明示する準備が要る。

7. Demakeinの最適化アルゴリズムの中身と、CipherFluteの経験式との数理的な関係を確かめていない。実装コードを読めば、両者の設計問題の包含関係を明確に書ける。

## 検証の記録

2026年7月30日に、この切り口の文献一覧を最初に書いた担当者とは別の担当者が、書誌情報の実在をすべて独立に検証し直した。以下がその記録である。

検証の対象は、検証前のこのファイルに挙げられていた書誌情報を伴う項目のすべてであり、重複を除いて41件であった。内訳は「新規性への脅威が大きい文献」の節に14件(全10項のうち第1項はACM Transactions on Graphics版とISMA 2017短縮版の2件、第6項と第8項もそれぞれ2件の文献を束ねているため、項の数より文献の数が多い)、「背景として押さえるべき文献」の節に22件(全21項のうちRuczらの項が2件を束ねている)、「未検証のまま残ったもの」の節に文献6件である。openwindは脅威の節と背景の節の両方に現れるため、重複を除いて1件と数えた。加えて、本文中の文献以外の主張として、CiNii Researchの検索結果の件数と、特許の存在についても検証した。

検証の方法は次のとおりである。DOIを持つ文献は、doi.orgに対してコンテンツネゴシエーション(Accept: application/vnd.citationstyles.csl+json)を行い、Crossrefに登録された著者名・題名・掲載誌名・巻号・ページ・年・出版者を直接取り出して照合した。DOIを持たない文献は、学会の予稿集ページ、著者や研究所の公式ページ、DBLP、DataCite、OpenAIRE、Semantic Scholar、CiNii Researchの機械可読レコード、スタンフォード大学デジタルリポジトリ、Google Patentsのいずれかに当たった。数値や事実の主張については、可能な範囲で原典のPDFを取得して本文で裏を取った。実際に本文を取得して精読したのは、PrintoneのISMA 2017短縮版、DabinらのNIME 2016論文、FlueBricksのarXiv版、Damodaranらの総説、OkadaらのISMA 2019論文、Di MaggioらのNIME 2026論文の6件である。

その結果、書誌情報の水準で実在を確認できなかった文献は1件もなかった。存在しない文献を捏造した箇所は見つからなかった。削除した項目も1件もない。

訂正は合わせて21件行った。うち書誌情報そのものの誤りの訂正と欠落の補完が12件である。第一に、Demakeinの公開年を2014年から2012年に直した。PyPIの全リリース履歴により、最初の版0.1の公開が2012年9月28日であることを確認した。2014年という数字は、Dabinらの参考文献が付記した参照年に由来すると考えられる。第二に、Lanの博士論文の著者名を「Yuan Lan」から「Yang Lan」に直した。DataCiteの登録が「Lan, Yang」である。第三に、CIM14の会議名に抜けていた「International」を補い、正式には「9th International Conference on Interdisciplinary Musicology」であることを示した。第四に、Hoekjeの掲載誌名を「Journal of the Catgut Acoustical Society」から正式表記の「Catgut Acoustical Society Journal」に直した。第五に、Bucurの章のページを593-612から593-613に直した。第六に、Blowholeの発表媒体を「Proceedings of Graphics Interface 2018」から、DBLPが記録する正式名称の「Proceedings of the 44th Graphics Interface Conference」に改め、開催地と会期も補った。第七から第十二として、Zhongらの第115巻、Howeらの第4号、小島の第41巻第3号とページ1-4、山田のページ21-26、Avanziniらの第14巻第1号とページ71-92、PrintoneのACM Transactions on Graphics版の論文番号184(pp. 184:1-184:14)を、それぞれ補った。

残る9件は内容の要約の訂正である。第一に、FlueBricksが挙げる6つの内部形状の一覧から「調律スロット」を除き、原文どおりの6つ(フルー管路、空気室、風道、窓、分割エッジ、発音室)に置き換えた。調律スロットは共鳴部の側の別モジュールであり、生成部の内部形状ではない。第二に、Kolomietsらのチタン製の楽器を「リコーダー型の笛」からフルートに直した。第三に、同じ研究の造形方式を電子ビーム溶融と明記した。第四に、同じ研究について「音響的な振る舞いが従来の金属製フルートに近い」という要約が裏を取れず、総説の伝えるところでは「著しく豊かな楽音」と要約の向きが逆であることを注記した。第五に、Di Maggioらの空気圧楽器キットについて「電源を使わない」という記述を、電子部品とデジタル制御を使わないがポンプで送気する構成である旨に直した。第六に、Blowholeについて、前任が書いた識別クラス数9個、正解率98パーセントから90パーセント、SLA印刷が予測に約100ヘルツ近いといった数値が、予稿集ページとACM Digital Libraryのいずれもボット判定と権限不足でHTTP 403を返したために裏を取れなかった旨を明記し、「9クラスで約3.2ビット」という容量の対比も未検証であると断った。CipherFluteの最重要の比較対象であるから、これらの数値を論文に書く前に本文を確実に入手すべきである。第七に、ZoranとKolomietsとMakinoについて、前任が「本文を通読した」と書いていたものを、実際に到達できた資料の範囲に合わせて書き換えた。第八に、Demakeinの音響モデルが「枝分かれした管の共鳴周波数を求める形で組まれている」という記述に、公式の文書に対応する記載がないことを注記した。第九に、DabinらのFDM機での失敗の記述を原文に合わせて精密にした。原文は、ラビウムの望む鋭さが出ないことと、ボア内壁の粗さのために奏者がより高い吹圧を要し、安定した音を立ち上げるまでに市販品より長い時間がかかったことを述べており、「発音が不安定になった」という要約より具体的である。

一方で、確かめた結果として前任の記述が正確であった箇所も多い。Printoneの「56個の目標周波数のうち53個が実測範囲に入った」と「16本の楽器」はISMA 2017版の原文どおりであった。Dabinらのセント値(リコーダー1が+6から+34、リコーダー2が−40から+1、手修正版が−13から+14)と5セント以内という将来目標は、原論文の表1と本文で一字一句合っていた。Damodaranらの総説に音高精度のセント表記がないことと、Printone・Dabinら・Makinoらを紹介していることも全文検索で確認した。Makinoらの警笛について「笛の半径が周波数に大きく効く」「空気の循環量の効果を高校生が予測できた」という要約も、総説の記述と一致していた。CiNii Researchで「3Dプリンタ 笛」が0件であることも再現した。

さらに、前任が「未検証のまま残ったもの」に置いていた7件のうち6件を確定させ、本文の該当する節に移した。Szabóの3Dプリントのパンフルート合奏体(Jazz Research Journal, 2024年)、Lanの博士論文(2015年)、OkadaらのISMA 2019論文、Hoekjeの掲載号、Prairieの自主公開文書、Bucurの章である。この過程で、前任が見落としていた査読誌の論文を1件新たに見つけた。Lan と Waltham による「Acoustic Modeling and Optimization of the Xiao」(Acta Acustica united with Acustica, 第102巻第6号, pp. 1128-1137, 2016年)である。伝達行列法で縦笛を設計する研究であり、CipherFluteの一次元の経験式に最も近い位置にあるので、脅威の度合いを「中」として本文に追加した。あわせて、前任が「検索結果に現れる」とだけ書いていた特許2件について、米国特許US 6,348,647 B1と日本の特開平7-64562という具体的な識別番号、発明者、出願人、日付を確定させた。

残る不確かさは、末尾の「未検証のまま残ったもの」に11項目として整理した。要するに書誌情報はすべて信頼して引用できる状態になったが、内容の数値を論文に書くには、Blowhole、Zoran、Kolomiets、Makino、PrintoneのTOG版の5件について本文の入手がまだ必要である。
