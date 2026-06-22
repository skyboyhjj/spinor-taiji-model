# -*- coding: utf-8 -*-
import re

with open("docs/10-词汇表/旋量太极词汇表.md", "r", encoding="utf-8") as f:
    md_content = f.read()

with open("docs/10-词汇表/旋量太极词汇表_增强版.html", "r", encoding="utf-8") as f:
    html_content = f.read()

md_terms_raw = re.findall(r"\*\*([^*]+)\*\*：", md_content)
md_terms = []
for term in md_terms_raw:
    term = term.strip()
    match = re.match(r"(.+?)[（(][^）)]*[）)]", term)
    if match:
        md_terms.append(match.group(1).strip())
    else:
        md_terms.append(term)
html_terms = [t.strip() for t in re.findall(r'<div class="term-card" data-term="([^"]+)"', html_content) if t.strip()]

print("=" * 70)
print("词汇表内容核对报告")
print("=" * 70)

print("\n【文件信息】")
print(f"  MD文件词汇数量: {len(md_terms)}")
print(f"  HTML文件词汇数量: {len(html_terms)}")

print("\n【MD文件词汇列表】")
print("  " + ", ".join(sorted(md_terms)))

print("\n【HTML文件词汇列表】")
print("  " + ", ".join(sorted(html_terms)))

print("\n【MD中存在但HTML中缺失的词汇】")
missing_in_html = [t for t in md_terms if t not in html_terms]
if missing_in_html:
    print("   " + ", ".join(missing_in_html))
else:
    print("   无缺失")

print("\n【HTML中存在但MD中缺失的词汇】")
missing_in_md = [t for t in html_terms if t not in md_terms]
if missing_in_md:
    print("   " + ", ".join(missing_in_md))
else:
    print("   无新增")

print("\n【词汇定义一致性检查】")
matching_terms = [t for t in md_terms if t in html_terms]
print(f"  共同词汇数量: {len(matching_terms)}")

print("\n" + "=" * 70)
print("核对完成")
print("=" * 70)
