# crawler: Hindi/Bengali タブラコーパス構築

目標: バヤン奏法に関する Hindi/Bengali/English のテキスト文書を網羅的に収集し、
奏法に関する主張 (claim) を文書横断で集計可能にする。

## コーパス規模の Fermi 推定

| ソース | 概算 |
|---|---|
| Hindi/Bengali Wikipedia + 関連 | ~200 |
| 教育機関 PDF (NCERT/NIOS/大学シラバス) | ~500 |
| 教則ブログ・解説サイト | 2,000-5,000 |
| フォーラム / Quora Hindi / コメント | 2,000-5,000 |
| 書籍スキャン (44books, granthagara, archive.org) | ~500 (OCR 品質低) |
| YouTube 自動字幕 (तबला कैसे बजाएँ 系) | 2,000-10,000 本 |

テキスト換算 ~10^4 文書 × 平均 3k tokens = ~3×10^7 tokens。
全文 LLM 処理は不要。キーワードスコアで絞った上位のみ LLM に通す。

## パイプライン

```
discover -> frontier -> fetch -> extract -> dedup -> score(kw) -> score(llm) -> claims -> report
```

1. **discover**: queries.txt のクエリを検索 API に投げ、ヒット URL を frontier へ。
   seeds.txt のドメインは sitemap/リンクを直接展開
2. **fetch**: robots.txt 遵守、ドメインごと 1 req/s。HTML は zlib 圧縮して pages に保存 (再抽出可能に)
3. **extract**: trafilatura で本文抽出、langdetect で言語判定
4. **dedup**: URL 正規化 + content simhash (ハミング距離 <= 3 で同一視)
5. **score (kw)**: 部位語 (बायाँ/डग्गा/कलाई/घे...) × 奏法語の共起スコア。docs/01 の対照表が語彙源
6. **score (llm)**: kw 上位 ~2,000 件のみ。関連度 + 要約 + claim 抽出を 1 プロンプトで
7. **claims**: topic (wrist_position / finger_angle / pressure / strike_point...) × stance に正規化。
   文書横断で「手首位置: maidan 支持 N 件 / kinar 支持 M 件」の集計を出す
8. **report**: 集計を markdown で docs/ に自動生成、git commit

## recall の測定 (悉皆性の代替)

- クエリを独立な 2 系統 (部位語系 / 動作語系) に分けて走らせ、
  ヒット集合の重複率から capture-recapture で母集団サイズを推定
- 推定母集団に対する被覆率を report に出す。「全部読んだ」ではなく「被覆率 x% (推定)」と言う

## 正直なボトルネック

- **discovery が本体**: リンクグラフだけでは孤立ブログに到達しない。検索 API (Google CSE 100 req/day 無料枠,
  それ以上は有料) が必須。API なしなら seeds からの BFS + Wikipedia 外部リンク + sitemap で妥協
- **最重要コンテンツは動画**: yt-dlp で自動字幕 (hi) を取る別レーンが必要。字幕は句読点なしの連続テキストで
  claim 抽出の難度が高い
- **FTS5 と Devanagari**: unicode61 tokenizer は分かち書きなしの Indic に弱い。trigram tokenizer を併用
- **OCR**: granthagara 系スキャンは tesseract (hin/ben) でも品質が出ない。優先度最下位
- **礼儀**: robots.txt、レート制限、User-Agent 明示。ペイウォール突破はしない

## 使い方

```bash
pip install -r requirements.txt
python pipeline.py init          # DB 作成
python pipeline.py seed          # seeds.txt / queries.txt を frontier へ
python pipeline.py fetch -n 100  # 100 件取得
python pipeline.py extract       # 本文抽出 + 言語判定 + simhash
python pipeline.py score         # キーワードスコア
python pipeline.py stats         # 進捗と言語分布
```
