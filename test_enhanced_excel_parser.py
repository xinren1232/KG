#!/usr/bin/env python3
"""
测试增强的Excel解析器
"""

import sys
import os
sys.path.append('.')

from api.parsers.enhanced_excel_parser import EnhancedExcelParser, parse_excel
from pathlib import Path
import json

def test_enhanced_parser():
    """测试增强解析器"""
    print("=== 测试增强Excel解析器 ===")
    
    # 检查测试文件
    test_file = Path("test_files/水利问题调查表.xlsx")
    if not test_file.exists():
        print(f"❌ 测试文件不存在: {test_file}")
        return False
    
    print(f"📁 测试文件: {test_file}")
    
    try:
        # 创建解析器实例
        parser = EnhancedExcelParser()
        
        # 测试解析
        print("\n1️⃣ 开始解析...")
        items = parser.parse_excel_robust(test_file)
        
        print(f"✅ 解析成功，共 {len(items)} 条记录")
        
        # 分析解析结果
        print("\n2️⃣ 解析结果分析:")
        if items:
            first_item = items[0]
            print(f"📋 第一条记录的字段:")
            for key, value in first_item.items():
                print(f"  {key:15s}: {value}")
            
            # 检查关键字段
            key_fields = ["anomaly_key", "title", "component", "symptom", "root_cause", "countermeasure"]
            print(f"\n🔍 关键字段检查:")
            for field in key_fields:
                value = first_item.get(field)
                if value and str(value).strip() and not str(value).startswith('ANOM-'):
                    print(f"  ✅ {field}: {value}")
                else:
                    print(f"  ❌ {field}: {value} (可能有问题)")
            
            # 数据质量统计
            print(f"\n📊 数据质量统计:")
            total_records = len(items)
            
            for field in key_fields:
                valid_count = sum(1 for item in items if item.get(field) and str(item[field]).strip())
                percentage = (valid_count / total_records) * 100
                print(f"  {field:15s}: {valid_count:2d}/{total_records:2d} ({percentage:5.1f}%)")
            
            # 检查是否有异常键值
            anomaly_keys = [item.get("anomaly_key", "") for item in items]
            problematic_keys = [key for key in anomaly_keys if key.startswith('ANOM-') and len(key) > 10]
            
            if problematic_keys:
                print(f"\n⚠ 发现 {len(problematic_keys)} 个异常键值:")
                for key in problematic_keys[:3]:  # 只显示前3个
                    print(f"    {key}")
            else:
                print(f"\n✅ 没有发现异常键值，所有问题编号都是有意义的")
        
        return True
        
    except Exception as e:
        print(f"❌ 解析失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_direct_parsing():
    """直接测试解析函数"""
    print("\n=== 直接测试解析函数 ===")
    
    test_file = Path("test_files/水利问题调查表.xlsx")
    if not test_file.exists():
        print(f"❌ 测试文件不存在: {test_file}")
        return False
    
    try:
        # 使用兼容性函数
        items = parse_excel(test_file)
        
        print(f"✅ 直接解析成功，共 {len(items)} 条记录")
        
        if items:
            print(f"\n📋 示例记录:")
            example = items[0]
            for key, value in example.items():
                if value and str(value).strip():
                    print(f"  {key}: {value}")
        
        return True
        
    except Exception as e:
        print(f"❌ 直接解析失败: {e}")
        return False

def test_with_api():
    """通过API测试解析效果"""
    print("\n=== 通过API测试解析效果 ===")
    
    import requests
    import time
    
    # 检查API服务
    try:
        response = requests.get("http://127.0.0.1:8000/kg/stats", timeout=5)
        if response.status_code != 200:
            print("❌ API服务不可用")
            return False
    except:
        print("❌ API服务连接失败")
        return False
    
    # 上传测试文件
    test_file = "test_files/水利问题调查表.xlsx"
    try:
        with open(test_file, 'rb') as f:
            files = {'file': ('水利问题调查表.xlsx', f, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
            response = requests.post("http://127.0.0.1:8000/kg/upload", files=files, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    upload_id = result.get('upload_id')
                    print(f"✅ 文件上传成功 (ID: {upload_id})")
                else:
                    print(f"❌ 文件上传失败: {result.get('message')}")
                    return False
            else:
                print(f"❌ 文件上传失败 (状态码: {response.status_code})")
                return False
    except Exception as e:
        print(f"❌ 文件上传异常: {e}")
        return False
    
    # 等待解析完成
    print("⏳ 等待解析完成...")
    for _ in range(15):  # 最多等待30秒
        try:
            status_response = requests.get(f"http://127.0.0.1:8000/kg/files/{upload_id}/status", timeout=10)
            if status_response.status_code == 200:
                status_result = status_response.json()
                if status_result.get('success'):
                    status = status_result.get('data', {}).get('status')
                    
                    if status == 'parsed':
                        print("✅ 解析完成")
                        break
                    elif status == 'failed':
                        error = status_result.get('data', {}).get('error', '未知错误')
                        print(f"❌ 解析失败: {error}")
                        return False
        except:
            pass
        
        time.sleep(2)
    else:
        print("❌ 解析超时")
        return False
    
    # 获取解析结果
    try:
        preview_response = requests.get(f"http://127.0.0.1:8000/kg/files/{upload_id}/preview", timeout=10)
        if preview_response.status_code == 200:
            preview_result = preview_response.json()
            if preview_result.get('success'):
                data = preview_result.get('data', {})
                
                # 检查解析结果
                raw_data = data.get('raw_data', [])
                print(f"✅ 获取解析结果成功，共 {len(raw_data)} 条记录")
                
                if raw_data:
                    first_record = raw_data[0]
                    anomaly_key = first_record.get('anomaly_key', '')
                    
                    print(f"\n📋 第一条记录的问题编号: {anomaly_key}")
                    
                    if anomaly_key.startswith('ANOM-') and len(anomaly_key) > 10:
                        print("❌ 仍然是异常键值，解析器可能没有生效")
                        return False
                    else:
                        print("✅ 问题编号正常，解析器生效")
                        
                        # 显示更多字段
                        print(f"\n📋 完整记录示例:")
                        for key, value in first_record.items():
                            if value and str(value).strip():
                                print(f"  {key}: {value}")
                        
                        return True
                
        print("❌ 无法获取解析结果")
        return False
        
    except Exception as e:
        print(f"❌ 获取解析结果异常: {e}")
        return False

if __name__ == "__main__":
    print("🔧 增强Excel解析器测试")
    print("="*50)
    
    # 测试1: 直接测试解析器
    success1 = test_enhanced_parser()
    
    # 测试2: 测试兼容性函数
    success2 = test_direct_parsing()
    
    # 测试3: 通过API测试
    success3 = test_with_api()
    
    print("\n" + "="*50)
    print("📊 测试结果总结:")
    print(f"  增强解析器: {'✅ 通过' if success1 else '❌ 失败'}")
    print(f"  兼容性函数: {'✅ 通过' if success2 else '❌ 失败'}")
    print(f"  API集成测试: {'✅ 通过' if success3 else '❌ 失败'}")
    
    if all([success1, success2, success3]):
        print("\n🎉 所有测试通过！增强解析器工作正常！")
    else:
        print("\n❌ 部分测试失败，需要进一步调试。")
