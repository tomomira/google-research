"""Tavily API接続テスト"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from core.search_api import SearchAPIClient
from core.searcher import SearchOptions
from config.settings import Settings

def test_tavily_connection():
    """Tavily API接続テスト"""

    print("=" * 60)
    print("Tavily API接続テスト")
    print("=" * 60)
    print()

    # 設定確認
    print("[1/3] API設定を確認中...")
    api_key = Settings.TAVILY_API_KEY
    provider = Settings.SEARCH_API_PROVIDER

    if api_key:
        # APIキーの最初と最後の数文字のみ表示
        masked_key = api_key[:5] + "*" * (len(api_key) - 10) + api_key[-5:]
        print(f"✓ TAVILY_API_KEY: {masked_key} (設定済み)")
    else:
        print("✗ TAVILY_API_KEY: 未設定")
        print()
        print("エラー: .envファイルにTAVILY_API_KEYを設定してください")
        return False

    print(f"✓ SEARCH_API_PROVIDER: {provider}")
    print()

    # API接続テスト
    print("[2/3] Tavily APIで検索テスト中...")
    try:
        client = SearchAPIClient(provider="tavily")
        options = SearchOptions(num_results=3)

        # シンプルなキーワードでテスト
        keyword = "Python programming"
        print(f"検索キーワード: {keyword}")

        results = client.search(keyword, options)

        print(f"✓ {len(results)}件の検索結果を取得しました")
        print()

        # 結果を表示
        if results:
            print("--- 検索結果 ---")
            for item in results:
                print(f"{item.rank}. {item.title}")
                print(f"   URL: {item.url}")
                print(f"   説明: {item.description[:100]}...")
                print()
        else:
            print("検索結果が0件でした")
            return False

        # 日本語検索テスト
        print("[3/3] 日本語検索テスト中...")
        keyword_ja = "東京 観光"
        print(f"検索キーワード: {keyword_ja}")

        results_ja = client.search(keyword_ja, options)
        print(f"✓ {len(results_ja)}件の検索結果を取得しました")
        print()

        if results_ja:
            print("--- 日本語検索結果（最初の1件） ---")
            first = results_ja[0]
            print(f"1. {first.title}")
            print(f"   URL: {first.url}")
            print(f"   説明: {first.description[:150]}...")
            print()

        print("=" * 60)
        print("✓ Tavily API接続テスト成功！")
        print("=" * 60)
        print()
        print("次のステップ:")
        print("  - 実際のキーワードで検索を試してください")
        print("  - python3 test_full_flow_tavily.py で全体の動作確認")
        print("=" * 60)

        return True

    except Exception as e:
        print()
        print(f"✗ エラー: {e}")
        print()
        print("トラブルシューティング:")
        print("  1. .envファイルのTAVILY_API_KEYが正しいか確認")
        print("  2. インターネット接続を確認")
        print("  3. Tavilyダッシュボードで残クレジットを確認")
        print("     https://app.tavily.com/")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_tavily_connection()
    sys.exit(0 if success else 1)
