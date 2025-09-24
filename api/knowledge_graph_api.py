#!/usr/bin/env python3
"""
知识图谱核心API
聚焦于文档解析、知识抽取、图谱构建和词典管理的核心功能
"""
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import json
import logging
from datetime import datetime
from pathlib import Path
import tempfile
import os

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="知识图谱核心API",
    description="文档解析、知识抽取、图谱构建和词典管理的核心服务",
    version="1.0.0"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# 数据模型定义
# ============================================================================

class DocumentUploadResponse(BaseModel):
    """文档上传响应"""
    success: bool
    file_id: str
    filename: str
    file_type: str
    size: int
    message: str

class ExtractionRequest(BaseModel):
    """知识抽取请求"""
    file_id: str = Field(..., description="文件ID")
    extraction_type: str = Field("auto", description="抽取类型: auto/entity/relation")
    options: Dict[str, Any] = Field(default_factory=dict, description="抽取选项")

class ExtractionResponse(BaseModel):
    """知识抽取响应"""
    success: bool
    file_id: str
    entities: List[Dict[str, Any]]
    relations: List[Dict[str, Any]]
    metadata: Dict[str, Any]

class GraphBuildRequest(BaseModel):
    """图谱构建请求"""
    entities: List[Dict[str, Any]] = Field(..., description="实体列表")
    relations: List[Dict[str, Any]] = Field(..., description="关系列表")
    merge_strategy: str = Field("auto", description="合并策略: auto/strict/loose")

class GraphBuildResponse(BaseModel):
    """图谱构建响应"""
    success: bool
    nodes_created: int
    relations_created: int
    nodes_merged: int
    graph_stats: Dict[str, Any]

class GraphQueryRequest(BaseModel):
    """图谱查询请求"""
    query_type: str = Field(..., description="查询类型: cypher/pattern/search")
    query: str = Field(..., description="查询语句或模式")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="查询参数")
    limit: int = Field(100, description="结果限制")

class GraphQueryResponse(BaseModel):
    """图谱查询响应"""
    success: bool
    results: List[Dict[str, Any]]
    total_count: int
    execution_time: float

class DictionaryEntry(BaseModel):
    """词典条目"""
    id: str
    term: str
    category: str
    aliases: List[str]
    definition: str
    metadata: Dict[str, Any]

class DictionaryResponse(BaseModel):
    """词典响应"""
    success: bool
    entries: List[DictionaryEntry]
    total_count: int

# ============================================================================
# 核心服务类
# ============================================================================

