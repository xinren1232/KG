#!/usr/bin/env python3
"""
增强的Excel解析器
使用多种解析库确保最佳解析效果
"""

import pandas as pd
import openpyxl
import yaml
import logging
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class EnhancedExcelParser:
    """增强的Excel解析器"""
    
    def __init__(self):
        self.supported_engines = ['openpyxl', 'xlrd', 'calamine']
        
    def parse_excel_robust(self, file_path: Path, mapping_yaml: Path = None) -> List[Dict[str, Any]]:
        """
        使用多种方法解析Excel文件，确保最佳效果
        
        Args:
            file_path: Excel文件路径
            mapping_yaml: 映射配置文件路径
            
        Returns:
            解析后的数据列表
        """
        logger.info(f"开始增强解析Excel文件: {file_path}")
        
        # 尝试多种解析引擎
        for engine in self.supported_engines:
            try:
                logger.info(f"尝试使用引擎: {engine}")
                df = self._read_excel_with_engine(file_path, engine)
                if df is not None and not df.empty:
                    logger.info(f"成功使用引擎 {engine} 读取Excel")
                    break
            except Exception as e:
                logger.warning(f"引擎 {engine} 失败: {e}")
                continue
        else:
            raise Exception("所有解析引擎都失败了")
        
        # 加载映射配置
        mapping = self._load_mapping_config(mapping_yaml)
        
        # 智能列名匹配
        column_mapping = self._smart_column_mapping(df.columns, mapping)
        
        # 解析数据
        items = self._parse_dataframe(df, column_mapping)
        
        logger.info(f"Excel解析完成，共解析 {len(items)} 条记录")
        return items
    
    def _read_excel_with_engine(self, file_path: Path, engine: str) -> Optional[pd.DataFrame]:
        """使用指定引擎读取Excel"""
        try:
            if engine == 'openpyxl':
                # 使用openpyxl引擎
                df = pd.read_excel(file_path, engine='openpyxl', sheet_name=0)
            elif engine == 'xlrd':
                # 使用xlrd引擎
                df = pd.read_excel(file_path, engine='xlrd', sheet_name=0)
            elif engine == 'calamine':
                # 使用calamine引擎（如果可用）
                df = pd.read_excel(file_path, engine='calamine', sheet_name=0)
            else:
                # 默认引擎
                df = pd.read_excel(file_path, sheet_name=0)
            
            logger.info(f"使用 {engine} 成功读取: {df.shape[0]} 行 x {df.shape[1]} 列")
            logger.info(f"列名: {list(df.columns)}")
            
            return df
            
        except Exception as e:
            logger.error(f"引擎 {engine} 读取失败: {e}")
            return None
    
    def _load_mapping_config(self, mapping_yaml: Path = None) -> Dict[str, Any]:
        """加载映射配置"""
        # 优先级：指定配置 > 优化配置 > 默认配置
        config_files = []
        
        if mapping_yaml and mapping_yaml.exists():
            config_files.append(mapping_yaml)
        
        config_files.extend([
            Path("api/mappings/mapping_excel_comprehensive.yaml"),
            Path("api/mappings/mapping_excel_default.yaml")
        ])
        
        for config_file in config_files:
            if config_file.exists():
                try:
                    with open(config_file, 'r', encoding='utf-8') as f:
                        mapping = yaml.safe_load(f)
                    logger.info(f"使用映射配置: {config_file}")
                    return mapping
                except Exception as e:
                    logger.warning(f"配置文件 {config_file} 加载失败: {e}")
        
        # 如果所有配置都失败，使用内置默认配置
        logger.warning("使用内置默认映射配置")
        return self._get_default_mapping()
    
    def _get_default_mapping(self) -> Dict[str, Any]:
        """获取内置默认映射配置"""
        return {
            "sheet": 0,
            "columns": {
                "anomaly_key": "问题编号",
                "title": "不良现象",
                "date": "发生日期",
                "severity": "严重度",
                "factory": "工厂",
                "product": "机型",
                "component": "部件",
                "symptom": "不良现象",
                "root_cause": "原因分析",
                "countermeasure": "改善对策",
                "supplier": "供应商",
                "status": "状态"
            }
        }
    
    def _smart_column_mapping(self, df_columns: List[str], mapping: Dict[str, Any]) -> Dict[str, str]:
        """智能列名映射"""
        columns_mapping = mapping.get("columns", {})
        result_mapping = {}
        
        # 清理列名
        clean_columns = [str(col).strip() for col in df_columns]
        
        logger.info(f"原始列名: {clean_columns}")
        
        for key, target_col in columns_mapping.items():
            matched_col = self._find_matching_column(target_col, clean_columns)
            if matched_col:
                result_mapping[key] = matched_col
                logger.info(f"映射成功: {key} -> {matched_col}")
            else:
                logger.warning(f"未找到匹配列: {key} -> {target_col}")
        
        return result_mapping
    
    def _find_matching_column(self, target: str, columns: List[str]) -> Optional[str]:
        """查找匹配的列名"""
        # 1. 精确匹配
        if target in columns:
            return target
        
        # 2. 去除空格匹配
        target_clean = target.replace(" ", "").lower()
        for col in columns:
            if col.replace(" ", "").lower() == target_clean:
                return col
        
        # 3. 包含匹配
        for col in columns:
            if target in col or col in target:
                return col
        
        # 4. 模糊匹配（关键词）
        target_keywords = target.split()
        for col in columns:
            for keyword in target_keywords:
                if keyword in col:
                    return col
        
        return None
    
    def _parse_dataframe(self, df: pd.DataFrame, column_mapping: Dict[str, str]) -> List[Dict[str, Any]]:
        """解析DataFrame为记录列表，只保留原始列名，避免重复"""
        items = []

        for i, row in df.iterrows():
            record = {}

            # 首先添加行号（系统字段，放在最前面）
            record["_row_number"] = i + 2  # Excel行号从2开始（第1行是表头）

            # 然后添加原始Excel列（使用原始列名作为键）
            for col_name in df.columns:
                value = row[col_name]
                # 处理NaN值
                if pd.isna(value):
                    record[col_name] = None
                else:
                    # 特殊处理时间戳对象
                    if hasattr(value, 'isoformat'):
                        # 如果是时间戳对象，转换为ISO格式字符串
                        record[col_name] = value.isoformat()
                    else:
                        record[col_name] = str(value).strip()

            # 只添加必要的系统字段，不重复业务数据
            # 确保有问题编号字段（如果原始数据中没有合适的标识）
            anomaly_key = None
            for col_name in df.columns:
                if any(keyword in col_name for keyword in ['编号', '问题', 'ID', 'id', 'key']):
                    anomaly_key = record[col_name]
                    break

            if not anomaly_key or str(anomaly_key).strip() in [None, "", "nan", "None"]:
                # 只有在没有找到合适的问题编号时才生成
                record["_generated_id"] = f"ISSUE-{i+1:03d}"
                logger.info(f"为第 {i+1} 行生成问题编号: {record['_generated_id']}")

            # 数据质量检查 - 检查原始列是否有数据
            if self._is_valid_record_with_original_columns(record, df.columns):
                items.append(record)
            else:
                logger.warning(f"跳过无效记录: 行 {i+2}")

        return items
    
    def _is_valid_record(self, record: Dict[str, Any]) -> bool:
        """检查记录是否有效"""
        # 至少要有一个非空的关键字段
        key_fields = ["title", "symptom", "component", "root_cause"]
        return any(record.get(field) and str(record[field]).strip() for field in key_fields)

    def _is_valid_record_with_original_columns(self, record: Dict[str, Any], original_columns: list) -> bool:
        """检查记录是否有效（基于原始列）"""
        # 检查原始列是否有数据
        for col in original_columns:
            if record.get(col) and str(record[col]).strip() and str(record[col]).strip() not in ['nan', 'None']:
                return True

        # 如果原始列都没有数据，检查映射字段
        key_fields = ["title", "symptom", "component", "root_cause", "anomaly_key"]
        return any(record.get(field) and str(record[field]).strip() for field in key_fields)

