#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终诊断
"""

import paramiko
import hashlib

SERVER_HOST = "47.108.152.16"
SERVER_USER = "root"
SERVER_PASSWORD = "Zxylsy.99"

def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(SERVER_HOST, username=SERVER_USER, password=SERVER_PASSWORD, timeout=30)
    
    print("=" * 80)
    print("最终诊断")
    print("=" * 80)
    
    # 1. 检查本地文件
    print("\n1. 本地文件信息:")
    with open('api/main.py', 'rb') as f:
        local_content = f.read()
        local_md5 = hashlib.md5(local_content).hexdigest()
        local_lines = local_content.decode('utf-8').count('\n')
        print(f"   行数: {local_lines}")
        print(f"   MD5: {local_md5}")
        print(f"   大小: {len(local_content)} 字节")
    
    # 2. 检查服务器文件
    print("\n2. 服务器文件信息:")
    stdin, stdout, stderr = ssh.exec_command('wc -l /opt/knowledge-graph/api/main.py')
    server_lines = stdout.read().decode('utf-8').strip()
    print(f"   行数: {server_lines}")
    
    stdin, stdout, stderr = ssh.exec_command('md5sum /opt/knowledge-graph/api/main.py')
    server_md5 = stdout.read().decode('utf-8').split()[0]
    print(f"   MD5: {server_md5}")
    
    stdin, stdout, stderr = ssh.exec_command('stat -c%s /opt/knowledge-graph/api/main.py')
    server_size = stdout.read().decode('utf-8').strip()
    print(f"   大小: {server_size} 字节")
    
    # 3. 比较
    print("\n3. 比较结果:")
    if local_md5 == server_md5:
        print("   ✅ 文件完全一致")
    else:
        print("   ❌ 文件不一致！需要重新上传")
    
    # 4. 检查新路由
    print("\n4. 检查新路由定义:")
    stdin, stdout, stderr = ssh.exec_command('grep -n "@app.post.*kg/relations/validate" /opt/knowledge-graph/api/main.py')
    output = stdout.read().decode('utf-8').strip()
    if output:
        print(f"   ✅ 找到: {output}")
    else:
        print("   ❌ 未找到 @app.post.*kg/relations/validate")
    
    # 5. 检查导入
    print("\n5. 检查导入语句:")
    stdin, stdout, stderr = ssh.exec_command('grep -n "from models.relation_models" /opt/knowledge-graph/api/main.py')
    output = stdout.read().decode('utf-8').strip()
    if output:
        print(f"   ✅ 找到: {output}")
    else:
        print("   ❌ 未找到导入语句")
    
    # 6. 统计所有@app装饰器
    print("\n6. 统计所有路由:")
    stdin, stdout, stderr = ssh.exec_command('grep -c "^@app\\." /opt/knowledge-graph/api/main.py')
    count = stdout.read().decode('utf-8').strip()
    print(f"   总共 {count} 个@app装饰器")
    
    # 7. 列出所有新路由
    print("\n7. 列出新路由:")
    new_routes = [
        '/kg/relations/validate',
        '/kg/relations/import',
        '/kg/relations/stats',
        '/kg/diagnose',
        '/kg/prevent',
        '/kg/test-path',
        '/kg/dependencies'
    ]
    
    for route in new_routes:
        stdin, stdout, stderr = ssh.exec_command(f'grep -c "{route}" /opt/knowledge-graph/api/main.py')
        count = stdout.read().decode('utf-8').strip()
        status = "✅" if int(count) > 0 else "❌"
        print(f"   {status} {route}: {count} 次")
    
    print("\n" + "=" * 80)
    
    ssh.close()

if __name__ == "__main__":
    main()

