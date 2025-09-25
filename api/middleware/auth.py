#!/usr/bin/env python3
"""
认证中间件
处理API访问认证和授权
"""

import os
import jwt
import logging
from typing import Callable, Optional
from fastapi import Request, Response, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

logger = logging.getLogger(__name__)

class AuthMiddleware(BaseHTTPMiddleware):
    """认证中间件"""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.jwt_secret = os.getenv("JWT_SECRET_KEY", "your_jwt_secret_key_here")
        self.jwt_algorithm = os.getenv("JWT_ALGORITHM", "HS256")
        self.api_key = os.getenv("API_KEY")
        
        # 不需要认证的路径
        self.public_paths = {
            "/health",
            "/docs",
            "/redoc",
            "/openapi.json",
            "/favicon.ico"
        }
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """处理认证"""
        path = request.url.path
        
        # 检查是否为公开路径
        if path in self.public_paths or path.startswith("/static"):
            return await call_next(request)
        
        # 检查认证
        auth_result = await self._authenticate(request)
        if not auth_result["success"]:
            return JSONResponse(
                status_code=401,
                content={
                    "ok": False,
                    "error": {
                        "type": "authentication_error",
                        "message": auth_result["message"]
                    }
                }
            )
        
        # 将用户信息添加到请求中
        request.state.user = auth_result.get("user")
        
        return await call_next(request)
    
    async def _authenticate(self, request: Request) -> dict:
        """执行认证检查"""
        
        # 方法1: API Key认证
        api_key = request.headers.get("X-API-Key")
        if api_key:
            if self.api_key and api_key == self.api_key:
                return {
                    "success": True,
                    "user": {"type": "api_key", "id": "api_user"}
                }
            else:
                return {
                    "success": False,
                    "message": "无效的API密钥"
                }
        
        # 方法2: JWT Token认证
        authorization = request.headers.get("Authorization")
        if authorization:
            try:
                # 提取Bearer token
                if not authorization.startswith("Bearer "):
                    return {
                        "success": False,
                        "message": "无效的认证格式，应使用Bearer token"
                    }
                
                token = authorization.split(" ")[1]
                
                # 验证JWT token
                payload = jwt.decode(
                    token,
                    self.jwt_secret,
                    algorithms=[self.jwt_algorithm]
                )
                
                return {
                    "success": True,
                    "user": {
                        "type": "jwt",
                        "id": payload.get("user_id"),
                        "username": payload.get("username"),
                        "roles": payload.get("roles", [])
                    }
                }
                
            except jwt.ExpiredSignatureError:
                return {
                    "success": False,
                    "message": "Token已过期"
                }
            except jwt.InvalidTokenError:
                return {
                    "success": False,
                    "message": "无效的Token"
                }
        
        # 如果没有配置认证，则允许访问（开发模式）
        if not self.api_key and not self.jwt_secret:
            logger.warning("未配置认证密钥，允许匿名访问")
            return {
                "success": True,
                "user": {"type": "anonymous", "id": "anonymous"}
            }
        
        return {
            "success": False,
            "message": "缺少认证信息"
        }

# 认证依赖函数
def get_current_user(request: Request) -> Optional[dict]:
    """获取当前用户信息"""
    return getattr(request.state, "user", None)

def require_auth(request: Request) -> dict:
    """要求认证的依赖"""
    user = get_current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="需要认证")
    return user

def require_role(required_role: str):
    """要求特定角色的依赖"""
    def _require_role(request: Request) -> dict:
        user = require_auth(request)
        user_roles = user.get("roles", [])
        if required_role not in user_roles:
            raise HTTPException(status_code=403, detail=f"需要{required_role}角色")
        return user
    return _require_role
