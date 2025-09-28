#!/usr/bin/env python3
"""
测试文档上传和解析功能
"""
import requests
import json
import time

def test_upload_and_parse():
    """测试文档上传和解析流程"""
    
    # 1. 上传文件
    print("🔄 正在上传文件...")
    with open('test_upload.txt', 'rb') as f:
        files = {'file': ('test_upload.txt', f, 'text/plain')}
        response = requests.post('http://localhost:8000/kg/upload', files=files)
    
    if response.status_code != 200:
        print(f"❌ 上传失败: {response.status_code}")
        print(response.text)
        return
    
    upload_result = response.json()
    print(f"✅ 上传成功: {upload_result}")
    
    upload_id = upload_result.get('upload_id')
    if not upload_id:
        print("❌ 未获取到upload_id")
        return
    
    # 2. 触发解析
    print(f"🔄 正在触发解析: {upload_id}")
    parse_response = requests.post(f'http://localhost:8000/kg/files/{upload_id}/parse')
    
    if parse_response.status_code != 200:
        print(f"❌ 解析触发失败: {parse_response.status_code}")
        print(parse_response.text)
        return
    
    parse_result = parse_response.json()
    print(f"✅ 解析触发成功: {parse_result}")
    
    # 3. 轮询状态
    print("🔄 正在等待解析完成...")
    max_attempts = 30
    for attempt in range(max_attempts):
        status_response = requests.get(f'http://localhost:8000/kg/files/{upload_id}/status')
        
        if status_response.status_code != 200:
            print(f"❌ 状态查询失败: {status_response.status_code}")
            continue
        
        status_result = status_response.json()
        file_status = status_result.get('status')
        print(f"📊 当前状态: {file_status}")
        
        if file_status == 'parsed':
            print("✅ 解析完成!")
            break
        elif file_status == 'error':
            print(f"❌ 解析失败: {status_result.get('message', '未知错误')}")
            return
        
        time.sleep(2)
    else:
        print("⏰ 解析超时")
        return
    
    # 4. 获取预览结果
    print("🔄 正在获取解析结果...")
    preview_response = requests.get(f'http://localhost:8000/kg/files/{upload_id}/preview')
    
    if preview_response.status_code != 200:
        print(f"❌ 预览获取失败: {preview_response.status_code}")
        print(preview_response.text)
        return
    
    preview_result = preview_response.json()
    print("✅ 解析结果获取成功!")
    
    # 显示结果统计
    data = preview_result.get('data', {})
    entities = data.get('entities', [])
    relations = data.get('relations', [])
    
    print(f"\n📊 解析统计:")
    print(f"   实体数量: {len(entities)}")
    print(f"   关系数量: {len(relations)}")
    
    # 显示部分实体
    if entities:
        print(f"\n🏷️  实体示例:")
        for i, entity in enumerate(entities[:5]):
            print(f"   {i+1}. {entity.get('name', 'N/A')} ({entity.get('type', 'N/A')})")
    
    # 显示部分关系
    if relations:
        print(f"\n🔗 关系示例:")
        for i, relation in enumerate(relations[:5]):
            print(f"   {i+1}. {relation.get('source', 'N/A')} -> {relation.get('target', 'N/A')} ({relation.get('type', 'N/A')})")
    
    return upload_id, preview_result

if __name__ == "__main__":
    try:
        result = test_upload_and_parse()
        if result:
            print("\n🎉 测试完成!")
        else:
            print("\n❌ 测试失败!")
    except Exception as e:
        print(f"❌ 测试异常: {e}")
