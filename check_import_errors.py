#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查导入错误
"""

import paramiko
import time

SERVER_HOST = "47.108.152.16"
SERVER_USER = "root"
SERVER_PASSWORD = "Zxylsy.99"

def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(SERVER_HOST, username=SERVER_USER, password=SERVER_PASSWORD, timeout=30)
    
    print("=" * 80)
    print("检查导入错误")
    print("=" * 80)
    
    # 1. 测试导入main.py
    print("\n1. 测试导入main.py...")
    test_script = '''
cd /opt/knowledge-graph/api
python3 -c "
import sys
sys.path.insert(0, '/opt/knowledge-graph/api')

try:
    # 尝试导入main模块（不运行）
    import ast
    with open('main.py', 'r') as f:
        code = f.read()
    
    # 检查语法
    try:
        ast.parse(code)
        print('✅ main.py语法正确')
    except SyntaxError as e:
        print(f'❌ 语法错误: {e}')
    
    # 尝试导入依赖
    try:
        from models.relation_models import RelationInput, RelationBatch
        print('✅ 成功导入 relation_models')
    except Exception as e:
        print(f'❌ 导入 relation_models 失败: {e}')
    
    try:
        from services.kg_relation_service import KGRelationService
        print('✅ 成功导入 kg_relation_service')
    except Exception as e:
        print(f'❌ 导入 kg_relation_service 失败: {e}')
    
    try:
        from services.kg_query_service import KGQueryService
        print('✅ 成功导入 kg_query_service')
    except Exception as e:
        print(f'❌ 导入 kg_query_service 失败: {e}')
    
except Exception as e:
    print(f'❌ 错误: {e}')
    import traceback
    traceback.print_exc()
" 2>&1
'''
    
    stdin, stdout, stderr = ssh.exec_command(test_script)
    output = stdout.read().decode('utf-8')
    print(output)
    
    # 2. 杀死旧进程并重启
    print("\n2. 重启服务...")
    stdin, stdout, stderr = ssh.exec_command('killall -9 python3 2>/dev/null || true')
    time.sleep(2)
    
    stdin, stdout, stderr = ssh.exec_command('echo "" > /tmp/kg-api-debug.log')
    
    # 使用详细模式启动
    stdin, stdout, stderr = ssh.exec_command('cd /opt/knowledge-graph/api && python3 -v main.py > /tmp/kg-api-debug.log 2>&1 &')
    time.sleep(10)
    
    # 3. 检查详细日志
    print("\n3. 检查详细日志（最后100行）...")
    stdin, stdout, stderr = ssh.exec_command('tail -100 /tmp/kg-api-debug.log | grep -A 5 -B 5 "relation_models\\|kg_relation_service\\|kg_query_service\\|Error\\|Exception"')
    output = stdout.read().decode('utf-8')
    if output:
        print(output)
    else:
        print("   没有找到相关错误")
    
    # 4. 测试API
    print("\n4. 测试API端点...")
    stdin, stdout, stderr = ssh.exec_command('curl -s http://localhost:8000/kg/relations/stats')
    output = stdout.read().decode('utf-8')
    print(f"   /kg/relations/stats: {output[:100]}")
    
    # 5. 获取OpenAPI
    print("\n5. 检查OpenAPI规范...")
    stdin, stdout, stderr = ssh.exec_command('curl -s http://localhost:8000/openapi.json | python3 -c "import sys, json; data=json.load(sys.stdin); new_paths=[p for p in data.get(\'paths\', {}).keys() if \'relations/validate\' in p or \'diagnose\' in p]; print(\'找到新端点:\', new_paths) if new_paths else print(\'❌ 未找到新端点\')"')
    output = stdout.read().decode('utf-8')
    print(f"   {output}")
    
    print("\n" + "=" * 80)
    
    ssh.close()

if __name__ == "__main__":
    main()

