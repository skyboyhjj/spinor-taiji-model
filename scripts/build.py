import os
import shutil
import json
import time
import hashlib
from pathlib import Path

class BuildLogger:
    def __init__(self):
        self.start_time = time.time()
        self.entries = []
    
    def log(self, message, level='INFO'):
        timestamp = time.strftime('%H:%M:%S')
        self.entries.append((timestamp, level, message))
        prefix = {
            'INFO': '[INFO]',
            'WARN': '[WARN]',
            'ERROR': '[ERROR]',
            'SUCCESS': '[SUCCESS]'
        }.get(level, '[INFO]')
        print(f"{timestamp} {prefix} {message}")
    
    def info(self, message):
        self.log(message, 'INFO')
    
    def warn(self, message):
        self.log(message, 'WARN')
    
    def error(self, message):
        self.log(message, 'ERROR')
    
    def success(self, message):
        self.log(message, 'SUCCESS')
    
    def elapsed(self):
        return round(time.time() - self.start_time, 2)

def validate_json_file(filepath):
    """验证JSON文件格式是否正确"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return True, data
    except json.JSONDecodeError as e:
        return False, f"JSON格式错误: {e}"
    except FileNotFoundError:
        return False, "文件不存在"
    except Exception as e:
        return False, f"未知错误: {str(e)}"

def compute_file_hash(filepath):
    """计算文件SHA256哈希值"""
    sha256_hash = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()

def copy_if_modified(src, dst):
    """仅当源文件修改时才复制"""
    if not os.path.exists(src):
        return False, "源文件不存在"
    
    if os.path.exists(dst):
        src_hash = compute_file_hash(src)
        dst_hash = compute_file_hash(dst)
        if src_hash == dst_hash:
            return False, "文件未修改，跳过"
    
    try:
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
        return True, "文件已复制"
    except Exception as e:
        return False, f"复制失败: {str(e)}"

def copy_directory_with_check(src, dst, logger):
    """复制目录，跳过未修改的文件，删除已不存在的文件"""
    if not os.path.exists(src):
        logger.warn(f"源目录不存在: {src}")
        return False
    
    os.makedirs(dst, exist_ok=True)
    
    copied_count = 0
    skipped_count = 0
    deleted_count = 0
    error_count = 0
    
    src_files = set()
    for root, dirs, files in os.walk(src):
        rel_path = os.path.relpath(root, src)
        dst_root = os.path.join(dst, rel_path)
        os.makedirs(dst_root, exist_ok=True)
        
        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(dst_root, file)
            src_files.add(dst_file.replace('\\', '/'))
            
            success, msg = copy_if_modified(src_file, dst_file)
            if success:
                copied_count += 1
            elif "跳过" in msg:
                skipped_count += 1
            else:
                logger.error(f"复制失败 {src_file}: {msg}")
                error_count += 1
    
    for root, dirs, files in os.walk(dst):
        for file in files:
            dst_file = os.path.join(root, file)
            dst_file_normalized = dst_file.replace('\\', '/')
            
            if dst_file_normalized not in src_files:
                try:
                    os.remove(dst_file)
                    deleted_count += 1
                    logger.info(f"删除已不存在的文件: {dst_file}")
                except Exception as e:
                    logger.error(f"删除文件失败 {dst_file}: {str(e)}")
                    error_count += 1
    
    logger.info(f"复制完成: {copied_count} 复制, {skipped_count} 跳过, {deleted_count} 删除, {error_count} 错误")
    return error_count == 0

def main():
    logger = BuildLogger()
    logger.info("=" * 60)
    logger.info("旋量-太极模型 构建系统 v2.0")
    logger.info("=" * 60)
    
    project_root = os.getcwd()
    logger.info(f"项目根目录: {project_root}")
    
    # 定义路径
    paths = {
        'articles_src': os.path.join(project_root, "articles"),
        'docs_src': os.path.join(project_root, "docs"),
        'assets_src': os.path.join(project_root, "assets"),
        'functions_src': os.path.join(project_root, "functions"),
        'dist_dir': os.path.join(project_root, "dist"),
        'config_aliases': os.path.join(project_root, "config", "article_aliases.json"),
        'config_headers': os.path.join(project_root, "config", "headers_config.json")
    }
    
    # 验证配置文件
    logger.info("")
    logger.info("【阶段1】配置文件验证")
    
    valid, data = validate_json_file(paths['config_aliases'])
    if not valid:
        logger.error(f"配置文件验证失败: {paths['config_aliases']}")
        logger.error(f"错误信息: {data}")
        return 1
    
    config = data
    logger.success(f"配置文件验证通过: article_aliases.json")
    logger.info(f"配置版本: {config.get('version', '1.0')}")
    
    if os.path.exists(paths['config_headers']):
        valid, data = validate_json_file(paths['config_headers'])
        if not valid:
            logger.error(f"配置文件验证失败: {paths['config_headers']}")
            logger.error(f"错误信息: {data}")
            return 1
        logger.success(f"配置文件验证通过: headers_config.json")
    else:
        logger.warn("headers_config.json 不存在，将跳过")
    
    # 创建dist目录
    logger.info("")
    logger.info("【阶段2】目录准备")
    
    if not os.path.exists(paths['dist_dir']):
        os.makedirs(paths['dist_dir'])
        logger.info(f"创建dist目录: {paths['dist_dir']}")
    else:
        logger.info(f"dist目录已存在")
    
    # 复制目录（增量构建）
    logger.info("")
    logger.info("【阶段3】文件复制（增量模式）")
    
    directories_to_copy = [
        ('articles', paths['articles_src'], os.path.join(paths['dist_dir'], 'articles')),
        ('docs', paths['docs_src'], os.path.join(paths['dist_dir'], 'docs')),
        ('assets', paths['assets_src'], os.path.join(paths['dist_dir'], 'assets')),
        ('functions', paths['functions_src'], os.path.join(paths['dist_dir'], 'functions'))
    ]
    
    for name, src, dst in directories_to_copy:
        logger.info(f"复制 {name} 目录...")
        start = time.time()
        success = copy_directory_with_check(src, dst, logger)
        elapsed = round(time.time() - start, 2)
        if success:
            logger.success(f"{name} 目录复制完成 ({elapsed}s)")
        else:
            logger.error(f"{name} 目录复制失败")
    
    # 处理别名
    logger.info("")
    logger.info("【阶段4】别名处理")
    
    alias_map = config.get("aliases", {})
    dist_zh = os.path.join(paths['dist_dir'], 'articles', 'zh')
    
    if alias_map:
        for chinese_file, alias_file in alias_map.items():
            chinese_path = os.path.join(dist_zh, chinese_file)
            alias_path = os.path.join(dist_zh, alias_file)
            
            if os.path.exists(chinese_path):
                shutil.copy2(chinese_path, alias_path)
                logger.info(f"创建别名: {chinese_file} -> {alias_file}")
            else:
                logger.warn(f"源文件不存在，跳过别名: {chinese_file}")
    else:
        logger.info("无别名配置")
    
    # 生成首页
    logger.info("")
    logger.info("【阶段5】首页生成")
    
    index_html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>旋量太极知识库 | Spinor-Taiji Knowledge Base</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; line-height: 1.6; color: #333; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        header { background: rgba(255,255,255,0.95); backdrop-filter: blur(10px); border-radius: 16px; padding: 20px 30px; margin-bottom: 30px; box-shadow: 0 10px 40px rgba(0,0,0,0.1); }
        .header-top { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px; }
        .logo { font-size: 24px; font-weight: bold; color: #333; }
        .logo-en { font-size: 14px; font-weight: normal; color: #666; margin-left: 10px; }
        .lang-switcher { display: flex; gap: 10px; }
        .lang-btn { padding: 8px 20px; border: 2px solid #667eea; border-radius: 25px; background: transparent; cursor: pointer; transition: all 0.3s; font-size: 14px; }
        .lang-btn:hover { background: #667eea; color: white; }
        .lang-btn.active { background: #667eea; color: white; }
        .main-content { display: grid; gap: 30px; }
        .card { background: rgba(255,255,255,0.95); backdrop-filter: blur(10px); border-radius: 16px; padding: 30px; box-shadow: 0 10px 40px rgba(0,0,0,0.1); }
        .card-title { font-size: 20px; font-weight: bold; color: #333; margin-bottom: 20px; padding-bottom: 15px; border-bottom: 2px solid #eee; }
        .card-title-en { font-size: 14px; font-weight: normal; color: #666; margin-left: 10px; }
        .btn { display: inline-block; padding: 12px 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-decoration: none; border-radius: 25px; font-weight: 600; transition: transform 0.3s, box-shadow 0.3s; }
        .btn:hover { transform: translateY(-2px); box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4); }
        .btn-outline { background: transparent; border: 2px solid #667eea; color: #667eea; }
        .btn-outline:hover { background: #667eea; color: white; }
        .glossary-preview { margin-top: 20px; }
        .glossary-item { padding: 15px; border-left: 4px solid #667eea; margin-bottom: 10px; background: #f8f9fa; border-radius: 0 8px 8px 0; }
        .glossary-term { font-weight: bold; color: #333; }
        .glossary-def { color: #666; margin-top: 5px; }
        .declaration-preview { margin-top: 20px; }
        .declaration-text { color: #555; line-height: 1.8; }
        .declaration-tag { display: inline-block; padding: 5px 15px; background: #e8f5e9; color: #2e7d32; border-radius: 20px; font-size: 12px; margin-right: 10px; margin-bottom: 10px; }
        footer { text-align: center; color: rgba(255,255,255,0.8); margin-top: 50px; padding: 20px; }
    </style>
    <script>
        function setLanguage(lang) {
            document.documentElement.lang = lang;
            document.querySelectorAll('.lang-btn').forEach(btn => btn.classList.remove('active'));
            document.querySelector(`[data-lang="${lang}"]`).classList.add('active');
            
            const contentZh = document.querySelectorAll('.content-zh');
            const contentEn = document.querySelectorAll('.content-en');
            
            if (lang === 'zh-CN') {
                contentZh.forEach(el => el.style.display = 'block');
                contentEn.forEach(el => el.style.display = 'none');
            } else {
                contentZh.forEach(el => el.style.display = 'none');
                contentEn.forEach(el => el.style.display = 'block');
            }
            
            localStorage.setItem('preferredLanguage', lang);
        }
        
        document.addEventListener('DOMContentLoaded', () => {
            const savedLang = localStorage.getItem('preferredLanguage') || 'zh-CN';
            setLanguage(savedLang);
        });
    </script>
</head>
<body>
    <div class="container">
        <header>
            <div class="header-top">
                <div>
                    <span class="logo content-zh">旋量太极知识库</span>
                    <span class="logo content-en">Spinor-Taiji Knowledge Base</span>
                    <span class="logo-en content-zh">Knowledge Base</span>
                    <span class="logo-en content-en">旋量太极知识库</span>
                </div>
                <div class="lang-switcher">
                    <button class="lang-btn" data-lang="zh-CN" onclick="setLanguage('zh-CN')">中文</button>
                    <button class="lang-btn" data-lang="en" onclick="setLanguage('en')">English</button>
                </div>
            </div>
        </header>

        <div class="main-content">
            <div class="card">
                <h2 class="card-title">
                    <span class="content-zh">📚 词汇表</span>
                    <span class="content-en">📚 Glossary</span>
                    <span class="card-title-en content-zh">Glossary</span>
                    <span class="card-title-en content-en">词汇表</span>
                </h2>
                <div class="content-zh">
                    <p style="color: #666; margin-bottom: 20px;">探索旋量太极理论中的核心概念与术语，理解宇宙的振动本质。</p>
                    <div class="glossary-preview">
                        <div class="glossary-item">
                            <div class="glossary-term">旋量 (Spinor)</div>
                            <div class="glossary-def">需720°复原的振动种子，正负双解共源</div>
                        </div>
                        <div class="glossary-item">
                            <div class="glossary-term">时间 (Time)</div>
                            <div class="glossary-def">平方与开方的连续脉冲</div>
                        </div>
                        <div class="glossary-item">
                            <div class="glossary-term">爱 (Love)</div>
                            <div class="glossary-def">两旋量场的相位锁定</div>
                        </div>
                    </div>
                    <div style="margin-top: 20px;">
                        <a href="articles/zh/spinor-taiji-glossary.html" class="btn">查看完整词汇表</a>
                    </div>
                </div>
                <div class="content-en" style="display: none;">
                    <p style="color: #666; margin-bottom: 20px;">Explore core concepts and terminology in Spinor-Taiji theory, understanding the vibrational nature of the universe.</p>
                    <div class="glossary-preview">
                        <div class="glossary-item">
                            <div class="glossary-term">Spinor</div>
                            <div class="glossary-def">A vibrational seed requiring 720° restoration, with dual positive and negative solutions</div>
                        </div>
                        <div class="glossary-item">
                            <div class="glossary-term">Time</div>
                            <div class="glossary-def">Continuous pulse of squaring and rooting operations</div>
                        </div>
                        <div class="glossary-item">
                            <div class="glossary-term">Love</div>
                            <div class="glossary-def">Phase locking of two spinor fields</div>
                        </div>
                    </div>
                    <div style="margin-top: 20px;">
                        <a href="articles/en/spinor-taiji-glossary.html" class="btn">View Full Glossary</a>
                    </div>
                </div>
            </div>

            <div class="card">
                <h2 class="card-title">
                    <span class="content-zh">📖 旋量-太极模型声明</span>
                    <span class="content-en">📖 Spinor-Taiji Model Declaration</span>
                    <span class="card-title-en content-zh">Model Declaration</span>
                    <span class="card-title-en content-en">旋量-太极模型声明</span>
                </h2>
                <div class="content-zh">
                    <div class="declaration-preview">
                        <div style="margin-bottom: 15px;">
                            <span class="declaration-tag">本体论声明</span>
                            <span class="declaration-tag">方法论框架</span>
                            <span class="declaration-tag">实践指南</span>
                        </div>
                        <p class="declaration-text">
                            <strong>旋量-太极模型</strong>是一个基于量子力学与东方哲学融合的认知框架。它将旋量（Spinor）作为宇宙的基本振动单元，
                            通过平方与开方的操作来描述从潜能到显现的转化过程。
                        </p>
                        <p class="declaration-text" style="margin-top: 15px;">
                            模型的核心命题是：<strong>"万物皆旋量，旋量即道"</strong>。
                            一切存在都是不同频率的旋量振动，而道则是容纳所有旋量生灭的空性场域。
                        </p>
                    </div>
                    <div style="margin-top: 20px;">
                        <a href="articles/zh/spinor-taiji-model-statement.html" class="btn">阅读完整声明</a>
                    </div>
                </div>
                <div class="content-en" style="display: none;">
                    <div class="declaration-preview">
                        <div style="margin-bottom: 15px;">
                            <span class="declaration-tag">Ontological Declaration</span>
                            <span class="declaration-tag">Methodological Framework</span>
                            <span class="declaration-tag">Practice Guide</span>
                        </div>
                        <p class="declaration-text">
                            The <strong>Spinor-Taiji Model</strong> is a cognitive framework integrating quantum mechanics with Eastern philosophy. 
                            It takes Spinor as the fundamental vibrational unit of the universe, describing the transformation from potential to manifestation 
                            through squaring and rooting operations.
                        </p>
                        <p class="declaration-text" style="margin-top: 15px;">
                            The core proposition of the model is: <strong>"All things are spinors, spinors are the Dao"</strong>. 
                            All existence is spinor vibration at different frequencies, and the Dao is the empty field that contains all spinor births and deaths.
                        </p>
                    </div>
                    <div style="margin-top: 20px;">
                        <a href="articles/en/spinor-taiji-model-declaration.html" class="btn">Read Full Declaration</a>
                    </div>
                </div>
            </div>

        </div>

        <footer>
            <p class="content-zh">旋量太极知识库 © 2026 | 探索宇宙的振动本质</p>
            <p class="content-en" style="display: none;">Spinor-Taiji Knowledge Base © 2026 | Exploring the vibrational nature of the universe</p>
        </footer>
    </div>
</body>
</html>"""
    
    try:
        with open(os.path.join(paths['dist_dir'], 'index.html'), 'w', encoding='utf-8') as f:
            f.write(index_html)
        logger.success("首页生成完成")
    except Exception as e:
        logger.error(f"首页生成失败: {str(e)}")
        return 1
    
    # 生成 _redirects 文件
    logger.info("")
    logger.info("【阶段6】配置文件生成")
    
    redirect_rules = config.get("redirect_rules", {}).get("rules", [])
    redirects_lines = ["# Cloudflare Pages 重定向规则", "# 中文主文件 -> 英文别名（用于SEO优化）", ""]
    for rule in redirect_rules:
        redirects_lines.append(f"{rule['from']} {rule['to']} {rule['status']}")
    redirects_lines.append("")
    redirects_lines.append("# 首页重定向")
    redirects_lines.append("/docs/ / 301")
    redirects_content = "\n".join(redirects_lines)
    
    try:
        with open(os.path.join(paths['dist_dir'], '_redirects'), 'w', encoding='utf-8') as f:
            f.write(redirects_content)
        logger.success(f"_redirects 文件生成完成 ({len(redirect_rules)} 条规则)")
    except Exception as e:
        logger.error(f"_redirects 文件生成失败: {str(e)}")
        return 1
    
    # 生成 _headers 文件
    if os.path.exists(paths['config_headers']):
        try:
            headers_config = json.load(open(paths['config_headers'], 'r', encoding='utf-8'))
            headers_lines = []
            for header_rule in headers_config["headers"]:
                headers_lines.append(f"{header_rule['path']}")
                for name, value in header_rule["headers"].items():
                    headers_lines.append(f"  {name}: {value}")
                headers_lines.append("")
            headers_content = "\n".join(headers_lines)
            
            with open(os.path.join(paths['dist_dir'], '_headers'), 'w', encoding='utf-8') as f:
                f.write(headers_content)
            logger.success(f"_headers 文件生成完成 ({len(headers_config['headers'])} 条规则)")
        except Exception as e:
            logger.error(f"_headers 文件生成失败: {str(e)}")
            return 1
    else:
        logger.warn("headers_config.json 不存在，跳过 _headers 生成")
    
    # 生成构建报告
    logger.info("")
    logger.info("=" * 60)
    logger.info("【构建报告】")
    logger.info("=" * 60)
    
    # 统计文件数量
    article_count = 0
    total_files = 0
    
    for root, dirs, files in os.walk(paths['dist_dir']):
        for f in files:
            total_files += 1
            if f.endswith('.html') and 'articles' in root:
                article_count += 1
    
    logger.info(f"总文件数: {total_files}")
    logger.info(f"文章文件数: {article_count}")
    logger.info(f"构建耗时: {logger.elapsed()} 秒")
    
    # 检查输出目录结构
    dist_contents = os.listdir(paths['dist_dir'])
    logger.info(f"输出目录内容: {dist_contents}")
    
    logger.success("")
    logger.success("构建完成！")
    logger.success("=" * 60)
    
    return 0

if __name__ == "__main__":
    try:
        exit_code = main()
        exit(exit_code)
    except Exception as e:
        print(f"[FATAL] 构建过程发生未预期错误: {str(e)}")
        exit(1)
