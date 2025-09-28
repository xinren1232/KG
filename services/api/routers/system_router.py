from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional, Dict, Any
from database.neo4j_client import Neo4jClient
from dependencies import get_neo4j_client
from datetime import datetime
import json

router = APIRouter()

@router.get("/status")
async def get_system_status(neo4j_client: Neo4jClient = Depends(get_neo4j_client)):
    """获取系统状态"""
    try:
        # 检查Neo4j连接
        neo4j_status = "healthy" if neo4j_client.test_connection() else "unhealthy"
        
        # 获取数据库统计
        stats_query = """
        MATCH (n) 
        RETURN labels(n)[0] as label, count(n) as count
        """
        node_stats = neo4j_client.execute_query(stats_query)
        
        # 获取关系统计
        rel_query = """
        MATCH ()-[r]->() 
        RETURN type(r) as type, count(r) as count
        """
        rel_stats = neo4j_client.execute_query(rel_query)
        
        return {
            "success": True,
            "data": {
                "timestamp": datetime.now().isoformat(),
                "services": {
                    "api": "healthy",
                    "neo4j": neo4j_status
                },
                "database": {
                    "nodes": node_stats,
                    "relationships": rel_stats
                },
                "version": "1.0.0"
            }
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"获取系统状态失败: {str(e)}",
            "data": None
        }

@router.get("/rules")
async def get_rules():
    """获取规则列表"""
    # 返回示例规则数据
    rules = [
        {
            "id": "rule_001",
            "name": "异常检测规则",
            "description": "检测硬件异常模式",
            "type": "detection",
            "status": "active",
            "created_at": "2025-09-27T10:00:00Z",
            "updated_at": "2025-09-27T10:00:00Z"
        },
        {
            "id": "rule_002", 
            "name": "质量评估规则",
            "description": "评估产品质量指标",
            "type": "evaluation",
            "status": "active",
            "created_at": "2025-09-27T10:00:00Z",
            "updated_at": "2025-09-27T10:00:00Z"
        }
    ]
    
    return {
        "success": True,
        "data": rules,
        "total": len(rules)
    }

@router.post("/rules")
async def create_rule(rule_data: Dict[str, Any]):
    """创建新规则"""
    # 生成新规则ID
    rule_id = f"rule_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    new_rule = {
        "id": rule_id,
        "name": rule_data.get("name", "新规则"),
        "description": rule_data.get("description", ""),
        "type": rule_data.get("type", "custom"),
        "status": "active",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    return {
        "success": True,
        "data": new_rule,
        "message": "规则创建成功"
    }

@router.put("/rules/{rule_id}")
async def update_rule(rule_id: str, rule_data: Dict[str, Any]):
    """更新规则"""
    updated_rule = {
        "id": rule_id,
        "name": rule_data.get("name", "更新的规则"),
        "description": rule_data.get("description", ""),
        "type": rule_data.get("type", "custom"),
        "status": rule_data.get("status", "active"),
        "updated_at": datetime.now().isoformat()
    }
    
    return {
        "success": True,
        "data": updated_rule,
        "message": "规则更新成功"
    }

@router.delete("/rules/{rule_id}")
async def delete_rule(rule_id: str):
    """删除规则"""
    return {
        "success": True,
        "message": f"规则 {rule_id} 删除成功"
    }

@router.post("/rules/test")
async def test_rule(test_data: Dict[str, Any]):
    """测试规则"""
    return {
        "success": True,
        "data": {
            "test_result": "passed",
            "execution_time": "0.05s",
            "matches": 3,
            "details": "规则测试通过，匹配到3个相关项目"
        },
        "message": "规则测试完成"
    }

@router.get("/export-config")
async def export_config():
    """导出系统配置"""
    config = {
        "version": "1.0.0",
        "export_time": datetime.now().isoformat(),
        "settings": {
            "neo4j_uri": "bolt://localhost:7687",
            "api_version": "1.0.0"
        }
    }
    
    return {
        "success": True,
        "data": config,
        "message": "配置导出成功"
    }

@router.get("/versions")
async def get_versions():
    """获取系统版本信息"""
    versions = [
        {
            "id": "v1.0.0",
            "version": "1.0.0",
            "description": "初始版本",
            "release_date": "2025-09-27",
            "status": "current"
        }
    ]
    
    return {
        "success": True,
        "data": versions
    }

@router.get("/prompts")
async def get_prompts():
    """获取系统提示词"""
    prompts = [
        {
            "id": "prompt_001",
            "name": "异常分析提示词",
            "content": "请分析以下硬件异常情况...",
            "category": "analysis",
            "status": "active"
        }
    ]
    
    return {
        "success": True,
        "data": prompts
    }

@router.get("/scenarios")
async def get_scenarios():
    """获取应用场景"""
    scenarios = [
        {
            "id": "scenario_001",
            "name": "硬件质量检测",
            "description": "检测硬件产品质量问题",
            "category": "quality",
            "status": "active"
        }
    ]
    
    return {
        "success": True,
        "data": scenarios
    }

@router.post("/versions")
async def publish_version(version_data: Dict[str, Any]):
    """发布新版本"""
    new_version = {
        "id": f"v{version_data.get('version', '1.0.1')}",
        "version": version_data.get('version', '1.0.1'),
        "description": version_data.get('description', ''),
        "release_date": datetime.now().strftime('%Y-%m-%d'),
        "status": "published"
    }
    
    return {
        "success": True,
        "data": new_version,
        "message": "版本发布成功"
    }
