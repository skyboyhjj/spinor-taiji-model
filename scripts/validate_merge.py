#!/usr/bin/env python3
"""验证融合后的词汇表 HTML 文件"""
import re

with open(r'E:\Trac Project\spinor-taiji-model\articles\zh\spinor-taiji-glossary.html', 'r', encoding='utf-8') as f:
    html = f.read()

print('=' * 60)
print('  融合验证报告')
print('=' * 60)
print()

# 1. 检查旧功能是否保留
checks = [
    ('搜索框 searchInput', 'id="searchInput"'),
    ('侧边栏导航 nav-list', 'class="nav-list"'),
    ('引言区域 intro', 'id="intro"'),
    ('版本模块 version', 'id="version"'),
    ('关系图 graph', 'id="graph"'),
    ('返回顶部 backToTop', 'id="backToTop"'),
    ('返回首页 backToHome', 'id="backToHome"'),
    ('页脚 footer', '<footer>'),
    ('搜索 JS', 'searchInput.addEventListener'),
    ('导航 JS', 'navItems.forEach'),
    ('关系图点击 JS', 'clickable-node'),
    ('相关词条跳转 JS', 'related-link'),
]

print('1. 旧功能保留检查:')
all_ok = True
for name, pattern in checks:
    status = 'OK' if pattern in html else 'FAIL'
    if status == 'FAIL':
        all_ok = False
    print(f'  [{status}] {name}')

# 2. 检查 V1.1.0 新内容
print()
print('2. V1.1.0 新词条检查:')
new_terms = ['频谱一元论', '旋量旋转', '神', '思想', '情绪', '气', '能量', '精', '物质', '精气神', '意识', '信息', '经络']
for term in new_terms:
    status = 'OK' if 'data-term="{}"'.format(term) in html else 'FAIL'
    if status == 'FAIL':
        all_ok = False
    print(f'  [{status}] {term}')

# 3. 检查版本号
print()
print('3. 版本信息:')
if 'v1.1.0' in html:
    print('  [OK] 版本号: v1.1.0')
else:
    print('  [FAIL] 版本号未更新')
    all_ok = False
if '三层标签升级版' in html:
    print('  [OK] 版本状态: 三层标签升级版')
else:
    print('  [FAIL] 版本状态未更新')
    all_ok = False
if '2026年6月23日' in html:
    print('  [OK] 日期: 2026年6月23日')
else:
    print('  [FAIL] 日期未更新')
    all_ok = False

# 4. 检查侧边栏与内容 id 一致性
nav_ids = re.findall(r'data-section="([^"]+)"', html)
section_ids = re.findall(r'<div id="([^"]+)" class="(?:section|intro-section|version-module|relation-graph)"', html)
print()
print('4. 侧边栏导航 ID 一致性:')
for nav_id in nav_ids:
    if nav_id in section_ids:
        print(f'  [OK] {nav_id} -> 对应内容区域存在')
    else:
        print(f'  [FAIL] {nav_id} -> 找不到对应内容区域')
        all_ok = False

# 5. 检查关系图节点目标
term_names = set(re.findall(r'data-term="([^"]+)"', html))
graph_section = html[html.find('<g class="graph-nodes">'):html.find('</g>')]
graph_targets = re.findall(r'data-target="([^"]+)"', graph_section)
print()
print('5. 关系图节点目标验证:')
for target in graph_targets:
    if target in term_names:
        print(f'  [OK] {target} -> term-card 存在')
    else:
        print(f'  [FAIL] {target} -> 找不到 term-card')
        all_ok = False

# 6. 检查相关词条链接
print()
print('6. 相关词条链接抽样检查:')
related_links = re.findall(r'<a href="([^"]+)" class="related-link">', html)
print(f'  相关词条链接总数: {len(related_links)}')
# 检查链接格式
invalid_links = [l for l in related_links if not l.startswith('#')]
if invalid_links:
    print(f'  [FAIL] 发现非内部链接: {invalid_links[:5]}')
    all_ok = False
else:
    print('  [OK] 所有链接均为内部锚点链接')

# 7. 统计
print()
print('7. 统计:')
print(f'  词条总数: {len(term_names)}')
print(f'  侧边栏项: {len(nav_ids)}')
print(f'  关系图节点: {len(graph_targets)}')
print(f'  章节数: {len(section_ids)}')
print(f'  相关词条链接: {len(related_links)}')

# 8. 最终结果
print()
print('=' * 60)
if all_ok:
    print('  验证结果: 全部通过!')
else:
    print('  验证结果: 存在 FAIL 项，请检查')
print('=' * 60)