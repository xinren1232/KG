#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import requests
import json
import time
import os
import sys
from pathlib import Path

def check_neo4j_status():
    """检查Neo4j服务状态"""
    print("🔍 检查Neo4j服务状态...")
    try:
        from neo4j import GraphDatabase
        driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'password123'))
        
        with driver.session() as session:
            # 测试连接
            result = session.run("RETURN 1 as test").single()
            if result and result['test'] == 1:
                print("✅ Neo4j服务运行正常")
                
                # 获取数据统计
                dict_count = session.run('MATCH (n:Dictionary) RETURN count(n) AS c').single()['c']
                rel_count = session.run('MATCH ()-[r]->() RETURN count(r) AS c').single()['c']
                tag_count = session.run('MATCH (n:Tag) RETURN count(n) AS c').single()['c']
                cat_count = session.run('MATCH (n:Category) RETURN count(n) AS c').single()['c']
                
                print(f"   📊 数据统计:")
                print(f"   - Dictionary节点: {dict_count}")
                print(f"   - 关系总数: {rel_count}")
                print(f"   - Tag节点: {tag_count}")
                print(f"   - Category节点: {cat_count}")
                
                return True
            else:
                print("❌ Neo4j连接异常")
                return False
                
        driver.close()
        
    except Exception as e:
        print(f"❌ Neo4j连接失败: {e}")
        print("   请确保Neo4j服务已启动并运行在端口7687")
        return False

def start_api_service():
    """启动API服务"""
    print("\n🚀 启动API服务...")
    
    # 检查API是否已经运行
    try:
        response = requests.get('http://localhost:8000/health', timeout=3)
        if response.status_code == 200:
            print("✅ API服务已在运行")
            return True
    except:
        pass
    
    # 启动API服务
    try:
        print("   正在启动API服务...")
        api_process = subprocess.Popen(
            [sys.executable, 'api/main.py'],
            cwd=os.getcwd(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0
        )
        
        # 等待服务启动
        for i in range(10):
            time.sleep(2)
            try:
                response = requests.get('http://localhost:8000/health', timeout=3)
                if response.status_code == 200:
                    print(f"✅ API服务启动成功 (PID: {api_process.pid})")
                    return True
            except:
                continue
        
        print("❌ API服务启动超时")
        return False
        
    except Exception as e:
        print(f"❌ API服务启动失败: {e}")
        return False

def test_api_endpoints():
    """测试API端点"""
    print("\n🧪 测试API端点...")
    
    endpoints = [
        ('/health', '健康检查'),
        ('/kg/real-stats', '真实统计数据'),
        ('/kg/graph-data', '图谱可视化数据'),
        ('/kg/dictionary', '词典数据'),
        ('/docs', 'API文档')
    ]
    
    results = {}
    
    for endpoint, name in endpoints:
        try:
            response = requests.get(f'http://localhost:8000{endpoint}', timeout=10)
            if response.status_code == 200:
                print(f"✅ {name}: {response.status_code}")
                results[endpoint] = 'success'
                
                # 显示部分数据
                if endpoint in ['/kg/real-stats', '/kg/graph-data']:
                    try:
                        data = response.json()
                        if data.get('success') and data.get('data'):
                            if 'stats' in data['data']:
                                stats = data['data']['stats']
                                print(f"   📊 数据: 节点{stats.get('totalNodes', 'N/A')}, 关系{stats.get('totalRelations', 'N/A')}")
                    except:
                        pass
            else:
                print(f"❌ {name}: {response.status_code}")
                results[endpoint] = 'failed'
                
        except Exception as e:
            print(f"❌ {name}: 连接失败 - {e}")
            results[endpoint] = 'error'
    
    return results

def check_data_files():
    """检查数据文件"""
    print("\n📁 检查数据文件...")
    
    files_to_check = [
        'api/data/dictionary.json',
        'config/frontend_real_data.json',
        'config/graph_visualization_data.json'
    ]
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                if file_path == 'api/data/dictionary.json':
                    print(f"✅ {file_path}: {len(data)} 条词典数据")
                elif 'stats' in data:
                    stats = data['stats']
                    print(f"✅ {file_path}: 节点{stats.get('totalNodes', 'N/A')}, 关系{stats.get('totalRelations', 'N/A')}")
                else:
                    print(f"✅ {file_path}: 文件正常")
                    
            except Exception as e:
                print(f"❌ {file_path}: 读取失败 - {e}")
        else:
            print(f"❌ {file_path}: 文件不存在")

def generate_service_report():
    """生成服务状态报告"""
    print("\n📋 生成服务状态报告...")
    
    # 收集系统信息
    report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "services": {
            "neo4j": check_neo4j_status(),
            "api": False,
            "frontend": False
        },
        "endpoints": {},
        "data_files": {},
        "system_info": {
            "python_version": sys.version,
            "working_directory": os.getcwd(),
            "platform": os.name
        }
    }
    
    # 检查API服务
    try:
        response = requests.get('http://localhost:8000/health', timeout=3)
        report["services"]["api"] = response.status_code == 200
    except:
        report["services"]["api"] = False
    
    # 检查前端服务
    try:
        response = requests.get('http://localhost:5173', timeout=3)
        report["services"]["frontend"] = response.status_code == 200
    except:
        report["services"]["frontend"] = False
    
    # 测试API端点
    if report["services"]["api"]:
        report["endpoints"] = test_api_endpoints()
    
    # 保存报告
    with open('服务状态报告.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print("✅ 服务状态报告已保存: 服务状态报告.json")
    return report

def main():
    """主函数"""
    print("🚀 启动并检查所有后端服务")
    print("=" * 60)
    
    # 1. 检查Neo4j
    neo4j_ok = check_neo4j_status()
    
    # 2. 启动API服务
    api_ok = start_api_service()
    
    # 3. 测试API端点
    if api_ok:
        test_results = test_api_endpoints()
    
    # 4. 检查数据文件
    check_data_files()
    
    # 5. 生成报告
    report = generate_service_report()
    
    # 6. 显示总结
    print("\n" + "=" * 60)
    print("📊 服务状态总结")
    print("=" * 60)
    
    services_status = report["services"]
    print(f"Neo4j数据库: {'✅ 正常' if services_status['neo4j'] else '❌ 异常'}")
    print(f"API服务:     {'✅ 正常' if services_status['api'] else '❌ 异常'}")
    print(f"前端服务:    {'✅ 正常' if services_status['frontend'] else '❌ 未启动'}")
    
    print("\n🌐 访问地址:")
    if services_status['api']:
        print("- API服务: http://localhost:8000")
        print("- API文档: http://localhost:8000/docs")
        print("- 图谱数据: http://localhost:8000/kg/graph-data")
    
    if services_status['frontend']:
        print("- 前端服务: http://localhost:5173")
        print("- 图谱可视化: http://localhost:5173/graph-viz")
    else:
        print("- 前端服务: 需要手动启动 (cd apps/web && npm run dev)")
    
    if services_status['neo4j']:
        print("- Neo4j浏览器: http://localhost:7474")
    
    print("\n💡 下一步操作:")
    if not services_status['frontend']:
        print("1. 启动前端服务: cd apps/web && npm run dev")
    print("2. 访问图谱可视化: http://localhost:5173/graph-viz")
    print("3. 查看API文档: http://localhost:8000/docs")
    
    if not neo4j_ok:
        print("⚠️ 注意: Neo4j服务未运行，某些功能可能受限")

if __name__ == "__main__":
    main()
