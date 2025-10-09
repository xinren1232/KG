#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全面重启知识图谱系统所有服务
包括Neo4j数据库、API服务、前端服务的完整重启流程
"""

import os
import sys
import time
import json
import subprocess
import psutil
import requests
from pathlib import Path
from datetime import datetime

def print_header(title):
    """打印标题"""
    print(f"\n{'='*60}")
    print(f"🔄 {title}")
    print(f"{'='*60}")

def print_step(step):
    """打印步骤"""
    print(f"\n📋 {step}")
    print("-" * 40)

def check_port(port):
    """检查端口是否被占用"""
    for conn in psutil.net_connections():
        if conn.laddr.port == port:
            return True, conn.pid
    return False, None

def kill_process_by_port(port):
    """根据端口杀死进程"""
    try:
        for conn in psutil.net_connections():
            if conn.laddr.port == port and conn.pid:
                process = psutil.Process(conn.pid)
                print(f"  🔪 终止进程: {process.name()} (PID: {conn.pid})")
                process.terminate()
                time.sleep(2)
                if process.is_running():
                    process.kill()
                return True
    except Exception as e:
        print(f"  ❌ 终止进程失败: {e}")
    return False

def kill_processes_by_name(process_names):
    """根据进程名杀死进程"""
    killed = []
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            proc_info = proc.info
            if any(name.lower() in proc_info['name'].lower() for name in process_names):
                # 检查是否是我们的服务进程
                cmdline = ' '.join(proc_info['cmdline'] or [])
                if any(keyword in cmdline.lower() for keyword in ['main.py', 'npm run dev', 'vite', 'fastapi']):
                    print(f"  🔪 终止进程: {proc_info['name']} (PID: {proc_info['pid']})")
                    proc.terminate()
                    killed.append(proc_info['pid'])
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    # 等待进程终止
    if killed:
        time.sleep(3)
        for pid in killed:
            try:
                proc = psutil.Process(pid)
                if proc.is_running():
                    proc.kill()
            except psutil.NoSuchProcess:
                pass
    
    return len(killed)

def check_neo4j_status():
    """检查Neo4j服务状态"""
    print_step("检查Neo4j数据库状态")
    
    # 检查端口7687 (Bolt)
    bolt_running, bolt_pid = check_port(7687)
    # 检查端口7474 (HTTP)
    http_running, http_pid = check_port(7474)
    
    if bolt_running and http_running:
        print("  ✅ Neo4j服务正在运行")
        print(f"     - Bolt端口 (7687): PID {bolt_pid}")
        print(f"     - HTTP端口 (7474): PID {http_pid}")
        return True
    else:
        print("  ❌ Neo4j服务未运行")
        print("     请手动启动Neo4j Desktop或服务")
        return False

def stop_all_services():
    """停止所有现有服务"""
    print_step("停止所有现有服务")
    
    # 停止特定端口的服务
    ports_to_check = [8000, 5173]
    for port in ports_to_check:
        running, pid = check_port(port)
        if running:
            print(f"  🔍 发现端口 {port} 被占用 (PID: {pid})")
            kill_process_by_port(port)
        else:
            print(f"  ✅ 端口 {port} 空闲")
    
    # 停止相关进程
    print("  🔍 查找相关进程...")
    killed = kill_processes_by_name(['python', 'node'])
    if killed > 0:
        print(f"  ✅ 已终止 {killed} 个进程")
    else:
        print("  ✅ 没有发现需要终止的进程")

def check_dependencies():
    """检查依赖环境"""
    print_step("检查依赖环境")
    
    # 检查Python
    try:
        python_version = subprocess.check_output([sys.executable, '--version'], 
                                               text=True).strip()
        print(f"  ✅ Python: {python_version}")
    except Exception as e:
        print(f"  ❌ Python检查失败: {e}")
        return False
    
    # 检查Node.js
    try:
        node_version = subprocess.check_output(['node', '--version'], 
                                             text=True).strip()
        print(f"  ✅ Node.js: {node_version}")
    except Exception as e:
        print(f"  ❌ Node.js检查失败: {e}")
        return False
    
    # 检查API依赖
    api_requirements = Path("api/requirements.txt")
    if api_requirements.exists():
        print("  ✅ API requirements.txt 存在")
    else:
        print("  ❌ API requirements.txt 不存在")
        return False
    
    # 检查前端依赖
    frontend_package = Path("apps/web/package.json")
    if frontend_package.exists():
        print("  ✅ 前端 package.json 存在")
        
        node_modules = Path("apps/web/node_modules")
        if node_modules.exists():
            print("  ✅ 前端依赖已安装")
        else:
            print("  🔄 安装前端依赖...")
            try:
                subprocess.run(['npm', 'install'], 
                             cwd='apps/web', 
                             check=True, 
                             capture_output=True)
                print("  ✅ 前端依赖安装完成")
            except subprocess.CalledProcessError as e:
                print(f"  ❌ 前端依赖安装失败: {e}")
                return False
    else:
        print("  ❌ 前端 package.json 不存在")
        return False
    
    return True

def start_api_service():
    """启动API服务"""
    print_step("启动API服务")
    
    try:
        # 启动API服务
        api_process = subprocess.Popen(
            [sys.executable, 'api/main.py'],
            cwd=os.getcwd(),
            creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0
        )
        print(f"  🚀 API服务启动中... (PID: {api_process.pid})")
        print("     - 地址: http://localhost:8000")
        print("     - 文档: http://localhost:8000/docs")
        
        # 等待服务启动
        print("  ⏳ 等待API服务启动...")
        for i in range(30):  # 最多等待30秒
            time.sleep(1)
            try:
                response = requests.get("http://localhost:8000/health", timeout=2)
                if response.status_code == 200:
                    print("  ✅ API服务启动成功")
                    return True
            except requests.exceptions.RequestException:
                continue
            
            if i % 5 == 0:
                print(f"     等待中... ({i+1}/30秒)")
        
        print("  ⚠️ API服务启动超时，但进程已创建")
        return True
        
    except Exception as e:
        print(f"  ❌ API服务启动失败: {e}")
        return False

def start_frontend_service():
    """启动前端服务"""
    print_step("启动前端服务")
    
    try:
        # 启动前端服务
        frontend_process = subprocess.Popen(
            ['npm', 'run', 'dev'],
            cwd='apps/web',
            creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0
        )
        print(f"  🚀 前端服务启动中... (PID: {frontend_process.pid})")
        print("     - 地址: http://localhost:5173")
        print("     - 图谱: http://localhost:5173/graph-viz")
        
        # 等待服务启动
        print("  ⏳ 等待前端服务启动...")
        for i in range(60):  # 最多等待60秒
            time.sleep(1)
            running, _ = check_port(5173)
            if running:
                print("  ✅ 前端服务启动成功")
                return True
            
            if i % 10 == 0 and i > 0:
                print(f"     编译中... ({i+1}/60秒)")
        
        print("  ⚠️ 前端服务启动超时，但进程已创建")
        return True
        
    except Exception as e:
        print(f"  ❌ 前端服务启动失败: {e}")
        return False

def verify_services():
    """验证所有服务状态"""
    print_step("验证服务状态")
    
    services_status = {}
    
    # 检查Neo4j
    neo4j_running, _ = check_port(7687)
    services_status['neo4j'] = neo4j_running
    print(f"  Neo4j数据库 (7687): {'✅ 运行中' if neo4j_running else '❌ 未运行'}")
    
    # 检查API
    api_running, _ = check_port(8000)
    services_status['api'] = api_running
    print(f"  API服务 (8000): {'✅ 运行中' if api_running else '❌ 未运行'}")
    
    # 检查前端
    frontend_running, _ = check_port(5173)
    services_status['frontend'] = frontend_running
    print(f"  前端服务 (5173): {'✅ 运行中' if frontend_running else '❌ 未运行'}")
    
    return services_status

def main():
    """主函数"""
    print_header("全面重启知识图谱系统所有服务")
    print(f"🕒 启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 1. 停止所有现有服务
    stop_all_services()
    
    # 2. 检查Neo4j状态
    neo4j_ok = check_neo4j_status()
    if not neo4j_ok:
        print("\n⚠️ 警告: Neo4j未运行，某些功能可能受限")
        print("   请启动Neo4j Desktop或通过命令行启动Neo4j服务")
    
    # 3. 检查依赖环境
    if not check_dependencies():
        print("\n❌ 依赖检查失败，无法继续")
        return False
    
    # 4. 启动API服务
    if not start_api_service():
        print("\n❌ API服务启动失败")
        return False
    
    # 5. 启动前端服务
    if not start_frontend_service():
        print("\n❌ 前端服务启动失败")
        return False
    
    # 6. 验证服务状态
    services_status = verify_services()
    
    # 7. 显示总结
    print_header("服务重启完成")
    
    print("📊 服务状态:")
    for service, status in services_status.items():
        status_text = "✅ 正常" if status else "❌ 异常"
        service_name = {"neo4j": "Neo4j数据库", "api": "API服务", "frontend": "前端服务"}[service]
        print(f"   {service_name}: {status_text}")
    
    print("\n🌐 访问地址:")
    if services_status['frontend']:
        print("   - 前端界面: http://localhost:5173")
        print("   - 图谱可视化: http://localhost:5173/graph-viz")
        print("   - 系统管理: http://localhost:5173/system")
    
    if services_status['api']:
        print("   - API服务: http://localhost:8000")
        print("   - API文档: http://localhost:8000/docs")
    
    if services_status['neo4j']:
        print("   - Neo4j浏览器: http://localhost:7474")
    
    print("\n💡 使用提示:")
    print("   - 前端服务需要1-2分钟完成编译")
    print("   - 如果页面显示异常，请等待编译完成后刷新")
    print("   - 服务窗口会显示详细的运行日志")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n🎉 所有服务重启完成！")
        else:
            print("\n❌ 服务重启过程中出现错误")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断操作")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 发生未预期的错误: {e}")
        sys.exit(1)
