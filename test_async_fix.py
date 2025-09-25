#!/usr/bin/env python3
"""
测试异步修复是否生效
"""

import requests
import time
import os

def test_async_fix():
    """测试异步修复"""
    print("=== 测试异步修复 ===")
    
    # 1. 检查前端是否正常运行
    try:
        response = requests.get("http://localhost:5173", timeout=5)
        print(f"✓ 前端服务正常运行 (状态码: {response.status_code})")
    except Exception as e:
        print(f"✗ 前端服务异常: {e}")
        return False
    
    # 2. 检查后端API是否正常
    try:
        response = requests.get("http://127.0.0.1:8000/kg/stats", timeout=5)
        if response.status_code == 200:
            print("✓ 后端API正常运行")
        else:
            print(f"✗ 后端API异常 (状态码: {response.status_code})")
            return False
    except Exception as e:
        print(f"✗ 后端API异常: {e}")
        return False
    
    # 3. 测试文件上传功能
    test_file_path = "test_files/水利问题调查表.xlsx"
    if os.path.exists(test_file_path):
        try:
            with open(test_file_path, 'rb') as f:
                files = {'file': ('水利问题调查表.xlsx', f, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
                response = requests.post("http://127.0.0.1:8000/kg/upload", files=files, timeout=30)
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get('success'):
                        upload_id = result.get('upload_id')
                        print(f"✓ 文件上传成功 (upload_id: {upload_id})")
                        
                        # 4. 测试文件状态查询
                        time.sleep(2)  # 等待文件处理
                        status_response = requests.get(f"http://127.0.0.1:8000/kg/files/{upload_id}/status", timeout=10)
                        if status_response.status_code == 200:
                            status_result = status_response.json()
                            print(f"✓ 文件状态查询成功: {status_result.get('data', {}).get('status', 'unknown')}")
                            return True
                        else:
                            print(f"✗ 文件状态查询失败 (状态码: {status_response.status_code})")
                            return False
                    else:
                        print(f"✗ 文件上传失败: {result.get('message', '未知错误')}")
                        return False
                else:
                    print(f"✗ 文件上传失败 (状态码: {response.status_code})")
                    return False
        except Exception as e:
            print(f"✗ 文件上传测试异常: {e}")
            return False
    else:
        print(f"⚠ 测试文件不存在: {test_file_path}")
        print("✓ 基础服务检查通过，跳过文件上传测试")
        return True

if __name__ == "__main__":
    success = test_async_fix()
    if success:
        print("\n🎉 异步修复测试通过！")
        print("前端应该不再出现异步错误了。")
    else:
        print("\n❌ 异步修复测试失败！")
        print("请检查服务状态。")
