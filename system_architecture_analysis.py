#!/usr/bin/env python3
"""系统架构全面分析"""

try:
    import paramiko
except ImportError:
    import subprocess
    subprocess.run(["pip", "install", "paramiko"], check=True)
    import paramiko

import json
import os

SERVER_IP = "47.108.152.16"
SERVER_USER = "root"
SERVER_PASSWORD = "Zxylsy.99"

def exec_ssh(client, command):
    """执行SSH命令"""
    try:
        stdin, stdout, stderr = client.exec_command(command, timeout=30)
        output = stdout.read().decode('utf-8', errors='ignore')
        return output
    except Exception as e:
        return f"Error: {e}"

def main():
    print("="*80)
    print("系统架构全面分析")
    print("="*80)
    
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect(SERVER_IP, username=SERVER_USER, password=SERVER_PASSWORD)
        print("✓ 已连接到服务器\n")
        
        project_dir = "/opt/knowledge-graph"
        
        analysis = {
            "project_structure": {},
            "code_quality": {},
            "dependencies": {},
            "configuration": {},
            "database": {},
            "api_design": {},
            "frontend": {},
            "deployment": {}
        }
        
        # 1. 项目结构分析
        print("1. 分析项目结构...")
        print("="*80)
        
        # 获取目录树
        output = exec_ssh(client, f"cd {project_dir} && find . -maxdepth 3 -type d | head -50")
        print(output)
        
        # 统计文件类型
        print("\n文件类型统计:")
        output = exec_ssh(client, f"cd {project_dir} && find . -type f | sed 's/.*\\.//' | sort | uniq -c | sort -rn | head -20")
        print(output)
        
        # 2. 后端API分析
        print("\n2. 后端API分析")
        print("="*80)
        
        print("\nAPI目录结构:")
        output = exec_ssh(client, f"ls -lh {project_dir}/api/")
        print(output)
        
        print("\nAPI主文件大小:")
        output = exec_ssh(client, f"wc -l {project_dir}/api/main.py")
        print(output)
        
        print("\nAPI依赖:")
        output = exec_ssh(client, f"cat {project_dir}/api/requirements.txt 2>/dev/null || echo 'No requirements.txt'")
        print(output)
        
        # 3. 前端分析
        print("\n3. 前端分析")
        print("="*80)
        
        print("\n前端目录结构:")
        output = exec_ssh(client, f"ls -lh {project_dir}/apps/web/")
        print(output)
        
        print("\npackage.json:")
        output = exec_ssh(client, f"cat {project_dir}/apps/web/package.json 2>/dev/null | head -50")
        print(output)
        
        print("\n前端组件:")
        output = exec_ssh(client, f"find {project_dir}/apps/web/src -name '*.vue' | wc -l")
        vue_count = output.strip()
        print(f"Vue组件数量: {vue_count}")
        
        # 4. 数据库分析
        print("\n4. 数据库分析")
        print("="*80)
        
        print("\nNeo4j配置:")
        output = exec_ssh(client, f"cat /etc/neo4j/neo4j.conf 2>/dev/null | grep -v '^#' | grep -v '^$' | head -20")
        print(output)
        
        # 5. 配置文件分析
        print("\n5. 配置文件分析")
        print("="*80)
        
        print("\n配置文件:")
        output = exec_ssh(client, f"ls -lh {project_dir}/config/")
        print(output)
        
        # 6. 数据文件分析
        print("\n6. 数据文件分析")
        print("="*80)
        
        print("\n数据目录:")
        output = exec_ssh(client, f"du -sh {project_dir}/data/*")
        print(output)
        
        # 7. Nginx配置分析
        print("\n7. Nginx配置分析")
        print("="*80)
        
        print("\nNginx配置:")
        output = exec_ssh(client, f"cat {project_dir}/nginx/nginx.conf 2>/dev/null || cat /etc/nginx/sites-enabled/default 2>/dev/null | head -50")
        print(output)
        
        # 8. 服务配置分析
        print("\n8. Systemd服务配置")
        print("="*80)
        
        print("\nAPI服务配置:")
        output = exec_ssh(client, f"cat /etc/systemd/system/kg-api.service 2>/dev/null")
        print(output)
        
        print("\n前端服务配置:")
        output = exec_ssh(client, f"cat /etc/systemd/system/kg-frontend.service 2>/dev/null")
        print(output)
        
        # 9. 代码质量分析
        print("\n9. 代码质量分析")
        print("="*80)
        
        print("\nPython代码行数:")
        output = exec_ssh(client, f"find {project_dir} -name '*.py' -exec wc -l {{}} + | tail -1")
        print(output)
        
        print("\nJavaScript/Vue代码行数:")
        output = exec_ssh(client, f"find {project_dir}/apps/web/src -name '*.js' -o -name '*.vue' -o -name '*.ts' | xargs wc -l 2>/dev/null | tail -1")
        print(output)
        
        # 10. 安全性检查
        print("\n10. 安全性检查")
        print("="*80)
        
        print("\n环境变量文件:")
        output = exec_ssh(client, f"find {project_dir} -name '.env*' -o -name '*.env'")
        print(output)
        
        print("\n敏感文件权限:")
        output = exec_ssh(client, f"ls -la {project_dir}/.env* 2>/dev/null || echo 'No .env files'")
        print(output)
        
    finally:
        client.close()
        print("\n连接已关闭")

if __name__ == "__main__":
    main()

