#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
仓库目录结构整理脚本
- 将脚本文件移动到 scripts/
- 将图片文件移动到 media/
- 将公众号文章（HTML）移动到 articles/
- 将数据文件移动到 data/
- 保持 docs/ 只包含 Markdown 文档
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

# 仓库根目录
REPO_ROOT = Path(r'E:\Trac Project\spinor-taiji-model')

# 目标目录
TARGET_DIRS = {
    'scripts': REPO_ROOT / 'scripts',
    'media': REPO_ROOT / 'media',
    'articles': REPO_ROOT / 'articles',
    'data': REPO_ROOT / 'data',
    'templates': REPO_ROOT / 'templates',
}

# 文件分类规则
FILE_RULES = {
    # 脚本文件 -> scripts/
    '.py': 'scripts',
    '.bat': 'scripts',
    '.sh': 'scripts',
    '.mmd': 'scripts',  # Mermaid流程图
    
    # 图片文件 -> media/
    '.png': 'media',
    '.jpg': 'media',
    '.jpeg': 'media',
    '.gif': 'media',
    '.svg': 'media',
    '.webp': 'media',
    
    # 公众号文章 -> articles/
    '_公众号版.html': 'articles',
    '_公众号专业版.html': 'articles',
    '_微信公众号版.html': 'articles',
    '_公众号排版版.html': 'articles',
    '_内联样式.html': 'articles',
    
    # 数据文件 -> data/
    '.json': 'data',
    '.txt': 'data',
    
    # 模板文件 -> templates/
    '_模板.html': 'templates',
    '模板': 'templates',
    
    # PDF文件 -> docs/（保持原位）
    '.pdf': 'docs',
    
    # Markdown文件 -> docs/（保持原位）
    '.md': 'docs',
}

# 排除移动的文件（根目录核心文件）
EXCLUDE_FILES = [
    'README.md',
    '.gitignore',
    'LICENSE',
    'CONTRIBUTING.md',
    'requirements.txt',
]

def get_target_dir(filepath):
    """根据文件类型确定目标目录"""
    filepath_str = str(filepath)
    
    # 检查文件名中的特殊模式
    for pattern, target in FILE_RULES.items():
        if pattern.startswith('_') and pattern in filepath_str:
            return TARGET_DIRS.get(target)
    
    # 检查文件扩展名
    ext = filepath.suffix.lower()
    for pattern, target in FILE_RULES.items():
        if pattern == ext:
            return TARGET_DIRS.get(target)
    
    return None  # 保持原位

def organize_files():
    """整理文件"""
    print("=" * 70)
    print("仓库目录结构整理")
    print("=" * 70)
    print()
    
    # 创建目标目录
    for name, path in TARGET_DIRS.items():
        path.mkdir(parents=True, exist_ok=True)
        print(f"✅ 创建目录: {name}/")
    
    print()
    
    # 统计
    stats = {
        'scripts': 0,
        'media': 0,
        'articles': 0,
        'data': 0,
        'templates': 0,
        'kept': 0,
    }
    
    # 遍历 docs/ 目录
    docs_dir = REPO_ROOT / 'docs'
    
    for file_path in docs_dir.rglob('*'):
        if not file_path.is_file():
            continue
        
        # 检查是否是排除文件
        if file_path.name in EXCLUDE_FILES:
            continue
        
        # 确定目标目录
        target_dir = get_target_dir(file_path)
        
        if target_dir is None:
            stats['kept'] += 1
            continue
        
        # 计算相对路径（保持子目录结构）
        rel_path = file_path.relative_to(docs_dir)
        
        # 构建目标路径
        target_path = target_dir / rel_path
        
        # 创建目标目录
        target_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 移动文件
        try:
            shutil.move(str(file_path), str(target_path))
            
            category = None
            for name, path in TARGET_DIRS.items():
                if path == target_dir:
                    category = name
                    break
            
            stats[category] += 1
            print(f"✅ [{category}] {rel_path}")
            
        except Exception as e:
            print(f"❌ 移动失败: {rel_path} - {e}")
    
    # 清理空目录
    print()
    print("清理空目录...")
    for dir_path in docs_dir.rglob('*'):
        if dir_path.is_dir() and not any(dir_path.iterdir()):
            dir_path.rmdir()
            print(f"  🗑️ 删除空目录: {dir_path.relative_to(docs_dir)}")
    
    # 输出统计
    print()
    print("=" * 70)
    print("整理完成统计")
    print("=" * 70)
    print(f"  scripts/  : {stats['scripts']} 个文件")
    print(f"  media/    : {stats['media']} 个文件")
    print(f"  articles/ : {stats['articles']} 个文件")
    print(f"  data/     : {stats['data']} 个文件")
    print(f"  templates/: {stats['templates']} 个文件")
    print(f"  docs/保留 : {stats['kept']} 个文件")
    print("=" * 70)
    
    return stats

