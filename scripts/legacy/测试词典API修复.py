#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import time

def test_api_endpoints():
    """测试API端点"""
    print("🧪 测试词典API修复效果")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    
    # 等待API启动
    print("⏳ 等待API服务启动...")
    for i in range(10):
        try:
            response = requests.get(f"{base_url}/health", timeout=3)
            if response.status_code == 200:
                print("✅ API服务已启动")
                break
        except:
            time.sleep(2)
    else:
        print("❌ API服务启动超时")
        return False
    
    # 测试端点
    endpoints = [
        ("/kg/dictionary", "词典数据"),
        ("/kg/dictionary/entries", "词典条目"),
        ("/kg/real-stats", "实时统计"),
        ("/kg/graph-data", "图谱数据")
    ]
    
    results = {}
    
    for endpoint, name in endpoints:
        print(f"\n🔍 测试 {name} ({endpoint})")
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if endpoint == "/kg/dictionary":
                    total = data.get('total', 0)
                    message = data.get('message', '')
                    print(f"✅ {name}: {total} 条数据")
                    print(f"   消息: {message}")
                    
                    # 显示前几条数据样本
                    if data.get('data') and len(data['data']) > 0:
                        sample = data['data'][0]
                        print(f"   样本: {sample}")
                    
                    results[endpoint] = {'status': 'success', 'count': total}
                
                elif endpoint == "/kg/dictionary/entries":
                    entries = data.get('data', {}).get('entries', [])
                    total = len(entries)
                    print(f"✅ {name}: {total} 条条目")
                    
                    if entries:
                        sample = entries[0]
                        print(f"   样本: {dict(list(sample.items())[:3])}")
                    
                    results[endpoint] = {'status': 'success', 'count': total}
                
                elif endpoint == "/kg/real-stats":
                    stats = data.get('data', {}).get('stats', {})
                    total_nodes = stats.get('totalNodes', 0)
                    total_dict = stats.get('totalDictionary', 0)
                    total_relations = stats.get('totalRelations', 0)
                    
                    print(f"✅ {name}: 节点{total_nodes}, 词典{total_dict}, 关系{total_relations}")
                    print(f"   消息: {data.get('message', '')}")
                    
                    results[endpoint] = {
                        'status': 'success', 
                        'nodes': total_nodes,
                        'dictionary': total_dict,
                        'relations': total_relations
                    }
                
                elif endpoint == "/kg/graph-data":
                    graph_data = data.get('data', {})
                    nodes = graph_data.get('nodes', [])
                    edges = graph_data.get('edges', [])
                    
                    print(f"✅ {name}: {len(nodes)} 节点, {len(edges)} 边")
                    print(f"   消息: {data.get('message', '')}")
                    
                    results[endpoint] = {
                        'status': 'success',
                        'nodes': len(nodes),
                        'edges': len(edges)
                    }
                
            else:
                print(f"❌ {name}: HTTP {response.status_code}")
                results[endpoint] = {'status': 'error', 'code': response.status_code}
                
        except Exception as e:
            print(f"❌ {name}: 连接失败 - {e}")
            results[endpoint] = {'status': 'failed', 'error': str(e)}
    
    return results

def analyze_results(results):
    """分析测试结果"""
    print("\n" + "=" * 50)
    print("📊 测试结果分析")
    print("=" * 50)
    
    # 检查词典数据
    dict_endpoint = results.get('/kg/dictionary', {})
    dict_count = dict_endpoint.get('count', 0)
    
    entries_endpoint = results.get('/kg/dictionary/entries', {})
    entries_count = entries_endpoint.get('count', 0)
    
    stats_endpoint = results.get('/kg/real-stats', {})
    neo4j_dict_count = stats_endpoint.get('dictionary', 0)
    neo4j_nodes = stats_endpoint.get('nodes', 0)
    neo4j_relations = stats_endpoint.get('relations', 0)
    
    print(f"词典数据源:")
    print(f"  - API词典文件: {dict_count} 条")
    print(f"  - 词典条目: {entries_count} 条")
    print(f"  - Neo4j词典节点: {neo4j_dict_count} 个")
    print(f"  - Neo4j总节点: {neo4j_nodes} 个")
    print(f"  - Neo4j关系: {neo4j_relations} 个")
    
    # 问题诊断
    print(f"\n🔍 问题诊断:")
    
    if dict_count > 1000:
        print("✅ API词典文件数据正常 (>1000条)")
    elif dict_count > 0:
        print(f"⚠️ API词典文件数据较少 ({dict_count}条)")
    else:
        print("❌ API词典文件无数据")
    
    if neo4j_dict_count > 100:
        print("✅ Neo4j词典节点数据正常")
    elif neo4j_dict_count > 0:
        print(f"⚠️ Neo4j词典节点较少 ({neo4j_dict_count}个)")
    else:
        print("❌ Neo4j词典节点无数据")
    
    if neo4j_relations > 0:
        print("✅ Neo4j关系数据正常")
    else:
        print("❌ Neo4j关系数据缺失")
    
    # 修复建议
    print(f"\n💡 修复建议:")
    
    if dict_count > 0 and neo4j_dict_count == 0:
        print("1. 文件数据存在但Neo4j无词典节点")
        print("   - 需要将文件数据导入Neo4j")
        print("   - 检查数据导入脚本")
    
    if dict_count == 0:
        print("1. API词典文件缺失或为空")
        print("   - 检查api/data/dictionary.json文件")
        print("   - 从其他数据源重新生成")
    
    if neo4j_nodes > 0 and neo4j_dict_count == 0:
        print("2. Neo4j有节点但无Dictionary标签")
        print("   - 现有节点可能使用Component/Symptom/Tool标签")
        print("   - API已更新查询这些实际标签")

def main():
    """主函数"""
    print("🔧 词典API修复测试")
    print("=" * 60)
    
    # 测试API端点
    results = test_api_endpoints()
    
    if results:
        # 分析结果
        analyze_results(results)
        
        # 保存结果
        with open('词典API测试结果.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"\n📄 测试结果已保存: 词典API测试结果.json")
    
    print(f"\n🌐 访问地址:")
    print(f"- API文档: http://localhost:8000/docs")
    print(f"- 词典数据: http://localhost:8000/kg/dictionary")
    print(f"- 前端应用: http://localhost:5173")

if __name__ == "__main__":
    main()
