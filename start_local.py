#!/usr/bin/env python3
"""
本地开发环境启动脚本
"""

import os
import sys
import subprocess
import time
import requests
from pathlib import Path

def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 11):
        print("❌ Python版本需要3.11+，当前版本:", sys.version)
        return False
    print(f"✅ Python版本: {sys.version}")
    return True

def check_neo4j_connection():
    """检查Neo4j连接"""
    try:
        response = requests.get("http://localhost:7474", timeout=5)
        if response.status_code == 200:
            print("✅ Neo4j服务运行中 (http://localhost:7474)")
            return True
        else:
            print("❌ Neo4j服务响应异常")
            return False
    except requests.exceptions.RequestException:
        print("❌ Neo4j服务未启动或无法连接")
        print("   请启动Neo4j Desktop并确保数据库运行在localhost:7474")
        return False

def install_dependencies():
    """安装Python依赖"""
    print("📦 安装API依赖...")
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "services/api/requirements.txt"
        ], check=True, capture_output=True)
        print("✅ API依赖安装完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖安装失败: {e}")
        return False

def check_env_file():
    """检查环境变量文件"""
    if not os.path.exists(".env"):
        print("⚠️  .env文件不存在，使用默认配置")
        # 创建基本的.env文件
        with open(".env", "w") as f:
            f.write("""NEO4J_USER=neo4j
NEO4J_PASS=password123
NEO4J_URI=bolt://localhost:7687
LOG_LEVEL=INFO
""")
        print("✅ 已创建默认.env文件")
    else:
        print("✅ .env文件存在")
    return True

def start_api_server():
    """启动API服务器"""
    print("🚀 启动API服务器...")
    os.chdir("services/api")
    
    try:
        # 使用uvicorn启动服务
        subprocess.run([
            sys.executable, "-m", "uvicorn", "main:app", 
            "--reload", "--host", "0.0.0.0", "--port", "8000"
        ])
    except KeyboardInterrupt:
        print("\n🛑 API服务器已停止")
    except Exception as e:
        print(f"❌ API服务器启动失败: {e}")

def show_neo4j_setup_guide():
    """显示Neo4j设置指南"""
    print("\n" + "="*60)
    print("📋 Neo4j设置指南")
    print("="*60)
    print("1. 下载并安装Neo4j Desktop:")
    print("   https://neo4j.com/download/")
    print()
    print("2. 创建新数据库:")
    print("   - 打开Neo4j Desktop")
    print("   - 点击'New Project'")
    print("   - 点击'Add Database' -> 'Local DBMS'")
    print("   - 设置密码为: password123")
    print("   - 点击'Create'")
    print()
    print("3. 启动数据库:")
    print("   - 点击数据库旁边的'Start'按钮")
    print("   - 等待状态变为'Active'")
    print()
    print("4. 初始化数据:")
    print("   - 点击'Open with Neo4j Browser'")
    print("   - 复制并执行以下文件中的Cypher语句:")
    print("     * services/api/neo4j_init/neo4j_constraints.cypher")
    print("     * services/api/neo4j_init/sample_data.cypher")
    print()
    print("5. 重新运行此脚本")
    print("="*60)

def main():
    """主函数"""
    print("🚀 质量知识图谱助手 - 本地开发环境启动")
    print("="*60)
    
    # 检查Python版本
    if not check_python_version():
        return
    
    # 检查环境变量文件
    check_env_file()
    
    # 检查Neo4j连接
    if not check_neo4j_connection():
        show_neo4j_setup_guide()
        return
    
    # 安装依赖
    if not install_dependencies():
        return
    
    print("\n✅ 环境检查完成，启动API服务器...")
    print("📍 API文档: http://localhost:8000/docs")
    print("📍 健康检查: http://localhost:8000/health")
    print("📍 Neo4j控制台: http://localhost:7474")
    print("\n按 Ctrl+C 停止服务器\n")
    
    # 启动API服务器
    start_api_server()

if __name__ == "__main__":
    main()
