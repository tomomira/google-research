# Google検索リサーチツール

クラウドワークスなどのリサーチ案件における情報収集作業を自動化・効率化するツールです。

## 概要

検索APIを使って情報を自動収集し、Excel形式で出力するCLIアプリケーションです。

### 主な機能

- **Tavily API統合検索**: 月1,000件まで無料で検索可能
- **Webページからの詳細情報抽出**: 電話番号、メールアドレス、住所、SNSリンク等
- **Excel形式での自動出力**: 整形済みデータを即座にExcelファイルで取得
- **柔軟なAPI切り替え**: TavilyとGoogle APIを簡単に切り替え可能
- **CLI操作**: シンプルで直感的なコマンドライン操作

## 開発ステータス

**Phase 1完了 - 本番運用可能！** ✨

- [x] Phase 0: プロジェクト構造設計
- [x] **Phase 1: MVP（基本検索・抽出・Excel出力）** ✅ 完了
- [x] **Tavily API統合** ✅ 完了（2025年11月28日）
- [ ] Phase 2: 詳細情報抽出機能の拡充
- [ ] Phase 3: GUI実装
- [ ] Phase 4: テスト・バグ修正・ドキュメント整備

## 必要要件

- Python 3.10以上
- インターネット接続
- Tavily APIキー（無料、クレジットカード不要）

## クイックスタート

### 1. リポジトリのクローン

```bash
git clone <repository-url>
cd google_research
```

### 2. 仮想環境の作成と有効化

```bash
# 仮想環境の作成
python -m venv venv

# 仮想環境の有効化（macOS/Linux）
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

### 4. Tavily APIキーの取得と設定

詳細は [docs/TAVILY_SETUP.md](docs/TAVILY_SETUP.md) を参照

```bash
# 1. https://app.tavily.com/ でアカウント作成（無料）
# 2. APIキーをコピー
# 3. .envファイルを作成
cp .env.example .env

# 4. .envファイルを編集してAPIキーを設定
# TAVILY_API_KEY=tvly-your-api-key-here
```

### 5. 動作確認

```bash
# API接続テスト
python3 test_tavily_api.py

# 全体フローテスト
python3 test_full_flow_tavily.py
```

### 6. 実行

```bash
python3 main.py
```

## 使い方

### 基本的な使用方法

1. **アプリケーションを起動**
```bash
source venv/bin/activate
python3 main.py
```

2. **キーワードを入力**
```
検索キーワードを入力してください: 東京 歯科医院
```

3. **取得件数を指定**（デフォルト: 10件）
```
検索結果の取得件数を入力してください (デフォルト: 10): 10
```

4. **詳細情報取得の有無を選択**
```
詳細情報を取得しますか? (y/n, デフォルト: n): y
```

5. **Excel出力完了**
```
✓ Excelファイルを保存しました: output/search_results_20251128_181243.xlsx
```

### 出力ファイル

- **Excel**: `output/search_results_YYYYMMDD_HHMMSS.xlsx`
  - 順位、タイトル、URL、説明、電話番号、メール、住所等
- **ログ**: `logs/app.log`

## プロジェクト構造

```
google_research/
├── main.py                    # メインエントリーポイント
├── requirements.txt           # 依存パッケージ
├── README.md                  # 本ファイル
├── config/                    # 設定ファイル
├── core/                      # コア機能モジュール
├── gui/                       # GUIモジュール
├── output/                    # 出力機能モジュール
├── utils/                     # ユーティリティ
├── tests/                     # テストコード
├── docs/                      # ドキュメント
├── logs/                      # ログ出力先
└── output/                    # Excel出力先（デフォルト）
```

## ドキュメント

### 主要ドキュメント
- [要件定義書](docs/requirements_specification.md) - 機能要件と非機能要件
- [実装計画書](docs/implementation_plan.md) - システムアーキテクチャと詳細設計
- [Phase 1完了報告](docs/PHASE1_COMPLETE.md) - 実装内容とテスト結果

### Tavily API関連
- [Tavily APIセットアップガイド](docs/TAVILY_SETUP.md) - APIキー取得と設定手順
- [検索API比較](docs/search_api_comparison.md) - Tavily vs Google API
- [Tavily統合完了報告](docs/TAVILY_INTEGRATION.md) - 統合内容と動作確認

## Tavily API無料枠について

- **月間クレジット**: 1,000クエリ/月（無料）
- **クレジットカード**: 不要
- **検索精度**: 約95%（店舗情報リサーチには十分）
- **制限**: 月1,000件を超える場合は有料プラン（$30/月で4,000クエリ）

詳細は [docs/search_api_comparison.md](docs/search_api_comparison.md) を参照

## 注意事項

### API利用規約について

本ツールはTavily APIを使用しています。

1. Tavily APIの利用規約を遵守してください
2. 月1,000件を超える場合は有料プラン検討
3. 大規模運用時はGoogle Custom Search APIへの移行を推奨
4. 各Webサイトのrobots.txtを遵守してください（詳細情報抽出時）

### 法的責任

本ツールの使用は自己責任で行ってください。開発者は本ツールの使用により生じたいかなる損害についても責任を負いません。

## ライセンス

（後日追加予定）

## 貢献

（後日追加予定）

## 開発者

（後日追加予定）

## 技術スタック

- **Python 3.12**
- **Tavily API** - AI最適化検索API
- **BeautifulSoup4** - HTML解析
- **openpyxl** - Excel出力
- **pandas** - データ処理
- **python-dotenv** - 環境変数管理

## 変更履歴

- 2025-11-28:
  - プロジェクト初期化、要件定義・実装計画作成
  - Phase 1実装完了（検索・抽出・Excel出力）
  - Tavily API統合完了
  - 本番運用開始可能
