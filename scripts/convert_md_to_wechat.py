import os

def main():
    input_path = r'docs/《旋量-太极模型声明》.md'
    output_path = r'docs/旋量-太极模型声明_微信公众号版.html'
    
    with open(input_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>旋量-太极模型声明</title>
<style>
body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif; font-size: 16px; line-height: 1.8; color: #333; max-width: 680px; margin: 0 auto; padding: 20px; background: #fff; }
h1 { font-size: 24px; font-weight: bold; text-align: center; color: #1a1a1a; margin-bottom: 10px; padding-bottom: 15px; border-bottom: 2px solid #0066cc; }
h2 { font-size: 20px; font-weight: bold; color: #0066cc; margin-top: 30px; margin-bottom: 15px; padding-left: 10px; border-left: 4px solid #0066cc; }
h3 { font-size: 18px; font-weight: bold; color: #333; margin-top: 25px; margin-bottom: 12px; }
h4 { font-size: 16px; font-weight: bold; color: #444; margin-top: 20px; margin-bottom: 10px; }
p { margin-bottom: 15px; text-indent: 2em; }
strong { color: #0066cc; font-weight: bold; }
blockquote { border-left: 4px solid #0066cc; padding: 15px; margin: 20px 0; color: #666; background: #f8f9fa; border-radius: 0 4px 4px 0; }
table { width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 14px; }
th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
th { background: #0066cc; color: #fff; }
tr:nth-child(even) { background: #f8f9fa; }
a { color: #0066cc; text-decoration: none; }
.footer { margin-top: 40px; padding-top: 20px; border-top: 1px solid #eee; text-align: center; color: #888; font-size: 14px; }
.tag-blue { color: #1e88e5; font-weight: bold; }
.tag-green { color: #43a047; font-weight: bold; }
.tag-orange { color: #fb8c00; font-weight: bold; }
</style>
</head>
<body>
'''
    
    lines = md_content.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i]
        
        if line.startswith('## 《') and line.endswith('》'):
            title = line[3:-1]
            html += '<h1>' + title + '</h1>'
        
        elif line.startswith('> **版本**'):
            html += '<div style="text-align:center;color:#888;font-size:14px;margin-bottom:30px;">'
            html += line.replace('> **', '').replace('**', '')
            i += 1
            while i < len(lines) and lines[i].startswith('> '):
                html += ' | ' + lines[i].replace('> ', '').replace('**', '')
                i += 1
            html += '</div>'
            continue
        
        elif line.startswith('### 一、') or line.startswith('### 二、') or line.startswith('### 三、') or line.startswith('### 四、') or line.startswith('### 五、') or line.startswith('### 六、'):
            html += '<h2>' + line[4:] + '</h2>'
        
        elif line.startswith('#### 2.') or line.startswith('#### 3.'):
            html += '<h3>' + line[5:] + '</h3>'
        
        elif line.startswith('**') and line.endswith('**'):
            html += '<p><strong>' + line[2:-2] + '</strong></p>'
        
        elif line.startswith('- **🔵'):
            html += '<p><span class="tag-blue">🔵</span> ' + line[6:].replace('**', '') + '</p>'
        
        elif line.startswith('- **🟢'):
            html += '<p><span class="tag-green">🟢</span> ' + line[6:].replace('**', '') + '</p>'
        
        elif line.startswith('- **🟠'):
            html += '<p><span class="tag-orange">🟠</span> ' + line[6:].replace('**', '') + '</p>'
        
        elif line.startswith('- ') and not line.startswith('- **'):
            html += '<p style="text-indent:0;">• ' + line[2:] + '</p>'
        
        elif line.startswith('| '):
            html += '<table>'
            while i < len(lines) and line.startswith('|'):
                cells = [c.strip() for c in line.split('|') if c.strip()]
                if line.startswith('| :---'):
                    i += 1
                    line = lines[i] if i < len(lines) else ''
                    continue
                is_header = i < len(lines)-1 and lines[i+1].startswith('| :---')
                tag = 'th' if is_header else 'td'
                html += '<tr>' + ''.join(['<' + tag + '>' + c + '</' + tag + '>' for c in cells]) + '</tr>'
                i += 1
                line = lines[i] if i < len(lines) else ''
            html += '</table>'
            continue
        
        elif line.startswith('>'):
            html += '<blockquote>' + line[1:].strip() + '</blockquote>'
        
        elif line.strip() and not line.startswith('#'):
            if line[0].isdigit() and '.' in line:
                html += '<h4>' + line + '</h4>'
            else:
                html += '<p>' + line.strip() + '</p>'
        
        i += 1
    
    html += '''
<div class="footer">
<p>— END —</p>
<p>旋量-太极模型 · 以旋量之镜，照太极之道</p>
</div>
</body>
</html>'''
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print('微信公众号文章已生成：' + output_path)

if __name__ == '__main__':
    main()