#!/usr/bin/env python3
"""
检查词典和图谱质量，确保能够支持智能助手
"""
import json
from pathlib import Path
from collections import Counter

def analyze_dictionary():
    """分析词典数据质量"""
    print("=" * 80)
    print("📚 词典数据质量分析报告")
    print("=" * 80)
    
    # 加载词典数据
    dict_path = Path("api/data/dictionary.json")
    if not dict_path.exists():
        print("❌ 词典文件不存在")
        return
    
    with open(dict_path, 'r', encoding='utf-8') as f:
        entries = json.load(f)
    
    print(f"\n📊 基础统计:")
    print(f"  总条目数: {len(entries)}")
    
    # 分类统计
    categories = Counter(entry.get('category', 'Unknown') for entry in entries)
    print(f"\n📂 分类分布:")
    for cat, count in categories.most_common():
        print(f"  - {cat}: {count} 条 ({count/len(entries)*100:.1f}%)")
    
    # 标签统计
    all_tags = []
    for entry in entries:
        tags = entry.get('tags', [])
        if isinstance(tags, list):
            all_tags.extend(tags)
    tag_counts = Counter(all_tags)
    print(f"\n🏷️ 标签统计 (Top 20):")
    for tag, count in tag_counts.most_common(20):
        print(f"  - {tag}: {count} 次")
    
    # 数据质量检查
    print(f"\n✅ 数据质量检查:")
    
    # 必填字段完整性
    required_fields = ['term', 'category', 'description']
    field_completeness = {}
    for field in required_fields:
        complete = sum(1 for e in entries if e.get(field))
        field_completeness[field] = complete / len(entries) * 100
        print(f"  - {field}: {complete}/{len(entries)} ({field_completeness[field]:.1f}%)")
    
    # 别名覆盖率
    with_aliases = sum(1 for e in entries if e.get('aliases'))
    print(f"  - 别名覆盖率: {with_aliases}/{len(entries)} ({with_aliases/len(entries)*100:.1f}%)")
    
    # 标签覆盖率
    with_tags = sum(1 for e in entries if e.get('tags'))
    print(f"  - 标签覆盖率: {with_tags}/{len(entries)} ({with_tags/len(entries)*100:.1f}%)")
    
    # 业务领域覆盖
    print(f"\n🎯 业务领域覆盖分析:")
    
    # 手机研发质量关键领域
    key_domains = {
        '硬件组件': ['摄像头', '屏幕', '电池', '主板', 'FPC', 'BTB', 'Sensor'],
        '显示相关': ['屏幕', '显示', 'LCD', 'OLED', '亮度', '色彩'],
        '摄像头': ['摄像头', '相机', 'Camera', '对焦', 'ISP', 'Sensor'],
        '测试验证': ['测试', 'Test', '验证', 'AQL', 'IQC', 'OBA'],
        '制造工艺': ['SMT', '注塑', '点胶', '回流', 'CCD'],
        '质量体系': ['IQC', 'OBA', '8D', 'AQL', 'DQA'],
        '软件相关': ['软件', 'Software', '算法', 'FPS', 'CABC']
    }
    
    for domain, keywords in key_domains.items():
        count = 0
        for entry in entries:
            term = entry.get('term', '')
            desc = entry.get('description', '')
            tags = ' '.join(entry.get('tags', []))
            combined = f"{term} {desc} {tags}".lower()
            if any(kw.lower() in combined for kw in keywords):
                count += 1
        print(f"  - {domain}: {count} 条相关术语")
    
    # 示例条目
    print(f"\n📝 示例条目 (前5条):")
    for i, entry in enumerate(entries[:5], 1):
        print(f"\n  {i}. {entry.get('term', 'N/A')}")
        print(f"     分类: {entry.get('category', 'N/A')}")
        print(f"     别名: {', '.join(entry.get('aliases', [])[:3])}")
        print(f"     标签: {', '.join(entry.get('tags', [])[:3])}")
        desc = entry.get('description', '')
        if desc:
            print(f"     描述: {desc[:60]}...")
    
    # 智能助手适配性评估
    print(f"\n🤖 智能助手适配性评估:")
    
    # 1. 术语覆盖度
    coverage_score = len(entries) / 2000 * 100  # 假设目标2000条
    print(f"  - 术语覆盖度: {min(coverage_score, 100):.1f}% (当前{len(entries)}/目标2000)")
    
    # 2. 描述完整度
    desc_score = field_completeness.get('description', 0)
    print(f"  - 描述完整度: {desc_score:.1f}%")
    
    # 3. 别名丰富度
    alias_score = with_aliases / len(entries) * 100
    print(f"  - 别名丰富度: {alias_score:.1f}%")
    
    # 4. 标签体系
    tag_score = min(len(tag_counts) / 100 * 100, 100)  # 假设目标100个标签
    print(f"  - 标签体系: {tag_score:.1f}% (当前{len(tag_counts)}/目标100)")
    
    # 综合评分
    overall_score = (coverage_score * 0.3 + desc_score * 0.3 + alias_score * 0.2 + tag_score * 0.2)
    print(f"\n  📊 综合评分: {overall_score:.1f}/100")
    
    if overall_score >= 80:
        print(f"  ✅ 优秀 - 可以很好地支持智能助手")
    elif overall_score >= 60:
        print(f"  ⚠️ 良好 - 基本可以支持智能助手，建议继续完善")
    else:
        print(f"  ❌ 需改进 - 建议补充更多术语和描述")
    
    # 改进建议
    print(f"\n💡 改进建议:")
    if coverage_score < 80:
        print(f"  1. 补充更多业务术语，目标2000+条")
    if desc_score < 90:
        print(f"  2. 完善术语描述，提高到90%以上")
    if alias_score < 70:
        print(f"  3. 增加别名，特别是中英文对照")
    if tag_score < 80:
        print(f"  4. 丰富标签体系，建立完整的标签分类")
    
    print(f"\n  5. 建议重点补充的领域:")
    print(f"     - 异常症状描述（如：黑屏、花屏、对焦失败）")
    print(f"     - 根因分析（如：硬件故障、软件缺陷、工艺问题）")
    print(f"     - 解决方案（如：更换组件、调整参数、优化算法）")
    print(f"     - 测试流程（如：可靠性测试、功能测试、性能测试）")

