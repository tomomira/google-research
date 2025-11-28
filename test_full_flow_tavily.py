"""Tavily APIを使った全体フローテスト（検索→抽出→Excel出力）"""

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from core.search_api import SearchAPIClient
from core.searcher import SearchOptions
from core.scraper import WebScraper
from core.extractor import InfoExtractor
from output.formatter import DataFormatter
from output.excel_writer import ExcelWriter
from utils.logger import get_logger

logger = get_logger(__name__)


def test_full_flow():
    """Tavily APIを使った全体フローテスト"""

    print("=" * 60)
    print("Tavily API 全体フローテスト")
    print("検索 → 詳細情報抽出 → Excel出力")
    print("=" * 60)
    print()

    # テストパラメータ
    keyword = "東京 歯科医院"
    num_results = 3  # テストなので少なめ
    extract_details = True  # 詳細情報を抽出

    print(f"検索キーワード: {keyword}")
    print(f"取得件数: {num_results}件")
    print(f"詳細情報取得: {'はい' if extract_details else 'いいえ'}")
    print()
    print("-" * 60)
    print()

    try:
        # 1. Tavily APIで検索
        print("[1/5] Tavily APIで検索中...")
        client = SearchAPIClient(provider="tavily")
        options = SearchOptions(num_results=num_results)
        search_items = client.search(keyword, options)

        print(f"✓ {len(search_items)}件の検索結果を取得しました")
        print()

        # 検索結果の表示
        print("--- 検索結果 ---")
        for item in search_items:
            print(f"{item.rank}. {item.title}")
            print(f"   URL: {item.url}")
            print()

        # 2. 詳細情報の抽出（オプション）
        detailed_infos = None

        if extract_details and search_items:
            print("[2/5] 各URLから詳細情報を抽出中...")
            logger.info("Starting detail extraction")

            scraper = WebScraper()
            extractor = InfoExtractor()
            detailed_infos = []

            for i, item in enumerate(search_items, 1):
                print(f"  処理中: {i}/{len(search_items)} - {item.title[:50]}...")

                try:
                    # ページコンテンツの取得
                    page_content = scraper.fetch_page(item.url, respect_robots=True)

                    if page_content:
                        # 情報の抽出
                        detail = extractor.extract_all(page_content.html)
                        detailed_infos.append(detail)

                        # 抽出結果のサマリー表示
                        if detail.phone or detail.email:
                            print(f"    ✓ 電話: {len(detail.phone)}件, メール: {len(detail.email)}件")
                    else:
                        logger.warning(f"Failed to fetch page: {item.url}")
                        detailed_infos.append(None)

                except Exception as e:
                    logger.error(f"Error extracting details from {item.url}: {e}")
                    detailed_infos.append(None)

            print(f"✓ 詳細情報の抽出が完了しました")
            print()
        else:
            print("[2/5] 詳細情報の抽出をスキップしました")
            print()

        # 3. データの整形
        print("[3/5] データを整形中...")
        formatter = DataFormatter()
        output_data = formatter.format_data(search_items, detailed_infos)
        output_data = formatter.remove_duplicates(output_data)
        output_data = formatter.validate_data(output_data)

        print(f"✓ {len(output_data)}件のデータを整形しました")
        print()

        # 4. Excel出力
        print("[4/5] Excelファイルを生成中...")
        writer = ExcelWriter()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"tavily_search_{timestamp}.xlsx"

        output_path = writer.write(output_data, filename, apply_format=True)

        if output_path:
            print(f"✓ Excelファイルを保存しました!")
            print(f"   パス: {output_path}")
            print()
        else:
            print("✗ Excelファイルの保存に失敗しました")
            return False

        # 5. 完了
        print("[5/5] テスト完了！")
        print()
        print("=" * 60)
        print("テスト結果サマリー")
        print("=" * 60)
        print(f"検索キーワード: {keyword}")
        print(f"検索結果件数: {len(search_items)}件")
        print(f"出力データ件数: {len(output_data)}件")
        print(f"詳細情報抽出: {'実施' if extract_details else 'スキップ'}")
        print(f"出力ファイル: {output_path}")
        print("=" * 60)
        print()
        print("✅ すべての処理が正常に完了しました！")
        print()
        print("次のステップ:")
        print("  1. 出力されたExcelファイルを開いて確認してください")
        print("  2. main.pyで実際の運用を開始できます")
        print("     python3 main.py")
        print("=" * 60)

        return True

    except Exception as e:
        print()
        print(f"✗ エラー: {e}")
        logger.error(f"Test failed: {e}", exc_info=True)
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_full_flow()
    sys.exit(0 if success else 1)
