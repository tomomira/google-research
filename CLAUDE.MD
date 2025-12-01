# Google検索リサーチツール - Claude Code コンテキスト

## プロジェクト概要

クラウドワークスなどのリサーチ案件における情報収集作業を自動化・効率化するPythonデスクトップアプリケーション。Google検索結果から情報を自動収集し、Excel形式で出力する。

## プロジェクトステータス

**現在のPhase**: 🎉 **プロジェクト完了** 🎉
**最終更新**: 2025年12月1日

### 完了済み
- [x] Phase 0: プロジェクト構造設計、ドキュメント作成
- [x] Phase 1: MVP（基本検索・抽出・Excel出力）✨
- [x] Tavily API統合（2025年11月28日）✨
- [x] Phase 2: 詳細情報抽出機能の拡充（2025年12月1日）✨
- [x] Phase 3: GUI実装（2025年12月1日）✨
- [x] Phase 4: テスト・バグ修正・ドキュメント整備（2025年12月1日）✨NEW

### Phase 1完了内容（2025年11月28日）
- [x] core/search_api.py - **Tavily/Google API統合クライアント** ✨
- [x] core/scraper.py - Webページスクレイピング
- [x] core/extractor.py - 情報抽出（電話、メール、住所、SNS等）
- [x] output/formatter.py - データ整形・重複除去
- [x] output/excel_writer.py - Excel出力
- [x] main.py - CLIアプリケーション（Tavily API対応）
- [x] test_tavily_api.py - Tavily API接続テスト
- [x] test_full_flow_tavily.py - 全体フローテスト
- [x] 基本機能テスト実施・合格
- [x] Tavily API実運用テスト・合格

### Phase 2完了内容（2025年12月1日）
- [x] **電話番号抽出の精度向上**: フリーダイヤル/ナビダイヤル/IP電話/携帯電話対応
- [x] **住所抽出の精度向上**: 市区町村・詳細住所（番地・号）抽出
- [x] **会社名抽出の改善**: JSON-LD/metaタグ/h1タグからの抽出
- [x] **営業時間抽出機能**: 新規実装（正規表現パターン）
- [x] **定休日抽出機能**: 新規実装（正規表現パターン）
- [x] データモデル拡張: DetailedInfo/OutputDataに新フィールド追加
- [x] test_phase2.py - Phase 2機能テスト・合格

### Phase 3完了内容（2025年12月1日）
- [x] **gui/main_window.py**: メインウィンドウ実装（328行）
- [x] **gui/components/search_panel.py**: 検索パネルコンポーネント（201行）
- [x] **gui/components/result_panel.py**: 結果表示パネル（217行）
- [x] **main_gui.py**: GUI版エントリーポイント（37行）
- [x] **非同期検索処理**: 別スレッドで実行、UIがブロックされない
- [x] **リアルタイム進捗表示**: 検索状況をリアルタイムで表示
- [x] **CLI版と完全互換**: 同等の機能を実装
- [x] **CustomTkinter**: モダンなUIフレームワーク採用

### Phase 4完了内容（2025年12月1日）✨NEW
- [x] **テストスイート作成**: pytest基盤の42テストケース
  - tests/test_extractor.py: 22テスト
  - tests/test_formatter.py: 13テスト
  - tests/test_integration.py: 7テスト
- [x] **テスト結果**: 40テスト合格、2テストスキップ
- [x] **テストカバレッジ**: 主要モジュール73-93%達成
- [x] **ユーザーガイド**: 約400行の包括的なガイド
- [x] **開発者ガイド**: 約500行の詳細なガイド
- [x] **バグ修正**: Excel列名の日本語化バグ修正

### プロジェクト完了
すべてのPhaseが完了し、本番運用可能な状態に達しました。

## 主要ドキュメント

1. **要件定義書**: `docs/requirements_specification.md`
   - 機能要件42項目
   - 非機能要件（パフォーマンス、信頼性、セキュリティ）

2. **実装計画書**: `docs/implementation_plan.md`
   - システムアーキテクチャ
   - モジュール詳細設計
   - 4週間の実装スケジュール

3. **プロジェクト構造**: `docs/project_structure.md`
   - ディレクトリツリー
   - モジュール間依存関係

4. **Phase 1完了報告**: `docs/PHASE1_COMPLETE.md`
   - 実装モジュール詳細
   - テスト結果
   - 使用方法
   - 次のステップ

