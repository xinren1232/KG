#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查词典数据完整性
"""

import paramiko
import sys

SERVER_HOST = "47.108.152.16"
SERVER_USER = "root"
SERVER_PASSWORD = "Zxylsy.99"
PROJECT_DIR = "/opt/knowledge-graph"

def main():
    """主函数"""
    print("=" * 80)
    print("词典数据完整性检查")
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
        
        # 执行检查脚本
        check_script = """
cd /opt/knowledge-graph && python3 << 'PYTHON_SCRIPT'
from neo4j import GraphDatabase

driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'password123'))

with driver.session() as session:
    print('=' * 80)
    print('1. 检查缺少描述的术语')
    print('=' * 80)
    result = session.run('''
        MATCH (t:Term)
        WHERE t.description IS NULL OR t.description = ''
        RETURN t.name as name, t.category as category
        ORDER BY t.name
        LIMIT 20
    ''')
    no_desc = list(result)
    
    # 统计总数
    result = session.run('''
        MATCH (t:Term)
        WHERE t.description IS NULL OR t.description = ''
        RETURN count(t) as count
    ''')
    no_desc_count = result.single()['count']
    
    print(f'缺少描述的术语总数: {no_desc_count}')
    if no_desc:
        print('\\n前20个示例:')
        for i, record in enumerate(no_desc, 1):
            cat = record['category'] or '(无分类)'
            print(f'  {i:2d}. {record["name"]:40s} - {cat}')
    
    print('\\n' + '=' * 80)
    print('2. 检查缺少分类的术语')
    print('=' * 80)
    result = session.run('''
        MATCH (t:Term)
        WHERE t.category IS NULL OR t.category = ''
        RETURN t.name as name
        LIMIT 20
    ''')
    no_category = list(result)
    
    result = session.run('''
        MATCH (t:Term)
        WHERE t.category IS NULL OR t.category = ''
        RETURN count(t) as count
    ''')
    no_category_count = result.single()['count']
    
    print(f'缺少分类的术语总数: {no_category_count}')
    if no_category:
        print('\\n前20个示例:')
        for i, record in enumerate(no_category, 1):
            print(f'  {i:2d}. {record["name"]}')
    
    print('\\n' + '=' * 80)
    print('3. 检查没有标签的术语')
    print('=' * 80)
    result = session.run('''
        MATCH (t:Term)
        WHERE NOT (t)-[:HAS_TAG]->(:Tag)
        RETURN t.name as name, t.category as category
        ORDER BY t.name
        LIMIT 20
    ''')
    no_tags = list(result)
    
    result = session.run('''
        MATCH (t:Term)
        WHERE NOT (t)-[:HAS_TAG]->(:Tag)
        RETURN count(t) as count
    ''')
    no_tags_count = result.single()['count']
    
    print(f'没有标签的术语总数: {no_tags_count}')
    if no_tags:
        print('\\n前20个示例:')
        for i, record in enumerate(no_tags, 1):
            cat = record['category'] or '(无分类)'
            print(f'  {i:2d}. {record["name"]:40s} - {cat}')
    
    print('\\n' + '=' * 80)
    print('4. 检查没有别名的术语')
    print('=' * 80)
    result = session.run('''
        MATCH (t:Term)
        WHERE NOT (t)<-[:ALIAS_OF]-(:Alias)
        RETURN count(t) as count
    ''')
    no_aliases_count = result.single()['count']
    print(f'没有别名的术语总数: {no_aliases_count}')
    
    print('\\n' + '=' * 80)
    print('5. 数据完整性统计')
    print('=' * 80)
    result = session.run('''
        MATCH (t:Term)
        RETURN 
            count(t) as total,
            sum(CASE WHEN t.description IS NOT NULL AND t.description <> '' THEN 1 ELSE 0 END) as has_valid_desc,
            sum(CASE WHEN t.category IS NOT NULL AND t.category <> '' THEN 1 ELSE 0 END) as has_valid_category
    ''')
    stats = result.single()
    total = stats['total']
    has_valid_desc = stats['has_valid_desc']
    has_valid_category = stats['has_valid_category']
    
    print(f'总术语数: {total}')
    print(f'有效描述(非空): {has_valid_desc} ({has_valid_desc/total*100:.1f}%)')
    print(f'有效分类(非空): {has_valid_category} ({has_valid_category/total*100:.1f}%)')
    print(f'缺少描述: {total - has_valid_desc} ({(total - has_valid_desc)/total*100:.1f}%)')
    print(f'缺少分类: {total - has_valid_category} ({(total - has_valid_category)/total*100:.1f}%)')
    
    print('\\n' + '=' * 80)
    print('6. 检查因果关系导入的节点')
    print('=' * 80)
    result = session.run('''
        MATCH (t:Term)
        WHERE t.source = 'causal_relationship_import'
        RETURN t.name as name, t.description as description, t.category as category
        ORDER BY t.name
        LIMIT 10
    ''')
    causal_nodes = list(result)
    
    result = session.run('''
        MATCH (t:Term)
        WHERE t.source = 'causal_relationship_import'
        RETURN count(t) as count
    ''')
    causal_count = result.single()['count']
    
    print(f'因果关系导入的节点总数: {causal_count}')
    if causal_nodes:
        print('\\n前10个示例:')
        for i, record in enumerate(causal_nodes, 1):
            desc = record['description'] or '(无描述)'
            cat = record['category'] or '(无分类)'
            print(f'\\n  {i:2d}. {record["name"]}')
            print(f'      分类: {cat}')
            if len(desc) > 80:
                print(f'      描述: {desc[:80]}...')
            else:
                print(f'      描述: {desc}')
    
    print('\\n' + '=' * 80)
    print('7. 按分类统计数据完整性')
    print('=' * 80)
    result = session.run('''
        MATCH (t:Term)
        WHERE t.category IS NOT NULL AND t.category <> ''
        WITH t.category as category, 
             count(t) as total,
             sum(CASE WHEN t.description IS NOT NULL AND t.description <> '' THEN 1 ELSE 0 END) as has_desc
        RETURN category, total, has_desc, total - has_desc as no_desc
        ORDER BY no_desc DESC, total DESC
    ''')
    
    print(f'{"分类":20s} {"总数":>8s} {"有描述":>8s} {"无描述":>8s} {"完整率":>8s}')
    print('-' * 80)
    for record in result:
        category = record['category']
        total = record['total']
        has_desc = record['has_desc']
        no_desc = record['no_desc']
        completeness = has_desc / total * 100 if total > 0 else 0
        print(f'{category:20s} {total:8d} {has_desc:8d} {no_desc:8d} {completeness:7.1f}%')

driver.close()
print('\\n' + '=' * 80)
print('检查完成')
print('=' * 80)
PYTHON_SCRIPT
"""
        
        stdin, stdout, stderr = ssh.exec_command(check_script)
        
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

