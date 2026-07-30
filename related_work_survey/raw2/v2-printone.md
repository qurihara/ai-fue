# v2 追検証: Printone を原典で確定し、印刷笛の音高精度をセントで報告した研究を整理する

検証日は2026年7月30日である。検証者は前段の調査とは別に、対象論文の本体（ACM Transactions on Graphics 版の全14ページ）を実際に取得して全文を読み、数値と語彙をすべて原文で照合した。前段の調査で未達成のまま残されていた「PrintoneのACM Transactions on Graphics版の本文に到達できていない」という項目は、この検証で解消した。

---

## 0. 結論の要旨

前段の報告は**おおむね正しいが、最も重要な数値の解釈に一箇所の重大な誤解がある**。

「56個の目標周波数のうち53個が実測範囲に入った」という記述は、短縮版（International Symposium on Musical Acoustics 2017）に一字一句そのまま存在する。しかし本体であるACM Transactions on Graphics版は、同じ評価について**まったく違う数え方をしており、「104個の目標周波数のうち、目標を出せなかったのは4個だけであった」と書いている**。さらに決定的なのは、この「実測範囲」がセント単位の精度を表す量ではまったくないという点である。実測範囲とは、**吹く速さを徐々に上げていったときに明瞭な音が鳴った最低周波数から最高周波数までの幅**である。つまりこの評価が言っているのは「奏者が吹き方を調整すれば目標音を出せる」ということであって、「設計どおりの音高が何セントの精度で出た」ということではない。Printoneの本文には「セント」という語が一度も現れない。

したがって、前段の「Printoneは目標周波数への合わせ込みを実機で検証しているため、CipherFluteの実測評価も同じ土俵で比較される」という警告は、**同じ土俵ではないという方向に修正されるべきである**。Printoneは吹き方で音高を動かせることを前提として、目標がその可動範囲に入るかどうかを見ている。CipherFluteは逆に、吹き方によるずれを基準笛で打ち消して離散スロットに落とすことを目指している。両者は音高の扱いに対する態度が正反対である。

一方で、「境界要素法で共鳴周波数を予測しながらフィップル吹き口を配置する」ことと「情報を符号として載せる発想がまったく無い」ことは、いずれも原典で完全に裏が取れた。

---

## 1. 対象論文の書誌を確定する

### 本体

Nobuyuki Umetani, Athina Panotopoulou, Ryan Schmidt, Emily Whiting, "Printone: Interactive Resonance Simulation for Free-form Print-wind Instrument Design", ACM Transactions on Graphics, 第35巻第6号, 論文番号184, pp. 184:1-184:14, 2016年11月11日（SIGGRAPH Asia 2016 Technical Papers, 12月5日から8日, マカオ）。所属はUmetaniとSchmidtがAutodesk Research、PanotopoulouがDartmouth CollegeとAutodesk Research、WhitingがDartmouth Collegeである。

- 書誌の確認先は https://doi.org/10.1145/2980179.2980250 に対するコンテンツネゴシエーションであり、著者4名・掲載誌名・巻号・ページ・出版年・出版者を直接取得して照合した。なおCrossrefに登録されている題名は副題のない「Printone」だけであり、ページは「1-14」と登録されている。
- **本文の確認先は https://www.dropbox.com/s/xyt2ixcpisl3wpi/2016_sigga_printone.pdf である。** これは著者本人が運営する研究室ページ https://cgenglab.github.io/en/publication/sigga16_printone/ が公開版として掲げているリンクであり、全14ページのPDFを取得できた。ACM Digital LibraryとDartmouth大学のページ（https://www.cs.dartmouth.edu/~athina/papers/a184-umetani.pdf）はいずれもHTTP 403を返して取得できなかったため、著者公開版で代替した。PDFの内部の題名情報にも「Printone: Interactive Resonance Simulation for ree-form Print-wind Instrument Design」と記録されており（先頭のFが欠けているのは製作時の不具合である）、本体であることを確認した。
- 補足資料の動画は https://www.youtube.com/watch?v=dWHYLqcCPuU で公開されている。

### 短縮版

Nobuyuki Umetani, Athina Panotopoulou, Ryan Schmidt, Emily Whiting, "Printone: Interactive Resonance Simulation for Print-wind Instrument Design", Proceedings of the 2017 International Symposium on Musical Acoustics, 6月18日から22日, モントリオール, カナダ, pp. 18-21, 2017年。

- 確認先は https://isma2017.cirmmt.mcgill.ca/proceedings/pdf/ISMA_2017_paper_47.pdf であり、全4ページの本文を取得した。各ページの下部に18から21までのページ番号が印字されていることも確認した。題名から「Free-form」が落ちている点は本体と異なる。
- 短縮版は本体を参考文献[1]として自己引用し、「ACM Trans. Graph., vol. 35, no. 6, pp. 184:1-184:14, Nov. 2016」と記載している。前段の報告が論文番号184の根拠としてこれを挙げていたのは正しい。

