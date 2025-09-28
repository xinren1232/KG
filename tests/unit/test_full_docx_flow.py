#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.parsers.ir_unified_parser import IRUnifiedParser
from api.parsers.ir_core import IRConverter
from pathlib import Path
import json

def test_full_docx_flow():
    """测试完整的DOCX解析流程"""
    
    # 找到一个真正的DOCX文件
    docx_file = Path("api/uploads/357d434f-3011-4732-aec6-6217392bfe3f")
    
    if not docx_file.exists():
        print(f"❌ DOCX文件不存在: {docx_file}")
        return
    
    print(f"📄 测试DOCX文件: {docx_file}")
    print(f"   文件大小: {docx_file.stat().st_size} bytes")
    
    try:
        # 步骤1: IR解析
        print("\n🔄 步骤1: IR解析...")
        parser = IRUnifiedParser()
        ir_result = parser.parse_document(docx_file, ".docx")
        
        if not ir_result['success']:
            print(f"❌ IR解析失败: {ir_result['error']}")
            return
        
        document_ir = ir_result['ir']
        print(f"✅ IR解析成功: {len(document_ir.blocks)} 个内容块")
        
        # 显示前几个块的信息
        print("   前5个内容块:")
        for i, block in enumerate(document_ir.blocks[:5]):
            print(f"     块{i+1}: {block.type.value} - {(block.text or '')[:50]}...")
        
        # 步骤2: 转换为前端格式
        print("\n🔄 步骤2: 转换为前端格式...")
        preview_data = IRConverter.to_legacy_format(document_ir)
        
        print(f"✅ 格式转换成功:")
        print(f"   raw_data: {len(preview_data.get('raw_data', []))} 条记录")
        print(f"   entities: {len(preview_data.get('entities', []))} 个实体")
        print(f"   relations: {len(preview_data.get('relations', []))} 个关系")
        print(f"   metadata: {len(preview_data.get('metadata', {}))} 个元数据字段")
        
        # 显示前几条记录
        print("\n   前3条记录:")
        for i, record in enumerate(preview_data.get('raw_data', [])[:3]):
            content_type = record.get('content_type', 'unknown')
            content = record.get('content', '')
            print(f"     记录{i+1}: {content_type} - {content[:80]}...")
        
        # 步骤3: 验证数据结构
        print("\n🔄 步骤3: 验证数据结构...")
        
        # 检查必需字段
        required_fields = ['raw_data', 'entities', 'relations', 'metadata']
        missing_fields = [field for field in required_fields if field not in preview_data]
        
        if missing_fields:
            print(f"❌ 缺少必需字段: {missing_fields}")
        else:
            print("✅ 数据结构完整")
        
        # 检查raw_data结构
        if preview_data.get('raw_data'):
            first_record = preview_data['raw_data'][0]
            print(f"   第一条记录字段: {list(first_record.keys())}")
        
        # 步骤4: 模拟保存和加载
        print("\n🔄 步骤4: 模拟保存和加载...")
        
        # 保存到JSON文件
        test_file = "test_preview_data.json"
        with open(test_file, 'w', encoding='utf-8') as f:
            json.dump(preview_data, f, ensure_ascii=False, indent=2)
        
        # 重新加载
        with open(test_file, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)
        
        print(f"✅ 数据保存和加载成功")
        print(f"   保存的记录数: {len(loaded_data.get('raw_data', []))}")
        
        # 清理测试文件
        os.remove(test_file)
        
        print("\n🎉 完整流程测试成功！")
        print("   DOCX文件可以正常解析并转换为前端期望的格式")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_full_docx_flow()
