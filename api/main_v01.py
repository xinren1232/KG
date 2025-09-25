#!/usr/bin/env python3
"""
FastAPI主服务 - 基于ontology v0.1设计
技术栈：FastAPI + Neo4j Driver + Pydantic v2
"""
import os
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path

from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from neo4j import GraphDatabase

# 导入新的文档解析模块
from files.manager import new_upload, write_file, set_status, get_meta, save_preview, load_preview, FileStatus
from parsers.enhanced_excel_parser import parse_excel, detect_excel_structure, parse_excel_robust
from parsers.pdf_docx import parse_pdf, parse_docx, parse_text, detect_document_structure
from parsers.enhanced_document_parser import parse_document_enhanced
from extract.pipeline_adapter import excel_items_to_preview, text_blocks_to_preview
import uvicorn

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pydantic v2 模型定义






class ExtractRequest(BaseModel):
    file_id: str = Field(..., description="文件ID")
    extraction_type: str = Field(default="auto", description="抽取类型")

class BuildGraphRequest(BaseModel):
    entities: List[Dict[str, Any]] = Field(..., description="实体列表")
    relations: List[Dict[str, Any]] = Field(..., description="关系列表")
    merge_strategy: str = Field(default="auto", description="合并策略")

class StandardResponse(BaseModel):
    ok: bool
    data: Optional[Any] = None
    error: Optional[Dict[str, str]] = None

class ErrorResponse(BaseModel):
    ok: bool = False
    error: Dict[str, str]

# Neo4j连接管理
class Neo4jConnection:
    def __init__(self):
        self.driver = None
        self.connect()
    
    def connect(self):
        """连接Neo4j数据库"""
        try:
            uri = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
            user = os.getenv('NEO4J_USER', 'neo4j')
            password = os.getenv('NEO4J_PASS', 'password123')
            
            self.driver = GraphDatabase.driver(uri, auth=(user, password))
            
            # 验证连接
            with self.driver.session() as session:
                session.run("RETURN 1")
            
            logger.info(f"Neo4j连接成功: {uri}")
            
        except Exception as e:
            logger.error(f"Neo4j连接失败: {e}")
            self.driver = None
    
    def get_session(self):
        """获取数据库会话"""
        if not self.driver:
            raise HTTPException(
                status_code=503,
                detail={"ok": False, "error": {"code": "NEO4J_CONN", "message": "数据库连接失败"}}
            )
        return self.driver.session()
    
    def close(self):
        """关闭连接"""
        if self.driver:
            self.driver.close()

# 全局数据库连接
db = Neo4jConnection()

