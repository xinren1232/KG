#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from neo4j import GraphDatabase
from collections import defaultdict, Counter
from pathlib import Path

class GraphDataQualityChecker:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="password123"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        
    def close(self):
        self.driver.close()
    
    def check_node_duplicates(self):
        """检查节点重复情况"""
        print("🔍 检查节点重复情况")
        print("=" * 60)
        
        with self.driver.session() as session:
            # 检查同名节点
            duplicate_query = """
            MATCH (n)
            WHERE n:Component OR n:Symptom OR n:Tool OR n:Process OR n:TestCase OR n:Material OR n:Role OR n:Metric
            WITH n.name as name, labels(n)[0] as label, count(n) as count, collect(id(n)) as node_ids
            WHERE count > 1
            RETURN name, label, count, node_ids
            ORDER BY count DESC
            """
            
            result = session.run(duplicate_query)
            duplicates = list(result)
            
            if duplicates:
                print(f"❌ 发现 {len(duplicates)} 组重复节点:")
                total_duplicate_nodes = 0
                for record in duplicates:
                    name = record['name']
                    label = record['label']
                    count = record['count']
                    node_ids = record['node_ids']
                    total_duplicate_nodes += count - 1  # 减去1个保留的
                    print(f"  '{name}' ({label}): {count} 个重复 - IDs: {node_ids}")
                
                print(f"\n📊 重复统计:")
                print(f"  重复组数: {len(duplicates)}")
                print(f"  多余节点数: {total_duplicate_nodes}")
                print(f"  去重后预期节点数: {1350 - total_duplicate_nodes}")
                
                return duplicates, total_duplicate_nodes
            else:
                print("✅ 没有发现重复节点")
                return [], 0
    
    def check_dictionary_coverage(self):
        """检查词典数据覆盖情况"""
        print("\n🔍 检查词典数据覆盖情况")
        print("=" * 60)
        
        # 加载词典数据
        dict_file = Path("api/data/dictionary.json")
        if not dict_file.exists():
            print("❌ 词典文件不存在")
            return
        
        with open(dict_file, 'r', encoding='utf-8') as f:
            dictionary_data = json.load(f)
        
        print(f"📚 词典数据: {len(dictionary_data)} 条")
        
        # 统计词典中的类别
        dict_categories = Counter()
        dict_terms = set()
        for item in dictionary_data:
            category = item.get('category', 'Unknown')
            term = item.get('term', '')
            dict_categories[category] += 1
            dict_terms.add(term)
        
        print(f"📊 词典类别分布:")
        for category, count in dict_categories.most_common():
            print(f"  {category}: {count} 条")
        
        # 检查图谱中的覆盖情况
        with self.driver.session() as session:
            graph_categories = Counter()
            graph_terms = set()
            
            for category in dict_categories.keys():
                if category in ['Component', 'Symptom', 'Tool', 'Process', 'TestCase', 'Material', 'Role', 'Metric']:
                    query = f"""
                    MATCH (n:{category})
                    RETURN n.name as name
                    """
                    result = session.run(query)
                    category_terms = [record['name'] for record in result]
                    graph_categories[category] = len(category_terms)
                    graph_terms.update(category_terms)
        
        print(f"\n📊 图谱类别分布:")
        for category, count in graph_categories.most_common():
            print(f"  {category}: {count} 个节点")
        
        # 分析覆盖情况
        print(f"\n📈 覆盖情况分析:")
        missing_terms = dict_terms - graph_terms
        extra_terms = graph_terms - dict_terms
        
        print(f"  词典术语总数: {len(dict_terms)}")
        print(f"  图谱术语总数: {len(graph_terms)}")
        print(f"  缺失术语数: {len(missing_terms)}")
        print(f"  额外术语数: {len(extra_terms)}")
        
        if missing_terms:
            print(f"\n❌ 缺失的术语 (前10个):")
            for term in list(missing_terms)[:10]:
                print(f"    - {term}")
        
        if extra_terms:
            print(f"\n⚠️ 额外的术语 (前10个):")
            for term in list(extra_terms)[:10]:
                print(f"    - {term}")
        
        return missing_terms, extra_terms
    
    def check_relationship_types(self):
        """检查关系类型情况"""
        print("\n🔍 检查关系类型情况")
        print("=" * 60)
        
        with self.driver.session() as session:
            # 获取所有关系类型
            rel_query = """
            MATCH ()-[r]->()
            RETURN type(r) as rel_type, count(r) as count
            ORDER BY count DESC
            """
            
            result = session.run(rel_query)
            relationships = list(result)
            
            total_rels = sum(record['count'] for record in relationships)
            
            print(f"📊 关系类型统计 (总计 {total_rels} 个关系):")
            for record in relationships:
                rel_type = record['rel_type']
                count = record['count']
                percentage = (count / total_rels * 100) if total_rels > 0 else 0
                print(f"  {rel_type}: {count} 个 ({percentage:.1f}%)")
            
            # 检查是否有其他类型的关系应该存在
            print(f"\n🔍 检查预期的关系类型:")
            expected_relations = [
                'HAS_SYMPTOM', 'CAUSES', 'USED_IN', 'TESTS', 'MEASURES',
                'BELONGS_TO', 'RELATED_TO', 'PART_OF', 'REQUIRES'
            ]
            
            existing_types = {record['rel_type'] for record in relationships}
            missing_types = set(expected_relations) - existing_types
            
            if missing_types:
                print(f"❌ 缺失的关系类型:")
                for rel_type in missing_types:
                    print(f"    - {rel_type}")
            else:
                print(f"✅ 所有预期关系类型都存在")
            
            return relationships, missing_types
    
    def analyze_relationship_distribution(self):
        """分析关系分布的合理性"""
        print("\n🔍 分析关系分布合理性")
        print("=" * 60)
        
        with self.driver.session() as session:
            # 检查各类别节点的关系数量
            categories = ['Component', 'Symptom', 'Tool', 'Process', 'TestCase', 'Material', 'Role', 'Metric']
            
            for category in categories:
                # 出度关系
                out_query = f"""
                MATCH (n:{category})-[r]->()
                RETURN count(r) as out_count
                """
                out_result = session.run(out_query)
                out_count = out_result.single()['out_count'] if out_result.single() else 0
                
                # 入度关系
                in_query = f"""
                MATCH ()-[r]->(n:{category})
                RETURN count(r) as in_count
                """
                in_result = session.run(in_query)
                in_count = in_result.single()['in_count'] if in_result.single() else 0
                
                # 节点数量
                node_query = f"""
                MATCH (n:{category})
                RETURN count(n) as node_count
                """
                node_result = session.run(node_query)
                node_count = node_result.single()['node_count'] if node_result.single() else 0
                
                avg_out = out_count / node_count if node_count > 0 else 0
                avg_in = in_count / node_count if node_count > 0 else 0
                
                print(f"  {category} ({node_count} 个节点):")
                print(f"    出度关系: {out_count} 个 (平均 {avg_out:.1f}/节点)")
                print(f"    入度关系: {in_count} 个 (平均 {avg_in:.1f}/节点)")
    
    def suggest_cleanup_actions(self, duplicates, missing_types):
        """建议清理操作"""
        print("\n💡 建议的清理操作")
        print("=" * 60)
        
        actions = []
        
        if duplicates:
            actions.append("1. 清理重复节点")
            print("1. 清理重复节点:")
            print("   - 保留每组重复节点中的一个")
            print("   - 合并重复节点的关系")
            print("   - 删除多余的节点")
        
        if missing_types:
            actions.append("2. 恢复缺失的关系类型")
            print("2. 恢复缺失的关系类型:")
            for rel_type in missing_types:
                print(f"   - 重新创建 {rel_type} 关系")
        
        if len(actions) == 0:
            print("✅ 数据质量良好，无需特殊清理操作")
        
        return actions

