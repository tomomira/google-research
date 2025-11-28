"""基本的な動作テスト"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from core.searcher import GoogleSearcher, SearchOptions
from core.extractor import InfoExtractor
from output.formatter import DataFormatter
from output.excel_writer import ExcelWriter

def test_basic_functionality():
    """基本機能のテスト"""
    print("=" * 60)
    print("基本機能テスト")
    print("=" * 60)
    print()

    # 1. GoogleSearcherのテスト
    print("[1/4] GoogleSearcherの初期化...")
    try:
        searcher = GoogleSearcher()
        print("✓ GoogleSearcher initialized successfully")
    except Exception as e:
        print(f"✗ GoogleSearcher initialization failed: {e}")
        return False

    # 2. InfoExtractorのテスト
    print("[2/4] InfoExtractorの初期化...")
    try:
        extractor = InfoExtractor()

        # 簡単な抽出テスト
        test_html = """
        <html>
        <body>
        <p>電話番号: 03-1234-5678</p>
        <p>メール: test@example.com</p>
        <p>住所: 東京都渋谷区</p>
        </body>
        </html>
        """

        phones = extractor.extract_phone(test_html)
        emails = extractor.extract_email(test_html)

        print(f"✓ InfoExtractor initialized successfully")
        print(f"  - 電話番号抽出: {phones}")
        print(f"  - メール抽出: {emails}")
    except Exception as e:
        print(f"✗ InfoExtractor test failed: {e}")
        return False

    # 3. DataFormatterのテスト
    print("[3/4] DataFormatterの初期化...")
    try:
        formatter = DataFormatter()
        print("✓ DataFormatter initialized successfully")
    except Exception as e:
        print(f"✗ DataFormatter initialization failed: {e}")
        return False

    # 4. ExcelWriterのテスト
    print("[4/4] ExcelWriterの初期化...")
    try:
        writer = ExcelWriter()
        print("✓ ExcelWriter initialized successfully")
    except Exception as e:
        print(f"✗ ExcelWriter initialization failed: {e}")
        return False

    print()
    print("=" * 60)
    print("✓ すべての基本機能テストが成功しました！")
    print("=" * 60)

    return True


if __name__ == "__main__":
    success = test_basic_functionality()
    sys.exit(0 if success else 1)
