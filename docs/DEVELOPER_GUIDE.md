# Google検索リサーチツール - 開発者ガイド

**バージョン**: 1.0.0
**最終更新**: 2025年12月1日

---

## 目次

1. [開発環境のセットアップ](#開発環境のセットアップ)
2. [プロジェクト構造](#プロジェクト構造)
3. [アーキテクチャ](#アーキテクチャ)
4. [コーディング規約](#コーディング規約)
5. [テスト](#テスト)
6. [デバッグ](#デバッグ)
7. [リリース手順](#リリース手順)

---

## 開発環境のセットアップ

### 必須ツール

- Python 3.10+
- Git
- テキストエディタ（VS Code推奨）

### 開発用パッケージのインストール

```bash
# 仮想環境の作成と有効化
python3 -m venv venv
source venv/bin/activate

# 依存パッケージのインストール
pip install -r requirements.txt

# 開発用パッケージ（必要に応じて）
pip install pytest pytest-cov black flake8
```

### VS Codeの設定

`.vscode/settings.json`:

```json
{
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": ["tests/"]
}
```

---

## プロジェクト構造

```
google_research/
├── config/                 # 設定ファイル
│   ├── __init__.py
│   ├── constants.py       # 定数定義
│   └── settings.py        # アプリ設定
├── core/                   # コア機能
│   ├── __init__.py
│   ├── search_api.py      # 検索APIクライアント
│   ├── scraper.py         # Webスクレイパー
│   ├── extractor.py       # 情報抽出
│   └── searcher.py        # 検索制御
├── gui/                    # GUI関連
│   ├── __init__.py
│   ├── main_window.py     # メインウィンドウ
│   └── components/        # UIコンポーネント
│       ├── __init__.py
│       ├── search_panel.py
│       └── result_panel.py
├── output/                 # 出力機能
│   ├── __init__.py
│   ├── formatter.py       # データ整形
│   └── excel_writer.py    # Excel出力
├── utils/                  # ユーティリティ
│   ├── __init__.py
│   └── logger.py          # ログ機能
├── tests/                  # テストコード
│   ├── __init__.py
│   ├── test_extractor.py
│   ├── test_formatter.py
│   └── test_integration.py
├── docs/                   # ドキュメント
├── logs/                   # ログ出力先
├── output/                 # Excel出力先
├── main.py                 # CLIエントリーポイント
├── main_gui.py             # GUIエントリーポイント
├── requirements.txt        # 依存パッケージ
├── .env.example            # 環境変数テンプレート
└── README.md               # プロジェクト概要
```

---

## アーキテクチャ

### レイヤー構成

```
┌─────────────────────────────────────┐
│        GUI Layer (Phase 3)          │
│  CustomTkinter - ユーザーI/F        │
└─────────────┬───────────────────────┘
              │
┌─────────────▼───────────────────────┐
│      Application Layer              │
│  main.py, main_gui.py               │
└─────────────┬───────────────────────┘
              │
    ┌─────────┴─────────┐
    │                   │
┌───▼────────┐   ┌──────▼──────┐
│Core Layer  │   │Output Layer │
│- SearchAPI │   │- Formatter  │
│- Scraper   │   │- ExcelWriter│
│- Extractor │   └─────────────┘
└────────────┘
    │
┌───▼────────┐
│Utils Layer │
│- Logger    │
│- Config    │
└────────────┘
```

### データフロー

```
検索キーワード
    ↓
SearchAPIClient (Tavily/Google)
    ↓
SearchItem[] (検索結果)
    ↓
WebScraper (HTML取得)
    ↓
InfoExtractor (情報抽出)
    ↓
DetailedInfo[] (詳細情報)
    ↓
DataFormatter (整形・重複除去)
    ↓
OutputData[] (出力用データ)
    ↓
ExcelWriter (Excel出力)
    ↓
search_results_*.xlsx
```

### 主要なデータモデル

#### SearchItem（検索結果）

```python
@dataclass
class SearchItem:
    rank: int              # 順位
    title: str             # タイトル
    url: str               # URL
    description: str       # 説明文
    snippet: str           # スニペット
```

#### DetailedInfo（詳細情報）

```python
@dataclass
class DetailedInfo:
    phone: list[str]                      # 電話番号リスト
    email: list[str]                      # メールアドレスリスト
    address: Optional[dict]               # 住所情報
    fax: list[str]                        # FAX番号リスト
    company_name: Optional[str]           # 会社名・店舗名
    sns_links: dict[str, list[str]]       # SNSリンク
    business_hours: Optional[str]         # 営業時間
    closed_days: Optional[str]            # 定休日
```

#### OutputData（Excel出力用）

```python
@dataclass
class OutputData:
    rank: int
    title: str
    url: str
    description: str
    phone: str = ""
    email: str = ""
    postal_code: str = ""
    prefecture: str = ""
    fax: str = ""
    company_name: str = ""
    sns_twitter: str = ""
    sns_facebook: str = ""
    sns_instagram: str = ""
    business_hours: str = ""
    closed_days: str = ""
```

---

## コーディング規約

### スタイルガイド

**PEP 8準拠**を基本とし、以下の追加ルールを適用:

#### 1. 命名規則

```python
# クラス: PascalCase
class InfoExtractor:
    pass

# 関数・変数: snake_case
def extract_phone(html: str) -> list[str]:
    phone_numbers = []
    return phone_numbers

# 定数: UPPER_SNAKE_CASE
MAX_RETRIES = 3
DEFAULT_WAIT_TIME = 3.0

# プライベート: 先頭にアンダースコア
def _internal_method(self):
    pass
```

#### 2. 型ヒント

すべての関数に型ヒントを付ける:

```python
def extract_email(self, html: str) -> list[str]:
    """メールアドレスを抽出

    Args:
        html: 解析対象のHTML文字列

    Returns:
        抽出されたメールアドレスのリスト
    """
    pass
```

#### 3. Docstring

Google形式のdocstringを使用:

```python
def extract_address(self, html: str) -> Optional[dict]:
    """住所情報を抽出

    Args:
        html: 解析対象のHTML文字列

    Returns:
        住所情報の辞書。抽出できなかった場合はNone
        {
            "postal_code": "150-0001",
            "prefecture": "東京都",
            "city": "渋谷区",
            "address": "神宮前1-2-3"
        }

    Raises:
        ValueError: HTMLが不正な場合
    """
    pass
```

#### 4. インポート順序

```python
# 1. 標準ライブラリ
import sys
from pathlib import Path
from typing import Optional

# 2. サードパーティライブラリ
import pandas as pd
from bs4 import BeautifulSoup

# 3. ローカルモジュール
from config.settings import Settings
from utils.logger import get_logger
```

#### 5. 行の長さ

- 最大100文字（PEP 8の79文字より緩和）

---

## テスト

### テストの実行

#### すべてのテストを実行

```bash
pytest tests/ -v
```

#### 特定のテストのみ実行

```bash
pytest tests/test_extractor.py -v
```

#### カバレッジ測定

```bash
pytest tests/ --cov=core --cov=output --cov-report=term-missing
```

#### カバレッジHTML レポート

```bash
pytest tests/ --cov=core --cov=output --cov-report=html
# htmlcov/index.htmlを開く
```

### テストの書き方

#### フィクスチャの使用

```python
import pytest

@pytest.fixture
def extractor():
    """InfoExtractorのフィクスチャ"""
    return InfoExtractor()

def test_extract_phone(extractor):
    """電話番号抽出のテスト"""
    html = "<p>電話: 03-1234-5678</p>"
    phones = extractor.extract_phone(html)
    assert "03-1234-5678" in phones
```

#### パラメータ化テスト

```python
@pytest.mark.parametrize("html,expected", [
    ("<p>03-1234-5678</p>", "03-1234-5678"),
    ("<p>0120-123-456</p>", "0120-123-456"),
    ("<p>090-1234-5678</p>", "090-1234-5678"),
])
def test_extract_phone_patterns(extractor, html, expected):
    """様々な電話番号パターンのテスト"""
    phones = extractor.extract_phone(html)
    assert expected in phones
```

### テストカバレッジ目標

- **全体**: 70%以上
- **core/extractor.py**: 80%以上
- **output/formatter.py**: 90%以上
- **output/excel_writer.py**: 80%以上

---

## デバッグ

### ログ出力

#### ログレベル

```python
from utils.logger import get_logger

logger = get_logger(__name__)

logger.debug("デバッグ情報")      # 開発時のみ
logger.info("情報メッセージ")     # 通常の動作
logger.warning("警告メッセージ")  # 警告
logger.error("エラーメッセージ")  # エラー
```

#### ログファイル

- **場所**: `logs/app.log`
- **ローテーション**: 10MB x 5ファイル

### デバッグモード

```python
# settings.pyで設定
DEBUG = True  # デバッグモード有効
```

### よく使うデバッグテクニック

#### 1. pdbの使用

```python
import pdb; pdb.set_trace()
```

#### 2. ログ出力での確認

```python
logger.debug(f"HTML length: {len(html)}")
logger.debug(f"Extracted phones: {phones}")
```

#### 3. 例外の詳細情報

```python
try:
    # 処理
    pass
except Exception as e:
    logger.error(f"Error occurred: {e}", exc_info=True)
```

---

## リリース手順

### 1. バージョン番号の更新

```bash
# __init__.pyなどにバージョンを記載
__version__ = "1.0.0"
```

### 2. 変更履歴の更新

`CHANGELOG.md`を作成・更新:

```markdown
# Changelog

## [1.0.0] - 2025-12-01

### Added
- GUI版リリース
- CustomTkinter使用

### Changed
- 詳細情報抽出の精度向上

### Fixed
- Excel出力時の列名バグ修正
```

### 3. テストの実行

```bash
# すべてのテストが合格することを確認
pytest tests/ -v
```

### 4. ドキュメントの確認

- README.md
- USER_GUIDE.md
- DEVELOPER_GUIDE.md

### 5. Gitタグの作成

```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

### 6. GitHubリリースの作成

1. GitHubのReleasesページに移動
2. "Create a new release"をクリック
3. タグを選択
4. リリースノートを記載
5. "Publish release"をクリック

---

## 貢献

### プルリクエストの流れ

1. **Issueの作成**: 機能追加・バグ修正の前にIssueを作成
2. **ブランチの作成**: `feature/feature-name`または`bugfix/bug-name`
3. **実装**: コーディング規約に従って実装
4. **テストの追加**: 新機能には必ずテストを追加
5. **プルリクエスト**: mainブランチに対してPR作成
6. **レビュー**: コードレビューを受ける
7. **マージ**: レビュー承認後にマージ

### コミットメッセージの書き方

```
<type>: <subject>

<body>

<footer>
```

**Type**:
- `feat`: 新機能
- `fix`: バグ修正
- `docs`: ドキュメント
- `test`: テスト
- `refactor`: リファクタリング

**例**:
```
feat: 営業時間抽出機能を追加

core/extractor.pyに営業時間を抽出する機能を追加しました。
5種類の正規表現パターンに対応しています。

Closes #123
```

---

## 参考資料

- [PEP 8 -- Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [pytest Documentation](https://docs.pytest.org/)
- [CustomTkinter Documentation](https://github.com/TomSchimansky/CustomTkinter)
- [Tavily API Documentation](https://docs.tavily.com/)

---

**Happy Coding! 🚀**
