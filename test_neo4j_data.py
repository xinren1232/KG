#!/usr/bin/env python3
"""
测试Neo4j数据和知识图谱功能
"""
from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

def test_neo4j_data():
    """测试Neo4j中的数据"""
    load_dotenv()
    
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    user = os.getenv("NEO4J_USER", "neo4j")
    password = os.getenv("NEO4J_PASS", "password123")
    
    print("🔍 连接Neo4j数据库...")
    driver = GraphDatabase.driver(uri, auth=(user, password))
    
    try:
        with driver.session() as session:
            print("✅ 数据库连接成功")
            
            # 1. 检查节点统计
            print("\n📊 节点统计:")
            node_types = ["Product", "Component", "Anomaly", "TestCase", "Symptom"]
            for node_type in node_types:
                result = session.run(f"MATCH (n:{node_type}) RETURN count(n) as count")
                count = result.single()["count"]
                print(f"   {node_type}: {count} 个")
            
            # 2. 检查关系统计
            print("\n🔗 关系统计:")
            result = session.run("MATCH ()-[r]->() RETURN type(r) as rel_type, count(r) as count")
            for record in result:
                print(f"   {record['rel_type']}: {record['count']} 条")
            
            # 3. 查看产品和组件
            print("\n📱 产品信息:")
            result = session.run("MATCH (p:Product) RETURN p.name, p.model, p.category")
            for record in result:
                print(f"   {record['p.name']} ({record['p.model']}) - {record['p.category']}")
            
            # 4. 查看异常信息
            print("\n⚠️ 异常信息:")
            result = session.run("MATCH (a:Anomaly) RETURN a.title, a.severity, a.status")
            for record in result:
                print(f"   {record['a.title']} - {record['a.severity']} - {record['a.status']}")
            
            # 5. 查看关系路径
            print("\n🔍 关系路径示例:")
            result = session.run("""
                MATCH (p:Product)-[r1]->(c:Component)-[r2]->(a:Anomaly)
                RETURN p.name, type(r1), c.name, type(r2), a.title
                LIMIT 3
            """)
            for record in result:
                print(f"   {record['p.name']} --{record['type(r1)']}--> {record['c.name']} --{record['type(r2)']}--> {record['a.title']}")
            
            # 6. 图谱可视化数据
            print("\n🎨 图谱可视化数据:")
            result = session.run("""
                MATCH (n)-[r]->(m)
                RETURN 
                    id(n) as source_id, labels(n)[0] as source_label, n.name as source_name,
                    type(r) as relationship,
                    id(m) as target_id, labels(m)[0] as target_label, m.name as target_name
                LIMIT 5
            """)
            
            nodes = set()
            edges = []
            
            for record in result:
                # 添加节点
                nodes.add((record['source_id'], record['source_label'], record['source_name']))
                nodes.add((record['target_id'], record['target_label'], record['target_name']))
                
                # 添加边
                edges.append({
                    'source': record['source_id'],
                    'target': record['target_id'],
                    'relationship': record['relationship']
                })
            
            print(f"   节点数量: {len(nodes)}")
            print(f"   关系数量: {len(edges)}")
            
            for node_id, label, name in list(nodes)[:3]:
                print(f"   节点: {label} - {name}")
            
            for edge in edges[:3]:
                print(f"   关系: {edge['source']} --{edge['relationship']}--> {edge['target']}")
            
            return True
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False
    finally:
        driver.close()

def main():
    """主函数"""
    print("🚀 Neo4j数据测试")
    print("=" * 50)
    
    success = test_neo4j_data()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 Neo4j数据测试成功！")
        print("\n📋 可以进行的操作:")
        print("   1. 访问 http://localhost:7474 查看Neo4j Browser")
        print("   2. 访问 http://localhost:8000/docs 查看API文档")
        print("   3. 访问 http://localhost:5173 查看前端应用")
        print("   4. 测试文档上传和知识图谱构建功能")
    else:
        print("❌ Neo4j数据测试失败")

if __name__ == "__main__":
    main()
