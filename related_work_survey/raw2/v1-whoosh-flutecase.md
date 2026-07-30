# 原典確認 v1: Whoosh / FluteCase（ISWC 2016）

調査日: 2026年7月30日
調査者: 原典確認担当（第二段）

---

## 0. 何を確認したか、結論から

前段の担当者の報告は、**事実の面ではおおむね正しかった**。FluteCaseは実在し、8本の閉管であり、電源も電子部品も持たない受動構造であり、3Dプリントであり、管長は 2 の 12 乗根を公比とする等比数列（すなわち平均律の半音比）で定義されており、「2キロヘルツから10キロヘルツ」という記述も本文にそのまま存在する。認証への言及も実在する。

ただし前段の報告には、**新規性の評価を誤らせる三つの過大表現**があった。第一に、FluteCaseは音の高さを測っていない。周波数推定は一切行わず、メル周波数ケプストラム係数とサポートベクターマシンによる利用者ごとの学習分類である。第二に、「2キロヘルツから10キロヘルツ」は帯域の言明にすぎず、実際に設計式から出る8本の基本周波数はおよそ3.8キロヘルツから5.7キロヘルツの範囲、すなわち半音7個分（完全5度）しか広がらない。第三に、認証の記述はFluteCaseの節ではなく「無改造の時計での応用」の節にあり、8本の管とは無関係である。

そして最も重要な差分は、前段が触れていないところにある。**FluteCaseの管長は論文に公開された固定の定数であり、すべての複製が同一形状になることを目的としている。情報は「どの穴を吹いたか」という利用者の選択から生まれるのであって、形状には一切載っていない。** CipherFluteはこれと正反対で、形状そのものが秘密の担い手である。この向きの違いは決定的である。

---

## 1. 書誌情報の確認

