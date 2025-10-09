#!/usr/bin/env python3
"""
Excel文件解析器
"""

import pandas as pd
import yaml
import hashlib
import logging
from pathlib import Path
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

def parse_excel(file_path: Path, mapping_yaml: Path = None) -> List[Dict[str, Any]]:
    """
    解析Excel文件
    
    Args:
        file_path: Excel文件路径
        mapping_yaml: 映射配置文件路径
        
    Returns:
        解析后的数据列表
    """
    logger.info(f"开始解析Excel文件: {file_path}")
    
    try:
        # 加载映射配置
        if mapping_yaml and mapping_yaml.exists():
            mapping = yaml.safe_load(mapping_yaml.read_text(encoding="utf-8"))
            logger.info(f"使用映射配置: {mapping_yaml}")
        else:
            # 默认映射配置
            mapping = {
                "sheet": 0,  # 第一个sheet
                "columns": {
                    "anomaly_key": "问题编号",
                    "title": "不良现象", 
                    "date": "发生日期",
                    "severity": "严重度",
                    "factory": "工厂",
                    "product": "机型",
                    "build": "版本",
                    "component": "部件",
                    "symptom": "不良现象",
                    "root_cause": "原因分析",
                    "countermeasure": "改善对策"
                }
            }
            logger.info("使用默认映射配置")
        
        # 读取Excel文件
        sheet_name = mapping.get("sheet", 0)
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        logger.info(f"读取Excel成功，行数: {len(df)}, 列数: {len(df.columns)}")
        logger.info(f"列名: {list(df.columns)}")
        
        # 列映射
        columns_mapping = mapping.get("columns", {})
        
        def safe_get_column(col_name: str):
            """安全获取列数据，支持模糊匹配"""
            if col_name in df.columns:
                return df[col_name]
            
            # 模糊匹配：去除空格、转小写
            candidates = {c.replace(" ", "").lower(): c for c in df.columns}
            key = col_name.replace(" ", "").lower()
            
            if key in candidates:
                actual_col = candidates[key]
                logger.info(f"列名模糊匹配: '{col_name}' -> '{actual_col}'")
                return df[actual_col]
            
            logger.warning(f"未找到列: {col_name}")
            return None
        
        # 解析数据
        items = []
        for i, row in df.iterrows():
            record = {}
            
            # 映射各列数据
            for key, col_name in columns_mapping.items():
                series = safe_get_column(col_name)
                if series is not None:
                    value = series.iloc[i]
                    # 处理NaN值
                    if pd.isna(value):
                        record[key] = None
                    else:
                        # 特殊处理时间戳对象
                        if hasattr(value, 'isoformat'):
                            # 如果是时间戳对象，转换为ISO格式字符串
                            record[key] = value.isoformat()
                        else:
                            record[key] = str(value).strip()
                else:
                    record[key] = None
            
            # 生成异常键（如果没有的话）
            if not record.get("anomaly_key"):
                base_text = (record.get("title") or "") + \
                           (record.get("product") or "") + \
                           (record.get("date") or "")
                record["anomaly_key"] = "ANOM-" + hashlib.md5(
                    base_text.encode("utf-8")
                ).hexdigest()[:10]
            
            # 添加行号
            record["row_number"] = i + 2  # Excel行号从2开始（第1行是表头）
            
            items.append(record)
        
        logger.info(f"Excel解析完成，共解析 {len(items)} 条记录")
        return items
        
    except Exception as e:
        logger.error(f"Excel解析失败: {e}")
        raise

def detect_excel_structure(file_path: Path) -> Dict[str, Any]:
    """
    检测Excel文件结构
    
    Returns:
        文件结构信息
    """
    try:
        # 读取所有sheet
        excel_file = pd.ExcelFile(file_path)
        sheets_info = []
        
        for sheet_name in excel_file.sheet_names:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            sheets_info.append({
                "name": sheet_name,
                "rows": len(df),
                "columns": len(df.columns),
                "column_names": list(df.columns)
            })
        
        return {
            "file_type": "excel",
            "sheets": sheets_info,
            "total_sheets": len(sheets_info)
        }
        
    except Exception as e:
        logger.error(f"检测Excel结构失败: {e}")
        return {"error": str(e)}

def suggest_mapping(file_path: Path) -> Dict[str, str]:
    """
    根据Excel列名建议映射配置
    
    Returns:
        建议的列映射
    """
    try:
        df = pd.read_excel(file_path, sheet_name=0)
        columns = [col.strip() for col in df.columns]
        
        # 常见列名映射
        suggestions = {}
        
        # 映射规则
        mapping_rules = {
            "anomaly_key": ["问题编号", "编号", "ID", "id", "序号"],
            "title": ["标题", "问题", "不良现象", "现象", "描述"],
            "date": ["日期", "时间", "发生日期", "创建日期"],
            "severity": ["严重度", "等级", "级别", "优先级"],
            "factory": ["工厂", "厂区", "生产线"],
            "product": ["产品", "机型", "型号", "产品型号"],
            "component": ["部件", "组件", "零件", "器件"],
            "symptom": ["症状", "现象", "不良现象", "问题现象"],
            "root_cause": ["原因", "根因", "原因分析", "根本原因"],
            "countermeasure": ["对策", "措施", "改善对策", "解决方案"]
        }
        
        for key, candidates in mapping_rules.items():
            for col in columns:
                for candidate in candidates:
                    if candidate in col:
                        suggestions[key] = col
                        break
                if key in suggestions:
                    break
        
        logger.info(f"建议的列映射: {suggestions}")
        return suggestions
        
    except Exception as e:
        logger.error(f"生成映射建议失败: {e}")
        return {}
