#!/usr/bin/env python3
"""
数据治理体系
建立异常标签、组件词典、供应商管理等数据治理机制，支持持续优化和维护
"""
import json
import pandas as pd
from typing import Dict, List, Any, Optional, Set
from pathlib import Path
from datetime import datetime, date
import logging
from dataclasses import dataclass, asdict
from enum import Enum

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataQualityLevel(Enum):
    """数据质量等级"""
    EXCELLENT = "优秀"
    GOOD = "良好"
    FAIR = "一般"
    POOR = "较差"

class EntityStatus(Enum):
    """实体状态"""
    ACTIVE = "活跃"
    INACTIVE = "非活跃"
    DEPRECATED = "已废弃"
    PENDING = "待审核"

@dataclass
class AnomalyLabel:
    """异常标签"""
    id: str
    name: str
    category: str
    severity: str
    description: str
    keywords: List[str]
    created_at: str
    updated_at: str
    status: str = EntityStatus.ACTIVE.value

@dataclass
class ComponentDictionary:
    """组件词典"""
    id: str
    name: str
    category: str
    subcategory: str
    aliases: List[str]
    specifications: Dict[str, Any]
    suppliers: List[str]
    created_at: str
    updated_at: str
    status: str = EntityStatus.ACTIVE.value

@dataclass
class SupplierProfile:
    """供应商档案"""
    id: str
    name: str
    contact_info: Dict[str, str]
    business_scope: List[str]
    quality_rating: str
    certification: List[str]
    risk_level: str
    components_supplied: List[str]
    performance_metrics: Dict[str, float]
    created_at: str
    updated_at: str
    status: str = EntityStatus.ACTIVE.value

@dataclass
class DataQualityMetrics:
    """数据质量指标"""
    entity_type: str
    total_count: int
    complete_count: int
    duplicate_count: int
    invalid_count: int
    completeness_rate: float
    accuracy_rate: float
    consistency_rate: float
    quality_level: str
    last_check: str

