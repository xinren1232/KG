#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import time

def trigger_api_reparse():
    """通过API触发重新解析"""
    
    upload_id = "357d434f-3011-4732-aec6-6217392bfe3f"
    
    print(f"🔄 通过API触发重新解析: {upload_id}")
    
    try:
        # 1. 检查当前状态
        print("\n📋 步骤1: 检查当前状态...")
        status_url = f"http://127.0.0.1:8000/kg/files/{upload_id}/status"
        status_response = requests.get(status_url)
        
        if status_response.status_code == 200:
            status_data = status_response.json()
            print(f"   当前状态: {status_data['data']['status']}")
        else:
            print(f"❌ 获取状态失败: {status_response.status_code}")
            return
        
        # 2. 直接调用解析任务
        print("\n🔄 步骤2: 直接调用解析任务...")
        parse_url = f"http://127.0.0.1:8000/kg/files/{upload_id}/parse"
        parse_response = requests.post(parse_url)
        
        if parse_response.status_code == 200:
            parse_data = parse_response.json()
            print(f"✅ 解析任务启动: {parse_data}")
        else:
            print(f"❌ 解析任务失败: {parse_response.status_code}")
            print(f"   响应: {parse_response.text}")
            return
        
        # 3. 等待解析完成
        print("\n⏳ 步骤3: 等待解析完成...")
        max_wait = 30  # 最多等待30秒
        wait_time = 0
        
        while wait_time < max_wait:
            time.sleep(2)
            wait_time += 2
            
            status_response = requests.get(status_url)
            if status_response.status_code == 200:
                status_data = status_response.json()
                current_status = status_data['data']['status']
                print(f"   等待中... 当前状态: {current_status}")
                
                if current_status == 'parsed':
                    print("✅ 解析完成！")
                    break
                elif current_status == 'failed':
                    print("❌ 解析失败")
                    return
            else:
                print(f"❌ 状态检查失败: {status_response.status_code}")
                return
        
        if wait_time >= max_wait:
            print("⏰ 等待超时")
            return
        
        # 4. 验证新的解析结果
        print("\n📄 步骤4: 验证新的解析结果...")
        preview_url = f"http://127.0.0.1:8000/kg/files/{upload_id}/preview"
        preview_response = requests.get(preview_url)
        
        if preview_response.status_code == 200:
            preview_data = preview_response.json()
            
            if preview_data.get('success'):
                data = preview_data.get('data', {})
                raw_data = data.get('raw_data', [])
                
                print(f"✅ 新的解析结果:")
                print(f"   raw_data: {len(raw_data)} 条记录")
                
                if raw_data:
                    first_record = raw_data[0]
                    print(f"   第一条记录content_type: {first_record.get('content_type')}")
                    print(f"   第一条记录字段: {list(first_record.keys())}")
                    
                    # 检查段落记录
                    paragraph_records = [r for r in raw_data if r.get('content_type') == 'paragraph']
                    print(f"   段落记录数: {len(paragraph_records)}")
                    
                    if paragraph_records:
                        print(f"   第一个段落: {paragraph_records[0].get('content', '')[:80]}...")
                else:
                    print("   ❌ raw_data仍然为空")
            else:
                print(f"   ❌ API返回失败: {preview_data.get('message')}")
        else:
            print(f"❌ 获取预览失败: {preview_response.status_code}")
        
        print("\n🎉 重新解析测试完成！")
        
    except Exception as e:
        print(f"❌ 重新解析测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    trigger_api_reparse()
