# 受動的な音響タグと音で読む物体

本稿は CipherFlute（電源を持たない3Dプリント笛を日用品に埋め込み、吹いた音の高さを符号として秘密情報を読み出す手法）の新規性を確かめるために、「電源を持たない物体を音や振動で識別・読み出しする研究」を洗い直したものである。調査は2026年7月30日に実施した。

書誌情報の確認方法について先に断っておく。ACM Digital Library と IEEE Xplore と AIP Publishing と Wiley Online Library は自動取得を拒否したため、これらに掲載された文献については、著者本人が公開している論文PDF、学会の予稿集ページ、または DOI 登録機関である Crossref が保持する書誌レコード（`https://api.crossref.org/works/<DOI>`）で確認した。Crossref の書誌レコードは出版社が DOI 登録時に届け出た一次的な書誌情報であり、題名・著者・掲載誌・巻号ページ・年をそこで確認できたものは「確認済み」として扱った。本文の技術的内容まで一次資料で読めたものと、書誌だけ確認できたものは、本文中で区別して書いた。

本稿は2026年7月30日に、初稿とは別の担当者による独立した検証を受けている。検証では、記載されたすべての文献について Crossref の書誌レコードに一件ずつ照会し、論文番号や号の欠落は計算機科学の書誌データベースである dblp（`https://dblp.org/search/publ/api`）で補い、要旨は OpenAlex（`https://api.openalex.org/works/`）と Semantic Scholar（`https://api.semanticscholar.org/graph/v1/paper/`）から取得した。加えて、著者や学会が公開している本文PDFを8件ダウンロードして全文を読み、数値の主張を原典と突き合わせた。その結果として訂正した箇所は、どこをどう直したかが分かるように本文中に明示してある。詳細は末尾の「検証の記録」の節に書いた。

---

## この切り口の要約

電源を持たない物体を音で識別する研究は、HCI の分野に厚い蓄積がある。動作の種類でおおまかに分けると、こする系（Acoustic Barcodes、Stane、Rubbinput）、はじく系（Lamello）、叩く系（Tickers and Talker、Acoustic Voxels、Knocker）、吹く系（Blowhole、Whoosh の FluteCase、SqueezaPulse）、剥がす系（Let It Rip!）、そして機械的に弾かれて超音波を出す系（SoundOff）がある。工学の分野には、表面弾性波を使う受動タグ（SAW RFID）、水中の受動音響識別タグ、音響メタマテリアルによる識別タグ（EMIT）が別系統で存在する。

CipherFlute にとって最も危険なのは次の3件である。第一に Whoosh（ISWC 2016）の FluteCase は、長さの異なる8本の閉管を並べた受動的な3Dプリント構造を吹いて、2キロヘルツから10キロヘルツの帯域内に置いた8つの音高で位置を識別する。しかも論文中で、一連のイベント列を認証に使う構想まで述べている。物理機構としては CipherFlute の最近接であるにもかかわらず、現在の論文はこれを引用していない。第二に Acoustic Barcodes（UIST 2012）は、受動音響タグに6ビットから24ビットの二進符号を載せ、先頭と末尾にガード列を置き、0の連続を禁じる制約を課し、ハミング符号、BCH符号、拡張ゴレイ符号、Reed–Solomon 符号による誤り訂正まで論じている。CipherFlute が符号層で主張しうる要素（ガード、遷移保証、誤り訂正）は2012年の時点でほぼ出そろっている。第三に Blowhole（GI 2018）は、3Dプリント物の内部にヘルムホルツ共鳴器を埋め、吹いた音高で1物体あたり最大9個のタグを識別する（空洞6個までなら98パーセント）。

一方で、これらのどれもが「1個の物体から100ビットを超える秘密の値そのものを読み出す」ことを目的にしていない。運べる情報量は、Acoustic Voxels が実証4ビット、Acoustic Barcodes が誤り訂正込みで12ビットから30ビット、水中の受動音響バーコードが実証3ビット（7通り）、Blowhole が1物体あたり最大9個のタグである。表面弾性波タグは32ビットから128ビットが語られるが、それは目標値であって、章が書かれた時点の実用品は約1万通り（およそ13ビット）にとどまる。また、脅威モデルを明示して秘匿性を秘密分散に委ねる議論と、気温や息の強さを打ち消す基準笛は、先行研究に見当たらなかった。ただし「周波数軸を等間隔の小帯域に区切り、各帯域を符号の1桁として使う」という設計そのものは、水中の受動音響バーコード（Journal of Applied Physics, 2022年）にすでに存在する。CipherFlute の語彙設計に残る新しさは、格子がセント等分の対数格子であること、および各スロットが在無の2値ではなく13元のアルファベットであることに絞られる。

---

## 新規性への脅威が大きい文献

### 1. Whoosh: non-voice acoustics for low-cost, hands-free, and rapid input on smartwatches

