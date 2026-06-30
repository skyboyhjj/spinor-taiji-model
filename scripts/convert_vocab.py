#!/usr/bin/env python3
"""
旋量-太极词汇表 Markdown 转 HTML 转换脚本
将词汇表 Markdown 文件转换为带有完整交互功能的 HTML 页面
"""

import os
import re
import json
from datetime import datetime

# 项目路径配置
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOCAB_MD_PATH = os.path.join(PROJECT_ROOT, 'docs', '10-词汇表', '旋量-太极模型 词汇表2-1-2.md')
OUTPUT_ZH_PATH = os.path.join(PROJECT_ROOT, 'articles', 'zh', 'spinor-taiji-glossary.html')
OUTPUT_EN_PATH = os.path.join(PROJECT_ROOT, 'articles', 'en', 'spinor-taiji-glossary.html')

# 版本信息
VERSION = "2.1.2"
RELEASE_DATE = "2026年6月30日"
RELEASE_DATE_EN = "June 30, 2026"

def parse_markdown_vocab(md_path):
    """解析 Markdown 词汇表文件"""
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 解析目录结构（中文数字序号）
    categories = []
    # 匹配格式: | 一 | [体-相-用核心架构](#一体-相-用核心架构) | 12 |
    category_pattern = r'\| ([一二三四五六七八九十]+) \| \[([^\]]+)\]\(#[^\)]+\) \| (\d+) \|'
    chinese_to_num = {'一': '1', '二': '2', '三': '3', '四': '4', '五': '5', 
                      '六': '6', '七': '7', '八': '8', '九': '9', '十': '10',
                      '十一': '11', '十二': '12', '十三': '13', '十四': '14'}
    for match in re.finditer(category_pattern, content):
        chinese_num = match.group(1)
        categories.append({
            'id': chinese_to_num.get(chinese_num, chinese_num),
            'name': match.group(2),
            'count': int(match.group(3))
        })
    
    # 解析各分类词条
    all_terms = []
    category_sections = re.split(r'\n## ', content)
    
    for section in category_sections:
        # 匹配分类标题: "一、体-相-用核心架构" 等
        cat_match = re.match(r'([一二三四五六七八九十]+)、(.+)', section)
        if not cat_match:
            continue
        
        lines = section.split('\n')
        # 提取分类名称（去掉序号前缀）
        cat_name_raw = lines[0].strip()  # 例如: "一、体-相-用核心架构"
        # 去掉中文序号前缀，只保留分类名称
        cat_name = re.sub(r'^[一二三四五六七八九十]+、', '', cat_name_raw)  # 例如: "体-相-用核心架构"
        
        # 找到表格开始
        table_start = None
        for i, line in enumerate(lines):
            if line.startswith('| **'):
                table_start = i
                break
        
        if table_start is None:
            continue
        
        # 解析表格内容
        current_terms = []
        for line in lines[table_start:]:
            if not line.startswith('| **'):
                continue
            
            # 解析表格行
            parts = line.split('|')
            if len(parts) >= 5:
                term_cell = parts[1].strip()
                # 提取词汇名
                term_name_match = re.search(r'\*\*([^*]+)\*\*', term_cell)
                if term_name_match:
                    term_name = term_name_match.group(1)
                    pinyin = parts[2].strip() if len(parts) > 2 else ''
                    category = parts[3].strip() if len(parts) > 3 else ''
                    definition = parts[4].strip() if len(parts) > 4 else ''
                    related = parts[5].strip() if len(parts) > 5 else ''
                    
                    current_terms.append({
                        'name': term_name,
                        'pinyin': pinyin,
                        'category': category,
                        'definition': definition,
                        'related': related,
                        'main_category': cat_name
                    })
        
        all_terms.extend(current_terms)
    
    return {
        'categories': categories,
        'terms': all_terms,
        'version': VERSION,
        'release_date': RELEASE_DATE
    }

