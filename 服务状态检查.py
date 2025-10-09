#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的服务状态检查工具
"""

import subprocess
import requests
import time

def check_port(port):
    """检查端口是否被占用"""
    try:
        result = subprocess.run(['netstat', '-an'], capture_output=True, text=True, shell=True)
        return f":{port}" in result.stdout
    except:
        return False

def check_services():
    """检查所有服务状态"""
    print("🔍 检查知识图谱系统服务状态")
    print("=" * 50)
    
    services = {
        "Neo4j Bolt (7687)": 7687,
        "Neo4j HTTP (7474)": 7474,
        "API服务 (8000)": 8000,
        "前端服务 (5173)": 5173
    }
    
    for service, port in services.items():
        if check_port(port):
            print(f"✅ {service}: 运行中")
        else:
            print(f"❌ {service}: 未运行")
    
    # 测试API连接
    print(f"\n🔗 测试API连接...")
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print(f"✅ API服务响应正常")
        else:
            print(f"❌ API服务响应异常: {response.status_code}")
    except:
        print(f"❌ API服务连接失败")
    
    # 测试前端连接
    print(f"\n🔗 测试前端连接...")
    try:
        response = requests.get("http://localhost:5173", timeout=5)
        if response.status_code == 200:
            print(f"✅ 前端服务响应正常")
        else:
            print(f"❌ 前端服务响应异常: {response.status_code}")
    except:
        print(f"❌ 前端服务连接失败")
    
    print(f"\n🌐 访问地址:")
    print(f"   - 前端界面: http://localhost:5173")
    print(f"   - API服务: http://localhost:8000")
    print(f"   - API文档: http://localhost:8000/docs")
    print(f"   - Neo4j浏览器: http://localhost:7474")

if __name__ == "__main__":
    check_services()
