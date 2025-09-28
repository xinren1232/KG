#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
合并所有补充数据生成完整的导入脚本
"""

import json
from datetime import datetime

def merge_all_data():
    """合并所有补充数据"""
    
    print("🚀 开始合并所有补充数据...")
    
    # 读取现有的Cypher脚本
    scripts_to_merge = [
        ('补充数据导入脚本.cypher', '基础补充数据'),
        ('硬件模块数据导入脚本.cypher', '硬件模块数据')
    ]
    
    all_statements = []
    script_stats = {}
    
    for script_file, script_name in scripts_to_merge:
        try:
            with open(script_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 提取CREATE语句
            lines = content.split('\n')
            statements = [line.strip() for line in lines if line.strip().startswith('CREATE')]
            
            print(f"✅ {script_name}: {len(statements)} 条CREATE语句")
            script_stats[script_name] = len(statements)
            all_statements.extend(statements)
            
        except Exception as e:
            print(f"❌ 读取 {script_name} 失败: {e}")
    
    total_statements = len(all_statements)
    print(f"\n📊 总计: {total_statements} 条CREATE语句")
    
    # 统计Label分布
    label_counts = {}
    for statement in all_statements:
        # 提取Label (CREATE (:Label {...})
        if 'CREATE (:' in statement:
            start = statement.find('CREATE (:') + 9
            end = statement.find(' {', start)
            if end > start:
                label = statement[start:end]
                label_counts[label] = label_counts.get(label, 0) + 1
    
    print(f"\n📋 合并后Label分布:")
    for label, count in sorted(label_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {label}: {count}条")
    
    # 生成完整的合并脚本
    with open('完整词典补充数据导入脚本.cypher', 'w', encoding='utf-8') as f:
        f.write("// 完整词典补充数据导入脚本\n")
        f.write(f"// 生成时间: {datetime.now().isoformat()}\n")
        f.write(f"// 总计: {total_statements}条补充数据\n")
        f.write("// 包含: 基础补充数据(139条) + 硬件模块数据(95条)\n")
        f.write("//\n")
        f.write("// 数据来源:\n")
        for script_name, count in script_stats.items():
            f.write(f"//   - {script_name}: {count}条\n")
        f.write("//\n")
        f.write("// Label分布:\n")
        for label, count in sorted(label_counts.items(), key=lambda x: x[1], reverse=True):
            f.write(f"//   - {label}: {count}条\n")
        f.write("\n")
        
        # 按Label分组写入
        for label in sorted(label_counts.keys()):
            label_statements = [stmt for stmt in all_statements if f'CREATE (:{label} ' in stmt]
            if label_statements:
                f.write(f"// ========== {label} ({len(label_statements)}条) ==========\n")
                for stmt in label_statements:
                    f.write(stmt + "\n")
                f.write("\n")
    
    print(f"\n✅ 完整合并脚本已生成: 完整词典补充数据导入脚本.cypher")
    print(f"包含 {total_statements} 条CREATE语句，按Label分组排列")
    
    # 生成合并统计报告
    merge_report = {
        'merge_time': datetime.now().isoformat(),
        'total_statements': total_statements,
        'source_scripts': script_stats,
        'label_distribution': label_counts,
        'files_generated': ['完整词典补充数据导入脚本.cypher'],
        'summary': {
            'basic_supplement': script_stats.get('基础补充数据', 0),
            'hardware_modules': script_stats.get('硬件模块数据', 0),
            'total_new_data': total_statements,
            'estimated_final_total': 526 + total_statements  # 原有526条 + 新增数据
        }
    }
    
    with open('完整补充数据合并报告.json', 'w', encoding='utf-8') as f:
        json.dump(merge_report, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 合并报告已生成: 完整补充数据合并报告.json")
    
    return total_statements, label_counts, script_stats

def main():
    print("📋 词典补充数据合并处理...")
    
    total, labels, sources = merge_all_data()
    
    if total > 0:
        print(f"\n📈 合并完成!")
        print(f"总计合并: {total}条补充数据")
        print(f"数据来源: {len(sources)}个脚本文件")
        
        print(f"\n🎯 数据构成:")
        for source, count in sources.items():
            print(f"• {source}: {count}条")
        
        print(f"\n📊 预期效果:")
        original_count = 526
        final_count = original_count + total
        growth_rate = (total / original_count) * 100
        print(f"• 原有数据: {original_count}条")
        print(f"• 新增数据: {total}条")
        print(f"• 最终总量: {final_count}条")
        print(f"• 增长率: +{growth_rate:.1f}%")
        
        print(f"\n💡 下一步:")
        print(f"1. 等待Neo4j认证问题解决")
        print(f"2. 执行完整补充数据导入脚本")
        print(f"3. 验证{total}条新数据导入结果")
        print(f"4. 更新前端界面显示新数据")
    
    else:
        print("❌ 数据合并失败")

if __name__ == "__main__":
    main()
