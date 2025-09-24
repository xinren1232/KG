from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

from database.neo4j_client import Neo4jClient
from routers import kg_router, health_router

# 加载环境变量
load_dotenv()

# 全局Neo4j客户端
neo4j_client = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时初始化Neo4j连接
    global neo4j_client
    neo4j_client = Neo4jClient(
        uri=os.getenv("NEO4J_URI", "bolt://localhost:7687"),
        user=os.getenv("NEO4J_USER", "neo4j"),
        password=os.getenv("NEO4J_PASS", "password123")
    )
    
    # 测试连接
    try:
        neo4j_client.test_connection()
        print("✅ Neo4j connection established")
    except Exception as e:
        print(f"❌ Failed to connect to Neo4j: {e}")
        raise
    
    yield
    
    # 关闭时清理连接
    if neo4j_client:
        neo4j_client.close()
        print("🔌 Neo4j connection closed")

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

@app.get("/")
async def root():
    return {
        "message": "质量知识图谱API服务",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

# 获取Neo4j客户端的依赖注入函数
def get_neo4j_client() -> Neo4jClient:
    if neo4j_client is None:
        raise HTTPException(status_code=500, detail="Neo4j client not initialized")
    return neo4j_client
