#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import psutil
import time
import os
import json
from pathlib import Path

def check_port(port):
    """检查端口是否被占用"""
    for conn in psutil.net_connections():
        if conn.laddr.port == port:
            return True, conn.pid
    return False, None

def find_neo4j_desktop():
    """查找Neo4j Desktop安装路径"""
    possible_paths = [
        Path(os.environ.get('USERPROFILE', '')) / 'AppData' / 'Local' / 'Neo4j',
        Path(os.environ.get('USERPROFILE', '')) / 'AppData' / 'Local' / 'Programs' / 'Neo4j Desktop',
        Path('C:') / 'Program Files' / 'Neo4j Desktop',
        Path('C:') / 'Program Files (x86)' / 'Neo4j Desktop'
    ]
    
    for path in possible_paths:
        if path.exists():
            print(f"✅ 找到Neo4j Desktop: {path}")
            return path
    
    return None

def check_neo4j_desktop_running():
    """检查Neo4j Desktop是否运行"""
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if 'neo4j desktop' in proc.info['name'].lower():
                return True, proc.info['pid']
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False, None

def start_neo4j_with_docker_compose():
    """尝试使用docker-compose启动Neo4j"""
    print("🐳 尝试使用Docker Compose启动Neo4j...")
    
    if not Path("docker-compose.yml").exists():
        print("❌ docker-compose.yml 不存在")
        return False
    
    try:
        # 检查docker是否可用
        subprocess.run(['docker', '--version'], check=True, capture_output=True)
        
        # 启动Neo4j服务
        result = subprocess.run(
            ['docker-compose', 'up', '-d', 'neo4j'],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            print("✅ Neo4j Docker容器启动成功")
            return True
        else:
            print(f"❌ Docker启动失败: {result.stderr}")
            return False
            
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        print("❌ Docker不可用或启动失败")
        return False

def create_standalone_neo4j():
    """创建独立的Neo4j实例"""
    print("🔧 尝试创建独立Neo4j实例...")
    
    # 创建Neo4j数据目录
    neo4j_dir = Path("neo4j_standalone")
    neo4j_dir.mkdir(exist_ok=True)
    
    data_dir = neo4j_dir / "data"
    logs_dir = neo4j_dir / "logs"
    conf_dir = neo4j_dir / "conf"
    
    data_dir.mkdir(exist_ok=True)
    logs_dir.mkdir(exist_ok=True)
    conf_dir.mkdir(exist_ok=True)
    
    # 创建配置文件
    config_content = """
# Neo4j configuration
server.default_listen_address=0.0.0.0
server.bolt.listen_address=:7687
server.http.listen_address=:7474

# Authentication
dbms.security.auth_enabled=true

# Memory settings
server.memory.heap.initial_size=512m
server.memory.heap.max_size=1G
server.memory.pagecache.size=512m

# Logging
server.logs.user.stdout_enabled=true
"""
    
    config_file = conf_dir / "neo4j.conf"
    with open(config_file, 'w') as f:
        f.write(config_content)
    
    print(f"✅ 创建Neo4j配置: {config_file}")
    return neo4j_dir

def wait_for_neo4j_startup(timeout=60):
    """等待Neo4j启动"""
    print("⏳ 等待Neo4j启动...")
    
    for i in range(timeout):
        bolt_running, _ = check_port(7687)
        http_running, _ = check_port(7474)
        
        if bolt_running and http_running:
            print("✅ Neo4j启动成功！")
            print("   - Bolt端口 (7687): ✅")
            print("   - HTTP端口 (7474): ✅")
            return True
        
        if i % 10 == 0 and i > 0:
            print(f"   等待中... ({i}/{timeout}秒)")
        
        time.sleep(1)
    
    print("❌ Neo4j启动超时")
    return False

def main():
    """主函数"""
    print("🚀 启动Neo4j数据库服务")
    print("=" * 50)
    
    # 1. 检查当前状态
    bolt_running, bolt_pid = check_port(7687)
    http_running, http_pid = check_port(7474)
    
    if bolt_running and http_running:
        print("✅ Neo4j已经在运行")
        print(f"   - Bolt端口 (7687): PID {bolt_pid}")
        print(f"   - HTTP端口 (7474): PID {http_pid}")
        print("   - 浏览器访问: http://localhost:7474")
        return True
    
    # 2. 检查Neo4j Desktop
    desktop_running, desktop_pid = check_neo4j_desktop_running()
    if desktop_running:
        print(f"✅ Neo4j Desktop正在运行 (PID: {desktop_pid})")
        print("💡 请在Neo4j Desktop中手动启动数据库实例")
        print("   1. 打开Neo4j Desktop应用")
        print("   2. 选择或创建数据库实例")
        print("   3. 点击'Start'按钮")
        
        # 等待用户手动启动
        print("\n⏳ 等待数据库启动...")
        if wait_for_neo4j_startup(120):  # 等待2分钟
            return True
    
    # 3. 尝试Docker方式
    print("\n🐳 尝试Docker方式启动...")
    if start_neo4j_with_docker_compose():
        if wait_for_neo4j_startup():
            return True
    
    # 4. 提供手动启动指导
    print("\n" + "=" * 50)
    print("❌ 自动启动失败，请手动启动Neo4j")
    print("\n📋 手动启动方法:")
    print("1. Neo4j Desktop:")
    print("   - 打开Neo4j Desktop应用")
    print("   - 创建或选择数据库实例")
    print("   - 点击'Start'按钮")
    print("\n2. 命令行 (如果已安装):")
    print("   neo4j console")
    print("\n3. Windows服务 (如果已安装):")
    print("   net start neo4j")
    print("\n4. Docker (如果已安装):")
    print("   docker-compose up -d neo4j")
    
    print("\n🔗 启动后访问:")
    print("   - Neo4j浏览器: http://localhost:7474")
    print("   - 默认用户名: neo4j")
    print("   - 默认密码: password123")
    
    return False

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n🎉 Neo4j启动成功！")
            print("现在可以使用完整的知识图谱系统了")
        else:
            print("\n⚠️ 需要手动启动Neo4j")
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断操作")
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