class DataGovernanceSystem:
    """数据治理系统"""
    
    def __init__(self, data_dir: str = "data/governance"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # 初始化各个治理组件
        self.anomaly_labels: Dict[str, AnomalyLabel] = {}
        self.component_dict: Dict[str, ComponentDictionary] = {}
        self.supplier_profiles: Dict[str, SupplierProfile] = {}
        self.quality_metrics: Dict[str, DataQualityMetrics] = {}
        
        # 加载现有数据
        self._load_governance_data()
    
    def _load_governance_data(self):
        """加载治理数据"""
        try:
            # 加载异常标签
            labels_file = self.data_dir / "anomaly_labels.json"
            if labels_file.exists():
                with open(labels_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.anomaly_labels = {k: AnomalyLabel(**v) for k, v in data.items()}
            
            # 加载组件词典
            components_file = self.data_dir / "component_dictionary.json"
            if components_file.exists():
                with open(components_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.component_dict = {k: ComponentDictionary(**v) for k, v in data.items()}
            
            # 加载供应商档案
            suppliers_file = self.data_dir / "supplier_profiles.json"
            if suppliers_file.exists():
                with open(suppliers_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.supplier_profiles = {k: SupplierProfile(**v) for k, v in data.items()}
            
            logger.info(f"加载治理数据完成: {len(self.anomaly_labels)}个标签, {len(self.component_dict)}个组件, {len(self.supplier_profiles)}个供应商")
            
        except Exception as e:
            logger.error(f"加载治理数据失败: {e}")
    
    def _save_governance_data(self):
        """保存治理数据"""
        try:
            # 保存异常标签
            labels_file = self.data_dir / "anomaly_labels.json"
            with open(labels_file, 'w', encoding='utf-8') as f:
                data = {k: asdict(v) for k, v in self.anomaly_labels.items()}
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            # 保存组件词典
            components_file = self.data_dir / "component_dictionary.json"
            with open(components_file, 'w', encoding='utf-8') as f:
                data = {k: asdict(v) for k, v in self.component_dict.items()}
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            # 保存供应商档案
            suppliers_file = self.data_dir / "supplier_profiles.json"
            with open(suppliers_file, 'w', encoding='utf-8') as f:
                data = {k: asdict(v) for k, v in self.supplier_profiles.items()}
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            logger.info("治理数据保存完成")
            
        except Exception as e:
            logger.error(f"保存治理数据失败: {e}")
    
    def initialize_standard_data(self):
        """初始化标准数据"""
        logger.info("初始化标准治理数据...")
        
        # 初始化异常标签
        self._init_anomaly_labels()
        
        # 初始化组件词典
        self._init_component_dictionary()
        
        # 初始化供应商档案
        self._init_supplier_profiles()
        
        # 保存数据
        self._save_governance_data()
        
        logger.info("标准治理数据初始化完成")
    
    def _init_anomaly_labels(self):
        """初始化异常标签"""
        standard_labels = [
            {
                "id": "AL001",
                "name": "外观缺陷",
                "category": "质量问题",
                "severity": "S2",
                "description": "产品外观存在可见缺陷",
                "keywords": ["裂纹", "划伤", "变形", "污染", "破损"]
            },
            {
                "id": "AL002",
                "name": "功能异常",
                "category": "质量问题",
                "severity": "S1",
                "description": "产品功能无法正常工作",
                "keywords": ["对焦失败", "充电异常", "触摸不灵敏", "音质异常"]
            },
            {
                "id": "AL003",
                "name": "性能不达标",
                "category": "质量问题",
                "severity": "S2",
                "description": "产品性能指标未达到要求",
                "keywords": ["响应慢", "续航短", "信号弱", "发热严重"]
            },
            {
                "id": "AL004",
                "name": "尺寸偏差",
                "category": "质量问题",
                "severity": "S3",
                "description": "产品尺寸超出公差范围",
                "keywords": ["尺寸超差", "装配困难", "间隙过大", "配合不良"]
            },
            {
                "id": "AL005",
                "name": "工艺问题",
                "category": "制造问题",
                "severity": "S2",
                "description": "制造工艺存在问题",
                "keywords": ["压合不良", "焊接缺陷", "涂装不均", "组装错误"]
            }
        ]
        
        for label_data in standard_labels:
            label = AnomalyLabel(
                **label_data,
                created_at=datetime.now().isoformat(),
                updated_at=datetime.now().isoformat()
            )
            self.anomaly_labels[label.id] = label
    
    def _init_component_dictionary(self):
        """初始化组件词典"""
        standard_components = [
            {
                "id": "CP001",
                "name": "摄像头",
                "category": "光学组件",
                "subcategory": "主摄像头",
                "aliases": ["相机", "Camera", "镜头"],
                "specifications": {"分辨率": "108MP", "光圈": "f/1.8", "焦距": "26mm"},
                "suppliers": ["YY光学有限公司", "ZZ精密制造"]
            },
            {
                "id": "CP002",
                "name": "电池",
                "category": "电源组件",
                "subcategory": "锂电池",
                "aliases": ["电芯", "Battery", "蓄电池"],
                "specifications": {"容量": "5000mAh", "电压": "3.85V", "类型": "锂聚合物"},
                "suppliers": ["AA电池科技", "BB能源公司"]
            },
            {
                "id": "CP003",
                "name": "显示屏",
                "category": "显示组件",
                "subcategory": "OLED屏幕",
                "aliases": ["屏幕", "Display", "LCD", "OLED"],
                "specifications": {"尺寸": "6.7英寸", "分辨率": "2400x1080", "刷新率": "120Hz"},
                "suppliers": ["CC显示技术", "DD光电公司"]
            },
            {
                "id": "CP004",
                "name": "触摸屏",
                "category": "交互组件",
                "subcategory": "电容触摸",
                "aliases": ["触控", "Touch", "触摸面板"],
                "specifications": {"技术": "电容式", "多点触控": "10点", "响应时间": "1ms"},
                "suppliers": ["EE触控科技", "FF交互技术"]
            },
            {
                "id": "CP005",
                "name": "扬声器",
                "category": "音频组件",
                "subcategory": "立体声扬声器",
                "aliases": ["喇叭", "Speaker", "音响"],
                "specifications": {"功率": "1W", "频响": "20Hz-20kHz", "阻抗": "8Ω"},
                "suppliers": ["GG音响技术", "HH声学公司"]
            }
        ]
        
        for comp_data in standard_components:
            component = ComponentDictionary(
                **comp_data,
                created_at=datetime.now().isoformat(),
                updated_at=datetime.now().isoformat()
            )
            self.component_dict[component.id] = component
    
    def _init_supplier_profiles(self):
        """初始化供应商档案"""
        standard_suppliers = [
            {
                "id": "SP001",
                "name": "XX精密制造有限公司",
                "contact_info": {"电话": "0755-12345678", "邮箱": "contact@xx-precision.com", "地址": "深圳市南山区"},
                "business_scope": ["结构件", "精密加工", "模具制造"],
                "quality_rating": "A",
                "certification": ["ISO9001", "ISO14001", "IATF16949"],
                "risk_level": "低",
                "components_supplied": ["CP001", "CP003"],
                "performance_metrics": {"准时交付率": 0.95, "质量合格率": 0.98, "成本竞争力": 0.85}
            },
            {
                "id": "SP002",
                "name": "YY光学有限公司",
                "contact_info": {"电话": "0512-87654321", "邮箱": "info@yy-optics.com", "地址": "苏州市工业园区"},
                "business_scope": ["光学器件", "镜头组装", "光学测试"],
                "quality_rating": "A+",
                "certification": ["ISO9001", "ISO14001", "RoHS"],
                "risk_level": "低",
                "components_supplied": ["CP001"],
                "performance_metrics": {"准时交付率": 0.98, "质量合格率": 0.99, "成本竞争力": 0.80}
            },
            {
                "id": "SP003",
                "name": "ZZ电子有限公司",
                "contact_info": {"电话": "021-11223344", "邮箱": "sales@zz-electronics.com", "地址": "上海市浦东新区"},
                "business_scope": ["电子元器件", "PCB制造", "SMT贴装"],
                "quality_rating": "B+",
                "certification": ["ISO9001", "UL认证"],
                "risk_level": "中",
                "components_supplied": ["CP002", "CP004", "CP005"],
                "performance_metrics": {"准时交付率": 0.90, "质量合格率": 0.95, "成本竞争力": 0.90}
            }
        ]
        
        for supplier_data in standard_suppliers:
            supplier = SupplierProfile(
                **supplier_data,
                created_at=datetime.now().isoformat(),
                updated_at=datetime.now().isoformat()
            )
            self.supplier_profiles[supplier.id] = supplier
    
    def add_anomaly_label(self, name: str, category: str, severity: str, 
                         description: str, keywords: List[str]) -> str:
        """添加异常标签"""
        label_id = f"AL{len(self.anomaly_labels) + 1:03d}"
        
        label = AnomalyLabel(
            id=label_id,
            name=name,
            category=category,
            severity=severity,
            description=description,
            keywords=keywords,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
        
        self.anomaly_labels[label_id] = label
        self._save_governance_data()
        
        logger.info(f"添加异常标签: {label_id} - {name}")
        return label_id
    
    def add_component(self, name: str, category: str, subcategory: str,
                     aliases: List[str], specifications: Dict[str, Any],
                     suppliers: List[str]) -> str:
        """添加组件"""
        comp_id = f"CP{len(self.component_dict) + 1:03d}"
        
        component = ComponentDictionary(
            id=comp_id,
            name=name,
            category=category,
            subcategory=subcategory,
            aliases=aliases,
            specifications=specifications,
            suppliers=suppliers,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
        
        self.component_dict[comp_id] = component
        self._save_governance_data()
        
        logger.info(f"添加组件: {comp_id} - {name}")
        return comp_id
    
    def add_supplier(self, name: str, contact_info: Dict[str, str],
                    business_scope: List[str], quality_rating: str,
                    certification: List[str], risk_level: str,
                    components_supplied: List[str],
                    performance_metrics: Dict[str, float]) -> str:
        """添加供应商"""
        supplier_id = f"SP{len(self.supplier_profiles) + 1:03d}"
        
        supplier = SupplierProfile(
            id=supplier_id,
            name=name,
            contact_info=contact_info,
            business_scope=business_scope,
            quality_rating=quality_rating,
            certification=certification,
            risk_level=risk_level,
            components_supplied=components_supplied,
            performance_metrics=performance_metrics,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
        
        self.supplier_profiles[supplier_id] = supplier
        self._save_governance_data()
        
        logger.info(f"添加供应商: {supplier_id} - {name}")
        return supplier_id
    
    def search_anomaly_labels(self, keyword: str) -> List[AnomalyLabel]:
        """搜索异常标签"""
        results = []
        keyword_lower = keyword.lower()
        
        for label in self.anomaly_labels.values():
            if (keyword_lower in label.name.lower() or
                keyword_lower in label.description.lower() or
                any(keyword_lower in kw.lower() for kw in label.keywords)):
                results.append(label)
        
        return results
    
    def search_components(self, keyword: str) -> List[ComponentDictionary]:
        """搜索组件"""
        results = []
        keyword_lower = keyword.lower()
        
        for component in self.component_dict.values():
            if (keyword_lower in component.name.lower() or
                keyword_lower in component.category.lower() or
                any(keyword_lower in alias.lower() for alias in component.aliases)):
                results.append(component)
        
        return results
    
    def search_suppliers(self, keyword: str) -> List[SupplierProfile]:
        """搜索供应商"""
        results = []
        keyword_lower = keyword.lower()
        
        for supplier in self.supplier_profiles.values():
            if (keyword_lower in supplier.name.lower() or
                any(keyword_lower in scope.lower() for scope in supplier.business_scope)):
                results.append(supplier)
        
        return results
    
    def check_data_quality(self) -> Dict[str, DataQualityMetrics]:
        """检查数据质量"""
        logger.info("开始数据质量检查...")
        
        # 检查异常标签质量
        labels_metrics = self._check_anomaly_labels_quality()
        self.quality_metrics["anomaly_labels"] = labels_metrics
        
        # 检查组件词典质量
        components_metrics = self._check_components_quality()
        self.quality_metrics["components"] = components_metrics
        
        # 检查供应商档案质量
        suppliers_metrics = self._check_suppliers_quality()
        self.quality_metrics["suppliers"] = suppliers_metrics
        
        # 保存质量指标
        self._save_quality_metrics()
        
        logger.info("数据质量检查完成")
        return self.quality_metrics
    
    def _check_anomaly_labels_quality(self) -> DataQualityMetrics:
        """检查异常标签质量"""
        total_count = len(self.anomaly_labels)
        complete_count = 0
        duplicate_count = 0
        invalid_count = 0
        
        names = set()
        for label in self.anomaly_labels.values():
            # 检查完整性
            if (label.name and label.category and label.severity and 
                label.description and label.keywords):
                complete_count += 1
            
            # 检查重复
            if label.name in names:
                duplicate_count += 1
            else:
                names.add(label.name)
            
            # 检查有效性
            if label.severity not in ["S1", "S2", "S3", "S4"]:
                invalid_count += 1
        
        completeness_rate = complete_count / total_count if total_count > 0 else 0
        accuracy_rate = (total_count - invalid_count) / total_count if total_count > 0 else 0
        consistency_rate = (total_count - duplicate_count) / total_count if total_count > 0 else 0
        
        # 计算质量等级
        avg_rate = (completeness_rate + accuracy_rate + consistency_rate) / 3
        if avg_rate >= 0.9:
            quality_level = DataQualityLevel.EXCELLENT.value
        elif avg_rate >= 0.8:
            quality_level = DataQualityLevel.GOOD.value
        elif avg_rate >= 0.7:
            quality_level = DataQualityLevel.FAIR.value
        else:
            quality_level = DataQualityLevel.POOR.value
        
        return DataQualityMetrics(
            entity_type="anomaly_labels",
            total_count=total_count,
            complete_count=complete_count,
            duplicate_count=duplicate_count,
            invalid_count=invalid_count,
            completeness_rate=completeness_rate,
            accuracy_rate=accuracy_rate,
            consistency_rate=consistency_rate,
            quality_level=quality_level,
            last_check=datetime.now().isoformat()
        )
    
    def _check_components_quality(self) -> DataQualityMetrics:
        """检查组件词典质量"""
        total_count = len(self.component_dict)
        complete_count = 0
        duplicate_count = 0
        invalid_count = 0
        
        names = set()
        for component in self.component_dict.values():
            # 检查完整性
            if (component.name and component.category and component.subcategory and
                component.aliases and component.specifications):
                complete_count += 1
            
            # 检查重复
            if component.name in names:
                duplicate_count += 1
            else:
                names.add(component.name)
            
            # 检查有效性（这里简化处理）
            if not component.suppliers:
                invalid_count += 1
        
        completeness_rate = complete_count / total_count if total_count > 0 else 0
        accuracy_rate = (total_count - invalid_count) / total_count if total_count > 0 else 0
        consistency_rate = (total_count - duplicate_count) / total_count if total_count > 0 else 0
        
        # 计算质量等级
        avg_rate = (completeness_rate + accuracy_rate + consistency_rate) / 3
        if avg_rate >= 0.9:
            quality_level = DataQualityLevel.EXCELLENT.value
        elif avg_rate >= 0.8:
            quality_level = DataQualityLevel.GOOD.value
        elif avg_rate >= 0.7:
            quality_level = DataQualityLevel.FAIR.value
        else:
            quality_level = DataQualityLevel.POOR.value
        
        return DataQualityMetrics(
            entity_type="components",
            total_count=total_count,
            complete_count=complete_count,
            duplicate_count=duplicate_count,
            invalid_count=invalid_count,
            completeness_rate=completeness_rate,
            accuracy_rate=accuracy_rate,
            consistency_rate=consistency_rate,
            quality_level=quality_level,
            last_check=datetime.now().isoformat()
        )
    
    def _check_suppliers_quality(self) -> DataQualityMetrics:
        """检查供应商档案质量"""
        total_count = len(self.supplier_profiles)
        complete_count = 0
        duplicate_count = 0
        invalid_count = 0
        
        names = set()
        for supplier in self.supplier_profiles.values():
            # 检查完整性
            if (supplier.name and supplier.contact_info and supplier.business_scope and
                supplier.quality_rating and supplier.performance_metrics):
                complete_count += 1
            
            # 检查重复
            if supplier.name in names:
                duplicate_count += 1
            else:
                names.add(supplier.name)
            
            # 检查有效性
            if supplier.quality_rating not in ["A+", "A", "B+", "B", "C"]:
                invalid_count += 1
        
        completeness_rate = complete_count / total_count if total_count > 0 else 0
        accuracy_rate = (total_count - invalid_count) / total_count if total_count > 0 else 0
        consistency_rate = (total_count - duplicate_count) / total_count if total_count > 0 else 0
        
        # 计算质量等级
        avg_rate = (completeness_rate + accuracy_rate + consistency_rate) / 3
        if avg_rate >= 0.9:
            quality_level = DataQualityLevel.EXCELLENT.value
        elif avg_rate >= 0.8:
            quality_level = DataQualityLevel.GOOD.value
        elif avg_rate >= 0.7:
            quality_level = DataQualityLevel.FAIR.value
        else:
            quality_level = DataQualityLevel.POOR.value
        
        return DataQualityMetrics(
            entity_type="suppliers",
            total_count=total_count,
            complete_count=complete_count,
            duplicate_count=duplicate_count,
            invalid_count=invalid_count,
            completeness_rate=completeness_rate,
            accuracy_rate=accuracy_rate,
            consistency_rate=consistency_rate,
            quality_level=quality_level,
            last_check=datetime.now().isoformat()
        )
    
    def _save_quality_metrics(self):
        """保存质量指标"""
        try:
            metrics_file = self.data_dir / "quality_metrics.json"
            with open(metrics_file, 'w', encoding='utf-8') as f:
                data = {k: asdict(v) for k, v in self.quality_metrics.items()}
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            logger.info("质量指标保存完成")
            
        except Exception as e:
            logger.error(f"保存质量指标失败: {e}")
    
    def generate_governance_report(self) -> Dict[str, Any]:
        """生成治理报告"""
        logger.info("生成数据治理报告...")
        
        # 检查数据质量
        quality_metrics = self.check_data_quality()
        
        report = {
            "report_info": {
                "generated_at": datetime.now().isoformat(),
                "report_type": "数据治理报告",
                "version": "1.0"
            },
            "summary": {
                "anomaly_labels_count": len(self.anomaly_labels),
                "components_count": len(self.component_dict),
                "suppliers_count": len(self.supplier_profiles),
                "overall_quality": self._calculate_overall_quality(quality_metrics)
            },
            "quality_metrics": {k: asdict(v) for k, v in quality_metrics.items()},
            "recommendations": self._generate_recommendations(quality_metrics)
        }
        
        # 保存报告
        report_file = self.data_dir / f"governance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        logger.info(f"治理报告已生成: {report_file}")
        return report
    
    def _calculate_overall_quality(self, metrics: Dict[str, DataQualityMetrics]) -> str:
        """计算整体质量等级"""
        if not metrics:
            return DataQualityLevel.POOR.value
        
        total_score = 0
        for metric in metrics.values():
            avg_rate = (metric.completeness_rate + metric.accuracy_rate + metric.consistency_rate) / 3
            total_score += avg_rate
        
        avg_score = total_score / len(metrics)
        
        if avg_score >= 0.9:
            return DataQualityLevel.EXCELLENT.value
        elif avg_score >= 0.8:
            return DataQualityLevel.GOOD.value
        elif avg_score >= 0.7:
            return DataQualityLevel.FAIR.value
        else:
            return DataQualityLevel.POOR.value
    
    def _generate_recommendations(self, metrics: Dict[str, DataQualityMetrics]) -> List[str]:
        """生成改进建议"""
        recommendations = []
        
        for entity_type, metric in metrics.items():
            if metric.completeness_rate < 0.8:
                recommendations.append(f"提高{entity_type}的数据完整性，当前完整率仅{metric.completeness_rate:.1%}")
            
            if metric.accuracy_rate < 0.8:
                recommendations.append(f"改善{entity_type}的数据准确性，当前准确率仅{metric.accuracy_rate:.1%}")
            
            if metric.consistency_rate < 0.8:
                recommendations.append(f"消除{entity_type}的重复数据，当前一致性率仅{metric.consistency_rate:.1%}")
        
        if not recommendations:
            recommendations.append("数据质量良好，建议继续保持现有的治理标准")
        
        return recommendations

def main():
    """主函数 - 测试数据治理系统"""
    governance = DataGovernanceSystem()
    
    # 初始化标准数据
    governance.initialize_standard_data()
    
    # 生成治理报告
    report = governance.generate_governance_report()
    
    print("🏛️ 数据治理系统测试完成!")
    print(f"📊 治理概况:")
    print(f"  - 异常标签: {report['summary']['anomaly_labels_count']} 个")
    print(f"  - 组件词典: {report['summary']['components_count']} 个")
    print(f"  - 供应商档案: {report['summary']['suppliers_count']} 个")
    print(f"  - 整体质量: {report['summary']['overall_quality']}")
    
    print(f"\n💡 改进建议:")
    for i, rec in enumerate(report['recommendations'], 1):
        print(f"  {i}. {rec}")

if __name__ == "__main__":
    main()
