#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为《“平方根”：从“空”到“色”的生成操作——深度读解》生成头图
主题：融合数学（平方根、旋量）与东方哲学（空、色、太极）
"""

import os
import sys
import requests
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from doubao_config import DOUBAO_API_KEY, DOUBAO_MODEL

API_KEY = DOUBAO_API_KEY
MODEL = DOUBAO_MODEL
BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"

# 保存目录
SAVE_DIR = Path(r"E:\Trac Project\02-文化自信\images\平方根深度读解_images")
SAVE_DIR.mkdir(parents=True, exist_ok=True)

DATE_STR = datetime.now().strftime('%Y%m%d')
FILENAME = f"cover_{DATE_STR}.jpg"
SAVE_PATH = SAVE_DIR / FILENAME


def generate_cover():
    print("\n" + "=" * 70)
    print("[任务] 为「平方根深度读解」生成头图")
    print("[主题] 从空到色的生成操作")
    print("[尺寸] 900×500像素")
    print("=" * 70)

    prompt = """
    【设计风格】
    高端学术风格，融合数学与东方哲学元素

    【核心视觉元素】
    1. 中心：数学平方根符号 √ 与太极图融合
       - 平方根符号穿过太极阴阳鱼
       - 体现"从空到色"的生成过程

    2. 左侧：复数域可视化
       - 实部（可见的色）与虚部（隐藏的空）
       - 虚数 i 符号
       - 旋量数学图形（720度旋转）

    3. 右侧：东方哲学元素
       - "色即是空，空即是色"经文
       - 量子波动线条
       - 粒子效果

    4. 背景：深邃星空渐变
       - 量子场论波形
       - 能量流动效果

    【配色方案】
    - 主色：深蓝 #1a237e（数学/科学感）
    - 辅色：金色 #c9a227（智慧）
    - 点缀：太极红 #8B1E22
    - 背景：深空蓝渐变

    【文字区域】
    - 底部预留标题区域
    - 标题："平方根"
    - 副标题：从"空"到"色"的生成操作

    【技术规格】
    - 尺寸：900×500像素
    - 比例：16:9
    - 模式：RGB
    - 分辨率：300dpi

    【整体风格】
    - 专业性与禅意融合
    - 数学与哲学完美结合
    - 构图平衡大气
    - 适合作为微信公众号文章封面
    """

    print(f"[路径] {SAVE_PATH}")
    print("\n[等待] 正在调用豆包AI生成图片...")

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
        response = requests.post(url, headers=headers, json=payload, timeout=180)

        if response.status_code == 200:
            result = response.json()
            print("[成功] 生成成功!")

            if 'data' in result and len(result['data']) > 0:
                image_url = result['data'][0].get('url', '')
                
                if image_url:
                    print("[下载] 正在下载图片...")
                    img_response = requests.get(image_url, timeout=60)
                    
                    if img_response.status_code == 200:
                        with open(SAVE_PATH, 'wb') as f:
                            f.write(img_response.content)
                        
                        file_size = os.path.getsize(SAVE_PATH)
                        
                        print("\n" + "=" * 70)
                        print("[成功] 头图生成完成!")
                        print(f"[文件] {FILENAME}")
                        print(f"[路径] {SAVE_PATH}")
                        print(f"[大小] {file_size / 1024:.2f} KB")
                        print("=" * 70)

                        return {
                            "success": True,
                            "path": str(SAVE_PATH),
                            "filename": FILENAME,
                            "size": file_size
                        }
                    else:
                        print(f"[失败] 下载失败: HTTP {img_response.status_code}")
                        return {"success": False, "error": "下载失败"}
                else:
                    print("[失败] 未获取到图片URL")
                    return {"success": False, "error": "未获取到图片URL"}
            else:
                print("[失败] 响应格式错误")
                return {"success": False, "error": "响应格式错误"}
        else:
            print(f"[失败] 生成失败: HTTP {response.status_code}")
            print(f"[错误] {response.text}")
            return {"success": False, "error": response.text}

    except Exception as e:
        print(f"[失败] 发生错误: {str(e)}")
        return {"success": False, "error": str(e)}


if __name__ == "__main__":
    result = generate_cover()
    
    print("\n" + "=" * 70)
    if result and result.get("success"):
        print("[完成] 任务完成!")
        print(f"[路径] {result.get('path')}")
    else:
        print("[失败] 任务失败")
        print(f"[错误] {result.get('error', '未知错误')}")
    print("=" * 70)
