#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
《道德经》无死地_Spinor-Taiji model读解 - 修复版推送脚本
参考 push_to_wechat_v2.py 的实现逻辑
"""

import requests
import json
import os
from pathlib import Path

class WeChatPublisher:
    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret
        self.access_token = None
    
    def get_access_token(self):
        url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={self.app_id}&secret={self.app_secret}"
        try:
            response = requests.get(url, timeout=30, verify=False)
            data = response.json()
            if 'access_token' in data:
                self.access_token = data['access_token']
                print(f"✅ 成功获取access_token")
                return True
            else:
                print(f"❌ 获取access_token失败: {data.get('errmsg', '未知错误')}")
                return False
        except Exception as e:
            print(f"❌ 请求失败: {str(e)}")
            return False
    
    def upload_image(self, image_path):
        """上传本地图片到微信服务器"""
        if not self.access_token:
            print("❌ 请先获取access_token")
            return None
        
        url = f"https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token={self.access_token}"
        
        try:
            with open(image_path, 'rb') as f:
                files = {'media': (os.path.basename(image_path), f, 'image/jpeg')}
                response = requests.post(url, files=files, timeout=60, verify=False)
                data = response.json()
                
                if 'url' in data:
                    print(f"✅ 图片上传成功: {os.path.basename(image_path)}")
                    return data['url']
                else:
                    print(f"❌ 图片上传失败: {data.get('errmsg', '未知错误')}")
                    return None
        except Exception as e:
            print(f"❌ 上传图片失败: {str(e)}")
            return None
    
    def upload_cover(self, image_path):
        """上传封面图到微信服务器（返回media_id）"""
        if not self.access_token:
            print("❌ 请先获取access_token")
            return None
        
        url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={self.access_token}&type=image"
        
        try:
            with open(image_path, 'rb') as f:
                files = {'media': (os.path.basename(image_path), f, 'image/jpeg')}
                response = requests.post(url, files=files, timeout=60, verify=False)
                data = response.json()
                
                if 'media_id' in data:
                    print(f"✅ 封面图上传成功: {os.path.basename(image_path)}")
                    print(f"   media_id: {data['media_id']}")
                    return data['media_id']
                else:
                    print(f"❌ 封面图上传失败: {data.get('errmsg', '未知错误')}")
                    return None
        except Exception as e:
            print(f"❌ 上传封面图失败: {str(e)}")
            return None
    
    def create_draft(self, title, content, thumb_media_id=""):
        """创建公众号草稿"""
        if not self.access_token:
            print("❌ 请先获取access_token")
            return None
        
        url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={self.access_token}"
        
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
        
        try:
            headers = {'Content-Type': 'application/json'}
            response = requests.post(
                url, 
                data=json.dumps(data, ensure_ascii=False).encode('utf-8'), 
                headers=headers, 
                timeout=60,
                verify=False
            )
            result = response.json()
            
            print(f"📝 API响应: {json.dumps(result, ensure_ascii=False)[:300]}")
            
            if 'media_id' in result:
                print(f"✅ 草稿创建成功，media_id: {result['media_id']}")
                return result['media_id']
            else:
                print(f"❌ 创建草稿失败: {result.get('errmsg', '未知错误')}")
                return None
        except Exception as e:
            print(f"❌ 创建草稿失败: {str(e)}")
            return None

def main():
    # 配置信息
    APP_ID = "wx8389670551fc8f0c"
    APP_SECRET = "5b582f604dc29f0da323325f98a30820"
    
    # 文章配置
    article_path = Path(r'E:\Trac Project\07- Spinor-Taiji model读解道德经\《道德经》无死地_Spinor-Taiji model读解_公众号版_with_new_images.html')
    title = "《道德经》'无死地'Spinor-Taiji model读解"
    
    if not article_path.exists():
        print(f"❌ 文章文件不存在: {article_path}")
        return
    
    with open(article_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("=" * 60)
    print("微信公众号草稿推送工具（修复版）")
    print("=" * 60)
    print(f"文章标题: {title}")
    print(f"文章位置: {article_path}")
    print(f"文章长度: {len(content)} 字符")
    print("=" * 60)
    
    publisher = WeChatPublisher(APP_ID, APP_SECRET)
    
    print("\nStep 1: 获取微信公众号access_token...")
    if not publisher.get_access_token():
        return
    
    print("\nStep 2: 上传文章图片...")
    image_dir = Path(r'E:\Trac Project\07- Spinor-Taiji model读解道德经\images')
    image_files = list(image_dir.glob('*.png')) + list(image_dir.glob('*.jpg'))
    
    for img_path in image_files:
        url = publisher.upload_image(str(img_path))
        if url:
            old_path = img_path.name
            count = content.count(old_path)
            if count > 0:
                content = content.replace(old_path, url)
                print(f"  → 替换图片: {old_path} → {url[:50]}... (替换 {count} 次)")
    
    # 也替换远程URL
    import re
    img_pattern = r'<img[^>]+src="([^"]+ark-acg[^"]+)"'
    img_urls = re.findall(img_pattern, content)
    
    for url in img_urls:
        print(f"\n处理远程图片: {url[:50]}...")
        # 下载图片临时保存
        try:
            response = requests.get(url, timeout=30, verify=False)
            temp_path = Path(f"temp_{hash(url) % 10000}.jpg")
            with open(temp_path, 'wb') as f:
                f.write(response.content)
            
            wechat_url = publisher.upload_image(str(temp_path))
            if wechat_url:
                content = content.replace(url, wechat_url)
                print(f"  → 已替换为微信URL")
            temp_path.unlink()
        except Exception as e:
            print(f"  → 处理失败: {e}")
    
    print("\nStep 3: 创建公众号草稿...")
    http_count = content.count('http://mmbiz.qpic.cn')
    https_count = content.count('https://mmbiz.qpic.cn')
    print(f"  → 内容中包含 {http_count + https_count} 个微信图片URL")
    
    media_id = publisher.create_draft(title, content)
    
    if media_id:
        print("\n" + "=" * 60)
        print("🎉 推送成功！")
        print("=" * 60)
        print(f"草稿ID: {media_id}")
        print("=" * 60)
        print("您可以在微信公众号后台查看草稿：")
        print("路径：内容与互动 → 草稿箱")
        print("=" * 60)

if __name__ == '__main__':
    main()