import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from viewer_window import ViewerWindow


def main():
    # Windows タスクバーアイコン分離用 AppUserModelID の登録
    if sys.platform == "win32":
        try:
            import ctypes
            myappid = "orga29.fastimageviewer.picasa.1"
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except Exception:
            pass

    app = QApplication(sys.argv)
    app.setApplicationName("Picasa風 Fast Image Viewer")

    # アプリケーションアイコンの設定
    base_dir = os.path.dirname(__file__)
    icon_path = os.path.join(base_dir, "app_icon.ico")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    window = ViewerWindow()
    window.show()

    # コマンドライン引数でファイル/フォルダが指定されている場合は直ちに読み込み
    if len(sys.argv) > 1:
        target_path = sys.argv[1]
        if os.path.exists(target_path):
            window.open_target(target_path)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
