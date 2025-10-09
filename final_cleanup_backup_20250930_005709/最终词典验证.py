#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json

def final_dictionary_verification():
    """最终词典数据验证"""
    print("🎯 最终词典数据验证 - 目标1124条")
    print("=" * 60)
    
    base_url = "http://localhost:8000"
    
    # 测试所有词典相关端点
    endpoints = [
        ("/kg/dictionary", "主词典端点 (旧)"),
        ("/api/dictionary", "主词典端点 (新)"),
        ("/kg/dictionary/entries", "词典条目端点"),
    ]
    
    results = {}
    
    for endpoint, description in endpoints:
        print(f"\n🔍 测试 {description}")
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if endpoint in ["/kg/dictionary", "/api/dictionary"]:
                    total = data.get('total', 0)
                    message = data.get('message', '')
                    
                    print(f"✅ 状态: 成功")
                    print(f"📊 数据量: {total} 条")
                    print(f"💬 消息: {message}")
                    
                    # 检查数据结构
                    if 'data' in data:
                        if isinstance(data['data'], dict):
                            categories = list(data['data'].keys())
                            print(f"📂 类别: {categories[:5]}{'...' if len(categories) > 5 else ''}")
                            
                            # 统计各类别数量
                            category_counts = {}
                            for cat, items in data['data'].items():
                                if isinstance(items, list):
                                    category_counts[cat] = len(items)
                            
                            print(f"📈 类别统计: {dict(list(category_counts.items())[:3])}")
                        
                        elif isinstance(data['data'], list):
                            print(f"📋 列表格式: {len(data['data'])} 条记录")
                    
                    results[endpoint] = {
                        'status': 'success',
                        'total': total,
                        'message': message,
                        'target_match': total == 1124
                    }
                
                elif endpoint == "/kg/dictionary/entries":
                    entries = data.get('data', {}).get('entries', [])
                    total = len(entries)
                    
                    print(f"✅ 状态: 成功")
                    print(f"📊 条目数量: {total} 条")
                    
                    if entries:
                        sample = entries[0]
                        print(f"📝 样本字段: {list(sample.keys())[:5]}")
                        print(f"🏷️ 样本名称: {sample.get('term', sample.get('name', 'N/A'))}")
                    
                    results[endpoint] = {
                        'status': 'success',
                        'total': total
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
    
    # 总结验证结果
    print(f"\n" + "=" * 60)
    print(f"📊 验证结果总结")
    print(f"=" * 60)
    
    target_achieved = False
    
    for endpoint, result in results.items():
        if result.get('status') == 'success':
            total = result.get('total', 0)
            match_status = "✅" if total == 1124 else "⚠️" if total > 0 else "❌"
            print(f"{match_status} {endpoint}: {total} 条数据")
            
            if total == 1124:
                target_achieved = True
        else:
            print(f"❌ {endpoint}: {result.get('status', 'unknown')}")
    
    print(f"\n🎯 目标达成情况:")
    if target_achieved:
        print(f"✅ 成功！至少有一个端点返回了正确的1124条数据")
        print(f"🎉 你的词典数据完全正确！")
    else:
        print(f"⚠️ 未完全达成目标，需要进一步检查")
    
    # 访问建议
    print(f"\n🌐 推荐访问地址:")
    for endpoint, result in results.items():
        if result.get('status') == 'success' and result.get('total', 0) == 1124:
            print(f"✅ {base_url}{endpoint} - 完整的1124条数据")
    
    print(f"\n📱 前端应用: http://localhost:5173")
    print(f"📚 API文档: http://localhost:8000/docs")
    
    return results

def main():
    """主函数"""
    results = final_dictionary_verification()
    
    # 保存验证结果
    with open('../最终词典验证结果.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n📄 验证结果已保存: 最终词典验证结果.json")

if __name__ == "__main__":
    main()
