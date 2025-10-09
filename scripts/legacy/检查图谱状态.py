#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from neo4j import GraphDatabase

def check_graph_status():
    """检查图谱状态"""
    driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'password123'))
    
    try:
        with driver.session() as session:
            # 获取节点统计
            result = session.run('MATCH (n) RETURN labels(n)[0] as label, count(n) as count ORDER BY count DESC')
            stats = list(result)
            total = sum(r['count'] for r in stats)
            
            print(f"🎯 图谱数据补充后状态")
            print(f"=" * 40)
            print(f"总节点数: {total}")
            print(f"节点分布:")
            for r in stats:
                print(f"  {r['label']}: {r['count']} 个")
            
            # 获取关系统计
            rel_result = session.run('MATCH ()-[r]->() RETURN type(r) as type, count(r) as count ORDER BY count DESC')
            rel_stats = list(rel_result)
            total_rels = sum(r['count'] for r in rel_stats)
            
            print(f"\n总关系数: {total_rels}")
            print(f"关系分布:")
            for r in rel_stats:
                print(f"  {r['type']}: {r['count']} 个")
            
            # 检查是否达到预期
            if total >= 1000:
                print(f"\n✅ 图谱数据已充实！节点数达到 {total} 个")
            else:
                print(f"\n⚠️ 图谱数据仍需补充，当前节点数 {total} 个")
                
    finally:
        driver.close()

if __name__ == "__main__":
    check_graph_status()
