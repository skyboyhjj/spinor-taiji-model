import os
import shutil

articles_dir = "articles"
en_dir = os.path.join(articles_dir, "en")
zh_dir = os.path.join(articles_dir, "zh")

file_mapping = {
    "chronic-gastritis.html": "chronic-gastritis",
    "daodejing-chapter-1.html": "daodejing-chapter-1",
    "daodejing-dao-sun.html": "daodejing-dao-sun",
    "daodejing-wusidi.html": "daodejing-wusidi",
    "form-is-emptiness.html": "form-is-emptiness",
    "from-knowing-to-being.html": "from-knowing-to-being",
    "gaokao-essay-spinor.html": "gaokao-essay-spinor",
    "heart-sutra-vibration.html": "heart-sutra-vibration",
    "lunli-ji-daoti.html": "lunli-ji-daoti",
    "lunli-reading-map.html": "lunli-reading-map",
    "responsive-table-demo.html": "responsive-table-demo",
    "spinor-taiji-glossary.html": "spinor-taiji-glossary",
    "spinor-taiji-model-declaration.html": "spinor-taiji-model-declaration",
    "spinor-taiji-three-realms.html": "spinor-taiji-three-realms",
    "stomach-disease-slice.html": "stomach-disease-slice",
    "three-realms-data.html": "three-realms-data",
    "从认识道到成为道_一场认知与实践的升级_大众版_公众号版.html": "from-knowing-to-being",
    "伦理即道体理念落地指南_公众号版.html": "lunli-ji-daoti",
    "伦理即道体系列_阅读地图与实修指南_修复版_公众号版.html": "lunli-reading-map",
    "微信公众号响应式表格演示_公众号版.html": "responsive-table-demo",
    "旋量太极词汇表_增强版.html": "spinor-taiji-glossary",
    "旋量-太极模型声明_微信公众号版.html": "spinor-taiji-model-statement",
}

chinese_files = [
    "从认识道到成为道_一场认知与实践的升级_大众版_公众号版.html",
    "伦理即道体理念落地指南_公众号版.html",
    "伦理即道体系列_阅读地图与实修指南_修复版_公众号版.html",
    "微信公众号响应式表格演示_公众号版.html",
    "旋量太极词汇表_增强版.html",
    "旋量-太极模型声明_微信公众号版.html",
]

def is_chinese_char(c):
    return '\u4e00' <= c <= '\u9fff'

def contains_chinese(filename):
    for c in filename:
        if is_chinese_char(c):
            return True
    return False

for filename in os.listdir(articles_dir):
    filepath = os.path.join(articles_dir, filename)
    
    if not os.path.isfile(filepath):
        continue
    
    if filename.endswith(".html"):
        if contains_chinese(filename):
            target_slug = file_mapping.get(filename, filename.replace(".html", ""))
            target_path = os.path.join(zh_dir, f"{target_slug}.html")
            print(f"移动中文文件: {filename} -> zh/{target_slug}.html")
            shutil.move(filepath, target_path)
        else:
            target_slug = file_mapping.get(filename, filename.replace(".html", ""))
            target_path = os.path.join(en_dir, f"{target_slug}.html")
            print(f"移动英文文件: {filename} -> en/{target_slug}.html")
            shutil.move(filepath, target_path)

print("\n文件迁移完成！")

print("\n--- zh 目录内容 ---")
for f in sorted(os.listdir(zh_dir)):
    print(f"  {f}")

print("\n--- en 目录内容 ---")
for f in sorted(os.listdir(en_dir)):
    print(f"  {f}")