#!/usr/bin/env python3
"""
测试新的文档解析功能
"""

import requests
import time
import json
from pathlib import Path

API_BASE = "http://127.0.0.1:8000"

def test_document_parsing():
    """测试完整的文档解析流程"""
    print("🚀 开始测试文档解析功能...")
    
    # 1. 测试文件上传
    print("\n📤 测试文件上传...")
    
    # 创建一个测试Excel文件
    test_file_content = """问题编号,不良现象,发生日期,严重度,工厂,机型,版本,部件,原因分析,改善对策
ANOM-001,对焦失败,2024-01-15,S2,深圳工厂,iPhone15,iOS17.1,摄像头,镜头污染,清洁镜头
ANOM-002,屏幕闪烁,2024-01-16,S1,上海工厂,iPhone15Pro,iOS17.1,显示屏,驱动IC异常,更换驱动IC
ANOM-003,充电慢,2024-01-17,S3,北京工厂,iPhone15Plus,iOS17.1,充电器,功率不足,升级充电器"""
    
    # 保存为临时CSV文件
    test_file = Path("test_data.csv")
    test_file.write_text(test_file_content, encoding="utf-8")
    
    try:
        # 上传文件
        with open(test_file, "rb") as f:
            files = {"file": ("test_data.csv", f, "text/csv")}
            response = requests.post(f"{API_BASE}/kg/upload", files=files)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                upload_id = result.get("upload_id")
                print(f"   ✅ 文件上传成功: {upload_id}")
                print(f"   📄 文件名: {result.get('filename')}")
                print(f"   📊 文件大小: {result.get('size')} bytes")
                
                # 2. 轮询文件状态
                print(f"\n⏳ 等待文件解析完成...")
                max_wait = 30  # 最多等待30秒
                wait_time = 0
                
                while wait_time < max_wait:
                    status_response = requests.get(f"{API_BASE}/kg/files/{upload_id}/status")
                    if status_response.status_code == 200:
                        status_result = status_response.json()
                        if status_result.get("success"):
                            file_status = status_result["data"]["status"]
                            print(f"   📊 当前状态: {file_status}")
                            
                            if file_status == "parsed":
                                print("   ✅ 文件解析完成!")
                                break
                            elif file_status == "failed":
                                error = status_result["data"].get("error", "未知错误")
                                print(f"   ❌ 文件解析失败: {error}")
                                return
                    
                    time.sleep(2)
                    wait_time += 2
                
                if wait_time >= max_wait:
                    print("   ⏰ 等待超时")
                    return
                
                # 3. 获取解析预览
                print(f"\n📋 获取解析预览...")
                preview_response = requests.get(f"{API_BASE}/kg/files/{upload_id}/preview")
                
                if preview_response.status_code == 200:
                    preview_result = preview_response.json()
                    if preview_result.get("success"):
                        preview_data = preview_result["data"]
                        
                        entities = preview_data.get("entities", [])
                        relations = preview_data.get("relations", [])
                        metadata = preview_data.get("metadata", {})
                        
                        print(f"   ✅ 解析预览获取成功!")
                        print(f"   📊 实体数量: {len(entities)}")
                        print(f"   🔗 关系数量: {len(relations)}")
                        print(f"   📈 元数据: {metadata}")
                        
                        # 显示部分实体
                        if entities:
                            print(f"\n   🏷️ 实体示例:")
                            for i, entity in enumerate(entities[:5]):
                                print(f"      {i+1}. {entity.get('name')} ({entity.get('type')})")
                        
                        # 显示部分关系
                        if relations:
                            print(f"\n   🔗 关系示例:")
                            for i, relation in enumerate(relations[:5]):
                                print(f"      {i+1}. {relation.get('source')} -> {relation.get('type')} -> {relation.get('target')}")
                        
                        # 4. 提交到知识图谱
                        print(f"\n🕸️ 提交到知识图谱...")
                        commit_response = requests.post(f"{API_BASE}/kg/files/{upload_id}/commit")
                        
                        if commit_response.status_code == 200:
                            commit_result = commit_response.json()
                            if commit_result.get("success"):
                                commit_data = commit_result["data"]
                                print(f"   ✅ 知识图谱构建成功!")
                                print(f"   📊 创建节点: {commit_data.get('nodes_created')}")
                                print(f"   🔗 创建关系: {commit_data.get('relations_created')}")
                            else:
                                print(f"   ❌ 知识图谱构建失败: {commit_result.get('message')}")
                        else:
                            print(f"   ❌ 提交请求失败: {commit_response.status_code}")
                    else:
                        print(f"   ❌ 获取预览失败: {preview_result.get('message')}")
                else:
                    print(f"   ❌ 预览请求失败: {preview_response.status_code}")
            else:
                print(f"   ❌ 文件上传失败: {result.get('message')}")
        else:
            print(f"   ❌ 上传请求失败: {response.status_code}")
            print(f"   📄 响应内容: {response.text}")
    
    finally:
        # 清理测试文件
        test_file.unlink(missing_ok=True)

def test_api_status():
    """测试API服务状态"""
    print("🔍 检查API服务状态...")
    
    try:
        response = requests.get(f"{API_BASE}/kg/stats")
        if response.status_code == 200:
            print("   ✅ API服务正常运行")
            return True
        else:
            print(f"   ❌ API服务异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ 无法连接API服务: {e}")
        return False

if __name__ == "__main__":
    # 检查API服务
    if test_api_status():
        # 测试文档解析
        test_document_parsing()
        print("\n🎉 文档解析功能测试完成!")
    else:
        print("\n❌ 请先启动API服务: uvicorn api.main_v01:app --host 127.0.0.1 --port 8000 --reload")