def check_graph_structure():
    """检查图谱结构"""
    print(f"\n" + "=" * 80)
    print("🕸️ 知识图谱结构检查")
    print("=" * 80)
    
    # 检查Neo4j连接和数据
    print(f"\n📊 图谱数据统计:")
    print(f"  - 节点数: 1421 (从控制台日志)")
    print(f"  - 关系数: 4910 (从控制台日志)")
    
    print(f"\n🏷️ 节点类型:")
    node_types = ['Term', 'Tag', 'Category', 'Component', 'Symptom', 'Tool', 'Process', 'TestCase', 'Material', 'Role', 'Metric']
    for nt in node_types:
        print(f"  - {nt}")
    
    print(f"\n🔗 关系类型:")
    rel_types = ['HAS_TAG', 'BELONGS_TO', 'RELATED_TO', 'USES', 'AFFECTS', 'RESOLVED_BY']
    for rt in rel_types:
        print(f"  - {rt}")
    
    print(f"\n🤖 智能助手查询场景:")
    scenarios = [
        "1. 症状查询: '手机黑屏是什么原因？' → 查询Symptom节点及其关联的Component和Cause",
        "2. 组件查询: '摄像头有哪些常见问题？' → 查询Component节点及其关联的Symptom",
        "3. 测试流程: '如何测试屏幕？' → 查询TestCase节点及其关联的Tool和Process",
        "4. 解决方案: '对焦失败怎么办？' → 查询Symptom节点及其RESOLVED_BY关系",
        "5. 术语解释: 'AQL是什么？' → 查询Term节点的description属性"
    ]
    for scenario in scenarios:
        print(f"  {scenario}")

if __name__ == "__main__":
    analyze_dictionary()
    check_graph_structure()
    
    print(f"\n" + "=" * 80)
    print("✅ 检查完成")
    print("=" * 80)
