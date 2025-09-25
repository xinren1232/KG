#!/usr/bin/env python3
"""
清理缓存并重新测试解析效果
"""

import os
import shutil
import requests
import time
from pathlib import Path

def clear_cache():
    """清理所有缓存"""
    print("=== 清理缓存 ===")
    
    # 清理上传目录
    upload_dirs = [
        "api/uploads",
        "api/processed", 
        "api/previews",
        "data/uploads",
        "data/processed"
    ]
    
    for upload_dir in upload_dirs:
        if os.path.exists(upload_dir):
            try:
                # 清理目录内容但保留目录
                for item in os.listdir(upload_dir):
                    item_path = os.path.join(upload_dir, item)
                    if os.path.isfile(item_path):
                        os.remove(item_path)
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                print(f"✅ 清理目录: {upload_dir}")
            except Exception as e:
                print(f"⚠ 清理目录失败 {upload_dir}: {e}")
    
    # 清理可能的缓存文件
    cache_patterns = [
        "*.pyc",
        "__pycache__",
        ".pytest_cache"
    ]
    
    print("✅ 缓存清理完成")

def restart_services():
    """重启服务（如果需要）"""
    print("\n=== 检查服务状态 ===")
    
    try:
        response = requests.get("http://127.0.0.1:8000/kg/stats", timeout=5)
        if response.status_code == 200:
            print("✅ 后端API服务正常")
        else:
            print(f"⚠ 后端API状态异常: {response.status_code}")
    except Exception as e:
        print(f"❌ 后端API连接失败: {e}")
        return False
    
    try:
        response = requests.get("http://localhost:5173", timeout=5)
        if response.status_code == 200:
            print("✅ 前端服务正常")
        else:
            print(f"⚠ 前端服务状态异常: {response.status_code}")
    except Exception as e:
        print(f"❌ 前端服务连接失败: {e}")
        return False
    
    return True

def test_fresh_upload():
    """测试全新上传"""
    print("\n=== 测试全新上传和解析 ===")
    
    test_file = "test_files/水利问题调查表.xlsx"
    if not os.path.exists(test_file):
        print(f"❌ 测试文件不存在: {test_file}")
        return False
    
    try:
        # 上传文件
        with open(test_file, 'rb') as f:
            files = {'file': ('水利问题调查表_新测试.xlsx', f, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
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
    for i in range(20):  # 最多等待40秒
        try:
            status_response = requests.get(f"http://127.0.0.1:8000/kg/files/{upload_id}/status", timeout=10)
            if status_response.status_code == 200:
                status_result = status_response.json()
                if status_result.get('success'):
                    status = status_result.get('data', {}).get('status')
                    print(f"📊 解析状态: {status}")
                    
                    if status == 'parsed':
                        print("✅ 解析完成")
                        break
                    elif status == 'failed':
                        error = status_result.get('data', {}).get('error', '未知错误')
                        print(f"❌ 解析失败: {error}")
                        return False
        except Exception as e:
            print(f"⚠ 状态查询异常: {e}")
        
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
                
                # 详细分析解析结果
                return analyze_parsing_result(data, upload_id)
            else:
                print(f"❌ 获取解析结果失败: {preview_result.get('message')}")
                return False
        else:
            print(f"❌ 获取解析结果失败 (状态码: {preview_response.status_code})")
            return False
    except Exception as e:
        print(f"❌ 获取解析结果异常: {e}")
        return False

def analyze_parsing_result(data, upload_id):
    """详细分析解析结果"""
    print("\n📊 详细解析结果分析:")
    
    raw_data = data.get('raw_data', [])
    entities = data.get('entities', [])
    relations = data.get('relations', [])
    
    print(f"  - 原始记录: {len(raw_data)} 条")
    print(f"  - 抽取实体: {len(entities)} 个")
    print(f"  - 抽取关系: {len(relations)} 个")
    
    if not raw_data:
        print("❌ 没有原始数据")
        return False
    
    # 检查第一条记录
    first_record = raw_data[0]
    anomaly_key = first_record.get('anomaly_key', '')
    
    print(f"\n📋 第一条记录分析:")
    print(f"  问题编号: {anomaly_key}")
    
    # 判断是否为异常键值
    if anomaly_key.startswith('ANOM-') and len(anomaly_key) > 10:
        print("❌ 仍然是异常键值！")
        print("🔍 可能的原因:")
        print("  1. 解析器没有正确加载")
        print("  2. 映射配置有问题")
        print("  3. 缓存没有清理干净")
        
        # 显示完整记录用于调试
        print(f"\n🐛 调试信息 - 完整记录:")
        for key, value in first_record.items():
            print(f"    {key}: {value}")
        
        return False
    else:
        print("✅ 问题编号正常！")
        
        # 显示关键字段
        key_fields = ["title", "component", "symptom", "root_cause", "countermeasure"]
        print(f"\n📋 关键字段:")
        for field in key_fields:
            value = first_record.get(field, '')
            print(f"  {field:15s}: {value}")
        
        # 检查所有记录
        print(f"\n📊 所有记录的问题编号:")
        for i, record in enumerate(raw_data):
            key = record.get('anomaly_key', '')
            print(f"  记录 {i+1}: {key}")
        
        print(f"\n🎉 解析结果完全正确！上传ID: {upload_id}")
        return True

def provide_troubleshooting_guide():
    """提供故障排除指南"""
    print("\n" + "="*60)
    print("🔧 故障排除指南")
    print("="*60)
    print("如果前端仍然显示异常键值，请检查:")
    print()
    print("1. 🔄 浏览器缓存:")
    print("   - 按 Ctrl+F5 强制刷新页面")
    print("   - 清除浏览器缓存")
    print("   - 尝试无痕模式")
    print()
    print("2. 📱 前端缓存:")
    print("   - 重启前端开发服务器")
    print("   - 检查是否有旧的解析结果缓存")
    print()
    print("3. 🔧 后端服务:")
    print("   - 重启后端API服务")
    print("   - 检查日志输出")
    print()
    print("4. 📁 文件上传:")
    print("   - 尝试上传新的文件名")
    print("   - 确保使用最新的测试文件")
    print()
    print("5. 🎯 配置检查:")
    print("   - 确认增强解析器已正确导入")
    print("   - 检查映射配置文件")
    print("="*60)

if __name__ == "__main__":
    print("🧹 清理缓存并重新测试")
    print("="*50)
    
    # 步骤1: 清理缓存
    clear_cache()
    
    # 步骤2: 检查服务
    if not restart_services():
        print("❌ 服务状态异常，请检查服务")
        exit(1)
    
    # 步骤3: 测试全新上传
    success = test_fresh_upload()
    
    if success:
        print("\n🎉 测试成功！解析器工作正常！")
        print("如果前端仍显示异常键值，请检查浏览器缓存。")
    else:
        print("\n❌ 测试失败！")
        provide_troubleshooting_guide()
    
    print("\n📝 建议:")
    print("1. 在前端重新上传文件进行测试")
    print("2. 检查前端是否显示正确的解析结果")
    print("3. 如有问题，请按照故障排除指南操作")
