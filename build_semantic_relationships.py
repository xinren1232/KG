#!/usr/bin/env python3
"""
自动建立语义关系脚本
基于词条描述、标签、别名自动匹配并建立关系
"""
import json
import re
from collections import defaultdict
from neo4j import GraphDatabase

# Neo4j连接配置
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "password123"

# 加载词典数据
with open('api/data/dictionary.json', 'r', encoding='utf-8') as f:
    dictionary = json.load(f)

# 按分类组织数据
data_by_category = defaultdict(list)
for entry in dictionary:
    data_by_category[entry['category']].append(entry)

# 创建术语索引（用于快速查找）
term_index = {entry['term']: entry for entry in dictionary}
alias_index = {}
for entry in dictionary:
    for alias in entry.get('aliases', []):
        alias_index[alias.lower()] = entry['term']

print("=" * 80)
print("🔗 自动建立语义关系")
print("=" * 80)

# 1. Symptom → Component (AFFECTS)
print("\n1️⃣ 建立 Symptom → Component (AFFECTS) 关系")
print("-" * 80)

symptom_component_relations = []

for symptom in data_by_category['Symptom']:
    symptom_term = symptom['term']
    symptom_desc = symptom.get('description', '').lower()
    symptom_tags = set(symptom.get('tags', []))
    
    # 在描述中查找组件名称
    for component in data_by_category['Component']:
        component_term = component['term']
        component_tags = set(component.get('tags', []))
        
        # 匹配条件
        match_score = 0
        
        # 1. 描述中直接提到组件名称
        if component_term.lower() in symptom_desc:
            match_score += 10
        
        # 2. 描述中提到组件别名
        for alias in component.get('aliases', []):
            if alias.lower() in symptom_desc:
                match_score += 8
                break
        
        # 3. 标签重叠度
        common_tags = symptom_tags & component_tags
        if common_tags:
            match_score += len(common_tags) * 2
        
        # 如果匹配分数足够高，建立关系
        if match_score >= 8:
            symptom_component_relations.append({
                'from': symptom_term,
                'to': component_term,
                'score': match_score,
                'reason': f"描述匹配 + {len(common_tags)}个共同标签"
            })

print(f"发现 {len(symptom_component_relations)} 条潜在关系")
print(f"Top 10 高分关系:")
for rel in sorted(symptom_component_relations, key=lambda x: x['score'], reverse=True)[:10]:
    print(f"  {rel['from']:20s} -[AFFECTS]-> {rel['to']:20s} (分数:{rel['score']}, {rel['reason']})")

# 2. TestCase → Component (TESTS)
print("\n2️⃣ 建立 TestCase → Component (TESTS) 关系")
print("-" * 80)

testcase_component_relations = []

for testcase in data_by_category['TestCase']:
    testcase_term = testcase['term']
    testcase_desc = testcase.get('description', '').lower()
    testcase_tags = set(testcase.get('tags', []))
    
    for component in data_by_category['Component']:
        component_term = component['term']
        component_tags = set(component.get('tags', []))
        
        match_score = 0
        
        # 描述匹配
        if component_term.lower() in testcase_desc:
            match_score += 10
        
        for alias in component.get('aliases', []):
            if alias.lower() in testcase_desc:
                match_score += 8
                break
        
        # 标签匹配
        common_tags = testcase_tags & component_tags
        if common_tags:
            match_score += len(common_tags) * 2
        
        if match_score >= 8:
            testcase_component_relations.append({
                'from': testcase_term,
                'to': component_term,
                'score': match_score,
                'reason': f"描述匹配 + {len(common_tags)}个共同标签"
            })

print(f"发现 {len(testcase_component_relations)} 条潜在关系")
print(f"Top 10 高分关系:")
for rel in sorted(testcase_component_relations, key=lambda x: x['score'], reverse=True)[:10]:
    print(f"  {rel['from']:20s} -[TESTS]-> {rel['to']:20s} (分数:{rel['score']}, {rel['reason']})")

# 3. Tool → TestCase (USED_IN)
print("\n3️⃣ 建立 Tool → TestCase (USED_IN) 关系")
print("-" * 80)

tool_testcase_relations = []

