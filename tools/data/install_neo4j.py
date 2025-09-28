#!/usr/bin/env python3
"""
Neo4j自动安装和配置脚本
"""
import os
import sys
import subprocess
import requests
import time
from pathlib import Path

def run_command(cmd, check=True):
    """执行命令"""
    print(f"执行: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, check=check, 
                              capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return result
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败: {e}")
        if e.stderr:
            print(f"错误: {e.stderr}")
        return None

def check_java():
    """检查Java版本"""
    print("🔍 检查Java版本...")
    result = run_command("java -version", check=False)
    if result and result.returncode == 0:
        print("✅ Java已安装")
        return True
    else:
        print("❌ Java未安装或版本不兼容")
        print("请安装Java 17或更高版本")
        return False

def check_docker():
    """检查Docker是否可用"""
    print("🔍 检查Docker...")
    result = run_command("docker --version", check=False)
    if result and result.returncode == 0:
        print("✅ Docker可用")
        return True
    else:
        print("❌ Docker不可用")
        return False

def install_with_docker():
    """使用Docker安装Neo4j"""
    print("🐳 使用Docker安装Neo4j...")
    
    # 停止现有容器
    run_command("docker stop neo4j", check=False)
    run_command("docker rm neo4j", check=False)
    
    # 拉取并运行Neo4j
    cmd = """docker run -d \
        --name neo4j \
        -p 7474:7474 -p 7687:7687 \
        -e NEO4J_AUTH=neo4j/password123 \
        -e NEO4J_PLUGINS='["apoc"]' \
        neo4j:5.23"""
    
    result = run_command(cmd)
    if result and result.returncode == 0:
        print("✅ Neo4j Docker容器启动成功")
        return True
    else:
        print("❌ Neo4j Docker容器启动失败")
        return False

def download_neo4j_desktop():
    """指导下载Neo4j Desktop"""
    print("💻 Neo4j Desktop安装指导:")
    print("1. 访问: https://neo4j.com/download/")
    print("2. 点击'Download'按钮")
    print("3. 填写信息获取下载链接")
    print("4. 下载并安装Neo4j Desktop")
    print("5. 创建新项目和数据库")
    print("6. 设置密码为: password123")
    
    input("完成Neo4j Desktop安装后，按Enter继续...")

def wait_for_neo4j():
    """等待Neo4j启动"""
    print("⏳ 等待Neo4j启动...")
    max_attempts = 30
    
    for attempt in range(max_attempts):
        try:
            response = requests.get("http://localhost:7474", timeout=5)
            if response.status_code == 200:
                print("✅ Neo4j已启动")
                return True
        except requests.exceptions.RequestException:
            pass
        
        print(f"等待中... ({attempt + 1}/{max_attempts})")
        time.sleep(2)
    
    print("❌ Neo4j启动超时")
    return False

def test_neo4j_connection():
    """测试Neo4j连接"""
    print("🔗 测试Neo4j连接...")
    try:
        from neo4j import GraphDatabase
        
        driver = GraphDatabase.driver(
            "bolt://localhost:7687",
            auth=("neo4j", "password123")
        )
        
        with driver.session() as session:
            result = session.run("RETURN 'Hello Neo4j' as message")
            record = result.single()
            print(f"✅ 连接成功: {record['message']}")
            
        driver.close()
        return True
        
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        print("请检查Neo4j是否正确启动，用户名密码是否正确")
        return False

def create_constraints():
    """创建数据库约束"""
    print("🔧 创建数据库约束...")
    try:
        from neo4j import GraphDatabase
        
        driver = GraphDatabase.driver(
            "bolt://localhost:7687",
            auth=("neo4j", "password123")
        )
        
        constraints = [
            "CREATE CONSTRAINT component_name IF NOT EXISTS FOR (c:Component) REQUIRE c.name IS UNIQUE",
            "CREATE CONSTRAINT symptom_name IF NOT EXISTS FOR (s:Symptom) REQUIRE s.name IS UNIQUE",
            "CREATE CONSTRAINT cause_name IF NOT EXISTS FOR (c:Cause) REQUIRE c.name IS UNIQUE",
            "CREATE CONSTRAINT countermeasure_name IF NOT EXISTS FOR (c:Countermeasure) REQUIRE c.name IS UNIQUE"
        ]
        
        with driver.session() as session:
            for constraint in constraints:
                try:
                    session.run(constraint)
                    print(f"✅ 约束创建成功")
                except Exception as e:
                    print(f"⚠️ 约束可能已存在: {e}")
        
        driver.close()
        print("✅ 数据库约束配置完成")
        return True
        
    except Exception as e:
        print(f"❌ 约束创建失败: {e}")
        return False

def update_env_file():
    """更新.env文件"""
    print("📝 更新.env文件...")
    
    env_content = """# Neo4j数据库配置
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASS=password123
NEO4J_DATABASE=neo4j

# API配置
API_HOST=0.0.0.0
API_PORT=8000

# 前端配置
FRONTEND_URL=http://localhost:5173
"""
    
    try:
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        print("✅ .env文件更新成功")
        return True
    except Exception as e:
        print(f"❌ .env文件更新失败: {e}")
        return False

def install_neo4j_driver():
    """安装Neo4j Python驱动"""
    print("📦 安装Neo4j Python驱动...")
    result = run_command("pip install neo4j", check=False)
    if result and result.returncode == 0:
        print("✅ Neo4j驱动安装成功")
        return True
    else:
        print("❌ Neo4j驱动安装失败")
        return False

def main():
    """主函数"""
    print("🚀 Neo4j自动安装和配置")
    print("=" * 50)
    
    # 安装Neo4j驱动
    if not install_neo4j_driver():
        print("请手动安装: pip install neo4j")
    
    # 检查安装方式
    if check_docker():
        print("选择Docker安装方式")
        if install_with_docker():
            if wait_for_neo4j():
                success = True
            else:
                success = False
        else:
            success = False
    else:
        print("选择Neo4j Desktop安装方式")
        download_neo4j_desktop()
        if wait_for_neo4j():
            success = True
        else:
            success = False
    
    if success:
        # 测试连接
        if test_neo4j_connection():
            # 创建约束
            create_constraints()
            # 更新配置
            update_env_file()
            
            print("\n🎉 Neo4j安装配置完成!")
            print("📊 访问地址:")
            print("  - Neo4j Browser: http://localhost:7474")
            print("  - 用户名: neo4j")
            print("  - 密码: password123")
            print("\n🔄 现在可以重启您的API服务以连接Neo4j")
        else:
            print("\n❌ 安装完成但连接测试失败")
            print("请检查Neo4j是否正确启动")
    else:
        print("\n❌ Neo4j安装失败")
        print("请参考 install_neo4j_guide.md 手动安装")

if __name__ == "__main__":
    main()
