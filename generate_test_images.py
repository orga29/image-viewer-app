import os
from PIL import Image, ImageDraw, ImageFont

def create_test_images():
    output_dir = os.path.join(os.path.dirname(__file__), "test_images")
    os.makedirs(output_dir, exist_ok=True)

    configs = [
        ("test_01.png", (1920, 1080), "blue", "Image 1: 1920x1080 (Blue)"),
        ("test_02.jpg", (2560, 1440), "darkgreen", "Image 2: 2560x1440 (Green)"),
        ("test_03.png", (1280, 720), "maroon", "Image 3: 1280x720 (Red)"),
        ("test_04.jpg", (3840, 2160), "purple", "Image 4: 3840x2160 (Purple)"),
    ]

    for filename, size, color, text in configs:
        img = Image.new("RGB", size, color=color)
        draw = ImageDraw.Draw(img)
        
        # グリッド描画
        w, h = size
        for x in range(0, w, 100):
            draw.line([(x, 0), (x, h)], fill="gray", width=1)
        for y in range(0, h, 100):
            draw.line([(0, y), (w, y)], fill="gray", width=1)
            
        # テキストと中心マーク描画
        cx, cy = w // 2, h // 2
        draw.line([(cx - 50, cy), (cx + 50, cy)], fill="yellow", width=5)
        draw.line([(cx, cy - 50), (cx, cy + 50)], fill="yellow", width=5)
        draw.rectangle([(cx - 200, cy - 100), (cx + 200, cy + 100)], outline="white", width=4)
        
        # 四隅に識別マーク
        draw.rectangle([(50, 50), (250, 250)], fill="yellow")
        draw.rectangle([(w - 250, 50), (w - 50, 250)], fill="cyan")
        draw.rectangle([(50, h - 250), (250, h - 50)], fill="magenta")
        draw.rectangle([(w - 250, h - 250), (w - 50, h - 50)], fill="orange")

        filepath = os.path.join(output_dir, filename)
        img.save(filepath)
        print(f"Created: {filepath}")

if __name__ == "__main__":
    create_test_images()
