#!/usr/bin/env python3
"""
完整测试Schema功能
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
        
        if response.status_code == 200:
            data = response.json()
            print(f"📊 响应数据:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            return True, data
        else:
            print(f"❌ 请求失败: {response.text[:200]}")
            return False, None
    except Exception as e:
        print(f"❌ 错误: {str(e)}")
        return False, None

def main():
    print("🚀 开始测试Schema功能...")
    print(f"🌐 服务器: {BASE_URL}")
    
    # 测试API端点
    tests = [
        ("/api/health", "健康检查"),
        ("/api/kg/dictionary/stats", "词典统计"),
        ("/api/kg/dictionary/categories", "分类详情"),
        ("/api/kg/entities", "实体统计"),
        ("/api/kg/relations", "关系统计"),
        ("/api/kg/stats", "图谱总体统计"),
    ]
    
    results = []
    data_summary = {}
    
    for endpoint, description in tests:
        success, data = test_api(endpoint, description)
        results.append((description, success))
        if success and data:
            data_summary[description] = data
    
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
    
    # 数据摘要
    if data_summary:
        print(f"\n{'='*60}")
        print("📈 数据摘要")
        print(f"{'='*60}")
        
        if "词典统计" in data_summary:
            stats = data_summary["词典统计"].get("data", {})
            print(f"\n📚 词典数据:")
            print(f"  术语总数: {stats.get('totalTerms', 0)}")
            print(f"  分类数量: {stats.get('totalCategories', 0)}")
            print(f"  标签数量: {stats.get('totalTags', 0)}")
            print(f"  别名数量: {stats.get('totalAliases', 0)}")
        
        if "图谱总体统计" in data_summary:
            graph_stats = data_summary["图谱总体统计"].get("data", {})
            print(f"\n🕸️ 图谱数据:")
            print(f"  节点总数: {graph_stats.get('total_nodes', 0)}")
            print(f"  关系总数: {graph_stats.get('total_relationships', 0)}")
        
        if "实体统计" in data_summary:
            entities = data_summary["实体统计"].get("data", [])
            print(f"\n📦 实体类型 (Top 5):")
            for i, entity in enumerate(entities[:5], 1):
                print(f"  {i}. {entity.get('label', 'N/A')}: {entity.get('count', 0)}")
        
        if "关系统计" in data_summary:
            relations = data_summary["关系统计"].get("data", [])
            print(f"\n🔗 关系类型 (Top 5):")
            for i, relation in enumerate(relations[:5], 1):
                print(f"  {i}. {relation.get('type', 'N/A')}: {relation.get('count', 0)}")
        
        if "分类详情" in data_summary:
            categories = data_summary["分类详情"].get("data", [])
            print(f"\n📂 分类详情 (Top 5):")
            for i, cat in enumerate(categories[:5], 1):
                print(f"  {i}. {cat.get('name', 'N/A')}: {cat.get('termCount', 0)} 术语")
    
    # 最终结论
    print(f"\n{'='*60}")
    if passed == total:
        print("🎉 所有测试通过！Schema功能正常工作！")
        print("\n✅ 下一步:")
        print("  1. 访问 http://47.108.152.16/")
        print("  2. 进入「系统管理」页面")
        print("  3. 点击「词典Schema」或「图谱Schema」标签")
        print("  4. 查看完整的Schema设计和统计信息")
    else:
        print(f"⚠️ {total - passed} 个测试失败，请检查配置")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()

