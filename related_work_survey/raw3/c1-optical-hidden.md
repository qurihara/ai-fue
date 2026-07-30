# 反例検証：「隠蔽と可読性の両立は光学符号には原理的に得られない」は成立するか

対象となる主張（CipherFlute側）
- 主張A：符号を担体の外観にまったく現さずに機械可読に保てる。光学的な符号は表面に露出していなければ読めないため日用品に埋めると読めなくなるが、共鳴管は物体の内部空洞として存在でき、外部に必要なのは窓と吸込口という小さな開口だけである。この隠蔽と可読性の両立は光学符号には原理的に得られない構造的な差である。
- 主張B：既知の値を持つ基準素子を同じ物体に同居させ、比で読んで環境変動を打ち消すという構造的な自己補正は、造形物への情報埋め込みの文脈で前例がない。

評価者の反論
- AirCodeは符号を表面下の空隙として埋め、通常照明下では外観を変えず、投影と撮影で機械可読にしている。
- InfraredTagsは肉眼では見えない内部のQRコードやArUcoマーカーを低価格の近赤外カメラで最大250センチメートルから読む。
- したがって「符号が表面に露出していなければ光学的に読めない」という前提自体が偽である。

結論を先に書く。**この反論は正しい。** 主張Aのうち「光学的な符号は表面に露出していなければ読めない」という前提は、一次資料に当たると成り立たない。したがって「隠蔽と可読性の両立は光学符号には原理的に得られない」という主張Aは撤回する必要がある。ただし、両方式には材料と読み取り装置に関する強い制約があり、そこにCipherFluteとの差分が残る。以下、一次資料の記述で確認した内容を順に書く。

---

## 1. 書誌の確認

### AirCode

| 項目 | 内容 |
| --- | --- |
| 題名 | AirCode: Unobtrusive Physical Tags for Digital Fabrication |
| 著者 | Dingzeyu Li, Avinash S. Nair, Shree K. Nayar, Changxi Zheng（Columbia University） |
| 会議 | Proceedings of the 30th Annual ACM Symposium on User Interface Software and Technology（UIST 2017） |
| 年・ページ | 2017年、449〜460ページ |
| DOI | 10.1145/3126594.3126635 |

確認先
- Crossref（DOIの解決先）：https://api.crossref.org/works/10.1145/3126594.3126635
- DBLP：https://dblp.org/search/publ/api?q=AirCode%20Unobtrusive%20Physical%20Tags&format=json
- 著者公開版（arXiv、本文と補足資料を含む）：https://arxiv.org/abs/1707.05754 および https://arxiv.org/pdf/1707.05754

以下の引用はすべてarXiv版（1707.05754v2）の本文から取った。arXiv版の1ページ目に `DOI: https://doi.org/10.1145/3126594.3126635` が印字されており、UIST 2017版と同一の原稿であると判断した。なお、ACM Digital Libraryの本文ページは取得時にHTTP 403を返したため、出版社ページ本体は読めていない。

### InfraredTags

| 項目 | 内容 |
| --- | --- |
| 題名 | InfraredTags: Embedding Invisible AR Markers and Barcodes Using Low-Cost, Infrared-Based 3D Printing and Imaging Tools |
| 著者 | Mustafa Doga Dogan, Ahmad Taka, Michael Lu, Yunyi Zhu, Akshat Kumar, Aakar Gupta, Stefanie Mueller（Aakar Guptaのみ Facebook Reality Labs、他はMIT CSAIL） |
| 会議 | CHI Conference on Human Factors in Computing Systems（CHI '22）、2022年4月29日〜5月5日、New Orleans |
| 論文番号・ページ | Article 269、12ページ |
| DOI | 10.1145/3491102.3501951 |

確認先
- DBLP：https://dblp.org/search/publ/api?q=InfraredTags+Embedding+Invisible+AR+Markers&format=json
- 著者公開版（MIT CSAIL HCI Engineering Group）：https://hcie.csail.mit.edu/research/infraredtags/infraredtags.html
- 本文PDF：https://groups.csail.mit.edu/hcie/files/research-projects/infraredtags/2022-CHI-InfraredTags-paper.pdf

