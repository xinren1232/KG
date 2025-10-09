#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复API查询逻辑，统一使用Dictionary标签
"""

import requests
import json
from neo4j import GraphDatabase

def test_current_api_queries():
    """测试当前API查询结果"""
    print("🔍 测试当前API查询结果")
    print("=" * 50)
    
    try:
        driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password123"))
        
        with driver.session() as session:
            # 1. 测试Term查询
            result = session.run("MATCH (t:Term) RETURN count(t) as count")
            term_count = result.single()["count"]
            print(f"📊 Term节点数量: {term_count}")
            
            # 2. 测试Dictionary查询
            result = session.run("MATCH (d:Dictionary) RETURN count(d) as count")
            dict_count = result.single()["count"]
            print(f"📊 Dictionary节点数量: {dict_count}")
            
            # 3. 测试同时具有两个标签的节点
            result = session.run("MATCH (n:Term:Dictionary) RETURN count(n) as count")
            both_count = result.single()["count"]
            print(f"📊 同时具有Term和Dictionary标签的节点: {both_count}")
            
            # 4. 测试API中使用的具体查询
            print("\n🔍 测试API中的具体查询:")
            
            # API中的Term查询
            result = session.run("""
                MATCH (t:Term)
                RETURN t.category AS category, count(t) AS count
                ORDER BY count DESC
            """)
            term_stats = list(result)
            print(f"   Term分类查询结果: {len(term_stats)} 个分类")
            
            # API中的Dictionary查询
            result = session.run("""
                MATCH (d:Dictionary)
                RETURN d.category AS category, count(d) AS count
                ORDER BY count DESC
            """)
            dict_stats = list(result)
            print(f"   Dictionary分类查询结果: {len(dict_stats)} 个分类")
            
            # 5. 检查数据一致性
            if term_count == dict_count == both_count:
                print("✅ 数据一致：所有Term节点都已添加Dictionary标签")
            else:
                print("❌ 数据不一致，需要进一步修复")
        
        driver.close()
        return True
        
    except Exception as e:
        print(f"❌ 查询测试失败: {e}")
        return False

def check_api_real_stats():
    """检查/kg/real-stats API的实际查询"""
    print("\n🔍 检查 /kg/real-stats API")
    print("=" * 40)
    
    try:
        response = requests.get("http://localhost:8000/kg/real-stats", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                stats = data.get("data", {}).get("stats", {})
                print("📊 API返回的统计数据:")
                print(f"   totalTerms: {stats.get('totalTerms', 'N/A')}")
                print(f"   dictEntries: {stats.get('dictEntries', 'N/A')}")
                print(f"   totalNodes: {stats.get('totalNodes', 'N/A')}")
                print(f"   totalRelations: {stats.get('totalRelations', 'N/A')}")
                
                # 检查为什么dictEntries可能为0
                if stats.get('dictEntries', 0) == 0:
                    print("❌ dictEntries为0，可能API查询有问题")
                    return False
                else:
                    print("✅ dictEntries正常")
                    return True
            else:
                print(f"❌ API返回失败: {data.get('message')}")
        else:
            print(f"❌ API请求失败: HTTP {response.status_code}")
        
        return False
        
    except Exception as e:
        print(f"❌ API检查失败: {e}")
        return False

def fix_api_queries_in_database():
    """在数据库层面确保查询一致性"""
    print("\n🔧 修复数据库查询一致性")
    print("=" * 40)
    
    try:
        driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password123"))
        
        with driver.session() as session:
            # 确保所有Term节点都有Dictionary标签
            result = session.run("""
                MATCH (t:Term)
                WHERE NOT t:Dictionary
                SET t:Dictionary
                RETURN count(t) as updated
            """)
            updated = result.single()["updated"]
            if updated > 0:
                print(f"✅ 为 {updated} 个Term节点添加了Dictionary标签")
            else:
                print("✅ 所有Term节点都已有Dictionary标签")
            
            # 验证最终结果
            result = session.run("""
                MATCH (d:Dictionary)
                WITH count(d) as dict_count
                MATCH (t:Term)
                WITH dict_count, count(t) as term_count
                RETURN dict_count, term_count
            """)
            counts = result.single()
            dict_count = counts["dict_count"]
            term_count = counts["term_count"]
            
            print(f"📊 最终统计:")
            print(f"   Dictionary节点: {dict_count}")
            print(f"   Term节点: {term_count}")
            
            if dict_count == term_count:
                print("✅ 数据一致性修复成功")
                return True
            else:
                print("❌ 数据仍不一致")
                return False
        
        driver.close()
        
    except Exception as e:
        print(f"❌ 数据库修复失败: {e}")
        return False

def restart_api_service():
    """重启API服务以应用修复"""
    print("\n🔄 建议重启API服务")
    print("=" * 40)
    
    print("💡 重启API服务的方法:")
    print("   1. 在API服务窗口按 Ctrl+C 停止")
    print("   2. 重新运行: python api/main.py")
    print("   3. 或者运行: python 快速启动API.py")
    
    print("\n⚠️ 重启后需要验证:")
    print("   1. API服务正常启动")
    print("   2. /kg/real-stats 返回正确数据")
    print("   3. 前端显示正确的词典条目数")

def generate_verification_script():
    """生成验证脚本"""
    print("\n📝 生成验证脚本")
    print("=" * 40)
    
    verification_script = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证数据模型修复效果
"""

import requests
import json

def verify_fix():
    """验证修复效果"""
    print("🔍 验证数据模型修复效果")
    
    # 1. 检查API统计
    try:
        response = requests.get("http://localhost:8000/kg/real-stats", timeout=10)
        if response.status_code == 200:
            data = response.json()
            stats = data.get("data", {}).get("stats", {})
            
            dict_entries = stats.get("dictEntries", 0)
            total_terms = stats.get("totalTerms", 0)
            
            print(f"📊 词典条目数: {dict_entries}")
            print(f"📊 Term节点数: {total_terms}")
            
            if dict_entries > 0 and dict_entries == total_terms:
                print("✅ 修复成功！词典条目数正常")
                return True
            else:
                print("❌ 修复失败，词典条目数仍为0")
                return False
        else:
            print("❌ API请求失败")
            return False
    except Exception as e:
        print(f"❌ 验证失败: {e}")
        return False

if __name__ == "__main__":
    verify_fix()
'''
    
    with open("验证修复效果.py", "w", encoding="utf-8") as f:
        f.write(verification_script)
    
    print("💾 验证脚本已保存到: 验证修复效果.py")

def main():
    """主函数"""
    print("🔧 修复API查询逻辑")
    print("=" * 60)
    
    # 1. 测试当前查询状态
    if test_current_api_queries():
        
        # 2. 检查API实际返回
        api_ok = check_api_real_stats()
        
        # 3. 修复数据库查询一致性
        if fix_api_queries_in_database():
            
            # 4. 再次检查API
            if not api_ok:
                print("\n🔄 数据库修复完成，但API可能需要重启")
                restart_api_service()
            
            # 5. 生成验证脚本
            generate_verification_script()
            
            print("\n🎯 总结:")
            print("✅ 数据模型已修复：所有Term节点都有Dictionary标签")
            print("✅ 数据库查询一致性已确保")
            print("⚠️ 如果前端仍显示0，请重启API服务")
            
        else:
            print("\n❌ 数据库修复失败")
    
    else:
        print("\n❌ 查询测试失败，无法继续修复")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ 修复过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
