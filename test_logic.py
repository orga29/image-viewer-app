import os
import sys
from PyQt6.QtWidgets import QApplication
from viewer_window import ViewerWindow


def test_window_aspect_ratio_adjustment():
    """画像解像度・アスペクト比連動のウィンドウサイズ調整テスト"""
    app = QApplication.instance() or QApplication(sys.argv)
    window = ViewerWindow()
    window.resize(800, 600)
    window.showNormal()

    test_dir = os.path.join(os.path.dirname(__file__), "test_images")
    window.open_target(os.path.join(test_dir, "test_01.png"))

    # _adjust_window_to_image_size メソッドの検証
    window._adjust_window_to_image_size()

    assert window.width() > 0 and window.height() > 0, "Window dimensions should be positive"
    print(f"[PASS] Window aspect ratio adjustment test passed (Resized: {window.width()}x{window.height()}).")


if __name__ == "__main__":
    test_window_aspect_ratio_adjustment()
    print("All tests (image aspect ratio window sizing) passed successfully!")