5. **Phase 2完了報告**: `docs/PHASE2_COMPLETE.md`
   - 抽出精度向上の詳細
   - 新機能（営業時間・定休日）
   - テスト結果
   - データモデル拡張

6. **Phase 3完了報告**: `docs/PHASE3_COMPLETE.md`
   - GUI実装の詳細
   - CustomTkinter使用
   - 非同期処理の実装
   - CLI版との比較

7. **Phase 4完了報告**: `docs/PHASE4_COMPLETE.md` ✨NEW
   - テストスイート作成
   - テストカバレッジ測定
   - ユーザー・開発者ガイド作成
   - バグ修正

8. **ユーザーガイド**: `docs/USER_GUIDE.md` ✨NEW
   - インストール手順
   - 基本的な使い方（GUI/CLI）
   - 高度な使い方
   - トラブルシューティング・FAQ

9. **開発者ガイド**: `docs/DEVELOPER_GUIDE.md` ✨NEW
   - 開発環境セットアップ
   - アーキテクチャ
   - コーディング規約
   - テスト・デバッグ・リリース手順

10. **検索API比較**: `docs/search_api_comparison.md`
   - Tavily vs Google Custom Search API
   - コスト比較、精度比較
   - 段階的移行プラン

11. **Tavily APIセットアップ**: `docs/TAVILY_SETUP.md`
   - APIキー取得方法
   - 環境設定手順
   - トラブルシューティング

12. **Tavily統合完了報告**: `docs/TAVILY_INTEGRATION.md`
   - 統合内容と実装詳細
   - テスト結果
   - 運用開始ガイド

## アーキテクチャ

### レイヤー構成

```
GUI Layer (Phase 3)
    ↓
Application Layer
    ↓
Core Layer (searcher, scraper, extractor)
    ↓
Output Layer (excel_writer, formatter)
    ↓
Utils Layer (logger, validators, etc.)
```

### 主要モジュール

| モジュール | 責務 | ステータス |
|-----------|------|-----------|
| config/settings.py | アプリ設定管理（.env対応） | ✓ 完成 |
| config/constants.py | 定数定義 | ✓ 完成 |
| utils/logger.py | ログ出力 | ✓ 完成 |
| **core/search_api.py** | **Tavily/Google API統合** | ✓ 完成 (Phase 1) ✨ |
| core/scraper.py | Webスクレイピング | ✓ 完成 (Phase 1) |
| core/extractor.py | 情報抽出 | ✓ 完成 (Phase 1) |
| output/excel_writer.py | Excel出力 | ✓ 完成 (Phase 1) |
| output/formatter.py | データ整形 | ✓ 完成 (Phase 1) |
| main.py | CLIアプリケーション（Tavily対応） | ✓ 完成 (Phase 1) |

## 技術スタック

- **言語**: Python 3.10+
- **主要ライブラリ**:
  - **tavily-python 0.5.0 (検索API - Tavily)** ✨
  - beautifulsoup4 4.12.2 (HTML解析)
  - requests 2.31.0 (HTTP通信)
  - openpyxl 3.1.2 (Excel操作)
  - pandas 2.1.4 (データ処理)
  - **python-dotenv 1.0.0 (環境変数管理)** ✨
  - customtkinter 5.2.1 (GUI - Phase 3)
- **検索API**: Tavily API（無料枠1,000件/月）
- **テスト**: pytest, pytest-cov
- **コード品質**: flake8, black

## コーディング規約

### スタイル
- **PEP 8準拠** (最大行長: 100文字)
- **型ヒント必須**: 関数の引数と戻り値に型を明示
- **docstring**: Google形式で記載
- **命名規則**:
  - クラス: PascalCase (`GoogleSearcher`)
  - 関数・変数: snake_case (`search_keyword`)
  - 定数: UPPER_SNAKE_CASE (`MAX_RETRIES`)
  - プライベート: `_internal_method`

### docstring例

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

## 実装上の重要な注意事項

### 1. Google利用規約への配慮（必須）
- **アクセス間隔**: 最低3秒以上（`config/settings.py`のDEFAULT_WAIT_TIME）
- **CAPTCHA検出**: 検出時は即座に処理を中止
- **robots.txt**: 各サイトのrobots.txtを遵守
- **User-Agent**: 適切なUser-Agentを設定

