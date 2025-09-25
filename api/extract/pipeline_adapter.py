#!/usr/bin/env python3
"""
知识抽取管道适配器
复用现有的抽取逻辑，适配新的文档解析流程
"""

import logging
from typing import List, Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)

def excel_items_to_preview(items: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    将Excel解析结果转换为预览格式
    
    Args:
        items: Excel解析的记录列表
        
    Returns:
        预览数据格式
    """
    logger.info(f"开始转换Excel数据，共 {len(items)} 条记录")
    
    entities = []
    relations = []
    
    # 实体类型映射
    entity_types = {
        "component": "Component",
        "symptom": "Symptom", 
        "root_cause": "RootCause",
        "countermeasure": "Countermeasure",
        "product": "Product",
        "factory": "Factory"
    }
    
    # 收集所有实体
    entity_set = set()
    
    for record in items:
        # 提取各类实体
        for field, entity_type in entity_types.items():
            value = record.get(field)
            if value and value.strip():
                entity_key = (entity_type, value.strip())
                if entity_key not in entity_set:
                    entity_set.add(entity_key)
                    entities.append({
                        "id": f"{entity_type.lower()}_{len(entities)}",
                        "name": value.strip(),
                        "type": entity_type,
                        "properties": {
                            "source": "excel",
                            "anomaly_key": record.get("anomaly_key", "")
                        }
                    })
        
        # 构建关系
        anomaly_key = record.get("anomaly_key", "")
        
        # 症状 -> 根因
        if record.get("symptom") and record.get("root_cause"):
            relations.append({
                "source": record["symptom"],
                "target": record["root_cause"],
                "type": "HAS_ROOTCAUSE",
                "properties": {
                    "anomaly_key": anomaly_key,
                    "confidence": 1.0
                }
            })
        
        # 根因 -> 对策
        if record.get("root_cause") and record.get("countermeasure"):
            relations.append({
                "source": record["root_cause"],
                "target": record["countermeasure"],
                "type": "RESOLVED_BY",
                "properties": {
                    "anomaly_key": anomaly_key,
                    "confidence": 1.0
                }
            })
        
        # 症状 -> 部件
        if record.get("symptom") and record.get("component"):
            relations.append({
                "source": record["symptom"],
                "target": record["component"],
                "type": "AFFECTS",
                "properties": {
                    "anomaly_key": anomaly_key,
                    "confidence": 0.9
                }
            })
        
        # 产品 -> 部件
        if record.get("product") and record.get("component"):
            relations.append({
                "source": record["product"],
                "target": record["component"],
                "type": "CONTAINS",
                "properties": {
                    "anomaly_key": anomaly_key,
                    "confidence": 0.8
                }
            })
    
    # 去重关系
    unique_relations = []
    relation_set = set()
    
    for rel in relations:
        rel_key = (rel["source"], rel["target"], rel["type"])
        if rel_key not in relation_set:
            relation_set.add(rel_key)
            unique_relations.append(rel)
    
    result = {
        "raw_data": items,  # 添加原始数据
        "entities": entities,
        "relations": unique_relations,
        "metadata": {
            "total_records": len(items),
            "entity_count": len(entities),
            "relation_count": len(unique_relations),
            "field_count": len(items[0].keys()) if items else 0,
            "entity_types": {etype: len([e for e in entities if e["type"] == etype])
                           for etype in entity_types.values()},
            "source": "excel_structured"
        }
    }
    
    logger.info(f"Excel数据转换完成: {len(entities)} 实体, {len(unique_relations)} 关系")
    return result

def text_blocks_to_preview(blocks: List[str], file_type: str = "text") -> Dict[str, Any]:
    """
    将文本块转换为预览格式（使用词典匹配）
    
    Args:
        blocks: 文本块列表
        file_type: 文件类型
        
    Returns:
        预览数据格式
    """
    logger.info(f"开始处理文本块，共 {len(blocks)} 个块")
    
    try:
        # 简化的文本实体识别（基于关键词匹配）
        all_entities = []
        all_relations = []

        # 定义关键词映射
        keyword_mapping = {
            "Component": ["摄像头", "显示屏", "充电器", "电池", "扬声器", "麦克风", "传感器", "按键"],
            "Symptom": ["对焦失败", "屏幕闪烁", "充电慢", "发热", "死机", "卡顿", "黑屏", "白屏"],
            "RootCause": ["驱动IC异常", "镜头污染", "功率不足", "电池老化", "软件bug"],
            "Countermeasure": ["清洁镜头", "更换驱动IC", "升级充电器", "更新软件", "重启设备"]
        }

        # 对每个文本块进行实体识别
        for i, block in enumerate(blocks):
            if not block.strip():
                continue

            # 简单的关键词匹配
            for entity_type, keywords in keyword_mapping.items():
                for keyword in keywords:
                    if keyword in block:
                        entity = {
                            "id": f"{entity_type.lower()}_{len(all_entities)}",
                            "name": keyword,
                            "type": entity_type,
                            "properties": {
                                "block_index": i,
                                "source_text": block[:100],
                                "confidence": 0.8
                            }
                        }
                        all_entities.append(entity)
        
        # 简单的关系推断（基于共现）
        # 在同一文本块中出现的实体可能有关系
        block_entities = {}
        for entity in all_entities:
            block_idx = entity["properties"]["block_index"]
            if block_idx not in block_entities:
                block_entities[block_idx] = []
            block_entities[block_idx].append(entity)
        
        # 生成关系
        for block_idx, entities in block_entities.items():
            if len(entities) >= 2:
                # 症状和部件的关系
                symptoms = [e for e in entities if e["type"] == "Symptom"]
                components = [e for e in entities if e["type"] == "Component"]
                
                for symptom in symptoms:
                    for component in components:
                        all_relations.append({
                            "source": symptom["name"],
                            "target": component["name"],
                            "type": "AFFECTS",
                            "properties": {
                                "block_index": block_idx,
                                "confidence": 0.7,
                                "source": "co_occurrence"
                            }
                        })
        
        # 去重实体
        unique_entities = []
        entity_set = set()
        
        for entity in all_entities:
            entity_key = (entity["type"], entity["name"])
            if entity_key not in entity_set:
                entity_set.add(entity_key)
                unique_entities.append(entity)
        
        result = {
            "entities": unique_entities,
            "relations": all_relations,
            "metadata": {
                "total_blocks": len(blocks),
                "processed_blocks": len([b for b in blocks if b.strip()]),
                "entity_count": len(unique_entities),
                "relation_count": len(all_relations),
                "file_type": file_type,
                "source": "text_dictionary_matching"
            }
        }
        
        logger.info(f"文本处理完成: {len(unique_entities)} 实体, {len(all_relations)} 关系")
        return result
        
    except ImportError:
        logger.warning("词典服务不可用，返回基础文本统计")
        return {
            "entities": [],
            "relations": [],
            "metadata": {
                "total_blocks": len(blocks),
                "processed_blocks": len([b for b in blocks if b.strip()]),
                "entity_count": 0,
                "relation_count": 0,
                "file_type": file_type,
                "source": "text_basic",
                "warning": "词典服务不可用，无法进行实体抽取"
            }
        }
    except Exception as e:
        logger.error(f"文本处理失败: {e}")
        return {
            "entities": [],
            "relations": [],
            "metadata": {
                "total_blocks": len(blocks),
                "error": str(e),
                "file_type": file_type,
                "source": "text_error"
            }
        }
