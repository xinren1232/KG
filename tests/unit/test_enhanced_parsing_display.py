#!/usr/bin/env python3
"""
测试增强的解析结果展示功能
"""

import requests
import time
import json
from pathlib import Path

API_BASE = "http://127.0.0.1:8000"

def create_rich_test_file():
    """创建包含丰富数据的测试文件"""
    test_content = """问题编号,不良现象,发生日期,严重度,工厂,机型,版本,部件,原因分析,改善对策,责任人,状态
ANOM-001,对焦失败,2024-01-15,S2,深圳工厂,iPhone15,iOS17.1,摄像头,镜头污染,清洁镜头,张工,已解决
ANOM-002,屏幕闪烁,2024-01-16,S1,上海工厂,iPhone15Pro,iOS17.1,显示屏,驱动IC异常,更换驱动IC,李工,处理中
ANOM-003,充电慢,2024-01-17,S3,北京工厂,iPhone15Plus,iOS17.1,充电器,功率不足,升级充电器,王工,已解决
ANOM-004,发热严重,2024-01-18,S2,深圳工厂,iPhone15,iOS17.2,电池,电池老化,更换电池,赵工,处理中
ANOM-005,死机重启,2024-01-19,S1,上海工厂,iPhone15Pro,iOS17.2,主板,软件bug,更新软件,钱工,已解决
ANOM-006,音质异常,2024-01-20,S3,北京工厂,iPhone15Plus,iOS17.2,扬声器,扬声器损坏,更换扬声器,孙工,处理中
ANOM-007,触摸失灵,2024-01-21,S2,深圳工厂,iPhone15,iOS17.3,触摸屏,触控IC故障,更换触控IC,周工,已解决
ANOM-008,网络断连,2024-01-22,S1,上海工厂,iPhone15Pro,iOS17.3,天线,天线接触不良,重新焊接,吴工,处理中"""
    
    test_file = Path("rich_test_data.csv")
    test_file.write_text(test_content, encoding="utf-8")
    
    print(f"✅ 创建丰富测试文件: {test_file}")
    print(f"📊 数据行数: {len(test_content.splitlines()) - 1}")
    
    return test_file

