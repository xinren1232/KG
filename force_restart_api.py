#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
强制重启API服务
"""

import paramiko
import time

SERVER_HOST = "47.108.152.16"
SERVER_USER = "root"
SERVER_PASSWORD = "Zxylsy.99"

def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(SERVER_HOST, username=SERVER_USER, password=SERVER_PASSWORD, timeout=30)
    
    print("=" * 80)
    print("强制重启API服务")
    print("=" * 80)
    
    print("\n1. 杀死所有Python进程...")
    stdin, stdout, stderr = ssh.exec_command('killall -9 python3 2>/dev/null || true')
    time.sleep(2)
    
    print("\n2. 清除所有Python缓存...")
    stdin, stdout, stderr = ssh.exec_command('find /opt/knowledge-graph/api -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true')
    stdin, stdout, stderr = ssh.exec_command('find /opt/knowledge-graph/api -type f -name "*.pyc" -delete 2>/dev/null || true')
    time.sleep(1)
    
    print("\n3. 验证文件...")
    stdin, stdout, stderr = ssh.exec_command('grep -c "/kg/relations/validate" /opt/knowledge-graph/api/main.py')
    count = stdout.read().decode('utf-8').strip()
    print(f"   main.py包含 /kg/relations/validate: {count} 次")
    
    print("\n4. 清空日志...")
    stdin, stdout, stderr = ssh.exec_command('echo "" > /tmp/kg-api.log')
    
    print("\n5. 启动新进程...")
    stdin, stdout, stderr = ssh.exec_command('cd /opt/knowledge-graph/api && nohup python3 -u main.py > /tmp/kg-api.log 2>&1 &')
    print("   等待10秒...")
    time.sleep(10)
    
    print("\n6. 检查进程...")
    stdin, stdout, stderr = ssh.exec_command('ps aux | grep "python3.*main.py" | grep -v grep')
    output = stdout.read().decode('utf-8')
    if output:
        print("   ✅ 进程已启动:")
        print("   " + output.replace('\n', '\n   '))
    else:
        print("   ❌ 进程未启动")
    
    print("\n7. 检查日志...")
    stdin, stdout, stderr = ssh.exec_command('tail -30 /tmp/kg-api.log')
    output = stdout.read().decode('utf-8')
    print(output)
    
    print("\n8. 测试API...")
    stdin, stdout, stderr = ssh.exec_command('curl -s http://localhost:8000/')
    output = stdout.read().decode('utf-8')
    print(f"   根路径: {output}")
    
    print("\n9. 测试新端点...")
    stdin, stdout, stderr = ssh.exec_command('curl -s http://localhost:8000/kg/relations/stats')
    output = stdout.read().decode('utf-8')
    print(f"   /kg/relations/stats: {output[:200]}")
    
    print("\n10. 获取OpenAPI规范...")
    stdin, stdout, stderr = ssh.exec_command('curl -s http://localhost:8000/openapi.json | python3 -c "import sys, json; data=json.load(sys.stdin); paths=[p for p in data.get(\'paths\', {}).keys() if \'relations\' in p or \'diagnose\' in p]; print(\'\\n\'.join(paths) if paths else \'未找到新端点\')"')
    output = stdout.read().decode('utf-8')
    print(f"   新端点:\n{output}")
    
    print("\n" + "=" * 80)
    print("✅ 重启完成")
    print("=" * 80)
    
    ssh.close()

if __name__ == "__main__":
    main()

