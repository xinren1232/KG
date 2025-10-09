#!/usr/bin/env python3
"""
更新服务器前端代码
"""
import paramiko
import os
import sys
from pathlib import Path

# 服务器配置
SERVER_HOST = "47.108.152.16"
SERVER_USER = "root"
SERVER_PASSWORD = "Zxylsy.99"
SERVER_PATH = "/var/www/html"

# 本地文件路径
LOCAL_FILES = [
    ("apps/web/src/api/index.js", "/var/www/html/src/api/index.js"),
    ("apps/web/src/views/GraphVisualization.vue", "/var/www/html/src/views/GraphVisualization.vue")
]

def upload_files():
    """上传文件到服务器"""
    try:
        # 创建SSH客户端
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        print("📡 连接服务器...")
        ssh.connect(SERVER_HOST, username=SERVER_USER, password=SERVER_PASSWORD)
        
        # 创建SFTP客户端
        sftp = ssh.open_sftp()
        
        for local_file, remote_file in LOCAL_FILES:
            if os.path.exists(local_file):
                print(f"📤 上传 {local_file} -> {remote_file}")
                
                # 确保远程目录存在
                remote_dir = os.path.dirname(remote_file)
                try:
                    sftp.stat(remote_dir)
                except FileNotFoundError:
                    # 创建目录
                    ssh.exec_command(f"mkdir -p {remote_dir}")
                
                # 上传文件
                sftp.put(local_file, remote_file)
                print(f"✅ {local_file} 上传成功")
            else:
                print(f"❌ 本地文件不存在: {local_file}")
        
        # 重启前端服务（如果有的话）
        print("🔄 重启前端服务...")
        stdin, stdout, stderr = ssh.exec_command("cd /var/www/html && npm run build")
        build_output = stdout.read().decode()
        build_error = stderr.read().decode()
        
        if build_error:
            print(f"⚠️ 构建警告: {build_error}")
        
        print("✅ 前端代码更新完成")
        
        sftp.close()
        ssh.close()
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 更新服务器前端代码")
    print("=" * 60)
    
    success = upload_files()
    
    if success:
        print("\n🎉 更新完成！")
        print("🌐 请访问: http://47.108.152.16 查看效果")
    else:
        print("\n❌ 更新失败")
        sys.exit(1)
