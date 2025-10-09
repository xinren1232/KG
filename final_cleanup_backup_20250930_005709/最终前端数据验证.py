#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import time

def test_frontend_api_calls():
    """测试前端实际调用的API"""
    print("🔍 测试前端实际调用的API")
    print("=" * 60)
    
    base_url = "http://localhost:8000"
    
    # 测试前端修复后的API调用
    test_cases = [
        {
            "name": "前端词典管理页面API",
            "url": f"{base_url}/kg/dictionary/entries?page_size=1124",
            "description": "EnhancedDictionaryManagement.vue 调用"
        },
        {
            "name": "前端词典管理API (通过kgApi)",
            "url": f"{base_url}/kg/dictionary/entries?page_size=1124",
            "description": "DictionaryManagement.vue 通过 kgApi.getDictionary 调用"
        },
        {
            "name": "主词典端点 (完整数据)",
            "url": f"{base_url}/kg/dictionary",
            "description": "主词典端点，返回分类数据"
        },
        {
            "name": "新词典端点 (完整数据)",
            "url": f"{base_url}/api/dictionary",
            "description": "新词典端点，返回列表数据"
        }
    ]
    
    results = []
    
    for test_case in test_cases:
        print(f"\n📊 测试: {test_case['name']}")
        print(f"   URL: {test_case['url']}")
        print(f"   说明: {test_case['description']}")
        
        try:
            response = requests.get(test_case['url'], timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                # 分析数据
                if 'data' in data and 'entries' in data['data']:
                    # 词典条目格式
                    entries = data['data']['entries']
                    total = data['data'].get('total', len(entries))
                    
                    print(f"✅ 成功: 返回 {len(entries)} 条数据")
                    print(f"📊 总数: {total} 条")
                    
                    if len(entries) == 1124:
                        print(f"🎯 完美！返回了全部1124条数据")
                        status = "perfect"
                    elif len(entries) >= 1000:
                        print(f"✅ 很好！返回了大部分数据")
                        status = "good"
                    elif len(entries) >= 100:
                        print(f"⚠️ 一般：返回了部分数据")
                        status = "partial"
                    else:
                        print(f"❌ 问题：返回数据太少")
                        status = "poor"
                    
                    results.append({
                        'name': test_case['name'],
                        'status': status,
                        'returned': len(entries),
                        'total': total,
                        'success': True
                    })
                
                elif 'data' in data and isinstance(data['data'], dict):
                    # 分类格式
                    categories = list(data['data'].keys())
                    total_items = 0
                    for cat, items in data['data'].items():
                        if isinstance(items, list):
                            total_items += len(items)
                    
                    declared_total = data.get('total', total_items)
                    
                    print(f"✅ 成功: {len(categories)} 个类别")
                    print(f"📊 实际数据: {total_items} 条")
                    print(f"📊 声明总数: {declared_total} 条")
                    
                    if total_items == 1124:
                        print(f"🎯 完美！包含全部1124条数据")
                        status = "perfect"
                    else:
                        print(f"⚠️ 数据量不匹配")
                        status = "partial"
                    
                    results.append({
                        'name': test_case['name'],
                        'status': status,
                        'returned': total_items,
                        'total': declared_total,
                        'success': True
                    })
                
                elif 'data' in data and isinstance(data['data'], list):
                    # 列表格式
                    items = data['data']
                    declared_total = data.get('total', len(items))
                    
                    print(f"✅ 成功: 返回 {len(items)} 条数据")
                    print(f"📊 声明总数: {declared_total} 条")
                    
                    if len(items) == 1124:
                        print(f"🎯 完美！返回了全部1124条数据")
                        status = "perfect"
                    else:
                        print(f"⚠️ 数据量不匹配")
                        status = "partial"
                    
                    results.append({
                        'name': test_case['name'],
                        'status': status,
                        'returned': len(items),
                        'total': declared_total,
                        'success': True
                    })
                
                else:
                    print(f"⚠️ 未知数据格式")
                    results.append({
                        'name': test_case['name'],
                        'status': 'unknown',
                        'success': True
                    })
                
            else:
                print(f"❌ HTTP错误: {response.status_code}")
                results.append({
                    'name': test_case['name'],
                    'status': 'error',
                    'error': response.status_code,
                    'success': False
                })
                
        except Exception as e:
            print(f"❌ 连接失败: {e}")
            results.append({
                'name': test_case['name'],
                'status': 'failed',
                'error': str(e),
                'success': False
            })
    
    return results

def test_frontend_access():
    """测试前端页面访问"""
    print("\n🌐 测试前端页面访问")
    print("=" * 60)
    
    try:
        response = requests.get('http://localhost:5173', timeout=10)
        if response.status_code == 200:
            print("✅ 前端页面访问正常")
            return True
        else:
            print(f"❌ 前端页面访问异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 前端页面访问失败: {e}")
        return False

def main():
    """主函数"""
    print("🎯 最终前端数据验证 - 修复后测试")
    print("=" * 80)
    
    # 1. 测试前端页面访问
    frontend_ok = test_frontend_access()
    
    # 2. 测试API调用
    api_results = test_frontend_api_calls()
    
    # 3. 总结结果
    print("\n" + "=" * 80)
    print("📊 修复验证总结")
    print("=" * 80)
    
    perfect_count = sum(1 for r in api_results if r.get('status') == 'perfect')
    good_count = sum(1 for r in api_results if r.get('status') == 'good')
    success_count = sum(1 for r in api_results if r.get('success', False))
    
    print(f"📈 API测试结果:")
    print(f"  - 完美 (1124条): {perfect_count} 个端点")
    print(f"  - 良好 (1000+条): {good_count} 个端点")
    print(f"  - 成功响应: {success_count}/{len(api_results)} 个端点")
    
    if perfect_count >= 2:
        print(f"\n🎉 修复成功！")
        print(f"✅ 前端现在可以获取完整的1124条词典数据")
        print(f"✅ 多个API端点都能正确返回全部数据")
        
        if frontend_ok:
            print(f"✅ 前端页面访问正常")
            print(f"\n🌐 请访问以下地址验证:")
            print(f"  - 前端应用: http://localhost:5173")
            print(f"  - 词典管理: http://localhost:5173/#/dictionary")
            print(f"  - 增强词典管理: http://localhost:5173/#/enhanced-dictionary")
        else:
            print(f"⚠️ 前端页面访问异常，请检查前端服务")
    
    elif perfect_count >= 1:
        print(f"\n✅ 部分修复成功")
        print(f"⚠️ 部分API端点仍需要进一步调整")
    
    else:
        print(f"\n❌ 修复未完成")
        print(f"⚠️ 需要进一步检查API端点和前端代码")
    
    # 4. 详细结果
    print(f"\n📋 详细测试结果:")
    for result in api_results:
        status_icon = {
            'perfect': '🎯',
            'good': '✅',
            'partial': '⚠️',
            'poor': '❌',
            'error': '❌',
            'failed': '❌',
            'unknown': '❓'
        }.get(result.get('status'), '❓')
        
        name = result['name']
        if result.get('success'):
            returned = result.get('returned', 'N/A')
            total = result.get('total', 'N/A')
            print(f"  {status_icon} {name}: {returned}/{total} 条数据")
        else:
            error = result.get('error', 'unknown')
            print(f"  {status_icon} {name}: 失败 - {error}")
    
    print(f"\n💡 下一步建议:")
    if perfect_count >= 2 and frontend_ok:
        print(f"  1. 访问前端页面验证词典数据显示")
        print(f"  2. 检查词典管理功能是否正常")
        print(f"  3. 验证搜索和筛选功能")
    else:
        print(f"  1. 检查前端服务状态")
        print(f"  2. 验证API端点响应")
        print(f"  3. 检查前端代码中的API调用")

if __name__ == "__main__":
    main()
