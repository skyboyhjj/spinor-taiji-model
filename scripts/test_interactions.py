# -*- coding: utf-8 -*-
import re

with open("docs/10-词汇表/旋量太极词汇表_增强版.html", "r", encoding="utf-8") as f:
    content = f.read()

print("=" * 60)
print("Interaction Test Report")
print("=" * 60)

print("\n[Test 1] Sidebar Navigation")
nav_items = re.findall(r'<li class="nav-item[^>]* data-section="([^"]+)"', content)
sections = re.findall(r'<div id="([^"]+)"', content)
print(f"  - Navigation items: {len(nav_items)}")
print(f"  - Target sections: {len(sections)}")
missing = [n for n in nav_items if n not in sections]
if not missing:
    print("  OK All navigation items have targets")
else:
    print(f"  FAIL Missing: {missing}")

print("\n[Test 2] Graph Node Click")
nodes = re.findall(r'<circle[^>]*data-target="([^"]+)"', content)
cards = re.findall(r'<div class="term-card" data-term="([^"]+)"', content)
print(f"  - Clickable nodes: {len(nodes)}")
print(f"  - Term cards: {len(cards)}")
missing = [n for n in nodes if n not in cards]
if not missing:
    print("  OK All nodes have matching cards")
else:
    print(f"  FAIL Missing: {missing}")

print("\n[Test 3] Hover Effects Removed")
hover_patterns = [(".nav-item:hover", "nav items"), (".term-card:hover", "term cards"), (".clickable-node:hover", "graph nodes"), ("mouseenter", "mouseenter events"), ("mouseleave", "mouseleave events")]
for pattern, desc in hover_patterns:
    if pattern in content:
        print(f"  FAIL {desc} hover effect still exists")
    else:
        print(f"  OK {desc} hover effect removed")

print("\n[Test 4] Other Features")
features = [("id=\"backToTop\"", "Back to top button"), ("scrollTo({ top: 0", "Back to top function"), ("id=\"searchInput\"", "Search input"), ("scrollIntoView({ behavior: \"smooth\"", "Smooth scroll")]
for pattern, desc in features:
    if re.search(pattern, content):
        print(f"  OK {desc}")
    else:
        print(f"  FAIL {desc}")

print("\n" + "=" * 60)
print("Tests completed")
print("=" * 60)
