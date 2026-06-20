#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为《当下：理入与行入》生成头图
"""

import os
import requests

def generate_header_image():
    """生成符合要求的头图"""
    
    prompt = """
    A mystical and serene header image for an article about "The Present Moment" in Tao Te Ching philosophy,
    featuring:
    1. Deep cosmic blue and purple gradient background with subtle starfield
    2. A glowing golden Tai Chi (Yin-Yang) symbol floating in center
    3. Soft flowing energy waves representing breath/vibration
    4. Three concentric circles representing the "Three Breaths" practice
    5. A meditating figure silhouette at the bottom center
    6. Chinese calligraphy "当下" (Present Moment) in elegant golden font
    7. Subtle light rays emanating from the center
    8. Color scheme: deep blue, purple, gold, with white highlights
    9. Professional book cover quality, mystical atmosphere, 16:9 aspect ratio
    10. Smooth transitions between light and shadow, creating depth and dimension
    """
    
    prompt = ' '.join(prompt.split())
    
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
        
        img_response = requests.get(image_url, timeout=60, verify=False)
        img_response.raise_for_status()
        
        output_path = r'e:\Trac Project\10-时空\当下_头图.png'
        with open(output_path, 'wb') as f:
            f.write(img_response.content)
        
        file_size = os.path.getsize(output_path) / 1024
        
        print("✅ 头图生成成功！")
        print(f"📁 文件路径: {output_path}")
        print(f"📐 文件大小: {file_size:.2f} KB")
        print(f"🖼️ 分辨率: 2560×1440 (16:9)")
        
        if file_size > 2048:
            print("⚠️ 文件大小超过2MB，建议优化")
        
        return output_path
        
    except Exception as e:
        print(f"❌ 头图生成失败: {e}")
        return None

if __name__ == '__main__':
    generate_header_image()
