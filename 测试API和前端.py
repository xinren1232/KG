#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import subprocess
import time
import os

def test_api_endpoint():
    """测试API端点"""
    try:
        print("=== 测试API端点 ===")
        
        # 测试健康检查
        try:
            response = requests.get('http://localhost:8000/health', timeout=5)
            print(f"健康检查: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"健康检查失败: {e}")
        
        # 测试真实统计数据端点
        try:
            response = requests.get('http://localhost:8000/kg/real-stats', timeout=10)
            print(f"真实统计数据: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"数据预览: {json.dumps(data, indent=2, ensure_ascii=False)[:500]}...")
            else:
                print(f"响应内容: {response.text}")
        except Exception as e:
            print(f"真实统计数据测试失败: {e}")
            
    except Exception as e:
        print(f"API测试失败: {e}")

def start_services():
    """启动服务"""
    print("=== 启动服务 ===")
    
    # 启动API服务
    try:
        print("启动API服务...")
        api_process = subprocess.Popen(
            ['python', 'api/main.py'],
            cwd=os.getcwd(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print(f"API服务进程ID: {api_process.pid}")
        time.sleep(3)  # 等待服务启动
        
        # 检查API服务状态
        if api_process.poll() is None:
            print("✅ API服务启动成功")
        else:
            stdout, stderr = api_process.communicate()
            print(f"❌ API服务启动失败")
            print(f"stdout: {stdout.decode()}")
            print(f"stderr: {stderr.decode()}")
            
    except Exception as e:
        print(f"启动API服务失败: {e}")

def check_frontend_config():
    """检查前端配置"""
    print("=== 检查前端配置 ===")
    
    # 检查配置文件
    config_file = 'config/frontend_real_data.json'
    if os.path.exists(config_file):
        print(f"✅ 配置文件存在: {config_file}")
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"配置数据预览:")
                print(f"  - 总节点数: {data.get('stats', {}).get('totalNodes', 'N/A')}")
                print(f"  - 总关系数: {data.get('stats', {}).get('totalRelations', 'N/A')}")
                print(f"  - 分类数量: {len(data.get('categories', []))}")
        except Exception as e:
            print(f"❌ 读取配置文件失败: {e}")
    else:
        print(f"❌ 配置文件不存在: {config_file}")

def check_neo4j_status():
    """检查Neo4j状态"""
    print("=== 检查Neo4j状态 ===")
    
    try:
        from neo4j import GraphDatabase
        driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'password123'))
        
        with driver.session() as session:
            # 简单查询测试连接
            result = session.run("RETURN 1 as test").single()
            if result and result['test'] == 1:
                print("✅ Neo4j连接正常")
                
                # 获取基本统计
                dict_count = session.run('MATCH (n:Dictionary) RETURN count(n) AS c').single()['c']
                rel_count = session.run('MATCH ()-[r]->() RETURN count(r) AS c').single()['c']
                print(f"  - Dictionary节点: {dict_count}")
                print(f"  - 关系数量: {rel_count}")
            else:
                print("❌ Neo4j查询异常")
                
        driver.close()
        
    except Exception as e:
        print(f"❌ Neo4j连接失败: {e}")

def main():
    """主函数"""
    print("🚀 全面重启和检查知识图谱系统")
    print("=" * 50)
    
    # 1. 检查Neo4j状态
    check_neo4j_status()
    print()
    
    # 2. 检查前端配置
    check_frontend_config()
    print()
    
    # 3. 启动服务
    start_services()
    print()
    
    # 4. 测试API
    test_api_endpoint()
    print()
    
    print("=" * 50)
    print("🎯 系统检查完成")
    print()
    print("📋 下一步操作:")
    print("1. 如果API服务正常，访问: http://localhost:8000/docs")
    print("2. 启动前端服务: cd apps/web && npm run dev")
    print("3. 访问前端: http://localhost:5173")
    print("4. 检查Neo4j浏览器: http://localhost:7474")

if __name__ == "__main__":
    main()