以下の引用はこの著者公開版PDFから取った。

---

## 2. AirCodeのタグは肉眼で見えないのか

### 論文が外観について述べていること

見えないと明言している。原文をそのまま引く（訳は筆者による）。

図1のキャプション（1ページ目）
> "An AirCode tag is embedded inside the object, without changing its geometry or appearance. (d) The fabricated tag is invisible under environmental lighting."

（AirCodeタグは物体の内部に埋め込まれ、その形状も外観も変えない。(d) 製造されたタグは環境光の下では見えない。）

概要
> "the air pockets affect only the scattering light transport under the surface, and thus are hard to notice to our naked eyes. But, by using a computational imaging method, the tags become detectable."

（空気ポケットは表面下の散乱光輸送だけに影響するので、肉眼では気づきにくい。しかし計算撮像の手法を使えば、タグは検出可能になる。）

不可視性を数値で担保している箇所（Human Vision Sensitivityの節）
> "Exploiting the results of [2], we choose air pocket size and depth such that the resulting contrast (or the change of surface radiosity) is within 5%. This way, by construction the air pockets are invisible to the human eye"

（[2]の結果を利用し、生じるコントラスト（すなわち表面放射輝度の変化）が5%以内になるように空気ポケットの大きさと深さを選ぶ。こうすることで、構成上、空気ポケットは人間の目には見えないものになる。）

ここでいう5%は、Bijlらの心理物理実験で示されたガウシアン状のぼやけた斑点に対する人間のコントラスト感度閾値である。論文はさらに、極端な照明下でも見えないままであることを実験で確認したと書いている（補足資料の図18のキャプション）。

> "Under different extreme lighting, the embedded AirCode tags remain invisible. We capture these photos while moving a strong light source around the statue and the mug. The light source we use is a 45W photography light bulb at 6500K."

（さまざまな極端な照明の下でも、埋め込まれたAirCodeタグは見えないままである。これらの写真は、強い光源を彫像とマグカップの周りで動かしながら撮影した。使用した光源は6500Kの45Wの撮影用電球である。）

### 判定

「AirCodeのタグは通常照明下で肉眼に見えない」という評価者の指摘は、論文の記述どおりであり、正しい。

---

## 3. AirCodeの読み出しに何が必要か

### 装置の構成

Fabrication and Imaging Setupの節に明記されている。

> "For global component imaging, we project checkerboard illumination patterns using a Mitsubishi PK20 DLP projector (800×600 resolution). Images were captured using a Point Grey Grasshopper3 monochrome linear camera (2048×1536 resolution). We use a monochrome camera to avoid Bayer demosaicing, as we consider scattering at a single wavelength."

したがって必要なのは、DLPプロジェクタ1台（三菱PK20、800×600）と、モノクロ産業用カメラ1台（Point Grey Grasshopper3、2048×1536）である。さらに次の2つが加わる。

偏光板について（Polarizationの節）
> "We mitigate the negative effect of specular light by placing linear polarizers in front of both the projector and the camera lens [41, 6]. ... we place the two polarizers that are out of phase with each other to maximally eliminate the specular light."

（プロジェクタとカメラレンズの両方の前に直線偏光板を置く。2枚の偏光板は互いに位相をずらして配置し、鏡面反射光を最大限に取り除く。）

波長について（Wavelength Choiceの節）
> "we take advantage of our full control of the projector and illuminate the object with the longest light wavelength, the red light. ... In all of our imaging experiments, we use red light unless otherwise specified."

（プロジェクタを完全に制御できることを活かし、最も長い波長である赤色光で物体を照らす。すべての撮像実験では、特に断らない限り赤色光を使う。）

つまり、プロジェクタとカメラと交差偏光板からなる据え置きの光学ベンチを構成し、赤色の市松模様を何度もずらしながら投影して、NayarらのDirect-Global分離を行う。手に持って向けるだけの装置ではない。

### 撮像にかかる時間

Discussion and Future Workの節に明記されている。

> "the capturing process still takes 3-4 minutes. This is because a checkerboard sweeping takes about 10 seconds. To reduce imaging noise, we take multiple sweeps and average them."

