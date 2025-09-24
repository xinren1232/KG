#!/usr/bin/env python3
"""
测试文件抽取功能
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'services', 'etl'))

from file_extractor import FileExtractor

def test_extraction():
    """测试文件抽取功能"""
    extractor = FileExtractor()
    
    # 测试CSV文件
    test_file = "data/raw/test_sample.csv"
    
    if not os.path.exists(test_file):
        print(f"测试文件不存在: {test_file}")
        return
    
    print(f"开始测试文件抽取: {test_file}")
    
    try:
        result = extractor.extract_file(test_file)
        
        print(f"\n抽取结果:")
        print(f"文件路径: {result.file_path}")
        print(f"文件类型: {result.file_type}")
        print(f"实体数量: {len(result.entities)}")
        print(f"关系数量: {len(result.relations)}")
        print(f"错误信息: {result.errors}")
        
        print(f"\n元数据:")
        for key, value in result.metadata.items():
            print(f"  {key}: {value}")
        
        print(f"\n前5个实体:")
        for i, entity in enumerate(result.entities[:5]):
            print(f"  {i+1}. {entity.name} ({entity.type}) - {entity.source_location}")
        
        print(f"\n前5个关系:")
        for i, relation in enumerate(result.relations[:5]):
            print(f"  {i+1}. {relation.source_entity} -> {relation.target_entity} ({relation.relation_type})")
        
        return result
        
    except Exception as e:
        print(f"抽取失败: {e}")
        return None

if __name__ == "__main__":
    test_extraction()
