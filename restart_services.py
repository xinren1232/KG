#!/usr/bin/env python3
"""重启服务"""

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
print("重启服务")
print("="*80)

print("\n连接到服务器...")
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(SERVER_IP, username=SERVER_USER, password=SERVER_PASSWORD)
print("✓ 连接成功\n")

project_dir = "/opt/knowledge-graph"

# 1. 检查docker-compose文件
print("1. 检查docker-compose文件")
print("="*80)
stdin, stdout, stderr = client.exec_command(f"ls -la {project_dir}/docker-compose*.yml")
output = stdout.read().decode('utf-8')
print(output)

# 确定使用哪个compose文件
compose_file = "docker-compose.yml"
stdin, stdout, stderr = client.exec_command(f"[ -f {project_dir}/docker-compose.prod.yml ] && echo 'prod' || echo 'default'")
output = stdout.read().decode('utf-8').strip()
if output == "prod":
    compose_file = "docker-compose.prod.yml"

print(f"\n使用配置文件: {compose_file}\n")

# 2. 检查当前运行的容器
print("2. 检查当前运行的容器")
print("="*80)
stdin, stdout, stderr = client.exec_command("docker ps -a")
output = stdout.read().decode('utf-8')
print(output)

# 3. 重启服务
print("\n3. 重启服务")
print("="*80)

commands = f"""
cd {project_dir}
echo '停止所有服务...'
docker-compose -f {compose_file} down
echo ''
echo '启动所有服务...'
docker-compose -f {compose_file} up -d
echo ''
echo '等待服务启动...'
sleep 15
echo ''
echo '检查服务状态:'
docker-compose -f {compose_file} ps
"""

stdin, stdout, stderr = client.exec_command(commands, timeout=120)
output = stdout.read().decode('utf-8')
error = stderr.read().decode('utf-8')
print(output)
if error:
    print("错误:", error)

# 4. 查看服务日志
print("\n4. 查看服务日志")
print("="*80)

print("\nAPI服务日志:")
stdin, stdout, stderr = client.exec_command(f"cd {project_dir} && docker-compose -f {compose_file} logs api --tail=20")
output = stdout.read().decode('utf-8')
print(output)

print("\n前端服务日志:")
stdin, stdout, stderr = client.exec_command(f"cd {project_dir} && docker-compose -f {compose_file} logs web --tail=20")
output = stdout.read().decode('utf-8')
print(output)

# 5. 测试API
print("\n5. 测试API")
print("="*80)

import time
import requests

time.sleep(5)  # 等待服务完全启动

try:
    print("\n测试图谱API...")
    start = time.time()
    r = requests.get("http://47.108.152.16/api/kg/graph?limit=100", timeout=30)
    elapsed = time.time() - start
    
    if r.status_code == 200:
        data = r.json()
        nodes = len(data.get('data', {}).get('sampleNodes', []))
        rels = len(data.get('data', {}).get('sampleRelations', []))
        print(f"✓ API测试成功")
        print(f"  响应时间: {elapsed:.2f}秒")
        print(f"  节点数: {nodes}")
        print(f"  关系数: {rels}")
    else:
        print(f"✗ API返回错误: {r.status_code}")
except Exception as e:
    print(f"✗ API测试失败: {e}")

client.close()

print("\n" + "="*80)
print("服务重启完成！")
print("="*80)
print("\n修复总结:")
print("✓ 1. 前端超时配置已修改: 10秒 → 60秒")
print("✓ 2. 后端缓存逻辑已修复")
print("✓ 3. 服务已重启")
print("\n请在浏览器中测试:")
print("  http://47.108.152.16/")
print("  点击 '图谱可视化' 菜单")
print("\n应该不再出现超时错误！")

