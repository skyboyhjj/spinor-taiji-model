import os
import shutil

def normalize_filenames(directory=None):
    if directory is None:
        articles_dir = os.path.join(os.getcwd(), "articles")
    else:
        articles_dir = directory
    
    if not os.path.exists(articles_dir):
        print(f"错误：目录不存在: {articles_dir}")
        return []
    
    renamed_files = []
    
    for filename in os.listdir(articles_dir):
        if not filename.endswith(".html"):
            continue
        
        old_path = os.path.join(articles_dir, filename)
        
        new_filename = filename
        new_filename = new_filename.replace("\u201c", "").replace("\u201d", "")
        new_filename = new_filename.replace("《", "").replace("》", "")
        new_filename = new_filename.replace("“", "").replace("”", "")
        new_filename = new_filename.replace("\"", "")
        
        new_path = os.path.join(articles_dir, new_filename)
        
        if old_path != new_path:
            shutil.move(old_path, new_path)
            renamed_files.append(f"{filename} -> {new_filename}")
            print(f"重命名: {filename} -> {new_filename}")
    
    print(f"\n重命名完成！共处理 {len(renamed_files)} 个文件")
    return renamed_files

if __name__ == "__main__":
    normalize_filenames()