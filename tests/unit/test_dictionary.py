#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试词典管理功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.dictionary_manager import DictionaryManager, DictionaryEntry
import json

def test_dictionary_management():
    """测试词典管理功能"""
    
    print("🧪 开始测试词典管理功能...")
    
    # 初始化词典管理器
    manager = DictionaryManager()
    
    # 测试1: 基本功能测试
    print("\n📋 测试1: 基本功能测试")
    
    # 添加测试条目
    test_entry = DictionaryEntry(
        term="测试术语",
        aliases=["测试别名1", "测试别名2"],
        category="测试类别",
        tags=["测试标签1", "测试标签2"],
        definition="这是一个测试术语的定义",
        source="test"
    )
    
    success = manager.add_entry(test_entry)
    print(f"   添加条目: {'✅' if success else '❌'}")
    
    # 更新条目
    test_entry.definition = "更新后的定义"
    manager.update_entry(test_entry)
    print("   ✅ 更新条目")
    
    # 搜索条目
    results = manager.search_entries("测试")
    print(f"   搜索结果: {len(results)} 条")
    
    # 测试2: 重复检测和清除
    print("\n🔍 测试2: 重复检测和清除")
    
    # 添加重复条目
    duplicate_entry = DictionaryEntry(
        term="测试术语",  # 相同主术语
        aliases=["另一个别名"],
        category="测试类别",  # 相同类别
        tags=["另一个标签"],
        definition="重复的测试术语",
        source="test"
    )
    
    manager.add_entry(duplicate_entry)
    
    # 查找重复项
    duplicates = manager.find_duplicates()
    print(f"   发现重复项: {len(duplicates)} 个")
    
    for dup in duplicates:
        print(f"     术语: {dup['term']} (出现{dup['count']}次)")
    
    # 清除重复项
    if duplicates:
        clean_result = manager.remove_duplicates("merge")
        print(f"   清除结果: 删除{clean_result['entries_removed']}条，合并{clean_result['entries_merged']}条")
    
    # 测试3: 批量导入
    print("\n📥 测试3: 批量导入")
    
    batch_data = [
        {
            "术语": "批量术语1",
            "别名": "别名1;别名2",
            "类别": "批量类别",
            "多标签": "标签1;标签2",
            "备注": "批量导入的测试术语1"
        },
        {
            "术语": "批量术语2",
            "别名": "别名3;别名4",
            "类别": "批量类别",
            "多标签": "标签3;标签4",
            "备注": "批量导入的测试术语2"
        }
    ]
    
    import_result = manager.batch_import_from_table(batch_data)
    print(f"   导入结果: 新增{import_result['imported']}条，更新{import_result['updated']}条")
    
    # 测试4: 统计信息
    print("\n📊 测试4: 统计信息")
    
    stats = manager.get_statistics()
    print(f"   总条目: {stats['total_entries']}")
    print(f"   总别名: {stats['total_aliases']}")
    print(f"   平均别名: {stats['avg_aliases_per_entry']}")
    print(f"   类别分布: {stats['categories']}")
    
    # 测试5: 导出功能
    print("\n📤 测试5: 导出功能")
    
    export_file = manager.export_to_csv()
    print(f"   导出文件: {export_file}")
    print(f"   文件存在: {'✅' if export_file.exists() else '❌'}")
    
    # 测试6: 数据持久化
    print("\n💾 测试6: 数据持久化")
    
    # 保存词典
    manager.save_dictionary()
    print("   ✅ 保存词典")
    
    # 重新加载
    new_manager = DictionaryManager()
    print(f"   重新加载: {len(new_manager.entries)} 条记录")
    
    # 验证数据一致性
    original_count = len(manager.entries)
    reloaded_count = len(new_manager.entries)
    print(f"   数据一致性: {'✅' if original_count == reloaded_count else '❌'}")
    
    # 测试7: 错误处理
    print("\n⚠️ 测试7: 错误处理")
    
    # 测试空术语
    try:
        empty_entry = DictionaryEntry(
            term="",
            aliases=[],
            category="测试",
            tags=[],
            definition=""
        )
        manager.add_entry(empty_entry)
        print("   空术语处理: ❌ (应该被拒绝)")
    except:
        print("   空术语处理: ✅ (正确拒绝)")
    
    # 测试删除不存在的条目
    delete_result = manager.delete_entry("不存在的术语", "不存在的类别")
    print(f"   删除不存在条目: {'✅' if not delete_result else '❌'}")
    
    # 测试8: 性能测试
    print("\n⚡ 测试8: 性能测试")
    
    import time
    
    # 批量添加测试
    start_time = time.time()
    for i in range(100):
        perf_entry = DictionaryEntry(
            term=f"性能测试术语{i}",
            aliases=[f"别名{i}"],
            category="性能测试",
            tags=[f"标签{i}"],
            definition=f"性能测试术语{i}的定义"
        )
        manager.add_entry(perf_entry)
    
    add_time = time.time() - start_time
    print(f"   添加100条记录耗时: {add_time:.3f}秒")
    
    # 搜索性能测试
    start_time = time.time()
    search_results = manager.search_entries("性能测试")
    search_time = time.time() - start_time
    print(f"   搜索耗时: {search_time:.3f}秒，结果: {len(search_results)}条")
    
    # 重复检测性能测试
    start_time = time.time()
    duplicates = manager.find_duplicates()
    duplicate_time = time.time() - start_time
    print(f"   重复检测耗时: {duplicate_time:.3f}秒，发现: {len(duplicates)}个重复项")
    
    # 最终统计
    print("\n📈 最终统计:")
    final_stats = manager.get_statistics()
    print(f"   总条目数: {final_stats['total_entries']}")
    print(f"   总别名数: {final_stats['total_aliases']}")
    print(f"   类别数量: {len(final_stats['categories'])}")
    
    print("\n🎉 词典管理功能测试完成！")
    
    # 清理测试数据
    print("\n🧹 清理测试数据...")
    test_categories = ["测试类别", "批量类别", "性能测试"]
    
    entries_to_remove = []
    for entry_hash, entry in manager.entries.items():
        if entry.category in test_categories or entry.source == "test":
            entries_to_remove.append(entry_hash)
    
    for entry_hash in entries_to_remove:
        del manager.entries[entry_hash]
    
    manager.save_dictionary()
    print(f"   清理了 {len(entries_to_remove)} 条测试数据")
    
    return True

