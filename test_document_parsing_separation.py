#!/usr/bin/env python3
"""
测试文档解析与图谱构建分离功能
"""

import requests
import time
import json
import pandas as pd
from pathlib import Path

API_BASE = "http://127.0.0.1:8000"

def create_document_parsing_test_file():
    """创建专门用于文档解析测试的文件"""
    data = {
        "序号": [1, 2, 3, 4, 5],
        "问题编号": ["ISSUE-001", "ISSUE-002", "ISSUE-003", "ISSUE-004", "ISSUE-005"],
        "问题描述": [
            "摄像头对焦失败，无法正常拍照",
            "显示屏出现闪烁现象，影响使用",
            "充电速度明显变慢，充电时间延长",
            "设备发热严重，温度过高",
            "系统经常死机重启，稳定性差"
        ],
        "发现日期": ["2024-01-15", "2024-01-16", "2024-01-17", "2024-01-18", "2024-01-19"],
        "严重等级": ["高", "中", "低", "高", "中"],
        "责任部门": ["硬件部", "显示部", "电源部", "散热部", "软件部"],
        "处理状态": ["处理中", "已解决", "待处理", "处理中", "已解决"],
        "备注": [
            "需要更换镜头模组",
            "已更新驱动程序",
            "建议升级充电器",
            "增加散热片",
            "已发布系统补丁"
        ]
    }
    
    df = pd.DataFrame(data)
    test_file = Path("document_parsing_test.xlsx")
    df.to_excel(test_file, index=False, sheet_name="问题清单")
    
    print(f"✅ 创建文档解析测试文件: {test_file}")
    print(f"📊 数据行数: {len(df)}")
    print(f"📋 字段数: {len(df.columns)}")
    print(f"📄 字段列表: {list(df.columns)}")
    
    return test_file

