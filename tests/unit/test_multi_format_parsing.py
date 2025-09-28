#!/usr/bin/env python3
"""
测试多格式文档解析功能
"""

import requests
import time
import json
import os
from pathlib import Path

def test_multi_format_parsing():
    """测试多格式文档解析功能"""
    print("=== 测试多格式文档解析功能 ===")
    
    # 测试文件列表
    test_files = [
        {
            'name': 'Excel测试',
            'file': 'test_files/水利问题调查表.xlsx',
            'type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        }
    ]
    
    # 检查是否有其他测试文件
    test_dir = Path('test_files')
    if test_dir.exists():
        for file_path in test_dir.iterdir():
            if file_path.is_file():
                ext = file_path.suffix.lower()
                if ext in ['.pdf', '.docx', '.doc', '.pptx', '.ppt', '.txt', '.csv', '.md', '.rtf']:
                    test_files.append({
                        'name': f'{ext[1:].upper()}测试',
                        'file': str(file_path),
                        'type': get_mime_type(ext)
                    })
    
    success_count = 0
    total_count = len(test_files)
    
    for i, test_file in enumerate(test_files, 1):
        print(f"\n{'='*60}")
        print(f"测试 {i}/{total_count}: {test_file['name']}")
        print(f"文件: {test_file['file']}")
        
        if test_single_file(test_file):
            success_count += 1
            print(f"✅ {test_file['name']} 解析成功")
        else:
            print(f"❌ {test_file['name']} 解析失败")
    
    print(f"\n{'='*60}")
    print(f"🎊 多格式解析测试完成！")
    print(f"📊 成功率: {success_count}/{total_count} ({success_count/total_count*100:.1f}%)")
    
    return success_count == total_count

def get_mime_type(ext):
    """获取MIME类型"""
    mime_types = {
        '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        '.xls': 'application/vnd.ms-excel',
        '.pdf': 'application/pdf',
        '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        '.doc': 'application/msword',
        '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
        '.ppt': 'application/vnd.ms-powerpoint',
        '.txt': 'text/plain',
        '.csv': 'text/csv',
        '.md': 'text/markdown',
        '.rtf': 'application/rtf'
    }
    return mime_types.get(ext, 'application/octet-stream')

def test_single_file(test_file):
    """测试单个文件"""
    try:
        # 检查文件是否存在
        if not os.path.exists(test_file['file']):
            print(f"⚠ 文件不存在: {test_file['file']}")
            return False
        
        # 1. 上传文件
        print(f"\n📁 步骤1: 上传文件")
        upload_id = upload_file(test_file)
        if not upload_id:
            return False
        
        # 2. 触发解析
        print(f"\n🔧 步骤2: 触发解析")
        if not trigger_parse(upload_id):
            return False
        
        # 3. 监控解析过程
        print(f"\n⏳ 步骤3: 监控解析过程")
        if not monitor_parsing(upload_id):
            return False
        
        # 4. 验证解析结果
        print(f"\n✅ 步骤4: 验证解析结果")
        if not verify_parsing_results(upload_id, test_file):
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ 测试异常: {e}")
        return False

def upload_file(test_file):
    """上传文件"""
    try:
        with open(test_file['file'], 'rb') as f:
            files = {
                'file': (os.path.basename(test_file['file']), f, test_file['type'])
            }
            
            response = requests.post("http://127.0.0.1:8000/kg/upload", files=files, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    upload_id = result.get('upload_id')
                    print(f"✅ 文件上传成功 (ID: {upload_id})")
                    return upload_id
                else:
                    print(f"❌ 上传失败: {result.get('message')}")
                    return None
            else:
                print(f"❌ 上传请求失败: {response.status_code}")
                return None
                
    except Exception as e:
        print(f"❌ 上传异常: {e}")
        return None

def trigger_parse(upload_id):
    """触发解析"""
    try:
        parse_response = requests.post(f"http://127.0.0.1:8000/kg/files/{upload_id}/parse", timeout=30)
        
        if parse_response.status_code == 200:
            parse_result = parse_response.json()
            if parse_result.get('success'):
                print("✅ 解析触发成功")
                return True
            else:
                print(f"❌ 解析触发失败: {parse_result.get('message')}")
                return False
        else:
            print(f"❌ 解析请求失败: {parse_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 解析触发异常: {e}")
        return False

def monitor_parsing(upload_id):
    """监控解析过程"""
    max_attempts = 20
    
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
                        return True
                    elif file_status == 'failed':
                        error = status_data.get('error', '未知错误')
                        print(f"❌ 解析失败: {error}")
                        return False
                    elif file_status in ['parsing', 'uploaded']:
                        time.sleep(3)
                        continue
                    else:
                        print(f"⚠ 意外状态: {file_status}")
                        time.sleep(3)
                        continue
                else:
                    print(f"❌ 状态查询失败: {status_result.get('message')}")
                    return False
            else:
                print(f"❌ 状态查询请求失败: {status_response.status_code}")
                return False
                
        except Exception as e:
            print(f"⚠ 状态查询异常: {e}")
            time.sleep(3)
            continue
    
    print("❌ 解析超时")
    return False

def verify_parsing_results(upload_id, test_file):
    """验证解析结果"""
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
                
                print(f"📊 解析结果:")
                print(f"   原始记录: {len(raw_data)} 条")
                print(f"   抽取实体: {len(entities)} 个")
                print(f"   抽取关系: {len(relations)} 个")
                print(f"   元数据: {len(metadata)} 项")
                
                if metadata:
                    print(f"   元数据详情: {metadata}")
                
                if raw_data:
                    first_record = raw_data[0]
                    print(f"\n📋 第一条记录的字段 ({len(first_record)} 个):")
                    
                    # 显示前10个字段
                    for i, (key, value) in enumerate(list(first_record.items())[:10], 1):
                        print(f"   {i:2d}. {key}: {str(value)[:80]}")
                    
                    if len(first_record) > 10:
                        print(f"   ... 还有 {len(first_record) - 10} 个字段")
                    
                    # 验证row_number是否在前面
                    keys_list = list(first_record.keys())
                    if '_row_number' in keys_list:
                        row_number_index = keys_list.index('_row_number')
                        if row_number_index == 0:
                            print("   ✅ _row_number 字段位于第一位")
                        else:
                            print(f"   ⚠ _row_number 字段位于第 {row_number_index + 1} 位")
                    
                    # 验证数据质量
                    non_empty_fields = sum(1 for v in first_record.values() if v and str(v).strip())
                    data_quality = non_empty_fields / len(first_record) * 100
                    print(f"   数据完整性: {data_quality:.1f}%")
                    
                    if len(raw_data) > 0 and len(entities) > 0:
                        print("✅ 解析结果验证通过")
                        return True
                    else:
                        print("⚠ 解析结果为空")
                        return False
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

def create_test_files():
    """创建测试文件"""
    print("\n=== 创建测试文件 ===")
    
    test_dir = Path('test_files')
    test_dir.mkdir(exist_ok=True)
    
    # 创建测试文本文件
    txt_file = test_dir / 'test_document.txt'
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write("""这是一个测试文档

第一段内容：
这里包含了一些测试数据，用于验证文本解析功能。

第二段内容：
包含了问题编号：TEST-001
问题描述：文本解析测试
解决方案：验证解析器功能

第三段内容：
更多的测试数据，确保解析器能够正确处理中文内容。
""")
    
    # 创建测试CSV文件
    csv_file = test_dir / 'test_data.csv'
    with open(csv_file, 'w', encoding='utf-8') as f:
        f.write("""编号,名称,类型,描述
001,测试项目1,类型A,这是第一个测试项目
002,测试项目2,类型B,这是第二个测试项目
003,测试项目3,类型C,这是第三个测试项目
""")
    
    print(f"✅ 创建测试文件:")
    print(f"   - {txt_file}")
    print(f"   - {csv_file}")

if __name__ == "__main__":
    print("🔍 多格式文档解析功能测试")
    print("="*60)
    
    # 1. 创建测试文件
    create_test_files()
    
    # 2. 测试多格式解析
    success = test_multi_format_parsing()
    
    print("\n" + "="*60)
    if success:
        print("🎉 多格式文档解析功能测试成功！")
        print("现在系统支持Excel、PDF、Word、PowerPoint、文本等多种格式！")
    else:
        print("❌ 多格式文档解析功能测试失败！")
    
    print("\n📋 测试完成！")