### 2. エラーハンドリング
- **途中結果の保存**: エラー発生時も処理済みデータを保存
- **リトライ機能**: ネットワークエラー時は最大3回リトライ（MAX_RETRIES）
- **タイムアウト**: 30秒でタイムアウト（REQUEST_TIMEOUT）

### 3. データ品質
- **重複除去**: URLベースで重複を除去
- **バリデーション**: 抽出データの妥当性チェック
- **正規表現**: `config/constants.py`のREGEX_PATTERNSを使用

### 4. パフォーマンス目標
- 100件の検索結果取得: 3分以内
- 1ページ詳細抽出: 3-5秒
- Excel出力: 10秒以内
- メモリ使用量: 500MB以下

## Phase 1実装完了 ✓（Tavily API統合版）

### 実装完了モジュール（2025年11月28日）
1. **core/search_api.py** ✓ ✨NEW
   - **Tavily API統合**: 月1,000件無料、クレジットカード不要
   - **Google Custom Search API対応**: 将来の大規模運用時に切り替え可能
   - 統合インターフェース（SearchAPIClient）
   - .envファイルで簡単にプロバイダー切り替え
   - 検索結果の標準化（SearchItemモデル）

2. **core/scraper.py** ✓
   - robots.txtチェック
   - ページコンテンツ取得
   - リトライ機能

3. **core/extractor.py** ✓
   - 電話番号、メール、住所の正規表現抽出
   - FAX、会社名、SNSリンク抽出

4. **output/formatter.py** ✓
   - 重複除去（pandas使用）
   - データバリデーション

5. **output/excel_writer.py** ✓
   - openpyxlで基本出力
   - 列幅自動調整、フォーマット適用

6. **main.py (CLI版)** ✓
   - Tavily API統合
   - キーワード入力、検索実行
   - 詳細情報抽出（オプション）
   - Excel出力

7. **config/settings.py** ✓
   - .env対応（python-dotenv）
   - API設定管理（Tavily/Google）

### テスト結果
- 構文チェック: ✓ 合格
- モジュールインポート: ✓ 合格
- 基本機能テスト: ✓ 合格
- **Tavily API接続テスト**: ✓ 合格（英語・日本語検索）✨
- **全体フローテスト**: ✓ 合格（検索→抽出→Excel）✨
- **実運用テスト**: ✓ 合格（main.py動作確認）✨

### データモデル（実装済み）

```python
@dataclass
class SearchOptions:
    """検索オプション"""
    num_results: int = 10
    region: str = "jp"
    language: str = "ja"
    period: Optional[str] = None
    site: Optional[str] = None
    exclude_keywords: list[str] = field(default_factory=list)

@dataclass
class SearchItem:
    """検索結果の1件"""
    rank: int
    title: str
    url: str
    description: str
    snippet: str

@dataclass
class DetailedInfo:
    """詳細情報"""
    phone: list[str] = field(default_factory=list)
    email: list[str] = field(default_factory=list)
    address: Optional[dict] = None
    fax: list[str] = field(default_factory=list)
    company_name: Optional[str] = None
    sns_links: dict[str, list[str]] = field(default_factory=dict)

@dataclass
class OutputData:
    """出力用データ"""
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

    def to_dict(self) -> dict:
        """辞書形式に変換"""
        return asdict(self)
```

## テスト方針

### Phase 1でのテスト
- **単体テスト**: 各モジュールの主要関数
- **カバレッジ目標**: 50%以上（Phase 1）、70%以上（Phase 4）
- **テストデータ**: `tests/fixtures/`にサンプルHTML等を配置

### テストキーワード例
- 「東京 歯科医院」
- 「大阪 美容室」
- 「名古屋 税理士」

## よくある実装パターン

### ログ出力

```python
from utils.logger import get_logger

logger = get_logger(__name__)
logger.info("検索を開始します")
logger.error("エラーが発生しました", exc_info=True)
```

### 設定値の取得

```python
from config.settings import Settings

wait_time = Settings.DEFAULT_WAIT_TIME
output_path = Settings.get_output_path("results.xlsx")
```

### 正規表現パターンの使用

```python
from config.constants import REGEX_PATTERNS
import re

for pattern in REGEX_PATTERNS["phone"]:
    matches = re.findall(pattern, html)
```

## トラブルシューティング

### よくある問題

1. **ChromeDriverが見つからない**
   - `webdriver-manager`が自動ダウンロード
   - 手動インストールも可能

