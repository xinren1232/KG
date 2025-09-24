#!/usr/bin/env python3
"""
知识图谱构建API服务
专门用于文件抽取和知识图谱构建
"""

import os
import sys
import tempfile
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path
import shutil

from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn

# 添加ETL模块路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'etl'))

from file_extractor import FileExtractor, ExtractionResult
from knowledge_graph_builder import KnowledgeGraphBuilder, GraphStats

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title="质量知识图谱构建API",
    description="文件信息抽取和知识图谱构建服务",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局变量
file_extractor = FileExtractor()
kg_builder = None

# 数据模型
class FileUploadResponse(BaseModel):
    """文件上传响应"""
    file_id: str
    filename: str
    file_size: int
    file_type: str
    status: str

class ExtractionResponse(BaseModel):
    """抽取响应"""
    file_path: str
    file_type: str
    entities_count: int
    relations_count: int
    errors: List[str]
    metadata: Dict[str, Any]

class GraphBuildResponse(BaseModel):
    """图谱构建响应"""
    created_nodes: int
    created_relationships: int
    source_file: str
    processing_errors: List[str]

class EntityModel(BaseModel):
    """实体模型"""
    id: str
    name: str
    type: str
    properties: Dict[str, Any]
    source_file: str

class RelationModel(BaseModel):
    """关系模型"""
    source_entity: str
    target_entity: str
    relation_type: str
    properties: Dict[str, Any]
    confidence: float

class GraphQueryRequest(BaseModel):
    """图谱查询请求"""
    cypher_query: str
    parameters: Optional[Dict[str, Any]] = None

# 初始化函数
@app.on_event("startup")
async def startup_event():
    """应用启动时初始化"""
    global kg_builder
    
    # 初始化知识图谱构建器
    neo4j_uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    neo4j_user = os.getenv("NEO4J_USER", "neo4j")
    neo4j_password = os.getenv("NEO4J_PASSWORD", "password")
    
    kg_builder = KnowledgeGraphBuilder(neo4j_uri, neo4j_user, neo4j_password)
    
    try:
        kg_builder.connect()
        kg_builder.initialize_schema()
        logger.info("知识图谱构建器初始化成功")
    except Exception as e:
        logger.warning(f"Neo4j连接失败，将使用模拟模式: {e}")
        kg_builder = None

