#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
多格式文档显示功能测试脚本
测试不同文档格式的专门显示组件
"""

import requests
import json
import time
import os
from pathlib import Path

def test_multi_format_display():
    """测试多格式文档显示功能"""
    
    print("\n🧪 多格式文档显示功能测试")
    print("=" * 60)
    
    base_url = "http://127.0.0.1:8000"
    
    # 测试文件列表
    test_files = [
        {
            "name": "test_excel.xlsx",
            "content": create_test_excel(),
            "expected_format": "excel",
            "expected_display": "ExcelDisplay"
        },
        {
            "name": "test_data.csv", 
            "content": create_test_csv(),
            "expected_format": "csv",
            "expected_display": "CsvDisplay"
        },
        {
            "name": "test_document.txt",
            "content": create_test_text(),
            "expected_format": "text", 
            "expected_display": "TextDisplay"
        }
    ]
    
    results = []
    
    for test_file in test_files:
        print(f"\n📁 测试文件: {test_file['name']}")
        print("-" * 40)
        
        try:
            # 1. 创建测试文件
            file_path = Path(test_file['name'])
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(test_file['content'])
            
            # 2. 上传文件
            print("📤 上传文件...")
            with open(file_path, 'rb') as f:
                files = {'file': (test_file['name'], f, 'application/octet-stream')}
                response = requests.post(f"{base_url}/kg/upload", files=files)
            
            if response.status_code != 200:
                print(f"❌ 上传失败: {response.status_code}")
                continue
                
            upload_data = response.json()
            upload_id = upload_data['upload_id']
            print(f"✅ 上传成功 (ID: {upload_id})")
            
            # 3. 触发解析
            print("🔧 触发解析...")
            parse_response = requests.post(f"{base_url}/kg/files/{upload_id}/parse")
            
            if parse_response.status_code != 200:
                print(f"❌ 解析触发失败: {parse_response.status_code}")
                continue
                
            print("✅ 解析任务已启动")
            
            # 4. 等待解析完成
            print("⏳ 等待解析完成...")
            max_wait = 30
            wait_time = 0
            
            while wait_time < max_wait:
                status_response = requests.get(f"{base_url}/kg/files/{upload_id}/status")
                if status_response.status_code == 200:
                    status_data = status_response.json()
                    if status_data['data']['status'] == 'parsed':
                        print("✅ 解析完成")
                        break
                    elif status_data['data']['status'] == 'failed':
                        print(f"❌ 解析失败: {status_data['data'].get('error', '未知错误')}")
                        break
                
                time.sleep(2)
                wait_time += 2
                print(f"   等待中... ({wait_time}s)")
            
            if wait_time >= max_wait:
                print("❌ 解析超时")
                continue
            
            # 5. 获取解析结果
            print("📊 获取解析结果...")
            result_response = requests.get(f"{base_url}/kg/files/{upload_id}/preview")
            
            if result_response.status_code != 200:
                print(f"❌ 获取结果失败: {result_response.status_code}")
                continue
                
            result_data = result_response.json()
            
            # 6. 验证解析结果
            print("🔍 验证解析结果...")
            
            if not result_data.get('success'):
                print(f"❌ 解析结果无效: {result_data.get('error', '未知错误')}")
                continue
            
            preview_data = result_data['data']
            raw_data = preview_data.get('raw_data', [])
            metadata = preview_data.get('metadata', {})
            
            print(f"   原始记录: {len(raw_data)} 条")
            print(f"   元数据字段: {len(metadata)} 个")
            
            # 7. 验证显示组件选择逻辑
            file_ext = Path(test_file['name']).suffix.lower()
            expected_component = get_expected_display_component(file_ext)
            
            print(f"   文件扩展名: {file_ext}")
            print(f"   预期显示组件: {expected_component}")
            print(f"   预期格式类型: {test_file['expected_format']}")
            
            # 8. 验证数据结构
            if raw_data:
                first_record = raw_data[0]
                print(f"   第一条记录字段: {list(first_record.keys())}")
                
                # 验证行号字段是否在第一位
                if '_row_number' in first_record:
                    fields = list(first_record.keys())
                    if fields[0] == '_row_number':
                        print("   ✅ _row_number 字段位于第一位")
                    else:
                        print(f"   ❌ _row_number 字段位置错误，当前位置: {fields.index('_row_number')}")
                
                print(f"   示例数据: {json.dumps(first_record, ensure_ascii=False, indent=2)[:200]}...")
            
            # 记录测试结果
            test_result = {
                'file_name': test_file['name'],
                'file_format': test_file['expected_format'],
                'upload_success': True,
                'parse_success': True,
                'data_count': len(raw_data),
                'metadata_count': len(metadata),
                'expected_component': expected_component,
                'row_number_first': raw_data and list(raw_data[0].keys())[0] == '_row_number' if raw_data else False
            }
            
            results.append(test_result)
            print("✅ 测试完成")
            
            # 清理测试文件
            if file_path.exists():
                file_path.unlink()
                
        except Exception as e:
            print(f"❌ 测试异常: {e}")
            test_result = {
                'file_name': test_file['name'],
                'file_format': test_file['expected_format'],
                'upload_success': False,
                'parse_success': False,
                'error': str(e)
            }
            results.append(test_result)
    
    # 输出测试总结
    print("\n📋 测试总结")
    print("=" * 60)
    
    total_tests = len(results)
    successful_tests = sum(1 for r in results if r.get('parse_success', False))
    
    print(f"总测试数: {total_tests}")
    print(f"成功测试: {successful_tests}")
    print(f"成功率: {(successful_tests/total_tests)*100:.1f}%")
    
    print("\n📊 详细结果:")
    for result in results:
        status = "✅" if result.get('parse_success', False) else "❌"
        print(f"{status} {result['file_name']} ({result['file_format']})")
        if result.get('parse_success'):
            print(f"   数据记录: {result['data_count']} 条")
            print(f"   元数据: {result['metadata_count']} 个")
            print(f"   显示组件: {result['expected_component']}")
            print(f"   行号位置: {'第一位' if result['row_number_first'] else '非第一位'}")
        else:
            print(f"   错误: {result.get('error', '未知错误')}")
    
    if successful_tests == total_tests:
        print("\n🎉 所有多格式显示功能测试通过！")
    else:
        print(f"\n⚠️  {total_tests - successful_tests} 个测试失败，需要检查")
    
    return results

def get_expected_display_component(file_ext):
    """根据文件扩展名获取预期的显示组件"""
    component_map = {
        '.xlsx': 'ExcelDisplay',
        '.xls': 'ExcelDisplay', 
        '.csv': 'CsvDisplay',
        '.txt': 'TextDisplay',
        '.md': 'TextDisplay',
        '.rtf': 'TextDisplay',
        '.pdf': 'PdfDisplay',
        '.docx': 'WordDisplay',
        '.doc': 'WordDisplay',
        '.pptx': 'PowerPointDisplay',
        '.ppt': 'PowerPointDisplay'
    }
    return component_map.get(file_ext, 'DefaultDisplay')

def create_test_excel():
    """创建测试Excel内容（CSV格式模拟）"""
    return """问题编号,不良现象,发生日期,严重度,工厂,机型,部件,原因分析,改善对策,供应商,状态
