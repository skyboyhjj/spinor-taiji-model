import os

# 需要修复的文件列表
files_to_fix = [
    r"articles\《道德经》第一章 旋量-太极读解_微信公众号专业版.html",
    r"docs\00-产品宪法\慧惠数字生命  最高产品宪法v2.0.0.md",
    r"docs\01-核心模型\03-道境坐标系\道境坐标系 v2.0：旋量-太极动态导航系统.md",
    r"docs\01-核心模型\04-伦理即道体\「伦理即道体」理念落地指南  宪法合规性审查报告.md",
    r"docs\02-经典读解\《道德经》第七十九章 旋量-太极读解.md",
    r"docs\04-阅读指南\Spinor-Taiji model：阅读地图与实修指南.md",
    r"docs\05-五步读解法\《道德经》五步协同读解报告 动力机制分析汇总.md",
    r"media\images\旋量-太极读解道德经_第一章 知行合一实践指南.png"
]

def fix_filename(filepath):
    """修复文件名中的空格"""
    dirname = os.path.dirname(filepath)
    filename = os.path.basename(filepath)
    
    # 将空格替换为下划线
    new_filename = filename.replace(' ', '_')
    new_filepath = os.path.join(dirname, new_filename)
    
    return new_filepath

def main():
    print("=" * 60)
    print("批量修复空格文件名")
    print("=" * 60)
    
    print("\n待修复文件清单:")
    print("-" * 60)
    
    for filepath in files_to_fix:
        if os.path.exists(filepath):
            new_path = fix_filename(filepath)
            print(f" {filepath}")
            print(f"   {new_path}")
            os.rename(filepath, new_path)
        else:
            print(f" {filepath} - 文件不存在")
    
    print("\n" + "=" * 60)
    print("修复完成！")
    print("=" * 60)

if __name__ == '__main__':
    main()
