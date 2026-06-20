#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
《道德经》无死地_Spinor-Taiji model读解 - 插图生成脚本
根据文章内容精准生成高质量配图，符合公众号视觉标准
"""

import os
import sys
import requests
import json
from pathlib import Path

# ==================== 配置参数 ====================
API_KEY = "ark-bcdb4b90-cf05-490d-9bc6-d3586d06ffd5-6bfb7"
MODEL = "doubao-seedream-5-0-260128"

# 输出目录
OUTPUT_DIR = Path(r"E:\Trac Project\07- Spinor-Taiji model读解道德经\images")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ==================== 图片尺寸规范 ====================
# 【默认规范】微信公众号文章插图默认尺寸：2560×1440像素（16:9宽高比）
# 此尺寸满足API最小像素要求（3,686,400像素），保证最佳显示效果
COVER_SIZE = "2560x1440"   # 封面图（16:9，默认规范尺寸）
HEADER_SIZE = "2560x1440"  # 内文配图（16:9，默认规范尺寸）

# ==================== 配图配置 ====================
IMAGE_CONFIGS = [
    {
        "id": "taiji_life",
        "title": "太极与生命",
        "description": "配合引言部分，展示太极与生命能量的关系",
        "prompt": """Traditional Chinese Tai Chi yin-yang symbol with soft golden energy flowing around it, 
meditation and mindfulness concept, serene zen atmosphere, ink wash painting style, 
golden accent colors, minimalist composition, soft gradient background from pale blue to warm beige, 
gentle light rays, spiritual tranquility, 8k ultra-detailed, cinematic lighting, 
mountains and trees in background, peaceful nature elements""",
        "size": HEADER_SIZE
    },
    {
        "id": "six_levels",
        "title": "无死地的六个层次",
        "description": "配合六个Spinor-Taiji model层次章节",
        "prompt": """Six levels of spiritual enlightenment visualized, staircase leading upwards with soft golden light, 
Chinese traditional ink painting style, zen meditation atmosphere, abstract geometric shapes, 
ethereal glow effects, ascending energy flow, peaceful mountain landscape background, 
mystical golden and purple color palette, 8k ultra-detailed, panoramic view, 
transcendent spiritual journey""",
        "size": HEADER_SIZE
    },
    {
        "id": "cover",
        "title": "封面图",
        "description": "文章封面图，体现道德经无死地主题",
        "prompt": """Professional book cover design for Tao Te Ching interpretation, 
