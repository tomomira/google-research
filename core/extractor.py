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
    """詳細情報"""
    phone: list[str] = field(default_factory=list)
    email: list[str] = field(default_factory=list)
    address: Optional[dict] = None
    fax: list[str] = field(default_factory=list)
    company_name: Optional[str] = None
    sns_links: dict[str, list[str]] = field(default_factory=dict)


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
        """すべての情報を抽出

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
            sns_links=self.extract_sns_links(html)
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
        """住所を抽出

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

        if postal_code or prefecture:
            address_info = {
                "postal_code": postal_code,
                "prefecture": prefecture,
                "city": None,  # Phase 2で実装
                "address": None  # Phase 2で実装
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
        """会社名・店舗名を抽出

        HTMLから会社名や店舗名を抽出します。
        Phase 1では簡易実装、Phase 2で改善予定。

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

            # titleタグから抽出を試みる
            title = soup.find('title')
            if title and title.string:
                company_name = title.string.strip()
                # 余分な文字列を除去（簡易版）
                company_name = company_name.split('|')[0].strip()
                company_name = company_name.split('-')[0].strip()
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
        """電話番号の妥当性を検証

        Args:
            phone: 電話番号文字列

        Returns:
            妥当な電話番号の場合True
        """
        # ハイフンを除去した数字のみの文字列
        digits_only = re.sub(r'[^0-9]', '', phone)

        # 10桁または11桁の電話番号のみ許可
        if len(digits_only) not in [10, 11]:
            return False

        # 0で始まること
        if not digits_only.startswith('0'):
            return False

        return True

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
