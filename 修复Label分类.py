#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复Label分类 - 将所有词典数据重新映射到标准的8个Label
"""

import json
from pathlib import Path
from datetime import datetime

# 标准的8个Label定义
STANDARD_LABELS = {
    'Symptom': '症状',      # 异常现象描述
    'Component': '组件',    # 硬件部件
    'Tool': '工具',         # 检测工具、方法
    'Process': '流程',      # 制造/质量流程
    'TestCase': '测试用例', # 测试方法
    'Metric': '性能指标',   # 量化指标
    'Material': '物料',     # 原材料
    'Role': '角色'          # 组织职责
}

# 分类映射规则
CATEGORY_MAPPING = {
    # Symptom (症状) - 异常现象描述
    'Symptom': 'Symptom',
    '异常现象': 'Symptom',
    '症状': 'Symptom',
    '故障': 'Symptom',
    '缺陷': 'Symptom',
    
    # Component (组件) - 硬件部件
    'Component': 'Component',
    'components': 'Component',
    '组件': 'Component',
    '硬件相关': 'Component',
    '部件': 'Component',
    '器件': 'Component',
    '摄像头模组': 'Component',
    '显示相关': 'Component',
    '影像相关': 'Component',
    '结构相关': 'Component',
    
    # Tool (工具) - 检测工具、方法
    'Tool': 'Tool',
    '工具': 'Tool',
    '设备': 'Tool',
    '仪器': 'Tool',
    '测试设备': 'Tool',
    
    # Process (流程) - 制造/质量流程
    'Process': 'Process',
    '流程': 'Process',
    '工艺': 'Process',
    '制造工艺': 'Process',
    '流程相关': 'Process',
    '工艺流程': 'Process',
    
    # TestCase (测试用例) - 测试方法
    'TestCase': 'TestCase',
    '测试用例': 'TestCase',
    '测试方法': 'TestCase',
    '测试验证': 'TestCase',
    '验证': 'TestCase',
    
    # Metric (性能指标) - 量化指标
    'Metric': 'Metric',
    '性能指标': 'Metric',
    '指标': 'Metric',
    '参数': 'Metric',
    '规格': 'Metric',
    
    # Material (物料) - 原材料
    'Material': 'Material',
    '物料': 'Material',
    '材料': 'Material',
    '原料': 'Material',
    
    # Role (角色) - 组织职责
    'Role': 'Role',
    '角色': 'Role',
    '职责': 'Role',
    '组织职责': 'Role',
    '岗位': 'Role'
}

# 基于关键词的智能分类
KEYWORD_CLASSIFICATION = {
    'Symptom': [
        '异常', '故障', '失效', '缺陷', '问题', '错误', '不良', '坏点', '白点', '黄斑', 
        '漏光', '闪烁', '卡顿', '发热', '噪音', '振动', '松动', '脱落', '开裂',
        '变色', '褪色', '划痕', '磨损', '腐蚀', '氧化', '短路', '断路', '虚焊'
    ],
    'Component': [
        '芯片', '电路', '连接器', '传感器', '摄像头', '显示屏', '电池', '天线', 
        '扬声器', '麦克风', '马达', '按键', '外壳', '中框', '后盖', '镜头',
        'PCB', 'FPC', 'BTB', 'OLED', 'LCD', 'CPU', 'GPU', 'RAM', 'ROM',
        '电容', '电阻', '电感', '二极管', '三极管', '晶振', '滤波器'
    ],
    'Tool': [
        '测试仪', '示波器', '万用表', '频谱仪', '显微镜', '探针', '治具', '夹具',
        '测试台', '老化箱', '恒温箱', '振动台', '跌落台', '拉力机', '硬度计',
        'ICT', 'FCT', 'AOI', 'SPI', 'X-Ray', '光谱仪', '色差仪'
    ],
    'Process': [
        '工艺', '流程', '制程', '生产', '制造', '装配', '焊接', '贴片', '封装',
        '测试', '检验', '校准', '调试', '老化', '筛选', '分拣', '包装',
        '喷涂', '电镀', '阳极氧化', '激光', '蚀刻', '清洗', '烘烤'
    ],
    'TestCase': [
        '测试', '验证', '检测', '校验', '评估', '分析', '诊断', '排查',
        '功能测试', '性能测试', '可靠性测试', '环境测试', '兼容性测试',
        '压力测试', '老化测试', '温度测试', '湿度测试', '振动测试'
    ],
    'Metric': [
        '频率', '电压', '电流', '功率', '温度', '湿度', '压力', '速度', '精度',
        '分辨率', '亮度', '对比度', '色域', '响应时间', '刷新率', '帧率',
        '容量', '密度', '厚度', '重量', '尺寸', '角度', '距离', '时间',
        '效率', '良率', '合格率', '不良率', 'PPM', 'DPM', 'FIT'
    ],
    'Material': [
        '材料', '物料', '原料', '基材', '涂料', '胶水', '焊料', '助焊剂',
        '塑料', '金属', '玻璃', '陶瓷', '硅胶', '泡棉', '胶带', '薄膜',
        '铜', '铝', '钢', '镁', '钛', '银', '金', '锡', '铅'
    ],
    'Role': [
        '工程师', '技术员', '操作员', '检验员', '质检员', '测试员', '调试员',
        '经理', '主管', '专员', '分析师', '设计师', '开发', '维护', '支持'
    ]
}

def classify_by_keywords(term, description, tags):
    """基于关键词智能分类"""
    text = f"{term} {description} {' '.join(tags)}".lower()
    
    scores = {}
    for label, keywords in KEYWORD_CLASSIFICATION.items():
        score = 0
        for keyword in keywords:
            if keyword.lower() in text:
                score += 1
        scores[label] = score
    
    # 返回得分最高的分类
    if scores:
        best_label = max(scores, key=scores.get)
        if scores[best_label] > 0:
            return best_label
    
    return 'Component'  # 默认分类

def fix_label_classification():
    """修复Label分类"""
    print("🔧 修复Label分类...")
    
    # 读取当前数据
    input_file = Path("api/data/dictionary.json")
    
    if not input_file.exists():
        print(f"❌ 词典文件不存在: {input_file}")
        return False
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"📊 原始数据: {len(data)} 条")
        
        # 备份原始文件
        backup_file = Path(f"api/data/dictionary_before_label_fix_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"💾 备份文件: {backup_file}")
        
        # 统计原始分类
        original_categories = {}
        for item in data:
            category = item.get('category', '未分类')
            original_categories[category] = original_categories.get(category, 0) + 1
        
        print(f"📊 原始分类分布:")
        for cat, count in sorted(original_categories.items(), key=lambda x: x[1], reverse=True):
            print(f"  {cat}: {count} 条")
        
        # 修复分类
        fixed_data = []
        classification_stats = {label: 0 for label in STANDARD_LABELS.keys()}
        
        for item in data:
            fixed_item = fix_single_item_classification(item)
            fixed_data.append(fixed_item)
            
            new_category = fixed_item['category']
            if new_category in classification_stats:
                classification_stats[new_category] += 1
        
        print(f"✅ 分类修复完成: {len(fixed_data)} 条")
        
        # 显示新分类分布
        print(f"📊 修复后分类分布:")
        for label, count in sorted(classification_stats.items(), key=lambda x: x[1], reverse=True):
            chinese_name = STANDARD_LABELS[label]
            print(f"  {label} ({chinese_name}): {count} 条")
        
        # 保存修复后的数据
        with open(input_file, 'w', encoding='utf-8') as f:
            json.dump(fixed_data, f, ensure_ascii=False, indent=2)
        
        print(f"💾 修复后数据已保存: {input_file}")
        
        # 生成分类修复报告
        generate_classification_report(original_categories, classification_stats)
        
        return True
        
    except Exception as e:
        print(f"❌ 修复过程出错: {e}")
        return False

def fix_single_item_classification(item):
    """修复单个条目的分类"""
    if not isinstance(item, dict):
        return item
    
    # 获取原始分类
    original_category = item.get('category', '').strip()
    term = item.get('term', '').strip()
    description = item.get('description', '').strip()
    tags = item.get('tags', [])
    
    # 1. 首先尝试直接映射
    new_category = CATEGORY_MAPPING.get(original_category)
    
    # 2. 如果直接映射失败，使用智能分类
    if not new_category:
        new_category = classify_by_keywords(term, description, tags)
    
    # 3. 确保分类有效
    if new_category not in STANDARD_LABELS:
        new_category = 'Component'  # 默认分类
    
    # 更新条目
    fixed_item = item.copy()
    fixed_item['category'] = new_category
    fixed_item['original_category'] = original_category  # 保留原始分类用于追踪
    
    return fixed_item

def generate_classification_report(original_categories, new_categories):
    """生成分类修复报告"""
    print("📝 生成分类修复报告...")
    
    report = {
        'fix_time': datetime.now().isoformat(),
        'standard_labels': STANDARD_LABELS,
        'original_distribution': original_categories,
        'new_distribution': new_categories,
        'mapping_rules': CATEGORY_MAPPING,
        'total_original_categories': len(original_categories),
        'total_new_categories': len(new_categories)
    }
    
    # 保存报告
    report_file = Path("Label分类修复报告.json")
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"📄 分类修复报告已保存: {report_file}")

def test_fixed_classification():
    """测试修复后的分类"""
    print("🔍 测试修复后的分类...")
    
    input_file = Path("api/data/dictionary.json")
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"📊 数据总数: {len(data)}")
        
        # 统计分类分布
        category_stats = {}
        for item in data:
            category = item.get('category', '未知')
            category_stats[category] = category_stats.get(category, 0) + 1
        
        print(f"\n📊 最终分类分布:")
        for label in STANDARD_LABELS.keys():
            count = category_stats.get(label, 0)
            chinese_name = STANDARD_LABELS[label]
            print(f"  {label} ({chinese_name}): {count} 条")
        
        # 检查是否有非标准分类
        non_standard = {k: v for k, v in category_stats.items() if k not in STANDARD_LABELS}
        if non_standard:
            print(f"\n⚠️ 非标准分类:")
            for cat, count in non_standard.items():
                print(f"  {cat}: {count} 条")
        else:
            print(f"\n✅ 所有分类都符合标准8个Label")
        
        # 显示每个分类的示例
        print(f"\n📋 分类示例:")
        for label in STANDARD_LABELS.keys():
            examples = [item for item in data if item.get('category') == label][:2]
            chinese_name = STANDARD_LABELS[label]
            print(f"\n{label} ({chinese_name}):")
            for example in examples:
                print(f"  - {example.get('term', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 修复Label分类")
    print("=" * 50)
    
    print("📋 标准8个Label:")
    for label, chinese in STANDARD_LABELS.items():
        print(f"  {label} ({chinese})")
    
    print("\n" + "=" * 50)
    
    # 1. 修复分类
    success = fix_label_classification()
    
    if success:
        # 2. 测试修复结果
        test_fixed_classification()
        
        print("\n" + "=" * 50)
        print("✅ Label分类修复完成!")
        print("💡 下一步:")
        print("  1. 重启API服务")
        print("  2. 刷新前端页面")
        print("  3. 验证分类显示正确")
        print("  4. 检查8个Label分布是否合理")
    else:
        print("\n❌ Label分类修复失败")

if __name__ == "__main__":
    main()