Traditional Chinese Tai Chi yin-yang symbol as central element, 
soft golden energy waves flowing around, serene zen atmosphere, 
ink wash painting style meets modern design, deep red accent color (#8B1E22), 
mountains and mist background, spiritual tranquility, 
Chinese calligraphy style title area, minimalist elegant composition, 
high contrast for visibility, 8k ultra-detailed, cinematic lighting""",
        "size": COVER_SIZE
    }
]

# ==================== 核心函数 ====================

def generate_image(prompt, size, output_path):
    """
    使用API生成图片
    :param prompt: 图片生成提示词
    :param size: 图片尺寸
    :param output_path: 输出路径
    :return: 图片URL或None
    """
    sys.stdout.write(f"📸 正在生成图片: {output_path.name}\n")
    sys.stdout.write(f"   尺寸: {size}\n")
    
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
        
        response = requests.post(url, headers=headers, data=json.dumps(data), timeout=60, verify=False)
        
        sys.stdout.write(f"   响应状态: {response.status_code}\n")
        
        if response.status_code == 200:
            result = response.json()
            
            if "data" in result and isinstance(result["data"], list) and len(result["data"]) > 0:
                image_info = result["data"][0]
                image_url = image_info.get("url")
                
                if image_url:
                    sys.stdout.write(f"   ✅ 图片生成成功!\n")
                    
                    # 下载图片
                    image_response = requests.get(image_url, timeout=30, verify=False)
                    with open(output_path, "wb") as f:
                        f.write(image_response.content)
                    
                    sys.stdout.write(f"   📥 图片已保存: {output_path}\n")
                    return image_url
                else:
                    sys.stdout.write("   ❌ 无法获取图片URL\n")
                    return None
            else:
                sys.stdout.write("   ❌ 响应数据格式错误\n")
                return None
        else:
            sys.stdout.write(f"   ❌ API请求失败: {response.text[:200]}\n")
            return None
            
    except Exception as e:
        sys.stdout.write(f"   ❌ 生成过程出错: {str(e)}\n")
        return None

def generate_all_images():
    """生成所有配图"""
    generated_images = {}
    
    print("=" * 60)
    print("🎨 《道德经》无死地_Spinor-Taiji model读解 - 配图生成")
    print("=" * 60)
    print()
    
    for config in IMAGE_CONFIGS:
        print(f"处理: {config['title']}")
        print(f"描述: {config['description']}")
        
        output_path = OUTPUT_DIR / f"{config['id']}.png"
        image_url = generate_image(config['prompt'], config['size'], output_path)
        
        if image_url:
            generated_images[config['id']] = {
                'url': image_url,
                'path': str(output_path),
                'title': config['title']
            }
        
        print()
    
    print("=" * 60)
    return generated_images

def update_html_with_new_images(html_path, generated_images):
    """
    更新HTML文档中的图片URL
    :param html_path: HTML文件路径
    :param generated_images: 生成的图片字典
    """
    print(f"📝 更新HTML文档: {html_path}")
    
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 更新太极与生命配图
        if 'taiji_life' in generated_images:
            old_url = 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=Traditional%20Chinese%20Tai%20Chi%20yin%20yang%20symbol%20with%20soft%20golden%20energy%20flow%2C%20surrounded%20by%20peaceful%20nature%20elements%20like%20mountains%20and%20trees%2C%20serene%20zen%20atmosphere%2C%20ink%20wash%20painting%20style&image_size=landscape_16_9'
            content = content.replace(old_url, generated_images['taiji_life']['url'])
            print("   ✅ 更新太极与生命配图")
        
        # 更新六个层次配图
        if 'six_levels' in generated_images:
            old_url = 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=Six%20levels%20of%20spiritual%20enlightenment%2C%20staircase%20leading%20upwards%20with%20soft%20golden%20light%2C%20Chinese%20traditional%20ink%20painting%20style%2C%20zen%20meditation%20atmosphere&image_size=landscape_16_9'
            content = content.replace(old_url, generated_images['six_levels']['url'])
            print("   ✅ 更新六个层次配图")
        
        # 保存更新后的HTML
        new_html_path = html_path.replace('.html', '_with_new_images.html')
        with open(new_html_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"   ✅ HTML文档已更新并保存为: {new_html_path}")
        return new_html_path
        
    except Exception as e:
        print(f"   ❌ 更新HTML失败: {e}")
        return None

def validate_images(generated_images):
    """验证生成的图片"""
    print("\n🔍 验证生成结果:")
    valid_count = 0
    
    for img_id, info in generated_images.items():
        path = Path(info['path'])
        if path.exists() and path.stat().st_size > 0:
            print(f"   ✅ {info['title']}: 有效")
            valid_count += 1
        else:
            print(f"   ❌ {info['title']}: 无效或为空")
    
    print(f"\n   总计: {valid_count}/{len(generated_images)} 张图片有效")
    return valid_count == len(generated_images)

# ==================== 主流程 ====================

def main():
    # Step 1: 生成图片
    generated_images = generate_all_images()
    
    # Step 2: 验证图片
    if not validate_images(generated_images):
        print("\n❌ 部分图片生成失败，请检查网络或重试")
        return
    
    # Step 3: 更新HTML文档
    html_path = Path(r"E:\Trac Project\07- Spinor-Taiji model读解道德经\《道德经》无死地_Spinor-Taiji model读解_公众号版.html")
    if html_path.exists():
        new_html_path = update_html_with_new_images(str(html_path), generated_images)
        
        if new_html_path:
            print("\n🎉 配图更新完成!")
            print("=" * 60)
            print("📊 生成结果汇总:")
            print("=" * 60)
            for img_id, info in generated_images.items():
                print(f"\n📌 {info['title']}")
                print(f"   文件: {info['path']}")
                print(f"   URL: {info['url']}")
            print(f"\n📄 更新后的HTML: {new_html_path}")
    else:
        print(f"\n❌ HTML文件不存在: {html_path}")

if __name__ == "__main__":
    main()