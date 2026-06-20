import os
import re

def check_naming_rules(filepath):
    """检查文件名是否违反命名规范"""
    issues = []
    filename = os.path.basename(filepath)
    
    # 规则1: 禁用空格
    if ' ' in filename:
        issues.append(('空格', f"文件名包含空格: {filename}"))
    
    # 规则2: 禁用特殊字符 (除了下划线和连字符)
    special_chars = re.findall(r'[^a-zA-Z0-9\u4e00-\u9fa5._-]', filename)
    if special_chars:
        issues.append(('特殊字符', f"包含非法字符 '{''.join(set(special_chars))}': {filename}"))
    
    # 规则3: 文件名长度控制在50字以内
    if len(filename) > 50:
        issues.append(('长度超限', f"文件名过长({len(filename)}字): {filename}"))
    
    # 规则4: 检查是否为无意义命名
    meaningless_names = ['新建文档', '新建文本文档', '未命名', 'untitled', 'document']
    name_without_ext = os.path.splitext(filename)[0].lower()
    if any(name in name_without_ext for name in meaningless_names):
        issues.append(('无意义命名', f"无意义文件名: {filename}"))
    
    # 规则5: 检查版本后缀是否规范
    version_patterns = ['_v1', '_v2', '_v3', '_公众号', '_修复', '_优化', '_校准']
    has_valid_suffix = any(pattern in filename for pattern in version_patterns)
    
    return issues

def scan_directory(root_dir):
    """扫描目录并检查所有文件"""
    violations = []
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # 跳过隐藏目录和.git目录
        dirnames[:] = [d for d in dirnames if not d.startswith('.')]
        
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            
            # 跳过特定文件
            if filename in ['README.md', 'LICENSE', 'CONTRIBUTING.md', 'requirements.txt']:
                continue
            
            issues = check_naming_rules(filepath)
            if issues:
                rel_path = os.path.relpath(filepath, root_dir)
                violations.append({
                    'path': rel_path,
                    'filename': filename,
                    'issues': issues
                })
    
    return violations

def main():
    print("=" * 70)
    print("知识库命名规范检查脚本")
    print("=" * 70)
    print("\n正在扫描项目目录...")
    
    root_dir = '.'
    violations = scan_directory(root_dir)
    
    print(f"\n扫描完成，发现 {len(violations)} 个违反命名规范的文件\n")
    
    if violations:
        print("违反规则的文件清单:")
        print("-" * 70)
        
        for i, violation in enumerate(violations, 1):
            print(f"\n{i}. 文件: {violation['path']}")
            print(f"   问题:")
            for rule, desc in violation['issues']:
                print(f"      [{rule}] {desc}")
        
        print("\n" + "=" * 70)
        print("问题分类统计:")
        print("-" * 70)
        
        category_counts = {}
        for violation in violations:
            for rule, _ in violation['issues']:
                category_counts[rule] = category_counts.get(rule, 0) + 1
        
        for category, count in sorted(category_counts.items()):
            print(f"  {category}: {count} 个文件")
        
        print("\n建议修正方案:")
        print("-" * 70)
        print("  1. 空格  使用下划线 '_'")
        print("  2. 特殊字符  删除或替换为中文/英文")
        print("  3. 过长文件名  精简至50字以内")
        print("  4. 无意义命名  使用描述性名称")
    else:
        print(" 所有文件均符合命名规范")
    
    print("\n" + "=" * 70)

if __name__ == '__main__':
    main()
