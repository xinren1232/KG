#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import time
import requests
import json

def reset_neo4j_auth():
    """重置Neo4j认证"""
    print("🔧 重置Neo4j认证...")
    
    # 方法1: 尝试通过HTTP API重置
    try:
        print("📡 尝试通过HTTP API连接...")
        
        # 尝试无认证访问
        response = requests.get("http://localhost:7474/db/data/", timeout=5)
        if response.status_code == 200:
            print("✅ Neo4j HTTP接口可访问")
            
            # 尝试获取版本信息
            response = requests.get("http://localhost:7474/", timeout=5)
            if response.status_code == 200:
                print("✅ Neo4j Web界面可访问")
                print("💡 请在浏览器中访问 http://localhost:7474 手动设置密码")
                return True
                
    except Exception as e:
        print(f"❌ HTTP API访问失败: {e}")
    
    # 方法2: 检查是否是首次启动
    print("\n🔍 检查是否是首次启动...")
    try:
        # 尝试连接到默认的初始状态
        from neo4j import GraphDatabase
        
        # 首次启动时，可能需要设置密码
        uri = "bolt://localhost:7687"
        
        # 尝试无密码连接
        try:
            driver = GraphDatabase.driver(uri, auth=None)
            with driver.session() as session:
                result = session.run("RETURN 1")
                print("✅ 无需认证即可连接")
                driver.close()
                return True
        except:
            pass
        
        # 尝试默认密码
        default_passwords = ["", "neo4j", "password", "admin", "123456", "password123"]
        
        for password in default_passwords:
            try:
                print(f"🔍 尝试密码: '{password}'")
                driver = GraphDatabase.driver(uri, auth=("neo4j", password))
                
                with driver.session() as session:
                    # 如果是初始密码，需要更改
                    if password == "neo4j":
                        print("🔄 检测到初始密码，尝试更改为 'password123'")
                        session.run("ALTER CURRENT USER SET PASSWORD FROM 'neo4j' TO 'password123'")
                        print("✅ 密码已更改为 'password123'")
                    
                    result = session.run("RETURN 'Connected!' as message")
                    message = result.single()["message"]
                    print(f"✅ 连接成功: {message}")
                    
                    # 测试数据库
                    result = session.run("MATCH (n) RETURN count(n) as count")
                    count = result.single()["count"]
                    print(f"📊 数据库节点数: {count}")
                    
                driver.close()
                return True, password if password != "neo4j" else "password123"
                
            except Exception as e:
                print(f"❌ 密码 '{password}' 失败: {str(e)[:100]}")
                continue
        
    except Exception as e:
        print(f"❌ 连接测试失败: {e}")
    
    return False

def provide_manual_instructions():
    """提供手动重置说明"""
    print("\n" + "=" * 60)
    print("📋 手动重置Neo4j密码指南")
    print("=" * 60)
    
    print("\n🌐 方法1: 通过Web界面")
    print("1. 打开浏览器访问: http://localhost:7474")
    print("2. 如果是首次启动，会提示设置密码")
    print("3. 用户名: neo4j")
    print("4. 设置新密码 (建议: password123)")
    
    print("\n🖥️ 方法2: 通过Neo4j Desktop")
    print("1. 打开Neo4j Desktop")
    print("2. 选择数据库实例")
    print("3. 点击 '...' 菜单")
    print("4. 选择 'Settings' 或 'Manage'")
    print("5. 重置密码")
    
    print("\n⚙️ 方法3: 删除认证文件 (高级)")
    print("1. 停止Neo4j服务")
    print("2. 删除 data/dbms/auth 文件")
    print("3. 重启Neo4j服务")
    print("4. 重新设置密码")
    
    print("\n🔧 方法4: 命令行 (如果可用)")
    print("neo4j-admin set-initial-password password123")

def main():
    """主函数"""
    print("🔐 Neo4j密码重置工具")
    print("=" * 40)
    
    result = reset_neo4j_auth()
    
    if result:
        if isinstance(result, tuple):
            success, password = result
            print(f"\n🎉 Neo4j认证成功!")
            print(f"✅ 用户名: neo4j")
            print(f"✅ 密码: {password}")
        else:
            print(f"\n🎉 Neo4j连接成功!")
        
        print("\n🌐 现在可以访问:")
        print("   - Neo4j浏览器: http://localhost:7474")
        print("   - 知识图谱前端: http://localhost:5173")
        
    else:
        print("\n❌ 自动重置失败")
        provide_manual_instructions()
        
        print("\n⏳ 等待手动设置完成...")
        print("设置完成后，请重新运行服务状态检查")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断操作")
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
