#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为"Spinor-Taiji model"模型中"看山三境界"文章生成头图
使用豆包AI图片生成

文章：《"Spinor-Taiji model"模型中，"看山三境界"》
主题：融合量子物理与东方智慧，体现"看山三境界"递进式构图
"""

import os
import sys
import requests
import json
from pathlib import Path
from datetime import datetime

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from doubao_config import DOUBAO_API_KEY, DOUBAO_MODEL

# 配置参数
API_KEY = DOUBAO_API_KEY
MODEL = DOUBAO_MODEL
BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"

# 保存目录
SAVE_DIR = Path(r"E:\Trac Project\02-文化自信\images\Spinor-Taiji model模型中'看山三境界'")
SAVE_DIR.mkdir(parents=True, exist_ok=True)

# 生成文件名：标题+日期
DATE_STR = datetime.now().strftime('%Y%m%d')
FILENAME = f"cover_{DATE_STR}.jpg"
SAVE_PATH = SAVE_DIR / FILENAME


def generate_cover_image():
    """
    生成"看山三境界"头图

    设计理念：
    1. 中心：太极图，代表"道"的本源
    2. 左区：具象山峰（第一境界：看山是山）
    3. 中区：旋量数学图形（第二境界：看山不是山）
    4. 右区：抽象山峰轮廓（第三境界：看山还是山）
    5. 背景：量子场论波形，体现科技感
    6. 预留标题区域在底部
    """

    print("\n[开始] 生成「看山三境界」头图")
    print("=" * 70)
    print(f"[文章] 《\"Spinor-Taiji model\"模型中，\"看山三境界\"》")
    print(f"[尺寸] 目标: 1200x630像素 (16:9)")
    print(f"[路径] {SAVE_PATH}")
    print("=" * 70 + "\n")

    # 图片生成提示词
    prompt = """
    【设计风格】
    高端学术风格，融合量子物理与东方哲学元素

    【核心视觉元素 - 三层递进构图】
    1. 左区（第一境界）：具象山峰，坚实厚重
       - 象征"看山是山"
       - 对应"矢量/色/正题"
       - 代表对现象世界的完全认同

    2. 中区（第二境界）：旋量数学图形
       - 720度旋转的旋量矢量场
       - 象征"看山不是山"
       - 对应"旋量/空/反题"
       - 代表穿透现象看到背后的振动源头

    3. 右区（第三境界）：抽象山峰剪影，光芒万丈
       - 象征"看山还是山"
       - 对应"觉知/阴阳和合"
       - 代表否定之否定后的螺旋回归

    4. 中心焦点：太极图与旋量融合
       - 阴阳鱼相互环绕旋转
       - 量子粒子围绕飞行
       - 代表"道生万物"的生成过程

    5. 背景：
       - 量子场论波形与粒子效果
       - 星空深邃渐变
       - 科学性与禅意完美融合

    【配色方案】
    - 主色：深蓝 #1a237e（科技感）
    - 辅色：金色 #c9a227（智慧）
    - 点缀：太极红 #8B1E22（传统文化）
    - 背景：深空蓝渐变

    【文字区域】
    - 底部预留20%空间作为标题区域
    - 半透明深色背景
    - 标题："看山三境界"
    - 副标题："Spinor-Taiji model"模型解读

    【技术规格】
    - 尺寸：1200×630像素
    - 比例：16:9
    - 模式：RGB
    - 分辨率：300dpi

    【整体风格】
    - 专业性与禅意融合
    - 科技感与传统文化结合
    - 构图平衡大气，留白得当
    - 适合作为微信公众号文章封面
    - 传达从"数学"到"觉悟"的升维之旅
    """

    print("[提示] 正在调用豆包AI生成图片...")
    print(f"   模型: {MODEL}\n")

    # API调用
    url = f"{BASE_URL}/images/generations"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "prompt": prompt.strip(),
        "size": "2K",
        "n": 1
    }

    try:
        print("[等待] 正在生成中，请稍候...")
        response = requests.post(url, headers=headers, json=payload, timeout=180)

        if response.status_code == 200:
            result = response.json()
            print("\n[成功] 生成成功!\n")

            # 获取图片URL
            if 'data' in result and len(result['data']) > 0:
                image_url = result['data'][0].get('url', '')

                if image_url:
                    print("[下载] 正在下载图片...")

                    # 下载图片
                    img_response = requests.get(image_url, timeout=60)

                    if img_response.status_code == 200:
                        # 保存图片
                        with open(SAVE_PATH, 'wb') as f:
                            f.write(img_response.content)

                        # 获取文件大小
                        file_size = os.path.getsize(SAVE_PATH)

                        print("\n" + "=" * 70)
                        print("[成功] 头图生成并保存成功!")
                        print("=" * 70)
                        print(f"[文件名] {FILENAME}")
                        print(f"[路径] {SAVE_PATH}")
                        print(f"[尺寸] 1200x630像素")
                        print(f"[大小] {file_size / 1024:.2f} KB")
                        print(f"[格式] JPG")
                        url_short = image_url[:50] + "..." if len(image_url) > 50 else image_url
                        print(f"[URL] {url_short}")
                        print("=" * 70 + "\n")

                        return {
                            "success": True,
                            "path": str(SAVE_PATH),
                            "filename": FILENAME,
                            "size": file_size,
                            "url": image_url
                        }
                    else:
                        print(f"\n[失败] 下载失败: HTTP {img_response.status_code}")
                        return {"success": False, "error": "下载失败"}
                else:
                    print("\n[失败] 未获取到图片URL")
                    print(f"[响应] {json.dumps(result, ensure_ascii=False, indent=2)}")
                    return {"success": False, "error": "未获取到图片URL"}
            else:
                print("\n[失败] 响应格式错误")
                print(f"[响应] {json.dumps(result, ensure_ascii=False, indent=2)}")
                return {"success": False, "error": "响应格式错误"}

        else:
            print(f"\n[失败] 生成失败: HTTP {response.status_code}")
            print(f"[错误] {response.text}")
            return {"success": False, "error": response.text}

    except requests.exceptions.Timeout:
        print("\n[失败] 请求超时，请检查网络连接后重试")
        return {"success": False, "error": "请求超时"}

    except requests.exceptions.ConnectionError:
        print("\n[失败] 网络连接失败，请检查网络设置")
        return {"success": False, "error": "网络连接失败"}

    except Exception as e:
        print(f"\n[失败] 发生未知错误: {str(e)}")
        return {"success": False, "error": str(e)}


def create_placeholder():
    """
    如果API生成失败，创建一个占位符图像
    """
    try:
        from PIL import Image, ImageDraw, ImageFont

        # 创建图像
        width, height = 1200, 630
        img = Image.new('RGB', (width, height), color=(26, 35, 126))  # 深蓝色背景
        draw = ImageDraw.Draw(img)

        # 绘制太极图
        center_x, center_y = width // 2, height // 2 - 50
        radius = 120

        # 外圆
        draw.ellipse(
            [center_x - radius, center_y - radius,
             center_x + radius, center_y + radius],
            outline=(201, 162, 39),  # 金色边框
            width=3
        )

        # 标题区域背景
        title_y = height - 100
        draw.rectangle(
            [0, title_y, width, height],
            fill=(0, 0, 0, 180)  # 半透明黑色
        )

        # 添加标题文字
        try:
            font_large = ImageFont.truetype("arial.ttf", 56)
            font_small = ImageFont.truetype("arial.ttf", 28)
        except:
            font_large = ImageFont.load_default()
            font_small = font_large

        # 主标题
        draw.text(
            (width // 2, title_y + 35),
            "看山三境界",
            fill=(255, 255, 255),
            font=font_large,
            anchor='mm'
        )

        # 副标题
        draw.text(
            (width // 2, title_y + 80),
            '"Spinor-Taiji model"模型解读',
            fill=(201, 162, 39),
            font=font_small,
            anchor='mm'
        )

        # 保存图像
        img.save(SAVE_PATH, 'JPEG', quality=95)

        print("\n[警告] 豆包API不可用，已创建占位符图像")
        print(f"[路径] {SAVE_PATH}")

        return {
            "success": True,
            "path": str(SAVE_PATH),
            "filename": FILENAME,
            "note": "占位符图像"
        }

    except ImportError:
        print("\n[失败] PIL库不可用，无法创建占位符图像")
        return {"success": False, "error": "PIL库不可用"}


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("\n[任务] 为「看山三境界」生成头图")
    print("[主题] \"Spinor-Taiji model\"模型与\"看山三境界\"")
    print("[尺寸] 1200x630像素\n")

    # 生成头图
    result = generate_cover_image()

    # 如果失败，尝试创建占位符
    if not result or not result.get("success"):
        print("\n[重试] 尝试创建占位符图像...")
        result = create_placeholder()

    # 输出最终结果
    print("\n" + "=" * 70)
    if result and result.get("success"):
        print("[完成] 任务完成!")
        print(f"[路径] 头图已保存至: {result.get('path')}")
        if result.get('size'):
            print(f"[大小] 文件大小: {result.get('size') / 1024:.2f} KB")
    else:
        print("[失败] 任务失败")
        print(f"[错误] {result.get('error', '未知错误')}")
    print("=" * 70 + "\n")
