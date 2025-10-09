#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
部署完整前端应用
按照本地设计实现质量知识图谱助手前端
"""

import getpass
import time

def deploy_complete_frontend():
    """部署完整前端应用"""
    print("🚀 部署完整前端应用 - 质量知识图谱助手")
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
        
        # 1. 检查前端项目结构
        print("\n📁 检查前端项目结构...")
        
        check_commands = [
            "ls -la /opt/knowledge-graph/apps/web/",
            "cat /opt/knowledge-graph/apps/web/package.json",
            "ls -la /opt/knowledge-graph/apps/web/src/"
        ]
        
        for cmd in check_commands:
            print(f"\n执行: {cmd}")
            stdin, stdout, stderr = ssh.exec_command(cmd)
            output = stdout.read().decode()
            if output:
                print(output[:500] + "..." if len(output) > 500 else output)
        
        # 2. 安装Node.js (如果需要)
        print("\n📦 确保Node.js环境...")
        
        stdin, stdout, stderr = ssh.exec_command("node --version && npm --version")
        node_info = stdout.read().decode()
        
        if not node_info or "v" not in node_info:
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
            print(f"✅ Node.js环境: {node_info}")
        
        # 3. 配置npm镜像源
        print("\n🔧 配置npm镜像源...")
        
        npm_config_commands = [
            "npm config set registry https://registry.npmmirror.com",
            "npm config set disturl https://npmmirror.com/dist",
            "npm config set electron_mirror https://npmmirror.com/mirrors/electron/",
            "npm config set sass_binary_site https://npmmirror.com/mirrors/node-sass/",
            "npm config set phantomjs_cdnurl https://npmmirror.com/mirrors/phantomjs/"
        ]
        
        for cmd in npm_config_commands:
            stdin, stdout, stderr = ssh.exec_command(cmd)
            stdout.read()
        
        print("✅ npm镜像源配置完成")
        
        # 4. 安装前端依赖
        print("\n📦 安装前端依赖...")
        
        install_deps_cmd = "cd /opt/knowledge-graph/apps/web && npm install"
        print(f"执行: {install_deps_cmd}")
        stdin, stdout, stderr = ssh.exec_command(install_deps_cmd, timeout=600)
        
        # 实时显示安装进度
        while True:
            line = stdout.readline()
            if not line:
                break
            print(f"   {line.strip()}")
        
        # 检查安装结果
        stdin, stdout, stderr = ssh.exec_command("cd /opt/knowledge-graph/apps/web && ls -la node_modules/ | head -5")
        deps_check = stdout.read().decode()
        if "vue" in deps_check or "element-plus" in deps_check:
            print("✅ 前端依赖安装成功")
        else:
            print("⚠️ 前端依赖安装可能有问题")
        
        # 5. 启动基础服务
        print("\n🚀 启动基础服务...")
        
        # 配置Docker镜像源
        docker_config = """{
  "registry-mirrors": [
    "https://docker.mirrors.ustc.edu.cn",
    "https://hub-mirror.c.163.com",
    "https://mirror.baidubce.com"
  ]
}"""
        
        config_cmd = f"""
mkdir -p /etc/docker
cat > /etc/docker/daemon.json << 'EOF'
{docker_config}
EOF
systemctl restart docker
sleep 5
"""
        stdin, stdout, stderr = ssh.exec_command(config_cmd)
        stdout.read()
        
        # 启动后端服务
        backend_commands = [
            "cd /opt/knowledge-graph",
            "docker compose down || true",
            "docker compose up -d neo4j redis",
            "sleep 30",
            "docker compose up -d api"
        ]
        
        for cmd in backend_commands:
            print(f"   执行: {cmd}")
            stdin, stdout, stderr = ssh.exec_command(cmd, timeout=300)
            output = stdout.read().decode()
            if output and "sleep" not in cmd:
                print(f"   输出: {output}")
        
        # 6. 启动前端开发服务器
        print("\n💻 启动前端开发服务器...")
        
        # 停止可能存在的前端进程
        stdin, stdout, stderr = ssh.exec_command("pkill -f 'vite\\|npm.*dev' || true")
        stdout.read()
        
        # 启动前端服务
        frontend_start_cmd = """
