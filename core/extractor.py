"""Webページから情報を抽出するモジュール

このモジュールは、HTMLから電話番号、メールアドレス、住所などの
情報を正規表現を使って抽出する機能を提供します。
"""

from dataclasses import dataclass, field
from typing import Optional
import re
from bs4 import BeautifulSoup

from config.constants import REGEX_PATTERNS
from utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class DetailedInfo:
    """詳細情報（Phase 2で拡充）"""
    phone: list[str] = field(default_factory=list)
    email: list[str] = field(default_factory=list)
    address: Optional[dict] = None
    fax: list[str] = field(default_factory=list)
    company_name: Optional[str] = None
    sns_links: dict[str, list[str]] = field(default_factory=dict)
    business_hours: Optional[str] = None  # Phase 2で追加
    closed_days: Optional[str] = None  # Phase 2で追加


class InfoExtractor:
    """Webページから情報を抽出するクラス

    HTMLから電話番号、メールアドレス、住所などの情報を抽出します。
    正規表現パターンを使用して、各種情報を検出します。
    """

    def __init__(self):
        """初期化

        InfoExtractorインスタンスを初期化します。
        """
        self.phone_patterns = REGEX_PATTERNS["phone"]
        self.email_patterns = REGEX_PATTERNS["email"]
        self.postal_code_patterns = REGEX_PATTERNS["postal_code"]
        logger.info("InfoExtractor initialized")

    def extract_all(self, html: str) -> DetailedInfo:
        """すべての情報を抽出（Phase 2で拡充）

        HTMLからすべての情報を一度に抽出します。

        Args:
            html: 解析対象のHTML文字列

        Returns:
            抽出された詳細情報
        """
        logger.info("Extracting all information from HTML")

        detailed_info = DetailedInfo(
            phone=self.extract_phone(html),
            email=self.extract_email(html),
            address=self.extract_address(html),
            fax=self.extract_fax(html),
            company_name=self.extract_company_name(html),
            sns_links=self.extract_sns_links(html),
            business_hours=self.extract_business_hours(html),  # Phase 2で追加
            closed_days=self.extract_closed_days(html)  # Phase 2で追加
        )

        logger.info(f"Extraction completed: phone={len(detailed_info.phone)}, "
                   f"email={len(detailed_info.email)}, "
                   f"fax={len(detailed_info.fax)}")

        return detailed_info

    def extract_phone(self, html: str) -> list[str]:
        """電話番号を抽出

        HTMLから電話番号を抽出します。

        Args:
            html: 解析対象のHTML文字列

        Returns:
            抽出された電話番号のリスト（重複除去済み）
        """
        if not html:
            logger.warning("HTML is empty")
            return []

        # HTMLタグを除去してテキストのみを取得
        text = self._strip_html_tags(html)

        phone_numbers = set()

        # 各パターンで検索
        for pattern in self.phone_patterns:
            try:
                matches = re.findall(pattern, text)
                for match in matches:
                    # 正規化（ハイフンの統一など）
                    normalized = self._normalize_phone(match)
                    if normalized and self._validate_phone(normalized):
                        phone_numbers.add(normalized)
            except re.error as e:
                logger.error(f"Regex error in phone pattern '{pattern}': {e}")

        result = sorted(list(phone_numbers))
        logger.debug(f"Extracted {len(result)} phone numbers")
        return result

    def extract_email(self, html: str) -> list[str]:
        """メールアドレスを抽出

        HTMLからメールアドレスを抽出します。

        Args:
            html: 解析対象のHTML文字列

        Returns:
            抽出されたメールアドレスのリスト（重複除去済み）
        """
        if not html:
            logger.warning("HTML is empty")
            return []

        # HTMLタグを除去してテキストのみを取得
        text = self._strip_html_tags(html)

        email_addresses = set()

        # 各パターンで検索
        for pattern in self.email_patterns:
            try:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    # 正規化（小文字に統一）
                    normalized = match.lower().strip()
                    if self._validate_email(normalized):
                        email_addresses.add(normalized)
            except re.error as e:
                logger.error(f"Regex error in email pattern '{pattern}': {e}")

        result = sorted(list(email_addresses))
        logger.debug(f"Extracted {len(result)} email addresses")
        return result

    def extract_address(self, html: str) -> Optional[dict]:
        """住所を抽出（Phase 2で拡充）

        HTMLから住所を抽出します。

        Args:
            html: 解析対象のHTML文字列

        Returns:
            抽出された住所情報の辞書（postal_code, prefecture, city, address）
            見つからない場合はNone
        """
        if not html:
            logger.warning("HTML is empty")
            return None

        text = self._strip_html_tags(html)

        # 郵便番号の抽出
        postal_code = None
        for pattern in self.postal_code_patterns:
            try:
                match = re.search(pattern, text)
                if match:
                    postal_code = match.group(0)
                    # 正規化（ハイフン付きの形式に統一）
                    postal_code = re.sub(r'[〒\s]', '', postal_code)
                    if len(postal_code) == 7:
                        postal_code = f"{postal_code[:3]}-{postal_code[3:]}"
                    break
            except re.error as e:
                logger.error(f"Regex error in postal code pattern '{pattern}': {e}")

        # 都道府県の抽出
        prefecture_pattern = r'(北海道|青森県|岩手県|宮城県|秋田県|山形県|福島県|茨城県|栃木県|群馬県|埼玉県|千葉県|東京都|神奈川県|新潟県|富山県|石川県|福井県|山梨県|長野県|岐阜県|静岡県|愛知県|三重県|滋賀県|京都府|大阪府|兵庫県|奈良県|和歌山県|鳥取県|島根県|岡山県|広島県|山口県|徳島県|香川県|愛媛県|高知県|福岡県|佐賀県|長崎県|熊本県|大分県|宮崎県|鹿児島県|沖縄県)'
        prefecture_match = re.search(prefecture_pattern, text)
        prefecture = prefecture_match.group(0) if prefecture_match else None

        # 市区町村の抽出（Phase 2で実装）
        city = None
        if prefecture:
            # 都道府県の後に続く市区町村を抽出
            city_pattern = rf'{re.escape(prefecture)}([^\s]+?[市区町村])'
            city_match = re.search(city_pattern, text)
            if city_match:
                city = city_match.group(1)

        # 詳細住所の抽出（Phase 2で実装）
        full_address = None
        if prefecture:
            # 都道府県から始まる住所パターンを抽出
            # 番地・号まで含む住所を抽出
            address_pattern = rf'{re.escape(prefecture)}[^\s。、]{5,50}?(?:\d+[-ー\s]?\d+[-ー\s]?\d+|[0-9０-９]+[-ー\s]?[0-9０-９]+)'
            address_match = re.search(address_pattern, text)
            if address_match:
                full_address = address_match.group(0)
                # 余分な文字を除去
                full_address = re.sub(r'[「」『』【】\(\)]', '', full_address).strip()

        if postal_code or prefecture:
            address_info = {
                "postal_code": postal_code,
                "prefecture": prefecture,
                "city": city,
                "address": full_address
            }
            logger.debug(f"Extracted address: {address_info}")
            return address_info

        logger.debug("No address information found")
        return None

    def extract_fax(self, html: str) -> list[str]:
        """FAX番号を抽出

        HTMLからFAX番号を抽出します。

        Args:
            html: 解析対象のHTML文字列

        Returns:
            抽出されたFAX番号のリスト（重複除去済み）
        """
        if not html:
            logger.warning("HTML is empty")
            return []

        text = self._strip_html_tags(html)
        fax_numbers = set()

        # FAXの近くにある電話番号パターンを検索
        fax_pattern = r'(?:FAX|Fax|fax|ファックス|ファクス)[:\s]*([0-9\-\(\)]+)'

        try:
            matches = re.findall(fax_pattern, text)
            for match in matches:
                normalized = self._normalize_phone(match)
                if normalized and self._validate_phone(normalized):
                    fax_numbers.add(normalized)
        except re.error as e:
            logger.error(f"Regex error in fax pattern: {e}")

        result = sorted(list(fax_numbers))
        logger.debug(f"Extracted {len(result)} fax numbers")
        return result

    def extract_company_name(self, html: str) -> Optional[str]:
        """会社名・店舗名を抽出（Phase 2で拡充）

        HTMLから会社名や店舗名を抽出します。
        metaタグ、hタグ、JSON-LD、titleタグの順に試行します。

        Args:
            html: 解析対象のHTML文字列

        Returns:
            抽出された会社名。見つからない場合はNone
        """
        if not html:
            logger.warning("HTML is empty")
            return None

        try:
            soup = BeautifulSoup(html, 'lxml')

            # 1. JSON-LDから抽出を試みる（構造化データ）
            json_ld_scripts = soup.find_all('script', type='application/ld+json')
            for script in json_ld_scripts:
                try:
                    import json
                    data = json.loads(script.string)
                    # 組織名または店舗名を取得
                    if isinstance(data, dict):
                        name = data.get('name') or data.get('legalName')
                        if name:
                            logger.debug(f"Extracted company name from JSON-LD: {name}")
                            return name.strip()
                    elif isinstance(data, list):
                        for item in data:
                            if isinstance(item, dict):
                                name = item.get('name') or item.get('legalName')
                                if name:
                                    logger.debug(f"Extracted company name from JSON-LD: {name}")
                                    return name.strip()
                except (json.JSONDecodeError, AttributeError) as e:
                    logger.debug(f"Failed to parse JSON-LD: {e}")

            # 2. metaタグのog:site_nameから抽出
            og_site_name = soup.find('meta', property='og:site_name')
            if og_site_name and og_site_name.get('content'):
                company_name = og_site_name['content'].strip()
                logger.debug(f"Extracted company name from og:site_name: {company_name}")
                return company_name

            # 3. h1タグから抽出（最初のh1を会社名とみなす）
            h1 = soup.find('h1')
            if h1 and h1.get_text():
                company_name = h1.get_text().strip()
                # 明らかに会社名ではないものを除外
                if len(company_name) < 50 and '検索' not in company_name:
                    logger.debug(f"Extracted company name from h1: {company_name}")
                    return company_name

            # 4. titleタグから抽出（従来の方法）
            title = soup.find('title')
            if title and title.string:
                company_name = title.string.strip()
                # 余分な文字列を除去
                separators = ['|', '-', '–', '—', '/', '＜', '【']
                for sep in separators:
                    if sep in company_name:
                        company_name = company_name.split(sep)[0].strip()
                        break
                if len(company_name) > 0:
                    logger.debug(f"Extracted company name from title: {company_name}")
                    return company_name

        except Exception as e:
            logger.error(f"Error extracting company name: {e}")

        logger.debug("No company name found")
        return None

    def extract_sns_links(self, html: str) -> dict[str, list[str]]:
        """SNSリンクを抽出

        HTMLからSNS（Twitter, Facebook, Instagram等）のリンクを抽出します。

        Args:
            html: 解析対象のHTML文字列

        Returns:
            SNS名をキー、URLのリストを値とする辞書
        """
        if not html:
            logger.warning("HTML is empty")
            return {}

        sns_links = {
            "twitter": [],
            "facebook": [],
            "instagram": [],
            "line": [],
            "youtube": []
        }

        sns_patterns = {
            "twitter": r'https?://(?:www\.)?(?:twitter\.com|x\.com)/[\w]+',
            "facebook": r'https?://(?:www\.)?facebook\.com/[\w\.]+',
            "instagram": r'https?://(?:www\.)?instagram\.com/[\w\.]+',
            "line": r'https?://line\.me/[\w/]+',
            "youtube": r'https?://(?:www\.)?youtube\.com/[\w/\?=]+',
        }

        for sns_name, pattern in sns_patterns.items():
            try:
                matches = re.findall(pattern, html, re.IGNORECASE)
                sns_links[sns_name] = list(set(matches))
            except re.error as e:
                logger.error(f"Regex error in {sns_name} pattern: {e}")

        # 空のリストを除外
        sns_links = {k: v for k, v in sns_links.items() if v}

        logger.debug(f"Extracted SNS links: {list(sns_links.keys())}")
        return sns_links

    def _strip_html_tags(self, html: str) -> str:
        """HTMLタグを除去

        Args:
            html: HTML文字列

        Returns:
            タグを除去したテキスト
        """
        try:
            soup = BeautifulSoup(html, 'lxml')
            # scriptとstyleタグを削除
            for script in soup(["script", "style"]):
                script.decompose()
            text = soup.get_text(separator=' ')
            # 連続する空白を1つにまとめる
            text = re.sub(r'\s+', ' ', text)
            return text.strip()
        except Exception as e:
            logger.error(f"Error stripping HTML tags: {e}")
            return html

    def _normalize_phone(self, phone: str) -> str:
        """電話番号を正規化

        Args:
            phone: 電話番号文字列

        Returns:
            正規化された電話番号
        """
        # 全角数字を半角に変換
        phone = phone.translate(str.maketrans('0123456789', '0123456789'))
        # 括弧を除去
        phone = re.sub(r'[()（）]', '', phone)
        # スペースを除去
        phone = re.sub(r'\s', '', phone)
        return phone.strip()

    def _validate_phone(self, phone: str) -> bool:
        """電話番号の妥当性を検証（Phase 2で拡充）

        Args:
            phone: 電話番号文字列

        Returns:
            妥当な電話番号の場合True
        """
        # ハイフンを除去した数字のみの文字列
        digits_only = re.sub(r'[^0-9]', '', phone)

        # 0で始まること
        if not digits_only.startswith('0'):
            return False

        # 各種番号の桁数チェック
        length = len(digits_only)

        # フリーダイヤル (0120/0800)
        if digits_only.startswith('0120') or digits_only.startswith('0800'):
            return length == 10

        # ナビダイヤル (0570)
        if digits_only.startswith('0570'):
            return length == 10

        # IP電話 (050)
        if digits_only.startswith('050'):
            return length == 11

        # 携帯電話 (070/080/090)
        if digits_only.startswith(('070', '080', '090')):
            return length == 11

        # 固定電話 (市外局番による桁数の違い)
        # 10桁または11桁を許可
        if length in [10, 11]:
            return True

        return False

    def _validate_email(self, email: str) -> bool:
        """メールアドレスの妥当性を検証

        Args:
            email: メールアドレス文字列

        Returns:
            妥当なメールアドレスの場合True
        """
        # 基本的なフォーマットチェック
        if '@' not in email:
            return False

        # 画像ファイル等を除外
        invalid_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.svg']
        if any(email.endswith(ext) for ext in invalid_extensions):
            return False

        return True

    def extract_business_hours(self, html: str) -> Optional[str]:
        """営業時間を抽出（Phase 2で追加）

        HTMLから営業時間を抽出します。

        Args:
            html: 解析対象のHTML文字列

        Returns:
            抽出された営業時間。見つからない場合はNone
        """
        if not html:
            logger.warning("HTML is empty")
            return None

        text = self._strip_html_tags(html)

        # 営業時間のパターン
        patterns = [
            r'営業時間[：:\s]*([^\n。、]{5,50})',
            r'営業[：:\s]*([0-9０-９]+[時:：][0-9０-９]+[^\n。、]{0,30})',
            r'受付時間[：:\s]*([^\n。、]{5,50})',
            r'定休日を除く[：:\s]*([0-9０-９]+[時:：][0-9０-９]+[^\n。、]{0,30})',
            r'([月火水木金土日祝]+)[：:\s]*([0-9０-９]+[時:：][0-9０-９]+[-~〜～][0-9０-９]+[時:：][0-9０-９]+)',
        ]

        for pattern in patterns:
            try:
                match = re.search(pattern, text)
                if match:
                    business_hours = match.group(1).strip() if len(match.groups()) == 1 else match.group(0).strip()
                    # 長すぎる場合は先頭50文字のみ
                    if len(business_hours) > 100:
                        business_hours = business_hours[:100] + '...'
                    logger.debug(f"Extracted business hours: {business_hours}")
                    return business_hours
            except re.error as e:
                logger.error(f"Regex error in business hours pattern: {e}")

        logger.debug("No business hours found")
        return None

    def extract_closed_days(self, html: str) -> Optional[str]:
        """定休日を抽出（Phase 2で追加）

        HTMLから定休日を抽出します。

        Args:
            html: 解析対象のHTML文字列

        Returns:
            抽出された定休日。見つからない場合はNone
        """
        if not html:
            logger.warning("HTML is empty")
            return None

        text = self._strip_html_tags(html)

        # 定休日のパターン
        patterns = [
            r'定休日[：:\s]*([^\n。、]{2,30})',
            r'休業日[：:\s]*([^\n。、]{2,30})',
            r'休み[：:\s]*([月火水木金土日祝、・]+)',
            r'([月火水木金土日]+曜日?)休み',
        ]

        for pattern in patterns:
            try:
                match = re.search(pattern, text)
                if match:
                    closed_days = match.group(1).strip() if len(match.groups()) == 1 else match.group(0).strip()
                    # 長すぎる場合は先頭50文字のみ
                    if len(closed_days) > 50:
                        closed_days = closed_days[:50] + '...'
                    logger.debug(f"Extracted closed days: {closed_days}")
                    return closed_days
            except re.error as e:
                logger.error(f"Regex error in closed days pattern: {e}")

        logger.debug("No closed days found")
        return None
