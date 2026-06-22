import os
import json
import shutil
import datetime
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scripts/article_manager.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class ArticleManager:
    def __init__(self, config_path='config/article_aliases.json'):
        self.config_path = config_path
        self.config = self._load_config()
        self.articles_dir = 'articles'
    
    def _load_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            'description': 'Article filename mapping configuration',
            'version': '1.0',
            'aliases': {},
            'redirect_rules': {
                'description': 'Cloudflare Pages redirect rules',
                'rules': []
            },
            'history': []
        }
    
    def _save_config(self):
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=4)
    
    def generate_english_name(self, chinese_name):
        name_map = {
            '旋量-太极': 'spinor-taiji',
            '模型': 'model',
            '声明': 'statement',
            '伦理': 'lunli',
            '即': 'ji',
            '道体': 'daoti',
            '理念': 'philosophy',
            '落地': 'practice',
            '指南': 'guide',
            '道德经': 'daodejing',
            '无死地': 'wusidi',
            '读解': 'reading',
            '心经': 'heart-sutra',
            '振动': 'vibration',
            '科学': 'science',
            '觉知': 'awareness',
            '智慧': 'wisdom',
            '色即是空': 'form-is-emptiness',
            '认知': 'cognition',
            '实践': 'practice',
            '升级': 'upgrade',
            '高考': 'gaokao',
            '作文': 'essay',
            '胃病': 'stomach-disease',
            '调理': 'chronic-gastritis',
            '长期': 'chronic',
            '响应式': 'responsive',
            '表格': 'table',
            '演示': 'demo',
            '阅读': 'reading',
            '地图': 'map',
            '看山': 'three-realms',
            '境界': 'realms',
            '核心': 'core',
            '数据': 'data',
            '思维': 'thinking',
            '为什么': 'why',
            '为道日损': 'dao-sun',
            '排版': 'layout',
            '大众': 'popular',
            '修复': 'fixed',
            '专业': 'professional',
            '系列': 'series',
            '实修': 'practice',
            '对比': 'comparison',
            '学术': 'academic',
            '公众号': 'official',
            '微信': 'wechat',
            '版': 'version'
        }
        
        name = chinese_name.replace('.html', '')
        name = name.replace('_公众号版', '').replace('_微信公众号版', '')
        name = name.replace('_修复后', '').replace('_修复版', '')
        name = name.replace('_排版版', '').replace('_对比版', '')
        name = name.replace('_学术版', '').replace('_专业版', '')
        name = name.replace('_大众版', '').replace('_数据', '')
        name = name.replace('_6月4日模板', '').replace('_with_new_images', '')
        
        parts = []
        remaining = name
        while remaining:
            matched = False
            for key in sorted(name_map.keys(), key=len, reverse=True):
                if remaining.startswith(key):
                    parts.append(name_map[key])
                    remaining = remaining[len(key):]
                    remaining = remaining.lstrip('_')
                    matched = True
                    break
            if not matched:
                remaining = remaining[1:]
        
        if not parts:
            parts = ['article']
        
        return '-'.join(parts).lower() + '.html'
    
    def add_article(self, source_path, chinese_name=None):
        try:
            if not os.path.exists(source_path):
                logging.error(f"源文件不存在: {source_path}")
                return False, "源文件不存在"
            
            if chinese_name is None:
                chinese_name = os.path.basename(source_path)
            
            if not chinese_name.endswith('.html'):
                logging.error(f"文件名必须以.html结尾: {chinese_name}")
                return False, "文件名必须以.html结尾"
            
            dest_path = os.path.join(self.articles_dir, chinese_name)
            
            shutil.copy2(source_path, dest_path)
            logging.info(f"文件已复制到: {dest_path}")
            
            english_name = self.generate_english_name(chinese_name)
            
            if chinese_name in self.config['aliases']:
                logging.warning(f"文件名已存在于映射表中，将被更新: {chinese_name}")
            
            self.config['aliases'][chinese_name] = english_name
            
            existing_rule = next((r for r in self.config['redirect_rules']['rules'] 
                                if r['from'] == f'/articles/{chinese_name}'), None)
            if existing_rule:
                existing_rule['to'] = f'/articles/{english_name}'
            else:
                self.config['redirect_rules']['rules'].append({
                    'from': f'/articles/{chinese_name}',
                    'to': f'/articles/{english_name}',
                    'status': 301
                })
            
            self.config['history'].append({
                'action': 'add',
                'chinese_name': chinese_name,
                'english_name': english_name,
                'source_path': source_path,
                'dest_path': dest_path,
                'date': datetime.datetime.now().isoformat()
            })
            
            version_parts = self.config['version'].split('.')
            self.config['version'] = f"{version_parts[0]}.{int(version_parts[1]) + 1}"
            
            self._save_config()
            logging.info(f"文章添加成功: {chinese_name} -> {english_name}")
            
            return True, f"文章添加成功\n中文文件名: {chinese_name}\n英文文件名: {english_name}\n存储路径: {dest_path}"
        
        except Exception as e:
            logging.error(f"添加文章失败: {str(e)}")
            return False, f"添加文章失败: {str(e)}"
    
    def move_article(self, source_path, chinese_name=None):
        try:
            if not os.path.exists(source_path):
                logging.error(f"源文件不存在: {source_path}")
                return False, "源文件不存在"
            
            if chinese_name is None:
                chinese_name = os.path.basename(source_path)
            
            dest_path = os.path.join(self.articles_dir, chinese_name)
            
            shutil.move(source_path, dest_path)
            logging.info(f"文件已移动到: {dest_path}")
            
            return self.add_article(dest_path, chinese_name)
        
        except Exception as e:
            logging.error(f"移动文章失败: {str(e)}")
            return False, f"移动文章失败: {str(e)}"
    
    def list_articles(self):
        articles = []
        for chinese, english in self.config['aliases'].items():
            path = os.path.join(self.articles_dir, chinese)
            exists = os.path.exists(path)
            articles.append({
                'chinese_name': chinese,
                'english_name': english,
                'exists': exists,
                'path': path
            })
        return articles
    
    def show_mapping_table(self):
        print("\n" + "="*80)
        print(f"文章映射表 - 版本: {self.config['version']}")
        print("="*80)
        print(f"{'中文文件名':<40} {'英文文件名':<30} {'状态'}")
        print("-"*80)
        
        articles = self.list_articles()
        for article in articles:
            status = "✓ 存在" if article['exists'] else "✗ 缺失"
            print(f"{article['chinese_name']:<40} {article['english_name']:<30} {status}")
        
        print("="*80)
        print(f"总计: {len(articles)} 篇文章")
        print("="*80)

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='文章管理工具')
    parser.add_argument('--add', help='添加文章文件')
    parser.add_argument('--move', help='移动文章文件到articles目录')
    parser.add_argument('--list', action='store_true', help='列出所有文章')
    parser.add_argument('--name', help='指定中文文件名（可选）')
    
    args = parser.parse_args()
    
    manager = ArticleManager()
    
    if args.move:
        success, message = manager.move_article(args.move, args.name)
        print(message)
        if success:
            manager.show_mapping_table()
    
    elif args.add:
        success, message = manager.add_article(args.add, args.name)
        print(message)
        if success:
            manager.show_mapping_table()
    
    elif args.list:
        manager.show_mapping_table()
    
    else:
        parser.print_help()

if __name__ == '__main__':
