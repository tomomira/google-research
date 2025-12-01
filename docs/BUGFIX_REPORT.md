# バグ修正報告書

**報告日**: 2025年12月1日
**対象期間**: Phase 4完了後（2025年12月1日）

---

## 概要

Phase 4完了後、ユーザーテストにおいてGUI版で3つのバグが発見されました。すべて同日中に修正し、動作確認を完了しました。

---

## バグ修正一覧

### バグ #1: GUI版の検索API呼び出しパラメータ不一致

**発見日**: 2025年12月1日
**重要度**: 🔴 高（GUI版が動作不能）
**コミットID**: 52cdb51

#### 問題
GUI版で検索を実行すると、以下のエラーが発生：
```
TypeError: SearchAPIClient.search() got an unexpected keyword argument 'query'
```

#### 原因
`gui/main_window.py:233` で `SearchAPIClient.search()` を呼び出す際に、誤ったパラメータ名を使用していました。

**誤ったコード**:
```python
search_items = self.search_client.search(
    query=config.keyword,        # ← 誤り: 'query'
    num_results=config.num_results  # ← 誤り: 'num_results'
)
```

**正しいAPI**:
```python
def search(self, keyword: str, options: Optional[SearchOptions] = None)
```

#### 修正内容
1. `from core.searcher import SearchOptions` をインポート
2. `SearchOptions` オブジェクトを作成してパラメータを渡す

**修正後のコード**:
```python
search_options = SearchOptions(num_results=config.num_results)
search_items = self.search_client.search(
    keyword=config.keyword,
    options=search_options
)
```

#### 副次的な修正
同じコミットで、lambda式での変数キャプチャの問題も修正：

**修正前**:
```python
except Exception as e:
    # ...
    self.after(0, lambda: self.update_status(f"エラー: {str(e)}"))
    # ↑ NameError: cannot access free variable 'e' が発生
```

**修正後**:
```python
except Exception as e:
    error_msg = str(e)
    self.after(0, lambda msg=error_msg: self.update_status(f"エラー: {msg}"))
    # ↑ デフォルト引数でキャプチャ
```

#### 影響範囲
- GUI版の検索機能が完全に動作不能
- CLI版は影響なし

---

### バグ #2: WebScraperメソッド名の不一致

**発見日**: 2025年12月1日
**重要度**: 🔴 高（詳細情報取得が動作不能）
**コミットID**: e99c724

#### 問題
「詳細情報を取得する」チェックボックスを有効にすると、以下のエラーが発生：
```
AttributeError: 'WebScraper' object has no attribute 'fetch'
```

#### 原因
`gui/main_window.py:256` で存在しないメソッド `fetch()` を呼び出していました。

**誤ったコード**:
```python
html = self.scraper.fetch(item.url)  # ← 誤り: fetch()は存在しない
if html:
    detailed_info = self.extractor.extract_all(html)
```

**正しいメソッド**:
```python
def fetch_page(self, url: str, respect_robots: bool = True) -> Optional[PageContent]
```

#### 修正内容
1. メソッド名を `fetch()` → `fetch_page()` に修正
2. 戻り値の型が `PageContent` オブジェクトなので、`.html` 属性にアクセス

**修正後のコード**:
```python
page_content = self.scraper.fetch_page(item.url)
if page_content and page_content.html:
    detailed_info = self.extractor.extract_all(page_content.html)
    detailed_infos.append(detailed_info)
else:
    detailed_infos.append(None)
```

#### 影響範囲
- GUI版の詳細情報取得機能が完全に動作不能
- CLI版は影響なし（正しいメソッド名を使用していた）

---

### バグ #3: 個別サイトエラー時の処理停止

**発見日**: 2025年12月1日
**重要度**: 🟡 中（一部サイトで処理が完全停止）
**コミットID**: c7a5953

#### 問題
詳細情報取得中に1つのサイトで robots.txt によりアクセスが拒否されると、以下のエラーで処理全体が停止：
```
検索エラー: robots.txtによりアクセスが拒否されました。
```

#### 原因
`gui/main_window.py` の詳細情報取得ループ（line 252-262）で、個別サイトのエラーがキャッチされず、外側の `except Exception as e:` (line 278) まで伝播していました。

