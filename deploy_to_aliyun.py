#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
阿里云服务器自动部署脚本
用于构建前端并部署到阿里云服务器
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import json

# 配置
SERVER_IP = "47.108.152.16"
SERVER_USER = "root"
SERVER_PATH = "/opt/kg"

class Colors:
    """终端颜色"""
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color

def print_step(step, message):
    """打印步骤信息"""
    print(f"\n{Colors.YELLOW}步骤{step}: {message}{Colors.NC}")

def print_success(message):
    """打印成功信息"""
    print(f"{Colors.GREEN}✓ {message}{Colors.NC}")

def print_error(message):
    """打印错误信息"""
    print(f"{Colors.RED}✗ {message}{Colors.NC}")

def print_info(message):
    """打印提示信息"""
    print(f"{Colors.BLUE}ℹ {message}{Colors.NC}")

def run_command(cmd, cwd=None, shell=True):
    """运行命令"""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            shell=shell,
            check=True,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def check_prerequisites():
    """检查前置条件"""
    print_step(1, "检查前置条件")
    
    # 检查Node.js
    success, output = run_command("node --version")
    if success:
        print_success(f"Node.js已安装: {output.strip()}")
    else:
        print_error("Node.js未安装，请先安装Node.js")
        return False
    
    # 检查npm
    success, output = run_command("npm --version")
    if success:
        print_success(f"npm已安装: {output.strip()}")
    else:
        print_error("npm未安装")
        return False
    
    # 检查项目目录
    if not Path("apps/web").exists():
        print_error("apps/web目录不存在")
        return False
    print_success("项目目录检查通过")
    
    return True

def build_frontend():
    """构建前端"""
    print_step(2, "构建前端应用")
    
    web_dir = Path("apps/web")
    
    # 检查node_modules
    if not (web_dir / "node_modules").exists():
        print_info("安装前端依赖...")
        success, output = run_command("npm install", cwd=web_dir)
        if not success:
            print_error(f"依赖安装失败: {output}")
            return False
        print_success("依赖安装成功")
    
    # 构建前端
    print_info("构建前端...")
    success, output = run_command("npm run build", cwd=web_dir)
    if not success:
        print_error(f"前端构建失败: {output}")
        return False
    
    # 检查构建结果
    if not (web_dir / "dist").exists():
        print_error("构建失败，dist目录不存在")
        return False
    
    print_success("前端构建成功")
    return True

def prepare_deployment_files():
    """准备部署文件"""
    print_step(3, "准备部署文件")
    
    # 复制dist目录
    if Path("dist").exists():
        shutil.rmtree("dist")
    shutil.copytree("apps/web/dist", "dist")
    print_success("构建文件已复制到 ./dist")
    
    # 更新nginx配置
    if Path("nginx/nginx.http.conf").exists():
        shutil.copy("nginx/nginx.http.conf", "nginx/nginx.conf")
        print_success("Nginx配置已更新为HTTP模式")
    else:
        print_error("nginx/nginx.http.conf不存在")
        return False
    
    return True

def upload_to_server():
    """上传文件到服务器"""
    print_step(4, "上传文件到服务器")
    
    print_info(f"目标服务器: {SERVER_USER}@{SERVER_IP}:{SERVER_PATH}")
    
    # 检查SSH连接
    print_info("测试SSH连接...")
    success, _ = run_command(f'ssh -o ConnectTimeout=5 {SERVER_USER}@{SERVER_IP} "echo connected"')
    if not success:
        print_error("无法连接到服务器，请检查:")
        print("  1. 服务器IP是否正确")
        print("  2. SSH密钥是否配置")
        print("  3. 网络连接是否正常")
        print("\n手动上传命令:")
        print(f"  scp -r dist/ {SERVER_USER}@{SERVER_IP}:{SERVER_PATH}/")
        print(f"  scp nginx/nginx.conf {SERVER_USER}@{SERVER_IP}:{SERVER_PATH}/nginx/")
        print(f"  scp docker-compose.prod.yml {SERVER_USER}@{SERVER_IP}:{SERVER_PATH}/")
        return False
    
    print_success("SSH连接成功")
    
    # 上传dist目录
    print_info("上传dist目录...")
    success, output = run_command(f'scp -r dist/ {SERVER_USER}@{SERVER_IP}:{SERVER_PATH}/')
    if not success:
        print_error(f"上传dist失败: {output}")
        return False
    print_success("dist目录上传成功")
    
    # 上传nginx配置
    print_info("上传nginx配置...")
    success, output = run_command(f'scp nginx/nginx.conf {SERVER_USER}@{SERVER_IP}:{SERVER_PATH}/nginx/')
    if not success:
        print_error(f"上传nginx配置失败: {output}")
        return False
    print_success("nginx配置上传成功")
    
    # 上传docker-compose配置
    print_info("上传docker-compose配置...")
    success, output = run_command(f'scp docker-compose.prod.yml {SERVER_USER}@{SERVER_IP}:{SERVER_PATH}/')
    if not success:
        print_error(f"上传docker-compose配置失败: {output}")
        return False
    print_success("docker-compose配置上传成功")
    
    return True

