#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
部署API更新到服务器
"""

import paramiko
import sys
import os

SERVER_HOST = "47.108.152.16"
SERVER_USER = "root"
SERVER_PASSWORD = "Zxylsy.99"
REMOTE_DIR = "/opt/knowledge-graph/api"

def main():
    """主函数"""
    print("=" * 80)
    print("部署API更新到服务器")
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
        
        # 创建SFTP客户端
        sftp = ssh.open_sftp()
        
        # 1. 创建目录
        print("=" * 80)
        print("1. 创建目录结构")
        print("=" * 80)
        
        directories = [
            f"{REMOTE_DIR}/models",
            f"{REMOTE_DIR}/services"
        ]
        
        for directory in directories:
            try:
                sftp.stat(directory)
                print(f"✅ 目录已存在: {directory}")
            except FileNotFoundError:
                sftp.mkdir(directory)
                print(f"✅ 创建目录: {directory}")
        
        # 2. 上传文件
        print("\n" + "=" * 80)
        print("2. 上传文件")
        print("=" * 80)
        
        files_to_upload = [
            ("api/models/relation_models.py", f"{REMOTE_DIR}/models/relation_models.py"),
            ("api/services/kg_relation_service.py", f"{REMOTE_DIR}/services/kg_relation_service.py"),
            ("api/services/kg_query_service.py", f"{REMOTE_DIR}/services/kg_query_service.py"),
            ("api/main.py", f"{REMOTE_DIR}/main.py")
        ]
        
        for local_file, remote_file in files_to_upload:
            if os.path.exists(local_file):
                sftp.put(local_file, remote_file)
                print(f"✅ 上传: {local_file} -> {remote_file}")
            else:
                print(f"⚠️  文件不存在: {local_file}")
        
        # 创建__init__.py文件
        print("\n创建__init__.py文件...")
        for directory in ["models", "services"]:
            init_file = f"{REMOTE_DIR}/{directory}/__init__.py"
            with sftp.open(init_file, 'w') as f:
                f.write("")
            print(f"✅ 创建: {init_file}")
        
        sftp.close()
        
        # 3. 重启API服务
        print("\n" + "=" * 80)
        print("3. 重启API服务")
        print("=" * 80)
        
        # 检查服务状态
        stdin, stdout, stderr = ssh.exec_command("pm2 list")
        output = stdout.read().decode('utf-8')
        print("当前PM2服务:")
        print(output)
        
        # 重启服务
        print("\n重启API服务...")
        stdin, stdout, stderr = ssh.exec_command("cd /opt/knowledge-graph/api && pm2 restart kg-api || pm2 start main.py --name kg-api --interpreter python3")
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        
        if output:
            print(output)
        if error:
            print(f"错误: {error}")
        
        # 等待服务启动
        print("\n等待服务启动...")
        import time
        time.sleep(3)
        
        # 检查服务状态
        stdin, stdout, stderr = ssh.exec_command("pm2 list")
        output = stdout.read().decode('utf-8')
        print("\n服务状态:")
        print(output)
        
        # 4. 测试API
        print("\n" + "=" * 80)
        print("4. 测试API")
        print("=" * 80)
        
        stdin, stdout, stderr = ssh.exec_command("curl -s http://localhost:8000/")
        output = stdout.read().decode('utf-8')
        print(f"API根路径响应: {output}")
        
        print("\n" + "=" * 80)
        print("✅ 部署完成")
        print("=" * 80)
        print("\n新增API端点:")
        print("  - POST /kg/relations/validate - 验证关系数据")
        print("  - POST /kg/relations/import - 批量导入关系")
        print("  - GET  /kg/relations/stats - 获取关系统计")
        print("  - GET  /kg/diagnose - 故障诊断")
        print("  - GET  /kg/prevent - 获取预防措施")
        print("  - GET  /kg/test-path - 获取测试路径")
        print("  - GET  /kg/dependencies - 获取组件依赖")
        print("\n可以运行 python test_new_apis.py 进行测试")
        
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

