#!/usr/bin/env python3
"""
前端启动脚本
"""

import os
import sys
import subprocess
from pathlib import Path

def check_node():
    """检查Node.js是否安装"""
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js版本: {result.stdout.strip()}")
            return True
        else:
            print("❌ Node.js未安装或无法访问")
            return False
    except FileNotFoundError:
        print("❌ Node.js未安装")
        return False

def check_npm():
    """检查npm是否可用"""
    try:
        result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ npm版本: {result.stdout.strip()}")
            return True
        else:
            print("❌ npm不可用")
            return False
    except FileNotFoundError:
        print("❌ npm未安装")
        return False

def install_dependencies():
    """安装依赖"""
    print("📦 安装前端依赖...")
    try:
        subprocess.run(['npm', 'install'], check=True, cwd='apps/web')
        print("✅ 依赖安装完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖安装失败: {e}")
        return False

def start_dev_server():
    """启动开发服务器"""
    print("🚀 启动前端开发服务器...")
    print("📍 前端地址: http://localhost:5173")
    print("📍 确保API服务运行在: http://localhost:8000")
    print("\n按 Ctrl+C 停止服务器\n")
    
    try:
        subprocess.run(['npm', 'run', 'dev'], cwd='apps/web')
    except KeyboardInterrupt:
        print("\n🛑 前端服务器已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")

def main():
    """主函数"""
    print("🌐 质量知识图谱助手 - 前端启动")
    print("="*50)
    
    # 检查是否在正确的目录
    if not Path("apps/web/package.json").exists():
        print("❌ 请在项目根目录运行此脚本")
        return
    
    # 检查Node.js和npm
    if not check_node() or not check_npm():
        print("\n请先安装Node.js:")
        print("https://nodejs.org/")
        return
    
    # 检查是否需要安装依赖
    if not Path("apps/web/node_modules").exists():
        if not install_dependencies():
            return
    
    # 启动开发服务器
    start_dev_server()

if __name__ == "__main__":
    main()
