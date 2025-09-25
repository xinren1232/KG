#!/usr/bin/env python3
"""
测试前端集成的完整流程
"""

import requests
import time
import json
from pathlib import Path

API_BASE = "http://127.0.0.1:8000"

def test_complete_workflow():
    """测试完整的前端集成工作流程"""
    print("🚀 开始测试前端集成工作流程...")
    
    # 创建测试CSV文件（模拟前端上传）
    test_content = """问题编号,不良现象,发生日期,严重度,工厂,机型,版本,部件,原因分析,改善对策
ANOM-001,对焦失败,2024-01-15,S2,深圳工厂,iPhone15,iOS17.1,摄像头,镜头污染,清洁镜头
ANOM-002,屏幕闪烁,2024-01-16,S1,上海工厂,iPhone15Pro,iOS17.1,显示屏,驱动IC异常,更换驱动IC"""
    
    test_file = Path("frontend_test.csv")
    test_file.write_text(test_content, encoding="utf-8")
    
    try:
        # 步骤1: 文件上传（模拟前端上传）
        print("\n📤 步骤1: 文件上传...")
        with open(test_file, "rb") as f:
            files = {"file": ("frontend_test.csv", f, "text/csv")}
            upload_response = requests.post(f"{API_BASE}/kg/upload", files=files)
        
        print(f"   上传响应状态: {upload_response.status_code}")
        upload_result = upload_response.json()
        print(f"   上传响应内容: {json.dumps(upload_result, ensure_ascii=False, indent=2)}")
        
        if not upload_result.get("success"):
            print("   ❌ 文件上传失败")
            return False
        
        upload_id = upload_result.get("upload_id")
        print(f"   ✅ 文件上传成功，upload_id: {upload_id}")
        
        # 步骤2: 状态轮询（模拟前端轮询）
        print(f"\n⏳ 步骤2: 状态轮询...")
        max_attempts = 15
        for attempt in range(max_attempts):
            status_response = requests.get(f"{API_BASE}/kg/files/{upload_id}/status")
            status_result = status_response.json()
            
            print(f"   尝试 {attempt + 1}: 状态响应 {status_response.status_code}")
            
            if status_result.get("success"):
                file_status = status_result["data"]["status"]
                print(f"   文件状态: {file_status}")
                
                if file_status == "parsed":
                    print("   ✅ 文件解析完成!")
                    break
                elif file_status == "failed":
                    error = status_result["data"].get("error", "未知错误")
                    print(f"   ❌ 文件解析失败: {error}")
                    return False
                elif file_status in ["uploaded", "parsing"]:
                    print(f"   ⏳ 文件正在处理中...")
                    time.sleep(2)
                    continue
            else:
                print(f"   ❌ 状态查询失败: {status_result.get('message')}")
                return False
        else:
            print("   ⏰ 状态轮询超时")
            return False
        
        # 步骤3: 获取预览（模拟前端获取解析结果）
        print(f"\n📋 步骤3: 获取解析预览...")
        preview_response = requests.get(f"{API_BASE}/kg/files/{upload_id}/preview")
        preview_result = preview_response.json()
        
        print(f"   预览响应状态: {preview_response.status_code}")
        
        if preview_result.get("success"):
            preview_data = preview_result["data"]
            entities = preview_data.get("entities", [])
            relations = preview_data.get("relations", [])
            metadata = preview_data.get("metadata", {})
            
            print(f"   ✅ 获取预览成功!")
            print(f"   📊 实体数量: {len(entities)}")
            print(f"   🔗 关系数量: {len(relations)}")
            print(f"   📈 元数据: {metadata}")
            
            # 显示部分数据
            if entities:
                print(f"   🏷️ 实体示例:")
                for i, entity in enumerate(entities[:3]):
                    print(f"      {i+1}. {entity.get('name')} ({entity.get('type')})")
            
            if relations:
                print(f"   🔗 关系示例:")
                for i, relation in enumerate(relations[:3]):
                    print(f"      {i+1}. {relation.get('source')} -> {relation.get('type')} -> {relation.get('target')}")
        else:
            print(f"   ❌ 获取预览失败: {preview_result.get('message')}")
            return False
        
        # 步骤4: 提交到知识图谱（模拟前端构建图谱）
        print(f"\n🕸️ 步骤4: 提交到知识图谱...")
        commit_response = requests.post(f"{API_BASE}/kg/files/{upload_id}/commit")
        commit_result = commit_response.json()
        
        print(f"   提交响应状态: {commit_response.status_code}")
        
        if commit_result.get("success"):
            commit_data = commit_result["data"]
            print(f"   ✅ 知识图谱构建成功!")
            print(f"   📊 创建节点: {commit_data.get('nodes_created')}")
            print(f"   🔗 创建关系: {commit_data.get('relations_created')}")
        else:
            print(f"   ❌ 知识图谱构建失败: {commit_result.get('message')}")
            return False
        
        # 步骤5: 验证最终状态
        print(f"\n🔍 步骤5: 验证最终状态...")
        final_status_response = requests.get(f"{API_BASE}/kg/files/{upload_id}/status")
        final_status_result = final_status_response.json()
        
        if final_status_result.get("success"):
            final_status = final_status_result["data"]["status"]
            print(f"   最终状态: {final_status}")
            
            if final_status == "committed":
                print("   ✅ 工作流程完成，文件已成功入库!")
                return True
            else:
                print(f"   ⚠️ 状态异常: {final_status}")
                return False
        else:
            print(f"   ❌ 最终状态查询失败")
            return False
    
    finally:
        # 清理测试文件
        test_file.unlink(missing_ok=True)

def test_api_endpoints():
    """测试所有API端点是否可用"""
    print("🔍 测试API端点可用性...")
    
    endpoints = [
        ("GET", "/kg/stats", "统计信息"),
        ("GET", "/kg/dictionary", "词典数据"),
    ]
    
    for method, endpoint, description in endpoints:
        try:
            if method == "GET":
                response = requests.get(f"{API_BASE}{endpoint}")
            else:
                response = requests.post(f"{API_BASE}{endpoint}")
            
            print(f"   {method} {endpoint} ({description}): {response.status_code}")
        except Exception as e:
            print(f"   {method} {endpoint} ({description}): 错误 - {e}")

if __name__ == "__main__":
    print("🧪 前端集成测试开始")
    print("=" * 50)
    
    # 测试API端点
    test_api_endpoints()
    
    print("\n" + "=" * 50)
    
    # 测试完整工作流程
    if test_complete_workflow():
        print("\n🎉 前端集成测试成功!")
        print("✅ 所有步骤都正常工作，前端可以正常使用新的API接口")
    else:
        print("\n❌ 前端集成测试失败!")
        print("⚠️ 请检查API服务和解析逻辑")
    
    print("\n" + "=" * 50)
    print("测试完成")