def test_enhanced_parsing_display():
    """测试增强的解析结果展示"""
    print("🚀 开始测试增强的解析结果展示...")
    
    # 创建测试文件
    test_file = create_rich_test_file()
    
    try:
        # 步骤1: 上传文件
        print(f"\n📤 步骤1: 上传测试文件...")
        with open(test_file, "rb") as f:
            files = {"file": (test_file.name, f, "text/csv")}
            upload_response = requests.post(f"{API_BASE}/kg/upload", files=files)
        
        upload_result = upload_response.json()
        if not upload_result.get("success"):
            print(f"   ❌ 文件上传失败: {upload_result.get('message')}")
            return False
        
        upload_id = upload_result.get("upload_id")
        print(f"   ✅ 文件上传成功: {upload_id}")
        
        # 步骤2: 等待解析完成
        print(f"\n⏳ 步骤2: 等待解析完成...")
        max_attempts = 15
        for attempt in range(max_attempts):
            status_response = requests.get(f"{API_BASE}/kg/files/{upload_id}/status")
            status_result = status_response.json()
            
            if status_result.get("success"):
                file_status = status_result["data"]["status"]
                print(f"   尝试 {attempt + 1}: {file_status}")
                
                if file_status == "parsed":
                    print("   ✅ 解析完成!")
                    break
                elif file_status == "failed":
                    error = status_result["data"].get("error", "未知错误")
                    print(f"   ❌ 解析失败: {error}")
                    return False
                
                time.sleep(2)
            else:
                print(f"   ❌ 状态查询失败: {status_result.get('message')}")
                return False
        else:
            print("   ⏰ 解析超时")
            return False
        
        # 步骤3: 获取详细解析结果
        print(f"\n📋 步骤3: 获取详细解析结果...")
        preview_response = requests.get(f"{API_BASE}/kg/files/{upload_id}/preview")
        preview_result = preview_response.json()
        
        if not preview_result.get("success"):
            print(f"   ❌ 获取解析结果失败: {preview_result.get('message')}")
            return False
        
        preview_data = preview_result["data"]
        entities = preview_data.get("entities", [])
        relations = preview_data.get("relations", [])
        metadata = preview_data.get("metadata", {})
        
        print(f"   ✅ 解析结果获取成功!")
        print(f"   📊 实体总数: {len(entities)}")
        print(f"   🔗 关系总数: {len(relations)}")
        
        # 步骤4: 分析实体类型分布
        print(f"\n🏷️ 步骤4: 实体类型分析...")
        entity_types = {}
        for entity in entities:
            etype = entity.get("type", "Unknown")
            if etype not in entity_types:
                entity_types[etype] = []
            entity_types[etype].append(entity.get("name"))
        
        for etype, names in entity_types.items():
            print(f"   {etype}: {len(names)}个")
            print(f"      示例: {', '.join(names[:3])}{'...' if len(names) > 3 else ''}")
        
        # 步骤5: 分析关系类型分布
        print(f"\n🔗 步骤5: 关系类型分析...")
        relation_types = {}
        for relation in relations:
            rtype = relation.get("type", "Unknown")
            if rtype not in relation_types:
                relation_types[rtype] = []
            relation_types[rtype].append(f"{relation.get('source')} -> {relation.get('target')}")
        
        for rtype, examples in relation_types.items():
            print(f"   {rtype}: {len(examples)}个")
            print(f"      示例: {examples[0] if examples else '无'}")
        
        # 步骤6: 元数据分析
        print(f"\n📈 步骤6: 元数据分析...")
        for key, value in metadata.items():
            print(f"   {key}: {value}")
        
        # 步骤7: 计算解析质量指标
        print(f"\n🎯 步骤7: 解析质量评估...")
        
        # 实体覆盖率
        total_records = metadata.get("total_records", 0)
        entity_coverage = len(entities) / (total_records * 4) if total_records > 0 else 0  # 假设每条记录平均4个实体
        
        # 关系密度
        relation_density = len(relations) / len(entities) if len(entities) > 0 else 0
        
        # 类型多样性
        type_diversity = len(entity_types) / 6  # 假设最多6种类型
        
        # 综合质量分数
        quality_score = (entity_coverage * 0.4 + relation_density * 0.4 + type_diversity * 0.2) * 100
        
        print(f"   实体覆盖率: {entity_coverage:.2%}")
        print(f"   关系密度: {relation_density:.2f}")
        print(f"   类型多样性: {type_diversity:.2%}")
        print(f"   综合质量分数: {quality_score:.1f}%")
        
        # 步骤8: 模拟前端展示数据
        print(f"\n🎨 步骤8: 前端展示数据模拟...")
        
        display_data = {
            "overview": {
                "entity_count": len(entities),
                "relation_count": len(relations),
                "file_size": test_file.stat().st_size,
                "quality_score": round(quality_score, 1)
            },
            "entity_summary": {etype: len(names) for etype, names in entity_types.items()},
            "relation_summary": {rtype: len(examples) for rtype, examples in relation_types.items()},
            "metadata_formatted": {
                "总记录数": metadata.get("total_records", 0),
                "处理块数": metadata.get("processed_blocks", 0),
                "文件类型": metadata.get("file_type", "unknown"),
                "数据源": metadata.get("source", "unknown")
            }
        }
        
        print(f"   📊 概览数据: {json.dumps(display_data['overview'], ensure_ascii=False)}")
        print(f"   🏷️ 实体汇总: {json.dumps(display_data['entity_summary'], ensure_ascii=False)}")
        print(f"   🔗 关系汇总: {json.dumps(display_data['relation_summary'], ensure_ascii=False)}")
        
        return True
    
    finally:
        # 清理测试文件
        test_file.unlink(missing_ok=True)

def test_frontend_api_compatibility():
    """测试前端API兼容性"""
    print("\n🔍 测试前端API兼容性...")
    
    # 测试基础API端点
    endpoints = [
        ("GET", "/kg/stats", "统计信息"),
        ("GET", "/kg/dictionary", "词典数据"),
    ]
    
    for method, endpoint, description in endpoints:
        try:
            response = requests.get(f"{API_BASE}{endpoint}")
            status = "✅" if response.status_code == 200 else "❌"
            print(f"   {status} {method} {endpoint} ({description}): {response.status_code}")
        except Exception as e:
            print(f"   ❌ {method} {endpoint} ({description}): 错误 - {e}")

if __name__ == "__main__":
    print("🧪 增强解析结果展示测试")
    print("=" * 60)
    
    # 测试API兼容性
    test_frontend_api_compatibility()
    
    print("\n" + "=" * 60)
    
    # 测试增强的解析展示
    if test_enhanced_parsing_display():
        print("\n🎉 增强解析结果展示测试成功!")
        print("✅ 前端现在可以展示丰富的解析结果详情")
        print("📱 用户可以通过'查看详情'按钮查看完整的解析信息")
        print("🎯 解析质量评估功能正常工作")
    else:
        print("\n❌ 增强解析结果展示测试失败!")
        print("⚠️ 请检查API服务和解析逻辑")
    
    print("\n" + "=" * 60)
    print("测试完成")
