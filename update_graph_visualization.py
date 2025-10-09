#!/usr/bin/env python3
"""
快速更新服务器上的图谱可视化组件
"""
import paramiko
import os
import sys

# 服务器配置
SERVER_CONFIG = {
    'hostname': '47.97.161.175',
    'port': 22,
    'username': 'root',
    'password': 'Aa112211'
}

def upload_file(ssh_client, local_path, remote_path):
    """上传文件到服务器"""
    try:
        sftp = ssh_client.open_sftp()
        print(f"📤 上传文件: {local_path} -> {remote_path}")
        sftp.put(local_path, remote_path)
        sftp.close()
        print(f"✅ 上传成功")
        return True
    except Exception as e:
        print(f"❌ 上传失败: {e}")
        return False

def execute_command(ssh_client, command, description=""):
    """执行SSH命令"""
    try:
        if description:
            print(f"\n🔧 {description}")
        print(f"执行命令: {command}")
        
        stdin, stdout, stderr = ssh_client.exec_command(command)
        exit_status = stdout.channel.recv_exit_status()
        
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        
        if output:
            print(f"输出:\n{output}")
        if error and exit_status != 0:
            print(f"错误:\n{error}")
            
        return exit_status == 0
    except Exception as e:
        print(f"❌ 命令执行失败: {e}")
        return False

def main():
    print("=" * 60)
    print("🚀 更新服务器图谱可视化组件")
    print("=" * 60)
    
    # 连接服务器
    print("\n📡 连接服务器...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(**SERVER_CONFIG)
        print("✅ 服务器连接成功")
        
        # 1. 上传GraphVisualization.vue
        local_file = "apps/web/src/views/GraphVisualization.vue"
        remote_file = "/root/KG/apps/web/src/views/GraphVisualization.vue"
        
        if not os.path.exists(local_file):
            print(f"❌ 本地文件不存在: {local_file}")
            return False
            
        if not upload_file(ssh, local_file, remote_file):
            return False
        
        # 2. 重新构建前端
        print("\n" + "=" * 60)
        print("🔨 重新构建前端...")
        print("=" * 60)
        
        commands = [
            ("cd /root/KG/apps/web && npm run build", "构建前端项目"),
        ]
        
        for cmd, desc in commands:
            if not execute_command(ssh, cmd, desc):
                print(f"❌ {desc}失败")
                return False
        
        # 3. 重启前端服务
        print("\n" + "=" * 60)
        print("🔄 重启前端服务...")
        print("=" * 60)
        
        restart_commands = [
            ("systemctl restart kg-frontend", "重启前端服务"),
            ("systemctl status kg-frontend --no-pager", "检查服务状态"),
        ]
        
        for cmd, desc in restart_commands:
            execute_command(ssh, cmd, desc)
        
        print("\n" + "=" * 60)
        print("✅ 更新完成！")
        print("=" * 60)
        print("\n请访问: http://47.97.161.175:5173")
        print("检查图谱可视化是否显示正确的颜色和标签")
        
        return True
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False
    finally:
        ssh.close()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

