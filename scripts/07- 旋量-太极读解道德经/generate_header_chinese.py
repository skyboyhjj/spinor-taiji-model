#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成全中文的《道德经》操作手册系列头图
"""

import os
import requests

def generate_chinese_header_image():
    """生成全中文头图"""
    
    # 全中文prompt
    prompt = """
    神秘的《道德经》操作手册系列头图，包含以下元素：
    1. 深蓝色星空背景，带有闪烁的星星和宇宙尘埃
    2. 金色发光的太极阴阳符号，悬浮在顶部中央
    3. 古老羊皮纸风格的阅读地图铺开展示，地图上标注"路径A：系统学习"、"路径B：从痛点切入"、"路径C：从兴趣切入"，汇聚到中央罗盘
    4. 底部中央有一个莲花坐姿的冥想者剪影
    5. 从中心散发柔和的金色光芒
    6. 金色书法风格标题"道德经操作手册系列"
    7. 地图和冥想者周围有流动的能量波纹
    8. 配色方案：深蓝色背景，金色点缀，神秘哲学氛围
    9. 专业书籍封面品质，16:9宽高比
    """
    
    # 清理prompt
    prompt = ' '.join(prompt.split())
    
    print(f"生成全中文头图中...")
    
    # 使用指定的API配置
    API_KEY = "ark-bcdb4b90-cf05-490d-9bc6-d3586d06ffd5-6bfb7"
    MODEL = "doubao-seedream-5-0-260128"
    
    url = "https://ark.cn-beijing.volces.com/api/v3/images/generations"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "prompt": prompt,
        "model": MODEL,
        "size": "2560x1440",
        "quality": "high"
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=120, verify=False)
        response.raise_for_status()
        
        result = response.json()
        image_url = result['data'][0]['url']
        
        print(f"图片生成成功: {image_url}")
        
        # 下载图片
        img_response = requests.get(image_url, timeout=60, verify=False)
        img_response.raise_for_status()
        
        output_path = r'e:\Trac Project\07- Spinor-Taiji model读解道德经\阅读地图头图_中文版.png'
        with open(output_path, 'wb') as f:
            f.write(img_response.content)
        
        file_size = os.path.getsize(output_path) / 1024
        print(f"\n✅ 全中文头图生成成功！")
        print(f"📁 文件路径: {output_path}")
        print(f"📐 文件大小: {file_size:.2f} KB")
        print(f"🖼️ 分辨率: 2560×1440 (16:9)")
        
        return output_path
        
    except Exception as e:
        print(f"❌ 头图生成失败: {e}")
        return None

def main():
    output_path = generate_chinese_header_image()
    
    if output_path:
        print("\n后续所有交互将优先使用中文进行沟通。")

if __name__ == '__main__':
    main()
