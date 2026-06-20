#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
公众号推送脚本 - 使用临时素材API上传封面图
"""

import requests
import os

APP_ID = "wx8389670551fc8f0c"
APP_SECRET = "5b582f604dc29f0da323325f98a30820"
TITLE = "伦理即道体"
AUTHOR = "TS"
DIGEST = "伦理是产品的本质属性"
COVER_PATH = r"E:\Trac Project\04-伦理即内核\images\AI伦理的新范式_头图_最终精确版_1080x560.jpg"

HTML_CONTENT = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>伦理即道体</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif; line-height: 1.8; font-size: 15px; }
        h1 { text-align: center; color: #8B1E22; font-size: 22px; }
        h2 { color: #8B1E22; font-size: 18px; border-left: 4px solid #8B1E22; padding-left: 10px; }
        p { margin: 10px 0; }
        strong { color: #8B1E22; }
    </style>
</head>
<body>
<h1>伦理即道体</h1>
<p>伦理不是外在的约束，而是产品存在的根本属性，是技术的呼吸方式。</p>
<h2>一、核心理念</h2>
<p><strong>道体</strong>：事物的本质、本体。</p>
<p><strong>伦理即道体</strong>：伦理是产品的本质属性。</p>
<h2>二、核心原则</h2>
<p>• <strong>减法优先</strong>：重新思考设计</p>
<p>• <strong>用户主权</strong>：选择权在用户手中</p>
<p>• <strong>坦诚透明</strong>：分工清晰可见</p>
<p>• <strong>性分自觉</strong>：知己所能所不能</p>
<h2>三、实施路线</h2>
<p><strong>短期</strong>：培训、试点、制度</p>
<p><strong>中期</strong>：优化、完善、建设</p>
<p><strong>长期</strong>：文化、改进、标准</p>
<p style="text-align:center;color:#999;font-size:13px">TS联盟</p>
</body>
</html>
"""

def get_access_token():
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APP_ID}&secret={APP_SECRET}"
    response = requests.get(url)
    result = response.json()
    if 'access_token' in result:
        print("✅ 获取access_token成功")
        return result['access_token']
    else:
        print(f"❌ 获取失败: {result}")
        return None

def upload_temp_cover(access_token):
    """使用临时素材API上传封面图"""
    if not os.path.exists(COVER_PATH):
        print(f"❌ 封面图不存在: {COVER_PATH}")
        return None
    
    url = f"https://api.weixin.qq.com/cgi-bin/media/upload?access_token={access_token}&type=image"
    with open(COVER_PATH, 'rb') as f:
        files = {'media': ('cover.jpg', f, 'image/jpeg')}
        response = requests.post(url, files=files)
    
    result = response.json()
    print(f"临时素材上传响应: {result}")
    
    if 'media_id' in result:
        print(f"✅ 临时封面图上传成功: {result['media_id'][:20]}...")
        return result['media_id']
    else:
        print(f"❌ 临时封面图上传失败")
        return None

def push_draft(access_token, cover_media_id):
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={access_token}"
    payload = {
        "articles": [{
            "title": TITLE,
            "author": AUTHOR,
            "digest": DIGEST,
            "content": HTML_CONTENT,
            "content_source_url": "",
            "thumb_media_id": cover_media_id
        }]
    }
    
    response = requests.post(url, json=payload)
    result = response.json()
    print(f"草稿推送响应: {result}")
    
    if 'draft_id' in result:
        print(f"✅ 推送成功! draft_id: {result['draft_id']}")
        return result['draft_id']
    else:
        print(f"❌ 推送失败")
        return None

def check_drafts(access_token):
    url = f"https://api.weixin.qq.com/cgi-bin/draft/batchget?access_token={access_token}"
    payload = {"offset": 0, "count": 5}
    response = requests.post(url, json=payload)
    result = response.json()
    print("\n📋 草稿箱内容:")
    if 'item' in result:
        for item in result['item'][:5]:
            print(f"- {item['title']}")
    return result

def main():
    print("="*50)
    print("📤 公众号草稿推送")
    print("="*50)
    
    token = get_access_token()
    if not token:
        return
    
    cover_id = upload_temp_cover(token)
    if not cover_id:
        return
    
    draft_id = push_draft(token, cover_id)
    if draft_id:
        check_drafts(token)
        print("\n🎉 任务完成!")

if __name__ == "__main__":
    main()