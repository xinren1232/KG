#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import psutil
import requests
import time
import os
from datetime import datetime

def check_port(port):
    """检查端口是否被占用"""
    for conn in psutil.net_connections():
        if conn.laddr.port == port:
            return True, conn.pid
    return False, None

def check_service_health():
    """检查所有服务的健康状态"""
    print("🔍 检查服务状态...")
    print("=" * 50)
    
    services = {
        "Neo4j (7687)": 7687,
        "Neo4j HTTP (7474)": 7474,
        "API服务 (8000)": 8000,
        "前端服务 (5173)": 5173
    }
    
    status = {}
    
    for service_name, port in services.items():
        running, pid = check_port(port)
        status[service_name] = {"running": running, "pid": pid, "port": port}
        
        if running:
            print(f"✅ {service_name}: 运行中 (PID: {pid})")
        else:
            print(f"❌ {service_name}: 未运行")
    
    return status

def test_api_connection():
    """测试API连接"""
    print("\n🔗 测试API连接...")
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ API服务响应正常")
            return True
        else:
            print(f"⚠️ API服务响应异常: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ API服务连接失败: {e}")
        return False

def test_frontend_connection():
    """测试前端连接"""
    print("🔗 测试前端连接...")
    try:
        response = requests.get("http://localhost:5173", timeout=5)
        if response.status_code == 200:
            print("✅ 前端服务响应正常")
            return True
        else:
            print(f"⚠️ 前端服务响应异常: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ 前端服务连接失败: {e}")
        return False

def start_api_service():
    """启动API服务"""
    print("\n🚀 启动API服务...")
    try:
        # 使用subprocess.Popen启动API服务
        process = subprocess.Popen(
            ["python", "api/main.py"],
            cwd=os.getcwd(),
            creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0
        )
        print(f"✅ API服务启动中... (PID: {process.pid})")
        
        # 等待服务启动
        for i in range(30):
            time.sleep(1)
            if check_port(8000)[0]:
                print("✅ API服务启动成功")
                return True
        
        print("⚠️ API服务启动超时")
        return False
        
    except Exception as e:
        print(f"❌ API服务启动失败: {e}")
        return False

def start_frontend_service():
    """启动前端服务"""
    print("\n🎨 启动前端服务...")
    try:
        frontend_dir = os.path.join(os.getcwd(), "apps", "web")
        vite_path = os.path.join(frontend_dir, "node_modules", "vite", "bin", "vite.js")
        
        if not os.path.exists(vite_path):
            print(f"❌ Vite不存在: {vite_path}")
            return False
        
        # 启动前端服务
        process = subprocess.Popen(
            ["node", vite_path],
            cwd=frontend_dir,
            creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0
        )
        print(f"✅ 前端服务启动中... (PID: {process.pid})")
        
        # 等待服务启动
        for i in range(60):
            time.sleep(1)
            if check_port(5173)[0]:
                print("✅ 前端服务启动成功")
                return True
            if i % 10 == 0 and i > 0:
                print(f"   等待中... ({i}/60秒)")
        
        print("⚠️ 前端服务启动超时")
        return False
        
    except Exception as e:
        print(f"❌ 前端服务启动失败: {e}")
        return False

def main():
    """主函数"""
    print("🔄 知识图谱系统服务管理")
    print(f"🕒 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 1. 检查当前服务状态
    status = check_service_health()
    
    # 2. 测试API连接
    if status["API服务 (8000)"]["running"]:
        test_api_connection()
    else:
        print("\n🚀 API服务未运行，尝试启动...")
        start_api_service()
    
    # 3. 测试前端连接
    if status["前端服务 (5173)"]["running"]:
        test_frontend_connection()
    else:
        print("\n🎨 前端服务未运行，尝试启动...")
        start_frontend_service()
    
    # 4. 最终状态检查
    print("\n" + "=" * 60)
    print("📊 最终服务状态:")
    final_status = check_service_health()
    
    print("\n🌐 访问地址:")
    if final_status["前端服务 (5173)"]["running"]:
        print("   - 前端界面: http://localhost:5173")
        print("   - 图谱可视化: http://localhost:5173/graph-viz")
    
    if final_status["API服务 (8000)"]["running"]:
        print("   - API服务: http://localhost:8000")
        print("   - API文档: http://localhost:8000/docs")
    
    if final_status["Neo4j (7687)"]["running"]:
        print("   - Neo4j浏览器: http://localhost:7474")
    else:
        print("   ⚠️ Neo4j未运行，请手动启动Neo4j Desktop")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断操作")
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
