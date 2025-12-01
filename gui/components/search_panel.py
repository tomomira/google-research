"""検索パネルコンポーネント

このモジュールは、検索設定パネルのUIコンポーネントを提供します。
"""

import customtkinter as ctk
from typing import Callable, Optional
from dataclasses import dataclass

from utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class SearchConfig:
    """検索設定データクラス"""
    keyword: str
    num_results: int = 10
    fetch_details: bool = False


class SearchPanel(ctk.CTkFrame):
    """検索パネルクラス

    検索キーワードや取得件数などの設定UIを提供します。
    """

    def __init__(
        self,
        parent,
        on_search_callback: Optional[Callable[[SearchConfig], None]] = None,
        on_export_callback: Optional[Callable[[], None]] = None,
        **kwargs
    ):
        """初期化

        Args:
            parent: 親ウィジェット
            on_search_callback: 検索ボタンクリック時のコールバック関数
            on_export_callback: Excel出力ボタンクリック時のコールバック関数
        """
        super().__init__(parent, **kwargs)

        self.on_search_callback = on_search_callback
        self.on_export_callback = on_export_callback

        logger.info("Initializing SearchPanel")

        # UIコンポーネントの作成
        self._create_widgets()

    def _create_widgets(self) -> None:
        """ウィジェットを作成"""
        logger.debug("Creating search panel widgets")

        # タイトル
        title = ctk.CTkLabel(
            self,
            text="検索設定",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title.pack(pady=(10, 5))

        # 検索キーワード入力
        keyword_label = ctk.CTkLabel(
            self,
            text="検索キーワード:",
            font=ctk.CTkFont(size=12)
        )
        keyword_label.pack(pady=(20, 5), padx=10, anchor="w")

        self.keyword_entry = ctk.CTkEntry(
            self,
            placeholder_text="例: 東京 歯科医院",
            height=35
        )
        self.keyword_entry.pack(pady=(0, 10), padx=10, fill="x")

        # 取得件数
        num_label = ctk.CTkLabel(
            self,
            text="取得件数:",
            font=ctk.CTkFont(size=12)
        )
        num_label.pack(pady=(10, 5), padx=10, anchor="w")

        self.num_entry = ctk.CTkEntry(
            self,
            placeholder_text="10",
            height=35
        )
        self.num_entry.pack(pady=(0, 10), padx=10, fill="x")
        self.num_entry.insert(0, "10")  # デフォルト値を設定

        # 詳細情報取得チェックボックス
        self.detail_var = ctk.BooleanVar(value=False)
        self.detail_checkbox = ctk.CTkCheckBox(
            self,
            text="詳細情報を取得する",
            variable=self.detail_var,
            font=ctk.CTkFont(size=12)
        )
        self.detail_checkbox.pack(pady=(10, 5), padx=10, anchor="w")

        # 詳細情報の説明
        detail_info = ctk.CTkLabel(
            self,
            text="※ 電話番号、メール、住所、\n営業時間などを抽出します",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        detail_info.pack(pady=(0, 20), padx=10, anchor="w")

        # 検索ボタン
        self.search_button = ctk.CTkButton(
            self,
            text="検索開始",
            command=self._on_search_click,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#1f6aa5",
            hover_color="#144870"
        )
        self.search_button.pack(pady=(10, 10), padx=10, fill="x")

        # Excel出力ボタン
        self.export_button = ctk.CTkButton(
            self,
            text="Excelに出力",
            command=self._on_export_click,
            height=40,
            font=ctk.CTkFont(size=14),
            state="disabled"
        )
        self.export_button.pack(pady=(10, 10), padx=10, fill="x")

        # 使い方ガイド
        guide_frame = ctk.CTkFrame(self, fg_color="transparent")
        guide_frame.pack(pady=(30, 10), padx=10, fill="x")

        guide_title = ctk.CTkLabel(
            guide_frame,
            text="使い方",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        guide_title.pack(anchor="w")

        guide_text = ctk.CTkLabel(
            guide_frame,
            text=(
                "1. 検索キーワードを入力\n"
                "2. 取得件数を指定 (最大100)\n"
                "3. 詳細情報の取得を選択\n"
                "4. 検索開始をクリック\n"
                "5. Excelに出力をクリック"
            ),
            font=ctk.CTkFont(size=11),
            text_color="gray",
            justify="left"
        )
        guide_text.pack(anchor="w", pady=(5, 0))

    def _on_search_click(self) -> None:
        """検索ボタンクリック時の処理"""
        logger.info("Search button clicked")

        # 入力値の取得とバリデーション
        keyword = self.keyword_entry.get().strip()
        if not keyword:
            logger.warning("Keyword is empty")
            # TODO: エラーダイアログを表示
            return

        # 取得件数のバリデーション
        try:
            num_results = int(self.num_entry.get().strip())
            if num_results < 1 or num_results > 100:
                raise ValueError("取得件数は1〜100の範囲で指定してください")
        except ValueError as e:
            logger.warning(f"Invalid num_results: {e}")
            # TODO: エラーダイアログを表示
            return

        # 検索設定の作成
        config = SearchConfig(
            keyword=keyword,
            num_results=num_results,
            fetch_details=self.detail_var.get()
        )

        logger.info(f"Search config: keyword={config.keyword}, num={config.num_results}, details={config.fetch_details}")

        # コールバック関数の呼び出し
        if self.on_search_callback:
            self.on_search_callback(config)

    def _on_export_click(self) -> None:
        """Excel出力ボタンクリック時の処理"""
        logger.info("Export button clicked")

        # コールバック関数の呼び出し
        if self.on_export_callback:
            self.on_export_callback()

    def enable_export_button(self) -> None:
        """Excel出力ボタンを有効化"""
        self.export_button.configure(state="normal")
        logger.debug("Export button enabled")

    def disable_export_button(self) -> None:
        """Excel出力ボタンを無効化"""
        self.export_button.configure(state="disabled")
        logger.debug("Export button disabled")

    def set_search_running(self, is_running: bool) -> None:
        """検索実行中の状態を設定

        Args:
            is_running: 検索実行中かどうか
        """
        if is_running:
            self.search_button.configure(state="disabled", text="検索中...")
            self.keyword_entry.configure(state="disabled")
            self.num_entry.configure(state="disabled")
            self.detail_checkbox.configure(state="disabled")
        else:
            self.search_button.configure(state="normal", text="検索開始")
            self.keyword_entry.configure(state="normal")
            self.num_entry.configure(state="normal")
            self.detail_checkbox.configure(state="normal")

        logger.debug(f"Search running state: {is_running}")
