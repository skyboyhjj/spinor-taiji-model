import os
import re

def generate_index(root_dir):
    """生成完整的知识库索引目录"""
    index_lines = []
    index_lines.append("# 旋量-太极模型知识库索引目录")
    index_lines.append("")
    index_lines.append("> 本索引目录自动生成，反映知识库最新结构")
    index_lines.append("")
    index_lines.append("---")
    index_lines.append("")
    index_lines.append("## 目录结构概览")
    index_lines.append("")
    
    # 目录结构树
    tree_lines = []
    tree_lines.append("```")
    tree_lines.append("spinor-taiji-model/")
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # 跳过隐藏目录
        dirnames[:] = [d for d in dirnames if not d.startswith('.')]
        dirnames.sort()
        filenames.sort()
        
        # 计算层级
        rel_path = os.path.relpath(dirpath, root_dir)
        depth = rel_path.count(os.sep) if rel_path != '.' else 0
        
        if depth == 0:
            prefix = " "
        else:
            prefix = "   " * (depth - 1) + " "
        
        # 添加目录
        if rel_path != '.':
            tree_lines.append(f"{prefix}{os.path.basename(dirpath)}/")
        
        # 添加文件（只显示前5个，避免过长）
        for i, filename in enumerate(filenames[:5]):
            file_prefix = "   " * depth + " "
            tree_lines.append(f"{file_prefix}{filename}")
        if len(filenames) > 5:
            file_prefix = "   " * depth + " ..."
            tree_lines.append(f"{file_prefix} (还有 {len(filenames) - 5} 个文件)")
    
    tree_lines.append("```")
    index_lines.extend(tree_lines)
    index_lines.append("")
    
    # 分类索引
    index_lines.append("---")
    index_lines.append("")
    index_lines.append("## 分类索引")
    index_lines.append("")
    
    categories = {
        "00-产品宪法": "项目核心规范文档",
        "01-核心模型": "基础理论与核心概念",
        "02-经典读解": "《道德经》各章解读",
        "03-应用实践": "跨领域应用案例",
        "04-阅读指南": "学习路径与指导",
        "05-五步读解法": "解经方法论体系",
        "09-参考文献": "学术参考资料",
        "10-词汇表": "术语定义与规范"
    }
    
    for cat, desc in categories.items():
        cat_path = os.path.join(root_dir, "docs", cat)
        if os.path.exists(cat_path):
            index_lines.append(f"### {cat}")
            index_lines.append(f"> {desc}")
            index_lines.append("")
            
            files = sorted([f for f in os.listdir(cat_path) if f.endswith('.md')])
            for f in files[:10]:
                index_lines.append(f"- [{f}](docs/{cat}/{f})")
            if len(files) > 10:
                index_lines.append(f"- ... 还有 {len(files) - 10} 个文件")
            index_lines.append("")
    
    # 快速导航
    index_lines.append("---")
    index_lines.append("")
    index_lines.append("## 快速导航")
    index_lines.append("")
    index_lines.append("| 需求 | 推荐位置 |")
    index_lines.append("|------|----------|")
    index_lines.append("| 了解项目背景 | docs/00-产品宪法 |")
    index_lines.append("| 理解核心理论 | docs/01-核心模型 |")
    index_lines.append("| 深入经典解读 | docs/02-经典读解 |")
    index_lines.append("| 寻找实践方法 | docs/03-应用实践 |")
    index_lines.append("| 规划学习路径 | docs/04-阅读指南 |")
    index_lines.append("| 掌握解读方法 | docs/05-五步读解法 |")
    index_lines.append("| 查阅参考文献 | docs/09-参考文献 |")
    index_lines.append("| 查询术语定义 | docs/10-词汇表 |")
    index_lines.append("")
    
    # 更新时间
    import datetime
    index_lines.append("---")
    index_lines.append("")
    index_lines.append(f"> 生成时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    index_lines.append(f"> 文件总数: {count_files(root_dir)}")
    
    return '\n'.join(index_lines)

def count_files(root_dir):
    """统计文件总数"""
    count = 0
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if not d.startswith('.')]
        count += len(filenames)
    return count

def update_readme(root_dir):
    """更新README.md"""
    readme_path = os.path.join(root_dir, "README.md")
    
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 更新目录结构部分
    new_tree = """## 目录结构

```
spinor-taiji-model/
 .github/              # GitHub配置
 articles/             # 公众号文章(HTML)
 data/                 # 数据文件
 docs/                 # 核心文档库
    00-产品宪法/      # 项目规范
    01-核心模型/      # 理论基础
    02-经典读解/      # 道德经解读
    03-应用实践/      # 应用案例
    04-阅读指南/      # 学习指导
    05-五步读解法/    # 方法论
    09-参考文献/      # 参考资料
    10-词汇表/        # 术语规范
 media/                # 媒体资源
 scripts/              # 工具脚本
 skill/                # 技能文档
 templates/            # 模板文件
 README.md             # 项目说明
 requirements.txt      # Python依赖
```"""
    
    content = re.sub(r'## 目录结构.*?(?=\n##|\Z)', new_tree, content, flags=re.DOTALL)
    
    # 更新快速入口
    new_entries = """### 快速入口

| 需求 | 推荐目录 |
|------|----------|
| 了解项目背景 | docs/00-产品宪法 |
| 理解核心理论 | docs/01-核心模型 |
| 深入经典解读 | docs/02-经典读解 |
| 寻找实践方法 | docs/03-应用实践 |
| 规划学习路径 | docs/04-阅读指南 |
| 掌握解读方法 | docs/05-五步读解法 |
| 查阅参考文献 | docs/09-参考文献 |
| 查询术语定义 | docs/10-词汇表 |
| 使用工具脚本 | scripts/ |
| 查看公众号文章 | articles/ |"""
    
    content = re.sub(r'### 快速入口.*?(?=\n##|\Z)', new_entries, content, flags=re.DOTALL)
    
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    root_dir = '.'
    
    print("Generating knowledge base index...")
    index_content = generate_index(root_dir)
    
    index_path = os.path.join(root_dir, "docs", "知识库索引目录.md")
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_content)
    print(f"Index file created: {index_path}")
    
    print("Updating README.md...")
    update_readme(root_dir)
    print("README.md updated successfully")
    
    print("")
    print("=" * 60)
    print("Knowledge base index generation complete!")
    print("=" * 60)

if __name__ == '__main__':
    main()
