#!/usr/bin/env python3
"""融合新旧词汇表：将 V1.1.0 内容嵌入旧版框架，保留所有交互功能（方案A）"""

import re
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

# V1.1.0 章节标题 -> section id 映射
SECTION_ID_MAP = {
    "一、频谱一元论：全景框架": "spectrum",
    "二、频谱频段：从高到低的显化": "freq",
    "三、底层操作：旋量与矢量": "basic",
    "四、觉知与信息：不在频谱上的维度": "awareness",
    "五、时间：平方与开方的节律": "time",
    "六、存在主体：谁在振动？": "existence",
    "七、生命状态：频谱的相干与卡顿": "life",
    "八、关系：振动之间的相位": "relation",
    "九、心灵操作：自主的平方与开方": "mind",
    "十、经典读解：圣人的旋量操作": "classic",
}

# 简化标题（用于侧边栏显示）
def clean_title(full_title):
    """从完整标题中提取简化标题"""
    if '：' in full_title:
        parts = full_title.split('：', 1)
        num_part = parts[0]  # e.g., "一、频谱一元论"
        # 去掉序号前缀
        import re as re_mod
        cleaned = re_mod.sub(r'^[一二三四五六七八九十]+、', '', num_part)
        return cleaned
    return full_title

def extract_v11_sections(html):
    """从 V1.1.0 HTML 中提取所有 <section> 块"""
    # 找到 container div 内的所有 section
    container_start = html.find('<div class="container">')
    container_end = html.find('</div>', html.rfind('</footer>'))
    if container_end < 0:
        container_end = len(html)
    body = html[container_start:container_end]
    
    sections = []
    # 匹配 <!-- comment -->\n<section>...</section> 模式
    pattern = re.compile(r'<!--\s*(.*?)\s*-->\s*<section>(.*?)</section>', re.DOTALL)
    for m in pattern.finditer(body):
        comment = m.group(1).strip()
        section_html = m.group(2)
        sections.append({
            'comment': comment,
            'html': section_html
        })
    
    return sections

def parse_glossary_items(section_html):
    """解析 section 中的 glossary-item 块"""
    # 提取 h2 标题
    h2_match = re.search(r'<h2>(.*?)</h2>', section_html)
    title = h2_match.group(1) if h2_match else ""
    
    items = []
    # 提取所有 glossary-item
    item_pattern = re.compile(
        r'<div class="glossary-item">(.*?)</div>\s*'
        r'(?=\s*</section>|\s*<div class="glossary-item">|$)',
        re.DOTALL
    )
    for m in item_pattern.finditer(section_html):
        items.append(m.group(1))
    
    return title, items

def parse_term_card(item_html):
    """将新版 glossary-item HTML 解析为结构化数据"""
    # 提取 term id 和名称
    term_match = re.search(r'<div class="term"[^>]*id="([^"]*)"[^>]*>(.*?)</div>', item_html)
    if not term_match:
        term_match = re.search(r'<div class="term"[^>]*>(.*?)</div>', item_html)
    term_id = term_match.group(1) if term_match and 'id=' in item_html else ""
    term_name = term_match.group(1) if term_match else ""
    # 如果 term_name 包含 id 属性，重新提取
    if 'id="' in str(term_name):
        term_id = re.search(r'id="([^"]*)"', str(term_name))
        term_id = term_id.group(1) if term_id else ""
        term_name = re.search(r'>(.*?)</div>', str(term_name))
        term_name = term_name.group(1) if term_name else ""
    
    # 提取定义项
    definitions = []
    def_pattern = re.compile(
        r'<li class="definition-item (\w+)">(.*?)</li>',
        re.DOTALL
    )
    for dm in def_pattern.finditer(item_html):
        def_type = dm.group(1)
        def_content = dm.group(2)
        
        # 提取标签文本
        tag_match = re.search(
            r'<span class="tag[^"]*">\s*<span class="tag-icon"></span>\s*(.*?)\s*</span>',
            def_content
        )
        tag_text = tag_match.group(1).strip() if tag_match else ""
        
        # 提取定义文本
        text_match = re.search(
            r'<p class="definition-text">(.*?)</p>',
            def_content,
            re.DOTALL
        )
        def_text = text_match.group(1).strip() if text_match else ""
        
        # 标签颜色类
        tag_class_map = {
            'physical': 'tag-physical',
            'philosophy': 'tag-philosophy',
            'extension': 'tag-extension'
        }
        
        definitions.append({
            'type': def_type,
            'tag': tag_text,
            'tag_class': tag_class_map.get(def_type, ''),
            'text': def_text
        })
    
    # 提取相关词条
    related_terms = []
    related_match = re.search(
        r'<div class="related-terms">(.*?)</div>',
        item_html,
        re.DOTALL
    )
    if related_match:
        link_pattern = re.compile(r'<a href="([^"]+)">([^<]+)</a>')
        for lm in link_pattern.finditer(related_match.group(1)):
            related_terms.append({
                'href': lm.group(1),
                'text': lm.group(2)
            })
    
    return {
        'id': term_id,
        'name': term_name,
        'definitions': definitions,
        'related': related_terms
    }

