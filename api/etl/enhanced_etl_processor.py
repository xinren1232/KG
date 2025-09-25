#!/usr/bin/env python3
"""
增强版Excel ETL处理器
支持幂等导入、字段映射、错误处理和统计报告
"""

import pandas as pd
import json
import yaml
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import hashlib

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ETLStats:
    """ETL统计信息"""
    total_rows: int = 0
    processed_rows: int = 0
    success_rows: int = 0
    failed_rows: int = 0
    skipped_rows: int = 0
    duplicate_rows: int = 0
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    errors: List[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = []
    
    @property
    def duration(self) -> Optional[float]:
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return None
    
    @property
    def success_rate(self) -> float:
        if self.processed_rows > 0:
            return self.success_rows / self.processed_rows
        return 0.0

class EnhancedETLProcessor:
    """增强版Excel ETL处理器"""
    
    def __init__(self, mapping_file: str = "api/etl/mapping.yaml"):
        self.mapping_file = Path(mapping_file)
        self.mapping = self._load_mapping()
        self.stats = ETLStats()
        self.processed_hashes = set()  # 用于检测重复行
        
    def _load_mapping(self) -> Dict[str, Any]:
        """加载字段映射配置"""
        try:
            if self.mapping_file.exists():
                with open(self.mapping_file, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f)
            else:
                logger.warning(f"Mapping file not found: {self.mapping_file}")
                return self._get_default_mapping()
        except Exception as e:
            logger.error(f"Failed to load mapping file: {e}")
            return self._get_default_mapping()
    
    def _get_default_mapping(self) -> Dict[str, Any]:
        """获取默认字段映射"""
        return {
            "entities": {
                "Product": {
                    "id_field": "产品",
                    "name_field": "产品",
                    "properties": {
                        "category": "产品类别",
                        "description": "产品描述"
                    }
                },
                "Build": {
                    "id_field": "版本",
                    "name_field": "版本",
                    "properties": {
                        "product_id": "产品",
                        "release_date": "发布日期"
                    }
                },
                "Component": {
                    "id_field": "组件",
                    "name_field": "组件",
                    "properties": {
                        "type": "组件类型",
                        "category": "组件分类"
                    }
                },
                "Anomaly": {
                    "id_field": "异常ID",
                    "name_field": "异常描述",
                    "properties": {
                        "severity": "严重程度",
                        "status": "状态",
                        "occurrence_date": "发生日期"
                    }
                },
                "Symptom": {
                    "id_field": "症状",
                    "name_field": "症状",
                    "properties": {
                        "category": "症状分类",
                        "severity": "严重程度"
                    }
                }
            },
            "relationships": {
                "HAS_BUILD": {
                    "from": "Product",
                    "to": "Build",
                    "condition": "产品 == 产品"
                },
                "INCLUDES": {
                    "from": "Product",
                    "to": "Component",
                    "condition": "产品 == 产品"
                },
                "OBSERVED_IN": {
                    "from": "Anomaly",
                    "to": "Component",
                    "condition": "组件 == 组件"
                },
                "HAS_SYMPTOM": {
                    "from": "Anomaly",
                    "to": "Symptom",
                    "condition": "症状 == 症状"
                }
            },
            "validation": {
                "required_columns": ["产品", "版本", "组件", "症状"],
                "data_types": {
                    "产品": "string",
                    "版本": "string",
                    "组件": "string",
                    "症状": "string"
                }
            }
        }
    
    def _generate_row_hash(self, row: pd.Series) -> str:
        """生成行的哈希值用于重复检测"""
        # 使用主要字段生成哈希
        key_fields = ["产品", "版本", "组件", "症状", "异常描述"]
        key_values = []
        
        for field in key_fields:
            if field in row.index:
                value = str(row[field]) if pd.notna(row[field]) else ""
                key_values.append(value)
        
        key_string = "|".join(key_values)
        return hashlib.md5(key_string.encode('utf-8')).hexdigest()
    
    def _validate_row(self, row: pd.Series, row_index: int) -> Tuple[bool, List[str]]:
        """验证行数据"""
        errors = []
        
        # 检查必需列
        required_columns = self.mapping.get("validation", {}).get("required_columns", [])
        for col in required_columns:
            if col not in row.index or pd.isna(row[col]) or str(row[col]).strip() == "":
                errors.append(f"Missing required field: {col}")
        
        # 检查数据类型
        data_types = self.mapping.get("validation", {}).get("data_types", {})
        for col, expected_type in data_types.items():
            if col in row.index and pd.notna(row[col]):
                value = row[col]
                if expected_type == "string" and not isinstance(value, str):
                    try:
                        str(value)
                    except:
                        errors.append(f"Invalid data type for {col}: expected string")
        
        return len(errors) == 0, errors
    
    def _normalize_value(self, value: Any) -> str:
        """标准化值"""
        if pd.isna(value):
            return ""
        return str(value).strip()
    
    def _extract_entities(self, row: pd.Series) -> List[Dict[str, Any]]:
        """从行中提取实体"""
        entities = []
        
        for entity_type, config in self.mapping.get("entities", {}).items():
            id_field = config.get("id_field")
            name_field = config.get("name_field")
            
            if id_field in row.index and pd.notna(row[id_field]):
                entity_id = self._normalize_value(row[id_field])
                entity_name = self._normalize_value(row[name_field]) if name_field in row.index else entity_id
                
                if entity_id:  # 只有非空ID才创建实体
                    entity = {
                        "type": entity_type,
                        "id": f"{entity_type}:{entity_id}",
                        "name": entity_name,
                        "properties": {}
                    }
                    
                    # 添加属性
                    for prop_name, col_name in config.get("properties", {}).items():
                        if col_name in row.index and pd.notna(row[col_name]):
                            entity["properties"][prop_name] = self._normalize_value(row[col_name])
                    
                    entities.append(entity)
        
        return entities
    
    def _extract_relationships(self, row: pd.Series, entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """从行中提取关系"""
        relationships = []
        entity_map = {entity["type"]: entity["id"] for entity in entities}
        
        for rel_type, config in self.mapping.get("relationships", {}).items():
            from_type = config.get("from")
            to_type = config.get("to")
            
            if from_type in entity_map and to_type in entity_map:
                relationship = {
                    "type": rel_type,
                    "source": entity_map[from_type],
                    "target": entity_map[to_type],
                    "properties": {}
                }
                relationships.append(relationship)
        
        return relationships
    
    def _record_error(self, row_index: int, error_type: str, message: str, row_data: Dict[str, Any] = None):
        """记录错误"""
        error = {
            "row_index": row_index,
            "error_type": error_type,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "row_data": row_data
        }
        self.stats.errors.append(error)
        logger.error(f"Row {row_index}: {error_type} - {message}")
    
    def process_excel(self, file_path: str) -> Dict[str, Any]:
        """处理Excel文件"""
        self.stats = ETLStats()
        self.stats.start_time = datetime.now()
        self.processed_hashes.clear()
        
        try:
            # 读取Excel文件
            logger.info(f"Reading Excel file: {file_path}")
            df = pd.read_excel(file_path)
            self.stats.total_rows = len(df)
            
            logger.info(f"Loaded {self.stats.total_rows} rows from Excel")
            logger.info(f"Columns: {list(df.columns)}")
            
            # 处理每一行
            all_entities = []
            all_relationships = []
            
            for index, row in df.iterrows():
                self.stats.processed_rows += 1
                
                try:
                    # 生成行哈希检查重复
                    row_hash = self._generate_row_hash(row)
                    if row_hash in self.processed_hashes:
                        self.stats.duplicate_rows += 1
                        self.stats.skipped_rows += 1
                        logger.debug(f"Skipping duplicate row {index}")
                        continue
                    
                    self.processed_hashes.add(row_hash)
                    
                    # 验证行数据
                    is_valid, validation_errors = self._validate_row(row, index)
                    if not is_valid:
                        self.stats.failed_rows += 1
                        self._record_error(index, "validation", "; ".join(validation_errors), row.to_dict())
                        continue
                    
                    # 提取实体和关系
                    entities = self._extract_entities(row)
                    relationships = self._extract_relationships(row, entities)
                    
                    all_entities.extend(entities)
                    all_relationships.extend(relationships)
                    
                    self.stats.success_rows += 1
                    
                except Exception as e:
                    self.stats.failed_rows += 1
                    self._record_error(index, "processing", str(e), row.to_dict())
            
            self.stats.end_time = datetime.now()
            
            # 去重实体（基于ID）
            unique_entities = {}
            for entity in all_entities:
                entity_id = entity["id"]
                if entity_id not in unique_entities:
                    unique_entities[entity_id] = entity
                else:
                    # 合并属性
                    unique_entities[entity_id]["properties"].update(entity["properties"])
            
            # 去重关系
            unique_relationships = []
            seen_rels = set()
            for rel in all_relationships:
                rel_key = f"{rel['source']}-{rel['type']}-{rel['target']}"
                if rel_key not in seen_rels:
                    unique_relationships.append(rel)
                    seen_rels.add(rel_key)
            
            result = {
                "entities": list(unique_entities.values()),
                "relationships": unique_relationships,
                "stats": asdict(self.stats),
                "metadata": {
                    "source_file": file_path,
                    "processed_at": datetime.now().isoformat(),
                    "mapping_version": "1.0"
                }
            }
            
            logger.info(f"ETL completed: {self.stats.success_rows}/{self.stats.processed_rows} rows processed successfully")
            logger.info(f"Extracted {len(result['entities'])} entities and {len(result['relationships'])} relationships")
            
            return result
            
        except Exception as e:
            self.stats.end_time = datetime.now()
            logger.error(f"ETL processing failed: {e}")
            self._record_error(-1, "fatal", str(e))
            raise
    
    def save_report(self, result: Dict[str, Any], output_dir: str = "etl_reports"):
        """保存ETL报告"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 保存统计报告
        stats_file = output_path / f"etl_stats_{timestamp}.json"
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(result["stats"], f, ensure_ascii=False, indent=2, default=str)
        
        # 保存错误报告
        if result["stats"]["errors"]:
            errors_file = output_path / f"etl_errors_{timestamp}.json"
            with open(errors_file, 'w', encoding='utf-8') as f:
                json.dump(result["stats"]["errors"], f, ensure_ascii=False, indent=2, default=str)
        
        # 保存提取结果
        data_file = output_path / f"etl_result_{timestamp}.json"
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump({
                "entities": result["entities"],
                "relationships": result["relationships"],
                "metadata": result["metadata"]
            }, f, ensure_ascii=False, indent=2, default=str)
        
        logger.info(f"ETL reports saved to {output_path}")

def main():
    """主函数用于测试"""
    processor = EnhancedETLProcessor()
    
    # 测试文件路径
    test_file = "data/test_data.xlsx"
    
    if Path(test_file).exists():
        result = processor.process_excel(test_file)
        processor.save_report(result)
        
        print(f"ETL Stats:")
        print(f"  Total rows: {result['stats']['total_rows']}")
        print(f"  Success: {result['stats']['success_rows']}")
        print(f"  Failed: {result['stats']['failed_rows']}")
        print(f"  Duplicates: {result['stats']['duplicate_rows']}")
        print(f"  Success rate: {result['stats']['success_rows']/result['stats']['processed_rows']*100:.1f}%")
    else:
        print(f"Test file not found: {test_file}")

if __name__ == "__main__":
    main()
