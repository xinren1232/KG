#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import requests
import time
import os
import sys
import psutil
from pathlib import Path
from neo4j import GraphDatabase

def check_process_by_port(port):
    """检查指定端口的进程"""
    try:
        for conn in psutil.net_connections():
            if conn.laddr.port == port and conn.status == 'LISTEN':
                try:
                    process = psutil.Process(conn.pid)
                    return {
                        'pid': conn.pid,
                        'name': process.name(),
                        'cmdline': ' '.join(process.cmdline()),
                        'status': process.status()
                    }
                except:
                    return {'pid': conn.pid, 'name': 'unknown', 'cmdline': 'unknown', 'status': 'unknown'}
        return None
    except Exception as e:
        print(f"检查端口 {port} 失败: {e}")
        return None

def kill_process_by_port(port):
    """杀死占用指定端口的进程"""
    try:
        for conn in psutil.net_connections():
            if conn.laddr.port == port and conn.status == 'LISTEN':
                try:
                    process = psutil.Process(conn.pid)
                    print(f"  终止进程: PID {conn.pid} - {process.name()}")
                    process.terminate()
                    time.sleep(2)
                    if process.is_running():
                        process.kill()
                    return True
                except Exception as e:
                    print(f"  终止进程失败: {e}")
                    return False
        return True
    except Exception as e:
        print(f"杀死端口 {port} 进程失败: {e}")
        return False

def check_neo4j_service():
    """检查Neo4j服务"""
    print("🔍 检查Neo4j服务...")
    
    # 检查端口7474 (HTTP) 和 7687 (Bolt)
    http_process = check_process_by_port(7474)
    bolt_process = check_process_by_port(7687)
    
    if http_process or bolt_process:
        print("✅ Neo4j进程运行中:")
        if http_process:
            print(f"  HTTP端口7474: PID {http_process['pid']} - {http_process['name']}")
        if bolt_process:
            print(f"  Bolt端口7687: PID {bolt_process['pid']} - {bolt_process['name']}")
    else:
        print("❌ Neo4j进程未运行")
        return False
    
    # 测试连接
    try:
        response = requests.get('http://localhost:7474', timeout=5)
        if response.status_code == 200:
            print("✅ Neo4j HTTP接口正常")
        else:
            print(f"⚠️ Neo4j HTTP接口异常: {response.status_code}")
    except Exception as e:
        print(f"❌ Neo4j HTTP连接失败: {e}")
        return False
    
    # 测试数据库连接
    try:
        driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'password123'))
        with driver.session() as session:
            result = session.run("RETURN 1 as test").single()
            if result and result['test'] == 1:
                print("✅ Neo4j数据库连接正常")
                
                # 获取数据统计
                node_count = session.run('MATCH (n) RETURN count(n) AS count').single()['count']
                rel_count = session.run('MATCH ()-[r]->() RETURN count(r) AS count').single()['count']
                print(f"  📊 数据统计: {node_count} 节点, {rel_count} 关系")
                
        driver.close()
        return True
    except Exception as e:
        print(f"❌ Neo4j数据库连接失败: {e}")
        return False

def check_api_service():
    """检查API服务"""
    print("\n🔍 检查API服务...")
    
    # 检查端口8000
    api_process = check_process_by_port(8000)
    
    if api_process:
        print(f"✅ API进程运行中: PID {api_process['pid']} - {api_process['name']}")
        print(f"  命令行: {api_process['cmdline'][:100]}...")
    else:
        print("❌ API进程未运行")
        return False
    
    # 测试API端点
    try:
        response = requests.get('http://localhost:8000/health', timeout=5)
        if response.status_code == 200:
            print("✅ API健康检查正常")
        else:
            print(f"⚠️ API健康检查异常: {response.status_code}")
    except Exception as e:
        print(f"❌ API连接失败: {e}")
        return False
    
    # 测试词典端点
    try:
        response = requests.get('http://localhost:8000/kg/dictionary', timeout=10)
        if response.status_code == 200:
            data = response.json()
            total = data.get('total', 0)
            print(f"✅ 词典端点正常: {total} 条数据")
        else:
            print(f"⚠️ 词典端点异常: {response.status_code}")
    except Exception as e:
        print(f"❌ 词典端点测试失败: {e}")
    
    return True

def check_frontend_service():
    """检查前端服务"""
    print("\n🔍 检查前端服务...")
    
    # 检查端口5173
    frontend_process = check_process_by_port(5173)
    
    if frontend_process:
        print(f"✅ 前端进程运行中: PID {frontend_process['pid']} - {frontend_process['name']}")
    else:
        print("❌ 前端进程未运行")
        return False
    
    # 测试前端访问
    try:
        response = requests.get('http://localhost:5173', timeout=5)
        if response.status_code == 200:
            print("✅ 前端服务正常")
        else:
            print(f"⚠️ 前端服务异常: {response.status_code}")
    except Exception as e:
        print(f"❌ 前端连接失败: {e}")
        return False
    
    return True

