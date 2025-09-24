#!/usr/bin/env python3
"""
Excel数据处理器
用于将Excel中的测试用例和异常数据导入到Neo4j
"""

import pandas as pd
import os
import sys
from pathlib import Path
from typing import Dict, List, Any
import logging

# 添加父目录到路径，以便导入API模块
sys.path.append(str(Path(__file__).parent.parent / "api"))

from database.neo4j_client import Neo4jClient
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExcelProcessor:
    def __init__(self):
        self.neo4j_client = Neo4jClient(
            uri=os.getenv("NEO4J_URI", "bolt://localhost:7687"),
            user=os.getenv("NEO4J_USER", "neo4j"),
            password=os.getenv("NEO4J_PASS", "password123")
        )
    
    def process_test_cases_excel(self, file_path: str) -> bool:
        """
        处理测试用例Excel文件
        期望的Excel格式：
        - 产品名称 | 组件名称 | 用例ID | 用例标题 | 用例描述 | 优先级 | 类型 | 测试步骤 | 期望结果
        """
        try:
            df = pd.read_excel(file_path)
            logger.info(f"读取Excel文件: {file_path}, 共{len(df)}行数据")
            
            # 检查必要的列
            required_columns = ['产品名称', '组件名称', '用例ID', '用例标题']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                logger.error(f"缺少必要的列: {missing_columns}")
                return False
            
            success_count = 0
            for index, row in df.iterrows():
                try:
                    # 创建或更新产品
                    self._upsert_product(row['产品名称'])
                    
                    # 创建或更新组件
                    self._upsert_component(row['组件名称'])
                    
                    # 建立产品-组件关系
                    self._create_product_component_relation(row['产品名称'], row['组件名称'])
                    
                    # 创建测试用例
                    self._upsert_test_case(row)
                    
                    # 建立测试用例-组件关系
                    self._create_testcase_component_relation(row['用例ID'], row['组件名称'])
                    
                    success_count += 1
                    
                except Exception as e:
                    logger.error(f"处理第{index+1}行数据失败: {e}")
                    continue
            
            logger.info(f"成功处理 {success_count}/{len(df)} 条测试用例数据")
            return True
            
        except Exception as e:
            logger.error(f"处理Excel文件失败: {e}")
            return False
    
    def process_anomaly_excel(self, file_path: str) -> bool:
        """
        处理异常数据Excel文件
        期望的Excel格式：
        - 异常ID | 异常标题 | 异常描述 | 严重程度 | 状态 | 组件名称 | 症状描述 | 根因描述 | 对策描述 | 创建日期 | 报告人
        """
        try:
            df = pd.read_excel(file_path)
            logger.info(f"读取异常Excel文件: {file_path}, 共{len(df)}行数据")
            
            # 检查必要的列
            required_columns = ['异常ID', '异常标题', '组件名称']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                logger.error(f"缺少必要的列: {missing_columns}")
                return False
            
            success_count = 0
            for index, row in df.iterrows():
                try:
                    # 创建异常
                    self._upsert_anomaly(row)
                    
                    # 创建症状（如果有）
                    if pd.notna(row.get('症状描述')):
                        self._upsert_symptom(row['症状描述'])
                        self._create_anomaly_symptom_relation(row['异常ID'], row['症状描述'])
                    
                    # 创建根因（如果有）
                    if pd.notna(row.get('根因描述')):
                        self._upsert_root_cause(row['根因描述'])
                        self._create_anomaly_root_cause_relation(row['异常ID'], row['根因描述'])
                    
                    # 创建对策（如果有）
                    if pd.notna(row.get('对策描述')):
                        self._upsert_countermeasure(row['对策描述'])
                        self._create_anomaly_countermeasure_relation(row['异常ID'], row['对策描述'])
                    
                    # 建立异常-组件关系
                    self._create_anomaly_component_relation(row['异常ID'], row['组件名称'])
                    
                    success_count += 1
                    
                except Exception as e:
                    logger.error(f"处理第{index+1}行异常数据失败: {e}")
                    continue
            
            logger.info(f"成功处理 {success_count}/{len(df)} 条异常数据")
            return True
            
        except Exception as e:
            logger.error(f"处理异常Excel文件失败: {e}")
            return False
    
    def _upsert_product(self, product_name: str):
        """创建或更新产品"""
        query = """
        MERGE (p:Product {name: $name})
        SET p.status = 'active'
        RETURN p.name
        """
        self.neo4j_client.execute_write(query, {"name": product_name})
    
    def _upsert_component(self, component_name: str):
        """创建或更新组件"""
        query = """
        MERGE (c:Component {name: $name})
        SET c.type = 'unknown'
        RETURN c.name
        """
        self.neo4j_client.execute_write(query, {"name": component_name})
    
    def _create_product_component_relation(self, product_name: str, component_name: str):
        """建立产品-组件关系"""
        query = """
        MATCH (p:Product {name: $product_name})
        MATCH (c:Component {name: $component_name})
        MERGE (p)-[:HAS_COMPONENT]->(c)
        """
        self.neo4j_client.execute_write(query, {
            "product_name": product_name,
            "component_name": component_name
        })
    
    def _upsert_test_case(self, row: pd.Series):
        """创建或更新测试用例"""
        query = """
        MERGE (tc:TestCase {id: $id})
        SET tc.title = $title,
            tc.description = $description,
            tc.priority = $priority,
            tc.type = $type,
            tc.steps = $steps,
            tc.expected_result = $expected_result
        RETURN tc.id
        """
        
        # 处理测试步骤（可能是字符串，需要转换为列表）
        steps = row.get('测试步骤', '')
        if isinstance(steps, str) and steps:
            steps = [step.strip() for step in steps.split('\n') if step.strip()]
        else:
            steps = []
        
        self.neo4j_client.execute_write(query, {
            "id": row['用例ID'],
            "title": row['用例标题'],
            "description": row.get('用例描述', ''),
            "priority": row.get('优先级', 'medium'),
            "type": row.get('类型', 'functional'),
            "steps": steps,
            "expected_result": row.get('期望结果', '')
        })
    
    def _create_testcase_component_relation(self, testcase_id: str, component_name: str):
        """建立测试用例-组件关系"""
        query = """
        MATCH (tc:TestCase {id: $testcase_id})
        MATCH (c:Component {name: $component_name})
        MERGE (tc)-[:TESTS]->(c)
        """
        self.neo4j_client.execute_write(query, {
            "testcase_id": testcase_id,
            "component_name": component_name
        })
    
    def _upsert_anomaly(self, row: pd.Series):
        """创建或更新异常"""
        query = """
        MERGE (a:Anomaly {id: $id})
        SET a.title = $title,
            a.description = $description,
            a.severity = $severity,
            a.status = $status,
            a.created_date = $created_date,
            a.reporter = $reporter
        RETURN a.id
        """
        self.neo4j_client.execute_write(query, {
            "id": row['异常ID'],
            "title": row['异常标题'],
            "description": row.get('异常描述', ''),
            "severity": row.get('严重程度', 'medium'),
            "status": row.get('状态', 'open'),
            "created_date": str(row.get('创建日期', '')),
            "reporter": row.get('报告人', '')
        })
    
    def _upsert_symptom(self, description: str):
        """创建症状"""
        query = """
        MERGE (s:Symptom {description: $description})
        RETURN s.description
        """
        self.neo4j_client.execute_write(query, {"description": description})
    
    def _upsert_root_cause(self, description: str):
        """创建根因"""
        query = """
        MERGE (rc:RootCause {description: $description})
        RETURN rc.description
        """
        self.neo4j_client.execute_write(query, {"description": description})
    
    def _upsert_countermeasure(self, description: str):
        """创建对策"""
        query = """
        MERGE (cm:Countermeasure {description: $description})
        RETURN cm.description
        """
        self.neo4j_client.execute_write(query, {"description": description})
    
    def _create_anomaly_symptom_relation(self, anomaly_id: str, symptom_description: str):
        """建立异常-症状关系"""
        query = """
        MATCH (a:Anomaly {id: $anomaly_id})
        MATCH (s:Symptom {description: $symptom_description})
        MERGE (a)-[:HAS_SYMPTOM]->(s)
        """
        self.neo4j_client.execute_write(query, {
            "anomaly_id": anomaly_id,
            "symptom_description": symptom_description
        })
    
    def _create_anomaly_root_cause_relation(self, anomaly_id: str, root_cause_description: str):
        """建立异常-根因关系"""
        query = """
        MATCH (a:Anomaly {id: $anomaly_id})
        MATCH (rc:RootCause {description: $root_cause_description})
        MERGE (a)-[:CAUSED_BY]->(rc)
        """
        self.neo4j_client.execute_write(query, {
            "anomaly_id": anomaly_id,
            "root_cause_description": root_cause_description
        })
    
    def _create_anomaly_countermeasure_relation(self, anomaly_id: str, countermeasure_description: str):
        """建立异常-对策关系"""
        query = """
        MATCH (a:Anomaly {id: $anomaly_id})
        MATCH (cm:Countermeasure {description: $countermeasure_description})
        MERGE (a)-[:SOLVED_BY]->(cm)
        """
        self.neo4j_client.execute_write(query, {
            "anomaly_id": anomaly_id,
            "countermeasure_description": countermeasure_description
        })
    
    def _create_anomaly_component_relation(self, anomaly_id: str, component_name: str):
        """建立异常-组件关系"""
        query = """
        MATCH (a:Anomaly {id: $anomaly_id})
        MATCH (c:Component {name: $component_name})
        MERGE (a)-[:OCCURS_IN]->(c)
        """
        self.neo4j_client.execute_write(query, {
            "anomaly_id": anomaly_id,
            "component_name": component_name
        })
    
    def close(self):
        """关闭连接"""
        self.neo4j_client.close()

def main():
    """主函数"""
    processor = ExcelProcessor()
    
    try:
        # 检查数据目录
        raw_data_dir = Path("../../data/raw")
        if not raw_data_dir.exists():
            logger.error("数据目录不存在: ../../data/raw")
            return
        
        # 处理测试用例文件
        test_case_files = list(raw_data_dir.glob("*测试用例*.xlsx"))
        for file_path in test_case_files:
            logger.info(f"处理测试用例文件: {file_path}")
            processor.process_test_cases_excel(str(file_path))
        
        # 处理异常数据文件
        anomaly_files = list(raw_data_dir.glob("*异常*.xlsx"))
        for file_path in anomaly_files:
            logger.info(f"处理异常数据文件: {file_path}")
            processor.process_anomaly_excel(str(file_path))
        
        if not test_case_files and not anomaly_files:
            logger.info("未找到Excel文件，请将文件放在 data/raw/ 目录下")
            logger.info("文件命名建议：")
            logger.info("  - 测试用例文件：包含'测试用例'关键词")
            logger.info("  - 异常数据文件：包含'异常'关键词")
    
    finally:
        processor.close()

if __name__ == "__main__":
    main()
