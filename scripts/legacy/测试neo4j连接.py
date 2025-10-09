#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试Neo4j连接
"""

print("🔧 测试Neo4j连接...")

# 1. 检查neo4j驱动
try:
    import neo4j
    print("✅ Neo4j驱动已安装")
except ImportError:
    print("📦 安装Neo4j驱动...")
    import subprocess
    import sys
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "neo4j"])
        print("✅ Neo4j驱动安装成功")
        import neo4j
    except Exception as e:
        print(f"❌ Neo4j驱动安装失败: {e}")
        exit(1)

# 2. 测试连接
from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
auth_configs = [
    ("neo4j", "password"),
    ("neo4j", "neo4j"),
    ("neo4j", "123456"),
    ("neo4j", "admin"),
]

driver = None
for username, password in auth_configs:
    try:
        print(f"🔍 尝试连接: {username}/{password}")
        driver = GraphDatabase.driver(uri, auth=(username, password))
        
        with driver.session() as session:
            result = session.run("RETURN 1 as test")
            test_value = result.single()["test"]
            if test_value == 1:
                print(f"✅ Neo4j连接成功! (用户: {username})")
                
                # 检查当前Dictionary节点数
                result = session.run("MATCH (n:Dictionary) RETURN count(n) as count")
                current_count = result.single()["count"]
                print(f"📊 当前Dictionary节点: {current_count} 个")
                
                break
                
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        continue

if driver:
    driver.close()
    print("🎯 Neo4j连接测试完成")
else:
    print("❌ 无法连接Neo4j")