for tool in data_by_category['Tool']:
    tool_term = tool['term']
    tool_desc = tool.get('description', '').lower()
    tool_tags = set(tool.get('tags', []))
    
    for testcase in data_by_category['TestCase']:
        testcase_term = testcase['term']
        testcase_desc = testcase.get('description', '').lower()
        testcase_tags = set(testcase.get('tags', []))
        
        match_score = 0
        
        # 测试用例描述中提到工具
        if tool_term.lower() in testcase_desc:
            match_score += 10
        
        for alias in tool.get('aliases', []):
            if alias.lower() in testcase_desc:
                match_score += 8
                break
        
        # 工具描述中提到测试
        if testcase_term.lower() in tool_desc:
            match_score += 10
        
        # 标签匹配
        common_tags = tool_tags & testcase_tags
        if common_tags:
            match_score += len(common_tags) * 2
        
        if match_score >= 8:
            tool_testcase_relations.append({
                'from': tool_term,
                'to': testcase_term,
                'score': match_score,
                'reason': f"描述匹配 + {len(common_tags)}个共同标签"
            })

print(f"发现 {len(tool_testcase_relations)} 条潜在关系")
print(f"Top 10 高分关系:")
for rel in sorted(tool_testcase_relations, key=lambda x: x['score'], reverse=True)[:10]:
    print(f"  {rel['from']:20s} -[USED_IN]-> {rel['to']:20s} (分数:{rel['score']}, {rel['reason']})")

# 4. Process → Component (PRODUCES)
print("\n4️⃣ 建立 Process → Component (PRODUCES) 关系")
print("-" * 80)

process_component_relations = []

for process in data_by_category['Process']:
    process_term = process['term']
    process_desc = process.get('description', '').lower()
    process_tags = set(process.get('tags', []))
    
    for component in data_by_category['Component']:
        component_term = component['term']
        component_desc = component.get('description', '').lower()
        component_tags = set(component.get('tags', []))
        
        match_score = 0
        
        # 工艺描述中提到组件
        if component_term.lower() in process_desc:
            match_score += 10
        
        # 组件描述中提到工艺
        if process_term.lower() in component_desc:
            match_score += 10
        
        # 标签匹配
        common_tags = process_tags & component_tags
        if common_tags:
            match_score += len(common_tags) * 2
        
        if match_score >= 8:
            process_component_relations.append({
                'from': process_term,
                'to': component_term,
                'score': match_score,
                'reason': f"描述匹配 + {len(common_tags)}个共同标签"
            })

print(f"发现 {len(process_component_relations)} 条潜在关系")
print(f"Top 10 高分关系:")
for rel in sorted(process_component_relations, key=lambda x: x['score'], reverse=True)[:10]:
    print(f"  {rel['from']:20s} -[PRODUCES]-> {rel['to']:20s} (分数:{rel['score']}, {rel['reason']})")

# 统计总结
print("\n" + "=" * 80)
print("📊 关系发现总结")
print("=" * 80)

total_relations = (
    len(symptom_component_relations) +
    len(testcase_component_relations) +
    len(tool_testcase_relations) +
    len(process_component_relations)
)

print(f"\n总计发现 {total_relations} 条潜在关系:")
print(f"  Symptom → Component (AFFECTS):  {len(symptom_component_relations):4d} 条")
print(f"  TestCase → Component (TESTS):   {len(testcase_component_relations):4d} 条")
print(f"  Tool → TestCase (USED_IN):      {len(tool_testcase_relations):4d} 条")
print(f"  Process → Component (PRODUCES): {len(process_component_relations):4d} 条")

# 保存关系数据
relationships_data = {
    'symptom_component': symptom_component_relations,
    'testcase_component': testcase_component_relations,
    'tool_testcase': tool_testcase_relations,
    'process_component': process_component_relations
}

with open('semantic_relationships.json', 'w', encoding='utf-8') as f:
    json.dump(relationships_data, f, ensure_ascii=False, indent=2)

print(f"\n✅ 关系数据已保存到 semantic_relationships.json")

# 导入到Neo4j（可选）
print("\n" + "=" * 80)
print("是否导入到Neo4j? (需要人工审核后再导入)")
print("=" * 80)
print("\n建议:")
print("1. 先审核 semantic_relationships.json 中的关系")
print("2. 调整匹配阈值（当前>=8分）")
print("3. 确认无误后运行 import_relationships_to_neo4j.py")

print("\n" + "=" * 80)
print("✅ 分析完成")
print("=" * 80)

