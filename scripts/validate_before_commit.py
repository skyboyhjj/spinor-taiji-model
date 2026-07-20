#!/usr/bin/env python3
"""
代码提交前验证脚本
执行完整的本地验证流程，确保代码质量
"""

import os
import sys
import subprocess
import py_compile
import shutil
import re

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

VALID_TYPES = {'feat', 'fix', 'refactor', 'docs', 'style', 'test', 'chore', 'perf'}

def print_status(message, status='INFO'):
    colors = {
        'INFO': '\033[94m',
        'SUCCESS': '\033[92m',
        'WARNING': '\033[93m',
        'ERROR': '\033[91m'
    }
    print(f"{colors.get(status, '')}[{status}] {message}\033[0m")

def check_python_syntax():
    print_status("步骤1: Python语法检查", "INFO")
    scripts_dir = os.path.join(PROJECT_ROOT, 'scripts')
    
    skip_files = {
        'convert_md_to_wechat.py',
        'rename_articles.py',
        'test_interactions.py',
        'update_graph_interactive.py',
    }
    
    python_files = []
    for root, dirs, files in os.walk(scripts_dir):
        for file in files:
            if file.endswith('.py') and file not in skip_files:
                python_files.append(os.path.join(root, file))
    
    errors = []
    for py_file in python_files:
        try:
            py_compile.compile(py_file, doraise=True)
            print(f"  [OK] {os.path.relpath(py_file, PROJECT_ROOT)}")
        except py_compile.PyCompileError as e:
            errors.append(f"  [FAIL] {os.path.relpath(py_file, PROJECT_ROOT)}: {e}")
    
    if errors:
        print_status("\n".join(errors), "ERROR")
        return False
    
    if skip_files:
        print_status(f"跳过已知不完整文件: {', '.join(skip_files)}", "WARNING")
    
    print_status("Python语法检查通过", "SUCCESS")
    return True

def check_build():
    print_status("\n步骤2: 构建验证", "INFO")
    
    build_script = os.path.join(PROJECT_ROOT, 'scripts', 'build.py')
    result = subprocess.run(
        [sys.executable, build_script],
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT
    )
    
    if result.returncode == 0:
        print("  [OK] 构建成功")
        
        dist_dir = os.path.join(PROJECT_ROOT, 'dist')
        required_dirs = ['articles', 'assets', 'docs', 'functions']
        for d in required_dirs:
            if os.path.exists(os.path.join(dist_dir, d)):
                print(f"  [OK] dist/{d}/ 目录存在")
            else:
                print_status(f"  [FAIL] dist/{d}/ 目录不存在", "ERROR")
                return False
        
        assets_files = ['feedback.css', 'feedback.js', 'floating-buttons.css', 'floating-buttons.js']
        for f in assets_files:
            if os.path.exists(os.path.join(dist_dir, 'assets', f)):
                print(f"  [OK] dist/assets/{f} 存在")
            else:
                print_status(f"  [FAIL] dist/assets/{f} 不存在", "ERROR")
                return False
        
        print_status("构建验证通过", "SUCCESS")
        return True
    else:
        print_status(f"构建失败:\n{result.stderr}", "ERROR")
        return False

