"""Seleniumブラウザを制御するモジュール

このモジュールは、Selenium WebDriverを使用してブラウザを制御し、
JavaScriptで動的に生成されるコンテンツの取得を可能にします。
"""

from typing import Optional
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

from config.settings import Settings
from config.constants import ERROR_MESSAGES
from utils.logger import get_logger

logger = get_logger(__name__)


class BrowserController:
    """Seleniumブラウザを制御するクラス

    Selenium WebDriverを使用してChromeブラウザを制御し、
    JavaScriptで動的に生成されるコンテンツの取得を行います。
    """

    def __init__(self, headless: bool = True):
        """初期化

        Args:
            headless: ヘッドレスモードで起動するかどうか（デフォルト: True）
        """
        self.headless = headless
        self.driver: Optional[webdriver.Chrome] = None
        self.timeout = Settings.REQUEST_TIMEOUT
        self.wait_time = Settings.DEFAULT_WAIT_TIME
        logger.info(f"BrowserController initialized (headless={headless})")

    def start_browser(self) -> None:
        """ブラウザを起動

        Chrome WebDriverを起動し、必要な設定を適用します。

        Raises:
            WebDriverException: ブラウザの起動に失敗した場合
        """
        if self.driver is not None:
            logger.warning("Browser is already running")
            return

        try:
            logger.info("Starting Chrome browser")

            # Chromeオプションの設定
            chrome_options = Options()

            if self.headless:
                chrome_options.add_argument('--headless')
                chrome_options.add_argument('--disable-gpu')

            # 一般的なオプション
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_argument(f'user-agent={Settings.USER_AGENT}')
            chrome_options.add_argument('--window-size=1920,1080')

            # 検出回避のための設定
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)

            # ChromeDriverの自動インストールと起動
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)

            # WebDriver検出の無効化
            self.driver.execute_script(
                "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
            )

            logger.info("Browser started successfully")

        except WebDriverException as e:
            logger.error(f"Failed to start browser: {e}", exc_info=True)
            raise RuntimeError(ERROR_MESSAGES["browser_start_failed"]) from e

    def stop_browser(self) -> None:
        """ブラウザを終了

        実行中のChromeブラウザを終了します。
        """
        if self.driver is None:
            logger.warning("Browser is not running")
            return

        try:
            logger.info("Stopping browser")
            self.driver.quit()
            self.driver = None
            logger.info("Browser stopped successfully")

        except Exception as e:
            logger.error(f"Error while stopping browser: {e}", exc_info=True)
            self.driver = None

    def get_page(self, url: str, wait_for_element: Optional[str] = None) -> str:
        """ページを取得（JavaScriptレンダリング含む）

        指定されたURLのページを取得します。
        JavaScriptで動的に生成されるコンテンツも取得可能です。

        Args:
            url: 取得するページのURL
            wait_for_element: 待機する要素のCSSセレクタ（オプション）

        Returns:
            ページのHTMLソース

        Raises:
            RuntimeError: ブラウザが起動していない場合
            TimeoutException: ページの読み込みがタイムアウトした場合
        """
        if self.driver is None:
            logger.error("Browser is not running")
            raise RuntimeError(ERROR_MESSAGES["browser_not_running"])

        try:
            logger.info(f"Getting page: {url}")

            # ページを開く
            self.driver.get(url)

            # 特定の要素を待機
            if wait_for_element:
                logger.debug(f"Waiting for element: {wait_for_element}")
                WebDriverWait(self.driver, self.timeout).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, wait_for_element))
                )
            else:
                # デフォルトでbody要素の読み込みを待機
                WebDriverWait(self.driver, self.timeout).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )

            # レート制限のための待機
            time.sleep(self.wait_time)

            # HTMLソースを取得
            html = self.driver.page_source
            logger.info(f"Successfully retrieved page (length: {len(html)} chars)")

            return html

        except TimeoutException as e:
            logger.error(f"Timeout while loading page: {url}", exc_info=True)
            raise TimeoutException(ERROR_MESSAGES["page_load_timeout"]) from e

        except Exception as e:
            logger.error(f"Error while getting page: {e}", exc_info=True)
            raise

    def execute_script(self, script: str) -> any:
        """JavaScriptを実行

        Args:
            script: 実行するJavaScriptコード

        Returns:
            スクリプトの実行結果

        Raises:
            RuntimeError: ブラウザが起動していない場合
        """
        if self.driver is None:
            logger.error("Browser is not running")
            raise RuntimeError(ERROR_MESSAGES["browser_not_running"])

        try:
            logger.debug(f"Executing JavaScript: {script[:50]}...")
            result = self.driver.execute_script(script)
            return result

        except Exception as e:
            logger.error(f"Error while executing script: {e}", exc_info=True)
            raise

    def get_current_url(self) -> str:
        """現在のURLを取得

        Returns:
            現在のURL

        Raises:
            RuntimeError: ブラウザが起動していない場合
        """
        if self.driver is None:
            logger.error("Browser is not running")
            raise RuntimeError(ERROR_MESSAGES["browser_not_running"])

        return self.driver.current_url

    def take_screenshot(self, filepath: str) -> bool:
        """スクリーンショットを撮影

        Args:
            filepath: 保存先のファイルパス

        Returns:
            成功した場合True

        Raises:
            RuntimeError: ブラウザが起動していない場合
        """
        if self.driver is None:
            logger.error("Browser is not running")
            raise RuntimeError(ERROR_MESSAGES["browser_not_running"])

        try:
            logger.info(f"Taking screenshot: {filepath}")
            result = self.driver.save_screenshot(filepath)
            if result:
                logger.info("Screenshot saved successfully")
            return result

        except Exception as e:
            logger.error(f"Error while taking screenshot: {e}", exc_info=True)
            return False

    def __enter__(self):
        """コンテキストマネージャー: enter"""
        self.start_browser()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """コンテキストマネージャー: exit"""
        self.stop_browser()
        return False
