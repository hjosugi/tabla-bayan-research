# FINDINGS — 主張台帳

会話・文献・論文から得た知見を 1 主張 = 1 エントリで固定する。docs/ は読み物、ここが正典。

- status: **確定** (3+ 独立ソース一致) / **有力** (2 ソース or 論文 1 + 整合) / **割れる** (ソース間で不一致) / **推定** (自前モデル、未検証) / **棄却** / **未検証**
- kw: 検索用キーワード (日/EN/HI/BN)。`tools/notes_search.py` と grep の両方で引く前提

---

## P: 物理

### P-01 減衰の 4 因子モデル
- status: 推定 (物理的に妥当だが定量未検証)
- claim: damping ≒ 接触面積 × その点の膜変位 × 接触物の損失係数 × 接触時間。変位項が支配的
- kw: 減衰 damping 変位 displacement 損失係数 loss factor 接触時間 contact time

### P-02 時間スケール
- status: 有力
- claim: バヤン基音 ~80-120 Hz、1 周期 ~10 ms。指が数 ms で離れれば打撃、数十 ms 残れば吸収体
- kw: 基音 fundamental 周期 period 接触 contact ms

### P-03 変位プロファイル
- status: 確定 (膜振動論の基礎)
- claim: 膜は縁で固定。基音モードの変位は中央付近で最大、縁でほぼゼロ。触る位置で減衰が桁で変わる
- kw: 節 node 腹 antinode モード mode 縁 edge किनार কিনার

### P-04 硬い接触は境界、柔らかい接触はダンパー
- status: 有力
- claim: 硬く据えた手 = 低損失境界として反射。脱力した手 = 粘弾性ダンパーとして吸収。「触るか」ではなく「どの硬さで触るか」
- kw: 境界 boundary 反射 reflection 粘弾性 viscoelastic 脱力 硬さ stiffness

### P-05 手首 = 可動境界
- status: 有力 (T-01/T-05 と整合、直接実測なし)
- claim: マイダーンに据えた手首は膜を 2 セグメントに分割し、手首より奥のセグメントが鳴る。圧増 → 有効面積縮小 + 張力増 → ピッチ上昇。トーキングドラムと同原理
- kw: 手首 wrist कलाई मणिबंध কব্জি 境界 segment ピッチベンド pitch bend talking drum

### P-06 タブラの調和倍音列 (Raman 1920)
- status: 確定
- claim: 倍音が 1:2:3:4:5 の調和列。膜楽器として例外的。最初の 5 共鳴は 9 個の固有モードに対応
- kw: Raman 倍音 harmonic overtone 調和 1:2:3:4:5 Nature 1920

### P-07 キナールは設計上のダンパー
- status: 確定 (Raman、2025 論文で再確認)
- claim: キナールは膜と完全密着せず、ピッチではなく高次非調和モードの抑制に働く
- kw: キナール kinar chat किनार চাঁটি 非調和 inharmonic 抑制 suppression

### P-08 複合膜理論 (Ramakrishna & Sondhi 1954)
- status: 確定
- claim: 面密度に段差を持つ複合膜として理想化。半径比 0.4・密度比 3.125 で第 9 モードまでほぼ調和。縮退モード多数
- kw: 複合膜 composite membrane 半径比 密度比 縮退 degenerate Ramakrishna Sondhi

### P-09 バヤンのスィヤヒは偏心
- status: 確定 (NCERT + ESPI 実測 + モード計算論文)
- claim: 偏心ロードがモード縮退を破り非対称振動パターンを作る。ダーヤー (同心) と別物。手首の効きは角度依存
- kw: 偏心 eccentric スィヤヒ syahi स्याही গাব 非対称 asymmetric ESPI

### P-10 空気負荷の効果
- status: 確定 (Khula bols 論文)
- claim: 空気負荷はダーヤーでは調和性の微調整、バヤンでは調和性を大幅改善し、音楽的に重要なモードの減衰時間を延長
- kw: 空気負荷 air loading 減衰時間 decay time khula bols

### P-11 スィヤヒのひび割れ網は工法
- status: 確定
- claim: 層を重ね乾燥・研磨して意図的にひび割れ網を作り、付加質量の剛性を下げる。ひび自体は故障ではない。縁の浮き・剥がれは故障
- kw: ひび crack reticulum 剛性 stiffness 剥がれ delamination

