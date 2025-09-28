#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
from collections import Counter, defaultdict
import re

def analyze_dictionary_data():
    """分析词典数据质量"""
    print("🔍 分析当前词典数据质量...")
    
    # 读取词典数据
    with open('api/data/dictionary.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"📊 总数据量: {len(data)} 条")
    
    # 数据质量分析
    quality_report = {
        "total_entries": len(data),
        "categories": {},
        "tags": {},
        "data_quality": {
            "complete_entries": 0,
            "missing_description": 0,
            "missing_aliases": 0,
            "missing_tags": 0,
            "duplicate_terms": 0,
            "empty_fields": 0
        },
        "sources": {},
        "modules": {},
        "issues": []
    }
    
    # 统计分类分布
    categories = Counter()
    tags = Counter()
    sources = Counter()
    terms = []
    
    for entry in data:
        # 分类统计
        category = entry.get('category', 'Unknown')
        categories[category] += 1
        
        # 标签统计
        entry_tags = entry.get('tags', [])
        if isinstance(entry_tags, list):
            for tag in entry_tags:
                if tag and tag.strip():
                    tags[tag.strip()] += 1
        
        # 来源统计
        source = entry.get('source', 'Unknown')
        sources[source] += 1
        
        # 术语收集
        term = entry.get('term', '').strip()
        if term:
            terms.append(term)
        
        # 数据完整性检查
        if all([
            entry.get('term'),
            entry.get('category'),
            entry.get('description'),
            entry.get('tags')
        ]):
            quality_report["data_quality"]["complete_entries"] += 1
        
        if not entry.get('description'):
            quality_report["data_quality"]["missing_description"] += 1
        
        if not entry.get('aliases') or len(entry.get('aliases', [])) == 0:
            quality_report["data_quality"]["missing_aliases"] += 1
        
        if not entry.get('tags') or len(entry.get('tags', [])) == 0:
            quality_report["data_quality"]["missing_tags"] += 1
    
    # 重复术语检查
    term_counts = Counter(terms)
    duplicates = {term: count for term, count in term_counts.items() if count > 1}
    quality_report["data_quality"]["duplicate_terms"] = len(duplicates)
    
    # 填充统计结果
    quality_report["categories"] = dict(categories.most_common())
    quality_report["tags"] = dict(tags.most_common(20))  # 前20个标签
    quality_report["sources"] = dict(sources)
    
    # 计算数据质量分数
    total = len(data)
    completeness_score = (quality_report["data_quality"]["complete_entries"] / total) * 100
    uniqueness_score = ((total - quality_report["data_quality"]["duplicate_terms"]) / total) * 100
    coverage_score = ((total - quality_report["data_quality"]["missing_description"]) / total) * 100
    
    overall_quality = (completeness_score + uniqueness_score + coverage_score) / 3
    quality_report["overall_quality_score"] = round(overall_quality, 1)
    
    # 生成问题列表
    issues = []
    if quality_report["data_quality"]["missing_description"] > 0:
        issues.append(f"{quality_report['data_quality']['missing_description']} 条记录缺少描述")
    
    if quality_report["data_quality"]["missing_aliases"] > total * 0.5:
        issues.append(f"{quality_report['data_quality']['missing_aliases']} 条记录缺少别名")
    
    if quality_report["data_quality"]["duplicate_terms"] > 0:
        issues.append(f"发现 {quality_report['data_quality']['duplicate_terms']} 个重复术语")
    
    quality_report["issues"] = issues
    
    return quality_report

def analyze_neo4j_consistency():
    """分析Neo4j数据一致性"""
    print("\n🔍 分析Neo4j数据一致性...")
    
    try:
        from neo4j import GraphDatabase
        driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'password123'))
        
        consistency_report = {
            "neo4j_status": "connected",
            "node_counts": {},
            "relationship_counts": {},
            "orphaned_nodes": 0,
            "consistency_issues": []
        }
        
        with driver.session() as session:
            # 节点统计
            node_result = session.run("""
                CALL db.labels() YIELD label
                CALL {
                    WITH label
                    MATCH (n)
                    WHERE label IN labels(n)
                    RETURN count(n) as count
                }
                RETURN label, count
                ORDER BY count DESC
            """)
            
            for record in node_result:
                consistency_report["node_counts"][record['label']] = record['count']
            
            # 关系统计
            rel_result = session.run("""
                MATCH ()-[r]->() 
                RETURN type(r) AS type, count(r) AS count 
                ORDER BY count DESC
            """)
            
            for record in rel_result:
                consistency_report["relationship_counts"][record['type']] = record['count']
            
            # 检查孤立节点
            orphaned = session.run("""
                MATCH (n:Dictionary)
                WHERE NOT (n)-[]-()
                RETURN count(n) AS count
            """).single()
            
            consistency_report["orphaned_nodes"] = orphaned['count'] if orphaned else 0
            
            # 检查数据一致性问题
            issues = []
            
            # 检查是否有Dictionary节点没有分类关系
            no_category = session.run("""
                MATCH (d:Dictionary)
                WHERE NOT (d)-[:IN_CATEGORY]->()
                RETURN count(d) AS count
            """).single()
            
            if no_category and no_category['count'] > 0:
                issues.append(f"{no_category['count']} 个Dictionary节点缺少分类关系")
            
            # 检查是否有空的标签节点
            empty_tags = session.run("""
                MATCH (t:Tag)
                WHERE NOT ()-[:HAS_TAG]->(t)
                RETURN count(t) AS count
            """).single()
            
            if empty_tags and empty_tags['count'] > 0:
                issues.append(f"{empty_tags['count']} 个Tag节点没有被引用")
            
            consistency_report["consistency_issues"] = issues
        
        driver.close()
        return consistency_report
        
    except Exception as e:
        print(f"❌ Neo4j连接失败: {e}")
        return {
            "neo4j_status": "disconnected",
            "error": str(e)
        }

