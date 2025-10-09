#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速处理补充词典数据
"""

import pandas as pd
import json
from datetime import datetime

def process_csv_files():
    """处理CSV文件并生成统计"""
    
    # 加载数据
    try:
        df1 = pd.read_csv('补充词典数据_批次1.csv', encoding='utf-8')
        print(f"✅ 批次1: {len(df1)} 条记录")
    except Exception as e:
        print(f"❌ 批次1加载失败: {e}")
        df1 = pd.DataFrame()
    
    try:
        df2 = pd.read_csv('补充词典数据_批次2.csv', encoding='utf-8')
        print(f"✅ 批次2: {len(df2)} 条记录")
    except Exception as e:
        print(f"❌ 批次2加载失败: {e}")
        df2 = pd.DataFrame()
    
    # 合并数据
    if not df1.empty and not df2.empty:
        df_all = pd.concat([df1, df2], ignore_index=True)
    elif not df1.empty:
        df_all = df1
    elif not df2.empty:
        df_all = df2
    else:
        print("❌ 没有可用数据")
        return
    
    print(f"📊 总计: {len(df_all)} 条新数据")
    
    # 按Label统计
    label_stats = df_all['category'].value_counts().to_dict()
    print("\n📋 按Label分布:")
    for label, count in sorted(label_stats.items(), key=lambda x: x[1], reverse=True):
        print(f"  {label}: {count}条")
    
    # 重点关注Material和Role
    material_count = label_stats.get('Material', 0)
    role_count = label_stats.get('Role', 0)
    print(f"\n🎯 重点补充:")
    print(f"  Material: {material_count}条")
    print(f"  Role: {role_count}条")
    
    # 生成Cypher脚本
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
        properties.append(f"name: '{term.replace(chr(39), chr(39)+chr(39))}'")  # 转义单引号
        
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
        
        properties.append(f"source: '标准化词典'")
        properties.append(f"status: 'active'")
        properties.append(f"updated_at: '{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}'")
        
        properties_str = ', '.join(properties)
        cypher = f"CREATE (:{category} {{{properties_str}}});"
        cypher_statements.append(cypher)
    
    # 保存Cypher脚本
    with open('补充数据导入脚本.cypher', 'w', encoding='utf-8') as f:
        f.write("// 补充词典数据导入脚本\n")
        f.write(f"// 生成时间: {datetime.now().isoformat()}\n")
        f.write(f"// 总计: {len(cypher_statements)}条新数据\n\n")
        
        for statement in cypher_statements:
            f.write(statement + "\n")
    
    print(f"\n✅ Cypher脚本已生成: 补充数据导入脚本.cypher")
    print(f"包含 {len(cypher_statements)} 条CREATE语句")
    
    # 生成统计报告
    report = {
        'generation_time': datetime.now().isoformat(),
        'total_records': len(df_all),
        'label_distribution': label_stats,
        'files_generated': ['补充数据导入脚本.cypher'],
        'key_additions': {
            'Material': material_count,
            'Role': role_count
        }
    }
    
    with open('补充数据统计报告.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 统计报告已生成: 补充数据统计报告.json")
    
    return len(df_all), label_stats

def main():
    print("🚀 快速处理补充词典数据...")
    
    total, stats = process_csv_files()
    
    print(f"\n📈 处理完成!")
    print(f"总计处理: {total}条新数据")
    print(f"Material类别: {stats.get('Material', 0)}条")
    print(f"Role类别: {stats.get('Role', 0)}条")
    
    print(f"\n💡 下一步:")
    print(f"1. 等待Neo4j认证问题解决")
    print(f"2. 执行生成的Cypher脚本导入数据")
    print(f"3. 验证数据导入结果")

if __name__ == "__main__":
    main()
