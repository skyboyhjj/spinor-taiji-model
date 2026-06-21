import os
import json

def validate_build():
    """验证构建输出是否正确"""
    project_root = os.getcwd()
    dist_dir = os.path.join(project_root, "dist")
    dist_articles = os.path.join(dist_dir, "articles")
    config_path = os.path.join(project_root, "config", "article_aliases.json")
    
    print("=== 构建验证脚本 ===")
    print()
    
    # 加载配置
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    alias_map = config["aliases"]
    
    errors = []
    warnings = []
    successes = []
    
    # 1. 检查 dist 目录是否存在
    if not os.path.exists(dist_dir):
        errors.append(f"错误：dist 目录不存在: {dist_dir}")
    else:
        successes.append("✓ dist 目录存在")
    
    # 2. 检查 articles 目录
    if not os.path.exists(dist_articles):
        errors.append(f"错误：dist/articles 目录不存在")
    else:
        successes.append("✓ dist/articles 目录存在")
    
    # 3. 检查所有英文别名文件
    print("\n--- 检查英文别名文件 ---")
    for chinese_file, alias_file in alias_map.items():
        alias_path = os.path.join(dist_articles, alias_file)
        
        if not os.path.exists(alias_path):
            errors.append(f"错误：英文别名文件不存在: {alias_file}")
        else:
            # 检查文件大小
            file_size = os.path.getsize(alias_path)
            if file_size < 100:
                warnings.append(f"警告：文件过小，可能是重定向页面: {alias_file} ({file_size} bytes)")
            else:
                successes.append(f"✓ 英文别名文件正常: {alias_file}")
    
    # 4. 检查英文别名文件内容（不是重定向页面）
    print("\n--- 检查文件内容 ---")
    for chinese_file, alias_file in alias_map.items():
        alias_path = os.path.join(dist_articles, alias_file)
        if os.path.exists(alias_path):
            with open(alias_path, "r", encoding="utf-8") as f:
                content = f.read()
                if "meta http-equiv=\"refresh\"" in content or "window.location.href" in content:
                    errors.append(f"错误：英文别名文件是重定向页面: {alias_file}")
                elif "<html" in content.lower():
                    successes.append(f"✓ 文件包含 HTML 内容: {alias_file}")
                else:
                    warnings.append(f"警告：文件内容不像是 HTML: {alias_file}")
    
    # 5. 检查 _redirects 文件
    print("\n--- 检查 _redirects 文件 ---")
    redirects_path = os.path.join(dist_dir, "_redirects")
    if os.path.exists(redirects_path):
        with open(redirects_path, "r", encoding="utf-8") as f:
            content = f.read()
            rule_count = content.count("301")
            successes.append(f"✓ _redirects 文件存在，包含 {rule_count} 条规则")
    else:
        errors.append("错误：_redirects 文件不存在")
    
    # 6. 检查首页
    print("\n--- 检查首页 ---")
    index_path = os.path.join(dist_dir, "index.html")
    if os.path.exists(index_path):
        successes.append("✓ 首页 index.html 存在")
    else:
        errors.append("错误：首页 index.html 不存在")
    
    # 输出结果
    print("\n=== 验证结果 ===")
    print(f"\n成功: {len(successes)} 项")
    for s in successes:
        print(f"  {s}")
    
    if warnings:
        print(f"\n警告: {len(warnings)} 项")
        for w in warnings:
            print(f"  ⚠️ {w}")
    
    if errors:
        print(f"\n错误: {len(errors)} 项")
        for e in errors:
            print(f"  ❌ {e}")
        return False
    else:
        print("\n✅ 所有验证通过！")
        return True

if __name__ == "__main__":
    success = validate_build()
    exit(0 if success else 1)