#!/usr/bin/env python3
"""
测试Excel文件解析功能
"""

import pandas as pd
import requests
import time
from pathlib import Path

API_BASE = "http://127.0.0.1:8000"

def create_test_excel():
    """创建测试Excel文件"""
    data = {
        "问题编号": ["ANOM-001", "ANOM-002", "ANOM-003", "ANOM-004", "ANOM-005"],
        "不良现象": ["对焦失败", "屏幕闪烁", "充电慢", "发热严重", "死机重启"],
        "发生日期": ["2024-01-15", "2024-01-16", "2024-01-17", "2024-01-18", "2024-01-19"],
        "严重度": ["S2", "S1", "S3", "S2", "S1"],
        "工厂": ["深圳工厂", "上海工厂", "北京工厂", "深圳工厂", "上海工厂"],
        "机型": ["iPhone15", "iPhone15Pro", "iPhone15Plus", "iPhone15", "iPhone15Pro"],
        "版本": ["iOS17.1", "iOS17.1", "iOS17.1", "iOS17.2", "iOS17.2"],
        "部件": ["摄像头", "显示屏", "充电器", "电池", "主板"],
        "原因分析": ["镜头污染", "驱动IC异常", "功率不足", "电池老化", "软件bug"],
        "改善对策": ["清洁镜头", "更换驱动IC", "升级充电器", "更换电池", "更新软件"]
    }
    
    df = pd.DataFrame(data)
    excel_file = Path("test_quality_data.xlsx")
    df.to_excel(excel_file, index=False, sheet_name="来料问题洗后版")
    
    print(f"✅ 创建测试Excel文件: {excel_file}")
    print(f"📊 数据行数: {len(df)}")
    print(f"📋 列名: {list(df.columns)}")
    
    return excel_file

def test_excel_parsing():
    """测试Excel文件解析"""
    print("🚀 开始测试Excel文件解析...")
    
    # 创建测试文件
    excel_file = create_test_excel()
    
    try:
        # 上传Excel文件
        print(f"\n📤 上传Excel文件...")
        with open(excel_file, "rb") as f:
            files = {"file": (excel_file.name, f, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
            response = requests.post(f"{API_BASE}/kg/upload", files=files)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                upload_id = result.get("upload_id")
                print(f"   ✅ Excel文件上传成功: {upload_id}")
                
                # 等待解析完成
                print(f"\n⏳ 等待Excel解析完成...")
                max_wait = 30
                wait_time = 0
                
                while wait_time < max_wait:
                    status_response = requests.get(f"{API_BASE}/kg/files/{upload_id}/status")
                    if status_response.status_code == 200:
                        status_result = status_response.json()
                        if status_result.get("success"):
                            file_status = status_result["data"]["status"]
                            print(f"   📊 当前状态: {file_status}")
                            
                            if file_status == "parsed":
                                print("   ✅ Excel解析完成!")
                                break
                            elif file_status == "failed":
                                error = status_result["data"].get("error", "未知错误")
                                print(f"   ❌ Excel解析失败: {error}")
                                return
                    
                    time.sleep(2)
                    wait_time += 2
                
                # 获取解析结果
                print(f"\n📋 获取Excel解析结果...")
                preview_response = requests.get(f"{API_BASE}/kg/files/{upload_id}/preview")
                
                if preview_response.status_code == 200:
                    preview_result = preview_response.json()
                    if preview_result.get("success"):
                        preview_data = preview_result["data"]
                        
                        entities = preview_data.get("entities", [])
                        relations = preview_data.get("relations", [])
                        metadata = preview_data.get("metadata", {})
                        
                        print(f"   ✅ Excel解析结果:")
                        print(f"   📊 实体数量: {len(entities)}")
                        print(f"   🔗 关系数量: {len(relations)}")
                        print(f"   📈 处理记录: {metadata.get('total_records', 0)}")
                        print(f"   🏷️ 实体类型分布: {metadata.get('entity_types', {})}")
                        
                        # 显示实体详情
                        if entities:
                            print(f"\n   🏷️ 实体详情:")
                            entity_types = {}
                            for entity in entities:
                                etype = entity.get("type")
                                if etype not in entity_types:
                                    entity_types[etype] = []
                                entity_types[etype].append(entity.get("name"))
                            
                            for etype, names in entity_types.items():
                                print(f"      {etype}: {', '.join(names[:5])}{'...' if len(names) > 5 else ''}")
                        
                        # 显示关系详情
                        if relations:
                            print(f"\n   🔗 关系详情:")
                            for i, relation in enumerate(relations[:10]):
                                print(f"      {i+1}. {relation.get('source')} --{relation.get('type')}--> {relation.get('target')}")
                        
                        return True
                    else:
                        print(f"   ❌ 获取解析结果失败: {preview_result.get('message')}")
                else:
                    print(f"   ❌ 解析结果请求失败: {preview_response.status_code}")
            else:
                print(f"   ❌ Excel文件上传失败: {result.get('message')}")
        else:
            print(f"   ❌ 上传请求失败: {response.status_code}")
            print(f"   📄 响应内容: {response.text}")
    
    finally:
        # 清理测试文件
        excel_file.unlink(missing_ok=True)
    
    return False

if __name__ == "__main__":
    if test_excel_parsing():
        print("\n🎉 Excel文件解析测试成功!")
    else:
        print("\n❌ Excel文件解析测试失败!")
