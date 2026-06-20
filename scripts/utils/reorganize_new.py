#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
目录重新编排脚本，按知识体系重组文件

VERSION: v1.0.0
CREATED: 2026-06-20
STATUS: 历史迁移脚本，已完成任务
LOCATION: scripts/utils/reorganize_new.py

注意：此脚本为历史迁移工具，已完成其使命。
如需执行类似操作，请确认当前目录结构是否仍适用。
"""

import os
import shutil
from pathlib import Path

# 仓库根目录
REPO_ROOT = Path(r'E:\Trac Project\spinor-taiji-model')

# 新目录结构定义
NEW_STRUCTURE = {
    '00-产品宪法': {
        'description': '慧惠项目核心文档、规范说明及项目背景资料',
        'keywords': ['慧惠', '产品宪法', '最高产品宪法', 'AI伦理', '伦理即道体']
    },
    '01-核心模型': {
        'description': '基础理论内容，读者入门的首要阅读区域',
        'keywords': ['旋量-太极', '道境', '坐标系', '模型', '框架', '呼吸', '振动']
    },
    '02-经典读解': {
        'description': '《道德经》各章节的旋量-太极读解内容',
        'keywords': ['道德经', '第一章', '第二十七章', '第五十八章', '第七十九章']
    },
    '03-应用实践': {
        'description': '跨领域应用案例与实践方法',
        'keywords': ['胃病', '心理创伤', '高考作文', '康复', '案例', '实践']
    },
    '04-阅读指南': {
        'description': '系列入口说明、阅读路径地图及实修练习指导',
        'keywords': ['阅读地图', '实修指南', '导读', '系列', '练习', '冥想']
    },
    '05-五步读解法': {
        'description': '系统阐述解经方法论的完整流程、步骤及应用技巧',
        'keywords': ['五步', '方法论', '读解法', '操作手册', '流程']
    },
}

def determine_target_dir(filepath):
    """根据文件内容确定目标目录"""
    filepath_str = str(filepath)
    filename = filepath.name
    
    # 优先级排序：更具体的关键词优先匹配
    
    # 1. 慧惠/产品宪法
    if any(kw in filepath_str for kw in ['慧惠', '产品宪法', '最高产品宪法', 'HuiHui', 'huihui']):
        return '00-产品宪法'
    
    # 2. 五步读解法/方法论
    if any(kw in filepath_str for kw in ['五步', '方法论', '读解法', '操作手册', '核心架构']):
        return '05-五步读解法'
    
    # 3. 阅读指南/实修
    if any(kw in filepath_str for kw in ['阅读地图', '实修', '导读', '练习', '冥想', '系列']):
        return '04-阅读指南'
    
    # 4. 道德经经典读解
    if any(kw in filepath_str for kw in ['道德经', '第一章', '第二十七章', '第五十八章', '第七十九章', '第三十七章', '第四十二章']):
        return '02-经典读解'
    
    # 5. 应用实践
    if any(kw in filepath_str for kw in ['胃病', '心理创伤', '高考作文', '康复', '案例', '心经']):
        return '03-应用实践'
    
    # 6. 核心模型（基础理论）
    if any(kw in filepath_str for kw in ['旋量-太极', '道境', '坐标系', '呼吸', '振动', '当下', '时空', '明朝', '文化自信']):
        return '01-核心模型'
    
    # 默认放到核心模型
    return '01-核心模型'

def reorganize_files():
    """重新组织文件"""
    print("=" * 70)
    print("项目目录重新编排")
    print("=" * 70)
    print()
    
    # 创建新目录
    for dirname, info in NEW_STRUCTURE.items():
        target_dir = REPO_ROOT / dirname
        target_dir.mkdir(parents=True, exist_ok=True)
        print(f"✅ 创建目录: {dirname}/")
        print(f"   说明: {info['description']}")
    print()
    
    # 统计
    stats = {name: 0 for name in NEW_STRUCTURE.keys()}
    
    # 遍历 docs/ 目录
    docs_dir = REPO_ROOT / 'docs'
    
    # 收集所有Markdown文件
    md_files = list(docs_dir.rglob('*.md')) if docs_dir.exists() else []
    
    # 遍历其他目录
    for subdir in ['articles', 'scripts', 'media', 'data', 'templates']:
        dir_path = REPO_ROOT / subdir
        if dir_path.exists():
            md_files.extend(dir_path.rglob('*.md'))
            md_files.extend(dir_path.rglob('*.html'))
    
    # 处理每个文件
    for filepath in md_files:
        if not filepath.is_file():
            continue
        
        # 确定目标目录
        target_dirname = determine_target_dir(filepath)
        target_dir = REPO_ROOT / target_dirname
        
        # 保持子目录结构
        # 提取子目录名称（如果有）
        try:
            rel_path = filepath.relative_to(docs_dir) if filepath.is_relative_to(docs_dir) else filepath
        except:
            rel_path = filepath
        
        if isinstance(rel_path, Path):
            parts = rel_path.parts
            if len(parts) > 1:
                # 保留第一个子目录
                target_subdir = parts[0]
                target_path = target_dir / target_subdir / filepath.name
            else:
                target_path = target_dir / filepath.name
        else:
            target_path = target_dir / filepath.name
        
        # 创建目标目录
        target_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 移动文件
        try:
            # 如果目标文件已存在，添加后缀
            if target_path.exists():
                target_path = target_path.parent / f"{target_path.stem}_copy{target_path.suffix}"
            
            shutil.move(str(filepath), str(target_path))
            stats[target_dirname] += 1
            print(f"  ✅ [{target_dirname}] {filepath.name}")
        except Exception as e:
            print(f"  ❌ 移动失败: {filepath.name} - {e}")
    
    # 输出统计
    print()
    print("=" * 70)
    print("重新编排完成统计")
    print("=" * 70)
    for name, count in stats.items():
        print(f"  {name}/ : {count} 个文件")
    print("=" * 70)
    
    return stats

def create_reading_guide():
    """创建阅读指南文档"""
    guide_content = """# Spinor-Taiji Model 阅读指南

