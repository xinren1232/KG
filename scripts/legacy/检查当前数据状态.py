#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from neo4j import GraphDatabase
import json

def check_neo4j_data():
    """检查当前Neo4j数据状态"""
    driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'password123'))
    
    try:
        with driver.session() as session:
            print("=== 当前Neo4j数据状态 ===")
            
            # 检查节点数量
            dictionary_count = session.run('MATCH (n:Dictionary) RETURN count(n) AS c').single()['c']
            tag_count = session.run('MATCH (n:Tag) RETURN count(n) AS c').single()['c']
            category_count = session.run('MATCH (n:Category) RETURN count(n) AS c').single()['c']
            alias_count = session.run('MATCH (n:Alias) RETURN count(n) AS c').single()['c']
            total_relations = session.run('MATCH ()-[r]->() RETURN count(r) AS c').single()['c']
            
            print(f"Dictionary节点: {dictionary_count}")
            print(f"Tag节点: {tag_count}")
            print(f"Category节点: {category_count}")
            print(f"Alias节点: {alias_count}")
            print(f"总关系数: {total_relations}")
            
            print("\n=== 关系类型分布 ===")
            relations = session.run('MATCH ()-[r]->() RETURN type(r) AS rel, count(r) AS cnt ORDER BY cnt DESC')
            for record in relations:
                print(f"{record['rel']}: {record['cnt']}")
            
            print("\n=== 分类分布 ===")
            categories = session.run('MATCH (d:Dictionary) RETURN d.category AS cat, count(d) AS cnt ORDER BY cnt DESC')
            for record in categories:
                print(f"{record['cat']}: {record['cnt']}")
            
            # 生成前端需要的数据
            frontend_data = {
                "stats": {
                    "totalNodes": dictionary_count,
                    "totalRelations": total_relations,
                    "totalCategories": category_count,
                    "totalTags": tag_count,
                    "totalAliases": alias_count
                },
                "categories": [],
                "relations": []
            }
            
            # 获取分类数据
            for record in categories:
                frontend_data["categories"].append({
                    "name": record['cat'],
                    "count": record['cnt']
                })
            
            # 获取关系数据
            for record in session.run('MATCH ()-[r]->() RETURN type(r) AS rel, count(r) AS cnt ORDER BY cnt DESC'):
                frontend_data["relations"].append({
                    "type": record['rel'],
                    "count": record['cnt']
                })
            
            # 保存到文件
            with open('config/frontend_real_data.json', 'w', encoding='utf-8') as f:
                json.dump(frontend_data, f, ensure_ascii=False, indent=2)
            
            print(f"\n前端数据已保存到: config/frontend_real_data.json")
            return frontend_data
            
    except Exception as e:
        print(f"错误: {e}")
        return None
    finally:
        driver.close()

if __name__ == "__main__":
    check_neo4j_data()
