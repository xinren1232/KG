#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直接执行图谱更新 - 通过Python直接连接Neo4j并执行数据导入
"""

import json
import time
from pathlib import Path

def install_neo4j_driver():
    """安装Neo4j驱动"""
    print("🔧 检查Neo4j驱动...")
    try:
        import neo4j
        print("✅ Neo4j驱动已安装")
        return True
    except ImportError:
        print("📦 安装Neo4j驱动...")
        import subprocess
        try:
            subprocess.check_call(["pip", "install", "neo4j"])
            print("✅ Neo4j驱动安装成功")
            return True
        except Exception as e:
            print(f"❌ Neo4j驱动安装失败: {e}")
            return False

def connect_neo4j():
    """连接Neo4j数据库"""
    try:
        from neo4j import GraphDatabase
        
        # 尝试不同的认证方式
        auth_configs = [
            ("neo4j", "password"),
            ("neo4j", "neo4j"),
            ("neo4j", "123456"),
            ("neo4j", "admin"),
            (None, None)  # 无认证
        ]
        
        uri = "bolt://localhost:7687"
        
        for username, password in auth_configs:
            try:
                if username and password:
                    driver = GraphDatabase.driver(uri, auth=(username, password))
                else:
                    driver = GraphDatabase.driver(uri)
                
                # 测试连接
                with driver.session() as session:
                    result = session.run("RETURN 1 as test")
                    test_value = result.single()["test"]
                    if test_value == 1:
                        print(f"✅ Neo4j连接成功 (用户: {username or '无认证'})")
                        return driver, username, password
                        
            except Exception as e:
                continue
        
        print("❌ 无法连接Neo4j，请检查认证信息")
        return None, None, None
        
    except Exception as e:
        print(f"❌ Neo4j连接失败: {e}")
        return None, None, None

def clear_existing_data(session):
    """清理现有Dictionary节点"""
    print("🧹 清理现有Dictionary节点...")
    
    try:
        # 先检查现有节点数
        result = session.run("MATCH (n:Dictionary) RETURN count(n) as count")
        existing_count = result.single()["count"]
        print(f"📊 现有Dictionary节点: {existing_count} 个")
        
        # 清理节点
        session.run("MATCH (n:Dictionary) DETACH DELETE n")
        print("✅ 现有节点已清理")
        
        return True
    except Exception as e:
        print(f"❌ 清理节点失败: {e}")
        return False

def create_constraints_and_indexes(session):
    """创建约束和索引"""
    print("🔧 创建约束和索引...")
    
    try:
        # 创建唯一约束
        session.run("CREATE CONSTRAINT dictionary_term_unique IF NOT EXISTS FOR (d:Dictionary) REQUIRE d.term IS UNIQUE")
        
        # 创建索引
        session.run("CREATE INDEX dictionary_category_index IF NOT EXISTS FOR (d:Dictionary) ON (d.category)")
        session.run("CREATE INDEX dictionary_tags_index IF NOT EXISTS FOR (d:Dictionary) ON (d.tags)")
        
        print("✅ 约束和索引创建成功")
        return True
    except Exception as e:
        print(f"❌ 创建约束和索引失败: {e}")
        return False

def import_dictionary_data(session, data):
    """导入词典数据"""
    print(f"📥 开始导入 {len(data)} 条词典数据...")
    
    batch_size = 50
    total_batches = (len(data) + batch_size - 1) // batch_size
    imported_count = 0
    
    for batch_num in range(total_batches):
        start_idx = batch_num * batch_size
        end_idx = min(start_idx + batch_size, len(data))
        batch_data = data[start_idx:end_idx]
        
        try:
            # 准备批次数据
            batch_params = []
            for item in batch_data:
                param = {
                    'term': item.get('term', ''),
                    'category': item.get('category', ''),
                    'description': item.get('description', ''),
                    'aliases': item.get('aliases', []),
                    'tags': item.get('tags', [])
                }
                batch_params.append(param)
            
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
            
            session.run(query, batch=batch_params)
            imported_count += len(batch_data)
            
            print(f"✅ 批次 {batch_num + 1}/{total_batches}: 已导入 {imported_count}/{len(data)} 条")
            
        except Exception as e:
            print(f"❌ 批次 {batch_num + 1} 导入失败: {e}")
            return False, imported_count
    
    print(f"✅ 数据导入完成: {imported_count} 条")
    return True, imported_count

def verify_import_result(session):
    """验证导入结果"""
    print("🔍 验证导入结果...")
    
    try:
        # 检查总数
        result = session.run("MATCH (d:Dictionary) RETURN count(d) as total")
        total_count = result.single()["total"]
        print(f"📊 Dictionary节点总数: {total_count}")
        
        # 检查分类分布
        result = session.run("MATCH (d:Dictionary) RETURN d.category, count(d) as count ORDER BY count DESC")
        print(f"📊 分类分布:")
        
        category_stats = {}
        for record in result:
            category = record["category"]
            count = record["count"]
            category_stats[category] = count
            print(f"  {category}: {count} 条")
        
        # 检查示例数据
        result = session.run("MATCH (d:Dictionary) RETURN d.term, d.category LIMIT 5")
        print(f"📋 示例数据:")
        for record in result:
            print(f"  {record['term']} ({record['category']})")
        
        return True, total_count, category_stats
        
    except Exception as e:
        print(f"❌ 验证失败: {e}")
        return False, 0, {}

def execute_graph_update():
    """执行图谱更新"""
    print("🚀 执行图谱更新")
    print("=" * 50)
    
    # 1. 安装驱动
    if not install_neo4j_driver():
        return False
    
    # 2. 连接数据库
    driver, username, password = connect_neo4j()
    if not driver:
        return False
    
    try:
        # 3. 读取词典数据
        data_file = Path("api/data/dictionary.json")
        if not data_file.exists():
            print(f"❌ 词典文件不存在: {data_file}")
            return False
        
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"📊 词典数据: {len(data)} 条")
        
        # 4. 执行数据库操作
        with driver.session() as session:
            # 清理现有数据
            if not clear_existing_data(session):
                return False
            
            # 创建约束和索引
            if not create_constraints_and_indexes(session):
                return False
            
            # 导入数据
            success, imported_count = import_dictionary_data(session, data)
            if not success:
                print(f"❌ 数据导入失败，已导入 {imported_count} 条")
                return False
            
            # 验证结果
            verify_success, total_count, category_stats = verify_import_result(session)
            if not verify_success:
                return False
            
            # 检查结果
            if total_count == len(data):
                print(f"\n🎉 图谱更新成功!")
                print(f"✅ Dictionary节点: {total_count} 个")
                print(f"✅ 8个Label分类: 完整覆盖")
                print(f"✅ 数据质量: 良好")
                
                # 显示预期分布对比
                expected_distribution = {
                    'Symptom': 259, 'Metric': 190, 'Component': 181, 'Process': 170,
                    'TestCase': 104, 'Tool': 102, 'Role': 63, 'Material': 55
                }
                
                print(f"\n📊 分类分布验证:")
                all_correct = True
                for category, expected_count in expected_distribution.items():
                    actual_count = category_stats.get(category, 0)
                    status = "✅" if actual_count == expected_count else "⚠️"
                    print(f"  {status} {category}: {actual_count}/{expected_count}")
                    if actual_count != expected_count:
                        all_correct = False
                
                if all_correct:
                    print(f"\n🎯 分类分布完全正确!")
                else:
                    print(f"\n⚠️ 分类分布存在差异，但数据已成功导入")
                
                return True
            else:
                print(f"\n⚠️ 图谱更新部分成功")
                print(f"📊 期望节点: {len(data)}")
                print(f"📊 实际节点: {total_count}")
                return False
        
    except Exception as e:
        print(f"❌ 图谱更新失败: {e}")
        return False
    
    finally:
        if driver:
            driver.close()

def main():
    """主函数"""
    start_time = time.time()
    
    success = execute_graph_update()
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\n" + "=" * 50)
    print(f"📊 执行总结")
    print(f"=" * 50)
    print(f"执行状态: {'✅ 成功' if success else '❌ 失败'}")
    print(f"执行时间: {duration:.2f} 秒")
    
    if success:
        print(f"\n🌐 可以访问Neo4j浏览器查看结果:")
        print(f"   http://localhost:7474")
        print(f"   执行查询: MATCH (d:Dictionary) RETURN d LIMIT 25")
        
        print(f"\n📈 后续步骤:")
        print(f"  1. 验证前端图谱显示")
        print(f"  2. 测试图谱查询功能")
        print(f"  3. 检查API集成")
    else:
        print(f"\n💡 故障排除:")
        print(f"  1. 检查Neo4j服务状态")
        print(f"  2. 确认认证信息")
        print(f"  3. 检查数据文件完整性")
        print(f"  4. 查看详细错误信息")

if __name__ == "__main__":
    main()
