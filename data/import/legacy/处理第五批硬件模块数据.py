#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
处理第五批硬件模块词典数据
"""

import pandas as pd
import json
from datetime import datetime

def process_fifth_batch_hardware_modules():
    """处理第五批硬件模块数据"""
    
    # 第五批硬件模块文件列表
    module_files = [
        ('硬件模块词典数据_材料科学基础.csv', '材料科学基础模块'),
        ('硬件模块词典数据_先进制造工艺.csv', '先进制造工艺模块'),
        ('硬件模块词典数据_失效分析可靠性.csv', '失效分析与可靠性工程模块'),
        ('硬件模块词典数据_标准法规.csv', '标准与法规模块')
    ]
    
    all_data = []
    module_stats = {}
    
    print("🚀 开始处理第五批硬件模块词典数据...")
    
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
        print(f"\n📊 第五批硬件模块总计: {total_count} 条新数据")
        
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
        with open('第五批硬件模块数据导入脚本.cypher', 'w', encoding='utf-8') as f:
            f.write("// 第五批硬件模块词典数据导入脚本\n")
            f.write(f"// 生成时间: {datetime.now().isoformat()}\n")
            f.write(f"// 总计: {len(cypher_statements)}条第五批硬件模块数据\n")
            f.write("// 包含: 材料科学基础、先进制造工艺、失效分析可靠性、标准法规四大模块\n\n")
            
            for statement in cypher_statements:
                f.write(statement + "\n")
        
        print(f"\n✅ Cypher脚本已生成: 第五批硬件模块数据导入脚本.cypher")
        print(f"包含 {len(cypher_statements)} 条CREATE语句")
        
        # 生成统计报告
        report = {
            'generation_time': datetime.now().isoformat(),
            'total_records': total_count,
            'modules': module_stats,
            'total_label_distribution': total_label_stats,
            'files_generated': ['第五批硬件模块数据导入脚本.cypher'],
            'module_coverage': {
                '材料科学基础模块': f'{module_stats.get("材料科学基础模块", {}).get("total", 0)}条 - 材料力学、热学、电学性能指标',
                '先进制造工艺模块': f'{module_stats.get("先进制造工艺模块", {}).get("total", 0)}条 - 微弧氧化、ALD、MEMS、3D打印',
                '失效分析与可靠性工程模块': f'{module_stats.get("失效分析与可靠性工程模块", {}).get("total", 0)}条 - 失效分析、可靠性测试、统计模型',
                '标准与法规模块': f'{module_stats.get("标准与法规模块", {}).get("total", 0)}条 - 3C、CE、FCC、RoHS、EMC测试'
            }
        }
        
        with open('第五批硬件模块数据统计报告.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 统计报告已生成: 第五批硬件模块数据统计报告.json")
        
        return total_count, total_label_stats, module_stats
    
    else:
        print("❌ 没有可用的第五批硬件模块数据")
        return 0, {}, {}

def main():
    print("🔧 第五批硬件模块词典数据处理...")
    
    total, label_stats, module_stats = process_fifth_batch_hardware_modules()
    
    if total > 0:
        print(f"\n📈 处理完成!")
        print(f"总计处理: {total}条第五批硬件模块数据")
        print(f"涵盖模块: 材料科学基础、先进制造工艺、失效分析可靠性、标准法规")
        
        print(f"\n🎯 重点扩展领域:")
        print(f"• 材料科学: 力学性能、热学性能、电学性能、化学性能")
        print(f"• 先进制造: 微弧氧化、ALD、MEMS、3D打印、激光加工")
        print(f"• 可靠性工程: 失效分析、FMEA、HALT、威布尔分布")
        print(f"• 标准法规: 3C、CE、FCC、RoHS、EMC测试、安全认证")
        
        print(f"\n💡 下一步:")
        print(f"1. 合并所有20个硬件模块数据")
        print(f"2. 执行完整硬件模块Cypher脚本导入")
        print(f"3. 验证硬件模块数据导入结果")
        print(f"4. 继续扩展其他专业模块")
    
    else:
        print("❌ 第五批硬件模块数据处理失败")

if __name__ == "__main__":
    main()
