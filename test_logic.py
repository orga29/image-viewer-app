import os
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent
from viewer_window import ViewerWindow


def test_arrow_key_zoom():
    """↑キーで拡大、↓キーで縮小されるかのキーハンドリングテスト"""
    app = QApplication.instance() or QApplication(sys.argv)
    window = ViewerWindow()
    window.resize(1920, 1080)
    window.show()

    test_dir = os.path.join(os.path.dirname(__file__), "test_images")
    window.open_target(os.path.join(test_dir, "test_01.png"))

    initial_pct = window.image_view.get_current_zoom_percent()
    assert abs(initial_pct - 100.0) < 1.0

    # 1. ↑ キー (Up Arrow) を押す -> 拡大
    up_event = QKeyEvent(QKeyEvent.Type.KeyPress, Qt.Key.Key_Up, Qt.KeyboardModifier.NoModifier)
    window.keyPressEvent(up_event)

    zoomed_in_pct = window.image_view.get_current_zoom_percent()
    assert zoomed_in_pct > initial_pct, f"Up arrow should increase zoom percent (Got {zoomed_in_pct}%)"

    # 2. ↓ キー (Down Arrow) を押す -> 縮小
    down_event = QKeyEvent(QKeyEvent.Type.KeyPress, Qt.Key.Key_Down, Qt.KeyboardModifier.NoModifier)
    window.keyPressEvent(down_event)

    zoomed_out_pct = window.image_view.get_current_zoom_percent()
    assert zoomed_out_pct < zoomed_in_pct, f"Down arrow should decrease zoom percent (Got {zoomed_out_pct}%)"

    print(f"[PASS] Arrow key zoom test passed (Initial: {initial_pct}%, ZoomIn: {zoomed_in_pct}%, ZoomOut: {zoomed_out_pct}%).")


if __name__ == "__main__":
    test_arrow_key_zoom()
    print("All tests (arrow key zoom in/out) passed successfully!")
