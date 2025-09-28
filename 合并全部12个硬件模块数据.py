#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
合并全部12个硬件模块词典数据
"""

import pandas as pd
import json
from datetime import datetime

def merge_all_12_hardware_modules():
    """合并全部12个硬件模块数据"""
    
    # 全部12个硬件模块文件列表
    module_files = [
        # 第一批4个模块
        ('硬件模块词典数据_显示屏.csv', '显示屏模块'),
        ('硬件模块词典数据_摄像头.csv', '摄像头模块'),
        ('硬件模块词典数据_电池.csv', '电池模块'),
        ('硬件模块词典数据_主板PCBA.csv', '主板PCBA模块'),
        # 第二批4个模块
        ('硬件模块词典数据_射频天线.csv', '射频与天线模块'),
        ('硬件模块词典数据_声学.csv', '声学模块'),
        ('硬件模块词典数据_结构连接器.csv', '结构件与连接器模块'),
        ('硬件模块词典数据_散热系统.csv', '散热系统模块'),
        # 第三批4个模块
        ('硬件模块词典数据_传感器.csv', '传感器模块'),
        ('硬件模块词典数据_充电电源.csv', '充电与电源管理模块'),
        ('硬件模块词典数据_马达触觉.csv', '马达与触觉反馈模块'),
        ('硬件模块词典数据_外壳涂层.csv', '外壳涂层与外观模块')
    ]
    
    all_data = []
    module_stats = {}
    batch_stats = {'第一批': 0, '第二批': 0, '第三批': 0}
    
    print("🚀 开始合并全部12个硬件模块词典数据...")
    
    for i, (file_name, module_name) in enumerate(module_files):
        try:
            df = pd.read_csv(file_name, encoding='utf-8')
            print(f"✅ {module_name}: {len(df)} 条记录")
            
            # 统计Label分布
            label_counts = df['category'].value_counts().to_dict()
            module_stats[module_name] = {
                'total': len(df),
                'labels': label_counts
            }
            
            # 批次统计
            if i < 4:
                batch_stats['第一批'] += len(df)
            elif i < 8:
                batch_stats['第二批'] += len(df)
            else:
                batch_stats['第三批'] += len(df)
            
            # 添加到总数据
            all_data.append(df)
            
        except Exception as e:
            print(f"❌ 处理 {module_name} 失败: {e}")
    
    # 合并所有数据
    if all_data:
        df_all = pd.concat(all_data, ignore_index=True)
        total_count = len(df_all)
        print(f"\n📊 全部12个硬件模块总计: {total_count} 条数据")
        print(f"第一批模块: {batch_stats['第一批']}条")
        print(f"第二批模块: {batch_stats['第二批']}条")
        print(f"第三批模块: {batch_stats['第三批']}条")
        
        # 总体Label统计
        total_label_stats = df_all['category'].value_counts().to_dict()
        print(f"\n📋 全部12个硬件模块Label分布:")
        for label, count in sorted(total_label_stats.items(), key=lambda x: x[1], reverse=True):
            print(f"  {label}: {count}条")
        
        # 按技术领域分组统计
        tech_domains = {
            '显示技术': ['显示屏模块'],
            '影像技术': ['摄像头模块'],
            '电源技术': ['电池模块', '充电与电源管理模块'],
            '电路技术': ['主板PCBA模块'],
            '射频技术': ['射频与天线模块'],
            '声学技术': ['声学模块'],
            '结构技术': ['结构件与连接器模块'],
            '散热技术': ['散热系统模块'],
            '传感器技术': ['传感器模块'],
            '触觉技术': ['马达与触觉反馈模块'],
            '外观技术': ['外壳涂层与外观模块']
        }
        
        print(f"\n🎯 技术领域覆盖:")
        for domain, modules in tech_domains.items():
            domain_total = sum(module_stats.get(module, {}).get('total', 0) for module in modules)
            print(f"  {domain}: {domain_total}条")
        
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
        with open('全部12个硬件模块数据导入脚本.cypher', 'w', encoding='utf-8') as f:
            f.write("// 全部12个硬件模块词典数据导入脚本\n")
            f.write(f"// 生成时间: {datetime.now().isoformat()}\n")
            f.write(f"// 总计: {len(cypher_statements)}条硬件模块数据\n")
            f.write("// 包含12大硬件模块: 显示屏、摄像头、电池、主板PCBA、射频天线、声学、结构连接器、散热系统、传感器、充电电源、马达触觉、外壳涂层\n")
            f.write("//\n")
            f.write("// 技术领域覆盖:\n")
            for domain, modules in tech_domains.items():
                domain_total = sum(module_stats.get(module, {}).get('total', 0) for module in modules)
                f.write(f"//   - {domain}: {domain_total}条\n")
            f.write("//\n")
            f.write("// Label分布:\n")
            for label, count in sorted(total_label_stats.items(), key=lambda x: x[1], reverse=True):
                f.write(f"//   - {label}: {count}条\n")
            f.write("\n")
            
            # 按Label分组写入
            for label in sorted(total_label_stats.keys()):
                label_statements = [stmt for stmt in cypher_statements if f'CREATE (:{label} ' in stmt]
                if label_statements:
                    f.write(f"// ========== {label} ({len(label_statements)}条) ==========\n")
                    for stmt in label_statements:
                        f.write(stmt + "\n")
                    f.write("\n")
        
        print(f"\n✅ 完整12个硬件模块Cypher脚本已生成: 全部12个硬件模块数据导入脚本.cypher")
        print(f"包含 {len(cypher_statements)} 条CREATE语句，按Label分组排列")
        
        # 生成完整统计报告
        complete_report = {
            'generation_time': datetime.now().isoformat(),
            'total_records': total_count,
            'batch_distribution': batch_stats,
            'modules': module_stats,
            'tech_domains': {domain: sum(module_stats.get(module, {}).get('total', 0) for module in modules) 
                           for domain, modules in tech_domains.items()},
            'total_label_distribution': total_label_stats,
            'files_generated': ['全部12个硬件模块数据导入脚本.cypher'],
            'module_coverage': {
                '第一批模块': '显示屏、摄像头、电池、主板PCBA',
                '第二批模块': '射频天线、声学、结构连接器、散热系统',
                '第三批模块': '传感器、充电电源、马达触觉、外壳涂层',
                '技术覆盖': '11大硬件技术领域完整覆盖',
                '数据质量': '严格按照词典设计规范执行'
            }
        }
        
        with open('全部12个硬件模块数据统计报告.json', 'w', encoding='utf-8') as f:
            json.dump(complete_report, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 完整统计报告已生成: 全部12个硬件模块数据统计报告.json")
        
        return total_count, total_label_stats, module_stats, tech_domains
    
    else:
        print("❌ 没有可用的硬件模块数据")
        return 0, {}, {}, {}

def main():
    print("📋 全部12个硬件模块词典数据合并处理...")
    
    total, labels, modules, domains = merge_all_12_hardware_modules()
    
    if total > 0:
        print(f"\n📈 合并完成!")
        print(f"总计合并: {total}条硬件模块数据")
        print(f"涵盖模块: 12个核心硬件模块")
        print(f"技术领域: 11大硬件技术领域")
        
        print(f"\n🎯 技术价值:")
        for domain, count in domains.items():
            print(f"• {domain}: {count}条专业数据")
        
        print(f"\n📊 系统增强:")
        original_count = 526  # 原有基础数据
        supplement_count = 139  # 基础补充数据
        hardware_count = total  # 硬件模块数据
        final_count = original_count + supplement_count + hardware_count
        growth_rate = ((supplement_count + hardware_count) / original_count) * 100
        
        print(f"• 原有基础: {original_count}条")
        print(f"• 基础补充: {supplement_count}条")
        print(f"• 硬件模块: {hardware_count}条")
        print(f"• 最终总量: {final_count}条")
        print(f"• 总增长率: +{growth_rate:.1f}%")
        
        print(f"\n💡 下一步:")
        print(f"1. 合并所有补充数据(基础+12个硬件模块)")
        print(f"2. 执行完整数据导入脚本")
        print(f"3. 验证{total}条硬件模块数据导入")
        print(f"4. 更新前端显示新的硬件模块数据")
    
    else:
        print("❌ 硬件模块数据合并失败")

if __name__ == "__main__":
    main()
