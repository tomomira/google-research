"""Seleniumを使った検索テスト"""

import sys
from pathlib import Path
import time

sys.path.insert(0, str(Path(__file__).parent))

from core.browser import BrowserController
from core.searcher import GoogleSearcher, SearchOptions
from bs4 import BeautifulSoup

def test_selenium_search():
    """Seleniumを使った検索テスト"""

    print("=" * 60)
    print("Selenium検索テスト")
    print("=" * 60)
    print()

    keyword = "Python プログラミング"
    searcher = GoogleSearcher()
    options = SearchOptions(num_results=3)

    # 検索URLの構築
    search_url = searcher.build_search_url(keyword, options)
    print(f"検索URL: {search_url}")
    print()

    try:
        print("[1/3] Seleniumブラウザを起動中...")
        with BrowserController(headless=True) as browser:
            print("✓ ブラウザ起動成功")
            print()

            print("[2/3] ページを取得中...")
            html = browser.get_page(search_url)
            print(f"✓ HTML取得成功（長さ: {len(html)}文字）")
            print()

            # HTMLをファイルに保存
            debug_file = Path("debug_selenium_search.html")
            with open(debug_file, "w", encoding="utf-8") as f:
                f.write(html)
            print(f"HTMLを保存しました: {debug_file}")
            print()

            print("[3/3] 検索結果をパース中...")
            results = searcher.parse_search_results(html, options.num_results)
            print(f"✓ {len(results)}件の検索結果を取得")
            print()

            if results:
                print("--- 検索結果 ---")
                for item in results:
                    print(f"{item.rank}. {item.title}")
                    print(f"   URL: {item.url}")
                    print(f"   説明: {item.description[:100]}...")
                    print()
                print("=" * 60)
                print("✓ テスト成功！")
                return True
            else:
                print("検索結果が0件でした。HTMLの構造を確認してください。")
                return False

    except Exception as e:
        print(f"✗ エラー: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_selenium_search()
    sys.exit(0 if success else 1)
