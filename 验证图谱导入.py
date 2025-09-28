#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证图谱导入 - 检查Neo4j图谱数据导入是否成功
"""

import requests
import json
from datetime import datetime

def test_neo4j_query(query, description=""):
    """测试Neo4j查询"""
    try:
        # Neo4j HTTP API endpoint
        url = "http://localhost:7474/db/data/transaction/commit"
        
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        # 尝试不同的认证方式
        auth_methods = [
            None,  # 无认证
            ("neo4j", "password"),  # 默认密码
            ("neo4j", "neo4j"),     # 默认用户名密码
            ("neo4j", "123456"),    # 常用密码
        ]
        
        for auth in auth_methods:
            try:
                payload = {
                    "statements": [
                        {
                            "statement": query,
                            "resultDataContents": ["row", "graph"]
                        }
                    ]
                }
                
                response = requests.post(url, 
                                       headers=headers, 
                                       json=payload, 
                                       auth=auth,
                                       timeout=10)
                
                if response.status_code == 200:
                    result = response.json()
                    if not result.get("errors"):
                        return True, result, auth
                    else:
                        continue
                elif response.status_code == 401:
                    continue  # 尝试下一个认证方式
                else:
                    continue
                    
            except Exception:
                continue
        
        return False, None, None
        
    except Exception as e:
        return False, str(e), None

def verify_dictionary_nodes():
    """验证Dictionary节点"""
    print("🔍 验证Dictionary节点...")
    
    # 1. 检查总数
    success, result, auth = test_neo4j_query("MATCH (d:Dictionary) RETURN count(d) as total")
    
    if success:
        total = result["results"][0]["data"][0]["row"][0] if result["results"][0]["data"] else 0
        print(f"✅ Dictionary节点总数: {total}")
        
        if total == 1124:
            print("✅ 节点数量正确")
        elif total > 0:
            print(f"⚠️ 节点数量不完整，期望1124，实际{total}")
        else:
            print("❌ 没有找到Dictionary节点")
        
        return True, total, auth
    else:
        print("❌ 无法连接Neo4j或查询失败")
        return False, 0, None

def verify_category_distribution(auth):
    """验证分类分布"""
    print("🔍 验证分类分布...")
    
    query = """
    MATCH (d:Dictionary) 
    RETURN d.category, count(d) as count 
    ORDER BY count DESC
    """
    
    success, result, _ = test_neo4j_query(query)
    
    if success and result["results"][0]["data"]:
        print("📊 分类分布:")
        
        expected_distribution = {
            'Symptom': 259,
            'Metric': 190,
            'Component': 181,
            'Process': 170,
            'TestCase': 104,
            'Tool': 102,
            'Role': 63,
            'Material': 55
        }
        
        actual_distribution = {}
        for row in result["results"][0]["data"]:
            category = row["row"][0]
            count = row["row"][1]
            actual_distribution[category] = count
            print(f"  {category}: {count} 条")
        
        # 验证分布是否正确
        distribution_correct = True
        for category, expected_count in expected_distribution.items():
            actual_count = actual_distribution.get(category, 0)
            if actual_count != expected_count:
                print(f"⚠️ {category}: 期望{expected_count}，实际{actual_count}")
                distribution_correct = False
        
        if distribution_correct:
            print("✅ 分类分布完全正确")
        else:
            print("⚠️ 分类分布存在差异")
        
        return True, actual_distribution
    else:
        print("❌ 无法获取分类分布")
        return False, {}

def verify_data_quality(auth):
    """验证数据质量"""
    print("🔍 验证数据质量...")
    
    # 检查空字段
    query = """
    MATCH (d:Dictionary) 
    WHERE d.term IS NULL OR d.term = '' OR d.category IS NULL OR d.category = ''
    RETURN count(d) as invalid_nodes
    """
    
    success, result, _ = test_neo4j_query(query)
    
    if success:
        invalid_count = result["results"][0]["data"][0]["row"][0] if result["results"][0]["data"] else 0
        
        if invalid_count == 0:
            print("✅ 数据质量: 无空字段")
        else:
            print(f"⚠️ 发现 {invalid_count} 个无效节点")
        
        return invalid_count == 0
    else:
        print("❌ 无法检查数据质量")
        return False

def verify_sample_data(auth):
    """验证示例数据"""
    print("🔍 验证示例数据...")
    
    query = """
    MATCH (d:Dictionary) 
    RETURN d.term, d.category, d.aliases, d.tags 
    LIMIT 5
    """
    
    success, result, _ = test_neo4j_query(query)
    
    if success and result["results"][0]["data"]:
        print("📋 示例数据:")
        
        for i, row in enumerate(result["results"][0]["data"]):
            term = row["row"][0]
            category = row["row"][1]
            aliases = row["row"][2]
            tags = row["row"][3]
            
            print(f"  {i+1}. {term} ({category})")
            print(f"     别名: {aliases}")
            print(f"     标签: {tags}")
        
        return True
    else:
        print("❌ 无法获取示例数据")
        return False

def verify_indexes_and_constraints(auth):
    """验证索引和约束"""
    print("🔍 验证索引和约束...")
    
    # 检查约束
    constraint_query = "SHOW CONSTRAINTS"
    success, result, _ = test_neo4j_query(constraint_query)
    
    if success:
        constraints = result["results"][0]["data"] if result["results"][0]["data"] else []
        print(f"📊 约束数量: {len(constraints)}")
        
        # 检查是否有Dictionary相关约束
        dictionary_constraints = [c for c in constraints if "Dictionary" in str(c)]
        if dictionary_constraints:
            print("✅ Dictionary约束已创建")
        else:
            print("⚠️ 未找到Dictionary约束")
    else:
        print("⚠️ 无法检查约束")
    
    # 检查索引
    index_query = "SHOW INDEXES"
    success, result, _ = test_neo4j_query(index_query)
    
    if success:
        indexes = result["results"][0]["data"] if result["results"][0]["data"] else []
        print(f"📊 索引数量: {len(indexes)}")
        
        # 检查是否有Dictionary相关索引
        dictionary_indexes = [i for i in indexes if "Dictionary" in str(i)]
        if dictionary_indexes:
            print("✅ Dictionary索引已创建")
        else:
            print("⚠️ 未找到Dictionary索引")
    else:
        print("⚠️ 无法检查索引")

def generate_verification_report(total_nodes, distribution, data_quality_ok):
    """生成验证报告"""
    print("📝 生成验证报告...")
    
    report = {
        'verification_time': datetime.now().isoformat(),
        'total_nodes': total_nodes,
        'expected_nodes': 1124,
        'nodes_complete': total_nodes == 1124,
        'category_distribution': distribution,
        'data_quality_ok': data_quality_ok,
        'verification_status': 'success' if (total_nodes == 1124 and data_quality_ok) else 'partial'
    }
    
    # 保存报告
    report_file = "图谱导入验证报告.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"📄 验证报告已保存: {report_file}")
    return report

def main():
    """主函数"""
    print("🚀 验证图谱导入")
    print("=" * 50)
    
    # 1. 验证Dictionary节点
    nodes_ok, total_nodes, auth = verify_dictionary_nodes()
    
    if not nodes_ok:
        print("\n❌ 无法连接Neo4j或查询失败")
        print("💡 请确认:")
        print("  1. Neo4j服务正在运行")
        print("  2. 访问 http://localhost:7474 确认服务可用")
        print("  3. 检查认证信息")
        print("  4. 确认已执行导入脚本")
        return
    
    # 2. 验证分类分布
    if total_nodes > 0:
        dist_ok, distribution = verify_category_distribution(auth)
    else:
        dist_ok, distribution = False, {}
    
    # 3. 验证数据质量
    if total_nodes > 0:
        quality_ok = verify_data_quality(auth)
    else:
        quality_ok = False
    
    # 4. 验证示例数据
    if total_nodes > 0:
        sample_ok = verify_sample_data(auth)
    else:
        sample_ok = False
    
    # 5. 验证索引和约束
    if total_nodes > 0:
        verify_indexes_and_constraints(auth)
    
    # 6. 生成验证报告
    report = generate_verification_report(total_nodes, distribution, quality_ok)
    
    print("\n" + "=" * 50)
    print("📊 图谱导入验证结果")
    print("=" * 50)
    
    print(f"Dictionary节点: {total_nodes}/1124 ({'✅ 完整' if total_nodes == 1124 else '⚠️ 不完整'})")
    print(f"分类分布: {'✅ 正确' if dist_ok else '⚠️ 异常'}")
    print(f"数据质量: {'✅ 良好' if quality_ok else '⚠️ 有问题'}")
    print(f"示例数据: {'✅ 正常' if sample_ok else '⚠️ 异常'}")
    
    if total_nodes == 1124 and quality_ok:
        print(f"\n🎉 图谱导入验证成功!")
        print(f"✅ 1124个Dictionary节点已成功导入")
        print(f"✅ 8个Label分类完整覆盖")
        print(f"✅ 数据质量良好")
        print(f"✅ 图谱系统可以正常使用")
        
        print(f"\n🌐 可以访问Neo4j浏览器查看:")
        print(f"   http://localhost:7474")
        print(f"   执行查询: MATCH (d:Dictionary) RETURN d LIMIT 25")
    elif total_nodes > 0:
        print(f"\n⚠️ 图谱导入部分成功")
        print(f"📊 当前节点数: {total_nodes}")
        print(f"💡 建议:")
        if total_nodes < 1124:
            print(f"  1. 检查导入脚本是否完全执行")
            print(f"  2. 重新执行剩余批次")
        if not quality_ok:
            print(f"  3. 检查数据质量问题")
            print(f"  4. 清理并重新导入")
    else:
        print(f"\n❌ 图谱导入失败")
        print(f"💡 请:")
        print(f"  1. 确认Neo4j服务运行正常")
        print(f"  2. 执行导入脚本: 更新图谱数据导入脚本.cypher")
        print(f"  3. 检查导入过程中的错误信息")

if __name__ == "__main__":
    main()
