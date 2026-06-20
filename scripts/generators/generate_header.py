#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成《道德经》操作手册系列头图
参考图风格：星空背景、太极符号、阅读地图、冥想元素
"""

import os
import sys
import requests

def generate_header_image():
    """生成头图"""
    
    # 根据参考图设计的prompt
    prompt = """
    A mystical header image for a Tao Te Ching operations manual series, 
    featuring:
    1. Deep blue starry night sky background with twinkling stars and cosmic dust
    2. Glowing golden Tai Chi (Yin-Yang) symbol floating in the center top
    3. An ancient parchment-style reading map spread open below the Tai Chi, 
       showing multiple paths (Path A, Path B, Path C) converging to a central compass
    4. A silhouette of a meditating person in lotus position at the bottom center
    5. Soft golden light rays emanating from the center
    6. Traditional Chinese calligraphy style title "道德经操作手册" in golden text
    7. Flowing energy waves around the map and meditator
    8. Color scheme: deep blue background, golden accents, mystical atmosphere
    9. Professional book cover quality, 16:9 aspect ratio
    """
    
    # 清理prompt
    prompt = ' '.join(prompt.split())
    
    print(f"生成头图中...")
    print(f"Prompt: {prompt[:100]}...")
    
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
        
        output_path = r'e:\Trac Project\07- Spinor-Taiji model读解道德经\阅读地图头图.png'
        with open(output_path, 'wb') as f:
            f.write(img_response.content)
        
        file_size = os.path.getsize(output_path) / 1024
        print(f"\n✅ 头图生成成功！")
        print(f"📁 文件路径: {output_path}")
        print(f"📐 文件大小: {file_size:.2f} KB")
        print(f"🖼️ 分辨率: 2560×1440 (16:9)")
        
        return output_path
        
    except Exception as e:
        print(f"❌ 头图生成失败: {e}")
        # 使用备用方法
        return fallback_generate(prompt)

def fallback_generate(prompt):
    """备用生成方法"""
    print("使用备用方法生成头图...")
    
    # 使用Trae内置API
    import urllib.request
    import urllib.parse
    
    encoded_prompt = urllib.parse.quote(prompt)
    image_url = f'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt={encoded_prompt}&image_size=landscape_16_9'
    
    try:
        req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req, timeout=120)
        image_data = response.read()
        
        output_path = r'e:\Trac Project\07- Spinor-Taiji model读解道德经\阅读地图头图.png'
        with open(output_path, 'wb') as f:
            f.write(image_data)
        
        file_size = os.path.getsize(output_path) / 1024
        print(f"\n✅ 备用方法生成成功！")
        print(f"📁 文件路径: {output_path}")
        print(f"📐 文件大小: {file_size:.2f} KB")
        
        return output_path
        
    except Exception as e:
        print(f"❌ 备用方法也失败: {e}")
        return None

def main():
    output_path = generate_header_image()
    
    if output_path:
        # 更新HTML文件中的头图引用
        html_path = r'e:\Trac Project\07- Spinor-Taiji model读解道德经\道德经操作手册系列_阅读地图与实修指南_公众号版.html'
        if os.path.exists(html_path):
            with open(html_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 添加头图引用
            head_image_tag = f'<img src="阅读地图头图.png" alt="道德经操作手册系列" style="width:100%;border-radius:8px;margin-bottom:20px;">'
            if '<h1>' in content and head_image_tag not in content:
                content = content.replace('<h1>', head_image_tag + '\n<h1>')
                with open(html_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ HTML文件已更新头图引用")

if __name__ == '__main__':
    main()
