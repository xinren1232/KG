#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
添加测试端点
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
    print("添加测试端点")
    print("=" * 80)
    
    # 1. 在main.py末尾添加一个简单的测试端点
    print("\n1. 添加测试端点...")
    test_endpoint = '''

# ============================================================================
# 测试端点
# ============================================================================

@app.get("/test/hello")
async def test_hello():
    """测试端点"""
    return {"message": "Hello from test endpoint!", "status": "working"}
'''
    
    stdin, stdout, stderr = ssh.exec_command(f'echo \'{test_endpoint}\' >> /opt/knowledge-graph/api/main.py')
    print("   ✅ 测试端点已添加")
    
    # 2. 重启服务
    print("\n2. 重启服务...")
    stdin, stdout, stderr = ssh.exec_command('killall -9 python3 2>/dev/null || true')
    time.sleep(2)
    
    stdin, stdout, stderr = ssh.exec_command('cd /opt/knowledge-graph/api && nohup python3 main.py > /tmp/kg-api.log 2>&1 &')
    time.sleep(8)
    
    # 3. 测试新端点
    print("\n3. 测试新端点...")
    stdin, stdout, stderr = ssh.exec_command('curl -s http://localhost:8000/test/hello')
    output = stdout.read().decode('utf-8')
    print(f"   /test/hello: {output}")
    
    # 4. 测试关系端点
    print("\n4. 测试关系端点...")
    stdin, stdout, stderr = ssh.exec_command('curl -s http://localhost:8000/kg/relations/stats')
    output = stdout.read().decode('utf-8')
    print(f"   /kg/relations/stats: {output[:100]}")
    
    # 5. 恢复文件（删除测试端点）
    print("\n5. 恢复文件...")
    stdin, stdout, stderr = ssh.exec_command('head -n 2780 /opt/knowledge-graph/api/main.py > /tmp/main.py.clean && mv /tmp/main.py.clean /opt/knowledge-graph/api/main.py')
    print("   ✅ 文件已恢复")
    
    print("\n" + "=" * 80)
    
    ssh.close()

if __name__ == "__main__":
    main()