# 兼容性函数
def parse_excel(file_path: Path, mapping_yaml: Path = None) -> List[Dict[str, Any]]:
    """
    兼容性函数，使用增强解析器
    """
    parser = EnhancedExcelParser()
    return parser.parse_excel_robust(file_path, mapping_yaml)

def parse_excel_robust(file_path: Path, mapping_yaml: Path = None) -> Dict[str, Any]:
    """
    增强的Excel解析函数，返回完整的解析结果
    """
    parser = EnhancedExcelParser()

    try:
        # 使用全面映射配置
        if mapping_yaml is None:
            mapping_yaml = Path("api/mappings/mapping_excel_comprehensive.yaml")

        raw_data = parser.parse_excel_robust(file_path, mapping_yaml)

        # 构建完整的返回结果
        result = {
            'success': True,
            'data': {
                'raw_data': raw_data,
                'entities': [],
                'relations': []
            },
            'stats': {
                'total_records': len(raw_data),
                'total_fields': len(raw_data[0].keys()) if raw_data else 0,
                'data_quality': 1.0 if raw_data else 0.0
            }
        }

        # 简单的实体抽取
        entities = []
        relations = []

        for i, record in enumerate(raw_data):
            # 为每个记录创建实体
            for field, value in record.items():
                if value and str(value).strip():
                    entities.append({
                        'id': f"{field}_{i}",
                        'type': field,
                        'value': str(value),
                        'source_record': i
                    })

        # 创建简单的关系
        for i, record in enumerate(raw_data):
            if 'anomaly_key' in record and 'root_cause' in record:
                relations.append({
                    'source': f"anomaly_key_{i}",
                    'target': f"root_cause_{i}",
                    'type': 'HAS_CAUSE',
                    'confidence': 1.0
                })

        result['data']['entities'] = entities
        result['data']['relations'] = relations

        return result

    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'data': None
        }

