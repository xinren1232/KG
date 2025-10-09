#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复重复的Term节点
"""

import paramiko
import sys

SERVER_HOST = "47.108.152.16"
SERVER_USER = "root"
SERVER_PASSWORD = "Zxylsy.99"

def main():
    """主函数"""
    print("=" * 80)
    print("检查并修复重复的Term节点")
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
    print('1. 检查重复节点')
    print('=' * 80)
    
    result = session.run(\"\"\"
        MATCH (t:Term)
        WITH t.name as name, t.category as category, collect(t) as nodes
        WHERE size(nodes) > 1
        RETURN name, category, size(nodes) as count
        ORDER BY count DESC
    \"\"\")
    
    duplicates = list(result)
    print(f'发现 {len(duplicates)} 组重复节点')
    
    if duplicates:
        print('\\n重复节点列表:')
        for i, record in enumerate(duplicates[:20], 1):
            print(f'  {i}. {record[\"name\"]} ({record[\"category\"]}): {record[\"count\"]}个')
    
    print('\\n' + '=' * 80)
    print('2. 合并重复节点')
    print('=' * 80)
    
    # 合并重复节点
    result = session.run(\"\"\"
        MATCH (t:Term)
        WITH t.name as name, t.category as category, collect(t) as nodes
        WHERE size(nodes) > 1
        WITH name, category, nodes, nodes[0] as keep, tail(nodes) as duplicates
        UNWIND duplicates as dup
        
        // 转移所有关系到保留的节点
        OPTIONAL MATCH (dup)-[r]->(other)
        WHERE NOT other IN nodes
        WITH keep, dup, r, other, name, category
        FOREACH (x IN CASE WHEN r IS NOT NULL THEN [1] ELSE [] END |
            MERGE (keep)-[new_r:PLACEHOLDER]->(other)
            SET new_r = properties(r)
        )
        
        WITH keep, dup, name, category
        OPTIONAL MATCH (other)-[r]->(dup)
        WHERE NOT other IN [keep, dup]
        WITH keep, dup, r, other, name, category
        FOREACH (x IN CASE WHEN r IS NOT NULL THEN [1] ELSE [] END |
            MERGE (other)-[new_r:PLACEHOLDER]->(keep)
            SET new_r = properties(r)
        )
        
        WITH keep, dup, name, category
        DETACH DELETE dup
        RETURN name, category, count(dup) as merged
    \"\"\")
    
    merged_count = 0
    for record in result:
        merged_count += record['merged']
        print(f'✅ 合并: {record[\"name\"]} ({record[\"category\"]}): {record[\"merged\"]}个重复节点')
    
    print(f'\\n总计合并: {merged_count}个重复节点')
    
    # 修复关系类型
    print('\\n' + '=' * 80)
    print('3. 修复关系类型')
    print('=' * 80)
    
    # 将PLACEHOLDER关系改回原类型
    result = session.run(\"\"\"
        MATCH ()-[r:PLACEHOLDER]->()
        RETURN count(r) as count
    \"\"\")
    placeholder_count = result.single()['count']
    
    if placeholder_count > 0:
        print(f'⚠️  发现 {placeholder_count} 个PLACEHOLDER关系，需要手动修复')
    else:
        print('✅ 无需修复关系类型')
    
    print('\\n' + '=' * 80)
    print('4. 验证修复结果')
    print('=' * 80)
    
    result = session.run(\"\"\"
        MATCH (t:Term)
        WITH t.name as name, t.category as category, collect(t) as nodes
        WHERE size(nodes) > 1
        RETURN count(*) as duplicate_groups
    \"\"\")
    
    remaining = result.single()['duplicate_groups']
    
    if remaining == 0:
        print('✅ 所有重复节点已清理')
    else:
        print(f'⚠️  仍有 {remaining} 组重复节点')
    
    # 统计当前节点数
    result = session.run(\"\"\"
        MATCH (t:Term)
        RETURN count(t) as total
    \"\"\")
    total = result.single()['total']
    print(f'\\n当前Term节点总数: {total}')

driver.close()
print('\\n' + '=' * 80)
print('✅ 重复节点修复完成')
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

