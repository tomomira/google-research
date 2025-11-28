"""Webページをスクレイピングするモジュール

このモジュールは、個別のWebページにアクセスしてHTMLを取得する機能を提供します。
robots.txtの遵守やリトライ機能を含みます。
"""

from dataclasses import dataclass
from typing import Optional
import time
import requests
from urllib.parse import urlparse, urljoin
from urllib.robotparser import RobotFileParser

from config.settings import Settings
from config.constants import ERROR_MESSAGES
from utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class PageContent:
    """ページコンテンツ"""
    url: str
    html: str
    status_code: int
    content_type: str
    encoding: str


class WebScraper:
    """Webページをスクレイピングするクラス

    個別のWebページにアクセスしてHTMLを取得します。
    robots.txtの遵守、User-Agent設定、リトライ機能を含みます。
    """

    def __init__(self):
        """初期化

        WebScraperインスタンスを初期化します。
        """
        self.timeout = Settings.REQUEST_TIMEOUT
        self.max_retries = Settings.MAX_RETRIES
        self.user_agent = Settings.USER_AGENT
        self.wait_time = Settings.DEFAULT_WAIT_TIME
        self.last_request_time = 0
        self.robots_parsers = {}  # ドメインごとのRobotFileParserをキャッシュ
        logger.info("WebScraper initialized")

    def fetch_page(self, url: str, respect_robots: bool = True) -> Optional[PageContent]:
        """ページコンテンツを取得

        指定されたURLのページコンテンツを取得します。

        Args:
            url: 取得するページのURL
            respect_robots: robots.txtを遵守するかどうか（デフォルト: True）

        Returns:
            ページコンテンツ。取得に失敗した場合はNone

        Raises:
            ValueError: URLが不正な場合
            RuntimeError: robots.txtでアクセスが禁止されている場合
        """
        if not url or not url.strip():
            logger.error("URL is empty")
            raise ValueError(ERROR_MESSAGES["invalid_url"])

        # URLの検証
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            logger.error(f"Invalid URL format: {url}")
            raise ValueError(ERROR_MESSAGES["invalid_url"])

        # robots.txtのチェック
        if respect_robots and not self.check_robots_txt(url):
            logger.warning(f"Access denied by robots.txt: {url}")
            raise RuntimeError(ERROR_MESSAGES["robots_denied"])

        logger.info(f"Fetching page: {url}")

        # レート制限の適用
        self._wait_for_rate_limit()

        # HTMLの取得
        html = self._fetch_html(url)

        if html is None:
            logger.error(f"Failed to fetch page: {url}")
            return None

        # PageContentの作成
        page_content = PageContent(
            url=url,
            html=html,
            status_code=200,
            content_type="text/html",
            encoding="utf-8"
        )

        logger.info(f"Successfully fetched page (length: {len(html)} chars)")
        return page_content

    def check_robots_txt(self, url: str) -> bool:
        """robots.txtをチェック

        指定されたURLへのアクセスがrobots.txtで許可されているかチェックします。

        Args:
            url: チェックするURL

        Returns:
            アクセスが許可されている場合True
        """
        try:
            parsed = urlparse(url)
            domain = f"{parsed.scheme}://{parsed.netloc}"

            # キャッシュからRobotFileParserを取得
            if domain not in self.robots_parsers:
                logger.debug(f"Loading robots.txt for domain: {domain}")
                rp = RobotFileParser()
                robots_url = urljoin(domain, "/robots.txt")
                rp.set_url(robots_url)

                try:
                    rp.read()
                    self.robots_parsers[domain] = rp
                    logger.debug(f"robots.txt loaded successfully: {domain}")
                except Exception as e:
                    logger.warning(f"Failed to load robots.txt for {domain}: {e}")
                    # robots.txtが取得できない場合はアクセスを許可
                    return True

            # アクセス可否の判定
            rp = self.robots_parsers[domain]
            can_fetch = rp.can_fetch(self.user_agent, url)

            if can_fetch:
                logger.debug(f"Access allowed by robots.txt: {url}")
            else:
                logger.warning(f"Access denied by robots.txt: {url}")

            return can_fetch

        except Exception as e:
            logger.error(f"Error checking robots.txt: {e}", exc_info=True)
            # エラー時はアクセスを許可
            return True

    def _fetch_html(self, url: str) -> Optional[str]:
        """HTMLを取得（リトライ機能付き）

        Args:
            url: 取得するURL

        Returns:
            取得したHTML。失敗した場合はNone
        """
        headers = {
            'User-Agent': self.user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'ja,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }

        for attempt in range(1, self.max_retries + 1):
            try:
                logger.debug(f"Fetching HTML (attempt {attempt}/{self.max_retries})")

                response = requests.get(
                    url,
                    headers=headers,
                    timeout=self.timeout,
                    allow_redirects=True
                )

                # ステータスコードのチェック
                if response.status_code == 200:
                    logger.debug(f"Successfully fetched HTML (status: {response.status_code})")
                    return response.text
                elif response.status_code == 404:
                    logger.warning(f"Page not found (404): {url}")
                    return None
                elif response.status_code == 403:
                    logger.warning(f"Access forbidden (403): {url}")
                    return None
                else:
                    logger.warning(f"Unexpected status code {response.status_code}: {url}")
                    response.raise_for_status()

            except requests.Timeout as e:
                logger.warning(f"Request timeout (attempt {attempt}/{self.max_retries}): {e}")

                if attempt == self.max_retries:
                    logger.error(f"Max retries exceeded due to timeout: {url}")
                    return None

            except requests.RequestException as e:
                logger.warning(f"Request failed (attempt {attempt}/{self.max_retries}): {e}")

                if attempt == self.max_retries:
                    logger.error(f"Max retries exceeded: {url}")
                    return None

            # 次のリトライ前に待機（指数バックオフ）
            if attempt < self.max_retries:
                wait_time = self.wait_time * (2 ** (attempt - 1))
                logger.debug(f"Waiting {wait_time} seconds before retry")
                time.sleep(wait_time)

        return None

    def _wait_for_rate_limit(self) -> None:
        """レート制限のための待機

        前回のリクエストから十分な時間が経過していない場合、待機します。
        """
        current_time = time.time()
        elapsed = current_time - self.last_request_time

        if elapsed < self.wait_time:
            wait_duration = self.wait_time - elapsed
            logger.debug(f"Rate limiting: waiting {wait_duration:.2f} seconds")
            time.sleep(wait_duration)

        self.last_request_time = time.time()

    def clear_robots_cache(self) -> None:
        """robots.txtのキャッシュをクリア"""
        logger.info("Clearing robots.txt cache")
        self.robots_parsers.clear()