def restart_services():
    """重启服务器上的服务"""
    print_step(5, "重启服务")
    
    commands = [
        "cd /opt/kg",
        "docker-compose -f docker-compose.prod.yml down",
        "docker-compose -f docker-compose.prod.yml up -d --build",
        "sleep 5",
        "docker-compose -f docker-compose.prod.yml ps"
    ]
    
    cmd = f'ssh {SERVER_USER}@{SERVER_IP} "{"; ".join(commands)}"'
    success, output = run_command(cmd)
    
    if success:
        print_success("服务重启成功")
        print("\n服务状态:")
        print(output)
        return True
    else:
        print_error(f"服务重启失败: {output}")
        print("\n请手动在服务器上执行:")
        print("  cd /opt/kg")
        print("  docker-compose -f docker-compose.prod.yml down")
        print("  docker-compose -f docker-compose.prod.yml up -d --build")
        return False

def verify_deployment():
    """验证部署"""
    print_step(6, "验证部署")
    
    import urllib.request
    import urllib.error
    
    urls = [
        f"http://{SERVER_IP}/health",
        f"http://{SERVER_IP}/",
    ]
    
    for url in urls:
        try:
            print_info(f"测试 {url}")
            response = urllib.request.urlopen(url, timeout=10)
            if response.status == 200:
                print_success(f"✓ {url} 访问正常")
            else:
                print_error(f"✗ {url} 返回状态码: {response.status}")
        except urllib.error.URLError as e:
            print_error(f"✗ {url} 访问失败: {e}")
        except Exception as e:
            print_error(f"✗ {url} 测试失败: {e}")

def main():
    """主函数"""
    print("=" * 50)
    print("质量知识图谱系统 - 阿里云自动部署")
    print("=" * 50)
    
    # 检查前置条件
    if not check_prerequisites():
        sys.exit(1)
    
    # 构建前端
    if not build_frontend():
        sys.exit(1)
    
    # 准备部署文件
    if not prepare_deployment_files():
        sys.exit(1)
    
    # 询问是否上传
    print("\n" + "=" * 50)
    print_info("本地构建完成！")
    print("\n选择部署方式:")
    print("  1. 自动上传到服务器并重启服务 (需要SSH密钥)")
    print("  2. 仅本地构建，手动上传")
    print("  3. 退出")
    
    choice = input("\n请选择 (1/2/3): ").strip()
    
    if choice == "1":
        # 上传到服务器
        if not upload_to_server():
            print_error("\n自动上传失败，请使用手动上传方式")
            sys.exit(1)
        
        # 重启服务
        if not restart_services():
            print_error("\n服务重启失败")
            sys.exit(1)
        
        # 验证部署
        verify_deployment()
        
        print("\n" + "=" * 50)
        print_success("部署完成！")
        print("=" * 50)
        print(f"\n访问地址: {Colors.GREEN}http://{SERVER_IP}/{Colors.NC}")
        print(f"API地址: {Colors.GREEN}http://{SERVER_IP}/api/{Colors.NC}")
        print(f"健康检查: {Colors.GREEN}http://{SERVER_IP}/health{Colors.NC}")
        
    elif choice == "2":
        print("\n" + "=" * 50)
        print_success("本地构建完成！")
        print("=" * 50)
        print("\n请手动上传以下文件到服务器:")
        print(f"  scp -r dist/ {SERVER_USER}@{SERVER_IP}:{SERVER_PATH}/")
        print(f"  scp nginx/nginx.conf {SERVER_USER}@{SERVER_IP}:{SERVER_PATH}/nginx/")
        print(f"  scp docker-compose.prod.yml {SERVER_USER}@{SERVER_IP}:{SERVER_PATH}/")
        print("\n然后在服务器上执行:")
        print(f"  ssh {SERVER_USER}@{SERVER_IP}")
        print(f"  cd {SERVER_PATH}")
        print("  docker-compose -f docker-compose.prod.yml down")
        print("  docker-compose -f docker-compose.prod.yml up -d --build")
    else:
        print("退出部署")
        sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n部署已取消")
        sys.exit(1)
    except Exception as e:
        print_error(f"\n发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