---

## 2. 確認事項への回答

### 2.1 境界要素法で共鳴周波数を予測しながらフィップル吹き口を配置するという記述は本当にあるか

**本当にある。完全に裏が取れた。**

境界要素法については、本体の概要が「we present a novel efficient method to estimate the resonance frequency based on the boundary element method by formulating the resonance problem as a minimum eigenvalue problem」と述べている。本文の第5節では、ヘルムホルツ方程式を境界要素法で離散化して A(k)p = f という行列形式に落とし、波数 k について非線形に変化する係数行列 A(k) の最小固有値が小さくなる波数を共鳴と定義している。第6節では、この非線形固有値問題を波数について一次のテイラー展開で近似し、一般化非エルミート固有値問題に帰着させて逆べき乗法で解くという高速化を示している。

吹き口の配置については、本体の第4節「User Interface」の冒頭が「The 3D user interface consists of geometric editing tools to place finger holes and the fipple.」と明記している。同節の「Geometric editing」の項は、利用者が物体表面をクリックしてフィップルと指孔を置き、フィップルの向きも調整できると述べている。しかも「Design procedure」の項は、フィップルの位置を変えると達成済みの共鳴周波数がすべて変わってしまうため、設計の最初に吹き口を置くよう推奨し、図17の形状ではフィップルの移動によって共鳴周波数が最大20ヘルツ変化したという実測値まで挙げている。つまり吹き口の配置と共鳴予測は明確に連動している。

フィップルを選んだ理由も明示されている。「Our mouthpiece is the fipple, which is commonly used for recorders or ocarinas.」と述べ、リードを避けた理由として「the vibration properties of reeds are very sensitive to material stiffness and thus are difficult to fabricate with commonly available FDM printers」と説明している。**家庭用の熱溶解積層方式で作りやすいからフィップルを選ぶという判断は、CipherFluteとまったく同じである。**

なお、フィップルの発音そのものは物理的に解いていない。本体の第3節は、吹き口の振動と共鳴の結合を無視して「passive resonator（受動共鳴器）」として扱うと明言し、結合を解くには計算流体力学による乱流解析が必要であるとしている。したがってPrintoneが計算しているのは共鳴器の共鳴周波数であって、笛が実際に鳴らす音そのものではない。

### 2.2 「16本を製作し56個の目標周波数のうち53個が実測範囲に入った」は本当にその論文に書かれているか。書かれているならその「実測範囲」は何セントに相当するか

これは**三つに分けて答える必要がある**。

**(a) 「16本」は本体に書かれている。** 本体の第9節「Results」の冒頭が「Figure 1, 10, 15 and 17 show sixteen wind instruments created using our tool.」と述べている。短縮版も「Figure 1 and Figure 3 show five out of sixteen wind instruments created using our tool.」と述べており、16本という総数は両版で一致する。

**(b) 「56個中53個」は短縮版にだけ書かれており、本体はまったく違う数を挙げている。** 短縮版の第5節は「We observe that the target frequencies generally (53 out of 56 target frequencies) fall within measured ranges」と書いており、前段の報告の引用は正確である。しかし本体の同じ「Accuracy」の段落は、次のように書いている。

> 「Among the 104 target frequencies we created with various instrument shapes, we experienced only 4 instances where the instrument could not play a target frequency: at the highest frequencies of BEETHOVEN, BUNNY, LIZARD and FLUTE3.」

つまり本体は**目標周波数を104個作って、出せなかったのは4個だけであった**と述べている。本体の全文を機械的に検索したが、「56」という数は14ページのどこにも現れず（唯一の一致はページ番号である）、「53」も参考文献のページ番号としてしか現れない。

この二つの数の食い違いについて、失敗した本数の側は説明がつく。本体が名指しした4本の失敗のうち、BEETHOVEN、BUNNY、LIZARDの3本は短縮版の図3にも載っている形状であり、残るFLUTE3は本体の図10にしかない笛である。したがって短縮版の「3個の失敗」は、短縮版が載せた範囲での失敗数として整合する。しかし**母数の側は整合しない**。本体の図17に列挙された笛の目標音数を合計すると65音になり、短縮版が言う56にも本体が言う104にも一致しない。短縮版の「56」がどの範囲を数えたものかは、両版の本文からは確定できなかった。**論文に書くのであれば、本体の「104個中4個が失敗」を使うべきである。** これが著者が全16本について報告した公式の数である。

**(c) 「実測範囲」はセント単位の精度ではない。ここが前段の報告の最大の誤解である。** 本体の該当箇所を引く。

