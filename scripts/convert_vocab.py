import os

def convert_vocabulary():
    input_path = 'docs/10-词汇表/旋量太极词汇表.md'
    output_path = 'docs/10-词汇表/旋量太极词汇表_微信公众号版.html'
    
    with open(input_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    lines = md_content.split('\n')
    
    html_parts = []
    html_parts.append('<!DOCTYPE html>')
    html_parts.append('<html lang="zh-CN">')
    html_parts.append('<head>')
    html_parts.append('<meta charset="UTF-8">')
    html_parts.append('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
    html_parts.append('<title>旋量-太极词汇表</title>')
    html_parts.append('<style>')
    html_parts.append('body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif; font-size: 16px; line-height: 1.8; color: #333; max-width: 680px; margin: 0 auto; padding: 20px; background: #fff; }')
    html_parts.append('h1 { font-size: 24px; font-weight: bold; text-align: center; color: #1a1a1a; margin-bottom: 10px; padding-bottom: 15px; border-bottom: 2px solid #0066cc; }')
    html_parts.append('h2 { font-size: 20px; font-weight: bold; color: #0066cc; margin-top: 30px; margin-bottom: 15px; padding-left: 10px; border-left: 4px solid #0066cc; }')
    html_parts.append('p { margin-bottom: 15px; text-indent: 2em; }')
    html_parts.append('strong { color: #0066cc; font-weight: bold; }')
    html_parts.append('blockquote { border-left: 4px solid #0066cc; padding: 15px; margin: 20px 0; color: #666; background: #f8f9fa; border-radius: 0 4px 4px 0; font-style: italic; }')
    html_parts.append('table { width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 14px; }')
    html_parts.append('th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }')
    html_parts.append('th { background: #0066cc; color: #fff; }')
    html_parts.append('tr:nth-child(even) { background: #f8f9fa; }')
    html_parts.append('.divider { border-bottom: 1px dashed #ddd; margin: 20px 0; }')
    html_parts.append('.term { display: inline-block; background: #0066cc; color: #fff; padding: 4px 10px; border-radius: 4px; font-weight: bold; font-size: 14px; margin-right: 8px; }')
    html_parts.append('.footer { margin-top: 40px; padding-top: 20px; border-top: 1px solid #eee; text-align: center; color: #888; font-size: 14px; }')
    html_parts.append('</style>')
    html_parts.append('</head>')
    html_parts.append('<body>')
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        if line.startswith('# '):
            html_parts.append('<h1>' + line[2:] + '</h1>')
        
        elif line.startswith('>'):
            html_parts.append('<blockquote>' + line[1:].strip() + '</blockquote>')
        
        elif line.startswith('---'):
            html_parts.append('<div class="divider"></div>')
        
        elif line.startswith('## '):
            html_parts.append('<h2>' + line[3:] + '</h2>')
        
        elif line.startswith('**') and line.endswith('**') and '：' in line:
            parts = line.split('：', 1)
            term = parts[0][2:]
            definition = parts[1][:-2]
            html_parts.append('<p><span class="term">' + term + '</span>：' + definition + '</p>')
        
        elif line.startswith('**') and line.endswith('**'):
            html_parts.append('<p><strong>' + line[2:-2] + '</strong></p>')
        
        elif line.startswith('| '):
            html_parts.append('<table>')
            while i < len(lines) and lines[i].startswith('|'):
                current_line = lines[i]
                cells = [c.strip() for c in current_line.split('|') if c.strip()]
                
                if current_line.startswith('| :---'):
                    i += 1
                    continue
                
                is_header = current_line.startswith('| 词汇')
                tag = 'th' if is_header else 'td'
                row_cells = []
                for cell in cells:
                    row_cells.append('<' + tag + '>' + cell + '</' + tag + '>')
                html_parts.append('<tr>' + ''.join(row_cells) + '</tr>')
                i += 1
            html_parts.append('</table>')
            continue
        
        elif line.strip() and not line.startswith('#') and not line.startswith('>') and not line.startswith('---') and not line.startswith('|'):
            html_parts.append('<p>' + line.strip() + '</p>')
        
        i += 1
    
    html_parts.append('<div class="footer">')
    html_parts.append('<p>— END —</p>')
    html_parts.append('<p>旋量-太极模型 · 名可名，非常名</p>')
    html_parts.append('</div>')
    html_parts.append('</body>')
    html_parts.append('</html>')
    
    html = '\n'.join(html_parts)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print('转换完成:', output_path)

if __name__ == '__main__':
    convert_vocabulary()