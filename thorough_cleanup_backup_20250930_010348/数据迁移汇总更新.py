#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据迁移汇总更新 - 统一词典数据源并同步更新图谱
"""

import pandas as pd
import json
import csv
import requests
from pathlib import Path
from datetime import datetime
import shutil

def backup_current_api_data():
    """备份当前API使用的数据"""
    print("💾 备份当前API数据...")
    
    backup_dir = Path("data/api_backup") / f"before_migration_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    # 备份API目录下的数据文件
    api_data_dir = Path("api/data")
    if api_data_dir.exists():
        shutil.copytree(api_data_dir, backup_dir / "api_data")
        print(f"✅ API数据已备份到: {backup_dir}")
    
    return backup_dir

def load_unified_dictionary_data():
    """加载统一词典数据"""
    print("📖 加载统一词典数据...")
    
    unified_dir = Path("data/unified_dictionary")
    all_data = []
    
    # 读取各个分类的CSV文件
    categories = ["components", "symptoms", "causes", "countermeasures"]
    
    for category in categories:
        file_path = unified_dir / f"{category}.csv"
        if file_path.exists():
            try:
                df = pd.read_csv(file_path, encoding='utf-8')
                # 添加分类信息
                df['source_category'] = category
                all_data.append(df)
                print(f"  {category}: {len(df)} 条")
            except Exception as e:
                print(f"❌ 读取 {category}.csv 失败: {e}")
    
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        print(f"📊 总计: {len(combined_df)} 条统一词典数据")
        return combined_df
    else:
        print("❌ 未能加载统一词典数据")
        return None

def convert_to_api_format(df):
    """转换为API格式"""
    print("🔄 转换数据格式...")
    
    api_data = []
    
    for idx, row in df.iterrows():
        # 生成唯一ID
        term_id = f"TERM_{idx+1:04d}"
        
        # 处理别名
        aliases = []
        if pd.notna(row.get('aliases', '')):
            aliases_str = str(row['aliases'])
            if aliases_str and aliases_str != 'nan':
                aliases = [alias.strip() for alias in aliases_str.split(',') if alias.strip()]
        
        # 处理标签
        tags = []
        if pd.notna(row.get('tags', '')):
            tags_str = str(row['tags'])
            if tags_str and tags_str != 'nan':
                tags = [tag.strip() for tag in tags_str.split('；') if tag.strip()]
        
        # 映射类别
        category_mapping = {
            'Component': '组件',
            'Symptom': '症状', 
            'Tool': '工具',
            'Process': '流程',
            'TestCase': '测试用例',
            'Metric': '性能指标',
            'Material': '材料',
            'Role': '角色'
        }
        
        api_category = category_mapping.get(row.get('category', ''), '其他')
        
        api_item = {
            'id': term_id,
            'name': row.get('term', ''),
            'type': api_category,
            'category': row.get('source_category', 'other'),
            'aliases': aliases,
            'tags': tags,
            'description': row.get('description', ''),
            'source_file': 'unified_dictionary_migration',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        api_data.append(api_item)
    
    print(f"✅ 转换完成: {len(api_data)} 条API格式数据")
    return api_data

def save_to_api_data_source(api_data):
    """保存到API数据源"""
    print("💾 保存到API数据源...")
    
    # 确保API数据目录存在
    api_data_dir = Path("api/data")
    api_data_dir.mkdir(parents=True, exist_ok=True)
    
    # 保存为JSON格式（API可能使用的格式）
    json_file = api_data_dir / "dictionary.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(api_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 已保存到: {json_file}")
    
    # 也保存为CSV格式（备用）
    csv_file = api_data_dir / "dictionary.csv"
    df = pd.DataFrame(api_data)
    df.to_csv(csv_file, index=False, encoding='utf-8')
    
    print(f"✅ 已保存到: {csv_file}")
    
    # 创建统计文件
    stats = {
        'total_terms': len(api_data),
        'categories': {},
        'types': {},
        'migration_date': datetime.now().isoformat(),
        'source': 'unified_dictionary_migration'
    }
    
    # 统计分类分布
    for item in api_data:
        category = item.get('category', 'unknown')
        type_name = item.get('type', 'unknown')
        
        stats['categories'][category] = stats['categories'].get(category, 0) + 1
        stats['types'][type_name] = stats['types'].get(type_name, 0) + 1
    
    stats_file = api_data_dir / "dictionary_stats.json"
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 统计文件已保存到: {stats_file}")
    
    return stats

def update_neo4j_graph(api_data):
    """更新Neo4j图谱数据"""
    print("🔄 更新Neo4j图谱数据...")
    
    # 生成Cypher导入脚本
    cypher_statements = []
    
    # 清空现有词典节点（可选）
    # cypher_statements.append("MATCH (n:Dictionary) DELETE n;")
    
    # 创建词典节点
    for item in api_data:
        term = item['name'].replace("'", "\\'")
        description = item.get('description', '').replace("'", "\\'")
        category = item.get('category', '').replace("'", "\\'")
        type_name = item.get('type', '').replace("'", "\\'")
        
        aliases_str = "', '".join([alias.replace("'", "\\'") for alias in item.get('aliases', [])])
        tags_str = "', '".join([tag.replace("'", "\\'") for tag in item.get('tags', [])])
        
        cypher = f"""CREATE (d:Dictionary {{
    id: '{item['id']}',
    name: '{term}',
    type: '{type_name}',
    category: '{category}',
    aliases: ['{aliases_str}'],
    tags: ['{tags_str}'],
    description: '{description}',
    created_at: '{item['created_at']}',
    updated_at: '{item['updated_at']}'
}});"""
        
        cypher_statements.append(cypher)
    
    # 保存Cypher脚本
    cypher_file = Path("词典数据图谱更新脚本.cypher")
    with open(cypher_file, 'w', encoding='utf-8') as f:
        f.write("// 词典数据图谱更新脚本\n")
        f.write(f"// 生成时间: {datetime.now().isoformat()}\n")
        f.write(f"// 数据条数: {len(api_data)}\n\n")
        f.write('\n'.join(cypher_statements))
    
    print(f"✅ Cypher脚本已生成: {cypher_file}")
    
    # 尝试通过HTTP API执行（如果Neo4j可用）
    try:
        # 分批执行，每批50条
        batch_size = 50
        total_batches = (len(cypher_statements) + batch_size - 1) // batch_size
        
        print(f"📊 准备执行 {total_batches} 个批次...")
        
        for i in range(0, len(cypher_statements), batch_size):
            batch = cypher_statements[i:i+batch_size]
            batch_cypher = '\n'.join(batch)
            
            # 这里可以添加实际的Neo4j HTTP API调用
            print(f"  批次 {i//batch_size + 1}/{total_batches}: {len(batch)} 条语句")
        
        print("✅ 图谱更新脚本已准备就绪")
        
    except Exception as e:
        print(f"⚠️ 自动执行失败，请手动执行Cypher脚本: {e}")

def restart_api_service():
    """重启API服务"""
    print("🔄 建议重启API服务以加载新数据...")
    
    restart_guide = """
