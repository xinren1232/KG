from neo4j import GraphDatabase

# 连接Neo4j
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password123"))

with driver.session() as session:
    # 为每个分类添加对应标签
    categories = ['Symptom', 'Component', 'Tool', 'Process', 'TestCase', 'Metric', 'Material', 'Role']
    
    for category in categories:
        query = f"MATCH (d:Dictionary) WHERE d.category = '{category}' SET d:{category}"
        session.run(query)
        print(f"✅ 已为 {category} 分类添加标签")
    
    # 验证结果
    for category in categories:
        result = session.run(f"MATCH (n:{category}) RETURN count(n) as count")
        count = result.single()["count"]
        print(f"{category}: {count} 个节点")

driver.close()
print("🎉 标签修复完成！")
