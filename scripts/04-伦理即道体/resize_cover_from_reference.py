#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片尺寸调整脚本
基于参考图片"AI讨好现象及其风险_头图_2048x1800.png"重新设计
调整至微信公众号标准尺寸：1080 × 560 像素
"""

from PIL import Image
from pathlib import Path

def resize_and_adjust_image(input_path, output_path, target_width=1080, target_height=560):
    """
    调整图片尺寸并保持核心视觉元素
    
    参数:
        input_path: 参考图片路径
        output_path: 输出图片路径
        target_width: 目标宽度（默认1080px）
        target_height: 目标高度（默认560px）
    """
    
    print(f"正在处理图片: {input_path}")
    print(f"目标尺寸: {target_width} × {target_height} 像素")
    
    try:
        # 打开参考图片
        with Image.open(input_path) as img:
            original_width, original_height = img.size
            print(f"原始尺寸: {original_width} × {original_height} 像素")
            
            # 计算缩放比例
            width_ratio = target_width / original_width
            height_ratio = target_height / original_height
            scale_ratio = min(width_ratio, height_ratio)
            
            print(f"缩放比例: {scale_ratio:.2f}")
            
            # 计算缩放后的尺寸
            scaled_width = int(original_width * scale_ratio)
            scaled_height = int(original_height * scale_ratio)
            
            # 调整尺寸（使用高质量缩放算法）
            resized_img = img.resize((scaled_width, scaled_height), Image.Resampling.LANCZOS)
            
            # 创建新画布并居中放置调整后的图片
            new_img = Image.new('RGB', (target_width, target_height), color=(5, 15, 35))
            
            # 计算居中位置
            x_offset = (target_width - scaled_width) // 2
            y_offset = (target_height - scaled_height) // 2
            
            # 将调整后的图片粘贴到新画布上
            new_img.paste(resized_img, (x_offset, y_offset))
            
            # 如果高度方向有空白，尝试裁剪原图以更好地适配
            if scaled_height < target_height:
                # 计算需要裁剪的区域（保留中心部分）
                crop_top = (original_height - (target_height / scale_ratio)) / 2
                crop_bottom = original_height - crop_top
                
                # 重新裁剪并调整
                cropped_img = img.crop((0, crop_top, original_width, crop_bottom))
                resized_cropped = cropped_img.resize((target_width, target_height), Image.Resampling.LANCZOS)
                new_img = resized_cropped
            
            # 保存结果
            new_img.save(output_path, quality=95)
            print(f"✅ 图片已成功保存到: {output_path}")
            
            # 验证结果
            final_img = Image.open(output_path)
            final_width, final_height = final_img.size
            print(f"最终尺寸验证: {final_width} × {final_height} 像素 ✓")
            
            return output_path
            
    except Exception as e:
        print(f"❌ 处理过程中出错: {e}")
        return None

if __name__ == '__main__':
    # 输入输出路径
    input_path = r"E:\Trac Project\04-伦理即内核\images\AI讨好现象及其风险_头图_2048x1800.png"
    output_path = r"E:\Trac Project\04-伦理即内核\images\AI讨好现象及其风险_公众号头图_1080x560_v2.jpg"
    
    # 执行调整
    resize_and_adjust_image(input_path, output_path)
