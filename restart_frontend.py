#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重启前端服务
"""

import paramiko

SERVER_HOST = "47.108.152.16"
SERVER_USER = "root"
SERVER_PASSWORD = "Zxylsy.99"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    print("连接服务器...")
    ssh.connect(hostname=SERVER_HOST, username=SERVER_USER, password=SERVER_PASSWORD, timeout=30)
    print("✅ 连接成功\n")
    
    # 检查Docker容器
    print("检查Docker容器状态...")
    stdin, stdout, stderr = ssh.exec_command("docker ps")
    for line in stdout:
        print(line.strip())
    
    # 重启nginx容器
    print("\n重启nginx容器...")
    stdin, stdout, stderr = ssh.exec_command("cd /opt/knowledge-graph && docker-compose restart nginx")
    for line in stdout:
        print(line.strip())
    
    error = stderr.read().decode('utf-8')
    if error:
        print(f"错误: {error}")
    
    # 检查重启后的状态
    print("\n检查重启后的容器状态...")
    stdin, stdout, stderr = ssh.exec_command("docker ps | grep nginx")
    for line in stdout:
        print(line.strip())
    
    print("\n✅ 前端服务已重启")
    print("请访问 http://47.108.152.16 查看首页数据")
    
except Exception as e:
    print(f"❌ 错误: {str(e)}")
finally:
    ssh.close()

