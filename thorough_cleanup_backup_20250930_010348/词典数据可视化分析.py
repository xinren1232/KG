#!/usr/bin/env python3
"""
词典数据可视化分析
生成词典系统的数据分析图表和统计报告
"""

import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter, defaultdict
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

def load_dictionary_data():
    """加载词典数据"""
    print("📊 加载词典数据...")
    
    try:
        with open('api/data/dictionary.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"  ✅ 成功加载 {len(data)} 条词典数据")
        return data
    except Exception as e:
        print(f"  ❌ 加载失败: {e}")
        return []

def analyze_category_distribution(data):
    """分析分类分布"""
    print("📊 分析分类分布...")
    
    categories = [item.get('category', 'Unknown') for item in data]
    category_counts = Counter(categories)
    
    # 创建分类分布图
    plt.figure(figsize=(12, 8))
    
    # 饼图
    plt.subplot(2, 2, 1)
    colors = plt.cm.Set3(np.linspace(0, 1, len(category_counts)))
    wedges, texts, autotexts = plt.pie(category_counts.values(), 
                                       labels=category_counts.keys(),
                                       autopct='%1.1f%%',
                                       colors=colors,
                                       startangle=90)
    plt.title('词典分类分布 (饼图)', fontsize=14, fontweight='bold')
    
    # 柱状图
    plt.subplot(2, 2, 2)
    bars = plt.bar(category_counts.keys(), category_counts.values(), 
                   color=colors[:len(category_counts)])
    plt.title('词典分类分布 (柱状图)', fontsize=14, fontweight='bold')
    plt.xlabel('分类')
    plt.ylabel('数量')
    plt.xticks(rotation=45)
    
    # 添加数值标签
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{int(height)}', ha='center', va='bottom')
    
    # 水平柱状图
    plt.subplot(2, 2, 3)
    y_pos = np.arange(len(category_counts))
    plt.barh(y_pos, list(category_counts.values()), color=colors[:len(category_counts)])
    plt.yticks(y_pos, list(category_counts.keys()))
    plt.xlabel('数量')
    plt.title('词典分类分布 (水平)', fontsize=14, fontweight='bold')
    
    # 添加数值标签
    for i, v in enumerate(category_counts.values()):
        plt.text(v + 5, i, str(v), va='center')
    
    # 累积分布
    plt.subplot(2, 2, 4)
    sorted_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
    cumulative = np.cumsum([count for _, count in sorted_categories])
    plt.plot(range(len(cumulative)), cumulative, 'o-', linewidth=2, markersize=8)
    plt.xlabel('分类排名')
    plt.ylabel('累积数量')
    plt.title('分类累积分布', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('词典分类分布分析.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return category_counts

def analyze_tag_distribution(data):
    """分析标签分布"""
    print("📊 分析标签分布...")
    
    all_tags = []
    for item in data:
        tags = item.get('tags', [])
        if isinstance(tags, list):
            all_tags.extend(tags)
        elif isinstance(tags, str):
            all_tags.extend([tag.strip() for tag in tags.split(',') if tag.strip()])
    
    tag_counts = Counter(all_tags)
    top_20_tags = dict(tag_counts.most_common(20))
    
    # 创建标签分布图
    plt.figure(figsize=(15, 10))
    
    # TOP 20标签柱状图
    plt.subplot(2, 2, 1)
    bars = plt.bar(range(len(top_20_tags)), list(top_20_tags.values()), 
                   color=plt.cm.viridis(np.linspace(0, 1, len(top_20_tags))))
    plt.title('TOP 20 标签使用频率', fontsize=14, fontweight='bold')
    plt.xlabel('标签')
    plt.ylabel('使用次数')
    plt.xticks(range(len(top_20_tags)), list(top_20_tags.keys()), rotation=45, ha='right')
    
    # 添加数值标签
    for i, bar in enumerate(bars):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{int(height)}', ha='center', va='bottom', fontsize=8)
    
    # 标签使用分布直方图
    plt.subplot(2, 2, 2)
    usage_counts = list(tag_counts.values())
    plt.hist(usage_counts, bins=20, color='skyblue', alpha=0.7, edgecolor='black')
    plt.title('标签使用频率分布', fontsize=14, fontweight='bold')
    plt.xlabel('使用次数')
    plt.ylabel('标签数量')
    plt.grid(True, alpha=0.3)
    
    # 标签长度分布
    plt.subplot(2, 2, 3)
    tag_lengths = [len(tag) for tag in tag_counts.keys()]
    plt.hist(tag_lengths, bins=15, color='lightcoral', alpha=0.7, edgecolor='black')
    plt.title('标签长度分布', fontsize=14, fontweight='bold')
    plt.xlabel('标签长度 (字符数)')
    plt.ylabel('标签数量')
    plt.grid(True, alpha=0.3)
    
    # 标签使用率分析
    plt.subplot(2, 2, 4)
    total_items = len(data)
    usage_rates = [(count/total_items)*100 for count in tag_counts.values()]
    plt.scatter(range(len(usage_rates)), sorted(usage_rates, reverse=True), 
               alpha=0.6, s=30, c=range(len(usage_rates)), cmap='plasma')
    plt.title('标签使用率分布', fontsize=14, fontweight='bold')
    plt.xlabel('标签排名')
    plt.ylabel('使用率 (%)')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('词典标签分布分析.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return tag_counts

def analyze_data_quality(data):
    """分析数据质量"""
    print("📊 分析数据质量...")
    
    total_items = len(data)
    quality_metrics = {}
    
    # 字段完整性分析
    fields = ['term', 'aliases', 'category', 'tags', 'description']
    completeness = {}
    
    for field in fields:
        non_empty_count = 0
        for item in data:
            value = item.get(field)
            if value:
                if isinstance(value, list) and len(value) > 0:
                    non_empty_count += 1
                elif isinstance(value, str) and value.strip():
                    non_empty_count += 1
        
        completeness[field] = (non_empty_count / total_items) * 100
    
    # 创建数据质量图表
    plt.figure(figsize=(15, 10))
    
    # 字段完整性
    plt.subplot(2, 3, 1)
    bars = plt.bar(completeness.keys(), completeness.values(), 
                   color=['green' if v >= 90 else 'orange' if v >= 70 else 'red' for v in completeness.values()])
    plt.title('字段完整性分析', fontsize=14, fontweight='bold')
    plt.ylabel('完整率 (%)')
    plt.xticks(rotation=45)
    plt.ylim(0, 100)
    
    # 添加数值标签
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height:.1f}%', ha='center', va='bottom')
    
    # 别名数量分布
    plt.subplot(2, 3, 2)
    alias_counts = []
    for item in data:
        aliases = item.get('aliases', [])
        if isinstance(aliases, list):
            alias_counts.append(len(aliases))
        else:
            alias_counts.append(0)
    
    plt.hist(alias_counts, bins=10, color='lightblue', alpha=0.7, edgecolor='black')
    plt.title('别名数量分布', fontsize=14, fontweight='bold')
    plt.xlabel('别名数量')
    plt.ylabel('词条数量')
    plt.grid(True, alpha=0.3)
    
    # 标签数量分布
    plt.subplot(2, 3, 3)
    tag_counts_per_item = []
    for item in data:
        tags = item.get('tags', [])
        if isinstance(tags, list):
            tag_counts_per_item.append(len(tags))
        else:
            tag_counts_per_item.append(0)
    
    plt.hist(tag_counts_per_item, bins=10, color='lightgreen', alpha=0.7, edgecolor='black')
    plt.title('每条词典的标签数量分布', fontsize=14, fontweight='bold')
    plt.xlabel('标签数量')
    plt.ylabel('词条数量')
    plt.grid(True, alpha=0.3)
    
    # 描述长度分布
    plt.subplot(2, 3, 4)
    description_lengths = []
    for item in data:
        desc = item.get('description', '')
        if isinstance(desc, str):
            description_lengths.append(len(desc))
        else:
            description_lengths.append(0)
    
    plt.hist(description_lengths, bins=20, color='lightyellow', alpha=0.7, edgecolor='black')
    plt.title('描述长度分布', fontsize=14, fontweight='bold')
    plt.xlabel('描述长度 (字符数)')
    plt.ylabel('词条数量')
    plt.grid(True, alpha=0.3)
    
    # 术语长度分布
    plt.subplot(2, 3, 5)
    term_lengths = []
    for item in data:
        term = item.get('term', '')
        if isinstance(term, str):
            term_lengths.append(len(term))
        else:
            term_lengths.append(0)
    
    plt.hist(term_lengths, bins=15, color='lightpink', alpha=0.7, edgecolor='black')
    plt.title('术语长度分布', fontsize=14, fontweight='bold')
    plt.xlabel('术语长度 (字符数)')
    plt.ylabel('词条数量')
    plt.grid(True, alpha=0.3)
    
    # 质量评分雷达图
    plt.subplot(2, 3, 6)
    categories = list(completeness.keys())
    values = list(completeness.values())
    
    # 计算角度
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    values += values[:1]  # 闭合图形
    angles += angles[:1]
    
    ax = plt.subplot(2, 3, 6, projection='polar')
    ax.plot(angles, values, 'o-', linewidth=2, color='blue')
    ax.fill(angles, values, alpha=0.25, color='blue')
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    ax.set_ylim(0, 100)
    ax.set_title('数据质量雷达图', fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig('词典数据质量分析.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return completeness

def generate_summary_report(data, category_counts, tag_counts, completeness):
    """生成总结报告"""
    print("📊 生成总结报告...")
    
    total_items = len(data)
    total_categories = len(category_counts)
    total_tags = len(tag_counts)
    
    # 计算平均值
    avg_aliases = np.mean([len(item.get('aliases', [])) if isinstance(item.get('aliases', []), list) else 0 for item in data])
    avg_tags = np.mean([len(item.get('tags', [])) if isinstance(item.get('tags', []), list) else 0 for item in data])
    avg_description_length = np.mean([len(item.get('description', '')) if isinstance(item.get('description', ''), str) else 0 for item in data])
    
    # 生成报告
    report = f"""
# 📊 词典数据分析总结报告

## 🎯 数据概览
- **总词条数**: {total_items:,} 条
- **分类数量**: {total_categories} 个
- **标签数量**: {total_tags} 个
- **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📊 分类分布
"""
    
    for category, count in category_counts.most_common():
        percentage = (count / total_items) * 100
        report += f"- **{category}**: {count} 条 ({percentage:.1f}%)\n"
    
    report += f"""
## 🏷️ 标签使用情况
- **最常用标签**: {tag_counts.most_common(1)[0][0]} ({tag_counts.most_common(1)[0][1]} 次)
- **标签使用总次数**: {sum(tag_counts.values())} 次
- **平均每条词典标签数**: {avg_tags:.1f} 个

### TOP 10 标签
"""
    
    for tag, count in tag_counts.most_common(10):
        usage_rate = (count / total_items) * 100
        report += f"- **{tag}**: {count} 次 ({usage_rate:.1f}%)\n"
    
    report += f"""
## 📈 数据质量指标
- **平均别名数**: {avg_aliases:.1f} 个
- **平均描述长度**: {avg_description_length:.0f} 字符

### 字段完整性
"""
    
    for field, completeness_rate in completeness.items():
        status = "优秀" if completeness_rate >= 90 else "良好" if completeness_rate >= 70 else "需改进"
        report += f"- **{field}**: {completeness_rate:.1f}% ({status})\n"
    
    report += f"""
## 🎯 关键发现
1. **数据规模**: 共 {total_items:,} 条词典数据，规模较大
2. **分类均衡**: {category_counts.most_common(1)[0][0]} 类别占比最高 ({(category_counts.most_common(1)[0][1]/total_items)*100:.1f}%)
3. **标签丰富**: 共使用 {total_tags} 个不同标签，标签体系完整
4. **质量水平**: 整体数据质量良好，核心字段完整性高

## 💡 改进建议
1. **平衡分类分布**: 补充数量较少的分类数据
2. **优化标签使用**: 提高低频标签的使用率
3. **完善描述信息**: 提高描述字段的完整性
4. **标准化管理**: 建立更严格的数据质量控制流程

---
*报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    # 保存报告
    with open('词典数据分析报告.md', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("  ✅ 报告已保存: 词典数据分析报告.md")
    return report

def main():
    """主函数"""
    print("🔍 词典数据可视化分析")
    print("=" * 50)
    
    # 加载数据
    data = load_dictionary_data()
    if not data:
        print("❌ 无法加载数据，退出分析")
        return
    
    # 分析分类分布
    category_counts = analyze_category_distribution(data)
    
    # 分析标签分布
    tag_counts = analyze_tag_distribution(data)
    
    # 分析数据质量
    completeness = analyze_data_quality(data)
    
    # 生成总结报告
    report = generate_summary_report(data, category_counts, tag_counts, completeness)
    
    print("\n" + "=" * 50)
    print("📊 分析完成！生成的文件:")
    print("  📈 词典分类分布分析.png")
    print("  🏷️ 词典标签分布分析.png")
    print("  📊 词典数据质量分析.png")
    print("  📋 词典数据分析报告.md")
    print("\n🎉 词典数据可视化分析完成！")

if __name__ == "__main__":
    main()
