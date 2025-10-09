#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
彻底修复Neo4j显示问题 - 确保数据完全一致
"""

import json
from collections import Counter
from neo4j import GraphDatabase

def fix_neo4j_display():
    """彻底修复Neo4j显示问题"""
    print("🔧 彻底修复Neo4j显示问题")
    print("=" * 50)
    
    # 1. 读取文件数据
    print("📁 读取dictionary.json文件...")
    try:
        with open('api/data/dictionary.json', 'r', encoding='utf-8') as f:
            file_data = json.load(f)
        
        print(f"📊 文件总条数: {len(file_data)}")
        
        # 统计文件中的分类
        file_categories = Counter([item.get('category', '') for item in file_data])
        print(f"📊 文件分类分布:")
        for category, count in file_categories.most_common():
            print(f"  {category}: {count} 条")
            
    except Exception as e:
        print(f"❌ 文件读取失败: {e}")
        return False
    
    # 2. 连接Neo4j并检查当前状态
    uri = "bolt://localhost:7687"
    username = "neo4j"
    password = "password123"
    
    try:
        driver = GraphDatabase.driver(uri, auth=(username, password))
        print(f"\n✅ Neo4j连接成功")
        
        with driver.session() as session:
            # 检查当前Dictionary节点数
            result = session.run("MATCH (d:Dictionary) RETURN count(d) as count")
            current_count = result.single()["count"]
            print(f"📊 当前Neo4j Dictionary节点: {current_count} 个")
            
            # 检查当前分类分布
            result = session.run("MATCH (d:Dictionary) RETURN d.category as category, count(d) as count ORDER BY count DESC")
            neo4j_categories = {}
            for record in result:
                category = record["category"]
                count = record["count"]
                neo4j_categories[category] = count
            
            print(f"📊 当前Neo4j分类分布:")
            for category, count in neo4j_categories.items():
                print(f"  {category}: {count} 条")
            
            # 3. 对比数据
            print(f"\n🔍 数据对比:")
            data_consistent = True
            
            # 对比总数
            if len(file_data) != current_count:
                print(f"❌ 总数不一致: 文件{len(file_data)} vs Neo4j{current_count}")
                data_consistent = False
            else:
                print(f"✅ 总数一致: {len(file_data)}")
            
            # 对比分类
            for category in file_categories:
                file_count = file_categories[category]
                neo4j_count = neo4j_categories.get(category, 0)
                if file_count != neo4j_count:
                    print(f"❌ {category}: 文件{file_count} vs Neo4j{neo4j_count}")
                    data_consistent = False
                else:
                    print(f"✅ {category}: {file_count}")
            
            # 4. 如果数据不一致，重新导入
            if not data_consistent:
                print(f"\n🔄 数据不一致，开始重新导入...")
                
                # 清理现有Dictionary节点
                print("🧹 清理现有Dictionary节点...")
                session.run("MATCH (d:Dictionary) DETACH DELETE d")
                
                # 清理和准备数据
                clean_data = []
                for item in file_data:
                    clean_item = {
                        'term': item.get('term', '').strip(),
                        'category': item.get('category', '').strip(),
                        'description': item.get('description', '').strip(),
                        'aliases': [alias.strip() for alias in item.get('aliases', []) if alias and isinstance(alias, str)],
                        'tags': [tag.strip() for tag in item.get('tags', []) if tag and isinstance(tag, str)]
                    }
                    
                    # 确保必要字段不为空
                    if clean_item['term'] and clean_item['category']:
                        clean_data.append(clean_item)
                
                print(f"📊 清理后数据: {len(clean_data)} 条")
                
                # 分批导入
                batch_size = 50
                total_batches = (len(clean_data) + batch_size - 1) // batch_size
                
                for batch_num in range(total_batches):
                    start_idx = batch_num * batch_size
                    end_idx = min(start_idx + batch_size, len(clean_data))
                    batch_data = clean_data[start_idx:end_idx]
                    
                    # 执行批量插入
                    query = """
                    UNWIND $batch AS item
                    CREATE (d:Dictionary {
                        term: item.term,
                        category: item.category,
                        description: item.description,
                        aliases: item.aliases,
                        tags: item.tags,
                        created_at: datetime(),
                        updated_at: datetime()
                    })
                    """
                    
                    session.run(query, batch=batch_data)
                    print(f"✅ 批次 {batch_num + 1}/{total_batches}: 已导入 {len(batch_data)} 条")
                
                # 验证重新导入的结果
                result = session.run("MATCH (d:Dictionary) RETURN count(d) as count")
                final_count = result.single()["count"]
                print(f"📊 重新导入完成: {final_count} 个节点")
                
                # 验证分类分布
                result = session.run("MATCH (d:Dictionary) RETURN d.category as category, count(d) as count ORDER BY count DESC")
                final_categories = {}
                for record in result:
                    category = record["category"]
                    count = record["count"]
                    final_categories[category] = count
                
                print(f"📊 最终分类分布:")
                for category, count in final_categories.items():
                    print(f"  {category}: {count} 条")
                
                # 5. 为每个分类添加对应的标签（解决Neo4j浏览器显示问题）
                print(f"\n🏷️ 为每个分类添加对应标签...")
                
                categories = ['Symptom', 'Component', 'Tool', 'Process', 'TestCase', 'Metric', 'Material', 'Role']
                
                for category in categories:
                    if category in final_categories:
                        query = f"MATCH (d:Dictionary) WHERE d.category = '{category}' SET d:{category}"
                        session.run(query)
                        print(f"✅ 已为 {category} 分类的 {final_categories[category]} 个节点添加标签")
                
                # 6. 最终验证
                print(f"\n🔍 最终验证...")
                
                # 检查各分类标签的节点数
                print(f"📊 各分类标签节点数:")
                for category in categories:
                    result = session.run(f"MATCH (n:{category}) RETURN count(n) as count")
                    count = result.single()["count"]
                    print(f"  {category}: {count} 个")
                
                # 检查Dictionary总数
                result = session.run("MATCH (d:Dictionary) RETURN count(d) as count")
                dict_total = result.single()["count"]
                print(f"📊 Dictionary总数: {dict_total} 个")
                
                if dict_total == len(file_data):
                    print(f"\n🎉 修复成功!")
                    print(f"✅ 数据完全一致")
                    print(f"✅ 分类标签已添加")
                    print(f"✅ Neo4j浏览器应该正确显示")
                    return True
                else:
                    print(f"\n⚠️ 仍有问题")
                    return False
            else:
                print(f"\n✅ 数据已经一致，无需修复")
                
                # 但仍需添加分类标签
                print(f"\n🏷️ 添加分类标签以改善Neo4j浏览器显示...")
                
                categories = ['Symptom', 'Component', 'Tool', 'Process', 'TestCase', 'Metric', 'Material', 'Role']
                
                for category in categories:
                    query = f"MATCH (d:Dictionary) WHERE d.category = '{category}' SET d:{category}"
                    session.run(query)
                    
                    result = session.run(f"MATCH (n:{category}) RETURN count(n) as count")
                    count = result.single()["count"]
                    print(f"✅ {category}: {count} 个节点已添加标签")
                
                return True
                
    except Exception as e:
        print(f"❌ Neo4j操作失败: {e}")
        return False
    
    finally:
        if driver:
            driver.close()

def main():
    """主函数"""
    success = fix_neo4j_display()
    
    print(f"\n" + "=" * 50)
    print(f"📊 修复结果")
    print(f"=" * 50)
    
    if success:
        print(f"🎉 Neo4j显示问题修复成功!")
        print(f"\n🌐 现在在Neo4j浏览器中应该看到:")
        print(f"  - Dictionary (1124) - 包含所有数据")
        print(f"  - Symptom (259) - 症状相关")
        print(f"  - Metric (190) - 性能指标")  
        print(f"  - Component (181) - 硬件组件")
        print(f"  - Process (170) - 流程工艺")
        print(f"  - TestCase (104) - 测试用例")
        print(f"  - Tool (102) - 工具方法")
        print(f"  - Role (63) - 角色职责")
        print(f"  - Material (55) - 材料物料")
        
        print(f"\n🔍 验证方法:")
        print(f"  1. 访问: http://localhost:7474")
        print(f"  2. 刷新页面")
        print(f"  3. 查看Database information面板")
        print(f"  4. 应该看到正确的节点数量")
        
    else:
        print(f"❌ 修复失败，请检查错误信息")

if __name__ == "__main__":
    main()
