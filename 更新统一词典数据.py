#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新统一词典数据 - 添加654条新数据
"""

import pandas as pd
import json
import csv
from datetime import datetime
from pathlib import Path

def backup_current_data():
    """备份当前数据"""
    print("💾 备份当前统一词典数据...")
    
    backup_dir = Path("data/dictionary_backup") / f"before_update_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    unified_dir = Path("data/unified_dictionary")
    if unified_dir.exists():
        import shutil
        shutil.copytree(unified_dir, backup_dir / "unified_dictionary")
        print(f"✅ 备份完成: {backup_dir}")
    
    return backup_dir

def load_new_supplement_data():
    """加载新的补充数据"""
    print("📖 加载新的补充数据...")
    
    # 读取基础补充数据
    basic_files = [
        ('补充词典数据_批次1.csv', '基础补充批次1'),
        ('补充词典数据_批次2.csv', '基础补充批次2')
    ]
    
    # 读取20个硬件模块数据
    hardware_files = [
        ('硬件模块词典数据_显示屏.csv', '显示屏模块'),
        ('硬件模块词典数据_摄像头.csv', '摄像头模块'),
        ('硬件模块词典数据_电池.csv', '电池模块'),
        ('硬件模块词典数据_主板PCBA.csv', '主板PCBA模块'),
        ('硬件模块词典数据_射频天线.csv', '射频与天线模块'),
        ('硬件模块词典数据_声学.csv', '声学模块'),
        ('硬件模块词典数据_结构连接器.csv', '结构件与连接器模块'),
        ('硬件模块词典数据_散热系统.csv', '散热系统模块'),
        ('硬件模块词典数据_传感器.csv', '传感器模块'),
        ('硬件模块词典数据_充电电源.csv', '充电与电源管理模块'),
        ('硬件模块词典数据_马达触觉.csv', '马达与触觉反馈模块'),
        ('硬件模块词典数据_外壳涂层.csv', '外壳涂层与外观模块'),
        ('硬件模块词典数据_连接网络.csv', '连接与网络模块'),
        ('硬件模块词典数据_接口连接器.csv', '接口与连接器模块'),
        ('硬件模块词典数据_被动元件.csv', '被动元件与电路保护模块'),
        ('硬件模块词典数据_生产测试治具.csv', '生产与测试治具模块'),
        ('硬件模块词典数据_材料科学基础.csv', '材料科学基础模块'),
        ('硬件模块词典数据_先进制造工艺.csv', '先进制造工艺模块'),
        ('硬件模块词典数据_失效分析可靠性.csv', '失效分析与可靠性工程模块'),
        ('硬件模块词典数据_标准法规.csv', '标准与法规模块')
    ]
    
    all_files = basic_files + hardware_files
    all_data = []
    
    for file_name, desc in all_files:
        try:
            df = pd.read_csv(file_name, encoding='utf-8')
            all_data.append(df)
            print(f"✅ {desc}: {len(df)} 条记录")
        except Exception as e:
            print(f"❌ 读取 {desc} 失败: {e}")
    
    if all_data:
        df_all = pd.concat(all_data, ignore_index=True)
        print(f"📊 总计加载: {len(df_all)} 条新数据")
        return df_all
    else:
        print("❌ 未能加载任何新数据")
        return None

def categorize_data(df):
    """将数据按照统一词典的分类进行归类"""
    print("📋 按统一词典分类归类数据...")
    
    categories = {
        "components": [],
        "symptoms": [],
        "causes": [],
        "countermeasures": []
    }
    
    for _, row in df.iterrows():
        term = row['term']
        category = row['category']
        
        # 转换为统一词典格式
        item = {
            'term': term,
            'canonical_name': term,
            'aliases': row.get('aliases', ''),
            'category': category,
            'tags': row.get('tags', ''),
            'description': row.get('definition', ''),
            'source_file': 'hardware_module_expansion',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        # 根据Label分类
        if category in ['Component', 'Material']:
            categories["components"].append(item)
        elif category in ['Symptom']:
            categories["symptoms"].append(item)
        elif category in ['Process', 'TestCase', 'Tool', 'Role']:
            categories["countermeasures"].append(item)
        elif category in ['Metric']:
            categories["components"].append(item)  # 性能指标归类到组件
        else:
            categories["countermeasures"].append(item)  # 默认归类到对策
    
    print(f"📊 分类结果:")
    for cat, items in categories.items():
        print(f"  {cat}: {len(items)} 条")
    
    return categories

def load_existing_data():
    """加载现有的统一词典数据"""
    print("📖 加载现有统一词典数据...")
    
    unified_dir = Path("data/unified_dictionary")
    existing_data = {
        "components": [],
        "symptoms": [],
        "causes": [],
        "countermeasures": []
    }
    
    for category in existing_data.keys():
        file_path = unified_dir / f"{category}.csv"
        if file_path.exists():
            try:
                df = pd.read_csv(file_path, encoding='utf-8')
                existing_data[category] = df.to_dict('records')
                print(f"  {category}: {len(existing_data[category])} 条现有数据")
            except Exception as e:
                print(f"❌ 读取 {category}.csv 失败: {e}")
    
    return existing_data

def merge_and_save_data(existing_data, new_categories):
    """合并并保存数据"""
    print("💾 合并并保存数据...")
    
    unified_dir = Path("data/unified_dictionary")
    fieldnames = ['term', 'canonical_name', 'aliases', 'category', 'tags', 'description', 'source_file', 'created_at', 'updated_at']
    
    total_added = 0
    final_counts = {}
    
    for category_name in existing_data.keys():
        existing_items = existing_data[category_name]
        new_items = new_categories[category_name]
        
        # 去重 - 基于term字段
        existing_terms = {item['term'].lower() for item in existing_items}
        unique_new_items = []
        
        for item in new_items:
            if item['term'].lower() not in existing_terms:
                unique_new_items.append(item)
            else:
                print(f"⚠️ 跳过重复词条: {item['term']}")
        
        # 合并数据
        all_items = existing_items + unique_new_items
        final_counts[category_name] = len(all_items)
        total_added += len(unique_new_items)
        
        # 保存文件
        file_path = unified_dir / f"{category_name}.csv"
        with open(file_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_items)
        
        print(f"✅ 更新 {category_name}.csv: 新增{len(unique_new_items)}条，总计{len(all_items)}条")
    
    # 更新统计文件
    stats = {
        'total_terms': sum(final_counts.values()),
        'categories': final_counts,
        'last_updated': datetime.now().isoformat(),
        'last_expansion': {
            'date': datetime.now().isoformat(),
            'added_count': total_added,
            'source': 'hardware_module_expansion_654_terms',
            'modules_covered': 20,
            'tech_domains': 18
        },
        'unified_directory': str(unified_dir)
    }
    
    with open(unified_dir / "statistics.json", 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 统计文件已更新")
    return total_added, final_counts

def main():
    """主函数"""
    print("🚀 更新统一词典数据 - 添加654条硬件模块数据")
    print("=" * 60)
    
    # 1. 备份当前数据
    backup_dir = backup_current_data()
    
    # 2. 加载新的补充数据
    new_df = load_new_supplement_data()
    if new_df is None:
        print("❌ 无法加载新数据，退出")
        return
    
    # 3. 分类新数据
    new_categories = categorize_data(new_df)
    
    # 4. 加载现有数据
    existing_data = load_existing_data()
    
    # 5. 合并并保存
    total_added, final_counts = merge_and_save_data(existing_data, new_categories)
    
    print("\n" + "=" * 60)
    print("🎉 统一词典数据更新完成!")
    print(f"💾 备份目录: {backup_dir}")
    print(f"📊 本次新增: {total_added} 条")
    print(f"📊 最终统计:")
    for cat, count in final_counts.items():
        print(f"  {cat}: {count} 条")
    print(f"📊 总计: {sum(final_counts.values())} 条")
    
    growth_rate = (total_added / 110) * 100  # 原有110条
    print(f"📈 增长率: +{growth_rate:.1f}%")
    
    print(f"\n💡 下一步:")
    print(f"1. 重启API服务以加载新数据")
    print(f"2. 重启前端服务")
    print(f"3. 验证前端词典页面显示")
    print(f"4. 测试新增硬件模块数据查询")

if __name__ == "__main__":
    main()
