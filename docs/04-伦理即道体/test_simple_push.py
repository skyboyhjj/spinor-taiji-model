#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化测试：推送不含图片的文章到草稿箱
"""

import os
import json
import requests

def load_env(env_path='.env'):
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

load_env()

APP_ID = os.getenv('WECHAT_APP_ID')
APP_SECRET = os.getenv('WECHAT_APP_SECRET')

def get_access_token():
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APP_ID}&secret={APP_SECRET}"
    response = requests.get(url, timeout=30, verify=False)
    result = response.json()
    if 'access_token' in result:
        return result['access_token']
    return None

def push_simple_draft(access_token):
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={access_token}"
    
    # 简化的测试内容，不包含图片
    content = '''
    <p>这是一篇测试文章</p>
    <p>用于验证草稿接口是否正常工作</p>
    <p>不包含任何图片</p>
    '''
    
    payload = {
        "articles": [{
            "title": "测试文章（无图片）",
            "author": "测试",
            "digest": "测试摘要",
            "content": content,
            "content_source_url": "",
            "need_open_comment": 1,
            "only_fans_can_comment": 0
        }]
    }
    
    response = requests.post(url, json=payload, timeout=60, verify=False)
    print(f"Response: {response.text}")
    return response.json()

# 执行测试
print("=" * 60)
print("🔍 测试无图片文章推送")
print("=" * 60)

access_token = get_access_token()
if access_token:
    print(f"✅ 获取access_token成功")
    print("\n推送测试文章...")
    result = push_simple_draft(access_token)
    if 'draft_id' in result:
        print(f"✅ 推送成功！draft_id: {result['draft_id']}")
    else:
        print(f"❌ 推送失败: {result}")
else:
    print("❌ 获取access_token失败")