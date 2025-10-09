#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试文档解析问题
"""

import requests
import json
import time
import os
from pathlib import Path

def test_simple_text_parsing():
    """测试简单文本解析"""
    print("=== 测试简单文本解析 ===")
    
    # 创建简单测试文件
    test_content = """硬件测试报告
电池续航异常
屏幕显示正常
摄像头故障"""
    
    test_file = 'simple_test.txt'
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    print(f"✅ 创建测试文件: {test_file}")
    
    # 1. 上传文件
    print("1. 上传文件...")
    with open(test_file, 'rb') as f:
        files = {'file': f}
        upload_r = requests.post('http://localhost:8000/kg/upload', files=files)
    
    print(f"   状态码: {upload_r.status_code}")
    print(f"   响应: {upload_r.text}")
    
    if upload_r.status_code == 200:
        upload_result = upload_r.json()
        if upload_result.get('success'):
            upload_id = upload_result.get('upload_id')
            print(f"   ✅ 上传成功，ID: {upload_id}")
            
            # 2. 触发解析
            print("2. 触发解析...")
            parse_r = requests.post(f'http://localhost:8000/kg/files/{upload_id}/parse')
            print(f"   状态码: {parse_r.status_code}")
            print(f"   响应: {parse_r.text}")
            
            if parse_r.status_code == 200:
                parse_result = parse_r.json()
                if parse_result.get('success'):
                    print("   ✅ 解析触发成功")
                    
                    # 3. 等待解析完成
                    print("3. 等待解析完成...")
                    time.sleep(3)
                    
                    # 4. 检查结果文件是否存在
                    upload_dir = Path(f'api/uploads/{upload_id}')
                    result_file = upload_dir / f'{upload_id}_result.json'
                    
                    print(f"4. 检查结果文件: {result_file}")
                    if result_file.exists():
                        print("   ✅ 结果文件存在")
                        
                        # 读取结果文件
                        with open(result_file, 'r', encoding='utf-8') as f:
                            result_data = json.load(f)
                        
                        print(f"   原始数据条数: {len(result_data.get('raw_data', []))}")
                        print(f"   实体数量: {len(result_data.get('entities', []))}")
                        
                        # 显示部分内容
                        raw_data = result_data.get('raw_data', [])
                        if raw_data:
                            print("   原始数据示例:")
                            for i, item in enumerate(raw_data[:2]):
                                print(f"      {i+1}. {item}")
                        
                        entities = result_data.get('entities', [])
                        if entities:
                            print("   识别实体:")
                            for entity in entities[:3]:
                                print(f"      - {entity}")
                    else:
                        print("   ❌ 结果文件不存在")
                        
                        # 列出目录内容
                        if upload_dir.exists():
                            files_in_dir = list(upload_dir.iterdir())
                            print(f"   目录内容: {[f.name for f in files_in_dir]}")
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

def check_api_status():
    """检查API状态"""
    print("=== 检查API状态 ===")
    
    try:
        # 健康检查
        health_r = requests.get('http://localhost:8000/health', timeout=5)
        print(f"健康检查: {health_r.status_code} - {health_r.text}")
        
        # 文件列表
        files_r = requests.get('http://localhost:8000/kg/files', timeout=5)
        print(f"文件列表: {files_r.status_code}")
        
        if files_r.status_code == 200:
            files_data = files_r.json()
            print(f"文件数量: {len(files_data.get('files', []))}")
        
        return True
    except Exception as e:
        print(f"❌ API连接失败: {e}")
        return False

def check_dependencies():
    """检查依赖库"""
    print("=== 检查依赖库 ===")
    
    dependencies = ['pandas', 'openpyxl', 'docx', 'pdfplumber']
    
    for dep in dependencies:
        try:
            if dep == 'docx':
                import docx
                print(f"✅ python-docx: 可用")
            elif dep == 'pdfplumber':
                import pdfplumber
                print(f"✅ pdfplumber: 可用")
            elif dep == 'pandas':
                import pandas
                print(f"✅ pandas: 可用")
            elif dep == 'openpyxl':
                import openpyxl
                print(f"✅ openpyxl: 可用")
        except ImportError:
            print(f"❌ {dep}: 不可用")

def main():
    """主函数"""
    print("🔍 开始调试文档解析问题...")
    
    # 检查依赖
    check_dependencies()
    print()
    
    # 检查API状态
    if not check_api_status():
        return
    print()
    
    # 测试简单文本解析
    test_simple_text_parsing()

if __name__ == "__main__":
    main()
