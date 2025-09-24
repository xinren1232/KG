#!/usr/bin/env python3
"""
性能监控中间件
监控API性能指标和系统资源使用情况
"""

import time
import psutil
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict, deque
from dataclasses import dataclass, asdict
from fastapi import Request, Response
import asyncio
import threading

logger = logging.getLogger(__name__)

@dataclass
class RequestMetrics:
    """请求指标"""
    path: str
    method: str
    status_code: int
    duration: float
    timestamp: datetime
    request_size: int = 0
    response_size: int = 0
    user_agent: str = ""
    ip_address: str = ""

@dataclass
class SystemMetrics:
    """系统指标"""
    cpu_percent: float
    memory_percent: float
    memory_used: int
    memory_available: int
    disk_usage_percent: float
    network_io: Dict[str, int]
    timestamp: datetime

class PerformanceMonitor:
    """性能监控器"""
    
    def __init__(self, max_history: int = 1000):
        self.max_history = max_history
        self.request_history: deque = deque(maxlen=max_history)
        self.system_history: deque = deque(maxlen=100)  # 系统指标历史较少
        
        # 实时统计
        self.stats = {
            "total_requests": 0,
            "total_errors": 0,
            "avg_response_time": 0.0,
            "requests_per_minute": 0,
            "start_time": datetime.now()
        }
        
        # 按端点统计
        self.endpoint_stats = defaultdict(lambda: {
            "count": 0,
            "total_time": 0.0,
            "avg_time": 0.0,
            "min_time": float('inf'),
            "max_time": 0.0,
            "error_count": 0,
            "last_access": None
        })
        
        # 按状态码统计
        self.status_code_stats = defaultdict(int)
        
        # 慢请求阈值（秒）
        self.slow_request_threshold = 2.0
        self.slow_requests: deque = deque(maxlen=50)
        
        # 启动系统监控线程
        self._start_system_monitoring()
        
        # 线程锁
        self._lock = threading.RLock()
    
    async def track_request(self, request: Request, call_next):
        """跟踪请求性能"""
        start_time = time.time()
        
        # 获取请求信息
        path = request.url.path
        method = request.method
        user_agent = request.headers.get("user-agent", "")
        ip_address = self._get_client_ip(request)
        
        # 估算请求大小
        request_size = len(str(request.headers)) + len(await request.body()) if hasattr(request, 'body') else 0
        
        try:
            # 执行请求
            response = await call_next(request)
            status_code = response.status_code
            
            # 计算响应时间
            duration = time.time() - start_time
            
            # 估算响应大小
            response_size = 0
            if hasattr(response, 'body'):
                response_size = len(response.body) if response.body else 0
            
            # 记录指标
            metrics = RequestMetrics(
                path=path,
                method=method,
                status_code=status_code,
                duration=duration,
                timestamp=datetime.now(),
                request_size=request_size,
                response_size=response_size,
                user_agent=user_agent,
                ip_address=ip_address
            )
            
            self._record_request_metrics(metrics)
            
            # 添加性能头
            response.headers["X-Response-Time"] = f"{duration:.3f}s"
            response.headers["X-Request-ID"] = request.headers.get("X-Request-ID", "unknown")
            
            return response
            
        except Exception as e:
            # 记录错误请求
            duration = time.time() - start_time
            metrics = RequestMetrics(
                path=path,
                method=method,
                status_code=500,
                duration=duration,
                timestamp=datetime.now(),
                request_size=request_size,
                response_size=0,
                user_agent=user_agent,
                ip_address=ip_address
            )
            
            self._record_request_metrics(metrics)
            raise
    
    def _record_request_metrics(self, metrics: RequestMetrics):
        """记录请求指标"""
        with self._lock:
            # 添加到历史记录
            self.request_history.append(metrics)
            
            # 更新总体统计
            self.stats["total_requests"] += 1
            if metrics.status_code >= 400:
                self.stats["total_errors"] += 1
            
            # 更新平均响应时间
            total_time = sum(req.duration for req in self.request_history)
            self.stats["avg_response_time"] = total_time / len(self.request_history)
            
            # 更新每分钟请求数
            now = datetime.now()
            recent_requests = [req for req in self.request_history 
                             if (now - req.timestamp).total_seconds() <= 60]
            self.stats["requests_per_minute"] = len(recent_requests)
            
            # 更新端点统计
            endpoint_key = f"{metrics.method} {metrics.path}"
            endpoint_stat = self.endpoint_stats[endpoint_key]
            endpoint_stat["count"] += 1
            endpoint_stat["total_time"] += metrics.duration
            endpoint_stat["avg_time"] = endpoint_stat["total_time"] / endpoint_stat["count"]
            endpoint_stat["min_time"] = min(endpoint_stat["min_time"], metrics.duration)
            endpoint_stat["max_time"] = max(endpoint_stat["max_time"], metrics.duration)
            endpoint_stat["last_access"] = metrics.timestamp
            
            if metrics.status_code >= 400:
                endpoint_stat["error_count"] += 1
            
            # 更新状态码统计
            self.status_code_stats[metrics.status_code] += 1
            
            # 记录慢请求
            if metrics.duration > self.slow_request_threshold:
                self.slow_requests.append(metrics)
                logger.warning(
                    f"Slow request detected: {endpoint_key} took {metrics.duration:.3f}s",
                    extra={
                        "path": metrics.path,
                        "method": metrics.method,
                        "duration": metrics.duration,
                        "status_code": metrics.status_code
                    }
                )
    
    def _start_system_monitoring(self):
        """启动系统监控线程"""
        def monitor_system():
            while True:
                try:
                    # 获取系统指标
                    cpu_percent = psutil.cpu_percent(interval=1)
                    memory = psutil.virtual_memory()
                    disk = psutil.disk_usage('/')
                    network = psutil.net_io_counters()
                    
                    metrics = SystemMetrics(
                        cpu_percent=cpu_percent,
                        memory_percent=memory.percent,
                        memory_used=memory.used,
                        memory_available=memory.available,
                        disk_usage_percent=disk.percent,
                        network_io={
                            "bytes_sent": network.bytes_sent,
                            "bytes_recv": network.bytes_recv,
                            "packets_sent": network.packets_sent,
                            "packets_recv": network.packets_recv
                        },
                        timestamp=datetime.now()
                    )
                    
                    with self._lock:
                        self.system_history.append(metrics)
                    
                    # 检查资源使用警告
                    if cpu_percent > 80:
                        logger.warning(f"High CPU usage: {cpu_percent}%")
                    if memory.percent > 80:
                        logger.warning(f"High memory usage: {memory.percent}%")
                    if disk.percent > 90:
                        logger.warning(f"High disk usage: {disk.percent}%")
                    
                except Exception as e:
                    logger.error(f"System monitoring error: {e}")
                
                time.sleep(30)  # 每30秒监控一次
        
        thread = threading.Thread(target=monitor_system, daemon=True)
        thread.start()
    
    def _get_client_ip(self, request: Request) -> str:
        """获取客户端IP地址"""
        # 检查代理头
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        # 回退到直接连接IP
        return request.client.host if request.client else "unknown"
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """获取性能统计"""
        with self._lock:
            # 计算运行时间
            uptime = datetime.now() - self.stats["start_time"]
            
            # 获取最新系统指标
            latest_system = self.system_history[-1] if self.system_history else None
            
            # 计算错误率
            error_rate = (self.stats["total_errors"] / max(1, self.stats["total_requests"])) * 100
            
            # 获取最慢的端点
            slowest_endpoints = sorted(
                [(k, v) for k, v in self.endpoint_stats.items()],
                key=lambda x: x[1]["avg_time"],
                reverse=True
            )[:5]
            
            # 获取最频繁的端点
            busiest_endpoints = sorted(
                [(k, v) for k, v in self.endpoint_stats.items()],
                key=lambda x: x[1]["count"],
                reverse=True
            )[:5]
            
            return {
                "overview": {
                    "uptime_seconds": uptime.total_seconds(),
                    "total_requests": self.stats["total_requests"],
                    "total_errors": self.stats["total_errors"],
                    "error_rate_percent": error_rate,
                    "avg_response_time": self.stats["avg_response_time"],
                    "requests_per_minute": self.stats["requests_per_minute"]
                },
                "system": asdict(latest_system) if latest_system else None,
                "endpoints": {
                    "slowest": [{"endpoint": k, **v} for k, v in slowest_endpoints],
                    "busiest": [{"endpoint": k, **v} for k, v in busiest_endpoints]
                },
                "status_codes": dict(self.status_code_stats),
                "slow_requests": len(self.slow_requests),
                "recent_slow_requests": [
                    {
                        "path": req.path,
                        "method": req.method,
                        "duration": req.duration,
                        "timestamp": req.timestamp.isoformat()
                    }
                    for req in list(self.slow_requests)[-5:]
                ]
            }
    
    def get_endpoint_stats(self, endpoint: str = None) -> Dict[str, Any]:
        """获取端点统计"""
        with self._lock:
            if endpoint:
                return dict(self.endpoint_stats.get(endpoint, {}))
            else:
                return {k: dict(v) for k, v in self.endpoint_stats.items()}
    
    def get_system_history(self, hours: int = 1) -> List[Dict[str, Any]]:
        """获取系统历史数据"""
        with self._lock:
            cutoff_time = datetime.now() - timedelta(hours=hours)
            recent_metrics = [
                asdict(metrics) for metrics in self.system_history
                if metrics.timestamp >= cutoff_time
            ]
            return recent_metrics
    
    def get_request_history(self, hours: int = 1, path: str = None) -> List[Dict[str, Any]]:
        """获取请求历史数据"""
        with self._lock:
            cutoff_time = datetime.now() - timedelta(hours=hours)
            filtered_requests = [
                asdict(req) for req in self.request_history
                if req.timestamp >= cutoff_time and (not path or req.path == path)
            ]
            return filtered_requests
    
    def reset_stats(self):
        """重置统计数据"""
        with self._lock:
            self.request_history.clear()
            self.system_history.clear()
            self.endpoint_stats.clear()
            self.status_code_stats.clear()
            self.slow_requests.clear()
            
            self.stats = {
                "total_requests": 0,
                "total_errors": 0,
                "avg_response_time": 0.0,
                "requests_per_minute": 0,
                "start_time": datetime.now()
            }

# 创建全局性能监控实例
performance_monitor = PerformanceMonitor()
