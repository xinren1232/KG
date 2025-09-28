#!/usr/bin/env python3
"""
测试图谱API修复
验证前端API调用问题是否已解决
"""

import requests
import json
import sys

def test_api_endpoint(url, description):
    """测试API端点"""
    print(f"\n🧪 测试: {description}")
    print(f"📡 URL: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        print(f"✅ 状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and 'stats' in data['data']:
                stats = data['data']['stats']
                print(f"📊 统计数据:")
                print(f"   - 词条数量: {stats.get('totalNodes', 0)}")
                print(f"   - 关系数量: {stats.get('totalRelations', 0)}")
                print(f"   - 分类数量: {stats.get('totalCategories', 0)}")
                print(f"   - 标签数量: {stats.get('totalTags', 0)}")
                
                nodes_count = len(data['data'].get('nodes', []))
                relations_count = len(data['data'].get('relations', []))
                print(f"🎯 可视化数据:")
                print(f"   - 节点数量: {nodes_count}")
                print(f"   - 关系数量: {relations_count}")
                
                return True
            else:
                print(f"⚠️ 响应数据格式异常")
                return False
        else:
            print(f"❌ 请求失败: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 网络错误: {e}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ JSON解析错误: {e}")
        return False

def main():
    """主测试函数"""
    print("🔧 图谱API修复验证测试")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    
    # 测试用例
    test_cases = [
        {
            "url": f"{base_url}/kg/graph",
            "description": "默认参数 (应该使用limit=100)"
        },
        {
            "url": f"{base_url}/kg/graph?limit=50",
            "description": "指定limit=50"
        },
        {
            "url": f"{base_url}/kg/graph?show_all=true",
            "description": "显示所有节点 (show_all=true)"
        },
        {
            "url": f"{base_url}/kg/graph?show_all=true&limit=1000",
            "description": "显示所有节点且limit=1000 (前端实际调用)"
        },
        {
            "url": f"{base_url}/kg/graph?show_all=false&limit=100",
            "description": "限制显示 (show_all=false)"
        }
    ]
    
    # 执行测试
    success_count = 0
    total_count = len(test_cases)
    
    for test_case in test_cases:
        if test_api_endpoint(test_case["url"], test_case["description"]):
            success_count += 1
    
    # 测试错误情况
    print(f"\n🧪 测试: 错误参数处理")
    print(f"📡 URL: {base_url}/kg/graph?show_all=invalid")
    try:
        response = requests.get(f"{base_url}/kg/graph?show_all=invalid", timeout=5)
        if response.status_code == 422:
            print(f"✅ 正确返回422错误 (参数验证失败)")
            success_count += 1
        else:
            print(f"❌ 期望422错误，实际返回: {response.status_code}")
    except Exception as e:
        print(f"❌ 测试错误: {e}")
    
    total_count += 1
    
    # 测试不存在的路径
    print(f"\n🧪 测试: 不存在的路径")
    print(f"📡 URL: {base_url}/kg/graph/data")
    try:
        response = requests.get(f"{base_url}/kg/graph/data", timeout=5)
        if response.status_code == 404:
            print(f"✅ 正确返回404错误 (路径不存在)")
            success_count += 1
        else:
            print(f"❌ 期望404错误，实际返回: {response.status_code}")
    except Exception as e:
        print(f"❌ 测试错误: {e}")
    
    total_count += 1
    
    # 总结
    print("\n" + "=" * 50)
    print(f"📋 测试总结:")
    print(f"✅ 成功: {success_count}/{total_count}")
    print(f"❌ 失败: {total_count - success_count}/{total_count}")
    
    if success_count == total_count:
        print(f"\n🎉 所有测试通过！图谱API修复成功！")
        return 0
    else:
        print(f"\n⚠️ 部分测试失败，需要进一步检查")
        return 1

if __name__ == "__main__":
    sys.exit(main())
