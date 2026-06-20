#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调整图片尺寸到1200x630像素
"""

import sys
from pathlib import Path

def resize_image():
    try:
        from PIL import Image
    except ImportError:
        sys.stdout.write("Error: PIL/Pillow library not installed\n")
        sys.exit(1)
    
    input_path = Path(r"E:\Trac Project\04-伦理即内核\images\AI讨好现象及其风险_头图_2048x1800.png")
    output_path = Path(r"E:\Trac Project\04-伦理即内核\images\AI讨好现象及其风险_头图_1200x630.png")
    
    if not input_path.exists():
        sys.stdout.write("Input image not found\n")
        return
    
    sys.stdout.write("Resizing image to 1200x630...\n")
    
    try:
        with Image.open(input_path) as img:
            # 调整尺寸并保持比例
            img.thumbnail((1200, 630), Image.Resampling.LANCZOS)
            
            # 如果图像比例不对，添加背景
            if img.size[0] < 1200 or img.size[1] < 630:
                new_img = Image.new("RGB", (1200, 630), (30, 30, 30))
                x = (1200 - img.size[0]) // 2
                y = (630 - img.size[1]) // 2
                new_img.paste(img, (x, y))
                img = new_img
            
            img.save(output_path, "PNG", quality=95)
            sys.stdout.write("Resized image saved to: " + str(output_path) + "\n")
            
    except Exception as e:
        sys.stdout.write("Error resizing image: " + str(e) + "\n")

if __name__ == "__main__":
    resize_image()