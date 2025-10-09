#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import csv
import requests
from pathlib import Path
from neo4j import GraphDatabase

def check_all_dictionary_files():
    """检查所有词典文件"""
    print("📁 全面检查词典数据文件")
    print("=" * 60)
    
    # 所有可能的词典文件位置
    file_sources = [
        ("api/data/dictionary.json", "API主词典文件"),
        ("data/unified_dictionary/components.csv", "统一词典-组件"),
        ("data/unified_dictionary/symptoms.csv", "统一词典-症状"),
        ("data/unified_dictionary/causes.csv", "统一词典-原因"),
        ("data/unified_dictionary/countermeasures.csv", "统一词典-对策"),
        ("ontology/dictionaries/components.csv", "本体词典-组件"),
        ("ontology/dictionaries/symptoms.csv", "本体词典-症状"),
        ("ontology/dictionaries/causes.csv", "本体词典-原因"),
        ("ontology/dictionaries/countermeasures.csv", "本体词典-对策"),
        ("ontology/dictionaries/enhanced_components.csv", "增强组件词典"),
        ("ontology/dictionaries/enhanced_symptoms.csv", "增强症状词典"),
        ("ontology/dictionaries/enhanced_tools_processes.csv", "增强工具流程词典"),
    ]
    
    total_records = 0
    file_details = {}
    
    for file_path, description in file_sources:
        # 从api目录开始，需要回到上级目录
        if file_path.startswith('api/'):
            actual_path = Path(file_path)
        else:
            actual_path = Path("..") / file_path
            
        if actual_path.exists():
            try:
                if actual_path.suffix == '.json':
                    with open(actual_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        count = len(data) if isinstance(data, list) else len(data.get('entries', []))
                        
                    # 显示JSON文件的结构
                    if isinstance(data, list) and len(data) > 0:
                        sample = data[0]
                        print(f"✅ {description}: {count} 条记录")
                        print(f"   路径: {actual_path}")
                        print(f"   样本字段: {list(sample.keys())[:5]}")
                        print(f"   样本数据: {sample.get('term', sample.get('name', 'N/A'))}")
                    else:
                        print(f"✅ {description}: {count} 条记录 (非列表格式)")
                        
                elif actual_path.suffix == '.csv':
                    with open(actual_path, 'r', encoding='utf-8') as f:
                        reader = csv.reader(f)
                        rows = list(reader)
                        count = len(rows) - 1 if len(rows) > 0 else 0  # 减去标题行
                        
                    print(f"✅ {description}: {count} 条记录")
                    print(f"   路径: {actual_path}")
                    if len(rows) > 1:
                        headers = rows[0]
                        sample_row = rows[1]
                        print(f"   字段: {headers[:5]}")
                        print(f"   样本: {sample_row[0] if sample_row else 'N/A'}")
                
                file_details[file_path] = {
                    'count': count,
                    'exists': True,
                    'path': str(actual_path),
                    'description': description
                }
                total_records += count
                
            except Exception as e:
                print(f"❌ {description}: 读取失败 - {e}")
                file_details[file_path] = {
                    'count': 0,
                    'exists': True,
                    'error': str(e),
                    'description': description
                }
        else:
            print(f"❌ {description}: 文件不存在 ({actual_path})")
            file_details[file_path] = {
                'count': 0,
                'exists': False,
                'description': description
            }
    
    print(f"\n📊 文件数据源总计: {total_records} 条记录")
    return file_details, total_records

def check_neo4j_dictionary_data():
    """检查Neo4j中的词典数据"""
    print("\n🔍 检查Neo4j词典数据")
    print("=" * 60)
    
    try:
        driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'password123'))
        
        with driver.session() as session:
            # 检查所有标签
            labels_result = session.run('CALL db.labels() YIELD label RETURN label ORDER BY label')
            labels = [record['label'] for record in labels_result]
            
            print(f"所有标签: {labels}")
            
            # 检查词典相关标签的详细信息
            dictionary_labels = ['Dictionary', 'Component', 'Symptom', 'Tool', 'Process', 'TestCase', 'Metric', 'Material', 'Role']
            neo4j_data = {}
            
            for label in dictionary_labels:
                if label in labels:
                    # 获取数量
                    count_result = session.run(f'MATCH (n:{label}) RETURN count(n) AS count').single()
                    count = count_result['count'] if count_result else 0
                    
                    # 获取样本数据
                    sample_result = session.run(f'MATCH (n:{label}) RETURN n LIMIT 3')
                    samples = [dict(record['n']) for record in sample_result]
                    
                    print(f"✅ {label}: {count} 个节点")
                    if samples:
                        sample = samples[0]
                        print(f"   样本字段: {list(sample.keys())[:5]}")
                        print(f"   样本名称: {sample.get('name', sample.get('term', 'N/A'))}")
                    
                    neo4j_data[label] = {
                        'count': count,
                        'samples': samples
                    }
                else:
                    print(f"❌ {label}: 标签不存在")
                    neo4j_data[label] = {'count': 0, 'samples': []}
            
            # 计算词典节点总数
            total_dict_nodes = sum(data['count'] for label, data in neo4j_data.items() 
                                 if label in ['Component', 'Symptom', 'Tool', 'Process'])
            
            print(f"\n📊 Neo4j词典节点总计: {total_dict_nodes} 个")
            
        driver.close()
        return neo4j_data, total_dict_nodes
        
    except Exception as e:
        print(f"❌ Neo4j连接失败: {e}")
        return {}, 0

