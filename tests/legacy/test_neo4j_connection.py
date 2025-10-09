#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试Neo4j连接和数据状态
"""

import requests
import base64
from neo4j import GraphDatabase

def test_http_api():
    """测试HTTP API连接"""
    print("🔍 测试Neo4j HTTP API连接...")
    
    # 尝试不同的认证
    auth_configs = [
        ('neo4j', 'password'),
        ('neo4j', 'neo4j'),
        ('neo4j', '123456'),
        ('neo4j', 'admin')
    ]
    
    for username, password in auth_configs:
        try:
            auth_string = base64.b64encode(f'{username}:{password}'.encode()).decode('ascii')
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Basic {auth_string}'
            }
            
            response = requests.post(
                'http://localhost:7474/db/neo4j/query/v2',
                headers=headers,
                json={'query': 'MATCH (n) RETURN count(n) as total'},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                total = data['data'][0]['total']
                print(f"✅ HTTP API连接成功 ({username}:{password})")
                print(f"当前节点总数: {total}")
                
                # 检查Label分布
                response2 = requests.post(
                    'http://localhost:7474/db/neo4j/query/v2',
                    headers=headers,
                    json={'query': 'MATCH (n) RETURN labels(n)[0] as label, count(n) as count ORDER BY count DESC'}
                )
                
                if response2.status_code == 200:
                    data2 = response2.json()
                    print("Label分布:")
                    for row in data2['data']:
                        label = row['label']
                        count = row['count']
                        print(f"  {label}: {count}个")
                
                return True, (username, password)
            else:
                print(f"❌ HTTP API失败 ({username}:{password}): {response.status_code}")
                
        except Exception as e:
            print(f"❌ HTTP API连接失败 ({username}:{password}): {e}")
    
    return False, None

def test_bolt_api():
    """测试Bolt API连接"""
    print("\n🔍 测试Neo4j Bolt API连接...")
    
    auth_configs = [
        ('neo4j', 'password'),
        ('neo4j', 'neo4j'),
        ('neo4j', '123456'),
        ('neo4j', 'admin')
    ]
    
    for username, password in auth_configs:
        try:
            driver = GraphDatabase.driver('bolt://localhost:7687', auth=(username, password))
            with driver.session() as session:
                result = session.run('RETURN 1 as test')
                result.single()
                print(f"✅ Bolt API连接成功 ({username}:{password})")
                
                # 检查数据
                result = session.run('MATCH (n) RETURN count(n) as total')
                total = result.single()['total']
                print(f"当前节点总数: {total}")
                
                # 检查Label分布
                result = session.run('MATCH (n) RETURN labels(n)[0] as label, count(n) as count ORDER BY count DESC')
                print("Label分布:")
                for record in result:
                    label = record['label']
                    count = record['count']
                    print(f"  {label}: {count}个")
                
            driver.close()
            return True, (username, password)
            
        except Exception as e:
            print(f"❌ Bolt API连接失败 ({username}:{password}): {e}")
    
    return False, None

def main():
    print("🚀 开始测试Neo4j连接...")
    
    # 测试HTTP API
    http_success, http_auth = test_http_api()
    
    # 测试Bolt API
    bolt_success, bolt_auth = test_bolt_api()
    
    print("\n📊 测试结果总结:")
    if http_success:
        print(f"✅ HTTP API可用: {http_auth[0]}:{http_auth[1]}")
    else:
        print("❌ HTTP API不可用")
    
    if bolt_success:
        print(f"✅ Bolt API可用: {bolt_auth[0]}:{bolt_auth[1]}")
    else:
        print("❌ Bolt API不可用")
    
    if not http_success and not bolt_success:
        print("\n⚠️  Neo4j服务可能未启动或认证配置有问题")
        print("请检查:")
        print("1. Neo4j服务是否正在运行")
        print("2. 端口7474(HTTP)和7687(Bolt)是否开放")
        print("3. 用户名密码是否正确")

if __name__ == "__main__":
    main()
