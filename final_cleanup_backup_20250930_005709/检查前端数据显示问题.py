#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import time

def check_api_endpoints_detailed():
    """详细检查API端点数据"""
    print("🔍 详细检查API端点数据")
    print("=" * 60)
    
    base_url = "http://localhost:8000"
    
    # 检查所有词典相关端点
    endpoints = [
        ("/kg/dictionary", "主词典端点"),
        ("/api/dictionary", "新词典端点"),
        ("/kg/dictionary/entries", "词典条目端点 (默认分页)"),
        ("/kg/dictionary/entries?page=1&page_size=100", "词典条目端点 (100条)"),
        ("/kg/dictionary/entries?page=1&page_size=1000", "词典条目端点 (1000条)"),
        ("/kg/dictionary/entries?page=1&page_size=2000", "词典条目端点 (2000条)"),
    ]
    
    results = {}
    
    for endpoint, description in endpoints:
        print(f"\n📊 测试 {description}")
        print(f"   URL: {base_url}{endpoint}")
        
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                # 分析数据结构
                if endpoint.startswith("/kg/dictionary/entries"):
                    # 词典条目端点
                    entries = data.get('data', {}).get('entries', [])
                    total = data.get('data', {}).get('total', len(entries))
                    page = data.get('data', {}).get('page', 1)
                    page_size = data.get('data', {}).get('page_size', len(entries))
                    
                    print(f"✅ 状态: 成功")
                    print(f"📊 返回条目: {len(entries)} 条")
                    print(f"📈 总数: {total} 条")
                    print(f"📄 分页: 第{page}页, 每页{page_size}条")
                    
                    if entries:
                        sample = entries[0]
                        print(f"📝 样本字段: {list(sample.keys())}")
                        print(f"🏷️ 样本名称: {sample.get('term', sample.get('name', 'N/A'))}")
                    
                    results[endpoint] = {
                        'status': 'success',
                        'returned_count': len(entries),
                        'total_count': total,
                        'page': page,
                        'page_size': page_size
                    }
                
                elif endpoint in ["/kg/dictionary", "/api/dictionary"]:
                    # 主词典端点
                    total = data.get('total', 0)
                    
                    if isinstance(data.get('data'), dict):
                        # 分类格式
                        categories = list(data['data'].keys())
                        category_counts = {cat: len(items) if isinstance(items, list) else 0 
                                         for cat, items in data['data'].items()}
                        actual_total = sum(category_counts.values())
                        
                        print(f"✅ 状态: 成功")
                        print(f"📊 声明总数: {total} 条")
                        print(f"📊 实际总数: {actual_total} 条")
                        print(f"📂 类别数: {len(categories)}")
                        print(f"📈 类别统计: {dict(list(category_counts.items())[:3])}")
                        
                        results[endpoint] = {
                            'status': 'success',
                            'declared_total': total,
                            'actual_total': actual_total,
                            'categories': len(categories),
                            'category_counts': category_counts
                        }
                    
                    elif isinstance(data.get('data'), list):
                        # 列表格式
                        actual_count = len(data['data'])
                        
                        print(f"✅ 状态: 成功")
                        print(f"📊 声明总数: {total} 条")
                        print(f"📊 实际总数: {actual_count} 条")
                        
                        if data['data']:
                            sample = data['data'][0]
                            print(f"📝 样本字段: {list(sample.keys())}")
                        
                        results[endpoint] = {
                            'status': 'success',
                            'declared_total': total,
                            'actual_total': actual_count
                        }
                
            else:
                print(f"❌ HTTP错误: {response.status_code}")
                results[endpoint] = {
                    'status': 'error',
                    'code': response.status_code
                }
                
        except Exception as e:
            print(f"❌ 连接失败: {e}")
            results[endpoint] = {
                'status': 'failed',
                'error': str(e)
            }
    
    return results

def check_frontend_api_calls():
    """检查前端可能调用的API"""
    print("\n🌐 检查前端可能调用的API")
    print("=" * 60)
    
    # 前端可能调用的API端点
    frontend_apis = [
        ("/kg/dictionary", "前端主词典API"),
        ("/kg/dictionary/entries", "前端词典条目API"),
        ("/kg/dictionary/categories", "前端词典类别API"),
        ("/kg/dictionary/statistics", "前端词典统计API"),
        ("/kg/real-stats", "前端实时统计API"),
        ("/kg/graph-data", "前端图谱数据API"),
    ]
    
    base_url = "http://localhost:8000"
    
    for endpoint, description in frontend_apis:
        print(f"\n📱 测试 {description}")
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # 简化的数据分析
                if 'total' in data:
                    print(f"✅ 响应正常: {data.get('total', 'N/A')} 条数据")
                elif 'data' in data:
                    if isinstance(data['data'], list):
                        print(f"✅ 响应正常: {len(data['data'])} 条数据")
                    elif isinstance(data['data'], dict):
                        if 'entries' in data['data']:
                            print(f"✅ 响应正常: {len(data['data']['entries'])} 条条目")
                        else:
                            print(f"✅ 响应正常: 字典格式数据")
                    else:
                        print(f"✅ 响应正常: 其他格式数据")
                else:
                    print(f"✅ 响应正常: 无数据计数")
                
                # 检查消息
                if 'message' in data:
                    print(f"💬 消息: {data['message']}")
                    
            else:
                print(f"❌ HTTP错误: {response.status_code}")
                
        except Exception as e:
            print(f"❌ 连接失败: {e}")

