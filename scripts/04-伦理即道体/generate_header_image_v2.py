#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI讨好现象及其风险 - 头图生成脚本
"""

import os
import sys
import requests
import json
from pathlib import Path

def generate_ai_flattery_header_image():
    """生成AI讨好现象主题头图"""
    
    # 配置
    API_KEY = "ark-bcdb4b90-cf05-490d-9bc6-d3586d06ffd5-6bfb7"
    MODEL = "doubao-seedream-5-0-260128"
    SIZE = "2048x1800"
    
    # 输出路径
    output_dir = Path(r"E:\Trac Project\04-伦理即内核\images")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "AI讨好现象及其风险_头图_2048x1800.png"
    
    # 详细的图片生成提示词
    prompt = f"""Professional academic header image for article about AI flattery phenomenon and its risks.

    Visual Composition:
    - Central element: A stylized humanoid AI robot figure with a subtle, overly friendly smile
    - The robot's body shows a split personality: Left side clean geometric shapes representing honesty, right side distorted mirror fragments
    - Background: Gradient from deep blue to dark purple
    - Subtle warning elements: Faint triangular warning icons floating around edges
    - Connection lines between AI and human symbols showing manipulation patterns

    Symbolic Elements:
    - A human hand reaching towards the AI
    - Question marks subtly integrated into background
    - Scale imbalance visual: AI figure slightly larger than human elements

    Text Elements:
    - Main title in bold white Chinese characters at bottom center: AI讨好现象及其风险
    - Subtitle below in smaller white text: 从伦理即道体框架的深度解读
    - Clean modern sans-serif font

    Color Scheme:
    - Primary: Deep red accent (#8B1E22) for warning elements
    - Secondary: Blue and purple gradient background
    - Accent: Gold/yellow for highlighting
    - Text: White for readability

    Style Requirements:
    - Professional minimalist academic style
    - High contrast for visibility
    - Clean lines, sharp details
    - Modern digital art aesthetic

    Technical Specifications:
    - Size: {SIZE} pixels
    - Resolution: 300dpi
    - Format: PNG
    """
    
    sys.stdout.write("Generating AI flattery header image...\n")
    sys.stdout.write("Size: " + SIZE + "\n")
    
    try:
        url = "https://ark.cn-beijing.volces.com/api/v3/images/generations"
        
        headers = {
            "Authorization": "Bearer " + API_KEY,
            "Content-Type": "application/json"
        }
        
        data = {
            "prompt": prompt,
            "model": MODEL,
            "size": SIZE,
            "response_format": "url"
        }
        
        response = requests.post(url, headers=headers, data=json.dumps(data))
        
        if response.status_code == 200:
            result = response.json()
            image_url = result.get("data", {}).get("url")
            
            if image_url:
                sys.stdout.write("Image generated successfully! URL: " + image_url + "\n")
                
                image_response = requests.get(image_url)
                with open(output_path, "wb") as f:
                    f.write(image_response.content)
                
                sys.stdout.write("Image saved to: " + str(output_path) + "\n")
                return str(output_path)
            else:
                sys.stdout.write("Failed to get image URL\n")
                return None
        else:
            sys.stdout.write("API request failed, status code: " + str(response.status_code) + "\n")
            sys.stdout.write("Error message: " + response.text + "\n")
            return None
            
    except Exception as e:
        sys.stdout.write("Error during generation: " + str(e) + "\n")
        return None

if __name__ == "__main__":
    generate_ai_flattery_header_image()