def generate_governance_config():
    """生成数据治理配置"""
    print("\n📋 生成数据治理配置...")
    
    # 分析数据
    dict_report = analyze_dictionary_data()
    neo4j_report = analyze_neo4j_consistency()
    
    # 生成治理配置
    governance_config = {
        "timestamp": "2024-01-20 10:00:00",
        "data_overview": {
            "total_entries": dict_report["total_entries"],
            "categories": len(dict_report["categories"]),
            "tags": len(dict_report["tags"]),
            "quality_score": dict_report["overall_quality_score"]
        },
        "quality_metrics": [
            {
                "metric": "数据完整性",
                "value": f"{dict_report['data_quality']['complete_entries']}/{dict_report['total_entries']}",
                "percentage": round((dict_report['data_quality']['complete_entries'] / dict_report['total_entries']) * 100, 1),
                "status": "good" if dict_report['data_quality']['complete_entries'] / dict_report['total_entries'] > 0.8 else "warning"
            },
            {
                "metric": "术语唯一性",
                "value": f"{dict_report['total_entries'] - dict_report['data_quality']['duplicate_terms']}/{dict_report['total_entries']}",
                "percentage": round(((dict_report['total_entries'] - dict_report['data_quality']['duplicate_terms']) / dict_report['total_entries']) * 100, 1),
                "status": "good" if dict_report['data_quality']['duplicate_terms'] == 0 else "warning"
            },
            {
                "metric": "描述覆盖率",
                "value": f"{dict_report['total_entries'] - dict_report['data_quality']['missing_description']}/{dict_report['total_entries']}",
                "percentage": round(((dict_report['total_entries'] - dict_report['data_quality']['missing_description']) / dict_report['total_entries']) * 100, 1),
                "status": "good"
            },
            {
                "metric": "标签覆盖率",
                "value": f"{dict_report['total_entries'] - dict_report['data_quality']['missing_tags']}/{dict_report['total_entries']}",
                "percentage": round(((dict_report['total_entries'] - dict_report['data_quality']['missing_tags']) / dict_report['total_entries']) * 100, 1),
                "status": "good"
            }
        ],
        "category_distribution": dict_report["categories"],
        "top_tags": dict_report["tags"],
        "data_sources": dict_report["sources"],
        "issues": dict_report["issues"] + neo4j_report.get("consistency_issues", []),
        "neo4j_status": neo4j_report,
        "recommendations": [
            "定期检查数据完整性",
            "建立标准化的术语审核流程",
            "实施自动化的数据质量监控",
            "建立数据变更追踪机制"
        ]
    }
    
    # 保存配置
    with open('config/data_governance_config.json', 'w', encoding='utf-8') as f:
        json.dump(governance_config, f, ensure_ascii=False, indent=2)
    
    print("✅ 数据治理配置已生成: config/data_governance_config.json")
    
    # 显示摘要
    print(f"\n📊 数据治理摘要:")
    print(f"   总数据量: {dict_report['total_entries']} 条")
    print(f"   数据质量分: {dict_report['overall_quality_score']}%")
    print(f"   分类数量: {len(dict_report['categories'])} 个")
    print(f"   标签数量: {len(dict_report['tags'])} 个")
    print(f"   发现问题: {len(governance_config['issues'])} 个")
    
    return governance_config

if __name__ == "__main__":
    generate_governance_config()