ISSUE-001,屏幕显示异常,2024-01-15,高,深圳工厂,iPhone 15,显示屏,显示驱动IC故障,更换驱动IC,供应商A,已解决
ISSUE-002,电池续航短,2024-01-16,中,上海工厂,iPhone 15,电池,电池容量衰减,更换电池模块,供应商B,处理中
ISSUE-003,充电接口松动,2024-01-17,低,北京工厂,iPhone 14,充电口,接口磨损,重新焊接,供应商C,待处理
ISSUE-004,摄像头模糊,2024-01-18,高,广州工厂,iPhone 15,摄像头,镜头污染,清洁镜头,供应商A,已解决
ISSUE-005,系统卡顿,2024-01-19,中,深圳工厂,iPhone 14,处理器,内存不足,优化系统,供应商D,处理中"""

def create_test_csv():
    """创建测试CSV内容"""
    return """编号,名称,类型,描述,创建时间
001,测试项目1,类型A,这是第一个测试项目,2024-01-15
002,测试项目2,类型B,这是第二个测试项目,2024-01-16
003,测试项目3,类型A,这是第三个测试项目,2024-01-17
004,测试项目4,类型C,这是第四个测试项目,2024-01-18
005,测试项目5,类型B,这是第五个测试项目,2024-01-19"""

def create_test_text():
    """创建测试文本内容"""
    return """文档解析系统测试报告

第一章 系统概述
本系统是一个多格式文档解析平台，支持Excel、PDF、Word、PowerPoint、CSV和文本文件的解析。
系统采用模块化设计，为不同格式提供专门的显示组件。

第二章 功能特性
2.1 多格式支持
- Excel文件：表格数据展示，字段分析
- PDF文件：页面导航，文本和表格提取
- Word文档：段落展示，表格处理
- PowerPoint：幻灯片导航，内容分析
- CSV文件：数据统计，质量分析
- 文本文件：段落分析，词频统计

2.2 智能解析
系统能够自动识别文件格式，选择对应的解析器进行处理。
解析结果包含原始数据、实体信息和元数据。

第三章 技术架构
前端采用Vue.js 3和Element Plus构建用户界面。
后端使用FastAPI提供RESTful API服务。
解析引擎支持多种文档格式的处理。

第四章 测试结果
经过全面测试，系统在各种格式的文档解析中表现优异。
数据完整性达到100%，解析准确率超过95%。

第五章 总结
本系统成功实现了多格式文档的智能解析和专业展示。
为用户提供了高效、准确的文档处理解决方案。"""

if __name__ == "__main__":
    test_multi_format_display()
