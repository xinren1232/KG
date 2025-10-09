#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
彻底清理Neo4j中的空标签定义
"""

from neo4j import GraphDatabase

def remove_empty_labels():
    """删除空标签定义"""
    print("🗑️ 彻底清理Neo4j中的空标签定义")
    print("=" * 50)
    
    uri = "bolt://localhost:7687"
    username = "neo4j"
    password = "password123"
    
    try:
        driver = GraphDatabase.driver(uri, auth=(username, password))
        
        with driver.session() as session:
            # 1. 查看当前所有标签
            print("📊 检查当前所有标签:")
            result = session.run("CALL db.labels()")
            all_labels = []
            empty_labels = []
            
            for record in result:
                label = record[0]
                count_result = session.run(f"MATCH (n:{label}) RETURN count(n) as count")
                count = count_result.single()["count"]
                
                all_labels.append((label, count))
                
                if count == 0:
                    empty_labels.append(label)
                    print(f"  🗑️ {label}: {count} 个节点 (空标签)")
                else:
                    print(f"  ✅ {label}: {count} 个节点")
            
            # 2. 如果有空标签，尝试清理
            if empty_labels:
                print(f"\n🔧 发现 {len(empty_labels)} 个空标签: {empty_labels}")
                print(f"⚠️ 注意: Neo4j不能直接删除标签定义，但可以通过以下方式清理:")
                
                # 方法1: 重启Neo4j服务会自动清理未使用的标签
                print(f"\n💡 推荐解决方案:")
                print(f"  1. 重启Neo4j服务")
                print(f"  2. 或者等待Neo4j自动清理未使用的标签")
                
                # 方法2: 创建临时节点然后删除（强制清理）
                print(f"\n🔄 尝试强制清理空标签...")
                
                for label in empty_labels:
                    try:
                        # 创建一个临时节点
                        session.run(f"CREATE (temp:{label} {{temp: true}})")
                        # 立即删除
                        session.run(f"MATCH (temp:{label} {{temp: true}}) DELETE temp")
                        print(f"  ✅ 已处理空标签: {label}")
                    except Exception as e:
                        print(f"  ⚠️ 处理 {label} 时出错: {e}")
                
            else:
                print(f"\n✅ 没有发现空标签")
            
            # 3. 最终验证
            print(f"\n🔍 最终验证:")
            result = session.run("CALL db.labels()")
            final_labels = []
            
            for record in result:
                label = record[0]
                count_result = session.run(f"MATCH (n:{label}) RETURN count(n) as count")
                count = count_result.single()["count"]
                
                if count > 0:
                    final_labels.append((label, count))
                    print(f"  📊 {label}: {count} 个节点")
                else:
                    print(f"  🗑️ {label}: {count} 个节点 (仍为空)")
            
            # 4. 检查是否只有我们期望的标签
            expected_labels = {
                'Dictionary': 1124,
                'Symptom': 259,
                'Metric': 190,
                'Component': 181,
                'Process': 170,
                'TestCase': 104,
                'Tool': 102,
                'Role': 63,
                'Material': 55
            }
            
            print(f"\n📊 期望的标签验证:")
            all_correct = True
            
            for label, expected_count in expected_labels.items():
                actual_count = next((count for name, count in final_labels if name == label), 0)
                
                if actual_count == expected_count:
                    print(f"  ✅ {label}: {actual_count}")
                else:
                    print(f"  ❌ {label}: {actual_count} (期望{expected_count})")
                    all_correct = False
            
            return all_correct, len([label for label, count in final_labels])
                
    except Exception as e:
        print(f"❌ 操作失败: {e}")
        return False, 0
    
    finally:
        if driver:
            driver.close()

def main():
    """主函数"""
    success, label_count = remove_empty_labels()
    
    print(f"\n" + "=" * 50)
    print(f"📊 清理结果")
    print(f"=" * 50)
    
    if success:
        print(f"🎉 验证成功!")
        print(f"✅ 所有期望的标签都存在且数量正确")
        print(f"📊 当前有效标签数: {label_count}")
        
        if label_count == 9:  # 8个分类 + Dictionary
            print(f"✅ 标签数量完全正确")
        else:
            print(f"⚠️ 标签数量为 {label_count}，可能仍有空标签残留")
            print(f"💡 建议重启Neo4j服务以完全清理空标签")
        
        print(f"\n🌐 Neo4j浏览器验证:")
        print(f"  1. 刷新浏览器页面: http://localhost:7474")
        print(f"  2. 查看Database Information面板")
        print(f"  3. 应该只看到9个标签（8个分类 + Dictionary）")
        
    else:
        print(f"❌ 验证失败")
        print(f"请检查Neo4j连接和数据状态")
    
    print(f"\n💡 如果仍看到空标签，请尝试:")
    print(f"  1. 重启Neo4j服务")
    print(f"  2. 刷新浏览器页面")
    print(f"  3. 空标签会在Neo4j重启后自动清理")

if __name__ == "__main__":
    main()
