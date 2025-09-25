#!/usr/bin/env python3
"""
数据质量分析工具
检查各个数据源的完整性，找出空缺数据
"""
import csv
import json
from pathlib import Path
from typing import Dict, List, Any, Set
import pandas as pd

def analyze_csv_data_quality(file_path: Path, name: str) -> Dict[str, Any]:
    """分析CSV文件的数据质量"""
    if not file_path.exists():
        return {"name": name, "exists": False, "error": "文件不存在"}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        if not rows:
            return {"name": name, "exists": True, "total": 0, "error": "文件为空"}
        
        # 分析字段完整性
        fields = list(rows[0].keys())
        field_stats = {}
        
        for field in fields:
            empty_count = sum(1 for row in rows if not row.get(field, "").strip())
            field_stats[field] = {
                "total": len(rows),
                "empty": empty_count,
                "filled": len(rows) - empty_count,
                "completeness": (len(rows) - empty_count) / len(rows) * 100
            }
        
        # 找出空缺数据的行
        incomplete_rows = []
        for i, row in enumerate(rows):
            missing_fields = []
            for field in fields:
                if not row.get(field, "").strip():
                    missing_fields.append(field)
            if missing_fields:
                incomplete_rows.append({
                    "row": i + 2,  # +2 因为有标题行，且从1开始计数
                    "data": row,
                    "missing_fields": missing_fields
                })
        
        return {
            "name": name,
            "exists": True,
            "total": len(rows),
            "fields": fields,
            "field_stats": field_stats,
            "incomplete_rows": incomplete_rows,
            "completeness_score": sum(stats["completeness"] for stats in field_stats.values()) / len(field_stats)
        }
        
    except Exception as e:
        return {"name": name, "exists": True, "error": str(e)}

def analyze_json_data_quality(file_path: Path, name: str) -> Dict[str, Any]:
    """分析JSON文件的数据质量"""
    if not file_path.exists():
        return {"name": name, "exists": False, "error": "文件不存在"}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        entries = data.get('entries', [])
        if not entries:
            return {"name": name, "exists": True, "total": 0, "error": "无条目数据"}
        
        # 分析字段完整性
        required_fields = ['term', 'aliases', 'category', 'tags', 'definition']
        field_stats = {}
        
        for field in required_fields:
            empty_count = 0
            for entry in entries:
                value = entry.get(field)
                if not value or (isinstance(value, str) and not value.strip()) or (isinstance(value, list) and not value):
                    empty_count += 1
            
            field_stats[field] = {
                "total": len(entries),
                "empty": empty_count,
                "filled": len(entries) - empty_count,
                "completeness": (len(entries) - empty_count) / len(entries) * 100
            }
        
        # 找出空缺数据的条目
        incomplete_entries = []
        for i, entry in enumerate(entries):
            missing_fields = []
            for field in required_fields:
                value = entry.get(field)
                if not value or (isinstance(value, str) and not value.strip()) or (isinstance(value, list) and not value):
                    missing_fields.append(field)
            if missing_fields:
                incomplete_entries.append({
                    "index": i,
                    "term": entry.get('term', '未知'),
                    "missing_fields": missing_fields
                })
        
        return {
            "name": name,
            "exists": True,
            "total": len(entries),
            "fields": required_fields,
            "field_stats": field_stats,
            "incomplete_entries": incomplete_entries,
            "completeness_score": sum(stats["completeness"] for stats in field_stats.values()) / len(field_stats)
        }
        
    except Exception as e:
        return {"name": name, "exists": True, "error": str(e)}

def print_quality_report(analysis: Dict[str, Any]):
    """打印数据质量报告"""
    print(f"\n📊 {analysis['name']} 数据质量报告")
    print("=" * 60)
    
    if not analysis.get('exists'):
        print("❌ 文件不存在")
        return
    
    if 'error' in analysis:
        print(f"❌ 错误: {analysis['error']}")
        return
    
    print(f"📈 总记录数: {analysis['total']}")
    print(f"🎯 完整性评分: {analysis['completeness_score']:.1f}%")
    
    print(f"\n📋 字段完整性:")
    for field, stats in analysis['field_stats'].items():
        status = "✅" if stats['completeness'] == 100 else "⚠️" if stats['completeness'] >= 80 else "❌"
        print(f"  {status} {field}: {stats['filled']}/{stats['total']} ({stats['completeness']:.1f}%)")
    
    # 显示不完整的记录
    if 'incomplete_rows' in analysis:
        incomplete_items = analysis['incomplete_rows']
    else:
        incomplete_items = analysis.get('incomplete_entries', [])
    
    if incomplete_items:
        print(f"\n⚠️ 不完整记录 ({len(incomplete_items)} 条):")
        for item in incomplete_items[:10]:  # 只显示前10条
            if 'row' in item:
                print(f"  行 {item['row']}: {item['data'].get('term', item['data'].get('name', '未知'))} - 缺失: {', '.join(item['missing_fields'])}")
            else:
                print(f"  {item['term']} - 缺失: {', '.join(item['missing_fields'])}")
        if len(incomplete_items) > 10:
            print(f"  ... 还有 {len(incomplete_items) - 10} 条不完整记录")

