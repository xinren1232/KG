#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import os
import sys
import time

def start_frontend():
    """启动前端服务"""
    print("🎨 启动前端服务...")
    print("访问地址: http://localhost:5173")
    print("按 Ctrl+C 停止服务")
    print("-" * 50)
    
    # 切换到前端目录
    frontend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "apps", "web")
    
    if not os.path.exists(frontend_dir):
        print(f"❌ 前端目录不存在: {frontend_dir}")
        return False
    
    # 检查node_modules
    node_modules = os.path.join(frontend_dir, "node_modules")
    if not os.path.exists(node_modules):
        print("❌ node_modules不存在，请先运行 npm install")
        return False
    
    # 检查vite
    vite_path = os.path.join(node_modules, "vite", "bin", "vite.js")
    if not os.path.exists(vite_path):
        print("❌ vite不存在")
        return False
    
    try:
        # 启动vite开发服务器
        cmd = ["node", vite_path]
        print(f"执行命令: {' '.join(cmd)}")
        print(f"工作目录: {frontend_dir}")
        
        process = subprocess.Popen(
            cmd,
            cwd=frontend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        print("✅ 前端服务启动中...")
        
        # 实时输出日志
        for line in process.stdout:
            print(line.rstrip())
            if "Local:" in line and "localhost" in line:
                print("🎉 前端服务启动成功！")
        
        process.wait()
        
    except KeyboardInterrupt:
        print("\n🛑 用户中断，停止前端服务")
        if 'process' in locals():
            process.terminate()
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        return False
    
    return True

if __name__ == "__main__":
    start_frontend()
