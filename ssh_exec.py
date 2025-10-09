#!/usr/bin/env python3
"""
SSH执行脚本 - 自动使用密码连接
"""
import subprocess
import sys

def ssh_exec(command):
    """执行SSH命令"""
    password = "Zxylsy.99"
    server = "root@47.108.152.16"
    
    # 使用echo传递密码给ssh
    full_command = f'echo {password} | ssh {server} "{command}"'
    
    print(f"执行命令: {command}")
    print("="*60)
    
    result = subprocess.run(
        full_command,
        shell=True,
        capture_output=True,
        text=True
    )
    
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print("错误:", result.stderr)
    
    return result.returncode

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python ssh_exec.py '命令'")
        sys.exit(1)
    
    command = sys.argv[1]
    exit_code = ssh_exec(command)
    sys.exit(exit_code)

