#!/usr/bin/env python3
"""
导入语义关系到Neo4j
从semantic_relationships.json中筛选高质量关系并导入
"""
import json
from neo4j import GraphDatabase

# Neo4j连接配置
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "password123"

# 加载关系数据
with open('semantic_relationships.json', 'r', encoding='utf-8') as f:
    relationships_data = json.load(f)

print("=" * 80)
print("🔗 导入语义关系到Neo4j")
print("=" * 80)

# 连接Neo4j
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def import_relationships(tx, rel_type, relationships, min_score=10):
    """导入关系到Neo4j"""
    imported = 0
    skipped = 0
    
    for rel in relationships:
        if rel['score'] >= min_score:
            # 创建关系
            query = f"""
            MATCH (from:Term {{name: $from_term}})
            MATCH (to:Term {{name: $to_term}})
            MERGE (from)-[r:{rel_type}]->(to)
            SET r.score = $score, r.reason = $reason
            RETURN r
            """
            try:
                result = tx.run(query, 
                    from_term=rel['from'],
                    to_term=rel['to'],
                    score=rel['score'],
                    reason=rel['reason']
                )
                if result.single():
                    imported += 1
            except Exception as e:
                skipped += 1
                # print(f"  ⚠️ 跳过: {rel['from']} -> {rel['to']} ({e})")
    
    return imported, skipped

# 1. 导入 Symptom → Component (AFFECTS)
print("\n1️⃣ 导入 Symptom → Component (AFFECTS) 关系")
print("-" * 80)

symptom_component = relationships_data['symptom_component']
# 按分数排序，只导入高分关系
symptom_component_sorted = sorted(symptom_component, key=lambda x: x['score'], reverse=True)

print(f"总计: {len(symptom_component)} 条")
print(f"筛选条件: 分数 >= 12")

with driver.session() as session:
    imported, skipped = session.execute_write(
        import_relationships, 
        'AFFECTS', 
        symptom_component_sorted,
        min_score=12
    )

print(f"✅ 已导入: {imported} 条")
print(f"⚠️ 跳过: {skipped} 条")

# 2. 导入 TestCase → Component (TESTS)
print("\n2️⃣ 导入 TestCase → Component (TESTS) 关系")
print("-" * 80)

testcase_component = relationships_data['testcase_component']
testcase_component_sorted = sorted(testcase_component, key=lambda x: x['score'], reverse=True)

print(f"总计: {len(testcase_component)} 条")
print(f"筛选条件: 分数 >= 12")

with driver.session() as session:
    imported, skipped = session.execute_write(
        import_relationships,
        'TESTS',
        testcase_component_sorted,
        min_score=12
    )

print(f"✅ 已导入: {imported} 条")
print(f"⚠️ 跳过: {skipped} 条")

# 3. 导入 Tool → TestCase (USED_IN)
print("\n3️⃣ 导入 Tool → TestCase (USED_IN) 关系")
print("-" * 80)

tool_testcase = relationships_data['tool_testcase']
tool_testcase_sorted = sorted(tool_testcase, key=lambda x: x['score'], reverse=True)

print(f"总计: {len(tool_testcase)} 条")
print(f"筛选条件: 分数 >= 12")

with driver.session() as session:
    imported, skipped = session.execute_write(
        import_relationships,
        'USED_IN',
        tool_testcase_sorted,
        min_score=12
    )

print(f"✅ 已导入: {imported} 条")
print(f"⚠️ 跳过: {skipped} 条")

# 4. 导入 Process → Component (PRODUCES)
print("\n4️⃣ 导入 Process → Component (PRODUCES) 关系")
print("-" * 80)

process_component = relationships_data['process_component']
process_component_sorted = sorted(process_component, key=lambda x: x['score'], reverse=True)

print(f"总计: {len(process_component)} 条")
print(f"筛选条件: 分数 >= 12")

with driver.session() as session:
    imported, skipped = session.execute_write(
        import_relationships,
        'PRODUCES',
        process_component_sorted,
        min_score=12
    )

print(f"✅ 已导入: {imported} 条")
print(f"⚠️ 跳过: {skipped} 条")

# 5. 统计图谱关系
print("\n5️⃣ 统计图谱关系")
print("-" * 80)

with driver.session() as session:
    # 统计各类关系数量
    result = session.run("""
        MATCH ()-[r]->()
        RETURN type(r) AS rel_type, count(r) AS count
        ORDER BY count DESC
    """)
    
    print("关系类型统计:")
    total_rels = 0
    for record in result:
        rel_type = record['rel_type']
        count = record['count']
        total_rels += count
        print(f"  {rel_type:20s}: {count:5d} 条")
    
    print(f"\n总关系数: {total_rels} 条")

# 关闭连接
driver.close()

print("\n" + "=" * 80)
print("✅ 导入完成")
print("=" * 80)

