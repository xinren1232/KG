#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import time

def check_neo4j():
    """检查Neo4j服务"""
    print("🔍 检查Neo4j服务...")
    try:
        from neo4j import GraphDatabase
        driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'password123'))
        
        with driver.session() as session:
            result = session.run("RETURN 1 as test").single()
            if result and result['test'] == 1:
                print("✅ Neo4j服务正常")
                
                # 获取数据统计
                dict_count = session.run('MATCH (n:Dictionary) RETURN count(n) AS c').single()['c']
                rel_count = session.run('MATCH ()-[r]->() RETURN count(r) AS c').single()['c']
                
                print(f"   📊 Dictionary节点: {dict_count}")
                print(f"   📊 关系总数: {rel_count}")
                return True
            else:
                print("❌ Neo4j查询异常")
                return False
        
        driver.close()
        
    except Exception as e:
        print(f"❌ Neo4j连接失败: {e}")
        return False

def check_api():
    """检查API服务"""
    print("\n🔍 检查API服务...")
    
    # 检查健康状态
    try:
        response = requests.get('http://localhost:8000/health', timeout=5)
        if response.status_code == 200:
            print("✅ API服务正常")
            print(f"   📊 响应: {response.json()}")
            return True
        else:
            print(f"❌ API服务异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API服务连接失败: {e}")
        return False

def test_api_endpoints():
    """测试关键API端点"""
    print("\n🧪 测试API端点...")
    
    endpoints = [
        '/kg/real-stats',
        '/kg/graph-data',
        '/kg/dictionary'
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f'http://localhost:8000{endpoint}', timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {endpoint}: 正常")
                
                # 显示关键信息
                if endpoint == '/kg/real-stats' and data.get('data', {}).get('stats'):
                    stats = data['data']['stats']
                    print(f"   📊 节点: {stats.get('totalNodes')}, 关系: {stats.get('totalRelations')}")
                elif endpoint == '/kg/graph-data' and data.get('data', {}).get('sampleNodes'):
                    nodes = data['data']['sampleNodes']
                    print(f"   📊 示例节点: {len(nodes)}个")
                elif endpoint == '/kg/dictionary' and data.get('data'):
                    print(f"   📊 词典数据: 正常")
            else:
                print(f"❌ {endpoint}: {response.status_code}")
        except Exception as e:
            print(f"❌ {endpoint}: {e}")

def check_frontend():
    """检查前端服务"""
    print("\n🔍 检查前端服务...")
    try:
        response = requests.get('http://localhost:5173', timeout=5)
        if response.status_code == 200:
            print("✅ 前端服务正常")
            return True
        else:
            print(f"❌ 前端服务异常: {response.status_code}")
            return False
    except Exception as e:
        print("❌ 前端服务未启动")
        print("   启动命令: cd apps/web && npm run dev")
        return False

def main():
    """主检查函数"""
    print("🚀 检查所有后端服务状态")
    print("=" * 50)
    
    # 检查各个服务
    neo4j_ok = check_neo4j()
    api_ok = check_api()
    
    if api_ok:
        test_api_endpoints()
    
    frontend_ok = check_frontend()
    
    # 总结
    print("\n" + "=" * 50)
    print("📊 服务状态总结")
    print("=" * 50)
    
    print(f"Neo4j数据库: {'✅ 正常' if neo4j_ok else '❌ 异常'}")
    print(f"API服务:     {'✅ 正常' if api_ok else '❌ 异常'}")
    print(f"前端服务:    {'✅ 正常' if frontend_ok else '❌ 未启动'}")
    
    print("\n🌐 访问地址:")
    if api_ok:
        print("- API服务: http://localhost:8000")
        print("- API文档: http://localhost:8000/docs")
        print("- 图谱数据: http://localhost:8000/kg/graph-data")
        print("- 真实统计: http://localhost:8000/kg/real-stats")
    
    if frontend_ok:
        print("- 前端服务: http://localhost:5173")
        print("- 图谱可视化: http://localhost:5173/graph-viz")
    else:
        print("- 前端服务: 需要启动 (cd apps/web && npm run dev)")
    
    if neo4j_ok:
        print("- Neo4j浏览器: http://localhost:7474")
    
    print("\n💡 下一步:")
    if not frontend_ok:
        print("1. 启动前端: cd apps/web && npm run dev")
    print("2. 访问图谱: http://localhost:5173/graph-viz")
    print("3. 查看API: http://localhost:8000/docs")
    
    # 生成状态报告
    status_report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "services": {
            "neo4j": neo4j_ok,
            "api": api_ok,
            "frontend": frontend_ok
        },
        "urls": {
            "api": "http://localhost:8000" if api_ok else None,
            "frontend": "http://localhost:5173" if frontend_ok else None,
            "neo4j": "http://localhost:7474" if neo4j_ok else None
        }
    }
    
    with open('服务状态.json', 'w', encoding='utf-8') as f:
        json.dump(status_report, f, ensure_ascii=False, indent=2)
    
    print(f"\n📋 状态报告已保存: 服务状态.json")

if __name__ == "__main__":
    main()
