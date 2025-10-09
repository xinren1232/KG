#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
诊断前端访问问题
解决403 Forbidden错误
"""

import getpass
import time

def diagnose_frontend_access():
    """诊断前端访问问题"""
    print("🔍 诊断前端访问问题 - 解决403 Forbidden")
    print("=" * 60)
    
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
        
        # 1. 检查当前服务状态
        print("\n📋 检查当前服务状态...")
        
        # 检查Docker容器
        stdin, stdout, stderr = ssh.exec_command("docker ps")
        containers = stdout.read().decode()
        print(f"运行中的容器:\n{containers}")
        
        # 检查端口占用
        stdin, stdout, stderr = ssh.exec_command("netstat -tlnp | grep ':80\\|:8000\\|:5173\\|:3000'")
        ports = stdout.read().decode()
        print(f"端口占用情况:\n{ports}")
        
        # 2. 检查Nginx状态
        print("\n🌐 检查Nginx状态...")
        nginx_commands = [
            "systemctl status nginx",
            "nginx -t",
            "ps aux | grep nginx"
        ]
        
        for cmd in nginx_commands:
            print(f"\n执行: {cmd}")
            stdin, stdout, stderr = ssh.exec_command(cmd)
            output = stdout.read().decode()
            error = stderr.read().decode()
            if output:
                print(f"输出: {output}")
            if error:
                print(f"错误: {error}")
        
        # 3. 检查防火墙和安全组
        print("\n🔒 检查防火墙设置...")
        firewall_commands = [
            "ufw status",
            "iptables -L -n | grep -E '80|8000|5173|3000'",
            "ss -tlnp | grep ':80\\|:8000\\|:5173\\|:3000'"
        ]
        
        for cmd in firewall_commands:
            print(f"\n执行: {cmd}")
            stdin, stdout, stderr = ssh.exec_command(cmd)
            output = stdout.read().decode()
            if output:
                print(f"输出: {output}")
        
        # 4. 检查项目配置
        print("\n📁 检查项目配置...")
        
        # 检查项目目录
        stdin, stdout, stderr = ssh.exec_command("ls -la /opt/knowledge-graph/")
        project_files = stdout.read().decode()
        print(f"项目文件:\n{project_files}")
        
        # 检查Docker Compose配置
        stdin, stdout, stderr = ssh.exec_command("cat /opt/knowledge-graph/docker-compose.yml")
        compose_config = stdout.read().decode()
        print(f"Docker Compose配置:\n{compose_config[:500]}...")
        
        # 5. 启动前端服务
        print("\n🚀 尝试启动前端服务...")
        
        # 方案1: 使用Docker启动前端
        print("方案1: Docker方式启动前端...")
        docker_commands = [
            "cd /opt/knowledge-graph",
            "docker compose down web || true",
            "docker compose up -d web"
        ]
        
        for cmd in docker_commands:
            print(f"   执行: {cmd}")
            stdin, stdout, stderr = ssh.exec_command(cmd, timeout=120)
            output = stdout.read().decode()
            error = stderr.read().decode()
            if output:
                print(f"   输出: {output}")
            if error and "warning" not in error.lower():
                print(f"   错误: {error}")
        
        # 6. 配置Nginx反向代理
        print("\n🌐 配置Nginx反向代理...")
        
        # 创建Nginx配置
        nginx_config = """
