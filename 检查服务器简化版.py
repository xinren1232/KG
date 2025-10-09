#!/usr/bin/env python3
"""
简化版服务器检查脚本
使用sshpass或直接SSH命令
"""

import subprocess
import json
from datetime import datetime

SERVER = "root@47.108.152.16"
PASSWORD = "Zxylsy.99"

def run_ssh(command):
    """执行SSH命令"""
    try:
        # 使用subprocess执行SSH命令
        full_cmd = f'ssh -o StrictHostKeyChecking=no {SERVER} "{command}"'
        result = subprocess.run(
            full_cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout, result.stderr
    except Exception as e:
        return "", str(e)

print("=" * 80)
print("🔍 检查阿里云服务器部署状态")
print("=" * 80)
print(f"服务器: {SERVER}")
print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# 1. 检查运行的进程
print("=" * 80)
print("1️⃣  检查运行的进程")
print("=" * 80)
stdout, stderr = run_ssh("ps aux | grep -E 'python|node|neo4j|redis|nginx|java' | grep -v grep")
if stdout:
    print(stdout)
else:
    print("❌ 无法获取进程信息")
    if stderr:
        print(f"错误: {stderr}")
print()

# 2. 检查监听的端口
print("=" * 80)
print("2️⃣  检查监听的端口")
print("=" * 80)
stdout, stderr = run_ssh("netstat -tlnp | grep -E '80|443|5173|8000|7474|7687|6379'")
if stdout:
    print(stdout)
else:
    print("❌ 无法获取端口信息")
print()

# 3. 检查项目目录
print("=" * 80)
print("3️⃣  检查项目目录")
print("=" * 80)
stdout, stderr = run_ssh("ls -la /opt/knowledge-graph/ 2>/dev/null")
if stdout:
    print(stdout)
else:
    print("❌ 目录不存在或无权限")
print()

# 4. 检查项目文件结构
print("=" * 80)
print("4️⃣  检查项目文件结构")
print("=" * 80)
stdout, stderr = run_ssh("find /opt/knowledge-graph -maxdepth 2 -type d 2>/dev/null")
if stdout:
    print("目录结构:")
    print(stdout)
else:
    print("❌ 无法获取目录结构")
print()

# 5. 检查API服务
print("=" * 80)
print("5️⃣  检查API服务")
print("=" * 80)
stdout, stderr = run_ssh("ls -la /opt/knowledge-graph/api/ 2>/dev/null | head -20")
if stdout:
    print(stdout)
else:
    print("❌ API目录不存在")
print()

# 6. 检查前端服务
print("=" * 80)
print("6️⃣  检查前端服务")
print("=" * 80)
stdout, stderr = run_ssh("ls -la /opt/knowledge-graph/apps/web/ 2>/dev/null | head -20")
if stdout:
    print(stdout)
else:
    print("❌ 前端目录不存在")
print()

# 7. 检查Nginx配置
print("=" * 80)
print("7️⃣  检查Nginx配置")
print("=" * 80)
stdout, stderr = run_ssh("cat /etc/nginx/sites-available/knowledge-graph 2>/dev/null")
if stdout:
    print(stdout)
else:
    print("❌ Nginx配置不存在")
print()

# 8. 测试HTTP端点
print("=" * 80)
print("8️⃣  测试HTTP端点")
print("=" * 80)

endpoints = [
    ("主页", "http://localhost/"),
    ("前端(5173)", "http://localhost:5173/"),
    ("API健康检查", "http://localhost:8000/health"),
    ("API文档", "http://localhost:8000/docs"),
    ("Neo4j", "http://localhost:7474/"),
]

for name, url in endpoints:
    stdout, stderr = run_ssh(f"curl -s -o /dev/null -w '%{{http_code}}' {url} 2>&1")
    status = stdout.strip()
    if status.isdigit():
        code = int(status)
        if 200 <= code < 300:
            print(f"✅ {name}: {code}")
        elif code == 502:
            print(f"❌ {name}: {code} (Bad Gateway - 后端服务未运行)")
        else:
            print(f"⚠️  {name}: {code}")
    else:
        print(f"❌ {name}: 无法连接")
print()

# 9. 检查环境变量和版本
print("=" * 80)
print("9️⃣  检查环境和软件版本")
print("=" * 80)

commands = [
    ("Python版本", "python3 --version 2>&1"),
    ("Node.js版本", "node --version 2>&1"),
    ("Neo4j状态", "systemctl status neo4j 2>&1 | head -5"),
]

for name, cmd in commands:
    stdout, stderr = run_ssh(cmd)
    if stdout:
        print(f"{name}:")
        print(f"  {stdout.strip()}")
    else:
        print(f"❌ {name}: 未安装")
print()

print("=" * 80)
print("✅ 检查完成")
print("=" * 80)