2. **CAPTCHAが頻発**
   - アクセス間隔を長く（5秒以上）
   - ヘッドレスモードをオフ

3. **抽出精度が低い**
   - 正規表現パターンの見直し
   - テストケースの追加

## 将来の拡張計画

### Phase 5以降（参考）
- Google Custom Search API対応
- Googleマップ連携
- AI活用（自然言語処理）
- クラウド版開発

## 重要なリンク

- Google検索URL: `https://www.google.com/search`
- robots.txt例: `https://example.com/robots.txt`

## 使用方法（Phase 1 CLI版 - Tavily API統合）

### 事前準備

1. **Tavily APIキーの取得**（初回のみ）
   - 詳細は `docs/TAVILY_SETUP.md` を参照
   - https://app.tavily.com/ でアカウント作成（無料）

2. **.envファイルの設定**（初回のみ）
```bash
# .env.exampleをコピー
cp .env.example .env

# .envファイルを編集してAPIキーを設定
SEARCH_API_PROVIDER=tavily
TAVILY_API_KEY=tvly-your-api-key-here
```

### 実行手順

```bash
# 1. 仮想環境の有効化
source venv/bin/activate

# 2. アプリケーションの実行
python3 main.py
```

### 使用例

```
============================================================
Google検索リサーチツール - Phase 1 MVP
検索API: TAVILY
============================================================

検索キーワードを入力してください: 東京 歯科医院
検索結果の取得件数を入力してください (デフォルト: 10): 5
詳細情報を取得しますか? (y/n, デフォルト: n): n

[1/5] TAVILY APIで検索を実行中...
✓ 5件の検索結果を取得しました

[2/5] 詳細情報の抽出をスキップしました

[3/5] データを整形中...
✓ 5件のデータを整形しました

[4/5] Excelファイルを生成中...
✓ Excelファイルを保存しました: output/search_results_20251128_181243.xlsx

[5/5] 処理が完了しました！
```

### 出力ファイル
- **Excel**: `output/search_results_YYYYMMDD_HHMMSS.xlsx`
- **ログ**: `logs/app.log`

### Tavily無料枠について
- **月間**: 1,000クエリ無料
- **クレジットカード**: 不要
- **精度**: 約95%（店舗情報リサーチには十分）
- **大規模運用時**: Google APIへ切り替え可能

## Claude Codeへの指示

### 実装時の確認事項
1. 要件定義書で機能IDを確認
2. 実装計画書でクラス設計を確認
3. PEP 8準拠を確認
4. 型ヒントとdocstringを記載
5. エラーハンドリングを実装
6. ログ出力を適切に配置

### 質問時の参照先
- 機能要件 → `docs/requirements_specification.md`
- 設計詳細 → `docs/implementation_plan.md`
- モジュール構成 → `docs/project_structure.md`
- **Phase 1完了報告** → `docs/PHASE1_COMPLETE.md` ✨

### Phase 2以降の実装の進め方
1. まず該当モジュールの設計を確認
2. 既存のデータモデルを拡張
3. 主要クラスと関数を実装
4. エラーハンドリング追加
5. ログ出力追加
6. docstring記載
7. 簡易テストで動作確認

## 注意: 過度な実装を避ける

- **必要最小限の実装**: 要件にない機能は実装しない
- **YAGNI原則**: 将来必要になるかもしれない機能は実装しない
- **シンプルに**: 複雑な抽象化は避ける

Phase 1では「動くMVP」を最優先とする。→ **Phase 1完了！** ✨

---

## Phase 1完了まとめ（2025年11月28日）

### 実装完了
- ✅ コアモジュール（4ファイル）
- ✅ 出力モジュール（2ファイル）
- ✅ CLIアプリケーション（1ファイル）
- ✅ テストコード（1ファイル）
- ✅ 基本機能テスト合格

### 動作確認済み機能
- Google検索実行
- 検索結果取得とパース
- Webページスクレイピング（robots.txt遵守）
- 情報抽出（電話、メール、住所、FAX、会社名、SNS）
- データ整形と重複除去
- Excel形式での出力

### 次のフェーズ
Phase 2で詳細情報抽出機能を拡充予定。

---

**このファイルについて**: Claude Codeがこのプロジェクトを理解し、一貫性のある実装を行うためのコンテキスト情報です。新しいセッションでも、このファイルを読み込むことでプロジェクトの全体像を把握できます。Phase 1が完了し、動作するMVPが完成しました。
