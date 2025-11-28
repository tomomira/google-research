"""検索結果のデバッグ"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from core.searcher import GoogleSearcher, SearchOptions

def debug_search():
    """検索結果のデバッグ"""

    print("検索結果HTMLのデバッグ")
    print("=" * 60)

    searcher = GoogleSearcher()
    keyword = "Python"  # シンプルなキーワードでテスト
    options = SearchOptions(num_results=3)

    # 検索URLの構築
    url = searcher.build_search_url(keyword, options)
    print(f"検索URL: {url}")
    print()

    # HTMLの取得
    try:
        html = searcher._fetch_search_results(url)
        print(f"HTML取得成功（長さ: {len(html)}文字）")
        print()

        # HTMLの一部を表示
        print("HTML の最初の1000文字:")
        print("-" * 60)
        print(html[:1000])
        print("-" * 60)
        print()

        # HTMLをファイルに保存
        debug_file = Path("debug_google_search.html")
        with open(debug_file, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"HTMLを保存しました: {debug_file}")
        print()

        # パース処理
        print("検索結果のパース:")
        print("-" * 60)
        results = searcher.parse_search_results(html, options.num_results)
        print(f"パース結果: {len(results)}件")

        for i, item in enumerate(results, 1):
            print(f"\n{i}. {item.title}")
            print(f"   URL: {item.url}")
            print(f"   説明: {item.description[:100]}...")

    except Exception as e:
        print(f"エラー: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_search()
