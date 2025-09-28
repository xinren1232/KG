#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
补充词典数据导入脚本
将新的词典数据导入到Neo4j数据库中
"""

import pandas as pd
import numpy as np
from neo4j import GraphDatabase
import json
from datetime import datetime
import os

class DictionaryDataImporter:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="password"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        
    def close(self):
        self.driver.close()
    
    def load_csv_data(self, csv_file):
        """加载CSV数据"""
        try:
            df = pd.read_csv(csv_file, encoding='utf-8')
            print(f"✅ 成功加载 {csv_file}: {len(df)} 条记录")
            return df
        except Exception as e:
            print(f"❌ 加载 {csv_file} 失败: {e}")
            return None
    
    def validate_data(self, df):
        """验证数据质量"""
        issues = []
        
        # 检查必填字段
        required_fields = ['term', 'category']
        for field in required_fields:
            if field not in df.columns:
                issues.append(f"缺少必填字段: {field}")
            elif df[field].isna().any():
                null_count = df[field].isna().sum()
                issues.append(f"字段 {field} 有 {null_count} 个空值")
        
        # 检查category是否在允许的Label中
        valid_labels = ['Symptom', 'Component', 'Tool', 'Process', 'TestCase', 'Metric', 'Material', 'Role']
        if 'category' in df.columns:
            invalid_categories = df[~df['category'].isin(valid_labels)]['category'].unique()
            if len(invalid_categories) > 0:
                issues.append(f"无效的category值: {invalid_categories}")
        
        # 检查重复术语
        if 'term' in df.columns:
            duplicates = df[df['term'].duplicated()]['term'].unique()
            if len(duplicates) > 0:
                issues.append(f"重复的术语: {duplicates}")
        
        return issues
    
    def check_existing_terms(self, df):
        """检查数据库中已存在的术语"""
        with self.driver.session() as session:
            existing_terms = []
            for _, row in df.iterrows():
                term = row['term']
                category = row['category']
                
                # 检查是否已存在
                query = f"""
                MATCH (n:{category} {{name: $term}})
                RETURN n.name as name
                """
                result = session.run(query, term=term)
                if result.single():
                    existing_terms.append(term)
            
            return existing_terms
    
    def import_data(self, df, skip_existing=True):
        """导入数据到Neo4j"""
        success_count = 0
        error_count = 0
        skipped_count = 0
        
        # 检查已存在的术语
        existing_terms = self.check_existing_terms(df) if skip_existing else []
        
        with self.driver.session() as session:
            for index, row in df.iterrows():
                try:
                    term = row['term']
                    category = row['category']
                    
                    # 跳过已存在的术语
                    if skip_existing and term in existing_terms:
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
                    
                    # 构建节点属性
                    properties = {
                        'name': term,
                        'aliases': aliases,
                        'tags': tags,
                        'definition': str(row.get('definition', '')).strip() if pd.notna(row.get('definition')) else '',
                        'example': str(row.get('example', '')).strip() if pd.notna(row.get('example')) else '',
                        'source': str(row.get('source', '标准化词典')).strip(),
                        'status': str(row.get('status', 'active')).strip(),
                        'updated_at': str(row.get('updated_at', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))).strip()
                    }
                    
                    # 添加子类别
                    if pd.notna(row.get('sub_category')):
                        properties['sub_category'] = str(row['sub_category']).strip()
                    
                    # 创建节点
                    query = f"""
                    CREATE (n:{category} $properties)
                    RETURN n.name as name
                    """
                    
                    result = session.run(query, properties=properties)
                    if result.single():
                        print(f"✅ 成功导入: {term} ({category})")
                        success_count += 1
                    else:
                        print(f"❌ 导入失败: {term}")
                        error_count += 1
                        
                except Exception as e:
                    print(f"❌ 导入 {row.get('term', 'Unknown')} 时出错: {e}")
                    error_count += 1
        
        return {
            'success': success_count,
            'error': error_count,
            'skipped': skipped_count,
            'total': len(df)
        }
    
    def get_statistics(self):
        """获取导入后的统计信息"""
        with self.driver.session() as session:
            query = """
            MATCH (n)
            RETURN labels(n)[0] as label, count(n) as count
            ORDER BY count DESC
            """
            result = session.run(query)
            stats = []
            total = 0
            for record in result:
                label = record['label']
                count = record['count']
                stats.append({'label': label, 'count': count})
                total += count
            
            return {'labels': stats, 'total': total}

def main():
    print("🚀 开始补充词典数据导入...")
    
    # 初始化导入器
    importer = DictionaryDataImporter()
    
    try:
        # 导入批次1数据
        print("\n📋 导入批次1数据...")
        df1 = importer.load_csv_data('补充词典数据_批次1.csv')
        if df1 is not None:
            # 验证数据
            issues1 = importer.validate_data(df1)
            if issues1:
                print("⚠️  数据验证发现问题:")
                for issue in issues1:
                    print(f"   - {issue}")
            
            # 导入数据
            result1 = importer.import_data(df1, skip_existing=True)
            print(f"📊 批次1导入结果: 成功{result1['success']}条, 失败{result1['error']}条, 跳过{result1['skipped']}条")
        
        # 导入批次2数据
        print("\n📋 导入批次2数据...")
        df2 = importer.load_csv_data('补充词典数据_批次2.csv')
        if df2 is not None:
            # 验证数据
            issues2 = importer.validate_data(df2)
            if issues2:
                print("⚠️  数据验证发现问题:")
                for issue in issues2:
                    print(f"   - {issue}")
            
            # 导入数据
            result2 = importer.import_data(df2, skip_existing=True)
            print(f"📊 批次2导入结果: 成功{result2['success']}条, 失败{result2['error']}条, 跳过{result2['skipped']}条")
        
        # 获取最终统计
        print("\n📈 导入后数据库统计:")
        stats = importer.get_statistics()
        print(f"总节点数: {stats['total']}")
        for label_stat in stats['labels']:
            print(f"  {label_stat['label']}: {label_stat['count']}个")
        
        # 保存统计报告
        report = {
            'import_time': datetime.now().isoformat(),
            'batch1_result': result1 if df1 is not None else None,
            'batch2_result': result2 if df2 is not None else None,
            'final_statistics': stats,
            'validation_issues': {
                'batch1': issues1 if df1 is not None else [],
                'batch2': issues2 if df2 is not None else []
            }
        }
        
        with open('补充数据导入报告.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ 补充数据导入完成! 详细报告已保存到: 补充数据导入报告.json")
        
    except Exception as e:
        print(f"❌ 导入过程中发生错误: {e}")
    
    finally:
        importer.close()

if __name__ == "__main__":
    main()
