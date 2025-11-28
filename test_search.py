"""簡単な検索テスト - 詳細情報抽出なし"""

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from core.searcher import GoogleSearcher, SearchOptions
from output.formatter import DataFormatter
from output.excel_writer import ExcelWriter
from utils.logger import get_logger

logger = get_logger(__name__)

def test_simple_search():
    """簡単な検索テスト（詳細情報抽出なし）"""

    print("=" * 60)
    print("簡単な検索テスト - 詳細情報抽出なし")
    print("=" * 60)
    print()

    # テストパラメータ
    keyword = "東京 歯科医院"
    num_results = 3  # テストなので少なめ

    print(f"検索キーワード: {keyword}")
    print(f"取得件数: {num_results}件")
    print(f"詳細情報取得: いいえ")
    print()
    print("-" * 60)
    print()

    try:
        # 1. Google検索の実行
        print("[1/4] Google検索を実行中...")
        searcher = GoogleSearcher()
        search_options = SearchOptions(num_results=num_results)
        search_items = searcher.search(keyword, search_options)

        print(f"✓ {len(search_items)}件の検索結果を取得しました")
        print()

        # 検索結果の表示
        print("--- 検索結果 ---")
        for item in search_items:
            print(f"{item.rank}. {item.title}")
            print(f"   URL: {item.url}")
            print(f"   説明: {item.description[:100]}...")
            print()

        # 2. データの整形
        print("[2/4] データを整形中...")
        formatter = DataFormatter()
        output_data = formatter.format_data(search_items, detailed_infos=None)
        output_data = formatter.remove_duplicates(output_data)
        output_data = formatter.validate_data(output_data)

        print(f"✓ {len(output_data)}件のデータを整形しました")
        print()

        # 3. Excel出力
        print("[3/4] Excelファイルを生成中...")
        writer = ExcelWriter()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"test_search_{timestamp}.xlsx"

        output_path = writer.write(output_data, filename, apply_format=True)

        if output_path:
            print(f"✓ Excelファイルを保存しました: {output_path}")
        else:
            print("✗ Excelファイルの保存に失敗しました")
            return False

        # 4. 完了
        print()
        print("[4/4] テスト完了！")
        print()
        print("=" * 60)
        print("テスト結果サマリー")
        print("=" * 60)
        print(f"検索キーワード: {keyword}")
        print(f"検索結果件数: {len(search_items)}件")
        print(f"出力データ件数: {len(output_data)}件")
        print(f"出力ファイル: {output_path}")
        print("=" * 60)

        return True

    except Exception as e:
        print()
        print(f"✗ エラーが発生しました: {e}")
        logger.error(f"Test failed: {e}", exc_info=True)
        return False


if __name__ == "__main__":
    success = test_simple_search()
    sys.exit(0 if success else 1)
