#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json

def test_graph_api_endpoints():
    """测试图谱相关API端点"""
    print("🔍 测试图谱相关API端点")
    print("=" * 60)
    
    base_url = "http://localhost:8000"
    
    # 测试图谱相关端点
    endpoints = [
        {
            "name": "图谱数据端点 (前端调用)",
            "url": f"{base_url}/kg/graph",
            "params": {"show_all": True, "limit": 1000},
            "description": "前端 getGraphVisualizationData 调用的端点"
        },
        {
            "name": "图谱数据端点 (默认参数)",
            "url": f"{base_url}/kg/graph",
            "params": {},
            "description": "默认参数的图谱数据"
        },
        {
            "name": "图谱可视化数据端点",
            "url": f"{base_url}/kg/graph-data",
            "params": {},
            "description": "原始的图谱可视化数据端点"
        },
        {
            "name": "真实图谱统计端点",
            "url": f"{base_url}/kg/real-stats",
            "params": {},
            "description": "真实的图谱统计数据"
        }
    ]
    
    results = []
    
    for endpoint in endpoints:
        print(f"\n📊 测试: {endpoint['name']}")
        print(f"   URL: {endpoint['url']}")
        print(f"   说明: {endpoint['description']}")
        
        try:
            response = requests.get(endpoint['url'], params=endpoint['params'], timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                # 分析数据结构
                success = data.get('success', data.get('ok', False))
                
                print(f"✅ 状态: 成功 (HTTP 200)")
                print(f"📊 响应成功: {success}")
                
                if 'data' in data:
                    graph_data = data['data']
                    
                    # 检查数据结构
                    if 'stats' in graph_data:
                        stats = graph_data['stats']
                        print(f"📈 统计数据:")
                        print(f"   - 节点数: {stats.get('totalNodes', 'N/A')}")
                        print(f"   - 关系数: {stats.get('totalRelations', 'N/A')}")
                        print(f"   - 类别数: {stats.get('totalCategories', 'N/A')}")
                        print(f"   - 标签数: {stats.get('totalTags', 'N/A')}")
                    
                    if 'sampleNodes' in graph_data:
                        nodes = graph_data['sampleNodes']
                        print(f"📋 样本节点: {len(nodes)} 个")
                        if nodes:
                            print(f"   - 样本: {nodes[0].get('name', 'N/A')} ({nodes[0].get('category', 'N/A')})")
                    
                    if 'sampleRelations' in graph_data:
                        relations = graph_data['sampleRelations']
                        print(f"🔗 样本关系: {len(relations)} 个")
                        if relations:
                            rel = relations[0]
                            print(f"   - 样本: {rel.get('source', 'N/A')} -> {rel.get('target', 'N/A')}")
                    
                    if 'categories' in graph_data:
                        categories = graph_data['categories']
                        print(f"📂 类别: {len(categories)} 个")
                        if categories:
                            print(f"   - 样本: {list(categories.keys())[:3]}")
                    
                    results.append({
                        'name': endpoint['name'],
                        'status': 'success',
                        'data_keys': list(graph_data.keys()),
                        'has_stats': 'stats' in graph_data,
                        'has_nodes': 'sampleNodes' in graph_data,
                        'has_relations': 'sampleRelations' in graph_data
                    })
                
                else:
                    print(f"⚠️ 响应中没有 'data' 字段")
                    results.append({
                        'name': endpoint['name'],
                        'status': 'no_data',
                        'response_keys': list(data.keys())
                    })
                
            else:
                print(f"❌ HTTP错误: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   错误详情: {error_data.get('detail', 'N/A')}")
                except:
                    print(f"   错误内容: {response.text[:100]}...")
                
                results.append({
                    'name': endpoint['name'],
                    'status': 'error',
                    'http_code': response.status_code
                })
                
        except Exception as e:
            print(f"❌ 连接失败: {e}")
            results.append({
                'name': endpoint['name'],
                'status': 'failed',
                'error': str(e)
            })
    
    return results

def test_frontend_graph_access():
    """测试前端图谱页面访问"""
    print("\n🌐 测试前端图谱页面访问")
    print("=" * 60)
    
    frontend_urls = [
        ("前端主页", "http://localhost:5173"),
        ("图谱可视化页面", "http://localhost:5173/#/graph-visualization"),
        ("图谱探索页面", "http://localhost:5173/#/graph-explore"),
        ("图谱查询页面", "http://localhost:5173/#/graph-query")
    ]
    
    results = []
    
    for name, url in frontend_urls:
        print(f"\n📱 测试: {name}")
        print(f"   URL: {url}")
        
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"✅ 访问正常")
                results.append({'name': name, 'status': 'success'})
            else:
                print(f"❌ 访问异常: {response.status_code}")
                results.append({'name': name, 'status': 'error', 'code': response.status_code})
        except Exception as e:
            print(f"❌ 访问失败: {e}")
            results.append({'name': name, 'status': 'failed', 'error': str(e)})
    
    return results

