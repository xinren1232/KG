#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试main.py导入
"""

import paramiko

SERVER_HOST = "47.108.152.16"
SERVER_USER = "root"
SERVER_PASSWORD = "Zxylsy.99"

def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(SERVER_HOST, username=SERVER_USER, password=SERVER_PASSWORD, timeout=30)
    
    print("测试main.py导入...")
    test_script = '''
cd /opt/knowledge-graph/api
python3 << 'EOF'
import sys
sys.path.insert(0, '/opt/knowledge-graph/api')

try:
    # 测试导入
    from models.relation_models import RelationInput, RelationBatch
    from services.kg_relation_service import KGRelationService
    from services.kg_query_service import KGQueryService
    print("✅ 所有导入成功")
    
    # 检查main.py中的路由
    import importlib.util
    spec = importlib.util.spec_from_file_location("main", "/opt/knowledge-graph/api/main.py")
    main_module = importlib.util.module_from_spec(spec)
    
    # 不执行，只检查语法
    with open('/opt/knowledge-graph/api/main.py', 'r') as f:
        content = f.read()
        if '/kg/relations/validate' in content:
            print("✅ main.py包含 /kg/relations/validate")
        if '/kg/diagnose' in content:
            print("✅ main.py包含 /kg/diagnose")
        
        # 统计@app装饰器
        import re
        routes = re.findall(r'@app\.(get|post|put|delete|patch)\("([^"]+)"\)', content)
        print(f"\\n找到 {len(routes)} 个路由:")
        
        # 查找新路由
        new_routes = [r for r in routes if 'relations' in r[1] or 'diagnose' in r[1] or 'prevent' in r[1] or 'test-path' in r[1] or 'dependencies' in r[1]]
        if new_routes:
            print("\\n新路由:")
            for method, path in new_routes:
                print(f"  {method.upper()} {path}")
        else:
            print("\\n❌ 未找到新路由")
        
except Exception as e:
    print(f"❌ 错误: {e}")
    import traceback
    traceback.print_exc()
EOF
'''
    
    stdin, stdout, stderr = ssh.exec_command(test_script)
    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')
    
    print(output)
    if error:
        print("\n错误:")
        print(error)
    
    ssh.close()

if __name__ == "__main__":
    main()

