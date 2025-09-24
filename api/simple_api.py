#!/usr/bin/env python3
"""
简化版知识图谱API - 用于测试
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import json
from datetime import datetime

app = FastAPI(
    title="知识图谱简化API",
    description="用于测试的简化版API",
    version="1.0.0"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DictionaryEntry(BaseModel):
    """词典条目"""
    id: str
    term: str
    category: str
    aliases: List[str]
    definition: str
    metadata: Dict[str, Any]

class DictionaryResponse(BaseModel):
    """词典响应"""
    success: bool
    entries: List[DictionaryEntry]
    total_count: int

@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "service": "Knowledge Graph Simple API",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

@app.get("/kg/dictionary", response_model=DictionaryResponse)
async def get_dictionary(category: Optional[str] = None):
    """获取词典"""
    # 模拟词典数据
    sample_entries = [
        {
            "id": "dict_001",
            "term": "摄像头",
            "category": "组件",
            "aliases": ["相机", "Camera"],
            "definition": "用于拍照和录像的光学设备",
            "metadata": {"frequency": "高", "domain": "硬件"}
        },
        {
            "id": "dict_002",
            "term": "对焦失败",
            "category": "异常",
            "aliases": ["无法对焦", "对焦异常"],
            "definition": "摄像头无法正确对焦的故障现象",
            "metadata": {"severity": "S1", "domain": "质量"}
        },
        {
            "id": "dict_003",
            "term": "电池",
            "category": "组件",
            "aliases": ["电芯", "Battery"],
            "definition": "为设备提供电力的组件",
            "metadata": {"frequency": "高", "domain": "硬件"}
        }
    ]
    
    entries = sample_entries
    if category:
        entries = [e for e in sample_entries if e["category"] == category]
    
    return DictionaryResponse(
        success=True,
        entries=[DictionaryEntry(**entry) for entry in entries],
        total_count=len(entries)
    )

@app.get("/kg/stats")
async def get_statistics():
    """获取统计信息"""
    return {
        "success": True,
        "stats": {
            "uploaded_files": 5,
            "extracted_files": 3,
            "total_nodes": 1250,
            "total_edges": 3420,
            "dictionary_entries": 156
        },
        "timestamp": datetime.now().isoformat()
    }

@app.get("/kg/graph/data")
async def get_graph_data():
    """获取图谱数据"""
    return {
        "success": True,
        "data": {
            "nodes": [
                {"id": "node1", "name": "摄像头", "type": "Component"},
                {"id": "node2", "name": "对焦失败", "type": "Anomaly"}
            ],
            "edges": [
                {"source": "node1", "target": "node2", "type": "HAS_ANOMALY"}
            ],
            "stats": {"total_nodes": 2, "total_edges": 1}
        },
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
