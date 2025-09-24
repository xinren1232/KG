#!/usr/bin/env python3
"""
Dify工具集成 - 质量知识图谱工具
将知识图谱查询接口注册为Dify工具，实现RAG检索与图谱查询的并联工作流
"""
import json
import requests
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DifyToolBase(BaseModel):
    """Dify工具基类"""
    name: str
    description: str
    parameters: Dict[str, Any]

class AnomalyTraceToolInput(BaseModel):
    """异常溯源工具输入"""
    symptom: Optional[str] = Field(None, description="症状描述，如：裂纹、对焦失败、充电慢")
    anomaly_id: Optional[str] = Field(None, description="异常编号，如：A-20241231-37300344")
    factory: Optional[str] = Field(None, description="工厂名称，如：泰衡诺工厂")
    material_code: Optional[str] = Field(None, description="物料编码，如：37300344")

class CaseReuseToolInput(BaseModel):
    """案例复用工具输入"""
    symptom: str = Field(..., description="症状描述，如：裂纹、对焦失败、充电慢")
    component: Optional[str] = Field(None, description="组件名称，如：摄像头、电池、显示屏")
    similarity_threshold: float = Field(0.7, description="相似度阈值，范围0-1")

class QualityStatsToolInput(BaseModel):
    """质量统计工具输入"""
    factory: Optional[str] = Field(None, description="工厂名称过滤")
    project: Optional[str] = Field(None, description="项目名称过滤")
    group_by: str = Field("factory", description="分组维度：factory/project/material/supplier")

class ProcessLinkageToolInput(BaseModel):
    """流程联动工具输入"""
    anomaly_id: str = Field(..., description="异常编号")
    include_sop: bool = Field(True, description="是否包含SOP文档")
    include_test_cases: bool = Field(True, description="是否包含测试用例")

