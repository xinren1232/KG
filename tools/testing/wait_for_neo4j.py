#!/usr/bin/env python3
"""
等待Neo4j启动的脚本
"""
import time
import sys

def check_neo4j_connection():
    """检查Neo4j连接"""
    try:
        from neo4j import GraphDatabase
        
        driver = GraphDatabase.driver(
            "bolt://localhost:7687", 
            auth=("neo4j", "password123")
        )
        
        with driver.session() as session:
            result = session.run("RETURN 1 as test")
            record = result.single()
            if record and record["test"] == 1:
                return True
        
        driver.close()
        return False
        
    except Exception:
        return False

def check_neo4j_browser():
    """检查Neo4j Browser"""
    try:
        import requests
        response = requests.get("http://localhost:7474", timeout=3)
        return response.status_code == 200
    except:
        return False

def main():
    """主函数"""
    print("⏳ 等待Neo4j启动...")
    print("💡 请确保Neo4j Desktop中的数据库已启动")
    print("   - 打开Neo4j Desktop")
    print("   - 点击数据库的'Start'按钮")
    print("   - 等待状态变为'Active'")
    print("\n按 Ctrl+C 取消等待\n")
    
    max_attempts = 60  # 最多等待5分钟
    attempt = 0
    
    try:
        while attempt < max_attempts:
            attempt += 1
            
            # 检查Browser
            browser_ok = check_neo4j_browser()
            
            # 检查数据库连接
            db_ok = check_neo4j_connection()
            
            status_browser = "✅" if browser_ok else "❌"
            status_db = "✅" if db_ok else "❌"
            
            print(f"\r尝试 {attempt:2d}/{max_attempts} - Browser: {status_browser} | Database: {status_db}", end="")
            
            if browser_ok and db_ok:
                print("\n\n🎉 Neo4j启动成功！")
                print("📍 Neo4j Browser: http://localhost:7474")
                print("📍 数据库连接: bolt://localhost:7687")
                print("\n✅ 可以继续下一步操作")
                return True
            
            time.sleep(5)  # 等待5秒
        
        print(f"\n\n❌ 等待超时（{max_attempts * 5}秒）")
        print("💡 请检查Neo4j Desktop是否正确启动")
        return False
        
    except KeyboardInterrupt:
        print("\n\n⏹️ 用户取消等待")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
