#!/usr/bin/env python3
"""修复图谱API超时问题"""

import os
import sys
import subprocess
import time

SERVER_IP = "47.108.152.16"
SERVER_USER = "root"
SERVER_PATH = "/opt/kg"

def run_ssh_command(command, show_output=True):
    """执行SSH命令"""
    ssh_cmd = f'ssh {SERVER_USER}@{SERVER_IP} "{command}"'
    print(f"\n执行命令: {command}")
    result = subprocess.run(ssh_cmd, shell=True, capture_output=True, text=True)
    if show_output:
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(f"错误: {result.stderr}")
    return result.returncode == 0

def upload_file(local_path, remote_path):
    """上传文件到服务器"""
    scp_cmd = f'scp "{local_path}" {SERVER_USER}@{SERVER_IP}:{remote_path}'
    print(f"\n上传文件: {local_path} -> {remote_path}")
    result = subprocess.run(scp_cmd, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print("✓ 上传成功")
        return True
    else:
        print(f"✗ 上传失败: {result.stderr}")
        return False

def main():
    print("="*70)
    print("修复图谱API超时问题")
    print("="*70)
    
    # 1. 上传修复后的前端文件
    print("\n步骤 1: 上传修复后的前端API配置")
    if not upload_file(
        "apps/web/src/api/index.js",
        f"{SERVER_PATH}/apps/web/src/api/index.js"
    ):
        print("上传前端文件失败")
        return False
    
    # 2. 上传修复后的后端文件
    print("\n步骤 2: 上传修复后的后端API")
    if not upload_file(
        "api/main.py",
        f"{SERVER_PATH}/api/main.py"
    ):
        print("上传后端文件失败")
        return False
    
    # 3. 重启前端服务
    print("\n步骤 3: 重新构建并重启前端服务")
    commands = [
        f"cd {SERVER_PATH}",
        "docker-compose -f docker-compose.prod.yml restart web"
    ]
    run_ssh_command(" && ".join(commands))
    
    # 4. 重启后端API服务
    print("\n步骤 4: 重启后端API服务")
    commands = [
        f"cd {SERVER_PATH}",
        "docker-compose -f docker-compose.prod.yml restart api"
    ]
    run_ssh_command(" && ".join(commands))
    
    # 5. 等待服务启动
    print("\n步骤 5: 等待服务启动...")
    time.sleep(10)
    
    # 6. 检查服务状态
    print("\n步骤 6: 检查服务状态")
    commands = [
        f"cd {SERVER_PATH}",
        "docker-compose -f docker-compose.prod.yml ps"
    ]
    run_ssh_command(" && ".join(commands))
    
    # 7. 查看API日志
    print("\n步骤 7: 查看API服务日志（最后20行）")
    commands = [
        f"cd {SERVER_PATH}",
        "docker-compose -f docker-compose.prod.yml logs api --tail=20"
    ]
    run_ssh_command(" && ".join(commands))
    
    print("\n" + "="*70)
    print("修复完成！")
    print("="*70)
    print("\n修复内容:")
    print("1. ✓ 前端axios超时时间从10秒增加到60秒")
    print("2. ✓ 后端修复了缓存逻辑bug")
    print("\n请在浏览器中测试:")
    print(f"  http://{SERVER_IP}/")
    print("\n如果仍有问题，请查看日志:")
    print(f"  ssh {SERVER_USER}@{SERVER_IP}")
    print(f"  cd {SERVER_PATH}")
    print("  docker-compose -f docker-compose.prod.yml logs -f api")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n操作已取消")
        sys.exit(1)
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

