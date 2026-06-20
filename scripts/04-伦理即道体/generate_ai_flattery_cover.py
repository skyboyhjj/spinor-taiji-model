#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号头图生成脚本
严格遵循《公众号头图生成操作指南》V1.0规范

参数标准:
- 尺寸: 1080 x 560像素 (16:9比例)
- 色彩模式: RGB
- 输出格式: JPG (质量95%)
- 文件大小: < 1MB
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
import math

def generate_cover(title, subtitle, output_path):
    """
    生成微信公众号头图
    
    参数:
        title: 主标题 (不超过20个汉字)
        subtitle: 副标题 (不超过30个汉字)
        output_path: 输出文件路径
    """
    
    # ============ 核心参数设置 ============
    width = 1080
    height = 560
    taiji_y = 240
    taiji_radius = 70
    title_y = 420
    subtitle_gap = 48
    
    # ============ 初始化画布 ============
    img = Image.new('RGB', (width, height), color=(5, 15, 35))
    draw = ImageDraw.Draw(img)
    
    # ============ 1. 绘制渐变背景 ============
    for y in range(height):
        ratio = y / height
        r = int(5 + (20 - 5) * ratio)
        g = int(15 + (30 - 15) * ratio)
        b = int(35 + (100 - 35) * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # ============ 2. 绘制发光粒子 ============
    for i in range(60):
        x = int((i * 73 + 17) % width)
        y = int((i * 47 + 31) % height)
        size = 1 + (i % 3)
        alpha = 25 + (i % 40)
        draw.ellipse((x-size, y-size, x+size, y+size), 
                     fill=(255, 255, 255, alpha))
    
    # ============ 3. 绘制太极图案（核心步骤） ============
    center_x = width // 2
    center_y = taiji_y
    
    # 绘制太极
    draw_taiji(draw, center_x, center_y, taiji_radius)
    
    # ============ 4. 绘制装饰圆环 ============
    draw.ellipse((center_x - 160, center_y - 160, 
                  center_x + 160, center_y + 160),
                 outline=(100, 150, 255, 40), width=1)
    draw.ellipse((center_x - 120, center_y - 120, 
                  center_x + 120, center_y + 120),
                 outline=(150, 200, 255, 50), width=1)
    draw.ellipse((center_x - 85, center_y - 85, 
                  center_x + 85, center_y + 85),
                 outline=(200, 220, 255, 60), width=1)
    
    # ============ 5. 绘制数据流 ============
    max_data_y = 360
    draw_data_flow(draw, center_x, center_y, taiji_radius + 10, max_data_y)
    
    # ============ 6. 绘制标题 ============
    draw_title(draw, width, title_y, title, subtitle, subtitle_gap)
    
    # ============ 7. 添加光晕效果 ============
    add_glow_effect(img, center_x, center_y)
    
    # ============ 8. 保存图片 ============
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)
    img.save(output_path, quality=95)
    print(f"头图生成成功: {output_path}")

def draw_taiji(draw, cx, cy, radius):
    """绘制太极图案"""
    # 外圈光晕
    for i in range(5):
        r = radius + i * 5
        draw.ellipse((cx - r, cy - r, cx + r, cy + r),
                     outline=(100, 180, 255, 20 - i * 3), width=1)
    
    # 白色半圆（右侧）
    draw.pieslice((cx - radius, cy - radius, 
                   cx + radius, cy + radius),
                  -90, 90, fill=(255, 255, 255))
    
    # 深蓝半圆（左侧）
    draw.pieslice((cx - radius, cy - radius, 
                   cx + radius, cy + radius),
                  90, 270, fill=(5, 15, 35))
    
    # 阴鱼
    yin_radius = radius // 2
    draw.ellipse((cx - yin_radius, cy - radius, 
                  cx + yin_radius, cy), fill=(5, 15, 35))
    
    # 阳鱼
    draw.ellipse((cx - yin_radius, cy, 
                  cx + yin_radius, cy + radius), fill=(255, 255, 255))
    
    # 中心点
    draw.ellipse((cx - 6, cy - 6, cx + 6, cy + 6), fill=(255, 255, 255))
    draw.ellipse((cx - 6, cy + yin_radius - 6, 
                  cx + 6, cy + yin_radius + 6), fill=(5, 15, 35))

