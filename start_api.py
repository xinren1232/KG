#!/usr/bin/env python3
"""
简化的API启动脚本
用于本地开发环境
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """启动API服务"""
    print("🚀 启动质量知识图谱API服务")
    print("="*50)
    
    # 检查是否在正确的目录
    if not Path("services/api/main.py").exists():
        print("❌ 请在项目根目录运行此脚本")
        return
    
    # 切换到API目录
    api_dir = Path("services/api")
    os.chdir(api_dir)
    
    print("📍 API服务将启动在: http://localhost:8000")
    print("📍 API文档地址: http://localhost:8000/docs")
    print("📍 健康检查: http://localhost:8000/health")
    print("\n按 Ctrl+C 停止服务\n")
    
    try:
        # 启动uvicorn服务器
        subprocess.run([
            sys.executable, "-m", "uvicorn", "main:app",
            "--reload", "--host", "0.0.0.0", "--port", "8000"
        ])
    except KeyboardInterrupt:
        print("\n🛑 API服务已停止")
    except FileNotFoundError:
        print("❌ 未找到uvicorn，请先安装依赖:")
        print("   pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ 启动失败: {e}")

if __name__ == "__main__":
    main()
