#!/usr/bin/env python3
"""
同步dictionary.json到Neo4j图谱
"""
import json
import sys
from neo4j import GraphDatabase

# Neo4j连接配置
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "password123"

class Neo4jSync:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def close(self):
        self.driver.close()
    
    def clear_graph(self):
        """清空图谱（可选）"""
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
            print("✅ 图谱已清空")
    
    def create_term_node(self, tx, entry):
        """创建术语节点"""
        query = """
        MERGE (t:Term {name: $term})
        SET t.category = $category,
            t.description = $description,
            t.aliases = $aliases,
            t.source = $source
        RETURN t
        """
        result = tx.run(query, 
                       term=entry['term'],
                       category=entry['category'],
                       description=entry['description'],
                       aliases=entry['aliases'],
                       source=entry.get('source', 'unknown'))
        return result.single()
    
    def create_tag_nodes(self, tx, tags):
        """创建标签节点"""
        for tag in tags:
            query = """
            MERGE (t:Tag {name: $tag})
            RETURN t
            """
            tx.run(query, tag=tag)
    
    def create_category_node(self, tx, category):
        """创建分类节点"""
        query = """
        MERGE (c:Category {name: $category})
        RETURN c
        """
        tx.run(query, category=category)
    
    def create_relationships(self, tx, term, tags, category):
        """创建关系"""
        # Term -> Tag
        for tag in tags:
            query = """
            MATCH (t:Term {name: $term})
            MATCH (tag:Tag {name: $tag})
            MERGE (t)-[:HAS_TAG]->(tag)
            """
            tx.run(query, term=term, tag=tag)
        
        # Term -> Category
        query = """
        MATCH (t:Term {name: $term})
        MATCH (c:Category {name: $category})
        MERGE (t)-[:BELONGS_TO]->(c)
        """
        tx.run(query, term=term, category=category)
    
    def sync_dictionary(self, dictionary_file, clear_first=False):
        """同步词典到Neo4j"""
        print("=" * 80)
        print("🔄 开始同步词典到Neo4j图谱")
        print("=" * 80)
        
        # 加载词典
        print("\n1️⃣ 加载词典数据...")
        with open(dictionary_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"   词典条目: {len(data)}条")
        
        # 可选：清空图谱
        if clear_first:
            print("\n2️⃣ 清空现有图谱...")
            self.clear_graph()
        else:
            print("\n2️⃣ 保留现有图谱，增量同步...")
        
        # 同步数据
        print("\n3️⃣ 同步数据到Neo4j...")
        
        with self.driver.session() as session:
            for i, entry in enumerate(data, 1):
                if i % 100 == 0:
                    print(f"   进度: {i}/{len(data)} ({i/len(data)*100:.1f}%)")
                
                # 创建术语节点
                session.execute_write(self.create_term_node, entry)
                
                # 创建标签节点
                tags = entry.get('tags', [])
                session.execute_write(self.create_tag_nodes, tags)
                
                # 创建分类节点
                category = entry.get('category', 'Unknown')
                session.execute_write(self.create_category_node, category)
                
                # 创建关系
                session.execute_write(self.create_relationships, 
                                     entry['term'], tags, category)
        
        print(f"   ✅ 同步完成: {len(data)}条")
        
        # 统计
        print("\n4️⃣ 图谱统计:")
        with self.driver.session() as session:
            # 节点统计
            result = session.run("MATCH (n:Term) RETURN count(n) as count")
            term_count = result.single()['count']
            print(f"   Term节点: {term_count}个")
            
            result = session.run("MATCH (n:Tag) RETURN count(n) as count")
            tag_count = result.single()['count']
            print(f"   Tag节点: {tag_count}个")
            
            result = session.run("MATCH (n:Category) RETURN count(n) as count")
            category_count = result.single()['count']
            print(f"   Category节点: {category_count}个")
            
            # 关系统计
            result = session.run("MATCH ()-[r:HAS_TAG]->() RETURN count(r) as count")
            has_tag_count = result.single()['count']
            print(f"   HAS_TAG关系: {has_tag_count}条")
            
            result = session.run("MATCH ()-[r:BELONGS_TO]->() RETURN count(r) as count")
            belongs_to_count = result.single()['count']
            print(f"   BELONGS_TO关系: {belongs_to_count}条")
        
        print("\n" + "=" * 80)
        print("✅ 同步完成！")
        print("=" * 80)

def main():
    # 检查参数
    if len(sys.argv) > 1 and sys.argv[1] == '--clear':
        clear_first = True
        print("⚠️ 将清空现有图谱后重新导入")
    else:
        clear_first = False
        print("ℹ️ 增量同步模式（保留现有图谱）")
    
    # 使用配置的密码
    password = NEO4J_PASSWORD
    
    # 同步
    try:
        sync = Neo4jSync(NEO4J_URI, NEO4J_USER, password)
        sync.sync_dictionary('api/data/dictionary.json', clear_first=clear_first)
        sync.close()
    except Exception as e:
        print(f"\n❌ 同步失败: {e}")
        print("\n可能的原因:")
        print("  1. Neo4j服务未启动")
        print("  2. 密码错误")
        print("  3. 连接配置错误")
        sys.exit(1)

if __name__ == "__main__":
    main()