def get_category(term_id, term_name):
    """根据词条 ID 或名称确定分类标签"""
    spectrum_ids = {'频谱一元论', '旋量旋转'}
    freq_ids = {'神', '思想', '情绪', '气', '能量', '精', '物质', '精气神'}
    awareness_ids = {'意识', '域/觉知', '信息', '经络'}
    operation_ids = {'旋量', '矢量', '平方', '开方', '720°复原', '360°翻转', '正负双解'}
    time_ids = {'时间', '过去', '未来', '当下'}
    existence_ids = {'我', '呼吸', '身体'}
    life_ids = {'生生之厚', '含德之厚', '精之至', '和之至', '有死地', '无死地', '临在', '心流'}
    relation_ids = {'爱', '共情', '善', '不善', '善人/不善人', '祸/福'}
    mind_ids = {'修行', '无欲/有欲', '欲', '闷闷/察察', '反者道之动', '弱者道之用'}
    classic_ids = {'善行无辙迹', '道生一', '物壮则老', '出生入死'}
    
    name = term_name or term_id
    if term_id in spectrum_ids or name in spectrum_ids:
        return '全景框架'
    if term_id in freq_ids or name in freq_ids:
        return '频谱频段'
    if term_id in awareness_ids or name in awareness_ids:
        return '觉知与信息'
    if term_id in operation_ids or name in operation_ids:
        return '底层操作'
    if term_id in time_ids or name in time_ids:
        return '时间概念'
    if term_id in existence_ids or name in existence_ids:
        return '主体概念'
    if term_id in life_ids or name in life_ids:
        return '生命状态'
    if term_id in relation_ids or name in relation_ids:
        return '关系概念'
    if term_id in mind_ids or name in mind_ids:
        return '心灵操作'
    if term_id in classic_ids or name in classic_ids:
        return '经典解读'
    return '基础概念'

def build_term_card_html(card):
    """生成旧版 term-card HTML"""
    cat = get_category(card['id'], card['name'])
    
    lines = []
    lines.append(f'<div class="term-card" data-term="{card["name"]}">')
    lines.append(f'<div class="term-header"><span class="term-tag">{card["name"]}</span><span class="term-category">{cat}</span></div>')
    
    for d in card['definitions']:
        # 标签前缀
        tag_label = d['tag']
        if tag_label in ('物理事实', '文化事实'):
            prefix = '🔵 ' + tag_label
        elif tag_label == '哲学类比':
            prefix = '🟢 ' + tag_label
        elif tag_label == '创见延伸':
            prefix = '🟠 ' + tag_label
        else:
            prefix = tag_label
        
        lines.append(f'<p class="term-definition"><strong>{prefix}</strong>：{d["text"]}</p>')
    
    if card['related']:
        related_links = ' · '.join([
            f'<a href="{r["href"]}" class="related-link">{r["text"]}</a>'
            for r in card['related']
        ])
        lines.append(f'<div class="related-terms"><strong>相关词条：</strong>{related_links}</div>')
    
    lines.append('</div>')
    return '\n'.join(lines)

