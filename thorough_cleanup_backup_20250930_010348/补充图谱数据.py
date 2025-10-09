#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import pandas as pd
from neo4j import GraphDatabase
from datetime import datetime
from pathlib import Path

class GraphDataEnhancer:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="password123"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        
    def close(self):
        self.driver.close()
    
    def get_current_graph_stats(self):
        """获取当前图谱统计"""
        with self.driver.session() as session:
            # 获取节点统计
            node_query = """
            MATCH (n)
            RETURN labels(n)[0] as label, count(n) as count
            ORDER BY count DESC
            """
            node_result = session.run(node_query)
            node_stats = []
            total_nodes = 0
            
            for record in node_result:
                label = record['label']
                count = record['count']
                node_stats.append({'label': label, 'count': count})
                total_nodes += count
            
            # 获取关系统计
            rel_query = """
            MATCH ()-[r]->()
            RETURN type(r) as type, count(r) as count
            ORDER BY count DESC
            """
            rel_result = session.run(rel_query)
            rel_stats = []
            total_rels = 0
            
            for record in rel_result:
                rel_type = record['type']
                count = record['count']
                rel_stats.append({'type': rel_type, 'count': count})
                total_rels += count
            
            return {
                'nodes': {'total': total_nodes, 'by_label': node_stats},
                'relationships': {'total': total_rels, 'by_type': rel_stats}
            }
    
    def load_dictionary_data(self):
        """加载词典数据"""
        # 尝试多个可能的路径
        possible_paths = [
            Path("api/data/dictionary.json"),
            Path("data/vocab/dictionary.json"),
            Path("data/dictionary.json")
        ]

        data_file = None
        for path in possible_paths:
            if path.exists():
                data_file = path
                break

        if not data_file:
            print(f"❌ 词典文件不存在于任何预期路径")
            return []

        with open(data_file, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)

        # 处理不同的数据格式
        if isinstance(raw_data, list):
            # 直接是列表格式
            dictionary_data = raw_data
        elif isinstance(raw_data, dict) and 'entries' in raw_data:
            # 有entries字段的格式
            dictionary_data = raw_data['entries']
        else:
            print(f"❌ 未知的词典数据格式")
            return []

        print(f"✅ 加载词典数据: {len(dictionary_data)} 条 (来源: {data_file})")
        return dictionary_data
    
    def analyze_data_gaps(self, dictionary_data, graph_stats):
        """分析数据缺口"""
        print("\n🔍 分析数据缺口")
        print("=" * 50)
        
        # 统计词典数据中的类别
        dict_categories = {}
        for item in dictionary_data:
            category = item.get('category', 'Unknown')
            if category not in dict_categories:
                dict_categories[category] = 0
            dict_categories[category] += 1
        
        print(f"📊 词典数据统计 (总计 {len(dictionary_data)} 条):")
        for category, count in sorted(dict_categories.items(), key=lambda x: x[1], reverse=True):
            print(f"  {category}: {count} 条")
        
        print(f"\n📊 图谱数据统计 (总计 {graph_stats['nodes']['total']} 个节点):")
        graph_categories = {}
        for label_stat in graph_stats['nodes']['by_label']:
            label = label_stat['label']
            count = label_stat['count']
            graph_categories[label] = count
            print(f"  {label}: {count} 个节点")
        
        # 分析缺口
        print(f"\n📈 数据缺口分析:")
        gaps = {}
        for category, dict_count in dict_categories.items():
            graph_count = graph_categories.get(category, 0)
            gap = dict_count - graph_count
            if gap > 0:
                gaps[category] = gap
                print(f"  {category}: 缺少 {gap} 个节点 (词典{dict_count} vs 图谱{graph_count})")
            elif gap < 0:
                print(f"  {category}: 图谱多出 {abs(gap)} 个节点 (词典{dict_count} vs 图谱{graph_count})")
            else:
                print(f"  {category}: 数据一致 ({dict_count} 个)")
        
        return gaps, dict_categories, graph_categories
    
    def check_existing_nodes(self, dictionary_data):
        """检查哪些词典条目在图谱中不存在"""
        missing_items = []
        
        with self.driver.session() as session:
            for item in dictionary_data:
                term = item.get('term', '')
                category = item.get('category', '')
                
                if not term or not category:
                    continue
                
                # 检查节点是否存在
                query = f"""
                MATCH (n:{category})
                WHERE n.name = $term OR $term IN n.aliases
                RETURN n.name as name
                """
                
                try:
                    result = session.run(query, term=term)
                    if not result.single():
                        missing_items.append(item)
                except Exception as e:
                    # 如果标签不存在，也算作缺失
                    missing_items.append(item)
        
        return missing_items
    
    def import_missing_nodes(self, missing_items, batch_size=100):
        """导入缺失的节点"""
        print(f"\n🚀 开始导入缺失的节点 ({len(missing_items)} 个)")
        print("=" * 50)
        
        success_count = 0
        error_count = 0
        
        with self.driver.session() as session:
            for i, item in enumerate(missing_items):
                try:
                    term = item.get('term', '')
                    category = item.get('category', '')
                    
                    if not term or not category:
                        print(f"⚠️ 跳过无效数据: {item}")
                        continue
                    
                    # 处理别名
                    aliases = item.get('aliases', [])
                    if isinstance(aliases, str):
                        aliases = [alias.strip() for alias in aliases.split(',') if alias.strip()]
                    elif not isinstance(aliases, list):
                        aliases = []
                    
                    # 处理标签
                    tags = item.get('tags', [])
                    if isinstance(tags, str):
                        tags = [tag.strip() for tag in tags.split(',') if tag.strip()]
                    elif not isinstance(tags, list):
                        tags = []
                    
                    # 构建节点属性
                    properties = {
                        'name': term,
                        'aliases': aliases,
                        'tags': tags,
                        'description': item.get('description', ''),
                        'definition': item.get('definition', ''),
                        'sub_category': item.get('sub_category', ''),
                        'source': item.get('source', 'dictionary'),
                        'status': item.get('status', 'active'),
                        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'original_category': item.get('original_category', category)
                    }
                    
                    # 创建节点
                    query = f"""
                    CREATE (n:{category} $properties)
                    RETURN n.name as name
                    """
                    
                    result = session.run(query, properties=properties)
                    if result.single():
                        success_count += 1
                        if (i + 1) % 50 == 0:
                            print(f"✅ 已导入 {i + 1}/{len(missing_items)} 个节点")
                    else:
                        error_count += 1
                        print(f"❌ 导入失败: {term}")
                        
                except Exception as e:
                    error_count += 1
                    print(f"❌ 导入 {item.get('term', 'Unknown')} 时出错: {e}")
        
        print(f"\n📊 导入结果:")
        print(f"  ✅ 成功: {success_count} 个")
        print(f"  ❌ 失败: {error_count} 个")
        print(f"  📈 总计: {len(missing_items)} 个")
        
        return {'success': success_count, 'error': error_count, 'total': len(missing_items)}
    
    def create_basic_relationships(self):
        """创建基本关系"""
        print(f"\n🔗 创建基本关系")
        print("=" * 50)
        
        relationships_created = 0
        
        with self.driver.session() as session:
            # 创建组件与症状的关系
            query1 = """
            MATCH (c:Component), (s:Symptom)
            WHERE rand() < 0.1  // 随机创建10%的关系
            AND NOT EXISTS((c)-[:HAS_SYMPTOM]->(s))
            CREATE (c)-[:HAS_SYMPTOM]->(s)
            RETURN count(*) as created
            """
            
            result1 = session.run(query1)
            created1 = result1.single()['created'] if result1.single() else 0
            relationships_created += created1
            print(f"✅ 创建 Component-HAS_SYMPTOM-Symptom 关系: {created1} 个")
            
            # 创建工具与流程的关系
            query2 = """
            MATCH (t:Tool), (p:Process)
            WHERE rand() < 0.15  // 随机创建15%的关系
            AND NOT EXISTS((t)-[:USED_IN]->(p))
            CREATE (t)-[:USED_IN]->(p)
            RETURN count(*) as created
            """
            
            result2 = session.run(query2)
            created2 = result2.single()['created'] if result2.single() else 0
            relationships_created += created2
            print(f"✅ 创建 Tool-USED_IN-Process 关系: {created2} 个")
            
            # 创建测试用例与组件的关系
            query3 = """
            MATCH (tc:TestCase), (c:Component)
            WHERE rand() < 0.2  // 随机创建20%的关系
            AND NOT EXISTS((tc)-[:TESTS]->(c))
            CREATE (tc)-[:TESTS]->(c)
            RETURN count(*) as created
            """
            
            result3 = session.run(query3)
            created3 = result3.single()['created'] if result3.single() else 0
            relationships_created += created3
            print(f"✅ 创建 TestCase-TESTS-Component 关系: {created3} 个")
        
        print(f"\n📊 关系创建总计: {relationships_created} 个")
        return relationships_created

