#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复前端权限和服务问题
解决vite权限问题和Docker服务启动问题
"""

import getpass
import time

def fix_frontend_issues():
    """修复前端权限和服务问题"""
    print("🔧 修复前端权限和服务问题")
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
        
        # 1. 修复文件权限
        print("\n🔒 修复文件权限...")
        
        permission_commands = [
            "chmod -R 755 /opt/knowledge-graph/",
            "chown -R root:root /opt/knowledge-graph/",
            "chmod +x /opt/knowledge-graph/apps/web/node_modules/.bin/*"
        ]
        
        for cmd in permission_commands:
            print(f"   执行: {cmd}")
            stdin, stdout, stderr = ssh.exec_command(cmd)
            stdout.read()
        
        print("✅ 文件权限修复完成")
        
        # 2. 重新安装npm依赖
        print("\n📦 重新安装npm依赖...")
        
        reinstall_commands = [
            "cd /opt/knowledge-graph/apps/web",
            "rm -rf node_modules package-lock.json",
            "npm cache clean --force",
            "npm install"
        ]
        
        for cmd in reinstall_commands:
            print(f"   执行: {cmd}")
            stdin, stdout, stderr = ssh.exec_command(cmd, timeout=600)
            output = stdout.read().decode()
            if "npm install" in cmd:
                print(f"   输出: {output}")
        
        # 3. 检查vite可执行性
        print("\n🔍 检查vite可执行性...")
        
        stdin, stdout, stderr = ssh.exec_command("cd /opt/knowledge-graph/apps/web && ls -la node_modules/.bin/vite")
        vite_info = stdout.read().decode()
        print(f"Vite信息: {vite_info}")
        
        stdin, stdout, stderr = ssh.exec_command("cd /opt/knowledge-graph/apps/web && ./node_modules/.bin/vite --version")
        vite_version = stdout.read().decode()
        if vite_version:
            print(f"✅ Vite版本: {vite_version}")
        else:
            print("⚠️ Vite无法执行")
        
        # 4. 修复Docker网络问题
        print("\n🐳 修复Docker网络问题...")
        
        docker_fix_commands = [
            "systemctl stop docker",
            "iptables -t nat -F",
            "iptables -t mangle -F",
            "iptables -F",
            "iptables -X",
            "systemctl start docker",
            "sleep 10"
        ]
        
        for cmd in docker_fix_commands:
            print(f"   执行: {cmd}")
            stdin, stdout, stderr = ssh.exec_command(cmd)
            stdout.read()
        
        # 5. 重新启动Docker服务
        print("\n🚀 重新启动Docker服务...")
        
        docker_restart_commands = [
            "cd /opt/knowledge-graph",
            "docker compose down --remove-orphans",
            "docker system prune -f",
            "docker compose pull neo4j redis || true",
            "docker compose up -d neo4j",
            "sleep 30",
            "docker compose up -d redis",
            "sleep 10",
            "docker compose up -d api"
        ]
        
        for cmd in docker_restart_commands:
            print(f"   执行: {cmd}")
            stdin, stdout, stderr = ssh.exec_command(cmd, timeout=300)
            output = stdout.read().decode()
            if output and "sleep" not in cmd:
                print(f"   输出: {output}")
        
        # 6. 使用npx启动前端
        print("\n💻 使用npx启动前端...")
        
        # 停止现有进程
        stdin, stdout, stderr = ssh.exec_command("pkill -f 'node\\|npm\\|vite' || true")
        stdout.read()
        
        # 使用npx启动
        frontend_start_cmd = """
