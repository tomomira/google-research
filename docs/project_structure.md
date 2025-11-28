# プロジェクト構造ドキュメント

作成日: 2025年11月28日

## ディレクトリツリー

```
google_research/
├── main.py                          # アプリケーションエントリーポイント
├── requirements.txt                 # 依存パッケージ定義
├── README.md                        # プロジェクト概要・使い方
├── .gitignore                       # Git除外設定
│
├── config/                          # 設定ファイル
│   ├── __init__.py
│   ├── settings.py                  # アプリケーション設定（パス、デフォルト値等）
│   ├── constants.py                 # 定数定義（正規表現、メッセージ等）
│   └── presets/                     # 検索プリセット保存先
│       └── default.json             # デフォルト設定
│
├── core/                            # コア機能モジュール（Phase 1で実装予定）
│   ├── __init__.py
│   ├── searcher.py                  # Google検索実行（未実装）
│   ├── scraper.py                   # Webページスクレイピング（未実装）
│   ├── extractor.py                 # 情報抽出ロジック（未実装）
│   └── browser.py                   # ブラウザ制御（Selenium）（未実装）
│
├── gui/                             # GUIモジュール（Phase 3で実装予定）
│   ├── __init__.py
│   ├── main_window.py              # メインウィンドウ（未実装）
│   ├── search_panel.py             # 検索設定パネル（未実装）
│   ├── result_panel.py             # 結果表示パネル（未実装）
│   ├── settings_dialog.py          # 設定ダイアログ（未実装）
│   └── components/                 # 再利用可能なUIコンポーネント
│       ├── __init__.py
│       └── progress_bar.py         # プログレスバー（未実装）
│
├── output/                          # 出力機能モジュール（Phase 1で実装予定）
│   ├── __init__.py
│   ├── excel_writer.py             # Excel出力（未実装）
│   └── formatter.py                # データフォーマット（未実装）
│
├── utils/                           # ユーティリティモジュール
│   ├── __init__.py
│   ├── logger.py                   # ログ出力（実装済み）
│   ├── validators.py               # バリデーション（未実装）
│   ├── file_utils.py               # ファイル操作（未実装）
│   └── text_utils.py               # テキスト処理（未実装）
│
├── tests/                           # テストコード
│   ├── __init__.py
│   ├── test_searcher.py            # searcher.pyのテスト（未実装）
│   ├── test_scraper.py             # scraper.pyのテスト（未実装）
│   ├── test_extractor.py           # extractor.pyのテスト（未実装）
│   ├── test_excel_writer.py        # excel_writer.pyのテスト（未実装）
│   └── fixtures/                   # テスト用データ
│       └── sample_search_results.html  # サンプルHTML（未作成）
│
├── docs/                            # ドキュメント
│   ├── requirements_memo.txt       # 元の要件メモ
│   ├── requirements_specification.md # 要件定義書（完成）
│   ├── implementation_plan.md      # 実装計画書（完成）
│   ├── project_structure.md        # 本ドキュメント
│   ├── api_design.md               # API設計書（Phase 1開始前に作成予定）
│   └── user_manual.md              # ユーザーマニュアル（Phase 4で作成予定）
│
├── logs/                            # ログファイル出力先
│   └── .gitkeep
│
└── output/                          # Excel出力先（デフォルト）
    └── .gitkeep
```

## モジュール説明

### 1. config/ - 設定モジュール

#### settings.py
アプリケーション全体の設定を管理。

**主要機能:**
- ディレクトリパスの定義
- デフォルト値の設定
- 検索・スクレイピング・Excel出力の各種パラメータ

**主要クラス:**
- `Settings`: 設定を管理する静的クラス

#### constants.py
アプリケーション全体で使用する定数を定義。

**主要定数:**
- `GOOGLE_SEARCH_URL`: Google検索のURL
- `REGEX_PATTERNS`: 電話番号、メールアドレス等の正規表現
- `ERROR_MESSAGES`: エラーメッセージのテンプレート
- `SNS_DOMAINS`: SNSサービスのドメインリスト

### 2. core/ - コア機能モジュール（Phase 1で実装）

#### searcher.py（未実装）
Google検索を実行し、検索結果を取得。

**主要クラス:**
- `GoogleSearcher`: 検索実行クラス

**主要メソッド:**
- `search()`: 検索実行
- `build_search_url()`: 検索URL構築
- `parse_search_results()`: 検索結果のパース

#### scraper.py（未実装）
個別Webページにアクセスし、HTMLを取得。

**主要クラス:**
- `WebScraper`: スクレイピング実行クラス

**主要メソッド:**
- `fetch_page()`: ページコンテンツ取得
- `check_robots_txt()`: robots.txt確認

#### extractor.py（未実装）
HTMLから必要な情報を抽出。

**主要クラス:**
- `InfoExtractor`: 情報抽出クラス

**主要メソッド:**
- `extract_phone()`: 電話番号抽出
- `extract_email()`: メールアドレス抽出
- `extract_address()`: 住所抽出

