#!/usr/bin/env python3
"""
测试Schema API端点
"""

import requests
import json

BASE_URL = "http://47.108.152.16"

def test_api(endpoint, description):
    """测试API端点"""
    print(f"\n{'='*60}")
    print(f"📌 {description}")
    print(f"{'='*60}")
    print(f"🌐 URL: {BASE_URL}{endpoint}")
    
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
        print(f"✅ 状态码: {response.status_code}")
        print(f"📝 响应内容长度: {len(response.text)} 字节")
        print(f"📝 响应内容: {response.text[:500]}")

        if response.status_code == 200:
            if response.text:
                data = response.json()
                print(f"📊 响应数据:")
                print(json.dumps(data, indent=2, ensure_ascii=False))
                return True
            else:
                print("⚠️ 响应为空")
                return False
        else:
            print(f"❌ 请求失败: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("🚀 开始测试Schema API端点...")
    
    tests = [
        ("/kg/dictionary/stats", "词典统计"),
        ("/kg/dictionary/categories", "分类详情"),
        ("/kg/entities", "实体统计"),
        ("/kg/relations", "关系统计"),
        ("/kg/stats", "图谱总体统计"),
    ]
    
    results = []
    for endpoint, description in tests:
        success = test_api(endpoint, description)
        results.append((description, success))
    
    # 总结
    print(f"\n{'='*60}")
    print("📊 测试总结")
    print(f"{'='*60}")
    
    for desc, success in results:
        status = "✅ 通过" if success else "❌ 失败"
        print(f"{status} - {desc}")
    
    passed = sum(1 for _, s in results if s)
    total = len(results)
    print(f"\n总计: {passed}/{total} 通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！")
    else:
        print(f"\n⚠️ {total - passed} 个测试失败")

if __name__ == "__main__":
    main()