> 「Red lines are the target frequencies, while the measured frequencies are shown as ranges between the light and dark green lines. This range occurs because the sound is influenced by the speed of blowing (higher speed produces higher frequencies). We gradually increased the blowing speed and recorded the lowest and highest frequencies that produce clear sound.」

すなわち実測範囲とは、**吹く速さを徐々に上げながら、明瞭な音が出た最低の周波数と最高の周波数を記録した幅**である。続く文が「i.e., the user can play the exact tones with proper blowing speed. This type of fine-scale tuning by adjusting the blowing speed is very common in wind instruments.」と述べているとおり、この評価の主張は「奏者が吹き方を選べば目標音に当てられる」ということである。設計誤差の大きさを示す量ではまったくない。したがって「53個が実測範囲に入った」を音高精度の実績として読むのは誤りである。

**本体の全文に「cent」および「cents」という語は一度も現れない。** 機械的な語境界検索で0件であることを確認した。Printoneはセント単位の精度をいっさい報告していない。

ただし本体には、セントに換算できる数値がいくつか別の文脈で書かれている。以下の換算は検証者による計算であり、論文が書いた値ではないことを明記する。

| 論文が報告している値 | 出典箇所 | 検証者によるセント換算 |
| --- | --- | --- |
| 失敗した4個は目標より最大3パーセント低い（「These frequencies are at most 3% lower than the target frequency」） | 本体 第9節 Accuracy | 約マイナス52.7セント |
| 受動共鳴の実測とシミュレーションの差は最大10ヘルツ（「We observed up to 10 Hz deviation between the simulation and the experiment」、立方体は一辺4センチメートル） | 本体 第9節 Accuracy | 1000ヘルツ付近で約17.2セント、1500ヘルツで約11.5セント、3000ヘルツで約5.8セント |
| フィップルの位置を移すと共鳴周波数が最大20ヘルツ変化する | 本体 第4節 Design procedure | 1000ヘルツ付近で約34.3セント |
| 感度解析による一次近似の誤差は10パーセント未満（孔径の変化が半音相当のとき） | 本体 第7節 | 対話中の粗い近似の誤差であり、完成品の音高精度ではない |

論文自身が精度の妥当性を主張する論拠は、「Since changes in the blowing speed can easily compensate for a 10Hz error, we believe the parameters we used are reasonable.」という一文である。**10ヘルツ程度の誤差は吹き方で吸収できるから十分だ**という立場であり、CipherFluteが必要とする「吹き方によらず離散スロットに落ちること」とは要求が真逆である。同様に材料の議論でも「at the object scales we explored, fabrication error is small compared to the range of frequencies the mouthpiece can produce by changing the blowing speed」と述べており、造形誤差を吹奏可変範囲より小さいという相対評価で片づけている。

### 2.3 複数の音を1つの物体で出す設計を扱っているか。同時発音か切り替えか

**扱っている。ただし完全に切り替えであり、同時発音ではない。**

本体は1つの物体に1つのフィップルと3個から5個の指孔を設け、指孔の開閉の組合せで4音から9音を出している。図17に列挙された笛の内訳は、指孔3個で4音または5音、指孔4個で6音から8音、指孔5個で9音（DOUGHNUT）である。本体は「we have been able to achieve between 5 to 8 target frequencies for the shapes we have tested, with three to four finger holes」と述べ、設計手順の節では「N holes are sufficient to produce N+1 target tones」「there are actually 2^N finger configurations for N holes, fewer holes can also be used」と、指孔の組合せ論を明示的に使っている。

同時発音については、本体の全文に「simultaneous」「chord」「polyphony」に相当する語が**いずれも0件**である。基本周波数のみを対象とし、倍音も音色も扱わないと繰り返し明言しており（「we do not simulate the timbre of the instrument」）、出力は常に単音である。目的も単音の旋律を奏でること（「play a specific song」「familiar songs」）に限られている。吹き口も1個だけであり、複数のフィップルを1物体に共存させる設計は現れない。

したがって「1つの印刷物から複数の異なる音高を得る」ことそれ自体は、Printoneが2016年に達成済みである。**しかもDOUGHNUTは1物体で9個の異なる音高を出しており、CipherFluteの13スロットという語彙の大きさと桁は同じである。** ここはCipherFluteが新規性として主張してはいけない部分である。区別できるのは、Printoneが「1本の笛を指で切り替えて旋律を奏でる」構成であるのに対し、CipherFluteが「多数の単音笛を並べて順に吹き、音高の並びを符号列として読む」構成である点だけである。

### 2.4 情報を符号として載せる発想がまったく無いことの確認

**まったく無い。機械的な語彙検索で確定した。**

本体の全文（14ページ、約11万文字の抽出テキスト）に対して語境界つきの検索を行った結果は次のとおりである。

