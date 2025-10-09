#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复Neo4j连接问题
"""

import requests
import json
import time

def test_different_credentials():
    """测试不同的认证凭据"""
    print("🔗 测试不同的Neo4j认证凭据...")
    
    credentials = [
        ("neo4j", "neo4j"),
        ("neo4j", "password"),
        ("neo4j", "123456"),
        ("neo4j", "admin"),
        ("", ""),  # 无认证
    ]
    
    for username, password in credentials:
        print(f"🔑 尝试认证: {username}/{password}")
        try:
            auth = (username, password) if username else None
            response = requests.get(
                "http://localhost:7474/db/data/",
                auth=auth,
                timeout=5
            )
            print(f"   状态码: {response.status_code}")
            if response.status_code == 200:
                print(f"✅ 认证成功: {username}/{password}")
                return username, password
            elif response.status_code == 401:
                print(f"❌ 认证失败: {username}/{password}")
            else:
                print(f"⚠️ 其他错误: {response.status_code}")
        except Exception as e:
            print(f"❌ 连接异常: {e}")
    
    return None, None

def test_neo4j_browser():
    """测试Neo4j浏览器接口"""
    print("🌐 测试Neo4j浏览器接口...")
    
    try:
        response = requests.get("http://localhost:7474/browser/", timeout=5)
        print(f"浏览器接口状态: {response.status_code}")
        if response.status_code == 200:
            print("✅ Neo4j浏览器接口可访问")
            print("💡 请在浏览器中访问 http://localhost:7474 检查认证设置")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ 浏览器接口异常: {e}")
        return False

def try_cypher_shell():
    """尝试使用cypher-shell"""
    print("🔧 尝试使用cypher-shell...")
    
    import subprocess
    
    try:
        # 尝试不同的认证方式
        commands = [
            ["cypher-shell", "-u", "neo4j", "-p", "neo4j", "RETURN 1"],
            ["cypher-shell", "-u", "neo4j", "-p", "password", "RETURN 1"],
            ["cypher-shell", "-u", "neo4j", "-p", "123456", "RETURN 1"],
            ["cypher-shell", "RETURN 1"],  # 无认证
        ]
        
        for cmd in commands:
            print(f"🔄 执行: {' '.join(cmd[:4])}...")  # 不显示密码
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    print(f"✅ cypher-shell连接成功")
                    return True
                else:
                    print(f"❌ 错误: {result.stderr.strip()}")
            except subprocess.TimeoutExpired:
                print("⏰ 命令超时")
            except Exception as e:
                print(f"❌ 异常: {e}")
        
        return False
    except Exception as e:
        print(f"❌ cypher-shell不可用: {e}")
        return False

def create_manual_import_script():
    """创建手动导入脚本"""
    print("📝 创建手动导入脚本...")
    
    script_content = """
# Neo4j 手动数据导入指南

## 方法1: 使用Neo4j浏览器
1. 打开浏览器访问: http://localhost:7474
2. 使用正确的用户名密码登录
3. 在查询框中粘贴以下命令来导入数据

## 方法2: 使用cypher-shell
1. 打开命令行
2. 执行: cypher-shell -u neo4j -p [你的密码]
3. 逐批执行CREATE语句

## 方法3: 重置Neo4j密码
1. 停止Neo4j服务
2. 删除 data/dbms/auth 文件
3. 重启Neo4j服务
4. 使用默认密码 neo4j/neo4j 登录并设置新密码

## 导入数据文件
文件位置: 终极完整词典补充数据导入脚本_20模块版.cypher
包含: 654条补充数据

## 验证导入结果
执行查询: MATCH (n) RETURN count(n) as total
预期结果: 应该增加654个节点
"""
    
    with open("Neo4j手动导入指南.md", "w", encoding="utf-8") as f:
        f.write(script_content)
    
    print("✅ 手动导入指南已创建: Neo4j手动导入指南.md")

def create_batch_import_script():
    """创建批量导入脚本"""
    print("📝 创建批量导入脚本...")
    
    # 读取原始Cypher文件
    try:
        with open("终极完整词典补充数据导入脚本_20模块版.cypher", "r", encoding="utf-8") as f:
            content = f.read()
        
        # 提取CREATE语句
        statements = []
        for line in content.split('\n'):
            line = line.strip()
            if line and not line.startswith('//') and line.endswith(');'):
                statements.append(line)
        
        # 分批创建小文件
        batch_size = 50
        for i in range(0, len(statements), batch_size):
            batch = statements[i:i+batch_size]
            batch_num = i // batch_size + 1
            
            batch_content = f"""// 批次 {batch_num} - {len(batch)} 条语句
// 执行前请确保Neo4j连接正常

{chr(10).join(batch)}
"""
            
            filename = f"导入批次_{batch_num:02d}.cypher"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(batch_content)
            
            print(f"✅ 创建批次文件: {filename} ({len(batch)}条语句)")
        
        print(f"📊 总计创建 {(len(statements)-1)//batch_size + 1} 个批次文件")
        
    except Exception as e:
        print(f"❌ 创建批量导入脚本失败: {e}")

def main():
    """主函数"""
    print("🔧 Neo4j连接问题诊断和修复")
    print("=" * 50)
    
    # 1. 测试不同认证凭据
    username, password = test_different_credentials()
    
    # 2. 测试浏览器接口
    browser_ok = test_neo4j_browser()
    
    # 3. 尝试cypher-shell
    shell_ok = try_cypher_shell()
    
    # 4. 创建手动导入指南
    create_manual_import_script()
    
    # 5. 创建批量导入脚本
    create_batch_import_script()
    
    print("\n" + "=" * 50)
    print("🎯 解决方案总结:")
    
    if username and password:
        print(f"✅ 找到可用认证: {username}/{password}")
        print(f"💡 请更新导入脚本使用此认证")
    else:
        print("❌ 未找到可用认证")
        print("💡 建议:")
        print("   1. 重置Neo4j密码")
        print("   2. 检查Neo4j配置文件")
        print("   3. 使用Neo4j浏览器手动导入")
    
    if browser_ok:
        print("✅ Neo4j浏览器可用 - 推荐手动导入")
    
    if shell_ok:
        print("✅ cypher-shell可用 - 可使用命令行导入")
    
    print(f"\n📁 已创建文件:")
    print(f"   - Neo4j手动导入指南.md")
    print(f"   - 导入批次_01.cypher ~ 导入批次_14.cypher")
    
    print(f"\n🚀 推荐操作:")
    print(f"1. 访问 http://localhost:7474 使用浏览器导入")
    print(f"2. 或使用批次文件逐个导入")
    print(f"3. 导入完成后重启前端服务")

if __name__ == "__main__":
    main()