def get_css_styles():
    """获取 CSS 样式"""
    return '''<style>
:root { --primary-color: #0066cc; --secondary-color: #00cc99; --accent-color: #ff6600; }
* { margin: 0; padding: 0; box-sizing: border-box; }
html { scroll-behavior: smooth; }
body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif; font-size: 16px; line-height: 1.8; color: #333; background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%); min-height: 100vh; }
header { position: fixed; top: 0; left: 0; right: 0; z-index: 999; background: rgba(255,255,255,0.95); backdrop-filter: blur(10px); box-shadow: 0 2px 20px rgba(0,0,0,0.08); }
.header-content { max-width: 1200px; margin: 0 auto; padding: 15px 20px; display: flex; justify-content: space-between; align-items: center; }
.logo { font-size: 20px; font-weight: bold; background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.search-box { padding: 8px 16px; border: 2px solid #e0e0e0; border-radius: 25px; font-size: 14px; width: 250px; outline: none; }
.search-box:focus { border-color: var(--primary-color); }
.main-container { display: flex; max-width: 1200px; margin: 0 auto; padding: 80px 20px 100px; gap: 30px; }
.sidebar { width: 250px; flex-shrink: 0; position: sticky; top: 100px; }
.sidebar-title { font-size: 16px; font-weight: bold; color: var(--primary-color); margin-bottom: 15px; padding-left: 10px; border-left: 4px solid var(--primary-color); }
.nav-list { list-style: none; background: white; border-radius: 12px; padding: 10px 0; box-shadow: 0 4px 12px rgba(0,102,204,0.1); }
.nav-item { padding: 10px 20px; cursor: pointer; color: #666; font-size: 14px; transition: all 0.2s; }
.nav-item:hover { background: rgba(0,102,204,0.05); }
.nav-item.active { background: rgba(0,102,204,0.1); color: var(--primary-color); font-weight: bold; }
.content { flex: 1; }
.intro-section { background: linear-gradient(135deg, var(--primary-color), #0088dd); color: white; padding: 40px; border-radius: 16px; margin-bottom: 30px; }
.intro-title { font-size: 32px; font-weight: bold; text-align: center; margin-bottom: 20px; }
.intro-subtitle { font-size: 16px; opacity: 0.9; text-align: center; font-style: italic; }
.section { background: white; border-radius: 16px; padding: 30px; margin-bottom: 30px; box-shadow: 0 4px 12px rgba(0,102,204,0.1); }
.section-title { font-size: 22px; font-weight: bold; color: var(--primary-color); margin-bottom: 25px; }
.section-title::before { content: ""; width: 4px; height: 24px; background: linear-gradient(180deg, var(--primary-color), var(--secondary-color)); display: inline-block; margin-right: 10px; }
.term-card { background: linear-gradient(135deg, #fafbfc, #f5f7fa); border-radius: 12px; padding: 20px; margin-bottom: 20px; border-left: 4px solid var(--primary-color); transition: all 0.2s; }
.term-card:hover { transform: translateY(-2px); box-shadow: 0 6px 16px rgba(0,102,204,0.15); }
.term-header { display: flex; align-items: center; gap: 12px; margin-bottom: 12px; }
.term-tag { background: linear-gradient(135deg, var(--primary-color), #0077dd); color: white; padding: 6px 14px; border-radius: 20px; font-weight: bold; font-size: 14px; }
.term-category { font-size: 12px; color: #999; background: #f0f0f0; padding: 4px 10px; border-radius: 10px; }
.term-pinyin { font-size: 13px; color: #666; font-style: italic; margin-left: 8px; }
.term-definition { font-size: 15px; color: #555; line-height: 1.8; }
.related-terms { margin-top: 12px; padding-top: 12px; border-top: 1px dashed #ddd; }
.related-terms strong { color: #7f8c8d; font-size: 0.9em; }
.related-link { color: #3498DB; text-decoration: none; margin-right: 10px; cursor: pointer; transition: color 0.2s; }
.related-link:hover { color: #2980B9; text-decoration: underline; }
.version-module { background: linear-gradient(135deg, #fff9e6, #fff5cc); border-left: 4px solid #ff9900; border-radius: 0 12px 12px 0; padding: 25px; margin-bottom: 30px; }
.version-title { font-size: 18px; font-weight: bold; color: #cc7700; margin-bottom: 20px; }
.version-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; }
.version-item { background: rgba(255,255,255,0.8); padding: 15px; border-radius: 8px; }
.version-label { font-size: 12px; color: #999; margin-bottom: 5px; }
.version-value { font-size: 14px; font-weight: bold; color: #333; }
.back-to-top { position: fixed; bottom: 30px; right: 30px; width: 50px; height: 50px; background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)); color: white; border: none; border-radius: 50%; cursor: pointer; opacity: 0; visibility: hidden; transition: all 0.3s; z-index: 1100; font-size: 18px; }
.back-to-top.show { opacity: 1; visibility: visible; }
.back-to-top:hover { transform: translateY(-3px); box-shadow: 0 6px 20px rgba(0,102,204,0.4); }
.back-to-home { position: fixed; bottom: 30px; right: 90px; width: 50px; height: 50px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 50%; cursor: pointer; opacity: 0; visibility: hidden; transition: all 0.3s; z-index: 1100; font-size: 16px; }
.back-to-home.show { opacity: 1; visibility: visible; }
.back-to-home:hover { transform: translateY(-3px); box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4); }
.feedback-float { position: fixed; bottom: 90px; right: 30px; background: linear-gradient(135deg, #f39c12, #e67e22); color: white; border: none; border-radius: 24px; cursor: pointer; opacity: 0; visibility: hidden; transition: all 0.3s; z-index: 1100; font-size: 15px; padding: 12px 18px; box-shadow: 0 4px 15px rgba(243, 156, 18, 0.4); display: flex; align-items: center; gap: 6px; }
.feedback-float.show { opacity: 1; visibility: visible; }
.feedback-float:hover { transform: translateY(-3px); box-shadow: 0 6px 20px rgba(243, 156, 18, 0.5); }
.feedback-overlay { display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.45); z-index: 3000; align-items: center; justify-content: center; }
.feedback-overlay.active { display: flex; }
.feedback-modal { background: #fff; border-radius: 16px; padding: 32px; max-width: 440px; width: 90%; box-shadow: 0 12px 40px rgba(0,0,0,0.2); position: relative; max-height: 90vh; overflow-y: auto; z-index: 3001; }
.feedback-modal-close { position: absolute; top: 14px; right: 18px; background: none; border: none; font-size: 22px; cursor: pointer; color: #999; line-height: 1; }
.feedback-modal-close:hover { color: #333; }
.feedback-modal h3 { font-size: 1.2em; margin: 0 0 6px; color: #2c3e50; }
.feedback-modal-sub { font-size: 0.85em; color: #888; margin: 0 0 20px; }
.feedback-form-group { margin-bottom: 16px; }
.feedback-form-group label { display: block; font-size: 0.9em; font-weight: 600; color: #555; margin-bottom: 6px; }
.feedback-form-group select, .feedback-form-group textarea, .feedback-form-group input { width: 100%; padding: 10px 14px; border: 1px solid #ddd; border-radius: 8px; font-size: 0.95em; font-family: inherit; outline: none; transition: border-color 0.2s; box-sizing: border-box; }
.feedback-form-group select:focus, .feedback-form-group textarea:focus, .feedback-form-group input:focus { border-color: #f39c12; }
.feedback-form-group textarea { min-height: 120px; resize: vertical; }
.feedback-submit { width: 100%; padding: 12px; background: linear-gradient(135deg, #f39c12, #e67e22); color: #fff; border: none; border-radius: 24px; font-size: 1em; font-weight: 600; cursor: pointer; transition: transform 0.2s, box-shadow 0.2s; }
.feedback-submit:hover { transform: translateY(-2px); box-shadow: 0 4px 16px rgba(243, 156, 18, 0.4); }
.feedback-submit:disabled { opacity: 0.6; cursor: not-allowed; transform: none; }
.feedback-success { display: none; text-align: center; padding: 20px 0; }
.feedback-success.show { display: block; }
.feedback-success-icon { font-size: 3em; margin-bottom: 12px; }
.feedback-success p { color: #555; margin: 4px 0; }
footer { background: #2c3e50; color: white; padding: 30px; text-align: center; margin-top: 50px; }
.footer-text { font-size: 14px; opacity: 0.8; }
.no-results { text-align: center; padding: 40px; color: #999; font-size: 16px; }
@media (max-width: 768px) {
    .header-content { padding: 10px 12px; flex-wrap: wrap; gap: 8px; }
    .logo { font-size: 17px; }
    .search-box { width: 100%; font-size: 13px; padding: 6px 12px; }
    .main-container { flex-direction: column; padding: 96px 12px 120px; gap: 0; }
    .sidebar { width: 100%; position: sticky; top: 92px; z-index: 998; background: rgba(255,255,255,0.95); backdrop-filter: blur(8px); padding: 8px 0; margin: 0 -12px; }
    .sidebar-title { display: none; }
    .nav-list { display: flex; flex-wrap: nowrap; overflow-x: auto; gap: 6px; padding: 0 12px; background: transparent; box-shadow: none; border-radius: 0; -webkit-overflow-scrolling: touch; scrollbar-width: none; }
    .nav-list::-webkit-scrollbar { display: none; }
    .nav-item { flex-shrink: 0; padding: 6px 14px; font-size: 13px; white-space: nowrap; border-radius: 16px; background: #f0f0f0; }
    .nav-item.active { background: var(--primary-color); color: #fff; }
    .content { width: 100%; }
    .intro-section { padding: 24px 20px; }
    .intro-title { font-size: 24px; }
    .intro-subtitle { font-size: 14px; }
    .section { padding: 20px 16px; }
    .section-title { font-size: 18px; }
    .term-card { padding: 16px; }
    .term-tag { font-size: 12px; padding: 4px 10px; }
    .term-definition { font-size: 14px; }
    .back-to-home { right: 65px; width: 45px; height: 45px; font-size: 14px; }
    .back-to-top { right: 15px; width: 45px; height: 45px; font-size: 14px; }
    .feedback-float { right: 15px; bottom: 85px; padding: 10px 14px; font-size: 14px; }
    .version-grid { grid-template-columns: repeat(2, 1fr); }
}
</style>'''