#### browser.py（未実装）
Seleniumを使用したブラウザ制御。

**主要クラス:**
- `BrowserController`: ブラウザ制御クラス

### 3. output/ - 出力機能モジュール（Phase 1で実装）

#### excel_writer.py（未実装）
Excel形式でのデータ出力。

**主要クラス:**
- `ExcelWriter`: Excel出力クラス

#### formatter.py（未実装）
データの整形、重複除去。

**主要クラス:**
- `DataFormatter`: データフォーマットクラス

### 4. gui/ - GUIモジュール（Phase 3で実装）

CustomTkinterを使用したデスクトップGUI。

#### main_window.py（未実装）
アプリケーションのメインウィンドウ。

#### search_panel.py（未実装）
検索設定を入力するパネル。

#### result_panel.py（未実装）
検索結果を表示するパネル。

### 5. utils/ - ユーティリティモジュール

#### logger.py（実装済み）
アプリケーション全体のログ出力を管理。

**主要クラス:**
- `AppLogger`: ログ管理クラス

**使用例:**
```python
from utils.logger import get_logger

logger = get_logger(__name__)
logger.info("情報メッセージ")
logger.error("エラーメッセージ")
```

#### validators.py（未実装）
入力値のバリデーション。

#### file_utils.py（未実装）
ファイル操作のユーティリティ。

#### text_utils.py（未実装）
テキスト処理のユーティリティ。

### 6. tests/ - テストモジュール（Phase 2-4で実装）

pytestを使用した単体テスト・統合テスト。

## 依存関係

### 外部ライブラリ（requirements.txt）

```
selenium==4.16.0          # ブラウザ自動操作
beautifulsoup4==4.12.2    # HTML解析
requests==2.31.0          # HTTP通信
lxml==5.1.0               # XML/HTMLパーサー
pandas==2.1.4             # データ処理
openpyxl==3.1.2           # Excel操作
customtkinter==5.2.1      # モダンなGUI
webdriver-manager==4.0.1  # ChromeDriver自動管理
python-dotenv==1.0.0      # 環境変数管理
pytest==7.4.3             # テストフレームワーク
pytest-cov==4.1.0         # カバレッジ測定
flake8==7.0.0             # Linter
black==23.12.1            # コードフォーマッター
```

### モジュール間の依存関係

```
main.py
  └── utils/logger.py

core/searcher.py（予定）
  ├── core/browser.py
  ├── config/settings.py
  ├── config/constants.py
  └── utils/logger.py

core/scraper.py（予定）
  ├── core/browser.py
  ├── config/settings.py
  └── utils/logger.py

core/extractor.py（予定）
  ├── config/constants.py
  └── utils/logger.py

output/excel_writer.py（予定）
  ├── output/formatter.py
  ├── config/settings.py
  └── utils/logger.py

gui/main_window.py（予定）
  ├── gui/search_panel.py
  ├── gui/result_panel.py
  ├── core/searcher.py
  ├── output/excel_writer.py
  └── utils/logger.py
```

## データフロー

```
[ユーザー入力]
    ↓
[GUI Layer / CLI]
    ↓
[core/searcher.py]
    → Google検索実行
    → 検索結果取得
    ↓
[core/scraper.py]
    → 各URLにアクセス
    → HTML取得
    ↓
[core/extractor.py]
    → 情報抽出（電話番号、住所等）
    ↓
[output/formatter.py]
    → データ整形
    → 重複除去
    ↓
[output/excel_writer.py]
    → Excel出力
    ↓
[ファイル保存]
```

## 開発状況

### Phase 0: プロジェクト構造設計（完了）
- [x] ディレクトリ構造作成
- [x] 基本ファイル作成
- [x] 設定モジュール作成
- [x] ログモジュール作成
- [x] requirements.txt作成
- [x] README.md作成

### Phase 1: MVP実装（次のステップ）
- [ ] core/searcher.py実装
- [ ] core/scraper.py実装
- [ ] core/extractor.py実装
- [ ] core/browser.py実装
- [ ] output/excel_writer.py実装
- [ ] output/formatter.py実装
- [ ] main.py（CLI版）実装

### Phase 2: 詳細情報抽出機能（未着手）
### Phase 3: GUI実装（未着手）
### Phase 4: テスト・ドキュメント整備（未着手）

## 次のアクション

1. **Phase 1開始準備**
   - API設計書の作成（docs/api_design.md）
   - データモデルクラスの定義

2. **コア機能実装**
   - core/searcher.py から実装開始
   - 基本的な検索機能を実装
   - 単体テストを並行して作成

3. **動作確認**
   - main.py（CLI版）で動作確認
   - 基本的な検索→抽出→Excel出力フローの確立

## 補足

このプロジェクト構造は、実装計画書（docs/implementation_plan.md）に基づいて設計されています。
詳細な実装方針やスケジュールについては、実装計画書を参照してください。
