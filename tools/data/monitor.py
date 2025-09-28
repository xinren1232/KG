#!/usr/bin/env python3
"""
系统监控脚本
监控质量知识图谱助手系统的运行状态
"""

import time
import requests
import psutil
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import smtplib
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
import argparse

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class ServiceStatus:
    """服务状态"""
    name: str
    url: str
    status: str  # online, offline, degraded
    response_time: float
    last_check: datetime
    error_message: Optional[str] = None

@dataclass
class SystemMetrics:
    """系统指标"""
    cpu_percent: float
    memory_percent: float
    disk_percent: float
    network_io: Dict[str, int]
    timestamp: datetime

@dataclass
class Alert:
    """告警信息"""
    level: str  # critical, warning, info
    message: str
    timestamp: datetime
    service: Optional[str] = None
    metric_value: Optional[float] = None

class SystemMonitor:
    """系统监控器"""
    
    def __init__(self, config_file: str = "monitor_config.json"):
        self.config = self._load_config(config_file)
        self.services = self.config.get("services", [])
        self.thresholds = self.config.get("thresholds", {})
        self.notification = self.config.get("notification", {})
        
        # 状态存储
        self.service_statuses: List[ServiceStatus] = []
        self.system_metrics_history: List[SystemMetrics] = []
        self.alerts: List[Alert] = []
        
        # 告警状态跟踪
        self.alert_states = {}
    
    def _load_config(self, config_file: str) -> Dict:
        """加载配置文件"""
        default_config = {
            "services": [
                {
                    "name": "API服务",
                    "url": "http://localhost:8000/health",
                    "timeout": 10,
                    "expected_status": 200
                },
                {
                    "name": "前端服务",
                    "url": "http://localhost:5173",
                    "timeout": 10,
                    "expected_status": 200
                },
                {
                    "name": "Neo4j数据库",
                    "url": "http://localhost:7474",
                    "timeout": 10,
                    "expected_status": 200
                }
            ],
            "thresholds": {
                "cpu_percent": 80,
                "memory_percent": 85,
                "disk_percent": 90,
                "response_time": 5.0
            },
            "notification": {
                "email": {
                    "enabled": False,
                    "smtp_server": "smtp.example.com",
                    "smtp_port": 587,
                    "username": "monitor@example.com",
                    "password": "password",
                    "recipients": ["admin@example.com"]
                },
                "webhook": {
                    "enabled": False,
                    "url": "https://hooks.slack.com/services/xxx"
                }
            },
            "check_interval": 60,
            "alert_cooldown": 300
        }
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                custom_config = json.load(f)
                default_config.update(custom_config)
        except FileNotFoundError:
            logger.info(f"配置文件 {config_file} 不存在，使用默认配置")
            # 创建默认配置文件
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=2, ensure_ascii=False)
        
        return default_config
    
    def check_services(self):
        """检查服务状态"""
        logger.info("检查服务状态...")
        
        for service_config in self.services:
            status = self._check_single_service(service_config)
            self.service_statuses.append(status)
            
            # 检查是否需要告警
            self._check_service_alerts(status)
        
        # 保留最近的状态记录
        if len(self.service_statuses) > 1000:
            self.service_statuses = self.service_statuses[-1000:]
    
    def _check_single_service(self, service_config: Dict) -> ServiceStatus:
        """检查单个服务"""
        name = service_config["name"]
        url = service_config["url"]
        timeout = service_config.get("timeout", 10)
        expected_status = service_config.get("expected_status", 200)
        
        start_time = time.time()
        
        try:
            response = requests.get(url, timeout=timeout)
            response_time = time.time() - start_time
            
            if response.status_code == expected_status:
                status = "online"
                error_message = None
            else:
                status = "degraded"
                error_message = f"HTTP {response.status_code}"
            
        except requests.RequestException as e:
            response_time = time.time() - start_time
            status = "offline"
            error_message = str(e)
        
        return ServiceStatus(
            name=name,
            url=url,
            status=status,
            response_time=response_time,
            last_check=datetime.now(),
            error_message=error_message
        )
    
    def collect_system_metrics(self):
        """收集系统指标"""
        logger.info("收集系统指标...")
        
        try:
            # CPU使用率
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # 内存使用率
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            # 磁盘使用率
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            
            # 网络IO
            network = psutil.net_io_counters()
            network_io = {
                "bytes_sent": network.bytes_sent,
                "bytes_recv": network.bytes_recv,
                "packets_sent": network.packets_sent,
                "packets_recv": network.packets_recv
            }
            
            metrics = SystemMetrics(
                cpu_percent=cpu_percent,
                memory_percent=memory_percent,
                disk_percent=disk_percent,
                network_io=network_io,
                timestamp=datetime.now()
            )
            
            self.system_metrics_history.append(metrics)
            
            # 检查系统指标告警
            self._check_system_alerts(metrics)
            
            # 保留最近的指标记录
            if len(self.system_metrics_history) > 1440:  # 24小时的分钟数
                self.system_metrics_history = self.system_metrics_history[-1440:]
            
        except Exception as e:
            logger.error(f"收集系统指标失败: {e}")
    
    def _check_service_alerts(self, status: ServiceStatus):
        """检查服务告警"""
        alert_key = f"service_{status.name}"
        
        # 服务离线告警
        if status.status == "offline":
            if not self._is_alert_active(alert_key):
                alert = Alert(
                    level="critical",
                    message=f"服务 {status.name} 离线: {status.error_message}",
                    timestamp=datetime.now(),
                    service=status.name
                )
                self._add_alert(alert, alert_key)
        
        # 响应时间告警
        elif status.response_time > self.thresholds.get("response_time", 5.0):
            alert_key_rt = f"service_{status.name}_response_time"
            if not self._is_alert_active(alert_key_rt):
                alert = Alert(
                    level="warning",
                    message=f"服务 {status.name} 响应时间过长: {status.response_time:.2f}s",
                    timestamp=datetime.now(),
                    service=status.name,
                    metric_value=status.response_time
                )
                self._add_alert(alert, alert_key_rt)
        
        # 服务恢复
        elif status.status == "online":
            if self._is_alert_active(alert_key):
                alert = Alert(
                    level="info",
                    message=f"服务 {status.name} 已恢复正常",
                    timestamp=datetime.now(),
                    service=status.name
                )
                self._add_alert(alert)
                self._clear_alert(alert_key)
    
    def _check_system_alerts(self, metrics: SystemMetrics):
        """检查系统指标告警"""
        # CPU告警
        if metrics.cpu_percent > self.thresholds.get("cpu_percent", 80):
            alert_key = "system_cpu"
            if not self._is_alert_active(alert_key):
                alert = Alert(
                    level="warning",
                    message=f"CPU使用率过高: {metrics.cpu_percent}%",
                    timestamp=datetime.now(),
                    metric_value=metrics.cpu_percent
                )
                self._add_alert(alert, alert_key)
        
        # 内存告警
        if metrics.memory_percent > self.thresholds.get("memory_percent", 85):
            alert_key = "system_memory"
            if not self._is_alert_active(alert_key):
                alert = Alert(
                    level="warning",
                    message=f"内存使用率过高: {metrics.memory_percent}%",
                    timestamp=datetime.now(),
                    metric_value=metrics.memory_percent
                )
                self._add_alert(alert, alert_key)
        
        # 磁盘告警
        if metrics.disk_percent > self.thresholds.get("disk_percent", 90):
            alert_key = "system_disk"
            if not self._is_alert_active(alert_key):
                alert = Alert(
                    level="critical",
                    message=f"磁盘使用率过高: {metrics.disk_percent}%",
                    timestamp=datetime.now(),
                    metric_value=metrics.disk_percent
                )
                self._add_alert(alert, alert_key)
    
    def _add_alert(self, alert: Alert, alert_key: str = None):
        """添加告警"""
        self.alerts.append(alert)
        
        if alert_key:
            self.alert_states[alert_key] = datetime.now()
        
        # 发送通知
        self._send_notification(alert)
        
        # 记录日志
        logger.warning(f"[{alert.level.upper()}] {alert.message}")
        
        # 保留最近的告警记录
        if len(self.alerts) > 500:
            self.alerts = self.alerts[-500:]
    
    def _is_alert_active(self, alert_key: str) -> bool:
        """检查告警是否处于冷却期"""
        if alert_key not in self.alert_states:
            return False
        
        cooldown = self.config.get("alert_cooldown", 300)
        last_alert = self.alert_states[alert_key]
        
        return (datetime.now() - last_alert).total_seconds() < cooldown
    
    def _clear_alert(self, alert_key: str):
        """清除告警状态"""
        if alert_key in self.alert_states:
            del self.alert_states[alert_key]
    
    def _send_notification(self, alert: Alert):
        """发送通知"""
        # 邮件通知
        if self.notification.get("email", {}).get("enabled", False):
            self._send_email_notification(alert)
        
        # Webhook通知
        if self.notification.get("webhook", {}).get("enabled", False):
            self._send_webhook_notification(alert)
    
    def _send_email_notification(self, alert: Alert):
        """发送邮件通知"""
        try:
            email_config = self.notification["email"]
            
            msg = MimeMultipart()
            msg['From'] = email_config["username"]
            msg['To'] = ", ".join(email_config["recipients"])
            msg['Subject'] = f"[{alert.level.upper()}] 系统监控告警"
            
            body = f"""
            告警级别: {alert.level}
            告警时间: {alert.timestamp}
            告警消息: {alert.message}
            服务名称: {alert.service or 'N/A'}
            指标值: {alert.metric_value or 'N/A'}
            """
            
            msg.attach(MimeText(body, 'plain', 'utf-8'))
            
            server = smtplib.SMTP(email_config["smtp_server"], email_config["smtp_port"])
            server.starttls()
            server.login(email_config["username"], email_config["password"])
            server.send_message(msg)
            server.quit()
            
            logger.info("邮件通知发送成功")
            
        except Exception as e:
            logger.error(f"邮件通知发送失败: {e}")
    
    def _send_webhook_notification(self, alert: Alert):
        """发送Webhook通知"""
        try:
            webhook_config = self.notification["webhook"]
            
            payload = {
                "level": alert.level,
                "message": alert.message,
                "timestamp": alert.timestamp.isoformat(),
                "service": alert.service,
                "metric_value": alert.metric_value
            }
            
            response = requests.post(
                webhook_config["url"],
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info("Webhook通知发送成功")
            else:
                logger.error(f"Webhook通知发送失败: HTTP {response.status_code}")
                
        except Exception as e:
            logger.error(f"Webhook通知发送失败: {e}")
    
    def generate_report(self) -> Dict[str, Any]:
        """生成监控报告"""
        now = datetime.now()
        
        # 服务状态摘要
        service_summary = {}
        for status in self.service_statuses[-len(self.services):]:  # 最新状态
            service_summary[status.name] = {
                "status": status.status,
                "response_time": status.response_time,
                "last_check": status.last_check.isoformat(),
                "error_message": status.error_message
            }
        
        # 系统指标摘要
        latest_metrics = self.system_metrics_history[-1] if self.system_metrics_history else None
        system_summary = asdict(latest_metrics) if latest_metrics else None
        
        # 最近告警
        recent_alerts = [
            asdict(alert) for alert in self.alerts[-10:]
        ]
        
        # 统计信息
        total_alerts = len(self.alerts)
        critical_alerts = len([a for a in self.alerts if a.level == "critical"])
        warning_alerts = len([a for a in self.alerts if a.level == "warning"])
        
        return {
            "timestamp": now.isoformat(),
            "services": service_summary,
            "system": system_summary,
            "alerts": {
                "recent": recent_alerts,
                "total": total_alerts,
                "critical": critical_alerts,
                "warning": warning_alerts
            },
            "uptime": {
                "monitor_start": self.config.get("start_time", now.isoformat()),
                "current_time": now.isoformat()
            }
        }
    
    def run_once(self):
        """执行一次监控检查"""
        logger.info("开始监控检查...")
        
        # 检查服务
        self.check_services()
        
        # 收集系统指标
        self.collect_system_metrics()
        
        logger.info("监控检查完成")
    
    def run_continuous(self):
        """持续监控"""
        logger.info("开始持续监控...")
        
        check_interval = self.config.get("check_interval", 60)
        
        try:
            while True:
                self.run_once()
                time.sleep(check_interval)
                
        except KeyboardInterrupt:
            logger.info("监控已停止")
        except Exception as e:
            logger.error(f"监控异常: {e}")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="系统监控脚本")
    parser.add_argument("--config", default="monitor_config.json", help="配置文件路径")
    parser.add_argument("--once", action="store_true", help="执行一次检查后退出")
    parser.add_argument("--report", action="store_true", help="生成监控报告")
    
    args = parser.parse_args()
    
    monitor = SystemMonitor(args.config)
    
    if args.report:
        report = monitor.generate_report()
        print(json.dumps(report, indent=2, ensure_ascii=False))
    elif args.once:
        monitor.run_once()
    else:
        monitor.run_continuous()

if __name__ == "__main__":
    main()
