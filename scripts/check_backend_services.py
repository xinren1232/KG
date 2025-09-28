#!/usr/bin/env python3
"""
后端服务全面检查脚本
检查所有后端服务的运行状态、端口占用、进程状态等
"""

import requests
import subprocess
import psutil
import json
import time
from datetime import datetime
from pathlib import Path
import socket

class BackendServiceChecker:
    def __init__(self):
        self.services = {
            "知识图谱核心API": {
                "url": "http://localhost:8000",
                "health_endpoint": "/health",
                "process_name": "uvicorn",
                "port": 8000
            },
            "Neo4j数据库": {
                "url": "http://localhost:7474",
                "health_endpoint": "/db/data/",
                "process_name": "neo4j",
                "port": 7474,
                "bolt_port": 7687
            },
            "前端开发服务器": {
                "url": "http://localhost:5173",
                "health_endpoint": "/",
                "process_name": "node",
                "port": 5173
            },
            "Dify服务": {
                "url": "http://localhost:3000",
                "health_endpoint": "/",
                "process_name": "dify",
                "port": 3000
            }
        }
        
        self.api_endpoints = [
            "/health",
            "/kg/stats",
            "/kg/files",
            "/system/status",
            "/system/rules",
            "/kg/dictionary/entries"
        ]
        
        self.results = {
            "check_time": datetime.now().isoformat(),
            "services": {},
            "ports": {},
            "processes": {},
            "api_endpoints": {},
            "recommendations": []
        }

    def check_port(self, port):
        """检查端口是否被占用"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('localhost', port))
            sock.close()
            return result == 0
        except Exception:
            return False

    def check_process(self, process_name):
        """检查进程是否运行"""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if process_name.lower() in proc.info['name'].lower():
                        processes.append({
                            'pid': proc.info['pid'],
                            'name': proc.info['name'],
                            'cmdline': ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                        })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            return processes
        except Exception as e:
            return []

    def check_service_health(self, service_name, config):
        """检查服务健康状态"""
        result = {
            "status": "未知",
            "response_time": None,
            "error": None,
            "port_open": False,
            "processes": []
        }
        
        # 检查端口
        result["port_open"] = self.check_port(config["port"])
        
        # 检查进程
        result["processes"] = self.check_process(config["process_name"])
        
        # 检查HTTP响应
        try:
            start_time = time.time()
            url = config["url"] + config.get("health_endpoint", "/")
            response = requests.get(url, timeout=5)
            result["response_time"] = time.time() - start_time
            
            if response.status_code == 200:
                result["status"] = "运行中"
            else:
                result["status"] = f"异常 (HTTP {response.status_code})"
                result["error"] = f"HTTP状态码: {response.status_code}"
                
        except requests.exceptions.ConnectionError:
            result["status"] = "连接失败"
            result["error"] = "无法连接到服务"
        except requests.exceptions.Timeout:
            result["status"] = "超时"
            result["error"] = "请求超时"
        except Exception as e:
            result["status"] = "错误"
            result["error"] = str(e)
        
        return result

    def check_api_endpoints(self):
        """检查API端点"""
        base_url = "http://localhost:8000"
        
        for endpoint in self.api_endpoints:
            result = {
                "status": "未知",
                "response_time": None,
                "error": None
            }
            
            try:
                start_time = time.time()
                response = requests.get(base_url + endpoint, timeout=5)
                result["response_time"] = time.time() - start_time
                
                if response.status_code == 200:
                    result["status"] = "正常"
                else:
                    result["status"] = f"异常 (HTTP {response.status_code})"
                    result["error"] = f"HTTP状态码: {response.status_code}"
                    
            except requests.exceptions.ConnectionError:
                result["status"] = "连接失败"
                result["error"] = "无法连接到API服务"
            except Exception as e:
                result["status"] = "错误"
                result["error"] = str(e)
            
            self.results["api_endpoints"][endpoint] = result

    def check_all_services(self):
        """检查所有服务"""
        print("🔍 开始检查后端服务...")
        
        # 检查各个服务
        for service_name, config in self.services.items():
            print(f"检查 {service_name}...")
            self.results["services"][service_name] = self.check_service_health(service_name, config)
        
        # 检查端口占用情况
        common_ports = [8000, 7474, 7687, 5173, 3000, 5432, 27017, 6379]
        for port in common_ports:
            self.results["ports"][port] = {
                "open": self.check_port(port),
                "description": self.get_port_description(port)
            }
        
        # 检查API端点
        print("检查API端点...")
        self.check_api_endpoints()
        
        # 生成建议
        self.generate_recommendations()

    def get_port_description(self, port):
        """获取端口描述"""
        descriptions = {
            8000: "知识图谱API服务",
            7474: "Neo4j HTTP接口",
            7687: "Neo4j Bolt接口",
            5173: "前端开发服务器",
            3000: "Dify服务",
            5432: "PostgreSQL数据库",
            27017: "MongoDB数据库",
            6379: "Redis缓存"
        }
        return descriptions.get(port, f"端口 {port}")

    def generate_recommendations(self):
        """生成修复建议"""
        recommendations = []
        
        # 检查核心服务
        kg_api = self.results["services"].get("知识图谱核心API", {})
        if kg_api.get("status") != "运行中":
            recommendations.append({
                "priority": "高",
                "service": "知识图谱核心API",
                "issue": "服务未运行",
                "solution": "启动API服务: cd services && python main.py"
            })
        
        neo4j = self.results["services"].get("Neo4j数据库", {})
        if neo4j.get("status") != "运行中":
            recommendations.append({
                "priority": "高",
                "service": "Neo4j数据库",
                "issue": "数据库未运行",
                "solution": "启动Neo4j: scripts/neo4j_manager.bat start"
            })
        
        # 检查端口冲突
        if not self.results["ports"].get(8000, {}).get("open"):
            recommendations.append({
                "priority": "中",
                "service": "API端口",
                "issue": "端口8000未开放",
                "solution": "检查API服务是否正确启动"
            })
        
        # 检查API端点
        failed_endpoints = [ep for ep, result in self.results["api_endpoints"].items() 
                          if result.get("status") != "正常"]
        if failed_endpoints:
            recommendations.append({
                "priority": "中",
                "service": "API端点",
                "issue": f"以下端点异常: {', '.join(failed_endpoints)}",
                "solution": "检查API服务配置和数据库连接"
            })
        
        self.results["recommendations"] = recommendations

    def print_report(self):
        """打印检查报告"""
        print("\n" + "="*60)
        print("🔍 后端服务检查报告")
        print("="*60)
        print(f"检查时间: {self.results['check_time']}")
        
        # 服务状态
        print("\n📊 服务状态:")
        for service_name, result in self.results["services"].items():
            status_icon = "✅" if result["status"] == "运行中" else "❌"
            print(f"  {status_icon} {service_name}: {result['status']}")
            if result.get("response_time"):
                print(f"     响应时间: {result['response_time']:.3f}s")
            if result.get("error"):
                print(f"     错误: {result['error']}")
            if result.get("processes"):
                print(f"     进程: {len(result['processes'])} 个")
        
        # 端口状态
        print("\n🔌 端口状态:")
        for port, result in self.results["ports"].items():
            status_icon = "✅" if result["open"] else "❌"
            print(f"  {status_icon} {port}: {result['description']} - {'开放' if result['open'] else '关闭'}")
        
        # API端点状态
        print("\n🌐 API端点状态:")
        for endpoint, result in self.results["api_endpoints"].items():
            status_icon = "✅" if result["status"] == "正常" else "❌"
            print(f"  {status_icon} {endpoint}: {result['status']}")
            if result.get("response_time"):
                print(f"     响应时间: {result['response_time']:.3f}s")
        
        # 修复建议
        if self.results["recommendations"]:
            print("\n💡 修复建议:")
            for i, rec in enumerate(self.results["recommendations"], 1):
                priority_icon = "🔴" if rec["priority"] == "高" else "🟡"
                print(f"  {i}. {priority_icon} [{rec['priority']}] {rec['service']}")
                print(f"     问题: {rec['issue']}")
                print(f"     解决: {rec['solution']}")
        else:
            print("\n✅ 所有服务运行正常！")

    def save_report(self, filename=None):
        """保存检查报告"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"backend_service_report_{timestamp}.json"
        
        report_path = Path("config") / filename
        report_path.parent.mkdir(exist_ok=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        
        print(f"\n📄 报告已保存到: {report_path}")
        return report_path

def main():
    checker = BackendServiceChecker()
    checker.check_all_services()
    checker.print_report()
    checker.save_report()

if __name__ == "__main__":
    main()
