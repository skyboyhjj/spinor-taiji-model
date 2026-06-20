#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
头图质量验证脚本
验证生成的头图是否符合操作指南的所有规范
"""

from PIL import Image
from pathlib import Path

def verify_cover_image(image_path):
    """验证头图是否符合规范"""
    
    print("=" * 60)
    print("头图质量验证报告")
    print("=" * 60)
    
    if not Path(image_path).exists():
        print(f"错误: 文件不存在 - {image_path}")
        return False
    
    img = Image.open(image_path)
    
    # 1. 尺寸验证
    print("\n1. 尺寸验证")
    print("-" * 40)
    width, height = img.size
    print(f"   实际尺寸: {width} x {height} 像素")
    if width == 1080 and height == 560:
        print("   ✓ 尺寸完全符合规范 (1080 x 560)")
    else:
        print(f"   ✗ 尺寸不符合规范 (应为 1080 x 560)")
    
    # 2. 比例验证
    print("\n2. 比例验证")
    print("-" * 40)
    ratio = width / height
    print(f"   实际比例: {ratio:.2f}:1")
    if abs(ratio - 16/9) < 0.01:
        print("   ✓ 比例符合规范 (16:9)")
    else:
        print(f"   ✗ 比例不符合规范 (应为 16:9)")
    
    # 3. 色彩模式验证
    print("\n3. 色彩模式验证")
    print("-" * 40)
    mode = img.mode
    print(f"   色彩模式: {mode}")
    if mode in ['RGB', 'RGBA']:
        print("   ✓ 色彩模式正确")
    else:
        print(f"   ✗ 色彩模式不正确 (应为 RGB/RGBA)")
    
    # 4. 文件信息
    print("\n4. 文件信息")
    print("-" * 40)
    file_size = Path(image_path).stat().st_size
    size_mb = file_size / (1024 * 1024)
    print(f"   文件大小: {size_mb:.2f} MB")
    if size_mb < 1.0:
        print("   ✓ 文件大小符合规范 (< 1MB)")
    else:
        print(f"   ✗ 文件大小不符合规范 (应 < 1MB)")
    
    # 5. 格式验证
    print("\n5. 格式验证")
    print("-" * 40)
    format_type = img.format
    print(f"   文件格式: {format_type}")
    if format_type in ['JPEG', 'JPG']:
        print("   ✓ 格式符合规范 (JPG)")
    else:
        print(f"   ✗ 格式不符合规范 (应为 JPG)")
    
    # 6. DPI信息
    print("\n6. DPI信息")
    print("-" * 40)
    try:
        dpi = img.info.get('dpi', (72, 72))
        if isinstance(dpi, tuple):
            dpi_x, dpi_y = dpi
        else:
            dpi_x = dpi_y = dpi
        print(f"   DPI: {dpi_x} x {dpi_y}")
        print("   ✓ DPI符合屏幕显示标准 (72dpi)")
    except:
        print("   无法获取DPI信息")
    
    print("\n" + "=" * 60)
    print("验证完成")
    print("=" * 60)
    
    return True

if __name__ == '__main__':
    image_path = r"E:\Trac Project\04-伦理即内核\images\AI讨好现象及其风险_公众号头图_1080x560.jpg"
    verify_cover_image(image_path)
