"""Phase 2の機能テスト

Phase 2で追加・改善した機能のテストスクリプト
"""

from core.extractor import InfoExtractor

# テスト用HTML（改善された抽出機能をテスト）
test_html = """
<!DOCTYPE html>
<html>
<head>
    <title>テスト歯科医院 | 東京都渋谷区</title>
    <meta property="og:site_name" content="テスト歯科医院">
    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "テスト歯科医院",
        "legalName": "株式会社テスト歯科"
    }
    </script>
</head>
<body>
    <h1>テスト歯科医院</h1>

    <div class="contact">
        <p>電話: 03-1234-5678</p>
        <p>FAX: 03-1234-5679</p>
        <p>フリーダイヤル: 0120-123-456</p>
        <p>携帯: 090-1234-5678</p>
        <p>IP電話: 050-1234-5678</p>
        <p>メール: info@test-dental.com</p>
    </div>

    <div class="address">
        <p>〒150-0001</p>
        <p>東京都渋谷区神宮前1-2-3 テストビル3F</p>
    </div>

    <div class="hours">
        <p>営業時間: 9:00-18:00</p>
        <p>定休日: 水曜日、日曜日</p>
    </div>

    <div class="social">
        <a href="https://twitter.com/test_dental">Twitter</a>
        <a href="https://www.facebook.com/testdental">Facebook</a>
        <a href="https://www.instagram.com/test.dental">Instagram</a>
    </div>
</body>
</html>
"""

def test_phone_extraction():
    """電話番号抽出のテスト（Phase 2拡充）"""
    print("\n=== 電話番号抽出テスト ===")
    extractor = InfoExtractor()
    phones = extractor.extract_phone(test_html)
    print(f"抽出された電話番号 ({len(phones)}件):")
    for phone in phones:
        print(f"  - {phone}")

    # 期待値: 固定電話、フリーダイヤル、携帯、IP電話
    expected_types = ["03-", "0120-", "090-", "050-"]
    for exp_type in expected_types:
        if any(exp_type in phone for phone in phones):
            print(f"  ✓ {exp_type}系の番号が抽出されました")
        else:
            print(f"  ✗ {exp_type}系の番号が抽出されませんでした")

def test_address_extraction():
    """住所抽出のテスト（Phase 2拡充）"""
    print("\n=== 住所抽出テスト ===")
    extractor = InfoExtractor()
    address = extractor.extract_address(test_html)

    if address:
        print("抽出された住所情報:")
        print(f"  郵便番号: {address.get('postal_code')}")
        print(f"  都道府県: {address.get('prefecture')}")
        print(f"  市区町村: {address.get('city')}")
        print(f"  詳細住所: {address.get('address')}")

        # 検証
        if address.get('postal_code'):
            print("  ✓ 郵便番号が抽出されました")
        if address.get('prefecture'):
            print("  ✓ 都道府県が抽出されました")
        if address.get('city'):
            print("  ✓ 市区町村が抽出されました")
    else:
        print("  ✗ 住所情報が抽出されませんでした")

def test_company_name_extraction():
    """会社名抽出のテスト（Phase 2拡充）"""
    print("\n=== 会社名抽出テスト ===")
    extractor = InfoExtractor()
    company_name = extractor.extract_company_name(test_html)

    if company_name:
        print(f"抽出された会社名: {company_name}")
        print("  ✓ 会社名が抽出されました")
    else:
        print("  ✗ 会社名が抽出されませんでした")

def test_business_hours_extraction():
    """営業時間抽出のテスト（Phase 2新規）"""
    print("\n=== 営業時間抽出テスト ===")
    extractor = InfoExtractor()
    business_hours = extractor.extract_business_hours(test_html)

    if business_hours:
        print(f"抽出された営業時間: {business_hours}")
        print("  ✓ 営業時間が抽出されました")
    else:
        print("  ✗ 営業時間が抽出されませんでした")

def test_closed_days_extraction():
    """定休日抽出のテスト（Phase 2新規）"""
    print("\n=== 定休日抽出テスト ===")
    extractor = InfoExtractor()
    closed_days = extractor.extract_closed_days(test_html)

    if closed_days:
        print(f"抽出された定休日: {closed_days}")
        print("  ✓ 定休日が抽出されました")
    else:
        print("  ✗ 定休日が抽出されませんでした")

def test_all_extraction():
    """すべての情報を一度に抽出するテスト"""
    print("\n=== 統合抽出テスト ===")
    extractor = InfoExtractor()
    detailed_info = extractor.extract_all(test_html)

    print("DetailedInfo:")
    print(f"  電話番号: {detailed_info.phone}")
    print(f"  メール: {detailed_info.email}")
    print(f"  FAX: {detailed_info.fax}")
    print(f"  住所: {detailed_info.address}")
    print(f"  会社名: {detailed_info.company_name}")
    print(f"  SNS: {list(detailed_info.sns_links.keys()) if detailed_info.sns_links else []}")
    print(f"  営業時間: {detailed_info.business_hours}")
    print(f"  定休日: {detailed_info.closed_days}")

if __name__ == "__main__":
    print("=" * 60)
    print("Phase 2 機能テスト開始")
    print("=" * 60)

    test_phone_extraction()
    test_address_extraction()
    test_company_name_extraction()
    test_business_hours_extraction()
    test_closed_days_extraction()
    test_all_extraction()

    print("\n" + "=" * 60)
    print("Phase 2 機能テスト完了")
    print("=" * 60)
