
import re

with open("docs/10-词汇表/旋量太极词汇表_增强版.html", "r", encoding="utf-8") as f:
    content = f.read()

new_svg = '''
<div id="graph" class="relation-graph">
<div class="graph-title">🔗 词汇关系图</div>
<div class="graph-container">
<svg width="800" height="500" viewBox="0 0 800 500">
<defs>
<linearGradient id="mainGrad" x1="0%" y1="0%" x2="100%" y2="100%">
<stop offset="0%" style="stop-color:#0066cc"/>
<stop offset="100%" style="stop-color:#00cc99"/>
</linearGradient>
<filter id="glow">
<feGaussianBlur stdDeviation="3" result="coloredBlur"/>
<feMerge>
<feMergeNode in="coloredBlur"/>
<feMergeNode in="SourceGraphic"/>
</feMerge>
</filter>
</defs>
<g class="graph-nodes">
<circle cx="400" cy="50" r="40" fill="url(#mainGrad)" class="clickable-node" data-target="域/觉知" style="cursor:pointer;transition:all 0.3s;"/><text x="400" y="48" text-anchor="middle" fill="white" font-weight="bold" font-size="14">域/觉知</text>
<circle cx="400" cy="140" r="30" fill="#1890ff" class="clickable-node" data-target="旋量" style="cursor:pointer;transition:all 0.3s;"/><text x="400" y="138" text-anchor="middle" fill="white" font-size="12" font-weight="bold">旋量</text>
<circle cx="280" cy="230" r="25" fill="#1890ff" class="clickable-node" data-target="平方" style="cursor:pointer;transition:all 0.3s;"/><text x="280" y="228" text-anchor="middle" fill="white" font-size="11" font-weight="bold">平方</text>
<circle cx="520" cy="230" r="25" fill="#1890ff" class="clickable-node" data-target="开方" style="cursor:pointer;transition:all 0.3s;"/><text x="520" y="228" text-anchor="middle" fill="white" font-size="11" font-weight="bold">开方</text>
<circle cx="200" cy="320" r="22" fill="#666" class="clickable-node" data-target="矢量" style="cursor:pointer;transition:all 0.3s;"/><text x="200" y="318" text-anchor="middle" fill="white" font-size="10" font-weight="bold">矢量</text>
<circle cx="600" cy="320" r="22" fill="#666" class="clickable-node" data-target="时间" style="cursor:pointer;transition:all 0.3s;"/><text x="600" y="318" text-anchor="middle" fill="white" font-size="10" font-weight="bold">时间</text>
<circle cx="120" cy="410" r="20" fill="#52c41a" class="clickable-node" data-target="含德之厚" style="cursor:pointer;transition:all 0.3s;"/><text x="120" y="408" text-anchor="middle" fill="white" font-size="9" font-weight="bold">生命状态</text>
<circle cx="300" cy="410" r="20" fill="#fa8c16" class="clickable-node" data-target="爱" style="cursor:pointer;transition:all 0.3s;"/><text x="300" y="408" text-anchor="middle" fill="white" font-size="9" font-weight="bold">关系</text>
<circle cx="500" cy="410" r="20" fill="#722ed1" class="clickable-node" data-target="修行" style="cursor:pointer;transition:all 0.3s;"/><text x="500" y="408" text-anchor="middle" fill="white" font-size="9" font-weight="bold">心灵操作</text>
<circle cx="680" cy="410" r="20" fill="#13c2c2" class="clickable-node" data-target="道生一" style="cursor:pointer;transition:all 0.3s;"/><text x="680" y="408" text-anchor="middle" fill="white" font-size="9" font-weight="bold">经典读解</text>
</g>
<line x1="400" y1="90" x2="400" y2="110" stroke="#0066cc" stroke-width="3" marker-end="url(#arrowhead)"/>
<line x1="400" y1="170" x2="280" y2="205" stroke="#1890ff" stroke-width="2" marker-end="url(#arrowhead)"/>
<line x1="400" y1="170" x2="520" y2="205" stroke="#1890ff" stroke-width="2" marker-end="url(#arrowhead)"/>
<line x1="280" y1="255" x2="200" y2="298" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
<line x1="520" y1="255" x2="600" y2="298" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
<line x1="200" y1="342" x2="120" y2="390" stroke="#52c41a" stroke-width="2" marker-end="url(#arrowhead)"/>
<line x1="200" y1="342" x2="300" y2="390" stroke="#fa8c16" stroke-width="2" marker-end="url(#arrowhead)"/>
<line x1="600" y1="342" x2="500" y2="390" stroke="#722ed1" stroke-width="2" marker-end="url(#arrowhead)"/>
<line x1="600" y1="342" x2="680" y2="390" stroke="#13c2c2" stroke-width="2" marker-end="url(#arrowhead)"/>
<defs>
<marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
<polygon points="0 0, 10 3.5, 0 7" fill="#999"/>
</marker>
</defs>
</svg>
<div class="graph-hint" style="text-align:center;color:#999;font-size:13px;margin-top:15px;">💡 点击节点可跳转到对应词汇定义</div>
</div>
<div class="legend">
<div class="legend-item"><div class="legend-color" style="background:linear-gradient(135deg,#0066cc,#00cc99)"></div><span class="legend-text">本源概念</span></div>
<div class="legend-item"><div class="legend-color" style="background:#1890ff"></div><span class="legend-text">基础操作</span></div>
<div class="legend-item"><div class="legend-color" style="background:#666"></div><span class="legend-text">核心概念</span></div>
<div class="legend-item"><div class="legend-color" style="background:#52c41a"></div><span class="legend-text">生命状态</span></div>
<div class="legend-item"><div class="legend-color" style="background:#fa8c16"></div><span class="legend-text">关系</span></div>
<div class="legend-item"><div class="legend-color" style="background:#722ed1"></div><span class="legend-text">心灵操作</span></div>
<div class="legend-item"><div class="legend-color" style="background:#13c2c2"></div><span class="legend-text">经典读解</span></div>
</div>
</div>
'''

