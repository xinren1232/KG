#!/usr/bin/env python3
"""
检查系统日志问题
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

def check_logs():
    """检查系统日志"""
    
    print("🚀 开始检查系统日志...")
    
    # 创建SSH客户端
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # 连接服务器
        print(f"\n🔗 连接服务器 {SERVER_IP}...")
        ssh.connect(SERVER_IP, username=USERNAME, password=PASSWORD)
        print("✅ 连接成功！")
        
        # 1. 检查API服务日志
        execute_ssh_command(
            ssh,
            "journalctl -u kg-api -n 50 --no-pager",
            "检查API服务日志（最近50条）"
        )
        
        # 2. 检查前端服务日志
        execute_ssh_command(
            ssh,
            "journalctl -u kg-frontend -n 30 --no-pager",
            "检查前端服务日志（最近30条）"
        )
        
        # 3. 检查Nginx错误日志
        execute_ssh_command(
            ssh,
            "tail -50 /var/log/nginx/error.log",
            "检查Nginx错误日志"
        )
        
        # 4. 检查API进程
        execute_ssh_command(
            ssh,
            "ps aux | grep -E 'python3.*main.py|uvicorn' | grep -v grep",
            "检查API进程"
        )
        
        # 5. 检查端口占用
        execute_ssh_command(
            ssh,
            "netstat -tlnp | grep -E ':8000|:5173'",
            "检查端口占用"
        )
        
        # 6. 检查磁盘空间
        execute_ssh_command(
            ssh,
            "df -h",
            "检查磁盘空间"
        )
        
        # 7. 检查内存使用
        execute_ssh_command(
            ssh,
            "free -h",
            "检查内存使用"
        )
        
        # 8. 检查系统负载
        execute_ssh_command(
            ssh,
            "uptime",
            "检查系统负载"
        )
        
        # 9. 检查Neo4j连接
        execute_ssh_command(
            ssh,
            "docker exec neo4j cypher-shell -u neo4j -p Zxylsy.99 'MATCH (n) RETURN count(n) LIMIT 1;' 2>&1",
            "检查Neo4j连接"
        )
        
        # 10. 检查Redis连接
        execute_ssh_command(
            ssh,
            "docker exec redis redis-cli ping",
            "检查Redis连接"
        )
        
    except Exception as e:
        print(f"\n❌ 错误: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        ssh.close()
        print("\n🔌 SSH连接已关闭")

if __name__ == "__main__":
    check_logs()

