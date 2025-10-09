#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查应用程序日志
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import paramiko

# 服务器配置
SERVER_IP = "47.108.152.16"
USERNAME = "root"
PASSWORD = "Zxylsy.99"

def execute_ssh_command(ssh, command, description=""):
    """执行SSH命令并返回结果"""
    if description:
        print(f"\n{'='*60}")
        print(f"📌 {description}")
        print(f"{'='*60}")
    
    print(f"💻 执行命令: {command}")
    stdin, stdout, stderr = ssh.exec_command(command)
    
    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')
    
    if output:
        print(f"✅ 输出:\n{output[:2000]}")  # 限制输出长度
        if len(output) > 2000:
            print(f"\n... (输出被截断，总长度: {len(output)} 字符)")
    if error and "warning" not in error.lower():
        print(f"⚠️ 错误:\n{error[:2000]}")
        if len(error) > 2000:
            print(f"\n... (错误被截断，总长度: {len(error)} 字符)")
    
    return output, error

def check_app_logs():
    """检查应用程序日志"""
    
    print("🚀 开始检查应用程序日志...")
    
    # 创建SSH客户端
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # 连接服务器
        print(f"\n🔗 连接服务器 {SERVER_IP}...")
        ssh.connect(SERVER_IP, username=USERNAME, password=PASSWORD)
        print("✅ 连接成功！")
        
        # 1. 检查前端完整日志（最近100行）
        execute_ssh_command(
            ssh,
            "journalctl -u kg-frontend -n 100 --no-pager",
            "检查前端服务完整日志（最近100行）"
        )
        
        # 2. 检查API完整日志（最近100行）
        execute_ssh_command(
            ssh,
            "journalctl -u kg-api -n 100 --no-pager",
            "检查API服务完整日志（最近100行）"
        )
        
        # 3. 检查是否有应用日志文件
        execute_ssh_command(
            ssh,
            "ls -lh /opt/knowledge-graph/*.log 2>&1",
            "检查应用日志文件"
        )
        
        # 4. 检查是否有错误日志
        execute_ssh_command(
            ssh,
            "ls -lh /var/log/kg-* 2>&1",
            "检查系统日志目录"
        )
        
        # 5. 检查前端进程输出
        execute_ssh_command(
            ssh,
            "ps aux | grep 'vite\\|npm' | grep -v grep",
            "检查前端进程"
        )
        
        # 6. 检查API进程输出
        execute_ssh_command(
            ssh,
            "ps aux | grep 'python3.*main.py' | grep -v grep",
            "检查API进程"
        )
        
        # 7. 检查systemd服务配置
        execute_ssh_command(
            ssh,
            "cat /etc/systemd/system/kg-frontend.service",
            "查看前端服务配置"
        )
        
        execute_ssh_command(
            ssh,
            "cat /etc/systemd/system/kg-api.service",
            "查看API服务配置"
        )
        
        # 8. 测试前端访问
        execute_ssh_command(
            ssh,
            "curl -s -I http://localhost:5173 | head -10",
            "测试前端服务（端口5173）"
        )
        
        # 9. 测试API访问
        execute_ssh_command(
            ssh,
            "curl -s -I http://localhost:8000/health | head -10",
            "测试API服务（端口8000）"
        )
        
        # 10. 检查Nginx访问日志
        execute_ssh_command(
            ssh,
            "tail -20 /var/log/nginx/access.log",
            "检查Nginx访问日志"
        )
        
    except Exception as e:
        print(f"\n❌ 错误: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        ssh.close()
        print("\n🔌 SSH连接已关闭")

if __name__ == "__main__":
    check_app_logs()

