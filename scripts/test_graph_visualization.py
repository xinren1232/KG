#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试图谱可视化数据
检查节点、关系、样式等配置
"""

import requests
import json
from collections import Counter

def test_graph_api():
    """测试图谱API"""
    print("=" * 80)
    print("🔍 测试图谱可视化API")
    print("=" * 80)
    
    base_url = "http://localhost:8000"
    
    # 测试不同参数
    test_cases = [
        {
            "name": "默认参数（100个节点）",
            "url": f"{base_url}/kg/graph",
            "params": {}
        },
        {
            "name": "显示所有节点",
            "url": f"{base_url}/kg/graph",
            "params": {"show_all": True, "limit": 1000}
        },
        {
            "name": "限制50个节点",
            "url": f"{base_url}/kg/graph",
            "params": {"limit": 50}
        }
    ]
    
    for test_case in test_cases:
        print(f"\n📊 {test_case['name']}")
        print("-" * 80)
        
        try:
            response = requests.get(test_case['url'], params=test_case['params'], timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('success'):
                    graph_data = data.get('data', {})
                    stats = graph_data.get('stats', {})
                    nodes = graph_data.get('nodes', [])
                    relations = graph_data.get('relations', [])
                    categories = graph_data.get('categories', [])
                    
                    print(f"✅ API调用成功")
                    print(f"\n📈 统计信息:")
                    print(f"  总词条数: {stats.get('totalNodes', 0)}")
                    print(f"  总关系数: {stats.get('totalRelations', 0)}")
                    print(f"  总分类数: {stats.get('totalCategories', 0)}")
                    print(f"  总标签数: {stats.get('totalTags', 0)}")
                    
                    print(f"\n🔢 实际数据:")
                    print(f"  返回节点数: {len(nodes)}")
                    print(f"  返回关系数: {len(relations)}")
                    print(f"  分类数量: {len(categories)}")
                    
                    # 分析节点分类分布
                    if nodes:
                        category_dist = Counter(node.get('category') for node in nodes)
                        print(f"\n📊 节点分类分布:")
                        for cat, count in category_dist.most_common():
                            print(f"  {cat}: {count}")
                        
                        # 分析节点大小分布
                        sizes = [node.get('symbolSize', 0) for node in nodes]
                        print(f"\n📏 节点大小统计:")
                        print(f"  最小: {min(sizes)}")
                        print(f"  最大: {max(sizes)}")
                        print(f"  平均: {sum(sizes) / len(sizes):.2f}")
                        
                        # 分析连接数
                        connections = [node.get('connections', 0) for node in nodes]
                        print(f"\n🔗 节点连接数统计:")
                        print(f"  最小: {min(connections)}")
                        print(f"  最大: {max(connections)}")
                        print(f"  平均: {sum(connections) / len(connections):.2f}")
                        
                        # 显示前5个最重要的节点
                        top_nodes = sorted(nodes, key=lambda x: x.get('connections', 0), reverse=True)[:5]
                        print(f"\n⭐ 连接数最多的5个节点:")
                        for i, node in enumerate(top_nodes, 1):
                            print(f"  {i}. {node.get('name')} ({node.get('category')}) - {node.get('connections')}个连接")
                    
                    # 分析关系类型分布
                    if relations:
                        rel_types = Counter(rel.get('type') for rel in relations)
                        print(f"\n🔗 关系类型分布:")
                        for rel_type, count in rel_types.most_common():
                            print(f"  {rel_type}: {count}")
                    
                    # 检查数据质量
                    print(f"\n✅ 数据质量检查:")
                    nodes_with_name = sum(1 for n in nodes if n.get('name'))
                    nodes_with_desc = sum(1 for n in nodes if n.get('description'))
                    print(f"  有名称的节点: {nodes_with_name}/{len(nodes)} ({nodes_with_name/len(nodes)*100:.1f}%)")
                    print(f"  有描述的节点: {nodes_with_desc}/{len(nodes)} ({nodes_with_desc/len(nodes)*100:.1f}%)")
                    
                else:
                    print(f"❌ API返回失败: {data.get('message')}")
            else:
                print(f"❌ HTTP错误: {response.status_code}")
                print(f"   响应: {response.text[:200]}")
                
        except requests.exceptions.Timeout:
            print(f"❌ 请求超时")
        except requests.exceptions.ConnectionError:
            print(f"❌ 连接失败 - 请确保API服务正在运行")
        except Exception as e:
            print(f"❌ 错误: {e}")

def test_neo4j_connection():
    """测试Neo4j连接"""
    print("\n" + "=" * 80)
    print("🔍 测试Neo4j数据库连接")
    print("=" * 80)
    
    try:
        from neo4j import GraphDatabase
        
        # 尝试连接
        uri = "bolt://localhost:7687"
        driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))
        
        with driver.session() as session:
            # 获取节点统计
            result = session.run("""
                MATCH (n)
                RETURN labels(n)[0] as label, count(n) as count
                ORDER BY count DESC
            """)
            
            print("\n📊 数据库节点统计:")
            total = 0
            for record in result:
                label = record['label']
                count = record['count']
                total += count
                print(f"  {label}: {count}")
            print(f"  总计: {total}")
            
            # 获取关系统计
            result = session.run("""
                MATCH ()-[r]->()
                RETURN type(r) as type, count(r) as count
                ORDER BY count DESC
            """)
            
            print("\n🔗 数据库关系统计:")
            total_rels = 0
            for record in result:
                rel_type = record['type']
                count = record['count']
                total_rels += count
                print(f"  {rel_type}: {count}")
            print(f"  总计: {total_rels}")
        
        driver.close()
        print("\n✅ Neo4j连接成功")
        
    except ImportError:
        print("❌ neo4j驱动未安装，跳过数据库测试")
    except Exception as e:
        print(f"❌ Neo4j连接失败: {e}")

def main():
    """主函数"""
    print("\n" + "🎯" * 40)
    print("图谱可视化测试工具")
    print("🎯" * 40 + "\n")
    
    # 测试API
    test_graph_api()
    
    # 测试数据库
    test_neo4j_connection()
    
    print("\n" + "=" * 80)
    print("✅ 测试完成")
    print("=" * 80)

if __name__ == "__main__":
    main()