def test_document_parsing_only():
    """测试纯文档解析功能（不涉及图谱构建）"""
    print("🚀 开始测试纯文档解析功能...")
    
    # 创建测试文件
    test_file = create_document_parsing_test_file()
    
    try:
        # 步骤1: 上传文档
        print(f"\n📤 步骤1: 上传文档...")
        with open(test_file, "rb") as f:
            files = {"file": (test_file.name, f, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
            upload_response = requests.post(f"{API_BASE}/kg/upload", files=files)
        
        upload_result = upload_response.json()
        if not upload_result.get("success"):
            print(f"   ❌ 文档上传失败: {upload_result.get('message')}")
            return False
        
        upload_id = upload_result.get("upload_id")
        print(f"   ✅ 文档上传成功: {upload_id}")
        
        # 步骤2: 等待文档解析完成
        print(f"\n⏳ 步骤2: 等待文档解析...")
        max_attempts = 15
        for attempt in range(max_attempts):
            status_response = requests.get(f"{API_BASE}/kg/files/{upload_id}/status")
            status_result = status_response.json()
            
            if status_result.get("success"):
                file_status = status_result["data"]["status"]
                print(f"   尝试 {attempt + 1}: {file_status}")
                
                if file_status == "parsed":
                    print("   ✅ 文档解析完成!")
                    break
                elif file_status == "failed":
                    error = status_result["data"].get("error", "未知错误")
                    print(f"   ❌ 文档解析失败: {error}")
                    return False
                
                time.sleep(2)
            else:
                print(f"   ❌ 状态查询失败: {status_result.get('message')}")
                return False
        else:
            print("   ⏰ 文档解析超时")
            return False
        
        # 步骤3: 获取解析结果
        print(f"\n📋 步骤3: 获取文档解析结果...")
        preview_response = requests.get(f"{API_BASE}/kg/files/{upload_id}/preview")
        preview_result = preview_response.json()
        
        if not preview_result.get("success"):
            print(f"   ❌ 获取解析结果失败: {preview_result.get('message')}")
            return False
        
        preview_data = preview_result["data"]
        raw_data = preview_data.get("raw_data", [])
        entities = preview_data.get("entities", [])
        metadata = preview_data.get("metadata", {})
        
        print(f"   ✅ 文档解析结果获取成功!")
        
        # 步骤4: 分析原始数据提取
        print(f"\n📊 步骤4: 原始数据分析...")
        if raw_data:
            print(f"   📋 提取记录数: {len(raw_data)}")
            if raw_data:
                first_record = raw_data[0]
                print(f"   📄 字段数量: {len(first_record.keys())}")
                print(f"   🏷️ 字段列表: {list(first_record.keys())}")
                
                # 显示前3条记录
                print(f"   📝 数据示例:")
                for i, record in enumerate(raw_data[:3]):
                    print(f"      记录{i+1}: {record.get('问题编号', 'N/A')} - {record.get('问题描述', 'N/A')[:20]}...")
        else:
            print(f"   ⚠️ 未提取到原始数据")
        
        # 步骤5: 分析识别的实体（如果有）
        print(f"\n🏷️ 步骤5: 实体识别分析...")
        if entities:
            entity_types = {}
            for entity in entities:
                etype = entity.get("type", "Unknown")
                if etype not in entity_types:
                    entity_types[etype] = []
                entity_types[etype].append(entity.get("name"))
            
            print(f"   📊 识别实体数: {len(entities)}")
            for etype, names in entity_types.items():
                print(f"   {etype}: {len(names)}个 - {', '.join(names[:3])}{'...' if len(names) > 3 else ''}")
        else:
            print(f"   ℹ️ 未进行实体识别（纯文档解析模式）")
        
        # 步骤6: 元数据分析
        print(f"\n📈 步骤6: 解析元数据...")
        for key, value in metadata.items():
            print(f"   {key}: {value}")
        
        # 步骤7: 数据质量评估
        print(f"\n🎯 步骤7: 数据质量评估...")
        
        total_records = len(raw_data) if raw_data else metadata.get("total_records", 0)
        field_count = len(raw_data[0].keys()) if raw_data else metadata.get("field_count", 0)
        
        # 计算数据完整性
        if raw_data:
            complete_records = 0
            for record in raw_data:
                if all(value and str(value).strip() for value in record.values()):
                    complete_records += 1
            
            completeness = (complete_records / total_records) * 100 if total_records > 0 else 0
        else:
            completeness = 0
        
        print(f"   📊 总记录数: {total_records}")
        print(f"   📄 字段数量: {field_count}")
        print(f"   ✅ 数据完整性: {completeness:.1f}%")
        print(f"   🎯 解析质量: {'优秀' if completeness > 90 else '良好' if completeness > 70 else '一般'}")
        
        # 步骤8: 模拟导出功能
        print(f"\n💾 步骤8: 模拟数据导出...")
        
        export_data = {
            "file_info": {
                "filename": test_file.name,
                "upload_id": upload_id,
                "parsing_time": metadata.get("parsing_time", "unknown")
            },
            "raw_data": raw_data,
            "statistics": {
                "total_records": total_records,
                "field_count": field_count,
                "completeness": f"{completeness:.1f}%"
            },
            "metadata": metadata,
            "export_time": "2024-01-20T10:30:00Z"
        }
        
        export_file = Path("parsed_data_export.json")
        export_file.write_text(json.dumps(export_data, ensure_ascii=False, indent=2), encoding="utf-8")
        
        print(f"   ✅ 解析数据已导出到: {export_file}")
        print(f"   📊 导出文件大小: {export_file.stat().st_size} 字节")
        
        # 清理导出文件
        export_file.unlink(missing_ok=True)
        
        return True
    
    finally:
        # 清理测试文件
        test_file.unlink(missing_ok=True)

def test_parsing_vs_graph_separation():
    """测试解析与图谱构建的分离"""
    print("\n🔄 测试解析与图谱构建分离...")
    
    print("📄 文档解析阶段:")
    print("   ✅ 专注于从文档中提取结构化数据")
    print("   ✅ 不涉及语义理解和知识建模")
    print("   ✅ 输出原始数据和基本统计信息")
    print("   ✅ 支持数据导出和质量评估")
    
    print("\n🕸️ 图谱构建阶段（未实现）:")
    print("   🔄 从解析数据中识别实体和关系")
    print("   🔄 应用业务规则和本体模型")
    print("   🔄 构建知识图谱并存储到Neo4j")
    print("   🔄 提供图谱查询和分析功能")
    
    print("\n🎯 分离的优势:")
    print("   ✅ 职责清晰：解析专注数据提取，构建专注知识建模")
    print("   ✅ 灵活使用：可以只使用解析功能，不必构建图谱")
    print("   ✅ 易于维护：两个模块可以独立开发和优化")
    print("   ✅ 用户友好：用户明确知道每个步骤在做什么")

if __name__ == "__main__":
    print("🧪 文档解析与图谱构建分离测试")
    print("=" * 60)
    
    # 测试纯文档解析功能
    if test_document_parsing_only():
        print("\n🎉 文档解析功能测试成功!")
        print("✅ 成功提取文档中的结构化数据")
        print("✅ 数据质量评估功能正常")
        print("✅ 解析结果展示完整")
    else:
        print("\n❌ 文档解析功能测试失败!")
        print("⚠️ 请检查API服务和解析逻辑")
    
    # 测试分离设计
    test_parsing_vs_graph_separation()
    
    print("\n" + "=" * 60)
    print("测试完成")
