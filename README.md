# tabla-bayan-research

バヤン (tabla 左手) の Ghe が鳴らない問題を、物理・奏法・文献の 3 面から潰すためのリサーチノート。

## 現時点の結論 (2026-08-07)

1. 手首はマイダーンの中に **据える** (浮かせない)。バヤンのスィヤヒが偏心しているのは手首の席を空けるための設計
2. 据えた手首はダンパーではなく **可動境界**。膜を分割し、手首より奥のセグメントが鳴る
3. 打つのは 90 度に立てた指の先端。指を寝かせると Ka (ミュート音) になる
4. 圧ゼロの Ghe は標準奏法に存在しない。「軽い圧のベースライン + 圧の増減でピッチ変調」が正しいモデル
5. 連打が閉じるのは、次打の準備で **指** を面に戻すため。手首は固定、動くのは指だけ
6. 腕の疲労はフォーム誤りのセンサー。正しい Ghe は腕をほぼ使わない
7. ベンドは圧の量ではなく打後のローリング軌道。firm さは重さで作る。押すと段差、転がすとグライド (T-12)

詳細と根拠は docs/ 参照。

## 構成

読む順: FINDINGS.md (主張台帳、正典) → INDEX.md (多言語索引) → docs/ (読み物)。
全文検索: `python tools/notes_search.py <query>` (日/EN/HI/BN 対応、FTS5 trigram + 短語 LIKE)。

| ファイル | 内容 |
|---|---|
| FINDINGS.md | 全知見の主張台帳。ID + status (確定/割れる/推定/棄却) + 多言語 kw |
| INDEX.md | 概念 -> FINDINGS ID / docs の多言語索引。別表記の罠つき |
| tools/notes_search.py | ノート全文検索 CLI |
| crawler/ | Hindi/Bengali コーパス構築パイプライン (SQLite) |
| search/ | コーパス検索エンジン。多言語クエリ展開 + FTS5。`python search/app.py` で http://localhost:8765 |
| docs/01-anatomy.md | 打面の部位名 (日/英/ヒンディー/ベンガル) |
| docs/02-physics.md | 膜振動・減衰モデル・スィヤヒの音響 |
| docs/03-technique-ghe.md | Ghe 奏法の確定事項と流派差 |
| docs/04-troubleshooting.md | 「鳴らない」の診断ツリー |
| docs/05-health.md | 腕・手首の負傷予防 |
| docs/06-sources.md | 注釈付き文献リスト (学術/奏者/Hindi/Bengali) |
| docs/07-open-questions.md | 未解決事項 = issue 候補 |

## 経緯

- 症状: 左の Ghe がまったく伸びない。連打も open にならない
- 転機となった自己観察: 「音程を変えながら叩くと長い尾が出る」→ 楽器・打点・インパルスは正常、差分は打後の左手の質のみ、と確定
- 初期仮説「手首を面に乗せない」は奏者文献 (NCERT, Sangtar, TaalGyan) と矛盾し **棄却**。docs/03 参照
