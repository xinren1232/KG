#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Redis缓存管理器 - 提供高性能缓存服务
"""

import json
import logging
import asyncio
from typing import Any, Optional, Union, Dict
from datetime import datetime, timedelta
import redis.asyncio as redis
import pickle
import hashlib
from functools import wraps
import os

logger = logging.getLogger(__name__)

class RedisManager:
    """Redis缓存管理器"""
    
    def __init__(self):
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        self.redis_client: Optional[redis.Redis] = None
        self.default_ttl = 3600  # 默认1小时过期
        
    async def connect(self):
        """连接Redis"""
        try:
            self.redis_client = redis.from_url(
                self.redis_url,
                encoding="utf-8",
                decode_responses=False,  # 使用bytes以支持pickle
                max_connections=20
            )
            # 测试连接
            await self.redis_client.ping()
            logger.info("Redis连接成功")
        except Exception as e:
            logger.error(f"Redis连接失败: {e}")
            self.redis_client = None
    
    async def disconnect(self):
        """断开Redis连接"""
        if self.redis_client:
            await self.redis_client.close()
            logger.info("Redis连接已关闭")
    
    def _generate_key(self, prefix: str, *args, **kwargs) -> str:
        """生成缓存键"""
        # 创建唯一键
        key_data = f"{prefix}:{args}:{sorted(kwargs.items())}"
        key_hash = hashlib.md5(key_data.encode()).hexdigest()
        return f"kg:{prefix}:{key_hash}"
    
    async def get(self, key: str) -> Optional[Any]:
        """获取缓存值"""
        if not self.redis_client:
            return None
        
        try:
            value = await self.redis_client.get(key)
            if value:
                return pickle.loads(value)
            return None
        except Exception as e:
            logger.error(f"Redis获取失败 {key}: {e}")
            return None
    
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """设置缓存值"""
        if not self.redis_client:
            return False
        
        try:
            ttl = ttl or self.default_ttl
            serialized_value = pickle.dumps(value)
            await self.redis_client.setex(key, ttl, serialized_value)
            return True
        except Exception as e:
            logger.error(f"Redis设置失败 {key}: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """删除缓存"""
        if not self.redis_client:
            return False
        
        try:
            await self.redis_client.delete(key)
            return True
        except Exception as e:
            logger.error(f"Redis删除失败 {key}: {e}")
            return False
    
    async def exists(self, key: str) -> bool:
        """检查键是否存在"""
        if not self.redis_client:
            return False
        
        try:
            return await self.redis_client.exists(key) > 0
        except Exception as e:
            logger.error(f"Redis检查失败 {key}: {e}")
            return False
    
    async def clear_pattern(self, pattern: str) -> int:
        """清除匹配模式的所有键"""
        if not self.redis_client:
            return 0
        
        try:
            keys = await self.redis_client.keys(pattern)
            if keys:
                return await self.redis_client.delete(*keys)
            return 0
        except Exception as e:
            logger.error(f"Redis清除模式失败 {pattern}: {e}")
            return 0
    
    async def get_stats(self) -> Dict[str, Any]:
        """获取Redis统计信息"""
        if not self.redis_client:
            return {}
        
        try:
            info = await self.redis_client.info()
            return {
                "connected_clients": info.get("connected_clients", 0),
                "used_memory": info.get("used_memory_human", "0B"),
                "total_commands_processed": info.get("total_commands_processed", 0),
                "keyspace_hits": info.get("keyspace_hits", 0),
                "keyspace_misses": info.get("keyspace_misses", 0),
                "hit_rate": self._calculate_hit_rate(
                    info.get("keyspace_hits", 0),
                    info.get("keyspace_misses", 0)
                )
            }
        except Exception as e:
            logger.error(f"获取Redis统计失败: {e}")
            return {}
    
    def _calculate_hit_rate(self, hits: int, misses: int) -> float:
        """计算缓存命中率"""
        total = hits + misses
        if total == 0:
            return 0.0
        return round((hits / total) * 100, 2)

# 全局Redis管理器实例
redis_manager = RedisManager()

def cache_result(prefix: str, ttl: Optional[int] = None):
    """缓存装饰器"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 生成缓存键
            cache_key = redis_manager._generate_key(prefix, *args, **kwargs)
            
            # 尝试从缓存获取
            cached_result = await redis_manager.get(cache_key)
            if cached_result is not None:
                logger.debug(f"缓存命中: {cache_key}")
                return cached_result
            
            # 执行函数
            result = await func(*args, **kwargs)
            
            # 缓存结果
            if result is not None:
                await redis_manager.set(cache_key, result, ttl)
                logger.debug(f"缓存设置: {cache_key}")
            
            return result
        return wrapper
    return decorator

