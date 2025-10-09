#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试条件导入
"""

import paramiko

SERVER_HOST = "47.108.152.16"
SERVER_USER = "root"
SERVER_PASSWORD = "Zxylsy.99"

def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(SERVER_HOST, username=SERVER_USER, password=SERVER_PASSWORD, timeout=30)
    
    print("=" * 80)
    print("测试条件导入")
    print("=" * 80)
    
    # 创建一个测试脚本来模拟main.py的导入
    test_script = '''
cd /opt/knowledge-graph/api
python3 << 'EOF'
import sys
sys.path.insert(0, '/opt/knowledge-graph/api')

print("开始测试导入...")

# 测试1: 直接导入
try:
    from models.relation_models import RelationInput, RelationBatch
    from services.kg_relation_service import KGRelationService
    from services.kg_query_service import KGQueryService
    print("✅ 所有导入成功")
except Exception as e:
    print(f"❌ 导入失败: {e}")
    import traceback
    traceback.print_exc()

# 测试2: 检查main.py是否能完整加载
print("\\n检查main.py加载...")
try:
    import importlib.util
    spec = importlib.util.spec_from_file_location("main_test", "/opt/knowledge-graph/api/main.py")
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        # 不执行，只检查能否加载
        print("✅ main.py可以加载")
        
        # 检查app对象
        if hasattr(module, '__file__'):
            print(f"   模块文件: {module.__file__}")
    else:
        print("❌ 无法创建模块规范")
except Exception as e:
    print(f"❌ 加载main.py失败: {e}")
    import traceback
    traceback.print_exc()

# 测试3: 检查FastAPI应用
print("\\n检查FastAPI应用...")
try:
    # 读取main.py并检查
    with open('/opt/knowledge-graph/api/main.py', 'r') as f:
        content = f.read()
    
    # 统计@app装饰器
    import re
    app_decorators = re.findall(r'@app\\.(get|post|put|delete|patch)\\("([^"]+)"\\)', content)
    print(f"   找到 {len(app_decorators)} 个路由装饰器")
    
    # 查找新路由
    new_routes = [r for r in app_decorators if 'relations/validate' in r[1] or 'diagnose' in r[1]]
    if new_routes:
        print(f"   ✅ 找到 {len(new_routes)} 个新路由:")
        for method, path in new_routes[:5]:
            print(f"      {method.upper()} {path}")
    else:
        print("   ❌ 未找到新路由")
        
except Exception as e:
    print(f"❌ 检查失败: {e}")

EOF
'''
    
    stdin, stdout, stderr = ssh.exec_command(test_script)
    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')
    
    print(output)
    if error:
        print("\n错误输出:")
        print(error)
    
    print("\n" + "=" * 80)
    
    ssh.close()

if __name__ == "__main__":
    main()

