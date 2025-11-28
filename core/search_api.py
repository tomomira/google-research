"""検索API統合モジュール

TavilyとGoogle Custom Search APIの両方をサポートする統一インターフェース
"""

from typing import Optional
import requests
from dataclasses import dataclass

from config.settings import Settings
from config.constants import ERROR_MESSAGES
from core.searcher import SearchItem, SearchOptions
from utils.logger import get_logger

logger = get_logger(__name__)


class SearchAPIClient:
    """検索APIクライアント（Tavily/Google対応）"""

    def __init__(self, provider: Optional[str] = None):
        """初期化

        Args:
            provider: 使用するAPI（"tavily" or "google"）。Noneの場合は設定ファイルから取得
        """
        self.provider = provider or Settings.SEARCH_API_PROVIDER

        if self.provider == "tavily":
            self.api_key = Settings.TAVILY_API_KEY
            if not self.api_key:
                raise ValueError("TAVILY_API_KEYが設定されていません。.envファイルを確認してください。")
        elif self.provider == "google":
            self.api_key = Settings.GOOGLE_API_KEY
            self.cx_id = Settings.GOOGLE_CX_ID
            if not self.api_key or not self.cx_id:
                raise ValueError("GOOGLE_API_KEYまたはGOOGLE_CX_IDが設定されていません。")
        else:
            raise ValueError(f"不正なプロバイダー: {self.provider}")

        logger.info(f"SearchAPIClient initialized (provider={self.provider})")

    def search(self, keyword: str, options: Optional[SearchOptions] = None) -> list[SearchItem]:
        """検索を実行

        Args:
            keyword: 検索キーワード
            options: 検索オプション

        Returns:
            検索結果のリスト

        Raises:
            ValueError: キーワードが空の場合
            RuntimeError: API呼び出しに失敗した場合
        """
        if not keyword or not keyword.strip():
            logger.error("Search keyword is empty")
            raise ValueError(ERROR_MESSAGES["empty_keyword"])

        if options is None:
            options = SearchOptions()

        logger.info(f"Starting {self.provider} search for keyword: {keyword}")

        if self.provider == "tavily":
            return self._search_tavily(keyword, options)
        elif self.provider == "google":
            return self._search_google(keyword, options)

    def _search_tavily(self, keyword: str, options: SearchOptions) -> list[SearchItem]:
        """Tavily APIで検索

        Args:
            keyword: 検索キーワード
            options: 検索オプション

        Returns:
            検索結果のリスト
        """
        url = "https://api.tavily.com/search"

        payload = {
            "api_key": self.api_key,
            "query": keyword,
            "max_results": options.num_results,
            "search_depth": "basic",  # "basic" or "advanced"
            "include_answer": False,
            "include_raw_content": False,
            "include_domains": [],
            "exclude_domains": []
        }

        try:
            logger.debug(f"Calling Tavily API: {url}")
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()

            data = response.json()
            results = data.get("results", [])

            logger.info(f"Tavily API returned {len(results)} results")

            # SearchItemに変換
            search_items = []
            for rank, result in enumerate(results, start=1):
                search_item = SearchItem(
                    rank=rank,
                    title=result.get("title", ""),
                    url=result.get("url", ""),
                    description=result.get("content", ""),
                    snippet=result.get("content", "")[:200]  # 最初の200文字をスニペットに
                )
                search_items.append(search_item)

            return search_items

        except requests.exceptions.RequestException as e:
            logger.error(f"Tavily API request failed: {e}", exc_info=True)
            raise RuntimeError(f"Tavily API呼び出しに失敗しました: {e}")

    def _search_google(self, keyword: str, options: SearchOptions) -> list[SearchItem]:
        """Google Custom Search APIで検索

        Args:
            keyword: 検索キーワード
            options: 検索オプション

        Returns:
            検索結果のリスト
        """
        url = "https://www.googleapis.com/customsearch/v1"

        params = {
            "key": self.api_key,
            "cx": self.cx_id,
            "q": keyword,
            "num": min(options.num_results, 10),  # Google APIは最大10件
            "gl": options.region,
            "lr": f"lang_{options.language}"
        }

        try:
            logger.debug(f"Calling Google Custom Search API: {url}")
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()
            items = data.get("items", [])

            logger.info(f"Google API returned {len(items)} results")

            # SearchItemに変換
            search_items = []
            for rank, item in enumerate(items, start=1):
                search_item = SearchItem(
                    rank=rank,
                    title=item.get("title", ""),
                    url=item.get("link", ""),
                    description=item.get("snippet", ""),
                    snippet=item.get("snippet", "")
                )
                search_items.append(search_item)

            return search_items

        except requests.exceptions.RequestException as e:
            logger.error(f"Google API request failed: {e}", exc_info=True)
            raise RuntimeError(f"Google API呼び出しに失敗しました: {e}")
