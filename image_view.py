import os
from typing import Optional, Tuple, Dict, Any

from PyQt6.QtCore import Qt, QPointF, QRectF, pyqtSignal
from PyQt6.QtGui import QPixmap, QTransform, QWheelEvent, QMouseEvent, QKeyEvent, QPainter, QDragEnterEvent, QDragMoveEvent, QDropEvent
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem


class ImageView(QGraphicsView):
    """
    画像をシーンに描画し、ズーム・パン機能および
    各画像ごとの独立した「ズーム倍率・表示中心座標」を記憶・管理するカスタムグラフィックスビュー。
    """

    # ズーム倍率が変更された時に通知するシグナル (倍率パーセンテージ: 例 150.0)
    zoom_changed = pyqtSignal(float)

    # 最大拡大倍率（フィット基準で最大5.0倍）、最小縮小倍率（フィット基準で最小0.2倍）
    MAX_ZOOM_FACTOR = 5.0
    MIN_ZOOM_FACTOR = 0.2

    def __init__(self, parent=None):
        super().__init__(parent)

        self._scene = QGraphicsScene(self)
        self.setScene(self._scene)

        self.pixmap_item: Optional[QGraphicsPixmapItem] = None
        self.image_path: Optional[str] = None

        # 各画像ファイルごとの個別ズーム・表示状態辞書
        self.saved_view_states: Dict[str, Dict[str, Any]] = {}

        # 現在の画像の表示状態フラグおよび基準スケール
        self.is_custom_zoomed: bool = False
        self.fit_scale: float = 1.0  # フィット表示時の基本スケール (m11)

        # 描画品質とビューの設定
        self.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)

        # 背景を黒に設定
        self.setStyleSheet("background-color: black; border: none;")

        # ドラッグ＆ドロップ受け入れ設定
        self.setAcceptDrops(True)

        # ドラッグ（パン）モードの有効化
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # ホイールズームのアンカー設定（カーソル位置を中心にズーム）
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)

    def _get_key(self, path: Optional[str]) -> Optional[str]:
        if not path:
            return None
        return os.path.normcase(os.path.abspath(path))

    def get_current_zoom_percent(self) -> float:
        """現在のズーム倍率パーセンテージ (フィット表示時を100.0%とする) を計算"""
        if not self.pixmap_item or self.fit_scale <= 0:
            return 100.0
        current_scale = self.transform().m11()
        return round((current_scale / self.fit_scale) * 100.0, 1)

    def load_image(self, file_path: str) -> bool:
        """
        指定されたパスから画像を読み込み、シーンにセットする。
        """
        if not os.path.exists(file_path):
            return False

        pixmap = QPixmap(file_path)
        if pixmap.isNull():
            return False

        self.image_path = file_path

        # シーンをクリアして新規アイテム配置
        self._scene.clear()
        self.pixmap_item = QGraphicsPixmapItem(pixmap)
        self.pixmap_item.setTransformationMode(Qt.TransformationMode.SmoothTransformation)
        self._scene.addItem(self.pixmap_item)

        # シーンの境界領域を pixmap のサイズに合わせる
        self._scene.setSceneRect(QRectF(pixmap.rect()))

        return True

    def save_view_state(self, file_path: Optional[str] = None):
        """
        指定された画像（省略時は現在画像）のズーム倍率と画像上相対中心座標を個別保存する。
        """
        target_path = file_path or self.image_path
        key = self._get_key(target_path)

        if not key or not self.pixmap_item:
            return

        transform = self.transform()

        viewport_center = self.viewport().rect().center()
        scene_center = self.mapToScene(viewport_center)

        boundingRect = self.pixmap_item.boundingRect()
        img_width = boundingRect.width()
        img_height = boundingRect.height()

        if img_width > 0 and img_height > 0:
            rel_x = scene_center.x() / img_width
            rel_y = scene_center.y() / img_height
            relative_center = (rel_x, rel_y)
        else:
            relative_center = (0.5, 0.5)

        self.saved_view_states[key] = {
            "transform": transform,
            "relative_center": relative_center,
            "is_custom_zoomed": self.is_custom_zoomed,
            "fit_scale": self.fit_scale
        }

    def restore_view_state(self, file_path: Optional[str] = None):
        """
        指定された画像（省略時は現在画像）の過去の個別ズーム記憶があれば復元し、
        無ければ初期フィット表示にする。
        """
        target_path = file_path or self.image_path
        key = self._get_key(target_path)

        if not key or not self.pixmap_item:
            return

        state = self.saved_view_states.get(key)

        if state and state.get("is_custom_zoomed"):
            self.is_custom_zoomed = True
            saved_transform = state["transform"]
            rel_x, rel_y = state["relative_center"]
            if "fit_scale" in state:
                self.fit_scale = state["fit_scale"]

            self.setTransform(saved_transform)

            boundingRect = self.pixmap_item.boundingRect()
            target_scene_x = rel_x * boundingRect.width()
            target_scene_y = rel_y * boundingRect.height()

            self.centerOn(QPointF(target_scene_x, target_scene_y))
        else:
            self.fit_to_view(reset_saved_state=False)

    def fit_to_view(self, reset_saved_state: bool = True):
        """
        画像をウィンドウサイズ（アスペクト比維持）にフィット表示する。
        """
        if not self.pixmap_item:
            return

        self.resetTransform()
        self.fitInView(self.pixmap_item, Qt.AspectRatioMode.KeepAspectRatio)
        self.fit_scale = self.transform().m11()
        self.is_custom_zoomed = False

        if reset_saved_state and self.image_path:
            key = self._get_key(self.image_path)
            if key in self.saved_view_states:
                del self.saved_view_states[key]

    def _zoom_step(self, zoom_factor: float):
        """倍率調整処理 (共通処理)"""
        if not self.pixmap_item:
            return

        current_scale = self.transform().m11()
        next_scale = current_scale * zoom_factor

        base_scale = self.fit_scale if self.fit_scale > 0 else 1.0
        relative_scale = next_scale / base_scale

        if zoom_factor > 1.0 and relative_scale > self.MAX_ZOOM_FACTOR:
            return
        if zoom_factor < 1.0 and relative_scale < self.MIN_ZOOM_FACTOR:
            return

        self.scale(zoom_factor, zoom_factor)
        self.is_custom_zoomed = True
        self.save_view_state()

        zoom_pct = self.get_current_zoom_percent()
        self.zoom_changed.emit(zoom_pct)

    def zoom_in(self):
        """拡大 (キーボード等の外部入力用)"""
        self._zoom_step(1.15)

    def zoom_out(self):
        """縮小 (キーボード等の外部入力用)"""
        self._zoom_step(1.0 / 1.15)

    def wheelEvent(self, event: QWheelEvent):
        """
        マウスホイールイベントハンドラ（ズームイン / ズームアウト）
        """
        if not self.pixmap_item:
            return

        zoom_in_factor = 1.15
        zoom_out_factor = 1.0 / zoom_in_factor

        if event.angleDelta().y() > 0:
            self.zoom_in()
        else:
            self.zoom_out()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_custom_zoomed = True
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() & Qt.MouseButton.LeftButton:
            self.is_custom_zoomed = True
            self.save_view_state()
        super().mouseMoveEvent(event)

    def keyPressEvent(self, event: QKeyEvent):
        event.ignore()

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super().dragEnterEvent(event)

    def dragMoveEvent(self, event: QDragMoveEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super().dragMoveEvent(event)

    def dropEvent(self, event: QDropEvent):
        parent_window = self.window()
        if hasattr(parent_window, "handle_drop_event"):
            parent_window.handle_drop_event(event)
        else:
            super().dropEvent(event)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if not self.is_custom_zoomed and self.pixmap_item:
            self.fit_to_view(reset_saved_state=False)
