#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化测试：直接测试图片上传和草稿创建
"""

import requests
import json

APP_ID = "wx8389670551fc8f0c"
APP_SECRET = "5b582f604dc29f0da323325f98a30820"

def get_token():
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APP_ID}&secret={APP_SECRET}"
    response = requests.get(url, timeout=30, verify=False)
    result = response.json()
    if 'access_token' in result:
        return result['access_token']
    return None

def upload_img(access_token, image_path):
    """上传本地图片到微信服务器"""
    url = f"https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token={access_token}"
    with open(image_path, 'rb') as f:
        files = {'media': ('test.jpg', f, 'image/jpeg')}
        response = requests.post(url, files=files, timeout=60, verify=False)
        result = response.json()
        print(f"Upload Response: {result}")
        if 'url' in result:
            return result['url']
        return None

def create_draft(access_token, wechat_url):
    """创建草稿"""
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={access_token}"
    
    # 简化内容，只包含一张图片
    content = f'<p>测试文章</p><img src="{wechat_url}" />'
    
    payload = {
        "articles": [{
            "title": "测试文章",
            "content": content,
            "content_source_url": "",
            "show_cover_pic": 0,
            "author": "",
            "digest": "",
            "need_open_comment": 0,
            "only_fans_can_comment": 0
        }]
    }
    
    headers = {'Content-Type': 'application/json'}
    response = requests.post(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode('utf-8'),
        headers=headers,
        timeout=60,
        verify=False
    )
    result = response.json()
    print(f"Draft Response: {result}")
    return result

# 执行测试
print("=" * 60)
print("🔍 简化测试")
print("=" * 60)

access_token = get_token()
if access_token:
    print(f"✅ 获取access_token成功")
    
    # 上传测试图片
    print("\n上传图片...")
    wechat_url = upload_img(access_token, r"E:\Trac Project\07- Spinor-Taiji model读解道德经\images\taiji_life.png")
    print(f"微信URL: {wechat_url}")
    
    if wechat_url:
        print("\n创建草稿...")
        result = create_draft(access_token, wechat_url)
        if 'media_id' in result:
            print(f"✅ 成功！draft_id: {result['media_id']}")
        else:
            print(f"❌ 失败: {result.get('errmsg', '未知错误')}")
else:
    print("❌ 获取access_token失败")