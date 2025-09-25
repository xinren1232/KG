#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.parsers.ir_unified_parser import IRUnifiedParser
from pathlib import Path

def test_docx_parsing():
    """测试DOCX解析功能"""

    # 找到一个真正的DOCX文件
    docx_file = Path("api/uploads/357d434f-3011-4732-aec6-6217392bfe3f")

    if not docx_file.exists():
        print(f"❌ DOCX文件不存在: {docx_file}")
        return

    print(f"📄 测试DOCX文件: {docx_file}")
    print(f"   文件大小: {docx_file.stat().st_size} bytes")

    try:
        # 创建统一解析器
        parser = IRUnifiedParser()
        print("✅ IRUnifiedParser 创建成功")

        # 解析文件
        print("🔄 开始解析DOCX文件...")
        result = parser.parse_document(docx_file, ".docx")
        
        if result:
            print(f"✅ 解析成功！")
            print(f"   解析结果类型: {type(result)}")
            print(f"   解析结果长度: {len(result) if hasattr(result, '__len__') else 'N/A'}")
            
            # 显示前几条记录
            if isinstance(result, list) and len(result) > 0:
                print(f"   前3条记录:")
                for i, record in enumerate(result[:3]):
                    if isinstance(record, dict):
                        content_type = record.get('content_type', 'unknown')
                        content = record.get('content', '')
                        print(f"     记录{i+1}: {content_type} - {content[:100]}...")
                    else:
                        print(f"     记录{i+1}: {str(record)[:100]}...")
            elif isinstance(result, str):
                print(f"   文本内容预览: {result[:200]}...")
            else:
                print(f"   结果内容: {result}")
        else:
            print("❌ 解析结果为空")
            
    except Exception as e:
        print(f"❌ 解析失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_docx_parsing()
