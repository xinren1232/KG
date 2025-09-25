#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.main_v01 import do_parse
import asyncio

async def trigger_reparse():
    """触发重新解析"""
    
    upload_id = "357d434f-3011-4732-aec6-6217392bfe3f"
    
    print(f"🔄 触发重新解析: {upload_id}")
    
    try:
        # 调用解析函数
        await do_parse(upload_id)
        print("✅ 重新解析完成")
        
        # 验证结果
        from api.files.manager import load_preview
        preview_data = load_preview(upload_id)
        
        print(f"📊 解析结果:")
        print(f"   raw_data: {len(preview_data.get('raw_data', []))} 条记录")
        
        # 检查第一条记录的格式
        if preview_data.get('raw_data'):
            first_record = preview_data['raw_data'][0]
            print(f"   第一条记录content_type: {first_record.get('content_type')}")
            print(f"   第一条记录字段: {list(first_record.keys())}")
        
    except Exception as e:
        print(f"❌ 重新解析失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(trigger_reparse())
