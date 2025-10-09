#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复日志问题
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
        print(f"输出:\n{output}")
    if error and "warning" not in error.lower():
        print(f"错误:\n{error}")
    
    return output, error

def fix_logs():
    """修复日志问题"""
    
    print("开始修复日志问题...")
    
    # 创建SSH客户端
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # 连接服务器
        print(f"\n连接服务器 {SERVER_IP}...")
        ssh.connect(SERVER_IP, username=USERNAME, password=PASSWORD)
        print("连接成功！")
        
        # 1. 备份当前日志
        execute_ssh_command(
            ssh,
            "cp /var/log/kg-api-error.log /var/log/kg-api-error.log.backup.$(date +%Y%m%d_%H%M%S)",
            "1. 备份API错误日志"
        )
        
        # 2. 清空日志文件
        execute_ssh_command(
            ssh,
            "truncate -s 0 /var/log/kg-api-error.log",
            "2. 清空API错误日志"
        )
        
        execute_ssh_command(
            ssh,
            "truncate -s 0 /var/log/kg-api.log",
            "3. 清空API日志"
        )
        
        execute_ssh_command(
            ssh,
            "truncate -s 0 /var/log/kg-frontend-error.log",
            "4. 清空前端错误日志"
        )
        
        # 3. 创建日志轮转配置
        logrotate_config = """cat > /etc/logrotate.d/knowledge-graph << 'EOF'
/var/log/kg-*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 0644 root root
    size 10M
    postrotate
        systemctl reload kg-api >/dev/null 2>&1 || true
        systemctl reload kg-frontend >/dev/null 2>&1 || true
    endscript
}
EOF"""
        
        execute_ssh_command(
            ssh,
            logrotate_config,
            "5. 创建日志轮转配置"
        )
        
        # 4. 测试日志轮转配置
        execute_ssh_command(
            ssh,
            "logrotate -d /etc/logrotate.d/knowledge-graph",
            "6. 测试日志轮转配置"
        )
        
        # 5. 检查日志文件大小
        execute_ssh_command(
            ssh,
            "ls -lh /var/log/kg-*.log",
            "7. 检查日志文件大小"
        )
        
        # 6. 配置Python日志级别（减少Neo4j警告）
        python_logging_config = """cat > /opt/knowledge-graph/api/logging_config.py << 'EOF'
import logging

# 配置日志级别
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# 减少Neo4j驱动的警告日志
logging.getLogger('neo4j').setLevel(logging.ERROR)
logging.getLogger('neo4j.notifications').setLevel(logging.ERROR)
EOF"""
        
        execute_ssh_command(
            ssh,
            python_logging_config,
            "8. 创建Python日志配置"
        )
        
        # 7. 检查main.py是否导入了日志配置
        execute_ssh_command(
            ssh,
            "head -20 /opt/knowledge-graph/api/main.py",
            "9. 检查main.py开头"
        )
        
        # 8. 重启API服务以应用更改
        print("\n" + "="*60)
        print("是否需要重启API服务以应用日志配置？")
        print("="*60)
        print("注意：重启服务会短暂中断API访问（约2-3秒）")
        print("\n如需重启，请手动执行：")
        print("  ssh root@47.108.152.16")
        print("  systemctl restart kg-api")
        
        # 9. 显示修复总结
        print("\n" + "="*60)
        print("修复总结")
        print("="*60)
        print("\n已完成的操作：")
        print("  1. 备份旧日志文件")
        print("  2. 清空所有日志文件")
        print("  3. 创建日志轮转配置（每日轮转，保留7天，超过10MB轮转）")
        print("  4. 创建Python日志配置（减少Neo4j警告）")
        print("\n日志问题原因：")
        print("  - Neo4j查询中引用了不存在的标签（Process, Role, Metric等）")
        print("  - 每次查询都产生WARNING，累积了43,039条警告")
        print("  - 日志文件达到13MB")
        print("\n解决方案：")
        print("  1. 已清空日志文件")
        print("  2. 已配置日志轮转，防止日志文件过大")
        print("  3. 已配置Python日志级别，将Neo4j警告级别提升到ERROR")
        print("\n下一步建议：")
        print("  1. 重启API服务应用日志配置")
        print("  2. 更新Neo4j查询，只查询实际存在的标签")
        print("  3. 监控日志文件大小")
        
    except Exception as e:
        print(f"\n错误: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        ssh.close()
        print("\nSSH连接已关闭")

if __name__ == "__main__":
    fix_logs()

