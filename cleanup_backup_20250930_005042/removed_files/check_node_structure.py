#!/usr/bin/env python3
"""
检查Neo4j中节点的实际结构
"""

from neo4j import GraphDatabase

def check_node_structure():
    """检查节点结构"""
    driver = None
    try:
        # 连接Neo4j
        driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'password123'))
        
        with driver.session() as session:
            print("🔍 检查节点标签结构")
            print("=" * 50)
            
            # 检查所有标签组合
            print("\n📊 标签组合统计:")
            label_result = session.run("""
                MATCH (n) 
                RETURN DISTINCT labels(n) as labels, count(n) as count 
                ORDER BY count DESC
            """)
            
            for record in label_result:
                labels = record["labels"]
                count = record["count"]
                print(f"  {labels}: {count}个")
            
            # 检查节点属性
            print("\n📋 节点属性示例:")
            sample_result = session.run("""
                MATCH (n) 
                RETURN labels(n) as labels, properties(n) as props
                LIMIT 5
            """)
            
            for i, record in enumerate(sample_result, 1):
                labels = record["labels"]
                props = record["props"]
                print(f"\n  节点 {i}:")
                print(f"    标签: {labels}")
                print(f"    属性: {list(props.keys())}")
                if 'name' in props:
                    print(f"    名称: {props['name']}")
                if 'term' in props:
                    print(f"    术语: {props['term']}")
            
            # 检查特定标签的节点
            print("\n🎯 检查特定标签:")
            for label in ['Component', 'Symptom', 'Tool', 'TestCase', 'Process', 'Metric']:
                result = session.run(f"""
                    MATCH (n:{label}) 
                    RETURN count(n) as count, 
                           collect(n.name)[0..3] as sample_names,
                           collect(n.term)[0..3] as sample_terms
                """)
                
                record = result.single()
                if record and record["count"] > 0:
                    count = record["count"]
                    names = [n for n in record["sample_names"] if n]
                    terms = [t for t in record["sample_terms"] if t]
                    print(f"  {label}: {count}个")
                    if names:
                        print(f"    示例名称: {names}")
                    if terms:
                        print(f"    示例术语: {terms}")
                else:
                    print(f"  {label}: 0个")
            
            # 检查Dictionary标签
            print("\n🔍 检查Dictionary标签:")
            dict_result = session.run("""
                MATCH (n:Dictionary) 
                RETURN labels(n) as labels, count(n) as count
            """)
            
            dict_found = False
            for record in dict_result:
                dict_found = True
                labels = record["labels"]
                count = record["count"]
                print(f"  Dictionary节点: {count}个，标签: {labels}")
            
            if not dict_found:
                print("  ❌ 没有找到Dictionary标签的节点")
                print("  💡 这解释了为什么关系导入失败")
                
        print("\n🎯 结论:")
        print("  如果没有Dictionary标签，需要修改关系导入脚本")
        print("  或者为现有节点添加Dictionary标签")
                
    except Exception as e:
        print(f"❌ 检查失败: {e}")
        
    finally:
        if driver:
            driver.close()

if __name__ == "__main__":
    check_node_structure()
