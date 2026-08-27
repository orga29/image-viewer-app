import os
import sys
from PyQt6.QtWidgets import QApplication
from viewer_window import ViewerWindow


def test_multi_monitor_screen_tracking():
    """マルチモニター環境における動的スクリーントラッキングのテスト"""
    app = QApplication.instance() or QApplication(sys.argv)
    window = ViewerWindow()
    window.resize(800, 600)
    window.showNormal()

    # _get_current_screen メソッドの動作確認
    current_screen = window._get_current_screen()
    assert current_screen is not None, "Should get a valid QScreen instance"
    assert current_screen.availableGeometry().width() > 0, "Screen geometry should have valid width"

    # toggle_fullscreen が動的スクリーンを維持するか
    window.toggle_fullscreen()
    assert window.isFullScreen(), "Window should toggle to fullscreen"

    window.toggle_fullscreen()
    assert not window.isFullScreen(), "Window should toggle back to normal"

    print(f"[PASS] Multi-monitor screen tracking test passed (Screen: {current_screen.name()}).")


if __name__ == "__main__":
    test_multi_monitor_screen_tracking()
    print("All tests (multi-monitor screen tracking) passed successfully!")