old_svg_pattern = r'<div id="graph" class="relation-graph">.*?</div>\s*<div class="legend">'
replacement = new_svg

content = re.sub(old_svg_pattern, new_svg, content, flags=re.DOTALL)

new_css = '''
.clickable-node:hover {
  transform: scale(1.15);
  filter: drop-shadow(0 0 8px rgba(0, 102, 204, 0.6));
}
.clickable-node.active {
  animation: pulse 1.5s infinite;
}
@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}
.highlight-card {
  animation: highlight 0.6s ease-out;
}
@keyframes highlight {
  0% { background-color: rgba(0, 102, 204, 0.3); }
  100% { background-color: transparent; }
}
.graph-container svg {
  overflow: visible;
}
'''

content = content.replace('</style>', new_css + '</style>')

new_script = '''
const nodes = document.querySelectorAll('.clickable-node');
nodes.forEach(node => {
  node.addEventListener('mouseenter', function() {
    this.style.filter = 'drop-shadow(0 0 10px rgba(0, 102, 204, 0.8))';
  });
  node.addEventListener('mouseleave', function() {
    this.style.filter = '';
  });
  node.addEventListener('click', function() {
    const targetTerm = this.getAttribute('data-target');
    const targetCard = document.querySelector(`[data-term="${targetTerm}"]`);
    if (targetCard) {
      document.querySelectorAll('.term-card').forEach(card => {
        card.classList.remove('highlight-card');
      });
      targetCard.classList.add('highlight-card');
      targetCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
      setTimeout(() => {
        targetCard.classList.remove('highlight-card');
      }, 1000);
    }
  });
});
'''

content = content.replace('</script>', new_script + '</script>')

with open("docs/10-词汇表/旋量太极词汇表_增强版.html", "w", encoding="utf-8") as f:
    f.write(content)

print("词汇关系图交互功能已添加完成！")
