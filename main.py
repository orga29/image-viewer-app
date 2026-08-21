import sys
import os
from PyQt6.QtWidgets import QApplication
from viewer_window import ViewerWindow


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Picasa Clone Viewer")

    window = ViewerWindow()
    window.show()

    # コマンドライン引数でファイル/フォルダが指定されている場合は直ちに読み込み
    if len(sys.argv) > 1:
        target_path = sys.argv[1]
        if os.path.exists(target_path):
            window.open_target(target_path)
    # 引数がない場合は、ダイアログを自動表示せずドラッグ＆ドロップ待機画面として立ち上げる

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
