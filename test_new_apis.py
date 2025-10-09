#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试新的API端点
"""

import requests
import json

BASE_URL = "http://47.108.152.16:8000"

def test_validate_relation():
    """测试关系验证"""
    print("=" * 80)
    print("1. 测试关系验证API")
    print("=" * 80)
    
    # 测试有效的关系
    valid_relation = {
        "relation_type": "RESOLVED_BY",
        "source": {
            "name": "电池盖裂纹",
            "category": "Symptom"
        },
        "target": {
            "name": "更换治具并清洁",
            "category": "Solution"
        },
        "props": {
            "confidence": 0.9,
            "evidence": "更换治具后，裂纹不良率从5%降至0.1%",
            "source": "manual",
            "effectiveness": 0.95,
            "risk": "low",
            "cost_level": "M"
        }
    }
    
    response = requests.post(f"{BASE_URL}/kg/relations/validate", json=valid_relation)
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
    
    # 测试无效的关系（类型不匹配）
    print("\n测试无效关系（类型不匹配）:")
    invalid_relation = {
        "relation_type": "RESOLVED_BY",
        "source": {
            "name": "电池盖裂纹",
            "category": "Symptom"
        },
        "target": {
            "name": "摄像头模组",
            "category": "Component"  # 错误：应该是Solution
        },
        "props": {
            "confidence": 0.9,
            "evidence": "测试证据，至少需要10个字符"
        }
    }
    
    response = requests.post(f"{BASE_URL}/kg/relations/validate", json=invalid_relation)
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")


def test_import_relations():
    """测试批量导入关系"""
    print("\n" + "=" * 80)
    print("2. 测试批量导入关系API")
    print("=" * 80)
    
    batch = {
        "relations": [
            {
                "relation_type": "CAUSES",
                "source": {
                    "name": "治具颗粒杂质",
                    "category": "RootCause"
                },
                "target": {
                    "name": "电池盖裂纹",
                    "category": "Symptom"
                },
                "props": {
                    "confidence": 0.85,
                    "evidence": "治具上的颗粒杂质导致压合时局部受力不均，引发裂纹",
                    "source": "test_api",
                    "severity": "P1",
                    "phase": "DVT"
                }
            }
        ]
    }
    
    response = requests.post(f"{BASE_URL}/kg/relations/import", json=batch)
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")


def test_relation_stats():
    """测试关系统计"""
    print("\n" + "=" * 80)
    print("3. 测试关系统计API")
    print("=" * 80)
    
    response = requests.get(f"{BASE_URL}/kg/relations/stats")
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")


def test_diagnose():
    """测试故障诊断"""
    print("\n" + "=" * 80)
    print("4. 测试故障诊断API")
    print("=" * 80)
    
    response = requests.get(f"{BASE_URL}/kg/diagnose", params={
        "symptom": "电池盖裂纹",
        "max_depth": 3,
        "min_confidence": 0.6
    })
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")


def test_prevention():
    """测试预防措施"""
    print("\n" + "=" * 80)
    print("5. 测试预防措施API")
    print("=" * 80)
    
    response = requests.get(f"{BASE_URL}/kg/prevent", params={
        "symptom": "电池盖裂纹",
        "min_confidence": 0.6
    })
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")


def test_test_path():
    """测试测试路径"""
    print("\n" + "=" * 80)
    print("6. 测试测试路径API")
    print("=" * 80)
    
    response = requests.get(f"{BASE_URL}/kg/test-path", params={
        "target": "摄像头模组",
        "target_category": "Component",
        "min_confidence": 0.6
    })
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")


def test_dependencies():
    """测试组件依赖"""
    print("\n" + "=" * 80)
    print("7. 测试组件依赖API")
    print("=" * 80)
    
    response = requests.get(f"{BASE_URL}/kg/dependencies", params={
        "component": "摄像头模组",
        "direction": "both",
        "max_depth": 2,
        "min_confidence": 0.6
    })
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")


if __name__ == "__main__":
    print("开始测试新的API端点...")
    print("服务器地址:", BASE_URL)
    print()
    
    try:
        # 测试验证API
        test_validate_relation()
        
        # 测试导入API
        test_import_relations()
        
        # 测试统计API
        test_relation_stats()
        
        # 测试诊断API
        test_diagnose()
        
        # 测试预防API
        test_prevention()
        
        # 测试测试路径API
        test_test_path()
        
        # 测试依赖API
        test_dependencies()
        
        print("\n" + "=" * 80)
        print("✅ 所有测试完成")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()

