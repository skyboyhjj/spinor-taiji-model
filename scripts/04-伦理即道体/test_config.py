#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证配置文件的可访问性
"""

import os
import sys

def load_env(env_path='.env'):
    """从.env文件加载环境变量"""
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()
        return True
    return False

def test_config():
    """测试配置文件是否正确加载"""
    print("=" * 60)
    print("🔍 验证配置文件可访问性")
    print("=" * 60)
    print()
    
    # 加载配置
    env_path = '.env'
    print(f"1. 尝试加载配置文件: {env_path}")
    if load_env(env_path):
        print(f"   ✅ 配置文件加载成功")
    else:
        print(f"   ❌ 配置文件加载失败")
        return False
    
    # 检查配置项
    print("\n2. 验证配置项:")
    required_keys = ['WECHAT_APP_ID', 'WECHAT_APP_SECRET', 'API_KEY', 'MODEL']
    all_valid = True
    
    for key in required_keys:
        value = os.getenv(key)
        if value:
            masked = value[:8] + '*' * (len(value) - 8) if len(value) > 8 else value
            print(f"   ✅ {key}: {masked}")
        else:
            print(f"   ❌ {key}: 未设置")
            all_valid = False
    
    # 验证配置格式
    print("\n3. 验证配置格式:")
    app_id = os.getenv('WECHAT_APP_ID')
    app_secret = os.getenv('WECHAT_APP_SECRET')
    
    if app_id and app_id.startswith('wx') and len(app_id) == 18:
        print(f"   ✅ WECHAT_APP_ID 格式正确")
    else:
        print(f"   ⚠️ WECHAT_APP_ID 格式可能不正确")
    
    if app_secret and len(app_secret) == 32:
        print(f"   ✅ WECHAT_APP_SECRET 格式正确")
    else:
        print(f"   ⚠️ WECHAT_APP_SECRET 格式可能不正确")
    
    # 测试读取配置文件内容
    print("\n4. 测试直接读取配置文件:")
    try:
        with open('.env', 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.strip().split('\n')
            print(f"   ✅ 配置文件内容读取成功")
            print(f"   配置项数量: {len([l for l in lines if l.strip() and not l.strip().startswith('#')])}")
    except Exception as e:
        print(f"   ❌ 读取配置文件失败: {e}")
        all_valid = False
    
    print("\n" + "=" * 60)
    if all_valid:
        print("🎉 配置验证通过！")
        print("   应用程序可以正确读取配置值。")
    else:
        print("⚠️ 部分配置验证未通过，请检查配置文件。")
    
    print("=" * 60)
    return all_valid

if __name__ == "__main__":
    success = test_config()
    sys.exit(0 if success else 1)