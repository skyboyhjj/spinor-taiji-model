#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
伦理即道体理念落地指南 - 公众号推送脚本
严格按照《公众号文章制作完整操作手册》标准流程执行
"""

import os
import sys
import json
import requests
from pathlib import Path

# ==================== 配置参数 ====================
# 文章配置
TITLE = "伦理即道体：从理念到实践的完整落地指南"
AUTHOR = "TS爱心联盟"
DIGEST = "伦理不是外在的约束，而是产品存在的根本属性。本文系统阐述如何将这一核心理念转化为具体的产品开发实践。"
HTML_FILE = r"E:\Trac Project\04-伦理即内核\伦理即道体理念落地指南_公众号版_clean.html"

# 微信公众号配置（从环境变量读取）
APP_ID = os.getenv('WECHAT_APP_ID')
APP_SECRET = os.getenv('WECHAT_APP_SECRET')

# 输出文件
DRAFT_LIST_FILE = "draft_list.json"

# ==================== 辅助函数 ====================

def get_access_token(app_id, app_secret):
    """获取微信公众号access_token"""
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={app_id}&secret={app_secret}"
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        result = response.json()
        if 'access_token' in result:
            print(f"✅ 获取access_token成功")
            return result['access_token']
        else:
            print(f"❌ 获取access_token失败: {result}")
            return None
    except Exception as e:
        print(f"❌ 获取access_token异常: {e}")
        return None

def read_html_content(file_path):
    """读取HTML文件内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"✅ 成功读取HTML文件: {file_path}")
        return content
    except Exception as e:
        print(f"❌ 读取HTML文件失败: {e}")
        return None

def push_to_draft(access_token, title, author, digest, content):
    """推送文章到草稿箱"""
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={access_token}"
    
    payload = {
        "articles": [
            {
                "title": title,
                "author": author,
                "digest": digest,
                "content": content,
                "content_source_url": "",
                "need_open_comment": 1,
                "only_fans_can_comment": 0
            }
        ]
    }
    
    try:
        response = requests.post(url, json=payload, timeout=60)
        response.raise_for_status()
        result = response.json()
        if 'draft_id' in result:
            print(f"✅ 推送草稿成功！")
            print(f"   draft_id: {result['draft_id']}")
            return result['draft_id']
        else:
            print(f"❌ 推送草稿失败: {result}")
            return None
    except Exception as e:
        print(f"❌ 推送草稿异常: {e}")
        return None

def check_drafts(access_token):
    """检查草稿箱内容"""
    url = f"https://api.weixin.qq.com/cgi-bin/draft/batchget?access_token={access_token}"
    
    payload = {
        "offset": 0,
        "count": 10
    }
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        # 保存到文件
        with open(DRAFT_LIST_FILE, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"✅ 草稿列表已保存到: {DRAFT_LIST_FILE}")
        
        if 'item' in result and len(result['item']) > 0:
            print("\n📋 草稿箱最新文章列表:")
            for i, item in enumerate(result['item'], 1):
                print(f"{i}. {item['title']}")
                print(f"   创建时间: {item['update_time']}")
                print()
        
        return result
    except Exception as e:
        print(f"❌ 获取草稿列表失败: {e}")
        return None

def validate_config():
    """验证配置是否完整"""
    errors = []
    
    # 检查HTML文件
    if not Path(HTML_FILE).exists():
        errors.append(f"HTML文件不存在: {HTML_FILE}")
    
    # 检查微信配置
    if not APP_ID:
        errors.append("未配置WECHAT_APP_ID环境变量")
    if not APP_SECRET:
        errors.append("未配置WECHAT_APP_SECRET环境变量")
    
    if errors:
        print("❌ 配置验证失败:")
        for error in errors:
            print(f"   - {error}")
        return False
    
    print("✅ 配置验证通过")
    return True

# ==================== 主流程 ====================

def main():
    print("=" * 60)
    print("📤 伦理即道体理念落地指南 - 公众号推送")
    print("=" * 60)
    print()
    
    # Step 1: 验证配置
    print("Step 1/4: 验证配置...")
    if not validate_config():
        sys.exit(1)
    print()
    
    # Step 2: 读取HTML内容
    print("Step 2/4: 读取HTML内容...")
    content = read_html_content(HTML_FILE)
    if not content:
        sys.exit(1)
    print(f"   内容长度: {len(content)} 字符")
    print()
    
    # Step 3: 获取access_token
    print("Step 3/4: 获取微信公众号access_token...")
    access_token = get_access_token(APP_ID, APP_SECRET)
    if not access_token:
        sys.exit(1)
    print()
    
    # Step 4: 推送草稿
    print("Step 4/4: 推送文章到草稿箱...")
    draft_id = push_to_draft(access_token, TITLE, AUTHOR, DIGEST, content)
    if not draft_id:
        sys.exit(1)
    print()
    
    # 验证推送结果
    print("🔍 验证推送结果...")
    check_drafts(access_token)
    
    print("=" * 60)
    print("🎉 推送任务完成！")
    print("=" * 60)
    print(f"📌 文章标题: {TITLE}")
    print(f"📌 草稿ID: {draft_id}")
    print(f"📌 下一步: 登录微信公众号后台 → 素材管理 → 草稿箱")
    print()

if __name__ == "__main__":
    main()