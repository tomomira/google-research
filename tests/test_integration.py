"""統合テスト

このモジュールは、複数のモジュール間の連携をテストします。
"""

import pytest
from pathlib import Path
from core.search_api import SearchAPIClient
from core.extractor import InfoExtractor
from output.formatter import DataFormatter
from output.excel_writer import ExcelWriter


@pytest.fixture
def search_client():
    """SearchAPIClientのフィクスチャ"""
    return SearchAPIClient()


@pytest.fixture
def extractor():
    """InfoExtractorのフィクスチャ"""
    return InfoExtractor()


@pytest.fixture
def formatter():
    """DataFormatterのフィクスチャ"""
    return DataFormatter()


@pytest.fixture
def excel_writer():
    """ExcelWriterのフィクスチャ"""
    return ExcelWriter()


class TestSearchToFormat:
    """検索→整形の統合テスト"""

    @pytest.mark.skip(reason="Tavily API呼び出しが必要なため、手動テストのみ")
    def test_search_and_format(self, search_client, formatter):
        """検索結果を整形するフロー"""
        # 検索実行
        search_items = search_client.search("東京 歯科医院", num_results=3)

        # データ整形
        output_data = formatter.format_data(search_items, None)

        # 検証
        assert len(output_data) > 0
        assert all(hasattr(data, "title") for data in output_data)
        assert all(hasattr(data, "url") for data in output_data)


class TestFormatToExcel:
    """整形→Excel出力の統合テスト"""

    def test_format_and_export(self, formatter, excel_writer, tmp_path):
        """整形したデータをExcelに出力するフロー"""
        from output.formatter import OutputData

        # テストデータの作成
        output_data = [
            OutputData(
                rank=1,
                title="テスト歯科医院1",
                url="https://example1.com",
                description="テスト用の歯科医院",
                phone="03-1234-5678",
                email="info@example1.com",
                company_name="テスト歯科医院1"
            ),
            OutputData(
                rank=2,
                title="テスト歯科医院2",
                url="https://example2.com",
                description="もう一つのテスト用歯科医院",
                phone="06-1234-5678",
                email="info@example2.com",
                company_name="テスト歯科医院2"
            ),
        ]

        # 重複除去とバリデーション
        output_data = formatter.remove_duplicates(output_data)
        output_data = formatter.validate_data(output_data)

        # Excel出力（一時ディレクトリに出力）
        test_filename = "test_output.xlsx"
        excel_writer.output_dir = tmp_path
        output_path = excel_writer.write(output_data, test_filename)

        # 検証
        assert output_path is not None
        assert output_path.exists()
        assert output_path.suffix == ".xlsx"


class TestFullFlow:
    """完全なフローの統合テスト"""

    @pytest.mark.skip(reason="Tavily API呼び出しが必要なため、手動テストのみ")
    def test_full_flow_without_details(
        self, search_client, formatter, excel_writer, tmp_path
    ):
        """検索→整形→Excel出力の完全なフロー（詳細情報なし）"""
        # 1. 検索実行
        search_items = search_client.search("東京 歯科医院", num_results=3)
        assert len(search_items) > 0

        # 2. データ整形
        output_data = formatter.format_data(search_items, None)
        output_data = formatter.remove_duplicates(output_data)
        output_data = formatter.validate_data(output_data)
        assert len(output_data) > 0

        # 3. Excel出力
        excel_writer.output_dir = tmp_path
        output_path = excel_writer.write(output_data, "test_full_flow.xlsx")
        assert output_path is not None
        assert output_path.exists()


class TestDataPipeline:
    """データパイプラインのテスト"""

    def test_data_pipeline_validation(self, formatter):
        """データパイプライン全体のバリデーション"""
        from output.formatter import OutputData

        # 不正なデータを含むリストを作成
        data_list = [
            OutputData(rank=1, title="Valid", url="https://example1.com", description="Valid"),
            OutputData(rank=2, title="", url="https://example2.com", description="Empty title"),
            OutputData(rank=3, title="Invalid URL", url="", description="Empty URL"),
            OutputData(rank=4, title="Valid", url="https://example1.com", description="Duplicate"),
        ]

        # パイプライン処理
        data_list = formatter.remove_duplicates(data_list)  # 重複除去
        data_list = formatter.validate_data(data_list)      # バリデーション

        # 検証: 有効なデータのみが残る（重複・空タイトル・空URLは除外）
        assert len(data_list) == 1
        assert data_list[0].title == "Valid"
        assert data_list[0].url == "https://example1.com"


class TestErrorHandling:
    """エラーハンドリングのテスト"""

    def test_empty_search_results(self, formatter):
        """空の検索結果の処理"""
        output_data = formatter.format_data([], None)
        assert output_data == []

    def test_excel_write_empty_data(self, excel_writer):
        """空のデータでExcel出力を試みる"""
        with pytest.raises(ValueError):
            excel_writer.write([], "test_empty.xlsx")

    def test_invalid_data_filtering(self, formatter):
        """無効なデータのフィルタリング"""
        from output.formatter import OutputData

        invalid_data = [
            OutputData(rank=1, title="", url="", description=""),  # すべて空
            OutputData(rank=2, title="Title", url="invalid-url", description="Invalid"),  # 無効URL
        ]

        valid_data = formatter.validate_data(invalid_data)
        # すべて無効なので、結果は空
        assert len(valid_data) == 0