**問題のあるコード**:
```python
for i, item in enumerate(search_items, 1):
    # HTMLを取得
    page_content = self.scraper.fetch_page(item.url)  # ← RuntimeError発生
    # ↑ エラーがキャッチされず、外側のexceptまで伝播
```

#### 修正内容
ループ内に個別のエラーハンドリングを追加：

**修正後のコード**:
```python
for i, item in enumerate(search_items, 1):
    try:
        # HTMLを取得
        page_content = self.scraper.fetch_page(item.url)
        if page_content and page_content.html:
            detailed_info = self.extractor.extract_all(page_content.html)
            detailed_infos.append(detailed_info)
        else:
            detailed_infos.append(None)
    except Exception as e:
        # 個別のスクレイピングエラーはログに記録して続行
        logger.warning(f"Failed to fetch details from {item.url}: {e}")
        self.after(0, lambda url=item.url: self.result_panel.show_progress(f"  ⚠ スキップ: {url}"))
        detailed_infos.append(None)
```

#### CLI版の修正
CLI版でもユーザーフィードバックを改善：

**修正内容**:
```python
except Exception as e:
    logger.warning(f"Failed to fetch details from {item.url}: {e}")
    print(f"  ⚠ スキップ: {item.url} (理由: {str(e)[:50]})")
    detailed_infos.append(None)
```

#### 動作
- 個別サイトでエラーが発生しても、処理は続行
- 失敗したサイトには「⚠ スキップ」と表示
- 取得できたサイトの情報は正常に処理・表示
- 詳細情報が取得できなかったサイトは、基本情報（タイトル、URL、説明）のみ出力

#### 影響範囲
- GUI版: 処理全体が停止していた
- CLI版: 既に個別エラーハンドリングがあったが、メッセージを改善

---

## 動作確認

### テストケース

**検索キーワード**: 「千葉市 スポーツクラブ」
**取得件数**: 10件
**詳細情報取得**: 有効

### 確認結果

#### GUI版
- ✅ 検索が正常に実行される
- ✅ 詳細情報取得が正常に動作
- ✅ robots.txt拒否サイトはスキップして処理続行
- ✅ Excelファイルが正常に出力される

#### CLI版
- ✅ 検索が正常に実行される
- ✅ 詳細情報取得が正常に動作
- ✅ robots.txt拒否サイトはスキップメッセージを表示して処理続行
- ✅ Excelファイルが正常に出力される

---

## 修正後のコミット履歴

```
c7a5953 Improve error handling for individual site scraping failures
e99c724 Fix WebScraper method call in GUI
52cdb51 fix: GUI版の検索API呼び出しを修正
```

---

## 学んだ教訓

### 1. GUI版の実装時にAPI仕様を再確認する
- Phase 1-2でCLI版を実装し、Phase 3でGUI版を実装した際に、API仕様の確認が不十分だった
- 特に `SearchAPIClient.search()` のパラメータ名が変更されていることに気づかなかった

### 2. メソッド名の一貫性を保つ
- `WebScraper.fetch_page()` というメソッド名が長いため、`fetch()` と誤記しやすい
- コード補完を活用する、もしくはメソッド名を短縮する検討が必要

### 3. エラーハンドリングの粒度を適切に設計する
- 複数のアイテムを処理するループでは、個別アイテムのエラーと全体のエラーを区別する
- 個別アイテムのエラーで全体を停止すべきではない

### 4. ユーザーフィードバックの重要性
- 実際のユーザーテストで初めて発見されるバグがある
- 早期のユーザーテストが重要

---

## 再発防止策

### 1. 統合テストの追加
現在のテストは単体テストが中心。以下を追加検討：
- GUI版のE2Eテスト
- エラーケースの統合テスト（robots.txt拒否など）

### 2. コードレビュー
- GUI版実装時に、CLI版との整合性をチェック
- API呼び出し部分は特に注意深くレビュー

### 3. ドキュメント整備
- API仕様書の作成（引数名、戻り値の型など）
- 実装ガイドラインの作成

---

**報告者**: Claude Code
**最終更新**: 2025年12月1日
