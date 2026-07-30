# 受動的な音響タグと音で読む物体

本稿は CipherFlute（電源を持たない3Dプリント笛を日用品に埋め込み、吹いた音の高さを符号として秘密情報を読み出す手法）の新規性を確かめるために、「電源を持たない物体を音や振動で識別・読み出しする研究」を洗い直したものである。調査は2026年7月30日に実施した。

書誌情報の確認方法について先に断っておく。ACM Digital Library と IEEE Xplore と AIP Publishing と Wiley Online Library は自動取得を拒否したため、これらに掲載された文献については、著者本人が公開している論文PDF、学会の予稿集ページ、または DOI 登録機関である Crossref が保持する書誌レコード（`https://api.crossref.org/works/<DOI>`）で確認した。Crossref の書誌レコードは出版社が DOI 登録時に届け出た一次的な書誌情報であり、題名・著者・掲載誌・巻号ページ・年をそこで確認できたものは「確認済み」として扱った。本文の技術的内容まで一次資料で読めたものと、書誌だけ確認できたものは、本文中で区別して書いた。

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
- 八田将志, 村尾和哉, 「音響と振動のセンシングによる充填率の異なる3Dプリンタ生成物の識別手法」, マルチメディア，分散協調とモバイルシンポジウム2020論文集, pp. 382–391, 2020年。<https://cir.nii.ac.jp/crid/1050292572093342336> 充填率の違う造形物を音響と振動で識別する日本語の先行研究である。

**空気の流れや管を使う3Dプリント物の入力**

- Liang He, Gierad Laput, Eric Brockmeyer, Jon E. Froehlich, "SqueezaPulse: Adding Interactive Input to Fabricated Objects Using Corrugated Tubes and Air Pulses", TEI '17, pp. 341–350, 2017年。<https://doi.org/10.1145/3024969.3024976>
- Valkyrie Savage, Ryan Schmidt, Tovi Grossman, George Fitzmaurice, Björn Hartmann, "A series of tubes: adding interactivity to 3D prints using internal pipes", UIST '14, pp. 3–12, 2014年。<https://doi.org/10.1145/2642918.2647374>
- Carlos E. Tejada, Raf Ramakers, Sebastian Boring, Daniel Ashbrook, "AirTouch: 3D-printed Touch-Sensitive Objects Using Pneumatic Sensing", CHI '20, 2020年。<https://doi.org/10.1145/3313831.3376136>
- Valkyrie Savage, Carlos Tejada, Mengyu Zhong, Raf Ramakers, Daniel Ashbrook, Hyunyoung Kim, "AirLogic: Embedding Pneumatic Computation and I/O in 3D Models to Fabricate Electronics-Free Interactive Objects", UIST '22, pp. 1–12, 2022年。<https://doi.org/10.1145/3526113.3545642> 電子部品を使わない対話物体という方向性で Blowhole の系譜に連なる。
- Carlos E. Tejada, Jess McIntosh, Klaes Alexander Bergen, Sebastian Boring, Daniel Ashbrook, Asier Marzo, "EchoTube: Robust Touch Sensing along Flexible Tubes using Waveguided Ultrasound", ISS '19, pp. 147–155, 2019年。<https://doi.org/10.1145/3343055.3359712>

**こする、叩く、揺らすことで生じる音や振動の識別**

