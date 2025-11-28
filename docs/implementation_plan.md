# Google検索リサーチツール - 実装計画書

バージョン: 1.0
作成日: 2025年11月28日
最終更新: 2025年11月28日

---

## 1. 実装方針

### 1.1 開発アプローチ
**アジャイル・反復型開発**
- Phase単位で機能を段階的に実装
- 各Phaseで動作確認とテストを実施
- 早期に最小限の動作版（MVP）を完成させる

### 1.2 優先順位の考え方
1. **Phase 1（MVP）**: コア機能の実装（検索、基本抽出、Excel出力）
2. **Phase 2**: 詳細情報抽出機能の拡充
3. **Phase 3**: GUI実装とユーザビリティ向上
4. **Phase 4**: テスト・バグ修正・ドキュメント整備

### 1.3 技術選定理由

| 技術 | 選定理由 |
|------|---------|
| Python 3.10+ | 豊富なスクレイピングライブラリ、学習コストが低い |
| Selenium | JavaScript実行環境が必要なページに対応 |
| BeautifulSoup4 | HTMLパースが高速かつ柔軟 |
| openpyxl | Excel操作が簡単、xlsx形式対応 |
| pandas | データ整形・重複除去が容易 |
| CustomTkinter | モダンなUIを簡単に実装可能 |

---

## 2. システムアーキテクチャ

### 2.1 全体構成図

```
┌─────────────────────────────────────────────────┐
│                 GUI Layer                        │
│  (CustomTkinter - ユーザーインターフェース)        │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│              Application Layer                   │
│  (メインロジック、検索制御、データフロー管理)        │
└─────────────────┬───────────────────────────────┘
                  │
        ┌─────────┴─────────┐
        │                   │
┌───────▼────────┐   ┌──────▼──────────┐
│  Core Layer    │   │  Output Layer   │
│  - Searcher    │   │  - ExcelWriter  │
│  - Scraper     │   │  - DataFormatter│
│  - Extractor   │   └─────────────────┘
└────────────────┘
        │
┌───────▼────────┐
│  Utils Layer   │
│  - Config      │
│  - Logger      │
│  - Validator   │
└────────────────┘
```

### 2.2 ディレクトリ構造

```
google_research/
├── main.py                          # アプリケーションエントリーポイント
├── requirements.txt                 # 依存パッケージ
├── README.md                        # プロジェクト概要
├── .gitignore                       # Git除外設定
│
├── config/                          # 設定ファイル
│   ├── __init__.py
│   ├── settings.py                  # アプリケーション設定
│   ├── constants.py                 # 定数定義
│   └── presets/                     # 検索プリセット保存先
│       └── default.json
│
├── core/                            # コア機能モジュール
│   ├── __init__.py
│   ├── searcher.py                  # Google検索実行
│   ├── scraper.py                   # Webページスクレイピング
│   ├── extractor.py                 # 情報抽出ロジック
│   └── browser.py                   # ブラウザ制御（Selenium）
│
├── gui/                             # GUIモジュール
│   ├── __init__.py
│   ├── main_window.py              # メインウィンドウ
│   ├── search_panel.py             # 検索設定パネル
│   ├── result_panel.py             # 結果表示パネル
│   ├── settings_dialog.py          # 設定ダイアログ
│   └── components/                 # 再利用可能なUIコンポーネント
│       ├── __init__.py
│       └── progress_bar.py
│
├── output/                          # 出力機能モジュール
│   ├── __init__.py
│   ├── excel_writer.py             # Excel出力
│   └── formatter.py                # データフォーマット
│
├── utils/                           # ユーティリティ
│   ├── __init__.py
│   ├── logger.py                   # ログ出力
│   ├── validators.py               # バリデーション
│   ├── file_utils.py               # ファイル操作
│   └── text_utils.py               # テキスト処理
│
├── tests/                           # テストコード
│   ├── __init__.py
│   ├── test_searcher.py
│   ├── test_scraper.py
│   ├── test_extractor.py
│   ├── test_excel_writer.py
│   └── fixtures/                   # テスト用データ
│       └── sample_search_results.html
│
├── docs/                            # ドキュメント
│   ├── requirements_memo.txt       # 元の要件メモ
│   ├── requirements_specification.md # 要件定義書
│   ├── implementation_plan.md      # 本ドキュメント
│   ├── api_design.md               # API設計書
│   └── user_manual.md              # ユーザーマニュアル
│
├── logs/                            # ログファイル出力先
│   └── .gitkeep
│
└── output/                          # Excel出力先（デフォルト）
    └── .gitkeep
```

