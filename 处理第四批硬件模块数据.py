#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
处理第四批硬件模块词典数据
"""

import pandas as pd
import json
from datetime import datetime

def process_fourth_batch_hardware_modules():
    """处理第四批硬件模块数据"""
    
    # 第四批硬件模块文件列表
    module_files = [
        ('硬件模块词典数据_连接网络.csv', '连接与网络模块'),
        ('硬件模块词典数据_接口连接器.csv', '接口与连接器模块'),
        ('硬件模块词典数据_被动元件.csv', '被动元件与电路保护模块'),
        ('硬件模块词典数据_生产测试治具.csv', '生产与测试治具模块')
    ]
    
    all_data = []
    module_stats = {}
    
    print("🚀 开始处理第四批硬件模块词典数据...")
    
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
        print(f"\n📊 第四批硬件模块总计: {total_count} 条新数据")
        
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
        with open('第四批硬件模块数据导入脚本.cypher', 'w', encoding='utf-8') as f:
            f.write("// 第四批硬件模块词典数据导入脚本\n")
            f.write(f"// 生成时间: {datetime.now().isoformat()}\n")
            f.write(f"// 总计: {len(cypher_statements)}条第四批硬件模块数据\n")
            f.write("// 包含: 连接网络、接口连接器、被动元件、生产测试治具四大模块\n\n")
            
            for statement in cypher_statements:
                f.write(statement + "\n")
        
        print(f"\n✅ Cypher脚本已生成: 第四批硬件模块数据导入脚本.cypher")
        print(f"包含 {len(cypher_statements)} 条CREATE语句")
        
        # 生成统计报告
        report = {
            'generation_time': datetime.now().isoformat(),
            'total_records': total_count,
            'modules': module_stats,
            'total_label_distribution': total_label_stats,
            'files_generated': ['第四批硬件模块数据导入脚本.cypher'],
            'module_coverage': {
                '连接与网络模块': f'{module_stats.get("连接与网络模块", {}).get("total", 0)}条 - Wi-Fi、蓝牙、5G、GNSS、NFC',
                '接口与连接器模块': f'{module_stats.get("接口与连接器模块", {}).get("total", 0)}条 - USB-C、Lightning、FPC、BTB连接器',
                '被动元件与电路保护模块': f'{module_stats.get("被动元件与电路保护模块", {}).get("total", 0)}条 - 电容、电感、保护器件、ESD',
                '生产与测试治具模块': f'{module_stats.get("生产与测试治具模块", {}).get("total", 0)}条 - ICT、FCT、自动化测试、治具设计'
            }
        }
        
        with open('第四批硬件模块数据统计报告.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 统计报告已生成: 第四批硬件模块数据统计报告.json")
        
        return total_count, total_label_stats, module_stats
    
    else:
        print("❌ 没有可用的第四批硬件模块数据")
        return 0, {}, {}

def main():
    print("🔧 第四批硬件模块词典数据处理...")
    
    total, label_stats, module_stats = process_fourth_batch_hardware_modules()
    
    if total > 0:
        print(f"\n📈 处理完成!")
        print(f"总计处理: {total}条第四批硬件模块数据")
        print(f"涵盖模块: 连接网络、接口连接器、被动元件、生产测试治具")
        
        print(f"\n🎯 重点扩展领域:")
        print(f"• 连接技术: Wi-Fi 6E、蓝牙5.3、5G调制解调器、GNSS、NFC")
        print(f"• 接口技术: USB-C、Lightning、FPC、BTB、信号完整性")
        print(f"• 被动元件: MLCC、电感、保护器件、ESD防护")
        print(f"• 生产测试: ICT、FCT、自动化测试、治具设计")
        
        print(f"\n💡 下一步:")
        print(f"1. 合并所有16个硬件模块数据")
        print(f"2. 执行完整硬件模块Cypher脚本导入")
        print(f"3. 验证硬件模块数据导入结果")
        print(f"4. 继续扩展其他专业模块")
    
    else:
        print("❌ 第四批硬件模块数据处理失败")

if __name__ == "__main__":
    main()