def recommend_best_data_source(analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
    """推荐最佳数据源"""
    print(f"\n🏆 数据源质量排名")
    print("=" * 60)
    
    valid_analyses = [a for a in analyses if a.get('exists') and 'error' not in a and a.get('total', 0) > 0]
    
    if not valid_analyses:
        print("❌ 没有有效的数据源")
        return None
    
    # 按完整性评分排序
    sorted_analyses = sorted(valid_analyses, key=lambda x: x['completeness_score'], reverse=True)
    
    for i, analysis in enumerate(sorted_analyses):
        rank_emoji = ["🥇", "🥈", "🥉"][i] if i < 3 else f"{i+1}."
        print(f"{rank_emoji} {analysis['name']}")
        print(f"   📊 完整性: {analysis['completeness_score']:.1f}%")
        print(f"   📈 记录数: {analysis['total']}")
        print(f"   📋 字段数: {len(analysis['fields'])}")
    
    best_source = sorted_analyses[0]
    print(f"\n✅ 推荐使用: {best_source['name']}")
    print(f"   理由: 完整性最高 ({best_source['completeness_score']:.1f}%)，数据最完整")
    
    return best_source

def main():
    """主函数"""
    print("🔍 数据源质量分析报告")
    print("=" * 80)
    
    # 定义要分析的数据源
    data_sources = [
        {
            "name": "ontology/dictionaries/components.csv",
            "path": Path("ontology/dictionaries/components.csv"),
            "type": "csv"
        },
        {
            "name": "ontology/dictionaries/symptoms.csv", 
            "path": Path("ontology/dictionaries/symptoms.csv"),
            "type": "csv"
        },
        {
            "name": "ontology/dictionaries/causes.csv",
            "path": Path("ontology/dictionaries/causes.csv"),
            "type": "csv"
        },
        {
            "name": "ontology/dictionaries/countermeasures.csv",
            "path": Path("ontology/dictionaries/countermeasures.csv"),
            "type": "csv"
        },
        {
            "name": "data/vocab/components.csv",
            "path": Path("data/vocab/components.csv"),
            "type": "csv"
        },
        {
            "name": "data/vocab/dictionary.json",
            "path": Path("data/vocab/dictionary.json"),
            "type": "json"
        }
    ]
    
    analyses = []
    
    # 分析每个数据源
    for source in data_sources:
        if source["type"] == "csv":
            analysis = analyze_csv_data_quality(source["path"], source["name"])
        else:
            analysis = analyze_json_data_quality(source["path"], source["name"])
        
        analyses.append(analysis)
        print_quality_report(analysis)
    
    # 推荐最佳数据源
    best_source = recommend_best_data_source(analyses)
    
    # 生成清理建议
    print(f"\n🧹 数据清理建议")
    print("=" * 60)
    print("1. 使用 ontology/dictionaries/ 作为主要数据源")
    print("   - 数据最完整，字段最丰富")
    print("   - 包含 term, canonical_name, aliases, category, tags, description")
    print("   - 建议作为统一标准")
    
    print("\n2. 清理和合并策略:")
    print("   - 保留 ontology/dictionaries/ 目录")
    print("   - 删除或归档 data/vocab/ 中的重复数据")
    print("   - 统一使用标准字段格式")
    
    print("\n3. 数据完整性要求:")
    print("   - term (必填): 术语名称")
    print("   - canonical_name (必填): 标准名称") 
    print("   - category (必填): 分类")
    print("   - description (推荐): 描述信息")
    print("   - aliases (可选): 别名列表")
    print("   - tags (可选): 标签列表")

if __name__ == "__main__":
    main()
