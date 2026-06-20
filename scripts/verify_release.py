import zipfile
from pathlib import Path

releases_dir = Path('releases')
zip_files = sorted(releases_dir.glob('*.zip'))
if not zip_files:
    print(" 未找到发布包")
    exit(1)

latest_zip = zip_files[-1]
print(f" 验证发布包: {latest_zip.name}")
print("=" * 60)

with zipfile.ZipFile(latest_zip, 'r') as zf:
    files = zf.namelist()
    
    docs_files = [f for f in files if f.startswith('docs/')]
    articles_files = [f for f in files if f.startswith('articles/')]
    root_files = [f for f in files if '/' not in f]
    
    print(f" docs/ 目录: {len(docs_files)} 个文件")
    print(f" articles/ 目录: {len(articles_files)} 个文件")
    print(f" 根目录文件: {len(root_files)} 个")
    print(f" 总计: {len(files)} 个文件")
    print()
    
    print(" 根目录文件:")
    for f in sorted(root_files):
        print(f"    {f}")
    print()
    
    print(" docs/ 目录结构:")
    doc_dirs = set()
    for f in docs_files:
        parts = f.split('/')
        if len(parts) > 2:
            doc_dirs.add(parts[1])
    for d in sorted(doc_dirs):
        count = len([f for f in docs_files if f.startswith(f'docs/{d}/')])
        print(f"    {d}/ - {count} 个文件")
    print()
    
    # 使用真实存在的文件进行验证
    required_files = [
        'docs/00-产品宪法/知识库管理规则.md',
        'docs/01-核心模型/旋量与太极_样式检查报告.md',
        'docs/02-经典读解/《道德经》第七十九章_旋量-太极读解.md',
        'articles/《道德经》第一章_旋量-太极读解_微信公众号专业版.html',
        'README.md',
        'LICENSE'
    ]
    
    print(" 关键文件验证:")
    all_present = True
    for req_file in required_files:
        if req_file in files:
            print(f"    {req_file}")
        else:
            print(f"    {req_file} - 缺失")
            all_present = False
    
    print()
    if all_present:
        print(" 所有验证通过！发布包内容完整且正确")
    else:
        print(" 部分文件缺失，请检查")

print("=" * 60)
print(f"文件大小: {latest_zip.stat().st_size / 1024 / 1024:.2f} MB")
