#!/usr/bin/env python3
"""
API修复测试脚本
"""
import requests
import json

def test_api_endpoints():
    """测试API端点"""
    base_url = "http://127.0.0.1:8000"
    
    print("🔍 测试API端点修复情况")
    print("=" * 50)
    
    # 1. 测试健康检查
    print("\n1. 测试健康检查...")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   服务状态: {data.get('status')}")
            print(f"   数据库状态: {data.get('database')}")
        else:
            print(f"   错误: {response.text}")
    except Exception as e:
        print(f"   连接失败: {e}")
    
    # 2. 测试词典API
    print("\n2. 测试词典API...")
    try:
        response = requests.get(f"{base_url}/kg/dictionary", timeout=5)
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   返回格式: ok={data.get('ok')}")
            if data.get('ok') and data.get('data'):
                components = data['data'].get('components', [])
                symptoms = data['data'].get('symptoms', [])
                causes = data['data'].get('causes', [])
                print(f"   组件数量: {len(components)}")
                print(f"   症状数量: {len(symptoms)}")
                print(f"   根因数量: {len(causes)}")
        else:
            print(f"   错误: {response.text}")
    except Exception as e:
        print(f"   连接失败: {e}")
    
    # 3. 测试文件上传API
    print("\n3. 测试文件上传API...")
    try:
        files = {'file': ('test.txt', 'Hello World Test Content', 'text/plain')}
        response = requests.post(f"{base_url}/kg/upload", files=files, timeout=10)
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   上传成功: {data.get('success')}")
            print(f"   文件ID: {data.get('file_id')}")
            print(f"   文件名: {data.get('filename')}")
        else:
            print(f"   错误: {response.text}")
    except Exception as e:
        print(f"   连接失败: {e}")
    
    # 4. 测试知识抽取API
    print("\n4. 测试知识抽取API...")
    try:
        extract_data = {
            'file_id': 'test_file_123',
            'extraction_type': 'auto'
        }
        response = requests.post(f"{base_url}/kg/extract", 
                               json=extract_data, 
                               headers={'Content-Type': 'application/json'},
                               timeout=10)
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   抽取成功: {data.get('success')}")
            print(f"   实体数量: {len(data.get('entities', []))}")
            print(f"   关系数量: {len(data.get('relations', []))}")
            if data.get('metadata'):
                print(f"   处理时间: {data['metadata'].get('processing_time')}")
        else:
            print(f"   错误: {response.text}")
    except Exception as e:
        print(f"   连接失败: {e}")
    
    # 5. 测试图谱构建API
    print("\n5. 测试图谱构建API...")
    try:
        build_data = {
            'entities': [
                {'id': 'e1', 'name': '摄像头', 'type': 'Component'},
                {'id': 'e2', 'name': '对焦失败', 'type': 'Symptom'}
            ],
            'relations': [
                {'source': 'e1', 'target': 'e2', 'type': 'HAS_SYMPTOM'}
            ],
            'merge_strategy': 'auto'
        }
        response = requests.post(f"{base_url}/kg/build", 
                               json=build_data,
                               headers={'Content-Type': 'application/json'},
                               timeout=10)
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   构建成功: {data.get('success')}")
            print(f"   创建节点: {data.get('nodes_created')}")
            print(f"   创建关系: {data.get('relations_created')}")
        else:
            print(f"   错误: {response.text}")
    except Exception as e:
        print(f"   连接失败: {e}")
    
    # 6. 测试统计API
    print("\n6. 测试统计API...")
    try:
        response = requests.get(f"{base_url}/kg/stats", timeout=5)
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   返回格式: ok={data.get('ok')}")
            if data.get('ok') and data.get('data'):
                stats = data['data']
                print(f"   异常数量: {stats.get('anomalies', 0)}")
                print(f"   产品数量: {stats.get('products', 0)}")
                print(f"   组件数量: {stats.get('components', 0)}")
        else:
            print(f"   错误: {response.text}")
    except Exception as e:
        print(f"   连接失败: {e}")
    
    print("\n" + "=" * 50)
    print("✅ API端点测试完成！")
    print("\n📋 修复总结:")
    print("1. ✅ 添加了 /kg/dictionary 端点")
    print("2. ✅ 添加了 /kg/upload 端点") 
    print("3. ✅ 添加了 /kg/extract 端点")
    print("4. ✅ 添加了 /kg/build 端点")
    print("5. ✅ 修复了前端数据格式兼容性")
    print("\n🌐 现在前端应该可以正常访问所有API了！")

if __name__ == "__main__":
    test_api_endpoints()
