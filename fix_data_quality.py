#!/usr/bin/env python3
"""
修复数据质量问题
1. 补充缺失别名
2. 为标签不足的词条补充标签
"""
import json

# 加载词典数据
with open('api/data/dictionary.json', 'r', encoding='utf-8') as f:
    dictionary = json.load(f)

print("=" * 80)
print("🔧 修复数据质量问题")
print("=" * 80)

# 1. 查找缺少别名的词条
print("\n1️⃣ 查找缺少别名的词条")
print("-" * 80)

no_alias_entries = []
for entry in dictionary:
    if not entry.get('aliases') or len(entry.get('aliases', [])) == 0:
        no_alias_entries.append(entry)

print(f"发现 {len(no_alias_entries)} 条缺少别名的词条:")
for entry in no_alias_entries:
    print(f"  - {entry['term']} ({entry['category']})")

# 补充别名
if no_alias_entries:
    print("\n补充别名:")
    for entry in no_alias_entries:
        term = entry['term']
        # 根据术语特点补充别名
        if term == "飞线":
            entry['aliases'] = ["跳线", "Jumper Wire", "修补线"]
            print(f"  ✅ {term}: {entry['aliases']}")
        elif term == "彩虹纹":
            entry['aliases'] = ["Newton Ring", "牛顿环", "彩虹效应"]
            print(f"  ✅ {term}: {entry['aliases']}")

# 2. 查找标签少于2个的词条
print("\n2️⃣ 查找标签少于2个的词条")
print("-" * 80)

few_tags_entries = []
for entry in dictionary:
    if len(entry.get('tags', [])) < 2:
        few_tags_entries.append(entry)

print(f"发现 {len(few_tags_entries)} 条标签少于2个的词条:")
for entry in few_tags_entries[:20]:  # 只显示前20条
    tags = entry.get('tags', [])
    print(f"  - {entry['term']:20s} ({entry['category']:10s}): {tags}")

# 补充标签
print("\n补充标签:")
tag_additions = {
    # Symptom类
    '反白': ['显示相关', '异常现象'],
    '黄斑': ['显示相关', '异常现象'],
    '亮斑': ['显示相关', '异常现象'],
    '亮线': ['显示相关', '异常现象'],
    '闪退': ['软件相关', '异常现象'],
    '失效': ['可靠性', '异常现象'],
    '云纹': ['影像相关', '异常现象'],
    '噪点': ['影像相关', '异常现象'],
    '醉机': ['软件相关', '异常现象'],
    # TestCase类
    '环测': ['可靠性', '测试验证'],
    '老化': ['可靠性', '测试验证'],
    '三防': ['可靠性', '测试验证'],
    '周波': ['可靠性', '测试验证'],
    # Process类
    '胶量': ['工艺参数', '制造工艺'],
    # Material类
    '原材': ['物料', '供应链'],
    '子料': ['物料', '供应链'],
    # Component类
    'CMF': ['外观', '设计'],
    'Gap': ['外观', '装配'],
    'Lens': ['影像相关', '部件'],
    'OIS': ['影像相关', '功能'],
    'SPK': ['声学', '部件'],
    'TP': ['人机交互', '部件'],
    'WLAN': ['通信相关', '功能'],
    '包材': ['外观', '物料'],
    '背光': ['显示相关', '部件'],
    '边框': ['结构相关', '外观'],
    '充电口': ['电气连接', '部件'],
    '触点': ['电气连接', '部件'],
    '电芯': ['硬件相关', '安全相关'],
    '飞线': ['PCB', '部件'],
    '盖板': ['外观', '部件'],
    '高光': ['CMF', '外观'],
}

updated_count = 0
for entry in dictionary:
    term = entry['term']
    if term in tag_additions:
        current_tags = set(entry.get('tags', []))
        new_tags = set(tag_additions[term])
        combined_tags = list(current_tags | new_tags)
        if len(combined_tags) > len(current_tags):
            entry['tags'] = combined_tags
            print(f"  ✅ {term:20s}: {current_tags} → {combined_tags}")
            updated_count += 1

print(f"\n已更新 {updated_count} 条词条的标签")

# 3. 保存修复后的数据
print("\n3️⃣ 保存修复后的数据")
print("-" * 80)

# 备份原文件
import shutil
shutil.copy('api/data/dictionary.json', 'api/data/dictionary_backup_before_fix.json')
print("✅ 已备份原文件: dictionary_backup_before_fix.json")

# 保存修复后的数据
with open('api/data/dictionary.json', 'w', encoding='utf-8') as f:
    json.dump(dictionary, f, ensure_ascii=False, indent=2)

print("✅ 已保存修复后的数据")

# 4. 验证修复结果
print("\n4️⃣ 验证修复结果")
print("-" * 80)

# 重新检查
no_alias_after = sum(1 for e in dictionary if not e.get('aliases'))
few_tags_after = sum(1 for e in dictionary if len(e.get('tags', [])) < 2)

print(f"缺少别名: {len(no_alias_entries)} → {no_alias_after}")
print(f"标签不足: {len(few_tags_entries)} → {few_tags_after}")

if no_alias_after == 0 and few_tags_after == 0:
    print("\n✅ 所有数据质量问题已修复！")
else:
    print(f"\n⚠️ 仍有 {no_alias_after} 条缺少别名，{few_tags_after} 条标签不足")

print("\n" + "=" * 80)
print("✅ 修复完成")
print("=" * 80)

