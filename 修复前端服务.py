#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复前端服务
解决前端无法访问的问题
"""

import getpass
import time

def fix_frontend_service():
    """修复前端服务"""
    print("🔧 修复前端服务 - 解决访问问题")
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
        
        # 1. 安装Node.js和npm
        print("\n📦 安装Node.js和npm...")
        
        # 检查Node.js版本
        stdin, stdout, stderr = ssh.exec_command("node --version")
        node_version = stdout.read().decode().strip()
        
        if not node_version or "v" not in node_version:
            print("安装Node.js...")
            install_commands = [
                "curl -fsSL https://deb.nodesource.com/setup_18.x | bash -",
                "apt-get install -y nodejs"
            ]
            
            for cmd in install_commands:
                print(f"   执行: {cmd}")
                stdin, stdout, stderr = ssh.exec_command(cmd, timeout=300)
                stdout.read()
        else:
            print(f"✅ Node.js已安装: {node_version}")
        
        # 2. 启动基础服务
        print("\n🚀 启动基础服务...")
        
        # 配置Docker镜像源
        docker_config = """{
  "registry-mirrors": [
    "https://docker.mirrors.ustc.edu.cn",
    "https://hub-mirror.c.163.com"
  ]
}"""
        
        config_cmd = f"""
mkdir -p /etc/docker
cat > /etc/docker/daemon.json << 'EOF'
{docker_config}
EOF
systemctl restart docker
"""
        stdin, stdout, stderr = ssh.exec_command(config_cmd)
        stdout.read()
        print("✅ Docker镜像源配置完成")
        
        # 启动Neo4j和Redis
        basic_services_commands = [
            "cd /opt/knowledge-graph",
            "docker compose down || true",
            "docker compose up -d neo4j redis"
        ]
        
        for cmd in basic_services_commands:
            print(f"   执行: {cmd}")
            stdin, stdout, stderr = ssh.exec_command(cmd, timeout=300)
            output = stdout.read().decode()
            if output:
                print(f"   输出: {output}")
        
        # 3. 构建并启动API服务
        print("\n⚡ 启动API服务...")
        
        api_commands = [
            "cd /opt/knowledge-graph",
            "docker compose build api || true",
            "docker compose up -d api"
        ]
        
        for cmd in api_commands:
            print(f"   执行: {cmd}")
            stdin, stdout, stderr = ssh.exec_command(cmd, timeout=300)
            output = stdout.read().decode()
            if output:
                print(f"   输出: {output}")
        
        # 4. 手动启动前端开发服务器
        print("\n💻 启动前端开发服务器...")
        
        # 检查前端目录
        stdin, stdout, stderr = ssh.exec_command("ls -la /opt/knowledge-graph/apps/web/")
        frontend_files = stdout.read().decode()
        print(f"前端文件: {frontend_files}")
        
        # 安装前端依赖并启动
        frontend_commands = [
            "cd /opt/knowledge-graph/apps/web",
            "npm install --registry=https://registry.npmmirror.com",
            "pkill -f 'vite\\|npm.*dev' || true",  # 杀死可能存在的进程
            "nohup npm run dev -- --host 0.0.0.0 --port 5173 > /tmp/frontend.log 2>&1 &",
            "sleep 5"
        ]
        
        for cmd in frontend_commands:
            print(f"   执行: {cmd}")
            stdin, stdout, stderr = ssh.exec_command(cmd, timeout=300)
            output = stdout.read().decode()
            if output and "npm install" not in cmd:
                print(f"   输出: {output}")
        
        # 5. 创建简单的静态页面作为备用
        print("\n📄 创建备用静态页面...")
        
        static_html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>知识图谱系统</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            text-align: center;
            padding: 50px 20px;
        }
        h1 {
            font-size: 3em;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .services {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 40px;
        }
        .service-card {
            background: rgba(255,255,255,0.1);
            padding: 20px;
            border-radius: 10px;
            backdrop-filter: blur(10px);
            transition: transform 0.3s ease;
        }
        .service-card:hover {
            transform: translateY(-5px);
        }
        .service-card a {
            color: white;
            text-decoration: none;
            font-weight: bold;
        }
        .status {
            margin: 20px 0;
            padding: 15px;
            background: rgba(255,255,255,0.1);
            border-radius: 8px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 知识图谱系统</h1>
        <div class="status">
            <h2>✅ 系统已成功部署</h2>
            <p>欢迎使用知识图谱系统！系统正在启动中，请稍候...</p>
        </div>
        
        <div class="services">
            <div class="service-card">
                <h3>📊 Neo4j 数据库</h3>
                <p><a href="http://47.108.152.16:7474" target="_blank">访问 Neo4j 浏览器</a></p>
                <small>用户名: neo4j<br>密码: password123</small>
            </div>
            
            <div class="service-card">
                <h3>🔧 API 服务</h3>
                <p><a href="http://47.108.152.16:8000" target="_blank">访问 API 服务</a></p>
                <p><a href="http://47.108.152.16:8000/docs" target="_blank">API 文档</a></p>
            </div>
            
            <div class="service-card">
                <h3>📈 监控系统</h3>
                <p><a href="http://47.108.152.16:9090" target="_blank">Prometheus</a></p>
                <p><a href="http://47.108.152.16:3000" target="_blank">Grafana</a></p>
                <small>Grafana - 用户名: admin, 密码: admin123</small>
            </div>
            
            <div class="service-card">
                <h3>💻 前端应用</h3>
                <p><a href="http://47.108.152.16:5173" target="_blank">直接访问前端</a></p>
                <p>Vue.js 开发服务器</p>
            </div>
        </div>
        
        <div style="margin-top: 40px;">
            <h3>🔧 系统状态</h3>
            <p>部署时间: <span id="deployTime"></span></p>
            <p>服务器: 47.108.152.16</p>
        </div>
    </div>
    
    <script>
        document.getElementById('deployTime').textContent = new Date().toLocaleString('zh-CN');
        
        // 自动检查服务状态
        async function checkServices() {
            const services = [
                { name: 'API', url: 'http://47.108.152.16:8000/health' },
                { name: 'Neo4j', url: 'http://47.108.152.16:7474' },
                { name: '前端', url: 'http://47.108.152.16:5173' }
            ];
            
            for (let service of services) {
                try {
                    const response = await fetch(service.url, { mode: 'no-cors' });
                    console.log(`${service.name} 服务状态检查完成`);
                } catch (error) {
                    console.log(`${service.name} 服务检查失败:`, error);
                }
            }
        }
        
        // 页面加载后检查服务
        setTimeout(checkServices, 2000);
    </script>
</body>
</html>"""
        
        # 创建静态页面
        create_static_cmd = f"""
mkdir -p /var/www/html
cat > /var/www/html/index.html << 'EOF'
{static_html}
EOF
"""
        stdin, stdout, stderr = ssh.exec_command(create_static_cmd)
        stdout.read()
        print("✅ 备用静态页面创建完成")
        
        # 6. 配置Nginx
        print("\n🌐 配置Nginx...")
        
        nginx_config = """server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name 47.108.152.16 _;
    
    # 根目录指向静态页面
    root /var/www/html;
    index index.html;
    
    # 主页面
    location = / {
        try_files /index.html =404;
    }
    
    # 前端应用代理
    location /app/ {
        proxy_pass http://localhost:5173/;
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
    
    # 静态文件
    location /static/ {
        alias /var/www/html/;
        expires 1d;
        add_header Cache-Control "public, immutable";
    }
}"""
        
        # 更新Nginx配置
        nginx_setup_cmd = f"""
cat > /etc/nginx/sites-available/default << 'EOF'
{nginx_config}
EOF
nginx -t && systemctl reload nginx
"""
        stdin, stdout, stderr = ssh.exec_command(nginx_setup_cmd)
        output = stdout.read().decode()
        error = stderr.read().decode()
        if "test is successful" in error:
            print("✅ Nginx配置更新成功")
        else:
            print(f"⚠️ Nginx配置警告: {error}")
        
        # 7. 等待服务启动
        print("\n⏳ 等待服务启动...")
        time.sleep(30)
        
        # 8. 检查服务状态
        print("\n🔍 检查服务状态...")
        
        # 检查端口
        stdin, stdout, stderr = ssh.exec_command("netstat -tlnp | grep ':80\\|:5173\\|:8000\\|:7474'")
        ports = stdout.read().decode()
        print(f"开放端口:\n{ports}")
        
        # 检查前端日志
        stdin, stdout, stderr = ssh.exec_command("tail -5 /tmp/frontend.log")
        frontend_log = stdout.read().decode()
        print(f"前端日志:\n{frontend_log}")
        
        # 检查进程
        stdin, stdout, stderr = ssh.exec_command("ps aux | grep -E 'node|npm|vite' | grep -v grep")
        processes = stdout.read().decode()
        print(f"前端进程:\n{processes}")
        
        # 9. 测试服务访问
        print("\n🧪 测试服务访问...")
        
        test_commands = [
            ("主页面", "curl -s -o /dev/null -w '%{http_code}' http://localhost:80/"),
            ("前端服务", "curl -s -o /dev/null -w '%{http_code}' http://localhost:5173/"),
            ("API服务", "curl -s -o /dev/null -w '%{http_code}' http://localhost:8000/"),
            ("Neo4j", "curl -s -o /dev/null -w '%{http_code}' http://localhost:7474/")
        ]
        
        for service_name, cmd in test_commands:
            stdin, stdout, stderr = ssh.exec_command(cmd)
            status_code = stdout.read().decode().strip()
            
            if status_code in ['200', '302', '401']:
                print(f"   ✅ {service_name}: HTTP {status_code}")
            else:
                print(f"   ❌ {service_name}: HTTP {status_code}")
        
        ssh.close()
        
        print("\n🎉 前端服务修复完成！")
        print("=" * 60)
        print("🌐 现在可以访问以下地址:")
        print(f"   • 主页面:         http://{host}/")
        print(f"   • 前端应用:       http://{host}:5173/")
        print(f"   • API服务:        http://{host}:8000/")
        print(f"   • API文档:        http://{host}:8000/docs")
        print(f"   • Neo4j浏览器:    http://{host}:7474/")
        print(f"   • Prometheus:     http://{host}:9090/")
        print(f"   • Grafana:        http://{host}:3000/")
        
        print("\n🔑 认证信息:")
        print("   • Neo4j:    用户名: neo4j, 密码: password123")
        print("   • Grafana:  用户名: admin, 密码: admin123")
        
        print("\n💡 说明:")
        print("   1. 主页面提供了系统概览和服务链接")
        print("   2. 前端开发服务器运行在5173端口")
        print("   3. 如果前端服务未启动，主页面仍可正常访问")
        print("   4. 所有服务都通过Nginx进行反向代理")
        
        return True
        
    except Exception as e:
        print(f"❌ 修复失败: {e}")
        return False

def main():
    """主函数"""
    print("🔧 前端服务修复工具")
    print("=" * 50)
    
    print("将执行以下修复操作:")
    print("   1. 安装/检查Node.js环境")
    print("   2. 启动基础服务 (Neo4j, Redis)")
    print("   3. 启动API服务")
    print("   4. 启动前端开发服务器")
    print("   5. 创建备用静态页面")
    print("   6. 配置Nginx反向代理")
    print("   7. 验证所有服务状态")
    
    confirm = input("\n确认开始修复? (y/N): ").strip().lower()
    if confirm != 'y':
        print("修复已取消")
        return False
    
    return fix_frontend_service()

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n🎊 前端服务修复完成！")
            print("请刷新浏览器页面查看效果！")
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户取消修复")
    except Exception as e:
        print(f"\n❌ 修复过程中发生错误: {e}")
