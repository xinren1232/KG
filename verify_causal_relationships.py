#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证因果关系导入结果
用于服务器端执行
"""

from neo4j import GraphDatabase
import sys

# Neo4j连接配置
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "password123"


def verify_causal_relationships():
    """验证因果关系导入结果"""
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    
    try:
        with driver.session() as session:
            print("=" * 80)
            print("因果关系导入验证报告")
            print("=" * 80)
            
            # 1. 统计CAUSES关系总数
            result = session.run('MATCH ()-[r:CAUSES]->() RETURN count(r) as count')
            total_count = result.single()['count']
            print(f"\n✅ CAUSES关系总数: {total_count}")
            
            # 2. 统计高置信度关系
            result = session.run('''
                MATCH ()-[r:CAUSES]->() 
                WHERE r.confidence >= 0.8 
                RETURN count(r) as count
            ''')
            high_conf = result.single()['count']
            print(f"✅ 高置信度关系(>=0.8): {high_conf} ({high_conf/total_count*100:.1f}%)")
            
            # 3. 统计中置信度关系
            result = session.run('''
                MATCH ()-[r:CAUSES]->() 
                WHERE r.confidence >= 0.6 AND r.confidence < 0.8
                RETURN count(r) as count
            ''')
            mid_conf = result.single()['count']
            print(f"✅ 中置信度关系(0.6-0.8): {mid_conf} ({mid_conf/total_count*100:.1f}%)")
            
            # 4. 置信度分布
            print("\n" + "=" * 80)
            print("置信度分布")
            print("=" * 80)
            result = session.run('''
                MATCH ()-[r:CAUSES]->() 
                RETURN r.confidence as conf, count(*) as count
                ORDER BY r.confidence DESC
            ''')
            for record in result:
                conf = record['conf']
                count = record['count']
                print(f"  置信度 {conf}: {count}个关系")
            
            # 5. 显示前10个高置信度因果关系
            print("\n" + "=" * 80)
            print("前10个高置信度因果关系")
            print("=" * 80)
            result = session.run('''
                MATCH (s:Term)-[r:CAUSES]->(t:Term)
                RETURN s.name as source, t.name as target, r.confidence as confidence
                ORDER BY r.confidence DESC, s.name
                LIMIT 10
            ''')
            for i, record in enumerate(result, 1):
                source = record['source']
                target = record['target']
                confidence = record['confidence']
                print(f"{i:2d}. {source} -> {target}")
                print(f"    置信度: {confidence}")
            
            # 6. 按结果分组统计（找出最常见的结果）
            print("\n" + "=" * 80)
            print("最常见的结果（Top 10）")
            print("=" * 80)
            result = session.run('''
                MATCH ()-[r:CAUSES]->(t:Term)
                RETURN t.name as result, count(r) as cause_count
                ORDER BY cause_count DESC
                LIMIT 10
            ''')
            for i, record in enumerate(result, 1):
                result_name = record['result']
                cause_count = record['cause_count']
                print(f"{i:2d}. {result_name}: {cause_count}个原因")
            
            # 7. 查找因果链（A->B->C）
            print("\n" + "=" * 80)
            print("因果链示例（A导致B，B导致C）")
            print("=" * 80)
            result = session.run('''
                MATCH (a:Term)-[r1:CAUSES]->(b:Term)-[r2:CAUSES]->(c:Term)
                RETURN a.name as cause, b.name as intermediate, c.name as effect,
                       r1.confidence as conf1, r2.confidence as conf2
                ORDER BY (r1.confidence + r2.confidence) DESC
                LIMIT 5
            ''')
            chain_found = False
            for i, record in enumerate(result, 1):
                chain_found = True
                cause = record['cause']
                intermediate = record['intermediate']
                effect = record['effect']
                conf1 = record['conf1']
                conf2 = record['conf2']
                print(f"{i}. {cause} -> {intermediate} -> {effect}")
                print(f"   置信度: {conf1} -> {conf2}")
            
            if not chain_found:
                print("  未发现因果链（这是正常的，因为导入的关系相对独立）")
            
            # 8. 查找特定症状的所有可能原因
            print("\n" + "=" * 80)
            print("示例：屏幕相关问题的原因分析")
            print("=" * 80)
            result = session.run('''
                MATCH (cause:Term)-[r:CAUSES]->(symptom:Term)
                WHERE symptom.name CONTAINS "屏幕"
                RETURN symptom.name as symptom, cause.name as cause, 
                       r.confidence as confidence
                ORDER BY symptom.name, r.confidence DESC
            ''')
            current_symptom = None
            for record in result:
                symptom = record['symptom']
                cause = record['cause']
                confidence = record['confidence']
                
                if symptom != current_symptom:
                    print(f"\n【{symptom}】的可能原因:")
                    current_symptom = symptom
                
                print(f"  - {cause} (置信度: {confidence})")
            
            # 9. 数据质量检查
            print("\n" + "=" * 80)
            print("数据质量检查")
            print("=" * 80)
            
            # 检查是否有缺失证据的关系
            result = session.run('''
                MATCH ()-[r:CAUSES]->()
                WHERE r.evidence IS NULL OR r.evidence = ""
                RETURN count(r) as count
            ''')
            missing_evidence = result.single()['count']
            if missing_evidence == 0:
                print("✅ 所有关系都有证据描述")
            else:
                print(f"⚠️  有 {missing_evidence} 个关系缺少证据描述")
            
            # 检查是否有缺失置信度理由的关系
            result = session.run('''
                MATCH ()-[r:CAUSES]->()
                WHERE r.confidence_reason IS NULL OR r.confidence_reason = ""
                RETURN count(r) as count
            ''')
            missing_reason = result.single()['count']
            if missing_reason == 0:
                print("✅ 所有关系都有置信度评估理由")
            else:
                print(f"⚠️  有 {missing_reason} 个关系缺少置信度理由")
            
            # 10. 平均置信度
            result = session.run('''
                MATCH ()-[r:CAUSES]->()
                RETURN avg(r.confidence) as avg_conf, 
                       min(r.confidence) as min_conf,
                       max(r.confidence) as max_conf
            ''')
            record = result.single()
            avg_conf = record['avg_conf']
            min_conf = record['min_conf']
            max_conf = record['max_conf']
            print(f"\n置信度统计:")
            print(f"  平均值: {avg_conf:.3f}")
            print(f"  最小值: {min_conf}")
            print(f"  最大值: {max_conf}")
            
            print("\n" + "=" * 80)
            print("✅ 验证完成！")
            print("=" * 80)
            
    except Exception as e:
        print(f"\n❌ 验证过程发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        driver.close()
    
    return 0


if __name__ == "__main__":
    sys.exit(verify_causal_relationships())