def extract_quick_ref_table(html):
    """从 V1.1.0 HTML 提取快速检索表"""
    start = html.find('<!-- 附：快速检索表 -->')
    if start < 0:
        return ""
    
    section_start = html.find('<section>', start)
    section_end = html.find('</section>', section_start)
    if section_end < 0:
        return ""
    
    section_html = html[section_start:section_end + len('</section>')]
    
    # 提取 h2 和 table
    h2_match = re.search(r'<h2>(.*?)</h2>', section_html)
    title = h2_match.group(1) if h2_match else "快速检索表"
    
    table_start = section_html.find('<table')
    table_end = section_html.find('</table>', table_start)
    if table_end < 0:
        return section_html
    
    table_html = section_html[table_start:table_end + len('</table>')]
    
    # 转换为旧版表格样式
    table_html = table_html.replace('class="reference-table"', 'style="width:100%;border-collapse:collapse;"')
    table_html = table_html.replace('class="category"', '')
    
    # 去掉标签列中的 span 标签
    table_html = re.sub(r'<span class="tag-box \w+"></span>', '', table_html)
    
    # 简化表头（去掉标签列）
    table_html = re.sub(
        r'<thead>.*?</thead>',
        '<thead><tr><th style="background:#0066cc;color:white;padding:12px;text-align:left;">分类</th><th style="background:#0066cc;color:white;padding:12px;text-align:left;">词汇</th><th style="background:#0066cc;color:white;padding:12px;text-align:left;">一句定义</th></tr></thead>',
        table_html,
        flags=re.DOTALL
    )
    
    # 去掉标签列：匹配每行最后一个 <td>（标签列，已被清空为 <td></td>）
    # 使用模式：<td></td></tr> -> </tr>，只匹配行尾的空标签列
    table_html = re.sub(r'<td>\s*</td>\s*</tr>', '</tr>', table_html)
    
    return table_html

