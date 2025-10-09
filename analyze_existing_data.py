#!/usr/bin/env python3
"""
分析现有词典数据，提取设计规范和质量标准
"""
import json
from collections import Counter, defaultdict

def analyze_existing_dictionary():
    """分析现有词典的设计规范"""
    print("=" * 80)
    print("📚 现有词典数据分析 - 提取设计规范")
    print("=" * 80)
    
    with open('api/data/dictionary.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"\n总条目数: {len(data)}")
    
    # 1. 分析字段结构
    print(f"\n📋 字段结构分析:")
    if data:
        sample = data[0]
        print(f"标准字段: {list(sample.keys())}")
        for key, value in sample.items():
            print(f"  - {key}: {type(value).__name__} = {str(value)[:60]}...")
    
    # 2. 分析分类分布
    print(f"\n📂 分类(category)分布:")
    categories = Counter(e.get('category', 'Unknown') for e in data)
    for cat, count in categories.most_common():
        print(f"  {cat}: {count}条")
    
    # 3. 分析标签使用
    print(f"\n🏷️ 标签(tags)使用分析:")
    all_tags = []
    for entry in data:
        tags = entry.get('tags', [])
        if isinstance(tags, list):
            all_tags.extend(tags)
    tag_counts = Counter(all_tags)
    print(f"  总标签数: {len(tag_counts)}")
    print(f"  Top 20标签:")
    for tag, count in tag_counts.most_common(20):
        print(f"    - {tag}: {count}次")
    
    # 4. 分析摄像头相关数据
    print(f"\n📷 摄像头相关数据分析:")
    camera_keywords = ['摄像头', 'Camera', '对焦', '镜头', 'Lens', '影像', 'VCM', 'ISP', 'OIS']
    camera_entries = []
    for entry in data:
        term = entry.get('term', '')
        desc = entry.get('description', '')
        tags = ' '.join(entry.get('tags', []))
        combined = f"{term} {desc} {tags}"
        if any(kw in combined for kw in camera_keywords):
            camera_entries.append(entry)
    
    print(f"  摄像头相关条目: {len(camera_entries)}条")
    
    # 按分类统计
    camera_by_category = defaultdict(list)
    for entry in camera_entries:
        camera_by_category[entry.get('category', 'Unknown')].append(entry)
    
    print(f"  分类分布:")
    for cat, entries in sorted(camera_by_category.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"    {cat}: {len(entries)}条")
    
    # 显示示例
    print(f"\n  Component类示例 (前3条):")
    for i, entry in enumerate([e for e in camera_entries if e.get('category')=='Component'][:3], 1):
        print(f"    {i}. {entry.get('term')}")
        print(f"       别名: {', '.join(entry.get('aliases', [])[:3])}")
        print(f"       标签: {', '.join(entry.get('tags', [])[:3])}")
        print(f"       描述: {entry.get('description', '')[:80]}...")
    
    print(f"\n  Symptom类示例 (前3条):")
    for i, entry in enumerate([e for e in camera_entries if e.get('category')=='Symptom'][:3], 1):
        print(f"    {i}. {entry.get('term')}")
        print(f"       别名: {', '.join(entry.get('aliases', [])[:3])}")
        print(f"       标签: {', '.join(entry.get('tags', [])[:3])}")
        desc = entry.get('description', '')
        if '**定义**' in desc:
            print(f"       描述: [结构化描述]")
        else:
            print(f"       描述: {desc[:80]}...")
    
    # 5. 分析描述格式
    print(f"\n📝 描述(description)格式分析:")
    structured_count = 0
    simple_count = 0
    for entry in data:
        desc = entry.get('description', '')
        if '**定义**' in desc or '**判定口径**' in desc:
            structured_count += 1
        else:
            simple_count += 1
    
    print(f"  结构化描述: {structured_count}条 ({structured_count/len(data)*100:.1f}%)")
    print(f"  简单描述: {simple_count}条 ({simple_count/len(data)*100:.1f}%)")
    
    # 显示结构化描述示例
    structured_examples = [e for e in data if '**定义**' in e.get('description', '')]
    if structured_examples:
        print(f"\n  结构化描述示例:")
        example = structured_examples[0]
        print(f"    术语: {example.get('term')}")
        print(f"    描述: {example.get('description', '')[:200]}...")
    
    # 6. 分析别名格式
    print(f"\n🔤 别名(aliases)格式分析:")
    alias_counts = [len(e.get('aliases', [])) for e in data]
    avg_aliases = sum(alias_counts) / len(alias_counts) if alias_counts else 0
    print(f"  平均别名数: {avg_aliases:.1f}")
    print(f"  最多别名数: {max(alias_counts)}")
    
    # 显示别名丰富的示例
    rich_alias_entries = sorted(data, key=lambda x: len(x.get('aliases', [])), reverse=True)[:3]
    print(f"\n  别名丰富示例:")
    for i, entry in enumerate(rich_alias_entries, 1):
        print(f"    {i}. {entry.get('term')}: {len(entry.get('aliases', []))}个别名")
        print(f"       {', '.join(entry.get('aliases', [])[:5])}")
    
    # 7. 分析Material类数据
    print(f"\n🧪 Material类数据分析:")
    materials = [e for e in data if e.get('category') == 'Material']
    print(f"  Material条目: {len(materials)}条")
    
    if materials:
        print(f"\n  Material标签分布:")
        material_tags = []
        for m in materials:
            material_tags.extend(m.get('tags', []))
        material_tag_counts = Counter(material_tags)
        for tag, count in material_tag_counts.most_common(10):
            print(f"    - {tag}: {count}次")
        
        print(f"\n  Material示例 (前3条):")
        for i, entry in enumerate(materials[:3], 1):
            print(f"    {i}. {entry.get('term')}")
            print(f"       别名: {', '.join(entry.get('aliases', [])[:2])}")
            print(f"       标签: {', '.join(entry.get('tags', [])[:3])}")
            print(f"       描述: {entry.get('description', '')[:60]}...")
    
    # 8. 提取设计规范
    print(f"\n" + "=" * 80)
    print("📐 提取的设计规范总结")
    print("=" * 80)
    
    print(f"\n1. 字段结构:")
    print(f"   必填字段: term, aliases, category, tags, description")
    print(f"   可选字段: sub_category, source, status, original_category")
    
    print(f"\n2. 分类(category)规范:")
    print(f"   标准分类: {', '.join(categories.keys())}")
    
    print(f"\n3. 标签(tags)规范:")
    print(f"   - 使用数组格式")
    print(f"   - 平均每条{sum(len(e.get('tags',[])) for e in data)/len(data):.1f}个标签")
    print(f"   - 常用标签: 硬件相关、测试验证、可靠性、制造工艺等")
    
    print(f"\n4. 描述(description)规范:")
    print(f"   - 简单描述: 一句话说明术语含义和应用场景")
    print(f"   - 结构化描述: 包含定义、判定口径、常见场景、排查路径、对策")
    print(f"   - 推荐Symptom类使用结构化描述")
    
    print(f"\n5. 别名(aliases)规范:")
    print(f"   - 使用数组格式")
    print(f"   - 包含中文别名、英文全称、英文缩写")
    print(f"   - 平均每条{avg_aliases:.1f}个别名")
    
    print(f"\n6. 摄像头领域规范:")
    print(f"   - Component类: 硬件组件，标签包含'影像相关'、'摄像头模组'")
    print(f"   - Symptom类: 异常现象，标签包含'影像相关'、'摄像头模组'、'异常现象'")
    print(f"   - TestCase类: 测试方法，标签包含'测试验证'、'影像相关'")
    print(f"   - Process类: 工艺流程，标签包含'制造工艺'、'影像相关'")
    
    print(f"\n7. Material类规范:")
    print(f"   - 标签必含'物料'")
    print(f"   - 常用标签: EMC、热管理、显示相关、点胶、结构相关等")
    print(f"   - 描述格式: 说明材料用途和特性")

if __name__ == "__main__":
    analyze_existing_dictionary()
