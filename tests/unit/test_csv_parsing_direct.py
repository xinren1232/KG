#!/usr/bin/env python3
"""
直接测试CSV解析功能
"""

import requests
import time
import json

def test_csv_parsing_direct():
    """直接测试CSV解析"""
    print("=== 直接测试CSV解析功能 ===")
    
    # 1. 上传CSV文件
    print("\n📁 步骤1: 上传CSV文件")
    
    try:
        with open('test_files/test_data.csv', 'rb') as f:
            files = {
                'file': ('test_data.csv', f, 'text/csv')
            }
            
            response = requests.post("http://127.0.0.1:8000/kg/upload", files=files, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    upload_id = result.get('upload_id')
                    print(f"✅ 文件上传成功 (ID: {upload_id})")
                else:
                    print(f"❌ 上传失败: {result.get('message')}")
                    return False
            else:
                print(f"❌ 上传请求失败: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ 上传异常: {e}")
        return False
    
    # 2. 检查文件状态
    print(f"\n🔍 步骤2: 检查文件状态")
    try:
        status_response = requests.get(f"http://127.0.0.1:8000/kg/files/{upload_id}/status", timeout=10)
        
        if status_response.status_code == 200:
            status_result = status_response.json()
            print(f"状态查询结果: {status_result}")
        else:
            print(f"❌ 状态查询失败: {status_response.status_code}")
            
    except Exception as e:
        print(f"❌ 状态查询异常: {e}")
    
    # 3. 手动触发解析
    print(f"\n🔧 步骤3: 手动触发解析")
    try:
        parse_response = requests.post(f"http://127.0.0.1:8000/kg/files/{upload_id}/parse", timeout=30)
        
        if parse_response.status_code == 200:
            parse_result = parse_response.json()
            print(f"解析触发结果: {parse_result}")
            
            if not parse_result.get('success'):
                print(f"❌ 解析触发失败: {parse_result.get('message')}")
                return False
        else:
            print(f"❌ 解析请求失败: {parse_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 解析触发异常: {e}")
        return False
    
    # 4. 监控解析过程
    print(f"\n⏳ 步骤4: 监控解析过程")
    max_attempts = 10
    
    for attempt in range(max_attempts):
        try:
            status_response = requests.get(f"http://127.0.0.1:8000/kg/files/{upload_id}/status", timeout=10)
            
            if status_response.status_code == 200:
                status_result = status_response.json()
                if status_result.get('success'):
                    status_data = status_result.get('data', {})
                    file_status = status_data.get('status')
                    
                    print(f"   轮询 {attempt+1}: {file_status}")
                    
                    if file_status == 'parsed':
                        print("✅ 解析完成")
                        break
                    elif file_status == 'failed':
                        error = status_data.get('error', '未知错误')
                        print(f"❌ 解析失败: {error}")
                        return False
                    elif file_status in ['parsing', 'uploaded']:
                        time.sleep(2)
                        continue
                    else:
                        print(f"⚠ 意外状态: {file_status}")
                        time.sleep(2)
                        continue
                else:
                    print(f"❌ 状态查询失败: {status_result.get('message')}")
                    return False
            else:
                print(f"❌ 状态查询请求失败: {status_response.status_code}")
                return False
                
        except Exception as e:
            print(f"⚠ 状态查询异常: {e}")
            time.sleep(2)
            continue
    else:
        print("❌ 解析超时")
        return False
    
    # 5. 验证解析结果
    print(f"\n✅ 步骤5: 验证解析结果")
    try:
        preview_response = requests.get(f"http://127.0.0.1:8000/kg/files/{upload_id}/preview", timeout=15)
        
        if preview_response.status_code == 200:
            preview_result = preview_response.json()
            if preview_result.get('success'):
                preview_data = preview_result.get('data', {})
                
                raw_data = preview_data.get('raw_data', [])
                entities = preview_data.get('entities', [])
                relations = preview_data.get('relations', [])
                metadata = preview_data.get('metadata', {})
                
                print(f"📊 CSV解析结果:")
                print(f"   原始记录: {len(raw_data)} 条")
                print(f"   抽取实体: {len(entities)} 个")
                print(f"   抽取关系: {len(relations)} 个")
                print(f"   元数据: {metadata}")
                
                if raw_data:
                    first_record = raw_data[0]
                    print(f"\n📋 第一条记录:")
                    for key, value in first_record.items():
                        print(f"   {key}: {value}")
                    
                    print("✅ CSV解析成功")
                    return True
                else:
                    print("❌ 没有解析数据")
                    return False
            else:
                print(f"❌ 获取解析结果失败: {preview_result.get('message')}")
                return False
        else:
            print(f"❌ 解析结果请求失败: {preview_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 验证结果异常: {e}")
        return False

if __name__ == "__main__":
    print("🧪 直接测试CSV解析功能")
    print("="*60)
    
    success = test_csv_parsing_direct()
    
    print("\n" + "="*60)
    if success:
        print("🎉 CSV解析功能测试成功！")
    else:
        print("❌ CSV解析功能测试失败！")
    
    print("\n📋 测试完成！")
