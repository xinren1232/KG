#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import time
import subprocess
import sys

def check_service_status(url, service_name, timeout=5):
    """检查服务状态"""
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            print(f"✅ {service_name}: 运行正常 (状态码: {response.status_code})")
            return True
        else:
            print(f"❌ {service_name}: 状态异常 (状态码: {response.status_code})")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ {service_name}: 连接失败 - 服务可能未启动")
        return False
    except requests.exceptions.Timeout:
        print(f"❌ {service_name}: 连接超时")
        return False
    except Exception as e:
        print(f"❌ {service_name}: 检查失败 - {e}")
        return False

def check_neo4j_connection():
    """检查Neo4j连接"""
    try:
        from neo4j import GraphDatabase
        driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'password123'))
        
        with driver.session() as session:
            result = session.run("RETURN 1 as test").single()
            if result and result['test'] == 1:
                print("✅ Neo4j数据库: 连接正常")
                
                # 获取数据统计
                dict_count = session.run('MATCH (n:Dictionary) RETURN count(n) AS c').single()['c']
                rel_count = session.run('MATCH ()-[r]->() RETURN count(r) AS c').single()['c']
                
                print(f"   📊 数据统计: Dictionary节点 {dict_count}, 关系 {rel_count}")
                return True
            else:
                print("❌ Neo4j数据库: 查询异常")
                return False
                
        driver.close()
        
    except Exception as e:
        print(f"❌ Neo4j数据库: 连接失败 - {e}")
        return False

def main():
    """主函数"""
    print("🔍 检查所有服务状态")
    print("=" * 50)
    
    services = [
        ('http://localhost:7474', 'Neo4j浏览器'),
        ('http://localhost:8000/health', 'API服务'),
        ('http://localhost:8000/docs', 'API文档'),
        ('http://localhost:5173', '前端服务'),
    ]
    
    results = {}
    
    # 检查HTTP服务
    for url, name in services:
        results[name] = check_service_status(url, name)
    
    # 检查Neo4j数据库连接
    results['Neo4j数据库'] = check_neo4j_connection()
    
    print("\n" + "=" * 50)
    print("📊 服务状态总结")
    print("=" * 50)
    
    all_ok = True
    for service, status in results.items():
        status_text = "✅ 正常" if status else "❌ 异常"
        print(f"{service}: {status_text}")
        if not status:
            all_ok = False
    
    print("\n🌐 访问地址:")
    if results.get('前端服务'):
        print("- 前端应用: http://localhost:5173")
    if results.get('API服务'):
        print("- API服务: http://localhost:8000")
        print("- API文档: http://localhost:8000/docs")
    if results.get('Neo4j浏览器'):
        print("- Neo4j浏览器: http://localhost:7474")
    
    if all_ok:
        print("\n🎉 所有服务运行正常！")
    else:
        print("\n⚠️ 部分服务存在问题，请检查启动状态")
        
        # 提供启动建议
        print("\n💡 启动建议:")
        if not results.get('Neo4j浏览器') or not results.get('Neo4j数据库'):
            print("1. 启动Neo4j: 通过Neo4j Desktop或命令行启动")
        if not results.get('API服务'):
            print("2. 启动API服务: python api/main.py")
        if not results.get('前端服务'):
            print("3. 启动前端服务: cd apps/web && npm run dev")

if __name__ == "__main__":
    main()
