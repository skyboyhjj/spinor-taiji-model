import os
import re

def sanitize_filename(filename):
    """清理文件名中的特殊字符"""
    filename = filename.replace('\u201c', '').replace('\u201d', '')
    filename = filename.replace('\u300a', '').replace('\u300b', '')
    filename = filename.replace('\uff1a', '_').replace('\uff0c', '_')
    filename = filename.replace(' ', '_')
    filename = re.sub(r'_+', '_', filename)
    filename = filename.strip('_')
    return filename

def generate_alias(filename):
    pinyin_map = {
        '伦理即道体': 'lunli-ji-daoti',
        '旋量太极看山三境界': 'spinor-taiji-three-realms',
        '心经的振动科学与觉知智慧一句一句的现代读解': 'heart-sutra-vibration',
        '道德经无死地': 'daodejing-wusidi',
        '道德经第一章': 'daodejing-chapter-1',
        '从认识道到成为道一场认知与实践的升级': 'from-knowing-to-being',
        '伦理即道体系列阅读地图与实修指南': 'lunli-reading-map',
        '微信公众号响应式表格演示': 'responsive-table-demo',
        '旋量太极模型写高考作文两篇对比版': 'gaokao-essay-spinor',
        '看山三境界核心数据表格': 'three-realms-data',
        '胃病切片': 'stomach-disease-slice',
        '色即是空空即是色认知与实践的升级': 'form-is-emptiness',
        '道德经里的思维智慧为什么为道日损': 'daodejing-dao-sun',
        '长期胃病': 'chronic-gastritis'
    }
    
    name = filename.replace('_公众号版.html', '').replace('.html', '')
    for chinese, pinyin in pinyin_map.items():
        if chinese in name or name in chinese:
            return pinyin + '.html'
    return 'article-' + str(abs(hash(name)))[:8] + '.html'

def main():
    articles_dir = 'articles'
    if not os.path.exists(articles_dir):
        print("articles directory not found")
        return
    
    renamed_count = 0
    alias_count = 0
    
    for filename in os.listdir(articles_dir):
        if filename.endswith('.html'):
            old_path = os.path.join(articles_dir, filename)
            
            if filename.startswith('article-') or ('-' in filename and '_' not in filename):
                print("Skip alias:", filename)
                continue
            
            new_name = sanitize_filename(filename)
            
            if '_微信版' in new_name:
                new_name = new_name.replace('_微信版', '_公众号版')
            elif '_公众号版' not in new_name:
                new_name = new_name.replace('.html', '_公众号版.html')
            
            new_path = os.path.join(articles_dir, new_name)
            
            if old_path != new_path:
                os.rename(old_path, new_path)
                print("Renamed:", filename, "->", new_name)
                renamed_count += 1
            else:
                print("Already OK:", filename)
            
            alias = generate_alias(new_name)
            alias_path = os.path.join(articles_dir, alias)
            
            if os.path.exists(alias_path):
                print("Alias exists:", alias)
                continue
            
            redirect_html = '''<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="refresh" content="0;url=''' + new_name + '''">
    <link rel="canonical" href="''' + new_name + '''">
</head>
<body>
    <script>window.location.href = "''' + new_name + '''";</script>
</body>
</html>'''
            
            with open(alias_path, 'w', encoding='utf-8') as f:
                f.write(redirect_html)
            print("Created alias:", alias)
            alias_count += 1
    
    print("\nDone! Renamed:", renamed_count, "Aliases:", alias_count)

if __name__ == '__