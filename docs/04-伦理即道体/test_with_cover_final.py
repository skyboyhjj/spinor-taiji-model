#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试：上传封面图并创建草稿
"""

import requests
import json

APP_ID = "wx8389670551fc8f0c"
APP_SECRET = "5b582f604dc29f0da323325f98a30820"

proxies = {'http': None, 'https': None}

def get_token():
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APP_ID}&secret={APP_SECRET}"
    response = requests.get(url, timeout=30, verify=False, proxies=proxies)
    result = response.json()
    if 'access_token' in result:
        return result['access_token']
    return None

def upload_cover(access_token, image_path):
    """上传封面图（使用永久素材接口）"""
    url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={access_token}&type=image"
    with open(image_path, 'rb') as f:
        files = {'media': ('cover.jpg', f, 'image/jpeg')}
        response = requests.post(url, files=files, timeout=60, verify=False, proxies=proxies)
        result = response.json()
        print(f"Cover Upload: {result}")
        if 'media_id' in result:
            return result['media_id']
        return None

def upload_img(access_token, image_path):
    """上传文章图片"""
    url = f"https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token={access_token}"
    with open(image_path, 'rb') as f:
        files = {'media': ('test.jpg', f, 'image/jpeg')}
        response = requests.post(url, files=files, timeout=60, verify=False, proxies=proxies)
        result = response.json()
        print(f"Image Upload: {result}")
        if 'url' in result:
            # 移除查询参数
            url = result['url']
            if '?' in url:
                url = url.split('?')[0]
            return url
        return None

def create_draft(access_token, title, content, thumb_media_id):
    """创建草稿（参考工作版本实现）"""
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={access_token}"
    
    article = {
        "title": title,
        "content": content,
        "content_source_url": "",
        "show_cover_pic": 1 if thumb_media_id else 0,
        "author": "",
        "digest": "",
        "need_open_comment": 0,
        "only_fans_can_comment": 0
    }
    
    if thumb_media_id:
        article["thumb_media_id"] = thumb_media_id
    
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
    print(f"Draft Response: {result}")
    return result

print("=" * 60)
print("🔍 测试：上传封面图并创建草稿")
print("=" * 60)

access_token = get_token()
if access_token:
    print(f"✅ 获取access_token成功")
    
    # 上传封面图
    print("\n上传封面图...")
    thumb_media_id = upload_cover(access_token, r"E:\Trac Project\07- Spinor-Taiji model读解道德经\images\cover.png")
    
    if thumb_media_id:
        print(f"✅ 封面图上传成功: {thumb_media_id}")
        
        # 上传文章图片
        print("\n上传文章图片...")
        wechat_url = upload_img(access_token, r"E:\Trac Project\07- Spinor-Taiji model读解道德经\images\taiji_life.png")
        
        if wechat_url:
            print(f"✅ 文章图片上传成功: {wechat_url}")
            
            # 创建草稿
            print("\n创建草稿...")
            content = f'<p>测试文章</p><img src="{wechat_url}" />'
            result = create_draft(access_token, "测试文章", content, thumb_media_id)
            
            if 'media_id' in result:
                print(f"✅ 成功！draft_id: {result['media_id']}")
            else:
                print(f"❌ 失败: {result.get('errmsg', '未知错误')}")
        else:
            print("❌ 文章图片上传失败")
    else:
        print("❌ 封面图上传失败")
else:
    print("❌ 获取access_token失败")