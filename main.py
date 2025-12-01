"""Google検索リサーチツール - メインエントリーポイント

Phase 1 MVP版: CLI操作で検索→抽出→Excel出力を実行
Tavily API統合版
"""

import sys
from pathlib import Path
from datetime import datetime

# プロジェクトルートをPythonパスに追加
sys.path.insert(0, str(Path(__file__).parent))

from core.search_api import SearchAPIClient
from core.searcher import SearchOptions
from core.scraper import WebScraper
from core.extractor import InfoExtractor
from output.formatter import DataFormatter
from output.excel_writer import ExcelWriter
from utils.logger import get_logger
from config.settings import Settings
from config.constants import SUCCESS_MESSAGES, ERROR_MESSAGES

logger = get_logger(__name__)


def main():
    """メイン関数 - CLI版（Tavily API統合）"""
    logger.info("Google検索リサーチツールを起動しました")

    print("=" * 60)
    print("Google検索リサーチツール - Phase 1 MVP")
    print(f"検索API: {Settings.SEARCH_API_PROVIDER.upper()}")
    print("=" * 60)
    print()

    # キーワード入力
    keyword = input("検索キーワードを入力してください: ").strip()

    if not keyword:
        print(ERROR_MESSAGES["empty_keyword"])
        logger.error("No keyword provided")
        return

    # 検索件数の入力
    try:
        num_results_input = input("検索結果の取得件数を入力してください (デフォルト: 10): ").strip()
        num_results = int(num_results_input) if num_results_input else 10
    except ValueError:
        print("無効な数値です。デフォルト値(10件)を使用します。")
        num_results = 10

    # 詳細情報を取得するかの確認
    extract_details_input = input("詳細情報を取得しますか? (y/n, デフォルト: n): ").strip().lower()
    extract_details = extract_details_input == 'y'

    print()
    print("-" * 60)
    print(f"検索キーワード: {keyword}")
    print(f"取得件数: {num_results}件")
    print(f"詳細情報取得: {'はい' if extract_details else 'いいえ'}")
    print("-" * 60)
    print()

    try:
        # 1. Tavily/Google検索の実行
        print(f"[1/5] {Settings.SEARCH_API_PROVIDER.upper()} APIで検索を実行中...")
        logger.info(f"Starting search for keyword: {keyword}")

        # Tavily/Google APIクライアント
        search_client = SearchAPIClient()
        search_options = SearchOptions(num_results=num_results)
        search_items = search_client.search(keyword, search_options)

        print(f"✓ {len(search_items)}件の検索結果を取得しました")
        logger.info(f"Search completed: {len(search_items)} results found")

        # 2. 詳細情報の抽出（オプション）
        detailed_infos = None

        if extract_details and search_items:
            print()
            print("[2/5] 詳細情報を抽出中...")
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
                    else:
                        logger.warning(f"Failed to fetch page: {item.url}")
                        detailed_infos.append(None)

                except Exception as e:
                    logger.warning(f"Failed to fetch details from {item.url}: {e}")
                    print(f"  ⚠ スキップ: {item.url} (理由: {str(e)[:50]})")
                    detailed_infos.append(None)

            print(f"✓ 詳細情報の抽出が完了しました")
            logger.info("Detail extraction completed")
        else:
            print()
            print("[2/5] 詳細情報の抽出をスキップしました")

        # 3. データの整形
        print()
        print("[3/5] データを整形中...")
        logger.info("Formatting data")

        formatter = DataFormatter()
        output_data = formatter.format_data(search_items, detailed_infos)

        # 重複除去
        output_data = formatter.remove_duplicates(output_data)

        # バリデーション
        output_data = formatter.validate_data(output_data)

        print(f"✓ {len(output_data)}件のデータを整形しました")
        logger.info(f"Data formatted: {len(output_data)} items")

        # 4. Excel出力
        print()
        print("[4/5] Excelファイルを生成中...")
        logger.info("Writing to Excel")

        writer = ExcelWriter()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"search_results_{timestamp}.xlsx"

        output_path = writer.write(output_data, filename, apply_format=True)

        if output_path:
            print(f"✓ Excelファイルを保存しました: {output_path}")
            logger.info(f"Excel file saved: {output_path}")
        else:
            print("✗ Excelファイルの保存に失敗しました")
            logger.error("Failed to save Excel file")
            return

        # 5. 完了
        print()
        print("[5/5] 処理が完了しました！")
        print()
        print("=" * 60)
        print("処理結果サマリー")
        print("=" * 60)
        print(f"検索キーワード: {keyword}")
        print(f"検索結果件数: {len(search_items)}件")
        print(f"出力データ件数: {len(output_data)}件")
        print(f"出力ファイル: {output_path}")
        print("=" * 60)

        logger.info("Application completed successfully")

    except KeyboardInterrupt:
        print()
        print()
        print("処理を中断しました")
        logger.info("Process interrupted by user")

    except Exception as e:
        print()
        print(f"✗ エラーが発生しました: {e}")
        logger.error(f"Application error: {e}", exc_info=True)
        return


if __name__ == "__main__":
    main()
