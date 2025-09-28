#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速验证API数据 - 检查API返回的数据总数和路径唯一性
"""

import requests
import json

def test_api_data():
    """测试API数据"""
    print("🔍 测试API数据...")
    
    try:
        # 测试主要端点
        response = requests.get("http://localhost:8000/kg/dictionary/entries?page=1&page_size=1", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success") and "data" in data:
                total = data["data"].get("total", 0)
                entries = data["data"].get("entries", [])
                
                print(f"✅ API正常工作")
                print(f"📊 总数据量: {total} 条")
                print(f"📊 返回条目: {len(entries)} 条")
                
                if entries:
                    entry = entries[0]
                    print(f"📊 示例数据:")
                    print(f"  词条: {entry.get('term', 'N/A')}")
                    print(f"  类型: {entry.get('type', 'N/A')}")
                    print(f"  类别: {entry.get('category', 'N/A')}")
                
                return True, total
            else:
                print(f"❌ API返回错误: {data}")
                return False, 0
        else:
            print(f"❌ HTTP错误: {response.status_code}")
            return False, 0
            
    except Exception as e:
        print(f"❌ API测试失败: {e}")
        return False, 0

def test_search_function():
    """测试搜索功能"""
    print("🔍 测试搜索功能...")
    
    search_terms = ["显示屏", "电池", "传感器"]
    
    for term in search_terms:
        try:
            response = requests.get(f"http://localhost:8000/kg/dictionary/entries?search={term}&page_size=3", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    entries = data["data"].get("entries", [])
                    print(f"  '{term}': {len(entries)} 条结果")
                    
                    for entry in entries[:2]:
                        print(f"    - {entry.get('term', 'N/A')}")
                else:
                    print(f"  '{term}': 搜索失败")
            else:
                print(f"  '{term}': HTTP {response.status_code}")
                
        except Exception as e:
            print(f"  '{term}': 异常 - {e}")

def check_data_files():
    """检查数据文件"""
    print("📁 检查数据文件...")
    
    from pathlib import Path
    
    files = [
        "api/data/dictionary.json",
        "api/data/dictionary_stats.json",
        "unified_final_dictionary/dictionary.json",
        "unified_final_dictionary/statistics.json"
    ]
    
    for file_path in files:
        path = Path(file_path)
        if path.exists():
            size = path.stat().st_size
            print(f"  ✅ {file_path}: {size:,} bytes")
            
            # 如果是JSON文件，检查内容
            if file_path.endswith('.json') and 'dictionary.json' in file_path:
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    if isinstance(data, list):
                        print(f"    📊 包含 {len(data)} 条记录")
                    elif isinstance(data, dict) and 'total_terms' in data:
                        print(f"    📊 统计: {data['total_terms']} 条")
                except Exception as e:
                    print(f"    ❌ 读取失败: {e}")
        else:
            print(f"  ❌ {file_path}: 文件不存在")

def check_path_uniqueness():
    """检查路径唯一性"""
    print("🔍 检查API路径唯一性...")
    
    # 测试所有可能的API端点
    endpoints = [
        "/kg/dictionary/entries",
        "/api/dictionary", 
        "/kg/dictionary",
        "/dictionary"
    ]
    
    working_endpoints = []
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"http://localhost:8000{endpoint}?page_size=1", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") or data.get("ok"):
                    working_endpoints.append(endpoint)
                    print(f"  ✅ {endpoint}: 可用")
                else:
                    print(f"  ⚠️ {endpoint}: 返回错误")
            else:
                print(f"  ❌ {endpoint}: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ {endpoint}: 连接失败")
    
    print(f"📊 可用端点: {len(working_endpoints)} 个")
    
    if len(working_endpoints) == 1:
        print(f"✅ 路径唯一: {working_endpoints[0]}")
        return working_endpoints[0]
    elif len(working_endpoints) > 1:
        print(f"⚠️ 多个路径可用，可能存在冲突: {working_endpoints}")
        return working_endpoints[0]
    else:
        print(f"❌ 没有可用的API端点")
        return None

def main():
    """主函数"""
    print("🚀 快速验证API数据")
    print("=" * 40)
    
    # 1. 检查数据文件
    check_data_files()
    
    # 2. 测试API数据
    api_ok, total = test_api_data()
    
    # 3. 测试搜索功能
    if api_ok:
        test_search_function()
    
    # 4. 检查路径唯一性
    unique_path = check_path_uniqueness()
    
    print("\n" + "=" * 40)
    print("📊 验证结果:")
    print(f"API状态: {'✅ 正常' if api_ok else '❌ 异常'}")
    print(f"数据总量: {total} 条")
    print(f"唯一路径: {unique_path if unique_path else '❌ 无'}")
    
    if api_ok and total > 1000:
        print("✅ 数据统一汇总成功！")
        print("💡 现在可以访问前端验证显示效果")
        print("🌐 前端地址: http://localhost:5173")
    elif api_ok and total > 0:
        print(f"⚠️ 数据量较少，当前只有 {total} 条")
    else:
        print("❌ API或数据存在问题")
    
    print(f"\n📋 前端应该显示: {total} 条数据")

if __name__ == "__main__":
    main()
