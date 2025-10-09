#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查错误日志
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
    _, stdout, stderr = ssh.exec_command(command)
    
    output = stdout.read().decode('utf-8', errors='ignore')
    error = stderr.read().decode('utf-8', errors='ignore')
    
    if output:
        print(f"✅ 输出:\n{output[:3000]}")
        if len(output) > 3000:
            print(f"\n... (输出被截断，总长度: {len(output)} 字符)")
    if error and "warning" not in error.lower():
        print(f"⚠️ 错误:\n{error[:1000]}")
    
    return output, error

def check_error_logs():
    """检查错误日志"""
    
    print("开始检查错误日志...")
    
    # 创建SSH客户端
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # 连接服务器
        print(f"\n连接服务器 {SERVER_IP}...")
        ssh.connect(SERVER_IP, username=USERNAME, password=PASSWORD)
        print("连接成功！")
        
        # 1. 检查API错误日志大小和最后修改时间
        execute_ssh_command(
            ssh,
            "ls -lh /var/log/kg-api-error.log",
            "检查API错误日志文件信息"
        )
        
        # 2. 查看API错误日志最后100行
        execute_ssh_command(
            ssh,
            "tail -100 /var/log/kg-api-error.log",
            "API错误日志（最后100行）"
        )
        
        # 3. 统计错误类型
        execute_ssh_command(
            ssh,
            "grep -o 'Error\\|Exception\\|WARNING\\|CRITICAL' /var/log/kg-api-error.log | sort | uniq -c | sort -rn",
            "统计错误类型"
        )
        
        # 4. 查看前端错误日志
        execute_ssh_command(
            ssh,
            "cat /var/log/kg-frontend-error.log",
            "前端错误日志"
        )
        
        # 5. 检查最近的错误（最近1小时）
        execute_ssh_command(
            ssh,
            "find /var/log/kg-api-error.log -mmin -60 -exec tail -50 {} \\;",
            "最近1小时的API错误"
        )
        
        # 6. 检查日志文件行数
        execute_ssh_command(
            ssh,
            "wc -l /var/log/kg-api-error.log",
            "API错误日志行数"
        )
        
        # 7. 查看日志中的唯一错误消息（去重）
        execute_ssh_command(
            ssh,
            "tail -1000 /var/log/kg-api-error.log | grep -E 'Error|Exception' | sort | uniq -c | sort -rn | head -20",
            "最常见的错误消息（最近1000行）"
        )
        
        # 8. 检查是否有磁盘空间问题
        execute_ssh_command(
            ssh,
            "df -h /var/log",
            "检查日志分区磁盘空间"
        )
        
        # 9. 检查日志轮转配置
        execute_ssh_command(
            ssh,
            "ls -lh /etc/logrotate.d/ | grep kg",
            "检查日志轮转配置"
        )
        
        # 10. 查看当前API进程的实时日志
        execute_ssh_command(
            ssh,
            "journalctl -u kg-api --since '5 minutes ago' --no-pager",
            "API服务最近5分钟的日志"
        )
        
    except Exception as e:
        print(f"\n错误: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        ssh.close()
        print("\nSSH连接已关闭")

if __name__ == "__main__":
    check_error_logs()

