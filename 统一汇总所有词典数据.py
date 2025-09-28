#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一汇总所有词典数据 - 确保数据完整性和路径唯一性
"""

import pandas as pd
import json
import csv
from pathlib import Path
from datetime import datetime
import shutil

def find_all_dictionary_sources():
    """查找所有可能的词典数据源"""
    print("🔍 查找所有词典数据源...")
    
    sources = []
    
    # 1. 统一词典目录
    unified_dir = Path("data/unified_dictionary")
    if unified_dir.exists():
        for file in ["components.csv", "symptoms.csv", "causes.csv", "countermeasures.csv"]:
            file_path = unified_dir / file
            if file_path.exists():
                sources.append({
                    "path": str(file_path),
                    "type": "unified_dictionary",
                    "category": file.replace(".csv", ""),
                    "size": file_path.stat().st_size
                })
    
    # 2. API数据目录
    api_data_dir = Path("api/data")
    if api_data_dir.exists():
        for file in ["dictionary.json", "dictionary.csv"]:
            file_path = api_data_dir / file
            if file_path.exists():
                sources.append({
                    "path": str(file_path),
                    "type": "api_data",
                    "category": "all",
                    "size": file_path.stat().st_size
                })
    
    # 3. 硬件模块CSV文件
    for file in Path(".").glob("硬件模块词典数据_*.csv"):
        sources.append({
            "path": str(file),
            "type": "hardware_module",
            "category": file.stem.replace("硬件模块词典数据_", ""),
            "size": file.stat().st_size
        })
    
    # 4. 补充数据文件
    for file in Path(".").glob("补充词典数据_*.csv"):
        sources.append({
            "path": str(file),
            "type": "supplement",
            "category": file.stem.replace("补充词典数据_", ""),
            "size": file.stat().st_size
        })
    
    # 5. 其他可能的词典文件
    other_files = [
        "data/vocab/dictionary.json",
        "data/dicts/quality_terms.csv",
        "new_dictionary_data.csv"
    ]
    
    for file_path in other_files:
        path = Path(file_path)
        if path.exists():
            sources.append({
                "path": str(path),
                "type": "other",
                "category": path.stem,
                "size": path.stat().st_size
            })
    
    print(f"📊 找到 {len(sources)} 个数据源:")
    for source in sources:
        print(f"  {source['type']}: {source['path']} ({source['size']:,} bytes)")
    
    return sources

def load_and_merge_all_data(sources):
    """加载并合并所有数据"""
    print("📖 加载并合并所有数据...")
    
    all_data = []
    source_stats = {}
    
    for source in sources:
        try:
            path = Path(source["path"])
            
            if path.suffix == ".csv":
                df = pd.read_csv(path, encoding='utf-8')
                data = df.to_dict('records')
            elif path.suffix == ".json":
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if not isinstance(data, list):
                        continue  # 跳过非列表格式的JSON
            else:
                continue
            
            # 标记数据源
            for item in data:
                if isinstance(item, dict):
                    item['_source'] = source["type"]
                    item['_source_file'] = source["path"]
            
            all_data.extend(data)
            source_stats[source["path"]] = len(data)
            print(f"  ✅ {source['path']}: {len(data)} 条")
            
        except Exception as e:
            print(f"  ❌ {source['path']}: 加载失败 - {e}")
            source_stats[source["path"]] = 0
    
    print(f"📊 总计加载: {len(all_data)} 条原始数据")
    return all_data, source_stats

def standardize_data_format(all_data):
    """标准化数据格式"""
    print("🔄 标准化数据格式...")
    
    standardized_data = []
    field_mappings = {
        # 词条名称
        'term': ['term', 'name', '术语', '词条'],
        # 别名
        'aliases': ['aliases', 'alias', '别名', '同义词'],
        # 类别
        'category': ['category', 'label', 'type', '类别', '标签'],
        # 标签
        'tags': ['tags', 'tag', '标签', '多标签'],
        # 描述
        'description': ['description', 'definition', 'desc', '定义', '描述', '备注'],
        # 子类别
        'sub_category': ['sub_category', 'subcategory', '子类别'],
        # 来源
        'source': ['source', 'source_file', '来源'],
        # 状态
        'status': ['status', '状态']
    }
    
    for item in all_data:
        if not isinstance(item, dict):
            continue
        
        standardized_item = {}
        
        # 映射字段
        for std_field, possible_fields in field_mappings.items():
            value = None
            for field in possible_fields:
                if field in item and item[field] is not None:
                    value = item[field]
                    break
            
            if value is not None:
                # 处理特殊字段
                if std_field in ['aliases', 'tags']:
                    if isinstance(value, str):
                        # 分割字符串
                        if '；' in value:
                            value = [v.strip() for v in value.split('；') if v.strip()]
                        elif ';' in value:
                            value = [v.strip() for v in value.split(';') if v.strip()]
                        elif ',' in value:
                            value = [v.strip() for v in value.split(',') if v.strip()]
                        else:
                            value = [value.strip()] if value.strip() else []
                    elif not isinstance(value, list):
                        value = []
                elif std_field == 'description':
                    value = str(value).strip()
                else:
                    value = str(value).strip()
            else:
                # 设置默认值
                if std_field in ['aliases', 'tags']:
                    value = []
                else:
                    value = ''
            
            standardized_item[std_field] = value
        
        # 添加元数据
        standardized_item['_source'] = item.get('_source', 'unknown')
        standardized_item['_source_file'] = item.get('_source_file', 'unknown')
        standardized_item['_processed_at'] = datetime.now().isoformat()
        
        # 只保留有效的词条（必须有term）
        if standardized_item['term']:
            standardized_data.append(standardized_item)
    
    print(f"✅ 标准化完成: {len(standardized_data)} 条有效数据")
    return standardized_data

def deduplicate_data(standardized_data):
    """去重数据"""
    print("🔄 去重数据...")
    
    # 按term去重，保留最完整的记录
    term_groups = {}
    
    for item in standardized_data:
        term = item['term'].lower().strip()
        
        if term not in term_groups:
            term_groups[term] = []
        
        term_groups[term].append(item)
    
    deduplicated_data = []
    duplicate_count = 0
    
    for term, items in term_groups.items():
        if len(items) == 1:
            deduplicated_data.append(items[0])
        else:
            # 选择最完整的记录
            best_item = max(items, key=lambda x: (
                len(x['description']),
                len(x['aliases']),
                len(x['tags']),
                1 if x['category'] else 0
            ))
            
            # 合并别名和标签
            all_aliases = set()
            all_tags = set()
            
            for item in items:
                all_aliases.update(item['aliases'])
                all_tags.update(item['tags'])
            
            best_item['aliases'] = list(all_aliases)
            best_item['tags'] = list(all_tags)
            
            deduplicated_data.append(best_item)
            duplicate_count += len(items) - 1
    
    print(f"✅ 去重完成: 移除 {duplicate_count} 条重复数据，保留 {len(deduplicated_data)} 条")
    return deduplicated_data

def save_unified_data(deduplicated_data):
    """保存统一数据"""
    print("💾 保存统一数据...")
    
    # 创建输出目录
    output_dir = Path("unified_final_dictionary")
    output_dir.mkdir(exist_ok=True)
    
    # 备份现有数据
    backup_dir = Path("data/dictionary_backup") / f"before_final_unification_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    # 保存为JSON格式（API使用）
    json_file = output_dir / "dictionary.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(deduplicated_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ JSON文件已保存: {json_file}")
    
    # 保存为CSV格式（备用）
    csv_file = output_dir / "dictionary.csv"
    df = pd.DataFrame(deduplicated_data)
    df.to_csv(csv_file, index=False, encoding='utf-8')
    
    print(f"✅ CSV文件已保存: {csv_file}")
    
    # 生成统计报告
    stats = {
        'total_terms': len(deduplicated_data),
        'categories': {},
        'sources': {},
        'unification_date': datetime.now().isoformat()
    }
    
    for item in deduplicated_data:
        category = item.get('category', 'unknown')
        source = item.get('_source', 'unknown')
        
        stats['categories'][category] = stats['categories'].get(category, 0) + 1
        stats['sources'][source] = stats['sources'].get(source, 0) + 1
    
    stats_file = output_dir / "statistics.json"
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 统计文件已保存: {stats_file}")
    
    return output_dir, stats

def update_api_data_source(output_dir):
    """更新API数据源"""
    print("🔄 更新API数据源...")
    
    # 确保API数据目录存在
    api_data_dir = Path("api/data")
    api_data_dir.mkdir(parents=True, exist_ok=True)
    
    # 复制统一数据到API目录
    source_json = output_dir / "dictionary.json"
    target_json = api_data_dir / "dictionary.json"
    
    if source_json.exists():
        shutil.copy2(source_json, target_json)
        print(f"✅ 已更新API数据源: {target_json}")
    
    # 复制CSV文件
    source_csv = output_dir / "dictionary.csv"
    target_csv = api_data_dir / "dictionary.csv"
    
    if source_csv.exists():
        shutil.copy2(source_csv, target_csv)
        print(f"✅ 已更新API CSV文件: {target_csv}")
    
    # 复制统计文件
    source_stats = output_dir / "statistics.json"
    target_stats = api_data_dir / "dictionary_stats.json"
    
    if source_stats.exists():
        shutil.copy2(source_stats, target_stats)
        print(f"✅ 已更新API统计文件: {target_stats}")

def main():
    """主函数"""
    print("🚀 统一汇总所有词典数据")
    print("=" * 60)
    
    # 1. 查找所有数据源
    sources = find_all_dictionary_sources()
    
    if not sources:
        print("❌ 未找到任何词典数据源")
        return
    
    # 2. 加载并合并所有数据
    all_data, source_stats = load_and_merge_all_data(sources)
    
    if not all_data:
        print("❌ 未能加载任何数据")
        return
    
    # 3. 标准化数据格式
    standardized_data = standardize_data_format(all_data)
    
    # 4. 去重数据
    deduplicated_data = deduplicate_data(standardized_data)
    
    # 5. 保存统一数据
    output_dir, stats = save_unified_data(deduplicated_data)
    
    # 6. 更新API数据源
    update_api_data_source(output_dir)
    
    print("\n" + "=" * 60)
    print("🎉 词典数据统一汇总完成!")
    print(f"📊 最终数据: {stats['total_terms']} 条")
    print(f"📊 数据分布:")
    for category, count in sorted(stats['categories'].items(), key=lambda x: x[1], reverse=True):
        print(f"  {category}: {count} 条")
    
    print(f"\n📁 输出文件:")
    print(f"  统一数据: {output_dir}/dictionary.json")
    print(f"  API数据: api/data/dictionary.json")
    print(f"  统计报告: {output_dir}/statistics.json")
    
    print(f"\n💡 下一步:")
    print(f"1. 重启API服务加载新数据")
    print(f"2. 验证前端显示 {stats['total_terms']} 条数据")
    print(f"3. 测试搜索和筛选功能")
    print(f"4. 确认路径唯一性")

if __name__ == "__main__":
    main()