| 語 | 出現回数 | 備考 |
| --- | --- | --- |
| bit / bits | 0 / 0 | |
| code / codes / coding | 0 / 0 / 0 | |
| encode / encoding / decode | 0 / 0 / 0 | |
| information | 1 | 「the sensitivity information（感度情報）」を使って孔径を最適化するという文脈だけである |
| data | 1 | 「measured ground truth data（実測の真値データ）」という文脈だけである |
| secret | 0 | |
| message | 0 | |
| identification | 0 | |
| identify | 1 | 「To identify the resonance frequencies（共鳴周波数を同定するには）」という文脈だけである |
| tag / tags | 0 / 0 | |
| watermark | 0 | |
| steganography | 0 | |
| cryptography | 0 | |
| key | 0 | |
| storage / store | 0 / 0 | |
| capacity | 0 | |
| symbol / alphabet | 0 / 0 | |

「情報」「符号」「ビット」「秘密」「識別子」「記憶」「容量」に相当する語が、情報を物体に載せる意味では**一度も使われていない**。Printoneの目的は一貫して「自由形状の物体を機能する管楽器に変えて旋律を奏でさせること」であり、限界と将来課題の節も音色のシミュレーションと吹き口の設計最適化を挙げるにとどまる。**この確認は、CipherFluteの符号化という貢献がPrintoneに先取りされていないことを積極的に支持する証拠である。**

### 2.5 追加の重要な発見: 造形方法が根本的に違う

前段の報告には現れていないが、論文に書くうえで決定的に重要な差がある。Printoneの造形は次のとおりである。

> 「We print the designed wind instruments using PLA filament on a MakerBot Replicator 2 printer, which is a widely available printer/material combination. In order to create an empty cavity inside the shape, we cut the model in half, print each half separately, and then glue the halves together. The cutting was done manually using a standard mesh editing software, with the cut placed such that we can remove the support material inside the cavity after printing.」

つまりPrintoneは、**空洞を作るために模型を手作業で半分に割り、別々に印刷し、内部のサポート材を取り除いてから接着している**。粉末方式の装置なら分割は不要だと述べているが、実際に使ったのは家庭用の熱溶解積層方式の装置である。材料の影響を調べるために追加でPolyJet方式（Objet Connex 260、VeroWhitePlus材）と光造形方式（Autodesk Ember、紫外線硬化樹脂）でも印刷しているが、基本音に可聴な差はなかったと報告している。

CipherFluteは、円筒を軸方向に半分に割った断面という形を選ぶことで、**サポート材なしの平置き一体印刷**を実現し、分割も接着も後処理も要らない。さらに同じ物体に多数本を融合できる。この造形上の性質は、Printoneが明示的に妥協した点をまさに解消するものであり、CipherFluteの実装上の貢献としてはっきり主張できる。逆にPrintoneを引用しないままだと、この差が読者に見えない。

---

## 3. 印刷した笛の音高精度をセント単位で報告した研究の整理

### 3.1 Matthew Dabin ら（NIME 2016）の数値は原典で完全に一致した

Matthew Dabin, Terumi Narushima, Stephen Beirne, Christian Ritz, Kraig Grady, "3D Modelling and Printing of Microtonal Flutes", Proceedings of the 16th International Conference on New Interfaces for Musical Expression (NIME 2016), pp. 286-290, 2016年7月11日から15日, グリフィス大学, ブリスベン。

確認先は https://www.nime.org/proceedings/2016/nime2016_paper0056.pdf であり、本文と表1を取得して照合した。書誌は https://nime.org/proc/nime2016_dabin/ で確認した。

表1の原文の数値をそのまま書き出す。第7から第12下方倍音にあたる6音と、オーバーブローによる2音について、目標周波数との差をセントで報告している。

| 下方倍音 | 目標(ヘルツ) | リコーダー1(ヘルツ) | 差(セント) | リコーダー2(ヘルツ) | 差(セント) | リコーダー2改(ヘルツ) | 差(セント) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 12分の1 | 616 | 628 | +34 | 617 | 1 | 612 | -10 |
| 11分の1 | 672 | 681 | +23 | 664 | -21 | 673 | 5 |
| 10分の1 | 739 | 749 | +24 | 738 | -3 | 745 | 14 |
| 9分の1 | 821 | 828 | +14 | 810 | -24 | 815 | -13 |
| 8分の1 | 924 | 932 | +16 | 908 | -30 | 923.5 | -1 |
| 7分の1 | 1056 | 1060 | +6 | 1031 | -40 | 1049 | -12 |
| 12分の1（オーバーブロー） | 1232 | 1246 | +19 | 1228 | -5 | 1236 | 5 |
| 11分の1（オーバーブロー） | 1344 | 1359 | +20 | 1335 | -11 | 1351 | 9 |

前段の報告が挙げた数値は**すべて正しい**。リコーダー1は+6から+34セント、リコーダー2は-40から+1セント、指孔2個をやすりで手修正したリコーダー2改は-13から+14セントである。

