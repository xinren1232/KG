#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from neo4j import GraphDatabase
from pathlib import Path
from datetime import datetime

class QuickGraphRebuilder:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="password123"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        
    def close(self):
        self.driver.close()
    
    def analyze_current_data(self):
        """分析当前数据"""
        print("🔍 分析当前图谱数据")
        print("=" * 50)
        
        with self.driver.session() as session:
            # 节点统计
            node_result = session.run("""
                MATCH (n)
                WHERE n:Component OR n:Symptom OR n:Tool OR n:Process OR n:TestCase OR n:Material OR n:Role OR n:Metric
                RETURN labels(n)[0] as label, count(n) as count
                ORDER BY count DESC
            """)
            
            total_nodes = 0
            print("📊 当前节点分布:")
            for record in node_result:
                count = record['count']
                total_nodes += count
                print(f"  {record['label']}: {count} 个")
            
            # 关系统计
            rel_result = session.run("""
                MATCH ()-[r]->()
                RETURN type(r) as rel_type, count(r) as count
                ORDER BY count DESC
            """)
            
            total_rels = 0
            print(f"\n🔗 当前关系分布:")
            for record in rel_result:
                count = record['count']
                total_rels += count
                print(f"  {record['rel_type']}: {count} 个")
            
            print(f"\n📈 当前总计:")
            print(f"  节点数: {total_nodes}")
            print(f"  关系数: {total_rels}")
            
            return total_nodes, total_rels
    
    def clear_all_data(self):
        """清空所有数据"""
        print("\n🧹 清空所有图谱数据")
        print("=" * 50)
        
        with self.driver.session() as session:
            # 删除所有关系
            rel_result = session.run("""
                MATCH ()-[r]->()
                DELETE r
                RETURN count(r) as deleted
            """)
            deleted_rels = rel_result.single()['deleted']
            
            # 删除所有相关节点
            node_result = session.run("""
                MATCH (n)
                WHERE n:Component OR n:Symptom OR n:Tool OR n:Process OR n:TestCase OR n:Material OR n:Role OR n:Metric
                DELETE n
                RETURN count(n) as deleted
            """)
            deleted_nodes = node_result.single()['deleted']
            
            print(f"✅ 已删除 {deleted_rels} 个关系")
            print(f"✅ 已删除 {deleted_nodes} 个节点")
            
            return deleted_nodes, deleted_rels
    
    def import_dictionary_data(self):
        """导入词典数据"""
        print("\n📥 导入词典数据")
        print("=" * 50)
        
        # 加载词典数据
        dict_file = Path("api/data/dictionary.json")
        if not dict_file.exists():
            print("❌ 词典文件不存在")
            return 0, {}
        
        with open(dict_file, 'r', encoding='utf-8') as f:
            dictionary_data = json.load(f)
        
        print(f"📚 准备导入 {len(dictionary_data)} 条词典数据")
        
        imported_count = 0
        category_counts = {}
        
        with self.driver.session() as session:
            for i, item in enumerate(dictionary_data):
                try:
                    term = item.get('term', f'term_{i}')
                    category = item.get('category', 'Component')
                    definition = item.get('definition', '')
                    aliases = item.get('aliases', [])
                    tags = item.get('tags', [])
                    
                    # 确保category是有效的标签
                    valid_categories = ['Component', 'Symptom', 'Tool', 'Process', 'TestCase', 'Material', 'Role', 'Metric']
                    if category not in valid_categories:
                        category = 'Component'
                    
                    # 处理标签和别名
                    if isinstance(aliases, str):
                        aliases = [aliases] if aliases else []
                    if isinstance(tags, str):
                        tags = [tags] if tags else []
                    
                    # 创建节点
                    session.run(f"""
                        CREATE (n:{category})
                        SET n.name = $term,
                            n.term = $term,
                            n.definition = $definition,
                            n.description = $definition,
                            n.aliases = $aliases,
                            n.tags = $tags,
                            n.category = $category,
                            n.source = 'dictionary',
                            n.created_at = datetime(),
                            n.updated_at = datetime()
                    """, term=term, definition=definition, aliases=aliases, tags=tags, category=category)
                    
                    imported_count += 1
                    category_counts[category] = category_counts.get(category, 0) + 1
                    
                    if imported_count % 100 == 0:
                        print(f"  已导入 {imported_count}/{len(dictionary_data)} 个节点")
                        
                except Exception as e:
                    print(f"❌ 导入节点失败: {item.get('term', f'item_{i}')} - {e}")
        
        print(f"\n✅ 词典数据导入完成:")
        print(f"  总计: {imported_count} 个节点")
        for category, count in sorted(category_counts.items()):
            print(f"  {category}: {count} 个")
        
        return imported_count, category_counts
    
    def create_smart_relationships(self):
        """创建智能关系"""
        print("\n🔗 创建智能关系")
        print("=" * 50)
        
        total_created = 0
        
        with self.driver.session() as session:
            # 1. Component -> Symptom (组件有症状)
            print("  创建 Component -> Symptom 关系...")
            result1 = session.run("""
                MATCH (c:Component), (s:Symptom)
                WHERE size(c.tags) > 0 AND size(s.tags) > 0
                WITH c, s, [tag IN c.tags WHERE tag IN s.tags] as common_tags
                WHERE size(common_tags) >= 1
                MERGE (c)-[r:HAS_SYMPTOM]->(s)
                SET r.confidence = toFloat(size(common_tags)) / 5.0,
                    r.source = 'tag_similarity',
                    r.created_at = datetime()
                RETURN count(r) as created
            """)
            created1 = result1.single()['created'] if result1.single() else 0
            total_created += created1
            print(f"    创建了 {created1} 个 HAS_SYMPTOM 关系")
            
            # 2. TestCase -> Tool (测试用例使用工具)
            print("  创建 TestCase -> Tool 关系...")
            result2 = session.run("""
                MATCH (tc:TestCase), (t:Tool)
                WHERE size(tc.tags) > 0 AND size(t.tags) > 0
                WITH tc, t, [tag IN tc.tags WHERE tag IN t.tags] as common_tags
                WHERE size(common_tags) >= 1
                MERGE (tc)-[r:USES_TOOL]->(t)
                SET r.confidence = toFloat(size(common_tags)) / 5.0,
                    r.source = 'tag_similarity',
                    r.created_at = datetime()
                RETURN count(r) as created
            """)
            created2 = result2.single()['created'] if result2.single() else 0
            total_created += created2
            print(f"    创建了 {created2} 个 USES_TOOL 关系")
            
            # 3. TestCase -> Metric (测试用例测量指标)
            print("  创建 TestCase -> Metric 关系...")
            result3 = session.run("""
                MATCH (tc:TestCase), (m:Metric)
                WHERE size(tc.tags) > 0 AND size(m.tags) > 0
                WITH tc, m, [tag IN tc.tags WHERE tag IN m.tags] as common_tags
                WHERE size(common_tags) >= 1
                MERGE (tc)-[r:MEASURES]->(m)
                SET r.confidence = toFloat(size(common_tags)) / 5.0,
                    r.source = 'tag_similarity',
                    r.created_at = datetime()
                RETURN count(r) as created
            """)
            created3 = result3.single()['created'] if result3.single() else 0
            total_created += created3
            print(f"    创建了 {created3} 个 MEASURES 关系")
            
            # 4. Process -> Material (流程使用材料)
            print("  创建 Process -> Material 关系...")
            result4 = session.run("""
                MATCH (p:Process), (m:Material)
                WHERE size(p.tags) > 0 AND size(m.tags) > 0
                WITH p, m, [tag IN p.tags WHERE tag IN m.tags] as common_tags
                WHERE size(common_tags) >= 1
                MERGE (p)-[r:USES_MATERIAL]->(m)
                SET r.confidence = toFloat(size(common_tags)) / 5.0,
                    r.source = 'tag_similarity',
                    r.created_at = datetime()
                RETURN count(r) as created
            """)
            created4 = result4.single()['created'] if result4.single() else 0
            total_created += created4
            print(f"    创建了 {created4} 个 USES_MATERIAL 关系")
            
            # 5. Process -> Tool (流程使用工具)
            print("  创建 Process -> Tool 关系...")
            result5 = session.run("""
                MATCH (p:Process), (t:Tool)
                WHERE size(p.tags) > 0 AND size(t.tags) > 0
                WITH p, t, [tag IN p.tags WHERE tag IN t.tags] as common_tags
                WHERE size(common_tags) >= 1
                MERGE (p)-[r:USES_TOOL]->(t)
                SET r.confidence = toFloat(size(common_tags)) / 5.0,
                    r.source = 'tag_similarity',
                    r.created_at = datetime()
                RETURN count(r) as created
            """)
            created5 = result5.single()['created'] if result5.single() else 0
            total_created += created5
            print(f"    创建了 {created5} 个 USES_TOOL 关系")
            
            # 6. Component -> Component (相关组件)
            print("  创建 Component -> Component 关系...")
            result6 = session.run("""
                MATCH (c1:Component), (c2:Component)
                WHERE id(c1) < id(c2)
                AND size(c1.tags) > 0 AND size(c2.tags) > 0
                WITH c1, c2, [tag IN c1.tags WHERE tag IN c2.tags] as common_tags
                WHERE size(common_tags) >= 2
                MERGE (c1)-[r:RELATED_TO]->(c2)
                SET r.confidence = toFloat(size(common_tags)) / 5.0,
                    r.source = 'tag_similarity',
                    r.created_at = datetime()
                RETURN count(r) as created
            """)
            created6 = result6.single()['created'] if result6.single() else 0
            total_created += created6
            print(f"    创建了 {created6} 个 RELATED_TO 关系")
        
        print(f"\n✅ 关系创建完成，总计: {total_created} 个")
        return total_created
    
    def verify_final_result(self):
        """验证最终结果"""
        print("\n🔍 验证最终结果")
        print("=" * 50)
        
        with self.driver.session() as session:
            # 节点统计
            node_result = session.run("""
                MATCH (n)
                WHERE n:Component OR n:Symptom OR n:Tool OR n:Process OR n:TestCase OR n:Material OR n:Role OR n:Metric
                RETURN labels(n)[0] as label, count(n) as count
                ORDER BY count DESC
            """)
            
            total_nodes = 0
            print("📊 最终节点分布:")
            for record in node_result:
                count = record['count']
                total_nodes += count
                print(f"  {record['label']}: {count} 个")
            
            # 关系统计
            rel_result = session.run("""
                MATCH ()-[r]->()
                RETURN type(r) as rel_type, count(r) as count
                ORDER BY count DESC
            """)
            
            total_rels = 0
            print(f"\n🔗 最终关系分布:")
            for record in rel_result:
                count = record['count']
                total_rels += count
                print(f"  {record['rel_type']}: {count} 个")
            
            print(f"\n📈 最终总计:")
            print(f"  节点数: {total_nodes}")
            print(f"  关系数: {total_rels}")
            
            # 验证结果
            if total_nodes == 1124:
                print(f"🎉 节点数完美！正好是1124条词典数据")
            elif abs(total_nodes - 1124) <= 10:
                print(f"✅ 节点数接近预期，差异在可接受范围内")
            else:
                print(f"⚠️ 节点数与预期差异较大")
            
            if total_rels >= 1000:
                print(f"🎉 关系数充足！")
            else:
                print(f"⚠️ 关系数较少，可能需要优化关系创建规则")
            
            return total_nodes, total_rels

