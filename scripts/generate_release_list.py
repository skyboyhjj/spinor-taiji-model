import os
from pathlib import Path

print("=" * 70)
print("Spinor-Taiji Model - 发布清单生成")
print("=" * 70)
print()

RELEASE_DIRS = ["docs", "articles"]
ROOT_FILES = ["README.md", "LICENSE", "CONTRIBUTING.md", "发布文件清单.md"]

release_files = []

for dir_name in RELEASE_DIRS:
    dir_path = Path(dir_name)
    if dir_path.exists():
        for root, dirs, files in os.walk(dir_path):
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            for file in sorted(files):
                if not any(file.startswith(".") or file.endswith(ext) for ext in [".pyc", ".pyo", ".log", ".tmp", ".bak"]):
                    full_path = Path(root) / file
                    rel_path = full_path.relative_to(".")
                    size = full_path.stat().st_size
                    release_files.append({
                        "path": str(rel_path),
                        "size": size,
                        "type": dir_name
                    })

for file in ROOT_FILES:
    if Path(file).exists():
        size = Path(file).stat().st_size
        release_files.append({
            "path": file,
            "size": size,
            "type": "root"
        })

docs_files = [f for f in release_files if f["type"] == "docs"]
articles_files = [f for f in release_files if f["type"] == "articles"]
root_files = [f for f in release_files if f["type"] == "root"]

total_size = sum(f["size"] for f in release_files)

print("发布清单统计")
print("-" * 70)
print(f"总计文件数: {len(release_files)}")
print(f"总计大小: {total_size / 1024 / 1024:.2f} MB")
print()

print("docs/ 目录 (核心文档库)")
print("-" * 70)
subdirs = {}
for f in sorted(docs_files, key=lambda x: x["path"]):
    parts = f["path"].split("/")
    subdir = parts[1] if len(parts) > 1 else "根目录"
    if subdir not in subdirs:
        subdirs[subdir] = []
    subdirs[subdir].append(f)

for subdir, files in sorted(subdirs.items()):
    print(f"  {subdir}/ ({len(files)} 个文件)")
    for f in files[:10]:
        print(f"     - {f['path']}")
    if len(files) > 10:
        print(f"     ... 还有 {len(files) - 10} 个文件")
print(f"  小计: {len(docs_files)} 个文件")
print()

print("articles/ 目录 (公众号文章)")
print("-" * 70)
for f in sorted(articles_files, key=lambda x: x["path"]):
    print(f"  - {f['path']}")
print(f"小计: {len(articles_files)} 个文件")
print()

print("根目录文件")
print("-" * 70)
for f in sorted(root_files, key=lambda x: x["path"]):
    print(f"  - {f['path']}")
print()

print("=" * 70)
print("发布清单生成完成")
print("=" * 70)
