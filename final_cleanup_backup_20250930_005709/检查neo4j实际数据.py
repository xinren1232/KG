#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查Neo4j中的实际数据
"""

from neo4j import GraphDatabase

def check_neo4j_data():
    """检查Neo4j中的实际数据"""
    print("🔍 检查Neo4j中的实际数据")
    print("=" * 50)
    
    uri = "bolt://localhost:7687"
    username = "neo4j"
    password = "password123"
    
    try:
        driver = GraphDatabase.driver(uri, auth=(username, password))
        print(f"✅ Neo4j连接成功")
        
        with driver.session() as session:
            # 1. 检查总节点数
            result = session.run("MATCH (n) RETURN count(n) as total")
            total_nodes = result.single()["total"]
            print(f"📊 总节点数: {total_nodes}")
            
            # 2. 检查Dictionary节点数
            result = session.run("MATCH (d:Dictionary) RETURN count(d) as count")
            dict_count = result.single()["count"]
            print(f"📊 Dictionary节点数: {dict_count}")
            
            # 3. 检查所有标签
            result = session.run("CALL db.labels()")
            labels = [record["label"] for record in result]
            print(f"📊 所有标签: {labels}")
            
            # 4. 检查每个标签的节点数
            print(f"\n📊 各标签节点数:")
            for label in labels:
                result = session.run(f"MATCH (n:{label}) RETURN count(n) as count")
                count = result.single()["count"]
                print(f"  {label}: {count} 个")
            
            # 5. 检查Dictionary节点的属性结构
            result = session.run("MATCH (d:Dictionary) RETURN d LIMIT 3")
            print(f"\n📋 Dictionary节点示例:")
            for i, record in enumerate(result):
                node = record["d"]
                print(f"  示例{i+1}: {dict(node)}")
            
            # 6. 检查category属性
            try:
                result = session.run("MATCH (d:Dictionary) WHERE d.category IS NOT NULL RETURN DISTINCT d.category as category ORDER BY category")
                categories = [record["category"] for record in result]
                print(f"\n📊 发现的category值: {categories}")
                
                # 统计每个category的数量
                print(f"📊 category分布:")
                for category in categories:
                    result = session.run("MATCH (d:Dictionary) WHERE d.category = $cat RETURN count(d) as count", cat=category)
                    count = result.single()["count"]
                    print(f"  {category}: {count} 条")
                    
            except Exception as e:
                print(f"⚠️ category查询失败: {e}")
            
            # 7. 检查是否有category为空的节点
            result = session.run("MATCH (d:Dictionary) WHERE d.category IS NULL OR d.category = '' RETURN count(d) as count")
            empty_category_count = result.single()["count"]
            print(f"\n📊 category为空的节点: {empty_category_count} 个")
            
            # 8. 检查节点的所有属性
            result = session.run("MATCH (d:Dictionary) RETURN keys(d) as keys LIMIT 1")
            if result.peek():
                keys = result.single()["keys"]
                print(f"\n📋 Dictionary节点属性: {keys}")
            
            return dict_count, categories if 'categories' in locals() else []
                
    except Exception as e:
        print(f"❌ 检查失败: {e}")
        return 0, []
    
    finally:
        if driver:
            driver.close()

def main():
    dict_count, categories = check_neo4j_data()
    
    print(f"\n" + "=" * 50)
    print(f"📊 检查结果总结")
    print(f"=" * 50)
    
    if dict_count > 0:
        print(f"✅ Dictionary节点: {dict_count} 个")
        print(f"📊 发现的分类: {len(categories)} 个")
        
        # 期望的8个分类
        expected_categories = {'Symptom', 'Component', 'Tool', 'Process', 'TestCase', 'Metric', 'Material', 'Role'}
        actual_categories = set(categories)
        
        print(f"\n📊 分类对比:")
        print(f"  期望: {expected_categories}")
        print(f"  实际: {actual_categories}")
        
        if actual_categories == expected_categories:
            print(f"✅ 分类完全匹配")
        else:
            print(f"⚠️ 分类不匹配")
            print(f"  缺失: {expected_categories - actual_categories}")
            print(f"  多余: {actual_categories - expected_categories}")
        
        if dict_count == 1124:
            print(f"✅ 节点数量正确")
        else:
            print(f"⚠️ 节点数量异常，期望1124，实际{dict_count}")
    else:
        print(f"❌ 没有找到Dictionary节点")

if __name__ == "__main__":
    main()
