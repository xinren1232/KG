#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
词典管理系统
支持重复清除、批量导入、持续更新等功能
"""

import json
import csv
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any, Optional, Set, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import logging
import hashlib

logger = logging.getLogger(__name__)

@dataclass
class DictionaryEntry:
    """词典条目数据结构"""
    term: str                    # 主术语
    aliases: List[str]           # 别名列表
    category: str                # 类别
    tags: List[str]              # 多标签
    definition: str              # 定义/备注
    source: str = "manual"       # 来源：manual/import/auto
    created_at: str = None       # 创建时间
    updated_at: str = None       # 更新时间
    version: int = 1             # 版本号
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
        if self.updated_at is None:
            self.updated_at = self.created_at
    
    def get_hash(self) -> str:
        """生成条目的唯一哈希值"""
        content = f"{self.term.lower()}|{self.category.lower()}"
        return hashlib.md5(content.encode()).hexdigest()[:8]
    
    def get_all_terms(self) -> Set[str]:
        """获取所有术语（主术语+别名）"""
        terms = {self.term.lower()}
        terms.update(alias.lower() for alias in self.aliases)
        return terms

class DictionaryManager:
    """词典管理器"""
    
    def __init__(self, data_dir: Path = None):
        self.data_dir = data_dir or Path("data/vocab")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # 词典文件路径
        self.dictionary_file = self.data_dir / "dictionary.json"
        self.backup_dir = self.data_dir / "backups"
        self.backup_dir.mkdir(exist_ok=True)
        
        # 加载现有词典
        self.entries: Dict[str, DictionaryEntry] = {}
        self.load_dictionary()
    
    def load_dictionary(self):
        """加载词典数据"""
        try:
            if self.dictionary_file.exists():
                with open(self.dictionary_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for entry_data in data.get('entries', []):
                        entry = DictionaryEntry(**entry_data)
                        self.entries[entry.get_hash()] = entry
                logger.info(f"加载词典成功: {len(self.entries)} 条记录")
            else:
                # 从旧格式迁移
                self._migrate_from_old_format()
        except Exception as e:
            logger.error(f"加载词典失败: {e}")
    
    def save_dictionary(self):
        """保存词典数据"""
        try:
            # 创建备份
            self._create_backup()
            
            # 保存新数据
            data = {
                'version': '1.0',
                'updated_at': datetime.now().isoformat(),
                'total_entries': len(self.entries),
                'entries': [asdict(entry) for entry in self.entries.values()]
            }
            
            with open(self.dictionary_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"保存词典成功: {len(self.entries)} 条记录")
        except Exception as e:
            logger.error(f"保存词典失败: {e}")
            raise
    
    def add_entry(self, entry: DictionaryEntry) -> bool:
        """添加词典条目"""
        entry_hash = entry.get_hash()
        
        if entry_hash in self.entries:
            logger.warning(f"词典条目已存在: {entry.term}")
            return False
        
        self.entries[entry_hash] = entry
        logger.info(f"添加词典条目: {entry.term}")
        return True
    
    def update_entry(self, entry: DictionaryEntry) -> bool:
        """更新词典条目"""
        entry_hash = entry.get_hash()
        
        if entry_hash in self.entries:
            # 保留创建时间，更新其他信息
            entry.created_at = self.entries[entry_hash].created_at
            entry.version = self.entries[entry_hash].version + 1
            entry.updated_at = datetime.now().isoformat()
            
            self.entries[entry_hash] = entry
            logger.info(f"更新词典条目: {entry.term}")
            return True
        else:
            # 新增条目
            return self.add_entry(entry)
    
    def delete_entry(self, term: str, category: str) -> bool:
        """删除词典条目"""
        temp_entry = DictionaryEntry(term=term, category=category, aliases=[], tags=[], definition="")
        entry_hash = temp_entry.get_hash()
        
        if entry_hash in self.entries:
            del self.entries[entry_hash]
            logger.info(f"删除词典条目: {term}")
            return True
        
        logger.warning(f"词典条目不存在: {term}")
        return False
    
    def find_duplicates(self) -> List[Dict[str, Any]]:
        """查找重复条目"""
        duplicates = []
        term_to_entries = {}
        
        # 按术语分组
        for entry_hash, entry in self.entries.items():
            for term in entry.get_all_terms():
                if term not in term_to_entries:
                    term_to_entries[term] = []
                term_to_entries[term].append((entry_hash, entry))
        
        # 找出重复的术语
        for term, entries_list in term_to_entries.items():
            if len(entries_list) > 1:
                duplicates.append({
                    'term': term,
                    'count': len(entries_list),
                    'entries': [
                        {
                            'hash': entry_hash,
                            'main_term': entry.term,
                            'category': entry.category,
                            'aliases': entry.aliases,
                            'definition': entry.definition
                        }
                        for entry_hash, entry in entries_list
                    ]
                })
        
        return duplicates
    
    def remove_duplicates(self, strategy: str = "keep_latest") -> Dict[str, Any]:
        """清除重复条目
        
        Args:
            strategy: 清除策略
                - keep_latest: 保留最新的
                - keep_first: 保留最早的
                - merge: 合并条目
        """
        duplicates = self.find_duplicates()
        removed_count = 0
        merged_count = 0
        
        for duplicate in duplicates:
            entries = duplicate['entries']
            
            if strategy == "keep_latest":
                # 按更新时间排序，保留最新的
                entries.sort(key=lambda x: self.entries[x['hash']].updated_at)
                to_remove = entries[:-1]
                
                for entry_info in to_remove:
                    del self.entries[entry_info['hash']]
                    removed_count += 1
                    
            elif strategy == "keep_first":
                # 按创建时间排序，保留最早的
                entries.sort(key=lambda x: self.entries[x['hash']].created_at)
                to_remove = entries[1:]
                
                for entry_info in to_remove:
                    del self.entries[entry_info['hash']]
                    removed_count += 1
                    
            elif strategy == "merge":
                # 合并条目
                if len(entries) > 1:
                    # 获取有效的条目对象
                    valid_entries = []
                    for entry_info in entries:
                        if entry_info['hash'] in self.entries:
                            valid_entries.append(self.entries[entry_info['hash']])

                    if len(valid_entries) > 1:
                        merged_entry = self._merge_entries(valid_entries)

                        # 删除原条目
                        for entry_info in entries:
                            if entry_info['hash'] in self.entries:
                                del self.entries[entry_info['hash']]

                        # 添加合并后的条目
                        self.entries[merged_entry.get_hash()] = merged_entry
                        merged_count += 1
                        removed_count += len(valid_entries) - 1
        
        return {
            'duplicates_found': len(duplicates),
            'entries_removed': removed_count,
            'entries_merged': merged_count,
            'strategy': strategy
        }
    
    def _merge_entries(self, entries: List[DictionaryEntry]) -> DictionaryEntry:
        """合并多个条目"""
        # 选择主术语（最短的非空术语）
        main_term = min((e.term for e in entries if e.term), key=len)
        
        # 合并别名
        all_aliases = set()
        for entry in entries:
            all_aliases.update(entry.aliases)
            if entry.term != main_term:
                all_aliases.add(entry.term)
        
        # 合并标签
        all_tags = set()
        for entry in entries:
            all_tags.update(entry.tags)
        
        # 选择最详细的定义
        definition = max((e.definition for e in entries if e.definition), key=len, default="")
        
        # 选择最常见的类别
        categories = [e.category for e in entries if e.category]
        category = max(set(categories), key=categories.count) if categories else ""
        
        # 创建合并后的条目
        merged_entry = DictionaryEntry(
            term=main_term,
            aliases=list(all_aliases),
            category=category,
            tags=list(all_tags),
            definition=definition,
            source="merged",
            created_at=min(e.created_at for e in entries),
            updated_at=datetime.now().isoformat(),
            version=max(e.version for e in entries) + 1
        )
        
        return merged_entry

    def batch_import_from_table(self, table_data: List[Dict[str, str]]) -> Dict[str, Any]:
        """从表格数据批量导入词典

        Args:
            table_data: 表格数据，每行包含 term, aliases, category, tags, definition
        """
        imported_count = 0
        updated_count = 0
        skipped_count = 0
        errors = []

        for i, row in enumerate(table_data):
            try:
                # 解析数据
                term = row.get('术语', '').strip()
                aliases_str = row.get('别名', '')
                category = row.get('类别', '').strip()
                tags_str = row.get('多标签', '')
                definition = row.get('备注', '').strip()

                if not term:
                    skipped_count += 1
                    continue

                # 解析别名（分号分隔）
                aliases = []
                if aliases_str:
                    aliases = [alias.strip() for alias in aliases_str.split(';') if alias.strip()]

                # 解析标签（分号分隔）
                tags = []
                if tags_str:
                    tags = [tag.strip() for tag in tags_str.split(';') if tag.strip()]

                # 创建词典条目
                entry = DictionaryEntry(
                    term=term,
                    aliases=aliases,
                    category=category,
                    tags=tags,
                    definition=definition,
                    source="import"
                )

                # 检查是否已存在
                entry_hash = entry.get_hash()
                if entry_hash in self.entries:
                    # 更新现有条目
                    self.update_entry(entry)
                    updated_count += 1
                else:
                    # 添加新条目
                    self.add_entry(entry)
                    imported_count += 1

            except Exception as e:
                errors.append(f"第{i+1}行: {str(e)}")

        return {
            'imported': imported_count,
            'updated': updated_count,
            'skipped': skipped_count,
            'errors': errors,
            'total_processed': len(table_data)
        }

    def export_to_csv(self, file_path: Path = None) -> Path:
        """导出词典到CSV文件"""
        if file_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = self.data_dir / f"dictionary_export_{timestamp}.csv"

        data = []
        for entry in self.entries.values():
            data.append({
                '术语': entry.term,
                '别名': ';'.join(entry.aliases),
                '类别': entry.category,
                '多标签': ';'.join(entry.tags),
                '备注': entry.definition,
                '来源': entry.source,
                '创建时间': entry.created_at,
                '更新时间': entry.updated_at,
                '版本': entry.version
            })

        df = pd.DataFrame(data)
        df.to_csv(file_path, index=False, encoding='utf-8-sig')

        logger.info(f"导出词典到: {file_path}")
        return file_path

    def get_statistics(self) -> Dict[str, Any]:
        """获取词典统计信息"""
        categories = {}
        sources = {}
        total_aliases = 0

        for entry in self.entries.values():
            # 统计类别
            categories[entry.category] = categories.get(entry.category, 0) + 1

            # 统计来源
            sources[entry.source] = sources.get(entry.source, 0) + 1

            # 统计别名
            total_aliases += len(entry.aliases)

        return {
            'total_entries': len(self.entries),
            'total_aliases': total_aliases,
            'categories': categories,
            'sources': sources,
            'avg_aliases_per_entry': round(total_aliases / len(self.entries), 2) if self.entries else 0
        }

    def search_entries(self, query: str, category: str = None) -> List[DictionaryEntry]:
        """搜索词典条目"""
        query_lower = query.lower()
        results = []

        for entry in self.entries.values():
            # 类别过滤
            if category and entry.category != category:
                continue

            # 文本匹配
            if (query_lower in entry.term.lower() or
                any(query_lower in alias.lower() for alias in entry.aliases) or
                query_lower in entry.definition.lower() or
                any(query_lower in tag.lower() for tag in entry.tags)):
                results.append(entry)

        return results

    def _create_backup(self):
        """创建备份"""
        if self.dictionary_file.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = self.backup_dir / f"dictionary_backup_{timestamp}.json"

            import shutil
            shutil.copy2(self.dictionary_file, backup_file)

            # 只保留最近10个备份
            backups = sorted(self.backup_dir.glob("dictionary_backup_*.json"))
            if len(backups) > 10:
                for old_backup in backups[:-10]:
                    old_backup.unlink()

    def _migrate_from_old_format(self):
        """从旧格式迁移数据"""
        try:
            # 迁移components.csv
            components_file = self.data_dir / "components.csv"
            if components_file.exists():
                df = pd.read_csv(components_file)
                for _, row in df.iterrows():
                    name = str(row.get('name', '')).strip()
                    alias = str(row.get('alias', '')).strip()

                    if name:
                        aliases = [alias] if alias else []
                        entry = DictionaryEntry(
                            term=name,
                            aliases=aliases,
                            category="硬件相关",
                            tags=["部件"],
                            definition="",
                            source="migration"
                        )
                        self.add_entry(entry)

            # 迁移symptoms.csv
            symptoms_file = self.data_dir / "symptoms.csv"
            if symptoms_file.exists():
                df = pd.read_csv(symptoms_file)
                for _, row in df.iterrows():
                    name = str(row.get('name', '')).strip()
                    if name:
                        entry = DictionaryEntry(
                            term=name,
                            aliases=[],
                            category="异常现象",
                            tags=["症状"],
                            definition="",
                            source="migration"
                        )
                        self.add_entry(entry)

            # 迁移causes.csv
            causes_file = self.data_dir / "causes.csv"
            if causes_file.exists():
                df = pd.read_csv(causes_file)
                for _, row in df.iterrows():
                    name = str(row.get('name', '')).strip()
                    if name:
                        entry = DictionaryEntry(
                            term=name,
                            aliases=[],
                            category="根因分析",
                            tags=["根因"],
                            definition="",
                            source="migration"
                        )
                        self.add_entry(entry)

            logger.info("旧格式数据迁移完成")

        except Exception as e:
            logger.error(f"数据迁移失败: {e}")
