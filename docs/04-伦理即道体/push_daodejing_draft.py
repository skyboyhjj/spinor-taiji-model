#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
《道德经》无死地_Spinor-Taiji model读解 - 公众号推送脚本
将更新后的文章推送到微信公众号草稿箱
"""

import os
import sys
import json
import requests
import re
from pathlib import Path

# ==================== 加载.env配置文件 ====================
def load_env(env_path='.env'):
    """从.env文件加载环境变量"""
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()
        print(f"✅ 已从 {env_path} 加载配置")
    else:
        print(f"⚠️ 未找到 {env_path} 文件，将使用系统环境变量")

# 加载配置
load_env()

# ==================== 配置参数 ====================
# 文章配置
TITLE = "《道德经》'无死地'Spinor-Taiji model读解"
AUTHOR = "TS爱心联盟"
DIGEST = "《道德经》第50章'善摄生者，无死地'与第55章'含德之厚，毒虫不螫'的千古争议，今日终于有了新解。本文运用Spinor-Taiji model模型，从六个层次深度剖析'无死地'的本质。"
HTML_FILE = r"E:\Trac Project\07- Spinor-Taiji model读解道德经\《道德经》无死地_Spinor-Taiji model读解_公众号版_with_new_images.html"

# 微信公众号配置（从环境变量读取）
APP_ID = os.getenv('WECHAT_APP_ID')
APP_SECRET = os.getenv('WECHAT_APP_SECRET')

# 输出文件
DRAFT_LIST_FILE = "draft_list_daodejing.json"

# ==================== 辅助函数 ====================

def get_access_token(app_id, app_secret):
    """获取微信公众号access_token"""
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={app_id}&secret={app_secret}"
    try:
        response = requests.get(url, timeout=30, verify=False)
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
        print(f"   内容长度: {len(content)} 字符")
        return content
    except Exception as e:
        print(f"❌ 读取HTML文件失败: {e}")
        return None

def upload_image_to_wechat(access_token, image_url):
    """将图片上传到微信永久素材接口，返回标准格式的图片URL"""
    url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={access_token}&type=image"
    
    try:
        # 先下载图片
        image_response = requests.get(image_url, timeout=30, verify=False)
        image_response.raise_for_status()
        
        # 构造multipart请求
        files = {
            'media': ('image.jpg', image_response.content, 'image/jpeg')
        }
        
        response = requests.post(url, files=files, timeout=60, verify=False)
        response.raise_for_status()
        result = response.json()
        
        if 'media_id' in result:
            # 使用标准的微信图片URL格式
            media_id = result['media_id']
            wechat_url = f"https://mmbiz.qpic.cn/mmbiz_jpg/{media_id}/0"
            print(f"✅ 图片上传成功: {wechat_url[:50]}...")
            return wechat_url
        else:
            print(f"❌ 图片上传失败: {result}")
            return None
    except Exception as e:
        print(f"❌ 图片上传异常: {e}")
        return None

def replace_images_with_media_ids(content, access_token):
    """将HTML中的图片URL替换为微信素材库URL"""
    print("\n🔄 正在上传图片并替换为微信URL...")
    
    # 查找所有img标签
    img_pattern = r'<img[^>]+src="([^"]+)"'
    img_urls = re.findall(img_pattern, content)
    
    if not img_urls:
        print("   ⚠️ 未找到图片链接")
        return content
    
    for i, url in enumerate(img_urls, 1):
        print(f"\n   处理图片{i}: {url[:50]}...")
        wechat_url = upload_image_to_wechat(access_token, url)
        
        if wechat_url:
            # 替换为微信图片URL
            old_tag = f'src="{url}"'
            new_tag = f'src="{wechat_url}"'
            content = content.replace(old_tag, new_tag)
            print(f"   ✅ 已替换为微信URL")
        else:
            print(f"   ⚠️ 图片上传失败，保留原URL")
    
    return content

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
        response = requests.post(url, json=payload, timeout=60, verify=False)
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
        response = requests.post(url, json=payload, timeout=30, verify=False)
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

def validate_images_in_html(content):
    """验证HTML中的图片链接是否有效"""
    print("\n🔍 验证HTML中的图片:")
    
    img_pattern = r'<img[^>]+src="([^"]+)"'
    img_urls = re.findall(img_pattern, content)
    
    if not img_urls:
        print("   ❌ 未找到图片链接")
        return False
    
    valid_count = 0
    for i, url in enumerate(img_urls, 1):
        print(f"   图片{i}: {url[:50]}...")
        if url.startswith('http'):
            valid_count += 1
            print(f"      ✅ 有效URL")
        else:
            print(f"      ❌ URL格式不正确")
    
    print(f"\n   总计: {valid_count}/{len(img_urls)} 张图片有效")
    return valid_count == len(img_urls)

# ==================== 主流程 ====================

def main():
    print("=" * 60)
    print("📤 《道德经》无死地_Spinor-Taiji model读解 - 公众号推送")
    print("=" * 60)
    print()
    
    # Step 1: 验证配置
    print("Step 1/6: 验证配置...")
    if not validate_config():
        sys.exit(1)
    print()
    
    # Step 2: 读取HTML内容
    print("Step 2/6: 读取HTML内容...")
    content = read_html_content(HTML_FILE)
    if not content:
        sys.exit(1)
    print()
    
    # Step 3: 验证图片
    print("Step 3/6: 验证图片链接...")
    validate_images_in_html(content)
    print()
    
    # Step 4: 获取access_token
    print("Step 4/6: 获取微信公众号access_token...")
    access_token = get_access_token(APP_ID, APP_SECRET)
    if not access_token:
        sys.exit(1)
    print()
    
    # Step 5: 上传图片并替换为media_id
    print("Step 5/6: 上传图片到微信素材库...")
    content_with_media = replace_images_with_media_ids(content, access_token)
    print()
    
    # Step 6: 推送草稿
    print("Step 6/6: 推送文章到草稿箱...")
    draft_id = push_to_draft(access_token, TITLE, AUTHOR, DIGEST, content_with_media)
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