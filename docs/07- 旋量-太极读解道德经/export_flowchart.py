#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将三步法流程图导出为高质量PNG图片
"""

import sys
import os

# 添加技能路径
sys.path.insert(0, r'e:\Trac Project\.trae\skills\mermaid-exporter')

def export_mermaid_diagram(mermaid_code, output_path, background="white", width=1200, scale=2.0):
    """导出Mermaid图表为PNG"""
    
    try:
        from mermaid import Mermaid
    except ImportError:
        print("正在安装mermaid包...")
        os.system(f'"{sys.executable}" -m pip install mermaid -q')
        from mermaid import Mermaid
    
    print(f"正在导出流程图到: {output_path}")
    print(f"参数: width={width}, scale={scale}, background={background}")
    
    mmd = Mermaid(mermaid_code)
    
    # 导出为PNG
    image_data = mmd.draw(background=background, width=width, scale=scale)
    
    with open(output_path, 'wb') as f:
        f.write(image_data)
    
    file_size = os.path.getsize(output_path) / 1024
    print(f"✅ 导出成功！文件大小: {file_size:.2f} KB")
    return output_path

def main():
    # Mermaid格式的三步法流程图
    mermaid_code = """flowchart TB
    %% 样式定义
    classDef golden fill:#d4af37,stroke:#8B6914,color:#333,stroke-width:3px
    classDef blue fill:#2c3e50,stroke:#1a252f,color:white,stroke-width:3px
    classDef purple fill:#8e44ad,stroke:#6c3483,color:white,stroke-width:2px
    classDef green fill:#27ae60,stroke:#1e8449,color:white,stroke-width:2px
    classDef orange fill:#e67e22,stroke:#d35400,color:white,stroke-width:2px
    classDef diamond fill:#f39c12,stroke:#d35400,color:white,stroke-width:2px
    
    %% 节点定义
    A(("☯ 觉知域<br/>（道）")) --> B("① 第一步：识别状态<br/><small>诊断当前振动模式</small>")
    B --> C{"◆ 当前状态？ ◆"}
    
    C -->|"旋量态<br/>流动·灵活·潜能"| D["旋量态"]
    C -->|"矢量态<br/>固化·僵硬·边界"| E["矢量态"]
    
    D --> F["② 平方操作<br/><small>显化·创造·行动</small>"]
    E --> G["② 开方操作<br/><small>消解·流动·回归</small>"]
    
    F --> H["③ 第三步：安住觉知域<br/><small>超越操作，回归观察者背景</small>"]
    G --> H
    
    H --> I(("☯ 觉知域<br/>（道）"))
    
    %% 应用样式
    class A,I golden
    class B,H blue
    class C diamond
    class D purple
    class E green
    class F,G orange
"""
    
    output_path = r'e:\Trac Project\07- Spinor-Taiji model读解道德经\三步法流程图.png'
    
    try:
        export_mermaid_diagram(
            mermaid_code=mermaid_code,
            output_path=output_path,
            background="white",
            width=1200,
            scale=3.0  # 高分辨率
        )
        print(f"\n📁 文件已保存: {output_path}")
    except Exception as e:
        print(f"❌ 导出失败: {e}")
        print("\n尝试使用备用方法...")
        fallback_export(mermaid_code, output_path)

def fallback_export(mermaid_code, output_path):
    """使用mmdc命令行工具导出"""
    import subprocess
    
    # 保存mermaid代码到临时文件
    mmd_path = r'e:\Trac Project\07- Spinor-Taiji model读解道德经\temp_flowchart.mmd'
    with open(mmd_path, 'w', encoding='utf-8') as f:
        f.write(mermaid_code)
    
    print(f"Mermaid代码已保存到: {mmd_path}")
    print("\n请手动运行以下命令导出图片：")
    print(f'mmdc -i "{mmd_path}" -o "{output_path}" -b white -w 1200 -s 3')
    
    # 尝试自动运行
    try:
        result = subprocess.run(
            ['mmdc', '-i', mmd_path, '-o', output_path, '-b', 'white', '-w', '1200', '-s', '3'],
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode == 0:
            print(f"\n✅ 备用方法导出成功！")
            file_size = os.path.getsize(output_path) / 1024
            print(f"📁 文件大小: {file_size:.2f} KB")
        else:
            print(f"❌ 备用方法失败: {result.stderr}")
    except FileNotFoundError:
        print("❌ mmdc命令未找到，请安装 mermaid-cli:")
        print("npm install -g @mermaid-js/mermaid-cli")
    except Exception as e:
        print(f"❌ 备用方法出错: {e}")

if __name__ == '__main__':
    main()