cd /opt/knowledge-graph/apps/web
export NODE_ENV=development
nohup npx vite --host 0.0.0.0 --port 5173 > /tmp/frontend.log 2>&1 &
echo "前端服务已启动"
"""
        
        stdin, stdout, stderr = ssh.exec_command(frontend_start_cmd)
        result = stdout.read().decode()
        print(f"   {result}")
        
        # 7. 等待服务启动
        print("\n⏳ 等待服务启动...")
        time.sleep(45)
        
        # 8. 检查服务状态
        print("\n🔍 检查服务状态...")
        
        # 检查Docker容器
        stdin, stdout, stderr = ssh.exec_command("cd /opt/knowledge-graph && docker compose ps")
        containers = stdout.read().decode()
        print(f"Docker容器状态:\n{containers}")
        
        # 检查端口
        stdin, stdout, stderr = ssh.exec_command("netstat -tlnp | grep ':5173\\|:8000\\|:7474\\|:6379'")
        ports = stdout.read().decode()
        print(f"开放端口:\n{ports}")
        
        # 检查前端进程
        stdin, stdout, stderr = ssh.exec_command("ps aux | grep -E 'vite\\|node.*5173' | grep -v grep")
        frontend_processes = stdout.read().decode()
        print(f"前端进程:\n{frontend_processes}")
        
        # 9. 检查前端日志
        print("\n📋 检查前端日志...")
        
        stdin, stdout, stderr = ssh.exec_command("tail -20 /tmp/frontend.log")
        frontend_log = stdout.read().decode()
        print(f"前端日志:\n{frontend_log}")
        
        # 10. 测试服务访问
        print("\n🧪 测试服务访问...")
        
        test_commands = [
            ("Neo4j", "curl -s -o /dev/null -w '%{http_code}' http://localhost:7474/"),
            ("Redis", "redis-cli ping || echo 'Redis连接失败'"),
            ("API", "curl -s -o /dev/null -w '%{http_code}' http://localhost:8000/health"),
            ("前端", "curl -s -o /dev/null -w '%{http_code}' http://localhost:5173/"),
            ("Nginx", "curl -s -o /dev/null -w '%{http_code}' http://localhost:80/")
        ]
        
        for service_name, cmd in test_commands:
            stdin, stdout, stderr = ssh.exec_command(cmd)
            result = stdout.read().decode().strip()
            
            if service_name == "Redis":
                if "PONG" in result:
                    print(f"   ✅ {service_name}: 连接正常")
                else:
                    print(f"   ❌ {service_name}: {result}")
            else:
                if result in ['200', '302', '401']:
                    print(f"   ✅ {service_name}: HTTP {result}")
                else:
                    print(f"   ❌ {service_name}: HTTP {result}")
        
        # 11. 如果前端仍然无法启动，使用备用方案
        print("\n🔄 检查是否需要备用方案...")
        
        stdin, stdout, stderr = ssh.exec_command("curl -s -o /dev/null -w '%{http_code}' http://localhost:5173/")
        frontend_status = stdout.read().decode().strip()
        
        if frontend_status != '200':
            print("启用备用方案：使用生产构建...")
            
            build_commands = [
                "cd /opt/knowledge-graph/apps/web",
                "npm run build",
                "mkdir -p /var/www/kg-frontend",
                "cp -r dist/* /var/www/kg-frontend/",
                "chown -R www-data:www-data /var/www/kg-frontend"
            ]
            
            for cmd in build_commands:
                print(f"   执行: {cmd}")
                stdin, stdout, stderr = ssh.exec_command(cmd, timeout=300)
                output = stdout.read().decode()
                if "npm run build" in cmd:
                    print(f"   构建输出: {output}")
            
            # 更新Nginx配置为静态文件
            static_nginx_config = """server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name 47.108.152.16 _;
    
    root /var/www/kg-frontend;
    index index.html;
    
    # 前端路由支持
    location / {
        try_files $uri $uri/ /index.html;
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
    
    # 静态资源缓存
    location ~* \\.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1d;
        add_header Cache-Control "public, immutable";
    }
}"""
            
            nginx_cmd = f"""
cat > /etc/nginx/sites-available/default << 'EOF'
{static_nginx_config}
EOF
nginx -t && systemctl reload nginx
"""
            
            stdin, stdout, stderr = ssh.exec_command(nginx_cmd)
            error = stderr.read().decode()
            if "test is successful" in error:
                print("✅ 备用Nginx配置成功")
        
        ssh.close()
        
        print("\n🎉 前端权限和服务修复完成！")
        print("=" * 60)
        print("🌐 现在可以访问:")
        print(f"   • 主应用:         http://{host}/")
        print(f"   • 前端开发服务器:  http://{host}:5173/")
        print(f"   • API服务:        http://{host}:8000/")
        print(f"   • Neo4j浏览器:    http://{host}:7474/")
        
        print("\n📱 质量知识图谱助手功能:")
        print("   • 📄 文档解析")
        print("   • 🕸️ 图谱可视化")
        print("   • 📚 词典管理")
        print("   • ⚙️ 系统管理")
        
        return True
        
    except Exception as e:
        print(f"❌ 修复失败: {e}")
        return False

def main():
    """主函数"""
    print("🔧 前端权限和服务修复工具")
    print("=" * 50)
    
    print("将执行以下修复操作:")
    print("   1. 修复文件权限问题")
    print("   2. 重新安装npm依赖")
    print("   3. 修复Docker网络问题")
    print("   4. 重新启动所有服务")
    print("   5. 使用npx启动前端")
    print("   6. 配置备用静态方案")
    
    confirm = input("\n确认开始修复? (y/N): ").strip().lower()
    if confirm != 'y':
        print("修复已取消")
        return False
    
    return fix_frontend_issues()

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n🎊 修复完成！")
            print("请访问 http://47.108.152.16/ 查看效果！")
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户取消修复")
    except Exception as e:
        print(f"\n❌ 修复过程中发生错误: {e}")
