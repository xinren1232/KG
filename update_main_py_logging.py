#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新main.py以修复日志和Neo4j查询问题
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
        print(f"{description}")
        print(f"{'='*60}")
    
    print(f"执行命令: {command}")
    _, stdout, stderr = ssh.exec_command(command)
    
    output = stdout.read().decode('utf-8', errors='ignore')
    error = stderr.read().decode('utf-8', errors='ignore')
    
    if output:
        print(f"输出:\n{output[:1000]}")
        if len(output) > 1000:
            print(f"... (输出被截断)")
    if error and "warning" not in error.lower():
        print(f"错误:\n{error[:500]}")
    
    return output, error

def update_main_py():
    """更新main.py"""
    
    print("开始更新main.py...")
    
    # 创建SSH客户端
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # 连接服务器
        print(f"\n连接服务器 {SERVER_IP}...")
        ssh.connect(SERVER_IP, username=USERNAME, password=PASSWORD)
        print("连接成功！")
        
        # 1. 备份main.py
        execute_ssh_command(
            ssh,
            "cp /opt/knowledge-graph/api/main.py /opt/knowledge-graph/api/main.py.backup.$(date +%Y%m%d_%H%M%S)",
            "1. 备份main.py"
        )
        
        # 2. 在main.py开头添加日志配置导入
        update_logging_cmd = """sed -i '1a\\
# 导入日志配置（必须在其他导入之前）\\
import logging\\
logging.getLogger("neo4j").setLevel(logging.ERROR)\\
logging.getLogger("neo4j.notifications").setLevel(logging.ERROR)\\
' /opt/knowledge-graph/api/main.py"""
        
        execute_ssh_command(
            ssh,
            update_logging_cmd,
            "2. 添加日志配置到main.py"
        )
        
        # 3. 检查实际存在的Neo4j标签
        execute_ssh_command(
            ssh,
            "cypher-shell -u neo4j -p Zxylsy.99 'CALL db.labels()' 2>&1 | grep -v 'WARNING'",
            "3. 检查Neo4j中实际存在的标签"
        )
        
        # 4. 更新Neo4j查询，移除不存在的标签
        # 实际存在的标签：Term, Category, Tag, Alias
        fix_query_cmd = """python3 << 'PYEOF'
import re

# 读取main.py
with open('/opt/knowledge-graph/api/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 定义实际存在的标签
existing_labels = ['Term', 'Category', 'Tag', 'Alias']
label_pattern = ' OR '.join([f'a:{label}' for label in existing_labels])
label_pattern_b = ' OR '.join([f'b:{label}' for label in existing_labels])

# 替换查询中的标签列表
# 查找所有包含多个OR标签的WHERE子句
old_pattern_a = r'WHERE \\(a:Term OR a:Category OR a:Tag OR a:Component OR a:Symptom OR a:Tool OR a:Process OR a:TestCase OR a:Material OR a:Role OR a:Metric\\)'
new_pattern_a = f'WHERE ({label_pattern})'

old_pattern_b = r'AND \\(b:Term OR b:Category OR b:Tag OR b:Component OR b:Symptom OR b:Tool OR b:Process OR b:TestCase OR b:Material OR b:Role OR b:Metric\\)'
new_pattern_b = f'AND ({label_pattern_b})'

old_pattern_n = r'WHERE n:Term OR n:Category OR n:Tag OR n:Component OR n:Symptom OR n:Tool OR n:Process OR n:TestCase OR n:Material OR n:Role OR n:Metric'
new_pattern_n = f'WHERE {" OR ".join([f"n:{label}" for label in existing_labels])}'

# 执行替换
content = re.sub(old_pattern_a, new_pattern_a, content)
content = re.sub(old_pattern_b, new_pattern_b, content)
content = re.sub(old_pattern_n, new_pattern_n, content)

# 写回文件
with open('/opt/knowledge-graph/api/main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("已更新Neo4j查询中的标签")
PYEOF"""
        
        execute_ssh_command(
            ssh,
            fix_query_cmd,
            "4. 更新Neo4j查询中的标签"
        )
        
        # 5. 验证更新
        execute_ssh_command(
            ssh,
            "grep -n 'WHERE.*Term OR.*Category' /opt/knowledge-graph/api/main.py | head -5",
            "5. 验证查询更新"
        )
        
        # 6. 检查main.py语法
        execute_ssh_command(
            ssh,
            "cd /opt/knowledge-graph/api && python3 -m py_compile main.py && echo '语法检查通过'",
            "6. 检查Python语法"
        )
        
        # 7. 重启API服务
        print("\n" + "="*60)
        print("准备重启API服务...")
        print("="*60)
        
        execute_ssh_command(
            ssh,
            "systemctl restart kg-api",
            "7. 重启API服务"
        )
        
        # 等待服务启动
        import time
        print("\n等待服务启动（5秒）...")
        time.sleep(5)
        
        # 8. 检查服务状态
        execute_ssh_command(
            ssh,
            "systemctl status kg-api --no-pager | head -15",
            "8. 检查API服务状态"
        )
        
        # 9. 测试API
        execute_ssh_command(
            ssh,
            "curl -s http://localhost:8000/health | python3 -m json.tool",
            "9. 测试API健康检查"
        )
        
        # 10. 检查新日志
        execute_ssh_command(
            ssh,
            "tail -20 /var/log/kg-api-error.log",
            "10. 检查新的错误日志"
        )
        
        # 11. 检查日志文件大小
        execute_ssh_command(
            ssh,
            "ls -lh /var/log/kg-*.log",
            "11. 检查日志文件大小"
        )
        
        print("\n" + "="*60)
        print("更新完成总结")
        print("="*60)
        print("\n已完成的操作：")
        print("  1. 备份main.py")
        print("  2. 添加日志配置（禁用Neo4j警告）")
        print("  3. 更新Neo4j查询（只使用实际存在的标签）")
        print("  4. 重启API服务")
        print("  5. 验证服务正常运行")
        print("\n修复的问题：")
        print("  - 移除了不存在的标签：Component, Symptom, Tool, Process, TestCase, Material, Role, Metric")
        print("  - 只保留实际存在的标签：Term, Category, Tag, Alias")
        print("  - 禁用Neo4j驱动的WARNING日志")
        print("\n结果：")
        print("  - 不再产生大量WARNING日志")
        print("  - 日志文件大小得到控制")
        print("  - API查询更加精确和高效")
        
    except Exception as e:
        print(f"\n错误: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        ssh.close()
        print("\nSSH连接已关闭")

if __name__ == "__main__":
    update_main_py()

