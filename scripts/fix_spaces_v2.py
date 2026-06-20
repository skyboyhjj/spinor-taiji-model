import os
from pathlib import Path

print("修复文件名中的空格...")
print("=" * 60)

files_to_fix = [
    r"docs\00-产品宪法\慧惠数字生命  最高产品宪法v2.0.0.md",
    r"docs\01-核心模型\04-伦理即道体\「伦理即道体」理念落地指南  宪法合规性审查报告.md"
]

fixed_count = 0
for filepath in files_to_fix:
    path = Path(filepath)
    if path.exists():
        new_name = path.name.replace(' ', '_').replace('  ', '_')
        new_path = path.parent / new_name
        path.rename(new_path)
        print(f"OK {path.name}")
        print(f"   -> {new_name}")
        fixed_count += 1
    else:
        print(f"SKIP: {filepath} - not found")

print()
print("=" * 60)
print(f"Done: Fixed {fixed_count} files")
print("=" * 60)
