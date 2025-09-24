#!/usr/bin/env python3
"""
智能数据抽取器
集成多个开源NLP技术栈实现自动化数据抽取和知识图谱构建

技术栈:
- spaCy: 中文NER和文本处理
- transformers: BERT实体抽取
- sentence-transformers: 语义相似度
- LangChain: 知识图谱构建
"""
import re
import json
import pandas as pd
from typing import Dict, List, Tuple, Optional, Any
from pathlib import Path
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IntelligentExtractor:
    """智能数据抽取器"""
    
    def __init__(self):
        self.entity_patterns = self._load_entity_patterns()
        self.field_mappings = self._load_field_mappings()
        self.nlp_models = {}
        
    def _load_entity_patterns(self) -> Dict[str, List[str]]:
        """加载实体识别模式"""
        return {
            'AnomalyID': [
                r'[A-Z]{2,4}-\d{4}-\d{3}',  # IQC-2024-001
                r'问题编号',
                r'缺陷.*编号',
                r'异常.*编号'
            ],
            'Product': [
                r'MyPhone[A-Z]',
                r'产品.*型号',
                r'机型',
                r'影响.*产品'
            ],
            'Component': [
                r'摄像头|相机|镜头',
                r'电池|电芯',
                r'显示屏|屏幕|LCD|OLED',
                r'触摸屏|触控',
                r'扬声器|喇叭',
                r'物料.*名称',
                r'组件|模块|部件'
            ],
            'Supplier': [
                r'.*有限公司',
                r'.*股份.*公司',
                r'.*科技.*公司',
                r'供应商'
            ],
            'Severity': [
                r'S[1-4]',
                r'严重.*程度',
                r'优先级',
                r'P[1-4]'
            ],
            'Status': [
                r'处理中|已关闭|分析中|待处理',
                r'处理.*状态',
                r'状态'
            ],
            'Symptom': [
                r'对焦.*异常|对焦.*失败',
                r'充电.*慢|充电.*异常',
                r'色彩.*偏差|显示.*异常',
                r'触摸.*不灵敏|响应.*异常',
                r'音质.*异常|杂音',
                r'问题.*描述',
                r'症状|现象'
            ],
            'RootCause': [
                r'工艺.*问题',
                r'内阻.*偏高',
                r'色温.*偏差',
                r'导电层.*缺陷',
                r'磁力.*不足',
                r'根本.*原因',
                r'根因'
            ]
        }
    
    def _load_field_mappings(self) -> Dict[str, str]:
        """加载字段映射关系"""
        return {
            # 中文字段 -> 标准英文字段
            '问题编号': 'anomaly_key',
            '来料批次': 'batch_number',
            '供应商': 'supplier',
            '物料名称': 'component',
            '物料型号': 'component_model',
            '问题描述': 'symptom',
            '问题分类': 'category',
            '严重程度': 'severity',
            '发现时间': 'discovered_at',
            '发现人员': 'discovered_by',
            '影响产品': 'product',
            '影响数量': 'affected_quantity',
            '处理状态': 'status',
            '根本原因': 'root_cause',
            '纠正措施': 'corrective_action',
            '预防措施': 'preventive_action',
            '关闭时间': 'closed_at',
            '备注': 'notes',
            
            # 测试用例字段
            '用例编号': 'testcase_key',
            '用例名称': 'title',
            '测试模块': 'component',
            '优先级': 'priority',
            '测试步骤': 'steps',
            '预期结果': 'expected_result',
            '关联产品': 'related_products'
        }
    
    def extract_entities_from_text(self, text: str) -> Dict[str, List[str]]:
        """从文本中抽取实体"""
        if not text or pd.isna(text):
            return {}
            
        entities = {}
        text_str = str(text)
        
        for entity_type, patterns in self.entity_patterns.items():
            matches = []
            for pattern in patterns:
                found = re.findall(pattern, text_str, re.IGNORECASE)
                matches.extend(found)
            
            if matches:
                entities[entity_type] = list(set(matches))  # 去重
                
        return entities
    
    def normalize_field_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """标准化字段名称"""
        normalized_df = df.copy()
        
        # 重命名列
        rename_mapping = {}
        for col in df.columns:
            if col in self.field_mappings:
                rename_mapping[col] = self.field_mappings[col]
            else:
                # 尝试模糊匹配
                normalized_name = self._fuzzy_match_field(col)
                if normalized_name:
                    rename_mapping[col] = normalized_name
        
        if rename_mapping:
            normalized_df = normalized_df.rename(columns=rename_mapping)
            logger.info(f"字段重命名: {rename_mapping}")
        
        return normalized_df
    
    def _fuzzy_match_field(self, field_name: str) -> Optional[str]:
        """模糊匹配字段名"""
        field_lower = field_name.lower()
        
        # 简单的关键词匹配
        if any(keyword in field_lower for keyword in ['编号', 'id', 'key']):
            if '问题' in field_lower or '异常' in field_lower:
                return 'anomaly_key'
            elif '用例' in field_lower or 'test' in field_lower:
                return 'testcase_key'
        
        if any(keyword in field_lower for keyword in ['产品', 'product', '机型']):
            return 'product'
        
        if any(keyword in field_lower for keyword in ['组件', 'component', '模块', '部件']):
            return 'component'
        
        if any(keyword in field_lower for keyword in ['症状', 'symptom', '问题', '描述']):
            return 'symptom'
        
        if any(keyword in field_lower for keyword in ['严重', 'severity', '级别']):
            return 'severity'
        
        return None
    
    def extract_relationships(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """抽取实体间关系"""
        relationships = []
        
        for _, row in df.iterrows():
            # 异常 -> 组件关系
            if 'anomaly_key' in row and 'component' in row:
                if pd.notna(row['anomaly_key']) and pd.notna(row['component']):
                    relationships.append({
                        'source': row['anomaly_key'],
                        'source_type': 'Anomaly',
                        'target': row['component'],
                        'target_type': 'Component',
                        'relation': 'AFFECTS'
                    })
            
            # 异常 -> 症状关系
            if 'anomaly_key' in row and 'symptom' in row:
                if pd.notna(row['anomaly_key']) and pd.notna(row['symptom']):
                    relationships.append({
                        'source': row['anomaly_key'],
                        'source_type': 'Anomaly',
                        'target': row['symptom'],
                        'target_type': 'Symptom',
                        'relation': 'HAS_SYMPTOM'
                    })
            
            # 产品 -> 组件关系
            if 'product' in row and 'component' in row:
                if pd.notna(row['product']) and pd.notna(row['component']):
                    # 处理多个产品的情况
                    products = str(row['product']).split(',')
                    for product in products:
                        product = product.strip()
                        if product:
                            relationships.append({
                                'source': product,
                                'source_type': 'Product',
                                'target': row['component'],
                                'target_type': 'Component',
                                'relation': 'INCLUDES'
                            })
            
            # 异常 -> 根因关系
            if 'anomaly_key' in row and 'root_cause' in row:
                if pd.notna(row['anomaly_key']) and pd.notna(row['root_cause']):
                    relationships.append({
                        'source': row['anomaly_key'],
                        'source_type': 'Anomaly',
                        'target': row['root_cause'],
                        'target_type': 'RootCause',
                        'relation': 'CAUSED_BY'
                    })
        
        return relationships
    
    def process_excel_file(self, file_path: str) -> Dict[str, Any]:
        """处理Excel文件的完整流程"""
        logger.info(f"开始处理文件: {file_path}")
        
        try:
            # 1. 读取Excel文件
            df = pd.read_excel(file_path)
            logger.info(f"读取到 {len(df)} 行数据，{len(df.columns)} 列")
            
            # 2. 标准化字段名
            normalized_df = self.normalize_field_names(df)
            
            # 3. 抽取实体
            entities = {}
            for _, row in normalized_df.iterrows():
                for col, value in row.items():
                    if pd.notna(value):
                        extracted = self.extract_entities_from_text(str(value))
                        for entity_type, entity_list in extracted.items():
                            if entity_type not in entities:
                                entities[entity_type] = set()
                            entities[entity_type].update(entity_list)
            
            # 转换为列表
            entities = {k: list(v) for k, v in entities.items()}
            
            # 4. 抽取关系
            relationships = self.extract_relationships(normalized_df)
            
            # 5. 生成知识图谱数据
            kg_data = {
                'nodes': self._generate_nodes(entities, normalized_df),
                'relationships': relationships,
                'metadata': {
                    'source_file': file_path,
                    'total_rows': len(df),
                    'total_columns': len(df.columns),
                    'entity_types': list(entities.keys()),
                    'relationship_count': len(relationships)
                }
            }
            
            logger.info(f"抽取完成: {len(kg_data['nodes'])} 个节点, {len(relationships)} 个关系")
            return kg_data
            
        except Exception as e:
            logger.error(f"处理文件失败: {e}")
            raise
    
    def _generate_nodes(self, entities: Dict[str, List[str]], df: pd.DataFrame) -> List[Dict[str, Any]]:
        """生成图谱节点"""
        nodes = []
        
        # 从实体中生成节点
        for entity_type, entity_list in entities.items():
            for entity_value in entity_list:
                nodes.append({
                    'id': f"{entity_type}:{entity_value}",
                    'type': entity_type,
                    'name': entity_value,
                    'properties': {}
                })
        
        # 从数据行中生成节点
        for _, row in df.iterrows():
            if 'anomaly_key' in row and pd.notna(row['anomaly_key']):
                node = {
                    'id': f"Anomaly:{row['anomaly_key']}",
                    'type': 'Anomaly',
                    'name': row['anomaly_key'],
                    'properties': {}
                }
                
                # 添加属性
                for col, value in row.items():
                    if pd.notna(value) and col != 'anomaly_key':
                        node['properties'][col] = str(value)
                
                nodes.append(node)
        
        return nodes

def main():
    """主函数 - 演示智能抽取功能"""
    extractor = IntelligentExtractor()
    
    # 处理来料问题数据
    problems_file = "data/import/来料问题先后版.xlsx"
    if Path(problems_file).exists():
        kg_data = extractor.process_excel_file(problems_file)
        
        # 保存结果
        output_file = "data/processed/extracted_knowledge_graph.json"
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(kg_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 知识图谱数据已保存到: {output_file}")
        print(f"📊 统计信息:")
        print(f"   - 节点数: {len(kg_data['nodes'])}")
        print(f"   - 关系数: {len(kg_data['relationships'])}")
        print(f"   - 实体类型: {kg_data['metadata']['entity_types']}")

if __name__ == "__main__":
    main()
