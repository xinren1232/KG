#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
在服务器上测试API
"""

import paramiko

SERVER_HOST = "47.108.152.16"
SERVER_USER = "root"
SERVER_PASSWORD = "Zxylsy.99"

def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(SERVER_HOST, username=SERVER_USER, password=SERVER_PASSWORD, timeout=30)
    
    print("测试关系统计API...")
    stdin, stdout, stderr = ssh.exec_command('curl -s http://localhost:8000/kg/relations/stats')
    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')
    print(f"输出: {output}")
    if error:
        print(f"错误: {error}")
    
    print("\n测试诊断API...")
    stdin, stdout, stderr = ssh.exec_command('curl -s "http://localhost:8000/kg/diagnose?symptom=电池盖裂纹"')
    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')
    print(f"输出: {output}")
    if error:
        print(f"错误: {error}")
    
    print("\n检查API日志...")
    stdin, stdout, stderr = ssh.exec_command('tail -100 /tmp/kg-api.log')
    output = stdout.read().decode('utf-8')
    print(output)
    
    ssh.close()

if __name__ == "__main__":
    main()

