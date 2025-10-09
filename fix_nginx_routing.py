#!/usr/bin/env python3
"""
修复Nginx路由配置，确保API请求正确转发
"""

import paramiko

# 服务器配置
SERVER_IP = "47.108.152.16"
USERNAME = "root"
PASSWORD = "Zxylsy.99"

def execute_ssh_command(ssh, command, description=""):
    """执行SSH命令并返回结果"""
    if description:
        print(f"\n{'='*60}")
        print(f"📌 {description}")
        print(f"{'='*60}")
    
    print(f"💻 执行命令: {command}")
    stdin, stdout, stderr = ssh.exec_command(command)
    
    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')
    
    if output:
        print(f"✅ 输出:\n{output}")
    if error and "warning" not in error.lower():
        print(f"⚠️ 错误:\n{error}")
    
    return output, error

def fix_nginx_routing():
    """修复Nginx路由配置"""
    
    print("🚀 开始修复Nginx路由配置...")
    
    # 创建SSH客户端
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # 连接服务器
        print(f"\n🔗 连接服务器 {SERVER_IP}...")
        ssh.connect(SERVER_IP, username=USERNAME, password=PASSWORD)
        print("✅ 连接成功！")
        
        # 1. 查看当前Nginx配置
        execute_ssh_command(
            ssh,
            "cat /etc/nginx/sites-available/knowledge-graph",
            "查看当前Nginx配置"
        )
        
        # 2. 备份当前配置
        execute_ssh_command(
            ssh,
            "cp /etc/nginx/sites-available/knowledge-graph /etc/nginx/sites-available/knowledge-graph.backup.$(date +%Y%m%d_%H%M%S)",
            "备份Nginx配置"
        )
        
        # 3. 创建新的Nginx配置
        nginx_config = '''server {
    listen 80;
    server_name _;

    # API路由 - 优先匹配
    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        proxy_read_timeout 60s;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
    }

    # 前端路由
    location / {
        proxy_pass http://localhost:5173;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
'''
        
        # 4. 写入新配置
        execute_ssh_command(
            ssh,
            f"cat > /etc/nginx/sites-available/knowledge-graph << 'NGINX_EOF'\n{nginx_config}\nNGINX_EOF",
            "写入新的Nginx配置"
        )
        
        # 5. 测试Nginx配置
        execute_ssh_command(
            ssh,
            "nginx -t",
            "测试Nginx配置"
        )
        
        # 6. 重新加载Nginx
        execute_ssh_command(
            ssh,
            "systemctl reload nginx",
            "重新加载Nginx"
        )
        
        # 7. 检查Nginx状态
        execute_ssh_command(
            ssh,
            "systemctl status nginx --no-pager | head -15",
            "检查Nginx状态"
        )
        
        # 8. 测试API端点
        import time
        print("\n⏳ 等待Nginx重新加载...")
        time.sleep(2)
        
        test_commands = [
            ("curl -s http://localhost/api/health | python3 -m json.tool", "测试健康检查"),
            ("curl -s http://localhost/api/kg/dictionary/stats | python3 -m json.tool", "测试词典统计"),
            ("curl -s http://localhost/api/kg/entities | python3 -m json.tool | head -20", "测试实体统计"),
        ]
        
        for cmd, desc in test_commands:
            execute_ssh_command(ssh, cmd, desc)
            time.sleep(1)
        
        print("\n" + "="*60)
        print("🎉 Nginx路由配置修复完成！")
        print("="*60)
        print("\n📋 路由规则:")
        print("  ✅ /api/* → http://localhost:8000/")
        print("  ✅ /* → http://localhost:5173/ (前端)")
        print("\n🌐 访问地址:")
        print(f"  http://{SERVER_IP}/api/kg/dictionary/stats")
        print(f"  http://{SERVER_IP}/api/kg/entities")
        print(f"  http://{SERVER_IP}/api/kg/relations")
        print("\n💡 提示:")
        print("  - 前端需要更新API基础URL为 /api")
        print("  - 所有API请求需要加上 /api 前缀")
        
    except Exception as e:
        print(f"\n❌ 错误: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        ssh.close()
        print("\n🔌 SSH连接已关闭")

if __name__ == "__main__":
    fix_nginx_routing()

