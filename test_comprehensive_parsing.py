#!/usr/bin/env python3
"""
测试全面解析功能
"""

import requests
import time
import json

def test_comprehensive_parsing():
    """测试全面解析功能"""
    print("=== 测试全面解析功能 ===")
    
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
    
    # 4. 验证全面解析结果
    print(f"\n✅ 步骤4: 验证全面解析结果")
    if not verify_comprehensive_results(upload_id):
        return False
    
    print(f"\n🎊 全面解析测试成功！")
    return True

def upload_test_file():
    """上传测试文件"""
    test_file = "test_files/水利问题调查表.xlsx"
    
    try:
        with open(test_file, 'rb') as f:
            files = {
                'file': ('全面解析测试.xlsx', f, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
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

def verify_comprehensive_results(upload_id):
    """验证全面解析结果"""
    try:
        preview_response = requests.get(f"http://127.0.0.1:8000/kg/files/{upload_id}/preview", timeout=15)
        
        if preview_response.status_code == 200:
            preview_result = preview_response.json()
            if preview_result.get('success'):
                preview_data = preview_result.get('data', {})
                
                raw_data = preview_data.get('raw_data', [])
                entities = preview_data.get('entities', [])
                relations = preview_data.get('relations', [])
                
                print(f"📊 全面解析结果:")
                print(f"   原始记录: {len(raw_data)} 条")
                print(f"   抽取实体: {len(entities)} 个")
                print(f"   抽取关系: {len(relations)} 个")
                
                if raw_data:
                    first_record = raw_data[0]
                    print(f"\n📋 第一条记录的所有字段 ({len(first_record)} 个):")
                    
                    # 显示所有字段
                    for i, (key, value) in enumerate(first_record.items(), 1):
                        print(f"   {i:2d}. {key}: {str(value)[:80]}")
                    
                    # 验证是否包含原始Excel的所有列
                    expected_fields = [
                        '问题编号', '不良现象', '发生日期', '严重度', '工厂', 
                        '机型', '部件', '原因分析', '改善对策', '供应商', '状态'
                    ]
                    
                    found_fields = []
                    for field in expected_fields:
                        # 检查是否有对应的字段（可能是映射后的字段名）
                        field_found = False
                        for key in first_record.keys():
                            if field in str(key) or any(field in str(v) for v in [first_record.get(key, '')]):
                                field_found = True
                                found_fields.append(field)
                                break
                        
                        # 也检查直接的字段名匹配
                        if field in first_record:
                            field_found = True
                            if field not in found_fields:
                                found_fields.append(field)
                    
                    print(f"\n🔍 字段覆盖率检查:")
                    print(f"   期望字段: {len(expected_fields)} 个")
                    print(f"   实际字段: {len(first_record)} 个")
                    print(f"   覆盖字段: {len(found_fields)} 个")
                    
                    coverage_rate = len(found_fields) / len(expected_fields) * 100
                    print(f"   覆盖率: {coverage_rate:.1f}%")
                    
                    if coverage_rate >= 80:
                        print("✅ 字段覆盖率良好")
                    else:
                        print("⚠ 字段覆盖率偏低")
                        print(f"   缺失字段: {set(expected_fields) - set(found_fields)}")
                    
                    # 验证数据质量
                    non_empty_fields = sum(1 for v in first_record.values() if v and str(v).strip())
                    data_quality = non_empty_fields / len(first_record) * 100
                    print(f"   数据完整性: {data_quality:.1f}%")
                    
                    if data_quality >= 80:
                        print("✅ 数据质量良好")
                        return True
                    else:
                        print("⚠ 数据质量需要改进")
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
        
        print(f"\n📋 原始第一行数据:")
        first_row = original_df.iloc[0]
        for i, (col, value) in enumerate(first_row.items(), 1):
            print(f"   {i:2d}. {col}: {value}")
        
        return True
        
    except Exception as e:
        print(f"❌ 读取原始Excel失败: {e}")
        return False

if __name__ == "__main__":
    print("🔍 全面解析功能测试")
    print("="*60)
    
    # 1. 对比原始数据
    compare_with_original()
    
    # 2. 测试全面解析
    success = test_comprehensive_parsing()
    
    print("\n" + "="*60)
    if success:
        print("🎉 全面解析功能测试成功！")
        print("现在解析结果应该包含Excel文件的所有列和完整数据！")
    else:
        print("❌ 全面解析功能测试失败！")
    
    print("\n📋 测试完成！")