目標についても原文を確認した。「our goal is to continue to improve the pitch accuracy of our 3D-printed designs to no more than a five cent error so that manual adjustments are not needed.」であり、5セント以内という将来目標も正しい。

評価方法は、無響環境でBehringer ECM8000測定用マイクロフォンとBehringer ADA8000プリアンプで録音し、Melodyneソフトウェアで音高を求めるものである。

### 3.2 同じ研究グループの短報が「既存モデルは30セント程度」という有用な基準を与えている

Christian Ritz, Matthew Dabin, Terumi Narushima, Kraig Grady, Stephen Beirne, "3D printing for custom design and manufacture of microtonal flutes", SPIE Newsroom, 2015年9月18日。書誌の確認先は https://doi.org/10.1117/2.1201508.006082 であり、本文は https://spie.org/news/6082-3d-printing-for-custom-design-and-manufacture-of-microtonal-flutes で取得した。

この短報は「existing mathematical models gave approximate solutions to finger hole locations, usually with an accuracy of 30 cents compared with the desired frequency」と述べ、続けて「Our goal is to achieve no more than a five-cent error, which we consider to be an acceptable deviation for wind instruments such as the flute」と書いている。

**「既存の数理モデルによる指孔位置の解は目標周波数に対して通常30セント程度の精度である」という一文は、CipherFluteが100セント刻みという粗い量子化を選ぶ判断を外部から裏づける、きわめて使いやすい基準である。** 前段の報告にはこの30セントという数値が現れていなかったので、新たな収穫として記録する。ただし査読論文ではなく学会の広報媒体の短報であることに注意が必要である。

### 3.3 セント単位の報告はDabinらがほぼ唯一であることを、前段の資料群全体に対して機械的に確認した

前段の調査で取得された文献群（作業領域に蓄積されていた抽出テキスト群、印刷楽器・受動音響タグ・音響センシング・物理符号など全切り口にわたる119件のテキストファイル、うち内容のある3000文字超のものが106件、合計約768万文字）に対して、語境界つきで「cent」および「cents」を機械的に検索した。結果は次のとおりである。

- **印刷した楽器の音高精度をセントで報告しているのは、Dabinら（NIME 2016）ただ1件であった。**（「cents」が5件、「cent」が1件であり、いずれも音高の差または5セント以内という目標の文脈である。）
- Printone は本体（ACM Transactions on Graphics 2016）も短縮版（International Symposium on Musical Acoustics 2017）も、ともに0件である。
- FlueBricks（CHI 2026）は0件である。
- Blowhole（Graphics Interface 2018）は0件である。
- 残る一致はすべて通貨のセント（封印の単価が75セント、無線タグの単価が10セントなど）であり、音高とは無関係であった。

したがって前段の「音高精度をセント単位で報告した査読文献はDabinらがほぼ唯一である」という判断は、**この文献群のもとで正しい**と確認できた。しかもDabinらの装置はPolyJet方式であり、家庭用の熱溶解積層方式で多数本の笛の音高分布をセントで測った報告は、依然として見つかっていない。

### 3.4 参考: 楽器音響の分野にはセント単位の報告があるが、印刷とは結びついていない

Nathan Szwarcberg, Tom Colinot, Christophe Vergez, Michaël Jousserand, "Geometric sensitivity of modal parameters in wind instrument models: a case study on saxophone intonation", Acta Acustica, 第9巻, 論文番号57, 2025年。確認先は https://doi.org/10.1051/aacus/2025039 に対するコンテンツネゴシエーションと、本文 https://acta-acustica.edpsciences.org/articles/aacus/full_html/2025/01/aacus250082/aacus250082.html である。

サクソフォンの音程の非調和性をセントで報告しており（例として上流側の孔で最小プラス68.8セント、下流側の孔でプラス18.6セント、レジスターホールの半径を0.2ミリメートル小さくすると3.4セント改善するという見積もり）、幾何形状の微小な変化が音程に効く感度を定量化している。3Dプリントは扱わず、情報の符号化も扱わない。

**この研究は、CipherFluteが「寸法の小さな誤差が音高に効く」ことを述べる際の音響学側の裏づけとして使える。** 同時に、セント単位で音程を論じることは楽器音響では当然の作法であって、CipherFluteがセントで測ること自体には新規性がないことも示す。

---

## 4. demakein と openwind の位置づけ

### demakein

作者はPaul Francis Harrisonである。公式ページ http://www.logarithmic.net/pfh/design の自己説明は「Software to design and make woodwind instruments using a 3D printer or CNC mill. The 'design' phase determines the size and placements of holes, and shape of the bore.」である。つまり**設計段階で孔の寸法と位置、およびボアの形状を決める**ソフトウェアである。組み込みの楽器はフルート、ホイッスル（フィップル笛）、ショームであり、いずれも移調や変形の指定ができるパラメトリックな楽器として用意されている。Pythonに慣れた利用者は「play exactly the scale you want」（望む音階をそのまま鳴らす）ように独自の楽器を記述できると書かれている。バージョン1.1が2025年7月に公開され、Python 3へ移行している。

