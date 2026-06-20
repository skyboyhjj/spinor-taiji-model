#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
发布内容筛选与打包脚本

功能：
1. 筛选符合发布规范的文件（仅 docs/ 和 articles/）
2. 创建发布包
3. 验证发布内容完整性

VERSION: v1.0.0
CREATED: 2026-06-20
"""

import os
import shutil
import zipfile
from pathlib import Path
from datetime import datetime

# 发布内容定义
RELEASE_CONTENT = {
    'directories': [
        'docs',
        'articles'
    ],
    'root_files': [
        'README.md',
        'LICENSE',
        'CONTRIBUTING.md',
        '发布文件清单.md'
    ]
}

# 排除规则
EXCLUDE_PATTERNS = [
    '.git',
    '__pycache__',
    '.pyc',
    '.pyo',
    '.pyd',
    '.log',
    '.tmp',
    '.bak',
    '.backup',
    '.DS_Store',
    'Thumbs.db',
    'venv',
    'env',
    '.venv',
    '.vscode',
    '.idea'
]

def should_exclude(name):
    """判断是否应排除"""
    for pattern in EXCLUDE_PATTERNS:
        if name == pattern or name.startswith(pattern):
            return True
    return False

def copy_release_files(source_dir, dest_dir):
    """复制发布文件"""
    stats = {
        'directories': 0,
        'files': 0,
        'skipped': 0
    }
    
    # 复制目录
    for dir_name in RELEASE_CONTENT['directories']:
        src_path = source_dir / dir_name
        dest_path = dest_dir / dir_name
        
        if not src_path.exists():
            print(f" 目录不存在: {dir_name}")
            continue
        
        shutil.copytree(src_path, dest_path, ignore=shutil.ignore_patterns(*EXCLUDE_PATTERNS))
        stats['directories'] += 1
        
        # 统计文件数
        for _, _, files in os.walk(dest_path):
            stats['files'] += len(files)
    
    # 复制根目录文件
    for file_name in RELEASE_CONTENT['root_files']:
        src_path = source_dir / file_name
        dest_path = dest_dir / file_name
        
        if src_path.exists():
            shutil.copy(src_path, dest_path)
            stats['files'] += 1
        else:
            print(f" 文件不存在: {file_name}")
            stats['skipped'] += 1
    
    return stats

def create_release_package(source_dir, output_dir=None):
    """创建发布包"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    package_name = f"spinor-taiji-release_{timestamp}"
    
    if output_dir is None:
        output_dir = source_dir / 'releases'
    
    # 创建输出目录
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建临时目录
    temp_dir = output_dir / package_name
    temp_dir.mkdir(exist_ok=True)
    
    print(f" 创建发布包: {package_name}")
    print("-" * 50)
    
    # 复制文件
    stats = copy_release_files(source_dir, temp_dir)
    
    # 创建ZIP包
    zip_path = output_dir / f"{package_name}.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(temp_dir):
            dirs[:] = [d for d in dirs if not should_exclude(d)]
            for file in files:
                if should_exclude(file):
                    continue
                file_path = Path(root) / file
                arcname = file_path.relative_to(temp_dir)
                zf.write(file_path, arcname)
    
    # 清理临时目录
    shutil.rmtree(temp_dir)
    
    print("-" * 50)
    print(f" 发布包创建完成")
    print(f"   目录数: {stats['directories']}")
    print(f"   文件数: {stats['files']}")
    print(f"   跳过: {stats['skipped']}")
    print(f"   位置: {zip_path}")
    
    return zip_path

def validate_release(source_dir):
    """验证发布内容"""
    print(" 验证发布内容...")
    print("-" * 50)
    
    issues = []
    
    # 检查目录
    for dir_name in RELEASE_CONTENT['directories']:
        dir_path = source_dir / dir_name
        if not dir_path.exists():
            issues.append(f" 缺少目录: {dir_name}")
        elif not any(dir_path.iterdir()):
            issues.append(f" 目录为空: {dir_name}")
        else:
            file_count = sum(1 for _ in dir_path.rglob('*') if _.is_file())
            print(f" {dir_name}/ - {file_count} 个文件")
    
    # 检查根文件
    for file_name in RELEASE_CONTENT['root_files']:
        file_path = source_dir / file_name
        if not file_path.exists():
            issues.append(f" 缺少文件: {file_name}")
        else:
            print(f" {file_name}")
    
    print("-" * 50)
    
    if issues:
        print("发现问题:")
        for issue in issues:
            print(f"   {issue}")
        return False
    else:
        print(" 所有验证通过")
        return True

def main():
    source_dir = Path('.')
    
    print("=" * 60)
    print("Spinor-Taiji Model - 发布内容筛选工具")
    print("=" * 60)
    print()
    
    # 验证发布内容
    if not validate_release(source_dir):
        print("\n 验证未通过，请修复上述问题后重试")
        return
    
    print("\n 发布内容范围:")
    print("   - docs/ (核心文档库)")
    print("   - articles/ (公众号文章)")
    print("   - README.md, LICENSE, CONTRIBUTING.md")
    print()
    
    # 创建发布包
    create_release_package(source_dir)
    
    print("\n" + "=" * 60)
    print("发布准备完成！")
    print("=" * 60)

if __name__ == '__main__':
    main()