def check_api_endpoints():
    """检查所有API端点"""
    print("\n🌐 检查API端点")
    print("=" * 60)
    
    base_url = "http://localhost:8000"
    
    # 所有词典相关的API端点
    endpoints = [
        ("/kg/dictionary", "词典数据 (旧)"),
        ("/api/dictionary", "词典数据 (新)"),
        ("/kg/dictionary/entries", "词典条目"),
        ("/kg/dictionary/categories", "词典类别"),
        ("/kg/dictionary/statistics", "词典统计"),
        ("/api/dictionary/labels", "词典标签"),
        ("/api/dictionary/tags", "词典标签统计"),
    ]
    
    api_results = {}
    
    for endpoint, description in endpoints:
        print(f"\n🔍 测试 {description} ({endpoint})")
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # 分析不同端点的数据
                if endpoint in ["/kg/dictionary", "/api/dictionary"]:
                    if 'data' in data:
                        if isinstance(data['data'], list):
                            count = len(data['data'])
                        elif isinstance(data['data'], dict):
                            # 可能是分类的数据
                            count = sum(len(v) if isinstance(v, list) else 0 for v in data['data'].values())
                        else:
                            count = data.get('total', 0)
                    else:
                        count = data.get('total', 0)
                    
                    print(f"✅ {description}: {count} 条数据")
                    print(f"   消息: {data.get('message', 'N/A')}")
                    
                    # 显示数据结构
                    if 'data' in data and data['data']:
                        if isinstance(data['data'], list) and len(data['data']) > 0:
                            sample = data['data'][0]
                            print(f"   样本字段: {list(sample.keys())[:5]}")
                        elif isinstance(data['data'], dict):
                            print(f"   数据类别: {list(data['data'].keys())}")
                    
                    api_results[endpoint] = {
                        'status': 'success',
                        'count': count,
                        'message': data.get('message', ''),
                        'data_type': type(data.get('data', None)).__name__
                    }
                
                elif endpoint == "/kg/dictionary/entries":
                    entries = data.get('data', {}).get('entries', [])
                    count = len(entries)
                    print(f"✅ {description}: {count} 条条目")
                    
                    if entries:
                        sample = entries[0]
                        print(f"   样本字段: {list(sample.keys())[:5]}")
                    
                    api_results[endpoint] = {
                        'status': 'success',
                        'count': count
                    }
                
                else:
                    print(f"✅ {description}: 响应正常")
                    api_results[endpoint] = {
                        'status': 'success',
                        'data': data
                    }
                    
            else:
                print(f"❌ {description}: HTTP {response.status_code}")
                api_results[endpoint] = {
                    'status': 'error',
                    'code': response.status_code
                }
                
        except Exception as e:
            print(f"❌ {description}: 连接失败 - {e}")
            api_results[endpoint] = {
                'status': 'failed',
                'error': str(e)
            }
    
    return api_results

