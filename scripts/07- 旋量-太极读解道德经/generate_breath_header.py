#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成《呼吸的双重阴阳螺旋》文章头图
"""

import os
import requests

def generate_header_image():
    """生成头图"""
    
    # 主题相关的prompt
    prompt = """
    A mystical header image for an article about "Double Yin-Yang Spiral of Breath",
    featuring:
    1. Deep blue cosmic background with swirling energy patterns
    2. A glowing golden Tai Chi (Yin-Yang) symbol at the center
    3. Two interlocking spirals - one golden (yang) and one silver (yin)
    4. A silhouette of a person in meditative breathing pose
    5. Soft flowing energy waves representing breath
    6. Chinese calligraphy title "双重阴阳螺旋" in golden text
    7. Number "720°" elegantly incorporated
    8. Color scheme: deep blue, gold, silver, mystical atmosphere
    9. Professional book cover quality, 16:9 aspect ratio
    """
    
    # 清理prompt
    prompt = ' '.join(prompt.split())
    
    print(f"生成头图中...")
    
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
        
        output_path = r'e:\Trac Project\07- Spinor-Taiji model读解道德经\双重阴阳螺旋_头图.png'
        with open(output_path, 'wb') as f:
            f.write(img_response.content)
        
        file_size = os.path.getsize(output_path) / 1024
        print(f"\n✅ 头图生成成功！")
        print(f"📁 文件路径: {output_path}")
        print(f"📐 文件大小: {file_size:.2f} KB")
        print(f"🖼️ 分辨率: 2560×1440 (16:9)")
        
        # 更新HTML文件
        update_html(output_path)
        
        return output_path
        
    except Exception as e:
        print(f"❌ 头图生成失败: {e}")
        return None

def update_html(image_path):
    """更新HTML文件添加头图"""
    html_path = r'e:\Trac Project\07- Spinor-Taiji model读解道德经\双重阴阳螺旋_公众号版.html'
    
    if os.path.exists(html_path):
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 添加头图
        head_image_tag = f'<img src="双重阴阳螺旋_头图.png" alt="呼吸的双重阴阳螺旋" style="width:100%;border-radius:8px;margin-bottom:20px;">'
        
        if '<h1>' in content and head_image_tag not in content:
            content = content.replace('<h1>', head_image_tag + '\n<h1>')
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ HTML文件已更新头图引用")

if __name__ == '__main__':
    generate_header_image()
