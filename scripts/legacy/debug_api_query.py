#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from neo4j import GraphDatabase

def debug_api_query():
    """调试API查询问题"""
    driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'password123'))
    
    try:
        with driver.session() as session:
            # 模拟API查询
            min_confidence = 0.0
            inferred = None
            types_list = None
            limit = 50
            
            allowed = "Component|Symptom|Tool|Process|TestCase|Material|Role|Metric"
            rel_sample_query = f"""
                MATCH (a)-[r]->(b)
                WHERE (a:{' OR a:'.join(allowed.split('|'))})
                  AND (b:{' OR b:'.join(allowed.split('|'))})
                  AND coalesce(r.confidence, 1.0) >= $min_conf
                  AND ($inferred IS NULL OR coalesce(r.inferred,false) = $inferred)
                  AND ($types IS NULL OR type(r) IN $types)
                RETURN elementId(a) AS sid,
                       labels(a)[0] AS sc,
                       coalesce(a.name, a.term, 'Unknown') AS sname,
                       coalesce(a.description, a.definition, '') AS sdesc,
                       elementId(b) AS tid,
                       labels(b)[0] AS tc,
                       coalesce(b.name, b.term, 'Unknown') AS tname,
                       coalesce(b.description, b.definition, '') AS tdesc,
                       type(r) AS rel_type,
                       properties(r) AS rel_props
                ORDER BY coalesce(r.confidence, 1.0) DESC
                LIMIT $limit
            """
            
            print("执行查询...")
            print(f"参数: min_conf={min_confidence}, inferred={inferred}, types={types_list}, limit={limit}")
            
            result = session.run(rel_sample_query, min_conf=min_confidence, inferred=inferred, types=types_list, limit=limit)
            rel_rows = result.data()
            
            print(f"查询结果数量: {len(rel_rows)}")
            
            if len(rel_rows) > 0:
                print("前5条结果:")
                for i, row in enumerate(rel_rows[:5]):
                    print(f"  {i+1}. {row['sname']} ({row['sc']}) --[{row['rel_type']}]--> {row['tname']} ({row['tc']})")
                    print(f"     rel_props: {row['rel_props']}")
            else:
                print("没有查询结果，检查条件...")
                
                # 检查各个条件
                print("\n1. 检查节点标签条件:")
                test_query1 = """
                    MATCH (a)-[r]->(b)
                    WHERE (a:Component OR a:Symptom OR a:Tool OR a:Process OR a:TestCase OR a:Material OR a:Role OR a:Metric)
                      AND (b:Component OR b:Symptom OR b:Tool OR b:Process OR b:TestCase OR b:Material OR b:Role OR b:Metric)
                    RETURN count(r) AS count
                """
                result1 = session.run(test_query1).single()
                print(f"   符合节点标签条件的关系数: {result1['count']}")
                
                print("\n2. 检查置信度条件:")
                test_query2 = """
                    MATCH (a)-[r]->(b)
                    WHERE (a:Component OR a:Symptom OR a:Tool OR a:Process OR a:TestCase OR a:Material OR a:Role OR a:Metric)
                      AND (b:Component OR b:Symptom OR b:Tool OR b:Process OR b:TestCase OR b:Material OR b:Role OR b:Metric)
                      AND coalesce(r.confidence, 1.0) >= 0.0
                    RETURN count(r) AS count
                """
                result2 = session.run(test_query2).single()
                print(f"   符合置信度条件的关系数: {result2['count']}")
                
                print("\n3. 检查inferred条件:")
                test_query3 = """
                    MATCH (a)-[r]->(b)
                    WHERE (a:Component OR a:Symptom OR a:Tool OR a:Process OR a:TestCase OR a:Material OR a:Role OR a:Metric)
                      AND (b:Component OR b:Symptom OR b:Tool OR b:Process OR b:TestCase OR b:Material OR b:Role OR b:Metric)
                      AND coalesce(r.confidence, 1.0) >= 0.0
                      AND (NULL IS NULL OR coalesce(r.inferred,false) = NULL)
                    RETURN count(r) AS count
                """
                result3 = session.run(test_query3).single()
                print(f"   符合inferred条件的关系数: {result3['count']}")
                
                print("\n4. 检查关系属性:")
                test_query4 = """
                    MATCH ()-[r]->()
                    WHERE r.confidence IS NOT NULL OR r.inferred IS NOT NULL
                    RETURN count(r) AS count
                """
                result4 = session.run(test_query4).single()
                print(f"   有confidence或inferred属性的关系数: {result4['count']}")
    
    finally:
        driver.close()

if __name__ == "__main__":
    debug_api_query()
