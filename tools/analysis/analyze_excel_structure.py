#!/usr/bin/env python3
"""
分析Excel文件结构，创建完整的解析规则
"""

import os
import pandas as pd
import json
from pathlib import Path

def analyze_excel_files():
    """分析上传的Excel文件结构"""
    print("=== Excel文件结构分析 ===")

    # 1. 检查上传目录中的文件
    upload_files = []
    try:
        all_items = os.listdir('api/uploads')
        for item in all_items:
            item_path = f'api/uploads/{item}'
            if os.path.isfile(item_path) and item.endswith('.xlsx'):
                upload_files.append(item)
            elif os.path.isdir(item_path):
                # 检查子目录中的Excel文件
                try:
                    sub_files = os.listdir(item_path)
                    for sub_file in sub_files:
                        if sub_file.endswith('.xlsx'):
                            upload_files.append(f'{item}/{sub_file}')
                except:
                    pass
    except Exception as e:
        print(f"❌ 检查上传目录失败: {e}")
        return None, None

    if not upload_files:
        print("❌ 没有找到Excel文件")
        # 尝试使用测试文件
        test_file = 'test_files/水利问题调查表.xlsx'
        if os.path.exists(test_file):
            print(f"📄 使用测试文件: {test_file}")
            upload_files = [test_file]
        else:
            return None, None

    print(f"📁 找到 {len(upload_files)} 个Excel文件")

    # 检查最新的文件
    for upload_file in upload_files[-3:]:
        print(f"\n📂 检查文件: {upload_file}")

        if upload_file.startswith('test_files/'):
            file_path = upload_file
        else:
            file_path = f'api/uploads/{upload_file}'

        print(f"📄 Excel文件路径: {file_path}")

        try:
            # 读取Excel文件
            df = pd.read_excel(file_path)

            print(f"📊 数据形状: {df.shape}")
            print(f"📋 列名 ({len(df.columns)} 列):")
            for i, col in enumerate(df.columns, 1):
                print(f"  {i:2d}. {col}")

            print(f"\n📝 前3行数据:")
            for i, row in df.head(3).iterrows():
                print(f"  行 {i+1}:")
                for col in df.columns[:10]:  # 只显示前10列
                    value = str(row[col])[:50]  # 限制显示长度
                    print(f"    {col}: {value}")
                print()

            return df, file_path

        except Exception as e:
            print(f"❌ 读取Excel文件失败: {e}")
            continue

    return None, None

def create_comprehensive_mapping(df):
    """基于实际Excel结构创建全面的映射配置"""
    if df is None:
        return None
    
    print("\n=== 创建全面映射配置 ===")
    
    columns = list(df.columns)
    print(f"📋 总共 {len(columns)} 列需要映射")
    
    # 创建全面的列映射
    comprehensive_mapping = {
        'sheet': 0,
        'columns': {},
        'options': {
            'skip_empty_rows': True,
            'trim_whitespace': True,
            'auto_detect_encoding': True,
            'include_all_columns': True  # 新增：包含所有列
        }
    }
    
    # 智能映射所有列
    for i, col in enumerate(columns):
        # 使用列名作为键，确保所有列都被包含
        safe_key = f"col_{i+1:02d}_{col.replace(' ', '_').replace('/', '_').replace('(', '').replace(')', '')}"
        comprehensive_mapping['columns'][safe_key] = col
    
    # 添加一些常见的业务字段映射
    business_mappings = {
        'anomaly_key': None,
        'title': None,
        'date': None,
        'factory': None,
        'product': None,
        'component': None,
        'symptom': None,
        'root_cause': None,
        'countermeasure': None,
        'supplier': None,
        'status': None,
        'severity': None
    }
    
    # 智能匹配业务字段
    for business_field, _ in business_mappings.items():
        for col in columns:
            col_lower = col.lower()
            if business_field == 'anomaly_key' and any(x in col for x in ['编号', '问题', 'ID', 'id']):
                business_mappings[business_field] = col
            elif business_field == 'title' and any(x in col for x in ['标题', '现象', '问题', '描述']):
                business_mappings[business_field] = col
            elif business_field == 'date' and any(x in col for x in ['日期', '时间', 'date', 'time']):
                business_mappings[business_field] = col
            elif business_field == 'factory' and any(x in col for x in ['工厂', '厂', 'factory']):
                business_mappings[business_field] = col
            elif business_field == 'product' and any(x in col for x in ['产品', '机型', 'product']):
                business_mappings[business_field] = col
            elif business_field == 'component' and any(x in col for x in ['部件', '组件', 'component']):
                business_mappings[business_field] = col
            elif business_field == 'root_cause' and any(x in col for x in ['原因', '根因', 'cause']):
                business_mappings[business_field] = col
            elif business_field == 'countermeasure' and any(x in col for x in ['对策', '措施', '改善']):
                business_mappings[business_field] = col
            elif business_field == 'supplier' and any(x in col for x in ['供应商', 'supplier']):
                business_mappings[business_field] = col
    
    # 添加业务字段映射
    for field, col in business_mappings.items():
        if col:
            comprehensive_mapping['columns'][field] = col
    
    print(f"✅ 映射了 {len(comprehensive_mapping['columns'])} 个字段")
    
    return comprehensive_mapping

