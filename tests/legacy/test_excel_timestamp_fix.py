#!/usr/bin/env python3
import requests
import json
import time
import pandas as pd
from pathlib import Path

def create_test_excel_with_timestamps():
    """创建包含时间戳的测试Excel文件"""
    print("📊 创建包含时间戳的测试Excel文件...")
    
    # 创建包含时间戳的测试数据
    data = {
        '问题编号': ['ISSUE-001', 'ISSUE-002', 'ISSUE-003'],
        '问题描述': ['屏幕显示异常', '电池续航不足', '摄像头模糊'],
        '发生时间': pd.to_datetime(['2025-01-15 10:30:00', '2025-01-16 14:20:00', '2025-01-17 09:15:00']),
        '解决时间': pd.to_datetime(['2025-01-15 16:45:00', '2025-01-17 11:30:00', '2025-01-18 13:20:00']),
        '组件': ['显示屏', '电池', '摄像头'],
        '严重程度': ['高', '中', '低']
    }
    
    df = pd.DataFrame(data)
    test_file = 'test_excel_with_timestamps.xlsx'
    df.to_excel(test_file, index=False)
    
    print(f"   ✅ 创建测试文件: {test_file}")
    print(f"   数据行数: {len(df)}")
    print(f"   列名: {list(df.columns)}")
    print(f"   时间戳列: 发生时间, 解决时间")
    
    return test_file

def test_excel_timestamp_parsing():
    """测试Excel时间戳解析修复"""
    
    print("=== 测试Excel时间戳解析修复 ===")
    
    # 1. 创建测试文件
    test_file = create_test_excel_with_timestamps()
    
    # 2. 上传Excel文件
    print("\n1. 上传包含时间戳的Excel文件...")
    try:
        with open(test_file, 'rb') as f:
            files = {'file': f}
            upload_response = requests.post('http://localhost:8000/kg/upload', files=files)
        
        print(f"   上传状态码: {upload_response.status_code}")
        
        if upload_response.status_code != 200:
            print(f"   ❌ 上传失败: HTTP {upload_response.status_code}")
            print(f"   响应: {upload_response.text}")
            return
        
        upload_result = upload_response.json()
        if not upload_result.get('success'):
            print(f"   ❌ 上传失败: {upload_result.get('message')}")
            return
            
        upload_id = upload_result.get('upload_id')
        print(f"   ✅ Excel文件上传成功，ID: {upload_id}")
        
    except Exception as e:
        print(f"   ❌ 上传异常: {e}")
        return
    
    # 3. 触发解析
    print("\n2. 触发Excel解析...")
    try:
        parse_response = requests.post(f'http://localhost:8000/kg/files/{upload_id}/parse')
        
        print(f"   解析状态码: {parse_response.status_code}")
        
        if parse_response.status_code != 200:
            print(f"   ❌ 解析请求失败: HTTP {parse_response.status_code}")
            print(f"   响应: {parse_response.text}")
            return
        
        # 检查响应是否包含时间戳序列化错误
        parse_text = parse_response.text
        if "Timestamp" in parse_text and "not JSON serializable" in parse_text:
            print(f"   ❌ 仍然存在时间戳序列化错误")
            print(f"   错误响应: {parse_text}")
            return
        
        try:
            parse_result = parse_response.json()
            print(f"   ✅ 解析响应JSON解析成功")
            
            if not parse_result.get('success'):
                print(f"   ❌ 解析失败: {parse_result.get('message')}")
                return
            
            print(f"   ✅ Excel解析触发成功")
            
        except json.JSONDecodeError as e:
            print(f"   ❌ 解析响应JSON解析失败: {e}")
            print(f"   原始响应: {parse_text}")
            return
        
    except Exception as e:
        print(f"   ❌ 解析异常: {e}")
        return
    
    # 4. 等待解析完成
    print("\n3. 等待解析完成...")
    time.sleep(3)
    
    # 5. 获取解析结果
    print("\n4. 获取Excel解析结果...")
    try:
        preview_response = requests.get(f'http://localhost:8000/kg/files/{upload_id}/preview')
        
        print(f"   预览状态码: {preview_response.status_code}")
        
        if preview_response.status_code != 200:
            print(f"   ❌ 预览请求失败: HTTP {preview_response.status_code}")
            print(f"   响应: {preview_response.text}")
            return
        
        # 检查预览响应是否包含时间戳序列化错误
        preview_text = preview_response.text
        if "Timestamp" in preview_text and "not JSON serializable" in preview_text:
            print(f"   ❌ 预览响应仍然存在时间戳序列化错误")
            print(f"   错误响应: {preview_text}")
            return
        
        try:
            preview_result = preview_response.json()
            print(f"   ✅ 预览响应JSON解析成功")
            
            if not preview_result.get('success'):
                print(f"   ❌ 预览失败: {preview_result.get('message')}")
                return
            
            # 检查解析结果
            data = preview_result.get('data', {})
            raw_data = data.get('raw_data', [])
            metadata = data.get('metadata', {})
            
            print(f"   ✅ Excel解析成功")
            print(f"   原始数据条数: {len(raw_data)}")
            print(f"   文件类型: {metadata.get('file_type')}")
            
            # 检查时间戳字段是否正确序列化
            if raw_data:
                print("\n   📄 检查时间戳字段序列化:")
                first_record = raw_data[0]
                
                for key, value in first_record.items():
                    if '时间' in key:
                        print(f"      {key}: {value} (类型: {type(value).__name__})")
                        
                        # 验证时间戳是否为字符串格式
                        if isinstance(value, str):
                            print(f"         ✅ 时间戳已正确序列化为字符串")
                        else:
                            print(f"         ❌ 时间戳未正确序列化: {type(value)}")
            
            print("\n✅ Excel时间戳解析修复测试完成 - 修复成功")
            
        except json.JSONDecodeError as e:
            print(f"   ❌ 预览响应JSON解析失败: {e}")
            print(f"   错误位置: 第{e.lineno}行，第{e.colno}列")
            print(f"   原始响应前500字符: {preview_text[:500]}")
            
            # 查找时间戳相关错误
            if "Timestamp" in preview_text:
                print("   🔍 发现Timestamp相关内容:")
                lines = preview_text.split('\n')
                for i, line in enumerate(lines):
                    if "Timestamp" in line:
                        print(f"      第{i+1}行: {line}")
            
            return
        
    except Exception as e:
        print(f"   ❌ 预览异常: {e}")
        return
    
    # 6. 清理测试文件
    try:
        Path(test_file).unlink()
        print(f"\n🧹 清理测试文件: {test_file}")
    except:
        pass

if __name__ == "__main__":
    test_excel_timestamp_parsing()
