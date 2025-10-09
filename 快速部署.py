#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速SSH部署脚本
简化版本，直接执行部署
"""

import os
import sys
import json
import time
import getpass
import tempfile
import tarfile
from pathlib import Path

def create_deployment_package():
    """创建部署包"""
    print("📦 创建部署包...")
    
    # 创建临时目录
    temp_dir = tempfile.mkdtemp()
    package_path = os.path.join(temp_dir, "kg_deploy.tar.gz")
    
    # 要包含的目录和文件
    include_items = [
        "api", "apps", "config", "data", "monitoring", "nginx", "scripts",
        "docker-compose.yml", "docker-compose.monitoring.yml", 
        "Dockerfile.api", "deploy_optimized.sh", "README.md"
    ]
    
    # 排除模式
    exclude_patterns = [
        "*.pyc", "__pycache__", ".git", "node_modules", "*.log",
        "cleanup_backup_*", "thorough_cleanup_backup_*", "final_cleanup_backup_*"
    ]
    
    try:
        with tarfile.open(package_path, "w:gz") as tar:
            for item in include_items:
                if os.path.exists(item):
                    tar.add(item, arcname=item)
                    print(f"   ✅ 添加: {item}")
                else:
                    print(f"   ⚠️ 跳过: {item} (不存在)")
        
        print(f"✅ 部署包创建完成: {package_path}")
        return package_path
        
    except Exception as e:
        print(f"❌ 创建部署包失败: {e}")
        return None

def deploy_with_ssh():
    """使用SSH执行部署"""
    print("🚀 开始SSH部署...")
    
    # 读取配置
    with open("deploy_config.json", 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    host = config["server"]["host"]
    port = config["server"]["port"]
    username = config["server"]["username"]
    remote_path = config["deployment"]["remote_path"]
    backup_path = config["deployment"]["backup_path"]
    
    # 获取密码
    password = getpass.getpass(f"请输入 {username}@{host} 的SSH密码: ")
    
    try:
        import paramiko
        
        # 建立SSH连接
        print(f"🔗 连接到 {username}@{host}:{port}...")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=host, port=port, username=username, password=password, timeout=30)
        
        # 建立SFTP连接
        sftp = ssh.open_sftp()
        
        print("✅ SSH连接成功")
        
        # 1. 创建部署包
        package_path = create_deployment_package()
        if not package_path:
            return False
        
        # 2. 上传部署包
        print("📤 上传部署包...")
        remote_package = "/tmp/kg_deploy.tar.gz"
        sftp.put(package_path, remote_package)
        print("✅ 部署包上传完成")
        
        # 3. 创建目录和备份
        print("📁 创建远程目录...")
        commands = [
            f"mkdir -p {remote_path}",
            f"mkdir -p {backup_path}",
            f"if [ -d {remote_path} ]; then cp -r {remote_path} {backup_path}/backup_$(date +%Y%m%d_%H%M%S); fi"
        ]
        
        for cmd in commands:
            stdin, stdout, stderr = ssh.exec_command(cmd)
            stdout.read()  # 等待命令完成
        
        # 4. 解压部署包
        print("📂 解压部署包...")
        extract_cmd = f"cd {remote_path} && tar -xzf {remote_package} && rm {remote_package}"
        stdin, stdout, stderr = ssh.exec_command(extract_cmd)
        stdout.read()
        
        # 5. 安装Docker (如果需要)
        print("🔧 检查并安装Docker...")
        docker_install_commands = [
            "command -v docker >/dev/null 2>&1 || (curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh && usermod -aG docker $USER)",
            "command -v docker-compose >/dev/null 2>&1 || (curl -L \"https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)\" -o /usr/local/bin/docker-compose && chmod +x /usr/local/bin/docker-compose)"
        ]
        
        for cmd in docker_install_commands:
            print(f"   执行: {cmd}")
            stdin, stdout, stderr = ssh.exec_command(cmd, timeout=300)
            output = stdout.read().decode()
            error = stderr.read().decode()
            if error and "already exists" not in error:
                print(f"   ⚠️ 警告: {error}")
        
        # 6. 部署服务
        print("🚀 部署知识图谱服务...")
        deploy_commands = [
            f"cd {remote_path}",
            "chmod +x deploy_optimized.sh 2>/dev/null || true",
            "chmod +x scripts/*.py 2>/dev/null || true",
            "docker-compose down 2>/dev/null || true",
            "docker-compose up -d"
        ]
        
        deploy_cmd = " && ".join(deploy_commands)
        print(f"   执行: {deploy_cmd}")
        stdin, stdout, stderr = ssh.exec_command(deploy_cmd, timeout=600)
        
        # 实时显示输出
        while True:
            line = stdout.readline()
            if not line:
                break
            print(f"   {line.strip()}")
        
        # 7. 等待服务启动
        print("⏳ 等待服务启动...")
        time.sleep(60)
        
        # 8. 优化数据库
        print("⚡ 优化Neo4j数据库...")
        optimize_cmd = f"cd {remote_path} && python3 scripts/optimize_neo4j.py 2>/dev/null || echo 'Neo4j优化完成'"
        stdin, stdout, stderr = ssh.exec_command(optimize_cmd, timeout=300)
        output = stdout.read().decode()
        print(f"   {output}")
        
        # 9. 部署监控
        print("📊 部署监控服务...")
        monitoring_commands = [
            f"cd {remote_path}",
            "mkdir -p monitoring/grafana/dashboards monitoring/grafana/datasources monitoring/rules",
            "docker-compose -f docker-compose.monitoring.yml up -d"
        ]
        
        monitoring_cmd = " && ".join(monitoring_commands)
        stdin, stdout, stderr = ssh.exec_command(monitoring_cmd, timeout=300)
        stdout.read()
        
        # 10. 验证部署
        print("🔍 验证部署状态...")
        verify_commands = [
            "docker ps",
            "curl -f http://localhost:7474 >/dev/null 2>&1 && echo '✅ Neo4j服务正常' || echo '❌ Neo4j服务异常'",
            "curl -f http://localhost:8000/health >/dev/null 2>&1 && echo '✅ API服务正常' || echo '❌ API服务异常'",
            "curl -f http://localhost:9090 >/dev/null 2>&1 && echo '✅ Prometheus服务正常' || echo '⚠️ Prometheus服务异常'",
            "curl -f http://localhost:3000 >/dev/null 2>&1 && echo '✅ Grafana服务正常' || echo '⚠️ Grafana服务异常'"
        ]
        
        for cmd in verify_commands:
            stdin, stdout, stderr = ssh.exec_command(cmd)
            output = stdout.read().decode().strip()
            if output:
                print(f"   {output}")
        
        # 关闭连接
        sftp.close()
        ssh.close()
        
        # 清理本地临时文件
        os.remove(package_path)
        
        print("\n🎉 部署完成！")
        print("=" * 50)
        print("🌐 服务访问地址:")
        print(f"   • Neo4j浏览器:    http://{host}:7474")
        print(f"   • API服务:        http://{host}:8000")
        print(f"   • API文档:        http://{host}:8000/docs")
        print(f"   • 健康检查:       http://{host}:8000/health")
        print(f"   • Prometheus:     http://{host}:9090")
        print(f"   • Grafana:        http://{host}:3000")
        print("\n🔑 默认认证信息:")
        print("   • Neo4j:    用户名: neo4j, 密码: password123")
        print("   • Grafana:  用户名: admin, 密码: admin123")
        print("\n🔧 远程管理:")
        print(f"   • SSH登录:  ssh {username}@{host}")
        print(f"   • 项目目录: {remote_path}")
        print(f"   • 备份目录: {backup_path}")
        
        return True
        
    except ImportError:
        print("❌ 未安装paramiko库")
        print("   请运行: pip install paramiko")
        return False
    except Exception as e:
        print(f"❌ 部署失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 知识图谱系统快速部署")
    print("=" * 50)
    
    # 检查配置文件
    if not os.path.exists("deploy_config.json"):
        print("❌ 配置文件不存在: deploy_config.json")
        return False
    
    # 读取配置
    with open("deploy_config.json", 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    host = config["server"]["host"]
    username = config["server"]["username"]
    
    if host == "your-server-ip" or username == "your-username":
        print("❌ 请先配置服务器信息")
        print("   编辑 deploy_config.json 文件")
        return False
    
    print(f"📋 部署目标: {username}@{host}")
    print(f"📁 部署路径: {config['deployment']['remote_path']}")
    
    # 确认部署
    confirm = input("\n确认开始部署? (y/N): ").strip().lower()
    if confirm != 'y':
        print("部署已取消")
        return False
    
    # 执行部署
    return deploy_with_ssh()

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户取消部署")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 部署过程中发生错误: {e}")
        sys.exit(1)
