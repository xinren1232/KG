#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json

def test_graph_api():
    """测试图谱API"""
    print("🔍 测试图谱API...")
    
    try:
        # 测试图谱数据API
        response = requests.get('http://localhost:8000/kg/graph-data?min_confidence=0.0&limit=50')
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API状态: {response.status_code}")
            print(f"✅ 成功: {data.get('success')}")
            
            graph_data = data.get('data', {})
            nodes = graph_data.get('nodes', [])
            links = graph_data.get('links', [])
            
            print(f"📊 节点数: {len(nodes)}")
            print(f"📊 关系数: {len(links)}")
            
            if len(nodes) > 0:
                print("\n前3个节点:")
                for i, node in enumerate(nodes[:3]):
                    print(f"  {i+1}. {node.get('name', 'Unknown')} ({node.get('category', 'Unknown')})")
            
            if len(links) > 0:
                print("\n前3个关系:")
                for i, rel in enumerate(links[:3]):
                    print(f"  {i+1}. {rel.get('type', 'Unknown')} (置信度: {rel.get('confidence', 'N/A')})")
            
            # 测试统计信息
            stats = graph_data.get('stats', {})
            print(f"\n📈 统计信息:")
            print(f"  总节点数: {stats.get('totalNodes', 'N/A')}")
            print(f"  总关系数: {stats.get('totalRelations', 'N/A')}")
            print(f"  总类别数: {stats.get('totalCategories', 'N/A')}")
            
        else:
            print(f"❌ API错误: {response.status_code}")
            print(f"❌ 响应: {response.text}")
    
    except Exception as e:
        print(f"❌ 测试失败: {e}")

if __name__ == "__main__":
    test_graph_api()