def main():
    old_path = os.path.join(PROJECT_ROOT, 'articles', 'zh', 'spinor-taiji-glossary.html')
    new_path = os.path.join(PROJECT_ROOT, 'docs', '10-词汇表', '旋量-太极词汇表_v1.1.0.html')
    output_path = old_path  # 直接覆盖旧文件
    
    old_html = read_file(old_path)
    new_html = read_file(new_path)
    
    # ===== 第一步：从 V1.1.0 提取内容 =====
    sections = extract_v11_sections(new_html)
    print(f"提取到 {len(sections)} 个章节")
    
    # 解析所有章节
    all_sections = []
    for sec in sections:
        title, items = parse_glossary_items(sec['html'])
        if not title or not items:
            continue
        
        section_id = SECTION_ID_MAP.get(title, 'basic')
        short_title = clean_title(title)
        
        cards_html = []
        for item_html in items:
            card = parse_term_card(item_html)
            cards_html.append(build_term_card_html(card))
        
        all_sections.append({
            'id': section_id,
            'title': title,
            'short_title': short_title,
            'cards': '\n'.join(cards_html)
        })
        print(f"  - {title} ({section_id}): {len(items)} 个词条")
    
    # ===== 第二步：构建新内容区域 =====
    new_sections_html = []
    for sec in all_sections:
        new_sections_html.append(f'''<div id="{sec['id']}" class="section">
<h2 class="section-title">{sec['title']}</h2>
{sec['cards']}
</div>''')
    
    new_content = '\n'.join(new_sections_html)
    
    # 快速检索表
    quick_table = extract_quick_ref_table(new_html)
    new_quick_section = f'<div id="quick" class="section">\n<h2 class="section-title">📊 快速检索表</h2>\n{quick_table}\n</div>'
    
    # ===== 第三步：定位旧版中的插入点 =====
    # 保留：intro, version, graph
    # 找到 graph section 结束的位置
    graph_end_match = re.search(r'<div id="graph" class="relation-graph">.*?</div>\s*</div>', old_html, re.DOTALL)
    if not graph_end_match:
        print("ERROR: 找不到 relation-graph 结束位置")
        return
    
    insert_pos = graph_end_match.end()
    
    # 找到 </main> 前的内容结束位置
    main_end = old_html.find('</main>')
    if main_end < 0:
        print("ERROR: 找不到 </main>")
        return
    
    # ===== 第四步：拼接 =====
    # 头部（到 graph 结束）
    head = old_html[:insert_pos]
    # 尾部（从 </main> 开始）
    tail = old_html[main_end:]
    
    merged_html = head + '\n' + new_content + '\n' + new_quick_section + '\n' + tail
    
    # ===== 第五步：更新侧边栏 =====
    sidebar_items = [
        '<li class="nav-item active" data-section="intro">引言</li>',
        '<li class="nav-item " data-section="version">版本</li>',
        '<li class="nav-item " data-section="graph">图形</li>',
    ]
    for sec in all_sections:
        sidebar_items.append(
            f'<li class="nav-item " data-section="{sec["id"]}">{sec["short_title"]}</li>'
        )
    sidebar_items.append('<li class="nav-item " data-section="quick">快速</li>')
    
    new_sidebar = '\n'.join(sidebar_items)
    
    # 替换侧边栏中的 nav-list 内容
    nav_start = merged_html.find('<ul class="nav-list">')
    nav_end = merged_html.find('</ul>', nav_start)
    if nav_start > 0 and nav_end > 0:
        merged_html = (
            merged_html[:nav_start + len('<ul class="nav-list">')] +
            '\n' + new_sidebar + '\n' +
            merged_html[nav_end:]
        )
    
    # ===== 第六步：更新版本信息 =====
    merged_html = merged_html.replace('v1.0.0', 'v1.1.0')
    merged_html = merged_html.replace('初始版本', '三层标签升级版')
    merged_html = merged_html.replace('2026年6月22日', '2026年6月23日')
    
    # ===== 第七步：添加相关词条样式 =====
    related_style = '''
.related-terms { margin-top: 12px; padding-top: 12px; border-top: 1px dashed #ddd; }
.related-terms strong { color: #7f8c8d; font-size: 0.9em; }
.related-link { color: #3498DB; text-decoration: none; margin-right: 10px; transition: color 0.2s; }
.related-link:hover { color: #2980B9; text-decoration: underline; }'''
    
    style_end = merged_html.find('</style>')
    if style_end > 0:
        merged_html = merged_html[:style_end] + related_style + '\n' + merged_html[style_end:]
    
    # ===== 第八步：添加相关词条点击跳转 JS =====
    new_js = '''
// === V1.1.0 相关词条跳转逻辑 ===
document.querySelectorAll('.related-link').forEach(link => {
  link.addEventListener('click', function(e) {
    e.preventDefault();
    const href = this.getAttribute('href');
    if (!href || !href.startsWith('#')) return;
    
    const targetId = href.replace('#', '');
    
    // 方法1: 通过 data-term 属性匹配
    const targetCard = document.querySelector(`[data-term="${targetId}"]`);
    if (targetCard) {
      document.querySelectorAll('.term-card').forEach(card => card.classList.remove('highlight-card'));
      targetCard.classList.add('highlight-card');
      targetCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
      setTimeout(() => targetCard.classList.remove('highlight-card'), 1200);
      return;
    }
    
    // 方法2: 通过 term-tag 文本匹配
    const allCards = document.querySelectorAll('.term-card');
    for (let card of allCards) {
      const tag = card.querySelector('.term-tag');
      if (tag && tag.textContent.trim() === targetId) {
        card.classList.add('highlight-card');
        card.scrollIntoView({ behavior: 'smooth', block: 'center' });
        setTimeout(() => card.classList.remove('highlight-card'), 1200);
        return;
      }
    }
    
    // 方法3: 直接通过 id 跳转
    const targetEl = document.getElementById(targetId);
    if (targetEl) {
      targetEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  });
});'''
    
    # 找到最后一个 </script> 之前插入
    last_script_end = merged_html.rfind('</script>')
    if last_script_end > 0:
        merged_html = merged_html[:last_script_end] + new_js + '\n' + merged_html[last_script_end:]
    
    # ===== 第九步：写入文件 =====
    write_file(output_path, merged_html)
    print(f"\n融合完成！输出: {output_path}")
    print(f"共 {len(all_sections)} 个章节，{sum(len(parse_glossary_items(s['html'])[1]) for s in sections if parse_glossary_items(s['html'])[1])} 个词条")

if __name__ == '__main__':
    main()