- Roderick Murray-Smith, John Williamson, Stephen Hughes, Torben Quaade, "Stane: synthesized surfaces for tactile input", CHI '08, pp. 1299–1302, 2008年。<https://doi.org/10.1145/1357054.1357257> 表面のテクスチャをこすった振動を分類する。Acoustic Barcodes が直接の先行研究として挙げている。
- Ryosuke Kawakatsu, Shigeyuki Hirai, "Rubbinput: An Interaction Technique for Wet Environments Utilizing Squeak Sounds Caused by Finger-Rubbing", PerCom Workshops 2018。<https://doi.org/10.1109/percomw.2018.8480335>
- Taesik Gong, Hyunsung Cho, Bowon Lee, Sung-Ju Lee, "Knocker: Vibroacoustic-based Object Recognition with Smartphones", Proceedings of the ACM on IMWUT, 第3巻, pp. 1–21, 2019年。<https://doi.org/10.1145/3351240> 同じ著者らの短報として "Identifying Everyday Objects with a Smartphone Knock", CHI EA '18, pp. 1–6, 2018年、<https://doi.org/10.1145/3170427.3188514> がある。既存の物体を叩いて識別する研究であり、タグを設計する研究ではない。
- Chang Xiao, Karl Bayer, Changxi Zheng, Shree K. Nayar, "Vidgets: modular mechanical widgets for mobile devices", ACM Transactions on Graphics, 第38巻, pp. 1–12, 2019年。<https://doi.org/10.1145/3306346.3322943> 機械式部品の非線形応答を加速度センサで読む。音ではないが、受動的な機械式タグの近縁である。
- Aakar Gupta, Jiushan Yang, Ravin Balakrishnan, "Asterisk and Obelisk: Motion Codes for Passive Tagging", UIST '18, pp. 725–736, 2018年。<https://doi.org/10.1145/3242587.3242637> 受動タグに動きの符号を持たせる。音響ではないが「受動タグに符号を設計する」という発想の近縁である。
- Xin Li, Yilin Yang, Zhengkun Ye, Yan Wang, Yingying Chen, "EarCase: Sound Source Localization Leveraging Mini Acoustic Structure Equipped Phone Cases for Hearing-challenged People", MobiHoc '23, pp. 240–249, 2023年。<https://doi.org/10.1145/3565287.3610270> 受動的な音響構造をスマートフォンのケースに付ける点が FluteCase に近い。

**安全性の文脈で音を扱う研究**

- Girish Vaidya, T. V. Prabhakar, Nithish Gnani, Ryan Shah, Shishir Nagaraja, "Sensor Identification via Acoustic Physically Unclonable Function", Digital Threats: Research and Practice, 第4巻, pp. 1–25, 2022年。<https://doi.org/10.1145/3488306> 製造ばらつきに由来する音響的な個体差を複製困難な指紋として使う。CipherFlute が「物理層に秘匿の力はない」と宣言していることの対極にあり、脅威モデルの議論で対比材料になる。
- Soundarya Ramesh, Harini Ramprasad, Jun Han, "Listen to Your Key: Towards Acoustics-based Physical Key Inference", HotMobile '20, pp. 3–8, 2020年。<https://doi.org/10.1145/3376897.3377853> 鍵を差し込むときの音から鍵山の形状を推定する攻撃である。物理的な秘密が音として漏れるという事実を示しており、CipherFlute の脅威モデル（形状を計測されれば無音で読める、複製も容易）を裏打ちする。

---

## 未検証のまま残ったもの

以下は、実在または詳細を確認しきれなかったものである。憶測で書かないために、どこまで確認できたかを明示する。

1. **Semantic Scholar 上に "Encoding data into physical objects with digitally fabricated textures"（2013年）という記録がある。** Acoustic Barcodes の被引用一覧に現れたが、掲載誌や会議名も DOI も付いておらず、Crossref で該当する書誌を見つけられなかった。学位論文か未公刊の報告である可能性が高い。実在を確認できていないため、論文には引用すべきでない。

2. **Semantic Scholar 上に "EchoTube: Modular and Robust Press Sensing along Flexible Tubes using Waveguided Ultrasound"（2019年）という別記録がある。** ISS 2019 版の重複記録である可能性が高いが、独立した文献として実在するかは確認できなかった。

3. **Journal of the Acoustical Society of America の水中受動音響識別タグ（2020年、2024年）について、本文の技術的細部を確認できていない。** 題名、著者、巻号ページ、年は DOI 書誌レコードで確認したが、出版社サイトが自動取得を拒否したため、識別可能なタグの個数、ビット容量、符号設計の有無、誤り訂正の有無は未確認である。

4. **Applied Acoustics の水中音響バーコード（2022年）についても同様である。** 書誌は確認したが、本文の符号設計は未確認である。

5. **Advanced Functional Materials の EMIT 論文について、ビット容量と識別可能タグ数と誤り訂正の有無は未確認である。** 題名、著者、掲載誌、年、要旨は DOI に紐づく書誌情報として確認したが、本文は購読が必要であり読めていない。

6. **IEEE Sensors Journal の "Ultralow Power Wireless Ultrasonic Sensor Tag With ID"（2025年）は書誌を確認していない。** Acoustic Barcodes の被引用一覧に現れたが、追跡する前に検索の予算を使い切った。超音波タグに識別子を載せる研究であり、追加調査の価値がある。

