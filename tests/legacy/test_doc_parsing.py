#!/usr/bin/env python3
import requests
import time

def test_doc_parsing():
    """测试DOC文档解析修复"""
    print("=== 测试DOC文档解析修复 ===")
    
    # 创建一个简单的DOC文件（实际上是文本文件，但扩展名为.doc）
    # 这是为了测试解析逻辑，真实的DOC文件需要Microsoft Word创建
    doc_content = """硬件质量测试报告

1. 测试概述
本报告描述了对智能手机硬件的质量测试结果。

2. 测试项目
主要测试项目包括：
- 电池续航测试
- 屏幕显示测试
- 摄像头功能测试
- 充电接口测试

3. 测试结果
电池续航: 发现异常，续航时间不足
屏幕显示: 正常，无故障
摄像头: 部分功能异常，需要进一步检查
充电接口: 正常工作

4. 问题分析
主要问题集中在电池和摄像头模块。
建议加强供应商质量控制。

5. 结论
需要对电池供应商进行质量审核。
摄像头模块需要重新设计。
"""
    
    # 创建测试DOC文件
    with open('test_hardware_report.doc', 'w', encoding='utf-8') as f:
        f.write(doc_content)
    print("✅ 创建DOC测试文件: test_hardware_report.doc")
    
    try:
        # 1. 上传文件
        print("1. 上传DOC文档...")
        with open('test_hardware_report.doc', 'rb') as f:
            files = {'file': f}
            upload_response = requests.post('http://localhost:8000/kg/upload', files=files, timeout=10)
        
        if upload_response.status_code != 200:
            print(f"   ❌ 上传失败: {upload_response.status_code}")
            print(f"   错误: {upload_response.text}")
            return False
        
        upload_result = upload_response.json()
        if not upload_result.get('success'):
            print(f"   ❌ 上传失败: {upload_result.get('message')}")
            return False
        
        upload_id = upload_result.get('upload_id')
        print(f"   ✅ 上传成功: {upload_id}")
        
        # 2. 触发解析
        print("2. 触发解析...")
        parse_response = requests.post(f'http://localhost:8000/kg/files/{upload_id}/parse', timeout=10)
        
        if parse_response.status_code != 200:
            print(f"   ❌ 解析请求失败: {parse_response.status_code}")
            print(f"   错误: {parse_response.text}")
            return False
        
        parse_result = parse_response.json()
        if not parse_result.get('success'):
            print(f"   ❌ 解析失败: {parse_result.get('message')}")
            return False
        
        print(f"   ✅ 解析触发成功: {parse_result.get('message')}")
        
        # 3. 等待解析完成
        print("3. 等待解析完成...")
        time.sleep(3)
        
        # 4. 获取解析结果
        print("4. 获取解析结果...")
        preview_response = requests.get(f'http://localhost:8000/kg/files/{upload_id}/preview', timeout=10)
        
        if preview_response.status_code != 200:
            print(f"   ❌ 获取结果失败: {preview_response.status_code}")
            print(f"   错误: {preview_response.text}")
            return False
        
        preview_result = preview_response.json()
        if not preview_result.get('success'):
            print(f"   ❌ 获取结果失败: {preview_result.get('message')}")
            return False
        
        data = preview_result.get('data', {})
        raw_data = data.get('raw_data', [])
        entities = data.get('entities', [])
        
        print(f"   ✅ 解析结果获取成功!")
        print(f"   📊 统计信息:")
        print(f"      - 原始数据条数: {len(raw_data)}")
        print(f"      - 识别实体数量: {len(entities)}")
        
        # 显示解析内容
        if raw_data:
            print(f"   📄 解析内容示例:")
            for i, item in enumerate(raw_data[:5]):
                content = item.get('content', '')[:80]
                item_type = item.get('type', '未知')
                print(f"      {i+1}. [{item_type}] {content}...")
        else:
            print("   ⚠️ 没有解析到内容数据")
        
        # 显示识别的实体
        if entities:
            print(f"   🏷️ 识别的实体:")
            for entity in entities[:5]:
                name = entity.get('name')
                entity_type = entity.get('type')
                confidence = entity.get('confidence', 0)
                print(f"      - {name} ({entity_type}) - 置信度: {confidence:.2f}")
        else:
            print("   ⚠️ 没有识别到实体")
        
        return len(raw_data) > 0  # 如果有解析数据就算成功
        
    except Exception as e:
        print(f"   ❌ 测试异常: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_api_status():
    """测试API状态"""
    try:
        response = requests.get('http://localhost:8000/health', timeout=5)
        if response.status_code == 200:
            print("✅ API服务正常")
            return True
        else:
            print(f"❌ API响应异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API连接失败: {e}")
        return False

if __name__ == "__main__":
    print("🔧 开始测试DOC文档解析修复...")
    
    # 检查API状态
    if not test_api_status():
        print("❌ API服务不可用，请确保API服务正在运行")
        exit(1)
    
    # 测试DOC文档解析
    if test_doc_parsing():
        print("\n🎉 DOC文档解析修复成功!")
    else:
        print("\n❌ DOC文档解析仍有问题")
    
    print("\n测试完成。")
