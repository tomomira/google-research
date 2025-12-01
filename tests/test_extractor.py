"""extractorモジュールのテスト

このモジュールは、InfoExtractorクラスの単体テストを提供します。
"""

import pytest
from core.extractor import InfoExtractor, DetailedInfo


@pytest.fixture
def extractor():
    """InfoExtractorのフィクスチャ"""
    return InfoExtractor()


@pytest.fixture
def sample_html():
    """テスト用HTMLのフィクスチャ"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>テスト歯科医院</title>
        <meta property="og:site_name" content="テスト歯科医院">
        <script type="application/ld+json">
        {
            "@context": "https://schema.org",
            "@type": "Organization",
            "name": "テスト歯科医院"
        }
        </script>
    </head>
    <body>
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
            <p>東京都渋谷区神宮前1-2-3</p>
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


class TestPhoneExtraction:
    """電話番号抽出のテスト"""

    def test_extract_phone_basic(self, extractor, sample_html):
        """基本的な電話番号抽出"""
        phones = extractor.extract_phone(sample_html)
        assert len(phones) > 0
        assert any("03-" in phone for phone in phones)

    def test_extract_phone_freephone(self, extractor, sample_html):
        """フリーダイヤル抽出"""
        phones = extractor.extract_phone(sample_html)
        assert any("0120-" in phone for phone in phones)

    def test_extract_phone_mobile(self, extractor, sample_html):
        """携帯電話番号抽出"""
        phones = extractor.extract_phone(sample_html)
        assert any("090-" in phone for phone in phones)

    def test_extract_phone_ip(self, extractor, sample_html):
        """IP電話番号抽出"""
        phones = extractor.extract_phone(sample_html)
        assert any("050-" in phone for phone in phones)

    def test_extract_phone_empty(self, extractor):
        """電話番号が存在しないHTMLのテスト"""
        html = "<html><body>No phone</body></html>"
        phones = extractor.extract_phone(html)
        assert phones == []


class TestEmailExtraction:
    """メールアドレス抽出のテスト"""

    def test_extract_email_basic(self, extractor, sample_html):
        """基本的なメールアドレス抽出"""
        emails = extractor.extract_email(sample_html)
        assert len(emails) > 0
        assert "info@test-dental.com" in emails

    def test_extract_email_empty(self, extractor):
        """メールアドレスが存在しないHTMLのテスト"""
        html = "<html><body>No email</body></html>"
        emails = extractor.extract_email(html)
        assert emails == []

    def test_extract_email_multiple(self, extractor):
        """複数のメールアドレス抽出"""
        html = """
        <html><body>
            <p>info@example.com</p>
            <p>support@example.com</p>
        </body></html>
        """
        emails = extractor.extract_email(html)
        assert len(emails) >= 2


class TestAddressExtraction:
    """住所抽出のテスト"""

    def test_extract_address_with_postal_code(self, extractor, sample_html):
        """郵便番号付き住所抽出"""
        address = extractor.extract_address(sample_html)
        assert address is not None
        assert address.get("postal_code") == "150-0001"

    def test_extract_address_prefecture(self, extractor, sample_html):
        """都道府県抽出"""
        address = extractor.extract_address(sample_html)
        assert address is not None
        assert address.get("prefecture") == "東京都"

    def test_extract_address_city(self, extractor, sample_html):
        """市区町村抽出"""
        address = extractor.extract_address(sample_html)
        assert address is not None
        assert address.get("city") == "渋谷区"

    def test_extract_address_empty(self, extractor):
        """住所が存在しないHTMLのテスト"""
        html = "<html><body>No address</body></html>"
        address = extractor.extract_address(html)
        assert address is None


class TestCompanyNameExtraction:
    """会社名抽出のテスト"""

    def test_extract_company_name_json_ld(self, extractor, sample_html):
        """JSON-LDから会社名抽出"""
        company_name = extractor.extract_company_name(sample_html)
        assert company_name == "テスト歯科医院"

    def test_extract_company_name_empty(self, extractor):
        """会社名が存在しないHTMLのテスト"""
        html = "<html><body>No company name</body></html>"
        company_name = extractor.extract_company_name(html)
        assert company_name is None


class TestBusinessHoursExtraction:
    """営業時間抽出のテスト"""

    def test_extract_business_hours(self, extractor, sample_html):
        """営業時間抽出"""
        business_hours = extractor.extract_business_hours(sample_html)
        assert business_hours is not None
        assert "9:00" in business_hours or "9時" in business_hours

    def test_extract_business_hours_empty(self, extractor):
        """営業時間が存在しないHTMLのテスト"""
        html = "<html><body>No hours</body></html>"
        business_hours = extractor.extract_business_hours(html)
        assert business_hours is None


class TestClosedDaysExtraction:
    """定休日抽出のテスト"""

    def test_extract_closed_days(self, extractor, sample_html):
        """定休日抽出"""
        closed_days = extractor.extract_closed_days(sample_html)
        assert closed_days is not None
        assert "水曜" in closed_days or "日曜" in closed_days

    def test_extract_closed_days_empty(self, extractor):
        """定休日が存在しないHTMLのテスト"""
        html = "<html><body>No closed days</body></html>"
        closed_days = extractor.extract_closed_days(html)
        assert closed_days is None


class TestSNSLinksExtraction:
    """SNSリンク抽出のテスト"""

    def test_extract_sns_links(self, extractor, sample_html):
        """SNSリンク抽出"""
        sns_links = extractor.extract_sns_links(sample_html)
        assert "twitter" in sns_links
        assert "facebook" in sns_links
        assert "instagram" in sns_links

    def test_extract_sns_links_empty(self, extractor):
        """SNSリンクが存在しないHTMLのテスト"""
        html = "<html><body>No SNS links</body></html>"
        sns_links = extractor.extract_sns_links(html)
        assert sns_links == {}


class TestExtractAll:
    """統合抽出のテスト"""

    def test_extract_all(self, extractor, sample_html):
        """すべての情報を一度に抽出"""
        detailed_info = extractor.extract_all(sample_html)

        # DetailedInfoのインスタンスであることを確認
        assert isinstance(detailed_info, DetailedInfo)

        # 各フィールドが適切に抽出されていることを確認
        assert len(detailed_info.phone) > 0
        assert len(detailed_info.email) > 0
        assert detailed_info.address is not None
        assert detailed_info.company_name is not None
        assert detailed_info.business_hours is not None
        assert detailed_info.closed_days is not None
        assert len(detailed_info.sns_links) > 0

    def test_extract_all_empty(self, extractor):
        """空のHTMLから抽出"""
        html = "<html><body></body></html>"
        detailed_info = extractor.extract_all(html)

        # 空の結果でもDetailedInfoのインスタンスであることを確認
        assert isinstance(detailed_info, DetailedInfo)
        assert detailed_info.phone == []
        assert detailed_info.email == []
        assert detailed_info.address is None
