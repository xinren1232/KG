#!/usr/bin/env python3
"""
检查Docker容器状态
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

def check_containers():
    """检查Docker容器"""
    
    print("🚀 开始检查Docker容器...")
    
    # 创建SSH客户端
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # 连接服务器
        print(f"\n🔗 连接服务器 {SERVER_IP}...")
        ssh.connect(SERVER_IP, username=USERNAME, password=PASSWORD)
        print("✅ 连接成功！")
        
        # 1. 列出所有容器
        execute_ssh_command(
            ssh,
            "docker ps -a",
            "列出所有Docker容器"
        )
        
        # 2. 检查Neo4j容器
        output, _ = execute_ssh_command(
            ssh,
            "docker ps | grep neo4j",
            "查找Neo4j容器"
        )
        
        if output:
            # 提取容器名称
            container_name = output.split()[-1] if output else None
            if container_name:
                print(f"\n✅ 找到Neo4j容器: {container_name}")
                
                # 测试连接
                execute_ssh_command(
                    ssh,
                    f"docker exec {container_name} cypher-shell -u neo4j -p Zxylsy.99 'MATCH (n) RETURN count(n) LIMIT 1;' 2>&1",
                    f"测试Neo4j连接（容器: {container_name}）"
                )
        
        # 3. 检查Redis容器
        output, _ = execute_ssh_command(
            ssh,
            "docker ps | grep redis",
            "查找Redis容器"
        )
        
        if output:
            # 提取容器名称
            container_name = output.split()[-1] if output else None
            if container_name:
                print(f"\n✅ 找到Redis容器: {container_name}")
                
                # 测试连接
                execute_ssh_command(
                    ssh,
                    f"docker exec {container_name} redis-cli ping",
                    f"测试Redis连接（容器: {container_name}）"
                )
        
        # 4. 检查Docker网络
        execute_ssh_command(
            ssh,
            "docker network ls",
            "列出Docker网络"
        )
        
        # 5. 检查Docker卷
        execute_ssh_command(
            ssh,
            "docker volume ls",
            "列出Docker卷"
        )
        
    except Exception as e:
        print(f"\n❌ 错误: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        ssh.close()
        print("\n🔌 SSH连接已关闭")

if __name__ == "__main__":
    check_containers()

