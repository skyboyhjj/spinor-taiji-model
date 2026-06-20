#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试版本：输出详细信息诊断推送问题
"""

import os
import sys
import json
import requests
import re
from pathlib import Path

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
    print(f"Access Token Response: {response.text[:200]}")
    result = response.json()
    if 'access_token' in result:
        return result['access_token']
    return None

def upload_image(access_token, image_url):
    url = f"https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token={access_token}"
    image_response = requests.get(image_url, timeout=30, verify=False)
    files = {'media': ('image.jpg', image_response.content, 'image/jpeg')}
    response = requests.post(url, files=files, timeout=60, verify=False)
    print(f"Image Upload Response: {response.text}")
    result = response.json()
    if 'url' in result:
        return result['url'].replace('http://', 'https://')
    return None

# 测试流程
print("=" * 60)
print("🔍 调试推送流程")
print("=" * 60)

# 1. 获取access_token
print("\n1. 获取access_token...")
access_token = get_access_token()
print(f"   access_token: {access_token[:20]}..." if access_token else "   ❌ 获取失败")

# 2. 测试上传单张图片
if access_token:
    print("\n2. 测试上传图片...")
    test_image_url = "https://ark-acg-cn-beijing.tos-cn-beijing.volces.com/doubao-seedream-5-0/0217815774136244f24b207f6c3c840415c2dc20832f65f371b30_0.jpeg?X-Tos-Algorithm=TOS4-HMAC-SHA256&X-Tos-Credential=AKLTYWJkZTExNjA1ZDUyNDc3YzhjNTM5OGIyNjBhNDcyOTQ%2F20260616%2Fcn-beijing%2Ftos%2Frequest&X-Tos-Date=20260616T023725Z&X-Tos-Expires=86400&X-Tos-Signature=a18d08a439a8c232602485df95448d95a091962a7e85948292aeb4c7f2d31725&X-Tos-SignedHeaders=host"
    wechat_url = upload_image(access_token, test_image_url)
    print(f"   WeChat URL: {wechat_url}")

# 3. 测试推送草稿
if access_token and wechat_url:
    print("\n3. 测试推送草稿...")
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={access_token}"
    
    # 简化的测试内容
    content = f'''
    <p>测试文章</p>
    <img src="{wechat_url}" />
    '''
    
    payload = {
        "articles": [{
            "title": "测试文章",
            "author": "测试",
            "digest": "测试摘要",
            "content": content,
            "content_source_url": "",
            "need_open_comment": 1,
            "only_fans_can_comment": 0
        }]
    }
    
    print(f"Payload preview (first 500 chars): {json.dumps(payload)[:500]}...")
    
    response = requests.post(url, json=payload, timeout=60, verify=False)
    print(f"\nDraft Response: {response.text}")

print("\n" + "=" * 60)
print("调试完成")
print("=" * 60)