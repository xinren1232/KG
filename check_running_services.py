#!/usr/bin/env python3
"""检查正在运行的服务"""

try:
    import paramiko
except ImportError:
    import subprocess
    subprocess.run(["pip", "install", "paramiko"], check=True)
    import paramiko

SERVER_IP = "47.108.152.16"
SERVER_USER = "root"
SERVER_PASSWORD = "Zxylsy.99"

print("="*80)
print("检查正在运行的服务")
print("="*80)

print("\n连接到服务器...")
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(SERVER_IP, username=SERVER_USER, password=SERVER_PASSWORD)
print("✓ 连接成功\n")

# 1. 检查Python进程
print("1. 检查Python进程")
print("="*80)
stdin, stdout, stderr = client.exec_command("ps aux | grep python | grep -v grep")
output = stdout.read().decode('utf-8')
print(output)

# 2. 检查Node进程
print("\n2. 检查Node/Vite进程")
print("="*80)
stdin, stdout, stderr = client.exec_command("ps aux | grep -E 'node|vite' | grep -v grep")
output = stdout.read().decode('utf-8')
print(output)

# 3. 检查Nginx进程
print("\n3. 检查Nginx进程")
print("="*80)
stdin, stdout, stderr = client.exec_command("ps aux | grep nginx | grep -v grep")
output = stdout.read().decode('utf-8')
print(output)

# 4. 检查监听的端口
print("\n4. 检查监听的端口")
print("="*80)
stdin, stdout, stderr = client.exec_command("netstat -tlnp | grep -E '80|8000|3000|5173'")
output = stdout.read().decode('utf-8')
print(output)

# 5. 检查systemd服务
print("\n5. 检查systemd服务")
print("="*80)
stdin, stdout, stderr = client.exec_command("systemctl list-units --type=service | grep -E 'kg|knowledge'")
output = stdout.read().decode('utf-8')
print(output)

# 6. 查找服务配置文件
print("\n6. 查找systemd服务配置")
print("="*80)
stdin, stdout, stderr = client.exec_command("ls -la /etc/systemd/system/ | grep -E 'kg|knowledge'")
output = stdout.read().decode('utf-8')
print(output)

# 7. 检查服务状态
print("\n7. 检查服务状态")
print("="*80)

services = ["kg-api", "kg-web", "kg-frontend", "knowledge-graph-api", "knowledge-graph-web"]
for service in services:
    stdin, stdout, stderr = client.exec_command(f"systemctl status {service} 2>&1 | head -10")
    output = stdout.read().decode('utf-8')
    if "could not be found" not in output and "not found" not in output.lower():
        print(f"\n服务: {service}")
        print(output)

client.close()

print("\n" + "="*80)
print("检查完成")
print("="*80)

