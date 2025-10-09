#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
补充剩余3个缺少描述的术语
"""

import paramiko
import sys

SERVER_HOST = "47.108.152.16"
SERVER_USER = "root"
SERVER_PASSWORD = "Zxylsy.99"

def main():
    """主函数"""
    print("=" * 80)
    print("补充剩余缺少描述的术语")
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
        
        # 执行补充脚本
        fix_script = """
cd /opt/knowledge-graph && python3 << 'PYTHON_SCRIPT'
from neo4j import GraphDatabase

driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'password123'))

# 补充描述
descriptions = {
    "可靠性测试": "对产品进行可靠性验证的测试活动，包括环境测试、寿命测试、压力测试等，以确保产品在规定条件下能够稳定可靠地工作",
    "来料检验": "对供应商提供的原材料、零部件、组件等进行质量检验的过程，确保来料符合质量标准和技术要求",
    "环境测试": "模拟产品在实际使用环境中可能遇到的各种环境条件（如温度、湿度、振动、跌落等）进行的测试，验证产品的环境适应性"
}

# 标签映射
tags_mapping = {
    "可靠性测试": ["可靠性", "测试", "质量保证"],
    "来料检验": ["质量管理", "检验", "供应链"],
    "环境测试": ["可靠性", "测试", "环境"]
}

with driver.session() as session:
    for name, description in descriptions.items():
        # 更新描述
        session.run('''
            MATCH (t:Term {name: $name})
            SET t.description = $description,
                t.updated_at = datetime()
        ''', name=name, description=description)
        
        # 添加标签
        for tag in tags_mapping[name]:
            # 创建或获取Tag节点
            session.run('''
                MERGE (g:Tag {name: $tag})
                ON CREATE SET g.created_at = datetime()
            ''', tag=tag)
            
            # 创建HAS_TAG关系
            session.run('''
                MATCH (t:Term {name: $name})
                MATCH (g:Tag {name: $tag})
                MERGE (t)-[r:HAS_TAG]->(g)
                ON CREATE SET r.created_at = datetime()
            ''', name=name, tag=tag)
        
        print(f'✅ 已补充: {name}')
        print(f'   描述: {description[:60]}...')
        print(f'   标签: {", ".join(tags_mapping[name])}')
        print()

# 验证
print('=' * 80)
print('验证补充结果')
print('=' * 80)

with driver.session() as session:
    result = session.run('''
        MATCH (t:Term)
        WHERE t.description IS NULL OR t.description = ''
        RETURN count(t) as count
    ''')
    no_desc_count = result.single()['count']
    
    result = session.run('''
        MATCH (t:Term)
        WHERE NOT (t)-[:HAS_TAG]->(:Tag)
        RETURN count(t) as count
    ''')
    no_tags_count = result.single()['count']
    
    result = session.run('''
        MATCH (t:Term)
        RETURN count(t) as total
    ''')
    total = result.single()['total']
    
    print(f'总术语数: {total}')
    print(f'缺少描述: {no_desc_count} ({no_desc_count/total*100:.1f}%)')
    print(f'缺少标签: {no_tags_count} ({no_tags_count/total*100:.1f}%)')
    print()
    
    if no_desc_count == 0:
        print('🎉 所有术语都有描述了！')
    if no_tags_count == 0:
        print('🎉 所有术语都有标签了！')

driver.close()
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
        
        print("\n" + "=" * 80)
        print("✅ 补充完成！")
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

