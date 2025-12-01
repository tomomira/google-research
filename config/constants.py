"""定数定義モジュール"""

# Google検索関連
GOOGLE_SEARCH_URL = "https://www.google.com/search"
GOOGLE_DOMAIN = "www.google.com"

# 検索結果件数の選択肢
NUM_RESULTS_OPTIONS = [10, 20, 50, 100]

# 地域設定の選択肢
REGION_OPTIONS = {
    "日本": "jp",
    "アメリカ": "us",
    "イギリス": "uk",
}

# 言語設定の選択肢
LANGUAGE_OPTIONS = {
    "日本語": "ja",
    "英語": "en",
}

# 期間指定の選択肢
PERIOD_OPTIONS = {
    "すべて": None,
    "過去24時間": "d",
    "過去1週間": "w",
    "過去1ヶ月": "m",
    "過去1年": "y",
}

# 抽出項目の定義
EXTRACTION_FIELDS = {
    "title": "タイトル",
    "url": "URL",
    "description": "説明文",
    "rank": "検索順位",
    "phone": "電話番号",
    "email": "メールアドレス",
    "address": "住所",
    "fax": "FAX番号",
    "company_name": "会社名・店舗名",
    "sns_links": "SNSリンク",
}

# 正規表現パターン
REGEX_PATTERNS = {
    # 電話番号（複数パターン）- Phase 2で拡充
    "phone": [
        r"0\d{1,4}-\d{1,4}-\d{4}",  # ハイフン区切り（基本）
        r"0\d{9,10}",  # ハイフンなし
        r"\(\d{2,4}\)\s?\d{1,4}-\d{4}",  # 括弧付き
        # フリーダイヤル
        r"0120-\d{3}-\d{3}",  # 0120
        r"0120\d{6}",  # 0120（ハイフンなし）
        r"0800-\d{3}-\d{4}",  # 0800
        r"0800\d{7}",  # 0800（ハイフンなし）
        # ナビダイヤル
        r"0570-\d{3}-\d{3}",
        r"0570\d{6}",
        # IP電話
        r"050-\d{4}-\d{4}",
        r"050\d{8}",
        # 携帯電話（特定パターン）
        r"0[789]0-\d{4}-\d{4}",
        r"0[789]0\d{8}",
    ],
    # メールアドレス
    "email": [
        r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
    ],
    # 郵便番号
    "postal_code": [
        r"〒\s?\d{3}-?\d{4}",  # 〒記号付き
        r"\d{3}-\d{4}",  # ハイフン付き
    ],
    # FAX番号
    "fax": [
        r"FAX[：:\s]*0\d{1,4}-\d{1,4}-\d{4}",
        r"ファックス[：:\s]*0\d{1,4}-\d{1,4}-\d{4}",
        r"fax[：:\s]*0\d{1,4}-\d{1,4}-\d{4}",
        r"Fax[：:\s]*0\d{1,4}-\d{1,4}-\d{4}",
    ],
}

# SNSドメイン
SNS_DOMAINS = {
    "twitter": ["twitter.com", "x.com"],
    "instagram": ["instagram.com"],
    "facebook": ["facebook.com", "fb.com"],
    "line": ["line.me"],
    "youtube": ["youtube.com"],
}

# エラーメッセージ
ERROR_MESSAGES = {
    "captcha_detected": "CAPTCHAが検出されました。処理を中止します。",
    "network_error": "ネットワークエラーが発生しました。",
    "timeout_error": "タイムアウトしました。",
    "parse_error": "ページの解析に失敗しました。",
    "file_save_error": "ファイルの保存に失敗しました。",
    "empty_keyword": "検索キーワードが空です。",
    "empty_data": "出力するデータがありません。",
    "invalid_url": "不正なURLです。",
    "robots_denied": "robots.txtによりアクセスが拒否されました。",
    "browser_start_failed": "ブラウザの起動に失敗しました。",
    "browser_not_running": "ブラウザが起動していません。",
    "page_load_timeout": "ページの読み込みがタイムアウトしました。",
}

# 成功メッセージ
SUCCESS_MESSAGES = {
    "search_completed": "検索が完了しました。",
    "extraction_completed": "情報抽出が完了しました。",
    "file_saved": "ファイルを保存しました: {filepath}",
    "excel_saved": "Excelファイルを保存しました: {path}",
}