def main():
    """主函数"""
    print("🎯 图谱数据质量检查")
    print("=" * 80)
    
    checker = GraphDataQualityChecker()
    
    try:
        # 1. 检查节点重复
        duplicates, duplicate_count = checker.check_node_duplicates()
        
        # 2. 检查词典覆盖
        missing_terms, extra_terms = checker.check_dictionary_coverage()
        
        # 3. 检查关系类型
        relationships, missing_rel_types = checker.check_relationship_types()
        
        # 4. 分析关系分布
        checker.analyze_relationship_distribution()
        
        # 5. 建议清理操作
        actions = checker.suggest_cleanup_actions(duplicates, missing_rel_types)
        
        # 6. 生成报告
        report = {
            'check_time': '2025-09-28',
            'node_analysis': {
                'total_nodes': 1350,
                'expected_from_dict': 1124,
                'duplicates_found': len(duplicates),
                'duplicate_nodes_count': duplicate_count,
                'missing_terms_count': len(missing_terms),
                'extra_terms_count': len(extra_terms)
            },
            'relationship_analysis': {
                'total_relationships': sum(r['count'] for r in relationships),
                'relationship_types': len(relationships),
                'missing_rel_types': list(missing_rel_types)
            },
            'recommended_actions': actions
        }
        
        with open('图谱数据质量检查报告.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        # 7. 总结
        print(f"\n" + "=" * 80)
        print(f"📊 数据质量检查总结")
        print(f"=" * 80)
        
        print(f"🔢 节点分析:")
        print(f"  当前节点数: 1350")
        print(f"  词典数据: 1124 条")
        print(f"  重复节点: {duplicate_count} 个")
        print(f"  预期去重后: {1350 - duplicate_count} 个")
        
        print(f"\n🔗 关系分析:")
        total_rels = sum(r['count'] for r in relationships)
        print(f"  当前关系数: {total_rels}")
        print(f"  关系类型数: {len(relationships)}")
        print(f"  缺失关系类型: {len(missing_rel_types)} 个")
        
        if duplicate_count > 0 or missing_rel_types:
            print(f"\n⚠️ 发现数据质量问题，建议执行清理操作")
        else:
            print(f"\n✅ 数据质量良好")
        
        print(f"\n📄 详细报告已保存: 图谱数据质量检查报告.json")
        
    except Exception as e:
        print(f"❌ 检查过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        checker.close()

if __name__ == "__main__":
    main()
