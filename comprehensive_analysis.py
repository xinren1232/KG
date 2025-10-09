#!/usr/bin/env python3
"""
词典分类和图谱设计全面评估分析
"""
import json
from collections import defaultdict, Counter

# 加载词典数据
with open('api/data/dictionary.json', 'r', encoding='utf-8') as f:
    dictionary = json.load(f)

print("=" * 80)
print("📊 词典分类和图谱设计全面评估报告")
print("=" * 80)

# 1. 基础统计
print("\n1️⃣ 基础统计")
print("-" * 80)
print(f"总词条数: {len(dictionary)}")

# 分类统计
category_stats = Counter(entry['category'] for entry in dictionary)
print(f"\n分类分布 (8类):")
for category, count in category_stats.most_common():
    percentage = count / len(dictionary) * 100
    print(f"  {category:20s}: {count:4d} 条 ({percentage:5.1f}%)")

# 2. 标签体系分析
print("\n2️⃣ 标签体系分析")
print("-" * 80)

all_tags = []
for entry in dictionary:
    all_tags.extend(entry.get('tags', []))

tag_stats = Counter(all_tags)
print(f"标签总数: {len(tag_stats)} 个")
print(f"标签使用总次数: {len(all_tags)} 次")
print(f"平均每词条标签数: {len(all_tags) / len(dictionary):.2f} 个")

print(f"\nTop 20 高频标签:")
for tag, count in tag_stats.most_common(20):
    percentage = count / len(dictionary) * 100
    print(f"  {tag:20s}: {count:4d} 次 ({percentage:5.1f}%)")

# 3. 别名覆盖率分析
print("\n3️⃣ 别名覆盖率分析")
print("-" * 80)

entries_with_aliases = sum(1 for entry in dictionary if entry.get('aliases'))
total_aliases = sum(len(entry.get('aliases', [])) for entry in dictionary)
avg_aliases = total_aliases / len(dictionary)

print(f"有别名的词条: {entries_with_aliases} / {len(dictionary)} ({entries_with_aliases/len(dictionary)*100:.1f}%)")
print(f"别名总数: {total_aliases}")
print(f"平均每词条别名数: {avg_aliases:.2f} 个")

# 4. 描述完整度分析
print("\n4️⃣ 描述完整度分析")
print("-" * 80)

entries_with_desc = sum(1 for entry in dictionary if entry.get('description'))
desc_lengths = [len(entry.get('description', '')) for entry in dictionary if entry.get('description')]
avg_desc_length = sum(desc_lengths) / len(desc_lengths) if desc_lengths else 0

print(f"有描述的词条: {entries_with_desc} / {len(dictionary)} ({entries_with_desc/len(dictionary)*100:.1f}%)")
print(f"平均描述长度: {avg_desc_length:.1f} 字符")

# 5. 领域覆盖分析
print("\n5️⃣ 领域覆盖分析（基于标签）")
print("-" * 80)

domain_tags = {
    '影像相关': 0,
    '显示相关': 0,
    '射频相关': 0,
    '通信相关': 0,
    '声学': 0,
    '热管理': 0,
    'EMC': 0,
    '结构相关': 0,
    '电气性能': 0,
    '软件相关': 0,
    '测试验证': 0,
    '制造工艺': 0,
    '质量体系': 0,
}

for tag, count in tag_stats.items():
    for domain in domain_tags:
        if domain in tag:
            domain_tags[domain] += count
            break

print("领域标签使用统计:")
for domain, count in sorted(domain_tags.items(), key=lambda x: x[1], reverse=True):
    if count > 0:
        print(f"  {domain:20s}: {count:4d} 次")

# 6. 分类-标签关联分析
print("\n6️⃣ 分类-标签关联分析")
print("-" * 80)

category_tag_map = defaultdict(Counter)
for entry in dictionary:
    category = entry['category']
    for tag in entry.get('tags', []):
        category_tag_map[category][tag] += 1

print("各分类的Top 5标签:")
for category in sorted(category_stats.keys()):
    print(f"\n{category}:")
    for tag, count in category_tag_map[category].most_common(5):
        print(f"  {tag:20s}: {count:3d} 次")

# 7. 数据质量评分
print("\n7️⃣ 数据质量评分")
print("-" * 80)

