#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用doubao-seedream API生成《有死地到无死地_以欲为量尺》头图
完全参考 generate_daodejing_images.py 的实现方式
"""

import os
import sys
import requests
import json
from pathlib import Path

# ==================== 配置参数（完全参考 generate_daodejing_images.py）====================
API_KEY = "ark-bcdb4b90-cf05-490d-9bc6-d3586d06ffd5-6bfb7"
MODEL = "doubao-seedream-5-0-260128"

# 输出目录
OUTPUT_DIR = Path(r"E:\Trac Project\07- Spinor-Taiji model读解道德经")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ==================== 图片尺寸规范 ====================
# 【默认规范】微信公众号文章插图默认尺寸：2560×1440像素（16:9宽高比）
# 此尺寸满足API最小像素要求（3,686,400像素），保证最佳显示效果
HEADER_SIZE = "2560x1440"  # 16:9, 默认规范尺寸

# ==================== 头图配置 ====================
HEADER_CONFIG = {
    "id": "wusidi_header_new",
    "title": "有死地到无死地_头图",
    "description": "配合《从有死地到无死地：以欲为量尺》文章头图",
    "prompt": """Professional Chinese philosophical artwork for WeChat official account header image. 
16:9 landscape composition, 1080x560 resolution. Central element: elegant Taiji (yin-yang) symbol with soft breathing light rays emanating from center, representing life's ebb and flow. 
Left side: dark turbulent waves (symbolizing 'death ground'), transitioning smoothly into calm water on the right (symbolizing 'no death ground'). 
Golden measuring scale crossing diagonally, connecting the two realms. Traditional Chinese ink painting style with modern minimalist elements. 
Deep red (#8B1E22) and gold color scheme, serene yet profound atmosphere. Clean background suitable for text overlay. 
High resolution professional quality, cinematic lighting, spiritual tranquility.""",
    "size": HEADER_SIZE
}

# ==================== 核心函数 ====================

def generate_image(prompt, size, output_path):
    """
    使用API生成图片（完全参考 generate_daodejing_images.py）
    :param prompt: 图片生成提示词
    :param size: 图片尺寸
    :param output_path: 输出路径
    :return: 图片URL或None
    """
    sys.stdout.write(f"📸 正在生成图片: {output_path.name}\n")
    sys.stdout.write(f"   尺寸: {size}\n")
    sys.stdout.write(f"   模型: {MODEL}\n")
    
    try:
        url = "https://ark.cn-beijing.volces.com/api/v3/images/generations"
        
        headers = {
            "Authorization": "Bearer " + API_KEY,
            "Content-Type": "application/json"
        }
        
        data = {
            "prompt": prompt,
            "model": MODEL,
            "size": size,
            "response_format": "url"
        }
        
        sys.stdout.write(f"   正在请求API...\n")
        response = requests.post(url, headers=headers, data=json.dumps(data), timeout=120, verify=False)
        
        sys.stdout.write(f"   响应状态: {response.status_code}\n")
        
        if response.status_code == 200:
            result = response.json()
            
            if "data" in result and isinstance(result["data"], list) and len(result["data"]) > 0:
                image_info = result["data"][0]
                image_url = image_info.get("url")
                
                if image_url:
                    sys.stdout.write(f"   ✅ 图片生成成功!\n")
                    sys.stdout.write(f"   图片URL: {image_url[:50]}...\n")
                    
                    # 下载图片
                    sys.stdout.write(f"   正在下载图片...\n")
                    image_response = requests.get(image_url, timeout=60, verify=False)
                    with open(output_path, "wb") as f:
                        f.write(image_response.content)
                    
                    file_size = os.path.getsize(output_path) / 1024
                    sys.stdout.write(f"   📥 图片已保存: {output_path} ({file_size:.2f} KB)\n")
                    return image_url
                else:
                    sys.stdout.write("   ❌ 无法获取图片URL\n")
                    return None
            else:
                sys.stdout.write(f"   ❌ 响应数据格式错误: {result}\n")
                return None
        else:
            sys.stdout.write(f"   ❌ API请求失败: {response.text[:300]}\n")
            return None
            
    except Exception as e:
        sys.stdout.write(f"   ❌ 生成过程出错: {str(e)}\n")
        import traceback
        traceback.print_exc()
        return None

def update_html_file(html_path, image_path):
    """
    更新HTML文件中的头图引用
    """
    print(f"\n📝 更新HTML文档: {html_path}")
    
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 更新头图引用
        old_patterns = [
            '有死地到无死地_头图.png',
            '有死地到无死地_头图_新版.png'
        ]
        
        new_filename = image_path.name
        
        for old_pattern in old_patterns:
            if old_pattern in content:
                content = content.replace(old_pattern, new_filename)
                print(f"   ✅ 替换头图引用: {old_pattern} -> {new_filename}")
        
        # 保存更新后的HTML
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"   ✅ HTML文档已更新")
        return True
        
    except Exception as e:
        print(f"   ❌ 更新HTML失败: {e}")
        return False

# ==================== 主流程 ====================

def main():
    print("=" * 60)
    print("🎨 使用 doubao-seedream API 生成头图")
    print("=" * 60)
    print(f"API_KEY: {API_KEY[:20]}...")
    print(f"MODEL: {MODEL}")
    print(f"尺寸: {HEADER_SIZE}")
    print("=" * 60)
    print()
    
    # 生成头图
    output_path = OUTPUT_DIR / f"{HEADER_CONFIG['id']}.png"
    
    print(f"处理: {HEADER_CONFIG['title']}")
    print(f"描述: {HEADER_CONFIG['description']}")
    print(f"输出: {output_path}")
    print()
    
    image_url = generate_image(HEADER_CONFIG['prompt'], HEADER_CONFIG['size'], output_path)
    
    if image_url:
        print("\n" + "=" * 60)
        print("✅ 头图生成成功!")
        print("=" * 60)
        print(f"📌 文件名: {output_path}")
        print(f"📐 尺寸: {HEADER_SIZE}")
        print(f"🔗 URL: {image_url}")
        
        # 更新HTML文件
        html_path = OUTPUT_DIR / "有死地到无死地_以欲为量尺_公众号专业版.html"
        if html_path.exists():
            update_html_file(html_path, output_path)
        else:
            print(f"\n⚠️ HTML文件不存在: {html_path}")
            
        print("\n🎉 任务完成!")
    else:
        print("\n❌ 头图生成失败")
        sys.exit(1)

if __name__ == "__main__":
    main()
