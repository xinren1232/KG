#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
处理硬件模块词典数据
"""

import pandas as pd
import json
from datetime import datetime

def process_hardware_modules():
    """处理硬件模块数据"""
    
    # 硬件模块文件列表
    module_files = [
        ('硬件模块词典数据_显示屏.csv', '显示屏模块'),
        ('硬件模块词典数据_摄像头.csv', '摄像头模块'),
        ('硬件模块词典数据_电池.csv', '电池模块'),
        ('硬件模块词典数据_主板PCBA.csv', '主板PCBA模块')
    ]
    
    all_data = []
    module_stats = {}
    
    print("🚀 开始处理硬件模块词典数据...")
    
    for file_name, module_name in module_files:
        try:
            df = pd.read_csv(file_name, encoding='utf-8')
            print(f"✅ {module_name}: {len(df)} 条记录")
            
            # 统计Label分布
            label_counts = df['category'].value_counts().to_dict()
            module_stats[module_name] = {
                'total': len(df),
                'labels': label_counts
            }
            
            # 添加到总数据
            all_data.append(df)
            
        except Exception as e:
            print(f"❌ 处理 {module_name} 失败: {e}")
    
    # 合并所有数据
    if all_data:
        df_all = pd.concat(all_data, ignore_index=True)
        total_count = len(df_all)
        print(f"\n📊 硬件模块总计: {total_count} 条新数据")
        
        # 总体Label统计
        total_label_stats = df_all['category'].value_counts().to_dict()
        print("\n📋 总体Label分布:")
        for label, count in sorted(total_label_stats.items(), key=lambda x: x[1], reverse=True):
            print(f"  {label}: {count}条")
        
        # 详细模块统计
        print("\n📋 各模块详细统计:")
        for module_name, stats in module_stats.items():
            print(f"\n🔧 {module_name} ({stats['total']}条):")
            for label, count in sorted(stats['labels'].items(), key=lambda x: x[1], reverse=True):
                print(f"    {label}: {count}条")
        
        # 生成Cypher导入脚本
        cypher_statements = []
        for _, row in df_all.iterrows():
            term = row['term']
            category = row['category']
            
            # 处理别名
            aliases = []
            if pd.notna(row.get('aliases', '')):
                aliases = [alias.strip() for alias in str(row['aliases']).split(';') if alias.strip()]
            
            # 处理标签
            tags = []
            if pd.notna(row.get('tags', '')):
                tags = [tag.strip() for tag in str(row['tags']).split(';') if tag.strip()]
            
            # 构建属性
            properties = []
            properties.append(f"name: '{term.replace(chr(39), chr(39)+chr(39))}'")
            
            if aliases:
                aliases_str = str(aliases).replace("'", '"')
                properties.append(f"aliases: {aliases_str}")
            
            if tags:
                tags_str = str(tags).replace("'", '"')
                properties.append(f"tags: {tags_str}")
            
            if pd.notna(row.get('definition', '')):
                definition = str(row['definition']).replace("'", "''")
                properties.append(f"definition: '{definition}'")
            
            if pd.notna(row.get('example', '')):
                example = str(row['example']).replace("'", "''")
                properties.append(f"example: '{example}'")
            
            if pd.notna(row.get('sub_category', '')):
                sub_category = str(row['sub_category']).replace("'", "''")
                properties.append(f"sub_category: '{sub_category}'")
            
            properties.append(f"source: '硬件模块扩展'")
            properties.append(f"status: 'active'")
            properties.append(f"updated_at: '{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}'")
            
            properties_str = ', '.join(properties)
            cypher = f"CREATE (:{category} {{{properties_str}}});"
            cypher_statements.append(cypher)
        
        # 保存Cypher脚本
        with open('硬件模块数据导入脚本.cypher', 'w', encoding='utf-8') as f:
            f.write("// 硬件模块词典数据导入脚本\n")
            f.write(f"// 生成时间: {datetime.now().isoformat()}\n")
            f.write(f"// 总计: {len(cypher_statements)}条硬件模块数据\n")
            f.write("// 包含: 显示屏、摄像头、电池、主板PCBA四大模块\n\n")
            
            for statement in cypher_statements:
                f.write(statement + "\n")
        
        print(f"\n✅ Cypher脚本已生成: 硬件模块数据导入脚本.cypher")
        print(f"包含 {len(cypher_statements)} 条CREATE语句")
        
        # 生成统计报告
        report = {
            'generation_time': datetime.now().isoformat(),
            'total_records': total_count,
            'modules': module_stats,
            'total_label_distribution': total_label_stats,
            'files_generated': ['硬件模块数据导入脚本.cypher'],
            'module_coverage': {
                '显示屏模块': '24条 - OLED/LCD面板、触控、光学测试',
                '摄像头模块': '24条 - 传感器、镜头、对焦、影像质量',
                '电池模块': '21条 - 电芯、保护板、充电、安全测试',
                '主板PCBA模块': '22条 - PCB、芯片、SMT、电气测试'
            }
        }
        
        with open('硬件模块数据统计报告.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 统计报告已生成: 硬件模块数据统计报告.json")
        
        return total_count, total_label_stats, module_stats
    
    else:
        print("❌ 没有可用的硬件模块数据")
        return 0, {}, {}

def main():
    print("🔧 硬件模块词典数据处理...")
    
    total, label_stats, module_stats = process_hardware_modules()
    
    if total > 0:
        print(f"\n📈 处理完成!")
        print(f"总计处理: {total}条硬件模块数据")
        print(f"涵盖模块: 显示屏、摄像头、电池、主板PCBA")
        
        print(f"\n🎯 重点扩展领域:")
        print(f"• 显示技术: OLED/LCD、触控、光学调试")
        print(f"• 影像技术: 传感器、镜头、对焦、MTF测试")
        print(f"• 电池技术: 电芯、BMS、快充、安全测试")
        print(f"• 电路技术: PCB、芯片、SMT、信号完整性")
        
        print(f"\n💡 下一步:")
        print(f"1. 执行硬件模块Cypher脚本导入数据")
        print(f"2. 验证硬件模块数据导入结果")
        print(f"3. 继续扩展其他硬件模块（射频、音频、传感器等）")
    
    else:
        print("❌ 硬件模块数据处理失败")

if __name__ == "__main__":
    main()
