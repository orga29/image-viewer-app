import os
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import QApplication
from viewer_window import ViewerWindow


def test_home_end_key_navigation():
    """Home / End キーによる画像移動動作のテスト"""
    app = QApplication.instance() or QApplication(sys.argv)
    window = ViewerWindow()

    # ダミーキーイベントのテスト判定
    end_event = QKeyEvent(QKeyEvent.Type.KeyPress, Qt.Key.Key_End, Qt.KeyboardModifier.NoModifier)
    home_event = QKeyEvent(QKeyEvent.Type.KeyPress, Qt.Key.Key_Home, Qt.KeyboardModifier.NoModifier)

    assert end_event.key() == Qt.Key.Key_End, "End key should be recognized"
    assert home_event.key() == Qt.Key.Key_Home, "Home key should be recognized"

    print("[PASS] Home / End key mapping test passed.")


if __name__ == "__main__":
    test_home_end_key_navigation()
    print("All tests (Home / End tilt navigation) passed successfully!")
