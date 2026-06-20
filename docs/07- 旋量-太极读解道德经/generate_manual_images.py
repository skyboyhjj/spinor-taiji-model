#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为《道德经》操作手册文章生成配图
"""

import os
import sys
import requests
import json
from pathlib import Path

# 配置参数
API_KEY = "ark-bcdb4b90-cf05-490d-9bc6-d3586d06ffd5-6bfb7"
MODEL = "doubao-seedream-5-0-260128"
IMAGE_SIZE = "2560x1440"  # 16:9, 默认规范尺寸
OUTPUT_DIR = Path(r"E:\Trac Project\07- Spinor-Taiji model读解道德经")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 配图配置
IMAGE_CONFIGS = [
    {
        "id": "cover",
        "title": "封面图",
        "description": "《道德经》操作手册封面，体现宇宙动力与Spinor-Taiji model",
        "prompt": """Professional book cover design for Tao Te Ching interpretation. 
Central element: elegant Taiji yin-yang symbol with swirling energy patterns, representing the universe's intrinsic power. 
Deep space background with golden constellations and flowing energy waves. 
Traditional Chinese ink painting style blended with modern cosmic elements. 
Rich red (#8B1E22) and gold color scheme, ethereal and profound atmosphere. 
Book title area with classic Chinese calligraphy style. 
16:9 landscape composition, 2560x1440, cinematic lighting, ultra detailed."""
    },
    {
        "id": "vector_vs_spinor",
        "title": "矢量与旋量对比图",
        "description": "展示矢量态与旋量态的区别，配合文章第一部分",
        "prompt": """Abstract visualization comparing vector and spinor states in Taoist philosophy. 
Left side: rigid geometric arrows representing fixed vectors (chaotic, sharp edges, dark colors). 
Right side: flowing, swirling vortex representing spinor (fluid, harmonious, golden light). 
Central Taiji symbol connecting both sides. 
Traditional Chinese ink wash style with modern abstract elements. 
Deep blue to golden gradient background. 
16:9 landscape, 2560x1440, mystical atmosphere, professional quality."""
    },
    {
        "id": "mindfulness_field",
        "title": "觉知域图",
        "description": "展示安住觉知域的状态，配合文章第三部分",
        "prompt": """Serene visualization of mindful awareness field. 
A peaceful meditating figure sitting in the center of a vast, calm field of consciousness. 
Soft golden light emanating from the center, surrounded by gentle energy waves. 
Traditional Chinese landscape elements: mountains, mist, flowing water. 
Harmonious blend of inner peace and cosmic connection. 
16:9 landscape, 2560x1440, tranquil spiritual atmosphere, ethereal lighting."""
    }
]

def generate_image(prompt, size, output_path):
    """生成图片"""
    print(f"📸 正在生成: {output_path.name}")
    
    try:
        url = "https://ark.cn-beijing.volces.com/api/v3/images/generations"
        headers = {"Authorization": "Bearer " + API_KEY, "Content-Type": "application/json"}
        data = {"prompt": prompt, "model": MODEL, "size": size, "response_format": "url"}
        
        response = requests.post(url, headers=headers, data=json.dumps(data), timeout=120, verify=False)
        
        if response.status_code == 200:
            result = response.json()
            if "data" in result and len(result["data"]) > 0:
                image_url = result["data"][0].get("url")
                if image_url:
                    print(f"   ✅ 生成成功")
                    image_response = requests.get(image_url, timeout=60, verify=False)
                    with open(output_path, "wb") as f:
                        f.write(image_response.content)
                    print(f"   📥 已保存: {output_path}")
                    return image_url
        print(f"   ❌ 生成失败: {response.text[:200]}")
        return None
    except Exception as e:
        print(f"   ❌ 错误: {e}")
        return None

def update_html_with_images(html_path, images):
    """更新HTML中的图片引用"""
    print(f"\n📝 更新HTML文档")
    
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 添加封面图
    cover_img = f'''<div style="width:100%;max-width:900px;margin:0 auto 20px;">
        <img src="cover.png" alt="《道德经》操作手册" style="width:100%;height:auto;display:block;border-radius:8px;">
        <p style="text-align:center;font-size:12px;color:#999;margin-top:8px;">图：Spinor-Taiji model · 宇宙动力</p>
    </div>'''
    content = content.replace('<body>', '<body>\n' + cover_img)
    
    # 添加矢量与旋量对比图
    vector_img = f'''<div style="width:100%;max-width:900px;margin:20px auto;">
        <img src="vector_vs_spinor.png" alt="矢量与旋量" style="width:100%;height:auto;display:block;border-radius:8px;">
        <p style="text-align:center;font-size:12px;color:#999;margin-top:8px;">图：矢量态与旋量态的对比</p>
    </div>'''
    content = content.replace('### 二、第一步：识别状态', vector_img + '\n### 二、第一步：识别状态')
    
    # 添加觉知域图
    mindful_img = f'''<div style="width:100%;max-width:900px;margin:20px auto;">
        <img src="mindfulness_field.png" alt="觉知域" style="width:100%;height:auto;display:block;border-radius:8px;">
        <p style="text-align:center;font-size:12px;color:#999;margin-top:8px;">图：安住于觉知域</p>
    </div>'''
    content = content.replace('### 四、第三步：安住觉知域', mindful_img + '\n### 四、第三步：安住觉知域')
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("   ✅ HTML已更新")

def main():
    print("=" * 60)
    print("🎨 为《道德经》操作手册生成配图")
    print("=" * 60)
    
    generated_images = {}
    
    for config in IMAGE_CONFIGS:
        print(f"\n处理: {config['title']}")
        output_path = OUTPUT_DIR / f"{config['id']}.png"
        image_url = generate_image(config['prompt'], IMAGE_SIZE, output_path)
        if image_url:
            generated_images[config['id']] = {"url": image_url, "path": str(output_path)}
    
    # 更新HTML
    html_path = OUTPUT_DIR / "道德经操作手册_公众号专业版.html"
    if html_path.exists():
        update_html_with_images(html_path, generated_images)
    
    print("\n" + "=" * 60)
    print("✅ 配图生成完成!")
    for img_id, info in generated_images.items():
        print(f"📌 {info['path']}")
    print("=" * 60)

if __name__ == "__main__":
    main()
