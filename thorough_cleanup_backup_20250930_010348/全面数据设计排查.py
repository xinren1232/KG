#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全面排查词典和关系数据设计问题
分析数据偏差的根本原因
"""

import requests
import json
import time
from neo4j import GraphDatabase
from datetime import datetime
import pandas as pd

def check_neo4j_connection():
    """检查Neo4j连接和认证"""
    print("🔗 检查Neo4j连接...")
    
    uri = "bolt://localhost:7687"
    passwords = ["password123", "neo4j", "admin", "password", "123456"]
    
    for password in passwords:
        try:
            driver = GraphDatabase.driver(uri, auth=("neo4j", password))
            with driver.session() as session:
                result = session.run("RETURN 1 as test")
                test_value = result.single()["test"]
                if test_value == 1:
                    print(f"✅ Neo4j连接成功 (密码: {password})")
                    driver.close()
                    return password
        except Exception as e:
            if "AuthenticationRateLimit" not in str(e):
                print(f"❌ 密码 '{password}' 失败: {str(e)[:100]}")
            continue
    
    print("❌ 无法连接Neo4j")
    return None

def analyze_current_data_structure():
    """分析当前数据结构"""
    print("\n📊 分析当前数据结构...")
    
    password = check_neo4j_connection()
    if not password:
        print("❌ 无法连接Neo4j，跳过数据结构分析")
        return None
    
    try:
        driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", password))
        
        with driver.session() as session:
            # 1. 检查所有标签
            print("\n1. 当前数据库标签:")
            result = session.run("CALL db.labels()")
            labels = [record["label"] for record in result]
            print(f"   标签数量: {len(labels)}")
            for label in sorted(labels):
                count_result = session.run(f"MATCH (n:{label}) RETURN count(n) as count")
                count = count_result.single()["count"]
                print(f"   - {label}: {count} 个节点")
            
            # 2. 检查关系类型
            print("\n2. 当前关系类型:")
            result = session.run("CALL db.relationshipTypes()")
            rel_types = [record["relationshipType"] for record in result]
            print(f"   关系类型数量: {len(rel_types)}")
            for rel_type in sorted(rel_types):
                count_result = session.run(f"MATCH ()-[r:{rel_type}]-() RETURN count(r) as count")
                count = count_result.single()["count"]
                print(f"   - {rel_type}: {count} 个关系")
            
            # 3. 检查Dictionary节点结构
            print("\n3. Dictionary节点结构分析:")
            result = session.run("""
                MATCH (d:Dictionary) 
                RETURN d.category as category, count(*) as count 
                ORDER BY count DESC LIMIT 10
            """)
            
            categories = list(result)
            if categories:
                print("   按类别分布:")
                for record in categories:
                    category = record["category"] or "未分类"
                    count = record["count"]
                    print(f"   - {category}: {count} 个")
            else:
                print("   ❌ 没有找到Dictionary节点")
            
            # 4. 检查重复数据
            print("\n4. 重复数据检查:")
            
            # 检查重复的Dictionary节点
            result = session.run("""
                MATCH (d:Dictionary)
                WITH d.term as term, d.category as category, count(*) as count
                WHERE count > 1
                RETURN term, category, count
                ORDER BY count DESC LIMIT 10
            """)
            
            duplicates = list(result)
            if duplicates:
                print("   发现重复Dictionary节点:")
                for record in duplicates:
                    print(f"   - '{record['term']}' ({record['category']}): {record['count']} 个重复")
            else:
                print("   ✅ 没有发现重复Dictionary节点")
            
            # 5. 检查数据完整性
            print("\n5. 数据完整性检查:")
            
            # 检查缺少必要属性的节点
            result = session.run("""
                MATCH (d:Dictionary)
                WHERE d.term IS NULL OR d.term = ""
                RETURN count(*) as count
            """)
            empty_terms = result.single()["count"]
            if empty_terms > 0:
                print(f"   ❌ 发现 {empty_terms} 个空term的Dictionary节点")
            else:
                print("   ✅ 所有Dictionary节点都有term属性")
            
            # 检查孤立节点
            result = session.run("""
                MATCH (d:Dictionary)
                WHERE NOT (d)-[]-()
                RETURN count(*) as count
            """)
            isolated = result.single()["count"]
            if isolated > 0:
                print(f"   ⚠️ 发现 {isolated} 个孤立的Dictionary节点")
            else:
                print("   ✅ 没有孤立的Dictionary节点")
        
        driver.close()
        return {
            "labels": labels,
            "relationships": rel_types,
            "categories": categories,
            "duplicates": duplicates,
            "empty_terms": empty_terms,
            "isolated": isolated
        }
        
    except Exception as e:
        print(f"❌ 数据结构分析失败: {e}")
        return None

def check_api_data_consistency():
    """检查API数据一致性"""
    print("\n🔍 检查API数据一致性...")
    
    try:
        # 1. 检查词典统计
        print("1. 词典统计检查:")
        response = requests.get("http://localhost:8000/kg/dictionary/stats", timeout=10)
        if response.status_code == 200:
            stats = response.json()
            if stats.get("success"):
                data = stats.get("data", {})
                print(f"   API报告词典条目: {data.get('total_terms', 0)}")
                print(f"   API报告类别数: {data.get('total_categories', 0)}")
                
                categories = data.get("categories", [])
                if categories:
                    print("   类别分布:")
                    for cat in categories[:10]:  # 显示前10个
                        print(f"   - {cat.get('category', '未知')}: {cat.get('count', 0)} 个")
            else:
                print(f"   ❌ API返回错误: {stats.get('message')}")
        else:
            print(f"   ❌ API请求失败: HTTP {response.status_code}")
        
        # 2. 检查图谱统计
        print("\n2. 图谱统计检查:")
        response = requests.get("http://localhost:8000/kg/graph/stats", timeout=10)
        if response.status_code == 200:
            stats = response.json()
            if stats.get("success"):
                data = stats.get("data", {})
                print(f"   API报告节点数: {data.get('total_nodes', 0)}")
                print(f"   API报告关系数: {data.get('total_relationships', 0)}")
                
                node_types = data.get("node_types", [])
                if node_types:
                    print("   节点类型分布:")
                    for nt in node_types:
                        print(f"   - {nt.get('label', '未知')}: {nt.get('count', 0)} 个")
            else:
                print(f"   ❌ API返回错误: {stats.get('message')}")
        else:
            print(f"   ❌ API请求失败: HTTP {response.status_code}")
        
        return True
        
    except Exception as e:
        print(f"❌ API数据一致性检查失败: {e}")
        return False

def identify_data_inconsistency_causes():
    """识别数据不一致的原因"""
    print("\n🔍 识别数据不一致原因...")
    
    potential_causes = []
    
    # 1. 检查配置文件
    print("1. 检查配置文件:")
    config_files = [
        "api/unified_dictionary_config.py",
        "config/system_management_config.json",
        "data/unified_dictionary/schema.json"
    ]
    
    for config_file in config_files:
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if "Dictionary" in content:
                    print(f"   ✅ 找到配置文件: {config_file}")
                else:
                    print(f"   ⚠️ 配置文件可能有问题: {config_file}")
                    potential_causes.append(f"配置文件问题: {config_file}")
        except FileNotFoundError:
            print(f"   ❌ 配置文件不存在: {config_file}")
            potential_causes.append(f"缺少配置文件: {config_file}")
        except Exception as e:
            print(f"   ❌ 读取配置文件失败: {config_file} - {e}")
    
    # 2. 检查数据导入脚本
    print("\n2. 检查数据导入脚本:")
    import_scripts = [
        "导入批次_01.cypher",
        "导入批次_02.cypher", 
        "完整词典补充数据导入脚本.cypher"
    ]
    
    for script in import_scripts:
        try:
            with open(script, 'r', encoding='utf-8') as f:
                content = f.read()
                if "CREATE" in content and "Dictionary" in content:
                    print(f"   ✅ 找到导入脚本: {script}")
                    # 检查是否有重复导入
                    if "MERGE" not in content and content.count("CREATE") > 100:
                        print(f"      ⚠️ 脚本使用CREATE而非MERGE，可能导致重复数据")
                        potential_causes.append(f"重复导入风险: {script}")
        except FileNotFoundError:
            print(f"   ⚠️ 导入脚本不存在: {script}")
        except Exception as e:
            print(f"   ❌ 读取导入脚本失败: {script} - {e}")
    
    # 3. 检查API启动时的数据初始化
    print("\n3. 检查API启动时的数据初始化:")
    try:
        with open("api/main.py", 'r', encoding='utf-8') as f:
            content = f.read()
            if "startup" in content.lower() or "initialize" in content.lower():
                print("   ✅ API有启动初始化逻辑")
                if "dictionary" in content.lower():
                    print("   ⚠️ API启动时可能重新初始化词典数据")
                    potential_causes.append("API启动时重新初始化数据")
            else:
                print("   ✅ API没有启动初始化逻辑")
    except Exception as e:
        print(f"   ❌ 检查API启动逻辑失败: {e}")
    
    return potential_causes

def generate_fix_recommendations(causes, data_analysis):
    """生成修复建议"""
    print("\n💡 修复建议:")
    print("=" * 50)
    
    recommendations = []
    
    # 基于发现的问题生成建议
    if data_analysis and data_analysis.get("duplicates"):
        recommendations.append({
            "问题": "发现重复数据",
            "建议": "执行去重脚本，使用MERGE替代CREATE",
            "优先级": "高"
        })
    
    if data_analysis and data_analysis.get("empty_terms", 0) > 0:
        recommendations.append({
            "问题": "存在空term的节点",
            "建议": "清理无效数据节点",
            "优先级": "中"
        })
    
    if "API启动时重新初始化数据" in causes:
        recommendations.append({
            "问题": "API启动时重复初始化",
            "建议": "修改API启动逻辑，避免重复初始化",
            "优先级": "高"
        })
    
    if any("重复导入" in cause for cause in causes):
        recommendations.append({
            "问题": "导入脚本可能重复执行",
            "建议": "使用MERGE语句替代CREATE，添加唯一性约束",
            "优先级": "高"
        })
    
    # 通用建议
    recommendations.extend([
        {
            "问题": "数据一致性保证",
            "建议": "建立数据版本控制和校验机制",
            "优先级": "中"
        },
        {
            "问题": "启动时数据偏差",
            "建议": "实现幂等性数据初始化",
            "优先级": "高"
        }
    ])
    
    for i, rec in enumerate(recommendations, 1):
        priority_icon = "🔴" if rec["优先级"] == "高" else "🟡" if rec["优先级"] == "中" else "🟢"
        print(f"{i}. {priority_icon} {rec['问题']}")
        print(f"   建议: {rec['建议']}")
        print()
    
    return recommendations

def main():
    """主函数"""
    print("🔍 全面数据设计排查")
    print("=" * 60)
    print(f"🕒 检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 1. 分析当前数据结构
    data_analysis = analyze_current_data_structure()
    
    # 2. 检查API数据一致性
    api_consistent = check_api_data_consistency()
    
    # 3. 识别不一致原因
    causes = identify_data_inconsistency_causes()
    
    # 4. 生成修复建议
    recommendations = generate_fix_recommendations(causes, data_analysis)
    
    # 5. 生成总结报告
    print("\n📋 问题总结:")
    print("=" * 50)
    
    if causes:
        print("🔴 发现的潜在问题:")
        for i, cause in enumerate(causes, 1):
            print(f"   {i}. {cause}")
    else:
        print("✅ 没有发现明显的配置问题")
    
    print(f"\n📊 数据状态:")
    if data_analysis:
        print(f"   - 标签数量: {len(data_analysis.get('labels', []))}")
        print(f"   - 关系类型: {len(data_analysis.get('relationships', []))}")
        print(f"   - 重复数据: {len(data_analysis.get('duplicates', []))}")
        print(f"   - 空term节点: {data_analysis.get('empty_terms', 0)}")
        print(f"   - 孤立节点: {data_analysis.get('isolated', 0)}")
    
    print(f"\n🎯 下一步行动:")
    print("   1. 根据修复建议优先处理高优先级问题")
    print("   2. 实施数据去重和清理")
    print("   3. 修改启动逻辑确保幂等性")
    print("   4. 建立数据一致性监控")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断操作")
    except Exception as e:
        print(f"\n❌ 排查过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
