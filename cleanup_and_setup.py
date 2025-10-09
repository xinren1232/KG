#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理数据并设置约束
"""

import paramiko
import sys

SERVER_HOST = "47.108.152.16"
SERVER_USER = "root"
SERVER_PASSWORD = "Zxylsy.99"

def main():
    """主函数"""
    print("=" * 80)
    print("清理数据并设置约束")
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

driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'password123'))

with driver.session() as session:
    # 1. 删除PLACEHOLDER关系
    print('1. 删除PLACEHOLDER关系...')
    result = session.run("MATCH ()-[r:PLACEHOLDER]->() DELETE r RETURN count(r) as deleted")
    deleted = result.single()['deleted']
    print(f'   删除了 {deleted} 个PLACEHOLDER关系')
    
    # 2. 创建唯一约束
    print('\\n2. 创建唯一约束...')
    try:
        session.run("CREATE CONSTRAINT term_uq IF NOT EXISTS FOR (t:Term) REQUIRE (t.name, t.category) IS UNIQUE")
        print('   ✅ Term节点唯一约束创建成功')
    except Exception as e:
        print(f'   ⚠️  {str(e)}')
    
    # 3. 验证
    print('\\n3. 验证结果...')
    result = session.run("MATCH (t:Term) RETURN count(t) as total")
    total = result.single()['total']
    print(f'   Term节点总数: {total}')
    
    result = session.run("MATCH ()-[r]->() RETURN type(r) as rel_type, count(*) as count ORDER BY count DESC")
    print('\\n   关系类型统计:')
    for record in result:
        print(f'   {record["rel_type"]:20s}: {record["count"]:6d}')

driver.close()
print('\\n✅ 完成')
'''
        
        # 上传脚本
        sftp = ssh.open_sftp()
        remote_script = '/opt/knowledge-graph/cleanup_setup.py'
        with sftp.open(remote_script, 'w') as f:
            f.write(script_content)
        sftp.close()
        print("✅ 脚本已上传\n")
        
        # 执行脚本
        print("=" * 80)
        print("执行清理和设置")
        print("=" * 80)
        
        stdin, stdout, stderr = ssh.exec_command(f'cd /opt/knowledge-graph && python3 cleanup_setup.py')
        
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

