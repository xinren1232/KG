#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import csv
from pathlib import Path
from neo4j import GraphDatabase

def check_neo4j_dictionary_data():
    """检查Neo4j中的词典数据"""
    print("🔍 检查Neo4j中的词典数据")
    print("=" * 50)
    
    try:
        driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'password123'))
        
        with driver.session() as session:
            # 检查Dictionary节点
            dict_result = session.run('MATCH (n:Dictionary) RETURN count(n) AS count').single()
            dict_count = dict_result['count'] if dict_result else 0
            print(f"Dictionary节点数量: {dict_count}")
            
            # 检查所有标签
            labels_result = session.run('CALL db.labels() YIELD label RETURN label ORDER BY label')
            labels = [record['label'] for record in labels_result]
            print(f"所有标签: {labels}")
            
            # 检查各标签的节点数量
            for label in labels:
                count_result = session.run(f'MATCH (n:{label}) RETURN count(n) AS count').single()
                count = count_result['count'] if count_result else 0
                print(f"  {label}: {count} 个节点")
            
            # 如果Dictionary节点为0，检查是否有其他词典相关节点
            if dict_count == 0:
                print("\n🔍 检查其他可能的词典节点...")
                for label in ['Component', 'Symptom', 'Cause', 'Countermeasure']:
                    if label in labels:
                        sample_result = session.run(f'MATCH (n:{label}) RETURN n LIMIT 3')
                        samples = [dict(record['n']) for record in sample_result]
                        if samples:
                            print(f"  {label}样本: {samples[0]}")
        
        driver.close()
        return dict_count > 0
        
    except Exception as e:
        print(f"❌ Neo4j连接失败: {e}")
        return False

def check_file_data_sources():
    """检查文件数据源"""
    print("\n📁 检查文件数据源")
    print("=" * 50)
    
    data_sources = [
        ("api/data/dictionary.json", "API词典文件"),
        ("data/unified_dictionary/components.csv", "统一词典-组件"),
        ("data/unified_dictionary/symptoms.csv", "统一词典-症状"),
        ("data/unified_dictionary/causes.csv", "统一词典-原因"),
        ("data/unified_dictionary/countermeasures.csv", "统一词典-对策"),
        ("ontology/dictionaries/components.csv", "本体词典-组件"),
        ("ontology/dictionaries/symptoms.csv", "本体词典-症状"),
        ("ontology/dictionaries/causes.csv", "本体词典-原因"),
        ("ontology/dictionaries/countermeasures.csv", "本体词典-对策"),
    ]
    
    total_records = 0
    
    for file_path, description in data_sources:
        path = Path(file_path)
        if path.exists():
            try:
                if path.suffix == '.json':
                    with open(path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        count = len(data) if isinstance(data, list) else len(data.get('entries', []))
                elif path.suffix == '.csv':
                    with open(path, 'r', encoding='utf-8') as f:
                        reader = csv.reader(f)
                        count = sum(1 for row in reader) - 1  # 减去标题行
                        
                print(f"✅ {description}: {count} 条记录 ({file_path})")
                total_records += count
                
                # 显示前几条数据样本
                if path.suffix == '.csv' and count > 0:
                    with open(path, 'r', encoding='utf-8') as f:
                        reader = csv.DictReader(f)
                        sample = next(reader, None)
                        if sample:
                            print(f"   样本: {dict(list(sample.items())[:3])}")
                            
            except Exception as e:
                print(f"❌ {description}: 读取失败 - {e}")
        else:
            print(f"❌ {description}: 文件不存在 ({file_path})")
    
    print(f"\n📊 文件数据源总计: {total_records} 条记录")
    return total_records

def check_api_configuration():
    """检查API配置"""
    print("\n⚙️ 检查API配置")
    print("=" * 50)
    
    # 检查main.py中的配置
    main_py = Path("api/main.py")
    if main_py.exists():
        with open(main_py, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("API配置分析:")
        
        # 检查是否使用统一词典管理器
        if "unified_dictionary_config" in content:
            print("✅ 使用统一词典管理器")
        else:
            print("❌ 未使用统一词典管理器")
        
        # 检查备用数据
        if "FALLBACK_DATA" in content:
            print("⚠️ 使用硬编码备用数据")
        
        # 检查词典路径
        if "api/data/dictionary.json" in content:
            print("📁 使用api/data/dictionary.json")
        
        if "data/unified_dictionary" in content:
            print("📁 使用data/unified_dictionary")
            
        if "ontology/dictionaries" in content:
            print("📁 使用ontology/dictionaries")

def suggest_fixes():
    """建议修复方案"""
    print("\n🔧 修复建议")
    print("=" * 50)
    
    print("1. 数据导入问题:")
    print("   - Neo4j中Dictionary节点为0，需要重新导入数据")
    print("   - 检查数据导入脚本是否正确执行")
    
    print("\n2. API配置问题:")
    print("   - API使用硬编码备用数据，只有5条记录")
    print("   - 需要配置API使用实际的词典文件")
    
    print("\n3. 推荐修复步骤:")
    print("   a. 使用统一词典管理器")
    print("   b. 将文件数据导入Neo4j")
    print("   c. 更新API配置使用Neo4j数据")
    print("   d. 测试数据完整性")

def main():
    """主函数"""
    print("🔍 词典数据路径和数量检查")
    print("=" * 60)
    
    # 1. 检查Neo4j数据
    neo4j_ok = check_neo4j_dictionary_data()
    
    # 2. 检查文件数据源
    file_count = check_file_data_sources()
    
    # 3. 检查API配置
    check_api_configuration()
    
    # 4. 提供修复建议
    suggest_fixes()
    
    print("\n" + "=" * 60)
    print("📊 检查总结")
    print("=" * 60)
    print(f"Neo4j Dictionary节点: {'✅ 有数据' if neo4j_ok else '❌ 无数据'}")
    print(f"文件数据源: {'✅ 有数据' if file_count > 0 else '❌ 无数据'} ({file_count} 条)")
    print(f"主要问题: {'数据导入' if not neo4j_ok else 'API配置'}")

if __name__ == "__main__":
    main()
