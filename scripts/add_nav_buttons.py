import os
import re

CSS_STYLES = """
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
"""

HTML_BUTTONS = """
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
"""

HTML_BUTTONS_EN = """
<div class="nav-buttons">
    <button class="back-to-home" id="backToHome" title="Back to Home">🏠</button>
    <button class="back-to-top" id="backToTop" title="Back to Top">↑</button>
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
"""

def is_redirect_page(content):
    if 'meta http-equiv="refresh"' in content:
        return True
    if 'window.location.href' in content and len(content) < 500:
        return True
    return False

def has_nav_buttons(content):
    return 'back-to-home' in content

def add_buttons_to_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if is_redirect_page(content):
        print(f"跳过重定向页面: {filepath}")
        return False
    
    if has_nav_buttons(content):
        print(f"已存在按钮: {filepath}")
        return False
    
    print(f"处理页面: {filepath}")
    
    is_chinese = '/zh/' in filepath
    buttons = HTML_BUTTONS if is_chinese else HTML_BUTTONS_EN
    
    if '</style>' in content:
        content = content.replace('</style>', CSS_STYLES + '</style>')
    elif '<style' in content and '</head>' in content:
        content = content.replace('</head>', '<style>' + CSS_STYLES + '</style></head>')
    
    if '</body>' in content:
        content = content.replace('</body>', buttons + '</body>')
    elif content.strip().startswith('<section'):
        content = content + '<style>' + CSS_STYLES + '</style>' + buttons
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def process_directory(directory):
    processed_count = 0
    skipped_count = 0
    
    for filename in os.listdir(directory):
        if filename.endswith('.html'):
            filepath = os.path.join(directory, filename)
            if add_buttons_to_file(filepath):
                processed_count += 1
            else:
                skipped_count += 1
    
    print(f"\n处理完成: {directory}")
    print(f"已添加按钮: {processed_count}")
    print(f"跳过: {skipped_count}")

if __name__ == '__main__':
    articles_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/articles'
    
    en_dir = os.path.join(articles_dir, 'en')
    zh_dir = os.path.join(articles_dir, 'zh')
    
    print("=== 处理英文目录 ===")
    process_directory(en_dir)
    
    print("\n=== 处理中文目录 ===")
    process_directory(zh_dir)
    
    print("\n=== 全部完成 ===")