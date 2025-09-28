from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional, Dict, Any
from database.neo4j_client import Neo4jClient
from models.schemas import (
    FlowQueryRequest, FlowQueryResponse,
    CausePathQueryRequest, CausePathResponse,
    AnomalyUpsertRequest, ApiResponse,
    ProductListResponse, ComponentListResponse,
    GraphDataResponse, TestCase, CausePath,
    Product, Component
)
from dependencies import get_neo4j_client
from datetime import datetime

def get_dictionary_stats():
    """获取词典数据统计"""
    import json
    from pathlib import Path
    from collections import Counter

    try:
        # 读取词典数据
        dict_path = Path("../../api/data/dictionary.json")
        if not dict_path.exists():
            current_file = Path(__file__)
            project_root = current_file.parent.parent.parent
            dict_path = project_root / "api" / "data" / "dictionary.json"

        with open(dict_path, 'r', encoding='utf-8') as f:
            all_entries = json.load(f)

        # 统计分类
        categories = Counter(entry.get('category', 'Unknown') for entry in all_entries)

        # 统计标签
        all_tags = set()
        for entry in all_entries:
            tags = entry.get('tags', [])
            if isinstance(tags, list):
                all_tags.update(tags)
            elif isinstance(tags, str):
                all_tags.update(tags.split())

        return {
            'total_entries': len(all_entries),
            'total_categories': len(categories),
            'total_tags': len(all_tags),
            'categories': dict(categories)
        }
    except Exception as e:
        return {
            'total_entries': 0,
            'total_categories': 0,
            'total_tags': 0,
            'categories': {}
        }

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

@router.get("/graph")
async def get_graph_data(
    limit: int = Query(default=100, ge=1, le=2000, description="返回节点数量限制"),
    show_all: bool = Query(default=False, description="是否显示所有节点（忽略limit限制）"),
    neo4j_client: Neo4jClient = Depends(get_neo4j_client)
):
    """获取知识图谱可视化数据"""
    try:
        # 如果show_all为True，获取所有节点，否则使用limit限制
        actual_limit = None if show_all else limit
        graph_data = neo4j_client.get_graph_data(actual_limit or 1000)

        # 获取全局统计数据（不受limit限制）
        global_stats = neo4j_client.get_global_stats()

        # 获取词典数据统计
        dict_stats = get_dictionary_stats()

        # 转换为前端期望的格式
        nodes = []
        for node in graph_data['nodes']:
            nodes.append({
                'id': str(node['id']),
                'name': node['name'],
                'category': node['label'],
                'description': node['properties'].get('description', ''),
                'symbolSize': 30,
                'properties': node['properties']
            })

        relationships = []
        for edge in graph_data['edges']:
            relationships.append({
                'source': str(edge['source']),
                'target': str(edge['target']),
                'type': edge['relationship']
            })

        # 生成统计信息
        categories = {}
        for node in nodes:
            cat = node['category']
            categories[cat] = categories.get(cat, 0) + 1

        result = {
            'success': True,
            'data': {
                'stats': {
                    'totalNodes': dict_stats['total_entries'],  # 使用词典条目数作为"词条条目"
                    'totalRelations': global_stats['total_relations'],  # 使用图谱关系数
                    'totalCategories': dict_stats['total_categories'],  # 使用词典分类数
                    'totalTags': dict_stats['total_tags']  # 使用词典标签数
                },
                'categories': [{'name': k, 'count': v} for k, v in categories.items()],
                'tags': [],
                'nodes': nodes,
                'relations': relationships,
                'sampleNodes': nodes[:50],  # 限制显示数量
                'sampleRelations': relationships[:100]
            }
        }

        return result
    except Exception as e:
        return {
            'success': False,
            'message': f"获取图谱数据失败: {str(e)}",
            'data': {
                'stats': {'totalNodes': 0, 'totalRelations': 0, 'totalCategories': 0, 'totalTags': 0},
                'categories': [],
                'tags': [],
                'nodes': [],
                'relations': [],
                'sampleNodes': [],
                'sampleRelations': []
            }
        }

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

