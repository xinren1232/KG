#!/usr/bin/env python3
"""
完整的状态修复测试
"""

import requests
import time
import json

def test_complete_workflow():
    """测试完整的工作流程"""
    print("=== 完整状态修复测试 ===")
    
    # 1. 检查API服务
    try:
        response = requests.get("http://127.0.0.1:8000/kg/stats", timeout=5)
        print("✅ API服务连接正常")
    except:
        print("❌ API服务连接失败")
        return False
    
    # 2. 上传文件
    print("\n📤 步骤1: 上传文件")
    upload_id = upload_test_file()
    if not upload_id:
        return False
    
    # 3. 检查上传后状态
    print(f"\n🔍 步骤2: 检查上传后状态")
    if not check_upload_status(upload_id):
        return False
    
    # 4. 手动触发解析
    print(f"\n🔧 步骤3: 手动触发解析")
    if not trigger_manual_parse(upload_id):
        return False
    
    # 5. 监控解析过程
    print(f"\n⏳ 步骤4: 监控解析过程")
    if not monitor_parsing_process(upload_id):
        return False
    
    # 6. 验证最终结果
    print(f"\n✅ 步骤5: 验证最终结果")
    if not verify_final_result(upload_id):
        return False
    
    print(f"\n🎉 完整工作流程测试成功！")
    return True

def upload_test_file():
    """上传测试文件"""
    test_file = "test_files/水利问题调查表.xlsx"
    
    try:
        with open(test_file, 'rb') as f:
            files = {
                'file': ('完整测试文件.xlsx', f, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
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

def check_upload_status(upload_id):
    """检查上传后的状态"""
    try:
        # 等待一下确保状态稳定
        time.sleep(1)
        
        status_response = requests.get(f"http://127.0.0.1:8000/kg/files/{upload_id}/status", timeout=10)
        
        if status_response.status_code == 200:
            status_result = status_response.json()
            if status_result.get('success'):
                status_data = status_result.get('data', {})
                file_status = status_data.get('status')
                
                print(f"📊 文件状态: {file_status}")
                
                if file_status == 'uploaded':
                    print("✅ 正确！文件上传后状态为 'uploaded'")
                    print("💡 前端应该显示: '待解析' 状态")
                    return True
                elif file_status == 'parsing':
                    print("❌ 错误！文件上传后立即显示 'parsing'")
                    print("🐛 后端仍有自动解析逻辑")
                    return False
                else:
                    print(f"⚠ 意外状态: {file_status}")
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

def trigger_manual_parse(upload_id):
    """触发手动解析"""
    try:
        parse_response = requests.post(f"http://127.0.0.1:8000/kg/files/{upload_id}/parse", timeout=30)
        
        if parse_response.status_code == 200:
            parse_result = parse_response.json()
            if parse_result.get('success'):
                print("✅ 手动解析触发成功")
                print(f"📝 消息: {parse_result.get('message')}")
                return True
            else:
                print(f"❌ 手动解析触发失败: {parse_result.get('message')}")
                return False
        else:
            print(f"❌ 手动解析请求失败: {parse_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 手动解析异常: {e}")
        return False

def monitor_parsing_process(upload_id):
    """监控解析过程"""
    print("⏳ 监控解析进度...")
    
    max_attempts = 20
    for attempt in range(max_attempts):
        try:
            status_response = requests.get(f"http://127.0.0.1:8000/kg/files/{upload_id}/status", timeout=10)
            
            if status_response.status_code == 200:
                status_result = status_response.json()
                if status_result.get('success'):
                    status_data = status_result.get('data', {})
                    file_status = status_data.get('status')
                    
                    print(f"   轮询 {attempt+1}: 状态 = {file_status}")
                    
                    if file_status == 'parsed':
                        print("✅ 解析完成")
                        return True
                    elif file_status == 'failed':
                        error = status_data.get('error', '未知错误')
                        print(f"❌ 解析失败: {error}")
                        return False
                    elif file_status == 'parsing':
                        # 继续等待
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

def verify_final_result(upload_id):
    """验证最终解析结果"""
    try:
        preview_response = requests.get(f"http://127.0.0.1:8000/kg/files/{upload_id}/preview", timeout=15)
        
        if preview_response.status_code == 200:
            preview_result = preview_response.json()
            if preview_result.get('success'):
                preview_data = preview_result.get('data', {})
                
                raw_data = preview_data.get('raw_data', [])
                entities = preview_data.get('entities', [])
                relations = preview_data.get('relations', [])
                
                print(f"📊 解析结果统计:")
                print(f"   原始记录: {len(raw_data)} 条")
                print(f"   抽取实体: {len(entities)} 个")
                print(f"   抽取关系: {len(relations)} 个")
                
                if raw_data:
                    first_record = raw_data[0]
                    anomaly_key = first_record.get('anomaly_key', '')
                    
                    print(f"\n📋 第一条记录:")
                    print(f"   问题编号: {anomaly_key}")
                    print(f"   标题: {first_record.get('title', '')}")
                    print(f"   部件: {first_record.get('component', '')}")
                    
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

def provide_final_summary():
    """提供最终总结"""
    print("\n" + "="*60)
    print("📊 状态修复最终总结")
    print("="*60)
    print("🔧 修复的问题:")
    print("  1. ❌ 文件上传后立即显示'解析中' → ✅ 显示'待解析'")
    print("  2. ❌ 后端自动启动解析任务 → ✅ 等待手动触发")
    print("  3. ❌ 前端状态显示混乱 → ✅ 清晰的状态流程")
    print()
    print("✅ 修复后的工作流程:")
    print("  1. 用户上传文件 → 状态: '待解析'")
    print("  2. 用户点击'开始解析' → 状态: '解析中'")
    print("  3. 解析完成 → 状态: '已解析'")
    print("  4. 用户查看结果和导出数据")
    print()
    print("🎯 用户体验改进:")
    print("  - 明确的操作控制权")
    print("  - 清晰的状态反馈")
    print("  - 符合预期的交互流程")
    print("  - 避免混淆的状态显示")
    print("="*60)

if __name__ == "__main__":
    print("🔧 完整状态修复测试")
    print("="*50)
    
    success = test_complete_workflow()
    
    provide_final_summary()
    
    if success:
        print(f"\n🎉 状态修复完全成功！")
        print("现在用户上传文件后将看到正确的'待解析'状态")
        print("只有手动点击'开始解析'按钮才会开始解析")
    else:
        print(f"\n❌ 状态修复需要进一步调试")
    
    print("\n📋 测试完成！")
