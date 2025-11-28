# Google検索リサーチツール

クラウドワークスなどのリサーチ案件における情報収集作業を自動化・効率化するツールです。

## 概要

Google検索結果から情報を自動収集し、Excel形式で出力するデスクトップアプリケーションです。

### 主な機能

- Google検索結果の自動取得
- Webページからの詳細情報抽出（電話番号、メールアドレス、住所等）
- Excel形式でのデータ出力
- 検索設定のプリセット管理
- 直感的なGUIインターフェース

## 開発ステータス

現在開発中です。以下のPhaseで段階的に実装を進めています。

- [x] Phase 0: プロジェクト構造設計
- [ ] Phase 1: MVP（基本検索・抽出・Excel出力）
- [ ] Phase 2: 詳細情報抽出機能の拡充
- [ ] Phase 3: GUI実装
- [ ] Phase 4: テスト・バグ修正・ドキュメント整備

## 必要要件

- Python 3.10以上
- Google Chrome または Chromium
- インターネット接続

## セットアップ

### 1. リポジトリのクローン

```bash
git clone <repository-url>
cd google_research
```

### 2. 仮想環境の作成と有効化

```bash
# 仮想環境の作成
python -m venv venv

# 仮想環境の有効化
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

### 4. 動作確認

```bash
python main.py --help
```

## 使い方

（Phase 1実装後に追記予定）

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

- [要件定義書](docs/requirements_specification.md)
- [実装計画書](docs/implementation_plan.md)
- [要件メモ](docs/requirements_memo.txt)

## 注意事項

### 利用規約について

本ツールはGoogle検索結果のスクレイピングを行うため、Googleの利用規約に抵触する可能性があります。以下の点にご注意ください。

1. 過度なアクセスは避けてください
2. アクセス間隔は最低3秒以上に設定してください
3. 商用利用や大量データ収集にはGoogle Custom Search API の利用を推奨します
4. 各Webサイトのrobots.txtを遵守してください

### 法的責任

本ツールの使用は自己責任で行ってください。開発者は本ツールの使用により生じたいかなる損害についても責任を負いません。

## ライセンス

（後日追加予定）

## 貢献

（後日追加予定）

## 開発者

（後日追加予定）

## 変更履歴

- 2025-11-28: プロジェクト初期化、要件定義・実装計画作成