def detect_excel_structure(file_path: Path) -> Dict[str, Any]:
    """
    检测Excel文件结构
    """
    try:
        # 尝试多种引擎
        df = None
        for engine in ['openpyxl', 'xlrd', None]:
            try:
                if engine:
                    df = pd.read_excel(file_path, engine=engine, sheet_name=0)
                else:
                    df = pd.read_excel(file_path, sheet_name=0)
                break
            except:
                continue
        
        if df is None:
            raise Exception("无法读取Excel文件")
        
        return {
            "file_type": "excel",
            "sheets": [{
                "name": "Sheet1",
                "rows": len(df),
                "columns": len(df.columns),
                "column_names": list(df.columns)
            }],
            "total_sheets": 1,
            "sample_data": df.head(3).to_dict('records') if len(df) > 0 else []
        }
        
    except Exception as e:
        logger.error(f"检测Excel结构失败: {e}")
        return {"error": str(e)}

def suggest_mapping(file_path: Path) -> Dict[str, str]:
    """
    根据Excel列名建议映射配置
    """
    try:
        parser = EnhancedExcelParser()
        
        # 尝试读取文件
        df = None
        for engine in ['openpyxl', 'xlrd', None]:
            try:
                if engine:
                    df = pd.read_excel(file_path, engine=engine, sheet_name=0)
                else:
                    df = pd.read_excel(file_path, sheet_name=0)
                break
            except:
                continue
        
        if df is None:
            return {}
        
        columns = [str(col).strip() for col in df.columns]
        
        # 使用智能映射
        default_mapping = parser._get_default_mapping()
        suggestions = {}
        
        for key, target_col in default_mapping["columns"].items():
            matched_col = parser._find_matching_column(target_col, columns)
            if matched_col:
                suggestions[key] = matched_col
        
        logger.info(f"建议的列映射: {suggestions}")
        return suggestions
        
    except Exception as e:
        logger.error(f"生成映射建议失败: {e}")
        return {}