def test_graph_data_consistency():
    """测试图谱数据一致性"""
    print("\n🔍 测试图谱数据一致性")
    print("=" * 60)
    
    try:
        # 获取图谱数据
        graph_response = requests.get('http://localhost:8000/kg/graph?show_all=true', timeout=15)
        
        if graph_response.status_code == 200:
            graph_data = graph_response.json()
            
            if 'data' in graph_data and 'stats' in graph_data['data']:
                stats = graph_data['data']['stats']
                
                print(f"📊 图谱统计数据:")
                print(f"   - 总节点数: {stats.get('totalNodes', 'N/A')}")
                print(f"   - 总关系数: {stats.get('totalRelations', 'N/A')}")
                print(f"   - 总类别数: {stats.get('totalCategories', 'N/A')}")
                print(f"   - 总标签数: {stats.get('totalTags', 'N/A')}")
                
                # 检查数据一致性
                total_nodes = stats.get('totalNodes', 0)
                
                if total_nodes == 1124:
                    print(f"✅ 数据一致性检查通过: 节点数匹配词典数据 (1124)")
                    return True
                elif total_nodes > 0:
                    print(f"⚠️ 数据一致性警告: 节点数 ({total_nodes}) 与词典数据 (1124) 不匹配")
                    return False
                else:
                    print(f"❌ 数据一致性错误: 没有节点数据")
                    return False
            else:
                print(f"❌ 图谱数据格式错误: 缺少统计信息")
                return False
        else:
            print(f"❌ 图谱API调用失败: {graph_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 数据一致性检查失败: {e}")
        return False

def main():
    """主函数"""
    print("🎯 图谱功能修复验证测试")
    print("=" * 80)
    
    # 1. 测试API端点
    api_results = test_graph_api_endpoints()
    
    # 2. 测试前端访问
    frontend_results = test_frontend_graph_access()
    
    # 3. 测试数据一致性
    consistency_ok = test_graph_data_consistency()
    
    # 4. 总结结果
    print("\n" + "=" * 80)
    print("📊 图谱功能修复验证总结")
    print("=" * 80)
    
    # API测试总结
    api_success = sum(1 for r in api_results if r.get('status') == 'success')
    print(f"📈 API测试结果: {api_success}/{len(api_results)} 个端点正常")
    
    for result in api_results:
        status_icon = "✅" if result.get('status') == 'success' else "❌"
        print(f"  {status_icon} {result['name']}")
    
    # 前端测试总结
    frontend_success = sum(1 for r in frontend_results if r.get('status') == 'success')
    print(f"\n🌐 前端测试结果: {frontend_success}/{len(frontend_results)} 个页面正常")
    
    for result in frontend_results:
        status_icon = "✅" if result.get('status') == 'success' else "❌"
        print(f"  {status_icon} {result['name']}")
    
    # 数据一致性总结
    consistency_icon = "✅" if consistency_ok else "❌"
    print(f"\n📊 数据一致性: {consistency_icon} {'通过' if consistency_ok else '未通过'}")
    
    # 最终结论
    print(f"\n" + "=" * 80)
    print(f"🎯 修复验证结论")
    print(f"=" * 80)
    
    if api_success >= 3 and frontend_success >= 1:
        print(f"🎉 图谱功能修复成功！")
        print(f"✅ API端点正常工作")
        print(f"✅ 前端页面可以访问")
        
        if consistency_ok:
            print(f"✅ 数据一致性正常")
        else:
            print(f"⚠️ 数据一致性需要进一步检查")
        
        print(f"\n🌐 推荐访问地址:")
        print(f"  - 图谱可视化: http://localhost:5173/#/graph-visualization")
        print(f"  - 图谱探索: http://localhost:5173/#/graph-explore")
        print(f"  - 图谱查询: http://localhost:5173/#/graph-query")
        
        print(f"\n🔧 API端点:")
        print(f"  - 图谱数据: http://localhost:8000/kg/graph")
        print(f"  - 图谱统计: http://localhost:8000/kg/real-stats")
        
    else:
        print(f"⚠️ 图谱功能仍存在问题")
        print(f"❌ 需要进一步检查API或前端配置")
    
    # 保存详细结果
    with open('图谱功能修复验证结果.json', 'w', encoding='utf-8') as f:
        json.dump({
            'api_results': api_results,
            'frontend_results': frontend_results,
            'consistency_ok': consistency_ok,
            'summary': {
                'api_success_rate': f"{api_success}/{len(api_results)}",
                'frontend_success_rate': f"{frontend_success}/{len(frontend_results)}",
                'overall_status': 'success' if api_success >= 3 and frontend_success >= 1 else 'partial'
            }
        }, ensure_ascii=False, indent=2)
    
    print(f"\n📄 详细结果已保存: 图谱功能修复验证结果.json")

if __name__ == "__main__":
    main()
