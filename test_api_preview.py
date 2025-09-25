#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json

def test_api_preview():
    """测试API预览接口"""
    
    # 测试文件ID
    upload_id = "357d434f-3011-4732-aec6-6217392bfe3f"
    
    print(f"🔄 测试API预览接口: {upload_id}")
    
    try:
        # 1. 检查文件状态
        print("\n📋 步骤1: 检查文件状态...")
        status_url = f"http://127.0.0.1:8000/kg/files/{upload_id}/status"
        status_response = requests.get(status_url)
        
        if status_response.status_code == 200:
            status_data = status_response.json()
            print(f"✅ 文件状态: {status_data}")
        else:
            print(f"❌ 获取状态失败: {status_response.status_code}")
            print(f"   响应: {status_response.text}")
            return
        
        # 2. 获取预览数据
        print("\n📄 步骤2: 获取预览数据...")
        preview_url = f"http://127.0.0.1:8000/kg/files/{upload_id}/preview"
        preview_response = requests.get(preview_url)
        
        if preview_response.status_code == 200:
            preview_data = preview_response.json()
            print(f"✅ 预览数据获取成功")
            
            if preview_data.get('success'):
                data = preview_data.get('data', {})
                print(f"   raw_data: {len(data.get('raw_data', []))} 条记录")
                print(f"   entities: {len(data.get('entities', []))} 个实体")
                print(f"   relations: {len(data.get('relations', []))} 个关系")
                print(f"   metadata: {len(data.get('metadata', {}))} 个元数据字段")
                
                # 显示前几条记录
                raw_data = data.get('raw_data', [])
                if raw_data:
                    print("\n   前3条记录:")
                    for i, record in enumerate(raw_data[:3]):
                        content_type = record.get('content_type', 'unknown')
                        content = record.get('content', '')
                        print(f"     记录{i+1}: {content_type} - {content[:80]}...")
                else:
                    print("   ❌ raw_data为空")
            else:
                print(f"   ❌ API返回失败: {preview_data.get('message')}")
        else:
            print(f"❌ 获取预览失败: {preview_response.status_code}")
            print(f"   响应: {preview_response.text}")
            return
        
        # 3. 测试重新解析
        print("\n🔄 步骤3: 测试重新解析...")
        reparse_url = f"http://127.0.0.1:8000/kg/files/{upload_id}/reparse"
        reparse_response = requests.post(reparse_url)
        
        if reparse_response.status_code == 200:
            reparse_data = reparse_response.json()
            print(f"✅ 重新解析请求成功: {reparse_data}")
        else:
            print(f"❌ 重新解析失败: {reparse_response.status_code}")
            print(f"   响应: {reparse_response.text}")
        
        print("\n🎉 API测试完成！")
        
    except Exception as e:
        print(f"❌ API测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_api_preview()
