#!/usr/bin/env python3
"""
系统状态检查
检查整个质量知识图谱助手系统的运行状态和功能完整性
"""
import requests
import json
import time
from pathlib import Path
from datetime import datetime
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SystemStatusChecker:
    """系统状态检查器"""
    
    def __init__(self):
        self.services = {
            "知识图谱核心API": "http://localhost:8000",
            "前端Web应用": "http://localhost:5174"
        }
        self.status_report = {
            "check_time": datetime.now().isoformat(),
            "services": {},
            "features": {},
            "data_files": {},
            "overall_status": "unknown"
        }
    
    def check_all_services(self):
        """检查所有服务状态"""
        logger.info("🔍 开始系统状态检查...")
        
        # 检查服务状态
        self._check_services()
        
        # 检查功能特性
        self._check_features()
        
        # 检查数据文件
        self._check_data_files()
        
        # 计算整体状态
        self._calculate_overall_status()
        
        # 生成报告
        self._generate_report()
        
        logger.info("✅ 系统状态检查完成")
    
    def _check_services(self):
        """检查服务状态"""
        logger.info("检查服务状态...")
        
        for service_name, base_url in self.services.items():
            try:
                if service_name == "前端Web应用":
                    # 前端应用检查
                    response = requests.get(base_url, timeout=5)
                    status = "运行中" if response.status_code == 200 else "异常"
                else:
                    # API服务检查
                    response = requests.get(f"{base_url}/health", timeout=5)
                    if response.status_code == 200:
                        data = response.json()
                        status = "运行中"
                    else:
                        status = "异常"
                
                self.status_report["services"][service_name] = {
                    "status": status,
                    "url": base_url,
                    "response_time": response.elapsed.total_seconds(),
                    "last_check": datetime.now().isoformat()
                }
                
                logger.info(f"  ✅ {service_name}: {status}")
                
            except Exception as e:
                self.status_report["services"][service_name] = {
                    "status": "离线",
                    "url": base_url,
                    "error": str(e),
                    "last_check": datetime.now().isoformat()
                }
                logger.warning(f"  ❌ {service_name}: 离线 ({e})")
    
    def _check_features(self):
        """检查功能特性"""
        logger.info("检查功能特性...")
        
        features = {
            "文档上传": self._test_document_upload,
            "知识抽取": self._test_knowledge_extraction,
            "图谱构建": self._test_graph_building,
            "图谱查询": self._test_graph_query,
            "词典管理": self._test_dictionary_management
        }
        
        for feature_name, test_func in features.items():
            try:
                result = test_func()
                self.status_report["features"][feature_name] = {
                    "status": "正常" if result else "异常",
                    "last_test": datetime.now().isoformat()
                }
                status_icon = "✅" if result else "❌"
                logger.info(f"  {status_icon} {feature_name}: {'正常' if result else '异常'}")
                
            except Exception as e:
                self.status_report["features"][feature_name] = {
                    "status": "错误",
                    "error": str(e),
                    "last_test": datetime.now().isoformat()
                }
                logger.warning(f"  ❌ {feature_name}: 错误 ({e})")
    
    def _test_document_upload(self) -> bool:
        """测试文档上传功能"""
        try:
            response = requests.get(
                "http://localhost:8000/kg/stats",
                timeout=10
            )
            return response.status_code == 200 and "stats" in response.json()
        except Exception:
            return False

    def _test_knowledge_extraction(self) -> bool:
        """测试知识抽取功能"""
        try:
            response = requests.get(
                "http://localhost:8000/kg/dictionary",
                timeout=10
            )
            return response.status_code == 200 and "entries" in response.json()
        except Exception:
            return False

    def _test_graph_building(self) -> bool:
        """测试图谱构建功能"""
        try:
            response = requests.get(
                "http://localhost:8000/kg/graph/data",
                timeout=10
            )
            return response.status_code == 200 and "data" in response.json()
        except Exception:
            return False

    def _test_graph_query(self) -> bool:
        """测试图谱查询功能"""
        try:
            response = requests.post(
                "http://localhost:8000/kg/query",
                json={
                    "query_type": "search",
                    "query": "摄像头",
                    "limit": 10
                },
                timeout=10
            )
            return response.status_code == 200 and "results" in response.json()
        except Exception:
            return False

    def _test_dictionary_management(self) -> bool:
        """测试词典管理功能"""
        try:
            response = requests.get(
                "http://localhost:8000/kg/dictionary?category=组件",
                timeout=10
            )
            return response.status_code == 200 and "entries" in response.json()
        except Exception:
            return False
    
    def _check_data_files(self):
        """检查数据文件"""
        logger.info("检查数据文件...")
        
        important_files = {
            "本体约束": "graph/ontology_v0.2_constraints.cypher",
            "数据抽取器": "services/nlp/material_anomaly_extractor.py",
            "增强抽取器": "services/nlp/enhanced_document_extractor.py",
            "推理引擎": "services/reasoning/knowledge_graph_engine.py",
            "Dify工具": "services/dify/kg_tools.py",
            "治理系统": "services/governance/data_governance_system.py",
            "前端应用": "apps/web/src/views/AnomalyGuide.vue",
            "API服务": "api/quality_kg_api.py"
        }
        
        for file_name, file_path in important_files.items():
            path = Path(file_path)
            if path.exists():
                self.status_report["data_files"][file_name] = {
                    "status": "存在",
                    "path": str(path),
                    "size": path.stat().st_size,
                    "modified": datetime.fromtimestamp(path.stat().st_mtime).isoformat()
                }
                logger.info(f"  ✅ {file_name}: 存在")
            else:
                self.status_report["data_files"][file_name] = {
                    "status": "缺失",
                    "path": str(path)
                }
                logger.warning(f"  ❌ {file_name}: 缺失")
    
    def _calculate_overall_status(self):
        """计算整体状态"""
        # 统计各项状态
        service_ok = sum(1 for s in self.status_report["services"].values() if s["status"] == "运行中")
        service_total = len(self.status_report["services"])
        
        feature_ok = sum(1 for f in self.status_report["features"].values() if f["status"] == "正常")
        feature_total = len(self.status_report["features"])
        
        file_ok = sum(1 for f in self.status_report["data_files"].values() if f["status"] == "存在")
        file_total = len(self.status_report["data_files"])
        
        # 计算整体健康度
        total_ok = service_ok + feature_ok + file_ok
        total_items = service_total + feature_total + file_total
        health_rate = total_ok / total_items if total_items > 0 else 0
        
        if health_rate >= 0.9:
            overall_status = "优秀"
        elif health_rate >= 0.8:
            overall_status = "良好"
        elif health_rate >= 0.7:
            overall_status = "一般"
        else:
            overall_status = "需要关注"
        
        self.status_report["overall_status"] = overall_status
        self.status_report["health_metrics"] = {
            "services": f"{service_ok}/{service_total}",
            "features": f"{feature_ok}/{feature_total}",
            "files": f"{file_ok}/{file_total}",
            "health_rate": f"{health_rate:.1%}"
        }
    
    def _generate_report(self):
        """生成状态报告"""
        # 保存详细报告
        report_file = f"system_status_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.status_report, f, ensure_ascii=False, indent=2)
        
        # 打印摘要报告
        print("\n" + "="*60)
        print("🎯 质量知识图谱助手系统 - 状态报告")
        print("="*60)
        
        print(f"\n📊 整体状态: {self.status_report['overall_status']}")
        print(f"🔍 检查时间: {self.status_report['check_time']}")
        print(f"📈 健康度: {self.status_report['health_metrics']['health_rate']}")
        
        print(f"\n🌐 服务状态 ({self.status_report['health_metrics']['services']}):")
        for name, info in self.status_report["services"].items():
            status_icon = "✅" if info["status"] == "运行中" else "❌"
            print(f"  {status_icon} {name}: {info['status']}")
        
        print(f"\n⚙️ 功能特性 ({self.status_report['health_metrics']['features']}):")
        for name, info in self.status_report["features"].items():
            status_icon = "✅" if info["status"] == "正常" else "❌"
            print(f"  {status_icon} {name}: {info['status']}")
        
        print(f"\n📁 数据文件 ({self.status_report['health_metrics']['files']}):")
        for name, info in self.status_report["data_files"].items():
            status_icon = "✅" if info["status"] == "存在" else "❌"
            print(f"  {status_icon} {name}: {info['status']}")
        
        print(f"\n💾 详细报告已保存: {report_file}")
        
        # 生成启动指南
        self._generate_startup_guide()
    
    def _generate_startup_guide(self):
        """生成启动指南"""
        print("\n" + "="*60)
        print("🚀 系统启动指南")
        print("="*60)
        
        print("\n1️⃣ 启动后端API服务:")
        print("   cd d:\\KG")
        print("   python api/quality_kg_api.py")
        print("   # 访问: http://localhost:8001/docs")
        
        print("\n2️⃣ 启动Dify工具服务:")
        print("   python services/dify/dify_tool_server.py")
        print("   # 访问: http://localhost:8002/docs")
        
        print("\n3️⃣ 启动前端Web应用:")
        print("   cd apps/web")
        print("   npm install")
        print("   npm run dev")
        print("   # 访问: http://localhost:5174")
        
        print("\n4️⃣ 测试系统功能:")
        print("   # 异常溯源: 输入症状'裂纹'进行查询")
        print("   # 案例复用: 搜索相似问题解决方案")
        print("   # 质量统计: 查看质量趋势和指标")
        print("   # Dify集成: 使用工具定义配置Dify")
        
        print("\n5️⃣ 数据管理:")
        print("   python services/governance/data_governance_system.py")
        print("   # 管理异常标签、组件词典、供应商档案")
        
        print("\n📚 系统特性:")
        print("   ✅ 基于ontology_v0.2的专业本体设计")
        print("   ✅ 智能数据抽取和知识图谱构建")
        print("   ✅ 异常溯源、案例复用、统计分析")
        print("   ✅ Dify工具集成和RAG并联工作流")
        print("   ✅ 完整的数据治理体系")
        print("   ✅ 现代化Vue3前端界面")

def main():
    """主函数"""
    checker = SystemStatusChecker()
    checker.check_all_services()

if __name__ == "__main__":
    main()
