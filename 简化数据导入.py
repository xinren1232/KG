#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化的数据导入脚本 - 尝试多种连接方式
"""

import requests
import json
import time
from datetime import datetime

def try_import_with_different_auth():
    """尝试使用不同认证方式导入数据"""
    print("🔄 尝试使用不同认证方式导入数据...")
    
    # 先执行一个简单的查询来测试连接
    test_query = "MATCH (n) RETURN count(n) as total"
    
    # 尝试不同的认证方式
    auth_methods = [
        None,  # 无认证
        ("neo4j", "neo4j"),
        ("neo4j", "password"),
        ("neo4j", "123456"),
        ("neo4j", "admin"),
        ("", ""),
    ]
    
    for auth in auth_methods:
        print(f"🔑 尝试认证: {auth}")
        
        try:
            url = "http://localhost:7474/db/data/transaction/commit"
            headers = {"Content-Type": "application/json"}
            
            payload = {
                "statements": [
                    {
                        "statement": test_query,
                        "resultDataContents": ["row"]
                    }
                ]
            }
            
            response = requests.post(
                url, 
                json=payload, 
                headers=headers, 
                auth=auth, 
                timeout=10
            )
            
            print(f"   状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                if not result.get("errors"):
                    count = result["results"][0]["data"][0]["row"][0]
                    print(f"✅ 连接成功! 当前节点数: {count}")
                    return auth
                else:
                    print(f"❌ 查询错误: {result['errors']}")
            elif response.status_code == 429:
                print("⏰ 请求过于频繁，等待5秒...")
                time.sleep(5)
            else:
                print(f"❌ HTTP错误: {response.status_code}")
                
        except Exception as e:
            print(f"❌ 连接异常: {e}")
    
    return None

def import_single_batch(auth, batch_file):
    """导入单个批次文件"""
    print(f"📄 导入批次文件: {batch_file}")
    
    try:
        with open(batch_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取CREATE语句
        statements = []
        for line in content.split('\n'):
            line = line.strip()
            if line and not line.startswith('//') and line.endswith(');'):
                statements.append(line)
        
        if not statements:
            print("❌ 未找到有效的CREATE语句")
            return False
        
        print(f"📊 找到 {len(statements)} 条CREATE语句")
        
        # 执行导入
        url = "http://localhost:7474/db/data/transaction/commit"
        headers = {"Content-Type": "application/json"}
        
        payload = {
            "statements": [
                {
                    "statement": '\n'.join(statements),
                    "resultDataContents": ["row"]
                }
            ]
        }
        
        response = requests.post(
            url, 
            json=payload, 
            headers=headers, 
            auth=auth, 
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            if not result.get("errors"):
                print(f"✅ 批次导入成功: {len(statements)} 条语句")
                return True
            else:
                print(f"❌ 导入错误: {result['errors']}")
                return False
        else:
            print(f"❌ HTTP错误: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 导入异常: {e}")
        return False

def main():
    """主函数"""
    print("🚀 简化数据导入")
    print("=" * 40)
    
    # 1. 尝试找到可用的认证方式
    auth = try_import_with_different_auth()
    
    if not auth:
        print("❌ 无法连接到Neo4j")
        print("💡 请检查:")
        print("   1. Neo4j服务是否运行")
        print("   2. 端口7474是否可访问")
        print("   3. 认证设置是否正确")
        print("   4. 尝试在浏览器中访问 http://localhost:7474")
        return
    
    print(f"✅ 使用认证: {auth}")
    
    # 2. 获取导入前状态
    print("\n📊 获取导入前状态...")
    try:
        url = "http://localhost:7474/db/data/transaction/commit"
        headers = {"Content-Type": "application/json"}
        payload = {
            "statements": [
                {
                    "statement": "MATCH (n) RETURN count(n) as total",
                    "resultDataContents": ["row"]
                }
            ]
        }
        
        response = requests.post(url, json=payload, headers=headers, auth=auth, timeout=10)
        if response.status_code == 200:
            result = response.json()
            before_count = result["results"][0]["data"][0]["row"][0]
            print(f"导入前节点数: {before_count}")
        else:
            before_count = 0
            print("无法获取导入前节点数")
    except:
        before_count = 0
        print("无法获取导入前节点数")
    
    # 3. 导入第一个批次作为测试
    print(f"\n🔄 测试导入第一个批次...")
    success = import_single_batch(auth, "导入批次_01.cypher")
    
    if success:
        print(f"✅ 测试导入成功!")
        
        # 获取导入后状态
        try:
            response = requests.post(url, json=payload, headers=headers, auth=auth, timeout=10)
            if response.status_code == 200:
                result = response.json()
                after_count = result["results"][0]["data"][0]["row"][0]
                added = after_count - before_count
                print(f"导入后节点数: {after_count}")
                print(f"新增节点数: {added}")
                
                if added > 0:
                    print(f"\n🎉 成功导入 {added} 条数据!")
                    
                    # 询问是否继续导入其他批次
                    print(f"\n💡 继续导入其他批次:")
                    print(f"   还有13个批次文件需要导入")
                    print(f"   可以手动在Neo4j浏览器中执行")
                    print(f"   或运行此脚本导入其他批次")
                else:
                    print(f"⚠️ 未检测到新增数据，可能存在重复")
            else:
                print("无法获取导入后状态")
        except:
            print("无法获取导入后状态")
    else:
        print(f"❌ 测试导入失败")
    
    print(f"\n📁 批次文件列表:")
    for i in range(1, 15):
        print(f"   导入批次_{i:02d}.cypher")
    
    print(f"\n💡 下一步:")
    print(f"1. 在Neo4j浏览器中逐个执行批次文件")
    print(f"2. 或修改此脚本批量导入所有批次")
    print(f"3. 导入完成后重启前端服务")

if __name__ == "__main__":
    main()
