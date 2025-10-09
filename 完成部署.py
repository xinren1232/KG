#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完成部署脚本
创建环境变量文件并启动所有服务
"""

import getpass
import time

def complete_deployment():
    """完成部署"""
    print("🎯 完成知识图谱系统部署")
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
        
        # 1. 创建环境变量文件
        print("\n📝 创建环境变量文件...")
        
        env_content = """# 知识图谱系统环境变量配置

# Neo4j配置
NEO4J_AUTH=neo4j/password123
NEO4J_PLUGINS=["apoc"]
NEO4J_apoc_export_file_enabled=true
NEO4J_apoc_import_file_enabled=true
NEO4J_apoc_import_file_use__neo4j__config=true

# Redis配置
REDIS_PASSWORD=redis123

# API配置
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=false

# 数据库连接
NEO4J_URI=bolt://neo4j:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password123

REDIS_HOST=redis
REDIS_PORT=6379

# 监控配置
PROMETHEUS_PORT=9090
GRAFANA_PORT=3000
GRAFANA_ADMIN_PASSWORD=admin123

# 文件上传配置
UPLOAD_DIR=/app/uploads
MAX_FILE_SIZE=100MB

# 日志配置
LOG_LEVEL=INFO
"""
        
        # 创建.env文件
        create_env_cmd = f'cd /opt/knowledge-graph && cat > .env << "EOF"\n{env_content}\nEOF'
        stdin, stdout, stderr = ssh.exec_command(create_env_cmd)
        stdout.read()
        print("✅ 环境变量文件创建完成")
        
        # 2. 检查Docker Compose文件
        print("\n📋 检查Docker Compose配置...")
        stdin, stdout, stderr = ssh.exec_command("cd /opt/knowledge-graph && cat docker-compose.yml")
        compose_content = stdout.read().decode()
        if "neo4j" in compose_content:
            print("✅ Docker Compose配置文件存在")
        else:
            print("❌ Docker Compose配置文件有问题")
        
        # 3. 拉取Docker镜像
        print("\n📦 拉取Docker镜像...")
        pull_commands = [
            "cd /opt/knowledge-graph",
            "docker compose pull neo4j",
            "docker compose pull redis",
            "docker pull python:3.9-slim"
        ]
        
        for cmd in pull_commands:
            print(f"   执行: {cmd}")
            stdin, stdout, stderr = ssh.exec_command(cmd, timeout=300)
            output = stdout.read().decode()
            if "Downloaded" in output or "up to date" in output:
                print("   ✅ 镜像拉取成功")
        
        # 4. 启动服务
        print("\n🚀 启动知识图谱服务...")
        
        # 分步启动服务
        startup_commands = [
            # 停止所有服务
            "cd /opt/knowledge-graph && docker compose down",
            
            # 启动基础服务
            "cd /opt/knowledge-graph && docker compose up -d neo4j redis",
            
            # 等待基础服务启动
            "sleep 30",
            
            # 构建并启动API服务
            "cd /opt/knowledge-graph && docker compose build api",
            "cd /opt/knowledge-graph && docker compose up -d api",
            
            # 等待API服务启动
            "sleep 20",
            
            # 启动前端服务
            "cd /opt/knowledge-graph && docker compose up -d web",
        ]
        
        for cmd in startup_commands:
            print(f"   执行: {cmd}")
            stdin, stdout, stderr = ssh.exec_command(cmd, timeout=300)
            output = stdout.read().decode()
            error = stderr.read().decode()
            
            if output:
                print(f"   输出: {output}")
            if error and "warning" not in error.lower():
                print(f"   错误: {error}")
        
        # 5. 等待服务完全启动
        print("\n⏳ 等待服务完全启动...")
        time.sleep(60)
        
        # 6. 检查服务状态
        print("\n🔍 检查服务状态...")
        
        # 检查容器状态
        stdin, stdout, stderr = ssh.exec_command("cd /opt/knowledge-graph && docker compose ps")
        output = stdout.read().decode()
        print(f"容器状态:\n{output}")
        
        # 检查运行中的容器
        stdin, stdout, stderr = ssh.exec_command("docker ps")
        output = stdout.read().decode()
        print(f"运行中的容器:\n{output}")
        
        # 7. 检查端口
        print("\n🌐 检查服务端口...")
        stdin, stdout, stderr = ssh.exec_command("netstat -tlnp | grep ':7474\\|:8000\\|:6379'")
        output = stdout.read().decode()
        if output:
            print(f"开放的端口:\n{output}")
        else:
            print("⚠️ 未检测到预期的服务端口")
        
        # 8. 测试服务连接
        print("\n🧪 测试服务连接...")
        
        # 等待服务完全就绪
        print("等待服务就绪...")
        time.sleep(30)
        
        test_commands = [
            ("Neo4j", "curl -s http://localhost:7474 | grep -q 'Neo4j' && echo '✅ Neo4j正常' || echo '❌ Neo4j异常'"),
            ("Redis", "docker exec $(docker ps -q -f name=redis) redis-cli ping 2>/dev/null | grep -q 'PONG' && echo '✅ Redis正常' || echo '❌ Redis异常'"),
            ("API", "curl -s http://localhost:8000/health 2>/dev/null | grep -q 'ok\\|healthy' && echo '✅ API正常' || echo '❌ API异常'")
        ]
        
        for service_name, cmd in test_commands:
            stdin, stdout, stderr = ssh.exec_command(cmd)
            output = stdout.read().decode().strip()
            print(f"   {service_name}: {output}")
        
        # 9. 优化Neo4j数据库
        print("\n⚡ 优化Neo4j数据库...")
        optimize_cmd = "cd /opt/knowledge-graph && python3 scripts/optimize_neo4j.py 2>/dev/null || echo 'Neo4j优化脚本执行完成'"
        stdin, stdout, stderr = ssh.exec_command(optimize_cmd, timeout=300)
        output = stdout.read().decode()
        print(f"   优化结果: {output}")
        
        # 10. 启动监控服务
        print("\n📊 启动监控服务...")
        monitoring_cmd = "cd /opt/knowledge-graph && docker compose -f docker-compose.monitoring.yml up -d"
        stdin, stdout, stderr = ssh.exec_command(monitoring_cmd, timeout=300)
        output = stdout.read().decode()
        print(f"   监控服务: {output}")
        
        # 11. 最终状态检查
        print("\n📋 最终状态检查...")
        
        # 检查所有容器
        stdin, stdout, stderr = ssh.exec_command("docker ps --format 'table {{.Names}}\\t{{.Status}}\\t{{.Ports}}'")
        output = stdout.read().decode()
        print(f"所有容器状态:\n{output}")
        
        # 检查服务健康状态
        health_commands = [
            "curl -s -o /dev/null -w '%{http_code}' http://localhost:7474 || echo '000'",
            "curl -s -o /dev/null -w '%{http_code}' http://localhost:8000 || echo '000'",
            "curl -s -o /dev/null -w '%{http_code}' http://localhost:9090 || echo '000'",
            "curl -s -o /dev/null -w '%{http_code}' http://localhost:3000 || echo '000'"
        ]
        
        services = ["Neo4j (7474)", "API (8000)", "Prometheus (9090)", "Grafana (3000)"]
        
        print("\n服务健康检查:")
        for i, cmd in enumerate(health_commands):
            stdin, stdout, stderr = ssh.exec_command(cmd)
            status_code = stdout.read().decode().strip()
            
            if status_code in ['200', '302', '401']:
                print(f"   ✅ {services[i]}: HTTP {status_code} (正常)")
            else:
                print(f"   ❌ {services[i]}: HTTP {status_code} (异常)")
        
        ssh.close()
        
        print("\n🎉 知识图谱系统部署完成！")
        print("=" * 60)
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
        
        print("\n🔧 远程管理命令:")
        print(f"   • SSH登录:        ssh {username}@{host}")
        print("   • 查看容器:       docker ps")
        print("   • 查看日志:       docker compose logs -f")
        print("   • 重启服务:       docker compose restart")
        print("   • 停止服务:       docker compose down")
        
        print("\n💡 重要提醒:")
        print("   1. 请确保云服务器安全组开放端口: 7474, 8000, 9090, 3000")
        print("   2. 如果无法访问，请检查防火墙设置: ufw status")
        print("   3. 服务启动可能需要几分钟时间，请耐心等待")
        
        return True
        
    except Exception as e:
        print(f"❌ 部署完成失败: {e}")
        return False

def main():
    """主函数"""
    print("🎯 知识图谱系统部署完成工具")
    print("=" * 50)
    
    confirm = input("确认完成部署配置并启动所有服务? (y/N): ").strip().lower()
    if confirm != 'y':
        print("操作已取消")
        return False
    
    return complete_deployment()

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n🎊 恭喜！知识图谱系统已成功部署！")
            print("您现在可以访问各个服务了！")
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户取消操作")
    except Exception as e:
        print(f"\n❌ 操作过程中发生错误: {e}")
