"""結果表示パネルコンポーネント

このモジュールは、検索結果表示パネルのUIコンポーネントを提供します。
"""

import customtkinter as ctk
from typing import Optional
from datetime import datetime

from output.formatter import OutputData
from utils.logger import get_logger

logger = get_logger(__name__)


class ResultPanel(ctk.CTkFrame):
    """結果表示パネルクラス

    検索結果をテーブル形式で表示します。
    """

    def __init__(self, parent, **kwargs):
        """初期化

        Args:
            parent: 親ウィジェット
        """
        super().__init__(parent, **kwargs)

        self.results_data: list[OutputData] = []

        logger.info("Initializing ResultPanel")

        # UIコンポーネントの作成
        self._create_widgets()

    def _create_widgets(self) -> None:
        """ウィジェットを作成"""
        logger.debug("Creating result panel widgets")

        # タイトルとサマリー行
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=(10, 5))

        # タイトル
        self.title_label = ctk.CTkLabel(
            header_frame,
            text="検索結果",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.title_label.pack(side="left")

        # サマリー（件数表示）
        self.summary_label = ctk.CTkLabel(
            header_frame,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.summary_label.pack(side="right")

        # 結果表示用テキストボックス（スクロール可能）
        self.result_textbox = ctk.CTkTextbox(
            self,
            wrap="word",
            font=ctk.CTkFont(size=11, family="Courier")
        )
        self.result_textbox.pack(pady=(5, 10), padx=10, fill="both", expand=True)

        # 初期メッセージ
        self._show_welcome_message()

    def _show_welcome_message(self) -> None:
        """ウェルカムメッセージを表示"""
        welcome_text = """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Google検索リサーチツール - Phase 3 GUI版
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

検索結果がここに表示されます。

左側の検索設定パネルから検索を開始してください。

【主な機能】
  ✓ Tavily API統合検索（月1,000件無料）
  ✓ 詳細情報抽出（電話番号、メール、住所、営業時間など）
  ✓ Excel形式での出力

【使い方】
  1. 検索キーワードを入力
  2. 取得件数を指定
  3. 詳細情報の取得を選択（オプション）
  4. 検索開始をクリック
  5. Excelに出力をクリック

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        self.result_textbox.delete("1.0", "end")
        self.result_textbox.insert("1.0", welcome_text)
        self.result_textbox.configure(state="disabled")

    def show_search_results(self, results: list[OutputData], keyword: str) -> None:
        """検索結果を表示

        Args:
            results: 検索結果のリスト
            keyword: 検索キーワード
        """
        logger.info(f"Displaying {len(results)} search results")

        self.results_data = results

        # サマリーの更新
        self.summary_label.configure(text=f"{len(results)}件の結果")

        # 結果の整形と表示
        self.result_textbox.configure(state="normal")
        self.result_textbox.delete("1.0", "end")

        # ヘッダー
        header = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    検索結果: {keyword}
    取得件数: {len(results)}件
    取得日時: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
        self.result_textbox.insert("end", header)

        # 各結果の表示
        for i, result in enumerate(results, 1):
            result_text = self._format_result(i, result)
            self.result_textbox.insert("end", result_text)
            self.result_textbox.insert("end", "\n" + "─" * 80 + "\n\n")

        self.result_textbox.configure(state="disabled")
        logger.debug("Search results displayed")

    def _format_result(self, rank: int, result: OutputData) -> str:
        """検索結果を整形

        Args:
            rank: 順位
            result: 検索結果データ

        Returns:
            整形されたテキスト
        """
        lines = [f"【{rank}】 {result.title}"]
        lines.append(f"URL: {result.url}")

        if result.description:
            lines.append(f"説明: {result.description[:100]}...")

        # 詳細情報（取得されている場合のみ表示）
        if result.phone:
            lines.append(f"電話: {result.phone}")
        if result.email:
            lines.append(f"メール: {result.email}")
        if result.company_name:
            lines.append(f"会社名: {result.company_name}")
        if result.prefecture:
            address_parts = [result.prefecture]
            lines.append(f"住所: {', '.join(address_parts)}")
        if result.business_hours:
            lines.append(f"営業時間: {result.business_hours}")
        if result.closed_days:
            lines.append(f"定休日: {result.closed_days}")

        return "\n".join(lines)

    def show_progress(self, message: str) -> None:
        """進捗メッセージを表示

        Args:
            message: 表示するメッセージ
        """
        logger.debug(f"Progress message: {message}")

        self.result_textbox.configure(state="normal")
        self.result_textbox.insert("end", f"\n{message}")
        self.result_textbox.see("end")  # 最後までスクロール
        self.result_textbox.configure(state="disabled")

    def show_error(self, error_message: str) -> None:
        """エラーメッセージを表示

        Args:
            error_message: エラーメッセージ
        """
        logger.error(f"Error message: {error_message}")

        self.result_textbox.configure(state="normal")
        self.result_textbox.delete("1.0", "end")

        error_text = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    エラーが発生しました
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{error_message}

もう一度お試しください。
問題が解決しない場合は、ログファイル (logs/app.log) を確認してください。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        self.result_textbox.insert("1.0", error_text)
        self.result_textbox.configure(state="disabled")

    def clear_results(self) -> None:
        """結果をクリア"""
        logger.debug("Clearing results")
        self.results_data = []
        self.summary_label.configure(text="")
        self._show_welcome_message()

    def start_search(self, keyword: str) -> None:
        """検索開始時の表示

        Args:
            keyword: 検索キーワード
        """
        logger.debug(f"Starting search: {keyword}")

        self.result_textbox.configure(state="normal")
        self.result_textbox.delete("1.0", "end")

        search_text = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    検索中: {keyword}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

検索を実行しています...

"""
        self.result_textbox.insert("1.0", search_text)
        self.result_textbox.configure(state="disabled")
