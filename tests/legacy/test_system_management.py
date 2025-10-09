#!/usr/bin/env python3
"""
测试系统管理相关的API端点
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_api_endpoint(endpoint, description):
    """测试API端点"""
    try:
        url = f"{BASE_URL}{endpoint}"
        print(f"\n🔍 测试 {description}")
        print(f"URL: {url}")
        
        response = requests.get(url, timeout=10)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 成功: {json.dumps(data, ensure_ascii=False, indent=2)[:200]}...")
            return True
        else:
            print(f"❌ 失败: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 连接错误: {e}")
        return False
    except Exception as e:
        print(f"❌ 其他错误: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始测试系统管理API端点...")
    
    # 测试的端点列表
    endpoints = [
        ("/", "根路径"),
        ("/api/dictionary", "字典数据"),
        ("/api/dictionary/labels", "字典标签"),
        ("/kg/real-stats", "系统统计"),
        ("/kg/graph-data", "图谱数据"),
        ("/kg/dictionary", "旧版字典API"),
    ]
    
    success_count = 0
    total_count = len(endpoints)
    
    for endpoint, description in endpoints:
        if test_api_endpoint(endpoint, description):
            success_count += 1
    
    print(f"\n📊 测试结果: {success_count}/{total_count} 个端点正常")
    
    if success_count == total_count:
        print("🎉 所有API端点测试通过！")
    else:
        print("⚠️ 部分API端点存在问题")

if __name__ == "__main__":
    main()
