#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析当前图谱结构
"""

import paramiko
import sys

SERVER_HOST = "47.108.152.16"
SERVER_USER = "root"
SERVER_PASSWORD = "Zxylsy.99"

def main():
    """主函数"""
    print("=" * 80)
    print("当前图谱结构分析")
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
        
        # 执行分析脚本
        analyze_script = """
cd /opt/knowledge-graph && python3 << 'PYTHON_SCRIPT'
from neo4j import GraphDatabase

driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'password123'))

with driver.session() as session:
    print('=' * 80)
    print('1. 当前关系类型统计')
    print('=' * 80)
    result = session.run(
        "MATCH ()-[r]->() RETURN type(r) as rel_type, count(*) as count ORDER BY count DESC"
    )
    
    total_rels = 0
    for record in result:
        rel_type = record['rel_type']
        count = record['count']
        total_rels += count
        print(f'{rel_type:20s}: {count:6d}')
    
    print(f'{"总计":20s}: {total_rels:6d}')
    
    print('\\n' + '=' * 80)
    print('2. 检查CAUSES关系的属性')
    print('=' * 80)

    query = \"\"\"
        MATCH ()-[r:CAUSES]->()
        RETURN
            count(r) as total,
            sum(CASE WHEN r.confidence IS NOT NULL THEN 1 ELSE 0 END) as has_confidence,
            sum(CASE WHEN r.evidence IS NOT NULL THEN 1 ELSE 0 END) as has_evidence,
            sum(CASE WHEN r.confidence_reason IS NOT NULL THEN 1 ELSE 0 END) as has_reason,
            avg(r.confidence) as avg_confidence
    \"\"\"
    result = session.run(query)
    stats = result.single()
    if stats and stats['total'] > 0:
        print(f'CAUSES关系: {stats["total"]}条')
        print(f'  - 有confidence: {stats["has_confidence"]} ({stats["has_confidence"]/stats["total"]*100:.1f}%)')
        print(f'  - 有evidence: {stats["has_evidence"]} ({stats["has_evidence"]/stats["total"]*100:.1f}%)')
        print(f'  - 有confidence_reason: {stats["has_reason"]} ({stats["has_reason"]/stats["total"]*100:.1f}%)')
        print(f'  - 平均confidence: {stats["avg_confidence"]:.3f}')
    
    print('\\n' + '=' * 80)
    print('3. 节点标签分布')
    print('=' * 80)
    result = session.run(
        "MATCH (n) UNWIND labels(n) as label RETURN label, count(*) as count ORDER BY count DESC"
    )
    
    for record in result:
        label = record['label']
        count = record['count']
        print(f'{label:20s}: {count:6d}')
    
    print('\\n' + '=' * 80)
    print('4. Term节点的category分布')
    print('=' * 80)
    result = session.run(
        "MATCH (t:Term) RETURN t.category as category, count(*) as count ORDER BY count DESC"
    )
    
    for record in result:
        category = record['category']
        count = record['count']
        print(f'{category:20s}: {count:6d}')
    
    print('\\n' + '=' * 80)
    print('5. 检查关系的起止节点类型')
    print('=' * 80)
    
    # 检查CAUSES关系
    query = \"\"\"
        MATCH (s)-[r:CAUSES]->(t)
        RETURN
            labels(s)[0] as source_label,
            s.category as source_category,
            labels(t)[0] as target_label,
            t.category as target_category,
            count(*) as count
        ORDER BY count DESC
        LIMIT 10
    \"\"\"
    result = session.run(query)
    
    print('CAUSES关系的起止节点:')
    for record in result:
        src_label = record['source_label']
        src_cat = record['source_category'] or 'N/A'
        tgt_label = record['target_label']
        tgt_cat = record['target_category'] or 'N/A'
        count = record['count']
        print(f'  ({src_label}:{src_cat}) -[:CAUSES]-> ({tgt_label}:{tgt_cat}): {count}')
    
    print('\\n' + '=' * 80)
    print('6. 检查是否有孤立节点')
    print('=' * 80)
    
    query = \"\"\"
        MATCH (n:Term)
        WHERE NOT (n)-[]-()
        RETURN count(n) as isolated_count
    \"\"\"
    result = session.run(query)
    isolated = result.single()['isolated_count']
    
    result = session.run("MATCH (n:Term) RETURN count(n) as total")
    total = result.single()['total']
    
    print(f'孤立节点: {isolated} / {total} ({isolated/total*100:.1f}%)')
    
    print('\\n' + '=' * 80)
    print('7. 检查关系属性示例')
    print('=' * 80)
    
    query = \"\"\"
        MATCH (s)-[r:CAUSES]->(t)
        RETURN s.name as source, t.name as target,
               r.confidence as confidence,
               r.evidence as evidence,
               r.source as source_type
        LIMIT 3
    \"\"\"
    result = session.run(query)
    
    print('CAUSES关系示例:')
    for i, record in enumerate(result, 1):
        print(f'\\n{i}. {record["source"]} -[:CAUSES]-> {record["target"]}')
        print(f'   confidence: {record["confidence"]}')
        print(f'   evidence: {record["evidence"][:80]}...' if record["evidence"] and len(record["evidence"]) > 80 else f'   evidence: {record["evidence"]}')
        print(f'   source: {record["source_type"]}')

driver.close()
PYTHON_SCRIPT
"""
        
        stdin, stdout, stderr = ssh.exec_command(analyze_script)
        
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