def get_javascript():
    """获取 JavaScript 交互功能"""
    return '''<script>
// 搜索功能
const searchBox = document.getElementById('searchBox');
const termCards = document.querySelectorAll('.term-card');
const sections = document.querySelectorAll('.section, .intro-section, .version-module');

searchBox.addEventListener('input', function() {
    const query = this.value.toLowerCase().trim();
    
    termCards.forEach(card => {
        const term = card.querySelector('.term-tag').textContent.toLowerCase();
        const definition = card.querySelector('.term-definition').textContent.toLowerCase();
        const pinyin = (card.querySelector('.term-pinyin')?.textContent || '').toLowerCase();
        
        if (query === '' || term.includes(query) || definition.includes(query) || pinyin.includes(query)) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
    
    // 如果搜索词为空，显示所有内容
    if (!query) {
        document.querySelectorAll('.section').forEach(section => {
            section.style.display = 'block';
        });
        const introSection = document.querySelector('.intro-section');
        if (introSection) introSection.style.display = 'block';
        const versionModule = document.querySelector('.version-module');
        if (versionModule) versionModule.style.display = 'block';
        return;
    }
    
    // 显示/隐藏 section
    document.querySelectorAll('.section').forEach(section => {
        let hasVisibleCard = false;
        section.querySelectorAll('.term-card').forEach(card => {
            if (card.style.display !== 'none') {
                hasVisibleCard = true;
            }
        });
        if (hasVisibleCard) {
            section.style.display = 'block';
        } else {
            section.style.display = 'none';
        }
    });
    
    // 搜索时隐藏简介和版本模块
    const introSection2 = document.querySelector('.intro-section');
    if (introSection2) introSection2.style.display = 'none';
    const versionModule2 = document.querySelector('.version-module');
    if (versionModule2) versionModule2.style.display = 'none';
});

// 侧边栏导航
const navItems = document.querySelectorAll('.nav-item');
navItems.forEach(item => {
    item.addEventListener('click', function() {
        const sectionId = this.getAttribute('data-section');
        if (sectionId) {
            // 移除所有 active
            navItems.forEach(i => i.classList.remove('active'));
            this.classList.add('active');
            
            // 滚动到对应 section
            const section = document.getElementById(sectionId);
            if (section) {
                section.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        }
    });
});

// 滚动时更新导航状态
window.addEventListener('scroll', function() {
    const scrollPos = window.scrollY + 150;
    
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionBottom = sectionTop + section.offsetHeight;
        
        if (scrollPos >= sectionTop && scrollPos < sectionBottom) {
            const sectionId = section.getAttribute('id');
            navItems.forEach(item => {
                if (item.getAttribute('data-section') === sectionId) {
                    item.classList.add('active');
                } else {
                    item.classList.remove('active');
                }
            });
        }
    });
    
    // 显示返回按钮
    const backToTop = document.querySelector('.back-to-top');
    const backToHome = document.querySelector('.back-to-home');
    const feedbackFloat = document.querySelector('.feedback-float');
    
    if (window.scrollY > 300) {
        backToTop?.classList.add('show');
        backToHome?.classList.add('show');
        feedbackFloat?.classList.add('show');
    } else {
        backToTop?.classList.remove('show');
        backToHome?.classList.remove('show');
        feedbackFloat?.classList.remove('show');
    }
});

// 返回顶部
document.querySelector('.back-to-top')?.addEventListener('click', function() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
});

// 相关词条点击跳转
document.querySelectorAll('.related-link').forEach(link => {
    link.addEventListener('click', function() {
        const termName = this.textContent;
        searchBox.value = termName;
        searchBox.dispatchEvent(new Event('input'));
        
        // 滚动到第一个匹配的卡片
        const cards = document.querySelectorAll('.term-card');
        for (const card of cards) {
            if (card.querySelector('.term-tag').textContent === termName) {
                card.scrollIntoView({ behavior: 'smooth', block: 'center' });
                card.classList.add('highlight');
                setTimeout(() => card.classList.remove('highlight'), 2000);
                break;
            }
        }
    });
});

// 反馈弹窗功能
const feedbackFloat = document.getElementById('feedbackFloat');
const feedbackOverlay = document.getElementById('feedbackOverlay');
const feedbackClose = document.getElementById('feedbackClose');
const feedbackForm = document.getElementById('feedbackForm');
const feedbackSuccess = document.getElementById('feedbackSuccess');
const fbSubmit = document.getElementById('fbSubmit');

function openFeedback() {
    feedbackOverlay.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeFeedback() {
    feedbackOverlay.classList.remove('active');
    document.body.style.overflow = '';
    feedbackForm.style.display = '';
    feedbackSuccess.classList.remove('show');
    document.getElementById('fbContent').value = '';
}

feedbackFloat?.addEventListener('click', openFeedback);
feedbackClose?.addEventListener('click', closeFeedback);
feedbackOverlay?.addEventListener('click', function(e) {
    if (e.target === feedbackOverlay) closeFeedback();
});
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && feedbackOverlay?.classList.contains('active')) closeFeedback();
});

fbSubmit?.addEventListener('click', async function(e) {
    e.preventDefault();
    const content = document.getElementById('fbContent').value.trim();
    if (content.length < 5) {
        alert('反馈内容至少需要5个字符');
        return;
    }
    fbSubmit.disabled = true;
    fbSubmit.textContent = '提交中…';
    try {
        const resp = await fetch('/api/feedback', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                type: document.getElementById('fbType').value,
                source: 'glossary',
                content: content,
                contact: document.getElementById('fbContact').value.trim()
            })
        });
        const data = await resp.json();
        if (data.success) {
            feedbackForm.style.display = 'none';
            feedbackSuccess.classList.add('show');
        } else {
            alert('提交失败：' + (data.error || '请稍后重试'));
        }
    } catch (e) {
        alert('网络错误，请稍后重试。也可通过微信公众号「TS爱心联盟」提交反馈。');
    } finally {
        fbSubmit.disabled = false;
        fbSubmit.textContent = '提交反馈';
    }
});
</script>'''