def test_api_integration():
    """测试API集成"""
    
    print("\n🌐 测试API集成...")
    
    try:
        import requests
        
        # 测试获取词典条目
        response = requests.get('http://127.0.0.1:8000/kg/dictionary/entries')
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"   ✅ API获取词典: {len(data['data']['entries'])} 条记录")
            else:
                print("   ❌ API返回失败")
        else:
            print(f"   ❌ API请求失败: {response.status_code}")
        
        # 测试获取统计信息
        response = requests.get('http://127.0.0.1:8000/kg/dictionary/statistics')
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"   ✅ API获取统计: {data['data']['total_entries']} 条记录")
            else:
                print("   ❌ API统计失败")
        else:
            print(f"   ❌ API统计请求失败: {response.status_code}")
        
        # 测试查找重复项
        response = requests.get('http://127.0.0.1:8000/kg/dictionary/duplicates')
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"   ✅ API查找重复: {data['data']['count']} 个重复项")
            else:
                print("   ❌ API重复检测失败")
        else:
            print(f"   ❌ API重复检测请求失败: {response.status_code}")
        
        print("   🎉 API集成测试完成")
        
    except ImportError:
        print("   ⚠️ requests库未安装，跳过API测试")
    except Exception as e:
        print(f"   ❌ API测试失败: {e}")

if __name__ == "__main__":
    # 运行词典管理测试
    test_dictionary_management()
    
    # 运行API集成测试
    test_api_integration()
