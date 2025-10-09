#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试文档解析功能（带详细日志）
"""

import requests
import json
import time
from pathlib import Path

def test_simple_text_parsing():
    """测试简单文本解析"""
    print("=== 测试简单文本解析 ===")
    
    # 创建简单测试文件
    test_content = """硬件测试报告
电池续航异常
屏幕显示正常
摄像头故障
充电接口正常"""
    
    test_file = 'simple_test_debug.txt'
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    print(f"✅ 创建测试文件: {test_file}")
    
    # 1. 上传文件
    print("1. 上传文件...")
    with open(test_file, 'rb') as f:
        files = {'file': f}
        upload_r = requests.post('http://localhost:8000/kg/upload', files=files)
    
    print(f"   状态码: {upload_r.status_code}")
    if upload_r.status_code == 200:
        upload_result = upload_r.json()
        print(f"   响应: {upload_result}")
        
        if upload_result.get('success'):
            upload_id = upload_result.get('upload_id')
            print(f"   ✅ 上传成功，ID: {upload_id}")
            
            # 2. 触发解析
            print("2. 触发解析...")
            parse_r = requests.post(f'http://localhost:8000/kg/files/{upload_id}/parse')
            print(f"   状态码: {parse_r.status_code}")
            
            if parse_r.status_code == 200:
                parse_result = parse_r.json()
                print(f"   响应: {parse_result}")
                
                if parse_result.get('success'):
                    print("   ✅ 解析触发成功")
                    
                    # 3. 等待解析完成
                    print("3. 等待解析完成...")
                    time.sleep(3)
                    
                    # 4. 检查结果文件是否存在
                    upload_dir = Path(f'api/uploads')
                    result_file = upload_dir / f'{upload_id}_result.json'
                    
                    print(f"4. 检查结果文件: {result_file}")
                    if result_file.exists():
                        print("   ✅ 结果文件存在")
                        
                        # 读取结果文件
                        try:
                            with open(result_file, 'r', encoding='utf-8') as f:
                                result_data = json.load(f)
                            
                            print(f"   原始数据条数: {len(result_data.get('raw_data', []))}")
                            print(f"   实体数量: {len(result_data.get('entities', []))}")
                            print(f"   元数据: {result_data.get('metadata', {})}")
                            
                            # 显示部分内容
                            raw_data = result_data.get('raw_data', [])
                            if raw_data:
                                print("   原始数据示例:")
                                for i, item in enumerate(raw_data[:3]):
                                    print(f"      {i+1}. {item}")
                            
                            entities = result_data.get('entities', [])
                            if entities:
                                print("   识别实体:")
                                for entity in entities[:5]:
                                    print(f"      - {entity}")
                        except Exception as e:
                            print(f"   ❌ 读取结果文件失败: {e}")
                    else:
                        print("   ❌ 结果文件不存在")
                        
                        # 列出目录内容
                        if upload_dir.exists():
                            files_in_dir = list(upload_dir.glob(f"{upload_id}*"))
                            print(f"   目录中相关文件: {[f.name for f in files_in_dir]}")
                        else:
                            print("   ❌ 上传目录不存在")
                    
                    # 5. 测试预览API
                    print("5. 测试预览API...")
                    preview_r = requests.get(f'http://localhost:8000/kg/files/{upload_id}/preview')
                    print(f"   状态码: {preview_r.status_code}")
                    
                    if preview_r.status_code == 200:
                        preview_result = preview_r.json()
                        print(f"   预览成功: {preview_result.get('success')}")
                        
                        if preview_result.get('success'):
                            data = preview_result.get('data', {})
                            print(f"   ✅ 预览数据包含: {list(data.keys())}")
                            print(f"   实体数量: {len(data.get('entities', []))}")
                            print(f"   关系数量: {len(data.get('relations', []))}")
                            print(f"   原始数据数量: {len(data.get('raw_data', []))}")
                            
                            # 显示一些实体
                            entities = data.get('entities', [])
                            if entities:
                                print("   识别的实体:")
                                for entity in entities[:3]:
                                    name = entity.get('name')
                                    entity_type = entity.get('type')
                                    confidence = entity.get('confidence', 0)
                                    print(f"      - {name} ({entity_type}) - 置信度: {confidence}")
                        else:
                            print(f"   ❌ 预览失败: {preview_result.get('message')}")
                    else:
                        print(f"   ❌ 预览请求失败: {preview_r.text}")
                else:
                    print(f"   ❌ 解析失败: {parse_result.get('message')}")
            else:
                print(f"   ❌ 解析请求失败: {parse_r.text}")
        else:
            print(f"   ❌ 上传失败: {upload_result.get('message')}")
    else:
        print(f"   ❌ 上传请求失败: {upload_r.text}")

def main():
    """主函数"""
    print("🔍 开始测试文档解析功能（带详细日志）...")
    
    # 检查API状态
    try:
        r = requests.get('http://localhost:8000/health', timeout=5)
        if r.status_code == 200:
            print("✅ API服务器连接正常")
        else:
            print(f"❌ API服务器响应异常: {r.status_code}")
            return
    except Exception as e:
        print(f"❌ 无法连接到API服务器: {e}")
        return
    
    # 测试简单文本解析
    test_simple_text_parsing()

if __name__ == "__main__":
    main()