@router.get("/stats")
async def get_graph_stats(neo4j_client: Neo4jClient = Depends(get_neo4j_client)):
    """获取图谱统计信息"""
    try:
        # 获取节点统计
        node_query = """
        MATCH (n)
        RETURN labels(n)[0] as label, count(n) as count
        ORDER BY count DESC
        """
        node_stats = neo4j_client.execute_query(node_query)

        # 获取关系统计
        rel_query = """
        MATCH ()-[r]->()
        RETURN type(r) as type, count(r) as count
        ORDER BY count DESC
        """
        rel_stats = neo4j_client.execute_query(rel_query)

        # 计算总数
        total_nodes = sum(stat['count'] for stat in node_stats)
        total_relations = sum(stat['count'] for stat in rel_stats)

        return {
            "success": True,
            "data": {
                "nodes": {
                    "total": total_nodes,
                    "by_type": node_stats
                },
                "relationships": {
                    "total": total_relations,
                    "by_type": rel_stats
                },
                "last_updated": datetime.now().isoformat()
            }
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"获取统计信息失败: {str(e)}",
            "data": {"nodes": {"total": 0, "by_type": []}, "relationships": {"total": 0, "by_type": []}}
        }

@router.get("/files")
async def get_files():
    """获取已上传文件列表"""
    # 返回示例文件列表
    files = [
        {
            "id": "file_001",
            "name": "硬件质量报告.pdf",
            "size": 1024000,
            "upload_time": "2025-09-27T10:00:00Z",
            "status": "processed",
            "type": "pdf"
        },
        {
            "id": "file_002",
            "name": "异常案例集.docx",
            "size": 512000,
            "upload_time": "2025-09-27T09:30:00Z",
            "status": "processing",
            "type": "docx"
        }
    ]

    return {
        "success": True,
        "data": files,
        "total": len(files)
    }

@router.get("/dictionary/entries")
async def get_dictionary_entries(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=10000),
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None)
):
    """获取词典条目"""
    import json
    import os
    from pathlib import Path

    try:
        # 读取完整的词典数据 - 1124条真实业务术语
        # API服务运行在services/api目录，需要向上两级到项目根目录
        dict_path = Path("../../api/data/dictionary.json")
        if not dict_path.exists():
            # 备用路径：使用绝对路径计算
            current_file = Path(__file__)
            project_root = current_file.parent.parent.parent
            dict_path = project_root / "api" / "data" / "dictionary.json"

        with open(dict_path, 'r', encoding='utf-8') as f:
            all_entries = json.load(f)

        # 转换为前端期望的格式
        formatted_entries = []
        for i, entry in enumerate(all_entries):
            # 映射分类名称为中文
            category_mapping = {
                "Symptom": "症状",
                "Component": "组件",
                "Tool": "工具",
                "Process": "流程",
                "TestCase": "测试用例",
                "Metric": "指标",
                "Role": "角色",
                "Material": "材料"
            }

            formatted_entries.append({
                "id": f"entry_{i+1:04d}",
                "term": entry.get("term", ""),
                "definition": entry.get("description", ""),
                "category": category_mapping.get(entry.get("category", ""), entry.get("category", "其他")),
                "aliases": entry.get("aliases", []),
                "tags": entry.get("tags", []),
                "created_at": entry.get("created_at", "2025-09-27T10:00:00Z"),
                "updated_at": entry.get("updated_at", "2025-09-27T10:00:00Z"),
                "source": entry.get("source", "业务词典"),
                "sub_category": entry.get("sub_category", ""),
                "status": entry.get("status", "active"),
                "original_category": entry.get("original_category", "")
            })

        # 应用搜索过滤
        if search:
            search_lower = search.lower()
            formatted_entries = [
                e for e in formatted_entries
                if search_lower in e['term'].lower() or
                   search_lower in e['definition'].lower() or
                   any(search_lower in alias.lower() for alias in e['aliases'])
            ]

        # 应用分类过滤
        if category:
            formatted_entries = [e for e in formatted_entries if e['category'] == category]

        # 获取所有分类
        all_categories = {e['category'] for e in formatted_entries}

        # 分页
        total_entries = len(formatted_entries)
        start = (page - 1) * size
        end = start + size
        page_entries = formatted_entries[start:end]

        return {
            "success": True,
            "data": {
                "entries": page_entries,
                "pagination": {
                    "page": page,
                    "size": size,
                    "total": total_entries,
                    "pages": (total_entries + size - 1) // size
                },
                "categories": sorted(list(all_categories)),
                "total_tags": len({tag for entry in formatted_entries for tag in entry['tags'] if tag})
            }
        }

    except Exception as e:
        # 如果读取文件失败，返回空数据
        return {
            "success": False,
            "message": f"读取词典数据失败: {str(e)}",
            "data": {
                "entries": [],
                "pagination": {"page": page, "size": size, "total": 0, "pages": 0},
                "categories": [],
                "total_tags": 0
            }
        }