（撮像の処理には依然として3〜4分かかる。市松模様の走査1回に約10秒かかるためである。撮像ノイズを減らすため、複数回の走査を行って平均する。）

さらにノイズ対策として、Fabrication and Imaging Setupの節に次の記述がある。

> "Under low-light, the output from this camera sensor is noisy. We, therefore, averaged 16 images for each projected checkerboard pattern."

（低照度ではこのカメラセンサの出力はノイズが多い。そのため、投影する市松模様1枚ごとに16枚の画像を平均した。）

InfraredTags側もAirCodeの所要時間を表1で「3-4 minutes」と記載しており、2つの一次資料で一致している。

### 物体との距離

**確認できなかった。** 論文には、カメラおよびプロジェクタと物体との距離を示す数値が見当たらない。論文中に出てくる75センチメートルという数値は、カメラの距離ではなく、人間がタグを見るときの標準的な視距離として不可視性の解析に使われたものである。

> "In our problem, an AirCode tag has a size typically around 2cm. When viewed from a normal distance (e.g., around 75cm) away, the view angle spanned by the codes is around 100 min arc."

代わりに論文が示しているのは角度の許容範囲である。

> "Figure 17 shows that our method is able to read the subsurface codes for rotations in the range of [-40, 40] with respect to the camera view direction."

（図17は、カメラの視線方向に対して[-40度, 40度]の範囲の回転であれば表面下の符号を読めることを示している。）

### 必要な照明条件

論文は読み取り時の周囲照度を数値で規定していない。ただし方式上、プロジェクタが投じる構造化光そのものが照明であり、そのうえで低照度でのセンサノイズを16枚平均で潰していると書かれている。したがって、周囲の環境光は制御された（暗めの）状態が前提だと読める。この点は論文が明示的に書いていないので、推測であることを断っておく。

### 材料と製造装置の制約（重要）

AirCodeが機能する条件は、材料が均質で半透明であることに強く依存する。

> "We fabricated objects with subsurface air pocket tags using Stratasys Eden260VS, a PolyJet 3D printer with 16-micron layer accuracy (Z direction) and 200-micron planar accuracy (XY plane). We use a white opaque material (VeroWhitePlus, RGD835) and a water-soluble support material (SUP707)."

限界について、論文自身が次のように書いている。

> "Our analysis assumes that the 3D printing material is largely homogeneous and semitransparent. While this assumption is valid for many 3D printing systems that fabricate with plastic materials, other printers cannot produce nearly homogeneous materials. For example, many fused-deposition modeling (FDM) printers deposit relatively thick filaments, and the printed object is not homogeneous. Moreover, it is a common postprocess to paint the surface of a 3D printed object. While our method can account for semitransparent paint, it will fail if the paint is completely opaque."

（我々の解析は、3Dプリント材料がおおむね均質で半透明であることを仮定している。この仮定はプラスチックで造形する多くの3Dプリント方式では妥当だが、他のプリンタではほぼ均質な材料を作れない。たとえば多くの熱溶解積層方式のプリンタは比較的太いフィラメントを積むため、造形物は均質にならない。さらに、3Dプリント物の表面を塗装するのは一般的な後処理である。半透明の塗料なら我々の手法で扱えるが、完全に不透明な塗料であれば失敗する。）

またタグの深さは表面直下に限られる。透過アルベドの解析から `dmax = 3mm`、機械的強度から `dmin = 1mm` と定めている。タグの寸法は2センチメートル角で約106ビット、5センチメートル角で500ビット超である。

---

## 4. InfraredTagsは肉眼で見えないのか

見えないと明言している。概要の冒頭に次のようにある。

> "We present InfraredTags, which are 2D markers and barcodes imperceptible to the naked eye that can be 3D printed as part of objects, and detected rapidly by low-cost near-infrared cameras."

（InfraredTagsを提案する。これは肉眼では知覚できない2次元マーカーおよびバーコードであり、物体の一部として3Dプリントでき、低価格の近赤外カメラで素早く検出できる。）

不可視性の担保も、AirCodeと同じ5%のコントラスト閾値で行っている（Shell Thicknessの節）。