def save_comprehensive_mapping(mapping):
    """保存全面的映射配置"""
    if not mapping:
        return False
    
    import yaml
    
    # 保存为YAML文件
    mapping_file = 'api/mappings/mapping_excel_comprehensive.yaml'
    
    try:
        with open(mapping_file, 'w', encoding='utf-8') as f:
            yaml.dump(mapping, f, default_flow_style=False, allow_unicode=True, indent=2)
        
        print(f"✅ 全面映射配置已保存到: {mapping_file}")
        return True
        
    except Exception as e:
        print(f"❌ 保存映射配置失败: {e}")
        return False

def update_parser_to_use_comprehensive_mapping():
    """更新解析器使用全面映射"""
    print("\n=== 更新解析器配置 ===")
    
    # 更新enhanced_excel_parser.py
    parser_file = 'api/parsers/enhanced_excel_parser.py'
    
    try:
        with open(parser_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 替换默认映射文件
        updated_content = content.replace(
            'mapping_excel_optimized.yaml',
            'mapping_excel_comprehensive.yaml'
        )
        
        with open(parser_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print("✅ 解析器已更新为使用全面映射配置")
        return True
        
    except Exception as e:
        print(f"❌ 更新解析器失败: {e}")
        return False

def test_comprehensive_parsing():
    """测试全面解析效果"""
    print("\n=== 测试全面解析 ===")
    
    try:
        from api.parsers.enhanced_excel_parser import parse_excel_robust
        
        # 找到测试文件
        upload_dirs = [d for d in os.listdir('api/uploads') if os.path.isdir(f'api/uploads/{d}')]
        if not upload_dirs:
            print("❌ 没有测试文件")
            return False
        
        latest_dir = upload_dirs[-1]
        dir_path = f'api/uploads/{latest_dir}'
        files = os.listdir(dir_path)
        excel_files = [f for f in files if f.endswith('.xlsx')]
        
        if not excel_files:
            print("❌ 没有Excel文件")
            return False
        
        test_file = f'{dir_path}/{excel_files[0]}'
        print(f"📄 测试文件: {test_file}")
        
        # 执行解析
        result = parse_excel_robust(test_file)
        
        if result['success']:
            data = result['data']
            print(f"✅ 解析成功!")
            print(f"📊 原始记录: {len(data.get('raw_data', []))} 条")
            print(f"🔍 抽取实体: {len(data.get('entities', []))} 个")
            print(f"🔗 抽取关系: {len(data.get('relations', []))} 个")
            
            # 显示第一条记录的所有字段
            raw_data = data.get('raw_data', [])
            if raw_data:
                first_record = raw_data[0]
                print(f"\n📋 第一条记录的所有字段 ({len(first_record)} 个):")
                for key, value in first_record.items():
                    print(f"  {key}: {str(value)[:100]}")
            
            return True
        else:
            print(f"❌ 解析失败: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ 测试解析异常: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Excel文件结构分析和全面解析配置")
    print("="*60)
    
    # 1. 分析Excel文件结构
    df, file_path = analyze_excel_files()
    
    if df is not None:
        # 2. 创建全面映射配置
        mapping = create_comprehensive_mapping(df)
        
        if mapping:
            # 3. 保存映射配置
            if save_comprehensive_mapping(mapping):
                # 4. 更新解析器
                if update_parser_to_use_comprehensive_mapping():
                    # 5. 测试解析效果
                    test_comprehensive_parsing()
    
    print("\n" + "="*60)
    print("🎊 Excel结构分析完成！")
