#!/usr/bin/env python3
"""查找项目目录"""

try:
    import paramiko
except ImportError:
    import subprocess
    subprocess.run(["pip", "install", "paramiko"], check=True)
    import paramiko

SERVER_IP = "47.108.152.16"
SERVER_USER = "root"
SERVER_PASSWORD = "Zxylsy.99"

print("连接到服务器...")
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(SERVER_IP, username=SERVER_USER, password=SERVER_PASSWORD)
print("✓ 连接成功\n")

# 查找docker-compose.prod.yml文件
print("查找docker-compose.prod.yml文件...")
stdin, stdout, stderr = client.exec_command("find / -name 'docker-compose.prod.yml' 2>/dev/null | head -10", timeout=60)
output = stdout.read().decode('utf-8')
print(output)

# 查找可能的项目目录
print("\n查找可能的项目目录...")
stdin, stdout, stderr = client.exec_command("ls -la / | grep -E 'kg|KG|project'")
output = stdout.read().decode('utf-8')
print(output)

# 查看root目录
print("\nroot用户主目录:")
stdin, stdout, stderr = client.exec_command("ls -la ~/ | head -20")
output = stdout.read().decode('utf-8')
print(output)

# 查看/opt目录
print("\n/opt目录:")
stdin, stdout, stderr = client.exec_command("ls -la /opt/ 2>/dev/null")
output = stdout.read().decode('utf-8')
print(output)

# 查看/home目录
print("\n/home目录:")
stdin, stdout, stderr = client.exec_command("ls -la /home/ 2>/dev/null")
output = stdout.read().decode('utf-8')
print(output)

# 查看docker容器
print("\nDocker容器:")
stdin, stdout, stderr = client.exec_command("docker ps -a")
output = stdout.read().decode('utf-8')
print(output)

client.close()