server {
    listen 80;
    server_name 47.108.152.16;
    
    # 前端静态文件
    location / {
        proxy_pass http://localhost:5173;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket支持
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
    
    # API代理
    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Neo4j代理
    location /neo4j/ {
        proxy_pass http://localhost:7474/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
"""
        
        # 写入Nginx配置
        create_nginx_cmd = f"""
cat > /etc/nginx/sites-available/knowledge-graph << 'EOF'
{nginx_config}
EOF
"""
        stdin, stdout, stderr = ssh.exec_command(create_nginx_cmd)
        stdout.read()
        
        # 启用站点
        nginx_setup_commands = [
            "ln -sf /etc/nginx/sites-available/knowledge-graph /etc/nginx/sites-enabled/",
            "rm -f /etc/nginx/sites-enabled/default",
            "nginx -t",
            "systemctl restart nginx",
            "systemctl enable nginx"
        ]
        
        for cmd in nginx_setup_commands:
            print(f"   执行: {cmd}")
            stdin, stdout, stderr = ssh.exec_command(cmd)
            output = stdout.read().decode()
            error = stderr.read().decode()
            if output:
                print(f"   输出: {output}")
            if error and "test is successful" not in error:
                print(f"   错误: {error}")
        
        # 7. 直接启动前端开发服务器
        print("\n💻 启动前端开发服务器...")
        
        # 检查Node.js
        stdin, stdout, stderr = ssh.exec_command("node --version && npm --version")
        node_info = stdout.read().decode()
        if node_info:
            print(f"Node.js版本: {node_info}")
        else:
            print("安装Node.js...")
            install_node_commands = [
                "curl -fsSL https://deb.nodesource.com/setup_18.x | bash -",
                "apt-get install -y nodejs"
            ]
            
            for cmd in install_node_commands:
                stdin, stdout, stderr = ssh.exec_command(cmd, timeout=300)
                stdout.read()
        
        # 启动前端服务
        frontend_commands = [
            "cd /opt/knowledge-graph/apps/web",
            "npm install || true",
            "nohup npm run dev -- --host 0.0.0.0 --port 5173 > /tmp/frontend.log 2>&1 &"
        ]
        
        for cmd in frontend_commands:
            print(f"   执行: {cmd}")
            stdin, stdout, stderr = ssh.exec_command(cmd, timeout=300)
            output = stdout.read().decode()
            if output:
                print(f"   输出: {output}")
        
        # 8. 等待服务启动
        print("\n⏳ 等待服务启动...")
        time.sleep(30)
        
        # 9. 验证服务状态
        print("\n🔍 验证服务状态...")
        
        # 检查端口
        stdin, stdout, stderr = ssh.exec_command("netstat -tlnp | grep ':80\\|:5173\\|:8000'")
        ports_after = stdout.read().decode()
        print(f"服务端口:\n{ports_after}")
        
        # 测试HTTP访问
        test_commands = [
            ("Nginx (80)", "curl -I http://localhost:80 2>/dev/null | head -1 || echo 'Nginx访问失败'"),
            ("前端 (5173)", "curl -I http://localhost:5173 2>/dev/null | head -1 || echo '前端访问失败'"),
            ("API (8000)", "curl -I http://localhost:8000 2>/dev/null | head -1 || echo 'API访问失败'")
        ]
        
        for service_name, cmd in test_commands:
            stdin, stdout, stderr = ssh.exec_command(cmd)
            result = stdout.read().decode().strip()
            print(f"   {service_name}: {result}")
        
        # 10. 检查日志
        print("\n📋 检查服务日志...")
        
        log_commands = [
            "tail -10 /var/log/nginx/error.log 2>/dev/null || echo 'Nginx错误日志为空'",
            "tail -10 /tmp/frontend.log 2>/dev/null || echo '前端日志为空'",
            "docker compose logs --tail=5 web 2>/dev/null || echo 'Docker前端日志为空'"
        ]
        
        for cmd in log_commands:
            print(f"\n执行: {cmd}")
            stdin, stdout, stderr = ssh.exec_command(f"cd /opt/knowledge-graph && {cmd}")
            output = stdout.read().decode()
            if output:
                print(output)
        
        ssh.close()
        
        print("\n🎉 前端访问问题诊断完成！")
        print("=" * 60)
        print("🌐 现在尝试访问以下地址:")
        print(f"   • 主页面:         http://{host}/")
        print(f"   • 前端直接访问:    http://{host}:5173/")
        print(f"   • API服务:        http://{host}:8000/")
        print(f"   • Neo4j浏览器:    http://{host}:7474/")
        
        print("\n💡 如果仍然无法访问，请检查:")
        print("   1. 云服务器安全组是否开放端口 80, 5173, 8000, 7474")
        print("   2. 服务器防火墙设置")
        print("   3. 等待几分钟让服务完全启动")
        
        return True
        
    except Exception as e:
        print(f"❌ 诊断失败: {e}")
        return False

def main():
    """主函数"""
    print("🔍 前端访问问题诊断工具")
    print("=" * 50)
    
    print("检测到前端访问403 Forbidden错误")
    print("这通常是由以下原因造成的:")
    print("   1. 前端服务未启动")
    print("   2. Nginx配置问题")
    print("   3. 防火墙/安全组设置")
    print("   4. 端口冲突")
    
    confirm = input("\n确认开始诊断并修复? (y/N): ").strip().lower()
    if confirm != 'y':
        print("诊断已取消")
        return False
    
    return diagnose_frontend_access()

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n🎊 前端访问问题诊断完成！")
            print("请尝试重新访问前端页面！")
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户取消诊断")
    except Exception as e:
        print(f"\n❌ 诊断过程中发生错误: {e}")