class QualityKGDifyTools:
    """质量知识图谱Dify工具集"""
    
    def __init__(self, api_base_url: str = "http://localhost:8001"):
        self.api_base_url = api_base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'QualityKG-Dify-Tools/1.0'
        })
    
    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        """获取所有工具定义"""
        return [
            self._get_anomaly_trace_tool_def(),
            self._get_case_reuse_tool_def(),
            self._get_quality_stats_tool_def(),
            self._get_process_linkage_tool_def(),
            self._get_entity_search_tool_def()
        ]
    
    def _get_anomaly_trace_tool_def(self) -> Dict[str, Any]:
        """异常溯源工具定义"""
        return {
            "name": "anomaly_trace",
            "description": "根据症状、异常编号等条件，追溯异常的完整路径：症状→异常→根因→对策→责任人，提供专业的质量分析",
            "parameters": {
                "type": "object",
                "properties": {
                    "symptom": {
                        "type": "string",
                        "description": "症状描述，如：裂纹、对焦失败、充电慢、显示异常等"
                    },
                    "anomaly_id": {
                        "type": "string",
                        "description": "异常编号，如：A-20241231-37300344（可选）"
                    },
                    "factory": {
                        "type": "string",
                        "description": "工厂名称，如：泰衡诺工厂（可选）"
                    },
                    "material_code": {
                        "type": "string",
                        "description": "物料编码，如：37300344（可选）"
                    }
                },
                "required": []
            }
        }
    
    def _get_case_reuse_tool_def(self) -> Dict[str, Any]:
        """案例复用工具定义"""
        return {
            "name": "case_reuse",
            "description": "根据症状和组件，查找相似的历史案例，提供解决方案复用建议，帮助快速解决质量问题",
            "parameters": {
                "type": "object",
                "properties": {
                    "symptom": {
                        "type": "string",
                        "description": "症状描述，如：裂纹、对焦失败、充电慢等"
                    },
                    "component": {
                        "type": "string",
                        "description": "组件名称，如：摄像头、电池、显示屏、触摸屏等（可选）"
                    },
                    "similarity_threshold": {
                        "type": "number",
                        "description": "相似度阈值，范围0-1，默认0.7",
                        "default": 0.7
                    }
                },
                "required": ["symptom"]
            }
        }
    
    def _get_quality_stats_tool_def(self) -> Dict[str, Any]:
        """质量统计工具定义"""
        return {
            "name": "quality_stats",
            "description": "按工厂、项目、时间等维度统计质量指标，提供趋势分析和改进建议，支持质量管理决策",
            "parameters": {
                "type": "object",
                "properties": {
                    "factory": {
                        "type": "string",
                        "description": "工厂名称过滤，如：泰衡诺工厂（可选）"
                    },
                    "project": {
                        "type": "string",
                        "description": "项目名称过滤，如：BG6（可选）"
                    },
                    "group_by": {
                        "type": "string",
                        "description": "分组维度：factory（工厂）/project（项目）/material（物料）/supplier（供应商）",
                        "enum": ["factory", "project", "material", "supplier"],
                        "default": "factory"
                    }
                },
                "required": []
            }
        }
    
    def _get_process_linkage_tool_def(self) -> Dict[str, Any]:
        """流程联动工具定义"""
        return {
            "name": "process_linkage",
            "description": "根据异常编号，查询相关的SOP文档、测试用例、流程状态等信息，实现质量流程联动",
            "parameters": {
                "type": "object",
                "properties": {
                    "anomaly_id": {
                        "type": "string",
                        "description": "异常编号，如：A-20241231-37300344"
                    },
                    "include_sop": {
                        "type": "boolean",
                        "description": "是否包含SOP文档，默认true",
                        "default": True
                    },
                    "include_test_cases": {
                        "type": "boolean",
                        "description": "是否包含测试用例，默认true",
                        "default": True
                    }
                },
                "required": ["anomaly_id"]
            }
        }
    
    def _get_entity_search_tool_def(self) -> Dict[str, Any]:
        """实体搜索工具定义"""
        return {
            "name": "entity_search",
            "description": "根据关键词搜索知识图谱中的实体，支持模糊匹配，帮助快速定位相关信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "搜索关键词，如：摄像头、裂纹、BG6等"
                    },
                    "entity_type": {
                        "type": "string",
                        "description": "实体类型过滤，如：Anomaly、Material、Symptom等（可选）"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "返回数量限制，默认10",
                        "default": 10
                    }
                },
                "required": ["query"]
            }
        }
    
    def anomaly_trace(self, **kwargs) -> str:
        """执行异常溯源"""
        try:
            # 构建请求参数
            params = {k: v for k, v in kwargs.items() if v is not None}
            
            response = self.session.post(
                f"{self.api_base_url}/kg/trace/anomaly",
                json=params
            )
            response.raise_for_status()
            
            data = response.json()
            
            # 格式化返回结果
            result = f"🎯 **异常溯源结果**\n\n"
            result += f"**异常标题**: {data['anomaly']['title']}\n"
            result += f"**严重程度**: {data['anomaly']['severity']}\n"
            result += f"**不良率**: {data['anomaly']['defect_rate']*100:.2f}%\n"
            result += f"**工厂**: {data['anomaly']['factory']}\n"
            result += f"**项目**: {data['anomaly']['project']}\n"
            result += f"**责任人**: {data['anomaly']['owner']}\n\n"
            
            result += f"🔗 **溯源路径**:\n"
            for i, step in enumerate(data['trace_path'], 1):
                result += f"{i}. {step['type']}: {step['name']}\n"
            
            result += f"\n💡 **解决建议**:\n"
            for i, rec in enumerate(data['recommendations'], 1):
                result += f"{i}. {rec}\n"
            
            if data['related_cases']:
                result += f"\n🔄 **相关案例** ({len(data['related_cases'])}个):\n"
                for case in data['related_cases'][:3]:  # 只显示前3个
                    result += f"- {case['title']} ({case['severity']})\n"
            
            return result
            
        except Exception as e:
            logger.error(f"异常溯源失败: {e}")
            return f"❌ 异常溯源查询失败: {str(e)}"
    
    def case_reuse(self, **kwargs) -> str:
        """执行案例复用"""
        try:
            response = self.session.post(
                f"{self.api_base_url}/kg/reuse/cases",
                json=kwargs
            )
            response.raise_for_status()
            
            data = response.json()
            
            result = f"📚 **相似案例复用结果**\n\n"
            result += f"找到 {len(data['similar_cases'])} 个相似案例:\n\n"
            
            for i, case in enumerate(data['similar_cases'][:5], 1):  # 显示前5个
                result += f"**案例 {i}**: {case['title']}\n"
                result += f"- 症状: {case['symptom']}\n"
                result += f"- 解决方案: {case['countermeasure']}\n"
                result += f"- 相似度: {case['similarity']*100:.0f}%\n\n"
            
            result += f"🎯 **复用建议**:\n"
            for i, suggestion in enumerate(data['reuse_suggestions'], 1):
                result += f"{i}. {suggestion['suggestion']} (置信度: {suggestion['confidence']*100:.0f}%)\n"
            
            return result
            
        except Exception as e:
            logger.error(f"案例复用失败: {e}")
            return f"❌ 案例复用查询失败: {str(e)}"
    
    def quality_stats(self, **kwargs) -> str:
        """执行质量统计"""
        try:
            response = self.session.post(
                f"{self.api_base_url}/kg/stats/quality",
                json=kwargs
            )
            response.raise_for_status()
            
            data = response.json()
            
            result = f"📊 **质量统计分析结果**\n\n"
            result += f"**总体概况**:\n"
            result += f"- 异常总数: {data['summary']['total_anomalies']}\n"
            result += f"- 平均不良率: {data['summary']['avg_defect_rate']*100:.2f}%\n"
            
            if 'severity_distribution' in data['summary']:
                result += f"- 严重程度分布: {data['summary']['severity_distribution']}\n"
            
            result += f"\n📈 **趋势分析**:\n"
            for trend in data['trends']:
                result += f"- {trend['date']}: {trend['anomaly_count']}个异常, 不良率{trend['defect_rate']*100:.2f}%\n"
            
            result += f"\n🔥 **主要问题**:\n"
            for i, issue in enumerate(data['top_issues'], 1):
                result += f"{i}. {issue['issue']} (影响: {issue['impact']})\n"
            
            result += f"\n💡 **改进建议**:\n"
            for i, rec in enumerate(data['recommendations'], 1):
                result += f"{i}. {rec}\n"
            
            return result
            
        except Exception as e:
            logger.error(f"质量统计失败: {e}")
            return f"❌ 质量统计查询失败: {str(e)}"
    
    def process_linkage(self, **kwargs) -> str:
        """执行流程联动"""
        try:
            response = self.session.post(
                f"{self.api_base_url}/kg/linkage/process",
                json=kwargs
            )
            response.raise_for_status()
            
            data = response.json()
            
            result = f"🔗 **流程联动结果**\n\n"
            result += f"**异常信息**: {data['anomaly_info']['title']}\n"
            result += f"**责任人**: {data['anomaly_info']['owner']}\n\n"
            
            if data['related_docs']:
                result += f"📄 **相关文档**:\n"
                for doc in data['related_docs']:
                    result += f"- {doc['type']}: {doc['title']}\n"
                result += "\n"
            
            if data['test_cases']:
                result += f"🧪 **测试用例**:\n"
                for tc in data['test_cases']:
                    result += f"- {tc['id']}: {tc['title']} ({tc['priority']})\n"
                result += "\n"
            
            result += f"⚙️ **流程状态**:\n"
            for step in data['process_flow']:
                status_icon = "✅" if step['status'] == 'completed' else "🔄" if step['status'] == 'in_progress' else "⏳"
                result += f"{step['step']}. {step['name']} {status_icon}\n"
            
            return result
            
        except Exception as e:
            logger.error(f"流程联动失败: {e}")
            return f"❌ 流程联动查询失败: {str(e)}"
    
    def entity_search(self, **kwargs) -> str:
        """执行实体搜索"""
        try:
            response = self.session.get(
                f"{self.api_base_url}/kg/search",
                params=kwargs
            )
            response.raise_for_status()
            
            data = response.json()
            
            result = f"🔍 **实体搜索结果**\n\n"
            result += f"找到 {data['total']} 个相关实体:\n\n"
            
            for i, entity in enumerate(data['results'], 1):
                result += f"**{i}. {entity['name']}**\n"
                result += f"- 类型: {entity['type']}\n"
                result += f"- 匹配度: {entity['score']*100:.0f}%\n"
                result += f"- 标识: {entity['key']}\n\n"
            
            return result
            
        except Exception as e:
            logger.error(f"实体搜索失败: {e}")
            return f"❌ 实体搜索失败: {str(e)}"

def main():
    """主函数 - 测试Dify工具集成"""
    tools = QualityKGDifyTools()
    
    # 输出工具定义（用于Dify配置）
    tool_definitions = tools.get_tool_definitions()
    
    print("🤖 质量知识图谱Dify工具定义:")
    print("=" * 50)
    
    for tool_def in tool_definitions:
        print(f"\n**工具名称**: {tool_def['name']}")
        print(f"**描述**: {tool_def['description']}")
        print(f"**参数**: {json.dumps(tool_def['parameters'], ensure_ascii=False, indent=2)}")
        print("-" * 30)
    
    # 测试工具调用
    print("\n🧪 测试工具调用:")
    print("=" * 50)
    
    # 测试异常溯源
    print("\n1. 测试异常溯源:")
    result = tools.anomaly_trace(symptom="裂纹")
    print(result)
    
    # 测试案例复用
    print("\n2. 测试案例复用:")
    result = tools.case_reuse(symptom="对焦失败", component="摄像头")
    print(result)

if __name__ == "__main__":
    main()
