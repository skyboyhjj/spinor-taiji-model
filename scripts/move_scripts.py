import os
import shutil
from pathlib import Path

REPO_ROOT = Path('.')

# 要处理的脚本文件
scripts = [
    {
        'name': 'organize_repo.py',
        'version': 'v1.0.0',
        'purpose': '目录结构整理脚本，按文件类型分类移动文件',
        'created': '2026-06-20',
        'status': '历史迁移脚本，已完成任务'
    },
    {
        'name': 'reorganize_new.py', 
        'version': 'v1.0.0',
        'purpose': '目录重新编排脚本，按知识体系重组文件',
        'created': '2026-06-20',
        'status': '历史迁移脚本，已完成任务'
    }
]

# 版本标记模板
VERSION_TEMPLATE = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
{purpose}

VERSION: {version}
CREATED: {created}
STATUS: {status}
LOCATION: scripts/utils/{name}

注意：此脚本为历史迁移工具，已完成其使命。
如需执行类似操作，请确认当前目录结构是否仍适用。
"""

'''

def process_script(script_info):
    """处理单个脚本文件"""
    src_path = REPO_ROOT / script_info['name']
    
    if not src_path.exists():
        print(f" 文件不存在: {script_info['name']}")
        return False
    
    # 读取原文件内容
    with open(src_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 移除原有的shebang和编码声明
    lines = content.split('\n')
    while lines and (lines[0].startswith('#!/') or lines[0].startswith('# -*-')):
        lines.pop(0)
    
    # 移除原有的docstring
    if lines and lines[0].startswith('"""'):
        end_idx = None
        for i, line in enumerate(lines):
            if line.endswith('"""') and i > 0:
                end_idx = i
                break
        if end_idx:
            lines = lines[end_idx + 1:]
    
    # 添加版本标记
    version_comment = VERSION_TEMPLATE.format(**script_info)
    new_content = version_comment + '\n'.join(lines).strip()
    
    # 创建目标目录
    target_dir = REPO_ROOT / 'scripts' / 'utils'
    target_dir.mkdir(parents=True, exist_ok=True)
    
    # 写入新文件
    target_path = target_dir / script_info['name']
    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    # 删除原文件
    src_path.unlink()
    
    print(f" 已移动并更新: {script_info['name']}")
    print(f"   -> scripts/utils/{script_info['name']}")
    print(f"   版本: {script_info['version']}")
    return True

def main():
    print("=" * 60)
    print("脚本文件迁移与版本标记")
    print("=" * 60)
    print()
    
    success_count = 0
    for script in scripts:
        if process_script(script):
            success_count += 1
    
    print()
    print("=" * 60)
    print(f"完成: {success_count}/{len(scripts)} 个脚本")
    print("=" * 60)

if __name__ == '__main__':
    main()
