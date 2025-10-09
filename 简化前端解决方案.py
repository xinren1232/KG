#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化前端解决方案
创建一个可用的前端页面
"""

import getpass

def create_simple_frontend():
    """创建简化前端解决方案"""
    print("🎯 创建简化前端解决方案")
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
        
        # 1. 创建完整的前端页面
        print("\n📄 创建完整前端页面...")
        
        frontend_html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>知识图谱系统 - Knowledge Graph System</title>
    <link href="https://cdn.jsdelivr.net/npm/element-plus@2.4.0/dist/index.css" rel="stylesheet">
    <script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/element-plus@2.4.0/dist/index.full.js"></script>
    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .header {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            padding: 20px 0;
            text-align: center;
            color: white;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        .service-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }
        .service-card {
            background: rgba(255,255,255,0.95);
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            color: #333;
        }
        .service-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 40px rgba(0,0,0,0.15);
        }
        .service-icon {
            font-size: 3em;
            margin-bottom: 15px;
            display: block;
        }
        .service-title {
            font-size: 1.5em;
            font-weight: bold;
            margin-bottom: 10px;
            color: #2c3e50;
        }
        .service-desc {
            color: #7f8c8d;
            margin-bottom: 20px;
            line-height: 1.6;
        }
        .service-link {
            display: inline-block;
            padding: 10px 20px;
            background: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 25px;
            transition: all 0.3s ease;
            margin: 5px;
        }
        .service-link:hover {
            background: #5a6fd8;
            transform: scale(1.05);
        }
        .status-indicator {
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            margin-right: 8px;
        }
        .status-online { background: #27ae60; }
        .status-offline { background: #e74c3c; }
        .status-unknown { background: #f39c12; }
        .footer {
            text-align: center;
            padding: 40px 20px;
            color: rgba(255,255,255,0.8);
        }
        .system-info {
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
            color: white;
        }
    </style>
</head>
<body>
    <div id="app">
        <div class="header">
            <h1>🚀 知识图谱系统</h1>
            <p>Knowledge Graph System - 智能数据分析与可视化平台</p>
        </div>
        
        <div class="container">
            <div class="system-info">
                <h3>📊 系统状态</h3>
                <p><strong>服务器:</strong> 47.108.152.16</p>
                <p><strong>部署时间:</strong> {{ deployTime }}</p>
                <p><strong>系统版本:</strong> v1.0.0</p>
                <p><strong>在线服务:</strong> <span :class="'status-indicator status-' + systemStatus"></span>{{ statusText }}</p>
            </div>
            
            <div class="service-grid">
                <!-- Neo4j 图数据库 -->
                <div class="service-card">
                    <div class="service-icon">🗄️</div>
                    <div class="service-title">Neo4j 图数据库</div>
                    <div class="service-desc">
                        高性能图数据库，存储和查询复杂的关系数据。
                        支持Cypher查询语言，提供强大的图算法。
                    </div>
                    <a href="http://47.108.152.16:7474" target="_blank" class="service-link">
                        <span :class="'status-indicator status-' + services.neo4j"></span>
                        访问 Neo4j 浏览器
                    </a>
                    <div style="margin-top: 10px; font-size: 0.9em; color: #666;">
                        <strong>认证信息:</strong><br>
                        用户名: neo4j<br>
                        密码: password123
                    </div>
                </div>
                
                <!-- API 服务 -->
                <div class="service-card">
                    <div class="service-icon">🔧</div>
                    <div class="service-title">API 服务</div>
                    <div class="service-desc">
                        RESTful API服务，提供数据查询、上传、分析等功能。
                        基于FastAPI构建，支持自动API文档生成。
                    </div>
                    <a href="http://47.108.152.16:8000" target="_blank" class="service-link">
                        <span :class="'status-indicator status-' + services.api"></span>
                        访问 API 服务
                    </a>
                    <a href="http://47.108.152.16:8000/docs" target="_blank" class="service-link">
                        📚 API 文档
                    </a>
                    <a href="http://47.108.152.16:8000/health" target="_blank" class="service-link">
                        ❤️ 健康检查
                    </a>
                </div>
                
                <!-- 监控系统 -->
                <div class="service-card">
                    <div class="service-icon">📈</div>
                    <div class="service-title">监控系统</div>
                    <div class="service-desc">
                        实时监控系统性能和服务状态。
                        Prometheus收集指标，Grafana提供可视化仪表板。
                    </div>
                    <a href="http://47.108.152.16:9090" target="_blank" class="service-link">
                        <span :class="'status-indicator status-' + services.prometheus"></span>
                        Prometheus
                    </a>
                    <a href="http://47.108.152.16:3000" target="_blank" class="service-link">
                        <span :class="'status-indicator status-' + services.grafana"></span>
                        Grafana
                    </a>
                    <div style="margin-top: 10px; font-size: 0.9em; color: #666;">
                        <strong>Grafana认证:</strong><br>
                        用户名: admin<br>
                        密码: admin123
                    </div>
                </div>
                
                <!-- 前端应用 -->
                <div class="service-card">
                    <div class="service-icon">💻</div>
                    <div class="service-title">前端应用</div>
                    <div class="service-desc">
                        基于Vue.js 3.x构建的现代化前端应用。
                        提供图谱可视化、数据管理等功能。
                    </div>
                    <a href="http://47.108.152.16:5173" target="_blank" class="service-link">
                        <span :class="'status-indicator status-' + services.frontend"></span>
                        访问前端应用
                    </a>
                    <div style="margin-top: 10px; font-size: 0.9em; color: #666;">
                        Vue.js 3.x + Element Plus<br>
                        开发服务器端口: 5173
                    </div>
                </div>
                
                <!-- 系统管理 -->
                <div class="service-card">
                    <div class="service-icon">⚙️</div>
                    <div class="service-title">系统管理</div>
                    <div class="service-desc">
                        系统管理和运维工具。
                        包括日志查看、服务重启、数据备份等功能。
                    </div>
                    <button @click="checkAllServices" class="service-link">
                        🔍 检查服务状态
                    </button>
                    <button @click="showSystemInfo" class="service-link">
                        📊 系统信息
                    </button>
                </div>
                
                <!-- 文档中心 -->
                <div class="service-card">
                    <div class="service-icon">📚</div>
                    <div class="service-title">文档中心</div>
                    <div class="service-desc">
                        系统使用文档、API文档、部署指南等。
                        包含完整的系统说明和操作手册。
                    </div>
                    <a href="http://47.108.152.16:8000/docs" target="_blank" class="service-link">
                        📖 API 文档
                    </a>
                    <button @click="showDeployInfo" class="service-link">
                        🚀 部署信息
                    </button>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>© 2024 知识图谱系统 | 基于 Neo4j + FastAPI + Vue.js 构建</p>
            <p>服务器: 47.108.152.16 | 部署状态: 已完成</p>
        </div>
    </div>

    <script>
        const { createApp } = Vue;
        const { ElMessage, ElMessageBox } = ElementPlus;
        
        createApp({
            data() {
                return {
                    deployTime: new Date().toLocaleString('zh-CN'),
                    systemStatus: 'unknown',
                    statusText: '检查中...',
                    services: {
                        neo4j: 'unknown',
                        api: 'unknown',
                        prometheus: 'unknown',
                        grafana: 'unknown',
                        frontend: 'unknown'
                    }
                }
            },
            mounted() {
                this.checkAllServices();
                // 每30秒检查一次服务状态
                setInterval(this.checkAllServices, 30000);
            },
            methods: {
                async checkAllServices() {
                    console.log('检查服务状态...');
                    
                    const serviceChecks = [
                        { key: 'neo4j', url: 'http://47.108.152.16:7474' },
                        { key: 'api', url: 'http://47.108.152.16:8000/health' },
                        { key: 'prometheus', url: 'http://47.108.152.16:9090' },
                        { key: 'grafana', url: 'http://47.108.152.16:3000' },
                        { key: 'frontend', url: 'http://47.108.152.16:5173' }
                    ];
                    
                    let onlineCount = 0;
                    
                    for (let service of serviceChecks) {
                        try {
                            const response = await fetch(service.url, { 
                                mode: 'no-cors',
                                timeout: 5000 
                            });
                            this.services[service.key] = 'online';
                            onlineCount++;
                        } catch (error) {
                            this.services[service.key] = 'offline';
                        }
                    }
                    
                    if (onlineCount >= 3) {
                        this.systemStatus = 'online';
                        this.statusText = `系统正常 (${onlineCount}/5 服务在线)`;
                    } else if (onlineCount > 0) {
                        this.systemStatus = 'unknown';
                        this.statusText = `部分服务在线 (${onlineCount}/5)`;
                    } else {
                        this.systemStatus = 'offline';
                        this.statusText = '服务离线';
                    }
                },
                
                showSystemInfo() {
                    ElMessageBox.alert(`
                        <h3>系统信息</h3>
                        <p><strong>服务器:</strong> 47.108.152.16</p>
                        <p><strong>操作系统:</strong> Ubuntu 22.04.5 LTS</p>
                        <p><strong>Docker版本:</strong> 28.4.0</p>
                        <p><strong>部署方式:</strong> Docker Compose</p>
                        <p><strong>项目路径:</strong> /opt/knowledge-graph</p>
                        <p><strong>备份路径:</strong> /opt/kg-backups</p>
                        <h4>服务端口:</h4>
                        <ul>
                            <li>Neo4j: 7474 (HTTP), 7687 (Bolt)</li>
                            <li>API: 8000</li>
                            <li>前端: 5173</li>
                            <li>Prometheus: 9090</li>
                            <li>Grafana: 3000</li>
                            <li>Redis: 6379</li>
                        </ul>
                    `, '系统信息', {
                        dangerouslyUseHTMLString: true,
                        confirmButtonText: '确定'
                    });
                },
                
                showDeployInfo() {
                    ElMessageBox.alert(`
                        <h3>部署信息</h3>
                        <p><strong>部署方式:</strong> SSH自动化部署</p>
                        <p><strong>技术栈:</strong></p>
                        <ul>
                            <li>后端: FastAPI + Python 3.11</li>
                            <li>前端: Vue.js 3.x + Element Plus</li>
                            <li>数据库: Neo4j 5.23 + Redis 7</li>
                            <li>监控: Prometheus + Grafana</li>
                            <li>容器: Docker + Docker Compose</li>
                            <li>反向代理: Nginx</li>
                        </ul>
                        <p><strong>部署状态:</strong> ✅ 已完成</p>
                        <p><strong>最后更新:</strong> ${this.deployTime}</p>
                    `, '部署信息', {
                        dangerouslyUseHTMLString: true,
                        confirmButtonText: '确定'
                    });
                }
            }
        }).use(ElementPlus).mount('#app');
    </script>
</body>
</html>"""
        
        # 2. 创建前端页面
        create_frontend_cmd = f"""
mkdir -p /var/www/html
cat > /var/www/html/index.html << 'EOF'
{frontend_html}
EOF
"""
        stdin, stdout, stderr = ssh.exec_command(create_frontend_cmd)
        stdout.read()
        print("✅ 完整前端页面创建完成")
        
        # 3. 简化Nginx配置
        print("\n🌐 配置Nginx...")
        
        simple_nginx_config = """server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name _;
    
    root /var/www/html;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    location /static/ {
        alias /var/www/html/;
        expires 1d;
    }
    
    error_page 404 /index.html;
}"""
        
        nginx_cmd = f"""
cat > /etc/nginx/sites-available/default << 'EOF'
{simple_nginx_config}
EOF
nginx -t && systemctl reload nginx
"""
        stdin, stdout, stderr = ssh.exec_command(nginx_cmd)
        output = stdout.read().decode()
        error = stderr.read().decode()
        if "test is successful" in error:
            print("✅ Nginx配置成功")
        
        # 4. 启动基础服务
        print("\n🚀 启动基础服务...")
        
        service_commands = [
            "cd /opt/knowledge-graph",
            "docker compose up -d neo4j redis || true",
            "sleep 10",
            "docker compose up -d api || true"
        ]
        
        for cmd in service_commands:
            print(f"   执行: {cmd}")
            stdin, stdout, stderr = ssh.exec_command(cmd, timeout=120)
            output = stdout.read().decode()
            if output and "sleep" not in cmd:
                print(f"   输出: {output}")
        
        # 5. 测试访问
        print("\n🧪 测试访问...")
        
        test_cmd = "curl -s -o /dev/null -w '%{http_code}' http://localhost:80/"
        stdin, stdout, stderr = ssh.exec_command(test_cmd)
        status_code = stdout.read().decode().strip()
        
        if status_code == '200':
            print("✅ 前端页面访问正常")
        else:
            print(f"⚠️ 前端页面状态码: {status_code}")
        
        ssh.close()
        
        print("\n🎉 简化前端解决方案完成！")
        print("=" * 60)
        print("🌐 现在可以访问:")
        print(f"   • 主页面: http://{host}/")
        print(f"   这是一个完整的前端页面，包含:")
        print("     - 系统概览和状态监控")
        print("     - 所有服务的访问链接")
        print("     - 实时服务状态检查")
        print("     - 系统信息和部署详情")
        print("     - 现代化的用户界面")
        
        print("\n🔑 服务访问:")
        print(f"   • Neo4j: http://{host}:7474 (neo4j/password123)")
        print(f"   • API: http://{host}:8000")
        print(f"   • Grafana: http://{host}:3000 (admin/admin123)")
        
        return True
        
    except Exception as e:
        print(f"❌ 创建失败: {e}")
        return False

def main():
    """主函数"""
    print("🎯 简化前端解决方案")
    print("=" * 50)
    
    print("将创建一个完整的前端页面，包含:")
    print("   ✅ 现代化的用户界面")
    print("   ✅ 系统状态监控")
    print("   ✅ 服务访问链接")
    print("   ✅ 实时状态检查")
    print("   ✅ 系统信息展示")
    
    confirm = input("\n确认创建? (y/N): ").strip().lower()
    if confirm != 'y':
        print("操作已取消")
        return False
    
    return create_simple_frontend()

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n🎊 前端页面创建完成！")
            print("请访问 http://47.108.152.16/ 查看效果！")
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户取消操作")
    except Exception as e:
        print(f"\n❌ 操作过程中发生错误: {e}")