### P-12 強打の非線形化
- status: 推定 (もっともらしいが出典なし)
- claim: 強打で膜が非線形領域に入り基音以外にエネルギーが散る。弱打のほうが伸びる
- kw: 非線形 nonlinear 強打 hard strike

---

## T: 奏法

### T-01 手首はマイダーンの中に据える
- status: 確定 (NCERT / Sangtar / TaalGyan / Sachitra Tabla Shiksha)
- claim: 手首の付け根を面上のマイダーンに置いたまま打つ。浮かせない
- 注: R-01 (棄却済み初期仮説) を置換
- kw: 手首 wrist कलाई मणिबंध মণিবন্ধ মায়দান 据える rest maidan

### T-02 スィヤヒ偏心は手首の席
- status: 確定 (NCERT 第 2 章に明記)
- claim: バヤンのスィヤヒが偏心しているのは、手首を置いて演奏する前提の設計だから
- kw: 偏心 offset 設計 design डग्गा dagga

### T-03 指は 90 度、先端で打つ
- status: 確定
- claim: 指を 90 度に曲げ第一関節の先で打つ。「蛇のフードのように」(সাপের ফণার মত) アーチを保つ。寝かせると Ka 化
- kw: 90度 fingertip 指先 アーチ snake hood সাপের ফণা अँगुली আঙ্গুল

### T-04 打点はスィヤヒとキナールの間
- status: 確定
- claim: マイダーン (लव) を打つ。スィヤヒ上は質量が乗っていて伸びない
- kw: 打点 strike point マイダーン maidan lav लव ময়দান

### T-05 圧ゼロの Ghe は存在しない
- status: 確定 (Chordia/CCRMA + 各教本)
- claim: Ghe は全ボル中唯一の連続可変音。打つ瞬間の掌圧が音程を作る。ベースラインは「軽い圧」であり「無圧」ではない
- kw: 圧 pressure दबाव চাপ 変調 modulation 連続可変 continuous

### T-06 打った指は即離す、手首は動かさない
- status: 確定
- claim: 減衰源は残留した指。手首は固定された橋脚、動くのは指だけ
- kw: 離す release 残留 lingering 固定 anchor

### T-07 連打は指を浮かせて待機
- status: 有力
- claim: 連打が閉じる原因は次打準備で指が面に戻ること。面上 2-3 cm で待機、人差し指・中指の交互推奨
- kw: 連打 repeated strokes 交互 alternate 待機 hover open

### T-08 ボル分類 (誤爆診断)
- status: 確定
- claim: Ghe/Ge = 据えた手首 + 立てた指先、有音程開音。Ka/Ke = 平手、無音程閉音。Ghissa = 打後スライドで共鳴を閉じるベンド。指の角度だけで Ghe と Ka が分かれる
- kw: ボル bol घे गे के घिस्सा ঘে গে Ka Ke Ghissa 開音 閉音 khula band

### T-09 指の使い分けはソース間で割れる
- status: 割れる
- claim: NCERT = 中指+薬指 / Sangtar = 人差し指(Ge)・中指(Ghe) / TaalGyan・Bengali 教本 = 中指系。手首の厳密位置も「マイダーン内」〜「スィヤヒ縁のすぐ外」で幅
- kw: 中指 middle finger 人差し指 index 薬指 ring 流派差 variation

### T-10 ガラーナーは 2 哲学に大別
- status: 有力 (Courtney)
- claim: Delhi 系 (Delhi, Ajrada) と Purbi 系 (Lucknow, Farrukhabad, Benares)。現代では単一ガラーナー厳守は職業的に不利
- kw: ガラーナー gharana घराना Delhi Purbi Ajrada Benares

### T-11 変調は口伝領域、上限は高い
- status: 有力
- claim: 左手ベンドの具体的推奨は文字化されていない (Courtney 本人が明言)。圧+スライドだけでメロディ演奏が可能な水準まである (Zakir Hussain)
- kw: 変調 modulation 口伝 oral tradition Zakir Hussain スライド slide

---

## D: 診断

### D-01 楽器切り分けテスト
- status: 確定 (自明な手続き)
- claim: 左手を離し右手指 1 本でマイダーンを軽打即離。1 秒以上鳴れば楽器正常、原因は左手
- kw: 切り分け isolation テスト test 診断 diagnosis