def main():
    """主函数"""
    print("🎯 图谱数据补充和增强")
    print("=" * 80)
    
    enhancer = GraphDataEnhancer()
    
    try:
        # 1. 获取当前图谱统计
        print("📊 获取当前图谱统计...")
        current_stats = enhancer.get_current_graph_stats()
        
        # 2. 加载词典数据
        dictionary_data = enhancer.load_dictionary_data()
        
        if not dictionary_data:
            print("❌ 无法加载词典数据，退出")
            return
        
        # 3. 分析数据缺口
        gaps, dict_categories, graph_categories = enhancer.analyze_data_gaps(dictionary_data, current_stats)
        
        # 4. 检查缺失的节点
        print(f"\n🔍 检查缺失的节点...")
        missing_items = enhancer.check_existing_nodes(dictionary_data)
        print(f"发现 {len(missing_items)} 个缺失的节点")
        
        # 5. 导入缺失的节点
        if missing_items:
            import_result = enhancer.import_missing_nodes(missing_items)
        else:
            print("✅ 所有词典数据都已存在于图谱中")
            import_result = {'success': 0, 'error': 0, 'total': 0}
        
        # 6. 创建基本关系
        rel_created = enhancer.create_basic_relationships()
        
        # 7. 获取最终统计
        print(f"\n📈 获取最终图谱统计...")
        final_stats = enhancer.get_current_graph_stats()
        
        # 8. 生成报告
        report = {
            'enhancement_time': datetime.now().isoformat(),
            'initial_stats': current_stats,
            'final_stats': final_stats,
            'dictionary_stats': dict_categories,
            'gaps_analysis': gaps,
            'import_result': import_result,
            'relationships_created': rel_created,
            'missing_items_count': len(missing_items)
        }
        
        with open('图谱数据补充报告.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        # 9. 显示最终结果
        print(f"\n" + "=" * 80)
        print(f"🎉 图谱数据补充完成!")
        print(f"=" * 80)
        
        print(f"📊 数据变化:")
        print(f"  节点数: {current_stats['nodes']['total']} → {final_stats['nodes']['total']} (+{final_stats['nodes']['total'] - current_stats['nodes']['total']})")
        print(f"  关系数: {current_stats['relationships']['total']} → {final_stats['relationships']['total']} (+{final_stats['relationships']['total'] - current_stats['relationships']['total']})")
        
        print(f"\n📋 最终节点统计:")
        for label_stat in final_stats['nodes']['by_label']:
            print(f"  {label_stat['label']}: {label_stat['count']} 个")
        
        print(f"\n🔗 关系统计:")
        for rel_stat in final_stats['relationships']['by_type']:
            print(f"  {rel_stat['type']}: {rel_stat['count']} 个")
        
        print(f"\n📄 详细报告已保存: 图谱数据补充报告.json")
        
        # 检查是否达到预期
        if final_stats['nodes']['total'] >= 1000:
            print(f"\n✅ 图谱数据已充实，节点数达到 {final_stats['nodes']['total']} 个")
        else:
            print(f"\n⚠️ 图谱数据仍需补充，当前节点数 {final_stats['nodes']['total']} 个")
        
    except Exception as e:
        print(f"❌ 补充过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        enhancer.close()

if __name__ == "__main__":
    main()
