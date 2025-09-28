from fastapi import HTTPException
from database.neo4j_client import Neo4jClient

# 全局Neo4j客户端
neo4j_client = None

def set_neo4j_client(client: Neo4jClient):
    """设置全局Neo4j客户端"""
    global neo4j_client
    neo4j_client = client

def get_neo4j_client() -> Neo4jClient:
    """获取Neo4j客户端的依赖注入函数"""
    if neo4j_client is None:
        raise HTTPException(status_code=500, detail="Neo4j client not initialized")
    return neo4j_client
