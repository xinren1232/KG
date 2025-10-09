#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from neo4j import GraphDatabase

def test_graph_query():
    """测试图谱查询"""
    driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'password123'))
    
    try:
        with driver.session() as session:
            # 测试基本查询
            print("1. 测试节点查询:")
            result = session.run("""
                MATCH (n) 
                WHERE n:Component OR n:Symptom OR n:Tool OR n:Process OR n:TestCase OR n:Material OR n:Role OR n:Metric
                RETURN labels(n)[0] AS label, count(n) AS count
                ORDER BY count DESC
            """)
            for record in result:
                print(f"   {record['label']}: {record['count']}")
            
            print("\n2. 测试关系查询:")
            result = session.run("""
                MATCH ()-[r]->()
                RETURN type(r) AS rel_type, count(r) AS count
                ORDER BY count DESC
                LIMIT 10
            """)
            for record in result:
                print(f"   {record['rel_type']}: {record['count']}")
            
            print("\n3. 测试图谱数据查询:")
            result = session.run("""
                MATCH (a)-[r]->(b)
                WHERE (a:Component OR a:Symptom OR a:Tool OR a:Process OR a:TestCase OR a:Material OR a:Role OR a:Metric)
                  AND (b:Component OR b:Symptom OR b:Tool OR b:Process OR b:TestCase OR b:Material OR b:Role OR b:Metric)
                  AND coalesce(r.confidence, 1.0) >= 0.0
                RETURN elementId(a) AS sid,
                       labels(a)[0] AS sc,
                       coalesce(a.name, a.term, 'Unknown') AS sname,
                       elementId(b) AS tid,
                       labels(b)[0] AS tc,
                       coalesce(b.name, b.term, 'Unknown') AS tname,
                       type(r) AS rel_type
                LIMIT 5
            """)
            
            count = 0
            for record in result:
                count += 1
                print(f"   关系 {count}: {record['sname']} ({record['sc']}) --[{record['rel_type']}]--> {record['tname']} ({record['tc']})")
            
            if count == 0:
                print("   没有找到符合条件的关系")
                
                # 检查是否有任何关系
                result2 = session.run("MATCH ()-[r]->() RETURN count(r) AS total")
                total = result2.single()['total']
                print(f"   数据库中总关系数: {total}")
                
                # 检查关系类型
                result3 = session.run("MATCH ()-[r]->() RETURN DISTINCT type(r) AS types LIMIT 10")
                types = [record['types'] for record in result3]
                print(f"   关系类型: {types}")
    
    finally:
        driver.close()

if __name__ == "__main__":
    test_graph_query()
