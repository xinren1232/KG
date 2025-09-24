#!/usr/bin/env python3
"""
Dify工具服务器
提供HTTP接口供Dify调用质量知识图谱工具
"""
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
import json
import logging
from datetime import datetime
from kg_tools import QualityKGDifyTools

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="质量知识图谱Dify工具服务",
    description="为Dify提供质量知识图谱工具调用接口",
    version="0.2.0"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Dify可能从不同域名访问
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建工具实例
kg_tools = QualityKGDifyTools()

# ============================================================================
# 数据模型
# ============================================================================

class ToolRequest(BaseModel):
    """工具调用请求"""
    tool_name: str = Field(..., description="工具名称")
    parameters: Dict[str, Any] = Field(..., description="工具参数")

class ToolResponse(BaseModel):
    """工具调用响应"""
    success: bool
    result: str
    metadata: Dict[str, Any] = {}

class ToolDefinitionResponse(BaseModel):
    """工具定义响应"""
    tools: List[Dict[str, Any]]
    metadata: Dict[str, Any]

# ============================================================================
# API端点
# ============================================================================

@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "service": "QualityKG Dify Tool Server",
        "timestamp": datetime.now().isoformat(),
        "tools_available": len(kg_tools.get_tool_definitions())
    }

@app.get("/tools/definitions", response_model=ToolDefinitionResponse)
async def get_tool_definitions():
    """获取所有工具定义"""
    try:
        definitions = kg_tools.get_tool_definitions()
        return ToolDefinitionResponse(
            tools=definitions,
            metadata={
                "total_tools": len(definitions),
                "categories": ["质量分析", "案例分析", "统计分析", "流程管理", "信息检索"],
                "version": "0.2.0"
            }
        )
    except Exception as e:
        logger.error(f"获取工具定义失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tools/invoke", response_model=ToolResponse)
async def invoke_tool(request: ToolRequest):
    """调用指定工具"""
    try:
        tool_name = request.tool_name
        parameters = request.parameters
        
        logger.info(f"调用工具: {tool_name}, 参数: {parameters}")
        
        # 根据工具名称调用对应方法
        if tool_name == "anomaly_trace":
            result = kg_tools.anomaly_trace(**parameters)
        elif tool_name == "case_reuse":
            result = kg_tools.case_reuse(**parameters)
        elif tool_name == "quality_stats":
            result = kg_tools.quality_stats(**parameters)
        elif tool_name == "process_linkage":
            result = kg_tools.process_linkage(**parameters)
        elif tool_name == "entity_search":
            result = kg_tools.entity_search(**parameters)
        else:
            raise ValueError(f"未知的工具名称: {tool_name}")
        
        return ToolResponse(
            success=True,
            result=result,
            metadata={
                "tool_name": tool_name,
                "execution_time": datetime.now().isoformat(),
                "parameters_used": parameters
            }
        )
        
    except Exception as e:
        logger.error(f"工具调用失败: {e}")
        return ToolResponse(
            success=False,
            result=f"工具调用失败: {str(e)}",
            metadata={
                "tool_name": request.tool_name,
                "error": str(e),
                "execution_time": datetime.now().isoformat()
            }
        )

@app.post("/tools/anomaly_trace")
async def anomaly_trace_endpoint(
    symptom: Optional[str] = None,
    anomaly_id: Optional[str] = None,
    factory: Optional[str] = None,
    material_code: Optional[str] = None
):
    """异常溯源工具端点"""
    try:
        params = {k: v for k, v in locals().items() if v is not None}
        result = kg_tools.anomaly_trace(**params)
        return {"success": True, "result": result}
    except Exception as e:
        logger.error(f"异常溯源失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tools/case_reuse")
async def case_reuse_endpoint(
    symptom: str,
    component: Optional[str] = None,
    similarity_threshold: float = 0.7
):
    """案例复用工具端点"""
    try:
        result = kg_tools.case_reuse(
            symptom=symptom,
            component=component,
            similarity_threshold=similarity_threshold
        )
        return {"success": True, "result": result}
    except Exception as e:
        logger.error(f"案例复用失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tools/quality_stats")
async def quality_stats_endpoint(
    factory: Optional[str] = None,
    project: Optional[str] = None,
    group_by: str = "factory"
):
    """质量统计工具端点"""
    try:
        result = kg_tools.quality_stats(
            factory=factory,
            project=project,
            group_by=group_by
        )
        return {"success": True, "result": result}
    except Exception as e:
        logger.error(f"质量统计失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tools/process_linkage")
async def process_linkage_endpoint(
    anomaly_id: str,
    include_sop: bool = True,
    include_test_cases: bool = True
):
    """流程联动工具端点"""
    try:
        result = kg_tools.process_linkage(
            anomaly_id=anomaly_id,
            include_sop=include_sop,
            include_test_cases=include_test_cases
        )
        return {"success": True, "result": result}
    except Exception as e:
        logger.error(f"流程联动失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tools/entity_search")
async def entity_search_endpoint(
    query: str,
    entity_type: Optional[str] = None,
    limit: int = 10
):
    """实体搜索工具端点"""
    try:
        result = kg_tools.entity_search(
            query=query,
            entity_type=entity_type,
            limit=limit
        )
        return {"success": True, "result": result}
    except Exception as e:
        logger.error(f"实体搜索失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tools/config")
async def get_dify_config():
    """获取Dify配置"""
    try:
        with open("services/dify/dify_config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
        return config
    except Exception as e:
        logger.error(f"获取配置失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/webhook/dify")
async def dify_webhook(request: Request):
    """Dify Webhook端点"""
    try:
        body = await request.json()
        logger.info(f"收到Dify Webhook: {body}")
        
        # 处理Dify的工具调用请求
        if "tool_name" in body and "parameters" in body:
            tool_request = ToolRequest(**body)
            response = await invoke_tool(tool_request)
            return response.dict()
        
        return {"status": "received", "message": "Webhook处理成功"}
        
    except Exception as e:
        logger.error(f"Webhook处理失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    """根路径"""
    return {
        "service": "质量知识图谱Dify工具服务",
        "version": "0.2.0",
        "description": "为Dify提供质量知识图谱工具调用接口",
        "endpoints": {
            "health": "/health",
            "tool_definitions": "/tools/definitions",
            "invoke_tool": "/tools/invoke",
            "anomaly_trace": "/tools/anomaly_trace",
            "case_reuse": "/tools/case_reuse",
            "quality_stats": "/tools/quality_stats",
            "process_linkage": "/tools/process_linkage",
            "entity_search": "/tools/entity_search",
            "dify_config": "/tools/config",
            "webhook": "/webhook/dify"
        },
        "documentation": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    
    logger.info("启动质量知识图谱Dify工具服务...")
    logger.info("服务地址: http://localhost:8002")
    logger.info("API文档: http://localhost:8002/docs")
    logger.info("工具定义: http://localhost:8002/tools/definitions")
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8002,
        log_level="info"
    )
