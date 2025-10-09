#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查API端点
"""

import paramiko
import json

SERVER_HOST = "47.108.152.16"
SERVER_USER = "root"
SERVER_PASSWORD = "Zxylsy.99"

def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(SERVER_HOST, username=SERVER_USER, password=SERVER_PASSWORD, timeout=30)
    
    print("获取OpenAPI规范...")
    stdin, stdout, stderr = ssh.exec_command('curl -s http://localhost:8000/openapi.json')
    output = stdout.read().decode('utf-8')
    
    try:
        openapi = json.loads(output)
        paths = openapi.get('paths', {})
        
        print(f"\n总共 {len(paths)} 个端点:\n")
        
        # 查找新的端点
        new_endpoints = [
            '/kg/relations/validate',
            '/kg/relations/import',
            '/kg/relations/stats',
            '/kg/diagnose',
            '/kg/prevent',
            '/kg/test-path',
            '/kg/dependencies'
        ]
        
        print("检查新端点:")
        for endpoint in new_endpoints:
            if endpoint in paths:
                print(f"  ✅ {endpoint}")
            else:
                print(f"  ❌ {endpoint} - 未找到")
        
        print("\n所有/kg/开头的端点:")
        kg_endpoints = [p for p in sorted(paths.keys()) if p.startswith('/kg/')]
        for endpoint in kg_endpoints:
            methods = list(paths[endpoint].keys())
            print(f"  {endpoint}: {methods}")
        
    except json.JSONDecodeError as e:
        print(f"解析JSON失败: {e}")
        print(f"输出: {output[:500]}")
    
    ssh.close()

if __name__ == "__main__":
    main()