---

## 3. モジュール詳細設計

### 3.1 Core Layer

#### 3.1.1 searcher.py - Google検索実行

**責務:**
- Google検索の実行
- 検索結果ページの取得
- 検索オプションの適用

**主要クラス:**

```python
class GoogleSearcher:
    """Google検索を実行するクラス"""

    def __init__(self, config: dict):
        """初期化"""

    def search(self, keyword: str, options: SearchOptions) -> SearchResult:
        """検索を実行"""

    def build_search_url(self, keyword: str, options: SearchOptions) -> str:
        """検索URLを構築"""

    def parse_search_results(self, html: str) -> list[SearchItem]:
        """検索結果HTMLをパース"""
```

**主要メソッド:**
- `search()`: 検索実行のエントリーポイント
- `build_search_url()`: 検索クエリの構築
- `parse_search_results()`: 検索結果のパース
- `_handle_captcha()`: CAPTCHA検出処理
- `_wait_for_rate_limit()`: レート制限対応

#### 3.1.2 scraper.py - Webページスクレイピング

**責務:**
- 個別Webページへのアクセス
- HTMLの取得
- エラーハンドリング

**主要クラス:**

```python
class WebScraper:
    """Webページをスクレイピングするクラス"""

    def __init__(self, config: dict):
        """初期化"""

    def fetch_page(self, url: str) -> PageContent:
        """ページコンテンツを取得"""

    def check_robots_txt(self, url: str) -> bool:
        """robots.txtをチェック"""

    def extract_html(self, url: str) -> str:
        """HTMLを取得"""
```

**主要メソッド:**
- `fetch_page()`: ページ取得のエントリーポイント
- `check_robots_txt()`: robots.txt遵守チェック
- `extract_html()`: HTML取得
- `_retry_on_error()`: エラー時のリトライ処理
- `_set_user_agent()`: User-Agent設定

#### 3.1.3 extractor.py - 情報抽出

**責務:**
- HTMLから必要情報の抽出
- 正規表現による情報抽出
- データのバリデーション

**主要クラス:**

```python
class InfoExtractor:
    """Webページから情報を抽出するクラス"""

    def __init__(self):
        """初期化"""

    def extract_phone(self, html: str) -> list[str]:
        """電話番号を抽出"""

    def extract_email(self, html: str) -> list[str]:
        """メールアドレスを抽出"""

    def extract_address(self, html: str) -> dict:
        """住所を抽出"""

    def extract_company_name(self, html: str) -> str:
        """会社名・店舗名を抽出"""
```

**正規表現パターン:**
- 電話番号: `0\d{1,4}-\d{1,4}-\d{4}`, `0\d{9,10}`
- メールアドレス: `[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}`
- 郵便番号: `〒?\d{3}-?\d{4}`

#### 3.1.4 browser.py - ブラウザ制御

**責務:**
- Selenium WebDriverの管理
- ブラウザの起動・終了
- JavaScript実行環境の提供

**主要クラス:**

```python
class BrowserController:
    """Seleniumブラウザを制御するクラス"""

    def __init__(self, headless: bool = True):
        """初期化"""

    def start_browser(self):
        """ブラウザを起動"""

    def stop_browser(self):
        """ブラウザを終了"""

    def get_page(self, url: str) -> str:
        """ページを取得（JavaScriptレンダリング含む）"""
```

### 3.2 Output Layer

#### 3.2.1 excel_writer.py - Excel出力

**責務:**
- データのExcel形式出力
- フォーマット適用
- ファイル保存

**主要クラス:**

```python
class ExcelWriter:
    """Excel形式でデータを出力するクラス"""

    def __init__(self, config: dict):
        """初期化"""

    def write(self, data: list[dict], filepath: str, columns: list[str]):
        """データをExcelに書き込み"""

    def format_cells(self, worksheet):
        """セルのフォーマット適用"""

    def auto_adjust_column_width(self, worksheet):
        """列幅を自動調整"""
```

#### 3.2.2 formatter.py - データフォーマット

**責務:**
- データの整形
- 重複除去
- バリデーション

**主要クラス:**

