#!/usr/bin/env python3
import requests
import json
import time

def debug_timestamp_issue():
    """调试时间戳序列化问题"""
    
    print("=== 调试时间戳序列化问题 ===")
    
    # 1. 上传文件
    print("\n1. 上传测试文件...")
    try:
        files = {'file': open('test_simple.txt', 'rb')}
        upload_response = requests.post('http://localhost:8000/kg/upload', files=files)
        
        print(f"   上传状态码: {upload_response.status_code}")
        print(f"   上传响应: {upload_response.text}")
        
        upload_result = upload_response.json()
        if not upload_result.get('success'):
            print(f"   ❌ 上传失败: {upload_result.get('message')}")
            return
            
        upload_id = upload_result.get('upload_id')
        print(f"   ✅ 上传成功，ID: {upload_id}")
        
    except Exception as e:
        print(f"   ❌ 上传异常: {e}")
        return
    
    # 2. 触发解析并捕获详细错误
    print("\n2. 触发解析...")
    try:
        parse_response = requests.post(f'http://localhost:8000/kg/files/{upload_id}/parse')
        
        print(f"   解析状态码: {parse_response.status_code}")
        print(f"   解析响应头: {dict(parse_response.headers)}")
        
        # 获取原始响应文本
        parse_text = parse_response.text
        print(f"   解析响应长度: {len(parse_text)}")
        print(f"   解析响应前500字符: {parse_text[:500]}")
        
        # 尝试解析JSON
        try:
            parse_result = json.loads(parse_text)
            print(f"   ✅ JSON解析成功")
            print(f"   解析结果: {parse_result}")
        except json.JSONDecodeError as json_error:
            print(f"   ❌ JSON解析失败: {json_error}")
            print(f"   错误位置: 第{json_error.lineno}行，第{json_error.colno}列")
            print(f"   错误内容: {json_error.msg}")
            
            # 查找可能的时间戳问题
            if "Timestamp" in parse_text:
                print("   🔍 发现Timestamp关键词")
                lines = parse_text.split('\n')
                for i, line in enumerate(lines):
                    if "Timestamp" in line:
                        print(f"      第{i+1}行: {line}")
            
            return
        
    except Exception as e:
        print(f"   ❌ 解析异常: {e}")
        return
    
    # 3. 等待解析完成
    print("\n3. 等待解析完成...")
    time.sleep(3)
    
    # 4. 获取预览数据并检查时间戳
    print("\n4. 获取预览数据...")
    try:
        preview_response = requests.get(f'http://localhost:8000/kg/files/{upload_id}/preview')
        
        print(f"   预览状态码: {preview_response.status_code}")
        
        # 获取原始响应文本
        preview_text = preview_response.text
        print(f"   预览响应长度: {len(preview_text)}")
        
        # 检查是否包含时间戳问题
        if "Timestamp" in preview_text:
            print("   🔍 预览响应中发现Timestamp关键词")
            lines = preview_text.split('\n')
            for i, line in enumerate(lines):
                if "Timestamp" in line:
                    print(f"      第{i+1}行: {line}")
        
        # 尝试解析JSON
        try:
            preview_result = json.loads(preview_text)
            print(f"   ✅ 预览JSON解析成功")
            
            # 检查数据结构
            data = preview_result.get('data', {})
            metadata = data.get('metadata', {})
            
            print(f"   元数据: {metadata}")
            
            # 检查是否有时间戳字段
            for key, value in metadata.items():
                if 'time' in key.lower():
                    print(f"   时间字段 {key}: {value} (类型: {type(value)})")
            
        except json.JSONDecodeError as json_error:
            print(f"   ❌ 预览JSON解析失败: {json_error}")
            print(f"   错误位置: 第{json_error.lineno}行，第{json_error.colno}列")
            print(f"   错误内容: {json_error.msg}")
            
            # 显示错误附近的内容
            lines = preview_text.split('\n')
            error_line = json_error.lineno - 1
            start = max(0, error_line - 2)
            end = min(len(lines), error_line + 3)
            
            print("   错误附近的内容:")
            for i in range(start, end):
                marker = " >>> " if i == error_line else "     "
                print(f"{marker}第{i+1}行: {lines[i]}")
        
    except Exception as e:
        print(f"   ❌ 预览异常: {e}")

if __name__ == "__main__":
    debug_timestamp_issue()
