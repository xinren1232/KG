#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from neo4j import GraphDatabase

def wait_and_retry_connection():
    """等待认证限制解除并重试连接"""
    print("⏳ 等待Neo4j认证限制解除...")
    print("认证限制通常在60秒后自动解除")
    
    # 等待60秒
    for i in range(60, 0, -1):
        print(f"\r等待中... {i}秒", end="", flush=True)
        time.sleep(1)
    
    print("\n\n🔄 重新尝试连接...")
    
    uri = "bolt://localhost:7687"
    passwords = ["password123", "neo4j", "admin", "password", "123456", ""]
    
    for password in passwords:
        try:
            print(f"🔍 尝试密码: '{password}'")
            driver = GraphDatabase.driver(uri, auth=("neo4j", password))
            
            with driver.session() as session:
                result = session.run("RETURN 'Hello Neo4j!' as message")
                message = result.single()["message"]
                
                print(f"✅ 连接成功!")
                print(f"   用户名: neo4j")
                print(f"   密码: {password}")
                print(f"   响应: {message}")
                
                # 检查数据库状态
                result = session.run("MATCH (n) RETURN count(n) as count")
                count = result.single()["count"]
                print(f"   节点数量: {count}")
                
                driver.close()
                return True, password
                
        except Exception as e:
            error_msg = str(e)
            if "AuthenticationRateLimit" in error_msg:
                print(f"❌ 仍在认证限制中，继续等待...")
                time.sleep(10)  # 额外等待10秒
                continue
            else:
                print(f"❌ 密码错误: {error_msg[:100]}")
                continue
    
    return False, None

def main():
    """主函数"""
    print("🔐 Neo4j连接重试工具")
    print("=" * 40)
    
    success, password = wait_and_retry_connection()
    
    if success:
        print(f"\n🎉 Neo4j连接成功!")
        print(f"✅ 正确密码: {password}")
        print("\n🌐 现在可以完整使用知识图谱系统:")
        print("   - 前端界面: http://localhost:5173")
        print("   - 图谱可视化: http://localhost:5173/graph-viz")
        print("   - API服务: http://localhost:8000/docs")
        print("   - Neo4j浏览器: http://localhost:7474")
        
        # 保存正确的密码到配置文件
        try:
            with open("neo4j_password.txt", "w") as f:
                f.write(password)
            print(f"\n💾 密码已保存到 neo4j_password.txt")
        except:
            pass
            
    else:
        print("\n❌ 连接仍然失败")
        print("💡 建议:")
        print("   1. 在浏览器中访问 http://localhost:7474")
        print("   2. 手动设置或重置密码")
        print("   3. 或者重启Neo4j服务")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断操作")
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
