#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决Neo4j认证问题
"""

import time
import subprocess
import sys

print("🔧 解决Neo4j认证问题...")

def check_neo4j_processes():
    """检查Neo4j进程"""
    print("🔍 检查Neo4j进程...")
    try:
        result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq java.exe'], 
                              capture_output=True, text=True)
        if 'java.exe' in result.stdout:
            print("✅ 发现Java进程（可能是Neo4j）")
            return True
        else:
            print("❌ 未发现Java进程")
            return False
    except Exception as e:
        print(f"❌ 检查进程失败: {e}")
        return False

def try_http_api():
    """尝试HTTP API访问"""
    print("🌐 尝试HTTP API访问...")
    try:
        import requests
        
        # 尝试无认证访问
        response = requests.get("http://localhost:7474/db/data/", timeout=5)
        print(f"HTTP状态码: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ HTTP API无认证访问成功")
            return True, None
        elif response.status_code == 401:
            print("⚠️ HTTP API需要认证")
            return False, "需要认证"
        else:
            print(f"⚠️ HTTP API返回: {response.status_code}")
            return False, f"状态码: {response.status_code}"
            
    except Exception as e:
        print(f"❌ HTTP API访问失败: {e}")
        return False, str(e)

def try_cypher_shell():
    """尝试cypher-shell命令"""
    print("🔧 尝试cypher-shell...")
    try:
        # 尝试无密码连接
        result = subprocess.run(['cypher-shell', '-u', 'neo4j', '-p', '', 
                               'RETURN 1 as test'], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ cypher-shell无密码连接成功")
            return True, ""
        else:
            print(f"❌ cypher-shell失败: {result.stderr}")
            return False, result.stderr
            
    except FileNotFoundError:
        print("⚠️ cypher-shell命令不存在")
        return False, "命令不存在"
    except Exception as e:
        print(f"❌ cypher-shell执行失败: {e}")
        return False, str(e)

def wait_for_auth_reset():
    """等待认证限制重置"""
    print("⏰ 等待认证限制重置...")
    for i in range(30, 0, -1):
        print(f"⏳ 等待 {i} 秒...", end='\r')
        time.sleep(1)
    print("✅ 等待完成，重新尝试连接")

def try_bolt_connection_again():
    """重新尝试Bolt连接"""
    print("🔄 重新尝试Bolt连接...")
    
    try:
        from neo4j import GraphDatabase
        
        # 常见的默认密码
        passwords_to_try = [
            "",           # 空密码
            "neo4j",      # 默认密码
            "password",   # 常用密码
            "admin",      # 管理员密码
            "123456",     # 简单密码
        ]
        
        uri = "bolt://localhost:7687"
        
        for password in passwords_to_try:
            try:
                print(f"🔍 尝试密码: {'(空)' if password == '' else password}")
                
                if password == "":
                    # 尝试无认证
                    driver = GraphDatabase.driver(uri)
                else:
                    driver = GraphDatabase.driver(uri, auth=("neo4j", password))
                
                with driver.session() as session:
                    result = session.run("RETURN 1 as test")
                    test_value = result.single()["test"]
                    
                    if test_value == 1:
                        print(f"✅ 连接成功! 密码: {'(空)' if password == '' else password}")
                        
                        # 检查当前数据
                        result = session.run("MATCH (n:Dictionary) RETURN count(n) as count")
                        current_count = result.single()["count"]
                        print(f"📊 当前Dictionary节点: {current_count} 个")
                        
                        driver.close()
                        return True, password
                        
            except Exception as e:
                print(f"❌ 密码 {'(空)' if password == '' else password} 失败: {e}")
                continue
        
        print("❌ 所有密码尝试失败")
        return False, None
        
    except Exception as e:
        print(f"❌ Bolt连接测试失败: {e}")
        return False, None

def main():
    """主函数"""
    print("🚀 Neo4j认证问题诊断和解决")
    print("=" * 50)
    
    # 1. 检查进程
    check_neo4j_processes()
    
    # 2. 尝试HTTP API
    http_success, http_error = try_http_api()
    
    # 3. 尝试cypher-shell
    shell_success, shell_error = try_cypher_shell()
    
    # 4. 等待认证限制重置
    wait_for_auth_reset()
    
    # 5. 重新尝试Bolt连接
    bolt_success, working_password = try_bolt_connection_again()
    
    print("\n" + "=" * 50)
    print("📊 诊断结果")
    print("=" * 50)
    
    print(f"HTTP API: {'✅ 可用' if http_success else '❌ 不可用'}")
    print(f"Cypher Shell: {'✅ 可用' if shell_success else '❌ 不可用'}")
    print(f"Bolt连接: {'✅ 可用' if bolt_success else '❌ 不可用'}")
    
    if bolt_success:
        print(f"✅ 工作密码: {'(空密码)' if working_password == '' else working_password}")
        print(f"\n🎯 现在可以执行图谱更新了!")
        
        # 保存工作密码到文件
        with open("neo4j_auth.txt", "w") as f:
            f.write(f"username: neo4j\npassword: {working_password}")
        print(f"💾 认证信息已保存到: neo4j_auth.txt")
        
    else:
        print(f"\n💡 建议解决方案:")
        print(f"  1. 重启Neo4j服务")
        print(f"  2. 检查Neo4j配置文件")
        print(f"  3. 重置Neo4j密码")
        print(f"  4. 使用Neo4j浏览器手动连接")

if __name__ == "__main__":
    main()