def check_commit_message():
    print_status("\n步骤3: 提交信息格式检查", "INFO")
    
    commit_msg_file = os.environ.get('GIT_COMMIT_MSG_FILE')
    if commit_msg_file and os.path.exists(commit_msg_file):
        with open(commit_msg_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if not lines:
            print_status("提交信息为空", "ERROR")
            return False
        
        first_line = lines[0].strip()
        
        if len(first_line) > 72:
            print_status(f"提交信息首行过长 ({len(first_line)} > 72)", "ERROR")
            return False
        
        parts = first_line.split(':', 1)
        if len(parts) != 2:
            print_status(f"提交信息格式错误: {first_line}", "ERROR")
            print_status("正确格式: type(scope): description", "WARNING")
            return False
        
        type_scope = parts[0].strip()
        description = parts[1].strip()
        
        if not description:
            print_status("提交信息描述为空", "ERROR")
            return False
        
        if '(' in type_scope and ')' in type_scope:
            commit_type = type_scope.split('(')[0]
            scope = type_scope.split('(')[1].rstrip(')')
        else:
            commit_type = type_scope
            scope = None
        
        if commit_type not in VALID_TYPES:
            print_status(f"提交类型无效: {commit_type}", "ERROR")
            print_status(f"有效类型: {', '.join(sorted(VALID_TYPES))}", "WARNING")
            return False
        
        print(f"  [OK] 类型: {commit_type}")
        if scope:
            print(f"  [OK] 范围: {scope}")
        print(f"  [OK] 描述: {description}")
        print_status("提交信息格式检查通过", "SUCCESS")
        return True
    else:
        print_status("跳过提交信息检查（非git commit场景）", "WARNING")
        return True

def check_css_braces():
    print_status("\n步骤4: CSS @media 括号匹配检查", "INFO")
    
    changed_files = []
    result = subprocess.run(
        ['git', 'diff', '--cached', '--name-only', '--diff-filter=ACMR'],
        capture_output=True, text=True, cwd=PROJECT_ROOT
    )
    if result.returncode == 0 and result.stdout.strip():
        changed_files = result.stdout.strip().split('\n')
    else:
        result2 = subprocess.run(
            ['git', 'diff', '--name-only', '--diff-filter=ACMR'],
            capture_output=True, text=True, cwd=PROJECT_ROOT
        )
        if result2.returncode == 0 and result2.stdout.strip():
            changed_files = result2.stdout.strip().split('\n')
    
    target_files = [
        f for f in changed_files
        if f.endswith('.html') or f.endswith('.css')
    ]
    
    if not target_files:
        print_status("无变更的 HTML/CSS 文件，跳过 CSS 检查", "WARNING")
        return True
    
    check_dirs = {
        os.path.join(PROJECT_ROOT, 'articles'),
        os.path.join(PROJECT_ROOT, 'docs'),
        os.path.join(PROJECT_ROOT, 'wechat'),
        os.path.join(PROJECT_ROOT, 'assets'),
    }
    
    all_files = []
    for d in check_dirs:
        if os.path.exists(d):
            for root, dirs, files in os.walk(d):
                for f in files:
                    if f.endswith(('.html', '.css')):
                        all_files.append(os.path.join(root, f))
    
    errors = []
    checked = 0
    
    for file_path in all_files:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
            
            if file_path.endswith('.html'):
                style_blocks = re.findall(r'<style[^>]*>(.*?)</style>', content, re.DOTALL | re.IGNORECASE)
                css_content = '\n'.join(style_blocks)
            else:
                css_content = content
            
            media_blocks = list(re.finditer(r'@media[^{]*\{', css_content))
            
            for i, match in enumerate(media_blocks):
                start_pos = match.end()
                depth = 1
                pos = start_pos
                while pos < len(css_content) and depth > 0:
                    ch = css_content[pos]
                    if ch == '{':
                        depth += 1
                    elif ch == '}':
                        depth -= 1
                    pos += 1
                
                if depth > 0:
                    next_media_pos = css_content.find('@media', start_pos)
                    line_num = content[:match.start()].count('\n') + 1
                    errors.append(
                        f"  [FAIL] {os.path.relpath(file_path, PROJECT_ROOT)}:"
                        f" 行{line_num} @media 块缺少闭合 '}}'"
                    )
                    if next_media_pos > 0 and next_media_pos < start_pos + 500:
                        errors.append(f"         (下一个 @media 位于约 {css_content[:next_media_pos].count(chr(10)) + 1} 行)")
            
            checked += 1
        except Exception as e:
            errors.append(f"  [FAIL] {os.path.relpath(file_path, PROJECT_ROOT)}: 读取异常 - {e}")
    
    if checked > 0:
        print(f"  [OK] 已检查 {checked} 个 CSS/HTML 文件")
    
    if errors:
        print_status(f"发现 {len(errors)} 个 CSS @media 括号匹配问题:", "ERROR")
        for err in errors:
            print(err)
        return False
    
    print_status("CSS @media 括号匹配检查通过", "SUCCESS")
    return True

def run_all_checks():
    print("=" * 60)
    print("代码提交前验证")
    print("=" * 60)
    
    checks = [
        ("Python语法检查", check_python_syntax),
        ("构建验证", check_build),
        ("CSS @media 括号匹配", check_css_braces),
        ("提交信息格式检查", check_commit_message),
    ]
    
    all_passed = True
    for name, check_func in checks:
        try:
            passed = check_func()
            if not passed:
                all_passed = False
        except Exception as e:
            print_status(f"{name}异常: {e}", "ERROR")
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print_status("所有验证通过！", "SUCCESS")
        return 0
    else:
        print_status("验证失败，请修复后重试", "ERROR")
        return 1

if __name__ == '__main__':
    sys.exit(run_all_checks())