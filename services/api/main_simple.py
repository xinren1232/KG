from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any

# 创建FastAPI应用
app = FastAPI(
    title="质量知识图谱API",
    description="手机研发质量部门知识图谱助手API服务",
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

@app.get("/")
async def root():
    return {
        "message": "质量知识图谱API服务",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {
        "status": "healthy",
        "service": "质量知识图谱API",
        "version": "1.0.0"
    }

# 模拟数据
MOCK_PRODUCTS = [
    {"name": "iPhone 15", "model": "A2846", "category": "smartphone", "status": "active"},
    {"name": "Galaxy S24", "model": "SM-S921", "category": "smartphone", "status": "active"}
]

MOCK_COMPONENTS = [
    {"name": "摄像头模块", "type": "hardware", "criticality": "high"},
    {"name": "电池模块", "type": "hardware", "criticality": "high"},
    {"name": "WiFi模块", "type": "hardware", "criticality": "medium"},
    {"name": "屏幕模块", "type": "hardware", "criticality": "high"}
]

MOCK_TEST_CASES = [
    {
        "id": "TC-CAM-001",
        "title": "摄像头对焦功能测试",
        "description": "验证摄像头在各种光线条件下的对焦功能",
        "priority": "high",
        "type": "functional"
    },
    {
        "id": "TC-BAT-001",
        "title": "电池充电功能测试",
        "description": "验证电池充电功能的正常性",
        "priority": "high",
        "type": "functional"
    }
]

MOCK_ANOMALIES = [
    {
        "anomaly_id": "ANO-2024-001",
        "anomaly_title": "摄像头无法对焦",
        "severity": "high",
        "status": "resolved",
        "symptom": "摄像头对焦失败",
        "root_cause": "传感器校准偏差",
        "countermeasure": "重新校准摄像头传感器",
        "component": "摄像头模块"
    }
]

@app.get("/kg/products")
async def get_products():
    """获取所有产品列表"""
    return {
        "success": True,
        "message": "获取产品列表成功",
        "data": MOCK_PRODUCTS
    }

@app.get("/kg/products/{product_name}/components")
async def get_components(product_name: str):
    """获取指定产品的组件列表"""
    return {
        "success": True,
        "message": f"获取{product_name}的组件列表成功",
        "data": MOCK_COMPONENTS
    }

@app.post("/kg/query/flow")
async def query_test_flow(request: Dict[str, Any]):
    """查询测试流程和用例"""
    product_name = request.get("product_name", "")
    component_name = request.get("component_name", "")
    
    # 模拟过滤逻辑
    filtered_cases = MOCK_TEST_CASES
    if component_name:
        # 这里可以根据组件名称过滤
        pass
    
    return {
        "success": True,
        "message": f"找到 {len(filtered_cases)} 个测试用例",
        "data": filtered_cases
    }

@app.post("/kg/query/cause_path")
async def query_cause_path(request: Dict[str, Any]):
    """查询异常因果路径"""
    symptom_description = request.get("symptom_description", "")
    
    # 模拟搜索逻辑
    filtered_anomalies = []
    for anomaly in MOCK_ANOMALIES:
        if symptom_description.lower() in anomaly["symptom"].lower():
            filtered_anomalies.append(anomaly)
    
    return {
        "success": True,
        "message": f"找到 {len(filtered_anomalies)} 个相关异常",
        "data": filtered_anomalies
    }

@app.get("/kg/graph")
async def get_graph_data(limit: int = 100):
    """获取知识图谱可视化数据"""
    # 模拟图谱数据
    nodes = [
        {"id": 1, "label": "Product", "name": "iPhone 15"},
        {"id": 2, "label": "Component", "name": "摄像头模块"},
        {"id": 3, "label": "Anomaly", "name": "摄像头无法对焦"},
        {"id": 4, "label": "TestCase", "name": "摄像头对焦功能测试"}
    ]
    
    edges = [
        {"source": 1, "target": 2, "relationship": "HAS_COMPONENT"},
        {"source": 3, "target": 2, "relationship": "OCCURS_IN"},
        {"source": 4, "target": 2, "relationship": "TESTS"}
    ]
    
    return {
        "success": True,
        "message": f"获取到 {len(nodes)} 个节点，{len(edges)} 条关系",
        "data": {"nodes": nodes, "edges": edges}
    }

# 智能问答相关API
@app.post("/kg/qa/ask")
async def ask_question(request: Dict[str, Any]):
    """智能问答"""
    question = request.get("question", "")
    if not question:
        raise HTTPException(status_code=400, detail="问题不能为空")

    # 模拟智能问答结果
    mock_answer = {
        "question": question,
        "answer": f"根据您的问题 '{question}'，我为您分析如下：\n\n这是一个关于质量管理的问题。建议您：\n1. 查看相关测试用例和流程\n2. 检查历史异常记录\n3. 咨询相关技术专家\n\n如需更详细的信息，请提供具体的产品或组件名称。",
        "confidence": 0.85,
        "sources": [
            {"type": "knowledge_base", "title": "质量管理手册", "relevance": "high"},
            {"type": "test_case", "title": "相关测试用例", "relevance": "medium"}
        ],
        "suggestions": [
            "尝试使用更具体的关键词",
            "指定产品或组件名称",
            "查看相关文档和案例"
        ],
        "timestamp": "2024-01-01T12:00:00Z"
    }

    return {"success": True, "data": mock_answer}

@app.post("/kg/qa/similar_anomalies")
async def find_similar_anomalies(request: Dict[str, Any]):
    """查找相似异常"""
    symptom = request.get("symptom", "")
    limit = request.get("limit", 5)

    if not symptom:
        raise HTTPException(status_code=400, detail="症状描述不能为空")

    # 模拟相似异常结果
    mock_similar = [
        {
            "anomaly_id": "ANO-2024-001",
            "title": "摄像头无法对焦",
            "description": "用户反馈摄像头无法正常对焦，影响拍照质量",
            "similarity_score": 0.92,
            "symptoms": ["对焦失败", "拍照模糊"],
            "root_causes": ["镜头污染", "对焦马达故障"],
            "countermeasures": ["清洁镜头", "更换对焦马达", "软件校准"]
        },
        {
            "anomaly_id": "ANO-2024-002",
            "title": "摄像头启动缓慢",
            "description": "摄像头应用启动时间过长",
            "similarity_score": 0.75,
            "symptoms": ["启动慢", "响应延迟"],
            "root_causes": ["内存不足", "处理器负载高"],
            "countermeasures": ["优化算法", "增加内存", "后台清理"]
        }
    ]

    return {"success": True, "data": mock_similar[:limit]}

@app.post("/kg/qa/extract_entities")
async def extract_entities(request: Dict[str, Any]):
    """从文本中抽取实体"""
    text = request.get("text", "")
    if not text:
        raise HTTPException(status_code=400, detail="文本不能为空")

    # 模拟实体抽取结果
    mock_entities = {
        "products": ["iPhone 15", "Galaxy S24"],
        "components": ["摄像头", "电池", "屏幕"],
        "symptoms": ["无法开机", "发热", "耗电快"],
        "actions": ["测试", "检查", "验证"]
    }

    return {"success": True, "data": mock_entities}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