**査読論文としての位置づけはまったく無い。** 公式ページに論文の引用はなく、学術的な発表媒体を持たない。ただしDabinら（NIME 2016）が参考文献[10]としてこのソフトウェアを引用しているので、印刷楽器の分野の査読論文がこの道具を認知していることは確認できる。

なお、公式ページが自動最適化を行うと明言しているかどうかは、今回の取得でも断定できなかった。前段の報告が書いた「与えた運指と音階に対して正しい音が出るように数値最適化する」という記述のうち、「孔の寸法と位置とボア形状を設計段階で決める」ことは自己説明のとおりであるが、それが最適化アルゴリズムによるものだという明示は公式ページには見当たらない。実装コードを読まないかぎり断定できない。

### openwind

InriaのMakutuチームが開発するPythonライブラリであり、ライセンスはGPL-3.0である。公式ページ https://openwind.inria.fr/ が挙げる機能は三つである。第一に入力インピーダンスの計算であり、放射、断面変化、側孔、各種のボア形状を扱う。第二に音のシミュレーションであり、リードや唇の力学と管の音響を結合して時間領域の有限差分で解く。第三に楽器形状の最適化であり、**測定したインピーダンスからボア形状を復元する逆問題を含む**。

**openwindには査読論文としての位置づけが明確に存在する。** 三つ確認した。

1. Augustin Ernoult, Christophe Vergez, Samy Missoum, Philippe Guillemain, Michael Jousserand, "Woodwind instrument design optimization based on impedance characteristics with geometric constraints", The Journal of the Acoustical Society of America, 第148巻第5号, pp. 2864-2877, 2020年11月1日。確認先は https://doi.org/10.1121/10.0002449 に対するコンテンツネゴシエーションである。
2. Augustin Ernoult, Juliette Chabassier, Samuel Rodriguez, Augustin Humeau, "Full waveform inversion for bore reconstruction of woodwind-like instruments", Acta Acustica, 第5巻, 論文番号47, 2021年。確認先は https://doi.org/10.1051/aacus/2021038 に対するコンテンツネゴシエーションである。
3. A. Ernoult, J. Cabaret, J. Chabassier, "Openwind: a software to simulate wind instruments, as a tool for acoustic teachers", Proceedings of the 10th Convention of the European Acoustics Association Forum Acusticum 2023, pp. 4873-4876, 出版者はEuropean Acoustics Associationである。確認先は https://doi.org/10.61782/fa.2023.0233 に対するコンテンツネゴシエーションであり、公開版は https://inria.hal.science/hal-04217988 にある。これは道具そのものを主題とする査読つき会議論文である。

したがって前段の整理は正しい。**「管の形状から音高を求める順問題」も「音の測定から管形状を復元する逆問題」も、査読論文として確立した技術である。** とくに逆問題の存在は、CipherFluteが脅威モデルで宣言している「物理層に秘匿の力はない」という主張を補強する材料になる。音を録るだけでも管の形状が推定できる技術が公開ライブラリとして存在するのだから、「音を録られたら読まれる」という前提は誇張ではなく実在の技術に裏づけられている。

なお、openwindの公式ページのうち、引用先を列挙しているとされる contributions.html と publications.html はいずれもHTTP 404を返した。上記の3件は検索結果とHAL、およびCrossrefの登録情報から確定した。

---

## 5. 前段の報告に対する判定

### 正しかったこと

- Printoneが境界要素法で共鳴周波数を予測し、フィップル吹き口と指孔を配置する対話的な設計道具であること。
- フィップルを選んだ理由が家庭用の熱溶解積層方式で作りやすいことであり、CipherFluteと同じ発音機構であること。
- 16本の楽器を設計・印刷したこと。
- 短縮版に「56個の目標周波数のうち53個が実測範囲に入った」と書かれていること（引用そのものは正確である）。
- 共鳴を非線形行列の最小固有値問題として定式化し、一次のテイラー展開で一般化固有値問題に帰着させていること。
- 指孔径の連続変更中は感度解析による一次近似で毎秒30フレーム以上を保ち、待機中に数秒かけて精確な計算を回すこと。
- 目標周波数を複数の運指について指定して指孔径を自動最適化するAutoTune機能があること。
- 音色を扱わず基本周波数だけを対象とすると明記していること。
- 短縮版が道具全体の平均動作速度を毎秒5フレームと報告していること。
- Dabinら（NIME 2016）が報告したセント値と、5セント以内という将来目標を掲げていること。
- 印刷楽器の音高精度をセントで報告した査読文献がDabinらほぼ唯一であること。
- demakeinが査読論文を持たない設計道具であり、openwindが査読論文に裏づけられた順問題と逆問題の道具であること。

