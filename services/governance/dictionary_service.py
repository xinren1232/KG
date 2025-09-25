#!/usr/bin/env python3
"""
词典管理服务
提供标准化、别名映射、冲突检测和导入校验功能
"""

import csv
import json
import re
import logging
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import difflib

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class DictionaryEntry:
    """词典条目"""
    term: str
    canonical_name: str
    aliases: List[str]
    category: str
    tags: List[str] = field(default_factory=list)
    description: str = ""
    confidence: float = 1.0
    source: str = ""
    created_at: str = ""
    updated_at: str = ""
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if not self.updated_at:
            self.updated_at = datetime.now().isoformat()

@dataclass
class ValidationResult:
    """验证结果"""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    suggestions: List[str]
    
    def __post_init__(self):
        if not hasattr(self, 'errors'):
            self.errors = []
        if not hasattr(self, 'warnings'):
            self.warnings = []
        if not hasattr(self, 'suggestions'):
            self.suggestions = []

class DictionaryService:
    """词典管理服务"""
    
    def __init__(self, dictionary_dir: str = "ontology/dictionaries"):
        self.dictionary_dir = Path(dictionary_dir)
        self.dictionary_dir.mkdir(parents=True, exist_ok=True)
        
        # 词典数据
        self.dictionaries: Dict[str, Dict[str, DictionaryEntry]] = {}
        self.alias_mapping: Dict[str, str] = {}  # alias -> canonical_name
        self.category_mapping: Dict[str, str] = {}  # term -> category
        
        # 配置
        self.similarity_threshold = 0.8
        self.valid_categories = {
            "components", "symptoms", "causes", "countermeasures",
            "products", "suppliers", "owners", "test_cases",
            "enhanced_components", "enhanced_symptoms", "enhanced_tools_processes"
        }
        
        # 加载现有词典
        self._load_dictionaries()
    
    def _load_dictionaries(self):
        """加载所有词典文件"""
        logger.info(f"Loading dictionaries from {self.dictionary_dir}")
        
        for category in self.valid_categories:
            dict_file = self.dictionary_dir / f"{category}.csv"
            if dict_file.exists():
                self._load_dictionary_file(category, dict_file)
            else:
                logger.warning(f"Dictionary file not found: {dict_file}")
                self.dictionaries[category] = {}
        
        self._build_mappings()
        logger.info(f"Loaded {len(self.alias_mapping)} aliases across {len(self.dictionaries)} categories")
    
    def _load_dictionary_file(self, category: str, file_path: Path):
        """加载单个词典文件"""
        try:
            entries = {}
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    term = row.get('term', '').strip()
                    canonical_name = row.get('canonical_name', term).strip()
                    aliases_str = row.get('aliases', '').strip()
                    tags_str = row.get('tags', '').strip()
                    description = row.get('description', '').strip()

                    if term:
                        aliases = [alias.strip() for alias in aliases_str.split(';') if alias.strip()]
                        tags = [tag.strip() for tag in tags_str.split(';') if tag.strip()]
                        entry = DictionaryEntry(
                            term=term,
                            canonical_name=canonical_name,
                            aliases=aliases,
                            category=category,
                            tags=tags,
                            description=description,
                            source=str(file_path)
                        )
                        entries[term] = entry
            
            self.dictionaries[category] = entries
            logger.info(f"Loaded {len(entries)} entries from {category} dictionary")
            
        except Exception as e:
            logger.error(f"Failed to load dictionary {file_path}: {e}")
            self.dictionaries[category] = {}
    
    def _build_mappings(self):
        """构建别名映射和分类映射"""
        self.alias_mapping.clear()
        self.category_mapping.clear()
        
        for category, entries in self.dictionaries.items():
            for term, entry in entries.items():
                # 主名称映射
                self.alias_mapping[entry.canonical_name.lower()] = entry.canonical_name
                self.category_mapping[entry.canonical_name] = category
                
                # 别名映射
                for alias in entry.aliases:
                    if alias:
                        self.alias_mapping[alias.lower()] = entry.canonical_name
                        self.category_mapping[alias] = category
                
                # 原始术语映射
                if term != entry.canonical_name:
                    self.alias_mapping[term.lower()] = entry.canonical_name
                    self.category_mapping[term] = category
    
    def normalize(self, term: str) -> str:
        """标准化术语"""
        if not term or not isinstance(term, str):
            return ""
        
        # 清理输入
        cleaned_term = term.strip()
        if not cleaned_term:
            return ""
        
        # 直接匹配
        canonical = self.alias_mapping.get(cleaned_term.lower())
        if canonical:
            return canonical
        
        # 模糊匹配
        best_match = self._fuzzy_match(cleaned_term)
        if best_match:
            return best_match
        
        # 返回原始术语（清理后）
        return cleaned_term
    
    def _fuzzy_match(self, term: str) -> Optional[str]:
        """模糊匹配"""
        term_lower = term.lower()
        best_match = None
        best_score = 0
        
        for alias, canonical in self.alias_mapping.items():
            # 计算相似度
            score = difflib.SequenceMatcher(None, term_lower, alias).ratio()
            
            if score > best_score and score >= self.similarity_threshold:
                best_score = score
                best_match = canonical
        
        return best_match
    
    def get_category(self, term: str) -> Optional[str]:
        """获取术语的分类"""
        canonical = self.normalize(term)
        return self.category_mapping.get(canonical)
    
    def add_entry(self, category: str, term: str, canonical_name: str = None, 
                  aliases: List[str] = None, description: str = "") -> ValidationResult:
        """添加词典条目"""
        # 验证输入
        validation = self._validate_entry(category, term, canonical_name, aliases, description)
        if not validation.is_valid:
            return validation
        
        # 创建条目
        if canonical_name is None:
            canonical_name = term
        if aliases is None:
            aliases = []
        
        entry = DictionaryEntry(
            term=term,
            canonical_name=canonical_name,
            aliases=aliases,
            category=category,
            description=description
        )
        
        # 添加到词典
        if category not in self.dictionaries:
            self.dictionaries[category] = {}
        
        self.dictionaries[category][term] = entry
        
        # 重建映射
        self._build_mappings()
        
        logger.info(f"Added entry: {term} -> {canonical_name} in {category}")
        return ValidationResult(is_valid=True, errors=[], warnings=[], suggestions=[])
    
    def _validate_entry(self, category: str, term: str, canonical_name: str = None,
                       aliases: List[str] = None, description: str = "") -> ValidationResult:
        """验证词典条目"""
        errors = []
        warnings = []
        suggestions = []
        
        # 验证分类
        if category not in self.valid_categories:
            errors.append(f"Invalid category: {category}. Valid categories: {', '.join(self.valid_categories)}")
        
        # 验证术语
        if not term or not isinstance(term, str) or not term.strip():
            errors.append("Term cannot be empty")
        else:
            term = term.strip()
            
            # 检查非法字符
            if re.search(r'[<>"\'\\\n\r\t]', term):
                errors.append(f"Term contains illegal characters: {term}")
            
            # 检查重复
            if category in self.dictionaries and term in self.dictionaries[category]:
                warnings.append(f"Term already exists: {term}")
        
        # 验证标准名称
        if canonical_name:
            canonical_name = canonical_name.strip()
            if re.search(r'[<>"\'\\\n\r\t]', canonical_name):
                errors.append(f"Canonical name contains illegal characters: {canonical_name}")
        
        # 验证别名
        if aliases:
            for alias in aliases:
                if alias and re.search(r'[<>"\'\\\n\r\t]', alias):
                    errors.append(f"Alias contains illegal characters: {alias}")
                
                # 检查别名冲突
                existing_canonical = self.alias_mapping.get(alias.lower())
                if existing_canonical and existing_canonical != (canonical_name or term):
                    warnings.append(f"Alias '{alias}' already maps to '{existing_canonical}'")
        
        # 相似性检查
        if term:
            similar_terms = self._find_similar_terms(term, category)
            if similar_terms:
                suggestions.extend([f"Similar term found: {sim_term}" for sim_term in similar_terms])
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            suggestions=suggestions
        )
    
    def _find_similar_terms(self, term: str, category: str, threshold: float = 0.7) -> List[str]:
        """查找相似术语"""
        similar_terms = []
        term_lower = term.lower()
        
        if category in self.dictionaries:
            for existing_term in self.dictionaries[category].keys():
                score = difflib.SequenceMatcher(None, term_lower, existing_term.lower()).ratio()
                if score >= threshold and score < 1.0:  # 相似但不完全相同
                    similar_terms.append(existing_term)
        
        return similar_terms
    
    def detect_conflicts(self) -> List[Dict[str, Any]]:
        """检测词典冲突"""
        conflicts = []
        
        # 检查别名冲突
        alias_conflicts = {}
        for alias, canonical in self.alias_mapping.items():
            if alias in alias_conflicts:
                conflicts.append({
                    "type": "alias_conflict",
                    "alias": alias,
                    "canonical_names": [alias_conflicts[alias], canonical],
                    "severity": "high"
                })
            else:
                alias_conflicts[alias] = canonical
        
        # 检查分类冲突
        for category, entries in self.dictionaries.items():
            for term, entry in entries.items():
                # 检查同一术语在不同分类中
                for other_category, other_entries in self.dictionaries.items():
                    if other_category != category and term in other_entries:
                        conflicts.append({
                            "type": "category_conflict",
                            "term": term,
                            "categories": [category, other_category],
                            "severity": "medium"
                        })
        
        return conflicts
    
    def import_from_csv(self, category: str, file_path: str) -> Dict[str, Any]:
        """从CSV文件导入词典"""
        result = {
            "imported": 0,
            "skipped": 0,
            "errors": [],
            "warnings": []
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row_num, row in enumerate(reader, 1):
                    try:
                        term = row.get('term', '').strip()
                        canonical_name = row.get('canonical_name', '').strip() or term
                        aliases_str = row.get('aliases', '').strip()
                        description = row.get('description', '').strip()
                        
                        aliases = [alias.strip() for alias in aliases_str.split(';') if alias.strip()]
                        
                        validation = self.add_entry(category, term, canonical_name, aliases, description)
                        
                        if validation.is_valid:
                            result["imported"] += 1
                        else:
                            result["skipped"] += 1
                            result["errors"].extend([f"Row {row_num}: {error}" for error in validation.errors])
                        
                        result["warnings"].extend([f"Row {row_num}: {warning}" for warning in validation.warnings])
                        
                    except Exception as e:
                        result["errors"].append(f"Row {row_num}: {str(e)}")
                        result["skipped"] += 1
        
        except Exception as e:
            result["errors"].append(f"Failed to read file: {str(e)}")
        
        return result
    
    def export_to_csv(self, category: str, file_path: str) -> bool:
        """导出词典到CSV文件"""
        try:
            if category not in self.dictionaries:
                logger.error(f"Category not found: {category}")
                return False
            
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                fieldnames = ['term', 'canonical_name', 'aliases', 'description', 'created_at', 'updated_at']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for entry in self.dictionaries[category].values():
                    writer.writerow({
                        'term': entry.term,
                        'canonical_name': entry.canonical_name,
                        'aliases': ';'.join(entry.aliases),
                        'description': entry.description,
                        'created_at': entry.created_at,
                        'updated_at': entry.updated_at
                    })
            
            logger.info(f"Exported {category} dictionary to {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to export dictionary: {e}")
            return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取词典统计信息"""
        stats = {
            "categories": len(self.dictionaries),
            "total_entries": sum(len(entries) for entries in self.dictionaries.values()),
            "total_aliases": len(self.alias_mapping),
            "category_stats": {}
        }
        
        for category, entries in self.dictionaries.items():
            total_aliases = sum(len(entry.aliases) for entry in entries.values())
            stats["category_stats"][category] = {
                "entries": len(entries),
                "aliases": total_aliases,
                "avg_aliases_per_entry": total_aliases / len(entries) if entries else 0
            }
        
        return stats
    
    def search(self, query: str, category: str = None, limit: int = 10) -> List[Dict[str, Any]]:
        """搜索词典条目"""
        results = []
        query_lower = query.lower()
        
        categories_to_search = [category] if category else self.dictionaries.keys()
        
        for cat in categories_to_search:
            if cat not in self.dictionaries:
                continue
                
            for entry in self.dictionaries[cat].values():
                score = 0
                
                # 精确匹配
                if query_lower == entry.canonical_name.lower():
                    score = 1.0
                elif query_lower in [alias.lower() for alias in entry.aliases]:
                    score = 0.9
                elif query_lower == entry.term.lower():
                    score = 0.8
                # 部分匹配
                elif query_lower in entry.canonical_name.lower():
                    score = 0.6
                elif any(query_lower in alias.lower() for alias in entry.aliases):
                    score = 0.5
                elif query_lower in entry.description.lower():
                    score = 0.3
                
                if score > 0:
                    results.append({
                        "entry": asdict(entry),
                        "score": score,
                        "match_type": "exact" if score >= 0.8 else "partial"
                    })
        
        # 排序并限制结果
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:limit]

def main():
    """主函数用于测试"""
    service = DictionaryService()
    
    # 测试标准化
    test_terms = ["摄像头", "Camera", "相机", "镜头", "未知组件"]
    for term in test_terms:
        normalized = service.normalize(term)
        category = service.get_category(term)
        print(f"{term} -> {normalized} ({category})")
    
    # 获取统计信息
    stats = service.get_statistics()
    print(f"\nDictionary Statistics:")
    print(f"Total entries: {stats['total_entries']}")
    print(f"Total aliases: {stats['total_aliases']}")

if __name__ == "__main__":
    main()
