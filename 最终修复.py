#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终修复脚本
解决Docker daemon问题并启动服务
"""

import getpass
import time

def final_fix():
    """最终修复"""
    print("🔧 最终修复 - 解决Docker daemon问题")
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
        
        # 1. 修复Docker daemon
        print("\n🐳 修复Docker daemon...")
        
        # 停止snap docker服务
        print("停止snap docker服务...")
        stop_commands = [
            "systemctl stop snap.docker.dockerd",
            "systemctl disable snap.docker.dockerd",
            "snap remove docker"
        ]
        
        for cmd in stop_commands:
            print(f"   执行: {cmd}")
            stdin, stdout, stderr = ssh.exec_command(cmd, timeout=60)
            stdout.read()
        
        # 使用官方方式安装Docker
        print("使用官方方式安装Docker...")
        install_commands = [
            # 清理旧的Docker
            "apt-get remove -y docker docker-engine docker.io containerd runc || true",
            
            # 安装依赖
            "apt-get update",
            "apt-get install -y ca-certificates curl gnupg lsb-release",
            
            # 添加Docker官方GPG密钥 (使用国内镜像)
            "mkdir -p /etc/apt/keyrings",
            "curl -fsSL https://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg",
            
            # 添加Docker仓库 (使用阿里云镜像)
            'echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://mirrors.aliyun.com/docker-ce/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null',
            
            # 更新包索引
            "apt-get update",
            
            # 安装Docker
            "apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin"
        ]
        
        for cmd in install_commands:
            print(f"   执行: {cmd}")
            stdin, stdout, stderr = ssh.exec_command(cmd, timeout=300)
            output = stdout.read().decode()
            error = stderr.read().decode()
            if "E:" in error or "ERROR" in error:
                print(f"   ⚠️ 警告: {error}")
        
        # 2. 启动Docker服务
        print("\n🚀 启动Docker服务...")
        service_commands = [
            "systemctl start docker",
            "systemctl enable docker",
            "systemctl status docker"
        ]
        
        for cmd in service_commands:
            print(f"   执行: {cmd}")
            stdin, stdout, stderr = ssh.exec_command(cmd, timeout=60)
            output = stdout.read().decode()
            if "active (running)" in output:
                print("   ✅ Docker服务启动成功")
            elif output:
                print(f"   输出: {output}")
        
        # 3. 验证Docker
        print("\n🔍 验证Docker安装...")
        verify_commands = [
            "docker --version",
            "docker info",
            "docker run hello-world"
        ]
        
        for cmd in verify_commands:
            print(f"\n执行: {cmd}")
            stdin, stdout, stderr = ssh.exec_command(cmd, timeout=120)
            output = stdout.read().decode().strip()
            error = stderr.read().decode().strip()
            
            if output:
                print(f"输出: {output}")
            if error and "Unable to find image" not in error:
                print(f"错误: {error}")
        
        # 4. 安装Docker Compose (如果需要)
        print("\n📦 确保Docker Compose可用...")
        stdin, stdout, stderr = ssh.exec_command("docker compose version")
        output = stdout.read().decode()
        if "Docker Compose version" in output:
            print("✅ Docker Compose已可用")
        else:
            print("安装独立的Docker Compose...")
            compose_cmd = 'curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && chmod +x /usr/local/bin/docker-compose'
            stdin, stdout, stderr = ssh.exec_command(compose_cmd, timeout=300)
            stdout.read()
        
        # 5. 重新部署服务
        print("\n🚀 重新部署知识图谱服务...")
        
        # 检查项目文件
        print("检查项目文件...")
        stdin, stdout, stderr = ssh.exec_command("ls -la /opt/knowledge-graph/")
        output = stdout.read().decode()
        print(f"项目文件: {output}")
        
        # 使用docker compose (新版本命令)
        deploy_commands = [
            "cd /opt/knowledge-graph",
            "docker compose down || docker-compose down || true",
            "docker compose up -d || docker-compose up -d"
        ]
        
        deploy_cmd = " && ".join(deploy_commands)
        print(f"执行部署: {deploy_cmd}")
        stdin, stdout, stderr = ssh.exec_command(deploy_cmd, timeout=600)
        
        # 显示输出
        output = stdout.read().decode()
        error = stderr.read().decode()
        if output:
            print(f"部署输出: {output}")
        if error:
            print(f"部署错误: {error}")
        
        # 6. 等待服务启动
        print("\n⏳ 等待服务启动...")
        time.sleep(30)
        
        # 7. 检查容器状态
        print("\n🔍 检查容器状态...")
        status_commands = [
            "docker ps -a",
            "docker compose ps || docker-compose ps || true"
        ]
        
        for cmd in status_commands:
            print(f"\n执行: {cmd}")
            stdin, stdout, stderr = ssh.exec_command(f"cd /opt/knowledge-graph && {cmd}")
            output = stdout.read().decode().strip()
            if output:
                print(output)
        
        # 8. 检查端口
        print("\n🌐 检查端口状态...")
        stdin, stdout, stderr = ssh.exec_command("netstat -tlnp | grep ':7474\\|:8000\\|:9090\\|:3000'")
        output = stdout.read().decode().strip()
        if output:
            print(f"开放端口: {output}")
        else:
            print("⚠️ 未检测到服务端口")
        
        # 9. 测试服务
        print("\n🧪 测试服务连接...")
        test_commands = [
            "curl -I http://localhost:7474 2>/dev/null | head -1 || echo 'Neo4j: 连接失败'",
            "curl -I http://localhost:8000 2>/dev/null | head -1 || echo 'API: 连接失败'",
            "curl -I http://localhost:9090 2>/dev/null | head -1 || echo 'Prometheus: 连接失败'",
            "curl -I http://localhost:3000 2>/dev/null | head -1 || echo 'Grafana: 连接失败'"
        ]
        
        for cmd in test_commands:
            stdin, stdout, stderr = ssh.exec_command(cmd)
            output = stdout.read().decode().strip()
            if output:
                print(f"   {output}")
        
        # 10. 检查日志
        print("\n📋 检查关键服务日志...")
        log_commands = [
            "cd /opt/knowledge-graph && docker compose logs --tail=5 neo4j || docker-compose logs --tail=5 neo4j || true",
            "cd /opt/knowledge-graph && docker compose logs --tail=5 api || docker-compose logs --tail=5 api || true"
        ]
        
        for cmd in log_commands:
            print(f"\n执行日志检查...")
            stdin, stdout, stderr = ssh.exec_command(cmd)
            output = stdout.read().decode().strip()
            if output:
                print(output)
        
        ssh.close()
        
        print("\n🎉 最终修复完成！")
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
        
        print("\n💡 如果服务仍然无法访问，请检查:")
        print("   1. 云服务器安全组是否开放端口 7474, 8000, 9090, 3000")
        print("   2. 服务器防火墙设置: ufw status")
        print("   3. 手动重启服务: docker compose restart")
        
        return True
        
    except Exception as e:
        print(f"❌ 最终修复失败: {e}")
        return False

def main():
    """主函数"""
    print("🔧 知识图谱系统最终修复工具")
    print("=" * 50)
    
    confirm = input("确认开始最终修复? (y/N): ").strip().lower()
    if confirm != 'y':
        print("修复已取消")
        return False
    
    return final_fix()

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n🎊 恭喜！知识图谱系统部署修复完成！")
            print("现在可以尝试访问各个服务了！")
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户取消修复")
    except Exception as e:
        print(f"\n❌ 修复过程中发生错误: {e}")
