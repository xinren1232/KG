#!/usr/bin/env python3
"""
API响应模型定义
使用Pydantic v2进行数据验证和序列化
"""

from typing import List, Dict, Any, Optional, Union
from pydantic import BaseModel, Field
from datetime import datetime

class StandardResponse(BaseModel):
    """标准API响应"""
    ok: bool = Field(..., description="请求是否成功")
    data: Optional[Any] = Field(default=None, description="响应数据")
    message: Optional[str] = Field(default=None, description="响应消息")
    timestamp: datetime = Field(default_factory=datetime.now, description="响应时间")

class ErrorResponse(BaseModel):
    """错误响应"""
    ok: bool = Field(default=False, description="请求是否成功")
    error: Dict[str, Any] = Field(..., description="错误信息")
    timestamp: datetime = Field(default_factory=datetime.now, description="响应时间")

class UploadResponse(StandardResponse):
    """文件上传响应"""
    data: Optional[Dict[str, Any]] = Field(
        default=None,
        description="上传结果",
        example={
            "file_id": "file_123456",
            "filename": "example.xlsx",
            "size": 1024000,
            "type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "upload_time": "2024-01-01T12:00:00"
        }
    )

class ExtractResponse(StandardResponse):
    """知识抽取响应"""
    data: Optional[Dict[str, Any]] = Field(
        default=None,
        description="抽取结果",
        example={
            "entities": [
                {
                    "id": "entity_1",
                    "type": "Component",
                    "name": "摄像头",
                    "properties": {"category": "硬件"}
                }
            ],
            "relations": [
                {
                    "id": "relation_1",
                    "type": "HAS_COMPONENT",
                    "source": "product_1",
                    "target": "component_1"
                }
            ],
            "metadata": {
                "extraction_type": "auto",
                "total_entities": 10,
                "total_relations": 5,
                "processing_time": 2.5
            }
        }
    )

class GraphResponse(StandardResponse):
    """图谱构建响应"""
    data: Optional[Dict[str, Any]] = Field(
        default=None,
        description="图谱构建结果",
        example={
            "graph_id": "graph_123",
            "nodes_created": 15,
            "relationships_created": 8,
            "nodes_updated": 2,
            "relationships_updated": 1,
            "merge_strategy": "auto",
            "build_time": 1.2
        }
    )

class StatsResponse(StandardResponse):
    """统计信息响应"""
    data: Optional[Dict[str, Any]] = Field(
        default=None,
        description="统计信息",
        example={
            "total_nodes": 1000,
            "total_relationships": 500,
            "node_types": {
                "Product": 10,
                "Component": 100,
                "Anomaly": 50
            },
            "relationship_types": {
                "HAS_COMPONENT": 80,
                "CAUSES": 30,
                "RESOLVED_BY": 25
            },
            "last_updated": "2024-01-01T12:00:00"
        }
    )

class DictionaryResponse(StandardResponse):
    """词典查询响应"""
    data: Optional[Dict[str, Any]] = Field(
        default=None,
        description="词典数据",
        example={
            "terms": [
                {
                    "term": "摄像头",
                    "canonical_name": "摄像头",
                    "aliases": ["相机", "Camera", "镜头"],
                    "category": "components",
                    "description": "用于拍照和录像的硬件组件"
                }
            ],
            "total_count": 200,
            "categories": ["components", "symptoms", "causes", "countermeasures"]
        }
    )

class CausePathResponse(StandardResponse):
    """因果路径响应"""
    data: Optional[Dict[str, Any]] = Field(
        default=None,
        description="因果路径数据",
        example={
            "paths": [
                {
                    "path_id": "path_1",
                    "symptom": {
                        "id": "symptom_1",
                        "name": "黑屏"
                    },
                    "causes": [
                        {
                            "id": "cause_1",
                            "name": "硬件故障",
                            "confidence": 0.8
                        }
                    ],
                    "countermeasures": [
                        {
                            "id": "counter_1",
                            "name": "更换组件",
                            "effectiveness": 0.9
                        }
                    ],
                    "path_length": 3,
                    "confidence": 0.75
                }
            ],
            "total_paths": 5,
            "max_depth": 5
        }
    )

class AnomaliesResponse(StandardResponse):
    """异常查询响应"""
    data: Optional[Dict[str, Any]] = Field(
        default=None,
        description="异常数据",
        example={
            "anomalies": [
                {
                    "id": "anomaly_1",
                    "product_id": "product_1",
                    "component_id": "component_1",
                    "symptom": "黑屏",
                    "severity": "高",
                    "occurrence_date": "2024-01-01T10:00:00",
                    "status": "已解决"
                }
            ],
            "total_count": 150,
            "page_info": {
                "limit": 100,
                "offset": 0,
                "has_next": True
            }
        }
    )

class GraphQueryResponse(StandardResponse):
    """图查询响应"""
    data: Optional[Dict[str, Any]] = Field(
        default=None,
        description="图查询结果",
        example={
            "nodes": [
                {
                    "id": "node_1",
                    "type": "Component",
                    "properties": {"name": "摄像头"}
                }
            ],
            "relationships": [
                {
                    "id": "rel_1",
                    "type": "HAS_COMPONENT",
                    "source": "product_1",
                    "target": "component_1"
                }
            ],
            "query_info": {
                "query_type": "neighbors",
                "execution_time": 0.5,
                "result_count": 10
            }
        }
    )

class ETLResponse(StandardResponse):
    """ETL处理响应"""
    data: Optional[Dict[str, Any]] = Field(
        default=None,
        description="ETL处理结果",
        example={
            "job_id": "etl_job_123",
            "status": "completed",
            "file_path": "/data/input.xlsx",
            "total_rows": 1000,
            "processed_rows": 950,
            "success_rows": 900,
            "failed_rows": 50,
            "skipped_rows": 50,
            "duplicate_rows": 25,
            "success_rate": 0.95,
            "processing_time": 30.5,
            "errors": [
                {
                    "row_index": 10,
                    "error_type": "validation_error",
                    "message": "缺少必需字段"
                }
            ]
        }
    )

class HealthResponse(StandardResponse):
    """健康检查响应"""
    data: Optional[Dict[str, Any]] = Field(
        default=None,
        description="健康状态",
        example={
            "status": "healthy",
            "version": "2.0.0",
            "uptime": 3600,
            "database": {
                "status": "connected",
                "response_time": 0.05
            },
            "memory_usage": {
                "used": "256MB",
                "total": "1GB",
                "percentage": 25.6
            },
            "disk_usage": {
                "used": "10GB",
                "total": "100GB",
                "percentage": 10.0
            }
        }
    )

# 联合响应类型
APIResponse = Union[
    StandardResponse,
    ErrorResponse,
    UploadResponse,
    ExtractResponse,
    GraphResponse,
    StatsResponse,
    DictionaryResponse,
    CausePathResponse,
    AnomaliesResponse,
    GraphQueryResponse,
    ETLResponse,
    HealthResponse
]