def generate_html_zh(vocab_data):
    """生成中文 HTML 页面"""
    categories = vocab_data['categories']
    terms = vocab_data['terms']
    
    # 生成侧边栏导航
    nav_items = '<li class="nav-item" data-section="intro">简介</li>\n'
    nav_items += '<li class="nav-item" data-section="version">版本</li>\n'
    for cat in categories:
        section_id = cat['name'].replace('-', '').replace(' ', '').replace('（', '').replace('）', '')
        nav_items += f'<li class="nav-item" data-section="cat-{cat["id"]}">{cat["name"]} ({cat["count"]})</li>\n'
    nav_items += '<li class="nav-item" data-section="quick-index">快速检索</li>'
    
    # 生成各分类词条内容
    sections_html = ''
    category_terms_map = {}
    for term in terms:
        cat_key = term['main_category']
        if cat_key not in category_terms_map:
            category_terms_map[cat_key] = []
        category_terms_map[cat_key].append(term)
    
    cat_index = 1
    for cat in categories:
        cat_name = cat['name']
        terms_in_cat = category_terms_map.get(cat_name, [])
        
        if not terms_in_cat:
            continue
        
        alias_map = {
            '觉知域': '域/觉知',
            '频谱一元论': '域/觉知',
            '无欲': '无欲/有欲',
            '有欲': '无欲/有欲',
            '不善人': '善人/不善人',
            '善人': '善人/不善人',
            '祸': '祸/福',
            '福': '祸/福',
            '阴': '阴阳螺旋',
            '阳': '阴阳螺旋',
        }
        all_term_names = [t['name'] for t in terms]
        for t in all_term_names:
            base_name = re.sub(r'\s*\([^)]+\)', '', t).strip()
            base_name = re.sub(r'\s*（[^）]+）', '', base_name).strip()
            if base_name != t:
                alias_map[base_name] = t
            
            bracket_match = re.search(r'（([^）]+)）', t)
            if bracket_match:
                bracket_content = bracket_match.group(1).strip()
                if bracket_content != t:
                    alias_map[bracket_content] = t
            
            bracket_match_en = re.search(r'\(([^)]+)\)', t)
            if bracket_match_en:
                bracket_content_en = bracket_match_en.group(1).strip()
                if bracket_content_en != t:
                    alias_map[bracket_content_en] = t
            
            slash_match = re.search(r'(.+)/(.+)', t)
            if slash_match:
                slash_part1 = slash_match.group(1).strip()
                slash_part2 = slash_match.group(2).strip()
                if slash_part1 != t:
                    alias_map[slash_part1] = t
                if slash_part2 != t:
                    alias_map[slash_part2] = t
            
            slash_match2 = re.search(r'(.+)/(.+)/(.+)', t)
            if slash_match2:
                alias_map[slash_match2.group(1).strip()] = t
                alias_map[slash_match2.group(2).strip()] = t
                alias_map[slash_match2.group(3).strip()] = t
        
        cards_html = ''
        for term in terms_in_cat:
            related_links = ''
            if term['related']:
                related_terms = [t.strip() for t in term['related'].split('、') if t.strip()]
                for rt in related_terms[:5]:
                    actual_name = alias_map.get(rt, rt)
                    related_links += f'<a class="related-link">{actual_name}</a>'
            
            card_html = f'''
<div class="term-card" data-term="{term['name']}">
<div class="term-header">
<span class="term-tag">{term['name']}</span>
<span class="term-pinyin">{term['pinyin']}</span>
<span class="term-category">{term['category']}</span>
</div>
<p class="term-definition">{term['definition']}</p>
{f'<div class="related-terms"><strong>相关词条：</strong>{related_links}</div>' if related_links else ''}
</div>'''
            cards_html += card_html
        
        sections_html += f'''
<div id="cat-{cat["id"]}" class="section">
<h2 class="section-title">{cat_name}</h2>
{cards_html}
</div>'''
        cat_index += 1
    
    # 生成快速检索表
    quick_index_html = '''
<div id="quick-index" class="section">
<h2 class="section-title">📊 快速检索表</h2>
<div style="overflow-x: auto;">
<table style="width: 100%; border-collapse: collapse; font-size: 14px;">
<thead>
<tr style="background: linear-gradient(135deg, #0066cc, #00cc99); color: white;">
<th style="padding: 12px 8px; text-align: left;">分类</th>
<th style="padding: 12px 8px; text-align: left;">词汇</th>
<th style="padding: 12px 8px; text-align: left;">拼音</th>
<th style="padding: 12px 8px; text-align: left;">一句定义</th>
</tr>
</thead>
<tbody>'''
    
    for cat in categories[:7]:  # 显示前7个分类的快速检索
        cat_name = cat['name']
        terms_in_cat = category_terms_map.get(cat_name, [])
        for term in terms_in_cat[:4]:  # 每个分类最多4个
            # 提取简短定义（取第一句）
            short_def = term['definition'].split('。')[0][:50] + '...' if len(term['definition']) > 50 else term['definition'].split('。')[0]
            quick_index_html += f'''
<tr style="border-bottom: 1px solid #eee;">
<td style="padding: 10px 8px; color: #666;">{cat_name}</td>
<td style="padding: 10px 8px;"><strong>{term['name']}</strong></td>
<td style="padding: 10px 8px; color: #999; font-style: italic;">{term['pinyin']}</td>
<td style="padding: 10px 8px; color: #555;">{short_def}</td>
</tr>'''
    
    quick_index_html += '''
</tbody>
</table>
</div>
</div>'''
    
    # 组装完整 HTML
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>旋量-太极词汇表 V{VERSION}</title>
{get_css_styles()}
</head>
<body>
<header>
<div class="header-content">
<div class="logo">旋量-太极词汇表</div>
<input type="text" id="searchBox" class="search-box" placeholder="搜索词汇、拼音或定义...">
</div>
</header>

