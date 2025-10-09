#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终验证8个Label - 确认所有问题都已解决
"""

import requests
import json

def test_api_with_8_labels():
    """测试API返回的8个Label分类"""
    print("🔍 测试API的8个Label分类...")
    
    try:
        response = requests.get("http://localhost:8000/kg/dictionary/entries?page_size=20", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("success") and "data" in data:
                total = data["data"].get("total", 0)
                entries = data["data"].get("entries", [])
                
                print(f"✅ API正常工作")
                print(f"📊 总数据量: {total} 条")
                
                # 统计分类分布
                category_stats = {}
                for entry in entries:
                    category = entry.get('category', '未知')
                    category_stats[category] = category_stats.get(category, 0) + 1
                
                print(f"📊 API返回的分类分布 (前20条样本):")
                for category, count in sorted(category_stats.items(), key=lambda x: x[1], reverse=True):
                    print(f"  {category}: {count} 条")
                
                # 检查每个标准Label的示例
                standard_labels = ['Symptom', 'Component', 'Tool', 'Process', 'TestCase', 'Metric', 'Material', 'Role']
                
                print(f"\n📋 8个Label示例:")
                for label in standard_labels:
                    examples = [entry for entry in entries if entry.get('category') == label]
                    if examples:
                        example = examples[0]
                        print(f"  {label}: {example.get('term', 'N/A')}")
                    else:
                        print(f"  {label}: (在前20条中未找到)")
                
                return True, total, category_stats
            else:
                print(f"❌ API返回错误: {data}")
                return False, 0, {}
        else:
            print(f"❌ HTTP错误: {response.status_code}")
            return False, 0, {}
            
    except Exception as e:
        print(f"❌ API测试失败: {e}")
        return False, 0, {}

def test_full_label_distribution():
    """测试完整的Label分布"""
    print("🔍 测试完整的Label分布...")
    
    try:
        # 获取所有数据来统计完整分布
        response = requests.get("http://localhost:8000/kg/dictionary/entries?page_size=10000", timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("success") and "data" in data:
                entries = data["data"].get("entries", [])
                
                # 统计完整分类分布
                full_category_stats = {}
                for entry in entries:
                    category = entry.get('category', '未知')
                    full_category_stats[category] = full_category_stats.get(category, 0) + 1
                
                print(f"📊 完整Label分布:")
                
                # 标准8个Label
                standard_labels = {
                    'Symptom': '症状',
                    'Component': '组件', 
                    'Tool': '工具',
                    'Process': '流程',
                    'TestCase': '测试用例',
                    'Metric': '性能指标',
                    'Material': '物料',
                    'Role': '角色'
                }
                
                total_standard = 0
                for label, chinese_name in standard_labels.items():
                    count = full_category_stats.get(label, 0)
                    total_standard += count
                    print(f"  {label} ({chinese_name}): {count} 条")
                
                # 检查是否有非标准分类
                non_standard = {k: v for k, v in full_category_stats.items() if k not in standard_labels}
                
                if non_standard:
                    print(f"\n⚠️ 非标准分类:")
                    for cat, count in non_standard.items():
                        print(f"  {cat}: {count} 条")
                else:
                    print(f"\n✅ 所有数据都使用标准8个Label")
                
                print(f"\n📊 总计: {total_standard} 条标准分类数据")
                
                return True, full_category_stats, len(entries)
            else:
                print(f"❌ 获取完整数据失败: {data}")
                return False, {}, 0
        else:
            print(f"❌ HTTP错误: {response.status_code}")
            return False, {}, 0
            
    except Exception as e:
        print(f"❌ 完整分布测试失败: {e}")
        return False, {}, 0

def test_search_by_category():
    """测试按分类搜索"""
    print("🔍 测试按分类搜索...")
    
    standard_labels = ['Symptom', 'Component', 'Tool', 'Process', 'TestCase', 'Metric', 'Material', 'Role']
    
    for label in standard_labels:
        try:
            # 这里假设API支持按category过滤，如果不支持可以跳过
            response = requests.get(f"http://localhost:8000/kg/dictionary/entries?search={label}&page_size=3", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    entries = data["data"].get("entries", [])
                    # 检查返回的结果是否包含该分类
                    matching_entries = [e for e in entries if e.get('category') == label]
                    print(f"  {label}: 搜索到 {len(entries)} 条，匹配分类 {len(matching_entries)} 条")
                else:
                    print(f"  {label}: 搜索失败")
            else:
                print(f"  {label}: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"  {label}: 异常 - {e}")

def generate_final_verification_report():
    """生成最终验证报告"""
    print("\n" + "=" * 60)
    print("📊 最终验证报告 - 8个Label分类系统")
    print("=" * 60)
    
    # 1. 测试API基本功能
    api_ok, total, sample_stats = test_api_with_8_labels()
    
    # 2. 测试完整分布
    if api_ok:
        full_ok, full_stats, full_total = test_full_label_distribution()
    else:
        full_ok, full_stats, full_total = False, {}, 0
    
    # 3. 测试搜索功能
    if api_ok:
        test_search_by_category()
    
    print("\n" + "=" * 60)
    print("🎯 最终验证结果:")
    print("=" * 60)
    
    print(f"API服务状态: {'✅ 正常' if api_ok else '❌ 异常'}")
    print(f"数据总量: {total} 条")
    print(f"完整分布获取: {'✅ 成功' if full_ok else '❌ 失败'}")
    
    if full_ok and full_stats:
        # 检查8个Label是否都有数据
        standard_labels = ['Symptom', 'Component', 'Tool', 'Process', 'TestCase', 'Metric', 'Material', 'Role']
        all_labels_present = all(label in full_stats and full_stats[label] > 0 for label in standard_labels)
        
        print(f"8个Label完整性: {'✅ 完整' if all_labels_present else '⚠️ 不完整'}")
        
        # 检查是否有非标准分类
        non_standard = {k: v for k, v in full_stats.items() if k not in standard_labels}
        print(f"分类标准化: {'✅ 完全标准化' if not non_standard else '⚠️ 存在非标准分类'}")
        
        if api_ok and full_ok and all_labels_present and not non_standard and total > 1000:
            print(f"\n🎉 系统验证完全成功!")
            print(f"✅ 词典数据: {total} 条")
            print(f"✅ 8个Label: 完整覆盖")
            print(f"✅ 分类标准化: 100%")
            print(f"✅ API服务: 正常工作")
            print(f"✅ 前端显示: 应该正确")
            
            print(f"\n📊 最终Label分布:")
            label_names = {
                'Symptom': '症状', 'Component': '组件', 'Tool': '工具', 'Process': '流程',
                'TestCase': '测试用例', 'Metric': '性能指标', 'Material': '物料', 'Role': '角色'
            }
            
            for label in standard_labels:
                count = full_stats.get(label, 0)
                chinese_name = label_names[label]
                percentage = (count / total * 100) if total > 0 else 0
                print(f"  {label} ({chinese_name}): {count} 条 ({percentage:.1f}%)")
            
            print(f"\n🌐 前端验证:")
            print(f"   访问: http://localhost:5173")
            print(f"   检查: 词典管理页面")
            print(f"   确认: 类别字段显示8个标准Label")
            print(f"   验证: 总数显示1124条")
            
        else:
            print(f"\n⚠️ 系统仍有问题需要解决")
            if not api_ok:
                print(f"❌ API服务异常")
            if not all_labels_present:
                print(f"❌ 8个Label不完整")
            if non_standard:
                print(f"❌ 存在非标准分类: {list(non_standard.keys())}")
            if total <= 1000:
                print(f"❌ 数据量不足: {total}")
    else:
        print(f"\n❌ 无法获取完整验证数据")

def main():
    """主函数"""
    print("🚀 最终验证8个Label分类系统")
    print("=" * 50)
    
    generate_final_verification_report()

if __name__ == "__main__":
    main()
