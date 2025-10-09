#!/usr/bin/env python3
"""
导入新批次词典数据到dictionary.json和Neo4j图谱
"""
import json
import csv
from datetime import datetime

def load_existing_dictionary():
    """加载现有词典"""
    with open('api/data/dictionary.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def load_csv_data(csv_file):
    """从CSV加载新数据"""
    new_entries = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # 解析别名（分号分隔）
            aliases = [a.strip() for a in row['别名'].split(';') if a.strip()]
            
            # 解析标签（分号分隔）
            tags = [t.strip() for t in row['多标签'].split(';') if t.strip()]
            
            entry = {
                "term": row['术语'].strip(),
                "aliases": aliases,
                "category": row['类别'].strip(),
                "tags": tags,
                "description": row['备注'].strip(),
                "sub_category": "",
                "source": "manual_supplement_2025",
                "status": "",
                "original_category": row['类别'].strip()
            }
            new_entries.append(entry)
    
    return new_entries

def check_duplicates(existing_data, new_entries):
    """检查重复"""
    existing_terms = set(e['term'] for e in existing_data)
    duplicates = []
    unique_entries = []
    
    for entry in new_entries:
        if entry['term'] in existing_terms:
            duplicates.append(entry['term'])
        else:
            unique_entries.append(entry)
    
    return unique_entries, duplicates

def merge_and_save(existing_data, new_entries, output_file):
    """合并并保存"""
    merged_data = existing_data + new_entries
    
    # 保存到文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=2)
    
    return merged_data

def generate_import_report(existing_count, new_count, duplicates):
    """生成导入报告"""
    report = f"""
{'='*80}
📊 词典数据导入报告
{'='*80}

导入时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📋 数据统计:
  原有词典: {existing_count}条
  新增数据: {new_count}条
  导入后总数: {existing_count + new_count}条
  增长率: {new_count/existing_count*100:.1f}%

"""
    
    if duplicates:
        report += f"""
⚠️ 重复术语 ({len(duplicates)}条):
"""
        for dup in duplicates:
            report += f"  - {dup}\n"
    else:
        report += "✅ 无重复术语\n"
    
    report += f"""
{'='*80}
✅ 导入完成
{'='*80}
"""
    
    return report

def main():
    print("=" * 80)
    print("📥 开始导入新批次词典数据")
    print("=" * 80)
    
    # 1. 加载现有词典
    print("\n1️⃣ 加载现有词典...")
    existing_data = load_existing_dictionary()
    print(f"   现有词典: {len(existing_data)}条")
    
    # 2. 加载新数据
    print("\n2️⃣ 加载新批次数据...")
    csv_file = 'batch_60_corrected.csv'
    new_entries = load_csv_data(csv_file)
    print(f"   新批次数据: {len(new_entries)}条")
    
    # 3. 检查重复
    print("\n3️⃣ 检查重复...")
    unique_entries, duplicates = check_duplicates(existing_data, new_entries)
    print(f"   唯一数据: {len(unique_entries)}条")
    if duplicates:
        print(f"   ⚠️ 重复数据: {len(duplicates)}条")
        for dup in duplicates[:5]:
            print(f"      - {dup}")
    else:
        print(f"   ✅ 无重复数据")
    
    # 4. 合并并保存
    print("\n4️⃣ 合并并保存...")
    output_file = 'api/data/dictionary.json'
    merged_data = merge_and_save(existing_data, unique_entries, output_file)
    print(f"   ✅ 已保存到: {output_file}")
    print(f"   总条目数: {len(merged_data)}条")
    
    # 5. 生成报告
    print("\n5️⃣ 生成导入报告...")
    report = generate_import_report(len(existing_data), len(unique_entries), duplicates)
    
    # 保存报告
    report_file = 'IMPORT_REPORT.md'
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"   ✅ 报告已保存到: {report_file}")
    
    # 6. 显示报告
    print(report)
    
    # 7. 分类统计
    print("\n6️⃣ 分类统计:")
    from collections import Counter
    category_counts = Counter(e['category'] for e in merged_data)
    for cat, count in category_counts.most_common():
        print(f"   {cat}: {count}条")
    
    print("\n" + "=" * 80)
    print("✅ 导入完成！")
    print("=" * 80)
    
    print("\n📝 下一步:")
    print("   1. 运行 python check_dictionary_quality.py 验证数据质量")
    print("   2. 运行 python sync_to_neo4j.py 同步到Neo4j图谱")
    print("   3. 重启后端API服务")

if __name__ == "__main__":
    main()