def analyze_discrepancies(file_details, neo4j_data, api_results):
    """分析数据差异"""
    print("\n🔍 数据差异分析")
    print("=" * 60)
    
    # 主要数据源统计
    main_file_count = file_details.get('api/data/dictionary.json', {}).get('count', 0)
    neo4j_total = sum(data['count'] for data in neo4j_data.values())
    api_old_count = api_results.get('/kg/dictionary', {}).get('count', 0)
    api_new_count = api_results.get('/api/dictionary', {}).get('count', 0)
    api_entries_count = api_results.get('/kg/dictionary/entries', {}).get('count', 0)
    
    print(f"📊 数据源对比:")
    print(f"  - 主词典文件 (api/data/dictionary.json): {main_file_count} 条")
    print(f"  - Neo4j词典节点总计: {neo4j_total} 个")
    print(f"  - API旧端点 (/kg/dictionary): {api_old_count} 条")
    print(f"  - API新端点 (/api/dictionary): {api_new_count} 条")
    print(f"  - API条目端点 (/kg/dictionary/entries): {api_entries_count} 条")
    
    print(f"\n🎯 目标: 1124条词典数据")
    
    # 问题诊断
    print(f"\n🔍 问题诊断:")
    
    if main_file_count == 1124:
        print("✅ 主词典文件数据正确 (1124条)")
    elif main_file_count > 0:
        print(f"⚠️ 主词典文件数据不匹配: {main_file_count} ≠ 1124")
    else:
        print("❌ 主词典文件无数据或不存在")
    
    if api_entries_count > 0:
        print(f"✅ API条目端点有数据 ({api_entries_count}条)")
    else:
        print("❌ API条目端点无数据")
    
    if api_old_count == 0 and api_new_count == 0:
        print("❌ 两个主要API端点都无数据")
    elif api_old_count != main_file_count or api_new_count != main_file_count:
        print(f"⚠️ API端点数据与文件不匹配")
    
    # 修复建议
    print(f"\n💡 修复建议:")
    
    if main_file_count == 1124 and (api_old_count == 0 or api_new_count == 0):
        print("1. 文件数据正确但API端点返回错误")
        print("   - 检查API端点的文件路径配置")
        print("   - 检查API端点的数据处理逻辑")
        print("   - 可能存在多个同名端点冲突")
    
    if neo4j_total == 0:
        print("2. Neo4j无词典数据")
        print("   - 需要将文件数据导入Neo4j")
        print("   - 运行数据导入脚本")
    
    return {
        'main_file_count': main_file_count,
        'neo4j_total': neo4j_total,
        'api_old_count': api_old_count,
        'api_new_count': api_new_count,
        'api_entries_count': api_entries_count
    }

def main():
    """主函数"""
    print("🔍 全面检查词典数据 - 目标1124条")
    print("=" * 80)
    
    # 1. 检查所有文件
    file_details, total_file_records = check_all_dictionary_files()
    
    # 2. 检查Neo4j数据
    neo4j_data, total_neo4j_records = check_neo4j_dictionary_data()
    
    # 3. 检查API端点
    api_results = check_api_endpoints()
    
    # 4. 分析差异
    summary = analyze_discrepancies(file_details, neo4j_data, api_results)
    
    # 5. 保存详细报告
    report = {
        'timestamp': '2025-09-28',
        'target_count': 1124,
        'file_details': file_details,
        'neo4j_data': neo4j_data,
        'api_results': api_results,
        'summary': summary,
        'total_file_records': total_file_records,
        'total_neo4j_records': total_neo4j_records
    }
    
    with open('../词典数据全面检查报告.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n📄 详细报告已保存: 词典数据全面检查报告.json")
    
    # 6. 总结
    print(f"\n" + "=" * 80)
    print(f"📊 检查总结")
    print(f"=" * 80)
    print(f"目标数据量: 1124条")
    print(f"文件数据总计: {total_file_records}条")
    print(f"Neo4j数据总计: {total_neo4j_records}个节点")
    print(f"主词典文件: {summary['main_file_count']}条")
    print(f"API旧端点: {summary['api_old_count']}条")
    print(f"API新端点: {summary['api_new_count']}条")
    print(f"API条目端点: {summary['api_entries_count']}条")
    
    if summary['main_file_count'] == 1124:
        print(f"\n✅ 主词典文件数据正确！")
    else:
        print(f"\n⚠️ 主词典文件数据需要检查")

if __name__ == "__main__":
    main()