def create_directory_guide():
    """创建目录说明文档"""
    guide_content = """# 仓库目录结构说明

本文档说明 Spinor-Taiji Model 项目的目录结构和文件存放规则。

## 目录结构

```
spinor-taiji-model/
├── docs/                    # 文档目录（主要文档存储位置）
│   ├── 02-文化自信/         # 文化自信主题文档
│   ├── 03-道境坐标系/       # 道境坐标系文档
│   ├── 04-伦理即道体/       # 伦理即道体文档
│   ├── 05-端云一体化/       # 端云一体化文档
│   ├── 06-何为欲/           # 何为欲文档
│   ├── 07-旋量-太极读解道德经/  # 道德经解读文档
│   ├── 08-呼吸-特德·姜/     # 呼吸主题文档
│   ├── 09-明朝/             # 明朝研究文档
│   └── 10-时空/             # 时空主题文档
├── articles/                # 公众号文章（HTML版本）
├── scripts/                 # 代码脚本
├── data/                    # 数据文件
├── media/                   # 媒体文件（图片、音频、视频）
├── templates/               # 模板文件
├── .github/                 # GitHub配置
├── README.md                # 项目说明
├── .gitignore               # Git忽略配置
├── LICENSE                  # 许可证
├── CONTRIBUTING.md          # 贡献指南
└── requirements.txt         # Python依赖
```

## 文件存放规则

### docs/ 目录
存放所有 Markdown 文档和理论文档：
- `.md` 文件：Markdown 文档
- `.pdf` 文件：PDF 文档

### articles/ 目录
存放公众号文章的 HTML 版本：
- `*_公众号版.html`
- `*_公众号专业版.html`
- `*_微信公众号版.html`
- `*_公众号排版版.html`
- `*_内联样式.html`

### scripts/ 目录
存放所有代码脚本：
- `.py` 文件：Python 脚本
- `.bat` 文件：批处理脚本
- `.sh` 文件：Shell 脚本
- `.mmd` 文件：Mermaid 流程图

### media/ 目录
存放所有媒体文件：
- `.png`、`.jpg`、`.jpeg`：图片文件
- `.gif`、`.svg`、`.webp`：其他图片格式
- 音频、视频文件

### data/ 目录
存放数据文件：
- `.json` 文件：配置数据
- `.txt` 文件：文本数据

### templates/ 目录
存放模板文件：
- HTML 模板
- 文档模板

## 根目录核心文件

以下文件保持在根目录，不进行移动：
- `README.md`：项目说明文档
- `.gitignore`：Git 忽略配置
- `LICENSE`：项目许可证
- `CONTRIBUTING.md`：贡献指南
- `requirements.txt`：Python 依赖列表

## 版本历史

| 日期 | 版本 | 说明 |
|------|------|------|
| 2026-06-20 | v1.0 | 初始目录结构整理 |

---
*最后更新：2026-06-20*
"""
    
    guide_path = REPO_ROOT / 'docs' / '目录结构说明.md'
    guide_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(guide_path, 'w', encoding='utf-8') as f:
        f.write(guide_content)
    
    print(f"\n✅ 创建目录说明文档: docs/目录结构说明.md")

def main():
    # 整理文件
    stats = organize_files()
    
    # 创建目录说明
    create_directory_guide()
    
    print("\n下一步操作:")
    print("1. cd 'E:\\Trac Project\\spinor-taiji-model'")
    print("2. git add .")
    print("3. git commit -m 'Reorganize: directory structure'")
    print("4. git push origin master")

if __name__ == '__main__':
    main()