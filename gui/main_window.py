"""メインウィンドウモジュール

このモジュールは、アプリケーションのメインウィンドウを提供します。
CustomTkinterを使用してモダンなUIを実装します。
"""

import customtkinter as ctk
from pathlib import Path
from typing import Optional
from datetime import datetime
import threading

from config.settings import Settings
from utils.logger import get_logger
from gui.components.search_panel import SearchPanel, SearchConfig
from gui.components.result_panel import ResultPanel
from core.search_api import SearchAPIClient
from core.searcher import SearchOptions
from core.scraper import WebScraper
from core.extractor import InfoExtractor
from output.formatter import DataFormatter
from output.excel_writer import ExcelWriter

logger = get_logger(__name__)


class MainWindow(ctk.CTk):
    """メインウィンドウクラス

    アプリケーションのメインウィンドウを管理します。
    """

    def __init__(self):
        """初期化

        メインウィンドウを初期化します。
        """
        super().__init__()

        logger.info("Initializing main window")

        # ウィンドウの基本設定
        self.title("Google検索リサーチツール - Phase 3")
        self.geometry("1200x800")

        # 最小サイズを設定
        self.minsize(800, 600)

        # テーマ設定
        ctk.set_appearance_mode("system")  # "light", "dark", "system"
        ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"

        # 変数の初期化
        self.search_running = False
        self.search_results = []

        # コアコンポーネントの初期化
        self.search_client = SearchAPIClient()
        self.scraper = WebScraper()
        self.extractor = InfoExtractor()
        self.formatter = DataFormatter()
        self.excel_writer = ExcelWriter()

        # UIコンポーネントの作成
        self._create_menu_bar()
        self._create_main_layout()
        self._create_status_bar()

        # ウィンドウを中央に配置
        self._center_window()

        logger.info("Main window initialized")

    def _create_menu_bar(self) -> None:
        """メニューバーを作成

        ファイル、編集、ヘルプメニューを作成します。
        """
        logger.debug("Creating menu bar")

        # メニューバーフレーム
        self.menu_frame = ctk.CTkFrame(self, height=40, corner_radius=0)
        self.menu_frame.pack(fill="x", side="top")

        # ファイルメニュー
        self.file_button = ctk.CTkButton(
            self.menu_frame,
            text="ファイル",
            width=80,
            command=self._show_file_menu
        )
        self.file_button.pack(side="left", padx=5, pady=5)

        # 設定メニュー
        self.settings_button = ctk.CTkButton(
            self.menu_frame,
            text="設定",
            width=80,
            command=self._show_settings
        )
        self.settings_button.pack(side="left", padx=5, pady=5)

        # ヘルプメニュー
        self.help_button = ctk.CTkButton(
            self.menu_frame,
            text="ヘルプ",
            width=80,
            command=self._show_help
        )
        self.help_button.pack(side="left", padx=5, pady=5)

    def _create_main_layout(self) -> None:
        """メインレイアウトを作成

        検索パネルと結果パネルを配置します。
        """
        logger.debug("Creating main layout")

        # メインコンテナ
        self.main_container = ctk.CTkFrame(self, corner_radius=0)
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)

        # 左側: 検索設定パネル（固定幅360px）
        self.search_panel = SearchPanel(
            self.main_container,
            on_search_callback=self._on_search,
            on_export_callback=self._on_export
        )
        self.search_panel.pack(side="left", fill="both", padx=(0, 5), pady=0)
        self.search_panel.configure(width=360)

        # 右側: 結果表示パネル（可変幅）
        self.result_panel = ResultPanel(self.main_container)
        self.result_panel.pack(side="right", fill="both", expand=True, padx=(5, 0), pady=0)


    def _create_status_bar(self) -> None:
        """ステータスバーを作成

        アプリケーションの状態を表示します。
        """
        logger.debug("Creating status bar")

        # ステータスバーフレーム
        self.status_frame = ctk.CTkFrame(self, height=30, corner_radius=0)
        self.status_frame.pack(fill="x", side="bottom")

        # ステータスラベル
        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="準備完了",
            font=ctk.CTkFont(size=11)
        )
        self.status_label.pack(side="left", padx=10, pady=5)

        # API情報
        api_provider = Settings.SEARCH_API_PROVIDER.upper()
        self.api_label = ctk.CTkLabel(
            self.status_frame,
            text=f"検索API: {api_provider}",
            font=ctk.CTkFont(size=11)
        )
        self.api_label.pack(side="right", padx=10, pady=5)

    def _center_window(self) -> None:
        """ウィンドウを画面中央に配置"""
        self.update_idletasks()

        # 画面サイズを取得
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # ウィンドウサイズを取得
        window_width = self.winfo_width()
        window_height = self.winfo_height()

        # 中央座標を計算
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # ウィンドウを配置
        self.geometry(f"+{x}+{y}")

    def _show_file_menu(self) -> None:
        """ファイルメニューを表示（仮実装）"""
        logger.info("File menu clicked")
        # TODO: ファイルメニューの実装
        self.update_status("ファイルメニュー（未実装）")

    def _show_settings(self) -> None:
        """設定ダイアログを表示（仮実装）"""
        logger.info("Settings menu clicked")
        # TODO: 設定ダイアログの実装
        self.update_status("設定画面（未実装）")

    def _show_help(self) -> None:
        """ヘルプダイアログを表示（仮実装）"""
        logger.info("Help menu clicked")
        # TODO: ヘルプダイアログの実装
        self.update_status("ヘルプ画面（未実装）")

    def _on_search(self, config: SearchConfig) -> None:
        """検索開始時の処理

        Args:
            config: 検索設定
        """
        logger.info(f"Starting search: {config}")

        # 検索を別スレッドで実行
        search_thread = threading.Thread(
            target=self._execute_search,
            args=(config,),
            daemon=True
        )
        search_thread.start()

    def _execute_search(self, config: SearchConfig) -> None:
        """検索を実行（別スレッド）

        Args:
            config: 検索設定
        """
        try:
            # UI更新（メインスレッド）
            self.after(0, lambda: self.search_panel.set_search_running(True))
            self.after(0, lambda: self.result_panel.start_search(config.keyword))
            self.after(0, lambda: self.update_status(f"検索中: {config.keyword}"))

            # 検索実行
            logger.info(f"Searching: {config.keyword}, num={config.num_results}")
            search_options = SearchOptions(num_results=config.num_results)
            search_items = self.search_client.search(
                keyword=config.keyword,
                options=search_options
            )

            if not search_items:
                self.after(0, lambda: self.result_panel.show_error("検索結果が見つかりませんでした"))
                self.after(0, lambda: self.update_status("検索結果なし"))
                return

            self.after(0, lambda: self.update_status(f"{len(search_items)}件の結果を取得"))

            # 詳細情報の取得（オプション）
            detailed_infos = None
            if config.fetch_details:
                self.after(0, lambda: self.result_panel.show_progress("詳細情報を抽出中..."))
                self.after(0, lambda: self.update_status("詳細情報を抽出中..."))

                detailed_infos = []
                for i, item in enumerate(search_items, 1):
                    self.after(0, lambda i=i: self.result_panel.show_progress(f"  [{i}/{len(search_items)}] {item.url}"))

                    # HTMLを取得
                    page_content = self.scraper.fetch_page(item.url)
                    if page_content and page_content.html:
                        # 詳細情報を抽出
                        detailed_info = self.extractor.extract_all(page_content.html)
                        detailed_infos.append(detailed_info)
                    else:
                        detailed_infos.append(None)

            # データの整形
            self.after(0, lambda: self.update_status("データを整形中..."))
            output_data = self.formatter.format_data(search_items, detailed_infos)
            output_data = self.formatter.remove_duplicates(output_data)
            output_data = self.formatter.validate_data(output_data)

            # 結果を保存
            self.search_results = output_data

            # 結果を表示
            self.after(0, lambda: self.result_panel.show_search_results(output_data, config.keyword))
            self.after(0, lambda: self.search_panel.enable_export_button())
            self.after(0, lambda: self.update_status(f"完了: {len(output_data)}件の結果"))

        except Exception as e:
            logger.error(f"Search failed: {e}", exc_info=True)
            error_msg = str(e)
            self.after(0, lambda msg=error_msg: self.result_panel.show_error(f"検索エラー: {msg}"))
            self.after(0, lambda msg=error_msg: self.update_status(f"エラー: {msg}"))

        finally:
            self.after(0, lambda: self.search_panel.set_search_running(False))

    def _on_export(self) -> None:
        """Excel出力時の処理"""
        logger.info("Exporting to Excel")

        if not self.search_results:
            self.update_status("エラー: 出力するデータがありません")
            return

        try:
            self.update_status("Excelファイルを生成中...")

            # ファイル名の生成
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"search_results_{timestamp}.xlsx"

            # Excel出力
            output_path = self.excel_writer.write(
                self.search_results,
                filename
            )

            if output_path:
                self.update_status(f"保存完了: {output_path}")
                logger.info(f"Excel file saved: {output_path}")
            else:
                self.update_status("エラー: Excel出力に失敗しました")

        except Exception as e:
            logger.error(f"Export failed: {e}", exc_info=True)
            self.update_status(f"エラー: {str(e)}")

    def update_status(self, message: str) -> None:
        """ステータスバーを更新

        Args:
            message: 表示するメッセージ
        """
        self.status_label.configure(text=message)
        logger.debug(f"Status updated: {message}")

    def run(self) -> None:
        """アプリケーションを実行

        イベントループを開始します。
        """
        logger.info("Starting main window")
        self.mainloop()


def main():
    """メイン関数（テスト用）"""
    app = MainWindow()
    app.run()


if __name__ == "__main__":
    main()
