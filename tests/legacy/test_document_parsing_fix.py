#!/usr/bin/env python3
import requests
import time
import json

def test_document_parsing():
    """测试文档解析功能修复"""
    
    print("=== 测试文档解析功能修复 ===")
    
    # 1. 测试文件上传
    print("\n1. 测试文件上传...")
    try:
        files = {'file': open('test_simple.txt', 'rb')}
        upload_response = requests.post('http://localhost:8000/kg/upload', files=files)
        
        print(f"   上传状态码: {upload_response.status_code}")
        upload_result = upload_response.json()
        print(f"   上传成功: {upload_result.get('success')}")
        
        if not upload_result.get('success'):
            print(f"   ❌ 文件上传失败: {upload_result.get('message')}")
            return
            
        upload_id = upload_result.get('upload_id')
        print(f"   ✅ 文件上传成功，ID: {upload_id}")
        
    except Exception as e:
        print(f"   ❌ 上传异常: {e}")
        return
    
    # 2. 测试状态检查（修复后应该能找到文件）
    print("\n2. 测试状态检查...")
    try:
        status_response = requests.get(f'http://localhost:8000/kg/files/{upload_id}/status')
        
        print(f"   状态检查状态码: {status_response.status_code}")
        status_result = status_response.json()
        print(f"   状态检查成功: {status_result.get('success')}")
        
        if status_result.get('success'):
            file_status = status_result.get('data', {}).get('status')
            print(f"   ✅ 文件状态: {file_status}")
        else:
            print(f"   ❌ 状态检查失败: {status_result.get('message')}")
            return
            
    except Exception as e:
        print(f"   ❌ 状态检查异常: {e}")
        return
    
    # 3. 测试解析触发
    print("\n3. 测试解析触发...")
    try:
        parse_response = requests.post(f'http://localhost:8000/kg/files/{upload_id}/parse')
        
        print(f"   解析状态码: {parse_response.status_code}")
        parse_result = parse_response.json()
        print(f"   解析触发成功: {parse_result.get('success')}")
        
        if not parse_result.get('success'):
            print(f"   ❌ 解析触发失败: {parse_result.get('message')}")
            return
            
        print("   ✅ 解析触发成功")
        
    except Exception as e:
        print(f"   ❌ 解析异常: {e}")
        return
    
    # 4. 等待解析完成并检查状态
    print("\n4. 等待解析完成...")
    max_attempts = 10
    for attempt in range(max_attempts):
        try:
            time.sleep(1)
            status_response = requests.get(f'http://localhost:8000/kg/files/{upload_id}/status')
            status_result = status_response.json()
            
            if status_result.get('success'):
                file_status = status_result.get('data', {}).get('status')
                print(f"   尝试 {attempt + 1}: 状态 = {file_status}")
                
                if file_status == 'parsed':
                    print("   ✅ 文件解析完成")
                    break
            else:
                print(f"   ❌ 状态检查失败: {status_result.get('message')}")
                break
                
        except Exception as e:
            print(f"   ❌ 状态检查异常: {e}")
            break
    else:
        print("   ⚠️ 解析超时")
    
    # 5. 获取解析结果
    print("\n5. 获取解析结果...")
    try:
        preview_response = requests.get(f'http://localhost:8000/kg/files/{upload_id}/preview')
        
        print(f"   预览状态码: {preview_response.status_code}")
        preview_result = preview_response.json()
        
        success = preview_result.get('success')
        print(f"   预览成功: {success}")
        
        if success:
            data = preview_result.get('data', {})
            raw_data = data.get('raw_data', [])
            entities = data.get('entities', [])
            relations = data.get('relations', [])
            metadata = data.get('metadata', {})
            
            print(f"   ✅ 解析结果获取成功")
            print(f"   原始数据条数: {len(raw_data)}")
            print(f"   实体数量: {len(entities)}")
            print(f"   关系数量: {len(relations)}")
            print(f"   文件类型: {metadata.get('file_type')}")
            
            # 显示原始数据样本
            if raw_data:
                print("\n   📄 原始数据样本:")
                for i, item in enumerate(raw_data[:3]):
                    content = str(item.get('content', ''))[:100]
                    print(f"      {i+1}. {content}...")
            
            # 显示实体样本
            if entities:
                print("\n   🏷️ 实体样本:")
                for i, entity in enumerate(entities[:5]):
                    name = entity.get('name')
                    entity_type = entity.get('type')
                    confidence = entity.get('confidence', 'N/A')
                    print(f"      {i+1}. {name} ({entity_type}) - 置信度: {confidence}")
            
            print("\n✅ 文档解析功能测试完成 - 所有功能正常工作")
        else:
            message = preview_result.get('message', '未知错误')
            print(f"   ❌ 预览失败: {message}")
            
    except Exception as e:
        print(f"   ❌ 预览异常: {e}")

if __name__ == "__main__":
    test_document_parsing()