# 计算各项指标
alias_score = (entries_with_aliases / len(dictionary)) * 100
desc_score = (entries_with_desc / len(dictionary)) * 100
tag_score = min((len(all_tags) / len(dictionary) / 3) * 100, 100)  # 目标平均3个标签
category_balance_score = (1 - (max(category_stats.values()) - min(category_stats.values())) / len(dictionary)) * 100

overall_score = (alias_score + desc_score + tag_score + category_balance_score) / 4

print(f"别名覆盖率得分: {alias_score:.1f}/100")
print(f"描述完整度得分: {desc_score:.1f}/100")
print(f"标签丰富度得分: {tag_score:.1f}/100")
print(f"分类平衡度得分: {category_balance_score:.1f}/100")
print(f"\n综合质量得分: {overall_score:.1f}/100")

# 8. 图谱关系潜力分析
print("\n8️⃣ 图谱关系潜力分析")
print("-" * 80)

# 分析可以建立的关系类型
symptom_count = category_stats.get('Symptom', 0)
component_count = category_stats.get('Component', 0)
testcase_count = category_stats.get('TestCase', 0)
tool_count = category_stats.get('Tool', 0)
process_count = category_stats.get('Process', 0)

print(f"当前关系数: 3770 (HAS_TAG) + 1333 (BELONGS_TO) = 5103")
print(f"\n潜在关系扩展:")
print(f"  Symptom → Component (AFFECTS): 最多 {symptom_count * component_count} 条")
print(f"  TestCase → Component (TESTS): 最多 {testcase_count * component_count} 条")
print(f"  Tool → TestCase (USED_IN): 最多 {tool_count * testcase_count} 条")
print(f"  Process → Component (PRODUCES): 最多 {process_count * component_count} 条")

# 9. 问题识别
print("\n9️⃣ 问题识别")
print("-" * 80)

issues = []

# 检查缺少别名的词条
no_alias_entries = [e for e in dictionary if not e.get('aliases')]
if no_alias_entries:
    issues.append(f"⚠️ {len(no_alias_entries)} 条词条缺少别名")

# 检查缺少描述的词条
no_desc_entries = [e for e in dictionary if not e.get('description')]
if no_desc_entries:
    issues.append(f"⚠️ {len(no_desc_entries)} 条词条缺少描述")

# 检查标签过少的词条
few_tags_entries = [e for e in dictionary if len(e.get('tags', [])) < 2]
if few_tags_entries:
    issues.append(f"⚠️ {len(few_tags_entries)} 条词条标签少于2个")

# 检查分类不平衡
max_cat = max(category_stats.values())
min_cat = min(category_stats.values())
if max_cat / min_cat > 5:
    issues.append(f"⚠️ 分类不平衡: 最多{max_cat}条 vs 最少{min_cat}条 (差距{max_cat/min_cat:.1f}倍)")

if issues:
    print("发现的问题:")
    for issue in issues:
        print(f"  {issue}")
else:
    print("✅ 未发现明显问题")

# 10. 优化建议
print("\n🔟 优化建议")
print("-" * 80)

suggestions = []

# 基于分析给出建议
if alias_score < 95:
    suggestions.append(f"📝 提升别名覆盖率: 当前{alias_score:.1f}%，建议补充{len(dictionary) - entries_with_aliases}条词条的别名")

if tag_score < 90:
    suggestions.append(f"🏷️ 增加标签丰富度: 当前平均{len(all_tags)/len(dictionary):.2f}个/词条，建议增至3个以上")

if category_balance_score < 80:
    suggestions.append(f"⚖️ 平衡分类分布: 补充{min(category_stats, key=category_stats.get)}类词条")

# 领域覆盖建议
weak_domains = [d for d, c in domain_tags.items() if c < 50]
if weak_domains:
    suggestions.append(f"🎯 加强弱势领域: {', '.join(weak_domains[:3])}")

# 关系建立建议
suggestions.append(f"🔗 建立语义关系: 优先建立Symptom-Component、TestCase-Component关系")

if suggestions:
    print("优化建议:")
    for i, suggestion in enumerate(suggestions, 1):
        print(f"  {i}. {suggestion}")

print("\n" + "=" * 80)
print("✅ 评估完成")
print("=" * 80)