<div class="main-container">
<div class="sidebar">
<div class="sidebar-title">目录导航</div>
<ul class="nav-list">
{nav_items}
</ul>
</div>

<div class="content">
<div id="intro" class="intro-section">
<h1 class="intro-title">旋量-太极词汇表</h1>
<p class="intro-subtitle">以下定义，是在"万物皆振动"与"旋量-太极"模型的交叉读解中重新锚定的。<br>名可名，非常名——这些定义不是最终的真理，是可操作的比喻脚手架。</p>
</div>

<div id="version" class="version-module">
<div class="version-title">📋 版本管理信息</div>
<div class="version-grid">
<div class="version-item"><div class="version-label">版本号</div><div class="version-value">v{VERSION}</div></div>
<div class="version-item"><div class="version-label">发布日期</div><div class="version-value">{RELEASE_DATE}</div></div>
<div class="version-item"><div class="version-label">词条总数</div><div class="version-value">{len(terms)}个</div></div>
<div class="version-item"><div class="version-label">分类结构</div><div class="version-value">{len(categories)}个分类</div></div>
</div>
</div>

{sections_html}
{quick_index_html}
</div>
</div>

<button class="back-to-top" title="返回顶部">↑</button>
<button class="back-to-home" title="返回首页" onclick="window.location.href='spinor-taiji-model-statement.html'">🏠</button>
<button class="feedback-float" id="feedbackFloat" title="反馈建议">📝 反馈建议</button>