| 項目 | 内容 |
|---|---|
| 題名 | Whoosh: Non-Voice Acoustics for Low-Cost, Hands-Free, and Rapid Input on Smartwatches |
| 著者 | Gabriel Reyes, Dingtian Zhang, Sarthak Ghosh, Pratik Shah, Jason Wu, Aman Parnami, Bailey Bercik, Thad Starner, Gregory D. Abowd, W. Keith Edwards（全員 Georgia Institute of Technology） |
| 掲載 | Proceedings of the 2016 ACM International Symposium on Wearable Computers (ISWC '16), Heidelberg, Germany, September 12-16 2016, pp. 120-127 |
| DOI | 10.1145/2971763.2971765 |
| 全文の取得元 | https://sites.cc.gatech.edu/fac/keith/pubs/iswc2016-whoosh.pdf （著者所属機関が公開している版。8ページ、pdfTeX 生成、2016年7月20日作成。本文中に `DOI: http://dx.doi.org/10.1145/2971763.2971765` と `ISWC '16, September 12-16 2016, Heidelberg, Germany.` が刷り込まれている） |
| 掲載誌名とページの照合先 | Crossref (https://api.crossref.org/works/10.1145/2971763.2971765) が `Proceedings of the 2016 ACM International Symposium on Wearable Computers` の `120-127` を返した。DBLP (https://dblp.org/rec/conf/iswc/ReyesZGSWPBSAE16) も `ISWC 120-127` を返した |

ACM Digital Library本体には当たっていないため、印刷版と著者公開版が一字一句同一であることは確認できていない。ただし題名、著者、DOI、ページ、会議名はCrossrefとDBLPの双方と一致した。

なお、Semantic Scholar の当該論文の `venue` フィールドは `International Workshop on the Semantic Web` という誤った値になっている。これはSemantic Scholar側のメタデータの誤りであって、論文の実際の掲載先はISWC 2016（ウェアラブルコンピューティングの国際シンポジウム）である。同じ略称の別会議と混同されている。この点は後続の被引用調査でも注意が必要である。

---

## 2. 前段の主張を一つずつ原典に当てる

### 2.1 「FluteCaseと呼ばれる構造が存在する」——**成り立つ**

節の見出しがそのまま `FLUTECASE: A PASSIVE 3D-PRINTED WATCH CASE` である（本文6ページ）。

> "FluteCase is a custom 3D-printed watch case for both square and circular smartwatches that alters the acoustic response of blowing events on and around the smartwatch. The case provides a low-cost and entirely passive (meaning no electronics nor battery usage) means of expanding the range of inputs that are recognized by our system."

日本語訳: 「FluteCaseは、角形と円形の両方のスマートウォッチのために作った専用の3Dプリント時計ケースであり、スマートウォッチの上および周囲で起きる吹奏イベントの音響応答を変化させる。このケースは、我々のシステムが認識する入力の範囲を広げるための、低コストで完全に受動的な（電子部品もバッテリー消費も無いという意味である）手段を提供する。」

論文冒頭の要約にも次の記述がある。

> "Further, inspired by the design of musical instruments, we develop a custom modification of the physical structure of the watch case to passively alter the acoustic response of events around the bezel; this physical redesign expands our input vocabulary with no additional electronics."

日本語訳: 「さらに我々は、楽器の設計に着想を得て、ベゼル周辺のイベントの音響応答を受動的に変えるために、時計ケースの物理構造に専用の改変を加えたものを開発した。この物理的な再設計は、追加の電子部品なしで我々の入力語彙を拡張する。」

貢献の箇条書きにも次のとおり明記されている。

> "We introduce the use of passive, 3D-printed smartwatch cases to expand the expressivity of events by introducing air swipes, circular blows, and bezel blows."

日本語訳: 「我々は、エアスワイプ、円周吹き、ベゼル吹きを導入することでイベントの表現力を広げるために、受動的な3Dプリント製スマートウォッチケースを用いることを提案する。」

### 2.2 「本当に8本の管なのか」——**成り立つ**

> "The cases have 8 closed pipe tubes of different lengths, each with an open hole. The tubes' "head" (the end with the open hole) and "tail" (the closed end) are connected to each other. In the case of a circular smartwatch, the head and tail form a ring shape around the watch display. A base that fits the shape and size of the watch bezel attaches tightly to the watch."

日本語訳: 「ケースは長さの異なる8本の閉管を持ち、それぞれに開いた穴が一つある。管の「頭」（穴が開いている側の端）と「尾」（閉じている端）は互いにつながっている。円形のスマートウォッチの場合、頭と尾は時計の表示部を囲む輪の形をなす。時計のベゼルの形と大きさに合う台座が、時計にぴったり取り付く。」

図4Bの半透明レンダリングには管の番号が 0 から 7 まで記されている（実際に画像を確認した。角形ケースの四隅と四辺に相当する位置に 7, 2, 4 / 0, 1 / 5, 3, 6 の番号が振られている）。したがって式中の添字 i は 0 から 7 の8通りである。

### 2.3 「本当に受動的（電源なし）なのか」——**ケース単体としては成り立つ。ただし系全体は能動である**

ケースそのものは上記引用のとおり `entirely passive (meaning no electronics nor battery usage)`（完全に受動的、電子部品もバッテリー消費も無い）である。この点は前段の報告のとおりである。

ただし読み取り側は完全に能動である。論文自身が次のように認めている。

> "While our technique does require an active microphone and continuous analysis, the majority of smartwatches today are already "always-on" for hotword detection (e.g., "Ok Google")."

日本語訳: 「我々の手法は能動的なマイクロフォンと連続的な解析を必要とするが、今日のスマートウォッチの大半は既にホットワード検出（たとえば「オーケー、グーグル」）のために常時起動している。」

すなわちFluteCaseは「電源のいらない記憶媒体」ではなく、「電源の入った時計に取り付ける、電源のいらない入力部品」である。CipherFluteの「電源も電子部品も持たない物理鍵」という位置づけと、受動性の意味するところが違う。CipherFluteも読み取りにはスマートフォンのマイクロフォンを使うので、この点では両者は同じ構図であるが、FluteCaseの受動性は「時計の電池を食わない」という省電力の主張であって、「電源を失っても秘密が残る」という保管の主張ではない。

### 2.4 「本当に3Dプリントなのか」——**成り立つ**

節の見出しと貢献の箇条書きの双方に `3D-printed` と書かれている（2.1の引用を参照）。ただしプリンタの機種、材料、造形方向、サポート材の有無については本文に記述が無い。CipherFluteが力を入れている「家庭用の熱溶解積層方式でサポート材なしに平置きで刷れる」という造形上の主張は、Whooshには存在しない。この主張を先取りしているのはWhooshではなく、後述するBlowhole（GI 2018）である。

### 2.5 「管長を半音比の等比数列で決めたと本当に書いてあるのか」——**成り立つ。ただし「半音」という語は一度も使われていない**

まず物理の説明として次の記述がある。

> "When air is blown into a tube-shaped resonator, standing waves are created that cause the air to vibrate and produce sound. For closed pipe wind instruments like ours, the pitch of the vibration is determined by the length of the tube. For example, the Greek pan flute has multiple tubes with different lengths open at one end for blowing and is closed at the other end. Closed pipe resonators do not require finger operation and their fundamental air resonant frequencies are defined by:"
>
> f = v / λ  [Hz]  (1)
>
> "where f is the air resonant frequency, v is the speed of sound, λ = kL is the wavelength, where k is a constant determined by open or closed pipe and L is the length of the pipe. Generally, the shorter the pipe is, the higher the resonant frequencies produced."

日本語訳: 「管の形をした共鳴体に空気を吹き込むと定在波が生じ、空気が振動して音が出る。我々のもののような閉管の管楽器では、振動の音の高さは管の長さで決まる。たとえばギリシャのパンフルートは、長さの異なる複数の管を持ち、吹くための一方の端が開き、他方の端が閉じている。閉管の共鳴体は指の操作を必要とせず、その基本空気共鳴周波数は次式で定義される。ここで f は空気共鳴周波数、v は音速、λ = kL は波長であり、k は開管か閉管かで決まる定数、L は管の長さである。一般に、管が短いほど生じる共鳴周波数は高くなる。」

そして設計式が次のとおり与えられている（本文6ページ、式(2)。この式は文字抽出では崩れるため、200 dpi で当該ページを画像に描画して目視で確認した）。

> "The overall width, length, and depth of the square case are 45.60 mm, 51.06 mm, and 5.58 mm, respectively. The diameter of each hole is 4.05 mm. The width of each circular tube is constant at 4.096 mm. The length of each tube is defined by:"
>
> **L = 14.956 ∗ 2^(i/12)  [mm]  (2)**
>
> "where L is the length of each tube as a function of i, which denotes the ith tube (labeled in Figure 4B)."

日本語訳: 「角形ケースの全体の幅、長さ、深さは、それぞれ45.60ミリメートル、51.06ミリメートル、5.58ミリメートルである。各穴の直径は4.05ミリメートルである。各円形管の幅は4.096ミリメートルで一定である。各管の長さは次式で定義される。ここで L は i の関数としての各管の長さであり、i は i 番目の管を表す（図4Bに番号を付した）。」

公比 2^(1/12) は平均律の半音比そのものである。したがって「管長は半音比の等比数列で決められている」という前段の主張は、数式の上では**完全に正しい**。

ただし補足すべき点が二つある。第一に、論文は `semitone`（半音）、`temperament`（音律）、`chromatic`（半音階）、`octave`（オクターブ）のいずれの語も一度も使っていない（全文を平坦化して数えたところ出現回数はいずれも0であった）。音楽的な言及は `inspired by the design of musical instruments`（楽器の設計に着想を得て）と `similar to the structures of a musical instrument`（楽器の構造に似て）の2箇所、およびパンフルートへの言及1箇所だけである。つまり著者たちは半音格子を音律として意識して選んだのではなく、8本を等比に並べる自然な刻みとして 2^(1/12) を書いた可能性がある。第二に、CipherFluteが半音格子を使う理由は「符号の語彙を等間隔のセントで切って復号の判定を確実にする」ためであり、FluteCaseが使う理由は「8つの穴を分類器が取り違えないようにする」ためである。同じ式でも役割が違う。とはいえ、**「受動的な3Dプリント多管構造の管長を平均律の半音比で並べる」という設計それ自体は、2016年に既に印刷されている**。この事実は動かない。

### 2.6 「周波数の範囲は本当に2キロヘルツから10キロヘルツなのか」——**本文にその記述はある。ただし記述と設計式は整合していない**

本文の記述は次のとおりである。

> "The eight tubes are designed to resonate at eight distinct frequencies between 2kHz to 10kHz, allowing blows near particular regions of the watch face to be readily disambiguated."

日本語訳: 「8本の管は2キロヘルツから10キロヘルツの間の8つの異なる周波数で共鳴するよう設計されており、これにより時計面の特定の領域の近くへの吹奏を容易に見分けられる。」

したがって前段の「2キロヘルツから10キロヘルツ」という記述は、論文の文言をそのまま写したものであって捏造ではない。

しかし、これを「8本が2キロヘルツから10キロヘルツに散らばっている」と読んではならない。式(2)から私が自分で計算した結果は次のとおりである（音速343メートル毎秒、閉管の f = v/(4L) を用いた。これは論文が報告した数値ではなく、私の計算である）。

| i | L（ミリメートル） | 閉管としての基本周波数（ヘルツ） |
|---|---|---|
| 0 | 14.956 | 5733 |
| 1 | 15.845 | 5412 |
| 2 | 16.788 | 5108 |
| 3 | 17.786 | 4821 |
| 4 | 18.843 | 4551 |
| 5 | 19.964 | 4295 |
| 6 | 21.151 | 4054 |
| 7 | 22.409 | 3827 |

すなわち8本の設計上の基本周波数はおよそ3.8キロヘルツから5.7キロヘルツの範囲に収まり、全体の広がりは半音7個分、周波数比で 2^(7/12) ≈ 1.498 にすぎない。「2キロヘルツから10キロヘルツの間」という言明は、8本がその帯域の内側にあるという意味では正しいが、その帯域を埋めているという意味では正しくない。論文は8本の実測共鳴周波数を一切報告していないため、実測との照合はできなかった。図5Gのベゼル吹き8回のスペクトログラムを画像として確認したが、そこに見えるのは広帯域の吹奏雑音であり、8つの離散した細い音の線としては読み取れなかった。

参考として、CipherFluteの符号語彙はF#6（約1480ヘルツ）からF#7（約2960ヘルツ）の1オクターブ13スロットであり、FluteCaseの帯域とは重なっていない。両者は「小さな印刷管が数キロヘルツで鳴る」という同じ物理の領域にいるが、選んだ窓は別である。

### 2.7 「認証への言及」——**存在する。ただし構想の一言に近い水準であり、しかもFluteCaseとは無関係である**

該当箇所の全文は次のとおりである。ページ7の `DEMONSTRATION APPLICATIONS`（実演アプリケーション）の節の中の、`Unmodified Watch Applications`（**無改造の時計での応用**）という小見出しの下、`Notifications` の次の項目である。この配置は該当ページを画像に描画して目視で確認した。

> "*Authentication*: A person can also use a sequence of Whoosh events as an additional layer of security on their devices. The smartwatch can automatically lock whenever the user removes it from the wrist. In our application, a lock screen pops up and a pre-determined sequence of Whoosh events is used to unlock the device. Whoosh events on the watch could also be used as a physical authentication challenge to complete a purchase on another device (e.g., mobile phone or desktop)."

日本語訳: 「**認証**: 人は、Whooshイベントの列を自分の機器の追加の安全性の層として使うこともできる。スマートウォッチは、利用者が手首から外したときに自動的に施錠できる。我々のアプリケーションでは、施錠画面が現れ、あらかじめ決めておいたWhooshイベントの列が機器の解錠に使われる。時計上のWhooshイベントは、別の機器（たとえば携帯電話やデスクトップ計算機）での購入を完了するための物理的な認証チャレンジとしても使える可能性がある。」

踏み込みの程度を厳しく評価すると次のようになる。

- **解錠の部分**: 実演アプリケーションとして実装されている（`In our application, a lock screen pops up`）。ただし評価は一切無い。イベント列の長さも、取りうる組み合わせの数も、推測に対する強さも、肩越しに覗く攻撃への耐性も、何も論じていない。エントロピーの語（`entropy`）は全文に0回である。
- **購入承認の部分**: `could also be used`（使える可能性がある）という条件法一文だけである。実装も設計も無い。
- **安全性の議論全般**: `security` の出現は全文で**この段落の1回だけ**である。`threat`（脅威）、`adversar`（敵対者）、`cryptograph`（暗号）、`encrypt`（暗号化）、`secret`（秘密）はいずれも**0回**である。脅威モデルは存在しない。
- **決定的な点**: この認証は**無改造の時計**の10イベント（短い吹き、二連吹き、長い吹き、上下のエアスワイプ、円周吹き、シュー音、開口呼気、吸いと吐き）で行われるものであり、FluteCaseの8本の管は使われていない。FluteCaseの応用として挙がっているのは地図（`Maps`）とアプリの近道（`Application Shortcuts`）の2つだけである。

したがって前段の「一連の吹奏イベント列を端末のロック解除や購入承認の物理的チャレンジに使う認証構想まで論文中で述べている」は、事実としては正しいが、**「FluteCaseを認証に使う構想」ではない**。ここは前段の報告が読み違えている。Whooshの認証は「利用者が頭の中に覚えた吹き方の並び」を合図とするものであって、物体に刻まれた情報を読み出すものではない。暗証番号を吹いて入力する話であり、鍵を読む話ではない。

### 2.8 追加で確認した重要な事実——FluteCaseは音の高さを測っていない

前段は「8つの音高で位置を識別する」と書いたが、これは機構の読み違えである。認識系は次のとおりである。

> "Mel-frequency cepstral coefficients (MFCCs) are a set of acoustic features modeling the human auditory system's non-linear response to different spectral bands. We calculate a 26-dimension MFCC with band edges from 0Hz to half the sampling rate at 24kHz. ... The MFCC vectors for each half add up to a total of 52 features. We use an additional 26 features based on the deltas of the MFCC coefficients. The features are normalized for classification. We run principal component analysis (PCA) on these features to facilitate our real-time classification."
>
> "Classification: We use a support vector machine (SVM) algorithm trained using Weka's sequential minimal optimization (SMO) implementation with a cubic polykernel and default parameters."

日本語訳: 「メル周波数ケプストラム係数は、異なるスペクトル帯に対する人間の聴覚系の非線形応答をモデル化した音響特徴の組である。我々は0ヘルツから標本化周波数の半分である24キロヘルツまでを帯域端とする26次元のメル周波数ケプストラム係数を計算する。（中略）各半分のメル周波数ケプストラム係数ベクトルは合計52個の特徴になる。さらに係数の差分に基づく26個の特徴を加える。特徴は分類のために正規化される。実時間分類を容易にするため、これらの特徴に主成分分析をかける。」「分類: 三次の多項式カーネルと既定のパラメータを用いた、Wekaの逐次最小最適化実装で学習させたサポートベクターマシンのアルゴリズムを用いる。」

すなわち基本周波数の推定は行わない。スペクトル形状の指紋照合である。しかもこれは利用者ごとに学習した分類器であり、精度は次のとおりである。

> "For 10-fold cross validation, the average accuracy across 8 users and 14 events is 91.4% (sd=5.3%). ... Preliminary leave-one-participant-out analysis across 8 participants and 14 events results in overall accuracy of 79.7% (sd=9.7%)."

日本語訳: 「10分割交差検証では、8人の利用者と14イベントにわたる平均精度は91.4パーセント（標準偏差5.3パーセント）である。（中略）8人の参加者と14イベントにわたる、一人を除いて学習する予備的な解析では、全体精度は79.7パーセント（標準偏差9.7パーセント）となる。」

利用者に依存しない条件では79.7パーセントまで落ちる。CipherFluteのように40本から49本を続けて正しく読み切る必要がある系では、この水準の利用者依存性はそのままでは使えない。CipherFluteが基準笛による比の正規化を導入している理由は、まさにこの依存性を機械学習ではなく物理で消すことにある。ここは重なりではなく差分である。

なお要約と結論は14イベントの精度を91.3パーセントと書き、本文は91.4パーセントと書いている。論文内部の小さな不整合である。

---

## 3. CipherFluteとの本当の差分

誇張も過小評価もせずに並べる。「先取りされている」ものと「先取りされていない」ものを分ける。

### 3.1 FluteCaseに先取りされているもの（CipherFluteが新規性を主張できないもの）

1. **受動的な3Dプリント多管構造を口で吹き、汎用機器のマイクロフォンで読むという枠組みそのもの。** 2016年に完全に成立している。
2. **閉管の長さを平均律の半音比 2^(1/12) の等比数列で並べる設計。** 式(2)がそのままそれである。CipherFluteは「半音格子を使う」ことを新しいとは主張できない。
3. **f と管長 L を単純な閉管の式で結び付けて設計する手法。** 式(1)がそれである。CipherFluteの f = A/(L+e) は端補正 e を加えて実測に合わせた較正式であり、その点は前進であるが、骨格は同じである。
4. **数ミリメートル径の小さな印刷管が数キロヘルツで鳴るという物理の利用。** 穴径4.05ミリメートル、管幅4.096ミリメートル、ケース厚5.58ミリメートルという寸法は、CipherFluteの厚さ4ミリメートル、幅7ミリメートルと同じ規模である。
5. **複数の管を一つの部品に融合して一体で印刷すること。** 8本が輪状につながった一体のケースである。
6. **吹奏を機器の認証に使うという着想の存在。** 解錠と、別機器での購入承認の物理的チャレンジという言葉が既にある。

### 3.2 FluteCaseに先取りされていないもの（CipherFluteに残るもの）

ここが本質である。項目ごとに、確認した根拠を添える。

1. **情報の向きが正反対である。** これが最大の差分である。FluteCaseの管長は論文に定数として公開されており（`For replicability, we describe the dimensions of the square case used during our user evaluation.` すなわち「再現可能性のため、利用者評価で用いた角形ケースの寸法を記す」）、**すべての複製が同一形状になることを意図している**。情報は形状にではなく「利用者が8つの穴のどれを吹いたか」という選択に載る。FluteCaseは8鍵の鍵盤であって、記憶媒体ではない。CipherFluteは逆で、形状が物体ごとに違い、その違いこそが運ぶべき値である。読み取り側は事前にその値を知らない。この向きの違いは、貢献の性質を根本的に分ける。

2. **多ビットのデータを運ぶ設計が無い。** `bit` の出現は全文で6回だが、その内訳は `multitouch` と `exhibit(s)` の語の一部が4回、`16-bit PCM encoding`（音声標本の量子化ビット数）が1回、`4-7kHz` の周辺が1回であり、**情報量としてのビットの概念は一度も登場しない**。容量の見積もりも、符号語への連結も、128ビットという目標も無い。14イベントは選択肢としては log2(14) ≈ 3.8 ビット相当だが、それは「押せるキーが14個ある」という意味であって、格納容量ではない。

3. **誤り訂正が無い。** `error correction` の出現は全文で1回だけであり、それは序論で他人の研究（文献[9] WatchWriter、スマートウォッチの画面上キーボードでの文字入力）を紹介する文脈である。音響の通信路に対する誤り訂正は存在しない。`Reed`、`Solomon`、`Hamming` はいずれも0回である。

4. **基準となる音による正規化が無い。** `calibrat`、`temperature`、`humidity` はいずれも0回である。`normaliz` の1回は分類器のための特徴量の正規化であって、音の高さの正規化ではない。環境変動や息の強さの変動は、基準音との比ではなく、利用者ごとの学習データで吸収している。CipherFluteの基準笛は、この問題を機械学習なしに物理で閉じる仕組みであり、Whooshには対応物が無い。

5. **秘密情報を扱う議論が無い。** `secret`、`encrypt`、`cryptograph`、`entropy`、`threat`、`adversar` はすべて0回である。脅威モデルは存在しない。秘密分散も鍵素材も鍵の復元も出てこない。`security` は認証の段落の1回だけである。CipherFluteが「物理層に暗号学的な秘匿の力は無いと宣言し、秘匿性を秘密分散にのみ負わせる」という立て方は、Whooshには影も無い。

6. **日用品への埋め込みや偽装の議論が無い。** `embed`、`conceal`、`hidden`、`disguis`、`stegano` はすべて0回である。FluteCaseは時計に取り付ける、見てそれと分かる目立つ付属品である（図4Aと図4C-Eで、白い枠が腕時計の外側にはっきり見える）。隠す意図はなく、むしろ8つの穴が等間隔に並んでいることを利用者に見せて操作させる設計である。CipherFluteの「探索コストの引き上げ」という物理層の役割は、まったく共有されていない。

7. **本数の規模が二桁違う。** FluteCaseは8本、しかも時計のベゼル一周という固定の配置である。CipherFluteの40本から49本を一つの日用品に融合するという規模の問題は扱われていない。

8. **絶対的な音高の読み出しという問題設定が無い。** 2.8で見たとおり、FluteCaseは周波数を測らずスペクトル指紋を照合する。利用者非依存では79.7パーセントに落ちる。CipherFluteが必要とする「初めて見る物体の音高を、利用者も機器も温度も変わりうる条件で絶対値として読む」という問題は、Whooshでは提起すらされていない。

9. **サポート材なしの造形性の議論が無い。** 2.4で述べたとおり、プリンタ、材料、造形方向についての記述が皆無である。ただしこの点でCipherFluteが対抗すべき相手はWhooshではなくBlowholeである（次節を参照）。

10. **隣接同音禁止などの符号語設計が無い。** 制約付き符号の概念そのものが無い。

---

## 4. 被引用をたどる——FluteCaseの路線を継いだ後続研究はあるか

### 4.1 調べ方

Semantic Scholar の引用取得（`https://api.semanticscholar.org/graph/v1/paper/DOI:10.1145/2971763.2971765/citations?fields=title,year,venue,externalIds,abstract&limit=100`）で44件の引用元を取得し、題名、掲載先、年、抄録（取得できたもの）を全件目視した。Crossref の被引用数は33件であった（`is-referenced-by-count`）。両者の差はSemantic Scholarが会議録以外の文書（学位論文や特許出願らしきものを含む）も拾っているためと見られる。

### 4.2 結果——路線を継いだのは1件だけである

44件のうち、受動的な3Dプリント構造を吹いて共鳴音で識別するという路線を継いだものは、**Blowhole（Graphics Interface 2018）ただ1件**である。他の43件は、非音声音響入力、呼吸入力、スマートウォッチの入力手法、人体活動認識、可視光通信、生体認証といった別方向であり、印刷された共鳴管を情報の担い手とする話には向かっていない。近接するものとして BeatIt（`Knock knock, what's there: converting passive objects into customizable smart controllers`, MobileHCI 2018）が受動物体を叩く音で操作する話をしているが、これは既存物体の固有音の学習照合であり、管の設計は無い。また `Improving ultrasound-based gesture recognition using a partially shielded single microphone`（UbiComp 2018）が3Dプリントのカバーでマイクロフォンの特性を変える話をしているが、これは超音波ドップラーの話であって共鳴管の符号ではない。

`FluteCase` という語で言及している後続文献は見つからなかった。Blowholeも `FluteCase` の語は使わず（全文で0回）、`Whoosh [16]` として引用している（3回）。ウェブ検索でも `FluteCase` の実質的な言及は原論文以外に見つからなかった。

### 4.3 Blowholeの記述が示す重要な事実

Blowhole（http://graphicsinterface.org/wp-content/uploads/gi2018-18.pdf から全文を取得した）は、Whooshを明示的に自分の直前の研究として位置づけている。

> "Whoosh [16] adds small predefined cavities to a watch, allowing hands-free control via blowing at the watch face. Blowhole extends this previous work, adding multiple blow-activated tags to imbue arbitrary 3D-printed objects with interactivity. Blowhole achieves high accuracy with up to nine tags per object—more than most other passive acoustic approaches in the literature."

日本語訳: 「Whoosh[16]は時計に小さなあらかじめ定めた空洞を追加し、時計面に吹くことで手を使わない操作を可能にする。Blowholeはこの先行研究を拡張し、任意の3Dプリント物体に対話性を付与するために複数の吹奏起動タグを追加する。Blowholeは1物体あたり最大9個のタグで高い精度を達成し、これは文献中の他の受動音響手法の大半を上回る。」

さらに、CipherFluteにとって極めて有利な記述が同論文にある。

> "This last criterion poses the strongest limitation due to the limited ability of FDM 3D printers to print with overhangs—angles greater than 45° from gravity—and bridging—printing material with nothing underneath it as a support. We experimented with a number of shapes. Simple tubes (as used, for example, in Whoosh [16]) printed well at any orientation but quickly became too large to embed in smaller objects while supporting a range of frequencies. We tested several variations on shorter tubes connecting to larger cavities, which preserve a standard opening size but allow the production of a greater range of frequencies."

日本語訳: 「この最後の基準は、熱溶解積層方式の3Dプリンタが、重力から45度を超える角度のオーバーハングと、下に支えが何も無い状態で材料を渡すブリッジを印刷する能力が限られているために、最も強い制約となる。我々はいくつもの形状を試した。単純な管（たとえばWhoosh[16]で使われているもの）はどの向きでもよく印刷できたが、周波数の範囲を確保しようとするとすぐに、より小さな物体に埋め込むには大きすぎるものになった。我々は、標準的な開口寸法を保ちながらより広い周波数範囲を作れる、より短い管を大きな空洞につなぐ形をいくつか試した。」

これは重要である。**Blowholeは「Whooshのような単純な直管は、周波数の範囲を確保しようとすると小さな物体に埋め込むには大きすぎる」と明言して、直管を捨ててヘルムホルツ共鳴の球状空洞に移った。** CipherFluteの半割り断面（厚さ4ミリメートル、幅7ミリメートル）による小型直管は、Blowholeが諦めたこの問題に別の答えを出している。すなわちCipherFluteの造形上の貢献は、Whoosh（管は大きくてよい、時計の外周に一周させるだけだから）とBlowhole（管では埋め込めないから空洞にする）の両方に対して、「管のままで薄く小さくする」という第三の道として位置づけられる。ここは残る新規性であり、しかも先行研究の言葉で正当化できる。

---

## 5. 前段の報告に対する判定

| 前段の主張 | 判定 |
|---|---|
| 長さの異なる8本の閉管を並べた受動的な3Dプリント構造（FluteCase）がある | 成り立つ |
| 管長は半音比の等比数列で決められている | 成り立つ（式(2)が L = 14.956 × 2^(i/12)）。ただし論文は「半音」という語を使っていない |
| CipherFluteの物理機構および音高設計とほぼ一致する | **物理機構については成り立つ。音高設計については半分だけ成り立つ**（刻みは一致するが、帯域も、絶対音高を測るという発想も、基準による正規化も一致しない） |
| 2キロヘルツから10キロヘルツの8つの音高で位置を識別する | **一部誤り**。この文言は本文にあるが、式から出る8本の設計周波数はおよそ3.8から5.7キロヘルツ（半音7個分）にしか広がらない。また識別は音高の測定ではなくメル周波数ケプストラム係数とサポートベクターマシンによる利用者別の分類である |
| 認証構想まで論文中で述べている | 成り立つ。ただし**FluteCaseの応用ではなく無改造の時計の応用**であり、安全性の分析は皆無で、購入承認は条件法一文である |
| 受動3Dプリント多管笛を吹いて音高で識別するというCipherFluteの物理機構の新規性がほぼ消える | **成り立つ**。この水準の主張は放棄すべきである |
| 現在の論文はこの文献を一切引用していない | 成り立つ。`paper/cipherflute_wiss2026_v1.2.docx` の本文を機械的に検査したところ、`whoosh`、`flutecase`、`reyes` はいずれも0回であった（Blowholeは4回、Acoustic Barcodesは3回、Lamelloは3回、Acoustic Voxelsは3回引用されている） |

総合すると、前段の報告は**おおむね正しい**。脅威度「高」という評定も妥当である。ただし脅威の中身は前段が想定したものとは少し違う。詳細は次節に述べる。

---

## 6. 私自身の判断——CipherFluteの新規性はどこまで残るか

### 6.1 消えるもの

**物理層の新規性は、少なくとも次の形では完全に消える。**

「電源も電子部品も持たない3Dプリントの笛を複数本融合し、吹いた音の高さで情報を読む」という一文は、2016年のFluteCaseで既に成立している。「管長を半音比の等比数列で並べる」も同じである。CipherFluteの論文がこの二つを貢献として書いているなら、それは事実として誤りである。書き直すしかない。

さらに悪いことに、この論文を一つも引用していない。ISWCという主要会議の、AbowdとStarnerが著者に入っている論文であり、しかも題名に `Whoosh`、節見出しに `FLUTECASE` と書いてあって、笛の研究をしていて見落としたという言い分は通りにくい。査読者が知っていた場合の打撃は、重なりの実質以上に大きい。「この著者は自分の分野を知らない」という印象は、個別の差分の説明では回復しにくい。

「吹奏を認証に使う」という着想も、弱い形ではあるが先にある。CipherFluteが認証や承認の文脈を新しいものとして提示するなら、それも成り立たない。

### 6.2 残るもの

**それでもCipherFluteの中核は残る。残るのは「情報の向き」である。**

FluteCaseは鍵盤である。8本の管の長さは論文に定数として印刷され、すべての複製が同一であることを目的とし、情報は形状ではなく利用者の選択に載る。物体は何も覚えていない。CipherFluteは記憶媒体である。管の長さが物体ごとに違い、その違いが運ぶべき値であり、読み取り側はその値を事前に知らない。この違いは程度の差ではなく種類の差である。したがって次の五つは、この文献群のもとでもなお残る。

第一に、**形状を秘密の担い手にするという問題設定そのもの**。Whooshには情報量としてのビットの概念が一度も現れない。Blowholeも最大9個のタグの識別であって、符号語ではない。100ビットを超える値を電源なしの可聴音構造に載せた例は、今回の44件の被引用の中には無かった。

第二に、**絶対的な音高を利用者非依存・機器非依存で読み切るための、基準笛による比の正規化**。Whooshはこの問題を利用者ごとの学習で回避しており、利用者非依存では79.7パーセントに落ちる。物理で閉じる設計は前例が見つからない。

第三に、**符号層（半音格子を語彙とし、隣接同音を禁じ、Reed-Solomon符号で訂正する）を実際に動く系として組んだこと**。ただしここは要注意である。前段が指摘したとおり、Acoustic Barcodes（UIST 2012）が遷移保証と誤り訂正をすでに詳細に論じている。Whooshは無関係だが、符号層の新規性はWhooshではなくAcoustic Barcodesとの間で削られる。半音格子を語彙にするという点はFluteCaseに先取りされている。したがって符号層で残るのは「これらを組み合わせて40本以上の多本数系で実測まで通した」という統合と規模の主張だけであり、要素技術としての新規性はほとんど無い。ここを新規性の柱にするのは危険である。

第四に、**日用品への偽装という物理層の役割と、それを暗号学的な秘匿と峻別する脅威モデル**。Whooshにはこの語彙が一切無い。ここは無競合である。ただし正直に言えば、これは技術的な新規性ではなく議論の作法の新規性である。査読者によっては貢献と認めない。

第五に、**Blowholeが「管では小さな物体に埋め込めない」として捨てた道を、半割り断面で復活させた造形上の解**。厚さ4ミリメートル、幅7ミリメートルという数字は、Blowholeの当該文と直接対比できる。ここは数字で示せる工学的な前進である。

### 6.3 厳しい結論

CipherFluteの新規性は、**物理機構と音高格子から完全に退却し、「形状が秘密を運ぶ記憶媒体である」という一点に絞れば残る。絞らなければ残らない。**

そして残る部分も、単独で強いのは第一と第二である。第三は先行研究の組み合わせであり、第四は議論の作法であり、第五は局所的な工学である。「128ビット級の秘密を電源なしの印刷物に載せ、汎用機器で誤りなく読み出す系を実際に作った」という、容量と統合と実機動作を一体にした主張が、現実的に守れる最も強い線である。逆に「印刷した笛を吹いて音高で読む」「半音格子を使う」「認証に使う」という三つの言い方は、いずれもこの文献群のもとでは主張として成立しないため、論文から削るべきである。

なお、Whooshを引用して差分を書くこと自体は、むしろ論文を強くする。Whooshの管長式が半音比であるという事実を自分から指摘し、「同じ格子を使うが、あちらは全複製が同一形状になることを目的とし、こちらは形状の違いが値である」と書けば、貢献の輪郭が一段はっきりする。Blowholeの「単純な管は小さな物体に埋め込めない」という一文を引いて自分の半割り断面を正当化するのも同様である。引用を避けることによる利益は無く、損失だけがある。

---

## 7. 確認できなかったこと

1. **ACM Digital Libraryの印刷版との一字一句の照合**。著者所属機関が公開している版（https://sites.cc.gatech.edu/fac/keith/pubs/iswc2016-whoosh.pdf ）を用いた。題名、著者10名、DOI、会議名、ページ（120-127、CrossrefとDBLPで確認）は一致したが、印刷版そのものは取得していない。
2. **付随する動画の内容**。論文は `We refer the reader to the video accompanying this paper for live demonstrations of each application.`（各応用の実演については本論文に付随する動画を参照されたい）と書いている。この動画は取得していないため、認証の実演が本文の記述より踏み込んでいる可能性は排除できない。ただし本文に安全性の分析が皆無であることは確認済みである。
3. **8本の管の実測共鳴周波数**。論文は設計式と「2キロヘルツから10キロヘルツの間」という帯域の言明のみを与え、実測値を一切報告していない。本報告の3.8キロヘルツから5.7キロヘルツという数値は、式(2)と閉管の関係式 f = v/(4L) から私が計算したものであり、著者が報告した値ではない。図5Gのスペクトログラムからは8つの離散した音高を読み取れなかった。
4. **式(2)の添字 i の下限**。図4Bの管の番号が0から7であることから i は0から7と判断したが、本文にその明示は無い。i が1から8であれば長さは15.845ミリメートルから23.74ミリメートル、周波数は3612ヘルツから5412ヘルツとなる。いずれにしても広がりは半音7個分であり、結論は変わらない。
5. **被引用の網羅性**。Semantic Scholarで44件、Crossrefで33件を確認した。Google Scholarは今回の手段では参照できていないため、これらに現れない後続研究がある可能性は残る。また44件のうち数件（Blowhole、LeapTrak、特許様の文書2件）は抄録が取得できず、題名と掲載先のみで判断した。ただしBlowholeについては全文を取得して読んだ。
6. **FluteCaseの管が音響的に独立しているかどうか**。本文は `The tubes' "head" ... and "tail" ... are connected to each other.`（管の頭と尾は互いにつながっている）と書いているが、これが構造上つながっているだけなのか、空気の通路としてもつながっているのかは判別できなかった。図4Bの目視では、管が輪状に並んだ一体の枠に見える。

---

## 付録: 使った資料の所在

- Whoosh 全文（PDF、8ページ）: https://sites.cc.gatech.edu/fac/keith/pubs/iswc2016-whoosh.pdf
- Whoosh 書誌（Crossref）: https://api.crossref.org/works/10.1145/2971763.2971765
- Whoosh 書誌（DBLP）: https://dblp.org/rec/conf/iswc/ReyesZGSWPBSAE16
- Whoosh 被引用一覧（Semantic Scholar）: https://api.semanticscholar.org/graph/v1/paper/DOI:10.1145/2971763.2971765/citations?fields=title,year,venue,externalIds,abstract&limit=100
- Blowhole 全文（PDF、7ページ）: http://graphicsinterface.org/wp-content/uploads/gi2018-18.pdf
- CipherFlute 現行稿（引用の有無を検査した対象）: `/Users/kurihara/Library/CloudStorage/GoogleDrive-qurihara@gmail.com/マイドライブ/share/google_desktop_share/ai-fue/paper/cipherflute_wiss2026_v1.2.docx`