```python
class DataFormatter:
    """データを整形するクラス"""

    def remove_duplicates(self, data: list[dict]) -> list[dict]:
        """重複データを除去"""

    def validate_data(self, data: list[dict]) -> list[dict]:
        """データをバリデーション"""

    def sort_data(self, data: list[dict], key: str) -> list[dict]:
        """データをソート"""
```

### 3.3 GUI Layer

#### 3.3.1 main_window.py - メインウィンドウ

**責務:**
- アプリケーションのメインUI
- 各パネルの統合
- イベント制御

**主要クラス:**

```python
class MainWindow(ctk.CTk):
    """メインウィンドウクラス"""

    def __init__(self):
        """初期化"""

    def setup_ui(self):
        """UI要素を配置"""

    def on_search_start(self):
        """検索開始イベント"""

    def on_search_stop(self):
        """検索停止イベント"""

    def update_progress(self, current: int, total: int):
        """進捗を更新"""
```

#### 3.3.2 search_panel.py - 検索設定パネル

**責務:**
- 検索パラメータの入力UI
- バリデーション
- プリセット管理

#### 3.3.3 result_panel.py - 結果表示パネル

**責務:**
- 検索結果のテーブル表示
- リアルタイム更新
- データのプレビュー

### 3.4 Utils Layer

#### 3.4.1 logger.py - ログ出力

**責務:**
- ログの記録
- ログレベル管理
- ファイル出力

**主要クラス:**

```python
class AppLogger:
    """アプリケーションログを管理するクラス"""

    def __init__(self, name: str):
        """初期化"""

    def info(self, message: str):
        """情報ログ"""

    def error(self, message: str, exception: Exception = None):
        """エラーログ"""

    def debug(self, message: str):
        """デバッグログ"""
```

#### 3.4.2 validators.py - バリデーション

**責務:**
- 入力値の検証
- URL形式チェック
- データ整合性確認

---

## 4. データモデル設計

### 4.1 主要データクラス

#### SearchOptions - 検索オプション
```python
@dataclass
class SearchOptions:
    """検索オプション"""
    num_results: int = 10          # 検索結果件数
    region: str = "jp"             # 地域指定
    language: str = "ja"           # 言語指定
    period: str = None             # 期間指定
    site: str = None               # サイト内検索
    exclude_keywords: list[str] = None  # 除外キーワード
```

#### SearchItem - 検索結果アイテム
```python
@dataclass
class SearchItem:
    """検索結果の1件"""
    rank: int                      # 検索順位
    title: str                     # タイトル
    url: str                       # URL
    description: str               # 説明文
    snippet: str                   # スニペット
```

#### DetailedInfo - 詳細情報
```python
@dataclass
class DetailedInfo:
    """詳細情報"""
    phone: list[str] = None        # 電話番号
    email: list[str] = None        # メールアドレス
    address: dict = None           # 住所情報
    fax: str = None                # FAX番号
    company_name: str = None       # 会社名・店舗名
    sns_links: dict = None         # SNSリンク
```

#### OutputData - 出力データ
```python
@dataclass
class OutputData:
    """出力用データ"""
    search_item: SearchItem        # 検索結果
    detailed_info: DetailedInfo    # 詳細情報

    def to_dict(self) -> dict:
        """辞書形式に変換"""
```

---

## 5. Phase別実装計画

### Phase 1: MVP（最小機能版） - 1週間

**目標:** 基本的な検索・抽出・Excel出力が動作する状態

#### Week 1 - Day 1-2: 環境構築とコア機能の骨格
- [ ] プロジェクト構造の作成
- [ ] 依存パッケージのインストール
- [ ] `searcher.py`の基本実装
  - Google検索URL構築
  - 検索結果HTMLの取得
  - 基本的なパース処理
- [ ] `browser.py`のSelenium基本実装

**成果物:**
- 動作するプロジェクト構造
- 検索結果（タイトル、URL、説明文）が取得できる

#### Week 1 - Day 3-4: スクレイピング機能
- [ ] `scraper.py`の実装
  - ページコンテンツ取得
  - robots.txtチェック
  - エラーハンドリング
- [ ] `extractor.py`の基本実装
  - 電話番号抽出（正規表現）
  - メールアドレス抽出
  - 住所抽出（基本パターン）

**成果物:**
- 個別ページから情報を抽出できる