- 著者: Gabriel Reyes, Dingtian Zhang, Sarthak Ghosh, Pratik Shah, Jason Wu, Aman Parnami, Bailey Bercik, Thad Starner, Gregory D. Abowd, W. Keith Edwards
- 発表: Proceedings of the 2016 ACM International Symposium on Wearable Computers (ISWC '16), pp. 120–127, 2016年
- 確認先: 著者所属機関が公開する本文PDF <https://sites.cc.gatech.edu/fac/keith/pubs/iswc2016-whoosh.pdf>（本文全体を取得して読んだ）および DOI 書誌レコード <https://doi.org/10.1145/2971763.2971765>
- 題名の表記について。本文PDFの標題は "Whoosh: Non-Voice Acoustics for Low-Cost, Hands-Free, and Rapid Input on Smartwatches" とタイトルケースで組まれており、ACM の書誌レコードは同じ題名を小文字化して登録している。どちらを写しても同じ文献である。

内容の要約を述べる。この研究は、スマートウォッチのマイクロホンだけで、吹く、すする、息を吹き付けるといった非音声の音響イベントを認識する手法を提案している。中核となるのが FluteCase と名付けた受動的な3Dプリント時計ケースであり、著者らは「閉管楽器の構造に着想を得た」と述べ、その例としてギリシャのパンフルートを挙げている（パンフルートそのものを模したと書いているのではない）。ケースには長さの異なる8本の閉管が仕込まれ、それぞれに開口穴があり、本文は「8本の管は2キロヘルツから10キロヘルツの間の8つの異なる周波数で共鳴するように設計した」と述べている。管長は本文の式(2)で `L = 14.956 × 2^(i/12)` ミリメートル（i は管の番号）と定められており、公比は半音比 `2^(1/12)` そのものである（この式は本文PDFから抽出した文字列 "L = 14.9562 i 12 [mm] (2)" を組み直して読んだものであり、指数表記の復元に一段の解釈が入っていることを断っておく）。ここで数値の整合について注意を書き添える。i を0から7まで動かすと管長は14.96ミリメートルから22.39ミリメートルまでの約1.5倍しか動かないので、8つの音高は2キロヘルツから10キロヘルツの帯域「を張る」のではなく、その帯域の「内側に収まる」と読むのが正しい。本文には8本それぞれの周波数を並べた表は無く、この点は実測値では裏が取れていない。ケースの外形は正方形版が幅45.60ミリメートル、長さ51.06ミリメートル、深さ5.58ミリメートルで、穴径は4.05ミリメートル、管幅は一定の4.096ミリメートルである。8名の参加者と14種類のイベントで平均91.4パーセント（標準偏差5.3パーセント）の認識精度を得ている。応用の節では、あらかじめ決めた一連の Whoosh イベント列で端末のロックを解除する認証や、他端末での購入を完了させるための物理的なチャレンジとしての利用に言及している。

CipherFlute との関係を述べる。長さの異なる管を並べた受動的な3Dプリント構造を吹き、生じる音高で符号を区別するという物理機構が、CipherFlute とほぼ同一である。さらに管長を半音比の等比数列で決めている点まで一致する。ただし FluteCase の8本は「押しボタンの代わり」であって、物体側に情報が格納されているわけではない。秘密は利用者が記憶しているイベント列の側にあり、物体は入力装置にすぎない。CipherFlute は逆に、秘密を物体の幾何に格納し、利用者は何も覚えない。なお Blowhole は Whoosh を引用したうえで、「Whoosh で使われているような単純な管はどの向きでも良好に印刷できたが、広い周波数範囲を確保しようとすると小さな物体に埋め込むには大きくなりすぎた」と述べて退けている。CipherFlute の薄いフィップル笛はこの制約を回避する方向にあたるので、この一文は差分を述べる足場になる。

脅威の度合いは「高」である。理由は三つある。第一に、受動的な3Dプリント多管笛を吹いて音高で識別するという物理機構の新規性は、この研究によってほぼ消える。第二に、管長を半音比で決めるという設計も先行例がある。第三に、認証という文脈での利用にまで踏み込んでおり、しかも現在の論文はこの文献を一切引用していないため、査読で指摘された場合の打撃が大きい。

### 2. Acoustic Barcodes: Passive, Durable and Inexpensive Notched Identification Tags

- 著者: Chris Harrison, Robert Xiao, Scott E. Hudson（本文PDFの著者行は "Scott E. Hudson" である。ACM の書誌レコードは中間名の頭文字を落として "Scott Hudson" と登録しているが、同一人物である）
- 発表: Proceedings of the 25th Annual ACM Symposium on User Interface Software and Technology (UIST '12), pp. 563–568, 2012年
- 確認先: 著者本人が公開する本文PDF <https://www.chrisharrison.net/projects/acousticbarcodes/AcousticBarcodes.pdf>（本文全体を取得して読んだ）および DOI 書誌レコード <https://doi.org/10.1145/2380116.2380187>

内容の要約を述べる。表面に刻んだ切り欠きの列を爪やペンでこすると、切り欠きの間隔に応じた過渡音の列が生じる。この過渡音の時間間隔を復号して二進の識別子を得る。切り欠きは厚さ0.25ミリメートルから0.5ミリメートル、深さ0.1ミリメートルから0.3ミリメートルで、単位間隔は1.6ミリメートルまたは3.2ミリメートルである。爪や尖筆が入るように、切り欠きの幅は7ミリメートル以上を推奨している。符号列の前後には、単位間隔で並ぶ3本の溝からなるガード列を置き、これが符号の切り出しと単位間隔の基準の両方を兼ねる。符号化方式は二つあり、固定切り欠き数方式と固定物理長方式である。前者は0を「切り欠き＋単位間隔1つ」、1を「切り欠き＋単位間隔2つ」で表すので切り欠き数は一定だが全長が変わる。後者は1を切り欠き、0を空白（切り欠きなし）とし、どの桁も単位間隔1つで区切るので全長が一定になる。後者では切り欠きのない区間が長く続くのを避けるため、0が2回続く系列を許容集合から除外し、クロック信号が必ず復元できるようにしている。

評価では7名の参加者に、6ビット、12ビット、24ビットの符号と、1.6ミリメートルまたは3.2ミリメートルの単位間隔を、爪、白板用マーカー、携帯電話の3通りの入力方法で読ませた。誤りゼロで完全一致した割合は、携帯電話が最良で87.4パーセント、爪が77.9パーセント、白板用マーカーが最下位で66.4パーセントである。誤り訂正を符号に含めた場合の推定値は、それぞれ93.1パーセント、87.4パーセント、77.3パーセントである。考察では、6ビット符号なら切り詰めた(7,4)ハミング符号で3データビットと3検査ビット、12ビット符号なら切り詰めた(15,7) BCH 符号で4データビットと8検査ビット、24ビット符号なら拡張ゴレイ符号で12データビットと12検査ビットとなり4096通りの識別子が得られること、(63,30) BCH 符号なら30データビットで約10億通りになることを具体的に計算している。単位間隔を1ミリメートルに詰めれば約6センチメートルに60ビットを載せられるとも述べている。素材には3Dプリント物も含まれ、高密度かつ光沢の設定で刷ることが条件だと注記している。符号列を Hamming 符号や Reed–Solomon 符号で前処理してよいとも明記している。なお Blowhole の関連研究節によれば、Acoustic Barcodes の相互作用要素は最小でも7ミリメートル×22ミリメートルを占める。

CipherFlute との関係を述べる。CipherFlute が符号層で採用している三つの工夫、すなわち基準を与えるガード的な要素、隣接する記号が同じにならない遷移保証、Reed–Solomon 符号による誤り訂正のいずれもが、この研究にすでに現れている。ただし Acoustic Barcodes の符号語は時間間隔であって音高ではなく、読み出しは接触マイクロホンでこすることを要し、タグは表面に露出していて隠蔽されていない。搬送できる情報量も、誤り訂正込みで12ビットから30ビット程度にとどまる。

脅威の度合いは「高」である。理由を述べる。この研究の存在によって、「受動音響タグに符号設計と誤り訂正を持ち込んだ」という水準の主張は成立しなくなる。現在の論文はこの文献を引用しているものの、遷移保証と誤り訂正の設計論がすでに詳細に論じられていることまで踏まえた差分の書き方をしないと、符号層の貢献が丸ごと否定されかねない。

### 3. Blowhole: Blowing-Activated Tags for Interactive 3D-Printed Models

- 著者: Carlos Tejada, Osamu Fujimoto, Zhiyuan Li, Daniel Ashbrook
- 発表: Proceedings of the 44th Graphics Interface Conference (GI 2018), pp. 122–128, 2018年
- 確認先: 学会予稿集の本文PDF <http://graphicsinterface.org/wp-content/uploads/gi2018-18.pdf>（本文全体を取得して読んだ。第1ページの柱に "Graphics Interface Conference 2018, 8-11 May, Toronto, Ontario, Canada" とあり、各ページの下端の頁番号から通し頁が122から128であることを確認した）
- URLの注意: 予稿集ページ <http://graphicsinterface.org/proceedings/gi2018/gi2018-18/> と DOI <https://doi.org/10.20380/GI2018.18> は、いずれも現在 ACM Digital Library の <https://dl.acm.org/doi/10.20380/GI2018.18> へ転送される。DOI は登録されていて生きているが、Crossref には書誌レコードが無く（照会すると "Resource not found" が返る）、ACM 側は自動取得を拒否する。したがって書誌の裏取りは上記の本文PDFで行った。論文に引くなら DOI と学会PDFの両方を書くのが安全である。

内容の要約を述べる。3Dモデルの内部に球状の空洞と、そこから表面へ抜ける直管を彫り、利用者が口を5センチメートルから10センチメートル離して軽く吹くと、ヘルムホルツ共鳴の式にしたがう音高が出る。管径を5ミリメートルに固定し、球径を8ミリメートルから40ミリメートルまで4ミリメートル刻みで、管長を2.5、3.5、5、7.5、8.5、10ミリメートルの6通りに変えて48個の試験片を作り、10名から830回分の吹奏を収録した。周波数の設計範囲は500ヘルツ（管径5ミリメートル、管長10ミリメートル、球径40ミリメートル）から5900ヘルツ（管径5ミリメートル、管長2.5ミリメートル、球径8ミリメートル）である。管長2.5ミリメートルで球径8ミリメートルから28ミリメートルの6種類を使うと、利用者非依存で98パーセントの識別精度が出る。球径32ミリメートルを加えると90パーセントに下がり、さらに大きな球を足すと下がり続ける。結論では1物体あたり最大9個のタグまで高い性能が出ると述べ、これが受動音響方式としては先行研究より多いと主張している。空洞と管はサポート材なしで印刷でき、後加工も組み立ても要らない（ただし大きな球空洞では上部が水平に近づいて造形が乱れるので、対応する径のドリルを手で回して整える手直しが要ると述べている）。設計ソフトウェアが深さ優先探索と後戻りで空洞の配置を最適化する。

CipherFlute との関係を述べる。電源も電子部品も持たない3Dプリント物を吹いて、生じる音高で符号を読むという着想の直接の先行研究である。CipherFlute の笛はフィップル（エッジトーン）方式であってヘルムホルツ共鳴器ではなく、平置きで印刷でき複数本を融合できるという造形上の性質が異なる。また Blowhole の各穴は独立した識別子であって、複数の穴を並べて一つの長い符号語を作るという発想はない。誤り訂正も基準音による正規化も秘密情報の議論も存在しない。

脅威の度合いは「高」である。理由を述べる。現在の論文はこの文献を引用しているものの、「吹く受動音響タグ」という枠だけを見れば主要な着想が先取りされている。CipherFlute が主張できるのは、1本あたりの符号語彙を13スロットまで細分したこと、それを40本から49本並べて128ビットの秘密を運んだこと、基準笛と誤り訂正で読み出しを成立させたこと、そして秘密情報という用途を持ち込んだことに限られる。この差分を数字で明確に書かないと、増分的な改良と見なされる危険が高い。

### 4. Lamello: Passive Acoustic Sensing for Tangible Input Components

- 著者: Valkyrie Savage, Andrew Head, Björn Hartmann, Dan B. Goldman, Gautham Mysore, Wilmot Li
- 発表: Proceedings of the 33rd Annual ACM Conference on Human Factors in Computing Systems (CHI '15), pp. 1277–1280, 2015年
- 確認先: 著者本人が公開する本文PDF <https://people.eecs.berkeley.edu/~bjoern/papers/savage-lamello-chi2015.pdf>（本文全体を取得して読んだ）および DOI 書誌レコード <https://doi.org/10.1145/2702123.2702207>

内容の要約を述べる。長さの異なる櫛歯（tine）を並べた構造を作り、利用者がスライダやダイヤルを動かすと歯が弾かれて、歯ごとに異なる基本周波数の音が出る。名称の由来は本文に「Lamello という名は、長さの異なる舌状の部品が振動して音を出すラメロフォン族の楽器から採った」と書かれている（親指ピアノなど個々の楽器名は本文には出てこないので、ここでは挙げない）。歯の基本周波数は幾何形状と材料定数から予測でき、実測との残差は平均69.0ヘルツ、標準偏差112.5ヘルツであった。7本の歯の予測周波数は、スライダが924、1103、1340、1662、2116、2784、3824ヘルツ、ダイヤルが840、1003、1218、1511、1923、2530、3478ヘルツである（図6の横軸で確認した）。認識性能は表1にまとめられており、歯4本のときはFDMスライダが適合率93パーセントと再現率90パーセント、FDMダイヤルが90パーセントと85パーセント、指で弾くデルリン製が98パーセントと97パーセントである。歯7本にするとそれぞれ49パーセントと56パーセント、63パーセントと54パーセント、72パーセントと73パーセントまで落ちる。本文はこの劣化の理由を「2キロヘルツを超える基本周波数はエネルギーが小さく減衰も速いため認識器が分類に失敗する」と述べ、結論でも「基本周波数が2キロヘルツを超える領域には新しい手法が要る」と明記している。論文の主要な貢献の一つとして「情報の符号化方式」を挙げており、de Bruijn 系列 D(k,n) を使って、少ない種類の基本周波数でも n 回の連続認識から位置と向きを一意に定める設計を示している。なお Blowhole の関連研究節によれば、Lamello の相互作用要素は4ミリメートル×50ミリメートルを要する。

CipherFlute との関係を述べる。音高そのものを符号の記号として使い、しかも符号語の設計（de Bruijn 系列）まで踏み込んだ受動音響部品の先行例である。周波数域も CipherFlute の1480ヘルツから2960ヘルツと大きく重なっており、しかも2キロヘルツ以上で識別が難しくなるという報告は、CipherFlute の音域選択の妥当性に対する反証材料にも援護射撃にもなりうる。ただし Lamello は入力部品の状態検出が目的であり、物体に固定的な情報を格納する発想はなく、誤り訂正も秘密情報の視点もない。

脅威の度合いは「中」である。理由を述べる。音高を記号とする受動音響符号という枠組みが先行しているため必ず引用して差分を述べる必要がある。ただし運ぶ情報はスライダ位置などの状態であって、任意のビット列ではない。

### 5. Acoustic Voxels: Computational Optimization of Modular Acoustic Filters

- 著者: Dingzeyu Li, David I. W. Levin, Wojciech Matusik, Changxi Zheng
- 発表: ACM Transactions on Graphics, 第35巻第4号, 論文番号88, pp. 88:1–88:12, 2016年（SIGGRAPH 2016）
- 確認先: 著者らのプロジェクトページが公開する本文PDF <https://www.cs.columbia.edu/cg/lego/acoustic-voxels-siggraph-2016-li-et-al.pdf>（本文全体を取得して読んだ）、DOI 書誌レコード <https://doi.org/10.1145/2897824.2925960>、および論文番号を確認した dblp のレコード <https://dblp.org/search/publ/api?q=Acoustic+voxels>

内容の要約を述べる。伝達行列をあらかじめ計算した形状素片を組み合わせて、目標とする音響特性を満たすフィルタを自動設計する手法である。応用として音響タグと音響符号化の二つを示している。音響タグでは、外見の同じ豚の置物3体それぞれに異なるインピーダンス曲線を与え、鼻を手のひらで叩いた音を iPhone アプリで解析して識別する。3体の目標ピークはそれぞれ305・836・1200ヘルツ、250・890・1300ヘルツ、338・1004・1607ヘルツの各3本である。音響符号化では、透過損失曲線の上で2N個の周波数を等間隔に取り、隣り合う対の大小関係で1ビットずつ表すという単純な符号化を提案し、外見の同じタコ型の造形物3体で "0000"、"1001"、"0111" という4ビットの符号列を実現した。こちらの読み出しは、iPhone のスピーカとマイクロホンを物体の吸込口と吐出口に合わせ、白色雑音を通して透過後の振幅を測る方式である。

なお「10個以上のピーク」という数字について訂正を書き添える。本調査の前に書かれていた記述は、豚の置物3体が各々10個以上のピークを持つと述べていたが、これは誤りである。本文で「10個を超えるピークを最適化した」と述べられているのは、くちばしを吸込口、尾を吐出口としてボクセル化したアヒル型の浮き輪 BOB についてであり、豚の置物のピークは上記のとおり各3本である。

CipherFlute との関係を述べる。「3Dプリント物の音響応答にビット列を埋め込み、市販のスマートフォンで復号する」という骨格が完全に一致する先行研究である。ただし読み出しは叩打または雑音の透過であって吹奏ではなく、実証された容量は4ビットにとどまり、誤り訂正も基準による正規化も秘密情報の視点もない。また Blowhole の関連研究節は、Acoustic Voxels は情報を符号化するのに2センチメートル角の構造を複数必要とするため物体が大きくならざるをえないと指摘している。CipherFlute は同じ骨格を、1本あたり約3.7ビット、40本から49本で128ビットという規模まで押し上げている点で差分がある。

脅威の度合いは「中」である。理由を述べる。着想としては最も近い部類だが、実証容量が4ビットと桁違いに小さく、CipherFlute の「暗号鍵の復元情報を丸ごと運ぶ」という主張を直接は脅かさない。現在の論文はすでに引用しているので、4ビットという数字を明示して規模の差を書くべきである。

### 6. Tickers and Talker: An Accessible Labeling Toolkit for 3D Printed Models

- 著者: Lei Shi, Idan Zelzer, Catherine Feng, Shiri Azenkot
- 発表: Proceedings of the 2016 CHI Conference on Human Factors in Computing Systems (CHI '16), pp. 4896–4907, 2016年
- 確認先: DOI 書誌レコード <https://doi.org/10.1145/2858036.2858507> および要旨全文を取得した OpenAlex のレコード <https://api.openalex.org/works/https://doi.org/10.1145/2858036.2858507>

内容の要約を述べる。3Dモデルに小さな打楽器状の突起（Ticker）を付け、利用者がそれをはじくと部位ごとに異なる音が鳴る。Talker と呼ぶ信号処理アプリケーションがその音を検出して分類し、あらかじめ録音しておいた音声ラベルを再生する。視覚障害のある利用者が3Dプリント模型の各部位のラベルを聞き取れるようにすることが目的である。手順は、模型の設計者が3Dモデリングソフトウェアで Ticker を足し、利用者が印刷してから各 Ticker に音声ラベルを録音し、以後は Ticker をはじけば対応するラベルが再生されるというものである。3種類の模型を使って全盲の参加者9名で評価し、全参加者と全模型を通じて93パーセントの精度を得ている。Blowhole の関連研究節によれば、Ticker の相互作用要素は11.5ミリメートル×17ミリメートルの寸法を要する。

CipherFlute との関係を述べる。電源を持たない3Dプリント構造を機械的に励起して、音の違いで場所を識別するという点が共通する。情報量は模型の部位数の範囲であり、符号設計も誤り訂正も秘密情報の視点もない。

脅威の度合いは「中」である。理由を述べる。受動音響タグの直接の系譜にあり Blowhole も比較対象としているため引用が必要だが、CipherFlute の符号化と秘密という主張には触れない。

### 7. SoundOff: Low-cost Passive Ultrasound Tags for Non-invasive and Non-Intrusive Smart Home Sensing

- 著者: Yibo Fu, Vivian Shen, Víctor Riera Naranjo, Bolei Deng, Alex Adams, Josiah Hester
- 発表: Proceedings of the ACM on Interactive, Mobile, Wearable and Ubiquitous Technologies, 第9巻第4号, 論文番号174, pp. 1–32, 2025年
- 確認先: 米国国立科学財団の公開リポジトリ <https://par.nsf.gov/biblio/10670927-soundoff-low-cost-passive-ultrasound-tags-non-invasive-non-intrusive-smart-home-sensing>（要旨を取得した）、DOI 書誌レコード <https://doi.org/10.1145/3770666>、および論文番号174を確認した dblp のレコード <https://dblp.org/search/publ/api?q=SoundOff+passive+ultrasound+tags>（"9(4): 174:1-174:32 (2025)" と記録されている）

内容の要約を述べる。電池も電子部品も持たない3Dプリント製のタグを、扉の取っ手、便座の蓋、戸棚、蛇口、窓などに貼り付ける。家具が動くとタグが固有の超音波を鳴らし、利用者が身に着けたウェアラブル機器がそれを拾って、どのタグが鳴ったかを判別する。可聴域より上の周波数を使うため人には聞こえず、電子部品も追加の設備も要らない。著者らは、物理に基づくモデルによって、固有かつ識別容易な超音波を出す設計を数千通り系統的に生成できると述べている。以上はいずれも要旨で裏を取った記述である。ただし発音機構の細部、すなわち「ポリ乳酸樹脂製の片持ち梁が金属円板を弾く」「部品は片持ち梁、台座、蓋の3点のみ」という説明は要旨には現れず、本文は ACM Digital Library が自動取得を拒否するため確認できていない。論文に引くときは、この2点を根拠として使わないほうがよい。

CipherFlute との関係を述べる。電源を持たない3Dプリント構造の機械的励起で固有周波数を出し、それを識別子として読むという枠組みが同じである。しかも「数千通りの識別可能な設計」という主張は、CipherFlute の13スロットという語彙よりはるかに大きい。ただしタグ1個が1個の識別子に対応する設計であり、複数個を並べて長い符号語を作る発想も、誤り訂正も秘密情報の視点もない。周波数域は超音波であって、人が耳で確かめられる可聴音ではない。

脅威の度合いは「中」である。理由を述べる。2025年の最新研究として審査員が想起しやすく、識別可能な設計数の大きさで CipherFlute の語彙設計が見劣りしうる。一方で用途が家庭内の行動センシングであり、秘密情報の保管という土俵は共有していない。

### 8. Artificial Intelligence in Metamaterial Informatics for Sonic Frequency Mechanical Identification Tags

- 著者: Daniel Saatchi, Myung‐Joon Lee, Tushar Prashant Pandit, Manmatha Mahato, Il‐Kwon Oh
- 発表: Advanced Functional Materials, 第35巻第10号, 論文番号2414670, 2025年3月（オンライン先行公開は2024年12月4日）
- 確認先: Crossref の書誌レコード <https://api.crossref.org/works/10.1002/adfm.202414670>（巻35・号10・論文番号2414670・冊子は2025年3月・オンラインは2024年12月4日をここで確認した）および要旨全文を取得した Semantic Scholar のレコード <https://api.semanticscholar.org/graph/v1/paper/DOI:10.1002/adfm.202414670?fields=abstract>。出版社の頁 <https://onlinelibrary.wiley.com/doi/10.1002/adfm.202414670> は購読を求めて本文を返さない

内容の要約を述べる。三重周期極小曲面をもとにした3Dプリントのフォノニック構造を設計し、機械学習でソニック帯のバンド周波数番号（band frequency number）を予測する枠組みを作った。これによって作られるのが「符号化された機械式識別タグ（encoded mechanical identification tag、著者らは EMIT と略す）」であり、音波と相互作用して固有の応答を返す。復号側は深層学習の音響分類器であり、楽器の所有者識別という応用を示している。水中での応用として、民事の事故調査、すなわち行方不明の航空機、潜水者、沈没船、価値のある積荷を積んだコンテナの音響的な探索にも触れている。著者らはこれを第一世代の受動的ソニック周波数識別（passive sonic frequency identification、著者らは SFID と略す）トランスポンダタグと位置づけている。以上はすべて要旨で裏を取った記述である。

CipherFlute との関係を述べる。3Dプリント構造の固有振動を符号として使い、音で読み出す受動タグという点が一致する。「符号化された」という語をタグ名に含み、識別を主目的に据えている点で、CipherFlute の音響符号層と正面から重なる。ただし読み出しは分類器による個体識別であって、任意のビット列を復元するものではない。

脅威の度合いは「中」である。理由を述べる。材料科学側から「受動ソニック識別タグ」という枠を正面から立てた最新の研究であり、引用しないと分野横断の目配りを欠くと見なされる。ただしビット数や識別可能個数、誤り訂正の有無は要旨からは読み取れず、秘密情報の視点は見当たらない。

### 9. FabAuth: Printed Objects Identification Using Resonant Properties of Their Inner Structures ならびに続報

- 著者: Yuki Kubo, Kana Eguchi, Ryosuke Aoki, Shigekuni Kondo, Shozo Azuma, Takuya Indo
- 発表: Extended Abstracts of the 2019 CHI Conference on Human Factors in Computing Systems (CHI EA '19), pp. 1–6, 2019年
- 確認先: DOI 書誌レコード <https://doi.org/10.1145/3290607.3313005> および要旨全文を取得した Semantic Scholar のレコード <https://api.semanticscholar.org/graph/v1/paper/DOI:10.1145/3290607.3313005?fields=abstract>
- 続報: Yuki Kubo, Kana Eguchi, Ryosuke Aoki, "3D-Printed Object Identification Method using Inner Structure Patterns Configured by Slicer Software", Extended Abstracts of the 2020 CHI Conference on Human Factors in Computing Systems (CHI EA '20), pp. 1–7, 2020年、確認先 <https://doi.org/10.1145/3334480.3382847>

内容の要約を述べる。外見が同一でも内部構造を変えれば共振特性が変わることを利用し、3Dプリント物を識別する。物体に振動を送り込み、物体を透過してきた振動から共振特性の差を読み取る。充填率の低い造形物でも、音波が一方のセンサから他方へ通り抜けさえすれば適用でき、予備実験で平均92.2パーセントの分類精度を得た。続報ではスライサソフトウェアの設定で内部構造のパターンを作り分ける方法へ発展させている。名称に authentication の語を含むとおり、真正性の確認という文脈を持つ。なお加振に使う素子の種類については、要旨には「振動」「センサ」とあるだけで圧電素子とは書かれていない。本文は ACM Digital Library が自動取得を拒否するため確認できていないので、素子の種類を根拠にした差分の書き方は避けるべきである。

CipherFlute との関係を述べる。3Dプリント物の内部構造の共振で個体を識別するという枠組みが近い。とくに「同じ外見で内部だけ違う」という設計思想は、CipherFlute の「日用品に見えるが内部に笛がある」という偽装と発想が重なる。ただし読み出しには加振器を物体に接触させる能動的な励起が必要であり、電源のない吹奏とは異なる。運ぶ情報は個体の識別子であって任意のビット列ではない。

脅威の度合いは「中」である。理由を述べる。造形物の内部を音響で読むという系譜の代表例であり、しかも真正性という安全性の文脈を持つため、引用して差分を述べる必要がある。

### 10. Surface Acoustic Wave RFID Tags ならびに Review on SAW RFID tags

- 著者: S. Härmä, V. P. Plessky（章）／ Victor P. Plessky, Leonhard M. Reindl（総説）
- 発表: 章は書籍 *Development and Implementation of RFID Technology*（Cristina Turcu 編, InTech, 2009年, ISBN 978-3-902613-54-7）第8章, pp. 145–160。総説は IEEE Transactions on Ultrasonics, Ferroelectrics, and Frequency Control, 第57巻第3号, pp. 654–668, 2010年
- 確認先: 章の本文PDF <https://cdn.intechopen.com/pdfs/6032/InTech-Surface_acoustic_wave_rfid_tags.pdf>（本文全体を取得して読んだ。書名・編者・ISBN は本文末尾の "How to reference" の欄に印字されており、頁範囲は各ページの柱の番号から確認した）、出版社の章ページ <https://www.intechopen.com/chapters/6032>、総説の DOI 書誌レコード <https://doi.org/10.1109/tuffc.2010.1462>
- 著者名の表記について。章のPDFと出版社の章ページはいずれも "S. Härmä" と頭文字だけを記している。本調査では given name が Sanna であることを一次資料で確認できなかったため、頭文字のままにした。論文に引くときも "S. Härmä" と書くのが安全である。
- DOI についての警告。出版社の章ページはこの章の DOI を 10.5772/6032 と表示するが、この DOI を実際に解決すると <https://www.intechopen.com/chapters/5340> という別の章に飛び、Crossref に照会すると "Asymptotic Stability Analysis of Linear Time-Delay Systems" という無関係な章の書誌が返る。つまりこの DOI は当該章を指していない。論文に引くときは DOI を書かず、書名・編者・ISBN・頁と上記の PDF の URL で示すべきである。

内容の要約を述べる。表面弾性波タグは電池を持たない完全に受動的な素子であり、問い合わせ電波を弾性波に変換し、反射器の列で遅延させて返す。符号化は反射器の時間位置を使う方式（時間位置符号化）が実用の中心であり、位相符号化を組み合わせる方式も研究されている。有限要素法と境界要素法で模擬した実装例は反射器を14個持ち、そのうち10個を符号そのものに充て、最初と最後の1個ずつを校正用として他より強い応答になるよう設計し、最後の1個の手前に並ぶ2個を誤り制御、すなわちチェックサムの作成に充てている。時間位置符号化では1個の反射器が取りうる時間位置は十進法の10通りであり、市販の表面弾性波タグの容量は約1万通り、つまり十進の時間位置系では符号用反射器4個に相当する。位相符号化では反射器の位置を波長の8分の1の整数倍だけずらして90度刻みの位相差を作るので、1個あたり4つの位相状態、すなわち2ビットが時間位置符号化に上乗せされる。これを加えると上記の符号用反射器10個のタグは2の40乗通り、40ビット、およそ10の12乗通りの符号を持つと述べられている。目標容量については、商業的に成り立つには少なくとも20ビットから32ビットが要るとし、32ビット（できれば64ビットか128ビット）を得るには16メガヘルツ（あるいは32、64メガヘルツ）の帯域が必要だと計算し、64ビットや128ビットへの飛躍を狙う研究が進んでいると述べている。すなわち32ビットから128ビットは目標値であって、章が書かれた時点の実用品は約1万通り（およそ13ビット）にとどまる。

CipherFlute との関係を述べる。電源を持たない音響素子に多ビットの符号を載せ、校正用の要素とチェックサム用の要素を別に置くという設計が、CipherFlute の基準笛と誤り訂正の対応物になっている。ここで一点、CipherFlute にとって不都合な事実を明示しておく。この章は校正用反射器の役割を「温度、製造ばらつき、その他の変動に由来する位置の誤差を吸収する」と明記している。つまり「既知の基準要素をタグ自身に混ぜて温度変動を打ち消す」という発想そのものは、受動音響タグの分野に確立した先行例がある。CipherFlute に残る差は、打ち消す軸が時間軸ではなく周波数軸であること、および吹く息の強さという人間側の変動まで同じ仕組みで吸収していることである。そのほかの相違点として、読み出しには無線送受信機が要り、素子は圧電結晶であって家庭用3Dプリンタでは作れず、可聴音でもない。またタグの符号は工場で決まる識別子であって、利用者の秘密を格納する媒体ではない。

脅威の度合いは「中」である。理由を述べる。「受動音響タグの多ビット符号化」と「基準要素による環境変動の打ち消し」という一般論は、いずれも工学分野に確立した先行例があるため、CipherFlute が符号設計や基準の考え方そのものを新規と主張することはできない。むしろ設計の作法を借りた先行例として位置づけるのが安全である。

### 11. 水中の受動音響識別タグの系列

- Yanling Zhou, Jun Fan, Jinfeng Huang, Bin Wang, "Passive underwater acoustic barcodes using Rayleigh wave resonance", Journal of Applied Physics, 第131巻第12号, 論文番号124901, 2022年。確認先: 著者版全文PDF <https://arxiv.org/pdf/2107.13860>（本文全体を取得して読んだ）、プレプリントの書誌ページ <https://arxiv.org/abs/2107.13860>（同ページに掲載誌の DOI が明記されており同一論文であることを確認した）、および Crossref の書誌レコード <https://api.crossref.org/works/10.1063/5.0086290>
- Fulin Zhou, Jun Fan, Bin Wang, Yanling Zhou, Jinfeng Huang, "Acoustic barcode based on the acoustic scattering characteristics of underwater targets", Applied Acoustics, 第189巻, 論文番号108607, 2022年。確認先: Crossref の書誌レコード <https://api.crossref.org/works/10.1016/j.apacoust.2021.108607>（書誌のみ。本文は未確認）
- Aprameya Satish, David Trivett, Karim G. Sabra, "Omnidirectional passive acoustic identification tags for underwater navigation", The Journal of the Acoustical Society of America, 第147巻第6号, pp. EL517–EL522, 2020年。確認先: Crossref の書誌レコード <https://api.crossref.org/works/10.1121/10.0001444>（書誌のみ。本文は未確認）
- Nizar Somaan, Ananya Bhardwaj, Karim G. Sabra, "Passive acoustic identification tags for marking underwater docking stations", JASA Express Letters, 第4巻第12号, 論文番号126001, 2024年。確認先: Crossref の書誌レコード <https://api.crossref.org/works/10.1121/10.0034495>（書誌のみ。本文は未確認）

内容の要約を述べる。ここでは本文まで読めた Journal of Applied Physics 論文（上海交通大学の Zhou らによるもの）について詳しく書き、残りは書誌のみ確認したことを断っておく。アクリル製の弾性体に広帯域のパルス音を当てると、亜音速レイリー波の共鳴に由来する強い後方散乱ピークが現れる。レイリー波速度は対象の周波数帯ではほぼ一定なので、共鳴ピークの位置は球の半径で決まり、半径を変えたり複数の球を組み合わせたりすれば固有の音響署名を作れる。

ここが重要な点である。この論文の符号化は、単に「固有の署名で個体を見分ける」だけの話ではない。エコーの帯域幅 B を m 個の等幅の小帯域に区切り、ある小帯域に共鳴ピークがあれば「1」、無ければ「0」（空白）として、白黒のバーコードを作ると明記している。図1では0キロヘルツから38キロヘルツにわたる17桁の二進列 "00001101010110101" を示している。実験では6キロヘルツから10.5キロヘルツを幅1.5キロヘルツの3つの小帯域に区切り、半径0.045、0.05、0.06、0.065メートルの4種類のアクリル球から2個を選ぶ組み合わせを7通り作って、それぞれの符号を表1に示している。すなわち実証された容量は3ビット、識別できた組み合わせは7通りである。復号はあらかじめ計算または実測した応答の対照表と照合する方式であり、ガード列、基準要素、誤り訂正符号はいずれも導入されていない。著者らは Acoustic Barcodes（Harrison ら, UIST 2012）を文献2として引用しており、空気中の音響バーコードの系譜を意識して書かれている。応用として水中目標の認識、測位、航法を挙げ、加えて「情報が対象の音響散乱特性に変調されるので、秘匿的な情報伝送と目標識別が実現できる」とも述べている。別系統（Satish らと Somaan らの JASA 系列）では、半径方向に層を成す殻の厚みと材料を選んで固有の鏡面反射パターンを作る全方向性の識別タグが提案され、水中ドッキング局の標識にも展開されているが、こちらは書誌のみ確認した段階であり、符号設計の有無は未確認である。

CipherFlute との関係を述べる。共鳴周波数を語彙として物体に情報を載せ、電源なしで読み出すという設計思想が同じである。とくに「大きさの違う共鳴体を組み合わせて署名を作る」という発想は、CipherFlute が管長の違う笛を並べる設計と直接対応する。さらに踏み込んで言えば、「周波数軸を等間隔の小帯域に区切り、各小帯域を符号の1桁として使う」という語彙設計そのものが、この2022年の論文にすでに存在する。したがって CipherFlute が「音の高さを格子に量子化して符号語彙にした」ことを無条件に新規と書くことはできない。残る差分は三つある。第一に、格子が線形等間隔（1.5キロヘルツ刻み）ではなくセント等分の対数格子（100セント刻み）であること。第二に、各スロットが共鳴ピークの在無を表す2値ではなく、13元のアルファベットの1文字であること。第三に、可聴域であり人の息で励起できるので、送受信装置を持たない利用者が耳と携帯電話だけで読めることである。読み出しに超音波の送受信装置が要る点、誤り訂正が無い点、秘密情報の視点が無い点は、従来どおり差分として使える。

脅威の度合いは「中」である。理由を述べる。音響物理の分野に「受動音響バーコード」という語がすでに定着しているだけでなく、周波数軸を等間隔に区切って二進符号を載せる設計まで実装されているため、CipherFlute の語彙設計に関する主張はこの論文との差分として書き直す必要がある。それでも「高」にしないのは、実証容量が3ビットで、誤り訂正も基準要素も無く、可聴域でも家庭用3Dプリンタでもなく、秘密情報の保管という土俵をまったく共有していないからである。

### 12. MechanoBeat: Monitoring Interactions with Everyday Objects using 3D Printed Harmonic Oscillators and Ultra-Wideband Radar

- 著者: Md. Farhan Tasnim Oshim, Julian Killingback, Dave Follette, Huaishu Peng, Tauhidur Rahman（ACM の書誌レコードは第一著者を "Md. Farhan Tasnim Oshim" と点付きで登録している）
- 発表: Proceedings of the 33rd Annual ACM Symposium on User Interface Software and Technology (UIST '20), pp. 430–444, 2020年
- 確認先: DOI 書誌レコード <https://doi.org/10.1145/3379337.3415902> および要旨全文を取得した Semantic Scholar のレコード <https://api.semanticscholar.org/graph/v1/paper/DOI:10.1145/3379337.3415902?fields=abstract>（電池も珪素チップも電子部品も要らないこと、家庭用の卓上3Dプリンタと安価な材料で作れること、壁越しの見通し外でも検出できることを、いずれも要旨で確認した）

内容の要約を述べる。電池も半導体も電子部品も持たない3Dプリントの機械式タグを日用品に取り付ける。利用者が触れるとタグが固有の周波数で振動し、超広帯域レーダの配列がその振動を検出して、どのタグが動いたかを識別する。壁越しの見通し外でも検出できると報告している。家庭用の3Dプリンタと安価な材料で作れる。

CipherFlute との関係を述べる。3Dプリントの受動的な機械共振体に固有周波数を割り当てて識別するという設計が同じである。読み出しが音ではなく電波であるという一点で分野が異なる。符号設計や誤り訂正や秘密情報の視点はない。

脅威の度合いは「中」である。理由を述べる。「電源のない3Dプリント共振体を識別子として使う」という枠組みの先行例として、音以外の読み出し手段まで含めた先行研究の広がりを示す必要があるため、引用しておく価値がある。

### 13. Printone: Interactive Resonance Simulation for Free-form Print-wind Instrument Design

- 著者: Nobuyuki Umetani, Athina Panotopoulou, Ryan Schmidt, Emily Whiting
- 発表: ACM Transactions on Graphics, 第35巻第6号, 論文番号184, pp. 184:1–184:14, 2016年（SIGGRAPH Asia 2016）
- 確認先: DOI 書誌レコード <https://doi.org/10.1145/2980179.2980250>、要旨全文を取得した OpenAlex のレコード <https://api.openalex.org/works/https://doi.org/10.1145/2980179.2980250>、論文番号を確認した dblp のレコード <https://dblp.org/search/publ/api?q=Printone>、および Blowhole 本文PDFの文献[26]（"ACM Transactions on Graphics (TOG), 35(6):184-14, Nov. 2016" と記載されている）

内容の要約を述べる。自由形状の3Dプリント管楽器を対話的に設計できるようにするために、内部空洞の共鳴を高速に模擬する手法を提案している。利用者が形を編集すると、そのつど音の模擬結果が返るので、独自の管楽器の形を探索できる。手法の中身は、楽器を受動的な共鳴体として扱い（歌口からの結合振動の励起は無視する）、共鳴問題を最小固有値問題として定式化して境界要素法で共鳴周波数を推定するというものである。さらに一般化固有値問題に基づく近似手法で高速化している。著者らは成果物を「印刷風の楽器（print-wind instruments）」と呼んでいる。Blowhole はこの研究を「音楽用途に最適化されており利用者の入力を多く要する」と評して差別化している。

なお本調査の前に書かれていた「歌口や指孔の配置も自動で行える」という記述は訂正した。要旨にそのような主張は無く、むしろ歌口からの結合振動の励起は明示的に無視すると書かれているので、この記述は根拠を欠く。

CipherFlute との関係を述べる。3Dプリント笛の管形状と発音周波数の関係を計算で扱った直接の先行研究である。CipherFlute が用いる $f = A/(L+e)$ という単純な近似式に対して、Printone はより一般の自由形状を扱う。したがって「3Dプリント笛の音高を設計できる」こと自体には新規性がない。

脅威の度合いは「中」である。理由を述べる。CipherFlute の物理層の設計（管長から音高を決める）は既存技術であり、そこに新規性を置けないことを明確にするために引用が必要である。現在の論文はこの文献を引用していない。

### 14. Let It Rip! Using Velcro for Acoustic Labeling

- 著者: Tzu-Sheng Kuo, Eric Rawn
- 発表: Adjunct Publication of the 33rd Annual ACM Symposium on User Interface Software and Technology (UIST '20 Adjunct), pp. 28–30, 2020年
- 確認先: 著者本人が公開する本文PDF <https://www.ericrawn.media/assets/blog/publications/velcro/3379350.3416175.pdf>（本文全体を取得して読んだ。第1ページの柱に "Poster Session, UIST '20 Adjunct, October 20-23, 2020, Virtual Event, USA" とあり、頁下端に28が印字されている）および DOI 書誌レコード <https://doi.org/10.1145/3379350.3416175>

内容の要約を述べる。市販の面ファスナーを異なる形に切り出してラベルを作り、二枚を剥がすときに生じる音の違いで、どのラベルが剥がされたかを分類する。中心となる集合（core set）、リング状の集合（ring set）、文字の集合（letter set）、数字の集合（number set）という4組それぞれ3種類のラベルで評価し、精度はそれぞれ82パーセント、70パーセント、68パーセント、60パーセントであった。録音は2019年式のノート型計算機の内蔵マイクロホンを48キロヘルツで用いている。机や壁から物が持ち去られたことを検知する応用として、6種類のラベルを付けた6個の物（コップ、ミント、鏡、靴下、レンチ、巻尺）で実演している。著者ら自身が初期段階の試作と位置づけている。

CipherFlute との関係を述べる。電源も電子部品も持たない安価な物体を、人の動作で鳴らして識別するという受動音響ラベルの一例である。1組あたり3種類という語彙の小ささが際立ち、符号設計も誤り訂正も秘密情報の視点もない。

脅威の度合いは「中」である。理由を述べる。剥がすという動作まで含めて受動音響タグの設計空間が探索されていることを示す文献であり、CipherFlute が「吹く」を選んだ理由を述べるうえで対比材料になる。ただし単体では CipherFlute の主張を脅かさない。

### 15. Randomized resonant metamaterials for single-sensor identification of elastic vibrations

- 著者: Tianxi Jiang, Chong Li, Qingbo He, Zhi-Ke Peng
- 発表: Nature Communications, 第11巻第1号, 論文番号2353, 2020年
- 確認先: 出版社の全文ページ <https://www.nature.com/articles/s41467-020-15950-1>、公開されている本文PDF <https://www.nature.com/articles/s41467-020-15950-1.pdf>、および Crossref の書誌レコード <https://api.crossref.org/works/10.1038/s41467-020-15950-1>（論文番号2353をここで確認した）

内容の要約を述べる。局所共振子をランダムに結合させたメタマテリアルを設計し、空間的な振動情報を物理的に符号化する。要旨は機構を「局所共振子の等価質量が無秩序になることで、振動の伝達特性どうしの相関が著しく低くなる」と述べている。そのおかげで単一のセンサだけで複数の振動源を識別できるようになり、復元は圧縮センシングの枠組みで行う。すなわち圧縮センシングの観測行列を物理構造として実装したものと解釈できる。構造は再構成が可能で、再構成しても性能が保たれると述べている。

CipherFlute との関係を述べる。共振構造の設計によって物理的に情報を符号化するという発想が共通する。ただし目的は振動源の識別であって、物体に固定的なビット列を格納することではない。誤り訂正や秘密情報の視点はない。

脅威の度合いは「中」である。理由を述べる。音響メタマテリアルによる受動的な符号化という文脈で、CipherFlute の「共鳴器の設計で情報を運ぶ」という主張が物理分野では既知の枠組みであることを示す。背景として引用しておくと、分野の目配りを示せる。

---

## 背景として押さえるべき文献

以下は脅威の度合いが「低」であり、背景として引用する程度でよいと判断したものである。いずれも書誌情報を Crossref の書誌レコード（`https://api.crossref.org/works/<DOI>`）で一件ずつ確認し、巻号・論文番号・頁・年に誤りがあったものは dblp のレコードで裏を取って直した。

**能動音響センシングによる物体・接触の識別**

- Makoto Ono, Buntarou Shizuki, Jiro Tanaka, "Touch & Activate: adding interactivity to existing objects using active acoustic sensing", UIST '13, pp. 31–40, 2013年。<https://doi.org/10.1145/2501988.2501989> 圧電素子で音を送り込み、握り方などによる共振変化を分類する。電源が要る点で CipherFlute とは前提が異なる。
- Shohei Katakura, Keita Watanabe, "ProtoHole: Prototyping Interactive 3D Printed Objects Using Holes and Acoustic Sensing", CHI EA '18, pp. 1–6, 2018年。<https://doi.org/10.1145/3170427.3188471> 造形物の内部に掃引信号を出し、穴をふさいだときの共鳴変化を機械学習で分類する。穴をボタンとして使う点が興味深いが、内部に電子回路を要する。
- Jan Rod, David Collins, Daniel Wessolek, Thavishi Ilandara, Ye Ai, Hyowon Lee, Suranga Nanayakkara, "UTAP - Unique Topographies for Acoustic Propagation: Designing Algorithmic Waveguides for Sensing in Interactive Malleable Interfaces", TEI '17, pp. 141–152, 2017年。<https://doi.org/10.1145/3024969.3024987> 音響導波路の形状を設計して伝搬特性を作り込む。
- Yasha Iravantchi, Yi Zhao, Kenrick Kin, Alanson P. Sample, "SAWSense: Using Surface Acoustic Waves for Surface-bound Event Recognition", CHI '23, pp. 1–18, 2023年。<https://doi.org/10.1145/3544548.3580991>
- Ethan Kepros, Premjeet Chahal, "Ultralow Power Wireless Ultrasonic Sensor Tag With ID", IEEE Sensors Journal, 第25巻第5号, pp. 8823–8827, 2025年。<https://doi.org/10.1109/jsen.2025.3529891> 確認先は Crossref の書誌レコード <https://api.crossref.org/works/10.1109/jsen.2025.3529891> である。超音波タグに識別子を載せる最新の研究であり、Acoustic Barcodes の被引用一覧から拾った。ただし題名が示すとおり「超低消費電力」であって完全な受動素子ではないので、電源も電子部品も持たない CipherFlute とは前提が異なる。本文は IEEE Xplore が自動取得を拒否するため未確認であり、内容の要約はここには書かない。
- 八田将志, 村尾和哉, 「音響と振動のセンシングによる充填率の異なる3Dプリンタ生成物の識別手法」, マルチメディア，分散協調とモバイルシンポジウム2077論文集, 第2020巻, pp. 382–391, 2020年6月17日, 情報処理学会。確認先: 情報処理学会電子図書館のレコード <https://ipsj.ixsq.nii.ac.jp/records/210771> および CiNii Research のレコード <https://cir.nii.ac.jp/crid/1050292572093342336>。収録刊行物名の表記について注意しておく。この「2077」は本調査の誤記ではなく、情報処理学会電子図書館と CiNii Research の双方が同じ文字列で登録している。実体は DICOMO2020 のシンポジウム論文集であるから、論文に引くときは一次レコードの表記をそのまま写すか、あるいは「マルチメディア，分散，協調とモバイル（DICOMO2020）シンポジウム論文集」と正した表記に注記を添えるかを、投稿先の作法に合わせて選ぶべきである。内容は、音響と振動の特性が異なる3Dプリンタ生成物をスマートフォンで叩き、特性の違いから認識して対応するアプリケーションを起動する手法である。11種類の生成物を1,100回叩いて、全体で約81パーセント、最大96パーセントの精度を得たと報告している。この一件は、物体側に電子部品を要さず市販のスマートフォンだけで読めるという点で、この背景群のなかでは CipherFlute にいちばん近い。ただし読み出しは叩打による分類であって、任意のビット列を復元するものではない。

**空気の流れや管を使う3Dプリント物の入力**

- Liang He, Gierad Laput, Eric Brockmeyer, Jon E. Froehlich, "SqueezaPulse: Adding Interactive Input to Fabricated Objects Using Corrugated Tubes and Air Pulses", TEI '17, pp. 341–350, 2017年。<https://doi.org/10.1145/3024969.3024976>
- Valkyrie Savage, Ryan Schmidt, Tovi Grossman, George Fitzmaurice, Björn Hartmann, "A series of tubes: adding interactivity to 3D prints using internal pipes", UIST '14, pp. 3–12, 2014年。<https://doi.org/10.1145/2642918.2647374>
- Carlos E. Tejada, Raf Ramakers, Sebastian Boring, Daniel Ashbrook, "AirTouch: 3D-printed Touch-Sensitive Objects Using Pneumatic Sensing", CHI '20, pp. 1–10, 2020年。<https://doi.org/10.1145/3313831.3376136>
- Valkyrie Savage, Carlos Tejada, Mengyu Zhong, Raf Ramakers, Daniel Ashbrook, Hyunyoung Kim, "AirLogic: Embedding Pneumatic Computation and I/O in 3D Models to Fabricate Electronics-Free Interactive Objects", UIST '22, pp. 1–12, 2022年。<https://doi.org/10.1145/3526113.3545642> 電子部品を使わない対話物体という方向性で Blowhole の系譜に連なる。
- Carlos E. Tejada, Jess McIntosh, Klaes Alexander Bergen, Sebastian Boring, Daniel Ashbrook, Asier Marzo, "EchoTube: Robust Touch Sensing along Flexible Tubes using Waveguided Ultrasound", ISS '19, pp. 147–155, 2019年。<https://doi.org/10.1145/3343055.3359712>

**こする、叩く、揺らすことで生じる音や振動の識別**

- Roderick Murray-Smith, John Williamson, Stephen Hughes, Torben Quaade, "Stane: synthesized surfaces for tactile input", CHI '08, pp. 1299–1302, 2008年。<https://doi.org/10.1145/1357054.1357257> 表面のテクスチャをこすった振動を分類する。Acoustic Barcodes が直接の先行研究として挙げている。
- Ryosuke Kawakatsu, Shigeyuki Hirai, "Rubbinput: An Interaction Technique for Wet Environments Utilizing Squeak Sounds Caused by Finger-Rubbing", PerCom Workshops 2018。<https://doi.org/10.1109/percomw.2018.8480335>
- Taesik Gong, Hyunsung Cho, Bowon Lee, Sung-Ju Lee, "Knocker: Vibroacoustic-based Object Recognition with Smartphones", Proceedings of the ACM on Interactive, Mobile, Wearable and Ubiquitous Technologies, 第3巻第3号, 論文番号82, pp. 82:1–82:21, 2019年。<https://doi.org/10.1145/3351240> 同じ著者らの短報として "Identifying Everyday Objects with a Smartphone Knock", CHI EA '18, pp. 1–6, 2018年、<https://doi.org/10.1145/3170427.3188514> がある。既存の物体を叩いて識別する研究であり、タグを設計する研究ではない。
- Chang Xiao, Karl Bayer, Changxi Zheng, Shree K. Nayar, "Vidgets: modular mechanical widgets for mobile devices", ACM Transactions on Graphics, 第38巻第4号, 論文番号100, pp. 100:1–100:12, 2019年。<https://doi.org/10.1145/3306346.3322943> 機械式部品の非線形応答を加速度センサで読む。音ではないが、受動的な機械式タグの近縁である。
- Aakar Gupta, Jiushan Yang, Ravin Balakrishnan, "Asterisk and Obelisk: Motion Codes for Passive Tagging", UIST '18, pp. 725–736, 2018年。<https://doi.org/10.1145/3242587.3242637> 受動タグに動きの符号を持たせる。音響ではないが「受動タグに符号を設計する」という発想の近縁である。
- Xin Li, Yilin Yang, Zhengkun Ye, Yan Wang, Yingying Chen, "EarCase: Sound Source Localization Leveraging Mini Acoustic Structure Equipped Phone Cases for Hearing-challenged People", MobiHoc '23, pp. 240–249, 2023年。<https://doi.org/10.1145/3565287.3610270> 受動的な音響構造をスマートフォンのケースに付ける点が FluteCase に近い。

**安全性の文脈で音を扱う研究**

- Girish Vaidya, T. V. Prabhakar, Nithish Gnani, Ryan Shah, Shishir Nagaraja, "Sensor Identification via Acoustic Physically Unclonable Function", Digital Threats: Research and Practice, 第4巻第2号, 論文番号20, pp. 20:1–20:25, 2023年（オンライン先行公開は2022年3月15日）。<https://doi.org/10.1145/3488306> 年について注意する。Crossref の書誌レコードはオンライン先行公開の2022年3月15日を発行日として持つが、第4巻第2号という号は2023年のものであり、dblp も2023年として記録している。論文に引くときは2023年とし、必要ならオンライン先行公開の年を添えるのが正確である。製造ばらつきに由来する音響的な個体差を複製困難な指紋として使う。CipherFlute が「物理層に秘匿の力はない」と宣言していることの対極にあり、脅威モデルの議論で対比材料になる。
- Soundarya Ramesh, Harini Ramprasad, Jun Han, "Listen to Your Key: Towards Acoustics-based Physical Key Inference", HotMobile '20, pp. 3–8, 2020年。<https://doi.org/10.1145/3376897.3377853> 鍵を差し込むときの音から鍵山の形状を推定する攻撃である。物理的な秘密が音として漏れるという事実を示しており、CipherFlute の脅威モデル（形状を計測されれば無音で読める、複製も容易）を裏打ちする。
- Soundarya Ramesh, Rui Xiao, Anindya Maiti, Jong Taek Lee, Harini Ramprasad, Ananda Kumar, Murtuza Jadliwala, Jun Han, "Acoustics to the Rescue: Physical Key Inference Attack Revisited", Proceedings of the 30th USENIX Security Symposium (USENIX Security '21), pp. 3255–3272, 2021年。確認先: dblp のレコード <https://dblp.org/search/publ/api?q=Acoustics+to+the+Rescue+Physical+Key+Inference+Attack+Revisited> および USENIX の発表ページ <https://www.usenix.org/conference/usenixsecurity21/presentation/ramesh>。上記 HotMobile 2020 の短報を本格的な攻撃実装へ発展させた続報である。DOI は付与されていない。この続報の存在は、「物理的な秘密は音として漏れる」という CipherFlute の脅威モデルの前提が、査読付きの安全性会議で確立した知見であることを示すので、脅威モデルの節で引くとよい。

---

## 未検証のまま残ったもの

以下は、実在または詳細を確認しきれなかったものである。憶測で書かないために、どこまで確認できたかを明示する。2026年7月30日の検証で決着したものは、この節から外して本文の該当箇所へ移した。

1. **Semantic Scholar 上に "Encoding data into physical objects with digitally fabricated textures"（2013年）という記録がある。** Acoustic Barcodes の被引用一覧に現れたが、掲載誌や会議名も DOI も付いていない。2026年7月30日の検証で、Crossref に該当する書誌が無いことに加えて、計算機科学の書誌データベースである dblp にも該当する記録が1件も無いことを確かめた（`https://dblp.org/search/publ/api?q=Encoding+data+into+physical+objects+with+digitally+fabricated+textures` が0件を返す）。査読を経た公刊文献であればこの二つのどちらかには載るはずなので、学位論文か未公刊の報告である可能性がさらに高まった。実在と書誌を確認できていないため、論文には引用すべきでない。

2. **Semantic Scholar 上に "EchoTube: Modular and Robust Press Sensing along Flexible Tubes using Waveguided Ultrasound"（2019年）という別記録がある。** 2026年7月30日の検証で、dblp には EchoTube という題名の記録が ISS 2019 の "EchoTube: Robust Touch Sensing along Flexible Tubes using Waveguided Ultrasound"（pp. 147–155, DOI 10.1145/3343055.3359712）の1件しか無いことを確かめた。したがってこの "Modular and Robust Press Sensing" 版は Semantic Scholar 側の重複ないし誤登録であると判断してよい。独立した文献としては存在しないものとして扱い、引用しない。

3. **The Journal of the Acoustical Society of America と JASA Express Letters の水中受動音響識別タグ（2020年、2024年）について、本文の技術的細部を確認できていない。** 題名、著者、巻号、頁または論文番号、年は Crossref の書誌レコードで確認したが、出版社サイトが自動取得を拒否したため、識別可能なタグの個数、ビット容量、符号設計の有無、誤り訂正の有無は未確認である。なお同じ系列のうち Journal of Applied Physics の論文（Zhou ら, 2022年）については、著者版の全文が arXiv で公開されていたため本調査で本文まで読み、符号設計を確認して本文の該当箇所に書き足した。

4. **Applied Acoustics の水中音響バーコード（2022年）についても同様である。** 書誌は Crossref で確認したが、本文の符号設計は未確認である。

5. **Advanced Functional Materials の EMIT 論文について、ビット容量と識別可能タグ数と誤り訂正の有無は未確認である。** 題名、著者、掲載誌、巻号、論文番号、年は Crossref の書誌レコードで確認し、要旨の全文は Semantic Scholar 経由で取得して読んだが、本文は購読が必要であり読めていない。要旨には識別可能なタグ数もビット数も誤り訂正の記述も現れない。

6. **Proceedings of the ACM on Interactive, Mobile, Wearable and Ubiquitous Technologies の SoundOff（2025年）について、発音機構の細部が未確認である。** 書誌（第9巻第4号、論文番号174、pp. 174:1–174:32）と要旨は確認したが、片持ち梁が金属円板を弾くという機構や部品数は要旨に現れず、本文は ACM Digital Library が自動取得を拒否するため読めていない。

7. **Extended Abstracts of the CHI Conference の FabAuth（2019年）について、加振に用いる素子の種類が未確認である。** 要旨には「振動」「センサ」とあるだけで、圧電素子とは書かれていない。本文は ACM Digital Library が自動取得を拒否するため読めていない。

---

## この切り口で見つからなかったこと

CipherFlute の新規性の根拠になる事項を、丁寧に書き出す。以下はいずれも、上記の調査範囲では該当する先行研究を見つけられなかった。

**その一、100ビットを超える秘密の値そのものを、電源を持たない音響読み出し物体に格納した例が見つからなかった。** 確認できた最大容量を並べると、Acoustic Voxels が実証4ビット、Acoustic Barcodes が誤り訂正込みで12ビットから30ビット（1ミリメートル単位間隔なら約6センチメートルに60ビットまで拡張可能と述べるにとどまる）、水中の受動音響バーコードが実証3ビット（球の組み合わせ7通り）、Blowhole が1物体あたり最大9個のタグ、Lamello がスライダ位置、SoundOff が1タグ1識別子である。表面弾性波タグについては注意が要る。32ビットから128ビットという数字は目標値として語られているものであって、章が書かれた時点の実用品の容量は約1万通り、およそ13ビットにとどまる。しかも無線送受信機を要し、素子は圧電結晶である。CipherFlute の「128ビットのリカバリーシードを40本から49本の笛で運ぶ」という規模は、家庭用3Dプリンタで作れる可聴音の受動タグとしては前例がない。

**その二、音の高さを対数格子（セント等分）で量子化し、多元アルファベットの符号語彙とした例が見つからなかった。** ここは本調査で表現を狭めた項目である。「周波数軸を等間隔の小帯域に区切り、各小帯域を符号の1桁として使う」という設計そのものは、水中の受動音響バーコード（Zhou ら, Journal of Applied Physics, 2022年）に明確に存在する。その論文は帯域幅を m 個の等幅の小帯域に区切り、共鳴ピークがあれば1、無ければ0として白黒のバーコードを作ると述べており、実験では6キロヘルツから10.5キロヘルツを1.5キロヘルツ幅の3小帯域に区切っている。したがって「周波数の格子を符号語彙にした」ことは新規と主張できない。残る新しさは二点である。第一に、格子が線形等間隔ではなく100セント刻みの対数格子であり、音楽の半音と一致していること。第二に、各スロットが共鳴ピークの在無を表す2値ではなく13元のアルファベットの1文字であり、1本あたり約3.7ビットを運ぶことである。Whoosh の FluteCase は管長を半音比の等比数列で決めているが、それは8個のイベントを区別しやすくするためであって、半音を符号の単位（スロット）として定義したものではない。Lamello の櫛歯の周波数は音楽的な格子上にはない。Blowhole はヘルムホルツ式の予測値に最も近い空洞を選ぶ最近傍判定であって、等間隔のセント格子ではない。

**その三、物体の中に基準となる既知の音高を混ぜて、環境変動を「周波数の比」で打ち消す設計が見つからなかった。** ここも本調査で表現を狭めた項目である。「既知の基準要素をタグ自身に混ぜて温度変動を打ち消す」という発想そのものには、はっきりした先行例がある。表面弾性波タグの校正用反射器について、Härmä と Plessky の章は「校正用反射器は、温度、製造ばらつき、その他の変動に由来する位置の誤差を吸収するのに役立つ」と明記している。したがって基準要素という考え方の新規性は主張できない。Acoustic Barcodes のガード列も、3本の溝を単位間隔で並べて、こする速度のばらつきを吸収するための基準を与える。残る差分は二点である。第一に、これらの先行例が打ち消す量は時間軸のスケール（遅延や速度）であるのに対し、CipherFlute が打ち消すのは周波数軸のスケールであること。第二に、打ち消す対象が製造ばらつきと温度だけでなく、吹く息の強さという人間側の変動まで含むことである。周波数軸に基準を置いて全体のずれを比で正規化するという通信のパイロット信号に相当する設計は、受動音響タグの文献には見当たらなかった。

**その四、フィップル（エッジトーン）方式の笛を受動音響タグに使った例が見つからなかった。** 確認できた励起方式は、ヘルムホルツ共鳴器に吹き込む方式（Blowhole）、閉管の開口を横切って吹く方式（Whoosh の FluteCase）、櫛歯をはじく方式（Lamello）、突起を打つ方式（Tickers and Talker）、切り欠きをこする方式（Acoustic Barcodes）、面ファスナーを剥がす方式（Let It Rip!）、片持ち梁が金属円板を弾く方式（SoundOff）、音響フィルタに雑音を通すか叩く方式（Acoustic Voxels）である。フィップル笛は音量が大きく音高が安定するという利点があるが、これを識別タグに使った先行研究は見つからなかった。あわせて、円筒を軸方向に半分に割った断面の笛を、サポート材なしで平置き印刷し複数本を融合するという造形手法にも先行例が見つからなかった。

**その五、Reed–Solomon 符号を実装した受動音響タグの動作系が見つからなかった。** Acoustic Barcodes はハミング符号、BCH 符号、拡張ゴレイ符号、Reed–Solomon 符号を「使ってよい」と述べ、事後解析としてどれだけの検査ビットが要るか、また訂正込みならどれだけ精度が上がるかを計算しているが、実験に使ったタグ自体には誤り訂正を入れていない（実験に用いた符号はすべて固定物理長方式であり、その理由をスワイプ距離のばらつきによる交絡を避けるためと明記している）。表面弾性波タグにはチェックサム用の反射器があるが、これは誤り検出であって誤り訂正ではない。水中の受動音響バーコードは誤り訂正にまったく触れていない。誤り訂正符号を実装して動く受動音響タグは見つからなかった。

**その六、受動音響タグの文献に、暗号学的な脅威モデルを明示した例が見つからなかった。** 「音や物体の層には秘匿の力がまったく無い」と宣言し、秘匿性を秘密分散にのみ負わせ、物理層の役割を偽装による探索コストの引き上げと正当利用者の手軽さに限定する、という構成の議論は一件も見つからなかった。Blowhole は構造の大半を表面下に隠すが、それは外観を損なわないためであって、攻撃者の探索を難しくするためではない。FabAuth は真正性を扱うが、複製困難性の主張であって秘匿性の議論ではない。音響物理的複製困難関数（acoustic physically unclonable function）は複製困難性を主張する方向であり、CipherFlute の「複製は容易だと認める」という立場と正反対である。

**その七、暗号資産の復元用情報の保管という用途を、受動音響タグで扱った例が見つからなかった。** 音響タグの応用として挙げられているのは、教育用模型の注釈（Blowhole、Tickers and Talker）、視覚障害者向けのラベル（Tickers and Talker）、機器の入力（Lamello、Whoosh、SqueezaPulse）、物品の識別と著作権情報（Acoustic Voxels、Acoustic Barcodes）、家庭内の行動センシング（SoundOff）、水中航法（水中識別タグ）、所有者識別（EMIT）である。秘密情報の物理的な保管という用途は、この系譜には存在しない。

**その八、日用品への偽装を目的として受動音響タグを設計した例が見つからなかった。** Acoustic Barcodes は「表面によっては見えなくできる」と述べ、Blowhole は「目立たない開口」と述べているが、いずれも美観と実装の都合であって、第三者に秘密の存在を悟らせないという安全上の目的ではない。ただしこの項目には一件、留保が必要である。水中の受動音響バーコード（Zhou ら, 2022年）は「情報が対象の音響散乱特性に変調されるので、秘匿的な情報伝送（covert information transmission）と目標識別が実現できる」と明記している。すなわち隠蔽を目的として語る受動音響タグは存在する。もっともその隠蔽は、敵のソナーに標識の存在を悟らせないという軍事寄りの文脈であって、CipherFlute のように「日用品に見せかけて第三者の探索コストを上げる」という設計ではない。査読で偽装の新規性を問われた場合は、この一件を認めたうえで日用品への擬装という設計目標との違いを述べるのが誠実である。

---

## 調べ残した穴

以下は時間と検索回数の都合で追い切れなかった方向である。追加調査の候補として記しておく。

1. **Blowhole の被引用は Semantic Scholar 上で17件しか登録されていない。** Google Scholar の被引用一覧は本調査では参照できなかったため、実際にはもっと多い可能性がある。とくに2023年以降の造形分野の論文で Blowhole を引く新しい研究を取りこぼしているおそれがある。

2. **Acoustic Barcodes の被引用99件のうち、題名から明らかに無関係と判断したものを個別には確認していない。** 一覧そのものは取得済みなので、必要なら追跡できる。とくに次の3件は造形物への情報埋め込みと安全性を扱っており、別の切り口の担当者と重なる可能性がある。2026年7月30日の検証で、いずれも書誌情報を一次情報で確定させたので、正確な形で書き留めておく。本文は未読であるから、内容の要約はここには書かない。

   - Riddhi R. Adhikari, Karim A. ElSayed, Ergun Akleman, Jitesh H. Panchal, Vinayak Krishnamurthy, "SplitCode: Voronoi-based error exaggeration for authentication of manufactured parts", Journal of Manufacturing Systems, 第65巻, pp. 605–621, 2022年。<https://doi.org/10.1016/j.jmsy.2022.10.005> 確認先は Crossref の書誌レコードである。題名の綴りは "SplitCode" であって "Splitcode" ではない。なお同名の先行版が SSRN に2021年付で登録されている（DOI 10.2139/ssrn.3993045）ので、引くときは査読誌版のほうを指すべきである。
   - Canran Wang, Jinwen Wang, Mi Zhou, Vinh Pham, Senyue Hao, Chao Zhou, Ning Zhang, Netanel Raviv, "Secure Information Embedding in Forensic 3D Fingerprinting", Proceedings of the 34th USENIX Security Symposium (USENIX Security '25), pp. 1887–1906, 2025年。確認先は dblp のレコード <https://dblp.org/search/publ/api?q=Secure+Information+Embedding+Forensic+3D+Fingerprinting> および USENIX の発表ページ <https://www.usenix.org/conference/usenixsecurity25/presentation/wang-canran> である。年について訂正しておく。本調査の前に書かれていた「USENIX Security 2024」は誤りで、正しくは2025年である。2024年付で存在するのは題名の異なる arXiv のプレプリント "Secure Information Embedding and Extraction in Forensic 3D Fingerprinting"（arXiv:2403.04918, DOI 10.48550/arXiv.2403.04918）であり、これと会議版を混同したものと考えられる。
   - Choonsung Shin, Sunghee Hong, Hieyong Jeong, Hyoseok Yoon, Byoungsoo Koh, "All-in-one encoder/decoder approach for non-destructive identification of 3D-printed objects", Mathematical Biosciences and Engineering, 2022年。<https://doi.org/10.3934/mbe.2022657> 確認先は Semantic Scholar のレコード（要旨全文を取得した）である。要旨によれば、識別用の一次元符号から三次元バーコードを生成して造形物の STL ファイルの底部の空き領域に埋め込み、テラヘルツ波で検出して符号を取り出す手法である。すなわち読み出しは音響ではなくテラヘルツ波であり、AirCode や InfraStructs の系譜に属する。この切り口ではなく、電磁波で読む埋め込み符号を扱う切り口の担当者に渡すのが適切である。

3. **特許を体系的に検索していない。** 音を使った識別タグは玩具や包装の分野で特許が多い領域と予想される。とくに「吹くと音が出る識別子」に関する特許は、学術文献より先行している可能性がある。

4. **中国語と韓国語の文献を調べていない。** 水中音響バーコードや音響メタマテリアル識別タグの分野は中国と韓国の研究機関が活発であり、英語で発表されていない関連研究がある可能性が高い。

5. **日本語の文献の調査が浅い。** CiNii Research では「音響タグ」「受動的音響センシング」「3Dプリンタ 音響 識別」の3語で検索したにとどまる。2026年7月30日の検証では、八田と村尾の論文について情報処理学会電子図書館のレコードまで当たって書誌を確定させたが、電子情報通信学会の技術研究報告、WISS とインタラクションの各年の予稿集を直接めくる作業は依然として行えていない。とくにヒューマンインタフェース学会と情報処理学会のヒューマンコンピュータインタラクション研究会には、音で読む物体の未発掘の研究がある可能性がある。

6. **玩具、楽器、鳥笛、汽笛といった実用品の先行技術を調べていない。** 「複数の音高を出す受動的な吹奏具」は工業製品として長い歴史があり、学術文献より前に存在する事例があるはずである。とくに犬笛や救難笛の規格、鉄道の汽笛による信号（音高で意味を伝える運用）は、CipherFlute の位置づけを述べるうえで参照価値がある。

7. **超音波の受動タグのうち、医療用インプラントに埋め込む音響識別子の文献を調べていない。** 体内に埋め込んだ受動共振体を超音波で読む研究は医用工学の分野に存在すると予想されるが、今回は探索できなかった。

8. **検索の予算を使い切ったため、最後に予定していた2件の確認ができなかった。** 一つは物理鍵の音響推定攻撃の最新版であり、もう一つは「音で読める秘密の物理バックアップ」という直球の検索である。前者は2026年7月30日の検証で決着し、"Acoustics to the Rescue: Physical Key Inference Attack Revisited"（USENIX Security 2021, pp. 3255–3272）として背景の節に加えた。後者は依然として穴のまま残っている。CipherFlute の新規性の中心に関わるため、優先して埋めるべき穴である。なお本検証の担当者も、この直球の検索に着手する前に Web 検索の予算を使い切ったため、同じ穴を埋められなかった。次に取り組む者は、この検索を最初に回すことを勧める。

---

## 検証の記録

2026年7月30日に、この文書の初稿を書いた調査担当者とは別の担当者が、記載されているすべての書誌情報の実在を独立に確かめ直した。以下にその作業の内容と結果を書く。

確かめた件数は次のとおりである。「新規性への脅威が大きい文献」の節に挙げられた15項目（うち第11項は4件の論文を束ねたもの、第9項と第10項はそれぞれ2件を束ねたものなので、論文の数では20件になる）、「背景として押さえるべき文献」の節に初稿の時点で挙げられていた19件、「未検証のまま残ったもの」の節に挙げられた7項目、「調べ残した穴」の節で名前だけ挙げられていた3件、合わせて49件の書誌を確認の対象とした。

このうち47件については、題名・著者・掲載誌または会議名・巻号・頁または論文番号・年のすべてを一次情報で確定させることができた。確定できなかったのは2件で、いずれも初稿が「未検証のまま残ったもの」の節に置いていたものである（第1項と第2項）。この2件については、公刊文献として実在しない可能性が高いと判定を強めたうえで、同じ節に残した。

なお「書誌を確定できた」ことと「本文の主張を裏づけられた」ことは別である。書誌は確定できても本文が読めず、要旨より細かい技術的主張の裏を取れなかったものが6件ある。SoundOff の発音機構、FabAuth の加振素子、EMIT のビット容量、そして水中タグのうち JASA 系列の2件と Applied Acoustics の1件の符号設計である。これらは何が確認できなかったかを「未検証のまま残ったもの」の節に書き分けた。

確認に用いた一次情報は次のものである。Crossref の書誌レコードには DOI を持つ全件を照会した。ACM の会議録に特有の論文番号や、雑誌の号の情報が Crossref に無い場合は dblp のレコードで補った。要旨は OpenAlex と Semantic Scholar から取得した。さらに、Blowhole（Graphics Interface 2018）、Whoosh（ISWC 2016）、Acoustic Barcodes（UIST 2012）、Lamello（CHI 2015）、Acoustic Voxels（SIGGRAPH 2016）、表面弾性波タグの書籍章（InTech 2009）、Let It Rip!（UIST 2020 Adjunct）、そして水中の受動音響バーコード（Journal of Applied Physics 2022）の著者版という8件については、本文PDFを取得して全文を読み、書かれている数値を一つずつ突き合わせた。日本語の文献については、CiNii Research のレコードと情報処理学会電子図書館のレコードの両方に当たった。

実在しないと判断して削除した文献は一件も無い。したがって「検証で削除したもの」という節は設けていない。ただし「未検証のまま残ったもの」の第1項と第2項の2件については、Crossref と dblp の両方に記録が無いことを確かめたので、公刊文献としては存在しない可能性が高いと判定を強めた。とくに第2項の EchoTube の別題名版は、dblp に EchoTube という題名の記録が ISS 2019 版の1件しか無いことから、書誌データベース側の重複登録であると結論した。

訂正した箇所は次の12件である。

第一に、Acoustic Barcodes の認識精度の読み違いを直した。初稿は「最良の入力方法で87.4パーセント、全体平均で66.4パーセント」と書いていたが、原典を読むと66.4パーセントは3つの入力方法のうち最下位である白板用マーカーの数値であって、全体平均ではない。携帯電話が87.4パーセント、爪が77.9パーセント、白板用マーカーが66.4パーセントである。誤り訂正を含めた場合の推定値93.1パーセント、87.4パーセント、77.3パーセントも書き足した。

第二に、Acoustic Barcodes の誤り訂正符号の対応を直した。24ビット符号に使うと述べられているのは拡張ゴレイ符号であって BCH 符号ではない。6ビット符号に切り詰めた(7,4)ハミング符号の記述も抜けていたので補った。

第三に、Acoustic Voxels の「各個体は10個以上のピークを持つ」という記述を訂正した。10個を超えるピークを最適化したと書かれているのは、アヒル型の浮き輪 BOB についてであって、音響タグの実例である豚の置物3体ではない。豚の置物のピークは各3本であり、その周波数も本文から書き写した。

第四に、表面弾性波タグの反射器の役割を直した。初稿は「10個の反射器を符号に使い、最初と最後の反射器は基準とチェックサムの作成に充てている」と書いていたが、原典は反射器14個のうち10個を符号に、最初と最後の1個ずつを校正に、最後の1個の手前に並ぶ2個をチェックサムに充てると述べている。校正用とチェックサム用は別の反射器である。

第五に、表面弾性波タグの「反射器1個あたり4つの位置」という記述を直した。時間位置符号化で1個の反射器が取りうる位置は十進法の10通りであり、4つの状態を取るのは位相符号化のほうである。あわせて、市販品の容量が約1万通り（およそ13ビット）にとどまり、32ビットから128ビットは目標値であることを明記した。この訂正は「その一」の容量の一覧にも反映した。

第六に、Printone の「歌口や指孔の配置も自動で行える」という記述を削除した。要旨にそのような主張は無く、むしろ歌口からの結合振動の励起は明示的に無視すると書かれている。かわりに、境界要素法と最小固有値問題による共鳴周波数の推定という実際の手法を書いた。

第七に、Lamello の名称の由来から「親指ピアノなど」という語を落とした。原典は「長さの異なる舌状の部品が振動して音を出すラメロフォン族の楽器から採った」と書いているだけで、個々の楽器名は挙げていない。

第八に、Whoosh の着想の由来を弱めた。初稿は「ギリシャのパンフルートに着想を得たと明記している」と書いていたが、原典は閉管楽器の構造に着想を得たと述べ、その例としてパンフルートを挙げているにすぎない。あわせて、管長の式を半音比の等比数列と読むと8本の管長は約1.5倍しか動かないので、8つの音高は2キロヘルツから10キロヘルツの帯域を張るのではなく帯域の内側に収まると読むべきであることを、数値の根拠とともに書き添えた。

第九に、Digital Threats: Research and Practice の音響的複製困難関数の論文の年を2022年から2023年に直した。第4巻第2号という号は2023年のものであり、2022年3月15日はオンライン先行公開の日付である。あわせて論文番号20と号の情報を補った。

第十に、日本語の文献の収録刊行物名を、情報処理学会電子図書館と CiNii Research が実際に登録している表記に合わせた。両者は揃って「マルチメディア，分散協調とモバイルシンポジウム2077論文集」と記録している。実体は DICOMO2020 の論文集であるから、この「2077」が一次レコード側の異常であることを注記として添えた。査読者が確認しに行ったときに食い違わないようにするためである。

第十一に、水中の受動音響識別タグの項を大きく書き足した。Journal of Applied Physics の論文は著者版の全文が arXiv で公開されていたので本文まで読むことができ、初稿が「符号語彙の設計や誤り訂正は見当たらない」と書いていた部分のうち、符号語彙については事実と異なることが分かった。この論文は帯域幅を等幅の小帯域に区切り、共鳴ピークの在無で1と0を表す二進バーコードを明確に設計しており、実験では6キロヘルツから10.5キロヘルツを1.5キロヘルツ幅の3小帯域に区切って7通りの組み合わせ、すなわち3ビットを実証している。この事実は CipherFlute の新規性の主張に直接影響するので、「その二」の項目を「周波数の格子を符号語彙にしたこと」から「セント等分の対数格子と13元アルファベットであること」へと狭めて書き直した。同じ論文が「秘匿的な情報伝送」を目的として挙げていることも、「その八」の項目に留保として書き加えた。

第十二に、「調べ残した穴」の節で名前だけ挙げられていた文献のうち、"Secure Information Embedding in Forensic 3D Fingerprinting" の発表年を USENIX Security 2024 から2025年に直した。2024年付で存在するのは題名の異なる arXiv のプレプリントである。あわせて SplitCode の綴りと掲載誌、および "All-in-one encoder/decoder approach" の掲載誌を確定させ、後者が音響ではなくテラヘルツ波で読む手法であることを明記した。

このほか、実在の可否には関わらないが査読での照合のしやすさに関わる補いとして、次の作業を行った。Acoustic Voxels、Printone、Vidgets、Knocker、SoundOff、Nature Communications の論文、Advanced Functional Materials の論文について、欠けていた論文番号または号を dblp と Crossref から補った。Blowhole については、初稿が挙げていた予稿集ページの URL が現在は ACM Digital Library へ転送されて内容を返さないこと、また DOI が Crossref に登録されていないことを確かめ、書誌の裏取りは学会が公開している本文PDFで行ったことを明記した。表面弾性波タグの書籍章については、出版社の頁が表示する DOI 10.5772/6032 が別の章に解決してしまうことを確かめたので、この DOI を引かないよう警告を書いた。書籍の編者名と ISBN と頁範囲は本文PDF末尾の引用案内から採った。

最後に、検証で新たに確定させた文献を2件、背景の節に加えた。一つは "Acoustics to the Rescue: Physical Key Inference Attack Revisited"（USENIX Security 2021, pp. 3255–3272）であり、これは「未検証のまま残ったもの」の第7項として挙げられていたものである。もう一つは "Ultralow Power Wireless Ultrasonic Sensor Tag With ID"（IEEE Sensors Journal, 第25巻第5号, pp. 8823–8827, 2025年）であり、これは第6項として挙げられていたものである。後者は完全な受動素子ではなく超低消費電力の能動素子であるから、脅威の度合いは低いと判断した。

残る不確かさを正直に書いておく。第一に、ACM Digital Library と IEEE Xplore と Wiley Online Library と AIP Publishing は自動取得を拒否するので、これらにしか本文が無い文献については、要旨より細かい技術的主張を独立に裏づけられていない。具体的には SoundOff の発音機構、FabAuth の加振素子、EMIT のビット容量、JASA と Applied Acoustics の水中タグの符号設計である。これらは「未検証のまま残ったもの」の節に列挙した。第二に、Whoosh の管長の式は本文PDFから抽出した文字列が指数表記を失っているため、半音比の等比数列という読み方には一段の解釈が入っている。組版された数式そのものを目で見て確認する作業は、この環境に PDF を画像として描き出す手段が無かったためできなかった。第三に、表面弾性波タグの章の著者 S. Härmä の given name が Sanna であることを一次資料で確認できなかったので、頭文字のままにした。第四に、本検証でも Web 検索の予算を使い切ったため、「音で読める秘密の物理バックアップ」という直球の検索は行えていない。これは CipherFlute の新規性の中心に関わる穴であり、次に取り組む者が最初に埋めるべきである。
