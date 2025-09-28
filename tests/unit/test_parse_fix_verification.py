#!/usr/bin/env python3
"""
验证解析修复效果
"""

import requests
import time
import json
import os
from pathlib import Path

def test_parse_fix():
    """测试解析修复效果"""
    print("=== 验证解析修复效果 ===")
    
    # 1. 清理旧的缓存文件
    print("🧹 清理旧缓存...")
    cleanup_old_cache()
    
    # 2. 测试完整的上传和解析流程
    print("\n📤 测试完整流程...")
    success = test_complete_flow()
    
    if success:
        print("\n🎉 解析修复验证成功！")
        return True
    else:
        print("\n❌ 解析修复验证失败！")
        return False

def cleanup_old_cache():
    """清理旧的缓存文件"""
    cache_dir = Path("api/cache")
    if cache_dir.exists():
        # 删除所有.json文件
        json_files = list(cache_dir.glob("*.json"))
        for f in json_files:
            try:
                f.unlink()
            except:
                pass
        print(f"✅ 清理了 {len(json_files)} 个缓存文件")

def test_complete_flow():
    """测试完整的上传解析流程"""
    
    # 1. 检查API服务
    try:
        response = requests.get("http://127.0.0.1:8000/kg/stats", timeout=5)
        print("✅ API服务正常")
    except:
        print("❌ API服务异常")
        return False
    
    # 2. 上传文件
    print("\n📁 步骤1: 上传文件")
    upload_id = upload_test_file()
    if not upload_id:
        return False
    
    # 3. 验证上传状态
    print(f"\n📊 步骤2: 验证上传状态")
    if not verify_upload_status(upload_id):
        return False
    
    # 4. 手动触发解析
    print(f"\n🔧 步骤3: 手动触发解析")
    if not trigger_parse(upload_id):
        return False
    
    # 5. 监控解析过程
    print(f"\n⏳ 步骤4: 监控解析过程")
    if not monitor_parsing(upload_id):
        return False
    
    # 6. 验证解析结果
    print(f"\n✅ 步骤5: 验证解析结果")
    if not verify_results(upload_id):
        return False
    
    print(f"\n🎊 完整流程测试成功！")
    return True

def upload_test_file():
    """上传测试文件"""
    test_file = "test_files/水利问题调查表.xlsx"
    
    if not os.path.exists(test_file):
        print(f"❌ 测试文件不存在: {test_file}")
        return None
    
    try:
        with open(test_file, 'rb') as f:
            files = {
                'file': ('修复验证文件.xlsx', f, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
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

def verify_upload_status(upload_id):
    """验证上传状态"""
    try:
        time.sleep(1)  # 等待状态稳定
        
        status_response = requests.get(f"http://127.0.0.1:8000/kg/files/{upload_id}/status", timeout=10)
        
        if status_response.status_code == 200:
            status_result = status_response.json()
            if status_result.get('success'):
                status_data = status_result.get('data', {})
                file_status = status_data.get('status')
                
                print(f"📊 文件状态: {file_status}")
                
                if file_status == 'uploaded':
                    print("✅ 上传状态正确")
                    return True
                else:
                    print(f"❌ 上传状态异常: {file_status}")
                    return False
            else:
                print(f"❌ 状态查询失败: {status_result.get('message')}")
                return False
        else:
            print(f"❌ 状态查询请求失败: {status_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 状态查询异常: {e}")
        return False

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

def verify_results(upload_id):
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
                
                print(f"📊 解析结果:")
                print(f"   原始记录: {len(raw_data)} 条")
                print(f"   抽取实体: {len(entities)} 个")
                print(f"   抽取关系: {len(relations)} 个")
                
                if raw_data:
                    first_record = raw_data[0]
                    anomaly_key = first_record.get('anomaly_key', '')
                    
                    print(f"\n📋 第一条记录:")
                    print(f"   问题编号: {anomaly_key}")
                    print(f"   标题: {first_record.get('title', '')}")
                    
                    # 验证数据质量
                    if anomaly_key.startswith('ANOM-') and len(anomaly_key) > 10:
                        print("❌ 仍然是异常键值")
                        return False
                    else:
                        print("✅ 解析结果正确")
                        return True
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

def test_frontend_simulation():
    """模拟前端操作"""
    print("\n🖥 模拟前端操作测试")
    
    # 模拟前端的完整操作流程
    try:
        # 1. 上传文件
        upload_id = upload_test_file()
        if not upload_id:
            return False
        
        # 2. 模拟前端检查状态
        time.sleep(1)
        status_response = requests.get(f"http://127.0.0.1:8000/kg/files/{upload_id}/status")
        status_result = status_response.json()
        
        if status_result.get('success'):
            file_status = status_result.get('data', {}).get('status')
            print(f"📱 前端看到的状态: {file_status}")
            
            if file_status == 'uploaded':
                print("✅ 前端将显示'待解析'状态")
            else:
                print(f"❌ 前端状态异常: {file_status}")
                return False
        
        # 3. 模拟前端点击解析按钮
        print("🖱 模拟用户点击'开始解析'按钮")
        parse_response = requests.post(f"http://127.0.0.1:8000/kg/files/{upload_id}/parse")
        parse_result = parse_response.json()
        
        if parse_result.get('success'):
            print("✅ 前端解析请求成功")
        else:
            print(f"❌ 前端解析请求失败: {parse_result.get('message')}")
            return False
        
        # 4. 模拟前端轮询状态
        print("⏳ 模拟前端轮询解析状态")
        for i in range(10):
            time.sleep(2)
            status_response = requests.get(f"http://127.0.0.1:8000/kg/files/{upload_id}/status")
            status_result = status_response.json()
            
            if status_result.get('success'):
                file_status = status_result.get('data', {}).get('status')
                print(f"   前端轮询 {i+1}: {file_status}")
                
                if file_status == 'parsed':
                    print("✅ 前端检测到解析完成")
                    break
                elif file_status == 'failed':
                    print("❌ 前端检测到解析失败")
                    return False
        
        # 5. 模拟前端获取结果
        print("📊 模拟前端获取解析结果")
        preview_response = requests.get(f"http://127.0.0.1:8000/kg/files/{upload_id}/preview")
        preview_result = preview_response.json()
        
        if preview_result.get('success'):
            data = preview_result.get('data', {})
            raw_data = data.get('raw_data', [])
            print(f"✅ 前端成功获取 {len(raw_data)} 条解析记录")
            return True
        else:
            print(f"❌ 前端获取结果失败: {preview_result.get('message')}")
            return False
        
    except Exception as e:
        print(f"❌ 前端模拟异常: {e}")
        return False

if __name__ == "__main__":
    print("🔧 解析修复验证测试")
    print("="*50)
    
    # 测试1: 完整流程
    success1 = test_parse_fix()
    
    # 测试2: 前端模拟
    success2 = test_frontend_simulation()
    
    print("\n" + "="*50)
    print("📊 测试结果总结:")
    print(f"  完整流程测试: {'✅ 通过' if success1 else '❌ 失败'}")
    print(f"  前端模拟测试: {'✅ 通过' if success2 else '❌ 失败'}")
    
    if success1 and success2:
        print("\n🎉 解析功能修复完全成功！")
        print("现在用户可以正常使用解析功能了！")
    else:
        print("\n❌ 解析功能仍有问题，需要进一步调试。")
    
    print("\n📋 验证完成！")
