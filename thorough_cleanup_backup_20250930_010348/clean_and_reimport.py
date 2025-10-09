#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理并重新导入正确数据 - 解决节点数量和分类问题
"""

import json
from pathlib import Path
from neo4j import GraphDatabase

def clean_and_reimport():
    """清理并重新导入正确数据"""
    print("🧹 清理并重新导入正确数据")
    print("=" * 50)
    
    # 连接数据库
    uri = "bolt://localhost:7687"
    username = "neo4j"
    password = "password123"
    
    try:
        driver = GraphDatabase.driver(uri, auth=(username, password))
        print(f"✅ Neo4j连接成功")
        
        with driver.session() as session:
            # 1. 检查当前状态
            print("🔍 检查当前数据状态...")
            
            # 检查所有节点类型
            result = session.run("CALL db.labels()")
            labels = [record["label"] for record in result]
            print(f"📊 当前节点标签: {labels}")
            
            # 检查各类型节点数量
            for label in labels:
                result = session.run(f"MATCH (n:{label}) RETURN count(n) as count")
                count = result.single()["count"]
                print(f"  {label}: {count} 个")
            
            # 2. 完全清理数据库
            print("\n🧹 完全清理数据库...")
            
            # 删除所有节点和关系
            session.run("MATCH (n) DETACH DELETE n")
            print("✅ 所有节点和关系已删除")
            
            # 3. 验证清理结果
            result = session.run("MATCH (n) RETURN count(n) as count")
            remaining_count = result.single()["count"]
            print(f"📊 清理后剩余节点: {remaining_count} 个")
            
            # 4. 读取正确的词典数据
            print("\n📖 读取词典数据...")
            data_file = Path("api/data/dictionary.json")
            
            if not data_file.exists():
                print(f"❌ 词典文件不存在: {data_file}")
                return False
            
            with open(data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            print(f"📊 词典数据: {len(data)} 条")
            
            # 验证数据格式
            valid_categories = {'Symptom', 'Component', 'Tool', 'Process', 'TestCase', 'Metric', 'Material', 'Role'}
            
            # 过滤和清理数据
            clean_data = []
            category_counts = {}
            
            for item in data:
                category = item.get('category', '')
                if category in valid_categories:
                    clean_item = {
                        'term': item.get('term', '').strip(),
                        'category': category,
                        'description': item.get('description', '').strip(),
                        'aliases': [alias.strip() for alias in item.get('aliases', []) if alias and isinstance(alias, str)],
                        'tags': [tag.strip() for tag in item.get('tags', []) if tag and isinstance(tag, str)]
                    }
                    
                    # 确保term不为空
                    if clean_item['term']:
                        clean_data.append(clean_item)
                        category_counts[category] = category_counts.get(category, 0) + 1
            
            print(f"📊 清理后数据: {len(clean_data)} 条")
            print(f"📊 分类分布:")
            for category, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
                print(f"  {category}: {count} 条")
            
            # 5. 创建约束和索引
            print("\n🔧 创建约束和索引...")
            try:
                session.run("CREATE CONSTRAINT dictionary_term_unique IF NOT EXISTS FOR (d:Dictionary) REQUIRE d.term IS UNIQUE")
                print("✅ 唯一约束创建成功")
            except Exception as e:
                print(f"⚠️ 约束已存在: {e}")

            try:
                session.run("CREATE INDEX dictionary_category_index IF NOT EXISTS FOR (d:Dictionary) ON (d.category)")
                print("✅ 分类索引创建成功")
            except Exception as e:
                print(f"⚠️ 分类索引已存在: {e}")

            try:
                session.run("CREATE INDEX dictionary_tags_index IF NOT EXISTS FOR (d:Dictionary) ON (d.tags)")
                print("✅ 标签索引创建成功")
            except Exception as e:
                print(f"⚠️ 标签索引已存在: {e}")

            print("✅ 约束和索引处理完成")
            
            # 6. 分批导入清理后的数据
            print(f"\n📥 开始导入 {len(clean_data)} 条清理数据...")
            
            batch_size = 50
            total_batches = (len(clean_data) + batch_size - 1) // batch_size
            imported_count = 0
            
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
                imported_count += len(batch_data)
                
                print(f"✅ 批次 {batch_num + 1}/{total_batches}: 已导入 {imported_count}/{len(clean_data)} 条")
            
            # 7. 验证最终结果
            print(f"\n🔍 验证最终结果...")
            
            # 检查总数
            result = session.run("MATCH (d:Dictionary) RETURN count(d) as total")
            final_count = result.single()["total"]
            print(f"📊 Dictionary节点总数: {final_count}")
            
            # 检查分类分布
            result = session.run("MATCH (d:Dictionary) RETURN d.category as category, count(d) as count ORDER BY count DESC")
            print(f"📊 最终分类分布:")
            
            final_category_stats = {}
            for record in result:
                category = record["category"]
                count = record["count"]
                final_category_stats[category] = count
                print(f"  {category}: {count} 条")
            
            # 检查节点标签
            result = session.run("CALL db.labels()")
            final_labels = [record["label"] for record in result]
            print(f"📊 最终节点标签: {final_labels}")
            
            # 8. 最终验证
            success = (
                final_count == len(clean_data) and
                len(final_labels) == 1 and
                final_labels[0] == "Dictionary" and
                len(final_category_stats) <= 8
            )
            
            if success:
                print(f"\n🎉 数据清理和重新导入成功!")
                print(f"✅ Dictionary节点: {final_count} 个")
                print(f"✅ 节点标签: 仅Dictionary (正确)")
                print(f"✅ 分类数量: {len(final_category_stats)} 个")
                print(f"✅ 数据质量: 完全清洁")
                
                return True
            else:
                print(f"\n⚠️ 验证发现问题:")
                print(f"  期望节点数: {len(clean_data)}, 实际: {final_count}")
                print(f"  期望标签: ['Dictionary'], 实际: {final_labels}")
                print(f"  期望分类数: ≤8, 实际: {len(final_category_stats)}")
                
                return False
                
    except Exception as e:
        print(f"❌ 操作失败: {e}")
        return False
    
    finally:
        if driver:
            driver.close()

def main():
    """主函数"""
    success = clean_and_reimport()
    
    print(f"\n" + "=" * 50)
    print(f"📊 操作结果")
    print(f"=" * 50)
    
    if success:
        print(f"✅ 清理和重新导入成功!")
        print(f"\n🌐 现在可以验证:")
        print(f"  1. Neo4j浏览器: http://localhost:7474")
        print(f"  2. 应该看到正确的节点数量")
        print(f"  3. 只有Dictionary标签")
        print(f"  4. 8个标准分类")
    else:
        print(f"❌ 清理和重新导入失败")

if __name__ == "__main__":
    main()
