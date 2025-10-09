#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完全重启
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
    print("完全重启API服务")
    print("=" * 80)
    
    # 1. 检查所有Python进程
    print("\n1. 检查所有Python进程...")
    stdin, stdout, stderr = ssh.exec_command('ps aux | grep python | grep -v grep')
    output = stdout.read().decode('utf-8')
    if output:
        print(output)
    else:
        print("   没有Python进程")
    
    # 2. 杀死所有Python进程
    print("\n2. 杀死所有Python进程...")
    stdin, stdout, stderr = ssh.exec_command('killall -9 python python3 2>/dev/null || true')
    time.sleep(3)
    
    # 3. 检查端口占用
    print("\n3. 检查端口8000占用...")
    stdin, stdout, stderr = ssh.exec_command('lsof -i:8000 || echo "端口8000未被占用"')
    output = stdout.read().decode('utf-8')
    print(output)
    
    # 4. 清除所有缓存
    print("\n4. 清除所有缓存...")
    stdin, stdout, stderr = ssh.exec_command('find /opt/knowledge-graph -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true')
    stdin, stdout, stderr = ssh.exec_command('find /opt/knowledge-graph -type f -name "*.pyc" -delete 2>/dev/null || true')
    stdin, stdout, stderr = ssh.exec_command('find /root/.cache/Python* -type f -delete 2>/dev/null || true')
    print("   ✅ 缓存已清除")
    
    # 5. 验证文件
    print("\n5. 验证main.py...")
    stdin, stdout, stderr = ssh.exec_command('grep -c "/kg/relations/validate" /opt/knowledge-graph/api/main.py')
    count = stdout.read().decode('utf-8').strip()
    print(f"   包含 /kg/relations/validate: {count} 次")
    
    # 6. 使用uvicorn直接启动（而不是让main.py自己启动）
    print("\n6. 使用uvicorn启动...")
    stdin, stdout, stderr = ssh.exec_command('cd /opt/knowledge-graph/api && nohup uvicorn main:app --host 0.0.0.0 --port 8000 --reload > /tmp/kg-api-uvicorn.log 2>&1 &')
    print("   等待10秒...")
    time.sleep(10)
    
    # 7. 检查进程
    print("\n7. 检查进程...")
    stdin, stdout, stderr = ssh.exec_command('ps aux | grep uvicorn | grep -v grep')
    output = stdout.read().decode('utf-8')
    if output:
        print("   ✅ uvicorn进程已启动:")
        print("   " + output.replace('\n', '\n   '))
    else:
        print("   ❌ uvicorn进程未启动")
    
    # 8. 检查日志
    print("\n8. 检查日志...")
    stdin, stdout, stderr = ssh.exec_command('tail -50 /tmp/kg-api-uvicorn.log')
    output = stdout.read().decode('utf-8')
    print(output)
    
    # 9. 测试API
    print("\n9. 测试API...")
    stdin, stdout, stderr = ssh.exec_command('curl -s http://localhost:8000/')
    output = stdout.read().decode('utf-8')
    print(f"   根路径: {output}")
    
    # 10. 测试新端点
    print("\n10. 测试新端点...")
    stdin, stdout, stderr = ssh.exec_command('curl -s http://localhost:8000/kg/relations/stats')
    output = stdout.read().decode('utf-8')
    print(f"   /kg/relations/stats: {output[:200]}")
    
    # 11. 获取所有端点
    print("\n11. 获取所有端点...")
    stdin, stdout, stderr = ssh.exec_command('curl -s http://localhost:8000/openapi.json | python3 -c "import sys, json; data=json.load(sys.stdin); paths=[p for p in sorted(data.get(\'paths\', {}).keys()) if \'relations\' in p or \'diagnose\' in p or \'prevent\' in p]; print(\'\\n\'.join(paths) if paths else \'未找到新端点\')"')
    output = stdout.read().decode('utf-8')
    print(f"   新端点:\n{output}")
    
    print("\n" + "=" * 80)
    print("✅ 重启完成")
    print("=" * 80)
    
    ssh.close()

if __name__ == "__main__":
    main()

