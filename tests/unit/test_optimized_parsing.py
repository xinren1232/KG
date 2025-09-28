#!/usr/bin/env python3
"""
测试优化后的Excel解析效果
"""

import requests
import time
import os
from pathlib import Path

def test_optimized_parsing():
    """测试优化后的解析效果"""
    print("=== 测试优化后的Excel解析 ===")
    
    # 1. 检查服务状态
    try:
        response = requests.get("http://127.0.0.1:8000/kg/stats", timeout=5)
        if response.status_code == 200:
            print("✅ 后端API服务正常")
        else:
            print(f"❌ 后端API异常 (状态码: {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ 后端API连接失败: {e}")
        return False
    
    # 2. 检查测试文件
    test_file = "test_files/水利问题调查表.xlsx"
    if not os.path.exists(test_file):
        print(f"❌ 测试文件不存在: {test_file}")
        return False
    
    print(f"📁 使用测试文件: {test_file}")
    
    # 3. 上传文件
    try:
        with open(test_file, 'rb') as f:
            files = {'file': ('水利问题调查表.xlsx', f, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
            response = requests.post("http://127.0.0.1:8000/kg/upload", files=files, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    upload_id = result.get('upload_id')
                    print(f"✅ 文件上传成功 (upload_id: {upload_id})")
                else:
                    print(f"❌ 文件上传失败: {result.get('message')}")
                    return False
            else:
                print(f"❌ 文件上传失败 (状态码: {response.status_code})")
                return False
    except Exception as e:
        print(f"❌ 文件上传异常: {e}")
        return False
    
    # 4. 等待解析完成
    print("⏳ 等待文件解析...")
    max_wait = 30  # 最多等待30秒
    wait_time = 0
    
    while wait_time < max_wait:
        try:
            status_response = requests.get(f"http://127.0.0.1:8000/kg/files/{upload_id}/status", timeout=10)
            if status_response.status_code == 200:
                status_result = status_response.json()
                if status_result.get('success'):
                    status = status_result.get('data', {}).get('status')
                    print(f"📊 当前状态: {status}")
                    
                    if status == 'parsed':
                        print("✅ 文件解析完成")
                        break
                    elif status == 'failed':
                        error = status_result.get('data', {}).get('error', '未知错误')
                        print(f"❌ 文件解析失败: {error}")
                        return False
                    
        except Exception as e:
            print(f"⚠ 状态查询异常: {e}")
        
        time.sleep(2)
        wait_time += 2
    
    if wait_time >= max_wait:
        print("❌ 解析超时")
        return False
    
    # 5. 获取解析结果
    try:
        preview_response = requests.get(f"http://127.0.0.1:8000/kg/files/{upload_id}/preview", timeout=10)
        if preview_response.status_code == 200:
            preview_result = preview_response.json()
            if preview_result.get('success'):
                data = preview_result.get('data', {})
                print("✅ 获取解析结果成功")
                
                # 分析解析结果
                analyze_parsing_result(data)
                return True
            else:
                print(f"❌ 获取解析结果失败: {preview_result.get('message')}")
                return False
        else:
            print(f"❌ 获取解析结果失败 (状态码: {preview_response.status_code})")
            return False
    except Exception as e:
        print(f"❌ 获取解析结果异常: {e}")
        return False

def analyze_parsing_result(data):
    """分析解析结果"""
    print("\n=== 解析结果分析 ===")
    
    # 基本统计
    entities = data.get('entities', [])
    relations = data.get('relations', [])
    raw_data = data.get('raw_data', [])
    
    print(f"📊 统计信息:")
    print(f"  - 原始记录: {len(raw_data)} 条")
    print(f"  - 抽取实体: {len(entities)} 个")
    print(f"  - 抽取关系: {len(relations)} 个")
    
    # 分析原始数据
    if raw_data:
        print(f"\n📋 原始数据预览 (前3条):")
        for i, record in enumerate(raw_data[:3]):
            print(f"\n--- 记录 {i+1} ---")
            for key, value in record.items():
                if value and str(value).strip():
                    print(f"  {key:15s}: {str(value)[:50]}")
    
    # 分析实体类型
    if entities:
        entity_types = {}
        for entity in entities:
            entity_type = entity.get('type', 'Unknown')
            entity_types[entity_type] = entity_types.get(entity_type, 0) + 1
        
        print(f"\n🏷 实体类型分布:")
        for entity_type, count in entity_types.items():
            print(f"  - {entity_type}: {count} 个")
        
        print(f"\n📝 实体示例 (前5个):")
        for i, entity in enumerate(entities[:5]):
            name = entity.get('name', 'N/A')
            entity_type = entity.get('type', 'N/A')
            confidence = entity.get('confidence', 0)
            print(f"  {i+1}. {name} ({entity_type}) - 置信度: {confidence:.2f}")
    
    # 分析关系类型
    if relations:
        relation_types = {}
        for relation in relations:
            relation_type = relation.get('type', 'Unknown')
            relation_types[relation_type] = relation_types.get(relation_type, 0) + 1
        
        print(f"\n🔗 关系类型分布:")
        for relation_type, count in relation_types.items():
            print(f"  - {relation_type}: {count} 个")
        
        print(f"\n🔗 关系示例 (前5个):")
        for i, relation in enumerate(relations[:5]):
            source = relation.get('source', 'N/A')
            target = relation.get('target', 'N/A')
            relation_type = relation.get('type', 'N/A')
            confidence = relation.get('confidence', 0)
            print(f"  {i+1}. {source} --[{relation_type}]--> {target} (置信度: {confidence:.2f})")
    
    # 质量评估
    print(f"\n📈 解析质量评估:")
    if raw_data:
        data_completeness = sum(1 for record in raw_data if any(record.values())) / len(raw_data) * 100
        print(f"  - 数据完整性: {data_completeness:.1f}%")
    
    if entities and raw_data:
        entity_extraction_rate = len(entities) / len(raw_data)
        print(f"  - 实体抽取率: {entity_extraction_rate:.2f} 个/记录")
    
    if relations and raw_data:
        relation_extraction_rate = len(relations) / len(raw_data)
        print(f"  - 关系抽取率: {relation_extraction_rate:.2f} 个/记录")

if __name__ == "__main__":
    success = test_optimized_parsing()
    if success:
        print("\n🎉 优化后的Excel解析测试成功！")
        print("📝 解析结果应该显示真实的Excel数据，而不是异常键值")
    else:
        print("\n❌ 优化后的Excel解析测试失败！")
        print("请检查服务状态和配置文件。")