def main():
    """主函数"""
    print("🎯 快速重建图谱数据")
    print("=" * 80)
    
    rebuilder = QuickGraphRebuilder()
    
    try:
        # 1. 分析当前数据
        current_nodes, current_rels = rebuilder.analyze_current_data()
        
        print(f"\n⚠️ 即将清空所有数据并重建")
        print(f"当前数据: {current_nodes} 个节点, {current_rels} 个关系")
        response = input("确认继续？(y/n): ").strip().lower()
        
        if response != 'y':
            print("❌ 用户取消操作")
            return
        
        # 2. 清空所有数据
        deleted_nodes, deleted_rels = rebuilder.clear_all_data()
        
        # 3. 导入词典数据
        imported_count, category_counts = rebuilder.import_dictionary_data()
        
        # 4. 创建智能关系
        relationships_created = rebuilder.create_smart_relationships()
        
        # 5. 验证结果
        final_nodes, final_rels = rebuilder.verify_final_result()
        
        # 6. 总结
        print(f"\n" + "=" * 80)
        print(f"🎉 图谱数据重建完成！")
        print(f"=" * 80)
        
        print(f"📊 重建统计:")
        print(f"  删除节点: {deleted_nodes} 个")
        print(f"  删除关系: {deleted_rels} 个")
        print(f"  导入节点: {imported_count} 个")
        print(f"  创建关系: {relationships_created} 个")
        
        print(f"\n📈 最终结果:")
        print(f"  总节点数: {final_nodes} (目标: 1124)")
        print(f"  总关系数: {final_rels}")
        
        if final_nodes == 1124:
            print(f"\n🎉 完美！图谱现在包含纯净的1124条词典数据")
        
        print(f"\n🌐 现在可以访问前端查看重建后的图谱:")
        print(f"  - 图谱可视化: http://localhost:5173/#/graph-visualization")
        print(f"  - 词典管理: http://localhost:5173/#/dictionary")
        
    except Exception as e:
        print(f"❌ 重建过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        rebuilder.close()

if __name__ == "__main__":
    main()
