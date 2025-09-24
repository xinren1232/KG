#!/usr/bin/env python3
"""
增强版ETL管线
集成智能抽取器，支持多种Excel格式的自动适配和知识图谱构建
"""
import sys
import json
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime

# 添加项目路径
sys.path.append(str(Path(__file__).parent.parent.parent))

from services.nlp.intelligent_extractor import IntelligentExtractor

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedETLPipeline:
    """增强版ETL管线"""
    
    def __init__(self):
        self.extractor = IntelligentExtractor()
        self.supported_formats = ['.xlsx', '.xls', '.csv']
        
    def detect_file_type(self, file_path: str) -> str:
        """检测文件类型和内容特征"""
        path = Path(file_path)
        
        if path.suffix.lower() not in self.supported_formats:
            raise ValueError(f"不支持的文件格式: {path.suffix}")
        
        # 读取文件并分析内容
        try:
            if path.suffix.lower() in ['.xlsx', '.xls']:
                df = pd.read_excel(file_path)
            else:
                df = pd.read_csv(file_path)
            
            # 基于列名和内容判断文件类型
            columns = [col.lower() for col in df.columns]
            
            # 异常/问题数据特征
            anomaly_keywords = ['问题', '异常', '缺陷', '故障', 'anomaly', 'issue', 'defect']
            if any(keyword in ' '.join(columns) for keyword in anomaly_keywords):
                return 'anomaly_data'
            
            # 测试用例数据特征
            testcase_keywords = ['用例', '测试', 'test', 'case', 'tc-']
            if any(keyword in ' '.join(columns) for keyword in testcase_keywords):
                return 'testcase_data'
            
            # 供应商数据特征
            supplier_keywords = ['供应商', '来料', '批次', 'supplier', 'vendor']
            if any(keyword in ' '.join(columns) for keyword in supplier_keywords):
                return 'supplier_data'
            
            # 默认为通用数据
            return 'generic_data'
            
        except Exception as e:
            logger.error(f"文件类型检测失败: {e}")
            return 'unknown'
    
    def process_file(self, file_path: str, file_type: Optional[str] = None) -> Dict[str, Any]:
        """处理单个文件"""
        logger.info(f"开始处理文件: {file_path}")
        
        # 自动检测文件类型
        if not file_type:
            file_type = self.detect_file_type(file_path)
        
        logger.info(f"文件类型: {file_type}")
        
        # 使用智能抽取器处理
        kg_data = self.extractor.process_excel_file(file_path)
        
        # 根据文件类型进行特定处理
        processed_data = self._process_by_type(kg_data, file_type)
        
        # 数据标准化
        normalized_data = self._normalize_data(processed_data)
        
        # 生成入库脚本
        cypher_scripts = self._generate_cypher_scripts(normalized_data)
        
        return {
            'file_path': file_path,
            'file_type': file_type,
            'raw_data': kg_data,
            'processed_data': processed_data,
            'normalized_data': normalized_data,
            'cypher_scripts': cypher_scripts,
            'metadata': {
                'processed_at': datetime.now().isoformat(),
                'node_count': len(normalized_data.get('nodes', [])),
                'relationship_count': len(normalized_data.get('relationships', []))
            }
        }
    
    def _process_by_type(self, kg_data: Dict[str, Any], file_type: str) -> Dict[str, Any]:
        """根据文件类型进行特定处理"""
        processed = kg_data.copy()
        
        if file_type == 'anomaly_data':
            processed = self._process_anomaly_data(kg_data)
        elif file_type == 'testcase_data':
            processed = self._process_testcase_data(kg_data)
        elif file_type == 'supplier_data':
            processed = self._process_supplier_data(kg_data)
        
        return processed
    
    def _process_anomaly_data(self, kg_data: Dict[str, Any]) -> Dict[str, Any]:
        """处理异常数据"""
        logger.info("处理异常数据特定逻辑")
        
        # 增强异常数据的关系抽取
        enhanced_relationships = []
        
        for rel in kg_data.get('relationships', []):
            enhanced_relationships.append(rel)
            
            # 为异常数据添加额外的推理关系
            if rel['relation'] == 'AFFECTS' and rel['source_type'] == 'Anomaly':
                # 添加严重程度关系
                enhanced_relationships.append({
                    'source': rel['source'],
                    'source_type': 'Anomaly',
                    'target': 'S1',  # 从数据中提取实际严重程度
                    'target_type': 'Severity',
                    'relation': 'HAS_SEVERITY'
                })
        
        kg_data['relationships'] = enhanced_relationships
        return kg_data
    
    def _process_testcase_data(self, kg_data: Dict[str, Any]) -> Dict[str, Any]:
        """处理测试用例数据"""
        logger.info("处理测试用例数据特定逻辑")
        
        # 为测试用例添加执行关系
        enhanced_relationships = kg_data.get('relationships', []).copy()
        
        for node in kg_data.get('nodes', []):
            if node['type'] == 'TestCase':
                # 添加测试用例与产品的关系
                if 'related_products' in node.get('properties', {}):
                    products = node['properties']['related_products'].split(',')
                    for product in products:
                        product = product.strip()
                        if product:
                            enhanced_relationships.append({
                                'source': node['name'],
                                'source_type': 'TestCase',
                                'target': product,
                                'target_type': 'Product',
                                'relation': 'TESTS'
                            })
        
        kg_data['relationships'] = enhanced_relationships
        return kg_data
    
    def _process_supplier_data(self, kg_data: Dict[str, Any]) -> Dict[str, Any]:
        """处理供应商数据"""
        logger.info("处理供应商数据特定逻辑")
        
        # 为供应商数据添加供应关系
        enhanced_relationships = kg_data.get('relationships', []).copy()
        
        for rel in kg_data.get('relationships', []):
            if rel['source_type'] == 'Supplier' and rel['target_type'] == 'Component':
                # 添加供应关系
                enhanced_relationships.append({
                    'source': rel['source'],
                    'source_type': 'Supplier',
                    'target': rel['target'],
                    'target_type': 'Component',
                    'relation': 'SUPPLIES'
                })
        
        kg_data['relationships'] = enhanced_relationships
        return kg_data
    
    def _normalize_data(self, processed_data: Dict[str, Any]) -> Dict[str, Any]:
        """数据标准化"""
        logger.info("执行数据标准化")
        
        normalized = processed_data.copy()
        
        # 标准化节点
        normalized_nodes = []
        for node in processed_data.get('nodes', []):
            normalized_node = {
                'key': self._generate_node_key(node),
                'type': node['type'],
                'name': node['name'],
                'properties': node.get('properties', {})
            }
            normalized_nodes.append(normalized_node)
        
        # 标准化关系
        normalized_relationships = []
        for rel in processed_data.get('relationships', []):
            normalized_rel = {
                'source_key': self._generate_entity_key(rel['source'], rel['source_type']),
                'target_key': self._generate_entity_key(rel['target'], rel['target_type']),
                'relation_type': rel['relation'],
                'properties': rel.get('properties', {})
            }
            normalized_relationships.append(normalized_rel)
        
        normalized['nodes'] = normalized_nodes
        normalized['relationships'] = normalized_relationships
        
        return normalized
    
    def _generate_node_key(self, node: Dict[str, Any]) -> str:
        """生成节点唯一键"""
        return f"{node['type']}:{node['name']}"
    
    def _generate_entity_key(self, name: str, entity_type: str) -> str:
        """生成实体唯一键"""
        return f"{entity_type}:{name}"
    
    def _generate_cypher_scripts(self, normalized_data: Dict[str, Any]) -> List[str]:
        """生成Cypher入库脚本"""
        scripts = []
        
        # 生成节点创建脚本
        for node in normalized_data.get('nodes', []):
            cypher = f"""
MERGE (n:Entity:{node['type']} {{key: '{node['key']}'}})
SET n.name = '{node['name']}'
"""
            # 添加属性
            for prop_key, prop_value in node.get('properties', {}).items():
                if prop_value:
                    cypher += f", n.{prop_key} = '{str(prop_value).replace("'", "\\'")}'"
            
            scripts.append(cypher.strip())
        
        # 生成关系创建脚本
        for rel in normalized_data.get('relationships', []):
            cypher = f"""
MATCH (a:Entity {{key: '{rel['source_key']}'}})
MATCH (b:Entity {{key: '{rel['target_key']}'}})
MERGE (a)-[r:{rel['relation_type']}]->(b)
"""
            scripts.append(cypher.strip())
        
        return scripts
    
    def process_directory(self, directory_path: str) -> Dict[str, Any]:
        """批量处理目录中的文件"""
        logger.info(f"批量处理目录: {directory_path}")
        
        directory = Path(directory_path)
        if not directory.exists():
            raise FileNotFoundError(f"目录不存在: {directory_path}")
        
        results = {}
        
        # 查找所有支持的文件
        for file_path in directory.rglob('*'):
            if file_path.suffix.lower() in self.supported_formats:
                try:
                    result = self.process_file(str(file_path))
                    results[str(file_path)] = result
                    logger.info(f"✅ 处理完成: {file_path}")
                except Exception as e:
                    logger.error(f"❌ 处理失败: {file_path}, 错误: {e}")
                    results[str(file_path)] = {'error': str(e)}
        
        return results
    
    def save_results(self, results: Dict[str, Any], output_dir: str):
        """保存处理结果"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # 保存完整结果
        results_file = output_path / 'etl_results.json'
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        # 保存Cypher脚本
        cypher_file = output_path / 'import_scripts.cypher'
        with open(cypher_file, 'w', encoding='utf-8') as f:
            for file_path, result in results.items():
                if 'cypher_scripts' in result:
                    f.write(f"// Scripts for {file_path}\n")
                    for script in result['cypher_scripts']:
                        f.write(script + ";\n\n")
        
        logger.info(f"结果已保存到: {output_path}")

def main():
    """主函数"""
    pipeline = EnhancedETLPipeline()
    
    # 处理导入目录中的所有文件
    import_dir = "data/import"
    results = pipeline.process_directory(import_dir)
    
    # 保存结果
    pipeline.save_results(results, "data/processed/etl_output")
    
    # 打印统计信息
    print("🎉 ETL处理完成!")
    print(f"📁 处理文件数: {len(results)}")
    
    total_nodes = 0
    total_relationships = 0
    
    for file_path, result in results.items():
        if 'metadata' in result:
            total_nodes += result['metadata'].get('node_count', 0)
            total_relationships += result['metadata'].get('relationship_count', 0)
            print(f"   📄 {Path(file_path).name}: {result['metadata'].get('node_count', 0)} 节点, {result['metadata'].get('relationship_count', 0)} 关系")
    
    print(f"📊 总计: {total_nodes} 节点, {total_relationships} 关系")

if __name__ == "__main__":
    main()
