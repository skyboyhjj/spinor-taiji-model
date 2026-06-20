#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版公众号推送脚本
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
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif; line-height: 1.8; }
        h1 { text-align: center; color: #8B1E22; font-size: 22px; }
        h2 { color: #8B1E22; font-size: 18px; border-left: 4px solid #8B1E22; padding-left: 10px; }
        p { margin: 10px 0; font-size: 15px; }
        strong { color: #8B1E22; }
    </style>
</head>
<body>
<h1>伦理即道体</h1>
<p>伦理不是外在的约束，而是产品存在的根本属性，是技术的呼吸方式。</p>
<h2>一、核心理念</h2>
<p><strong>道体</strong>：事物的本质、本体，是一切存在的根基和法则。</p>
<p><strong>伦理即道体</strong>：伦理不是外挂，而是产品的本质属性。</p>
<h2>二、核心原则</h2>
<p>• <strong>减法优先</strong>：如果答案不是减法，重新思考设计</p>
<p>• <strong>用户主权</strong>：选择权永远在用户手中</p>
<p>• <strong>坦诚透明</strong>：AI与人类分工清晰可见</p>
<p>• <strong>性分自觉</strong>：知己所能，知己所不能</p>
<h2>三、实施路线</h2>
<p><strong>短期目标</strong>：团队培训、试点运行、制度落地</p>
<p><strong>中期目标</strong>：流程优化、指标完善、工具建设</p>
<p><strong>长期目标</strong>：文化形成、持续改进、标准输出</p>
<p style="text-align:center;color:#999;font-size:13px">TS联盟 · 探索爱的真谛</p>
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

def upload_cover(access_token):
    if not os.path.exists(COVER_PATH):
        print(f"❌ 封面图不存在: {COVER_PATH}")
        return None
    
    url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={access_token}&type=image"
    with open(COVER_PATH, 'rb') as f:
        files = {'media': ('cover.jpg', f, 'image/jpeg')}
        response = requests.post(url, files=files)
    
    result = response.json()
    if 'media_id' in result:
        print(f"✅ 封面图上传成功: {result['media_id'][:20]}...")
        return result['media_id']
    else:
        print(f"❌ 封面图上传失败: {result}")
        return None

def push_draft(access_token, cover_id):
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={access_token}"
    payload = {
        "articles": [{
            "title": TITLE,
            "author": AUTHOR,
            "digest": DIGEST,
            "content": HTML_CONTENT,
            "content_source_url": ""
        }]
    }
    
    response = requests.post(url, json=payload)
    result = response.json()
    print(f"响应: {result}")
    
    if 'draft_id' in result:
        print(f"✅ 推送成功! draft_id: {result['draft_id']}")
        return result['draft_id']
    else:
        print(f"❌ 推送失败")
        return None

def main():
    print("="*50)
    print("📤 公众号草稿推送")
    print("="*50)
    
    token = get_access_token()
    if not token:
        return
    
    cover_id = upload_cover(token)
    if not cover_id:
        return
    
    draft_id = push_draft(token, cover_id)
    if draft_id:
        print("\n🎉 任务完成!")

if __name__ == "__main__":
    main()