#!/usr/bin/env python3
"""
知识图谱核心API - 基于Neo4j的业务查询接口
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from neo4j import GraphDatabase
from typing import List, Dict, Any, Optional
import os
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title="知识图谱核心API",
    description="基于Neo4j的质量知识图谱查询接口",
    version="2.0.0"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Neo4j连接配置
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASS = os.getenv("NEO4J_PASS", "password123")

try:
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))
    logger.info("成功连接Neo4j数据库")
except Exception as e:
    logger.error(f"连接Neo4j失败: {e}")
    driver = None

# 请求模型
class SymptomRequest(BaseModel):
    symptom: str

class AnomalyFilterRequest(BaseModel):
    factory: Optional[str] = None
    project: Optional[str] = None
    material_code: Optional[str] = None
    limit: Optional[int] = 200

# 响应模型
class PathNode(BaseModel):
    id: str
    labels: List[str]
    properties: Dict[str, Any]

class PathRelation(BaseModel):
    id: str
    type: str
    start_node: str
    end_node: str
    properties: Dict[str, Any] = {}

class CausePath(BaseModel):
    nodes: List[PathNode]
    relations: List[PathRelation]

class CausePathResponse(BaseModel):
    success: bool
    paths: List[CausePath]
    message: str = ""

class AnomalyItem(BaseModel):
    key: str
    title: str
    defects_number: int
    defect_rate: float
    factory: str
    project: str
    material_code: str
    date: str

class AnomalyResponse(BaseModel):
    success: bool
    items: List[AnomalyItem]
    total_count: int
    message: str = ""

@app.get("/health")
async def health_check():
    """健康检查"""
    neo4j_status = "connected" if driver else "disconnected"
    return {
        "status": "healthy",
        "service": "Knowledge Graph Core API",
        "neo4j": neo4j_status,
        "version": "2.0.0"
    }

@app.post("/kg/query/cause_path", response_model=CausePathResponse)
async def query_cause_path(request: SymptomRequest):
    """
    查询症状到根因到对策的因果路径
    用于异常指导页面
    """
    if not driver:
        raise HTTPException(status_code=500, detail="Neo4j数据库连接失败")
    
    try:
        query = """
        MATCH (s:Symptom {name: $symptom})
        OPTIONAL MATCH path = (s)<-[:HAS_SYMPTOM]-(a:Anomaly)-[:HAS_ROOTCAUSE]->(rc:RootCause)-[:RESOLVED_BY]->(c:Countermeasure)
        WITH path, s, a, rc, c
        WHERE path IS NOT NULL
        RETURN path
        LIMIT 5
        """
        
        paths = []
        with driver.session() as session:
            result = session.run(query, symptom=request.symptom)
            
            for record in result:
                if record["path"]:
                    path_obj = record["path"]
                    
                    # 提取节点
                    nodes = []
                    for node in path_obj.nodes:
                        nodes.append(PathNode(
                            id=str(node.element_id),
                            labels=list(node.labels),
                            properties=dict(node)
                        ))
                    
                    # 提取关系
                    relations = []
                    for rel in path_obj.relationships:
                        relations.append(PathRelation(
                            id=str(rel.element_id),
                            type=rel.type,
                            start_node=str(rel.start_node.element_id),
                            end_node=str(rel.end_node.element_id),
                            properties=dict(rel)
                        ))
                    
                    paths.append(CausePath(nodes=nodes, relations=relations))
        
        return CausePathResponse(
            success=True,
            paths=paths,
            message=f"找到 {len(paths)} 条因果路径"
        )
        
    except Exception as e:
        logger.error(f"查询因果路径失败: {e}")
        raise HTTPException(status_code=500, detail=f"查询失败: {str(e)}")

@app.post("/kg/query/anomalies", response_model=AnomalyResponse)
async def query_anomalies(request: AnomalyFilterRequest):
    """
    查询异常记录，支持按工厂、项目、物料筛选
    用于台账筛选和统计分析
    """
    if not driver:
        raise HTTPException(status_code=500, detail="Neo4j数据库连接失败")
    
    try:
        query = """
        MATCH (a:Anomaly)
        OPTIONAL MATCH (a)-[:HAPPENED_IN]->(f:Factory)
        OPTIONAL MATCH (a)-[:RELATED_TO]->(p:Project)
        OPTIONAL MATCH (a)-[:INVOLVES]->(m:Material)
        WHERE ($factory IS NULL OR f.name = $factory)
          AND ($project IS NULL OR p.name = $project)
          AND ($material_code IS NULL OR m.code = $material_code)
        RETURN 
            a.key AS key, 
            a.title AS title, 
            a.defects_number AS defects_number, 
            a.defect_rate AS defect_rate,
            COALESCE(f.name, '') AS factory, 
            COALESCE(p.name, '') AS project, 
            COALESCE(m.code, '') AS material_code,
            COALESCE(a.date, '') AS date
        ORDER BY a.date DESC NULLS LAST 
        LIMIT $limit
        """
        
        items = []
        with driver.session() as session:
            result = session.run(
                query, 
                factory=request.factory,
                project=request.project, 
                material_code=request.material_code,
                limit=request.limit
            )
            
            for record in result:
                items.append(AnomalyItem(
                    key=record["key"],
                    title=record["title"],
                    defects_number=record["defects_number"] or 0,
                    defect_rate=record["defect_rate"] or 0.0,
                    factory=record["factory"],
                    project=record["project"],
                    material_code=record["material_code"],
                    date=record["date"]
                ))
        
        return AnomalyResponse(
            success=True,
            items=items,
            total_count=len(items),
            message=f"查询到 {len(items)} 条异常记录"
        )
        
    except Exception as e:
        logger.error(f"查询异常记录失败: {e}")
        raise HTTPException(status_code=500, detail=f"查询失败: {str(e)}")

@app.get("/kg/stats")
async def get_statistics():
    """获取知识图谱统计信息"""
    if not driver:
        raise HTTPException(status_code=500, detail="Neo4j数据库连接失败")
    
    try:
        stats = {}
        with driver.session() as session:
            # 统计各类节点数量
            node_counts = session.run("""
                MATCH (n) 
                RETURN labels(n)[0] AS label, count(n) AS count
                ORDER BY count DESC
            """)
            
            stats["node_counts"] = {record["label"]: record["count"] for record in node_counts}
            
            # 统计关系数量
            rel_counts = session.run("""
                MATCH ()-[r]->() 
                RETURN type(r) AS type, count(r) AS count
                ORDER BY count DESC
            """)
            
            stats["relationship_counts"] = {record["type"]: record["count"] for record in rel_counts}
            
            # 总体统计
            total_stats = session.run("""
                MATCH (n) 
                WITH count(n) AS total_nodes
                MATCH ()-[r]->()
                WITH total_nodes, count(r) AS total_relationships
                RETURN total_nodes, total_relationships
            """).single()
            
            if total_stats:
                stats["total_nodes"] = total_stats["total_nodes"]
                stats["total_relationships"] = total_stats["total_relationships"]
        
        return {
            "success": True,
            "stats": stats,
            "message": "统计信息获取成功"
        }
        
    except Exception as e:
        logger.error(f"获取统计信息失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取统计信息失败: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
