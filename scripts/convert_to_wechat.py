#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
旋量-太极模型 — 公众号版 HTML 转换脚本
用法:
  python convert_to_wechat.py statement  # 转换声明
  python convert_to_wechat.py glossary   # 转换词汇表
"""

import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
WE_CHAT_DIR = PROJECT_ROOT / "wechat"


# ============================================================
# 微信公众号样式（6月4日模板 v2.0.0 + 项目定制）
# ============================================================
_WE_CHAT_STYLE_CSS = """\
/* 基础变量 */
:root {
    --primary-color: #8B1E22;
    --secondary-color: #a82830;
    --accent-gold: #c9a227;
    --bg-color: #ffffff;
    --light-bg: #f9f9f9;
    --text-color: #333333;
    --text-secondary: #666666;
    --text-muted: #999999;
    --spacing-xs: 4px;
    --spacing-sm: 8px;
    --spacing-md: 16px;
    --spacing-lg: 24px;
    --spacing-xl: 32px;
}

/* 重置 */
* { margin: 0; padding: 0; box-sizing: border-box; }

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    line-height: 1.8;
}

/* 文章容器 */
.article-container {
    max-width: 677px;
    margin: 0 auto;
    padding: var(--spacing-md);
}

/* 标题 */
.article-title {
    font-size: 22px;
    font-weight: bold;
    color: var(--primary-color);
    text-align: center;
    letter-spacing: 0.1em;
    line-height: 1.3;
    padding: 14px 20px;
    background-image: repeating-linear-gradient(45deg, rgba(139,30,34,0.03), rgba(139,30,34,0.03) 2px, transparent 2px, transparent 8px);
    border-top: 2px solid var(--primary-color);
    border-bottom: 2px solid var(--primary-color);
    width: 90%;
    margin: 20px auto 28px;
}

.version-badge {
    display: inline-block;
    background: var(--primary-color);
    color: #fff;
    font-size: 12px;
    padding: 3px 10px;
    border-radius: 12px;
    vertical-align: middle;
    margin-left: 8px;
    font-weight: 500;
}

/* 章节标题 */
h1 {
    font-size: 22px;
    font-weight: bold;
    color: var(--primary-color);
    text-align: center;
    line-height: 1.4;
    letter-spacing: 0.08em;
    margin-bottom: 18px;
}

h2 {
    font-size: 19px;
    font-weight: bold;
    color: var(--primary-color);
    line-height: 1.3;
    letter-spacing: 0.05em;
    padding: 0 0 6px 12px;
    border-left: 4px solid var(--primary-color);
    border-bottom: 1px dashed rgba(139,30,34,0.3);
    margin: 30px 0 16px;
}

h3 {
    font-size: 17px;
    font-weight: 600;
    color: var(--primary-color);
    line-height: 1.5;
    padding: 0 0 4px 12px;
    border-left: 3px solid var(--primary-color);
    margin: 24px 0 12px;
}

h4 {
    font-size: 16px;
    font-weight: 600;
    color: #444;
    margin: 20px 0 10px;
}

/* 段落 */
p {
    font-size: 15px;
    color: var(--text-color);
    line-height: 2;
    margin-bottom: 14px;
    text-align: justify;
}

strong { font-weight: bold; color: var(--primary-color); }

/* 引用块 */
blockquote {
    margin: 16px 0;
    padding: 14px 18px;
    background: rgba(139,30,34,0.05);
    border-left: 4px solid var(--primary-color);
    font-size: 15px;
    color: var(--text-secondary);
    line-height: 1.9;
}
blockquote p { margin-bottom: 8px; }
blockquote p:last-child { margin-bottom: 0; }

/* 有序列表 */
ol { margin: 14px 0 14px 28px; }
ol li { font-size: 15px; line-height: 1.9; margin: 8px 0; }

/* 无序列表 */
ul { margin: 14px 0 14px 24px; }
ul li { font-size: 15px; line-height: 1.9; margin: 6px 0; }

/* 术语卡片 */
.term-card {
    background: linear-gradient(135deg, #fafbfc, #f5f7fa);
    border-radius: 10px;
    padding: 16px 18px;
    margin-bottom: 16px;
    border-left: 4px solid var(--primary-color);
}

.term-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 10px;
    flex-wrap: wrap;
}

