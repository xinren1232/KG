#!/usr/bin/env python3
"""
缓存服务
提供内存缓存和Redis缓存支持
"""

import json
import time
import hashlib
import logging
from typing import Any, Optional, Dict, List
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import threading

# 尝试导入Redis，如果没有安装则使用内存缓存
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

logger = logging.getLogger(__name__)

@dataclass
class CacheItem:
    """缓存项"""
    key: str
    value: Any
    created_at: datetime
    expires_at: Optional[datetime] = None
    hit_count: int = 0
    
    def is_expired(self) -> bool:
        """检查是否过期"""
        if self.expires_at is None:
            return False
        return datetime.now() > self.expires_at
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'key': self.key,
            'value': self.value,
            'created_at': self.created_at.isoformat(),
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'hit_count': self.hit_count
        }

class MemoryCache:
    """内存缓存实现"""
    
    def __init__(self, max_size: int = 1000):
        self.max_size = max_size
        self._cache: Dict[str, CacheItem] = {}
        self._lock = threading.RLock()
        self._stats = {
            'hits': 0,
            'misses': 0,
            'sets': 0,
            'deletes': 0,
            'evictions': 0
        }
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存值"""
        with self._lock:
            if key not in self._cache:
                self._stats['misses'] += 1
                return None
            
            item = self._cache[key]
            
            # 检查是否过期
            if item.is_expired():
                del self._cache[key]
                self._stats['misses'] += 1
                return None
            
            # 更新命中统计
            item.hit_count += 1
            self._stats['hits'] += 1
            
            return item.value
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """设置缓存值"""
        with self._lock:
            # 检查缓存大小限制
            if len(self._cache) >= self.max_size and key not in self._cache:
                self._evict_lru()
            
            expires_at = None
            if ttl is not None:
                expires_at = datetime.now() + timedelta(seconds=ttl)
            
            self._cache[key] = CacheItem(
                key=key,
                value=value,
                created_at=datetime.now(),
                expires_at=expires_at
            )
            
            self._stats['sets'] += 1
            return True
    
    def delete(self, key: str) -> bool:
        """删除缓存值"""
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                self._stats['deletes'] += 1
                return True
            return False
    
    def clear(self) -> None:
        """清空缓存"""
        with self._lock:
            self._cache.clear()
    
    def exists(self, key: str) -> bool:
        """检查键是否存在"""
        with self._lock:
            if key not in self._cache:
                return False
            
            item = self._cache[key]
            if item.is_expired():
                del self._cache[key]
                return False
            
            return True
    
    def keys(self, pattern: str = "*") -> List[str]:
        """获取所有键"""
        with self._lock:
            # 简单的模式匹配
            if pattern == "*":
                return list(self._cache.keys())
            
            # 支持简单的通配符
            import fnmatch
            return [key for key in self._cache.keys() if fnmatch.fnmatch(key, pattern)]
    
    def get_stats(self) -> Dict[str, Any]:
        """获取缓存统计"""
        with self._lock:
            total_requests = self._stats['hits'] + self._stats['misses']
            hit_rate = self._stats['hits'] / total_requests if total_requests > 0 else 0
            
            return {
                **self._stats,
                'total_requests': total_requests,
                'hit_rate': hit_rate,
                'cache_size': len(self._cache),
                'max_size': self.max_size
            }
    
    def _evict_lru(self) -> None:
        """LRU淘汰策略"""
        if not self._cache:
            return
        
        # 找到最少使用的项
        lru_key = min(self._cache.keys(), 
                     key=lambda k: (self._cache[k].hit_count, self._cache[k].created_at))
        
        del self._cache[lru_key]
        self._stats['evictions'] += 1

class RedisCache:
    """Redis缓存实现"""
    
    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 0, 
                 password: Optional[str] = None, prefix: str = 'kg:'):
        self.prefix = prefix
        self.client = redis.Redis(
            host=host,
            port=port,
            db=db,
            password=password,
            decode_responses=True
        )
        
        # 测试连接
        try:
            self.client.ping()
            logger.info("Redis连接成功")
        except Exception as e:
            logger.error(f"Redis连接失败: {e}")
            raise
    
    def _make_key(self, key: str) -> str:
        """生成带前缀的键"""
        return f"{self.prefix}{key}"
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存值"""
        try:
            redis_key = self._make_key(key)
            value = self.client.get(redis_key)
            
            if value is None:
                return None
            
            # 尝试解析JSON
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
                
        except Exception as e:
            logger.error(f"Redis获取失败: {e}")
            return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """设置缓存值"""
        try:
            redis_key = self._make_key(key)
            
            # 序列化值
            if isinstance(value, (dict, list)):
                serialized_value = json.dumps(value, ensure_ascii=False)
            else:
                serialized_value = str(value)
            
            if ttl is not None:
                return self.client.setex(redis_key, ttl, serialized_value)
            else:
                return self.client.set(redis_key, serialized_value)
                
        except Exception as e:
            logger.error(f"Redis设置失败: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """删除缓存值"""
        try:
            redis_key = self._make_key(key)
            return bool(self.client.delete(redis_key))
        except Exception as e:
            logger.error(f"Redis删除失败: {e}")
            return False
    
    def clear(self) -> None:
        """清空缓存"""
        try:
            pattern = self._make_key("*")
            keys = self.client.keys(pattern)
            if keys:
                self.client.delete(*keys)
        except Exception as e:
            logger.error(f"Redis清空失败: {e}")
    
    def exists(self, key: str) -> bool:
        """检查键是否存在"""
        try:
            redis_key = self._make_key(key)
            return bool(self.client.exists(redis_key))
        except Exception as e:
            logger.error(f"Redis检查存在失败: {e}")
            return False
    
    def keys(self, pattern: str = "*") -> List[str]:
        """获取所有键"""
        try:
            redis_pattern = self._make_key(pattern)
            keys = self.client.keys(redis_pattern)
            # 移除前缀
            return [key[len(self.prefix):] for key in keys]
        except Exception as e:
            logger.error(f"Redis获取键失败: {e}")
            return []
    
    def get_stats(self) -> Dict[str, Any]:
        """获取缓存统计"""
        try:
            info = self.client.info()
            return {
                'redis_version': info.get('redis_version'),
                'used_memory': info.get('used_memory_human'),
                'connected_clients': info.get('connected_clients'),
                'total_commands_processed': info.get('total_commands_processed'),
                'keyspace_hits': info.get('keyspace_hits', 0),
                'keyspace_misses': info.get('keyspace_misses', 0),
                'hit_rate': info.get('keyspace_hits', 0) / max(1, info.get('keyspace_hits', 0) + info.get('keyspace_misses', 0))
            }
        except Exception as e:
            logger.error(f"Redis获取统计失败: {e}")
            return {}

class CacheService:
    """缓存服务统一接口"""
    
    def __init__(self, use_redis: bool = True, redis_config: Optional[Dict] = None):
        self.backend = None
        
        if use_redis and REDIS_AVAILABLE:
            try:
                config = redis_config or {}
                self.backend = RedisCache(**config)
                logger.info("使用Redis缓存")
            except Exception as e:
                logger.warning(f"Redis初始化失败，回退到内存缓存: {e}")
                self.backend = MemoryCache()
        else:
            self.backend = MemoryCache()
            logger.info("使用内存缓存")
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存值"""
        return self.backend.get(key)
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """设置缓存值"""
        return self.backend.set(key, value, ttl)
    
    def delete(self, key: str) -> bool:
        """删除缓存值"""
        return self.backend.delete(key)
    
    def clear(self) -> None:
        """清空缓存"""
        self.backend.clear()
    
    def exists(self, key: str) -> bool:
        """检查键是否存在"""
        return self.backend.exists(key)
    
    def keys(self, pattern: str = "*") -> List[str]:
        """获取所有键"""
        return self.backend.keys(pattern)
    
    def get_stats(self) -> Dict[str, Any]:
        """获取缓存统计"""
        stats = self.backend.get_stats()
        stats['backend_type'] = type(self.backend).__name__
        return stats
    
    def cache_key(self, *args, **kwargs) -> str:
        """生成缓存键"""
        # 将参数转换为字符串并生成哈希
        key_parts = []
        
        for arg in args:
            if isinstance(arg, (dict, list)):
                key_parts.append(json.dumps(arg, sort_keys=True, ensure_ascii=False))
            else:
                key_parts.append(str(arg))
        
        for k, v in sorted(kwargs.items()):
            if isinstance(v, (dict, list)):
                key_parts.append(f"{k}:{json.dumps(v, sort_keys=True, ensure_ascii=False)}")
            else:
                key_parts.append(f"{k}:{v}")
        
        key_string = "|".join(key_parts)
        return hashlib.md5(key_string.encode('utf-8')).hexdigest()

# 创建全局缓存实例
cache_service = CacheService()

def cached(ttl: int = 300, key_prefix: str = ""):
    """缓存装饰器"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            # 生成缓存键
            cache_key = f"{key_prefix}:{func.__name__}:{cache_service.cache_key(*args, **kwargs)}"
            
            # 尝试从缓存获取
            cached_result = cache_service.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # 执行函数并缓存结果
            result = func(*args, **kwargs)
            cache_service.set(cache_key, result, ttl)
            
            return result
        
        return wrapper
    return decorator