### 誤り、または重大に不十分だったこと

1. **「実測範囲」の意味を取り違えている。** これが最大の誤りである。実測範囲は吹く速さを上げながら明瞭に鳴った最低周波数から最高周波数までの幅であり、設計精度を表す量ではない。前段の要約は文言としては「吹く速さを徐々に上げながら明瞭に鳴る最低周波数と最高周波数を記録し」と正しく書いているのに、脅威の判定では「Printoneが目標周波数への合わせ込みを実機で検証しているため、CipherFluteの実測評価も同じ土俵で比較される」と結論しており、両者が同じ土俵だという誤った含意を残している。実際には音高精度に対する要求が正反対である。
2. **本体の公式の数値である「104個中4個が失敗」を見落としている。** 短縮版の「56個中53個」だけを引いており、しかも「16本を製作し56個の目標周波数のうち」と続けたために、56個が16本すべてを数えたものだと読める。本体は104個を数えている。論文に書くなら104個中4個を使うべきである。
3. **Printoneがセントをいっさい報告していないという事実を明示していない。** 前段は「セント換算の定量値を取れていない」と未達成項目に書いていたが、正しくは「原典にセント表記が存在しない」である。これは調査の欠落ではなく原典の性質である。
4. **造形方法の根本的な違いを見落としている。** Printoneは模型を半分に割って別々に印刷し、内部のサポート材を除去して接着している。CipherFluteのサポートなし一体平置き印刷との差は、実装上の貢献として主張できる重要な論点である。
5. **1つの物体から出せる音高の数を押さえていない。** Printoneは指孔5個のDOUGHNUTで9音を出している。CipherFluteの13スロットと桁が同じであり、「1つの印刷物から多数の音高を出す」ことを新規性に数えられないという厳しい事実である。
6. **Ritzらの短報にある「既存モデルは30セント程度の精度」という数値を拾っていない。** CipherFluteの100セント刻みを正当化する最良の外部基準である。

---

## 6. この文献群のもとでCipherFluteに残る新規性の厳しい判断

前段は「Printoneが印刷された笛の計算設計という技術的貢献をほぼ完全に先取りしている」と判定した。原典に当たった結果、**この判定は結論としては維持されるが、理由は前段が書いたものとは違う**。

まず、崩れた主張を並べる。第一に、「管の長さと音の高さの対応を計算して笛の形を決め、家庭用の熱溶解積層方式で印刷し、狙った音高が出ることを実機で確かめる」という工程は、Printoneが2016年に、より一般的な自由形状に対して、より厳密な物理（境界要素法による三次元の波動方程式）で達成している。しかもPrintoneが引く先行研究のとおり、円筒管の共鳴を管長から求める一次元モデルは、Printone自身が「既知の単純な近似式」として本文の図3で紹介して脇に置いた出発点である。CipherFluteの f = A/(L+e) は、まさにその脇に置かれた側の式である。**したがって「管長と周波数の対応式を作った」ことに新規性はいっさい無い。**これは10年前の論文が前提として図解している既知の関係であり、demakeinが2012年から実装し、openwindが査読論文つきで一般化している領域である。CipherFluteは較正定数AとeをPETGや自機の造形条件に合わせて実測で当てはめたにすぎず、それは工学的な較正であって学術的な新規性ではない。

第二に、「1つの印刷物から複数の音高を出す」ことにも新規性が無い。Printoneは指孔の組合せで最大9音を1物体から出している。

第三に、「印刷した笛の音高を実機で測って目標と比べる」ことにも新規性が無い。PrintoneとDabinらの両方がやっている。

次に、残る新規性を述べる。**残るものは、前段が書いたとおり「符号化」の側にあり、それは原典の確認によってむしろ強固になった。** 具体的には次の四つである。

