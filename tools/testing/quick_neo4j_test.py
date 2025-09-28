#!/usr/bin/env python3
"""
快速Neo4j连接测试
"""
def test_neo4j():
    try:
        from neo4j import GraphDatabase
        
        print("🔗 测试Neo4j连接...")
        driver = GraphDatabase.driver(
            "bolt://localhost:7687", 
            auth=("neo4j", "password123")
        )
        
        with driver.session() as session:
            result = session.run("RETURN 'Hello Neo4j!' as message")
            record = result.single()
            print(f"✅ 连接成功: {record['message']}")
            
            # 检查节点数量
            result = session.run("MATCH (n) RETURN count(n) as count")
            count = result.single()["count"]
            print(f"📊 当前节点数量: {count}")
        
        driver.close()
        return True
        
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        return False

def test_browser():
    try:
        import requests
        response = requests.get("http://localhost:7474", timeout=5)
        if response.status_code == 200:
            print("✅ Neo4j Browser可访问: http://localhost:7474")
            return True
        else:
            print(f"❌ Browser响应异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Browser不可访问: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Neo4j快速测试")
    print("=" * 30)
    
    browser_ok = test_browser()
    db_ok = test_neo4j()
    
    print("\n" + "=" * 30)
    if browser_ok and db_ok:
        print("🎉 Neo4j运行正常！")
        print("\n📋 下一步:")
        print("   python init_neo4j.py")
    else:
        print("❌ Neo4j未正常运行")
        print("\n💡 请检查Neo4j Desktop是否已启动数据库")
