"""Google検索を実行するモジュール

このモジュールは、Google検索を実行し、検索結果を取得する機能を提供します。
"""

from dataclasses import dataclass, field
from typing import Optional
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus, urljoin

from config.settings import Settings
from config.constants import GOOGLE_SEARCH_URL, ERROR_MESSAGES
from utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class SearchOptions:
    """検索オプション"""
    num_results: int = 10
    region: str = "jp"
    language: str = "ja"
    period: Optional[str] = None
    site: Optional[str] = None
    exclude_keywords: list[str] = field(default_factory=list)


@dataclass
class SearchItem:
    """検索結果の1件"""
    rank: int
    title: str
    url: str
    description: str
    snippet: str


class GoogleSearcher:
    """Google検索を実行するクラス

    Google検索を実行し、検索結果を取得する機能を提供します。
    アクセス間隔の制御やCAPTCHA検出などの機能を含みます。
    """

    def __init__(self):
        """初期化

        GoogleSearcherインスタンスを初期化します。
        """
        self.wait_time = Settings.DEFAULT_WAIT_TIME
        self.timeout = Settings.REQUEST_TIMEOUT
        self.max_retries = Settings.MAX_RETRIES
        self.user_agent = Settings.USER_AGENT
        self.last_request_time = 0
        logger.info("GoogleSearcher initialized")

    def search(self, keyword: str, options: Optional[SearchOptions] = None) -> list[SearchItem]:
        """検索を実行

        指定されたキーワードでGoogle検索を実行し、結果を取得します。

        Args:
            keyword: 検索キーワード
            options: 検索オプション。Noneの場合はデフォルトを使用

        Returns:
            検索結果のリスト

        Raises:
            ValueError: キーワードが空の場合
            requests.RequestException: リクエスト失敗時
        """
        if not keyword or not keyword.strip():
            logger.error("Search keyword is empty")
            raise ValueError(ERROR_MESSAGES["empty_keyword"])

        if options is None:
            options = SearchOptions()

        logger.info(f"Starting search for keyword: {keyword}")
        logger.info(f"Search options: num_results={options.num_results}, "
                   f"region={options.region}, language={options.language}")

        # レート制限の適用
        self._wait_for_rate_limit()

        # 検索URL構築
        search_url = self.build_search_url(keyword, options)
        logger.debug(f"Search URL: {search_url}")

        # 検索結果取得
        html = self._fetch_search_results(search_url)

        # CAPTCHA検出
        if self._detect_captcha(html):
            logger.error("CAPTCHA detected. Stopping search.")
            raise RuntimeError(ERROR_MESSAGES["captcha_detected"])

        # 検索結果のパース
        search_items = self.parse_search_results(html, options.num_results)

        logger.info(f"Search completed. Found {len(search_items)} results")
        return search_items

    def build_search_url(self, keyword: str, options: SearchOptions) -> str:
        """検索URLを構築

        検索キーワードとオプションから、Google検索のURLを構築します。

        Args:
            keyword: 検索キーワード
            options: 検索オプション

        Returns:
            構築された検索URL
        """
        # キーワードのエンコード
        encoded_keyword = quote_plus(keyword)

        # 除外キーワードの追加
        for exclude in options.exclude_keywords:
            encoded_keyword += f" -{quote_plus(exclude)}"

        # サイト指定
        if options.site:
            encoded_keyword += f" site:{quote_plus(options.site)}"

        # URLパラメータ構築
        params = [
            f"q={encoded_keyword}",
            f"num={options.num_results}",
            f"hl={options.language}",
            f"gl={options.region}",
        ]

        # 期間指定
        if options.period:
            params.append(f"tbs=qdr:{options.period}")

        url = f"{GOOGLE_SEARCH_URL}?{'&'.join(params)}"
        return url

    def parse_search_results(self, html: str, max_results: int) -> list[SearchItem]:
        """検索結果HTMLをパース

        Google検索結果のHTMLから、タイトル、URL、説明文を抽出します。

        Args:
            html: 検索結果のHTML
            max_results: 取得する最大結果数

        Returns:
            抽出された検索結果のリスト
        """
        soup = BeautifulSoup(html, 'lxml')
        search_items = []

        # Google検索結果のdiv要素を取得
        # NOTE: Googleの構造は変更される可能性があるため、複数のセレクタを試行
        result_divs = soup.select('div.g') or soup.select('div[data-sokoban-container]')

        logger.debug(f"Found {len(result_divs)} result elements")

        for rank, div in enumerate(result_divs[:max_results], start=1):
            try:
                # タイトルとURLの取得
                title_elem = div.select_one('h3')
                link_elem = div.select_one('a')

                if not title_elem or not link_elem:
                    logger.debug(f"Skipping result {rank}: missing title or link")
                    continue

                title = title_elem.get_text(strip=True)
                url = link_elem.get('href', '')

                # URLの正規化
                if url.startswith('/url?q='):
                    # Googleのリダイレクトを除去
                    url = url.split('/url?q=')[1].split('&')[0]

                # 説明文の取得
                desc_elem = div.select_one('div[data-sncf]') or div.select_one('div.VwiC3b')
                description = desc_elem.get_text(strip=True) if desc_elem else ""

                # スニペット（要約）の取得
                snippet = description[:200] if description else title

                search_item = SearchItem(
                    rank=rank,
                    title=title,
                    url=url,
                    description=description,
                    snippet=snippet
                )

                search_items.append(search_item)
                logger.debug(f"Parsed result {rank}: {title}")

            except Exception as e:
                logger.warning(f"Failed to parse result {rank}: {e}")
                continue

        return search_items

    def _fetch_search_results(self, url: str) -> str:
        """検索結果を取得（リトライ機能付き）

        Args:
            url: 検索URL

        Returns:
            取得したHTML

        Raises:
            requests.RequestException: リトライ回数を超えた場合
        """
        headers = {
            'User-Agent': self.user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'ja,en;q=0.9',
        }

        for attempt in range(1, self.max_retries + 1):
            try:
                logger.debug(f"Fetching search results (attempt {attempt}/{self.max_retries})")
                response = requests.get(
                    url,
                    headers=headers,
                    timeout=self.timeout
                )
                response.raise_for_status()

                logger.debug(f"Successfully fetched search results (status: {response.status_code})")
                return response.text

            except requests.RequestException as e:
                logger.warning(f"Request failed (attempt {attempt}/{self.max_retries}): {e}")

                if attempt == self.max_retries:
                    logger.error(f"Max retries exceeded for URL: {url}")
                    raise

                # 次のリトライ前に待機
                time.sleep(self.wait_time * attempt)

        # このコードには到達しないが、型チェッカー対策
        raise RuntimeError("Unexpected error in _fetch_search_results")

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

    def _detect_captcha(self, html: str) -> bool:
        """CAPTCHA検出

        検索結果のHTMLにCAPTCHAが含まれているかチェックします。

        Args:
            html: 検索結果のHTML

        Returns:
            CAPTCHAが検出された場合True
        """
        captcha_indicators = [
            'g-recaptcha',
            'captcha',
            'robot check',
            'unusual traffic',
        ]

        html_lower = html.lower()
        for indicator in captcha_indicators:
            if indicator in html_lower:
                logger.warning(f"CAPTCHA indicator detected: {indicator}")
                return True

        return False
