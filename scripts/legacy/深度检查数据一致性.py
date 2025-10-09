#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
深度检查数据一致性 - 对比文件数据和Neo4j数据
"""

import json
from collections import Counter
from neo4j import GraphDatabase

def check_file_data():
    """检查文件中的数据"""
    print("📁 检查dictionary.json文件数据")
    print("=" * 40)
    
    try:
        with open('api/data/dictionary.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"📊 文件总条数: {len(data)}")
        
        # 统计分类
        categories = []
        for item in data:
            category = item.get('category', '')
            if category:
                categories.append(category)
        
        category_counts = Counter(categories)
        
        print(f"📊 文件中的分类分布:")
        for category, count in category_counts.most_common():
            print(f"  {category}: {count} 条")
        
        print(f"📊 文件中分类总数: {len(category_counts)}")
        
        # 检查是否有非标准分类
        expected_categories = {'Symptom', 'Component', 'Tool', 'Process', 'TestCase', 'Metric', 'Material', 'Role'}
        actual_categories = set(category_counts.keys())
        
        print(f"\n📊 分类对比:")
        print(f"  期望分类: {expected_categories}")
        print(f"  文件分类: {actual_categories}")
        print(f"  多余分类: {actual_categories - expected_categories}")
        print(f"  缺失分类: {expected_categories - actual_categories}")
        
        return data, category_counts
        
    except Exception as e:
        print(f"❌ 文件检查失败: {e}")
        return None, None

def check_neo4j_data():
    """检查Neo4j中的数据"""
    print("\n🗄️ 检查Neo4j数据")
    print("=" * 40)
    
    uri = "bolt://localhost:7687"
    username = "neo4j"
    password = "password123"
    
    try:
        driver = GraphDatabase.driver(uri, auth=(username, password))
        
        with driver.session() as session:
            # 检查Dictionary节点总数
            result = session.run("MATCH (d:Dictionary) RETURN count(d) as count")
            dict_count = result.single()["count"]
            print(f"📊 Neo4j Dictionary节点: {dict_count} 个")
            
            # 检查分类分布
            result = session.run("MATCH (d:Dictionary) RETURN d.category as category, count(d) as count ORDER BY count DESC")
            neo4j_categories = {}
            for record in result:
                category = record["category"]
                count = record["count"]
                neo4j_categories[category] = count
            
            print(f"📊 Neo4j中的分类分布:")
            for category, count in neo4j_categories.items():
                print(f"  {category}: {count} 条")
            
            print(f"📊 Neo4j分类总数: {len(neo4j_categories)}")
            
            return dict_count, neo4j_categories
            
    except Exception as e:
        print(f"❌ Neo4j检查失败: {e}")
        return 0, {}
    
    finally:
        if driver:
            driver.close()

def compare_data(file_data, file_categories, neo4j_count, neo4j_categories):
    """对比文件和Neo4j数据"""
    print(f"\n🔍 数据一致性对比")
    print("=" * 40)
    
    # 对比总数
    file_count = len(file_data) if file_data else 0
    print(f"📊 总数对比:")
    print(f"  文件: {file_count} 条")
    print(f"  Neo4j: {neo4j_count} 条")
    print(f"  一致性: {'✅' if file_count == neo4j_count else '❌'}")
    
    # 对比分类
    print(f"\n📊 分类对比:")
    all_categories = set(file_categories.keys()) | set(neo4j_categories.keys())
    
    inconsistent_categories = []
    for category in sorted(all_categories):
        file_count = file_categories.get(category, 0)
        neo4j_count = neo4j_categories.get(category, 0)
        status = "✅" if file_count == neo4j_count else "❌"
        print(f"  {category}: 文件{file_count} vs Neo4j{neo4j_count} {status}")
        
        if file_count != neo4j_count:
            inconsistent_categories.append(category)
    
    return inconsistent_categories

def fix_data_if_needed(inconsistent_categories):
    """如果需要，修复数据不一致问题"""
    if not inconsistent_categories:
        print(f"\n✅ 数据完全一致，无需修复")
        return True
    
    print(f"\n🔧 发现数据不一致，需要重新导入")
    print(f"不一致的分类: {inconsistent_categories}")
    
    # 重新导入数据
    print(f"\n🔄 开始重新导入数据...")
    
    uri = "bolt://localhost:7687"
    username = "neo4j"
    password = "password123"
    
    try:
        # 读取文件数据
        with open('api/data/dictionary.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        driver = GraphDatabase.driver(uri, auth=(username, password))
        
        with driver.session() as session:
            # 清理现有Dictionary节点
            print("🧹 清理现有Dictionary节点...")
            session.run("MATCH (d:Dictionary) DETACH DELETE d")
            
            # 重新导入数据
            print(f"📥 重新导入 {len(data)} 条数据...")
            
            batch_size = 50
            total_batches = (len(data) + batch_size - 1) // batch_size
            
            for batch_num in range(total_batches):
                start_idx = batch_num * batch_size
                end_idx = min(start_idx + batch_size, len(data))
                batch_data = data[start_idx:end_idx]
                
                # 清理批次数据
                clean_batch = []
                for item in batch_data:
                    clean_item = {
                        'term': item.get('term', '').strip(),
                        'category': item.get('category', '').strip(),
                        'description': item.get('description', '').strip(),
                        'aliases': [alias.strip() for alias in item.get('aliases', []) if alias and isinstance(alias, str)],
                        'tags': [tag.strip() for tag in item.get('tags', []) if tag and isinstance(tag, str)]
                    }
                    
                    if clean_item['term'] and clean_item['category']:
                        clean_batch.append(clean_item)
                
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
                
                session.run(query, batch=clean_batch)
                print(f"✅ 批次 {batch_num + 1}/{total_batches}: 已导入 {len(clean_batch)} 条")
            
            # 验证重新导入的结果
            result = session.run("MATCH (d:Dictionary) RETURN count(d) as count")
            final_count = result.single()["count"]
            print(f"📊 重新导入完成: {final_count} 个节点")
            
            return True
            
    except Exception as e:
        print(f"❌ 重新导入失败: {e}")
        return False
    
    finally:
        if driver:
            driver.close()

def main():
    """主函数"""
    print("🔍 深度检查数据一致性")
    print("=" * 50)
    
    # 1. 检查文件数据
    file_data, file_categories = check_file_data()
    
    # 2. 检查Neo4j数据
    neo4j_count, neo4j_categories = check_neo4j_data()
    
    # 3. 对比数据
    if file_data and neo4j_categories:
        inconsistent_categories = compare_data(file_data, file_categories, neo4j_count, neo4j_categories)
        
        # 4. 修复数据（如果需要）
        if inconsistent_categories:
            success = fix_data_if_needed(inconsistent_categories)
            if success:
                print(f"\n🎉 数据修复完成！")
                print(f"🌐 请刷新Neo4j浏览器查看更新结果")
            else:
                print(f"\n❌ 数据修复失败")
        else:
            print(f"\n✅ 数据完全一致！")
    
    print(f"\n" + "=" * 50)
    print(f"📊 检查完成")

if __name__ == "__main__":
    main()
