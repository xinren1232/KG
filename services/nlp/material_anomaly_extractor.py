#!/usr/bin/env python3
"""
来料异常数据抽取器 (基于 ontology_v0.2)
专门处理来料异常Excel数据，按照新本体设计抽取实体和关系

实体类型：Factory, Project, Material, Anomaly, Symptom, RootCause, 
         Countermeasure, Owner, Supplier, Doc

关系类型：HAPPENED_IN, RELATED_TO, INVOLVES, HAS_SYMPTOM, HAS_ROOTCAUSE,
         RESOLVED_BY, OWNED_BY, SUPPLIED_BY, DOCUMENTED_IN
"""
import re
import json
import pandas as pd
from typing import Dict, List, Tuple, Optional, Any
from pathlib import Path
import logging
from datetime import datetime
from dataclasses import dataclass

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ExtractedEntity:
    """抽取的实体"""
    key: str
    type: str
    name: str
    properties: Dict[str, Any]

@dataclass
class ExtractedRelation:
    """抽取的关系"""
    source_key: str
    target_key: str
    relation_type: str
    properties: Dict[str, Any] = None

class MaterialAnomalyExtractor:
    """来料异常数据抽取器"""
    
    def __init__(self):
        self.field_mappings = self._load_field_mappings()
        self.entity_patterns = self._load_entity_patterns()
        self.vocabulary = self._load_vocabulary()
        
    def _load_field_mappings(self) -> Dict[str, str]:
        """加载字段映射关系"""
        return {
            # 工厂相关
            '工厂名称': 'factory_name',
            '工厂': 'factory_name',
            '发生地点': 'factory_name',
            
            # 项目相关
            '项目名称': 'project_name',
            '项目': 'project_name',
            '阶段': 'project_phase',
            '项目阶段': 'project_phase',
            
            # 物料相关
            '物料编码': 'material_code',
            '物料编码8码': 'material_code',
            '物料描述': 'material_desc',
            '物料名称': 'material_desc',
            '物料类别': 'material_category',
            
            # 异常相关
            '问题描述': 'anomaly_title',
            '异常描述': 'anomaly_title',
            '不良数量': 'defects_number',
            '不良率': 'defect_rate',
            '发现日期': 'anomaly_date',
            '位置': 'anomaly_position',
            '严重程度': 'severity',
            
            # 根因和对策
            '原因分析': 'root_cause',
            '根因描述': 'root_cause',
            '根本原因': 'root_cause',
            '临时措施': 'temp_countermeasure',
            '技术措施': 'tech_countermeasure',
            '管理措施': 'mgmt_countermeasure',
            '对策': 'countermeasure',
            
            # 责任人
            '问题分析责任人': 'owner_name',
            '责任人': 'owner_name',
            '处理人': 'owner_name',
            
            # 供应商
            '供应商': 'supplier_name',
            '供应商名称': 'supplier_name'
        }
    
    def _load_entity_patterns(self) -> Dict[str, List[str]]:
        """加载实体识别模式"""
        return {
            'Factory': [
                r'.*工厂$',
                r'.*厂区$',
                r'.*生产基地$',
                r'.*制造中心$'
            ],
            'Project': [
                r'[A-Z]{2,4}\d*',  # BG6, MP3等
                r'项目[A-Z0-9]+',
                r'[A-Z]+项目'
            ],
            'Material': [
                r'\d{8}',  # 8位物料编码
                r'\d{6,10}',  # 6-10位编码
                r'.*组件$',
                r'.*模块$',
                r'.*部件$'
            ],
            'Symptom': [
                r'裂纹|破损|变形|划伤|污染',
                r'不良|缺陷|异常|故障',
                r'.*失效$',
                r'.*不合格$'
            ],
            'RootCause': [
                r'.*导致.*',
                r'.*原因.*',
                r'.*不当.*',
                r'.*偏差.*',
                r'.*不足.*'
            ],
            'Countermeasure': [
                r'更换.*',
                r'调整.*',
                r'增加.*',
                r'改进.*',
                r'优化.*',
                r'.*措施$'
            ],
            'Owner': [
                r'[\u4e00-\u9fa5]{2,4}',  # 中文姓名2-4字
                r'[A-Za-z]+\s+[A-Za-z]+',  # 英文姓名
            ],
            'Supplier': [
                r'.*有限公司$',
                r'.*股份.*公司$',
                r'.*科技.*公司$',
                r'.*制造.*公司$',
                r'.*电子.*公司$'
            ]
        }
    
    def _load_vocabulary(self) -> Dict[str, List[str]]:
        """加载标准词汇表"""
        return {
            'severity_levels': ['S1', 'S2', 'S3', 'S4', '高', '中', '低'],
            'project_phases': ['设计', '开发', '试产', '量产', '维护'],
            'countermeasure_types': ['临时措施', '技术措施', '管理措施', '预防措施'],
            'material_categories': ['电池组件', '显示组件', '摄像头组件', '结构件', '电子器件'],
            'symptom_categories': ['外观缺陷', '功能异常', '性能不达标', '尺寸偏差']
        }
    
    def extract_from_excel(self, file_path: str) -> Dict[str, Any]:
        """从Excel文件抽取来料异常数据"""
        logger.info(f"开始抽取来料异常数据: {file_path}")
        
        try:
            # 读取Excel文件
            df = pd.read_excel(file_path)
            logger.info(f"读取到 {len(df)} 行数据，{len(df.columns)} 列")
            
            # 标准化列名
            df = self._normalize_columns(df)
            
            # 抽取实体和关系
            entities = []
            relations = []
            
            for index, row in df.iterrows():
                row_entities, row_relations = self._extract_from_row(row, index, file_path)
                entities.extend(row_entities)
                relations.extend(row_relations)
            
            # 去重
            entities = self._deduplicate_entities(entities)
            relations = self._deduplicate_relations(relations)
            
            result = {
                'entities': [entity.__dict__ for entity in entities],
                'relations': [relation.__dict__ for relation in relations],
                'metadata': {
                    'source_file': file_path,
                    'total_rows': len(df),
                    'entity_count': len(entities),
                    'relation_count': len(relations),
                    'extracted_at': datetime.now().isoformat()
                }
            }
            
            logger.info(f"抽取完成: {len(entities)} 个实体, {len(relations)} 个关系")
            return result
            
        except Exception as e:
            logger.error(f"抽取失败: {e}")
            raise
    
    def _normalize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """标准化列名"""
        column_mapping = {}
        
        for col in df.columns:
            if col in self.field_mappings:
                column_mapping[col] = self.field_mappings[col]
            else:
                # 尝试模糊匹配
                normalized = self._fuzzy_match_column(col)
                if normalized:
                    column_mapping[col] = normalized
        
        if column_mapping:
            df = df.rename(columns=column_mapping)
            logger.info(f"列名标准化: {column_mapping}")
        
        return df
    
    def _fuzzy_match_column(self, column_name: str) -> Optional[str]:
        """模糊匹配列名"""
        col_lower = column_name.lower()
        
        # 简单的关键词匹配
        if any(keyword in col_lower for keyword in ['工厂', 'factory']):
            return 'factory_name'
        elif any(keyword in col_lower for keyword in ['项目', 'project']):
            return 'project_name'
        elif any(keyword in col_lower for keyword in ['物料', 'material', '编码']):
            if '编码' in col_lower or 'code' in col_lower:
                return 'material_code'
            else:
                return 'material_desc'
        elif any(keyword in col_lower for keyword in ['问题', '异常', '描述']):
            return 'anomaly_title'
        elif any(keyword in col_lower for keyword in ['原因', '根因']):
            return 'root_cause'
        elif any(keyword in col_lower for keyword in ['措施', '对策']):
            return 'countermeasure'
        elif any(keyword in col_lower for keyword in ['责任人', '处理人']):
            return 'owner_name'
        elif any(keyword in col_lower for keyword in ['供应商']):
            return 'supplier_name'
        
        return None
    
    def _extract_from_row(self, row: pd.Series, row_index: int, file_path: str) -> Tuple[List[ExtractedEntity], List[ExtractedRelation]]:
        """从单行数据抽取实体和关系"""
        entities = []
        relations = []
        
        # 生成异常实体的唯一键
        anomaly_key = self._generate_anomaly_key(row, row_index)
        
        # 抽取工厂实体
        if 'factory_name' in row and pd.notna(row['factory_name']):
            factory_entity = self._extract_factory(row['factory_name'])
            entities.append(factory_entity)
            
            # 创建 HAPPENED_IN 关系
            relations.append(ExtractedRelation(
                source_key=anomaly_key,
                target_key=factory_entity.key,
                relation_type='HAPPENED_IN'
            ))
        
        # 抽取项目实体
        if 'project_name' in row and pd.notna(row['project_name']):
            project_entity = self._extract_project(row)
            entities.append(project_entity)
            
            # 创建 RELATED_TO 关系
            relations.append(ExtractedRelation(
                source_key=anomaly_key,
                target_key=project_entity.key,
                relation_type='RELATED_TO'
            ))
        
        # 抽取物料实体
        if ('material_code' in row and pd.notna(row['material_code'])) or \
           ('material_desc' in row and pd.notna(row['material_desc'])):
            material_entity = self._extract_material(row)
            entities.append(material_entity)
            
            # 创建 INVOLVES 关系
            relations.append(ExtractedRelation(
                source_key=anomaly_key,
                target_key=material_entity.key,
                relation_type='INVOLVES'
            ))
            
            # 抽取供应商实体（如果有）
            if 'supplier_name' in row and pd.notna(row['supplier_name']):
                supplier_entity = self._extract_supplier(row['supplier_name'])
                entities.append(supplier_entity)
                
                # 创建 SUPPLIED_BY 关系
                relations.append(ExtractedRelation(
                    source_key=material_entity.key,
                    target_key=supplier_entity.key,
                    relation_type='SUPPLIED_BY'
                ))
        
        # 抽取异常实体
        anomaly_entity = self._extract_anomaly(row, anomaly_key)
        entities.append(anomaly_entity)
        
        # 抽取症状实体
        symptoms = self._extract_symptoms(row)
        for symptom in symptoms:
            entities.append(symptom)
            relations.append(ExtractedRelation(
                source_key=anomaly_key,
                target_key=symptom.key,
                relation_type='HAS_SYMPTOM'
            ))
        
        # 抽取根因实体
        if 'root_cause' in row and pd.notna(row['root_cause']):
            root_cause_entity = self._extract_root_cause(row['root_cause'])
            entities.append(root_cause_entity)
            
            # 创建 HAS_ROOTCAUSE 关系
            relations.append(ExtractedRelation(
                source_key=anomaly_key,
                target_key=root_cause_entity.key,
                relation_type='HAS_ROOTCAUSE'
            ))
            
            # 抽取对策实体
            countermeasures = self._extract_countermeasures(row)
            for countermeasure in countermeasures:
                entities.append(countermeasure)
                relations.append(ExtractedRelation(
                    source_key=root_cause_entity.key,
                    target_key=countermeasure.key,
                    relation_type='RESOLVED_BY'
                ))
        
        # 抽取责任人实体
        if 'owner_name' in row and pd.notna(row['owner_name']):
            owner_entity = self._extract_owner(row['owner_name'])
            entities.append(owner_entity)
            
            # 创建 OWNED_BY 关系
            relations.append(ExtractedRelation(
                source_key=anomaly_key,
                target_key=owner_entity.key,
                relation_type='OWNED_BY'
            ))
        
        # 抽取文档实体
        doc_entity = self._extract_document(file_path)
        entities.append(doc_entity)
        
        # 创建 DOCUMENTED_IN 关系
        relations.append(ExtractedRelation(
            source_key=anomaly_key,
            target_key=doc_entity.key,
            relation_type='DOCUMENTED_IN'
        ))
        
        return entities, relations
    
    def _generate_anomaly_key(self, row: pd.Series, row_index: int) -> str:
        """生成异常实体的唯一键"""
        # 尝试从多个字段生成键
        if 'factory_name' in row and 'anomaly_date' in row and 'material_code' in row:
            factory = str(row['factory_name'])[:10] if pd.notna(row['factory_name']) else 'UNK'
            date = str(row['anomaly_date'])[:10] if pd.notna(row['anomaly_date']) else 'UNK'
            material = str(row['material_code']) if pd.notna(row['material_code']) else 'UNK'
            return f"Anomaly:{factory}-{date}-{material}"
        else:
            # 使用行索引作为后备方案
            return f"Anomaly:ROW-{row_index:04d}"
    
    def _extract_factory(self, factory_name: str) -> ExtractedEntity:
        """抽取工厂实体"""
        return ExtractedEntity(
            key=f"Factory:{factory_name}",
            type="Factory",
            name=factory_name,
            properties={
                'location': '中国'  # 默认值，可以后续扩展
            }
        )
    
    def _extract_project(self, row: pd.Series) -> ExtractedEntity:
        """抽取项目实体"""
        project_name = str(row['project_name'])
        properties = {}
        
        if 'project_phase' in row and pd.notna(row['project_phase']):
            properties['phase'] = str(row['project_phase'])
        
        return ExtractedEntity(
            key=f"Project:{project_name}",
            type="Project",
            name=project_name,
            properties=properties
        )
    
    def _extract_material(self, row: pd.Series) -> ExtractedEntity:
        """抽取物料实体"""
        if 'material_code' in row and pd.notna(row['material_code']):
            material_key = str(row['material_code'])
        else:
            material_key = str(row.get('material_desc', 'UNKNOWN'))[:20]
        
        properties = {}
        if 'material_code' in row and pd.notna(row['material_code']):
            properties['code'] = str(row['material_code'])
        if 'material_desc' in row and pd.notna(row['material_desc']):
            properties['desc'] = str(row['material_desc'])
        if 'material_category' in row and pd.notna(row['material_category']):
            properties['category'] = str(row['material_category'])
        
        return ExtractedEntity(
            key=f"Material:{material_key}",
            type="Material",
            name=properties.get('desc', material_key),
            properties=properties
        )
    
    def _extract_anomaly(self, row: pd.Series, anomaly_key: str) -> ExtractedEntity:
        """抽取异常实体"""
        properties = {}
        
        if 'anomaly_title' in row and pd.notna(row['anomaly_title']):
            properties['title'] = str(row['anomaly_title'])
        if 'defects_number' in row and pd.notna(row['defects_number']):
            properties['defects_number'] = int(row['defects_number'])
        if 'defect_rate' in row and pd.notna(row['defect_rate']):
            properties['defect_rate'] = float(row['defect_rate'])
        if 'anomaly_date' in row and pd.notna(row['anomaly_date']):
            properties['date'] = str(row['anomaly_date'])
        if 'anomaly_position' in row and pd.notna(row['anomaly_position']):
            properties['position'] = str(row['anomaly_position'])
        if 'severity' in row and pd.notna(row['severity']):
            properties['severity'] = str(row['severity'])
        
        return ExtractedEntity(
            key=anomaly_key,
            type="Anomaly",
            name=properties.get('title', anomaly_key),
            properties=properties
        )
    
    def _extract_symptoms(self, row: pd.Series) -> List[ExtractedEntity]:
        """抽取症状实体"""
        symptoms = []
        
        # 从异常描述中抽取症状
        if 'anomaly_title' in row and pd.notna(row['anomaly_title']):
            title = str(row['anomaly_title'])
            
            # 使用模式匹配抽取症状
            for pattern_list in self.entity_patterns['Symptom']:
                matches = re.findall(pattern_list, title, re.IGNORECASE)
                for match in matches:
                    symptom = ExtractedEntity(
                        key=f"Symptom:{match}",
                        type="Symptom",
                        name=match,
                        properties={'category': self._categorize_symptom(match)}
                    )
                    symptoms.append(symptom)
        
        return symptoms
    
    def _extract_root_cause(self, root_cause_text: str) -> ExtractedEntity:
        """抽取根因实体"""
        return ExtractedEntity(
            key=f"RootCause:{root_cause_text}",
            type="RootCause",
            name=root_cause_text,
            properties={
                'detail': root_cause_text,
                'probability': 0.8  # 默认概率
            }
        )
    
    def _extract_countermeasures(self, row: pd.Series) -> List[ExtractedEntity]:
        """抽取对策实体"""
        countermeasures = []
        
        # 检查不同类型的对策字段
        countermeasure_fields = [
            ('temp_countermeasure', '临时措施'),
            ('tech_countermeasure', '技术措施'),
            ('mgmt_countermeasure', '管理措施'),
            ('countermeasure', '对策')
        ]
        
        for field, cm_type in countermeasure_fields:
            if field in row and pd.notna(row[field]):
                cm_text = str(row[field])
                countermeasure = ExtractedEntity(
                    key=f"Countermeasure:{cm_text}",
                    type="Countermeasure",
                    name=cm_text,
                    properties={
                        'type': cm_type,
                        'effectiveness': 0.8  # 默认有效性
                    }
                )
                countermeasures.append(countermeasure)
        
        return countermeasures
    
    def _extract_owner(self, owner_name: str) -> ExtractedEntity:
        """抽取责任人实体"""
        return ExtractedEntity(
            key=f"Owner:{owner_name}",
            type="Owner",
            name=owner_name,
            properties={'role': '质量工程师'}  # 默认角色
        )
    
    def _extract_supplier(self, supplier_name: str) -> ExtractedEntity:
        """抽取供应商实体"""
        return ExtractedEntity(
            key=f"Supplier:{supplier_name}",
            type="Supplier",
            name=supplier_name,
            properties={}
        )
    
    def _extract_document(self, file_path: str) -> ExtractedEntity:
        """抽取文档实体"""
        file_name = Path(file_path).name
        return ExtractedEntity(
            key=f"Doc:{file_name}",
            type="Doc",
            name=file_name,
            properties={
                'title': file_name,
                'path': file_path,
                'type': 'Excel',
                'date': datetime.now().strftime('%Y-%m-%d')
            }
        )
    
    def _categorize_symptom(self, symptom: str) -> str:
        """症状分类"""
        if any(keyword in symptom for keyword in ['裂纹', '破损', '变形', '划伤']):
            return '外观缺陷'
        elif any(keyword in symptom for keyword in ['失效', '故障', '异常']):
            return '功能异常'
        elif any(keyword in symptom for keyword in ['不达标', '偏差']):
            return '性能不达标'
        else:
            return '其他'
    
    def _deduplicate_entities(self, entities: List[ExtractedEntity]) -> List[ExtractedEntity]:
        """实体去重"""
        seen_keys = set()
        unique_entities = []
        
        for entity in entities:
            if entity.key not in seen_keys:
                seen_keys.add(entity.key)
                unique_entities.append(entity)
        
        return unique_entities
    
    def _deduplicate_relations(self, relations: List[ExtractedRelation]) -> List[ExtractedRelation]:
        """关系去重"""
        seen_relations = set()
        unique_relations = []
        
        for relation in relations:
            relation_tuple = (relation.source_key, relation.target_key, relation.relation_type)
            if relation_tuple not in seen_relations:
                seen_relations.add(relation_tuple)
                unique_relations.append(relation)
        
        return unique_relations

def main():
    """主函数 - 测试抽取器"""
    extractor = MaterialAnomalyExtractor()
    
    # 测试文件
    test_file = "data/import/来料问题先后版.xlsx"
    
    if Path(test_file).exists():
        result = extractor.extract_from_excel(test_file)
        
        # 保存结果
        output_file = "data/processed/material_anomaly_extracted.json"
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 来料异常数据抽取完成!")
        print(f"📊 抽取结果: {result['metadata']['entity_count']} 个实体, {result['metadata']['relation_count']} 个关系")
        print(f"💾 结果已保存到: {output_file}")
    else:
        print(f"❌ 测试文件不存在: {test_file}")

if __name__ == "__main__":
    main()
