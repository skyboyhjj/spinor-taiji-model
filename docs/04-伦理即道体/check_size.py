#!/usr/bin/env python3
import sys
from PIL import Image

def check_image_size(image_path):
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            print(f"{width}x{height}")
            return width == 1080 and height == 560
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == '__main__':
    image_path = r"E:\Trac Project\04-伦理即内核\images\AI讨好现象及其风险_公众号头图_1080x560_v2.jpg"
    check_image_size(image_path)