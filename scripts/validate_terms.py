import os
import re
import sys

def load_vocabulary(filepath):
    """加载词汇表文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def parse_vocabulary(content):
    """解析词汇表，提取词条信息"""
    entries = []
    sections = re.split(r'^##\s+(.+)', content, flags=re.MULTILINE)
    
    current_section = ""
    for i in range(len(sections)):
        if i % 2 == 0:
            continue
        current_section = sections[i].strip()
        section_content = sections[i+1] if i+1 < len(sections) else ""
        
        # 提取所有词条定义
        pattern = r'\*\*([^*]+)\*\*\s*：([^\n]+)'
        matches = re.findall(pattern, section_content)
        for match in matches:
            term = match[0].strip()
            definition = match[1].strip()
            entries.append({
                'term': term,
                'definition': definition,
                'section': current_section
            })
    
    return entries

def check_duplicate_terms(entries):
    """检查重复词汇"""
    term_counts = {}
    duplicates = []
    
    for entry in entries:
        term = entry['term']
        term_counts[term] = term_counts.get(term, 0) + 1
    
    for term, count in term_counts.items():
        if count > 1:
            duplicates.append((term, count))
    
    return duplicates

def check_definition_length(entries, max_length=50):
    """检查定义长度是否符合要求"""
    too_long = []
    for entry in entries:
        if len(entry['definition']) > max_length:
            too_long.append((entry['term'], len(entry['definition'])))
    return too_long

def check_cross_references(vocab_entries, docs_dir):
    """检查跨文档引用一致性"""
    terms = {entry['term'] for entry in vocab_entries}
    issues = []
    
    for root, dirs, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # 检查非标准术语使用
                    potential_terms = re.findall(r'[\u4e00-\u9fa5]{2,}', content)
                    for term in potential_terms:
                        if term in ['的', '是', '在', '有', '和', '与', '了', '我', '你', '他', '她', '它']:
                            continue
                        if len(term) >= 2 and term not in terms:
                            # 检查是否可能是词汇表中的术语变体
                            found_variant = False
                            for vocab_term in terms:
                                if term in vocab_term or vocab_term in term:
                                    found_variant = True
                                    break
                            if not found_variant and len(term) >= 3:
                                issues.append((filepath, term))
                except Exception as e:
                    print(f"Error reading {filepath}: {e}")
    
    return issues

def check_status_tags(entries):
    """检查状态标签是否正确"""
    valid_tags = ['', '', '']
    missing_tags = []
    for entry in entries:
        has_tag = any(tag in entry['definition'] for tag in valid_tags)
        if not has_tag:
            missing_tags.append(entry['term'])
    return missing_tags

def main():
    vocab_path = r'docs/10-词汇表/旋量太极词汇表.md'
    docs_dir = r'docs'
    
    print("=" * 60)
    print("词汇一致性校验脚本")
    print("=" * 60)
    
    # 加载词汇表
    if not os.path.exists(vocab_path):
        print(f"错误：词汇表文件不存在: {vocab_path}")
        return
    
    content = load_vocabulary(vocab_path)
    entries = parse_vocabulary(content)
    
    print(f"\n1. 词汇表概况")
    print(f"   - 词条总数: {len(entries)}")
    
    # 检查重复词汇
    duplicates = check_duplicate_terms(entries)
    if duplicates:
        print(f"\n2. 重复词汇检查 ")
        for term, count in duplicates:
            print(f"   - 「{term}」重复出现 {count} 次")
    else:
        print(f"\n2. 重复词汇检查 ")
        print(f"   - 未发现重复词汇")
    
    # 检查定义长度
    too_long = check_definition_length(entries)
    if too_long:
        print(f"\n3. 定义长度检查 ")
        for term, length in too_long:
            print(f"   - 「{term}」定义过长 ({length}字)")
    else:
        print(f"\n3. 定义长度检查 ")
        print(f"   - 所有定义长度符合要求")
    
    # 检查状态标签
    missing_tags = check_status_tags(entries)
    if missing_tags:
        print(f"\n4. 状态标签检查 ")
        for term in missing_tags[:5]:  # 只显示前5个
            print(f"   - 「{term}」缺少状态标签")
        if len(missing_tags) > 5:
            print(f"   - ... 还有 {len(missing_tags) - 5} 个词条缺少标签")
    else:
        print(f"\n4. 状态标签检查 ")
        print(f"   - 所有词条均有状态标签")
    
    # 检查跨文档引用
    print(f"\n5. 跨文档引用检查")
    print(f"   - 正在扫描文档...")
    issues = check_cross_references(entries, docs_dir)
    if issues:
        print(f"    发现潜在非标准术语:")
        for filepath, term in issues[:10]:  # 只显示前10个
            rel_path = os.path.relpath(filepath)
            print(f"     - {rel_path}: 「{term}」")
        if len(issues) > 10:
            print(f"     - ... 还有 {len(issues) - 10} 个潜在问题")
    else:
        print(f"    未发现明显的非标准术语引用")
    
    # 按分类统计
    print(f"\n6. 分类统计")
    section_counts = {}
    for entry in entries:
        section = entry['section']
        section_counts[section] = section_counts.get(section, 0) + 1
    
    for section, count in sorted(section_counts.items()):
        print(f"   - {section}: {count} 个词条")
    
    print("\n" + "=" * 60)
    print("校验完成")
    print("=" * 60)

if __name__ == '__main__':
    main()
