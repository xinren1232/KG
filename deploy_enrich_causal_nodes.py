#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
部署因果关系节点数据补充脚本到服务器并执行
"""

import paramiko
import sys
import os

SERVER_HOST = "47.108.152.16"
SERVER_USER = "root"
SERVER_PASSWORD = "Zxylsy.99"
PROJECT_DIR = "/opt/knowledge-graph"

def main():
    """主函数"""
    print("=" * 80)
    print("部署因果关系节点数据补充脚本")
    print("=" * 80)
    
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
        print("✅ 服务器连接成功\n")
        
        # 上传脚本
        print("上传补充脚本...")
        sftp = ssh.open_sftp()
        local_script = "enrich_causal_nodes.py"
        remote_script = f"{PROJECT_DIR}/enrich_causal_nodes.py"
        
        sftp.put(local_script, remote_script)
        print(f"✅ 上传成功: {local_script} -> {remote_script}\n")
        sftp.close()
        
        # 执行脚本
        print("=" * 80)
        print("执行数据补充脚本")
        print("=" * 80)
        
        command = f"cd {PROJECT_DIR} && python3 enrich_causal_nodes.py"
        stdin, stdout, stderr = ssh.exec_command(command)
        
        # 实时输出结果
        for line in stdout:
            print(line.rstrip())
        
        # 输出错误
        error_output = stderr.read().decode('utf-8')
        if error_output:
            print(f"\n错误输出:\n{error_output}")
        
        # 验证补充效果
        print("\n" + "=" * 80)
        print("验证补充效果")
        print("=" * 80)
        
        verify_script = """
cd /opt/knowledge-graph && python3 << 'PYTHON_SCRIPT'
from neo4j import GraphDatabase

driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'password123'))

with driver.session() as session:
    # 检查补充后的数据完整性
    result = session.run('''
        MATCH (t:Term)
        WHERE t.source = 'causal_relationship_import'
        RETURN 
            count(t) as total,
            sum(CASE WHEN t.description IS NOT NULL AND t.description <> '' THEN 1 ELSE 0 END) as has_desc,
            sum(CASE WHEN (t)-[:HAS_TAG]->(:Tag) THEN 1 ELSE 0 END) as has_tags
    ''')
    stats = result.single()
    
    total = stats['total']
    has_desc = stats['has_desc']
    has_tags = stats['has_tags']
    
    print(f'因果关系节点总数: {total}')
    print(f'有描述: {has_desc} ({has_desc/total*100:.1f}%)')
    print(f'有标签: {has_tags} ({has_tags/total*100:.1f}%)')
    print()
    
    # 显示几个示例
    print('补充后的示例:')
    result = session.run('''
        MATCH (t:Term)
        WHERE t.source = 'causal_relationship_import' 
          AND t.description IS NOT NULL 
          AND t.description <> ''
        OPTIONAL MATCH (t)-[:HAS_TAG]->(g:Tag)
        WITH t, collect(g.name) as tags
        RETURN t.name as name, t.description as description, tags
        LIMIT 5
    ''')
    
    for i, record in enumerate(result, 1):
        name = record['name']
        desc = record['description']
        tags = record['tags']
        print(f'\\n{i}. {name}')
        print(f'   描述: {desc[:60]}...' if len(desc) > 60 else f'   描述: {desc}')
        print(f'   标签: {", ".join(tags) if tags else "(无)"}')

driver.close()
PYTHON_SCRIPT
"""
        
        stdin, stdout, stderr = ssh.exec_command(verify_script)
        
        for line in stdout:
            print(line.rstrip())
        
        error_output = stderr.read().decode('utf-8')
        if error_output:
            print(f"\n错误输出:\n{error_output}")
        
        print("\n" + "=" * 80)
        print("✅ 部署和执行完成！")
        print("=" * 80)
        
        return 0
        
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