> "our goal is to find a value that achieves a contrast in the image smaller than 5% when the image is taken with a regular camera (i.e., with an IR cut-off filter). ... We chose 5% because this is the contrast value at which humans cannot differentiate contrast anymore [3]."

具体的な殻の厚さは表2にある。単一材料（IR PLAのみ）で殻1.08ミリメートル・符号2.00ミリメートル、多材料（IR PLA＋白PLA）で殻1.32ミリメートル・符号0.50ミリメートル、IR PLA＋黒PLAで殻1.08ミリメートル、IR PLA＋青PLAで殻1.20ミリメートルである。

ここで見落としてはならないのは、母材そのものの制約である。

> "We acquired the IR filament from manufacturer 3dk.berlin [1] (ca. $5.86/100g). It is made out of polylactic acid (PLA) ... To the naked eye, the filament has a slightly translucent black color, however, when 3D printed in multiple layers it looks opaque."

さらに議論の節で、色が黒に限られることを認めている。

> "While we only used black IR PLA in this project, manufacturers could produce filaments of other colors that have similar transmission characteristics"

つまり、物体全体を特定メーカーの黒い赤外透過フィラメントで印刷しなければならない。任意の材料・任意の色の日用品に後から埋めることはできない。

---

## 5. InfraredTagsの読み出しに何が必要か

### 市販のスマートフォン単体で読めるのか

**読めない。追加の撮像モジュールが要る。** 論文は明確に、専用の後付けモジュールを自作したと書いている。

> "Today, several recent smartphones already come with an IR camera either on the front (Apple iPhone X) or the rear (OnePlus 8 Pro), however, the phones' APIs may not allow developers to access these for non-native applications. Furthermore, not all mobile phones contain such a camera at the moment. To make our method compatible independent of the platform, we built an additional imaging add-on that can easily be attached to existing mobile phones."

（今日、いくつかの最近のスマートフォンは前面（iPhone X）または背面（OnePlus 8 Pro）に赤外カメラを備えている。しかし、電話機の提供する応用機能の窓口が、開発者に対してこれらを純正以外の応用から使わせない可能性がある。さらに、現時点ではすべての携帯電話がそうしたカメラを備えているわけではない。手法を機種に依存しないようにするため、既存の携帯電話に簡単に取り付けられる追加の撮像用付属品を作った。）

モジュールの構成（Attaching the IR camera moduleの節）
> "our add-on contains an infrared camera (model: Raspberry Pi NoIR). This camera can see infrared light since it has the IR cut-off filter removed that normally blocks IR light in regular cameras. Additionally, to remove the noise from visible light and improve detection, we added a visible light cut-off filter, as well as 2 IR LEDs (940nm) which illuminate the object when it is dark. This add-on has two 3D printed parts: a smartphone case from flexible TPU filament that can be reprinted based on the user's phone model, and the imaging module from rigid PLA filament that can be slid into this case. The imaging module has a Raspberry Pi Zero board and a battery and weighs 132g."

したがって必要なものは、赤外カットフィルタを外したカメラ（Raspberry Pi NoIR）、可視光カットフィルタ、940ナノメートルの赤外発光ダイオード2個、Raspberry Pi Zero基板、電池、そしてTPUで印刷した専用ケースである。

加えて、処理は端末上で完結しない。

> "the imaging module continuously streams the images to our image processing server. If the server detects any tags, it sends the location and the encoded message to the smartphone app to show to the user."

（撮像モジュールは画像を我々の画像処理サーバへ連続的に送り続ける。サーバがタグを検出すれば、位置と符号化されたメッセージをスマートフォンの応用へ送り、利用者に表示する。）

なお論文は、赤外カットフィルタを手で外した通常のUSBウェブカメラでも読めると述べている。

> "Even conventional USB webcams for personal computers can be used for this purpose by manually removing their infrared cut-off filter."

いずれにせよ、改造していない市販のスマートフォンだけでは読めない。

### 費用と重さ

- 赤外透過フィラメント：100グラムあたり約5.86米ドル（"ca. $5.86/100g"）
- Raspberry Pi NoIRカメラ：約20米ドル（"such as the Raspberry Pi NoIR ($20)"）
- 比較対象として挙げられている高価な赤外カメラ：FLIR ONE Proが400米ドル超（"may cost more than $400"）
- 撮像モジュールの重さ：132グラム（"weighs 132g"）
- **モジュール全体の合計費用は確認できなかった。** 論文はカメラ単体とフィラメントの価格しか書いておらず、可視光カットフィルタ、Raspberry Pi Zero、電池を含む総額を示していない。