#### Week 1 - Day 5-6: Excel出力機能
- [ ] `excel_writer.py`の実装
  - openpyxlによる基本出力
  - ヘッダー行生成
  - 列幅自動調整
- [ ] `formatter.py`の実装
  - 重複除去
  - データバリデーション

**成果物:**
- Excel形式でデータ出力が可能

#### Week 1 - Day 7: 統合とCLI版
- [ ] `main.py`の実装（CLI版）
- [ ] エンドツーエンドの動作確認
- [ ] 基本的なエラーハンドリング
- [ ] ログ出力機能

**成果物:**
- コマンドラインから検索→抽出→Excel出力が実行できる
- MVP完成

**Phase 1 完了基準:**
- [ ] キーワード検索が実行できる
- [ ] 検索結果（タイトル、URL、説明文）が取得できる
- [ ] 電話番号・メールアドレスが抽出できる
- [ ] Excel形式で出力できる
- [ ] 基本的なエラーハンドリングが動作する

---

### Phase 2: 詳細情報抽出機能の拡充 - 1週間

**目標:** 抽出精度の向上と抽出項目の追加

#### Week 2 - Day 1-2: 抽出ロジックの改善
- [ ] 電話番号抽出の精度向上
  - 複数パターン対応
  - フリーダイヤル対応
  - 海外番号対応
- [ ] 住所抽出の精度向上
  - 都道府県・市区町村の正確な抽出
  - 郵便番号との紐付け
- [ ] 会社名・店舗名抽出の実装
  - meta タグからの抽出
  - hタグからの抽出
  - JSON-LDからの抽出

**成果物:**
- 抽出精度90%以上達成

#### Week 2 - Day 3-4: 追加抽出項目の実装
- [ ] FAX番号抽出
- [ ] SNSリンク抽出
  - Twitter/X
  - Instagram
  - Facebook
  - LINE
- [ ] 営業時間・定休日抽出（基本パターン）

**成果物:**
- 要件定義の詳細情報項目をすべて実装

#### Week 2 - Day 5-6: 検索オプションの拡充
- [ ] 地域指定検索
- [ ] サイト内検索（site:）
- [ ] 期間指定検索
- [ ] 除外キーワード検索

**成果物:**
- 高度な検索オプションが利用可能

#### Week 2 - Day 7: テストとバグ修正
- [ ] 単体テストの作成
- [ ] 抽出精度の検証
- [ ] エッジケースの対応

**Phase 2 完了基準:**
- [ ] 詳細情報項目がすべて抽出可能
- [ ] 抽出精度90%以上
- [ ] 高度な検索オプションが動作
- [ ] 単体テストカバレッジ50%以上

---

### Phase 3: GUI実装とユーザビリティ向上 - 1週間

**目標:** 使いやすいデスクトップアプリケーションの完成

#### Week 3 - Day 1-2: 基本GUI実装
- [ ] `main_window.py`の実装
  - ウィンドウ基本構造
  - メニューバー
  - ステータスバー
- [ ] `search_panel.py`の実装
  - キーワード入力欄
  - 検索オプション選択UI
  - 抽出項目チェックボックス

**成果物:**
- 検索設定を入力できるGUI

#### Week 3 - Day 3-4: 結果表示と進捗管理
- [ ] `result_panel.py`の実装
  - テーブル形式での結果表示
  - リアルタイム更新
- [ ] プログレスバーの実装
- [ ] 処理状況ログ表示
- [ ] 実行制御（開始・停止・一時停止）

**成果物:**
- 検索結果がリアルタイムで表示される

#### Week 3 - Day 5-6: 設定管理機能
- [ ] `settings_dialog.py`の実装
  - 待機時間設定
  - 出力先フォルダ設定
  - デフォルト値設定
- [ ] プリセット機能の実装
  - 検索設定の保存
  - 保存済み設定の読み込み
  - プリセット管理UI

**成果物:**
- 設定管理が可能

#### Week 3 - Day 7: UI/UX改善
- [ ] デザインの調整
- [ ] エラーメッセージの改善
- [ ] ツールチップの追加
- [ ] ショートカットキーの実装

**Phase 3 完了基準:**
- [ ] GUIから全機能が利用可能
- [ ] 初回利用者が30分以内に操作習得可能
- [ ] プリセット保存・読込が動作
- [ ] エラーメッセージがわかりやすい

---

### Phase 4: テスト・バグ修正・ドキュメント整備 - 1週間

