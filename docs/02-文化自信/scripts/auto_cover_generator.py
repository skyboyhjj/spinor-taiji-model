#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号文章头图自动化生成系统
Automate WeChat Article Cover Image Generator

功能：
1. 自动触发头图生成
2. 按"文章标题+日期"命名
3. 保存至指定文件夹
4. 记录日志
5. 错误处理与重试机制

作者：TS爱心联盟技术团队
版本：v2.0.0
日期：2026-06-07
"""

import os
import sys
import json
import logging
import time
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import threading
import queue

# 尝试导入所需模块
try:
    from doubao_image_generator import generate_image
    DOUBÃO_AVAILABLE = True
except ImportError:
    DOUBÃO_AVAILABLE = False
    print("⚠️ 警告：豆包图像生成模块不可用")

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("⚠️ 警告：requests模块不可用")


@dataclass
class CoverGenerationTask:
    """头图生成任务"""
    task_id: str
    article_title: str
    article_dir: str
    prompt: str
    size: str = "16:9"
    quality: str = "high"
    created_at: str = ""
    status: str = "pending"  # pending, processing, completed, failed
    result: Optional[Dict] = None
    error: Optional[str] = None
    retry_count: int = 0
    max_retries: int = 3


@dataclass
class GenerationResult:
    """生成结果"""
    success: bool
    path: str = ""
    filename: str = ""
    size: int = 0
    format: str = "JPG"
    dimensions: str = ""
    url: str = ""
    error: Optional[str] = None
    generation_time: float = 0


class CoverImageGenerator:
    """头图生成器"""
    
    def __init__(self, base_dir: str = "E:/Trac Project/02-文化自信"):
        self.base_dir = Path(base_dir)
        self.images_dir = self.base_dir / "images"
        self.logs_dir = self.base_dir / "logs" / "cover_generation"
        self.config_file = self.base_dir / "cover_config.json"
        
        # 确保目录存在
        self.images_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        
        # 配置日志
        self._setup_logging()
        
        # 任务队列
        self.task_queue = queue.Queue()
        self.processing = False
        
        # 加载配置
        self.config = self._load_config()
        
        logger.info("=" * 60)
        logger.info("🎨 头图自动化生成系统初始化完成")
        logger.info(f"📁 基础目录：{self.base_dir}")
        logger.info(f"📁 图片目录：{self.images_dir}")
        logger.info(f"📁 日志目录：{self.logs_dir}")
        logger.info("=" * 60)
    
    def _setup_logging(self):
        """设置日志系统"""
        global logger
        
        log_file = self.logs_dir / f"generation_{datetime.now().strftime('%Y%m%d')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        logger = logging.getLogger(__name__)
    
    def _load_config(self) -> Dict:
        """加载配置文件"""
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # 默认配置
            default_config = {
                "default_size": "16:9",
                "default_quality": "high",
                "max_retries": 3,
                "retry_delay": 5,
                "image_format": "JPG",
                "dimensions": {
                    "16:9": {"width": 1200, "height": 630},
                    "1:1": {"width": 1080, "height": 1080}
                },
                "generation_templates": {}
            }
            self._save_config(default_config)
            return default_config
    
    def _save_config(self, config: Dict):
        """保存配置文件"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
    
    def _generate_task_id(self, article_title: str) -> str:
        """生成任务ID"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        hash_input = f"{article_title}_{timestamp}"
        hash_value = hashlib.md5(hash_input.encode()).hexdigest()[:8]
        return f"task_{timestamp}_{hash_value}"
    
    def _sanitize_filename(self, filename: str) -> str:
        """清理文件名，移除非法字符"""
        illegal_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        for char in illegal_chars:
            filename = filename.replace(char, '_')
        return filename
    
    def create_task(self, article_title: str, article_dir: str, 
                    prompt: str, size: str = "16:9") -> str:
        """
        创建头图生成任务
        
        Args:
            article_title: 文章标题
            article_dir: 文章目录
            prompt: 图像生成提示词
            size: 图像尺寸比例
            
        Returns:
            task_id: 任务ID
        """
        task_id = self._generate_task_id(article_title)
        
        task = CoverGenerationTask(
            task_id=task_id,
            article_title=article_title,
            article_dir=article_dir,
            prompt=prompt,
            size=size,
            created_at=datetime.now().isoformat()
        )
        
        self.task_queue.put(task)
        
        logger.info(f"📝 任务已创建：{task_id}")
        logger.info(f"   文章标题：{article_title}")
        logger.info(f"   保存目录：{article_dir}")
        logger.info(f"   图像尺寸：{size}")
        
        return task_id
    
    def generate_cover(self, article_title: str, article_dir: str,
                      prompt: str, size: str = "16:9",
                      save_dir: Optional[str] = None) -> GenerationResult:
        """
        生成头图
        
        Args:
            article_title: 文章标题
            article_dir: 文章目录
            prompt: 生成提示词
            size: 图像尺寸
            save_dir: 保存目录
            
        Returns:
            GenerationResult: 生成结果
        """
        start_time = time.time()
        
        # 清理文件名
        safe_title = self._sanitize_filename(article_title)
        
        # 确定保存目录
        if save_dir:
            target_dir = Path(save_dir)
        else:
            target_dir = self.images_dir / f"{safe_title}_images"
        
        target_dir.mkdir(parents=True, exist_ok=True)
        
        # 生成文件名：标题+日期+时间戳
        date_str = datetime.now().strftime('%Y%m%d')
        time_str = datetime.now().strftime('%H%M%S')
        filename = f"{safe_title}_{date_str}_{time_str}.jpg"
        save_path = target_dir / filename
        
        logger.info("=" * 60)
        logger.info(f"🎨 开始生成头图")
        logger.info(f"   文章标题：{article_title}")
        logger.info(f"   保存路径：{save_path}")
        logger.info(f"   图像尺寸：{size}")
        logger.info("=" * 60)
        
        # 生成图像
        if DOUBÃO_AVAILABLE and REQUESTS_AVAILABLE:
            for retry in range(self.config['max_retries']):
                try:
                    logger.info(f"🔄 尝试 {retry + 1}/{self.config['max_retries']}")
                    
                    # 调用豆包API生成图像
                    image_url = generate_image(
                        prompt=prompt,
                        size=size,
                        quality=self.config['default_quality']
                    )
                    
                    # 下载图像
                    response = requests.get(image_url, timeout=30)
                    
                    if response.status_code == 200:
                        with open(save_path, 'wb') as f:
                            f.write(response.content)
                        
                        file_size = os.path.getsize(save_path)
                        
                        result = GenerationResult(
                            success=True,
                            path=str(save_path),
                            filename=filename,
                            size=file_size,
                            format=self.config['image_format'],
                            dimensions=size,
                            url=image_url,
                            generation_time=time.time() - start_time
                        )
                        
                        self._log_result(result)
                        return result
                    else:
                        raise Exception(f"下载失败，HTTP状态码：{response.status_code}")
                        
                except Exception as e:
                    logger.warning(f"⚠️ 第{retry + 1}次尝试失败：{str(e)}")
                    if retry < self.config['max_retries'] - 1:
                        time.sleep(self.config['retry_delay'])
                    else:
                        result = GenerationResult(
                            success=False,
                            error=str(e),
                            generation_time=time.time() - start_time
                        )
                        self._log_result(result)
                        return result
        else:
            # 使用占位符图像
            logger.warning("⚠️ 使用占位符图像（模块不可用）")
            result = self._create_placeholder(save_path, safe_title)
            result.generation_time = time.time() - start_time
            self._log_result(result)
            return result
    
    def _create_placeholder(self, save_path: Path, title: str) -> GenerationResult:
        """创建占位符图像"""
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            # 获取尺寸配置
            dims = self.config['dimensions'].get('16:9', {'width': 1200, 'height': 630})
            width, height = dims['width'], dims['height']
            
            # 创建图像
            img = Image.new('RGB', (width, height), color=(26, 35, 126))
            draw = ImageDraw.Draw(img)
            
            # 绘制太极图
            center_x, center_y = width // 2, height // 2 - 50
            radius = 150
            
            draw.ellipse(
                [center_x - radius, center_y - radius,
                 center_x + radius, center_y + radius],
                outline=(201, 162, 39),
                width=3
            )
            
            # 标题区域
            title_y = height - 100
            draw.rectangle(
                [0, title_y, width, height],
                fill=(0, 0, 0, 180)
            )
            
            # 文字
            try:
                font = ImageFont.truetype("arial.ttf", 48)
                font_small = ImageFont.truetype("arial.ttf", 24)
            except:
                font = ImageFont.load_default()
                font_small = font
            
            draw.text((width // 2, title_y + 35), title,
                     fill=(255, 255, 255), font=font, anchor='mm')
            
            img.save(save_path, 'JPEG', quality=95)
            
            return GenerationResult(
                success=True,
                path=str(save_path),
                filename=save_path.name,
                size=os.path.getsize(save_path),
                format='JPG',
                dimensions='1200×630'
            )
            
        except ImportError:
            return GenerationResult(
                success=False,
                error="PIL库不可用，无法创建占位符"
            )
    
    def _log_result(self, result: GenerationResult):
        """记录生成结果"""
        logger.info("=" * 60)
        logger.info("📋 生成结果")
        logger.info("=" * 60)
        
        if result.success:
            logger.info(f"✅ 状态：成功")
            logger.info(f"📁 文件：{result.filename}")
            logger.info(f"💾 路径：{result.path}")
            logger.info(f"📊 大小：{result.size / 1024:.2f} KB")
            logger.info(f"🎨 格式：{result.format}")
            logger.info(f"📐 尺寸：{result.dimensions}")
            logger.info(f"⏱️ 用时：{result.generation_time:.2f}秒")
        else:
            logger.error(f"❌ 状态：失败")
            logger.error(f"💬 错误：{result.error}")
            logger.error(f"⏱️ 用时：{result.generation_time:.2f}秒")
        
        logger.info("=" * 60)
    
    def batch_generate(self, tasks: List[Dict]) -> List[GenerationResult]:
        """
        批量生成头图
        
        Args:
            tasks: 任务列表，每项包含article_title, article_dir, prompt
            
        Returns:
            List[GenerationResult]: 生成结果列表
        """
        results = []
        
        logger.info(f"\n{'=' * 60}")
        logger.info(f"📦 开始批量生成，共{len(tasks)}个任务")
        logger.info(f"{'=' * 60}\n")
        
        for i, task in enumerate(tasks, 1):
            logger.info(f"\n📝 任务 {i}/{len(tasks)}")
            logger.info(f"{'-' * 40}")
            
            result = self.generate_cover(
                article_title=task['article_title'],
                article_dir=task['article_dir'],
                prompt=task['prompt'],
                size=task.get('size', '16:9')
            )
            
            results.append(result)
            
            # 任务间隔
            if i < len(tasks):
                time.sleep(2)
        
        # 批量结果汇总
        success_count = sum(1 for r in results if r.success)
        fail_count = len(results) - success_count
        
        logger.info(f"\n{'=' * 60}")
        logger.info(f"📊 批量生成完成")
        logger.info(f"   总任务：{len(results)}")
        logger.info(f"   成功：{success_count}")
        logger.info(f"   失败：{fail_count}")
        logger.info(f"{'=' * 60}\n")
        
        return results


class ArticleCoverWorkflow:
    """文章头图工作流"""
    
    def __init__(self):
        self.generator = CoverImageGenerator()
    
    def create_article_cover(self, article_title: str, article_dir: str,
                             style: str = "quantum_taiji") -> GenerationResult:
        """
        为文章创建头图
        
        Args:
            article_title: 文章标题
            article_dir: 文章目录
            style: 风格类型
            
        Returns:
            GenerationResult: 生成结果
        """
        # 根据风格生成提示词
        prompt = self._generate_prompt(article_title, style)
        
        return self.generator.generate_cover(
            article_title=article_title,
            article_dir=article_dir,
            prompt=prompt
        )
    
    def _generate_prompt(self, article_title: str, style: str) -> str:
        """根据风格生成提示词"""
        
        base_template = """
        【设计风格】
        高端学术风格，融合现代科学与传统文化元素
        
        【构图要求】
        - 中心：核心视觉元素
        - 背景：渐变深邃背景
        - 预留标题区域（底部20%）
        
        【技术规格】
        - 尺寸：1200×630像素（16:9）
        - 分辨率：300dpi
        - 模式：RGB
        - 格式：JPG
        """
        
        style_templates = {
            "quantum_taiji": """
            【核心视觉】
            - 中心：太极图与量子旋量融合图形
            - 背景：量子场论波形与粒子效果
            - 配色：深蓝(#1a237e) + 金色(#c9a227) + 太极红(#8B1E22)
            
            【标题文字】
            - 主标题：{title}
            - 副标题："Spinor-Taiji model"系列
            
            【整体风格】
            - 科技感与禅意融合
            - 专业性与视觉美感兼顾
            """.format(title=article_title),
            
            "three_realms": """
            【核心视觉】
            - 三层递进构图，代表"看山三境界"
            - 第一层（底部）：具象山峰 - "看山是山"
            - 第二层（中部）：旋量图形 - "看山不是山"
            - 第三层（顶部）：抽象山峰剪影 - "看山还是山"
            
            【配色方案】
            - 主色：深蓝 + 金色
            - 辅色：太极红 + 量子蓝
            - 背景：星空渐变
            
            【标题】
            - 主标题：{title}
            - 副标题：从矢量到旋量到觉知
            
            【风格】
            - 学术性与禅意融合
            - 构图平衡大气
            """.format(title=article_title),
            
            "vibration": """
            【核心视觉】
            - 振动波形与曼陀罗图案
            - 中心：宁静的光球（象征空性）
            - 周围：声波/光波振动效果
            
            【配色】
            - 天青蓝 + 金色
            - 深邃背景渐变
            
            【标题】
            - 主标题：{title}
            
            【风格】
            - 专业性与禅意融合
            - 宁静智慧氛围
            """.format(title=article_title)
        }
        
        prompt = base_template + style_templates.get(style, style_templates["quantum_taiji"])
        
        return prompt


def main():
    """主函数 - 演示自动化流程"""
    
    print("\n" + "=" * 60)
    print("🎨 微信公众号文章头图自动化生成系统")
    print("=" * 60 + "\n")
    
    # 创建工作流
    workflow = ArticleCoverWorkflow()
    
    # 示例：生成"看山三境界"头图
    print("📝 示例任务：为「看山三境界」生成头图")
    print("-" * 60)
    
    result = workflow.create_article_cover(
        article_title="看山三境界",
        article_dir="Spinor-Taiji model",
        style="three_realms"
    )
    
    if result.success:
        print(f"\n✅ 头图生成成功！")
        print(f"📁 文件：{result.filename}")
        print(f"💾 路径：{result.path}")
        print(f"📊 大小：{result.size / 1024:.2f} KB")
        print(f"⏱️ 用时：{result.generation_time:.2f}秒")
    else:
        print(f"\n❌ 头图生成失败")
        print(f"💬 错误：{result.error}")
        print("\n🔄 请检查配置并重试")
    
    print("\n" + "=" * 60)
    print("🎉 演示完成")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