### 必要な近赤外の照度

Lighting conditionsの節に数値がある。

> "We measured the minimum NIR intensity needed to detect 4x4 ArUco markers using a lux meter which had a visible light cut-off filter (720nm) attached. We found that just a tiny amount of NIR is sufficient for this, i.e., that at least 1.1 lux is needed for single-material prints, and 0.2 lux for multi-material prints."

（720ナノメートルの可視光カットフィルタを取り付けた照度計を使い、4×4のArUcoマーカーを検出するのに必要な最小の近赤外強度を測った。ごくわずかな近赤外で十分であり、単一材料の造形物には少なくとも1.1ルクス、多材料の造形物には0.2ルクスが必要だと分かった。）

続けて、実運用の照明環境についても書いている。

> "Because sunlight also contains NIR wavelengths, the tags are detectable outdoors and also in an indoor areas that have windows during daytime. We also noticed that many lamps used for indoor lighting emit enough NIR to detect the codes at nighttime (e.g., 1.5 lux in our office). Furthermore, the IR LEDs on our imaging module (Section 4.2) provide high enough intensity to sufficiently illuminate multi-material markers even in complete darkness"

つまり、屋外や窓のある屋内では太陽光の近赤外成分で足り、夜間も一般的な室内照明の近赤外成分（著者らの居室で1.5ルクス）で足り、完全な暗闇でもモジュール上の赤外発光ダイオードで多材料の符号なら読める。単一材料の場合は完全な暗闇では不足すると認めている。

> "In the future, brighter LEDs can be added to support single-material prints in such difficult detection scenarios."

### 読み取り距離

概要に「250センチメートル」がある。

> "Our evaluation shows that the tags can be detected with little near-infrared illumination (0.2lux) and from distances as far as 250cm."

本文のDistanceの段落によれば、この評価は4×4のArUcoマーカーについて、マーカーの幅を10ミリメートルから80ミリメートルまで振って最大検出距離を測ったものである。

> "The marker size range we evaluated was 10-80mm for 4x4 ArUco markers, which would translate to a range for 42-336mm for 21x21 QR codes (can store up to 25 numeric characters). The results are given in Figure 10a, which shows that multi-material codes can be detected from further away than single single-material ones."

**どのマーカー寸法で250センチメートルに達したのかは、図10aが図版であるため本文の文字情報からは確認できなかった。** 250センチメートルは評価した範囲の最大値であり、マーカーの大きさに依存する値である点は注意が要る。QRコードの検出精度を測った実験は15センチメートルから80センチメートルの範囲で行われている。

> "We captured 124 images of a 21x21 QR code from different distances (15-80cm from the camera)."

その条件でのQRコードの復号精度は、フィルタのパラメータの組み合わせを3通り試して79.03%である（表3）。

### 復号にかかる時間

> "On average, it takes 6ms to decode a 4x4 ArUco marker and 14ms to decode a 21x21 QR code from a single original frame. The images we use as input are 512x288 pixels"

単一のフレームから復号するので、実時間で動く。これはAirCodeの3〜4分と比べて桁違いに速く、CipherFluteの吹奏による読み出しよりも速い。

### 最小のマーカー寸法

> "we determined that the smallest detectable 4x4 ArUco marker printable is 9mm wide for single-material prints and 6mm wide for multi-material prints."

---

## 6. 日用品に埋め込んだ実例はあるか

### AirCode

論文が示す実物は、Moai像、三角形の引き出し、マグカップ、iPhoneを支える猫の置物、ケーブル収納、工具立て、そして紙の透かしである。マグカップや引き出しは日用品と呼べる。ただし、これらはすべて著者らがPolyJetプリンタ（Stratasys Eden260VS）でVeroWhitePlusを使って自ら造形したものである。既製の日用品にあとから埋め込んだ例ではない。