def analyze_pagination_issue():
    """分析分页问题"""
    print("\n🔍 分析分页问题")
    print("=" * 60)
    
    base_url = "http://localhost:8000"
    
    # 测试不同的分页参数
    test_cases = [
        ("默认分页", "/kg/dictionary/entries"),
        ("第1页50条", "/kg/dictionary/entries?page=1&page_size=50"),
        ("第1页100条", "/kg/dictionary/entries?page=1&page_size=100"),
        ("第1页500条", "/kg/dictionary/entries?page=1&page_size=500"),
        ("第1页1124条", "/kg/dictionary/entries?page=1&page_size=1124"),
        ("第1页2000条", "/kg/dictionary/entries?page=1&page_size=2000"),
        ("无分页限制", "/kg/dictionary/entries?size=10000"),
    ]
    
    for description, endpoint in test_cases:
        print(f"\n📄 测试 {description}")
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                if 'data' in data and 'entries' in data['data']:
                    entries = data['data']['entries']
                    total = data['data'].get('total', len(entries))
                    
                    print(f"✅ 返回: {len(entries)} 条")
                    print(f"📊 总数: {total} 条")
                    
                    if len(entries) == 1124:
                        print(f"🎯 完美！返回了全部1124条数据")
                    elif len(entries) == 50:
                        print(f"⚠️ 只返回50条，可能是默认分页限制")
                    elif len(entries) < total:
                        print(f"⚠️ 返回数据少于总数，存在分页限制")
                else:
                    print(f"❌ 数据格式异常")
                    
            else:
                print(f"❌ HTTP错误: {response.status_code}")
                
        except Exception as e:
            print(f"❌ 请求失败: {e}")

def suggest_frontend_fix():
    """建议前端修复方案"""
    print("\n💡 前端修复建议")
    print("=" * 60)
    
    print("🔍 问题分析:")
    print("  前端只显示50条数据，可能的原因:")
    print("  1. 前端使用默认分页参数 (page_size=50)")
    print("  2. 前端没有请求全部数据")
    print("  3. 前端使用了错误的API端点")
    print("  4. 前端数据处理逻辑有限制")
    
    print("\n🔧 修复方案:")
    print("  1. 检查前端API调用参数:")
    print("     - 使用 page_size=1124 或更大值")
    print("     - 使用 size=10000 参数")
    print("     - 或者实现分页加载全部数据")
    
    print("  2. 推荐API端点:")
    print("     - /kg/dictionary/entries?page_size=1124")
    print("     - /kg/dictionary/entries?size=10000")
    print("     - /api/dictionary (返回全部1124条)")
    
    print("  3. 前端代码检查:")
    print("     - 检查 Vue 组件中的 API 调用")
    print("     - 检查数据加载逻辑")
    print("     - 检查分页组件配置")

def main():
    """主函数"""
    print("🔍 检查前端数据显示问题 - 目标1124条")
    print("=" * 80)
    
    # 1. 详细检查API端点
    api_results = check_api_endpoints_detailed()
    
    # 2. 检查前端可能调用的API
    check_frontend_api_calls()
    
    # 3. 分析分页问题
    analyze_pagination_issue()
    
    # 4. 提供修复建议
    suggest_frontend_fix()
    
    # 5. 总结
    print("\n" + "=" * 80)
    print("📊 问题诊断总结")
    print("=" * 80)
    
    # 检查是否有端点能返回全部数据
    full_data_available = False
    
    for endpoint, result in api_results.items():
        if result.get('status') == 'success':
            if 'actual_total' in result and result['actual_total'] == 1124:
                print(f"✅ {endpoint}: 可以返回全部1124条数据")
                full_data_available = True
            elif 'returned_count' in result and result['returned_count'] == 1124:
                print(f"✅ {endpoint}: 可以返回全部1124条数据")
                full_data_available = True
            elif 'returned_count' in result and result['returned_count'] == 50:
                print(f"⚠️ {endpoint}: 只返回50条数据 (分页限制)")
    
    if full_data_available:
        print(f"\n🎯 结论: API可以返回全部1124条数据")
        print(f"💡 问题在于前端调用时的参数或数据处理逻辑")
        print(f"🔧 建议: 检查前端代码中的API调用参数")
    else:
        print(f"\n⚠️ 结论: API端点存在分页限制")
        print(f"🔧 建议: 修改API端点以支持返回全部数据")
    
    # 保存结果
    with open('../前端数据显示问题检查报告.json', 'w', encoding='utf-8') as f:
        json.dump(api_results, f, ensure_ascii=False, indent=2)
    
    print(f"\n📄 详细报告已保存: 前端数据显示问题检查报告.json")

if __name__ == "__main__":
    main()
