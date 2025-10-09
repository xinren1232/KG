#!/usr/bin/env python3
import requests
import time

def main():
    print("🔧 验证DOC文档解析修复")
    
    # 创建测试DOC文件
    content = """硬件测试报告

电池测试结果：异常
屏幕测试结果：正常
摄像头测试结果：故障

问题分析：
电池续航时间不足，需要更换供应商。
摄像头模块存在缺陷，建议重新设计。
"""
    
    with open('simple_test.doc', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ 创建测试文件: simple_test.doc")
    
    try:
        # 测试上传
        with open('simple_test.doc', 'rb') as f:
            files = {'file': f}
            response = requests.post('http://localhost:8000/kg/upload', files=files, timeout=10)
        
        print(f"上传响应: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"上传结果: {result}")
            
            if result.get('success'):
                upload_id = result.get('upload_id')
                print(f"✅ 上传成功，ID: {upload_id}")
                
                # 测试解析
                parse_response = requests.post(f'http://localhost:8000/kg/files/{upload_id}/parse', timeout=10)
                print(f"解析响应: {parse_response.status_code}")
                
                if parse_response.status_code == 200:
                    parse_result = parse_response.json()
                    print(f"解析结果: {parse_result}")
                    
                    if parse_result.get('success'):
                        print("✅ 解析触发成功")
                        
                        # 等待并获取结果
                        time.sleep(3)
                        preview_response = requests.get(f'http://localhost:8000/kg/files/{upload_id}/preview', timeout=10)
                        
                        if preview_response.status_code == 200:
                            preview_result = preview_response.json()
                            print(f"预览结果: {preview_result}")
                            
                            if preview_result.get('success'):
                                data = preview_result.get('data', {})
                                raw_data = data.get('raw_data', [])
                                entities = data.get('entities', [])
                                
                                print(f"🎉 DOC解析修复成功!")
                                print(f"   数据条数: {len(raw_data)}")
                                print(f"   实体数量: {len(entities)}")
                                
                                if raw_data:
                                    print("   解析内容:")
                                    for i, item in enumerate(raw_data[:3]):
                                        print(f"      {i+1}. {item.get('content', '')[:50]}...")
                                
                                return True
                            else:
                                print(f"❌ 预览失败: {preview_result.get('message')}")
                        else:
                            print(f"❌ 预览请求失败: {preview_response.text}")
                    else:
                        print(f"❌ 解析失败: {parse_result.get('message')}")
                else:
                    print(f"❌ 解析请求失败: {parse_response.text}")
            else:
                print(f"❌ 上传失败: {result.get('message')}")
        else:
            print(f"❌ 上传请求失败: {response.text}")
    
    except Exception as e:
        print(f"❌ 测试异常: {e}")
        import traceback
        traceback.print_exc()
    
    return False

if __name__ == "__main__":
    main()
