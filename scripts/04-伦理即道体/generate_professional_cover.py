#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重新生成AI讨好现象头图
确保无黑色边框，符合项目设计规范
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
import math

def generate_professional_cover():
    """
    生成专业的公众号头图
    主题：AI讨好现象及其风险
    风格：符合"伦理即道体"项目的设计规范
    """
    
    # 规范参数
    width = 1080
    height = 560
    
    # 初始化画布 - 使用渐变背景而非黑色
    img = Image.new('RGB', (width, height), color=(10, 15, 35))
    draw = ImageDraw.Draw(img)
    
    # ============ 1. 创建渐变背景 ============
    # 从深蓝到深红的渐变（呼应项目主色调）
    for y in range(height):
        ratio = y / height
        # 渐变色彩
        r = int(10 + (139 - 10) * ratio)  # 10 → 139 (深红)
        g = int(15 + (30 - 15) * ratio)    # 15 → 30
        b = int(35 + (34 - 35) * ratio)    # 35 → 34
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # ============ 2. 绘制AI讨好主题的视觉元素 ============
    center_x = width // 2
    center_y = height // 2 - 20
    
    # 绘制太极元素（呼应"伦理即道体"）
    draw_taiji(draw, center_x - 200, center_y, 60)
    
    # 绘制机器人/AI元素（代表AI讨好）
    draw_ai_figure(draw, center_x + 100, center_y)
    
    # 绘制连接线/数据流
    draw_data_connection(draw, center_x - 100, center_y, center_x + 200, center_y)
    
    # ============ 3. 添加警示元素 ============
    draw_warning_icons(draw, width, height)
    
    # ============ 4. 添加发光粒子效果 ============
    add_light_particles(draw, width, height)
    
    # ============ 5. 绘制标题和副标题 ============
    draw_titles(draw, width, height)
    
    # ============ 6. 保存最终图片 ============
    output_path = Path(r"E:\Trac Project\04-伦理即内核\images\AI讨好现象及其风险_公众号头图_1080x560_final.jpg")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 保存高质量JPG
    img.save(output_path, "JPEG", quality=95, optimize=True)
    
    print(f"头图生成成功: {output_path}")
    return str(output_path)

def draw_taiji(draw, x, y, radius):
    """绘制太极元素"""
    # 外圆
    draw.ellipse((x - radius, y - radius, x + radius, y + radius),
                 outline=(200, 200, 255, 100), width=2)
    
    # 太极基本元素（简化版）
    # 白色半圆
    draw.pieslice((x - radius, y - radius, x + radius, y + radius),
                  -90, 90, fill=(255, 255, 255, 200))
    # 深色半圆
    draw.pieslice((x - radius, y - radius, x + radius, y + radius),
                  90, 270, fill=(139, 30, 34, 200))
    
    # 中心点
    draw.ellipse((x - 4, y - 4, x + 4, y + 4), fill=(255, 255, 255))

def draw_ai_figure(draw, x, y):
    """绘制AI元素 - 代表讨好的机器人"""
    # 圆形头部
    head_radius = 50
    draw.ellipse((x - head_radius, y - head_radius, 
                  x + head_radius, y + head_radius),
                 outline=(180, 200, 255), width=3)
    
    # 眼睛 - 友好的笑脸
    eye_offset = 15
    eye_y = y - 10
    draw.ellipse((x - eye_offset - 8, eye_y - 8, 
                  x - eye_offset + 8, eye_y + 8),
                 fill=(200, 220, 255))
    draw.ellipse((x + eye_offset - 8, eye_y - 8, 
                  x + eye_offset + 8, eye_y + 8),
                 fill=(200, 220, 255))
    
    # 微笑
    draw.arc((x - 20, y + 5, x + 20, y + 25),
             0, 180, fill=(180, 200, 255), width=3)
    
    # 身体/发光效果
    body_x1, body_y1 = x - 30, y + head_radius + 10
    body_x2, body_y2 = x + 30, y + head_radius + 60
    draw.rectangle((body_x1, body_y1, body_x2, body_y2),
                   outline=(150, 180, 255), width=2)

def draw_data_connection(draw, x1, y1, x2, y2):
    """绘制连接线条"""
    # 主要线条
    draw.line((x1, y1, x2, y2), fill=(100, 180, 255, 150), width=3)
    
    # 数据点
    for i in range(5):
        t = i / 4
        px = x1 + (x2 - x1) * t
        py = y1 + (y2 - y1) * t
        
        if i % 2 == 0:
            # 亮色数据点
            draw.ellipse((px - 6, py - 6, px + 6, py + 6),
                         fill=(200, 220, 255))
        else:
            # 暗色数据点
            draw.ellipse((px - 4, py - 4, px + 4, py + 4),
                         fill=(139, 30, 34))

def draw_warning_icons(draw, width, height):
    """绘制警示元素"""
    # 四个角落的小警示符号
    positions = [
        (100, 80),
        (width - 100, 80),
        (100, height - 80),
        (width - 100, height - 80)
    ]
    
    for (x, y) in positions:
        # 三角警示
        points = [(x, y - 12), (x - 12, y + 8), (x + 12, y + 8)]
        draw.polygon(points, outline=(255, 180, 100, 180), width=2)

def add_light_particles(draw, width, height):
    """添加发光粒子效果"""
    import random
    random.seed(42)  # 固定种子保证可重现
    
    for i in range(40):
        x = random.randint(20, width - 20)
        y = random.randint(20, height - 20)
        size = random.randint(1, 3)
        
        # 随机发光颜色
        r = 150 + random.randint(0, 105)
        g = 180 + random.randint(0, 75)
        b = 220 + random.randint(0, 35)
        
        draw.ellipse((x - size, y - size, x + size, y + size),
                     fill=(r, g, b, random.randint(30, 80)))

def draw_titles(draw, width, height):
    """绘制标题文字"""
    # 尝试加载中文字体
    fonts = [
        'simkai.ttf',
        'simhei.ttf',
        'msyh.ttf',
        'C:/Windows/Fonts/simkai.ttf',
        'C:/Windows/Fonts/simhei.ttf'
    ]
    
    title_font = None
    subtitle_font = None
    
    for font_path in fonts:
        try:
            if title_font is None:
                title_font = ImageFont.truetype(font_path, 44)
                subtitle_font = ImageFont.truetype(font_path, 24)
            break
        except:
            continue
    
    if title_font is None:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
    
    # 主标题
    title_text = "AI讨好现象及其风险"
    title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (width - title_width) // 2
    title_y = height - 120
    
    # 主标题阴影
    draw.text((title_x + 2, title_y + 2), title_text,
              fill=(0, 0, 0, 100), font=title_font)
    # 主标题
    draw.text((title_x, title_y), title_text,
              fill=(255, 255, 255), font=title_font)
    
    # 副标题
    subtitle_text = "从伦理即道体框架的深度解读"
    subtitle_bbox = draw.textbbox((0, 0), subtitle_text, font=subtitle_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    subtitle_x = (width - subtitle_width) // 2
    subtitle_y = title_y + 55
    
    # 副标题阴影
    draw.text((subtitle_x + 1, subtitle_y + 1), subtitle_text,
              fill=(0, 0, 0, 80), font=subtitle_font)
    # 副标题
    draw.text((subtitle_x, subtitle_y), subtitle_text,
              fill=(220, 200, 255), font=subtitle_font)

if __name__ == '__main__':
    generate_professional_cover()
