"""モックデータを使った動作確認"""

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from core.searcher import SearchItem
from core.extractor import InfoExtractor, DetailedInfo
from output.formatter import DataFormatter
from output.excel_writer import ExcelWriter

def test_with_mock_data():
    """モックデータで全体の動作を確認"""

    print("=" * 60)
    print("モックデータによる動作確認テスト")
    print("=" * 60)
    print()

    # モック検索結果を作成
    mock_search_items = [
        SearchItem(
            rank=1,
            title="東京歯科医院 | 新宿区の歯科クリニック",
            url="https://example-dental1.com",
            description="東京都新宿区にある歯科医院です。一般歯科、小児歯科、矯正歯科など幅広く対応しています。",
            snippet="東京都新宿区にある歯科医院です。"
        ),
        SearchItem(
            rank=2,
            title="スマイルデンタルクリニック - 渋谷の歯医者",
            url="https://example-dental2.com",
            description="渋谷駅から徒歩5分。最新設備で快適な治療を提供します。",
            snippet="渋谷駅から徒歩5分。"
        ),
        SearchItem(
            rank=3,
            title="品川歯科 - 品川区の歯科医院",
            url="https://example-dental3.com",
            description="品川区で30年の実績。地域密着型の歯科医院です。",
            snippet="品川区で30年の実績。"
        ),
    ]

    print(f"モック検索結果: {len(mock_search_items)}件")
    print()

    # モック詳細情報を作成
    mock_detailed_infos = [
        DetailedInfo(
            phone=["03-1234-5678", "0120-111-222"],
            email=["info@example-dental1.com"],
            address={"postal_code": "160-0022", "prefecture": "東京都"},
            fax=["03-1234-5679"],
            company_name="東京歯科医院",
            sns_links={
                "twitter": ["https://twitter.com/tokyo_dental"],
                "facebook": ["https://facebook.com/tokyodental"]
            }
        ),
        DetailedInfo(
            phone=["03-9876-5432"],
            email=["contact@example-dental2.com"],
            address={"postal_code": "150-0002", "prefecture": "東京都"},
            company_name="スマイルデンタルクリニック",
            sns_links={
                "instagram": ["https://instagram.com/smile_dental"]
            }
        ),
        DetailedInfo(
            phone=["03-5555-6666"],
            email=["inquiry@example-dental3.com"],
            address={"postal_code": "140-0001", "prefecture": "東京都"},
            fax=["03-5555-6667"],
            company_name="品川歯科"
        ),
    ]

    print(f"モック詳細情報: {len(mock_detailed_infos)}件")
    print()

    try:
        # 1. データの整形
        print("[1/3] データを整形中...")
        formatter = DataFormatter()
        output_data = formatter.format_data(mock_search_items, mock_detailed_infos)

        print(f"✓ {len(output_data)}件のデータを整形しました")
        print()

        # 整形データの表示
        print("--- 整形済みデータ（サンプル） ---")
        sample = output_data[0]
        print(f"順位: {sample.rank}")
        print(f"タイトル: {sample.title}")
        print(f"URL: {sample.url}")
        print(f"電話番号: {sample.phone}")
        print(f"メール: {sample.email}")
        print(f"郵便番号: {sample.postal_code}")
        print(f"都道府県: {sample.prefecture}")
        print(f"会社名: {sample.company_name}")
        print(f"Twitter: {sample.sns_twitter}")
        print()

        # 2. 重複除去とバリデーション
        print("[2/3] 重複除去とバリデーション中...")
        output_data = formatter.remove_duplicates(output_data)
        output_data = formatter.validate_data(output_data)

        print(f"✓ {len(output_data)}件のデータを検証しました")
        print()

        # 3. Excel出力
        print("[3/3] Excelファイルを生成中...")
        writer = ExcelWriter()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"test_mock_{timestamp}.xlsx"

        output_path = writer.write(output_data, filename, apply_format=True)

        if output_path:
            print(f"✓ Excelファイルを保存しました!")
            print(f"   パス: {output_path}")
            print()
        else:
            print("✗ Excelファイルの保存に失敗しました")
            return False

        # 完了
        print("=" * 60)
        print("✓ すべての処理が正常に完了しました！")
        print("=" * 60)
        print()
        print("テスト結果サマリー:")
        print(f"  - 検索結果件数: {len(mock_search_items)}件")
        print(f"  - 出力データ件数: {len(output_data)}件")
        print(f"  - 出力ファイル: {output_path}")
        print()
        print("次のステップ:")
        print("  1. 出力されたExcelファイルを確認してください")
        print("  2. データの形式とフォーマットが正しいか確認してください")
        print("  3. 実際のGoogle検索機能の実装を改善しましょう")
        print("=" * 60)

        return True

    except Exception as e:
        print(f"✗ エラー: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_with_mock_data()
    sys.exit(0 if success else 1)
