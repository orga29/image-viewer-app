import os
from typing import Optional

from PyQt6.QtCore import Qt, QTimer, QPoint
from PyQt6.QtGui import QKeyEvent, QDragEnterEvent, QDragMoveEvent, QDropEvent, QAction
from PyQt6.QtWidgets import QMainWindow, QFileDialog, QLabel, QApplication, QMenu

from file_manager import FileManager
from image_view import ImageView


class ViewerWindow(QMainWindow):
    """
    フルスクリーン画像ビューアのメインウィンドウ。
    キーボードイベント、ファイルの連続読み込み、オーバーレイ情報表示およびコンテキストメニューを制御する。
    """

    def __init__(self):
        super().__init__()

        self.file_manager = FileManager()

        # メインビューアウィジェットの設定
        self.image_view = ImageView(self)
        self.setCentralWidget(self.image_view)

        # ズーム倍率変更シグナルを接続
        self.image_view.zoom_changed.connect(self._on_zoom_changed)

        # UIの最適化: 背景色黒、余計なフレームの排除
        self.setStyleSheet("background-color: black;")
        self.setAcceptDrops(True)

        # 中央ガイドラベル (画像未読込時の待機メッセージ)
        self.guide_label = QLabel(self)
        self.guide_label.setText("画像をドラッグ＆ドロップ\nまたは [ O ] キー / 右クリックでファイルを開く")
        self.guide_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.guide_label.setStyleSheet("""
            QLabel {
                background-color: rgba(30, 30, 35, 200);
                color: #CCCCCC;
                font-size: 20px;
                font-family: 'Segoe UI', 'Helvetica Neue', sans-serif;
                font-weight: 500;
                padding: 30px 50px;
                border: 2px dashed #555566;
                border-radius: 12px;
            }
        """)
        self.guide_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.guide_label.show()

        # 左下オーバーレイラベル（ファイル名や[インデックス/総数]、倍率を表示）
        self.info_label = QLabel(self)
        self.info_label.setStyleSheet("""
            QLabel {
                background-color: rgba(0, 0, 0, 160);
                color: #FFFFFF;
                font-size: 14px;
                font-family: 'Segoe UI', sans-serif;
                padding: 6px 14px;
                border-radius: 4px;
            }
        """)
        self.info_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.info_label.hide()

        # 表示自動消去用タイマー (2.0秒後に隠す)
        self.info_timer = QTimer(self)
        self.info_timer.setSingleShot(True)
        self.info_timer.timeout.connect(self.info_label.hide)

        # 初期ウィンドウ状態: フルスクリーン
        self.showFullScreen()
        self._center_guide_label()

    def _center_guide_label(self):
        """中央ガイドラベルを画面中央に配置"""
        if self.guide_label and self.guide_label.isVisible():
            self.guide_label.adjustSize()
            lx = (self.width() - self.guide_label.width()) // 2
            ly = (self.height() - self.guide_label.height()) // 2
            self.guide_label.move(lx, ly)
            self.guide_label.raise_()

    def _on_zoom_changed(self, zoom_pct: float):
        """ズーム倍率が変更された際のスロット"""
        if self.file_manager.get_total_count() > 0:
            self._update_overlay_info(zoom_pct=zoom_pct)

    def open_target(self, path: str):
        """
        ファイルまたはディレクトリのパスを受け取り、同フォルダの画像を読み込んで表示する。
        """
        if not path:
            return

        norm_path = os.path.normpath(path)
        if self.file_manager.load_directory(norm_path):
            current_file = self.file_manager.get_current()
            if current_file:
                self.image_view.load_image(current_file)
                self.image_view.restore_view_state(current_file)
                self.guide_label.hide()
                self._update_overlay_info()

        # キーボードフォーカスを固定
        self.setFocus()
        self.activateWindow()

    def show_next_image(self):
        """現在表示中画像の個別ズーム状態を保存し、次の画像へ移動"""
        if self.file_manager.get_total_count() == 0:
            return

        self.image_view.save_view_state()
        next_file = self.file_manager.get_next()
        if next_file:
            if self.image_view.load_image(next_file):
                self.image_view.restore_view_state(next_file)
                self._update_overlay_info()

    def show_prev_image(self):
        """現在表示中画像の個別ズーム状態を保存し、前の画像へ移動"""
        if self.file_manager.get_total_count() == 0:
            return

        self.image_view.save_view_state()
        prev_file = self.file_manager.get_prev()
        if prev_file:
            if self.image_view.load_image(prev_file):
                self.image_view.restore_view_state(prev_file)
                self._update_overlay_info()

    def reset_current_view(self):
        """現在の画像のズームと表示位置をリセット"""
        if self.file_manager.get_total_count() > 0:
            self.image_view.fit_to_view(reset_saved_state=True)
            self._update_overlay_info(zoom_pct=100.0)

    def toggle_fullscreen(self):
        """フルスクリーン表示の切り替え"""
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def open_file_dialog(self):
        """ファイル選択ダイアログを開く"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "画像ファイルを開く",
            "",
            "画像ファイル (*.jpg *.jpeg *.png *.bmp *.webp *.gif *.tif *.tiff);;すべてのファイル (*.*)"
        )
        if file_path:
            self.open_target(file_path)

    def show_context_menu(self, global_pos: QPoint):
        """右クリックポップアップメニューを表示"""
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: #26262B;
                color: #EEEEEE;
                border: 1px solid #44444D;
                border-radius: 8px;
                padding: 6px;
                font-size: 14px;
                font-family: 'Segoe UI', sans-serif;
            }
            QMenu::item {
                padding: 8px 24px;
                border-radius: 4px;
            }
            QMenu::item:selected {
                background-color: #3D3D45;
                color: #FFFFFF;
            }
            QMenu::separator {
                height: 1px;
                background-color: #44444D;
                margin: 6px 4px;
            }
        """)

        # アクションの追加
        open_action = QAction("📂  ファイルを開く (O)...", self)
        open_action.triggered.connect(self.open_file_dialog)
        menu.addAction(open_action)

        menu.addSeparator()

        reset_action = QAction("🔄  ズーム・表示位置をリセット (F5 / R)", self)
        reset_action.triggered.connect(self.reset_current_view)
        menu.addAction(reset_action)

        fullscreen_action = QAction("🖥️  フルスクリーン表示切り替え (F11)", self)
        fullscreen_action.triggered.connect(self.toggle_fullscreen)
        menu.addAction(fullscreen_action)

        menu.addSeparator()

        quit_action = QAction("❌  アプリを終了 (Esc / Alt+F4)", self)
        quit_action.triggered.connect(QApplication.quit)
        menu.addAction(quit_action)

        menu.exec(global_pos)

    def contextMenuEvent(self, event):
        """メインウィンドウ上の右クリックイベントハンドラ"""
        self.show_context_menu(event.globalPos())

    def _update_overlay_info(self, zoom_pct: Optional[float] = None):
        """現在の画像情報および倍率を画面左下に浮き上がらせて表示"""
        current_file = self.file_manager.get_current()
        if not current_file:
            return

        filename = os.path.basename(current_file)
        idx = self.file_manager.get_current_index() + 1
        total = self.file_manager.get_total_count()

        if zoom_pct is None:
            zoom_pct = self.image_view.get_current_zoom_percent()

        if not self.image_view.is_custom_zoomed and abs(zoom_pct - 100.0) < 1.0:
            zoom_str = "100% (Fit)"
        else:
            zoom_str = f"{int(zoom_pct)}%"

        text = f"[{idx} / {total}] {filename}   |   {zoom_str}"
        self.info_label.setText(text)
        self.info_label.adjustSize()

        margin = 20
        label_y = self.height() - self.info_label.height() - margin
        self.info_label.move(margin, label_y)
        self.info_label.show()
        self.info_label.raise_()

        self.info_timer.start(2000)

    def resizeEvent(self, event):
        """ウィンドウリサイズ時にオーバーレイ位置を補正"""
        super().resizeEvent(event)
        self._center_guide_label()
        if self.info_label.isVisible():
            margin = 20
            label_y = self.height() - self.info_label.height() - margin
            self.info_label.move(margin, label_y)

    def keyPressEvent(self, event: QKeyEvent):
        """
        キーボード操作のハンドリング
        """
        key = event.key()

        # ↑ キー: ズームイン (拡大)
        if key == Qt.Key.Key_Up:
            self.image_view.zoom_in()
        # ↓ キー: ズームアウト (縮小)
        elif key == Qt.Key.Key_Down:
            self.image_view.zoom_out()
        # 次の画像へ: 右矢印 / Space / PageDown / D / L
        elif key in (Qt.Key.Key_Right, Qt.Key.Key_Space, Qt.Key.Key_PageDown, Qt.Key.Key_D, Qt.Key.Key_L):
            self.show_next_image()
        # 前の画像へ: 左矢印 / PageUp / Backspace / A / K
        elif key in (Qt.Key.Key_Left, Qt.Key.Key_PageUp, Qt.Key.Key_Backspace, Qt.Key.Key_A, Qt.Key.Key_K):
            self.show_prev_image()
        elif key in (Qt.Key.Key_F5, Qt.Key.Key_R, Qt.Key.Key_0):
            self.reset_current_view()
        elif key == Qt.Key.Key_O:
            self.open_file_dialog()
        elif key == Qt.Key.Key_F11:
            self.toggle_fullscreen()
        elif key == Qt.Key.Key_Escape:
            if self.isFullScreen():
                self.showNormal()
            else:
                QApplication.quit()
        else:
            super().keyPressEvent(event)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dragMoveEvent(self, event: QDragMoveEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def handle_drop_event(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls:
            url = urls[0]
            file_path = url.toLocalFile()
            if not file_path and url.isLocalFile():
                file_path = url.path()

            if file_path:
                if os.name == "nt" and file_path.startswith("/") and len(file_path) > 2 and file_path[2] == ":":
                    file_path = file_path[1:]

                file_path = os.path.normpath(file_path)
                if os.path.exists(file_path):
                    event.acceptProposedAction()
                    self.open_target(file_path)

    def dropEvent(self, event: QDropEvent):
        self.handle_drop_event(event)
