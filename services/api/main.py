from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

from database.neo4j_client import Neo4jClient
from dependencies import set_neo4j_client
from routers import kg_router, health_router, system_router

# 加载环境变量
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时初始化Neo4j连接
    client = Neo4jClient(
        uri=os.getenv("NEO4J_URI", "bolt://localhost:7687"),
        user=os.getenv("NEO4J_USER", "neo4j"),
        password=os.getenv("NEO4J_PASS", "password123")
    )

    # 测试连接
    try:
        client.test_connection()
        print("✅ Neo4j connection established")
        set_neo4j_client(client)
    except Exception as e:
        print(f"❌ Failed to connect to Neo4j: {e}")
        print("⚠️ Starting API without Neo4j connection")
        # 不抛出异常，允许API在没有Neo4j的情况下启动

    yield

    # 关闭时清理连接
    try:
        from dependencies import neo4j_client
        if neo4j_client:
            neo4j_client.close()
            print("🔌 Neo4j connection closed")
    except:
        pass

# 创建FastAPI应用
app = FastAPI(
    title="质量知识图谱API",
    description="手机研发质量部门知识图谱助手API服务",
    version="1.0.0",
    lifespan=lifespan
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(health_router.router, prefix="/health", tags=["健康检查"])
app.include_router(kg_router.router, prefix="/kg", tags=["知识图谱"])
app.include_router(system_router.router, prefix="/system", tags=["系统管理"])
app.include_router(system_router.router, prefix="/api/system", tags=["系统管理API"])

@app.get("/")
async def root():
    return {
        "message": "质量知识图谱API服务",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

# 启动服务器
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