<div class="feedback-overlay" id="feedbackOverlay">
    <div class="feedback-modal">
        <button class="feedback-modal-close" id="feedbackClose">&times;</button>
        <h3>📬 反馈与建议</h3>
        <p class="feedback-modal-sub">这份文档因你的反馈而不断进化</p>
        <div id="feedbackForm">
            <div class="feedback-form-group">
                <label for="fbType">反馈类型</label>
                <select id="fbType">
                    <option value="suggestion">改进建议</option>
                    <option value="correction">内容纠错</option>
                    <option value="question">疑问求助</option>
                    <option value="appreciation">赞赏鼓励</option>
                </select>
            </div>
            <div class="feedback-form-group">
                <label for="fbContent">具体内容 <span style="color:#e74c3c">*</span></label>
                <textarea id="fbContent" placeholder="请描述你的反馈内容…" required></textarea>
            </div>
            <div class="feedback-form-group">
                <label for="fbContact">联系方式（选填）</label>
                <input type="text" id="fbContact" placeholder="邮箱或微信，便于后续沟通">
            </div>
            <button class="feedback-submit" id="fbSubmit">提交反馈</button>
        </div>
        <div class="feedback-success" id="feedbackSuccess">
            <div class="feedback-success-icon">🎉</div>
            <p><strong>感谢你的反馈！</strong></p>
            <p style="font-size:0.85em">我们会尽快处理，如有需要会通过你留下的联系方式回复。</p>
        </div>
    </div>
