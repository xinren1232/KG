#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复词典数据格式 - 清理aliases和tags字段的格式错误
"""

import json
import re
from pathlib import Path
from datetime import datetime

def clean_list_field(field_value):
    """清理列表字段，去除嵌套字符串和格式错误"""
    if not field_value:
        return []
    
    if isinstance(field_value, str):
        # 如果是字符串，尝试解析
        field_value = [field_value]
    
    if not isinstance(field_value, list):
        return []
    
    cleaned_items = set()  # 使用set去重
    
    for item in field_value:
        if not item or not isinstance(item, str):
            continue
        
        # 清理单个项目
        cleaned_item = clean_single_item(item)
        if cleaned_item:
            cleaned_items.update(cleaned_item)
    
    return list(cleaned_items)

def clean_single_item(item):
    """清理单个项目"""
    if not item or not isinstance(item, str):
        return []
    
    # 移除多余的引号和括号
    item = item.strip()
    
    # 处理各种分隔符
    separators = [';', ',', '、', '，', '；']
    items = [item]
    
    for sep in separators:
        new_items = []
        for it in items:
            new_items.extend([x.strip() for x in it.split(sep) if x.strip()])
        items = new_items
    
    # 清理每个项目
    cleaned = []
    for it in items:
        # 移除各种括号和引号
        it = re.sub(r'^[\[\(\'"]+', '', it)
        it = re.sub(r'[\]\)\'"]+$', '', it)
        it = re.sub(r'^[\[\(\'"]+', '', it)  # 再次清理
        it = re.sub(r'[\]\)\'"]+$', '', it)
        
        # 移除包含特殊字符的无效项
        if re.search(r'[\[\]{}()"\']', it):
            continue
        
        # 移除空项和过短项
        it = it.strip()
        if len(it) > 1 and not re.match(r'^[^\w\u4e00-\u9fff]+$', it):
            cleaned.append(it)
    
    return cleaned

def fix_dictionary_data():
    """修复词典数据"""
    print("🔧 修复词典数据格式...")
    
    # 读取原始数据
    input_file = Path("api/data/dictionary.json")
    
    if not input_file.exists():
        print(f"❌ 词典文件不存在: {input_file}")
        return False
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"📊 原始数据: {len(data)} 条")
        
        # 备份原始文件
        backup_file = Path(f"api/data/dictionary_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"💾 备份文件: {backup_file}")
        
        # 修复数据
        fixed_data = []
        error_count = 0
        
        for i, item in enumerate(data):
            try:
                fixed_item = fix_single_entry(item)
                if fixed_item:
                    fixed_data.append(fixed_item)
                else:
                    error_count += 1
                    print(f"⚠️ 跳过无效条目 {i}: {item.get('term', 'Unknown')}")
            except Exception as e:
                error_count += 1
                print(f"❌ 处理条目 {i} 时出错: {e}")
        
        print(f"✅ 修复完成: {len(fixed_data)} 条有效数据")
        print(f"⚠️ 错误条目: {error_count} 条")
        
        # 保存修复后的数据
        with open(input_file, 'w', encoding='utf-8') as f:
            json.dump(fixed_data, f, ensure_ascii=False, indent=2)
        
        print(f"💾 修复后数据已保存: {input_file}")
        
        # 生成修复报告
        generate_fix_report(data, fixed_data, error_count)
        
        return True
        
    except Exception as e:
        print(f"❌ 修复过程出错: {e}")
        return False

def fix_single_entry(item):
    """修复单个词典条目"""
    if not isinstance(item, dict):
        return None
    
    # 必须有term字段
    term = item.get('term', '').strip()
    if not term:
        return None
    
    fixed_item = {
        'term': term,
        'aliases': clean_list_field(item.get('aliases', [])),
        'category': item.get('category', '').strip(),
        'tags': clean_list_field(item.get('tags', [])),
        'description': item.get('description', '').strip(),
        'sub_category': item.get('sub_category', '').strip(),
        'source': item.get('source', '').strip(),
        'status': item.get('status', '').strip()
    }
    
    # 移除空字段
    cleaned_item = {}
    for key, value in fixed_item.items():
        if key in ['term']:  # 必需字段
            cleaned_item[key] = value
        elif key in ['aliases', 'tags']:  # 列表字段
            if value:  # 只保留非空列表
                cleaned_item[key] = value
            else:
                cleaned_item[key] = []
        else:  # 字符串字段
            if value:  # 只保留非空字符串
                cleaned_item[key] = value
            else:
                cleaned_item[key] = ''
    
    return cleaned_item

def generate_fix_report(original_data, fixed_data, error_count):
    """生成修复报告"""
    print("📝 生成修复报告...")
    
    # 统计修复前后的数据
    original_stats = analyze_data(original_data)
    fixed_stats = analyze_data(fixed_data)
    
    report = {
        'fix_time': datetime.now().isoformat(),
        'original_count': len(original_data),
        'fixed_count': len(fixed_data),
        'error_count': error_count,
        'original_stats': original_stats,
        'fixed_stats': fixed_stats,
        'improvements': {
            'aliases_cleaned': original_stats['avg_aliases'] - fixed_stats['avg_aliases'],
            'tags_cleaned': original_stats['avg_tags'] - fixed_stats['avg_tags'],
            'empty_terms_removed': original_stats['empty_terms'] - fixed_stats['empty_terms']
        }
    }
    
    # 保存报告
    report_file = Path("词典数据修复报告.json")
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"📄 修复报告已保存: {report_file}")
    
    # 打印关键统计
    print(f"\n📊 修复统计:")
    print(f"  原始数据: {len(original_data)} 条")
    print(f"  修复后数据: {len(fixed_data)} 条")
    print(f"  错误条目: {error_count} 条")
    print(f"  平均别名数: {original_stats['avg_aliases']:.1f} → {fixed_stats['avg_aliases']:.1f}")
    print(f"  平均标签数: {original_stats['avg_tags']:.1f} → {fixed_stats['avg_tags']:.1f}")
    print(f"  空术语条目: {original_stats['empty_terms']} → {fixed_stats['empty_terms']}")

def analyze_data(data):
    """分析数据统计"""
    if not data:
        return {'avg_aliases': 0, 'avg_tags': 0, 'empty_terms': 0}
    
    total_aliases = 0
    total_tags = 0
    empty_terms = 0
    
    for item in data:
        if isinstance(item, dict):
            if not item.get('term', '').strip():
                empty_terms += 1
            
            aliases = item.get('aliases', [])
            if isinstance(aliases, list):
                total_aliases += len(aliases)
            
            tags = item.get('tags', [])
            if isinstance(tags, list):
                total_tags += len(tags)
    
    return {
        'avg_aliases': total_aliases / len(data) if data else 0,
        'avg_tags': total_tags / len(data) if data else 0,
        'empty_terms': empty_terms
    }

def test_fixed_data():
    """测试修复后的数据"""
    print("🔍 测试修复后的数据...")
    
    input_file = Path("api/data/dictionary.json")
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"📊 数据总数: {len(data)}")
        
        # 检查前几条数据
        for i, item in enumerate(data[:3]):
            print(f"\n📋 示例 {i+1}:")
            print(f"  术语: {item.get('term', 'N/A')}")
            print(f"  类别: {item.get('category', 'N/A')}")
            print(f"  别名: {item.get('aliases', [])} ({len(item.get('aliases', []))} 个)")
            print(f"  标签: {item.get('tags', [])} ({len(item.get('tags', []))} 个)")
            print(f"  描述: {item.get('description', 'N/A')[:50]}...")
        
        # 检查数据质量
        valid_terms = sum(1 for item in data if item.get('term', '').strip())
        has_aliases = sum(1 for item in data if item.get('aliases'))
        has_tags = sum(1 for item in data if item.get('tags'))
        has_description = sum(1 for item in data if item.get('description', '').strip())
        
        print(f"\n📊 数据质量:")
        print(f"  有效术语: {valid_terms}/{len(data)} ({valid_terms/len(data)*100:.1f}%)")
        print(f"  有别名: {has_aliases}/{len(data)} ({has_aliases/len(data)*100:.1f}%)")
        print(f"  有标签: {has_tags}/{len(data)} ({has_tags/len(data)*100:.1f}%)")
        print(f"  有描述: {has_description}/{len(data)} ({has_description/len(data)*100:.1f}%)")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 修复词典数据格式")
    print("=" * 50)
    
    # 1. 修复数据
    success = fix_dictionary_data()
    
    if success:
        # 2. 测试修复结果
        test_fixed_data()
        
        print("\n" + "=" * 50)
        print("✅ 词典数据修复完成!")
        print("💡 下一步:")
        print("  1. 重启API服务")
        print("  2. 刷新前端页面")
        print("  3. 验证数据显示正常")
    else:
        print("\n❌ 词典数据修复失败")

if __name__ == "__main__":
    main()
