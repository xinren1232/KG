from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

# 基础响应模型
class BaseResponse(BaseModel):
    success: bool = True
    message: str = "操作成功"
    data: Optional[Any] = None

# 健康检查响应
class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    version: str
    database: str

# 节点模型
class NodeModel(BaseModel):
    id: str
    labels: List[str]
    properties: Dict[str, Any]

# 关系模型
class RelationshipModel(BaseModel):
    id: str
    type: str
    start_node: str
    end_node: str
    properties: Dict[str, Any]

# 图谱数据模型
class GraphData(BaseModel):
    nodes: List[NodeModel]
    relationships: List[RelationshipModel]

# 查询请求模型
class QueryRequest(BaseModel):
    query: str
    parameters: Optional[Dict[str, Any]] = None

# 查询响应模型
class QueryResponse(BaseModel):
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    execution_time: Optional[float] = None

# 文档上传模型
class DocumentUpload(BaseModel):
    filename: str
    content_type: str
    size: int

# 解析结果模型
class ParseResult(BaseModel):
    document_id: str
    entities: List[Dict[str, Any]]
    relationships: List[Dict[str, Any]]
    metadata: Dict[str, Any]

# 统计信息模型
class GraphStats(BaseModel):
    node_count: int
    relationship_count: int
    node_types: Dict[str, int]
    relationship_types: Dict[str, int]

# 搜索请求模型
class SearchRequest(BaseModel):
    keyword: str
    node_types: Optional[List[str]] = None
    limit: int = 10

# 搜索结果模型
class SearchResult(BaseModel):
    nodes: List[NodeModel]
    total: int
    query_time: float

# 推荐请求模型
class RecommendRequest(BaseModel):
    node_id: str
    relationship_types: Optional[List[str]] = None
    limit: int = 5

# 推荐结果模型
class RecommendResult(BaseModel):
    recommendations: List[NodeModel]
    scores: List[float]
    total: int

# 流程查询请求模型
class FlowQueryRequest(BaseModel):
    product_name: str
    component_name: Optional[str] = None
    test_type: Optional[str] = None

# 流程查询响应模型
class FlowQueryResponse(BaseModel):
    success: bool
    data: Optional[List[Dict[str, Any]]] = None
    message: str = "查询成功"

# 原因路径查询请求模型
class CausePathQueryRequest(BaseModel):
    anomaly_id: str
    max_depth: int = 3

# 原因路径响应模型
class CausePath(BaseModel):
    path: List[Dict[str, Any]]
    confidence: float

class CausePathResponse(BaseModel):
    success: bool
    paths: List[CausePath]
    message: str = "查询成功"

# 异常数据上传请求模型
class AnomalyUpsertRequest(BaseModel):
    product_name: str
    component_name: str
    anomaly_type: str
    description: str
    severity: str
    metadata: Optional[Dict[str, Any]] = None

# 通用API响应模型
class ApiResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None

# 产品模型
class Product(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    properties: Dict[str, Any]

# 组件模型
class Component(BaseModel):
    id: str
    name: str
    product_id: str
    description: Optional[str] = None
    properties: Dict[str, Any]

# 测试用例模型
class TestCase(BaseModel):
    id: str
    name: str
    component_id: str
    test_type: str
    description: Optional[str] = None
    properties: Dict[str, Any]

# 产品列表响应模型
class ProductListResponse(BaseModel):
    success: bool
    products: List[Product]
    total: int

# 组件列表响应模型
class ComponentListResponse(BaseModel):
    success: bool
    components: List[Component]
    total: int

# 图谱数据响应模型
class GraphDataResponse(BaseModel):
    success: bool
    nodes: List[NodeModel]
    relationships: List[RelationshipModel]
    stats: Optional[GraphStats] = None
