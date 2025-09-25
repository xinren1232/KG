#!/usr/bin/env python3
"""
测试清洁解析功能 - 避免重复字段
"""

import requests
import time
import json

def test_clean_parsing():
    """测试清洁解析功能"""
    print("=== 测试清洁解析功能 ===")
    
    # 1. 上传测试文件
    print("\n📁 步骤1: 上传测试文件")
    upload_id = upload_test_file()
    if not upload_id:
        return False
    
    # 2. 手动触发解析
    print(f"\n🔧 步骤2: 手动触发解析")
    if not trigger_parse(upload_id):
        return False
    
    # 3. 监控解析过程
    print(f"\n⏳ 步骤3: 监控解析过程")
    if not monitor_parsing(upload_id):
        return False
    
    # 4. 验证清洁解析结果
    print(f"\n✅ 步骤4: 验证清洁解析结果")
    if not verify_clean_results(upload_id):
        return False
    
    print(f"\n🎊 清洁解析测试成功！")
    return True

def upload_test_file():
    """上传测试文件"""
    test_file = "test_files/水利问题调查表.xlsx"
    
    try:
        with open(test_file, 'rb') as f:
            files = {
                'file': ('清洁解析测试.xlsx', f, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
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
    max_attempts = 15
    
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
                        time.sleep(2)
                        continue
                    else:
                        print(f"⚠ 意外状态: {file_status}")
                        time.sleep(2)
                        continue
                else:
                    print(f"❌ 状态查询失败: {status_result.get('message')}")
                    return False
            else:
                print(f"❌ 状态查询请求失败: {status_response.status_code}")
                return False
                
        except Exception as e:
            print(f"⚠ 状态查询异常: {e}")
            time.sleep(2)
            continue
    
    print("❌ 解析超时")
    return False

def verify_clean_results(upload_id):
    """验证清洁解析结果"""
    try:
        preview_response = requests.get(f"http://127.0.0.1:8000/kg/files/{upload_id}/preview", timeout=15)
        
        if preview_response.status_code == 200:
            preview_result = preview_response.json()
            if preview_result.get('success'):
                preview_data = preview_result.get('data', {})
                
                raw_data = preview_data.get('raw_data', [])
                entities = preview_data.get('entities', [])
                relations = preview_data.get('relations', [])
                
                print(f"📊 清洁解析结果:")
                print(f"   原始记录: {len(raw_data)} 条")
                print(f"   抽取实体: {len(entities)} 个")
                print(f"   抽取关系: {len(relations)} 个")
                
                if raw_data:
                    first_record = raw_data[0]
                    print(f"\n📋 第一条记录的字段 ({len(first_record)} 个):")
                    
                    # 分析字段类型
                    original_fields = []
                    mapped_fields = []
                    duplicate_fields = []
                    
                    for key, value in first_record.items():
                        print(f"   {key}: {str(value)[:60]}")
                        
                        # 检查是否是原始Excel列名（中文）
                        if any(ord(c) > 127 for c in key):  # 包含中文字符
                            original_fields.append(key)
                        elif key in ['anomaly_key', 'title', 'date', 'severity', 'factory', 'product', 'component', 'root_cause', 'countermeasure', 'supplier', 'status', 'row_number']:
                            mapped_fields.append(key)
                        else:
                            duplicate_fields.append(key)
                    
                    print(f"\n🔍 字段分析:")
                    print(f"   原始字段 (中文): {len(original_fields)} 个")
                    print(f"   映射字段 (英文): {len(mapped_fields)} 个")
                    print(f"   其他字段: {len(duplicate_fields)} 个")
                    
                    if original_fields:
                        print(f"   原始字段: {original_fields}")
                    if mapped_fields:
                        print(f"   映射字段: {mapped_fields}")
                    if duplicate_fields:
                        print(f"   其他字段: {duplicate_fields}")
                    
                    # 检查重复内容
                    duplicate_content = []
                    for orig_field in original_fields:
                        orig_value = first_record.get(orig_field)
                        for mapped_field in mapped_fields:
                            mapped_value = first_record.get(mapped_field)
                            if orig_value == mapped_value and orig_value is not None:
                                duplicate_content.append((orig_field, mapped_field, orig_value))
                    
                    print(f"\n⚠ 重复内容检查:")
                    if duplicate_content:
                        print(f"   发现 {len(duplicate_content)} 个重复内容:")
                        for orig, mapped, value in duplicate_content:
                            print(f"     {orig} = {mapped} = {str(value)[:30]}")
                        print("   ❌ 存在重复字段问题")
                        return False
                    else:
                        print("   ✅ 无重复内容")
                    
                    # 验证原始Excel列是否完整
                    expected_original_fields = [
                        '问题编号', '不良现象', '发生日期', '严重度', '工厂', 
                        '机型', '部件', '原因分析', '改善对策', '供应商', '状态'
                    ]
                    
                    found_original = [f for f in expected_original_fields if f in original_fields]
                    coverage = len(found_original) / len(expected_original_fields) * 100
                    
                    print(f"\n📊 原始字段覆盖:")
                    print(f"   期望: {len(expected_original_fields)} 个")
                    print(f"   找到: {len(found_original)} 个")
                    print(f"   覆盖率: {coverage:.1f}%")
                    
                    if coverage >= 90:
                        print("   ✅ 原始字段覆盖良好")
                        return True
                    else:
                        print("   ❌ 原始字段覆盖不足")
                        missing = set(expected_original_fields) - set(found_original)
                        print(f"   缺失: {missing}")
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

def compare_with_original():
    """与原始Excel数据对比"""
    print("\n=== 与原始Excel数据对比 ===")
    
    try:
        import pandas as pd
        
        # 读取原始Excel
        original_df = pd.read_excel("test_files/水利问题调查表.xlsx")
        
        print(f"📊 原始Excel数据:")
        print(f"   行数: {len(original_df)}")
        print(f"   列数: {len(original_df.columns)}")
        print(f"   列名: {list(original_df.columns)}")
        
        return True
        
    except Exception as e:
        print(f"❌ 读取原始Excel失败: {e}")
        return False

if __name__ == "__main__":
    print("🧹 清洁解析功能测试")
    print("="*60)
    
    # 1. 对比原始数据
    compare_with_original()
    
    # 2. 测试清洁解析
    success = test_clean_parsing()
    
    print("\n" + "="*60)
    if success:
        print("🎉 清洁解析功能测试成功！")
        print("解析结果应该只包含原始Excel列名，无重复字段！")
    else:
        print("❌ 清洁解析功能测试失败！")
    
    print("\n📋 测试完成！")
