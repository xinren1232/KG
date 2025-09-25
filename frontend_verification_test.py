#!/usr/bin/env python3
"""
前端验证测试 - 模拟前端操作流程
"""

import requests
import time
import json
from pathlib import Path

def simulate_frontend_workflow():
    """模拟前端完整工作流程"""
    print("=== 模拟前端完整工作流程 ===")
    
    # 1. 检查API状态
    print("1️⃣ 检查API状态...")
    try:
        response = requests.get("http://127.0.0.1:8000/kg/stats")
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ API正常，统计信息: {stats}")
        else:
            print(f"❌ API状态异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API连接失败: {e}")
        return False
    
    # 2. 上传文件（模拟前端上传）
    print("\n2️⃣ 模拟前端文件上传...")
    test_file = "test_files/水利问题调查表.xlsx"
    
    try:
        with open(test_file, 'rb') as f:
            files = {
                'file': ('水利问题调查表_前端测试.xlsx', f, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            }
            
            # 模拟前端的上传请求
            response = requests.post(
                "http://127.0.0.1:8000/kg/upload",
                files=files,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    upload_id = result.get('upload_id')
                    file_info = result.get('file_info', {})
                    print(f"✅ 上传成功")
                    print(f"   Upload ID: {upload_id}")
                    print(f"   文件信息: {file_info}")
                else:
                    print(f"❌ 上传失败: {result.get('message')}")
                    return False
            else:
                print(f"❌ 上传请求失败: {response.status_code}")
                print(f"   响应内容: {response.text}")
                return False
                
    except Exception as e:
        print(f"❌ 上传异常: {e}")
        return False
    
    # 3. 轮询解析状态（模拟前端轮询）
    print("\n3️⃣ 模拟前端状态轮询...")
    max_attempts = 20
    for attempt in range(max_attempts):
        try:
            status_response = requests.get(
                f"http://127.0.0.1:8000/kg/files/{upload_id}/status",
                timeout=10
            )
            
            if status_response.status_code == 200:
                status_result = status_response.json()
                if status_result.get('success'):
                    status_data = status_result.get('data', {})
                    status = status_data.get('status')
                    
                    print(f"   轮询 {attempt+1}: 状态 = {status}")
                    
                    if status == 'parsed':
                        print("✅ 解析完成")
                        break
                    elif status == 'failed':
                        error = status_data.get('error', '未知错误')
                        print(f"❌ 解析失败: {error}")
                        return False
                    elif status in ['uploaded', 'parsing']:
                        # 继续等待
                        time.sleep(2)
                        continue
                    else:
                        print(f"⚠ 未知状态: {status}")
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
    else:
        print("❌ 解析超时")
        return False
    
    # 4. 获取解析预览（模拟前端获取预览）
    print("\n4️⃣ 模拟前端获取解析预览...")
    try:
        preview_response = requests.get(
            f"http://127.0.0.1:8000/kg/files/{upload_id}/preview",
            timeout=15
        )
        
        if preview_response.status_code == 200:
            preview_result = preview_response.json()
            if preview_result.get('success'):
                preview_data = preview_result.get('data', {})
                print("✅ 获取预览成功")
                
                # 分析预览数据（模拟前端处理）
                return analyze_frontend_data(preview_data, upload_id)
            else:
                print(f"❌ 获取预览失败: {preview_result.get('message')}")
                return False
        else:
            print(f"❌ 预览请求失败: {preview_response.status_code}")
            print(f"   响应内容: {preview_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 获取预览异常: {e}")
        return False

def analyze_frontend_data(data, upload_id):
    """分析前端接收到的数据"""
    print("\n📊 前端数据分析:")
    
    # 提取各部分数据
    raw_data = data.get('raw_data', [])
    entities = data.get('entities', [])
    relations = data.get('relations', [])
    metadata = data.get('metadata', {})
    
    print(f"   原始数据: {len(raw_data)} 条")
    print(f"   实体数据: {len(entities)} 个")
    print(f"   关系数据: {len(relations)} 个")
    print(f"   元数据: {metadata}")
    
    if not raw_data:
        print("❌ 没有原始数据")
        return False
    
    # 检查第一条记录（前端表格显示的内容）
    print(f"\n📋 前端表格第一行数据:")
    first_record = raw_data[0]
    
    # 模拟前端表格列显示
    table_columns = [
        'anomaly_key', 'title', 'date', 'severity', 'factory', 
        'product', 'component', 'symptom', 'root_cause', 
        'countermeasure', 'supplier', 'status'
    ]
    
    print("   表格列数据:")
    for col in table_columns:
        value = first_record.get(col, '')
        print(f"     {col:15s}: {value}")
    
    # 关键检查：问题编号
    anomaly_key = first_record.get('anomaly_key', '')
    print(f"\n🔍 关键检查 - 问题编号: '{anomaly_key}'")
    
    if anomaly_key.startswith('ANOM-') and len(anomaly_key) > 10:
        print("❌ 前端仍会显示异常键值！")
        print("🐛 这表明解析器可能没有正确工作")
        
        # 详细调试信息
        print(f"\n🔧 调试信息:")
        print(f"   Upload ID: {upload_id}")
        print(f"   完整第一条记录:")
        for key, value in first_record.items():
            print(f"     {key}: {value}")
        
        return False
    else:
        print("✅ 前端将显示正确的问题编号！")
        
        # 显示前端用户将看到的内容
        print(f"\n👀 用户在前端将看到:")
        print(f"   问题编号: {anomaly_key}")
        print(f"   不良现象: {first_record.get('title', '')}")
        print(f"   部件: {first_record.get('component', '')}")
        print(f"   根因: {first_record.get('root_cause', '')}")
        print(f"   对策: {first_record.get('countermeasure', '')}")
        
        # 检查所有记录
        print(f"\n📊 所有记录的问题编号:")
        for i, record in enumerate(raw_data):
            key = record.get('anomaly_key', '')
            title = record.get('title', '')
            print(f"     {i+1}. {key} - {title}")
        
        return True

def generate_frontend_test_data():
    """生成前端测试数据文件"""
    print("\n📁 生成前端测试数据...")
    
    # 模拟正确的解析结果
    correct_data = {
        "success": True,
        "data": {
            "raw_data": [
                {
                    "anomaly_key": "ISSUE-001",
                    "title": "屏幕显示异常",
                    "date": "2024-01-15",
                    "severity": "高",
                    "factory": "深圳工厂",
                    "product": "iPhone 15",
                    "component": "显示屏",
                    "symptom": "屏幕显示异常",
                    "root_cause": "显示驱动IC故障",
                    "countermeasure": "更换驱动IC",
                    "supplier": "供应商A",
                    "status": "已解决",
                    "row_number": 2
                },
                {
                    "anomaly_key": "ISSUE-002",
                    "title": "按键失灵",
                    "date": "2024-01-16",
                    "severity": "中",
                    "factory": "东莞工厂",
                    "product": "iPhone 15 Pro",
                    "component": "按键模组",
                    "symptom": "按键失灵",
                    "root_cause": "按键弹片老化",
                    "countermeasure": "更换按键模组",
                    "supplier": "供应商B",
                    "status": "处理中",
                    "row_number": 3
                }
            ],
            "entities": [],
            "relations": [],
            "metadata": {
                "total_records": 2,
                "entity_count": 0,
                "relation_count": 0
            }
        }
    }
    
    # 保存测试数据
    with open("frontend_test_data.json", 'w', encoding='utf-8') as f:
        json.dump(correct_data, f, ensure_ascii=False, indent=2)
    
    print("✅ 前端测试数据已保存到: frontend_test_data.json")

if __name__ == "__main__":
    print("🖥 前端验证测试")
    print("="*50)
    
    # 执行完整的前端工作流程测试
    success = simulate_frontend_workflow()
    
    # 生成测试数据
    generate_frontend_test_data()
    
    print("\n" + "="*50)
    if success:
        print("🎉 前端验证测试成功！")
        print("📝 结论:")
        print("  - 后端解析器工作正常")
        print("  - API返回正确的解析结果")
        print("  - 前端应该显示正确的数据")
        print()
        print("💡 如果前端仍显示异常键值，请:")
        print("  1. 清除浏览器缓存 (Ctrl+F5)")
        print("  2. 重新上传文件")
        print("  3. 检查前端是否有缓存机制")
    else:
        print("❌ 前端验证测试失败！")
        print("🔧 需要进一步调试后端解析逻辑")
    
    print("\n📋 测试完成！")
