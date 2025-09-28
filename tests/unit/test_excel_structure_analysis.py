#!/usr/bin/env python3
"""
分析Excel文件结构，优化解析配置
"""

import pandas as pd
import requests
import os
import json
from pathlib import Path

def analyze_excel_structure():
    """分析Excel文件结构"""
    print("=== Excel文件结构分析 ===")
    
    # 检查是否有测试文件
    test_files = [
        "test_files/水利问题调查表.xlsx",
        "api/uploads",  # 检查上传目录
        "data/uploads"  # 检查数据目录
    ]
    
    excel_file = None
    for file_path in test_files:
        if os.path.exists(file_path):
            if os.path.isfile(file_path) and file_path.endswith('.xlsx'):
                excel_file = file_path
                break
            elif os.path.isdir(file_path):
                # 查找目录中的Excel文件
                for f in os.listdir(file_path):
                    if f.endswith(('.xlsx', '.xls')):
                        excel_file = os.path.join(file_path, f)
                        break
                if excel_file:
                    break
    
    if not excel_file:
        print("❌ 未找到Excel测试文件")
        return False
    
    print(f"📁 分析文件: {excel_file}")
    
    try:
        # 读取Excel文件
        df = pd.read_excel(excel_file, sheet_name=0)
        print(f"✅ Excel文件读取成功")
        print(f"📊 数据维度: {df.shape[0]} 行 x {df.shape[1]} 列")
        print(f"📋 列名: {list(df.columns)}")
        
        # 分析列内容
        print("\n=== 列内容分析 ===")
        for i, col in enumerate(df.columns):
            non_null_count = df[col].count()
            sample_values = df[col].dropna().head(3).tolist()
            print(f"{i+1:2d}. {col:20s} | 非空: {non_null_count:3d} | 示例: {sample_values}")
        
        # 生成智能映射建议
        print("\n=== 智能映射建议 ===")
        mapping_suggestions = generate_smart_mapping(df.columns)
        for key, suggested_col in mapping_suggestions.items():
            print(f"{key:15s} -> {suggested_col}")
        
        # 生成优化的映射配置
        optimized_mapping = generate_optimized_mapping(df.columns, mapping_suggestions)
        
        # 保存优化配置
        config_path = "api/mappings/mapping_excel_optimized.yaml"
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(optimized_mapping)
        
        print(f"\n✅ 优化配置已保存到: {config_path}")
        
        # 测试解析效果
        print("\n=== 测试解析效果 ===")
        test_parsing_result(excel_file, mapping_suggestions)
        
        return True
        
    except Exception as e:
        print(f"❌ Excel分析失败: {e}")
        return False

def generate_smart_mapping(columns):
    """生成智能映射建议"""
    columns = [str(col).strip() for col in columns]
    suggestions = {}
    
    # 扩展的映射规则
    mapping_rules = {
        "anomaly_key": ["问题编号", "编号", "ID", "id", "序号", "No", "NO", "问题ID"],
        "title": ["标题", "问题", "不良现象", "现象", "描述", "问题描述", "异常现象"],
        "date": ["日期", "时间", "发生日期", "创建日期", "时间戳", "Date"],
        "severity": ["严重度", "等级", "级别", "优先级", "严重性", "重要性"],
        "factory": ["工厂", "厂区", "生产线", "工厂名称", "厂家"],
        "product": ["产品", "机型", "型号", "产品型号", "产品名称", "设备"],
        "component": ["部件", "组件", "零件", "器件", "组件名称", "部件名称"],
        "symptom": ["症状", "现象", "不良现象", "问题现象", "故障现象", "异常"],
        "root_cause": ["原因", "根因", "原因分析", "根本原因", "故障原因", "问题原因"],
        "countermeasure": ["对策", "措施", "改善对策", "解决方案", "处理措施", "改进措施"],
        "supplier": ["供应商", "厂商", "供货商", "提供商"],
        "status": ["状态", "处理状态", "当前状态", "进度"],
        "location": ["位置", "地点", "区域", "位置信息"],
        "operator": ["操作员", "操作者", "负责人", "处理人"],
        "remark": ["备注", "说明", "注释", "其他", "补充说明"]
    }
    
    # 使用更智能的匹配算法
    for key, candidates in mapping_rules.items():
        best_match = None
        best_score = 0
        
        for col in columns:
            col_lower = col.lower()
            for candidate in candidates:
                candidate_lower = candidate.lower()
                
                # 完全匹配
                if candidate_lower == col_lower:
                    suggestions[key] = col
                    best_match = col
                    break
                
                # 包含匹配
                elif candidate_lower in col_lower or col_lower in candidate_lower:
                    score = len(candidate_lower) / max(len(col_lower), len(candidate_lower))
                    if score > best_score:
                        best_score = score
                        best_match = col
            
            if key in suggestions:
                break
        
        if best_match and key not in suggestions and best_score > 0.5:
            suggestions[key] = best_match
    
    return suggestions

def generate_optimized_mapping(columns, suggestions):
    """生成优化的YAML配置"""
    yaml_content = f"""# 优化的Excel映射配置
# 基于实际文件结构自动生成: {len(columns)} 列

sheet: 0  # 第一个工作表

# 实际列名: {list(columns)}

columns:
"""
    
    # 添加映射的列
    for key, col in suggestions.items():
        yaml_content += f'  {key}: "{col}"\n'
    
    # 添加未映射的列作为注释
    unmapped_cols = [col for col in columns if col not in suggestions.values()]
    if unmapped_cols:
        yaml_content += f"\n# 未映射的列 (可根据需要添加):\n"
        for col in unmapped_cols:
            yaml_content += f'  # unknown_field: "{col}"\n'
    
    yaml_content += """
# 数据处理选项
options:
  skip_empty_rows: true
  trim_whitespace: true
  auto_detect_encoding: true

# 实体类型映射
entity_mapping:
  Component:
    fields: ["component"]
    label: "部件"
  Symptom:
    fields: ["symptom", "title"]
    label: "症状"
  RootCause:
    fields: ["root_cause"]
    label: "根因"
  Countermeasure:
    fields: ["countermeasure"]
    label: "对策"
"""
    
    return yaml_content

def test_parsing_result(excel_file, mapping_suggestions):
    """测试解析结果"""
    try:
        df = pd.read_excel(excel_file, sheet_name=0)
        
        print("📋 解析结果预览:")
        for i, row in df.head(3).iterrows():
            print(f"\n--- 记录 {i+1} ---")
            for key, col in mapping_suggestions.items():
                if col in df.columns:
                    value = row[col]
                    if pd.notna(value):
                        print(f"{key:15s}: {str(value)[:50]}")
                    else:
                        print(f"{key:15s}: [空值]")
        
        # 统计有效数据
        print(f"\n📊 数据质量统计:")
        for key, col in mapping_suggestions.items():
            if col in df.columns:
                non_null_count = df[col].count()
                total_count = len(df)
                percentage = (non_null_count / total_count) * 100
                print(f"{key:15s}: {non_null_count:3d}/{total_count:3d} ({percentage:5.1f}%)")
        
    except Exception as e:
        print(f"❌ 解析测试失败: {e}")

if __name__ == "__main__":
    success = analyze_excel_structure()
    if success:
        print("\n🎉 Excel结构分析完成！")
        print("📝 建议:")
        print("1. 检查生成的优化配置文件")
        print("2. 根据实际需求调整映射规则")
        print("3. 重新测试文档解析功能")
    else:
        print("\n❌ Excel结构分析失败！")
        print("请确保有可用的Excel测试文件。")
