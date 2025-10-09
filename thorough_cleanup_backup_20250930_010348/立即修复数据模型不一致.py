#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
立即修复数据模型不一致问题
问题：前端期望Dictionary节点，但数据库中是Term节点
"""

from neo4j import GraphDatabase
import requests
import json
import time

def execute_data_model_fix():
    """执行数据模型修复"""
    print("🔧 执行数据模型修复")
    print("=" * 50)
    
    try:
        driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password123"))
        
        with driver.session() as session:
            # 1. 备份当前Term节点数量
            result = session.run("MATCH (t:Term) RETURN count(t) as count")
            term_count = result.single()["count"]
            print(f"📊 发现 {term_count} 个Term节点需要转换")
            
            if term_count == 0:
                print("✅ 没有Term节点需要转换")
                return True
            
            # 2. 执行标签转换 - 添加Dictionary标签
            print("\n🔄 添加Dictionary标签...")
            result = session.run("""
                MATCH (t:Term)
                SET t:Dictionary
                RETURN count(t) as updated_count
            """)
            updated_count = result.single()["updated_count"]
            print(f"✅ 已为 {updated_count} 个节点添加Dictionary标签")
            
            # 3. 验证转换结果
            print("\n🔍 验证转换结果...")
            result = session.run("MATCH (d:Dictionary) RETURN count(d) as count")
            dict_count = result.single()["count"]
            print(f"📊 现在有 {dict_count} 个Dictionary节点")
            
            # 4. 检查Dictionary节点的属性
            result = session.run("""
                MATCH (d:Dictionary)
                RETURN d.category as category, count(*) as count
                ORDER BY count DESC
                LIMIT 10
            """)
            
            print("\n📋 Dictionary节点类别分布:")
            categories = list(result)
            for record in categories:
                category = record["category"] or "未分类"
                count = record["count"]
                print(f"   - {category}: {count} 个")
            
            # 5. 检查是否还需要保留Term标签
            print(f"\n❓ 是否移除Term标签？")
            print("   保留Term标签：节点同时具有Term和Dictionary标签")
            print("   移除Term标签：节点只有Dictionary标签")
            
            # 暂时保留Term标签，确保兼容性
            print("✅ 暂时保留Term标签以确保兼容性")
            
        driver.close()
        return True
        
    except Exception as e:
        print(f"❌ 数据模型修复失败: {e}")
        return False

def test_api_after_fix():
    """修复后测试API"""
    print("\n🧪 测试API修复效果")
    print("=" * 40)
    
    # 等待一下让数据生效
    time.sleep(2)
    
    # 测试各种API端点
    endpoints_to_test = [
        "/kg/real-stats",
        "/kg/stats", 
        "/kg/dictionary/statistics",
        "/api/dictionary"
    ]
    
    for endpoint in endpoints_to_test:
        try:
            url = f"http://localhost:8000{endpoint}"
            response = requests.get(url, timeout=10)
            print(f"📡 {endpoint}: HTTP {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if "data" in data:
                        stats = data.get("data", {}).get("stats", {})
                        if stats:
                            print(f"   📊 节点数: {stats.get('totalNodes', stats.get('dictEntries', 'N/A'))}")
                            print(f"   🔗 关系数: {stats.get('totalRelations', 'N/A')}")
                        else:
                            print(f"   📄 数据: {str(data)[:100]}...")
                except json.JSONDecodeError:
                    print(f"   📄 响应: {response.text[:100]}...")
            else:
                print(f"   ❌ 请求失败")
                
        except Exception as e:
            print(f"   ❌ 连接失败: {e}")

def verify_frontend_data():
    """验证前端数据显示"""
    print("\n🌐 验证前端数据显示")
    print("=" * 40)
    
    try:
        # 检查图谱数据API
        response = requests.get("http://localhost:8000/kg/real-stats", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                stats = data.get("data", {}).get("stats", {})
                print("✅ 前端应该显示:")
                print(f"   📊 词典条目: {stats.get('dictEntries', stats.get('totalTerms', 0))}")
                print(f"   🔗 关系数量: {stats.get('totalRelations', 0)}")
                print(f"   📁 分类数量: {stats.get('totalCategories', 0)}")
                print(f"   🏷️ 标签数量: {stats.get('totalTags', 0)}")
                
                return True
        
        print("❌ 无法获取前端数据")
        return False
        
    except Exception as e:
        print(f"❌ 验证前端数据失败: {e}")
        return False

def create_api_endpoint_fix():
    """创建API端点修复建议"""
    print("\n💡 API端点修复建议")
    print("=" * 40)
    
    print("🔧 需要确保以下API端点正常工作:")
    print("   1. /kg/dictionary/stats - 词典统计")
    print("   2. /kg/graph/stats - 图谱统计") 
    print("   3. /kg/real-stats - 实时统计")
    
    print("\n📝 建议的API修复:")
    print("   1. 统一使用Dictionary标签查询")
    print("   2. 确保API返回正确的数据结构")
    print("   3. 修复404错误的端点")
    
    # 生成API修复脚本
    api_fix_content = '''
# API端点修复建议

## 问题
- 前端调用 /kg/dictionary/stats 返回404
- 前端调用 /kg/graph/stats 返回404
- 数据模型不一致：Term vs Dictionary

## 修复方案
1. 确保API查询使用Dictionary标签
2. 添加缺失的API端点
3. 统一数据模型

## 修复后的查询
```cypher
// 使用Dictionary标签而不是Term
MATCH (d:Dictionary)
RETURN d.category as category, count(d) as count
ORDER BY count DESC
```
'''
    
    with open("API端点修复建议.md", "w", encoding="utf-8") as f:
        f.write(api_fix_content)
    
    print("💾 API修复建议已保存到: API端点修复建议.md")

def main():
    """主函数"""
    print("🚨 立即修复数据模型不一致问题")
    print("=" * 60)
    print("问题：前端期望Dictionary节点，但数据库中是Term节点")
    print("解决：为Term节点添加Dictionary标签")
    print()
    
    # 1. 执行数据模型修复
    if execute_data_model_fix():
        print("\n✅ 数据模型修复完成")
        
        # 2. 测试API修复效果
        test_api_after_fix()
        
        # 3. 验证前端数据
        if verify_frontend_data():
            print("\n🎉 修复成功！前端应该能正常显示数据了")
        else:
            print("\n⚠️ 前端数据验证失败，可能需要重启服务")
        
        # 4. 生成API修复建议
        create_api_endpoint_fix()
        
        print("\n🎯 下一步:")
        print("   1. 刷新前端页面查看效果")
        print("   2. 如果仍有问题，重启API服务")
        print("   3. 检查API端点是否需要进一步修复")
        
    else:
        print("\n❌ 数据模型修复失败")
        print("请检查Neo4j连接和权限")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断操作")
    except Exception as e:
        print(f"\n❌ 修复过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
