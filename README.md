# tabla-bayan-research

バヤン (tabla 左手) の Ghe が鳴らない問題を、物理・奏法・文献の 3 面から検証するためのリサーチノート。

## 現時点の結論 (2026-08-07)

1. 手首はマイダーンの中に **据える** (浮かせない)。バヤンのスィヤヒが偏心しているのは手首の席を空けるための設計
2. 据えた手首はダンパーではなく **可動境界**。膜を分割し、手首より奥のセグメントが鳴る
3. 打つのは 90 度に立てた指の先端。指を寝かせると Ka (ミュート音) になる
4. 圧ゼロの Ghe は標準奏法に存在しない。「軽い圧のベースライン + 圧の増減でピッチ変調」が正しいモデル
5. 連打が閉じるのは、次打の準備で **指** を面に戻すため。手首は固定、動くのは指だけ
6. 腕の疲労はフォーム誤りのセンサー。正しい Ghe は腕をほぼ使わない
7. ベンドは圧の量ではなく打後のローリング軌道。firm さは重さで作る。押すと段差、転がすとグライド (T-12)

詳細と根拠は `FINDINGS.md` と `docs/` を参照。

## 構成

読む順: `FINDINGS.md` (主張台帳、正典) → `INDEX.md` (多言語索引) → `docs/` (読み物)。

全文検索:

```bash
python tools/notes_search.py <query>
```

日本語、英語、Hindi、Bengali に対応し、FTS5 trigram と短語 LIKE fallback を使用します。

| ファイル | 内容 |
|---|---|
| `FINDINGS.md` | 全知見の主張台帳。ID + status (確定/割れる/推定/棄却) + 多言語 kw |
| `INDEX.md` | 概念 → FINDINGS ID / docs の多言語索引。別表記の注意点を収録 |
| `tools/notes_search.py` | ノート全文検索 CLI |
| `crawler/` | Hindi/Bengali コーパス構築パイプライン (SQLite) |
| `search/` | 多言語クエリ展開 + FTS5 のコーパス検索エンジン |
| `docs/01-anatomy.md` | 打面の部位名 (日/英/ヒンディー/ベンガル) |
| `docs/02-physics.md` | 膜振動・減衰モデル・スィヤヒの音響 |
| `docs/03-technique-ghe.md` | Ghe 奏法の確定事項と流派差 |
| `docs/04-troubleshooting.md` | 「鳴らない」の診断ツリー |
| `docs/05-health.md` | 腕・手首の負傷予防 |
| `docs/06-sources.md` | 注釈付き文献リスト (学術/奏者/Hindi/Bengali) |
| `docs/07-open-questions.md` | 未解決事項と検証計画 |
| `docs/08-session-summary.md` | Claude との研究セッション記録 |

## 検索エンジン

```bash
python search/app.py
```

`http://localhost:8765` で検索 UI を開けます。コーパスの FTS5 index と多言語 query expansion を組み合わせています。

## 未解決事項

検証課題は [GitHub Issues](https://github.com/hjosugi/tabla-bayan-research/issues) で追跡します。元の一覧と検証案は `docs/07-open-questions.md` にあります。

## 経緯

- 症状: 左の Ghe がまったく伸びず、連打も open にならない
- 転機: 「音程を変えながら叩くと長い尾が出る」という観察から、差分を打後の左手の運動へ絞り込んだ
- 初期仮説「手首を面に乗せない」は奏者文献 (NCERT, Sangtar, TaalGyan) と矛盾するため棄却した
