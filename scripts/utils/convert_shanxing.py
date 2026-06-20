#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将善行无辙迹文章转换为微信公众号HTML格式
"""

import sys
sys.path.insert(0, r'.trae\skills\wechat-typeset-pro\scripts')

from markdown_parser import EnhancedMarkdownParser

def main():
    # 读取Markdown文件
    md_path = r'e:\Trac Project\07- Spinor-Taiji model读解道德经\善行无辙迹_公众号版.md'
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # 解析Markdown
    parser = EnhancedMarkdownParser()
    html_content = parser.parse(md_content)

    # 添加微信公众号样式
    full_html = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; padding: 20px; max-width: 900px; margin: 0 auto; background: #fff; color: #333; line-height: 2; font-size: 15px; }
        h1 { text-align: center; border-top: 2px solid #8B1E22; border-bottom: 2px solid #8B1E22; padding: 15px 0; margin: 20px 0; font-size: 22px; color: #333; }
        h2 { border-left: 4px solid #8B1E22; padding-left: 12px; margin: 25px 0 15px; font-size: 20px; color: #333; border-bottom: 1px dashed #ddd; padding-bottom: 8px; }
        h3 { font-size: 16px; margin: 20px 0 10px; color: #8B1E22; }
        p { margin: 15px 0; text-indent: 2em; }
        strong { color: #8B1E22; font-weight: bold; }
        blockquote { border-left: 4px solid #8B1E22; padding-left: 15px; margin: 20px 0; color: #666; font-style: italic; background: #f9f9f9; padding: 10px 15px; }
        ul, ol { margin: 15px 0; padding-left: 30px; }
        li { margin: 10px 0; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 14px; }
        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
        th { background: #f5f5f5; color: #8B1E22; }
        tr:nth-child(even) { background: #f9f9f9; }
        .separator { text-align: center; margin: 30px 0; color: #ddd; }
        .tags { margin-top: 30px; padding: 15px; background: #f9f9f9; border-radius: 8px; }
        .tags span { display: inline-block; background: #8B1E22; color: white; padding: 5px 12px; border-radius: 20px; margin: 5px; font-size: 13px; }
        .footer { margin-top: 30px; padding-top: 20px; border-top: 1px dashed #ddd; text-align: center; color: #999; font-size: 13px; }
        @media (max-width: 600px) { body { padding: 15px; font-size: 14px; } h1 { font-size: 18px; } h2 { font-size: 16px; } }
    </style>
</head>
<body>
''' + html_content + '''
</body>
</html>'''

    # 保存HTML文件
    html_path = r'e:\Trac Project\07- Spinor-Taiji model读解道德经\善行无辙迹_公众号专业版.html'
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(full_html)

    print(f'✅ HTML文件已生成: {html_path}')
    print(f'📝 内容长度: {len(full_html)} 字符')

if __name__ == '__main__':
    main()
