#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
看山三境界 - 头图生成程序
基于Quantum_Tai_Chi_00.png的视觉风格设计

文章：《"Spinor-Taiji model"模型中，"看山三境界"》
设计：融合量子物理与太极元素，体现"看山三境界"递进式构图
尺寸：1200×630像素，300dpi
"""

import os
import sys
import logging
from datetime import datetime
from pathlib import Path

# 导入图像生成模块
try:
    from doubao_image_generator import generate_image
    DOUBÃO_AVAILABLE = True
except ImportError:
    DOUBÃO_AVAILABLE = False
    print("⚠️ 豆包图像生成模块不可用，使用占位符图像")

# 配置日志
LOG_DIR = Path("E:/Trac Project/02-文化自信/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / f"cover_generation_{datetime.now().strftime('%Y%m%d')}.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def generate_three_realms_cover():
    """
    为"看山三境界"生成头图
    
    设计理念：
    1. 中心：太极图，代表"道"的本源
    2. 左侧：矢量/色（第一境界：看山是山）
    3. 中间：旋量/空（第二境界：看山不是山）
    4. 右侧：觉知/域（第三境界：看山还是山）
    5. 背景：量子场论波形，体现科技感
    6. 预留标题区域在底部
    """
    
    logger.info("=" * 60)
    logger.info("开始生成「看山三境界」头图")
    logger.info("文章：《"Spinor-Taiji model"模型中，"看山三境界"》")
    logger.info("=" * 60)
    
    # 文章信息
    article_title = "看山三境界"
    article_dir = "Spinor-Taiji model"
    save_dir = Path(f"E:/Trac Project/02-文化自信/images/{article_dir}_images")
    save_dir.mkdir(parents=True, exist_ok=True)
    
    # 生成文件名：文章标题+日期
    date_str = datetime.now().strftime('%Y%m%d')
    filename = f"{article_title}_v2_{date_str}.jpg"
    save_path = save_dir / filename
    
    # 头图设计提示词
    design_prompt = """
    【设计风格】
    高端学术风格，融合量子物理与东方哲学元素
    
    【核心视觉元素】
    1. 中心：太极图，阴阳鱼相互环绕旋转
    2. 左区（第一境界）：具象山峰，代表"看山是山"
    3. 中区（第二境界）：旋量数学图形，720度旋转
    4. 右区（第三境界）：抽象山峰轮廓，象征回归
    5. 背景：量子场论波形，星光粒子效果
    
    【配色方案】
    - 主色：深蓝(#1a237e) + 金色(#c9a227)
    - 辅色：太极红(#8B1E22) + 量子蓝(#4fc3f7)
    - 背景：深邃星空渐变
    
    【技术规格】
    - 尺寸：1200×630像素（16:9）
    - 分辨率：300dpi
    - 模式：RGB
    - 格式：JPG
    
    【文字区域】
    - 底部预留标题区域
    - 标题："看山三境界" - "Spinor-Taiji model"模型解读
    - 字体：衬线体，优雅大气
    
    【整体风格】
    - 专业性与禅意融合
    - 科技感与传统文化结合
    - 构图平衡，留白得当
    - 适合微信公众号封面
    """
    
    logger.info(f"📐 设计规格：1200×630像素，300dpi")
    logger.info(f"💾 保存路径：{save_path}")
    logger.info(f"🎨 设计风格：量子物理+东方哲学融合")
    
    # 生成图像
    if DOUBÃO_AVAILABLE:
        try:
            logger.info("🔄 正在调用豆包AI生成图像...")
            image_url = generate_image(
                prompt=design_prompt,
                size="16:9",
                quality="high"
            )
            logger.info(f"✅ 图像生成成功：{image_url}")
            
            # 下载并保存图像
            import requests
            response = requests.get(image_url)
            if response.status_code == 200:
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                
                # 获取文件大小
                file_size = os.path.getsize(save_path)
                logger.info(f"💾 图像已保存：{save_path}")
                logger.info(f"📊 文件大小：{file_size / 1024:.2f} KB")
                logger.info(f"🎨 格式：JPG")
                
                return {
                    "success": True,
                    "path": str(save_path),
                    "filename": filename,
                    "size": file_size,
                    "format": "JPG",
                    "dimensions": "1200×630"
                }
            else:
                raise Exception(f"下载失败，HTTP状态码：{response.status_code}")
                
        except Exception as e:
            logger.error(f"❌ 图像生成失败：{str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    else:
        # 创建占位符图像
        logger.warning("⚠️ 豆包模块不可用，创建占位符图像")
        create_placeholder_image(save_path)
        return {
            "success": True,
            "path": str(save_path),
            "filename": filename,
            "note": "占位符图像"
        }


def create_placeholder_image(save_path):
    """创建占位符图像"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # 创建图像
        width, height = 1200, 630
        img = Image.new('RGB', (width, height), color=(26, 35, 126))  # 深蓝色背景
        draw = ImageDraw.Draw(img)
        
        # 绘制太极图（简化版）
        center_x, center_y = width // 2, height // 2 - 50
        radius = 150
        
        # 绘制外圆
        draw.ellipse(
            [center_x - radius, center_y - radius, 
             center_x + radius, center_y + radius],
            outline=(201, 162, 39),  # 金色边框
            width=3
        )
        
        # 绘制标题区域
        title_y = height - 100
        draw.rectangle(
            [0, title_y, width, height],
            fill=(0, 0, 0, 180)  # 半透明黑色背景
        )
        
        # 添加标题文字
        try:
            font = ImageFont.truetype("arial.ttf", 48)
            font_small = ImageFont.truetype("arial.ttf", 24)
        except:
            font = ImageFont.load_default()
            font_small = font
        
        draw.text(
            (width // 2, title_y + 35),
            "看山三境界",
            fill=(255, 255, 255),
            font=font,
            anchor='mm'
        )
        
        draw.text(
            (width // 2, title_y + 75),
            '"Spinor-Taiji model"模型解读',
            fill=(201, 162, 39),
            font=font_small,
            anchor='mm'
        )
        
        # 保存图像
        img.save(save_path, 'JPEG', quality=95)
        logger.info(f"✅ 占位符图像已创建：{save_path}")
        
    except ImportError:
        logger.error("❌ PIL库不可用，无法创建占位符图像")
        raise


def log_generation_result(result):
    """记录生成结果到日志"""
    logger.info("=" * 60)
    logger.info("📋 生成结果汇总")
    logger.info("=" * 60)
    
    if result["success"]:
        logger.info(f"✅ 状态：成功")
        logger.info(f"📁 文件：{result.get('filename')}")
        logger.info(f"💾 路径：{result.get('path')}")
        logger.info(f"📊 大小：{result.get('size', 0) / 1024:.2f} KB")
        logger.info(f"🎨 格式：{result.get('format')}")
        logger.info(f"📐 尺寸：{result.get('dimensions')}")
    else:
        logger.error(f"❌ 状态：失败")
        logger.error(f"💬 错误：{result.get('error')}")
    
    logger.info("=" * 60)


if __name__ == "__main__":
    print("🎨 开始为「看山三境界」生成头图...")
    print("=" * 60)
    
    # 生成头图
    result = generate_three_realms_cover()
    
    # 记录结果
    log_generation_result(result)
    
    # 输出结果
    if result["success"]:
        print("\n✅ 头图生成成功！")
        print(f"📁 文件：{result.get('filename')}")
        print(f"💾 路径：{result.get('path')}")
    else:
        print("\n❌ 头图生成失败")
        print(f"💬 错误：{result.get('error')}")
        print("\n🔄 请重试或检查配置")
