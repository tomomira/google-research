"""データを整形するモジュール

このモジュールは、抽出されたデータの整形、重複除去、
バリデーションを行う機能を提供します。
"""

from dataclasses import dataclass, asdict
from typing import Optional
import pandas as pd

from core.searcher import SearchItem
from core.extractor import DetailedInfo
from utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class OutputData:
    """出力用データ

    検索結果と詳細情報を統合したデータ構造。
    """
    rank: int
    title: str
    url: str
    description: str
    phone: str = ""
    email: str = ""
    postal_code: str = ""
    prefecture: str = ""
    fax: str = ""
    company_name: str = ""
    sns_twitter: str = ""
    sns_facebook: str = ""
    sns_instagram: str = ""

    def to_dict(self) -> dict:
        """辞書形式に変換

        Returns:
            データの辞書表現
        """
        return asdict(self)


class DataFormatter:
    """データフォーマットクラス

    検索結果と詳細情報を統合し、整形・重複除去を行います。
    """

    def __init__(self):
        """初期化

        DataFormatterインスタンスを初期化します。
        """
        logger.info("DataFormatter initialized")

    def format_data(
        self,
        search_items: list[SearchItem],
        detailed_infos: Optional[list[Optional[DetailedInfo]]] = None
    ) -> list[OutputData]:
        """データを整形

        検索結果と詳細情報を統合して、出力用データを作成します。

        Args:
            search_items: 検索結果のリスト
            detailed_infos: 詳細情報のリスト（Noneの場合は詳細情報なし）

        Returns:
            整形された出力データのリスト
        """
        logger.info(f"Formatting {len(search_items)} search items")

        output_data_list = []

        for i, search_item in enumerate(search_items):
            # 詳細情報の取得
            detailed_info = None
            if detailed_infos and i < len(detailed_infos):
                detailed_info = detailed_infos[i]

            # OutputDataの作成
            output_data = self._create_output_data(search_item, detailed_info)
            output_data_list.append(output_data)

        logger.info(f"Formatted {len(output_data_list)} output data items")
        return output_data_list

    def remove_duplicates(self, data_list: list[OutputData]) -> list[OutputData]:
        """重複を除去

        URLをキーとして重複データを除去します。

        Args:
            data_list: 出力データのリスト

        Returns:
            重複を除去したデータのリスト
        """
        logger.info(f"Removing duplicates from {len(data_list)} items")

        if not data_list:
            return []

        # DataFrameに変換
        df = pd.DataFrame([data.to_dict() for data in data_list])

        # URLで重複除去（最初の出現を保持）
        df_unique = df.drop_duplicates(subset=['url'], keep='first')

        # 元のランク順にソート
        df_unique = df_unique.sort_values('rank')

        # 辞書のリストに戻す
        unique_dicts = df_unique.to_dict('records')

        # OutputDataのリストに変換
        unique_data = [
            OutputData(**item) for item in unique_dicts
        ]

        logger.info(f"Removed {len(data_list) - len(unique_data)} duplicate items")
        return unique_data

    def validate_data(self, data_list: list[OutputData]) -> list[OutputData]:
        """データを検証

        不正なデータを除外します。

        Args:
            data_list: 出力データのリスト

        Returns:
            検証済みのデータのリスト
        """
        logger.info(f"Validating {len(data_list)} items")

        valid_data = []

        for data in data_list:
            if self._is_valid_data(data):
                valid_data.append(data)
            else:
                logger.warning(f"Invalid data detected (rank={data.rank}, url={data.url})")

        logger.info(f"Validated: {len(valid_data)} valid, {len(data_list) - len(valid_data)} invalid")
        return valid_data

    def to_dataframe(self, data_list: list[OutputData]) -> pd.DataFrame:
        """DataFrameに変換

        Args:
            data_list: 出力データのリスト

        Returns:
            pandas DataFrame
        """
        if not data_list:
            logger.warning("Data list is empty")
            return pd.DataFrame()

        df = pd.DataFrame([data.to_dict() for data in data_list])
        logger.debug(f"Converted to DataFrame: shape={df.shape}")
        return df

    def _create_output_data(
        self,
        search_item: SearchItem,
        detailed_info: Optional[DetailedInfo]
    ) -> OutputData:
        """OutputDataを作成

        Args:
            search_item: 検索結果
            detailed_info: 詳細情報（Noneの場合もあり）

        Returns:
            出力用データ
        """
        # 基本情報
        output_data = OutputData(
            rank=search_item.rank,
            title=search_item.title,
            url=search_item.url,
            description=search_item.description
        )

        # 詳細情報の追加
        if detailed_info:
            # 電話番号（カンマ区切りで結合）
            if detailed_info.phone:
                output_data.phone = ", ".join(detailed_info.phone)

            # メールアドレス（カンマ区切りで結合）
            if detailed_info.email:
                output_data.email = ", ".join(detailed_info.email)

            # FAX番号（カンマ区切りで結合）
            if detailed_info.fax:
                output_data.fax = ", ".join(detailed_info.fax)

            # 住所情報
            if detailed_info.address:
                output_data.postal_code = detailed_info.address.get("postal_code") or ""
                output_data.prefecture = detailed_info.address.get("prefecture") or ""

            # 会社名
            if detailed_info.company_name:
                output_data.company_name = detailed_info.company_name

            # SNSリンク
            if detailed_info.sns_links:
                if "twitter" in detailed_info.sns_links:
                    output_data.sns_twitter = ", ".join(detailed_info.sns_links["twitter"])
                if "facebook" in detailed_info.sns_links:
                    output_data.sns_facebook = ", ".join(detailed_info.sns_links["facebook"])
                if "instagram" in detailed_info.sns_links:
                    output_data.sns_instagram = ", ".join(detailed_info.sns_links["instagram"])

        return output_data

    def _is_valid_data(self, data: OutputData) -> bool:
        """データの妥当性を検証

        Args:
            data: 出力データ

        Returns:
            妥当なデータの場合True
        """
        # 必須項目のチェック
        if not data.url or not data.url.strip():
            logger.debug("Invalid: URL is empty")
            return False

        if not data.title or not data.title.strip():
            logger.debug("Invalid: Title is empty")
            return False

        # URLの基本的な形式チェック
        if not data.url.startswith(('http://', 'https://')):
            logger.debug(f"Invalid: URL format is invalid ({data.url})")
            return False

        return True
