"""Google検索リサーチツール - メインエントリーポイント"""
import sys
from pathlib import Path

# プロジェクトルートをPythonパスに追加
sys.path.insert(0, str(Path(__file__).parent))

from utils.logger import get_logger

logger = get_logger(__name__)


def main():
    """メイン関数"""
    logger.info("Google検索リサーチツールを起動しました")

    print("=" * 60)
    print("Google検索リサーチツール")
    print("=" * 60)
    print()
    print("現在、Phase 1の実装を準備中です。")
    print()
    print("プロジェクト構造:")
    print("  - 要件定義書: docs/requirements_specification.md")
    print("  - 実装計画書: docs/implementation_plan.md")
    print("  - 設定ファイル: config/settings.py")
    print()
    print("次のステップ: Phase 1のコア機能実装")
    print("=" * 60)

    logger.info("アプリケーションを正常終了しました")


if __name__ == "__main__":
    main()
