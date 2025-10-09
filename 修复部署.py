#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复部署问题
检查并修复服务器上的Docker和服务问题
"""

import getpass
import time

def fix_deployment():
    """修复部署问题"""
    print("🔧 修复部署问题")
    print("=" * 50)
    
    host = "47.108.152.16"
    username = "root"
    
    # 获取密码
    password = getpass.getpass(f"请输入 {username}@{host} 的SSH密码: ")
    
    try:
        import paramiko
        
        # 建立SSH连接
        print(f"🔗 连接到 {username}@{host}...")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=host, port=22, username=username, password=password, timeout=30)
        
        print("✅ SSH连接成功")
        
        # 1. 检查系统信息
        print("\n📋 检查系统信息...")
        system_commands = [
            "uname -a",
            "cat /etc/os-release",
            "df -h",
            "free -h"
        ]
        
        for cmd in system_commands:
            print(f"\n🔍 执行: {cmd}")
            stdin, stdout, stderr = ssh.exec_command(cmd)
            output = stdout.read().decode().strip()
            if output:
                print(output)
        
        # 2. 手动安装Docker
        print("\n🐳 手动安装Docker...")
        
        # 更新包管理器
        print("📦 更新包管理器...")
        update_commands = [
            "apt-get update",
            "apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release"
        ]
        
        for cmd in update_commands:
            print(f"   执行: {cmd}")
            stdin, stdout, stderr = ssh.exec_command(cmd, timeout=300)
            stdout.read()  # 等待完成
        
        # 安装Docker的替代方法
        print("🔧 使用snap安装Docker...")
        snap_commands = [
            "snap install docker",
            "systemctl start snap.docker.dockerd",
            "systemctl enable snap.docker.dockerd"
        ]
        
        for cmd in snap_commands:
            print(f"   执行: {cmd}")
            stdin, stdout, stderr = ssh.exec_command(cmd, timeout=300)
            output = stdout.read().decode()
            error = stderr.read().decode()
            if output:
                print(f"   输出: {output}")
            if error and "already installed" not in error:
                print(f"   错误: {error}")
        
        # 3. 检查Docker状态
        print("\n🔍 检查Docker状态...")
        docker_check_commands = [
            "docker --version",
            "docker info",
            "systemctl status snap.docker.dockerd"
        ]
        
        for cmd in docker_check_commands:
            print(f"\n执行: {cmd}")
            stdin, stdout, stderr = ssh.exec_command(cmd)
            output = stdout.read().decode().strip()
            error = stderr.read().decode().strip()
            if output:
                print(f"输出: {output}")
            if error:
                print(f"错误: {error}")
        
        # 4. 安装Docker Compose
        print("\n📦 安装Docker Compose...")
        compose_commands = [
            "curl -L \"https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)\" -o /usr/local/bin/docker-compose",
            "chmod +x /usr/local/bin/docker-compose",
            "ln -sf /usr/local/bin/docker-compose /usr/bin/docker-compose"
        ]
        
        for cmd in compose_commands:
            print(f"   执行: {cmd}")
            stdin, stdout, stderr = ssh.exec_command(cmd, timeout=300)
            stdout.read()
        
        # 检查Docker Compose
        print("\n🔍 检查Docker Compose...")
        stdin, stdout, stderr = ssh.exec_command("docker-compose --version")
        output = stdout.read().decode().strip()
        if output:
            print(f"✅ Docker Compose版本: {output}")
        
        # 5. 重新部署服务
        print("\n🚀 重新部署服务...")
        deploy_commands = [
            "cd /opt/knowledge-graph",
            "docker-compose down || true",
            "docker-compose pull || true",
            "docker-compose up -d"
        ]
        
        deploy_cmd = " && ".join(deploy_commands)
        print(f"执行: {deploy_cmd}")
        stdin, stdout, stderr = ssh.exec_command(deploy_cmd, timeout=600)
        
        # 实时显示输出
        while True:
            line = stdout.readline()
            if not line:
                break
            print(f"   {line.strip()}")
        
        # 6. 等待服务启动
        print("\n⏳ 等待服务启动...")
        time.sleep(60)
        
        # 7. 检查服务状态
        print("\n🔍 检查服务状态...")
        status_commands = [
            "cd /opt/knowledge-graph && docker-compose ps",
            "docker ps",
            "netstat -tlnp | grep ':7474\\|:8000\\|:9090\\|:3000'"
        ]
        
        for cmd in status_commands:
            print(f"\n执行: {cmd}")
            stdin, stdout, stderr = ssh.exec_command(cmd)
            output = stdout.read().decode().strip()
            if output:
                print(output)
        
        # 8. 测试服务连接
        print("\n🌐 测试服务连接...")
        test_commands = [
            "curl -I http://localhost:7474 2>/dev/null | head -1 || echo 'Neo4j连接失败'",
            "curl -I http://localhost:8000 2>/dev/null | head -1 || echo 'API连接失败'",
            "curl -I http://localhost:9090 2>/dev/null | head -1 || echo 'Prometheus连接失败'",
            "curl -I http://localhost:3000 2>/dev/null | head -1 || echo 'Grafana连接失败'"
        ]
        
        for cmd in test_commands:
            stdin, stdout, stderr = ssh.exec_command(cmd)
            output = stdout.read().decode().strip()
            if output:
                print(f"   {output}")
        
        # 9. 检查日志
        print("\n📋 检查服务日志...")
        log_commands = [
            "cd /opt/knowledge-graph && docker-compose logs --tail=10 neo4j",
            "cd /opt/knowledge-graph && docker-compose logs --tail=10 api"
        ]
        
        for cmd in log_commands:
            print(f"\n执行: {cmd}")
            stdin, stdout, stderr = ssh.exec_command(cmd)
            output = stdout.read().decode().strip()
            if output:
                print(output)
        
        ssh.close()
        
        print("\n🎉 修复完成！")
        print("=" * 50)
        print("🌐 请尝试访问以下地址:")
        print(f"   • Neo4j浏览器:    http://{host}:7474")
        print(f"   • API服务:        http://{host}:8000")
        print(f"   • API文档:        http://{host}:8000/docs")
        print(f"   • 健康检查:       http://{host}:8000/health")
        print(f"   • Prometheus:     http://{host}:9090")
        print(f"   • Grafana:        http://{host}:3000")
        
        return True
        
    except Exception as e:
        print(f"❌ 修复失败: {e}")
        return False

def main():
    """主函数"""
    print("🔧 知识图谱系统部署修复工具")
    print("=" * 50)
    
    confirm = input("确认开始修复部署? (y/N): ").strip().lower()
    if confirm != 'y':
        print("修复已取消")
        return False
    
    return fix_deployment()

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n💡 如果服务仍然无法访问，请检查:")
            print("   1. 服务器防火墙设置")
            print("   2. 云服务商安全组配置")
            print("   3. 端口是否正确开放")
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户取消修复")
    except Exception as e:
        print(f"\n❌ 修复过程中发生错误: {e}")
