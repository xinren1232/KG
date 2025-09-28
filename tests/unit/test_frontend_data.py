#!/usr/bin/env python3
"""
测试前端数据获取
模拟前端调用API获取真实数据
"""

import requests
import json

def test_frontend_apis():
    base_url = "http://127.0.0.1:8000"
    
    print("🎨 测试前端数据获取...")
    
    # 1. 首页统计数据
    print("\n📊 首页统计数据:")
    try:
        # 获取图谱统计
        stats_response = requests.get(f"{base_url}/kg/stats")
        if stats_response.status_code == 200:
            stats_data = stats_response.json()
            print(f"   Stats API: {stats_data}")
            
            if stats_data.get('ok') and stats_data.get('data'):
                data = stats_data['data']
                total_nodes = (data.get('anomalies', 0) + data.get('products', 0) + 
                              data.get('components', 0) + data.get('symptoms', 0))
                print(f"   📈 总节点数: {total_nodes}")
            else:
                print(f"   ❌ Stats failed: {stats_data.get('error', {}).get('message', 'Unknown error')}")
        
        # 获取词典统计
        dict_response = requests.get(f"{base_url}/kg/dictionary")
        if dict_response.status_code == 200:
            dict_data = dict_response.json()
            if dict_data.get('ok') and dict_data.get('data'):
                data = dict_data['data']
                total_entries = 0
                for category, items in data.items():
                    if isinstance(items, list):
                        total_entries += len(items)
                        print(f"   📚 {category}: {len(items)} 条目")
                print(f"   📚 总词典条目: {total_entries}")
            else:
                print(f"   ❌ Dictionary failed: {dict_data.get('error', {}).get('message', 'Unknown error')}")
                
    except Exception as e:
        print(f"   ❌ 首页数据获取失败: {e}")
    
    # 2. 数据治理页面数据
    print("\n🏛️ 数据治理页面数据:")
    try:
        # 统计信息
        stats_response = requests.get(f"{base_url}/kg/stats")
        if stats_response.status_code == 200:
            stats_data = stats_response.json()
            if stats_data.get('ok') and stats_data.get('data'):
                data = stats_data['data']
                print(f"   📊 异常数: {data.get('anomalies', 0)}")
                print(f"   📊 产品数: {data.get('products', 0)}")
                print(f"   📊 组件数: {data.get('components', 0)}")
                print(f"   📊 症状数: {data.get('symptoms', 0)}")
        
        # 词典数据
        dict_response = requests.get(f"{base_url}/kg/dictionary")
        if dict_response.status_code == 200:
            dict_data = dict_response.json()
            if dict_data.get('ok') and dict_data.get('data'):
                data = dict_data['data']
                if 'components' in data:
                    print(f"   🔧 组件词典: {len(data['components'])} 条目")
                    if data['components']:
                        sample = data['components'][0]
                        print(f"      示例: {sample.get('name', 'N/A')} - {sample.get('description', 'N/A')}")
                        
    except Exception as e:
        print(f"   ❌ 数据治理数据获取失败: {e}")
    
    # 3. 图谱探索页面数据
    print("\n🕸️ 图谱探索页面数据:")
    try:
        # 测试因果路径查询
        cause_path_data = {
            "symptom_name": "黑屏",
            "max_depth": 5,
            "include_countermeasures": True
        }
        
        response = requests.post(f"{base_url}/kg/cause_path", json=cause_path_data)
        print(f"   因果路径API状态: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   因果路径响应: {result}")
        else:
            print(f"   因果路径API暂不可用 (这是正常的，因为需要数据库连接)")
            
    except Exception as e:
        print(f"   ❌ 图谱探索数据获取失败: {e}")
    
    # 4. 词典管理页面数据
    print("\n📚 词典管理页面数据:")
    try:
        dict_response = requests.get(f"{base_url}/kg/dictionary")
        if dict_response.status_code == 200:
            dict_data = dict_response.json()
            if dict_data.get('ok') and dict_data.get('data'):
                data = dict_data['data']
                print(f"   📖 可用词典类别: {list(data.keys())}")
                
                for category, items in data.items():
                    if isinstance(items, list) and items:
                        print(f"   📝 {category} 示例:")
                        for i, item in enumerate(items[:3]):  # 显示前3个
                            print(f"      {i+1}. {item.get('name', 'N/A')} - {item.get('description', 'N/A')[:50]}...")
                        if len(items) > 3:
                            print(f"      ... 还有 {len(items) - 3} 个条目")
                            
    except Exception as e:
        print(f"   ❌ 词典管理数据获取失败: {e}")

if __name__ == "__main__":
    test_frontend_apis()
