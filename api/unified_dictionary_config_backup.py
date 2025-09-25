#!/usr/bin/env python3
"""
统一词典配置管理器
解决多个API使用不同词典数据源的问题
"""
import csv
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class UnifiedDictionaryManager:
    """统一词典管理器"""
    
    def __init__(self, base_dir: str = None):
        # 确定基础目录
        if base_dir:
            self.base_dir = Path(base_dir)
        else:
            # 自动检测项目根目录
            current_dir = Path(__file__).parent
            if (current_dir.parent / "ontology").exists():
                self.base_dir = current_dir.parent
            else:
                self.base_dir = current_dir
        
        # 词典数据源路径（按优先级排序）
        self.dictionary_sources = {
            "primary": self.base_dir / "ontology" / "dictionaries",
            "secondary": self.base_dir / "data" / "vocab",
            "backup": self.base_dir / "data" / "governance"
        }
        
        # 缓存
        self._cache = {}
        self._cache_timestamp = None
        
        logger.info(f"词典管理器初始化，基础目录: {self.base_dir}")
    
    def get_dictionary_data(self, force_reload: bool = False) -> Dict[str, List[Dict[str, Any]]]:
        """获取统一的词典数据"""
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
            "tools_processes": []
        }
        
        # 尝试从主要数据源加载
        if self._load_from_primary_source(dictionary_data):
            logger.info("从主要数据源加载词典成功")
        elif self._load_from_secondary_source(dictionary_data):
            logger.info("从次要数据源加载词典成功")
        else:
            logger.warning("所有数据源加载失败，使用默认数据")
            self._load_default_data(dictionary_data)
        
        # 更新缓存
        self._cache = dictionary_data
        self._cache_timestamp = datetime.now()
        
        return dictionary_data
    
    def _load_from_primary_source(self, dictionary_data: Dict) -> bool:
        """从主要数据源加载（ontology/dictionaries）"""
        try:
            primary_dir = self.dictionary_sources["primary"]
            if not primary_dir.exists():
                return False
            
            # 加载各类词典
            mappings = {
                "components": "components.csv",
                "symptoms": "symptoms.csv", 
                "causes": "causes.csv",
                "countermeasures": "countermeasures.csv"
            }
            
            loaded_any = False
            for category, filename in mappings.items():
                file_path = primary_dir / filename
                if file_path.exists():
                    count = self._load_csv_file(file_path, dictionary_data[category])
                    if count > 0:
                        loaded_any = True
                        logger.info(f"加载 {category}: {count} 条记录")
            
            # 对策词典可能映射到tools_processes
            if not dictionary_data["countermeasures"]:
                countermeasures_file = primary_dir / "countermeasures.csv"
                if countermeasures_file.exists():
                    count = self._load_csv_file(countermeasures_file, dictionary_data["tools_processes"])
                    if count > 0:
                        loaded_any = True
                        logger.info(f"加载 tools_processes: {count} 条记录")
            
            return loaded_any
            
        except Exception as e:
            logger.error(f"从主要数据源加载失败: {e}")
            return False
    
    def _load_from_secondary_source(self, dictionary_data: Dict) -> bool:
        """从次要数据源加载（data/vocab）"""
        try:
            secondary_dir = self.dictionary_sources["secondary"]
            
            # 尝试加载JSON格式
            json_file = secondary_dir / "dictionary.json"
            if json_file.exists():
                return self._load_json_file(json_file, dictionary_data)
            
            # 尝试加载CSV格式
            csv_files = {
                "components": secondary_dir / "components.csv",
                "symptoms": secondary_dir / "symptoms.csv",
                "causes": secondary_dir / "causes.csv"
            }
            
            loaded_any = False
            for category, file_path in csv_files.items():
                if file_path.exists():
                    count = self._load_simple_csv(file_path, dictionary_data[category])
                    if count > 0:
                        loaded_any = True
                        logger.info(f"加载 {category}: {count} 条记录")
            
            return loaded_any
            
        except Exception as e:
            logger.error(f"从次要数据源加载失败: {e}")
            return False
    
    def _load_csv_file(self, file_path: Path, target_list: List) -> int:
        """加载标准CSV文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                count = 0
                for row in reader:
                    entry = {
                        "name": row.get("term", row.get("name", "")),
                        "canonical_name": row.get("canonical_name", row.get("term", row.get("name", ""))),
                        "category": row.get("category", "未分类"),
                        "aliases": self._parse_aliases(row.get("aliases", "")),
                        "tags": self._parse_tags(row.get("tags", "")),
                        "description": row.get("description", row.get("definition", ""))
                    }
                    if entry["name"]:
                        target_list.append(entry)
                        count += 1
                return count
        except Exception as e:
            logger.error(f"加载CSV文件失败 {file_path}: {e}")
            return 0
    
    def _load_simple_csv(self, file_path: Path, target_list: List) -> int:
        """加载简单CSV文件（name,alias格式）"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                count = 0
                for row in reader:
                    name = row.get("name", "")
                    alias = row.get("alias", "")
                    if name:
                        entry = {
                            "name": name,
                            "canonical_name": name,
                            "category": "未分类",
                            "aliases": [alias] if alias else [],
                            "tags": [],
                            "description": ""
                        }
                        target_list.append(entry)
                        count += 1
                return count
        except Exception as e:
            logger.error(f"加载简单CSV文件失败 {file_path}: {e}")
            return 0
    
    def _load_json_file(self, file_path: Path, dictionary_data: Dict) -> bool:
        """加载JSON格式词典"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                entries = data.get('entries', [])
                
                # 按类别分组
                for entry in entries:
                    category = entry.get('category', '未分类')
                    formatted_entry = {
                        "name": entry.get('term', ''),
                        "canonical_name": entry.get('term', ''),
                        "category": category,
                        "aliases": entry.get('aliases', []),
                        "tags": entry.get('tags', []),
                        "description": entry.get('definition', '')
                    }
                    
                    # 根据类别分配到对应列表
                    if '硬件' in category or '组件' in category:
                        dictionary_data["components"].append(formatted_entry)
                    elif '症状' in category or '异常' in category:
                        dictionary_data["symptoms"].append(formatted_entry)
                    elif '原因' in category or '成因' in category:
                        dictionary_data["causes"].append(formatted_entry)
                    elif '对策' in category or '解决' in category:
                        dictionary_data["countermeasures"].append(formatted_entry)
                    else:
                        dictionary_data["components"].append(formatted_entry)
                
                return len(entries) > 0
                
        except Exception as e:
            logger.error(f"加载JSON文件失败 {file_path}: {e}")
            return False
    
    def _parse_aliases(self, aliases_str: str) -> List[str]:
        """解析别名字符串"""
        if not aliases_str:
            return []
        return [alias.strip() for alias in aliases_str.split(';') if alias.strip()]
    
    def _parse_tags(self, tags_str: str) -> List[str]:
        """解析标签字符串"""
        if not tags_str:
            return []
        return [tag.strip() for tag in tags_str.split(';') if tag.strip()]
    
    def _load_default_data(self, dictionary_data: Dict):
        """加载默认数据"""
        default_components = [
            {
                "name": "摄像头",
                "canonical_name": "摄像头",
                "category": "硬件组件",
                "aliases": ["相机", "Camera"],
                "tags": ["硬件"],
                "description": "用于拍照和录像的硬件组件"
            },
            {
                "name": "屏幕",
                "canonical_name": "屏幕", 
                "category": "硬件组件",
                "aliases": ["显示屏", "Display"],
                "tags": ["硬件"],
                "description": "显示图像和界面的硬件组件"
            }
        ]
        
        dictionary_data["components"].extend(default_components)
        logger.info("加载默认词典数据")
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取词典统计信息"""
        data = self.get_dictionary_data()
        return {
            "total_entries": sum(len(entries) for entries in data.values()),
            "components": len(data["components"]),
            "symptoms": len(data["symptoms"]),
            "causes": len(data["causes"]),
            "countermeasures": len(data["countermeasures"]),
            "tools_processes": len(data["tools_processes"]),
            "data_sources": {
                "primary": str(self.dictionary_sources["primary"]),
                "secondary": str(self.dictionary_sources["secondary"])
            },
            "cache_status": "active" if self._cache else "empty"
        }

# 创建全局实例
unified_dictionary = UnifiedDictionaryManager()

def get_unified_dictionary() -> Dict[str, List[Dict[str, Any]]]:
    """获取统一词典数据的便捷函数"""
    return unified_dictionary.get_dictionary_data()

def get_dictionary_statistics() -> Dict[str, Any]:
    """获取词典统计信息的便捷函数"""
    return unified_dictionary.get_statistics()
