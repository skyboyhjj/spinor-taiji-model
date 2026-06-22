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

    index_html = "<!DOCTYPE html><html lang='zh-CN'><head><meta charset='UTF-8'><title>旋量太极知识库</title></head><body><h1>旋量太极知识库</h1><a href='docs/'>文档</a></body></html>"
    with open(os.path.join(dist_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)
    print("创建首页")

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
