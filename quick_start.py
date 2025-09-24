#!/usr/bin/env python3
"""
快速启动脚本 - 一键启动知识图谱系统
"""
import subprocess
import time
import os
import sys
import requests
from pathlib import Path

def run_command(cmd, cwd=None, check=True):
    """执行命令"""
    print(f"执行命令: {cmd}")
    if cwd:
        print(f"工作目录: {cwd}")
    
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, check=check, 
                              capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return result
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败: {e}")
        if e.stderr:
            print(f"错误信息: {e.stderr}")
        return None

def wait_for_service(url, timeout=60, service_name="服务"):
    """等待服务启动"""
    print(f"等待{service_name}启动...")
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ {service_name}已启动: {url}")
                return True
        except requests.exceptions.RequestException:
            pass
        
        time.sleep(2)
    
    print(f"❌ {service_name}启动超时")
    return False

def main():
    """主函数"""
    print("🚀 启动知识图谱系统...")
    
    # 检查环境文件
    if not Path(".env").exists():
        print("❌ 未找到.env文件，请先复制.env.example并配置")
        return
    
    # 1. 启动Docker服务
    print("\n📦 启动Docker服务...")
    run_command("docker compose up -d")
    
    # 2. 等待Neo4j启动
    if wait_for_service("http://localhost:7474", service_name="Neo4j"):
        # 3. 初始化Neo4j约束
        print("\n🔧 初始化Neo4j约束...")
        time.sleep(5)  # 等待Neo4j完全启动
        run_command("docker exec kg_neo4j cypher-shell -u neo4j -p password123 -f /import/neo4j_constraints.cypher", check=False)
        
        # 4. 运行ETL导入数据
        print("\n📊 导入Excel数据...")
        if Path("来料问题洗后版.xlsx").exists():
            run_command("python api/etl/etl_from_excel.py")
        else:
            print("⚠️ 未找到Excel文件，跳过数据导入")
    
    # 5. 等待API服务启动
    wait_for_service("http://localhost:8000/health", service_name="API服务")
    
    # 6. 启动前端开发服务器
    print("\n🖥️ 启动前端服务...")
    frontend_process = subprocess.Popen(
        ["npm", "run", "dev"], 
        cwd="apps/web",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # 等待前端启动
    time.sleep(5)
    
    print("\n✅ 系统启动完成！")
    print("🌐 访问地址:")
    print("  - 前端应用: http://localhost:5175")
    print("  - API文档: http://localhost:8000/docs")
    print("  - Neo4j浏览器: http://localhost:7474")
    print("\n📝 测试API:")
    print('  curl -X POST http://localhost:8000/kg/query/cause_path -H "Content-Type: application/json" -d \'{"symptom":"裂纹"}\'')
    print('  curl -X POST http://localhost:8000/kg/query/anomalies -H "Content-Type: application/json" -d \'{"factory":"泰衡诺工厂"}\'')
    
    print("\n按Ctrl+C停止前端服务...")
    try:
        frontend_process.wait()
    except KeyboardInterrupt:
        print("\n🛑 停止前端服务...")
        frontend_process.terminate()
        frontend_process.wait()

if __name__ == "__main__":
    main()