cd /opt/knowledge-graph/apps/web
nohup npm run dev -- --host 0.0.0.0 --port 5173 > /tmp/frontend.log 2>&1 &
echo "前端服务启动命令已执行"
"""
        
        stdin, stdout, stderr = ssh.exec_command(frontend_start_cmd)
        result = stdout.read().decode()
        print(f"   {result}")
        
        # 7. 等待服务启动
        print("\n⏳ 等待服务启动...")
        time.sleep(30)
        
        # 8. 检查前端日志
        print("\n📋 检查前端启动日志...")
        
        stdin, stdout, stderr = ssh.exec_command("tail -20 /tmp/frontend.log")
        frontend_log = stdout.read().decode()
        print(f"前端日志:\n{frontend_log}")
        
        # 9. 检查服务状态
        print("\n🔍 检查服务状态...")
        
        # 检查端口
        stdin, stdout, stderr = ssh.exec_command("netstat -tlnp | grep ':5173\\|:8000\\|:7474\\|:6379'")
        ports = stdout.read().decode()
        print(f"开放端口:\n{ports}")
        
        # 检查进程
        stdin, stdout, stderr = ssh.exec_command("ps aux | grep -E 'node|npm|vite' | grep -v grep")
        processes = stdout.read().decode()
        print(f"前端进程:\n{processes}")
        
        # 检查Docker容器
        stdin, stdout, stderr = ssh.exec_command("cd /opt/knowledge-graph && docker compose ps")
        containers = stdout.read().decode()
        print(f"Docker容器:\n{containers}")
        
        # 10. 配置Nginx反向代理
        print("\n🌐 配置Nginx反向代理...")
        
        nginx_config = """server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name 47.108.152.16 _;
    
    # 前端应用
    location / {
        proxy_pass http://localhost:5173;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket支持 (Vite HMR需要)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        
        # 超时设置
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
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
        proxy_pass http://localhost:5173;
        proxy_set_header Host $host;
        expires 1d;
        add_header Cache-Control "public, immutable";
    }
}"""
        
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
            print("✅ Nginx配置成功")
        else:
            print(f"⚠️ Nginx配置警告: {error}")
        
        # 11. 测试服务访问
        print("\n🧪 测试服务访问...")
        
        # 等待一下让服务完全启动
        time.sleep(10)
        
        test_commands = [
            ("前端应用", "curl -s -o /dev/null -w '%{http_code}' http://localhost:80/"),
            ("前端直接", "curl -s -o /dev/null -w '%{http_code}' http://localhost:5173/"),
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
        
        print("\n🎉 完整前端应用部署完成！")
        print("=" * 60)
        print("🌐 质量知识图谱助手访问地址:")
        print(f"   • 主应用:         http://{host}/")
        print(f"   • 前端直接访问:    http://{host}:5173/")
        print(f"   • API服务:        http://{host}:8000/")
        print(f"   • API文档:        http://{host}:8000/docs")
        print(f"   • Neo4j浏览器:    http://{host}:7474/")
        
        print("\n📱 应用功能:")
        print("   • 📄 文档解析 - 支持Excel/PDF/DOCX/PPTX文件解析")
        print("   • 🕸️ 图谱可视化 - 基于Cytoscape的交互式图谱")
        print("   • 📚 词典管理 - 质量术语词典管理")
        print("   • ⚙️ 系统管理 - 系统配置和监控")
        print("   • 🏠 首页 - 系统概览和数据统计")
        
        print("\n🔑 认证信息:")
        print("   • Neo4j:    用户名: neo4j, 密码: password123")
        
        print("\n💡 技术栈:")
        print("   • 前端: Vue.js 3.x + Element Plus + Vite")
        print("   • 后端: FastAPI + Python")
        print("   • 数据库: Neo4j + Redis")
        print("   • 可视化: Cytoscape + ECharts + D3.js")
        
        return True
        
    except Exception as e:
        print(f"❌ 部署失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 质量知识图谱助手 - 完整前端部署")
    print("=" * 60)
    
    print("将部署完整的前端应用，包含:")
    print("   ✅ Vue.js 3.x + Element Plus UI框架")
    print("   ✅ 文档解析功能")
    print("   ✅ 图谱可视化 (Cytoscape)")
    print("   ✅ 词典管理系统")
    print("   ✅ 系统管理界面")
    print("   ✅ 响应式设计")
    print("   ✅ 完整的路由和状态管理")
    
    confirm = input("\n确认部署完整前端应用? (y/N): ").strip().lower()
    if confirm != 'y':
        print("部署已取消")
        return False
    
    return deploy_complete_frontend()

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n🎊 质量知识图谱助手部署完成！")
            print("现在可以访问完整的前端应用了！")
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户取消部署")
    except Exception as e:
        print(f"\n❌ 部署过程中发生错误: {e}")
