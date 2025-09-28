#!/usr/bin/env python3
"""
Neo4j连接检查脚本
"""
import os
import sys
from pathlib import Path

def check_neo4j_connection():
    """检查Neo4j连接"""
    try:
        from neo4j import GraphDatabase
        
        # 从环境变量读取配置
        uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        user = os.getenv("NEO4J_USER", "neo4j")
        password = os.getenv("NEO4J_PASS", "password123")
        
        print(f"🔍 检查Neo4j连接...")
        print(f"   URI: {uri}")
        print(f"   用户: {user}")
        print(f"   密码: {'*' * len(password)}")
        
        # 创建驱动
        driver = GraphDatabase.driver(uri, auth=(user, password))
        
        # 测试连接
        with driver.session() as session:
            result = session.run("RETURN 1 as test")
            record = result.single()
            if record and record["test"] == 1:
                print("✅ Neo4j连接成功！")
                
                # 检查数据库信息
                result = session.run("CALL db.info()")
                info = result.single()
                if info:
                    print(f"   数据库名称: {info.get('name', 'N/A')}")
                    print(f"   Neo4j版本: {info.get('kernelVersion', 'N/A')}")
                
                # 检查节点数量
                result = session.run("MATCH (n) RETURN count(n) as count")
                count = result.single()["count"]
                print(f"   节点总数: {count}")
                
                return True
            else:
                print("❌ Neo4j连接测试失败")
                return False
                
    except ImportError:
        print("❌ Neo4j驱动未安装，请运行: pip install neo4j")
        return False
    except Exception as e:
        print(f"❌ Neo4j连接失败: {e}")
        print("\n💡 请检查:")
        print("   1. Neo4j Desktop是否已启动")
        print("   2. 数据库是否处于Active状态")
        print("   3. 用户名密码是否正确")
        print("   4. 端口7687是否可访问")
        return False
    finally:
        try:
            driver.close()
        except:
            pass

def check_neo4j_browser():
    """检查Neo4j Browser是否可访问"""
    try:
        import requests
        response = requests.get("http://localhost:7474", timeout=5)
        if response.status_code == 200:
            print("✅ Neo4j Browser可访问: http://localhost:7474")
            return True
        else:
            print(f"❌ Neo4j Browser响应异常: {response.status_code}")
            return False
    except ImportError:
        print("⚠️ requests库未安装，跳过Browser检查")
        return True
    except Exception as e:
        print(f"❌ Neo4j Browser不可访问: {e}")
        return False

def main():
    """主函数"""
    print("🚀 Neo4j环境检查")
    print("=" * 50)
    
    # 检查环境变量
    env_file = Path(".env")
    if env_file.exists():
        print("✅ 找到.env配置文件")
        from dotenv import load_dotenv
        load_dotenv()
    else:
        print("⚠️ 未找到.env文件，使用默认配置")
    
    # 检查Neo4j连接
    neo4j_ok = check_neo4j_connection()
    
    # 检查Neo4j Browser
    browser_ok = check_neo4j_browser()
    
    print("\n" + "=" * 50)
    if neo4j_ok:
        print("🎉 Neo4j环境检查通过！")
        print("\n📋 下一步操作:")
        print("   1. 运行初始化脚本: python init_neo4j.py")
        print("   2. 启动完整版API: python start_full_api.py")
    else:
        print("❌ Neo4j环境检查失败")
        print("\n📋 解决方案:")
        print("   1. 确保Neo4j Desktop已启动")
        print("   2. 检查数据库状态为Active")
        print("   3. 验证用户名密码: neo4j/password123")
        print("   4. 访问 http://localhost:7474 测试连接")

if __name__ == "__main__":
    main()
