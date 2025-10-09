#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import pandas as pd
from neo4j import GraphDatabase
from pathlib import Path
from datetime import datetime

class GraphDataRebuilder:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="password123"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        
    def close(self):
        self.driver.close()
    
    def backup_current_graph(self):
        """备份当前图谱数据"""
        print("💾 备份当前图谱数据")
        print("=" * 50)
        
        backup_data = {
            'backup_time': datetime.now().isoformat(),
            'nodes': [],
            'relationships': []
        }
        
        with self.driver.session() as session:
            # 备份所有节点
            nodes_result = session.run("""
                MATCH (n)
                WHERE n:Component OR n:Symptom OR n:Tool OR n:Process OR n:TestCase OR n:Material OR n:Role OR n:Metric
                RETURN id(n) as node_id, labels(n) as labels, properties(n) as props
            """)
            
            for record in nodes_result:
                backup_data['nodes'].append({
                    'id': record['node_id'],
                    'labels': record['labels'],
                    'properties': dict(record['props'])
                })
            
            # 备份所有关系
            rels_result = session.run("""
                MATCH (a)-[r]->(b)
                WHERE (a:Component OR a:Symptom OR a:Tool OR a:Process OR a:TestCase OR a:Material OR a:Role OR a:Metric)
                AND (b:Component OR b:Symptom OR b:Tool OR b:Process OR b:TestCase OR b:Material OR b:Role OR b:Metric)
                RETURN id(a) as source_id, type(r) as rel_type, id(b) as target_id, properties(r) as props
            """)
            
            for record in rels_result:
                backup_data['relationships'].append({
                    'source_id': record['source_id'],
                    'type': record['rel_type'],
                    'target_id': record['target_id'],
                    'properties': dict(record['props'])
                })
        
        # 保存备份文件
        backup_file = f"graph_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 备份完成: {backup_file}")
        print(f"  节点数: {len(backup_data['nodes'])}")
        print(f"  关系数: {len(backup_data['relationships'])}")
        
        return backup_file
    
    def analyze_current_data(self):
        """分析当前数据，识别词典数据和原有数据"""
        print("\n🔍 分析当前图谱数据")
        print("=" * 50)
        
        # 加载词典数据作为参考
        dict_file = Path("api/data/dictionary.json")
        if not dict_file.exists():
            print("❌ 词典文件不存在")
            return None, None
        
        with open(dict_file, 'r', encoding='utf-8') as f:
            dictionary_data = json.load(f)
        
        dict_terms = {item.get('term', '') for item in dictionary_data}
        print(f"📚 词典数据: {len(dict_terms)} 个术语")
        
        # 分析图谱中的节点
        with self.driver.session() as session:
            result = session.run("""
                MATCH (n)
                WHERE n:Component OR n:Symptom OR n:Tool OR n:Process OR n:TestCase OR n:Material OR n:Role OR n:Metric
                RETURN id(n) as node_id, labels(n)[0] as label, 
                       coalesce(n.name, n.term, '') as name,
                       properties(n) as props
            """)
            
            graph_nodes = list(result)
            
        # 分类节点
        dict_nodes = []  # 来自词典的节点
        legacy_nodes = []  # 原有的节点
        
        for node in graph_nodes:
            name = node['name']
            props = dict(node['props'])
            
            # 判断是否来自词典数据
            if name in dict_terms:
                dict_nodes.append(node)
            else:
                # 检查是否有词典数据的特征（如term字段）
                if 'term' in props and props['term'] in dict_terms:
                    dict_nodes.append(node)
                else:
                    legacy_nodes.append(node)
        
        print(f"\n📊 数据分析结果:")
        print(f"  总节点数: {len(graph_nodes)}")
        print(f"  词典节点: {len(dict_nodes)} 个")
        print(f"  原有节点: {len(legacy_nodes)} 个")
        
        if legacy_nodes:
            print(f"\n🔍 原有节点示例 (前10个):")
            for node in legacy_nodes[:10]:
                print(f"  - {node['name']} ({node['label']}) [ID: {node['node_id']}]")
        
        return dict_nodes, legacy_nodes
    
    def clear_all_graph_data(self):
        """清空所有图谱数据"""
        print("\n🧹 清空所有图谱数据")
        print("=" * 50)
        
        with self.driver.session() as session:
            # 删除所有关系
            rel_result = session.run("""
                MATCH ()-[r]->()
                DELETE r
                RETURN count(r) as deleted_rels
            """)
            deleted_rels = rel_result.single()['deleted_rels']
            
            # 删除所有节点
            node_result = session.run("""
                MATCH (n)
                WHERE n:Component OR n:Symptom OR n:Tool OR n:Process OR n:TestCase OR n:Material OR n:Role OR n:Metric
                DELETE n
                RETURN count(n) as deleted_nodes
            """)
            deleted_nodes = node_result.single()['deleted_nodes']
            
            print(f"✅ 已删除 {deleted_rels} 个关系")
            print(f"✅ 已删除 {deleted_nodes} 个节点")
            
            return deleted_nodes, deleted_rels
    
    def import_clean_dictionary_data(self):
        """导入纯净的词典数据"""
        print("\n📥 导入纯净的词典数据")
        print("=" * 50)
        
        # 加载词典数据
        dict_file = Path("api/data/dictionary.json")
        with open(dict_file, 'r', encoding='utf-8') as f:
            dictionary_data = json.load(f)
        
        print(f"📚 准备导入 {len(dictionary_data)} 条词典数据")
        
        imported_count = 0
        category_counts = {}
        
        with self.driver.session() as session:
            for item in dictionary_data:
                try:
                    term = item.get('term', '')
                    category = item.get('category', 'Unknown')
                    definition = item.get('definition', '')
                    aliases = item.get('aliases', [])
                    tags = item.get('tags', [])
                    
                    # 确保category是有效的标签
                    valid_categories = ['Component', 'Symptom', 'Tool', 'Process', 'TestCase', 'Material', 'Role', 'Metric']
                    if category not in valid_categories:
                        category = 'Component'  # 默认分类
                    
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
                    print(f"❌ 导入节点失败: {item.get('term', 'Unknown')} - {e}")
        
        print(f"\n✅ 词典数据导入完成:")
        print(f"  总计: {imported_count} 个节点")
        for category, count in sorted(category_counts.items()):
            print(f"  {category}: {count} 个")
        
        return imported_count, category_counts
    
    def create_basic_relationships(self):
        """创建基本关系"""
        print("\n🔗 创建基本关系")
        print("=" * 50)
        
        relationships_created = 0
        
        with self.driver.session() as session:
            # 1. 基于标签创建关系
            print("  创建基于标签的关系...")
            
            # Component -> Symptom (基于共同标签)
            result1 = session.run("""
                MATCH (c:Component), (s:Symptom)
                WHERE any(tag IN c.tags WHERE tag IN s.tags)
                AND size(c.tags) > 0 AND size(s.tags) > 0
                WITH c, s, [tag IN c.tags WHERE tag IN s.tags] as common_tags
                WHERE size(common_tags) >= 1
                MERGE (c)-[r:HAS_SYMPTOM]->(s)
                SET r.confidence = toFloat(size(common_tags)) / 10.0,
                    r.source = 'tag_similarity',
                    r.common_tags = common_tags,
                    r.created_at = datetime()
                RETURN count(r) as created
            """)
            created1 = result1.single()['created'] if result1.single() else 0
            relationships_created += created1
            print(f"    Component->Symptom: {created1} 个")
            
            # TestCase -> Tool (测试用例使用工具)
            result2 = session.run("""
                MATCH (tc:TestCase), (t:Tool)
                WHERE any(tag IN tc.tags WHERE tag IN t.tags)
                AND size(tc.tags) > 0 AND size(t.tags) > 0
                WITH tc, t, [tag IN tc.tags WHERE tag IN t.tags] as common_tags
                WHERE size(common_tags) >= 1
                MERGE (tc)-[r:USES_TOOL]->(t)
                SET r.confidence = toFloat(size(common_tags)) / 10.0,
                    r.source = 'tag_similarity',
                    r.common_tags = common_tags,
                    r.created_at = datetime()
                RETURN count(r) as created
            """)
            created2 = result2.single()['created'] if result2.single() else 0
            relationships_created += created2
            print(f"    TestCase->Tool: {created2} 个")
            
            # TestCase -> Metric (测试用例测量指标)
            result3 = session.run("""
                MATCH (tc:TestCase), (m:Metric)
                WHERE any(tag IN tc.tags WHERE tag IN m.tags)
                AND size(tc.tags) > 0 AND size(m.tags) > 0
                WITH tc, m, [tag IN tc.tags WHERE tag IN m.tags] as common_tags
                WHERE size(common_tags) >= 1
                MERGE (tc)-[r:MEASURES]->(m)
                SET r.confidence = toFloat(size(common_tags)) / 10.0,
                    r.source = 'tag_similarity',
                    r.common_tags = common_tags,
                    r.created_at = datetime()
                RETURN count(r) as created
            """)
            created3 = result3.single()['created'] if result3.single() else 0
            relationships_created += created3
            print(f"    TestCase->Metric: {created3} 个")
            
            # Process -> Material (流程使用材料)
            result4 = session.run("""
                MATCH (p:Process), (m:Material)
                WHERE any(tag IN p.tags WHERE tag IN m.tags)
                AND size(p.tags) > 0 AND size(m.tags) > 0
                WITH p, m, [tag IN p.tags WHERE tag IN m.tags] as common_tags
                WHERE size(common_tags) >= 1
                MERGE (p)-[r:USES_MATERIAL]->(m)
                SET r.confidence = toFloat(size(common_tags)) / 10.0,
                    r.source = 'tag_similarity',
                    r.common_tags = common_tags,
                    r.created_at = datetime()
                RETURN count(r) as created
            """)
            created4 = result4.single()['created'] if result4.single() else 0
            relationships_created += created4
            print(f"    Process->Material: {created4} 个")
            
            # Process -> Tool (流程使用工具)
            result5 = session.run("""
                MATCH (p:Process), (t:Tool)
                WHERE any(tag IN p.tags WHERE tag IN t.tags)
                AND size(p.tags) > 0 AND size(t.tags) > 0
                WITH p, t, [tag IN p.tags WHERE tag IN t.tags] as common_tags
                WHERE size(common_tags) >= 1
                MERGE (p)-[r:USES_TOOL]->(t)
                SET r.confidence = toFloat(size(common_tags)) / 10.0,
                    r.source = 'tag_similarity',
                    r.common_tags = common_tags,
                    r.created_at = datetime()
                RETURN count(r) as created
            """)
            created5 = result5.single()['created'] if result5.single() else 0
            relationships_created += created5
            print(f"    Process->Tool: {created5} 个")
        
        print(f"\n✅ 关系创建完成，总计: {relationships_created} 个")
        return relationships_created
    
    def verify_rebuilt_data(self):
        """验证重建后的数据"""
        print("\n🔍 验证重建后的数据")
        print("=" * 50)
        
        with self.driver.session() as session:
            # 节点统计
            node_stats = session.run("""
                MATCH (n)
                WHERE n:Component OR n:Symptom OR n:Tool OR n:Process OR n:TestCase OR n:Material OR n:Role OR n:Metric
                RETURN labels(n)[0] as label, count(n) as count
                ORDER BY count DESC
            """)
            
            total_nodes = 0
            print("📊 节点分布:")
            for record in node_stats:
                count = record['count']
                total_nodes += count
                print(f"  {record['label']}: {count} 个")
            
            # 关系统计
            rel_stats = session.run("""
                MATCH ()-[r]->()
                RETURN type(r) as rel_type, count(r) as count
                ORDER BY count DESC
            """)
            
            total_rels = 0
            print(f"\n🔗 关系分布:")
            for record in rel_stats:
                count = record['count']
                total_rels += count
                print(f"  {record['rel_type']}: {count} 个")
            
            print(f"\n📈 总计:")
            print(f"  节点数: {total_nodes}")
            print(f"  关系数: {total_rels}")
            
            # 验证是否符合预期
            if total_nodes == 1124:
                print(f"✅ 节点数正确！正好是1124条词典数据")
            else:
                print(f"⚠️ 节点数异常，预期1124，实际{total_nodes}")
            
            if total_rels > 1000:
                print(f"✅ 关系数充足！")
            else:
                print(f"⚠️ 关系数较少，可能需要更多关系规则")
            
            return total_nodes, total_rels

