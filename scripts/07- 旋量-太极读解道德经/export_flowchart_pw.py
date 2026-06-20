#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用playwright将HTML流程图导出为高质量PNG图片
"""

import os
import sys
import asyncio
from pathlib import Path

async def export_flowchart_to_png():
    """导出流程图为PNG"""
    
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        print("正在安装playwright...")
        os.system(f'"{sys.executable}" -m pip install playwright -q')
        os.system(f'"{sys.executable}" -m playwright install chromium')
        from playwright.async_api import async_playwright
    
    # HTML流程图代码
    flowchart_html = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: white;
            padding: 40px;
            margin: 0;
        }
        .flowchart {
            max-width: 900px;
            margin: 0 auto;
        }
        .flow-v2 {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 0;
        }
        .flow-v2-row {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 100%;
            margin: 10px 0;
        }
        .flow-v2-box {
            padding: 18px 30px;
            border-radius: 12px;
            text-align: center;
            min-width: 240px;
            max-width: 300px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        .flow-v2-box.golden {
            background: linear-gradient(135deg, #d4af37, #f4d03f);
            color: #333;
            border: 3px solid #8B6914;
        }
        .flow-v2-box.blue {
            background: linear-gradient(135deg, #2c3e50, #34495e);
            color: white;
            border: 3px solid #1a252f;
        }
        .flow-v2-box.purple {
            background: linear-gradient(135deg, #8e44ad, #9b59b6);
            color: white;
            border: 3px solid #6c3483;
        }
        .flow-v2-box.green {
            background: linear-gradient(135deg, #27ae60, #2ecc71);
            color: white;
            border: 3px solid #1e8449;
        }
        .flow-v2-box.orange {
            background: linear-gradient(135deg, #e67e22, #f39c12);
            color: white;
            border: 3px solid #d35400;
        }
        .flow-v2-title {
            font-size: 16px;
            font-weight: bold;
            margin-bottom: 5px;
        }
        .flow-v2-desc {
            font-size: 13px;
            opacity: 0.9;
        }
        .flow-v2-line {
            width: 4px;
            height: 30px;
            background: linear-gradient(to bottom, #8B1E22, #d4af37);
            border-radius: 2px;
        }
        .flow-v2-branch {
            display: flex;
            justify-content: space-between;
            width: 100%;
            max-width: 800px;
            margin: 15px 0;
        }
        .flow-v2-branch-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            flex: 1;
        }
        .flow-v2-branch-arrow {
            font-size: 24px;
            color: #8B1E22;
            margin: 8px 0;
        }
        .flow-v2-diamond {
            width: 140px;
            height: 140px;
            background: linear-gradient(135deg, #f39c12, #e67e22);
            color: white;
            transform: rotate(45deg);
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 12px;
            box-shadow: 0 6px 16px rgba(0,0,0,0.25);
        }
        .flow-v2-diamond-inner {
            transform: rotate(-45deg);
            text-align: center;
            font-weight: bold;
        }
        .flow-title {
            text-align: center;
            font-size: 20px;
            font-weight: bold;
            color: #333;
            margin-bottom: 30px;
        }
        .flow-desc {
            text-align: center;
            font-size: 14px;
            color: #666;
            margin-top: 30px;
        }
    </style>
</head>
<body>
    <div class="flowchart">
        <div class="flow-title">Spinor-Taiji model模型：三步法操作流程图</div>
        <div class="flow-v2">
            
            <!-- 起点：觉知域 -->
            <div class="flow-v2-row">
                <div class="flow-v2-box golden">
                    <div class="flow-v2-title">☯ 觉知域（道）</div>
                    <div class="flow-v2-desc">一切操作的源头与归宿</div>
                </div>
            </div>
            
            <div class="flow-v2-branch-arrow">↓</div>
            
            <!-- 第一步：识别状态 -->
            <div class="flow-v2-row">
                <div class="flow-v2-box blue">
                    <div class="flow-v2-title">① 第一步：识别状态</div>
                    <div class="flow-v2-desc">诊断当前振动模式</div>
                </div>
            </div>
            
            <div class="flow-v2-branch-arrow">↓</div>
            
            <!-- 判断分支 -->
            <div class="flow-v2-row">
                <div class="flow-v2-diamond">
                    <div class="flow-v2-diamond-inner">
                        <div class="flow-v2-title" style="font-size:14px;">当前状态？</div>
                    </div>
                </div>
            </div>
            
            <!-- 分支路径 -->
            <div class="flow-v2-branch">
                
                <!-- 旋量态分支 -->
                <div class="flow-v2-branch-item">
                    <div class="flow-v2-branch-arrow">↓</div>
                    <div class="flow-v2-box purple">
                        <div class="flow-v2-title">旋量态</div>
                        <div class="flow-v2-desc">流动 · 灵活 · 潜能</div>
                    </div>
                    <div class="flow-v2-branch-arrow">↓</div>
                    <div class="flow-v2-box orange">
                        <div class="flow-v2-title">② 平方操作</div>
                        <div class="flow-v2-desc">显化 · 创造 · 行动</div>
                    </div>
                </div>
                
                <!-- 中间分隔 -->
                <div style="flex: 0.5;"></div>
                
                <!-- 矢量态分支 -->
                <div class="flow-v2-branch-item">
                    <div class="flow-v2-branch-arrow">↓</div>
                    <div class="flow-v2-box green">
                        <div class="flow-v2-title">矢量态</div>
                        <div class="flow-v2-desc">固化 · 僵硬 · 边界</div>
                    </div>
                    <div class="flow-v2-branch-arrow">↓</div>
                    <div class="flow-v2-box orange">
                        <div class="flow-v2-title">② 开方操作</div>
                        <div class="flow-v2-desc">消解 · 流动 · 回归</div>
                    </div>
                </div>
            </div>
            
            <!-- 合并箭头 -->
            <div class="flow-v2-branch-arrow">↓</div>
            
            <!-- 第三步：安住觉知域 -->
            <div class="flow-v2-row">
                <div class="flow-v2-box blue">
                    <div class="flow-v2-title">③ 第三步：安住觉知域</div>
                    <div class="flow-v2-desc">超越操作，回归观察者背景</div>
                </div>
            </div>
            
            <div class="flow-v2-branch-arrow">↓</div>
            
            <!-- 终点：觉知域 -->
            <div class="flow-v2-row">
                <div class="flow-v2-box golden">
                    <div class="flow-v2-title">☯ 觉知域（道）</div>
                    <div class="flow-v2-desc">循环往复，生生不息</div>
                </div>
            </div>
            
        </div>
        
        <div class="flow-desc">
            <strong>图示说明</strong>：从觉知域出发，经三步循环：识别状态 → 应用法则（平方/开方） → 安住觉知域，最终回归道体，形成完整的操作闭环。
        </div>
    </div>
</body>
</html>
'''
    
    output_dir = Path(r'e:\Trac Project\07- Spinor-Taiji model读解道德经')
    output_path = output_dir / '三步法流程图.png'
    temp_html = output_dir / 'temp_flowchart.html'
    
    # 保存HTML文件
    with open(temp_html, 'w', encoding='utf-8') as f:
        f.write(flowchart_html)
    
    print(f"正在使用playwright导出流程图...")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1200, 'height': 1600})
        
        # 加载HTML
        await page.goto(f'file:///{temp_html}')
        await page.wait_for_load_state('networkidle')
        
        # 等待内容加载
        await asyncio.sleep(1)
        
        # 截图
        await page.screenshot(path=str(output_path), full_page=True)
        
        await browser.close()
    
    # 删除临时文件
    os.remove(temp_html)
    
    file_size = os.path.getsize(output_path) / 1024
    print(f"\n✅ 导出成功！")
    print(f"📁 文件路径: {output_path}")
    print(f"📐 文件大小: {file_size:.2f} KB")
    
    return output_path

def main():
    output_path = asyncio.run(export_flowchart_to_png())
    print(f"\n流程图PNG已生成，可直接插入文章使用。")

if __name__ == '__main__':
    main()
