"""
AI讨好现象及其风险 - 封面图生成脚本（简化版）
"""

import sys
import os
from pathlib import Path

# 设置编码
os.environ['PYTHONIOENCODING'] = 'utf-8'

sys.path.insert(0, r"E:\Trac Project")

try:
    from doubao_image_generator import DoubaoImageGenerator
    import doubao_config
except ImportError as e:
    print(f"Error: Cannot import required modules: {e}")
    sys.exit(1)

def main():
    # 初始化生成器
    generator = DoubaoImageGenerator(doubao_config.DOUBAO_API_KEY)
    
    # 封面图提示词
    prompt = """Minimalist WeChat article cover image depicting AI flattery concept.
    
    Design elements:
    - Humanoid AI robot with friendly/flattering smile
    - Mirror reflections showing distortion
    - Clean geometric shapes representing truth vs flattery
    - Color: Deep red accent (#8B1E22), white background
    - Professional tech illustration style
    
    Theme: AI flattery phenomenon and ethical boundaries in AI design
    """
    
    # 输出路径
    output_dir = Path(r"E:\Trac Project\04-伦理即内核\images")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "AI讨好现象及其风险_封面图.jpg"
    
    print("Generating cover image...")
    
    try:
        result = generator.generate_image(
            prompt=prompt,
            image_size="landscape_16_9",
            output_path=str(output_path)
        )
        
        if result:
            print(f"Success! Image saved to: {output_path}")
        else:
            print("Failed to generate image")
            
    except Exception as e:
        print(f"Error during generation: {e}")

if __name__ == "__main__":
    main()
