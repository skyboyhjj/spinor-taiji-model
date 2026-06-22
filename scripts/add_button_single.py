import os

CSS_STYLES = '''
.back-to-home {
    position: fixed;
    bottom: 30px;
    right: 90px;
    width: 50px;
    height: 50px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 50%;
    cursor: pointer;
    opacity: 0;
    visibility: hidden;
    transition: all 0.3s;
    z-index: 1000;
    font-size: 16px;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}
.back-to-home.show {
    opacity: 1;
    visibility: visible;
}
.back-to-home:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
}
.back-to-top {
    position: fixed;
    bottom: 30px;
    right: 30px;
    width: 50px;
    height: 50px;
    background: linear-gradient(135deg, #0066cc, #00cc99);
    color: white;
    border: none;
    border-radius: 50%;
    cursor: pointer;
    opacity: 0;
    visibility: hidden;
    transition: all 0.3s;
    z-index: 1000;
    font-size: 16px;
    box-shadow: 0 4px 15px rgba(0, 102, 204, 0.4);
}
.back-to-top.show {
    opacity: 1;
    visibility: visible;
}
.back-to-top:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 20px rgba(0, 102, 204, 0.5);
}
@media (max-width: 768px) {
    .back-to-home {
        right: 65px;
        width: 45px;
        height: 45px;
        font-size: 14px;
    }
    .back-to-top {
        right: 15px;
        width: 45px;
        height: 45px;
        font-size: 14px;
    }
}
'''

BUTTONS = '''
<div class="nav-buttons">
    <button class="back-to-home" id="backToHome" title="返回首页">🏠</button>
    <button class="back-to-top" id="backToTop" title="返回顶部">↑</button>
</div>
<script>
const backToTopBtn = document.getElementById("backToTop");
const backToHomeBtn = document.getElementById("backToHome");
window.addEventListener("scroll", function() {
    const isVisible = window.scrollY > 300;
    backToTopBtn.classList.toggle("show", isVisible);
    backToHomeBtn.classList.toggle("show", isVisible);
});
backToTopBtn.addEventListener("click", () => window.scrollTo({ top: 0, behavior: "smooth" }));
backToHomeBtn.addEventListener("click", () => window.location.href = "/");
</script>
'''

filepath = 'articles/zh/spinor-taiji-model-statement.html'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

if 'back-to-home' in content:
    print('文件已包含按钮')
else:
    if '</style>' in content:
        content = content.replace('</style>', CSS_STYLES + '</style>')
    
    if '</body>' in content:
        content = content.replace('</body>', BUTTONS + '</body>')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print('按钮添加成功')
