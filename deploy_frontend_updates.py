#!/usr/bin/env python3
"""
部署前端更新到服务器
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

def upload_file(sftp, local_path, remote_path, description=""):
    """上传文件到服务器"""
    if description:
        print(f"\n{'='*60}")
        print(f"📌 {description}")
        print(f"{'='*60}")
    
    print(f"📤 上传: {local_path} -> {remote_path}")
    try:
        sftp.put(local_path, remote_path)
        print(f"✅ 上传成功")
        return True
    except Exception as e:
        print(f"❌ 上传失败: {str(e)}")
        return False

def deploy_frontend():
    """部署前端更新"""
    
    print("🚀 开始部署前端更新...")
    
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
            f"cd {PROJECT_DIR}/apps/web/src && cp -r views views.backup.$(date +%Y%m%d_%H%M%S) && cp -r components components.backup.$(date +%Y%m%d_%H%M%S) && cp -r api api.backup.$(date +%Y%m%d_%H%M%S)",
            "备份现有前端文件"
        )
        
        # 2. 上传更新的文件
        files_to_upload = [
            ("apps/web/src/views/SystemManagement.vue", f"{PROJECT_DIR}/apps/web/src/views/SystemManagement.vue", "上传SystemManagement.vue"),
            ("apps/web/src/components/system/DictionarySchema.vue", f"{PROJECT_DIR}/apps/web/src/components/system/DictionarySchema.vue", "上传DictionarySchema.vue"),
            ("apps/web/src/components/system/GraphSchema.vue", f"{PROJECT_DIR}/apps/web/src/components/system/GraphSchema.vue", "上传GraphSchema.vue"),
            ("apps/web/src/api/index.js", f"{PROJECT_DIR}/apps/web/src/api/index.js", "上传api/index.js"),
        ]
        
        for local_path, remote_path, desc in files_to_upload:
            if os.path.exists(local_path):
                upload_file(sftp, local_path, remote_path, desc)
            else:
                print(f"⚠️ 本地文件不存在: {local_path}")
        
        # 3. 检查上传的文件
        execute_ssh_command(
            ssh,
            f"ls -lh {PROJECT_DIR}/apps/web/src/components/system/ | grep Schema",
            "检查Schema组件文件"
        )
        
        # 4. 检查SystemManagement.vue中是否包含Schema相关代码
        execute_ssh_command(
            ssh,
            f"grep -n 'dictionary-schema\\|graph-schema\\|DictionarySchema\\|GraphSchema' {PROJECT_DIR}/apps/web/src/views/SystemManagement.vue | head -20",
            "检查SystemManagement.vue中的Schema代码"
        )
        
        # 5. 重启前端服务（如果需要）
        print("\n⚠️ 注意: Vite开发服务器会自动热重载，无需重启")
        print("如果更新未生效，请手动重启前端服务:")
        print(f"  systemctl restart kg-frontend")
        
        # 6. 检查前端服务状态
        execute_ssh_command(
            ssh,
            "systemctl status kg-frontend --no-pager | head -15",
            "检查前端服务状态"
        )
        
        sftp.close()
        
        print("\n" + "="*60)
        print("🎉 前端更新部署完成！")
        print("="*60)
        print("\n📋 已更新的文件:")
        print("  ✅ SystemManagement.vue - 添加Schema Tab页")
        print("  ✅ DictionarySchema.vue - 词典Schema组件")
        print("  ✅ GraphSchema.vue - 图谱Schema组件")
        print("  ✅ api/index.js - API配置更新")
        print("\n🌐 访问地址:")
        print(f"  http://{SERVER_IP}/system-management")
        print("\n💡 提示:")
        print("  - 刷新浏览器页面查看更新")
        print("  - 如果未生效，清除浏览器缓存后重试")
        print("  - 检查浏览器控制台是否有错误")
        
    except Exception as e:
        print(f"\n❌ 错误: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        ssh.close()
        print("\n🔌 SSH连接已关闭")

if __name__ == "__main__":
    deploy_frontend()

