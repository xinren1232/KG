#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
处理第三批硬件模块词典数据
"""

import pandas as pd
import json
from datetime import datetime

def process_third_batch_hardware_modules():
    """处理第三批硬件模块数据"""
    
    # 第三批硬件模块文件列表
    module_files = [
        ('硬件模块词典数据_传感器.csv', '传感器模块'),
        ('硬件模块词典数据_充电电源.csv', '充电与电源管理模块'),
        ('硬件模块词典数据_马达触觉.csv', '马达与触觉反馈模块'),
        ('硬件模块词典数据_外壳涂层.csv', '外壳涂层与外观模块')
    ]
    
    all_data = []
    module_stats = {}
    
    print("🚀 开始处理第三批硬件模块词典数据...")
    
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
        print(f"\n📊 第三批硬件模块总计: {total_count} 条新数据")
        
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
        with open('第三批硬件模块数据导入脚本.cypher', 'w', encoding='utf-8') as f:
            f.write("// 第三批硬件模块词典数据导入脚本\n")
            f.write(f"// 生成时间: {datetime.now().isoformat()}\n")
            f.write(f"// 总计: {len(cypher_statements)}条第三批硬件模块数据\n")
            f.write("// 包含: 传感器、充电电源、马达触觉、外壳涂层四大模块\n\n")
            
            for statement in cypher_statements:
                f.write(statement + "\n")
        
        print(f"\n✅ Cypher脚本已生成: 第三批硬件模块数据导入脚本.cypher")
        print(f"包含 {len(cypher_statements)} 条CREATE语句")
        
        # 生成统计报告
        report = {
            'generation_time': datetime.now().isoformat(),
            'total_records': total_count,
            'modules': module_stats,
            'total_label_distribution': total_label_stats,
            'files_generated': ['第三批硬件模块数据导入脚本.cypher'],
            'module_coverage': {
                '传感器模块': f'{module_stats.get("传感器模块", {}).get("total", 0)}条 - 加速度计、陀螺仪、传感器融合',
                '充电与电源管理模块': f'{module_stats.get("充电与电源管理模块", {}).get("total", 0)}条 - 无线充电、快充协议、电源管理',
                '马达与触觉反馈模块': f'{module_stats.get("马达与触觉反馈模块", {}).get("total", 0)}条 - 线性马达、触觉反馈、振动测试',
                '外壳涂层与外观模块': f'{module_stats.get("外壳涂层与外观模块", {}).get("total", 0)}条 - 表面处理、CMF设计、外观测试'
            }
        }
        
        with open('第三批硬件模块数据统计报告.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 统计报告已生成: 第三批硬件模块数据统计报告.json")
        
        return total_count, total_label_stats, module_stats
    
    else:
        print("❌ 没有可用的第三批硬件模块数据")
        return 0, {}, {}

def main():
    print("🔧 第三批硬件模块词典数据处理...")
    
    total, label_stats, module_stats = process_third_batch_hardware_modules()
    
    if total > 0:
        print(f"\n📈 处理完成!")
        print(f"总计处理: {total}条第三批硬件模块数据")
        print(f"涵盖模块: 传感器、充电电源、马达触觉、外壳涂层")
        
        print(f"\n🎯 重点扩展领域:")
        print(f"• 传感器技术: 加速度计、陀螺仪、传感器融合、精度校准")
        print(f"• 充电技术: 无线充电、快充协议、电源管理、安全保护")
        print(f"• 触觉技术: 线性马达、触觉反馈、振动测试、用户体验")
        print(f"• 外观技术: 表面处理、CMF设计、涂层工艺、外观测试")
        
        print(f"\n💡 下一步:")
        print(f"1. 合并所有硬件模块数据(12个模块)")
        print(f"2. 执行完整硬件模块Cypher脚本导入")
        print(f"3. 验证硬件模块数据导入结果")
        print(f"4. 继续扩展其他专业模块")
    
    else:
        print("❌ 第三批硬件模块数据处理失败")

if __name__ == "__main__":
    main()
