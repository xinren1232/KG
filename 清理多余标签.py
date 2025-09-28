#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理Neo4j中的多余标签，只保留8个标准分类
"""

from neo4j import GraphDatabase

def clean_extra_labels():
    """清理多余的标签"""
    print("🧹 清理Neo4j中的多余标签")
    print("=" * 50)
    
    uri = "bolt://localhost:7687"
    username = "neo4j"
    password = "password123"
    
    # 标准的8个分类标签
    standard_labels = {'Symptom', 'Component', 'Tool', 'Process', 'TestCase', 'Metric', 'Material', 'Role', 'Dictionary'}
    
    # 需要清理的多余标签
    extra_labels = {'Anomaly', 'Product', 'Term'}
    
    try:
        driver = GraphDatabase.driver(uri, auth=(username, password))
        
        with driver.session() as session:
            # 1. 查看当前所有标签
            print("📊 当前所有标签:")
            result = session.run("CALL db.labels()")
            current_labels = set()
            for record in result:
                label = record[0]
                current_labels.add(label)
                
                # 检查每个标签的节点数
                count_result = session.run(f"MATCH (n:{label}) RETURN count(n) as count")
                count = count_result.single()["count"]
                
                if label in standard_labels:
                    print(f"  ✅ {label}: {count} 个节点 (保留)")
                else:
                    print(f"  ❌ {label}: {count} 个节点 (需清理)")
            
            # 2. 识别需要清理的标签
            labels_to_clean = current_labels - standard_labels
            
            if labels_to_clean:
                print(f"\n🔧 开始清理多余标签: {labels_to_clean}")
                
                for label in labels_to_clean:
                    # 检查该标签的节点数
                    count_result = session.run(f"MATCH (n:{label}) RETURN count(n) as count")
                    count = count_result.single()["count"]
                    
                    if count > 0:
                        print(f"⚠️ 标签 {label} 有 {count} 个节点，需要处理")
                        
                        # 检查这些节点是否也有Dictionary标签
                        dict_check = session.run(f"MATCH (n:{label}:Dictionary) RETURN count(n) as count")
                        dict_count = dict_check.single()["count"]
                        
                        if dict_count == count:
                            # 所有节点都有Dictionary标签，可以安全移除多余标签
                            print(f"🔄 移除标签 {label} (所有节点都有Dictionary标签)")
                            session.run(f"MATCH (n:{label}) REMOVE n:{label}")
                        else:
                            # 有些节点没有Dictionary标签，需要删除这些节点
                            non_dict_count = count - dict_count
                            print(f"🗑️ 删除 {non_dict_count} 个非Dictionary的 {label} 节点")
                            session.run(f"MATCH (n:{label}) WHERE NOT n:Dictionary DETACH DELETE n")
                            
                            if dict_count > 0:
                                print(f"🔄 移除剩余 {dict_count} 个节点的 {label} 标签")
                                session.run(f"MATCH (n:{label}:Dictionary) REMOVE n:{label}")
                    else:
                        print(f"✅ 标签 {label} 没有节点，无需处理")
                
                print(f"\n🧹 清理完成")
            else:
                print(f"\n✅ 没有发现多余标签")
            
            # 3. 验证清理结果
            print(f"\n🔍 验证清理结果:")
            result = session.run("CALL db.labels()")
            final_labels = []
            
            for record in result:
                label = record[0]
                count_result = session.run(f"MATCH (n:{label}) RETURN count(n) as count")
                count = count_result.single()["count"]
                
                if count > 0:  # 只显示有节点的标签
                    final_labels.append((label, count))
                    print(f"  📊 {label}: {count} 个节点")
            
            # 4. 检查是否只剩下标准标签
            final_label_names = {label for label, count in final_labels}
            unexpected_labels = final_label_names - standard_labels
            
            if unexpected_labels:
                print(f"\n⚠️ 仍有意外标签: {unexpected_labels}")
                return False
            else:
                print(f"\n✅ 清理成功！只剩下标准标签")
                
                # 验证标准分类的节点数
                expected_counts = {
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
                
                print(f"\n📊 标准分类验证:")
                all_correct = True
                
                for label, expected in expected_counts.items():
                    actual = next((count for name, count in final_labels if name == label), 0)
                    
                    if actual == expected:
                        print(f"  ✅ {label}: {actual} (正确)")
                    else:
                        print(f"  ❌ {label}: {actual} (期望{expected})")
                        all_correct = False
                
                return all_correct
                
    except Exception as e:
        print(f"❌ 清理失败: {e}")
        return False
    
    finally:
        if driver:
            driver.close()

def main():
    """主函数"""
    print("🎯 开始清理Neo4j多余标签")
    
    success = clean_extra_labels()
    
    print(f"\n" + "=" * 50)
    print(f"📊 清理结果")
    print(f"=" * 50)
    
    if success:
        print(f"🎉 清理成功!")
        print(f"✅ 只保留了8个标准分类 + Dictionary标签")
        print(f"✅ 所有节点数量正确")
        
        print(f"\n🌐 现在Neo4j浏览器应该只显示:")
        print(f"  - Dictionary (1124)")
        print(f"  - Symptom (259)")
        print(f"  - Metric (190)")
        print(f"  - Component (181)")
        print(f"  - Process (170)")
        print(f"  - TestCase (104)")
        print(f"  - Tool (102)")
        print(f"  - Role (63)")
        print(f"  - Material (55)")
        
        print(f"\n🔄 请刷新Neo4j浏览器页面查看结果")
        
    else:
        print(f"❌ 清理失败或仍有问题")
        print(f"请检查错误信息并重试")

if __name__ == "__main__":
    main()
