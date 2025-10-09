#!/usr/bin/env python3
"""
上传更新后的VersionsManagement组件
"""

import paramiko
import os

# 服务器配置
SERVER_IP = "47.108.152.16"
USERNAME = "root"
PASSWORD = "Zxylsy.99"
PROJECT_DIR = "/opt/knowledge-graph"

def execute_ssh_command(ssh, command, description=""):
    """执行SSH命令并返回结果"""
    if description:
        print(f"\n{'='*60}")
        print(f"📌 {description}")
        print(f"{'='*60}")
    
    print(f"💻 执行命令: {command}")
    stdin, stdout, stderr = ssh.exec_command(command)
    
    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')
    
    if output:
        print(f"✅ 输出:\n{output}")
    if error and "warning" not in error.lower():
        print(f"⚠️ 错误:\n{error}")
    
    return output, error

def upload_versions_component():
    """上传VersionsManagement组件"""
    
    print("🚀 开始上传VersionsManagement组件...")
    
    # 创建SSH客户端
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # 连接服务器
        print(f"\n🔗 连接服务器 {SERVER_IP}...")
        ssh.connect(SERVER_IP, username=USERNAME, password=PASSWORD)
        print("✅ 连接成功！")
        
        # 创建SFTP客户端
        sftp = ssh.open_sftp()
        
        # 1. 备份现有文件
        execute_ssh_command(
            ssh,
            f"cp {PROJECT_DIR}/apps/web/src/components/system/VersionsManagement.vue {PROJECT_DIR}/apps/web/src/components/system/VersionsManagement.vue.backup.$(date +%Y%m%d_%H%M%S)",
            "备份VersionsManagement.vue"
        )
        
        # 2. 上传更新的文件
        local_path = "apps/web/src/components/system/VersionsManagement.vue"
        remote_path = f"{PROJECT_DIR}/apps/web/src/components/system/VersionsManagement.vue"
        
        if os.path.exists(local_path):
            print(f"\n📤 上传: {local_path} -> {remote_path}")
            sftp.put(local_path, remote_path)
            print(f"✅ 上传成功")
        else:
            print(f"⚠️ 本地文件不存在: {local_path}")
        
        # 3. 检查文件
        execute_ssh_command(
            ssh,
            f"ls -lh {PROJECT_DIR}/apps/web/src/components/system/VersionsManagement.vue",
            "检查文件"
        )
        
        # 4. 检查版本信息
        execute_ssh_command(
            ssh,
            f"grep -A 5 'v1.3.0' {PROJECT_DIR}/apps/web/src/components/system/VersionsManagement.vue | head -10",
            "检查v1.3.0版本信息"
        )
        
        sftp.close()
        
        print("\n" + "="*60)
        print("🎉 VersionsManagement组件上传完成！")
        print("="*60)
        print("\n📋 更新内容:")
        print("  ✅ v1.3.0 - Schema管理与系统优化")
        print("  ✅ v1.2.1 - 图谱超时问题修复")
        print("  ✅ 更新所有版本的时间为2025年")
        print("\n🌐 访问地址:")
        print(f"  http://{SERVER_IP}/system-management")
        print("\n💡 提示:")
        print("  - 刷新浏览器页面查看更新")
        print("  - 点击「版本管理」Tab查看最新版本")
        
    except Exception as e:
        print(f"\n❌ 错误: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        ssh.close()
        print("\n🔌 SSH连接已关闭")

if __name__ == "__main__":
    upload_versions_component()