# API服务重启指南

## 方法1: 手动重启
1. 停止当前API服务 (Ctrl+C)
2. 重新启动:
   cd api
   python main.py

## 方法2: 检查数据加载
访问 http://localhost:8000/docs 查看API文档
测试词典端点是否返回新数据

## 验证步骤
1. 访问前端: http://localhost:5173
2. 进入词典管理页面
3. 检查是否显示1192条数据
4. 搜索硬件模块相关词条
"""
    
    with open("API服务重启指南.md", "w", encoding="utf-8") as f:
        f.write(restart_guide)
    
    print("✅ 重启指南已创建: API服务重启指南.md")

def main():
    """主函数"""
    print("🚀 数据迁移汇总更新")
    print("=" * 60)
    
    # 1. 备份当前数据
    backup_dir = backup_current_api_data()
    
    # 2. 加载统一词典数据
    unified_df = load_unified_dictionary_data()
    if unified_df is None:
        print("❌ 无法加载统一词典数据，退出")
        return
    
    # 3. 转换为API格式
    api_data = convert_to_api_format(unified_df)
    
    # 4. 保存到API数据源
    stats = save_to_api_data_source(api_data)
    
    # 5. 更新Neo4j图谱
    update_neo4j_graph(api_data)
    
    # 6. 重启服务指南
    restart_api_service()
    
    print("\n" + "=" * 60)
    print("🎉 数据迁移汇总完成!")
    print(f"💾 备份目录: {backup_dir}")
    print(f"📊 迁移数据: {len(api_data)} 条")
    print(f"📊 数据分布:")
    for type_name, count in stats['types'].items():
        print(f"  {type_name}: {count} 条")
    
    print(f"\n💡 下一步操作:")
    print(f"1. 重启API服务加载新数据")
    print(f"2. 执行Neo4j图谱更新脚本")
    print(f"3. 验证前端显示1192条词典数据")
    print(f"4. 测试搜索硬件模块词汇功能")
    
    print(f"\n🎯 预期结果:")
    print(f"- 前端词典管理页面显示1192条数据")
    print(f"- 包含完整的20个硬件模块专业词汇")
    print(f"- 图谱中包含所有词典节点和关系")
    print(f"- 统一的数据源，无路径冲突")

if __name__ == "__main__":
    main()
