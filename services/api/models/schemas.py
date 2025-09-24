from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class SeverityLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class AnomalyStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"

class TestCasePriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

# 请求模型
class FlowQueryRequest(BaseModel):
    product_name: str = Field(..., description="产品名称")
    component_name: Optional[str] = Field(None, description="组件名称")

class CausePathQueryRequest(BaseModel):
    symptom_description: str = Field(..., description="症状描述")

class AnomalyUpsertRequest(BaseModel):
    anomaly_id: str = Field(..., description="异常ID")
    title: str = Field(..., description="异常标题")
    description: str = Field(..., description="异常描述")
    severity: SeverityLevel = Field(..., description="严重程度")
    status: AnomalyStatus = Field(default=AnomalyStatus.OPEN, description="状态")
    created_date: Optional[str] = Field(None, description="创建日期")
    reporter: Optional[str] = Field(None, description="报告人")

# 响应模型
class Product(BaseModel):
    name: str
    model: Optional[str] = None
    category: Optional[str] = None
    release_date: Optional[str] = None
    status: Optional[str] = None

class Component(BaseModel):
    name: str
    type: Optional[str] = None
    version: Optional[str] = None
    supplier: Optional[str] = None
    criticality: Optional[str] = None

class TestCase(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    priority: Optional[str] = None
    type: Optional[str] = None
    steps: Optional[List[str]] = None
    expected_result: Optional[str] = None

class CausePath(BaseModel):
    anomaly_id: str
    anomaly_title: str
    anomaly_description: Optional[str] = None
    severity: str
    status: str
    symptom: str
    root_cause: Optional[str] = None
    countermeasure: Optional[str] = None
    countermeasure_steps: Optional[List[str]] = None
    component: Optional[str] = None

class GraphNode(BaseModel):
    id: int
    label: str
    name: str
    properties: Dict[str, Any]

class GraphEdge(BaseModel):
    source: int
    target: int
    relationship: str

class GraphData(BaseModel):
    nodes: List[GraphNode]
    edges: List[GraphEdge]

# 通用响应模型
class ApiResponse(BaseModel):
    success: bool = True
    message: str = "操作成功"
    data: Optional[Any] = None

class FlowQueryResponse(ApiResponse):
    data: Optional[List[TestCase]] = None

class CausePathResponse(ApiResponse):
    data: Optional[List[CausePath]] = None

class ProductListResponse(ApiResponse):
    data: Optional[List[Product]] = None

class ComponentListResponse(ApiResponse):
    data: Optional[List[Component]] = None

class GraphDataResponse(ApiResponse):
    data: Optional[GraphData] = None
