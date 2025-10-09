#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
设置图谱约束和索引
"""

import paramiko
import sys

SERVER_HOST = "47.108.152.16"
SERVER_USER = "root"
SERVER_PASSWORD = "Zxylsy.99"

def main():
    """主函数"""
    print("=" * 80)
    print("设置图谱约束和索引")
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
        
        # 执行设置脚本
        setup_script = """
cd /opt/knowledge-graph && python3 << 'PYTHON_SCRIPT'
from neo4j import GraphDatabase

driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'password123'))

with driver.session() as session:
    print('=' * 80)
    print('1. 创建唯一约束')
    print('=' * 80)
    
    # Term节点唯一约束
    try:
        session.run(\"\"\"
            CREATE CONSTRAINT term_uq IF NOT EXISTS
            FOR (t:Term) REQUIRE (t.name, t.category) IS UNIQUE
        \"\"\")
        print('✅ Term节点唯一约束创建成功')
    except Exception as e:
        print(f'⚠️  Term节点唯一约束: {str(e)}')
    
    print('\\n' + '=' * 80)
    print('2. 创建属性索引')
    print('=' * 80)
    
    # category索引
    try:
        session.run(\"\"\"
            CREATE INDEX term_category IF NOT EXISTS
            FOR (t:Term) ON (t.category)
        \"\"\")
        print('✅ category索引创建成功')
    except Exception as e:
        print(f'⚠️  category索引: {str(e)}')
    
    # name索引
    try:
        session.run(\"\"\"
            CREATE INDEX term_name IF NOT EXISTS
            FOR (t:Term) ON (t.name)
        \"\"\")
        print('✅ name索引创建成功')
    except Exception as e:
        print(f'⚠️  name索引: {str(e)}')
    
    # source索引
    try:
        session.run(\"\"\"
            CREATE INDEX term_source IF NOT EXISTS
            FOR (t:Term) ON (t.source)
        \"\"\")
        print('✅ source索引创建成功')
    except Exception as e:
        print(f'⚠️  source索引: {str(e)}')
    
    print('\\n' + '=' * 80)
    print('3. 创建全文索引（支持中文搜索）')
    print('=' * 80)
    
    try:
        session.run(\"\"\"
            CREATE FULLTEXT INDEX term_fulltext IF NOT EXISTS
            FOR (t:Term) ON EACH [t.name, t.description]
        \"\"\")
        print('✅ 全文索引创建成功')
    except Exception as e:
        print(f'⚠️  全文索引: {str(e)}')
    
    print('\\n' + '=' * 80)
    print('4. 验证约束和索引')
    print('=' * 80)
    
    # 显示约束
    result = session.run('SHOW CONSTRAINTS')
    print('\\n当前约束:')
    for record in result:
        print(f'  - {record[\"name\"]}: {record[\"type\"]}')
    
    # 显示索引
    result = session.run('SHOW INDEXES')
    print('\\n当前索引:')
    for record in result:
        idx_type = record.get('type', 'N/A')
        idx_name = record.get('name', 'N/A')
        print(f'  - {idx_name}: {idx_type}')

driver.close()
print('\\n' + '=' * 80)
print('✅ 约束和索引设置完成')
print('=' * 80)
PYTHON_SCRIPT
"""
        
        stdin, stdout, stderr = ssh.exec_command(setup_script)
        
        # 输出结果
        for line in stdout:
            print(line.rstrip())
        
        # 输出错误
        error_output = stderr.read().decode('utf-8')
        if error_output:
            print(f"\n错误输出:\n{error_output}")
        
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

