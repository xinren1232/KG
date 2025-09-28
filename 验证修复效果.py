#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证修复效果 - 检查词典数据修复和前端显示是否正常
"""

import requests
import json
from pathlib import Path

def test_api_data_quality():
    """测试API数据质量"""
    print("🔍 测试API数据质量...")
    
    try:
        response = requests.get("http://localhost:8000/kg/dictionary/entries?page_size=5", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("success") and "data" in data:
                total = data["data"].get("total", 0)
                entries = data["data"].get("entries", [])
                
                print(f"✅ API正常工作")
                print(f"📊 总数据量: {total} 条")
                print(f"📊 返回样本: {len(entries)} 条")
                
                # 检查数据质量
                for i, entry in enumerate(entries):
                    print(f"\n📋 样本 {i+1}:")
                    print(f"  术语: '{entry.get('term', 'N/A')}'")
                    print(f"  类别: '{entry.get('category', 'N/A')}'")
                    
                    aliases = entry.get('aliases', [])
                    if isinstance(aliases, list):
                        print(f"  别名: {aliases} ({len(aliases)} 个)")
                    else:
                        print(f"  别名: {aliases} (格式错误)")
                    
                    tags = entry.get('tags', [])
                    if isinstance(tags, list):
                        print(f"  标签: {tags} ({len(tags)} 个)")
                    else:
                        print(f"  标签: {tags} (格式错误)")
                    
                    desc = entry.get('description', '')
                    print(f"  描述: '{desc[:50]}...' ({len(desc)} 字符)")
                
                return True, total, entries
            else:
                print(f"❌ API返回错误: {data}")
                return False, 0, []
        else:
            print(f"❌ HTTP错误: {response.status_code}")
            return False, 0, []
            
    except Exception as e:
        print(f"❌ API测试失败: {e}")
        return False, 0, []

def check_data_file_quality():
    """检查数据文件质量"""
    print("📁 检查数据文件质量...")
    
    data_file = Path("api/data/dictionary.json")
    
    if not data_file.exists():
        print(f"❌ 数据文件不存在: {data_file}")
        return False
    
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"📊 文件数据量: {len(data)} 条")
        
        # 检查数据质量
        quality_stats = {
            'valid_terms': 0,
            'has_category': 0,
            'has_aliases': 0,
            'has_tags': 0,
            'has_description': 0,
            'format_errors': 0
        }
        
        for item in data[:10]:  # 检查前10条
            if isinstance(item, dict):
                # 检查术语
                term = item.get('term', '').strip()
                if term:
                    quality_stats['valid_terms'] += 1
                
                # 检查类别
                category = item.get('category', '').strip()
                if category:
                    quality_stats['has_category'] += 1
                
                # 检查别名
                aliases = item.get('aliases', [])
                if isinstance(aliases, list) and aliases:
                    quality_stats['has_aliases'] += 1
                    # 检查别名格式
                    for alias in aliases:
                        if not isinstance(alias, str) or '[' in alias or ']' in alias:
                            quality_stats['format_errors'] += 1
                            break
                
                # 检查标签
                tags = item.get('tags', [])
                if isinstance(tags, list) and tags:
                    quality_stats['has_tags'] += 1
                    # 检查标签格式
                    for tag in tags:
                        if not isinstance(tag, str) or '[' in tag or ']' in tag:
                            quality_stats['format_errors'] += 1
                            break
                
                # 检查描述
                description = item.get('description', '').strip()
                if description:
                    quality_stats['has_description'] += 1
        
        print(f"📊 数据质量统计 (前10条):")
        print(f"  有效术语: {quality_stats['valid_terms']}/10")
        print(f"  有类别: {quality_stats['has_category']}/10")
        print(f"  有别名: {quality_stats['has_aliases']}/10")
        print(f"  有标签: {quality_stats['has_tags']}/10")
        print(f"  有描述: {quality_stats['has_description']}/10")
        print(f"  格式错误: {quality_stats['format_errors']} 个")
        
        return quality_stats['format_errors'] == 0
        
    except Exception as e:
        print(f"❌ 检查数据文件失败: {e}")
        return False

def test_search_functionality():
    """测试搜索功能"""
    print("🔍 测试搜索功能...")
    
    search_terms = ["显示屏", "电池", "传感器", "BTB", "OLED"]
    
    for term in search_terms:
        try:
            response = requests.get(f"http://localhost:8000/kg/dictionary/entries?search={term}&page_size=3", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    entries = data["data"].get("entries", [])
                    print(f"  '{term}': {len(entries)} 条结果")
                    
                    for entry in entries[:2]:
                        term_name = entry.get('term', 'N/A')
                        category = entry.get('category', 'N/A')
                        print(f"    - {term_name} ({category})")
                else:
                    print(f"  '{term}': 搜索失败")
            else:
                print(f"  '{term}': HTTP {response.status_code}")
                
        except Exception as e:
            print(f"  '{term}': 异常 - {e}")

def generate_verification_summary():
    """生成验证总结"""
    print("\n" + "=" * 60)
    print("📊 修复效果验证总结")
    print("=" * 60)
    
    # 1. 检查数据文件
    file_ok = check_data_file_quality()
    
    # 2. 测试API
    api_ok, total, samples = test_api_data_quality()
    
    # 3. 测试搜索
    if api_ok:
        test_search_functionality()
    
    print("\n" + "=" * 60)
    print("🎯 验证结果:")
    print(f"数据文件质量: {'✅ 良好' if file_ok else '❌ 有问题'}")
    print(f"API服务状态: {'✅ 正常' if api_ok else '❌ 异常'}")
    print(f"数据总量: {total} 条")
    
    if api_ok and file_ok and total > 1000:
        print("\n✅ 修复效果验证成功!")
        print("📊 词典数据格式已修复")
        print("🔧 API服务正常工作")
        print("🌐 前端应该能正确显示数据")
        print("\n💡 请访问前端验证:")
        print("   http://localhost:5173")
        print("   检查词典管理页面是否正确显示:")
        print("   - 术语名称不为空")
        print("   - 类别正确显示")
        print("   - 别名和标签格式正常")
        print("   - 总数显示1124条")
    else:
        print("\n⚠️ 仍有问题需要解决")
        if not file_ok:
            print("❌ 数据文件格式仍有问题")
        if not api_ok:
            print("❌ API服务异常")
        if total <= 1000:
            print(f"❌ 数据量不足: {total}")

def main():
    """主函数"""
    print("🚀 验证修复效果")
    print("=" * 40)
    
    generate_verification_summary()

if __name__ == "__main__":
    main()
