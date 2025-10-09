#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
标准化关系属性
"""

import paramiko
import sys

SERVER_HOST = "47.108.152.16"
SERVER_USER = "root"
SERVER_PASSWORD = "Zxylsy.99"

def main():
    """主函数"""
    print("=" * 80)
    print("标准化关系属性")
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
        
        # 上传并执行Python脚本
        script_content = '''from neo4j import GraphDatabase
import hashlib
from datetime import datetime

driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'password123'))

with driver.session() as session:
    print('=' * 80)
    print('1. 为CAUSES关系补充source_hash')
    print('=' * 80)

    # 获取所有CAUSES关系
    result = session.run("""
        MATCH (s)-[r:CAUSES]->(t)
        WHERE r.source_hash IS NULL
        RETURN id(r) as rel_id, s.name as source_name, t.name as target_name,
               coalesce(r.evidence, '') as evidence, coalesce(r.source, '') as source
    """)

    relations = list(result)
    print(f'找到 {len(relations)} 个需要更新的CAUSES关系')

    # 逐个更新
    updated = 0
    for rel in relations:
        # 生成hash
        hash_input = f"{rel['source_name']}|{rel['target_name']}|{rel['evidence']}|{rel['source']}"
        source_hash = hashlib.md5(hash_input.encode()).hexdigest()

        # 更新关系
        session.run("""
            MATCH ()-[r:CAUSES]->()
            WHERE id(r) = $rel_id
            SET r.source_hash = $source_hash,
                r.status = 'verified',
                r.updated_at = datetime()
        """, rel_id=rel['rel_id'], source_hash=source_hash)
        updated += 1

    print(f'✅ 更新了 {updated} 个CAUSES关系')
    
    print('\\n' + '=' * 80)
    print('2. 为其他业务关系补充基础属性')
    print('=' * 80)

    # 定义关系类型和默认置信度
    rel_configs = [
        ('AFFECTS', 0.8),
        ('TESTS', 0.9),
        ('USED_IN', 0.9),
        ('PRODUCES', 0.9),
        ('RELATED_TO', 0.7)
    ]

    for rel_type, default_conf in rel_configs:
        # 获取需要更新的关系
        result = session.run(f"""
            MATCH (s)-[r:{rel_type}]->(t)
            WHERE r.status IS NULL
            RETURN id(r) as rel_id, s.name as source_name, t.name as target_name
        """)

        relations = list(result)
        if not relations:
            print(f'✅ {rel_type}: 无需更新')
            continue

        # 逐个更新
        for rel in relations:
            hash_input = f"{rel['source_name']}|{rel['target_name']}|{rel_type}"
            source_hash = hashlib.md5(hash_input.encode()).hexdigest()

            session.run(f"""
                MATCH ()-[r:{rel_type}]->()
                WHERE id(r) = $rel_id
                SET r.status = 'verified',
                    r.confidence = coalesce(r.confidence, $default_conf),
                    r.source = coalesce(r.source, 'legacy_data'),
                    r.created_at = coalesce(r.created_at, datetime()),
                    r.updated_at = datetime(),
                    r.source_hash = $source_hash
            """, rel_id=rel['rel_id'], default_conf=default_conf, source_hash=source_hash)

        print(f'✅ {rel_type}: 更新了 {len(relations)} 个关系')
    
    print('\\n' + '=' * 80)
    print('3. 验证属性完整性')
    print('=' * 80)
    
    result = session.run("""
        MATCH ()-[r:CAUSES|AFFECTS|TESTS|USED_IN|PRODUCES|RELATED_TO]->()
        RETURN type(r) as rel_type,
               count(r) as total,
               sum(CASE WHEN r.status IS NOT NULL THEN 1 ELSE 0 END) as has_status,
               sum(CASE WHEN r.confidence IS NOT NULL THEN 1 ELSE 0 END) as has_confidence,
               sum(CASE WHEN r.source_hash IS NOT NULL THEN 1 ELSE 0 END) as has_hash,
               avg(r.confidence) as avg_conf
        ORDER BY total DESC
    """)
    
    print(f'{"关系类型":15s} {"总数":>6s} {"status":>8s} {"confidence":>12s} {"source_hash":>12s} {"平均置信度":>10s}')
    print('-' * 80)
    for record in result:
        rel_type = record['rel_type']
        total = record['total']
        has_status = record['has_status']
        has_conf = record['has_confidence']
        has_hash = record['has_hash']
        avg_conf = record['avg_conf'] or 0
        print(f'{rel_type:15s} {total:6d} {has_status:8d} {has_conf:12d} {has_hash:12d} {avg_conf:10.3f}')

driver.close()
print('\\n' + '=' * 80)
print('✅ 关系属性标准化完成')
print('=' * 80)
'''
        
        # 上传脚本
        sftp = ssh.open_sftp()
        remote_script = '/opt/knowledge-graph/standardize_relations.py'
        with sftp.open(remote_script, 'w') as f:
            f.write(script_content)
        sftp.close()
        print("✅ 脚本已上传\n")
        
        # 执行脚本
        print("=" * 80)
        print("执行关系属性标准化")
        print("=" * 80)
        
        stdin, stdout, stderr = ssh.exec_command(f'cd /opt/knowledge-graph && python3 standardize_relations.py')
        
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

