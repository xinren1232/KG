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
import argparse
from pathlib import Path
import shutil
import subprocess
import hashlib


class DictionaryDataImporter:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="password123"):
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

                    # 创建/更新节点（幂等） + 统一主键 canonical_id 回填
                    _prefix = {
                        'Component': 'CMP','Symptom': 'SYM','Tool': 'TOL','Process': 'PRC',
                        'TestCase': 'TST','Material': 'MAT','Role': 'ROL','Metric': 'MET'
                    }.get(category, 'UNK')
                    _hash = hashlib.sha1(f"{category}|{term.lower()}".encode('utf-8')).hexdigest()[:8].upper()
                    cid = f"{_prefix}_{_hash}"

                    query = f"""
                    MERGE (n:{category} {{name: $name}})
                    ON CREATE SET n += $properties,
                                   n.canonical_id = coalesce(n.canonical_id, $cid),
                                   n.created_at = coalesce(n.created_at, datetime())
                    ON MATCH SET n += $properties,
                                  n.canonical_id = coalesce(n.canonical_id, $cid),
                                  n.updated_at = datetime()
                    RETURN n.name as name
                    """

                    result = session.run(query, name=term, properties=properties, cid=cid)
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

    def merge_into_dictionary_file(self, dfs, dict_path="api/data/dictionary.json", dry_run=True, allow_new=False):
        """将CSV数据合并到字典JSON文件（默认只更新已存在术语，避免直接写库）
        - dfs: DataFrame 列表
        - dict_path: 词典JSON路径
        - dry_run: 只预览不落盘
        - allow_new: 允许新增术语（默认False，避免突破1124）
        返回：汇总结果字典
        """
        dict_path = Path(dict_path)
        if not dict_path.exists():
            raise FileNotFoundError(f"词典文件不存在: {dict_path}")

        # 加载现有词典
        with open(dict_path, 'r', encoding='utf-8') as f:
            try:
                dictionary = json.load(f)
                if isinstance(dictionary, dict) and 'entries' in dictionary:
                    dictionary = dictionary['entries']
                if not isinstance(dictionary, list):
                    raise ValueError('词典JSON格式应为数组')
            except Exception as e:
                raise RuntimeError(f"读取词典失败: {e}")

        # 建立索引 (term, category) -> idx
        index = {}
        for i, item in enumerate(dictionary):
            term = (item.get('term') or item.get('name') or '').strip()
            category = (item.get('category') or '').strip()
            if term and category:
                index[(term, category)] = i

        def normalize_list(v):
            if v is None or (isinstance(v, float) and pd.isna(v)):
                return []
            if isinstance(v, list):
                return [str(x).strip() for x in v if str(x).strip()]
            # 以分号拆分
            return [p.strip() for p in str(v).split(';') if p and str(p).strip()]

        # 合并多个数据源
        combined = []
        for df in dfs:
            if df is not None and len(df) > 0:
                combined.append(df)
        if not combined:
            return {
                'added': 0, 'updated': 0, 'skipped_new': 0, 'total_after': len(dictionary)
            }
        df_all = pd.concat(combined, ignore_index=True)

        added = 0
        updated = 0
        skipped_new = 0

        valid_labels = ['Symptom', 'Component', 'Tool', 'Process', 'TestCase', 'Metric', 'Material', 'Role']

        for _, row in df_all.iterrows():
            term = str(row.get('term', '')).strip()
            category = str(row.get('category', '')).strip()
            if not term or not category:
                continue
            if category not in valid_labels:
                continue

            definition = str(row.get('definition', '')).strip() if pd.notna(row.get('definition')) else ''
            aliases = normalize_list(row.get('aliases'))
            tags = normalize_list(row.get('tags'))
            sub_category = str(row.get('sub_category', '')).strip() if pd.notna(row.get('sub_category')) else ''

            key = (term, category)
            if key in index:
                # 更新
                i = index[key]
                item = dictionary[i]
                # 合并别名/标签
                old_aliases = normalize_list(item.get('aliases', []))
                old_tags = normalize_list(item.get('tags', []))
                new_aliases = sorted(list({*old_aliases, *aliases}))
                new_tags = sorted(list({*old_tags, *tags}))

                # 保留现有词典设计：不覆盖已有 definition/description，仅在缺失时补充
                if definition and not (item.get('definition') or item.get('description')):
                    item['definition'] = definition
                    item['description'] = definition
                item['aliases'] = new_aliases
                item['tags'] = new_tags
                item['category'] = category
                if sub_category:
                    item['sub_category'] = sub_category
                item['term'] = term
                item['name'] = term
                item['source'] = str(row.get('source', 'dictionary')).strip()
                item['status'] = str(row.get('status', 'active')).strip()
                item['updated_at'] = datetime.now().isoformat(timespec='seconds')
                updated += 1
            else:
                # 新增（默认不允许，避免突破1124）
                if not allow_new:
                    skipped_new += 1
                    continue
                new_item = {
                    'term': term,
                    'name': term,
                    'category': category,
                    'definition': definition,
                    'description': definition,
                    'aliases': aliases,
                    'tags': tags,
                    'sub_category': sub_category if sub_category else None,
                    'source': str(row.get('source', 'dictionary')).strip(),
                    'status': str(row.get('status', 'active')).strip(),
                    'created_at': datetime.now().isoformat(timespec='seconds'),
                    'updated_at': datetime.now().isoformat(timespec='seconds')
                }
                # 去掉None字段
                new_item = {k: v for k, v in new_item.items() if v is not None}
                dictionary.append(new_item)
                index[key] = len(dictionary) - 1
                added += 1

        # 落盘
        if not dry_run:
            backup_dir = Path('data/dictionary_backup')
            backup_dir.mkdir(parents=True, exist_ok=True)
            backup_file = backup_dir / f"dictionary_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            try:
                shutil.copyfile(dict_path, backup_file)
                print(f"💾 已备份词典到: {backup_file}")
            except Exception as e:
                print(f"⚠️ 备份失败: {e}")

            with open(dict_path, 'w', encoding='utf-8') as f:
                json.dump(dictionary, f, ensure_ascii=False, indent=2)
            print(f"✅ 已更新词典文件: {dict_path}")

        return {
            'added': added,
            'updated': updated,
            'skipped_new': skipped_new,
            'total_after': len(dictionary)
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
    print("🚀 补充词典数据 合并/导入 工具")

    ap = argparse.ArgumentParser()
    ap.add_argument('--mode', choices=['update-json', 'neo4j'], default='update-json', help='默认更新词典JSON，不直接写库')
    ap.add_argument('--dry-run', action='store_true', help='仅预览不落盘（仅对 update-json 模式有效）')
    ap.add_argument('--allow-new', action='store_true', help='允许新增术语（默认仅更新，不新增）')
    ap.add_argument('--rebuild', action='store_true', help='更新JSON后自动重建图谱（需非dry-run）')
    ap.add_argument('--dict', dest='dict_path', default='api/data/dictionary.json', help='词典JSON路径')
    ap.add_argument('--csv', nargs='*', default=['补充词典数据_批次1.csv', '补充词典数据_批次2.csv'], help='一个或多个CSV文件路径')
    args = ap.parse_args()

    importer = DictionaryDataImporter()

    try:
        # 1) 加载CSV
        dfs = []
        issues_all = []
        for csv_path in args.csv:
            if os.path.exists(csv_path):
                print(f"\n📋 加载CSV: {csv_path}")
                df = importer.load_csv_data(csv_path)
                if df is not None:
                    issues = importer.validate_data(df)
                    if issues:
                        print("⚠️  数据验证发现问题（前若干条）:")
                        for issue in issues[:10]:
                            print(f"   - {issue}")
                        issues_all.extend(issues)
                    dfs.append(df)
            else:
                print(f"⚠️ 未找到CSV: {csv_path}")

        if args.mode == 'update-json':
            # 2) 合并进词典JSON
            summary = importer.merge_into_dictionary_file(
                dfs, dict_path=args.dict_path, dry_run=args.dry_run, allow_new=args.allow_new
            )
            print(f"\n📊 合并结果: 更新 {summary['updated']} 条, 新增 {summary['added']} 条, 跳过新增 {summary['skipped_new']} 条")
            print(f"� 合并后词典总数: {summary['total_after']} 条")

            # 3) 可选重建图谱
            if args.rebuild and not args.dry_run:
                print("\n🔁 触发图谱重建...")
                try:
                    subprocess.run(['python', '自动重建图谱数据.py'], check=False)
                except Exception as e:
                    print(f"⚠️ 自动重建失败: {e}")

        else:
            # 2) 直接写库（MERGE 幂等）
            for df in dfs:
                if df is not None:
                    result = importer.import_data(df, skip_existing=False)
                    print(f"📊 导入结果: 成功{result['success']}条, 失败{result['error']}条, 跳过{result['skipped']}条")

            # 3) 统计
            stats = importer.get_statistics()
            print(f"\n📈 导入后数据库统计: 总节点数 {stats['total']}")
            for label_stat in stats['labels']:
                print(f"  {label_stat['label']}: {label_stat['count']}个")

    except Exception as e:
        print(f"❌ 处理过程中发生错误: {e}")
    finally:
        importer.close()

if __name__ == "__main__":
    main()
