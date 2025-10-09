#!/usr/bin/env python3
"""
检查Neo4j数据库中的节点和关系数据
"""

from neo4j import GraphDatabase
import json

def check_neo4j_data():
    """检查Neo4j数据"""
    driver = None
    try:
        # 连接Neo4j
        driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'password123'))
        
        with driver.session() as session:
            print("🔍 检查Neo4j数据库状态")
            print("=" * 50)
            
            # 检查节点统计
            print("\n📊 节点统计:")
            node_result = session.run("""
                MATCH (n) 
                RETURN labels(n)[0] as label, count(n) as count 
                ORDER BY count DESC
            """)
            
            total_nodes = 0
            for record in node_result:
                label = record["label"] or "Unknown"
                count = record["count"]
                total_nodes += count
                print(f"  {label}: {count}个")
            
            print(f"\n总节点数: {total_nodes}")
            
            # 检查关系统计
            print("\n🔗 关系统计:")
            rel_result = session.run("""
                MATCH ()-[r]->() 
                RETURN type(r) as relationship_type, count(r) as count 
                ORDER BY count DESC
            """)
            
            total_relations = 0
            relations_found = False
            for record in rel_result:
                relations_found = True
                rel_type = record["relationship_type"]
                count = record["count"]
                total_relations += count
                print(f"  {rel_type}: {count}个")
            
            if not relations_found:
                print("  ❌ 没有找到任何关系数据")
            
            print(f"\n总关系数: {total_relations}")
            
            # 检查具体的节点示例
            print("\n📋 节点示例 (前5个):")
            sample_result = session.run("""
                MATCH (n) 
                RETURN id(n) as id, labels(n)[0] as label, 
                       coalesce(n.name, n.title, n.id, 'Node_' + toString(id(n))) as name,
                       properties(n) as properties
                LIMIT 5
            """)
            
            for record in sample_result:
                node_id = record["id"]
                label = record["label"] or "Unknown"
                name = record["name"]
                print(f"  ID: {node_id}, Label: {label}, Name: {name}")
            
            # 检查关系示例
            print("\n🔗 关系示例 (前5个):")
            rel_sample_result = session.run("""
                MATCH (n)-[r]->(m) 
                RETURN id(n) as source_id, type(r) as rel_type, id(m) as target_id,
                       coalesce(n.name, 'Node_' + toString(id(n))) as source_name,
                       coalesce(m.name, 'Node_' + toString(id(m))) as target_name
                LIMIT 5
            """)
            
            relations_sample_found = False
            for record in rel_sample_result:
                relations_sample_found = True
                source_name = record["source_name"]
                rel_type = record["rel_type"]
                target_name = record["target_name"]
                print(f"  {source_name} --[{rel_type}]--> {target_name}")
            
            if not relations_sample_found:
                print("  ❌ 没有找到关系示例")
            
            # 分析问题
            print("\n🎯 问题分析:")
            if total_nodes > 0 and total_relations == 0:
                print("  ⚠️  发现问题: 有节点数据但没有关系数据")
                print("  💡 建议: 需要导入关系数据或重新构建图谱")
            elif total_nodes == 0:
                print("  ❌ 发现问题: 没有任何数据")
                print("  💡 建议: 需要重新导入数据")
            else:
                print("  ✅ 数据完整: 节点和关系都存在")
            
            # 检查数据导入脚本
            print("\n📁 检查数据导入脚本:")
            import os
            import glob
            
            # 查找导入脚本
            import_scripts = []
            for pattern in ["**/import*.py", "**/load*.py", "**/build*.py"]:
                import_scripts.extend(glob.glob(pattern, recursive=True))
            
            if import_scripts:
                print("  找到的导入脚本:")
                for script in import_scripts[:5]:  # 只显示前5个
                    print(f"    {script}")
            else:
                print("  ❌ 没有找到导入脚本")
            
            # 检查数据文件
            print("\n📄 检查数据文件:")
            data_files = []
            for pattern in ["**/data/**/*.csv", "**/data/**/*.json"]:
                data_files.extend(glob.glob(pattern, recursive=True))
            
            if data_files:
                print("  找到的数据文件:")
                for data_file in data_files[:10]:  # 只显示前10个
                    size = os.path.getsize(data_file)
                    print(f"    {data_file} ({size:,} bytes)")
            else:
                print("  ❌ 没有找到数据文件")
                
    except Exception as e:
        print(f"❌ 连接Neo4j失败: {e}")
        print("💡 请确保Neo4j服务正在运行")
        
    finally:
        if driver:
            driver.close()

if __name__ == "__main__":
    check_neo4j_data()
