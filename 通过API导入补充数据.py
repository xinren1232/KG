#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通过API导入补充词典数据
由于Neo4j直连有认证问题，改用API方式导入
"""

import pandas as pd
import requests
import json
from datetime import datetime

class APIDataImporter:
    def __init__(self, api_base_url="http://localhost:8000"):
        self.api_base_url = api_base_url
        
    def load_csv_data(self, csv_file):
        """加载CSV数据"""
        try:
            df = pd.read_csv(csv_file, encoding='utf-8')
            print(f"✅ 成功加载 {csv_file}: {len(df)} 条记录")
            return df
        except Exception as e:
            print(f"❌ 加载 {csv_file} 失败: {e}")
            return None
    
    def check_existing_term(self, term, category):
        """检查术语是否已存在"""
        try:
            response = requests.get(f"{self.api_base_url}/api/dictionary/{category}")
            if response.status_code == 200:
                data = response.json()
                existing_terms = [item['name'] for item in data['data']]
                return term in existing_terms
            return False
        except:
            return False
    
    def add_term_via_api(self, term_data):
        """通过API添加术语（模拟，实际需要API支持POST）"""
        # 注意：这里是模拟添加，实际需要API支持POST方法
        # 由于当前API只支持GET，我们先统计需要添加的数据
        return True
    
    def process_batch_data(self, df, batch_name):
        """处理批次数据"""
        if df is None:
            return {'success': 0, 'error': 0, 'skipped': 0, 'total': 0}
        
        success_count = 0
        error_count = 0
        skipped_count = 0
        new_terms = []
        
        print(f"\n📋 处理 {batch_name} 数据...")
        
        for index, row in df.iterrows():
            try:
                term = row['term']
                category = row['category']
                
                # 检查是否已存在
                if self.check_existing_term(term, category):
                    print(f"⏭️  跳过已存在的术语: {term}")
                    skipped_count += 1
                    continue
                
                # 处理别名
                aliases = []
                if pd.notna(row.get('aliases', '')):
                    aliases = [alias.strip() for alias in str(row['aliases']).split(';') if alias.strip()]
                
                # 处理标签
                tags = []
                if pd.notna(row.get('tags', '')):
                    tags = [tag.strip() for tag in str(row['tags']).split(';') if tag.strip()]
                
                # 构建术语数据
                term_data = {
                    'name': term,
                    'category': category,
                    'sub_category': str(row.get('sub_category', '')).strip() if pd.notna(row.get('sub_category')) else '',
                    'aliases': aliases,
                    'tags': tags,
                    'definition': str(row.get('definition', '')).strip() if pd.notna(row.get('definition')) else '',
                    'example': str(row.get('example', '')).strip() if pd.notna(row.get('example')) else '',
                    'source': str(row.get('source', '标准化词典')).strip(),
                    'status': str(row.get('status', 'active')).strip(),
                    'updated_at': str(row.get('updated_at', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))).strip()
                }
                
                new_terms.append(term_data)
                print(f"✅ 准备添加: {term} ({category})")
                success_count += 1
                
            except Exception as e:
                print(f"❌ 处理 {row.get('term', 'Unknown')} 时出错: {e}")
                error_count += 1
        
        return {
            'success': success_count,
            'error': error_count,
            'skipped': skipped_count,
            'total': len(df),
            'new_terms': new_terms
        }
    
    def generate_cypher_script(self, all_new_terms):
        """生成Cypher导入脚本"""
        cypher_statements = []
        
        for term_data in all_new_terms:
            category = term_data['category']
            
            # 构建属性字符串
            properties = []
            for key, value in term_data.items():
                if key == 'category':
                    continue
                if isinstance(value, list):
                    if value:  # 非空列表
                        value_str = str(value).replace("'", '"')
                        properties.append(f"{key}: {value_str}")
                elif value:  # 非空字符串
                    escaped_value = str(value).replace("'", "\\'").replace('"', '\\"')
                    properties.append(f"{key}: '{escaped_value}'")
            
            properties_str = ', '.join(properties)
            
            cypher = f"CREATE (:{category} {{{properties_str}}});"
            cypher_statements.append(cypher)
        
        return cypher_statements

def main():
    print("🚀 开始通过API导入补充词典数据...")
    
    importer = APIDataImporter()
    all_new_terms = []
    
    # 处理批次1数据
    df1 = importer.load_csv_data('补充词典数据_批次1.csv')
    result1 = importer.process_batch_data(df1, "批次1")
    if result1['new_terms']:
        all_new_terms.extend(result1['new_terms'])
    
    # 处理批次2数据
    df2 = importer.load_csv_data('补充词典数据_批次2.csv')
    result2 = importer.process_batch_data(df2, "批次2")
    if result2['new_terms']:
        all_new_terms.extend(result2['new_terms'])
    
    # 统计结果
    total_new = len(all_new_terms)
    print(f"\n📊 数据处理结果:")
    print(f"批次1: 成功{result1['success']}条, 跳过{result1['skipped']}条, 错误{result1['error']}条")
    print(f"批次2: 成功{result2['success']}条, 跳过{result2['skipped']}条, 错误{result2['error']}条")
    print(f"总计新增: {total_new}条")
    
    # 按Label分类统计
    label_stats = {}
    for term in all_new_terms:
        label = term['category']
        label_stats[label] = label_stats.get(label, 0) + 1
    
    print(f"\n📋 新增数据按Label分布:")
    for label, count in sorted(label_stats.items(), key=lambda x: x[1], reverse=True):
        print(f"  {label}: {count}条")
    
    # 生成Cypher导入脚本
    if total_new > 0:
        cypher_statements = importer.generate_cypher_script(all_new_terms)
        
        # 保存Cypher脚本
        with open('补充数据导入脚本.cypher', 'w', encoding='utf-8') as f:
            f.write("// 补充词典数据导入脚本\n")
            f.write(f"// 生成时间: {datetime.now().isoformat()}\n")
            f.write(f"// 总计: {total_new}条新数据\n\n")
            
            for statement in cypher_statements:
                f.write(statement + "\n")
        
        print(f"\n✅ Cypher导入脚本已生成: 补充数据导入脚本.cypher")
        print(f"包含 {len(cypher_statements)} 条CREATE语句")
        
        # 保存JSON格式的数据
        with open('补充数据.json', 'w', encoding='utf-8') as f:
            json.dump({
                'import_time': datetime.now().isoformat(),
                'total_count': total_new,
                'label_distribution': label_stats,
                'data': all_new_terms
            }, f, ensure_ascii=False, indent=2)
        
        print(f"✅ JSON数据文件已生成: 补充数据.json")
        
        # 生成导入报告
        report = {
            'import_time': datetime.now().isoformat(),
            'batch1_result': result1,
            'batch2_result': result2,
            'total_new_terms': total_new,
            'label_distribution': label_stats,
            'files_generated': [
                '补充数据导入脚本.cypher',
                '补充数据.json'
            ]
        }
        
        with open('补充数据处理报告.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 处理报告已生成: 补充数据处理报告.json")
        
        print(f"\n💡 下一步操作建议:")
        print(f"1. 等待Neo4j认证问题解决后，执行Cypher脚本导入数据")
        print(f"2. 或者开发API的POST接口来支持数据添加")
        print(f"3. 重点补充Material({label_stats.get('Material', 0)}条)和Role({label_stats.get('Role', 0)}条)类别")
    
    else:
        print(f"\n⚠️  没有新数据需要导入")

if __name__ == "__main__":
    main()
