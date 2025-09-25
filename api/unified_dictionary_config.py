#!/usr/bin/env python3
"""
简化版统一词典管理器
只使用ontology/dictionaries作为数据源
"""
import csv
import logging
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class SimplifiedDictionaryManager:
    """简化版词典管理器 - 只使用ontology/dictionaries"""
    
    def __init__(self):
        # 固定使用ontology/dictionaries作为数据源
        # 检测当前是否在api目录中
        current_dir = Path.cwd()
        if current_dir.name == "api":
            self.dictionary_dir = Path("../ontology/dictionaries")
        else:
            self.dictionary_dir = Path("ontology/dictionaries")
        
        # 缓存
        self._cache = {}
        self._cache_timestamp = None
        
        logger.info(f"词典管理器初始化，数据源: {self.dictionary_dir}")
    
    def get_dictionary_data(self, force_reload: bool = False) -> Dict[str, List[Dict[str, Any]]]:
        """获取词典数据"""
        # 检查缓存
        if not force_reload and self._cache and self._cache_timestamp:
            cache_age = (datetime.now() - self._cache_timestamp).seconds
            if cache_age < 300:  # 5分钟缓存
                return self._cache
        
        dictionary_data = {
            "components": [],
            "symptoms": [],
            "causes": [],
            "countermeasures": [],
            "tools_processes": []  # 兼容性字段
        }
        
        # 加载各类词典
        mappings = {
            "components": "components.csv",
            "symptoms": "symptoms.csv", 
            "causes": "causes.csv",
            "countermeasures": "countermeasures.csv"
        }
        
        total_loaded = 0
        for category, filename in mappings.items():
            file_path = self.dictionary_dir / filename
            if file_path.exists():
                count = self._load_csv_file(file_path, dictionary_data[category])
                total_loaded += count
                logger.info(f"加载 {category}: {count} 条记录")
        
        # 对策词典也映射到tools_processes（兼容性）
        dictionary_data["tools_processes"] = dictionary_data["countermeasures"].copy()
        
        # 更新缓存
        self._cache = dictionary_data
        self._cache_timestamp = datetime.now()
        
        logger.info(f"词典加载完成，总计: {total_loaded} 条记录")
        return dictionary_data
    
    def _load_csv_file(self, file_path: Path, target_list: List) -> int:
        """加载CSV文件 - 适配新字段格式"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                count = 0
                for row in reader:
                    # 适配新的字段格式：术语,别名,类别,多标签,备注
                    term = row.get("术语", row.get("term", ""))
                    aliases_str = row.get("别名", row.get("aliases", ""))
                    category = row.get("类别", row.get("category", "未分类"))
                    tags_str = row.get("多标签", row.get("tags", ""))
                    description = row.get("备注", row.get("description", ""))

                    entry = {
                        "name": term,
                        "canonical_name": term,  # 使用术语作为标准名称
                        "category": category,
                        "aliases": self._parse_aliases(aliases_str),
                        "tags": self._parse_aliases(tags_str),  # 多标签用同样的解析方法
                        "description": description
                    }
                    if entry["name"]:
                        target_list.append(entry)
                        count += 1
                return count
        except Exception as e:
            logger.error(f"加载CSV文件失败 {file_path}: {e}")
            return 0
    
    def _parse_aliases(self, aliases_str: str) -> List[str]:
        """解析别名字符串"""
        if not aliases_str:
            return []
        return [alias.strip() for alias in aliases_str.split(';') if alias.strip()]
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取词典统计信息"""
        data = self.get_dictionary_data()
        return {
            "total_entries": sum(len(entries) for entries in data.values() if isinstance(entries, list)),
            "components": len(data["components"]),
            "symptoms": len(data["symptoms"]),
            "causes": len(data["causes"]),
            "countermeasures": len(data["countermeasures"]),
            "tools_processes": len(data["tools_processes"]),
            "data_source": str(self.dictionary_dir),
            "cache_status": "active" if self._cache else "empty"
        }

# 创建全局实例
unified_dictionary = SimplifiedDictionaryManager()

def get_unified_dictionary() -> Dict[str, List[Dict[str, Any]]]:
    """获取统一词典数据的便捷函数"""
    return unified_dictionary.get_dictionary_data()

def get_dictionary_statistics() -> Dict[str, Any]:
    """获取词典统计信息的便捷函数"""
    return unified_dictionary.get_statistics()