# FastAPI应用
app = FastAPI(
    title="质量知识图谱API",
    description="手机研发质量管理知识图谱API服务",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:5175"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 支持的文件类型
ALLOWED_EXTENSIONS = {
    '.xlsx', '.xls',           # Excel文件
    '.pdf',                    # PDF文件
    '.docx', '.doc',          # Word文档
    '.pptx', '.ppt',          # PowerPoint文档
    '.csv',                   # CSV文件
    '.txt', '.md', '.rtf'     # 文本文件
}

# 文档解析后台任务
def parse_document_task(upload_id: str):
    """后台文档解析任务"""
    try:
        logger.info(f"开始解析文档: {upload_id}")

        # 更新状态为解析中
        set_status(upload_id, FileStatus.parsing)

        # 获取文件信息
        meta = get_meta(upload_id)
        if "error" in meta:
            set_status(upload_id, FileStatus.failed, error="文件元数据不存在")
            return

        filename = meta.get("name", "")

        # 使用文件管理器的路径配置
        from files.manager import UPLOAD
        file_path = UPLOAD / upload_id

        if not file_path.exists():
            logger.error(f"文件不存在: {file_path}")
            logger.info(f"上传目录: {UPLOAD}")
            logger.info(f"上传目录存在: {UPLOAD.exists()}")
            if UPLOAD.exists():
                files = list(UPLOAD.glob("*"))
                logger.info(f"上传目录文件: {[f.name for f in files[:5]]}")
            set_status(upload_id, FileStatus.failed, error=f"文件不存在: {file_path}")
            return

        # 根据文件类型选择解析器
        file_ext = Path(filename).suffix.lower()
        logger.info(f"解析文件类型: {file_ext}")

        if file_ext in {'.xlsx', '.xls'}:
            # Excel文件解析 - 使用全面映射配置
            comprehensive_mapping = Path("api/mappings/mapping_excel_comprehensive.yaml")
            optimized_mapping = Path("api/mappings/mapping_excel_optimized.yaml")
            default_mapping = Path("api/mappings/mapping_excel_default.yaml")

            # 优先使用全面映射配置
            if comprehensive_mapping.exists():
                mapping_file = comprehensive_mapping
            elif optimized_mapping.exists():
                mapping_file = optimized_mapping
            else:
                mapping_file = default_mapping

            logger.info(f"使用映射配置: {mapping_file}")

            # 使用增强解析器获取完整结果
            parse_result = parse_excel_robust(file_path, mapping_file)

            if parse_result['success']:
                preview_data = parse_result['data']
                logger.info(f"Excel解析成功: {len(preview_data.get('raw_data', []))} 条记录, {len(preview_data.get('entities', []))} 个实体")
            else:
                logger.error(f"Excel解析失败: {parse_result.get('error')}")
                set_status(upload_id, FileStatus.failed, error=f"Excel解析失败: {parse_result.get('error')}")
                return

        elif file_ext in {'.pdf', '.docx', '.doc', '.pptx', '.ppt', '.txt', '.csv', '.md', '.rtf'}:
            # 使用统一IR解析系统
            logger.info(f"使用统一IR解析系统处理: {file_ext}, 文件路径: {file_path}")

            try:
                from parsers.ir_unified_parser import IRUnifiedParser

                # 创建统一解析器
                ir_parser = IRUnifiedParser()

                # 解析文档为IR格式
                ir_result = ir_parser.parse_document(file_path, file_ext)

                if ir_result['success']:
                    # 转换IR为旧版格式（兼容现有前端）
                    from parsers.ir_core import IRConverter
                    document_ir = ir_result['ir']
                    preview_data = IRConverter.to_legacy_format(document_ir)

                    logger.info(f"IR解析成功: {len(preview_data.get('raw_data', []))} 条记录")
                    logger.info(f"解析器信息: {ir_parser.get_parser_info(file_ext)}")
                else:
                    error_msg = ir_result.get('error', '未知错误')
                    logger.error(f"IR解析失败: {error_msg}")
                    set_status(upload_id, FileStatus.failed, error=f"IR解析失败: {error_msg}")
                    return

            except Exception as e:
                logger.error(f"IR解析器异常: {e}")
                set_status(upload_id, FileStatus.failed, error=f"IR解析器异常: {str(e)}")
                return

        else:
            set_status(upload_id, FileStatus.failed, error=f"不支持的文件类型: {file_ext}")
            return

        # 保存预览数据
        save_preview(upload_id, preview_data)

        # 更新状态为解析完成
        set_status(upload_id, FileStatus.parsed,
                  entity_count=len(preview_data.get("entities", [])),
                  relation_count=len(preview_data.get("relations", [])))

        logger.info(f"文档解析完成: {upload_id}, 实体: {len(preview_data.get('entities', []))}, 关系: {len(preview_data.get('relations', []))}")

    except Exception as e:
        logger.error(f"文档解析失败: {upload_id} - {e}")
        import traceback
        logger.error(f"详细错误信息: {traceback.format_exc()}")
        try:
            set_status(upload_id, FileStatus.failed, error=str(e))
        except Exception as status_error:
            logger.error(f"更新状态失败: {status_error}")

# 依赖注入
def get_db_session():
    """获取数据库会话依赖"""
    return db.get_session()

# API路由
@app.get("/health")
async def health_check():
    """健康检查"""
    try:
        with get_db_session() as session:
            result = session.run("RETURN 1 as test")
            result.single()
        
        return {
            "status": "healthy",
            "service": "Quality Knowledge Graph API",
            "version": "1.0.0",
            "timestamp": datetime.now().isoformat(),
            "database": "connected"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "service": "Quality Knowledge Graph API",
            "version": "1.0.0",
            "timestamp": datetime.now().isoformat(),
            "database": "disconnected",
            "error": str(e)
        }

@app.post("/kg/upload")
async def upload_file(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    """文件上传并启动解析"""
    logger.info(f"收到文件上传请求: {file.filename}")
    try:
        # 验证文件类型
        file_ext = Path(file.filename).suffix.lower()
        logger.info(f"文件类型: {file_ext}")

        if file_ext not in ALLOWED_EXTENSIONS:
            logger.warning(f"不支持的文件类型: {file_ext}")
            return {
                "success": False,
                "message": f"不支持的文件类型: {file_ext}，支持的类型: {', '.join(ALLOWED_EXTENSIONS)}"
            }

        # 创建上传记录
        upload_id = new_upload(file.filename)

        # 保存文件内容
        content = await file.read()
        write_file(upload_id, content)

        # 不再自动启动解析任务，等待用户手动触发
        # 文件上传后状态为 'uploaded'，用户需要手动点击解析

        logger.info(f"文件上传成功: {file.filename}, 大小: {len(content)} bytes, ID: {upload_id}")

        return {
            "success": True,
            "upload_id": upload_id,
            "filename": file.filename,
            "file_type": file_ext,
            "size": len(content),
            "message": "文件上传成功，正在解析中..."
        }

    except Exception as e:
        logger.error(f"文件上传失败: {e}")
        return {
            "success": False,
            "message": str(e)
        }

@app.get("/kg/files/{upload_id}/status")
async def get_file_status(upload_id: str):
    """获取文件处理状态"""
    try:
        meta = get_meta(upload_id)
        if "error" in meta:
            return {
                "success": False,
                "message": "文件不存在"
            }

        return {
            "success": True,
            "data": meta
        }

    except Exception as e:
        logger.error(f"获取文件状态失败: {e}")
        return {
            "success": False,
            "message": str(e)
        }

@app.post("/kg/files/{upload_id}/parse")
async def parse_file_manually(upload_id: str, background_tasks: BackgroundTasks):
    """手动触发文件解析"""
    try:
        # 检查文件是否存在
        meta = get_meta(upload_id)
        if "error" in meta:
            return {
                "success": False,
                "message": "文件不存在"
            }

        # 检查文件状态
        current_status = meta.get("status")
        if current_status == "parsing":
            return {
                "success": False,
                "message": "文件正在解析中，请稍候"
            }
        elif current_status == "parsed":
            return {
                "success": False,
                "message": "文件已解析完成，如需重新解析请先删除"
            }

        # 启动解析任务
        background_tasks.add_task(parse_document_task, upload_id)

        logger.info(f"手动触发文件解析: {upload_id}")

        return {
            "success": True,
            "message": "解析任务已启动",
            "upload_id": upload_id
        }

    except Exception as e:
        logger.error(f"手动解析失败: {e}")
        return {
            "success": False,
            "message": str(e)
        }

@app.get("/kg/files/{upload_id}/preview")
async def get_file_preview(upload_id: str):
    """获取文件解析预览"""
    try:
        # 检查文件状态
        meta = get_meta(upload_id)
        if "error" in meta:
            return {
                "success": False,
                "message": "文件不存在"
            }

        if meta.get("status") != FileStatus.parsed:
            return {
                "success": False,
                "message": f"文件尚未解析完成，当前状态: {meta.get('status')}"
            }

        # 获取预览数据
        preview_data = load_preview(upload_id)

        return {
            "success": True,
            "data": preview_data
        }

    except Exception as e:
        logger.error(f"获取文件预览失败: {e}")
        return {
            "success": False,
            "message": str(e)
        }

@app.post("/kg/files/{upload_id}/commit")
async def commit_to_graph(upload_id: str):
    """将解析结果提交到知识图谱"""
    try:
        # 检查文件状态
        meta = get_meta(upload_id)
        if "error" in meta:
            return {
                "success": False,
                "message": "文件不存在"
            }

        if meta.get("status") != FileStatus.parsed:
            return {
                "success": False,
                "message": f"文件尚未解析完成，当前状态: {meta.get('status')}"
            }

        # 获取预览数据
        preview_data = load_preview(upload_id)
        entities = preview_data.get("entities", [])
        relations = preview_data.get("relations", [])

        # TODO: 这里应该调用Neo4j写入逻辑
        # 目前返回模拟结果
        nodes_created = len(entities)
        relations_created = len(relations)

        # 更新状态为已提交
        set_status(upload_id, FileStatus.committed,
                  nodes_created=nodes_created,
                  relations_created=relations_created)

        return {
            "success": True,
            "data": {
                "nodes_created": nodes_created,
                "relations_created": relations_created,
                "message": "知识图谱构建完成"
            }
        }

    except Exception as e:
        logger.error(f"提交到知识图谱失败: {e}")
        return {
            "success": False,
            "message": str(e)
        }

@app.post("/kg/build")
async def build_graph(request: BuildGraphRequest):
    """构建知识图谱"""
    try:
        # 模拟图谱构建过程
        # 在实际实现中，这里会将实体和关系写入Neo4j

        nodes_created = len(request.entities)
        relations_created = len(request.relations)

        return {
            "success": True,
            "nodes_created": nodes_created,
            "relations_created": relations_created,
            "merge_strategy": request.merge_strategy,
            "message": f"图谱构建成功！创建 {nodes_created} 个节点，{relations_created} 个关系"
        }

    except Exception as e:
        logger.error(f"图谱构建失败: {e}")
        return {
            "success": False,
            "message": str(e)
        }







@app.get("/kg/dictionary", response_model=StandardResponse)
async def get_dictionary():
    """获取词典数据"""
    try:
        # 使用统一词典管理器
        from unified_dictionary_config import get_unified_dictionary
        dictionary_data = get_unified_dictionary()

        return StandardResponse(ok=True, data=dictionary_data)

    except Exception as e:
        logger.error(f"获取词典失败: {e}")
        return StandardResponse(
            ok=False,
            error={"code": "DICTIONARY_FAILED", "message": str(e)}
        )

@app.get("/kg/stats", response_model=StandardResponse)
async def get_stats():
    """获取知识图谱统计信息"""
    try:
        cypher = """
        MATCH (a:Anomaly) WITH count(a) as anomaly_count
        MATCH (p:Product) WITH anomaly_count, count(p) as product_count
        MATCH (b:Build) WITH anomaly_count, product_count, count(b) as build_count
        MATCH (c:Component) WITH anomaly_count, product_count, build_count, count(c) as component_count
        MATCH (s:Symptom) WITH anomaly_count, product_count, build_count, component_count, count(s) as symptom_count
        OPTIONAL MATCH (tc:TestCase) WITH anomaly_count, product_count, build_count, component_count, symptom_count, count(tc) as testcase_count
        RETURN anomaly_count, product_count, build_count, component_count, symptom_count, testcase_count
        """

        with get_db_session() as session:
            result = session.run(cypher)
            record = result.single()

            if record:
                stats = {
                    "anomalies": record["anomaly_count"],
                    "products": record["product_count"],
                    "builds": record["build_count"],
                    "components": record["component_count"],
                    "symptoms": record["symptom_count"],
                    "testcases": record["testcase_count"] or 0
                }
                return StandardResponse(ok=True, data=stats)
            else:
                return StandardResponse(ok=True, data={})

    except Exception as e:
        logger.error(f"获取统计信息失败: {e}")
        return StandardResponse(
            ok=False,
            error={"code": "STATS_FAILED", "message": str(e)}
        )

# 应用生命周期
@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时清理资源"""
    db.close()

if __name__ == "__main__":
    uvicorn.run(
        "main_v01:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
