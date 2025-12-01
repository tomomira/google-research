"""formatterモジュールのテスト

このモジュールは、DataFormatterクラスの単体テストを提供します。
"""

import pytest
from output.formatter import DataFormatter, OutputData
from core.searcher import SearchItem
from core.extractor import DetailedInfo


@pytest.fixture
def formatter():
    """DataFormatterのフィクスチャ"""
    return DataFormatter()


@pytest.fixture
def sample_search_items():
    """テスト用SearchItemのフィクスチャ"""
    return [
        SearchItem(
            rank=1,
            title="テスト歯科医院1",
            url="https://example1.com",
            description="テスト用の歯科医院です",
            snippet="テスト用"
        ),
        SearchItem(
            rank=2,
            title="テスト歯科医院2",
            url="https://example2.com",
            description="もう一つのテスト用歯科医院",
            snippet="テスト用2"
        ),
    ]


@pytest.fixture
def sample_detailed_infos():
    """テスト用DetailedInfoのフィクスチャ"""
    return [
        DetailedInfo(
            phone=["03-1234-5678"],
            email=["info@example1.com"],
            address={"postal_code": "150-0001", "prefecture": "東京都"},
            company_name="テスト歯科医院1",
            business_hours="9:00-18:00",
            closed_days="水曜日"
        ),
        DetailedInfo(
            phone=["06-1234-5678"],
            email=["info@example2.com"],
            address={"postal_code": "530-0001", "prefecture": "大阪府"},
            company_name="テスト歯科医院2",
            business_hours="10:00-19:00",
            closed_days="日曜日"
        ),
    ]


class TestFormatData:
    """データ整形のテスト"""

    def test_format_data_basic(self, formatter, sample_search_items, sample_detailed_infos):
        """基本的なデータ整形"""
        output_data_list = formatter.format_data(sample_search_items, sample_detailed_infos)

        assert len(output_data_list) == 2
        assert all(isinstance(data, OutputData) for data in output_data_list)

    def test_format_data_without_details(self, formatter, sample_search_items):
        """詳細情報なしでのデータ整形"""
        output_data_list = formatter.format_data(sample_search_items, None)

        assert len(output_data_list) == 2
        # 詳細情報がない場合、基本情報のみが設定される
        assert output_data_list[0].phone == ""
        assert output_data_list[0].email == ""

    def test_format_data_with_details(self, formatter, sample_search_items, sample_detailed_infos):
        """詳細情報ありでのデータ整形"""
        output_data_list = formatter.format_data(sample_search_items, sample_detailed_infos)

        # 詳細情報が正しく統合されていることを確認
        assert output_data_list[0].phone == "03-1234-5678"
        assert output_data_list[0].email == "info@example1.com"
        assert output_data_list[0].company_name == "テスト歯科医院1"
        assert output_data_list[0].business_hours == "9:00-18:00"
        assert output_data_list[0].closed_days == "水曜日"


class TestRemoveDuplicates:
    """重複除去のテスト"""

    def test_remove_duplicates_no_duplicates(self, formatter):
        """重複なしの場合"""
        data_list = [
            OutputData(rank=1, title="Title1", url="https://example1.com", description="Desc1"),
            OutputData(rank=2, title="Title2", url="https://example2.com", description="Desc2"),
        ]

        unique_data = formatter.remove_duplicates(data_list)
        assert len(unique_data) == 2

    def test_remove_duplicates_with_duplicates(self, formatter):
        """重複ありの場合"""
        data_list = [
            OutputData(rank=1, title="Title1", url="https://example1.com", description="Desc1"),
            OutputData(rank=2, title="Title2", url="https://example2.com", description="Desc2"),
            OutputData(rank=3, title="Title1 (duplicate)", url="https://example1.com", description="Desc1"),
        ]

        unique_data = formatter.remove_duplicates(data_list)
        # 重複が除去され、2件になる
        assert len(unique_data) == 2
        # 最初の出現が保持される
        assert unique_data[0].title == "Title1"

    def test_remove_duplicates_empty_list(self, formatter):
        """空リストの場合"""
        unique_data = formatter.remove_duplicates([])
        assert unique_data == []


class TestValidateData:
    """データ検証のテスト"""

    def test_validate_data_valid(self, formatter):
        """有効なデータの検証"""
        data_list = [
            OutputData(rank=1, title="Title1", url="https://example1.com", description="Desc1"),
            OutputData(rank=2, title="Title2", url="https://example2.com", description="Desc2"),
        ]

        valid_data = formatter.validate_data(data_list)
        assert len(valid_data) == 2

    def test_validate_data_invalid_url(self, formatter):
        """無効なURL（http/httpsではない）のデータ"""
        data_list = [
            OutputData(rank=1, title="Title1", url="https://example1.com", description="Desc1"),
            OutputData(rank=2, title="Title2", url="ftp://example2.com", description="Desc2"),
        ]

        valid_data = formatter.validate_data(data_list)
        # 無効なURLのデータは除外される
        assert len(valid_data) == 1

    def test_validate_data_empty_url(self, formatter):
        """空URLのデータ"""
        data_list = [
            OutputData(rank=1, title="Title1", url="https://example1.com", description="Desc1"),
            OutputData(rank=2, title="Title2", url="", description="Desc2"),
        ]

        valid_data = formatter.validate_data(data_list)
        # 空URLのデータは除外される
        assert len(valid_data) == 1

    def test_validate_data_empty_title(self, formatter):
        """空タイトルのデータ"""
        data_list = [
            OutputData(rank=1, title="Title1", url="https://example1.com", description="Desc1"),
            OutputData(rank=2, title="", url="https://example2.com", description="Desc2"),
        ]

        valid_data = formatter.validate_data(data_list)
        # 空タイトルのデータは除外される
        assert len(valid_data) == 1


class TestToDataFrame:
    """DataFrame変換のテスト"""

    def test_to_dataframe_basic(self, formatter):
        """基本的なDataFrame変換"""
        data_list = [
            OutputData(rank=1, title="Title1", url="https://example1.com", description="Desc1"),
            OutputData(rank=2, title="Title2", url="https://example2.com", description="Desc2"),
        ]

        df = formatter.to_dataframe(data_list)
        assert len(df) == 2
        assert "rank" in df.columns
        assert "title" in df.columns
        assert "url" in df.columns

    def test_to_dataframe_empty(self, formatter):
        """空リストのDataFrame変換"""
        df = formatter.to_dataframe([])
        assert len(df) == 0


class TestOutputData:
    """OutputDataクラスのテスト"""

    def test_to_dict(self):
        """辞書変換のテスト"""
        data = OutputData(
            rank=1,
            title="Title1",
            url="https://example1.com",
            description="Desc1",
            phone="03-1234-5678",
            email="info@example.com"
        )

        data_dict = data.to_dict()
        assert isinstance(data_dict, dict)
        assert data_dict["rank"] == 1
        assert data_dict["title"] == "Title1"
        assert data_dict["phone"] == "03-1234-5678"
