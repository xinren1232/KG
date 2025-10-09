#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复PLACEHOLDER关系
"""

import paramiko
import sys

SERVER_HOST = "47.108.152.16"
SERVER_USER = "root"
SERVER_PASSWORD = "Zxylsy.99"

def main():
    """主函数"""
    print("=" * 80)
    print("修复PLACEHOLDER关系")
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
        
        # 执行修复脚本
        fix_script = """
cd /opt/knowledge-graph && python3 << 'PYTHON_SCRIPT'
from neo4j import GraphDatabase

driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'password123'))

with driver.session() as session:
    print('=' * 80)
    print('1. 检查PLACEHOLDER关系')
    print('=' * 80)
    
    result = session.run(\"\"\"
        MATCH (s)-[r:PLACEHOLDER]->(t)
        RETURN s.name as source, t.name as target, properties(r) as props
        LIMIT 20
    \"\"\")
    
    placeholders = list(result)
    print(f'发现 {len(placeholders)} 个PLACEHOLDER关系')
    
    if placeholders:
        print('\\nPLACEHOLDER关系示例:')
        for i, record in enumerate(placeholders[:5], 1):
            print(f'  {i}. {record[\"source\"]} -> {record[\"target\"]}')
            print(f'     属性: {record[\"props\"]}')
    
    print('\\n' + '=' * 80)
    print('2. 删除PLACEHOLDER关系（这些是合并过程中的临时关系）')
    print('=' * 80)
    
    result = session.run(\"\"\"
        MATCH ()-[r:PLACEHOLDER]->()
        DELETE r
        RETURN count(r) as deleted
    \"\"\")
    
    deleted = result.single()['deleted']
    print(f'✅ 删除了 {deleted} 个PLACEHOLDER关系')
    
    print('\\n' + '=' * 80)
    print('3. 验证修复结果')
    print('=' * 80)
    
    result = session.run(\"\"\"
        MATCH ()-[r:PLACEHOLDER]->()
        RETURN count(r) as count
    \"\"\")
    
    remaining = result.single()['count']
    
    if remaining == 0:
        print('✅ 所有PLACEHOLDER关系已清理')
    else:
        print(f'⚠️  仍有 {remaining} 个PLACEHOLDER关系')
    
    # 统计当前关系类型
    print('\\n' + '=' * 80)
    print('4. 当前关系类型统计')
    print('=' * 80)
    
    result = session.run(\"\"\"
        MATCH ()-[r]->()
        RETURN type(r) as rel_type, count(*) as count
        ORDER BY count DESC
    \"\"\")
    
    total = 0
    for record in result:
        rel_type = record['rel_type']
        count = record['count']
        total += count
        print(f'{rel_type:20s}: {count:6d}')
    
    print(f'{'总计':20s}: {total:6d}')

driver.close()
print('\\n' + '=' * 80)
print('✅ PLACEHOLDER关系修复完成')
print('=' * 80)
PYTHON_SCRIPT
"""
        
        stdin, stdout, stderr = ssh.exec_command(fix_script)
        
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

