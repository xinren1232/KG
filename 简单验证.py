#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单验证Neo4j状态
"""

from neo4j import GraphDatabase

def simple_verify():
    """简单验证"""
    print("🔍 简单验证Neo4j状态")
    print("=" * 40)
    
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
            print(f"📊 Dictionary节点: {dict_count}")
            
            # 3. 检查标签
            result = session.run("CALL db.labels()")
            labels = [record["label"] for record in result]
            print(f"📊 所有标签: {labels}")
            
            # 4. 检查Dictionary节点的属性
            result = session.run("MATCH (d:Dictionary) RETURN d LIMIT 1")
            sample = result.single()
            if sample:
                sample_node = sample["d"]
                print(f"📋 示例节点属性: {list(sample_node.keys())}")
                print(f"📋 示例节点: {dict(sample_node)}")
            
            # 5. 尝试检查分类
            try:
                result = session.run("MATCH (d:Dictionary) WHERE d.category IS NOT NULL RETURN DISTINCT d.category as category")
                categories = [record["category"] for record in result]
                print(f"📊 发现的分类: {categories}")
                
                # 统计每个分类的数量
                for category in categories:
                    result = session.run("MATCH (d:Dictionary) WHERE d.category = $cat RETURN count(d) as count", cat=category)
                    count = result.single()["count"]
                    print(f"  {category}: {count} 条")
                    
            except Exception as e:
                print(f"⚠️ 分类查询失败: {e}")
            
            # 6. 最终评估
            if dict_count == 1124:
                print(f"\n🎉 验证成功!")
                print(f"✅ Dictionary节点数量正确: {dict_count}")
                print(f"✅ 数据已成功导入")
                
                if len(categories) == 8:
                    print(f"✅ 8个分类完整")
                else:
                    print(f"⚠️ 分类数量: {len(categories)}")
                
                return True
            else:
                print(f"\n❌ 验证失败")
                print(f"期望Dictionary节点: 1124")
                print(f"实际Dictionary节点: {dict_count}")
                return False
                
    except Exception as e:
        print(f"❌ 验证失败: {e}")
        return False
    
    finally:
        if driver:
            driver.close()

if __name__ == "__main__":
    success = simple_verify()
    
    print(f"\n" + "=" * 40)
    if success:
        print(f"🎉 图谱状态正常!")
        print(f"🌐 可以访问Neo4j浏览器查看: http://localhost:7474")
        print(f"🔍 推荐查询: MATCH (d:Dictionary) RETURN count(d);")
    else:
        print(f"⚠️ 需要进一步检查")