class QueryCache:
    """查询缓存管理"""
    
    @staticmethod
    async def get_entity_by_id(entity_id: str) -> Optional[Dict]:
        """获取实体缓存"""
        key = redis_manager._generate_key("entity", entity_id)
        return await redis_manager.get(key)
    
    @staticmethod
    async def set_entity_by_id(entity_id: str, entity_data: Dict, ttl: int = 1800):
        """设置实体缓存 (30分钟)"""
        key = redis_manager._generate_key("entity", entity_id)
        await redis_manager.set(key, entity_data, ttl)
    
    @staticmethod
    async def get_search_results(query: str, filters: Dict = None) -> Optional[Dict]:
        """获取搜索结果缓存"""
        key = redis_manager._generate_key("search", query, filters or {})
        return await redis_manager.get(key)
    
    @staticmethod
    async def set_search_results(query: str, results: Dict, filters: Dict = None, ttl: int = 600):
        """设置搜索结果缓存 (10分钟)"""
        key = redis_manager._generate_key("search", query, filters or {})
        await redis_manager.set(key, results, ttl)
    
    @staticmethod
    async def get_graph_data(node_id: str, depth: int = 1) -> Optional[Dict]:
        """获取图数据缓存"""
        key = redis_manager._generate_key("graph", node_id, depth)
        return await redis_manager.get(key)
    
    @staticmethod
    async def set_graph_data(node_id: str, graph_data: Dict, depth: int = 1, ttl: int = 1200):
        """设置图数据缓存 (20分钟)"""
        key = redis_manager._generate_key("graph", node_id, depth)
        await redis_manager.set(key, graph_data, ttl)
    
    @staticmethod
    async def clear_entity_cache(entity_id: str = None):
        """清除实体缓存"""
        if entity_id:
            key = redis_manager._generate_key("entity", entity_id)
            await redis_manager.delete(key)
        else:
            await redis_manager.clear_pattern("kg:entity:*")
    
    @staticmethod
    async def clear_search_cache():
        """清除搜索缓存"""
        await redis_manager.clear_pattern("kg:search:*")
    
    @staticmethod
    async def clear_graph_cache():
        """清除图数据缓存"""
        await redis_manager.clear_pattern("kg:graph:*")

class FileCache:
    """文件处理缓存"""
    
    @staticmethod
    async def get_file_result(file_hash: str) -> Optional[Dict]:
        """获取文件处理结果缓存"""
        key = redis_manager._generate_key("file", file_hash)
        return await redis_manager.get(key)
    
    @staticmethod
    async def set_file_result(file_hash: str, result: Dict, ttl: int = 7200):
        """设置文件处理结果缓存 (2小时)"""
        key = redis_manager._generate_key("file", file_hash)
        await redis_manager.set(key, result, ttl)
    
    @staticmethod
    async def get_preview_data(file_hash: str) -> Optional[Dict]:
        """获取文件预览缓存"""
        key = redis_manager._generate_key("preview", file_hash)
        return await redis_manager.get(key)
    
    @staticmethod
    async def set_preview_data(file_hash: str, preview: Dict, ttl: int = 3600):
        """设置文件预览缓存 (1小时)"""
        key = redis_manager._generate_key("preview", file_hash)
        await redis_manager.set(key, preview, ttl)

# 初始化函数
async def init_redis():
    """初始化Redis连接"""
    await redis_manager.connect()

async def close_redis():
    """关闭Redis连接"""
    await redis_manager.disconnect()
