#!/usr/bin/env python3
"""
创建测试Excel文件并分析结构
"""

import pandas as pd
import os
from pathlib import Path

def create_test_excel():
    """创建测试Excel文件"""
    print("=== 创建测试Excel文件 ===")
    
    # 创建测试数据
    test_data = {
        "问题编号": ["ISSUE-001", "ISSUE-002", "ISSUE-003", "ISSUE-004", "ISSUE-005"],
        "不良现象": ["屏幕显示异常", "按键失灵", "电池续航短", "充电接口松动", "摄像头模糊"],
        "发生日期": ["2024-01-15", "2024-01-16", "2024-01-17", "2024-01-18", "2024-01-19"],
        "严重度": ["高", "中", "低", "高", "中"],
        "工厂": ["深圳工厂", "东莞工厂", "深圳工厂", "苏州工厂", "东莞工厂"],
        "机型": ["iPhone 15", "iPhone 15 Pro", "iPhone 14", "iPhone 15", "iPhone 15 Pro"],
        "部件": ["显示屏", "按键模组", "电池", "充电接口", "摄像头模组"],
        "原因分析": ["显示驱动IC故障", "按键弹片老化", "电池容量衰减", "接口焊接不良", "镜头污染"],
        "改善对策": ["更换驱动IC", "更换按键模组", "更换电池", "重新焊接", "清洁镜头"],
        "供应商": ["供应商A", "供应商B", "供应商C", "供应商D", "供应商E"],
        "状态": ["已解决", "处理中", "已解决", "处理中", "已解决"]
    }
    
    # 创建DataFrame
    df = pd.DataFrame(test_data)
    
    # 确保目录存在
    test_dir = Path("test_files")
    test_dir.mkdir(exist_ok=True)
    
    # 保存Excel文件
    excel_path = test_dir / "水利问题调查表.xlsx"
    df.to_excel(excel_path, index=False, sheet_name="问题清单")
    
    print(f"✅ 测试Excel文件已创建: {excel_path}")
    print(f"📊 数据维度: {df.shape[0]} 行 x {df.shape[1]} 列")
    print(f"📋 列名: {list(df.columns)}")
    
    return excel_path

def analyze_excel_file(excel_path):
    """分析Excel文件结构"""
    print(f"\n=== 分析Excel文件: {excel_path} ===")
    
    try:
        # 读取Excel文件
        df = pd.read_excel(excel_path, sheet_name=0)
        
        print(f"📊 数据维度: {df.shape[0]} 行 x {df.shape[1]} 列")
        print(f"📋 列名: {list(df.columns)}")
        
        # 分析列内容
        print("\n=== 列内容分析 ===")
        for i, col in enumerate(df.columns):
            non_null_count = df[col].count()
            sample_values = df[col].dropna().head(2).tolist()
            print(f"{i+1:2d}. {col:15s} | 非空: {non_null_count:3d} | 示例: {sample_values}")
        
        # 生成映射建议
        print("\n=== 映射建议 ===")
        mapping_suggestions = {
            "anomaly_key": "问题编号",
            "title": "不良现象", 
            "date": "发生日期",
            "severity": "严重度",
            "factory": "工厂",
            "product": "机型",
            "component": "部件",
            "symptom": "不良现象",
            "root_cause": "原因分析",
            "countermeasure": "改善对策",
            "supplier": "供应商",
            "status": "状态"
        }
        
        for key, col in mapping_suggestions.items():
            if col in df.columns:
                print(f"✅ {key:15s} -> {col}")
            else:
                print(f"❌ {key:15s} -> {col} (列不存在)")
        
        # 生成优化的映射配置
        generate_optimized_config(df.columns, mapping_suggestions)
        
        # 显示解析预览
        print("\n=== 解析预览 ===")
        for i, row in df.head(2).iterrows():
            print(f"\n--- 记录 {i+1} ---")
            for key, col in mapping_suggestions.items():
                if col in df.columns:
                    value = row[col]
                    if pd.notna(value):
                        print(f"  {key:15s}: {str(value)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Excel分析失败: {e}")
        return False

def generate_optimized_config(columns, mapping_suggestions):
    """生成优化的映射配置"""
    yaml_content = f"""# 优化的Excel映射配置
# 基于实际文件结构生成

sheet: 0  # 第一个工作表

columns:
"""
    
    # 添加映射的列
    for key, col in mapping_suggestions.items():
        if col in columns:
            yaml_content += f'  {key}: "{col}"\n'
    
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
  Product:
    fields: ["product"]
    label: "产品"
  Factory:
    fields: ["factory"]
    label: "工厂"
  Supplier:
    fields: ["supplier"]
    label: "供应商"

# 关系映射规则
relation_mapping:
  - source: "symptom"
    target: "root_cause"
    type: "HAS_ROOTCAUSE"
    confidence: 1.0
  - source: "root_cause"
    target: "countermeasure"
    type: "RESOLVED_BY"
    confidence: 1.0
  - source: "symptom"
    target: "component"
    type: "AFFECTS"
    confidence: 0.9
  - source: "product"
    target: "component"
    type: "CONTAINS"
    confidence: 0.8
  - source: "factory"
    target: "product"
    type: "PRODUCES"
    confidence: 0.7
  - source: "supplier"
    target: "component"
    type: "SUPPLIES"
    confidence: 0.8
"""
    
    # 保存配置文件
    config_path = "api/mappings/mapping_excel_optimized.yaml"
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(yaml_content)
    
    print(f"\n✅ 优化配置已保存到: {config_path}")

if __name__ == "__main__":
    # 创建测试Excel文件
    excel_path = create_test_excel()
    
    # 分析文件结构
    success = analyze_excel_file(excel_path)
    
    if success:
        print("\n🎉 Excel文件创建和分析完成！")
        print("📝 下一步:")
        print("1. 使用创建的测试文件进行上传测试")
        print("2. 检查解析结果是否正确")
        print("3. 根据需要调整映射配置")
    else:
        print("\n❌ Excel分析失败！")