7. **鍵の音響推定攻撃について、HotMobile 2020 版は確認したが、USENIX Security 2021 の "Acoustics to the Rescue: Physical Key Inference Attack Revisited" は書誌を確認できていない。** 被引用一覧に題名が現れたのみである。

---

## この切り口で見つからなかったこと

CipherFlute の新規性の根拠になる事項を、丁寧に書き出す。以下はいずれも、上記の調査範囲では該当する先行研究を見つけられなかった。

**その一、100ビットを超える秘密の値そのものを、電源を持たない音響読み出し物体に格納した例が見つからなかった。** 確認できた最大容量を並べると、Acoustic Voxels が実証4ビット、Acoustic Barcodes が誤り訂正込みで12ビットから30ビット（1ミリメートル単位間隔なら60ビットまで拡張可能と述べるにとどまる）、表面弾性波タグが32ビットから128ビット（ただし無線送受信機を要し圧電結晶製である）、Blowhole が1物体あたり9通り、Lamello がスライダ位置、SoundOff が1タグ1識別子である。CipherFlute の「128ビットのリカバリーシードを40本から49本の笛で運ぶ」という規模は、家庭用3Dプリンタで作れる可聴音の受動タグとしては前例がない。

**その二、音高を半音格子で量子化して符号語彙とした例が見つからなかった。** Whoosh の FluteCase は管長を半音比の等比数列で決めているが、それは8個のイベントを区別しやすくするためであって、半音を符号の単位（スロット）として定義したものではない。Lamello の櫛歯の周波数は音楽的な格子上にはない。Blowhole はヘルムホルツ式の予測値に最も近い空洞を選ぶ最近傍判定であって、等間隔のセント格子ではない。CipherFlute の「100セント刻みで13スロット、1本あたり約3.7ビット」という語彙定義は、この分野に前例がない。

**その三、物体の中に基準となる既知の音高を混ぜて、環境変動を比で打ち消す設計が見つからなかった。** 最も近いのは Acoustic Barcodes のガード列であり、これは3本の溝を単位間隔で並べて、こする速度のばらつきを吸収するための基準を与える。ただし打ち消す対象は速度であって温度や息の強さではなく、また基準は時間軸のスケールであって周波数軸のスケールではない。表面弾性波タグにも基準用の反射器があるが、これも遅延の基準である。周波数軸に基準を置いて全体のずれを比で正規化するという通信のパイロット信号に相当する設計は、受動音響タグの文献には見当たらなかった。

**その四、フィップル（エッジトーン）方式の笛を受動音響タグに使った例が見つからなかった。** 確認できた励起方式は、ヘルムホルツ共鳴器に吹き込む方式（Blowhole）、閉管の開口を横切って吹く方式（Whoosh の FluteCase）、櫛歯をはじく方式（Lamello）、突起を打つ方式（Tickers and Talker）、切り欠きをこする方式（Acoustic Barcodes）、面ファスナーを剥がす方式（Let It Rip!）、片持ち梁が金属円板を弾く方式（SoundOff）、音響フィルタに雑音を通すか叩く方式（Acoustic Voxels）である。フィップル笛は音量が大きく音高が安定するという利点があるが、これを識別タグに使った先行研究は見つからなかった。あわせて、円筒を軸方向に半分に割った断面の笛を、サポート材なしで平置き印刷し複数本を融合するという造形手法にも先行例が見つからなかった。

**その五、Reed–Solomon 符号を実装した受動音響タグの動作系が見つからなかった。** Acoustic Barcodes は Hamming 符号、BCH 符号、Reed–Solomon 符号を「使ってよい」と述べ、事後解析としてどれだけの検査ビットが要るかを計算しているが、実験に使ったタグ自体には誤り訂正を入れていない（比較を単純にするため固定物理長方式のみを使ったと明記している）。表面弾性波タグにはチェックサム用の反射器があるが、これは誤り検出であって誤り訂正ではない。誤り訂正符号を実装して動く受動音響タグは見つからなかった。

