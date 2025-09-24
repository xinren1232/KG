from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from database.neo4j_client import Neo4jClient
from models.schemas import (
    FlowQueryRequest, FlowQueryResponse,
    CausePathQueryRequest, CausePathResponse,
    AnomalyUpsertRequest, ApiResponse,
    ProductListResponse, ComponentListResponse,
    GraphDataResponse, TestCase, CausePath,
    Product, Component
)
from main import get_neo4j_client

router = APIRouter()

@router.get("/products", response_model=ProductListResponse)
async def get_products(neo4j_client: Neo4jClient = Depends(get_neo4j_client)):
    """获取所有产品列表"""
    try:
        products_data = neo4j_client.get_products()
        products = [Product(**product) for product in products_data]
        return ProductListResponse(data=products)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取产品列表失败: {str(e)}")

@router.get("/products/{product_name}/components", response_model=ComponentListResponse)
async def get_components(
    product_name: str,
    neo4j_client: Neo4jClient = Depends(get_neo4j_client)
):
    """获取指定产品的组件列表"""
    try:
        components_data = neo4j_client.get_components_by_product(product_name)
        components = [Component(**component) for component in components_data]
        return ComponentListResponse(data=components)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取组件列表失败: {str(e)}")

@router.post("/query/flow", response_model=FlowQueryResponse)
async def query_test_flow(
    request: FlowQueryRequest,
    neo4j_client: Neo4jClient = Depends(get_neo4j_client)
):
    """查询测试流程和用例"""
    try:
        if request.component_name:
            # 查询特定组件的测试用例
            test_cases_data = neo4j_client.get_test_cases_by_component(
                request.product_name, 
                request.component_name
            )
        else:
            # 查询产品所有组件的测试用例
            query = """
            MATCH (p:Product {name: $product_name})-[:HAS_COMPONENT]->(c:Component)
            MATCH (c)<-[:TESTS]-(tc:TestCase)
            RETURN tc.id as id, tc.title as title, tc.description as description,
                   tc.priority as priority, tc.type as type, tc.steps as steps,
                   tc.expected_result as expected_result, c.name as component_name
            ORDER BY tc.priority DESC, tc.id
            """
            test_cases_data = neo4j_client.execute_query(query, {"product_name": request.product_name})
        
        test_cases = [TestCase(**tc) for tc in test_cases_data]
        return FlowQueryResponse(
            data=test_cases,
            message=f"找到 {len(test_cases)} 个测试用例"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询测试流程失败: {str(e)}")

@router.post("/query/cause_path", response_model=CausePathResponse)
async def query_cause_path(
    request: CausePathQueryRequest,
    neo4j_client: Neo4jClient = Depends(get_neo4j_client)
):
    """查询异常因果路径"""
    try:
        cause_paths_data = neo4j_client.get_anomaly_cause_path(request.symptom_description)
        cause_paths = [CausePath(**cp) for cp in cause_paths_data]
        return CausePathResponse(
            data=cause_paths,
            message=f"找到 {len(cause_paths)} 个相关异常"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询因果路径失败: {str(e)}")

@router.post("/upsert/anomaly", response_model=ApiResponse)
async def upsert_anomaly(
    request: AnomalyUpsertRequest,
    neo4j_client: Neo4jClient = Depends(get_neo4j_client)
):
    """创建或更新异常记录"""
    try:
        anomaly_data = request.dict()
        result = neo4j_client.upsert_anomaly(anomaly_data)
        return ApiResponse(
            data=result,
            message=f"异常记录 {result['id']} 操作成功"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"异常记录操作失败: {str(e)}")

@router.get("/graph", response_model=GraphDataResponse)
async def get_graph_data(
    limit: int = Query(default=100, ge=1, le=500, description="返回节点数量限制"),
    neo4j_client: Neo4jClient = Depends(get_neo4j_client)
):
    """获取知识图谱可视化数据"""
    try:
        graph_data = neo4j_client.get_graph_data(limit)
        return GraphDataResponse(
            data=graph_data,
            message=f"获取到 {len(graph_data['nodes'])} 个节点，{len(graph_data['edges'])} 条关系"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取图谱数据失败: {str(e)}")

@router.get("/query/similar")
async def query_similar_anomalies(
    anomaly_id: str = Query(..., description="异常ID"),
    neo4j_client: Neo4jClient = Depends(get_neo4j_client)
):
    """查询相似异常（预留接口）"""
    try:
        # 这里可以实现相似异常查询逻辑
        # 目前返回基于组件的相似异常
        query = """
        MATCH (a1:Anomaly {id: $anomaly_id})-[:OCCURS_IN]->(c:Component)<-[:OCCURS_IN]-(a2:Anomaly)
        WHERE a1 <> a2
        RETURN a2.id as id, a2.title as title, a2.description as description,
               a2.severity as severity, a2.status as status, c.name as component
        ORDER BY a2.severity DESC
        LIMIT 10
        """
        similar_anomalies = neo4j_client.execute_query(query, {"anomaly_id": anomaly_id})
        return ApiResponse(
            data=similar_anomalies,
            message=f"找到 {len(similar_anomalies)} 个相似异常"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询相似异常失败: {str(e)}")
