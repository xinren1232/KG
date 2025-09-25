#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.files.manager import set_status, FileStatus, save_preview
from api.parsers.ir_unified_parser import IRUnifiedParser
from api.parsers.ir_core import IRConverter
from pathlib import Path
import json

def force_reparse():
    """强制重新解析"""
    
    upload_id = "357d434f-3011-4732-aec6-6217392bfe3f"
    
    print(f"🔄 强制重新解析: {upload_id}")
    
    try:
        # 1. 重置状态为解析中
        print("\n📋 步骤1: 重置状态...")
        set_status(upload_id, FileStatus.parsing)
        print("✅ 状态已重置为parsing")
        
        # 2. 重新解析
        print("\n🔄 步骤2: 重新解析...")
        docx_file = Path("api/uploads") / upload_id
        
        if not docx_file.exists():
            print(f"❌ 文件不存在: {docx_file}")
            return
        
        # 使用IR解析器
        parser = IRUnifiedParser()
        ir_result = parser.parse_document(docx_file, ".docx")
        
        if not ir_result['success']:
            print(f"❌ IR解析失败: {ir_result['error']}")
            set_status(upload_id, FileStatus.failed, error=ir_result['error'])
            return
        
        document_ir = ir_result['ir']
        print(f"✅ IR解析成功: {len(document_ir.blocks)} 个内容块")
        
        # 3. 转换为前端格式
        print("\n🔄 步骤3: 转换为前端格式...")
        preview_data = IRConverter.to_legacy_format(document_ir)
        
        print(f"✅ 格式转换成功:")
        print(f"   raw_data: {len(preview_data.get('raw_data', []))} 条记录")
        
        # 检查第一条记录
        if preview_data.get('raw_data'):
            first_record = preview_data['raw_data'][0]
            print(f"   第一条记录content_type: {first_record.get('content_type')}")
            print(f"   第一条记录字段: {list(first_record.keys())}")
        
        # 4. 保存新的预览数据
        print("\n💾 步骤4: 保存新的预览数据...")
        save_preview(upload_id, preview_data)
        
        # 5. 更新状态为解析完成
        set_status(upload_id, FileStatus.parsed,
                  entity_count=len(preview_data.get("entities", [])),
                  relation_count=len(preview_data.get("relations", [])))
        
        print("✅ 状态已更新为parsed")
        
        # 6. 验证结果
        print("\n📄 步骤5: 验证最终结果...")
        from api.files.manager import load_preview
        final_data = load_preview(upload_id)
        
        if final_data.get('raw_data'):
            first_record = final_data['raw_data'][0]
            print(f"✅ 最终验证:")
            print(f"   记录数: {len(final_data['raw_data'])}")
            print(f"   第一条记录content_type: {first_record.get('content_type')}")
            
            # 统计段落记录
            paragraph_records = [r for r in final_data['raw_data'] if r.get('content_type') == 'paragraph']
            print(f"   段落记录数: {len(paragraph_records)}")
            
            if paragraph_records:
                print(f"   第一个段落: {paragraph_records[0].get('content', '')[:80]}...")
        
        print("\n🎉 强制重新解析完成！")
        
    except Exception as e:
        print(f"❌ 强制重新解析失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    force_reparse()
