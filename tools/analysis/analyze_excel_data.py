#!/usr/bin/env python3
"""
Excel数据结构分析工具
分析用户提供的Excel文件，识别字段类型、数据质量、实体关系
为自动抽取和知识图谱构建做准备
"""
import pandas as pd
import numpy as np
from pathlib import Path
import re
from collections import Counter
import json

def analyze_excel_structure(file_path):
    """分析Excel文件结构"""
    print(f"🔍 分析文件: {file_path}")
    
    try:
        # 读取Excel文件
        df = pd.read_excel(file_path)
        
        print(f"📊 基本信息:")
        print(f"  - 行数: {len(df)}")
        print(f"  - 列数: {len(df.columns)}")
        print(f"  - 文件大小: {Path(file_path).stat().st_size / 1024:.1f} KB")
        
        print(f"\n📋 列名信息:")
        for i, col in enumerate(df.columns):
            print(f"  {i+1:2d}. {col}")
            
        print(f"\n🔍 数据类型分析:")
        for col in df.columns:
            dtype = df[col].dtype
            null_count = df[col].isnull().sum()
            unique_count = df[col].nunique()
            
            print(f"  {col}:")
            print(f"    - 类型: {dtype}")
            print(f"    - 空值: {null_count}/{len(df)} ({null_count/len(df)*100:.1f}%)")
            print(f"    - 唯一值: {unique_count}")
            
            # 显示样例数据
            sample_values = df[col].dropna().head(3).tolist()
            print(f"    - 样例: {sample_values}")
            print()
            
        return df
        
    except Exception as e:
        print(f"❌ 读取文件失败: {e}")
        return None

def identify_entity_types(df):
    """识别可能的实体类型"""
    print("🎯 实体类型识别:")
    
    entity_patterns = {
        'AnomalyID': [r'异常.*编号', r'问题.*编号', r'缺陷.*编号', r'ID', r'编号'],
        'Product': [r'产品', r'机型', r'型号', r'设备'],
        'Component': [r'组件', r'模块', r'部件', r'器件'],
        'Symptom': [r'症状', r'现象', r'问题.*描述', r'故障.*现象'],
        'Severity': [r'严重.*程度', r'级别', r'优先级'],
        'Status': [r'状态', r'进度'],
        'Date': [r'日期', r'时间', r'创建.*时间'],
        'Owner': [r'负责人', r'处理人', r'分配.*给'],
        'Description': [r'描述', r'说明', r'详情', r'备注']
    }
    
    identified_entities = {}
    
    for col in df.columns:
        col_lower = col.lower()
        for entity_type, patterns in entity_patterns.items():
            for pattern in patterns:
                if re.search(pattern, col, re.IGNORECASE):
                    identified_entities[col] = entity_type
                    print(f"  ✅ {col} -> {entity_type}")
                    break
            if col in identified_entities:
                break
    
    # 未识别的列
    unidentified = [col for col in df.columns if col not in identified_entities]
    if unidentified:
        print(f"  ❓ 未识别列: {unidentified}")
    
    return identified_entities

def analyze_data_quality(df):
    """分析数据质量"""
    print("📈 数据质量分析:")
    
    # 整体完整性
    total_cells = len(df) * len(df.columns)
    null_cells = df.isnull().sum().sum()
    completeness = (total_cells - null_cells) / total_cells * 100
    
    print(f"  - 数据完整性: {completeness:.1f}%")
    
    # 重复行检查
    duplicate_rows = df.duplicated().sum()
    print(f"  - 重复行: {duplicate_rows}")
    
    # 字段值分布
    print(f"  - 字段值分布:")
    for col in df.columns:
        if df[col].dtype == 'object':
            value_counts = df[col].value_counts()
            if len(value_counts) <= 10:
                print(f"    {col}: {dict(value_counts.head())}")
            else:
                print(f"    {col}: {len(value_counts)} 个唯一值")

def suggest_knowledge_graph_schema(df, identified_entities):
    """建议知识图谱Schema"""
    print("🕸️ 知识图谱Schema建议:")
    
    # 节点类型建议
    node_types = set(identified_entities.values())
    print(f"  📍 建议节点类型: {list(node_types)}")
    
    # 关系建议
    relationships = []
    if 'AnomalyID' in identified_entities.values() and 'Component' in identified_entities.values():
        relationships.append("Anomaly -[:AFFECTS]-> Component")
    if 'AnomalyID' in identified_entities.values() and 'Symptom' in identified_entities.values():
        relationships.append("Anomaly -[:HAS_SYMPTOM]-> Symptom")
    if 'Product' in identified_entities.values() and 'Component' in identified_entities.values():
        relationships.append("Product -[:INCLUDES]-> Component")
    
    print(f"  🔗 建议关系类型:")
    for rel in relationships:
        print(f"    - {rel}")

def generate_extraction_config(df, identified_entities):
    """生成抽取配置"""
    config = {
        'file_info': {
            'columns': df.columns.tolist(),
            'shape': df.shape,
            'dtypes': df.dtypes.astype(str).to_dict()
        },
        'entity_mapping': identified_entities,
        'extraction_rules': {}
    }
    
    # 为每个实体类型生成抽取规则
    for col, entity_type in identified_entities.items():
        config['extraction_rules'][col] = {
            'entity_type': entity_type,
            'required': df[col].isnull().sum() < len(df) * 0.5,  # 少于50%空值认为是必需字段
            'unique': df[col].nunique() > len(df) * 0.8,  # 超过80%唯一值认为是标识符
            'sample_values': df[col].dropna().head(5).tolist()
        }
    
    return config

def main():
    """主函数"""
    print("🚀 Excel数据结构分析工具")
    print("=" * 50)
    
    # 查找Excel文件
    data_dir = Path('data')
    excel_files = []
    
    for pattern in ['*.xlsx', '*.xls']:
        excel_files.extend(data_dir.rglob(pattern))
    
    if not excel_files:
        print("❌ 未找到Excel文件")
        return
    
    print(f"📁 找到 {len(excel_files)} 个Excel文件:")
    for i, file in enumerate(excel_files):
        print(f"  {i+1}. {file}")
    
    # 分析每个文件
    for file_path in excel_files:
        print(f"\n{'='*60}")
        df = analyze_excel_structure(file_path)
        
        if df is not None:
            identified_entities = identify_entity_types(df)
            analyze_data_quality(df)
            suggest_knowledge_graph_schema(df, identified_entities)
            
            # 生成配置文件
            config = generate_extraction_config(df, identified_entities)
            config_file = f"extraction_config_{file_path.stem}.json"
            
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            
            print(f"💾 配置文件已保存: {config_file}")

if __name__ == "__main__":
    main()