</div>

<footer>
<p class="footer-text">旋量-太极词汇表 V{VERSION} | {RELEASE_DATE}</p>
</footer>

{get_javascript()}
</body>
</html>'''
    
    return html

def generate_html_en(vocab_data):
    """生成英文 HTML 页面（简化版，主要词条翻译）"""
    categories = vocab_data['categories']
    terms = vocab_data['terms']
    
    # 简化翻译映射
    cat_translations = {
        '体-相-用核心架构': 'Ti-Xiang-Yong Core Architecture',
        '相的两大法则': 'Two Laws of Xiang',
        '频谱频段': 'Spectrum Bands',
        '底层操作': 'Fundamental Operations',
        '觉知与信息': 'Awareness & Information',
        '时间': 'Time',
        '存在主体': 'Being & Subject',
        '生命状态': 'Life States',
        '关系': 'Relationships',
        '心灵操作': 'Mental Operations',
        '弱者道之用的四重展开': 'Fourfold Manifestation',
        '经典读解关联': 'Classic Interpretations',
        '实践指南关联': 'Practice Guide',
        '三层标签系统': 'Three-Layer Label System'
    }
    
    # 生成侧边栏导航
    nav_items = '<li class="nav-item" data-section="intro">Intro</li>\n'
    nav_items += '<li class="nav-item" data-section="version">Version</li>\n'
    for cat in categories:
        nav_items += f'<li class="nav-item" data-section="cat-{cat["id"]}">{cat_translations.get(cat["name"], cat["name"])} ({cat["count"]})</li>\n'
    nav_items += '<li class="nav-item" data-section="quick-index">Quick Index</li>'
    
    # 生成各分类词条内容
    sections_html = ''
    category_terms_map = {}
    for term in terms:
        cat_key = term['main_category']
        if cat_key not in category_terms_map:
            category_terms_map[cat_key] = []
        category_terms_map[cat_key].append(term)
    
    cat_index = 1
    for cat in categories:
        cat_name = cat['name']
        terms_in_cat = category_terms_map.get(cat_name, [])
        
        if not terms_in_cat:
            continue
        
        alias_map = {
            '觉知域': '域/觉知',
            '频谱一元论': '域/觉知',
            '无欲': '无欲/有欲',
            '有欲': '无欲/有欲',
            '不善人': '善人/不善人',
            '善人': '善人/不善人',
            '祸': '祸/福',
            '福': '祸/福',
            '阴': '阴阳螺旋',
            '阳': '阴阳螺旋',
        }
        all_term_names = [t['name'] for t in terms]
        for t in all_term_names:
            base_name = re.sub(r'\s*\([^)]+\)', '', t).strip()
            base_name = re.sub(r'\s*（[^）]+）', '', base_name).strip()
            if base_name != t:
                alias_map[base_name] = t
            
            bracket_match = re.search(r'（([^）]+)）', t)
            if bracket_match:
                bracket_content = bracket_match.group(1).strip()
                if bracket_content != t:
                    alias_map[bracket_content] = t
            
            bracket_match_en = re.search(r'\(([^)]+)\)', t)
            if bracket_match_en:
                bracket_content_en = bracket_match_en.group(1).strip()
                if bracket_content_en != t:
                    alias_map[bracket_content_en] = t
            
            slash_match = re.search(r'(.+)/(.+)', t)
            if slash_match:
                slash_part1 = slash_match.group(1).strip()
                slash_part2 = slash_match.group(2).strip()
                if slash_part1 != t:
                    alias_map[slash_part1] = t
                if slash_part2 != t:
                    alias_map[slash_part2] = t
            
            slash_match2 = re.search(r'(.+)/(.+)/(.+)', t)
            if slash_match2:
                alias_map[slash_match2.group(1).strip()] = t
                alias_map[slash_match2.group(2).strip()] = t
                alias_map[slash_match2.group(3).strip()] = t
        
        cards_html = ''
        for term in terms_in_cat:
            related_links = ''
            if term['related']:
                related_terms = [t.strip() for t in term['related'].split('、') if t.strip()]
                for rt in related_terms[:5]:
                    actual_name = alias_map.get(rt, rt)
                    related_links += f'<a class="related-link">{actual_name}</a>'
            
            card_html = f'''
