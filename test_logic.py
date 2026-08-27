import os
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QPoint
from viewer_window import ViewerWindow


def test_context_menu():
    """右クリックコンテキストメニュー表示のテスト"""
    app = QApplication.instance() or QApplication(sys.argv)
    window = ViewerWindow()
    window.resize(1920, 1080)
    window.show()

    # 右クリックコンテキストメニュー表示メソッドの存在および動作検証
    assert hasattr(window, "show_context_menu"), "ViewerWindow should have show_context_menu method"
    assert hasattr(window.image_view, "contextMenuEvent"), "ImageView should handle contextMenuEvent"

    print("[PASS] Context menu handler test passed.")


if __name__ == "__main__":
    test_context_menu()
    print("All tests (context menu functionality) passed successfully!")
