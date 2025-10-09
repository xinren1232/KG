#!/usr/bin/env python3
"""
部署API修复到服务器
修复前端API导入问题和后端词典统计端点
"""
import paramiko
import os
from pathlib import Path

# 服务器配置
SERVER_IP = "47.108.152.16"
SERVER_USER = "root"
SERVER_PASSWORD = "Zxylsy.99"  # 直接使用密码
PROJECT_DIR = "/opt/knowledge-graph"

def deploy_fixes():
    """部署修复"""
    print("开始部署API修复...")

    # 连接服务器
    print(f"\n连接服务器 {SERVER_IP}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(SERVER_IP, username=SERVER_USER, password=SERVER_PASSWORD)
    print("连接成功！")
    
    sftp = ssh.open_sftp()
    
    try:
        # 1. 备份当前文件
        print("\n" + "="*60)
        print("1. 备份当前文件")
        print("="*60)
        
        backup_commands = [
            f"cp {PROJECT_DIR}/apps/web/src/api/index.js {PROJECT_DIR}/apps/web/src/api/index.js.backup",
            f"cp {PROJECT_DIR}/api/main.py {PROJECT_DIR}/api/main.py.backup"
        ]
        
        for cmd in backup_commands:
            stdin, stdout, stderr = ssh.exec_command(cmd)
            print(f"执行: {cmd}")
        
        # 2. 上传修复后的文件
        print("\n" + "="*60)
        print("2. 上传修复后的文件")
        print("="*60)
        
        # 上传文件列表
        files_to_upload = [
            ("apps/web/src/api/index.js", f"{PROJECT_DIR}/apps/web/src/api/index.js", "前端API文件"),
            ("api/main.py", f"{PROJECT_DIR}/api/main.py", "后端main.py"),
            ("apps/web/src/components/system/DictionarySchema.vue", f"{PROJECT_DIR}/apps/web/src/components/system/DictionarySchema.vue", "DictionarySchema.vue"),
            ("apps/web/src/components/system/GraphSchema.vue", f"{PROJECT_DIR}/apps/web/src/components/system/GraphSchema.vue", "GraphSchema.vue"),
            ("apps/web/src/views/SystemManagement.vue", f"{PROJECT_DIR}/apps/web/src/views/SystemManagement.vue", "SystemManagement.vue"),
            ("apps/web/src/views/DictionaryManagement.vue", f"{PROJECT_DIR}/apps/web/src/views/DictionaryManagement.vue", "DictionaryManagement.vue"),
            ("apps/web/src/views/GraphVisualization.vue", f"{PROJECT_DIR}/apps/web/src/views/GraphVisualization.vue", "GraphVisualization.vue"),
        ]

        for local_file, remote_file, description in files_to_upload:
            if os.path.exists(local_file):
                print(f"上传 {local_file} -> {remote_file}")
                sftp.put(local_file, remote_file)
                print(f"✓ {description}上传成功")
            else:
                print(f"⚠ 警告: {local_file} 不存在，跳过")

        
        # 3. 重新构建前端
        print("\n" + "="*60)
        print("3. 重新构建前端")
        print("="*60)
        
        build_commands = f"""
cd {PROJECT_DIR}/apps/web
npm run build
"""
        
        stdin, stdout, stderr = ssh.exec_command(build_commands)
        stdout.channel.recv_exit_status()  # 等待命令完成
        
        output = stdout.read().decode()
        error = stderr.read().decode()
        
        if error and "error" in error.lower():
            print(f"构建错误: {error}")
        else:
            print("✓ 前端构建成功")
            if output:
                print(output[-500:])  # 显示最后500字符
        
        # 4. 重启服务
        print("\n" + "="*60)
        print("4. 重启服务")
        print("="*60)
        
        restart_commands = [
            "systemctl restart kg-api",
            "systemctl restart kg-frontend"
        ]
        
        for cmd in restart_commands:
            stdin, stdout, stderr = ssh.exec_command(cmd)
            stdout.channel.recv_exit_status()
            print(f"✓ 执行: {cmd}")
        
        # 等待服务启动
        import time
        print("\n等待服务启动（5秒）...")
        time.sleep(5)
        
        # 5. 验证服务状态
        print("\n" + "="*60)
        print("5. 验证服务状态")
        print("="*60)
        
        status_commands = [
            "systemctl status kg-api --no-pager -l | head -20",
            "systemctl status kg-frontend --no-pager -l | head -20"
        ]
        
        for cmd in status_commands:
            stdin, stdout, stderr = ssh.exec_command(cmd)
            output = stdout.read().decode()
            print(f"\n{cmd}:")
            print(output)
        
        # 6. 测试API端点
        print("\n" + "="*60)
        print("6. 测试API端点")
        print("="*60)
        
        test_commands = [
            "curl -s http://localhost/api/kg/dictionary/stats | python3 -m json.tool | head -20",
            "curl -s http://localhost/api/kg/dictionary/categories | python3 -m json.tool | head -30"
        ]
        
        for cmd in test_commands:
            stdin, stdout, stderr = ssh.exec_command(cmd)
            output = stdout.read().decode()
            print(f"\n{cmd}:")
            print(output)
        
        # 7. 检查前端文件
        print("\n" + "="*60)
        print("7. 检查前端构建文件")
        print("="*60)
        
        check_cmd = f"ls -lh {PROJECT_DIR}/apps/web/dist/assets/*.js | head -5"
        stdin, stdout, stderr = ssh.exec_command(check_cmd)
        output = stdout.read().decode()
        print(output)
        
        print("\n" + "="*60)
        print("部署完成！")
        print("="*60)
        print("\n请访问以下URL验证修复效果：")
        print(f"  - 前端: http://{SERVER_IP}")
        print(f"  - 词典统计API: http://{SERVER_IP}/api/kg/dictionary/stats")
        print(f"  - 词典分类API: http://{SERVER_IP}/api/kg/dictionary/categories")
        print("\n在浏览器中打开系统管理页面，查看「词典Schema」和「图谱Schema」标签页")
        
    except Exception as e:
        print(f"\n❌ 部署失败: {e}")
        import traceback
        traceback.print_exc()
    finally:
        sftp.close()
        ssh.close()
        print("\nSSH连接已关闭")

if __name__ == "__main__":
    deploy_fixes()

