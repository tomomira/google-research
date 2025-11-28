# Tavily API セットアップガイド

作成日: 2025年11月28日

## 概要

このガイドでは、Google検索リサーチツールでTavily APIを使用するための設定手順を説明します。

---

## 前提条件

- インターネット接続
- メールアドレス
- クレジットカード**不要**（無料プラン利用時）

---

## ステップ1: Tavily APIキーの取得

### 1.1 Tavilyアカウントの作成

1. **Tavily公式サイトにアクセス**
   - URL: https://app.tavily.com/

2. **Sign Up（サインアップ）をクリック**
   - 右上の「Sign Up」ボタンをクリック

3. **メールアドレスで登録**
   - メールアドレスを入力
   - パスワードを設定
   - 「Create Account」をクリック

4. **メール確認**
   - 登録したメールアドレスに確認メールが届く
   - メール内のリンクをクリックして確認

### 1.2 APIキーの取得

1. **ダッシュボードにログイン**
   - https://app.tavily.com/ にアクセス
   - ログイン

2. **APIキーをコピー**
   - ダッシュボードにAPIキーが表示されます
   - 「API Key」の横にある「Copy」ボタンをクリック
   - または、設定ページから確認可能

3. **APIキーの保存**
   - コピーしたAPIキーをメモ帳などに一時保存

---

## ステップ2: プロジェクトへの設定

### 2.1 .envファイルの作成

1. **プロジェクトルートで.envファイルを作成**

```bash
cd /mnt/c/Users/tomom/docker-container-2025/test/google-research
cp .env.example .env
```

2. **.envファイルを編集**

```bash
nano .env
# または
vi .env
```

3. **APIキーを設定**

```.env
# 検索API設定
SEARCH_API_PROVIDER=tavily

# Tavily API設定
TAVILY_API_KEY=tvly-xxxxxxxxxxxxxxxxxxxxxxxxxx  # ← ここに取得したAPIキーを貼り付け

# Google API設定（今は不要、コメントのまま）
# GOOGLE_API_KEY=your_google_api_key_here
# GOOGLE_CX_ID=your_custom_search_engine_id_here
```

4. **保存して終了**
   - `Ctrl + X` → `Y` → `Enter`（nano の場合）
   - `:wq`（vi の場合）

### 2.2 .envファイルの確認

```bash
cat .env
```

**確認事項:**
- `SEARCH_API_PROVIDER=tavily` になっているか
- `TAVILY_API_KEY` に実際のAPIキーが設定されているか

---

## ステップ3: 動作確認

### 3.1 Tavily API接続テスト

テストスクリプトを実行して、APIキーが正しく設定されているか確認します。

```bash
# 仮想環境の有効化
source venv/bin/activate

# テストスクリプトの実行
python3 test_tavily_api.py
```

**期待される出力:**

```
============================================================
Tavily API接続テスト
============================================================

[1/2] API設定を確認中...
✓ TAVILY_API_KEY: tvly-**************************** (設定済み)
✓ SEARCH_API_PROVIDER: tavily

[2/2] Tavily APIで検索テスト中...
検索キーワード: Python programming
✓ 3件の検索結果を取得しました

--- 検索結果 ---
1. Python (programming language) - Wikipedia
   URL: https://en.wikipedia.org/wiki/Python_(programming_language)
   説明: Python is a high-level, general-purpose programming language...

2. Welcome to Python.org
   URL: https://www.python.org/
   説明: The official home of the Python Programming Language...

3. Learn Python Programming
   URL: https://www.programiz.com/python-programming
   説明: Learn Python programming with examples and tutorials...

============================================================
✓ Tavily API接続テスト成功！
============================================================
```

### 3.2 エラーが発生した場合

**エラー: "TAVILY_API_KEYが設定されていません"**
- `.env`ファイルが作成されているか確認
- `TAVILY_API_KEY`の値が正しく設定されているか確認
- APIキーの前後にスペースが入っていないか確認

**エラー: "Tavily API呼び出しに失敗しました"**
- インターネット接続を確認
- APIキーが正しいか確認（Tavilyダッシュボードで再確認）
- 無料枠を使い切っていないか確認（ダッシュボードで残クレジット確認）

---

## ステップ4: 統合テスト

### 4.1 検索→抽出→Excel出力のフルテスト

```bash
source venv/bin/activate
python3 test_full_flow_tavily.py
```

このテストでは以下を確認します：
1. Tavily APIでの検索
2. 検索結果の取得
3. データの整形
4. Excel出力

---

## Tavily API の無料枠

### 無料プラン
- **月間クレジット**: 1,000クレジット
- **クレジットカード**: 不要
- **有効期限**: なし（毎月リセット）

### クレジット消費
- **基本検索（basic）**: 1クエリ = 1クレジット
- **高度検索（advanced）**: 1クエリ = 2クレジット

### 使用例
- 1日30件検索 × 30日 = 月900クレジット（無料枠内）
- 1案件100件検索 × 月10案件 = 月1,000クレジット（無料枠ギリギリ）

### クレジット確認方法
1. https://app.tavily.com/ にログイン
2. ダッシュボードで残クレジット数を確認

---

## トラブルシューティング

### Q1: APIキーが機能しない

**確認事項:**
1. Tavilyダッシュボードでアカウントが有効か確認
2. APIキーをコピー&ペーストして再設定
3. `.env`ファイルの形式が正しいか確認（`KEY=value`の形式）

### Q2: 無料枠を使い切った

**対処法:**
1. 翌月まで待つ（毎月1日にリセット）
2. 有料プランにアップグレード（$30/月で4,000クレジット）
3. Google Custom Search APIに切り替え

### Q3: 検索結果が0件

**確認事項:**
1. キーワードが適切か確認
2. ネットワーク接続を確認
3. Tavilyのステータスページを確認（https://status.tavily.com/）

---

## 次のステップ

### 本番運用の準備

1. **テスト実行**
   - 実際のキーワードで検索テスト
   - 結果の精度を確認

2. **コスト管理**
   - 月間検索件数を把握
   - 無料枠内で運用できるか確認

3. **将来の計画**
   - 月1,000件を超える場合はGoogle APIへの移行を検討
   - 詳細は `docs/search_api_comparison.md` を参照

---

## 参考リンク

- **Tavily公式サイト**: https://app.tavily.com/
- **Tavily API ドキュメント**: https://docs.tavily.com/
- **Tavily 料金ページ**: https://docs.tavily.com/documentation/api-credits
- **検索API比較**: `docs/search_api_comparison.md`

---

## セキュリティに関する注意

### .envファイルの取り扱い

**重要**: `.env`ファイルにはAPIキーなどの機密情報が含まれます。

1. **Gitにコミットしない**
   - `.gitignore`に`.env`が含まれていることを確認
   - 既に`.gitignore`に追加済み

2. **公開しない**
   - GitHubなどにアップロードしない
   - スクリーンショットを撮らない

3. **共有する場合**
   - `.env.example`を共有（APIキーは含まれていない）
   - 各自で`.env`を作成してもらう

### APIキーが漏洩した場合

1. **すぐにTavilyダッシュボードで無効化**
2. **新しいAPIキーを生成**
3. **`.env`ファイルを更新**

---

**作成者**: 開発チーム
**ステータス**: セットアップ手順完成
**最終更新**: 2025年11月28日
