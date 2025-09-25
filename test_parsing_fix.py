#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试解析修复效果
"""

import requests
import json
import time
from pathlib import Path

def test_parsing_fix():
    """测试解析修复效果"""
    
    print("🔧 测试解析修复效果")
    print("=" * 50)
    
    base_url = "http://127.0.0.1:8000"
    
    # 1. 创建测试文件
    print("1️⃣ 创建测试文件...")
    test_content = "编号,名称,类型,描述\n001,测试项目1,类型A,这是第一个测试项目\n002,测试项目2,类型B,这是第二个测试项目"
    test_file = Path("test_fix.csv")
    test_file.write_text(test_content, encoding='utf-8')
    print(f"✅ 测试文件创建: {test_file.name}")
    
    try:
        # 2. 上传文件
        print("\n2️⃣ 上传文件...")
        with open(test_file, 'rb') as f:
            files = {'file': (test_file.name, f, 'text/csv')}
            response = requests.post(f"{base_url}/kg/upload", files=files)
        
        if response.status_code != 200:
            print(f"❌ 上传失败: {response.status_code}")
            print(f"响应: {response.text}")
            return False
            
        upload_data = response.json()
        upload_id = upload_data['upload_id']
        print(f"✅ 上传成功 (ID: {upload_id})")
        
        # 3. 检查文件状态
        print("\n3️⃣ 检查初始状态...")
        status_response = requests.get(f"{base_url}/kg/files/{upload_id}/status")
        if status_response.status_code == 200:
            status_data = status_response.json()
            print(f"✅ 初始状态: {status_data}")
        else:
            print(f"❌ 状态查询失败: {status_response.status_code}")
            print(f"响应: {status_response.text}")
        
        # 4. 触发解析
        print("\n4️⃣ 触发解析...")
        parse_response = requests.post(f"{base_url}/kg/files/{upload_id}/parse")
        
        print(f"解析响应状态: {parse_response.status_code}")
        print(f"解析响应内容: {parse_response.text}")
        
        if parse_response.status_code != 200:
            print(f"❌ 解析触发失败")
            return False
        
        # 5. 监控解析过程
        print("\n5️⃣ 监控解析过程...")
        max_wait = 30
        wait_time = 0
        
        while wait_time < max_wait:
            status_response = requests.get(f"{base_url}/kg/files/{upload_id}/status")
            
            if status_response.status_code == 200:
                try:
                    status_data = status_response.json()
                    current_status = status_data.get('data', {}).get('status', 'unknown')
                    print(f"   [{wait_time}s] 状态: {current_status}")
                    
                    if current_status == 'parsed':
                        print("✅ 解析完成")
                        break
                    elif current_status == 'failed':
                        error_msg = status_data.get('data', {}).get('error', '未知错误')
                        print(f"❌ 解析失败: {error_msg}")
                        return False
                except json.JSONDecodeError as e:
                    print(f"❌ 状态响应JSON解析失败: {e}")
                    print(f"原始响应: {status_response.text}")
                    return False
            else:
                print(f"❌ 状态查询失败: {status_response.status_code}")
                print(f"响应: {status_response.text}")
            
            time.sleep(2)
            wait_time += 2
        
        if wait_time >= max_wait:
            print("❌ 解析超时")
            return False
        
        # 6. 获取解析结果
        print("\n6️⃣ 获取解析结果...")
        preview_response = requests.get(f"{base_url}/kg/files/{upload_id}/preview")
        
        if preview_response.status_code == 200:
            try:
                preview_data = preview_response.json()
                print(f"✅ 预览数据获取成功")
                
                raw_data = preview_data.get('data', {}).get('raw_data', [])
                metadata = preview_data.get('data', {}).get('metadata', {})
                
                print(f"   数据记录数: {len(raw_data)}")
                print(f"   元数据字段数: {len(metadata)}")
                
                if raw_data:
                    print(f"   示例记录: {raw_data[0]}")
                
                return True
                
            except json.JSONDecodeError as e:
                print(f"❌ 预览响应JSON解析失败: {e}")
                print(f"原始响应: {preview_response.text}")
                return False
        else:
            print(f"❌ 预览数据获取失败: {preview_response.status_code}")
            print(f"响应: {preview_response.text}")
            return False
    
    except Exception as e:
        print(f"❌ 测试异常: {e}")
        return False
    
    finally:
        # 清理测试文件
        if test_file.exists():
            test_file.unlink()
            print(f"\n🧹 清理测试文件: {test_file.name}")

def test_file_paths():
    """测试文件路径配置"""
    print("\n🗂️ 测试文件路径配置")
    print("=" * 50)
    
    try:
        from api.files.manager import UPLOAD, CACHE
        
        print(f"上传目录: {UPLOAD.absolute()}")
        print(f"缓存目录: {CACHE.absolute()}")
        print(f"上传目录存在: {UPLOAD.exists()}")
        print(f"缓存目录存在: {CACHE.exists()}")
        
        if UPLOAD.exists():
            files = list(UPLOAD.glob("*"))
            print(f"上传文件数量: {len(files)}")
            for f in files[-3:]:
                print(f"   {f.name} ({f.stat().st_size} bytes)")
        
        if CACHE.exists():
            cache_files = list(CACHE.glob("*.json"))
            print(f"缓存文件数量: {len(cache_files)}")
            for f in cache_files[-3:]:
                print(f"   {f.name}")
        
        return True
        
    except Exception as e:
        print(f"❌ 路径测试失败: {e}")
        return False

if __name__ == "__main__":
    print("🔧 开始解析问题修复测试")
    
    # 测试文件路径
    path_ok = test_file_paths()
    
    # 测试解析流程
    if path_ok:
        parse_ok = test_parsing_fix()
        
        if parse_ok:
            print("\n🎉 解析修复测试成功！")
            print("问题已解决，解析功能正常工作")
        else:
            print("\n⚠️ 解析修复测试失败")
            print("需要进一步调试")
    else:
        print("\n❌ 文件路径配置有问题")
        print("需要检查目录配置")
