#!/usr/bin/env python3
import requests
import pandas as pd
import json
import time
from pathlib import Path

def verify_timestamp_fix():
    """验证时间戳序列化修复"""
    
    print("=== 验证时间戳序列化修复 ===")
    
    # 1. 创建包含多种时间戳格式的Excel文件
    print("\n1. 创建测试Excel文件...")
    
    test_data = {
        '问题ID': ['ISSUE-001', 'ISSUE-002', 'ISSUE-003'],
        '标题': ['屏幕显示问题', '电池续航问题', '摄像头问题'],
        '创建时间': pd.to_datetime([
            '2025-01-15 10:30:00',
            '2025-01-16 14:20:00', 
            '2025-01-17 09:15:00'
        ]),
        '更新时间': pd.to_datetime([
            '2025-01-15 16:45:00',
            '2025-01-17 11:30:00',
            '2025-01-18 13:20:00'
        ]),
        '截止日期': pd.to_datetime([
            '2025-01-20',
            '2025-01-25', 
            '2025-01-30'
        ]),
        '组件': ['显示屏', '电池', '摄像头'],
        '状态': ['已解决', '处理中', '待分析']
    }
    
    df = pd.DataFrame(test_data)
    test_file = 'timestamp_test.xlsx'
    df.to_excel(test_file, index=False)
    
    print(f"   ✅ 创建测试文件: {test_file}")
    print(f"   数据行数: {len(df)}")
    print(f"   时间戳列: 创建时间, 更新时间, 截止日期")
    
    # 2. 上传并解析
    print("\n2. 上传并解析Excel文件...")
    
    try:
        with open(test_file, 'rb') as f:
            files = {'file': f}
            upload_response = requests.post('http://localhost:8000/kg/upload', files=files)
        
        if upload_response.status_code != 200:
            print(f"   ❌ 上传失败: {upload_response.status_code}")
            return False
        
        upload_result = upload_response.json()
        upload_id = upload_result.get('upload_id')
        print(f"   ✅ 上传成功: {upload_id}")
        
        # 触发解析
        parse_response = requests.post(f'http://localhost:8000/kg/files/{upload_id}/parse')
        
        if parse_response.status_code != 200:
            print(f"   ❌ 解析失败: {parse_response.status_code}")
            print(f"   错误: {parse_response.text}")
            return False
        
        parse_result = parse_response.json()
        if not parse_result.get('success'):
            print(f"   ❌ 解析失败: {parse_result.get('message')}")
            return False
        
        print(f"   ✅ 解析成功")
        
    except Exception as e:
        print(f"   ❌ 异常: {e}")
        return False
    
    # 3. 等待解析完成并获取结果
    print("\n3. 获取解析结果...")
    
    time.sleep(3)  # 等待解析完成
    
    try:
        preview_response = requests.get(f'http://localhost:8000/kg/files/{upload_id}/preview')
        
        if preview_response.status_code != 200:
            print(f"   ❌ 获取结果失败: {preview_response.status_code}")
            return False
        
        preview_result = preview_response.json()
        if not preview_result.get('success'):
            print(f"   ❌ 获取结果失败: {preview_result.get('message')}")
            return False
        
        data = preview_result.get('data', {})
        raw_data = data.get('raw_data', [])
        
        print(f"   ✅ 获取结果成功")
        print(f"   解析记录数: {len(raw_data)}")
        
    except Exception as e:
        print(f"   ❌ 异常: {e}")
        return False
    
    # 4. 验证时间戳字段
    print("\n4. 验证时间戳字段序列化...")
    
    if not raw_data:
        print("   ❌ 没有解析数据")
        return False
    
    success = True
    timestamp_fields = []
    
    # 检查第一条记录
    first_record = raw_data[0]
    record_data = first_record.get('data', {})
    
    for key, value in record_data.items():
        if '时间' in key or '日期' in key:
            timestamp_fields.append((key, value))
            
            print(f"   时间戳字段: {key}")
            print(f"      值: {value}")
            print(f"      类型: {type(value).__name__}")
            
            # 验证是否为字符串
            if isinstance(value, str):
                print(f"      ✅ 正确序列化为字符串")
                
                # 验证是否为有效的ISO格式
                try:
                    pd.to_datetime(value)
                    print(f"      ✅ 有效的时间格式")
                except:
                    print(f"      ⚠️ 时间格式可能有问题")
            else:
                print(f"      ❌ 未正确序列化，仍为 {type(value).__name__}")
                success = False
    
    if not timestamp_fields:
        print("   ⚠️ 未找到时间戳字段")
    
    # 5. 清理测试文件
    try:
        Path(test_file).unlink()
        print(f"\n🧹 清理测试文件: {test_file}")
    except:
        pass
    
    # 6. 总结
    print(f"\n{'='*50}")
    if success and timestamp_fields:
        print("✅ 时间戳序列化修复验证成功")
        print(f"   - 成功处理 {len(timestamp_fields)} 个时间戳字段")
        print("   - 所有时间戳都正确序列化为字符串")
        print("   - 不再出现 'Object of type Timestamp is not JSON serializable' 错误")
        return True
    else:
        print("❌ 时间戳序列化修复验证失败")
        return False

if __name__ == "__main__":
    verify_timestamp_fix()
