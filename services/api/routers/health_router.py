from fastapi import APIRouter, Depends, HTTPException
from database.neo4j_client import Neo4jClient
from main import get_neo4j_client

router = APIRouter()

@router.get("/")
async def health_check():
    """健康检查接口"""
    return {
        "status": "healthy",
        "service": "质量知识图谱API",
        "version": "1.0.0"
    }

@router.get("/neo4j")
async def neo4j_health(neo4j_client: Neo4jClient = Depends(get_neo4j_client)):
    """Neo4j数据库健康检查"""
    try:
        is_connected = neo4j_client.test_connection()
        if is_connected:
            return {
                "status": "healthy",
                "database": "neo4j",
                "connection": "active"
            }
        else:
            raise HTTPException(status_code=503, detail="Neo4j connection failed")
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Neo4j health check failed: {str(e)}")
