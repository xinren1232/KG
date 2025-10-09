#!/usr/bin/env python3
"""
检查所有服务状态
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

def check_services():
    """检查所有服务"""
    
    print("🚀 开始检查所有服务...")
    
    # 创建SSH客户端
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # 连接服务器
        print(f"\n🔗 连接服务器 {SERVER_IP}...")
        ssh.connect(SERVER_IP, username=USERNAME, password=PASSWORD)
        print("✅ 连接成功！")
        
        # 1. 检查所有systemd服务
        execute_ssh_command(
            ssh,
            "systemctl list-units --type=service --state=running | grep -E 'neo4j|redis|kg-'",
            "检查运行中的服务"
        )
        
        # 2. 检查Neo4j服务
        execute_ssh_command(
            ssh,
            "systemctl status neo4j --no-pager | head -20",
            "检查Neo4j服务状态"
        )
        
        # 3. 检查Redis服务
        execute_ssh_command(
            ssh,
            "systemctl status redis --no-pager | head -20",
            "检查Redis服务状态"
        )
        
        # 4. 检查Neo4j进程
        execute_ssh_command(
            ssh,
            "ps aux | grep neo4j | grep -v grep",
            "检查Neo4j进程"
        )
        
        # 5. 检查Redis进程
        execute_ssh_command(
            ssh,
            "ps aux | grep redis | grep -v grep",
            "检查Redis进程"
        )
        
        # 6. 测试Neo4j连接
        execute_ssh_command(
            ssh,
            "cypher-shell -u neo4j -p Zxylsy.99 'MATCH (n) RETURN count(n) LIMIT 1;' 2>&1",
            "测试Neo4j连接"
        )
        
        # 7. 测试Redis连接
        execute_ssh_command(
            ssh,
            "redis-cli ping",
            "测试Redis连接"
        )
        
        # 8. 检查Neo4j端口
        execute_ssh_command(
            ssh,
            "netstat -tlnp | grep -E ':7474|:7687'",
            "检查Neo4j端口"
        )
        
        # 9. 检查Redis端口
        execute_ssh_command(
            ssh,
            "netstat -tlnp | grep :6379",
            "检查Redis端口"
        )
        
        # 10. 检查API日志中的错误
        execute_ssh_command(
            ssh,
            "journalctl -u kg-api --since '10 minutes ago' --no-pager | grep -i error | tail -20",
            "检查API错误日志（最近10分钟）"
        )
        
        # 11. 检查前端日志中的错误
        execute_ssh_command(
            ssh,
            "journalctl -u kg-frontend --since '10 minutes ago' --no-pager | grep -i error | tail -20",
            "检查前端错误日志（最近10分钟）"
        )
        
        # 12. 测试API健康检查
        execute_ssh_command(
            ssh,
            "curl -s http://localhost:8000/health | python3 -m json.tool",
            "测试API健康检查"
        )
        
        # 13. 测试API通过Nginx
        execute_ssh_command(
            ssh,
            "curl -s http://localhost/api/health | python3 -m json.tool",
            "测试API（通过Nginx）"
        )
        
    except Exception as e:
        print(f"\n❌ 错误: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        ssh.close()
        print("\n🔌 SSH连接已关闭")

if __name__ == "__main__":
    check_services()

