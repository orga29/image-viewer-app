import os
import re
from typing import List, Optional


class FileManager:
    """
    ターゲットフォルダ内の画像をリスト化し、インデックスや前後の画像パスを管理するクラス。
    """

    SUPPORTED_EXTENSIONS = {
        ".jpg", ".jpeg", ".png", ".bmp", ".webp", ".gif", ".tif", ".tiff"
    }

    def __init__(self):
        self.image_files: List[str] = []
        self.current_index: int = -1
        self.current_dir: Optional[str] = None

    def _natural_sort_key(self, s: str):
        """
        ファイル名を自然順（数字を認識した昇順）でソートするためのキー関数。
        例: img1.jpg, img2.jpg, img10.jpg の順にソートされる。
        """
        return [int(text) if text.isdigit() else text.lower() for text in re.split(r"(\d+)", s)]

    def load_directory(self, target_path: str, initial_file: Optional[str] = None) -> bool:
        """
        指定されたファイルまたはディレクトリから、同フォルダ内の対応画像を検索・リスト化する。
        任意ファイルが開かれた場合でも、同フォルダ内に対応画像があれば一覧を構築する。
        
        :param target_path: ディレクトリパスまたは画像/任意ファイルのパス
        :param initial_file: 最初に入力されたファイルパス（指定されている場合）
        :return: 閲覧可能な画像が1つ以上見つかった場合 True
        """
        if not target_path:
            return False

        abs_path = os.path.abspath(target_path)

        if os.path.isfile(abs_path):
            directory = os.path.dirname(abs_path)
            if not initial_file:
                initial_file = abs_path
        elif os.path.isdir(abs_path):
            directory = abs_path
        else:
            return False

        self.current_dir = directory
        files = []

        try:
            for entry in os.listdir(directory):
                full_path = os.path.join(directory, entry)
                if os.path.isfile(full_path):
                    ext = os.path.splitext(entry)[1].lower()
                    if ext in self.SUPPORTED_EXTENSIONS:
                        files.append(full_path)
        except Exception as e:
            print(f"ディレクトリの読み込みエラー: {e}")
            return False

        # 自然順でソート
        self.image_files = sorted(files, key=self._natural_sort_key)

        if not self.image_files:
            self.current_index = -1
            return False

        # 初期表示画像のインデックス設定 (Windows大文字小文字表記揺れに対応)
        if initial_file:
            norm_initial = os.path.normcase(os.path.abspath(initial_file))
            matched_idx = -1
            for idx, img_path in enumerate(self.image_files):
                if os.path.normcase(img_path) == norm_initial:
                    matched_idx = idx
                    break
            
            if matched_idx != -1:
                self.current_index = matched_idx
            else:
                self.current_index = 0
        else:
            self.current_index = 0

        return True

    def get_current(self) -> Optional[str]:
        """現在選択されている画像のフルパスを取得"""
        if 0 <= self.current_index < len(self.image_files):
            return self.image_files[self.current_index]
        return None

    def get_next(self) -> Optional[str]:
        """次の画像のフルパスを取得し、インデックスを移動（非ループ・末尾で停止）"""
        if not self.image_files:
            return None
        if self.current_index < len(self.image_files) - 1:
            self.current_index += 1
        return self.get_current()

    def get_prev(self) -> Optional[str]:
        """前の画像のフルパスを取得し、インデックスを移動（非ループ・先頭で停止）"""
        if not self.image_files:
            return None
        if self.current_index > 0:
            self.current_index -= 1
        return self.get_current()

    def get_total_count(self) -> int:
        """読み込まれている画像の総数を返す"""
        return len(self.image_files)

    def get_current_index(self) -> int:
        """現在のインデックス (0スタート) を返す"""
        return self.current_index