### D-02 ピッチベンドテストは決定的
- status: 確定 (本件で実証)
- claim: 圧をかけピッチを変えながら打って尾が伸びるなら、楽器・打点・インパルス全部正常。差分は打後の左手の質のみ。ユーザー自身の観察が診断を確定させた
- kw: ピッチベンド pitch bend 尾 tail sustain 診断 decisive

### D-03 「まったく違う音」= 意図しない Ka
- status: 有力
- claim: 指が寝る/手首不在だと境界条件が変わり別のボルになる。「パタ/ボフ」無音程音は Ka 化のサイン
- kw: 誤爆 wrong bol パタ ボフ slap 無音程 unpitched

### D-04 腕の疲労はフォーム誤りのセンサー
- status: 有力
- claim: 正しい Ghe は指の跳ね返しのみで腕をほぼ使わない。疲労ループ: 指残留で減衰 → 力不足と誤解釈 → 腕から強打 → 過負荷
- kw: 疲労 fatigue センサー sensor フォーム form 強打

---

## E: 楽器・環境

### E-01 日本の夏の湿度
- status: 有力
- claim: 皮が湿気を吸うと重くなりまず伸びなくなる。除湿部屋に半日 / 演奏前に温める
- kw: 湿度 humidity 皮 skin 夏 August 日本

### E-02 バヤンのチューニング手段
- status: 確定 (Courtney maintenance)
- claim: ガジャラーをハンマーで上から叩くと締まり下から叩くと緩む。バヤンはガッター (木駒) の挿入・上下でも調整
- kw: チューニング tuning ガッター gatta ガジャラー gajara ハンマー hammer

### E-03 バヤンの音程慣習
- status: 未検証 (フォーラム 1 件のみ)
- claim: 下オクターブの Ga/Pa/Ma あたりに合わせる慣習があるとの記述
- kw: 音程 pitch Ga Pa Ma 下オクターブ lower octave

---

## M: メタ (文献・調査法)

### M-01 教則本は記譜・作品中心、身体運用は薄い
- status: 有力 (ただし M-02 で範囲修正)
- claim: Hindi/Bengali 教則本の関心は記譜法・カーイダー等の作品・系譜。接触時間や圧の定量は書かれない
- kw: 教則本 manual 記譜 notation カーイダー kaida 口伝 oral

### M-02 「口伝は文字化不能」は YouTube 字幕で部分的に崩れる
- status: 有力 (未実装、crawler issue #1)
- claim: तबला कैसे बजाएँ 系動画は数千本、Hindi 自動字幕が付く。奏者が実演しながら話す内容はテキスト化・マイニング可能
- kw: YouTube 字幕 captions yt-dlp 自動字幕 auto-generated

### M-03 定量データは音響学論文にある
- status: 確定
- claim: 身体運用の定量的裏付けは教則本ではなく音響物理の論文 (主に英語、インドの研究機関発) にある
- kw: 音響学 acoustics 論文 paper 定量 quantitative

### M-04 コーパスは有界、悉皆性は被覆率で語る
- status: 有力 (Fermi 推定)
- claim: タブラ関連 Hindi/Bengali テキストは ~10^4 文書オーダー。悉皆性は証明不能だが、独立クエリ 2 系統の重複率から capture-recapture で母集団推定し被覆率 x% と言える
- kw: コーパス corpus capture-recapture 被覆率 coverage recall 10000

### M-05 ソースが割れる細部は動画添削が最速
- status: 有力
- claim: T-09 の割れは文字では詰められない。左手を横からスロー撮影し他人に見せる 1 回が全記事精読を上回る
- kw: 動画添削 video feedback スロー slow motion

---

## R: 棄却済み

### R-01 「手首はキナール上、マイダーンに食い込ませない」
- status: 棄却 (2026-08-07)
- 経緯: 初期に damping 回避のみから導出した仮説。NCERT/Sangtar/TaalGyan/Bengali 教本すべてと矛盾し撤回。T-01/T-02 が置換。楽器のスィヤヒ偏心自体が手首を置く前提の設計だった
- 教訓: 単一の物理原理 (減衰最小化) から奏法を演繹すると、楽器設計に織り込まれた前提を見落とす
- kw: 棄却 rejected キナール 初期仮説 initial hypothesis

### R-02 「口伝領域は調査不能」
- status: 棄却 → M-02/M-04 に置換
- 経緯: 「全記事調査は誰にもできない」という主張は、コーパスが有界であること・字幕という文字化経路を無視していた
- kw: 棄却 rejected 悉皆 exhaustive