.term-tag {
    background: linear-gradient(135deg, #8B1E22, #a82830);
    color: white;
    padding: 4px 12px;
    border-radius: 16px;
    font-weight: bold;
    font-size: 14px;
}

.term-category {
    font-size: 12px;
    color: #999;
    background: #f0f0f0;
    padding: 3px 8px;
    border-radius: 8px;
}

.term-definition {
    font-size: 14px;
    color: #555;
    line-height: 1.9;
    text-indent: 1.5em;
}

/* 版本信息 */
.version-module {
    background: linear-gradient(135deg, #fff9e6, #fff5cc);
    border-left: 4px solid var(--accent-gold);
    border-radius: 0 10px 10px 0;
    padding: 18px 20px;
    margin-bottom: 24px;
}

.version-title {
    font-size: 16px;
    font-weight: bold;
    color: #997700;
    margin-bottom: 14px;
}

.version-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
}

.version-item {
    background: rgba(255,255,255,0.8);
    padding: 10px 14px;
    border-radius: 6px;
}

.version-label { font-size: 11px; color: #999; margin-bottom: 3px; }
.version-value { font-size: 13px; font-weight: bold; color: #333; }

/* 表格 */
.article-table {
    width: 100%;
    border-collapse: collapse;
    margin: 18px 0;
    font-size: 13px;
    overflow-x: auto;
    display: block;
}

.article-table thead th {
    background: linear-gradient(to bottom, rgba(139,30,34,0.12), rgba(139,30,34,0.04));
    padding: 10px 12px;
    border-bottom: 2px solid rgba(139,30,34,0.4);
    text-align: left;
    font-weight: bold;
    color: var(--primary-color);
    white-space: nowrap;
}

.article-table tbody td {
    padding: 9px 12px;
    border-bottom: 1px solid rgba(139,30,34,0.08);
    color: var(--text-color);
    line-height: 1.6;
}

.article-table tbody tr:nth-child(even) { background: var(--light-bg); }

/* 分隔线 */
hr {
    margin: 28px auto;
    height: 1px;
    background: linear-gradient(to right, rgba(139,30,34,0), rgba(139,30,34,0.4), rgba(139,30,34,0));
    border: none;
    width: 80%;
}

/* 图片 */
img { max-width: 100%; height: auto; display: block; margin: 16px auto; }

/* 标签 */
.tag-label { font-weight: 600; }
.tag-label.blue { color: #1e88e5; }
.tag-label.green { color: #43a047; }
.tag-label.orange { color: #fb8c00; }

/* 引言区 */
.intro-section {
    background: linear-gradient(135deg, var(--primary-color), #0088dd);
    color: white;
    padding: 32px 28px;
    border-radius: 12px;
    margin-bottom: 28px;
}

.intro-title {
    font-size: 26px;
    font-weight: bold;
    text-align: center;
    margin-bottom: 14px;
}

.intro-subtitle {
    font-size: 14px;
    opacity: 0.9;
    text-align: center;
    font-style: italic;
    line-height: 1.8;
}

/* 底部信息 */
.article-footer {
    margin-top: 40px;
    padding-top: 20px;
    border-top: 1px solid #eee;
    text-align: center;
    color: #999;
    font-size: 13px;
}

/* 打印 */
@media print {
    .article-container { max-width: 100%; padding: 0; }
}
"""

_WE_CHAT_STYLE_TAG = '<style>\n' + _WE_CHAT_STYLE_CSS + '\n</style>\n'


def read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def clean_html(html: str) -> str:
    """彻底清理：移除所有 style、script、iframe 等非正文元素"""
    # 移除所有 <style>...</style> 块（逐块，防止跨块匹配）
    while True:
        start = re.search(r"<style", html, re.IGNORECASE)
        if not start:
            break
        end = re.search(r"</style>", html[start.start()+1:], re.IGNORECASE)
        if not end:
            html = html[:start.start()]
            break
        html = html[:start.start()] + html[start.start() + len(start.group()) + end.start() + len(end.group()) + 1:]
    # 移除所有 <script>...</script> 块
    while True:
        start = re.search(r"<script", html, re.IGNORECASE)
        if not start:
            break
        end = re.search(r"</script>", html[start.start()+1:], re.IGNORECASE)
        if not end:
            html = html[:start.start()]
            break
        html = html[:start.start()] + html[start.start() + len(start.group()) + end.start() + len(end.group()) + 1:]
    return html


def remove_by_class(html: str, cls: str) -> str:
    """移除所有 class 属性中包含 cls 的元素及其内容"""
    pattern = rf'<(\w+)[^>]*class="[^"]*\b{re.escape(cls)}\b[^"]*"[^>]*>[\s\S]*?</\1>'
    result = re.sub(pattern, "", html, flags=re.IGNORECASE)
    # 清理残留空 class
    result = re.sub(rf'class="[^"]*\b{re.escape(cls)}\b[^"]*"', "", result)
    return result


def remove_by_id(html: str, id_name: str) -> str:
    """移除指定 id 的元素"""
    return re.sub(
        rf'<\w+[^>]*id="{re.escape(id_name)}"[^>]*>[\s\S]*?</\w+>',
        "", html, flags=re.IGNORECASE
    )


def remove_by_tag(html: str, tag: str) -> str:
    """移除指定 HTML 标签及其内容（支持自闭合）"""
    # 先处理非自闭合标签
    result = re.sub(
        rf"<{tag}(?![a-zA-Z0-9_-])[^>]*>[\s\S]*?</{tag}>",
        "", html, flags=re.IGNORECASE
    )
    # 清理残留空 class 属性
    result = re.sub(rf'\s*class=""\s*', " ", result)
    return result


def extract_body(html: str) -> str:
    """提取 <body>...</body> 内容"""
    m = re.search(r"<body[^>]*>([\s\S]*?)</body>", html, re.IGNORECASE)
    return m.group(1).strip() if m else html


def build_document(content: str) -> str:
    """包裹为完整 HTML 文档"""
    return (
        "<!DOCTYPE html>\n"
        '<html lang="zh-CN">\n'
        "<head>\n"
        '<meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        "<title></title>\n"
        + _WE_CHAT_STYLE_TAG
        + "</head>\n"
        "<body>\n"
        '<div class="article-container">\n'
        + content.strip()
        + "\n</div>\n"
        "</body>\n"
        "</html>"
    )


# ============================================================
# 声明页转换
# ============================================================
def convert_statement():
    src = PROJECT_ROOT / "articles/zh/spinor-taiji-model-statement.html"
    dst = WE_CHAT_DIR / "旋量-太极模型声明_v1.2_公众号版.html"

    html = read_file(str(src))
    html = clean_html(html)          # 移除 CSS/JS
    html = extract_body(html)        # 提取 body

    # 移除所有浮动和反馈相关元素
    for cls in [
        "feedback-float", "feedback-overlay", "feedback-section",
        "nav-buttons", "back-to-top", "back-to-home",
        "footer",
    ]:
        html = remove_by_class(html, cls)

    # 清理空标签
    html = re.sub(r">\s*<", "><", html)
    html = re.sub(r"\s+", " ", html)

    with open(dst, "w", encoding="utf-8") as f:
        f.write(build_document(html))
    print(f"[OK] 声明已生成: {dst}")


# ============================================================
# 词汇表转换
# ============================================================
def convert_glossary():
    src = PROJECT_ROOT / "articles/zh/spinor-taiji-glossary.html"
    dst = WE_CHAT_DIR / "旋量-太极词汇表_v1.1.0_公众号版.html"

    html = read_file(str(src))
    html = clean_html(html)          # 移除 CSS/JS
    html = extract_body(html)        # 提取 body

    # 移除页面框架元素
    for cls in [
        "header-content", "search-box", "sidebar", "sidebar-title",
        "nav-list", "nav-item", "nav-buttons",
        "back-to-top", "back-to-home",
        "feedback-float", "feedback-overlay", "feedback-section",
        "feedback-form-group", "feedback-form", "feedback-success",
        "feedback-submit", "feedback-modal", "feedback-modal-close",
        "footer-text", "footer",
        "relation-graph", "graph-container",
    ]:
        html = remove_by_class(html, cls)

    # 按标签移除 header / footer / aside / svg
    for tag in ["header", "footer", "aside", "svg"]:
        html = remove_by_tag(html, tag)

    # 按 id 移除
    for sid in ["graph"]:
        html = remove_by_id(html, sid)

    # 移除孤立图形相关 div
    for cls in ["graph-title", "graph-hint", "legend", "legend-item", "legend-color"]:
        html = remove_by_class(html, cls)

    # 移除"经典读解"章节（id="classic"）
    html = remove_by_id(html, "classic")

    # 清理空标签
    html = re.sub(r">\s*<", "><", html)
    html = re.sub(r"\s+", " ", html)

    with open(dst, "w", encoding="utf-8") as f:
        f.write(build_document(html))
    print(f"[OK] 词汇表已生成: {dst}")


if __name__ == "__main__":
    WE_CHAT_DIR.mkdir(parents=True, exist_ok=True)
    mode = sys.argv[1] if len(sys.argv) > 1 else "both"
    if mode in ("statement", "both"):
        convert_statement()
    if mode in ("glossary", "both"):
        convert_glossary()
    print(f"\n产物目录: {WE_CHAT_DIR}")