**その六、受動音響タグの文献に、暗号学的な脅威モデルを明示した例が見つからなかった。** 「音や物体の層には秘匿の力がまったく無い」と宣言し、秘匿性を秘密分散にのみ負わせ、物理層の役割を偽装による探索コストの引き上げと正当利用者の手軽さに限定する、という構成の議論は一件も見つからなかった。Blowhole は構造の大半を表面下に隠すが、それは外観を損なわないためであって、攻撃者の探索を難しくするためではない。FabAuth は真正性を扱うが、複製困難性の主張であって秘匿性の議論ではない。音響物理的複製困難関数（acoustic physically unclonable function）は複製困難性を主張する方向であり、CipherFlute の「複製は容易だと認める」という立場と正反対である。

**その七、暗号資産の復元用情報の保管という用途を、受動音響タグで扱った例が見つからなかった。** 音響タグの応用として挙げられているのは、教育用模型の注釈（Blowhole、Tickers and Talker）、視覚障害者向けのラベル（Tickers and Talker）、機器の入力（Lamello、Whoosh、SqueezaPulse）、物品の識別と著作権情報（Acoustic Voxels、Acoustic Barcodes）、家庭内の行動センシング（SoundOff）、水中航法（水中識別タグ）、所有者識別（EMIT）である。秘密情報の物理的な保管という用途は、この系譜には存在しない。

**その八、日用品への偽装を目的として受動音響タグを設計した例が見つからなかった。** Acoustic Barcodes は「表面によっては見えなくできる」と述べ、Blowhole は「目立たない開口」と述べているが、いずれも美観と実装の都合であって、第三者に秘密の存在を悟らせないという安全上の目的ではない。

---

## 調べ残した穴

以下は時間と検索回数の都合で追い切れなかった方向である。追加調査の候補として記しておく。

1. **Blowhole の被引用は Semantic Scholar 上で17件しか登録されていない。** Google Scholar の被引用一覧は本調査では参照できなかったため、実際にはもっと多い可能性がある。とくに2023年以降の造形分野の論文で Blowhole を引く新しい研究を取りこぼしているおそれがある。

2. **Acoustic Barcodes の被引用99件のうち、題名から明らかに無関係と判断したものを個別には確認していない。** 一覧そのものは取得済みなので、必要なら追跡できる。とくに "Splitcode: Voronoi-Based Error Exaggeration for Authentication of Manufactured Parts"（2022年）、"Secure Information Embedding in Forensic 3D Fingerprinting"（USENIX Security 2024）、"All-in-one encoder/decoder approach for non-destructive identification of 3D-printed objects"（2022年）は、造形物への情報埋め込みと安全性を扱っており、別の切り口の担当者と重なる可能性がある。

3. **特許を体系的に検索していない。** 音を使った識別タグは玩具や包装の分野で特許が多い領域と予想される。とくに「吹くと音が出る識別子」に関する特許は、学術文献より先行している可能性がある。

4. **中国語と韓国語の文献を調べていない。** 水中音響バーコードや音響メタマテリアル識別タグの分野は中国と韓国の研究機関が活発であり、英語で発表されていない関連研究がある可能性が高い。

5. **日本語の文献の調査が浅い。** CiNii Research では「音響タグ」「受動的音響センシング」「3Dプリンタ 音響 識別」の3語で検索したにとどまる。情報処理学会電子図書館、電子情報通信学会の技術研究報告、WISS とインタラクションの各年の予稿集を直接めくる作業は行えていない。とくにヒューマンインタフェース学会と情報処理学会のヒューマンコンピュータインタラクション研究会には、音で読む物体の未発掘の研究がある可能性がある。

6. **玩具、楽器、鳥笛、汽笛といった実用品の先行技術を調べていない。** 「複数の音高を出す受動的な吹奏具」は工業製品として長い歴史があり、学術文献より前に存在する事例があるはずである。とくに犬笛や救難笛の規格、鉄道の汽笛による信号（音高で意味を伝える運用）は、CipherFlute の位置づけを述べるうえで参照価値がある。

7. **超音波の受動タグのうち、医療用インプラントに埋め込む音響識別子の文献を調べていない。** 体内に埋め込んだ受動共振体を超音波で読む研究は医用工学の分野に存在すると予想されるが、今回は探索できなかった。

8. **検索の予算を使い切ったため、最後に予定していた2件の確認ができなかった。** 一つは物理鍵の音響推定攻撃の最新版であり、もう一つは「音で読める秘密の物理バックアップ」という直球の検索である。後者は CipherFlute の新規性の中心に関わるため、優先して埋めるべき穴である。
