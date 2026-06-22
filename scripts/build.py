import os
import shutil
import json

def load_config(config_path):
    """从配置文件加载别名映射"""
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    return config

def main():
    project_root = os.getcwd()
    articles_src = os.path.join(project_root, "articles")
    docs_src = os.path.join(project_root, "docs")
    dist_dir = os.path.join(project_root, "dist")
    dist_articles = os.path.join(dist_dir, "articles")
    dist_docs = os.path.join(dist_dir, "docs")
    config_path = os.path.join(project_root, "config", "article_aliases.json")

    if not os.path.exists(dist_dir):
        os.makedirs(dist_dir)

    if os.path.exists(dist_articles):
        shutil.rmtree(dist_articles)
    shutil.copytree(articles_src, dist_articles)
    print("复制 articles 目录 (包含 en/zh 子目录)")

    if os.path.exists(dist_docs):
        shutil.rmtree(dist_docs)
    shutil.copytree(docs_src, dist_docs)
    print("复制 docs 目录")

    # 从配置文件加载别名映射
    config = load_config(config_path)
    alias_map = config["aliases"]
    print(f"加载配置文件: {config_path}")
    print(f"配置版本: {config.get('version', '1.0')}")

    # 将中文主文件内容复制到英文别名文件（在zh目录内）
    dist_zh = os.path.join(dist_articles, "zh")
    for chinese_file, alias_file in alias_map.items():
        chinese_path = os.path.join(dist_zh, chinese_file)
        alias_path = os.path.join(dist_zh, alias_file)
        if os.path.exists(chinese_path):
            shutil.copy2(chinese_path, alias_path)
            print(f"复制中文别名: {chinese_file} -> zh/{alias_file}")

    index_html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>旋量太极知识库 | Spinor-Taiji Knowledge Base</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; line-height: 1.6; color: #333; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        header { background: rgba(255,255,255,0.95); backdrop-filter: blur(10px); border-radius: 16px; padding: 20px 30px; margin-bottom: 30px; box-shadow: 0 10px 40px rgba(0,0,0,0.1); }
        .header-top { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px; }
        .logo { font-size: 24px; font-weight: bold; color: #333; }
        .logo-en { font-size: 14px; font-weight: normal; color: #666; margin-left: 10px; }
        .lang-switcher { display: flex; gap: 10px; }
        .lang-btn { padding: 8px 20px; border: 2px solid #667eea; border-radius: 25px; background: transparent; cursor: pointer; transition: all 0.3s; font-size: 14px; }
        .lang-btn:hover { background: #667eea; color: white; }
        .lang-btn.active { background: #667eea; color: white; }
        .main-content { display: grid; gap: 30px; }
        .card { background: rgba(255,255,255,0.95); backdrop-filter: blur(10px); border-radius: 16px; padding: 30px; box-shadow: 0 10px 40px rgba(0,0,0,0.1); }
        .card-title { font-size: 20px; font-weight: bold; color: #333; margin-bottom: 20px; padding-bottom: 15px; border-bottom: 2px solid #eee; }
        .card-title-en { font-size: 14px; font-weight: normal; color: #666; margin-left: 10px; }
        .btn { display: inline-block; padding: 12px 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-decoration: none; border-radius: 25px; font-weight: 600; transition: transform 0.3s, box-shadow 0.3s; }
        .btn:hover { transform: translateY(-2px); box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4); }
        .btn-outline { background: transparent; border: 2px solid #667eea; color: #667eea; }
        .btn-outline:hover { background: #667eea; color: white; }
        .glossary-preview { margin-top: 20px; }
        .glossary-item { padding: 15px; border-left: 4px solid #667eea; margin-bottom: 10px; background: #f8f9fa; border-radius: 0 8px 8px 0; }
        .glossary-term { font-weight: bold; color: #333; }
        .glossary-def { color: #666; margin-top: 5px; }
        .declaration-preview { margin-top: 20px; }
        .declaration-text { color: #555; line-height: 1.8; }
        .declaration-tag { display: inline-block; padding: 5px 15px; background: #e8f5e9; color: #2e7d32; border-radius: 20px; font-size: 12px; margin-right: 10px; margin-bottom: 10px; }
        footer { text-align: center; color: rgba(255,255,255,0.8); margin-top: 50px; padding: 20px; }
    </style>
    <script>
        function setLanguage(lang) {
            document.documentElement.lang = lang;
            document.querySelectorAll('.lang-btn').forEach(btn => btn.classList.remove('active'));
            document.querySelector(`[data-lang="${lang}"]`).classList.add('active');
            
            const contentZh = document.querySelectorAll('.content-zh');
            const contentEn = document.querySelectorAll('.content-en');
            
            if (lang === 'zh-CN') {
                contentZh.forEach(el => el.style.display = 'block');
                contentEn.forEach(el => el.style.display = 'none');
            } else {
                contentZh.forEach(el => el.style.display = 'none');
                contentEn.forEach(el => el.style.display = 'block');
            }
            
            localStorage.setItem('preferredLanguage', lang);
        }
        
        document.addEventListener('DOMContentLoaded', () => {
            const savedLang = localStorage.getItem('preferredLanguage') || 'zh-CN';
            setLanguage(savedLang);
        });
    </script>
</head>
<body>
    <div class="container">
        <header>
            <div class="header-top">
                <div>
                    <span class="logo content-zh">旋量太极知识库</span>
                    <span class="logo content-en">Spinor-Taiji Knowledge Base</span>
                    <span class="logo-en content-zh">Knowledge Base</span>
                    <span class="logo-en content-en">旋量太极知识库</span>
                </div>
                <div class="lang-switcher">
                    <button class="lang-btn" data-lang="zh-CN" onclick="setLanguage('zh-CN')">中文</button>
                    <button class="lang-btn" data-lang="en" onclick="setLanguage('en')">English</button>
                </div>
            </div>
        </header>

        <div class="main-content">
            <div class="card">
                <h2 class="card-title">
                    <span class="content-zh">📚 词汇表</span>
                    <span class="content-en">📚 Glossary</span>
                    <span class="card-title-en content-zh">Glossary</span>
                    <span class="card-title-en content-en">词汇表</span>
                </h2>
                <div class="content-zh">
                    <p style="color: #666; margin-bottom: 20px;">探索旋量太极理论中的核心概念与术语，理解宇宙的振动本质。</p>
                    <div class="glossary-preview">
                        <div class="glossary-item">
                            <div class="glossary-term">旋量 (Spinor)</div>
                            <div class="glossary-def">需720°复原的振动种子，正负双解共源</div>
                        </div>
                        <div class="glossary-item">
                            <div class="glossary-term">时间 (Time)</div>
                            <div class="glossary-def">平方与开方的连续脉冲</div>
                        </div>
                        <div class="glossary-item">
                            <div class="glossary-term">爱 (Love)</div>
                            <div class="glossary-def">两旋量场的相位锁定</div>
                        </div>
                    </div>
                    <div style="margin-top: 20px;">
                        <a href="articles/zh/spinor-taiji-glossary.html" class="btn">查看完整词汇表</a>
                    </div>
                </div>
                <div class="content-en" style="display: none;">
                    <p style="color: #666; margin-bottom: 20px;">Explore core concepts and terminology in Spinor-Taiji theory, understanding the vibrational nature of the universe.</p>
                    <div class="glossary-preview">
                        <div class="glossary-item">
                            <div class="glossary-term">Spinor</div>
                            <div class="glossary-def">A vibrational seed requiring 720° restoration, with dual positive and negative solutions</div>
                        </div>
                        <div class="glossary-item">
                            <div class="glossary-term">Time</div>
                            <div class="glossary-def">Continuous pulse of squaring and rooting operations</div>
                        </div>
                        <div class="glossary-item">
                            <div class="glossary-term">Love</div>
                            <div class="glossary-def">Phase locking of two spinor fields</div>
                        </div>
                    </div>
                    <div style="margin-top: 20px;">
                        <a href="articles/en/spinor-taiji-glossary.html" class="btn">View Full Glossary</a>
                    </div>
                </div>
            </div>

            <div class="card">
                <h2 class="card-title">
                    <span class="content-zh">📖 旋量-太极模型声明</span>
                    <span class="content-en">📖 Spinor-Taiji Model Declaration</span>
                    <span class="card-title-en content-zh">Model Declaration</span>
                    <span class="card-title-en content-en">旋量-太极模型声明</span>
                </h2>
                <div class="content-zh">
                    <div class="declaration-preview">
                        <div style="margin-bottom: 15px;">
                            <span class="declaration-tag">本体论声明</span>
                            <span class="declaration-tag">方法论框架</span>
                            <span class="declaration-tag">实践指南</span>
                        </div>
                        <p class="declaration-text">
                            <strong>旋量-太极模型</strong>是一个基于量子力学与东方哲学融合的认知框架。它将旋量（Spinor）作为宇宙的基本振动单元，
                            通过平方与开方的操作来描述从潜能到显现的转化过程。
                        </p>
                        <p class="declaration-text" style="margin-top: 15px;">
                            模型的核心命题是：<strong>"万物皆旋量，旋量即道"</strong>。
                            一切存在都是不同频率的旋量振动，而道则是容纳所有旋量生灭的空性场域。
                        </p>
                    </div>
                    <div style="margin-top: 20px;">
                        <a href="articles/zh/spinor-taiji-model-statement.html" class="btn">阅读完整声明</a>
                    </div>
                </div>
                <div class="content-en" style="display: none;">
                    <div class="declaration-preview">
                        <div style="margin-bottom: 15px;">
                            <span class="declaration-tag">Ontological Declaration</span>
                            <span class="declaration-tag">Methodological Framework</span>
                            <span class="declaration-tag">Practice Guide</span>
                        </div>
                        <p class="declaration-text">
                            The <strong>Spinor-Taiji Model</strong> is a cognitive framework integrating quantum mechanics with Eastern philosophy. 
                            It takes Spinor as the fundamental vibrational unit of the universe, describing the transformation from potential to manifestation 
                            through squaring and rooting operations.
                        </p>
                        <p class="declaration-text" style="margin-top: 15px;">
                            The core proposition of the model is: <strong>"All things are spinors, spinors are the Dao"</strong>. 
                            All existence is spinor vibration at different frequencies, and the Dao is the empty field that contains all spinor births and deaths.
                        </p>
                    </div>
                    <div style="margin-top: 20px;">
                        <a href="articles/en/spinor-taiji-model-declaration.html" class="btn">Read Full Declaration</a>
                    </div>
                </div>
            </div>

        </div>

        <footer>
            <p class="content-zh">旋量太极知识库 © 2026 | 探索宇宙的振动本质</p>
            <p class="content-en" style="display: none;">Spinor-Taiji Knowledge Base © 2026 | Exploring the vibrational nature of the universe</p>
        </footer>
    </div>
</body>
</html>"""
    with open(os.path.join(dist_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)
    print("创建首页（支持语言切换）")

    # 从配置文件生成 _redirects 文件
    redirect_rules = config.get("redirect_rules", {}).get("rules", [])
    redirects_lines = ["# Cloudflare Pages 重定向规则", "# 中文主文件 -> 英文别名（用于SEO优化）", ""]
    for rule in redirect_rules:
        redirects_lines.append(f"{rule['from']} {rule['to']} {rule['status']}")
    redirects_lines.append("")
    redirects_lines.append("# 首页重定向")
    redirects_lines.append("/docs/ / 301")
    redirects_content = "\n".join(redirects_lines)
    
    with open(os.path.join(dist_dir, "_redirects"), "w", encoding="utf-8") as f:
        f.write(redirects_content)
    print(f"创建 _redirects 文件 (共 {len(redirect_rules)} 条规则)")

    # 生成 _headers 文件
    headers_config_path = os.path.join(project_root, "config", "headers_config.json")
    if os.path.exists(headers_config_path):
        headers_config = load_config(headers_config_path)
        headers_lines = []
        for header_rule in headers_config["headers"]:
            headers_lines.append(f"{header_rule['path']}")
            for name, value in header_rule["headers"].items():
                headers_lines.append(f"  {name}: {value}")
            headers_lines.append("")
        headers_content = "\n".join(headers_lines)
        
        with open(os.path.join(dist_dir, "_headers"), "w", encoding="utf-8") as f:
            f.write(headers_content)
        print(f"创建 _headers 文件 (共 {len(headers_config['headers'])} 条规则)")
    else:
        print(f"警告：未找到 headers 配置文件: {headers_config_path}")

    article_count = 0
    for root, dirs, files in os.walk(dist_articles):
        for f in files:
            if f.endswith(".html"):
                article_count += 1
    print(f"构建完成！articles文件数: {article_count}")

if __name__ == "__main__":
    main()
