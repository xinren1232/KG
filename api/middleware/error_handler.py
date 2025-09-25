#!/usr/bin/env python3
"""
错误处理中间件
统一处理应用中的异常和错误响应
"""

import logging
import traceback
from typing import Callable
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

logger = logging.getLogger(__name__)

class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """错误处理中间件"""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """处理请求并捕获异常"""
        try:
            response = await call_next(request)
            return response
        
        except ValueError as e:
            # 参数错误
            logger.warning(f"参数错误: {str(e)} - {request.url}")
            return JSONResponse(
                status_code=400,
                content={
                    "ok": False,
                    "error": {
                        "type": "value_error",
                        "message": "参数错误",
                        "details": str(e)
                    }
                }
            )
        
        except FileNotFoundError as e:
            # 文件不存在
            logger.warning(f"文件不存在: {str(e)} - {request.url}")
            return JSONResponse(
                status_code=404,
                content={
                    "ok": False,
                    "error": {
                        "type": "file_not_found",
                        "message": "文件不存在",
                        "details": str(e)
                    }
                }
            )
        
        except PermissionError as e:
            # 权限错误
            logger.warning(f"权限错误: {str(e)} - {request.url}")
            return JSONResponse(
                status_code=403,
                content={
                    "ok": False,
                    "error": {
                        "type": "permission_error",
                        "message": "权限不足",
                        "details": str(e)
                    }
                }
            )
        
        except ConnectionError as e:
            # 连接错误（如数据库连接失败）
            logger.error(f"连接错误: {str(e)} - {request.url}")
            return JSONResponse(
                status_code=503,
                content={
                    "ok": False,
                    "error": {
                        "type": "connection_error",
                        "message": "服务连接失败",
                        "details": "数据库或外部服务连接失败"
                    }
                }
            )
        
        except TimeoutError as e:
            # 超时错误
            logger.error(f"超时错误: {str(e)} - {request.url}")
            return JSONResponse(
                status_code=408,
                content={
                    "ok": False,
                    "error": {
                        "type": "timeout_error",
                        "message": "请求超时",
                        "details": str(e)
                    }
                }
            )
        
        except Exception as e:
            # 未知错误
            logger.error(f"未知错误: {str(e)} - {request.url}")
            logger.error(f"错误堆栈: {traceback.format_exc()}")
            
            return JSONResponse(
                status_code=500,
                content={
                    "ok": False,
                    "error": {
                        "type": "internal_error",
                        "message": "服务器内部错误",
                        "details": "系统发生未知错误，请联系管理员"
                    }
                }
            )
