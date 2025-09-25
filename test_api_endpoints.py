#!/usr/bin/env python3
"""
测试API端点并获取真实数据
"""

import requests
import json

def test_api():
    base_url = "http://127.0.0.1:8000"
    
    print("🔍 测试API端点...")
    
    # 测试健康检查
    try:
        response = requests.get(f"{base_url}/health")
        print(f"✅ Health: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Health failed: {e}")
    
    # 测试统计信息
    try:
        response = requests.get(f"{base_url}/kg/stats")
        print(f"✅ Stats: {response.status_code}")
        data = response.json()
        print(f"   Response: {data}")
        if data.get('ok'):
            print(f"   📊 统计数据: {data.get('data', {})}")
    except Exception as e:
        print(f"❌ Stats failed: {e}")
    
    # 测试词典
    try:
        response = requests.get(f"{base_url}/kg/dictionary")
        print(f"✅ Dictionary: {response.status_code}")
        data = response.json()
        print(f"   Response keys: {list(data.keys()) if isinstance(data, dict) else type(data)}")
        if isinstance(data, dict) and 'data' in data:
            dict_data = data['data']
            if isinstance(dict_data, dict):
                print(f"   📚 词典类别: {list(dict_data.keys())}")
                for category, items in dict_data.items():
                    if isinstance(items, list):
                        print(f"      {category}: {len(items)} 条目")
    except Exception as e:
        print(f"❌ Dictionary failed: {e}")
    
    # 测试文件上传端点
    try:
        response = requests.get(f"{base_url}/kg/upload")
        print(f"✅ Upload endpoint: {response.status_code}")
    except Exception as e:
        print(f"❌ Upload endpoint failed: {e}")

if __name__ == "__main__":
    test_api()
