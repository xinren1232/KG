#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证服务器文件
"""

import paramiko

SERVER_HOST = "47.108.152.16"
SERVER_USER = "root"
SERVER_PASSWORD = "Zxylsy.99"

def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(SERVER_HOST, username=SERVER_USER, password=SERVER_PASSWORD, timeout=30)
    
    print("检查main.py文件内容（搜索新端点）...")
    stdin, stdout, stderr = ssh.exec_command('grep -n "kg/relations/validate" /opt/knowledge-graph/api/main.py')
    output = stdout.read().decode('utf-8')
    if output:
        print(f'✅ 找到: {output}')
    else:
        print('❌ 未找到 /kg/relations/validate')
    
    print("\n检查main.py文件行数...")
    stdin, stdout, stderr = ssh.exec_command('wc -l /opt/knowledge-graph/api/main.py')
    print(stdout.read().decode('utf-8'))
    
    print("检查main.py最后修改时间...")
    stdin, stdout, stderr = ssh.exec_command('stat /opt/knowledge-graph/api/main.py | grep Modify')
    print(stdout.read().decode('utf-8'))
    
    print("\n检查是否有多个main.py文件...")
    stdin, stdout, stderr = ssh.exec_command('find /opt/knowledge-graph -name main.py -type f')
    output = stdout.read().decode('utf-8')
    print(output)
    
    print("\n检查Python进程的工作目录...")
    stdin, stdout, stderr = ssh.exec_command('ps aux | grep "python3 main.py" | grep -v grep')
    output = stdout.read().decode('utf-8')
    print(output)
    
    ssh.close()

if __name__ == "__main__":
    main()

