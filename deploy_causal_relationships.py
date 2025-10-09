#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
部署因果关系导入脚本到服务器并执行
"""

import paramiko
import os
import sys
from pathlib import Path

# 服务器配置
SERVER_HOST = "47.108.152.16"
SERVER_USER = "root"
SERVER_PASSWORD = "Zxylsy.99"
PROJECT_DIR = "/opt/knowledge-graph"

def upload_file(sftp, local_path, remote_path):
    """上传文件到服务器"""
    try:
        sftp.put(local_path, remote_path)
        print(f"✅ 上传成功: {local_path} -> {remote_path}")
        return True
    except Exception as e:
        print(f"❌ 上传失败: {local_path} -> {remote_path}")
        print(f"   错误: {str(e)}")
        return False

def execute_command(ssh, command, description=""):
    """执行SSH命令"""
    if description:
        print(f"\n{'='*80}")
        print(f"执行: {description}")
        print(f"{'='*80}")
    
    stdin, stdout, stderr = ssh.exec_command(command)
    
    # 实时输出
    for line in stdout:
        print(line.strip())
    
    # 输出错误信息
    error_output = stderr.read().decode('utf-8')
    if error_output:
        print(f"错误输出:\n{error_output}")
    
    return stdout.channel.recv_exit_status()

def main():
    """主函数"""
    print("=" * 80)
    print("开始部署因果关系导入脚本到服务器")
    print("=" * 80)
    
    # 创建SSH客户端
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # 连接服务器
        print(f"\n连接服务器: {SERVER_HOST}")
        ssh.connect(
            hostname=SERVER_HOST,
            username=SERVER_USER,
            password=SERVER_PASSWORD,
            timeout=30
        )
        print("✅ 服务器连接成功")
        
        # 创建SFTP客户端
        sftp = ssh.open_sftp()
        
        # 上传导入脚本
        local_script = "import_causal_relationships.py"
        remote_script = f"{PROJECT_DIR}/import_causal_relationships.py"
        
        if not os.path.exists(local_script):
            print(f"❌ 本地文件不存在: {local_script}")
            return 1
        
        print(f"\n上传导入脚本...")
        if not upload_file(sftp, local_script, remote_script):
            return 1
        
        # 设置执行权限
        execute_command(
            ssh,
            f"chmod +x {remote_script}",
            "设置执行权限"
        )
        
        # 检查Neo4j连接
        print("\n检查Neo4j服务状态...")
        execute_command(
            ssh,
            "systemctl status neo4j | head -10",
            "Neo4j服务状态"
        )
        
        # 执行导入脚本
        print("\n" + "=" * 80)
        print("开始执行因果关系导入")
        print("=" * 80)
        
        exit_code = execute_command(
            ssh,
            f"cd {PROJECT_DIR} && python3 {remote_script}",
            "执行导入脚本"
        )
        
        if exit_code == 0:
            print("\n" + "=" * 80)
            print("✅ 因果关系导入成功完成！")
            print("=" * 80)
        else:
            print("\n" + "=" * 80)
            print(f"❌ 导入脚本执行失败，退出码: {exit_code}")
            print("=" * 80)
            return exit_code
        
        # 验证导入结果
        print("\n验证导入结果...")
        execute_command(
            ssh,
            f"""cd {PROJECT_DIR} && python3 -c "
from neo4j import GraphDatabase
driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'password123'))
with driver.session() as session:
    # 统计CAUSES关系数量
    result = session.run('MATCH ()-[r:CAUSES]->() RETURN count(r) as count')
    count = result.single()['count']
    print(f'✅ CAUSES关系总数: {{count}}')
    
    # 统计高置信度关系
    result = session.run('MATCH ()-[r:CAUSES]->() WHERE r.confidence >= 0.8 RETURN count(r) as count')
    high_conf = result.single()['count']
    print(f'✅ 高置信度关系(>=0.8): {{high_conf}}')
    
    # 显示部分关系示例
    result = session.run('''
        MATCH (s:Term)-[r:CAUSES]->(t:Term)
        RETURN s.name as source, t.name as target, r.confidence as confidence
        ORDER BY r.confidence DESC
        LIMIT 5
    ''')
    print('\\n前5个高置信度因果关系:')
    for record in result:
        print(f'  {{record[\"source\"]}} -> {{record[\"target\"]}} (置信度: {{record[\"confidence\"]}})')
driver.close()
"
""",
            "验证导入结果"
        )
        
        print("\n" + "=" * 80)
        print("✅ 部署和导入全部完成！")
        print("=" * 80)
        
        return 0
        
    except paramiko.AuthenticationException:
        print("❌ SSH认证失败，请检查用户名和密码")
        return 1
    except paramiko.SSHException as e:
        print(f"❌ SSH连接错误: {str(e)}")
        return 1
    except Exception as e:
        print(f"❌ 发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        ssh.close()
        print("\n服务器连接已关闭")

if __name__ == "__main__":
    sys.exit(main())

