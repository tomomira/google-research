"""ログ出力モジュール"""
import logging
from pathlib import Path
from typing import Optional
from config.settings import Settings


class AppLogger:
    """アプリケーションログを管理するクラス"""

    _loggers = {}

    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        """ロガーを取得

        Args:
            name: ロガー名（通常は__name__を指定）

        Returns:
            ロガーインスタンス
        """
        if name in cls._loggers:
            return cls._loggers[name]

        logger = logging.getLogger(name)
        logger.setLevel(Settings.LOG_LEVEL)

        # すでにハンドラが設定されている場合はスキップ
        if logger.handlers:
            cls._loggers[name] = logger
            return logger

        # フォーマッタの設定
        formatter = logging.Formatter(Settings.LOG_FORMAT)

        # コンソールハンドラ
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # ファイルハンドラ
        file_handler = logging.FileHandler(
            Settings.LOG_FILE, encoding="utf-8"
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        cls._loggers[name] = logger
        return logger


def get_logger(name: str) -> logging.Logger:
    """ロガーを取得する便利関数

    Args:
        name: ロガー名

    Returns:
        ロガーインスタンス
    """
    return AppLogger.get_logger(name)