> "We demonstrate with two objects (see Figure 3). In the triangular drawer (Figure 3-a), we embed three different AirCode tags on each side of the drawer. In the mug (Figure 3-b), we embed six tags under the curved surface of the mug."

紙への拡張だけは材料が異なる。

> "here we embed watermarks in a paper by stacking a few thinner papers together. We carve a pattern on one paper and sandwich it in other papers, and then stick all thin papers together."

### InfraredTags

応用の節で、家庭用スピーカー、サーモスタット、無線ルータ、マグカップ、ゲーム用のハンドルを示している。

> "In the application shown in Figure 7a and b, a user points their smartphone camera at the room and smart home appliances are identified through their InfraredTags, which are imperceptible to the human eye."

> "Figure 9 shows a 3D printed wheel with no electronics, being used as a game controller."

これらも、方式の制約上、黒い赤外透過PLAで印刷した筐体でなければならない。論文は既製の家電の元の筐体に埋め込んだとは書いていない。

### まとめ

**両者とも日用品の形をした造形物への埋め込みは示している。ただし、どちらも「その方式が要求する特定の材料で自ら造形した物体」に限られており、任意の材料でできた既製の日用品にあとから埋める例は示していない。**

---

## 7. 判定

### 主張Aについて

**反論は正しい。主張Aは成立しない。**

主張Aの中核は「光学的な符号は表面に露出していなければ読めない」という前提にある。この前提は偽である。AirCodeは表面から1〜3ミリメートルの深さにある空気ポケットを、投影と撮影による大域成分の分離で読む。InfraredTagsは表面から1.08〜1.32ミリメートルの殻の内側にあるQRコードやArUcoマーカーを、近赤外カメラで読む。どちらも肉眼のコントラスト閾値5%を下回るように設計されており、外観を変えていない。したがって「隠蔽と可読性の両立は光学符号には原理的に得られない」とは書けない。

さらに、主張Aの言い回しにはCipherFluteにとって不利な事実が隠れている。AirCodeとInfraredTagsは外部に開口をまったく必要としない。CipherFluteは窓と吸込口という2つの開口を外気に露出させなければならない。「外部に必要なのは小さな開口だけである」という言い方は、開口が不要な方式が実在する以上、優位性の主張にならない。むしろ外観の点では、CipherFluteのほうが露出が多い。

### 主張Bについて

**この反例の検証中に、主張Bも強い形では成り立たないことが分かった。**

AirCodeは、符号の格子の中に「既知の値を持つセル」を散らして配置し、それを使って復号器を現場で訓練している。Code Generationの節に次のようにある。

> "More remarkably, we place a few known bits. The blue cells are always filled with printing material as bits of 1, while the orange cells are filled with air pockets to indicate bits of 0. These bits are scattered on the grid to enable on-the-fly supervised training for our decoding algorithm."

（さらに注目すべきこととして、いくつかの既知のビットを配置する。青いセルは常に造形材料で埋めて1のビットとし、オレンジのセルは空気ポケットで埋めて0のビットとする。これらのビットは格子上に散らして配置され、復号アルゴリズムのその場での教師あり学習を可能にする。）

Decodingの節では、この既知ビットで訓練した分類器の特徴量を局所的な明るさの変化に合わせて正規化するとも書いている。

> "Each feature vector is normalized to adapt to local intensity changes."

これは、既知の値を持つ基準素子を同じ物体に同居させ、データと同時に読んで撮像条件と造形の個体差を打ち消す仕組みである。CipherFluteの基準笛とは、補正する物理量（一方は画像の明るさ、他方は音速すなわち気温と息の強さ）も、補正の演算（一方は分類器の訓練と正規化、他方は周波数の比）も異なる。しかし「同一物体に既知の基準を同居させて環境変動を吸収する」という構造そのものには前例がある。したがって「前例がない」とは書けない。「既存例は撮像系の変動を吸収するために使われており、担体の物理量（気温による音速変化）を打ち消すために基準素子の比を使った例は見当たらない」という程度まで主張を弱める必要がある。ただし、造形物への情報埋め込みの文献を網羅的に調べたわけではないので、この弱めた形が成立するかどうかは別途の確認が要る。

---

## 8. CipherFluteに残る差分

