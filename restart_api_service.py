#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重启API服务
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

    print("检查API进程...")
    stdin, stdout, stderr = ssh.exec_command('ps aux | grep main.py | grep -v grep')
    output = stdout.read().decode('utf-8')
    if output:
        print(output)
    else:
        print("没有运行的进程")

    print("\n清除Python缓存...")
    stdin, stdout, stderr = ssh.exec_command('find /opt/knowledge-graph/api -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true')
    time.sleep(1)

    print("\n杀死旧进程...")
    stdin, stdout, stderr = ssh.exec_command('pkill -9 -f python3')
    time.sleep(2)

    print("\n启动新进程...")
    stdin, stdout, stderr = ssh.exec_command('cd /opt/knowledge-graph/api && nohup python3 -u main.py > /tmp/kg-api.log 2>&1 &')
    time.sleep(5)
    
    print("\n检查新进程...")
    stdin, stdout, stderr = ssh.exec_command('ps aux | grep main.py | grep -v grep')
    output = stdout.read().decode('utf-8')
    if output:
        print("✅ 进程已启动:")
        print(output)
    else:
        print("❌ 进程未启动")
    
    print("\n检查日志...")
    stdin, stdout, stderr = ssh.exec_command('tail -30 /tmp/kg-api.log')
    print(stdout.read().decode('utf-8'))
    
    print("\n测试API...")
    stdin, stdout, stderr = ssh.exec_command('curl -s http://localhost:8000/')
    print(stdout.read().decode('utf-8'))
    
    ssh.close()

if __name__ == "__main__":
    main()

