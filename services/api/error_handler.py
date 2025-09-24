#!/usr/bin/env python3
"""
错误处理中间件
统一处理API错误和异常
"""

import logging
import traceback
import time
from typing import Dict, Any, Optional
from datetime import datetime
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import uuid

logger = logging.getLogger(__name__)

class ErrorCode:
    """错误代码常量"""
    # 通用错误
    INTERNAL_ERROR = "INTERNAL_ERROR"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    NOT_FOUND = "NOT_FOUND"
    UNAUTHORIZED = "UNAUTHORIZED"
    FORBIDDEN = "FORBIDDEN"
    
    # 业务错误
    DATABASE_ERROR = "DATABASE_ERROR"
    CACHE_ERROR = "CACHE_ERROR"
    EXTERNAL_API_ERROR = "EXTERNAL_API_ERROR"
    
    # 知识图谱相关错误
    GRAPH_CONNECTION_ERROR = "GRAPH_CONNECTION_ERROR"
    GRAPH_QUERY_ERROR = "GRAPH_QUERY_ERROR"
    DATA_IMPORT_ERROR = "DATA_IMPORT_ERROR"
    
    # 智能问答相关错误
    QA_SERVICE_ERROR = "QA_SERVICE_ERROR"
    LLM_API_ERROR = "LLM_API_ERROR"
    ENTITY_EXTRACTION_ERROR = "ENTITY_EXTRACTION_ERROR"

class APIError(Exception):
    """自定义API错误"""
    
    def __init__(self, 
                 message: str, 
                 error_code: str = ErrorCode.INTERNAL_ERROR,
                 status_code: int = 500,
                 details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(message)

class DatabaseError(APIError):
    """数据库错误"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code=ErrorCode.DATABASE_ERROR,
            status_code=500,
            details=details
        )

class GraphError(APIError):
    """图数据库错误"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code=ErrorCode.GRAPH_CONNECTION_ERROR,
            status_code=500,
            details=details
        )

