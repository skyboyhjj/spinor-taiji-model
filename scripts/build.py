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

    index_html = "<!DOCTYPE html><html lang='zh-CN'><head><meta charset='UTF-8'><title>旋量太极知识库</title></head><body><h1>旋量太极知识库</h1><a href='docs/'>文档</a></body></html>"
    with open(os.path.join(dist_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)
    print("创建首页")

    article_count = len([f for f in os.listdir(dist_articles) if f.endswith(".html")])
    print(f"构建完成！articles文件数: {article_count}")

if __name__ == "__main__":
    main()
