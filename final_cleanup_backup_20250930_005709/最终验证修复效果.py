#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终验证修复效果
"""

from neo4j import GraphDatabase

def verify_fix():
    """验证修复效果"""
    print("🔍 最终验证修复效果")
    print("=" * 50)
    
    uri = "bolt://localhost:7687"
    username = "neo4j"
    password = "password123"
    
    try:
        driver = GraphDatabase.driver(uri, auth=(username, password))
        
        with driver.session() as session:
            # 1. 检查Dictionary总数
            result = session.run("MATCH (d:Dictionary) RETURN count(d) as count")
            dict_count = result.single()["count"]
            print(f"📊 Dictionary节点总数: {dict_count}")
            
            # 2. 检查各分类标签的节点数
            categories = ['Symptom', 'Component', 'Tool', 'Process', 'TestCase', 'Metric', 'Material', 'Role']
            
            print(f"\n📊 各分类标签节点数:")
            total_labeled = 0
            for category in categories:
                result = session.run(f"MATCH (n:{category}) RETURN count(n) as count")
                count = result.single()["count"]
                print(f"  {category}: {count} 个")
                total_labeled += count
            
            print(f"  总计: {total_labeled} 个")
            
            # 3. 检查分类属性分布
            result = session.run("MATCH (d:Dictionary) RETURN d.category as category, count(d) as count ORDER BY count DESC")
            
            print(f"\n📊 分类属性分布:")
            total_by_category = 0
            for record in result:
                category = record["category"]
                count = record["count"]
                print(f"  {category}: {count} 条")
                total_by_category += count
            
            print(f"  总计: {total_by_category} 条")
            
            # 4. 验证数据一致性
            print(f"\n✅ 数据一致性验证:")
            
            expected_counts = {
                'Symptom': 259,
                'Metric': 190,
                'Component': 181,
                'Process': 170,
                'TestCase': 104,
                'Tool': 102,
                'Role': 63,
                'Material': 55
            }
            
            all_correct = True
            
            for category, expected in expected_counts.items():
                result = session.run(f"MATCH (n:{category}) RETURN count(n) as count")
                actual = result.single()["count"]
                
                if actual == expected:
                    print(f"  ✅ {category}: {actual} (正确)")
                else:
                    print(f"  ❌ {category}: {actual} (期望{expected})")
                    all_correct = False
            
            # 5. 检查总数
            expected_total = sum(expected_counts.values())
            if dict_count == expected_total:
                print(f"  ✅ 总数: {dict_count} (正确)")
            else:
                print(f"  ❌ 总数: {dict_count} (期望{expected_total})")
                all_correct = False
            
            # 6. 最终结果
            print(f"\n" + "=" * 50)
            print(f"📊 最终验证结果")
            print(f"=" * 50)
            
            if all_correct:
                print(f"🎉 验证成功!")
                print(f"✅ 所有数据完全正确")
                print(f"✅ 分类标签已正确添加")
                print(f"✅ Neo4j浏览器应该正确显示8个分类")
                
                print(f"\n🌐 Neo4j浏览器验证:")
                print(f"  1. 访问: http://localhost:7474")
                print(f"  2. 用户名: neo4j")
                print(f"  3. 密码: password123")
                print(f"  4. 在Database information面板中应该看到:")
                print(f"     - Dictionary (1124)")
                print(f"     - Symptom (259)")
                print(f"     - Metric (190)")
                print(f"     - Component (181)")
                print(f"     - Process (170)")
                print(f"     - TestCase (104)")
                print(f"     - Tool (102)")
                print(f"     - Role (63)")
                print(f"     - Material (55)")
                
                return True
            else:
                print(f"❌ 验证失败")
                print(f"仍有数据不一致问题")
                return False
                
    except Exception as e:
        print(f"❌ 验证失败: {e}")
        return False
    
    finally:
        if driver:
            driver.close()

if __name__ == "__main__":
    verify_fix()