## 项目简介

Spinor-Taiji Model（旋量-太极模型）是一个将现代量子物理与东方古典哲学进行深度互参的理论框架，旨在为《道德经》等经典提供现代化的解读方式。

## 目录结构

```
spinor-taiji-model/
├── 00-产品宪法/      # 慧惠项目核心文档
├── 01-核心模型/      # 基础理论（入门首选）
├── 02-经典读解/      # 《道德经》各章节解读
├── 03-应用实践/      # 跨领域应用案例
├── 04-阅读指南/      # 阅读路径与实修指导
├── 05-五步读解法/    # 解经方法论
├── scripts/          # 代码工具
├── media/           # 媒体资源
└── README.md        # 项目说明
```

## 推荐阅读顺序

### 入门路径（推荐）

```
1. 【01-核心模型】
   ↓
2. 【05-五步读解法】
   ↓
3. 【02-经典读解】
   ↓
4. 【04-阅读指南】
   ↓
5. 【03-应用实践】
```

### 快速入口

| 需求 | 推荐目录 |
|------|----------|
| 了解项目背景 | 00-产品宪法 |
| 理解核心理论 | 01-核心模型 |
| 深入经典解读 | 02-经典读解 |
| 寻找实践方法 | 03-应用实践 |
| 规划学习路径 | 04-阅读指南 |
| 掌握解读方法 | 05-五步读解法 |

## 各目录说明

### 00-产品宪法
慧惠项目的核心规范文档，包括产品宪法、AI伦理准则等。

### 01-核心模型
基础理论内容，包括：
- 旋量-太极模型基础
- 道境坐标系
- 呼吸与振动理论
- 量子物理解读

**推荐起点**：从这里开始您的学习之旅。

### 02-经典读解
《道德经》各章节的旋量-太极读解，包括：
- 第一章：道的显化
- 第二十七章：善行无辙迹
- 第五十八章：祸福相倚
- 第七十九章：执左契而不责

### 03-应用实践
将理论应用于实际问题的案例：
- 胃病调理
- 心理创伤修复
- 高考作文指导
- 日常生活实践

### 04-阅读指南
辅助学习材料：
- 系列阅读地图
- 实修练习指导
- 常见问题解答

### 05-五步读解法
解经方法论的完整体系：
- 五步读解流程
- 实际操作技巧
- 方法论案例

## 参与贡献

欢迎对项目内容进行补充和完善，请参阅 CONTRIBUTING.md 了解贡献指南。

## 许可证

本项目采用 CC BY-NC-SA 4.0 许可证。

---
*最后更新：2026-06-20*
"""
    
    guide_path = REPO_ROOT / 'README.md'
    with open(guide_path, 'w', encoding='utf-8') as f:
        f.write(guide_content)
    
    print(f"\n✅ 更新项目说明文档: README.md")

def main():
    # 重新组织文件
    stats = reorganize_files()
    
    # 更新阅读指南
    create_reading_guide()
    
    print("\n下一步操作:")
    print("1. cd 'E:\\Trac Project\\spinor-taiji-model'")
    print("2. git add .")
    print("3. git commit -m 'Reorganize: new directory structure by reading path'")
    print("4. git push origin master")

if __name__ == '__main__':
    main()