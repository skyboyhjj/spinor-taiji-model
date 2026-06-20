#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成《道德经》第七十九章头图并推送文章
"""

import os
import requests

def generate_header_image():
    """生成头图"""
    
    prompt = """
    A mystical header image for Tao Te Ching Chapter 79 about resolving resentment,
    featuring:
    1. Deep purple cosmic background with swirling energy patterns
    2. Golden balance scale (representing "执左契") floating in center
    3. Two wolves - one white/good and one black/evil - in peaceful harmony
    4. Soft golden light rays emanating from the center
    5. Chinese calligraphy title "执左契而不责" in golden text
    6. Tai Chi symbol subtly incorporated
    7. Color scheme: deep purple, gold, silver, mystical atmosphere
    8. Professional book cover quality, 16:9 aspect ratio
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
        
        output_path = r'e:\Trac Project\07- Spinor-Taiji model读解道德经\第七十九章_头图.png'
        with open(output_path, 'wb') as f:
            f.write(img_response.content)
        
        file_size = os.path.getsize(output_path) / 1024
        print(f"✅ 头图生成成功！")
        print(f"📁 文件路径: {output_path}")
        print(f"📐 文件大小: {file_size:.2f} KB")
        
        return output_path
        
    except Exception as e:
        print(f"❌ 头图生成失败: {e}")
        return None

def push_to_wechat():
    """推送文章到公众号"""
    import sys
    sys.path.insert(0, r'C:\Users\hejij\.trae-cn\skills\wechat-typeset-pro\scripts')
    
    from wechat_publisher_utils import WeChatPublisher, WeChatAPIError
    
    try:
        publisher = WeChatPublisher(disable_proxy=True, verify_ssl=False)
        
        html_path = r'e:\Trac Project\07- Spinor-Taiji model读解道德经\道德经第七十九章_公众号版.html'
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        cover_path = r'e:\Trac Project\07- Spinor-Taiji model读解道德经\第七十九章_头图.png'
        cover_media_id = publisher.upload_cover_image(cover_path)
        print(f"封面图上传成功")
        
        result = publisher.push_to_draft(
            title="《道德经》第七十九章：执左契而不责——化解怨恨的终极心法",
            content=content,
            author="TS爱心联盟",
            digest="和大怨，必有余怨，安可以为善？圣人执左契而不责于人，天道无亲常与善人。",
            cover_media_id=cover_media_id
        )
        
        print(f"\n✅ 推送成功！草稿ID: {result['draft_id']}")
        
    except WeChatAPIError as e:
        print(f"\n❌ 推送失败: {e.message}")
        print(f"错误码: {e.error_code}")
        if e.error_code == 40164:
            print("\n📌 请将公网IP添加到微信公众号IP白名单")
            print("   常见公网IP: 36.101.158.118")
    except Exception as e:
        print(f"\n❌ 推送失败: {e}")

def main():
    print("="*60)
    print("当前本地IP: 192.168.1.71")
    print("微信白名单需添加公网IP（如 36.101.158.118）")
    print("="*60)
    
    header_path = generate_header_image()
    
    if header_path:
        push_to_wechat()

if __name__ == '__main__':
    main()
