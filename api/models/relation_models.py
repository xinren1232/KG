#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
关系数据模型
"""

from pydantic import BaseModel, Field, validator
from typing import Literal, Optional, List
from datetime import datetime

class NodeRef(BaseModel):
    """节点引用"""
    name: str = Field(..., min_length=1, max_length=200, description="节点名称")
    category: Literal[
        'Symptom', 'RootCause', 'Solution', 'Component', 
        'TestCase', 'Metric', 'Tool', 'Material', 'Process', 'Role',
        '可靠性', '质量管理'
    ] = Field(..., description="节点分类")
    
    class Config:
        schema_extra = {
            "example": {
                "name": "电池盖裂纹",
                "category": "Symptom"
            }
        }


class RelationProps(BaseModel):
    """关系属性基类"""
    confidence: float = Field(..., ge=0.1, le=1.0, description="置信度 (0.1-1.0)")
    evidence: str = Field(..., min_length=10, max_length=500, description="证据描述")
    source: str = Field(default='manual', description="数据来源")
    doc_id: Optional[str] = Field(None, description="文档ID")
    chunk_id: Optional[str] = Field(None, description="文档切片ID")
    
    @validator('confidence')
    def validate_confidence(cls, v):
        """验证置信度"""
        if v < 0.6:
            # 低置信度会自动标记为plausible
            pass
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "confidence": 0.9,
                "evidence": "更换治具后，裂纹不良率从5%降至0.1%",
                "source": "manual"
            }
        }


class CausesProps(RelationProps):
    """CAUSES关系特有属性"""
    severity: Optional[Literal['P0', 'P1', 'P2', 'P3']] = Field(None, description="严重程度")
    phase: Optional[Literal['EVT', 'DVT', 'PVT', 'MP', 'Field']] = Field(None, description="阶段")
    
    class Config:
        schema_extra = {
            "example": {
                "confidence": 0.9,
                "evidence": "低温-10℃条件下AF失败率>35%",
                "source": "manual",
                "severity": "P1",
                "phase": "DVT"
            }
        }


class ResolvedByProps(RelationProps):
    """RESOLVED_BY关系特有属性"""
    effectiveness: float = Field(..., ge=0.0, le=1.0, description="有效性 (0-1)")
    risk: Literal['low', 'mid', 'high'] = Field(..., description="风险等级")
    cost_level: Literal['L', 'M', 'H'] = Field(..., description="成本等级")
    
    class Config:
        schema_extra = {
            "example": {
                "confidence": 0.9,
                "evidence": "更换治具后，裂纹不良率从5%降至0.1%",
                "source": "manual",
                "effectiveness": 0.95,
                "risk": "low",
                "cost_level": "M"
            }
        }


class PreventsProps(RelationProps):
    """PREVENTS关系特有属性"""
    evidence_level: Literal['lab', 'field', 'standard'] = Field(..., description="证据等级")
    
    class Config:
        schema_extra = {
            "example": {
                "confidence": 0.85,
                "evidence": "定期清洁可预防90%的裂纹问题",
                "source": "manual",
                "evidence_level": "field"
            }
        }


class DependsOnProps(RelationProps):
    """DEPENDS_ON关系特有属性"""
    criticality: Literal['blocker', 'major', 'minor'] = Field(..., description="关键性")
    interface: Optional[str] = Field(None, max_length=100, description="接口类型")
    
    class Config:
        schema_extra = {
            "example": {
                "confidence": 1.0,
                "evidence": "摄像头对焦功能依赖VCM马达",
                "source": "manual",
                "criticality": "blocker",
                "interface": "电气+机械"
            }
        }


class InteractsWithProps(RelationProps):
    """INTERACTS_WITH关系特有属性"""
    mode: Literal['EMC', 'thermal', 'mechanical', 'fw'] = Field(..., description="交互模式")
    direction: Literal['bidir'] = Field(default='bidir', description="方向")
    
    class Config:
        schema_extra = {
            "example": {
                "confidence": 0.8,
                "evidence": "天线与金属中框存在EMC干扰",
                "source": "manual",
                "mode": "EMC",
                "direction": "bidir"
            }
        }


class DetectsProps(RelationProps):
    """DETECTS关系特有属性"""
    coverage: float = Field(..., ge=0.0, le=1.0, description="覆盖率 (0-1)")
    env: Optional[str] = Field(None, max_length=200, description="测试环境")
    
    class Config:
        schema_extra = {
            "example": {
                "confidence": 0.9,
                "evidence": "该测试用例可检测95%的对焦问题",
                "source": "manual",
                "coverage": 0.95,
                "env": "常温25℃, 湿度50%"
            }
        }


class TestsProps(RelationProps):
    """TESTS关系特有属性"""
    method: Optional[str] = Field(None, max_length=100, description="测试方法")
    threshold: Optional[str] = Field(None, max_length=100, description="阈值")
    
    class Config:
        schema_extra = {
            "example": {
                "confidence": 0.9,
                "evidence": "使用标准测试流程验证组件功能",
                "source": "manual",
                "method": "功能测试",
                "threshold": "100%通过"
            }
        }


class MeasuresProps(RelationProps):
    """MEASURES关系特有属性"""
    method: Optional[str] = Field(None, max_length=100, description="测量方法")
    threshold: Optional[str] = Field(None, max_length=100, description="阈值")
    
    class Config:
        schema_extra = {
            "example": {
                "confidence": 0.9,
                "evidence": "使用标准仪器测量指标",
                "source": "manual",
                "method": "自动化测量",
                "threshold": "±5%"
            }
        }


class RelationInput(BaseModel):
    """关系输入"""
    relation_type: Literal[
        'CAUSES', 'RESOLVED_BY', 'PREVENTS', 
        'DEPENDS_ON', 'INTERACTS_WITH', 'DETECTS', 
        'TESTS', 'MEASURES', 'AFFECTS'
    ] = Field(..., description="关系类型")
    source: NodeRef = Field(..., description="源节点")
    target: NodeRef = Field(..., description="目标节点")
    props: dict = Field(..., description="关系属性")
    
    @validator('relation_type')
    def validate_relation_type(cls, v, values):
        """验证关系类型与节点类型的匹配"""
        if 'source' not in values or 'target' not in values:
            return v
        
        source_cat = values['source'].category
        target_cat = values['target'].category
        
        # 定义有效的关系组合
        valid_combinations = {
            'CAUSES': [
                ('Symptom', 'Symptom'),
                ('RootCause', 'Symptom'),
                ('Component', 'Symptom'),
                ('Process', 'Symptom'),
                ('Material', 'Symptom')
            ],
            'RESOLVED_BY': [('Symptom', 'Solution')],
            'PREVENTS': [('Solution', 'Symptom')],
            'DEPENDS_ON': [
                ('Component', 'Component'),
                ('Component', 'Material'),
                ('Component', 'Tool')
            ],
            'INTERACTS_WITH': [('Component', 'Component')],
            'DETECTS': [('TestCase', 'Symptom')],
            'TESTS': [
                ('TestCase', 'Component'),
                ('TestCase', 'Process')
            ],
            'MEASURES': [('TestCase', 'Metric')],
            'AFFECTS': [
                ('Component', 'Symptom'),
                ('Process', 'Symptom'),
                ('Material', 'Symptom')
            ]
        }
        
        if v in valid_combinations:
            valid_pairs = valid_combinations[v]
            if (source_cat, target_cat) not in valid_pairs:
                raise ValueError(
                    f'{v} 关系要求 {valid_pairs} 之一, '
                    f'但得到 ({source_cat}, {target_cat})'
                )
        
        return v
    
    @validator('props')
    def validate_props(cls, v, values):
        """验证属性是否包含必需字段"""
        if 'relation_type' not in values:
            return v
        
        rel_type = values['relation_type']
        
        # 检查必需字段
        required_fields = ['confidence', 'evidence']
        for field in required_fields:
            if field not in v:
                raise ValueError(f'{rel_type} 关系缺少必需字段: {field}')
        
        # 检查置信度范围
        if not (0.1 <= v['confidence'] <= 1.0):
            raise ValueError(f'confidence 必须在 0.1-1.0 之间，得到 {v["confidence"]}')
        
        # 检查证据长度
        if len(v['evidence']) < 10:
            raise ValueError(f'evidence 至少需要10个字符，得到 {len(v["evidence"])}')
        
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "relation_type": "RESOLVED_BY",
                "source": {
                    "name": "电池盖裂纹",
                    "category": "Symptom"
                },
                "target": {
                    "name": "更换治具并清洁",
                    "category": "Solution"
                },
                "props": {
                    "confidence": 0.9,
                    "evidence": "更换治具后，裂纹不良率从5%降至0.1%",
                    "source": "manual",
                    "effectiveness": 0.95,
                    "risk": "low",
                    "cost_level": "M"
                }
            }
        }


class RelationBatch(BaseModel):
    """批量关系输入"""
    relations: List[RelationInput] = Field(..., min_items=1, max_items=100, description="关系列表")
    
    class Config:
        schema_extra = {
            "example": {
                "relations": [
                    {
                        "relation_type": "RESOLVED_BY",
                        "source": {"name": "电池盖裂纹", "category": "Symptom"},
                        "target": {"name": "更换治具并清洁", "category": "Solution"},
                        "props": {
                            "confidence": 0.9,
                            "evidence": "更换治具后，裂纹不良率从5%降至0.1%",
                            "effectiveness": 0.95,
                            "risk": "low",
                            "cost_level": "M"
                        }
                    }
                ]
            }
        }