主張Aは撤回するとして、では何が残るのか。依頼された4つの観点で整理する。誇張も過小評価もせずに書く。

### 8.1 装置の必要性

**ここが最大の残る差分である。**

- AirCodeは、DLPプロジェクタ（三菱PK20）、モノクロ産業用カメラ（Point Grey Grasshopper3）、両者の前に置く交差した直線偏光板からなる据え置きの光学ベンチを必要とする。手持ちで物体に向けるという使い方はできない。
- InfraredTagsは、赤外カットフィルタを外したカメラ、可視光カットフィルタ、940ナノメートルの赤外発光ダイオード2個、Raspberry Pi Zero、電池を組んだ132グラムの付属品をスマートフォンに装着する必要がある。さらに画像処理はサーバ側で行う構成になっている。改造していない市販スマートフォン単体では読めない。
- CipherFluteは、利用者が既に持っているスマートフォンのマイクだけで読む。追加の部品も、改造も、専用のフィラメントも要らない。

**この差は「原理的」ではなく「装置の入手性と携帯性」の差である。** 光学で隠しつつ読むことは可能だが、そのために専用の撮像系が要る。音響で読むのは、既存の端末に既に載っている入力装置で足りる。主張は「光学では不可能」ではなく「光学では専用装置が要るが、音響では要らない」という形に書き換えるべきである。

なお、CipherFlute側の論文はこの点を既に第4章の性質(4)として「特別な機器なしに、息とスマートフォンだけで復元できる」と書いている。この記述は一次資料に照らして妥当であり、変更の必要はない。

### 8.2 読み出しの時間

**ここはCipherFluteが一方的に有利とは言えない。正直に書く必要がある。**

- AirCodeは3〜4分かかる。CipherFluteより明らかに遅い。
- InfraredTagsは1フレームから復号し、4×4のArUcoマーカーで6ミリ秒、21×21のQRコードで14ミリ秒である。実時間で動く。CipherFluteは笛を1本ずつ吹いて読むため、本数に比例した秒単位の時間がかかる。**InfraredTagsのほうが速い。**

したがって「光学は遅い」と一般化してはならない。AirCodeに限れば遅いが、それはAirCodeが構造化光の掃引を必要とするからであり、InfraredTagsはその問題を解いている。InfraredTags自身が表1で、AirCodeの「3-4 minutes」やInfraStructsの「2 minutes for a 100x100 pixel scan」に対して自分たちは「On the order of milliseconds」だと明示的に比較している。

### 8.3 外観

**ここもCipherFluteが有利とは言えない。**

- AirCodeとInfraredTagsは、いずれも肉眼のコントラスト閾値5%を下回るように設計されており、外部に開口をまったく持たない。外観上、符号の存在はどこにも現れない。
- CipherFluteは、窓と吸込口という2つの開口を外気に露出させなければならない。開口自体は小さいが、ゼロではない。

CipherFluteに残る外観上の利点は、符号の見えなさではなく、**材料と色の自由度**である。

- AirCodeは、均質で半透明な材料（PolyJet方式のVeroWhitePlusなど）を要求する。論文自身が、熱溶解積層方式では材料が均質にならないこと、不透明な塗装をすると失敗することを限界として認めている。
- InfraredTagsは、特定メーカーの赤外透過PLA（3dk.berlin製、黒）で物体全体を印刷することを要求する。論文自身が、他の色は今後の課題だと書いている。加えて、同じメーカーの異なる時期のスプールで透過特性が変わったので、スプールごとに較正をやり直すよう勧めている。
- CipherFluteは共鳴管の形状だけで符号を担うので、材料の光学的性質に依存しない。PLA、PETG、TPU、金属、どの色でも原理的には成り立つ。この点は、家庭用の3Dプリンタで、手元にある任意のフィラメントで作れるという実用上の差につながる。

したがって主張は「外観に符号が現れない」ではなく、「符号の担い手が形状であるため、担体の材料と色を選ばない」と書き換えるべきである。

### 8.4 読み出しの行為

**ここは構造的な差として残る。**