def restart_api_service():
    """重启API服务"""
    print("\n🔄 重启API服务...")
    
    # 1. 停止现有API服务
    print("  停止现有API服务...")
    if not kill_process_by_port(8000):
        print("  ⚠️ 停止API服务可能失败")
    
    time.sleep(3)
    
    # 2. 启动新的API服务
    print("  启动新的API服务...")
    try:
        # 切换到API目录并启动服务
        api_dir = Path("../api").resolve()
        
        # 使用uvicorn启动
        process = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"],
            cwd=api_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0
        )
        
        print(f"  ✅ API服务启动中... (PID: {process.pid})")
        
        # 等待服务启动
        for i in range(15):
            time.sleep(2)
            try:
                response = requests.get('http://localhost:8000/health', timeout=3)
                if response.status_code == 200:
                    print(f"  ✅ API服务启动成功")
                    return True
            except:
                continue
        
        print("  ⚠️ API服务启动超时，但进程已启动")
        return True
        
    except Exception as e:
        print(f"  ❌ API服务启动失败: {e}")
        return False

def restart_frontend_service():
    """重启前端服务"""
    print("\n🔄 重启前端服务...")
    
    # 1. 停止现有前端服务
    print("  停止现有前端服务...")
    if not kill_process_by_port(5173):
        print("  ⚠️ 停止前端服务可能失败")
    
    time.sleep(3)
    
    # 2. 启动新的前端服务
    print("  启动新的前端服务...")
    try:
        # 切换到前端目录并启动服务
        frontend_dir = Path("../apps/web").resolve()
        
        # 使用npm run dev启动
        process = subprocess.Popen(
            ["npm", "run", "dev"],
            cwd=frontend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0,
            shell=True
        )
        
        print(f"  ✅ 前端服务启动中... (PID: {process.pid})")
        
        # 等待服务启动
        for i in range(20):
            time.sleep(3)
            try:
                response = requests.get('http://localhost:5173', timeout=3)
                if response.status_code == 200:
                    print(f"  ✅ 前端服务启动成功")
                    return True
            except:
                continue
        
        print("  ⚠️ 前端服务启动超时，但进程已启动")
        return True
        
    except Exception as e:
        print(f"  ❌ 前端服务启动失败: {e}")
        return False

def final_service_check():
    """最终服务检查"""
    print("\n🔍 最终服务状态检查")
    print("=" * 50)
    
    services = [
        ("Neo4j数据库", "http://localhost:7474", 7474),
        ("API服务", "http://localhost:8000/health", 8000),
        ("前端服务", "http://localhost:5173", 5173)
    ]
    
    all_ok = True
    
    for name, url, port in services:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                process = check_process_by_port(port)
                pid = process['pid'] if process else 'unknown'
                print(f"✅ {name}: 正常运行 (PID: {pid})")
            else:
                print(f"⚠️ {name}: 响应异常 ({response.status_code})")
                all_ok = False
        except Exception as e:
            print(f"❌ {name}: 连接失败 - {e}")
            all_ok = False
    
    return all_ok

def main():
    """主函数"""
    print("🔧 检查并重启所有后端服务")
    print("=" * 60)
    
    # 1. 检查当前服务状态
    print("📊 当前服务状态检查")
    print("=" * 30)
    
    neo4j_ok = check_neo4j_service()
    api_ok = check_api_service()
    frontend_ok = check_frontend_service()
    
    # 2. 决定是否需要重启
    need_restart = False
    
    if not api_ok:
        print("\n⚠️ API服务需要重启")
        need_restart = True
    
    if not frontend_ok:
        print("\n⚠️ 前端服务需要重启")
        need_restart = True
    
    if not neo4j_ok:
        print("\n⚠️ Neo4j服务异常，请手动检查")
    
    # 3. 执行重启
    if need_restart:
        print("\n" + "=" * 60)
        print("🔄 开始重启服务")
        print("=" * 60)
        
        if not api_ok:
            restart_api_service()
        
        if not frontend_ok:
            restart_frontend_service()
        
        # 等待所有服务稳定
        print("\n⏳ 等待服务稳定...")
        time.sleep(10)
        
    else:
        print("\n✅ 所有服务运行正常，无需重启")
    
    # 4. 最终检查
    print("\n" + "=" * 60)
    final_ok = final_service_check()
    
    # 5. 总结
    print("\n" + "=" * 60)
    print("📊 服务重启总结")
    print("=" * 60)
    
    if final_ok:
        print("🎉 所有后端服务运行正常！")
        print("\n🌐 访问地址:")
        print("  - 前端应用: http://localhost:5173")
        print("  - API服务: http://localhost:8000")
        print("  - API文档: http://localhost:8000/docs")
        print("  - Neo4j浏览器: http://localhost:7474")
        print("  - 词典数据: http://localhost:8000/kg/dictionary")
    else:
        print("⚠️ 部分服务可能存在问题，请检查日志")
    
    print(f"\n💡 提示:")
    print(f"  - 如果Neo4j异常，请通过Neo4j Desktop重启")
    print(f"  - 服务启动可能需要几分钟时间")
    print(f"  - 可以通过浏览器访问上述地址验证服务状态")

if __name__ == "__main__":
    main()