def main():
    """主函数"""
    print("🎯 清理并重建图谱数据")
    print("=" * 80)
    
    rebuilder = GraphDataRebuilder()
    
    try:
        # 1. 备份当前数据
        backup_file = rebuilder.backup_current_graph()
        
        # 2. 分析当前数据
        dict_nodes, legacy_nodes = rebuilder.analyze_current_data()
        
        if legacy_nodes:
            print(f"\n⚠️ 发现 {len(legacy_nodes)} 个原有节点需要清理")
            response = input("是否继续清理并重建？(y/n): ").strip().lower()
            
            if response != 'y':
                print("❌ 用户取消操作")
                return
        
        # 3. 清空所有数据
        deleted_nodes, deleted_rels = rebuilder.clear_all_graph_data()
        
        # 4. 导入纯净的词典数据
        imported_count, category_counts = rebuilder.import_clean_dictionary_data()
        
        # 5. 创建基本关系
        relationships_created = rebuilder.create_basic_relationships()
        
        # 6. 验证重建结果
        final_nodes, final_rels = rebuilder.verify_rebuilt_data()
        
        # 7. 总结
        print(f"\n" + "=" * 80)
        print(f"🎉 图谱数据重建完成！")
        print(f"=" * 80)
        
        print(f"📊 重建统计:")
        print(f"  删除原有节点: {deleted_nodes} 个")
        print(f"  删除原有关系: {deleted_rels} 个")
        print(f"  导入词典节点: {imported_count} 个")
        print(f"  创建新关系: {relationships_created} 个")
        
        print(f"\n📈 最终结果:")
        print(f"  总节点数: {final_nodes} (预期: 1124)")
        print(f"  总关系数: {final_rels}")
        
        print(f"\n💾 备份文件: {backup_file}")
        print(f"🌐 现在可以访问前端查看重建后的图谱数据")
        
    except Exception as e:
        print(f"❌ 重建过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        rebuilder.close()

if __name__ == "__main__":
    main()
