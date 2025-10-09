#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
执行终极词典补充数据导入到Neo4j
"""

import requests
import json
import time
from datetime import datetime

def test_neo4j_connection():
    """测试Neo4j连接"""
    print("🔗 测试Neo4j连接...")
    
    # 尝试HTTP API连接
    try:
        response = requests.get(
            "http://localhost:7474/db/data/",
            auth=("neo4j", "password"),
            timeout=5
        )
        if response.status_code == 200:
            print("✅ Neo4j HTTP API连接成功")
            return True
        else:
            print(f"❌ Neo4j HTTP API连接失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Neo4j连接异常: {e}")
        return False

def execute_cypher_query(query, description=""):
    """执行Cypher查询"""
    url = "http://localhost:7474/db/data/transaction/commit"
    headers = {"Content-Type": "application/json"}
    auth = ("neo4j", "password")
    
    payload = {
        "statements": [
            {
                "statement": query,
                "resultDataContents": ["row"]
            }
        ]
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, auth=auth, timeout=30)
        if response.status_code == 200:
            result = response.json()
            if result.get("errors"):
                print(f"❌ {description} 执行失败: {result['errors']}")
                return False
            else:
                print(f"✅ {description} 执行成功")
                return True
        else:
            print(f"❌ {description} HTTP错误: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ {description} 异常: {e}")
        return False

def get_current_node_count():
    """获取当前节点数量"""
    print("📊 获取当前数据库节点数量...")
    
    query = "MATCH (n) RETURN count(n) as total"
    url = "http://localhost:7474/db/data/transaction/commit"
    headers = {"Content-Type": "application/json"}
    auth = ("neo4j", "password")
    
    payload = {
        "statements": [
            {
                "statement": query,
                "resultDataContents": ["row"]
            }
        ]
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, auth=auth, timeout=10)
        if response.status_code == 200:
            result = response.json()
            if result.get("results") and result["results"][0].get("data"):
                count = result["results"][0]["data"][0]["row"][0]
                print(f"📊 当前节点总数: {count}")
                return count
            else:
                print("❌ 无法获取节点数量")
                return 0
        else:
            print(f"❌ 查询节点数量失败: {response.status_code}")
            return 0
    except Exception as e:
        print(f"❌ 查询异常: {e}")
        return 0

def get_label_distribution():
    """获取Label分布"""
    print("📊 获取Label分布...")
    
    query = """
    CALL db.labels() YIELD label
    CALL apoc.cypher.run('MATCH (n:' + label + ') RETURN count(n) as count', {}) YIELD value
    RETURN label, value.count as count
    ORDER BY value.count DESC
    """
    
    # 简化版查询（不依赖APOC）
    simple_query = """
    MATCH (n)
    RETURN labels(n)[0] as label, count(n) as count
    ORDER BY count DESC
    """
    
    url = "http://localhost:7474/db/data/transaction/commit"
    headers = {"Content-Type": "application/json"}
    auth = ("neo4j", "password")
    
    payload = {
        "statements": [
            {
                "statement": simple_query,
                "resultDataContents": ["row"]
            }
        ]
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, auth=auth, timeout=10)
        if response.status_code == 200:
            result = response.json()
            if result.get("results") and result["results"][0].get("data"):
                print("📋 当前Label分布:")
                for row in result["results"][0]["data"]:
                    label = row["row"][0]
                    count = row["row"][1]
                    if label:  # 过滤空标签
                        print(f"  {label}: {count}条")
                return True
            else:
                print("❌ 无法获取Label分布")
                return False
        else:
            print(f"❌ 查询Label分布失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 查询异常: {e}")
        return False

def execute_cypher_file(file_path):
    """执行Cypher文件"""
    print(f"📄 执行Cypher文件: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 分割成单独的语句
        statements = []
        for line in content.split('\n'):
            line = line.strip()
            if line and not line.startswith('//') and line.endswith(');'):
                statements.append(line)
        
        print(f"📊 找到 {len(statements)} 条CREATE语句")
        
        # 批量执行
        batch_size = 50
        success_count = 0
        
        for i in range(0, len(statements), batch_size):
            batch = statements[i:i+batch_size]
            batch_query = '\n'.join(batch)
            
            print(f"🔄 执行批次 {i//batch_size + 1}/{(len(statements)-1)//batch_size + 1} ({len(batch)}条语句)...")
            
            if execute_cypher_query(batch_query, f"批次{i//batch_size + 1}"):
                success_count += len(batch)
            else:
                print(f"❌ 批次{i//batch_size + 1}执行失败")
                break
            
            time.sleep(0.5)  # 避免过快请求
        
        print(f"✅ 成功执行 {success_count}/{len(statements)} 条语句")
        return success_count == len(statements)
        
    except Exception as e:
        print(f"❌ 执行Cypher文件失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 执行终极词典补充数据导入")
    print("=" * 60)
    
    # 1. 测试连接
    if not test_neo4j_connection():
        print("❌ Neo4j连接失败，请检查服务状态")
        return
    
    # 2. 获取导入前状态
    print("\n📊 导入前数据库状态:")
    before_count = get_current_node_count()
    get_label_distribution()
    
    # 3. 执行数据导入
    print(f"\n🔄 开始执行数据导入...")
    cypher_file = "终极完整词典补充数据导入脚本_20模块版.cypher"
    
    start_time = time.time()
    success = execute_cypher_file(cypher_file)
    end_time = time.time()
    
    if success:
        print(f"\n✅ 数据导入完成! 耗时: {end_time - start_time:.2f}秒")
        
        # 4. 获取导入后状态
        print("\n📊 导入后数据库状态:")
        after_count = get_current_node_count()
        get_label_distribution()
        
        # 5. 统计结果
        added_count = after_count - before_count
        print(f"\n📈 导入统计:")
        print(f"导入前节点数: {before_count}")
        print(f"导入后节点数: {after_count}")
        print(f"新增节点数: {added_count}")
        
        if added_count > 0:
            print(f"\n🎉 成功导入 {added_count} 条新数据!")
            print(f"📊 数据增长: +{(added_count/before_count)*100:.1f}%")
        else:
            print(f"\n⚠️ 未检测到新增数据，可能存在重复或其他问题")
        
    else:
        print(f"\n❌ 数据导入失败!")
    
    print(f"\n💡 下一步:")
    print(f"1. 重启前端服务以刷新缓存")
    print(f"2. 验证前端词典页面显示")
    print(f"3. 测试新增硬件模块数据查询")
    print(f"4. 检查图谱可视化效果")

if __name__ == "__main__":
    main()
