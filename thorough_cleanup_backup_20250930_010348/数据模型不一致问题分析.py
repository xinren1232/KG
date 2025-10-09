#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据模型不一致问题深度分析
发现了关键问题：Dictionary节点为0，但Term节点有1275个
"""

from neo4j import GraphDatabase
import requests
import json

def analyze_data_model_mismatch():
    """分析数据模型不匹配问题"""
    print("🔍 数据模型不一致问题深度分析")
    print("=" * 60)
    
    # 连接Neo4j
    try:
        driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password123"))
        
        with driver.session() as session:
            print("📊 关键发现:")
            print("   - Dictionary节点: 0 个")
            print("   - Term节点: 1275 个")
            print("   - 这表明数据模型发生了变化！")
            
            print("\n🔍 详细分析Term节点:")
            
            # 1. 检查Term节点的属性结构
            result = session.run("""
                MATCH (t:Term)
                RETURN keys(t) as properties, count(*) as count
                ORDER BY count DESC
                LIMIT 5
            """)
            
            print("1. Term节点属性结构:")
            for record in result:
                props = record["properties"]
                count = record["count"]
                print(f"   属性组合: {props} - {count} 个节点")
            
            # 2. 检查Term节点的示例数据
            result = session.run("""
                MATCH (t:Term)
                RETURN t.term as term, t.category as category, t.description as description
                LIMIT 10
            """)
            
            print("\n2. Term节点示例数据:")
            terms = list(result)
            for i, record in enumerate(terms, 1):
                term = record["term"]
                category = record["category"]
                description = record["description"]
                print(f"   {i}. {term} ({category}) - {description[:50] if description else 'N/A'}...")
            
            # 3. 检查Term节点的类别分布
            result = session.run("""
                MATCH (t:Term)
                RETURN t.category as category, count(*) as count
                ORDER BY count DESC
                LIMIT 10
            """)
            
            print("\n3. Term节点类别分布:")
            for record in result:
                category = record["category"] or "未分类"
                count = record["count"]
                print(f"   - {category}: {count} 个")
            
            # 4. 检查是否有Dictionary标签的节点被误标记
            result = session.run("""
                MATCH (n)
                WHERE any(label in labels(n) WHERE label CONTAINS 'Dict')
                RETURN labels(n) as labels, count(*) as count
            """)
            
            dict_like = list(result)
            if dict_like:
                print("\n4. 类似Dictionary的标签:")
                for record in dict_like:
                    labels = record["labels"]
                    count = record["count"]
                    print(f"   - {labels}: {count} 个")
            else:
                print("\n4. ❌ 没有找到任何Dictionary相关标签")
            
            # 5. 检查Alias节点（可能是词典的别名）
            result = session.run("""
                MATCH (a:Alias)
                RETURN a.alias as alias, a.canonical_term as canonical_term
                LIMIT 10
            """)
            
            print("\n5. Alias节点示例（可能是词典数据）:")
            aliases = list(result)
            for i, record in enumerate(aliases, 1):
                alias = record["alias"]
                canonical = record["canonical_term"]
                print(f"   {i}. {alias} -> {canonical}")
            
            # 6. 检查关系模式
            result = session.run("""
                MATCH (t:Term)-[r]->(other)
                RETURN type(r) as rel_type, labels(other) as target_labels, count(*) as count
                ORDER BY count DESC
                LIMIT 10
            """)
            
            print("\n6. Term节点的关系模式:")
            for record in result:
                rel_type = record["rel_type"]
                target_labels = record["target_labels"]
                count = record["count"]
                print(f"   - {rel_type} -> {target_labels}: {count} 个")
        
        driver.close()
        
    except Exception as e:
        print(f"❌ Neo4j分析失败: {e}")
        return False
    
    return True

def check_api_endpoints():
    """检查API端点的实际情况"""
    print("\n🔍 检查API端点:")
    
    # 检查所有可能的词典相关端点
    endpoints = [
        "/kg/dictionary/stats",
        "/kg/terms/stats", 
        "/kg/graph/stats",
        "/kg/nodes/stats",
        "/health"
    ]
    
    for endpoint in endpoints:
        try:
            url = f"http://localhost:8000{endpoint}"
            response = requests.get(url, timeout=5)
            print(f"   {endpoint}: HTTP {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if isinstance(data, dict) and "data" in data:
                        print(f"      数据: {str(data['data'])[:100]}...")
                except:
                    print(f"      响应: {response.text[:100]}...")
            
        except Exception as e:
            print(f"   {endpoint}: 连接失败 - {e}")

def identify_root_cause():
    """识别根本原因"""
    print("\n🎯 根本原因分析:")
    print("=" * 40)
    
    print("🔴 发现的关键问题:")
    print("1. 数据模型不一致:")
    print("   - 前端期望: Dictionary节点")
    print("   - 实际数据: Term节点")
    print("   - 这导致前端显示0个词典条目")
    
    print("\n2. API端点不匹配:")
    print("   - 前端调用: /kg/dictionary/stats")
    print("   - API可能期望: /kg/terms/stats")
    
    print("\n3. 数据导入模型变更:")
    print("   - 历史数据使用Term标签")
    print("   - 新设计期望Dictionary标签")
    print("   - 没有进行数据迁移")
    
    print("\n💡 解决方案:")
    print("1. 立即修复方案:")
    print("   - 将Term节点重新标记为Dictionary")
    print("   - 或修改API以支持Term节点")
    
    print("\n2. 长期解决方案:")
    print("   - 统一数据模型定义")
    print("   - 实现数据迁移脚本")
    print("   - 建立模型版本控制")

def generate_immediate_fix():
    """生成立即修复脚本"""
    print("\n🔧 生成立即修复脚本:")
    
    # 方案1: 重新标记节点
    cypher_fix1 = """