<div class="term-card" data-term="{term['name']}">
<div class="term-header">
<span class="term-tag">{term['name']}</span>
<span class="term-pinyin">{term['pinyin']}</span>
<span class="term-category">{term['category']}</span>
</div>
<p class="term-definition">{term['definition']}</p>
{f'<div class="related-terms"><strong>Related:</strong>{related_links}</div>' if related_links else ''}
</div>'''
            cards_html += card_html
        
        sections_html += f'''
<div id="cat-{cat["id"]}" class="section">
<h2 class="section-title">{cat_translations.get(cat_name, cat_name)}</h2>
{cards_html}
</div>'''
        cat_index += 1
    
    # 组装完整 HTML
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Spinor-Taiji Glossary V{VERSION}</title>
{get_css_styles()}
</head>
<body>
<header>
<div class="header-content">
<div class="logo">Spinor-Taiji Glossary</div>
<input type="text" id="searchBox" class="search-box" placeholder="Search terms, pinyin or definition...">
</div>
</header>

<div class="main-container">
<div class="sidebar">
<div class="sidebar-title">Navigation</div>
<ul class="nav-list">
{nav_items}
</ul>
</div>

<div class="content">
<div id="intro" class="intro-section">
<h1 class="intro-title">Spinor-Taiji Glossary</h1>
<p class="intro-subtitle">The following definitions have been re-anchored through cross-interpretation of<br>"Everything is Vibration" and the "Spinor-Taiji" model.</p>
</div>

<div id="version" class="version-module">
<div class="version-title">Version Information</div>
<div class="version-grid">
<div class="version-item"><div class="version-label">Version</div><div class="version-value">v{VERSION}</div></div>
<div class="version-item"><div class="version-label">Release Date</div><div class="version-value">{RELEASE_DATE_EN}</div></div>
<div class="version-item"><div class="version-label">Total Terms</div><div class="version-value">{len(terms)}</div></div>
<div class="version-item"><div class="version-label">Categories</div><div class="version-value">{len(categories)}</div></div>
</div>
</div>

{sections_html}
</div>
</div>

<button class="back-to-top" title="Back to Top">↑</button>
<button class="back-to-home" title="Home" onclick="window.location.href='spinor-taiji-model-declaration.html'">🏠</button>
<button class="feedback-float" onclick="window.location.href='https://github.com/huihuihuang/spinor-taiji-model/issues'">📝 Feedback</button>

<footer>
<p class="footer-text">Spinor-Taiji Glossary V{VERSION} | {RELEASE_DATE_EN}</p>
</footer>

{get_javascript()}
</body>
</html>'''
    
    return html

def main():
    """主函数"""
    print("=" * 60)
    print("旋量-太极词汇表转换工具")
    print("=" * 60)
    
    # 检查输入文件
    if not os.path.exists(VOCAB_MD_PATH):
        print(f"错误: 找不到词汇表文件: {VOCAB_MD_PATH}")
        return
    
    print(f"输入文件: {VOCAB_MD_PATH}")
    
    # 解析 Markdown
    print("\n[1] 解析 Markdown 词汇表...")
    vocab_data = parse_markdown_vocab(VOCAB_MD_PATH)
    print(f"    - 分类数: {len(vocab_data['categories'])}")
    print(f"    - 词条数: {len(vocab_data['terms'])}")
    
    # 生成中文 HTML
    print("\n[2] 生成中文 HTML 页面...")
    html_zh = generate_html_zh(vocab_data)
    with open(OUTPUT_ZH_PATH, 'w', encoding='utf-8') as f:
        f.write(html_zh)
    print(f"    输出: {OUTPUT_ZH_PATH}")
    
    # 生成英文 HTML
    print("\n[3] 生成英文 HTML 页面...")
    html_en = generate_html_en(vocab_data)
    with open(OUTPUT_EN_PATH, 'w', encoding='utf-8') as f:
        f.write(html_en)
    print(f"    输出: {OUTPUT_EN_PATH}")
    
    print("\n" + "=" * 60)
    print("转换完成!")
    print("=" * 60)

if __name__ == '__main__':
    main()