**目標:** 品質向上とリリース準備

#### Week 4 - Day 1-2: テストの拡充
- [ ] 統合テストの作成
- [ ] E2Eテストの作成
- [ ] パフォーマンステスト
- [ ] クロスプラットフォームテスト
  - Windows 10/11
  - macOS

**成果物:**
- テストカバレッジ70%以上

#### Week 4 - Day 3-4: バグ修正と最適化
- [ ] テストで発見したバグの修正
- [ ] パフォーマンス最適化
- [ ] メモリリーク対策
- [ ] エラーハンドリングの強化

**成果物:**
- 安定動作版

#### Week 4 - Day 5-6: ドキュメント整備
- [ ] README.mdの作成
  - インストール手順
  - 基本的な使い方
  - トラブルシューティング
- [ ] ユーザーマニュアルの作成
  - 各機能の詳細説明
  - 画面キャプチャ付き
- [ ] API設計書の更新
- [ ] コメント・docstringの追加

**成果物:**
- 完全なドキュメント

#### Week 4 - Day 7: リリース準備
- [ ] requirements.txtの整備
- [ ] .gitignoreの確認
- [ ] ライセンスファイルの追加
- [ ] 初回リリース版のタグ付け

**Phase 4 完了基準:**
- [ ] 全テスト合格
- [ ] ドキュメント完備
- [ ] リリース可能な状態

---

## 6. テスト計画

### 6.1 テストレベル

#### 単体テスト（Unit Test）
**対象:** 各モジュールの個別関数・メソッド
**ツール:** pytest
**カバレッジ目標:** 70%以上

**主要テストケース:**
- `test_searcher.py`: 検索URL構築、パース処理
- `test_scraper.py`: ページ取得、robots.txtチェック
- `test_extractor.py`: 各抽出パターン（電話番号、メール等）
- `test_excel_writer.py`: Excel出力、フォーマット

#### 統合テスト（Integration Test）
**対象:** モジュール間の連携
**ツール:** pytest

**主要テストケース:**
- 検索→スクレイピング→抽出の一連の流れ
- 抽出→フォーマット→Excel出力の流れ
- GUI操作からバックエンド処理までの連携

#### E2Eテスト（End-to-End Test）
**対象:** アプリケーション全体
**手法:** 手動テスト + 自動化（可能な範囲）

**主要シナリオ:**
1. 基本検索から出力まで
2. 高度な検索オプション使用
3. プリセット保存・読込
4. エラー発生時の挙動
5. 大量データ処理（100件）

### 6.2 テストデータ

**検索キーワード例:**
- 「東京 歯科医院」
- 「大阪 美容室」
- 「名古屋 税理士」
- 「福岡 カフェ」

**期待される抽出パターン:**
- 電話番号: 03-1234-5678, 0120-123-456
- メール: info@example.com
- 住所: 東京都渋谷区〇〇1-2-3

### 6.3 パフォーマンステスト

**測定項目:**
- 検索結果10件取得時間
- 検索結果100件取得時間
- 詳細情報抽出時間（1ページあたり）
- Excel出力時間（100件）
- メモリ使用量

**目標値:**
- 100件検索: 3分以内
- 1ページ詳細抽出: 3-5秒
- Excel出力: 10秒以内
- メモリ: 500MB以下

---

## 7. リスク管理

### 7.1 技術的リスクと対策

| リスク | 影響 | 対策 | 担当 |
|--------|------|------|------|
| Google HTML構造変更 | 高 | 定期的な動作確認、柔軟なパーサー実装 | 開発者 |
| CAPTCHA頻発 | 中 | 適切な待機時間、検出時の処理停止 | 開発者 |
| 抽出精度が目標未達 | 中 | 正規表現の改善、テストケース追加 | 開発者 |
| クロスプラットフォーム問題 | 中 | 各OS環境でのテスト実施 | 開発者 |
| パフォーマンス目標未達 | 低 | プロファイリング、最適化 | 開発者 |

### 7.2 スケジュールリスクと対策

| リスク | 影響 | 対策 |
|--------|------|------|
| Phase 1遅延 | 高 | スコープの見直し、優先順位の再設定 |
| 想定外のバグ発生 | 中 | バッファ期間の確保、早期のテスト実施 |
| 外部ライブラリの不具合 | 低 | 代替ライブラリの調査 |

---

## 8. 開発環境セットアップ手順

