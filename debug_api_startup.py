#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试API启动
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
    
    print("杀死所有Python进程...")
    stdin, stdout, stderr = ssh.exec_command('pkill -9 python3')
    time.sleep(2)
    
    print("清空日志...")
    stdin, stdout, stderr = ssh.exec_command('echo "" > /tmp/kg-api.log')
    
    print("启动API服务...")
    stdin, stdout, stderr = ssh.exec_command('cd /opt/knowledge-graph/api && python3 main.py > /tmp/kg-api.log 2>&1 &')
    time.sleep(10)
    
    print("\n检查完整日志...")
    stdin, stdout, stderr = ssh.exec_command('cat /tmp/kg-api.log')
    output = stdout.read().decode('utf-8')
    print(output)
    
    print("\n检查进程...")
    stdin, stdout, stderr = ssh.exec_command('ps aux | grep python3 | grep -v grep')
    output = stdout.read().decode('utf-8')
    print(output if output else "没有Python进程")
    
    ssh.close()

if __name__ == "__main__":
    main()