class QAServiceError(APIError):
    """问答服务错误"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code=ErrorCode.QA_SERVICE_ERROR,
            status_code=500,
            details=details
        )

class ErrorResponse:
    """标准错误响应格式"""
    
    @staticmethod
    def create(
        error_code: str,
        message: str,
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None,
        request_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """创建标准错误响应"""
        return {
            "success": False,
            "error": {
                "code": error_code,
                "message": message,
                "details": details or {},
                "timestamp": datetime.now().isoformat(),
                "request_id": request_id
            }
        }

class ErrorHandler:
    """错误处理器"""
    
    def __init__(self):
        self.error_stats = {
            "total_errors": 0,
            "error_by_code": {},
            "error_by_endpoint": {},
            "last_reset": datetime.now()
        }
    
    async def handle_api_error(self, request: Request, exc: APIError) -> JSONResponse:
        """处理自定义API错误"""
        request_id = self._get_request_id(request)
        
        # 记录错误
        logger.error(
            f"API Error [{request_id}]: {exc.error_code} - {exc.message}",
            extra={
                "request_id": request_id,
                "error_code": exc.error_code,
                "status_code": exc.status_code,
                "details": exc.details,
                "path": request.url.path,
                "method": request.method
            }
        )
        
        # 更新统计
        self._update_error_stats(exc.error_code, request.url.path)
        
        # 创建响应
        response_data = ErrorResponse.create(
            error_code=exc.error_code,
            message=exc.message,
            status_code=exc.status_code,
            details=exc.details,
            request_id=request_id
        )
        
        return JSONResponse(
            status_code=exc.status_code,
            content=response_data
        )
    
    async def handle_http_exception(self, request: Request, exc: HTTPException) -> JSONResponse:
        """处理HTTP异常"""
        request_id = self._get_request_id(request)
        
        # 映射HTTP状态码到错误代码
        error_code_map = {
            400: ErrorCode.VALIDATION_ERROR,
            401: ErrorCode.UNAUTHORIZED,
            403: ErrorCode.FORBIDDEN,
            404: ErrorCode.NOT_FOUND,
            500: ErrorCode.INTERNAL_ERROR
        }
        
        error_code = error_code_map.get(exc.status_code, ErrorCode.INTERNAL_ERROR)
        
        logger.warning(
            f"HTTP Exception [{request_id}]: {exc.status_code} - {exc.detail}",
            extra={
                "request_id": request_id,
                "status_code": exc.status_code,
                "path": request.url.path,
                "method": request.method
            }
        )
        
        self._update_error_stats(error_code, request.url.path)
        
        response_data = ErrorResponse.create(
            error_code=error_code,
            message=str(exc.detail),
            status_code=exc.status_code,
            request_id=request_id
        )
        
        return JSONResponse(
            status_code=exc.status_code,
            content=response_data
        )
    
    async def handle_validation_error(self, request: Request, exc: RequestValidationError) -> JSONResponse:
        """处理验证错误"""
        request_id = self._get_request_id(request)
        
        # 格式化验证错误
        validation_errors = []
        for error in exc.errors():
            validation_errors.append({
                "field": ".".join(str(loc) for loc in error["loc"]),
                "message": error["msg"],
                "type": error["type"]
            })
        
        logger.warning(
            f"Validation Error [{request_id}]: {len(validation_errors)} validation errors",
            extra={
                "request_id": request_id,
                "validation_errors": validation_errors,
                "path": request.url.path,
                "method": request.method
            }
        )
        
        self._update_error_stats(ErrorCode.VALIDATION_ERROR, request.url.path)
        
        response_data = ErrorResponse.create(
            error_code=ErrorCode.VALIDATION_ERROR,
            message="请求参数验证失败",
            status_code=422,
            details={"validation_errors": validation_errors},
            request_id=request_id
        )
        
        return JSONResponse(
            status_code=422,
            content=response_data
        )
    
    async def handle_general_exception(self, request: Request, exc: Exception) -> JSONResponse:
        """处理通用异常"""
        request_id = self._get_request_id(request)
        
        # 记录详细错误信息
        logger.error(
            f"Unhandled Exception [{request_id}]: {type(exc).__name__} - {str(exc)}",
            extra={
                "request_id": request_id,
                "exception_type": type(exc).__name__,
                "traceback": traceback.format_exc(),
                "path": request.url.path,
                "method": request.method
            }
        )
        
        self._update_error_stats(ErrorCode.INTERNAL_ERROR, request.url.path)
        
        # 在生产环境中隐藏详细错误信息
        message = "服务器内部错误，请稍后重试"
        details = {}
        
        # 在开发环境中显示详细错误信息
        import os
        if os.getenv("DEBUG", "false").lower() == "true":
            message = str(exc)
            details = {
                "exception_type": type(exc).__name__,
                "traceback": traceback.format_exc().split('\n')
            }
        
        response_data = ErrorResponse.create(
            error_code=ErrorCode.INTERNAL_ERROR,
            message=message,
            status_code=500,
            details=details,
            request_id=request_id
        )
        
        return JSONResponse(
            status_code=500,
            content=response_data
        )
    
    def _get_request_id(self, request: Request) -> str:
        """获取或生成请求ID"""
        # 尝试从请求头获取
        request_id = request.headers.get("X-Request-ID")
        if not request_id:
            # 生成新的请求ID
            request_id = str(uuid.uuid4())
        return request_id
    
    def _update_error_stats(self, error_code: str, endpoint: str):
        """更新错误统计"""
        self.error_stats["total_errors"] += 1
        
        # 按错误代码统计
        if error_code not in self.error_stats["error_by_code"]:
            self.error_stats["error_by_code"][error_code] = 0
        self.error_stats["error_by_code"][error_code] += 1
        
        # 按端点统计
        if endpoint not in self.error_stats["error_by_endpoint"]:
            self.error_stats["error_by_endpoint"][endpoint] = 0
        self.error_stats["error_by_endpoint"][endpoint] += 1
    
    def get_error_stats(self) -> Dict[str, Any]:
        """获取错误统计"""
        return {
            **self.error_stats,
            "uptime_hours": (datetime.now() - self.error_stats["last_reset"]).total_seconds() / 3600
        }
    
    def reset_error_stats(self):
        """重置错误统计"""
        self.error_stats = {
            "total_errors": 0,
            "error_by_code": {},
            "error_by_endpoint": {},
            "last_reset": datetime.now()
        }

# 创建全局错误处理器实例
error_handler = ErrorHandler()

# 便捷函数
def raise_database_error(message: str, details: Optional[Dict[str, Any]] = None):
    """抛出数据库错误"""
    raise DatabaseError(message, details)

def raise_graph_error(message: str, details: Optional[Dict[str, Any]] = None):
    """抛出图数据库错误"""
    raise GraphError(message, details)

def raise_qa_error(message: str, details: Optional[Dict[str, Any]] = None):
    """抛出问答服务错误"""
    raise QAServiceError(message, details)

def raise_validation_error(message: str, field: str = None):
    """抛出验证错误"""
    details = {"field": field} if field else {}
    raise APIError(
        message=message,
        error_code=ErrorCode.VALIDATION_ERROR,
        status_code=400,
        details=details
    )

def raise_not_found_error(resource: str, identifier: str = None):
    """抛出资源不存在错误"""
    message = f"{resource}不存在"
    if identifier:
        message += f": {identifier}"
    
    raise APIError(
        message=message,
        error_code=ErrorCode.NOT_FOUND,
        status_code=404,
        details={"resource": resource, "identifier": identifier}
    )
