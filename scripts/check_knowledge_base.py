import os
from pathlib import Path

print("=" * 70)
print("知识库文件完整性检查")
print("=" * 70)
print()

docs_dir = Path('docs')
issues = []
checks = []

# 1. 检查各分类目录是否存在
categories = [
    ('00-产品宪法', ['知识库管理规则.md', '目录结构评估报告.md']),
    ('01-核心模型', ['旋量与太极的关系.md']),
    ('02-经典读解', []),
    ('03-应用实践', []),
    ('04-阅读指南', []),
    ('05-五步读解法', []),
    ('09-参考文献', []),
    ('10-词汇表', ['旋量太极词汇表.md', '词汇主表维护规范.md', '定义变更日志.md', '词汇关系图.md'])
]

print(" 目录结构检查:")
print("-" * 50)
for cat, required_files in categories:
    cat_path = docs_dir / cat
    if cat_path.exists():
        files = list(cat_path.glob('*'))
        md_files = [f for f in files if f.suffix == '.md']
        print(f" {cat}/ - {len(md_files)} 个Markdown文件")
        checks.append(True)
        
        # 检查必需文件
        for req_file in required_files:
            req_path = cat_path / req_file
            if req_path.exists():
                print(f"    {req_file}")
            else:
                print(f"    {req_file} - 未找到")
                issues.append(f"缺少: {cat}/{req_file}")
    else:
        print(f" {cat}/ - 目录不存在")
        issues.append(f"缺少目录: {cat}")
        checks.append(False)

print()
print(" 关键文档检查:")
print("-" * 50)

key_docs = [
    'docs/00-产品宪法/知识库管理规则.md',
    'docs/10-词汇表/旋量太极词汇表.md',
    'docs/10-词汇表/词汇主表维护规范.md',
    'docs/00-产品宪法/文件清理记录_20260620.md',
    'docs/知识库索引目录.md'
]

for doc in key_docs:
    doc_path = Path(doc)
    if doc_path.exists():
        size = doc_path.stat().st_size
        lines = len(doc_path.read_text(encoding='utf-8').splitlines())
        print(f" {doc}")
        print(f"   大小: {size/1024:.1f}KB, 行数: {lines}")
        checks.append(True)
    else:
        print(f" {doc} - 文件不存在")
        issues.append(f"缺少: {doc}")
        checks.append(False)

print()
print(" 文件命名规范检查:")
print("-" * 50)

naming_issues = []
for md_file in docs_dir.rglob('*.md'):
    filename = md_file.name
    # 检查空格
    if ' ' in filename:
        naming_issues.append(f"空格: {md_file.relative_to(docs_dir)}")
    # 检查特殊字符
    special_chars = ['@', '#', '$', '%', '^', '&', '*', '(', ')']
    if any(c in filename for c in special_chars):
        naming_issues.append(f"特殊字符: {md_file.relative_to(docs_dir)}")

if naming_issues:
    print(f" 发现 {len(naming_issues)} 个命名问题:")
    for issue in naming_issues[:5]:
        print(f"   {issue}")
    issues.extend(naming_issues)
else:
    print(" 所有文件命名符合规范")

print()
print("=" * 70)
print("检查结果汇总")
print("=" * 70)
print(f"检查项: {len(checks)} 项")
print(f"通过: {sum(checks)} 项")
print(f"问题: {len(issues)} 项")

if issues:
    print()
    print(" 发现的问题:")
    for issue in issues[:10]:
        print(f"   - {issue}")
    if len(issues) > 10:
        print(f"   ... 还有 {len(issues) - 10} 个问题")
else:
    print()
    print(" 所有检查通过！知识库文件完整且规范。")

print("=" * 70)
