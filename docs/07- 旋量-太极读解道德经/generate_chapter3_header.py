#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为第三章生成公众号头图
"""

import os
import sys
import requests
import json
from pathlib import Path

# 配置参数
API_KEY = "ark-bcdb4b90-cf05-490d-9bc6-d3586d06ffd5-6bfb7"
MODEL = "doubao-seedream-5-0-260128"
IMAGE_SIZE = "2560x1440"  # 16:9
OUTPUT_DIR = Path(r"E:\Trac Project\07- Spinor-Taiji model读解道德经")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def generate_image(prompt, size, output_path):
    """生成图片"""
    print(f"📸 正在生成头图: {output_path.name}")
    
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
                    file_size = os.path.getsize(output_path) / 1024
                    print(f"   📥 已保存: {output_path} ({file_size:.2f} KB)")
                    return image_url
        print(f"   ❌ 生成失败: {response.text[:200]}")
        return None
    except Exception as e:
        print(f"   ❌ 错误: {e}")
        return None

def update_html_with_header():
    """更新HTML文件中的头图引用"""
    html_path = OUTPUT_DIR / "第三章_操作手册的核心架构_公众号版.html"
    if html_path.exists():
        print("\n📝 更新HTML文档中的头图引用...")
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 添加头图
        header_img = f'''<div style="width:100%;max-width:900px;margin:0 auto 20px;">
            <img src="chapter3_header.png" alt="操作手册的核心架构" style="width:100%;height:auto;display:block;border-radius:8px;">
            <p style="text-align:center;font-size:12px;color:#999;margin-top:8px;">图：三步法操作框架 · Spinor-Taiji model</p>
        </div>'''
        
        content = content.replace('<body>', '<body>\n' + header_img)
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("   ✅ HTML已更新")

def main():
    print("=" * 60)
    print("🎨 为第三章生成公众号头图")
    print("=" * 60)
    
    # 头图设计prompt
    prompt = """Professional WeChat official account header image for Taoist philosophy article titled "操作手册的核心架构". 
Central theme: three-step operation framework (recognize state -> apply principle -> abide in awareness). 
Visual elements: 
- Three interconnected circles representing the three steps
- Elegant Taiji yin-yang symbol at the center
- Flowing arrows showing the cyclic process
- Traditional Chinese ink painting style with modern minimalist design
- Deep blue and gold color scheme representing wisdom and structure
- Subtle geometric patterns representing the operation framework
- Calligraphy-style title in elegant Chinese characters
- Soft gradient background from deep blue to light gold
- Professional, academic yet accessible atmosphere
- 16:9 landscape composition, cinematic quality, ultra detailed."""
    
    output_path = OUTPUT_DIR / "chapter3_header.png"
    image_url = generate_image(prompt, IMAGE_SIZE, output_path)
    
    if image_url:
        print("\n" + "=" * 60)
        print("✅ 头图生成完成!")
        print(f"📌 文件路径: {output_path}")
        print(f"📐 尺寸: {IMAGE_SIZE}")
        print("=" * 60)
        
        update_html_with_header()
    else:
        print("\n❌ 头图生成失败")

if __name__ == "__main__":
    main()
