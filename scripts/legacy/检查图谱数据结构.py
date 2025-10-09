#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from neo4j import GraphDatabase
import json

def analyze_graph_structure():
    """分析图谱数据结构"""
    driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'password123'))
    
    try:
        with driver.session() as session:
            print("=== 图谱数据结构分析 ===")
            
            # 1. 节点类型统计
            print("\n1. 节点类型统计:")
            node_stats = session.run("""
                CALL db.labels() YIELD label
                CALL {
                    WITH label
                    MATCH (n)
                    WHERE label IN labels(n)
                    RETURN count(n) as count
                }
                RETURN label, count
                ORDER BY count DESC
            """)
            
            for record in node_stats:
                print(f"  {record['label']}: {record['count']}")
            
            # 2. 关系类型统计
            print("\n2. 关系类型统计:")
            rel_stats = session.run("""
                MATCH ()-[r]->() 
                RETURN type(r) AS type, count(r) AS count 
                ORDER BY count DESC
            """)
            
            for record in rel_stats:
                print(f"  {record['type']}: {record['count']}")
            
            # 3. 分类分布
            print("\n3. Dictionary分类分布:")
            category_stats = session.run("""
                MATCH (d:Dictionary) 
                RETURN d.category AS category, count(d) AS count 
                ORDER BY count DESC
            """)
            
            categories = []
            for record in category_stats:
                categories.append({"name": record['category'], "count": record['count']})
                print(f"  {record['category']}: {record['count']}")
            
            # 4. 热门标签
            print("\n4. 热门标签 (前20个):")
            tag_stats = session.run("""
                MATCH (d:Dictionary)-[:HAS_TAG]->(t:Tag)
                RETURN t.name AS tag, count(d) AS count
                ORDER BY count DESC
                LIMIT 20
            """)
            
            tags = []
            for record in tag_stats:
                tags.append({"name": record['tag'], "count": record['count']})
                print(f"  {record['tag']}: {record['count']}")
            
            # 5. 获取示例节点和关系用于可视化
            print("\n5. 获取示例数据用于可视化:")
            sample_data = session.run("""
                MATCH (d:Dictionary)
                WHERE d.category IN ['Component', 'Symptom', 'Tool', 'Process']
                WITH d, rand() AS r
                ORDER BY r
                LIMIT 20
                OPTIONAL MATCH (d)-[rel]->(target)
                RETURN d.term AS term, d.category AS category, d.description AS description,
                       collect({type: type(rel), target: target.name}) AS relations
            """)
            
            sample_nodes = []
            sample_relations = []
            
            for record in sample_data:
                node = {
                    "id": f"dict_{len(sample_nodes)}",
                    "name": record['term'],
                    "category": record['category'],
                    "description": record['description'][:100] + "..." if len(record['description']) > 100 else record['description']
                }
                sample_nodes.append(node)
                
                # 添加关系
                for rel in record['relations']:
                    if rel['target']:
                        sample_relations.append({
                            "source": node['id'],
                            "target": f"target_{rel['target']}",
                            "type": rel['type']
                        })
            
            print(f"  获取了 {len(sample_nodes)} 个示例节点")
            print(f"  获取了 {len(sample_relations)} 个示例关系")
            
            # 6. 生成前端可视化数据
            visualization_data = {
                "stats": {
                    "totalNodes": session.run("MATCH (n:Dictionary) RETURN count(n) AS count").single()['count'],
                    "totalRelations": session.run("MATCH ()-[r]->() RETURN count(r) AS count").single()['count'],
                    "totalCategories": len(categories),
                    "totalTags": session.run("MATCH (n:Tag) RETURN count(n) AS count").single()['count']
                },
                "categories": categories,
                "tags": tags,
                "sampleNodes": sample_nodes[:10],  # 限制数量
                "sampleRelations": sample_relations[:20]
            }
            
            # 保存到文件
            with open('config/graph_visualization_data.json', 'w', encoding='utf-8') as f:
                json.dump(visualization_data, f, ensure_ascii=False, indent=2)
            
            print(f"\n✅ 可视化数据已保存到: config/graph_visualization_data.json")
            return visualization_data
            
    except Exception as e:
        print(f"❌ 分析失败: {e}")
        return None
    finally:
        driver.close()

if __name__ == "__main__":
    analyze_graph_structure()
