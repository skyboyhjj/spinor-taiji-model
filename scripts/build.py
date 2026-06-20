import os
import shutil

def main():
    project_root = os.getcwd()
    articles_src = os.path.join(project_root, "articles")
    docs_src = os.path.join(project_root, "docs")
    dist_dir = os.path.join(project_root, "dist")
    dist_articles = os.path.join(dist_dir, "articles")
    dist_docs = os.path.join(dist_dir, "docs")

    if not os.path.exists(dist_dir):
        os.makedirs(dist_dir)

    if os.path.exists(dist_articles):
        shutil.rmtree(dist_articles)
    shutil.copytree(articles_src, dist_articles)
    print("复制 articles 目录")

    if os.path.exists(dist_docs):
        shutil.rmtree(dist_docs)
    shutil.copytree(docs_src, dist_docs)
    print("复制 docs 目录")

    # 中文主文件 -> 英文别名映射（使用实际文件名）
    alias_map = {
        '"伦理即道体"理念落地指南_公众号版.html': 'lunli-ji-daoti.html',
        '伦理即道体系列_阅读地图与实修指南_修复版_公众号版.html': 'lunli-reading-map.html',
        '道德经无死地_旋量太极读解_公众号版_with_new_images.html': 'daodejing-wusidi.html',
        '道德经第一章_旋量-太极读解_微信公众号专业版_公众号版.html': 'daodejing-chapter-1.html',
        '道德经里的思维智慧_为什么"为道日损"_排版版_公众号版.html': 'daodejing-dao-sun.html',
        '"旋量-太极"模型中_"看山三境界"_公众号版_6月4日模板.html': 'spinor-taiji-three-realms.html',
        '看山三境界_核心数据表格_公众号版.html': 'three-realms-data.html',
        '心经的振动科学与觉知智慧_一句一句的现代读解_公众号版.html': 'heart-sutra-vibration.html',
        '色即是空_空即是色_认知与实践的升级_公众号版.html': 'form-is-emptiness.html',
        '从"认识道"到"成为道"_一场认知与实践的升级_大众版_公众号版.html': 'from-knowing-to-being.html',
        '旋量太极模型写高考作文_两篇对比版_公众号版_修复后.html': 'gaokao-essay-spinor.html',
        '胃病切片_学术排版版_公众号版.html': 'stomach-disease-slice.html',
        '长期胃病_公众号版_ima.html': 'chronic-gastritis.html',
        '微信公众号响应式表格演示_公众号版.html': 'responsive-table-demo.html',
    }

    # 将中文主文件内容复制到英文别名文件
    for chinese_file, alias_file in alias_map.items():
        chinese_path = os.path.join(dist_articles, chinese_file)
        alias_path = os.path.join(dist_articles, alias_file)
        if os.path.exists(chinese_path):
            shutil.copy2(chinese_path, alias_path)
            print(f"复制内容: {chinese_file} -> {alias_file}")

    index_html = "<!DOCTYPE html><html lang='zh-CN'><head><meta charset='UTF-8'><title>旋量太极知识库</title></head><body><h1>旋量太极知识库</h1><a href='docs/'>文档</a></body></html>"
    with open(os.path.join(dist_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)
    print("创建首页")

    # 生成 _redirects 文件
    redirects_content = """# Cloudflare Pages 重定向规则
# 中文主文件 -> 英文别名（用于SEO优化）

# 伦理即道体系列
/articles/伦理即道体理念落地指南_公众号版.html /articles/lunli-ji-daoti.html 301
/articles/伦理即道体系列_阅读地图与实修指南_修复版_公众号版.html /articles/lunli-reading-map.html 301

# 道德经系列
/articles/道德经无死地_旋量太极读解_公众号版_with_new_images.html /articles/daodejing-wusidi.html 301
/articles/道德经第一章_旋量-太极读解_微信公众号专业版_公众号版.html /articles/daodejing-chapter-1.html 301
/articles/道德经里的思维智慧_为什么为道日损_排版版_公众号版.html /articles/daodejing-dao-sun.html 301

# 旋量太极系列
/articles/旋量-太极模型中_看山三境界_公众号版_6月4日模板.html /articles/spinor-taiji-three-realms.html 301
/articles/看山三境界_核心数据表格_公众号版.html /articles/three-realms-data.html 301

# 心经
/articles/心经的振动科学与觉知智慧_一句一句的现代读解_公众号版.html /articles/heart-sutra-vibration.html 301

# 色即是空
/articles/色即是空_空即是色_认知与实践的升级_公众号版.html /articles/form-is-emptiness.html 301

# 认知升级
/articles/从认识道到成为道_一场认知与实践的升级_大众版_公众号版.html /articles/from-knowing-to-being.html 301

# 高考作文
/articles/旋量太极模型写高考作文_两篇对比版_公众号版_修复后.html /articles/gaokao-essay-spinor.html 301

# 胃病调理
/articles/胃病切片_学术排版版_公众号版.html /articles/stomach-disease-slice.html 301
/articles/长期胃病_公众号版_ima.html /articles/chronic-gastritis.html 301

# 技术演示
/articles/微信公众号响应式表格演示_公众号版.html /articles/responsive-table-demo.html 301

# 首页重定向
/docs/ / 301
"""
    with open(os.path.join(dist_dir, "_redirects"), "w", encoding="utf-8") as f:
        f.write(redirects_content)
    print("创建 _redirects 文件")

    article_count = len([f for f in os.listdir(dist_articles) if f.endswith(".html")])
    print(f"构建完成！articles文件数: {article_count}")

if __name__ == "__main__":
    main()