1. **音高の並びを符号語として読むという発想そのものが、Printoneに完全に存在しない。** 語彙検索で「bit」「code」「encode」「information」「data」「secret」「message」「capacity」「symbol」がいずれも情報を載せる意味では0件であることを確認した。Printoneの音高は演奏されるための音であって、読み取られるための記号ではない。この差は言葉遊びではなく、設計目標が根本的に違うことの帰結である。Printoneは「吹き方で音高を動かせるから目標に当てられる」ことを長所として報告する。CipherFluteは「吹き方で音高が動くこと」を打ち消すべき雑音として扱う。**同じ物理現象に対して、一方が可変性を資源とみなし、他方が可変性を敵とみなしている。** ここがCipherFluteの土台である。
2. **音高が既知の基準笛を同居させて比で読む較正は、この文献群に見つからなかった。** Printoneは吹く速さによる幅を「奏者が調整すればよいもの」として受け入れ、Dabinらは奏者の影響を「常に存在するもの」として受け入れる。物体の中に較正用の音源を混ぜて相対量で読む設計は、通信のパイロット信号からの転用としてCipherFlute固有と言える。
3. **誤り訂正符号と隣接同音禁止の制約を、物理的な形状設計の制約として持ち込む発想は見つからなかった。** Printoneが解いているのは「目標周波数を達成する形状を探す」最適化であり、「読み出し誤りに耐える符号語の集合を設計する」問題ではない。
4. **サポート材なしで平置き一体印刷できる小型フィップル笛を、多数本融合して日用品に偽装して埋め込む構成は見つからなかった。** Printoneは1物体を1つの楽器にし、しかも空洞を作るために分割と接着を要した。CipherFluteは分割も接着も要らない。ただし「多数の管を1つの印刷物にまとめる」ことそのものには前例があるので（前段が挙げたSzabóのパンフルート合奏体、FlueBricksの息を分配する連結部）、融合そのものではなく「単音笛を情報担体として日用品に偽装する」点に限って主張すべきである。

以上を踏まえた厳しい結論は次のとおりである。**CipherFluteは「管の長さと音の高さの対応式にもとづく符号化」という貢献の主張のうち、前半の「対応式」を新規性として掲げてはならない。掲げれば直ちに反証される。主張できるのは後半の「符号化」だけである。** すなわち貢献の言い方は、「既知の管長と周波数の関係を、離散スロットからなる符号の語彙として再定義し、基準笛による正規化と誤り訂正と隣接制約を伴う読み出し系として組み立てた」という形に限定すべきである。設計計算の新規性は明示的に放棄したほうが、査読者に対してかえって強い立場になる。

そして実務上の指示を一つ加える。**Printoneは必ず引用しなければならない。** 引用しないことの危険は前段が書いたとおりだが、引用したうえで書くべき差分は前段が想定したものとは違う。書くべきは「対話的な自由形状設計が不要な理由」ではなく、**「Printoneが長所として報告した吹奏による音高可変性が、情報を読み出す目的では最大の敵になること」**である。この一文があれば、CipherFluteが基準笛と100セント刻みという設計を選んだ理由が、先行研究との関係のなかで自然に説明される。あわせてDabinらの数十セント規模の実測値とRitzらの「既存モデルは30セント程度」という基準を並べれば、100セント刻みという粗い量子化は妥協ではなく必然として読める。

---

## 7. 確認できなかったこと

1. **短縮版の「56個の目標周波数」がどの範囲を数えたものかを確定できなかった。** 本体の図17に列挙された笛の目標音数の合計は65であり、56とも104とも一致しない。本体と短縮版のいずれの本文にも母数の内訳が書かれていない。失敗した3本が短縮版の図に載っている3本（BEETHOVEN、BUNNY、LIZARD）と整合することは確認したが、母数の56は説明がつかないまま残った。
2. **Printoneの実測範囲の幅そのものを数値で取り出せなかった。** 幅は図17と図10のグラフとして示されるだけで、最低値と最高値の表は本文に無い。したがって「吹き方で何セント動くのか」という、CipherFluteにとって最も知りたい数値は原典から読み取れない。図の画素を測れば概算できるが、それは論文に書ける精度の値ではない。もし論文で「吹奏による音高変動が数十セント規模である」と書きたいなら、CipherFlute自身の実測で示すべきである。
3. **Printoneの補足資料（Appendix Aを含む supplemental material）を取得していない。** 本文が「see (A.5) in the supplemental material」と参照しており、スケーリング不変性の証明が入っている。符号化には影響しないが、一次元近似との関係を数理的に厳密に書きたい場合は必要になる。
4. **demakeinが実際に最適化アルゴリズムを使っているかを、実装コードで確認していない。** 公式ページの自己説明は「孔の寸法と位置とボアの形状を決める」までであり、それが最適化によるものかどうかは断定できない。CipherFluteの経験式との包含関係を厳密に述べるには、リポジトリのコードを読む必要がある。
5. **openwindの公式な引用要請ページに到達できていない。** contributions.html と publications.html はいずれもHTTP 404であった。上記の3件は検索結果、HAL、Crossrefから確定したが、プロジェクトが「これを引用せよ」と指定している論文がどれかは確認できていない。
6. **Printone以後の被引用をたどっていない。** Printoneを引用した後続研究のなかに、音高を符号として読む方向へ進んだものがあるかどうかを確認していない。Semantic Scholarの被引用一覧を当たるべきである。
7. **前段が未確認として残した Blowhole の本文の数値は、この検証でも解消していない。** 抽出テキストは作業領域に存在するものの、本検証の対象範囲外としたため、識別クラス数や正解率をあらためて照合していない。CipherFluteの最重要の比較対象であるから、別途確定させるべきである。
