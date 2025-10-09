#!/usr/bin/env python3
"""
知识图谱系统全面检查
检查所有服务、功能、数据和配置的状态
"""

import requests
import json
import os
import sys
from pathlib import Path
from datetime import datetime
import subprocess
import time

class SystemChecker:
    def __init__(self):
        self.report = {
            "check_time": datetime.now().isoformat(),
            "services": {},
            "features": {},
            "data_files": {},
            "databases": {},
            "configurations": {},
            "api_endpoints": {},
            "frontend_pages": {},
            "overall_status": "unknown",
            "health_metrics": {},
            "recommendations": []
        }
        
    def check_service_health(self, name, url, timeout=5):
        """检查服务健康状态"""
        try:
            start_time = time.time()
            response = requests.get(url, timeout=timeout)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                return {
                    "status": "运行中",
                    "url": url,
                    "response_time": round(response_time, 3),
                    "status_code": response.status_code,
                    "last_check": datetime.now().isoformat()
                }
            else:
                return {
                    "status": "异常",
                    "url": url,
                    "status_code": response.status_code,
                    "error": f"HTTP {response.status_code}",
                    "last_check": datetime.now().isoformat()
                }
        except Exception as e:
            return {
                "status": "离线",
                "url": url,
                "error": str(e),
                "last_check": datetime.now().isoformat()
            }
    
    def check_api_endpoint(self, name, url, expected_keys=None, timeout=10):
        """检查API端点功能"""
        try:
            response = requests.get(url, timeout=timeout)
            if response.status_code == 200:
                data = response.json()
                
                # 检查期望的键
                if expected_keys:
                    missing_keys = [key for key in expected_keys if key not in data]
                    if missing_keys:
                        return {
                            "status": "部分功能",
                            "missing_keys": missing_keys,
                            "data_sample": str(data)[:200] + "..."
                        }
                
                return {
                    "status": "正常",
                    "data_size": len(str(data)),
                    "response_time": response.elapsed.total_seconds()
                }
            else:
                return {
                    "status": "错误",
                    "status_code": response.status_code,
                    "error": response.text[:200]
                }
        except Exception as e:
            return {
                "status": "失败",
                "error": str(e)
            }
    
    def check_file_status(self, name, path):
        """检查文件状态"""
        file_path = Path(path)
        if file_path.exists():
            stat = file_path.stat()
            return {
                "status": "存在",
                "path": str(file_path),
                "size": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
            }
        else:
            return {
                "status": "缺失",
                "path": str(file_path)
            }
    
    def check_database_connection(self, name, connection_info):
        """检查数据库连接"""
        if name == "Neo4j":
            try:
                # 检查Neo4j HTTP接口
                response = requests.get("http://localhost:7474", timeout=5)
                if response.status_code == 200:
                    # 检查数据库内容
                    try:
                        from neo4j import GraphDatabase
                        driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password123"))
                        with driver.session() as session:
                            result = session.run("MATCH (n) RETURN count(n) as count")
                            node_count = result.single()["count"]
                            
                            result = session.run("MATCH ()-[r]->() RETURN count(r) as count")
                            rel_count = result.single()["count"]
                            
                        driver.close()
                        return {
                            "status": "连接正常",
                            "node_count": node_count,
                            "relationship_count": rel_count,
                            "url": "bolt://localhost:7687"
                        }
                    except Exception as e:
                        return {
                            "status": "连接异常",
                            "error": str(e),
                            "http_status": "可访问"
                        }
                else:
                    return {
                        "status": "服务离线",
                        "http_status": response.status_code
                    }
            except Exception as e:
                return {
                    "status": "无法连接",
                    "error": str(e)
                }
        
        return {"status": "未检查", "info": connection_info}
    
    def run_comprehensive_check(self):
        """运行全面检查"""
        print("🔍 开始系统全面检查...")
        print("=" * 60)
        
        # 1. 检查核心服务
        print("\n📡 检查核心服务...")
        services = {
            "知识图谱核心API": "http://localhost:8000/health",
            "前端Web应用": "http://localhost:5173",
            "Neo4j数据库": "http://localhost:7474"
        }
        
        for name, url in services.items():
            print(f"  检查 {name}...")
            self.report["services"][name] = self.check_service_health(name, url)
            status = self.report["services"][name]["status"]
            print(f"    ✅ {status}" if status == "运行中" else f"    ❌ {status}")
        
        # 2. 检查API端点功能
        print("\n🔌 检查API端点功能...")
        api_endpoints = {
            "健康检查": ("http://localhost:8000/health", None),
            "图谱数据": ("http://localhost:8000/kg/graph?limit=5", ["success", "data"]),
            "词典管理": ("http://localhost:8000/kg/dictionary/entries?size=3", ["success", "data"]),
            "系统状态": ("http://localhost:8000/system/status", ["success", "data"]),
            "系统规则": ("http://localhost:8000/system/rules", ["success", "data"])
        }
        
        for name, (url, expected_keys) in api_endpoints.items():
            print(f"  检查 {name}...")
            self.report["api_endpoints"][name] = self.check_api_endpoint(name, url, expected_keys)
            status = self.report["api_endpoints"][name]["status"]
            print(f"    ✅ {status}" if status == "正常" else f"    ⚠️ {status}")
        
        # 3. 检查数据库
        print("\n🗄️ 检查数据库...")
        databases = {
            "Neo4j": {"host": "localhost", "port": 7687, "auth": "neo4j/password123"}
        }
        
        for name, info in databases.items():
            print(f"  检查 {name}...")
            self.report["databases"][name] = self.check_database_connection(name, info)
            status = self.report["databases"][name]["status"]
            print(f"    ✅ {status}" if "正常" in status else f"    ❌ {status}")
        
        # 4. 检查关键文件
        print("\n📁 检查关键文件...")
        key_files = {
            "API主服务": "services/api/main.py",
            "Neo4j客户端": "services/api/database/neo4j_client.py",
            "图谱路由": "services/api/routers/kg_router.py",
            "前端主页": "apps/web/src/views/GraphVisualization.vue",
            "词典管理": "apps/web/src/views/DictionaryManagement.vue",
            "API配置": "apps/web/src/api/index.js",
            "词典数据": "api/data/dictionary.json",
            "系统配置": "config/graph_visualization_data.json"
        }
        
        for name, path in key_files.items():
            print(f"  检查 {name}...")
            self.report["data_files"][name] = self.check_file_status(name, path)
            status = self.report["data_files"][name]["status"]
            print(f"    ✅ {status}" if status == "存在" else f"    ❌ {status}")
        
        # 5. 检查前端页面
        print("\n🌐 检查前端页面...")
        frontend_pages = {
            "图谱可视化": "http://localhost:5173/#/graph-viz",
            "词典管理": "http://localhost:5173/#/dictionary",
            "系统管理": "http://localhost:5173/#/system",
            "数据治理": "http://localhost:5173/#/governance"
        }
        
        for name, url in frontend_pages.items():
            print(f"  检查 {name}...")
            self.report["frontend_pages"][name] = self.check_service_health(name, url, timeout=3)
            status = self.report["frontend_pages"][name]["status"]
            print(f"    ✅ {status}" if status == "运行中" else f"    ⚠️ {status}")
        
        # 6. 计算健康指标
        self.calculate_health_metrics()
        
        # 7. 生成建议
        self.generate_recommendations()
        
        print(f"\n📊 系统健康度: {self.report['health_metrics']['overall_health']}")
        print(f"🎯 总体状态: {self.report['overall_status']}")
        
        return self.report
    
    def calculate_health_metrics(self):
        """计算健康指标"""
        # 服务健康度
        services_total = len(self.report["services"])
        services_healthy = sum(1 for s in self.report["services"].values() if s["status"] == "运行中")
        
        # API端点健康度
        apis_total = len(self.report["api_endpoints"])
        apis_healthy = sum(1 for a in self.report["api_endpoints"].values() if a["status"] == "正常")
        
        # 文件完整度
        files_total = len(self.report["data_files"])
        files_present = sum(1 for f in self.report["data_files"].values() if f["status"] == "存在")
        
        # 数据库健康度
        dbs_total = len(self.report["databases"])
        dbs_healthy = sum(1 for d in self.report["databases"].values() if "正常" in d["status"])
        
        # 前端页面健康度
        pages_total = len(self.report["frontend_pages"])
        pages_healthy = sum(1 for p in self.report["frontend_pages"].values() if p["status"] == "运行中")
        
        # 计算总体健康度
        total_checks = services_total + apis_total + files_total + dbs_total + pages_total
        total_healthy = services_healthy + apis_healthy + files_present + dbs_healthy + pages_healthy
        
        overall_health = (total_healthy / total_checks * 100) if total_checks > 0 else 0
        
        self.report["health_metrics"] = {
            "services": f"{services_healthy}/{services_total}",
            "api_endpoints": f"{apis_healthy}/{apis_total}",
            "data_files": f"{files_present}/{files_total}",
            "databases": f"{dbs_healthy}/{dbs_total}",
            "frontend_pages": f"{pages_healthy}/{pages_total}",
            "overall_health": f"{overall_health:.1f}%",
            "total_checks": total_checks,
            "total_healthy": total_healthy
        }
        
        # 确定总体状态
        if overall_health >= 90:
            self.report["overall_status"] = "优秀"
        elif overall_health >= 75:
            self.report["overall_status"] = "良好"
        elif overall_health >= 60:
            self.report["overall_status"] = "一般"
        elif overall_health >= 40:
            self.report["overall_status"] = "需要关注"
        else:
            self.report["overall_status"] = "严重问题"
    
    def generate_recommendations(self):
        """生成改进建议"""
        recommendations = []
        
        # 检查服务状态
        for name, service in self.report["services"].items():
            if service["status"] != "运行中":
                recommendations.append(f"🔧 修复服务: {name} 当前状态为 {service['status']}")
        
        # 检查API端点
        for name, api in self.report["api_endpoints"].items():
            if api["status"] != "正常":
                recommendations.append(f"🔌 修复API: {name} 当前状态为 {api['status']}")
        
        # 检查文件
        for name, file_info in self.report["data_files"].items():
            if file_info["status"] != "存在":
                recommendations.append(f"📁 补充文件: {name} 文件缺失")
        
        # 检查数据库
        for name, db in self.report["databases"].items():
            if "正常" not in db["status"]:
                recommendations.append(f"🗄️ 修复数据库: {name} 连接异常")
        
        # 性能建议
        slow_apis = [name for name, api in self.report["api_endpoints"].items() 
                    if api.get("response_time", 0) > 2.0]
        if slow_apis:
            recommendations.append(f"⚡ 优化性能: 以下API响应较慢 {', '.join(slow_apis)}")
        
        self.report["recommendations"] = recommendations

def main():
    """主函数"""
    checker = SystemChecker()
    report = checker.run_comprehensive_check()
    
    # 保存报告
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"config/system_status_report_{timestamp}.json"
    
    os.makedirs("config", exist_ok=True)
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n📄 报告已保存: {report_file}")
    
    # 显示摘要
    print("\n" + "=" * 60)
    print("📋 系统检查摘要")
    print("=" * 60)
    
    metrics = report["health_metrics"]
    print(f"🏥 系统健康度: {metrics['overall_health']}")
    print(f"📡 服务状态: {metrics['services']}")
    print(f"🔌 API端点: {metrics['api_endpoints']}")
    print(f"📁 关键文件: {metrics['data_files']}")
    print(f"🗄️ 数据库: {metrics['databases']}")
    print(f"🌐 前端页面: {metrics['frontend_pages']}")
    print(f"🎯 总体状态: {report['overall_status']}")
    
    if report["recommendations"]:
        print(f"\n💡 改进建议:")
        for rec in report["recommendations"]:
            print(f"  {rec}")
    else:
        print(f"\n🎉 系统运行良好，无需改进！")
    
    return 0 if report["overall_status"] in ["优秀", "良好"] else 1

if __name__ == "__main__":
    sys.exit(main())
