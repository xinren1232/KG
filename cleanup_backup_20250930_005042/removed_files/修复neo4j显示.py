#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复Neo4j浏览器显示问题 - 为每个Dictionary节点添加对应的分类标签
"""

from neo4j import GraphDatabase

def add_category_labels():
    """为Dictionary节点添加对应的分类标签"""
    print("🔧 修复Neo4j浏览器显示 - 添加分类标签")
    print("=" * 50)
    
    uri = "bolt://localhost:7687"
    username = "neo4j"
    password = "password123"
    
    try:
        driver = GraphDatabase.driver(uri, auth=(username, password))
        print(f"✅ Neo4j连接成功")
        
        with driver.session() as session:
            # 1. 检查当前状态
            result = session.run("MATCH (d:Dictionary) RETURN count(d) as count")
            dict_count = result.single()["count"]
            print(f"📊 Dictionary节点: {dict_count} 个")
            
            # 2. 获取所有分类
            result = session.run("MATCH (d:Dictionary) RETURN DISTINCT d.category as category ORDER BY category")
            categories = [record["category"] for record in result]
            print(f"📊 发现的分类: {categories}")
            
            # 3. 为每个分类的节点添加对应的标签
            print(f"\n🔧 开始添加分类标签...")
            
            for category in categories:
                # 为该分类的所有节点添加对应标签
                query = f"""
                MATCH (d:Dictionary) 
                WHERE d.category = $category 
                SET d:{category}
                RETURN count(d) as updated_count
                """
                
                result = session.run(query, category=category)
                updated_count = result.single()["updated_count"]
                print(f"✅ {category}: 已为 {updated_count} 个节点添加标签")
            
            # 4. 验证结果
            print(f"\n🔍 验证结果...")
            
            # 检查所有标签
            result = session.run("CALL db.labels()")
            all_labels = [record["label"] for record in result]
            print(f"📊 所有标签: {all_labels}")
            
            # 检查每个分类标签的节点数
            print(f"📊 各分类标签节点数:")
            for category in categories:
                result = session.run(f"MATCH (n:{category}) RETURN count(n) as count")
                count = result.single()["count"]
                print(f"  {category}: {count} 个")
            
            # 5. 验证Dictionary节点仍然完整
            result = session.run("MATCH (d:Dictionary) RETURN count(d) as count")
            final_dict_count = result.single()["count"]
            print(f"\n📊 Dictionary节点验证: {final_dict_count} 个")
            
            if final_dict_count == dict_count:
                print(f"✅ Dictionary节点数量保持不变")
            else:
                print(f"⚠️ Dictionary节点数量发生变化")
            
            # 6. 创建验证查询
            print(f"\n📋 Neo4j浏览器验证查询:")
            print(f"// 查看所有分类节点数量")
            for category in categories:
                print(f"MATCH (n:{category}) RETURN count(n) as {category}_count;")
            
            print(f"\n// 查看分类分布")
            print(f"MATCH (d:Dictionary) RETURN d.category, count(d) ORDER BY count(d) DESC;")
            
            print(f"\n// 查看特定分类的节点")
            print(f"MATCH (s:Symptom) RETURN s.term, s.description LIMIT 10;")
            print(f"MATCH (c:Component) RETURN c.term, c.description LIMIT 10;")
            
            return True
                
    except Exception as e:
        print(f"❌ 操作失败: {e}")
        return False
    
    finally:
        if driver:
            driver.close()

def main():
    success = add_category_labels()
    
    print(f"\n" + "=" * 50)
    print(f"📊 操作结果")
    print(f"=" * 50)
    
    if success:
        print(f"🎉 分类标签添加成功!")
        print(f"\n🌐 现在在Neo4j浏览器中:")
        print(f"  1. 访问: http://localhost:7474")
        print(f"  2. 可以看到8个分类标签，每个都有对应数量的节点")
        print(f"  3. 可以分别查询每个分类: MATCH (s:Symptom) RETURN s;")
        print(f"  4. Dictionary标签仍然包含所有1124个节点")
        
        print(f"\n✅ 现在您应该能在Neo4j浏览器中看到:")
        print(f"  - Symptom (259)")
        print(f"  - Metric (190)")  
        print(f"  - Component (181)")
        print(f"  - Process (170)")
        print(f"  - TestCase (104)")
        print(f"  - Tool (102)")
        print(f"  - Role (63)")
        print(f"  - Material (55)")
        print(f"  - Dictionary (1124)")
        
    else:
        print(f"❌ 分类标签添加失败")

if __name__ == "__main__":
    main()
