#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版公众号推送脚本
"""

import requests

APP_ID = "wx8389670551fc8f0c"
APP_SECRET = "5b582f604dc29f0da323325f98a30820"
TITLE = "伦理即道体：从理念到实践的完整落地指南"
AUTHOR = "TS爱心联盟"
DIGEST = "伦理不是外在的约束，而是产品存在的根本属性，是技术的呼吸方式。"

HTML_CONTENT = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>伦理即道体</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif; line-height: 1.8; font-size: 15px; }
        h1 { text-align: center; color: #8B1E22; font-size: 22px; border-bottom: 2px solid #8B1E22; padding-bottom: 10px; }
        h2 { color: #8B1E22; font-size: 18px; border-left: 4px solid #8B1E22; padding-left: 10px; margin: 20px 0; }
        p { margin: 12px 0; }
        strong { color: #8B1E22; }
        .highlight { background: #fff9e6; padding: 12px; border-radius: 8px; margin: 15px 0; }
        .footer { text-align: center; color: #999; font-size: 13px; margin-top: 30px; }
    </style>
</head>
<body>
<h1>伦理即道体：从理念到实践的完整落地指南</h1>
<p>伦理不是外在的约束，而是产品存在的根本属性，是技术的呼吸方式。本文系统阐述如何将这一核心理念转化为具体的产品开发实践。</p>
<h2>一、核心理念阐释</h2>
<p><strong>道体</strong>：指事物的本质、本体，是一切存在的根基和法则。</p>
<p><strong>伦理即道体</strong>：伦理不是外挂，而是产品的本质属性。</p>
<h2>二、核心原则体系（8项）</h2>
<p>• <strong>减法优先</strong>：如果答案不是减法，重新思考设计</p>
<p>• <strong>用户主权</strong>：选择权永远在用户手中</p>
<p>• <strong>善行无辙迹</strong>：帮助了用户，但不留痕迹</p>
<p>• <strong>坦诚透明</strong>：AI与人类分工清晰可见</p>
<p>• <strong>性分自觉</strong>：知己所能，知己所不能</p>
<p>• <strong>觉性唤醒</strong>：不灌输，只唤醒</p>
<p>• <strong>身体第一性</strong>：尊重身体节律</p>
<p>• <strong>P忠恕</strong>：北极星定位，不替用户选择</p>
<h2>三、用户主权保障</h2>
<div class="highlight">
<strong>四大权利：</strong><br>
• <strong>撤回权</strong>：阶段1-3可撤回需求<br>
• <strong>协商权</strong>：可对优先级提出申诉<br>
• <strong>退出权</strong>：随时终止流程<br>
• <strong>选择权</strong>：自主选择认知水平
</div>
<h2>四、实施路线图</h2>
<p><strong>短期目标（1-3个月）</strong>：团队培训宣贯、试点流程运行、审查制度落地</p>
<p><strong>中期目标（3-6个月）</strong>：流程优化迭代、量化指标完善、工具支持建设</p>
<p><strong>长期目标（6-12个月）</strong>：文化氛围形成、持续改进机制、行业标准输出</p>
<div class="footer">
<p>✨ TS爱心联盟 · 探索爱的真谛，让爱自由表达</p>
<p>文档版本：V1.0 | 发布日期：2026-06-09</p>
</div>
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

def push_draft(access_token):
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={access_token}"
    payload = {
        "articles": [{
            "title": TITLE,
            "author": AUTHOR,
            "digest": DIGEST,
            "content": HTML_CONTENT,
            "content_source_url": "",
            "need_open_comment": 1,
            "only_fans_can_comment": 0
        }]
    }
    response = requests.post(url, json=payload)
    result = response.json()
    if 'draft_id' in result:
        print(f"✅ 推送成功! draft_id: {result['draft_id']}")
        return result['draft_id']
    else:
        print(f"❌ 推送失败: {result}")
        return None

def check_drafts(access_token):
    url = f"https://api.weixin.qq.com/cgi-bin/draft/batchget?access_token={access_token}"
    payload = {"offset": 0, "count": 5}
    response = requests.post(url, json=payload)
    result = response.json()
    with open("draft_list.json", 'w', encoding='utf-8') as f:
        import json
        json.dump(result, f, ensure_ascii=False, indent=2)
    print("✅ 草稿列表已保存")
    if 'item' in result:
        print("\n📋 草稿箱最新文章:")
        for item in result['item'][:3]:
            print(f"- {item['title']}")
    return result

def main():
    print("="*50)
    print("📤 公众号草稿推送")
    print("="*50)
    token = get_access_token()
    if not token:
        return
    draft_id = push_draft(token)
    if not draft_id:
        return
    check_drafts(token)
    print("\n🎉 任务完成!")
    print("登录微信公众号后台 → 素材管理 → 草稿箱 查看")

if __name__ == "__main__":
    main()