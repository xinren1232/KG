#!/usr/bin/env python3
"""
API请求模型定义
使用Pydantic v2进行数据验证和序列化
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, validator
from datetime import datetime

class ExtractRequest(BaseModel):
    """知识抽取请求"""
    file_id: str = Field(..., description="文件ID", min_length=1)
    extraction_type: str = Field(default="auto", description="抽取类型")
    
    @validator('extraction_type')
    def validate_extraction_type(cls, v):
        allowed_types = ['auto', 'manual', 'hybrid']
        if v not in allowed_types:
            raise ValueError(f'extraction_type must be one of {allowed_types}')
        return v

class BuildGraphRequest(BaseModel):
    """构建图谱请求"""
    entities: List[Dict[str, Any]] = Field(..., description="实体列表")
    relations: List[Dict[str, Any]] = Field(..., description="关系列表")
    merge_strategy: str = Field(default="auto", description="合并策略")
    
    @validator('merge_strategy')
    def validate_merge_strategy(cls, v):
        allowed_strategies = ['auto', 'replace', 'merge', 'skip']
        if v not in allowed_strategies:
            raise ValueError(f'merge_strategy must be one of {allowed_strategies}')
        return v

class UpsertRequest(BaseModel):
    """数据插入/更新请求"""
    entity_type: str = Field(..., description="实体类型")
    entity_data: Dict[str, Any] = Field(..., description="实体数据")
    relations: Optional[List[Dict[str, Any]]] = Field(default=None, description="关系数据")
    
    @validator('entity_type')
    def validate_entity_type(cls, v):
        allowed_types = [
            'Product', 'Build', 'Component', 'TestCase', 'TestStep',
            'TestResult', 'Anomaly', 'Symptom', 'RootCause', 'Countermeasure'
        ]
        if v not in allowed_types:
            raise ValueError(f'entity_type must be one of {allowed_types}')
        return v

class CausePathRequest(BaseModel):
    """因果路径查询请求"""
    symptom_id: Optional[str] = Field(default=None, description="症状ID")
    symptom_name: Optional[str] = Field(default=None, description="症状名称")
    max_depth: int = Field(default=5, description="最大查询深度", ge=1, le=10)
    include_countermeasures: bool = Field(default=True, description="是否包含对策")
    
    @validator('symptom_id', 'symptom_name')
    def validate_symptom_input(cls, v, values):
        # 至少需要提供symptom_id或symptom_name之一
        if not v and not values.get('symptom_id') and not values.get('symptom_name'):
            raise ValueError('Must provide either symptom_id or symptom_name')
        return v

class AnomaliesRequest(BaseModel):
    """异常查询请求"""
    product_id: Optional[str] = Field(default=None, description="产品ID")
    component_id: Optional[str] = Field(default=None, description="组件ID")
    severity: Optional[str] = Field(default=None, description="严重程度")
    start_date: Optional[datetime] = Field(default=None, description="开始日期")
    end_date: Optional[datetime] = Field(default=None, description="结束日期")
    limit: int = Field(default=100, description="返回数量限制", ge=1, le=1000)
    offset: int = Field(default=0, description="偏移量", ge=0)
    
    @validator('severity')
    def validate_severity(cls, v):
        if v is not None:
            allowed_severities = ['低', '中', '高', '严重', 'Low', 'Medium', 'High', 'Critical']
            if v not in allowed_severities:
                raise ValueError(f'severity must be one of {allowed_severities}')
        return v
    
    @validator('end_date')
    def validate_date_range(cls, v, values):
        start_date = values.get('start_date')
        if start_date and v and v < start_date:
            raise ValueError('end_date must be after start_date')
        return v

class DictionaryRequest(BaseModel):
    """词典查询请求"""
    category: Optional[str] = Field(default=None, description="词典分类")
    search_term: Optional[str] = Field(default=None, description="搜索词条")
    include_aliases: bool = Field(default=True, description="是否包含别名")
    limit: int = Field(default=100, description="返回数量限制", ge=1, le=1000)
    
    @validator('category')
    def validate_category(cls, v):
        if v is not None:
            allowed_categories = ['components', 'symptoms', 'causes', 'countermeasures']
            if v not in allowed_categories:
                raise ValueError(f'category must be one of {allowed_categories}')
        return v

class DictionaryUpdateRequest(BaseModel):
    """词典更新请求"""
    term: str = Field(..., description="词条", min_length=1)
    canonical_name: str = Field(..., description="标准名称", min_length=1)
    aliases: Optional[List[str]] = Field(default=None, description="别名列表")
    category: str = Field(..., description="分类")
    description: Optional[str] = Field(default=None, description="描述")
    
    @validator('category')
    def validate_category(cls, v):
        allowed_categories = ['components', 'symptoms', 'causes', 'countermeasures']
        if v not in allowed_categories:
            raise ValueError(f'category must be one of {allowed_categories}')
        return v

class GraphQueryRequest(BaseModel):
    """图查询请求"""
    query_type: str = Field(..., description="查询类型")
    parameters: Dict[str, Any] = Field(default={}, description="查询参数")
    limit: int = Field(default=100, description="返回数量限制", ge=1, le=1000)
    
    @validator('query_type')
    def validate_query_type(cls, v):
        allowed_types = [
            'neighbors', 'path', 'subgraph', 'statistics',
            'centrality', 'community', 'similarity'
        ]
        if v not in allowed_types:
            raise ValueError(f'query_type must be one of {allowed_types}')
        return v

class ETLRequest(BaseModel):
    """ETL处理请求"""
    file_path: str = Field(..., description="文件路径", min_length=1)
    file_type: str = Field(default="excel", description="文件类型")
    mapping_config: Optional[Dict[str, Any]] = Field(default=None, description="映射配置")
    batch_size: int = Field(default=1000, description="批处理大小", ge=1, le=10000)
    enable_validation: bool = Field(default=True, description="启用数据验证")
    enable_deduplication: bool = Field(default=True, description="启用去重")
    dry_run: bool = Field(default=False, description="干运行模式")
    
    @validator('file_type')
    def validate_file_type(cls, v):
        allowed_types = ['excel', 'csv', 'json', 'xml']
        if v not in allowed_types:
            raise ValueError(f'file_type must be one of {allowed_types}')
        return v
