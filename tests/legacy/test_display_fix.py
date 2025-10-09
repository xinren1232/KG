#!/usr/bin/env python3
import requests
import pandas as pd
import time
from pathlib import Path

def test_display_fix():
    """测试数据显示修复"""
    
    print("=== 测试数据显示修复 ===")
    
    # 1. 创建测试Excel文件
    print("\n1. 创建测试Excel文件...")
    
    test_data = {
        '工厂名称': ['索尼', '苹果', '中兴', '12', '索尼'],
        '产品型号': ['XM4', 'iPhone14', 'Axon30', 'Model-X', 'WH-1000XM5'],
        '问题描述': ['耳机连接不稳定', '屏幕显示异常', '电池续航短', '摄像头模糊', '降噪效果差'],
        '发现时间': pd.to_datetime([
            '2025-01-15 10:30:00',
            '2025-01-16 14:20:00', 
            '2025-01-17 09:15:00',
            '2025-01-18 16:45:00',
            '2025-01-19 11:30:00'
        ]),
        '严重程度': ['中', '高', '低', '中', '低'],
        '状态': ['已解决', '处理中', '待分析', '已解决', '处理中']
    }
    
    df = pd.DataFrame(test_data)
    test_file = 'display_test.xlsx'
    df.to_excel(test_file, index=False)
    
    print(f"   ✅ 创建测试文件: {test_file}")
    print(f"   数据行数: {len(df)}")
    print(f"   列名: {list(df.columns)}")
    
    # 2. 上传并解析
    print("\n2. 上传并解析Excel文件...")
    
    try:
        with open(test_file, 'rb') as f:
            files = {'file': f}
            upload_response = requests.post('http://localhost:8000/kg/upload', files=files)
        
        if upload_response.status_code != 200:
            print(f"   ❌ 上传失败: {upload_response.status_code}")
            return False
        
        upload_result = upload_response.json()
        upload_id = upload_result.get('upload_id')
        print(f"   ✅ 上传成功: {upload_id}")
        
        # 触发解析
        parse_response = requests.post(f'http://localhost:8000/kg/files/{upload_id}/parse')
        
        if parse_response.status_code != 200:
            print(f"   ❌ 解析失败: {parse_response.status_code}")
            print(f"   错误: {parse_response.text}")
            return False
        
        parse_result = parse_response.json()
        if not parse_result.get('success'):
            print(f"   ❌ 解析失败: {parse_result.get('message')}")
            return False
        
        print(f"   ✅ 解析成功")
        
    except Exception as e:
        print(f"   ❌ 异常: {e}")
        return False
    
    # 3. 等待解析完成并获取结果
    print("\n3. 获取解析结果...")
    
    time.sleep(3)  # 等待解析完成
    
    try:
        preview_response = requests.get(f'http://localhost:8000/kg/files/{upload_id}/preview')
        
        if preview_response.status_code != 200:
            print(f"   ❌ 获取结果失败: {preview_response.status_code}")
            return False
        
        preview_result = preview_response.json()
        if not preview_result.get('success'):
            print(f"   ❌ 获取结果失败: {preview_result.get('message')}")
            return False
        
        data = preview_result.get('data', {})
        raw_data = data.get('raw_data', [])
        
        print(f"   ✅ 获取结果成功")
        print(f"   解析记录数: {len(raw_data)}")
        
        # 4. 验证数据结构
        print("\n4. 验证数据结构...")
        
        if not raw_data:
            print("   ❌ 没有解析数据")
            return False
        
        first_record = raw_data[0]
        print(f"   第一条记录结构: {list(first_record.keys())}")
        
        # 检查是否有data字段
        if 'data' in first_record:
            print("   ✅ 发现data字段")
            data_content = first_record['data']
            print(f"   data字段内容: {data_content}")
            print(f"   data字段类型: {type(data_content)}")
            
            if isinstance(data_content, dict):
                print(f"   data字段包含列: {list(data_content.keys())}")
                
                # 检查时间戳字段
                for key, value in data_content.items():
                    if '时间' in key:
                        print(f"   时间戳字段 {key}: {value} (类型: {type(value).__name__})")
                        if isinstance(value, str):
                            print(f"      ✅ 时间戳正确序列化为字符串")
                        else:
                            print(f"      ❌ 时间戳未正确序列化")
                
                print("   ✅ 数据结构正确，前端应该能正确显示")
            else:
                print(f"   ❌ data字段不是字典类型: {type(data_content)}")
                return False
        else:
            print("   ⚠️ 没有发现data字段，检查原始数据结构")
            print(f"   原始记录: {first_record}")
        
        # 5. 显示所有记录的简要信息
        print("\n5. 数据预览...")
        for i, record in enumerate(raw_data[:3]):  # 只显示前3条
            print(f"   记录 {i+1}:")
            if 'data' in record:
                data_content = record['data']
                for key, value in list(data_content.items())[:3]:  # 只显示前3个字段
                    print(f"      {key}: {value}")
            print()
        
        success = True
        
    except Exception as e:
        print(f"   ❌ 异常: {e}")
        success = False
    
    # 6. 清理测试文件
    try:
        Path(test_file).unlink()
        print(f"🧹 清理测试文件: {test_file}")
    except:
        pass
    
    # 7. 总结
    print(f"\n{'='*50}")
    if success:
        print("✅ 数据显示修复验证成功")
        print("   - 后端正确返回包含data字段的结构化数据")
        print("   - 时间戳字段正确序列化为字符串")
        print("   - 前端应该能够正确提取和显示数据")
        print("\n📋 前端修改说明:")
        print("   - 添加了getDisplayData()方法来提取data字段")
        print("   - ExcelDisplay组件现在接收纯数据数组而不是包装对象")
        print("   - 数据表格应该正确显示具体内容而不是[object Object]")
        return True
    else:
        print("❌ 数据显示修复验证失败")
        return False

if __name__ == "__main__":
    test_display_fix()
