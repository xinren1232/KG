#!/usr/bin/env python3
"""
Neo4j数据库初始化脚本
"""
import os
import sys
from pathlib import Path

def load_cypher_file(file_path):
    """加载Cypher文件内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except Exception as e:
        print(f"❌ 读取文件失败 {file_path}: {e}")
        return None

def execute_cypher_statements(session, content, description):
    """执行Cypher语句"""
    print(f"📝 执行{description}...")
    
    # 分割语句（以分号和换行分割）
    statements = []
    current_statement = ""
    
    for line in content.split('\n'):
        line = line.strip()
        if line and not line.startswith('//'):  # 跳过注释
            current_statement += line + " "
            if line.endswith(';'):
                statements.append(current_statement.strip())
                current_statement = ""
    
    # 添加最后一个语句（如果没有分号结尾）
    if current_statement.strip():
        statements.append(current_statement.strip())
    
    success_count = 0
    for i, statement in enumerate(statements):
        if statement.strip():
            try:
                result = session.run(statement)
                result.consume()  # 确保语句执行完成
                success_count += 1
                print(f"   ✅ 语句 {i+1}/{len(statements)} 执行成功")
            except Exception as e:
                print(f"   ⚠️ 语句 {i+1}/{len(statements)} 执行失败: {e}")
    
    print(f"   📊 成功执行 {success_count}/{len(statements)} 条语句")
    return success_count

def init_neo4j_database():
    """初始化Neo4j数据库"""
    try:
        from neo4j import GraphDatabase
        
        # 从环境变量读取配置
        uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        user = os.getenv("NEO4J_USER", "neo4j")
        password = os.getenv("NEO4J_PASS", "password123")
        
        print(f"🔗 连接到Neo4j数据库...")
        print(f"   URI: {uri}")
        
        # 创建驱动
        driver = GraphDatabase.driver(uri, auth=(user, password))
        
        with driver.session() as session:
            # 1. 执行约束和索引
            constraints_file = Path("services/api/neo4j_init/neo4j_constraints.cypher")
            if constraints_file.exists():
                content = load_cypher_file(constraints_file)
                if content:
                    execute_cypher_statements(session, content, "数据库约束和索引")
            else:
                print(f"⚠️ 约束文件不存在: {constraints_file}")
            
            # 2. 检查是否已有数据
            result = session.run("MATCH (n) RETURN count(n) as count")
            existing_count = result.single()["count"]
            
            if existing_count > 0:
                print(f"📊 数据库中已有 {existing_count} 个节点")
                response = input("是否要清空现有数据并重新导入？(y/N): ")
                if response.lower() == 'y':
                    print("🗑️ 清空现有数据...")
                    session.run("MATCH (n) DETACH DELETE n")
                    print("   ✅ 数据清空完成")
                else:
                    print("   ⏭️ 跳过数据导入")
                    return True
            
            # 3. 执行示例数据
            sample_file = Path("services/api/neo4j_init/sample_data.cypher")
            if sample_file.exists():
                content = load_cypher_file(sample_file)
                if content:
                    execute_cypher_statements(session, content, "示例数据")
            else:
                print(f"⚠️ 示例数据文件不存在: {sample_file}")
            
            # 4. 验证数据
            print("🔍 验证数据导入...")
            
            # 检查各类节点数量
            node_types = ["Product", "Component", "Anomaly", "TestCase", "Symptom"]
            for node_type in node_types:
                result = session.run(f"MATCH (n:{node_type}) RETURN count(n) as count")
                count = result.single()["count"]
                print(f"   {node_type}: {count} 个节点")
            
            # 检查关系数量
            result = session.run("MATCH ()-[r]->() RETURN count(r) as count")
            rel_count = result.single()["count"]
            print(f"   关系: {rel_count} 条")
            
            print("✅ Neo4j数据库初始化完成！")
            return True
            
    except ImportError:
        print("❌ Neo4j驱动未安装，请运行: pip install neo4j")
        return False
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        return False
    finally:
        try:
            driver.close()
        except:
            pass

def main():
    """主函数"""
    print("🚀 Neo4j数据库初始化")
    print("=" * 50)
    
    # 检查环境变量
    env_file = Path(".env")
    if env_file.exists():
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ 加载环境配置")
    else:
        print("⚠️ 使用默认配置")
    
    # 执行初始化
    success = init_neo4j_database()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 数据库初始化成功！")
        print("\n📋 下一步操作:")
        print("   1. 访问 http://localhost:7474 查看数据")
        print("   2. 启动完整版API服务")
        print("   3. 测试知识图谱功能")
    else:
        print("❌ 数据库初始化失败")
        print("\n💡 请先运行: python check_neo4j.py")

if __name__ == "__main__":
    main()
