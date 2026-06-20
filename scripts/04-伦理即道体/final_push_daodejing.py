#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
《道德经》无死地_Spinor-Taiji model读解 - 最终推送脚本
修复所有已知问题
"""

import requests
import json
import os
import re
from pathlib import Path

APP_ID = "wx8389670551fc8f0c"
APP_SECRET = "5b582f604dc29f0da323325f98a30820"

# 禁用代理（关键修复）
proxies = {'http': None, 'https': None}

def get_token():
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APP_ID}&secret={APP_SECRET}"
    response = requests.get(url, timeout=30, verify=False, proxies=proxies)
    result = response.json()
    if 'access_token' in result:
        return result['access_token']
    return None

def upload_cover(access_token, image_path):
    """上传封面图（永久素材）"""
    url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={access_token}&type=image"
    with open(image_path, 'rb') as f:
        files = {'media': ('cover.jpg', f, 'image/jpeg')}
        response = requests.post(url, files=files, timeout=60, verify=False, proxies=proxies)
        result = response.json()
        if 'media_id' in result:
            return result['media_id']
        return None

def upload_image(access_token, image_path):
    """上传文章图片"""
    url = f"https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token={access_token}"
    with open(image_path, 'rb') as f:
        files = {'media': ('image.jpg', f, 'image/jpeg')}
        response = requests.post(url, files=files, timeout=60, verify=False, proxies=proxies)
        result = response.json()
        if 'url' in result:
            return result['url']
        return None

def create_draft(access_token, title, content, thumb_media_id):
    """创建草稿"""
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={access_token}"
    
    article = {
        "title": title,
        "content": content,
        "content_source_url": "",
        "show_cover_pic": 1,
        "author": "",
        "digest": "",
        "need_open_comment": 0,
        "only_fans_can_comment": 0,
        "thumb_media_id": thumb_media_id
    }
    
    data = {"articles": [article]}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(
        url,
        data=json.dumps(data, ensure_ascii=False).encode('utf-8'),
        headers=headers,
        timeout=60,
        verify=False,
        proxies=proxies
    )
    result = response.json()
    return result

def main():
    print("=" * 60)
    print("📤 《道德经》无死地_Spinor-Taiji model读解 - 最终推送")
    print("=" * 60)
    
    # 1. 获取access_token
    print("\n【步骤1/5】获取access_token...")
    access_token = get_token()
    if not access_token:
        print("❌ 获取access_token失败")
        return
    print("✅ 获取access_token成功")
    
    # 2. 上传封面图
    print("\n【步骤2/5】上传封面图...")
    cover_path = r"E:\Trac Project\07- Spinor-Taiji model读解道德经\images\cover.png"
    thumb_media_id = upload_cover(access_token, cover_path)
    if not thumb_media_id:
        print("❌ 封面图上传失败")
        return
    print(f"✅ 封面图上传成功: {thumb_media_id}")
    
    # 3. 读取HTML内容
    print("\n【步骤3/5】读取HTML内容...")
    html_path = r"E:\Trac Project\07- Spinor-Taiji model读解道德经\《道德经》无死地_Spinor-Taiji model读解_公众号版_with_new_images.html"
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    print(f"✅ HTML内容长度: {len(content)} 字符")
    
    # 4. 上传并替换图片
    print("\n【步骤4/5】上传文章图片...")
    image_dir = Path(r'E:\Trac Project\07- Spinor-Taiji model读解道德经\images')
    image_files = list(image_dir.glob('*.png')) + list(image_dir.glob('*.jpg'))
    
    for img_path in image_files:
        wechat_url = upload_image(access_token, str(img_path))
        if wechat_url:
            old_name = img_path.name
            content = content.replace(old_name, wechat_url)
            print(f"  → 替换图片: {old_name}")
    
    # 替换远程URL图片
    img_pattern = r'<img[^>]+src="([^"]+ark-acg[^"]+)"'
    img_urls = re.findall(img_pattern, content)
    for url in img_urls:
        temp_path = Path(f"temp_{hash(url) % 10000}.jpg")
        try:
            response = requests.get(url, timeout=30, verify=False, proxies=proxies)
            with open(temp_path, 'wb') as f:
                f.write(response.content)
            wechat_url = upload_image(access_token, str(temp_path))
            if wechat_url:
                content = content.replace(url, wechat_url)
                print(f"  → 替换远程图片")
        except:
            pass
        finally:
            if temp_path.exists():
                temp_path.unlink()
    
    # 5. 创建草稿
    print("\n【步骤5/5】创建公众号草稿...")
    result = create_draft(access_token, "《道德经》'无死地'Spinor-Taiji model读解", content, thumb_media_id)
    
    if 'media_id' in result:
        print(f"✅ 推送成功！draft_id: {result['media_id']}")
        print("\n" + "=" * 60)
        print("🎉 推送任务完成！")
        print("=" * 60)
        print(f"📌 草稿ID: {result['media_id']}")
        print("📌 下一步: 登录微信公众号后台 → 素材管理 → 草稿箱")
        print("=" * 60)
    else:
        print(f"❌ 创建草稿失败: {result.get('errmsg', '未知错误')}")

if __name__ == '__main__':
    main()