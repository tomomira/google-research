"""アプリケーション設定モジュール"""
import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# .envファイルを読み込み
load_dotenv()


class Settings:
    """アプリケーション設定を管理するクラス"""

    # プロジェクトルートディレクトリ
    BASE_DIR = Path(__file__).parent.parent

    # ディレクトリ設定
    CONFIG_DIR = BASE_DIR / "config"
    LOGS_DIR = BASE_DIR / "logs"
    OUTPUT_DIR = BASE_DIR / "output"
    PRESETS_DIR = CONFIG_DIR / "presets"

    # 検索API設定
    SEARCH_API_PROVIDER = os.getenv("SEARCH_API_PROVIDER", "tavily")  # "tavily" or "google"
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
    GOOGLE_CX_ID = os.getenv("GOOGLE_CX_ID", "")

    # 検索設定のデフォルト値
    DEFAULT_NUM_RESULTS = 10
    DEFAULT_REGION = "jp"
    DEFAULT_LANGUAGE = "ja"
    DEFAULT_WAIT_TIME = 3  # 秒

    # スクレイピング設定
    REQUEST_TIMEOUT = 30  # 秒
    MAX_RETRIES = 3
    USER_AGENT = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )

    # Selenium設定
    HEADLESS_MODE = True
    PAGE_LOAD_TIMEOUT = 30  # 秒
    IMPLICIT_WAIT = 10  # 秒

    # Excel出力設定
    DEFAULT_OUTPUT_FILENAME = "research_results.xlsx"
    AUTO_COLUMN_WIDTH = True

    # ログ設定
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FILE = LOGS_DIR / "app.log"

    # 抽出設定
    EXTRACT_PHONE = True
    EXTRACT_EMAIL = True
    EXTRACT_ADDRESS = True

    @classmethod
    def ensure_directories(cls):
        """必要なディレクトリを作成"""
        cls.LOGS_DIR.mkdir(exist_ok=True)
        cls.OUTPUT_DIR.mkdir(exist_ok=True)
        cls.PRESETS_DIR.mkdir(exist_ok=True)

    @classmethod
    def get_output_path(cls, filename: Optional[str] = None) -> Path:
        """出力ファイルのパスを取得

        Args:
            filename: ファイル名（Noneの場合はデフォルト）

        Returns:
            出力ファイルの完全パス
        """
        if filename is None:
            filename = cls.DEFAULT_OUTPUT_FILENAME
        return cls.OUTPUT_DIR / filename


# アプリケーション起動時にディレクトリを作成
Settings.ensure_directories()
