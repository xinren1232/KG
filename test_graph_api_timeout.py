#!/usr/bin/env python3
"""测试图谱API的响应时间和超时问题"""

import requests
import time
import json

SERVER_URL = "http://47.108.152.16"

def test_graph_api():
    """测试图谱API"""
    print("\n" + "="*70)
    print("测试图谱可视化API")
    print("="*70)
    
    # 测试不同的参数组合
    test_cases = [
        {
            "name": "默认参数",
            "url": f"{SERVER_URL}/api/kg/graph",
            "params": {}
        },
        {
            "name": "小数据量 (limit=100)",
            "url": f"{SERVER_URL}/api/kg/graph",
            "params": {"limit": 100, "show_all": False}
        },
        {
            "name": "中等数据量 (limit=500)",
            "url": f"{SERVER_URL}/api/kg/graph",
            "params": {"limit": 500, "show_all": False}
        },
        {
            "name": "大数据量 (limit=1000)",
            "url": f"{SERVER_URL}/api/kg/graph",
            "params": {"limit": 1000, "show_all": False}
        },
        {
            "name": "显示全部 (show_all=true, limit=15000)",
            "url": f"{SERVER_URL}/api/kg/graph",
            "params": {"limit": 15000, "show_all": True}
        }
    ]
    
    for test in test_cases:
        print(f"\n测试: {test['name']}")
        print(f"URL: {test['url']}")
        print(f"参数: {test['params']}")
        
        try:
            start_time = time.time()
            response = requests.get(
                test['url'],
                params=test['params'],
                timeout=30  # 30秒超时
            )
            elapsed_time = time.time() - start_time
            
            print(f"状态码: {response.status_code}")
            print(f"响应时间: {elapsed_time:.2f}秒")
            
            if response.status_code == 200:
                data = response.json()
                if 'data' in data:
                    nodes_count = len(data['data'].get('sampleNodes', []))
                    relations_count = len(data['data'].get('sampleRelations', []))
                    print(f"✓ 成功 - 节点数: {nodes_count}, 关系数: {relations_count}")
                else:
                    print(f"✓ 成功 - 响应数据: {json.dumps(data, ensure_ascii=False)[:200]}")
            else:
                print(f"✗ 失败 - {response.text[:200]}")
                
        except requests.exceptions.Timeout:
            elapsed_time = time.time() - start_time
            print(f"✗ 超时 - 请求超过30秒")
            print(f"已等待时间: {elapsed_time:.2f}秒")
        except Exception as e:
            print(f"✗ 错误 - {str(e)}")

def test_neo4j_connection():
    """测试Neo4j连接"""
    print("\n" + "="*70)
    print("测试Neo4j连接状态")
    print("="*70)
    
    try:
        response = requests.get(f"{SERVER_URL}/api/health", timeout=10)
        print(f"健康检查状态: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"响应: {json.dumps(data, ensure_ascii=False, indent=2)}")
    except Exception as e:
        print(f"错误: {str(e)}")

def test_simple_query():
    """测试简单的Cypher查询"""
    print("\n" + "="*70)
    print("测试简单Cypher查询")
    print("="*70)
    
    try:
        # 测试简单的节点计数查询
        response = requests.post(
            f"{SERVER_URL}/api/kg/query",
            json={
                "cypher_query": "MATCH (n) RETURN count(n) as count LIMIT 1",
                "parameters": {}
            },
            timeout=10
        )
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ 查询成功: {json.dumps(data, ensure_ascii=False, indent=2)}")
        else:
            print(f"✗ 查询失败: {response.text}")
    except Exception as e:
        print(f"✗ 错误: {str(e)}")

if __name__ == "__main__":
    print("="*70)
    print("图谱API超时问题诊断")
    print("="*70)
    
    test_neo4j_connection()
    test_simple_query()
    test_graph_api()
    
    print("\n" + "="*70)
    print("诊断完成")
    print("="*70)