@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时清理"""
    if kg_builder:
        kg_builder.close()

# API端点

@app.get("/health")
async def health_check():
    """健康检查"""
    neo4j_status = "connected" if kg_builder else "disconnected"
    return {
        "status": "healthy",
        "neo4j": neo4j_status,
        "extractor": "ready"
    }

@app.post("/kg/upload", response_model=FileUploadResponse)
async def upload_file(file: UploadFile = File(...)):
    """上传文件"""
    try:
        # 检查文件类型
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in file_extractor.supported_formats:
            raise HTTPException(
                status_code=400,
                detail=f"不支持的文件格式: {file_ext}. 支持的格式: {file_extractor.supported_formats}"
            )
        
        # 保存文件到临时目录
        upload_dir = Path("data/uploads")
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = upload_dir / file.filename
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        file_size = file_path.stat().st_size
        
        return FileUploadResponse(
            file_id=str(hash(file.filename)),
            filename=file.filename,
            file_size=file_size,
            file_type=file_ext,
            status="uploaded"
        )
    
    except Exception as e:
        logger.error(f"文件上传失败: {e}")
        raise HTTPException(status_code=500, detail=f"文件上传失败: {str(e)}")

@app.post("/kg/extract/{filename}", response_model=ExtractionResponse)
async def extract_file_data(filename: str):
    """抽取文件数据"""
    try:
        file_path = Path("data/uploads") / filename
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="文件不存在")
        
        # 执行数据抽取
        extraction_result = file_extractor.extract_file(str(file_path))
        
        return ExtractionResponse(
            file_path=extraction_result.file_path,
            file_type=extraction_result.file_type,
            entities_count=len(extraction_result.entities),
            relations_count=len(extraction_result.relations),
            errors=extraction_result.errors,
            metadata=extraction_result.metadata
        )
    
    except Exception as e:
        logger.error(f"数据抽取失败: {e}")
        raise HTTPException(status_code=500, detail=f"数据抽取失败: {str(e)}")

@app.post("/kg/build/{filename}", response_model=GraphBuildResponse)
async def build_knowledge_graph(filename: str, background_tasks: BackgroundTasks):
    """构建知识图谱"""
    try:
        file_path = Path("data/uploads") / filename
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="文件不存在")
        
        # 执行数据抽取
        extraction_result = file_extractor.extract_file(str(file_path))
        
        if not kg_builder:
            # 模拟模式
            return GraphBuildResponse(
                created_nodes=len(extraction_result.entities),
                created_relationships=len(extraction_result.relations),
                source_file=str(file_path),
                processing_errors=["Neo4j未连接，使用模拟模式"]
            )
        
        # 构建知识图谱
        build_result = kg_builder.build_graph_from_extraction(extraction_result)
        
        return GraphBuildResponse(
            created_nodes=build_result['created_nodes'],
            created_relationships=build_result['created_relationships'],
            source_file=build_result['source_file'],
            processing_errors=build_result['processing_errors']
        )
    
    except Exception as e:
        logger.error(f"知识图谱构建失败: {e}")
        raise HTTPException(status_code=500, detail=f"知识图谱构建失败: {str(e)}")

@app.get("/kg/stats")
async def get_graph_stats():
    """获取图谱统计信息"""
    try:
        if not kg_builder:
            # 模拟模式下返回示例统计数据
            logger.info("Neo4j未连接，返回模拟统计数据")
            return {
                "total_nodes": 48,
                "total_relationships": 120,
                "node_types": {
                    "product": 8,
                    "component": 8,
                    "test_case": 8,
                    "anomaly": 8,
                    "root_cause": 8,
                    "countermeasure": 8
                },
                "relationship_types": {
                    "related_to": 96,
                    "contains": 8,
                    "tested_by": 8,
                    "detects": 4,
                    "caused_by": 2,
                    "resolved_by": 2
                },
                "source_files": ["test_sample.csv"],
                "status": "simulation_mode"
            }
        
        stats = kg_builder.get_graph_stats()
        
        return {
            "total_nodes": stats.total_nodes,
            "total_relationships": stats.total_relationships,
            "node_types": stats.node_types,
            "relationship_types": stats.relationship_types,
            "source_files": stats.source_files,
            "status": "connected"
        }
    
    except Exception as e:
        logger.error(f"获取图谱统计失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取图谱统计失败: {str(e)}")

@app.post("/kg/query")
async def query_graph(request: GraphQueryRequest):
    """查询知识图谱"""
    try:
        if not kg_builder:
            # 模拟模式下返回示例数据
            logger.info("Neo4j未连接，返回模拟查询结果")
            mock_results = [
                {"entity_type": "product", "count": 8},
                {"entity_type": "component", "count": 8},
                {"entity_type": "test_case", "count": 8},
                {"entity_type": "anomaly", "count": 8},
                {"entity_type": "root_cause", "count": 8},
                {"entity_type": "countermeasure", "count": 8}
            ]
            return {
                "query": request.cypher_query,
                "parameters": request.parameters or {},
                "results": mock_results,
                "count": len(mock_results),
                "status": "simulation_mode"
            }

        result = kg_builder.query_graph(request.cypher_query, request.parameters)

        return {
            "query": request.cypher_query,
            "parameters": request.parameters,
            "results": result,
            "count": len(result)
        }

    except Exception as e:
        logger.error(f"图谱查询失败: {e}")
        raise HTTPException(status_code=500, detail=f"图谱查询失败: {str(e)}")

@app.get("/kg/entities")
async def get_entities(entity_type: Optional[str] = None, limit: int = 100):
    """获取实体列表"""
    try:
        if not kg_builder:
            # 模拟模式下返回示例实体数据
            logger.info("Neo4j未连接，返回模拟实体数据")
            mock_entities = [
                {"id": "product_1", "name": "iPhone 15", "type": "product", "properties": {"category": "手机"}, "source_file": "test_sample.csv"},
                {"id": "component_1", "name": "摄像头", "type": "component", "properties": {"module": "硬件"}, "source_file": "test_sample.csv"},
                {"id": "test_case_1", "name": "TC001", "type": "test_case", "properties": {"priority": "高"}, "source_file": "test_sample.csv"},
                {"id": "anomaly_1", "name": "拍照模糊", "type": "anomaly", "properties": {"severity": "中"}, "source_file": "test_sample.csv"},
                {"id": "root_cause_1", "name": "镜头污染", "type": "root_cause", "properties": {"category": "硬件"}, "source_file": "test_sample.csv"},
                {"id": "countermeasure_1", "name": "清洁镜头", "type": "countermeasure", "properties": {"type": "维修"}, "source_file": "test_sample.csv"}
            ]

            # 如果指定了实体类型，过滤结果
            if entity_type:
                mock_entities = [e for e in mock_entities if e["type"] == entity_type]

            # 应用限制
            mock_entities = mock_entities[:limit]

            return {
                "entities": mock_entities,
                "count": len(mock_entities),
                "status": "simulation_mode"
            }

        if entity_type:
            cypher = """
            MATCH (e:Entity {type: $entity_type})
            RETURN e.id as id, e.name as name, e.type as type,
                   e.properties as properties, e.source_file as source_file
            LIMIT $limit
            """
            parameters = {"entity_type": entity_type, "limit": limit}
        else:
            cypher = """
            MATCH (e:Entity)
            RETURN e.id as id, e.name as name, e.type as type,
                   e.properties as properties, e.source_file as source_file
            LIMIT $limit
            """
            parameters = {"limit": limit}

        result = kg_builder.query_graph(cypher, parameters)

        return {
            "entities": result,
            "count": len(result),
            "status": "success"
        }

    except Exception as e:
        logger.error(f"获取实体列表失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取实体列表失败: {str(e)}")

@app.get("/kg/relations")
async def get_relations(relation_type: Optional[str] = None, limit: int = 100):
    """获取关系列表"""
    try:
        if not kg_builder:
            return {"relations": [], "count": 0, "status": "neo4j_disconnected"}
        
        if relation_type:
            cypher = f"""
            MATCH (source)-[r:{relation_type.upper()}]->(target)
            RETURN source.id as source_entity, target.id as target_entity,
                   type(r) as relation_type, r.properties as properties,
                   r.confidence as confidence
            LIMIT $limit
            """
            parameters = {"limit": limit}
        else:
            cypher = """
            MATCH (source)-[r]->(target)
            RETURN source.id as source_entity, target.id as target_entity,
                   type(r) as relation_type, r.properties as properties,
                   r.confidence as confidence
            LIMIT $limit
            """
            parameters = {"limit": limit}
        
        result = kg_builder.query_graph(cypher, parameters)
        
        return {
            "relations": result,
            "count": len(result),
            "status": "success"
        }
    
    except Exception as e:
        logger.error(f"获取关系列表失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取关系列表失败: {str(e)}")

@app.get("/kg/graph/data")
async def get_graph_data(node_limit: int = 100, include_relations: bool = True):
    """获取图谱可视化数据"""
    try:
        if not kg_builder:
            # 模拟模式下返回示例图谱数据
            logger.info("Neo4j未连接，返回模拟图谱数据")
            mock_nodes = [
                {"data": {"id": "product_1", "label": "iPhone 15", "type": "product", "properties": {"category": "手机"}}},
                {"data": {"id": "component_1", "label": "摄像头", "type": "component", "properties": {"module": "硬件"}}},
                {"data": {"id": "test_case_1", "label": "TC001", "type": "test_case", "properties": {"priority": "高"}}},
                {"data": {"id": "anomaly_1", "label": "拍照模糊", "type": "anomaly", "properties": {"severity": "中"}}},
                {"data": {"id": "root_cause_1", "label": "镜头污染", "type": "root_cause", "properties": {"category": "硬件"}}},
                {"data": {"id": "countermeasure_1", "label": "清洁镜头", "type": "countermeasure", "properties": {"type": "维修"}}}
            ]

            mock_edges = [
                {"data": {"id": "product_1-component_1", "source": "product_1", "target": "component_1", "type": "contains", "confidence": 1.0}},
                {"data": {"id": "component_1-test_case_1", "source": "component_1", "target": "test_case_1", "type": "tested_by", "confidence": 1.0}},
                {"data": {"id": "test_case_1-anomaly_1", "source": "test_case_1", "target": "anomaly_1", "type": "detects", "confidence": 0.9}},
                {"data": {"id": "anomaly_1-root_cause_1", "source": "anomaly_1", "target": "root_cause_1", "type": "caused_by", "confidence": 0.8}},
                {"data": {"id": "root_cause_1-countermeasure_1", "source": "root_cause_1", "target": "countermeasure_1", "type": "resolved_by", "confidence": 0.9}}
            ]

            return {
                "nodes": mock_nodes[:node_limit],
                "edges": mock_edges if include_relations else [],
                "status": "simulation_mode"
            }
        
        # 获取节点
        nodes_cypher = """
        MATCH (n:Entity)
        RETURN n.id as id, n.name as name, n.type as type,
               n.properties as properties
        LIMIT $limit
        """
        nodes_result = kg_builder.query_graph(nodes_cypher, {"limit": node_limit})
        
        # 转换节点格式
        nodes = []
        for node in nodes_result:
            nodes.append({
                "data": {
                    "id": node["id"],
                    "label": node["name"],
                    "type": node["type"],
                    "properties": node.get("properties", {})
                }
            })
        
        edges = []
        if include_relations:
            # 获取关系（只包含已加载的节点）
            node_ids = [node["id"] for node in nodes_result]
            if node_ids:
                edges_cypher = """
                MATCH (source)-[r]->(target)
                WHERE source.id IN $node_ids AND target.id IN $node_ids
                RETURN source.id as source, target.id as target,
                       type(r) as type, r.confidence as confidence
                """
                edges_result = kg_builder.query_graph(edges_cypher, {"node_ids": node_ids})
                
                # 转换关系格式
                for edge in edges_result:
                    edges.append({
                        "data": {
                            "id": f"{edge['source']}-{edge['target']}",
                            "source": edge["source"],
                            "target": edge["target"],
                            "type": edge["type"],
                            "confidence": edge.get("confidence", 1.0)
                        }
                    })
        
        return {
            "nodes": nodes,
            "edges": edges,
            "status": "success"
        }
    
    except Exception as e:
        logger.error(f"获取图谱数据失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取图谱数据失败: {str(e)}")

@app.delete("/kg/clear")
async def clear_graph():
    """清空知识图谱"""
    try:
        if not kg_builder:
            raise HTTPException(status_code=503, detail="Neo4j未连接")
        
        kg_builder.clear_graph()
        
        return {"message": "知识图谱已清空", "status": "success"}
    
    except Exception as e:
        logger.error(f"清空图谱失败: {e}")
        raise HTTPException(status_code=500, detail=f"清空图谱失败: {str(e)}")

@app.get("/kg/files")
async def list_uploaded_files():
    """列出已上传的文件"""
    try:
        upload_dir = Path("data/uploads")
        if not upload_dir.exists():
            return {"files": []}
        
        files = []
        for file_path in upload_dir.iterdir():
            if file_path.is_file():
                files.append({
                    "filename": file_path.name,
                    "size": file_path.stat().st_size,
                    "modified": file_path.stat().st_mtime,
                    "extension": file_path.suffix
                })
        
        return {"files": files}
    
    except Exception as e:
        logger.error(f"列出文件失败: {e}")
        raise HTTPException(status_code=500, detail=f"列出文件失败: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(
        "main_kg:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
