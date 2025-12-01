"""GUI版メインエントリーポイント

このスクリプトは、GUIアプリケーションを起動します。
"""

import sys
from pathlib import Path

# プロジェクトのルートディレクトリをパスに追加
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from gui.main_window import MainWindow
from utils.logger import get_logger

logger = get_logger(__name__)


def main():
    """メイン関数

    GUIアプリケーションを起動します。
    """
    logger.info("=" * 60)
    logger.info("Google検索リサーチツール - Phase 3 GUI版")
    logger.info("=" * 60)

    try:
        # メインウィンドウの作成と起動
        app = MainWindow()
        app.run()

    except KeyboardInterrupt:
        logger.info("アプリケーションが中断されました")
        sys.exit(0)

    except Exception as e:
        logger.error(f"予期しないエラーが発生しました: {e}", exc_info=True)
        sys.exit(1)

    finally:
        logger.info("アプリケーションを終了しました")


if __name__ == "__main__":
    main()