### 8.1 必要なソフトウェア

1. **Python 3.10以上**
   - ダウンロード: https://www.python.org/downloads/

2. **Google Chrome / Chromium**
   - Selenium WebDriver用

3. **ChromeDriver**
   - 自動ダウンロードまたは手動インストール

4. **Git**
   - バージョン管理用

### 8.2 セットアップ手順

```bash
# 1. リポジトリのクローン（または作成）
git clone <repository-url>
cd google_research

# 2. 仮想環境の作成
python -m venv venv

# 3. 仮想環境の有効化
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 4. 依存パッケージのインストール
pip install -r requirements.txt

# 5. 動作確認
python main.py --help
```

### 8.3 requirements.txt（Phase 1版）

```
selenium==4.16.0
beautifulsoup4==4.12.2
requests==2.31.0
openpyxl==3.1.2
pandas==2.1.4
customtkinter==5.2.1
webdriver-manager==4.0.1
```

---

## 9. コーディング規約

### 9.1 スタイルガイド
- **PEP 8準拠**
- **最大行長:** 100文字
- **インデント:** スペース4つ
- **命名規則:**
  - クラス: PascalCase (`GoogleSearcher`)
  - 関数・変数: snake_case (`search_keyword`)
  - 定数: UPPER_SNAKE_CASE (`MAX_RETRIES`)
  - プライベート: 先頭にアンダースコア (`_internal_method`)

### 9.2 型ヒント
- Python 3.10+の型ヒントを積極的に使用
- 関数の引数と戻り値には型を明示

```python
def search(keyword: str, num_results: int = 10) -> list[SearchItem]:
    """検索を実行"""
    pass
```

### 9.3 docstring
- Google形式のdocstringを使用

```python
def extract_phone(html: str) -> list[str]:
    """HTMLから電話番号を抽出する

    Args:
        html: 解析対象のHTML文字列

    Returns:
        抽出された電話番号のリスト

    Raises:
        ValueError: HTMLが不正な場合
    """
    pass
```

### 9.4 コメント
- 複雑なロジックには日本語でコメントを記載
- TODOコメントは `# TODO:` 形式で記載

---

## 10. デプロイ・配布方法（Phase 4以降）

### 10.1 配布形式

#### オプション1: Pythonパッケージ（pip install）
- PyPIへの公開（オプション）
- `setup.py`の作成

#### オプション2: 実行ファイル（推奨）
- **PyInstaller**による実行ファイル化
- Windows: .exe
- macOS: .app
- 利点: Pythonインストール不要

### 10.2 PyInstallerによるビルド

```bash
# インストール
pip install pyinstaller

# ビルド（ワンファイル版）
pyinstaller --onefile --windowed --name GoogleResearchTool main.py

# ビルド（ディレクトリ版、推奨）
pyinstaller --windowed --name GoogleResearchTool main.py
```

---

## 11. 今後の拡張計画（Phase 5以降）

### 11.1 短期的な拡張（3-6ヶ月）
1. **Google Custom Search API対応**
   - より安定した検索結果取得
   - API制限内での効率的な運用

2. **CSV/JSON出力対応**
   - 多様な出力形式

3. **バッチ処理機能**
   - 複数キーワードの一括処理
   - スケジュール実行

### 11.2 中長期的な拡張（6-12ヶ月）
1. **Googleマップ連携**
   - ビジネス情報の取得
   - レビュー情報の収集

2. **AI活用**
   - 自然言語処理による精度向上
   - 自動カテゴリ分類

3. **クラウド版開発**
   - Web版アプリケーション
   - 複数ユーザー対応

4. **Amazon・楽天版開発**
   - 共通モジュール化
   - マルチプラットフォーム対応

---

## 12. 承認・レビュー

### 12.1 レビュー項目
- [ ] アーキテクチャ設計は適切か
- [ ] Phase分けは妥当か
- [ ] スケジュールは実現可能か
- [ ] リスク対策は十分か
- [ ] テスト計画は網羅的か

### 12.2 承認

| 役割 | 氏名 | 承認日 | 署名 |
|------|------|--------|------|
| プロジェクトオーナー | - | - | - |
| 技術リーダー | - | - | - |

---

## 変更履歴

| バージョン | 日付 | 変更内容 | 変更者 |
|-----------|------|---------|--------|
| 1.0 | 2025-11-28 | 初版作成 | - |