AirCodeもInfraredTagsも、読み出しは無音であり、所有者の身体的な関与を必要としない。装置を持ち、どこに向ければよいかを知っている者が、物体に触れることなく、所有者に気づかれずに読める。AirCodeは物体を光学ベンチに置く必要があるので実際には持ち去りが要るが、InfraredTagsは最大250センチメートル離れた位置から読める。

CipherFluteは、誰かが息を吹き込まなければ音が出ない。読み出しは必ず能動的な身体行為を伴い、その行為は音として周囲に露出する。これは秘匿の仕組みではなく手続きの性質であり、CipherFlute側の論文が既に性質(3)として「正規の読み出しが目立つ」と書いているとおりである。立会人の前で儀式として実行できるという利点も、この性質から出る。

ただし、この差を過大評価してはならない。CipherFlute側の論文が第4章で自ら明示しているとおり、管の長さは静的な形状なので、攻撃者は吹かずにノギスや透過撮像で読める。つまり「吹かなければ読めない」わけではない。残るのは「正規の手続きが音を伴う」という一点だけであり、攻撃者に対する防御にはならない。

なお、InfraredTags自身も発見しやすさの問題を限界として認めている。

> "For InfraredTags to be detected, the user should orient the near-infrared camera such that the embedded marker is in the frame. However, similar to related projects such as AirCode [20] and InfraStructs [34], this might be challenging since the marker is invisible to users and thus they might not know where exactly on the object to point the camera at."

これは光学方式にとって不利な点だが、CipherFluteの窓と吸込口も同じ問題を抱える（どの開口を吹けばよいか分からない）ので、差分にはならない。

---

## 9. 論文への具体的な反映案

1. 「隠蔽と可読性の両立は光学符号には原理的に得られない」という文は削除する。一次資料に照らして偽である。
2. 代わりに、光学方式との差を次の3点に絞って書く。第一に、読み出し装置が既存のスマートフォンのマイクで足り、専用の撮像系（プロジェクタとカメラの光学ベンチ、または赤外カメラ付属品）を必要としないこと。第二に、符号の担い手が形状であるため、担体の材料と色を選ばず、任意の家庭用フィラメントで作れること。第三に、正規の読み出しが能動的な吹奏を伴い、音として露出すること。
3. 読み出しの速さは差分として主張しない。InfraredTagsはミリ秒で読む。
4. 外観については「符号がまったく見えない」を主張しない。窓と吸込口は露出する。AirCodeとInfraredTagsは開口ゼロである。
5. InfraredTags（Doganら、CHI 2022、DOI 10.1145/3491102.3501951）を関連研究に追加する。現行稿はAirCode（文献[3]）とInfraStructs（文献[4]）しか挙げていないが、InfraredTagsは「安価な装置で速く読める隠された光学符号」という最も強い比較対象であり、これを挙げずに光学方式の限界を論じると、査読で必ず指摘される。
6. 基準笛の自己補正について「前例がない」とは書かない。AirCodeが既知ビットによる現場訓練という形で同種の仕組みを持っている。「撮像系の変動を吸収する既知ビットの例はあるが、担体の物理量（気温による音速変化）を比で打ち消す例は見当たらない」という限定した書き方にする。

---

## 10. 確認できなかったこと

- ACM Digital Libraryの本文ページは、AirCode・InfraredTagsとも取得時にHTTP 403を返したため読めていない。書誌はCrossrefとDBLPで、本文は著者公開版（arXivおよびMIT CSAILの公開PDF）で確認した。
- AirCodeにおける、カメラおよびプロジェクタと物体との距離は、論文に数値が見当たらない。
- AirCodeの読み取り時に必要な周囲照度は、論文に数値が見当たらない。
- InfraredTagsの撮像モジュール全体の合計費用は、論文に記載がない。カメラ単体20米ドルとフィラメント100グラム約5.86米ドルのみが示されている。
- InfraredTagsの250センチメートルという最大検出距離が、どのマーカー寸法に対応するかは、図10aが図版であるため文字情報から特定できなかった。評価したマーカー幅の範囲は10〜80ミリメートルである。
- 主張Bを弱めた形（担体の物理量を基準素子の比で打ち消す例の有無）については、造形物への情報埋め込みの文献を網羅的に調べていないため、成立するかどうかを判定していない。