// 方案1: 将Term节点重新标记为Dictionary
MATCH (t:Term)
SET t:Dictionary
REMOVE t:Term
RETURN count(*) as migrated_count;
"""
    
    # 方案2: 添加Dictionary标签（保留Term）
    cypher_fix2 = """
// 方案2: 为Term节点添加Dictionary标签
MATCH (t:Term)
SET t:Dictionary
RETURN count(*) as updated_count;
"""
    
    print("Cypher修复脚本已生成:")
    print("方案1 (替换标签):")
    print(cypher_fix1)
    print("\n方案2 (添加标签):")
    print(cypher_fix2)
    
    # 保存修复脚本
    with open("数据模型修复.cypher", "w", encoding="utf-8") as f:
        f.write("// 数据模型不一致修复脚本\n")
        f.write("// 问题: Term节点应该是Dictionary节点\n\n")
        f.write("// 方案1: 替换标签 (推荐)\n")
        f.write(cypher_fix1)
        f.write("\n// 方案2: 添加标签 (保守)\n")
        f.write(cypher_fix2)
    
    print("\n💾 修复脚本已保存到: 数据模型修复.cypher")

def main():
    """主函数"""
    print("🚨 数据模型不一致问题分析")
    print("=" * 60)
    
    # 1. 深度分析数据模型
    if analyze_data_model_mismatch():
        
        # 2. 检查API端点
        check_api_endpoints()
        
        # 3. 识别根本原因
        identify_root_cause()
        
        # 4. 生成修复脚本
        generate_immediate_fix()
        
        print("\n🎯 总结:")
        print("=" * 40)
        print("✅ 问题已识别: Term vs Dictionary 标签不一致")
        print("✅ 修复脚本已生成")
        print("✅ 建议立即执行数据模型修复")
        
        print("\n⚠️ 注意事项:")
        print("- 执行修复前请备份数据")
        print("- 修复后需要重启API服务")
        print("- 验证前端显示是否正常")
    
    else:
        print("❌ 无法完成分析，请检查Neo4j连接")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ 分析过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