class KnowledgeGraphService:
    """知识图谱核心服务"""
    
    def __init__(self):
        self.upload_dir = Path("data/uploads")
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        
        self.processed_dir = Path("data/processed")
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        
        # 模拟数据存储
        self.uploaded_files = {}
        self.extracted_data = {}
        self.graph_data = {
            "nodes": [],
            "edges": [],
            "stats": {"total_nodes": 0, "total_edges": 0}
        }
        self.dictionary = {}
    
    def upload_document(self, file: UploadFile) -> DocumentUploadResponse:
        """上传文档"""
        try:
            # 生成文件ID
            file_id = f"doc_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
            
            # 保存文件
            file_path = self.upload_dir / file_id
            with open(file_path, "wb") as f:
                content = file.file.read()
                f.write(content)
            
            # 记录文件信息
            self.uploaded_files[file_id] = {
                "filename": file.filename,
                "file_type": file.content_type,
                "size": len(content),
                "upload_time": datetime.now().isoformat(),
                "file_path": str(file_path)
            }
            
            return DocumentUploadResponse(
                success=True,
                file_id=file_id,
                filename=file.filename,
                file_type=file.content_type,
                size=len(content),
                message="文档上传成功"
            )
            
        except Exception as e:
            logger.error(f"文档上传失败: {e}")
            return DocumentUploadResponse(
                success=False,
                file_id="",
                filename=file.filename,
                file_type="",
                size=0,
                message=f"上传失败: {str(e)}"
            )
    
    def extract_knowledge(self, request: ExtractionRequest) -> ExtractionResponse:
        """知识抽取"""
        try:
            if request.file_id not in self.uploaded_files:
                raise ValueError(f"文件不存在: {request.file_id}")
            
            file_info = self.uploaded_files[request.file_id]
            
            # 模拟知识抽取过程
            entities = [
                {
                    "id": "entity_001",
                    "type": "Material",
                    "name": "摄像头模块",
                    "properties": {
                        "category": "光学组件",
                        "supplier": "XX光学公司"
                    }
                },
                {
                    "id": "entity_002", 
                    "type": "Anomaly",
                    "name": "对焦失败",
                    "properties": {
                        "severity": "S1",
                        "frequency": "高"
                    }
                }
            ]
            
            relations = [
                {
                    "id": "rel_001",
                    "type": "HAS_ANOMALY",
                    "source": "entity_001",
                    "target": "entity_002",
                    "properties": {
                        "confidence": 0.9
                    }
                }
            ]
            
            # 保存抽取结果
            self.extracted_data[request.file_id] = {
                "entities": entities,
                "relations": relations,
                "extraction_time": datetime.now().isoformat()
            }
            
            return ExtractionResponse(
                success=True,
                file_id=request.file_id,
                entities=entities,
                relations=relations,
                metadata={
                    "extraction_type": request.extraction_type,
                    "entity_count": len(entities),
                    "relation_count": len(relations),
                    "source_file": file_info["filename"]
                }
            )
            
        except Exception as e:
            logger.error(f"知识抽取失败: {e}")
            return ExtractionResponse(
                success=False,
                file_id=request.file_id,
                entities=[],
                relations=[],
                metadata={"error": str(e)}
            )
    
    def build_graph(self, request: GraphBuildRequest) -> GraphBuildResponse:
        """构建知识图谱"""
        try:
            nodes_created = 0
            relations_created = 0
            nodes_merged = 0
            
            # 处理实体
            for entity in request.entities:
                existing_node = next((n for n in self.graph_data["nodes"] if n["id"] == entity["id"]), None)
                if existing_node:
                    # 合并节点
                    existing_node.update(entity)
                    nodes_merged += 1
                else:
                    # 创建新节点
                    self.graph_data["nodes"].append(entity)
                    nodes_created += 1
            
            # 处理关系
            for relation in request.relations:
                existing_edge = next((e for e in self.graph_data["edges"] if 
                                    e["source"] == relation["source"] and 
                                    e["target"] == relation["target"] and
                                    e["type"] == relation["type"]), None)
                if not existing_edge:
                    self.graph_data["edges"].append(relation)
                    relations_created += 1
            
            # 更新统计信息
            self.graph_data["stats"] = {
                "total_nodes": len(self.graph_data["nodes"]),
                "total_edges": len(self.graph_data["edges"]),
                "last_updated": datetime.now().isoformat()
            }
            
            return GraphBuildResponse(
                success=True,
                nodes_created=nodes_created,
                relations_created=relations_created,
                nodes_merged=nodes_merged,
                graph_stats=self.graph_data["stats"]
            )
            
        except Exception as e:
            logger.error(f"图谱构建失败: {e}")
            return GraphBuildResponse(
                success=False,
                nodes_created=0,
                relations_created=0,
                nodes_merged=0,
                graph_stats={}
            )
    
    def query_graph(self, request: GraphQueryRequest) -> GraphQueryResponse:
        """查询知识图谱"""
        try:
            start_time = datetime.now()
            
            results = []
            
            if request.query_type == "search":
                # 简单搜索
                query_lower = request.query.lower()
                for node in self.graph_data["nodes"]:
                    if query_lower in node.get("name", "").lower():
                        results.append(node)
                        if len(results) >= request.limit:
                            break
            
            elif request.query_type == "pattern":
                # 模式匹配（简化版）
                if "摄像头" in request.query:
                    results = [n for n in self.graph_data["nodes"] if "摄像头" in n.get("name", "")]
            
            else:
                # 返回所有节点（简化版）
                results = self.graph_data["nodes"][:request.limit]
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return GraphQueryResponse(
                success=True,
                results=results,
                total_count=len(results),
                execution_time=execution_time
            )
            
        except Exception as e:
            logger.error(f"图谱查询失败: {e}")
            return GraphQueryResponse(
                success=False,
                results=[],
                total_count=0,
                execution_time=0.0
            )
    
    def get_dictionary(self, category: Optional[str] = None) -> DictionaryResponse:
        """获取词典"""
        try:
            entries = []
            
            # 模拟词典数据
            sample_entries = [
                {
                    "id": "dict_001",
                    "term": "摄像头",
                    "category": "组件",
                    "aliases": ["相机", "Camera"],
                    "definition": "用于拍照和录像的光学设备",
                    "metadata": {"frequency": "高", "domain": "硬件"}
                },
                {
                    "id": "dict_002",
                    "term": "对焦失败",
                    "category": "异常",
                    "aliases": ["无法对焦", "对焦异常"],
                    "definition": "摄像头无法正确对焦的故障现象",
                    "metadata": {"severity": "S1", "domain": "质量"}
                }
            ]
            
            if category:
                entries = [e for e in sample_entries if e["category"] == category]
            else:
                entries = sample_entries
            
            return DictionaryResponse(
                success=True,
                entries=[DictionaryEntry(**entry) for entry in entries],
                total_count=len(entries)
            )
            
        except Exception as e:
            logger.error(f"获取词典失败: {e}")
            return DictionaryResponse(
                success=False,
                entries=[],
                total_count=0
            )

