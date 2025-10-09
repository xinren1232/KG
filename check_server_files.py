#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查服务器文件
"""

import paramiko

SERVER_HOST = "47.108.152.16"
SERVER_USER = "root"
SERVER_PASSWORD = "Zxylsy.99"

def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(SERVER_HOST, username=SERVER_USER, password=SERVER_PASSWORD, timeout=30)
    
    print("检查main.py文件...")
    stdin, stdout, stderr = ssh.exec_command('ls -lh /opt/knowledge-graph/api/main.py')
    print(stdout.read().decode('utf-8'))
    
    print("\n检查文件行数...")
    stdin, stdout, stderr = ssh.exec_command('wc -l /opt/knowledge-graph/api/main.py')
    print(stdout.read().decode('utf-8'))
    
    print("\n检查文件末尾...")
    stdin, stdout, stderr = ssh.exec_command('tail -100 /opt/knowledge-graph/api/main.py')
    output = stdout.read().decode('utf-8')
    print(output[-2000:])  # 只显示最后2000个字符
    
    print("\n检查导入语句...")
    stdin, stdout, stderr = ssh.exec_command('head -30 /opt/knowledge-graph/api/main.py')
    print(stdout.read().decode('utf-8'))
    
    print("\n检查models和services目录...")
    stdin, stdout, stderr = ssh.exec_command('ls -la /opt/knowledge-graph/api/models/')
    print("models目录:")
    print(stdout.read().decode('utf-8'))
    
    stdin, stdout, stderr = ssh.exec_command('ls -la /opt/knowledge-graph/api/services/')
    print("\nservices目录:")
    print(stdout.read().decode('utf-8'))
    
    ssh.close()

if __name__ == "__main__":
    main()

