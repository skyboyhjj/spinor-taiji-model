import os

def generate_enhanced_vocab():
    output_path = 'docs/10-词汇表/旋量太极词汇表_增强版.html'
    
    html_parts = []
    
    # HTML Header
    html_parts.append('<!DOCTYPE html>')
    html_parts.append('<html lang="zh-CN">')
    html_parts.append('<head>')
    html_parts.append('<meta charset="UTF-8">')
    html_parts.append('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
    html_parts.append('<title>旋量-太极词汇表</title>')
    
    # CSS Styles
    html_parts.append('<style>')
    html_parts.append(':root { --primary-color: #0066cc; --secondary-color: #00cc99; --accent-color: #ff6600; }')
    html_parts.append('* { margin: 0; padding: 0; box-sizing: border-box; }')
    html_parts.append('html { scroll-behavior: smooth; }')
    html_parts.append('body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif; font-size: 16px; line-height: 1.8; color: #333; background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%); min-height: 100vh; }')
    html_parts.append('header { position: fixed; top: 0; left: 0; right: 0; z-index: 1000; background: rgba(255,255,255,0.95); backdrop-filter: blur(10px); box-shadow: 0 2px 20px rgba(0,0,0,0.08); }')
    html_parts.append('.header-content { max-width: 1200px; margin: 0 auto; padding: 15px 20px; display: flex; justify-content: space-between; align-items: center; }')
    html_parts.append('.logo { font-size: 20px; font-weight: bold; background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }')
    html_parts.append('.search-box { padding: 8px 16px; border: 2px solid #e0e0e0; border-radius: 25px; font-size: 14px; width: 250px; outline: none; }')
    html_parts.append('.search-box:focus { border-color: var(--primary-color); }')
    html_parts.append('.main-container { display: flex; max-width: 1200px; margin: 0 auto; padding: 80px 20px 100px; gap: 30px; }')
    html_parts.append('.sidebar { width: 250px; flex-shrink: 0; position: sticky; top: 100px; }')
    html_parts.append('.sidebar-title { font-size: 16px; font-weight: bold; color: var(--primary-color); margin-bottom: 15px; padding-left: 10px; border-left: 4px solid var(--primary-color); }')
    html_parts.append('.nav-list { list-style: none; background: white; border-radius: 12px; padding: 10px 0; box-shadow: 0 4px 12px rgba(0,102,204,0.1); }')
    html_parts.append('.nav-item { padding: 10px 20px; cursor: pointer; transition: all 0.3s; color: #666; font-size: 14px; }')
    html_parts.append('.nav-item:hover { background: rgba(0,102,204,0.05); color: var(--primary-color); padding-left: 25px; }')
    html_parts.append('.nav-item.active { background: rgba(0,102,204,0.1); color: var(--primary-color); font-weight: bold; }')
    html_parts.append('.content { flex: 1; }')
    html_parts.append('.intro-section { background: linear-gradient(135deg, var(--primary-color), #0088dd); color: white; padding: 40px; border-radius: 16px; margin-bottom: 30px; }')
    html_parts.append('.intro-title { font-size: 32px; font-weight: bold; text-align: center; margin-bottom: 20px; }')
    html_parts.append('.intro-subtitle { font-size: 16px; opacity: 0.9; text-align: center; font-style: italic; }')
    html_parts.append('.section { background: white; border-radius: 16px; padding: 30px; margin-bottom: 30px; box-shadow: 0 4px 12px rgba(0,102,204,0.1); }')
    html_parts.append('.section-title { font-size: 22px; font-weight: bold; color: var(--primary-color); margin-bottom: 25px; }')
    html_parts.append('.section-title::before { content: ""; width: 4px; height: 24px; background: linear-gradient(180deg, var(--primary-color), var(--secondary-color)); display: inline-block; margin-right: 10px; }')
    html_parts.append('.term-card { background: linear-gradient(135deg, #fafbfc, #f5f7fa); border-radius: 12px; padding: 20px; margin-bottom: 20px; border-left: 4px solid var(--primary-color); }')
    html_parts.append('.term-card:hover { transform: translateY(-3px); box-shadow: 0 8px 24px rgba(0,102,204,0.2); }')
    html_parts.append('.term-header { display: flex; align-items: center; gap: 12px; margin-bottom: 12px; }')
    html_parts.append('.term-tag { background: linear-gradient(135deg, var(--primary-color), #0077dd); color: white; padding: 6px 14px; border-radius: 20px; font-weight: bold; font-size: 14px; }')
    html_parts.append('.term-category { font-size: 12px; color: #999; background: #f0f0f0; padding: 4px 10px; border-radius: 10px; }')
    html_parts.append('.term-definition { font-size: 15px; color: #555; line-height: 1.8; text-indent: 2em; }')
    html_parts.append('.version-module { background: linear-gradient(135deg, #fff9e6, #fff5cc); border-left: 4px solid #ff9900; border-radius: 0 12px 12px 0; padding: 25px; margin-bottom: 30px; }')
    html_parts.append('.version-title { font-size: 18px; font-weight: bold; color: #cc7700; margin-bottom: 20px; }')
    html_parts.append('.version-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; }')
    html_parts.append('.version-item { background: rgba(255,255,255,0.8); padding: 15px; border-radius: 8px; }')
    html_parts.append('.version-label { font-size: 12px; color: #999; margin-bottom: 5px; }')
    html_parts.append('.version-value { font-size: 14px; font-weight: bold; color: #333; }')
    html_parts.append('.change-log { margin-top: 20px; border-top: 1px dashed #ffcc66; padding-top: 20px; }')
    html_parts.append('.change-item { display: flex; gap: 10px; padding: 10px 0; border-bottom: 1px solid #ffeedd; }')
    html_parts.append('.change-type { font-size: 12px; padding: 3px 8px; border-radius: 15px; font-weight: bold; }')
    html_parts.append('.change-type.add { background: #e6f7ff; color: #1890ff; }')
    html_parts.append('.change-type.modify { background: #fff7e6; color: #fa8c16; }')
    html_parts.append('.relation-graph { background: white; border-radius: 16px; padding: 30px; margin-bottom: 30px; }')
    html_parts.append('.graph-title { font-size: 22px; font-weight: bold; color: var(--primary-color); margin-bottom: 25px; }')
    html_parts.append('.graph-container { overflow-x: auto; }')
    html_parts.append('.legend { display: flex; flex-wrap: wrap; gap: 20px; margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee; }')
    html_parts.append('.legend-item { display: flex; align-items: center; gap: 8px; }')
    html_parts.append('.legend-color { width: 16px; height: 16px; border-radius: 4px; }')
    html_parts.append('.legend-text { font-size: 13px; color: #666; }')
    html_parts.append('.back-to-top { position: fixed; bottom: 30px; right: 30px; width: 50px; height: 50px; background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)); color: white; border: none; border-radius: 50%; cursor: pointer; opacity: 0; visibility: hidden; transition: all 0.3s; z-index: 1000; }')
    html_parts.append('.back-to-top.show { opacity: 1; visibility: visible; }')
    html_parts.append('footer { background: #2c3e50; color: white; padding: 30px; text-align: center; margin-top: 50px; }')
    html_parts.append('.footer-text { font-size: 14px; opacity: 0.8; }')
    html_parts.append('</style>')
    html_parts.append('</head>')
    html_parts.append('<body>')
    
    # Header
    html_parts.append('<header><div class="header-content"><div class="logo">旋量-太极词汇表</div><input type="text" class="search-box" id="searchInput" placeholder="搜索术语..."></div></header>')
    
    # Main Container
    html_parts.append('<div class="main-container">')
    
    # Sidebar
    html_parts.append('<aside class="sidebar"><div class="sidebar-title">目录导航</div><ul class="nav-list">')
    nav_items = ['引言', '版本', '图形', '基础', '时间', '存在', '生命', '关系', '心灵', '经典', '快速']
    sections = ['intro', 'version', 'graph', 'basic', 'time', 'existence', 'life', 'relation', 'mind', 'classic', 'quick']
    for i, item in enumerate(nav_items):
        active = 'active' if i == 0 else ''
        html_parts.append(f'<li class="nav-item {active}" data-section="{sections[i]}">{item}</li>')
    html_parts.append('</ul></aside>')
    
    # Content
    html_parts.append('<main class="content">')
    
    # Intro
    html_parts.append('<div id="intro" class="intro-section"><h1 class="intro-title">旋量-太极词汇表</h1><p class="intro-subtitle">以下定义，是在"万物皆振动"与"旋量-太极"模型的交叉读解中重新锚定的。<br>名可名，非常名——这些定义不是最终的真理，是可操作的比喻脚手架。</p></div>')
    
    # Version Module
    html_parts.append('<div id="version" class="version-module">')
    html_parts.append('<div class="version-title">📋 版本管理信息</div>')
    html_parts.append('<div class="version-grid">')
    html_parts.append('<div class="version-item"><div class="version-label">版本号</div><div class="version-value">v2.1.0</div></div>')
    html_parts.append('<div class="version-item"><div class="version-label">发布日期</div><div class="version-value">2026年6月22日</div></div>')
    html_parts.append('<div class="version-item"><div class="version-label">变更责任人</div><div class="version-value">旋量太极团队</div></div>')
    html_parts.append('<div class="version-item"><div class="version-label">影响范围</div><div class="version-value">全部词汇条目</div></div>')
    html_parts.append('</div>')
    html_parts.append('<div class="change-log"><div style="font-size:15px;font-weight:bold;color:#cc7700;margin-bottom:15px;">📝 变更记录</div>')
    html_parts.append('<div class="change-item"><span class="change-type add">新增</span><span>添加词汇关系图，展示词汇层级与关联关系</span></div>')
    html_parts.append('<div class="change-item"><span class="change-type add">新增</span><span>添加版本管理模块，包含完整变更记录</span></div>')
    html_parts.append('<div class="change-item"><span class="change-type modify">修改</span><span>优化搜索功能，支持术语和定义双重匹配</span></div>')
    html_parts.append('<div class="change-item"><span class="change-type modify">修改</span><span>优化响应式布局，适配移动端设备</span></div>')
    html_parts.append('</div></div>')
    
    # Relation Graph
    html_parts.append('<div id="graph" class="relation-graph">')
    html_parts.append('<div class="graph-title">🔗 词汇关系图</div>')
    html_parts.append('<div class="graph-container">')
    html_parts.append('<svg width="800" height="500" viewBox="0 0 800 500">')
    html_parts.append('<defs><linearGradient id="mainGrad" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:#0066cc"/><stop offset="100%" style="stop-color:#00cc99"/></linearGradient></defs>')
    html_parts.append('<circle cx="400" cy="50" r="40" fill="url(#mainGrad)"/><text x="400" y="48" text-anchor="middle" fill="white" font-weight="bold" font-size="14">域/觉知</text>')
    html_parts.append('<circle cx="400" cy="140" r="30" fill="#1890ff"/><text x="400" y="138" text-anchor="middle" fill="white" font-size="12" font-weight="bold">旋量</text>')
    html_parts.append('<circle cx="280" cy="230" r="25" fill="#1890ff"/><text x="280" y="228" text-anchor="middle" fill="white" font-size="11" font-weight="bold">平方</text>')
    html_parts.append('<circle cx="520" cy="230" r="25" fill="#1890ff"/><text x="520" y="228" text-anchor="middle" fill="white" font-size="11" font-weight="bold">开方</text>')
    html_parts.append('<circle cx="200" cy="320" r="22" fill="#666"/><text x="200" y="318" text-anchor="middle" fill="white" font-size="10" font-weight="bold">矢量</text>')
    html_parts.append('<circle cx="600" cy="320" r="22" fill="#666"/><text x="600" y="318" text-anchor="middle" fill="white" font-size="10" font-weight="bold">时间</text>')
    html_parts.append('<circle cx="120" cy="410" r="20" fill="#52c41a"/><text x="120" y="408" text-anchor="middle" fill="white" font-size="9" font-weight="bold">生命状态</text>')
    html_parts.append('<circle cx="300" cy="410" r="20" fill="#fa8c16"/><text x="300" y="408" text-anchor="middle" fill="white" font-size="9" font-weight="bold">关系</text>')
    html_parts.append('<circle cx="500" cy="410" r="20" fill="#722ed1"/><text x="500" y="408" text-anchor="middle" fill="white" font-size="9" font-weight="bold">心灵操作</text>')
    html_parts.append('<circle cx="680" cy="410" r="20" fill="#13c2c2"/><text x="680" y="408" text-anchor="middle" fill="white" font-size="9" font-weight="bold">经典读解</text>')
    html_parts.append('<line x1="400" y1="90" x2="400" y2="110" stroke="#0066cc" stroke-width="3"/>')
    html_parts.append('<line x1="400" y1="170" x2="280" y2="205" stroke="#1890ff" stroke-width="2"/>')
    html_parts.append('<line x1="400" y1="170" x2="520" y2="205" stroke="#1890ff" stroke-width="2"/>')
    html_parts.append('<line x1="280" y1="255" x2="200" y2="298" stroke="#666" stroke-width="2"/>')
    html_parts.append('<line x1="520" y1="255" x2="600" y2="298" stroke="#666" stroke-width="2"/>')
    html_parts.append('<line x1="200" y1="342" x2="120" y2="390" stroke="#52c41a" stroke-width="2"/>')
    html_parts.append('<line x1="200" y1="342" x2="300" y2="390" stroke="#fa8c16" stroke-width="2"/>')
    html_parts.append('<line x1="600" y1="342" x2="500" y2="390" stroke="#722ed1" stroke-width="2"/>')
    html_parts.append('<line x1="600" y1="342" x2="680" y2="390" stroke="#13c2c2" stroke-width="2"/>')
    html_parts.append('</svg></div>')
    html_parts.append('<div class="legend">')
    html_parts.append('<div class="legend-item"><div class="legend-color" style="background:linear-gradient(135deg,#0066cc,#00cc99)"></div><span class="legend-text">本源概念</span></div>')
    html_parts.append('<div class="legend-item"><div class="legend-color" style="background:#1890ff"></div><span class="legend-text">基础操作</span></div>')
    html_parts.append('<div class="legend-item"><div class="legend-color" style="background:#666"></div><span class="legend-text">核心概念</span></div>')
    html_parts.append('<div class="legend-item"><div class="legend-color" style="background:#52c41a"></div><span class="legend-text">生命状态</span></div>')
    html_parts.append('<div class="legend-item"><div class="legend-color" style="background:#fa8c16"></div><span class="legend-text">关系</span></div>')
    html_parts.append('<div class="legend-item"><div class="legend-color" style="background:#722ed1"></div><span class="legend-text">心灵操作</span></div>')
    html_parts.append('<div class="legend-item"><div class="legend-color" style="background:#13c2c2"></div><span class="legend-text">经典读解</span></div>')
    html_parts.append('</div></div>')
    
    # Basic Section
    html_parts.append('<div id="basic" class="section"><h2 class="section-title">⚛️ 基础操作</h2>')
    html_parts.append('<div class="term-card" data-term="旋量"><div class="term-header"><span class="term-tag">旋量</span><span class="term-category">基础概念</span></div><p class="term-definition">需要720°才复原的振动种子。宇宙底层最小单位的旋转——旋转360°后不复原，反而"反号"（从显翻为隐，从阳翻为阴）。它同时携带正负两个解。看不见，但一切可见皆由此平方而来。</p></div>')
    html_parts.append('<div class="term-card" data-term="矢量"><div class="term-header"><span class="term-tag">矢量</span><span class="term-category">基础概念</span></div><p class="term-definition">旋量被平方后的可观测产物。物质、身体、念头、标签——所有"确定的东西"都是矢量。它不是假的，但它不是底层的。</p></div>')
    html_parts.append('<div class="term-card" data-term="平方"><div class="term-header"><span class="term-tag">平方（操作）</span><span class="term-category">操作</span></div><p class="term-definition">从旋量到矢量——从潜能凝结为体验。在人体上对应<strong>吸气</strong>。</p></div>')
    html_parts.append('<div class="term-card" data-term="开方"><div class="term-header"><span class="term-tag">开方（操作）</span><span class="term-category">操作</span></div><p class="term-definition">从矢量回到旋量——从体验消解回潜能。在人体上对应<strong>呼气</strong>。</p></div>')
    html_parts.append('</div>')
    
    # Time Section
    html_parts.append('<div id="time" class="section"><h2 class="section-title">⏳ 时间</h2>')
    html_parts.append('<div class="term-card" data-term="时间"><div class="term-header"><span class="term-tag">时间</span><span class="term-category">时间概念</span></div><p class="term-definition">旋量场连续平方和开方的节律。不是一条河，是一个脉冲序列——每一次平方生成"此刻"，每一次开方完成"此刻"的消解。</p></div>')
    html_parts.append('<div class="term-card" data-term="当下"><div class="term-header"><span class="term-tag">当下</span><span class="term-category">时间概念</span></div><p class="term-definition">旋量正在平方的那一瞬间——从潜能凝结为体验的、正在发生的事件。</p></div>')
    html_parts.append('</div>')
    
    # Existence Section
    html_parts.append('<div id="existence" class="section"><h2 class="section-title">👤 存在主体</h2>')
    html_parts.append('<div class="term-card" data-term="我"><div class="term-header"><span class="term-tag">我</span><span class="term-category">主体概念</span></div><p class="term-definition">一束长期被误认为矢量的高阶旋量。从小被教育"我是一个人"，但实际上"我"是一个正在持续"平方→开方→平方"的动态过程。</p></div>')
    html_parts.append('<div class="term-card" data-term="呼吸"><div class="term-header"><span class="term-tag">呼吸</span><span class="term-category">主体概念</span></div><p class="term-definition">平方与开方在人体上的直接体现。吸气 = 平方，呼气 = 开方。</p></div>')
    html_parts.append('</div>')
    
    # Life Section
    html_parts.append('<div id="life" class="section"><h2 class="section-title">💫 生命状态</h2>')
    html_parts.append('<div class="term-card" data-term="含德之厚"><div class="term-header"><span class="term-tag">含德之厚</span><span class="term-category">生命状态</span></div><p class="term-definition">吸呼自然交替——平方有平方的饱满，开方有开方的安心。旋量720°平滑旋转，没有一个相位被抗拒。</p></div>')
    html_parts.append('<div class="term-card" data-term="无死地"><div class="term-header"><span class="term-tag">无死地</span><span class="term-category">生命状态</span></div><p class="term-definition">没有一个可以被攻击的"我"。不是防御力强，是根本没有一个需要防御的独立个体。</p></div>')
    html_parts.append('</div>')
    
    # Relation Section
    html_parts.append('<div id="relation" class="section"><h2 class="section-title">❤️ 关系</h2>')
    html_parts.append('<div class="term-card" data-term="爱"><div class="term-header"><span class="term-tag">爱</span><span class="term-category">关系概念</span></div><p class="term-definition">两个独立的旋量场在同一个域中达到相位锁定。不是一方输出多于另一方，是双方周期对齐了。</p></div>')
    html_parts.append('<div class="term-card" data-term="善"><div class="term-header"><span class="term-tag">善</span><span class="term-category">关系概念</span></div><p class="term-definition">从旋量源头直接平方出来的完美矢量行为——不留下执着的"平方痕迹"。</p></div>')
    html_parts.append('</div>')
    
    # Mind Section
    html_parts.append('<div id="mind" class="section"><h2 class="section-title">🧠 心灵操作</h2>')
    html_parts.append('<div class="term-card" data-term="修行"><div class="term-header"><span class="term-tag">修行</span><span class="term-category">心灵操作</span></div><p class="term-definition">对修行本身的开方。最高一层的修行，不是追求某个特殊状态——是认出你本来就属于那个东西。</p></div>')
    html_parts.append('<div class="term-card" data-term="反者道之动"><div class="term-header"><span class="term-tag">反者道之动</span><span class="term-category">心灵操作</span></div><p class="term-definition">旋量的720°旋转法则——宇宙底层是永不停息的旋转，需要720度才能复原。</p></div>')
    html_parts.append('</div>')
    
    # Classic Section
    html_parts.append('<div id="classic" class="section"><h2 class="section-title">📜 经典读解</h2>')
    html_parts.append('<div class="term-card" data-term="道生一"><div class="term-header"><span class="term-tag">道生一（第42章）</span><span class="term-category">经典解读</span></div><p class="term-definition">完整的生成论链——道（域/觉知）→ 一（第一个旋量）→ 二（正负双解）→ 三（第一次平方操作）→ 万物。</p></div>')
    html_parts.append('</div>')
    
    # Quick Table
    html_parts.append('<div id="quick" class="section"><h2 class="section-title">📊 快速检索表</h2>')
    html_parts.append('<table style="width:100%;border-collapse:collapse;"><thead><tr><th style="background:#0066cc;color:white;padding:12px;text-align:left;">词汇</th><th style="background:#0066cc;color:white;padding:12px;text-align:left;">一句定义</th></tr></thead><tbody>')
    html_parts.append('<tr><td><strong>旋量</strong></td><td>需720°复原的振动种子</td></tr>')
    html_parts.append('<tr><td><strong>矢量</strong></td><td>旋量被平方后的可观测产物</td></tr>')
    html_parts.append('<tr><td><strong>平方（吸）</strong></td><td>从潜能到体验的生成操作</td></tr>')
    html_parts.append('<tr><td><strong>开方（呼）</strong></td><td>从体验到潜能的回归操作</td></tr>')
    html_parts.append('</tbody></table></div>')
    
    html_parts.append('</main></div>')
    
    # Back to top button
    html_parts.append('<button class="back-to-top" id="backToTop">↑</button>')
    
    # Footer
    html_parts.append('<footer><p class="footer-text">— 旋量-太极模型 · 名可名，非常名 —</p></footer>')
    
    # JavaScript
    html_parts.append('<script>')
    html_parts.append('const searchInput = document.getElementById("searchInput");')
    html_parts.append('const termCards = document.querySelectorAll(".term-card");')
    html_parts.append('searchInput.addEventListener("input", function() {')
    html_parts.append('  const searchTerm = this.value.toLowerCase().trim();')
    html_parts.append('  termCards.forEach(card => {')
    html_parts.append('    const term = card.getAttribute("data-term").toLowerCase();')
    html_parts.append('    const def = card.querySelector(".term-definition").textContent.toLowerCase();')
    html_parts.append('    card.style.display = (term.includes(searchTerm) || def.includes(searchTerm)) ? "block" : "none";')
    html_parts.append('  });')
    html_parts.append('});')
    html_parts.append('const navItems = document.querySelectorAll(".nav-item");')
    html_parts.append('navItems.forEach(item => {')
    html_parts.append('  item.addEventListener("click", function() {')
    html_parts.append('    navItems.forEach(n => n.classList.remove("active"));')
    html_parts.append('    this.classList.add("active");')
    html_parts.append('    document.getElementById(this.getAttribute("data-section")).scrollIntoView({ behavior: "smooth" });')
    html_parts.append('  });')
    html_parts.append('});')
    html_parts.append('const backToTopBtn = document.getElementById("backToTop");')
    html_parts.append('window.addEventListener("scroll", function() {')
    html_parts.append('  backToTopBtn.classList.toggle("show", window.scrollY > 300);')
    html_parts.append('});')
    html_parts.append('backToTopBtn.addEventListener("click", () => window.scrollTo({ top: 0, behavior: "smooth" }));')
    html_parts.append('</script>')
    
    html_parts.append('</body></html>')
    
    html = '\n'.join(html_parts)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f'增强版词汇表已生成: {output_path}')

if __name__ == '__main__':
    generate_enhanced_vocab()