# 创建服务实例
kg_service = KnowledgeGraphService()

# ============================================================================
# API端点定义
# ============================================================================

@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "service": "Knowledge Graph API",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

@app.post("/kg/upload", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """上传文档
    
    支持多种格式：Excel、PDF、Word、CSV、TXT等
    """
    return kg_service.upload_document(file)

@app.post("/kg/extract", response_model=ExtractionResponse)
async def extract_knowledge(request: ExtractionRequest):
    """知识抽取
    
    从上传的文档中抽取实体和关系
    """
    return kg_service.extract_knowledge(request)

@app.post("/kg/build", response_model=GraphBuildResponse)
async def build_graph(request: GraphBuildRequest):
    """构建知识图谱
    
    将抽取的实体和关系构建成知识图谱
    """
    return kg_service.build_graph(request)

@app.post("/kg/query", response_model=GraphQueryResponse)
async def query_graph(request: GraphQueryRequest):
    """查询知识图谱
    
    支持多种查询方式：Cypher、模式匹配、关键词搜索
    """
    return kg_service.query_graph(request)

@app.get("/kg/graph/data")
async def get_graph_data():
    """获取图谱数据
    
    返回完整的图谱数据用于可视化
    """
    return {
        "success": True,
        "data": kg_service.graph_data,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/kg/dictionary", response_model=DictionaryResponse)
async def get_dictionary(category: Optional[str] = None):
    """获取词典
    
    返回标准化词典，支持按类别过滤
    """
    return kg_service.get_dictionary(category)

@app.get("/kg/stats")
async def get_statistics():
    """获取统计信息
    
    返回系统的整体统计信息
    """
    return {
        "success": True,
        "stats": {
            "uploaded_files": len(kg_service.uploaded_files),
            "extracted_files": len(kg_service.extracted_data),
            "total_nodes": kg_service.graph_data["stats"].get("total_nodes", 0),
            "total_edges": kg_service.graph_data["stats"].get("total_edges", 0),
            "dictionary_entries": 2  # 模拟数据
        },
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
