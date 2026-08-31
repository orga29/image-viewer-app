import os
from PIL import Image

src_img_path = r"C:\Users\win\.gemini\antigravity-ide\brain\f0a8504a-1dcd-47ae-a7ff-8008166a2ade\picasa_app_icon_design_1788152467757.png"
dest_dir = r"d:\NextCloud\AI-workroom\image-viewer-app"
dest_pkg_dir = os.path.join(dest_dir, "FastViewer_Python_App")

if os.path.exists(src_img_path):
    img = Image.open(src_img_path).convert("RGBA")
    
    # 1. app_icon.png として保存
    png_path = os.path.join(dest_dir, "app_icon.png")
    pkg_png_path = os.path.join(dest_pkg_dir, "app_icon.png")
    img.save(png_path, "PNG")
    img.save(pkg_png_path, "PNG")
    
    # 2. マルチサイズ .ico ファイルとして保存 (16x16, 32x32, 48x48, 64x64, 128x128, 256x256)
    ico_path = os.path.join(dest_dir, "app_icon.ico")
    pkg_ico_path = os.path.join(dest_pkg_dir, "app_icon.ico")
    
    sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    img.save(ico_path, format="ICO", sizes=sizes)
    img.save(pkg_ico_path, format="ICO", sizes=sizes)
    
    print("[SUCCESS] App icons created successfully.")
else:
    print("[ERROR] Source image not found.")