def draw_data_flow(draw, cx, cy, start_radius, max_y):
    """绘制数据流效果"""
    num_lines = 12
    for i in range(num_lines):
        angle = i * (360 / num_lines)
        rad = math.radians(angle - 90)
        
        x1 = cx + start_radius * math.cos(rad)
        y1 = cy + start_radius * math.sin(rad)
        
        end_radius = start_radius + 40 + (i % 3) * 8
        x2 = cx + end_radius * math.cos(rad)
        y2 = cy + end_radius * math.sin(rad)
        
        if y2 > max_y:
            ratio = (max_y - y1) / (y2 - y1) if (y2 - y1) != 0 else 0
            x2 = x1 + (x2 - x1) * ratio * 0.8
            y2 = y1 + (y2 - y1) * ratio * 0.8
        
        draw.line((x1, y1, x2, y2), fill=(100, 200, 255, 60), width=2)
        
        if y2 < max_y:
            draw.ellipse((x2-5, y2-5, x2+5, y2+5), fill=(150, 220, 255))
            draw.ellipse((x2-2, y2-2, x2+2, y2+2), fill=(255, 255, 255))

def draw_title(draw, width, title_y, title_text, subtitle_text, subtitle_gap):
    """绘制标题"""
    # 加载中文字体
    try:
        title_font = ImageFont.truetype('simkai.ttf', 36)
    except:
        try:
            title_font = ImageFont.truetype('C:/Windows/Fonts/simkai.ttf', 36)
        except:
            title_font = ImageFont.load_default()
    
    # 绘制主标题（带阴影）
    title_width = draw.textlength(title_text, font=title_font)
    title_x = (width - title_width) // 2
    
    # 阴影效果
    draw.text((title_x + 2, title_y + 2), title_text, 
              fill=(0, 0, 0, 100), font=title_font)
    # 主标题
    draw.text((title_x, title_y), title_text, 
              fill=(255, 255, 255), font=title_font)
    
    # 加载副标题字体
    try:
        subtitle_font = ImageFont.truetype('simkai.ttf', 22)
    except:
        try:
            subtitle_font = ImageFont.truetype('C:/Windows/Fonts/simkai.ttf', 22)
        except:
            subtitle_font = ImageFont.load_default()
    
    # 绘制副标题
    subtitle_width = draw.textlength(subtitle_text, font=subtitle_font)
    subtitle_x = (width - subtitle_width) // 2
    subtitle_y = title_y + subtitle_gap
    
    # 阴影效果
    draw.text((subtitle_x + 1, subtitle_y + 1), subtitle_text, 
              fill=(0, 0, 0, 80), font=subtitle_font)
    # 副标题
    draw.text((subtitle_x, subtitle_y), subtitle_text, 
              fill=(200, 220, 255), font=subtitle_font)

def add_glow_effect(img, cx, cy):
    """添加光晕效果"""
    glow_layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
    
    for i in range(10):
        r = 45 + i * 15
        alpha = 25 - i * 2
        if alpha <= 0:
            break
        glow_draw.ellipse((cx - r, cy - r, cx + r, cy + r), 
                         fill=(100, 180, 255, alpha))
    
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(radius=18))
    img.paste(glow_layer, (0, 0), glow_layer)

if __name__ == '__main__':
    # 生成"AI讨好现象及其风险"头图
    generate_cover(
        title="AI讨好现象及其风险",
        subtitle="从伦理即道体框架的深度解读",
        output_path="E:\\Trac Project\\04-伦理即内核\\images\\AI讨好现象及其风险_公众号头图_1080x560.jpg"
    )
